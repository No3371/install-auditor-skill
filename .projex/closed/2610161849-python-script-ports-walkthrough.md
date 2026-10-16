# Walkthrough: Python Ports of Lookup Scripts

> **Execution Date:** 2026-10-16
> **Completed By:** Claude (Sonnet 5.5 executor; close by Sonnet 5.5 subagent under orchestrator)
> **Source Plan:** 2610161849-python-script-ports-plan.md
> **Parent:** 2610161849-python-script-ports-plan.md
> **Duration:** ~1h40 execution (18:55–20:35) + close
> **Result:** Success

---

## Summary

Four stdlib-only Python 3.8+ twins (`scripts/registry-lookup.py`, `typosquat-check.py`, `vuln-lookup.py`, `dep-scan.py`; 1471 lines) now mirror the `.ps1` scripts' flags and JSON contract. `.ps1` files unchanged. Doc call sites (`SKILL.md` lines 87 + 241, `references/criteria.md`, `references/criteria/registry-package.md`, `workflows/registry-package.md`) switched to Python-first with one `.ps1` twin note per file. 8/8 success criteria pass; OSV/GHSA success paths verified by offline fixtures only (proxy blocks hosts here).

---

## Objectives Completion

| Objective | Status | Notes |
|---|---|---|
| 4 Python ports exist, exec, stdlib-only | Complete | Mode `100755`, shebang, imports: argparse datetime gzip json math os re shutil subprocess sys tempfile time urllib |
| Py 3.8 grammar + `--help` | Complete | `ast.parse(feature_version=(3,8))` ok; `--help` rc 0 x4 (re-run at close with `-I`) |
| Flag parity | Complete | PS-style `-Flag` + `--kebab` aliases; registry-lookup also positional |
| JSON contract parity (success + error paths) | Complete | Key order asserted by harness for 3 scripts; registry-lookup by reading + live |
| Pure-logic parity (Levenshtein, semver, ranges, severity, pypi reqs) | Complete | Harness 66 asserts OK |
| Live usability | Complete | 5 ecosystems populated; dep-scan chalk Tier 2 + cache hit; mkdirp Tier 3 lockfile resolved via real npm |
| Doc call sites | Complete | Residue grep = allowed set; counts 6/4/1 |
| SKILL.md minimal; no `.ps1`/`evals/`/`.gitignore` edits | Complete | Hunks at 87, 241 only |

---

## Execution Detail

> Derived from git history + execution log. Branch commits (`b8922c1..projex/2610161849-python-script-ports`): `4b3370c` step 1 | `15db98a` step 2 | `0e6af6a` step 3 | `272fa4c` step 4 | `16aff36` step 5 | `0178221` complete.

### Step 1: Port registry-lookup

**Planned:** `scripts/registry-lookup.py` ≡ `.ps1`; positional + flag CLI; 5 ecosystems + openssf; not-found → stderr + exit 1.

**Actual:** Written as planned; CLI via `parse_intermixed_args` — named wins, positionals fill unbound slots in order (mirrors PowerShell binding). `chmod +x`.

**Deviation:** None (positional-binding detail refines plan's "named wins").

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|---|---|---|---|
| `scripts/registry-lookup.py` | Created | Yes | 364 lines |

**Verification:** Live `npm lodash`, `-Ecosystem npm -Name @types/node`, `pypi requests`, `crates serde` (`ecosystem: crates.io`), `rubygems rails`, `nuget Newtonsoft.Json` (gzip handled), `npm lodash 4.17.21`; not-found → rc 1, stderr `Package '<n>' not found on npm`, empty stdout; bad ecosystem/missing name → rc 2. Re-verified at close: `npm lodash` populated JSON, not-found rc 1.

**Issues:** None. Downloads/openssf null/absent (hosts blocked by proxy), as plan predicted.

---

### Step 2: Port typosquat-check

**Planned:** Faithful port incl. verbatim (known-broken) baseline query.

**Actual:** As planned. Cache write happens even with `-NoCache` (only the read is skipped, as `.ps1`).

**Deviation:** Per-name weekly-download lookups memoized within one analysis (`.ps1` fetches the queried name twice). Output identical; one fewer call.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|---|---|---|---|
| `scripts/typosquat-check.py` | Created | Yes | 333 lines |

**Verification:** Harness §A: `lev("expresss","express")==1`, `("lodahs","lodash")==2`, `("","abc")==3`, `token("@Scope/Foo__Bar")=="foo-bar"`. §B: `expresss` vs fixture baseline → `closestMatches[0].name=="express"`, `downloadRatio.ratio==-1`, `riskLevel=="critical"`, `combosquatHints==["express"]`; error path exit 0. Live `-CompareTo express -NoCache` → `{name: express, distance: 1}`, `riskLevel: high`, `downloadRatio: null` (api.npmjs.org blocked).

**Issues:** None; created cache dir removed.

---

### Step 3: Port vuln-lookup

**Planned:** Mirror incl. `[System.Version]` compare semantics and conservative quirks.

**Actual:** As planned: severity helpers, `_to_sysver`/`compare_semver`, `test_osv_version_affected`, `test_ghsa_version_affected`, `invoke_osv_query`, `invoke_ghsa_query`, `get_discrepancies`, `get_risk_level`, cache + main.

**Deviation:** `\d` → `[0-9]` in `_SYSVER` and CVSS-score regex (strict ASCII, like PS `[System.Version]`). `get_discrepancies` keys case-insensitive (PS hashtable semantics), original spelling emitted.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|---|---|---|---|
| `scripts/vuln-lookup.py` | Created | Yes | 362 lines |

**Verification:** §A all pass (semver 6, OSV range 4, GHSA 3, severity 3+). §B: minimist 0.0.8 → `osvResults` len 1, `summary == {totalCount:2, osvCount:1, ghsaCount:1, highestSeverity:"medium"}`, `sources==["OSV","GHSA"]`, key tail `riskLevel, version`; GHSA failing → `sources==["OSV"]`, `ghsaResults==[]`, `ghsaNote` (em dash verbatim); OSV failing → error JSON exit 0, not cached; cache round-trip zero network; `GITHUB_TOKEN` → Bearer header. Live lodash 4.17.20 → error JSON (`Tunnel connection failed: 403 Forbidden`), `riskLevel: unknown`, exit 0 (as predicted).

**Issues:** Latent `.ps1` defect mirrored, not fixed — see Issues Encountered.

---

### Step 4: Port dep-scan

**Planned:** Mirror; Tier 3 must run `npm install --package-lock-only --ignore-scripts` in a temp dir always deleted.

**Actual:** As planned. Flags exactly `install --package-lock-only --ignore-scripts --silent`; `tempfile.mkdtemp()` + `finally: rmtree`; `timeout=300`.

**Deviation:** `subprocess.TimeoutExpired` converted to `RuntimeError("npm install --package-lock-only timed out after 300 s")` for a readable `fallbackReason` (raw message embeds argv list). Direct-name set lower-cased for depth (PS hashtable semantics).

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|---|---|---|---|
| `scripts/dep-scan.py` | Created | Yes | 412 lines |

**Verification:** pypi requirement parsing → `["urllib3","idna","certifi"]`; `mkdirp 0.5.1 -Tier 2` fixture → minimist/high/`CVE-2020-7598`/depth 1, `directDepCount:1`, enrichment URL called once; second run `cacheHit:true`, zero network; Tier 3 with `which`→None → `fallback:true`, `fallbackReason:"npm CLI unavailable"`, `tier:2`; `crates serde` → `limitationNote`, `riskLevel:"none"`; fake-npm Tier 3 → `tier:3`, `transitiveDepCount:3`, argv/cwd recorded, temp dir gone (also after failing npm). Live: chalk 5.3.0 Tier 2 → `directDepCount:0`, `riskLevel:"none"`, rerun `cacheHit:true`; mkdirp Tier 3 → real npm 10.9 resolved lockfile, OSV 403 → error JSON; no leftover temp dir.

**Issues:** None.

---

### Step 5: Switch doc call sites to Python-first

**Planned:** Invocations → `python3 scripts/<x>.py`; prose → stem; twin note per file; SKILL.md lines 87 + 241 only.

**Actual:** Done as planned; edits matched by content, not line number (plan line numbers drifted by 2 after inserted twin notes).

**Deviation:** None (extra `.ps1 twin` mention at `workflows/registry-package.md:52` is within the plan's allowed residue).

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|---|---|---|---|
| `SKILL.md` | Modified | Yes | L87 lookup-scripts wording; L241 Reference Files script bullet (2+/2-) |
| `references/criteria.md` | Modified | Yes | L9 `.py` + twin sentence; L39/L159 stem; L63/L151/L157 `.py` (6+/6-) |
| `references/criteria/registry-package.md` | Modified | Yes | 4 invocation blocks → `python3`; prose → stem; twin note; `GITHUB_TOKEN` shell syntax (19+/17-) |
| `workflows/registry-package.md` | Modified | Yes | 6 invocation blocks → `python3`; table/prose → stem; twin note + L52 twin mention (28+/26-) |

**Verification:** `git diff -U0 SKILL.md` hunks at 87, 241 only. Residue grep (re-run at close): `SKILL.md:156` (deferred), `SKILL.md:241`, `workflows/registry-package.md:52,99,259`, `references/criteria.md:9`, `references/criteria/registry-package.md:134,166` — exactly the allowed set. `grep -c 'python3 scripts/'` → 6 | 4 | 1.

**Issues:** None.

---

## Complete Change Log

> **Derived from:** `git diff --stat b8922c1..projex/2610161849-python-script-ports` (10 files, +1614/-52 incl. plan + log).

### Files Created
| File | Purpose | Lines | In Plan? |
|---|---|---|---|
| `scripts/registry-lookup.py` | registry metadata lookup twin | 364 | Yes |
| `scripts/typosquat-check.py` | npm typosquat check twin | 333 | Yes |
| `scripts/vuln-lookup.py` | OSV + GHSA CVE lookup twin | 362 | Yes |
| `scripts/dep-scan.py` | dependency CVE scan twin | 412 | Yes |
| `.projex/2610161849-python-script-ports-log.md` | execution log | 86 | n/a (projex) |

### Files Modified
| File | Changes | Lines Affected | In Plan? |
|---|---|---|---|
| `SKILL.md` | L87, L241 | 2 | Yes |
| `references/criteria.md` | 6 script refs | 6 | Yes |
| `references/criteria/registry-package.md` | invocations, prose, twin note, token syntax | 19+/17- | Yes |
| `workflows/registry-package.md` | invocations, prose, twin note | 28+/26- | Yes |
| `.projex/2610161849-python-script-ports-plan.md` | status Complete, Log link | 3 | n/a (projex) |

### Files Deleted
None.

### Planned But Not Changed
None. (Plan's "no `.ps1`/`evals/`/`.gitignore` edits" honored.)

---

## Success Criteria Verification

### Criterion 1: 4 ports exist, `100755`, shebang, stdlib-only
**Verification Method:** `git ls-files -s scripts/*.py`; import grep.
**Evidence:** four `100755` entries; imports = argparse datetime gzip json math os re shutil subprocess sys tempfile time urllib.
**Result:** PASS

### Criterion 2: Py 3.8 grammar + `--help` exit 0
**Verification Method:** `ast.parse(..., feature_version=(3,8))`; `python3 -B -I scripts/<x>.py --help`.
**Evidence:** `ast ok`; four rc=0.
**Result:** PASS

### Criterion 3: Flag parity
**Verification Method:** `--help` vs `.ps1` `param()` blocks (execution review).
**Evidence:** `-Ecosystem -Name -Version -Tier -CompareTo -Size -CacheHours -NoCache` + kebab aliases per script; registry-lookup positional.
**Result:** PASS

### Criterion 4: JSON key set/order parity incl. error paths
**Verification Method:** Offline fixture harness (scratchpad, not committed).
**Evidence:** key order asserted for typosquat / vuln-lookup / dep-scan success, fallback, error; registry-lookup per `[ordered]@{}` read + live.
**Result:** PASS

### Criterion 5: Pure-logic parity
**Verification Method:** Harness §A.
**Evidence:** `OK 66 asserts` (typosquat vuln depscan suites).
**Result:** PASS

### Criterion 6: Live runs
**Verification Method:** Manual live matrix.
**Evidence:** five ecosystems populated; chalk Tier 2 + cache hit; mkdirp Tier 3 lockfile via npm. Unreachable: api.osv.dev, api.npmjs.org, pypistats.org, api.securityscorecards.dev (null/absent fields or error JSON, as predicted); `api.github.com/advisories` never reached live.
**Result:** PASS (OSV/GHSA success paths fixture-only)

### Criterion 7: `.ps1` residue
**Verification Method:** `grep -n '\.ps1'` over `SKILL.md workflows/ references/`.
**Evidence:** only allowed set (see Step 5).
**Result:** PASS

### Criterion 8: No out-of-scope edits
**Verification Method:** `git diff --stat`; `git diff -U0 SKILL.md`.
**Evidence:** SKILL.md hunks 87/241; no `.ps1`/`evals/`/`.gitignore` in diff.
**Result:** PASS

### Acceptance Criteria Summary

| Criterion | Method | Result | Evidence |
|---|---|---|---|
| 1 ports exist/exec/stdlib | git ls-files, grep | Pass | Criterion 1 |
| 2 grammar + help | ast, --help | Pass | Criterion 2 |
| 3 flag parity | help vs param() | Pass | Criterion 3 |
| 4 JSON parity | harness | Pass | Criterion 4 |
| 5 pure-logic | harness | Pass | Criterion 5 |
| 6 live | manual | Pass | Criterion 6 |
| 7 residue | grep | Pass | Criterion 7 |
| 8 minimal diff | git diff | Pass | Criterion 8 |

**Overall:** 8/8 criteria passed.

---

## Deviations from Plan

### Deviation 1: Worktree mode
- **Planned:** header `Worktree: No`.
- **Actual:** `Yes` (orchestrator override; concurrent plans share main checkout). Edited in base start commit `b8922c1`.
- **Impact:** none; clean isolation.
- **Recommendation:** none.

### Deviation 2: No Do-/Verify-Projex subagents
- **Planned:** "Encouraged" for steps 1–4.
- **Actual:** self-executed; no subagent tool in executor session. Self-verified by line-by-line comparison with `.ps1` + fixtures.
- **Impact:** parity not independently reviewed; `pwsh` absent, so no live `.ps1` diff either.
- **Recommendation:** first host with `pwsh` + OSV access should diff outputs.

### Deviation 3: typosquat download memoization
- Plan said line-for-line; port memoizes per-name downloads (output identical, one fewer network call).

### Deviation 4: dep-scan timeout message
- `TimeoutExpired` → `RuntimeError("npm install --package-lock-only timed out after 300 s")` instead of raw exception message.

### Deviation 5: `[0-9]` for `\d`
- `_SYSVER` and CVSS-score regex use `[0-9]` (strict ASCII like `[System.Version]`).

---

## Issues Encountered

### Issue 1: Latent `.ps1` defect in `Test-OsvVersionAffected` (mirrored, not fixed)
- **Description:** Open-ended-range tail sets `$floor = -1` when `$introduced -eq '0'`, then requires `$floor -ge 0`. OSV range `introduced: "0"` with no `fixed`/`last_affected` (all versions affected) is reported NOT affected when `-Version` is given. Anti-conservative (false negative). `test_osv_version_affected("1.0.0", [{type:SEMVER, events:[{introduced:"0"}]}], [])` returns False in both impls.
- **Severity:** Medium
- **Resolution:** Ported faithfully per plan; separate patch needed touching `.ps1` and `.py`.
- **Time Impact:** none
- **Prevention:** port plans should list known upstream defects up front (this one was found at Step 3).

### Issue 2: Base advanced during execution (close-time)
- **Description:** base gained `5c44b79` (dispatcher-rubric-consistency) and `3abdc75` (eval-runner-harness) while this branch was open. Both edited the roadmap nav; `5c44b79` added `references/classifier.md` bullet under `SKILL.md` Reference Files, adjacent to this branch's L241 edit; base also stripped roadmap labels from `workflows/registry-package.md`.
- **Severity:** Low
- **Resolution:** see Close-Time Integration below.

---

## Key Insights

**Rationale promoted:** none needed. Shipped rationale lives in script docstrings/comments (gzip handling, `-1` for infinity, `[0-9]` vs `\d`, no `npm ci`); each script docstring states "change both together".

### Lessons Learned

1. **Port from the contract, verify with fixtures when the reference runtime is absent**
   - Context: `pwsh` unavailable; proxy blocks OSV/GHSA.
   - Insight: offline fixtures routed by exact URL + pinned `.ps1` quirks (§A asserts) gave real parity evidence without the reference runtime.
   - Application: keep harness-as-scratchpad pattern for future ports; consider committing it if drift becomes a concern.

2. **Plan doc line numbers drift**
   - Context: twin-note inserts shifted later targets by 2 lines.
   - Insight: content-matched edits beat line-number edits.

### Pattern Discoveries

1. **Single `http_json` entry point**
   - Observed in: all four scripts.
   - Description: every network call funnels through one fn → trivially monkeypatched for fixtures; gzip handling in one place.
   - Reuse potential: any future script.

### Gotchas / Pitfalls

1. **NuGet registration5-gz is always gzip**
   - Trap: `urllib` does not auto-decompress (`Invoke-RestMethod` does).
   - Avoidance: magic-byte/Content-Encoding check in `http_json`.

2. **PowerShell pipeline unrolling shapes JSON**
   - Trap: 1-element results become scalars, empty → `null`; `.ps1` outputs differ from Python's true lists (Divergence 1).
   - Avoidance: consumers must tolerate both shapes; fix `.ps1` with `@(...)`.

### Technical Insights

- `python3 -I` drops script dir from `sys.path` → standalone scripts (no shared module) are required.
- Tier 3 safety rests on `--package-lock-only --ignore-scripts`; tests assert the exact argv.

---

## Recommendations

### Immediate Follow-ups
- [ ] Patch `Test-OsvVersionAffected` / `test_osv_version_affected`: `introduced: "0"` + no fix must be affected (both impls).
- [ ] Plan: typosquat popularity baseline query broken in both impls (`text=boost-exact:false` returns text matches for "boost"); needs curated top-N list or `objects[].downloads.weekly` sort.
- [ ] Patch `.ps1` single-result array counting (`@(...)` wraps): `osvResults`/`ghsaResults`/`summary.osvCount`, `registry-lookup` `maintainers`.
- [ ] First host with OSV/GHSA access: run `vuln-lookup.py -Ecosystem npm -Name lodash -Version 4.17.20` (expect CVE-2021-23337) and `dep-scan.py -Ecosystem npm -Name mkdirp -Version 0.5.1 -Tier 2` (expect minimist HIGH).

### Future Considerations
- Dual-impl drift: consider a STEWARDSHIP entry and/or committed fixture harness.
- `SKILL.md:156` (`registry-lookup.ps1 / npm API` in report skeleton) deferred to the SKILL.md compression plan.
- Script path resolution relative to skill install dir (pre-existing convention).

### Plan Improvements
- List known upstream defects before "line-for-line" porting.
- State doc edits by content anchors, not line numbers.

---

## Related Projex Updates

### Documents to Update
| Document | Update Needed |
|----------|---------------|
| 2610161849-python-script-ports-plan.md | Complete; Walkthrough + Log links; moved to closed/ |
| 2610161849-python-script-ports-log.md | Status Complete; moved to closed/ |
| 2604070218-install-auditor-subject-typed-redesign-nav.md | Phase 6 maintenance entry (updated in place) |

### New Projex Suggested
| Type | Description |
|------|-------------|
| Plan | Patch OSV `introduced: "0"` open-ended range false negative (both impls) |
| Plan | Fix typosquat popularity baseline (both impls) |
| Patch | `.ps1` array-wrapping for single-result JSON |
| Plan | SKILL.md compression (carry Reference Files script bullet wording; fix L156) |

---

## Close-Time Integration

- Merge strategy: squash into `claude/youthful-dijkstra-5ov1kt`.
- Anticipated conflicts, resolved by keeping both sides: `SKILL.md` Reference Files (this branch's script bullet + base's `references/classifier.md` bullet); roadmap nav add/add (Last Revised, Recent Progress, Phase 6 checklist, Revision Log).
- Tooling note: `close-precheck.sh` errors on the repo-relative `Worktree Path` header and `projex-tree.sh` lacks `.projex-tree.py`; close proceeded on direct git evidence.

---

## Appendix

### Execution Log
See `2610161849-python-script-ports-log.md`.

### Test Output
Close-time re-verification (worktree): `ast ok`; `--help` rc 0 x4; imports stdlib only; residue grep = allowed set; `grep -c 'python3 scripts/'` → 6 | 4 | 1; `registry-lookup.py npm lodash` populated; `registry-lookup.py npm zz9-nonexist-pkg-xx` rc 1; worktree `git status --porcelain --ignored=matching` empty.

### References
- Commits: `4b3370c`, `15db98a`, `0e6af6a`, `272fa4c`, `16aff36`, `0178221` on `projex/2610161849-python-script-ports` (fork `b8922c1`)
- Sibling closed plans: 2610161852-dispatcher-rubric-consistency-plan.md, 2610161850-eval-runner-harness-plan.md
