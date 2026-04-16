# Patch: Phase 4 Eval Gate — M4.5

> **Date:** 2026-04-16
> **Author:** Claude (patch-projex)
> **Directive:** Verify ≥1 eval case per long-tail workflow, check M4.5 checkbox, mark Phase 4 Complete, pivot nav to Phase 5.
> **Source Plan:** Direct — nav milestone M4.5
> **Nav:** 2604070218-install-auditor-subject-typed-redesign-nav.md
> **Result:** Success

---

## Summary

Phase 4 eval gate trivially passes: all four long-tail workflows have 2 eval cases each (8 Phase 4 cases total, 26 overall). Nav updated to reflect Phase 4 Complete and pivot roadmap to Phase 5 M5.1 (default-off generic).

---

## Verification

**Method:** Parse `evals/evals.json`, filter eval IDs by subject-type assertions and prompt content for each Phase 4 workflow.

**Result:**
```
desktop-app:        ids [18, 19] — 2 cases — PASS
cli-binary:         ids [20, 21] — 2 cases — PASS
agent-extension:    ids [22, 23] — 2 cases — PASS
remote-integration: ids [24, 25] — 2 cases — PASS
Total evals: 26
```

**Status:** PASS — gate satisfied with 2x margin (≥1 required, 2 present per workflow).

---

## Changes

### Nav — M4.5 checkbox

**File:** `.projex/2604070218-install-auditor-subject-typed-redesign-nav.md`
**Change Type:** Modified

- M4.5 checkbox: `[ ]` → `[x]` with completion note (ids verified, gate passes, Phase 4 exit criteria confirmed)
- Phase 4 header: `Status: Current (M4.1+…+M4.4 complete)` → `Status: Complete (2026-04-16)`
- Active Work: updated to Phases 0–4 complete, pivot to Phase 5 M5.1
- Priorities: current focus → Phase 5 M5.1 (default-off generic); next up → Phase 5 M5.2
- Recent Progress: M4.5 entry added at top
- Revision Log: M4.5 entry appended

**Why:** Gate verification is paperwork — no code changes needed. All Phase 4 eval cases were already in place from M4.1–M4.4 execution.

---

## Impact on Related Projex

| Document | Relationship | Update Made |
|----------|-------------|-------------|
| `2604070218-install-auditor-subject-typed-redesign-nav.md` | Source nav | M4.5 checked, Phase 4 → Complete, pivot to Phase 5 |

---

## Notes

- Phase 4 exit criteria from nav: "All 9 specific workflow files exist. `generic.md` is now genuinely a low-confidence fallback, not the everyday default." — confirmed.
- M4.5 eval gate was structurally satisfied before this patch ran; the patch formalizes the verification and closes the phase.
- Phase 5 M5.1 is the next concrete action: tighten the classifier in `SKILL.md` so Type 0 (generic) triggers only on low-confidence classifications.
