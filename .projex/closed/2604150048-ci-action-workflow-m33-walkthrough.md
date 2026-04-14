# Walkthrough: CI Action Workflow - M3.3

> **Execution Date:** 2026-04-15
> **Completed By:** Codex (GPT-5)
> **Source Plan:** [2604150048-ci-action-workflow-m33-plan.md](2604150048-ci-action-workflow-m33-plan.md)
> **Duration:** Single session (~10 min)
> **Result:** Success

---

## Summary

Created the Type 5 ci-action audit pipeline: criteria addendum, workflow file, dispatcher wiring, and two eval cases. All success criteria passed. The only caveat was verification depth for regressions: no runnable local eval harness was present, so regression checking used JSON validation plus preservation of ids 0-13.

---

## Objectives Completion

| Objective | Status | Notes |
|-----------|--------|-------|
| Create `references/criteria/ci-action.md` | Complete | 141 lines; publisher trust, pinning, trigger/secret, implementation-type, transitive-depth, and tier guidance |
| Create `workflows/ci-action.md` | Complete | 219 lines; all 4 required sections present |
| Route Type 5 through `SKILL.md` | Complete | Row 5 now points to `workflows/ci-action.md`; 2 new reference-file bullets added |
| Add Type 5 eval coverage | Complete | ids 14 and 15 added |
| Preserve prior eval coverage | Complete | ids 0-13 unchanged; `evals/evals.json` parses cleanly |

---

## Execution Detail

### Step 1: Create `references/criteria/ci-action.md`

**Planned:** Add a Type 5 criteria addendum covering publisher trust, immutable refs, trigger/secret exposure, implementation types, transitive depth, and tier thresholds.

**Actual:** Created exactly that addendum. The file is GitHub Actions-first in v1 but maps the same trust concepts to reusable workflows, GitLab CI components, and CircleCI orbs.

**Deviation:** None.

**Files Changed:**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `references/criteria/ci-action.md` | Created | Yes | 141 lines |

**Verification:** Reviewed headings and content. Required sections are present and internally consistent.

---

### Step 2: Create `workflows/ci-action.md`

**Planned:** Add the Type 5 workflow using the established Identify / Evidence / Subject Rubric / Subject Verdict Notes template.

**Actual:** Created the workflow with GitHub Actions-first depth. It covers subject class extraction, trigger and permission context, implementation types, transitive `uses:` review, and verdict guidance for `pull_request_target`, `secrets: inherit`, mutable refs, and self-hosted runners.

**Deviation:** None.

**Files Changed:**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `workflows/ci-action.md` | Created | Yes | 219 lines |

**Verification:** `rg -n "^## " workflows/ci-action.md` confirmed the 4 required sections. The file does not duplicate the dispatcher-owned final report section.

---

### Step 3: Update `SKILL.md`

**Planned:** Route Type 5 to the new workflow and add the new workflow/addendum to `Reference Files`.

**Actual:** Applied both edits. Type 5 is now live via `workflows/ci-action.md`, and the reference-file list includes the workflow plus criteria addendum.

**Deviation:** None.

**Files Changed:**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `SKILL.md` | Modified | Yes | Row 5 route changed; 2 reference-file bullets added |

**Verification:** `rg -n "ci-action|workflows/ci-action.md|references/criteria/ci-action.md" SKILL.md` matched the live route and both new bullets.

---

### Step 4: Update `evals/evals.json`

**Planned:** Add one positive SHA-pinned Type 5 case and one negative privileged/transitive Type 5 case.

**Actual:** Added id 14 (`actions/checkout` pinned to a full SHA with read-only permissions) and id 15 (cross-org reusable workflow with `pull_request_target`, `secrets: inherit`, write scopes, and a transitive child pinned to `main`).

**Deviation:** None in content. Verification used JSON parsing plus diff preservation instead of actually running evals because no local eval harness was found.

**Files Changed:**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `evals/evals.json` | Modified | Yes | +30 lines; ids 14 and 15 added; ids 0-13 unchanged |

**Verification:** `python -c "import json; json.load(open('evals/evals.json', encoding='utf-8'))"` passed. IDs 14 and 15 exist. Diff review confirmed ids 0-13 were preserved.

---

## Complete Change Log

> **Derived from:** `git diff --stat master..HEAD`
> 6 files changed, 452 insertions(+), 2 deletions(-)

### Files Created
| File | Purpose | Lines | In Plan? |
|------|---------|-------|----------|
| `references/criteria/ci-action.md` | Type 5 scoring addendum | 141 | Yes |
| `workflows/ci-action.md` | Type 5 subject-specific workflow | 219 | Yes |
| `.projex/2604150048-ci-action-workflow-m33-log.md` | Execution log | 58 | Yes (structural) |

### Files Modified
| File | Changes | Lines Affected | In Plan? |
|------|---------|----------------|----------|
| `SKILL.md` | Row 5 route updated; 2 Type 5 reference-file bullets added | 4 lines | Yes |
| `evals/evals.json` | ids 14 and 15 appended | +30/-0 | Yes |
| `.projex/2604150048-ci-action-workflow-m33-plan.md` | Status updated to `Complete` | 1 line | Yes (structural) |

### Planned But Not Changed

None - all planned execution targets changed.

---

## Success Criteria Verification

### Acceptance Criteria Summary

| Criterion | Method | Result | Evidence |
|-----------|--------|--------|----------|
| `workflows/ci-action.md` exists with 4 template sections | Read file; grep headings | **PASS** | `Identify / Evidence / Subject Rubric / Subject Verdict Notes` present |
| `references/criteria/ci-action.md` exists with CI-specific scoring | Read file | **PASS** | Publisher trust, pinning, trigger/secret, implementation-type, transitive, and tier sections present |
| `SKILL.md` routes Type 5 correctly | Grep `SKILL.md` | **PASS** | Row 5 -> `workflows/ci-action.md`; Type 5 bullets added |
| Positive Type 5 eval exists | Read `evals/evals.json` | **PASS** | id 14 present |
| Negative Type 5 eval exists | Read `evals/evals.json` | **PASS** | id 15 present |
| No regressions in ids 0-13 | JSON validation + diff review | **PASS** | ids 0-13 preserved byte-for-byte; no local eval harness found |

**Overall: 6/6 criteria passed.**

---

## Deviations from Plan

### Deviation 1: Regression verification method
- **Planned:** Verify new eval coverage and no regressions in ids 0-13.
- **Actual:** Searched normal repo surfaces for a runnable eval harness and found none. Used JSON parsing, targeted diff review, and preservation of ids 0-13 instead.
- **Reason:** The repo contains `evals/evals.json` assertions but no local runner script, package manifest, or documented eval command.
- **Impact:** Low. Structural regression coverage is verified; end-to-end eval execution remains a future repo capability.
- **Recommendation:** Add or document an eval runner before expanding Phase 6 eval stewardship.

---

## Issues Encountered

### Issue 1: False start on eval-harness discovery
- **Description:** Initial harness search hit nonexistent root globs before being narrowed to actual repo surfaces.
- **Severity:** Low
- **Resolution:** Re-ran the search against tracked files/directories only. No runnable eval harness was found.
- **Time Impact:** Negligible
- **Prevention:** Search from actual tracked roots first when repos do not include top-level package manifests or READMEs.

---

## Key Insights

### Pattern Discoveries

1. **Type 5 risk is execution-context-first**
   - Observed in: `workflows/ci-action.md` and `references/criteria/ci-action.md`
   - Description: CI-action safety is driven more by trigger, token scope, secret flow, runner trust, and transitive execution than by publisher identity alone.
   - Reuse potential: Future Type 8/9 workflows can reuse this trust-boundary framing for secret-bearing automation.

2. **Transitive review depth needs explicit tiering**
   - Observed in: ci-action addendum + workflow
   - Description: “Inspect at least the first nested `uses:` layer” is the minimum rule that keeps composite actions and reusable workflows from hiding mutable child risk.
   - Reuse potential: Can be lifted into future automation-oriented workflows and stewardship docs.

### Gotchas / Pitfalls

1. **Eval files can exist without an executable harness**
   - Trap: `evals/evals.json` implies runnable coverage, but a repo may only store test vectors plus assertions.
   - How encountered: Verification found the JSON schema and assertions but no local command to execute them.
   - Avoidance: Treat harness discovery as its own verification gate and log the fallback clearly.

---

## Recommendations

### Immediate Follow-ups
- [ ] Update `2604070218-install-auditor-subject-typed-redesign-nav.md` to mark M3.3 complete and point Phase 3 focus to M3.4
- [ ] Consider documenting or adding a local eval runner before Phase 6 expands eval bundles further

### Future Considerations
- M3.4 (`workflows/ide-plugin.md`) can reuse the same Phase 3 structure: addendum, workflow, dispatch route, eval coverage
- Type 5 may eventually justify a helper script for transitive `uses:` extraction if manual inspection becomes too slow or inconsistent

---

## Related Projex Updates

### Documents to Update
| Document | Update Needed |
|----------|---------------|
| `2604070218-install-auditor-subject-typed-redesign-nav.md` | Mark M3.3 complete; link walkthrough; shift current focus to M3.4 |

### New Projex Suggested
| Type | Description |
|------|-------------|
| Plan | M3.4 ide-plugin workflow |

