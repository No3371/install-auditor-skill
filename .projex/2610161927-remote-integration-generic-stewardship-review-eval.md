# remote-integration-generic-stewardship-review

> **Status:** Complete
> **Author:** Claude (Opus)
> **Parent:** Orchestrator
> **Subject:** `STEWARDSHIP.md` scheduled review pass (§ Re-Evaluation Checklist steps 1–3; step 4 offline only) — `workflows/remote-integration.md` + `references/criteria/remote-integration.md`; `workflows/generic.md` + routing context `references/classifier.md` + shared core `references/criteria.md`
> **Type:** Gap Analysis (Status Quo vs ecosystem reality, 2026-10-16)
> **Tier:** Standard
> **Lenses Applied:** Constraint Mapping | Inversion | Steel-Manning
> **Related Projex:** 2604070218-install-auditor-subject-typed-redesign-nav.md | 2604161000-remote-integration-workflow-m44-walkthrough.md | 2604170930-trim-generic-md-m52-walkthrough.md | 2604160430-tighten-classifier-m51-walkthrough.md | 2610161852-dispatcher-rubric-consistency-walkthrough.md | 2610161910-dispatcher-lean-report-and-trigger-walkthrough.md | 2610161927-browser-extension-ide-plugin-stewardship-review-eval.md | 2610161927-registry-package-and-ci-action-stewardship-review-eval.md

---

## 1. Executive Summary

Both subjects are past due (never reviewed; remote-integration 120 d, generic 180 d; last edits ~2026-04-16/17). **remote-integration** is structurally behind its siblings — no Tier Triage step, no Audit Coverage row set — and its threat model predates the 2025–26 SaaS OAuth supply-chain wave (Salesloft Drift → Gainsight → Klue; ShinyHunters vishing/device-code consent). Its scope table is GitHub-only and partly wrong (nonexistent `read:email`, misfiled `admin:org`, missing `repo`/`workflow`). Webhook, API-key, service-account and AI-connector coverage is thin. **generic** is sound in shape (probe → clarify → defensive minimum → warning), and the classifier's low-confidence routing still fits. Its Phase 3 checklist, though, is package-shaped and does not suit the non-package subjects that actually land there. Tier and audit-confidence handling also became ambiguous after today's report split. Recommendation: two plan-projex — **(A) remote-integration rubric refresh** and **(B) generic/classifier fallback fit**. Neither has a CRITICAL finding: current rubrics would still reach the right verdict on the 6 existing evals, but they would under-detect the dominant 2025–26 attack pattern.

## 2. Evaluation Scope

**Questions:** Do these files still reflect reality as of 2026-10-16? What is stale, missing, or wrong? For generic, do probe/clarify/defensive flow and the classifier's low-confidence routing still fit?

| Criterion | Weight | Description |
|---|---|---|
| Ecosystem currency | High | Rubric reflects current OAuth/SaaS/webhook/AI-data norms and attack patterns |
| Structural parity | High | Workflow provides what the dispatcher expects (tier → report shape, coverage rows) |
| Correctness | High | Literal identifiers/scope names/claims are accurate |
| Routing fit | Medium | Classifier routes ambiguous/hybrid subjects sensibly; generic flow handles what reaches it |
| Eval coverage | Medium | Eval cases exercise the current threat model |

**Out of scope:** editing workflow/criteria/STEWARDSHIP files (review only — checklist step 5 says file a plan); STEWARDSHIP steps 7–8 (inventory dates, nav log) — left for the orchestrator; live `run_evals.py run` (costs money, not approved); other subjects (sibling evals).

## 3. Context Analysis

- remote-integration created by M44 (2604161000-remote-integration-workflow-m44-*), 173 + 91 lines; untouched since except for today's dispatcher changes that it references (`SKILL.md` Step N).
- generic rewritten by M52 (2604170930-trim-generic-md-m52-*) to an 80-line, 4-phase fallback.
- Today on base: `references/classifier.md` created + Red Flags / "Tree terms & precedence" rewritten (2610161852); report template split into Tier 1 Quick skeleton in `SKILL.md` vs Tier 2/3 `references/report-template.md`, reports default to `.install-audits/` (2610161910); Python script twins (2610161849).
- Sibling workflows (`ci-action.md`, `agent-extension.md`, `cli-binary.md`, …) each carry an explicit Tier Triage and an "Audit coverage tracking" table; remote-integration does not (`grep -ci tier`: remote-integration 3 vs 8–31 for siblings, none are triage).

## 4. Foundations

| Assumption | Validity | Risk if wrong | Sensitivity |
|---|---|---|---|
| The SaaS vendor's own breach history is the main remote-integration risk signal | Weakened — 2025–26 incidents hit the *integration vendor's token store*, platform not vulnerable | Approves integrations whose standing tokens are the attack surface | High — drives RI-3 |
| A one-time approval of a connector stays valid until "major version bump" | False for SaaS/AI connectors (silent scope/tool drift) | Approved connector later gains destructive tools/scopes unreviewed | Medium — RI-7 |
| Subjects reaching generic are mostly packages with unclear type | Weak — all 3 generic evals are non-package (portal+cert, PowerShell one-liner, monorepo `make`) | Phase 3 checks (OSV by name+version, maintainer count) return nothing useful | Medium — G-1 |
| OAuth 2.1 is a final standard | False — still Internet-Draft (rev -15 Mar 2026; -16 reportedly Sep 2026) | Citing "OAuth 2.1 compliance" as a binary check | Low — cite RFC 9700 as the normative baseline |

## 5. Analysis — remote-integration

### RI-1 · No Tier Triage step and no Audit Coverage row set — HIGH · plan
- **Finding:** Workflow never assigns a tier. Criteria §5 defines Tier 1/2/3 thresholds but no workflow step invokes them. The dispatcher's report shape (Quick skeleton vs `references/report-template.md`) and audit-confidence rules key off tier. There's also no subject coverage table, so auditors fall back to the canonical rows in `references/criteria.md`. Those rows are package-shaped: Registry lookup, License, CVE for the requested version, OpenSSF Scorecard, Dependency tree, Install script review. For SaaS they're all N/A or forced, and the "CVE / advisory must not be Not available for T2/T3" rule doesn't fit a SaaS service.
- **Evidence:** `workflows/remote-integration.md` (sections Identify / Evidence A / Evidence B / Rubric / Verdict Notes, no tier step); compare `workflows/ci-action.md` "Evidence - Part A: Tier Triage" + "Audit coverage tracking", `workflows/agent-extension.md` coverage table. `SKILL.md` Step N → Report "Shape: by final tier". Confidence: High.
- **Implication:** Report shape and confidence rating are left to the auditor's judgment, so results vary run to run. Proposed rows: Scope audit | Vendor identity & verification | Distribution channel | Redirect/callback | Token lifecycle & custody | Webhook verification (if applicable) | ToS & AI data use | Compliance/DPA | Incident & breach search (vendor **and** integration vendor). CVE row → `N/A (hosted service)` unless a self-hosted component exists.

### RI-2 · Scope table (§1) is GitHub-only and partly incorrect — HIGH · plan
- **Wrong:** `read:email` is not a GitHub scope (it's `user:email`, own data). `admin:org` is filed under "Read-only, others' data" but grants full org admin. `admin:*`, `*` (wildcard) and `sudo` are written as literal scope names but are not GitHub OAuth scopes.
- **Missing:** `repo`, which gives full R/W to all private repos. GitHub OAuth apps cannot get read-only repo access, so "Zapier needs repo and org read access" (eval 32) really means write access. Also missing: `workflow`, which can modify Actions workflow files (a CI supply-chain pivot), and `admin:repo_hook` / `admin:org_hook`. GitHub's own docs prefer GitHub Apps (fine-grained, per-repo, short-lived tokens) over OAuth apps. That should be a scoring signal plus a condition ("prefer the vendor's GitHub App variant").
- **Missing providers:** Google classifies scopes as non-sensitive, sensitive or restricted. Restricted scopes such as `gmail.readonly` and full `drive` require a CASA third-party security assessment, re-done every 12 months, for apps that reach data through servers. That's a free, verifiable trust signal; eval 25 uses exactly these scopes. Microsoft Graph: delegated vs application permissions, `*.All` application permissions, admin consent. Slack: bot vs user tokens, `admin.*` scopes.
- **Evidence:** `references/criteria/remote-integration.md` §1; GitHub "Scopes for OAuth apps" + "About GitHub Apps and OAuth apps"; Google "Restricted scope verification". Confidence: High (GitHub/Google), Medium (exact per-provider tiering to adopt).

### RI-3 · Threat model predates the 2025–26 SaaS OAuth supply-chain wave — HIGH · plan
- **Pattern:** Attackers steal standing OAuth/refresh tokens held by a third-party *integration vendor*, then bulk-query the customer's platform. The platform itself isn't vulnerable.
  - Salesloft Drift: tokens abused 2025-08-08..18; Salesforce + some Google Workspace; secrets mined from case records (Cloudflare reported 104 API tokens stolen).
  - Gainsight: Salesforce revoked all Gainsight app tokens around 2025-11-19/20; Zendesk/HubSpot connectors pulled.
  - Klue: disclosed 2026-06-12. Entry point was reportedly a dormant prototype credential that was never deactivated. Victim count is disputed (12 / 195 / 700+).
- **Parallel path:** ShinyHunters/UNC6040 vishing. Callers posing as IT walk an employee through the OAuth **device-code** flow to authorize a fake "Data Loader" connected app. Microsoft (2026-07) maps three paths: vishing to a malicious connected app, tokens stolen from vendors, and misconfigured guest access.
- **Gaps in the workflow:**
  - §4.5 checks the *service's* breach history, but not the integration vendor's custody of your tokens: storage, encryption, IP allowlisting, rotation, dormant-credential hygiene.
  - Distribution check covers email/chat links but not phone/IT-support solicitation or device-code prompts.
  - Suggested conditions omit the controls every advisory now lists: admin-approval-only consent, connected-app allowlist/inventory, alert on bulk export/new authorizations, token IP restriction, revocation runbook, periodic grant review.
- **Evidence:** Gainsight/Salesforce coverage (CSO Online, BleepingComputer); Drift analyses (WTW, NHIMG); Klue coverage (Field Effect, CSA research note 2026-07-16 — fetch blocked, secondary summary only); Varonis UNC6040; The Hacker News 2026-07 (Microsoft report). Confidence: High (pattern), Medium (per-incident numbers).

### RI-4 · OAuth protocol hygiene not anchored to RFC 9700 — MEDIUM · plan
- **Finding:** RFC 9700 (BCP 240, Jan 2025) is the normative OAuth security baseline. OAuth 2.1 is still a draft (`draft-ietf-oauth-v2-1-15`, Mar 2026). The workflow has no check for:
  - implicit grant (`response_type=token`)
  - ROPC / "give us your password"
  - PKCE
  - refresh-token rotation or sender-constraint (DPoP RFC 9449 / mTLS)
  - exact redirect URI matching
- **Overbroad check:** Evidence A §4 treats "localhost, custom scheme" callbacks as suspicious. RFC 8252 sanctions both for native apps, so the check needs a native-vs-web distinction.
- **Evidence:** datatracker draft-ietf-oauth-v2-1; RFC 9700; OWASP OAuth2 cheat sheet. Confidence: High (RFC 9700 published), Medium (whether -16 is the live draft).

### RI-5 · API keys and service-account keys unscored — MEDIUM · plan
- **Finding:** Identify lists static API keys and service-account JSON, but §1 scores OAuth scopes only. There's no row for:
  - key scoping (restricted vs full keys)
  - expiry
  - IP/referrer restriction
  - per-integration key vs shared account key
- **Service-account keys:** Google enforces `constraints/iam.managed.disableServiceAccountKeyCreation` by default for orgs created on/after 2024-05-03. A vendor that requires a downloadable SA JSON key therefore deviates from Google's secure default, which is a flag. Better alternatives: workload identity federation, the vendor's GitHub App, fine-grained PATs.
- **Evidence:** Google "Manage security baseline constraints". Confidence: High.

### RI-6 · Webhook verification norms thin — MEDIUM · plan
- **Finding:** §4.6 and Evidence B §9 only mention "HMAC, shared secret". Missing:
  - timestamp + replay window (typically ~5 min)
  - constant-time comparison
  - secret rotation with dual signatures
  - asymmetric option: Standard Webhooks spec (`webhook-id` / `webhook-timestamp` / `webhook-signature`, `v1` HMAC-SHA256, `v1a` ed25519; steering includes Zapier, Twilio, Svix, Kong)
  - idempotency via the message id
- **Also missing:** a webhook URL is often itself a bearer credential (Slack incoming webhooks `hooks.slack.com/*`), so its leak/rotation story matters. The Identify table also conflates inbound (vendor posts to you) with outbound (you post to vendor URL).
- **Evidence:** Standard Webhooks library docs; spec governance. Confidence: Medium (adoption breadth unverified).

### RI-7 · AI connectors and AI data-sharing terms under-specified — MEDIUM · plan
- **Finding:** §3 covers only "AI/ML training opt-out". Missing:
  - **AI sub-processors:** does the integration forward your data to an LLM provider? Retention there? Zero-data-retention?
  - **Platform API terms that restrict AI use:** Slack API ToS "Data Usage" (effective ~2025-05-29) bars bulk export, persistent copies/indexes and LLM use of API-accessed data. A third-party "AI over your Slack" app may breach platform terms, which is a continuity and compliance risk.
  - **Connector drift:** PromptArmor tracked 2,517 Claude/ChatGPT connectors mid-May→June 2026. 931 changed capability, permissions or config. 86 requested new OAuth scopes, and 283 began injecting instructions into model context. Example: Dropbox went from 8 to 24 tools, including destructive ones. A one-time approval goes stale.
- **Re-audit trigger is package-shaped:** the shared Recommendation text says "re-audit on major version bump or maintainer change". For remote-integration it should be: scope change | new tools/capabilities | vendor acquisition/ownership change | ToS/sub-processor change.
- **Evidence:** Hunton (2025-08-05) on Slack API terms; letsdatascience/threatcluster coverage of PromptArmor (secondary). Confidence: Medium.

### RI-8 · No routing for hosted MCP servers / AI-assistant connectors — MEDIUM · plan (routing; coordinate with agent-extension review)
- **Finding:** "Add connector" to Claude/ChatGPT (remote MCP over HTTP + OAuth, no local code) fires both Type 8a signals (MCP) and Type 9 signals (OAuth, "Connect to", no local install). `references/classifier.md` Routing Overrides has no row for it, so the outcome is either a misroute or `generic`. `workflows/agent-extension.md` handles remote HTTP/SSE as a transport risk but not the OAuth grant or vendor-data posture.
- **Verifiable signals from the MCP authorization spec** (2026-07-28 revision per secondary sources):
  - Client ID Metadata Documents preferred; Dynamic Client Registration deprecated
  - RFC 9728 protected-resource metadata required
  - RFC 8707 `resource` audience binding
- **Fix:** Add a routing override (likely remote-integration with an 8a capability sub-step, or vice versa) plus a worked example.
- **Evidence:** classifier.md Routing Overrides table; agent-extension.md transport rows. MCP spec pages were not fetchable (DNS), so spec details rest on WorkOS/SSOJet summaries. Confidence: High (gap), Low-Medium (spec detail).

### RI-9 · Stale names; marketplace verification signals missing — LOW · fold into plan A
- "Slack App Directory" is now **Slack Marketplace** (renamed 2024-09-16). Affects the workflow Identify table and the eval 24 prompt/assertion (harmless for `contains_concept`).
- Signals missing from §4.3:
  - Microsoft Entra verified publisher + user-consent policy (Microsoft-managed default for new tenants; recommended: verified publishers + low-impact permissions only)
  - Google "unverified app" screen + CASA Letter of Assessment
  - Salesforce AppExchange security review
- Confidence: High.

### RI-10 · Compliance row partly outdated — LOW · fold into plan A
- §2 marks "US-only processing" as negative for GDPR. With EU-US Data Privacy Framework certification (adequacy 2023; Latombe challenge dismissed by the EU General Court, Sept 2025) or SCCs, US processing can be lawful. The signal should be "transfer mechanism stated (DPF/SCCs)", not location.
- Optional: ISO/IEC 42001 as a positive signal for AI vendors.
- Confidence: Medium (from prior knowledge; not re-fetched this pass).

## 6. Analysis — generic + classifier routing

### G-1 · Phase 3 Defensive Minimum is package-shaped — MEDIUM · plan
- **Finding:** Three of the four checks assume a package: CVE lookup by "package name + version", maintenance pulse (last release, maintainer count), and typosquat vs real names. All 3 generic evals are non-package:
  - **eval 33:** web portal + "accepting a browser certificate". This may be a **root CA install**, which grants TLS-interception capability. No workflow covers trust-store changes.
  - **eval 34:** remote script execution via a `bit.ly` shortener.
  - **eval 35:** monorepo `make install`.
- **Missing check:** "what executes / what trust is granted": remote code execution, trust-store or cert changes, privilege elevation, persistence, network exposure. Source-provenance smells (URL shortener, plain HTTP, unsolicited forum/DM origin) are also missing.
- **Evidence:** `workflows/generic.md` Phase 3; `evals/evals.json` ids 33–35. Confidence: High.

### G-2 · Tier and audit confidence undefined after the report split — MEDIUM · plan
- **Finding:** generic never states a tier, so after 2610161910 it's unclear whether the Quick skeleton or the full template applies. It also tells the auditor to mark rows `Skipped (generic fallback)`, but `SKILL.md`'s confidence rules only recognise `Skipped (Tier N)` / `N/A` as valid skips. The rating is therefore indeterminate (High? Low?).
- **Fix:** Pin the shape (suggest Quick skeleton plus the low-confidence stamp, or Tier 2 when Phase 3 flags fire). State how fallback skips count, and cap confidence (suggest ≤ Moderate).
- Confidence: High.

### G-3 · Windows pipe-to-shell signals absent; eval 34 route questionable — LOW-MEDIUM · plan
- **Finding:** cli-binary signals cover `curl … | sh` / `wget … | bash`. The PowerShell equivalents are missing: `iex (irm …)`, `iwr … | iex`, `Invoke-Expression`, `(New-Object Net.WebClient).DownloadString`. `workflows/cli-binary.md` already has an "Install script (curl-pipe-bash)" rubric (download, read, don't pipe), which fits eval 34 better than generic's Phase 3.
- **Steel-man for generic:** the tool's identity is hidden behind `bit.ly`, so the type truly can't be known. Verdict is REJECTED either way.
- **Recommendation:** Add the PowerShell signals and decide explicitly whether eval 34 expects `cli-binary` (medium) or `generic`. If `generic`, document why in classifier.md (unknown payload behind the shortener).
- Confidence: High (gap), Medium (which route is right).

### G-4 · Re-route after clarification contradicts "no re-classification mid-audit" — LOW · revise
- **Finding:** generic Phase 2 re-routes on user clarification. `references/classifier.md` Edge-Case Discipline ("No re-classification mid-audit") and `SKILL.md` Step 0 ("never re-runs mid-audit") don't name that exception. One-line carve-out needed: a user override during generic Phase 2 is the sole sanctioned re-route.
- Confidence: High.

### G-5 · Low-confidence routing itself still fits — INFO · no action
- high/medium → specific workflow; low → generic; "prefer generic with precise conflict rationale over a confident misroute". All still sound.
- Pressure points are new hybrid categories (RI-8 remote MCP / AI connectors) and missing signals (G-3), not the routing logic. Phase 2's non-interactive branch also works for `claude -p` evals.
- Minor improvement: record the unanswered clarification question in the report so a human can re-route later.

### E-1 · Eval coverage gaps — MEDIUM · plan (with A/B)
- remote-integration has 3 cases, all OAuth-consent shaped (Slack approve, Google phishing reject, Zapier+GitHub conditional). Nothing covers:
  - API key or service-account JSON
  - webhook
  - device-code / vishing consent
  - integration-vendor token-custody risk (Drift pattern)
  - hosted MCP / AI connector
- generic: no case for trust-store/root-CA install (eval 33 hints at it but asserts only routing).

## 7. Evidence Log

| # | Finding | Source | Type | Conf. | Notes |
|---|---|---|---|---|---|
| 1 | No tier triage / coverage table in remote-integration | `workflows/remote-integration.md`; `workflows/ci-action.md`, `workflows/agent-extension.md` | Primary | H | grep tier counts 3 vs 8–31 |
| 2 | Scope table errors | `references/criteria/remote-integration.md` §1; docs.github.com scopes-for-oauth-apps, differences-between-github-apps-and-oauth-apps | Primary + Tertiary | H | |
| 3 | Google restricted scopes → CASA, 12-month reassessment | developers.google.com …/restricted-scope-verification | Tertiary | H | |
| 4 | Drift (Aug 2025), Gainsight (Nov 2025), Klue (Jun 2026) token-custody breaches | CSO Online; BleepingComputer; WTW; Field Effect; CSA note (summary) | Tertiary | M-H | Victim counts disputed |
| 5 | UNC6040 vishing + device-code fake Data Loader; Microsoft 2026-07 three-path model | Varonis; The Hacker News 2026-07; RH-ISAC | Tertiary | M-H | |
| 6 | RFC 9700 BCP; OAuth 2.1 still draft (-15 Mar 2026) | datatracker; ietf.org I-D -15 | Tertiary | H / M | -16 unverified |
| 7 | GCP SA key creation disabled by default (orgs ≥ 2024-05-03) | docs.cloud.google.com manage-baseline-constraints | Tertiary | H | Constraint name `iam.managed.*` |
| 8 | Standard Webhooks headers, v1/v1a, replay window | standardwebhooks library docs (pkg.go.dev, packagist, dlang) | Tertiary | M | |
| 9 | Slack API ToS bars bulk export/LLM use (~2025-05-29) | Hunton 2025-08-05 | Tertiary | M | Primary terms not fetched |
| 10 | Connector drift 931/2,517 | PromptArmor via letsdatascience/threatcluster | Tertiary | M | Secondary coverage |
| 11 | MCP auth: CIMD over DCR, RFC 9728, RFC 8707 | WorkOS, SSOJet; modelcontextprotocol.io (DNS-blocked) | Tertiary | L-M | |
| 12 | Slack App Directory → Slack Marketplace (2024-09-16) | docs.slack.dev changelog | Tertiary | H | |
| 13 | Entra Microsoft-managed consent default for new tenants | lazyadmin; entradiff (Dec 2025) | Tertiary | M | |
| 14 | generic Phase 3 package-shaped; evals 33–35 non-package | `workflows/generic.md`; `evals/evals.json` | Primary | H | |
| 15 | Fallback skip status not in confidence rules | `workflows/generic.md` Phase 3; `SKILL.md` Step N | Primary | H | |
| 16 | No PowerShell pipe-to-shell signal | `references/classifier.md`, `SKILL.md` signal table, `workflows/cli-binary.md` | Primary | H | |
| 17 | Offline eval pass | `run_evals.py validate` ✓ (RI 3, generic 3); unittest 12/12 OK; `prepare --workflow remote-integration,generic` ✓ ids 24,25,32,33,34,35; `grade` 0 graded / 6 skipped (no responses) | Primary | H | Regression status undeterminable without live run |
| 18 | `file_exists` grader uses `rglob` → `.install-audits/` relocation safe for evals 33/35 | `evals/run_evals.py` grade fn | Primary | H | |

## 8. Evaluation Against Criteria

| Criterion | remote-integration | generic | Rationale |
|---|---|---|---|
| Ecosystem currency | Weak | Adequate | RI misses dominant 2025–26 attack pattern, RFC 9700, AI connector drift; generic is ecosystem-light by design |
| Structural parity | Weak | Adequate | RI lacks tier + coverage; generic lacks tier/confidence pinning post-split |
| Correctness | Weak | Strong | RI scope literals wrong; generic claims accurate |
| Routing fit | Adequate | Adequate | Core rule sound; hybrids (remote MCP) + PowerShell signals missing |
| Eval coverage | Weak | Adequate | RI 3 cases all OAuth-consent; generic covers its 3 classic ambiguity shapes |

**Overall:** remote-integration needs a substantive refresh. generic needs a targeted fit pass.

## 9. Challenges and Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Drift-pattern integration approved as APPROVED/CONDITIONAL without custody/revocation conditions | High | High | RI-3 conditions + custody check |
| Scope-table literal mismatch → auditor misclassifies real scopes (e.g. `repo` treated as read) | Medium | Medium-High | RI-2 per-provider mapping |
| Report shape/confidence varies run-to-run for RI and generic | High | Medium | RI-1, G-2 |
| Root-CA / trust-store install audited with package checks → misses TLS interception | Low-Medium | High | G-1 |
| Refresh overfits to Salesforce-ecosystem incidents | Medium | Low | Phrase checks provider-neutral (token custody, consent policy), keep incidents as examples only |
| Rubric bloat (RI file already 173 lines) | Medium | Low | Move per-provider scope maps to criteria addendum; keep workflow procedural |

## 10. Findings Summary

| ID | Severity | Subject | Finding | plan-projex? |
|---|---|---|---|---|
| RI-1 | HIGH | remote-integration | No Tier Triage + no Audit Coverage row set; canonical rows package-shaped | Yes (A) |
| RI-2 | HIGH | remote-integration | Scope table GitHub-only, wrong literals, missing `repo`/`workflow`, no Google/Microsoft/Slack maps | Yes (A) |
| RI-3 | HIGH | remote-integration | Misses integration-vendor token-custody breaches + vishing/device-code consent; conditions lack modern controls | Yes (A) |
| RI-4 | MEDIUM | remote-integration | Not anchored to RFC 9700 (implicit/ROPC/PKCE/refresh rotation); native-app redirect check overbroad | Yes (A) |
| RI-5 | MEDIUM | remote-integration | API keys + SA JSON keys unscored; GCP default disables SA keys | Yes (A) |
| RI-6 | MEDIUM | remote-integration | Webhook verification lacks replay/rotation/asymmetric/URL-as-secret | Yes (A) |
| RI-7 | MEDIUM | remote-integration | AI sub-processors, platform AI-use terms, connector drift; package-shaped re-audit trigger | Yes (A) |
| RI-8 | MEDIUM | classifier | No routing override for hosted MCP / AI connectors | Yes (B; coordinate with agent-extension review) |
| RI-9 | LOW | remote-integration | "Slack App Directory" stale; marketplace verification signals missing | Fold into A |
| RI-10 | LOW | remote-integration | GDPR "US-only = negative" outdated (DPF/SCCs) | Fold into A |
| G-1 | MEDIUM | generic | Phase 3 package-shaped; misses execution/trust-grant check (e.g. root CA) | Yes (B) |
| G-2 | MEDIUM | generic | Tier/report shape + confidence for `Skipped (generic fallback)` undefined post-split | Yes (B) |
| G-3 | LOW-MEDIUM | classifier/evals | PowerShell pipe-to-shell signals absent; eval 34 expected route needs decision | Yes (B) |
| G-4 | LOW | classifier/generic | Phase 2 re-route vs "no re-classification" unexcepted | Fold into B (or revise) |
| G-5 | INFO | classifier | Low-confidence routing logic still fits | No |
| E-1 | MEDIUM | evals | No API-key/webhook/SA/device-code/token-custody/remote-MCP/root-CA cases | Yes (with A/B) |

## 11. Recommendations

**Primary:** file two plan-projex (per STEWARDSHIP checklist steps 5–6).
1. **Plan A — remote-integration rubric refresh:** RI-1..7, RI-9, RI-10 + E-1 remote cases.
   - Add Tier Triage (Part A) and a coverage-tracking table.
   - Rebuild §1 as provider-neutral risk classes plus GitHub/Google/Microsoft/Slack maps.
   - Add a token-custody & consent-path section (§4.7) with Drift/Klue/UNC6040 as examples.
   - Add RFC 9700 hygiene checks, API-key/SA-key rows, webhook norms, and AI data-use/drift rows.
   - Define a remote-integration-specific re-audit trigger.
   - Add ≥3 eval cases: device-code/vishing connected app → REJECTED; vendor requiring a GCP SA JSON key → CONDITIONAL; AI connector with LLM sub-processor + `offline_access` → CONDITIONAL.
2. **Plan B — fallback & routing fit:** G-1..G-4, RI-8, E-1 generic case.
   - Extend Phase 3 with an execution/trust-grant check and provenance smells.
   - Pin generic report shape + confidence cap.
   - Add PowerShell signals and decide eval 34's route.
   - Add the classifier carve-out for Phase 2 re-route.
   - Add a hosted-MCP/AI-connector routing override + worked example, agreed with the agent-extension sibling review.
   - Add a root-CA install eval case.

**Conditional:** if the agent-extension review already claims remote MCP → move RI-8 to that plan and keep only the classifier override row in B. If plan bandwidth is limited → RI-1 + RI-3 + G-2 first (highest verdict/report impact).

**Next steps:** immediate — orchestrator updates STEWARDSHIP inventory (Last Reviewed 2026-10-16; Next Due remote-integration 2027-02-13, generic 2027-04-14) and nav Phase 6 log (steps 7–8). Short-term — Plans A/B. Long-term — once a funded live run is approved, run `prepare → run → grade → summary` for both workflows to close checklist step 4.

## 12. Open Questions

- [ ] Hosted MCP / AI connector: route to remote-integration (OAuth grant is the gate) or agent-extension 8a (tool capability is the risk)? Needs a joint decision with the agent-extension review.
- [ ] eval 34: expected route `cli-binary` (medium) or `generic`?
- [ ] generic report shape: Quick skeleton always, or escalate to the full template when Phase 3 flags fire?
- [ ] Is `draft-ietf-oauth-v2-1-16` (Sep 2026) the live draft? Primary MCP spec 2026-07-28 changelog not verified (DNS blocked).
- [ ] Should eval 33 be re-scoped to assert root-CA/trust-store risk explicitly?

## 13. Appendix

**Methodology:** read both workflows, both criteria files, classifier, shared criteria, and dispatcher `SKILL.md` end-to-end (checklist steps 1–2). Then web research for changes since ~2026-04 (step 3). Then the offline eval pass (step 4: validate, unittest, prepare, grade, summary; workspace in session scratch to avoid colliding with sibling runs).

**Tier rationale:** Standard — moderate stakes (rubric changes are routed through plans), external uncertainty bounded.

**Sources consulted:**
- Standards & specs: datatracker.ietf.org/doc/draft-ietf-oauth-v2-1 | ietf.org I-D draft-ietf-oauth-v2-1-15 | datatracker.ietf.org/doc/rfc9700 | cheatsheetseries.owasp.org OAuth2 cheat sheet | workos.com/blog/what-is-mcp-authorization | ssojet.com/blog/mcp-authorization-spec-2026-07-28-what-changed
- Vendor docs: docs.github.com scopes-for-oauth-apps + differences-between-github-apps-and-oauth-apps | developers.google.com restricted-scope-verification | docs.cloud.google.com manage-baseline-constraints | docs.slack.dev/changelog/2024/09/16/apps | lazyadmin.nl new-secure-by-default-changes | entradiff.merill.net/week/2025-12-08
- Incidents: csoonline.com/article/4094506 | bleepingcomputer.com Gainsight | wtwco.com drift-oauth-breach | fieldeffect.com klue-integration-breach | labs.cloudsecurityalliance.org ShinyHunters research note 2026-07-16 | varonis.com salesforce-vishing-threat-unc6040 | thehackernews.com/2026/07/microsoft-maps-year-long-shinyhunters.html
- Terms & AI connectors: hunton.com Slack API terms | letsdatascience.com PromptArmor connectors | pkg.go.dev std-webhooks-go

**Fetch limits:** CSA, Nudge Security and modelcontextprotocol.io returned DNS errors via the proxy, so claims from them rest on search-result summaries (confidence lowered accordingly).

**Dissenting view (steel-man):**
- "remote-integration is fine — the verdict tree already rejects phishing (eval 25) and conditions broad scopes (eval 32); adding provider maps bloats it."
- Counter: the Drift/Gainsight/Klue victims installed *legitimate, marketplace-listed* integrations from established vendors. Those would score APPROVED/Tier 1 today. The gap is in the APPROVED path, not the REJECTED path.

**Iteration history:**

| Date | Mode | Scope | Summary |
|---|---|---|---|
| 2026-10-16 | Initial | remote-integration + generic (+ classifier routing) | First STEWARDSHIP review pass; 3 HIGH, 8 MEDIUM/LOW-MEDIUM, 3 LOW, 1 INFO; Plans A/B recommended |
