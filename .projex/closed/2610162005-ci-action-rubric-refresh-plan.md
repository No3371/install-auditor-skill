# ci-action Rubric Refresh

> **Status:** Complete
> **Completed:** 2026-10-16
> **Walkthrough:** 2610162005-ci-action-rubric-refresh-walkthrough.md
> **Author:** Claude (Opus)
> **Parent:** 2610161927-registry-package-and-ci-action-stewardship-review-eval.md
> **Source:** 2610161927-registry-package-and-ci-action-stewardship-review-eval.md (CI-1–CI-6, CI-8; EV-1 and EV-2 noted for the eval plan) | shared contract 2610161941-shared-version-integrity-floor-plan.md (§4.6 plug-ins, Hand-off row "ci-action")
> **Related Projex:** 2610161941-shared-version-integrity-floor-plan.md (contract; merged to base as `20843cc`) | 2610161852-dispatcher-rubric-consistency-walkthrough.md (Red Flag "Mutable CI ref with privileged access"; ci-action alignment kept) | 2604070218-install-auditor-subject-typed-redesign-nav.md | 2610162010-registry-package-rubric-refresh-plan.md (sibling; also edits `references/registries.md`, other sections) | later eval-refresh plan (see Notes → Eval hand-off)
> **Worktree:** Yes
> **Log:** 2610162005-ci-action-rubric-refresh-log.md

---

## Summary

The ci-action rubric's core rule, a full-SHA pin for privileged jobs, still holds. But it misses four things that changed in 2025–26: (1) the cache-poisoning → OIDC-token chain and tools installed outside `uses:`; (2) GitHub's immutable releases and workflow lockfiles, which give new immutable-ref evidence; (3) pin freshness, since a SHA pin does not receive later safety fixes such as the `actions/checkout` fork-checkout refusal, and Dependabot alerts skip SHA-pinned actions; (4) a concrete runtime check (`runs.using`). The plan also fills the ci-action plug-ins of the new shared floor (`references/criteria.md` §4.6 V1–V5, plus the §4.3 own-code line) and fixes the narrow CI rule in `references/registries.md`.

All product facts were checked against primary sources on 2026-10-16: GitHub docs (`github/docs` main, commit date 2026-10-16), `actions/checkout` tags and `action.yml`, `actions/runner` source, and `zizmorcore/zizmor` docs. Facts that could not be verified are left out or hedged (Notes → Facts).

**Scope:** `workflows/ci-action.md` | `references/criteria/ci-action.md` | `references/registries.md` §CI/CD only. No `SKILL.md`, `references/criteria.md`, evals, scripts or `STEWARDSHIP.md`.
**Estimated Changes:** 3 files, 32 exact string replacements (simulated on base `20843cc`: all anchors match once). Sizes: workflow 7,775 → 11,028 B; addendum 7,322 → 17,115 B; registries 4,413 → 4,681 B.

---

## Objective

### Problem / Gap / Need

| ID | Gap | Fix (step) |
|---|---|---|
| CI-1 | No model of cache trust: privileged/release jobs restoring caches that lower-trust code can write (the TanStack chain); every step in an `id-token: write` job can mint OIDC tokens; tools installed via `run:` / `container:` are unpinned; PR-head checkout patterns incl. `allow-unsafe-pr-checkout: true` aren't named | Trigger matrix rows + scoring (2f–2h); workflow Tier 3 / research / verdict notes (1c, 1f, 1h, 1k, 1m, 1n) |
| CI-2 | Ref matrix treats every tag as mutable; immutable releases (tag locked, release attestation) not modelled | Matrix row + check method (2c, 2d); V2 plug-in (2n) |
| CI-3 | Workflow lockfiles (`actions.lock`, public preview) and the SHA-pinning policy not recognised | Matrix row (2c); transitive note (2j); V5 update controls (2n) |
| CI-4 | APPROVED path never asks whether the pin is current. SHA pins miss backported safety fixes, and Dependabot alerts don't fire for them | §Runtime & Pin Freshness (2i); APPROVED shape names update control (1o, 1p) |
| CI-5 | "Action runtime / deprecation state" names no concrete check | `runs.using` table (2i); workflow §4.5 pointer (1l) |
| CI-6 | `pull_request_target` semantics (default-branch workflow + checkout) and the new public-repo default event policy are not noted | Note paragraph (2g); risk unchanged |
| CI-8 | No static-analysis helper named | §Static Analysis Helper (2n), optional and pinned per the criteria tooling note |
| — | Impostor commits: a SHA from the fork network passes as "full SHA" | Matrix row + reachability check (2c, 2d, 2e); Tier 1 bullet (2k, 1e) |
| Contract | ci-action has no `## Version & Update Integrity (§4.6)` plug-in and no §4.3 own-code line; both headers say "more specific ci-action guidance wins" with no §4.6 exception | Plug-ins (2n); header carve-outs (1a, 2a); Tier 1 bars (1e, 2l) |
| RP-6 (CI line) | `registries.md` rule ("`secrets.*` → SHA") is narrower than the Red Flag; its example hard-codes checkout v4.2.2's SHA under `@v4` (`v4` now points to v4.4.0); unverified row "Medium" vs addendum "Medium-Low" | 3a, 3b |

### Success Criteria

- [ ] `references/criteria/ci-action.md` has exactly one `## Version & Update Integrity (§4.6)` heading with 5 bullets `- **V1**` … `- **V5**`, one `## CVE Scope (§4.3)`, one `## Runtime & Pin Freshness`, and one `## Static Analysis Helper (optional, Tier 2/3)`.
- [ ] Both file headers carry the §4.6 exception: `grep -c "except for"` → 1 in `workflows/ci-action.md` and 1 in `references/criteria/ci-action.md`.
- [ ] Every `§4.6 V<n>` reference in the 3 files names V1–V5. Every `addendum §<Name>` reference in the workflow names an existing addendum heading.
- [ ] New strings are present: `allow-unsafe-pr-checkout` (workflow 3, addendum 1); `cache-mode` (workflow 3, addendum 4); `actions.lock` (workflow 1, addendum 4); `gh release verify` (workflow 1, addendum 2).
- [ ] `references/registries.md` no longer contains `11bd71901bbe5b1630ceea73d27597364c9af683` or `Any action that accesses`; it names `Mutable CI ref with privileged access`.
- [ ] `SKILL.md`'s Red Flag "Mutable CI ref with privileged access" is untouched (`git diff` shows no `SKILL.md` change).
- [ ] Byte sizes are within ± 150 B of the simulation (11,028 / 17,115 / 4,681). If the registry sibling plan has already changed `references/registries.md`, check its delta instead (+268 B).
- [ ] New wrapped prose lines in `workflows/ci-action.md` are ≤ 80 columns. The 4 pre-existing longer lines stay as they are.
- [ ] `python3 evals/run_evals.py validate` passes; `python3 -m unittest discover -s evals -p "test_*.py"` passes with the Preflight count.
- [ ] Paper traces T1–T11 (Verification Plan) give the stated verdicts, each hop cited by section.
- [ ] `git diff --stat <base>..HEAD` lists exactly the 3 files (+ projex docs).

### Out of Scope

- `SKILL.md`. No change is required: the Red Flag already covers impostor SHAs as "unknown ref", and its tag sentence defers to `workflows/ci-action.md`. Two possible wording follow-ups are listed in Notes → For the orchestrator; neither is needed for correctness.
- `references/criteria.md` (shared plan owns it; §4.6/§4.3 consumed as-is).
- `evals/` (EV-1, EV-2 and the new cases go to the eval-refresh plan: Notes → Eval hand-off). The live paid eval run happens once, after all refreshes (human decision).
- Non-GitHub Type 5 depth (GitLab CI/CD Catalog components, CircleCI orb tiers): not re-researched. The existing "map to closest equivalent, lower confidence" rule stays.
- `references/registries.md` sections other than §CI/CD (registry-package plan: RP-6 PyPI/Go rows) and `scripts/` (no CI tooling; RP-7 is registry-only).
- `STEWARDSHIP.md` review dates (orchestrator bookkeeping: ci-action Last Reviewed 2026-10-16, Next Due 2027-02-13).
- Incident-specific examples whose details are secondary-source only: TanStack counts, trivy-action tag counts, LiteLLM CircleCI. The rubric states the patterns, not the incidents.

---

## Context

### Current State

- `workflows/ci-action.md` (218 lines, 7,775 B): Identify / Evidence (Tier triage, Research) / Subject Rubric 4.1–4.6 / Verdict Notes. The line "the more specific ci-action guidance wins" has no §4.6 exception. Tier 1 makes no version-integrity check. §4.5 lists "Action runtime / deprecation state" with no method. Nothing on caches, tool installs, immutable releases, lockfiles or `allow-unsafe-pr-checkout`.
- `references/criteria/ci-action.md` (141 lines, 7,322 B): publisher table; Ref Immutability Matrix (5 rows, all tags mutable); Trigger & Secret Exposure Matrix (7 rows); implementation types; transitive guidance; tier thresholds. No §4.6 plug-in, no §4.3 own-code line.
- `references/registries.md` §CI/CD (L74–85): trust table plus "Critical rule: Any action that accesses `secrets.*` MUST be pinned…" with a hard-coded checkout SHA (that SHA is tag `v4.2.2`; `v4` now resolves to `v4.4.0`, `11d5960…`, verified by `git ls-remote`).
- `SKILL.md` (15,484 B; shared plan headroom 16 B): the Red Flag "Mutable CI ref with privileged access" auto-REJECTs a branch / default-branch / unknown ref, or any non-SHA ref from an unverified third-party publisher, in a privileged job. Its tag sentence reads: "Tag-pinned actions from official/verified publishers are HIGH → CONDITIONAL (pin to SHA) per `workflows/ci-action.md`." Precedence now names the §4.6 floor as never downgraded.
- `references/criteria.md` (base `20843cc`) has §4.6 V1–V5 with `**Addendum:**` lines, §4.3 Blocking CVE mapping with its own Addendum line, the "Audit tooling is itself a dependency" note, and the canonical `Version integrity (§4.6)` coverage row.

### Verified facts this plan codifies (primary sources, read 2026-10-16)

| Fact | Source |
|---|---|
| Low-trust triggers (anything except `push`, `workflow_dispatch`, `repository_dispatch`, `delete`, `registry_package`, `page_build`, `schedule`) get **read-only** default-branch cache; `cache-mode: write` / `write-only` overrides this and "reintroduces the risk of cache-poisoning"; caches are unsigned | `github/docs` content/actions/reference/workflows-and-actions/dependency-caching.md §Cache access for low-trust workflow triggers, §Controlling cache access with `cache-mode` |
| `pull_request_target` takes the workflow and default `actions/checkout` from the base repo's default branch; it has a default public-repo event policy that blocks it (evaluate mode; "On November 2, 2026, GitHub will enforce…" for affected repos); `allow-unsafe-pr-checkout: true` opts out of the checkout protection; `git fetch` / `gh pr checkout` / artifacts are not covered | `github/docs` content/actions/reference/security/securely-using-pull_request_target.md |
| `actions/checkout` v7.0.0 "Block checking out fork PR for pull_request_target and workflow_run"; input `allow-unsafe-pr-checkout` (default false); backport releases v4.4.0, v5.1.0, v6.1.0 (2026-07-16) carry the input; `v4`/`v5`/`v6` tags point to them; v4.2.2 = `11bd719…` (2024-10-23, `node20`) | `actions/checkout` CHANGELOG.md, `action.yml` at tags, `git ls-remote --tags` |
| Immutable releases: tag locked to commit and can't be deleted while the release exists; tag name never reusable; release attestation; `gh release verify RELEASE-TAG`; floating major/minor tags are plain moved tags by design | `github/docs` immutable-releases.md; using-immutable-releases-and-tags-to-manage-your-actions-releases.md; verify-release-integrity |
| Workflow lockfiles: `.github/workflows/actions.lock`, generated by `gh actions-lock` (`--verify`, `--relock`); records `commit` + `owner_id`/`repo_id`, checked at run time; covers transitive action deps **except** inside reusable workflows; "Require lockfile" policy; **public preview**; feature versioned for fpt + ghec (how-tos labelled Enterprise Cloud) | `github/docs` workflow-dependency-lockfiles.md; lock-workflow-dependencies.md; enforce-workflow-lockfiles.md; data/features/actions-workflow-lockfiles.yml |
| Policy name "Require actions to be pinned to a full-length commit SHA" (fpt, ghec, ghes ≥ 3.19); locked deps satisfy it | `github/docs` data/reusables/actions/lockfile-allowed-actions-sha.md; data/features/actions-blocklist-sha-pinning.yml |
| "Dependabot only creates alerts for vulnerable actions that use semantic versioning and will not create alerts for actions pinned to SHA values"; SHA selection: "verify it is from the action's repository and not a repository fork" | `github/docs` secure-use.md; data/reusables/actions/actions-pin-commit-sha.md |
| Dependabot `cooldown` (version updates only); 3-day default cooldown (feature on fpt/ghec) | `github/docs` dependabot-options-reference.md §cooldown; data/features/dependabot-cooldown-default-days.yml |
| Runner: node12/node16 actions → node20; node20 → Node 24 when the server-side Node 24 default flag is on; Node 20 removal date constant "September 23rd, 2026"; opt-out `ACTIONS_ALLOW_USE_UNSECURE_NODE_VERSION`; Linux ARM32 can't run Node 24 | `actions/runner` main (2026-10-16) src/Runner.Worker/Handlers/HandlerFactory.cs, src/Runner.Common/Constants.cs |
| zizmor (v1.31.1) audits incl. `dangerous-triggers`, `cache-poisoning`, `unpinned-uses`, `unpinned-tools`, `impostor-commit`, `ref-version-mismatch`, `secrets-inherit`, `excessive-permissions` | `zizmorcore/zizmor` docs/audits.md, tags |

### Key Files

| File | Role | Change Summary |
|---|---|---|
| `workflows/ci-action.md` | Type 5 workflow | §4.6 carve-out; context items; Tier 1/3 bullets; research Q2/Q9; GitHub checks; coverage rows; §4.4/§4.5 bullets; verdict notes |
| `references/criteria/ci-action.md` | Type 5 addendum | §4.6 carve-out; ref matrix (3 new rows + checks); trigger matrix (4 rows + notes + scoring); §Runtime & Pin Freshness; transitive lockfile note; tier bullets; §CVE Scope (§4.3); §Version & Update Integrity (§4.6); §Static Analysis Helper |
| `references/registries.md` | Registry trust guide | §CI/CD unverified row → Medium-Low; Critical rule aligned to the Red Flag, no hard-coded SHA |

### Dependencies

- **Requires:** base `claude/youthful-dijkstra-5ov1kt` at or after `20843cc` (shared §4.6 floor merged). Preflight verifies it.
- **Concurrent:** sibling refresh plans. Only 2610162010-registry-package-rubric-refresh-plan.md shares a file (`references/registries.md`, other sections). Anchors 3a/3b sit in §CI/CD, which that plan doesn't own. Whichever closes second rebases; no textual conflict is expected unless that plan rewrites the §CI/CD table.
- **Blocks:** eval-refresh plan (new ci-action cases assert on this text); the single live eval run.

### Constraints

- Addenda may only tighten §4.6 and fill its plug-ins (`SKILL.md` Precedence). No text here may make Tier 1 or APPROVED easier than §4.6 allows.
- Red Flags are never downgraded. Immutable-release tags and lockfile entries relax only the addendum's own HIGH tag finding. The `SKILL.md` Red Flag cases (branch/unknown ref; any non-SHA ref from an unverified publisher in a privileged job) stay REJECTED.
- Preview features (lockfiles) count as evidence or update controls. They are never required.
- `workflows/*.md` prose wraps at ~78 columns; addendum tables and scoring bullets use long lines (existing style).
- No projex filenames in shipped files.

### Assumptions

- **A1:** The anchors match once on the execution base. Simulated on `20843cc` (32/32). If the registry sibling closed first, 3a/3b may move. Re-check them with `grep -cF`.
- **A2:** Eval 14 stays APPROVED. Checkout `11bd719…` = v4.2.2, released 2024-10-23 (V1 ≥ 7 d); reachable as tag `v4.2.2` (V2); `node20` → LOW; superseded → LOW. LOW notes don't bar Tier 1 (2i). **Verify in T1.**
- **A3:** Eval 27 stays CONDITIONAL. `docker/build-push-action@v5` is a floating major (never immutable) → HIGH tag finding stands. `v5` → 2024-05-29 commit, `node20` (verified via `git ls-remote` + `action.yml`).
- **A4:** "Any step in an `id-token: write` job can request an OIDC token" (2g) rests on the runner exposing `ACTIONS_ID_TOKEN_REQUEST_URL` / `ACTIONS_ID_TOKEN_REQUEST_TOKEN` to the job's steps. This is pre-cutoff knowledge and was not re-read this session. **Verify early** in GitHub docs (`content/actions/reference/security/oidc.md` or the custom-action OIDC page). If it's wrong, scope the sentence to "any action step" and keep the rating.
- **A5:** The `gh release view <tag> -R <owner>/<repo>` and `gh release verify <tag> -R …` flag forms (global `-R`) are standard `gh` usage. The docs show `gh release verify RELEASE-TAG` run inside the repo.

### Impact Analysis

- **Direct:** the 3 files.
- **Adjacent:** `SKILL.md` Red Flag and Tree terms are consumed unchanged. The `references/criteria.md` §4.6 plug-in convention is now filled for ci-action.
- **Downstream:** live audits change in these cases:
  - cache restores in release/OIDC jobs → MEDIUM, or CRITICAL with a low-trust writer;
  - PR-head fetch under a privileged trigger → HIGH, or CRITICAL if the code runs;
  - unpinned tool installs in privileged jobs → HIGH, or CRITICAL from a mutable non-vendor source;
  - verified immutable-release exact tags from official/verified publishers → LOW note instead of HIGH;
  - lockfile-locked official/verified tags → MEDIUM instead of HIGH;
  - impostor SHAs → unknown ref;
  - SHA bumps < 72 h old → CONDITIONAL (shared V1);
  - `node20` → LOW, `node16`/`node12` → MEDIUM.

  Eval 39 still conflicts with the rubric (EV-1, unchanged by this plan).

---

## Implementation

### Overview

Preflight → Step 1 workflow (16 replacements) → Step 2 addendum (14) → Step 3 registries (2). Every change is an exact `old → new` pair; each old string occurs once on base (simulated), and no anchor overlaps another edit's output. Apply with the Edit tool in listed order. A miss means the base moved: re-read that region and re-anchor. Don't improvise wording.

**Preflight (`<work-root>`):**
```bash
git log --oneline -1 --grep "shared version and update integrity floor"   # expect 20843cc (or a descendant contains it)
grep -c "^## 4.6 Version & Update Integrity (shared floor)$" references/criteria.md   # 1
grep -c "^### V[1-5] " references/criteria.md                              # 5
grep -c "Addendum plug-ins" references/criteria.md                         # 1
grep -c "Audit tooling is itself a dependency" references/criteria.md      # 1
grep -c "Mutable CI ref with privileged access" SKILL.md                    # 1
grep -c "Confirmed supply chain compromise" SKILL.md                        # ≥ 1
wc -c workflows/ci-action.md references/criteria/ci-action.md references/registries.md   # 7775 / 7322 / 4413 (registries may differ if the registry plan closed first)
python3 evals/run_evals.py validate | head -3
python3 -m unittest discover -s evals -p "test_*.py" 2>&1 | tail -3        # record count
```
If any of the first 7 checks fails, stop: the shared contract is not on base. Then verify A4 (OIDC env exposure) and log the result.

---

### Step 1: `workflows/ci-action.md`

**Objective:** add the §4.6 carve-out and wire the new surfaces (cache/tool trust, PR-head fetch, ref integrity, runtime/freshness, version integrity) into Identify, Tier triage, Research, Rubric and Verdict Notes. Detail lives in the addendum; the workflow points to it.
**Confidence:** High
**Depends on:** Preflight
**Do-Projex:** Encouraged

**Files:** `workflows/ci-action.md`

**Changes:** 16 exact replacements (1a–1p). Simulated result 11,028 B.

```markdown
// 1a Before:
scoring. When it conflicts with the shared rubric, the more specific
ci-action guidance wins.
// 1a After:
scoring. When it conflicts with the shared rubric, the more specific
ci-action guidance wins, except for the version-integrity floor in
`references/criteria.md` §4.6, which the addendum may only tighten
(`SKILL.md` Tree terms → Precedence).

// 1b Before:
- Ref type: full SHA | tag | branch | unknown
// 1b After:
- Ref type: full SHA | immutable-release tag | tag | branch | unknown

// 1c Before:
  explicit secrets, forked PR involvement, artifact inputs, checkout/build of
  untrusted code
// 1c After:
  explicit secrets, forked PR involvement, artifact inputs, checkout/build of
  untrusted code, cache use (`actions/cache`, setup-action `cache:` inputs,
  `cache-mode`), tools installed outside `uses:`
- Pin controls in the consuming repo: `.github/workflows/actions.lock` entry,
  SHA-pinning or lockfile policy, Dependabot or Renovate for actions

// 1d Before:
5. Whether the workflow checks out, builds, or executes untrusted external code
// 1d After:
5. Whether the workflow checks out, builds, or executes untrusted external
   code, restores caches, or installs tools outside `uses:`

// 1e Before:
- No risky transitive child visible from the current context

Quick audit scope: confirm publisher identity, SHA pinning, permission
scope, trigger safety, and any obvious nested `uses:` refs. If those stay
clean, proceed to Subject Verdict Notes without deeper recursion.
// 1e After:
- No risky transitive child visible from the current context
- `references/criteria.md` §4.6 raises nothing (addendum §Version & Update
  Integrity)

Quick audit scope: confirm publisher identity, SHA pinning (the SHA is
reachable from a branch or tag of the named repo), permission scope,
trigger safety, version integrity (release date of the pinned commit), and
any obvious nested `uses:` refs. If those stay clean, proceed to Subject
Verdict Notes without deeper recursion.

// 1f Before:
- Opaque or mutable transitive child

Deep scope:
// 1f After:
- Opaque or mutable transitive child
- `allow-unsafe-pr-checkout: true`, or a PR head checked out or fetched in a
  `pull_request_target`, `workflow_run`, or `issue_comment` job
- Low-trust trigger declaring `cache-mode: write` or `write-only`
- Release, publish, or `id-token: write` job that restores caches or
  installs tools outside `uses:`

Deep scope:

// 1g Before:
2. Is the ref immutable?
// 1g After:
2. Is the ref immutable (full SHA reachable from the named repo, verified
   immutable release, or lockfile entry), and is the pinned release current
   (no missed safety fix, supported runtime)?

// 1h Before:
   provenance warnings?
// 1h After:
   provenance warnings?
9. Can lower-trust code reach this job through caches, artifacts, or tools
   installed outside `uses:`?

// 1i Before:
- Self-hosted runner note when present

### Audit coverage tracking
// 1i After:
- Self-hosted runner note when present
- Ref integrity: SHA reachable from the named repo, not only from a fork;
  immutable release via `gh release verify <tag> -R <owner>/<repo>`;
  lockfile entry or pinning policy in the consuming repo
- Cache trust: who writes the caches a privileged or release job restores;
  `cache-mode` on low-trust triggers
- `allow-unsafe-pr-checkout` and other PR-head checkout or fetch patterns
- `runs.using` runtime and pin freshness (addendum §Runtime & Pin Freshness)
- Optional static analysis (addendum §Static Analysis Helper)

### Audit coverage tracking

// 1j Before:
- Runner context review
// 1j After:
- Runner context review
- Cache / artifact / tool-install trust review
- Version integrity (§4.6): release date, SHA reachability, continuity,
  compromise scope

// 1k Before:
- OIDC, package publish, deployment, or repo-write scopes
// 1k After:
- OIDC, package publish, deployment, or repo-write scopes
- Cache trust: caches restored in privileged or release jobs, and who can
  write them
- Tools installed outside `uses:` (`run:` downloads, package installs,
  `container:` / `services:` images)

// 1l Before:
- SHA pin quality vs mutable-tag drift risk
- Reusable workflow compatibility assumptions
- Action runtime / deprecation state
// 1l After:
- SHA pin quality vs mutable-tag drift risk, and pin freshness: a SHA pin
  does not receive later fixes (addendum §Runtime & Pin Freshness)
- Reusable workflow compatibility assumptions
- Action runtime / deprecation state: the `runs.using` value in `action.yml`
  (addendum §Runtime & Pin Freshness)

// 1m Before:
- Self-hosted runner plus untrusted external code path

Toward CONDITIONAL:
// 1m After:
- Self-hosted runner plus untrusted external code path
- Fork PR code checked out or fetched in a `pull_request_target`,
  `workflow_run`, or `issue_comment` job and then executed (pwn request),
  including via `allow-unsafe-pr-checkout: true`
- Cache written by a job that processes untrusted input, then restored by a
  release, publish, or `id-token: write` job
- Download-and-execute from a mutable non-vendor source (branch URL, gist,
  personal host) in a job with secrets, write scopes, OIDC, or publish rights

Toward CONDITIONAL:

// 1n Before:
- Clean top-level action with one moderate-risk child that can be SHA pinned
// 1n After:
- Clean top-level action with one moderate-risk child that can be SHA pinned
- Release, publish, or `id-token: write` job that restores caches written
  only by trusted triggers, or installs a tool without a pinned version

// 1o Before:
- Full SHA pin for the top-level subject and visible transitive children
// 1o After:
- Full SHA pin (reachable from the named repo) for the top-level subject and
  visible transitive children; a verified immutable-release tag or matching
  lockfile entry counts per the addendum Ref Immutability Matrix

// 1p Before:
- No negative incident history found
// 1p After:
- No negative incident history found, or only a resolved past compromise
  outside the pinned version (`references/criteria.md` §4.6 V4 case c)
- Recommendation names how the pin is kept current (§4.6 V5 update control)
```

**Rationale:**
- **1a.** Without it, "more specific ci-action guidance wins" could be read as overriding §4.6. It mirrors `SKILL.md` Precedence.
- **1e.** Tier 1 now names the §4.6 bar and SHA reachability. That is the impostor-commit gap: GitHub docs tell users to verify the SHA "is from the action's repository and not a repository fork".
- **1f / 1m / 1n.** These carry CI-1 into tiering and verdict notes. Ratings live in addendum 2h, so the two files can't drift.
- **1o / 1p.** The APPROVED shape adds update control as a Recommendation item, not a gate. A gate would flip eval 14. A resolved past compromise stays APPROVED-reachable per §4.6 V4 case c (LOW flag; Tier 1 barred by §4.6 itself).

**Verification:** `grep -c "except for" workflows/ci-action.md` → 1; `grep -c "allow-unsafe-pr-checkout" workflows/ci-action.md` → 3; `grep -c "cache-mode" workflows/ci-action.md` → 3; `grep -c "§4.6" workflows/ci-action.md` → 5; `wc -c` ≈ 11,028; `awk 'length>80 && !/^\|/' workflows/ci-action.md` lists only the 4 pre-existing lines (Publisher identity, Q6, `workflow_call` REJECTED bullet, Verified-creator CONDITIONAL bullet).

**If this fails:** `git -C <work-root> checkout -- workflows/ci-action.md` and reapply.

---

### Step 2: `references/criteria/ci-action.md`

**Objective:** encode CI-1–CI-6/CI-8 ratings and fill the §4.6 and §4.3 plug-ins.
**Confidence:** High for the mechanisms (primary-sourced). Medium for the rating choices (policy, see Rationale).
**Depends on:** Preflight (Step 1 references the headings created here; apply both before verifying either)
**Verify-Projex:** Encouraged (ratings interact with `SKILL.md` Red Flags and eval 14/27)

**Files:** `references/criteria/ci-action.md`

**Changes:** 14 exact replacements (2a–2n). Simulated result 17,115 B.

```markdown
// 2a Before:
When guidance here conflicts with the shared rubric, the more specific
ci-action guidance wins.
// 2a After:
When guidance here conflicts with the shared rubric, the more specific
ci-action guidance wins, except for §4.6 (version & update integrity): this
file only tightens it or fills its plug-ins (`SKILL.md` Tree terms →
Precedence).

// 2b Before:
- Verified creator badge = moderate positive, not sufficient on its own
// 2b After:
- Verified creator badge = moderate positive for publisher identity, not
  code (`references/criteria.md` §4.6 V2); not sufficient on its own

// 2c Before:
| Full commit SHA | Immutable | Required for Tier 1 and for any secret-bearing third-party action path |
| Release tag (`v4`, `v1.2.3`) | Mutable | CONDITIONAL from official/verified publishers (condition: pin to SHA); reject when the publisher is unverified and the job holds secrets, write perms, OIDC, or publish rights, or on untrusted code paths |
// 2c After:
| Full commit SHA, reachable from a branch or tag of the named repo | Immutable | Required for Tier 1 and for any secret-bearing third-party action path |
| Full commit SHA reachable only through a fork (impostor commit) | Not the publisher's code | Treat as an unknown ref |
| Exact-version tag (`v1.2.3`) of a verified immutable release | Immutable while the release exists; the tag name is never reused | An immutable ref, not a mutable tag: LOW note (prefer the SHA). Official/verified publisher: no pin condition. Tier 1 still needs a full SHA. Unverified publisher in a privileged job: still a non-SHA ref (`SKILL.md` Red Flag) |
| Release tag (`v4`, `v1.2.3`) | Mutable | CONDITIONAL from official/verified publishers (condition: pin to SHA); reject when the publisher is unverified and the job holds secrets, write perms, OIDC, or publish rights, or on untrusted code paths |
| Tag locked in the consuming repo's `.github/workflows/actions.lock` (public preview) | The locked commit runs; repo identity is checked at run time | Official/verified publisher, lock entry `commit` = the audited commit → MEDIUM instead of HIGH, no pin condition. Red Flag cases and Tier 1 unchanged: the workflow file still names a mutable ref |

// 2d Before:
| Unknown / omitted | Unknown | Treat as mutable until proven otherwise |

### Scoring impact
// 2d After:
| Unknown / omitted | Unknown | Treat as mutable until proven otherwise |

- **Check immutability:** `gh release verify <tag> -R <owner>/<repo>` passes,
  or the release page shows **Immutable**. A floating major tag (`v4`) is a
  plain tag the publisher moves by design; it is never an immutable release.
- **Check reachability:** the SHA is a tag target or on a branch of the named
  repo (`git ls-remote https://github.com/<owner>/<repo>`; the commit page
  shows no "does not belong to any branch" warning). GitHub serves commits
  from the whole fork network under the parent repo's name.

### Scoring impact

// 2e Before:
- Branch or floating ref = strong negative
// 2e After:
- Branch or floating ref = strong negative
- SHA reachable only through a fork = unknown ref (CRITICAL in a privileged
  job via the `SKILL.md` Red Flag)

// 2f Before:
| Self-hosted runner + untrusted input | High | Host exposure is materially worse than GitHub-hosted runners |
// 2f After:
| Self-hosted runner + untrusted input | High | Host exposure is materially worse than GitHub-hosted runners |
| Low-trust trigger (`pull_request_target`, `issue_comment`, `workflow_run`) declaring `cache-mode: write` or `write-only` | High | GitHub gives these triggers read-only access to the default-branch cache; the override lets untrusted input poison caches that privileged workflows restore |
| Release, publish, or deploy job (`id-token: write`, publish token) that restores caches | Medium-High | Caches are unsigned. Confirm only trusted triggers (`push`, `schedule`, `workflow_dispatch`, …) write those keys |
| PR head checked out or fetched under `pull_request_target` / `workflow_run` / `issue_comment` (`allow-unsafe-pr-checkout: true`, `ref:` set to the PR head, `repository:` set to the fork, `gh pr checkout`, `git fetch` of PR refs) | High | `actions/checkout` v7.0.0+ (backports: v4.4.0, v5.1.0, v6.1.0) refuses fork PR checkout under `pull_request_target` / `workflow_run` unless `allow-unsafe-pr-checkout` is set; other fetch paths are not covered |
| Tools installed outside `uses:` (`run:` downloads piped to a shell, unversioned `pip` / `npm` / `apt` / `go install …@latest`, `container:` / `services:` images by tag) | Medium | Same drift risk as a mutable action ref; rated by job privilege below |

// 2g Before:
- Artifact download / reuse from lower-trust workflows
// 2g After:
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

// 2h Before:
- `workflow_call` + `secrets: inherit` into third-party workflow = reject unless fully pinned and tightly scoped
// 2h After:
- `workflow_call` + `secrets: inherit` into third-party workflow = reject unless fully pinned and tightly scoped
- Cache written by a job that processes untrusted input and restored by a release, publish, or `id-token: write` job = CRITICAL (cache poisoning → token theft)
- Release, publish, or `id-token: write` job restoring caches written only by trusted triggers = MEDIUM (Recommendation: drop the cache restore from that job, or restore only trusted-trigger keys)
- Low-trust trigger declaring write-capable `cache-mode` = HIGH
- PR-head checkout or fetch under a privileged trigger = HIGH; CRITICAL when the fetched code is executed (pwn request)
- Unpinned tool install in a job with secrets, write scopes, OIDC, or publish rights = HIGH (condition: pin the version and verify a checksum or signature); from a mutable non-vendor source (branch URL, gist, personal host) = CRITICAL

// 2i Before:
- Docker action with download-and-execute patterns or privileged assumptions = strong negative

## Transitive Action Audit Guidance
// 2i After:
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

// 2j Before:
- downloads remote code or containers at runtime
// 2j After:
- downloads remote code or containers at runtime
- installs tools or images without a pinned version

A consuming-repo lockfile (`actions.lock`) records transitive action commits,
except dependencies inside reusable workflows; the lockfile of the repo that
defines the reusable workflow covers those.

// 2k Before:
- Top-level ref pinned to a full commit SHA
// 2k After:
- Top-level ref pinned to a full commit SHA reachable from a branch or tag
  of the named repo

// 2l Before:
- No risky transitive child refs visible from the current context
// 2l After:
- No risky transitive child refs visible from the current context
- `references/criteria.md` §4.6 raises nothing (§Version & Update Integrity
  below)

// 2m Before:
- Docker or composite action running download-and-execute patterns
// 2m After:
- Docker or composite action running download-and-execute patterns
- PR-head checkout or fetch under a privileged trigger
- Low-trust trigger with write-capable `cache-mode`
- Release, publish, or `id-token: write` job that restores caches or installs
  unpinned tools

// 2n Before:
Deep audits must examine the first nested layer and continue one more layer
when the first child still carries privilege, mutability, or opacity.
// 2n After:
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
```

**Rationale:**
- **Immutable-release tag = immutable ref (2c).** Docs: the tag "cannot be changed, and cannot be deleted while the release exists", and the name is never reusable. So an exact-version immutable tag carries the same code guarantee as a SHA. A LOW note (not "no finding") keeps "prefer the SHA" and keeps Tier 1 SHA-only (simple, and consistent with eval 14). It is not a "tag-pinned" mutable ref in the sense of the `SKILL.md` sentence (the Red Flag is titled *Mutable* CI ref). Unverified publishers stay under the Red Flag's literal "any non-SHA ref" clause: Red Flags are never downgraded.
- **Lockfile = MEDIUM, not "no finding" (2c).** Docs say a lockfile "supersedes SHA pinning", but it is in public preview, and the workflow file still names a mutable ref that a `--relock` can move. MEDIUM drops the HIGH while keeping a visible note; the Red Flag cases are unchanged.
- **Cache chain ratings (2f, 2h).**
  - CRITICAL only when an untrusted-input writer meets a release/publish/OIDC reader. That is the chain that produced token theft.
  - A restore from trusted-trigger caches is MEDIUM: caches are unsigned (docs), but GitHub's default read-only rule already blocks the low-trust write path.
  - A write-capable `cache-mode` on a low-trust trigger is HIGH on its own: it is the documented bypass.
- **Tool installs (2f, 2h).** These mirror the Red Flag's mutable-ref logic: a mutable non-vendor source in a privileged job = CRITICAL; an unpinned vendor package = HIGH with a pin+checksum condition.
- **Runtime (2i).**
  - `node20` is LOW, not MEDIUM: the runner upgrades it to Node 24 by default (runner source), so it runs; it only signals staleness. ARM32 self-hosted is the exception and is named.
  - `node16`/`node12` → MEDIUM: two or more generations behind.
  - This keeps eval 14 (checkout v4.2.2 is `node20`) at APPROVED.
- **Checkout freshness (2i).** The backport versions are verified from tags and `action.yml`, so the rule is concrete. It is MEDIUM, not HIGH, because an actually executed PR-head checkout is caught separately (HIGH/CRITICAL in 2h).
- **V1 (2n).** Commit dates are client-set, so the release date is the primary source. "Moved tag = new version" makes floating majors re-auditable under V5.
- **V2 (2n).** Absence is not a flag: actions are rarely signed, and a flag would push nearly every action off Tier 1.
- **§4.3 line (2n).** Nested `uses:` stay with transitive guidance (existing structure), not as CVE "components". That way the Blocking-CVE own-code rule only covers code the publisher ships.
- **zizmor (2n).** Optional, and pinned per the shared tooling note, because the helper is itself third-party tooling.

**Verification:**
```bash
grep -c "^## Version & Update Integrity (§4.6)$" references/criteria/ci-action.md   # 1
grep -c "^- \*\*V[1-5]\*\* " references/criteria/ci-action.md                       # 5
grep -c "^## CVE Scope (§4.3)$\|^## Runtime & Pin Freshness$\|^## Static Analysis Helper" references/criteria/ci-action.md   # 3
grep -c "except for §4.6" references/criteria/ci-action.md                         # 1
grep -c "cache-mode" references/criteria/ci-action.md                              # 4
grep -c "actions.lock" references/criteria/ci-action.md                            # 4
wc -c references/criteria/ci-action.md                                             # ≈ 17115
```

**If this fails:** `git -C <work-root> checkout -- references/criteria/ci-action.md` and reapply.

---

### Step 3: `references/registries.md` §CI/CD

**Objective:** align the CI trust row with the addendum and the Critical rule with the Red Flag; drop the stale hard-coded SHA.
**Confidence:** High
**Depends on:** Steps 1–2 (the rule points to them)
**Do-Projex:** Encouraged

**Files:** `references/registries.md`

**Changes:** 2 exact replacements.

```markdown
// 3a Before:
| GitHub Actions marketplace (unverified) | Medium — pin to SHA |
// 3a After:
| GitHub Actions marketplace (unverified) | Medium-Low — pin to SHA |

// 3b Before:
**Critical rule for GitHub Actions:** Any action that accesses `secrets.*` MUST be pinned to a commit SHA, not a tag. Tags can be moved. Example: `uses: actions/checkout@v4` → should be `uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683`.
// 3b After:
**Critical rule for GitHub Actions:** pin any action or reusable workflow that runs in a job holding secrets, a write-scoped token, `id-token: write`, or publish rights to a full commit SHA from the action's own repo (not a fork); tags and branches can be moved. Format: `uses: <owner>/<action>@<40-char SHA> # v<x.y.z>`. Ratings, immutable releases and lockfiles: `workflows/ci-action.md` and `references/criteria/ci-action.md`. The auto-REJECT case is the `SKILL.md` Red Flag "Mutable CI ref with privileged access".
```

**Rationale:** RP-6 found the old rule narrower than the Red Flag (it covered only `secrets.*`, not write token, `id-token: write` or publish rights). The example SHA is release v4.2.2, while `@v4` now resolves elsewhere, so any hard-coded SHA goes stale. A placeholder format with a version comment also matches what Dependabot maintains (docs: it updates same-line version comments).

**Verification:** `grep -c "11bd71901bbe5b1630ceea73d27597364c9af683\|Any action that accesses" references/registries.md` → 0; `grep -c "Mutable CI ref with privileged access" references/registries.md` → 1; `grep -c "Medium-Low — pin to SHA" references/registries.md` → 1.

**If this fails:** `git -C <work-root> checkout -- references/registries.md`. If the registry sibling plan rewrote §CI/CD first, re-anchor on its text, keep its wording elsewhere and apply only the two semantic changes.

---

## Verification Plan

### Automated Checks

- [ ] `python3 evals/run_evals.py validate` passes; unittest count = Preflight.
- [ ] Consistency script (run from `<work-root>`, not committed):
```bash
python3 - <<'EOF'
import re, pathlib
W = pathlib.Path("workflows/ci-action.md").read_text(encoding="utf-8")
A = pathlib.Path("references/criteria/ci-action.md").read_text(encoding="utf-8")
R = pathlib.Path("references/registries.md").read_text(encoding="utf-8")
C = pathlib.Path("references/criteria.md").read_text(encoding="utf-8")
S = pathlib.Path("SKILL.md").read_text(encoding="utf-8")
heads = set(re.findall(r"^### (V[1-5]) ", C, re.M)); assert heads == {"V1","V2","V3","V4","V5"}
for name, t in [("W", W), ("A", A), ("R", R)]:
    for v in re.findall(r"§4\.6 (V\d)", t): assert v in heads, (name, v)
ah = re.findall(r"^## (.+)$", A, re.M)
for ref in re.findall(r"addendum §([A-Z][A-Za-z &]+?)(?:[),.\n]| Integrity)", W):
    assert any(h.startswith(ref.strip()) for h in ah), ref
assert A.count("## Version & Update Integrity (§4.6)") == 1
assert len(re.findall(r"^- \*\*V[1-5]\*\* ", A, re.M)) == 5
assert "except for" in W and "except for §4.6" in A
assert "11bd71901bbe5b1630ceea73d27597364c9af683" not in R and "Mutable CI ref with privileged access" in R
assert "Mutable CI ref with privileged access" in S
for s in ["allow-unsafe-pr-checkout", "cache-mode", "actions.lock", "gh release verify", "runs.using: node20"]:
    assert s in A, s
print("OK")
EOF
```
- [ ] `git -C <work-root> diff --stat <base>..HEAD` lists exactly the 3 files plus projex docs.

### Manual Verification (paper traces)

Walk each trace through `SKILL.md` Step N, `references/criteria.md` §4.6 and the edited files. Log the cited rule for each hop.

| # | Case | Expected |
|---|---|---|
| T1 | eval 14: `actions/checkout@11bd719…` on `pull_request`, `contents: read` | Tier 1: official, SHA reachable (tag v4.2.2), §4.6 V1 2024-10-23 ≥ 7 d, V2 repo matches, no V3/V4. `node20` LOW, superseded LOW (don't bar Tier 1) → **APPROVED**; Recommendation names Dependabot/Renovate update control |
| T2 | eval 15: `pull_request_target`, `secrets: inherit`, `contents: write`, `vendor/…@v2` → child `third-party/build-action@main` | Red Flag (branch ref, privileged) → **REJECTED**; Tier 3 |
| T3 | eval 27: `docker/build-push-action@v5`, `packages: write` | Floating major, never immutable → HIGH tag finding → **CONDITIONAL** (pin to SHA); `node20` LOW; superseded by v6/v7 LOW |
| T4 | Release workflow (`id-token: write`) restores pnpm cache; a `pull_request_target` workflow in the repo declares `cache-mode: write` and builds fork code | 2h: untrusted-input writer + OIDC reader = CRITICAL → **REJECTED** (TanStack shape) |
| T5 | Same release job, caches written only by `push` CI; everything else clean | MEDIUM (Recommendation: drop restore / trusted keys only) → APPROVED reachable (single MEDIUM); Tier 2+ |
| T6 | `pull_request_target` job with secrets: checkout `allow-unsafe-pr-checkout: true` + `ref: head.sha`, then `make test` | PR-head fetch executed = CRITICAL → **REJECTED** |
| T7 | Verified publisher, `owner/act@v2.3.1`, `gh release verify v2.3.1 -R owner/act` passes, job has `packages: write` | Immutable ref → LOW note, no pin condition; Tier 3 (write scope) → **APPROVED** reachable. Same shape from an **unverified** publisher → non-SHA ref in privileged job → Red Flag → **REJECTED** |
| T8 | `owner/act@<sha>` where the SHA exists only in a fork; job holds secrets | Unknown ref (2c/2e) → Red Flag → **REJECTED** |
| T9 | Dependabot bumped the SHA to a release published 20 h ago | §4.6 V1 `fresh version` HIGH → **CONDITIONAL** (keep the previous SHA or wait 72 h; cite Dependabot `cooldown`); no escalation for this flag alone |
| T10 | `id-token: write` job: `curl https://raw.githubusercontent.com/x/y/main/install.sh \| bash` / separately `pip install trivy` (unversioned) | Mutable non-vendor source = CRITICAL → **REJECTED** / vendor package unpinned = HIGH → **CONDITIONAL** (pin + checksum) |
| T11 | tj-actions-shape action: past tag-retarget compromise, resolved (bad commits gone, advisory published), user pins a post-fix SHA | §4.6 V4 case c LOW `past compromise`; Tier 1 barred → Tier 2 → **APPROVED** reachable; V5 triggers listed |

### Acceptance Criteria Validation

| Criterion | How to Verify | Expected Result |
|---|---|---|
| Plug-ins + new sections | Step 2 greps; consistency script | 1 / 5 / 3; `OK` |
| §4.6 carve-outs | greps | 1 + 1 |
| References resolve | consistency script | `OK` |
| registries aligned | Step 3 greps | 0 / 1 / 1 |
| SKILL.md untouched | `git diff --stat` | not listed |
| Sizes | `wc -c` | ± 150 B of simulation |
| Harness green | validate + unittest | pass; same count |
| Traces | execution log T1–T11 | match table |

---

## Rollback Plan

1. Before close: `projex-abandon.sh <repo-root> claude/youthful-dijkstra-5ov1kt projex/2610162005-ci-action-rubric-refresh --worktree`. Base is untouched.
2. After squash-close: `git -C <repo-root> revert <squash-sha>`. That is a single commit touching 3 files. If the registry plan has since edited `references/registries.md`, resolve that hunk by hand.

---

## Notes

### Facts: verified vs not

- **Verified (primary):** see Context → Verified facts.
- **Corrected vs the review:**
  - Lockfiles are feature-versioned for github.com and GHEC, not "GHEC only". The how-tos are labelled Enterprise Cloud, so the plan states "public preview" without a plan tier.
  - The checkout backport shipped as new minor releases (v4.4.0 / v5.1.0 / v6.1.0) that the floating majors point to. Exact-version and SHA pins to *those* releases do get the fix.
  - The fork-scoped cache question (review Open Question) is resolved: low-trust triggers get read-only default-branch cache unless `cache-mode` overrides it.
- **Not verified, so kept out of shipped text:** release dates of immutable releases (GA 2025-10-28) and the SHA-pinning policy (Aug 2025); the `pull_request_target` change date (2025-12-08); TanStack / trivy-action / LiteLLM incident details; whether trivy-action `v0.35.0` is immutable; whether Node 20 has actually been removed (only the scheduled date from runner source is used).
- **Pre-cutoff, not re-read:** A4 (OIDC request env vars visible to all steps); Renovate `minimumReleaseAge`; the GitHub commit-page "does not belong to any branch" warning; GHSA/OSV ecosystem name `GitHub Actions`; `gh` global `-R` flag. All are long-standing, but execution should spot-check A4.

### For the orchestrator (no edit needed now)

- `SKILL.md` Red Flag tag sentence: "Tag-pinned actions from official/verified publishers are HIGH → CONDITIONAL (pin to SHA) per `workflows/ci-action.md`". The addendum now rates verified immutable-release tags LOW and lockfile-locked tags MEDIUM. The sentence defers to the workflow, and the Red Flag is titled "Mutable", so there is no contradiction in effect. A future `SKILL.md` pass could add "mutable" before "Tag-pinned" (+8 B, over the 16 B headroom only if combined with other changes).
- The same Red Flag's "any non-SHA ref from an unverified third-party publisher" still rejects immutable-release tags and lockfile entries from unverified publishers. This is deliberately left conservative.

### Eval hand-off (for the eval-refresh plan; `evals/` not edited here)

- **EV-1:** eval 39 (`docker/build-push-action`, no ref/permissions, expected `@v5`) expects exact `APPROVED`. The rubric gives CONDITIONAL for the `@v5` tag, and this plan doesn't change that. Fix: `verdict_check [APPROVED, CONDITIONAL]` or put a SHA in the prompt. Note `v5` is two majors behind (v7.4.0 current) and `node20` → extra LOW notes.
- Evals 14 / 15 / 27: no assertion change expected (T1–T3). Eval 14's SHA is checkout v4.2.2 (`node20`, superseded): its APPROVED now relies on "LOW notes don't bar Tier 1".
- **New cases (EV-2):**
  - cache-poisoning chain (T4) → REJECTED;
  - trusted-only cache restore in release job (T5) → APPROVED/CONDITIONAL;
  - `allow-unsafe-pr-checkout` + execution (T6) → REJECTED;
  - verified immutable-release tag (T7) → APPROVED/CONDITIONAL, plus its unverified twin → REJECTED;
  - impostor SHA (T8) → REJECTED;
  - fresh SHA bump (T9) → CONDITIONAL;
  - `curl | bash` in an OIDC job (T10) → REJECTED;
  - `node16` action → MEDIUM note;
  - lockfile-locked official tag → not REJECTED.

  Tag all with `"workflow": "ci-action"`.

### Risks

- **Rubric bloat.** The addendum grows +9.8 KB (~2.5k tokens) and is read on every ci-action audit. Mitigation: ratings sit in tables and scoring bullets; the workflow only points to them. Combined size (28 KB) stays below registry-package (40 KB) and container-image (37 KB).
- **Preview drift (lockfiles, default `pull_request_target` policy, `cache-mode`).** Mitigation: phrased as evidence or notes; nothing requires them; dates are cited as announced.
- **Rating policy is a judgment call** (immutable LOW, lockfile MEDIUM, cache MEDIUM/CRITICAL). Mitigation: each is one table cell or bullet; T4–T8 exercise them.
- **Concurrent registries.md edit.** Mitigation: anchors are confined to §CI/CD; Step 3 fallback.
- **Auditor can't run `gh` / `git ls-remote` (offline/no auth).** Mitigation: every check also names a web-page equivalent (Releases page "Immutable" label, commit-page warning). Otherwise the existing `Not available` coverage path applies.

### Open Questions

None blocking. A4 is verified in Preflight with a fallback wording.

### Split Decision

`No split — single scope, within size budget`. One `.projex/` scope; 3 steps. The plan is ~55 KB / ~750 lines because it carries all 32 before/after pairs verbatim, but the size heuristic also needs > 5 steps, so it is not tripped. Steps 1–2 cross-reference each other's headings, and Step 3 points to both.
