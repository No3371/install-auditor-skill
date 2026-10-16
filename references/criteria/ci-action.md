# CI Action — Criteria Addendum

Per-subject scoring extensions for **Type 5: ci-action** audits. This
addendum layers on top of the shared rubric in `references/criteria.md`.
When guidance here conflicts with the shared rubric, the more specific
ci-action guidance wins, except for §4.6 (version & update integrity): this
file only tightens it or fills its plug-ins (`SKILL.md` Tree terms →
Precedence).

Covers: GitHub Actions, reusable workflows, GitLab CI components, CircleCI
orbs, and equivalent CI-imported automation. Depth is GitHub Actions-first
in v1.

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
- Verified creator badge = moderate positive for publisher identity, not
  code (`references/criteria.md` §4.6 V2); not sufficient on its own
- Same-org repo without marketplace presence = neutral to moderate positive
- Unknown maintainer, sparse history, or recent repo transfer = moderate to
  strong negative depending on privilege

## Ref Immutability Matrix

| Ref style | Mutability | Scoring impact |
|-----------|------------|----------------|
| Full commit SHA, reachable from a branch or tag of the named repo | Immutable | Required for Tier 1 and for any secret-bearing third-party action path |
| Full commit SHA reachable only through a fork (impostor commit) | Not the publisher's code | Treat as an unknown ref |
| Exact-version tag (`v1.2.3`) of a verified immutable release | Immutable while the release exists; the tag name is never reused | An immutable ref, not a mutable tag: LOW note (prefer the SHA). Official/verified publisher: no pin condition. Tier 1 still needs a full SHA. Unverified publisher in a privileged job: still a non-SHA ref (`SKILL.md` Red Flag) |
| Release tag (`v4`, `v1.2.3`) | Mutable | CONDITIONAL from official/verified publishers (condition: pin to SHA); reject when the publisher is unverified and the job holds secrets, write perms, OIDC, or publish rights, or on untrusted code paths |
| Tag locked in the consuming repo's `.github/workflows/actions.lock` (public preview) | The locked commit runs; repo identity is checked at run time | Official/verified publisher, lock entry `commit` = the audited commit → MEDIUM instead of HIGH, no pin condition. Red Flag cases and Tier 1 unchanged: the workflow file still names a mutable ref |
| Branch (`main`, `master`) | Mutable | High-risk; pushes subject to Tier 3 |
| PR ref / fork SHA path | Mutable + untrusted | Reject for privileged workflows |
| Unknown / omitted | Unknown | Treat as mutable until proven otherwise |

- **Check immutability:** `gh release verify <tag> -R <owner>/<repo>` passes,
  or the release page shows **Immutable**. A floating major tag (`v4`) is a
  plain tag the publisher moves by design; it is never an immutable release.
- **Check reachability:** the SHA is a tag target or on a branch of the named
  repo (`git ls-remote https://github.com/<owner>/<repo>`; the commit page
  shows no "does not belong to any branch" warning). GitHub serves commits
  from the whole fork network under the parent repo's name.

### Scoring impact

- Full 40-char SHA = strong positive
- Semantic tag or major tag = moderate negative because retargeting is possible
- Branch or floating ref = strong negative
- SHA reachable only through a fork = unknown ref (CRITICAL in a privileged
  job via the `SKILL.md` Red Flag)
- Secret-bearing or write-capable code not pinned to SHA = HIGH finding (official/verified publisher, tag ref) | CRITICAL (branch/unknown ref, or unverified third-party publisher — `SKILL.md` Red Flags)

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
| Low-trust trigger (`pull_request_target`, `issue_comment`, `workflow_run`) declaring `cache-mode: write` or `write-only` | High | GitHub gives these triggers read-only access to the default-branch cache; the override lets untrusted input poison caches that privileged workflows restore |
| Release, publish, or deploy job (`id-token: write`, publish token) that restores caches | Medium-High | Caches are unsigned. Confirm only trusted triggers (`push`, `schedule`, `workflow_dispatch`, …) write those keys |
| PR head checked out or fetched under `pull_request_target` / `workflow_run` / `issue_comment` (`allow-unsafe-pr-checkout: true`, `ref:` set to the PR head, `repository:` set to the fork, `gh pr checkout`, `git fetch` of PR refs) | High | `actions/checkout` v7.0.0+ (backports: v4.4.0, v5.1.0, v6.1.0) refuses fork PR checkout under `pull_request_target` / `workflow_run` unless `allow-unsafe-pr-checkout` is set; other fetch paths are not covered |
| Tools installed outside `uses:` (`run:` downloads piped to a shell, unversioned `pip` / `npm` / `apt` / `go install …@latest`, `container:` / `services:` images by tag) | Medium | Same drift risk as a mutable action ref; rated by job privilege below |

Also inspect:
- Explicit `secrets.*` usage
- `permissions:` scope (`contents`, `packages`, `actions`, `checks`,
  `deployments`, `pull-requests`, `id-token`)
- Forked-code checkout or build execution
- Artifact download / reuse from lower-trust workflows
- Cache restores (`actions/cache`, `actions/cache/restore`, setup-action
  `cache:` inputs) and `cache-mode` at workflow and job level
- `id-token: write`: any step in the job, including third-party actions and
  `run:` scripts, can request an OIDC token, so every step there can
  publish or deploy as the workflow

`pull_request_target` runs the workflow file from the default branch, and
`actions/checkout` without `ref:` checks out the default branch; the
trigger stays privileged. GitHub's default event policy for public repos
blocks `pull_request_target` (evaluate mode; enforcement for affected repos
announced for 2026-11-02): a reliability note, not a risk change.

### Scoring impact

- Read-only token + no inherited secrets = positive
- Write scopes, package publish, deployment, or `id-token: write` = elevated review depth
- `pull_request_target` with third-party mutable refs = reject pattern
- `workflow_call` + `secrets: inherit` into third-party workflow = reject unless fully pinned and tightly scoped
- Cache written by a job that processes untrusted input and restored by a release, publish, or `id-token: write` job = CRITICAL (cache poisoning → token theft)
- Release, publish, or `id-token: write` job restoring caches written only by trusted triggers = MEDIUM (Recommendation: drop the cache restore from that job, or restore only trusted-trigger keys)
- Low-trust trigger declaring write-capable `cache-mode` = HIGH
- PR-head checkout or fetch under a privileged trigger = HIGH; CRITICAL when the fetched code is executed (pwn request)
- Unpinned tool install in a job with secrets, write scopes, OIDC, or publish rights = HIGH (condition: pin the version and verify a checksum or signature); from a mutable non-vendor source (branch URL, gist, personal host) = CRITICAL

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

## Runtime & Pin Freshness

A SHA pin freezes the action and also freezes out later fixes. Dependabot
alerts do not fire for SHA-pinned actions (GitHub docs), so compare the
pinned release with the action's newer releases yourself.

| Finding | Rating |
|---|---|
| `runs.using: node24`, composite, or Docker | No finding |
| `runs.using: node20` | LOW. Node 20 is end-of-life; GitHub set its runner removal for 2026-09-23 and the runner runs node20 actions on Node 24 by default. Linux ARM32 self-hosted runners cannot run Node 24 |
| `runs.using: node16` / `node12` | MEDIUM: two or more runtime generations behind |
| `ACTIONS_ALLOW_USE_UNSECURE_NODE_VERSION=true` in workflow or runner env | MEDIUM: forces an end-of-life Node runtime |
| A newer release fixes a security issue in the pinned release (advisory or release notes) | Rate per `references/criteria.md` §4.3 for the pinned version; condition: update the pin |
| Privileged trigger (`pull_request_target`, `workflow_run`) with `actions/checkout` pinned to a release without the fork-checkout refusal (below v7.0.0, other than v4.4.0+, v5.1.0+, v6.1.0+) | MEDIUM. Recommendation: update the pin |
| Pinned release superseded, nothing security-relevant in between | LOW note; Recommendation names update automation (§4.6 V5) |

LOW notes here do not bar Tier 1.

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
- installs tools or images without a pinned version

A consuming-repo lockfile (`actions.lock`) records transitive action commits,
except dependencies inside reusable workflows; the lockfile of the repo that
defines the reusable workflow covers those.

## Tier Thresholds (CI Actions)

### Tier 1 — Quick Audit

Use only when ALL of these hold:
- Official `actions/*` or verified creator with consistent source identity
- Top-level ref pinned to a full commit SHA reachable from a branch or tag
  of the named repo
- No `pull_request_target`
- No inherited secrets into third-party code
- Minimal read-only permissions
- No risky transitive child refs visible from the current context
- `references/criteria.md` §4.6 raises nothing (§Version & Update Integrity
  below)

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
- PR-head checkout or fetch under a privileged trigger
- Low-trust trigger with write-capable `cache-mode`
- Release, publish, or `id-token: write` job that restores caches or installs
  unpinned tools

Deep audits must examine the first nested layer and continue one more layer
when the first child still carries privilege, mutability, or opacity.

## CVE Scope (§4.3)

- **Own code:** `action.yml`, the action's scripts and committed `dist/`
  bundle, its `Dockerfile`, and reusable-workflow YAML.
- **Third-party component:** npm dependencies bundled into `dist/`, a Docker
  action's base image and OS packages, tools the action downloads at run
  time. Nested `uses:` children are audited as transitive actions, not as
  components.
- **Sources:** GitHub Advisory Database / OSV ecosystem `GitHub Actions` for
  `<owner>/<repo>`, plus the repo's security advisories. SHA-pinned actions
  get no Dependabot alerts, so query the pinned version yourself.

## Version & Update Integrity (§4.6)

- **V1** Publish time: the GitHub release of the tag that points at the
  audited commit (`gh release view <tag> -R <owner>/<repo>` or the Releases
  page). Commit dates are set by the committer's client: fallback only, and
  say so in the row. Version unit: the commit the ref resolves to now; a
  moved tag, including a floating major such as `v4`, is a new version.
  Cooldown setting for conditions: Dependabot `cooldown` (version updates;
  GitHub documents a 3-day default) or Renovate `minimumReleaseAge`.
- **V2** Identity: the source repo (`<owner>/<repo>`; numeric owner and repo
  id in an `actions.lock` entry) and the commit's reachability from it;
  Marketplace verified creator (publisher identity only); immutable-release
  attestation (`gh release verify <tag> -R <owner>/<repo>`). Expected
  identity: the repo the Marketplace listing or vendor docs name. Actions are
  rarely signed, so absent signatures are not a flag. A SHA reachable only
  through a fork is not verified (unknown ref).
- **V3** Diff the audited commit against the prior release. HIGH: the tag
  moved after its release was published, or the commit differs from the
  user's version comment or lock entry; `action.yml` changes the changelog
  does not explain (`runs.using` type, new inputs that take tokens, new
  nested `uses:`, new runtime downloads); committed `dist/` that does not
  match source (Tier 3). Repo transfer, rename, or changed owner/repo id:
  HIGH when the job is privileged, else MEDIUM.
- **V4** Extra incident sources: GitHub Advisory Database (GitHub Actions),
  the action repo's security advisories, CI-security vendor write-ups. If an
  affected version ran: search the logs of runs in the exposure window for
  leaked secrets, then rotate every secret, token, and OIDC trust those jobs
  could reach.
- **V5** Triggers: tag retarget seen (lockfile relock error, version-comment
  mismatch) | repo transfer or archive | implementation type change | new
  required permissions or secrets. Update controls: full SHA with a version
  comment (`# v1.2.3`) kept current by Dependabot (`package-ecosystem:
  github-actions`) or Renovate with a cooldown; a consuming-repo lockfile
  (`gh actions-lock`, `gh actions-lock --verify` in CI; public preview); the
  policy "Require actions to be pinned to a full-length commit SHA".

## Static Analysis Helper (optional, Tier 2/3)

`zizmor` lints workflow and action YAML for the patterns above (audits such
as `dangerous-triggers`, `cache-poisoning`, `unpinned-uses`,
`unpinned-tools`, `impostor-commit`, `ref-version-mismatch`,
`secrets-inherit`, `excessive-permissions`); some audits query GitHub. It is
audit tooling: pin its version per the tooling note in
`references/criteria.md` and record it in the coverage row. Its findings
are evidence; rate them with this addendum.
