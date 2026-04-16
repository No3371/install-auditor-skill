<!-- Remote-integration criteria addendum. Supplements references/criteria.md
     for Type 9 subjects. When guidance here conflicts with the shared rubric,
     this more-specific addendum wins. Phase 4 / M4.4. -->

# Remote Integration — Criteria Addendum

---

## §1 — OAuth Scope & Permission Assessment

Classify each requested scope/permission using the categories below. Apply scoring impact after full scope list is reviewed.

| Scope Category | Low Risk | Elevated Risk | High Risk |
|----------------|----------|---------------|-----------|
| Read-only, own data | `read:user`, `repo:status` | `read:org` | — |
| Read-only, others' data | — | `read:discussion` | `read:email`, `admin:org` |
| Write access | `write:packages` (own) | `write:repo_hook` | `delete:repo`, `admin:*` |
| Full account control | — | — | `*` (wildcard), `sudo` |
| Offline/persistent | — | `offline_access` | `offline_access` + broad scope |

**Scoring impact:**
- All scopes low-risk + principle of least privilege satisfied → lower tier signal
- One or more elevated-risk scopes without documented justification → neutral to raise tier
- Any high-risk scope (admin, wildcard, delete) without clear necessity → raise tier
- Overprivileged: requests write when read suffices, or wildcard when named scopes exist → raise tier

---

## §2 — Data Residency & Compliance Signals

| Signal | Positive | Negative |
|--------|----------|----------|
| Published data processing locations | Named regions, SOC2/ISO27001 | "Global" with no specifics |
| GDPR compliance | DPA available, EU data center option | No DPA, US-only processing |
| Sub-processor disclosure | Published list, change notifications | Undisclosed, blanket consent |
| Data retention | Defined policy, deletion API | Indefinite, no deletion path |

**Scoring impact:**
- SOC2 Type II + published DPA + named regions → lower tier signal
- Partial compliance (SOC2 Type I only, DPA available but no EU option) → neutral
- No compliance documentation for a service handling sensitive/regulated data → raise tier
- Blanket undisclosed sub-processors → raise tier

---

## §3 — Terms of Service & Data Sharing

| Clause | Acceptable | Concerning | Disqualifying |
|--------|------------|------------|---------------|
| Data sharing | Only for service delivery | Aggregated analytics shared | Sold to third parties |
| AI/ML training | Explicit opt-out, no training | Opt-out available but buried | Data used for training by default, no opt-out |
| Sub-processors | Named, notified on change | Named, no notification | Unnamed, blanket authority |
| Data portability | Export API, standard formats | Manual export only | No export capability |
| Termination | Data returned/deleted on exit | 30-day retention then delete | Indefinite post-termination retention |

**Scoring impact:**
- Data sold to third parties → strong REJECTED signal
- AI/ML training with no opt-out → strong REJECTED signal
- Transparent terms with all acceptable clauses → lower tier signal
- Mix of acceptable and concerning clauses → neutral; note specifics in audit

---

## §4 — Breach History & Security Posture

| Signal | Positive | Negative |
|--------|----------|----------|
| Breach history | No known breaches, or disclosed + remediated promptly | Undisclosed breaches, repeated incidents |
| Security disclosure | Published security policy, bug bounty, responsible disclosure | No security contact, no disclosure policy |
| Incident response | Published post-mortems, timely notification | Delayed notification, vague post-mortems |
| Certifications | SOC2 Type II, ISO 27001, pentest reports | Self-attested only, no third-party audit |
| Vulnerability track record | Prompt patching, CVE responsiveness | Slow patching, known unpatched vulns |

**Scoring impact:**
- Repeated unremediated breaches or undisclosed incidents → strong REJECTED signal
- Single historical breach with transparent disclosure + prompt remediation → neutral
- Clean record + SOC2 Type II + bug bounty → lower tier signal
- No discoverable security posture (no policy, no certs, no disclosure history) → raise tier

---

## §5 — Tier Thresholds

**Tier 1 — Quick Audit:**
Well-known vendor (e.g., Google, GitHub, Slack official apps), minimal scopes following least privilege, published compliance documentation (SOC2 Type II, ISO 27001), no disqualifying breach history. OAuth app listed in official marketplace with verified publisher badge. Integration type is unambiguous and distribution channel is official.

**Tier 2 — Standard Audit:**
Known vendor with moderate scopes (some elevated-risk but justifiable), compliance docs available but require review, clean-ish breach history (disclosed and remediated). Third-party OAuth apps with marketplace listing but without verified publisher badge. ToS terms are acceptable or concerning (not disqualifying).

**Tier 3 — Deep Audit:**
Unknown vendor, broad scopes (write/admin/wildcard without justification), no discoverable compliance documentation, breach history with inadequate disclosure, or active security posture concerns. Unverified OAuth apps distributed via email/chat links rather than official marketplace. Proxy services masquerading as the named vendor. Any disqualifying ToS clause (data sold, AI training forced, no opt-out). Non-standard domains or redirect URIs not matching the claimed vendor.
