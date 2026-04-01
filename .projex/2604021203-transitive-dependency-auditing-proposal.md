# Transitive Dependency Auditing

> **Status:** Draft
> **Created:** 2026-04-02
> **Author:** Claude (Opus 4.6)
> **Related Projex:** 2604021200-reliability-accuracy-improvements-imagine.md

---

## Summary

Extend the install-auditor beyond dependency counting to actually check transitive dependencies for known vulnerabilities. A tiered approach — direct-dependency scans for Tier 2, full tree resolution for Tier 3 — turns the report's "Dependency Risk" field from a guess into an evidence-backed assessment.

---

## Problem Statement

### Current State

The `scripts/registry-lookup.ps1` script reports `dependencyCount` — a single number from registry metadata. The `SKILL.md` § 4.3 instructs the agent to verify that "dependencies are themselves clean (no known-bad transitive deps)." But there's no mechanism to actually do this:

- No script resolves the dependency tree
- No API is queried for vulnerability data on dependencies
- The agent has no way to enumerate transitive dependencies without installing the package
- The "Dependency Risk" row in the report template gets filled with Low/Medium/High based on the agent's general impression

### Gap / Need / Opportunity

A package with 3 direct dependencies might pull in 400 transitive ones. The `event-stream` incident (2018) was a malicious transitive dependency — the direct dependency (`event-stream`) was compromised via a new maintainer who added `flatmap-stream` as a transitive dep. The current auditor would have counted dependencies but never looked inside.

The gap: the skill tells the agent to check something it has no tools to check. The agent either skips the check silently or makes a vague assessment. Neither is acceptable for a security audit.

### Why Now?

OSV.dev supports batch queries (`POST /v1/querybatch`) — up to 1,000 packages in a single API call. This makes checking even large dependency trees feasible without hitting rate limits. Package managers (`npm ls --all --json`, `pip show --verbose`, `pipdeptree --json`) can resolve trees programmatically. The infrastructure exists; the auditor just doesn't use it.

---

## Proposed Change

### Overview

Add dependency tree resolution and vulnerability scanning as a structured audit step, scaled by tier: direct-dependency scanning for Tier 2 (quick, ~5-20 API calls) and full transitive scanning for Tier 3 (thorough, uses batch APIs).

### Approach Options

#### Option A: Shallow Scan Only (Direct Dependencies)

- **Description:** For each direct dependency listed in the registry metadata, query OSV for known vulnerabilities. Report findings as: "8 direct deps checked, 0 with known CVEs" or "8 direct deps checked, 1 with HIGH CVE (CVE-2024-XXXX in `minimist`)."
- **Pros:** Simple. 5-20 API calls per audit. No need to install the package or resolve the full tree. Works across all ecosystems (direct deps are in registry metadata). Fast enough for Tier 2.
- **Cons:** Misses transitive dependencies entirely — the `event-stream` attack vector would be invisible. Provides a false sense of security for packages with deep trees.
- **Effort:** Low — extend `registry-lookup.ps1` to iterate over `dependencies` and query OSV for each.

#### Option B: Full Tree Resolution + Batch Scan

- **Description:** Use package manager commands to resolve the complete dependency tree (`npm ls --all --json`, `pipdeptree --json-tree`). Collect all package names + versions. Batch-query OSV (`/v1/querybatch`). Report: "12 direct, 147 transitive. 0 with known CVEs" or flag specific vulnerable packages with their depth in the tree.
- **Pros:** Complete coverage. Catches transitive vulnerabilities. OSV batch API handles up to 1,000 packages in one call. Provides the most accurate "Dependency Risk" assessment possible.
- **Cons:** Requires the package manager to be available (npm, pip, etc.) — not always true in the audit context if the package isn't installed yet. For some ecosystems, tree resolution requires downloading/installing. Some packages have enormous trees (create-react-app: 1,400+). Report noise from many low-severity transitive CVEs.
- **Effort:** High — tree resolution per ecosystem, batch query logic, report formatting for potentially large results.

#### Option C: Tiered Approach (Shallow for T2, Full for T3)

- **Description:** Tier 2 gets Option A (direct deps from registry metadata → OSV query). Tier 3 gets Option B (full tree resolution → batch scan). Tier 1 gets dependency count only (status quo). Each tier's report indicates what level of dependency checking was performed.
- **Pros:** Matches the auditor's existing tiered philosophy — don't over-audit low-risk, don't under-audit high-risk. Tier 2 is achievable without installing the package. Tier 3's deeper check is justified by the package's risk profile.
- **Cons:** Two different code paths. Tier 3 still has the "requires package manager" constraint. More complexity in the report template (different detail levels per tier).
- **Effort:** Medium-High — Option A for the base, Option B as an add-on for Tier 3.

### Recommended Approach

**Option C (Tiered).** Aligns with the auditor's existing tier structure. Tier 2 shallow scanning is high-ROI: it catches the most impactful vulnerabilities (direct deps are the closest attack surface) with minimal infrastructure. Tier 3 full-tree scanning is reserved for high-risk packages where the extra effort is justified.

For Tier 3 tree resolution: use `npm ls --all --json` (npm), `pip show` + `pipdeptree` (Python) where the package manager is available. If unavailable, fall back to shallow scan and note the limitation in the coverage table.

---

## Impact Analysis

### Affected Areas

- **`scripts/registry-lookup.ps1`** — Extend to extract direct dependency list from registry metadata and query OSV for each (Tier 2 path)
- **New script or script section** — Tier 3 tree resolution logic per ecosystem
- **`SKILL.md` Step 3 (Research)** — Add dependency scanning as an explicit research step, not a vague instruction
- **`SKILL.md` Step 2 (Tier definitions)** — Update tier descriptions to specify dependency checking depth per tier
- **`SKILL.md` Step 6 (Report template)** — Update "Dependency Risk" row to show evidence: deps checked, sources, findings
- **`references/criteria.md` § 4.3** — Update to reflect actual checking mechanism instead of aspirational instruction
- **`references/criteria.md` § 4.5 Cumulative Risk** — Factor in transitive dependency findings

### Dependencies

- OSV.dev batch query API (free, no auth)
- Registry APIs already used by `registry-lookup.ps1` (for direct dependency lists)
- Package manager CLIs for Tier 3 only (`npm`, `pip`, `cargo` — present if the user is installing for that ecosystem)
- Coordinates with `2604021201-multi-db-vulnerability-correlation-proposal.md` — the OSV integration proposed there would be reused here

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Dependency tree explosion (1,000+ packages) | Medium | Low — OSV batch handles 1,000 per call | Cap at 1,000; note in report if tree exceeds limit |
| Report noise from many low-severity transitive CVEs | High | Medium — list of 12 MEDIUM CVEs in transitive deps creates noise without clear action | Report only HIGH/CRITICAL for transitive deps. Summarize MEDIUM as count. Focus on actionability. |
| Package manager not available for Tier 3 tree resolution | Medium | Low — falls back to shallow scan | Graceful degradation. Note in coverage table: "Full tree resolution unavailable — shallow scan performed." |
| Tree resolution requires package installation | Medium (pip) | Medium — can't install untrusted package to audit it | For pip: use `pip download --no-deps` + manual metadata parsing, or use `pip index versions` + PyPI JSON API. Never install the audited package. |
| Stale dependency data in registry metadata | Low | Low — registry metadata is usually current for latest version | Pin to specific version when querying |

### Breaking Changes

None. Additive change. Existing reports gain more data in the Dependency Risk row. The verdict decision tree doesn't change structure — it gains better data inputs. Tier 1 behavior is unchanged.

---

## Open Questions

- [ ] For Tier 3 full-tree scanning: is it safe to run `npm ls --all --json` in a temp directory with just a `package.json` referencing the target package? This resolves the tree without installing into the user's project.
- [ ] Should the auditor flag *all* transitive CVEs or only those in the "reachable" dependency path? (Reachability analysis is much harder but reduces noise.)
- [ ] What's the right threshold for "dependency age heuristic"? 2 years? 3 years? Should age alone be a flag, or only age + no CVE checks available?
- [ ] How should the report handle packages where the transitive tree is clean but *enormous* (1,000+ deps)? Is tree size itself a risk signal?
- [ ] Should dependency findings affect the verdict directly (e.g., HIGH CVE in direct dep → CONDITIONAL), or only inform the human reviewer?

---

## Next Steps

If accepted:
1. Create Plan projex for implementation
2. Implement Tier 2 (shallow scan) first — highest ROI, fewest constraints
3. Validate against packages with known transitive vulnerabilities
4. Add Tier 3 tree resolution for npm (most common ecosystem)
5. Extend to pip, then remaining ecosystems
6. Update report template and criteria rubrics
7. Add eval cases testing dependency scanning behavior
