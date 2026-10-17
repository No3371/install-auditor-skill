#!/usr/bin/env python3
"""Registry Lookup: fetch package metadata from official registry APIs.

Queries npm, PyPI, crates.io, RubyGems, NuGet and OpenSSF Scorecard to gather
hard data for install audits (downloads, maintainers, publish dates, etc.).

Python twin of registry-lookup.ps1: same flags, same JSON keys. Change both together.
Intentional divergence from the .ps1: dates are computed in UTC.

Examples:
    python3 registry-lookup.py npm lodash
    python3 registry-lookup.py npm lodash 4.17.21
    python3 registry-lookup.py -Ecosystem pypi -Name requests
    python3 registry-lookup.py crates serde
"""
import argparse
import gzip
import json
import math
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

USER_AGENT = "install-auditor/1.0"
ECOSYSTEMS = ["npm", "pypi", "crates", "rubygems", "nuget"]


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
        # NuGet registration5-gz always gzip-encodes; urllib does not decompress
        # (Invoke-RestMethod does), so skipping this breaks the nuget lookup.
        if resp.headers.get("Content-Encoding", "").lower() == "gzip" or raw[:2] == b"\x1f\x8b":
            raw = gzip.decompress(raw)
    return json.loads(raw.decode("utf-8"))


def invoke_api(url, timeout=15):
    """Mirror of Invoke-Api: None on any failure."""
    try:
        return http_json(url, timeout=timeout)
    except Exception:
        return None


def _parse_dt(s):
    if not s:
        return None
    t = str(s).strip().replace("Z", "+00:00")
    t = re.sub(r"(\.\d{6})\d+", r"\1", t)  # fromisoformat on <3.11 rejects >6 fraction digits
    try:
        d = datetime.fromisoformat(t)
    except ValueError:
        try:
            d = datetime.strptime(t[:10], "%Y-%m-%d")
        except ValueError:
            return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def get_days_since(s):
    d = _parse_dt(s)
    return None if d is None else math.floor((datetime.now(timezone.utc) - d).total_seconds() / 86400)


def format_date_str(s):
    d = _parse_dt(s)
    return "unknown" if d is None else d.astimezone(timezone.utc).strftime("%Y-%m-%d")


def _enc(s):
    """[Uri]::EscapeDataString equivalent."""
    return urllib.parse.quote(s, safe="")


def _ieq(a, b):
    """PowerShell -eq on strings: case-insensitive."""
    return a is not None and b is not None and str(a).lower() == str(b).lower()


def _npm_identity(version_data):
    """Publisher account, trusted-publisher config and provenance type of one version."""
    user = version_data.get("_npmUser")
    user = user if isinstance(user, dict) else {}
    tp = user.get("trustedPublisher")
    att = (version_data.get("dist") or {}).get("attestations")
    prov = att.get("provenance") if isinstance(att, dict) else None
    return {
        "publisher": user.get("name"),
        "trustedPublisher": {"id": tp.get("id"), "oidcConfigId": tp.get("oidcConfigId")} if isinstance(tp, dict) else None,
        "provenance": prov.get("predicateType") if isinstance(prov, dict) else None,
    }


def _npm_previous_version(versions, time_map, current):
    """The still-served version published immediately before `current`.

    Prereleases are skipped unless `current` is one: canary builds often come from a
    different pipeline, so comparing a stable release with one reports false identity
    breaks. Versions missing from `versions` (unpublished or removed by the registry)
    are skipped because their metadata is gone; `removedVersions` lists them instead.
    """
    cur = _parse_dt(time_map.get(current))
    if cur is None:
        return None
    best = None
    for v, t in time_map.items():
        if v in ("created", "modified") or v == current or v not in versions:
            continue
        if "-" in v and "-" not in current:
            continue
        d = _parse_dt(t)
        if d is not None and d < cur and (best is None or d > best[1]):
            best = (v, d)
    return best[0] if best else None


def lookup_npm(name, version):
    pkg = invoke_api("https://registry.npmjs.org/" + _enc(name))
    if not pkg:
        raise LookupError("Package '%s' not found on npm" % name)

    latest = version if version else (pkg.get("dist-tags") or {}).get("latest")
    versions = pkg.get("versions") or {}
    version_data = versions.get(latest) or {}
    time_map = pkg.get("time") or {}

    weekly_downloads = None
    dl = invoke_api("https://api.npmjs.org/downloads/point/last-week/" + _enc(name))
    if dl:
        weekly_downloads = dl.get("downloads")

    maintainers = [m.get("name") for m in (pkg.get("maintainers") or []) if isinstance(m, dict) and m.get("name")]

    scripts = version_data.get("scripts") or {}
    install_scripts = []
    for hook in ("preinstall", "install", "postinstall"):
        if scripts.get(hook):
            install_scripts.append({"hook": hook, "command": scripts[hook]})

    deps = list((version_data.get("dependencies") or {}).keys())

    repo = pkg.get("repository")
    repository = repo if isinstance(repo, str) else (repo.get("url") if isinstance(repo, dict) else None)

    identity = _npm_identity(version_data)
    previous_version = None
    prev = _npm_previous_version(versions, time_map, latest)
    if prev:
        prev_data = versions.get(prev) or {}
        prev_scripts = prev_data.get("scripts") or {}
        prev_identity = _npm_identity(prev_data)
        previous_version = {
            "version": prev,
            "publishedAt": format_date_str(time_map.get(prev)),
            "publisher": prev_identity["publisher"],
            "trustedPublisher": prev_identity["trustedPublisher"],
            "provenance": prev_identity["provenance"],
            "installHooks": [h for h in ("preinstall", "install", "postinstall") if prev_scripts.get(h)],
        }
    removed_versions = [v for v in time_map if v not in ("created", "modified") and v not in versions]

    return {
        "ecosystem": "npm",
        "name": pkg.get("name"),
        "version": latest,
        "description": pkg.get("description"),
        "license": version_data.get("license") or pkg.get("license"),
        "homepage": pkg.get("homepage"),
        "repository": repository,
        "publishedAt": format_date_str(time_map.get(latest)),
        "daysSincePublish": get_days_since(time_map.get(latest)),
        "createdAt": format_date_str(time_map.get("created")),
        "lastModified": format_date_str(time_map.get("modified")),
        "maintainers": maintainers,
        "maintainerCount": len(maintainers),
        "weeklyDownloads": weekly_downloads,
        "versionCount": len(versions),
        "deprecated": version_data.get("deprecated") or None,
        "installScripts": install_scripts if install_scripts else None,
        "dependencies": deps,
        "dependencyCount": len(deps),
        "engines": version_data.get("engines"),
        "publisher": identity["publisher"],
        "trustedPublisher": identity["trustedPublisher"],
        "provenance": identity["provenance"],
        "previousVersion": previous_version,
        "removedVersions": removed_versions,
    }


def lookup_pypi(name, version):
    if version:
        url = "https://pypi.org/pypi/%s/%s/json" % (_enc(name), version)
    else:
        url = "https://pypi.org/pypi/%s/json" % _enc(name)
    pkg = invoke_api(url)
    if not pkg:
        raise LookupError("Package '%s' not found on PyPI" % name)

    info = pkg.get("info") or {}
    urls = pkg.get("urls") or []
    project_urls = info.get("project_urls") or {}

    monthly_downloads = None
    stats = invoke_api("https://pypistats.org/api/packages/%s/recent" % _enc(name))
    if stats and stats.get("data"):
        monthly_downloads = stats["data"].get("last_month")

    maintainers = [x for x in (info.get("author"), info.get("maintainer")) if x]

    deps = [req.split(" ")[0] for req in (info.get("requires_dist") or [])]

    publish_date = urls[0].get("upload_time_iso_8601") if urls else None

    classifiers = info.get("classifiers") or []
    return {
        "ecosystem": "pypi",
        "name": info.get("name"),
        "version": info.get("version"),
        "description": info.get("summary"),
        "license": info.get("license") or "unknown",
        "homepage": info.get("home_page") or project_urls.get("Homepage") or None,
        "repository": project_urls.get("Source") or project_urls.get("Repository") or None,
        "publishedAt": format_date_str(publish_date),
        "daysSincePublish": get_days_since(publish_date),
        "maintainers": maintainers,
        "maintainerCount": len(maintainers),
        "monthlyDownloads": monthly_downloads,
        "versionCount": len(pkg.get("releases") or {}),
        "deprecated": True if any(re.search("inactive", c, re.I) for c in classifiers) else None,
        "requiresPython": info.get("requires_python"),
        "dependencies": deps,
        "dependencyCount": len(deps),
    }


def lookup_crates(name, version):
    pkg = invoke_api("https://crates.io/api/v1/crates/" + _enc(name))
    if not pkg:
        raise LookupError("Crate '%s' not found" % name)

    crate = pkg.get("crate") or {}
    versions = pkg.get("versions") or []
    if version:
        latest = next((v for v in versions if _ieq(v.get("num"), version)), None)
    else:
        latest = versions[0] if versions else None

    return {
        "ecosystem": "crates.io",
        "name": crate.get("name"),
        "version": latest.get("num") if latest else "unknown",
        "description": crate.get("description"),
        "license": latest.get("license") if latest else "unknown",
        "homepage": crate.get("homepage"),
        "repository": crate.get("repository"),
        "publishedAt": format_date_str(latest.get("created_at")) if latest else "unknown",
        "daysSincePublish": get_days_since(latest.get("created_at")) if latest else None,
        "totalDownloads": crate.get("downloads"),
        "recentDownloads": crate.get("recent_downloads"),
        "versionCount": len(versions),
    }


def lookup_rubygems(name, version):
    pkg = invoke_api("https://rubygems.org/api/v1/gems/%s.json" % _enc(name))
    if not pkg:
        raise LookupError("Gem '%s' not found" % name)

    licenses = pkg.get("licenses")
    return {
        "ecosystem": "rubygems",
        "name": pkg.get("name"),
        "version": pkg.get("version"),
        "description": pkg.get("info"),
        "license": ", ".join(licenses) if licenses else "unknown",
        "homepage": pkg.get("homepage_uri"),
        "repository": pkg.get("source_code_uri"),
        "publishedAt": format_date_str(pkg.get("version_created_at")),
        "daysSincePublish": get_days_since(pkg.get("version_created_at")),
        "totalDownloads": pkg.get("downloads"),
        "versionDownloads": pkg.get("version_downloads"),
    }


def lookup_nuget(name, version):
    pkg = invoke_api("https://api.nuget.org/v3/registration5-gz-semver2/%s/index.json" % name.lower())
    if not pkg:
        raise LookupError("NuGet package '%s' not found" % name)

    pages = pkg.get("items") or []
    last_page = pages[-1] if pages else {}
    # Some registration pages are not inlined and must be fetched by @id.
    if last_page.get("items"):
        items = last_page["items"]
    else:
        page = invoke_api(last_page["@id"]) if last_page.get("@id") else None
        items = (page.get("items") or []) if page else []

    if version:
        latest = next((i for i in items if _ieq((i.get("catalogEntry") or {}).get("version"), version)), None)
    else:
        latest = items[-1] if items else None
    entry = (latest or {}).get("catalogEntry") or {}

    return {
        "ecosystem": "nuget",
        "name": entry.get("id") or name,
        "version": entry.get("version") or "unknown",
        "description": entry.get("description"),
        "license": entry.get("licenseExpression") or entry.get("licenseUrl") or "unknown",
        "homepage": entry.get("projectUrl"),
        "publishedAt": format_date_str(entry.get("published")),
        "daysSincePublish": get_days_since(entry.get("published")),
        "listed": entry.get("listed") is not False,
        "versionCount": len(items),
    }


def lookup_openssf(repo_url):
    if not repo_url or not isinstance(repo_url, str):
        return None
    m = re.search(r"github\.com[/:]([^/]+/[^/.]+)", repo_url, re.I)
    if not m:
        return None
    repo = re.sub(r"\.git$", "", m.group(1))

    data = invoke_api("https://api.scorecard.dev/projects/github.com/" + repo)
    if not data:
        return None

    checks = [{"name": c.get("name"), "score": c.get("score")} for c in (data.get("checks") or [])]
    return {"score": data.get("score"), "date": data.get("date"), "checks": checks}


LOOKUPS = {
    "npm": lookup_npm,
    "pypi": lookup_pypi,
    "crates": lookup_crates,
    "rubygems": lookup_rubygems,
    "nuget": lookup_nuget,
}


def emit(obj):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    sys.stdout.write(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def build_parser():
    p = argparse.ArgumentParser(
        prog="registry-lookup.py",
        allow_abbrev=False,
        description=__doc__.splitlines()[0],
        epilog="Positional form: registry-lookup.py <ecosystem> <name> [version]",
    )
    p.add_argument("pos", nargs="*", metavar="ECOSYSTEM NAME [VERSION]",
                   help="positional ecosystem, name and optional version")
    p.add_argument("-Ecosystem", "--ecosystem", dest="ecosystem", help="one of: " + ", ".join(ECOSYSTEMS))
    p.add_argument("-Name", "--name", dest="name", help="package name (e.g. lodash, requests, serde)")
    p.add_argument("-Version", "--version", dest="version", help="specific version (default: latest)")
    return p


def main(argv=None):
    p = build_parser()
    args = p.parse_intermixed_args(argv)

    # PowerShell binding: named parameters win; positionals fill the unbound
    # parameters in declaration order.
    pos = list(args.pos)
    if len(pos) > 3:
        p.error("too many positional arguments (expected: ecosystem name [version])")
    slots = {"ecosystem": args.ecosystem, "name": args.name, "version": args.version}
    for key in ("ecosystem", "name", "version"):
        if slots[key] is None and pos:
            slots[key] = pos.pop(0)
    if pos:
        p.error("too many positional arguments (expected: ecosystem name [version])")

    eco = (slots["ecosystem"] or "").lower()
    if not eco:
        p.error("ecosystem is required")
    if eco not in LOOKUPS:
        p.error("argument -Ecosystem: invalid choice: %r (choose from %s)" % (slots["ecosystem"], ", ".join(ECOSYSTEMS)))
    if not slots["name"]:
        p.error("name is required")

    try:
        result = LOOKUPS[eco](slots["name"], slots["version"])
    except LookupError as e:
        sys.stderr.write(str(e) + "\n")
        return 1

    repo_url = result.get("repository")
    if repo_url:
        scorecard = lookup_openssf(repo_url)
        if scorecard:
            result["openssf"] = scorecard

    emit(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
