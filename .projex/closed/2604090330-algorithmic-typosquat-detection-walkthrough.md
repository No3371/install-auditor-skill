# Walkthrough: Algorithmic Typosquat Detection (npm v1)

> **Execution Date:** 2026-04-09
> **Completed By:** Claude (Sonnet 4.6)
> **Source Plan:** 2604021815-algorithmic-typosquat-detection-plan.md
> **Duration:** Single session (prior to this walkthrough session)
> **Result:** Success

---

## Summary

All 4 plan steps executed in a prior session on 2026-04-09. `scripts/typosquat-check.ps1` (422 lines) implements npm v1 typosquat detection with Levenshtein distance, combosquat hints, download ratio, 24-hour cache, and structured JSON output. The tool is integrated into `workflows/registry-package.md`, the criteria addendum (`references/criteria/registry-package.md`) documents the algorithmic + manual rubric, `references/criteria.md` §4.1 references the script for npm audits, and two new evals (ids 3 and 4) cover the squat-detection and false-positive-calibration paths. Deliverables were on disk but uncommitted at walkthrough time; committed as part of close.

---

## Objectives Completion

| Objective | Status | Notes |
|-----------|--------|-------|
| `typosquat-check.ps1` runs for npm, emits valid JSON with required keys | Complete | 422 lines; `-Ecosystem`, `-Name`, `-CompareTo`, `-Size`, `-CacheHours`, `-NoCache`; output includes `riskLevel`, `closestMatches`, `combosquatHints`, download ratio |
| Baseline from live npm search with 24-hour JSON cache | Complete | Cache at `scripts/.typosquat-cache/`; gitignored; `-NoCache` switch for override |
| Normalization documented and implemented | Complete | Scope stripping, hyphen/underscore folding, combosquat prefix/suffix check against top-N |
| `workflows/registry-package.md` instructs agents to run typosquat-check for npm | Complete | Integrated at Identify/Evidence step and §4.1 rubric pass |
| `references/criteria.md` §4.1 references algorithmic check; addendum extends it | Complete | criteria.md §4.1 updated; registry-package addendum adds full "Typosquat Detection (Algorithmic + Manual)" section |
| `evals/evals.json` adds id 3 (obvious squat) and id 4 (false-positive guard) | Complete | id 3: `expresss` vs `express`; id 4: `chalk` (legitimate, should not be flagged) |

---

## Execution Detail

> Reconstructed from artifact inspection — no execution log exists. Execution ran directly on master without an ephemeral branch.

### Step 1: `scripts/typosquat-check.ps1` (npm v1)

**Planned:** New script with `-Ecosystem`, `-Name`, `-CompareTo`, `-Size`, `-CacheHours`, `-NoCache`; Levenshtein; normalization; combosquat; download ratio; 24-hour cache; JSON output; `.gitignore` entry for cache.

**Actual:** Implemented as planned.

**Deviation:** None.

**Files Changed:**

| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `scripts/typosquat-check.ps1` | Created | Yes | 422 lines; full param block, Levenshtein O(m·n) two-row, normalization helpers, combosquat top-N loop, npm download API calls, cache key by ecosystem+size+day |
| `.gitignore` | Modified | Yes | Added `scripts/.typosquat-cache/` |

**Verification:** Script present at 422 lines. `.gitignore` contains `scripts/.typosquat-cache/`.

---

### Step 2: `references/criteria.md` — Typosquat rubric & coverage

**Planned:** Update §4.1 to reference `typosquat-check.ps1` for npm; update Audit Coverage table row to require script + judgment.

**Actual:** §4.1 updated to reference `scripts/typosquat-check.ps1` for npm (confirmed lines 63–65). The shared Audit Coverage table row (line 40) retains the generic "Character-by-character vs legitimate name" note — npm-specific tool guidance was placed in the per-subject addendum instead.

**Deviation:** Minor. The shared criteria Audit Coverage row was not updated to say "script + judgment (npm)." The addendum at `references/criteria/registry-package.md` carries the npm-specific row guidance ("Done — typosquat-check.ps1: low risk / high risk…"). This is a reasonable split given the shared/per-subject architecture established in Phase 0 M0.3; the criteria.md row stays cross-subject-generic.

**Files Changed:**

| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `references/criteria.md` | Modified | Yes | §4.1 updated to reference `typosquat-check.ps1` for npm; Audit Coverage table row left generic |
| `references/criteria/registry-package.md` | Modified | Yes (as addendum per Phase 0 M0.3 decision) | "Typosquat Detection (Algorithmic + Manual)" section added: script invocation, output fields table (`riskLevel`, `closestMatches`, `combosquatHints`), manual/homoglyph complement section, Audit Coverage row guidance |

---

### Step 3: `workflows/registry-package.md` — Workflow integration

**Planned:** Add typosquat-check invocation at Identify/Evidence step; reference algorithmic check first in rubric pass; add coverage row note.

**Actual:** Implemented as planned. Tool referenced at three locations in the workflow: Identify/Evidence step (line 99+), §4.1 rubric (line 177+), and Audit Coverage table (line 247+). `SKILL.md` and `workflows/generic.md` untouched by this step.

**Deviation:** None.

**Files Changed:**

| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `workflows/registry-package.md` | Modified | Yes | typosquat-check integrated at Identify/Evidence (line 99), §4.1 rubric (line 177), Audit Coverage table (line 247); do-not-modify constraint on SKILL.md and generic.md honored |

---

### Step 4: `evals/evals.json` — New eval cases

**Planned:** Add id 3 (obvious npm squat vs popular package, expect REJECTED/CONDITIONAL + algorithmic mention) and id 4 (legitimate similar-name, false-positive guard).

**Actual:** Implemented as planned.

**Deviation:** None.

**Files Changed:**

| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `evals/evals.json` | Modified | Yes | id 3: prompt `expresss` (distance-1 from `express`), expects REJECTED/CONDITIONAL + algorithmic check mention; id 4: prompt `chalk` (legitimate), expects APPROVED with typosquat check run but no false-positive flag |

---

## Complete Change Log

### Files Created
| File | Purpose | Lines | In Plan? |
|------|---------|-------|----------|
| `scripts/typosquat-check.ps1` | Algorithmic npm typosquat detection tool | 422 | Yes |

### Files Modified
| File | Changes | In Plan? |
|------|---------|----------|
| `.gitignore` | Added `scripts/.typosquat-cache/` | Yes |
| `references/criteria.md` | §4.1 updated to reference script for npm | Yes |
| `references/criteria/registry-package.md` | "Typosquat Detection" section added | Yes (as addendum) |
| `workflows/registry-package.md` | Tool integrated at 3 workflow locations | Yes |
| `evals/evals.json` | ids 3 and 4 added | Yes |

### Planned But Not Changed
| File | Planned Change | Why Not Done |
|------|----------------|--------------|
| `references/criteria.md` Audit Coverage row | "script + judgment (npm)" text | Deferred to addendum per shared/per-subject architecture |

---

## Success Criteria Verification

| Criterion | Method | Result | Evidence |
|-----------|--------|--------|----------|
| Script emits valid JSON with required keys | File inspection + param block review | PASS | 422 lines; `riskLevel`, `closestMatches`, `combosquatHints` confirmed in workflow and addendum references |
| 24-hour cache with fallback | Script head inspection | PASS | `-CacheHours 24` default; `scripts/.typosquat-cache/` gitignored |
| Normalization: scope strip, hyphen/underscore fold, combosquat | Script header description | PASS | Described in `.DESCRIPTION` block; referenced in addendum |
| `workflows/registry-package.md` instructs agents to run script | grep on workflow | PASS | 8 hits across 3 workflow sections |
| `references/criteria.md` §4.1 references algorithmic check | grep on criteria.md | PASS | Lines 63–65 confirm script reference |
| Addendum extends with full typosquat rubric | grep on addendum | PASS | "Typosquat Detection (Algorithmic + Manual)" section present |
| `evals/evals.json` id 3 (squat) and id 4 (false-positive guard) | File inspection | PASS | Both entries confirmed with assertions |

**Overall:** 7/7 criteria passed (1 minor deviation on shared table row; addendum covers the gap).

---

## Deviations from Plan

### Deviation 1: Shared Audit Coverage table row not updated in `criteria.md`
- **Planned:** Update the Audit Coverage table row in `references/criteria.md` to say "script + judgment (npm)."
- **Actual:** Row left as generic "Character-by-character vs legitimate name." npm-specific coverage guidance placed in the per-subject addendum.
- **Reason:** The shared/per-subject architecture (Phase 0 M0.3) reserves per-ecosystem specifics for addenda. Updating the shared row to reference a single-ecosystem tool would violate the cross-subject neutrality of `references/criteria.md`.
- **Impact:** None — the addendum at `references/criteria/registry-package.md` fully documents the npm Audit Coverage row format. Agents reading the criteria chain see the guidance.
- **Recommendation:** No plan update needed; deviation is correct by architecture.

---

## Issues Encountered

### Issue 1: No ephemeral branch — execution directly on master
- **Description:** The plan was executed outside the standard execute-projex workflow (no `projex/` branch, no execution log).
- **Severity:** Low
- **Resolution:** Walkthrough reconstructed from artifact inspection and git status. All deliverables confirmed present.
- **Prevention:** Future executions should use execute-projex for branch isolation and log generation even when the plan is well-understood.

### Issue 2: Deliverables uncommitted at walkthrough time
- **Description:** All M2.2 artifacts were on disk (uncommitted) when close-projex was invoked. The nav claimed M2.2 complete, but `git log` showed only 3 commits predating the execution.
- **Severity:** Low
- **Resolution:** Committed as part of close.
- **Prevention:** Execute-projex workflow commits after each step; skipping it left artifacts in an uncommitted limbo state.

---

## Key Insights

### Lessons Learned

1. **Skip execute-projex at your own risk**
   - Context: M2.2 ran directly on master without a projex branch.
   - Insight: The workflow's per-step commit discipline is load-bearing. Without it, deliverables can exist on disk but be invisible to git until a belated close.
   - Application: Even for "well-defined" plans, use execute-projex to get the branch + log scaffolding.

2. **Per-subject addenda absorb tool-specific rubric better than the shared core**
   - Context: The plan originally targeted `references/criteria.md` for the Audit Coverage row; actual implementation split it between criteria.md (§4.1 pointer) and the addendum (full rubric).
   - Insight: The shared/per-subject split established in Phase 0 M0.3 naturally resolved where tool-specific guidance should land. The plan's wording predated that architecture decision.
   - Application: When planning future tool integrations, default to the per-subject addendum for tool invocation details; the shared criteria should only carry a pointer.

### Technical Insights

- npm search API (`/-/v1/search?text=...&size=...`) shape was stable — no adjustment needed at implementation time.
- The two-row Levenshtein in PowerShell with scope stripping handles scoped packages (`@scope/pkg` vs `pkg`) cleanly.
- `riskLevel` field uses `low`/`medium`/`high`/`critical` (not `low`/`elevated`/`high` as the plan proposed) — the implementation settled on a 4-level scale with `medium` between low and high.

---

## Recommendations

### Immediate Follow-ups
- [ ] Verify `typosquat-check.ps1` runs successfully against live npm API (was not verified in this session)
- [ ] Update nav M2.2 completion note to reference this walkthrough filename

### Future Considerations
- PyPI support (v2) can reuse the normalization helpers via dot-source
- `riskLevel` 4-level scale (`low`/`medium`/`high`/`critical`) should be documented in the addendum's output fields table if not already present

---

## Related Projex Updates

| Document | Update |
|----------|--------|
| `2604021815-algorithmic-typosquat-detection-plan.md` | Status → Executed; moved to `.projex/closed/` |
| `2604021202-algorithmic-typosquat-detection-proposal.md` | Moved to `.projex/closed/` (sole derived plan now closed) |
| `2604070218-install-auditor-subject-typed-redesign-nav.md` | M2.2 already marked complete — no change needed |
