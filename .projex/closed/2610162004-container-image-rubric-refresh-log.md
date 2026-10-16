# Execution Log: Container-Image Rubric Refresh

> **Status:** Complete
> **Started:** 20261016 20:10
> **Repo Root:** /home/user/install-auditor-skill
> **Plan File:** .projex/2610162004-container-image-rubric-refresh-plan.md
> **Parent:** 2610162004-container-image-rubric-refresh-plan.md
> **Base Branch:** claude/youthful-dijkstra-5ov1kt
> **Worktree Path:** .projexwt/2610162004-container-image-rubric-refresh

## Pre-Check Results

```
REPO_ROOT=/home/user/install-auditor-skill
BRANCH=claude/youthful-dijkstra-5ov1kt
PLAN_REL=.projex/2610162004-container-image-rubric-refresh-plan.md

PASS  Plan is committed (376ba86 projex: add plans - container-image + cli-binary rubric refresh)
WARN  Working tree has 4 uncommitted change(s)
PRE-CHECK PASSED
```

WARN resolution: the 4 uncommitted items are untracked sibling plan files (ide-plugin, desktop-app, agent-extension, registry-package) owned by other orchestrations. Not part of this plan; left untouched. The base-branch plan status commit (17fa9b1) staged only this plan's file.

## Steps

### [20261016 20:10] - Setup: start commit, worktree, bootstrap
**Action:** Plan status Ready -> In Progress committed on base (17fa9b1). Worktree created at `.projexwt/2610162004-container-image-rubric-refresh` (branch `projex/2610162004-container-image-rubric-refresh`, from 17fa9b1). Bootstrap: none needed (stdlib-only Python; no gitignored deps).
**Result:** Main checkout remains on base. No task/todo tool in this environment; steps tracked via this log.
**Status:** Success

### [20261016 20:11] - Preflight
**Action:** Ran the plan's Preflight in the worktree. Base is now 17fa9b1 (plan assumed 242310a; base advanced with sibling plans/start commits).
**Result:**
- `grep -c` shared-floor anchors: `## 4.6 ... (shared floor)` 1 | `**Curated pipelines:**` 1 | `**Addendum:**` 6 | "Audit tooling is itself a dependency" 1 | `| Version integrity (§4.6) |` 1 | `Blocking CVE` in SKILL.md 1 (>= 1). All pass.
- `git diff --stat 97f6bce -- workflows/container-image.md references/criteria/container-image.md`: empty (container files untouched by siblings).
- `### Docker Image Permissions` block matches Step 4 Before (4 bullets, lines 208-212).
- `python3 evals/run_evals.py validate`: 41 evals, 248 assertions (82 deterministic, 166 model-graded).
- `python3 -m unittest discover -s evals -p "test_*.py"`: Ran 12 tests, OK (Preflight count = 12).
- `python3 -m unittest discover -s tests`: Ran 19 tests, OK (skipped=6).
- Optional fact probe: `docker buildx imagetools inspect redis --format '{{json .Provenance}}'` returned a non-empty SLSA provenance (per-platform; e.g. `linux/386` with `buildConfig.digestMapping`). So DOI BuildKit provenance is present on the current `redis` digest. Builder/source fields not inspected beyond the first 400 chars. Rules are written conditionally (A4); no text change. Feeds the eval hand-off only.
**Status:** Success

### [20261016 20:25] - Step 1: Addendum factual refresh (header, registries, signing, SBOM)
**Action:** Applied 1a-1d to `references/criteria/container-image.md` by extracting the plan's After-blocks programmatically (line-range replace with start/end anchor assertions; applied bottom-up 1d, 1c, 1b, 1a). Header precedence carve-out + DHI/Artifact Registry covers; registry table (+DHI, other hardened catalogs, Artifact Registry rename, frozen namespace) and scoring bullets; Signing Standards table (identity flags, GitHub attestations, BuildKit, DCT retired) and scoring; SBOM fetch paragraph + scoring.
**Result:** Verification greps: DOCKER_CONTENT_TRUST=1 docker pull / "Still present for some older" -> 0 (expected 0). `cosign download sbom` -> 2 lines: the new "deprecated" line (77) and the old Tier 1 bullet (184, "SBOM retrievable via `cosign download sbom` / ..."); the latter lives in Tier Assignment Thresholds and is replaced by Step 2g, where the "survives only on deprecated lines" criterion is enforced. `certificate-oidc-issuer` -> 1 (>= 1). Hardened/Frozen/Artifact Registry rows -> 3 (expected 3). Self-verified via `git diff` read-through; Verify-Projex was "Encouraged" and not dispatched (text is verbatim plan After-blocks).
**Status:** Success

### [20261016 20:35] - Step 2: Addendum policy and plug-ins (layers, runtime, tags, CVE, §4.6, tiers)
**Action:** Applied 2a-2g to `references/criteria/container-image.md` (After-blocks extracted from the plan by line range with anchor assertions; applied bottom-up 2g, 2f, 2e, 2d, 2c, 2b, 2a). 2a root row split into root/entrypoint-drop/layer-secret rows; 2b root-at-runtime scoring bullet (dev LOW, non-dev HIGH); 2c user-namespace + PSS low-risk rows; 2d C7 runtime scoring (unverified -> CRITICAL, verified publisher -> HIGH); 2e tag-vs-digest table + scoring (C1, dev rule); 2f new `## CVE Scope (§4.3)` and `## Version & Update Integrity (§4.6)` (V1-V5, Curated pipelines) inserted before Tier thresholds; 2g Tier 1/2/3 rewritten (C4 exceptions, Blocking CVE, V3 trigger).
**Result:** Verification: 2 plug-in headings (expected 2); `^- **V1`..`V5` -> 1 each; `**Curated pipelines:** Docker Official Images` -> 1; stale-phrase grep (any one critical-risk flag on an unverified image | mostly immutable by convention | unpatched critical cve | specific immutable tag) -> 0. `cosign download sbom` now only on the deprecated line (77); `DOCKER_CONTENT_TRUST` only on the Retired row (57). Heading structure intact (257 lines, trailing newline preserved). Self-verified (Verify-Projex Encouraged, not dispatched: text is verbatim plan After-blocks; the full consistency script runs at COMPLETE).
**Status:** Success

### [20261016 20:50] - Step 3: Workflow alignment (`workflows/container-image.md`)
**Action:** Applied 3a-3w (23 replacements/insertions) with After-text extracted from the plan by line range plus start/end anchor assertions: intro; Identify table (Docker Hub row edit, new DHI row, Google Artifact Registry row); context item 2 dev/prod suffix; triage digest bullet; Tier 1 + quick scope; Tier 2 bullets; Tier 3 + deep scope; research Q2/Q3/Q4/Q6/Q8; signature/identity, SBOM and CVE+secret blocks; layer-entrypoint bullet; runtime positives; provenance block; coverage table (+ Version integrity row, canonical-row mapping paragraph); Subject Rubric 4.1 (3 bullets), 4.2 frozen namespaces, 4.3 CVE (+ secrets bullet), 4.4 (4 bullets), 4.6 heading renamed + 2 bullets after heading + Digest refresh after Transitive base CVEs; Verdict Notes REJECTED/CONDITIONAL/APPROVED.
**Result:** Verification: stale-phrase grep (DCT pull, slsa-github-generator, near-automatic rejection, default rejection on developer workloads, rootful image on developer workstation, high CVEs have documented mitigations, unpatched critical cve, specific immutable, google container registry / artifact registry) -> 0; `| Version integrity (§4.6) | Required | Required | Required |` -> 1; `### 4.6 Supply Chain & Version Integrity` -> 1; six template headings -> 6. File 317 -> 349 lines. Diff read-through of signature/SBOM/CVE blocks and 4.4/4.6 sections shows intended structure. Note: the file's top HTML comment (line 3) still says "GCR"; plan scope did not list it, left unchanged (see Issues). Self-verified (Verify-Projex Encouraged, not dispatched).
**Status:** Success

### [20261016 20:55] - Step 4: `references/criteria.md` section 4.4 Docker block (C7 shared leg)
**Action:** Replaced the 4 bullets under `### Docker Image Permissions` with the plan's pointer line + 3 summary bullets (root at runtime; critical-risk flag CRITICAL on unverified identity / HIGH on verified publisher; other caps and host namespaces).
**Result:** `git diff -U0 references/criteria.md`: one hunk, `@@ -209,4 +209,4 @@`, entirely inside the Docker block (4 -/4 +). `grep -c "CRITICAL on an image whose identity does not verify" references/criteria.md` -> 1. Self-verified.
**Status:** Success

### [20261016 21:05] - Post-execution: full verification, paper traces, reviews
**Action:** Ran the plan's consistency script, `python3 evals/run_evals.py validate`, `python3 -m unittest discover -s evals -p "test_*.py"`, `python3 -m unittest discover -s tests`, `git diff --stat 17fa9b1..HEAD`; walked traces T1-T12 against the refreshed files; re-read `references/criteria.md` section 4.3 and 4.6 (the shared floor) for spec compliance; grepped the 3 shipped files for projex references.
**Result:**
- Consistency script: `OK`. validate: 41 evals, 248 assertions (82 det / 166 model-graded), unchanged. evals unittest: 12 tests OK (= Preflight count). tests unittest: 19 tests OK (skipped=6, = baseline).
- `git diff --stat 17fa9b1..HEAD`: exactly 3 non-projex files (`references/criteria.md` 4 lines, `references/criteria/container-image.md`, `workflows/container-image.md`) plus this log. `criteria.md` has one hunk (`@@ -209,4 +209,4 @@`) inside `### Docker Image Permissions`. No projex references in the shipped files (grep for projex|2610|plan|step N -> none).
- Traces (paper): T1 Tier 3 `:latest` DOI exception -> Tier 1 (DOI, dev tag + recorded digest, curated checks, BuildKit SBOM, base DOI chain, root only LOW) -> APPROVED via Toward APPROVED "no flags above LOW" | T1b attestations not checkable -> Tier 2, DOI no-signature LOW note, APPROVED reachable | T1c unfixed OS HIGH -> third-party HIGH -> CONDITIONAL | T2 nginx:latest prod -> Tier 2, HIGH tag flag -> CONDITIONAL | T3 -> Tier 3, no identity, suspicious name -> REJECTED | T4 -> Tier 2, no identity credit, baked npm CVEs third-party HIGH -> CONDITIONAL | T5 V3 HIGH (Tier 3 trigger) -> CONDITIONAL, with confirmed advisory V4(a) "Version-scoped compromise" -> REJECTED | T6 addendum CRITICAL -> SKILL.md node 1 REJECTED, criteria.md section 4.4 agrees | T7 verified publisher + `--privileged` -> HIGH -> CONDITIONAL (isolate runner) | T8 DHI key-verified attestations -> strong positive, Tier 1 identity list includes hardened-catalog attestations | T9 unfixed OS HIGH -> CONDITIONAL; qualifying VEX (names version, justification, maintainer source) excludes it | T10 KEV CRITICAL any layer -> Blocking CVE REJECTED | T11 frozen namespace HIGH -> CONDITIONAL | T12 DOI entrypoint drop verified -> no root flag; `--user 0` override defeats the drop -> root at runtime prod HIGH -> CONDITIONAL. All match the plan's expected column.
- Spec compliance (shared section 4.3 / 4.6): addendum only fills or tightens. V1 version-unit hook, V2 curated-pipelines bullet (names what is checked), V3 diff + ownership, V4 sources, V5 triggers all present; CVE Scope does not change verdict classes and adds no reachability waiver. All met.
- Quality review: no dead text, section names cited by the workflow exist in the addendum, V references name V1-V5 only.
**Status:** Success

### [20261016 21:08] - Success criteria check
**Action:** Walked the plan's Success Criteria.
**Result:** (1) CVE Scope + V&UI sections once each, V1-V5 bullets once each, `**Curated pipelines:** Docker Official Images` present: met. (2) every `§4.6 V<n>` names V1-V5; exactly one shared floor heading: met. (3) stale phrases gone, `cosign download sbom` only on "deprecated" lines, `DOCKER_CONTENT_TRUST` only on "retired" lines: met. (4) no bare `cosign verify <image>`; keyless examples carry both identity flags: met. (5) C7 identical in addendum Runtime scoring, workflow 4.4 + Toward REJECTED/CONDITIONAL, criteria.md Docker block: met. (6) C4 encoded in addendum and workflow, T1 -> Tier 1 APPROVED: met. (7) C6 encoded, T9-T10 match: met. (8) coverage table row + mapping paragraph: met. (9) validate + unittests pass with Preflight count: met. (10) diff lists exactly the 3 files, criteria.md only Docker block: met.
**Status:** Success

### [20261016 21:10] - Cleanup
**Action:** Checked worktree for untracked/ignored artifacts. Scratch scripts (helper.py, step1-4.py) live in the session scratchpad outside the repo. No dependencies were installed, no containers/servers started (the one `docker buildx imagetools inspect` probe is a read-only registry query).
**Result:** `git status --short` in the worktree is empty before the completion commit.
**Status:** Success

## Deviations

- Base moved after planning: plan anchors were verified at 242310a; execution base was 376ba86 (+17fa9b1 start commit). Preflight greps and anchors still matched; no re-anchoring needed.
- Step 1 verification expected `cosign download sbom` on only the "deprecated" line; at that moment the old Tier 1 bullet (replaced in Step 2g) still matched. The plan's own consistency check (final state) passes; no text deviation.
- Verify-Projex was "Encouraged" for Steps 1-3 and Do-Projex for Step 4; neither was dispatched. All After-text was inserted verbatim from the plan by line range with anchor assertions and checked by the plan's greps, the consistency script, and a diff read-through.
- No task/todo tool exists in this environment; the log served as the task ledger.
- The first log commit (a2d0795, local, never pushed) was missing the required attribution trailers and was amended once to add them.

## Issues Encountered

- Precheck WARN "4 uncommitted changes": untracked sibling plan files owned by other orchestrations. Left untouched; the base start-commit staged only this plan.
- Observation, not fixed (out of plan scope): `workflows/container-image.md` top HTML comment (line 3) still lists "GCR" among registries; plan C8 listed only the intro and Identify rows.
- Observation, not fixed (not in plan): the addendum's Medium-risk runtime table still rates `securityContext.runAsUser: 0` as Medium, while the new root-at-runtime rule rates root in production as HIGH. T12 is satisfied through the root-at-runtime rule, but a future stewardship pass may want to reconcile the two rows.

## Data Gathered

- DOI provenance probe: `docker buildx imagetools inspect redis --format '{{json .Provenance}}'` returned a non-empty per-platform SLSA provenance on the current `redis` index, so the T1 premise (DOI BuildKit provenance present) held on 2026-10-16. The builder / source repo fields were not inspected, so Curated pipelines check (3) is still untested on a live digest (plan Risk "check (3) shape"). Useful for the eval hand-off: eval 26 can reach Tier 1 today; the time-dependent premises (no fresh upstream redis release, no unfixed OS HIGH) were not checked.

## User Interventions

None.
