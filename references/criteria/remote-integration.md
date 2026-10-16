<!-- Remote-integration criteria addendum. Supplements references/criteria.md
     for Type 9 subjects. When guidance here conflicts with the shared rubric,
     this more-specific addendum wins — except the shared floor in
     references/criteria.md §4.6, which this addendum only tightens or fills
     (see "Version & Update Integrity (§4.6)" below). -->

# Remote Integration — Criteria Addendum

Per-subject scoring for **Type 9: remote-integration** audits: hosted
services reached through a credential grant (OAuth token, API key, personal
access token, service-account key, webhook secret or URL). The risk is
what the grant lets the service do, **who holds the credential**, and how
the vendor handles the data it can reach.

Rating words map to the `SKILL.md` verdict tree: **CRITICAL** → REJECTED,
**HIGH** → CONDITIONAL, **MEDIUM** counts toward the 3+ MEDIUM rule,
**LOW** / note → no verdict effect. Record each rating and its reason in
Risk Flags.

---

## §1 — Scope & Permission Assessment

Classify every requested scope or permission into one class. Provider
docs and consent screens give the semantics; the maps below are examples,
not complete lists. A scope you cannot classify is **High** until its
docs show otherwise.

| Class | What it lets the integration do |
|-------|--------------------------------|
| **Low** | Sign-in / identity only (`openid`, `profile`, `email`); read metadata; act only on the integration's own resources (post as the app, its own files or records) |
| **Elevated** | Read the consenting user's own content (mail, files, calendar, messages); write or send on the user's behalf in limited resources; read org directory or membership |
| **High** | Read or write content beyond one user (org-wide, all mailboxes / files / repos); any app-only or tenant-wide permission granted by admin consent; delete; admin or directory management; modify CI workflows, webhooks, keys or package publishing; any scope the provider itself labels restricted |

**Standing-grant modifier:** a refresh token, offline access or a
non-expiring token held by a **third party** (not the platform vendor
itself) turns an Elevated content-read scope into High.

| Finding | Rating |
|---------|--------|
| High scope with no functional justification | CRITICAL |
| High scope, justified, but a narrower option exists (GitHub App on selected repos, fine-grained token, per-file or per-resource scope) | HIGH — condition: use the narrower option |
| High scope, justified, no narrower option offered | MEDIUM — note why |
| Elevated scope with no stated justification | MEDIUM |
| Write requested where read suffices, or a broad scope where named scopes exist | MEDIUM (HIGH if the broad scope is High class) |
| All scopes Low, or Elevated with justification | No flag |

### Provider maps (examples)

**GitHub.**
- Low: no scope (public read), `read:user`, `user:email`, `repo:status`.
- Elevated: `read:org`, `public_repo` (writes public repos), `gist`,
  `notifications`, `read:repo_hook`.
- High: `repo` (full read **and** write to every private repo the user
  can reach; OAuth apps have no read-only private-repo scope), `workflow`
  (edits Actions workflow files — a CI supply-chain pivot), `write:org`,
  `admin:org`, `admin:repo_hook`, `admin:org_hook`, `delete_repo`,
  `write:packages`, `admin:public_key`, `admin:gpg_key`.
- A **GitHub App** (fine-grained permissions, installable on selected
  repositories, short-lived installation tokens) is the narrower option
  to an OAuth app; a fine-grained personal access token is the narrower
  option to a classic one.

**Google.**
- Google classifies scopes as non-sensitive, sensitive or **restricted**.
  Restricted scopes (e.g. `gmail.readonly`, full `drive`) → High.
- Admin SDK directory scopes (`admin.directory.*`) and domain-wide
  delegation (a service account acting as any user) → High.
- Narrower options: per-file `drive.file` instead of full `drive`;
  read-only variants instead of read-write.

**Microsoft Entra / Graph.**
- Delegated permissions act as the signed-in user; **application**
  permissions act with no user, tenant-wide, and need admin consent →
  High (e.g. application `Mail.Read`, `Files.ReadWrite.All`,
  `Directory.ReadWrite.All`).
- Delegated `User.Read`, `openid`, `profile`, `email` → Low; delegated
  `Mail.Read` → Elevated; delegated `*.ReadWrite.All` → High.
  `offline_access` → standing-grant modifier.

**Slack.**
- Bot tokens act as the app in conversations it is added to; user tokens
  act as the user, with the user's access.
- Low: `chat:write` (posts as the app), `channels:read`.
- Elevated: `users:read`, `users:read.email`, `channels:history`,
  `files:read`, `chat:write.customize` (posts under another name / icon).
- High: `admin.*` scopes, user-token `im:history` / `mpim:history`
  across the workspace.

---

## §2 — Non-OAuth Credentials

API keys, personal access tokens (PATs), service-account keys and
webhook URLs are bearer secrets: whoever holds one has its full access.

| Signal | Positive | Negative |
|--------|----------|----------|
| Key scope | Restricted key (read-only, per-resource, per-environment) | Full-account or admin key |
| Lifetime | Expiry set; rotation documented | Never expires; no rotation path |
| Network restriction | IP / referrer allowlist supported and used | Usable from anywhere |
| Ownership | Dedicated key per integration, on a service identity | Shared key, or an admin's personal key or classic PAT |
| Revocation | Per-key revoke in the dashboard | Revoking breaks every integration sharing the key |

**Service-account keys.** A vendor that requires a downloadable,
long-lived service-account key (e.g. a GCP JSON key) → HIGH when the
platform offers a keyless option (workload identity federation, OAuth, a
GitHub App); MEDIUM otherwise. Google Cloud enforces a secure-by-default
policy that blocks service-account key creation for organizations created
on or after 2024-05-03, so such a vendor asks you to weaken a platform
default. Conditions: keyless option if offered; else a dedicated service
account with minimum roles, a key-expiry or rotation schedule, and a
policy exception scoped to one project.

**Scoring:** full-account or admin key with no expiry → HIGH; personal
key of an admin or classic PAT with High-class scopes → HIGH; scoped key
with expiry or rotation → no flag.

---

## §3 — OAuth Flow Hygiene

Baseline: **RFC 9700** (OAuth 2.0 Security Best Current Practice, BCP
240, January 2025). OAuth 2.1 is still an Internet-Draft — do not score
"OAuth 2.1 compliance" as a pass/fail check.

| Observation | Rating |
|-------------|--------|
| Redirect / callback domain does not match the vendor's canonical domain, or a web app uses a non-HTTPS callback | CRITICAL |
| Vendor asks for your platform password in its own form instead of the platform's sign-in page (password grant or credential capture) | CRITICAL |
| Device-code or "connection code" prompt (RFC 8628 device authorization grant) where the code came from someone else (call, email, chat), not from a device or CLI you started | CRITICAL |
| Implicit grant (`response_type=token` in the authorize URL) | MEDIUM — deprecated by RFC 9700 |
| Native or desktop app using a loopback (`http://127.0.0.1:<port>`, `http://localhost:<port>`) or private-use URI scheme callback | No flag — sanctioned for native apps by RFC 8252 |
| Refresh tokens rotated on use or sender-constrained (DPoP, RFC 9449; mutual TLS) | Positive note |
| PKCE (`code_challenge` in the authorize URL) for a public client | Positive note when observable; absence alone is not a flag |

---

## §4 — Data Residency & Compliance

| Signal | Positive | Negative |
|--------|----------|----------|
| Processing locations | Named regions, region choice | "Global" with no specifics |
| Cross-border transfer (GDPR) | Transfer mechanism stated (adequacy decision such as EU-US Data Privacy Framework certification, or SCCs) and DPA available | No DPA, no transfer mechanism stated |
| Sub-processor disclosure | Published list incl. AI providers, change notifications | Undisclosed, blanket consent |
| Data retention | Defined policy, deletion API | Indefinite, no deletion path |
| Certifications | SOC 2 Type II, ISO/IEC 27001 (ISO/IEC 42001 is an extra positive for AI vendors) | Self-attested only |

Processing outside the EU is not negative by itself; a missing transfer
mechanism is.

**Scoring:** SOC 2 Type II + DPA + named regions → positive; partial
(SOC 2 Type I only, DPA without regional options) → neutral; no
compliance documentation for a service handling sensitive or regulated
data → HIGH; undisclosed sub-processors → MEDIUM.

---

## §5 — Terms, Data Sharing & AI Use

| Clause | Acceptable | Concerning (MEDIUM) | Disqualifying (CRITICAL) |
|--------|------------|---------------------|--------------------------|
| Data sharing | Only for service delivery | Aggregated analytics shared | Sold to third parties |
| AI/ML training on your data | Off, or explicit opt-out | Opt-out available but buried | On by default, no opt-out |
| AI sub-processors (LLM providers) | Named, with retention terms or zero-data-retention | Named, retention unstated | Data sent to unnamed AI providers |
| Data portability | Export API, standard formats | Manual export only | No export |
| Termination | Data returned or deleted on exit | Fixed retention window, then delete | Indefinite retention after exit |

**Platform API terms.** Platforms can restrict what integrations do with
data fetched through their APIs — for example, Slack's API terms (2025)
limit bulk export, persistent copies or indexes, and LLM use of API data;
check the platform's current text. An integration whose core function
conflicts with the platform's terms → HIGH (continuity and compliance
risk). Condition: the vendor confirms it uses a platform-sanctioned API,
or written confirmation from the platform.

**AI connectors** (assistant connectors, hosted MCP servers): record the
tool list at audit time as the baseline for re-audit (§4.6 V3/V5 below).
Destructive or outbound tools (delete, send, pay, share externally) need
a stated justification; unjustified → HIGH.

---

## §6 — Token Custody & Consent Path

The 2025–26 SaaS attacks stole standing tokens from **integration
vendors** and used them to bulk-export customer data from platforms that
were not themselves vulnerable (e.g. Salesloft Drift, August 2025), or
talked employees into approving a malicious connected app by phone (e.g.
the UNC6040 vishing campaign posing as IT support). Score both paths.

### Custody (who holds the credential)

| Situation | Rating |
|-----------|--------|
| First-party: the platform vendor operates the integration itself | No custody flag |
| Third party holds a standing grant with only Low or Elevated scopes | Note — list custody evidence |
| Third party holds a standing grant with any High-class scope (after the §1 modifier) | HIGH `standing high-privilege grant` — conditions below |
| Confirmed theft of customer tokens or keys from the integration vendor, unresolved (tokens not revoked, no vendor remediation) | CRITICAL |
| Same, resolved (tokens revoked, postmortem and remediation published) | MEDIUM `past token-custody incident (<date>)`; Tier 1 unavailable; condition when CONDITIONAL: fresh grant, rotate secrets the old grant could reach |

Custody evidence (positive): encrypted token storage described;
customer-visible audit log of API calls; vendor egress IPs published so
the platform can restrict token use by IP; token rotation; dormant
credentials deactivated; published revocation procedure.

### Consent path (how the grant was requested)

| Situation | Rating |
|-----------|--------|
| Official marketplace install, vendor docs, or the user's own admin console | No flag |
| Unsolicited email or chat link | CRITICAL when combined with an unknown vendor, unverified app or High scope; otherwise HIGH |
| Phone or "IT support" request to approve an app or enter a code | CRITICAL |
| Consent-screen app name or branding differs from the registered publisher | CRITICAL |

### Org controls (use as conditions)

- **Admin-approval consent:** users cannot grant High-class scopes
  themselves (e.g. Entra admin consent workflow with user consent limited
  to verified publishers and low-impact permissions; Google Workspace app
  access control; Slack app approval; GitHub organization OAuth app access
  restrictions).
- **Inventory and review:** list connected apps and grants; review
  periodically (e.g. quarterly); revoke unused grants.
- **Alerting:** alert on new app authorizations and on bulk export or API
  volume spikes.
- **Token restriction:** restrict tokens to the vendor's published egress
  IPs where the platform supports it.
- **Revocation runbook:** how to revoke this app's tokens org-wide, then
  rotate any secrets stored in data the app could read.

---

## §7 — Vendor & Marketplace Verification

Verification proves **identity, not safety** (`references/criteria.md`
§4.6 V2): it lowers tier only together with the other Tier 1 conditions.

| Platform | Signal | Notes |
|----------|--------|-------|
| Slack | Listed in **Slack Marketplace** (renamed from Slack App Directory, 2024) | Listing passed Slack's review; unlisted apps installed by link get no credit |
| GitHub | Marketplace verified publisher; GitHub App vs OAuth app | Prefer the vendor's GitHub App variant (§1) |
| Google | OAuth app verification; **unverified app** warning screen; restricted scopes need an annual third-party security assessment (CASA) for apps that reach data through their servers | Unverified app requesting sensitive or restricted scopes → HIGH (CRITICAL with a consent-path flag) |
| Microsoft Entra | **Verified publisher** badge on the consent prompt | Unverified publisher requesting High-class permissions → HIGH |
| Salesforce | AppExchange listing (passed security review) | Connected apps installed outside AppExchange get no credit |

Proxy or wrapper services (the integration is not the named vendor, or
routes requests through undisclosed infrastructure) → HIGH; one
masquerading as the named vendor → CRITICAL.

---

## §8 — Breach History & Security Posture

Search both the **service vendor** and, when different, the **integration
vendor** that will hold your credential.

| Signal | Positive | Negative |
|--------|----------|----------|
| Breach history | None, or disclosed + remediated promptly | Undisclosed breaches, repeated incidents |
| Security disclosure | Security policy, bug bounty, responsible disclosure | No security contact or policy |
| Incident response | Published postmortems, timely notification | Delayed notification, vague postmortems |
| Certifications | SOC 2 Type II, ISO/IEC 27001, pentest summaries | Self-attested only |

**Scoring:** repeated unremediated or undisclosed breaches → CRITICAL;
single historical breach, disclosed and remediated → no flag; no
discoverable security posture → MEDIUM. Token-custody incidents are
rated by §6.

**CVE row (§4.3 plug-in):** a hosted service has no versioned artifact,
so the `CVE / advisories` row is `N/A (hosted service, no versioned
artifact)` and the `SKILL.md` Blocking CVE node does not apply. A known
unpatched vulnerability in the vendor's service → HIGH; confirmed active
exploitation that is not yet remediated → CRITICAL. A self-hosted or
locally installed component (agent, CLI, SDK, browser extension) is a
separate subject: note it in the report and audit it under its own type.

---

## §9 — Webhooks

Record the direction: **inbound** (the vendor posts to your endpoint) or
**outbound** (you post to a vendor URL).

| Check (inbound) | Good | Rating if missing |
|-----------------|------|-------------------|
| Payload signature | HMAC-SHA256 or asymmetric (e.g. Ed25519) signature verified by the receiver | HIGH if the receiver triggers privileged actions (deploy, write, payment); MEDIUM otherwise |
| Replay protection | Signed timestamp, rejected outside a short window (typically ~5 min) | MEDIUM |
| Verification method | Constant-time comparison; idempotency on the message id | Note |
| Secret rotation | Several signatures accepted during rotation | Note |

The Standard Webhooks spec (`webhook-id`, `webhook-timestamp`,
`webhook-signature` headers; `v1` HMAC-SHA256, `v1a` Ed25519) covers all
four checks and is a positive signal.

**Outbound:** a webhook URL that embeds its secret (e.g. Slack incoming
webhook URLs) is a bearer credential. Store it as a secret and confirm a
revoke / regenerate path. URL found in a repo, ticket or shared doc →
HIGH; condition: regenerate it.

---

## Version & Update Integrity (§4.6)

- **V1** — The service itself has no versioned artifact: `N/A (hosted
  service)`. The audited "version" is the vendor, app identity and the
  exact scope set (plus, for AI connectors, the tool list) approved now.
- **V2** — Identity mechanisms are the marketplace and consent-screen
  verification signals in §7; the expected identity is the publisher the
  vendor's own docs name. Credit them per the shared V2 rule. Absence on
  a platform that offers verification is rated by §7.
- **V3** — `N/A (hosted service)` at first audit. On re-consent or
  re-audit, diff the requested scopes and the connector tool list against
  the audited set: an increase the vendor's changelog does not explain →
  HIGH (shared V3 rule).
- **V4** — Incident sources: vendor trust or status pages, platform
  notices (mass token revocations, marketplace removals), government
  advisories and threat-intelligence reports. A hijacked listing or a
  malicious app update is case (a) until resolved. Token theft from the
  integration vendor is rated by §6, not V4.
- **V5** — Updates cannot be held: the vendor changes the service without
  a new install. Say so in the Recommendation and list the triggers.
  Subject triggers (in addition to the shared defaults): new or changed
  scope request or re-consent prompt | new tools or changed tool
  descriptions in an AI connector | vendor acquisition or ownership
  change | ToS, privacy-policy, AI-use or sub-processor change | security
  incident at the service vendor, integration vendor or platform | grant
  unused for a review period (e.g. 90 days) → revoke rather than
  re-audit. Update controls to cite: admin-approval consent and app
  allowlists (§6), which stop a changed scope set from taking effect
  without review.

---

## §10 — Tier Thresholds

**Tier 1 — Quick Audit:** all of:
- First-party app of the platform vendor, or verified publisher listed in
  the platform's official marketplace (§7)
- No High-class scope after the §1 modifier; Elevated scopes justified
- Official consent path (§6) and correct redirect domain (§3)
- Published compliance documentation (SOC 2 Type II or ISO/IEC 27001)
- No §2 long-lived key, no §9 webhook finding, no §5 flag
- No incident flag (§6, §8) and no §4.6 flag

**Tier 2 — Standard Audit:** the default, e.g.:
- Established third-party vendor, marketplace-listed without
  verification
- Justified High-class scopes, or a standing grant held by a third party
- API keys, PATs or webhooks in scope
- Compliance docs exist but need review; ToS concerning, not
  disqualifying

**Tier 3 — Deep Audit:** any of:
- Unknown vendor, or unverified app on a platform that offers
  verification
- High-class scope without justification
- Any consent-path flag (§6) or redirect mismatch (§3)
- Past or present token-custody incident (§6)
- Required service-account key (§2)
- AI connector with destructive tools or unnamed AI sub-processors (§5)
- Proxy or wrapper service (§7); disqualifying ToS clause (§5)
