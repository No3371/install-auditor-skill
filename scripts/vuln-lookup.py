#!/usr/bin/env python3
"""Query OSV.dev and the GitHub Advisory Database (GHSA) for known vulnerabilities.

Runs structured CVE lookups for registry packages, normalizes results, filters by
version if supplied, detects cross-DB discrepancies and emits a JSON risk
assessment to stdout.

GITHUB_TOKEN: set it in the environment to raise the GHSA rate limit 60 -> 5000/hr.
If unset or rate-limited, GHSA is skipped and OSV-only results are returned.
Cache: scripts/.vuln-cache/<eco>-<name>[-<ver>].json, TTL 24 hr.

Python twin of vuln-lookup.ps1: same flags, same JSON keys. Change both together.

Output (JSON to stdout):
    {ecosystem, package, osvResults: [{id, aliases, summary, severity, affectedVersions}],
     ghsaResults: [...], summary: {totalCount, osvCount, ghsaCount, highestSeverity},
     discrepancies: {onlyInOsv, onlyInGhsa}, sources, riskLevel, version?, ghsaNote?}
"""
import argparse
import gzip
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
USER_AGENT = "install-auditor/1.0"
ECOSYSTEMS = ["npm", "pypi", "crates", "rubygems", "nuget", "go", "maven", "hex"]
CACHE_DIR = ".vuln-cache"

OSV_ECO_MAP = {"npm": "npm", "pypi": "PyPI", "crates": "crates.io", "rubygems": "RubyGems",
               "nuget": "NuGet", "go": "Go", "maven": "Maven", "hex": "Hex"}
GHSA_ECO_MAP = {"npm": "npm", "pypi": "pip", "crates": "rust", "rubygems": "rubygems",
                "nuget": "nuget", "go": "go", "maven": "maven", "hex": "erlang"}


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


def _ieq(a, b):
    """PowerShell -eq on strings: case-insensitive."""
    return a is not None and b is not None and str(a).lower() == str(b).lower()


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


_SYSVER = re.compile(r"[0-9]+(\.[0-9]+){1,3}")


def _to_sysver(s):
    """[System.Version] cast: 2-4 numeric parts; missing parts sort as -1 (so 1.2 < 1.2.0)."""
    t = re.sub(r"[-+].*$", "", re.sub(r"^v", "", s, flags=re.I)).strip()
    if not _SYSVER.fullmatch(t):
        raise ValueError(t)
    parts = [int(x) for x in t.split(".")]
    return tuple(parts + [-1] * (4 - len(parts)))


def compare_semver(a, b):
    """-1/0/1; 0 (conservative include) when either side is unparseable."""
    if a is not None and b is not None and str(a).lower() == str(b).lower():
        return 0
    if not a or a == "0":
        return -1
    try:
        va, vb = _to_sysver(a), _to_sysver(b)
    except (ValueError, TypeError):
        return 0
    return (va > vb) - (va < vb)


def test_osv_version_affected(ver, ranges, versions_list):
    if not ranges and not versions_list:
        return True  # no range data: conservative include
    if versions_list and str(ver).lower() in [str(v).lower() for v in versions_list]:
        return True
    for rng in ranges or []:
        if str(rng.get("type") or "").upper() not in ("SEMVER", "ECOSYSTEM"):
            continue
        events = rng.get("events")
        if not events:
            return True
        introduced = None
        for event in events:
            if event.get("introduced") is not None:
                introduced = event["introduced"]
            if event.get("fixed") is not None and introduced is not None:
                if compare_semver(ver, introduced) >= 0 and compare_semver(ver, event["fixed"]) < 0:
                    return True
                introduced = None
            if event.get("last_affected") is not None and introduced is not None:
                if compare_semver(ver, introduced) >= 0 and compare_semver(ver, event["last_affected"]) <= 0:
                    return True
                introduced = None
        # Open-ended range (introduced, no fixed/last_affected). introduced "0" is OSV's
        # "every version" marker; it must not be compared as a version.
        if introduced is not None:
            if introduced == "0" or compare_semver(ver, introduced) >= 0:
                return True
    return False


_GHSA_PART = re.compile(r"^(>=|<=|>|<|=)\s*(.+)$")


def test_ghsa_version_affected(ver, range_strings):
    # GHSA ranges look like "< 4.17.21" or ">= 4.0.0, < 4.17.21"
    for range_str in range_strings:
        in_range = True
        for part in [p.strip() for p in range_str.split(",")]:
            m = _GHSA_PART.match(part)
            if not m:
                return True  # unparseable: conservative include
            op, bound = m.group(1), m.group(2).strip()
            cmp = compare_semver(ver, bound)
            ok = {">=": cmp >= 0, "<=": cmp <= 0, ">": cmp > 0, "<": cmp < 0, "=": cmp == 0}[op]
            if not ok:
                in_range = False
                break
        if in_range:
            return True
    return False


def invoke_osv_query(ecosystem, name, version):
    resp = http_json("https://api.osv.dev/v1/query", method="POST",
                     body={"package": {"name": name, "ecosystem": OSV_ECO_MAP[ecosystem]}}, timeout=20)
    results = []
    if not resp or not resp.get("vulns"):
        return results

    for v in resp["vulns"]:
        affected_ranges = []
        affected_versions = []
        for a in v.get("affected") or []:
            if _ieq((a.get("package") or {}).get("name"), name):
                if a.get("ranges"):
                    affected_ranges.extend(a["ranges"])
                if a.get("versions"):
                    affected_versions.extend(a["versions"])
        include = test_osv_version_affected(version, affected_ranges, affected_versions) if version else True
        if include:
            results.append({
                "id": v.get("id"),
                "aliases": [x for x in (v.get("aliases") or []) if x],
                "summary": v.get("summary"),
                "severity": get_severity_from_osv(v),
                "affectedVersions": affected_versions,
            })
    return results


def invoke_ghsa_query(ecosystem, name, version):
    """Return a result list, or None when the query fails or is rate-limited."""
    uri = "https://api.github.com/advisories?affects=%s&ecosystem=%s&per_page=100" % (
        urllib.parse.quote(name, safe=""), GHSA_ECO_MAP[ecosystem])
    headers = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = "Bearer " + token
    try:
        resp = http_json(uri, headers=headers, timeout=20)
        results = []
        for adv in resp:
            affected_ranges = []
            relevant = False
            for vuln in adv.get("vulnerabilities") or []:
                if _ieq((vuln.get("package") or {}).get("name"), name):
                    relevant = True
                    if vuln.get("vulnerable_version_range"):
                        affected_ranges.append(vuln["vulnerable_version_range"])
            if not relevant:
                continue

            include = test_ghsa_version_affected(version, affected_ranges) if (version and affected_ranges) else True
            if include:
                results.append({
                    "id": adv.get("ghsa_id"),
                    "aliases": [adv["cve_id"]] if adv.get("cve_id") else [],
                    "summary": adv.get("summary"),
                    "severity": normalize_severity(adv["severity"]) if adv.get("severity") else "medium",
                    "affectedVersions": affected_ranges,
                })
        return results
    except Exception:
        return None  # graceful degradation


def get_discrepancies(osv_results, ghsa_results):
    def cve_map(results):
        m = {}
        for r in results:
            for alias in r.get("aliases") or []:
                if re.match(r"^CVE-", alias, re.I):
                    m[alias.lower()] = alias
        return m

    osv_cves = cve_map(osv_results)
    ghsa_cves = cve_map(ghsa_results)
    return {
        "onlyInOsv": [v for k, v in osv_cves.items() if k not in ghsa_cves],
        "onlyInGhsa": [v for k, v in ghsa_cves.items() if k not in osv_cves],
    }


def get_risk_level(results):
    order = {"none": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}
    highest = "none"
    for r in results:
        if order.get(r["severity"], 0) > order[highest]:
            highest = r["severity"]
    return highest


def build_parser():
    p = argparse.ArgumentParser(prog="vuln-lookup.py", allow_abbrev=False, description=__doc__.splitlines()[0])
    p.add_argument("-Ecosystem", "--ecosystem", dest="ecosystem", required=True, type=str.lower, choices=ECOSYSTEMS,
                   help="registry ecosystem")
    p.add_argument("-Name", "--name", dest="name", required=True, help="package name")
    p.add_argument("-Version", "--version", dest="version",
                   help="filter results to vulns affecting this version (conservative: keeps vulns without range data)")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    eco, name, version = args.ecosystem, args.name, args.version

    cache_key = "%s-%s" % (eco, name) + ("-" + version if version else "")
    cached = read_cache(CACHE_DIR, cache_key, 24)
    if cached:
        emit(cached)
        return 0

    try:
        osv_results = invoke_osv_query(eco, name, version)
        ghsa_results = invoke_ghsa_query(eco, name, version)
        sources = ["OSV"]
        ghsa_note = None

        if ghsa_results is None:
            ghsa_note = "skipped — query failed or rate-limited"
            ghsa_results = []
        else:
            sources.append("GHSA")

        all_results = osv_results + ghsa_results
        discrepancies = get_discrepancies(osv_results, ghsa_results)
        risk_level = get_risk_level(all_results)

        output = {
            "ecosystem": eco,
            "package": name,
            "osvResults": osv_results,
            "ghsaResults": ghsa_results,
            "summary": {
                "totalCount": len(all_results),
                "osvCount": len(osv_results),
                "ghsaCount": len(ghsa_results),
                "highestSeverity": risk_level,
            },
            "discrepancies": discrepancies,
            "sources": sources,
            "riskLevel": risk_level,
        }
        if version:
            output["version"] = version
        if ghsa_note:
            output["ghsaNote"] = ghsa_note

        write_cache(CACHE_DIR, cache_key, output)
        emit(output)
    except Exception as e:
        emit({"ecosystem": eco, "package": name, "error": str(e), "riskLevel": "unknown"})
    return 0


if __name__ == "__main__":
    sys.exit(main())
