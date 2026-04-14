# Container Image Workflow — M3.2

> **Status:** Executed
> **Completed:** 2026-04-14
> **Walkthrough:** [2604141800-container-image-workflow-m32-walkthrough.md](2604141800-container-image-workflow-m32-walkthrough.md)
> **Created:** 2026-04-14
> **Author:** Claude (Opus 4.6)
> **Source:** [2604070218-install-auditor-subject-typed-redesign-nav.md](../2604070218-install-auditor-subject-typed-redesign-nav.md) Phase 3, M3.2
> **Related Projex:**
> - **Roadmap:** [2604070218-install-auditor-subject-typed-redesign-nav.md](../2604070218-install-auditor-subject-typed-redesign-nav.md)
> - **Framing eval (ideation §5.1, §5.3):** [2604070217-subject-typed-audit-dispatch-eval.md](../2604070217-subject-typed-audit-dispatch-eval.md)
> - **Taxonomy spec:** [2604070300-install-auditor-subject-type-taxonomy-def.md](../2604070300-install-auditor-subject-type-taxonomy-def.md)
> - **Pattern precedent (M3.1):** [2604141200-browser-extension-workflow-m31-plan.md](2604141200-browser-extension-workflow-m31-plan.md) — `workflows/browser-extension.md` is the structural template
> **Worktree:** No

---

## Summary

Create the container-image subject-specific workflow (`workflows/container-image.md`) and its criteria addendum (`references/criteria/container-image.md`), then wire them into the dispatcher and eval suite. This is the second Phase 3 milestone — it extends the dispatcher architecture to OCI/Docker images where the primary risk surface is signing + provenance + runtime privilege rather than permissions (browser extensions) or supply chain breadth (registry packages).

**Scope:** Type 4 container-image audit pipeline — workflow file, criteria addendum, dispatch table update, eval coverage.
**Estimated Changes:** 5 files (2 new, 3 modified), ~700 new lines.

---

## Objective

### Problem / Gap / Need

Container images currently route to `workflows/generic.md`, which knows nothing about image-specific trust signals. Gaps the framing eval (§5.1) identifies:

1. No signing-standard awareness — Cosign/Sigstore verification (with Rekor transparency log), Notary v2, and Docker Content Trust all have specific invocation patterns and verification semantics that the generic workflow can't express.
2. No SBOM handling — `cosign download sbom`, `docker scout sbom`, and `syft` are the standard tools, and SBOM presence is a first-class Tier 1 gate.
3. No base image lineage tracking — container risk compounds along `FROM` chains; the generic rubric has no vocabulary for this.
4. No `:latest` warning — tag vs digest immutability is container-specific and critical to production safety.
5. No runtime-privilege rubric — `--privileged`, `cap_add`, `hostNetwork`, `/var/run/docker.sock` mounts have no analog in any other subject type.
6. No registry trust taxonomy — Docker Hub (Official/Verified), GHCR (org-scoped), Quay, ECR, GCR each have different verification shapes.

### Success Criteria

- [x] `workflows/container-image.md` exists, follows Identify / Evidence / Subject Rubric / Subject Verdict Notes template
- [x] `references/criteria/container-image.md` exists, layers container-image-specific scoring
- [x] `SKILL.md` dispatch table row 4 routes to `workflows/container-image.md` (not `workflows/generic.md`)
- [x] At least 2 new container-image eval cases added (Tier 1 clean + Tier 3 high-risk)
- [x] No regressions in existing eval cases (ids 0–11)

### Out of Scope

- Helper scripts for `docker pull --dry-run` / `skopeo inspect` / `cosign verify` (no container-lookup.ps1 in M3.2 — agent uses CLI tools + web search when available; script is a future enhancement)
- Modifications to `workflows/generic.md`, `workflows/registry-package.md`, or `workflows/browser-extension.md`
- Changes to the shared `references/criteria.md`
- Other Phase 3 workflows (ci-action, ide-plugin)

---

## Context

### Current State

The dispatcher (`SKILL.md`) classifies container images via strong signals (`docker pull/run`, `FROM` in Dockerfile, `sha256:` digest, `hub.docker.com/*`, `ghcr.io/*`, `quay.io/*`, ECR/GCR) and routes them to `workflows/generic.md` as a fallback. The generic workflow has no container-specific logic.

M3.1 (browser-extension) is the most recent structural precedent. Its 4-section template and dispatcher contract (Audit Coverage owned by SKILL.md Step N) are inherited verbatim.

### Key Files

| File | Role | Change Summary |
|------|------|----------------|
| `workflows/container-image.md` | **New.** Type 4 subject-specific workflow | ~290 lines: Identify (registry + image extraction) / Evidence (tier thresholds + research on signing, SBOM, CVE, layers, runtime) / Subject Rubric (provenance-centric + runtime-privilege scoring) / Subject Verdict Notes |
| `references/criteria/container-image.md` | **New.** Per-subject criteria addendum | ~180 lines: registry trust signals, signing standards, SBOM standards, layer risk patterns, runtime privilege classification, tag/digest pinning, Tier 1/2/3 thresholds |
| `SKILL.md` | Dispatcher + dispatch table | Update 1 row + 2 reference-file bullets |
| `evals/evals.json` | New eval cases | Add id 12 (`nginx:latest` — Tier 2 CONDITIONAL) and id 13 (`someunknownregistry.io/cryptominer:latest` — Tier 3 REJECTED) |

### Dependencies

- **Requires:** Phase 3 M3.1 complete (2026-04-14) — browser-extension workflow provides the structural template
- **Blocks:** M3.5 eval gate (needs container-image eval coverage)

### Constraints

- Workflow must follow the established 4-section template
- Audit Coverage table and audit-confidence assertion stay in `SKILL.md` Step N
- No new scripts in M3.2 scope
- Criteria addendum follows the `references/criteria/browser-extension.md` pattern

### Assumptions

- Docker Hub, GHCR, Quay, ECR (public + private), and GCR/Artifact Registry are the registries worth covering in v1. Self-hosted Harbor and mirror registries get a note but not a dedicated row.
- Cosign/Sigstore is the modern default signing standard; Notary v2 is secondary; Docker Content Trust is legacy.
- Syft / Trivy / Grype / Docker Scout are the standard SBOM and CVE tools; the workflow describes both CLI invocation and "if tooling unavailable, use the registry UI" fallback.
- Runtime privilege classification covers both `docker run` flags and Kubernetes `securityContext` / Pod spec fields.

---

## Steps

1. Read structural templates (`workflows/browser-extension.md`, `references/criteria/browser-extension.md`, `SKILL.md`, `evals/evals.json`).
2. Write `workflows/container-image.md` following the 4-section template, specialized for container concerns.
3. Write `references/criteria/container-image.md` with registry trust, signing, SBOM, layer, runtime, tag/digest, and tier sections.
4. Update `SKILL.md` dispatch table row 4 and reference-files list.
5. Add eval cases id 12 (nginx:latest Tier 2) and id 13 (cryptominer Tier 3) to `evals/evals.json`.
6. Write walkthrough, close plan, update nav.

## Acceptance Criteria

- Workflow file exists at `workflows/container-image.md` with the required 4 sections and audit-coverage tracking table.
- Criteria addendum exists at `references/criteria/container-image.md` with registry trust, signing, SBOM, layer risk, runtime privilege, tag/digest, and tier sections.
- `SKILL.md` dispatch table shows Type 4 → `container-image.md` (Live — Phase 3 M3.2).
- `evals/evals.json` contains ids 12 and 13 using the existing structure.
- Nav updated: M3.2 checkbox flipped, Current Position notes M3.2 completion, Active Work / Priorities point to M3.3.
- Plan moved to `.projex/closed/` with Status: Executed.
- Walkthrough written.
