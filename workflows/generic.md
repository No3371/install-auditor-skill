<!--
workflows/generic.md - Phase 1 universal fallback workflow.
Contains the evidence acquisition & scoring pipeline (Identify / Evidence /
Subject Rubric / Subject Verdict Notes) inherited from the pre-pivot
monolithic SKILL.md. Verdict tree and report shape live in the dispatcher
(SKILL.md, Step N), not here.

This file is the Phase 1 fallback for every subject type. Specific workflows
(registry-package.md, browser-extension.md, etc.) land in Phases 2-4 and
will replace generic.md for their respective types.
-->

# Generic Workflow (Phase 1 Universal Fallback)

This workflow is the Phase 1 fallback for every subject type in the dispatch
table. It carries the evidence acquisition and scoring pipeline inherited
from the pre-pivot monolithic SKILL.md. After producing findings here,
return to `SKILL.md` Step N for the shared verdict tree and report shape.

Sections below use the Phase 1 workflow template: **Identify / Evidence /
Subject Rubric / Subject Verdict Notes**. Step numbers from the pre-pivot
monolith are preserved as secondary anchors so existing references keep
resolving.

---

## Identify

*(formerly Step 1 — Identify the Installable)*

Gather before auditing:

1. **Full name and version** (exact package name, extension ID, or binary name)
2. **Source / registry** (npm, PyPI, Chrome Web Store, GitHub, vendor site, etc.)
3. **Installation command or URL** (what the user is about to run or click)
4. **Stated purpose** (what the user says they need it for)
5. **Target environment** (dev machine, CI server, Docker container, browser profile)
6. **Checksum / signature** (if available — SHA hash, GPG signature, code signing cert)

If any of 1–5 are missing, ask before proceeding. Item 6 is optional but its presence increases trust.

---

## Evidence — Part A: Triage (Pick the Audit Tier)

*(formerly Step 2 — Triage)*

Not every package needs the same level of scrutiny. A quick triage up front prevents wasting 10 minutes auditing `react` while also ensuring obscure packages get proper attention.

**Run the `scripts/registry-lookup.ps1` script** first to get hard data (downloads, maintainer count, last publish date, known vulnerabilities). Then apply the triage logic:

### Tier 1 — Quick Audit (well-known, high-trust)

Use when **all** of these are true:
- From an official registry (npm, PyPI, crates.io, etc.)
- Published by a verified org or well-known maintainer
- High adoption (>100K weekly downloads or >5K GitHub stars)
- No known CVEs in current version
- No recent maintainer changes

**Quick audit scope:** Confirm version is current, check for CVEs, verify the name isn't a typosquat, note the license. Write a short report. Takes ~2 minutes.

### Tier 2 — Standard Audit (moderate trust signals)

Use when the package has *some* trust signals but doesn't meet all Tier 1 criteria:
- Moderate adoption (1K–100K weekly downloads)
- Individual maintainer with history
- No red flags but limited track record

**Standard audit scope:** Full research (Step 3) + structured report. This is the default tier.

### Tier 3 — Deep Audit (low trust or high risk)

Use when **any** of these are true:
- Very low adoption (<1K weekly downloads) and not a known niche tool
- Single anonymous maintainer, new account
- Published within last 72 hours with no prior history
- Requests unusual permissions for its stated purpose
- Will run in CI/CD with access to secrets
- User is asking about a package they received via DM, email link, or unfamiliar source

**Deep audit scope:** Everything in Standard, plus source code review of install scripts, dependency tree audit, and explicit alternatives comparison.

---

## Evidence — Part B: Research

*(formerly Step 3 — Research)*

The purpose of research is to answer these questions with *current* data (not training data alone):

1. **Is this the real package?** (typosquatting check — compare name character by character against the legitimate package)
2. **Are there known vulnerabilities?** (CVEs, security advisories, supply chain incidents)
3. **Who maintains it and are they still active?** (maintainer identity, last activity, ownership transfers)
4. **What permissions does it need and are they justified?** (least privilege analysis)
5. **Is anyone reporting problems?** (malware reports, data collection concerns, removal from stores)
6. **Is the project healthy?** (maintenance status, issue responsiveness, deprecation notices)

### How to research

**Start with the registry-lookup script** — it gives you download counts, maintainer info, last publish date, and vulnerability data from official APIs. This is faster and more reliable than web search for factual data.

**Then use web search** to find things the APIs don't cover — security blog posts, incident reports, community discussions, removal notices. Focus searches on:
- The package name + "vulnerability", "malware", "supply chain"
- The package name + "deprecated", "abandoned", "alternative"
- For browser extensions: whether it's been removed from stores
- For Docker images: Trivy/Grype scan results
- For GitHub Actions: whether it's pinned to commit SHAs

**Check the OpenSSF Scorecard** if available (via `api.securityscorecards.dev`). Scores below 4/10 are a significant negative signal. Scores above 7 are positive (but not sufficient alone).

**Collect all source URLs** as you research — they go in the report's Sources section.

### Audit coverage tracking

As you run each check, record its outcome for the **Audit Coverage** table (rendered in the dispatcher at `SKILL.md` Step N):

- Use the canonical row labels from `references/criteria.md` **Audit Coverage Checklist** for this tier and installable type.
- For each row: **Status** (`Done`, `Done, N results`, `Skipped (…)`, `Not available (…)`, `N/A (…)`) plus **Source or notes** (script name, API, search query, or why skipped).
- **Tier-skipped** checks (e.g., deep web search in Tier 1) are **not** the same as **Not available** — the latter means you tried and could not get data.

### For Tier 1 (Quick Audit)
Only confirm: no CVEs, not a typosquat, license is compatible. Skip the deep web research.

### For Tier 3 (Deep Audit)
Additionally: review install scripts (`preinstall`, `postinstall`), check for obfuscated code, audit the dependency tree for known-bad transitive dependencies, and look for behavioral red flags in source code (credential harvesting, unexpected network calls, encoded strings).

---

## Subject Rubric — Evaluate

*(formerly Step 4 — Evaluate; defers to `references/criteria.md` for the shared rubric)*

Score against these criteria. See `references/criteria.md` for detailed rubrics.

### 4.1 Provenance & Identity
- Source is an official registry or verified publisher
- Package name matches expected (no typosquatting)
- Publisher identity is verifiable
- Version is not suspiciously new or anomalous

### 4.2 Maintenance & Longevity
- Last commit/release within 12 months (or explicitly stable/archived)
- Active issue tracker with responses
- Clear ownership (not single anonymous maintainer for critical tool)
- No deprecation warnings or unaddressed successor packages

### 4.3 Security Track Record
- No unpatched CVEs in current version
- No history of supply chain compromise
- No reports of malicious behavior
- Dependencies are themselves clean (no known-bad transitive deps)

### 4.4 Permissions & Access
- Requested permissions match stated functionality (least privilege)
- No unexplained network access to external servers
- No filesystem access beyond stated need
- No credential or environment variable harvesting reported

### 4.5 Reliability & Compatibility
- Compatible with target OS/runtime versions
- License is compatible with org policy (see `references/licenses.md`)
- Adoption signal appropriate for use case
- No known conflicts with existing toolchain

### 4.6 Alternatives
- Is there a better-maintained or more trusted alternative that does the same thing?
- Is this functionality already built into the existing toolchain?
- If flagging an alternative, briefly compare: security posture, maintenance, adoption

To find alternatives: search `"<package name> vs"` or `"<package name> alternative"`, check the package's GitHub README for "similar projects" sections, and check registry categories.

---

---

## Subject Verdict Notes

Generic has no subject-specific verdict overrides. After completing
Identify / Evidence / Subject Rubric above, return to `SKILL.md` Step N for
the shared verdict tree and audit-coverage report shape.
