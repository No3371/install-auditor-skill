# Walkthrough: Measure Read-Cost Claim (Eval F7) — M5.3

> **Execution Date:** 2026-04-17
> **Completed By:** Claude (projex orchestration)
> **Source Plan:** `2604170511-measure-read-cost-f7-m53-plan.md`
> **Nav:** `2604070218-install-auditor-subject-typed-redesign-nav.md`
> **Result:** Success

---

## Summary

Empirically measured per-audit token read cost under the dispatch architecture vs the old monolith (`SKILL.md` pre-Phase 1). F7 — "per-audit read cost drops under dispatch even though total file count rises" — is **refuted**: every subject type reads 20–150% more bytes under dispatch. Findings documented; nav M5.3 marked complete. Phase 5 exit criteria met.

---

## Objectives Completion

| Objective | Status | Notes |
|-----------|--------|-------|
| Retrieve old monolith byte/line count from git | Complete | `1b02882`: 306 lines, 15,851 B |
| Measure current dispatcher SKILL.md | Complete | 242 lines, 15,272 B |
| Measure all 10 workflow files | Complete | 2,862 lines / 147,601 B total |
| 10-type comparison table | Complete | All 10 types: WORSE |
| Written finding — F7 validated or refuted | Complete | F7 refuted; findings doc at `2604170511-measure-read-cost-f7-m53-findings.md` |
| Nav M5.3 checkbox → complete with link | Complete | `[x]` with walkthrough + findings links |

---

## Execution Detail

### Step 1: Collect Measurements

**Planned:** Run `git show 1b02882:SKILL.md | wc -l -c`, `git show 3842b76:SKILL.md | wc -l -c`, `wc -l -c SKILL.md`, `wc -l -c workflows/*`.

**Actual:** Same commands executed exactly as planned. All numbers matched the plan's pre-computed Context table exactly — no discrepancies.

**Deviation:** None.

**Files Changed:**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `.projex/2604170511-measure-read-cost-f7-m53-log.md` | Created | Yes | Step 1 log entry written |

**Verification:** Numbers matched plan table verbatim.

---

### Step 2: Compute Comparison Table and Verdict

**Planned:** Compute `dispatcher_bytes + workflow_bytes` vs `old_monolith_bytes` for all 10 types; determine F7 verdict.

**Actual:** Pre-computed table from the plan confirmed by measurements. Both baselines tested:
- Current dispatcher (15,272 B): smallest combo (+ generic.md = 18,973 B) exceeds monolith by +20%
- Phase 1 dispatcher (13,126 B): smallest combo (+ generic.md = 16,827 B) exceeds monolith by +6.2%
- F7 refuted under both baselines.

**Deviation:** None.

**Files Changed:**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `.projex/2604170511-measure-read-cost-f7-m53-log.md` | Modified | Yes | Step 2 log entry appended |

---

### Step 3: Write Findings Document and Update Nav

**Planned:** Create `.projex/2604170511-measure-read-cost-f7-m53-findings.md`; edit nav M5.3 checkbox to `[x]`.

**Actual:** Findings document written with full executive summary, baselines table, 10-type comparison table, Phase 1 baseline check, root cause analysis, nuance section, recommendation. Nav M5.3 updated from `[ ]` to `[x]` with findings link and inline summary. Priorities section updated to "Phase 5 complete."

**Deviation:** None.

**Files Changed:**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `.projex/2604170511-measure-read-cost-f7-m53-findings.md` | Created | Yes | 121 lines — full measurement findings |
| `.projex/2604070218-install-auditor-subject-typed-redesign-nav.md` | Modified | Yes | M5.3 `[ ]` → `[x]`; priorities updated |

---

## Complete Change Log

> **Derived from:** `git diff --stat master..projex/2604170511-measure-read-cost-f7-m53`

### Files Created
| File | Purpose | Lines | In Plan? |
|------|---------|-------|----------|
| `.projex/2604170511-measure-read-cost-f7-m53-findings.md` | F7 measurement findings — verdict, tables, root cause, recommendation | 121 | Yes |
| `.projex/2604170511-measure-read-cost-f7-m53-log.md` | Execution log | 69 | Yes |

### Files Modified
| File | Changes | Lines Affected | In Plan? |
|------|---------|----------------|----------|
| `.projex/2604070218-install-auditor-subject-typed-redesign-nav.md` | M5.3 checkbox → `[x]`, findings link added, priorities updated | ~6 lines | Yes |
| `.projex/2604170511-measure-read-cost-f7-m53-plan.md` | Status → Complete, walkthrough link added | ~2 lines | Yes |

### Files Deleted
(none)

### Planned But Not Changed
(none — all planned changes executed)

---

## Success Criteria Verification

### Criterion 1: Old monolith measured

**Verification Method:** `git show 1b02882:SKILL.md | wc -c`
**Evidence:** 15,851 bytes
**Result:** PASS

---

### Criterion 2: Current dispatcher measured

**Verification Method:** `wc -c SKILL.md`
**Evidence:** 15,272 bytes
**Result:** PASS

---

### Criterion 3: All 10 workflows measured

**Verification Method:** `wc -l -c workflows/*`
**Evidence:** 2,862 lines / 147,601 bytes total across 10 files (agent-extension, browser-extension, ci-action, cli-binary, container-image, desktop-app, generic, ide-plugin, registry-package, remote-integration)
**Result:** PASS

---

### Criterion 4: 10-row comparison table in findings doc

**Verification Method:** Read findings doc — count rows in comparison table
**Evidence:** 10 rows, all marked WORSE. Range: generic +20% to container-image +150%
**Result:** PASS

---

### Criterion 5: Verdict documented

**Verification Method:** Read findings doc executive summary
**Evidence:** "F7 is refuted. Per-audit read cost rises 20–150% under dispatch vs the old monolith for every subject type."
**Result:** PASS

---

### Criterion 6: Nav M5.3 `[x]` with link

**Verification Method:** Read nav Phase 5 M5.3 line
**Evidence:** `- [x] **M5.3 ...** → [findings link] **F7 refuted...**`
**Result:** PASS

---

### Acceptance Criteria Summary

| Criterion | Method | Result | Evidence |
|-----------|--------|--------|----------|
| Old monolith measured | `git show 1b02882:SKILL.md \| wc -c` | Pass | 15,851 B |
| Current dispatcher measured | `wc -c SKILL.md` | Pass | 15,272 B |
| All 10 workflows measured | `wc -l -c workflows/*` | Pass | 147,601 B total |
| 10-type comparison table | Findings doc row count | Pass | 10 rows, all WORSE |
| Verdict documented | Executive summary | Pass | "F7 is refuted" |
| Nav M5.3 `[x]` + link | Nav line check | Pass | `[x]` with findings link |

**Overall: 6/6 criteria passed**

---

## Deviations from Plan

None. All steps executed exactly as planned. The pre-computed measurements in the plan Context table were confirmed verbatim by live `wc` output.

---

## Issues Encountered

None.

---

## Key Insights

### Lessons Learned

1. **Embedding measurements in the plan pays off**
   - Context: Opus plan agent pre-computed all 10 comparisons in the plan document before execution started.
   - Insight: When measurements are deterministic (byte counts from committed files), pre-computing them in the plan collapses execution to pure verification — no surprises.
   - Application: For measurement/analysis plans, compute as much as possible during planning to make execution a confirmation step.

2. **Dispatcher compression target missed early sets up a false claim**
   - Context: M1.1 set a ≤4 KB target for the dispatcher SKILL.md. The actual size was 12.5 KB (documented as deliberate trade-off). M5.1 classifier tightening added another ~2 KB.
   - Insight: An efficiency claim that depends on a size target should be flagged as contingent — not as a medium-high confidence finding — when the target is already known to be aspirational.
   - Application: In future architecture pivots, tie efficiency claims to explicit preconditions; if a precondition is missed, cascade the finding as tentative immediately.

### Pattern Discoveries

1. **F7-class findings: "reasoning not measurement"**
   - Observed in: eval doc `2604070217-subject-typed-audit-dispatch-eval.md`, where F7 was explicitly tagged "Reasoning, not measurement — flag for navigate-projex to validate"
   - Description: The eval's gap-tracking discipline (flagging unvalidated claims) made M5.3 straightforward to scope — the claim was already quarantined.
   - Reuse potential: Any architectural claim tagged "reasoning not measurement" should become a Phase N validation milestone in the nav; this pattern worked well here.

### Technical Insights

- Current dispatcher SKILL.md (15,272 B) is within 4% of the old monolith (15,851 B). The efficiency gap is not from the dispatcher adding structure — it's from M5.1 classifier tightening adding 2,146 B. The Phase 1 dispatcher (13,126 B) was genuinely smaller, but even then F7 was marginal (+6% over monolith at best case).
- The dispatch architecture's real value is qualitative: subject-specific rubrics, isolated maintainability, reduced blast radius per change. These hold regardless of F7.

---

## Recommendations

### Immediate Follow-ups
- [ ] Phase 5 exit review — all three milestones complete; confirm Phase 5 → Closed in nav
- [ ] Phase 6 planning — eval stewardship cadence, per-workflow eval bundles (M6.1+)

### Future Considerations
- If dispatcher compression becomes a goal (to validate F7 retroactively), target: SKILL.md ≤ 8 KB. The Step N verdict tree + audit-coverage table are the primary blockers (~5 KB). A factored approach (load verdict tree from a separate `references/verdict.md`) could achieve this.
- The F7 refutation is honest documentation — the architecture is still the right call. Consider updating the eval doc `2604070217-subject-typed-audit-dispatch-eval.md` to record F7 as empirically refuted.

---

## Related Projex Updates

### Documents Updated
| Document | Update |
|----------|--------|
| `2604170511-measure-read-cost-f7-m53-plan.md` | Status → Complete; walkthrough linked |
| `2604070218-install-auditor-subject-typed-redesign-nav.md` | M5.3 `[x]`; findings + walkthrough linked; priorities → Phase 5 complete |
