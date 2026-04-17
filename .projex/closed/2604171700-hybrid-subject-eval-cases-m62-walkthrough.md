# Walkthrough: M6.2 — Hybrid-Subject Eval Cases

> **Execution Date:** 2026-04-17
> **Completed By:** Claude (orchestrate-projex)
> **Source Plan:** 2604171700-hybrid-subject-eval-cases-m62-plan.md
> **Duration:** ~5 min
> **Result:** Success

---

## Summary

Added 5 hybrid-subject eval cases (ids 36-40) to `evals/evals.json`, bringing total to 41. Each case exercises the "innermost trust boundary" classifier rule from the taxonomy def, testing correct routing for the five canonical hybrid scenarios. All success criteria passed. No deviations.

---

## Objectives Completion

| Objective | Status | Notes |
|-----------|--------|-------|
| 41 cases, ids 0-40 sequential, no duplicates | Complete | Confirmed via JSON parse |
| 3 nav-specified hybrids present | Complete | ids 36 (npm CLI), 37 (VS Code+binary), 38 (Docker+npm) |
| 2 additional taxonomy hybrids | Complete | ids 39 (Action+Docker), 40 (skill via npm) |
| Each case asserts correct innermost type | Complete | 6 assertions per case including routing + type |
| Each case asserts decoy type not chosen | Complete | All 5 have negative-routing assertion |

---

## Execution Detail

### Step 1: Add 5 Hybrid Eval Cases (ids 36-40)

**Planned:** Append ids 36-40 to the `evals` array in one commit.

**Actual:** Appended exactly as specced. Each case:
- Prompt surfaces the dual-type ambiguity explicitly (user asks "should I treat this as X or Y?")
- `expected_output` names the correct innermost type and explains the boundary rule
- 6 assertions: correct type (contains_concept), not-decoy-type (contains_concept), boundary explanation, secondary concern mention, verdict_check, `## Audit Coverage`

**Deviation:** None.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `evals/evals.json` | Modified | Yes | Appended ids 36-40 (+70 lines) |

**Verification:** JSON parsed cleanly. 41 entries, ids 0-40 sequential, unique. All 5 new cases have 6 assertions with negative-routing checks.

**Issues:** None.

---

## Complete Change Log

> **Derived from:** `git diff --stat master..projex/2604171700-hybrid-subject-eval-cases-m62`

### Files Modified
| File | Changes | Lines Affected | In Plan? |
|------|---------|----------------|----------|
| `evals/evals.json` | Appended 5 hybrid eval objects | +70 lines | Yes |
| `.projex/2604171700-hybrid-subject-eval-cases-m62-plan.md` | Status In Progress → Complete | 1 line | Yes (by execute-projex) |

---

## Success Criteria Verification

| Criterion | Method | Result | Evidence |
|-----------|--------|--------|----------|
| 41 cases, sequential ids | JSON parse + count | Pass | `Total: 41, Sequential: true, Unique: true` |
| 3 nav hybrids | Inspect ids 36-38 | Pass | npm-CLI→registry-package, VS Code+binary→ide-plugin, Docker+npm→container-image |
| 2 additional hybrids | Inspect ids 39-40 | Pass | Action+Docker→ci-action, skill-via-npm→registry-package |
| Correct innermost type assertions | Manual review | Pass | Each has `contains_concept` asserting correct type |
| Decoy-type negative assertions | Check `has-negative-assertion` | Pass | All 5 have `not [decoy-type]` assertion |

**Overall: 6/6 criteria passed.**

---

## Key Insights

### Technical Insights

- The 5 taxonomy worked hybrid examples map cleanly to realistic user prompts — no synthetic cases needed.
- Prompt framing that asks "should I treat this as X or Y?" is intentionally explicit; this tests rule application, not inference from minimal context. Harder "stealth hybrid" cases (no explicit user framing) are a natural M6.3 extension.
- The negative assertion pattern (`routes to X workflow, not Y`) is a reusable template for future hybrid evals.

---

## Recommendations

### Immediate Follow-ups
- [ ] M6.3 — Stewardship cadence (schedule periodic rubric re-evaluation)

---

## Related Projex Updates

| Document | Update |
|----------|--------|
| `2604171700-hybrid-subject-eval-cases-m62-plan.md` | Status → Complete; walkthrough linked |
| `2604070218-install-auditor-subject-typed-redesign-nav.md` | M6.2 ✓; revision log entry added |
