# Execution Log: Eval Suite Refresh

> **Status:** Complete
> **Started:** 20261017 05:11
> **Repo Root:** /home/user/install-auditor-skill
> **Plan File:** .projex/2610170504-eval-suite-refresh-plan.md
> **Parent:** 2610170504-eval-suite-refresh-plan.md
> **Base Branch:** claude/youthful-dijkstra-5ov1kt
> **Worktree Path:** .projexwt/2610170504-eval-suite-refresh

## Pre-Check Results

```
REPO_ROOT=/home/user/install-auditor-skill
BRANCH=claude/youthful-dijkstra-5ov1kt
PLAN_REL=.projex/2610170504-eval-suite-refresh-plan.md

PASS  Plan is committed (28ad836 projex: add plan - eval-suite-refresh)
PASS  Working tree is clean

PRE-CHECK PASSED
```

## Setup

- Plan status set `In Progress` on base (2f4cfbd). Worktree + branch `projex/2610170504-eval-suite-refresh` created via `projex-worktree.sh`.
- Bootstrap: none needed — pure Python 3 stdlib, no gitignored deps. Baseline `validate` in worktree: `41 evals, 248 assertions (82 deterministic, 166 model-graded)`.
- Edit method: Python script (scratchpad, outside repo) that loads `evals/evals.json`, mutates, and re-serializes with a custom dumper. Round-trip of the unmodified file was verified byte-identical, so layout is preserved.
- No task-list tool available in this environment; the plan's steps and this log serve as the tracker.
- No live runs (`run_evals.py run` / `claude -p`) are performed in this execution.

## Steps

### [20261017 05:12] - Step 1: Calendar-robust assertions for time-dependent exact-APPROVED cases
**Action:** Script applied the guard pattern to ids 0, 11, 16, 18, 20, 26, 36, 37 (`exact_match APPROVED` → `verdict_check [APPROVED, CONDITIONAL]` + guard `contains_concept` G inserted right after); replaced `expected_output` on all 8; id 0 assertion text extended; id 37 prompt reworded. Self-executed (no do-projex/verify-projex sub-subagent).
**Result:** `validate` → `41 evals, 256 assertions (82 deterministic, 174 model-graded)` (matches plan). `grep -c "an APPROVED verdict passes this check" evals/evals.json` → 8. `git diff` reviewed: only the 8 cases touched; assertion layout preserved. A1 read: `MODEL_GRADER_INSTRUCTIONS` requires a quotable evidence span; for an APPROVED report the span is the report's `**Verdict:**` line, which the grader sees in the report text — judged acceptable; only a live run can confirm (residual risk already listed in plan Risks).
**Status:** Success

### [20261017 05:12] - Step 2: Recalibrate rubric conflicts and sync stale descriptions
**Action:** Script replaced eval 22 wholesale (plan literal); eval 39 `exact_match APPROVED` → `verdict_check [CONDITIONAL]` + SHA-pin concept + new `expected_output`; eval 33 gained `verdict_check [CONDITIONAL]` and condition concept after the classifier-uncertainty assertion, new `expected_output`; eval 24 prompt/assertion/`expected_output` renamed to Slack Marketplace + appended hosted-service sentence; `expected_output` edits for 12, 8 (append), 14 (append), 29, 31, 32 (append), 35. Self-executed, self-verified (no verify-projex sub-subagent).
**Result:** `validate` → `41 evals, 260 assertions (83 deterministic, 177 model-graded)` (matches plan). `grep -c "Anthropic-maintained MCP"` → 0; `grep -c "Slack App Directory at"` → 0. Diff reviewed: assertion changes limited to ids 22, 24, 33, 39; every substring replacement matched exactly once (script asserts).
**Status:** Success

### [20261017 05:13] - Step 3: Re-route eval 34 to cli-binary and add generic case 60 (atomic)
**Action:** One script run: eval 34 `workflow` generic → cli-binary, routing assertion replaced with `Subject type is cli-binary (PowerShell pipe-to-shell installer)`, `expected_output` replaced; eval 60 (root-CA email, generic) appended at file end. Both hunks in the same commit. Self-executed.
**Result:** `validate` → `42 evals, 266 assertions (86 deterministic, 180 model-graded)`; `cli-binary: 4`, `generic: 3` (matches plan). `git diff --stat`: only `evals/evals.json`.
**Status:** Success

### [20261017 05:14] - Step 4: Add 19 attack-pattern cases (ids 41-59)
**Action:** Wrote the 19 plan-literal objects to a scratchpad JSON (outside repo), inserted before id 60 in id order via the round-trip serializer. Paper-traced each table row against the current addenda in the worktree (grep of rule text; rule cited below). Self-executed, self-verified (no verify-projex sub-subagent).
**Result:** `validate` → `61 evals, 362 assertions (126 deterministic, 236 model-graded)`; per-workflow `agent-extension: 7`, `browser-extension: 5`, `ci-action: 7`, `cli-binary: 6`, `container-image: 5`, `desktop-app: 4`, `generic: 3`, `ide-plugin: 5`, `registry-package: 13`, `remote-integration: 6` (all match plan). `git diff --stat`: only `evals/evals.json`, 267 insertions, 19 new ids.
Paper traces (rule found ✓ in current text):
- 41, 42 registry-package: `references/criteria.md` §4.6 V4(a) "version to be installed is in the affected range" → REJECTED (✓ line 296); V1/V3 per §4.6 (42 verdict set is CONDITIONAL|REJECTED, never APPROVED). `Version integrity` and `## Audit Coverage` present in `SKILL.md`/`references/report-template.md` (A3 ✓).
- 43 ci-action: `workflows/ci-action.md` "Toward REJECTED": non-SHA ref from unverified third-party publisher with write scopes/secrets ✓; plus V4(a).
- 44 ci-action: "Toward REJECTED": fork PR code checked out in `pull_request_target` then executed (pwn request) ✓; cache written by untrusted-input job then restored by release/publish/`id-token: write` job ✓.
- 45 ci-action: SHA must be "reachable from the named repo, not only from a fork" (Ref integrity ✓); unknown ref + publish token → REJECTED.
- 46, 47 browser-extension: V3 ownership transfer plug-in (workflows/browser-extension.md addendum ref ✓); AI-chat data-disclosure check ("Where does page data go? … AI-chat" ✓). Verdict sets CONDITIONAL|REJECTED.
- 48 ide-plugin: forks use Open VSX as the registry; Open VSX namespace verification check ✓.
- 49 container-image: "Frozen namespaces … `bitnamilegacy` … HIGH flag" and "Frozen / legacy namespace: Condition — move to a maintained source" ✓ → CONDITIONAL.
- 50 cli-binary: Install-command lure + lookalike-domain install URL → CRITICAL/Red Flag ✓ (workflows/cli-binary.md verdict notes).
- 51 cli-binary: PowerShell `irm | iex` listed as pipe-to-shell form; Tier 3 trigger; known vendor docs path not an auto-REJECT ✓ (set APPROVED|CONDITIONAL).
- 52 desktop-app: notarization-with-unmatched-identity rule (workflows/desktop-app.md "signature (even notarized) whose identity cannot be tied to the…" ✓).
- 53, 55 agent-extension: addendum CRITICAL list names "prerequisite installer lure" and "tool poisoning or exfiltration steering" ✓. 54: shell surface that runs unattended / remote-fetching shell surface CRITICAL ✓ (`SessionStart` is not named literally; hook shell-surface rule applies). 56: classifier row "Remote MCP server … `claude mcp add --transport http`" → agent-extension (8a) ✓.
- 57, 58, 59 remote-integration: "connection code someone else supplied" ✓, "Unresolved token theft at the integration vendor" ✓, "data sent to unnamed AI providers" in the Toward-REJECTED list (so 59's set CONDITIONAL|REJECTED is consistent) ✓.
Spot-read prompts 41, 43, 55: none states the expected verdict or labels the subject malicious/poisoned.
**Status:** Success

### [20261017 05:15] - Step 5: Update self-test counts and run offline gates
**Action:** `evals/test_run_evals.py` pinned tuple `(41, 248, 82, 166)` → `(61, 362, 126, 236)`. Ran the plan's invariant script, `validate`, both unittest suites, `json.tool`, and the optional dry `prepare --ids 22,26,34,41,60` into a scratchpad workspace (outside repo; no `run`, no `claude -p`). Removed the workspace and the `__pycache__` dirs the test runs created in the worktree. Self-executed.
**Result:** invariant script → `OK`. `validate` → `61 evals, 362 assertions (126 deterministic, 236 model-graded)` with per-workflow counts as in Success Criteria. `python3 -m unittest discover -s evals -p "test_*.py"` → 12 tests OK. `python3 -m unittest discover -s tests` → 23 tests OK (8 skipped, pre-existing skips). `python3 -m json.tool evals/evals.json` → OK. `prepare` created 5 eval dirs, no model call. Step 5 `git diff --stat`: `evals/test_run_evals.py` only (`evals/evals.json` already committed in steps 1-4).
**Status:** Success

### [20261017 05:18] - Completion: full verification, spec compliance, quality review, cleanup
**Action:** Re-ran all gates on the final tree; checked every Success Criterion; re-read the plan's constraints; reviewed the full branch diff (`git diff base...branch`); removed agent-created ignored files.
**Result:**
- `validate` → `61 evals, 362 assertions (126 deterministic, 236 model-graded)`; per-workflow counts equal the Success Criteria list. unittest (evals) 12 OK; unittest (tests) 23 OK (8 skipped, pre-existing); invariant script `OK`; `json.tool` OK.
- Scope: `git diff --stat base...branch` → `evals/evals.json`, `evals/test_run_evals.py` plus this execution's own `.projex/` log/plan (doc-only). No `run`/`claude -p` invocation anywhere (only `prepare`, which makes no model call).
- Spec compliance: plan constraints met (<= 20 new cases: 20 incl. generic 60; no live runs; robust assertions via guard; human decisions C4/C6 encoded in the 26/12/others' `expected_output`). Plan Out-of-Scope files untouched.
- Quality review: JSON layout byte-compatible with prior style; every new case has a verdict assertion + `## Audit Coverage` (invariant script); no projex filenames or ids leak into `evals/evals.json`; new prompts do not state their expected verdict.
- Cleanup: removed the dry-run workspace and `evals/__pycache__`, `tests/__pycache__` in the worktree; worktree has no untracked/ignored leftovers. Scratch scripts live only in the shared scratchpad subdirectory `exec-evals-2610170504/` (outside repo).
**Status:** Success

## Deviations

- None affecting outcomes. Process notes: (a) no task-list tool was available, so the log + commits served as the tracker; (b) edits were done with a scratch Python script and a byte-exact round-trip serializer rather than hand edits; (c) cases 41-59 were inserted before 60 in id order (plan allowed either).
- Step timestamps in this log are wall-clock from the sandbox (`date`).

## Issues Encountered

- Base advanced during execution: the sibling consistency plan closed onto base (`dec2f83`, `fix(runtime): reconcile cross-plan consistency ...`) after this branch was cut from `2f4cfbd`. Its files (`SKILL.md`, `references/`, `workflows/`, `scripts/`, `STEWARDSHIP.md`, sibling `.projex/` docs) are disjoint from `evals/`, so no conflict is expected at close; `git diff base..branch` (two-dot) therefore shows sibling changes as inverse noise, use `base...branch`.
- Main checkout `evals/__pycache__/` (mtime 05:09, before this execution started) was not created by this execution; left untouched.

## Data Gathered

- A3 re-checked against the advanced base tip: `Version integrity` appears 1x in `references/report-template.md` and 1x in `SKILL.md`; `## Audit Coverage` 2x in each. The new string assertions stay valid.
- Observation (no action, out of scope): after the sibling plan, workflow headings read `4.1`-`4.6` without `§` and `references/criteria.md` headings read `## 4.3 ...` / `## 4.6 ...`; `§4.6`/`§4.3` citations are still used in `SKILL.md` and rubric text, so the guard assertion wording remains matchable.
- Not run (by decision): live eval run, model grader. A1 (grader accepts the verdict line as quotable evidence for "an APPROVED verdict passes this check") remains unconfirmed until the live run.

## User Interventions

None.
