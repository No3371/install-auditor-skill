---
name: install-auditor
description: >
  Security and reliability audit to run before any new third-party installable enters a dev
  environment. Use it whenever a user or agent is about to add an npm/pip/cargo/gem/go/nuget/maven
  dependency, browser extension, IDE plugin, desktop app, CLI tool or curl-pipe-to-shell installer,
  Docker image, CI action, MCP server, Claude Code plugin or skill, or OAuth/API-key integration;
  for a major-version upgrade or maintainer change of an existing dependency; and when asked
  "is X safe to install", "should we use X", or "audit this extension/plugin/tool". Skip it when only
  reinstalling what a lockfile or manifest already pins (npm ci, pip install -r with nothing new),
  for first-party or workspace packages, and for debugging package-manager errors. Produces an
  APPROVED/CONDITIONAL/REJECTED audit report to review before installing.
---

# Install Auditor

A security and reliability gate for anything installed into a dev environment. Catch supply-chain attacks, malicious packages, and abandoned tools *before* they land — without wasting time on packages that are obviously fine.

## Scope

Any installable: browser extensions, IDE/editor plugins, registry packages (npm, pip, cargo, gem, go, nuget, maven, composer, IaC modules), desktop/CLI apps, container images, CI/CD actions, agent extensions (MCP / Claude Code plugins / skills), remote integrations.

---

## Step 0 — Classify the Subject (Innermost Trust Boundary)

**Rule:** classify by the **innermost trust boundary the user is crossing** — the last verification gate between the user and the code that will actually execute. Full rule, routing overrides, extended signals, worked hybrid examples, and edge-case discipline live in `references/classifier.md`. Read it when the rule does not resolve cleanly on its own.

**Procedure:** (1) read URL + install command + manifest + user intent (read-only); (2) match against the signal table below; (3) apply confidence:

| Condition | Confidence | Routes to |
|-----------|------------|-----------|
| One strong signal match | **high** | `workflows/<matched-type>.md` |
| Multiple strong matches → innermost-boundary rule resolves to one type | **high** | `workflows/<resolved-type>.md` |
| Weak/partial signals point to a single best-candidate type | **medium** | `workflows/<best-candidate>.md` — note the uncertainty in Rationale |
| Multiple weak matches, no single best candidate after the boundary rule | **low** | `workflows/generic.md` — name the conflict in Rationale |
| No signals fire at all | **low** | `workflows/generic.md` |

(4) emit the structured output and route. **Only `low` confidence routes to `generic.md`. Medium-confidence subjects route to their best-match specific workflow — the workflow itself handles residual uncertainty via its tier system.**

**Signal table:**

| # | Type | Strong signals |
|---|---|---|
| 1 | registry-package | `npm/pip/cargo/gem/go/nuget install`, manifest files, `npmjs.com/package/*`, `pypi.org/project/*`, `crates.io/*`, Terraform/Ansible/Helm registries |
| 2 | browser-extension | manifest `permissions`+`host_permissions`, `chromewebstore.google.com/*`, `addons.mozilla.org/*`, `.crx`/`.xpi` |
| 3 | ide-plugin | `code --install-extension`, VSIX, `marketplace.visualstudio.com/*`, `open-vsx.org/*`, `plugins.jetbrains.com/*` |
| 4 | container-image | `docker pull/run`, `FROM` in Dockerfile, `sha256:` digest, `hub.docker.com/*`, `ghcr.io/*`, `quay.io/*`, ECR/GCR |
| 5 | ci-action | `uses:` in workflows, GitLab `include:`, CircleCI `orbs:`, `github.com/<owner>/<action>@<ref>` |
| 6 | desktop-app | `.msi/.dmg/.deb/.rpm/.pkg`, `brew install --cask`, `winget`, `choco`, MS/Mac App Store URLs |
| 7 | cli-binary | `curl … \| sh`, GitHub Releases binary, `brew install <formula>` (Homebrew core; `--cask` → desktop-app), nvm/pyenv/rustup, vendor-hosted executable URLs |
| 8 | agent-extension | MCP manifest (**8a**), Claude Code plugin bundle (**8b**), Claude Code skill with `SKILL.md` (**8c**) |
| 9 | remote-integration | OAuth flow, API key exchange, "Connect to <service>", no local code install |
| 0 | generic | no strong signals fire, or conflict unresolved after the innermost-boundary rule |

**Required output shape** (emit verbatim before routing):

```
Subject type:   <id> (<name>)
Confidence:     high | medium | low
Trust boundary: <one-line: what the user is actually crossing>
Rationale:      <1–3 sentences: which signals triggered the choice>
Routes to:      workflows/<type>.md
Sub-rubric:     <Type 8 only: 8a | 8b | 8c>
```

**User override:** if the user says "treat this as `<type>`", honor at high confidence with `user override: <verbatim>` in Rationale. Classification is read-only and never re-runs mid-audit.

### Dispatch Table

| # | Type | Workflow | Status |
|---|---|---|---|
| 1 | registry-package | `workflows/registry-package.md` | Live |
| 2 | browser-extension | `workflows/browser-extension.md` | Live |
| 3 | ide-plugin | `workflows/ide-plugin.md` | Live |
| 4 | container-image | `workflows/container-image.md` | Live |
| 5 | ci-action | `workflows/ci-action.md` | Live |
| 6 | desktop-app | `workflows/desktop-app.md` | Live |
| 7 | cli-binary | `workflows/cli-binary.md` | Live |
| 8 | agent-extension | `workflows/agent-extension.md` | Live; 8a/8b/8c resolved at classification |
| 9 | remote-integration | `workflows/remote-integration.md` | Live |
| 0 | generic | `workflows/generic.md` | Low-confidence fallback only |

---

## Step 1 — Load and Follow the Routed Workflow

Read `workflows/<type>.md` per the dispatch table. Follow its **Identify / Evidence / Subject Rubric / Subject Verdict Notes** sections to produce per-subject findings. Workflows defer to `references/criteria.md` (shared tier-aware rubric), `references/licenses.md` (SPDX compatibility), `references/registries.md` (per-ecosystem trust), and may invoke the lookup scripts in `scripts/` (see Reference Files). Then return here for Step N.

---

## Step N — Shared Verdict Tree + Audit-Coverage Report

### Verdict Tree

```
Any CRITICAL flag? (see Tree terms below) ──────────► REJECTED ❌
  │ No
Any unpatched HIGH/CRITICAL CVE? (see Tree terms) ──► REJECTED ❌
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

**Tree terms & precedence:**

- **CRITICAL flag** — any Red Flag below, **or** a finding the auditor rates CRITICAL using the routed workflow's addendum and its `Toward REJECTED` notes. Record each rating and its reason in the report's Risk Flags so the verdict is traceable.
- **Unpatched CVE** — affects the version to be installed **and** no fixed release exists (`references/criteria.md` §4.3 CVE Severity Mapping). A CVE fixed in a newer release does not trigger this node; rate it per the routed workflow (typically HIGH → CONDITIONAL with an upgrade condition).
- **Precedence** — Red Flags are subject-independent and are never downgraded. For subject-specific patterns (Dockerfile instructions, ref pinning, permission scopes, documented exceptions) the routed workflow and its criteria addendum win over generic wording here or in `references/criteria.md`.

**CONDITIONAL** means installation may proceed only after listed conditions are met (pin to safe version, disable permissions, sandbox only, etc.).

**Coverage gaps:** if **two or more** checks are **Not available** (failed API / 404 / timeout — **not** tier-skipped, **not** `N/A`), add a sentence to Recommendation that the audit has **reduced coverage**. Do **not** change the verdict label for coverage alone — the verdict still follows the tree above. Tier-skipped checks do not count toward this threshold.

### Report

**Location:** if the user or calling prompt names an output file or directory, write there. Otherwise write to `.install-audits/` at the project root (`git rev-parse --show-toplevel` from the current directory; outside a repo, the current directory), creating the folder if needed. File name: `audit-<name>-<version>.md`, lowercased, with `@`, `/`, `:` and spaces turned into `-` and no leading `-` (`@types/node` 20.11.0 → `audit-types-node-20.11.0.md`); drop `-<version>` when the subject has none. Do not edit `.gitignore` or commit the report. Finish by telling the user the verdict, the report path, and any conditions.

**Shape:** by final tier, after any mid-audit escalation. Tier 1 (Quick) uses the Quick skeleton below; keep it under 80 lines. Tier 2 and Tier 3 read `references/report-template.md` and fill its full skeleton. Every report keeps the verdict line, the `## Audit Coverage` heading, and the `**Audit confidence (coverage):**` line exactly as written; graders and tooling parse them.

**Audit confidence** measures how completely the tier-appropriate checklist was executed, not whether the installable is free of vulnerabilities. Rate it:

- **High:** All tier-required checks are Done, legitimately **N/A**, or **Skipped (Tier N)** by design; at most one **Not available** on a non-critical row.
- **Moderate:** One–two **Not available** rows that are not solely tier-skips, or a critical-adjacent gap.
- **Low:** Three or more **Not available**, or any tier-required check missing without a valid **Skipped** / **N/A** reason — especially **CVE / advisories** unavailable for Tier 2 or Tier 3.

**Quick skeleton (Tier 1):**

```
# Install Audit: <name> v<version>

**Verdict: [APPROVED ✅ | CONDITIONAL ⚠️ | REJECTED ❌]**
**Audit tier:** Quick
**Subject type:** <from Step 0 classifier output>
**Date:** <today's date>

## Summary
<2–3 sentences: what this is, who makes it, key finding.>

## Audit Coverage

**Audit confidence (coverage):** [ High | Moderate | Low ] — [short reason: e.g., "4/4 Tier 1 checks Done"]

| Check | Status | Source or notes |
|-------|--------|-----------------|
| Registry / metadata lookup | Done | e.g., registry-lookup / npm API |
| Typosquat / name verification | Done | compared to `<legitimate name>` |
| CVE / advisories | Done, 0 results | OSV, GHSA |
| License compatibility | Done | SPDX — Compatible |
| *(Tier 1 minimal set from `references/criteria.md`, ~3–6 rows; deeper rows `Skipped (Tier 1)` or omitted)* | | |

## Risk Flags
<"None identified", or one line per flag: - [HIGH/MEDIUM/LOW] description>

## Recommendation
<1–2 sentences. CONDITIONAL: list the conditions. APPROVED/CONDITIONAL: pin to <package>@<version>; re-audit on major version bump or maintainer change.>

**Sources:** <URLs consulted>
```

### Escalation

If verdict is **REJECTED** or **CONDITIONAL with HIGH flags**: append an escalation notice. On a team → recommend security/engineering review. Solo → recommend avoiding or strictly sandboxing.

### Red Flags — Automatic REJECTED

Subject-independent. Each applies only when its full condition holds; partial matches are rated by the routed workflow, not auto-rejected.

- **Confirmed typosquat / impersonation** — name, scope, or namespace imitates a legitimate subject (edit distance ≤2 from a top-1000 package, combosquat, homoglyph, or namespace impersonation such as `someuser/nginx` vs official `nginx`) **and** the subject has no independent legitimate history. For npm, a `typosquat-check` script result of `riskLevel: critical` qualifies unless legitimacy is affirmatively proven. Similarity alone (script `high`/`medium`, or a name merely close to a popular one) is a HIGH/MEDIUM flag per `references/criteria/registry-package.md`.
- **Brand new + no history** — published < 72 hours ago with no prior versions
- **Removed for cause** — previously removed from Chrome Web Store, npm, PyPI, etc. for malicious behavior, compromise, or a security-policy violation (not author unpublish, rename, or naming dispute)
- **Confirmed supply chain attack** — security blog or advisory confirms compromise
- **Excessive permissions** — browser extension reads all history/cookies/clipboard with no justification
- **Mutable CI ref with privileged access** — action or reusable workflow referenced by branch, default branch, or unknown ref — or by any non-SHA ref from an unverified third-party publisher — in a job holding secrets, a write-scoped token, `id-token: write`, or publish rights. Tag-pinned actions from official/verified publishers are HIGH → CONDITIONAL (pin to SHA) per `workflows/ci-action.md`.
- **Known malware** — confirmed cryptominer, credential stealer, or data exfiltration

### Behavioral Principles

1. **Err on the side of caution.** Unknown ≠ safe.
2. **Always use current data.** Run the lookup script; do live searches.
3. **Be specific.** Cite CVE IDs, permission names, download numbers.
4. **Don't be swayed by urgency.** "I need this now" doesn't change security posture.
5. **One report per installable.** Multiple packages → separate reports.
6. **Adapt depth to risk.** Use the tiering system.
7. **Document what you checked.** The Audit Coverage section is part of the evidence chain for every full report.

### Reference Files

- `workflows/<type>.md` — per-type workflow, one per Dispatch Table row; `workflows/generic.md` is the low-confidence fallback (subject probe + user clarification + defensive minimum audit)
- `references/classifier.md` — Full classifier rule: tie-breaking, routing overrides, extended signals, worked hybrid examples, edge-case discipline
- `references/criteria.md` — Shared tier-aware scoring rubric and canonical Audit Coverage rows
- `references/criteria/<type>.md` — Per-type criteria addendum (types 1–9); each workflow names its own and when to read it
- `references/report-template.md` — Full report skeleton for Tier 2 / Tier 3 audits
- `references/licenses.md` — License compatibility matrix
- `references/registries.md` — Trusted vs. untrusted registries per ecosystem
- `scripts/registry-lookup.py` | `typosquat-check.py` | `vuln-lookup.py` | `dep-scan.py` — registry metadata, npm typosquat, OSV+GHSA CVE, and dependency-CVE lookups; JSON to stdout. Run: `python3 scripts/<script>.py -Ecosystem <eco> -Name <name> [-Version <ver>]` (Python ≥3.8, stdlib only; Windows: `py -3`). PowerShell hosts: same-named `.ps1` twin, identical arguments. Neither available → query APIs directly (npm: `registry.npmjs.org/<pkg>`, PyPI: `pypi.org/pypi/<pkg>/json`, CVEs: POST `api.osv.dev/v1/query` with `{"package":{"name":"<pkg>","ecosystem":"<eco>"}}`, etc.).
