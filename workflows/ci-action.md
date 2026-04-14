<!--
workflows/ci-action.md - Type 5 subject-specific workflow.
Handles GitHub Actions, reusable workflows, GitLab CI components, and
CircleCI orbs referenced from CI configuration. GitHub Actions-first in v1.

This workflow replaces workflows/generic.md for Type 5 subjects. After
producing findings here, return to SKILL.md Step N for the shared verdict
tree and report shape. The Audit Coverage table and audit-confidence
assertion are owned by the dispatcher - do not duplicate them here.

Phase 3 / M3.3 - fourth subject-specific workflow (third Phase 3).
-->

# CI Action Workflow (Type 5)

This workflow handles **Type 5: ci-action** subjects - GitHub Actions,
reusable workflows, GitLab CI components, CircleCI orbs, and equivalent
CI-imported automation referenced from pipeline config. Primary depth in
v1 is GitHub Actions / reusable workflows because the repo's trust
references and milestone scope are GitHub-first.

After completing all sections below, return to `SKILL.md` Step N for the
shared verdict tree and audit-coverage report shape.

Sections follow the standard workflow template: **Identify / Evidence /
Subject Rubric / Subject Verdict Notes**.

Use `references/criteria/ci-action.md` for ci-action-specific tiering and
scoring. When it conflicts with the shared rubric, the more specific
ci-action guidance wins.

## Identify

### 1. Determine the subject class and execution shape

Extract and normalize:

- Subject class: action | reusable workflow | GitLab component | CircleCI orb
- GitHub ref: `<owner>/<repo>@<ref>` or reusable workflow path
- Ref type: full SHA | tag | branch | unknown
- Publisher identity: `actions/*` official | verified creator | same-org public repo | unknown
- Invocation context: trigger, runner type, `permissions:`, `secrets: inherit`,
  explicit secrets, forked PR involvement, artifact inputs, checkout/build of
  untrusted code
- Implementation type: JavaScript | composite | Docker | reusable workflow

If the subject is non-GitHub Type 5, map the same questions to the closest
equivalent and say confidence is lower when ecosystem-specific evidence is
thin.

### 2. Gather required context

Collect before proceeding:

1. Full action or workflow reference, including the exact ref
2. Trigger context: `pull_request`, `pull_request_target`, `workflow_call`,
   `workflow_run`, `workflow_dispatch`, `schedule`, or equivalent
3. Runner context: GitHub-hosted vs self-hosted
4. Token and secret scope: `permissions:`, explicit secrets, `secrets: inherit`
5. Whether the workflow checks out, builds, or executes untrusted external code

If any of 1-4 are missing, ask before proceeding. Item 5 can be confirmed
during source review if not obvious from the user's prompt.

## Evidence - Part A: Tier Triage

Tier the subject using `references/criteria/ci-action.md`, combining
publisher trust, ref immutability, trigger shape, token scope, runner
context, and transitive visibility.

### Tier 1 - Quick Audit

Use only when all of these hold:

- Official `actions/*` action or verified creator
- Full commit SHA pin
- Read-only or tightly scoped permissions
- No `pull_request_target`
- No inherited secrets into third-party code
- No risky transitive child visible from the current context

Quick audit scope: confirm publisher identity, SHA pinning, permission
scope, trigger safety, and any obvious nested `uses:` refs. If those stay
clean, proceed to Subject Verdict Notes without deeper recursion.

### Tier 2 - Standard Audit

Default path for most ci-action subjects:

- Tag-pinned action or reusable workflow
- Same-org or established third-party publisher
- Moderate privileges or one open trust question

Standard scope: review top-level source, trigger shape, permissions/secrets,
runner context, and the first nested `uses:` layer.

### Tier 3 - Deep Audit

Use when any higher-risk condition appears:

- Branch pin or unknown ref
- `pull_request_target`
- `workflow_call` plus `secrets: inherit`
- Self-hosted runner with untrusted input
- Write-capable permissions, package publish, deployment, or `id-token: write`
- Opaque or mutable transitive child

Deep scope: full Tier 2 work plus one more layer of transitive inspection
for any child that stays mutable, privileged, secret-bearing, or opaque.

## Evidence - Part B: Research

### Core research questions

Answer every question that applies to the assigned tier:

1. Is this the real action or workflow from the real publisher?
2. Is the ref immutable?
3. What trigger runs it, and does that trigger expose secrets or write scopes
   to untrusted input?
4. What `permissions:` and secrets does it receive?
5. What code actually runs: `action.yml`, workflow YAML, `Dockerfile`, or
   composite shell steps?
6. What nested `uses:` refs or base images does it pull in, and are those pinned?
7. Does it write to repo contents, releases, packages, checks, deployments,
   or mint OIDC tokens?
8. Are there prior incidents, compromises, maintainer transfers, or other
   provenance warnings?

### GitHub-specific checks

Always include these when the subject is on GitHub:

- Marketplace listing and verified creator state when applicable
- `pull_request_target` warning and trust-boundary review
- `workflow_call` plus `secrets: inherit` review
- `permissions:` least-privilege review
- Transitive `uses:` inspection
- Self-hosted runner note when present

### Audit coverage tracking

Track whether each ci-action surface was actually audited:

- Marketplace / publisher verification
- Ref pin review
- Trigger review
- Secrets / `permissions:` review
- Action source review (`action.yml` / workflow YAML / `Dockerfile`)
- Transitive child review
- Incident / advisory search
- Runner context review

## Subject Rubric - Evaluate

### 4.1 Provenance & Identity

- Official / verified creator / org alignment
- Repo history, release provenance, marketplace identity consistency
- Namespace or ownership changes that weaken trust

### 4.2 Maintenance & Longevity

- Release cadence
- Issue response and maintenance signals
- Archive status, stale runtime targets, or recent ownership transfer

### 4.3 Security Track Record

- Prior compromise, suspicious release changes, or advisory history
- Security policy presence and maintainer response quality

### 4.4 Permissions & Access

This is the dominant axis for Type 5:

- Trigger safety
- Secrets exposure
- `permissions:` scope
- Self-hosted runner risk
- Checkout/build of untrusted code
- OIDC, package publish, deployment, or repo-write scopes

### 4.5 Reliability & Compatibility

- SHA pin quality vs mutable-tag drift risk
- Reusable workflow compatibility assumptions
- Action runtime / deprecation state
- Required runner assumptions and external service dependencies

### 4.6 Alternatives

Prefer official first-party or verified alternatives when a third-party
action is risky, stale, or over-privileged.

## Subject Verdict Notes

Toward REJECTED:

- `pull_request_target` plus third-party mutable ref
- `workflow_call` plus `secrets: inherit` into third-party workflow not SHA pinned
- Branch or `main` pin on an action with write scopes, OIDC, package publish,
  or secret access
- Unknown transitive child introduced by composite or reusable workflow
- Self-hosted runner plus untrusted external code path

Toward CONDITIONAL:

- Trusted action but tag-pinned instead of SHA-pinned
- Verified creator with low-risk trigger but mutable ref or broader-than-needed permissions
- Clean top-level action with one moderate-risk child that can be SHA pinned

Toward APPROVED:

- Official or verified publisher
- Full SHA pin for the top-level subject and visible transitive children
- Read-only or narrowly scoped permissions
- No privileged trigger or secret inheritance issues
- No negative incident history found
