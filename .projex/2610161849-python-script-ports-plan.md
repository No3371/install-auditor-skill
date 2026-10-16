# Python Ports of Lookup Scripts

> **Status:** In Progress
> **Author:** Claude (Opus 5.5)
> **Parent:** Orchestrator
> **Source:** Direct request (orchestrator improvement candidate: "lookup scripts usable on hosts without PowerShell")
> **Related Projex:** 2604021200-reliability-accuracy-improvements-imagine.md (seed: "Multi-platform registry-lookup") | 2604070217-subject-typed-audit-dispatch-eval.md (§3.3 soft constraint "PowerShell remains the scripting language" — relaxed here: `.ps1` kept, Python twin added) | 2604070218-install-auditor-subject-typed-redesign-nav.md (roadmap) | 2604021815-algorithmic-typosquat-detection-plan.md, 2604101000-multi-db-cve-correlation-plan.md, 2604110900-transitive-dep-scan-plan.md (origin plans of the ported scripts) | siblings: 2610161850-eval-runner-harness-plan.md, 2610161852-dispatcher-rubric-consistency-plan.md
> **Worktree:** Yes

---

## Summary

All four skill scripts are PowerShell-only. Hosts without `pwsh` (common Linux/macOS dev boxes, most cloud agent sandboxes) skip them → agent hand-queries APIs, and `SKILL.md` documents a manual fallback only for registry-lookup. Plan: add stdlib-only Python 3.8+ twins (`scripts/<name>.py`) that mirror each `.ps1` CLI (same `-Ecosystem/-Name/...` flags) and JSON output contract, keep `.ps1` unchanged for PowerShell hosts, and switch doc call sites to Python-first with a one-line `.ps1` twin note per file.

**Scope:** 4 new `scripts/*.py` + script-invocation/reference lines in `SKILL.md` (lines 87, 241 only), `references/criteria.md`, `references/criteria/registry-package.md`, `workflows/registry-package.md`.
**Estimated Changes:** 4 new files (~1000 Python lines total) | 4 doc files edited (~55 lines).

---

## Objective

### Problem / Gap / Need

- Verified 2026-10-16: `scripts/registry-lookup.ps1` (310 lines), `typosquat-check.ps1` (422), `vuln-lookup.ps1` (362), `dep-scan.ps1` (461) — PowerShell only; no other impl.
- Linux host here: `pwsh` absent; `python3` 3.13, `node` 22, `npm` 10.9 present.
- Call sites hardcode `.\scripts\<x>.ps1` (Windows path syntax) in `workflows/registry-package.md` (6 code blocks, ~15 prose refs), `references/criteria/registry-package.md` (4 blocks, ~10 prose refs), `references/criteria.md` (6 refs), `SKILL.md:87,241`.
- `SKILL.md:241` fallback covers registry-lookup only; typosquat / CVE / dep-scan have no non-PowerShell path → those Evidence steps silently degrade to web search.

### Language Decision

| Option | Verdict | Reason |
|---|---|---|
| Python 3.8+ stdlib twin | **Chosen** | Preinstalled on most Linux/macOS dev hosts + any PyPI-ecosystem host; `urllib`/`json`/`argparse`/`subprocess`/`tempfile`/`gzip` cover every `.ps1` feature; zero third-party deps (an install auditor must not require installing packages to run). |
| Node port | Rejected | Present only where JS tooling is; PyPI/crates/RubyGems auditors may lack it. Python has wider default availability. |
| Replace `.ps1` entirely | Rejected | Windows hosts ship PowerShell, not Python; removing `.ps1` regresses them. |
| pwsh-install guidance only | Rejected | Requires installing software before an install audit; cloud sandboxes often cannot. |

Dual-impl drift risk accepted; mitigated by mirror-style port (same function names in snake_case, same output keys) + docstring rule "change both together".

### Success Criteria

- [ ] `scripts/registry-lookup.py`, `typosquat-check.py`, `vuln-lookup.py`, `dep-scan.py` exist, executable (`100755`), `#!/usr/bin/env python3`, stdlib-only imports.
- [ ] Each parses as Python 3.8 grammar (`ast.parse(..., feature_version=(3, 8))`) and `python3 scripts/<x>.py --help` exits 0.
- [ ] Each accepts the same flags as its `.ps1` twin (`-Ecosystem -Name -Version -Tier -CompareTo -Size -CacheHours -NoCache`, plus `--kebab-case` aliases); registry-lookup also accepts positional `<eco> <name> [version]`.
- [ ] Each emits JSON with the same top-level keys/order as its `.ps1` twin on success and on error paths (offline fixture harness, see Verification Plan).
- [ ] Pure-logic parity: Levenshtein, name normalization, `Compare-SemVer`, OSV/GHSA range tests, severity mapping, PyPI requirement parsing return the values listed in Verification Plan.
- [ ] Live runs succeed where network allows: registry-lookup for npm (incl. scoped) / pypi / crates / rubygems / nuget; dep-scan `npm chalk 5.3.0 -Tier 2`; dep-scan `-Tier 3` resolves lockfile via npm.
- [ ] `grep -n '\.ps1'` across `SKILL.md workflows/ references/` returns only the allowed residue listed in Step 5.
- [ ] No edits to `SKILL.md` outside lines 87 and 241; no edits to `.ps1` files, `evals/`, `.gitignore`.

### Out of Scope

- Fixing `.ps1` logic or porting `.ps1` bugs' *fixes* back (see Notes → Known PS defects).
- Fixing the typosquat baseline query (broken in both impls — see Notes; needs its own plan).
- `SKILL.md:156` report-skeleton text `e.g., registry-lookup.ps1 / npm API` — deferred to the planned SKILL.md compression plan (skeleton moves out of `SKILL.md`); avoids collision.
- `evals/evals.json` text mentioning `.ps1` names — owned by sibling eval-runner plan; assertions use `OR`/concept phrasing so remain satisfiable.
- New ecosystems, new features, committed test suite, CI.
- Script path resolution relative to skill install dir (pre-existing `scripts/` relative convention kept).

---

## Context

### Current State

- Scripts emit JSON to stdout (`ConvertTo-Json`). registry-lookup throws (non-zero exit, stderr text) on not-found; the other three always exit 0 and emit `{…, error, riskLevel: "unknown"}` on failure.
- Caches (gitignored in `.gitignore`): `scripts/.typosquat-cache/<eco>-<size>-<yyyy-MM-dd>.json` (TTL `-CacheHours`, default 24), `scripts/.vuln-cache/<eco>-<name>[-<ver>].json` (24 h), `scripts/.dep-scan-cache/<eco>-<name>[-<ver>]-t<tier>.json` (24 h). TTL = file mtime age.
- Endpoints: npm registry + `api.npmjs.org/downloads` + npm search | PyPI JSON + `pypistats.org` | crates.io | RubyGems | NuGet `registration5-gz-semver2` (**always gzip-encoded** — verified; `urllib` does not auto-decompress) | `api.securityscorecards.dev` | OSV `/v1/query`, `/v1/querybatch`, `/v1/vulns/{id}` | GitHub `/advisories` (+ optional `GITHUB_TOKEN`).
- Reachability from this sandbox (2026-10-16, Python `urllib`): ✓ registry.npmjs.org (incl. `/-/v1/search`, scoped `%40types%2Fnode` and literal `@types/node/latest`), pypi.org, crates.io, rubygems.org, api.nuget.org | ✗ proxy 403: api.osv.dev, api.npmjs.org, pypistats.org, api.securityscorecards.dev; api.github.com `/advisories` 403 ("sessions are bound to their configured repositories"). → OSV/GHSA success paths must be verified offline with fixtures.

### Key Files

| File | Role | Change Summary |
|---|---|---|
| `scripts/registry-lookup.py` | New | Port of `registry-lookup.ps1` |
| `scripts/typosquat-check.py` | New | Port of `typosquat-check.ps1` |
| `scripts/vuln-lookup.py` | New | Port of `vuln-lookup.ps1` |
| `scripts/dep-scan.py` | New | Port of `dep-scan.ps1` |
| `SKILL.md` | Dispatcher | Lines 87 + 241 only: Python-first invocation, `.ps1` twin, manual fallback for all four |
| `references/criteria.md` | Shared rubric | 6 script refs → `.py` / stem |
| `references/criteria/registry-package.md` | Registry criteria | 4 invocation blocks → `python3`, prose refs → stem, twin note, `GITHUB_TOKEN` shell syntax |
| `workflows/registry-package.md` | Registry workflow | 6 invocation blocks → `python3`, table + prose refs → stem, twin note |
| `scripts/*.ps1` | Reference impl | Unchanged — the source of truth each port mirrors |

### Dependencies

- **Requires:** none.
- **Blocks:** none hard. Sibling plans: (a) SKILL.md red-flag/classifier fixes — touches `SKILL.md` §Red Flags (line ~196+) and classifier ref; this plan touches only lines 87, 241 → no overlap. (b) 2610161850-eval-runner-harness-plan.md — touches `evals/`, `STEWARDSHIP.md`; this plan does not. Its snapshot copies `scripts/` and its tool allowlist already includes `Bash(python3 {s}/scripts/:*)` → `.py` ports work under it unchanged. (a) is 2610161852-dispatcher-rubric-consistency-plan.md. Later SKILL.md compression plan should carry the Step 5 wording of the Reference Files script bullet and fix `SKILL.md:156`.

### Constraints

- Python ≥ 3.8, stdlib only. No `match`, no `str.removeprefix`, no `dict |`, no builtin-generic runtime annotations (`list[str]`) unless `from __future__ import annotations`.
- Each `.py` standalone (no shared module): `python3 -I` (isolated mode) drops the script dir from `sys.path`, so a sibling import would break; mirrors the standalone `.ps1` design.
- Source Hygiene (SKILL.md of projex framework): no projex refs in code comments, no `# ─── X ───` / `====` banners (the `.ps1` banners are **not** copied), symbol names not line numbers, rationale comments name the rejected alternative.
- **Security — Tier 3 must never execute package code.** The `npm install` call keeps exactly `--package-lock-only --ignore-scripts` and runs in a fresh temp dir that is always deleted. Do not drop or reorder these flags; do not add `npm ci`/`npm install` without them.

### Assumptions

- Agents on non-Windows hosts can run `python3` (verify early: `python3 --version`).
- `.ps1` behavior read from source is the contract; no `pwsh` available to diff live outputs (verified absent). Parity is by code-reading + fixture tests.
- PowerShell string `-eq` / `-match` / `-in` / `ValidateSet` are case-insensitive; ports apply `.lower()`/`re.I` at those points.

### Impact Analysis

- **Direct:** 4 new scripts; 4 doc files.
- **Adjacent:** gitignored cache dirs shared by both impls (same paths/keys; both JSON). A cache written by `.ps1` and read by `.py` carries PS array-unrolling shapes — tolerable, 24 h TTL.
- **Downstream:** runtime agent's Audit Coverage rows now cite stem names (`vuln-lookup: none found (OSV, GHSA)`); eval graders use concept matching.

---

## Implementation

### Overview

Steps 1–4: one port per script, each self-contained, following **Port Conventions** below and the `.ps1` as line-by-line reference. Step 5: doc call sites. Order 1→5; Steps 1–4 independent of each other.

### Port Conventions (apply to Steps 1–4)

**File skeleton:**

```python
#!/usr/bin/env python3
"""<SYNOPSIS from .ps1, 1–3 lines>.

Python twin of <name>.ps1: same flags, same JSON keys. Change both together.
Intentional divergences from the .ps1: <list relevant items from "Divergences" below>.
"""
import argparse, json, os, sys, urllib.error, urllib.parse, urllib.request  # + per-script stdlib

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
USER_AGENT = "install-auditor/1.0"

# ... functions: snake_case mirrors of PS function names (Invoke-Api → invoke_api, Get-LevenshteinDistance → get_levenshtein_distance, ...)

def main(argv=None):
    args = build_parser().parse_args(argv)
    ...
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

**HTTP — single entry point** (every network call goes through `http_json`; harness monkeypatches it):

```python
import gzip

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
```

`[Uri]::EscapeDataString(x)` → `urllib.parse.quote(x, safe="")`. Where the `.ps1` interpolates the raw name (dep-scan `Get-NpmDeps`/`Get-PypiDeps`), keep raw (`@scope/name/latest` verified 200).

**Cache** (vuln, dep-scan, typosquat):

```python
import time

def cache_path(dirname, key):
    d = os.path.join(SCRIPT_DIR, dirname)
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, key + ".json")

def read_cache(dirname, key, ttl_hours):
    try:
        p = cache_path(dirname, key)
        if time.time() - os.path.getmtime(p) > ttl_hours * 3600:
            return None
        with open(p, encoding="utf-8-sig") as f:   # -sig: tolerate BOM from Windows PowerShell writes
            return json.load(f)
    except Exception:
        return None

def write_cache(dirname, key, data):
    try:
        with open(cache_path(dirname, key), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception:
        pass  # non-fatal, as in .ps1 (also covers scoped names whose "/" makes the path invalid)
```

Same dir names + key formats as `.ps1` (see Current State). Scoped-name keys containing `/` fail to write in both impls — parity kept, no sanitizing.

**Output:**

```python
def emit(obj):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    sys.stdout.write(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")
```

Use plain `dict` in insertion order = `[ordered]@{}` key order. Conditional keys appended at the end exactly where the `.ps1` adds them.

**CLI** — PS-style single-dash flags first, kebab aliases second, `allow_abbrev=False`, enum values lower-cased:

```python
def build_parser():
    p = argparse.ArgumentParser(prog="vuln-lookup.py", allow_abbrev=False, description=__doc__.splitlines()[0])
    p.add_argument("-Ecosystem", "--ecosystem", dest="ecosystem", required=True, type=str.lower, choices=ECOSYSTEMS)
    p.add_argument("-Name", "--name", dest="name", required=True)
    p.add_argument("-Version", "--version", dest="version")
    return p
```

**Divergences (intentional; list the relevant ones in each docstring):**

1. JSON arrays always emitted as arrays. PS pipeline unrolling turns 1-element results into scalars/objects and empty results into `null` (e.g. `maintainers: "name"`; vuln-lookup `osvResults: null`; with exactly one OSV hit `summary.osvCount` becomes the ordered-dictionary key count, 5). Python reports true lists and counts.
2. Dates computed in UTC (`publishedAt`, `daysSincePublish`); PS converts to local time → may differ by one day near midnight.
3. dep-scan Tier 3 `npm install` gets `timeout=300` s (PS: unbounded); timeout → Tier 2 fallback with reason.
4. String comparisons that are `-eq`/`-in`/`-match` in PS are case-insensitive in Python too (not a divergence — call out only if non-obvious).

**Date helper** (registry-lookup):

```python
from datetime import datetime, timezone
import math, re

def _parse_dt(s):
    if not s:
        return None
    t = str(s).strip().replace("Z", "+00:00")
    t = re.sub(r"(\.\d{6})\d+", r"\1", t)   # fromisoformat on <3.11 rejects >6 fraction digits
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
```

---

### Step 1: Port registry-lookup

**Objective:** `scripts/registry-lookup.py` ≡ `registry-lookup.ps1`.
**Confidence:** High
**Depends on:** None
**Do-Projex:** Encouraged

**Files:** `scripts/registry-lookup.py` (new)

**Changes:**

- CLI: positional `pos` (`nargs="*"`, max 3 → ecosystem, name, version) **and** `-Ecosystem/-Name/-Version` flags; named wins; validate ecosystem ∈ `npm pypi crates rubygems nuget` (case-insensitive) and name present → else `p.error(...)` (exit 2). Both `registry-lookup.py npm lodash 4.17.21` and `registry-lookup.py -Ecosystem npm -Name lodash` work.
- `lookup_npm` / `lookup_pypi` / `lookup_crates` / `lookup_rubygems` / `lookup_nuget` / `lookup_openssf`: same URLs, same fallbacks, same output keys in same order as the `.ps1` functions. Notes per function:
  - npm: `version_data = pkg.get("versions", {}).get(latest) or {}`; `installScripts` list of `{hook, command}` for `preinstall|install|postinstall`, `None` if empty; `repository` = string or `.url`; `license` = version license else package license; `versionCount = len(versions)`; `deprecated` = value or `None`; `engines` raw.
  - pypi: maintainers = `[x for x in (author, maintainer) if x]`; deps = `req.split(" ")[0]` per `requires_dist` (this script's simpler parse — not dep-scan's); `publishedAt` from `urls[0].upload_time_iso_8601`; `deprecated = True if any(re.search("inactive", c, re.I) for c in classifiers) else None`; `homepage`/`repository` fallbacks via `project_urls` (`Homepage`; `Source` then `Repository`), guard `project_urls` None.
  - crates: version = matching `num` or `versions[0]`; `ecosystem: "crates.io"` (as PS).
  - rubygems: `license = ", ".join(licenses)` or `"unknown"`.
  - nuget: URL uses `name.lower()` unescaped; last page `items` else fetch `@id`; latest = matching `catalogEntry.version` or `items[-1]`; `listed = entry.get("listed") is not False`; guard empty items → entry `{}`.
  - openssf: `re.search(r"github\.com[/:]([^/]+/[^/.]+)", url, re.I)`, strip `.git`; output `{score, date, checks:[{name, score}]}`; attach as `result["openssf"]` only when non-null.
- Not found (`invoke_api` → None for the primary lookup): print `Package '<name>' not found on npm` (exact PS messages per ecosystem: `on PyPI`, `Crate '<n>' not found`, `Gem '<n>' not found`, `NuGet package '<n>' not found`) to stderr, return 1.
- Output: `emit(result)`.

**Rationale:** Most-used script; positional form matches current `SKILL.md:241` example, flags match workflow examples.

**Verification:** `python3 -B scripts/registry-lookup.py npm lodash` → JSON with `name: "lodash"`, numeric `versionCount`, list `maintainers`; `-Ecosystem npm -Name "@types/node"` ✓; `pypi requests`, `crates serde`, `rubygems rails`, `nuget Newtonsoft.Json` → `name` populated, `version` ≠ `unknown`; `npm this-pkg-does-not-exist-zz9` → exit 1, stderr message, empty stdout. (`weeklyDownloads`/`monthlyDownloads`/`openssf` null/absent here — hosts blocked by proxy.)

**If this fails:** delete `scripts/registry-lookup.py`; no other file depends on it until Step 5.

---

### Step 2: Port typosquat-check

**Objective:** `scripts/typosquat-check.py` ≡ `typosquat-check.ps1`.
**Confidence:** High
**Depends on:** None
**Do-Projex:** Encouraged

**Files:** `scripts/typosquat-check.py` (new)

**Changes:**

- CLI: `-Ecosystem` (choices `npm`), `-Name`, `-CompareTo/--compare-to`, `-Size/--size` (int, 250), `-CacheHours/--cache-hours` (int, 24), `-NoCache/--no-cache` (store_true).
- `get_comparison_token`: lower + strip; `^@[^/]+/(.+)$` → group 1; `re.sub(r"[-_]+", "-", n)`.
- `get_levenshtein_distance`: two-row DP, identical semantics.
- Cache: dir `.typosquat-cache`, key `f"{eco}-{size}-{datetime.now().strftime('%Y-%m-%d')}"` (local date, as PS), TTL `cache_hours`, skipped on `-NoCache`.
- `get_npm_popular_baseline`: same URL **verbatim** (`text=boost-exact:false&size={size}&popularity=1.0`), `downloads = floor(popularity * 10_000_000)`, sort desc, write cache; API failure → `[]`. Do not "fix" the query here (see Notes).
- `get_npm_weekly_downloads`: `api.npmjs.org/downloads/point/last-week/<quote(name)>` → `int` or `None`.
- `invoke_typosquat_analysis`: port line-for-line — candidate list (`CompareTo` prepended if not in baseline, case-insensitive name compare), matches `dist <= 3` sorted `(distance, -downloads)` top 10, combosquat over top 100 (skip equal, skip `len < 3`, prefix/suffix either direction), download ratio (`round(closest / queried, 2)`; queried 0 → `-1` if closest > 0 else `1.0`; Python `round` = .NET banker's rounding ✓), update matched entry's `downloads`, risk ladder exactly as PS (distance 1/2/3 → high/medium/low-borderline; ratio `-1 or >= 1000` + `minDist <= 2` → critical; `>= 100`; `>= 10`; explicit CompareTo floor; combosquat lifts low → medium), `queriedExists`, `details` string assembly + `.strip()`.
- Output keys: `ecosystem, queriedName, normalizedName, compareTo, riskLevel, closestMatches, combosquatHints, downloadRatio, details`. Exception → `{ecosystem, queriedName, error, riskLevel: "unknown"}`, exit 0.

**Rationale:** Faithful port keeps the two impls interchangeable; logic fixes belong in a separate plan touching both.

**Verification:** Harness unit checks (Verification Plan §A) + live `python3 -B scripts/typosquat-check.py -Ecosystem npm -Name expresss -CompareTo express -NoCache` → `closestMatches[0] == {name: "express", distance: 1, ...}`, `riskLevel` ∈ `high|critical`, `downloadRatio` null here (downloads API blocked).

**If this fails:** delete `scripts/typosquat-check.py`.

---

### Step 3: Port vuln-lookup

**Objective:** `scripts/vuln-lookup.py` ≡ `vuln-lookup.ps1`.
**Confidence:** Medium (version-range semantics subtle)
**Depends on:** None
**Do-Projex:** Encouraged
**Verify-Projex:** Encouraged

**Files:** `scripts/vuln-lookup.py` (new)

**Changes:**

- CLI: `-Ecosystem` (`npm pypi crates rubygems nuget go maven hex`), `-Name`, `-Version`. Same `OSV_ECO_MAP` / `GHSA_ECO_MAP` dicts.
- Severity: `normalize_severity` (`critical|high|moderate→medium|medium|low`, default `medium`; `None` → `medium`), `get_severity_from_osv` (`database_specific.severity` first; else first `severity[].score` matching `^\d+(\.\d+)?$` → ≥9 critical, ≥7 high, ≥4 medium, else low; else `medium`).
- `compare_semver` must reproduce `[System.Version]` semantics — load-bearing, port exactly:

```python
_SYSVER = re.compile(r"\d+(\.\d+){1,3}")

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
```

  Consequence kept on purpose: single-part bounds like `introduced: "0"` are unparseable → compare 0 → treated as ≥ (conservative include), same as PS.
- `test_osv_version_affected(ver, ranges, versions_list)` and `test_ghsa_version_affected(ver, range_strings)`: line-for-line (event walk with `introduced`/`fixed`/`last_affected` reset; open-ended range; `introduced == "0"` → floor -1 in that branch only; GHSA `,`-split parts, `^(>=|<=|>|<|=)\s*(.+)$`, unparseable part → `True`). `ver in versions_list` case-insensitive.
- `invoke_osv_query`: POST `https://api.osv.dev/v1/query` body `{"package": {"name": name, "ecosystem": OSV_ECO_MAP[eco]}}`, timeout 20; raises on failure (→ top-level error JSON, as PS). Per vuln: collect `ranges`/`versions` from `affected[]` whose `package.name` equals name (case-insensitive); include if no version or affected; record `{id, aliases (truthy only), summary, severity, affectedVersions}`.
- `invoke_ghsa_query`: GET `https://api.github.com/advisories?affects=<quote>&ecosystem=<ghsa eco>&per_page=100`, headers `Accept: application/vnd.github+json` + `Authorization: Bearer $GITHUB_TOKEN` if env set, timeout 20; any exception → `None`. Relevant if any `vulnerabilities[].package.name` matches (case-insensitive); include rule as PS; record `{id: ghsa_id, aliases: [cve_id] if cve_id, summary, severity, affectedVersions}`.
- `get_discrepancies` (CVE-prefixed aliases, insertion order), `get_risk_level`.
- Main: cache key `f"{eco}-{name}" + (f"-{version}" if version else "")`, dir `.vuln-cache`, TTL 24 → cache hit emits cached JSON and returns 0. Else GHSA `None` → `ghsaNote = "skipped — query failed or rate-limited"` (em dash verbatim), `ghsaResults = []`, `sources = ["OSV"]`; else `["OSV", "GHSA"]`. Output keys: `ecosystem, package, osvResults, ghsaResults, summary{totalCount, osvCount, ghsaCount, highestSeverity}, discrepancies, sources, riskLevel` then `version` (if given), `ghsaNote` (if set). Write cache. Any exception → `{ecosystem, package, error: str(e), riskLevel: "unknown"}`, exit 0.

**Rationale:** Range logic determines CVE-applies verdicts; byte-for-byte semantic mirror (including conservative quirks) avoids impl-dependent verdicts.

**Verification:** Harness §A semver/range/severity asserts + §B vuln-lookup fixture; live run here → OSV 403 → error JSON with `riskLevel: "unknown"`, exit 0.

**If this fails:** delete `scripts/vuln-lookup.py`.

---

### Step 4: Port dep-scan

**Objective:** `scripts/dep-scan.py` ≡ `dep-scan.ps1`.
**Confidence:** Medium (subprocess + lockfile parsing)
**Depends on:** None (copy severity helpers from Step 3 spec if Step 3 not yet done — standalone files)
**Do-Projex:** Encouraged
**Verify-Projex:** Encouraged

**Files:** `scripts/dep-scan.py` (new)

**Changes:**

- CLI: `-Ecosystem` (8 ecosystems), `-Name`, `-Version`, `-Tier/--tier` (int, choices `2 3`, default 2).
- Severity helpers identical to Step 3; `get_risk_level(severities)` ignores unknown/None.
- `get_npm_deps`: GET `https://registry.npmjs.org/{name}/{version or 'latest'}` (raw name), timeout 20 → `[{"Name", "VersionRange"}]`.
- `get_pypi_deps`: GET `https://pypi.org/pypi/{name}/{version + '/' if version else ''}json` → per `requires_dist`: strip `\[[^\]]*\]`, split `;` [0] strip, split `[>=<!~\s]` [0] strip → `{"Name", "VersionRange": None}`.
- `get_npm_full_tree` (Tier 3):

```python
npm = shutil.which("npm")          # resolves npm.cmd on Windows via PATHEXT
if not npm:
    raise RuntimeError("npm CLI unavailable")
# version check: `npm --version`, major < 6 → RuntimeError(f"npm {v} is below minimum required version 6");
# any failure → RuntimeError(f"npm version check failed: {e}")
tmp = tempfile.mkdtemp()
try:
    write package.json {"dependencies": {name: version or "*"}}
    r = subprocess.run([npm, "install", "--package-lock-only", "--ignore-scripts", "--silent"],
                       cwd=tmp, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=300)
    if r.returncode != 0: raise RuntimeError(f"npm install --package-lock-only failed (exit {r.returncode})")
    lock missing → RuntimeError("package-lock.json was not generated")
    parse: lock["packages"] (skip key ""; name = re.sub(r"^(.*node_modules/)", "", key); need version)
           elif lock["dependencies"] (v1: key + .version)
finally:
    shutil.rmtree(tmp, ignore_errors=True)
```

  **Do not change the npm flags** (`--package-lock-only --ignore-scripts`): they are what guarantees no audited code runs. `subprocess.TimeoutExpired` message becomes `fallbackReason`.
- `invoke_osv_batch(queries)`: batches of 1000 → POST `https://api.osv.dev/v1/querybatch` `{"queries": [{"package": {"ecosystem", "name"}, "version"?}]}` timeout 30; missing `results` → `[{"vulns": []}] * len(batch)`; stub enrichment (`id` and no `database_specific`/`severity`/`aliases`) via GET `/v1/vulns/{id}` timeout 15, per-batch dict cache, failure keeps stub. Returns list parallel to queries.
- `get_dep_findings(deps, osv_results)`: per dep worst severity; `cveIds = sorted(set(CVE-* aliases))`; high/critical → finding `{name, ecosystem, version (Version or VersionRange or None), severity, cveIds, depth}`; medium/low counters; collect worst per dep for overall risk.
- Main: line-for-line with PS — cache key `f"{eco}-{name}{'-' + version if version else ''}-t{tier}"`, dir `.dep-scan-cache`; cache hit → set `cacheHit = True`, emit, return 0. Unsupported ecosystem → `limitationNote = f"Direct dep resolution is not supported for ecosystem '{eco}'. Supported: npm, pypi."` and empty deps. Tier 3 non-npm → fallback + exact PS reason string; Tier 3 npm failure → fallback + exception message; depth 1 if name ∈ direct names else 2. Output keys: `ecosystem, package, tier (effective), directDepCount, findings, mediumCount, lowCount, riskLevel, fallback, sources: ["OSV"], cacheHit: False` then `version`, `transitiveDepCount`, `fallbackReason`, `limitationNote` when set. Write cache. Exception → `{ecosystem, package, tier, error, riskLevel: "unknown", fallback: False, cacheHit: False}`, exit 0.

**Rationale:** Same as Step 3; Tier 3 safety flags preserved explicitly.

**Verification:** Harness §B dep-scan fixtures; live `python3 -B scripts/dep-scan.py -Ecosystem npm -Name chalk -Version 5.3.0 -Tier 2` → `directDepCount: 0`, `riskLevel: "none"`, `findings: []` (no OSV call needed); rerun → `cacheHit: true`. Live `-Name mkdirp -Version 0.5.1 -Tier 3` → lockfile resolves via npm (registry reachable), then OSV 403 → error JSON (expected here); confirm temp dir removed (no new `/tmp` dir left with `package.json` containing `mkdirp`).

**If this fails:** delete `scripts/dep-scan.py`.

---

### Step 5: Switch Doc Call Sites to Python-First

**Objective:** Every invocation shows the Python form; prose names scripts by stem; one `.ps1` twin note per file.
**Confidence:** High
**Depends on:** Steps 1–4
**Do-Projex:** Encouraged

**Files:** `SKILL.md`, `references/criteria.md`, `references/criteria/registry-package.md`, `workflows/registry-package.md`

**Rules:**

- Invocation code lines: `.\scripts\<x>.ps1 <args>` → `python3 scripts/<x>.py <args>` (args unchanged).
- Prose / table / Audit-Coverage example refs: `` `<x>.ps1` `` → `` `<x>` `` (e.g. `Done -- vuln-lookup: none found (OSV, GHSA)`); `scripts/<x>.ps1` in prose → `scripts/<x>.py`.
- Twin note text (verbatim): `> **PowerShell hosts:** each `scripts/<script>.py` has a `scripts/<script>.ps1` twin taking identical arguments (e.g. `.\scripts\vuln-lookup.ps1 -Ecosystem npm -Name "lodash"`).`
- Never touch `init.ps1`/`install.ps1` NuGet red-flag mentions.

**Changes:**

`SKILL.md` (only these two lines):

```markdown
// Line 87 — Before (fragment):
..., and may invoke `scripts/registry-lookup.ps1`. Then return here for Step N.
// After:
..., and may invoke the lookup scripts in `scripts/` (see Reference Files). Then return here for Step N.

// Line 241 — Before:
- `scripts/registry-lookup.ps1` — Automated registry data lookup. Run: `powershell -File scripts/registry-lookup.ps1 <ecosystem> <name> [version]`. If PowerShell is unavailable, query registry APIs directly (npm: `registry.npmjs.org/<pkg>`, PyPI: `pypi.org/pypi/<pkg>/json`, etc.).
// After:
- `scripts/registry-lookup.py` | `typosquat-check.py` | `vuln-lookup.py` | `dep-scan.py` — registry metadata, npm typosquat, OSV+GHSA CVE, and dependency-CVE lookups; JSON to stdout. Run: `python3 scripts/<script>.py -Ecosystem <eco> -Name <name> [-Version <ver>]` (Python ≥3.8, stdlib only; Windows: `py -3`). PowerShell hosts: same-named `.ps1` twin, identical arguments. Neither available → query APIs directly (npm: `registry.npmjs.org/<pkg>`, PyPI: `pypi.org/pypi/<pkg>/json`, CVEs: POST `api.osv.dev/v1/query` with `{"package":{"name":"<pkg>","ecosystem":"<eco>"}}`, etc.).
```

`references/criteria.md`: L9 `scripts/registry-lookup.ps1` → `scripts/registry-lookup.py` and append sentence `On PowerShell hosts use the same-named `.ps1` twin (identical arguments); this applies to every script named below.` | L39 `registry-lookup.ps1` → `registry-lookup` | L63 → `scripts/typosquat-check.py` | L151 → `scripts/vuln-lookup.py` | L157 → `scripts/dep-scan.py` | L159 `vuln-lookup.ps1` → `vuln-lookup`.

`references/criteria/registry-package.md`: L153 → `scripts/dep-scan.py` | L160, L163, L221, L285 invocation → `python3 scripts/...py` | insert twin note + blank line after the closing fence of `## Transitive Dependency Scanning` → `### Invocation` block (after current L164) | L208–211, L270–271, L329–332 → stem | L279 → `scripts/vuln-lookup.py` | L292 `Set `$env:GITHUB_TOKEN`` → ``Set `GITHUB_TOKEN` (`export GITHUB_TOKEN=…`; PowerShell: `$env:GITHUB_TOKEN = '…'`)``.

`workflows/registry-package.md`: L40–44 table cells `registry-lookup.ps1 -Ecosystem <x>` → `registry-lookup -Ecosystem <x>` | L52 `scripts/registry-lookup.ps1` → `scripts/registry-lookup.py` (`.ps1` twin) | L96, L103, L210, L217, L231, L236 → `python3 scripts/...py` | insert twin note + blank line after the closing fence following L96 (first invocation) | L178, L277–278, L282–286, L290–292, L304, L308, L369–370 → stem.

**Verification:**

```bash
grep -n '\.ps1' SKILL.md workflows/*.md references/*.md references/criteria/*.md
```
Allowed residue only: `SKILL.md:156` (deferred) | `SKILL.md` Reference Files bullet (`.ps1` twin) | `references/criteria.md:9` twin sentence | `references/criteria/registry-package.md` twin note + NuGet `init.ps1`/`install.ps1` row (L134) | `workflows/registry-package.md` twin note + L52 twin mention + NuGet `init.ps1` (L257).

```bash
grep -c 'python3 scripts/' workflows/registry-package.md references/criteria/registry-package.md SKILL.md
```
Expect 6 | 4 | 1. `git diff --stat SKILL.md` → 2 lines changed (`git diff -U0 SKILL.md` hunks only at 87, 241).

**If this fails:** `git checkout -- <file>` for the offending doc; redo edits.

---

## Verification Plan

Harness: a throwaway script **outside the repo** (OS temp / agent scratchpad), run with `python3 -B` (no `scripts/__pycache__`). Loads each port via `importlib.util.spec_from_file_location("<stem>", "scripts/<stem>.py")`, monkeypatches module attributes, calls `module.main([...])` with stdout captured (`contextlib.redirect_stdout`), asserts on parsed JSON. Not committed.

### Automated Checks

- [ ] `python3 -c "import ast,sys; [ast.parse(open(f).read(), f, feature_version=(3,8)) for f in sys.argv[1:]]" scripts/*.py` → no error.
- [ ] `python3 -B scripts/<each>.py --help` → exit 0.
- [ ] `grep -nE '^\s*(import|from) ' scripts/*.py` → stdlib modules only.
- [ ] `git ls-files -s scripts/*.py` after staging → mode `100755`.
- [ ] **§A pure logic** (harness asserts):
  - typosquat: `get_levenshtein_distance("expresss","express") == 1`, `("lodahs","lodash") == 2`, `("","abc") == 3`; `get_comparison_token("@Scope/Foo__Bar") == "foo-bar"`.
  - vuln/dep: `compare_semver("4.17.20","4.17.21") == -1`; `("1.2","1.2.0") == -1`; `("1","2") == 0`; `("v2.0.0-beta","2.0.0") == 0`; `("0","1.0") == -1`; `("1.0", None) == 0`.
  - `test_osv_version_affected("0.0.8", [{"type":"SEMVER","events":[{"introduced":"0"},{"fixed":"0.2.1"}]}], []) is True`; same ranges with `"1.2.6"` → `False`; `(x, [], [])` → `True`; `("1.0.0", [], ["1.0.0"])` → `True`.
  - `test_ghsa_version_affected("4.17.20", ["< 4.17.21"]) is True`; `("4.17.21", [">= 4.0.0, < 4.17.21"]) is False`; `("1.0", ["garbage"]) is True`.
  - `get_severity_from_osv({"database_specific":{"severity":"MODERATE"}}) == "medium"`; `{"severity":[{"score":"9.8"}]}` → `critical`; `{"severity":[{"score":"CVSS:3.1/AV:N"}]}` → `medium`.
  - dep-scan `get_pypi_deps` with patched `http_json` returning `{"info":{"requires_dist":['urllib3[socks]>=1.21 ; extra == "socks"', "idna (<4,>=2.5)", "certifi"]}}` → names `["urllib3","idna","certifi"]`.
- [ ] **§B offline fixtures** (patch `http_json`; route by URL; patch `shutil.which` via `unittest.mock.patch.object(module.shutil, "which", return_value=None)`):
  - vuln-lookup `-Ecosystem npm -Name minimist -Version 0.0.8`: OSV → 1 vuln `{id:"GHSA-vh95-rmgr-6w4m", aliases:["CVE-2020-7598"], database_specific:{severity:"MODERATE"}, affected:[{package:{name:"minimist"}, ranges:[{type:"SEMVER", events:[{introduced:"0"},{fixed:"0.2.1"}]}]}]}`; GHSA → 1 advisory `{ghsa_id:"GHSA-vh95-rmgr-6w4m", cve_id:"CVE-2020-7598", severity:"medium", vulnerabilities:[{package:{name:"minimist"}, vulnerable_version_range:"< 0.2.1"}]}`. Expect `osvResults` list len 1, `summary == {totalCount:2, osvCount:1, ghsaCount:1, highestSeverity:"medium"}`, `discrepancies == {onlyInOsv:[], onlyInGhsa:[]}`, `sources == ["OSV","GHSA"]`, key order ends `riskLevel, version`. Clear `.vuln-cache` entry before/after.
  - Same with GHSA raising → `sources == ["OSV"]`, `ghsaNote` present, `ghsaResults == []`.
  - OSV raising → `{ecosystem, package, error, riskLevel:"unknown"}`.
  - dep-scan `npm mkdirp 0.5.1 -Tier 2`: npm manifest `{dependencies:{minimist:"0.0.8"}}`; querybatch → `{results:[{vulns:[{id:"GHSA-vh95-rmgr-6w4m", modified:"x"}]}]}` (stub); `/v1/vulns/GHSA-vh95-rmgr-6w4m` → full record with `database_specific.severity:"HIGH"`, aliases CVE-2020-7598. Expect `findings == [{name:"minimist", ecosystem:"npm", version:"0.0.8", severity:"high", cveIds:["CVE-2020-7598"], depth:1}]`, `riskLevel:"high"`, `directDepCount:1`, `cacheHit:false`; enrichment URL called once.
  - dep-scan `-Tier 3` with `shutil.which` patched → `None`: `fallback:true`, `fallbackReason:"npm CLI unavailable"`, `tier:2`.
  - dep-scan `-Ecosystem crates -Name serde`: `limitationNote` present, `directDepCount:0`, `riskLevel:"none"`.
  - typosquat `-Ecosystem npm -Name expresss -NoCache`: patch `get_npm_popular_baseline` → `[{"name":"express","downloads":9}, {"name":"lodash","downloads":8}]`; downloads stub routed by **exact** URL suffix (`/last-week/expresss` → `{"downloads":0}`, `/last-week/express` → `{"downloads":1000}` — substring routing would match both) → `closestMatches[0].name == "express"`, `downloadRatio.ratio == -1`, `riskLevel:"critical"`, `combosquatHints == ["express"]`.
  - Delete harness-created cache files afterwards.

### Manual Verification (live, network-dependent; record unreachable hosts in log rather than failing)

- [ ] Step 1 live runs (npm, scoped npm, pypi, crates, rubygems, nuget, not-found).
- [ ] Step 2 live `expresss -CompareTo express -NoCache`.
- [ ] Step 4 live chalk Tier 2 + cache hit; mkdirp Tier 3 lockfile path + temp-dir cleanup.
- [ ] If api.osv.dev reachable on executing host: vuln-lookup `npm lodash 4.17.20` → ≥1 CVE incl. CVE-2021-23337; dep-scan `npm mkdirp 0.5.1 -Tier 2` → minimist HIGH finding (mirrors evals ids for lodash/mkdirp).
- [ ] Read diffs of 4 docs: every code block still fenced; twin note renders as blockquote; no SKILL.md change outside 87/241.
- [ ] Remove agent-created cache dirs (`scripts/.typosquat-cache`, `.vuln-cache`, `.dep-scan-cache`) and any `__pycache__` before close; `git status --porcelain` shows only intended files.

### Acceptance Criteria Validation

| Criterion | How to Verify | Expected Result |
|---|---|---|
| 4 ports exist, exec, stdlib | `ls -l scripts/*.py`, import grep, `git ls-files -s` | 4 files, `100755`, stdlib only |
| Py 3.8 grammar + `--help` | `ast.parse(feature_version=(3,8))`, `--help` | no error, exit 0 |
| Flag parity | `--help` output vs `.ps1` `param()` | all PS params present + kebab aliases; positional for registry-lookup |
| JSON contract parity | Harness §B | key sets/order match `.ps1` `[ordered]@{}` blocks |
| Pure-logic parity | Harness §A | all asserts pass |
| Live usability | Manual live runs | reachable registries return populated JSON |
| Doc call sites | Step 5 greps | only allowed `.ps1` residue; counts 6/4/1 |
| SKILL.md minimal | `git diff -U0 SKILL.md` | hunks at 87, 241 only |

---

## Rollback Plan

1. Abandon ephemeral branch (`projex-abandon`) — all changes are new files + doc edits on that branch.
2. Partial keep: delete individual `scripts/<x>.py` and `git checkout -- <doc>`; `.ps1` files untouched so behavior reverts fully.

---

## Notes

### Known PS Defects Found During Research (not fixed here)

- **Typosquat baseline is not a popularity baseline (both impls, inherited).** `GET registry.npmjs.org/-/v1/search?text=boost-exact:false&size=250&popularity=1.0` now returns text matches for "boost" (2026-10-16: 116/250 names contain "boost"; `express`, `lodash`, `react`, `chalk` absent; every `score.detail.popularity == 1`). Without `-CompareTo`, `typosquat-check` cannot flag `expresss`. Needs its own plan (e.g. curated top-N list or `objects[].downloads.weekly` sort) applied to both `.ps1` and `.py`.
- **vuln-lookup.ps1 single-result unrolling:** with exactly one OSV hit, `osvResults` serializes as an object and `summary.osvCount` reads the ordered-dictionary key count (5); with zero hits `osvResults` is `null`. Same pattern for `ghsaResults`. Python port emits correct lists/counts (Divergence 1). Fixing `.ps1` (wrap with `@(...)`) is a separate patch.
- `registry-lookup.ps1` `maintainers` collapses to a string with one maintainer (same root cause).

### Risks

- Dual impl drift → docstring "change both together"; future script plans must list both files. Consider STEWARDSHIP entry later (not here).
- Unverifiable parity against live `.ps1` (no pwsh) → mitigated by line-for-line port + fixture asserts that pin PS semantics (incl. `[System.Version]` quirks).
- Proxy blocks OSV/GHSA here → success paths verified offline only; flagged in log; first host with OSV access should run the live CVE checks.
- `python3` missing on some Windows hosts → `.ps1` twin documented; manual API fallback documented for all four.
- Eval graders reading `expected_output` literally (`vuln-lookup.ps1`) → assertions are concept-based with OR clauses; sibling eval plan may neutralize names.

### Split Decision

`No split — single scope, within size budget` (~570 lines but 5 steps; heuristic needs both > 500 lines and > 5 steps; all files in root `.projex` scope; no upstream/downstream mix; Steps 1–4 can run independently, Step 5 needs all four).

### Open Questions

(none)
