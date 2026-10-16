<!--
This workflow replaces workflows/generic.md for Type 9 subjects. After
producing findings here, return to SKILL.md Step N for the shared verdict
tree and report shape. The Audit Coverage table and audit-confidence
assertion are owned by the dispatcher — this workflow only names the rows
the table must carry for Type 9.
-->

# Remote Integration Workflow (Type 9)

This workflow handles **Type 9: remote-integration** subjects — hosted
services connected through a credential grant (OAuth token, API key,
personal access token, service-account key, webhook secret or URL). No
code is installed locally. The trust boundary is what the grant allows,
**who holds the credential**, and how the vendor handles the data it can
reach.

After completing all sections, return to `SKILL.md` Step N for the shared
verdict tree and audit-coverage report shape.

Use `references/criteria/remote-integration.md` (the addendum) for
remote-integration tiering and scoring. When it conflicts with the shared
rubric, the addendum wins — except the version-integrity floor in
`references/criteria.md` §4.6, which it only tightens.

---

## Identify

### 1. Determine integration type and credential mechanism

| Pattern / signal | Integration type | Credential |
|------------------|------------------|------------|
| "Add to Slack", "Connect your GitHub account", "Connect to \<service\>" redirect flow | OAuth app (delegated) | OAuth access + refresh token |
| Admin grants tenant-wide access with no signed-in user | OAuth app (app-only / application permissions) | Client credential, admin consent |
| "Install" on selected repositories (GitHub) | GitHub App | Short-lived installation token |
| Marketplace install (Slack Marketplace, GitHub Marketplace, Google Workspace Marketplace, Salesforce AppExchange, Microsoft AppSource) | Marketplace app | Usually OAuth |
| API key or PAT copied from a dashboard into the vendor | API key / PAT integration | Static bearer key |
| Vendor posts events to your URL | Inbound webhook | Signing secret |
| You post to a vendor-generated URL (e.g. Slack incoming webhook) | Outbound webhook | Secret embedded in URL |
| Service-account JSON or key file (GCP, Firebase, cloud IAM) | Service account | Long-lived key |
| "Enter this code at \<provider\>/device" or a "connection code" | Device authorization grant | OAuth token |
| "Sign in with Google/GitHub/Microsoft" only | SSO / federated sign-in | OIDC identity only |
| "Add connector" in an AI assistant (remote MCP over HTTP + OAuth, no local code) | AI connector | Usually OAuth |

Several rows can apply (e.g. OAuth app plus inbound webhook): audit each
credential.

### 2. Extract available metadata

From the consent screen, marketplace listing, vendor docs, or the message
that asked for the grant:

- **Service name** and **publisher / vendor**
- **Operator:** first-party (the platform vendor runs it) or third party
- **Integration type** and **credential** (table above)
- **Requested scopes / permissions** — full list, plus delegated vs
  application and user vs admin consent
- **Token lifetime** — refresh / offline / non-expiring / short-lived
- **Credential holder** — vendor servers, your infrastructure, browser
- **Consent path** — how the request reached the user (marketplace,
  vendor docs, admin console, email, chat, phone, device code)
- **Marketplace listing** and verification state
- **AI connectors:** tool list and the LLM providers the data reaches
- **Self-hosted or local components** (agent, CLI, SDK, extension) — each
  is a separate subject; note it and audit it under its own type
- **Pricing model** — free, freemium, paid (incentive analysis)

### 3. Gather required context

- Consent screen or scope documentation
- Vendor privacy policy, terms of service, DPA, sub-processor list
  (including AI providers)
- Security / trust page: certifications, token handling, audit logs,
  egress IPs, revocation procedure
- The platform's API or developer terms where the integration copies,
  indexes or feeds platform data to an AI model
- Incident search for the service vendor **and** the integration vendor:
  `"<vendor>" breach OR incident OR "OAuth token" OR "revoked"`
- Vendor domain age (WHOIS) when provenance is uncertain

---

## Evidence — Part A: Tier Triage

Tier the subject with the addendum §10. Tier 1 needs every Tier 1
condition; any Tier 3 condition sets Tier 3; otherwise Tier 2.
Escalate mid-audit when a later check finds a Tier 3 condition.

- **Tier 1 — Quick:** first-party or verified marketplace app, no
  High-class scope, official consent path, published compliance
  documentation, no key / webhook / AI-use / incident / §4.6 flag.
  Scope: checks 1–3, 5 and 8–11 below, briefly; the Quick skeleton in
  `SKILL.md`.
- **Tier 2 — Standard:** the default. Scope: every check that applies;
  full report template.
- **Tier 3 — Deep:** unknown or unverified vendor, unjustified High-class
  scope, consent-path or redirect flag, token-custody incident, required
  service-account key, risky AI connector, proxy, or disqualifying ToS.
  Scope: Tier 2 plus a documented answer to every addendum row, and a
  line-by-line justification of each High-class scope.

---

## Evidence — Part B: Checks

1. **Scope audit** — classify each scope Low / Elevated / High (addendum
   §1, including the standing-grant modifier and provider maps). For each
   Elevated or High scope: is it needed for the stated purpose, and does
   a narrower option exist?
2. **Vendor identity & marketplace verification** — the integration is
   the named vendor (domain, consent-screen publisher, docs link back to
   the listing); verification signals per addendum §7.
3. **Consent path & distribution** — how the request arrived (addendum
   §6): official channel, or email / chat / phone / someone else's device
   code; consent-screen name matches the publisher.
4. **OAuth flow hygiene** — redirect domain, grant type, device-code
   origin, refresh-token handling (addendum §3). Native apps may use
   loopback or private-use scheme callbacks.
5. **Token custody & lifecycle** — who holds the token, for how long,
   with what custody evidence; integration-vendor incidents (addendum
   §6).
6. **Non-OAuth credentials** (if applicable) — key scope, expiry,
   network restriction, ownership, service-account key requirement
   (addendum §2).
7. **Webhooks** (if applicable) — direction; signature, replay window,
   rotation; URL-as-secret handling (addendum §9).
8. **Data residency & compliance** — regions, transfer mechanism, DPA,
   certifications, sub-processors (addendum §4).
9. **Terms, AI data use & sub-processors** — data sharing, training, AI
   sub-processors, platform API terms; AI connector tool baseline
   (addendum §5).
10. **Breach history & incident search** — service vendor and
    integration vendor; security posture (addendum §8).
11. **Version & update integrity** — shared `references/criteria.md`
    §4.6 with the addendum plug-in: V1–V3 `N/A (hosted service)`, V4
    incident scope, V5 triggers for the Recommendation.

### Audit coverage tracking

The `SKILL.md` Audit Coverage table keeps every Required row from
`references/criteria.md` (labels unchanged) and adds the Type 9 rows.
Tier words follow `references/criteria.md` "Rows by tier". A Required
row that cannot apply stays as the `N/A (<reason>)` shown; one line each.

| Check | Tier 1 | Tier 2 | Tier 3 | Type 9 meaning / status |
|-------|--------|--------|--------|-------------------------|
| Registry / metadata lookup | Required | Required | Required | Marketplace listing or vendor docs page |
| Typosquat / name verification | Required | Required | Required | Vendor, app and domain names vs the real vendor (check 2) |
| CVE / advisories (requested version) | Required | Required | Required | `N/A (hosted service, no versioned artifact)` unless a self-hosted component is in scope |
| License compatibility | Required | Required | Required | `N/A (hosted service; terms in the data-handling row)` |
| Version integrity (§4.6) | Required | Required | Required | `Done` — V1–V3 N/A (hosted service); V4 result; V5 triggers listed |
| Permissions / least privilege | Required | Required | Required | Scope audit (check 1) |
| Vendor identity & consent path | Required | Required | Required | Checks 2–3 |
| Token custody & lifecycle | Required | Required | Required | Check 5 |
| Web search — incidents & supply chain | Required | Required | Required | Check 10, both vendors |
| Data handling, compliance & AI use | Required | Required | Required | Checks 8–9 (brief at Tier 1) |
| OAuth flow hygiene | Tier-skip | Required | Required | Check 4; `N/A (no OAuth flow)` otherwise |
| Maintainer / activity / health | Tier-skip (brief) | Required | Required | Vendor viability, listing age, ownership changes |
| Non-OAuth credential review | If applicable | If applicable | If applicable | Check 6 |
| Webhook verification | If applicable | If applicable | If applicable | Check 7 |
| OpenSSF Scorecard | Optional | Required | Required | `N/A (hosted service)` unless an open-source self-hosted component |
| Dependency tree / transitive risk | Tier-skip | Required | Required | `N/A (hosted service)`; AI sub-processors go in the data-handling row |
| Install script review (`pre`/`postinstall`, etc.) | Tier-skip | Required | Required | `N/A (no local install)` |
| Source code review (behavioral) | Tier-skip | Tier-skip | Required | `N/A (hosted service)` |

---

## Subject Rubric

Sections follow the shared `references/criteria.md` numbering, specialized
for Type 9.

### 4.1 Provenance & Identity

- Official vendor or a proxy / wrapper? First-party or third party?
- Vendor established (company history, domain age, reputation)?
- Marketplace and consent-screen verification (addendum §7) — identity,
  not safety.
- Official consent path and matching redirect domain (addendum §3, §6)?

### 4.2 Maintenance & Longevity

- Vendor viability, recent acquisition or ownership change, listing last
  updated.
- Does the integration's function depend on platform API terms that
  restrict it (addendum §5)? That is a continuity risk.

### 4.3 Security Track Record

- Breaches and incidents at the service vendor and the integration vendor;
  disclosure and remediation quality (addendum §6, §8).
- Security policy, bug bounty, third-party certifications.
- CVE row per addendum §8 (hosted: `N/A`).

### 4.4 Permissions & Access

Dominant axis for Type 9.

- Scope classes, justification, narrower options (addendum §1).
- Token lifetime and custody; standing grants held by third parties
  (addendum §6).
- API keys, PATs, service-account keys (addendum §2); webhooks (addendum
  §9).
- Org controls available to contain the grant (addendum §6).

### 4.5 Data Handling, Terms & AI Use

- Residency, transfer mechanism, DPA, retention, deletion (addendum §4).
- Data sharing, AI training, AI sub-processors, export, termination
  (addendum §5).
- AI connectors: tool baseline and destructive tools (addendum §5).

### 4.6 Version & Update Integrity

- Shared `references/criteria.md` §4.6 with the addendum plug-in:
  hosted → V1–V3 `N/A (hosted service)`; V4 and V5 apply.
- The approved unit is the vendor, app identity and exact scope set
  (plus tool list for AI connectors). Any change is a re-audit trigger.

---

## Subject Verdict Notes

**Toward REJECTED (rate CRITICAL):**
- High-class scope with no functional justification
- Consent requested by phone / "IT support", or via a device or
  connection code someone else supplied
- Email or chat link plus an unknown vendor, unverified app or High scope
- Consent-screen name or branding differs from the registered publisher
- Redirect domain mismatch, non-HTTPS web callback, or the vendor asks
  for your platform password in its own form
- Service masquerading as the named vendor
- Unresolved token theft at the integration vendor; unremediated active
  exploitation of the service
- Repeated unremediated or undisclosed breaches
- Data sold to third parties, AI training on by default with no opt-out,
  or data sent to unnamed AI providers

**Toward CONDITIONAL (HIGH):**
- Third party holds a standing grant with a High-class scope
- Justified High-class scope where a narrower option exists
- Required service-account key or admin / never-expiring API key
- Unsigned inbound webhook that triggers privileged actions; webhook URL
  exposed
- Unverified app requesting sensitive scopes, with no consent-path flag
- Function conflicts with the platform's API terms
- No compliance documentation for sensitive or regulated data
- **Suggested conditions:** admin-approval consent or app allowlist;
  narrowest scope or GitHub App variant; inventory and periodic grant
  review; alerts on new authorizations and bulk export; token IP
  restriction; documented revocation runbook; fresh grant and secret
  rotation after a vendor incident.

**Toward APPROVED:**
- First-party app, or verified publisher in the official marketplace
- Low or justified Elevated scopes only; no standing High-class grant
- Official consent path, correct redirect domain
- Clean incident record for both vendors, or disclosed and remediated
- SOC 2 Type II or ISO/IEC 27001; DPA with a stated transfer mechanism
- Favorable terms: no data selling, AI training off or opt-out, named AI
  sub-processors, export and deletion supported

**Recommendation wording:** name the approved app, publisher and exact
scope set; state that updates cannot be held at a version (hosted
service); list the re-audit triggers from `references/criteria.md` §4.6
V5 and the addendum plug-in; give the revocation path.
