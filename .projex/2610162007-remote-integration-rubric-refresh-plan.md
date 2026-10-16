# Remote-Integration Rubric Refresh

> **Status:** Ready
> **Author:** Claude (Opus)
> **Parent:** 2610161927-remote-integration-generic-stewardship-review-eval.md
> **Source:** 2610161927-remote-integration-generic-stewardship-review-eval.md (Plan A: RI-1..RI-7, RI-9, RI-10) | shared contract 2610161941-shared-version-integrity-floor-plan.md (§4.6 plug-ins, coverage-row contract) | human decision C6 (via orchestrator)
> **Related Projex:** 2610161941-shared-version-integrity-floor-plan.md (contract this builds on; landed on base at `20843cc`) | 2610162004-generic-fallback-and-classifier-refresh-plan.md (sibling: RI-8 routing, generic) | 2610162007-agent-extension-rubric-refresh-plan.md (sibling: remote MCP capability side) | 2604161000-remote-integration-workflow-m44-walkthrough.md (origin of both files) | 2604070218-install-auditor-subject-typed-redesign-nav.md
> **Worktree:** Yes

---

## Summary

Type 9 rubric predates the 2025–26 SaaS OAuth supply-chain wave. Attackers stole **standing tokens held by integration vendors** (Salesloft Drift, Aug 2025) or vished employees into approving malicious connected apps (UNC6040). The platforms themselves were not vulnerable. Legitimate, marketplace-listed integrations from established vendors score APPROVED/Tier 1 today, so the gap sits in the APPROVED path.

The rubric is also structurally behind its siblings:
- no Tier Triage step and no coverage row set (RI-1)
- the scope table is GitHub-only, with wrong literals (`read:email`, `delete:repo`, `sudo`, `admin:*`) and a misfiled `admin:org` (RI-2)
- no RFC 9700 anchoring (RI-4), no API-key or service-account scoring (RI-5), and thin webhook norms (RI-6)
- AI data use and connector drift are missing (RI-7), names are stale (RI-9), and the GDPR row is outdated (RI-10)
- its "§4.6 Integration Hygiene" heading now collides with shared `references/criteria.md` §4.6

The plan does a full rewrite of both Type 9 files, built on the shared floor that just landed:
- **Addendum:** provider-neutral scope classes plus GitHub/Google/Microsoft/Slack maps; ratings mapped to verdict-tree flags
- **New addendum sections:** non-OAuth credentials, OAuth flow hygiene, token custody & consent path, webhooks, AI-use rows, the §4.6 plug-in, and a §4.3 CVE note
- **Workflow:** Tier Triage, numbered checks, a coverage table that keeps every canonical Required row, a rubric renumbered to the shared 4.1–4.6, and updated verdict notes

**Scope:** `workflows/remote-integration.md` | `references/criteria/remote-integration.md`. Nothing else.
**Estimated Changes:** 2 files, both full-content replacements. Workflow 10,323 → 13,774 B; addendum 5,419 → 19,860 B. Simulated against base `20843cc`, consistency script `OK`.

---

## Objective

### Problem / Gap / Need

| ID | Gap (verified at planning against base `20843cc`) | Fix (section in new files) |
|---|---|---|
| RI-1 | Workflow has no tier step, though addendum §5 tiers exist and are never invoked. No coverage rows, so auditors fall back to package-shaped canonical rows. | Workflow "Evidence — Part A: Tier Triage". "Audit coverage tracking" table carries all 11 canonical Required rows (labels unchanged) with Type 9 `N/A (<reason>)` values, plus 7 subject rows. Satisfies the contract in `references/criteria.md` ("Workflow coverage tables … never drop a Required row") |
| RI-2 | Addendum §1 table: `read:email` (no such scope; it is `user:email`), `delete:repo` (it is `delete_repo`), `admin:*` / `*` / `sudo` written as scope literals, `admin:org` filed as "read-only", `write:packages` rated Low. `repo` and `workflow` missing. No Google/Microsoft/Slack mapping. | Addendum §1: Low / Elevated / High classes, a standing-grant modifier, a rating table mapped to CRITICAL/HIGH/MEDIUM, and provider maps (examples). GitHub App and fine-grained PAT count as the "narrower option" |
| RI-3 | No integration-vendor token-custody check. Consent-path check covers email/chat only. Conditions lack modern org controls. | Addendum §6: custody table (first-party vs third-party standing grant; incident resolved / unresolved), consent-path table (phone/IT-support, someone else's device code, branding mismatch), org-control conditions |
| RI-4 | No RFC 9700 baseline. Localhost / custom-scheme callbacks are treated as suspicious, contrary to RFC 8252. | Addendum §3: flow-hygiene table (implicit, password capture, device code origin, loopback/private-use scheme sanctioned, DPoP/rotation, PKCE note). OAuth 2.1 named as a draft |
| RI-5 | API keys and SA keys are listed in Identify but unscored. | Addendum §2: key table plus SA-key rule (GCP secure-by-default orgs ≥ 2024-05-03) |
| RI-6 | Webhooks: only "HMAC, shared secret". Inbound and outbound are conflated. | Addendum §9: direction, signature / replay / constant-time / rotation, Standard Webhooks, URL-as-secret |
| RI-7 | Only "AI/ML training opt-out". Re-audit trigger is package-shaped. | Addendum §5 AI sub-processor row, platform API terms, AI-connector tool baseline. `## Version & Update Integrity (§4.6)` plug-in: V5 subject triggers + update controls; V3 re-consent diff |
| RI-9 | "Slack App Directory" is stale; Entra / Google / AppExchange verification signals are missing. | Addendum §7 verification table; workflow Identify table uses "Slack Marketplace" |
| RI-10 | "US-only processing" listed as a GDPR negative. | Addendum §4: "transfer mechanism stated (adequacy e.g. EU-US DPF, or SCCs)"; ISO/IEC 42001 optional positive |
| (new) | Workflow `### §4.6 Integration Hygiene` collides with shared `references/criteria.md` §4.6 Version & Update Integrity. Rubric numbering doesn't match shared 4.1–4.5. | Workflow Subject Rubric renumbered 4.1 Provenance … 4.6 Version & Update Integrity, matching the shared file and siblings (`workflows/ci-action.md`). Hygiene content moves to addendum §2/§3/§9 |
| C6 | Shared §4.3 `**Addendum:**` line asks each addendum for its own-code boundary and scan sources. | Addendum §8 "CVE row (§4.3 plug-in)": hosted → `N/A (hosted service, no versioned artifact)`, Blocking CVE node does not apply. Self-hosted components are audited as their own type. Verdict classes untouched |

### Success Criteria

- [ ] `references/criteria/remote-integration.md` equals the Step 1 content byte-for-byte: 19,860 B, sha256 `2206909f4a74566be652e2234ce9b3b0c002e9ddd1a045c7aed96236f99af04a`. Any Assumption-driven edit is logged with its new hash.
- [ ] `workflows/remote-integration.md` equals the Step 2 content: 13,774 B, sha256 `71cda01a5f801bc395dea7eadba21fd1934e9fe8686d3e22855c68591034a9f8` (same rule).
- [ ] The consistency script (Verification Plan) prints `OK`. It checks:
  - size budgets: workflow ≤ 14,500 B, addendum ≤ 20,500 B
  - every `addendum §N` and in-addendum `§N` resolves to a `## §N —` heading (§1–§10)
  - one `## Version & Update Integrity (§4.6)` heading with exactly one bullet each for `V1`–`V5`
  - every `§4.6 V<n>` resolves to a `### V<n>` heading in `references/criteria.md`
  - every canonical Required row label from `references/criteria.md` "Rows by tier" appears as `| <label> |` in the workflow
  - stale literals are gone, and no projex filename or `.projex` appears in the shipped files
- [ ] `python3 evals/run_evals.py validate` passes. `python3 -m unittest discover -s evals -p "test_*.py"` passes with the Preflight test count.
- [ ] Paper traces P1–P10 (Verification Plan) reach the stated verdict/tier, citing a section per hop.
- [ ] `git diff --stat <base>..HEAD` lists exactly the 2 files. `evals/`, `SKILL.md`, `references/criteria.md` and `references/classifier.md` are untouched.

### Out of Scope

- **RI-8:** routing hosted MCP / AI-assistant connectors → sibling 2610162004-generic-fallback-and-classifier-refresh-plan.md (classifier) and 2610162007-agent-extension-rubric-refresh-plan.md. This plan only makes Type 9 *ready* (an Identify row, AI rows in §5, the V3/V5 tool baseline). See Notes → Hand-off.
- **E-1:** eval cases and the eval 24 "App Directory" wording → later eval-refresh plan (Hand-off). No `evals/` edits.
- `SKILL.md`, `references/criteria.md`, `references/report-template.md`, `references/classifier.md`, `workflows/generic.md` (shared or sibling-owned).
- `STEWARDSHIP.md` review dates (orchestrator).
- Live `run_evals.py run`. The human decided on one paid run, after all refreshes.
- Exhaustive per-provider scope catalogs. The maps are examples; the class definitions carry the rule.

---

## Context

### Current State

- `workflows/remote-integration.md` (173 lines, 10,323 B, blob `5e062e5b`):
  - Identify (8-row type table, metadata, context); Evidence A (checks 1–5); Evidence B (checks 6–10)
  - Subject Rubric `§4.1 OAuth Scope` … `§4.6 Integration Hygiene`; Verdict Notes
  - No tier step, no coverage table. Long lines.
- `references/criteria/remote-integration.md` (91 lines, 5,419 B, blob `ef950a95`): §1 scope table (GitHub-only, errors above), §2 residency, §3 ToS, §4 breach, §5 tier thresholds. Ratings are "raise/lower tier" signals, not flags.
- Shared floor on base (`20843cc`):
  - `references/criteria.md` has §4.6 V1–V5 and the hosted-service rule ("V1–V3 → `N/A (hosted service)`; V4 and V5 apply")
  - Row `Version integrity (§4.6)` is Required at all tiers; the workflow-coverage-table contract is in place
  - §4.3 Blocking CVE table, with an `**Addendum:**` line forbidding changes to the verdict classes
  - `SKILL.md` Precedence names §4.6 a floor; Tree term **Blocking CVE**; CRITICAL flag = Red Flag **or** a CRITICAL rating from the addendum and `Toward REJECTED` notes
- Evals (unchanged by this plan):
  - 24: official Slack app, `channels:read chat:write users:read`, exact APPROVED, expected "Tier 1"
  - 25: email-delivered unknown Google app with `gmail.readonly`, `drive`, `admin.directory.user`, `calendar`, exact REJECTED
  - 32: Zapier + GitHub org "repo and org read", CONDITIONAL, asserts `## Audit Coverage`
- Sibling conventions: `workflows/ci-action.md` "Evidence - Part A: Tier Triage" with Tier 1/2/3 lists and "Audit coverage tracking"; `workflows/desktop-app.md` and `workflows/agent-extension.md` use `| Check | Tier 1 | Tier 2 | Tier 3 |` tables. Addenda and most workflows wrap prose at ~78 columns.

### Key Files

| File | Role | Change Summary |
|------|------|----------------|
| `references/criteria/remote-integration.md` | Type 9 scoring addendum | Full rewrite: §1–§10 + `## Version & Update Integrity (§4.6)` plug-in |
| `workflows/remote-integration.md` | Type 9 procedure | Full rewrite: Identify, Tier Triage, 11 checks + coverage table, rubric 4.1–4.6, verdict notes |

### Dependencies

- **Requires:** base `claude/youthful-dijkstra-5ov1kt` at or after `20843cc` (shared floor landed). Preflight verifies.
- **Concurrent (no file overlap expected):** all sibling refresh plans (2610162003…2610162007). Two siblings may want text in these files: generic/classifier (RI-8 routing) and agent-extension (remote MCP). Either one must hand off rather than edit (Notes). If either has edited these two files on base by execution time, Preflight's blob check fails → stop and merge by hand.
- **Blocks:** eval-refresh plan (E-1 cases assert behavior defined here).

### Constraints

- Do not change shared verdict classes (§4.3 Addendum line). Do not loosen §4.6 (Precedence).
- Keep the parsed strings out of these files. They live in `SKILL.md`; this plan names no new parsed string.
- Coverage table: canonical labels verbatim; tier words from the canonical vocabulary (`Required` | `Tier-skip` | `Tier-skip (brief)` | `If applicable` | `Optional`).
- Shipped text: no projex filenames; no secondary-source statistics (victim counts, connector-drift numbers); incidents named only as examples.
- Prose wraps at ~78 columns; tables stay one line per row.

### Assumptions

Facts the shipped text relies on, with how they were checked at planning (2026-10-16, web search summaries of primary pages). Executor: re-check each marked **[verify]** item if the network allows. If one turns out false, edit only the cited sentence and log it.

- **A1 [verify]:** GitHub OAuth scopes:
  - `user:email` is read-only email; `delete_repo` uses an underscore
  - `repo` grants full access to private repos; `admin:org` is full org management; `workflow` updates Actions workflow files
  - No read-only private-repo scope exists for OAuth apps
  - Planning source: docs.github.com "Scopes for OAuth apps" (GHES versions via search; github.com page not fetched). `sudo` and `admin:*` are not listed scopes (prior knowledge).
- **A2:** Google restricted scopes need an annual (12-month) third-party security assessment for apps reaching data through servers. Source: developers.google.com restricted-scope-verification + Google Cloud help 13463816. **[verify]** that `gmail.readonly` and full `drive` are restricted (prior knowledge; the search summary named Gmail read scopes only).
- **A3:** Google Cloud secure-by-default policies apply to orgs created on/after 2024-05-03 and include `iam.managed.disableServiceAccountKeyCreation`. Source: docs.cloud.google.com "Manage security baseline constraints". The shipped text doesn't name the constraint.
- **A4:** RFC 9700 = BCP 240, Jan 2025, deprecates implicit and ROPC (datatracker). OAuth 2.1 is still a draft (review eval; `-16` unverified, so the shipped text says only "Internet-Draft"). RFC 8252 (native-app loopback / private-use schemes), RFC 8628 (device grant) and RFC 9449 (DPoP) are prior knowledge, stable RFCs.
- **A5:** Standard Webhooks: headers `webhook-id` / `webhook-timestamp` / `webhook-signature`, `v1` HMAC-SHA256, `v1a` Ed25519, multiple signatures for rotation, ~5 min tolerance typical. Source: library docs, secondary (pkg.go.dev, code.dlang.org). The official spec repo was not read.
- **A6:** Slack App Directory → Slack Marketplace (docs.slack.dev changelog 2024-09-16). Slack API terms (effective ~2025-05-29) bar bulk export, persistent copies and indexes, and LLM use. Source: Hunton / Cloud Wars, secondary; the shipped text hedges ("check the platform's current text").
- **A7:** Salesloft Drift: stolen OAuth tokens used 2025-08-08..18 (GTIG via Security Affairs / TechTarget). UNC6040: callers posing as IT support get a modified Data Loader approved via a connection code (GTIG blog / The Hacker News 2025-06). Gainsight and Klue are deliberately **not** named (Klue unverified; numbers disputed).
- **A8:** Entra user-consent option "verified publishers … low impact permissions" and the admin consent workflow (learn.microsoft.com). Google Workspace app access control, Slack app approval, GitHub org OAuth app access restrictions and Salesforce AppExchange security review are prior knowledge, named as "e.g." only. **[verify]** if possible.
- **A9:** EU-US DPF adequacy (2023) is prior knowledge; shipped text names it only as an example transfer mechanism.
- **A10:** Slack scope names `chat:write.customize`, `users:read.email`, `admin.*`, `im:history`, `mpim:history` and Graph names `Mail.Read`, `Files.ReadWrite.All`, `Directory.ReadWrite.All`, `User.Read` are prior knowledge **[verify]**. A wrong example name doesn't change any rule; fix or drop that example.
- **A11:** Evals 24 / 25 / 32 keep their expected verdicts under the new text (paper traces P1–P3). No eval asserts on remote-integration section numbers or scope-table wording (planning grep: only eval 24 mentions "App Directory", in a `contains_concept` assertion the new text still satisfies; §7 keeps "renamed from Slack App Directory").

### Impact Analysis

- **Direct:** the 2 files.
- **Adjacent:**
  - `SKILL.md` Step N reads the addendum's CRITICAL ratings and `Toward REJECTED` notes as CRITICAL flags. The new rating tables feed it directly.
  - The shared §4.6 hosted-service rule and the coverage contract are consumed, not changed.
  - `references/classifier.md` routes Type 9 here; unchanged.
- **Downstream:** live Type 9 verdicts shift.
  - Third-party integrations holding a standing grant with any High-class scope → CONDITIONAL (previously often APPROVED/Tier 1).
  - Vendors requiring SA JSON keys → CONDITIONAL.
  - Phone or device-code consent → REJECTED.
  - Native-app loopback callbacks are no longer flagged.
  - Reports gain ~10–18 coverage rows (several one-line `N/A`).
  - Eval verdicts are unchanged (P1–P3).

---

## Implementation

### Overview

Preflight → write the addendum (Step 1) → write the workflow (Step 2) → consistency script + harness + paper traces. Both steps are whole-file writes, not edits: nearly every section changes, and nobody else owns these files. Write each file with the content between its four-backtick `markdown` fence lines, exactly as given (fences excluded), ending in a single trailing newline.

**Preflight (`<work-root>` = worktree root):**

```bash
git -C <work-root> log --oneline -1 20843cc                                   # floor commit reachable
grep -c "^## 4.6 Version & Update Integrity (shared floor)" references/criteria.md   # 1
grep -c "^### V[1-5] " references/criteria.md                                 # 5
grep -c "^\*\*Hosted services\*\*" references/criteria.md                     # 1
grep -c "^\*\*Workflow coverage tables\*\*" references/criteria.md            # 1
grep -c "^| Version integrity (§4.6) |" references/criteria.md               # 1
grep -c "^- \*\*Blocking CVE\*\*" SKILL.md                                    # 1
git -C <work-root> rev-parse HEAD:workflows/remote-integration.md             # 5e062e5b96643db83e01712e630d96c36164d159
git -C <work-root> rev-parse HEAD:references/criteria/remote-integration.md   # ef950a9520f10c758fcc497a62d2723e830c1884
python3 evals/run_evals.py validate | head -3                                 # pass
python3 -m unittest discover -s evals -p "test_*.py" 2>&1 | tail -3           # record count (planning: Ran 12, OK)
```

**Stop rules:**
- Any floor grep ≠ expected → status `Blocked` (floor missing or renamed). Re-anchor the plug-in heading / row label to what landed only if the change is a pure rename; log it.
- Either blob hash differs → someone edited these files. Diff against the blob, merge their change into the Step 1/2 content by hand, log it, and continue.

---

### Step 1: Rewrite `references/criteria/remote-integration.md`

**Objective:** provider-neutral, flag-mapped Type 9 scoring addendum, with §4.6 plug-in and §4.3 CVE note (RI-2..RI-7, RI-9, RI-10, C6).
**Confidence:** High (structure, rules); Medium (example scope names; see A1/A2/A10)
**Depends on:** Preflight
**Do-Projex:** Encouraged
**Verify-Projex:** Encouraged (policy ratings; check traces P1–P10 against this file)

**Files:** `references/criteria/remote-integration.md`

**Changes:** replace the whole file (91 lines, `§1`…`§5`).

```markdown
// Before (abridged; full text at blob ef950a95):
<!-- Remote-integration criteria addendum. … this more-specific addendum wins. -->
# Remote Integration — Criteria Addendum
## §1 — OAuth Scope & Permission Assessment   (GitHub-only table incl. `read:email`, `delete:repo`, `admin:*`, `*`, `sudo`)
## §2 — Data Residency & Compliance Signals    ("US-only processing" negative)
## §3 — Terms of Service & Data Sharing
## §4 — Breach History & Security Posture
## §5 — Tier Thresholds
```

After (exact file content):

````markdown
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
````

**Rationale:**
- **Flags, not tier signals.** The old addendum only said "raise tier". The dispatcher tree runs on CRITICAL/HIGH/MEDIUM, so every new table names a rating. That cuts run-to-run variance (review risk "Report shape/confidence varies").
- **Scope classes + modifier instead of one big table.** Providers keep adding scopes. Classes generalize, and the maps are examples. The **standing-grant modifier** encodes the Drift lesson: a third party holding a long-lived token turns content-read into High.
- **§6 custody HIGH, not MEDIUM, for a standing High grant.** A MEDIUM alone yields APPROVED with no condition (tree). The review's steel-man counter says the gap is in the APPROVED path.
- **Resolved custody incident = MEDIUM, tighter than the shared V4(c) LOW.** For a package, a past hijack doesn't touch the audited artifact. For SaaS, the same token store holds the new grant. V4 is defined over malicious *code*, so custody theft is rated in §6 and the plug-in says so.
- **Consent-path ratings.** Email/chat link → HIGH, or CRITICAL with another phishing signal. This keeps eval 25 REJECTED without rejecting a legit vendor who emails a marketplace link. Phone and someone else's device code → CRITICAL, per the UNC6040 pattern.
- **Tier 1 keeps "published compliance documentation".** Eval 24 asserts the report mentions SOC 2; dropping the Tier 1 condition would risk that assertion.
- **§4.6 plug-in.** It follows the contract exactly (one heading, bullets `V1`–`V5`). V3 is tightened for re-consent (allowed: addenda may tighten). V5 lists subject triggers per RI-7.
- **Rejected alternatives:**
  - Per-provider scope tables as the primary rule (bloat; stale quickly).
  - Keeping §1–§5 numbering and appending (workflow references would still point at "§4.6 Integration Hygiene"-era structure).
  - Putting custody rules in the workflow (the workflow stays procedural; scoring lives in addenda, per sibling convention).

**Verification:**
```bash
wc -c < references/criteria/remote-integration.md                 # 19860
grep -c "^## §[0-9]* — " references/criteria/remote-integration.md # 10
grep -c "^## Version & Update Integrity (§4.6)$" references/criteria/remote-integration.md   # 1
grep -cE "read:email|delete:repo|US-only processing" references/criteria/remote-integration.md   # 0
sha256sum references/criteria/remote-integration.md               # 2206909f4a74566be652e2234ce9b3b0c002e9ddd1a045c7aed96236f99af04a
```

**If this fails:** `git -C <work-root> checkout -- references/criteria/remote-integration.md` and rewrite from the block.

---

### Step 2: Rewrite `workflows/remote-integration.md`

**Objective:** Type 9 procedure with Tier Triage, numbered checks, coverage rows per the shared contract, rubric aligned to shared numbering, updated verdict notes (RI-1, RI-3, RI-9, §4.6 collision).
**Confidence:** High
**Depends on:** Step 1 (section numbers referenced)
**Do-Projex:** Encouraged
**Verify-Projex:** Encouraged (coverage contract)

**Files:** `workflows/remote-integration.md`

**Changes:** replace the whole file (173 lines).

```markdown
// Before (abridged; full text at blob 5e062e5b):
## Identify            (8-row table incl. "Slack App Directory")
## Evidence — Part A   (checks 1–5, no tier step)
## Evidence — Part B   (checks 6–10)
## Subject Rubric      (### §4.1 OAuth Scope … ### §4.6 Integration Hygiene)
## Subject Verdict Notes
```

After (exact file content):

````markdown
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
````

**Rationale:**
- **Tier Triage as "Evidence — Part A"** mirrors `workflows/ci-action.md`. It names the report shape per tier, so `SKILL.md` Report → Shape stops depending on auditor judgment (RI-1).
- **Coverage table keeps canonical labels.** The shared contract requires it, and the consistency script checks every Required label. Subject rows (vendor identity & consent path, token custody, data handling, OAuth flow, non-OAuth credentials, webhooks) carry the Type 9 surface.
- **Required canonical rows at Tier 1 cost one line each.** Three of them are `N/A`. Tier 1 ends at ~10 rows, inside the Quick skeleton's 80-line budget.
- **Version integrity row = `Done`, not `N/A`.** V4 and V5 always apply to hosted services (shared hosted rule), so the row records their result. That is stricter than the shared row note, which is allowed.
- **Rubric renumbered 4.1–4.6** to the shared file's meaning (like ci-action). This removes the `§4.6` collision and puts the shared floor in its own numbered slot.
- **AI-connector Identify row.** It is route-agnostic: if the classifier sends hosted MCP connectors here (RI-8, sibling decision), the workflow already covers grant, data use and tool baseline. If it sends them to agent-extension, the row is harmless.
- **Rejected alternative:** section-level edits to the old file. Nearly every section changes, and the old structure is the thing being fixed.

**Verification:**
```bash
wc -c < workflows/remote-integration.md                                   # 13774
grep -c "^## Evidence — Part A: Tier Triage$" workflows/remote-integration.md   # 1
grep -c "^### 4\.[1-6] " workflows/remote-integration.md                  # 6
grep -c "§4.6 Integration Hygiene\|App Directory" workflows/remote-integration.md   # 0
sha256sum workflows/remote-integration.md                                 # 71cda01a5f801bc395dea7eadba21fd1934e9fe8686d3e22855c68591034a9f8
```

**If this fails:** `git -C <work-root> checkout -- workflows/remote-integration.md` and rewrite from the block.

---

## Verification Plan

### Automated Checks

- [ ] Consistency script, run from `<work-root>`, not committed. Prints `OK <wf bytes> <addendum bytes> canonical required rows: 11` (planning simulation result: `OK 13774 19860 canonical required rows: 11`):

```bash
python3 - <<'EOF'
import re, pathlib, sys
W = pathlib.Path("workflows/remote-integration.md").read_text(encoding="utf-8")
A = pathlib.Path("references/criteria/remote-integration.md").read_text(encoding="utf-8")
C = pathlib.Path("references/criteria.md").read_text(encoding="utf-8")
# sizes
assert len(W.encode()) <= 14500, len(W.encode())
assert len(A.encode()) <= 20500, len(A.encode())
# addendum section refs resolve
heads = set(re.findall(r"^## §(\d+) — ", A, re.M))
assert heads == {str(i) for i in range(1, 11)}, heads
for n in re.findall(r"addendum\s+§(\d+)", W):
    assert n in heads, ("workflow ref", n)
for n in re.findall(r"(?<![\d.])§(\d+)(?![\d.])", A):
    assert n in heads, ("addendum self-ref", n)
# §4.6 plug-in shape
assert A.count("## Version & Update Integrity (§4.6)") == 1
for v in ["V1", "V2", "V3", "V4", "V5"]:
    assert A.count(f"- **{v}** —") == 1, v
vheads = set(re.findall(r"^### (V[1-5]) ", C, re.M))
for f, t in (("W", W), ("A", A)):
    for v in re.findall(r"§4\.6 (V\d)", t):
        assert v in vheads, (f, v)
# canonical Required rows carried with unchanged labels
rows = re.findall(r"^\| ([^|]+?) \| ([^|]+?) \| ([^|]+?) \| ([^|]+?) \|", C.split("### Rows by tier")[1].split("\n\n**Tier 1")[0], re.M)
req = [r[0] for r in rows if "Required" in " ".join(r[1:4]) and r[0] != "Check"]
for label in req:
    assert f"| {label} |" in W, ("missing canonical row", label)
assert "Version integrity (§4.6)" in req, req
# stale literals gone
for bad in ["read:email", "delete:repo", "`admin:*`", "`sudo`", "US-only processing",
            "### §4.6 Integration Hygiene", "major version bump", "write:packages` (own)"]:
    assert bad not in W and bad not in A, bad
assert "App Directory" not in W and A.count("App Directory") == 1
# no projex artifacts in shipped files
for t in (W, A):
    assert not re.search(r"\d{10}-[a-z0-9-]+-(plan|eval|walkthrough|log)", t)
    assert ".projex" not in t
print("OK", len(W.encode()), len(A.encode()), "canonical required rows:", len(req))
EOF
```

- [ ] `python3 evals/run_evals.py validate` passes; unittest count = Preflight.
- [ ] `git -C <work-root> diff --stat <base>..HEAD` → exactly `references/criteria/remote-integration.md`, `workflows/remote-integration.md`.

### Manual Verification (paper traces)

Walk each case through the new workflow + addendum + `SKILL.md` Step N. Log the cited section per hop.

| # | Case | Expected |
|---|---|---|
| P1 | eval 24: official Slack app from Slack, `channels:read` (Low), `chat:write` (Low), `users:read` (Elevated, justified), Slack Marketplace, admin install | §1 no flag; §6 first-party → no custody flag; §7 listed; compliance published; §4.6 V1–V3 N/A, V4 none; §10 Tier 1 ✓ → **APPROVED**, Quick skeleton; Recommendation lists V5 triggers |
| P2 | eval 25: email link, unknown vendor, `.xyz`, `gmail.readonly` + `drive` (restricted → High), `admin.directory.user` (High) | §1 High unjustified → CRITICAL; §6 email + unknown vendor → CRITICAL; §7 unverified → HIGH; Tier 3 → **REJECTED** |
| P3 | eval 32: Zapier (third party) + GitHub `repo` (High) + `read:org` (Elevated) for labeling | §1 `repo` justified; narrower option (GitHub App on selected repos) → HIGH, or MEDIUM if none offered; §6 third-party standing High grant → **HIGH** regardless; Tier 2 → **CONDITIONAL** (conditions: narrower option / admin approval / grant review; data retention reviewed in data-handling row) |
| P4 | "IT support" calls, asks the user to enter a code at the provider's device page to approve "Data Loader" | §3 device code from someone else → CRITICAL; §6 phone → CRITICAL → **REJECTED** |
| P5 | Vendor requires a downloadable GCP SA JSON key with Editor role; workload identity federation is available | §2 SA key + keyless option → HIGH; Tier 3 → **CONDITIONAL** (keyless option, or dedicated SA + rotation + scoped exception) |
| P6 | AI meeting-notes connector: delegated calendar + Drive read with `offline_access`; forwards to a named LLM provider without retention terms | §1 Elevated + standing modifier → High; §6 third-party standing High → HIGH; §5 AI sub-processor retention unstated → MEDIUM → **CONDITIONAL** |
| P7 | Established vendor whose token store was breached 3 months ago; tokens revoked platform-wide, postmortem published; minimal scopes | §6 resolved → MEDIUM, Tier 1 unavailable → Tier 3; no HIGH → **APPROVED** with MEDIUM noted (or CONDITIONAL with 2 more MEDIUMs). Same, unresolved → CRITICAL → **REJECTED** |
| P8 | Inbound webhook without signature that triggers deploys | §9 → HIGH → **CONDITIONAL** (verify signatures + replay window) |
| P9 | Desktop app uses `http://127.0.0.1:<port>` callback, vendor domain otherwise canonical | §3 → no flag (RFC 8252); verdict decided by other checks |
| P10 | Third-party Slack app with `admin.*` scopes, no stated reason | §1 High unjustified → CRITICAL → **REJECTED** |

### Acceptance Criteria Validation

| Criterion | How to Verify | Expected Result |
|-----------|---------------|-----------------|
| Files match plan content | `wc -c` + `sha256sum` | 19,860 / 13,774 B; hashes as in Success Criteria (or logged deviation) |
| Contract, refs, stale literals | consistency script | `OK … 11` |
| Harness green | validate + unittest | pass; same count |
| Eval verdicts preserved | P1–P3 | APPROVED / REJECTED / CONDITIONAL |
| New behaviors | P4–P10 | as table |
| Only 2 files changed | `git diff --stat` | 2 files |

---

## Rollback Plan

1. Before close: `projex-abandon.sh <repo-root> claude/youthful-dijkstra-5ov1kt projex/<this-plan> --worktree`. Base is untouched.
2. After squash-close: `git -C <repo-root> revert <squash-sha>`. It touches only the 2 files; nothing else references their section numbers (planning grep: `SKILL.md` names only the workflow path).

---

## Notes

### Hand-off (requirements for other plans; this plan does not implement them)

| Plan | Requirement |
|---|---|
| generic / classifier (RI-8) 2610162004-generic-fallback-and-classifier-refresh-plan.md | Add a `references/classifier.md` Routing Override for "Add connector" / remote MCP over HTTP + OAuth with no local code. Whichever route is chosen, state the tie-break signal in one line plus a worked example. **If → remote-integration:** this workflow already has the Identify row "AI connector", addendum §5 tool baseline and destructive-tool rule, and §4.6 V3/V5 tool-list triggers. Tool-capability depth should cite `references/criteria/agent-extension.md` (capability classes) rather than copy it. **If → agent-extension:** that workflow should apply this addendum §1 (scope classes), §5 (AI data use) and §6 (custody & consent path) to the OAuth grant, by section reference. Unverified MCP-spec claims (CIMD preferred over DCR, RFC 9728, RFC 8707) stay hedged or out (review evidence #11, Low-Medium). Do **not** edit `workflows/remote-integration.md` or `references/criteria/remote-integration.md`; request a revise of this plan's output instead |
| agent-extension 2610162007-agent-extension-rubric-refresh-plan.md | Same coordination as above for remote Streamable-HTTP/OAuth MCP. No edits to the Type 9 files |
| eval refresh (E-1) | New Type 9 cases, matching traces P4–P6 (and optionally P7 unresolved, P8):<br>• device-code / vishing connected app → REJECTED<br>• vendor requiring a GCP SA JSON key → CONDITIONAL<br>• AI connector with LLM sub-processor + `offline_access` → CONDITIONAL<br>• Drift-pattern custody incident: unresolved → REJECTED<br>• unsigned inbound webhook → CONDITIONAL<br>Eval 24: update the prompt and expected text "Slack App Directory" → "Slack Marketplace" and the assertion "Report notes Slack App Directory as official marketplace" → "…Slack Marketplace (formerly App Directory)…"; the current assertion still passes. Eval 32: expected_output may note that GitHub `repo` is read **and** write (no read-only private-repo scope); the verdict is unchanged |
| STEWARDSHIP (orchestrator) | Type 9 row: Last Reviewed 2026-10-16; watch list: OAuth 2.1 RFC status, MCP authorization spec, Slack/Google API-terms changes, CASA program |

### Risks

- **Addendum size (5.4 → 19.9 KB, ~5k tokens per Type 9 audit).** Mitigation: maps are short examples, and the workflow stays procedural. If a later trim is wanted, cut the provider maps first; the class rules stand alone.
- **Over-conditioning.** Any third-party standing High grant → CONDITIONAL. Intentional (review Dissent/steel-man counter). The conditions are standard controls, so it is cheap to satisfy.
- **Example scope names wrong or renamed by providers (A1/A2/A10).** Mitigation: maps say "examples, not complete lists". An unknown scope defaults to High until docs show otherwise; fixing a name is a one-line revise.
- **Secondary-source facts (A5, A6).** Mitigation: hedged wording ("check the platform's current text"); no numbers or victim counts shipped.
- **RI-8 lands contradicting the AI-connector row.** Mitigation: the row is route-agnostic; the Hand-off states both outcomes.
- **Report length.** Tier 2/3 tables gain rows. Mitigation: one-line `N/A` rows; Tier 1 at ~10 rows.

### Open Questions

None blocking.
- RI-8 route is owned by the sibling plan; this plan works under either outcome.
- `draft-ietf-oauth-v2-1-16` status: irrelevant once the shipped text says only "Internet-Draft".

### Split Decision

`No split — single scope, within size budget`. 2 steps (heuristic needs > 5 steps), one `.projex/` scope, spec-only prose. The plan is > 500 lines because it embeds both files verbatim, but the steps are coupled: workflow section refs resolve against the addendum.

### Revision Log

| Date | Trigger | Change |
|---|---|---|
| 2026-10-16 | Initial | Full rewrite of both Type 9 files on the landed §4.6 floor (`20843cc`) |
