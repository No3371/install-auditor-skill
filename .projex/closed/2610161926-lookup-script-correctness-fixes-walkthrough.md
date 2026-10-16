# Walkthrough: Lookup Script Correctness Fixes

> **Execution Date:** 2026-10-16
> **Completed By:** Claude (executor subagent) | closed by close-projex subagent
> **Source Plan:** 2610161926-lookup-script-correctness-fixes-plan.md
> **Parent:** 2610161926-lookup-script-correctness-fixes-plan.md
> **Duration:** ~39 min (19:33–20:12 per execution log timestamps)
> **Result:** Success (two environment-bound caveats: `critical` typosquat escalation not exercised live; Windows PowerShell 5.1 not run — see Deviations)

---

## Summary

5 verified lookup-script bugs fixed across `scripts/{vuln-lookup,registry-lookup,typosquat-check}.{ps1,py}`: typosquat baseline now a bundled download-ranked unscoped top-1000 (B1) with a known-popular rule and registry-HEAD existence check (B2); OSV `introduced:"0"` open-ended ranges count as affected (B3); `vuln-lookup.ps1` and `registry-lookup.ps1` return true arrays (B4, B5). First committed offline regression suite for `scripts/` added (`tests/test_lookup_scripts.py`, 19 tests; 6 gated on `pwsh`). All `.ps1` changes were executed under pwsh 7.4.6 (mock-HTTP tests + live typosquat runs).

---

## Objectives Completion

| Objective | Status | Notes |
|-----------|--------|-------|
| B1 typosquat baseline returns text matches, not popular packages | Complete | Bundled `scripts/data/npm-popular.tsv` (1000 rows) + `refresh-npm-popular.py`; live `expresss` → `high`, closest `express` @ distance 1 |
| B2 false "does not exist" note; popular packages flag each other | Complete | `npm_package_exists` / `Test-NpmPackageExists` (HEAD registry.npmjs.org: 200 / 404 / unreachable); known-popular rule forces `low`, clears reasons + combosquat hints |
| B3 `introduced:"0"` open-ended range = not affected | Complete | Explicit `"0"` check, both impls |
| B4 `vuln-lookup.ps1` unrolling + GHSA coverage misreport | Complete | `return ,$results` ×3 |
| B5 `registry-lookup.ps1` unrolling | Complete | `@()` wraps ×2 + `,$installScripts` |
| Offline regression suite + `.gitignore` | Complete | 19 tests; red on old scripts (14), green on fixed |
| Docs (criteria addendum + STEWARDSHIP) | Complete | One paragraph + one table-row reword; one paragraph |

---

## Execution Detail

> Derived from git history (`51079d6`..`edb3b6f`) and the execution log. Hunk ranges are post-change line numbers.

### Step 1: Offline regression suite + `.gitignore` (`51079d6`)

**Planned:** Commit `tests/test_lookup_scripts.py` verbatim, add `__pycache__/` to `.gitignore`; observe red on current scripts (≥ 11 failures).

**Actual:** Both done verbatim. Red run with pwsh 7.4.6 on PATH: `FAILED (failures=11, errors=3)`, 19 run, 14 red. Red list: ERROR `BundledBaseline.test_bundled_file_shape`, `TyposquatPython.test_separator_typo_is_high`, `VulnLookupPowerShell.test_version_filter_keeps_introduced_zero`; FAIL `RegistryLookupPowerShell.test_single_entries_are_arrays`, `TyposquatParity.test_twins_agree`, `TyposquatPython` ×5 (`test_existence_notes`, `test_known_popular_packages_are_low`, `test_legacy_cache_flags_accepted`, `test_missing_baseline_still_checks_compare_to`, `test_typo_of_popular_package_is_high`), `VulnLookupPowerShell` ×2 (`test_single_hit_is_an_array`, `test_zero_hits_and_empty_ghsa_success`), `VulnLookupPython` ×2 (`test_osv_range_matrix`, `test_version_filter_keeps_introduced_zero`). Green on old code as expected: both `test_ghsa_failure_is_reported`, `RegistryLookupPython`, `test_scoped_name_is_not_known_popular`, `test_size_limits_baseline`. `scripts/.typosquat-cache/` created by the red run (old code does live search) deleted.

**Deviation:** 14 red vs plan estimate 13 — extra: `TyposquatPython.test_legacy_cache_flags_accepted` (also fails on old baseline logic). Criterion (≥ 11) met.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `tests/test_lookup_scripts.py` | Created | Yes | 338 lines; Python unit tests (module HTTP helpers replaced), `.ps1` tests via global `Invoke-RestMethod`/`Invoke-WebRequest` shadow functions in temp-dir copies, twin parity test |
| `.gitignore` | Modified | Yes | +1: `__pycache__/` |

**Verification:** red run as above.

**Issues:** None.

---

### Step 2: `vuln-lookup` B3 + B4 (`1885200`)

**Planned:** Open-ended range fix in both impls; `return ,$results` in `Invoke-OsvQuery` (×2) and `Invoke-GhsaQuery` (success); drop divergence note from `.py` docstring.

**Actual:** Applied as written. `vuln-lookup.ps1`: `Test-OsvVersionAffected` tail (~158–161), `Invoke-OsvQuery` returns (~201–204, 229), `Invoke-GhsaQuery` success return (~277–280). `vuln-lookup.py`: `test_osv_version_affected` tail (~174–177), docstring lines 13–16 removed.

**Deviation:** None. `verify-projex` marked Encouraged; self-verified via diff + tests (no sub-subagent).

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `scripts/vuln-lookup.ps1` | Modified | Yes | `introduced -eq '0' -or (Compare-SemVer …) -ge 0` → affected; `,$results` ×3 with rationale comments (names rejected `@()` at call site: would turn GHSA `$null` = failed into 1-element array) |
| `scripts/vuln-lookup.py` | Modified | Yes | same range fix; docstring divergence note removed |

**Verification:** `-k VulnLookup` → 7 tests OK (4 `.ps1` tests executed under pwsh 7.4.6).

**Issues:** None.

---

### Step 3: `registry-lookup.ps1` B5 (`c7e2414`)

**Planned:** Filter inside `@()` for npm + PyPI maintainers; `,$installScripts`; `.py` docstring reduced to UTC-date divergence.

**Actual:** As written. `registry-lookup.ps1`: `Lookup-Npm` maintainers (~85–87), `installScripts` value (~121–122), `Lookup-Pypi` maintainers (~148–149). `registry-lookup.py` docstring (line 8).

**Deviation:** None. Self-verified.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `scripts/registry-lookup.ps1` | Modified | Yes | 3 sites; comments explain unroll hazard |
| `scripts/registry-lookup.py` | Modified | Yes | docstring only |

**Verification:** `-k RegistryLookup` → 2 tests OK (`.ps1` test executed).

**Issues:** None.

---

### Step 4: Bundled npm baseline (`acec101`)

**Planned:** Create `scripts/data/refresh-npm-popular.py` verbatim; run it to generate `npm-popular.tsv`.

**Actual:** Generator written verbatim; run against live registry.npmjs.org (75 s): `wrote 1000 rows; must-include not found: ['request']` (plan-anticipated). TSV: 1004 lines = 4 `#` header lines + 1000 rows, snapshot 2026-10-16, top row `semver 877320600`. Ranks (1-based): chalk 13 | react 83 | lodash 104 | express 136 | prettier 144 | cross-env 700.

**Deviation:** `cross-env` rank 700 vs plan 701 (snapshot drift; no effect).

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `scripts/data/refresh-npm-popular.py` | Created | Yes | 103 lines; maintainer tool, no `.ps1` twin |
| `scripts/data/npm-popular.tsv` | Created | Yes | 1004 lines, generated |

**Verification:** `-k BundledBaseline` → OK.

**Issues:** None.

---

### Step 5: `typosquat-check` twins (`d11ce42`)

**Planned:** Bundled baseline loader; known-popular rule; registry-HEAD existence check; remove cache functions; `-Size` default 1000; keep `-CacheHours`/`-NoCache` as ignored.

**Actual:** All plan hunks applied to both twins via anchored exact-string replacement scripts (scratchpad; each `old` asserted to occur once). `.py`: docstring, imports (`math`, `time`, `datetime` dropped), `BASELINE_PATH`, `cache_path`/`read_cache`/`write_cache` deleted, `get_npm_popular_baseline` replaced, `npm_package_exists` added, `known_popular` rule + ratio guard + details block, parser defaults. `.ps1`: help block, param defaults, `Get-NpmPopularBaseline` replaced, `Test-NpmPackageExists` added, `$knownPopular` rule, details/existence block.

**Deviation:** None to the code. Live-run limits: see Deviations section.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `scripts/typosquat-check.py` | Modified | Yes | Net rewrite of baseline + analysis tail (hunks ~4–6, 20–31, 60, 102–126, 142, 196, 252–269, 297–309) |
| `scripts/typosquat-check.ps1` | Modified | Yes | same design (hunks ~6–53, 127–186, 267, 350–374); 149 lines churn |

**Verification:** `-k Typosquat` → 9 tests OK incl. `TyposquatParity.test_twins_agree` (`.ps1` executed). Live (registry.npmjs.org reachable, api.npmjs.org blocked → `downloadRatio` null): `expresss` py == ps1 JSON, `high`, closest express/1/145199376; `chalk` py == ps1, `low`, details start `'chalk' is in the bundled top-1000 popular npm package baseline`; `crossenv` py == ps1, `high`, closest cross-env/1. `.ps1` wall time 2.55 s / 1.45 s / 2.48 s. No `scripts/.typosquat-cache`, no pycache afterward.

**Issues:** None.

---

### Step 6: Docs (`3403bff`)

**Planned:** Baseline paragraph + `closestMatches` row reword in `references/criteria/registry-package.md`; lookup-test + refresh paragraph in `STEWARDSHIP.md`.

**Actual:** Inserted by content anchor (not line number) as written.

**Deviation:** None.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `references/criteria/registry-package.md` | Modified | Yes | +6-line baseline paragraph (~229–234); `closestMatches` row (~243) |
| `STEWARDSHIP.md` | Modified | Yes | +2 lines: lookup-script tests paragraph after `Self-test:` paragraph (~71) |

**Verification:** `grep -n "npm-popular.tsv"` → one hit per file; `python3 evals/run_evals.py validate` → exit 0 (41 evals, 248 assertions).

**Issues:** None.

---

## Complete Change Log

> **Derived from:** `git diff --stat cf327c5..projex/2610161926-lookup-script-correctness-fixes` (code files; projex-document entries are bookkeeping). Close-time bookkeeping commit and squash land on top.

### Files Created
| File | Purpose | Lines | In Plan? |
|------|---------|-------|----------|
| `tests/test_lookup_scripts.py` | Offline regression suite (Python + pwsh-gated `.ps1` + parity) | 338 | Yes |
| `scripts/data/refresh-npm-popular.py` | Baseline regeneration tool | 103 | Yes |
| `scripts/data/npm-popular.tsv` | Bundled top-1000 unscoped npm baseline | 1004 | Yes |
| `.projex/2610161926-lookup-script-correctness-fixes-log.md` | Execution log (moved to `closed/` at close) | 106 | Yes (execute-projex) |

### Files Modified
| File | Changes | Lines Affected | In Plan? |
|------|---------|----------------|----------|
| `scripts/typosquat-check.py` | Bundled baseline, known-popular, HEAD existence, cache removal | 137 churn | Yes |
| `scripts/typosquat-check.ps1` | same | 149 churn | Yes |
| `scripts/vuln-lookup.ps1` | B3 range; B4 `return ,$results` ×3 | 18 churn | Yes |
| `scripts/vuln-lookup.py` | B3 range; docstring | 10 churn | Yes |
| `scripts/registry-lookup.ps1` | B5 `@()` ×2, `,$installScripts` | 12 churn | Yes |
| `scripts/registry-lookup.py` | docstring | 3 churn | Yes |
| `references/criteria/registry-package.md` | baseline paragraph; table row | +8/−1 | Yes |
| `STEWARDSHIP.md` | test + refresh paragraph | +2 | Yes |
| `.gitignore` | `__pycache__/` | +1 | Yes |
| `.projex/2610161926-lookup-script-correctness-fixes-plan.md` | Status, `Log:` header (then Complete + walkthrough link at close) | — | Yes |

### Files Deleted
None.

### Planned But Not Changed
None. (`SKILL.md`, `dep-scan.*`, `evals/` untouched by design — Out of Scope.)

---

## Success Criteria Verification

Re-run by the closer in the worktree at close time (head `edb3b6f`) unless marked "log".

### Criterion 1: Suite `OK`, 19 tests, 0 skipped with pwsh; `OK (skipped=6)` without
**Method:** `PATH=<pwsh7.4.6>:$PATH python3 -B -m unittest discover -s tests -p "test_*.py"`; again with `PATH=/usr/bin:/bin`.
**Evidence:** `Ran 19 tests in 9.884s` `OK` | `Ran 19 tests in 0.102s` `OK (skipped=6)`.
**Result:** PASS

### Criterion 2: Suite fails on pre-fix scripts (≥ 11 failures)
**Method:** Step 1 red run (log).
**Evidence:** `FAILED (failures=11, errors=3)` → 14 red.
**Result:** PASS

### Criterion 3: `expresss` live → `high`/`critical`, closest `express`, distance 1
**Method:** live run both twins (log, Step 5).
**Evidence:** `riskLevel: high`; `closestMatches[0]` express / 1 / 145199376; py == ps1 JSON. `critical` not reachable: api.npmjs.org blocked by sandbox proxy → `downloadRatio` null. Plan accepts `high`.
**Result:** PASS

### Criterion 4: `chalk` live → `low`, details start `'chalk' is in the bundled top-1000`
**Method:** live run both twins (log).
**Evidence:** `riskLevel: low`; details prefix as required; py == ps1 JSON.
**Result:** PASS

### Criterion 5: `npm-popular.tsv` shape (≥ 1000 unscoped unique non-increasing rows; named packages present)
**Method:** `BundledBaseline.test_bundled_file_shape` (part of the full suite re-run above).
**Evidence:** test OK; 1000 rows; chalk 13 | react 83 | lodash 104 | express 136 | prettier 144 | cross-env 700.
**Result:** PASS

### Criterion 6: B3 — `introduced:"0"` + `-Version 1.0.0` → advisory included (both impls)
**Method:** `VulnLookupPython.test_osv_range_matrix`, `*.test_version_filter_keeps_introduced_zero` (Python + pwsh).
**Evidence:** included in the 19-test OK run.
**Result:** PASS

### Criterion 7: B4 — `.ps1` 1 hit → list len 1 + `osvCount: 1`; 0 hits → `[]`; GHSA `[]` → `["OSV","GHSA"]` no `ghsaNote`; GHSA failure → `["OSV"]` + `ghsaNote`
**Method:** `VulnLookupPowerShell.*` under pwsh 7.4.6.
**Evidence:** 4/4 OK (executed, not skipped).
**Result:** PASS

### Criterion 8: B5 — 1 maintainer → `["solo"]`; 1 hook → 1-element `installScripts` (npm + PyPI)
**Method:** `RegistryLookupPowerShell.test_single_entries_are_arrays`.
**Evidence:** OK (executed).
**Result:** PASS

### Criterion 9: `.gitignore` ignores `__pycache__/`; no `__pycache__` in `git status --porcelain`
**Method:** closer ran suites with `-B`; `git status --porcelain --ignored` in worktree afterwards.
**Evidence:** only ` M .projex/…-log.md` (closer's own header fix) listed; no `!!` or `??` entries.
**Result:** PASS

### Criterion 10: Python parses as 3.8; `.ps1` has no PS 6+/7-only syntax
**Method:** `ast.parse(..., feature_version=(3, 8))` over `scripts/*.py`, `scripts/data/*.py`, `tests/test_lookup_scripts.py`; pwsh `[Parser]::ParseFile` over `scripts/*.ps1`; grep of added `.ps1` lines (log).
**Evidence:** no errors; no `??`, `?.`, ternary, `-AsHashtable`, `-Parallel`, `AsByteStream`; only `Join-Path` added is nested 2-arg; `Invoke-WebRequest` carries `-UseBasicParsing`. PS 5.1 itself not run.
**Result:** PASS (static for 5.1)

### Criterion 11: No live `claude -p` eval runs
**Method:** log review.
**Evidence:** none run; evals 3/4 reruns not approved.
**Result:** PASS

### Acceptance Criteria Summary

| Criterion | Method | Result | Evidence |
|-----------|--------|--------|----------|
| 1 Suite green both modes | unittest ± pwsh | Pass | 19 OK / skipped=6 |
| 2 Red on old scripts | Step 1 run | Pass | 14 red |
| 3 `expresss` flagged | live, both twins | Pass | `high`, express @ 1 |
| 4 `chalk` low | live, both twins | Pass | `low`, bundled details |
| 5 Baseline shape | `BundledBaseline` | Pass | OK |
| 6 B3 | range matrix + version filter | Pass | OK |
| 7 B4 | `VulnLookupPowerShell` | Pass | 4/4 |
| 8 B5 | `RegistryLookupPowerShell` | Pass | OK |
| 9 No pycache leak | `git status --ignored` | Pass | clean |
| 10 py3.8 / PS parse | ast + Parser + grep | Pass | no errors |
| 11 No live evals | log | Pass | none run |

**Overall:** 11/11 criteria passed. Also green at close: `python3 -B -m unittest discover -s evals -p "test_*.py"` → 12 OK; `python3 -B evals/run_evals.py validate` → 41 evals / 248 assertions.

---

## Deviations from Plan

### Deviation 1: Red run count 14 vs 13
- **Planned:** ~13 red.
- **Actual:** 14 (extra: `TyposquatPython.test_legacy_cache_flags_accepted`).
- **Reason:** old baseline logic also fails the legacy-flags test.
- **Impact:** none; ≥ 11 floor met.
- **Recommendation:** none.

### Deviation 2: `cross-env` rank 700 vs 701
- **Reason:** live snapshot drift. **Impact:** none.

### Deviation 3: Steps 2, 3, 5 executed directly
- **Planned:** `do-projex` / `verify-projex` marked Encouraged.
- **Actual:** executor self-verified (diff review + tests + live runs); no sub-subagents.
- **Impact:** none observed; depth budget unused.

### Deviation 4: `critical` typosquat escalation not exercised live
- **Planned:** `high` or `critical` accepted.
- **Actual:** api.npmjs.org blocked by sandbox proxy → `downloadRatio` null → `expresss` scored `high`. The `critical` path (distance 1 + ≥ 1000× ratio) is covered by neither live run nor a test.
- **Impact:** `SKILL.md` Red Flag citing `riskLevel: critical` remains valid by design but unverified end-to-end.
- **Recommendation:** first host with api.npmjs.org access: run `typosquat-check.py -Ecosystem npm -Name expresss` and confirm `critical`.

### Deviation 5: `.ps1` runtime coverage is PowerShell 7.4 only
- **Actual:** all `.ps1` changes executed under pwsh 7.4.6 (mock-HTTP tests + live typosquat runs). Windows PowerShell 5.1 not run; compatibility checked by static checklist only. Test mocks use PS 7 exception types (test-only). The `.ps1` missing-baseline branch is covered by static review, not a test (parity test always supplies a baseline).
- **Impact:** residual 5.1 risk.
- **Recommendation:** run `tests/` on a Windows PowerShell 5.1 host if one becomes available.

### Deviation 6 (closer): execution-log header corrected
- **Actual:** log's `Worktree Path` header read `install-auditor-skill/.projexwt/…` (repo-name-prefixed, resolves to nothing under repo root), making `close-precheck.sh` fail with `recorded Worktree Path is missing or inaccessible`. Closer rewrote it to repo-root-relative `.projexwt/2610161926-lookup-script-correctness-fixes`; precheck then returned `PASS_WITH_WARNINGS` (sole warning: that same uncommitted edit). Header-only change.
- **Recommendation:** execute-projex logs should record `Worktree Path` as repo-root-relative or absolute, never prefixed with the repo directory name.

---

## Issues Encountered

### Issue 1: Framework scripts lack exec bit
- **Description:** `execute-precheck.sh` etc. → `Permission denied`.
- **Severity:** Low. **Resolution:** run with `bash <script>`. **Prevention:** set exec bit in skill sync.

### Issue 2: Task-list tool unavailable in executor subagent
- **Severity:** Low. **Resolution:** log + per-step commits as forcing function.

### Issue 3: Unrelated untracked eval doc on base at execute start
- **Description:** precheck WARN for `.projex/2610161928-stewardship-review-container-cli-desktop-eval.md` (owned by another workflow).
- **Severity:** Low. **Resolution:** left untouched; worktree mode kept it out of the execution. It has since been committed on base by its owner; close squash does not touch it.

### Issue 4: `projex-tree.sh` unusable
- **Description:** `.projex-tree.py` missing from skill directory. Advisory only; close evidence taken from git + log directly.
- **Severity:** Low.

---

## Key Insights

**Rationale promoted:** shipped docs already carry it — `references/criteria/registry-package.md` (bundled-baseline paragraph: known-popular rule, scope-basename caveat, refresh command) and `STEWARDSHIP.md` (baseline is a dated snapshot; refresh during each scheduled registry-package review). Script comments carry the rejected-alternative rationale (bare `return $results`, `@()` at call site, unwrapped `if` value, normalized-token match). No projex filenames in sources.

### Lessons Learned

1. **A baseline's membership must exempt its own members**
   - Context: after B1 was fixed, real popular packages (chalk/chai distance 2, react/react-dom prefix) flagged each other.
   - Insight: distance/combosquat scoring only makes sense for names outside the reference set.
   - Application: known-popular rule; any future allowlist-vs-candidate scorer needs the same exemption.

2. **Test the `.ps1` twin, not just the `.py`**
   - Context: B4/B5 existed only in PowerShell; the parent python-ports verification exercised only Python.
   - Insight: shadowing `Invoke-RestMethod` / `Invoke-WebRequest` with global functions runs the real script offline with no testability edits.
   - Application: reuse `run_ps` for the next `.ps1` change.

3. **Absence of evidence in a reachability probe is not non-existence**
   - Context: B2 reported "does not exist" whenever api.npmjs.org failed.
   - Insight: derive existence from the registry (404 vs unreachable), three-valued.
   - Application: `True | False | None` result with distinct notes.

### Pattern Discoveries

1. **PowerShell unroll triad**
   - Observed in: `vuln-lookup.ps1`, `registry-lookup.ps1`.
   - Description: `return $arr` (0 → `$null`, 1 → item), `X = if (…) { $arr }` inside a hashtable literal, and `@(…) | Where-Object` outside the `@()` all unroll.
   - Reuse: leading comma on return, `,$arr` inside `if` values, filter inside `@()`. Prefer `,$x` over `@()` at call sites when `$null` is a meaningful failure signal.

### Gotchas / Pitfalls

1. **OSV `introduced: "0"` is a marker, not a version**
   - Trap: comparing it as semver/skipping it silently drops all-versions advisories.
   - Avoidance: explicit `== "0"` check; do not rely on `compare_semver`'s unparseable→0 fallback.

2. **npm search API no longer honors `popularity=` or `boost-exact:`**
   - Trap: both are treated as text; every result carries `score.detail.popularity == 1`.
   - Avoidance: rank by `downloads.weekly`; keep search only as the refresh-tool data source.

### Technical Insights

- Top-level `tests/` stays out of the eval snapshot (`SNAPSHOT_DIRS` covers `scripts/`); `scripts/data/*` is tracked and therefore snapshotted into eval runs.
- Importing scripts under test needs `sys.dont_write_bytecode = True` or `scripts/__pycache__` appears (hence `.gitignore` entry too).
- `-CacheHours` / `-NoCache` stay accepted-but-ignored in both twins so existing invocations do not fail argument binding.

---

## Recommendations

### Immediate Follow-ups
- [ ] On a host with api.npmjs.org access: verify `expresss` → `critical` live (Deviation 4).
- [ ] Optional, needs spend approval: `python3 evals/run_evals.py prepare --ids 3,4` → run → grade → summary (evals 3/4 were the motivating cases).
- [ ] First host with OSV/GHSA access: live `vuln-lookup` lodash 4.17.20 / `dep-scan` mkdirp 0.5.1 (carried from `2610161849-python-script-ports-walkthrough.md`).

### Future Considerations
- Scope-impersonation signal (`@evil/chalk` basename equals popular `chalk` → no hint today; docs require manual scope check). Flagging every `@types/<popular>` needs an allowlist.
- Download fallback via search `downloads.weekly` when api.npmjs.org is blocked (restores `critical` escalation in restricted networks).
- Baseline staleness: snapshot ages; refresh duty now lives in `STEWARDSHIP.md`.
- Known-popular trusts the snapshot: a squat needs ~15 M weekly downloads to enter the top 1000.

### Plan Improvements
If re-executed:
- State `Worktree Path` convention expected by `close-precheck.sh` (repo-root-relative or absolute).
- Note api.npmjs.org may be unreachable in sandboxes; make `high` the primary live expectation and `critical` a conditional bonus.

---

## Related Projex Updates

### Documents to Update
| Document | Update Needed |
|----------|---------------|
| `2610161926-lookup-script-correctness-fixes-plan.md` | Complete; walkthrough link; moved to `closed/` (done at close) |
| `2610161926-lookup-script-correctness-fixes-log.md` | Moved to `closed/` (done at close) |
| `2604070218-install-auditor-subject-typed-redesign-nav.md` | Phase 6 checkbox + Revision Log entry + Recent Progress (done at close; plan carried no `Nav:` field — recorded per repo convention at orchestrator direction) |
| `2610161927-registry-package-and-ci-action-stewardship-review-eval.md` | Left active, unchanged: references this plan by filename only as the sibling that fixes RP-7-adjacent script bugs; its own follow-on (RP-7 tooling) is a separate plan |

### New Projex Suggested
| Type | Description |
|------|-------------|
| Plan | Scope-impersonation signal + download fallback for `typosquat-check` (follow-ups above); a concurrent planner already holds `2610161941-shared-version-integrity-floor-plan.md` (not touched here) |

---

## Appendix

### References
- Commits on `projex/2610161926-lookup-script-correctness-fixes` (merge-base `cf327c5`): `51079d6` step 1 | `1885200` step 2 | `c7e2414` step 3 | `acec101` step 4 | `d11ce42` step 5 | `3403bff` step 6 | `edb3b6f` completion.
- Execution log: `2610161926-lookup-script-correctness-fixes-log.md`.
- Parent follow-up source: `2610161849-python-script-ports-walkthrough.md`.
