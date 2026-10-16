# Eval Runner Harness

> **Status:** In Progress
> **Author:** Claude (Opus), plan-projex subagent
> **Parent:** Orchestrator
> **Source:** Direct request (orchestrated: "What can we do to improve this?" → "orchestrate it")
> **Related Projex:** 2604070218-install-auditor-subject-typed-redesign-nav.md (§ Priorities "Deferred: Eval runner tooling"), 2604150048-ci-action-workflow-m33-walkthrough.md (recommendation: add eval runner), 2604172000-stewardship-cadence-m63-plan.md (STEWARDSHIP.md checklist step 4), 2604171500-per-workflow-eval-bundles-m61-plan.md + 2604171700-hybrid-subject-eval-cases-m62-plan.md (id → workflow mapping source), 2610161849-python-script-ports-plan.md (sibling; adds `scripts/*.py` ports — covered by snapshot + `python3 <snapshot>/scripts/` allow rule; no `evals/` overlap), 2610161852-dispatcher-rubric-consistency-plan.md (sibling; `SKILL.md` red-flag/classifier — no file overlap)
> **Worktree:** Yes

---

## Summary

Make `evals/evals.json` (41 cases, 248 assertions) runnable and gradeable: annotate the file with machine-readable assertion params + per-eval `workflow` tag, and add a stdlib-only Python harness `evals/run_evals.py` (`validate | prepare | run | grade | summary`) plus unit tests. Deterministic grading (82 assertions) and validation run with zero credentials; executing audits and grading the 166 `contains_concept` assertions need a model — either `claude -p` (if authenticated) or an orchestrating agent working from files the harness emits.

**Scope:** `evals/evals.json` (additive fields) | new `evals/run_evals.py` | new `evals/test_run_evals.py` | `STEWARDSHIP.md` checklist step 4 + usage section.
**Estimated Changes:** 4 files; 1 new script (~450 lines, 5 subcommands), 1 new test module (~10 tests), 2 edits.

### Credential matrix (front-loaded)

| Capability | Needs model/credentials? |
|---|---|
| `validate` — schema/invariant check of `evals.json` | No |
| `prepare` — skill snapshot + per-eval task prompts + workspace layout | No |
| `grade` deterministic: `exact_match`, `verdict_check`, `contains_string`, `file_exists`, `line_count_max` (82 assertions) over saved outputs | No |
| `summary` — per-eval/per-workflow tables, exit code | No |
| `run --dry-run` — print exact `claude` commands | No |
| Unit tests (fixtures, no network) | No |
| `run` — perform the audits | **Yes** — `claude -p` auth, or agent-driven (orchestrating agent executes `task_prompt.md` files) |
| `grade --model-grader claude-cli` / agent-written `model_grading.json` for `contains_concept` (166 assertions) | **Yes** |

---

## Objective

### Problem / Gap / Need

- No eval runner exists. Every eval gate since M1.3 used "manual dry-run walkthrough" (nav § Priorities: "Eval runner tooling remains a cross-phase gap (no local harness; manual dry-run only)"; m33 walkthrough: "Add or document an eval runner before expanding Phase 6 eval stewardship").
- `STEWARDSHIP.md` checklist step 4 "Run existing eval cases for this workflow; confirm no regressions" has no mechanism; evals carry no workflow tag, so "this workflow's cases" is only recoverable from closed plans.
- Assertions are `{text, type}` only — even deterministic types have no machine-readable expected value (`exact_match` "Verdict is APPROVED", `verdict_check` "Verdict is REJECTED or CONDITIONAL with strong warnings"). Grading needs parsing prose.

Assertion inventory (verified 2026-10-16): `contains_concept` 166 | `contains_string` 33 | `exact_match` 21 | `verdict_check` 18 | `file_exists` 9 | `line_count_max` 1 → 248. Every eval has ≥1 non-concept assertion. Ids 0–40 unique (array order has id 9 after id 11 — harmless).

### Success Criteria

- [ ] Every eval in `evals/evals.json` has `"workflow"` ∈ the 10 `workflows/*.md` stems; every non-`contains_concept` assertion has its type's required param; existing `id/prompt/expected_output/files/assertions[].text/type` values byte-identical
- [ ] `python3 evals/run_evals.py validate` exits 0 on the repo file, prints `41 evals, 248 assertions (82 deterministic, 166 model-graded)` and per-workflow counts (each ≥3)
- [ ] `prepare` builds an iteration dir outside the repo with skill snapshot (no `evals/`, no `CLAUDE.md`, no `.projex/closed/`), `task_prompt.md` + `eval_metadata.json` per eval; `--ids` / `--workflow` filters work
- [ ] `run --dry-run` prints one `claude -p` command per selected eval using `--permission-mode dontAsk` and the restricted allowlist; never `bypassPermissions`
- [ ] `run` (without `--dry-run`) on a host where `claude -p` cannot authenticate aborts after the first eval with exit 2 and a message naming authentication; with auth, produces `response.md`, `assistant_text.md`, `transcript.jsonl`, `timing.json`, `run_meta.json` per run
- [ ] `grade` writes skill-creator-compatible `grading.json` (`expectations[].text/passed/evidence`, `summary.pass_rate`) per run; `contains_concept` items listed under `pending` with `model_grader_prompt.md` emitted; a present `model_grading.json` is merged
- [ ] `summary` writes `summary.md` + `summary.json`, exits 1 iff any graded assertion failed or a selected eval has no run
- [ ] `python3 -m unittest discover -s evals -p "test_*.py" -v` passes offline (no network, no `claude`)
- [ ] `STEWARDSHIP.md` step 4 names the exact commands; credential split documented

### Out of Scope

- `SKILL.md`, `workflows/`, `references/` content (sibling plan: red-flag/classifier consistency) — no verdict expectation changes
- `scripts/*.ps1` portability / Python ports (sibling `2610161849-python-script-ports-plan.md`); runs on hosts without `pwsh` degrade to "Not available" coverage rows — accepted
- Adding/removing eval cases or rewording assertion `text`; new assertion types (e.g. routing as a graded assertion — emitted as diagnostic only)
- Baseline (without-skill / old-skill) comparison runs, multi-run variance, HTML viewer — `grading.json` layout stays compatible with skill-creator's `aggregate_benchmark.py` / `eval-viewer` for optional external use; not vendored
- Executing a full live 41-eval run as part of this plan (cost + auth unknown); nav doc revision log update (close-projex / orchestrator)
- CI integration

---

## Context

### Current State

- `evals/evals.json`: `{"skill_name": "install-auditor", "evals": [ {id, prompt, expected_output, files: [], assertions: [{text, type}]} ]}`. Custom formatting: 2-space indent, each assertion a one-line object at 8-space indent (all 248 lines match `^\s*\{"text": "…", "type": "[a-z_]+"\},?$`), raw UTF-8 (`—`), no `\u` escapes. `json.dumps` round-trip does NOT reproduce it → edits must be text-level.
- Report contract (`SKILL.md` § Step N Report Skeleton): file `audit-<package-name>.md`; verdict line `**Verdict: [APPROVED ✅ | CONDITIONAL ⚠️ | REJECTED ❌]**`; section `## Audit Coverage`. Classifier output block (`SKILL.md` § Step 0, "emit verbatim before routing") includes `Routes to:      workflows/<type>.md`.
- `SKILL.md` references `.projex/2604070300-install-auditor-subject-type-taxonomy-def.md` for the full classifier rule → snapshot must carry it. `.projex/closed/` plans list expected verdicts per eval id → snapshot must NOT carry them (eval leakage).
- Repo root `CLAUDE.md` (tracked) holds context-mode harness rules; `claude -p` auto-discovers ancestor `CLAUDE.md` → runs inside the repo would be contaminated. Workspace must live outside the repo.
- skill-creator (installed at `<skills>/skill-creator/`, external): task-eval workflow is agent-driven (subagents), `scripts/run_eval.py` is description-trigger eval only (not reusable here). Reusable conventions: layout `eval-N/<config>/run-N/grading.json`, `grading.json.expectations[].{text,passed,evidence}`, `timing.json`.
- Environment (this host): Linux, python3.13, node22, `claude` 2.1.301; no `ANTHROPIC_API_KEY`, no `~/.claude/.credentials.json`, no `CLAUDE_CODE_OAUTH_TOKEN` → `claude -p` auth likely unavailable (unverified). No `pwsh`. `claude --help` confirms `-p`, `--output-format stream-json|json`, `--verbose`, `--permission-mode dontAsk`, `--allowedTools`, `--add-dir`, `--model`, `--max-budget-usd`, `--no-session-persistence`; no `--max-turns`.

### Id → workflow mapping (from m61 coverage table + m62 hybrid table)

| workflow | ids |
|---|---|
| registry-package | 0, 2, 3, 4, 5, 6, 7, 8, 9, 36, 40 |
| browser-extension | 1, 10, 11 |
| container-image | 12, 13, 26, 38 |
| ci-action | 14, 15, 27, 39 |
| ide-plugin | 16, 17, 28, 37 |
| desktop-app | 18, 19, 29 |
| cli-binary | 20, 21, 30 |
| agent-extension | 22, 23, 31 |
| remote-integration | 24, 25, 32 |
| generic | 33, 34, 35 |

Hybrids tagged with the innermost-boundary winner: 36 (npm CLI) → registry-package, 37 (VS Code + binary) → ide-plugin, 38 (Docker wrapping npm) → container-image, 39 (Action pulling Docker) → ci-action, 40 (skill via npm) → registry-package. Total 41.

### Key Files

| File | Role | Change Summary |
|---|---|---|
| `evals/evals.json` | Eval registry | +`workflow` per eval; +params on 82 deterministic assertions (text-level, additive) |
| `evals/run_evals.py` | New harness | `validate`, `prepare`, `run`, `grade`, `summary` |
| `evals/test_run_evals.py` | New unit tests | Offline fixtures for validator, grader, prepare, dry-run |
| `STEWARDSHIP.md` | Review checklist | Step 4 → exact commands; new "Running Evals" section |

### Dependencies

- **Requires:** none (python3 ≥3.9 stdlib, git)
- **Blocks:** later stewardship review pass (consumes `validate`/`grade`/`summary`); full-fidelity live runs benefit from sibling `2610161849-python-script-ports-plan.md` but do not depend on it

### Constraints

- Stdlib only; Python ≥3.9 (no `match`; `from __future__ import annotations`); must work on Windows paths (original author host) — use `pathlib`, no shell=True
- Never write into the skill repo during `prepare/run/grade/summary` (workspace outside repo enforced)
- No projex references in shipped source comments (Source Hygiene); rationale goes in docstrings/STEWARDSHIP.md
- evals.json formatting preserved (text-level edits)

### Assumptions

- `claude -p --output-format stream-json --verbose` emits JSONL with `{"type":"assistant","message":{"content":[{"type":"text"|"tool_use",…}]}}` events and a final `{"type":"result","result":<str>,"total_cost_usd":…,"usage":{…},"duration_ms":…}` — verify in Step 3 by reading one line shape if auth exists; parser must tolerate missing fields
- Claude Code `Bash(<prefix>:*)` allow rules do not authorize chained subcommands (`a && b`) beyond the prefix — reliance is defense-in-depth; `dontAsk` denies everything else
- Report files land in the executor cwd (`outputs/`); a run that writes elsewhere fails `file_exists` — correct per contract
- Global `install-auditor` skill may also be installed on the host; the task prompt pins the snapshot path and `run_meta.snapshot_skill_md_read` flags runs that never read the snapshot's `SKILL.md`

### Impact Analysis

- **Direct:** 4 files above
- **Adjacent:** any tool reading `evals.json` — new keys are additive; skill-creator's `expectations` schema unaffected (this repo uses `assertions`)
- **Downstream:** STEWARDSHIP review passes; future eval-adding plans must supply `workflow` + params (enforced by `validate`)

---

## Implementation

### Overview

1 annotate data → 2 harness core (`validate`, `prepare`) → 3 executor (`run`) → 4 grading (`grade`, `summary`) → 5 tests → 6 docs. Steps 2–4 build one file; each step leaves it runnable.

### Step 1: Annotate evals.json

**Objective:** add `workflow` per eval + required params per deterministic assertion, text-level, formatting preserved.
**Confidence:** High
**Depends on:** None
**Do-Projex:** Encouraged

**Files:** `evals/evals.json`

**Param schema** (`max` inclusive):

| type | required param | example |
|---|---|---|
| `exact_match` | `"expected": "<VERDICT>"` | `"expected": "APPROVED"` |
| `verdict_check` | `"expected": [<VERDICT>, …]` (canonical order APPROVED, CONDITIONAL, REJECTED) | `"expected": ["CONDITIONAL", "REJECTED"]` |
| `contains_string` | `"value": "<literal>"` | `"value": "## Audit Coverage"` |
| `file_exists` | `"glob": "<glob rel. to outputs/>"` | `"glob": "audit-*.md"` |
| `line_count_max` | `"max": <int>` | `"max": 79` ("under 80 lines") |
| `contains_concept` | — | — |

**Changes:** run this one-shot migration from repo root (not committed):

```python
import json, re, pathlib
p = pathlib.Path("evals/evals.json")
s = p.read_text(encoding="utf-8")
WF = {}
for wf, ids in {
    "registry-package": [0, 2, 3, 4, 5, 6, 7, 8, 9, 36, 40],
    "browser-extension": [1, 10, 11],
    "container-image": [12, 13, 26, 38],
    "ci-action": [14, 15, 27, 39],
    "ide-plugin": [16, 17, 28, 37],
    "desktop-app": [18, 19, 29],
    "cli-binary": [20, 21, 30],
    "agent-extension": [22, 23, 31],
    "remote-integration": [24, 25, 32],
    "generic": [33, 34, 35],
}.items():
    for i in ids:
        WF[i] = wf
AC, CR = '["APPROVED", "CONDITIONAL"]', '["CONDITIONAL", "REJECTED"]'
P = {
    ("contains_string", "## Audit Coverage"): '"value": "## Audit Coverage"',
    ("contains_string", "Report mentions @react-native-async-storage/async-storage"):
        '"value": "@react-native-async-storage/async-storage"',
    ("exact_match", "Verdict is APPROVED"): '"expected": "APPROVED"',
    ("exact_match", "Verdict is REJECTED"): '"expected": "REJECTED"',
    ("file_exists", "Report is saved to a .md file"): '"glob": "audit-*.md"',
    ("line_count_max", "Report is concise — under 80 lines"): '"max": 79',
    ("verdict_check", "Verdict is APPROVED or CONDITIONAL"): f'"expected": {AC}',
    ("verdict_check", "Verdict is APPROVED or CONDITIONAL (not REJECTED)"): f'"expected": {AC}',
    ("verdict_check", "Verdict is CONDITIONAL or APPROVED"): f'"expected": {AC}',
    ("verdict_check", "Verdict is CONDITIONAL or APPROVED (not REJECTED)"): f'"expected": {AC}',
    ("verdict_check", "Verdict is CONDITIONAL"): '"expected": ["CONDITIONAL"]',
    ("verdict_check", "Verdict is CONDITIONAL or REJECTED"): f'"expected": {CR}',
    ("verdict_check", "Verdict is REJECTED or CONDITIONAL"): f'"expected": {CR}',
    ("verdict_check", "Verdict is REJECTED or CONDITIONAL with strong warnings"): f'"expected": {CR}',
}
A = re.compile(r'^(\s*\{"text": ")((?:[^"\\]|\\.)*)(", "type": ")([a-z_]+)"\}(,?)$')
I = re.compile(r'^(\s*)"id": (\d+),$')
out, n_par, n_wf = [], 0, 0
for line in s.split("\n"):
    m = I.match(line)
    if m:
        out += [line, f'{m.group(1)}"workflow": "{WF[int(m.group(2))]}",']; n_wf += 1; continue
    m = A.match(line)
    if m and m.group(4) != "contains_concept":
        key = (m.group(4), json.loads('"' + m.group(2) + '"'))
        line = f'{m.group(1)}{m.group(2)}{m.group(3)}{m.group(4)}", {P[key]}}}{m.group(5)}'; n_par += 1
    out.append(line)
assert (n_wf, n_par) == (41, 82), (n_wf, n_par)
new = "\n".join(out)
json.loads(new)
p.write_text(new, encoding="utf-8")
```

```json
// Before:
      "id": 0,
      "prompt": "I want to install express …",
        {"text": "Verdict is APPROVED", "type": "exact_match"},
// After:
      "id": 0,
      "workflow": "registry-package",
      "prompt": "I want to install express …",
        {"text": "Verdict is APPROVED", "type": "exact_match", "expected": "APPROVED"},
```

**Rationale:** explicit params over grader-side prose parsing — one-time reviewable diff, validator can enforce them for future evals. Text-level edit keeps `git diff` to the touched lines. "with strong warnings" (ids 2, 9) keeps verdict-set check only; the warning-strength nuance stays prose (accepted loss, see Risks). `line_count_max` 79: "under 80" = strictly less than 80.

**Verification:** `git diff --stat evals/evals.json` → `123 insertions(+), 82 deletions(-)` (41 `workflow` lines + 82 rewritten assertion lines; snippet pre-tested on a scratch copy 2026-10-16 with exactly this result); `git diff evals/evals.json | grep '^-' | grep -v '^---' | grep -c '"type": "contains_concept"'` → 0; python check that for each eval, stripping `workflow` and the new params reproduces the pre-change object (`git show HEAD:evals/evals.json`).

**If this fails:** `git checkout -- evals/evals.json`; fix mapping (KeyError names the unmapped text) and rerun.

---

### Step 2: Harness core — loader, `validate`, `prepare`

**Objective:** create `evals/run_evals.py` with argparse subcommands; implement shared loading, validation, workspace + snapshot preparation.
**Confidence:** High
**Depends on:** Step 1
**Verify-Projex:** Encouraged

**Files:** `evals/run_evals.py` (new)

**Changes:** module docstring = usage + credential matrix (same table as Summary, prose). Core contracts:

```python
#!/usr/bin/env python3
from __future__ import annotations
import argparse, fnmatch, json, re, shutil, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
EVALS_PATH = SKILL_ROOT / "evals" / "evals.json"
VERDICTS = ("APPROVED", "CONDITIONAL", "REJECTED")
DETERMINISTIC = {"exact_match", "verdict_check", "contains_string", "file_exists", "line_count_max"}
MODEL_GRADED = {"contains_concept"}
SNAPSHOT_DIRS = ("workflows/", "references/", "scripts/")
MIN_CASES_PER_WORKFLOW = 3

def known_workflows(root: Path = SKILL_ROOT) -> set[str]:
    return {p.stem for p in (root / "workflows").glob("*.md")}

def validate(data: dict, workflows: set[str], root: Path = SKILL_ROOT) -> list[str]:
    """Return error strings; empty list = valid."""
    # checks: skill_name == SKILL.md frontmatter `name:`; evals is non-empty list;
    # id int + unique; prompt/expected_output non-empty str; files list of existing
    # paths under root; workflow in workflows; assertions non-empty list;
    # each assertion: text str, type in DETERMINISTIC|MODEL_GRADED, plus params:
    #   exact_match -> expected in VERDICTS
    #   verdict_check -> expected non-empty list, subset of VERDICTS, no dups
    #   contains_string -> value non-empty str
    #   file_exists -> glob non-empty str
    #   line_count_max -> max int > 0
    #   contains_concept -> no extra keys besides text/type
    # every workflow in `workflows` has >= MIN_CASES_PER_WORKFLOW evals
```

`validate` subcommand: load `EVALS_PATH` (or `--evals PATH`), print errors one per line + exit 1; else print `N evals, M assertions (D deterministic, C model-graded)` + `workflow: count` lines, exit 0.

`prepare [--workspace DIR] [--ids 0,5] [--workflow a,b]`:
1. Validate first; abort on errors.
2. Workspace default `SKILL_ROOT.parent / f"{SKILL_ROOT.name}-workspace"`. Resolve; if `SKILL_ROOT` is the workspace or one of its ancestors → exit 2 `"workspace must be outside the skill repo (ancestor CLAUDE.md would leak into runs)"`.
3. Iteration dir `iteration-<N>`, N = 1 + max existing.
4. Snapshot → `<iter>/skill-snapshot/`: files from `git -C SKILL_ROOT ls-files` that are `SKILL.md` or start with a `SNAPSHOT_DIRS` prefix, plus each `.projex/<name>.md` matched by `re.findall(r"\.projex/(\d{10}-[\w.-]+\.md)", SKILL.md text)` that exists at `.projex/<name>` (top level only). Copy with `shutil.copy2`. Working-tree content (uncommitted edits included — that is what a reviewer is testing).
5. `iteration_meta.json`: `{skill_root, git_head, git_dirty (bool from status --porcelain), created_utc, eval_ids, snapshot_files}`.
6. Per eval `eval-<id>/`: `eval_metadata.json` `{eval_id, eval_name: "eval-<id>-<workflow>", workflow, prompt, expected_output, assertions}`; `task_prompt.md` from template below; `with_skill/run-1/outputs/` created; each `files` entry copied into `outputs/`.
7. Print iteration path + next steps (`run`, or agent-driven instructions).

`task_prompt.md` template:

```text
You are performing an install audit using the install-auditor skill.

Skill path: {snapshot}
Read {snapshot}/SKILL.md first and follow it exactly. Relative paths in the skill (workflows/, references/, scripts/, .projex/) resolve against the skill path. Use only this copy of the skill, not any other installed install-auditor.

Working directory: {outputs}
Write every file you produce, including the audit report, into the working directory.

Safety: this is an audit. Never install, download-and-execute, pull, or run the subject under audit.

User request:
{prompt}
```

**Rationale:** snapshot isolates runs from repo mutations and from `.projex/closed/` answer leakage, and pins the skill version per iteration. Sibling-of-repo workspace mirrors skill-creator convention and avoids `CLAUDE.md` ancestor discovery. Rejected PowerShell (no `pwsh` on this host; portability is a sibling's open work) and Node (no `package.json`; Python already the sibling's port target).

**Verification:** `python3 evals/run_evals.py validate` → exit 0 + counts; `prepare --workspace <tmp> --ids 0,13` → `iteration-1/` with `eval-0/`, `eval-13/`, snapshot containing `SKILL.md`, 10 workflows, `references/criteria/*.md`, `scripts/*.ps1`, `.projex/2604070300-install-auditor-subject-type-taxonomy-def.md`, and no `evals/`, `CLAUDE.md`, `STEWARDSHIP.md`, `.projex/closed/`; `prepare --workspace <repo>/x` → exit 2.

**If this fails:** delete `evals/run_evals.py`; Step 1 stands alone.

---

### Step 3: Executor — `run`

**Objective:** execute prepared evals through `claude -p`, capture artifacts; dry-run prints commands only.
**Confidence:** Medium (stream-json shape + auth unverified on this host)
**Depends on:** Step 2
**Verify-Projex:** Encouraged

**Files:** `evals/run_evals.py`

**Changes:** `run [--workspace] [--iteration NAME(default latest)] [--model M] [--max-budget-usd B] [--timeout 900] [--allow-tool RULE ...] [--dry-run] [--keep-going] [--force]`.

```python
def default_allowed_tools(snapshot: Path) -> list[str]:
    s = snapshot.as_posix()
    return [
        "Read", "Write", "Edit", "Glob", "Grep", "WebFetch", "WebSearch",
        f"Bash(pwsh -File {s}/scripts/:*)", f"Bash(powershell -File {s}/scripts/:*)",
        f"Bash(python3 {s}/scripts/:*)",
        "Bash(npm view:*)", "Bash(cosign verify:*)", "Bash(crane manifest:*)", "Bash(skopeo inspect:*)",
    ]

def build_exec_cmd(task_prompt: str, snapshot: Path, model: str | None,
                   budget: float | None, extra: list[str]) -> list[str]:
    cmd = ["claude", "-p", task_prompt, "--output-format", "stream-json", "--verbose",
           "--permission-mode", "dontAsk", "--no-session-persistence",
           "--add-dir", str(snapshot),
           "--allowedTools", *default_allowed_tools(snapshot), *extra]
    if model: cmd += ["--model", model]
    if budget is not None: cmd += ["--max-budget-usd", str(budget)]
    return cmd
```

Per selected eval (sorted by id), run dir `eval-<id>/with_skill/run-1/`:
- Skip if `response.md` exists unless `--force`.
- `--dry-run`: print `shlex.join(cmd)` with the prompt replaced by `<task_prompt.md>`; no subprocess; exit 0.
- Else `subprocess.run(cmd, cwd=outputs, capture_output=True, text=True, encoding="utf-8", timeout=timeout)`; preflight `shutil.which("claude")` → exit 2 if missing.
- Write `transcript.jsonl` (stdout verbatim). Parse lines tolerantly (`json.loads` per line, skip bad): concat assistant `text` blocks → `assistant_text.md`; `result` event `.result` → `response.md`; `snapshot_skill_md_read` = any `tool_use` named `Read` whose `input.file_path` resolves to `<snapshot>/SKILL.md`.
- `timing.json`: `{total_duration_seconds, total_tokens}` (wall clock; tokens = sum of `usage` input+output if present, else null).
- `run_meta.json`: `{executor: "claude-cli", argv_without_prompt, exit_code, timed_out, duration_seconds, total_cost_usd, snapshot_skill_md_read, stderr_tail (last 2000 chars)}`.
- No `result` event → do not write `response.md`. If this is the first executed eval and not `--keep-going`: stop, exit 2, print `claude -p failed on eval <id> (exit <code>). Likely not authenticated: set ANTHROPIC_API_KEY or run 'claude' login. stderr tail: …`.

Agent-driven alternative (no code; documented in Step 6 + `prepare` output): orchestrating agent runs each `task_prompt.md` in a fresh subagent with cwd `outputs/`, saves final message to `response.md` (optionally `run_meta.json` `{executor: "agent"}`). `grade` treats both identically.

> **Security:** eval prompts deliberately contain hostile install commands (`curl … | sh`, `iex ((New-Object …`, `docker pull …/cryptominer`). The executor must never use `bypassPermissions` or a bare `Bash` / `Bash(pwsh:*)` allow rule. `dontAsk` + the prefix allowlist above is the containment; `--allow-tool` additions are operator responsibility.

**Rationale:** `dontAsk` auto-denies unlisted tools (no hang in headless mode). Abort-on-first-failure avoids 41 doomed calls on unauthenticated hosts. Resumable via skip-if-done.

**Verification:** `run --workspace <tmp> --dry-run` prints 2 commands (from Step 2's prepare) containing `--permission-mode dontAsk` and no `bypassPermissions`. On this host (no auth): `run --workspace <tmp>` → exit 2 with the auth message, `run_meta.json` present, no `response.md`. If auth works: one eval produces all 5 artifacts; check one `result` line shape and adjust parser keys if they differ (record in execution log).

**If this fails:** revert `run` subcommand code only; Steps 2/4 unaffected (agent-driven path still works).

---

### Step 4: Grading — `grade`, `summary`

**Objective:** deterministic grading, model-grading hand-off/merge, iteration summary.
**Confidence:** High
**Depends on:** Step 2 (Step 3 not required — grades any run dir with `response.md`)
**Verify-Projex:** Encouraged

**Files:** `evals/run_evals.py`

**Changes:**

```python
VERDICT_RE = re.compile(r"^[ \t>*_]*Verdict[ \t]*[:*]+[ \t*]*(APPROVED|CONDITIONAL|REJECTED)\b", re.M)
ROUTE_RE = re.compile(r"^\s*Routes to:\s*`?workflows/([a-z-]+)\.md", re.M)

def collect(run_dir: Path) -> dict:
    out = run_dir / "outputs"
    reports = sorted(out.rglob("audit-*.md")) if out.is_dir() else []
    read = lambda p: p.read_text(encoding="utf-8", errors="replace") if p.is_file() else ""
    report_texts = [read(p) for p in reports]
    response = read(run_dir / "response.md")
    assistant = read(run_dir / "assistant_text.md")
    verdicts = [v for t in report_texts for v in VERDICT_RE.findall(t)] or VERDICT_RE.findall(response)
    route = ROUTE_RE.search(assistant + "\n" + response)
    return {"outputs": out, "reports": reports, "report_texts": report_texts,
            "haystack": "\n".join(report_texts + [response, assistant]),
            "verdicts": verdicts, "routed_to": route.group(1) if route else None}

def grade_deterministic(a: dict, c: dict) -> tuple[bool, str]:
    t, v = a["type"], c["verdicts"]
    if t == "exact_match":
        return (bool(v) and set(v) == {a["expected"]}, f"verdicts found: {v or 'none'}")
    if t == "verdict_check":
        return (bool(v) and set(v) <= set(a["expected"]), f"verdicts found: {v or 'none'}; allowed {a['expected']}")
    if t == "contains_string":
        ok = a["value"] in c["haystack"]
        return ok, f"{'found' if ok else 'not found'}: {a['value']!r}"
    if t == "file_exists":
        hits = sorted(p.relative_to(c["outputs"]).as_posix() for p in c["outputs"].rglob(a["glob"])) if c["outputs"].is_dir() else []
        return bool(hits), f"matches for {a['glob']!r}: {hits or 'none'}"
    if t == "line_count_max":
        if not c["reports"]:
            return False, "no audit-*.md report"
        counts = {p.name: len(txt.splitlines()) for p, txt in zip(c["reports"], c["report_texts"])}
        return all(n <= a["max"] for n in counts.values()), f"line counts {counts}; max {a['max']}"
    raise ValueError(t)
```

Semantics: verdicts come from report files first, `response.md` only if no report verdict; all found verdicts must satisfy the assertion (multi-report runs can't hide a bad verdict). Skeleton placeholder `**Verdict: [APPROVED ✅ | …` does not match (`[` precedes the word).

`grade [--workspace] [--iteration] [--model-grader none|claude-cli] [--model M]` per run dir with `response.md` (others → reported "not run", skipped):
1. Deterministic assertions → `{"index","text","type","grader":"deterministic","passed","evidence"}`.
2. `contains_concept`: if `model_grading.json` exists, merge entries matching both `index` and `text` (`grader` from file); mismatched text → stays pending + stderr warning "assertion text changed since model grading".
3. Remaining concepts → `pending: [{"index","text","type"}]`; write `model_grader_prompt.md` = instructions + `expected_output` + numbered pending assertions + report texts (each fenced, with filename) + `response.md`; instructions: judge each assertion only from the provided outputs, PASS needs a quoted evidence span, reply with only `{"expectations":[{"index":int,"text":str,"passed":bool,"evidence":str}]}`.
4. `--model-grader claude-cli` and pending non-empty: `claude -p <prompt> --output-format json --permission-mode dontAsk --no-session-persistence [--model]`, cwd = run dir; parse stdout JSON `.result`, slice `[find("{"), rfind("}")+1]`, validate shape/indices, write `model_grading.json` `{"grader":"claude-cli","expectations":[…]}`, then redo step 2. Failure → leave pending, stderr message, continue.
5. Write `grading.json`:

```json
{
  "eval_id": 0, "workflow": "registry-package",
  "expectations": [{"index": 1, "text": "Verdict is APPROVED", "type": "exact_match", "grader": "deterministic", "passed": true, "evidence": "verdicts found: ['APPROVED']"}],
  "pending": [{"index": 0, "text": "Report identifies this as a Tier 1 / Quick audit", "type": "contains_concept"}],
  "diagnostics": {"verdicts": ["APPROVED"], "report_files": ["audit-express.md"], "routed_to": "registry-package", "routing_match": true, "snapshot_skill_md_read": true},
  "summary": {"passed": 3, "failed": 0, "total": 3, "pending": 1, "pass_rate": 1.0}
}
```

`total` counts graded only (≥1 always: every eval has a deterministic assertion). `routing_match` = `routed_to == workflow` (null if not found); `snapshot_skill_md_read` copied from `run_meta.json` if present else null. Diagnostics never affect pass/fail.

`summary [--workspace] [--iteration]`: read every selected eval's `grading.json` → `summary.md` (table: id | workflow | verdicts | deterministic pass/total | model pass/total | pending | routing; then per-workflow totals; then failing assertions with evidence) + `summary.json`; print the md. Exit 1 if any graded `passed: false` or any selected eval lacks `grading.json`; else 0.

**Rationale:** union haystack for `contains_string` (report or chat answer both count, e.g. id 2's alternative-package mention); verdict strictness prevents prose like "not APPROVED" from matching (line-anchored regex). File hand-off keeps model grading possible without `claude -p` auth.

**Verification:** covered by Step 5 fixtures; manual: hand-made run dir for eval 0 (report with `**Verdict: APPROVED ✅**`, `## Audit Coverage`, 40 lines) → `grade` → 3/3 deterministic pass, 1 pending, `model_grader_prompt.md` present; `summary` exit 0.

**If this fails:** revert grade/summary functions; Steps 1–3 stand.

---

### Step 5: Unit tests

**Objective:** prove validator, grader, prepare, dry-run offline.
**Confidence:** High
**Depends on:** Steps 2–4
**Do-Projex:** Encouraged

**Files:** `evals/test_run_evals.py` (new) — `unittest`, imports `run_evals` via `sys.path.insert(0, str(Path(__file__).parent))`; all fixtures in `tempfile.TemporaryDirectory()`.

**Changes — test cases:**
1. `test_repo_evals_valid` — `validate(load(EVALS_PATH), known_workflows())` == [] and counts 41/248/82/166.
2. `test_validate_rejects` — synthetic data: missing `expected` on `exact_match`; `verdict_check` with `"MAYBE"`; unknown type; unknown workflow; duplicate id; workflow under 3 cases → each yields ≥1 error naming the eval id.
3. `test_grade_pass` — eval-0-like assertions + report `audit-express.md` (verdict APPROVED, `## Audit Coverage`, 40 lines) → deterministic all pass, concept pending.
4. `test_grade_verdict_mismatch_and_missing` — REJECTED report vs `exact_match APPROVED` → fail; no report & no verdict in response → fail with "none".
5. `test_multi_report_verdict_check` — two reports APPROVED + REJECTED vs allowed [APPROVED, CONDITIONAL] → fail.
6. `test_placeholder_not_a_verdict` — skeleton line `**Verdict: [APPROVED ✅ | CONDITIONAL ⚠️ | REJECTED ❌]**` → verdicts == [].
7. `test_line_count_max` — 80-line report vs max 79 → fail; 79 → pass.
8. `test_model_grading_merge` — `model_grading.json` with matching index+text → concept graded; altered text → stays pending.
9. `test_routing_diagnostic` — response containing `Routes to:      workflows/registry-package.md` → `routed_to` == registry-package.
10. `test_prepare_snapshot` — `prepare` into temp workspace with `--ids 0` → snapshot has `SKILL.md` + taxonomy def, lacks `evals/`, `CLAUDE.md`, `.projex/closed`; `task_prompt.md` contains snapshot absolute path and eval 0 prompt; workspace inside repo → exit 2.
11. `test_dry_run_cmd` — `build_exec_cmd` contains `dontAsk`, no `bypassPermissions`, no bare `"Bash"` entry, no `Bash(pwsh:*)`.

**Verification:** `python3 -m unittest discover -s evals -p "test_*.py" -v` → 11 OK, runtime < 10 s, no network.

**If this fails:** fix code (tests encode the Step 2–4 contracts); do not loosen assertions to pass.

---

### Step 6: Document in STEWARDSHIP.md

**Objective:** wire checklist step 4 to the harness; document credential split.
**Confidence:** High
**Depends on:** Steps 2–4
**Do-Projex:** Encouraged

**Files:** `STEWARDSHIP.md`

**Changes:**

```markdown
// Before:
4. Run existing eval cases for this workflow; confirm no regressions

// After:
4. Run existing eval cases for this workflow; confirm no regressions (see Running Evals below: `prepare --workflow <name>` → run → `grade` → `summary`; any failed assertion or routing mismatch is a regression signal)
```

Append section before `## Record-Keeping`:

```markdown
## Running Evals

`evals/run_evals.py` (Python 3.9+, stdlib only). Workspace defaults to `<repo>-workspace/` beside the repo and must stay outside it.

| Command | Purpose | Needs a model |
|---|---|---|
| `python3 evals/run_evals.py validate` | Schema + invariants of `evals/evals.json` (params, `workflow` tags, ≥3 cases/workflow) | No |
| `python3 evals/run_evals.py prepare --workflow <name>` (or `--ids 0,5`) | Snapshot skill, write per-eval `task_prompt.md` | No |
| `python3 evals/run_evals.py run [--dry-run] [--model M] [--max-budget-usd B]` | Execute via `claude -p` (`dontAsk`, restricted tool allowlist) | Yes (`claude` auth) |
| `python3 evals/run_evals.py grade [--model-grader claude-cli]` | Deterministic grading; `contains_concept` → pending + `model_grader_prompt.md` | Only for `--model-grader` |
| `python3 evals/run_evals.py summary` | Per-eval / per-workflow table; exit 1 on any failure | No |

Without `claude -p` credentials, an agent session can execute instead: run each `eval-<id>/task_prompt.md` in a fresh subagent with cwd `eval-<id>/with_skill/run-1/outputs/`, save its final message to `../response.md`, and for model grading answer `model_grader_prompt.md` into `model_grading.json`; then rerun `grade` and `summary`.

New eval cases must carry `workflow` and the type's param (`exact_match`/`verdict_check` → `expected`, `contains_string` → `value`, `file_exists` → `glob`, `line_count_max` → `max`); `validate` enforces this. Self-test: `python3 -m unittest discover -s evals -p "test_*.py"`.
```

**Rationale:** STEWARDSHIP.md is the shipped doc for review passes (promotion target for runner rationale); no new README.

**Verification:** `grep -n "run_evals.py" STEWARDSHIP.md` ≥ 5 hits; step numbering 1–8 intact.

**If this fails:** `git checkout -- STEWARDSHIP.md`.

---

## Verification Plan

### Automated Checks
- [ ] `python3 evals/run_evals.py validate` → exit 0, `41 evals, 248 assertions (82 deterministic, 166 model-graded)`
- [ ] `python3 -m unittest discover -s evals -p "test_*.py" -v` → all pass offline
- [ ] `python3 -c "import json;json.load(open('evals/evals.json',encoding='utf-8'))"` → no error
- [ ] `git diff --check` clean

### Manual Verification
- [ ] E2E offline: `prepare --workspace <tmp> --ids 0,13` → hand-write `eval-0/.../outputs/audit-express.md` (APPROVED) + `response.md`; `eval-13` `response.md` only, verdict REJECTED, no report → `grade` → `summary`: eval 0 det 3/3, eval 13 `exact_match` pass, `contains_string ## Audit Coverage` fail → exit 1
- [ ] `run --workspace <tmp> --dry-run` → 2 commands, `dontAsk`
- [ ] `run --workspace <tmp>` on this host → exit 2 auth message (or, if auth works, 1 real eval end-to-end; record cost in execution log)
- [ ] Repo `git status` after all above: only the 4 planned files changed (workspace outside repo)

### Acceptance Criteria Validation

| Criterion | How to Verify | Expected Result |
|---|---|---|
| evals.json annotated, values preserved | Step 1 verification script vs `HEAD` | 41 `workflow`, 82 params, originals identical |
| `validate` | run | exit 0 + counts |
| `prepare` isolation | test 10 + manual tree check | snapshot excludes evals/, CLAUDE.md, .projex/closed |
| `run` safety + auth abort | test 11, dry-run, live attempt | `dontAsk`; exit 2 without auth |
| `grade` compat + pending | tests 3–9 | `grading.json` fields `text/passed/evidence`, pending listed |
| `summary` exit code | manual E2E | exit 1 with a failing assertion |
| Offline tests | unittest | all OK |
| STEWARDSHIP step 4 | grep | commands present |

---

## Rollback Plan

1. `git checkout -- evals/evals.json STEWARDSHIP.md`
2. Delete `evals/run_evals.py`, `evals/test_run_evals.py`
3. Delete any `<repo>-workspace/` dirs created during verification (outside repo; untracked)

---

## Notes

### Risks
- **`claude -p` auth unavailable here** → live `run` + `--model-grader claude-cli` unverifiable in this env. Mitigation: dry-run + abort path verified; agent-driven path documented; stream-json parser tolerant; first authenticated run should confirm event keys (Step 3 verification).
- **Hostile prompts executed by an agent** → see Step 3 Security block; allowlist excludes general shell and bare `pwsh`.
- **Model reads global installed `install-auditor` instead of snapshot** → task prompt pins path; `snapshot_skill_md_read` diagnostic surfaces it in `grading.json`.
- **Verdict regex misses unconventional report formats** → by design the `SKILL.md` contract is the spec; misses show as failures with "verdicts found: none" evidence, which is the regression signal STEWARDSHIP wants.
- **"with strong warnings" (ids 2, 9) partially deterministic** → verdict set graded; warning strength not graded. Accepted; a future eval-update plan may add a `contains_concept` for it.
- **Scripts are `.ps1`, no `pwsh` on Linux** → live runs record "Not available" lookups (coverage Low/Moderate); verdict assertions unaffected by design (coverage never changes verdict per `SKILL.md`). Improves with sibling `2610161849-python-script-ports-plan.md`.
- **Sibling plan edits `evals.json`** (e.g. adds cases) after this lands → `validate` will demand `workflow` + params; execution is serial, so whichever lands second rebases trivially.

### Split Decision
`No split — heuristic tripped (~575 lines, 6 steps) but steps tightly coupled (rationale: Steps 2–4 incrementally build the single file evals/run_evals.py and share loader/layout contracts; Step 1's params are the grader's input schema; Steps 5–6 only test/document 2–4. Splitting would force child plans to re-specify the same contracts.) Single projex scope; ~40 KB < 50 KB.`

### Open Questions
- (none)
