# Remote Integration Workflow — M4.4

> **Status:** Ready
> **Created:** 2026-04-16
> **Author:** Claude (projex planning agent)
> **Source:** Direct request — Phase 4 M4.4 from nav
> **Nav:** 2604070218-install-auditor-subject-typed-redesign-nav.md
> **Related Projex:** 2604160900-agent-extension-workflow-m43-plan.md (closed, structural template), 2604151500-cli-binary-workflow-m42-plan.md (closed), 2604151200-desktop-app-workflow-m41-plan.md (closed)
> **Worktree:** No

---

## Summary

Create the Type 9 subject-specific workflow at `workflows/remote-integration.md` and its criteria addendum at `references/criteria/remote-integration.md`, then wire Type 9 routing and eval coverage. M4.4 closes the final Phase 4 workflow gap: remote integrations (OAuth apps, API key integrations, webhook receivers, service accounts) still fall through to `workflows/generic.md`, which knows nothing about OAuth scope auditing, data residency compliance, terms-of-service risk, vendor breach history, or third-party API trust assessment.

**Scope:** Type 9 remote-integration audits — workflow file, criteria addendum, dispatcher wiring, eval coverage.
**Estimated Changes:** 4 files (2 new, 2 modified), ~500–700 lines.

---

## Objective

### Problem / Gap / Need

Type 9 (remote-integration) is the last subject type routing to `workflows/generic.md`. Remote integrations — OAuth apps (Slack, GitHub, Google Workspace, Notion, Zapier), API key integrations, webhook receivers, service accounts — have a fundamentally different trust boundary than locally-installed software. The user isn't installing code; they're granting a cloud-hosted service access to their data via credential grants. Generic workflow lacks:

- **OAuth scope audit** — principle of least privilege, scope creep detection, overprivileged access patterns
- **Data residency** — where data is processed/stored, GDPR/SOC2 compliance signals, sub-processor chains
- **Terms of service** — data sharing clauses, AI training opt-out, third-party sub-processors, data retention policies
- **Breach history** — HaveIBeenPwned-style vendor lookup, known incidents, security disclosure track record, incident response transparency
- **Third-party API trust** — is the service the named vendor or a proxy? Webhook authenticity, redirect URI validation, token storage practices

### Success Criteria

- [ ] `workflows/remote-integration.md` exists with Identify / Evidence — Part A / Evidence — Part B / Subject Rubric / Subject Verdict Notes sections (~200–300 lines)
- [ ] `references/criteria/remote-integration.md` exists with remote-integration-specific tiering and scoring (~125–160 lines)
- [ ] `SKILL.md` dispatch table row 9 routes to `workflows/remote-integration.md` with Live status
- [ ] `SKILL.md` Reference Files section lists both new files
- [ ] `evals/evals.json` has ids 24 (Tier 1 APPROVED positive) and 25 (Tier 3 REJECTED negative)
- [ ] ids 0–23 unchanged in `evals/evals.json`
- [ ] JSON parses without errors

### Out of Scope

- New helper scripts for OAuth scope enumeration or vendor breach lookup
- Broad rewrites to `references/criteria.md` or `references/registries.md`
- Remote integrations where the primary action is local code install (e.g., SDK packages route to Type 1 registry-package per taxonomy)
- Webhook-only integrations where no credential grant occurs (informational only)
- Phase 4 M4.5 eval gate or Phase 5 work

---

## Context

### Current State

Dispatch table row 9 routes to `workflows/generic.md` (fallback). Eight subject-specific workflows are live (Types 1–8). Type 9 is the last remaining fallback route before Phase 5 can begin. Remote integrations are unique in having no local code artifact — the trust boundary is entirely about credential scope, vendor security posture, and data handling practices.

### Key Files

| File | Role | Change Summary |
|------|------|----------------|
| `workflows/remote-integration.md` | New Type 9 workflow | Create ~200–300 lines, Identify/Evidence/Rubric/Verdict structure |
| `references/criteria/remote-integration.md` | New criteria addendum | Create ~125–160 lines, 5 sections with scoring impact |
| `SKILL.md` | Dispatcher + reference index | Update row 9 + add 2 Reference Files bullets |
| `evals/evals.json` | Eval coverage | Append ids 24 and 25 |

### Dependencies

- **Requires:** M4.1–M4.3 complete (confirmed — all three closed 2026-04-15/16)
- **Blocks:** M4.5 (eval gate), Phase 5 (default-off generic — needs all 9 specific workflows live)

### Constraints

- Workflow must follow Identify / Evidence — Part A / Evidence — Part B / Subject Rubric / Subject Verdict Notes template shape
- Must use `references/criteria/remote-integration.md` for type-specific tiering (more-specific wins over shared rubric)
- No sub-rubrics needed (unlike Type 8's 8a/8b/8c) — remote integrations share a uniform trust model
- Orchestrated execution: opus plans, sonnet executes

### Assumptions

- `workflows/agent-extension.md` is the structural template (most recent workflow)
- `references/criteria/agent-extension.md` is the criteria template (most recent addendum)
- Next available eval ids are 24 and 25 (24 total entries exist, ids 0–23)
- No scripts needed for v1 — web search + vendor documentation inspection

### Impact Analysis

- **Direct:** 4 files (2 new, 2 modified)
- **Adjacent:** `workflows/generic.md` loses its last non-Type-0 route — still used by Type 0 (generic) and low-confidence classifications
- **Downstream:** Phase 5 M5.1 (tighten classifier) unblocked once M4.4 lands; M4.5 eval gate can confirm coverage

---

## Implementation

### Overview

Four steps mirroring M4.1–M4.3 pattern: (1) create criteria addendum, (2) create workflow, (3) update dispatcher, (4) add evals.

### Step 1: Create `references/criteria/remote-integration.md`

**Objective:** Author the remote-integration criteria addendum with 5 domain-specific sections.
**Confidence:** High
**Depends on:** None

**Files:**
- `references/criteria/remote-integration.md` (new)

**Changes:**

Create the addendum file with this structure (~125–160 lines):

```markdown
<!-- Remote-integration criteria addendum. Supplements references/criteria.md
     for Type 9 subjects. When guidance here conflicts with the shared rubric,
     this more-specific addendum wins. Phase 4 / M4.4. -->

# Remote Integration — Criteria Addendum
```

**Section 1 — OAuth Scope & Permission Assessment:**
Table of scope categories with trust signals:

| Scope Category | Low Risk | Elevated Risk | High Risk |
|----------------|----------|---------------|-----------|
| Read-only, own data | `read:user`, `repo:status` | `read:org` | — |
| Read-only, others' data | — | `read:discussion` | `read:email`, `admin:org` |
| Write access | `write:packages` (own) | `write:repo_hook` | `delete:repo`, `admin:*` |
| Full account control | — | — | `*` (wildcard), `sudo` |
| Offline/persistent | — | `offline_access` | `offline_access` + broad scope |

Scoring impact: overprivileged scopes (requesting write when read suffices, wildcard scopes) → raise tier. Principle of least privilege satisfied → lower tier.

**Section 2 — Data Residency & Compliance Signals:**
Assessment criteria table:

| Signal | Positive | Negative |
|--------|----------|----------|
| Published data processing locations | Named regions, SOC2/ISO27001 | "Global" with no specifics |
| GDPR compliance | DPA available, EU data center option | No DPA, US-only processing |
| Sub-processor disclosure | Published list, change notifications | Undisclosed, blanket consent |
| Data retention | Defined policy, deletion API | Indefinite, no deletion path |

Scoring impact: no compliance documentation → raise tier. SOC2 + published DPA → lower tier.

**Section 3 — Terms of Service & Data Sharing:**
Assessment criteria table:

| Clause | Acceptable | Concerning | Disqualifying |
|--------|------------|------------|---------------|
| Data sharing | Only for service delivery | Aggregated analytics shared | Sold to third parties |
| AI/ML training | Explicit opt-out, no training | Opt-out available but buried | Data used for training by default, no opt-out |
| Sub-processors | Named, notified on change | Named, no notification | Unnamed, blanket authority |
| Data portability | Export API, standard formats | Manual export only | No export capability |
| Termination | Data returned/deleted on exit | 30-day retention then delete | Indefinite post-termination retention |

Scoring impact: data sold/AI training with no opt-out → strong REJECTED signal. Transparent terms with opt-outs → neutral.

**Section 4 — Breach History & Security Posture:**
Assessment criteria table:

| Signal | Positive | Negative |
|--------|----------|----------|
| Breach history | No known breaches, or disclosed + remediated promptly | Undisclosed breaches, repeated incidents |
| Security disclosure | Published security policy, bug bounty, responsible disclosure | No security contact, no disclosure policy |
| Incident response | Published post-mortems, timely notification | Delayed notification, vague post-mortems |
| Certifications | SOC2 Type II, ISO 27001, pentest reports | Self-attested only, no third-party audit |
| Vulnerability track record | Prompt patching, CVE responsiveness | Slow patching, known unpatched vulns |

Scoring impact: repeated unremediated breaches → strong REJECTED signal. Clean record + SOC2 Type II → lower tier.

**Section 5 — Tier Thresholds:**

- **Tier 1 — Quick Audit:** Well-known vendor (e.g., Google, GitHub, Slack official apps), minimal scopes, published compliance, no breach history. OAuth app listed in official marketplace with verified publisher.
- **Tier 2 — Standard Audit:** Known vendor with moderate scopes, compliance docs available but require review, clean-ish breach history. Third-party OAuth apps with marketplace listing.
- **Tier 3 — Deep Audit:** Unknown vendor, broad scopes (write/admin), no compliance documentation, breach history or no security posture evidence. Unverified OAuth apps, phishing-distributed "connect" links, proxy services masquerading as the named vendor.

**Rationale:** Five sections parallel the nav's ideation for M4.4 (OAuth scopes, data residency, terms-of-service, breach history, third-party API trust). Structure mirrors `references/criteria/agent-extension.md` (sections + scoring impact + tier thresholds).

**Verification:** File exists, ~125–160 lines, 5 titled sections each with table + scoring impact, Tier Thresholds section with 3 tiers.

**If this fails:** Delete the file; Type 9 continues routing through `workflows/generic.md`.

---

### Step 2: Create `workflows/remote-integration.md`

**Objective:** Author the Type 9 remote-integration workflow following the standard template shape.
**Confidence:** High
**Depends on:** Step 1

**Files:**
- `workflows/remote-integration.md` (new)

**Changes:**

Create the workflow file with this structure (~200–300 lines):

```markdown
<!--
This workflow replaces workflows/generic.md for Type 9 subjects. After
producing findings here, return to SKILL.md Step N for the shared verdict
tree and report shape. The Audit Coverage table and audit-confidence
assertion are owned by the dispatcher — do not duplicate them here.

Phase 4 / M4.4 — ninth subject-specific workflow (fourth Phase 4).
-->

# Remote Integration Workflow (Type 9)
```

**Intro paragraph:** This workflow handles **Type 9: remote-integration** subjects — cloud-hosted services integrated via credential grants (OAuth tokens, API keys, webhook secrets, service accounts). Unlike locally-installed software, the trust boundary is the service's data handling, permission scope, and operational security — no code is installed locally.

After completing all sections, return to `SKILL.md` Step N for shared verdict tree and audit-coverage report shape.

Use `references/criteria/remote-integration.md` for remote-integration-specific tiering and scoring. When it conflicts with the shared rubric, the more specific remote-integration guidance wins.

**## Identify**

**1. Determine integration type and credential mechanism** — table:

| Integration Pattern / Signal | Integration Type | Credential Mechanism |
|------------------------------|-----------------|---------------------|
| "Add to Slack", OAuth consent screen | OAuth app | OAuth 2.0 token |
| "Connect your GitHub account" | OAuth app | OAuth 2.0 token |
| API key in dashboard → paste into config | API key integration | Static API key |
| Webhook URL generation (e.g., Zapier, IFTTT) | Webhook receiver | Webhook secret/URL |
| Service account JSON (e.g., GCP, Firebase) | Service account | Service account credential |
| "Sign in with Google/GitHub/Microsoft" | SSO/federated auth | OAuth 2.0 / OIDC |
| "Connect to <service>" with redirect flow | OAuth app | OAuth 2.0 token |
| Marketplace "Install" button (Slack App Directory, GitHub Marketplace) | Marketplace OAuth app | OAuth 2.0 token |

**2. Extract available metadata** — collect from the integration channel:
- **Service name** — as listed in marketplace/dashboard/documentation
- **Publisher/vendor** — organization behind the service
- **Integration type** — OAuth app | API key | webhook | service account | SSO
- **Requested scopes/permissions** — full list from consent screen or docs
- **Marketplace listing** — if distributed via marketplace (Slack App Directory, GitHub Marketplace, Google Workspace Marketplace, etc.)
- **Version / API version** — if versioned
- **Pricing model** — free, freemium, paid (relevant to sustainability/incentive analysis)

**3. Gather required context:**
- OAuth consent screen or scope documentation
- Vendor's privacy policy and terms of service
- Security/compliance page (SOC2, GDPR, certifications)
- Breach history (web search: `"<vendor>" breach OR incident OR vulnerability`)
- Marketplace reviews/ratings if available

**## Evidence — Part A** (automated/structured checks)

1. **Scope audit** — list all requested scopes/permissions; classify each per criteria addendum §1 (low/elevated/high risk); flag any violating least privilege
2. **Vendor identity verification** — confirm the service is the named vendor (not a proxy or phishing clone); check domain ownership, marketplace verification badge, official documentation links
3. **Marketplace listing review** — if applicable: verified publisher badge, install count, ratings, listing age, developer contact info
4. **Redirect URI / callback validation** — for OAuth: does the redirect URI match the vendor's known domains? Custom scheme or localhost callbacks in production?
5. **Token storage & transmission** — does documentation describe secure token handling? HTTPS-only? Token rotation/expiry?

**## Evidence — Part B** (research-intensive checks)

6. **Data residency & compliance** — per criteria addendum §2: where is data processed/stored, what compliance certifications exist, DPA availability, sub-processor disclosure
7. **Terms of service review** — per criteria addendum §3: data sharing clauses, AI/ML training use, sub-processors, data portability, termination terms
8. **Breach history & security posture** — per criteria addendum §4: search for known breaches, check security disclosure policy, incident response track record, certifications
9. **Third-party API trust assessment** — is this the actual vendor or a third-party wrapper/proxy? Does the service intermediate requests through additional infrastructure? Are webhook payloads authenticated (HMAC signatures)?
10. **Scope necessity analysis** — for each elevated/high-risk scope: is it justified by the integration's stated purpose? Could the same functionality work with narrower scopes?

**## Subject Rubric**

**§4.1 OAuth Scope & Permission Model:**
- What scopes/permissions are requested?
- Does the integration follow principle of least privilege?
- Are there admin/write/delete scopes that aren't justified by functionality?
- Is `offline_access` or equivalent requested? Justified?
- Scoring: per criteria addendum §1

**§4.2 Data Handling & Residency:**
- Where does the vendor process and store data?
- What compliance certifications does the vendor hold?
- Is a DPA available for regulated data?
- Are sub-processors disclosed?
- Scoring: per criteria addendum §2

**§4.3 Vendor Trust & Provenance:**
- Is this the official vendor or a third-party proxy?
- Is the vendor established (age, size, reputation)?
- Marketplace verification status (if applicable)?
- Is the redirect URI / callback owned by the claimed vendor?
- Scoring: established + verified → lower tier; unknown proxy → raise tier

**§4.4 Terms of Service & Data Sharing:**
- Does the vendor share data with third parties?
- Is data used for AI/ML training? Opt-out available?
- What happens to data on account termination?
- Is data export supported?
- Scoring: per criteria addendum §3

**§4.5 Security Posture & Breach History:**
- Any known breaches? Were they disclosed and remediated promptly?
- Security disclosure policy? Bug bounty?
- SOC2 Type II, ISO 27001, or equivalent?
- Token rotation, HTTPS enforcement, secure defaults?
- Scoring: per criteria addendum §4

**§4.6 Integration Hygiene:**
- Does the integration support token expiry/rotation?
- Webhook signature verification available?
- Audit logging of API access provided?
- Rate limiting and abuse protection?
- Scoring: good hygiene → neutral; no expiry + no logging → raise tier

**## Subject Verdict Notes**

**Toward REJECTED:**
- Wildcard or admin scopes with no justification
- Vendor has unacknowledged/unremediated breaches
- Service is a proxy masquerading as the named vendor
- Data sold to third parties or used for AI training with no opt-out
- No compliance documentation for a service handling sensitive data
- Phishing-distributed "Connect" link (not from official marketplace or vendor site)

**Toward CONDITIONAL:**
- Moderate scopes that are justifiable but worth monitoring
- Vendor has breach history but with transparent disclosure and remediation
- Terms allow data sharing for aggregated analytics (not individual data)
- Compliance docs exist but are incomplete (e.g., SOC2 Type I but not Type II)
- Conditions: restrict to minimum required scopes, review on renewal, monitor vendor security posture

**Toward APPROVED:**
- Well-known vendor with verified marketplace listing
- Minimal scopes following principle of least privilege
- Clean breach history or transparent incident response
- Published compliance certifications (SOC2 Type II, ISO 27001)
- Clear terms: no data selling, AI training opt-out, data portability

**Rationale:** Structure mirrors `workflows/agent-extension.md` — Identify (3 subsections) / Evidence Part A (5 checks) / Evidence Part B (5 checks) / Subject Rubric (6 sections) / Subject Verdict Notes (3 directions). Remote-integration-specific: no sub-rubrics needed (uniform trust model unlike Type 8's 8a/8b/8c); emphasis on credential grants, vendor trust, and data handling rather than local code execution.

**Verification:** File exists, ~200–300 lines, standard template sections present, references criteria addendum, no sub-rubric labels.

**If this fails:** Delete the file; Type 9 continues routing through `workflows/generic.md`.

---

### Step 3: Update `SKILL.md`

**Objective:** Route dispatch table row 9 to the new workflow and index new reference files.
**Confidence:** High
**Depends on:** Steps 1–2

**Files:**
- `SKILL.md`

**Changes:**

**3a. Dispatch table row 9 (line 70):**

```markdown
// Before:
| 9 | remote-integration | `workflows/generic.md` | Fallback — specific workflow lands in Phase 4 (M4.4) |

// After:
| 9 | remote-integration | `workflows/remote-integration.md` | Live — Phase 4 (M4.4) |
```

**3b. Reference Files — workflow bullet (insert after `workflows/agent-extension.md` line, which is line 219):**

```markdown
// Before:
- `workflows/agent-extension.md` — Type 8 agent-extension workflow (Phase 4, M4.3)
- `references/criteria.md` — Shared tier-aware scoring rubric

// After:
- `workflows/agent-extension.md` — Type 8 agent-extension workflow (Phase 4, M4.3)
- `workflows/remote-integration.md` — Type 9 remote-integration workflow (Phase 4, M4.4)
- `references/criteria.md` — Shared tier-aware scoring rubric
```

**3c. Reference Files — addendum bullet (insert after `references/criteria/agent-extension.md` line, which is line 228):**

```markdown
// Before:
- `references/criteria/agent-extension.md` — Agent-extension criteria addendum (distribution/discovery channel trust, capability scope classification, transport & isolation, prompt/behavioral risk, tier thresholds)
- `references/licenses.md` — License compatibility matrix

// After:
- `references/criteria/agent-extension.md` — Agent-extension criteria addendum (distribution/discovery channel trust, capability scope classification, transport & isolation, prompt/behavioral risk, tier thresholds)
- `references/criteria/remote-integration.md` — Remote-integration criteria addendum (OAuth scope & permission assessment, data residency & compliance, terms of service & data sharing, breach history & security posture, tier thresholds)
- `references/licenses.md` — License compatibility matrix
```

**Rationale:** Dispatcher routing and reference-file index are the only `SKILL.md` edits needed. All subject logic lives in the new workflow and addendum.

**Verification:** `rg -n "remote-integration" SKILL.md` shows: signal table row 9 (already present), dispatch table row 9 → live route, workflow reference bullet, addendum reference bullet. Total: 4+ hits with the new additions.

**If this fails:** Revert row and remove bullets; Type 9 continues routing through `workflows/generic.md`.

---

### Step 4: Update `evals/evals.json`

**Objective:** Add Type 9 eval coverage — one positive Tier 1, one negative Tier 3.
**Confidence:** High
**Depends on:** Steps 1–3

**Files:**
- `evals/evals.json`

**Changes:**

Append two entries to the `evals` array (after id 23):

```json
    {
      "id": 24,
      "prompt": "Our team wants to add the official Slack app to our workspace for notifications. The admin would install it from the Slack App Directory at https://slack.com/apps — it requests these OAuth scopes: channels:read, chat:write, users:read. Is this integration safe?",
      "expected_output": "Tier 1 quick audit. Routes to remote-integration workflow. Should recognize the official Slack app installed via Slack App Directory (verified marketplace) as a first-party integration from Slack (Salesforce). Scopes are minimal and appropriate: channels:read (list channels), chat:write (post messages), users:read (list users) — all read-only or write-only-to-own-messages, no admin scopes, no offline_access. Slack is a well-known vendor with SOC2 Type II, ISO 27001, published DPA, and transparent data practices. No disqualifying breach history. Verdict should be APPROVED.",
      "files": [],
      "assertions": [
        {"text": "Subject type is remote-integration", "type": "contains_concept"},
        {"text": "Report identifies Slack as an established or well-known vendor", "type": "contains_concept"},
        {"text": "Report notes Slack App Directory as official marketplace", "type": "contains_concept"},
        {"text": "Report discusses OAuth scopes and least privilege", "type": "contains_concept"},
        {"text": "Report mentions compliance certifications or SOC2", "type": "contains_concept"},
        {"text": "Verdict is APPROVED", "type": "exact_match"},
        {"text": "Audit confidence", "type": "contains_concept"}
      ]
    },
    {
      "id": 25,
      "prompt": "I got an email saying I should connect this productivity app to my Google Workspace — it's at https://superproductivity-ai.xyz/connect and asks for these Google OAuth scopes: https://www.googleapis.com/auth/gmail.readonly, https://www.googleapis.com/auth/drive, https://www.googleapis.com/auth/admin.directory.user, https://www.googleapis.com/auth/calendar. The company is 'SuperProductivity AI' and I can't find much about them online. Should I authorize this?",
      "expected_output": "Tier 3 deep audit. Routes to remote-integration workflow. Should flag multiple critical risks: unknown vendor ('SuperProductivity AI' with no discoverable online presence), suspicious domain (superproductivity-ai.xyz — non-standard TLD, not an established vendor domain), email-distributed authorization link (potential phishing vector — not from Google Workspace Marketplace), grossly overprivileged scopes (full Gmail read, full Drive access, admin directory user management, full calendar access — requests admin scope without justification), no compliance documentation discoverable, no marketplace verification. The combination of email distribution + unknown vendor + broad scopes including admin access is a strong phishing/credential-harvesting signal. Verdict should be REJECTED.",
      "files": [],
      "assertions": [
        {"text": "Subject type is remote-integration", "type": "contains_concept"},
        {"text": "Report flags unknown vendor or unverifiable publisher", "type": "contains_concept"},
        {"text": "Report flags overprivileged or excessive OAuth scopes", "type": "contains_concept"},
        {"text": "Report flags email distribution or phishing risk", "type": "contains_concept"},
        {"text": "Report flags admin scope or admin.directory access", "type": "contains_concept"},
        {"text": "Verdict is REJECTED", "type": "exact_match"},
        {"text": "Audit confidence", "type": "contains_concept"}
      ]
    }
```

**Rationale:** Two cases exercise the Type 9 workflow's boundary conditions: id 24 tests a well-known first-party Slack integration with minimal scopes via official marketplace (Tier 1 positive path), and id 25 tests an unknown vendor with overprivileged Google OAuth scopes distributed via email phishing link (Tier 3 negative path). Both exercise the core remote-integration checks (scopes, vendor trust, marketplace, compliance, distribution channel).

**Verification:**
- `node -e "const d=JSON.parse(require('fs').readFileSync('evals/evals.json','utf8')); console.log(d.evals.length);"` → 26
- `node -e "const d=JSON.parse(require('fs').readFileSync('evals/evals.json','utf8')); console.log(d.evals[24].id, d.evals[25].id);"` → 24 25
- JSON parses without errors
- ids 0–23 are unchanged

**If this fails:** Remove the two new entries; eval coverage remains at 24. Type 9 workflow still functions but lacks eval validation.

---

## Verification Plan

### Automated Checks

- [ ] `node -e "JSON.parse(require('fs').readFileSync('evals/evals.json','utf8'))"` → no parse error
- [ ] `node -e "const d=JSON.parse(require('fs').readFileSync('evals/evals.json','utf8')); console.log(d.evals.length);"` → 26

### Manual Verification

- [ ] Workflow follows Identify / Evidence — Part A / Evidence — Part B / Subject Rubric / Subject Verdict Notes structure
- [ ] Workflow references `references/criteria/remote-integration.md` for type-specific tiering
- [ ] Criteria addendum covers 5 sections (OAuth scope, data residency, ToS, breach history, tier thresholds)
- [ ] Dispatch table row 9 routes to `workflows/remote-integration.md` with "Live — Phase 4 (M4.4)"
- [ ] Eval id 24 (Slack official OAuth app) tests the positive Tier 1 path
- [ ] Eval id 25 (phishing-distributed unknown vendor with broad Google scopes) tests the negative Tier 3 path
- [ ] ids 0–23 are unchanged in `evals/evals.json`

### Acceptance Criteria Validation

| Criterion | How to Verify | Expected Result |
|-----------|---------------|-----------------|
| Workflow exists with template | `grep "^## " workflows/remote-integration.md` | Identify, Evidence — Part A, Evidence — Part B, Subject Rubric, Subject Verdict Notes |
| Criteria addendum exists | File read; section scan | 5 sections with tables + scoring impact |
| Dispatch row 9 | `grep "remote-integration.*remote-integration.md" SKILL.md` | Row 9 routes to `workflows/remote-integration.md` |
| Reference Files bullets | `grep "remote-integration" SKILL.md` | 4+ total hits |
| Eval coverage | JSON parse + id count | 26 total entries, ids 0–25 |
| Eval id 24 (positive) | Read eval prompt + assertions | Slack official app, APPROVED expected |
| Eval id 25 (negative) | Read eval prompt + assertions | Unknown phishing vendor, REJECTED expected |
| No regressions | Diff ids 0–23 against pre-change | Zero diff |

---

## Rollback Plan

Per-step rollback is noted in each step. If the overall implementation must be abandoned:

1. Delete `workflows/remote-integration.md`
2. Delete `references/criteria/remote-integration.md`
3. Revert `SKILL.md` edits (dispatch table row 9, reference file bullets)
4. Remove eval ids 24 and 25 from `evals/evals.json`
5. All changes are in 4 files; `git checkout -- <files>` restores clean state

---

## Notes

### Risks

- **Scope calibration:** OAuth scope tables may need refinement when tested against real-world integrations with non-standard scope naming (e.g., Notion uses capability names, not OAuth standard scopes). **Mitigation:** criteria addendum uses categories (read-own, write-own, admin) rather than specific scope strings; workflow instructs auditor to classify per-integration.
- **Vendor breach data staleness:** Breach history checks depend on web search results which may be incomplete. **Mitigation:** workflow instructs auditor to search multiple sources and note coverage limitations in the audit confidence assertion.
- **No-code boundary:** Some remote integrations blur into local SDK installs (e.g., Firebase SDK = Type 1, Firebase console service account = Type 9). **Mitigation:** innermost-boundary classifier rule in taxonomy def handles this; out-of-scope for this workflow.

### Open Questions

(None — all resolved via prior M4.1–M4.3 pattern and nav ideation.)
