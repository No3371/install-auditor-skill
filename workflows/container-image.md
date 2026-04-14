<!--
workflows/container-image.md - Type 4 subject-specific workflow.
Handles OCI/Docker container images from Docker Hub, GHCR, Quay, ECR, GCR,
and other registries, whether pulled directly (`docker pull`), referenced
from a Dockerfile (`FROM`), or declared in Compose / Kubernetes manifests.

This workflow replaces workflows/generic.md for Type 4 subjects. After
producing findings here, return to SKILL.md Step N for the shared verdict
tree and report shape. The Audit Coverage table and audit-confidence
assertion are owned by the dispatcher — do not duplicate them here.

Phase 3 / M3.2 — third subject-specific workflow (second Phase 3).
-->

# Container Image Workflow (Type 4)

This workflow handles **Type 4: container-image** subjects — OCI/Docker
images distributed via Docker Hub, GitHub Container Registry (GHCR), Quay,
Amazon ECR, Google Container Registry / Artifact Registry (GCR/GAR), or any
other OCI registry. It specializes the generic evidence acquisition and
scoring pipeline for container concerns: signing (Cosign/Sigstore), SBOM
presence, base image lineage, tag vs digest pinning, layer CVEs, and
runtime privilege.

After completing all sections below, return to `SKILL.md` Step N for the
shared verdict tree and audit-coverage report shape.

Sections follow the standard workflow template: **Identify / Evidence /
Subject Rubric / Subject Verdict Notes**.

## Identify

### 1. Determine the registry and image identity

| Registry | URL / pull pattern | Trust notes |
|----------|--------------------|-------------|
| Docker Hub | `docker.io/<ns>/<repo>:<tag>` or bare `<repo>:<tag>` | Largest catalog; "Docker Official" and "Verified Publisher" badges exist but most images have neither |
| GitHub Container Registry (GHCR) | `ghcr.io/<org>/<repo>:<tag>` | Org-scoped; inherits GitHub org identity; supports package attestations |
| Quay | `quay.io/<ns>/<repo>:<tag>` | Red Hat ecosystem; integrated Clair scanner; supports signed images |
| Amazon ECR | `<acct>.dkr.ecr.<region>.amazonaws.com/<repo>` (private) or `public.ecr.aws/<ns>/<repo>` | Private by default; AWS-authenticated pulls; public gallery exists |
| Google Container Registry / Artifact Registry | `gcr.io/<proj>/<repo>` (legacy) or `<region>-docker.pkg.dev/<proj>/<repo>` | Google-authenticated; Artifact Registry supersedes GCR |
| Other / mirror | `<host>/<ns>/<repo>:<tag>` | Self-hosted Harbor, mirror registries, scraped registries — lower baseline trust |

If the user provides a full pull command, extract registry + repo + tag +
digest (if any). If they provide only a repo name, assume Docker Hub and
flag the absence of an explicit registry as a data point.

### 2. Extract the image reference and metadata

- **Registry**: Host component (explicit or defaulted to `docker.io`)
- **Repository**: `<namespace>/<repo>` — maps to a publisher organization
- **Tag**: `latest`, `1.27`, `1.27.3-alpine`, etc. — tags are mutable
- **Digest**: `sha256:<hex>` — immutable content address (may be absent)
- **Publisher**: Docker Hub publisher, GitHub org, Quay org, or AWS account
- **Publisher badge**: "Docker Official Image", "Verified Publisher", "Sponsored OSS", GHCR "Publisher" linked to verified org
- **Adoption metric**: Docker Hub pull count, GHCR package downloads (if visible), stars on source repo

### 3. Gather required context

Collect before proceeding:

1. **Full image reference** — registry + repo + tag, and digest if pinned
2. **Intended runtime** — local Docker, Docker Compose, Kubernetes, Podman, ECS/EKS/GKE, CI runner, or one-shot `docker run`
3. **Dockerfile availability** — does the user have / can produce the image's Dockerfile (for self-built images) or a source `Dockerfile` for reproduction
4. **Stated purpose** — what the user needs this image for (web server, database, build tool, dev environment, CI step, etc.)
5. **Organization signing policy** — does the org require Cosign-signed images, admission controller enforcement (e.g., Kyverno, Connaisseur, Sigstore policy-controller), or does it permit unsigned pulls
6. **Runtime privilege profile** — will the container run rootful, rootless, with added capabilities, mount host paths, use `hostNetwork`/`hostPid`, or run `--privileged`

If any of 1–5 are missing, ask before proceeding. Item 6 is obtained during research if not immediately available.

## Evidence — Part A: Triage (Pick the Audit Tier)

Gather registry listing data via web search or registry API:
- Publisher name, Docker Official / Verified Publisher badge, GHCR org status
- Last pushed date for the tag (mutable tags update; old last-pushed is a staleness flag)
- Creation date of the image (from manifest labels or registry metadata)
- Pull count or adoption signal
- Brief search for `"<image>" CVE OR vulnerability OR compromise OR malicious` for prior incidents

Then apply the **container-image-specific tier thresholds** from
`references/criteria/container-image.md` (section "Tier Assignment
Thresholds"):

### Tier 1 — Quick Audit (well-known, high-trust)

Use when ALL Tier 1 criteria from the addendum are met: Docker Official Image OR Verified Publisher (or equivalent GHCR/Quay publisher verification); digest-pinned reference OR a specific immutable semver tag; Cosign signature present OR the image ships as a GitHub-attested build; SBOM attached (via `cosign download sbom`, `docker scout sbom`, or `syft`); no critical CVEs surfaced in the last 90 days; base image drawn from a curated list (distroless, alpine, debian-slim, ubi-micro — from official sources).

**Quick audit scope:** Confirm publisher verification + signing + SBOM presence + recent CVE scan. Note the base image. No deep layer walk. If everything checks out, proceed directly to Subject Verdict Notes with minimal ceremony.

### Tier 2 — Standard Audit (default)

Default depth when not all Tier 1 criteria hold:
- Named tag (e.g., `nginx:1.27`) without digest pin
- No signing or unknown signing status
- Popular but unverified publisher
- Known base image, but no explicit SBOM

Full registry metadata lookup, signature/SBOM check, CVE scan against the image digest, base image lineage, Dockerfile inspection if available, and runtime-config review.

### Tier 3 — Deep Audit (any red flag)

Any Tier 3 trigger from the addendum: `:latest` with no digest pin; unknown or self-hosted registry; rootful USER with requested `--privileged` or dangerous capability adds; image older than 2 years with no rebuild; unpatched critical CVEs; scraped/mirror registry; suspicious naming (impersonates a well-known project or publisher); no publisher identity; `FROM` chain that transits an unknown base.

**Deep audit scope:** Full Tier 2 work + signing chain verification (Cosign + transparency log / Rekor), provenance check (SLSA level, build reproducibility), full layer CVE scan with Trivy/Grype, Dockerfile audit for secrets / `curl | bash` / privilege escalation patterns, and runtime-manifest audit (privileged, cap-add, hostPid, hostNetwork, mount paths).

## Evidence — Part B: Research

### Core research questions (all tiers)

Answer every question that applies to the assigned tier:

1. **Who publishes this image?** Company, GitHub org, cloud vendor, community? Is the publisher verified by the registry (Docker Official, Verified Publisher, GHCR org-scoped, Quay verified)? Check for impersonation (same name, different namespace, or scraped mirror on an unknown host).
2. **Is the reference pinned by digest?** Tags are mutable — a `:latest` or even `:1.27` can be re-pushed. A digest (`@sha256:...`) is immutable. Unpinned references mean every pull can deliver different content.
3. **Is the image signed?** Cosign (`cosign verify <image>`) checks a Sigstore-backed signature + Rekor transparency log entry. Notation (notary v2) verification is an alternative. For Docker Hub, absence of signing is common but is a Tier 2 flag on a privileged workload.
4. **Is there an SBOM?** `cosign download sbom`, `docker scout sbom`, or `syft <image>` should yield an SPDX or CycloneDX document. Absence is a gap, not automatic rejection — but SBOM presence strongly raises Tier 1 eligibility.
5. **What is the base image chain?** Parse `FROM` from the Dockerfile (if available) or inspect labels (`org.opencontainers.image.base.name`, `org.opencontainers.image.base.digest`). Trace to the root base — distroless / alpine / debian-slim / ubi / scratch — and flag deep chains or unfamiliar bases.
6. **What CVEs affect the image?** Run Trivy/Grype if available, or consult Docker Scout advisories on Docker Hub, GHCR vulnerability tab, or Quay Clair. Cross-reference base-image CVEs via OSV. Note critical/high unpatched findings.
7. **What is the runtime configuration?** If a Dockerfile is available, inspect `USER`, `EXPOSE`, `ENV`, `HEALTHCHECK`, `ENTRYPOINT`. If a Compose / Kubernetes manifest is available, inspect `privileged`, `cap_add`, `hostNetwork`, `hostPID`, `hostIPC`, volume mounts (especially `/var/run/docker.sock`, `/`), and `securityContext` (`runAsUser`, `allowPrivilegeEscalation`).
8. **What is the image's provenance?** Is there a GitHub Actions build (SLSA provenance via `slsa-framework/slsa-github-generator`)? Is the Dockerfile source public and the build reproducible? Are the layers minimal and explainable?

### How to research

**Registry metadata lookup** (all tiers):

Use `docker buildx imagetools inspect <image>`, `skopeo inspect docker://<image>`, or `crane manifest <image>` to pull the image manifest without a full download. Extract:
- Created timestamp
- Labels (`org.opencontainers.image.*`): base image, source repo, revision, description
- Layer count and cumulative size
- Multi-arch manifest list (amd64, arm64, etc.)

For Docker Hub listings, web search the tag page and note the "Last pushed" date, Docker Official / Verified Publisher badge, pull count, and the "Tags" tab for available variants.

**Signature check** (Tier 2 and Tier 3):

- `cosign verify <image>` (Sigstore / keyless or keyed) — checks signature + Rekor transparency log inclusion
- `cosign verify-attestation <image> --type slsaprovenance` — checks build provenance attestation
- `notation verify <image>` if the publisher uses notary v2
- Docker Content Trust (`DOCKER_CONTENT_TRUST=1 docker pull`) for older notary v1 signatures (deprecated)

If tooling is unavailable, check the registry web UI for a signatures tab (Docker Hub shows signatures for some Verified Publisher images; GHCR shows package attestations on the package page).

**SBOM check** (Tier 2 and Tier 3):

- `cosign download sbom <image>` — retrieves an attached SBOM if one exists
- `docker scout sbom <image>` — Docker's built-in SBOM fetch
- `syft <image> -o spdx-json` — generates an SBOM from the image layers locally

Record SBOM format (SPDX, CycloneDX), tool that produced it (Syft, Trivy, anchore), and package count. SBOM absence on a Tier 3 subject is a flag.

**CVE scan** (all tiers):

- `trivy image <image>` — scans image layers + OS packages + language ecosystems
- `grype <image>` — similar coverage
- `docker scout cves <image>` — uses Docker's advisory feed
- Docker Hub advisory tab (for Official images and some Verified Publishers)
- GHCR / Quay vulnerability tabs when available

Record critical + high counts, whether patches are available, and how fresh the advisory feed is.

**Base image lineage** (Tier 2 and Tier 3):

Parse `FROM` from the Dockerfile if available. Otherwise, inspect labels (`org.opencontainers.image.base.name`) or compare layer digests against known base image digests (registry UI sometimes shows this). Flag:
- Deep chains (A from B from C from D from E) — each link adds surface
- Unfamiliar bases (random user image as the base layer)
- Ancient bases (Debian < 11, Ubuntu < 20.04, CentOS EOL variants)
- `FROM scratch` images that nevertheless include a full interpreter — inspect how that got in

**Layer and Dockerfile analysis** (Tier 3, spot-check for Tier 2):

Inspect Dockerfile (or layer history via `docker history <image>` / `crane config <image>`) for:
- `USER root` (or no `USER` at all — defaults to root)
- `COPY . .` that bundles secrets (credentials, `.env`, private keys) from the build context
- `ENV` with secret-looking values (tokens, passwords)
- `RUN curl <url> | sh` or `wget | bash` — opaque install pipelines
- `ADD <url>` — similar but worse (no verification)
- `chmod -R 777` — over-permissive permissions
- `apt-get install` without `--no-install-recommends` and without cleanup — bloated layers
- Suspicious binaries (`nc`, `ncat`, full `curl` + `wget` + shell in a minimal image)

**Runtime configuration audit** (Tier 2 and Tier 3):

If the user has a `docker run` command, Compose file, or Kubernetes manifest, inspect:
- `--privileged` / `privileged: true` — grants most host capabilities; requires strong justification
- `--cap-add` / `capabilities.add` — enumerate added caps, score each per `references/criteria/container-image.md`
- `--network host` / `hostNetwork: true` — bypasses Docker/k8s network namespace
- `--pid host` / `hostPID: true` — visibility into host processes
- Bind mounts (`-v /:/host`, `/var/run/docker.sock`, `/proc`) — container escape vectors
- `securityContext.runAsUser: 0` — explicit root
- `allowPrivilegeEscalation: true` — bypass the no-new-privs bit

**Provenance and reproducibility** (Tier 3):

- Is the Dockerfile source public (GitHub, GitLab)?
- Is the image built via GitHub Actions with SLSA provenance (`slsa-framework/slsa-github-generator`)?
- Do the tags correspond to git tags on the source repo?
- Does `cosign verify-attestation` surface a build provenance document?
- Is the build reproducible (same source → same digest)?

### Audit coverage tracking

Map evidence to the Audit Coverage rows expected by `SKILL.md` Step N. For
container images, the standard rows are:

| Check | Tier 1 | Tier 2 | Tier 3 |
|-------|--------|--------|--------|
| Registry metadata / manifest | Required | Required | Required |
| Publisher verification | Required | Required | Required |
| Signature verification (Cosign/Notary) | Brief | Required | Required |
| SBOM presence | Brief | Required | Required |
| CVE / advisory scan | Required | Required | Required |
| Base image lineage | Brief | Required | Required |
| Dockerfile / layer audit | Tier-skip | If available | Required |
| Runtime config audit (privileged, caps, host*) | Brief | Required | Required |
| Provenance / SLSA attestation | Optional | If available | Required |
| Tag vs digest pinning | Note | Required | Required |
| Web search — incidents & compromise | Brief | Required | Required |

## Subject Rubric — Evaluate

Score against the shared rubric in `references/criteria.md` AND the
container-image addendum in `references/criteria/container-image.md`. The
sections below specialize the shared criteria for container context.

### 4.1 Provenance & Identity (container-image-specialized)

- **Image reference shape**: Digest-pinned (`@sha256:...`) is strong; specific immutable tag (`:1.27.3-alpine`) is moderate; floating tag (`:1.27`) is weak; `:latest` with no digest is weakest.
- **Publisher identity**: Docker Official Image, Verified Publisher, GHCR org linked to a recognizable GitHub org, Quay verified publisher, or a known cloud vendor namespace (e.g., `public.ecr.aws/amazonlinux/...`).
- **Signing chain**: Cosign verification passes (with transparency-log inclusion via Rekor); or Notary v2 verification passes; or the publisher is Docker Official and the image is signed via Docker's official build pipeline. Absence of signing is not automatic rejection but is a gap.
- **Build provenance**: SLSA provenance attestation, reproducible build from public Dockerfile source, GitHub Actions build log — any one of these raises confidence sharply.
- **Impersonation check**: Similarly-named images under different namespaces on Docker Hub (e.g., `<user>/nginx` vs official `nginx`) are a red flag. Scraped mirror registries republishing popular images under a different host are also suspect.

### 4.2 Maintenance & Longevity (container-image-specialized)

- **Image age / last push**: Container images should be rebuilt periodically to pick up base-image CVE fixes. >6 months with no push on an actively-used image is stale; >2 years is abandoned.
- **Base image freshness**: Even if the image itself is recent, if its base (`FROM`) is an old Debian / Ubuntu / Alpine variant with unpatched CVEs, the image inherits that surface.
- **Update cadence**: Does the publisher ship patches for new base-image CVEs within a reasonable window (days for criticals, weeks for highs)?
- **Abandoned images**: Repos with archived source, no pushes in 2+ years, deprecated publisher notices — score as abandoned and seek alternatives.

### 4.3 Security Track Record (container-image-specialized)

- **Critical/high CVEs**: Count unpatched critical + high CVEs from Trivy / Grype / Scout / Clair. Any unpatched critical CVE with a known exploit is CRITICAL.
- **SBOM completeness**: Does the SBOM enumerate OS packages, language packages, and binaries? Missing SBOM is a gap; incomplete SBOM (e.g., missing language ecosystems) is a smaller gap.
- **Known compromise incidents**: Search for `"<image>" compromised OR malicious OR cryptominer OR backdoor`. The history of typosquatted Docker Hub images and the occasional compromised base image (e.g., cryptomining images disguised as utilities) is the key risk pattern.
- **Publisher-level incidents**: Has the publisher had other images pulled for policy violations, or an account compromise?

### 4.4 Permissions & Access (container-image-specialized)

**This is the primary runtime risk surface.** Score each dimension against
`references/criteria/container-image.md`:

- **USER instruction**: `USER root` (explicit) or no `USER` at all (defaults to root in most base images) is a Tier 2 flag and a Tier 3 near-rejection unless justified.
- **Linux capabilities**: Default Docker drops most caps. `--cap-add=NET_ADMIN`, `SYS_ADMIN`, `SYS_PTRACE`, `DAC_OVERRIDE` each need justification. `SYS_ADMIN` is effectively root-equivalent.
- **`--privileged`**: Grants all capabilities and disables most isolation. Acceptable only for narrow use cases (DinD on a private CI runner, some system-level tools). Default rejection on developer workloads.
- **Host namespaces**: `hostNetwork`, `hostPID`, `hostIPC` each break a different isolation boundary. Score individually.
- **Volume mounts**: `/var/run/docker.sock` mounted into the container is container-escape-equivalent (can spawn other containers on the host). `/` or `/etc` or `/proc` mounts are similar. Scoped read-only mounts of specific config paths are low-risk.
- **`allowPrivilegeEscalation`**: Defaults to true in Kubernetes unless set to false. Explicitly setting it false is a positive signal.

### 4.5 Reliability & Compatibility (container-image-specialized)

- **Multi-arch support**: Does the image ship amd64 + arm64? Mac M-series, AWS Graviton, and ARM CI runners are common — an amd64-only image forces emulation or disqualification.
- **Image size**: Oversized images (>1 GB for a single-purpose workload) signal poor layer discipline — bloated layers pull in more potential CVEs and waste bandwidth. Distroless / alpine / scratch-based images are typically <100 MB.
- **Layer count and structure**: Dozens of layers usually indicates sprawling `RUN` commands without cleanup. 10–20 layers is typical for well-built images.
- **Dockerfile best practices**: Multi-stage builds, `--no-install-recommends`, pinned package versions, `COPY` before `RUN` for cache efficiency, minimal final stage.
- **Startup behavior**: Does the container start quickly and with predictable logs? Mystery `ENTRYPOINT` scripts that phone home are a flag.

### 4.6 Supply Chain (container-image-specialized)

- **Base image lineage depth**: `<app> FROM distroless` is shallow (good). `<app> FROM <lang-runtime> FROM <debian-slim> FROM <debian>` is moderate. Deeper chains or unfamiliar bases increase surface.
- **Mirror registry risk**: Is the image pulled directly from the primary registry (e.g., `nginx` from Docker Hub official) or through a mirror / scraper / private re-publish? Mirrors introduce an extra trust hop; unknown mirrors can republish tampered images under familiar names.
- **Reproducible builds**: Public Dockerfile + CI-built + SLSA attestation + digest stability across rebuilds from the same commit all support supply-chain confidence.
- **Transitive base CVEs**: Even a recently-built `<app>` image inherits the base's CVEs until the base is rebuilt and `<app>` rebases. Cross-reference base CVEs via OSV and note any criticals not yet patched in `<app>`.

## Subject Verdict Notes

Container-image-specific guidance for how findings map to verdicts. These
notes supplement the shared verdict tree in `SKILL.md` Step N — they do not
replace it.

### Toward REJECTED

Any one of these pushes strongly toward REJECTED:

- **Known compromised image / publisher**: Prior removal from Docker Hub, GHCR, or Quay for cryptomining, backdoor, or credential theft
- **Unpatched critical CVE with exploit available** in the image or a direct base layer, with no alternative tag available
- **Typosquat / impersonation**: Image under a different namespace than the legitimate one it mimics (`user/nginx` vs official `nginx`), especially on Docker Hub
- **Unknown registry + suspicious naming**: `someunknownregistry.io/cryptominer:latest` — no publisher identity, no signing, obviously malicious name
- **`--privileged` requested on an unverified/untrusted image**: Combining maximum host access with no signing / no SBOM / no provenance is a near-automatic rejection
- **`:latest` on a privileged workload from an unknown publisher**: No pin + full host access + no trust signals
- **Dockerfile contains `curl | sh` from an unpinned host**: Opaque install pipeline that can change under the user

### Toward CONDITIONAL

These findings push toward CONDITIONAL (installation may proceed with listed
conditions):

- **`:latest` tag from a trusted publisher**: Condition — pin to the current digest (`<image>@sha256:<hex>`), document it, re-audit on upgrade
- **Trusted image without a Cosign signature**: Condition — understand the signing gap; if org policy requires signatures, either skip the image or request signed variant from publisher
- **Base image has known CVEs but no patched variant yet**: Condition — apply workloads-level mitigations (network policy, seccomp, minimal mounts); re-audit when patched
- **Image requests specific `cap_add` with justification**: Condition — document which capabilities are needed and why; constrain runtime via seccomp / AppArmor
- **Rootful image on developer workstation**: Condition — run under rootless Docker / Podman, or map container UID to an unprivileged host user
- **Image older than 2 years but still actively used upstream**: Condition — identify a maintained alternative; if none, verify CVE exposure and mitigate
- **3+ MEDIUM flags accumulated**: Cumulative risk triggers CONDITIONAL per shared verdict tree

### Toward APPROVED

All of the following support APPROVED:

- All tier-appropriate checks completed with no flags
- Digest-pinned reference OR specific immutable tag from a Docker Official / Verified Publisher / recognized GitHub org
- Cosign signature verifies (or equivalent attestation), SBOM present
- No unpatched critical CVEs; high CVEs have documented mitigations or are pending a patch in an acceptable window
- Non-root `USER` set; no `--privileged`; no unnecessary `cap_add`
- Base image is a recognized minimal base (distroless, alpine, debian-slim, ubi-micro) at a recent version
- Multi-arch manifest available for target platforms
- Public Dockerfile source and reproducible build

After completing the Subject Rubric and noting verdict-relevant findings,
**return to `SKILL.md` Step N** for the shared verdict tree, report
skeleton, and escalation guidance.
