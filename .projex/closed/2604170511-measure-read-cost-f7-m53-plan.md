# Measure Read-Cost Claim (Eval F7) — M5.3

> **Status:** Complete
> **Completed:** 2026-04-17
> **Walkthrough:** `2604170511-measure-read-cost-f7-m53-walkthrough.md`
> **Created:** 2026-04-17
> **Author:** Claude (projex agent)
> **Source:** `2604070218-install-auditor-subject-typed-redesign-nav.md` Phase 5 M5.3
> **Nav:** `2604070218-install-auditor-subject-typed-redesign-nav.md`
> **Related Projex:** `2604070217-subject-typed-audit-dispatch-eval.md` (F7 claim origin), `2604082335-dispatcher-refactor-m11-m12-plan.md` (migration commit)
> **Worktree:** No

---

## Summary

Empirically validate eval F7: "Per-audit *read cost* drops under dispatch even though *total file count* rises." Compare old monolith SKILL.md (pre-refactor) against current dispatcher SKILL.md + each workflow file. Produce a findings document with exact numbers; update nav M5.3 checkbox.

**Scope:** Measurement + analysis + nav update. No workflow file changes unless F7 is refuted (escalates to human).
**Estimated Changes:** 1 new file (findings document), 1 edited file (nav)

---

## Objective

### Problem / Gap / Need

F7 is the dispatch architecture's primary token-efficiency argument: each audit reads only `SKILL.md` (dispatcher) + one relevant workflow — less than the old monolithic `SKILL.md` end-to-end. Confidence was rated Medium-High with evidence basis "Reasoning, not measurement." Phase 5 exit criteria require empirical validation.

### Success Criteria

- [ ] Old monolith SKILL.md byte/line count retrieved from git history (commit `1b02882`, parent of `3842b76`)
- [ ] Current dispatcher SKILL.md byte/line count measured
- [ ] All 10 workflow files measured (bytes + lines)
- [ ] Comparison table: old monolith vs (dispatcher + each workflow) for all 10 types
- [ ] Written finding: validates or refutes F7 with exact numbers and worst-case analysis
- [ ] Nav M5.3 checkbox marked complete with link to findings

### Out of Scope

- Changing any workflow file content
- Measuring runtime performance or actual LLM token counts (byte/line proxy is sufficient per eval framing)
- Refactoring if F7 is refuted (escalates to human review)

---

## Context

### Current State

Old monolith (commit `1b02882`): `SKILL.md` = 306 lines, 15,851 bytes — the single file read on every audit invocation.

Current dispatcher: `SKILL.md` = 242 lines, 15,272 bytes — read on every audit, then loads exactly one workflow file per subject type.

Workflow files (10 total, 2,862 lines / 147,601 bytes aggregate):

| Workflow | Lines | Bytes |
|----------|------:|------:|
| `generic.md` | 80 | 3,701 |
| `ci-action.md` | 219 | 8,019 |
| `remote-integration.md` | 175 | 10,568 |
| `agent-extension.md` | 230 | 12,977 |
| `cli-binary.md` | 264 | 13,393 |
| `ide-plugin.md` | 358 | 16,186 |
| `browser-extension.md` | 369 | 17,689 |
| `desktop-app.md` | 360 | 17,344 |
| `registry-package.md` | 488 | 23,304 |
| `container-image.md` | 319 | 24,420 |

### Key Files

| File | Role | Change Summary |
|------|------|----------------|
| `.projex/2604170511-measure-read-cost-f7-m53-findings.md` | New findings document | Written in Step 3 |
| `.projex/2604070218-install-auditor-subject-typed-redesign-nav.md` | Nav file | M5.3 checkbox → complete |

### Dependencies

- **Requires:** M5.1 (tighten classifier) ✓, M5.2 (trim generic.md) ✓
- **Blocks:** Phase 5 exit (all three milestones must complete)

### Constraints

- Measurement uses bytes/lines as proxy for token read cost (consistent with eval framing)
- If F7 is refuted, plan does NOT auto-fix — documents the finding and escalates to human

### Assumptions

- Old monolith at `1b02882` is the correct pre-refactor baseline (parent of dispatcher refactor commit `3842b76`)
- Per-audit read = `SKILL.md` + exactly one workflow file (dispatcher loads one, not multiple)
- Byte count is a reasonable proxy for token count (monotonic correlation, sufficient for relative comparison)
- SKILL.md size evolution matters: 13,126 B at Phase 1 refactor → 15,272 B at current HEAD (M5.1 classifier tightening added ~2 KB). Both snapshots should be tested against F7

### Impact Analysis

- **Direct:** New findings document, nav update
- **Adjacent:** Phase 5 exit criteria depend on this measurement
- **Downstream:** If F7 refuted → architecture reconsideration (human-gated)

---

## Implementation

### Overview

Three steps: (1) collect all measurements from git + filesystem, (2) compute comparisons and determine verdict, (3) write findings document and update nav.

### Step 1: Collect Measurements

**Objective:** Gather exact byte/line counts for old monolith and all current files.
**Confidence:** High
**Depends on:** None

**Files:**
- `SKILL.md` (read current)
- `workflows/*` (read current, 10 files)
- Git history commit `1b02882` for old `SKILL.md`

**Changes:**

```shell
# Old monolith (already confirmed: 306 lines, 15851 bytes)
git show 1b02882:SKILL.md | wc -l -c

# Current dispatcher (already confirmed: 242 lines, 15272 bytes)
wc -l -c SKILL.md

# Dispatcher at Phase 1 refactor (for evolution tracking: 218 lines, 13126 bytes)
git show 3842b76:SKILL.md | wc -l -c

# All workflow files (already confirmed individually above)
wc -l -c workflows/*
```

**Rationale:** Git history provides exact pre-refactor baseline. Phase 1 snapshot isolates dispatcher growth from subsequent phases. `wc` gives deterministic byte/line counts.

**Verification:** Numbers match the Context section above (already pre-gathered).

**If this fails:** If `1b02882` doesn't contain old SKILL.md, trace `git log --follow SKILL.md` to find correct baseline commit.

---

### Step 2: Compute Comparison Table and Verdict

**Objective:** For each subject type, compare old monolith read cost vs dispatcher + workflow read cost. Determine F7 validity.
**Confidence:** High
**Depends on:** Step 1

**Changes:**

Compute for each of 10 types: `(dispatcher_bytes + workflow_bytes)` vs `old_monolith_bytes`.

Key comparisons (pre-computed from Context data):

| Subject Type | Dispatcher + Workflow (bytes) | vs Old Monolith (15,851 B) | Delta |
|---|---:|---|---:|
| generic | 15,272 + 3,701 = 18,973 | **+3,122 (+20%)** | WORSE |
| ci-action | 15,272 + 8,019 = 23,291 | **+7,440 (+47%)** | WORSE |
| remote-integration | 15,272 + 10,568 = 25,840 | **+9,989 (+63%)** | WORSE |
| agent-extension | 15,272 + 12,977 = 28,249 | **+12,398 (+78%)** | WORSE |
| cli-binary | 15,272 + 13,393 = 28,665 | **+12,814 (+81%)** | WORSE |
| ide-plugin | 15,272 + 16,186 = 31,458 | **+15,607 (+98%)** | WORSE |
| desktop-app | 15,272 + 17,344 = 32,616 | **+16,765 (+106%)** | WORSE |
| browser-extension | 15,272 + 17,689 = 32,961 | **+17,110 (+108%)** | WORSE |
| registry-package | 15,272 + 23,304 = 38,576 | **+22,725 (+143%)** | WORSE |
| container-image | 15,272 + 24,420 = 39,692 | **+23,841 (+150%)** | WORSE |

**Secondary comparison — Phase 1 dispatcher baseline (13,126 B):**

Even at the smaller Phase 1 snapshot before subsequent phases grew SKILL.md, the smallest combo (dispatcher + generic.md = 13,126 + 3,701 = 16,827 B) still exceeds the old monolith (15,851 B) by 976 B (+6%). All other types exceed by more. F7 refuted under both snapshots.

**Preliminary verdict:** F7 is **refuted**. Every subject type reads MORE bytes under dispatch than the old monolith, under both current and Phase 1 dispatcher baselines. Root cause: the dispatcher SKILL.md was not compressed to ~4 KB as originally planned (deviation logged in M1.1 close: Step N's report skeleton blocked compression). Even at Phase 1 size (13,126 B), adding any workflow exceeds the old monolith.

**Rationale:** The F7 claim assumed the dispatcher would be much smaller than the monolith. The 4 KB target was missed — the dispatcher retained the full verdict tree, audit-coverage report skeleton, and red flags table. These are load-bearing and cannot be trivially removed.

**Verification:** Arithmetic checked against `wc` output. All 10 comparisons show the same direction.

**If this fails:** N/A — arithmetic is deterministic. If numbers don't match, re-run `wc` in Step 1.

---

### Step 3: Write Findings Document and Update Nav

**Objective:** Record measurement results, verdict, and analysis in a findings document. Update nav M5.3 checkbox.
**Confidence:** High
**Depends on:** Step 2

**Files:**
- `.projex/2604170511-measure-read-cost-f7-m53-findings.md` (new — findings document)
- `.projex/2604070218-install-auditor-subject-typed-redesign-nav.md` (edit — M5.3 checkbox)

**Changes:**

Findings document structure:
- Executive summary: F7 refuted — per-audit read cost rises 20–150% under dispatch
- Measurement table (10 types, exact bytes/lines, delta vs monolith)
- Root cause: dispatcher SKILL.md ≈ monolith size due to Step N report skeleton retention
- Nuance: dispatch still provides qualitative benefits (subject-specific rubrics, maintainability, extensibility) even though raw read cost increased
- Recommendation: accept the trade-off or pursue dispatcher compression in a future milestone

Nav update: mark M5.3 checkbox complete, link to findings document.

**Rationale:** Written record required by Phase 5 exit criteria. Nav back-link ensures traceability.

**Verification:** Findings document exists with complete comparison table. Nav M5.3 line shows `[x]` with link.

**If this fails:** Manual edit to nav if checkbox format doesn't match expected pattern.

---

## Verification Plan

### Manual Verification

- [ ] Findings document contains all 10 workflow comparisons with exact byte counts
- [ ] Verdict clearly states F7 validated or refuted
- [ ] Root cause analysis explains why (dispatcher size not compressed)
- [ ] Nav M5.3 checkbox is marked complete with link

### Acceptance Criteria Validation

| Criterion | How to Verify | Expected Result |
|-----------|---------------|-----------------|
| Old monolith measured | `git show 1b02882:SKILL.md \| wc -c` | 15,851 bytes |
| Current dispatcher measured | `wc -c SKILL.md` | 15,272 bytes |
| All 10 workflows measured | `wc -c workflows/*` | Matches Context table |
| Comparison table complete | Findings doc has 10-row table | All 10 types compared |
| Verdict documented | Findings doc executive summary | Clear validate/refute statement |
| Nav updated | Nav M5.3 line | `[x]` with link to findings |

---

## Rollback Plan

Measurement/analysis task — no code changes to roll back. If findings are contested:

1. Delete findings document
2. Revert nav M5.3 checkbox edit
3. Re-measure with different methodology if byte proxy is deemed insufficient

---

## Notes

### Risks

- **Dispatcher compression revisited:** F7 refutation doesn't invalidate the dispatch architecture — subject-specific rubrics, maintainability, and extensibility are independent benefits. But the efficiency claim must be honestly documented as false.
- **Nuance in "read cost":** The model may not read every byte linearly; structured dispatch *could* reduce effective cognitive load even at higher byte count. This plan measures raw bytes (the claim's basis), not cognitive efficiency.

### Open Questions

(None — measurement methodology and data sources are fully determined.)
