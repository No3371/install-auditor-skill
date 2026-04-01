# Audit Criteria — Detailed Scoring Rubrics

## Applying Rubrics by Audit Tier

- **Tier 1 (Quick):** Check 4.1 (provenance) and 4.3 (CVEs only). Skip deep rubric scoring — if the package is high-trust and no CVEs exist, a brief confirmation suffices.
- **Tier 2 (Standard):** Score all sections below. This is the default depth.
- **Tier 3 (Deep):** Score all sections below AND review source code for behavioral signals (install scripts, obfuscation, credential access patterns).

The `scripts/registry-lookup.js` script provides hard data for many of these checks (downloads, maintainer count, publish date, dependencies). Use it before manual research.

---

## 4.1 Provenance & Identity

### Typosquatting Check (CRITICAL)
Compare character by character against the known-legitimate package name.
Common substitutions to watch:
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

**Score < -1 → Flag as Stale. Score < -2 → Flag as Abandoned → CONDITIONAL or REJECTED.**

### Issue Tracker Health
- Open issues with maintainer responses in last 90 days → Healthy
- Open issues, no maintainer responses in 90+ days → Concerning
- Issues locked or disabled → Flag

---

## 4.3 Security Track Record

### CVE Severity Mapping
| CVSS Score | Severity | Verdict Impact |
|---|---|---|
| 9.0–10.0 | Critical | Auto-REJECTED if unpatched |
| 7.0–8.9 | High | REJECTED if unpatched; CONDITIONAL if patched in newer version |
| 4.0–6.9 | Medium | CONDITIONAL; note if patched |
| 0.1–3.9 | Low | Flag; APPROVED if patched or mitigated |

**Always check:** Is the CVE in the version being requested, or only in older versions? If user is installing an old pinned version that has known CVEs, escalate.

### Supply Chain Indicators
Search for these terms combined with the package name:
- "malicious package", "trojan", "backdoor", "data exfiltration"
- "hijacked", "compromised maintainer", "typosquatting confirmed"
- "removed from npm/PyPI" + reason

Sources to check: Sonatype blog, Snyk security advisories, Socket.dev, npm security advisories, GitHub Security Advisories (GHSA), OpenSSF Scorecard.

---

## 4.4 Permissions & Access

### Browser Extension Permissions — Risk Matrix
| Permission | Risk Level | Notes |
|---|---|---|
| `<all_urls>` | HIGH | Can read/modify all web traffic |
| `webRequest` + `<all_urls>` | CRITICAL | Full MITM capability |
| `cookies` (all domains) | HIGH | Can exfiltrate all session cookies |
| `history` | HIGH | Full browsing history access |
| `clipboardRead` | MEDIUM-HIGH | Can read anything copied |
| `nativeMessaging` | HIGH | Can communicate with local apps |
| `downloads` | MEDIUM | Can write files to disk |
| `storage` | LOW | Local extension storage only |
| `tabs` | LOW-MEDIUM | Tab titles/URLs |
| `activeTab` | LOW | Only current tab when user clicks |

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

## 4.7 OpenSSF Scorecard (if available)

If an OpenSSF Scorecard exists for the project (check via `api.securityscorecards.dev`), note:
- **Score below 4/10** → Flag as LOW trust
- **Score 4–7** → MEDIUM trust
- **Score 7+** → HIGH trust signal (not sufficient alone, but positive)

Key sub-scores to highlight if present:
- Branch Protection, Code Review, Signed Releases, Dependency Update Tool
