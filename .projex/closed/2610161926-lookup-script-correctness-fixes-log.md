# Execution Log: Lookup Script Correctness Fixes

> **Status:** Complete
> **Started:** 20261016 19:33
> **Repo Root:** /home/user/install-auditor-skill
> **Plan File:** .projex/2610161926-lookup-script-correctness-fixes-plan.md
> **Parent:** 2610161926-lookup-script-correctness-fixes-plan.md
> **Base Branch:** claude/youthful-dijkstra-5ov1kt
> **Worktree Path:** .projexwt/2610161926-lookup-script-correctness-fixes

## Pre-Check Results
```
PASS  Plan is committed (ec82069 projex: add plan - lookup-script-correctness-fixes; add eval - agent-extension stewardship review)
WARN  Working tree has 1 uncommitted change(s)
PRE-CHECK PASSED
```
WARN resolved: the one change is an untracked, unrelated eval doc (`.projex/2610161928-stewardship-review-container-cli-desktop-eval.md`) owned by another workflow; left untouched on base. Worktree mode keeps it out of this execution.

## Setup
- 20261016 19:33 Plan status set `In Progress`, committed on base (cf327c5).
- Ephemeral branch `projex/2610161926-lookup-script-correctness-fixes`, worktree `install-auditor-skill/.projexwt/2610161926-lookup-script-correctness-fixes`.
- Bootstrap: pwsh 7.4.6 linux-x64 official tarball downloaded (python urllib) into the session scratchpad (`pwsh-dl/`, `pwsh/`), outside the repo; `pwsh -NoProfile` reports 7.4.6. No in-repo deps needed (stdlib only).
- Task-list tool (TaskCreate) not available in this subagent environment; the plan steps are tracked through this log and per-step commits instead.

## Steps

### [20261016 19:38] - Step 1: Offline regression suite + .gitignore
**Action:** Wrote `tests/test_lookup_scripts.py` verbatim from the plan; added `__pycache__/` to `.gitignore`. Red run: `PATH=$SP/pwsh:$PATH python3 -B -m unittest discover -s tests -p "test_*.py"` against the unfixed scripts. Deleted the `scripts/.typosquat-cache/` the red run created (old code does live npm search).
**Result:** `FAILED (failures=11, errors=3)`, 19 run, 14 red (plan floor: >= 11; plan estimated 13 — the extra red is `TyposquatPython.test_legacy_cache_flags_accepted`, which also fails on the old baseline logic). pwsh tests actually executed (pwsh 7.4.6). Red list:
- ERROR `BundledBaseline.test_bundled_file_shape` (file absent until Step 4)
- ERROR `TyposquatPython.test_separator_typo_is_high`
- ERROR `VulnLookupPowerShell.test_version_filter_keeps_introduced_zero`
- FAIL `RegistryLookupPowerShell.test_single_entries_are_arrays`
- FAIL `TyposquatParity.test_twins_agree`
- FAIL `TyposquatPython`: `test_existence_notes`, `test_known_popular_packages_are_low`, `test_legacy_cache_flags_accepted`, `test_missing_baseline_still_checks_compare_to`, `test_typo_of_popular_package_is_high`
- FAIL `VulnLookupPowerShell`: `test_single_hit_is_an_array`, `test_zero_hits_and_empty_ghsa_success`
- FAIL `VulnLookupPython`: `test_osv_range_matrix`, `test_version_filter_keeps_introduced_zero`
Green on old code (as expected): `VulnLookupPowerShell.test_ghsa_failure_is_reported`, `VulnLookupPython.test_ghsa_failure_is_reported`, `RegistryLookupPython.test_single_entries_are_arrays`, `TyposquatPython.test_scoped_name_is_not_known_popular`, `TyposquatPython.test_size_limits_baseline`.
**Status:** Success

### [20261016 19:44] - Step 2: vuln-lookup B3 range fix (both) + B4 unrolling (.ps1)
**Action:** Applied plan hunks: `Test-OsvVersionAffected` / `test_osv_version_affected` open-ended tail; `return ,$results` x3 (`Invoke-OsvQuery` x2, `Invoke-GhsaQuery` success); `vuln-lookup.py` docstring divergence note removed.
**Result:** `PATH=$SP/pwsh:$PATH python3 -B -m unittest discover -s tests -p "test_*.py" -k VulnLookup` -> `Ran 7 tests ... OK` (the 4 `.ps1` tests ran under pwsh 7.4.6, not skipped). Self-verified via diff + tests; no verify-projex sub-subagent (marked Encouraged, depth budget unused).
**Status:** Success

### [20261016 19:47] - Step 3: registry-lookup.ps1 B5 unrolling
**Action:** `Lookup-Npm` maintainers filter moved inside `@()`; `installScripts = if (...) { ,$installScripts }`; `Lookup-Pypi` maintainers `@(@(...) | Where-Object ...)`; `registry-lookup.py` docstring reduced to the UTC-date divergence.
**Result:** `-k RegistryLookup` -> `Ran 2 tests ... OK` (the `.ps1` test executed under pwsh 7.4.6).
**Status:** Success

### [20261016 19:52] - Step 4: Bundled npm baseline generator + data
**Action:** Wrote `scripts/data/refresh-npm-popular.py` verbatim; ran `python3 -B scripts/data/refresh-npm-popular.py` against live registry.npmjs.org (75 s).
**Result:** `wrote 1000 rows ...; must-include not found: ['request']` (plan-anticipated miss). `npm-popular.tsv`: 1004 lines (4 `#` header lines + 1000 rows), top row `semver 877320600`. Ranks (1-based): chalk 13, react 83, lodash 104, express 136, prettier 144, cross-env 700 (plan: 701; snapshot drift). `-k BundledBaseline` -> OK. No stray caches or pycache.
**Status:** Success

### [20261016 20:01] - Step 5: typosquat-check twins (B1, B2)
**Action:** Applied all plan hunks to `scripts/typosquat-check.py` and `scripts/typosquat-check.ps1` via anchored exact-string replacement scripts (scratchpad, each `old` asserted to occur exactly once): docstring/help, imports (`math`, `time`, `datetime` dropped; no dangling refs, grep clean), `BASELINE_PATH`, cache functions deleted, `get_npm_popular_baseline`/`Get-NpmPopularBaseline` replaced, `npm_package_exists`/`Test-NpmPackageExists` added, `known_popular`/`$knownPopular` rule + ratio guard, existence/details block, `-Size` default 1000, `-CacheHours`/`-NoCache` kept as ignored.
**Result:**
- `-k Typosquat` -> `Ran 9 tests ... OK`, including `TyposquatParity.test_twins_agree` (the `.ps1` was executed under pwsh 7.4.6).
- Live (registry.npmjs.org reachable; api.npmjs.org NOT reachable through the proxy, so `downloadRatio` is `null` in all runs and `critical` escalation is not exercised live — plan anticipates this path):
  - `expresss`: py == ps1 JSON; `riskLevel: high`; `closestMatches[0]` = express / distance 1 / 145199376; details `Risk factors: Edit distance 1 from 'express'.`
  - `chalk`: py == ps1 JSON; `riskLevel: low`; details `'chalk' is in the bundled top-1000 popular npm package baseline; ...`. `closestMatches` still lists chai (distance 2) as informational, `combosquatHints` empty, as in the plan's known-popular design (override changes level/reasons/hints only).
  - `crossenv`: py == ps1 JSON; `riskLevel: high`; closest cross-env / distance 1.
- `ps1` wall time: expresss 2.55 s, chalk 1.45 s, crossenv 2.48 s (under the plan's 3 s / 10 s thresholds; `-Size` default stays 1000).
- `scripts/.typosquat-cache` absent after live runs; no pycache.
**Status:** Success

### [20261016 20:06] - Step 6: Docs
**Action:** Inserted the baseline paragraph after the `canonical package name to compare against.` paragraph and reworded the `closestMatches` row in `references/criteria/registry-package.md`; inserted the lookup-script tests / baseline refresh paragraph after the `Self-test:` paragraph in `STEWARDSHIP.md`. Content anchors, not line numbers.
**Result:** `grep -n "npm-popular.tsv"` -> one hit in each file (registry-package.md also carries the refresh command on the next line; STEWARDSHIP.md has both on one line). `python3 -B evals/run_evals.py validate` -> exit 0 (`41 evals, 248 assertions`). `git status` shows only the two intended files modified.
**Status:** Success

### [20261016 20:12] - Completion: full verification, criteria, reviews
**Action:** Ran the plan's Verification Plan in the worktree.
**Result:**
- Full suite with pwsh on PATH: `Ran 19 tests ... OK` (0 skipped). Without pwsh (`PATH=/usr/bin:/bin`): `OK (skipped=6)`.
- `python3 -B -m unittest discover -s evals -p "test_*.py"`: `Ran 12 tests ... OK`. `python3 -B evals/run_evals.py validate`: exit 0.
- `ast.parse(..., feature_version=(3, 8))` over `scripts/*.py`, `scripts/data/*.py`, `tests/test_lookup_scripts.py`: no error.
- pwsh `[Parser]::ParseFile` over `scripts/*.ps1`: no parse errors.
- `git status --porcelain --ignored`: only `tests/__pycache__/` appeared (ignored via the new `__pycache__/` rule; invisible to `git status --porcelain`); removed. No `scripts/.*-cache`.
- PS 5.1 static checklist over the `.ps1` diff (grep of added lines): no `??`, `?.`, ternary, `-AsHashtable`, `-Parallel`, `AsByteStream`; the only `Join-Path` added is nested 2-arg; the only `Invoke-WebRequest` carries `-UseBasicParsing`; status read via `[int]$_.Exception.Response.StatusCode`.
- Source Hygiene over the diff: no projex filenames/IDs, step labels, line-number refs or banners in added script comments (grep clean); new comments are present tense and name the rejected alternative (bare `return $results`, `@()` at call site, unwrapped `if` value, normalized-token match).
- Success criteria: suite OK 19 / skipped=6 [met]; red check 14 failures >= 11 [met, Step 1]; `expresss` live both twins -> `high`, express @ distance 1 [met; `critical` not reachable here, api.npmjs.org blocked]; `chalk` live both twins -> `low`, details start `'chalk' is in the bundled top-1000` [met]; baseline TSV >= 1000 unique unscoped non-increasing rows with required names [met, `BundledBaseline`]; B3 both impls [met]; B4 `.ps1` (1 hit -> list len 1 + `osvCount` 1; 0 hits -> `[]`; GHSA `[]` -> `["OSV","GHSA"]` no `ghsaNote`; GHSA failure -> `["OSV"]` + `ghsaNote`) [met, executed under pwsh 7.4.6]; B5 `.ps1` npm + PyPI [met, executed]; `.gitignore` `__pycache__/` [met]; py3.8 parse + PS parse [met]; no live `claude -p` eval runs [met, evals 3/4 rerun not approved and not run].
- Spec compliance: no external spec linked in the plan; every Step hunk applied as written (see Deviations for the only differences).
- Quality review: no dangling references to removed imports (`math`, `time`, `datetime`) or cache helpers (grep clean); `-CacheHours`/`-NoCache` still bound in both twins and ignored; `.ps1` empty-baseline path (`,@()`) goes through the existing `-not $baseline -or $baseline.Count -eq 0` guard and the missing-baseline test passes in the Python twin only (the `.ps1` missing-baseline branch is covered by static review, not by a test; parity test always supplies a baseline).
- Cleanup: scratch edit scripts and live-run JSON live in the session scratchpad (outside the repo). pwsh 7.4.6 left in the scratchpad `pwsh/` and `pwsh-dl/` for the orchestrator (outside the repo, not installed system-wide). Worktree has no untracked or ignored leftovers. `scripts/.typosquat-cache` created by the Step 1 red run was deleted.
- PowerShell execution status: all `.ps1` changes (vuln-lookup, registry-lookup, typosquat-check) were EXECUTED under pwsh 7.4.6 via the mock-HTTP tests (4 + 1 + parity) and live typosquat runs; Windows PowerShell 5.1 was not run (static checklist only).
**Status:** Success

## Deviations
- Step 1 red run: 14 red (11 FAIL + 3 ERROR) vs the plan's 13 estimate; extra red is `TyposquatPython.test_legacy_cache_flags_accepted`. Criterion (>= 11) met.
- Step 4: `cross-env` ranks 700 (plan: 701); snapshot drift, no effect.
- Steps 2, 3, 5: executed directly (no do-projex / verify-projex sub-subagents); marked Encouraged in the plan. Verification by diff review + tests + live runs.
- Step 5 live: api.npmjs.org is blocked by the sandbox proxy, so `downloadRatio` was `null` and `expresss` scored `high`, not `critical`. Plan states `high` is accepted.

## Issues Encountered
- `execute-precheck.sh` and the other framework scripts are not executable in the skill directory (`Permission denied`); ran them via `bash <script>`.
- Task-list tool unavailable in this subagent environment; the log and per-step commits served as the forcing function.
- Unrelated untracked file `.projex/2610161928-stewardship-review-container-cli-desktop-eval.md` was present on base at start (precheck WARN); left untouched.

## Data Gathered
- Baseline snapshot 2026-10-16: 1000 rows, top `semver 877320600`; ranks chalk 13 | react 83 | lodash 104 | express 136 | prettier 144 | cross-env 700. Must-include not found: `request`.
- `typosquat-check.ps1` wall time: 2.55 s (`expresss`), 1.45 s (`chalk`), 2.48 s (`crossenv`).

## User Interventions
None.
