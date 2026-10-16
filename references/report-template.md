# Report Template — Full (Tier 2 / Tier 3)

Full report skeleton for Standard and Deep audits. File location, Audit confidence rating rules, and the Quick (Tier 1) skeleton live in `SKILL.md` Step N → Report. Keep the verdict line, the `## Audit Coverage` heading, and the `**Audit confidence (coverage):**` line identical to the Quick skeleton; graders and tooling parse them.

```
# Install Audit: <name> v<version>

**Verdict: [APPROVED ✅ | CONDITIONAL ⚠️ | REJECTED ❌]**
**Audit tier:** [Standard | Deep]
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

**Audit confidence (coverage):** [ High | Moderate | Low ] — [short reason: e.g., "8/9 checks Done, 1 Not available"]

Audit confidence measures **how completely the tier-appropriate checklist was executed** — **not** whether the installable is free of vulnerabilities. Unknown issues remain possible even when coverage is High.

| Check | Status | Source or notes |
|-------|--------|-----------------|
| Registry / metadata lookup | Done | e.g., registry-lookup / npm API |
| Typosquat / name verification | Done | compared to `<legitimate name>` |
| CVE / advisories | Done, 0 results | OSV, GHSA |
| Version integrity | Done | §4.6: published <date> (<age>); identity matches <expected identity, source> |
| OpenSSF Scorecard | Not available | no repo for Scorecard API |
| Source code review (behavioral) | Skipped (Tier 2) | Tier 3 only |
| *(add rows from `references/criteria.md` for this tier)* | | |

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
- [ ] Verify checksum/signature against the expected identity (`references/criteria.md` §4.6 V2)
- [ ] Check lock file for unexpected entries after install
- [ ] Review post-install script output if applicable
- [ ] Hold updates at the audited version where possible; re-audit on any `references/criteria.md` §4.6 V5 trigger

**Sources:** <URLs consulted>
```
