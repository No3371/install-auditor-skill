<!--
This workflow replaces workflows/generic.md for Type 9 subjects. After
producing findings here, return to SKILL.md Step N for the shared verdict
tree and report shape. The Audit Coverage table and audit-confidence
assertion are owned by the dispatcher — do not duplicate them here.

Phase 4 / M4.4 — ninth subject-specific workflow (fourth Phase 4).
-->

# Remote Integration Workflow (Type 9)

This workflow handles **Type 9: remote-integration** subjects — cloud-hosted services integrated via credential grants (OAuth tokens, API keys, webhook secrets, service accounts). Unlike locally-installed software, the trust boundary is the service's data handling, permission scope, and operational security — no code is installed locally.

After completing all sections, return to `SKILL.md` Step N for shared verdict tree and audit-coverage report shape.

Use `references/criteria/remote-integration.md` for remote-integration-specific tiering and scoring. When it conflicts with the shared rubric, the more-specific remote-integration guidance wins.

---

## Identify

### 1. Determine integration type and credential mechanism

| Integration Pattern / Signal | Integration Type | Credential Mechanism |
|------------------------------|-----------------|---------------------|
| "Add to Slack", OAuth consent screen | OAuth app | OAuth 2.0 token |
| "Connect your GitHub account" | OAuth app | OAuth 2.0 token |
| API key in dashboard → paste into config | API key integration | Static API key |
| Webhook URL generation (e.g., Zapier, IFTTT) | Webhook receiver | Webhook secret/URL |
| Service account JSON (e.g., GCP, Firebase) | Service account | Service account credential |
| "Sign in with Google/GitHub/Microsoft" | SSO/federated auth | OAuth 2.0 / OIDC |
| "Connect to \<service\>" with redirect flow | OAuth app | OAuth 2.0 token |
| Marketplace "Install" button (Slack App Directory, GitHub Marketplace) | Marketplace OAuth app | OAuth 2.0 token |

### 2. Extract available metadata

Collect from the integration channel (consent screen, marketplace listing, documentation, email/link):

- **Service name** — as listed in marketplace/dashboard/documentation
- **Publisher/vendor** — organization behind the service
- **Integration type** — OAuth app | API key | webhook | service account | SSO
- **Requested scopes/permissions** — full list from consent screen or docs
- **Marketplace listing** — if distributed via marketplace (Slack App Directory, GitHub Marketplace, Google Workspace Marketplace, etc.)
- **Version / API version** — if versioned
- **Pricing model** — free, freemium, paid (relevant to sustainability/incentive analysis)

### 3. Gather required context

Before proceeding to Evidence, collect:

- OAuth consent screen or scope documentation
- Vendor's privacy policy and terms of service
- Security/compliance page (SOC2, GDPR, certifications)
- Breach history (web search: `"<vendor>" breach OR incident OR vulnerability`)
- Marketplace reviews/ratings if available
- Vendor domain registration and age (WHOIS) if provenance is uncertain

---

## Evidence — Part A

Automated/structured checks performable without deep research.

1. **Scope audit** — list all requested scopes/permissions; classify each per `references/criteria/remote-integration.md` §1 (low/elevated/high risk); flag any violating least privilege; note if any high-risk scope (admin, wildcard, delete) is present

2. **Vendor identity verification** — confirm the service is the named vendor (not a proxy or phishing clone); check domain ownership, marketplace verification badge, official documentation links match the integration's source URL

3. **Marketplace listing review** — if applicable: verified publisher badge present? Install count, ratings, listing age, developer contact info; is the listing in an official marketplace or a third-party directory?

4. **Redirect URI / callback validation** — for OAuth: does the redirect URI match the vendor's known domains? Localhost, custom scheme, or non-HTTPS callbacks in a production integration?

5. **Token storage & transmission** — does documentation describe secure token handling? HTTPS-only? Token rotation/expiry policy documented? Client-side token exposure risks?

---

## Evidence — Part B

Research-intensive checks requiring documentation review and web search.

6. **Data residency & compliance** — per `references/criteria/remote-integration.md` §2: where is data processed/stored, what compliance certifications exist (SOC2, ISO 27001), DPA availability for regulated data, sub-processor disclosure completeness

7. **Terms of service review** — per `references/criteria/remote-integration.md` §3: data sharing clauses (sold to third parties?), AI/ML training opt-out availability, sub-processor naming, data portability, post-termination retention terms

8. **Breach history & security posture** — per `references/criteria/remote-integration.md` §4: search for known breaches, check security disclosure policy existence, bug bounty program, incident response track record, third-party certifications vs self-attestation

9. **Third-party API trust assessment** — is this the actual vendor or a third-party wrapper/proxy? Does the service intermediate requests through additional infrastructure? For webhooks: are payloads authenticated (HMAC signatures, shared secrets)? Does the integration's domain match the claimed vendor's canonical domain?

10. **Scope necessity analysis** — for each elevated/high-risk scope: is it justified by the integration's stated purpose? Could the same functionality be achieved with narrower scopes? Is documentation provided explaining why the scope is required?

---

## Subject Rubric

### §4.1 OAuth Scope & Permission Model

- What scopes/permissions are requested? Full list.
- Does the integration follow principle of least privilege?
- Are there admin/write/delete scopes that aren't justified by stated functionality?
- Is `offline_access` or equivalent (persistent token) requested? If so, is it justified?
- Any wildcard or catch-all scopes?
- **Scoring:** per `references/criteria/remote-integration.md` §1

### §4.2 Data Handling & Residency

- Where does the vendor process and store data?
- What compliance certifications does the vendor hold (SOC2 Type I/II, ISO 27001)?
- Is a DPA available for regulated/sensitive data use cases?
- Are sub-processors disclosed with notification on change?
- Is data retention policy defined? Is a deletion path available?
- **Scoring:** per `references/criteria/remote-integration.md` §2

### §4.3 Vendor Trust & Provenance

- Is this the official vendor or a third-party proxy/intermediary?
- Is the vendor established (domain age, company history, size, reputation)?
- Marketplace verification status (verified publisher badge if applicable)?
- Does the redirect URI / callback domain match the vendor's canonical domain?
- Is the integration distributed through official channels (marketplace, vendor docs) or informal channels (email, chat links)?
- **Scoring:** established + verified + official distribution → lower tier; unknown proxy + informal distribution → raise tier

### §4.4 Terms of Service & Data Sharing

- Does the vendor share data with third parties beyond service delivery?
- Is data used for AI/ML training? Is opt-out available and easy to exercise?
- What happens to data on account termination? Defined retention/deletion timeline?
- Is data export supported (API, standard format)?
- Are sub-processors named, with change notifications?
- **Scoring:** per `references/criteria/remote-integration.md` §3

### §4.5 Security Posture & Breach History

- Any known breaches? Were they disclosed promptly and remediated?
- Is a security disclosure policy published? Bug bounty or responsible disclosure program?
- SOC2 Type II, ISO 27001, or equivalent third-party audit?
- Token rotation, HTTPS enforcement, secure defaults documented?
- CVE responsiveness and patching track record?
- **Scoring:** per `references/criteria/remote-integration.md` §4

### §4.6 Integration Hygiene

- Does the integration support token expiry and rotation?
- Webhook signature verification available (HMAC, shared secret)?
- Audit logging of API access provided to the integrating party?
- Rate limiting and abuse protection present?
- Least-privilege service account or credential scope recommended by vendor documentation?
- **Scoring:** good hygiene (expiry + rotation + logging + signatures) → neutral to lower tier; no expiry + no logging + no signature verification → raise tier

---

## Subject Verdict Notes

**Toward REJECTED:**
- Wildcard or admin scopes with no functional justification
- Vendor has unacknowledged or unremediated breaches
- Service is a proxy masquerading as the named vendor
- Data sold to third parties or used for AI/ML training with no opt-out
- No compliance documentation for a service handling sensitive or regulated data
- Integration distributed via email/chat phishing link, not official marketplace or vendor documentation
- Non-standard domain, mismatched redirect URI, or suspicious TLD inconsistent with established vendor

**Toward CONDITIONAL:**
- Moderate scopes that are justifiable but warrant scope-reduction request or monitoring
- Vendor has breach history but with transparent disclosure and demonstrated remediation
- Terms allow data sharing for aggregated analytics (not individual/identifiable data)
- Compliance docs exist but incomplete (SOC2 Type I not Type II, DPA available but no EU option)
- Integration hygiene is partial (HTTPS enforced but no token rotation documented)
- **Suggested conditions:** restrict to minimum required scopes, review on credential renewal, monitor vendor security advisories, enable audit logging if available

**Toward APPROVED:**
- Well-known vendor with verified marketplace listing and established reputation
- Minimal scopes consistent with principle of least privilege
- Clean breach history, or historical incident with transparent disclosure and prompt remediation
- Published compliance certifications (SOC2 Type II, ISO 27001)
- Clear, user-favorable terms: no data selling, AI training opt-out available, data portability supported, defined termination/deletion policy
- Official distribution channel (vendor documentation, official marketplace install flow)
