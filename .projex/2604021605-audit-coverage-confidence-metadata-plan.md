# Audit Coverage & Confidence Metadata

> **Status:** In Progress
> **Created:** 2026-04-02
> **Author:** Claude (plan-projex)
> **Source:** `2604021204-audit-coverage-confidence-metadata-proposal.md`
> **Related Projex:** `2604021200-reliability-accuracy-improvements-imagine.md`, `2604021204-audit-coverage-confidence-metadata-proposal.md`
> **Worktree:** No

---

## Summary

Implement Option B from the proposal: add a mandatory **Audit Coverage** table plus an **audit confidence** line (coverage completeness, not security assurance) to every install-auditor report, wire research and verdict steps to populate them, and define a canonical per-tier check list in `references/criteria.md` with eval assertions so outputs stay testable.

**Scope:** Skill docs (`SKILL.md`), audit criteria (`references/criteria.md`), eval suite (`evals/evals.json`) only — no new scripts or APIs.

**Estimated Changes:** 3 files, ~6 distinct edits (new section + instructional blocks + eval entries).

---

## Objective

### Problem / Gap / Need
Reports show findings without proving which checks ran. Readers cannot distinguish “clean after thorough checks” from “clean because little was checked.” The proposal fixes this with structured coverage metadata and a scoped confidence label.

### Success Criteria
- [ ] Step 6 report template includes `## Audit Coverage` (table + confidence line) with status vocabulary and framing that confidence = **coverage completeness**, not “safe.”
- [ ] Step 3 instructs agents to track each check’s status while researching; Step 5 links verdict narrative to unavailable/ failed checks when relevant.
- [ ] `references/criteria.md` defines a **canonical row set per tier** (what must appear as Done / Skipped / N/A / Not available).
- [ ] `evals/evals.json` asserts presence of an Audit Coverage section and of an audit-confidence line on at least one eval.
- [ ] Tier 1 stays short: only rows for checks actually performed or tier-skipped, per proposal.

### Out of Scope
- Option C (inline annotations in Security/Reliability cells).
- Changing global wording of every “None found” cell (optional follow-up).
- Re-audit diff narratives (e.g., vs previous run) — document as future enhancement only if needed.
- New automation/scripts; registry script name inconsistencies (`registry-lookup.js` vs `.ps1`) are pre-existing.

---

## Context

### Current State
- `SKILL.md` Step 6 is a fixed markdown skeleton (Summary → Security → Reliability → Risk Flags → …) with no coverage section.
- Step 3 lists research topics but does not require per-check status tracking.
- Step 5 is a verdict tree without guidance for “many lookups failed.”
- `references/criteria.md` describes rubrics by tier but not a **tabular checklist** aligned to report rows.
- `evals/evals.json` checks tier, verdict, file output, length — not coverage metadata.

### Key Files

| File | Role | Change Summary |
|------|------|----------------|
| `SKILL.md` | Authoritative skill | Add Step 3/5/6 + Behavioral Principle for coverage; insert template block after Reliability, before Risk Flags |
| `references/criteria.md` | Rubrics | New section: canonical Audit Coverage rows by tier (and installable type where it matters) |
| `evals/evals.json` | Regression tests | Add assertions for `## Audit Coverage` and confidence wording |

### Dependencies
- **Requires:** Proposal accepted or explicitly overridden for execution (proposal is currently **Draft** — confirm before execute).
- **Blocks:** None.

### Constraints
- Confidence labels must not imply security guarantee; wording must be explicit.
- Must not bloat Tier 1 reports: template must state minimal row count for Quick tier.

### Assumptions
- Placement: **after** Security and Reliability tables, **before** Risk Flags (matches proposal impact section; resolves “before vs after” open question).
- Verdict line stays `APPROVED` / `CONDITIONAL` / `REJECTED` unchanged; confidence remains under Audit Coverage (informational). Optional one sentence in **Recommendation** if 2+ checks unavailable — not a new verdict enum.

### Impact Analysis
- **Direct:** Report shape and agent behavior for all audits using this skill.
- **Adjacent:** Future proposals adding new checks will add rows to the canonical list in `criteria.md` and the template examples.
- **Downstream:** Eval runners must match new assertion strings.

---

## Implementation

### Overview
Edit `criteria.md` first so Step 6 can reference a single source of truth. Then update `SKILL.md` (Behavioral Principles → Step 3 → Step 5 → Step 6 order so later sections can reference earlier rules). Finally extend `evals.json`.

### Step 1: Canonical coverage rows by tier

**Objective:** Define check names and tier expectations so the coverage table is not ad hoc.

**Confidence:** High  
**Depends on:** None

**Files:**
- `references/criteria.md`

**Changes:**

Add a new top-level section (after “Applying Rubrics by Audit Tier” or as a dedicated `## Audit Coverage Checklist (Canonical)` section) that includes:

1. **Status vocabulary** — align with proposal: `Done` | `Done, N results` | `Skipped (<reason>)` | `Not available (<detail>)` | `N/A (<reason>)`.
2. **Tier matrices** — For Tier 1 / 2 / 3, list **rows** that must appear in the coverage table (e.g., registry/metadata lookup, typosquat, CVE/advisory sources, OpenSSF Scorecard, web search for incidents, dependency tree review, install script review, source review). Mark each as **Expected Done**, **Skipped by tier**, or **If applicable** (e.g., extension permissions row only for browser extensions).
3. **Footnote** that row labels in the report should match this list; agents may add rows for ecosystem-specific checks but must not omit tier-required rows.

**Rationale:** Reduces inconsistent tables; addresses “agent fills coverage table inconsistently” risk.

**Verification:** Section exists; tiers are distinguishable; lists are finite and copy-paste friendly.

**If this fails:** Revert the inserted section only.

---

### Step 2: Behavioral principle and Step 3 / Step 5 updates

**Objective:** Require tracking during research and tie verdict narrative to gaps.

**Confidence:** High  
**Depends on:** Step 1 (conceptually — can draft in parallel, but finalize Step 3 wording after checklist exists)

**Files:**
- `SKILL.md`

**Changes:**

1. **Behavioral Principles** — Add a principle: document what was checked; the Audit Coverage section is part of the evidence chain (not optional when producing a full report).
2. **Step 3 — Research** — After “How to research” (or at end of Step 3): short bullet block — for each canonical check applicable to this tier/installable, record status + minimal source detail for the coverage table as research proceeds.
3. **Step 5 — Verdict** — After the decision tree block: if **two or more** checks are **Not available** (failed API, blocked network — not tier-skipped), add guidance to mention reduced **coverage** in **Recommendation** (not to change PASS/FAIL semantics of APPROVED/CONDITIONAL/REJECTED). Clarify tier-skipped checks do not count toward that threshold.

**Rationale:** Connects behavior to proposal without merging “confidence” into the verdict label.

**Verification:** Grep `SKILL.md` for new subsection titles; read for internal consistency with Step 6.

**If this fails:** Revert `SKILL.md` hunks.

---

### Step 3: Step 6 report template — Audit Coverage + confidence

**Objective:** Add the structured section and template text.

**Confidence:** High  
**Depends on:** Step 1, Step 2

**Files:**
- `SKILL.md`

**Changes:**

Insert **after** the Reliability table template and **before** `## Risk Flags`:

- `## Audit Coverage`
- One-line **Audit confidence** definition, e.g.  
  `**Audit confidence (coverage):** High | Moderate | Low — <short formula referencing completed vs skipped-by-tier vs unavailable>`  
  Rules in prose:
  - **High:** All tier-appropriate checks completed or legitimately N/A; at most one **Not available** that is non-critical (define “critical” rows by reference to criteria.md — e.g., CVE scan must not be unavailable for Standard/Deep).
  - **Moderate:** One–two unavailable non-tier-skips, or one critical-adjacent gap.
  - **Low:** Three+ unavailable, or any tier-required check missing/not done without valid skip.
- Table template with columns: `Check | Status | Source or notes` and one example row per status type.
- Explicit sentence: **Audit confidence reflects how completely the tier-appropriate checklist was executed — not that the installable is free of vulnerabilities.**

For **Tier 1**, add: include only applicable rows (typically 3–6); do not list full Standard/Deep rows as “Skipped” if the table would become noise — use the canonical list’s Tier 1 minimal set from `criteria.md`.

**Rationale:** Implements Option B; avoids Option C clutter.

**Verification:** Template renders in order: Summary → Security → Reliability → Audit Coverage → Risk Flags.

**If this fails:** Revert Step 6 block.

---

### Step 4: Eval assertions

**Objective:** Catch regressions where agents omit coverage.

**Confidence:** Medium  
**Depends on:** Step 3 (stable headings)

**Files:**
- `evals/evals.json`

**Changes:**

- Add to eval `id: 1` (Standard tier — richer report): assertions for `## Audit Coverage` (or normalized substring) and for “Audit confidence” / “coverage” concept.
- Optionally add a lightweight assertion to eval `id: 0` that Tier 1 report still includes Audit Coverage (short table) — if that tightens Tier 1 too much, restrict to eval `id: 1` only.

**Rationale:** Proposal explicitly asked for eval coverage.

**Verification:** Eval harness still runs; assertions align with template strings.

**If this fails:** Remove or soften assertion text to match actual generated reports after a sample run.

---

## Verification Plan

### Automated Checks
- [ ] Valid JSON in `evals/evals.json` after edits
- [ ] Manual spot-check: run one eval prompt mentally against new template — coverage section fits Tier 1 and Tier 2

### Manual Verification
- [ ] Read `SKILL.md` Step 6 start-to-finish — no duplicate `##` numbering issues
- [ ] Confirm `criteria.md` checklist matches Step 6 example rows

### Acceptance Criteria Validation

| Criterion | How to Verify | Expected Result |
|-----------|---------------|-------------------|
| Coverage section in template | Open `SKILL.md` Step 6 | Audit Coverage appears between Reliability and Risk Flags |
| Canonical tier rows | Open `criteria.md` | New section lists tier-specific expectations |
| Evals reference coverage | Open `evals.json` | New assertions present on at least one eval |

---

## Rollback Plan

1. Revert commits or restore the three files from backup / VCS.
2. If only evals fail: strip new assertions first, keep skill changes.

---

## Notes

### Risks
- **Eval brittleness:** Assertions too strict → tune `contains_concept` vs `contains_string`.
- **Proposal still Draft:** Execution should wait for acceptance or user sign-off.

### Open Questions (resolved for this plan)
| Question | Resolution for this plan |
|----------|---------------------------|
| Confidence vs verdict | Informational only under Audit Coverage; optional Recommendation note if 2+ unavailable |
| Table placement | After Security + Reliability, before Risk Flags |
| Canonical checklist | Defined in `criteria.md` Step 1 of this plan |

### Open Questions (deferred)
- Should `None found` become `No issues in checked sources` — separate micro-projex if desired.
- Re-audit comparison lines — future enhancement.

---

## Repo / commit note

`install-auditor` at the skill path is **not** a git repository in this environment. Before `/execute-projex`, initialize git at the skill root or place the plan in whichever repo tracks this skill, then commit the plan per projex workflow.
