# Browser Extension Workflow — M3.1

> **Status:** Ready
> **Created:** 2026-04-14
> **Author:** Claude (Opus 4.6)
> **Source:** [2604070218-install-auditor-subject-typed-redesign-nav.md](2604070218-install-auditor-subject-typed-redesign-nav.md) Phase 3, M3.1
> **Related Projex:**
> - **Roadmap:** [2604070218-install-auditor-subject-typed-redesign-nav.md](2604070218-install-auditor-subject-typed-redesign-nav.md)
> - **Framing eval (ideation §5.1, §5.3):** [2604070217-subject-typed-audit-dispatch-eval.md](2604070217-subject-typed-audit-dispatch-eval.md)
> - **Taxonomy spec:** [2604070300-install-auditor-subject-type-taxonomy-def.md](2604070300-install-auditor-subject-type-taxonomy-def.md)
> - **Pattern precedent (M2.1):** Direct execution (2026-04-09) — no separate plan-projex; `workflows/registry-package.md` is the structural template
> **Worktree:** Yes

---

## Summary

Create the browser-extension subject-specific workflow (`workflows/browser-extension.md`) and its criteria addendum (`references/criteria/browser-extension.md`), then wire them into the dispatcher and eval suite. This is the first Phase 3 milestone — it validates that the dispatcher architecture extends cleanly beyond registry packages to a fundamentally different subject type where permissions (not supply chain) are the primary risk surface.

**Scope:** Type 2 browser-extension audit pipeline — workflow file, criteria addendum, dispatch table update, eval re-routing.
**Estimated Changes:** 4 files (2 new, 2 modified), ~700 new lines.

---

## Objective

### Problem / Gap / Need

Browser extensions currently route to `workflows/generic.md`, which was inherited from the pre-pivot monolith. The framing eval (§5.1) identifies six concrete failures:

1. `registry-lookup.ps1` runs uselessly — it knows nothing about Chrome Web Store, AMO, or Edge Add-ons.
2. §4.4 Permissions is the most critical rubric for extensions but sits as one generic bullet among five others — no manifest permission taxonomy, no MV2/MV3 awareness, no `host_permissions` vs `activeTab` guidance.
3. Tier thresholds (>100K weekly npm downloads) are npm-specific and meaningless for extensions whose adoption signal is store user count.
4. No store verification guidance — Chrome Web Store "Featured" badge, Firefox "Recommended" badge, Edge certified publisher.
5. No content-script reach analysis — extensions that inject into `<all_urls>` vs specific domains have radically different risk profiles.
6. No auto-update risk awareness — extensions auto-update silently, so a single compromised update pushes to every installed user with no lockfile equivalent.

The Wappalyzer eval case (id 1) already expects browser-extension-specific reasoning ("discusses browser extension permissions, broad URL access") but currently arrives via the generic fallback.

### Success Criteria

- [ ] `workflows/browser-extension.md` exists, follows the Identify / Evidence / Subject Rubric / Subject Verdict Notes template
- [ ] `references/criteria/browser-extension.md` exists, layers browser-extension-specific scoring on top of `references/criteria.md`
- [ ] `SKILL.md` dispatch table row 2 routes to `workflows/browser-extension.md` (not `workflows/generic.md`)
- [ ] Wappalyzer eval case (id 1) still passes — assertions remain compatible
- [ ] At least one new browser-extension eval case added (negative or edge case)
- [ ] No regressions in existing eval cases (ids 0, 2–9)

### Out of Scope

- Helper scripts for store API queries (no Chrome Web Store API script in M3.1 — agent uses web search; script is a future enhancement)
- Modifications to `workflows/generic.md` or `workflows/registry-package.md`
- Changes to the shared `references/criteria.md` beyond what's already there (the "Browser extensions: Always include Permissions / least privilege" note already exists)
- Other Phase 3 workflows (container-image, ci-action, ide-plugin)

---

## Context

### Current State

The dispatcher (`SKILL.md`) classifies browser extensions via strong signals (`manifest permissions+host_permissions`, `chromewebstore.google.com/*`, `addons.mozilla.org/*`, `.crx/.xpi`) and routes them to `workflows/generic.md` as a fallback. The generic workflow has no browser-extension-specific logic — the agent improvises permission analysis, store lookup, and manifest interpretation each time.

`references/criteria.md` §4.3 already contains one browser-extension-aware note: "Browser extensions: Always include Permissions / least privilege when the installable is an extension." This is the only subject-specific guidance in the shared rubric.

### Key Files

| File | Role | Change Summary |
|------|------|----------------|
| `workflows/browser-extension.md` | **New.** Type 2 subject-specific workflow | Create ~450 lines: Identify (store + manifest extraction) / Evidence (browser-extension tier thresholds + research) / Subject Rubric (permission-centric scoring) / Subject Verdict Notes |
| `references/criteria/browser-extension.md` | **New.** Per-subject criteria addendum | Create ~200 lines: permission risk tiers, store trust signals, manifest analysis guidance, auto-update risk, content-script scoring |
| `SKILL.md` | Dispatcher + dispatch table | Update 1 line: row 2 dispatch target → `workflows/browser-extension.md` |
| `evals/evals.json` | Regression + new eval cases | Update Wappalyzer (id 1) assertions for subject-type routing; add 1–2 new browser extension cases |

### Dependencies

- **Requires:** Phase 2 complete (confirmed 2026-04-12), dispatcher architecture live, registry-package workflow as pattern precedent
- **Blocks:** M3.5 eval gate (needs at least one browser-extension eval case)

### Constraints

- Workflow must follow the established 4-section template: Identify / Evidence / Subject Rubric / Subject Verdict Notes
- Audit Coverage table and audit-confidence assertion are owned by the dispatcher (`SKILL.md` Step N) — workflow must not duplicate them
- No new PowerShell scripts in M3.1 scope — evidence acquisition uses web search and manual manifest inspection
- Criteria addendum follows the `references/criteria/registry-package.md` pattern: layers on `references/criteria.md`, more-specific wins on conflict

### Assumptions

- Chrome Web Store, Firefox AMO, and Edge Add-ons are the three stores worth covering in v1. Safari Web Extensions (App Store distribution) deferred — different enough (Xcode-signed, App Store review) to warrant M4-era coverage or a note in the workflow.
- MV3 is the current standard; MV2 extensions still exist but Chrome is phasing them out. The workflow should flag MV2 as a risk signal (approaching end-of-life, may lose store support) rather than rejecting outright.
- Permission risk classification can be done statically from the manifest without executing the extension. Dynamic analysis (runtime behavior monitoring) is Tier 3 deep-audit territory and out of scope for the workflow prose (the agent can choose to do it, but the workflow won't prescribe a procedure).
- The Wappalyzer eval case (id 1) assertions are broad enough to pass whether the extension is routed through `generic.md` or `browser-extension.md` — the new workflow produces a superset of the expected findings.

### Impact Analysis

- **Direct:** `workflows/browser-extension.md` (new), `references/criteria/browser-extension.md` (new), `SKILL.md` dispatch table (1-line edit), `evals/evals.json` (update + additions)
- **Adjacent:** `workflows/generic.md` — no longer receives browser-extension traffic, but no code changes needed (it still works as fallback for other types)
- **Downstream:** M3.5 eval gate depends on browser-extension eval coverage existing

---

## Implementation

### Overview

Four steps, executed in dependency order: (1) create the criteria addendum (referenced by the workflow), (2) create the workflow file, (3) wire the dispatch table, (4) update evals. Steps 1–2 are the bulk of the work; steps 3–4 are mechanical.

### Step 1: Create `references/criteria/browser-extension.md`

**Objective:** Establish browser-extension-specific scoring extensions that layer on `references/criteria.md`.
**Confidence:** High
**Depends on:** None

**Files:**
- `references/criteria/browser-extension.md` (new)

**Changes:**

The addendum follows the `registry-package.md` pattern — header declaring scope, then sections that specialize the shared rubric's §4.x areas for browser extensions.

Content structure:

```markdown
# Browser Extension — Criteria Addendum

Per-subject scoring extensions for **Type 2: browser-extension** audits.
This addendum layers on top of the shared rubric in `references/criteria.md`.
When a criterion below conflicts with the shared rubric, the more specific
(browser-extension) guidance wins.

Covers: Chrome Web Store, Firefox Add-ons (AMO), Microsoft Edge Add-ons,
and sideloaded .crx/.xpi files.

## Store Trust Signals

| Store | Verified Publisher Signal | Adoption Metric | Trust Notes |
|-------|--------------------------|-----------------|-------------|
| Chrome Web Store | "Featured" badge, verified publisher | User count + rating count | Largest store; review process exists but is not exhaustive |
| Firefox Add-ons (AMO) | "Recommended" badge (human-reviewed) | User count + daily active | AMO "Recommended" is the strongest store signal — requires manual review |
| Edge Add-ons | "Certified" publisher | User count | Smaller catalog; many extensions are CWS cross-posts |
| Sideloaded (.crx/.xpi) | None | None | No store verification — highest baseline risk |

### Scoring impact

- AMO "Recommended" badge = strong positive (equivalent to npm verified publisher)
- CWS "Featured" badge = moderate positive (algorithmic, not human-reviewed)
- Edge "Certified" = moderate positive
- No store listing (sideloaded) = strong negative (equivalent to installing from unknown npm mirror)

## Permission Risk Classification

### High-risk permissions

These grant broad or sensitive access. Any one of these triggers elevated scrutiny:

| Permission | Risk | Why |
|------------|------|-----|
| `<all_urls>` / `*://*/*` | Critical | Full read/write access to every page the user visits |
| `webRequest` + `webRequestBlocking` | Critical | Can intercept, modify, or block all HTTP traffic (MV2 only — MV3 uses `declarativeNetRequest`) |
| `cookies` | High | Read/write cookies for any permitted domain — session hijacking vector |
| `nativeMessaging` | High | Communicates with native executables on the host — breaks the browser sandbox |
| `debugger` | High | Full Chrome DevTools Protocol access to any tab — equivalent to `<all_urls>` + JS execution |
| `proxy` | High | Routes all browser traffic through an attacker-controlled proxy |
| `downloads` | High | Can silently download files to the user's filesystem |
| `history` | Medium-High | Full browsing history access — privacy-sensitive |
| `bookmarks` | Medium | Full bookmark tree access — privacy-sensitive |
| `tabs` | Medium | Enumerate all open tabs with URLs and titles — privacy-sensitive and phishing enabler |
| `clipboardRead` / `clipboardWrite` | Medium | Read/write system clipboard — credential theft vector |
| `management` | Medium-High | Can enable/disable/uninstall other extensions |

### Medium-risk permissions

| Permission | Risk | Why |
|------------|------|-----|
| `activeTab` (with broad `host_permissions`) | Medium | `activeTab` alone is low risk, but combined with broad host_permissions it grants tab access on click across many sites |
| `storage` / `unlimitedStorage` | Medium | Local data storage — low risk alone, but can exfiltrate via other permissions |
| `notifications` | Low-Medium | Can display system notifications — social engineering vector |
| `contextMenus` | Low | Adds right-click menu items — low risk alone |
| Host patterns (specific) | Varies | `*://*.google.com/*` is narrower than `<all_urls>` but still grants full page access on matched domains |

### Low-risk permissions

| Permission | Risk | Why |
|------------|------|-----|
| `activeTab` (alone, no broad hosts) | Low | Only activates on user click, only for the current tab |
| `alarms` | Low | Scheduling — no data access |
| `idle` | Low | Detects user idle state — minimal privacy impact |
| `theme` | Low | Visual customization only |
| `declarativeNetRequest` (MV3) | Low-Medium | Rule-based network filtering — less powerful than `webRequestBlocking` by design |

### Scoring impact

- 0 high-risk permissions → neutral
- 1 high-risk permission with clear justification → note, not a flag
- 1 high-risk permission without justification → MEDIUM flag
- 2+ high-risk permissions → HIGH flag unless the extension's purpose requires them (ad blockers need `webRequest`/`declarativeNetRequest` + broad host access)
- `<all_urls>` or `*://*/*` without clear purpose → HIGH flag
- `nativeMessaging` on any extension that doesn't explicitly need host communication → CRITICAL flag

## Manifest Version (MV2 vs MV3)

| Signal | Interpretation |
|--------|---------------|
| MV3 | Current standard. Preferred. Uses `declarativeNetRequest` (less powerful than `webRequestBlocking`), service workers instead of persistent background pages, promise-based APIs. |
| MV2 | Legacy. Chrome deprecating (timeline shifting but direction clear). MV2 extensions can use more powerful APIs (`webRequestBlocking`) but face removal from CWS. Flag as: "MV2 — approaching end-of-life on Chrome; verify Firefox/Edge support timeline." |
| MV2 on Firefox only | Firefox has committed to long-term MV2 support. Not a risk signal if the extension targets Firefox exclusively. |

### Scoring impact

- MV3 = neutral (expected)
- MV2 on Chrome = MEDIUM flag (end-of-life risk, not a security flag per se)
- MV2 on Firefox = LOW note (acceptable — Firefox committed to MV2 support)

## Content Script Reach

Content scripts inject JavaScript/CSS into web pages. Their reach is the
most direct measure of an extension's attack surface.

| Pattern | Reach | Risk |
|---------|-------|------|
| `"matches": ["<all_urls>"]` | Every page | Critical — equivalent to `<all_urls>` permission |
| `"matches": ["*://*.google.com/*", ...]` (few specific domains) | Scoped | Low-Medium — proportional to domain count and sensitivity |
| `"matches": ["*://*/*"]` with `"exclude_matches"` | Broad with exclusions | High — exclusions reduce reach but default is still all HTTP(S) |
| No content scripts | None | Neutral |
| `"match_about_blank": true` | Extends to about:blank iframes | Medium — can inject into iframes on pages |

### Scoring impact

- Content scripts on `<all_urls>` = HIGH flag (must be justified by extension purpose)
- Content scripts on a handful of specific domains = proportional to domain sensitivity
- No content scripts = positive signal (extension works via popup/background only)

## Auto-Update Risk

Browser extensions auto-update silently. Unlike registry packages (lockfile,
pinned version), there is no user-side mechanism to prevent updates.

| Signal | Interpretation |
|--------|---------------|
| Open-source with release tags | Moderate mitigation — updates can be audited post-hoc |
| Closed-source | Higher risk — updates cannot be independently verified |
| Recent ownership transfer | CRITICAL — new owner can push malicious update to entire user base |
| "Self-hosted" update URL (MV2 Firefox) | HIGH — updates bypass store review entirely |

### Scoring impact

- Open-source + store-distributed = neutral (standard pattern)
- Closed-source + store-distributed = LOW note (common, but re-audit on incidents)
- Self-hosted updates = HIGH flag (no store review gate)
- Recent ownership change = MEDIUM-HIGH flag (re-audit from scratch)

## Tier Assignment Thresholds (Browser Extensions)

### Tier 1 — Quick Audit

ALL of these must hold:
- User count ≥ 100K on primary store
- Verified/Featured/Recommended badge present
- Publisher is a known company or well-known open-source project
- No `<all_urls>` or `*://*/*` unless the extension's purpose is inherently
  broad (ad blocker, password manager, dev tools — and even then, note it)
- MV3 manifest version (or MV2 on Firefox with AMO Recommended)
- No known incidents or store removals in search results
- Extension has been listed ≥ 1 year

### Tier 2 — Standard Audit (default)

Default when not all Tier 1 criteria are met:
- User count 1K–100K
- Identifiable publisher
- No known security incidents
- Listed > 30 days

### Tier 3 — Deep Audit

ANY of these triggers:
- User count < 1K
- No store listing (sideloaded .crx/.xpi)
- Publisher unknown or anonymous
- `<all_urls>` + `cookies` or `webRequest` without obvious justification
- Extension shared via direct link / chat (not store URL)
- Recent ownership transfer or developer change
- Known prior removal or policy violation from any store
- MV2 with `webRequestBlocking` on Chrome (powerful + deprecated = risk)
- `nativeMessaging` permission present
- Self-hosted update URL
```

**Rationale:** The addendum establishes the browser-extension-specific scoring vocabulary that the workflow references. Creating it first ensures the workflow can defer to it by path without forward references. The permission risk classification is the core contribution — the framing eval identified "no checklist of *which* manifest permissions are dangerous" as the top gap.

**Verification:** File exists at `references/criteria/browser-extension.md`. Sections cover: Store Trust Signals, Permission Risk Classification (high/medium/low), Manifest Version, Content Script Reach, Auto-Update Risk, Tier Assignment Thresholds.

**If this fails:** Delete the file. No other files depend on it yet.

---

### Step 2: Create `workflows/browser-extension.md`

**Objective:** Author the Type 2 workflow following the established template.
**Confidence:** High
**Depends on:** Step 1 (criteria addendum must exist for cross-references)

**Files:**
- `workflows/browser-extension.md` (new)

**Changes:**

The workflow follows the registry-package.md structural pattern (Identify / Evidence — Part A: Triage / Evidence — Part B: Research / Subject Rubric / Subject Verdict Notes) but with browser-extension-native content throughout.

Content structure:

```markdown
<!--
workflows/browser-extension.md - Type 2 subject-specific workflow.
Handles browser extensions from Chrome Web Store, Firefox Add-ons (AMO),
Microsoft Edge Add-ons, and sideloaded .crx/.xpi files.

This workflow replaces workflows/generic.md for Type 2 subjects. After
producing findings here, return to SKILL.md Step N for the shared verdict
tree and report shape. The Audit Coverage table and audit-confidence
assertion are owned by the dispatcher — do not duplicate them here.

Phase 3 / M3.1 — second subject-specific workflow (first Phase 3).
-->

# Browser Extension Workflow (Type 2)

This workflow handles **Type 2: browser-extension** subjects from Chrome Web
Store, Firefox Add-ons (AMO), Microsoft Edge Add-ons, and sideloaded
.crx/.xpi files. It specializes the generic evidence acquisition and scoring
pipeline for browser extension concerns: manifest permissions, store
verification, content-script reach, and auto-update risk.

After completing all sections below, return to `SKILL.md` Step N for the
shared verdict tree and audit-coverage report shape.

Sections follow the standard workflow template: **Identify / Evidence /
Subject Rubric / Subject Verdict Notes**.

## Identify

### 1. Determine the store and extension identity

| Store | URL pattern | Adoption metric |
|-------|-------------|-----------------|
| Chrome Web Store | `chromewebstore.google.com/detail/*` | User count |
| Firefox Add-ons (AMO) | `addons.mozilla.org/*/addon/*` | User count / daily active |
| Edge Add-ons | `microsoftedge.microsoft.com/addons/detail/*` | User count |
| Sideloaded | `.crx` / `.xpi` file, no store URL | None |

If the user provides a store URL, extract the extension name and ID from the
listing page. If they provide a name only, search the relevant store.

### 2. Extract the extension name and metadata

- **Extension name**: Exact name as listed in the store
- **Extension ID**: Chrome/Edge use a 32-character ID (e.g., `gppongmhjkpfnbhagpmjfkannfbllamg`);
  Firefox uses a GUID or `name@author` format
- **Publisher/developer**: Name shown on the store listing — map to company
  or individual
- **Version**: Current store version (extensions auto-update; users rarely
  pin versions)
- **Store badges**: Chrome "Featured", Firefox "Recommended", Edge "Certified"
- **User count and rating**: Primary adoption metric (replaces npm weekly
  downloads)

### 3. Gather required context

Collect before proceeding:

1. **Full name and store ID** — exact extension name + store identifier
2. **Source store** — which store (from table above), or sideloaded
3. **Installation method** — store install button, direct .crx/.xpi, managed
   via enterprise policy, or developer mode sideload
4. **Stated purpose** — what the user needs this extension for
5. **Target browser** — Chrome, Firefox, Edge, Brave, Arc, etc.
6. **Manifest version** — MV2 or MV3 (inspect the store listing or manifest.json)

If any of 1–5 are missing, ask before proceeding. Item 6 is obtained during
research if not immediately available.

## Evidence — Part A: Triage (Pick the Audit Tier)

Gather store listing data via web search:
- User count, rating, review count
- Publisher name and verification badges
- First listed date (if available from store or web archive)
- Brief search for "[extension name] malware OR removed OR security" to
  check for prior incidents

Then apply the **browser-extension-specific tier thresholds** from
`references/criteria/browser-extension.md` (section "Tier Assignment
Thresholds"):

### Tier 1 — Quick Audit (well-known, high-trust)

Use when ALL Tier 1 criteria from the addendum are met: ≥100K users, store
badge, known publisher, reasonable permissions for stated purpose, MV3 (or
MV2 on Firefox with Recommended), no incidents, listed ≥1 year.

**Quick audit scope:** Confirm store presence + badge, note permissions at
a glance, check for recent incidents, verify publisher. No deep manifest
analysis. If everything checks out, proceed directly to Subject Verdict
Notes with minimal ceremony.

### Tier 2 — Standard Audit (default)

Default depth. Full manifest analysis, permission justification assessment,
store verification, incident search, source code spot-check if open source.

### Tier 3 — Deep Audit (any red flag)

Any Tier 3 trigger from the addendum: low users, sideloaded, unknown
publisher, dangerous permission combinations, ownership change, prior
removal, self-hosted updates, `nativeMessaging`.

**Deep audit scope:** Full manifest analysis + permissions audit + source
code review (if available) + behavioral analysis of content scripts +
background script/service worker logic + network traffic patterns.

## Evidence — Part B: Research

### Core research questions (all tiers)

Answer every question that applies to the assigned tier:

1. **Who publishes this extension?** Company, individual, open-source
   project? Is the publisher the same entity across Chrome/Firefox/Edge
   listings? Check for impersonation (same name, different publisher).
2. **What permissions does the manifest declare?** Read `manifest.json`
   permissions, host_permissions (MV3), optional_permissions, and
   content_scripts matches. Cross-reference against the permission risk
   classification in `references/criteria/browser-extension.md`.
3. **Does the permission set match the stated purpose?** A tab manager
   requesting `<all_urls>` + `cookies` + `webRequest` is suspicious. An ad
   blocker requesting `declarativeNetRequest` + broad host access is expected.
4. **Is the extension on multiple stores?** Cross-listing (Chrome + Firefox +
   Edge) increases confidence. A Chrome-only extension with no Firefox
   version is not a red flag but is a data point.
5. **Are there known security incidents?** Search for prior store removals,
   malware reports, ownership changes, data exfiltration allegations.
6. **What is the update cadence?** Frequent updates = active maintenance.
   No updates in >1 year = stale but not necessarily dangerous (simple
   extensions may not need updates).
7. **Is the source code available?** Open-source extensions can be audited;
   closed-source cannot. Note the repo URL if available.

### How to research

**Store listing inspection** (all tiers):

Web search for the extension's store page. Extract:
- User count, rating, review count
- Publisher name + any verification badge
- Permissions shown on the store page (Chrome Web Store shows permissions
  pre-install; Firefox shows them post-install or in the listing)
- "Privacy practices" or "Privacy policy" link (CWS shows this)
- Reviews mentioning security, privacy, or suspicious behavior

**Manifest analysis** (Tier 2 and Tier 3):

Obtain `manifest.json` via one of:
- The extension's open-source repository (GitHub, GitLab, etc.)
- Chrome Web Store source viewer (crxcavator.io or similar)
- `about:debugging` in Firefox → inspect installed extension → manifest
- Direct .crx/.xpi download + unzip (ZIP format)

Inspect these manifest keys:
- `permissions` — API permissions (Chrome namespace APIs)
- `host_permissions` (MV3) or `permissions` URL patterns (MV2) — which
  domains the extension can access
- `optional_permissions` — permissions requested at runtime (lower risk than
  static, but note them)
- `content_scripts` → `matches` — which pages get injected JS/CSS
- `background` → `service_worker` (MV3) or `scripts` (MV2) — background
  logic that runs persistently or on events
- `externally_connectable` — which websites/extensions can message this one
- `content_security_policy` — custom CSP (relaxed CSP = risk signal)
- `update_url` (MV2 Firefox) — self-hosted update server (bypasses store
  review)
- `web_accessible_resources` — files exposed to web pages (fingerprinting /
  data exfiltration vector)

**Incident and reputation search** (all tiers, depth varies):

Web search queries:
- `"<extension name>" malware OR removed OR security OR vulnerability`
- `"<extension name>" privacy OR data OR tracking`
- `"<extension ID>" security` (catches technical reports)
- `"<publisher name>" extension OR addon OR malware` (catches publisher-wide
  incidents)

For Tier 3, also search:
- `"<extension name>" site:reddit.com` (user reports)
- `"<extension name>" site:github.com` (issue tracker reports)

**Source code review** (Tier 3 if open source, spot-check for Tier 2):

If the extension is open source, review:
- Content scripts: What do they inject? Do they read page data, modify DOM,
  intercept forms?
- Background script/service worker: Does it make external network calls?
  To what domains? Does it send collected data anywhere?
- `fetch()` / `XMLHttpRequest` calls: Where does data go? Is it the
  extension's own server, a third-party analytics service, or an unknown
  endpoint?
- Obfuscation: Is the code minified/obfuscated? Minification is normal for
  build output; heavy obfuscation (eval-based, string encoding) in a
  browser extension is a red flag.

### Audit coverage tracking

Map evidence to the Audit Coverage rows expected by `SKILL.md` Step N. For
browser extensions, the standard rows are:

| Check | Tier 1 | Tier 2 | Tier 3 |
|-------|--------|--------|--------|
| Store listing / metadata | Required | Required | Required |
| Publisher verification | Required | Required | Required |
| Permission manifest analysis | Brief | Required | Required |
| Content script reach | Brief | Required | Required |
| CVE / advisories | Required | Required | Required |
| Web search — incidents & removal | Brief | Required | Required |
| Source code review | Tier-skip | If open source | Required |
| Manifest version (MV2/MV3) | Note | Required | Required |
| Auto-update risk | Tier-skip | Note | Required |
| Cross-store listing check | Optional | Required | Required |
| OpenSSF Scorecard | Optional | If repo known | Required |

## Subject Rubric — Evaluate

Score against the shared rubric in `references/criteria.md` AND the
browser-extension addendum in `references/criteria/browser-extension.md`.
The sections below specialize the shared criteria for browser extension
context.

### 4.1 Provenance & Identity (browser-extension-specialized)

- **Store verification**: Is the extension listed on an official store? Which
  stores? Are the listings consistent (same publisher, same permissions)?
- **Publisher identity**: Can the publisher be linked to a real company or
  known open-source project? Check the store developer page, linked website,
  and GitHub/GitLab org.
- **Store badge**: Firefox "Recommended" (strongest signal — human review),
  Chrome "Featured" (moderate — algorithmic), Edge "Certified" (moderate).
- **Impersonation check**: Are there similarly-named extensions by different
  publishers? Search the store for the extension name and check for
  copycats.
- **Cross-store consistency**: If listed on multiple stores, is the publisher
  the same entity? Different publishers on different stores is a red flag.

### 4.2 Maintenance & Longevity (browser-extension-specialized)

- **Last update date**: When was the last version pushed to the store?
  Extensions may go longer between updates than packages (a simple tool may
  not need updates), but >2 years with no update on an extension that
  interacts with web pages is a concern (web APIs change).
- **User count trend**: Is the user count growing, stable, or declining? A
  sharp decline may indicate a quality or trust issue.
- **Review sentiment**: Check recent reviews for reports of suspicious
  behavior, broken functionality, or abrupt changes after an update.
- **Open-source activity**: If the source is public, check commit recency,
  issue responsiveness, and contributor count.

### 4.3 Security Track Record (browser-extension-specialized)

- **Store removal history**: Has this extension (or a same-name predecessor)
  ever been removed from a store for policy violations? Search for
  "[extension name] removed Chrome Web Store".
- **CVEs**: Browser extensions rarely have formal CVEs, but check GHSA and
  NVD for the extension name and any bundled libraries.
- **Bundled library vulnerabilities**: Extensions often bundle copies of
  jQuery, React, or other libraries. If source is available, check bundled
  library versions against known CVEs.
- **Incident reports**: Search for malware reports, data exfiltration
  allegations, or acquisition-then-abuse patterns (extension sold to new
  owner who injects ads/malware).

### 4.4 Permissions & Access (browser-extension-specialized)

**This is the primary risk surface for browser extensions.** Score each
declared permission against the risk classification in
`references/criteria/browser-extension.md`:

- **Permission justification**: For each high-risk permission, does the
  extension's stated purpose require it? Document the justification or its
  absence.
- **Least privilege**: Could the extension function with fewer permissions?
  `activeTab` instead of `<all_urls>`? Specific host patterns instead of
  `*://*/*`? `declarativeNetRequest` instead of `webRequestBlocking`?
- **Content script scope**: How many pages can the extension inject into?
  Use the reach classification from the addendum.
- **Host permissions breadth**: Count the host patterns. 1–3 specific
  domains = scoped. 10+ domains or wildcards = broad. `<all_urls>` = maximum.
- **Optional vs required permissions**: Optional permissions requested at
  runtime are lower risk (user sees a prompt). Required permissions are
  granted silently at install.
- **MV2 powerful APIs**: If MV2, does the extension use
  `webRequestBlocking`, persistent background pages, or other APIs being
  removed in MV3? These are more powerful and less constrained.

### 4.5 Reliability & Compatibility (browser-extension-specialized)

- **Manifest version**: MV3 is current. MV2 is legacy — Chrome deprecation
  timeline is shifting but direction is clear. MV2 on Firefox is explicitly
  supported long-term.
- **Browser compatibility**: Does the extension work on the user's target
  browser? Cross-browser extensions (WebExtension API) are more broadly
  compatible.
- **Auto-update risk**: Extensions auto-update silently. Is the extension
  open source (updates auditable)? Has the extension changed ownership
  recently? See addendum for scoring.
- **Enterprise policy compatibility**: If the user's org manages browser
  extensions via policy, note any conflicts.

### 4.6 Alternatives (browser-extension-specialized)

- Are there alternative extensions with fewer permissions for the same
  purpose?
- Is there a built-in browser feature that eliminates the need for the
  extension?
- If the extension is closed-source, is there an open-source alternative?

## Subject Verdict Notes

Browser-extension-specific guidance for how findings map to verdicts. These
notes supplement the shared verdict tree in `SKILL.md` Step N — they do not
replace it.

### Toward REJECTED

Any one of these pushes strongly toward REJECTED:

- **Known malware / store removal for malicious behavior**: Extension was
  removed from any store for injecting ads, stealing data, cryptomining, or
  similar
- **Impossible permission justification**: Extension requests
  `<all_urls>` + `cookies` + `nativeMessaging` for a purpose that requires
  none of these (e.g., a color picker)
- **Sideloaded with no source or provenance**: .crx/.xpi from unknown origin,
  no store listing, no source code, no publisher identity
- **Recent acquisition + permission escalation**: Extension was acquired by
  new entity and simultaneously added high-risk permissions
- **Self-hosted updates from unknown server**: MV2 extension with
  `update_url` pointing to an unverified server (bypasses store review)

### Toward CONDITIONAL

These findings push toward CONDITIONAL (installation may proceed with listed
conditions):

- **Broad permissions with justification**: Extension's purpose requires
  broad access (ad blocker, password manager, dev tools) — Condition:
  understand and accept the access scope; re-audit on ownership changes
- **MV2 on Chrome**: Condition: monitor Chrome's MV2 deprecation timeline;
  identify MV3 alternative
- **Closed-source with broad permissions**: Condition: limit to a separate
  browser profile; monitor for incidents
- **Single developer with no org backing**: Condition: monitor for
  acquisition; re-audit if publisher changes
- **Stale but functional**: Condition: verify it still works on current
  browser version; identify alternatives if maintenance stops
- **3+ MEDIUM flags accumulated**: Cumulative risk triggers CONDITIONAL per
  shared verdict tree

### Toward APPROVED

All of the following support APPROVED:

- All tier-appropriate checks completed with no flags
- Listed on at least one major store with verification badge
- Permissions are proportional to stated purpose
- Publisher is identified (company or known individual/project)
- No known incidents or store removals
- MV3 manifest version (or MV2 on Firefox with Recommended badge)
- No content scripts, or content scripts scoped to relevant domains
- Open source (bonus, not required)

After completing the Subject Rubric and noting verdict-relevant findings,
**return to `SKILL.md` Step N** for the shared verdict tree, report
skeleton, and escalation guidance.
```

**Rationale:** The workflow mirrors registry-package.md's structure (proven in Phase 2) but replaces every registry-specific concept with its browser-extension equivalent: store listing replaces registry lookup, manifest permission analysis replaces dependency/install-script review, store badges replace npm verified publisher. The permission risk classification (§4.4) is deliberately the longest section — the framing eval identified this as the top gap.

**Verification:** File exists at `workflows/browser-extension.md`. Contains all four template sections. References `references/criteria/browser-extension.md` by path. Does not duplicate the Audit Coverage table or audit-confidence assertion (those stay in `SKILL.md` Step N).

**If this fails:** Delete the file. Step 1's addendum remains usable for future attempts.

---

### Step 3: Update `SKILL.md` dispatch table

**Objective:** Route Type 2 subjects to the new workflow instead of `generic.md`.
**Confidence:** High
**Depends on:** Step 2 (workflow file must exist)

**Files:**
- `SKILL.md`

**Changes:**

```markdown
// Before:
| 2 | browser-extension | `workflows/generic.md` | Fallback — specific workflow lands in Phase 3 (M3.1) |

// After:
| 2 | browser-extension | `workflows/browser-extension.md` | Live — Phase 3 (M3.1) |
```

Single line change in the dispatch table (around line 63 of `SKILL.md`).

**Rationale:** Mechanical wiring — the dispatch table is the sole routing mechanism.

**Verification:** Run grep for `browser-extension` in `SKILL.md` — should show `workflows/browser-extension.md` in the dispatch table, not `workflows/generic.md`. The signal table row (around line 35) remains unchanged.

**If this fails:** Revert the one line back to `workflows/generic.md`.

---

### Step 4: Update `evals/evals.json`

**Objective:** Update the Wappalyzer eval case for subject-type-aware routing and add new browser extension eval cases.
**Confidence:** High
**Depends on:** Steps 2–3 (workflow and dispatch must be wired)

**Files:**
- `evals/evals.json`

**Changes:**

**4a. Update Wappalyzer case (id 1):**

Add an assertion that the report identifies the subject type as browser-extension. Existing assertions remain compatible — the new workflow produces a superset of the expected findings.

```json
// Add to id 1 assertions array:
{"text": "Subject type is browser-extension", "type": "contains_concept"}
```

Update expected_output to reflect the new routing:

```json
// Before:
"expected_output": "Standard/Tier 2 audit. Should research permissions (broad URL access), note Wappalyzer is a known tool, and produce CONDITIONAL or APPROVED with permission caveats."

// After:
"expected_output": "Standard/Tier 2 audit. Routes to browser-extension workflow. Should analyze manifest permissions (broad URL access via host_permissions), note Wappalyzer is a known company/tool with CWS Featured status, and produce CONDITIONAL or APPROVED with permission caveats."
```

**4b. Add new eval case — malicious/suspicious browser extension (id 10):**

```json
{
  "id": 10,
  "prompt": "A coworker shared this Chrome extension link in Slack: 'YouTube Video Downloader Pro'. Should I install it?",
  "expected_output": "Tier 3 deep audit. Should flag: video downloaders are frequently policy-violating (CWS bans YouTube downloaders), shared via Slack (not discovered organically), likely requests broad permissions. Verdict should be REJECTED or CONDITIONAL with strong warnings.",
  "files": [],
  "assertions": [
    {"text": "Subject type is browser-extension", "type": "contains_concept"},
    {"text": "Report discusses permissions", "type": "contains_concept"},
    {"text": "Report flags the Slack source or direct sharing as risk", "type": "contains_concept"},
    {"text": "Verdict is REJECTED or CONDITIONAL", "type": "verdict_check"},
    {"text": "## Audit Coverage", "type": "contains_string"},
    {"text": "Audit confidence", "type": "contains_concept"}
  ]
}
```

**4c. Add new eval case — well-known extension quick audit (id 11):**

```json
{
  "id": 11,
  "prompt": "Is uBlock Origin safe to install on Firefox? I want an ad blocker.",
  "expected_output": "Tier 1 quick audit. Should recognize uBlock Origin as a well-known open-source ad blocker with AMO Recommended badge. Should note broad permissions are expected for an ad blocker (declarativeNetRequest/webRequest + broad host access). Verdict APPROVED.",
  "files": [],
  "assertions": [
    {"text": "Subject type is browser-extension", "type": "contains_concept"},
    {"text": "Report identifies uBlock Origin as well-known or trusted", "type": "contains_concept"},
    {"text": "Report notes permissions are expected for an ad blocker", "type": "contains_concept"},
    {"text": "Verdict is APPROVED", "type": "exact_match"},
    {"text": "Report is saved to a .md file", "type": "file_exists"},
    {"text": "Audit confidence", "type": "contains_concept"}
  ]
}
```

**Rationale:** The Wappalyzer update adds subject-type awareness without breaking existing assertions. The two new cases exercise opposite ends: a suspicious/likely-rejected extension (id 10) and a well-known quick-audit path (id 11). Together with Wappalyzer (id 1), this gives three browser-extension cases covering Tier 1, Tier 2, and Tier 3.

**Verification:** JSON parses without error (`python3 -c "import json; json.load(open('evals/evals.json'))"`). All three browser-extension cases (ids 1, 10, 11) have `browser-extension` in assertions. Total eval count = 12 (ids 0–11).

**If this fails:** Revert `evals/evals.json` to its pre-edit state. The workflow and dispatch table remain functional without the eval changes.

---

## Verification Plan

### Automated Checks

- [ ] `python3 -c "import json; json.load(open('evals/evals.json'))"` — JSON valid
- [ ] Grep: `SKILL.md` dispatch table row 2 → `workflows/browser-extension.md`
- [ ] Grep: no `Audit Coverage` or `audit-confidence` section in `workflows/browser-extension.md` (owned by dispatcher)
- [ ] File exists: `workflows/browser-extension.md`
- [ ] File exists: `references/criteria/browser-extension.md`

### Manual Verification

- [ ] Read `workflows/browser-extension.md` end-to-end — verify it follows Identify / Evidence / Subject Rubric / Subject Verdict Notes structure
- [ ] Verify the Wappalyzer eval case (id 1) assertions are still satisfiable by the new workflow's output
- [ ] Run a mental trace of the Wappalyzer audit through the new workflow — confirm all existing assertions can be met
- [ ] Verify `references/criteria/browser-extension.md` sections match the pattern in `references/criteria/registry-package.md`

### Acceptance Criteria Validation

| Criterion | How to Verify | Expected Result |
|-----------|---------------|-----------------|
| Workflow exists with correct template | Read file, check section headers | 4 template sections present |
| Criteria addendum exists | Read file, check structure | Layers on `references/criteria.md`, not standalone |
| Dispatch table routes correctly | Grep `SKILL.md` for `browser-extension` | Row 2 → `workflows/browser-extension.md`, status "Live" |
| Wappalyzer eval compatible | Trace assertions against workflow | All 6 assertions satisfiable |
| New eval cases added | Read `evals/evals.json`, count browser-extension cases | ≥3 total (ids 1, 10, 11) |
| No regressions | Existing eval assertions unchanged for ids 0, 2–9 | Byte-identical except id 1 |

---

## Rollback Plan

1. Delete `workflows/browser-extension.md`
2. Delete `references/criteria/browser-extension.md`
3. Revert `SKILL.md` dispatch table row 2 to `workflows/generic.md` (one line)
4. Revert `evals/evals.json` to pre-edit state (git checkout)

All four steps are independent — partial rollback is possible (e.g., keep the files but revert the dispatch table to continue routing to generic while iterating on the workflow).

---

## Notes

### Risks

- **Permission taxonomy completeness**: The manifest permission list in the criteria addendum covers the most common and dangerous permissions but is not exhaustive. Chrome adds new permissions over time. Mitigation: the "Medium-risk" and "Low-risk" tables can be extended incrementally; the scoring impact rules handle unlisted permissions via the "number of high-risk permissions" heuristic.
- **Wappalyzer eval regression**: The updated assertions add a `browser-extension` subject-type check. If the classifier routes Wappalyzer to `generic` instead (low confidence), this assertion fails. Mitigation: Wappalyzer's store URL (`chromewebstore.google.com/detail/...`) is a strong signal in the classifier's signal table — confidence should be high.
- **No script-assisted evidence gathering**: Unlike registry-package (which has `registry-lookup.ps1`, `typosquat-check.ps1`, `vuln-lookup.ps1`, `dep-scan.ps1`), browser extensions rely entirely on web search and manual manifest inspection. Mitigation: this is acceptable for M3.1 — a store-lookup script is a future enhancement (M3.x or Phase 6 stewardship), not a blocker.

### Open Questions

None — all questions resolved during research. The scope is well-defined by the nav milestone, the pattern is established by M2.1, and the browser-extension-specific content is grounded in the framing eval's gap analysis.
