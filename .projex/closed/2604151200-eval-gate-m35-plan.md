# Eval Gate Closeout — Phase 3 M3.5

> **Status:** Complete
> **Created:** 2026-04-15
> **Completed:** 2026-04-15
> **Author:** Claude (Opus 4.6)
> **Source:** 2604070218-install-auditor-subject-typed-redesign-nav.md (Phase 3 M3.5)
> **Related Projex:** 2604070217-subject-typed-audit-dispatch-eval.md (eval §6 G3, §9 phase 6), 2604070218-install-auditor-subject-typed-redesign-nav.md
> **Walkthrough:** 2604151200-eval-gate-m35-walkthrough.md
> **Worktree:** No

---

## Summary

Verify that all four Phase 3 subject workflows have ≥1 positive + ≥1 negative eval case in `evals/evals.json`, validate structural integrity of the eval file, and update the navigation document to mark M3.5 complete and Phase 3 closed. This is a review/confirmation gate — no new workflows or eval cases are authored.

**Scope:** `evals/evals.json` (read-only verification) + `.projex/2604070218-install-auditor-subject-typed-redesign-nav.md` (status update)
**Estimated Changes:** 1 file edited (nav doc)

---

## Objective

### Problem / Gap / Need
Phase 3 M3.1–M3.4 each added subject workflows + eval cases individually. M3.5 is the collective gate: confirm the full matrix is covered before declaring Phase 3 complete and pivoting to Phase 4.

### Success Criteria
- [x] SC1: Each Phase 3 workflow (browser-extension, container-image, ci-action, ide-plugin) has ≥1 positive (APPROVED/CONDITIONAL) + ≥1 negative (REJECTED) eval case with `Subject type is <type>` assertion
- [x] SC2: `evals/evals.json` is valid JSON with no duplicate ids
- [x] SC3: All eval assertions use recognized types (`contains_concept`, `exact_match`, `verdict_check`, `contains_string`, `file_exists`, `line_count_max`)
- [x] SC4: Nav doc M3.5 checkbox marked complete with date + summary
- [x] SC5: Nav doc Phase 3 status → Complete with exit criteria confirmed
- [x] SC6: Nav doc Priorities + Active Work updated to pivot to Phase 4
- [x] SC7: Eval harness gap explicitly logged as a Phase 6 caveat (not a Phase 3 blocker)

### Out of Scope
- Authoring new eval cases
- Building an eval runner/harness (Phase 6)
- Modifying any workflow files, criteria addenda, or SKILL.md
- Phase 4 planning

---

## Context

### Current State
Phase 3 M3.1–M3.4 closed 2026-04-14 through 2026-04-15. Five subject-specific workflows are live (registry-package from Phase 2; browser-extension, container-image, ci-action, ide-plugin from Phase 3). `evals/evals.json` contains 18 cases (ids 0–17, with id numbering gap at id 9 which appears after id 11 in file order).

**Eval coverage matrix (expected):**

| Workflow | Positive cases (APPROVED/CONDITIONAL) | Negative cases (REJECTED) |
|----------|---------------------------------------|--------------------------|
| browser-extension | id 1 (Wappalyzer), id 11 (uBlock Origin) | id 10 (YouTube downloader) |
| container-image | id 12 (nginx:latest) | id 13 (cryptominer) |
| ci-action | id 14 (actions/checkout SHA-pinned) | id 15 (reusable workflow) |
| ide-plugin | id 16 (Prettier) | id 17 (sideloaded VSIX) |

### Key Files

| File | Role | Change Summary |
|------|------|----------------|
| `evals/evals.json` | Eval case registry | Read-only — verify coverage + structure |
| `.projex/2604070218-install-auditor-subject-typed-redesign-nav.md` | Living roadmap | Update M3.5/Phase 3 status, Active Work, Priorities |

### Dependencies
- **Requires:** M3.1–M3.4 complete (satisfied)
- **Blocks:** Phase 4 planning (next nav action after this gate closes)

### Constraints
- Nav doc is the single source of truth for roadmap state
- Eval file must not be modified — this is a read-only verification gate

### Assumptions
- Eval cases added during M3.1–M3.4 are still present and unmodified
- The subject-type assertion pattern `"Subject type is <type>"` exists in each Phase 3 eval case

### Impact Analysis
- **Direct:** Nav doc status fields
- **Adjacent:** None — read-only verification of evals
- **Downstream:** Phase 4 planning unblocks after this gate closes

---

## Implementation

### Overview
Two-step gate: (1) verify eval coverage matrix + structural integrity, (2) update nav doc to close M3.5 and Phase 3.

### Step 1: Verify Eval Coverage + Structure

**Objective:** Confirm SC1–SC3 by reading `evals/evals.json`
**Confidence:** High
**Depends on:** None

**Verification checklist (read-only — no file changes):**

1. Parse `evals/evals.json` — confirm valid JSON
2. Extract all eval ids — confirm no duplicates
3. For each Phase 3 workflow, confirm:
   - **browser-extension:** ≥1 case with `"Subject type is browser-extension"` assertion + APPROVED/CONDITIONAL verdict expectation; ≥1 case with REJECTED verdict expectation
   - **container-image:** same pattern
   - **ci-action:** same pattern
   - **ide-plugin:** same pattern
4. Scan all assertion `type` fields — confirm each is one of: `contains_concept`, `exact_match`, `verdict_check`, `contains_string`, `file_exists`, `line_count_max`
5. Note the eval harness gap: no local runner exists to execute these cases automatically. Log as Phase 6 caveat.

**Rationale:** Gate must verify actual file state, not rely on walkthrough claims from M3.1–M3.4.

**Verification:** Checklist items 1–5 pass. Document findings in execution log.

**If this fails:** If any workflow lacks coverage, author the missing eval case(s) as an additional substep before proceeding. If structural issues found, fix them.

---

### Step 2: Update Navigation Document

**Objective:** Mark M3.5 complete, close Phase 3, pivot roadmap to Phase 4
**Confidence:** High
**Depends on:** Step 1 (verification must pass first)

**Files:**
- `.projex/2604070218-install-auditor-subject-typed-redesign-nav.md`

**Changes:**

1. **M3.5 checkbox** (line ~150): `- [ ]` → `- [x]` with completion annotation:
```markdown
// Before:
- [ ] **M3.5 — Eval gate: subject-typed regression cases** — At least one positive + one negative case per new workflow added to `evals/evals.json`. Browser-extension, container-image, ci-action, and ide-plugin portions now satisfied. Separate repo-level gap remains: no local eval harness is documented or runnable yet.

// After:
- [x] **M3.5 — Eval gate: subject-typed regression cases** — *Completed 2026-04-15.* All four Phase 3 workflows verified: browser-extension (ids 1, 10, 11), container-image (ids 12, 13), ci-action (ids 14, 15), ide-plugin (ids 16, 17). 18 total eval cases, valid JSON, no structural issues. Eval harness gap logged as Phase 6 caveat — not a Phase 3 blocker.
```

2. **Phase 3 status** (line ~117 area): `Current` → `Complete`
```markdown
// Before:
### Phase 3: High-Volume Subject Workflows — **Status: Current**

// After:
### Phase 3: High-Volume Subject Workflows — **Status: Complete** (2026-04-15)
```

3. **Phase 3 exit criteria confirmation** — append verification line after the existing exit criteria text:
```markdown
// Before:
**Exit Criteria:** Four high-volume subject workflows exist with subject-native rubrics and eval coverage. The dispatcher routes confidently to them. `generic.md` is no longer the fallback for any of these subject types.

// After:
**Exit Criteria:** Four high-volume subject workflows exist with subject-native rubrics and eval coverage. The dispatcher routes confidently to them. `generic.md` is no longer the fallback for any of these subject types. **✓ Confirmed 2026-04-15** — all criteria met; eval harness absence noted as Phase 6 gap, not Phase 3 blocker.
```

4. **Current Position** (line ~35 area): Update to reflect M3.5 + Phase 3 complete
```markdown
// Before:
**Phases 0–2 complete** (2026-04-12). **Phase 3 M3.1 complete** (2026-04-14). **Phase 3 M3.2 complete** (2026-04-15). **Phase 3 M3.3 complete** (2026-04-15). **Phase 3 M3.4 complete** (2026-04-15). Phase 3 remains Current; M3.5 (eval gate) is next.

// After:
**Phases 0–3 complete** (2026-04-15). Phase 3 M3.5 eval gate passed — all four subject workflows verified with positive + negative eval coverage (18 cases total). Phase 4 (long-tail subjects) is next.
```

5. **Active Work** (line ~55 area): Update to reflect Phase 3 closed, Phase 4 next
```markdown
// Before:
- **Subject-typed redesign (this nav)** — **Phases 0–2 complete (2026-04-12); Phase 3 M3.1 complete (2026-04-14); Phase 3 M3.2 complete (2026-04-15); Phase 3 M3.3 complete (2026-04-15); Phase 3 M3.4 complete (2026-04-15).** Dispatcher live with five subject-specific workflows: registry-package (Type 1), browser-extension (Type 2), ide-plugin (Type 3), container-image (Type 4), and ci-action (Type 5). Eval coverage: 18 cases (ids 0–17) — browser-extension Tier 1/2/3, container-image Tier 2/3, ci-action Tier 1/3, and ide-plugin Tier 1/3. **Current next action: Phase 3 M3.5 — eval gate closeout.**

// After:
- **Subject-typed redesign (this nav)** — **Phases 0–3 complete** (2026-04-15). Dispatcher live with five subject-specific workflows: registry-package (Type 1), browser-extension (Type 2), ide-plugin (Type 3), container-image (Type 4), ci-action (Type 5). Eval coverage: 18 cases (ids 0–17). **Current next action: Phase 4 M4.1 — `workflows/desktop-app.md`.**
```

6. **Priorities** (line ~201 area): Pivot current focus to Phase 4
```markdown
// Before:
**Current focus:** **Phase 3 M3.5 — eval gate closeout.** M3.4 closed 2026-04-15; all four Phase 3 subject workflows are now live (browser-extension, container-image, ci-action, ide-plugin). Each has ≥1 positive + ≥1 negative eval case; M3.5 is a review/confirmation gate.

// After:
**Current focus:** **Phase 4 M4.1 — `workflows/desktop-app.md`.** Phase 3 closed 2026-04-15 with M3.5 eval gate passed. Four subject workflows live with eval coverage verified.
```

7. **Recent Progress** — prepend M3.5 entry:
```markdown
- **2026-04-15** — **Phase 3 M3.5 complete → Phase 3 closed.** Eval gate passed: all four Phase 3 workflows (browser-extension, container-image, ci-action, ide-plugin) have ≥1 positive + ≥1 negative eval case. 18 total cases, valid JSON, no structural issues. Eval harness gap logged as Phase 6 caveat. Phase 3 exit criteria confirmed. Roadmap pivots to Phase 4 M4.1 (`workflows/desktop-app.md`).
```

8. **Revision Log** — append entry:
```markdown
| 2026-04-15 | **Phase 3 M3.5 complete → Phase 3 closed.** Eval gate verified: browser-extension (ids 1, 10, 11), container-image (ids 12, 13), ci-action (ids 14, 15), ide-plugin (ids 16, 17) — 18 cases total, all structurally valid. Nav updated: Phase 3 status → Complete (2026-04-15); M3.5 checkbox checked; exit criteria confirmed; Current Position, Active Work, Priorities pivoted to Phase 4 M4.1. Eval harness absence noted as Phase 6 gap. |
```

**Rationale:** Nav is the single source of truth. All status transitions must be reflected here for downstream consumers.

**Verification:** Read back the edited nav sections and confirm all 8 changes landed correctly.

**If this fails:** Revert nav edits; investigate which section had a conflict.

---

## Verification Plan

### Automated Checks
- [ ] `evals/evals.json` parses as valid JSON (Step 1)
- [ ] No duplicate eval ids (Step 1)

### Manual Verification
- [ ] Coverage matrix confirmed: 4 workflows × (≥1 positive + ≥1 negative) (Step 1)
- [ ] Nav doc reflects Phase 3 Complete throughout (Step 2)
- [ ] Nav doc priorities point to Phase 4 (Step 2)

### Acceptance Criteria Validation
| Criterion | How to Verify | Expected Result |
|-----------|---------------|-----------------|
| SC1: Eval coverage matrix | Read evals.json, check subject-type assertions + verdicts | 4/4 workflows covered |
| SC2: Valid JSON, no dup ids | Parse + id extraction | Clean parse, 18 unique ids |
| SC3: Recognized assertion types | Scan all `type` fields | All match known set |
| SC4: M3.5 checkbox | Read nav line ~150 | `[x]` with date + summary |
| SC5: Phase 3 status | Read nav Phase 3 header | "Complete (2026-04-15)" |
| SC6: Priorities pivot | Read nav Priorities section | Phase 4 M4.1 as current focus |
| SC7: Eval harness gap | Read nav M3.5 annotation + Phase 6 | Documented as Phase 6 caveat |

---

## Rollback Plan

1. `git revert HEAD` — the only changed file is the nav doc; reverting restores Phase 3 to Current status
2. No code or eval files are modified, so no secondary rollback needed

---

## Notes

### Risks
- **Low:** Eval cases could have been accidentally removed since M3.1–M3.4 closed → Step 1 verification catches this

### Open Questions
- *(none)*
