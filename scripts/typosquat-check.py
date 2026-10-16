#!/usr/bin/env python3
"""Typosquat Check: algorithmic similarity detection for registry packages.

Fetches a popular-package baseline from the npm search API, computes Levenshtein
edit distance between the queried name and popular packages, detects combosquat
patterns (prefix/suffix overlap), compares download counts and emits a structured
JSON risk assessment to stdout. npm only.

Python twin of typosquat-check.ps1: same flags, same JSON keys. Change both together.
Intentional divergences from the .ps1: arrays are always emitted as arrays (the
.ps1 collapses one-element results to scalars and empty ones to null).

Examples:
    python3 typosquat-check.py -Ecosystem npm -Name expresss
    python3 typosquat-check.py -Ecosystem npm -Name lodahs -CompareTo lodash
    python3 typosquat-check.py -Ecosystem npm -Name chalk -Size 500
"""
import argparse
import gzip
import json
import math
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
USER_AGENT = "install-auditor/1.0"
ECOSYSTEMS = ["npm"]
CACHE_DIR = ".typosquat-cache"


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


def invoke_api(url, timeout=15):
    """Mirror of Invoke-Api: None on any failure."""
    try:
        return http_json(url, timeout=timeout)
    except Exception:
        return None


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
        pass  # non-fatal, as in the .ps1


def emit(obj):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    sys.stdout.write(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def get_comparison_token(raw_name):
    """Normalize a package name for comparison: lowercase, fold separators, strip scope prefix."""
    n = raw_name.lower().strip()
    m = re.match(r"^@[^/]+/(.+)$", n)
    if m:
        n = m.group(1)
    return re.sub(r"[-_]+", "-", n)


def get_levenshtein_distance(source, target):
    """Classic O(m*n) two-row Levenshtein distance."""
    m, n = len(source), len(target)
    if m == 0:
        return n
    if n == 0:
        return m

    prev = list(range(n + 1))
    curr = [0] * (n + 1)
    for i in range(1, m + 1):
        curr[0] = i
        for j in range(1, n + 1):
            cost = 0 if source[i - 1] == target[j - 1] else 1
            curr[j] = min(curr[j - 1] + 1, prev[j] + 1, prev[j - 1] + cost)
        prev, curr = curr, prev
    return prev[n]


def _ieq(a, b):
    """PowerShell -eq on strings: case-insensitive."""
    return a is not None and b is not None and str(a).lower() == str(b).lower()


def get_npm_popular_baseline(size, cache_hours, no_cache):
    """Return [{name, downloads}] sorted by downloads desc; [] on API failure."""
    key = "npm-%s-%s" % (size, datetime.now().strftime("%Y-%m-%d"))
    if not no_cache:
        cached = read_cache(CACHE_DIR, key, cache_hours)
        if cached:
            return cached

    url = "https://registry.npmjs.org/-/v1/search?text=boost-exact:false&size=%s&popularity=1.0" % size
    result = invoke_api(url)
    if not result or not result.get("objects"):
        return []

    baseline = []
    for obj in result["objects"]:
        pkg = obj.get("package") or {}
        downloads = 0
        popularity = ((obj.get("score") or {}).get("detail") or {}).get("popularity")
        if popularity:
            # Popularity is a 0-1 score, not a download count; scaled as an approximation.
            downloads = int(math.floor(popularity * 10000000))
        baseline.append({"name": pkg.get("name"), "downloads": downloads})

    baseline.sort(key=lambda b: b["downloads"], reverse=True)
    write_cache(CACHE_DIR, key, baseline)
    return baseline


def get_npm_weekly_downloads(package_name):
    dl = invoke_api("https://api.npmjs.org/downloads/point/last-week/" + urllib.parse.quote(package_name, safe=""))
    if dl and dl.get("downloads") is not None:
        return int(dl["downloads"])
    return None


def invoke_typosquat_analysis(ecosystem, name, compare_to, size, cache_hours, no_cache):
    normalized_name = get_comparison_token(name)

    baseline = get_npm_popular_baseline(size, cache_hours, no_cache) or []

    # An explicit -CompareTo is always a candidate, even when the baseline lacks it.
    candidates = []
    if compare_to:
        if not any(_ieq(b.get("name"), compare_to) for b in baseline):
            candidates.append({"name": compare_to, "downloads": 0})
    candidates.extend(baseline)

    matches = []
    for c in candidates:
        c_norm = get_comparison_token(c["name"])
        if c_norm == normalized_name:
            continue
        dist = get_levenshtein_distance(normalized_name, c_norm)
        if dist <= 3:
            matches.append({"name": c["name"], "distance": dist, "downloads": c.get("downloads")})
    matches.sort(key=lambda m: (m["distance"], -(m["downloads"] or 0)))
    closest_matches = matches[:10]

    combosquat_hints = []
    for b in baseline[:100]:
        b_norm = get_comparison_token(b["name"])
        if b_norm == normalized_name:
            continue
        if len(b_norm) < 3:  # very short names are noise
            continue
        is_combo = False
        if len(normalized_name) > len(b_norm):
            if normalized_name.startswith(b_norm) or normalized_name.endswith(b_norm):
                is_combo = True
        if len(b_norm) > len(normalized_name):
            if b_norm.startswith(normalized_name) or b_norm.endswith(normalized_name):
                is_combo = True
        if is_combo:
            combosquat_hints.append(b["name"])

    dl_memo = {}

    def weekly(pkg_name):
        if pkg_name not in dl_memo:
            dl_memo[pkg_name] = get_npm_weekly_downloads(pkg_name)
        return dl_memo[pkg_name]

    download_ratio = None
    best_compare = None
    if compare_to:
        best_compare = compare_to
    elif closest_matches:
        best_compare = closest_matches[0]["name"]

    if best_compare:
        queried_dl = weekly(name)
        closest_dl = weekly(best_compare)
        if queried_dl is not None and closest_dl is not None and queried_dl >= 0:
            if queried_dl > 0:
                ratio_value = round(closest_dl / queried_dl, 2)
            else:
                # Queried package has 0 downloads; infinity is not valid JSON, so -1 stands for it.
                ratio_value = -1 if closest_dl > 0 else 1.0
            download_ratio = {"queried": queried_dl, "closest": closest_dl, "ratio": ratio_value}
            for cm in closest_matches:
                if _ieq(cm["name"], best_compare):
                    cm["downloads"] = closest_dl
                    break

    risk_level = "low"
    risk_reasons = []
    min_dist = closest_matches[0]["distance"] if closest_matches else 999
    has_explicit_compare = bool(compare_to)

    if min_dist == 1:
        risk_level = "high"
        risk_reasons.append("Edit distance 1 from '%s'" % closest_matches[0]["name"])
    elif min_dist == 2:
        risk_level = "medium"
        risk_reasons.append("Edit distance 2 from '%s'" % closest_matches[0]["name"])
    elif min_dist == 3:
        risk_reasons.append("Edit distance 3 from '%s' (borderline)" % closest_matches[0]["name"])

    if download_ratio and download_ratio["ratio"] is not None:
        r = download_ratio["ratio"]
        stats = "(queried: %s, closest: %s)" % (download_ratio["queried"], download_ratio["closest"])
        if r == -1 or r >= 1000:
            if min_dist <= 2:
                risk_level = "critical"
                risk_reasons.append("Download ratio >= 1000x " + stats)
        elif r >= 100:
            if risk_level == "high" or min_dist <= 1:
                risk_level = "critical"
            elif risk_level != "critical":
                risk_level = "high"
            risk_reasons.append("Download ratio >= 100x " + stats)
        elif r >= 10:
            if risk_level == "medium":
                risk_level = "high"
            risk_reasons.append("Download ratio >= 10x " + stats)

    if has_explicit_compare and min_dist <= 2 and risk_level == "medium":
        risk_level = "high"
        risk_reasons.append("Explicit -CompareTo provided with close edit distance")

    if combosquat_hints:
        if risk_level == "low":
            risk_level = "medium"
        risk_reasons.append("Combosquat pattern detected: name overlaps with " + ", ".join(combosquat_hints))

    queried_exists = weekly(name) is not None

    if risk_reasons:
        details = "Risk factors: %s. " % "; ".join(risk_reasons)
    else:
        details = "No close matches found in top-%s popular packages. " % size
    if not queried_exists:
        details += "Note: '%s' does not appear to exist on npm (0 download data). " % name
    if combosquat_hints:
        details += "Combosquat hints: %s. " % ", ".join(combosquat_hints)

    return {
        "ecosystem": ecosystem,
        "queriedName": name,
        "normalizedName": normalized_name,
        "compareTo": compare_to if compare_to else None,
        "riskLevel": risk_level,
        "closestMatches": closest_matches,
        "combosquatHints": combosquat_hints,
        "downloadRatio": download_ratio,
        "details": details.strip(),
    }


def build_parser():
    p = argparse.ArgumentParser(prog="typosquat-check.py", allow_abbrev=False, description=__doc__.splitlines()[0])
    p.add_argument("-Ecosystem", "--ecosystem", dest="ecosystem", required=True, type=str.lower, choices=ECOSYSTEMS,
                   help="registry ecosystem (currently only npm)")
    p.add_argument("-Name", "--name", dest="name", required=True,
                   help="exact package name to check (e.g. 'expresss', '@scope/pkg')")
    p.add_argument("-CompareTo", "--compare-to", dest="compare_to",
                   help="known legitimate package name to compare against directly")
    p.add_argument("-Size", "--size", dest="size", type=int, default=250,
                   help="number of popular packages to fetch as baseline (default: 250)")
    p.add_argument("-CacheHours", "--cache-hours", dest="cache_hours", type=int, default=24,
                   help="hours to cache the popular-package baseline (default: 24)")
    p.add_argument("-NoCache", "--no-cache", dest="no_cache", action="store_true",
                   help="skip cache reads; always fetch a fresh baseline")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        result = invoke_typosquat_analysis(args.ecosystem, args.name, args.compare_to, args.size,
                                           args.cache_hours, args.no_cache)
        emit(result)
    except Exception as e:
        emit({
            "ecosystem": args.ecosystem,
            "queriedName": args.name,
            "error": str(e),
            "riskLevel": "unknown",
        })
    return 0


if __name__ == "__main__":
    sys.exit(main())
