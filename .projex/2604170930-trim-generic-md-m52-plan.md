# Trim `generic.md` to True Fallback (M5.2)

> **Nav:** 2604070218-install-auditor-subject-typed-redesign-nav.md
> **Status:** Ready
> **Created:** 2026-04-17
> **Author:** projex-agent
> **Source:** Nav M5.2 — Phase 5 "Default-Off Generic"
> **Related Projex:** 2604160430-tighten-classifier-m51-plan.md (predecessor — M5.1 tightened routing; M5.2 trims the file itself)
> **Worktree:** No

---

## Summary

Replace the 181-line Phase 1 monolith in `workflows/generic.md` with a ~70-line true low-confidence fallback. The new workflow: (1) identifies the subject from available signals, (2) asks the user to clarify the subject type so the dispatcher can re-route to a specific workflow, (3) runs a defensive minimum audit if the user cannot clarify, and (4) stamps a visible warning that this is a reduced-coverage fallback. Also updates the stale description in `SKILL.md` Reference Files.

**Scope:** `workflows/generic.md` (rewrite), `SKILL.md` line 219 (description update).
**Estimated Changes:** 2 files, 2 regions.

---

## Objective

### Problem / Gap / Need

`generic.md` still carries the full pre-pivot monolith: 6-item Identify checklist, 3-tier triage (Quick/Standard/Deep), full Research section with registry-lookup script instructions, 6-category Subject Rubric (Provenance, Maintenance, Security, Permissions, Reliability, Alternatives), and Subject Verdict Notes. This content is now redundant — every specific workflow (Types 1-9) has its own specialized version of these sections. When `generic.md` fires on a low-confidence classification, the monolith runs a full audit against the wrong abstraction: it treats the subject as a generic installable when the real problem is that the classifier couldn't determine what it is. The right behavior is to surface the uncertainty, try to resolve it, and only then run a minimal defensive audit as last resort.

Additionally, `SKILL.md` line 219 still describes generic.md as "Phase 1 universal fallback workflow (evidence acquisition + scoring)" — a stale label from before all 9 workflows went live.

### Success Criteria

- [ ] `generic.md` replaced with fallback workflow containing exactly these phases: (1) Subject Probe, (2) User Clarification, (3) Defensive Minimum Audit, (4) Low-Confidence Warning
- [ ] Clarification step presents the classifier's best-guess types and asks user to confirm or specify — if user clarifies, workflow instructs the dispatcher to re-route to the specific workflow
- [ ] Defensive minimum audit covers only: identity verification, CVE check, maintenance pulse, and permissions smell-test — no triage tiers, no full rubric
- [ ] Warning note is stamped in the report header and Recommendation section
- [ ] Old monolith content (triage tiers, full research, full rubric) is removed — not commented out
- [ ] `SKILL.md` Reference Files description updated from stale Phase 1 label
- [ ] File is <=80 lines (down from 181)

### Out of Scope

- Changing the classifier routing logic (done in M5.1)
- Changing the dispatch table in SKILL.md
- Modifying any of the 9 specific workflows
- Adding eval cases for the generic fallback (future work)
- Read-cost measurement (M5.3)

---

## Context

### Current State

`workflows/generic.md` (181 lines) contains:
- HTML comment header (lines 1-11) — references "Phase 1 universal fallback"
- Intro paragraph (lines 13-24) — "Phase 1 fallback for every subject type"
- **Identify** section (lines 26-41) — 6-item checklist, generic
- **Evidence Part A: Triage** (lines 43-83) — 3-tier system (Quick/Standard/Deep)
- **Evidence Part B: Research** (lines 85-127) — full research instructions, registry-lookup, OpenSSF, web search
- **Subject Rubric** (lines 129-170) — 6 evaluation categories (4.1–4.6)
- **Subject Verdict Notes** (lines 172-181) — empty pass-through to SKILL.md Step N

`SKILL.md` line 219: `- \`workflows/generic.md\` — Phase 1 universal fallback workflow (evidence acquisition + scoring)` — stale.

### Key Files

| File | Role | Change Summary |
|------|------|----------------|
| `workflows/generic.md` | Low-confidence fallback workflow | Full rewrite: monolith → probe + clarify + defensive audit + warning |
| `SKILL.md` | Dispatcher / entry point | Line 219 description update |

### Dependencies

- **Requires:** M5.1 complete (three-tier confidence model live) — done 2026-04-16
- **Blocks:** M5.3 (read-cost measurement) — M5.2 reduces generic.md token cost, which M5.3 measures

### Constraints

- Must preserve the workflow template convention: sections return to `SKILL.md` Step N for verdict tree and report shape
- Must not break the dispatch table reference (`workflows/generic.md` path unchanged)
- Defensive audit must still produce enough signal for the verdict tree to function (identity, CVEs, maintenance, permissions at minimum)

### Assumptions

- The classifier's Rationale field contains enough information (which signals conflicted, which types were candidates) to present useful clarification options to the user
- Users can clarify the subject type in most cases — the defensive-only path is the exception, not the rule
- The shared verdict tree in SKILL.md Step N works with reduced evidence (it already handles "Not available" rows in Audit Coverage)

### Impact Analysis

- **Direct:** `workflows/generic.md` (rewrite), `SKILL.md` (1-line description)
- **Adjacent:** None — no other file references generic.md's internal sections
- **Downstream:** Audit reports produced via generic fallback will have reduced coverage (by design) and a visible warning

---

## Implementation

### Overview

Two-step change: (1) rewrite `generic.md` from scratch as a short fallback workflow with four phases, (2) update the stale reference description in `SKILL.md`.

### Step 1: Rewrite `workflows/generic.md`

**Objective:** Replace the 181-line monolith with a ~70-line fallback workflow.
**Confidence:** High
**Depends on:** None

**Files:**
- `workflows/generic.md`

**Changes:**

Replace entire file content with:

```markdown
<!--
workflows/generic.md - Low-confidence fallback workflow.
Routes here only when Step 0 classifier produces LOW confidence
(conflicting signals or no signals). Not a general-purpose workflow —
every resolved subject type has its own specific workflow (Types 1-9).
-->

# Generic Fallback Workflow (Low-Confidence Only)

> **WARNING — Low-confidence classification.** The dispatcher could not
> confidently identify the subject type. This workflow attempts to resolve
> the ambiguity; if it cannot, it runs a defensive minimum audit with
> reduced coverage. Reports produced here carry a low-confidence warning.

After completing all sections below, return to `SKILL.md` Step N for the
shared verdict tree and audit-coverage report shape.

---

## Phase 1 — Subject Probe

Examine the available signals to determine what was installed:

1. **Read the classifier output** — the `Rationale` field names which signals
   fired and which types were candidates. Record the top 1-2 candidates.
2. **Inspect the install artifact** — URL, command, manifest, or file
   extension. Look for any signal the classifier may have missed.
3. **Check the user's stated purpose** — often reveals the subject type
   even when technical signals are ambiguous.

---

## Phase 2 — User Clarification

Present findings from Phase 1 and ask the user to resolve the ambiguity:

> "The classifier could not confidently determine the subject type.
> Based on available signals, the best candidates are **[candidate 1]**
> and **[candidate 2]**. Can you confirm which type this is, or provide
> additional context (e.g., where you found it, what it does, how it
> installs)?"

**If the user clarifies** → re-route to the appropriate specific workflow:
- Update the classifier output to reflect the user-confirmed type
- Set confidence to `high` with `user override: <verbatim>` in Rationale
- Route to `workflows/<confirmed-type>.md` and restart the audit there
- **Do not continue in this file**

**If the user cannot clarify** (or context is non-interactive) → proceed
to Phase 3.

---

## Phase 3 — Defensive Minimum Audit

Run a reduced checklist — enough signal for the verdict tree, nothing more:

| Check | What to do |
|-------|------------|
| **Identity verification** | Confirm name matches a known/legitimate entity; check for typosquatting against plausible real names |
| **CVE / advisory lookup** | Search OSV, GHSA, and NVD for the package name + version; note any unpatched findings |
| **Maintenance pulse** | Last release date, last commit, maintainer count — flag if abandoned (>24 months) or single anonymous maintainer |
| **Permissions smell-test** | List requested permissions / access scope; flag anything disproportionate to stated purpose |

Skip: full triage tiers, deep source review, transitive dependency audit,
OpenSSF Scorecard, alternatives comparison. These belong in specific workflows
that know the subject type.

Record each check in the **Audit Coverage** table using status values from
`references/criteria.md`. Non-executed checks → `Skipped (generic fallback)`.

---

## Phase 4 — Low-Confidence Warning

Stamp the following in the report:

- **Report header:** add `**Classification confidence:** Low — generic fallback` below the Subject type line
- **Recommendation section:** prepend: *"This audit was performed under the generic fallback workflow due to low classification confidence. Coverage is reduced compared to a type-specific audit. Consider re-running with an explicit subject type for full coverage."*

---

## Subject Verdict Notes

No subject-specific verdict overrides. After completing Phases 1-4 above,
return to `SKILL.md` Step N for the shared verdict tree and
audit-coverage report shape.
```

**Rationale:** The old monolith duplicated what every specific workflow already provides. The new structure surfaces the real problem (unresolved classification), tries to fix it (user clarification → re-route), and only falls back to a minimal defensive audit when clarification fails. The 4-check minimum (identity, CVEs, maintenance, permissions) is the smallest set that gives the verdict tree enough signal to produce a meaningful verdict.

**Verification:** `wc -l workflows/generic.md` should be ~75 lines. File should contain exactly 4 phases. No references to triage tiers, registry-lookup script, or 6-category rubric.

**If this fails:** Revert to the previous version from git: `git checkout HEAD -- workflows/generic.md`

---

### Step 2: Update `SKILL.md` Reference Files description

**Objective:** Fix the stale Phase 1 description on line 219.
**Confidence:** High
**Depends on:** Step 1

**Files:**
- `SKILL.md`

**Changes:**

```
// Before:
- `workflows/generic.md` — Phase 1 universal fallback workflow (evidence acquisition + scoring)

// After:
- `workflows/generic.md` — Low-confidence fallback (subject probe + user clarification + defensive minimum audit)
```

**Rationale:** Description should match the file's actual role post-M5.2.

**Verification:** `grep 'generic.md' SKILL.md` should show "Low-confidence fallback" on line 219, not "Phase 1".

**If this fails:** `git checkout HEAD -- SKILL.md` restores the previous description.

---

## Verification Plan

### Automated Checks

- [ ] `wc -l workflows/generic.md` <= 80 lines
- [ ] `grep -c 'Tier 1\|Tier 2\|Tier 3\|Quick Audit\|Standard Audit\|Deep Audit' workflows/generic.md` = 0 (no triage tiers)
- [ ] `grep -c 'registry-lookup' workflows/generic.md` = 0 (no script references)
- [ ] `grep -c '4\.1\|4\.2\|4\.3\|4\.4\|4\.5\|4\.6' workflows/generic.md` = 0 (no rubric sections)
- [ ] `grep 'generic.md' SKILL.md` shows updated description

### Manual Verification

- [ ] Read through the new `generic.md` end-to-end: phases flow logically, no leftover monolith content
- [ ] Confirm Phase 2 re-route instruction is clear and actionable
- [ ] Confirm Phase 3 checklist produces enough evidence rows for the verdict tree

### Acceptance Criteria Validation

| Criterion | How to Verify | Expected Result |
|-----------|---------------|-----------------|
| Four-phase structure | Read section headers | Phase 1-4 present |
| User clarification with re-route | Read Phase 2 | Clear instruction to re-route on user confirmation |
| Defensive minimum = 4 checks only | Read Phase 3 table | Identity, CVE, Maintenance, Permissions — no more |
| Warning in report | Read Phase 4 | Header line + Recommendation prepend specified |
| No old monolith | grep for triage/rubric terms | Zero matches |
| SKILL.md description updated | grep line 219 | "Low-confidence fallback" |
| <=80 lines | wc -l | <=80 |

---

## Rollback Plan

1. `git checkout HEAD -- workflows/generic.md` — restores pre-M5.2 monolith
2. `git checkout HEAD -- SKILL.md` — restores pre-M5.2 reference description

---

## Notes

### Risks

- **Defensive audit too thin:** 4 checks may miss something a full audit would catch. Mitigation: the Phase 2 clarification step is designed to prevent most audits from reaching Phase 3 at all — re-routing to a specific workflow is the primary outcome.
- **Non-interactive contexts:** If the audit runs in a pipeline or batch context where user clarification isn't possible, Phase 2 is skipped silently. Mitigation: Phase 3 still provides baseline coverage, and the warning in Phase 4 makes the reduced scope visible.

### Open Questions

None.
