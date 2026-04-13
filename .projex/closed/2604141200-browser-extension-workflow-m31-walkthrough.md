# Walkthrough: Browser Extension Workflow — M3.1

> **Execution Date:** 2026-04-14
> **Completed By:** Claude (Sonnet 4.6)
> **Source Plan:** [2604141200-browser-extension-workflow-m31-plan.md](2604141200-browser-extension-workflow-m31-plan.md)
> **Duration:** Single session (~25 min)
> **Result:** Success

---

## Summary

Created the browser-extension subject-specific audit pipeline: criteria addendum, workflow file, dispatch table wiring, and three eval cases. All six acceptance criteria passed. No deviations from plan.

---

## Objectives Completion

| Objective | Status | Notes |
|-----------|--------|-------|
| Create `references/criteria/browser-extension.md` | Complete | 163 lines, all 6 required sections |
| Create `workflows/browser-extension.md` | Complete | 369 lines, all 4 template sections |
| Wire dispatch table row 2 | Complete | Single line edit, SKILL.md:63 |
| Update Wappalyzer eval (id 1) | Complete | Added browser-extension assertion + updated expected_output |
| Add new eval case id 10 (YouTube downloader) | Complete | Tier 3, REJECTED/CONDITIONAL |
| Add new eval case id 11 (uBlock Origin) | Complete | Tier 1, APPROVED |

---

## Execution Detail

### Step 1: Create references/criteria/browser-extension.md

**Planned:** New file following `registry-package.md` pattern with browser-extension-specific scoring vocabulary.

**Actual:** Created exactly as specified. Six sections: Store Trust Signals, Permission Risk Classification (high/medium/low tiers with scoring impact rules), Manifest Version (MV2/MV3), Content Script Reach, Auto-Update Risk, Tier Assignment Thresholds.

**Deviation:** None.

**Files Changed:**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `references/criteria/browser-extension.md` | Created | Yes | 163 lines |

**Verification:** File exists at correct path. All six sections present per plan checklist.

---

### Step 2: Create workflows/browser-extension.md

**Planned:** Type 2 workflow following Identify / Evidence / Subject Rubric / Subject Verdict Notes template, mirroring registry-package.md structure with browser-extension-native content.

**Actual:** Created as specified. Identify (store identity + metadata extraction + required context), Evidence Part A (tier triage with Tier 1/2/3 scope descriptions), Evidence Part B (core research questions, store listing inspection, manifest analysis keys, incident search queries, source code review guidance, audit coverage tracking table), Subject Rubric (§4.1–4.6 all browser-extension-specialized), Subject Verdict Notes (toward REJECTED / CONDITIONAL / APPROVED with concrete trigger lists).

**Deviation:** None. The `### Audit coverage tracking` subsection in Evidence Part B appeared to trigger the "no Audit Coverage section" check during verification but is a guidance subsection for evidence collection — not the dispatcher-owned `## Audit Coverage` table. See Issues Encountered.

**Files Changed:**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `workflows/browser-extension.md` | Created | Yes | 369 lines |

**Verification:** File exists. All four template sections present. No `## Audit Coverage` heading (dispatcher-owned section absent). References `references/criteria/browser-extension.md` by path. Does not duplicate audit-confidence assertion.

---

### Step 3: Update SKILL.md dispatch table

**Planned:** Change row 2 from `workflows/generic.md` (Fallback) to `workflows/browser-extension.md` (Live — Phase 3 M3.1). Single line at SKILL.md:63.

**Actual:** Edit applied exactly as planned.

**Deviation:** None.

**Files Changed:**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `SKILL.md` | Modified | Yes | Line 63: `generic.md` → `browser-extension.md`, status updated |

**Verification:** `grep "browser-extension" SKILL.md` shows `| 2 | browser-extension | \`workflows/browser-extension.md\` | Live — Phase 3 (M3.1) |`.

---

### Step 4: Update evals/evals.json

**Planned:** (4a) Add browser-extension assertion to id 1 + update expected_output. (4b) Add id 10. (4c) Add id 11.

**Actual:** All three sub-steps executed as specified. Total eval count: 12 (ids 0–11). Three browser-extension cases cover Tier 1 (id 11), Tier 2 (id 1), and Tier 3 (id 10).

**Deviation:** None.

**Files Changed:**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `evals/evals.json` | Modified | Yes | +29/-2 lines: id 1 updated, ids 10+11 added |

**Verification:** `python3 -c "import json; json.load(...)"` → valid. IDs 0–11 present.

---

## Complete Change Log

> **Derived from:** `git diff --stat master..projex/2604141200-browser-extension-workflow-m31`
> 6 files changed, 618 insertions(+), 3 deletions(-)

### Files Created
| File | Purpose | Lines | In Plan? |
|------|---------|-------|----------|
| `references/criteria/browser-extension.md` | Browser-extension scoring addendum | 163 | Yes |
| `workflows/browser-extension.md` | Type 2 subject-specific audit workflow | 369 | Yes |
| `.projex/2604141200-browser-extension-workflow-m31-log.md` | Execution log | 54 | Yes (structural) |

### Files Modified
| File | Changes | Lines Affected | In Plan? |
|------|---------|----------------|----------|
| `SKILL.md` | Dispatch table row 2: `generic.md` → `browser-extension.md` | 1 line (~line 63) | Yes |
| `evals/evals.json` | id 1 updated; ids 10, 11 added | +29/-2 | Yes |
| `.projex/2604141200-browser-extension-workflow-m31-plan.md` | Status: Ready → Complete | 1 line | Yes (structural) |

### Planned But Not Changed
None — all planned files were changed as specified.

---

## Success Criteria Verification

### Acceptance Criteria Summary

| Criterion | Method | Result | Evidence |
|-----------|--------|--------|----------|
| `workflows/browser-extension.md` exists with 4 template sections | Read file, check headers | **PASS** | Identify / Evidence / Subject Rubric / Subject Verdict Notes all present |
| `references/criteria/browser-extension.md` exists | File existence check | **PASS** | File at correct path, 163 lines |
| SKILL.md row 2 routes to `workflows/browser-extension.md` | grep SKILL.md | **PASS** | `\| 2 \| browser-extension \| \`workflows/browser-extension.md\` \| Live — Phase 3 (M3.1) \|` |
| Wappalyzer eval (id 1) assertions still compatible | Trace assertions against new workflow output | **PASS** | All 7 assertions satisfiable; new workflow produces superset of expected findings |
| ≥1 new browser-extension eval case added | Count cases in evals.json | **PASS** | 2 new cases (ids 10, 11); 3 total browser-extension cases |
| No regressions in ids 0, 2–9 | Compare to pre-edit state | **PASS** | Byte-identical except id 1 assertion addition |

**Overall: 6/6 criteria passed.**

---

## Issues Encountered

### Issue 1: False-positive on Audit Coverage grep check
- **Description:** Verification check #3 used case-insensitive grep for "audit coverage" in `workflows/browser-extension.md` and flagged matches. Initial output showed "FAIL - found dispatcher-owned section."
- **Severity:** Low
- **Resolution:** Re-ran grep with anchored pattern `^## Audit Coverage` (exact heading). 0 matches. The workflow contains a `### Audit coverage tracking` subsection (lowercase, third-level heading) in Evidence Part B that guides evidence collection for the dispatcher's table — it is not a duplicate of the dispatcher's `## Audit Coverage` section. All three matches from the case-insensitive grep were legitimate: (1) header comment stating dispatcher ownership, (2) the guidance subsection, (3) a reference directing the agent to SKILL.md.
- **Prevention:** Use anchored pattern `^## Audit Coverage` rather than case-insensitive substring match for this check.

---

## Key Insights

### Pattern Discoveries

1. **Audit coverage tracking subsection is workflow-internal scaffolding**
   - Observed in: `workflows/browser-extension.md` Evidence Part B
   - Description: Each subject-specific workflow should include a coverage tracking table mapping checks to tier requirements — this is separate from the dispatcher-owned `## Audit Coverage` output table. The workflow's table is a _planning_ artifact; the dispatcher's section is the _output_ artifact.
   - Reuse potential: All future Phase 3/4 subject-specific workflows (container-image, ci-action, ide-plugin, etc.) should follow this same pattern.

2. **Permission taxonomy is the core browser-extension contribution**
   - The criteria addendum's Permission Risk Classification (high/medium/low with explicit scoring rules) was the main gap identified in the framing eval. This is what differentiates the browser-extension workflow from generic.md — not the store lookup or verdict structure, but the permission risk vocabulary.

### Gotchas / Pitfalls

1. **Worktree plan file starts at pre-"In Progress" state**
   - Trap: The worktree branches from master at the "Ready" commit, before the "In Progress" status was committed on master. The plan file in the worktree still reads "Ready" and needs to be updated to "Complete" directly.
   - How encountered: Tried to edit "In Progress" → "Complete" but the worktree copy said "Ready".
   - Avoidance: After updating plan status to "In Progress" on master, remember the worktree has the older state — edit to "Complete" directly rather than from "In Progress".

---

## Recommendations

### Immediate Follow-ups
- [ ] Update `2604070218-install-auditor-subject-typed-redesign-nav.md` to mark M3.1 complete
- [ ] Run eval suite against the three browser-extension cases (ids 1, 10, 11) to confirm assertions are satisfiable in practice

### Future Considerations
- Phase 3 next: M3.2 container-image workflow — can reuse this walkthrough as pattern
- Future enhancement: Chrome Web Store store-lookup script (deferred from M3.1 per plan scope)
- Verification check improvement: anchor `^## Audit Coverage` pattern rather than case-insensitive substring search

---

## Related Projex Updates

### Documents to Update
| Document | Update Needed |
|----------|---------------|
| `2604070218-install-auditor-subject-typed-redesign-nav.md` | Mark M3.1 as complete in Phase 3 milestone list |

### New Projex Suggested
| Type | Description |
|------|-------------|
| Plan | M3.2 container-image workflow (next Phase 3 milestone) |
