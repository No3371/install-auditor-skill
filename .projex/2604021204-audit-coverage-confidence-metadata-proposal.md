# Audit Coverage & Confidence Metadata

> **Status:** Draft
> **Created:** 2026-04-02
> **Author:** Claude (Opus 4.6)
> **Related Projex:** 2604021200-reliability-accuracy-improvements-imagine.md

---

## Summary

Add a structured "Audit Coverage" section to every install-auditor report, showing exactly which checks were performed, which were skipped (and why), and which were unavailable. This is the single highest-leverage improvement for report accuracy — it transforms ambiguous "None found" into precise, auditable evidence chains.

---

## Problem Statement

### Current State

The report template (SKILL.md Step 6) has Security and Reliability tables that show findings:

```
| CVEs / Advisories | None found |
| Supply Chain Risk | Low — reason |
```

But there is no section showing *what was actually checked* to arrive at those findings. Specific gaps:

- **"None found" is ambiguous.** It reads identically whether the auditor checked 4 databases or ran one web search that returned irrelevant results.
- **Skipped checks are invisible.** Tier 1 audits deliberately skip dependency tree scanning and source code review — by design. But the report doesn't document this. A reader can't distinguish "skipped by design" from "forgotten."
- **Failed lookups disappear.** If the OpenSSF Scorecard API returns 404, the report either omits the section or says "Not available" with no context about what was attempted.
- **The verdict doesn't account for data gaps.** The decision tree treats missing data the same as clean data. A package with "no CVEs found (checked 3 databases)" and "no CVEs found (web search returned nothing)" get the same verdict.

### Gap / Need / Opportunity

Reviewers reading an audit report today cannot assess its thoroughness. They must trust that the agent did a complete job — but they have no evidence of what "complete" means for that specific audit. This is the opposite of how security audits should work: the audit trail matters as much as the findings.

Adding coverage metadata solves this with minimal disruption. The findings tables stay the same. A new section makes the evidence chain explicit.

### Why Now?

The other proposals in this batch (`2604021201-multi-db-vulnerability-correlation-proposal.md`, `2604021202-algorithmic-typosquat-detection-proposal.md`, `2604021203-transitive-dependency-auditing-proposal.md`) all add new data sources and checks. As the number of possible checks grows, the need to track which ones were actually performed becomes more urgent. Coverage metadata should ship alongside or before the new capabilities — otherwise the new tools add power without accountability.

---

## Proposed Change

### Overview

Introduce a standardized "Audit Coverage" section in the report template, a defined status vocabulary for checks, and an optional confidence indicator derived from coverage completeness.

### Approach Options

#### Option A: Coverage Table Only (Minimal)

- **Description:** Add an `## Audit Coverage` section to the report template with a table:

```markdown
## Audit Coverage
| Check | Status | Source |
|-------|--------|--------|
| Registry metadata | Done | npm API via registry-lookup.ps1 |
| CVE scan | Done | OSV, GHSA |
| Typosquat check | Done | Edit distance vs top-500 npm |
| Dependency tree | Skipped (Tier 2) | — |
| Source code review | Skipped (Tier 2) | — |
| OpenSSF Scorecard | Not available | API returned 404 for github.com/org/repo |
| Web search: incidents | Done, 0 results | "express npm vulnerability 2026" |
| Install script review | N/A (no scripts) | package.json checked |
```

- **Status vocabulary:** `Done` | `Done, N results` | `Skipped (reason)` | `Not available (detail)` | `N/A (reason)`
- **Pros:** Simple, high-value, no behavioral changes. Readers see what was checked at a glance. Tier-appropriate skips are documented and legitimate. Failed lookups are visible.
- **Cons:** No structured way to connect coverage to verdict confidence. Just a table — the agent could fill it out inconsistently.
- **Effort:** Low — template change + behavioral guidance in SKILL.md.

#### Option B: Coverage Table + Confidence Indicator

- **Description:** Coverage table (as in Option A) plus a computed confidence line:

```markdown
**Audit confidence:** High (7/8 checks completed, 1 skipped by tier)
```

or:

```markdown
**Audit confidence:** Moderate (5/8 checks completed, 2 unavailable, 1 skipped by tier)
```

Confidence levels: **High** (all tier-appropriate checks completed), **Moderate** (1-2 checks unavailable/failed), **Low** (3+ checks unavailable/failed or critical check missing).

- **Pros:** Gives reviewers a quick signal without reading the full table. Connects coverage gaps to verdict reliability. Makes it explicit that a Tier 1 audit with all checks done is "High confidence" even though it skipped deep checks — because those skips are tier-appropriate.
- **Cons:** The confidence label could be misleading — "High confidence" based on coverage doesn't mean "high confidence there are no vulnerabilities." Needs careful framing. Adds a computation step.
- **Effort:** Medium — template change + confidence computation logic in SKILL.md behavioral instructions.

#### Option C: Full Coverage + Confidence + Inline Annotations

- **Description:** Coverage table, confidence indicator, AND inline annotations in the findings tables:

```markdown
| CVEs / Advisories | None found *(checked: OSV, GHSA, npm audit)* |
| Supply Chain Risk | Low *(based on: registry metadata, web search)* |
| Dependency Risk | Low *(12 direct deps scanned; transitive scan skipped — Tier 2)* |
```

- **Pros:** Maximum transparency — every finding cell shows its evidence chain. No need to cross-reference the coverage table with individual findings.
- **Cons:** Report becomes visually noisy. Tier 1 quick audit reports would be cluttered with annotations that outweigh the findings. Duplicates information between coverage table and finding rows.
- **Effort:** Medium — template changes throughout, more complex behavioral guidance.

### Recommended Approach

**Option B (Coverage Table + Confidence Indicator).** The table provides the detail; the confidence indicator provides the quick signal. Together they answer "how thorough was this audit?" without cluttering the findings tables. The confidence label is scoped explicitly to *coverage completeness*, not to *security assurance* — this distinction goes in the behavioral principles.

For Tier 1 quick audits: the coverage table is shortened to the 3-4 checks actually performed. No bloat.

---

## Impact Analysis

### Affected Areas

- **`SKILL.md` Step 6 (Report template)** — Add `## Audit Coverage` section with table template and confidence indicator. Place it after the findings tables, before Risk Flags.
- **`SKILL.md` Step 3 (Research)** — Add instruction: "As you perform each check, note its status for the coverage table — Done, Skipped, Not available, or N/A."
- **`SKILL.md` Behavioral Principles** — Add principle: "Document what you checked. The coverage table is not optional — it's the evidence chain that gives your findings credibility."
- **`SKILL.md` Step 5 (Verdict)** — Add guidance: "If 2+ checks were unavailable (not skipped-by-tier), consider noting reduced confidence in the verdict section."
- **`references/criteria.md`** — Add a section defining the standard check list per tier (what's expected to be "Done" vs. legitimately "Skipped" for each tier).
- **`evals/evals.json`** — Add assertions checking for coverage table presence and accuracy.

### Dependencies

- No external dependencies. This is a template and behavioral change — no new APIs, no new scripts.
- Synergizes with all other proposals in this batch: as new checks are added (multi-DB vulnerability, typosquat detection, dependency scanning), they become rows in the coverage table.

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Agent fills coverage table inconsistently | Medium | Medium — undermines the whole point | Define the exact check list per tier in criteria.md. Make the list canonical, not ad-hoc. |
| "High confidence" misread as "definitely safe" | Medium | High — false assurance | Explicit framing: "Confidence reflects coverage completeness, not absence of risk. Unknown vulnerabilities are outside any audit's scope." |
| Report bloat for Tier 1 | Low | Low — quick audits should stay quick | Tier 1 coverage table is 3-4 rows. Template specifies: "For Tier 1, include only checks actually performed." |
| Users ignore the coverage table | Medium | Low — the table still serves future auditors and re-audits | The confidence indicator at the top is the quick-glance summary. Detailed table is for those who want it. |

### Breaking Changes

None. Additive change to the report template. Existing report sections remain unchanged. New section provides additional context without altering findings or verdicts.

---

## Open Questions

- [ ] Should the confidence indicator affect the verdict itself? (e.g., "APPROVED, Moderate confidence" vs. plain "APPROVED") Or should it remain informational only?
- [ ] What is the canonical check list per tier? (This needs to be defined precisely — see criteria.md impact above.)
- [ ] Should the coverage table go before or after the findings tables? Before = readers see context first. After = readers see findings first and can check the evidence chain if needed.
- [ ] How should re-audits reference previous coverage? (e.g., "Last audit (2026-03-15) had High confidence. This re-audit adds dependency scanning not available previously.")
- [ ] Should the `"None found"` wording in existing fields be changed to `"No issues in checked sources"` or similar, even without the full coverage table?

---

## Next Steps

If accepted:
1. Define canonical check list per tier in `references/criteria.md`
2. Update report template in `SKILL.md` Step 6
3. Update behavioral principles and research instructions
4. Add eval assertions for coverage table presence
5. Coordinate with other accepted proposals — each new capability becomes a row in the coverage table
