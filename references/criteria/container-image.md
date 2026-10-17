# Container Image — Criteria Addendum

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

## Registry Trust Signals

| Registry | Verified Publisher Signal | Adoption Metric | Trust Notes |
|----------|--------------------------|-----------------|-------------|
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

## SBOM Standards

| Format | Producers | Notes |
|--------|----------|-------|
| SPDX (JSON or tag-value) | Syft, Trivy, anchore, Microsoft SBOM Tool | Linux Foundation standard; broadly supported by consumers |
| CycloneDX (JSON or XML) | Syft, Trivy, cyclonedx-cli, various language tooling | OWASP-maintained; common in enterprise supply-chain tooling |
| SPDX-lite / custom | Vendor-specific tools | Lower interoperability |

Fetch SBOMs from, in order of strength: a signed SBOM attestation (`cosign verify-attestation --type spdxjson|cyclonedx` with identity flags); a BuildKit SBOM attestation (`docker buildx imagetools inspect <image> --format '{{json .SBOM}}'`); `docker scout sbom <image>`; or a local scan (`syft <image> -o spdx-json` / `syft <image> -o cyclonedx-json`, pinned per the `references/criteria.md` audit-tooling note). `cosign download sbom` is deprecated and returns unsigned attachments: treat its output as contents data, not publisher-attested evidence.

### Scoring impact

- SBOM in a signed attestation whose identity verifies (§4.6 V2), complete (OS + language packages) = strong positive
- BuildKit SBOM attestation or legacy attached SBOM (unsigned), complete = moderate positive (publisher-built contents, not signed)
- SBOM generated by Syft or Trivy locally, complete = moderate positive (confirms contents but not publisher intent)
- No SBOM available from publisher, no local generation attempted = gap (note, not flag)
- Publisher claims SBOM but the attached document is empty / malformed = MEDIUM flag (supply chain hygiene concern)

## Layer Risk Patterns

Dockerfile / image-history patterns that elevate risk when observed:

| Pattern | Risk | Why |
|---------|------|-----|
| `USER root` (or no `USER`) and no verified entrypoint privilege drop | LOW on a dev workstation; HIGH in production (Scoring impact) | Container runs as root inside its namespace; combined with shared kernel, escape bugs land on the host as root |
| Entrypoint drops privileges (`gosu`, `su-exec`, `setpriv` in the entrypoint script) | Low | Starts as root to fix file ownership, then execs the service as a non-root user (e.g. `redis` runs `exec gosu redis` for `redis-server`). Read the entrypoint to verify; the drop often applies only to the image's default command |
| Secrets found by a layer scan (`trivy image --scanners secret`) | High | Same exposure as `ENV` secrets; leaked API keys in public images are common |
| `COPY . .` | Medium | Bundles the entire build context — often includes `.env`, `.git`, credentials, and SSH keys |
| `ENV` with secret-looking values (`PASSWORD=`, `TOKEN=`, `API_KEY=`) | High | Baked-in credentials readable by anyone who pulls the image |
| `RUN curl <url> \| sh` / `wget \| bash` | High | Opaque install pipeline; the `<url>` can change under the user between builds |
| `ADD <url>` | High | Similar to curl-pipe-bash but without checksum verification |
| `chmod -R 777` | Medium | Over-permissive filesystem; any process inside the container can modify anything |
| `apt-get install -y ...` without `--no-install-recommends` and without cleanup | Low-Medium | Bloated layers pull in more CVE surface |
| Full `curl` + `wget` + shell + package manager in a "minimal" image | Medium | Large attacker toolkit available post-compromise |
| Embedded `nc` / `ncat` / `socat` | Medium-High | Reverse shell primitives embedded in the image |
| `WORKDIR /root` or writes to `/root` | Low | Implies root-ownership assumptions; ties into USER-root pattern |

### Scoring impact

- Root at runtime (first row, or `securityContext.runAsUser: 0` in a manifest): dev workstation = LOW note `root at runtime (dev)` (the Recommendation may suggest rootless Docker / Podman); production or any other non-dev workload (shared host, CI runner, cluster) = HIGH flag → CONDITIONAL. Condition: non-root `USER` / `runAsNonRoot: true`, a rootless runtime, or Kubernetes user namespaces (`hostUsers: false`). This row is rated only by this rule, not by the pattern counts below
- Any 2 high patterns = HIGH flag
- Any 1 high pattern without justification = MEDIUM-HIGH flag
- Multiple medium patterns (3+) = MEDIUM flag (cumulative hygiene concern)

## Runtime Privilege Classification

Runtime flags on the *invocation* of the container, not the image itself.
Source: `docker run` arguments, Compose `service` config, Kubernetes `Pod` /
`Container` spec.

### High-risk runtime flags

| Flag | Risk | Why |
|------|------|-----|
| `--privileged` / `privileged: true` | Critical | Disables most isolation; grants all capabilities, device access, and a near-root view of the host |
| `--cap-add=SYS_ADMIN` | Critical | Effectively root; the "god cap" that covers mount, namespace manipulation, and more |
| `--cap-add=NET_ADMIN` | High | Full network-stack manipulation; can reshape routes, firewalls, and namespaces |
| `--cap-add=SYS_PTRACE` | High | Attach debugger to host processes (if pid namespace shared) |
| `--cap-add=DAC_OVERRIDE` / `DAC_READ_SEARCH` | High | Bypass file ownership/permission checks |
| Mount `/var/run/docker.sock` | Critical | Container-escape-equivalent: can spawn new containers on the host |
| Mount host `/`, `/etc`, `/proc`, `/sys`, `/dev` | Critical | Direct host filesystem access |
| `--network host` / `hostNetwork: true` | High | Bypasses Docker/k8s network namespace; container sees host interfaces |
| `--pid host` / `hostPID: true` | High | Sees and can signal host processes |
| `--ipc host` / `hostIPC: true` | Medium-High | Shares SysV IPC / shared memory with host |

### Medium-risk runtime flags

| Flag | Risk | Why |
|------|------|-----|
| `--cap-add=NET_RAW` | Medium | Raw socket access; enables some network attacks |
| `--cap-add=CHOWN` / `FOWNER` / `SETUID` / `SETGID` | Low-Medium | Per-cap risk is modest, but any cap-add on an unverified image is a note |
| `allowPrivilegeEscalation: true` (or not set) | Medium | In Kubernetes, defaults to true; explicitly false is the safe choice |
| `securityContext.runAsUser: 0` | LOW on a dev workstation; HIGH in production (Layer Risk Patterns → Scoring impact) | Explicit root at runtime; rated only by the root-at-runtime rule, like `USER root` |
| Bind-mount of specific host paths (config dirs) read-write | Low-Medium | Reduced risk vs whole-filesystem mount, but still host data exposure |
| Missing `readOnlyRootFilesystem: true` | Low | Not required, but a positive signal when set |

### Low-risk runtime flags

| Flag | Risk | Why |
|------|------|-----|
| Default capability set | Low | Docker's default drops most dangerous caps |
| Rootless container runtime (rootless Docker, Podman) | Low | Kernel namespacing reduces impact of escape bugs |
| Read-only root filesystem + scoped writable volume | Low | Strong defense-in-depth |
| `seccomp=default` + `apparmor=docker-default` | Low | Layered MAC policies |
| `hostUsers: false` (Kubernetes user namespaces; GA in v1.36) | Low | Container root maps to an unprivileged host UID; capabilities such as `NET_ADMIN` only affect the pod's own namespaces |
| Namespace enforces Pod Security Standard `restricted`; `seccompProfile: RuntimeDefault` | Low | Baseline that blocks privileged pods, host namespaces, hostPath mounts and root |

### Scoring impact

- Critical-risk flag (`--privileged`, `--cap-add=SYS_ADMIN`, `/var/run/docker.sock` or host `/`, `/etc`, `/proc`, `/sys`, `/dev` mounts) on an image whose identity does not verify (§4.6 V2, incl. the Docker Official Images curated-pipeline checks) or from an unknown publisher = CRITICAL → REJECTED (`SKILL.md` CRITICAL flag)
- Critical-risk flag on a verified-publisher image = HIGH flag → CONDITIONAL. Condition: drop the flag; or, where the publisher documents the need (e.g. Docker-in-Docker on an isolated CI runner, a node agent), isolate the host and record the justification
- User namespaces (`hostUsers: false`) or a rootless runtime lower each High-risk capability row one step (High → Medium); they do not lower Critical rows
- Multiple high-risk flags on the same container = compound; escalate verdict
- Default-safe runtime (non-root user, default caps, no host namespaces) = positive signal

## Tag vs Digest Pinning

| Reference shape | Immutability | Risk |
|-----------------|--------------|------|
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

## Tier Assignment Thresholds (Container Images)

### Tier 1 — Quick Audit

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
