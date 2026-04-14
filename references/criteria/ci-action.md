# CI Action — Criteria Addendum

Per-subject scoring extensions for **Type 5: ci-action** audits. This
addendum layers on top of the shared rubric in `references/criteria.md`.
When guidance here conflicts with the shared rubric, the more specific
ci-action guidance wins.

Covers: GitHub Actions, reusable workflows, GitLab CI components, CircleCI
orbs, and equivalent CI-imported automation. Depth is GitHub Actions-first
in v1 because the repo's current refs and milestone scope are GitHub-heavy.

## Publisher / Marketplace Trust Signals

| Source | Trust | Notes |
|--------|-------|-------|
| `actions/*` official | High | First-party GitHub-maintained actions. Still inspect the actual ref and privileges. |
| Marketplace verified creator | Medium-High | Strong identity signal, but still require source review plus immutable pinning. |
| Same-org repo + public source + established history | Medium | Reasonable default when the org is known and the repo history is stable. |
| Third-party marketplace action, unverified | Medium-Low | SHA pin required; mutable refs push this toward Tier 3. |
| Direct repo action, no marketplace / sparse history | Low | Treat as higher risk unless the usage context is tightly scoped and low privilege. |

### Scoring impact

- `actions/*` official + full SHA pin = strong positive
- Verified creator badge = moderate positive, not sufficient on its own
- Same-org repo without marketplace presence = neutral to moderate positive
- Unknown maintainer, sparse history, or recent repo transfer = moderate to
  strong negative depending on privilege

## Ref Immutability Matrix

| Ref style | Mutability | Scoring impact |
|-----------|------------|----------------|
| Full commit SHA | Immutable | Required for Tier 1 and for any secret-bearing third-party action path |
| Release tag (`v4`, `v1.2.3`) | Mutable | Usually CONDITIONAL; reject when paired with secrets, write perms, or untrusted code paths |
| Branch (`main`, `master`) | Mutable | High-risk; pushes subject to Tier 3 |
| PR ref / fork SHA path | Mutable + untrusted | Reject for privileged workflows |
| Unknown / omitted | Unknown | Treat as mutable until proven otherwise |

### Scoring impact

- Full 40-char SHA = strong positive
- Semantic tag or major tag = moderate negative because retargeting is possible
- Branch or floating ref = strong negative
- Secret-bearing or write-capable third-party code not pinned to SHA = high-risk finding

## Trigger & Secret Exposure Matrix

Review trigger shape and execution trust boundaries together:

| Context | Risk | Notes |
|---------|------|-------|
| `pull_request` with read-only permissions | Lower | Default safer PR path; still inspect checkout/build of contributed code |
| `workflow_dispatch` or `schedule` with narrow permissions | Medium | Trusted initiator, but still evaluate action code and write scopes |
| `workflow_run` consuming artifacts from other workflows | Medium-High | Artifact trust boundary matters; trace producer workflow if privileged |
| `workflow_call` without inherited secrets | Medium | Review caller + callee permissions and nested actions |
| `workflow_call` + `secrets: inherit` | High | Secrets flow across workflow boundary; treat third-party code as privileged |
| `pull_request_target` | High | Privileged trigger against fork-controlled inputs unless extremely constrained |
| Self-hosted runner + untrusted input | High | Host exposure is materially worse than GitHub-hosted runners |

Also inspect:
- Explicit `secrets.*` usage
- `permissions:` scope (`contents`, `packages`, `actions`, `checks`,
  `deployments`, `pull-requests`, `id-token`)
- Forked-code checkout or build execution
- Artifact download / reuse from lower-trust workflows

### Scoring impact

- Read-only token + no inherited secrets = positive
- Write scopes, package publish, deployment, or `id-token: write` = elevated review depth
- `pull_request_target` with third-party mutable refs = reject pattern
- `workflow_call` + `secrets: inherit` into third-party workflow = reject unless fully pinned and tightly scoped

## Action Implementation Types

Inspect according to execution mechanism:

| Type | What to inspect | Risk notes |
|------|-----------------|-----------|
| JavaScript action | `action.yml`, `runs.using: node*`, committed `dist/`, package manager metadata | Check whether committed runtime output matches source expectations and whether the action downloads more code at runtime |
| Composite action | `runs.using: composite`, inline shell, nested `uses:` refs | Composite actions often hide extra shell and transitive action calls |
| Docker action | `Dockerfile`, base image, entrypoint, network/download behavior | Review image provenance, runtime fetches, privilege assumptions, and any embedded secrets or package installs |
| Reusable workflow | `workflow_call`, jobs, `permissions:`, secrets flow, nested actions | Treat as a privileged orchestration layer; inspect the child jobs, not just the top-level `uses:` |

### Scoring impact

- Transparent JavaScript action with committed source + dist = moderate positive
- Composite or reusable workflow with opaque nested calls = moderate negative until transitive review is complete
- Docker action with download-and-execute patterns or privileged assumptions = strong negative

## Transitive Action Audit Guidance

- Tier 1: note transitive surface; no recursion unless child refs are already
  visible and obviously risky
- Tier 2: inspect the first nested `uses:` layer
- Tier 3: inspect the first nested layer, then continue one more layer for
  any child that is mutable, secret-bearing, privileged, or opaque

Escalate depth when a child action or reusable workflow:
- is pinned to a tag or branch
- receives secrets or write-capable token scopes
- runs on a self-hosted runner
- hides execution in composite shell or Docker entrypoint code
- downloads remote code or containers at runtime

## Tier Thresholds (CI Actions)

### Tier 1 — Quick Audit

Use only when ALL of these hold:
- Official `actions/*` or verified creator with consistent source identity
- Top-level ref pinned to a full commit SHA
- No `pull_request_target`
- No inherited secrets into third-party code
- Minimal read-only permissions
- No risky transitive child refs visible from the current context

### Tier 2 — Standard Audit

Default path for:
- Tag-pinned actions from otherwise credible publishers
- Same-org reusable workflows with moderate privileges
- Actions where source is visible but one or two trust questions remain open

Review top-level source, trigger shape, permissions, and the first nested
`uses:` layer.

### Tier 3 — Deep Audit

Use when ANY of these are true:
- Branch pin or unknown ref
- Unverified third-party action with secrets or write permissions
- `pull_request_target`
- `workflow_call` + `secrets: inherit`
- Self-hosted runner with untrusted input
- Opaque or mutable transitive child
- Docker or composite action running download-and-execute patterns

Deep audits must examine the first nested layer and continue one more layer
when the first child still carries privilege, mutability, or opacity.
