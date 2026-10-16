# Execution Log: ci-action Rubric Refresh

> **Status:** Complete
> **Started:** 20261016 20:20
> **Repo Root:** /home/user/install-auditor-skill
> **Plan File:** .projex/2610162005-ci-action-rubric-refresh-plan.md
> **Parent:** 2610162005-ci-action-rubric-refresh-plan.md
> **Base Branch:** claude/youthful-dijkstra-5ov1kt
> **Worktree Path:** .projexwt/2610162005-ci-action-rubric-refresh

## Pre-Check Results

```
PASS  Plan is committed (619d5d4 projex: add plan - ci-action-rubric-refresh)
WARN  Working tree has 6 uncommitted change(s)
PRE-CHECK PASSED
```

The 6 uncommitted changes are untracked sibling planner plans (`.projex/*-plan.md`) in the main checkout, not part of this execution.

## Steps

### [20261016 20:20] - Preflight: shared-floor contract, baselines, A4
**Action:** Ran the 9 Preflight commands in the worktree. Base start commit `888ff74` (descendant of `20843cc`). Verified A4 against a sparse shallow clone of `github/docs` (`content/actions/reference/security/oidc.md`).
**Result:**
- `20843cc` found via `git log --grep`; `^## 4.6 Version & Update Integrity (shared floor)$` = 1; `^### V[1-5] ` = 5; `Addendum plug-ins` = 1; `Audit tooling is itself a dependency` = 1; SKILL.md Red Flag = 1; `Confirmed supply chain compromise` = 2 (>= 1). All pass.
- `wc -c`: workflows/ci-action.md 7775; references/criteria/ci-action.md 7322; references/registries.md 4413. Match plan baselines (registry sibling not landed).
- `evals/run_evals.py validate`: 41 evals, 248 assertions (82 deterministic, 166 model-graded).
- `unittest discover -s evals -p "test_*.py"`: 12 tests OK. `unittest discover -s tests`: 19 tests OK (skipped=6).
- A4: `oidc.md` § "Methods for requesting the OIDC token" documents `ACTIONS_ID_TOKEN_REQUEST_URL` and `ACTIONS_ID_TOKEN_REQUEST_TOKEN` as runner environment variables, with a shell `curl` example. Supports the 2g sentence "any step in the job, including third-party actions and `run:` scripts". Plan wording kept unchanged.
**Status:** Success

### [20261016 20:32] - Step 1: workflows/ci-action.md
**Action:** Applied replacements 1a-1p with the Edit tool, each anchor matching exactly once (16/16 succeeded, no re-anchoring).
**Result:** `grep -c "except for"` = 1; `allow-unsafe-pr-checkout` = 3; `cache-mode` = 3; `§4.6` = 5; `actions.lock` = 1; `gh release verify` = 1. `wc -c` = 11028 (simulation 11,028, delta 0). `awk 'length>80 && !/^\|/'` lists exactly 4 lines (40, 138, 234, 252: Publisher identity, Q6, `workflow_call` REJECTED bullet, Verified-creator CONDITIONAL bullet), all pre-existing. Verified by self-review of `git diff` (no sub-subagent available in this execution).
**Status:** Success

### [20261016 20:36] - Step 2: references/criteria/ci-action.md
**Action:** Applied replacements 2a-2n (14/14 matched once; 2c and the 2f row block applied as single multi-line edits).
**Result:** `## Version & Update Integrity (§4.6)` heading = 1; `- **V1**`..`- **V5**` bullets = 5; CVE Scope + Runtime & Pin Freshness + Static Analysis Helper headings = 3; `except for §4.6` = 1; `cache-mode` = 4; `actions.lock` = 4; `allow-unsafe-pr-checkout` = 1; `gh release verify` = 2. `wc -c` = 17115 (simulation 17,115, delta 0). Self-verified against `git diff`; plan marks Verify-Projex Encouraged, not Required, and no verifier sub-subagent was available.
**Status:** Success

### [20261016 20:38] - Step 3: references/registries.md CI/CD
**Action:** Applied 3a (unverified row to `Medium-Low`) and 3b (Critical rule aligned to the Red Flag, hard-coded SHA removed). Registry sibling plan had not landed on the base; no fallback needed.
**Result:** `grep -c "11bd71901bbe5b1630ceea73d27597364c9af683\|Any action that accesses"` = 0; `Mutable CI ref with privileged access` = 1; `Medium-Low — pin to SHA` = 1. `wc -c` = 4681 (simulation 4,681, delta 0).
**Status:** Success

### [20261016 20:44] - Full verification, spec compliance, paper traces
**Action:** Ran the plan's consistency script, `evals/run_evals.py validate`, both unittest suites, and `git diff --stat 888ff74..HEAD`; spot-checked tag SHAs with `git ls-remote` on `actions/checkout` and `docker/build-push-action`; walked traces T1-T11 against `SKILL.md`, `references/criteria.md` §4.6 and the three edited files.
**Result:**
- Consistency script: `OK`. validate: 41 evals, 248 assertions (same as Preflight). `unittest -s evals`: 12 OK (same count). `unittest -s tests`: 19 OK (skipped=6, same).
- `git diff --stat 888ff74..HEAD`: the 3 target files plus this log. `SKILL.md` not changed. No projex filenames or ids in shipped files (grep clean).
- Sizes: workflow 11028 | addendum 17115 | registries 4681 (all delta 0 vs simulation).
- `git ls-remote`: `actions/checkout` `v4.2.2` = `11bd719…`; `v4` and `v4.4.0` = `11d5960…`; `v5.1.0`, `v6.1.0`, `v7.0.0` exist; `docker/build-push-action` `v5` = `ca052bb…`. Confirms A2/A3 facts and the 2i backport list.
- A5 (`gh` `-R` form) not exercised offline; wording kept as planned.
- Traces (shared floor = `references/criteria.md` §4.6; addendum = `references/criteria/ci-action.md`; wf = `workflows/ci-action.md`):
  - T1 eval 14: wf Tier 1 bullets (official `actions/*`, full SHA, read-only, no `pull_request_target`), addendum Ref Immutability Matrix row 1 (SHA = tag `v4.2.2`, reachable), shared V1 (2024-10-23, >= 7 d), V2 (repo matches `actions/checkout`), no V3/V4. §Runtime & Pin Freshness: `node20` LOW, superseded LOW; "LOW notes here do not bar Tier 1". APPROVED; wf APPROVED shape (1p) puts update control (Dependabot/Renovate, addendum V5) in the Recommendation. Matches.
  - T2 eval 15: `pull_request_target` + `secrets: inherit` + `contents: write`; child `@main`. `SKILL.md` Red Flag (branch ref, privileged) + wf Tier 3 + wf REJECTED bullets ("`pull_request_target` plus third-party mutable ref"). REJECTED. Matches.
  - T3 eval 27: `docker/build-push-action@v5` (`ca052bb…`, floating major) is not an immutable release (Matrix: "floating major tag is never an immutable release") -> mutable-tag row, HIGH; verified publisher -> CONDITIONAL (pin to SHA). `node20` LOW, superseded LOW. CONDITIONAL. Matches.
  - T4 cache chain: Trigger matrix + scoring bullet "Cache written by a job that processes untrusted input and restored by a release, publish, or `id-token: write` job = CRITICAL"; the `cache-mode: write` writer row = HIGH on its own; wf REJECTED bullet 2. REJECTED.
  - T5 trusted-only cache restore: scoring bullet "restoring caches written only by trusted triggers = MEDIUM"; wf CONDITIONAL bullet (1n). Single MEDIUM -> CONDITIONAL-or-APPROVED reachable per shared tree; Tier 2+ (id-token: write is a wf Tier 3 trigger, so Tier 3 in practice; rating unchanged). Matches plan ("MEDIUM, APPROVED reachable") with the Tier note below.
  - T6 `allow-unsafe-pr-checkout` + `make test`: PR-head row (High) + scoring "CRITICAL when the fetched code is executed"; wf REJECTED bullet 1. REJECTED.
  - T7 immutable release: Matrix row 3 (LOW note, no pin condition for verified publisher); `packages: write` -> Tier 3; shared V2 satisfied by `gh release verify` + repo match. APPROVED reachable. Unverified twin: Matrix row 3 final clause + `SKILL.md` Red Flag "any non-SHA ref from an unverified third-party publisher" -> REJECTED. Matches.
  - T8 impostor SHA: Matrix row 2 ("Treat as an unknown ref") + scoring bullet ("CRITICAL in a privileged job via the `SKILL.md` Red Flag") + addendum V2 ("not verified (unknown ref)"). REJECTED.
  - T9 SHA bumped to a 20 h old release: addendum V1 (release date from GitHub release) -> shared V1 `< 72 h` HIGH `fresh version` -> CONDITIONAL; condition cites Dependabot `cooldown`. Matches.
  - T10 `curl … main/install.sh | bash` in `id-token: write` job: scoring bullet "from a mutable non-vendor source = CRITICAL" -> REJECTED; unversioned `pip install trivy`: "Unpinned tool install … = HIGH (condition: pin + checksum)" -> CONDITIONAL. Matches.
  - T11 resolved tj-actions-style compromise, post-fix SHA: shared V4 case (c) LOW `past compromise`, Tier 1 barred -> wf Tier 2; wf APPROVED bullet (1p) allows "only a resolved past compromise outside the pinned version"; addendum V5 lists triggers/update controls. APPROVED reachable. Matches.
- Spec compliance: shared contract (`references/criteria.md` §4.6 V1-V5 plug-ins, §4.3 own-code line) satisfied: one `## Version & Update Integrity (§4.6)` with V1-V5 and one `## CVE Scope (§4.3)`; both headers carry the §4.6 carve-out; no rating relaxes a Red Flag or the §4.6 floor. All Success Criteria checked.
- Quality review: diff read end to end; no stray whitespace, no dead text, cross-references resolve (consistency script). Observation: in T5 the plan table says "Tier 2+" while wf Tier 3 lists `id-token: write`; the plan's own wf text governs (Tier 3 for `id-token: write` jobs), verdict unaffected. Not changed (out of scope, would alter plan text).
**Status:** Success

## Deviations

- No todo/task tool was available in this subagent environment, so the plan was tracked through the log and per-step commits instead of a task list (execute-projex § 2).
- No verify-projex or do-projex sub-subagents were spawned (no spawn tool available); all steps were self-executed and self-verified (plan marks Verify-Projex Encouraged only).
- Orchestrator-requested trailers (`Co-Authored-By`, `Claude-Session`) were added to every commit, including doc-only ones; the base start-execution commit was amended once (`b97cbb4` -> `888ff74`, unpushed, HEAD at the time) to add them.
- No plan text or anchor changed; all 32 replacements applied verbatim.

## Issues Encountered

- A4 verification needed `github/docs`: `gh api` was refused (session-bound repos), so a sparse shallow clone (`--filter=blob:none --sparse`) at `/home/user/github/docs` served the read; removed at cleanup.

## Data Gathered

- A4: confirmed (see Preflight entry).
- Tag SHAs: see verification entry.

## Cleanup

- Removed the scratch clone `/home/user/github/docs` (outside the repo). Worktree holds no untracked or ignored files.

## User Interventions

None.

