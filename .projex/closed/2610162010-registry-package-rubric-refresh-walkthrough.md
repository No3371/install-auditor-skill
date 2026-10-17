# Walkthrough: Registry-Package Rubric Refresh

> **Execution Date:** 2026-10-17
> **Completed By:** Claude (executor subagent) | closed by close-projex subagent
> **Source Plan:** 2610162010-registry-package-rubric-refresh-plan.md
> **Parent:** 2610162010-registry-package-rubric-refresh-plan.md
> **Duration:** ~32 min (04:48-05:20 per execution log timestamps)
> **Result:** Success

---

## Summary

Registry-package (Type 1) rubric moved from per-package to per-version trust on the shared §4.6 floor. Six shipped files changed: `registry-lookup` npm output gains identity and continuity fields in both twins (+4 tests); the addendum gains the trust-table rewrite, Tier 1 version-age and continuity rows, client execution model, new risk vectors, C6-aligned CVE tables and the `## CVE Scope (§4.3)` + `## Version & Update Integrity (§4.6)` plug-ins; the workflow is wired to match; `references/registries.md` language-registry rows corrected. All 47 plan edits applied verbatim, no Before-miss, no user intervention. Human decision "Relax: identity optional" encoded: absent trusted publishing or provenance never blocks Tier 1; a publisher change forces Tier 3.

This is the last of the 10 subject rubric refreshes; with the shared floor, all are now closed.

---

## Human Decision and Residual Risk (recorded)

**Human decision (2026-10-17, verbatim, via orchestrator):** "Relax: identity optional — Missing trusted publishing or provenance does not block Tier 1 if every other Tier 1 condition holds. These are still required: version at least 7 days old, no change of signer or publisher from the previous release, and big adoption. A publisher change still forces a deep audit. Quick audits stay fast for popular packages."

**Residual risk recorded by the planner (accepted by the human):** a stolen-token publish from the *same* account on a package that has never used trusted publishing or provenance changes neither signer nor publisher. Tier 1 then rests on the 7-day version-age rule (§4.6 V1) alone, plus the incident search and CVE checks. Mitigation is empirical (2025-26 incidents were mostly caught within 7 days). A drop of trusted publishing/provenance that a package *had* still breaks V3 and forces Tier 2/3 handling.

---

## Objectives Completion

| Objective | Status | Notes |
|-----------|--------|-------|
| RP-7 (npm) tooling: `publisher`, `trustedPublisher`, `provenance`, `previousVersion`, `removedVersions` in both twins, offline tests | Complete | No new HTTP calls; non-npm output unchanged; parity of key set and order checked ad hoc |
| RP-1 version age / pinned-version triage | Complete | Tier 1 row `daysSincePublish` ≥ 7; triage passes `-Version`; V1 plug-in with per-ecosystem sources and client cooldowns |
| RP-2 identity scored as origin, not safety; continuity | Complete | V2 scoring bullets; Continuity row; V3 diff rules; presence no longer "strong positive" |
| RP-4 client execution model, new vectors | Complete | npm 12 / pnpm / Bun script-blocking; `binding.gyp`, `.pth`, dropper, persistence |
| RP-5 trust table rewrite | Complete | PGP row dropped; trusted publishing for npm, PyPI, crates.io, RubyGems, NuGet; Go sumdb = consistency; `GONOSUMCHECK` row removed |
| RP-6 `registries.md` language-registry rows | Complete | 9 whole-line replacements, hunks at L6-38 only |
| RP-9 adoption bars per script field window | Complete | Per-field adoption table; "100K crates.io all-time" removed |
| C6 alignment | Complete | `vuln-lookup` / `dep-scan` tables rewritten to §4.3 classes; workflow "Unpatched CRITICAL/HIGH CVE" replaced |
| Eval-8 contradiction (missing provenance CONDITIONAL) | Complete | Never-used mechanism = note only; workflow CONDITIONAL removed |
| Human Tier 1 identity decision | Complete | Identity optional; continuity + age required; publisher change -> Tier 3 in addendum and workflow |

---

## Execution Detail

> Derived from `git log` / `git diff` of `3668e62..projex/2610162010-registry-package-rubric-refresh` and the execution log. Base start commit `3668e62`.

### Preflight

**Planned:** floor/siblings ancestry, greps, sizes, baseline tests.
**Actual:** `20843cc` and `8564410` ancestors of the branch; floor heading count 1; `Addendum:` lines 6; floor walkthrough present; `§4.6 V4` in workflow 2; `Version & Update Integrity` in addendum 0; sizes 17,237 / 23,201 / 4,932 B; tests Ran 19 OK (pwsh 7.4.6 on PATH for the run only); evals unittest Ran 12 OK; `validate` exit 0.
**Deviation:** None.

### Step 1: npm identity + continuity fields in `registry-lookup` (both twins) + tests

**Planned:** edits 1a-1h.
**Actual:** Python `_npm_identity`, `_npm_previous_version`, new npm keys (1a-1c). PowerShell `ConvertTo-UtcDate`, `Get-NpmIdentity`, `Get-NpmPreviousVersion`, same keys (1d-1f). Fixture `NPM_IDENTITY_DRIFT`, helper `without`, 2 asserts on existing single-entry tests, 2 new Python and 2 new PowerShell tests (1g-1h). Commit `b39152d`.
**Deviation:** None.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `scripts/registry-lookup.py` | Modified | Yes | +59: helpers at L93-129, new keys in `lookup_npm` (L158-174, L196-200) |
| `scripts/registry-lookup.ps1` | Modified | Yes | +75: helpers at L72-121, `Lookup-Npm` keys (L154-173, L196-200) |
| `tests/test_lookup_scripts.py` | Modified | Yes | +62: fixture L120-146; Python asserts/tests L259-284; PowerShell asserts/tests L292-305 |

**Verification:** tests Ran 23 OK with pwsh (the 4 PowerShell registry tests ran); without pwsh Ran 23 OK (skipped=8). Ad hoc parity check: identical npm key sets and order across twins for the drift fixture; `previousVersion.publishedAt` 2020-01-01 in both.

**Issues:** None.

### Step 2: Addendum `references/criteria/registry-package.md`

**Planned:** edits 2a-2m.
**Actual:** 13/13 applied via an extractor that took each Before/After pair verbatim from the plan fences and required exactly one match per Before (all-or-nothing write). 2m's Before (= 2f's After) matched because 2f went first. Commit `50478c3`.
**Deviation:** Size only (30,112 B vs "~27 KB" estimate); text is the plan's After verbatim.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `references/criteria/registry-package.md` | Modified | Yes | +221 / -44; 17,237 -> 30,112 B. Header precedence (L6-7); trust table and scoring (L17-48); Tier 1/2/3 and adoption (L74-121); `Client execution model` and new risk patterns (L130-243, L251-317); C6 CVE tables (L365-372); `## CVE Scope (§4.3)` and `## Version & Update Integrity (§4.6)` (L500+) |

**Verification:** `## Version & Update Integrity (§4.6)` count 1; bullets V1-V5 in order; `## CVE Scope (§4.3)` count 1 directly before it; `| Identity (§4.6 V2) | Not required` count 1; stale-phrase count 0.

**Issues:** None.

### Step 3: Workflow `workflows/registry-package.md`

**Planned:** edits 3a-3q.
**Actual:** 17/17 applied with the same extractor. Identify item 7 and triage `-Version` (3 invocation forms, `[-Version "<version>"]` x4); Tier 1/3 lists with publisher-change rule; research Q2/Q5; coverage row; verdict notes (removed "Missing provenance when mechanism exists", "Unpatched CRITICAL/HIGH CVE", "Presence is a strong positive"). Commit `c2a08c1`.
**Deviation:** Size only (26,589 B vs "+~3 KB" estimate); see Deviations for the awk width check.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `workflows/registry-package.md` | Modified | Yes | +84 / -29; 23,201 -> 26,589 B. 24 hunks from L83 to L537 (Identify, triage, Tier 1/2/3, dependency and CVE steps, coverage table, verdict notes) |

**Verification:** stale-phrase count 0; `§4.6 V[1-5]` references 13 (>= 8); no added prose line over 78 characters by character count.

**Issues:** None.

### Step 4: `references/registries.md` language-registry rows

**Planned:** edits 4a-4i.
**Actual:** 9/9 whole-line replacements (L6, 11, 14, 20, 23, 26, 29, 32, 38). PyPI "No mandatory publishing auth", Go "High trust for modules in the index" and "Direct VCS installs bypass this" corrected. Commit `eda463d`; completion commit `8f6da7f` (log, plan status).
**Deviation:** None.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `references/registries.md` | Modified | Yes | +9 / -9; 4,932 -> 6,176 B; nothing in §IDE / §CI/CD / §Container Images |
| `.projex/2610162010-registry-package-rubric-refresh-log.md` | Created | No (execution artifact) | 76-line execution log |
| `.projex/2610162010-registry-package-rubric-refresh-plan.md` | Modified | No (lifecycle) | Status In Progress -> Complete; `Log:` header added |

---

## Complete Change Log

> **Derived from:** `git diff --stat 3668e62..projex/2610162010-registry-package-rubric-refresh` (8 files, +588 / -83), before this close commit.

### Files Created
| File | Purpose | Lines | In Plan? |
|------|---------|-------|----------|
| `.projex/2610162010-registry-package-rubric-refresh-log.md` | Execution log | 76 | Lifecycle artifact |

### Files Modified
| File | Changes | Lines Affected | In Plan? |
|------|---------|----------------|----------|
| `references/criteria/registry-package.md` | Trust table, Tier rows, client model, vectors, C6, §4.3 + §4.6 plug-ins | +221 / -44 | Yes |
| `workflows/registry-package.md` | Identify, triage, Tier 1/3, research, coverage, verdict wiring | +84 / -29 | Yes |
| `references/registries.md` | 9 language-registry rows | +9 / -9 (L6-38) | Yes |
| `scripts/registry-lookup.py` | npm identity/continuity helpers and keys | +59 | Yes |
| `scripts/registry-lookup.ps1` | Same, PowerShell twin | +75 | Yes |
| `tests/test_lookup_scripts.py` | Fixture, helper, 4 new tests, 2 added asserts | +62 | Yes |
| `.projex/2610162010-registry-package-rubric-refresh-plan.md` | Status -> Complete, `Log:` link | +2 / -1 | Lifecycle |

### Files Deleted
None.

### Planned But Not Changed
None. `SKILL.md`, `references/criteria.md`, `evals/`, `STEWARDSHIP.md` untouched, as scoped (`git diff --stat -- evals` empty).

---

## Success Criteria Verification

Re-verified at the branch tip (`8f6da7f`) from the execution worktree during close, in addition to the executor's evidence.

### Criterion 1: npm output keys in both twins, non-npm unchanged

**Verification Method:** Step 1 tests; ad hoc parity check; consistency script field check.
**Evidence:** `tests` Ran 23 OK; consistency script asserts `trustedPublisher`, `provenance`, `previousVersion`, `removedVersions`, `publisher`, `daysSincePublish`, `installScripts` in Python npm output and named in docs. Twins: identical key set and order for the drift fixture.
**Result:** PASS

### Criterion 2: Tests: 23 OK with pwsh, OK with PowerShell skipped without

**Verification Method:** `python3 -m unittest discover -s tests -p "test_*.py"`.
**Evidence:** Executor, pwsh 7.4.6 on PATH: `Ran 23, OK`. Close re-run (pwsh absent): `Ran 23 tests ... OK (skipped=8)`.
**Result:** PASS

### Criterion 3: One §4.6 heading, V1-V5 in order, one §4.3 heading directly before

**Verification Method:** Consistency script.
**Evidence:** Close re-run printed `OK` (asserts heading counts, bullet order, `Blocking CVE boundary` absent).
**Result:** PASS

### Criterion 4: Tier 1 rule (addendum table + workflow list)

**Verification Method:** Consistency script Tier 1/3 asserts; traces R9, R12, R13.
**Evidence:** `OK`: `| Identity (§4.6 V2) | Not required`; "No change of signer, trusted-publisher config or publisher from the previous release"; `daysSincePublish` ≥ 7; workflow "is **not** required"; "publisher change" in both Tier 3 lists; old identity wordings absent; V2 wording "never enough on its own for Tier 1 or" kept.
**Result:** PASS

### Criterion 5: `§4.6 V<n>` references valid; documented script fields exist

**Verification Method:** Consistency script.
**Evidence:** `OK`; 13 workflow references to V1-V5.
**Result:** PASS

### Criterion 6: Stale phrases gone

**Verification Method:** Consistency script stale list (13 phrases); Step 2-4 greps.
**Evidence:** Count 0 in all three doc files.
**Result:** PASS

### Criterion 7: Eval harness green

**Verification Method:** `evals` unittest, `run_evals.py validate`, `git diff --stat -- evals`.
**Evidence:** Close re-run: `Ran 12 tests ... OK`; `validate` exit 0; evals diff empty (executor).
**Result:** PASS

### Criterion 8: Diff scope

**Verification Method:** `git diff --stat 3668e62..projex/...`; `git diff -U0 references/registries.md`.
**Evidence:** The 6 shipped files plus the log and plan status (projex documents); `registries.md` hunks start at L6, 11, 14, 20, 23, 26, 29, 32, 38.
**Result:** PASS

### Criterion 9: Paper traces produce stated outcomes

**Verification Method:** Executor traced R1-R13 against the final text, citing the rule per hop (log, Completion entry).
**Evidence:** R1/R2 chalk APPROVED reachable (never-used identity = note only); R3 TanStack shape CONDITIONAL on V1 cooldown; R4 Tier 3 + install previous release; R5 lodash@4.17.20 CONDITIONAL; R6 KEV dependency REJECTED / non-KEV CONDITIONAL; R7 unfixed HIGH REJECTED; R8 npm 12 native addon CONDITIONAL "approve only this package, pinned"; R9 prettier Tier 2 (< 7 d) / Tier 1 (>= 7 d), APPROVED reachable; R10 `.pth` HIGH, persistence REJECTED; R11 Go `GONOSUMDB` flagged; R12 lodash 4.18.1 Tier 1 APPROVED; R13 publisher change Tier 3.
**Result:** PASS (R11 wording nit, see Deviations)

### Acceptance Criteria Summary

| Criterion | Method | Result | Evidence |
|-----------|--------|--------|----------|
| npm fields in both twins | tests + parity | Pass | 23 OK |
| Test counts | unittest | Pass | 23 OK (8 skipped without pwsh) |
| §4.6 / §4.3 headings | consistency script | Pass | `OK` |
| Tier 1 rule | consistency script + R9/R12/R13 | Pass | `OK` |
| V refs and fields | consistency script | Pass | `OK` |
| Stale phrases | consistency script | Pass | 0 |
| Eval harness | unittest + validate | Pass | 12 OK; exit 0 |
| Diff scope | diff stat + hunks | Pass | 6 shipped files; hunks L6-38 |
| Paper traces | log trace table | Pass | R1-R13 match |

**Overall:** 9/9 criteria passed.

---

## Deviations from Plan

### Deviation 1: Size estimates low
- **Planned:** addendum ~27 KB; workflow +~3 KB.
- **Actual:** addendum 30,112 B (17,237 -> 30,112); workflow 26,589 B (+3,388 B).
- **Reason:** plan estimates were rough; the After text is applied verbatim.
- **Impact:** None on content; read cost on every registry audit is ~3 KB above estimate (the plan's "read cost" risk).
- **Recommendation:** None; the STEWARDSHIP review can trim.

### Deviation 2: Byte-based line-width check
- **Planned:** `awk length > 80` check on workflow lines.
- **Actual:** flags 2 lines because `→` / `≥` are multi-byte; a character-count check finds none over 78.
- **Impact:** None. Recommendation: use a character-aware check in future plans.

### Deviation 3: R11 wording nit
- **Planned:** R11 expects the Recommendation "remove pattern for public modules".
- **Actual:** the addendum Go trust row and `registries.md` Go line flag a `GONOSUMDB` / `GOPRIVATE` pattern covering public modules; the "remove the pattern" recommendation is implied by that row, not stated as its own sentence.
- **Impact:** Minor. Flag is raised; phrasing follows the plan's After text.
- **Recommendation:** Optional wording patch.

### Deviation 4: Optional sub-subagents not used
- verify-projex / do-projex marked Encouraged only; no task-list tool in the environment. Verification done by self (tests, parity check, consistency script).

### Deviation 5: Completion commit lacks attribution trailers
- **Planned:** every branch commit carries the `Projex:` and attribution trailers.
- **Actual:** completion commit `8f6da7f` ("projex: complete registry-package-rubric-refresh") has no trailers; step commits `b39152d`, `50478c3`, `c2a08c1`, `eda463d` do.
- **Reason / handling:** commits are never amended or rewritten; the squash commit carries `Projex:` plus both attribution trailers and supersedes `8f6da7f`.

---

## Issues Encountered

None during execution. No stash used; no user interventions (mid-execution or post-plan). `.ps1` tests ran under pwsh 7.4.6 (executor); `pwsh` absent at close, so the PowerShell classes skipped in the close re-run.

---

## Key Insights

**Rationale promoted:** shipped docs already carry the load-bearing rationale: `references/criteria/registry-package.md` (Tier 1 rule, V1-V5 plug-ins, trust table) and the script comments in `scripts/registry-lookup.py` / `.ps1` (rejected alternatives named). The residual stolen-token risk lives only in the plan Notes -> Risks and this walkthrough; if STEWARDSHIP wants it in a shipped doc, promote it there.

### Lessons Learned

1. **Verbatim extractor for large Before/After plans**
   - Context: 47 edits across 4 files, ~1.5k-line plan.
   - Insight: a scratchpad helper that parses fenced Before/After pairs, requires exactly one match per Before and writes all-or-nothing removed transcription risk and made order dependencies (2f -> 2m) explicit.
   - Application: reuse for any plan authored as pre-simulated Before/After blocks.

2. **Pre-simulated plan + consistency script**
   - Context: plan carried an in-plan consistency script asserting headings, Tier 1/3 rules, stale phrases and doc-to-script field names.
   - Insight: the same script was runnable unchanged at execution and at close (`OK`), giving cheap, repeatable proof.
   - Application: keep consistency scripts as plan sections; extract with awk for close re-runs.

### Pattern Discoveries

1. **Docs and the data fields they cite ship together**
   - Observed in: Step 1 before Steps 2-3 (plan Split Decision).
   - Description: script output fields land before the docs that name them, and a consistency check ties both together.
   - Reuse potential: any rubric refresh that depends on new tool output.

### Gotchas / Pitfalls

1. **Byte vs character width checks**
   - Trap: `awk length` counts bytes under `LC_ALL=C`, so `→` / `≥` inflate line width.
   - How encountered: Step 3 width check flagged 2 lines.
   - Avoidance: character-aware check.

### Technical Insights

- Twins keep identical JSON keys and key order; PowerShell date handling (`Format-DateStr` culture round-trip) is existing behaviour, pinned for Python by test.
- PowerShell tests skip silently without pwsh; a green run without it does not prove `.ps1` parity.

---

## Recommendations

### Immediate Follow-ups
- [ ] Eval refresh plan: new registry cases (fresh version, TP/provenance drop, npm 12 script approval, `.pth` / `binding.gyp`, KEV dependency REJECTED vs non-KEV CONDITIONAL, own-code unfixed HIGH, non-npm cases, PyPI quarantine) plus Tier 1 cases from the human decision (R12 / R13 shapes). See plan Notes -> Eval hand-off.
- [ ] RP-8 Scorecard host patch (`api.securityscorecards.dev`): still pending verification.
- [ ] STEWARDSHIP dates for registry-package (Last Reviewed 2026-10-16, Next Due 2027-01-14) and F-P1 watch list; orchestrator-owned.

### Future Considerations
- Tooling follow-on: PyPI `provenance` / `project-status`, RubyGems `-Version` support (`lookup_rubygems` always reports latest), optional KEV flag in `vuln-lookup`.
- Product facts age fast (npm 12 / pnpm 12 / Yarn 4.18 at planning); each row carries a "Since" version for the review.
- Adoption bars are policy; crates/gems/NuGet rest on top-package sanity data, npm/PyPI bars unvalidated.
- Navigation `2604070218-install-auditor-subject-typed-redesign-nav.md`: Phase 6 is continuous; no closure candidate.

### Plan Improvements
- Success criterion said "Paper traces R1-R10" while the table held R1-R13; align counts after revisions.
- Use character-aware width checks; give size estimates with headroom.
- State the R11 recommendation sentence in the After text if it is required.

---

## Related Projex Updates

### Documents to Update
| Document | Update Needed |
|----------|---------------|
| `2610162010-registry-package-rubric-refresh-plan.md` | Status Complete; Completed / Walkthrough / Log links; moved to closed |
| `2610162010-registry-package-rubric-refresh-log.md` | Status Complete (already); moved to closed |
| `2604070218-install-auditor-subject-typed-redesign-nav.md` | Recent Progress, Phase 6 checklist, Revision Log, Last Revised; all 10 subject rubric refreshes + shared floor now closed |
| `2610161927-registry-package-and-ci-action-stewardship-review-eval.md` | Left active (RP-8 patch, tooling follow-on and eval refresh still open; no plan link to update) |

### New Projex Suggested
| Type | Description |
|------|-------------|
| Plan | Eval refresh for registry-package (cases above) |
| Patch | RP-8 Scorecard host verification and fix |
| Plan | registry-lookup tooling follow-on (PyPI provenance, RubyGems `-Version`, KEV flag) |

---

## Appendix

### Execution Log
See `2610162010-registry-package-rubric-refresh-log.md`.

### Test Output
```
tests (close re-run, no pwsh):  Ran 23 tests in 0.082s  OK (skipped=8)
evals unittest:                 Ran 12 tests in 0.068s  OK
evals validate:                 exit 0
plan consistency script:        OK
sizes (B):                      30112 criteria/registry-package.md | 26589 workflows/registry-package.md | 6176 references/registries.md
```

### References
- Commits on `projex/2610162010-registry-package-rubric-refresh`: `b39152d` (step 1), `50478c3` (step 2), `c2a08c1` (step 3), `eda463d` (step 4), `8f6da7f` (completion). Base start commit `3668e62`; floor `20843cc`; siblings on base `8564410`.
- Parent review: `2610161927-registry-package-and-ci-action-stewardship-review-eval.md`
- Floor: `2610161941-shared-version-integrity-floor-walkthrough.md`
