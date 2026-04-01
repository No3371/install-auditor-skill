# License Compatibility Matrix

## Quick Reference

| License | SPDX ID | Commercial Use | Modification | Distribution | Copyleft | SaaS Safe | Notes |
|---|---|---|---|---|---|---|---|
| MIT | MIT | ✅ | ✅ | ✅ | None | ✅ | Most permissive common license |
| Apache 2.0 | Apache-2.0 | ✅ | ✅ | ✅ | None | ✅ | Patent grant included |
| BSD 2-Clause | BSD-2-Clause | ✅ | ✅ | ✅ | None | ✅ | |
| BSD 3-Clause | BSD-3-Clause | ✅ | ✅ | ✅ | None | ✅ | No endorsement clause |
| ISC | ISC | ✅ | ✅ | ✅ | None | ✅ | Functionally similar to MIT |
| MPL 2.0 | MPL-2.0 | ✅ | ✅ | ✅ | File-level | ✅ | Modified files must stay MPL |
| LGPL 2.1 | LGPL-2.1-only | ✅ | ✅ | ✅ | Library | ⚠️ | Dynamic linking usually OK |
| LGPL 3.0 | LGPL-3.0-only | ✅ | ✅ | ✅ | Library | ⚠️ | Review with legal |
| GPL 2.0 | GPL-2.0-only | ✅ | ✅ | ⚠️ | Strong | ❌ | Distributing linked code requires GPL |
| GPL 3.0 | GPL-3.0-only | ✅ | ✅ | ⚠️ | Strong | ❌ | As above, plus patent terms |
| AGPL 3.0 | AGPL-3.0-only | ✅ | ✅ | ⚠️ | Network | ❌ | SaaS use triggers copyleft |
| SSPL | SSPL-1.0 | ⚠️ | ⚠️ | ❌ | Extreme | ❌ | MongoDB; review with legal |
| BSL 1.1 | BUSL-1.1 | ❌ | ❌ | ❌ | N/A | ❌ | Not OSI-approved; commercial restriction |
| CC BY 4.0 | CC-BY-4.0 | ✅ | ✅ | ✅ | Weak | ✅ | For content, not code |
| CC BY-SA 4.0 | CC-BY-SA-4.0 | ✅ | ✅ | ⚠️ | Weak | ⚠️ | Derivatives must be same license |
| CC BY-NC 4.0 | CC-BY-NC-4.0 | ❌ | ✅ | ⚠️ | Weak | ❌ | No commercial use |
| Unlicense | Unlicense | ✅ | ✅ | ✅ | None | ✅ | Public domain dedication |
| No license stated | — | ❌ | ❌ | ❌ | Unknown | ❌ | Default copyright applies — flag! |
| Proprietary | — | ⚠️ | ❌ | ❌ | N/A | ⚠️ | Must review vendor terms |

## Audit Guidance

### For Internal Dev Tools (no distribution)
- MIT, Apache-2.0, BSD, ISC, MPL: **Compatible ✅**
- LGPL: **Compatible ✅** (internal use, no distribution)
- GPL: **Compatible ✅** (internal use only — no distribution triggers copyleft)
- AGPL: **Review needed ⚠️** — if tool runs as a service internally, seek legal opinion
- BSL, SSPL: **Review needed ⚠️**
- No license: **Flag ❌** — cannot use without explicit permission

### For SaaS / Distributed Products
- MIT, Apache-2.0, BSD, ISC: **Compatible ✅**
- LGPL: **Compatible if dynamically linked ✅; Review if statically linked ⚠️**
- GPL / AGPL: **Not compatible without open-sourcing ❌**
- Proprietary: **Must have valid license agreement ⚠️**

### Common Ambiguous Cases
1. **Dual-licensed (e.g., GPL + Commercial)**: Flag as "Review needed" — the commercial license may be needed
2. **"MIT-like" but modified**: Read the actual text; non-standard licenses need legal review
3. **No SPDX identifier, custom text**: Flag for legal review
4. **License file missing from published package**: Flag — may be different from source repo

## What to Report
In the audit report, always state:
- SPDX identifier (or "Unknown/None")
- Compatibility verdict: **Compatible | Review needed | Incompatible**
- One-line reason if not compatible
