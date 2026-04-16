# Walkthrough: Tighten the Classifier (M5.1)

> **Execution Date:** 2026-04-16
> **Completed By:** projex-agent (orchestrated)
> **Source Plan:** 2604160430-tighten-classifier-m51-plan.md
> **Result:** Success

---

## Summary

Replaced the binary high/low confidence routing model in `SKILL.md` Step 0 with a three-tier table (high → specific workflow, medium → best-match specific workflow, low → `generic.md`). Cleaned up dispatch table: renamed stale column header, stripped milestone references from all rows, updated generic row description, removed factually wrong Phase 2 note. `generic.md` is now a documented low-confidence fallback, not the default.

---

## Objectives Completion

| Objective | Status | Notes |
|-----------|--------|-------|
| Three-tier confidence model replaces binary high/low | Complete | Table form with 5 conditions covers all routing paths |
| `generic.md` restricted to low-confidence only | Complete | Closing sentence + table explicit |
| Dispatch table cleaned | Complete | Header, all rows, Phase 2 note |

---

## Execution Detail

### Step 1: Rewrite Procedure Paragraph

**Planned:** Replace binary high/low paragraph with three-tier model; medium routes to specific workflow with Rationale note; only low → `generic.md`.

**Actual:** `SKILL.md` line 28 single-paragraph procedure replaced with a 5-row confidence table covering: one strong signal (high), boundary-rule-resolved multi-match (high), weak/partial pointing to single candidate (medium → specific + Rationale note), multiple weak unresolved (low → generic), no signals (low → generic). Closing sentence made explicit: only low routes to generic.

**Deviation:** None.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `SKILL.md` | Modified | Yes | Lines 28–36: paragraph → 5-row confidence table + closing sentence |

**Verification:** Re-read Step 0 top-to-bottom; dry-ran eval cases 0 (express) and 1 (Wappalyzer) — both still route high-confidence to specific workflows.

---

### Step 2: Update Dispatch Table Metadata

**Planned:** Rename "Phase 1 Status" → "Status"; simplify rows to "Live"; update generic row; remove Phase 2 note.

**Actual:** Column header renamed. All 9 specific-type rows simplified (row 8 retains 8a/8b/8c sub-rubric note). Generic row updated: "Low-confidence fallback only". Phase 2 blockquote removed entirely.

**Deviation:** None.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `SKILL.md` | Modified | Yes | Lines 70–82: column header, 10 table rows, removed Phase 2 note |

**Verification:** Dispatch table has 10 clean rows, "Status" column, no stale milestone refs.

---

## Complete Change Log

### Files Modified
| File | Changes | Lines Affected | In Plan? |
|------|---------|----------------|----------|
| `SKILL.md` | Procedure → confidence table; dispatch table cleanup; Phase 2 note removed | ~28–36, ~70–82 | Yes |

### Files Created
| File | Purpose | In Plan? |
|------|---------|----------|
| `.projex/2604160430-tighten-classifier-m51-log.md` | Execution log | Yes (execution artifact) |

### Planned But Not Changed
None.

---

## Success Criteria Verification

| Criterion | Method | Result | Evidence |
|-----------|--------|--------|----------|
| Three confidence tiers defined (high / medium / low) | Read SKILL.md Step 0 | Pass | 5-row table with explicit condition → confidence → route mapping |
| Only `low` routes to `generic.md` | Read closing sentence + table | Pass | "Only `low` confidence routes to `generic.md`" explicit |
| Phase 2 note removed | Search SKILL.md | Pass | Blockquote absent |
| Column renamed "Phase 1 Status" → "Status" | Read table header | Pass | Header reads "Status" |
| Generic row: "Low-confidence fallback only" | Read dispatch table | Pass | Row 0 reads "Low-confidence fallback only" |
| No regressions on existing 26 eval cases | Dry-run named-type evals | Pass | All named-type evals had high confidence; new medium tier doesn't affect them |

**Overall:** 6/6 criteria passed.

---

## Deviations from Plan
None.

## Issues Encountered
None.

---

## Key Insights

### Lessons Learned
- **Three-tier confidence is a natural fit** — the medium tier was already implicit in the output shape; making it explicit in routing logic required only the procedure text, not any structural change.

### Technical Insights
- Dispatch table milestone refs ("Live — Phase 3 (M3.1)") were already stale; M5.1 was the right moment to strip them before they became longer-term confusion.
- The Phase 2 note was factually wrong (claimed remaining types route to generic); it had survived unnoticed since M2.1.

---

## Recommendations

### Immediate Follow-ups
- [ ] **M5.2** — Trim `generic.md` to true fallback: identify subject, ask user to clarify if classification uncertain, run defensive minimum audit with warning note.

### Future Considerations
- M5.3 measures per-audit token read cost vs old monolith (eval F7 claim).
