<!-- workflows/generic.md - Low-confidence fallback. Routes here only when Step 0
classifier produces LOW confidence (conflicting signals or no signals). Every
resolved subject type has its own specific workflow (Types 1-9). -->

# Generic Fallback Workflow (Low-Confidence Only)

> **WARNING — Low-confidence classification.** The dispatcher could not
> confidently identify the subject type. This workflow attempts to resolve the
> ambiguity; if it cannot, it runs a defensive minimum audit with reduced
> coverage. Reports produced here carry a low-confidence warning.

After completing all sections below, return to `SKILL.md` Step N for the
shared verdict tree and audit-coverage report shape.

---

## Phase 1 — Subject Probe

Examine available signals to determine what was installed:

1. **Read the classifier output** — the `Rationale` field names which signals
   fired and which types were candidates. Record the top 1-2 candidates.
2. **Inspect the install artifact** — URL, command, manifest, or file extension.
   Look for any signal the classifier may have missed.
3. **Check the user's stated purpose** — often reveals the subject type even
   when technical signals are ambiguous.

---

## Phase 2 — User Clarification

Present findings from Phase 1 and ask the user to resolve the ambiguity:

> "The classifier could not confidently determine the subject type. Based on
> available signals, the best candidates are **[candidate 1]** and
> **[candidate 2]**. Can you confirm which type this is, or provide additional
> context (e.g., where you found it, what it does, how it installs)?"

**If the user clarifies** → re-route to the appropriate specific workflow:
- Update the classifier output to reflect the user-confirmed type
- Set confidence to `high` with `user override: <verbatim>` in Rationale
- Route to `workflows/<confirmed-type>.md` and restart the audit there
- **Do not continue in this file**

**If the user cannot clarify** (or context is non-interactive) → proceed to Phase 3.

---

## Phase 3 — Defensive Minimum Audit

Run a reduced checklist — enough signal for the verdict tree, nothing more:

| Check | What to do |
|-------|------------|
| **Identity verification** | Confirm name matches a known/legitimate entity; check for typosquatting against plausible real names |
| **CVE / advisory lookup** | Search OSV, GHSA, and NVD for the package name + version; note any unpatched findings |
| **Maintenance pulse** | Last release date, last commit, maintainer count — flag if abandoned (>24 months) or single anonymous maintainer |
| **Permissions smell-test** | List requested permissions / access scope; flag anything disproportionate to stated purpose |

Skip: full triage tiers, deep source review, transitive dependency audit, OpenSSF
Scorecard, alternatives comparison. These belong in specific workflows.

Record each check in the **Audit Coverage** table using status values from
`references/criteria.md`. Non-executed checks → `Skipped (generic fallback)`.

---

## Phase 4 — Low-Confidence Warning

Stamp the following in the report:

- **Report header:** add `**Classification confidence:** Low — generic fallback` below the Subject type line
- **Recommendation section:** prepend: *"This audit used the generic fallback workflow (low classification confidence). Coverage is reduced. Consider re-running with an explicit subject type for full coverage."*

---

## Subject Verdict Notes

No subject-specific verdict overrides. After completing Phases 1-4, return to
`SKILL.md` Step N for the shared verdict tree and audit-coverage report shape.
