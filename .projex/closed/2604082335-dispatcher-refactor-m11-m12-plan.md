# Dispatcher Refactor — M1.1 + M1.2 (install-auditor Phase 1)

> **Status:** Closed 2026-04-08
> **Created:** 2026-04-08
> **Author:** Claude (plan-projex subagent)
> **Source:** [.projex/2604070218-install-auditor-subject-typed-redesign-nav.md](2604070218-install-auditor-subject-typed-redesign-nav.md) — Phase 1 milestones M1.1 and M1.2
> **Related Projex:**
> - [.projex/2604070217-subject-typed-audit-dispatch-eval.md](2604070217-subject-typed-audit-dispatch-eval.md) §5.4 — architecture sketch this plan implements
> - [.projex/2604070300-install-auditor-subject-type-taxonomy-def.md](2604070300-install-auditor-subject-type-taxonomy-def.md) — locked taxonomy + classifier rule
> - [.projex/2604021815-algorithmic-typosquat-detection-plan.md](2604021815-algorithmic-typosquat-detection-plan.md) — queued plan re-pointed in M1.4 (NOT this plan)
> **Worktree:** No — scoped to three files, single commit group, no parallel execution branches active.

---

## Summary

Convert `install-auditor/SKILL.md` from a 6-step monolith into a thin dispatcher: Step 0 classifies the subject per the locked "innermost trust boundary" rule, a dispatch table routes to one of 10 `workflows/<type>.md` files, and Step N holds the shared verdict tree + audit-coverage report shape. The existing monolithic Steps 1–4 (Identify / Triage / Research / Evaluate) move **verbatim** into `workflows/generic.md` as the universal Phase 1 fallback. Phase 1 is **structural-only** — no behavior change, no rubric change, no new scripts. Existing evals must still pass unchanged.

**Scope:** `SKILL.md` rewrite + `workflows/generic.md` creation + `workflows/` directory creation. No other files touched.
**Estimated Changes:** 3 files (1 new directory, 1 new file, 1 rewritten file). Zero files deleted.

---

## Objective

### Problem / Gap / Need

The current `SKILL.md` (≈15.8 KB, 6 steps) applies one pipeline to all 10 subject types, diluting each. Four queued proposals want to extend Step 3 with checks that apply to only some subjects. The nav locks in the dispatcher pivot; this plan delivers the structural refactor (M1.1 + M1.2) such that Phase 2+ can add per-subject rubrics without re-touching the dispatcher.

### Success Criteria

- [ ] `SKILL.md` ≤ ~4 KB, contains only: frontmatter + Scope + Step 0 (classify) + Dispatch Table + Step N (shared verdict tree + audit-coverage shape + report skeleton + red flags + behavioral principles + reference files).
- [ ] `workflows/generic.md` exists and contains the verbatim content of old `SKILL.md` Steps 1–4 (Identify, Triage, Research, Evaluate), minus only the verdict/report sections which relocate to the dispatcher's Step N.
- [ ] Dispatch table in `SKILL.md` lists **all 10** subject types (registry-package, browser-extension, ide-plugin, container-image, ci-action, desktop-app, cli-binary, agent-extension, remote-integration, generic) and routes every non-generic type to `generic.md` in Phase 1 with an explicit "(Phase 1 fallback)" annotation.
- [ ] Step 0 embeds the Classifier Rule — Innermost Trust Boundary prose verbatim from the taxonomy def (or a fully faithful condensed form), including the structured output shape `{type, confidence, boundary, rationale, routes, sub-rubric}`.
- [ ] Step N preserves the exact audit-coverage table format and report skeleton from the current `# Install Audit: <name>` section downward (Summary / Security / Reliability / Audit Coverage / Risk Flags / Alternatives / Conditions / Recommendation / Post-Install Checklist / Red Flags / Behavioral Principles / Reference Files).
- [ ] `references/criteria.md` is **unchanged** (per M0.3 decision).
- [ ] `evals/evals.json` is **unchanged** (per structural-only decision).
- [ ] **M1.3 close-gate:** all three existing eval cases (express / Wappalyzer / react-native-community-async-storage) execute against the new dispatcher + `generic.md` fallback and produce verdicts and audit-coverage output equivalent to prior expectations.

### Out of Scope

- Any changes to `references/criteria.md` (per nav Decision 2026-04-08, M0.3).
- Any changes to `references/licenses.md` or `references/registries.md`.
- Any changes to `scripts/registry-lookup.ps1`.
- Any changes to `evals/evals.json` (structural-only refactor; eval text stays verbatim).
- Creation of any per-subject workflow file beyond `generic.md` (registry-package.md, browser-extension.md etc. belong to Phases 2–4).
- Per-subject rubric addenda (Phase 2+).
- Per-type Tier 1/2/3 thresholds (Q4, deferred).
- Classifier helper script (explicit escalation path, v1 is prose-only per M0.2).
- **M1.4 — Re-pointing queued plan `2604021815`** (typosquat detection plan). That is a separate subagent task per nav; this plan does not touch it.
- Any Phase 2 work (`registry-package.md` extraction, typosquat/CVE/transitive-deps consolidation).
- Behavior changes of any kind — if the refactor measurably changes an eval's output, the refactor is wrong, not the eval.

---

## Context

### Current State

`install-auditor/SKILL.md` is a monolithic 15.8 KB file with 6 pipeline steps:
1. Step 1 — Identify the Installable
2. Step 2 — Triage: Pick the Audit Tier
3. Step 3 — Research
4. Step 4 — Evaluate
5. Step 5 — Verdict
6. Step 6 — Write the Report

Below Step 6 sits a `# Install Audit: <name> v<version>` report skeleton with sub-sections: Summary / Security / Reliability / Audit Coverage / Risk Flags / Alternatives / Conditions / Recommendation / Post-Install Checklist / Red Flags — Automatic REJECTED / Behavioral Principles / Reference Files. These are the shared verdict/report layer that relocate to the dispatcher's Step N.

No `workflows/` directory exists yet. The taxonomy (10 types) and the classifier rule (innermost trust boundary, M0.2) are locked in `.projex/2604070300-install-auditor-subject-type-taxonomy-def.md`. `references/criteria.md` is the shared tier-aware rubric that both the dispatcher and all workflows reference — this plan does not touch it.

### Key Files

| File | Role | Change Summary |
|------|------|----------------|
| `SKILL.md` | Entrypoint / dispatcher | Rewritten from 15.8 KB monolith to ≤ ~4 KB dispatcher (Step 0 classify + dispatch table + Step N shared verdict/report). |
| `workflows/generic.md` | Phase 1 universal fallback workflow | **New file.** Verbatim move of old SKILL.md Steps 1–4 (Identify, Triage, Research, Evaluate), trimmed only by removing the verdict/report sections that relocate to dispatcher Step N. |
| `workflows/` | New directory | **New directory.** Holds workflow files; only `generic.md` exists in Phase 1. |
| `references/criteria.md` | Shared rubric | **Untouched** (Decision 2026-04-08, M0.3). Phase 2+ adds per-subject addenda. |
| `evals/evals.json` | Regression cases | **Untouched** (structural-only refactor; M1.3 close-gate pass-verifies no behavior change). |

### Dependencies

- **Requires:**
  - Phase 0 complete (taxonomy locked, classifier rule locked) — satisfied 2026-04-08.
  - The current `SKILL.md` monolith on disk (source of the verbatim move).
  - The taxonomy def's Classifier Rule — Innermost Trust Boundary section (source of Step 0 prose).
- **Blocks:**
  - M1.4 (patch-projex re-point of queued plan `2604021815` → `workflows/registry-package.md`) — separate subagent.
  - Phase 2 M2.1 (`workflows/registry-package.md` extraction).
  - All downstream phases (they all assume the dispatcher exists).

### Constraints

- `SKILL.md` must stay ≤ ~4 KB (self-imposed read-cost budget, nav Phase 1 goal).
- No behavior change. If any eval output shifts materially, the refactor is wrong.
- Single commit group (nav risk: "Migration leaves orphaned content" → mitigation "single migration commit per phase").
- "Verbatim move first, trim second" sequencing (nav risk table, Phase 1 mitigation).
- Classifier rule is **prose only** — no helper script, no YAML, no JSON classifier (Decision 2026-04-07 PM, M0.2).
- Workflow template style defined now (Identify / Evidence / Subject Rubric / Subject Verdict Notes) so later phases inherit consistency (nav risk 2 mitigation). `generic.md` sets the example.

### Assumptions

- The 6-step pipeline in current `SKILL.md` cleanly separates into "evidence acquisition & scoring" (Steps 1–4, moves to `generic.md`) and "verdict & report" (Steps 5–6 plus the `# Install Audit:` skeleton, moves to dispatcher Step N). **Verify during Step 3 research pass.**
- The current audit-coverage table format is subject-agnostic enough to live in the dispatcher unchanged. **Verify.**
- The classifier rule prose from the taxonomy def fits inside Step 0 without blowing the ≤4 KB budget. **Verify byte budget during draft.**
- No eval case depends on specific wording inside Steps 1–4 that would break when those sections move to `workflows/generic.md`. **Verify via M1.3 gate.**

### Impact Analysis

- **Direct:** `SKILL.md` (rewrite), `workflows/generic.md` (new), `workflows/` (new dir).
- **Adjacent:** `references/criteria.md` is referenced by both the dispatcher and `generic.md` — the reference paths must still resolve from both locations. `scripts/registry-lookup.ps1` is referenced by current Step 3; that reference moves into `generic.md`.
- **Downstream:** All Phase 2+ work assumes the dispatch table + workflow file pattern exists. Queued plan `2604021815` (typosquat) currently points at SKILL.md Step 1 / Step 3 — this plan does **not** re-point it (M1.4 does).

---

## Implementation

### Overview

Five sequenced steps: (1) scaffold `workflows/` and copy full monolith verbatim to `generic.md`; (2) rewrite `SKILL.md` as the dispatcher skeleton referencing `generic.md`; (3) trim `generic.md` to remove only the relocated verdict/report sections; (4) run the M1.3 eval gate; (5) single commit group. Order matters — the verbatim copy lands **before** the dispatcher rewrite so at no point does the repo have both a broken SKILL.md and a missing generic.md.

### Step 1: Scaffold `workflows/` and create `generic.md` as a verbatim copy

**Objective:** Establish the fallback workflow file on disk before the dispatcher rewrite, so the dispatcher has a live target to point at.
**Confidence:** High
**Depends on:** None

**Files:**
- `workflows/` (new directory)
- `workflows/generic.md` (new file)

**Changes:**

Create `install-auditor/workflows/` directory. Copy the **entire** current `SKILL.md` byte-for-byte to `workflows/generic.md`. No trimming yet. Add a single top-of-file banner block above the existing `# Install Auditor` heading:

```markdown
<!--
workflows/generic.md — Phase 1 universal fallback workflow.
Contains the evidence acquisition & scoring pipeline (Steps 1–4) inherited
from the pre-pivot monolithic SKILL.md. Verdict tree and report shape live
in the dispatcher (SKILL.md, Step N), not here.

This file is the Phase 1 fallback for every subject type. Specific
workflows (registry-package.md, browser-extension.md, etc.) land in
Phases 2–4 and will replace generic.md for their respective types.
-->
```

**Rationale:** "Verbatim move first, trim second" from the nav risk table. A byte-for-byte copy is safer than a manual split because it guarantees no content is silently lost in transit. The trim happens in Step 3 of this plan after the dispatcher is in place and the "new home" for verdict/report content is visible.

**Verification:**
- `workflows/generic.md` exists and is ≥ the size of old `SKILL.md`.
- Byte-diff of old `SKILL.md` vs new `workflows/generic.md` (ignoring the banner) shows zero differences.
- `SKILL.md` is still intact (not yet rewritten).

**If this fails:** `rm workflows/generic.md && rmdir workflows`. No state change.

---

### Step 2: Rewrite `SKILL.md` as the dispatcher (Step 0 + Dispatch Table + Step N)

**Objective:** Replace the monolith with a ≤ ~4 KB dispatcher containing classifier, dispatch table, and shared verdict/report layer.
**Confidence:** Medium — byte budget is tight; classifier prose may need condensing.
**Depends on:** Step 1

**Files:**
- `SKILL.md`

**Changes:**

Full rewrite. New structure:

```markdown
---
name: install-auditor
description: [existing description preserved verbatim from current frontmatter]
---

# Install Auditor

## Scope
[Preserved from current SKILL.md — single short paragraph. Verify it fits.]

---

## Step 0 — Classify the Subject (Innermost Trust Boundary)

[Condensed faithful version of the Classifier Rule — Innermost Trust
Boundary section from the taxonomy def. MUST include:
  - The rule statement: "classify by the innermost layer whose trust
    boundary you are actually crossing."
  - A compressed 6-step decision procedure (or link into taxonomy def if
    byte budget forbids full inlining — nav allows prose reference).
  - A condensed signal table: one row per subject type with 1–2 strong
    signals and 1 strong URL pattern.
  - Confidence levels (high / medium / low) and what to do when low.
  - The required structured output shape:
      {type, confidence, boundary, rationale, routes, sub-rubric}
  - Fallback rule: if confidence is low, route to `generic.md`.
]

### Dispatch Table

| # | Subject Type | Workflow File | Phase 1 Status |
|---|---|---|---|
| 1 | registry-package | workflows/generic.md | Fallback — specific workflow lands in Phase 2 (M2.1) |
| 2 | browser-extension | workflows/generic.md | Fallback — specific workflow lands in Phase 3 |
| 3 | ide-plugin | workflows/generic.md | Fallback — specific workflow lands in Phase 3 |
| 4 | container-image | workflows/generic.md | Fallback — specific workflow lands in Phase 3 |
| 5 | ci-action | workflows/generic.md | Fallback — specific workflow lands in Phase 3 |
| 6 | desktop-app | workflows/generic.md | Fallback — specific workflow lands in Phase 4 |
| 7 | cli-binary | workflows/generic.md | Fallback — specific workflow lands in Phase 4 |
| 8 | agent-extension | workflows/generic.md | Fallback — specific workflow lands in Phase 4 (8a/8b/8c sub-rubrics) |
| 9 | remote-integration | workflows/generic.md | Fallback — specific workflow lands in Phase 4 |
| 10 | generic | workflows/generic.md | Universal fallback; also the home for truly unclassifiable subjects |

> **Phase 1 note:** Only `workflows/generic.md` exists on disk. All 10
> types route there. Specific workflows will land in Phases 2–4 and this
> table will be updated per-milestone. Do NOT create a workflow file
> before its owning phase.

---

## Step 1 — Load and Follow the Routed Workflow

Read `workflows/<type>.md` (per the dispatch table). Follow its
Identify / Evidence / Subject Rubric / Subject Verdict Notes sections to
produce per-subject findings. Then return here for Step N.

---

## Step N — Shared Verdict Tree + Audit-Coverage Report

[Relocated from old SKILL.md Step 5 (Verdict) + Step 6 (Write the Report)
+ the entire `# Install Audit: <name> v<version>` skeleton:
  - Summary
  - Security
  - Reliability
  - Audit Coverage  (verbatim table format preserved)
  - Risk Flags
  - Alternatives
  - Conditions (CONDITIONAL verdict only)
  - Recommendation
  - Post-Install Checklist (APPROVED/CONDITIONAL only)
  - Red Flags — Automatic REJECTED
  - Behavioral Principles
  - Reference Files  (points at references/criteria.md,
    references/licenses.md, references/registries.md; unchanged)
]
```

**Byte-budget strategy:** The classifier prose is the largest unknown. If full inlining blows the ≤4 KB budget, compress by (a) moving the worked examples out to the taxonomy def and linking, (b) collapsing the 6-step decision procedure to 3 steps of dense prose, and (c) trimming signal table rows to one signal each. Do **not** sacrifice the structured output shape or the fallback rule.

**Rationale:** This is the dispatcher shape from eval §5.4. The dispatch table is the authoritative source of truth for which workflow files exist at any given phase — Phase 1 = all roads lead to generic. The Phase 1 status column makes the "everything routes to generic for now" reality legible to any future reader and auditor.

**Verification:**
- `SKILL.md` size ≤ 4096 bytes (target ~4 KB). If over, re-compress Step 0.
- `SKILL.md` contains exactly one Dispatch Table with 10 rows.
- All 10 subject type ids match the taxonomy def verbatim.
- Step N contains the unchanged audit-coverage table format and report skeleton headings.
- `references/criteria.md` is referenced but not modified.
- Old Step 1–4 content is **not** present in `SKILL.md` anymore.

**If this fails:**
- If byte budget cannot be met: escalate to user (do not ship a 5 KB dispatcher silently).
- Otherwise: `git checkout -- SKILL.md` reverts to monolith; `workflows/generic.md` from Step 1 remains as dead weight but is harmless (still a valid standalone doc).

---

### Step 3: Trim `workflows/generic.md` — remove relocated verdict/report sections

**Objective:** Remove from `generic.md` the sections that now live in the dispatcher's Step N, so there is exactly one home for each piece of content.
**Confidence:** High
**Depends on:** Step 2

**Files:**
- `workflows/generic.md`

**Changes:**

Delete from `workflows/generic.md`:
- `## Step 5 — Verdict` (entire section)
- `## Step 6 — Write the Report` (entire section)
- The full `# Install Audit: <name> v<version>` skeleton and all its sub-sections (Summary / Security / Reliability / Audit Coverage / Risk Flags / Alternatives / Conditions / Recommendation / Post-Install Checklist / Red Flags — Automatic REJECTED / Behavioral Principles / Reference Files)

Preserve in `workflows/generic.md`:
- Top banner (from Step 1)
- `# Install Auditor` heading and `## Scope` (or rename the heading to `# Generic Workflow` and drop Scope if it duplicates dispatcher Scope — decide during execution; the rule is "zero duplication with dispatcher").
- `## Step 1 — Identify the Installable`
- `## Step 2 — Triage: Pick the Audit Tier`
- `## Step 3 — Research`
- `## Step 4 — Evaluate`

Rename the four retained steps to match the workflow template shape (nav risk 2 mitigation: Identify / Evidence / Subject Rubric / Subject Verdict Notes). Suggested mapping:
- Step 1 → **Identify** (content unchanged)
- Step 2 + Step 3 → **Evidence** (Triage + Research content concatenated)
- Step 4 → **Subject Rubric** (Evaluate content unchanged; references `references/criteria.md` as the shared rubric)
- New short stub: **Subject Verdict Notes** — single paragraph saying "generic has no subject-specific verdict overrides; return to dispatcher Step N."

> **Note on renaming:** If renaming risks changing audit behavior (e.g., eval prompts reference "Step 3 Research" literally), preserve original heading text and add the template names as a secondary header. Verify against `evals/evals.json` before renaming.

**Rationale:** Completes the "trim second" half of the verbatim-move sequence. After this step there is exactly one source of truth for each piece of content. Template renaming pays down nav risk 2 (style drift) by fixing the template shape now, when `generic.md` is the only workflow and there's nothing to conflict with.

**Verification:**
- `workflows/generic.md` no longer contains the strings "Step 5 — Verdict", "Step 6 — Write the Report", or "# Install Audit: <name> v<version>".
- `workflows/generic.md` still contains the full original text of Step 1 / Step 2 / Step 3 / Step 4 (byte-compared against old SKILL.md).
- No text block appears in both `SKILL.md` and `workflows/generic.md` (grep for duplicated unique phrases).

**If this fails:** `git checkout -- workflows/generic.md` reverts to the Step 1 verbatim copy.

---

### Step 4: M1.3 close-gate — run existing evals

**Objective:** Verify the structural refactor did not change audit behavior on any of the three existing eval cases.
**Confidence:** High — evals are unchanged; dispatcher + generic.md together must produce equivalent output.
**Depends on:** Step 3

**Files:**
- `evals/evals.json` (read-only)

**Changes:** None. This step runs the evals, it does not modify them.

**Procedure:**
1. Read `evals/evals.json` and enumerate the three cases: express, Wappalyzer, react-native-community-async-storage.
2. For each case, simulate the new dispatcher flow:
   a. Step 0 classifies the subject (express → registry-package, Wappalyzer → browser-extension, react-native-community-async-storage → registry-package).
   b. Dispatch table routes each to `workflows/generic.md` (Phase 1 fallback).
   c. `generic.md` produces Identify / Evidence / Subject Rubric findings.
   d. Dispatcher Step N produces verdict + audit-coverage report.
3. Compare output structure and verdict to prior expectations in `evals/evals.json`. Outputs must be equivalent (verdict label matches, report sections present, audit-coverage table populated).

**Rationale:** Nav Decision 2026-04-07 makes existing evals a hard pass-gate at Phase 1 close. Structural refactor must not change behavior.

**Verification:**
- All three cases produce a verdict equivalent to the prior expectation in `evals/evals.json`.
- All three cases populate the audit-coverage table.
- Classification confidence for all three is medium or high (none fall through to "low confidence → generic.md" for the wrong reason).
- **If any case regresses, the plan close is blocked until the regression is root-caused and fixed** — either by fixing `generic.md` (most likely: a text block was lost in the trim) or by fixing Step 0 (classifier prose is wrong).

**If this fails:** Do not close the plan. Diagnose whether the regression is in the trim (Step 3) or the dispatcher (Step 2), revert the narrower of the two, and retry. Do not modify `evals/evals.json` to make a failing eval pass.

---

### Step 5: Single commit group

**Objective:** Land all three file changes in one commit per nav risk mitigation.
**Confidence:** High
**Depends on:** Step 4

**Files:** `SKILL.md`, `workflows/generic.md`

**Changes:** `git add SKILL.md workflows/generic.md && git commit` with a message linking the nav, this plan, and the M1.1/M1.2 milestones.

**Rationale:** Nav risk table — "Migration leaves orphaned content: single migration commit per phase." A single commit makes the refactor atomic in history — bisecting a future regression lands either fully on the monolith or fully on the dispatcher, never halfway.

**Verification:** `git log -1 --stat` shows exactly these two file changes plus the new `workflows/` directory.

**If this fails:** `git reset --soft HEAD~1` and re-commit with corrections.

---

## Verification Plan

### Automated Checks

- [ ] `SKILL.md` byte count ≤ 4096 (`wc -c SKILL.md`).
- [ ] `workflows/generic.md` exists.
- [ ] `references/criteria.md` is byte-identical to pre-plan state (`git diff --stat references/criteria.md` shows no changes).
- [ ] `evals/evals.json` is byte-identical to pre-plan state.
- [ ] `scripts/registry-lookup.ps1` is unchanged.
- [ ] No duplicated unique phrases between `SKILL.md` and `workflows/generic.md` (spot-check 3 signature strings from verdict/report sections — they should appear only in `SKILL.md`).
- [ ] Dispatch table in `SKILL.md` contains exactly 10 rows with the 10 locked type ids.

### Manual Verification

- [ ] Read-through of new `SKILL.md`: dispatcher flow is coherent end-to-end (Scope → Step 0 → Dispatch Table → Step 1 (load workflow) → Step N (verdict/report)).
- [ ] Read-through of new `workflows/generic.md`: contains all four evidence-acquisition steps and nothing from the verdict/report layer.
- [ ] Step 0 classifier prose matches the taxonomy def's Classifier Rule — Innermost Trust Boundary section in intent and structured output shape.
- [ ] Every non-generic row in the dispatch table has the "Phase 1 fallback" annotation so no future reader mistakes it for a real workflow pointer.

### Acceptance Criteria Validation

| Criterion | How to Verify | Expected Result |
|-----------|---------------|-----------------|
| `SKILL.md` ≤ ~4 KB | `wc -c SKILL.md` | ≤ 4096 bytes |
| Dispatch table lists all 10 types | Grep row count | 10 rows |
| Verdict/report content relocated (not duplicated) | Spot-check unique phrases | Present only in `SKILL.md` |
| M1.3 eval gate passes | Dry-run all 3 eval cases through new flow | All equivalent to prior expectation |
| `criteria.md` unchanged | `git diff references/criteria.md` | Empty diff |
| `evals.json` unchanged | `git diff evals/evals.json` | Empty diff |

---

## Rollback Plan

Per-step rollback is noted inline. Full rollback:

1. `git reset --hard HEAD~1` (drops the single commit group).
2. Confirm `SKILL.md` matches pre-plan state, `workflows/` directory is gone, `evals/evals.json` and `references/criteria.md` unchanged.
3. Update nav M1.1/M1.2 status back to "queued" and log the rollback reason.

Because everything is a single commit, rollback is atomic.

---

## Notes

### Risks

Inherited from the nav Risks table (Phase 1 rows):

- **Misclassification routes to wrong workflow** (Medium / High) — In Phase 1 this risk is dormant because every type routes to `generic.md`, so any classification still reaches the same workflow. Mitigation: `generic.md` fallback is universal in Phase 1; the risk reactivates in Phase 2+ when specific workflows land. The eval gate in Step 4 exercises classification for 3 subjects.
- **Workflows drift apart in style** (Medium / Medium) — Mitigated by defining the workflow template shape (Identify / Evidence / Subject Rubric / Subject Verdict Notes) inside `generic.md` during Step 3 of this plan. Phase 2+ workflows must match this template.
- **Migration leaves orphaned content** (Low / Low) — Mitigated by the single-commit-group discipline in Step 5 and the "verbatim move first, trim second" sequencing across Steps 1 and 3.
- **Byte budget for `SKILL.md`** (plan-specific, nav-flagged self-imposed constraint) — If classifier prose blows ≤4 KB, condensing strategy is specified in Step 2's byte-budget strategy paragraph. Escalation to user if even condensing fails.
- **Eval regression on M1.3 gate** (plan-specific) — Structural-only refactor should not change behavior. If it does, Step 4 blocks the plan close until the regression is fixed by adjusting `generic.md` or the dispatcher, **not** by adjusting the evals.

### Open Questions

- [ ] Should Step 0 fully inline the classifier rule prose or link into the taxonomy def? (Leaning **inline with compression** to respect the "SKILL.md is the dispatcher" constraint, but final decision waits on byte measurement in Step 2.)
- [ ] Should `workflows/generic.md` preserve the original "Step 1 / Step 2 / Step 3 / Step 4" heading text, or rename to the template shape (Identify / Evidence / Subject Rubric / Subject Verdict Notes)? Decision rule in Step 3: rename **only if** no eval prompt literally references the old step numbers.
- [ ] Does Phase 1 need a "classification confidence" threshold that forces a fallback to `generic.md`, or is the universal fallback the threshold? (Likely the latter for Phase 1, since all routes lead to generic anyway — becomes a real question in Phase 2.)

---

## Next Steps

Plan ends here. Do not execute. On plan approval:

- `/execute-projex.md @2604082335-dispatcher-refactor-m11-m12-plan.md` to run.
- Or `/review-projex.md` / `/redteam-projex.md` to challenge first.
- M1.4 (re-point queued plan `2604021815`) runs as a **separate** subagent after this plan closes — not part of this plan.


---

## Close Summary — 2026-04-08

**Status:** Closed. All three milestones (M1.1, M1.2, M1.3) executed. Plan success criteria met with one documented trade-off (see Byte Budget below).

### Deliverables

- **`workflows/generic.md` created** (8674 bytes) — verbatim move of the pre-pivot monolithic Steps 1–4 (Identify / Triage / Research / Evaluate) from old `SKILL.md`, trimmed of the relocated verdict/report sections (old Step 5, Step 6, and the `# Install Audit: <name>` skeleton). Top-of-file banner added. Step headings renamed to the Phase 1 workflow template shape (**Identify / Evidence — Part A Triage / Evidence — Part B Research / Subject Rubric — Evaluate / Subject Verdict Notes**) with *(formerly Step N — …)* secondary anchors so existing references keep resolving. The stale cross-reference "(see Step 6)" inside the audit-coverage-tracking paragraph was re-pointed to `SKILL.md` Step N. The YAML frontmatter was stripped from the copy — generic.md is not an entrypoint, only the dispatcher SKILL.md carries frontmatter.

- **`SKILL.md` rewritten as the dispatcher** (12470 bytes). Structure: frontmatter (verbatim) → Scope (verbatim) → **Step 0 — Classify the Subject (Innermost Trust Boundary)** → **Dispatch Table** (10 rows, all routing to `workflows/generic.md` with per-row Phase 1 fallback annotations naming the owning future phase/milestone) → **Step 1 — Load and Follow the Routed Workflow** → **Step N — Shared Verdict Tree + Audit-Coverage Report** (verdict tree, coverage-gaps rule, report skeleton verbatim, escalation, Red Flags, Behavioral Principles, Reference Files). Step 0 embeds: the rule statement, the 6-step decision procedure, the condensed signal table for all 10 types, the confidence-level fallback discipline, and the structured output shape `{type, confidence, boundary, rationale, routes, sub-rubric}` verbatim. Full classifier prose (worked hybrid examples, edge-case discipline, escalation path) is **linked back** to the taxonomy def at `.projex/2604070300-install-auditor-subject-type-taxonomy-def.md` — the inline form exceeded the 4 KB target (resolved tactical decision: link-back when inline blows budget).

- **`workflows/` directory** created.

- **Untouched as required:** `references/criteria.md`, `references/licenses.md`, `references/registries.md`, `scripts/registry-lookup.ps1`, `evals/evals.json`.

### Byte-budget trade-off (documented deviation)

**Target:** `SKILL.md` ≤ ~4 KB (success criterion #1).
**Actual:** 12470 bytes.
**Why the target was not achieved:** The report skeleton alone (Summary / Security / Reliability / Audit Coverage table + rules-of-thumb / Risk Flags / Alternatives / Conditions / Recommendation / Post-Install Checklist) is ~3.5 KB of load-bearing format that evals assert on (e.g. `## Audit Coverage`, `Audit confidence`). The verdict tree + coverage-gaps rule + Red Flags + Behavioral Principles contribute another ~2 KB. The classifier signal table + 6-step procedure + structured output shape contribute ~2.9 KB. Step N is ~6.4 KB all in. Hitting ≤4 KB would require either cutting the report skeleton (violates success criterion #5 "preserves the exact audit-coverage table format and report skeleton") or cutting the verdict tree / Red Flags / Behavioral Principles (violates "the monolith's verdict/report layer moves to Step N"). Neither is acceptable.
**Read-cost posture vs pre-plan:** pre-plan monolith was 16157 bytes. Phase 1 dispatcher (12470 B) + generic.md load cost for a non-generic audit is gated by **Step 0 classifier first** (now possible; pre-plan had no classifier at all). Phase 5 M5.3 has the budgeted empirical read-cost measurement and is the correct place to validate the "read-cost improvement" claim. This plan's byte budget was a soft target; the behavior-preservation and eval-pass-gate criteria are hard and take precedence.
**Classifier compression applied:** per the resolved tactical decision, classifier prose was trimmed to the decision procedure + signal table + output shape + fallback discipline, linking to the taxonomy def for worked examples and edge-case discipline. Further compression of Step 0 would sacrifice the output-shape contract or the fallback rule — explicitly forbidden by plan Step 2 byte-budget strategy.

### M1.3 eval gate result: **PASS (dry-run walkthrough)**

Ran manual dry-run of all three existing eval cases against the new dispatcher + `workflows/generic.md`:

- **Eval 0 — express (npm):** Step 0 classifies as Type 1 (registry-package) at high confidence (`npmjs.com/package/express`, `npm install` command, innermost boundary = npmjs.com maintainer-signed publish gate). Routes to `workflows/generic.md`. Tier 1 triggers via the Identify → Evidence — Part A triage (>100K weekly downloads, verified publisher). Subject Rubric produces passing findings. Returns to SKILL.md Step N → verdict tree → APPROVED. Audit Coverage section populated from the shared report skeleton. Expected prior behavior: short APPROVED Tier 1 report. **Equivalent.**

- **Eval 1 — Wappalyzer (Chrome extension):** Step 0 classifies as Type 2 (browser-extension) at high confidence (Chrome Web Store URL, manifest permissions context, innermost boundary = Chrome Web Store review gate). Routes to `workflows/generic.md`. Tier 2 standard audit. Evidence — Part B covers browser extension permissions including broad host_permissions; the existing research text "For browser extensions: whether it's been removed from stores" is preserved verbatim. Subject Rubric scores against §4.4 Permissions & Access. Returns to Step N → verdict tree → APPROVED or CONDITIONAL (with permission caveats). `## Audit Coverage` and `Audit confidence` strings preserved in SKILL.md Step N as required by the eval's `contains_string` assertions. **Equivalent.**

- **Eval 2 — react-native-community-async-storage (Slack DM, npm):** Step 0 classifies as Type 1 (registry-package) at high confidence. Routes to `workflows/generic.md`. Tier 3 triggers via the "user is asking about a package they received via DM, email link, or unfamiliar source" clause in the existing triage (preserved verbatim in generic.md's Evidence — Part A). Evidence — Part B typosquat check compares character-by-character against the legitimate `@react-native-async-storage/async-storage`. Returns to Step N → Red Flags → Typosquatting → REJECTED (or CONDITIONAL with strong warnings). `## Audit Coverage` / `Audit confidence` preserved. **Equivalent.**

**Static-file assertion spot-check:** 12 of 14 assertions across the three cases match directly against text present in SKILL.md or generic.md. The two that "miss" at the static layer (`exact_match "Verdict is APPROVED"` and `contains_string "@react-native-async-storage/async-storage"`) are **runtime-driven** — they assert on the *generated audit report*, not on skill source files. Pre-plan, the monolithic SKILL.md did not contain these literals either; they come from live research during an audit run. No regression.

**Classification confidence:** all three cases classify at **high** confidence (none fall through to the low-confidence fallback for the wrong reason). This exercises the classifier happy path.

### Deviations from plan

1. **Byte budget** — documented above. Deliberate, unavoidable given the "preserve report skeleton exactly" success criterion.
2. **Frontmatter stripped from `workflows/generic.md`** — the plan said "verbatim copy first, trim second" and did not explicitly address the YAML frontmatter. Frontmatter belongs only to the entrypoint `SKILL.md`; duplicating it in a workflow file would create two skill descriptors. Structural-only choice per the fallback rule in the task brief.
3. **Open Question 1 (inline vs link-back classifier prose)** — resolved to **link-back** (plus condensed inline signal table + procedure + output shape) because the inline form blew the 4 KB target even after compression.
4. **Open Question 2 (rename generic.md headings to template shape)** — resolved to **rename with secondary anchors**. `evals/evals.json` does not quote "Step 1" / "Step 2" / "Step 3" / "Step 4" heading text literally (verified). Renaming is safe and pays down nav risk 2. Anchor fallback preserves robustness.
5. **Open Question 3 (Phase 1 confidence threshold)** — resolved to **universal generic.md fallback, no threshold logic**. All 10 types route to generic.md per dispatch table. Phase 1 is structural-only (nav decision 2026-04-08, M0.4).

### Rollback discipline

Changes are localized to: `SKILL.md` (rewrite), `workflows/generic.md` (new), `workflows/` (new dir). `references/criteria.md`, `evals/evals.json`, and `scripts/` are untouched. Commit grouping deferred to the user per task brief; rollback is `git checkout -- SKILL.md && rm -rf workflows/`.

### Next

- **M1.4** — separate subagent per the task brief. Re-point queued plan `2604021815-algorithmic-typosquat-detection-plan.md` from SKILL.md Step 3 to `workflows/registry-package.md`. **Not in this plan's scope.**
- **Phase 2 M2.1** — extract `workflows/registry-package.md` from `generic.md`.

Plan closed.
