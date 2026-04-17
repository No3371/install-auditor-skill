# Stewardship Cadence (M6.3)

> **Status:** Complete
> **Created:** 2026-04-17
> **Completed:** 2026-04-17
> **Author:** Claude (plan-projex)
> **Source:** Phase 6 M6.3 of subject-typed redesign nav
> **Nav:** 2604070218-install-auditor-subject-typed-redesign-nav.md
> **Related Projex:** 2604070218-install-auditor-subject-typed-redesign-nav.md (Phase 6), 2604171500-per-workflow-eval-bundles-m61-plan.md, 2604171700-hybrid-subject-eval-cases-m62-plan.md
> **Walkthrough:** 2604172000-stewardship-cadence-m63-walkthrough.md
> **Worktree:** No

---

## Summary

Create a stewardship schedule document that defines a durable, lightweight re-evaluation cadence for each of the skill's 10 workflow rubrics (9 subject-specific + generic fallback) and their companion criteria files. Subject-area tooling and trust signals shift fast; without a periodic review process, rubrics silently rot.

**Scope:** One new file (`STEWARDSHIP.md` at repo root) — no workflow, eval, or skill file changes.
**Estimated Changes:** 1 new file.

---

## Objective

### Problem / Gap / Need

The install-auditor skill has 10 workflow files and 9 criteria reference files covering a fast-moving landscape (package registries, browser extension stores, container registries, CI marketplaces, IDE marketplaces, app signing ecosystems, binary distribution patterns, agent/MCP tooling, and remote integration platforms). These rubrics encode specific trust signals, verification commands, and tier thresholds that become stale as:

- Ecosystems add or deprecate security features (e.g., npm provenance, Chrome Manifest V3 enforcement deadlines)
- New attack patterns emerge (e.g., typosquat variants, supply-chain injection techniques)
- Tooling changes (e.g., registry API endpoints, vulnerability database schemas)
- Platform policies shift (e.g., store review requirements, signing certificate rules)

Without a defined review cadence, drift accumulates silently until an audit produces a wrong verdict.

### Success Criteria

- [ ] `STEWARDSHIP.md` exists at repo root
- [ ] Document lists all 10 workflows and their paired criteria files
- [ ] Each workflow has a defined review interval (time-based) and event triggers
- [ ] A re-evaluation checklist defines what a review pass covers
- [ ] A record-keeping section specifies where pass results are logged (nav revision log)
- [ ] Document is self-contained — a new maintainer can follow it without external context

### Out of Scope

- Performing any actual re-evaluation pass (that happens during execution of the cadence, not in this plan)
- Building automation or tooling (reminders, CI checks, dashboards)
- Modifying any existing workflow, criteria, eval, or skill file

---

## Context

### Current State

The skill has:
- **10 workflow files** in `workflows/`: `registry-package.md`, `browser-extension.md`, `ide-plugin.md`, `container-image.md`, `ci-action.md`, `desktop-app.md`, `cli-binary.md`, `agent-extension.md`, `remote-integration.md`, `generic.md`
- **9 criteria files** in `references/criteria/`: one per subject-specific workflow (no criteria file for `generic.md` — it is a low-confidence fallback)
- **41 eval cases** in `evals/evals.json` providing regression coverage
- **No existing stewardship process** — reviews happen ad hoc

The nav doc (Phase 6) explicitly calls for this: *"Schedule periodic re-evaluation of each workflow's rubric (subject-area tooling and trust signals shift fast)."* Phase 6 is continuous and never closes; the revision log captures each maintenance pass.

### Key Files

> Quick reference — detailed changes are in Implementation steps below.

| File | Role | Change Summary |
|------|------|----------------|
| `STEWARDSHIP.md` (new) | Stewardship schedule and re-evaluation process | Created — defines cadence, triggers, checklist, record-keeping |

### Dependencies

- **Requires:** M6.1 (eval bundles) and M6.2 (hybrid evals) complete — both are done
- **Blocks:** Nothing — this is the final structural milestone; future maintenance passes are ongoing operations, not milestones

### Constraints

- Must be lightweight enough to actually follow — heavy process guarantees abandonment
- Must work for both human maintainers and LLM agents performing reviews
- Phase 6 never closes, so the stewardship doc must support indefinite iteration

### Assumptions

- The 10-workflow / 9-criteria structure is stable (Phase 4 is complete)
- The nav revision log is the canonical place to record maintenance activity
- Quarterly is a reasonable base cadence for most workflows; faster-moving ecosystems (registry-package, agent-extension) may warrant shorter intervals

### Impact Analysis

- **Direct:** New file `STEWARDSHIP.md` at repo root
- **Adjacent:** Nav doc M6.3 checkbox gets checked (during walkthrough, not this plan)
- **Downstream:** Future maintainers and agents use this document to schedule and execute review passes

---

## Implementation

### Overview

Create `STEWARDSHIP.md` at repo root with four sections: (1) workflow inventory table with review intervals and rationale, (2) event-based triggers, (3) re-evaluation checklist, (4) record-keeping conventions. The document is a process artifact, not code.

### Step 1: Create `STEWARDSHIP.md`

**Objective:** Author the complete stewardship schedule document.
**Confidence:** High
**Depends on:** None

**Files:**
- `STEWARDSHIP.md` (new, repo root)

**Changes:**

```markdown
// Before:
(file does not exist)

// After:
# Stewardship Schedule

## Purpose
[Brief statement: why periodic review exists]

## Workflow Inventory
[Table: workflow file | criteria file | review interval | rationale | last reviewed | next due]

Rows for all 10 workflows:
- registry-package.md  | references/criteria/registry-package.md  | 90 days  | Fast-moving: npm provenance, pypi attestations, new attack patterns
- browser-extension.md | references/criteria/browser-extension.md | 90 days  | Manifest V3 migration, store policy shifts
- container-image.md   | references/criteria/container-image.md   | 120 days | OCI spec changes, registry security features
- ci-action.md         | references/criteria/ci-action.md         | 120 days | Marketplace verification, pinning best practices evolve
- ide-plugin.md        | references/criteria/ide-plugin.md        | 120 days | Marketplace policies, sandboxing model changes
- desktop-app.md       | references/criteria/desktop-app.md       | 120 days | Code-signing ecosystem, notarization requirements
- cli-binary.md        | references/criteria/cli-binary.md        | 120 days | Binary distribution, provenance attestation standards
- agent-extension.md   | references/criteria/agent-extension.md   | 60 days  | Fastest-moving: MCP spec evolution, new agent frameworks
- remote-integration.md| references/criteria/remote-integration.md| 120 days | OAuth/API security standards, data residency rules
- generic.md           | (none — fallback)                        | 180 days | Low-confidence fallback; changes only when dispatch logic changes

## Event-Based Triggers
[List of events that trigger immediate review regardless of schedule]
- Major ecosystem security incident affecting a subject type
- Platform deprecates or adds a verification mechanism used in a rubric
- MCP or agent framework spec releases a breaking change
- An eval case starts producing unexpected results (regression signal)
- A real audit surfaces a gap not covered by the rubric

## Re-Evaluation Checklist
[Ordered checklist for each review pass]
1. Read the workflow file end-to-end; note any stale commands, URLs, or version references
2. Read the paired criteria file; verify tier thresholds still reflect current ecosystem norms
3. Check ecosystem changelogs/announcements since last review for security-relevant changes
4. Run existing eval cases for this workflow; confirm no regressions
5. If rubric gaps found: file a plan-projex for the update (do not edit in-place during review)
6. If eval gaps found: add new cases or update existing ones via plan-projex
7. Update the "last reviewed" and "next due" columns in this document
8. Add a dated entry to the nav doc revision log summarizing findings

## Record-Keeping
[Where results live]
- This document's inventory table tracks last-reviewed / next-due dates
- Each review pass adds a dated line to the nav doc revision log (Phase 6 section)
- Substantive changes produce plan-projex → execute-projex → walkthrough artifacts in .projex/
```

**Rationale:** A single self-contained document at repo root is discoverable and lightweight. The tiered intervals (60/90/120/180 days) reflect how fast each ecosystem moves. agent-extension gets the shortest interval (60 days) because MCP tooling is evolving rapidly. generic.md gets the longest (180 days) because it is a static fallback.

**Verification:** File exists at `STEWARDSHIP.md`, contains all 10 workflows, has non-empty sections for triggers, checklist, and record-keeping.

**If this fails:** Delete the file and retry — no other files are touched.

---

## Verification Plan

### Automated Checks

- [ ] `STEWARDSHIP.md` exists at repo root (ls check)
- [ ] File contains all 10 workflow filenames (grep check)

### Manual Verification

- [ ] All 10 workflows listed with intervals and rationale
- [ ] Event triggers section has >= 4 concrete triggers
- [ ] Re-evaluation checklist has >= 6 ordered steps
- [ ] Record-keeping section references the nav revision log
- [ ] Document is readable without external context

### Acceptance Criteria Validation

| Criterion | How to Verify | Expected Result |
|-----------|---------------|-----------------|
| `STEWARDSHIP.md` exists at repo root | `ls STEWARDSHIP.md` | File present |
| All 10 workflows listed | `grep -c '\.md' STEWARDSHIP.md` | >= 10 matches |
| Review intervals defined | Each row has a days value | 10 intervals present |
| Event triggers present | Section header + bullet list | >= 4 triggers |
| Checklist present | Numbered list in checklist section | >= 6 steps |
| Record-keeping defined | References nav revision log | Explicit mention |

---

## Rollback Plan

1. `git rm STEWARDSHIP.md` — single new file, no other changes to revert
2. Revert the commit: `git revert HEAD`

---

## Notes

### Risks

- **Cadence abandonment:** Mitigated by keeping the process ultra-lightweight (one checklist, one table update, one log line per pass). No tooling dependencies.
- **Interval calibration:** Initial intervals are best-guess. The first round of actual reviews will validate or adjust them. The document is designed to be self-amending.

### Open Questions

(None — this is a documentation-only plan with no ambiguous technical decisions.)
