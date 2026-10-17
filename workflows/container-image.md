<!--
workflows/container-image.md - Type 4 subject-specific workflow.
Handles OCI/Docker container images from Docker Hub, Docker Hardened
Images, GHCR, Quay, ECR, Google Artifact Registry (incl. legacy `gcr.io`)
and other registries, whether pulled directly (`docker pull`), referenced
from a Dockerfile (`FROM`), or declared in Compose / Kubernetes manifests.

This workflow replaces workflows/generic.md for Type 4 subjects. After
producing findings here, return to SKILL.md Step N for the shared verdict
tree and report shape. The Audit Coverage table and audit-confidence
assertion are owned by the dispatcher — do not duplicate them here.
-->

# Container Image Workflow (Type 4)

This workflow handles **Type 4: container-image** subjects — OCI/Docker
images distributed via Docker Hub, Docker Hardened Images (`dhi.io`),
GitHub Container Registry (GHCR), Quay, Amazon ECR, Google Artifact
Registry (incl. legacy `gcr.io` paths), or any other OCI registry. It
specializes the generic evidence acquisition and scoring pipeline for
container concerns: identity-matched signing and attestations, SBOM
presence, base image lineage, tag vs digest pinning, layer CVEs, version
integrity, and runtime privilege.

After completing all sections below, return to `SKILL.md` Step N for the
shared verdict tree and audit-coverage report shape.

Sections follow the standard workflow template: **Identify / Evidence /
Subject Rubric / Subject Verdict Notes**.

## Identify

### 1. Determine the registry and image identity

| Registry | URL / pull pattern | Trust notes |
|----------|--------------------|-------------|
| Docker Hub | `docker.io/<ns>/<repo>:<tag>` or bare `<repo>:<tag>` | Largest catalog; "Docker Official" and "Verified Publisher" badges exist but most images have neither; some namespaces are frozen (e.g. `bitnamilegacy`) |
| Docker Hardened Images | `dhi.io/<repo>:<tag>` (Docker login may be required) | Docker-built hardened catalog; signed attestations verified with Docker's key (addendum) |
| GitHub Container Registry (GHCR) | `ghcr.io/<org>/<repo>:<tag>` | Org-scoped; inherits GitHub org identity; supports package attestations |
| Quay | `quay.io/<ns>/<repo>:<tag>` | Red Hat ecosystem; integrated Clair scanner; supports signed images |
| Amazon ECR | `<acct>.dkr.ecr.<region>.amazonaws.com/<repo>` (private) or `public.ecr.aws/<ns>/<repo>` | Private by default; AWS-authenticated pulls; public gallery exists |
| Google Artifact Registry | `<region>-docker.pkg.dev/<proj>/<repo>` or legacy `gcr.io/<proj>/<repo>` | Google-authenticated; Container Registry is shut down and `gcr.io` paths are served by Artifact Registry |
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
2. **Intended runtime** — local Docker, Docker Compose, Kubernetes, Podman, ECS/EKS/GKE, CI runner, or one-shot `docker run` — and whether it is a **dev workstation or production / shared** environment (this changes tag and root-at-runtime grading)
3. **Dockerfile availability** — does the user have / can produce the image's Dockerfile (for self-built images) or a source `Dockerfile` for reproduction
4. **Stated purpose** — what the user needs this image for (web server, database, build tool, dev environment, CI step, etc.)
5. **Organization signing policy** — does the org require Cosign-signed images, admission controller enforcement (e.g., Kyverno, Connaisseur, Sigstore policy-controller), or does it permit unsigned pulls
6. **Runtime privilege profile** — will the container run rootful, rootless, with added capabilities, mount host paths, use `hostNetwork`/`hostPid`, or run `--privileged`

If any of 1–5 are missing, ask before proceeding. Item 6 is obtained during research if not immediately available.

## Evidence — Part A: Triage (Pick the Audit Tier)

Gather registry listing data via web search or registry API:
- Publisher name, Docker Official / Verified Publisher badge, GHCR org status
- Last pushed date for the tag (mutable tags update; old last-pushed is a staleness flag)
- The digest the tag resolves to now (`docker buildx imagetools inspect <image>`) and the upstream release it ships — needed for `references/criteria.md` §4.6 (addendum "Version & Update Integrity (§4.6)")
- Creation date of the image (from manifest labels or registry metadata)
- Pull count or adoption signal
- Brief search for `"<image>" CVE OR vulnerability OR compromise OR malicious` for prior incidents

Then apply the **container-image-specific tier thresholds** from
`references/criteria/container-image.md` (section "Tier Assignment
Thresholds"):

### Tier 1 — Quick Audit (well-known, high-trust)

Use when ALL Tier 1 criteria from the addendum are met and `references/criteria.md` §4.6 raises nothing that bars Tier 1: Docker Official Image, hardened-catalog image, Verified Publisher (or equivalent GHCR/Quay publisher verification); digest-pinned reference — or, on a dev workstation only, a Docker Official / hardened-catalog tag resolved to a recorded digest (a semver tag alone never qualifies); identity verified per §4.6 V2 (matched signature or attestation, or the Docker Official Images curated-pipeline checks); SBOM available; no CRITICAL and no Blocking CVE on the resolved digest; recognized minimal or hardened base; default-safe runtime (root at runtime only on a dev workstation).

**Quick audit scope:** Confirm publisher + identity checks + SBOM availability + CVE scan of the resolved digest + §4.6 version age. Note the base image. No deep layer walk. If everything checks out, proceed directly to Subject Verdict Notes with minimal ceremony.

### Tier 2 — Standard Audit (default)

Default depth when not all Tier 1 criteria hold:
- Named tag (e.g., `nginx:1.27`) without digest pin, or production `:latest` on a Docker Official / hardened-catalog image
- No verified identity (unsigned, identity unmatched, or curated-pipeline attestations not checkable)
- Popular but unverified publisher
- Known base image, but no explicit SBOM

Full registry metadata lookup, signature/SBOM check, CVE scan against the image digest, base image lineage, Dockerfile inspection if available, and runtime-config review.

### Tier 3 — Deep Audit (any red flag)

Any Tier 3 trigger from the addendum: `:latest` / no tag with no digest pin (except Docker Official and hardened-catalog images); unknown or self-hosted registry; critical-risk runtime flag (`--privileged`, dangerous capability adds, `docker.sock` or host-root mounts) or host namespaces; image older than 2 years with no rebuild; Blocking CVE, or an unfixed CRITICAL in an OS / base layer; §4.6 V3 HIGH flag (tag moved with no upstream release, provenance or signer mismatch); scraped/mirror registry; suspicious naming (impersonates a well-known project or publisher); no publisher identity; `FROM` chain that transits an unknown base.

**Deep audit scope:** Full Tier 2 work + identity-matched signature and attestation verification (§4.6 V2; transparency-log inclusion where the publisher uses it), provenance check (source repo, workflow, SLSA level, build reproducibility), §4.6 V3 diff against the previous release, full layer CVE + secret scan with a pinned Trivy/Grype, Dockerfile audit for secrets / `curl | bash` / privilege escalation patterns, and runtime-manifest audit (privileged, cap-add, hostPid, hostNetwork, mount paths, user namespaces).

## Evidence — Part B: Research

### Core research questions (all tiers)

Answer every question that applies to the assigned tier:

1. **Who publishes this image?** Company, GitHub org, cloud vendor, community? Is the publisher verified by the registry (Docker Official, Verified Publisher, GHCR org-scoped, Quay verified)? Check for impersonation (same name, different namespace, or scraped mirror on an unknown host).
2. **Is the reference pinned by digest?** Tags are mutable — `:latest`, `:1.27` and even `:1.27.3-alpine` can be re-pushed by the publisher or by anyone holding its credentials. A digest (`@sha256:...`) is immutable. A tag counts as immutable only where the registry enforces it and the setting is visible (addendum "Tag vs Digest Pinning"). Unpinned references mean every pull can deliver different content; record the digest the tag resolves to now.
3. **Is the image signed, and by whom?** Verify against the expected identity (§4.6 V2): keyless Cosign with `--certificate-identity` + `--certificate-oidc-issuer`, keyed Cosign with the publisher's key, `gh attestation verify oci://…`, or `notation verify` (addendum "Signing Standards"). Keyless `cosign verify` without identity flags errors — that is not "unsigned". Docker Official Images have no user-verifiable signature: use the curated-pipeline checks. For Docker Hub, absence of signing is common but is a Tier 2 flag on a privileged workload.
4. **Is there an SBOM?** A signed SBOM attestation (`cosign verify-attestation --type spdxjson|cyclonedx`), a BuildKit SBOM attestation (`docker buildx imagetools inspect <image> --format '{{json .SBOM}}'`), `docker scout sbom`, or a local `syft <image>` scan should yield an SPDX or CycloneDX document. Absence is a gap, not automatic rejection — but an available SBOM is a Tier 1 requirement.
5. **What is the base image chain?** Parse `FROM` from the Dockerfile (if available) or inspect labels (`org.opencontainers.image.base.name`, `org.opencontainers.image.base.digest`). Trace to the root base — distroless / alpine / debian-slim / ubi / scratch — and flag deep chains or unfamiliar bases.
6. **What CVEs affect the image?** Scan the resolved digest with registry-side data (Docker Scout, GHCR / Quay tabs) and a pinned local scanner (Trivy/Grype; `references/criteria.md` audit-tooling note). Split HIGH/CRITICAL findings into own code vs OS / base / language-dependency layers and fixable vs unfixable, check CRITICALs against CISA KEV, and apply qualifying VEX `not_affected` statements (addendum "CVE Scope (§4.3)").
7. **What is the runtime configuration?** If a Dockerfile is available, inspect `USER`, `EXPOSE`, `ENV`, `HEALTHCHECK`, `ENTRYPOINT`. If a Compose / Kubernetes manifest is available, inspect `privileged`, `cap_add`, `hostNetwork`, `hostPID`, `hostIPC`, volume mounts (especially `/var/run/docker.sock`, `/`), and `securityContext` (`runAsUser`, `allowPrivilegeEscalation`).
8. **What is the image's provenance?** Is there a verifiable build attestation — GitHub artifact attestation (`actions/attest-build-provenance`, verified with `gh attestation verify`), signed SLSA provenance, or BuildKit provenance — and do its source repo + workflow match the publisher's public source? Is the Dockerfile source public and the build reproducible? Are the layers minimal and explainable?

### How to research

**Registry metadata lookup** (all tiers):

Use `docker buildx imagetools inspect <image>`, `skopeo inspect docker://<image>`, or `crane manifest <image>` to pull the image manifest without a full download. Extract:
- Created timestamp
- Labels (`org.opencontainers.image.*`): base image, source repo, revision, description
- Layer count and cumulative size
- Multi-arch manifest list (amd64, arm64, etc.)

For Docker Hub listings, web search the tag page and note the "Last pushed" date, Docker Official / Verified Publisher badge, pull count, and the "Tags" tab for available variants.

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

**SBOM check** (Tier 2 and Tier 3):

- `cosign verify-attestation <image>@<digest> --type spdxjson|cyclonedx` + identity flags — signed SBOM attestation
- `docker buildx imagetools inspect <image> --format '{{json .SBOM}}'` — BuildKit SBOM attestation (unsigned)
- `docker scout sbom <image>` — Docker's SBOM fetch
- `syft <image> -o spdx-json` — generates an SBOM from the image layers locally (pinned tool version)

`cosign download sbom` is deprecated and its attachments are unsigned; do not cite it as publisher-attested evidence. Record SBOM format (SPDX, CycloneDX), source (signed attestation, BuildKit, Scout, local), and package count. SBOM absence on a Tier 3 subject is a flag.

**CVE and secret scan** (all tiers):

- Registry-side data: Docker Scout on Docker Hub (`docker scout cves <image>` applies image VEX automatically), GHCR / Quay vulnerability tabs
- `trivy image <image>@<digest>` / `grype <image>@<digest>` — pinned versions per the `references/criteria.md` audit-tooling note; add `--vex <file>` for publisher or maintainer VEX
- `trivy image --scanners secret <image>@<digest>` — secrets baked into layers (Tier 2 spot-check, Tier 3 required)

Record for each HIGH/CRITICAL: layer class (own code vs OS / base / language dependency), fixed version or none, KEV status for CRITICALs, and any VEX `not_affected` with its source. Rate per the addendum "CVE Scope (§4.3)". Note how fresh the advisory feed is.

**Base image lineage** (Tier 2 and Tier 3):

Parse `FROM` from the Dockerfile if available. Otherwise, inspect labels (`org.opencontainers.image.base.name`) or compare layer digests against known base image digests (registry UI sometimes shows this). Flag:
- Deep chains (A from B from C from D from E) — each link adds surface
- Unfamiliar bases (random user image as the base layer)
- Ancient bases (Debian < 11, Ubuntu < 20.04, CentOS EOL variants)
- `FROM scratch` images that nevertheless include a full interpreter — inspect how that got in

**Layer and Dockerfile analysis** (Tier 3, spot-check for Tier 2):

Inspect Dockerfile (or layer history via `docker history <image>` / `crane config <image>`) for:
- `USER root` (or no `USER` at all — defaults to root); then read the entrypoint for a privilege drop (`gosu`, `su-exec`, `setpriv`) before rating root at runtime
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
- Positive signals: `hostUsers: false` (Kubernetes user namespaces), rootless runtime, namespace Pod Security Standard `restricted`, `seccompProfile: RuntimeDefault`

**Provenance and reproducibility** (Tier 3):

- Is the Dockerfile source public (GitHub, GitLab)?
- Which build attestation exists (GitHub artifact attestation, signed SLSA provenance, BuildKit provenance), and do its source repo + workflow + ref match the publisher's public source (§4.6 V2)?
- Do the tags correspond to releases or git tags on the source repo? A tag with no matching upstream release is a §4.6 V3 HIGH flag
- Compared with the previous release's digest, did the source repo, workflow, signer or image config change (§4.6 V3)?
- Is the build reproducible (same source → same digest)?

### Audit coverage tracking

Map evidence to the Audit Coverage rows expected by `SKILL.md` Step N. For
container images, the standard rows are:

| Check | Tier 1 | Tier 2 | Tier 3 |
|-------|--------|--------|--------|
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

## Subject Rubric — Evaluate

Score against the shared rubric in `references/criteria.md` AND the
container-image addendum in `references/criteria/container-image.md`. The
sections below specialize the shared criteria for container context.

### 4.1 Provenance & Identity (container-image-specialized)

- **Image reference shape**: Digest-pinned (`@sha256:...`) is strong; a tag in a registry that visibly enforces tag immutability is moderate; any other tag — specific (`:1.27.3-alpine`), floating (`:1.27`) or `:latest` — is mutable and weak, and `:latest` with no digest is weakest.
- **Publisher identity**: Docker Official Image, Verified Publisher, GHCR org linked to a recognizable GitHub org, Quay verified publisher, or a known cloud vendor namespace (e.g., `public.ecr.aws/amazonlinux/...`).
- **Signing chain**: A signature or attestation verifies **and** names the expected identity (§4.6 V2), or the image is a Docker Official Image that passes the curated-pipeline checks (addendum "Version & Update Integrity (§4.6)"). Presence without a matched identity earns no credit. Absence of signing is not automatic rejection but is a gap.
- **Build provenance**: A verifiable provenance attestation whose source repo + workflow match the publisher's public source, a reproducible build from public Dockerfile source, or a public CI build log — any one raises confidence sharply. Provenance naming an unexpected repo is a §4.6 V3 HIGH flag.
- **Impersonation check**: Similarly-named images under different namespaces on Docker Hub (e.g., `<user>/nginx` vs official `nginx`) are a red flag. Scraped mirror registries republishing popular images under a different host are also suspect.

### 4.2 Maintenance & Longevity (container-image-specialized)

- **Image age / last push**: Container images should be rebuilt periodically to pick up base-image CVE fixes. >6 months with no push on an actively-used image is stale; >2 years is abandoned.
- **Base image freshness**: Even if the image itself is recent, if its base (`FROM`) is an old Debian / Ubuntu / Alpine variant with unpatched CVEs, the image inherits that surface.
- **Update cadence**: Does the publisher ship patches for new base-image CVEs within a reasonable window (days for criticals, weeks for highs)?
- **Abandoned images**: Repos with archived source, no pushes in 2+ years, deprecated publisher notices — score as abandoned and seek alternatives.
- **Frozen namespaces**: A publisher notice that a namespace gets no further updates (e.g. `bitnamilegacy`) makes every image in it abandoned regardless of badge or pull count → HIGH flag `frozen namespace` (addendum Registry Trust Signals).

### 4.3 Security Track Record (container-image-specialized)

- **Critical/high CVEs**: Count critical + high CVEs on the resolved digest from Trivy / Grype / Scout / Clair, after qualifying VEX. Rate per `references/criteria.md` §4.3 and the addendum "CVE Scope (§4.3)": a KEV-listed CRITICAL in any layer, or an unfixed HIGH/CRITICAL in the image's own code, is a Blocking CVE → REJECTED; every other HIGH/CRITICAL (fix available, or in OS / base / language-dependency layers) is a HIGH flag → CONDITIONAL.
- **Secrets in layers**: Credentials found by the layer secret scan or in `ENV` → HIGH (addendum Layer Risk Patterns).
- **SBOM completeness**: Does the SBOM enumerate OS packages, language packages, and binaries? Missing SBOM is a gap; incomplete SBOM (e.g., missing language ecosystems) is a smaller gap.
- **Known compromise incidents**: Search for `"<image>" compromised OR malicious OR cryptominer OR backdoor`. The history of typosquatted Docker Hub images and the occasional compromised base image (e.g., cryptomining images disguised as utilities) is the key risk pattern.
- **Publisher-level incidents**: Has the publisher had other images pulled for policy violations, or an account compromise?

### 4.4 Permissions & Access (container-image-specialized)

**This is the primary runtime risk surface.** Score each dimension against
`references/criteria/container-image.md`:

- **Root at runtime**: `USER root`, or no `USER` with no verified entrypoint privilege drop (`gosu` / `su-exec` / `setpriv`). Dev workstation → LOW note; production or any other non-dev workload → HIGH flag → CONDITIONAL (addendum Layer Risk Patterns).
- **Linux capabilities**: Default Docker drops most caps. `--cap-add=NET_ADMIN`, `SYS_ADMIN`, `SYS_PTRACE`, `DAC_OVERRIDE` each need justification. `SYS_ADMIN` is effectively root-equivalent. User namespaces (`hostUsers: false`) or a rootless runtime lower high-risk caps one step.
- **`--privileged`**: Grants all capabilities and disables most isolation. On an image whose identity does not verify (§4.6 V2) → CRITICAL; on a verified-publisher image → HIGH flag → CONDITIONAL (drop it, or isolate the host for a documented need such as DinD on a private CI runner).
- **Host namespaces**: `hostNetwork`, `hostPID`, `hostIPC` each break a different isolation boundary. Score individually.
- **Volume mounts**: `/var/run/docker.sock` mounted into the container is container-escape-equivalent (can spawn other containers on the host). `/` or `/etc` or `/proc` mounts are similar; both are rated like `--privileged`. Scoped read-only mounts of specific config paths are low-risk.
- **`allowPrivilegeEscalation`**: Defaults to true in Kubernetes unless set to false. Explicitly setting it false is a positive signal.

### 4.5 Reliability & Compatibility (container-image-specialized)

- **Multi-arch support**: Does the image ship amd64 + arm64? Mac M-series, AWS Graviton, and ARM CI runners are common — an amd64-only image forces emulation or disqualification.
- **Image size**: Oversized images (>1 GB for a single-purpose workload) signal poor layer discipline — bloated layers pull in more potential CVEs and waste bandwidth. Distroless / alpine / scratch-based images are typically <100 MB.
- **Layer count and structure**: Dozens of layers usually indicates sprawling `RUN` commands without cleanup. 10–20 layers is typical for well-built images.
- **Dockerfile best practices**: Multi-stage builds, `--no-install-recommends`, pinned package versions, `COPY` before `RUN` for cache efficiency, minimal final stage.
- **Startup behavior**: Does the container start quickly and with predictable logs? Mystery `ENTRYPOINT` scripts that phone home are a flag.

### 4.6 Supply Chain & Version Integrity (container-image-specialized)

- **Version integrity floor**: `references/criteria.md` §4.6 applies to the resolved digest; its container plug-ins (version unit, curated pipelines, release diff, triggers) are in the addendum "Version & Update Integrity (§4.6)". A Docker Official Image rebuild of the same upstream release is the same version; a new upstream release is a new version.
- **Tag moves**: A tag that now points at content with no matching upstream release, or provenance that names a different or newly created repo, is a §4.6 V3 HIGH flag (the 2026 trusted-publisher tag-overwrite pattern). Condition: pin the last digest that passes V3.
- **Base image lineage depth**: `<app> FROM distroless` is shallow (good). `<app> FROM <lang-runtime> FROM <debian-slim> FROM <debian>` is moderate. Deeper chains or unfamiliar bases increase surface.
- **Mirror registry risk**: Is the image pulled directly from the primary registry (e.g., `nginx` from Docker Hub official) or through a mirror / scraper / private re-publish? Mirrors introduce an extra trust hop; unknown mirrors can republish tampered images under familiar names.
- **Reproducible builds**: Public Dockerfile + CI-built + SLSA attestation + digest stability across rebuilds from the same commit all support supply-chain confidence.
- **Transitive base CVEs**: Even a recently-built `<app>` image inherits the base's CVEs until the base is rebuilt and `<app>` rebases. Cross-reference base CVEs via OSV and note any criticals not yet patched in `<app>`.
- **Digest refresh**: A pinned digest freezes its CVEs too. Recommend a refresh cadence (bot-driven digest updates with a release-age gate), auditing each new digest.

## Subject Verdict Notes

Container-image-specific guidance for how findings map to verdicts. These
notes supplement the shared verdict tree in `SKILL.md` Step N — they do not
replace it.

### Toward REJECTED

Any one of these pushes strongly toward REJECTED:

- **Known compromised image / publisher**: Prior removal from Docker Hub, GHCR, or Quay for cryptomining, backdoor, or credential theft
- **Blocking CVE** in the resolved digest (`SKILL.md` Tree terms; addendum "CVE Scope (§4.3)"): a KEV-listed CRITICAL in any layer, or an unfixed HIGH/CRITICAL in the image's own code
- **Version-scoped compromise**: the resolved digest is in a confirmed compromise's affected range, or the compromise is unresolved (`references/criteria.md` §4.6 V4 case a)
- **Typosquat / impersonation**: Image under a different namespace than the legitimate one it mimics (`user/nginx` vs official `nginx`), especially on Docker Hub
- **Unknown registry + suspicious naming**: `someunknownregistry.io/cryptominer:latest` — no publisher identity, no signing, obviously malicious name
- **Critical-risk runtime flag on an image whose identity does not verify**: `--privileged`, `--cap-add=SYS_ADMIN`, `/var/run/docker.sock` or host `/`, `/etc`, `/proc`, `/sys`, `/dev` mounts with no verified signer or curated pipeline (§4.6 V2) → CRITICAL
- **`:latest` on a privileged workload from an unknown publisher**: No pin + full host access + no trust signals
- **Dockerfile contains `curl | sh` from an unpinned host**: Opaque install pipeline that can change under the user

### Toward CONDITIONAL

These findings push toward CONDITIONAL (installation may proceed with listed
conditions):

- **`:latest`, no tag, or any non-digest tag in production from a trusted publisher**: Condition — pin to the current digest (`<image>@sha256:<hex>`), document it, re-audit per `references/criteria.md` §4.6 V5. (On a dev workstation this is a LOW note when the digest is recorded and pinned in the Recommendation.)
- **Trusted image without a verifiable signature** (other than a Docker Official Image passing the curated-pipeline checks): Condition — understand the signing gap; if org policy requires signatures, either skip the image or request signed variant from publisher
- **HIGH/CRITICAL CVE that is not blocking** (fix available, or unfixed in OS / base / language-dependency layers; not KEV; no qualifying VEX): Condition — pull or rebuild a digest with the fix where one exists; otherwise apply workload mitigations (network policy, seccomp, minimal mounts, non-root) and re-audit when patched
- **Image requests specific `cap_add` with justification**: Condition — document which capabilities are needed and why; constrain runtime via seccomp / AppArmor
- **Root at runtime in production or another non-dev workload**: Condition — set a non-root `USER` / `runAsNonRoot: true`, run under rootless Docker / Podman, or enable user namespaces (`hostUsers: false`). (On a dev workstation: LOW note only.)
- **Critical-risk runtime flag on a verified-publisher image**: Condition — drop the flag, or document the need and isolate the host (dedicated CI runner, no secrets)
- **Frozen / legacy namespace** (e.g. `bitnamilegacy/*`): Condition — move to a maintained source
- **§4.6 flags** (fresh version, V3 continuity break): conditions per `references/criteria.md` §4.6
- **Image older than 2 years but still actively used upstream**: Condition — identify a maintained alternative; if none, verify CVE exposure and mitigate
- **3+ MEDIUM flags accumulated**: Cumulative risk triggers CONDITIONAL per shared verdict tree

### Toward APPROVED

All of the following support APPROVED:

- All tier-appropriate checks completed with no flags above LOW (LOW notes such as root at runtime on a dev workstation are compatible)
- Digest-pinned reference, or — dev workstation only — a tag whose resolved digest is recorded and pinned in the Recommendation; publisher is Docker Official, a hardened catalog, a Verified Publisher, or a recognized GitHub org
- Identity verified per §4.6 V2 (matched signature or attestation, or the Docker Official Images curated-pipeline checks); SBOM available
- No Blocking CVE and no other HIGH/CRITICAL left after qualifying VEX
- Not root at runtime (non-root `USER` or verified entrypoint privilege drop) — or root on a dev workstation only; no `--privileged`; no unnecessary `cap_add`
- Base image is a recognized minimal or hardened base (distroless, alpine, debian-slim, ubi-micro, Docker Hardened Images, Chainguard / Wolfi) at a recent version, or a `FROM` chain of Docker Official Images
- Multi-arch manifest available for target platforms
- Public Dockerfile source and reproducible build

After completing the Subject Rubric and noting verdict-relevant findings,
**return to `SKILL.md` Step N** for the shared verdict tree, report
skeleton, and escalation guidance.
