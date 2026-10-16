# Walkthrough: Eval Runner Harness

> **Execution Date:** 2026-10-16
> **Completed By:** Claude (Sonnet) execute subagent; closed by Claude (Sonnet) close subagent
> **Source Plan:** 2610161850-eval-runner-harness-plan.md
> **Parent:** 2610161850-eval-runner-harness-plan.md
> **Duration:** ~34 min execution (18:56–19:30 local), plus close
> **Result:** Success

---

## Summary

`evals/evals.json` (41 cases, 248 assertions) is now runnable and gradeable: additive `workflow` + assertion-param annotations, a stdlib-only `evals/run_evals.py` (`validate | prepare | run | grade | summary`), 12 offline unit tests, and `STEWARDSHIP.md` wiring. Deterministic grading (82 assertions) and `validate` need no credentials; live `claude -p` run and `--model-grader claude-cli` were exercised on evals 0 and 13 (~$0.42). One close-time integration fix: the snapshot test no longer pins the taxonomy-def file after the sibling rubric-consistency pass removed `.projex/` links from `SKILL.md`.

---

## Objectives Completion

| Objective | Status | Notes |
|---|---|---|
| Annotate `evals.json` (`workflow` per eval, params on deterministic assertions) | Complete | 41 `workflow` lines, 82 param-bearing assertions; round-trip check reproduces originals |
| `validate` | Complete | Exit 0, `41 evals, 248 assertions (82 deterministic, 166 model-graded)`, each workflow ≥3 |
| `prepare` (snapshot + task prompts, filters) | Complete | Snapshot outside repo; excludes `evals/`, `CLAUDE.md`, `STEWARDSHIP.md`, `.projex/closed/` |
| `run` (+ `--dry-run`) | Complete | `dontAsk` + prefix allowlist; never `bypassPermissions`; live run worked (auth available) |
| `grade` / `summary` | Complete | `grading.json` compatible layout; pending + `model_grader_prompt.md`; `model_grading.json` merge; exit 1 on failure |
| Unit tests | Complete | 12 tests (plan: 11 + `test_parse_transcript_tolerant`) |
| `STEWARDSHIP.md` step 4 + Running Evals | Complete | |

---

## Execution Detail

> Derived from git history (`2db74fa..projex/2610161850-eval-runner-harness`) and the execution log.

### Step 1: Annotate evals.json

**Planned:** one-shot text-level migration adding `workflow` per eval and params on 82 deterministic assertions.

**Actual:** plan's script run as written (kept in scratchpad, not committed); asserted `(41, 82)`. Commit `3b59907`.

**Deviation:** None.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|---|---|---|---|
| `evals/evals.json` | Modified | Yes | `123 insertions(+), 82 deletions(-)`: 41 `workflow` lines, 82 assertion lines gained `expected`/`value`/`glob`/`max` |

**Verification:** diff stat matched plan; no `contains_concept` lines removed; Python round-trip vs `git show HEAD:evals/evals.json` reproduced 41/41 eval objects; `git diff --check` clean.

**Issues:** None.

---

### Steps 2–4: Harness core, executor, grading

**Planned:** `validate`/`prepare` (Step 2), `run` (Step 3), `grade`/`summary` (Step 4) as three increments of `evals/run_evals.py`.

**Actual:** all five subcommands authored in one pass and committed together as `ac7dfeb`; per-step verification logged separately. Later `2169586` replaced `----` banner comments with plain section comments (Source Hygiene rule 4).

**Deviation:**
- One commit for three steps (log Deviations).
- `collect()` routing search widened to reports + assistant + response (live runs put `Routes to:` inside the report file). Diagnostic only.
- Usage errors exit 2 via `die()` helper (initial draft exited 1 via bare `SystemExit(str)`).
- `claude -p` was authenticated on the host (plan assumed not), so the auth-abort path was verified by code path only; real end-to-end runs done instead.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|---|---|---|---|
| `evals/run_evals.py` | Created | Yes | 932 lines; `validate`, `prepare`, `run`, `grade`, `summary`; Python 3.9 compatible, pathlib, no `shell=True` |

**Verification:**
- `validate` exit 0 with counts; `prepare --ids 0,13` produced `iteration-1/` with 28-file snapshot; `prepare --workspace <repo>/x` exit 2; `--ids 99` exit 2.
- `run --dry-run`: 2 commands, `--permission-mode dontAsk`, `bypassPermissions` count 0.
- Live `run`: eval-0 55.8 s / $0.2601 / 14 turns; eval-13 32.4 s / $0.1636; all 5 artifacts per run; stream-json keys matched parser; eval-0's attempted `curl` landed in `permission_denials` (denied by `dontAsk`).
- `grade` + `summary`: real runs eval-0 3/3 deterministic + 1 pending, eval-13 2/2 + 5 pending; hand-made E2E (eval-13 missing `## Audit Coverage`) → `summary` exit 1 listing failing assertion with evidence; live `--model-grader claude-cli` on eval-13 merged 5 concept assertions → 7/7 graded.

**Issues:** first `prepare` draft exit code (fixed, see above).

---

### Step 5: Unit tests

**Planned:** 11 `unittest` cases, offline.

**Actual:** `evals/test_run_evals.py` with plan tests 1–11 plus `test_parse_transcript_tolerant`; dry-run assertions folded into `test_dry_run_cmd` via `main(["run","--dry-run"])`. Commit `cbc064d`.

**Deviation:** +1 test (12 total).

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|---|---|---|---|
| `evals/test_run_evals.py` | Created | Yes | 270 lines at step commit; 274 after close fix |

**Verification:** `python3 -m unittest discover -s evals -p "test_*.py"` → `Ran 12 tests ... OK` (~0.1 s, offline).

**Issues:** generated `evals/__pycache__/` removed before commit.

---

### Step 6: Document in STEWARDSHIP.md

**Planned:** checklist step 4 → harness flow; `## Running Evals` before `## Record-Keeping`.

**Actual:** as planned. Commit `cd405d3`.

**Deviation:** None.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|---|---|---|---|
| `STEWARDSHIP.md` | Modified | Yes | step 4 reworded; +18-line Running Evals section (command table, agent-driven fallback, new-case param rule, self-test) |

**Verification:** `grep -c run_evals.py STEWARDSHIP.md` → 6 lines (≥5); steps 1–8 intact.

---

### Close-time work (not in plan)

**Integration fix `cbfc85e`:** between fork (`2db74fa`) and close, base advanced with plan `2610161852-dispatcher-rubric-consistency-plan.md`, which promoted the classifier rule to `references/classifier.md` and removed `.projex/` links from `SKILL.md`. `test_prepare_snapshot` asserted the snapshot contains `.projex/2604070300-install-auditor-subject-type-taxonomy-def.md`; that would fail on base after merge. Test now derives the expectation from `SKILL.md`'s `.projex/` references (via `SNAPSHOT_REF_RE`) and asserts `references/` is present. Passes pre- and post-merge. The harness code (`snapshot_files`) already handled both states.

**Nav update (repo convention):** `2604070218-install-auditor-subject-typed-redesign-nav.md` — Last Revised, Recent Progress entry, Phase 6 maintenance checklist item, § Priorities (Deferred "Eval runner tooling" line removed, resolved note added), Revision Log row. Edited from base's current nav (carrying the rubric-consistency entries) so the squash merge applies cleanly.

---

## Complete Change Log

> **Derived from:** `git diff --stat 2db74fa..projex/2610161850-eval-runner-harness` plus close commits.

### Files Created
| File | Purpose | Lines | In Plan? |
|---|---|---|---|
| `evals/run_evals.py` | Eval harness (5 subcommands) | 932 | Yes |
| `evals/test_run_evals.py` | Offline unit tests | 274 | Yes |
| `.projex/closed/2610161850-eval-runner-harness-walkthrough.md` | This record | — | Yes (close) |

### Files Modified
| File | Changes | Lines Affected | In Plan? |
|---|---|---|---|
| `evals/evals.json` | `workflow` + assertion params (additive) | +123 / -82 | Yes |
| `STEWARDSHIP.md` | step 4 + Running Evals section | +20 / -2 (net) | Yes |
| `.projex/2604070218-install-auditor-subject-typed-redesign-nav.md` | Milestone, revision log, priorities | +6 / -1 over base | No (repo convention; orchestrator) |
| `.projex/2610161850-eval-runner-harness-plan.md` → `closed/` | Status Complete, Log/Completed/Walkthrough links | — | Yes (close) |
| `.projex/2610161850-eval-runner-harness-log.md` → `closed/` | Moved | — | Yes (close) |

### Files Deleted
None.

### Planned But Not Changed
None.

---

## Success Criteria Verification

### Criterion 1: Every eval has `workflow`; params present; originals byte-identical
**Verification Method:** Step 1 round-trip script; `validate`.
**Evidence:** 41/41 objects reproduced after stripping `workflow` + params; `validate` exit 0.
**Result:** PASS

### Criterion 2: `validate` exits 0 with counts and per-workflow ≥3
**Evidence (re-run at close):**
```
41 evals, 248 assertions (82 deterministic, 166 model-graded)
agent-extension: 3 | browser-extension: 3 | ci-action: 4 | cli-binary: 3 | container-image: 4
desktop-app: 3 | generic: 3 | ide-plugin: 4 | registry-package: 11 | remote-integration: 3
validate exit=0
```
**Result:** PASS

### Criterion 3: `prepare` isolation + filters
**Evidence:** snapshot holds `SKILL.md`, `workflows/`, `references/`, `scripts/` (+ referenced `.projex` files on the forked tree); none of `evals/`, `CLAUDE.md`, `STEWARDSHIP.md`, `.projex/closed/`; `--ids 0,13`, `--workflow generic` (3 evals) work; workspace inside repo → exit 2 (re-run at close).
**Result:** PASS

### Criterion 4: `run --dry-run` uses `dontAsk`, restricted allowlist, never `bypassPermissions`
**Evidence (re-run at close):** 2 commands printed, exit 0, `grep -c bypassPermissions` → 0; `test_dry_run_cmd` asserts no bare `Bash` / `Bash(pwsh:*)`.
**Result:** PASS

### Criterion 5: `run` aborts exit 2 without auth; produces 5 artifacts with auth
**Evidence:** host was authenticated; live run produced `response.md`, `assistant_text.md`, `transcript.jsonl`, `timing.json`, `run_meta.json` for evals 0 and 13. Unauthenticated abort path implemented but not exercised (no failing auth available to provoke).
**Result:** PASS (abort branch verified by code path only)

### Criterion 6: `grade` output, pending, prompt, merge
**Evidence:** `grading.json` with `expectations[].text/passed/evidence`, `summary.pass_rate`, `pending`, `model_grader_prompt.md`; `model_grading.json` merge unit-tested and exercised live via `claude-cli`.
**Result:** PASS

### Criterion 7: `summary` files and exit code
**Evidence:** `summary.md` + `summary.json` written; hand-made failing E2E → exit 1 with assertion and evidence; clean run → exit 0.
**Result:** PASS

### Criterion 8: Unit tests pass offline
**Evidence (re-run at close, post-fix):** `Ran 12 tests in 0.087s` `OK`.
**Result:** PASS

### Criterion 9: `STEWARDSHIP.md` step 4 names commands; credential split documented
**Evidence:** `grep -c run_evals.py STEWARDSHIP.md` → 6 lines; Running Evals table has a "Needs a model" column.
**Result:** PASS

### Acceptance Criteria Summary

| Criterion | Method | Result | Evidence |
|---|---|---|---|
| evals.json annotated | Round-trip vs HEAD | Pass | Step 1 |
| `validate` | Run | Pass | exit 0 + counts |
| `prepare` | Run + test | Pass | snapshot tree |
| `run --dry-run` | Run + test | Pass | dontAsk, 0 bypass |
| `run` auth abort / artifacts | Live | Pass (abort by code path) | 2 live evals |
| `grade` | Tests + live | Pass | grading.json |
| `summary` | E2E | Pass | exit 1 on failure |
| Offline tests | unittest | Pass | 12 OK |
| STEWARDSHIP | grep | Pass | 6 lines |

**Overall:** 9/9 criteria passed.

---

## Deviations from Plan

### Deviation 1: `Worktree: No` → `Yes`
- **Planned:** checkout-mode execution.
- **Actual:** worktree mode (orchestrator override; sibling plans executing concurrently).
- **Impact:** none on content; close uses `--worktree`.

### Deviation 2: Steps 2–4 in one commit
- **Impact:** coarser history; squash merge makes this moot.

### Deviation 3: Routing search widened; usage errors exit 2
- **Impact:** diagnostic accuracy; exit-code contract matches plan.

### Deviation 4: Live auth available
- **Impact:** real end-to-end evidence (~$0.42) instead of abort-path evidence.

### Deviation 5: Close-time test fix (`cbfc85e`) and nav update
- **Reason:** base advanced (`5c44b79`) and invalidated a snapshot-test assumption; nav is the repo's milestone record.
- **Impact:** test robust to both `SKILL.md` states.

---

## Issues Encountered

### Issue 1: Bare `SystemExit(str)` exit code 1
- **Severity:** Low. **Resolution:** `die()` helper → exit 2. **Prevention:** contract tests on exit codes.

### Issue 2: Cross-plan interaction with rubric-consistency pass
- **Description:** snapshot test hardcoded a `.projex/` taxonomy-def file that the sibling plan unlinked from `SKILL.md`.
- **Severity:** Medium (would have landed a failing test on base). **Resolution:** `cbfc85e`. **Prevention:** derive snapshot expectations from the content under test rather than a named file.

### Issue 3: Close tooling gaps (environment)
- **Description:** `close-precheck.sh` returned `ERROR=recorded Worktree Path is missing or inaccessible` because the log's `Worktree Path` is repo-name-relative (`install-auditor-skill/.projexwt/...`); from the base checkout it returned `execution log is missing or inaccessible` (log lives on the ephemeral branch). `projex-tree.sh` fails: `.projex-tree.py` helper absent from the framework directory (and `projex-tree.sh` is not executable). Both advisory; close proceeded on direct git evidence.
- **Severity:** Low. **Prevention:** record absolute-or-repo-relative `Worktree Path` in logs; ship `.projex-tree.py`.

---

## Key Insights

**Rationale promoted:** `STEWARDSHIP.md` § Running Evals (workspace-outside-repo, credential split, param rule). Remaining rationale lives in `evals/run_evals.py` docstring.

### Lessons Learned

1. **Merged plans interact through tests**
   - Context: two concurrent plans touched `SKILL.md` links and a test pinned them.
   - Insight: tests over live repo content should derive expectations from that content.
   - Application: check sibling plans' base deltas before close; run the suite on the merged tree.

2. **Plan assumptions about auth were wrong in the helpful direction**
   - Insight: verify env assumptions at execution, not at plan time.

### Pattern Discoveries

1. **Snapshot + out-of-repo workspace**
   - Observed in: `prepare`.
   - Description: copy a tracked-file subset to a workspace outside the repo to avoid ancestor `CLAUDE.md` leakage and answer leakage from `.projex/closed/`.
   - Reuse potential: any agent-run eval harness.

### Gotchas / Pitfalls

1. **Hostile prompts in eval corpus**
   - Trap: eval prompts contain `curl ... | sh`.
   - How encountered: eval-0 attempted `curl`; denied by `dontAsk`.
   - Avoidance: never `bypassPermissions`; prefix-scoped allowlist.

### Technical Insights

- `total_tokens` in `timing.json` = input+output only (excludes cache tokens).
- `claude -p` stream-json `result` event carries `result`, `total_cost_usd`, `usage`, `duration_ms`, `permission_denials`.

---

## Recommendations

### Immediate Follow-ups
- [ ] Full 41-eval baseline run and record pass rates (cost not yet measured; ~$0.2/eval observed)
- [ ] Add eval cases for typosquat false-positive and tag-pinned verified action (carried from rubric-consistency follow-ups; `validate` will require `workflow` + params)
- [ ] Add `.projex-tree.py` to the framework or fix `projex-tree.sh`; make logs' `Worktree Path` resolvable by `close-precheck.sh`

### Future Considerations
- `contains_concept` for "strong warnings" in ids 2, 9 (currently only the verdict set is graded)
- Task-prompt template still lists `.projex/` among skill-relative roots; harmless now that `SKILL.md` no longer links into `.projex/`
- Baseline/old-skill comparison runs, variance, CI integration (out of scope here)

### Plan Improvements
- Note sibling plans' touch on `SKILL.md` link structure when a test reads repo content.
- Do not assume `claude -p` auth state; plan both branches.

---

## Related Projex Updates

### Documents to Update
| Document | Update Needed |
|---|---|
| 2610161850-eval-runner-harness-plan.md | Complete; links added; moved to `closed/` |
| 2610161850-eval-runner-harness-log.md | Status Complete; moved to `closed/` |
| 2604070218-install-auditor-subject-typed-redesign-nav.md | Updated in place (not closed) |
| 2610161849-python-script-ports-plan.md | Untouched (still executing) |

### New Projex Suggested
| Type | Description |
|---|---|
| Plan | Full-suite baseline eval run + eval cases for typosquat false-positive and tag-pinned verified action |
| Patch | Framework: ship `.projex-tree.py`; align `close-precheck` with log `Worktree Path` convention |

---

## Appendix

### References
- Commits on the ephemeral branch: `3b59907` (step 1), `ac7dfeb` (steps 2–4), `cbc064d` (step 5), `cd405d3` (step 6), `2169586` (quality), `671b87b` (complete), `cbfc85e` (close-time test fix), close-docs commit
- Base at close: `5c44b79`
- Execution log: 2610161850-eval-runner-harness-log.md
