# Walkthrough: ci-action Rubric Refresh

> **Execution Date:** 2026-10-16
> **Completed By:** Claude (executor subagent) | closed by close-projex subagent
> **Source Plan:** 2610162005-ci-action-rubric-refresh-plan.md
> **Parent:** 2610162005-ci-action-rubric-refresh-plan.md
> **Duration:** ~24 min (20:20-20:44 per execution log timestamps)
> **Result:** Success

---

## Summary

ci-action rubric refreshed for the 2025-26 CI threat model and plugged into the shared §4.6 floor. `workflows/ci-action.md` 7,775 → 11,028 B (16 replacements). `references/criteria/ci-action.md` 7,322 → 17,115 B (14 replacements; new `## CVE Scope (§4.3)`, `## Runtime & Pin Freshness`, `## Version & Update Integrity (§4.6)`, `## Static Analysis Helper (optional, Tier 2/3)`). `references/registries.md` §CI/CD 4,413 → 4,681 B (2 line edits). All 32 anchors matched once; every size equals the plan's simulation (delta 0); consistency script `OK`.

---

## Objectives Completion

| Objective | Status | Notes |
|-----------|--------|-------|
| CI-1 cache trust, OIDC token reach, `run:`/`container:` tools, PR-head checkout patterns | Complete | Trigger matrix rows + scoring (cache writer/restorer chain CRITICAL, `cache-mode: write` HIGH, `allow-unsafe-pr-checkout` CRITICAL when executed); workflow Tier 3, research, verdict notes |
| CI-2 immutable releases | Complete | Ref Immutability Matrix row 3; `gh release verify`; V2 plug-in |
| CI-3 workflow lockfiles / SHA-pinning policy | Complete | `actions.lock` in matrix, transitive note, V5 |
| CI-4 pin freshness | Complete | `## Runtime & Pin Freshness`; APPROVED shape names update control |
| CI-5 `runs.using` runtime check | Complete | Runtime table; workflow §4.5 pointer |
| CI-6 `pull_request_target` semantics | Complete | Note paragraph; risk unchanged |
| CI-8 static-analysis helper | Complete | Optional, pinned, Tier 2/3 |
| Impostor-commit SHAs | Complete | Matrix row 2 "treat as an unknown ref"; reachability check; Tier 1 bullet |
| Contract: §4.6 plug-in, §4.3 line, header carve-outs | Complete | `except for §4.6` once in each file |
| RP-6 (CI line) registries alignment | Complete | Critical rule aligned to Red Flag, hard-coded SHA removed; unverified row `Medium-Low` |

---

## Execution Detail

> Derived from `git log`/`git diff` of `888ff74..projex/2610162005-ci-action-rubric-refresh` (branch point) and the execution log.

### Preflight

**Planned:** shared-floor contract greps, baselines, verify A4.
**Actual:** `20843cc` reachable; §4.6 heading 1, `### V[1-5]` 5, `Addendum plug-ins` 1, `Audit tooling is itself a dependency` 1, Red Flag 1. Baselines 7,775 / 7,322 / 4,413 B. `validate` 41 evals / 248 assertions; unittest evals 12 OK; tests 19 OK (6 skipped). A4 verified in `github/docs` (`oidc.md`): `ACTIONS_ID_TOKEN_REQUEST_URL` / `_TOKEN` are runner environment variables, so any step in the job can request the OIDC token. Commit `43b0512`.
**Deviation:** None.

### Step 1: `workflows/ci-action.md`

**Planned:** 16 replacements 1a-1p.
**Actual:** 16/16 matched once. `except for` 1; `allow-unsafe-pr-checkout` 3; `cache-mode` 3; `§4.6` 5; `actions.lock` 1; `gh release verify` 1. 11,028 B. Non-table lines > 80 columns = 4, all pre-existing (lines 40, 138, 234, 252 of the result). Commit `7529979`.
**Deviation:** None.

### Step 2: `references/criteria/ci-action.md`

**Planned:** 14 replacements 2a-2n.
**Actual:** 14/14 matched once (2c and the 2f row block as multi-line edits). One §4.6 heading with V1-V5; CVE Scope, Runtime & Pin Freshness, Static Analysis Helper headings once each; `except for §4.6` 1; `cache-mode` 4; `actions.lock` 4; `allow-unsafe-pr-checkout` 1; `gh release verify` 2. 17,115 B. Commit `007c97a`.
**Deviation:** None.

### Step 3: `references/registries.md` §CI/CD

**Planned:** 3a unverified row to `Medium-Low`; 3b Critical rule aligned to the Red Flag.
**Actual:** both applied; the hard-coded SHA and `Any action that accesses` text gone (0 hits); `Mutable CI ref with privileged access` 1; `Medium-Low — pin to SHA` 1; 4,681 B. The registry-package sibling plan had not landed, so no fallback was needed. Commit `f65f345`; completion commit `4bcc127`.
**Deviation:** None.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `workflows/ci-action.md` | Modified | Yes | 16 hunks, lines 27-265: header carve-out, Tier 1/3 bullets, research questions, runtime pointer, REJECTED/CONDITIONAL/APPROVED verdict notes; 73 lines changed |
| `references/criteria/ci-action.md` | Modified | Yes | 14 hunks, lines 6-265: header carve-out, ref matrix, trigger matrix and scoring, Runtime & Pin Freshness, CVE Scope, §4.6 plug-in, Static Analysis Helper (new tail, lines ~208-265) |
| `references/registries.md` | Modified | Yes | Lines 79 and 85 (CI/CD table row and Critical rule) |

---

## Complete Change Log

> **Derived from:** `git diff --stat 888ff74..projex/2610162005-ci-action-rubric-refresh`: 5 files changed, 288 insertions(+), 19 deletions(-) (including projex documents).

### Files Created
| File | Purpose | Lines | In Plan? |
|------|---------|-------|----------|
| `.projex/2610162005-ci-action-rubric-refresh-log.md` | Execution log | 95 | Yes (implicit) |
| `.projex/closed/2610162005-ci-action-rubric-refresh-walkthrough.md` | This walkthrough | - | Yes (close) |

### Files Modified
| File | Changes | Lines Affected | In Plan? |
|------|---------|----------------|----------|
| `workflows/ci-action.md` | 16 replacements | 73 changed; 11,028 B | Yes |
| `references/criteria/ci-action.md` | 14 replacements | 132 changed; 17,115 B | Yes |
| `references/registries.md` | 2 lines | +2/-2; 4,681 B | Yes |
| `.projex/2610162005-ci-action-rubric-refresh-plan.md` | Status Complete, Log, Walkthrough link | 3 lines | Yes (close) |

### Files Deleted
None.

### Planned But Not Changed
None. `SKILL.md` (Red Flag "Mutable CI ref with privileged access" untouched), `references/criteria.md`, `evals/`, `STEWARDSHIP.md` untouched, as scoped.

---

## Success Criteria Verification

| Criterion | Method | Result | Evidence |
|-----------|--------|--------|----------|
| Addendum headings: one §4.6 (5 V-bullets), CVE Scope, Runtime & Pin Freshness, Static Analysis Helper | grep + consistency script | Pass | all once; V1-V5 = 5 |
| `grep -c "except for"` = 1 in each file | grep | Pass | 1 / 1 |
| `§4.6 V<n>` and `addendum §<Name>` references resolve | consistency script | Pass | `OK` |
| New strings present with required counts | grep | Pass | 3/1, 3/4, 1/4, 1/2 |
| `registries.md` no longer has the hard-coded SHA / `Any action that accesses`; names the Red Flag | grep | Pass | 0 / 0 / 1 |
| `SKILL.md` untouched | `git diff --stat` | Pass | no change |
| Sizes within ±150 B of simulation | `wc -c` | Pass | 11,028 / 17,115 / 4,681 (delta 0) |
| New workflow prose lines ≤ 80 columns | awk | Pass | only the 4 pre-existing longer lines |
| `validate` + unittest with Preflight count | harness | Pass | 41 / 248; evals 12 OK; tests 19 OK (6 skipped) |
| Paper traces T1-T11 | manual walk | Pass | all match (log "Full verification"); tag SHAs spot-checked with `git ls-remote` |
| `git diff --stat` lists exactly the 3 files (+ projex docs) | diff | Pass | 3 shipped files + log + plan |

**Overall:** 11/11 criteria passed.

---

## Deviations from Plan

### Deviation 1: No task tool, no verifier sub-subagents
- **Planned:** per-step task tracking; Verify-Projex / Do-Projex Encouraged.
- **Actual:** tracked via log and per-step commits; self-executed and self-verified.
- **Reason:** no task or spawn tool available at the executor's depth.
- **Impact:** none; byte-exact size equality with the simulation supports verbatim application.
- **Recommendation:** none.

### Deviation 2: Trailers added to every commit; base start-execution commit amended once
- **Planned:** n/a (orchestrator-requested trailers).
- **Actual:** `Co-Authored-By` / `Claude-Session` trailers added to every execution commit, including doc-only ones. The executor amended the base start-execution commit once (`b97cbb4` → `888ff74`, unpushed, then HEAD) to add them.
- **Reason:** orchestrator request.
- **Impact:** none on content; the amend happened before this close. This close did not amend or rewrite any commit.
- **Recommendation:** none.

---

## Issues Encountered

### Issue 1: `gh api` refused for A4 verification
- **Description:** `gh api` was refused (session-bound repos).
- **Severity:** Low
- **Resolution:** sparse shallow clone of `github/docs` served the read; removed at cleanup (outside the repo).

### Issue 2: Roadmap nav and registries overlap at close
- **Description:** other closes landed on base during and after this execution (including the IDE close, which edits other rows of `references/registries.md`).
- **Severity:** Low
- **Resolution:** `references/registries.md` merged cleanly (different hunks: IDE rows ~line 72, CI rows 79/85). Nav add/add conflicts resolved by keeping both sides.

### Close notes
- Nav `2604070218-install-auditor-subject-typed-redesign-nav.md` updated in the close commit, following earlier rubric-refresh closes (plan carries no `Nav:` field).
- Observation (unchanged): trace T5 lists "Tier 2+" in the plan table while the workflow lists `id-token: write` as a Tier 3 trigger; workflow text governs, verdict unaffected.

---

## Key Insights

**Rationale promoted:** none needed. Rationale ships in the addendum text; no shipped file carries projex references (grep clean).

### Lessons Learned

1. **A SHA pin is not a safety guarantee over time**
   - Context: SHA pins miss backported safety fixes (e.g. `actions/checkout` fork-checkout refusal) and Dependabot alerts skip SHA-pinned actions.
   - Insight: APPROVED needs an update control (Dependabot/Renovate cooldown, `actions.lock`) in the Recommendation.
   - Application: `## Runtime & Pin Freshness` and V5.

### Gotchas / Pitfalls

1. **Impostor commits**
   - Trap: a SHA from the fork network passes as "full SHA".
   - Avoidance: reachability check in the ref matrix; treat unreachable SHAs as unknown refs (Red Flag in a privileged job).

2. **Cache write → privileged restore chain**
   - Trap: a job processing untrusted input writes a cache restored by a release or `id-token: write` job (TanStack shape).
   - Avoidance: trigger matrix rows; CRITICAL for the chain.

---

## Recommendations

### Immediate Follow-ups
- [ ] Eval refresh plan: EV-1, EV-2 and new ci-action cases (plan Notes → Eval hand-off).
- [ ] STEWARDSHIP: ci-action Last Reviewed 2026-10-16, Next Due 2027-02-13.
- [ ] Orchestrator: align the §4.3 plug-in heading across addenda (`## CVE Scope (§4.3)` here); consider the two optional `SKILL.md` wording follow-ups listed in the plan's Notes.
- [ ] Registry-package plan (`2610162010-registry-package-rubric-refresh-plan.md`) owns the remaining non-CI `references/registries.md` rows; it should rebase over this close.

### Future Considerations
- Non-GitHub Type 5 depth (GitLab CI/CD Catalog components, CircleCI orb tiers) not re-researched.
- A5 (`gh release verify -R` form) was not exercised offline; wording kept as planned.

### Plan Improvements
- Make the T5 tier note in the plan table match the workflow (`id-token: write` = Tier 3).

---

## Related Projex Updates

### Documents to Update
| Document | Update Needed |
|----------|---------------|
| `2610162005-ci-action-rubric-refresh-plan.md` | Status Complete; Walkthrough link; moved to closed |
| `2610162005-ci-action-rubric-refresh-log.md` | Moved to closed |
| `2604070218-install-auditor-subject-typed-redesign-nav.md` | Recent Progress, checklist, Revision Log, Last Revised |
| `2610161927-registry-package-and-ci-action-stewardship-review-eval.md` | Left active (registry-package plan still pending) |

### New Projex Suggested
| Type | Description |
|------|-------------|
| Plan | Eval refresh covering ci-action EV-1, EV-2 and new cases |

---

## Appendix

### References
- Execution commits: `43b0512` (preflight), `7529979` (step 1), `007c97a` (step 2), `f65f345` (step 3), `4bcc127` (complete)
- Execution log: `2610162005-ci-action-rubric-refresh-log.md`
