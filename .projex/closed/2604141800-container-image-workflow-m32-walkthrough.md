# Container Image Workflow — M3.2 Walkthrough

> **Status:** Executed (2026-04-14)
> **Plan:** [2604141800-container-image-workflow-m32-plan.md](2604141800-container-image-workflow-m32-plan.md)
> **Source nav:** [2604070218-install-auditor-subject-typed-redesign-nav.md](../2604070218-install-auditor-subject-typed-redesign-nav.md) Phase 3, M3.2

---

## What was built

### 1. `workflows/container-image.md` (new — ~290 lines)

Type 4 subject-specific workflow. Follows the Identify / Evidence Part A / Evidence Part B / Subject Rubric / Subject Verdict Notes template established by `workflows/browser-extension.md`.

Key specializations:

- **Identify** — Registry-aware image reference extraction (registry + repo + tag + optional digest). Required context includes intended runtime (Docker / Compose / k8s / CI), Dockerfile availability, and organization signing policy (lets the workflow down-grade missing-signature flags when policy permits unsigned images, or up-grade them when policy forbids unsigned).
- **Evidence Part A (triage)** — Container-specific Tier 1/2/3 thresholds: Tier 1 requires digest pin + signing + SBOM + minimal base + recent CVE scan clean. Tier 3 triggers include `:latest` without digest, unknown registry, `--privileged` on unverified image, and suspicious naming (e.g., `cryptominer`).
- **Evidence Part B (research)** — Eight core questions covering publisher, pinning, signing (Cosign/Sigstore with Rekor transparency log, Notary v2, Docker Content Trust), SBOM (SPDX/CycloneDX via cosign/scout/syft), base image lineage (from labels or Dockerfile), CVEs (Trivy/Grype/Scout/Clair), runtime config (privileged, cap_add, host namespaces, mounts), and provenance (SLSA, reproducible builds).
- **Subject Rubric §4.1–4.6** — Every criterion specialized: §4.1 adds image-reference-shape scoring (digest → semver → floating tag → `:latest`); §4.4 makes runtime privilege the dominant axis (replaces browser permissions); §4.6 explicitly handles mirror registry risk and transitive base CVEs.
- **Subject Verdict Notes** — Concrete REJECTED triggers (compromised image, typosquat, `--privileged` on unverified image, `:latest` + privileged + unknown publisher), CONDITIONAL triggers (trusted-publisher `:latest` → pin to digest, base CVEs without patch → mitigate + re-audit), and APPROVED criteria.

### 2. `references/criteria/container-image.md` (new — ~180 lines)

Sections:

- **Registry Trust Signals** — table for Docker Hub (Official / Verified / Sponsored OSS), GHCR (org-scoped), Quay (verified publisher, UBI), ECR Public (AWS namespaces), ECR Private, GCR / Artifact Registry (distroless, google-containers), self-hosted / mirror.
- **Signing Standards** — Cosign keyless (Sigstore + Fulcio + Rekor), Cosign keyed, Cosign attestations (SLSA provenance), Notary v2 / Notation, Docker Content Trust (legacy).
- **SBOM Standards** — SPDX, CycloneDX, producer tools (Syft, Trivy, anchore, docker scout); fetch patterns.
- **Layer Risk Patterns** — `USER root`, `COPY . .`, secret-looking `ENV`, `curl | sh`, `ADD <url>`, `chmod 777`, bloated installs, embedded attacker tools.
- **Runtime Privilege Classification** — three-tier (high/medium/low) for invocation-side flags, including `--privileged`, SYS_ADMIN / NET_ADMIN / SYS_PTRACE / DAC_OVERRIDE, `/var/run/docker.sock` mount, `hostNetwork`/`hostPID`/`hostIPC`, `allowPrivilegeEscalation`, `runAsUser: 0`.
- **Tag vs Digest Pinning** — immutability matrix from digest to `:latest`.
- **Tier Assignment Thresholds** — Tier 1 (all-positive gates), Tier 2 (default), Tier 3 (11 trigger conditions).

### 3. `SKILL.md` — dispatch table + reference files

- Row 4: `workflows/generic.md` (Fallback) → `workflows/container-image.md` (Live — Phase 3 M3.2).
- Reference Files list: appended `workflows/browser-extension.md`, `workflows/container-image.md`, `references/criteria/browser-extension.md`, `references/criteria/container-image.md` (browser-extension entries were absent — fixed as part of this update since they were missed in M3.1).

### 4. `evals/evals.json` — two new cases

- **id 12** — `docker pull nginx:latest`. Tier 2. Docker Official Image but `:latest` no-digest-pin. Expected CONDITIONAL with pinning recommendation.
- **id 13** — `docker pull someunknownregistry.io/cryptominer:latest`. Tier 3. Unknown registry + suspicious naming + `:latest`. Expected REJECTED with exact_match assertion.

Eval count: 12 → 14.

---

## Noteworthy decisions

1. **Runtime privilege gets its own section rather than folding into §4.4.** Container risk at runtime is invocation-side, not image-side — the same image is safe or dangerous depending on how it's run. The workflow keeps image-resident concerns (USER, Dockerfile patterns) and runtime-invocation concerns (privileged, cap_add, host namespaces) both visible in §4.4 but clearly separated.

2. **Organization signing policy collected up-front in Identify.** Unlike browser extensions where policy rarely enforces signing, container orgs increasingly use admission controllers (Kyverno, Connaisseur, policy-controller) that make unsigned images an outright block. Capturing policy in Identify lets the rubric calibrate severity.

3. **`:latest` is CONDITIONAL, not REJECTED, on trusted publishers.** The eval id 12 (nginx:latest) verifies this calibration: the fix is "pin to digest," not "don't use nginx." This matches established Docker practice and the M3.1 precedent of "broad permissions with justification → CONDITIONAL with conditions."

4. **Cryptominer eval (id 13) uses exact_match on REJECTED.** Unlike most eval cases which allow a range of acceptable verdicts, `cryptominer` on an unknown registry with `:latest` is an unambiguous REJECTED — the compound flag pattern matches known malicious container distribution. Using exact_match guards against any future rubric softening that would let a clear-cut case slip through.

5. **No helper script in M3.2.** The M3.1 precedent (browser-extension deferred a store-lookup script) is preserved. `cosign verify`, `trivy image`, `skopeo inspect`, and `docker scout` are standard CLI tools the agent can invoke directly; a wrapping PowerShell script offers marginal value over calling them directly and would duplicate logic in each tool. A future milestone can add one if the audit flow benefits from structured JSON aggregation.

6. **Deferred coverage:** Multi-arch risk (amd64 vs arm64) is noted in §4.5 Reliability but not weighted heavily — most audits don't hinge on architecture availability. ImageStream / OpenShift-specific registry semantics are covered under the Quay / generic OCI rows rather than getting dedicated treatment.

---

## Verification

- `workflows/container-image.md` — present; 4 sections present; audit coverage table present; references addendum in Subject Rubric.
- `references/criteria/container-image.md` — present; all 7 sections present; Tier thresholds match workflow's Evidence Part A.
- `SKILL.md` — dispatch table row 4 updated; reference files list now enumerates all three live workflows + their addenda.
- `evals/evals.json` — ids 12 and 13 present; JSON syntax valid (comma terminators correct).
- Nav — M3.2 checkbox flipped; Current Position records completion; Active Work and Priorities point to M3.3.

---

## Next

**M3.3 — `workflows/ci-action.md`.** SHA-pin rule, `pull_request_target` warning, marketplace verified-creator check, transitive action audit, secret access review. Precedent now includes three live workflows (registry-package, browser-extension, container-image) — the template is well-exercised, and M3.3 can proceed with the same structure.
