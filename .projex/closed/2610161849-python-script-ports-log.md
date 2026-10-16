# Execution Log: Python Ports of Lookup Scripts

> **Status:** Complete
> **Started:** 20261016 18:55
> **Repo Root:** /home/user/install-auditor-skill
> **Plan File:** .projex/2610161849-python-script-ports-plan.md
> **Parent:** 2610161849-python-script-ports-plan.md
> **Base Branch:** claude/youthful-dijkstra-5ov1kt
> **Worktree Path:** install-auditor-skill/.projexwt/2610161849-python-script-ports

## Pre-Check Results

```
REPO_ROOT=/home/user/install-auditor-skill
BRANCH=claude/youthful-dijkstra-5ov1kt
PLAN_REL=.projex/2610161849-python-script-ports-plan.md

PASS  Plan is committed (60420d7 projex: add plan - python-script-ports)
WARN  Working tree has 2 uncommitted change(s)

PRE-CHECK PASSED
```

WARN resolved/ignored: the uncommitted item is the untracked `.projex/2610161852-dispatcher-rubric-consistency-plan.md`, owned by a concurrent planner (orchestrator-confirmed, not mine). Plan status edit committed on base as b8922c1.

## Steps

### Setup: worktree + bootstrap
**Action:** Orchestrator override `Worktree: Yes` (plan header said `No`; header edited to `Yes` in the base-branch start commit b8922c1). `projex-worktree.sh` created branch `projex/2610161849-python-script-ports` at `.projexwt/2610161849-python-script-ports`. Bootstrap: none needed (stdlib-only Python; no deps).
**Result:** `python3 3.13.16`, `node`/`npm` present, `pwsh` absent.
**Status:** Success

### 20261016 19:05 - Step 1: Port registry-lookup
**Action:** Wrote `scripts/registry-lookup.py` (self-executed, mirrors `registry-lookup.ps1` function-by-function; `http_json`/`invoke_api` per Port Conventions). CLI: positional `ecosystem name [version]` + `-Ecosystem/-Name/-Version` (+ `--` aliases) via `parse_intermixed_args`; named wins, positionals fill unbound slots in order (PowerShell binding). `chmod +x`.
**Result:** Live runs OK: `npm lodash` (versionCount 117, maintainers list), `-Ecosystem npm -Name @types/node`, `pypi requests`, `crates serde` (ecosystem `crates.io`), `rubygems rails`, `nuget Newtonsoft.Json` (gzip handled; version populated), `npm lodash 4.17.21` honors version, `-Name requests PyPI` binds positional to Ecosystem case-insensitively. Not-found `npm this-pkg-does-not-exist-zz9` → exit 1, stderr `Package 'this-pkg-does-not-exist-zz9' not found on npm`, empty stdout. Bad ecosystem / missing name → exit 2. Key order per ecosystem matches the `.ps1` `[ordered]@{}` blocks. `ast.parse(feature_version=(3,8))` OK. Network note: weeklyDownloads/monthlyDownloads/openssf blocked by proxy as expected (null/absent). Self-verified (no verify-projex for this step; plan marks it Encouraged only for Steps 3-4).
**Status:** Success

### 20261016 19:20 - Step 2: Port typosquat-check
**Action:** Wrote `scripts/typosquat-check.py` (self-executed): flags `-Ecosystem/-Name/-CompareTo/-Size/-CacheHours/-NoCache` + kebab aliases; baseline query URL kept verbatim (known-broken upstream, out of scope); cache write happens even with `-NoCache` (as `.ps1`: only the read is skipped); per-name download lookups memoized within one analysis (equivalent output, avoids the `.ps1`'s duplicate call for `queriedExists`). Wrote throwaway harness in the session scratchpad (outside repo).
**Result:** Harness §A + §B typosquat: `lev("expresss","express")==1`, `("lodahs","lodash")==2`, `("","abc")==3`, `token("@Scope/Foo__Bar")=="foo-bar"`; fixture `expresss` vs baseline [express, lodash] with exact-suffix download routing → `closestMatches[0].name=="express"`, `downloadRatio.ratio==-1`, `riskLevel=="critical"`, `combosquatHints==["express"]`, output key order matches `.ps1`; error path → `{ecosystem, queriedName, error, riskLevel:"unknown"}` exit 0; API failure + `-CompareTo` → `[lodash, distance 2]`, risk `high`. Live `-Ecosystem npm -Name expresss -CompareTo express -NoCache` → `closestMatches[0]=={name:express,distance:1,downloads:0}`, `riskLevel:"high"`, `downloadRatio:null` (downloads API blocked by proxy; plan expected `high|critical`). Removed `scripts/.typosquat-cache` created by the live run.
**Status:** Success

### 20261016 19:40 - Step 3: Port vuln-lookup
**Action:** Wrote `scripts/vuln-lookup.py` (self-executed): `normalize_severity`, `get_severity_from_osv`, `_to_sysver`/`compare_semver` (plan snippet; `\d` tightened to `[0-9]` so non-ASCII digits are not treated as version parts), `test_osv_version_affected`, `test_ghsa_version_affected`, `invoke_osv_query`, `invoke_ghsa_query`, `get_discrepancies` (CVE keys case-insensitive like PS hashtables, original spelling emitted), `get_risk_level`, cache + main exactly per spec. Extended the scratchpad harness with a `vuln` suite.
**Result:** Harness §A all asserts pass (compare_semver 6 cases, OSV range 4 cases, GHSA 3 cases, severity 3 + extra). §B fixtures pass: minimist 0.0.8 with OSV+GHSA → `osvResults` list len 1, `summary == {totalCount:2, osvCount:1, ghsaCount:1, highestSeverity:"medium"}`, `discrepancies == {onlyInOsv:[], onlyInGhsa:[]}`, `sources == ["OSV","GHSA"]`, key order ends `riskLevel, version`; cache round-trip makes zero network calls; version 1.2.6 filtered out → riskLevel `none`; GHSA failing → `sources == ["OSV"]`, `ghsaResults == []`, `ghsaNote` (em dash verbatim), key tail `version, ghsaNote`; OSV failing → `{ecosystem, package, error, riskLevel:"unknown"}` exit 0 and not cached; `GITHUB_TOKEN` → `Authorization: Bearer` header. Live `-Ecosystem npm -Name lodash -Version 4.17.20` → error JSON (`<urlopen error Tunnel connection failed: 403 Forbidden>`, OSV blocked by proxy), `riskLevel:"unknown"`, exit 0, as the plan predicts. `ast.parse(feature_version=(3,8))` OK. Removed empty `scripts/.vuln-cache` dir. Verify-projex sub-subagent not used (no subagent tool in this session); self-verified by line-by-line read against `.ps1`.
**Status:** Success

### 20261016 20:05 - Step 4: Port dep-scan
**Action:** Wrote `scripts/dep-scan.py` (self-executed): severity helpers copied from Step 3 (standalone), `get_npm_deps` (raw name in URL), `get_pypi_deps` (extras/marker/specifier stripping), `get_npm_full_tree` (`shutil.which("npm")`, version check, fresh `tempfile.mkdtemp()` always `rmtree`d, flags exactly `install --package-lock-only --ignore-scripts --silent`, `timeout=300` mapped to a descriptive `RuntimeError`), `invoke_osv_batch` (1000/batch, per-batch stub enrichment cache), `get_dep_findings`, main with cache/tier/fallback/limitation semantics per spec. Direct-name set for depth is lower-cased (PS hashtable keys are case-insensitive). Extended scratchpad harness with a `depscan` suite incl. a fake `npm` script (scratchpad) that records argv/cwd and writes a v3 lockfile.
**Result:** Harness: pypi requirement parsing → `["urllib3","idna","certifi"]`; `npm mkdirp 0.5.1 -Tier 2` fixture → findings `[{name:"minimist", ecosystem:"npm", version:"0.0.8", severity:"high", cveIds:["CVE-2020-7598"], depth:1}]`, `riskLevel:"high"`, `directDepCount:1`, `cacheHit:false`, enrichment URL called exactly once, querybatch body shape correct, key order matches `.ps1`; second run served from cache with `cacheHit:true` and zero network; Tier 3 with `which`→None → `fallback:true`, `fallbackReason:"npm CLI unavailable"`, `tier:2`; `crates serde` → `limitationNote`, `directDepCount:0`, `riskLevel:"none"`; Tier 3 non-npm → exact PS fallback reason; exception → exact error shape; Tier 3 success with fake npm → `tier:3`, `transitiveDepCount:3` (root `""` and version-less link entries skipped, nested `@sc/b` name extracted), invoked as `install --package-lock-only --ignore-scripts --silent` in a temp dir that no longer exists afterwards (also after a failing npm: `fallbackReason:"npm install --package-lock-only failed (exit 7)"`). Live: `chalk 5.3.0 -Tier 2` → `directDepCount:0`, `riskLevel:"none"`, `findings:[]`; rerun → `cacheHit: true`. Live `mkdirp 0.5.1 -Tier 3` → real npm 10.9 resolved the lockfile (no fallback), then OSV 403 → error JSON `<urlopen error Tunnel connection failed: 403 Forbidden>` as the plan predicts; no leftover temp dir with a `package.json` in `/tmp`. Removed `scripts/.dep-scan-cache`. `ast.parse(feature_version=(3,8))` OK. No verify-projex sub-subagent (no subagent tool available); self-verified line-by-line against `.ps1`.
**Status:** Success

### 20261016 20:25 - Step 5: Switch doc call sites to Python-first
**Action:** `SKILL.md`: Edit on line 87 (lookup-scripts wording) and line 241 (Reference Files bullet, text verbatim from plan). `references/criteria.md`: L9 (`.py` + twin sentence), L39/L159 (stem), L63/L151/L157 (`.py`). `references/criteria/registry-package.md` and `workflows/registry-package.md`: regex pass (`.\scripts\X.ps1` → `python3 scripts/X.py`; `scripts/X.ps1` → `scripts/X.py`; remaining `X.ps1` prose → stem; `init.ps1`/`install.ps1` untouched), then manual inserts: twin note (verbatim) + blank line after the first invocation fence in each file, `(.ps1 twin)` mention on the workflow Script-coverage note, and the `GITHUB_TOKEN` shell-syntax sentence.
**Result:** `git diff -U0 SKILL.md` hunks at 87 and 241 only (`2 insertions, 2 deletions`). `grep -n '\.ps1'` residue is exactly the allowed set: `SKILL.md:156` (deferred), `SKILL.md:241` (twin sentence), `criteria.md:9` (twin sentence), `criteria/registry-package.md:134` (NuGet `init.ps1`/`install.ps1`) and `:166` (twin note), `workflows/registry-package.md:52` (twin mention), `:99` (twin note), `:259` (NuGet `init.ps1`). `grep -c 'python3 scripts/'` → workflows 6, criteria/registry-package 4, SKILL.md 1. Diff read in full: all code fences intact, twin notes are blockquotes with surrounding blank lines. Plan cites some doc line numbers (e.g. workflows `L257`, `L52`) that are 2 lines off after the inserted note; edits were matched by content, not number.
**Status:** Success

### 20261016 20:35 - Completion: full verification and reviews
**Action:** Ran every Automated Check and the three harness suites together; spec-compliance and quality review of the 4 new scripts and 4 doc diffs; cleanup.
**Result:**
- `ast.parse(..., feature_version=(3,8))` on all four `scripts/*.py` OK; `--help` exits 0 for all four; imports are stdlib only (`argparse datetime gzip json math os re shutil subprocess sys tempfile time urllib`); all four start with `#!/usr/bin/env python3`; `git ls-files -s` shows mode `100755` for all four; harness `typosquat vuln depscan` → `OK 66 asserts`.
- Flag parity: `-Ecosystem -Name -Version -Tier -CompareTo -Size -CacheHours -NoCache` + `--kebab` aliases present on the matching scripts; registry-lookup also takes positional `<eco> <name> [version]`.
- JSON contract: key sets/order per `.ps1` `[ordered]@{}` blocks asserted for typosquat, vuln-lookup, dep-scan (success + fallback + error paths); registry-lookup key order compared by reading against the `.ps1` and via live runs.
- Doc criteria: residue grep and counts 6/4/1 as listed in Step 5; `SKILL.md` touched at lines 87 and 241 only; no edits to `.ps1`, `evals/`, `.gitignore` (`git diff --stat` against base lists only the 4 new scripts, 4 docs, plan, log).
- Live matrix: reachable registries returned populated JSON for all five ecosystems; unreachable hosts (api.osv.dev, api.npmjs.org, pypistats.org, api.securityscorecards.dev) behaved as the plan predicts (null download fields, absent `openssf`, OSV error JSON). `api.github.com/advisories` not exercised live (OSV is queried first and fails first); GHSA success path verified with fixtures only. First host with OSV access should run: `vuln-lookup.py -Ecosystem npm -Name lodash -Version 4.17.20` (expect CVE-2021-23337) and `dep-scan.py -Ecosystem npm -Name mkdirp -Version 0.5.1 -Tier 2` (expect minimist HIGH).
- Quality review: no projex references, banners, or line numbers in the `.py` sources; rationale comments name the rejected alternative (gzip handling, `-1` for infinity, `[0-9]` vs `\d`, no `npm ci`). No dead code found.
- Cleanup: removed `scripts/.typosquat-cache`, `.vuln-cache`, `.dep-scan-cache` after each live run; no `__pycache__` (all runs used `-B`); harness and fake npm live in the session scratchpad outside the repo; `git status --porcelain` clean before the completion commit.
**Status:** Success

## Deviations

- Plan header `Worktree: No` → `Yes` per orchestrator override (concurrent plans share the main checkout). Edited in the base-branch start commit.
- Do-Projex / Verify-Projex (both only "Encouraged") not used: no subagent tool was available in this session. All steps self-executed and self-verified (Step 3 and 4 by line-by-line comparison with the `.ps1` plus fixture asserts).
- typosquat-check: per-name weekly-download lookups are memoized within one run (the `.ps1` fetches the queried name's downloads twice). Output is identical; one fewer network call.
- dep-scan: Tier 3 `subprocess.TimeoutExpired` is converted to `RuntimeError("npm install --package-lock-only timed out after 300 s")` so `fallbackReason` is readable (the plan said the exception message would be used; the raw message embeds the argv list).
- vuln-lookup/dep-scan: `[0-9]` used in place of `\d` in `_SYSVER` and the CVSS-score regex (strict ASCII, like the PowerShell `[System.Version]` parse).

## Issues Encountered

- **Latent `.ps1` defect mirrored, not fixed (found at Step 3):** `Test-OsvVersionAffected` open-ended-range tail sets `$floor = -1` when `$introduced -eq '0'` and then requires `$floor -ge 0`, so an OSV range that is `introduced: "0"` with no `fixed`/`last_affected` (all versions affected) is reported NOT affected when `-Version` is supplied. This is anti-conservative (false negative), unlike the other quirks. Ported faithfully per plan ("line-for-line", "floor -1 in that branch only"); `test_osv_version_affected("1.0.0", [{type:SEMVER, events:[{introduced:"0"}]}], [])` returns False in both impls. Needs a separate patch touching both `.ps1` and `.py`.

- **Base advanced during execution (close-time conflict expected):** base `claude/youthful-dijkstra-5ov1kt` gained the dispatcher-rubric-consistency squash commit (5c44b79) while this branch was open. `git merge-tree` of base + this branch reports one content conflict in `SKILL.md`: base rewrote line 242 (taxonomy-def bullet → `references/classifier.md` bullet, now line 249) directly under this branch's line-241 Reference Files edit. Resolution at close: keep both, i.e. this branch's new script bullet followed by base's `references/classifier.md` bullet; base's other SKILL.md hunks do not overlap. `workflows/registry-package.md` auto-merges.

## Data Gathered

## User Interventions
