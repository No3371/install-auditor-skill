# Audit Criteria — Detailed Scoring Rubrics

## Applying Rubrics by Audit Tier

- **Tier 1 (Quick):** Check 4.1 (provenance), 4.3 (CVEs only) and 4.6 (version integrity; it can bar Tier 1 whatever the addendum's Tier 1 thresholds say). Skip deep rubric scoring — if the package is high-trust, no CVEs exist and §4.6 raises nothing, a brief confirmation suffices.
- **Tier 2 (Standard):** Score all sections below. This is the default depth.
- **Tier 3 (Deep):** Score all sections below AND review source code for behavioral signals (install scripts, obfuscation, credential access patterns).

The `scripts/registry-lookup.py` script provides hard data for many of these checks (downloads, maintainer count, publish date, dependencies). Use it before manual research. On PowerShell hosts use the same-named `.ps1` twin (identical arguments); this applies to every script named below.

**Audit tooling is itself a dependency.** Third-party tools a workflow tells you to run (image scanners, SBOM generators, signature verifiers) can be hijacked like any installable. Use a release outside any known-compromised range whose identity verifies per §4.6 V2, and record tool + version in the coverage row's notes. If you cannot verify the tool, use registry- or vendor-side scan data instead and say so in the row. The bundled `scripts/` are stdlib-only and need no extra install.

---

## Audit Coverage Checklist (Canonical)

Reports must include an **Audit Coverage** table (see `SKILL.md` Step N → Report; Tier 2/3 skeleton in `references/report-template.md`). Row labels below should match the **Check** column unless you add an ecosystem-specific row — do **not** omit tier-required rows.

### Status vocabulary

Use one of these in the **Status** column:

| Status | When to use |
|--------|-------------|
| `Done` | Check completed; evidence exists |
| `Done, N results` | Completed with countable outcomes (e.g., web hits, CVE count) |
| `Skipped (<reason>)` | Deliberately not run — include tier or scope (e.g., `Skipped (Tier 1)`) |
| `Not available (<detail>)` | Attempted but blocked (API 404, no Scorecard repo, network failure) |
| `N/A (<reason>)` | Does not apply to this installable (e.g., no `postinstall` script) |

### Critical checks (confidence)

For **Tier 2 (Standard)** and **Tier 3 (Deep)**, a **CVE / advisory scan for the installable version** must **not** end as `Not available` without strong justification — if it does, **Audit confidence** cannot be **High** (see `SKILL.md`).

### Rows by tier

Each row is **Required** (must appear in the table), **Tier-skip** (Tier 1 uses `Skipped (Tier 1)` or omits the row per Tier 1 rules in `SKILL.md`), or **If applicable** (include when the installable type matches).

| Check | Tier 1 | Tier 2 | Tier 3 | Notes |
|-------|--------|--------|--------|-------|
| Registry / metadata lookup | Required | Required | Required | e.g., `registry-lookup` or registry API |
| Typosquat / name verification | Required | Required | Required | Character-by-character vs legitimate name |
| CVE / advisories (requested version) | Required | Required | Required | OSV, GHSA, registry advisory APIs — **critical** for T2/T3 |
| Version integrity (§4.6) | Required | Required | Required | Version age, identity, continuity, compromise scope; `N/A (hosted service)` when no versioned artifact |
| License compatibility | Required | Required | Required | See `references/licenses.md` |
| Maintainer / activity / health | Tier-skip (brief) | Required | Required | Downloads, last release, signals |
| Web search — incidents & supply chain | Tier-skip | Required | Required | Malware, hijack, removal notices |
| OpenSSF Scorecard | Optional | Required (Done or Not available) | Required | Query `api.securityscorecards.dev` when repo known |
| Permissions / least privilege | If applicable | If applicable | If applicable | Extensions, Docker, GH Actions, etc. |
| Dependency tree / transitive risk | Tier-skip | Required | Required | Known-bad transitive deps |
| Install script review (`pre`/`postinstall`, etc.) | Tier-skip | Required | Required | N/A if no scripts |
| Source code review (behavioral) | Tier-skip | Tier-skip | Required | Obfuscation, network calls, credential access |

**Tier 1 (Quick):** Include **only** the minimal row set — typically registry/metadata, typosquat, CVE/advisories, license, version integrity, plus **Skipped (Tier 1)** for deeper rows *or* omit deep rows entirely if the table stays readable (see `SKILL.md`). Do not pad with ten `Skipped` lines.

**Browser extensions:** Always include **Permissions / least privilege** when the installable is an extension.

**Containers / images:** Include image configuration checks (user, capabilities) under permissions or as extra rows.

**Workflow coverage tables** add subject rows to this table; they never drop a Required row. A Required row that cannot apply stays as `N/A (<reason>)` (e.g. `CVE / advisories — N/A (hosted service, no versioned artifact)`); the Tier 2/3 CVE rule under Critical checks applies only when a versioned artifact exists. A workflow may define its own `Skipped (<reason>)` values and cap Audit confidence for them (`SKILL.md` Step N).

---

## 4.1 Provenance & Identity

### Typosquatting Check (CRITICAL)

For **npm registry packages**, run `scripts/typosquat-check.py` first to get
algorithmic edit-distance, download-ratio, and combosquat analysis. See
`references/criteria/registry-package.md` "Typosquat Detection" for full
interpretation guidance and risk-level thresholds.

Then supplement with manual comparison — character by character against the
known-legitimate package name. Common substitutions to watch:
- `l` → `1`, `I` (lowercase L, number 1, uppercase i)
- `o` → `0`
- `-` insertion/removal (e.g., `cross-env` vs `crossenv`)
- Prefix/suffix additions (`python-requests` vs `requests`)
- Homoglyphs in unicode package names

**Auto-REJECT if:** Name differs by ≤2 characters from a top-1000 package with no prior history.

### Publisher Verification
| Signal | Trust Level |
|---|---|
| Official org account (e.g., `@babel`, `@angular`) | High |
| Verified publisher badge on registry | High |
| GitHub org with multiple contributors + history | Medium-High |
| Individual with long contribution history | Medium |
| Single-commit anonymous account | Low |
| No source code available | Very Low |

Badges, verified-publisher status and signatures establish **identity**, not code integrity: credit them only per §4.6 V2, never against a §4.6 flag.

### Registry Source
| Registry | Trust Baseline |
|---|---|
| npm (npmjs.com) | Medium (open, verified publishers higher) |
| PyPI | Medium |
| RubyGems | Medium |
| crates.io | Medium-High (requires GitHub auth) |
| Chrome Web Store | Medium (Google-reviewed) |
| VS Code Marketplace | Medium (Microsoft-reviewed) |
| Docker Hub official images | High |
| Docker Hub community images | Low-Medium |
| GitHub Packages | Varies |
| Random CDN / direct download | Low |
| Self-hosted with no verification | Very Low |

---

## 4.2 Maintenance & Longevity

### Activity Scoring
| Signal | Score |
|---|---|
| Release in last 30 days | +2 |
| Release in last 6 months | +1 |
| Release in last 12 months | 0 |
| Last release 1–2 years ago | -1 |
| Last release 2+ years ago | -2 |
| Explicitly archived with reason | 0 (stable is OK) |
| Explicitly deprecated, successor named | -1 (use successor) |
| Abandoned, no successor | -3 |

**Score < -1 → Flag as Stale. Score < -2 → Flag as Abandoned → CONDITIONAL** (`SKILL.md` tree: abandoned with no alternative). Abandonment reaches REJECTED only together with another REJECTED trigger (a `SKILL.md` Blocking CVE, §4.6 V4 case a).

### Issue Tracker Health
- Open issues with maintainer responses in last 90 days → Healthy
- Open issues, no maintainer responses in 90+ days → Concerning
- Issues locked or disabled → Flag

---

## 4.3 Security Track Record

### CVE Severity Mapping
`SKILL.md` "Blocking CVE" = the REJECTED cells below. Rate only CVEs that affect the version to be installed.

| CVSS Score | Severity | Verdict Impact |
|---|---|---|
| 9.0–10.0 | Critical | Listed in CISA KEV → REJECTED. Otherwise: in own code with no fixed release → REJECTED; else HIGH flag → CONDITIONAL |
| 7.0–8.9 | High | In own code with no fixed release → REJECTED; else (fixed release exists, or third-party component) HIGH flag → CONDITIONAL |
| 4.0–6.9 | Medium | CONDITIONAL; note if patched |
| 0.1–3.9 | Low | Flag; APPROVED if patched or mitigated |

**Always check:** Is the CVE in the version being requested, or only in older versions? If user is installing an old pinned version that has known CVEs, escalate.

- **Own code** = what the subject's publisher writes and ships (the package, binary, extension, action or app itself, incl. components it forks and maintains). **Third-party component** = OS packages, base-image layers, bundled or transitive dependencies.
- **Fixed release** = a published version that removes the CVE. When one exists, the condition is: install it (and audit that version). A KEV-listed CRITICAL rejects the requested version even when a fix exists; the Recommendation names the fixed release. Third-party component with no fix → condition: the routed workflow's mitigations, plus re-audit when a fix ships.
- **KEV:** check each CRITICAL against the CISA Known Exploited Vulnerabilities catalog; record the result in the CVE row. If the catalog is unreachable, search for in-the-wild exploitation; credible reports count as listed.
- **VEX:** a `not_affected` statement (OpenVEX, CSAF or CycloneDX VEX) counts as evidence that the CVE does not apply if it names this version, gives a justification, and comes from the subject's publisher or the component's maintainer. Record source + justification in the CVE row and leave the CVE out of the rating. For a signed statement, check the signer per §4.6 V2. `affected` / `under_investigation` change nothing.
- **Addendum:** draws the own-code / third-party line for its artifact type and names its scan and VEX sources. It does not change the verdict classes above.

### Supply Chain Indicators
Search for these terms combined with the package name:
- "malicious package", "trojan", "backdoor", "data exfiltration"
- "hijacked", "compromised maintainer", "typosquatting confirmed"
- "removed from npm/PyPI" + reason

Rate a confirmed hit by version scope per §4.6 V4: REJECTED only when the version to be installed is affected or the compromise is unresolved.

Sources to check: Sonatype blog, Snyk security advisories, Socket.dev, npm security advisories, GitHub Security Advisories (GHSA), OpenSSF Scorecard.

### Vulnerability Database Lookup (registry packages)

For registry packages (npm, PyPI, crates, RubyGems, NuGet, Go, Maven, Hex), run
`scripts/vuln-lookup.py` for structured OSV + GHSA queries before web search. See
`references/criteria/registry-package.md` "Multi-Database CVE Correlation" for
risk-level thresholds and coverage row format.

### Transitive Dependency Scan (registry packages)

Run `scripts/dep-scan.py` to check direct (Tier 2) or full transitive (Tier 3, npm only)
dependencies for known CVEs via the OSV batch API — no package installation required.
Invoke after `vuln-lookup` in the Evidence step for supported ecosystems. Tier 1
packages skip this step. Full risk-level-to-verdict guidance and output field reference
in `references/criteria/registry-package.md` §Transitive Dependency Scanning.

---

## 4.4 Permissions & Access

### Browser Extension Permissions — Risk Matrix
| Permission | Risk Level | Notes |
|---|---|---|
| `<all_urls>` / `*://*/*` | CRITICAL | Read/modify every page the user visits |
| `webRequestBlocking` (with `webRequest`) | CRITICAL | Full MITM: intercept, modify or block all HTTP traffic (MV2; Chrome MV3 only for policy-installed extensions) |
| `webRequest` (observe only) | HIGH | Sees every request URL and header on permitted hosts (MV2 and MV3); cannot modify |
| `cookies` | HIGH | Read/write cookies for permitted domains — session theft |
| `history` | MEDIUM-HIGH | Full browsing history access |
| `clipboardRead` | MEDIUM-HIGH | Can read anything copied |
| `nativeMessaging` | HIGH | Talks to native executables — leaves the browser sandbox |
| `downloads` | HIGH | Can silently download files to disk |
| `storage` / `unlimitedStorage` | LOW | Extension-local storage only; risk comes from permissions that read pages or send data |
| `tabs` | MEDIUM | URLs and titles of every open tab |
| `activeTab` (alone, no broad hosts) | LOW | Only current tab when user clicks |

Ratings mirror `references/criteria/browser-extension.md` § Permission Risk Classification, which holds the full list and scoring rules; change both together.

**Red flag:** Permissions far exceed stated functionality. A color picker extension requesting `<all_urls>` + `cookies` is suspicious.

### npm/pip Package Permissions (Behavioral)
Look for these in source code or security reports:
- `child_process.exec` with dynamic input → code execution risk
- `fs.readdir` scanning home directory → credential harvesting risk
- HTTP requests to non-obvious external domains in postinstall scripts
- `process.env` access (may harvest secrets from CI environment)
- Encoded/obfuscated strings in source → obfuscation red flag

### Docker Image Permissions
- `USER root` with no later `USER` switch → flag
- `--privileged` in run instructions → flag
- Mounting `/var/run/docker.sock` → CRITICAL (container escape)
- Capabilities: `SYS_ADMIN`, `NET_ADMIN` → flag unless justified

---

## 4.5 Reliability & Compatibility

### Adoption Signal Interpretation
| Signal | Interpretation |
|---|---|
| 1M+ weekly downloads (npm/PyPI) | High adoption, broad battle-testing |
| 100K–1M weekly downloads | Solid adoption |
| 10K–100K | Moderate; check if niche or growing |
| 1K–10K | Low; verify use case is niche, not failed |
| < 1K | Very low; extra scrutiny on alternatives |
| 10K+ GitHub stars | Strong community signal |
| Used by major orgs (listed in README) | Good signal |

Note: Download counts can be inflated by bots/mirrors. Cross-check with GitHub stars and issue activity.

### Cumulative Risk
Individual MEDIUM flags may be acceptable, but 3 or more MEDIUM flags together indicate systemic risk and should escalate to **CONDITIONAL**. Count all MEDIUM flags across all criteria sections.

### Compatibility Checks
- Node version: check `engines` field in package.json
- Python version: check `python_requires` in setup.py/pyproject.toml
- OS support: check CI matrix (does it test on Linux/Mac/Windows as relevant?)
- Architecture: ARM64/Apple Silicon support if applicable

---

## 4.6 Version & Update Integrity (shared floor)

Applies to every subject at every tier. An audit approves one **version**: the exact release, digest, commit SHA or scope set the user will get (for an unpinned request, what it resolves to now). It does not approve later updates. These rules are a floor (`SKILL.md` Tree terms → Precedence): addenda may tighten them, never loosen them. Record the outcome in the **Version integrity** coverage row.

**Addendum plug-ins:** a `references/criteria/<type>.md` file supplies what the **Addendum:** lines below ask for, under one heading `## Version & Update Integrity (§4.6)` with bullets labelled `V1`–`V5`. No plug-in → the shared default applies.

**Hosted services** with no versioned artifact (most remote-integration subjects): V1–V3 → `N/A (hosted service)`; V4 and V5 apply.

### V1 Version age (cooldown)

Find when the version to be installed was published (registry metadata, release page, store "updated" date, image push time).

| Version age | Effect |
|---|---|
| < 72 h | HIGH flag `fresh version` → CONDITIONAL. Condition: install the previous release if it passes this audit, or wait until the version is 72 h old and re-check advisories. Tier 1 unavailable. The condition is time-bound, so this flag alone does not need the `SKILL.md` escalation notice. |
| 72 h – 7 d | Tier 1 unavailable; no flag on its own. |
| ≥ 7 d | No effect. |
| Unknown | Row `Not available (<why>)`; Tier 1 unavailable. |

- **Security-fix exemption:** a release that fixes a CVE affecting the version the user runs now → `fresh version` drops to MEDIUM if V2 verifies and V3 finds no break. Tier 1 stays unavailable.
- A subject with no prior versions at all is the `SKILL.md` Red Flag "Brand new + no history", not V1.
- **Addendum:** where the publish time comes from; the version unit V1–V3 use (it may treat automated rebuilds of an unchanged release that trace to the publisher's documented pipeline, e.g. Docker Official Images base refreshes, as the same version; never a new release); the client cooldown setting to cite in conditions.

### V2 Verified identity

Identity evidence: signatures, attestations/provenance, trusted publishing, notarization, Authenticode, verified-publisher badges.

- **Verified** = the check passed **and** the identity it names (signer subject + issuer, source repo + workflow + ref, Team ID, certificate subject, publisher account) matches the **expected identity**: the one the vendor documents, or the one prior releases carried. Record the expected identity and its source in the row.
- Evidence checked only for presence, or not matched to an expected identity → note only, no trust credit.
- Absent or undeterminable identity → no credit. Whether absence is itself a flag is the addendum's call.
- **Curated pipelines:** an addendum may name a registry-operated build program with documented review (e.g. Docker Official Images) whose own attestations stand in for a user-verifiable signature. It must say what the auditor checks instead (namespace, attestation present, pipeline source). A subject passing those checks counts as verified for the addendum's Tier 1 identity requirement; every other Tier 1 condition still applies.
- Verified identity proves **origin, not safety**: never enough on its own for APPROVED or Tier 1; never offsets another §4.6 flag or a Red Flag.
- **Addendum:** the identity mechanisms, where the expected identity is documented, and the verification commands.

### V3 Continuity with the prior release

Compare the version to be installed with the previous release:

- Identity evidence that prior releases carried is missing, or names a different signer / repo / workflow than prior releases or vendor docs → HIGH flag.
- No matching upstream source tag, release or changelog entry where the project normally publishes one → HIGH flag.
- Permission, scope, capability or tool-set increase that the changelog does not explain → HIGH flag. Explained increases → rated by the addendum.
- Publisher, maintainer or owner change since the prior release → at least MEDIUM; the addendum's ownership-transfer rules may rate it higher.
- Any V3 item → Tier 1 unavailable. Condition for a V3 HIGH: install the last release that passes V3; re-audit once the vendor explains the change.
- **Addendum:** how to diff releases (manifest permissions, MCP `tools/list`, OAuth scopes, image config) and its ownership-transfer rules.

### V4 Version-scoped compromise

**Confirmed compromise** = an advisory, security blog or vendor postmortem confirms malicious code was published under the subject's name (hijacked account, poisoned pipeline, stolen token). Cite the source and its affected range.

| Case | Rating |
|---|---|
| (a) The version to be installed is in the affected range; or no bounded range is stated; or the compromise is unresolved (bad versions still installable, no vendor remediation) | Red Flag "Confirmed supply chain compromise" → REJECTED + incident-response note |
| (b) Subject malicious by design (malware, typosquat) | Red Flags "Known malware" / "Confirmed typosquat" → REJECTED for every version |
| (c) Resolved: bad versions removed, vendor remediation published, version to be installed outside the range | LOW flag `past compromise (<range>, <date>)`; Tier 1 unavailable. Recommendation: pin the audited version; confirm lockfiles and caches do not resolve into the range |

**Incident-response note** (case a, or when the user already installed an affected version): check lockfiles, caches and hosts for the exposure window. Follow the advisory's clean-up order: some payloads destroy data when their tokens are revoked, so remove persistence first. Then rotate every credential the affected environment could reach.

- **Addendum:** extra incident sources for its ecosystem (e.g. OSV `MAL-` records, store takedown notices).

### V5 Updates & re-audit triggers

The verdict covers the audited version only. A later version is unaudited until it passes V1–V4 again.

- **Re-audit triggers (default):** new major version | publisher, maintainer or owner change (incl. acquisition) | identity change (V3) | new permissions, scopes, capabilities or tools | a confirmed incident naming the subject or its publisher.
- **Re-audit depth:** Tier 2 or deeper, diffed against the audited version.
- **Update control:** APPROVED and CONDITIONAL Recommendations name how to hold updates at the audited version where the platform allows it (exact pin, lockfile, digest, commit SHA, client cooldown, auto-update policy). Where updates cannot be held (hosted services, forced store updates), say so and list the triggers to watch.
- **Addendum:** subject triggers (e.g. ToS or sub-processor change, tool-description change) and the platform's update controls.

---

## 4.7 OpenSSF Scorecard (if available)

If an OpenSSF Scorecard exists for the project (check via `api.securityscorecards.dev`), note:
- **Score below 4/10** → Flag as LOW trust
- **Score 4–7** → MEDIUM trust
- **Score 7+** → HIGH trust signal (not sufficient alone, but positive)

Key sub-scores to highlight if present:
- Branch Protection, Code Review, Signed Releases, Dependency Update Tool
