---
name: install-auditor
description: >
  Mandatory security and reliability audit for any installable in software development environments.
  Use this skill whenever an employee, developer, or agent wants to install, add, or enable anything
  to a development system — including browser extensions, VS Code/IDE plugins, npm/pip/gem packages,
  desktop applications, CLI tools, Docker images, GitHub Actions, or any third-party software.
  Trigger this skill before allowing any installation to proceed. Also trigger when someone asks
  "is it safe to install X", "can I add X to my dev environment", "should I use X package",
  or "audit this extension/plugin/tool". This skill produces a structured PASS/CONDITIONAL/FAIL
  audit report that must be reviewed before installation is approved.
---

# Install Auditor

A security and reliability gate for anything installed into a development environment. The goal is to catch supply-chain attacks, malicious packages, and abandoned tools *before* they land on a machine — while not wasting time on packages that are obviously fine.

## Scope

Audits any installable artifact: browser extensions, IDE/editor plugins, package manager installs (npm, pip, cargo, gem, go, nuget, apt, brew, etc.), desktop/CLI applications, container images, CI/CD plugins, infrastructure tools (Terraform, Ansible, Helm), and AI/LLM tools.

---

## Step 1 — Identify the Installable

Gather before auditing:

1. **Full name and version** (exact package name, extension ID, or binary name)
2. **Source / registry** (npm, PyPI, Chrome Web Store, GitHub, vendor site, etc.)
3. **Installation command or URL** (what the user is about to run or click)
4. **Stated purpose** (what the user says they need it for)
5. **Target environment** (dev machine, CI server, Docker container, browser profile)
6. **Checksum / signature** (if available — SHA hash, GPG signature, code signing cert)

If any of 1–5 are missing, ask before proceeding. Item 6 is optional but its presence increases trust.

---

## Step 2 — Triage: Pick the Audit Tier

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

## Step 3 — Research

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

As you run each check, record its outcome for the **Audit Coverage** table (see Step 6):

- Use the canonical row labels from `references/criteria.md` **Audit Coverage Checklist** for this tier and installable type.
- For each row: **Status** (`Done`, `Done, N results`, `Skipped (…)`, `Not available (…)`, `N/A (…)`) plus **Source or notes** (script name, API, search query, or why skipped).
- **Tier-skipped** checks (e.g., deep web search in Tier 1) are **not** the same as **Not available** — the latter means you tried and could not get data.

### For Tier 1 (Quick Audit)
Only confirm: no CVEs, not a typosquat, license is compatible. Skip the deep web research.

### For Tier 3 (Deep Audit)
Additionally: review install scripts (`preinstall`, `postinstall`), check for obfuscated code, audit the dependency tree for known-bad transitive dependencies, and look for behavioral red flags in source code (credential harvesting, unexpected network calls, encoded strings).

---

## Step 4 — Evaluate

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

## Step 5 — Verdict

Apply this decision tree:

```
Any CRITICAL red flag? (see Red Flags below) ───────► REJECTED ❌
  │ No
Any unpatched CVE (HIGH or CRITICAL severity)? ────► REJECTED ❌
  │ No
Confirmed supply chain compromise? ─────────────────► REJECTED ❌
  │ No
Any HIGH-severity flags OR medium CVEs? ────────────► CONDITIONAL ⚠️
  │ No
3+ MEDIUM flags (cumulative risk)? ─────────────────► CONDITIONAL ⚠️
  │ No
Abandoned with no alternative? ─────────────────────► CONDITIONAL ⚠️
  │ No
All criteria pass? ─────────────────────────────────► APPROVED ✅
```

**CONDITIONAL** means: installation may proceed only after listed conditions are met (pin to safe version, disable certain permissions, sandbox only, etc.).

### Coverage gaps and recommendation

If **two or more** checks are **Not available** (failed API, 404, timeout — **not** tier-skipped and **not** `N/A`), add a sentence in **Recommendation** that the audit has **reduced coverage** because key data sources could not be reached. Do **not** change the verdict label (APPROVED / CONDITIONAL / REJECTED) for coverage alone — the verdict still follows the tree above. **Tier-skipped** checks do not count toward this threshold.

---

## Step 6 — Write the Report

**Write the report to a file** (e.g., `audit-<package-name>.md`). Adapt the depth to the audit tier — a Tier 1 quick audit doesn't need every section filled out.

```
# Install Audit: <name> v<version>

**Verdict: [APPROVED ✅ | CONDITIONAL ⚠️ | REJECTED ❌]**
**Audit tier:** [Quick | Standard | Deep]
**Date:** <today's date>

## Summary
<2–4 sentences: what this is, who makes it, key finding.>

## Security
| Area | Finding |
|------|---------|
| CVEs / Advisories | None found · or · list with IDs and severity |
| Supply Chain Risk | Low / Medium / High — reason |
| Permissions | Acceptable · or · Concerns: list |
| Telemetry/Privacy | None · Opt-out · Always-on |
| Dependency Risk | Low / Medium / High — reason |

## Reliability
| Area | Finding |
|------|---------|
| Maintenance | Active / Stale / Abandoned / Archived |
| Last Release | date |
| Publisher Trust | Verified / Unverified / Anonymous |
| Adoption | downloads/week, stars, etc. |
| License | SPDX — Compatible / Review needed / Incompatible |

## Audit Coverage

**Audit confidence (coverage):** [ High | Moderate | Low ] — [short reason: e.g., "7/9 checks Done, 2 Skipped (Tier 1)"]

Audit confidence measures **how completely the tier-appropriate checklist was executed** — **not** whether the installable is free of vulnerabilities. Unknown issues remain possible even when coverage is High.

| Check | Status | Source or notes |
|-------|--------|-----------------|
| Registry / metadata lookup | Done | e.g., registry-lookup.ps1 / npm API |
| Typosquat / name verification | Done | compared to `<legitimate name>` |
| CVE / advisories | Done, 0 results | OSV, GHSA |
| OpenSSF Scorecard | Not available | no repo for Scorecard API |
| Deep web / incident search | Skipped (Tier 1) | — |
| *(add rows from `references/criteria.md` for this tier; Tier 1: keep to ~3–6 rows — minimal set only)* | | |

**Rules of thumb for confidence**

- **High:** All tier-required checks are Done, legitimately **N/A**, or **Skipped (Tier N)** by design; at most one **Not available** on a non-critical row (e.g., Scorecard missing while CVE scan completed).
- **Moderate:** One–two **Not available** rows that are not solely tier-skips, or a critical-adjacent gap (e.g., partial advisory data).
- **Low:** Three or more **Not available**, or any tier-required check missing without a valid **Skipped** / **N/A** reason — especially **CVE / advisories** unavailable for Tier 2 or Tier 3.

## Risk Flags
<List each, or "None identified">
- [CRITICAL/HIGH/MEDIUM/LOW] description

## Alternatives
<1–3 alternatives if concerning, or "No better alternative identified">

## Conditions (CONDITIONAL verdict only)
<Specific conditions that must be met before installation>

## Recommendation
<1–3 sentences. Clear guidance on what to do.>

## Post-Install Checklist (APPROVED/CONDITIONAL only)
- [ ] Pin to exact audited version (<package>@<version>)
- [ ] Verify checksum/signature if provided
- [ ] Check lock file for unexpected entries after install
- [ ] Review post-install script output if applicable
- [ ] Re-audit on major version bump or maintainer change

**Sources:** <URLs consulted>
```

### Escalation

If the verdict is **REJECTED** or **CONDITIONAL with HIGH flags**: append an escalation notice. Adapt it to the user's context — if they're on a team, recommend security/engineering review. If they're a solo developer, recommend they avoid the package or carefully sandbox it.

---

## Red Flags — Automatic REJECTED

These are the things that should immediately stop an installation:

- **Typosquatting** — package name differs from legitimate package by 1–2 characters
- **Brand new + no history** — published less than 72 hours ago with no prior versions
- **Removed from registry** — previously removed from Chrome Web Store, npm, PyPI, etc.
- **Confirmed supply chain attack** — any security blog or GitHub advisory confirms compromise
- **Excessive permissions** — browser extension reads all history/cookies/clipboard with no justification
- **Dangerous container defaults** — Docker image runs as root with no USER switch, no justification
- **Unpinned CI action with secrets access** — GitHub Action not pinned to commit SHA while accessing secrets
- **Known malware** — confirmed cryptominer, credential stealer, or data exfiltration

---

## Behavioral Principles

1. **Err on the side of caution.** Unknown ≠ safe. If you can't find information, that's a yellow flag, not a green light.
2. **Always use current data.** Training data goes stale — packages change, maintainers change, vulnerabilities appear. Run the lookup script and do web searches.
3. **Be specific.** Cite actual CVE IDs, actual permission names, actual download numbers. Vague statements like "seems safe" aren't useful.
4. **Don't be swayed by urgency.** "I need this now" doesn't change the security posture.
5. **One report per installable.** If multiple packages are requested, produce separate reports.
6. **Adapt depth to risk.** Use the tiering system — don't over-audit trusted packages, don't under-audit risky ones.
7. **Document what you checked.** The **Audit Coverage** section is part of the evidence chain for every full report — include it unless the run is explicitly aborted before a report file is written.

---

## Reference Files

- `references/criteria.md` — Full scoring rubrics for each criterion
- `references/licenses.md` — License compatibility matrix
- `references/registries.md` — Trusted vs. untrusted registry guide per ecosystem
- `scripts/registry-lookup.ps1` — Automated registry data lookup (downloads, maintainers, vulnerabilities). Run with: `powershell -File scripts/registry-lookup.ps1 <ecosystem> <name> [version]`. If PowerShell is unavailable, query the registry APIs directly via web search or sandbox HTTP calls (npm: `registry.npmjs.org/<pkg>`, PyPI: `pypi.org/pypi/<pkg>/json`, etc.).
