# Patch: Retarget typosquat plan 2604021815 to `workflows/registry-package.md`

> **Date:** 2026-04-08
> **Author:** Claude (patch-projex, Opus 4.6)
> **Directive:** Phase 1 M1.4 of the subject-typed redesign nav — re-point the queued typosquat plan's file references from monolithic `SKILL.md` Step 3 to the future `workflows/registry-package.md`, defer execution until Phase 2 M2.1 lands the target file, preserve all detection logic.
> **Source Plan / Nav:** [`.projex/2604070218-install-auditor-subject-typed-redesign-nav.md`](../2604070218-install-auditor-subject-typed-redesign-nav.md) — Phase 1 M1.4
> **Patched Plan:** [`.projex/2604021815-algorithmic-typosquat-detection-plan.md`](../2604021815-algorithmic-typosquat-detection-plan.md)
> **Result:** Success

---

## Summary

Retargeted the queued `2604021815` typosquat plan so every `SKILL.md` Step 3 reference now points at `workflows/registry-package.md` (a Phase 2 M2.1 deliverable that does not yet exist). Added explicit dependency and "Blocked On" framing, updated plan status to **Blocked — awaiting Phase 2 M2.1**, and logged the patch in the plan's new Revision History section. Closed Phase 1 M1.4 in the nav, flipped Phase 1 status to **Complete** and Phase 2 status to **Current**, removed the resolved known blocker, and added a Revision Log entry.

---

## Changes

### Plan: `.projex/2604021815-algorithmic-typosquat-detection-plan.md`

**Change Type:** Modified
**What Changed:**
- **Header block** — Status `Ready` → `Blocked — awaiting Phase 2 M2.1 (`workflows/registry-package.md` authored)`. Added `Last Revised: 2026-04-08`. Added nav file to Related Projex.
- **New "Blocked On" section** (immediately below the header) — Phase 2 M2.1 is a hard requirement. Explicitly notes `workflows/registry-package.md` does NOT yet exist. Plan scheduled as Phase 2 M2.2. Proposal-acceptance dependency retained.
- **Summary** — Replaced "Update `SKILL.md` and `references/criteria.md`" with `workflows/registry-package.md` + the optional `references/criteria/registry-package.md` addendum (per Phase 0 M0.3). Explicitly adds "No changes to `SKILL.md`" to prevent regression on the dispatcher.
- **Scope line** — `scripts/` path clarified as skill-root (not per-workflow); `SKILL.md` removed from scope; `workflows/registry-package.md` added; optional criteria addendum noted.
- **Success Criteria item 4** — `SKILL.md instructs agents…` → `workflows/registry-package.md instructs agents…` with "Retargeted from `SKILL.md` Step 3 per Phase 1 M1.4" tag.
- **Success Criteria item 5** — Added registry-package criteria addendum as an acceptable additional location alongside `references/criteria.md` § 4.1.
- **Current State** — Added a top-of-section architectural note explaining the Phase 1 dispatcher refactor: `SKILL.md` is now the dispatcher; old Step 3 content lives in `workflows/generic.md`; Phase 2 will route registry-package audits to the new `workflows/registry-package.md`. Clarified that `workflows/generic.md` (not this plan) holds the current character-by-character language, and that this plan does not modify `generic.md` because registry-package audits will stop routing through it after Phase 2.
- **Key Files table** — `SKILL.md` row replaced with `workflows/registry-package.md` row (marked "does not yet exist — Phase 2 M2.1 deliverable" and "Retargeted from `SKILL.md` per Phase 1 M1.4"). Scripts row clarified as skill-root. New conditional row for `references/criteria/registry-package.md` added.
- **Dependencies block** — Added Phase 2 M2.1 as a hard `Requires:` bullet. Added "Scheduled as: Phase 2 M2.2" line pointing to the nav.
- **Step 3 heading** — `Step 3: SKILL.md — Workflow integration` → `Step 3: workflows/registry-package.md — Workflow integration (retargeted 2026-04-08 from SKILL.md per Phase 1 M1.4)`.
- **Step 3 Objective** — Now explains that after the Phase 1 dispatcher refactor `SKILL.md` contains no per-subject workflow steps.
- **Step 3 Depends on** — `Step 2` → `Step 2 and Phase 2 M2.1 (workflows/registry-package.md must exist)`.
- **Step 3 Files** — `SKILL.md` → `workflows/registry-package.md (does not yet exist — Phase 2 M2.1 deliverable)`.
- **Step 3 Changes** — Rewrote to target the workflow's Identify / Evidence step. Added two explicit **do-not-touch** bullets: `SKILL.md` and `workflows/generic.md` must not be modified.
- **Step 3 Verification** — `Read Step 1–3 for internal consistency` → `Read the workflow end-to-end for internal consistency. Confirm no typosquat-specific language has leaked into SKILL.md or workflows/generic.md.`
- **Step 3 If this fails** — `Revert SKILL.md` → `Revert workflows/registry-package.md to its pre-plan state`.
- **Acceptance Criteria Validation table, row 3** — `Read criteria + SKILL` → `Read criteria + workflows/registry-package.md`; expected result now mentions dispatcher and `workflows/generic.md` remain unchanged.
- **Rollback Plan step 2** — `Restore SKILL.md, references/criteria.md, evals/evals.json from base branch` → `Restore workflows/registry-package.md, references/criteria.md (and references/criteria/registry-package.md if touched), evals/evals.json from base branch.` Added step 3: `SKILL.md` and `workflows/generic.md` should not need restoring.
- **New "Revision History" section** at end — Two rows: 2026-04-02 initial draft and 2026-04-08 retarget, with full per-section change inventory.

**Why:** The Phase 1 dispatcher refactor moved the old monolithic Steps 1–4 out of `SKILL.md` and into `workflows/generic.md`. Registry-package audits will route to a new `workflows/registry-package.md` in Phase 2 M2.1. The typosquat plan was drafted pre-pivot and targeted `SKILL.md` Step 3, which no longer owns any registry-package workflow language. M1.4 is the bookkeeping milestone that re-points the plan so (a) execution lands in the right file when Phase 2 starts, and (b) we don't accidentally resurrect the monolith by modifying `SKILL.md`.

**What is preserved (not changed):** Typosquat detection logic, Levenshtein thresholds, download-ratio gates, `riskHint` output shape, normalization rules (scope stripping, hyphen/underscore folding, combosquat hints), cache design, error-JSON fallback, Step 1 script implementation, Step 2 criteria alignment wording, Step 4 eval cases, Verification Plan, Acceptance Criteria rows 1/2/4, Risks, Open Questions, proposal-acceptance dependency.

---

### Nav: `.projex/2604070218-install-auditor-subject-typed-redesign-nav.md`

**Change Type:** Modified
**What Changed:**
- **Header** — `Last Revised: 2026-04-07` → `2026-04-08`.
- **Active Work bullet** — Rewrote to reflect Phase 1 **complete** (all 4 milestones, M1.4 explicitly called out as resolved via patch-projex) and Phase 2 now **current**. Next concrete action changed from "run a patch-projex subagent against queued plan" to "plan-projex for Phase 2 M2.1 — author `workflows/registry-package.md`". Chain of downstream milestones (M2.2 typosquat unblock, then M2.3 CVE, then M2.4 transitive deps) explicitly listed.
- **Known Blockers section** — "Queued plans reference monolithic SKILL.md paths" blocker **removed** and replaced with `*(none)*` + a resolution note citing 2026-04-08 patch-projex. Explicit note that the typosquat plan's new Phase 2 M2.1 dependency is orderly and not a redesign blocker.
- **Phase 1 header** — `Phase 1: Dispatcher Refactor — Status: Current` → `Phase 1: Dispatcher Refactor — Status: Complete (2026-04-08)`.
- **M1.4 checkbox line** — `[ ]` → `[x]`. Replaced the future-tense description with a completion summary: patch-projex applied, plan status changed, all touched plan sections enumerated, typosquat logic preserved, SKILL.md/generic.md/references/scripts/evals all confirmed untouched (paperwork-only as designed). Execution line now points to the patched plan's 2026-04-08 revision history entry.
- **Phase 2 header** — `Phase 2: registry-package.md Extraction — Status: Future` → `Status: Current (as of 2026-04-08)`.
- **Revision Log** — Appended new row dated 2026-04-08 after the existing M1.1-M1.3 entry (chronologically correct placement). Row documents: the patch-projex run, every plan section modified, status transitions, Phase 1 → Complete, Phase 2 → Current, known blocker removed, and the M2.1 next-action handoff.

**Why:** The nav is the single source of truth for phase/milestone state. M1.4's completion must flow through: milestone checkbox, phase status, active work description, known blockers list, and revision log. Phase 2 becoming current is a direct consequence of Phase 1 closing and needs to be reflected in the phase header for future readers.

---

## Verification

**Method:** Post-edit static review.

1. Plan file grep for `SKILL.md` — remaining hits are only in the Revision History entry (explaining the retarget) and in the Current State architectural note (explaining that `SKILL.md` is now the dispatcher and is out of scope). No remaining hit describes `SKILL.md` as a modification target.
2. Plan file grep for `workflows/registry-package.md` — appears in Blocked On, Summary, Scope, Success Criteria, Key Files, Step 3 title/body/files/verification/rollback, Acceptance Criteria, Dependencies, and Revision History.
3. Nav file — Phase 1 status line shows `Complete`, Phase 2 shows `Current`, M1.4 checkbox is `[x]`, Known Blockers shows `*(none)*`, Revision Log tail has the new 2026-04-08 M1.4 row with chronologically correct position (after the M1.1-M1.3 entry).
4. Confirmed no changes to `SKILL.md`, `workflows/generic.md`, `references/*`, `scripts/*`, or `evals/evals.json`. M1.4 is paperwork only.

**Status:** PASS

---

## Impact on Related Projex

| Document | Relationship | Update Made |
|----------|-------------|-------------|
| [`.projex/2604021815-algorithmic-typosquat-detection-plan.md`](../2604021815-algorithmic-typosquat-detection-plan.md) | Patched plan | Retargeted from `SKILL.md` to `workflows/registry-package.md`; status → Blocked — awaiting Phase 2 M2.1; Revision History entry added |
| [`.projex/2604070218-install-auditor-subject-typed-redesign-nav.md`](../2604070218-install-auditor-subject-typed-redesign-nav.md) | Governing nav | M1.4 closed; Phase 1 → Complete; Phase 2 → Current; Known Blockers cleared; Revision Log entry added |
| [`.projex/2604021202-algorithmic-typosquat-detection-proposal.md`](../2604021202-algorithmic-typosquat-detection-proposal.md) | Upstream proposal | **Not modified in this patch.** The proposal still references `SKILL.md` Step 3 in its pre-pivot form. Retargeting the proposal's own copy is out of scope for M1.4 (which names only plan `2604021815`) and should be handled when Phase 2 M2.1 begins, or as a separate Phase 2 opener patch if desired. Noted here for the next patch-projex author. |

---

## Notes

- **Paperwork-only milestone.** M1.4 deliberately changes no executable files. This is by design — it's a re-pointing of document references so Phase 2 has a clean starting position.
- **Proposal retargeting deferred.** The upstream proposal (`2604021202`) also contains `SKILL.md` Step 3 language. M1.4 as written in the nav only names plan `2604021815`, so the proposal was not touched in this patch. A follow-up patch can handle the proposal either (a) as a second paperwork patch before Phase 2 starts, or (b) as part of Phase 2 M2.1's plan-projex when `workflows/registry-package.md` is authored.
- **Scope guard check passed.** Scope was bounded (2 files — 1 plan, 1 nav), fully understood (follows the nav's explicit M1.4 directive), no architectural decisions (the retarget destination was locked in Phase 0 decisions and documented in the eval §9 retargeting table), verifiable immediately (grep + visual diff). Patch was the correct workflow choice over a new plan-execute cycle.
- **Commit convention.** Changes will be committed with the `projex(patch):` prefix per the patch-projex workflow spec.
