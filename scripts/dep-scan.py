#!/usr/bin/env python3
"""Scan direct (Tier 2) or full transitive (Tier 3, npm only) dependencies for known CVEs.

Uses the OSV batch API. Never installs the audited package: Tier 3 resolves a
lockfile only (npm --package-lock-only --ignore-scripts) in a temp dir that is
always deleted, so no package code or install script runs.

  Tier 2 (default): scan direct deps from registry metadata.
  Tier 3: resolve the full dep tree via npm; falls back to Tier 2 if the npm CLI
          is unavailable or lock generation fails.

Cache: scripts/.dep-scan-cache/<eco>-<name>[-<ver>]-t<tier>.json, TTL 24 hr.

Python twin of dep-scan.ps1: same flags, same JSON keys. Change both together.
Intentional divergences from the .ps1: arrays are always emitted as arrays; the
Tier 3 `npm install` is bounded by a 300 s timeout (the .ps1 waits forever) and a
timeout falls back to Tier 2 with a fallbackReason.

Output (JSON to stdout):
    {ecosystem, package, tier, directDepCount, findings: [{name, ecosystem, version,
     severity, cveIds, depth}], mediumCount, lowCount, riskLevel, fallback,
     sources: ["OSV"], cacheHit, version?, transitiveDepCount?, fallbackReason?,
     limitationNote?}
"""
import argparse
import gzip
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
USER_AGENT = "install-auditor/1.0"
ECOSYSTEMS = ["npm", "pypi", "crates", "rubygems", "nuget", "go", "maven", "hex"]
CACHE_DIR = ".dep-scan-cache"
NPM_TIMEOUT_SECONDS = 300

OSV_ECO_MAP = {"npm": "npm", "pypi": "PyPI", "crates": "crates.io", "rubygems": "RubyGems",
               "nuget": "NuGet", "go": "Go", "maven": "Maven", "hex": "Hex"}


def http_json(url, method="GET", body=None, headers=None, timeout=15):
    """Return parsed JSON. Raises on network, HTTP >= 400, or decode errors."""
    h = {"User-Agent": USER_AGENT}
    if headers:
        h.update(headers)
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        h["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
        # urllib does not decompress; Invoke-RestMethod does. Handle gzip bodies
        # explicitly so every registry behaves the same as in the .ps1.
        if resp.headers.get("Content-Encoding", "").lower() == "gzip" or raw[:2] == b"\x1f\x8b":
            raw = gzip.decompress(raw)
    return json.loads(raw.decode("utf-8"))


def cache_path(dirname, key):
    d = os.path.join(SCRIPT_DIR, dirname)
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, key + ".json")


def read_cache(dirname, key, ttl_hours):
    try:
        p = cache_path(dirname, key)
        if time.time() - os.path.getmtime(p) > ttl_hours * 3600:
            return None
        with open(p, encoding="utf-8-sig") as f:  # -sig: tolerate BOM from Windows PowerShell writes
            return json.load(f)
    except Exception:
        return None


def write_cache(dirname, key, data):
    try:
        with open(cache_path(dirname, key), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception:
        pass  # non-fatal, as in the .ps1 (also covers scoped names whose "/" makes the path invalid)


def emit(obj):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    sys.stdout.write(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def normalize_severity(sev):
    s = str(sev).lower() if sev is not None else ""
    if s in ("critical", "high", "low"):
        return s
    if s in ("moderate", "medium"):
        return "medium"
    return "medium"


def get_severity_from_osv(vuln):
    # database_specific.severity (HIGH/MODERATE/LOW/CRITICAL) wins over CVSS scores.
    db = vuln.get("database_specific")
    if db and db.get("severity"):
        return normalize_severity(db["severity"])
    for s in vuln.get("severity") or []:
        score = str(s.get("score")) if isinstance(s, dict) and s.get("score") is not None else ""
        if re.match(r"^[0-9]+(\.[0-9]+)?$", score):
            v = float(score)
            if v >= 9.0:
                return "critical"
            if v >= 7.0:
                return "high"
            if v >= 4.0:
                return "medium"
            return "low"
    return "medium"


def get_risk_level(severities):
    order = {"none": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}
    highest = "none"
    for s in severities:
        if s and s in order and order[s] > order[highest]:
            highest = s
    return highest


def get_npm_deps(pkg_name, pkg_version):
    # The npm registry accepts the literal package name, including "@" and "/" of scoped packages.
    ver = pkg_version if pkg_version else "latest"
    resp = http_json("https://registry.npmjs.org/%s/%s" % (pkg_name, ver), timeout=20)
    return [{"Name": k, "VersionRange": v} for k, v in (resp.get("dependencies") or {}).items()]


def get_pypi_deps(pkg_name, pkg_version):
    seg = pkg_version + "/" if pkg_version else ""
    resp = http_json("https://pypi.org/pypi/%s/%sjson" % (pkg_name, seg), timeout=20)
    deps = []
    for req in (resp.get("info") or {}).get("requires_dist") or []:
        r = re.sub(r"\[[^\]]*\]", "", req)               # strip extras: pkg[extra] -> pkg
        r = r.split(";")[0].strip()                      # strip env markers: req ; marker
        dep_name = re.split(r"[>=<!~\s]", r)[0].strip()  # strip version specifiers
        if dep_name:
            deps.append({"Name": dep_name, "VersionRange": None})
    return deps


def get_npm_full_tree(pkg_name, pkg_version):
    """Return [{Name, Version}] for every package in the resolved dep tree.

    Raises RuntimeError with a descriptive message; the caller records it as fallbackReason.
    The npm flags --package-lock-only --ignore-scripts are what guarantee no audited
    code runs: do not drop or reorder them, and do not use `npm ci`/`npm install` without them.
    """
    npm = shutil.which("npm")  # resolves npm.cmd on Windows via PATHEXT
    if not npm:
        raise RuntimeError("npm CLI unavailable")

    try:
        out = subprocess.run([npm, "--version"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             timeout=60, universal_newlines=True)
        npm_ver = out.stdout.strip()
        major = int(npm_ver.split(".")[0])
        if major < 6:
            raise RuntimeError("npm %s is below minimum required version 6" % npm_ver)
    except Exception as e:
        raise RuntimeError("npm version check failed: %s" % e)

    tmp = tempfile.mkdtemp()
    try:
        with open(os.path.join(tmp, "package.json"), "w", encoding="utf-8") as f:
            json.dump({"dependencies": {pkg_name: pkg_version if pkg_version else "*"}}, f)

        try:
            r = subprocess.run([npm, "install", "--package-lock-only", "--ignore-scripts", "--silent"],
                               cwd=tmp, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                               timeout=NPM_TIMEOUT_SECONDS)
        except subprocess.TimeoutExpired:
            raise RuntimeError("npm install --package-lock-only timed out after %d s" % NPM_TIMEOUT_SECONDS)
        if r.returncode != 0:
            raise RuntimeError("npm install --package-lock-only failed (exit %d)" % r.returncode)

        lock_path = os.path.join(tmp, "package-lock.json")
        if not os.path.exists(lock_path):
            raise RuntimeError("package-lock.json was not generated")

        with open(lock_path, encoding="utf-8") as f:
            lock = json.load(f)
        packages = []
        if lock.get("packages"):
            # Lockfile v2/v3: keys like "node_modules/foo", "node_modules/@scope/name",
            # "node_modules/a/node_modules/b"; "" is the root entry.
            for key, entry in lock["packages"].items():
                if key == "":
                    continue
                dep_name = re.sub(r"^(.*node_modules/)", "", key)
                dep_ver = (entry or {}).get("version")
                if dep_name and dep_ver:
                    packages.append({"Name": dep_name, "Version": dep_ver})
        elif lock.get("dependencies"):
            # Lockfile v1: flat dependency map
            for key, entry in lock["dependencies"].items():
                if (entry or {}).get("version"):
                    packages.append({"Name": key, "Version": entry["version"]})
        return packages
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def invoke_osv_batch(queries):
    """queries: [{Name, Ecosystem, Version?}]. Returns a list parallel to queries of {vulns: [...]}."""
    if not queries:
        return []

    all_results = []
    batch_size = 1000
    for i in range(0, len(queries), batch_size):
        batch = queries[i:i + batch_size]

        query_objs = []
        for q in batch:
            obj = {"package": {"ecosystem": q["Ecosystem"], "name": q["Name"]}}
            if q.get("Version"):
                obj["version"] = q["Version"]
            query_objs.append(obj)

        resp = http_json("https://api.osv.dev/v1/querybatch", method="POST",
                         body={"queries": query_objs}, timeout=30)

        if resp and resp.get("results"):
            raw_results = list(resp["results"])
        else:
            # Keep results parallel to the queries on an unexpected empty response.
            raw_results = [{"vulns": []} for _ in batch]

        # querybatch returns stubs {id, modified}, not full records; fetch each full record.
        enrich_cache = {}
        for result in raw_results:
            full_vulns = []
            for v in (result or {}).get("vulns") or []:
                is_stub = (v.get("id") and not v.get("database_specific")
                           and not v.get("severity") and not v.get("aliases"))
                if is_stub:
                    vid = v["id"]
                    if vid not in enrich_cache:
                        try:
                            enrich_cache[vid] = http_json("https://api.osv.dev/v1/vulns/" + vid, timeout=15)
                        except Exception:
                            enrich_cache[vid] = v  # keep the stub; severity defaults to 'medium'
                    full_vulns.append(enrich_cache[vid])
                else:
                    full_vulns.append(v)  # already a full record
            all_results.append({"vulns": full_vulns})
    return all_results


def get_dep_findings(ecosystem, deps, osv_results):
    findings = []
    medium_count = 0
    low_count = 0
    all_severities = []

    for i, dep in enumerate(deps):
        result = osv_results[i] if i < len(osv_results) else None
        vulns = list(result["vulns"]) if result and result.get("vulns") else []
        if not vulns:
            continue

        dep_sevs = [get_severity_from_osv(v) for v in vulns]
        cve_ids = sorted({a for v in vulns for a in (v.get("aliases") or []) if re.match(r"^CVE-", a, re.I)})
        dep_worst = get_risk_level(dep_sevs)
        all_severities.append(dep_worst)

        if dep_worst in ("high", "critical"):
            findings.append({
                "name": dep["Name"],
                "ecosystem": ecosystem,
                "version": dep.get("Version") or dep.get("VersionRange") or None,
                "severity": dep_worst,
                "cveIds": cve_ids,
                "depth": dep.get("Depth"),
            })
        elif dep_worst == "medium":
            medium_count += 1
        elif dep_worst == "low":
            low_count += 1

    return {"Findings": findings, "MediumCount": medium_count, "LowCount": low_count,
            "AllSeverities": all_severities}


def build_parser():
    p = argparse.ArgumentParser(prog="dep-scan.py", allow_abbrev=False, description=__doc__.splitlines()[0])
    p.add_argument("-Ecosystem", "--ecosystem", dest="ecosystem", required=True, type=str.lower, choices=ECOSYSTEMS,
                   help="registry ecosystem")
    p.add_argument("-Name", "--name", dest="name", required=True, help="target package name")
    p.add_argument("-Version", "--version", dest="version",
                   help="target package version (selects the version manifest when fetching deps)")
    p.add_argument("-Tier", "--tier", dest="tier", type=int, choices=[2, 3], default=2,
                   help="2: direct deps (default); 3: full transitive tree, npm only")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    eco, name, version, tier = args.ecosystem, args.name, args.version, args.tier

    cache_key = "%s-%s%s-t%d" % (eco, name, "-" + version if version else "", tier)
    cached = read_cache(CACHE_DIR, cache_key, 24)
    if cached:
        cached["cacheHit"] = True
        emit(cached)
        return 0

    fallback = False
    fallback_reason = None
    limitation_note = None
    transitive_dep_count = None

    try:
        if eco == "npm":
            direct_deps = get_npm_deps(name, version)
        elif eco == "pypi":
            direct_deps = get_pypi_deps(name, version)
        else:
            direct_deps = []
            limitation_note = ("Direct dep resolution is not supported for ecosystem '%s'. "
                               "Supported: npm, pypi." % eco)
        direct_dep_count = len(direct_deps)

        all_deps = None
        if tier == 3:
            if eco != "npm":
                fallback = True
                fallback_reason = ("Tier 3 full-tree resolution is only supported for npm; "
                                   "falling back to Tier 2 direct-dep scan.")
            else:
                try:
                    tree_packages = get_npm_full_tree(name, version)
                    transitive_dep_count = len(tree_packages)
                    direct_names = {d["Name"].lower() for d in direct_deps}
                    all_deps = [{
                        "Name": p["Name"],
                        "Version": p["Version"],
                        "VersionRange": None,
                        "Depth": 1 if p["Name"].lower() in direct_names else 2,
                    } for p in tree_packages]
                except Exception as e:
                    fallback = True
                    fallback_reason = str(e)

        if all_deps is None:
            all_deps = [{"Name": d["Name"], "Version": None, "VersionRange": d["VersionRange"], "Depth": 1}
                        for d in direct_deps]

        osv_eco = OSV_ECO_MAP[eco]
        queries = [{"Name": d["Name"], "Ecosystem": osv_eco, "Version": d["Version"]} for d in all_deps]
        osv_results = invoke_osv_batch(queries) if queries else []

        processed = get_dep_findings(eco, all_deps, osv_results)
        risk_level = get_risk_level(processed["AllSeverities"])

        effective_tier = 2 if (fallback and tier == 3) else tier
        output = {
            "ecosystem": eco,
            "package": name,
            "tier": effective_tier,
            "directDepCount": direct_dep_count,
            "findings": processed["Findings"],
            "mediumCount": processed["MediumCount"],
            "lowCount": processed["LowCount"],
            "riskLevel": risk_level,
            "fallback": fallback,
            "sources": ["OSV"],
            "cacheHit": False,
        }
        if version:
            output["version"] = version
        if transitive_dep_count is not None:
            output["transitiveDepCount"] = transitive_dep_count
        if fallback_reason:
            output["fallbackReason"] = fallback_reason
        if limitation_note:
            output["limitationNote"] = limitation_note

        write_cache(CACHE_DIR, cache_key, output)
        emit(output)
    except Exception as e:
        emit({
            "ecosystem": eco,
            "package": name,
            "tier": tier,
            "error": str(e),
            "riskLevel": "unknown",
            "fallback": False,
            "cacheHit": False,
        })
    return 0


if __name__ == "__main__":
    sys.exit(main())
