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

A security and reliability gate for anything installed into a dev environment. Catch supply-chain attacks, malicious packages, and abandoned tools *before* they land — without wasting time on packages that are obviously fine.

## Scope

Any installable: browser extensions, IDE/editor plugins, registry packages (npm, pip, cargo, gem, go, nuget, maven, composer, IaC modules), desktop/CLI apps, container images, CI/CD actions, agent extensions (MCP / Claude Code plugins / skills), remote integrations.

---

## Step 0 — Classify the Subject (Innermost Trust Boundary)

**Rule:** classify by the **innermost trust boundary the user is crossing** — the last verification gate between the user and the code that will actually execute. Full rule, worked hybrid examples, and edge-case discipline live in `.projex/2604070300-install-auditor-subject-type-taxonomy-def.md` under "Classifier Rule — Innermost Trust Boundary". Read that section when the rule does not resolve cleanly on its own.

**Procedure:** (1) read URL + install command + manifest + user intent (read-only); (2) match against the signal table below; (3) one strong match → **high** confidence; (4) multiple matches → apply the innermost-boundary rule to pick the last gate the user personally crosses; (5) no strong match OR conflict unresolved after the rule → **`generic` (type 0) at low confidence**, naming the conflict; (6) emit the structured output and route. **Low confidence routes to `generic`, never to a best-guess specific type.**

**Signal table:**

| # | Type | Strong signals |
|---|---|---|
| 1 | registry-package | `npm/pip/cargo/gem/go/nuget install`, manifest files, `npmjs.com/package/*`, `pypi.org/project/*`, `crates.io/*`, Terraform/Ansible/Helm registries |
| 2 | browser-extension | manifest `permissions`+`host_permissions`, `chromewebstore.google.com/*`, `addons.mozilla.org/*`, `.crx`/`.xpi` |
| 3 | ide-plugin | `code --install-extension`, VSIX, `marketplace.visualstudio.com/*`, `open-vsx.org/*`, `plugins.jetbrains.com/*` |
| 4 | container-image | `docker pull/run`, `FROM` in Dockerfile, `sha256:` digest, `hub.docker.com/*`, `ghcr.io/*`, `quay.io/*`, ECR/GCR |
| 5 | ci-action | `uses:` in workflows, GitLab `include:`, CircleCI `orbs:`, `github.com/<owner>/<action>@<ref>` |
| 6 | desktop-app | `.msi/.dmg/.deb/.rpm/.pkg`, `brew install --cask`, `winget`, `choco`, MS/Mac App Store URLs |
| 7 | cli-binary | `curl … \| sh`, GitHub Releases binary, nvm/pyenv/rustup, vendor-hosted executable URLs |
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

| # | Type | Workflow | Phase 1 Status |
|---|---|---|---|
| 1 | registry-package | `workflows/registry-package.md` | Live — Phase 2 (M2.1) |
| 2 | browser-extension | `workflows/browser-extension.md` | Live — Phase 3 (M3.1) |
| 3 | ide-plugin | `workflows/ide-plugin.md` | Live — Phase 3 (M3.4) |
| 4 | container-image | `workflows/container-image.md` | Live — Phase 3 (M3.2) |
| 5 | ci-action | `workflows/ci-action.md` | Live — Phase 3 (M3.3) |
| 6 | desktop-app | `workflows/desktop-app.md` | Live — Phase 4 (M4.1) |
| 7 | cli-binary | `workflows/cli-binary.md` | Live — Phase 4 (M4.2) |
| 8 | agent-extension | `workflows/agent-extension.md` | Live — Phase 4 (M4.3); 8a/8b/8c resolved at classification |
| 9 | remote-integration | `workflows/remote-integration.md` | Live — Phase 4 (M4.4) |
| 0 | generic | `workflows/generic.md` | Universal fallback; also the home for truly unclassifiable subjects |

> **Phase 2 note:** `workflows/registry-package.md` is live (M2.1). Remaining 9 types still route to `workflows/generic.md`; specific workflows land in Phases 2--4 and this table updates per milestone. Do **not** create a workflow file before its owning phase.

---

## Step 1 — Load and Follow the Routed Workflow

Read `workflows/<type>.md` per the dispatch table. Follow its **Identify / Evidence / Subject Rubric / Subject Verdict Notes** sections to produce per-subject findings. Workflows defer to `references/criteria.md` (shared tier-aware rubric), `references/licenses.md` (SPDX compatibility), `references/registries.md` (per-ecosystem trust), and may invoke `scripts/registry-lookup.ps1`. Then return here for Step N.

---

## Step N — Shared Verdict Tree + Audit-Coverage Report

### Verdict Tree

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

**CONDITIONAL** means installation may proceed only after listed conditions are met (pin to safe version, disable permissions, sandbox only, etc.).

**Coverage gaps:** if **two or more** checks are **Not available** (failed API / 404 / timeout — **not** tier-skipped, **not** `N/A`), add a sentence to Recommendation that the audit has **reduced coverage**. Do **not** change the verdict label for coverage alone — the verdict still follows the tree above. Tier-skipped checks do not count toward this threshold.

### Report Skeleton

Write the report to `audit-<package-name>.md`. Adapt depth to audit tier — a Tier 1 quick audit doesn't need every section filled out.

```
# Install Audit: <name> v<version>

**Verdict: [APPROVED ✅ | CONDITIONAL ⚠️ | REJECTED ❌]**
**Audit tier:** [Quick | Standard | Deep]
**Subject type:** <from Step 0 classifier output>
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

- **High:** All tier-required checks are Done, legitimately **N/A**, or **Skipped (Tier N)** by design; at most one **Not available** on a non-critical row.
- **Moderate:** One–two **Not available** rows that are not solely tier-skips, or a critical-adjacent gap.
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

If verdict is **REJECTED** or **CONDITIONAL with HIGH flags**: append an escalation notice. On a team → recommend security/engineering review. Solo → recommend avoiding or strictly sandboxing.

### Red Flags — Automatic REJECTED

- **Typosquatting** — name differs from legitimate package by 1–2 characters
- **Brand new + no history** — published < 72 hours ago with no prior versions
- **Removed from registry** — previously removed from Chrome Web Store, npm, PyPI, etc.
- **Confirmed supply chain attack** — security blog or advisory confirms compromise
- **Excessive permissions** — browser extension reads all history/cookies/clipboard with no justification
- **Dangerous container defaults** — image runs as root with no USER switch, unjustified
- **Unpinned CI action with secrets access** — not pinned to commit SHA while accessing secrets
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

- `workflows/generic.md` — Phase 1 universal fallback workflow (evidence acquisition + scoring)
- `workflows/registry-package.md` — Type 1 registry-package workflow (Phase 2, M2.1)
- `workflows/browser-extension.md` — Type 2 browser-extension workflow (Phase 3, M3.1)
- `workflows/container-image.md` — Type 4 container-image workflow (Phase 3, M3.2)
- `workflows/ci-action.md` — Type 5 ci-action workflow (Phase 3, M3.3)
- `workflows/ide-plugin.md` — Type 3 ide-plugin workflow (Phase 3, M3.4)
- `workflows/desktop-app.md` — Type 6 desktop-app workflow (Phase 4, M4.1)
- `workflows/cli-binary.md` — Type 7 cli-binary workflow (Phase 4, M4.2)
- `workflows/agent-extension.md` — Type 8 agent-extension workflow (Phase 4, M4.3)
- `workflows/remote-integration.md` — Type 9 remote-integration workflow (Phase 4, M4.4)
- `references/criteria.md` — Shared tier-aware scoring rubric
- `references/criteria/registry-package.md` — Registry-package criteria addendum (ecosystem trust signals, tier thresholds, install script patterns)
- `references/criteria/browser-extension.md` — Browser-extension criteria addendum (store trust, permission classification, content-script reach, auto-update risk)
- `references/criteria/container-image.md` — Container-image criteria addendum (registry trust, signing standards, SBOM, layer risk, runtime privilege, tag/digest pinning)
- `references/criteria/ci-action.md` — CI-action criteria addendum (publisher trust, pinning, trigger/secret exposure, transitive audit)
- `references/criteria/ide-plugin.md` — IDE-plugin criteria addendum (marketplace trust, capability risk, bundled-binary provenance, tier thresholds)
- `references/criteria/desktop-app.md` — Desktop-app criteria addendum (distribution channel trust, code signing, installer risk, sandboxing, tier thresholds)
- `references/criteria/cli-binary.md` — CLI-binary criteria addendum (distribution channel trust, signature/checksum standards, install-script risk, provenance, tier thresholds)
- `references/criteria/agent-extension.md` — Agent-extension criteria addendum (distribution/discovery channel trust, capability scope classification, transport & isolation, prompt/behavioral risk, tier thresholds)
- `references/criteria/remote-integration.md` — Remote-integration criteria addendum (OAuth scope & permission assessment, data residency & compliance, terms of service & data sharing, breach history & security posture, tier thresholds)
- `references/licenses.md` — License compatibility matrix
- `references/registries.md` — Trusted vs. untrusted registries per ecosystem
- `scripts/registry-lookup.ps1` — Automated registry data lookup. Run: `powershell -File scripts/registry-lookup.ps1 <ecosystem> <name> [version]`. If PowerShell is unavailable, query registry APIs directly (npm: `registry.npmjs.org/<pkg>`, PyPI: `pypi.org/pypi/<pkg>/json`, etc.).
- `.projex/2604070300-install-auditor-subject-type-taxonomy-def.md` — Locked 10-type taxonomy + full Classifier Rule
