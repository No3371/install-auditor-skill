# Container-Image Rubric Refresh

> **Status:** Complete
> **Completed:** 2026-10-16
> **Walkthrough:** 2610162004-container-image-rubric-refresh-walkthrough.md
> **Author:** Claude (Opus)
> **Parent:** 2610161928-stewardship-review-container-cli-desktop-eval.md
> **Source:** 2610161928-stewardship-review-container-cli-desktop-eval.md (C1–C9; container parts of X1/X3) | Hand-off "container-image" row of 2610161941-shared-version-integrity-floor-plan.md | human decisions C4 + C6 (relayed by orchestrator 2026-10-16)
> **Related Projex:** 2610161941-shared-version-integrity-floor-plan.md (Requires — contract this plan fills) | 2610161852-dispatcher-rubric-consistency-walkthrough.md (prior tensions a–c resolved here) | 2604070218-install-auditor-subject-typed-redesign-nav.md | sibling refresh plans (cli-binary, desktop-app, browser-extension — shares `references/criteria.md` §4.4)
> **Worktree:** Yes
> **Log:** 2610162004-container-image-rubric-refresh-log.md

---

## Summary

The container rubric (written 2026-04-15) scores trust by **presence**, and it is out of date. Three things are wrong:

1. It credits mutable semver tags as Tier-1 immutable.
2. It tells the auditor to run commands that are retired or broken: Docker Content Trust, bare keyless `cosign verify`, and `cosign download sbom`.
3. It grades critical runtime flags three different ways.

It also can't produce the human's C4 outcome (Docker Official Images at Tier 1; eval 26 APPROVED), and its CVE lines contradict the C6 Blocking-CVE rule. This plan rewrites the container addendum and workflow on top of the shared §4.6 floor:

- **Identity:** credit only when the signer, provenance or attestation is matched to the publisher's identity.
- **Curated pipeline for DOI:** a Docker Official Images path (DOI pipeline plus BuildKit attestations).
- **CVE plug-in:** an own-code vs OS/base-layer split, fixable/unfixable handling, KEV and VEX.
- **Version unit:** a DOI rebuild of the same upstream release counts as the same version.
- **C7:** one rule for critical runtime flags. Unverified image → CRITICAL; verified publisher → HIGH.
- **Root at runtime:** a dev workstation gets a LOW note; production is CONDITIONAL.
- **Catalogs:** hardened catalogs (DHI) added, frozen namespaces (`bitnamilegacy`) flagged, GCR naming fixed, user-namespace and PSS positives added, and pinned scanners.

**Scope:** `references/criteria/container-image.md` | `workflows/container-image.md` | `references/criteria.md` §4.4 "Docker Image Permissions" block only. No `SKILL.md`, no other §4.x, no evals, no `STEWARDSHIP.md`, no `references/registries.md`.
**Estimated Changes:** 3 files. Addendum: 2 new sections and 7 rewritten sections. Workflow: ~22 replacements. Criteria: 1 block.

---

## Objective

### Problem / Gap / Need

| ID | Gap (file:line at base `968e70f`) | Fix |
|---|---|---|
| C1 | `1.27.3-alpine` "Mostly immutable by convention … Low-Medium" (addendum L145); Tier 1 accepts "specific immutable tag" (addendum L164, workflow L84, L307) | Every tag is mutable unless the registry visibly enforces immutability. Tier 1 needs a digest, except the C4 dev path |
| C2 | `DOCKER_CONTENT_TRUST=1 docker pull` (workflow L136); "Still present for some older Docker Official tags" (addendum L41) | Mark DCT retired: absence carries no signal, and the variable breaks DOI pulls |
| C3 | Bare `cosign verify <image>` (workflow L112, L133); `cosign download sbom` as Tier 1 evidence (addendum L60, L166; workflow L84, L113, L142); `slsa-github-generator` only (L117, L192); no `gh attestation verify`, no BuildKit inspect | Identity flags are mandatory. Use `verify-attestation` for SBOMs, plus `gh attestation verify oci://` and `docker buildx imagetools inspect --format '{{json .Provenance}}'` |
| C4 (decided) | DOI Tier 1 unreachable (no user-verifiable signature); bare `redis` = `:latest` = Tier 3 trigger (addendum L183); rootful-dev = CONDITIONAL (workflow L298) | Add a V2 curated-pipeline plug-in (DOI) and a V1 version-unit plug-in. Dev-path tag rule; `:latest` Tier 3 exception for DOI/hardened; root-on-dev = LOW note, prod = CONDITIONAL; Toward APPROVED tolerates LOW notes |
| C5 | No hardened catalogs; base list stale (addendum L168) | DHI + other hardened-catalog rows, the DHI Rekor caveat, and a base-list update |
| C6 (decided) | "Any unpatched critical CVE with a known exploit is CRITICAL" (workflow L239); "Unpatched critical CVE with exploit available" (L282); "high CVEs have documented mitigations…" (L309); "Unpatched critical CVE" (addendum L189) | Add a `## CVE Scope (§4.3)` section covering the own-code boundary, fixable/unfixable, KEV, scan and VEX sources. Align the 4 lines to Blocking CVE |
| C7 | Addendum "critical flag on unverified image = HIGH flag" (L135) vs workflow "near-automatic rejection" (L285) vs `criteria.md` §4.4 "docker.sock → CRITICAL" (L194) | One rule in all three files: critical flag + unverified identity = CRITICAL; + verified publisher = HIGH → CONDITIONAL |
| C8 | No frozen-namespace signal (`bitnamilegacy`); "Google Container Registry" naming (addendum L21, workflow L17, L39) | Frozen-namespace row (HIGH → CONDITIONAL); Artifact Registry naming |
| C9 | No user-namespace / PSS / seccomp positives; no digest-refresh rule; no layer secret scan | Low-risk rows; V5 refresh rule; `trivy image --scanners secret` |
| X1 (container) | Signing scored "verify passes = strong positive" (addendum L45–46) | Score only an identity match (V2); a mismatch is a V3 HIGH |
| X3 (container) | Unpinned `trivy`/`grype`/`syft`/`cosign` (workflow L148–156) | Cite the `criteria.md` audit-tooling note; prefer registry-side data |
| Contract | Workflow coverage table lacks `Version integrity` and drops canonical Required rows | Add the row and a mapping sentence for the canonical rows |

### Success Criteria

- [ ] Addendum has `## CVE Scope (§4.3)` and `## Version & Update Integrity (§4.6)` (each once). The latter has bullets that start `- **V1`, `- **V2`, `- **V3`, `- **V4`, `- **V5` (one each) and a `**Curated pipelines:**` sub-bullet naming Docker Official Images.
- [ ] Every `§4.6 V<n>` reference in the 3 files names V1–V5. `references/criteria.md` still has exactly one `## 4.6 Version & Update Integrity (shared floor)`.
- [ ] Stale phrases gone from both container files (case-insensitive; list in the consistency script). `cosign download sbom` survives only on lines that say "deprecated". `DOCKER_CONTENT_TRUST` survives only on lines that say "retired".
- [ ] No backticked bare `` `cosign verify <image>` `` in either container file. Every keyless example carries `--certificate-identity` and `--certificate-oidc-issuer`.
- [ ] C7 says the same thing in the addendum Runtime scoring, the workflow §4.4 + Toward REJECTED/CONDITIONAL, and the `criteria.md` §4.4 Docker block: unverified → CRITICAL, verified publisher → HIGH.
- [ ] C4 is encoded in the addendum (curated pipeline, dev tag rule, Tier 1/3 exceptions, root rule) and in the workflow (Tier 1, Toward APPROVED "no flags above LOW"). Trace T1 yields **Tier 1 → APPROVED** for eval 26 under its stated premises.
- [ ] C6 is encoded: the 4 conflicting lines (workflow L239/L282/L309, addendum L189) now say Blocking CVE / HIGH flag. Traces T9–T10 match §4.3.
- [ ] The workflow coverage table has `| Version integrity (§4.6) |` (Required ×3) plus the canonical-row mapping sentence.
- [ ] `python3 evals/run_evals.py validate` passes. `python3 -m unittest discover -s evals -p "test_*.py"` passes with the Preflight count.
- [ ] `git diff --stat <base>..HEAD` lists exactly the 3 files. In `references/criteria.md`, only the `### Docker Image Permissions` block changes.

### Out of Scope

- `SKILL.md`, `references/criteria.md` §4.3 / §4.6 / Tree terms (shared plan owns them). The `storage` line and the browser table in §4.4 belong to the browser plan.
- `evals/` (eval plan; see Notes → Eval hand-off). `STEWARDSHIP.md` (orchestrator). `references/registries.md` Container Images rows (registry-package plan per the shared Hand-off; suggested rows in Notes).
- `scripts/` (no container scanner script; a KEV lookup is the shared plan's optional tooling follow-on).
- Live `run_evals.py run` (one paid run after all refreshes).
- Reachability-based CVE downgrades. C6 does not grant them, and adding them would loosen §4.3.

---

## Context

### Current State

- `references/criteria/container-image.md` (193 lines). Sections, in order: header (says the addendum wins over the shared rubric) | Registry Trust Signals | Signing Standards | SBOM Standards | Layer Risk Patterns | Runtime Privilege Classification | Tag vs Digest Pinning | Tier Assignment Thresholds. It has no CVE section and no §4.6 plug-in. All verification is presence-based.
- `workflows/container-image.md` (317 lines). Sections: Identify | Evidence Part A (tiers) | Part B (research + commands + coverage table) | Subject Rubric 4.1–4.6 (its `### 4.6 Supply Chain` predates the shared §4.6) | Subject Verdict Notes (Toward REJECTED/CONDITIONAL/APPROVED). The coverage table lacks the canonical Required rows.
- `references/criteria.md` §4.4 `### Docker Image Permissions`: 4 bullets, docker.sock = CRITICAL, the others "flag".
- **Shared floor (landed `20843cc`; re-verified in Preflight):** `criteria.md` has §4.6 V1–V5 with an `**Addendum:**` line each, plus the V2 `**Curated pipelines:**` bullet, the V1 version-unit hook, and the "Audit tooling is itself a dependency" paragraph. Its rows table has `Version integrity (§4.6)` and the "Workflow coverage tables … never drop a Required row" contract. §4.3 holds the C6 CVE table, the Own code / Fixed release / KEV / VEX definitions, and an `**Addendum:**` line ("draws the own-code / third-party line … names its scan and VEX sources. It does not change the verdict classes"). `SKILL.md` has the **Blocking CVE** term, §4.6 floor precedence, and the CRITICAL-flag → REJECTED tree node 1.
- Evals touching this subject: 12 (`nginx:latest` prod → `[APPROVED, CONDITIONAL]`), 13 (cryptominer → `REJECTED`), 26 (`redis` dev → exact `APPROVED`), 38 (`acmecorp/invoice-api` → `[APPROVED, CONDITIONAL]`). None asserts on tier.

### Verified facts (planning, 2026-10-16)

| Fact | Source | Conf |
|---|---|---|
| DCT retirement began with DOI. From 2025-08-08 DOI DCT certs expire; with `DOCKER_CONTENT_TRUST=1`, DOI pulls fail and `docker trust inspect` fails for DOI. Docker promised a replacement DOI signing solution without naming one | docker.com "Retiring Docker Content Trust" (fetched) | H |
| `cosign download sbom` is deprecated, and attached SBOMs are unsigned. The replacement is `cosign attest` / `verify-attestation --type spdxjson\|cyclonedx` | sigstore/cosign `doc/cosign_download_sbom.md`; cosign warning text | H |
| BuildKit stores provenance/SBOM in the image index. `docker buildx imagetools inspect --format '{{json .Provenance}}'` / `.SBOM` reads them | docs.docker.com build attestations | H |
| DOI program: Dockerfiles reviewed; "Actively rebuild"; rebuilt when a base updates. `docker-library/meta-scripts/provenance.jq` builds an in-toto v1 + SLSA Provenance v1 statement (builder = GitHub Actions `workflow_ref`, source = workflow repo) | docker-library/official-images README; meta-scripts `provenance.jq` (fetched) | M-H (DOI provenance generated); **unverified**: that every DOI digest carries it, and whether DOI SBOM attestations exist |
| DHI: SLSA Build L3, signed attestations (SBOM, provenance, VEX, scans), verified with Docker's published key via `docker scout attest get … --verify` or cosign. Some attestations are deliberately kept out of public Rekor, which produces "signature not found in transparency log" | docs.docker.com/dhi/how-to/verify, DHI VEX guide | H |
| `docker scout cves` applies image VEX automatically; `docker scout vex get` exports it. `trivy --vex <file>` (+ `--show-suppressed`), `grype --vex <file>` | Docker DHI scan / VEX docs; trivy.dev VEX docs | H (Trivy/Grype), M (Scout flag details) |
| `gh attestation verify oci://<image> --owner|--repo`, default predicate SLSA provenance v1 | cli.github.com manual | H |
| Tag immutability settings: ECR `IMMUTABLE` (+ `IMMUTABLE_WITH_EXCLUSION`), Artifact Registry immutable tags, Docker Hub immutable tags (**Beta**), configured per repository | AWS ECR docs; docs.docker.com hub immutable-tags; GAR docs | H |
| Bitnami: from ~2025-08-28 versioned images moved to `docker.io/bitnamilegacy` with no updates; free catalog `latest`-only | Rafay, GitLab issues, MOSIP advisory (secondary) | M-H |
| K8s user namespaces GA v1.36 (`hostUsers: false`); caps such as `NET_ADMIN` become namespaced; no gate since 1.33 | kubernetes.io blog 2026-04-23 | H |
| `redis` DOI entrypoint: `exec gosu redis "$0" "$@"` when `$1 = redis-server` and UID 0 | redis/docker-library-redis `docker-entrypoint.sh` (fetched) | H |

### Key Files

| File | Role | Change Summary |
|---|---|---|
| `references/criteria/container-image.md` | Container scoring addendum | Header precedence carve-out. Registry/Signing/SBOM tables refreshed. Layer/Runtime/Tag scoring per C1/C4/C7/C9. New `CVE Scope (§4.3)` + `Version & Update Integrity (§4.6)` sections. Tier thresholds rewritten |
| `workflows/container-image.md` | Container workflow | Intro/registry rows; tiers; research questions; command blocks; coverage table; Subject Rubric 4.1–4.6; Verdict Notes |
| `references/criteria.md` | Shared rubric | §4.4 `### Docker Image Permissions` block → C7/C4 summary pointing at the addendum |

### Dependencies

- **Requires:** 2610161941-shared-version-integrity-floor-plan.md on base `claude/youthful-dijkstra-5ov1kt`. **Verified at planning:** it landed as `20843cc`, and all six Preflight greps pass at base `242310a`. Preflight re-checks this; its stop rule guards against a revert.
- **Concurrent:** the browser-extension plan edits `references/criteria.md` §4.4's browser table, a different hunk from this plan's Docker block. Sibling plans editing `references/criteria.md` must rebase before close, and a conflict there resolves by keeping both hunks. No other sibling owns the container files.
- **Blocks:** eval-refresh plan (container cases; Notes → Eval hand-off).

### Constraints

- Addenda may **tighten or fill** §4.6 and the §4.3 plug-in, never loosen them (`SKILL.md` precedence). In particular, the CVE section must not change verdict classes or add reachability waivers.
- C4 / C6 wording follows the human decisions verbatim in effect (see Assumptions A2–A4 for the interpretation choices).
- Prose only. No projex filenames in shipped files. Dated facts carry "as of 2026-10" once (addendum header), not per line.
- Style: the addendum and the workflow keep their existing shapes. Paragraphs wrap at ~76–78 columns; bullet items and table rows stay as single long lines, as they are now.
- Preserve the workflow's section template headings (`## Identify`, `## Evidence — Part A …`, `## Evidence — Part B …`, `## Subject Rubric — Evaluate`, `## Subject Verdict Notes`, `### Toward REJECTED|CONDITIONAL|APPROVED`).

### Assumptions

- **A1:** The shared plan lands with the strings this plan cites. That covers `## 4.6 Version & Update Integrity (shared floor)`, `**Curated pipelines:**`, "Audit tooling is itself a dependency", `| Version integrity (§4.6) |` and "Blocking CVE". Preflight greps each one.
- **A2 (C4, dev vs non-dev):** the human decision names only "dev workstation" (LOW) and "production" (CONDITIONAL). This plan treats every non-dev workload (shared hosts, CI runners, clusters) as production, which is the conservative reading. Changing it is a one-phrase edit in 4 places (addendum Layer scoring, workflow §4.4 + Toward CONDITIONAL, `criteria.md` §4.4).
- **A3 (C4, tag on dev):** "Trust the DOI pipeline … enough for Tier 1" plus "eval 26 stays APPROVED" (bare `redis`) requires a non-digest Tier 1 path. It is scoped to Docker Official / hardened-catalog images on dev use, where the audit records the resolved digest and the Recommendation pins it. This matches §4.6's "for an unpinned request, what it resolves to now". Production tags never reach Tier 1 (C1).
- **A4 (C4, attestations):** "plus BuildKit attestations" is read as **required**. The curated-pipeline credit needs a non-empty BuildKit provenance attestation on the resolved digest. If the attestation cannot be checked, the audit falls to Tier 2 and APPROVED stays reachable. So eval 26 does not depend on the unverified DOI-attestation fact (Verified facts row 4), only its tier label does.
- **A5:** "Verified publisher" in the C7 rule = identity verified per §4.6 V2, including the DOI curated-pipeline checks. A merely badged but unchecked image counts as unverified.
- **A6:** Every Before string and block anchor below matched exactly once at base `242310a` (checked by script at planning). Container files are unchanged since `97f6bce`, and the shared plan left `criteria.md` §4.4 untouched. Re-anchor on a miss; don't improvise wording.

### Impact Analysis

- **Direct:** the 3 files.
- **Adjacent:** `SKILL.md` tree node 1 (CRITICAL flag → REJECTED) now fires for critical runtime flags on unverified images, where before it produced CONDITIONAL. The `SKILL.md` Red Flags are unchanged. The shared §4.3 verdict classes are applied, not altered.
- **Downstream:** live container verdicts shift.
  - Semver-tagged production images → Tier 2 + pin condition.
  - Unverified image + `--privileged`/docker.sock → REJECTED.
  - Unfixed OS-package HIGH → CONDITIONAL. This is already the shared rule; the workflow text now agrees.
  - Root-in-production → CONDITIONAL. Root on a dev workstation → LOW only.
  - `bitnamilegacy/*` → CONDITIONAL.
  - DOI on dev → Tier 1 possible.
  - Eval-level effects are in Notes → Eval hand-off.

---

## Implementation

### Overview

Preflight (shared plan landed? anchors intact?). Then the addendum, in two steps: factual refresh first, policy and plug-ins second. Then the workflow, then the `criteria.md` §4.4 block. Each change is either an exact `Before → After` pair or a **block replacement** bounded by two anchor lines ("from line X through the line before Y"). Use the Edit tool. A missed anchor means the base moved: re-read that region and re-anchor.

**Preflight** (run in `<work-root>`; log results):

```bash
git log --oneline -1
grep -c "^## 4\.6 Version & Update Integrity (shared floor)" references/criteria.md   # 1
grep -c "^- \*\*Curated pipelines:\*\*" references/criteria.md                         # 1
grep -c "^- \*\*Addendum:\*\*" references/criteria.md                                   # 6
grep -c "Audit tooling is itself a dependency" references/criteria.md                   # 1
grep -c "| Version integrity (§4.6) |" references/criteria.md                           # 1
grep -c "Blocking CVE" SKILL.md                                                         # >= 1
git diff --stat 97f6bce -- workflows/container-image.md references/criteria/container-image.md   # empty
grep -n -A4 "^### Docker Image Permissions" references/criteria.md                      # equals Step 4 Before
python3 evals/run_evals.py validate | head -3
python3 -m unittest discover -s evals -p "test_*.py" 2>&1 | tail -3                     # record count
```

**Stop rule:** any of the first six greps differs → set this plan `Blocked` (shared floor not on base) and stop. A non-empty container diff means a sibling touched the files: re-anchor every step against the new text.

**Optional fact probe** (only if `docker`, `crane` or `skopeo` exists; otherwise log "not probed"): `docker buildx imagetools inspect redis --format '{{json .Provenance}}' | head -c 400`. Log whether DOI provenance is present. The rules are written conditionally (A4), so the result changes no text. It only feeds the eval hand-off.

---

### Step 1: Addendum — factual refresh (header, registries, signing, SBOM)

**Objective:** fix C2, C3, C5, C8 and the X1 signing scoring in `references/criteria/container-image.md`. Add the precedence carve-out.
**Confidence:** High
**Depends on:** Preflight
**Verify-Projex:** Encouraged (identity scoring is easy to get subtly wrong)

**Files:** `references/criteria/container-image.md`

**1a — Header.** Replace lines 3–10 (from `Per-subject scoring extensions` through `(GCR/GAR), and other OCI-compliant registries.`) with:

```markdown
Per-subject scoring extensions for **Type 4: container-image** audits. This
addendum layers on top of the shared rubric in `references/criteria.md`.
When a criterion below conflicts with the shared rubric, the more specific
(container-image) guidance wins — except the version-integrity floor
(`references/criteria.md` §4.6) and the §4.3 CVE verdict classes, which
this addendum only tightens or fills (sections "CVE Scope (§4.3)"
and "Version & Update Integrity (§4.6)" below).

Covers: Docker Hub, Docker Hardened Images (`dhi.io`), GitHub Container
Registry (GHCR), Quay, Amazon ECR (public + private), Google Artifact
Registry (incl. legacy `gcr.io` paths), and other OCI-compliant registries.
Registry facts and commands are as of 2026-10; re-check them at each
stewardship review.
```

**1b — Registry Trust Signals.** Block replacement: from the line `| Docker Hub | "Docker Official Image" badge, …` through the line `- Self-hosted / mirror registry republishing a popular image = strong negative …` (the end of its `### Scoring impact`). Replace with:

```markdown
| Docker Hub | "Docker Official Image" badge, "Verified Publisher" badge, "Sponsored OSS" | Pull count, stars | Largest catalog. Official Images (`docker.io/library/<name>`, pulled as bare `<name>`) are built by the Docker Official Images program from reviewed Dockerfiles in public GitHub repos and rebuilt when their base updates — a curated pipeline (see "Version & Update Integrity (§4.6)"). Verified Publisher = vetted org. Unbadged images vary wildly in quality. Some namespaces are frozen (row below). |
| Docker Hardened Images (`dhi.io`) | Docker-built hardened catalog (Docker account login may be required) | — | Minimal images with signed attestations (SBOM, SLSA Build Level 3 provenance, VEX, scan results), verified with Docker's published key. Some attestations are deliberately kept out of the public Rekor log, so a default `cosign verify` can report "signature not found in transparency log" — that is not "unsigned" (Signing Standards). |
| Other hardened catalogs (e.g. Chainguard `cgr.dev`) | Vendor namespace | — | Minimal images signed with Cosign; the vendor documents the signing identity. Verify against that documented identity. |
| GHCR (`ghcr.io`) | Org-scoped (linked to GitHub org); "Publisher" tag on package page; optional package attestations | GitHub package downloads (where visible) | Inherits GitHub org identity. Strong when the GitHub org is well-known (e.g., `ghcr.io/open-telemetry/...`). |
| Quay (`quay.io`) | Verified Publisher; Red Hat-maintained orgs (`quay.io/redhat/*`, UBI images) | Pull count | Red Hat ecosystem; integrated Clair CVE scanner; long-standing signing support. |
| Amazon ECR Public (`public.ecr.aws`) | AWS-maintained namespaces (`public.ecr.aws/amazonlinux/`, `public.ecr.aws/lambda/`) | Pull count | Public ECR gallery. AWS namespaces are strongly trusted; third-party namespaces are case-by-case. |
| ECR Private | Private-account scope (authenticated pulls only) | None public | Trust derives from the AWS account and IAM policies, not a public badge. |
| Google Artifact Registry (`<region>-docker.pkg.dev`, legacy `gcr.io`) | Google-maintained projects (`gcr.io/distroless/*`, `gcr.io/google-containers/*`) | None public | Container Registry is shut down; `gcr.io` paths are served by Artifact Registry. Distroless images are a widely trusted minimal-base source. |
| Frozen / legacy namespace | Publisher notice that the namespace gets no further updates (e.g. `docker.io/bitnamilegacy`, from 2025-08) | Inherited pull counts mislead | Familiar publisher name, but no security updates. Badge and pull count say nothing about current maintenance. |
| Self-hosted / mirror | None | None | No external verification. Assume lower baseline trust; mirror registries can republish tampered images. |

### Scoring impact

- Docker Official Image = strong positive (equivalent to AMO Recommended for extensions). Identity credit comes from the curated-pipeline checks (§4.6 V2 plug-in); the badge does not make a tag immutable or a CVE acceptable
- Hardened-catalog image whose signed attestations verify against the publisher's documented key or identity = strong positive; satisfies the Tier 1 identity requirement
- Docker Hub Verified Publisher = moderate positive
- GHCR org-scoped under a recognizable GitHub org = moderate positive (equivalent to the GitHub org's reputation)
- Quay verified publisher or AWS/Google official namespace = moderate positive
- Unbadged Docker Hub image from an unknown user = neutral to negative (depends on adoption signals)
- Frozen / legacy namespace = HIGH flag `frozen namespace` → CONDITIONAL. Condition: move to a maintained source (upstream image, Docker Official Image, hardened catalog). Score maintenance as Abandoned (`references/criteria.md` §4.2)
- Self-hosted / mirror registry republishing a popular image = strong negative unless the mirror is operated by a trusted org (e.g., an internal corporate mirror)
```

**1c — Signing Standards.** Block replacement: from `## Signing Standards` through the line `- No signing, org policy requires signed images = HIGH flag (policy violation)`. Replace with:

```markdown
## Signing Standards

Record what each check proves and **whose** identity it names
(`references/criteria.md` §4.6 V2). Always check the resolved digest, and
confirm flags with `--help` on the pinned tool version.

| Standard | Invocation | Notes |
|----------|-----------|-------|
| Cosign / Sigstore (keyless) | `cosign verify <image>@<digest> --certificate-identity <expected SAN> --certificate-oidc-issuer <expected issuer>` (or `--certificate-identity-regexp` anchored to the publisher's repo and workflow) | OIDC identity + Fulcio-issued cert + transparency log. Identity flags are mandatory in keyless mode: without them the command errors, which is not evidence that the image is unsigned. |
| Cosign / Sigstore (keyed) | `cosign verify <image>@<digest> --key <publisher key>` | Key from the publisher's documented location. Docker Hardened Images: Docker's published key; follow Docker's verify docs (`docker scout attest get … --verify`, or the documented transparency-log skip) because some DHI attestations are not in public Rekor. |
| Cosign attestations | `cosign verify-attestation <image>@<digest> --type slsaprovenance\|spdxjson\|cyclonedx` + the keyless identity flags or `--key` | Signed in-toto attestations (provenance, SBOM). |
| GitHub artifact attestations | `gh attestation verify oci://<image>@<digest> --owner <org>` (or `--repo <org>/<repo>`) | Produced by `actions/attest-build-provenance` / `actions/attest`; checks SLSA provenance v1 by default. Registry login may be required. |
| BuildKit attestations | `docker buildx imagetools inspect <image> --format '{{json .Provenance}}'` (and `'{{json .SBOM}}'`) | Provenance / SBOM stored in the image index. Unsigned unless the publisher also signs them: they count as identity only through the curated-pipeline plug-in or when their source repo matches the expected identity. |
| Notary v2 / Notation | `notation verify <image>@<digest>` | OCI-standard alternative; needs the publisher's trust policy / certificate. Less common in practice than Cosign. |
| Docker Content Trust (Notary v1) | — (do not use) | Retired by Docker from 2025. With `DOCKER_CONTENT_TRUST=1` set, Docker Official Image pulls fail and `docker trust inspect` no longer works for them. Absence of DCT carries no signal. |

### Scoring impact

- Signature or attestation verifies **and** its identity (certificate SAN + issuer, key owner, or provenance source repo + workflow + ref) matches the expected identity (§4.6 V2) = strong positive for identity. It proves origin, not safety
- Check passed but identity not matched, or only presence checked = note, no credit
- Identity names a different signer or repo than prior releases or the publisher's docs = HIGH flag (§4.6 V3)
- Notation verify passes against the publisher's trust policy = moderate-to-strong positive
- No user-verifiable signature, Docker Official Image = LOW note; identity via the curated-pipeline checks ("Version & Update Integrity (§4.6)")
- No signing, unverified publisher = MEDIUM flag on any privileged workload
- No signing, org policy requires signed images = HIGH flag (policy violation)
```

**1d — SBOM Standards.** Block replacement: from the line `Fetch SBOMs via \`cosign download sbom <image>\`` through the line `- SBOM generated by Syft or Trivy locally, complete = moderate positive (confirms contents but not publisher intent)`. Replace with:

```markdown
Fetch SBOMs from, in order of strength: a signed SBOM attestation (`cosign verify-attestation --type spdxjson|cyclonedx` with identity flags); a BuildKit SBOM attestation (`docker buildx imagetools inspect <image> --format '{{json .SBOM}}'`); `docker scout sbom <image>`; or a local scan (`syft <image> -o spdx-json` / `syft <image> -o cyclonedx-json`, pinned per the `references/criteria.md` audit-tooling note). `cosign download sbom` is deprecated and returns unsigned attachments: treat its output as contents data, not publisher-attested evidence.

### Scoring impact

- SBOM in a signed attestation whose identity verifies (§4.6 V2), complete (OS + language packages) = strong positive
- BuildKit SBOM attestation or legacy attached SBOM (unsigned), complete = moderate positive (publisher-built contents, not signed)
- SBOM generated by Syft or Trivy locally, complete = moderate positive (confirms contents but not publisher intent)
```

(The two remaining SBOM bullets, "No SBOM available …" and "Publisher claims SBOM …", stay unchanged below.)

**Rationale:**
- Each table row states what the check proves. That makes X1's "presence ≠ trust" mechanical for the auditor.
- DCT is kept as a row so its absence is explicitly neutral. Deleting the row would leave auditors who know DCT guessing.
- DHI's Rekor caveat sits in two places (registry row + signing row) because both are where an auditor would wrongly conclude "unsigned".
- The frozen namespace is HIGH, not MEDIUM. No updates means guaranteed CVE accumulation, and MEDIUM alone would still allow APPROVED.
- GCR is renamed to Artifact Registry because the old name no longer exists (review C8).

**Verification:**
```bash
grep -c "DOCKER_CONTENT_TRUST=1 docker pull\|Still present for some older Docker Official tags" references/criteria/container-image.md   # 0
grep -n "cosign download sbom" references/criteria/container-image.md     # only the "deprecated" line
grep -c "certificate-oidc-issuer" references/criteria/container-image.md  # >= 1
grep -c "^| Docker Hardened Images\|^| Frozen / legacy namespace\|^| Google Artifact Registry" references/criteria/container-image.md   # 3
```

**If this fails:** `git -C <work-root> checkout -- references/criteria/container-image.md` and redo 1a–1d.

---

### Step 2: Addendum — policy and plug-ins (layers, runtime, tags, CVE, §4.6, tiers)

**Objective:** encode C1, C4, C6 (subject part), C7, C9, and fill the §4.6 and §4.3 plug-ins.
**Confidence:** High (C1/C7/C9); Medium-High (C4 curated-pipeline check 3; see Risks)
**Depends on:** Step 1
**Verify-Projex:** Encouraged (encodes two human policy decisions)

**Files:** `references/criteria/container-image.md`

**2a — Layer Risk Patterns, root row.** Before:
```markdown
| `USER root` (or no `USER`) | Medium-High | Container runs as root inside its namespace; combined with shared kernel, escape bugs land on the host as root |
```
After:
```markdown
| `USER root` (or no `USER`) and no verified entrypoint privilege drop | LOW on a dev workstation; HIGH in production (Scoring impact) | Container runs as root inside its namespace; combined with shared kernel, escape bugs land on the host as root |
| Entrypoint drops privileges (`gosu`, `su-exec`, `setpriv` in the entrypoint script) | Low | Starts as root to fix file ownership, then execs the service as a non-root user (e.g. `redis` runs `exec gosu redis` for `redis-server`). Read the entrypoint to verify; the drop often applies only to the image's default command |
| Secrets found by a layer scan (`trivy image --scanners secret`) | High | Same exposure as `ENV` secrets; leaked API keys in public images are common |
```

**2b — Layer Risk Patterns, scoring.** Before:
```markdown
- Any 2 high patterns = HIGH flag
- Any 1 high pattern without justification = MEDIUM-HIGH flag
- Multiple medium patterns (3+) = MEDIUM flag (cumulative hygiene concern)
```
After:
```markdown
- Root at runtime (first row): dev workstation = LOW note `root at runtime (dev)` (the Recommendation may suggest rootless Docker / Podman); production or any other non-dev workload (shared host, CI runner, cluster) = HIGH flag → CONDITIONAL. Condition: non-root `USER` / `runAsNonRoot: true`, a rootless runtime, or Kubernetes user namespaces (`hostUsers: false`). This row is rated only by this rule, not by the pattern counts below
- Any 2 high patterns = HIGH flag
- Any 1 high pattern without justification = MEDIUM-HIGH flag
- Multiple medium patterns (3+) = MEDIUM flag (cumulative hygiene concern)
```

**2c — Low-risk runtime rows.** After the line `| \`seccomp=default\` + \`apparmor=docker-default\` | Low | Layered MAC policies |` insert:
```markdown
| `hostUsers: false` (Kubernetes user namespaces; GA in v1.36) | Low | Container root maps to an unprivileged host UID; capabilities such as `NET_ADMIN` only affect the pod's own namespaces |
| Namespace enforces Pod Security Standard `restricted`; `seccompProfile: RuntimeDefault` | Low | Baseline that blocks privileged pods, host namespaces, hostPath mounts and root |
```

**2d — Runtime scoring (C7).** Before:
```markdown
- Any one critical-risk flag on an unverified image = HIGH flag
- Any critical-risk flag on any image without documented justification = MEDIUM-HIGH flag
```
After:
```markdown
- Critical-risk flag (`--privileged`, `--cap-add=SYS_ADMIN`, `/var/run/docker.sock` or host `/`, `/etc`, `/proc`, `/sys`, `/dev` mounts) on an image whose identity does not verify (§4.6 V2, incl. the Docker Official Images curated-pipeline checks) or from an unknown publisher = CRITICAL → REJECTED (`SKILL.md` CRITICAL flag)
- Critical-risk flag on a verified-publisher image = HIGH flag → CONDITIONAL. Condition: drop the flag; or, where the publisher documents the need (e.g. Docker-in-Docker on an isolated CI runner, a node agent), isolate the host and record the justification
- User namespaces (`hostUsers: false`) or a rootless runtime lower each High-risk capability row one step (High → Medium); they do not lower Critical rows
```
(The "Multiple high-risk flags …" and "Default-safe runtime …" bullets stay.)

**2e — Tag vs Digest Pinning (C1, C4 dev rule).** Block replacement: from the line `| \`<image>@sha256:<hex>\` (digest) | …` through the line `- \`:latest\` + \`--privileged\` + unknown publisher = compound flag, push to REJECTED`. Replace with:

```markdown
| `<image>@sha256:<hex>` (digest) | Immutable — content-addressed | Lowest; bit-identical pulls (but frozen — see §4.6 V5 plug-in) |
| Tag in a repository with enforced tag immutability (ECR `IMMUTABLE`, Artifact Registry immutable tags, Docker Hub immutable tags — beta) | Immutable while the setting holds | Low — only when the auditor can see the setting (own or org registry) or the publisher documents it |
| `<image>:<specific-semver>-<variant>` (e.g., `1.27.3-alpine`) | Mutable — the publisher, or anyone holding its push credentials, can repoint it; trusted-publisher tags were overwritten in 2026 incidents | Medium |
| `<image>:<major>` (e.g., `:1` or `:1.27`) | Mutable — floats to latest minor/patch | Medium |
| `<image>:latest` | Mutable — floats to whatever publisher most recently pushed | High on production; dev rule below |
| `<image>` (no tag) | Equivalent to `:latest` | High on production; dev rule below |

### Scoring impact

- Digest-pinned reference = strong positive; the default Tier 1 reference requirement
- Specific semver tag = weak positive; never Tier 1 eligible on its own. Production condition: pin the digest it resolves to now
- Floating minor/major tag = MEDIUM flag on production
- `:latest` or no tag on production = HIGH flag → CONDITIONAL (pin the digest)
- Any tag on dev / experimental use (incl. `:latest` or no tag) = LOW note when the audit records the digest the tag resolves to now and the Recommendation pins it; MEDIUM note otherwise
- `:latest` + `--privileged` + unknown publisher = compound flag, push to REJECTED
```

**2f — New sections.** Insert directly before `## Tier Assignment Thresholds (Container Images)`:

```markdown
## CVE Scope (§4.3)

`references/criteria.md` §4.3 and the `SKILL.md` term **Blocking CVE** set
the verdict classes; this section only maps them onto image layers. It does
not change the classes.

- **Own code** = what the image exists to ship and its publisher builds: the application binary or service (`redis-server` in `redis`, the app code in a team's service image) and any component the publisher compiles from source or patches itself.
- **Third-party component** = OS packages from the base distribution, base-image layers, and language dependencies installed into the image (e.g. `npm` / `pip` packages baked into an app layer).
- **Fixable vs unfixable** — the scanner's fixed-version column decides:
  - Fix exists → HIGH flag. Condition: pull or rebuild a digest that includes the fix (Official and hardened images are rebuilt for distro fixes; check whether a newer digest of the same tag already has it), then audit that digest per §4.6.
  - No fix (third-party component) → HIGH flag. Condition: workload mitigations (network policy, seccomp, no host mounts, non-root) and re-audit when a fix ships.
  - Use fixed-only filters (`trivy image --ignore-unfixed`) only to list what an upgrade would remove — never to drop unfixed findings from the rating.
- **KEV:** check every CRITICAL in every layer, OS packages included, per §4.3. A KEV-listed CRITICAL rejects the digest.
- **Scan sources** (prefer two; record tool + version per the `references/criteria.md` audit-tooling note): registry-side data (Docker Scout on Docker Hub, GHCR / Quay vulnerability tabs) | a pinned local scanner (`trivy image`, `grype`, `docker scout cves`). If the local scanner's identity cannot be verified, use registry-side data only and say so in the CVE row.
- **VEX sources:** VEX attestations shipped with the image (Docker Hardened Images ship them; `docker scout cves` applies image VEX automatically and `docker scout vex get` exports it) | OpenVEX / CSAF / CycloneDX VEX from the image publisher or the component's maintainer (e.g. the distribution), applied with `trivy image --vex <file>` or `grype --vex <file>`. A `not_affected` entry counts only when it meets §4.3 (names this image or package version, gives a justification, comes from the publisher or maintainer). Record suppressed CVEs and their VEX source in the CVE row (`trivy … --show-suppressed`).

## Version & Update Integrity (§4.6)

Plug-ins for the shared floor in `references/criteria.md` §4.6. Anything not
listed here uses the shared default.

- **V1 Version age:**
  - **Version unit** (used by V1–V3): the upstream application release the image ships (`org.opencontainers.image.version` label, or the upstream version the tag names). A rebuild of the same upstream release by the Docker Official Images program or a hardened catalog (base refresh, distro security fix, traceable to that pipeline) is the same version: age runs from the upstream release, not the rebuild. Any other publisher: a new digest is a new version unless verified provenance (V2) shows the same source revision as the prior digest. A new upstream release is always a new version.
  - **Publish time:** the upstream release date for the version unit. For a new digest outside a curated rebuild: its push time ("Last pushed" on the registry page, config `created`, `org.opencontainers.image.created`).
  - **Cooldown in conditions:** Docker has no client cooldown; cite a digest-update bot's release-age gate (e.g. Renovate `minimumReleaseAge`) applied to digest pins.
- **V2 Verified identity:**
  - **Mechanisms and commands:** the Signing Standards table. Every keyless check names the expected identity.
  - **Expected identity source:** the publisher's documentation (README, security or verification page), the release workflow in the `org.opencontainers.image.source` repo, or the identity prior digests carried. Record it in the Version integrity row.
  - **Absence:** no user-verifiable signature → no credit; flag rules in Signing Standards "Scoring impact".
  - **Curated pipelines:** Docker Official Images. Instead of a user-verifiable signature, check all three on the resolved digest: (1) the namespace is `docker.io/library/<name>` with the Docker Official Image badge; (2) a BuildKit provenance attestation is present (`docker buildx imagetools inspect <image>@<digest> --format '{{json .Provenance}}'` is non-empty; an SBOM attestation from `'{{json .SBOM}}'` also fills the SBOM row); (3) the provenance's builder or source repo belongs to the Official Images build infrastructure (`docker-library` GitHub org) or to the image's source repo linked from its Hub page — record what it names. All three pass → identity counts as verified for the Tier 1 identity requirement. Attestations cannot be checked (tool unavailable, none present) → no curated-pipeline credit; audit at Tier 2, where APPROVED stays reachable.
- **V3 Continuity:** compare the resolved digest with the previous release's digest. Check the `org.opencontainers.image.source` / `revision` labels, the provenance source repo + workflow, the signer identity, the image config (`User`, `Entrypoint`, `Cmd`, `ExposedPorts`) and the run flags the publisher documents. Two cases are a V3 HIGH flag (the 2026 trusted-publisher tag-overwrite pattern): a tag that moved to content with no matching upstream release or git tag, or provenance naming a different or newly created repo. A namespace transfer or new publisher account → at least MEDIUM.
- **V4 Incident sources:** registry removal notices (Docker Hub, GHCR, Quay), Docker and publisher security posts, GHSA for the image's source repo.
- **V5 Triggers and update controls:**
  - Triggers: base distribution major change (e.g. Debian 12 → 13) | new upstream major | namespace frozen or transferred | signer or provenance change.
  - Update controls: digest pins in Dockerfile `FROM`, Compose and Kubernetes manifests; bot-driven digest refresh with a release-age gate; admission policy that enforces the expected signer (e.g. Kyverno, Sigstore policy-controller).
  - A digest pin also freezes risk: an old digest keeps every CVE and backdoor it shipped with (Debian-based Hub images were reported still carrying the xz-utils backdoor, CVE-2024-3094, in 2025). Recommendation: refresh pins on a cadence and audit each new digest per §4.6.
```

**2g — Tier Assignment Thresholds.** Block replacement: from the line after `### Tier 1 — Quick Audit` (blank) through the last line of the file (`- Dockerfile contains \`curl \| sh\` / \`ADD <url>\` / embedded credentials`). Replace with:

```markdown

ALL of these must hold, and `references/criteria.md` §4.6 must raise nothing that bars Tier 1:
- Docker Official Image, hardened-catalog image, Verified Publisher, GHCR package under a recognizable GitHub org, or cloud-vendor official namespace — not a frozen / legacy namespace
- Reference is digest-pinned (`@sha256:...`), OR — dev / experimental use only — a Docker Official or hardened-catalog tag whose current digest the audit records and the Recommendation pins. A semver tag alone never qualifies
- Identity verified per §4.6 V2: a matched Cosign signature or attestation, a matched GitHub artifact attestation, a hardened catalog's key-verified attestations, or the Docker Official Images curated-pipeline checks ("Version & Update Integrity (§4.6)")
- SBOM available: signed or BuildKit SBOM attestation, `docker scout sbom`, or a publisher-provided SBOM
- No CRITICAL CVE and no Blocking CVE on the resolved digest after qualifying VEX ("CVE Scope (§4.3)")
- Base image is a recognized minimal or hardened base (distroless, alpine, debian-slim, ubi-micro, Docker Hardened Images, Chainguard / Wolfi) from an official source, or — for a Docker Official Image — a `FROM` chain of other Docker Official Images
- Runtime profile is default-safe: default caps, no host namespaces, no critical- or high-risk flag; root at runtime only on a dev workstation (LOW note)

### Tier 2 — Standard Audit (default)

Default when not all Tier 1 criteria are met:
- Named tag without digest pin outside the dev rule above, or a production `:latest` / no-tag reference to a Docker Official or hardened-catalog image
- No verifiable signature, but publisher is identifiable (incl. a Docker Official Image whose curated-pipeline attestations could not be checked)
- Popular but unverified Docker Hub publisher, or mid-tier GHCR package
- No explicit SBOM but image is from a recognized base and is recently pushed
- Runtime profile is mostly default but may request a specific `cap_add` or bind mount

### Tier 3 — Deep Audit

ANY of these triggers:
- `:latest` or no tag with no digest pin — except Docker Official and hardened-catalog images (Tier 2 in production with the HIGH tag flag; dev per Tier 1)
- Unknown or self-hosted mirror registry
- No publisher identity
- `--privileged` requested, OR `cap_add` including SYS_ADMIN/NET_ADMIN/SYS_PTRACE/DAC_OVERRIDE, OR `/var/run/docker.sock` mount
- `hostNetwork` / `hostPID` / `hostIPC` set
- Image older than 2 years with no rebuild
- Blocking CVE (`SKILL.md` Tree terms), or an unfixed CRITICAL in an OS / base layer
- §4.6 V3 HIGH flag (tag moved with no upstream release, provenance or signer mismatch)
- Suspicious naming (impersonates a well-known image, cryptominer-like names, typo of a popular base)
- `FROM` chain transits an unknown or unrecognized base
- Scraped / mirror registry republishing popular image names
- Dockerfile contains `curl \| sh` / `ADD <url>` / embedded credentials, or a layer secret scan finds credentials
```

**Rationale:**
- **C4 needs three coordinated edits.** The curated-pipeline credit (identity), the dev-tag rule (reference) and the `:latest` Tier 3 exception (trigger) each remove one of the three blockers trace C4 found, so without all three, eval 26 stays unreachable at Tier 1. The scope is narrow: DOI/hardened only, the dev path only, and attestations required (A3, A4).
- **Production behavior is unchanged in spirit.** Production unpinned → HIGH → CONDITIONAL, which matches eval 12. The DOI `:latest` exception moves eval 12 from Tier 3 to Tier 2, which also matches eval 12's description.
- **C7: one rule, enforced via `SKILL.md` node 1.** An addendum CRITICAL is a "CRITICAL flag" per Tree terms, so no `SKILL.md` edit is needed. A verified publisher gets HIGH because the remedy (drop the flag or isolate) is a condition, not a rejection. That keeps `docker:dind` on CI at CONDITIONAL.
- **C6 plug-in only maps layers.** "Fixable → HIGH" follows §4.3: Blocking CVE covers only own-code unfixed and KEV CRITICAL, so a fixable CRITICAL is a HIGH flag. The `--ignore-unfixed` guard stops a common scanner flag from silently hiding the CONDITIONAL class.
- **V3 targets the KICS pattern.** It is the only container-specific continuity signal with incident evidence.
- **Rejected alternatives.**
  - Grant DOI Tier 1 on the badge alone, without attestations: the human said "pipeline **plus** BuildKit attestations".
  - Keep semver tags at Low-Medium: 2026 incident evidence (review C1).
  - Rate the root-on-dev case MEDIUM: the human decided LOW.

**Verification:**
```bash
F=references/criteria/container-image.md
grep -c "^## CVE Scope (§4.3)$\|^## Version & Update Integrity (§4.6)$" $F   # 2
for v in 1 2 3 4 5; do grep -c "^- \*\*V$v " $F; done                                # 1 each
grep -c "\*\*Curated pipelines:\*\* Docker Official Images" $F                        # 1
grep -ci "any one critical-risk flag on an unverified image\|mostly immutable by convention\|unpatched critical cve\|specific immutable tag" $F   # 0
```

**If this fails:** revert the file to its post-Step-1 state (`git -C <work-root> diff` to inspect; re-checkout and redo Steps 1–2 if needed).

---

### Step 3: Workflow — align `workflows/container-image.md`

**Objective:** make the workflow's tiers, research questions, commands, coverage table, Subject Rubric and Verdict Notes match Steps 1–2 (C1–C9, C4, C6, X3).
**Confidence:** High
**Depends on:** Steps 1–2 (section names it cites)
**Verify-Projex:** Encouraged

**Files:** `workflows/container-image.md`

**3a — Intro paragraph.** Replace lines 15–21 (from `This workflow handles **Type 4: container-image** subjects` through `runtime privilege.`) with:
```markdown
This workflow handles **Type 4: container-image** subjects — OCI/Docker
images distributed via Docker Hub, Docker Hardened Images (`dhi.io`),
GitHub Container Registry (GHCR), Quay, Amazon ECR, Google Artifact
Registry (incl. legacy `gcr.io` paths), or any other OCI registry. It
specializes the generic evidence acquisition and scoring pipeline for
container concerns: identity-matched signing and attestations, SBOM
presence, base image lineage, tag vs digest pinning, layer CVEs, version
integrity, and runtime privilege.
```

**3b — Identify table.** Three row edits:
```markdown
// Before:
| Docker Hub | `docker.io/<ns>/<repo>:<tag>` or bare `<repo>:<tag>` | Largest catalog; "Docker Official" and "Verified Publisher" badges exist but most images have neither |
// After:
| Docker Hub | `docker.io/<ns>/<repo>:<tag>` or bare `<repo>:<tag>` | Largest catalog; "Docker Official" and "Verified Publisher" badges exist but most images have neither; some namespaces are frozen (e.g. `bitnamilegacy`) |
| Docker Hardened Images | `dhi.io/<repo>:<tag>` (Docker login may be required) | Docker-built hardened catalog; signed attestations verified with Docker's key (addendum) |

// Before:
| Google Container Registry / Artifact Registry | `gcr.io/<proj>/<repo>` (legacy) or `<region>-docker.pkg.dev/<proj>/<repo>` | Google-authenticated; Artifact Registry supersedes GCR |
// After:
| Google Artifact Registry | `<region>-docker.pkg.dev/<proj>/<repo>` or legacy `gcr.io/<proj>/<repo>` | Google-authenticated; Container Registry is shut down and `gcr.io` paths are served by Artifact Registry |
```

**3c — Context item 2.** Before: `2. **Intended runtime** — local Docker, Docker Compose, Kubernetes, Podman, ECS/EKS/GKE, CI runner, or one-shot \`docker run\``. After: same text + ` — and whether it is a **dev workstation or production / shared** environment (this changes tag and root-at-runtime grading)`.

**3d — Triage bullets.** After the line `- Last pushed date for the tag (mutable tags update; old last-pushed is a staleness flag)` insert:
```markdown
- The digest the tag resolves to now (`docker buildx imagetools inspect <image>`) and the upstream release it ships — needed for `references/criteria.md` §4.6 (addendum "Version & Update Integrity (§4.6)")
```

**3e — Tier 1 + quick scope.** Replace the two paragraphs from `Use when ALL Tier 1 criteria from the addendum are met:` through `…proceed directly to Subject Verdict Notes with minimal ceremony.` with:
```markdown
Use when ALL Tier 1 criteria from the addendum are met and `references/criteria.md` §4.6 raises nothing that bars Tier 1: Docker Official Image, hardened-catalog image, Verified Publisher (or equivalent GHCR/Quay publisher verification); digest-pinned reference — or, on a dev workstation only, a Docker Official / hardened-catalog tag resolved to a recorded digest (a semver tag alone never qualifies); identity verified per §4.6 V2 (matched signature or attestation, or the Docker Official Images curated-pipeline checks); SBOM available; no CRITICAL and no Blocking CVE on the resolved digest; recognized minimal or hardened base; default-safe runtime (root at runtime only on a dev workstation).

**Quick audit scope:** Confirm publisher + identity checks + SBOM availability + CVE scan of the resolved digest + §4.6 version age. Note the base image. No deep layer walk. If everything checks out, proceed directly to Subject Verdict Notes with minimal ceremony.
```

**3f — Tier 2 bullets.**
```markdown
// Before:
- Named tag (e.g., `nginx:1.27`) without digest pin
- No signing or unknown signing status
// After:
- Named tag (e.g., `nginx:1.27`) without digest pin, or production `:latest` on a Docker Official / hardened-catalog image
- No verified identity (unsigned, identity unmatched, or curated-pipeline attestations not checkable)
```

**3g — Tier 3 triggers + deep scope.** Replace the two paragraphs from `Any Tier 3 trigger from the addendum:` through `…runtime-manifest audit (privileged, cap-add, hostPid, hostNetwork, mount paths).` with:
```markdown
Any Tier 3 trigger from the addendum: `:latest` / no tag with no digest pin (except Docker Official and hardened-catalog images); unknown or self-hosted registry; critical-risk runtime flag (`--privileged`, dangerous capability adds, `docker.sock` or host-root mounts) or host namespaces; image older than 2 years with no rebuild; Blocking CVE, or an unfixed CRITICAL in an OS / base layer; §4.6 V3 HIGH flag (tag moved with no upstream release, provenance or signer mismatch); scraped/mirror registry; suspicious naming (impersonates a well-known project or publisher); no publisher identity; `FROM` chain that transits an unknown base.

**Deep audit scope:** Full Tier 2 work + identity-matched signature and attestation verification (§4.6 V2; transparency-log inclusion where the publisher uses it), provenance check (source repo, workflow, SLSA level, build reproducibility), §4.6 V3 diff against the previous release, full layer CVE + secret scan with a pinned Trivy/Grype, Dockerfile audit for secrets / `curl | bash` / privilege escalation patterns, and runtime-manifest audit (privileged, cap-add, hostPid, hostNetwork, mount paths, user namespaces).
```

**3h — Research questions 2, 3, 4, 6, 8.** Replace each numbered line whole:
```markdown
2. **Is the reference pinned by digest?** Tags are mutable — `:latest`, `:1.27` and even `:1.27.3-alpine` can be re-pushed by the publisher or by anyone holding its credentials. A digest (`@sha256:...`) is immutable. A tag counts as immutable only where the registry enforces it and the setting is visible (addendum "Tag vs Digest Pinning"). Unpinned references mean every pull can deliver different content; record the digest the tag resolves to now.
3. **Is the image signed, and by whom?** Verify against the expected identity (§4.6 V2): keyless Cosign with `--certificate-identity` + `--certificate-oidc-issuer`, keyed Cosign with the publisher's key, `gh attestation verify oci://…`, or `notation verify` (addendum "Signing Standards"). Keyless `cosign verify` without identity flags errors — that is not "unsigned". Docker Official Images have no user-verifiable signature: use the curated-pipeline checks. For Docker Hub, absence of signing is common but is a Tier 2 flag on a privileged workload.
4. **Is there an SBOM?** A signed SBOM attestation (`cosign verify-attestation --type spdxjson|cyclonedx`), a BuildKit SBOM attestation (`docker buildx imagetools inspect <image> --format '{{json .SBOM}}'`), `docker scout sbom`, or a local `syft <image>` scan should yield an SPDX or CycloneDX document. Absence is a gap, not automatic rejection — but an available SBOM is a Tier 1 requirement.
6. **What CVEs affect the image?** Scan the resolved digest with registry-side data (Docker Scout, GHCR / Quay tabs) and a pinned local scanner (Trivy/Grype; `references/criteria.md` audit-tooling note). Split HIGH/CRITICAL findings into own code vs OS / base / language-dependency layers and fixable vs unfixable, check CRITICALs against CISA KEV, and apply qualifying VEX `not_affected` statements (addendum "CVE Scope (§4.3)").
8. **What is the image's provenance?** Is there a verifiable build attestation — GitHub artifact attestation (`actions/attest-build-provenance`, verified with `gh attestation verify`), signed SLSA provenance, or BuildKit provenance — and do its source repo + workflow match the publisher's public source? Is the Dockerfile source public and the build reproducible? Are the layers minimal and explainable?
```

**3i — Signature check block.** Replace from `**Signature check** (Tier 2 and Tier 3):` through the line `If tooling is unavailable, check the registry web UI for a signatures tab (…).` with:
```markdown
**Signature and identity check** (Tier 2 and Tier 3; Tier 1 brief):

Use the commands in `references/criteria/container-image.md` "Signing
Standards", always on the resolved digest and always with the expected
identity (§4.6 V2):

- Keyless Cosign: `cosign verify <image>@<digest> --certificate-identity <SAN> --certificate-oidc-issuer <issuer>`
- Keyed Cosign / hardened catalogs: `cosign verify <image>@<digest> --key <publisher key>`, or the publisher's own verify command (Docker Hardened Images: `docker scout attest get … --verify`)
- Attestations: `cosign verify-attestation --type slsaprovenance` with identity flags, or `gh attestation verify oci://<image>@<digest> --owner <org>`
- BuildKit attestations: `docker buildx imagetools inspect <image> --format '{{json .Provenance}}'` — unsigned; Docker Official Images use them through the curated-pipeline checks
- `notation verify <image>@<digest>` if the publisher uses Notary v2

Do not use Docker Content Trust: it is retired, and `DOCKER_CONTENT_TRUST=1`
breaks Docker Official Image pulls. Record the expected identity, its
source, and the identity the check returned. If tooling is unavailable,
check the registry web UI (GHCR shows package attestations on the package
page) and rate identity as unverified.
```

**3j — SBOM check block.** Replace from `**SBOM check** (Tier 2 and Tier 3):` through `…SBOM absence on a Tier 3 subject is a flag.` with:
```markdown
**SBOM check** (Tier 2 and Tier 3):

- `cosign verify-attestation <image>@<digest> --type spdxjson|cyclonedx` + identity flags — signed SBOM attestation
- `docker buildx imagetools inspect <image> --format '{{json .SBOM}}'` — BuildKit SBOM attestation (unsigned)
- `docker scout sbom <image>` — Docker's SBOM fetch
- `syft <image> -o spdx-json` — generates an SBOM from the image layers locally (pinned tool version)

`cosign download sbom` is deprecated and its attachments are unsigned; do not cite it as publisher-attested evidence. Record SBOM format (SPDX, CycloneDX), source (signed attestation, BuildKit, Scout, local), and package count. SBOM absence on a Tier 3 subject is a flag.
```

**3k — CVE scan block.** Replace from `**CVE scan** (all tiers):` through `Record critical + high counts, whether patches are available, and how fresh the advisory feed is.` with:
```markdown
**CVE and secret scan** (all tiers):

- Registry-side data: Docker Scout on Docker Hub (`docker scout cves <image>` applies image VEX automatically), GHCR / Quay vulnerability tabs
- `trivy image <image>@<digest>` / `grype <image>@<digest>` — pinned versions per the `references/criteria.md` audit-tooling note; add `--vex <file>` for publisher or maintainer VEX
- `trivy image --scanners secret <image>@<digest>` — secrets baked into layers (Tier 2 spot-check, Tier 3 required)

Record for each HIGH/CRITICAL: layer class (own code vs OS / base / language dependency), fixed version or none, KEV status for CRITICALs, and any VEX `not_affected` with its source. Rate per the addendum "CVE Scope (§4.3)". Note how fresh the advisory feed is.
```

**3l — Layer bullet.** Before: `- \`USER root\` (or no \`USER\` at all — defaults to root)`. After: `- \`USER root\` (or no \`USER\` at all — defaults to root); then read the entrypoint for a privilege drop (\`gosu\`, \`su-exec\`, \`setpriv\`) before rating root at runtime`.

**3m — Runtime audit positives.** After the line `- \`allowPrivilegeEscalation: true\` — bypass the no-new-privs bit` insert:
```markdown
- Positive signals: `hostUsers: false` (Kubernetes user namespaces), rootless runtime, namespace Pod Security Standard `restricted`, `seccompProfile: RuntimeDefault`
```

**3n — Provenance block.** Replace the 5 bullets under `**Provenance and reproducibility** (Tier 3):` (from `- Is the Dockerfile source public (GitHub, GitLab)?` through `- Is the build reproducible (same source → same digest)?`) with:
```markdown
- Is the Dockerfile source public (GitHub, GitLab)?
- Which build attestation exists (GitHub artifact attestation, signed SLSA provenance, BuildKit provenance), and do its source repo + workflow + ref match the publisher's public source (§4.6 V2)?
- Do the tags correspond to releases or git tags on the source repo? A tag with no matching upstream release is a §4.6 V3 HIGH flag
- Compared with the previous release's digest, did the source repo, workflow, signer or image config change (§4.6 V3)?
- Is the build reproducible (same source → same digest)?
```

**3o — Coverage table.** Replace the table rows from `| Registry metadata / manifest | Required | Required | Required |` through `| Web search — incidents & compromise | Brief | Required | Required |` with:
```markdown
| Registry metadata / manifest | Required | Required | Required |
| Publisher verification | Required | Required | Required |
| Signature / attestation identity (§4.6 V2) | Brief | Required | Required |
| SBOM presence | Brief | Required | Required |
| CVE / advisory scan (resolved digest; KEV, VEX) | Required | Required | Required |
| Version integrity (§4.6) | Required | Required | Required |
| Base image lineage | Brief | Required | Required |
| Dockerfile / layer audit (incl. secret scan) | Tier-skip | If available | Required |
| Runtime config audit (privileged, caps, host*) | Brief | Required | Required |
| Provenance / SLSA attestation | Optional | If available | Required |
| Tag vs digest pinning | Note | Required | Required |
| Web search — incidents & compromise | Brief | Required | Required |

Also keep every Required row of the canonical table in
`references/criteria.md`; none is dropped. Container mappings:
**Typosquat / name verification** → the namespace impersonation check;
**License compatibility** → the main application's license
(`org.opencontainers.image.licenses` or upstream); **Maintainer / activity
/ health** → last push and rebuild cadence; **OpenSSF Scorecard** → the
`org.opencontainers.image.source` repo, else `Not available`; **Dependency
tree / transitive risk** → SBOM + layer CVE scan; **Install script review**
→ `N/A (image)`; **Source code review** → Dockerfile / layer audit.
```

**3p — Subject Rubric 4.1.** Replace three bullets whole:
```markdown
- **Image reference shape**: Digest-pinned (`@sha256:...`) is strong; a tag in a registry that visibly enforces tag immutability is moderate; any other tag — specific (`:1.27.3-alpine`), floating (`:1.27`) or `:latest` — is mutable and weak, and `:latest` with no digest is weakest.
- **Signing chain**: A signature or attestation verifies **and** names the expected identity (§4.6 V2), or the image is a Docker Official Image that passes the curated-pipeline checks (addendum "Version & Update Integrity (§4.6)"). Presence without a matched identity earns no credit. Absence of signing is not automatic rejection but is a gap.
- **Build provenance**: A verifiable provenance attestation whose source repo + workflow match the publisher's public source, a reproducible build from public Dockerfile source, or a public CI build log — any one raises confidence sharply. Provenance naming an unexpected repo is a §4.6 V3 HIGH flag.
```
(Replaces the bullets starting `- **Image reference shape**:`, `- **Signing chain**:`, `- **Build provenance**:`.)

**3q — 4.2.** After the bullet starting `- **Abandoned images**:` insert:
```markdown
- **Frozen namespaces**: A publisher notice that a namespace gets no further updates (e.g. `bitnamilegacy`) makes every image in it abandoned regardless of badge or pull count → HIGH flag `frozen namespace` (addendum Registry Trust Signals).
```

**3r — 4.3 (C6).** Replace the bullet starting `- **Critical/high CVEs**: Count unpatched critical + high CVEs` with:
```markdown
- **Critical/high CVEs**: Count critical + high CVEs on the resolved digest from Trivy / Grype / Scout / Clair, after qualifying VEX. Rate per `references/criteria.md` §4.3 and the addendum "CVE Scope (§4.3)": a KEV-listed CRITICAL in any layer, or an unfixed HIGH/CRITICAL in the image's own code, is a Blocking CVE → REJECTED; every other HIGH/CRITICAL (fix available, or in OS / base / language-dependency layers) is a HIGH flag → CONDITIONAL.
- **Secrets in layers**: Credentials found by the layer secret scan or in `ENV` → HIGH (addendum Layer Risk Patterns).
```

**3s — 4.4 (C4, C7).** Replace four bullets whole:
```markdown
- **Root at runtime**: `USER root`, or no `USER` with no verified entrypoint privilege drop (`gosu` / `su-exec` / `setpriv`). Dev workstation → LOW note; production or any other non-dev workload → HIGH flag → CONDITIONAL (addendum Layer Risk Patterns).
- **Linux capabilities**: Default Docker drops most caps. `--cap-add=NET_ADMIN`, `SYS_ADMIN`, `SYS_PTRACE`, `DAC_OVERRIDE` each need justification. `SYS_ADMIN` is effectively root-equivalent. User namespaces (`hostUsers: false`) or a rootless runtime lower high-risk caps one step.
- **`--privileged`**: Grants all capabilities and disables most isolation. On an image whose identity does not verify (§4.6 V2) → CRITICAL; on a verified-publisher image → HIGH flag → CONDITIONAL (drop it, or isolate the host for a documented need such as DinD on a private CI runner).
- **Volume mounts**: `/var/run/docker.sock` mounted into the container is container-escape-equivalent (can spawn other containers on the host). `/` or `/etc` or `/proc` mounts are similar; both are rated like `--privileged`. Scoped read-only mounts of specific config paths are low-risk.
```
(Replaces the bullets starting `- **USER instruction**:`, `- **Linux capabilities**:`, `- **\`--privileged\`**:`, `- **Volume mounts**:`.)

**3t — 4.6 heading + bullets.** Before: `### 4.6 Supply Chain (container-image-specialized)`. After:
```markdown
### 4.6 Supply Chain & Version Integrity (container-image-specialized)

- **Version integrity floor**: `references/criteria.md` §4.6 applies to the resolved digest; its container plug-ins (version unit, curated pipelines, release diff, triggers) are in the addendum "Version & Update Integrity (§4.6)". A Docker Official Image rebuild of the same upstream release is the same version; a new upstream release is a new version.
- **Tag moves**: A tag that now points at content with no matching upstream release, or provenance that names a different or newly created repo, is a §4.6 V3 HIGH flag (the 2026 trusted-publisher tag-overwrite pattern). Condition: pin the last digest that passes V3.
```
Then, after the existing bullet starting `- **Transitive base CVEs**:`, append:
```markdown
- **Digest refresh**: A pinned digest freezes its CVEs too. Recommend a refresh cadence (bot-driven digest updates with a release-age gate), auditing each new digest.
```

**3u — Toward REJECTED.**
```markdown
// Before:
- **Unpatched critical CVE with exploit available** in the image or a direct base layer, with no alternative tag available
// After:
- **Blocking CVE** in the resolved digest (`SKILL.md` Tree terms; addendum "CVE Scope (§4.3)"): a KEV-listed CRITICAL in any layer, or an unfixed HIGH/CRITICAL in the image's own code
- **Version-scoped compromise**: the resolved digest is in a confirmed compromise's affected range, or the compromise is unresolved (`references/criteria.md` §4.6 V4 case a)

// Before:
- **`--privileged` requested on an unverified/untrusted image**: Combining maximum host access with no signing / no SBOM / no provenance is a near-automatic rejection
// After:
- **Critical-risk runtime flag on an image whose identity does not verify**: `--privileged`, `--cap-add=SYS_ADMIN`, `/var/run/docker.sock` or host `/`, `/etc`, `/proc`, `/sys`, `/dev` mounts with no verified signer or curated pipeline (§4.6 V2) → CRITICAL
```

**3v — Toward CONDITIONAL.**
```markdown
// Before:
- **`:latest` tag from a trusted publisher**: Condition — pin to the current digest (`<image>@sha256:<hex>`), document it, re-audit on upgrade
- **Trusted image without a Cosign signature**: Condition — understand the signing gap; if org policy requires signatures, either skip the image or request signed variant from publisher
- **Base image has known CVEs but no patched variant yet**: Condition — apply workloads-level mitigations (network policy, seccomp, minimal mounts); re-audit when patched
// After:
- **`:latest`, no tag, or any non-digest tag in production from a trusted publisher**: Condition — pin to the current digest (`<image>@sha256:<hex>`), document it, re-audit per `references/criteria.md` §4.6 V5. (On a dev workstation this is a LOW note when the digest is recorded and pinned in the Recommendation.)
- **Trusted image without a verifiable signature** (other than a Docker Official Image passing the curated-pipeline checks): Condition — understand the signing gap; if org policy requires signatures, either skip the image or request signed variant from publisher
- **HIGH/CRITICAL CVE that is not blocking** (fix available, or unfixed in OS / base / language-dependency layers; not KEV; no qualifying VEX): Condition — pull or rebuild a digest with the fix where one exists; otherwise apply workload mitigations (network policy, seccomp, minimal mounts, non-root) and re-audit when patched

// Before:
- **Rootful image on developer workstation**: Condition — run under rootless Docker / Podman, or map container UID to an unprivileged host user
// After:
- **Root at runtime in production or another non-dev workload**: Condition — set a non-root `USER` / `runAsNonRoot: true`, run under rootless Docker / Podman, or enable user namespaces (`hostUsers: false`). (On a dev workstation: LOW note only.)
- **Critical-risk runtime flag on a verified-publisher image**: Condition — drop the flag, or document the need and isolate the host (dedicated CI runner, no secrets)
- **Frozen / legacy namespace** (e.g. `bitnamilegacy/*`): Condition — move to a maintained source
- **§4.6 flags** (fresh version, V3 continuity break): conditions per `references/criteria.md` §4.6
```

**3w — Toward APPROVED.** Replace the six bullets from `- All tier-appropriate checks completed with no flags` through `- Base image is a recognized minimal base (distroless, alpine, debian-slim, ubi-micro) at a recent version` with:
```markdown
- All tier-appropriate checks completed with no flags above LOW (LOW notes such as root at runtime on a dev workstation are compatible)
- Digest-pinned reference, or — dev workstation only — a tag whose resolved digest is recorded and pinned in the Recommendation; publisher is Docker Official, a hardened catalog, a Verified Publisher, or a recognized GitHub org
- Identity verified per §4.6 V2 (matched signature or attestation, or the Docker Official Images curated-pipeline checks); SBOM available
- No Blocking CVE and no other HIGH/CRITICAL left after qualifying VEX
- Not root at runtime (non-root `USER` or verified entrypoint privilege drop) — or root on a dev workstation only; no `--privileged`; no unnecessary `cap_add`
- Base image is a recognized minimal or hardened base (distroless, alpine, debian-slim, ubi-micro, Docker Hardened Images, Chainguard / Wolfi) at a recent version, or a `FROM` chain of Docker Official Images
```
(The "Multi-arch manifest" and "Public Dockerfile source" bullets stay.)

**Rationale:**
- **The workflow mirrors the addendum, it doesn't restate it.** Each rule points at an addendum section name, so a future stewardship pass edits facts in one file.
- **The 4.6 heading is renamed rather than renumbered.** That keeps the workflow's 4.1–4.6 rubric numbering aligned with `criteria.md`, whose §4.6 now exists, and makes it the natural home for the floor pointer.
- **The coverage mapping sentence** satisfies the shared "never drop a Required row" contract without padding the table with 7 rows that mostly map onto existing container rows.
- **3w "no flags above LOW"** is required by C4. With "no flags", the decided LOW root-on-dev note would block APPROVED for eval 26.

**Verification:**
```bash
F=workflows/container-image.md
grep -ci "docker_content_trust=1 docker pull\|slsa-framework/slsa-github-generator\|near-automatic rejection\|default rejection on developer workloads\|rootful image on developer workstation\|high cves have documented mitigations\|unpatched critical cve\|specific immutable\|google container registry / artifact registry" $F   # 0
grep -c "| Version integrity (§4.6) | Required | Required | Required |" $F   # 1
grep -c "^### 4\.6 Supply Chain & Version Integrity" $F                      # 1
grep -c "^## Identify$\|^## Subject Rubric — Evaluate$\|^## Subject Verdict Notes$\|^### Toward REJECTED$\|^### Toward CONDITIONAL$\|^### Toward APPROVED$" $F   # 6
```

**If this fails:** `git -C <work-root> checkout -- workflows/container-image.md` and redo 3a–3w.

---

### Step 4: `references/criteria.md` §4.4 Docker block (C7 shared leg)

**Objective:** make the shared Docker summary agree with the addendum (C7, C4 root rule). Touch no other line of the file.
**Confidence:** High
**Depends on:** Step 2
**Do-Projex:** Encouraged

**Files:** `references/criteria.md`

**Changes:**
```markdown
// Before:
### Docker Image Permissions
- `USER root` with no later `USER` switch → flag
- `--privileged` in run instructions → flag
- Mounting `/var/run/docker.sock` → CRITICAL (container escape)
- Capabilities: `SYS_ADMIN`, `NET_ADMIN` → flag unless justified

// After:
### Docker Image Permissions
Ratings live in `references/criteria/container-image.md` (Layer Risk Patterns, Runtime Privilege Classification); summary:
- Root at runtime (`USER root`, or no `USER` and no verified entrypoint privilege drop) → LOW note on a dev workstation; HIGH flag → CONDITIONAL in production or other non-dev use
- Critical-risk runtime flag (`--privileged`, `--cap-add=SYS_ADMIN`, mounting `/var/run/docker.sock` or host `/`, `/etc`, `/proc`, `/sys`, `/dev`) → CRITICAL on an image whose identity does not verify (§4.6 V2); HIGH flag → CONDITIONAL on a verified-publisher image
- Other added capabilities (`NET_ADMIN`, `SYS_PTRACE`, `DAC_OVERRIDE`, …) and host namespaces → flag unless justified
```

**Rationale:** the old block was the third grading in C7 ("docker.sock → CRITICAL" regardless of publisher). A summary plus a pointer keeps `criteria.md` readable for non-container audits, and the addendum stays authoritative.

**Verification:** `git -C <work-root> diff -U0 references/criteria.md` shows hunks only inside `### Docker Image Permissions`. `grep -c "CRITICAL on an image whose identity does not verify" references/criteria.md` → 1.

**If this fails:** `git -C <work-root> checkout -- references/criteria.md`.

---

## Verification Plan

### Automated Checks

- [ ] `python3 evals/run_evals.py validate` passes; `python3 -m unittest discover -s evals -p "test_*.py"` passes with the Preflight count.
- [ ] Consistency script (run from `<work-root>`; not committed):
```bash
python3 - <<'EOF'
import re, pathlib
A = pathlib.Path("references/criteria/container-image.md").read_text(encoding="utf-8")
W = pathlib.Path("workflows/container-image.md").read_text(encoding="utf-8")
C = pathlib.Path("references/criteria.md").read_text(encoding="utf-8")
assert C.count("## 4.6 Version & Update Integrity (shared floor)") == 1
for f, t in {"A": A, "W": W, "C": C}.items():
    for v in re.findall(r"§4\.6 (V\d)", t):
        assert v in {"V1","V2","V3","V4","V5"}, (f, v)
assert A.count("\n## CVE Scope (§4.3)\n") == 1 and A.count("\n## Version & Update Integrity (§4.6)\n") == 1
for v in "12345":
    assert len(re.findall(rf"^- \*\*V{v} ", A, re.M)) == 1, v
assert "**Curated pipelines:** Docker Official Images" in A
stale = ["mostly immutable by convention", "specific immutable", "slsa-framework/slsa-github-generator",
         "default rejection on developer workloads", "any one critical-risk flag on an unverified image",
         "high cves have documented mitigations", "unpatched critical cve", "rootful image on developer workstation",
         "still present for some older docker official tags", "google container registry / artifact registry",
         "docker_content_trust=1 docker pull", "no critical cves from scanner", "near-automatic rejection",
         "medium note on dev/experimental", "docker hub shows signatures"]
for name, t in {"A": A, "W": W}.items():
    low = t.lower()
    for s in stale:
        assert s not in low, (name, s)
    assert "`cosign verify <image>`" not in t, name
    for line in t.splitlines():
        if "cosign download sbom" in line: assert "deprecated" in line, (name, line)
        if "DOCKER_CONTENT_TRUST" in line: assert "retired" in line.lower(), (name, line)
assert "| Version integrity (§4.6) | Required | Required | Required |" in W
assert "CRITICAL on an image whose identity does not verify" in C
assert "= CRITICAL → REJECTED" in A and "On an image whose identity does not verify (§4.6 V2) → CRITICAL" in W
print("OK")
EOF
```
- [ ] `git -C <work-root> diff --stat <base>..HEAD` lists exactly the 3 files.

### Manual Verification (paper traces)

Walk each case through `SKILL.md` Step N + `criteria.md` §4.3/§4.6 + the refreshed container files, and log the cited rule at each hop.

| # | Case | Expected |
|---|---|---|
| T1 | eval 26 `docker pull redis`, dev. Premises: DOI provenance attestation present; no new upstream redis release < 7 d; no HIGH/CRITICAL after VEX | Not Tier 3 (`:latest` DOI exception). Tier 1: DOI ✓; dev tag + recorded digest ✓ (LOW note); curated pipeline ✓; SBOM ✓; CVEs ✓; base debian-slim / DOI chain ✓; runtime: entrypoint `gosu` drop → not root (else LOW note) ✓ → **Tier 1, APPROVED** (C4) |
| T1b | As T1, attestations not checkable | Tier 2; identity unverified → LOW note (DOI); no flag above LOW → **APPROVED** reachable |
| T1c | As T1, one unfixed OS-package HIGH (not KEV, no VEX) | §4.3 third-party → HIGH flag → **CONDITIONAL** (C6 wins; see Eval hand-off) |
| T2 | eval 12 `nginx:latest`, production | DOI exception → Tier 2; `:latest` prod HIGH → **CONDITIONAL**; Recommendation pins the digest (assertion "digest or immutable tag" ✓) |
| T3 | eval 13 `someunknownregistry.io/cryptominer:latest` | Tier 3; no identity; suspicious name → **REJECTED** |
| T4 | eval 38 `acmecorp/invoice-api`, unsigned | Tier 2; no identity credit; baked npm CVEs = third-party → HIGH → **CONDITIONAL** (accepted) |
| T5 | KICS-style: Verified Publisher semver tag repointed; no upstream release; provenance names a 1-day-old repo | V2 unmatched → no credit; V3 HIGH → Tier 3 → **CONDITIONAL** (pin last good digest); with a confirmed advisory → V4 (a) → **REJECTED** |
| T6 | Unknown-publisher image + `-v /var/run/docker.sock:/var/run/docker.sock` | Addendum CRITICAL → `SKILL.md` node 1 → **REJECTED**. `criteria.md` §4.4 agrees |
| T7 | `docker:dind` (DOI, curated checks pass) + `--privileged` on CI | Verified publisher → HIGH → **CONDITIONAL** (isolated runner) |
| T8 | DHI image, digest-pinned; default `cosign verify` reports "not found in transparency log"; `docker scout attest get … --verify` passes | V2 verified (key) → Tier 1 possible; VEX applied → **APPROVED** reachable |
| T9 | Debian-based image, unfixed OS HIGH; then same with a distribution VEX `not_affected` naming the package version + justification | → **CONDITIONAL**; with VEX → CVE excluded → APPROVED reachable |
| T10 | KEV-listed CRITICAL in an OS package, fix in a newer digest | Blocking CVE → **REJECTED**; Recommendation names the fixed digest |
| T11 | `bitnamilegacy/postgresql:16` | Frozen namespace HIGH → **CONDITIONAL** (move to maintained source) |
| T12 | DOI `postgres` in production, entrypoint drop verified; same image with `--user 0` override | No root flag → no change; with override → root at runtime prod → HIGH → **CONDITIONAL** |

### Acceptance Criteria Validation

| Criterion | How to Verify | Expected Result |
|---|---|---|
| Plug-in sections + V1–V5 bullets | Step 2 greps; consistency script | 2 headings; 1 each; `OK` |
| §4.6 refs resolve | consistency script | `OK` |
| Stale commands/phrases gone | Step 1/3 greps; script | 0; `OK` |
| C7 one rule in 3 files | script asserts; T6–T7 | `OK`; traces match |
| C4 encoded | T1, T1b, T2 | Tier 1 APPROVED; APPROVED; CONDITIONAL |
| C6 encoded | T1c, T9, T10 | CONDITIONAL; CONDITIONAL / APPROVED; REJECTED |
| Coverage contract | script | `OK` |
| Harness green | validate + unittest | pass; same count |
| Only 3 files; `criteria.md` hunk-scoped | `git diff --stat`; `diff -U0` | 3 files; §4.4 Docker block only |

---

## Rollback Plan

1. Before close: `projex-abandon.sh <repo-root> claude/youthful-dijkstra-5ov1kt projex/2610162004-container-image-rubric-refresh --worktree`. Base is untouched.
2. After squash-close: `git -C <repo-root> revert <squash-sha>` (one commit, 3 files). The shared floor stays valid without the container plug-ins: a missing plug-in means the shared default applies.

---

## Notes

### Eval hand-off (for the eval-refresh plan; `evals/` not edited here)

- **Eval 26** (`redis`, exact APPROVED). The rubric now reaches Tier 1 → APPROVED under T1's premises. Two premises are time- or state-dependent:
  - (a) a new upstream redis release < 72 h old → V1 → CONDITIONAL. Add eval 26 to the shared plan's time-dependent list (0, 11, 16, 18, 20, 22, 36, 37).
  - (b) an unfixed OS-package HIGH/CRITICAL in the current `redis` digest → CONDITIONAL under C6 (T1c).
  The two human decisions ("eval 26 stays APPROVED" and C6) collide in case (b). The eval plan must choose one of three options:
  - accept `[APPROVED, CONDITIONAL]` when the only conditions are CVE mitigations or cooldown;
  - pin a known-clean digest in the prompt;
  - escalate to the human.
  Also update the description: "Tier 1 (Tier 2 if DOI attestations cannot be checked)"; "implicit latest is standard for dev use" → "dev use; audit records and pins the resolved digest".
- **Eval 12** (`nginx:latest`). Its description recommends "an immutable tag (`nginx:1.27.3-alpine`)", which contradicts C1, so change it to digest-only. The assertion "pinning to a specific digest or immutable tag" still passes. "Standard/Tier 2" now matches the rubric (DOI exception).
- **New cases** (from review §5.E + this plan): KICS-style tag overwrite → not APPROVED (T5) | DHI image digest-pinned → APPROVED (T8) | docker.sock + unknown publisher → REJECTED (T6) | `bitnamilegacy/*` → CONDITIONAL (T11) | Debian image with unfixed OS HIGH → CONDITIONAL, then with VEX → APPROVED (T9) | root in production → CONDITIONAL (T12).

### Other hand-offs

- `references/registries.md` §Container Images (registry-package plan or a patch): suggest rows "Docker Hardened Images (`dhi.io`) | High" and "Frozen / legacy namespaces (e.g. `bitnamilegacy`) | Low (no updates)". Its line "Image digest pinning preferred over tag pinning" is already consistent.
- `STEWARDSHIP.md` container row Watch column (orchestrator): add "DOI signing replacement (Docker announced one after DCT; none confirmed as of 2026-10) | DHI verification flow | cosign/`gh attestation` flag changes".
- Sibling addenda: the §4.3 plug-in heading `## CVE Scope (§4.3)` matches the browser-extension and ci-action sibling plans, so the name is the same across addenda.

### Risks

- **DOI attestation coverage unverified** (Verified facts row 4). Mitigation: A4 makes Tier 1 conditional on a check the auditor runs. If the check is absent, the audit falls to Tier 2 and the verdict is unchanged.
- **Curated-pipeline check (3) shape.** What DOI provenance names as builder/source is inferred from `provenance.jq` (workflow repo), not observed on a live digest. Mitigation: check 3 accepts the `docker-library` org or the image's Hub-linked source repo, and tells the auditor to record what it names. Stewardship should re-check it once DOI signing ships.
- **Docker ships DOI signing.** Docker said it would follow DCT's retirement with a replacement. If it ships, the curated-pipeline path still works, but a matched signature becomes available. Mitigation: STEWARDSHIP watch item above.
- **Command flags rot** (cosign v3 bundle/referrer defaults, Scout flags). Mitigation: the addendum header carries "as of 2026-10" and "confirm flags with `--help`"; flag names live only in the Signing table and the plug-in.
- **A2 conservative reading** (CI = production) may surprise users auditing CI images. Mitigation: it's a one-phrase change in 4 places, and it's recorded here.
- **Merge with the browser plan on `criteria.md` §4.4.** Different hunks; rebase before close.

### Open Questions

None. C4/C6 are decided; interpretation choices are recorded as A2–A4; the eval 26 × C6 collision is handed to the eval plan with options.

### Split Decision

`No split — heuristic tripped but steps tightly coupled`. The plan is ~86 KB (> 50 KB), but it has 4 steps, so the auto-split heuristic (size **and** > 5 steps) does not fire. Most of the size is verbatim After-text, so execution doesn't have to improvise. It covers one `.projex/` scope and is all spec-level prose, with no upstream/downstream mix. Step 3 and Step 4 cite section names and rules Steps 1–2 create, and splitting them would leave the workflow citing sections that don't exist yet.

### Revision Log

| Date | Trigger | Change |
|---|---|---|
| 2026-10-16 | Initial | C1–C9, C4/C6 per human decisions, container X1/X3, coverage contract |
