# Walkthrough: Eval Suite Refresh — Rubric Re-expectation + 2025–26 Attack Cases

> **Execution Date:** 2026-10-17
> **Completed By:** Claude (executor subagent; closed by close-projex subagent)
> **Source Plan:** 2610170504-eval-suite-refresh-plan.md
> **Parent:** 2610170504-eval-suite-refresh-plan.md
> **Duration:** ~7 min (05:11–05:18 sandbox clock)
> **Result:** Success

---

## Summary

`evals/evals.json` now matches the refreshed rubrics: 8 time-dependent APPROVED cases got calendar-robust guard assertions, rubric-conflicting cases (22, 33, 39) were recalibrated, eval 34 re-routed to cli-binary, and 20 new cases (ids 41–60) cover 2025–26 attack patterns. Suite: 41 → 61 evals, 248 → 362 assertions (126 deterministic / 236 model-graded). All offline gates pass; no paid run was made.

---

## Objectives Completion

| Objective | Status | Notes |
|-----------|--------|-------|
| Calendar-robust assertions for ids 0, 11, 16, 18, 20, 26, 36, 37 | Complete | `exact_match APPROVED` → `verdict_check [APPROVED, CONDITIONAL]` + guard concept; 8 occurrences of guard text |
| Recalibrate rubric conflicts (22, 39, 33) + sync stale descriptions (8, 12, 14, 24, 29, 31, 32, 35) | Complete | 22 → Tier 2 CONDITIONAL; 39 → CONDITIONAL + SHA-pin concept; 33 gained CONDITIONAL + condition concept |
| Re-route eval 34 to cli-binary; add generic case 60 | Complete | Atomic (generic stays at minimum 3) |
| Add 19 attack-pattern cases (41–59) | Complete | Per-step paper traces logged with rule cited per id |
| Update self-test count tuple; run offline gates | Complete | `(41, 248, 82, 166)` → `(61, 362, 126, 236)` |

---

## Execution Detail

> Derived from git history and the execution log; re-verified at close.

### Step 1: Calendar-robust assertions for time-dependent exact-APPROVED cases

**Planned:** Apply guard pattern to ids 0, 11, 16, 18, 20, 26, 36, 37; replace `expected_output` (id 0 assertion text and id 37 prompt also edited).

**Actual:** As planned via a scratch Python script with a byte-exact round-trip serializer (unmodified round trip verified identical). Commit `194abee`.

**Deviation:** None.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `evals/evals.json` | Modified | Yes | 8 cases: assertion swap + guard insert, `expected_output` rewrites; id 0 assertion extended; id 37 prompt reworded |

**Verification:** `validate` → `41 evals, 256 assertions (82 deterministic, 174 model-graded)`; `grep -c "an APPROVED verdict passes this check"` → 8.

**Issues:** A1 (grader accepts verdict line as quotable evidence) judged acceptable by reading `MODEL_GRADER_INSTRUCTIONS`; only a live run can confirm.

---

### Step 2: Recalibrate rubric conflicts and sync stale descriptions

**Planned:** Replace eval 22; 39 → CONDITIONAL; 33 gains verdict; 24 Slack rename; `expected_output` edits for 12, 8, 14, 29, 31, 32, 35.

**Actual:** As planned; every substring replacement asserted to match exactly once. Commit `9450eb1`.

**Deviation:** None.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `evals/evals.json` | Modified | Yes | Assertion changes limited to ids 22, 24, 33, 39; `expected_output`/prompt text for 8, 12, 14, 22, 24, 29, 31, 32, 33, 35, 39 |

**Verification:** `validate` → `41 evals, 260 assertions (83 deterministic, 177 model-graded)`; `grep -c "Anthropic-maintained MCP"` → 0; `grep -c "Slack App Directory at"` → 0.

**Issues:** None.

---

### Step 3: Re-route eval 34 to cli-binary and add generic case 60 (atomic)

**Planned:** 34: `workflow` generic → cli-binary, routing assertion + `expected_output` replaced; append id 60 (root-CA email, generic).

**Actual:** Both hunks in one commit `1200874`; 60 appended at file end.

**Deviation:** None.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `evals/evals.json` | Modified | Yes | Eval 34 re-routed; eval 60 added |

**Verification:** `validate` → `42 evals, 266 assertions (86 deterministic, 180 model-graded)`; `cli-binary: 4`, `generic: 3`.

**Issues:** None.

---

### Step 4: Add 19 attack-pattern cases (ids 41–59)

**Planned:** Append 19 plan-literal objects; paper-trace each against current addenda.

**Actual:** Objects inserted before id 60 in id order (plan allowed either). Traced each row against the worktree's addenda; rule cited per id in the log (e.g. registry-package §4.6 V4(a) for 41/42; ci-action "Toward REJECTED" list for 43/44; Open VSX trust boundary for 48; frozen namespace for 49). Spot-read prompts 41, 43, 55: none states its expected verdict. Commit `4e0a23c`.

**Deviation:** None (insertion position is a plan-sanctioned choice). Note: 54's `SessionStart` is not named literally in the rubric; the hook shell-surface rule applies.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `evals/evals.json` | Modified | Yes | +267 lines, ids 41–59 |

**Verification:** `validate` → `61 evals, 362 assertions (126 deterministic, 236 model-graded)`; per-workflow counts equal Success Criteria.

**Issues:** None.

---

### Step 5: Update self-test counts and run offline gates

**Planned:** Update pinned tuple; run invariants, validate, unittest, json.tool, optional dry `prepare`.

**Actual:** Done; `prepare --ids 22,26,34,41,60` into a scratchpad workspace (5 dirs, no model call), workspace and `__pycache__` removed. Commit `33de351`; completion commit `b116a76`.

**Deviation:** None.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `evals/test_run_evals.py` | Modified | Yes | Count tuple `(41, 248, 82, 166)` → `(61, 362, 126, 236)` |

**Verification:** see Success Criteria below.

**Issues:** None.

---

## Complete Change Log

> **Derived from:** `git diff --stat 2f4cfbd...projex/2610170504-eval-suite-refresh` (three-dot / merge-base `2f4cfbd`). Two-dot against base tip `dec2f83` shows the sibling consistency close as inverse noise.

### Files Created
| File | Purpose | Lines | In Plan? |
|------|---------|-------|----------|
| `.projex/2610170504-eval-suite-refresh-log.md` | Execution log (moved to `closed/` at close) | 101 | Yes |

### Files Modified
| File | Changes | Lines Affected | In Plan? |
|------|---------|----------------|----------|
| `evals/evals.json` | 21 existing cases edited, 20 added | +332 / −38 | Yes |
| `evals/test_run_evals.py` | Pinned count tuple | +1 / −1 | Yes |
| `.projex/2610170504-eval-suite-refresh-plan.md` | Status/Log header | +2 / −1 | Yes |

### Files Deleted
None.

### Planned But Not Changed
None.

---

## Success Criteria Verification

Re-run by the closer on the branch tip `b116a76` before squash.

### Criterion 1: `validate` prints the new totals and per-workflow counts

**Verification Method:** `python3 evals/run_evals.py validate` in the worktree.

**Evidence:**
```
61 evals, 362 assertions (126 deterministic, 236 model-graded)
agent-extension: 7 | browser-extension: 5 | ci-action: 7 | cli-binary: 6
container-image: 5 | desktop-app: 4 | generic: 3 | ide-plugin: 5
registry-package: 13 | remote-integration: 6
```

**Result:** PASS

### Criterion 2: evals unittest passes

**Evidence:** `python3 -m unittest discover -s evals -p "test_*.py"` → `Ran 12 tests ... OK`.

**Result:** PASS

### Criterion 3: Step 5 invariant script prints `OK`

**Evidence:** Plan's script run verbatim from the worktree → `OK`.

**Result:** PASS

### Criterion 4: diff scope limited to `evals/evals.json` and `evals/test_run_evals.py`

**Evidence:** `git diff --stat 2f4cfbd...branch` → `evals/evals.json`, `evals/test_run_evals.py`, plus this execution's own `.projex/` log and plan (doc-only).

**Result:** PASS

### Criterion 5: No `run` / `claude -p` invocation

**Evidence:** Execution log: only `validate`, unittest, `json.tool` and `prepare` (no model call).

**Result:** PASS

### Acceptance Criteria Summary

| Criterion | Method | Result | Evidence |
|-----------|--------|--------|----------|
| Counts | `validate` | Pass | 61 / 362 / 126 / 236 |
| Self-test | unittest (evals) | Pass | 12 tests OK |
| Decisions encoded | invariant script | Pass | `OK` |
| Scope | `git diff --stat` | Pass | 2 code files + own projex docs |
| No paid run | execution log | Pass | none invoked |

**Overall:** 5/5 criteria passed. Extra close checks: `python3 -m unittest discover -s tests` → 23 OK (8 pre-existing skips); `python3 -m json.tool evals/evals.json` OK; close-precheck `RESULT=PASS` (both gates).

---

## Deviations from Plan

None affecting outcomes. Process notes: no task-list tool available (log + commits tracked progress); edits done via scratch script with byte-exact serializer; ids 41–59 inserted before 60 (plan-allowed).

---

## Issues Encountered

### Issue 1: Base advanced during execution
- **Description:** Sibling consistency plan closed onto base (`dec2f83`) after this branch was cut from `2f4cfbd`.
- **Severity:** Low
- **Resolution:** Its files (`SKILL.md`, `references/`, `workflows/`, `scripts/`, `STEWARDSHIP.md`, sibling `.projex/` docs) are disjoint from `evals/`; A3 re-checked against the advanced tip (`Version integrity` and `## Audit Coverage` still present in `SKILL.md` and `references/report-template.md`). Post-merge `validate` and tests re-run at close.
- **Time Impact:** None
- **Prevention:** Use three-dot diffs when comparing against a moving base.

### Issue 2: Executor report lost
- **Description:** Container restart lost the executor's final report after it had finished.
- **Severity:** Low
- **Resolution:** Orchestrator and closer re-verified from branch state and the execution log.
- **Time Impact:** Minor
- **Prevention:** Executors should rely on the log as the durable record (it was complete).

---

## Key Insights

**Rationale promoted:** none needed (no source files changed; eval data only).

### Lessons Learned

1. **Guard assertions keep "APPROVED expected" meaningful while tolerating V1/C6 CONDITIONAL**
   - Context: unpinned subjects drift with the calendar (fresh releases, new non-KEV HIGH CVEs).
   - Insight: `verdict_check [APPROVED, CONDITIONAL]` plus a concept assertion naming the only acceptable causes beats date-pinned prompts.
   - Application: reuse for any future eval on an unpinned popular subject.

2. **Round-trip serializer before bulk JSON edits**
   - Context: 41 → 61 cases edited by script.
   - Insight: verifying byte-identical round trip first keeps diffs reviewable.
   - Application: do the same for any large generated-edit pass over `evals/evals.json`.

### Pattern Discoveries

1. **Fictional subject + decisive facts in prompt + tolerant verdict set**
   - Observed in: new cases 42, 44–47, 50, 52–55, 58–60.
   - Description: registry lookups fail for invented names; prompts carry the evidence, and verdict sets accept "not found" pushing toward REJECTED.
   - Reuse potential: any attack-pattern eval that must not depend on live registry state.

### Gotchas / Pitfalls

1. **Generic workflow sits at the `MIN_CASES_PER_WORKFLOW = 3` floor**
   - Trap: any future generic re-route fails `validate`.
   - How encountered: moving eval 34 required adding case 60 in the same commit.
   - Avoidance: pair re-routes with replacement cases atomically.

2. **Two-dot diff against a moved base shows sibling changes as inverse noise**
   - Avoidance: use `base...branch` or the merge-base.

### Technical Insights

- Residual risk A1: the model grader's acceptance of the verdict line as quotable evidence for "an APPROVED verdict passes this check" is unconfirmed until the live run.
- After the sibling consistency plan, headings read `4.1`–`4.6` without `§` while `§4.6`/`§4.3` citations remain in `SKILL.md` and rubric text; the guard wording stays matchable (logged, no action).

---

## Recommendations

### Immediate Follow-ups
- [ ] Live paid run over all 61 evals — human-approved (~$12–15, per-eval cap `--max-budget-usd 0.6`). Runs after this close; not part of this plan. Pre-run: note latest release dates of express, uBlock Origin, Prettier, Firefox, ripgrep, redis (DOI), rust-analyzer, uv so a CONDITIONAL on guarded cases can be matched to V1.
- [ ] After the live run, confirm A1 and adjust the guard wording if the grader rejects verdict-line evidence.

### Future Considerations
- Deferred candidates (see plan Notes → Deferred candidates): Homebrew routing cases, per-sub-rubric (8a/8b/8c) minimum in `validate` (needs a `subrubric` field), further per-workflow attack shapes.

### Plan Improvements
If this plan were to be executed again:
- State the id-ordering choice for 41–60 up front instead of leaving it to the executor.

---

## Related Projex Updates

### Documents to Update
| Document | Update Needed |
|----------|---------------|
| 2610170504-eval-suite-refresh-plan.md | Complete; links to walkthrough and log; moved to `closed/` |
| 2610170504-eval-suite-refresh-log.md | Status Complete; moved to `closed/` |
| 2604070218-install-auditor-subject-typed-redesign-nav.md | Not referenced by the plan — untouched |
| Five 2610161927/28 stewardship review evals | Left active: inputs to multiple plans, not resolved by this plan alone (two already `Complete`, three `Draft`); no link change needed |

### New Projex Suggested
| Type | Description |
|------|-------------|
| Plan | Next-cycle eval additions from plan Notes → Deferred candidates (incl. Homebrew routing cases) |
| Plan | Per-sub-rubric minimum in `evals/run_evals.py validate` (`subrubric` field) |

---

## Appendix

### Human Decisions
- Live paid run approved for the full 61 evals (~$12–15; per-eval cap $0.60); runs after this close.
- Orchestrator (acting as user) accepted the execution; squash merge chosen.

### References
- Step commits: `194abee`, `9450eb1`, `1200874`, `4e0a23c`, `33de351`, completion `b116a76` on `projex/2610170504-eval-suite-refresh` (fork point `2f4cfbd`, base tip at close `dec2f83`).
