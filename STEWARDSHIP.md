# Stewardship Schedule

## Purpose

This document defines a periodic re-evaluation cadence for the install-auditor skill's 10 workflow rubrics and their companion criteria files. Subject-area tooling, trust signals, and platform policies shift continuously; without a scheduled review process, rubrics silently rot and audits produce wrong verdicts. This schedule makes drift visible and actionable.

---

## Workflow Inventory

| Workflow File | Criteria File | Interval | Rationale | Last Reviewed | Next Due |
|---|---|---|---|---|---|
| `registry-package.md` | `references/criteria/registry-package.md` | 90 days | Fast-moving: npm provenance, PyPI attestations, new supply-chain attack patterns | — | — |
| `browser-extension.md` | `references/criteria/browser-extension.md` | 90 days | Manifest V3 migration deadlines, store policy shifts, permission model changes | — | — |
| `container-image.md` | `references/criteria/container-image.md` | 120 days | OCI spec changes, registry security features (Sigstore, SLSA levels) | — | — |
| `ci-action.md` | `references/criteria/ci-action.md` | 120 days | Marketplace verification requirements, pinning best practices evolve | — | — |
| `ide-plugin.md` | `references/criteria/ide-plugin.md` | 120 days | Marketplace policies, extension sandboxing model changes | — | — |
| `desktop-app.md` | `references/criteria/desktop-app.md` | 120 days | Code-signing ecosystem changes, notarization requirement updates | — | — |
| `cli-binary.md` | `references/criteria/cli-binary.md` | 120 days | Binary distribution standards, provenance attestation tooling | — | — |
| `agent-extension.md` | `references/criteria/agent-extension.md` | 60 days | Fastest-moving: MCP spec evolution, new agent frameworks, tool-permission models | — | — |
| `remote-integration.md` | `references/criteria/remote-integration.md` | 120 days | OAuth/API security standards, data residency rules, webhook verification | — | — |
| `generic.md` | *(none — fallback only)* | 180 days | Low-confidence fallback; changes only when dispatch logic or probe structure changes | — | — |

**Interval rationale summary:** agent-extension (60 d) is on the shortest cycle because MCP tooling is evolving rapidly. registry-package and browser-extension (90 d) are next — both ecosystems have active security infrastructure work. All other subject-specific workflows (120 d) move at a moderate pace. generic.md (180 d) is a static fallback that changes rarely.

---

## Event-Based Triggers

Any of the following events triggers an immediate out-of-cycle review for the affected workflow, regardless of the scheduled interval:

- A platform or ecosystem announces a **security feature that should be a new trust signal** (e.g., npm adds mandatory provenance, a store adds mandatory 2FA for publishers)
- A platform **deprecates or removes** a verification mechanism currently used in a rubric (e.g., an API endpoint changes, a signing method is retired)
- The **MCP or agent framework spec** releases a breaking change affecting tool permissions, manifest format, or capability declarations
- An **eval case starts producing unexpected results** (regression signal) — indicates the rubric's expected output no longer matches ecosystem reality
- A **real audit surfaces a gap** not covered by the rubric — a case the workflow should have caught but didn't

---

## Re-Evaluation Checklist

Run these steps in order for each workflow during a scheduled or event-triggered review pass:

1. Read the workflow file end-to-end; note any stale commands, URLs, or version references
2. Read the paired criteria file; verify tier thresholds still reflect current ecosystem norms
3. Check ecosystem changelogs/announcements since last review for security-relevant changes
4. Run existing eval cases for this workflow; confirm no regressions
5. If rubric gaps found: file a `plan-projex` for the update (do not edit in-place during review)
6. If eval gaps found: add new cases or update existing ones via `plan-projex`
7. Update the "Last Reviewed" and "Next Due" columns in the inventory table above
8. Add a dated entry to the nav doc revision log summarizing findings (Phase 6 section)

---

## Record-Keeping

- This document's inventory table is the source of truth for last-reviewed and next-due dates; update it after every review pass
- Each review pass adds a dated line to the nav doc revision log (`2604070218-install-auditor-subject-typed-redesign-nav.md`, Phase 6 section) summarizing what was checked and whether changes were needed
- Substantive changes (rubric edits, new eval cases) produce the full plan-projex → execute-projex → walkthrough artifact chain in `.projex/`
- No-change passes still require a log entry in the nav doc confirming the review occurred
