# Lookup Script Correctness Fixes

> **Status:** Ready
> **Author:** Claude (Opus)
> **Parent:** 2610161849-python-script-ports-walkthrough.md
> **Source:** Direct request (orchestrator) — follow-ups recorded in 2610161849-python-script-ports-walkthrough.md § Immediate Follow-ups
> **Related Projex:** 2610161849-python-script-ports-plan.md | 2610161849-python-script-ports-walkthrough.md | 2610161850-eval-runner-harness-plan.md | 2610161910-dispatcher-lean-report-and-trigger-plan.md (executed; no file overlap)
> **Worktree:** Yes

---

## Summary

Fixes 5 verified correctness bugs in the lookup scripts (`.ps1` + Python twins). It also adds the first committed offline regression suite for `scripts/`, which runs the `.ps1` twins when `pwsh` is on PATH.

| # | Bug (re-verified 2026-10-16) | Impls | Effect |
|---|---|---|---|
| B1 | `typosquat-check` baseline query `text=boost-exact:false…` returns "boost" text matches: 116/250 names contain "boost", express/lodash/react/chalk all absent, every `downloads` = 10000000 | both | `expresss` → `riskLevel: low`, no matches (eval 3). `chalk` → matches `@boost/cli` (eval 4) |
| B2 | `typosquat-check` reports `'<name>' does not appear to exist on npm` whenever api.npmjs.org downloads fails (blocked/offline). Separately, once the baseline is real, popular packages flag each other (`chalk`→`chai` distance 2 → `medium`; `react` prefixes `react-dom` → combosquat) | both | False "does not exist" note on every package when downloads API unreachable. False positives on popular packages after B1 fix |
| B3 | `vuln-lookup` open-ended OSV range `introduced: "0"` (no `fixed`/`last_affected`) → NOT affected when `-Version` given | both | False negative: "all versions vulnerable" advisories dropped |
| B4 | `vuln-lookup.ps1` pipeline unrolling: 1 OSV hit → `osvResults` object, `summary.osvCount` = 5 (dict key count); 0 hits → `null`. **New:** GHSA success with 0 advisories → `$null` → reported `ghsaNote: "skipped — query failed or rate-limited"`, `sources: ["OSV"]` | `.ps1` | Wrong counts; coverage misreported as GHSA-skipped for every clean package |
| B5 | `registry-lookup.ps1` unrolling: 1 maintainer → `maintainers: "solo"` (npm + PyPI); **new:** 1 install hook → `installScripts` object | `.ps1` | Wrong JSON shape vs documented arrays |

**Scope:** `scripts/{vuln-lookup,registry-lookup,typosquat-check}.{ps1,py}` | new `scripts/data/npm-popular.tsv` + `scripts/data/refresh-npm-popular.py` | new `tests/test_lookup_scripts.py` | `.gitignore` | `references/criteria/registry-package.md` (typosquat section) | `STEWARDSHIP.md` (one paragraph). No `SKILL.md`, no `dep-scan.*`, no evals changes.
**Estimated Changes:** 6 edited scripts, 2 new data/tool files, 1 new test file, 3 doc/config edits. ~14 functions touched.

---

## Objective

### Problem / Gap / Need
Lookup scripts are the "hard data" layer of every registry-package audit. B1 disables npm typosquat detection entirely. B3 hides vulnerabilities. B4/B5 make the `.ps1` JSON contract (documented as arrays + counts) wrong for PowerShell hosts, and B4 misreports GHSA coverage. No committed test exercises any script, so these regressions went unnoticed. The parent walkthrough lists "committed fixture harness" under Future Considerations.

### Success Criteria
- [ ] `python3 -m unittest discover -s tests -p "test_*.py"` → `OK`, 19 tests, 0 skipped when `pwsh` on PATH; `OK (skipped=6)` without `pwsh`
- [ ] Same suite on pre-fix scripts fails (red check run once in Step 1; ≥ 11 failures)
- [ ] `typosquat-check.{py,ps1} -Ecosystem npm -Name expresss` (live, registry.npmjs.org) → `riskLevel` `high` or `critical`, `closestMatches[0].name == "express"`, distance 1
- [ ] `typosquat-check.{py,ps1} -Ecosystem npm -Name chalk` → `riskLevel: low`, details start `'chalk' is in the bundled top-1000`
- [ ] `scripts/data/npm-popular.tsv`: ≥ 1000 rows, unscoped, unique, weekly downloads non-increasing; contains express | lodash | react | chalk | cross-env | prettier | semver | commander
- [ ] `vuln-lookup` with OSV `introduced:"0"` only + `-Version 1.0.0` → advisory included (both impls; tests)
- [ ] `vuln-lookup.ps1`: 1 hit → `osvResults` list len 1 and `osvCount: 1`; 0 hits → `[]`; GHSA `[]` → `sources: ["OSV","GHSA"]`, no `ghsaNote`; GHSA failure → `["OSV"]` + `ghsaNote` (tests)
- [ ] `registry-lookup.ps1`: 1 maintainer → `["solo"]`; 1 hook → 1-element `installScripts` list (npm + PyPI; tests)
- [ ] `.gitignore` ignores `__pycache__/`; `git status --porcelain` shows no `__pycache__` after running both test suites
- [ ] Python files parse with `ast.parse(..., feature_version=(3, 8))`; `.ps1` edits use no PS 6+/7-only syntax (static check, see Verification)
- [ ] No live `claude -p` eval runs required

### Out of Scope
- `dep-scan.{ps1,py}`: reviewed. `.ps1` already wraps (`@(switch …)`, `@($findings)`), so no defect here.
- `SKILL.md` (Red Flag citing `riskLevel: critical` stays valid: distance-1 + ≥1000× download ratio still yields `critical` when api.npmjs.org is reachable)
- Scope-impersonation scoring (`@evil/chalk` basename equals popular `chalk` → self-skip). Pre-existing; docs already require a manual scope check. See Notes → follow-ups.
- Download-count fallback when api.npmjs.org is blocked (ratio stays `null`; risk then rests on distance)
- Non-npm typosquat support; `evals/evals.json` changes; live eval runs (cost money; need orchestrator approval)
- PowerShell 5.1 runtime testing (only pwsh 7.4 available; 5.1 compatibility checked statically)

---

## Context

### Current State
- `typosquat-check`: `Get-NpmPopularBaseline` / `get_npm_popular_baseline` GET `registry.npmjs.org/-/v1/search?text=boost-exact:false&size=$Size&popularity=1.0`, cache in `scripts/.typosquat-cache/`. npm search now ignores the `popularity` weight (all `score.detail.popularity == 1`) and treats `boost-exact:false` as text. Existence = `$null -ne (Get-NpmWeeklyDownloads $Name)` (api.npmjs.org). Self-skip compares normalized tokens; there is no "queried name is itself popular" rule. With the broken baseline this never mattered.
- npm search objects now carry real `downloads.weekly` (verified: `express` 145,199,376). Name-specific search can't find typo targets (`expresss` → no `express`; `lodahs` → no `lodash`), so a bundled ranked list is the fix, and search is only the data source for refreshing it.
- `vuln-lookup`: `Test-OsvVersionAffected` / `test_osv_version_affected` open-ended tail: `$floor = if ($introduced -eq '0') { -1 } …; if ($floor -ge 0)` → never true for `"0"`.
- `.ps1` unrolling: `return $results` (array) from a function → 0 items ⇒ `$null`, 1 item ⇒ the item. `X = if (…) { $arr }` inside a hashtable literal unrolls the same way. `@(…) | Where-Object` outside the `@()` unrolls too.
- Verified in pwsh 7.4.6 with mocked HTTP (planning-time probes, discarded): B4 one-hit → `osvCount: 5`, `ghsaNote` set although GHSA mock returned `[]`; B3 `-Version 1.0.0` → `osvResults: null`, `riskLevel: none`; B5 → `maintainers: "solo"`, `installScripts: {…}`. Every fix below was prototyped on scratch copies. The test suite in Step 1 passed 19/19 against them and failed 13 against current scripts.

### Key Files

> Quick reference — detailed changes are in Implementation steps below.

| File | Role | Change Summary |
|------|------|----------------|
| `tests/test_lookup_scripts.py` | New offline regression suite | Python unit + `.ps1` mock-HTTP tests (pwsh-gated) + twin parity |
| `.gitignore` | Ignore rules | add `__pycache__/` |
| `scripts/vuln-lookup.ps1` | OSV+GHSA lookup | B3 range fix; B4 `return ,$results` ×3 |
| `scripts/vuln-lookup.py` | Python twin | B3 range fix; docstring drops divergence note |
| `scripts/registry-lookup.ps1` | Registry metadata | B5 `@()` wraps ×2, `,$installScripts` |
| `scripts/registry-lookup.py` | Python twin | docstring: only UTC-date divergence remains |
| `scripts/data/refresh-npm-popular.py` | New maintainer tool | builds ranked unscoped top-N TSV from npm search |
| `scripts/data/npm-popular.tsv` | New bundled baseline | generated: 1000 rows `name<TAB>weekly` |
| `scripts/typosquat-check.ps1` | npm typosquat | bundled baseline; known-popular rule; HEAD existence check; cache removed; `-Size` 1000 |
| `scripts/typosquat-check.py` | Python twin | same as `.ps1` |
| `references/criteria/registry-package.md` | Typosquat interpretation | baseline paragraph; `closestMatches` row wording |
| `STEWARDSHIP.md` | Maintenance guide | test command + baseline refresh paragraph |

### Dependencies
- **Requires:** base `claude/youthful-dijkstra-5ov1kt` at or after `d22b53c` (python twins `f4e03a3` present). registry.npmjs.org reachable (Step 4 generator + live checks). pwsh 7.x for `.ps1` verification (bootstrap below).
- **Blocks:** nothing. Unblocks meaningful re-runs of evals 3/4 (separately approved).

### Constraints
- Twin rule: same flags, same JSON keys, change both together. Python stays stdlib-only, ≥ 3.8. `.ps1` must stay Windows PowerShell 5.1-compatible: no `??`, `?.`, ternary `a ? b : c`, `-AsHashtable`, `ForEach-Object -Parallel`, `Join-Path` with >2 positional args.
- Source Hygiene (SKILL.md of projex framework): no projex refs in code comments; non-obvious choices carry rationale naming the rejected alternative. Every comment below is written to that rule; copy it verbatim.
- CLI compatibility: `-CacheHours` / `-NoCache` stay accepted (ignored). Removing them would break existing invocations with an argparse/param-binding error.
- Eval harness snapshot copies tracked `scripts/**` via `git ls-files` (`evals/run_evals.py` `snapshot_files`), so `scripts/data/*` reaches eval runs once committed. Tests live in top-level `tests/` so they are **not** snapshotted.

### Assumptions
- npm search API keeps returning `objects[].downloads.weekly` (verified 2026-10-16). Only the refresh tool depends on it; runtime does not.
- `HEAD https://registry.npmjs.org/<EscapeDataString(name)>` → 200 exists / 404 missing (verified for `chalk`, `%40babel%2Fcore`, `this-pkg-should-not-exist-zq9x7` → 404).
- pwsh 7.4.6 linux-x64 tarball downloadable from github.com through the proxy (verified HEAD 200 and full download at planning time).

### Impact Analysis
- **Direct:** files in Key Files.
- **Adjacent:** `workflows/registry-package.md` and `references/criteria/registry-package.md` describe `typosquat-check` output keys. Keys are unchanged, only values change (`downloads` now real snapshot counts; `details` wording). `references/criteria.md` / `SKILL.md` mention scripts by name only.
- **Downstream:** audits see `riskLevel` change: typo names go from `low` to `high`/`critical`; popular names stay `low`, and their `details` now say "in the bundled top-1000". PowerShell-host audits see arrays and correct `osvCount`/`sources`. Old `scripts/.typosquat-cache/` dirs on user machines become unused (still gitignored).

---

## Implementation

### Overview
TDD order: Step 1 commits the suite (red), Steps 2–5 fix each script pair (green per class), Step 6 updates docs. Code below is the version that passed 19/19 in planning-time prototypes. Apply it literally.

**Prerequisite: pwsh bootstrap (not committed, outside the repo).** In the session scratchpad (call it `$SP`):
```bash
mkdir -p "$SP/pwsh-dl" "$SP/pwsh"
# download (python urllib; curl is blocked by the repo's CLAUDE.md routing rules)
python3 -I -c 'import sys,urllib.request,shutil; r=urllib.request.urlopen(urllib.request.Request(sys.argv[1],headers={"User-Agent":"x"}),timeout=300); shutil.copyfileobj(r,open(sys.argv[2],"wb"))' \
  https://github.com/PowerShell/PowerShell/releases/download/v7.4.6/powershell-7.4.6-linux-x64.tar.gz "$SP/pwsh-dl/pwsh.tgz"
tar -xzf "$SP/pwsh-dl/pwsh.tgz" -C "$SP/pwsh" && chmod +x "$SP/pwsh/pwsh"
"$SP/pwsh/pwsh" -NoProfile -Command '$PSVersionTable.PSVersion.ToString()'   # expect 7.4.6
```
Run tests with `PATH="$SP/pwsh:$PATH"`. **If the download fails:** continue. The 6 pwsh tests skip, and `.ps1` changes are verified by the static checklist in Verification Plan only. The execution log must then state "`.ps1` changes NOT executed — static review only".

All commands below run from `<work-root>` (worktree path).

---

### Step 1: Offline regression suite + `.gitignore`

**Objective:** Commit the suite first; observe red on current scripts.
**Confidence:** High (passed 19/19 vs prototypes; 13 red vs current)
**Depends on:** None
**Do-Projex:** Encouraged

**Files:**
- `tests/test_lookup_scripts.py` (new)
- `.gitignore`

**Changes:**

`.gitignore`:
```gitignore
// Before:
.claude/settings.local.json
scripts/.typosquat-cache/
scripts/.vuln-cache/
scripts/.dep-scan-cache/

// After:
.claude/settings.local.json
scripts/.typosquat-cache/
scripts/.vuln-cache/
scripts/.dep-scan-cache/
__pycache__/
```

`tests/test_lookup_scripts.py` (new, verbatim):
```python
"""Offline regression tests for the lookup scripts in scripts/ and their .ps1 twins.

No network. Python tests replace each module's HTTP helpers. PowerShell tests run when
`pwsh` is on PATH: they copy the .ps1 into a temp dir (so caches land there, not in
scripts/) and run it behind global Invoke-RestMethod / Invoke-WebRequest functions,
which take precedence over the cmdlets of the same name.

Run: python3 -m unittest discover -s tests -p "test_*.py"
"""
import contextlib
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True  # importing the scripts must not leave scripts/__pycache__ behind

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
PWSH = shutil.which("pwsh")


def load(stem):
    spec = importlib.util.spec_from_file_location(stem.replace("-", "_"), SCRIPTS / (stem + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_main(mod, argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        mod.main(argv)
    return json.loads(buf.getvalue())


PS_MOCK = r"""
$ErrorActionPreference = 'Stop'
$global:MockRoutes = @(Get-Content -Raw -Path $env:MOCK_ROUTES | ConvertFrom-Json)
function global:Invoke-RestMethod {
    param($Uri, $Method, $ContentType, $Body, $Headers, $TimeoutSec)
    foreach ($r in $global:MockRoutes) {
        if ("$Uri".Contains($r.match)) {
            if ($r.fail) { throw "mock: $Uri unreachable" }
            return $r.body
        }
    }
    throw "mock: no route for $Uri"
}
function global:Invoke-WebRequest {
    param($Uri, $Method, $Headers, $TimeoutSec, [switch]$UseBasicParsing)
    foreach ($r in $global:MockRoutes) {
        if ("$Uri".Contains($r.match)) {
            if ($r.status -eq 404) {
                $msg = [System.Net.Http.HttpResponseMessage]::new([System.Net.HttpStatusCode]::NotFound)
                throw [Microsoft.PowerShell.Commands.HttpResponseException]::new('404 (Not Found)', $msg)
            }
            if ($r.fail) { throw "mock: $Uri unreachable" }
            return [pscustomobject]@{ StatusCode = 200 }
        }
    }
    throw "mock: no route for $Uri"
}
$params = Get-Content -Raw -Path $env:MOCK_PARAMS | ConvertFrom-Json -AsHashtable
& $env:MOCK_SCRIPT @params
"""


def run_ps(stem, params, routes, baseline_tsv=None):
    """Run scripts/<stem>.ps1 offline. routes: [{match, body?, fail?, status?}], first match wins."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        script = tmp / (stem + ".ps1")
        shutil.copy2(SCRIPTS / (stem + ".ps1"), script)
        if baseline_tsv is not None:
            (tmp / "data").mkdir()
            (tmp / "data" / "npm-popular.tsv").write_text(baseline_tsv, encoding="utf-8")
        (tmp / "routes.json").write_text(json.dumps(routes), encoding="utf-8")
        (tmp / "params.json").write_text(json.dumps(params), encoding="utf-8")
        (tmp / "mock.ps1").write_text(PS_MOCK, encoding="utf-8")
        env = dict(os.environ, MOCK_ROUTES=str(tmp / "routes.json"),
                   MOCK_PARAMS=str(tmp / "params.json"), MOCK_SCRIPT=str(script))
        proc = subprocess.run([PWSH, "-NoProfile", "-NonInteractive", "-File", str(tmp / "mock.ps1")],
                              capture_output=True, text=True, env=env, timeout=180)
        if not proc.stdout.strip().startswith("{"):
            raise AssertionError("pwsh produced no JSON:\n" + proc.stderr + proc.stdout)
        return json.loads(proc.stdout)


# ── Fixtures ────────────────────────────────────────────────────────────────

OSV_ALL_VERSIONS = {"vulns": [{
    "id": "GHSA-test-0001", "aliases": ["CVE-2099-0001"], "summary": "fixture vuln",
    "database_specific": {"severity": "HIGH"},
    "affected": [{"package": {"name": "fixpkg"},
                  "ranges": [{"type": "SEMVER", "events": [{"introduced": "0"}]}]}],
}]}

NPM_ONE_MAINTAINER = {
    "name": "fixpkg", "description": "fixture", "dist-tags": {"latest": "1.0.0"},
    "maintainers": [{"name": "solo"}],
    "versions": {"1.0.0": {"license": "MIT", "scripts": {"postinstall": "node x.js"}}},
    "time": {"created": "2020-01-01T00:00:00Z", "modified": "2020-01-01T00:00:00Z",
             "1.0.0": "2020-01-01T00:00:00Z"},
}

PYPI_ONE_AUTHOR = {
    "info": {"name": "fixpkg", "version": "1.0.0", "summary": "fixture", "license": "MIT",
             "author": "solo", "maintainer": None, "requires_dist": None, "project_urls": None,
             "classifiers": []},
    "urls": [], "releases": {"1.0.0": []},
}

BASELINE_TSV = """# fixture baseline
chalk\t500000000
react\t180000000
react-dom\t170000000
lodash\t160000000
express\t145000000
chai\t140000000
cross-env\t26000000
"""


# ── vuln-lookup ─────────────────────────────────────────────────────────────

class VulnLookupPython(unittest.TestCase):
    def setUp(self):
        self.mod = load("vuln-lookup")
        self.tmp = tempfile.TemporaryDirectory()
        self.mod.CACHE_DIR = self.tmp.name  # absolute: os.path.join(SCRIPT_DIR, abs) -> abs

    def tearDown(self):
        self.tmp.cleanup()

    def test_osv_range_matrix(self):
        f = self.mod.test_osv_version_affected
        semver = lambda *events: [{"type": "SEMVER", "events": list(events)}]
        self.assertTrue(f("1.0.0", semver({"introduced": "0"}), []))            # all versions affected
        self.assertTrue(f("0.0.8", semver({"introduced": "0"}, {"fixed": "0.2.1"}), []))
        self.assertFalse(f("1.2.6", semver({"introduced": "0"}, {"fixed": "0.2.1"}), []))
        self.assertTrue(f("1.5.0", semver({"introduced": "1.0.0"}), []))        # open-ended, above floor
        self.assertFalse(f("0.9.0", semver({"introduced": "1.0.0"}), []))       # open-ended, below floor
        self.assertTrue(f("2.0.0", semver({"introduced": "1.0.0"}, {"last_affected": "2.0.0"}), []))
        self.assertTrue(f("1.0.0", [], []))                                      # no data: conservative
        self.assertTrue(f("1.0.0", [], ["1.0.0"]))

    def _run(self, argv, ghsa):
        def fake_http_json(url, **kw):
            if "osv.dev" in url:
                return OSV_ALL_VERSIONS
            if isinstance(ghsa, Exception):
                raise ghsa
            return ghsa
        self.mod.http_json = fake_http_json
        return run_main(self.mod, argv)

    def test_version_filter_keeps_introduced_zero(self):
        out = self._run(["-Ecosystem", "npm", "-Name", "fixpkg", "-Version", "1.0.0"], [])
        self.assertEqual(len(out["osvResults"]), 1)
        self.assertEqual(out["summary"], {"totalCount": 1, "osvCount": 1, "ghsaCount": 0, "highestSeverity": "high"})
        self.assertEqual(out["sources"], ["OSV", "GHSA"])
        self.assertNotIn("ghsaNote", out)

    def test_ghsa_failure_is_reported(self):
        out = self._run(["-Ecosystem", "npm", "-Name", "fixpkg"], OSError("blocked"))
        self.assertEqual(out["sources"], ["OSV"])
        self.assertEqual(out["ghsaResults"], [])
        self.assertIn("ghsaNote", out)


@unittest.skipUnless(PWSH, "pwsh not on PATH")
class VulnLookupPowerShell(unittest.TestCase):
    def test_single_hit_is_an_array(self):
        out = run_ps("vuln-lookup", {"Ecosystem": "npm", "Name": "fixpkg"},
                     [{"match": "api.osv.dev", "body": OSV_ALL_VERSIONS}, {"match": "api.github.com", "body": []}])
        self.assertIsInstance(out["osvResults"], list)
        self.assertEqual(len(out["osvResults"]), 1)
        self.assertEqual(out["summary"], {"totalCount": 1, "osvCount": 1, "ghsaCount": 0, "highestSeverity": "high"})

    def test_zero_hits_and_empty_ghsa_success(self):
        out = run_ps("vuln-lookup", {"Ecosystem": "npm", "Name": "fixpkg"},
                     [{"match": "api.osv.dev", "body": {}}, {"match": "api.github.com", "body": []}])
        self.assertEqual(out["osvResults"], [])
        self.assertEqual(out["ghsaResults"], [])
        self.assertEqual(out["sources"], ["OSV", "GHSA"])
        self.assertNotIn("ghsaNote", out)

    def test_version_filter_keeps_introduced_zero(self):
        out = run_ps("vuln-lookup", {"Ecosystem": "npm", "Name": "fixpkg", "Version": "1.0.0"},
                     [{"match": "api.osv.dev", "body": OSV_ALL_VERSIONS}, {"match": "api.github.com", "body": []}])
        self.assertEqual(len(out["osvResults"]), 1)
        self.assertEqual(out["riskLevel"], "high")

    def test_ghsa_failure_is_reported(self):
        out = run_ps("vuln-lookup", {"Ecosystem": "npm", "Name": "fixpkg"},
                     [{"match": "api.osv.dev", "body": OSV_ALL_VERSIONS}, {"match": "api.github.com", "fail": True}])
        self.assertEqual(out["sources"], ["OSV"])
        self.assertEqual(out["ghsaResults"], [])
        self.assertIn("ghsaNote", out)


# ── registry-lookup ─────────────────────────────────────────────────────────

REGISTRY_ROUTES = [
    {"match": "registry.npmjs.org", "body": NPM_ONE_MAINTAINER},
    {"match": "pypi.org/pypi/", "body": PYPI_ONE_AUTHOR},
    {"match": "", "fail": True},  # downloads, pypistats, scorecard: unreachable
]
ONE_HOOK = [{"hook": "postinstall", "command": "node x.js"}]


class RegistryLookupPython(unittest.TestCase):
    def setUp(self):
        self.mod = load("registry-lookup")

        def fake_invoke_api(url, timeout=15):
            for r in REGISTRY_ROUTES:
                if r["match"] in url:
                    return None if r.get("fail") else r["body"]
        self.mod.invoke_api = fake_invoke_api

    def test_single_entries_are_arrays(self):
        npm = run_main(self.mod, ["npm", "fixpkg"])
        self.assertEqual((npm["maintainers"], npm["maintainerCount"], npm["installScripts"]), (["solo"], 1, ONE_HOOK))
        pypi = run_main(self.mod, ["pypi", "fixpkg"])
        self.assertEqual((pypi["maintainers"], pypi["maintainerCount"]), (["solo"], 1))


@unittest.skipUnless(PWSH, "pwsh not on PATH")
class RegistryLookupPowerShell(unittest.TestCase):
    def test_single_entries_are_arrays(self):
        npm = run_ps("registry-lookup", {"Ecosystem": "npm", "Name": "fixpkg"}, REGISTRY_ROUTES)
        self.assertEqual((npm["maintainers"], npm["maintainerCount"], npm["installScripts"]), (["solo"], 1, ONE_HOOK))
        pypi = run_ps("registry-lookup", {"Ecosystem": "pypi", "Name": "fixpkg"}, REGISTRY_ROUTES)
        self.assertEqual((pypi["maintainers"], pypi["maintainerCount"]), (["solo"], 1))


# ── typosquat-check ─────────────────────────────────────────────────────────

class TyposquatPython(unittest.TestCase):
    def setUp(self):
        self.mod = load("typosquat-check")
        self.tmp = tempfile.TemporaryDirectory()
        path = Path(self.tmp.name) / "npm-popular.tsv"
        path.write_text(BASELINE_TSV, encoding="utf-8")
        self.mod.BASELINE_PATH = str(path)
        self.mod.get_npm_weekly_downloads = lambda name: None
        self.exists = True
        self.mod.npm_package_exists = lambda name: self.exists

    def tearDown(self):
        self.tmp.cleanup()

    def check(self, *args):
        return run_main(self.mod, ["-Ecosystem", "npm", "-Name"] + list(args))

    def test_typo_of_popular_package_is_high(self):
        out = self.check("expresss")
        self.assertEqual(out["riskLevel"], "high")
        self.assertEqual(out["closestMatches"][0], {"name": "express", "distance": 1, "downloads": 145000000})

    def test_separator_typo_is_high(self):
        self.assertEqual(self.check("crossenv")["closestMatches"][0]["name"], "cross-env")

    def test_known_popular_packages_are_low(self):
        for name in ("chalk", "react"):  # chalk~chai (distance 2), react prefixes react-dom
            out = self.check(name)
            self.assertEqual(out["riskLevel"], "low", name)
            self.assertEqual(out["combosquatHints"], [], name)
            self.assertTrue(out["details"].startswith("'%s' is in the bundled top-7" % name), out["details"])

    def test_scoped_name_is_not_known_popular(self):
        self.assertNotIn("is in the bundled", self.check("@evil/chalk")["details"])

    def test_size_limits_baseline(self):
        self.assertEqual(self.check("expresss", "-Size", "2")["riskLevel"], "low")

    def test_existence_notes(self):
        self.exists = False
        self.assertIn("registry returned 404", self.check("zzqqxx")["details"])
        self.exists = None
        self.assertIn("could not confirm", self.check("zzqqxx")["details"])

    def test_missing_baseline_still_checks_compare_to(self):
        self.mod.BASELINE_PATH = str(Path(self.tmp.name) / "absent.tsv")
        out = self.check("lodahs", "-CompareTo", "lodash")
        self.assertEqual(out["riskLevel"], "high")
        self.assertIn("missing or unreadable", out["details"])

    def test_legacy_cache_flags_accepted(self):
        self.assertEqual(self.check("expresss", "-NoCache", "-CacheHours", "1")["riskLevel"], "high")


class BundledBaseline(unittest.TestCase):
    def test_bundled_file_shape(self):
        rows = []
        for line in (SCRIPTS / "data" / "npm-popular.tsv").read_text(encoding="utf-8").splitlines():
            if line.strip() and not line.startswith("#"):
                name, weekly = line.split("\t")
                rows.append((name, int(weekly)))
        names = [n for n, _ in rows]
        self.assertGreaterEqual(len(rows), 1000)
        self.assertEqual(len(names), len(set(names)))
        self.assertFalse([n for n in names if n.startswith("@")])
        self.assertEqual([w for _, w in rows], sorted((w for _, w in rows), reverse=True))
        for must in ("express", "lodash", "react", "chalk", "cross-env", "prettier", "semver", "commander"):
            self.assertIn(must, names)


@unittest.skipUnless(PWSH, "pwsh not on PATH")
class TyposquatParity(unittest.TestCase):
    """The .ps1 must emit exactly what the .py emits for the same baseline, offline."""

    def test_twins_agree(self):
        py = TyposquatPython("test_typo_of_popular_package_is_high")
        py.setUp()
        try:
            for args in (["expresss"], ["chalk"], ["react"], ["lodahs", "-CompareTo", "lodash"], ["expresss", "-Size", "2"]):
                params = {"Ecosystem": "npm", "Name": args[0]}
                for flag, value in zip(args[1::2], args[2::2]):
                    params[flag.lstrip("-")] = int(value) if value.isdigit() else value
                ps = run_ps("typosquat-check", params,
                            [{"match": "api.npmjs.org", "fail": True}, {"match": "registry.npmjs.org", "status": 200}],
                            baseline_tsv=BASELINE_TSV)
                self.assertEqual(ps, py.check(*args), args)
        finally:
            py.tearDown()


if __name__ == "__main__":
    unittest.main()
```

**Rationale:** Top-level `tests/` keeps tests out of the eval snapshot (`SNAPSHOT_DIRS` covers `scripts/`). Function-shadowing mocks (a PS function beats a cmdlet of the same name) run the real `.ps1` offline with no script edits for testability. Temp-dir copies keep `$PSScriptRoot` caches out of `scripts/`. Rejected: a pwsh fixture harness kept out of the repo (as in the python-ports execution). It leaves nothing to catch the next drift.

**Verification:** `PATH="$SP/pwsh:$PATH" python3 -m unittest discover -s tests -p "test_*.py"` → FAILED. Expect failures/errors in at least: `TyposquatPython.*` (most; `get_npm_popular_baseline` signature/`BASELINE_PATH` absent), `VulnLookupPython.test_osv_range_matrix`, `VulnLookupPython.test_version_filter_keeps_introduced_zero`, `VulnLookupPowerShell.*` (except `test_ghsa_failure_is_reported`), `RegistryLookupPowerShell.test_single_entries_are_arrays`, `BundledBaseline` (file absent until Step 4), `TyposquatParity`. Record the failure list in the log. **Note:** red-run `TyposquatPython` tests on old code make live npm search calls and create `scripts/.typosquat-cache/`. Delete that dir after the red run.

**If this fails:** Suite errors on import (not assertion failures) → check `ROOT`/`SCRIPTS` resolution (`tests/` must sit at repo root). Revert: delete `tests/`, restore `.gitignore`.

---

### Step 2: `vuln-lookup` — B3 range fix (both) + B4 unrolling (`.ps1`)

**Objective:** `introduced:"0"` open-ended ranges count as affected; `.ps1` returns true arrays so counts and GHSA success detection are right.
**Confidence:** High
**Depends on:** Step 1
**Verify-Projex:** Encouraged

**Files:**
- `scripts/vuln-lookup.ps1`
- `scripts/vuln-lookup.py`

**Changes:**

`scripts/vuln-lookup.ps1` — `Test-OsvVersionAffected` tail:
```powershell
// Before:
            # Open-ended range (introduced, no fixed)
            if ($null -ne $introduced) {
                $floor = if ($introduced -eq '0') { -1 } else { Compare-SemVer $Ver $introduced }
                if ($floor -ge 0) { return $true }
            }

// After:
            # Open-ended range (introduced, no fixed/last_affected). introduced '0' is OSV's
            # "every version" marker; it must not be compared as a version.
            if ($null -ne $introduced) {
                if ($introduced -eq '0' -or (Compare-SemVer $Ver $introduced) -ge 0) { return $true }
            }
```

`scripts/vuln-lookup.ps1` — `Invoke-OsvQuery` (two returns):
```powershell
// Before:
    $results = @()
    if (-not $resp.vulns) { return $results }
…
        }
    }
    return $results
}

# ─── GHSA query

// After:
    $results = @()
    # Leading comma on every return: a bare `return $results` lets the pipeline unroll a
    # 1-element array to its dictionary (so .Count reads the key count, 5) and an empty
    # array to $null.
    if (-not $resp.vulns) { return ,$results }
…
        }
    }
    return ,$results
}

# ─── GHSA query
```

`scripts/vuln-lookup.ps1` — `Invoke-GhsaQuery` success return (the `catch { return $null }` stays):
```powershell
// Before:
        return $results
    } catch {

// After:
        # Leading comma as in Invoke-OsvQuery. Wrapping the call site in @() instead would
        # turn this function's $null (query failed) into a 1-element array, and an
        # unwrapped empty result would read as $null, i.e. "GHSA skipped".
        return ,$results
    } catch {
```

`scripts/vuln-lookup.py` — `test_osv_version_affected` tail:
```python
# Before:
        # Open-ended range (introduced, no fixed)
        if introduced is not None:
            floor = -1 if introduced == "0" else compare_semver(ver, introduced)
            if floor >= 0:
                return True

# After:
        # Open-ended range (introduced, no fixed/last_affected). introduced "0" is OSV's
        # "every version" marker; it must not be compared as a version.
        if introduced is not None:
            if introduced == "0" or compare_semver(ver, introduced) >= 0:
                return True
```

`scripts/vuln-lookup.py` — module docstring:
```python
# Before:
Python twin of vuln-lookup.ps1: same flags, same JSON keys. Change both together.
Intentional divergences from the .ps1: arrays are always emitted as arrays (the
.ps1 collapses one-element results to a scalar/object and empty ones to null, and
then reports osvCount as the dictionary key count); this port reports true lists
and counts.

# After:
Python twin of vuln-lookup.ps1: same flags, same JSON keys. Change both together.
```

**Rationale:** `,$results` keeps the null-means-failure contract of `Invoke-GhsaQuery` intact; `@(Invoke-GhsaQuery)` at call sites cannot. Range fix is an explicit `"0"` check rather than deleting the special case and relying on `Compare-SemVer`'s "unparseable → 0" fallback, which would hide the intent.

**Verification:** `PATH="$SP/pwsh:$PATH" python3 -m unittest discover -s tests -p "test_*.py" -k VulnLookup` → 7 tests OK. Regression guards inside `test_osv_range_matrix`: `introduced 0 + fixed 0.2.1` vs `1.2.6` stays False; `introduced 1.0.0` vs `0.9.0` stays False.

**If this fails:** `git -C <work-root> checkout -- scripts/vuln-lookup.ps1 scripts/vuln-lookup.py`; re-apply hunk by hunk.

---

### Step 3: `registry-lookup.ps1` — B5 unrolling

**Objective:** `maintainers` / `installScripts` always arrays in `.ps1`.
**Confidence:** High
**Depends on:** Step 1
**Do-Projex:** Encouraged

**Files:**
- `scripts/registry-lookup.ps1`
- `scripts/registry-lookup.py` (docstring only)

**Changes:**

`scripts/registry-lookup.ps1` — `Lookup-Npm`:
```powershell
// Before:
    # Maintainers
    $maintainers = @($pkg.maintainers | ForEach-Object { $_.name }) | Where-Object { $_ }

// After:
    # Maintainers. The filter sits inside @(): piping @(...) on to Where-Object unrolls a
    # single maintainer to a bare string.
    $maintainers = @($pkg.maintainers | ForEach-Object { $_.name } | Where-Object { $_ })
```
```powershell
// Before:
        installScripts   = if ($installScripts.Count -gt 0) { $installScripts } else { $null }

// After:
        # `if` used as a value unrolls its output; the leading comma keeps a lone hook a 1-element array.
        installScripts   = if ($installScripts.Count -gt 0) { ,$installScripts } else { $null }
```

`scripts/registry-lookup.ps1` — `Lookup-Pypi`:
```powershell
// Before:
    # Maintainers
    $maintainers = @($info.author, $info.maintainer) | Where-Object { $_ }

// After:
    # Maintainers (filter inside @(), as in Lookup-Npm)
    $maintainers = @(@($info.author, $info.maintainer) | Where-Object { $_ })
```

`scripts/registry-lookup.py` — module docstring:
```python
# Before:
Python twin of registry-lookup.ps1: same flags, same JSON keys. Change both together.
Intentional divergences from the .ps1: arrays are always emitted as arrays (the
.ps1 collapses one-element results to scalars); dates are computed in UTC.

# After:
Python twin of registry-lookup.ps1: same flags, same JSON keys. Change both together.
Intentional divergence from the .ps1: dates are computed in UTC.
```

**Rationale:** Minimal wraps at the 3 unrolling sites found. Other arrays in the file (`$deps`, `$checks`) are already `@()`-assigned variables and serialize correctly. `maintainerCount` was already right (`"solo".Count` = 1).

**Verification:** `PATH="$SP/pwsh:$PATH" python3 -m unittest discover -s tests -p "test_*.py" -k RegistryLookup` → 2 OK.

**If this fails:** `git -C <work-root> checkout -- scripts/registry-lookup.ps1 scripts/registry-lookup.py`.

---

### Step 4: Bundled npm baseline — generator + data file

**Objective:** Real, download-ranked, unscoped top-1000 npm list, regenerable.
**Confidence:** Medium (data source is live and volatile; generator verified at planning: 61 s, 1000 rows, ranks semver 1 | chalk 13 | react 83 | lodash 104 | express 136 | prettier 144 | cross-env 701)
**Depends on:** None (independent of Steps 2–3)
**Verify-Projex:** Encouraged

**Files:**
- `scripts/data/refresh-npm-popular.py` (new)
- `scripts/data/npm-popular.tsv` (new, generated)

**Changes:** create `scripts/data/refresh-npm-popular.py` verbatim:
```python
#!/usr/bin/env python3
"""Regenerate npm-popular.tsv, the bundled popular-package baseline of typosquat-check.

Maintainer tool: the skill never runs it, so it has no .ps1 twin. Needs registry.npmjs.org.
Candidates: npm search results for SEED_TERMS (two pages of 250 each) plus MUST_INCLUDE
(each resolved by an exact-name search). Scoped names are dropped (typosquat-check
compares unscoped basenames; generic scoped basenames such as core or cli would collide
with unrelated names). Ranked by the search API's downloads.weekly, highest first; the
top --count rows are written. The search API is used instead of
api.npmjs.org/downloads because one search page returns 250 weekly counts.

Usage: python3 scripts/data/refresh-npm-popular.py [--count 1000]
"""
import argparse
import datetime
import json
import os
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "npm-popular.tsv")
SEARCH = "https://registry.npmjs.org/-/v1/search?size=%d&from=%d&text=%s"

SEED_TERMS = [
    "react", "vue", "angular", "svelte", "next", "webpack", "vite", "rollup", "esbuild", "babel",
    "eslint", "prettier", "typescript", "types", "jest", "mocha", "test", "lint", "cli", "util",
    "utils", "string", "array", "object", "file", "fs", "path", "stream", "color", "ansi",
    "parse", "json", "yaml", "node", "http", "request", "fetch", "server", "express", "middleware",
    "promise", "async", "date", "time", "crypto", "hash", "buffer", "url", "glob", "lodash",
    "config", "env", "debug", "log", "core", "plugin", "loader", "postcss", "css", "aws",
    "google", "graphql", "database", "sql", "redis", "auth", "jwt", "uuid", "semver", "terminal",
]

MUST_INCLUDE = [
    "express", "lodash", "react", "react-dom", "chalk", "debug", "commander", "yargs", "semver",
    "uuid", "axios", "moment", "dayjs", "date-fns", "cross-env", "dotenv", "prettier", "eslint",
    "typescript", "webpack", "vite", "rollup", "esbuild", "jest", "mocha", "chai", "sinon",
    "request", "node-fetch", "cors", "body-parser", "cookie-parser", "morgan", "helmet",
    "jsonwebtoken", "bcrypt", "bcryptjs", "mongoose", "mysql", "mysql2", "pg", "redis", "ioredis",
    "socket.io", "ws", "minimist", "mkdirp", "rimraf", "glob", "fs-extra", "async", "bluebird",
    "underscore", "colors", "classnames", "prop-types", "react-router", "react-router-dom",
    "redux", "react-redux", "vue", "next", "nuxt", "electron", "tslib", "core-js", "zod", "rxjs",
    "nodemon", "concurrently", "husky", "lint-staged", "inquirer", "ora", "nanoid", "qs", "ms",
    "ua-parser-js", "rc",
]


def search(text, size, frm=0):
    url = SEARCH % (size, frm, urllib.parse.quote(text, safe=""))
    req = urllib.request.Request(url, headers={"User-Agent": "install-auditor/1.0"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.load(resp).get("objects") or []
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2 * (attempt + 1))
    return []


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--count", type=int, default=1000)
    args = p.parse_args(argv)

    weekly = {}

    def add(objs, only=None):
        for o in objs:
            name = (o.get("package") or {}).get("name")
            if not name or name.startswith("@") or (only and name != only):
                continue
            w = int((o.get("downloads") or {}).get("weekly") or 0)
            weekly[name] = max(w, weekly.get(name, 0))

    for term in SEED_TERMS:
        for frm in (0, 250):
            add(search(term, 250, frm))
    missing = []
    for name in dict.fromkeys(MUST_INCLUDE):
        before = name in weekly
        add(search(name, 20), only=name)
        if name not in weekly and not before:
            missing.append(name)

    ranked = sorted(weekly.items(), key=lambda kv: (-kv[1], kv[0]))[:args.count]
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("# npm popular-package baseline for typosquat-check.ps1 / typosquat-check.py\n")
        f.write("# Unscoped npm packages ranked by weekly downloads (registry.npmjs.org/-/v1/search downloads.weekly).\n")
        f.write("# Snapshot: %s. Regenerate: python3 scripts/data/refresh-npm-popular.py\n" % datetime.date.today().isoformat())
        f.write("# Format: <name><TAB><weekly downloads>, highest first.\n")
        for name, w in ranked:
            f.write("%s\t%d\n" % (name, w))
    print("wrote %d rows to %s; must-include not found: %s" % (len(ranked), OUT, missing or "none"), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```
Then run: `python3 -B scripts/data/refresh-npm-popular.py` (writes `scripts/data/npm-popular.tsv`, prints the must-include names not found to stderr. At planning, `request` and `left-pad` were not found; `left-pad` has since been dropped from the list. A few misses are acceptable).

**Rationale:**
- Bundled list over live search: search has no popularity ordering any more, and typo queries don't surface their targets (`expresss` ↛ `express`), so the runtime gets no live dependency.
- Unscoped only: generic scoped basenames (`@babel/core` → `core`, `@types/node` → `node`) would put popular-looking tokens next to unrelated names (e.g. `cors` at distance 1 from `core`).
- Search counts over api.npmjs.org: the downloads API takes one name per call (bulk excludes scoped names), while a search page returns 250 weekly counts.
- Maintainer tool with no `.ps1` twin: the skill never runs it.

**Verification:** `python3 -m unittest discover -s tests -p "test_*.py" -k BundledBaseline` → OK. `head -5 scripts/data/npm-popular.tsv` shows the 4 `#` header lines, then the top row. `wc -l` ≈ 1004.

**If this fails:** Network error → rerun (3 retries per request built in). Fewer than 1000 rows → add seed terms to `SEED_TERMS` (log which) and rerun. Must-include names missing beyond `request` → still OK if the `BundledBaseline` assertions pass. Revert: delete `scripts/data/`.

---

### Step 5: `typosquat-check` twins — bundled baseline, known-popular rule, existence check (B1, B2)

**Objective:** Load `data/npm-popular.tsv`; never score a baseline member against its peers; report existence from the registry, not the downloads API.
**Confidence:** High (prototype parity: identical JSON from both twins on 5 cases, live and offline)
**Depends on:** Steps 1, 4
**Verify-Projex:** Encouraged

**Files:**
- `scripts/typosquat-check.py`
- `scripts/typosquat-check.ps1`

**Changes — `scripts/typosquat-check.py`:**

Docstring:
```python
# Before:
Fetches a popular-package baseline from the npm search API, computes Levenshtein
edit distance between the queried name and popular packages, detects combosquat
patterns (prefix/suffix overlap), compares download counts and emits a structured
JSON risk assessment to stdout. npm only.

Python twin of typosquat-check.ps1: same flags, same JSON keys. Change both together.
Intentional divergences from the .ps1: arrays are always emitted as arrays (the
.ps1 collapses one-element results to scalars and empty ones to null).

# After:
Loads the bundled popular-package baseline (data/npm-popular.tsv: unscoped npm
packages ranked by weekly downloads), computes Levenshtein edit distance between
the queried name and baseline packages, detects combosquat patterns (prefix/suffix
overlap), compares live download counts and emits a structured JSON risk
assessment to stdout. A queried name that is itself in the baseline is reported
low risk. npm only. Refresh the baseline with data/refresh-npm-popular.py.

Python twin of typosquat-check.ps1: same flags, same JSON keys. Change both together.
```
(The divergence sentence was already false for this script: pwsh run at planning showed the `.ps1` emitting lists for `closestMatches`/`combosquatHints`.)

Imports + constant:
```python
# Before:
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
…
CACHE_DIR = ".typosquat-cache"

# After:
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
…
BASELINE_PATH = os.path.join(SCRIPT_DIR, "data", "npm-popular.tsv")
```
Delete functions `cache_path`, `read_cache`, `write_cache` (only the baseline used them).

Replace `get_npm_popular_baseline` entirely:
```python
def get_npm_popular_baseline(size):
    """Return the first `size` rows of the bundled baseline as [{name, downloads}]; [] if unreadable."""
    baseline = []
    try:
        with open(BASELINE_PATH, encoding="utf-8-sig") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                name, _, weekly = line.partition("\t")
                weekly = weekly.strip()
                baseline.append({"name": name.strip(), "downloads": int(weekly) if weekly.isdigit() else 0})
    except OSError:
        return []
    return baseline[:max(size, 0)]
```

Insert after `get_npm_weekly_downloads`, and change the analysis signature + baseline lines:
```python
# Before:
def invoke_typosquat_analysis(ecosystem, name, compare_to, size, cache_hours, no_cache):
    normalized_name = get_comparison_token(name)

    baseline = get_npm_popular_baseline(size, cache_hours, no_cache) or []

# After:
def npm_package_exists(package_name):
    """True if the registry has the package, False on HTTP 404, None when the registry is unreachable."""
    req = urllib.request.Request("https://registry.npmjs.org/" + urllib.parse.quote(package_name, safe=""),
                                 method="HEAD", headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=15):
            return True
    except urllib.error.HTTPError as e:
        return False if e.code == 404 else None
    except Exception:
        return None


def invoke_typosquat_analysis(ecosystem, name, compare_to, size):
    normalized_name = get_comparison_token(name)

    baseline = get_npm_popular_baseline(size)
    # Exact raw-name match, not the normalized token: "@evil/chalk" normalizes to "chalk"
    # but is not the baseline package.
    known_popular = any(_ieq(b.get("name"), name) for b in baseline)
```

Download-ratio guard:
```python
# Before:
    if best_compare:
        queried_dl = weekly(name)

# After:
    if best_compare and not known_popular:
        queried_dl = weekly(name)
```

Existence + details (replaces the block from `queried_exists = …` through the existence note; the trailing `if combosquat_hints:` details line stays):
```python
# Before:
    queried_exists = weekly(name) is not None

    if risk_reasons:
        details = "Risk factors: %s. " % "; ".join(risk_reasons)
    else:
        details = "No close matches found in top-%s popular packages. " % size
    if not queried_exists:
        details += "Note: '%s' does not appear to exist on npm (0 download data). " % name

# After:
    if known_popular:
        # Baseline members sit within edit distance 2 of each other (chalk/chai, react/redux)
        # and prefix each other (react/react-dom); scoring them would flag every popular package.
        risk_level = "low"
        risk_reasons = []
        combosquat_hints = []

    queried_exists = True if known_popular else npm_package_exists(name)

    if known_popular:
        details = "'%s' is in the bundled top-%d popular npm package baseline; distance and combosquat signals are not scored. " % (name, len(baseline))
    elif risk_reasons:
        details = "Risk factors: %s. " % "; ".join(risk_reasons)
    else:
        details = "No close matches found in top-%d popular packages. " % len(baseline)
    if not baseline:
        details += "Popular-package baseline (data/npm-popular.tsv) missing or unreadable; only -CompareTo was checked. "
    if queried_exists is False:
        details += "Note: '%s' does not exist on npm (registry returned 404). " % name
    elif queried_exists is None:
        details += "Note: could not confirm '%s' exists on npm (registry unreachable). " % name
```

Parser + main:
```python
# Before:
    p.add_argument("-Size", "--size", dest="size", type=int, default=250,
                   help="number of popular packages to fetch as baseline (default: 250)")
    p.add_argument("-CacheHours", "--cache-hours", dest="cache_hours", type=int, default=24,
                   help="hours to cache the popular-package baseline (default: 24)")
    p.add_argument("-NoCache", "--no-cache", dest="no_cache", action="store_true",
                   help="skip cache reads; always fetch a fresh baseline")
…
        result = invoke_typosquat_analysis(args.ecosystem, args.name, args.compare_to, args.size,
                                           args.cache_hours, args.no_cache)

# After:
    p.add_argument("-Size", "--size", dest="size", type=int, default=1000,
                   help="number of baseline packages to use, from the top of data/npm-popular.tsv (default: 1000)")
    p.add_argument("-CacheHours", "--cache-hours", dest="cache_hours", type=int, default=24,
                   help="ignored; accepted so existing invocations keep working (the baseline is a bundled file)")
    p.add_argument("-NoCache", "--no-cache", dest="no_cache", action="store_true",
                   help="ignored; accepted so existing invocations keep working (the baseline is a bundled file)")
…
        result = invoke_typosquat_analysis(args.ecosystem, args.name, args.compare_to, args.size)
```

**Changes — `scripts/typosquat-check.ps1`:**

Help block:
```powershell
// Before:
    Fetches a popular-package baseline from the npm search API, computes
    Levenshtein edit distance between the queried name and popular packages,
    detects combosquat patterns (prefix/suffix overlap), compares download
    counts, and emits a structured JSON risk assessment to stdout.
…
.PARAMETER Size
    Number of popular packages to fetch from the search API baseline.
    Default: 250.

.PARAMETER CacheHours
    Hours to cache the popular-package baseline. Default: 24.

.PARAMETER NoCache
    Skip cache — always fetch fresh baseline from the API.

// After:
    Loads the bundled popular-package baseline (data/npm-popular.tsv: unscoped
    npm packages ranked by weekly downloads), computes Levenshtein edit distance
    between the queried name and baseline packages, detects combosquat patterns
    (prefix/suffix overlap), compares live download counts, and emits a
    structured JSON risk assessment to stdout. A queried name that is itself in
    the baseline is reported low risk. Refresh the baseline with
    data/refresh-npm-popular.py.
…
.PARAMETER Size
    Number of baseline packages to use, from the top of data/npm-popular.tsv.
    Default: 1000.

.PARAMETER CacheHours
    Ignored. Accepted so existing invocations keep working (the baseline is a bundled file).

.PARAMETER NoCache
    Ignored. Accepted so existing invocations keep working (the baseline is a bundled file).
```
Param default: `[int]$Size = 250,` → `[int]$Size = 1000,`.

Delete the whole `# ─── Cache ───…` section (`Get-CachePath`, `Get-CachedBaseline`, `Set-CachedBaseline`) up to the `# ─── npm Baseline Fetch` banner (banner stays; the banners are pre-existing file structure).

Replace `Get-NpmPopularBaseline` entirely:
```powershell
function Get-NpmPopularBaseline {
    # Returns the first $Size rows of the bundled baseline as @{ name; downloads }; empty if unreadable.
    # The leading comma keeps a 0- or 1-row result an array instead of letting the pipeline unroll it.
    $path = Join-Path (Join-Path $PSScriptRoot 'data') 'npm-popular.tsv'
    if (-not (Test-Path $path)) { return ,@() }
    $rows = foreach ($line in (Get-Content -Path $path -Encoding UTF8)) {
        $t = $line.Trim()
        if (-not $t -or $t.StartsWith('#')) { continue }
        $f = $t -split "`t", 2
        $dl = [long]0
        if ($f.Count -gt 1) { [void][long]::TryParse($f[1].Trim(), [ref]$dl) }
        @{ name = $f[0].Trim(); downloads = $dl }
    }
    return ,@($rows | Select-Object -First ([math]::Max($Size, 0)))
}
```

Insert after `Get-NpmWeeklyDownloads` (before `# ─── Core Analysis`):
```powershell
function Test-NpmPackageExists {
    # $true if the registry has the package, $false on HTTP 404, $null when the registry is unreachable.
    param([string]$PackageName)
    $encoded = [Uri]::EscapeDataString($PackageName)
    try {
        Invoke-WebRequest -Uri "https://registry.npmjs.org/$encoded" -Method Head -UseBasicParsing `
            -Headers @{ 'User-Agent' = 'install-auditor/1.0' } -TimeoutSec 15 | Out-Null
        return $true
    } catch {
        $status = $null
        if ($_.Exception.Response) { $status = [int]$_.Exception.Response.StatusCode }
        if ($status -eq 404) { return $false }
        return $null
    }
}
```

In `Invoke-TyposquatAnalysis`, after the `if (-not $baseline -or $baseline.Count -eq 0) { … $baseline = @() }` block:
```powershell
    # Exact raw-name match, not the normalized token: "@evil/chalk" normalizes to "chalk"
    # but is not the baseline package.
    $knownPopular = $false
    foreach ($b in $baseline) {
        if ($b.name -eq $Name) { $knownPopular = $true; break }
    }
```
Ratio guard: `    if ($bestCompare) {` → `    if ($bestCompare -and -not $knownPopular) {`.

Existence + details:
```powershell
// Before:
    # Package existence check: if queried name does not resolve on npm, note it
    $queriedExists = $null -ne (Get-NpmWeeklyDownloads $Name)

    # Build human-readable summary
    $details = if ($riskReasons.Count -gt 0) {
        "Risk factors: $($riskReasons -join '; '). "
    } else {
        "No close matches found in top-$Size popular packages. "
    }
    if (-not $queriedExists) {
        $details += "Note: '$Name' does not appear to exist on npm (0 download data). "
    }

// After:
    if ($knownPopular) {
        # Baseline members sit within edit distance 2 of each other (chalk/chai, react/redux)
        # and prefix each other (react/react-dom); scoring them would flag every popular package.
        $riskLevel       = 'low'
        $riskReasons     = @()
        $combosquatHints = @()
    }

    $queriedExists = if ($knownPopular) { $true } else { Test-NpmPackageExists $Name }

    # Build human-readable summary
    $details = if ($knownPopular) {
        "'$Name' is in the bundled top-$($baseline.Count) popular npm package baseline; distance and combosquat signals are not scored. "
    } elseif ($riskReasons.Count -gt 0) {
        "Risk factors: $($riskReasons -join '; '). "
    } else {
        "No close matches found in top-$($baseline.Count) popular packages. "
    }
    if ($baseline.Count -eq 0) {
        $details += "Popular-package baseline (data/npm-popular.tsv) missing or unreadable; only -CompareTo was checked. "
    }
    if ($queriedExists -eq $false) {
        $details += "Note: '$Name' does not exist on npm (registry returned 404). "
    } elseif ($null -eq $queriedExists) {
        $details += "Note: could not confirm '$Name' exists on npm (registry unreachable). "
    }
```

**Rationale:**
- Known-popular is an exact raw-name match, not a token match, so a scoped name never inherits a popular package's pass.
- The override comes after scoring, rather than skipping blocks, to keep the diff small in both twins. The ratio guard avoids 2 pointless downloads-API calls.
- HEAD existence check: a full packument GET can be MBs. The downloads API conflates "missing" with "unreachable".
- `downloads` now holds real snapshot ints in both twins, where the old `.ps1` emitted the float `10000000.0`.

**Verification:**
- `python3 -m unittest discover -s tests -p "test_*.py" -k Typosquat` (pwsh on PATH) → all OK, including `TyposquatParity.test_twins_agree`.
- Live checks (registry.npmjs.org reachable):
  ```bash
  for n in expresss chalk crossenv; do python3 -B scripts/typosquat-check.py -Ecosystem npm -Name $n; "$SP/pwsh/pwsh" -NoProfile -File scripts/typosquat-check.ps1 -Ecosystem npm -Name $n; done
  ```
  Expect: `expresss` → `high` (`critical` if api.npmjs.org reachable), `closestMatches[0]` = express/1. `chalk` → `low`, details `'chalk' is in the bundled top-1000…`. `crossenv` → `high`, closest `cross-env`. Py vs ps1 JSON equal per name. Then `ls -d scripts/.typosquat-cache` → absent.
- PS runtime: `expresss` ≤ ~3 s wall (planning: 1000-name Levenshtein 0.17 s short / 1.0 s long name). If > 10 s, set the default `-Size` to 500 in both twins + docs and log it.

**If this fails:** `git -C <work-root> checkout -- scripts/typosquat-check.ps1 scripts/typosquat-check.py`; re-apply per hunk. Parity diff → compare `details` strings first (most likely drift point).

---

### Step 6: Docs — typosquat interpretation + stewardship

**Objective:** Shipped docs describe the bundled baseline, known-popular rule, test command, and refresh duty.
**Confidence:** High
**Depends on:** Steps 4, 5
**Do-Projex:** Encouraged

**Files:**
- `references/criteria/registry-package.md`
- `STEWARDSHIP.md`

**Changes:**

`references/criteria/registry-package.md` § Typosquat Detection — after the paragraph ending `canonical package name to compare against.` insert:
```markdown
The baseline is a bundled snapshot of the 1,000 most-downloaded unscoped npm
packages (`scripts/data/npm-popular.tsv`; refresh with
`python3 scripts/data/refresh-npm-popular.py`). A queried name that is itself in
the baseline is reported `low` without distance or combosquat scoring. Scoped
names are compared by unscoped basename only -- verify scope ownership manually
(see below).
```
Same section, table row:
```markdown
// Before:
| `closestMatches` | Top packages by edit distance, with distance and download counts |
// After:
| `closestMatches` | Top packages by edit distance, with distance and weekly downloads (baseline snapshot; the best match gets the live count when the npm downloads API answers) |
```

`STEWARDSHIP.md` § Running Evals — after the paragraph ending `Self-test: \`python3 -m unittest discover -s evals -p "test_*.py"\`.` insert a new paragraph:
```markdown
Lookup-script tests: `python3 -m unittest discover -s tests -p "test_*.py"` (offline fixtures; the `.ps1` twin tests run only when `pwsh` is on PATH, otherwise they are skipped). The npm typosquat baseline `scripts/data/npm-popular.tsv` is a dated snapshot: regenerate it with `python3 scripts/data/refresh-npm-popular.py` (needs registry.npmjs.org) during each scheduled registry-package review and commit the diff.
```

**Rationale:** Content anchors, not line numbers (python-ports walkthrough lesson). `SKILL.md` untouched: its Red Flag wording ("edit distance ≤2 from a top-1000 package", `riskLevel: critical`) already matches the new behavior.

**Verification:** `grep -n "npm-popular.tsv" references/criteria/registry-package.md STEWARDSHIP.md` → one hit per file (plus refresh command). `python3 evals/run_evals.py validate` → OK (no eval changes; harness sanity).

**If this fails:** `git -C <work-root> checkout -- references/criteria/registry-package.md STEWARDSHIP.md`.

---

## Verification Plan

> Per-step verification (above) confirms each change in isolation. This section confirms the changes work together end-to-end.

### Automated Checks
- [ ] `PATH="$SP/pwsh:$PATH" python3 -m unittest discover -s tests -p "test_*.py"` → `Ran 19 tests … OK` (no skips)
- [ ] `PATH=/usr/bin:/bin python3 -m unittest discover -s tests -p "test_*.py"` → `OK (skipped=6)`
- [ ] `python3 -m unittest discover -s evals -p "test_*.py"` → OK (unchanged harness)
- [ ] `python3 evals/run_evals.py validate` → OK
- [ ] `python3 -c "import ast,glob; [ast.parse(open(f).read(), feature_version=(3,8)) for f in glob.glob('scripts/*.py')+glob.glob('scripts/data/*.py')+['tests/test_lookup_scripts.py']]"` → no error
- [ ] `"$SP/pwsh/pwsh" -NoProfile -Command '$e=$null; foreach($f in Get-ChildItem scripts/*.ps1){ [void][System.Management.Automation.Language.Parser]::ParseFile($f.FullName,[ref]$null,[ref]$e); if($e){$f.Name; $e} }'` → no output
- [ ] `git -C <work-root> status --porcelain` → only intended files; no `__pycache__`, no `scripts/.*-cache`

### Manual Verification
- [ ] PS 5.1 static checklist over the diff of `scripts/*.ps1`: no `??` / `?.` / `? :` ternary / `-AsHashtable` / `-Parallel` / 3-arg `Join-Path` / `Get-Content -AsByteStream`; `Invoke-WebRequest` carries `-UseBasicParsing`; status read via `[int]$_.Exception.Response.StatusCode` (works for 5.1 `WebException` and 7.x `HttpResponseException`)
- [ ] Source Hygiene over the diff: no projex filenames in code comments; no line-number refs; every new comment present-tense
- [ ] Live typosquat checks from Step 5 recorded in the log (both twins)
- [ ] Optional, only if the orchestrator approves spend: `python3 evals/run_evals.py prepare --ids 3,4` → `run` → `grade` → `summary`

### Acceptance Criteria Validation
| Criterion | How to Verify | Expected Result |
|-----------|---------------|-----------------|
| Suite green both modes | unittest with / without pwsh | 19 OK / OK skipped=6 |
| Red on old scripts | Step 1 run | ≥ 11 failures, list logged |
| `expresss` flagged | Step 5 live run, both twins | `high`/`critical`, express @ distance 1 |
| `chalk` not flagged | Step 5 live run, both twins | `low`, known-popular details |
| Baseline data shape | `BundledBaseline` test | OK |
| B3 fixed | `test_osv_range_matrix`, `*_keeps_introduced_zero` | OK both impls |
| B4 fixed | `VulnLookupPowerShell.*` | OK |
| B5 fixed | `RegistryLookupPowerShell.*` | OK |
| No pycache leak | `git status --porcelain` after suites | clean apart from intended files |
| py3.8 / PS parse | ast + Parser checks | no errors |

---

## Rollback Plan

Per-step rollback is noted in each implementation step above. If the overall implementation must be abandoned:

1. `projex-abandon` the ephemeral branch with `--worktree` (all changes live only there).
2. Remove scratch pwsh: `rm -rf "$SP/pwsh" "$SP/pwsh-dl"` (outside the repo; nothing tracked).

---

## Notes

### Risks
- **Baseline staleness:** snapshot ages; new popular packages are unprotected until refresh. Mitigation: STEWARDSHIP refresh duty + `refresh-npm-popular.py`.
- **Search coverage gaps:** seed-term search can miss very popular names (planning: `semver`, `commander`, `uuid`, `cross-env`, `prettier` missing from seeds alone). Mitigation: `MUST_INCLUDE`. The `BundledBaseline` test asserts the key names.
- **More false positives for short names** (1000 candidates vs a near-empty effective baseline before): e.g. `axois` → `medium` (axios, distance 2). Intended behavior per rubric (medium = investigate). Popular names themselves are protected by the known-popular rule.
- **Known-popular trusts the snapshot:** a squat would need ~15 M weekly downloads to enter the top 1000 (planning cutoff 14.8 M). Acceptable.
- **`.ps1` only tested on pwsh 7.4:** 5.1 covered by static checklist. Mocks use PS 7 exception types (test-only).

### Follow-ups (not this plan)
- Scope-impersonation signal: scoped queried name whose basename equals a baseline name (`@evil/chalk`) currently gets no hint. Flagging every `@types/<popular>` would need an allowlist.
- Download fallback via search `downloads.weekly` when api.npmjs.org is blocked (would restore `critical` escalation in restricted networks).
- First host with OSV/GHSA access: live `vuln-lookup` lodash 4.17.20 / `dep-scan` mkdirp 0.5.1 (carried from parent walkthrough).

### Split Decision
`No split — heuristic tripped but steps tightly coupled (rationale: 1,258 lines / ~64 KB, mostly the verbatim test file (338 lines) and generator (103 lines); 6 steps share one test suite, one pwsh bootstrap and one scope (scripts/ + its tests/docs); Steps 2/3 are small and independent but splitting them would duplicate the suite/bootstrap across plans.)`

### Open Questions
- [x] none
