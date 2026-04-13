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
- **MV2 powerful APIs**: If MV2, does the extension use `webRequestBlocking`,
  persistent background pages, or other APIs being removed in MV3? These are
  more powerful and less constrained.

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
