# CI Action Workflow — M3.3

> **Status:** Ready
> **Created:** 2026-04-15
> **Author:** Codex (GPT-5)
> **Source:** [2604070218-install-auditor-subject-typed-redesign-nav.md](2604070218-install-auditor-subject-typed-redesign-nav.md) Phase 3, M3.3
> **Related Projex:**
> - **Roadmap:** [2604070218-install-auditor-subject-typed-redesign-nav.md](2604070218-install-auditor-subject-typed-redesign-nav.md)
> - **Framing eval:** [2604070217-subject-typed-audit-dispatch-eval.md](2604070217-subject-typed-audit-dispatch-eval.md)
> - **Taxonomy spec:** [2604070300-install-auditor-subject-type-taxonomy-def.md](2604070300-install-auditor-subject-type-taxonomy-def.md)
> - **Pattern precedent (M3.1):** [2604141200-browser-extension-workflow-m31-plan.md](closed/2604141200-browser-extension-workflow-m31-plan.md)
> - **Pattern precedent (M3.2):** [2604141800-container-image-workflow-m32-plan.md](closed/2604141800-container-image-workflow-m32-plan.md)
> **Worktree:** Yes

---

## Summary

Create the Type 5 subject-specific workflow at `workflows/ci-action.md` and its criteria addendum at `references/criteria/ci-action.md`, then wire Type 5 routing and eval coverage. M3.3 closes the largest remaining Phase 3 gap: CI actions still fall through `workflows/generic.md`, which only knows "check whether it's pinned to commit SHAs" and misses the actual risk drivers for GitHub Actions and reusable workflows.

**Scope:** Type 5 CI-action audits, GitHub Actions-first: workflow file, criteria addendum, dispatcher wiring, eval coverage.
**Estimated Changes:** 4 files (2 new, 2 modified), ~600–750 lines.

---

## Objective

### Problem / Gap / Need

Type 5 (`ci-action`) still routes to `workflows/generic.md`. Current guidance is too thin:

1. `workflows/generic.md` only gives one GitHub-Action-specific check: "whether it's pinned to commit SHAs."
2. No native treatment for `pull_request_target`, `workflow_call`, `workflow_run`, or `secrets: inherit`.
3. No marketplace trust model beyond the brief `references/registries.md` CI/CD table.
4. No review path for action implementation type: composite action, JavaScript action, Docker action, or reusable workflow.
5. No transitive action audit guidance. A safe-looking top-level reusable workflow can call an unsafe child action.
6. No secret-access / token-permission rubric. `permissions:`, `id-token: write`, repo write scopes, and self-hosted runners radically change risk.

The framing eval names this explicitly: "GitHub Actions audits have no native treatment. No SHA-pinning rule, no `pull_request_target` warning, no marketplace verification, no transitive action audit."

### Success Criteria

- [ ] `workflows/ci-action.md` exists and follows the Identify / Evidence / Subject Rubric / Subject Verdict Notes template
- [ ] `references/criteria/ci-action.md` exists and defines CI-action-specific scoring for publisher trust, ref immutability, trigger/secret exposure, and transitive audit depth
- [ ] `SKILL.md` dispatch table row 5 routes to `workflows/ci-action.md`
- [ ] `SKILL.md` Reference Files includes `workflows/ci-action.md` and `references/criteria/ci-action.md`
- [ ] `evals/evals.json` gains at least 2 Type 5 cases: one clean SHA-pinned positive path, one negative path that exercises `pull_request_target` + secret inheritance + transitive unpinned child
- [ ] No regressions in eval ids 0–13

### Out of Scope

- New helper scripts for GitHub Marketplace lookup, workflow parsing, or transitive `uses:` crawling
- Broad rewrites to `references/criteria.md` or `references/registries.md` unless execution finds a factual gap that blocks the workflow
- Full GitLab CI component / CircleCI orb parity beyond note-level mapping of the same trust principles
- Phase 3 M3.4+ workflows (`ide-plugin`, long-tail subjects)

---

## Context

### Current State

`SKILL.md` classifies Type 5 correctly (`uses:` in workflows, GitLab `include:`, CircleCI `orbs:`, GitHub `owner/action@ref`) but still dispatches Type 5 to `workflows/generic.md`. The generic workflow has only two CI-specific fragments:

- Tier 3 trigger: "Will run in CI/CD with access to secrets"
- Research hint: "For GitHub Actions: whether it's pinned to commit SHAs"

`references/registries.md` already contains the core CI trust baseline:

- `actions/*` official = High
- Marketplace verified creator = Medium-High
- Marketplace unverified = Medium, pin to SHA
- Critical rule: any action that accesses `secrets.*` must be pinned to a commit SHA

There is no existing Type 5 criteria addendum, no Type 5 workflow, and no Type 5 eval coverage.

### Key Files

| File | Role | Change Summary |
|------|------|----------------|
| `workflows/ci-action.md` | **New.** Type 5 workflow | Create GitHub Actions-first workflow: ref parsing, trigger/secret review, implementation-type review, transitive `uses:` audit, verdict notes |
| `references/criteria/ci-action.md` | **New.** Type 5 criteria addendum | Create CI-specific scoring: publisher trust, pinning matrix, trigger exposure, permission/token scope, transitive depth guidance, tier thresholds |
| `SKILL.md` | Dispatcher + reference-file index | Row 5 → `workflows/ci-action.md`; add 2 Reference Files bullets |
| `evals/evals.json` | Regression + new Type 5 coverage | Add ids 14 and 15 for positive and negative Type 5 paths |

### Dependencies

- **Requires:** Phase 3 M3.1 and M3.2 complete; dispatcher architecture stable; `references/registries.md` CI table already present
- **Blocks:** Phase 3 M3.5 eval gate; Phase 3 exit criterion that `generic.md` no longer handles high-volume Type 5 subjects

### Constraints

- Workflow must use the standard 4-section template
- Audit Coverage table and audit-confidence statement remain owned by `SKILL.md` Step N
- No scripts in M3.3; evidence acquisition is doc/web/source inspection
- Repo is dirty (`AGENTS.md` untracked), so execution should use worktree mode
- Type 5 file routes all CI-action subjects, but v1 depth will be GitHub Actions-first because local trust references and milestone wording are GitHub-native

### Assumptions

- GitHub Actions and reusable workflows are the dominant Type 5 path worth optimizing first; GitLab/CircleCI can inherit the same principles with shorter notes in v1
- Full 40-char commit SHA is the only immutable ref for GitHub Actions; tags, release tags, semver tags, and branches are mutable
- `pull_request_target`, `workflow_run`, `workflow_call` + `secrets: inherit`, self-hosted runners, and write-capable `permissions:` are the dominant exposure multipliers
- Transitive audit must inspect at least the first nested `uses:` layer; deeper recursion is only required when the first layer stays opaque or introduces mutable refs / secret-bearing children

### Impact Analysis

- **Direct:** New workflow, new criteria addendum, dispatcher wiring, eval additions
- **Adjacent:** `workflows/generic.md` no longer handles Type 5 once M3.3 lands, but needs no edits
- **Downstream:** M3.5 eval gate becomes reachable for Type 5; later Type 8/9 work can reuse the same secret-scope and nested-trust-boundary phrasing

---

## Implementation

### Overview

Execution is 4 steps: addendum first, workflow second, dispatcher wiring third, evals fourth. No shared-core doc changes expected. If execution discovers missing CI facts in `references/registries.md`, treat that as a scoped follow-up only if the workflow cannot be written cleanly without it.

### Step 1: Create `references/criteria/ci-action.md`

**Objective:** Define CI-action-specific scoring extensions that the workflow can cite.
**Confidence:** High
**Depends on:** None

**Files:**
- `references/criteria/ci-action.md` (new)

**Changes:**

Create a new addendum with this structure:

```markdown
# CI Action — Criteria Addendum

Per-subject scoring extensions for **Type 5: ci-action** audits.
Layers on top of `references/criteria.md`. More-specific guidance wins.

Covers: GitHub Actions, reusable workflows, GitLab CI components, CircleCI orbs.
Depth is GitHub Actions-first in v1.

## Publisher / Marketplace Trust Signals

| Source | Trust | Notes |
|--------|-------|-------|
| `actions/*` official | High | First-party GitHub-maintained actions |
| Marketplace verified creator | Medium-High | Strong signal, still require source review + pinning |
| Same-org repo + public source + established history | Medium | Good when no marketplace badge exists |
| Third-party marketplace action, unverified | Medium-Low | SHA pin required |
| Direct repo action, no marketplace / sparse history | Low | Tier 3 unless tightly scoped and SHA pinned |

## Ref Immutability Matrix

| Ref style | Mutability | Scoring impact |
|-----------|------------|----------------|
| Full commit SHA | Immutable | Required for Tier 1 and any secret-bearing third-party action |
| Release tag (`v4`, `v1.2.3`) | Mutable | Default to CONDITIONAL; reject when paired with secrets/write perms on third-party code |
| Branch (`main`, `master`) | Mutable | High-risk / Tier 3 |
| PR ref / SHA from fork | Mutable + untrusted | Reject for privileged workflows |

## Trigger & Secret Exposure Matrix

Cover: `pull_request`, `pull_request_target`, `workflow_dispatch`, `workflow_run`,
`schedule`, `workflow_call`, `secrets: inherit`, self-hosted runner, forked-code checkout,
artifact consumption, and `permissions:` scope (`contents`, `packages`, `actions`,
`pull-requests`, `id-token`).

## Action Implementation Types

Cover what to inspect for:
- JavaScript action (`action.yml` + `runs.using: node*` + compiled `dist/`)
- Composite action (`runs.using: composite`; nested shell + nested `uses:`)
- Docker action (`Dockerfile`, entrypoint, base image, network/download behavior)
- Reusable workflow (`workflow_call`; jobs, permissions, inherited secrets, nested actions)

## Transitive Action Audit Guidance

- Tier 1: note transitive surface; no recursion unless child refs are already visible
- Tier 2: inspect first nested `uses:` layer
- Tier 3: inspect first nested layer; continue one more layer for any child that is mutable,
  secret-bearing, privileged, or opaque

## Tier Thresholds (CI Actions)

### Tier 1 — Quick Audit
ALL: official or verified creator; full SHA pin; no `pull_request_target`; no inherited secrets
into third-party code; minimal read-only permissions; no high-risk transitive child.

### Tier 2 — Standard Audit
Default. Tag-pinned or moderate-trust actions without privileged trigger/secret shape.

### Tier 3 — Deep Audit
ANY: branch pin; unverified third-party action with secrets/write perms; `pull_request_target`;
`workflow_call` + `secrets: inherit`; self-hosted runner with untrusted input; opaque transitive
child; Docker/composite action running download-and-execute patterns.
```

**Rationale:** The shared rubric and `references/registries.md` already hold the baseline, but they do not define CI-specific scoring mechanics. This addendum becomes the single home for pinning severity, trigger risk, token scope, and transitive depth rules.

**Verification:** File exists. Sections present: publisher trust, ref immutability, trigger/secret exposure, implementation types, transitive audit guidance, tier thresholds.

**If this fails:** Delete `references/criteria/ci-action.md`.

---

### Step 2: Create `workflows/ci-action.md`

**Objective:** Author the Type 5 workflow with GitHub Actions-first evidence and verdict guidance.
**Confidence:** High
**Depends on:** Step 1

**Files:**
- `workflows/ci-action.md` (new)

**Changes:**

Create the workflow with this structure:

```markdown
<!--
workflows/ci-action.md - Type 5 subject-specific workflow.
GitHub Actions-first. Covers reusable workflows and nested actions.
Dispatcher owns the final verdict tree + Audit Coverage rendering.
-->

# CI Action Workflow (Type 5)

This workflow handles **Type 5: ci-action** subjects: GitHub Actions,
reusable workflows, GitLab CI components, and CircleCI orbs.
Primary depth in v1: GitHub Actions / reusable workflows.

## Identify

Extract and normalize:
- Subject class: action | reusable workflow | GitLab component | CircleCI orb
- GitHub ref: `<owner>/<repo>@<ref>` or reusable workflow path
- Ref type: full SHA | tag | branch | unknown
- Publisher identity: `actions/*` official | verified creator | same-org public repo | unknown
- Invocation context: trigger, runner type, `permissions:`, `secrets: inherit`, explicit secrets,
  forked PR involvement, artifact inputs, checkout/build of untrusted code
- Implementation type: JavaScript | composite | Docker | reusable workflow

If non-GitHub Type 5, map the same questions to the closest equivalent and call out reduced confidence.

## Evidence — Part A: Tier Triage

Tier by pin immutability + publisher trust + exposure:
- Tier 1: SHA pinned, trusted publisher, read-only / low-secret context
- Tier 2: default
- Tier 3: mutable ref, privileged trigger, inherited secrets, self-hosted runner,
  or opaque transitive child

## Evidence — Part B: Research

Answer these questions:
1. Is this the real action / workflow from the real publisher?
2. Is the ref immutable?
3. What trigger runs it, and does that trigger expose secrets or write scopes to untrusted input?
4. What `permissions:` and secrets does it receive?
5. What code actually runs? (`action.yml`, workflow YAML, Dockerfile, composite shell steps)
6. What nested `uses:` refs or base images does it pull in, and are those pinned?
7. Does it write to repo contents, releases, packages, checks, deployments, or mint OIDC tokens?
8. Are there prior incidents, compromises, or maintainer-transfer warnings?

GitHub-specific checks must include:
- marketplace listing / verified creator when applicable
- `pull_request_target` warning
- `workflow_call` + `secrets: inherit` review
- `permissions:` least-privilege review
- transitive `uses:` inspection
- self-hosted runner note when present

### Audit coverage tracking

Type 5 rows:
- Marketplace / publisher verification
- Ref pin review
- Trigger review
- Secrets / `permissions:` review
- Action source review (`action.yml` / workflow YAML / Dockerfile)
- Transitive child review
- Incident / advisory search
- Runner context review

## Subject Rubric — Evaluate

### 4.1 Provenance & Identity
- Official / verified creator / org alignment
- Repo history, release provenance, marketplace identity consistency

### 4.2 Maintenance & Longevity
- Release cadence, issue response, recent ownership transfer, archival state

### 4.3 Security Track Record
- Prior compromise, security advisories, suspicious maintainer or release changes

### 4.4 Permissions & Access
- This is the dominant axis for Type 5
- Trigger safety, secrets exposure, `permissions:` scope, self-hosted runner risk,
  checkout/build of untrusted code, OIDC / package publish scopes

### 4.5 Reliability & Compatibility
- SHA pin quality, mutable-tag drift risk, reusable workflow compatibility,
  action runtime / deprecation state, required runner assumptions

### 4.6 Alternatives
- Prefer official first-party or verified alternatives when a third-party action is risky

## Subject Verdict Notes

Toward REJECTED:
- `pull_request_target` + third-party mutable ref
- `workflow_call` + `secrets: inherit` into third-party workflow not SHA pinned
- Branch / `main` pin on action with write scopes, OIDC, package publish, or secret access
- Unknown transitive child introduced by composite / reusable workflow
- Self-hosted runner + untrusted external code path

Toward CONDITIONAL:
- Trusted action but tag-pinned instead of SHA
- Verified creator, low-risk trigger, but mutable ref or broader-than-needed permissions
- Clean top-level action with one moderate-risk child that can be SHA pinned

Toward APPROVED:
- Official or verified publisher
- Full SHA pin top-level and transitive children
- Read-only or narrowly scoped permissions
- No privileged trigger / secret inheritance issues
- No negative incident history
```

**Rationale:** This mirrors the established Phase 3 workflow shape but makes Type 5 risks first-class. The critical distinction is that CI actions are judged less by "what package is this" and more by "what code executes in what trust context with what secrets and write scopes."

**Verification:** File exists. Contains the 4 required sections. References `references/criteria/ci-action.md`. Does not duplicate dispatcher-owned final report text.

**If this fails:** Delete `workflows/ci-action.md`.

---

### Step 3: Update `SKILL.md`

**Objective:** Route Type 5 to the new workflow and index the new reference files.
**Confidence:** High
**Depends on:** Step 2

**Files:**
- `SKILL.md`

**Changes:**

Dispatch table row:

```markdown
// Before:
| 5 | ci-action | `workflows/generic.md` | Fallback — specific workflow lands in Phase 3 (M3.3) |

// After:
| 5 | ci-action | `workflows/ci-action.md` | Live — Phase 3 (M3.3) |
```

Reference Files list:

```markdown
// Insert after container-image bullets:
- `workflows/ci-action.md` — Type 5 ci-action workflow (Phase 3, M3.3)
- `references/criteria/ci-action.md` — CI-action criteria addendum (publisher trust, pinning, trigger/secret exposure, transitive audit)
```

**Rationale:** Dispatcher routing and the reference-file index are the only `SKILL.md` edits needed for M3.3. All subject logic lives in the new workflow and addendum.

**Verification:** `rg -n "ci-action|workflows/ci-action.md|references/criteria/ci-action.md" SKILL.md` shows row 5 → live route plus the two reference-file bullets.

**If this fails:** Revert the row and remove the two bullets; Type 5 continues to route through `workflows/generic.md`.

---

### Step 4: Update `evals/evals.json`

**Objective:** Add positive and negative Type 5 regression coverage.
**Confidence:** High
**Depends on:** Steps 2–3

**Files:**
- `evals/evals.json`

**Changes:**

Add id 14 — clean positive path:

```json
{
  "id": 14,
  "prompt": "Our workflow uses `actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683` on `pull_request` with `permissions: contents: read` and no extra secrets. Is this safe?",
  "expected_output": "Tier 1 quick audit. Routes to ci-action workflow. Should recognize `actions/checkout` as an official `actions/*` action, note the full commit-SHA pin, note the read-only permission scope and lack of `pull_request_target` / inherited-secrets exposure, and return APPROVED.",
  "files": [],
  "assertions": [
    {"text": "Subject type is ci-action", "type": "contains_concept"},
    {"text": "Report identifies `actions/checkout` as official or trusted", "type": "contains_concept"},
    {"text": "Report notes the action is pinned to a full commit SHA", "type": "contains_concept"},
    {"text": "Report notes the workflow uses read-only permissions or no dangerous secret exposure", "type": "contains_concept"},
    {"text": "Verdict is APPROVED", "type": "exact_match"},
    {"text": "Audit confidence", "type": "contains_concept"}
  ]
}
```

Add id 15 — negative privileged/transitive path:

```json
{
  "id": 15,
  "prompt": "Can I use this reusable workflow from another org?\n\n```yaml\non: pull_request_target\njobs:\n  release:\n    permissions:\n      contents: write\n      pull-requests: write\n    uses: vendor/release-workflow/.github/workflows/publish.yml@v2\n    secrets: inherit\n```\n\nI checked the reusable workflow and it calls `third-party/build-action@main`.",
  "expected_output": "Tier 3 deep audit. Routes to ci-action workflow. Should flag `pull_request_target`, inherited secrets, write-capable permissions, top-level tag pin instead of full SHA, and the transitive child action pinned to `main`. Verdict must be REJECTED.",
  "files": [],
  "assertions": [
    {"text": "Subject type is ci-action", "type": "contains_concept"},
    {"text": "Report flags `pull_request_target` as high-risk or dangerous", "type": "contains_concept"},
    {"text": "Report flags inherited secrets or privileged token scope", "type": "contains_concept"},
    {"text": "Report flags the top-level ref or transitive child as not SHA pinned", "type": "contains_concept"},
    {"text": "Report audits the nested or transitive action", "type": "contains_concept"},
    {"text": "Verdict is REJECTED", "type": "exact_match"},
    {"text": "## Audit Coverage", "type": "contains_string"},
    {"text": "Audit confidence", "type": "contains_concept"}
  ]
}
```

Do not rewrite existing ids 0–13 unless execution uncovers a schema issue.

**Rationale:** These two evals force the workflow to prove the two core M3.3 promises: it can approve a clean SHA-pinned official action and reject a privileged reusable workflow with mutable transitive code.

**Verification:** `python -c "import json; json.load(open('evals/evals.json', encoding='utf-8'))"` succeeds. IDs 14 and 15 exist. Total eval count becomes 16.

**If this fails:** Revert `evals/evals.json`.

---

## Verification Plan

### Automated Checks

- [ ] `python -c "import json; json.load(open('evals/evals.json', encoding='utf-8'))"`
- [ ] `rg -n "ci-action|workflows/ci-action.md|references/criteria/ci-action.md" SKILL.md`
- [ ] `rg -n "^## " workflows/ci-action.md` shows Identify / Evidence / Subject Rubric / Subject Verdict Notes
- [ ] File exists: `workflows/ci-action.md`
- [ ] File exists: `references/criteria/ci-action.md`

### Manual Verification

- [ ] Read `references/criteria/ci-action.md` end-to-end; confirm ref immutability, trigger/secret matrix, transitive depth, and tier thresholds are internally consistent
- [ ] Read `workflows/ci-action.md` end-to-end; confirm it routes non-GitHub Type 5 subjects with reduced-confidence notes rather than pretending full parity
- [ ] Mental-trace eval id 14 through the workflow; confirm APPROVED is reachable only because the action is official, SHA pinned, and low-privilege
- [ ] Mental-trace eval id 15 through the workflow; confirm REJECTED follows from `pull_request_target` + inherited secrets + mutable transitive child without needing extra assumptions

### Acceptance Criteria Validation

| Criterion | How to Verify | Expected Result |
|-----------|---------------|-----------------|
| Workflow exists with correct template | Read `workflows/ci-action.md` | 4 required sections present |
| Addendum exists with CI scoring | Read `references/criteria/ci-action.md` | Publisher trust, pinning, trigger/secret, implementation-type, transitive, tier sections present |
| Dispatcher routes Type 5 correctly | Grep `SKILL.md` | Row 5 → `workflows/ci-action.md`; Reference Files bullets added |
| Positive Type 5 eval exists | Read `evals/evals.json` | id 14 present; APPROVED path assertions intact |
| Negative Type 5 eval exists | Read `evals/evals.json` | id 15 present; `pull_request_target` + transitive child assertions intact |
| No regressions | Diff `evals/evals.json` | ids 0–13 unchanged except for formatting if unavoidable |

---

## Rollback Plan

1. Revert `SKILL.md` row 5 and remove the two Type 5 Reference Files bullets so Type 5 falls back to `workflows/generic.md` again.
2. Revert `evals/evals.json` to remove ids 14 and 15.
3. Delete `workflows/ci-action.md`.
4. Delete `references/criteria/ci-action.md`.

Recommended rollback order is front-loaded on routing: restore `SKILL.md` first so unfinished Type 5 docs never become live.

---

## Notes

### Risks

- **GitHub-first bias:** Type 5 includes GitLab and CircleCI, but milestone inputs are GitHub-native. Mitigation: state that v1 is GitHub Actions-first, map non-GitHub systems by equivalent trust concepts, and mark confidence lower when ecosystem-specific evidence is thin.
- **Transitive depth explosion:** Reusable workflows and composite actions can recurse. Mitigation: make first nested layer mandatory; go one layer deeper only when mutable refs, secrets, or privileged runners appear.
- **Marketplace badge drift:** "Verified creator" wording may change. Mitigation: use badge as one trust signal, not the only one; corroborate with source repo org, repo history, and action ownership consistency.

### Open Questions

None. Scope is bounded, precedent exists, and the local source set already contains the minimum trust data needed to draft the workflow cleanly.
