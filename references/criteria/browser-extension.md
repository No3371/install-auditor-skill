# Browser Extension — Criteria Addendum

Per-subject scoring extensions for **Type 2: browser-extension** audits.
This addendum layers on top of the shared rubric in `references/criteria.md`.
When a criterion below conflicts with the shared rubric, the more specific
(browser-extension) guidance wins — except `references/criteria.md` §4.6
(version & update integrity), which this addendum only tightens or fills
(see "Version & Update Integrity (§4.6)" below).

Covers: Chrome Web Store, Firefox Add-ons (AMO), Microsoft Edge Add-ons,
and sideloaded .crx/.xpi files.

## Store Trust Signals

| Store | Badge (what it means) | Adoption Metric | Trust Notes |
|-------|-----------------------|-----------------|-------------|
| Chrome Web Store | "Featured" (Chrome team reviews listing quality, practices, privacy); "Established Publisher" (automatic: verified identity + policy record; most extensions have it) | User count + rating count | Review is not exhaustive; badged extensions have shipped malicious updates |
| Firefox Add-ons (AMO) | "Recommended" (staff security review; Mozilla documents a full review of each new version) | User count + daily active | Strongest store signal — the only badge that covers the version installed |
| Edge Add-ons | "Featured" (Microsoft quality badge, re-evaluated; partly automated). No "Certified" badge exists | User count | Smaller catalog; many extensions are CWS cross-posts |
| Sideloaded (.crx/.xpi) | None | None | No store verification — highest baseline risk |

### Scoring impact

- AMO "Recommended" = strong positive (equivalent to npm verified publisher)
- CWS "Featured" = moderate positive (human review of listing quality, not a security audit of each update)
- Edge "Featured" = moderate positive
- CWS "Established Publisher" alone = weak positive (identity only; does not qualify for Tier 1)
- No store listing (sideloaded) = strong negative (equivalent to installing from unknown npm mirror)
- Badges are identity/quality signals (`references/criteria.md` §4.6 V2): they never offset a §4.6 flag, a permission HIGH flag or a Red Flag

### Install path

- **Chrome / Edge (Windows, macOS):** off-store `.crx` installs only via enterprise policy. Drag-in `.crx` or Developer mode "Load unpacked" = outside store review → Tier 3; unpacked copies never auto-update (no security fixes).
- **Release Firefox** runs only Mozilla-signed add-ons; a self-distributed (unlisted) `.xpi` passed automated checks only → rate as no store listing.
- **Enterprise force-install** is legitimate; the policy's update source decides the version (§4.6 V5).

## Permission Risk Classification

### High-risk permissions

These grant broad or sensitive access. Any one of these triggers elevated scrutiny:

| Permission | Risk | Why |
|------------|------|-----|
| `<all_urls>` / `*://*/*` | Critical | Full read/write access to every page the user visits |
| `webRequestBlocking` (with `webRequest`) | Critical | Can intercept, modify, or block all HTTP traffic (MV2; in Chrome MV3 only for policy-installed extensions) |
| `webRequest` (observe only) | High | Sees every request URL and header on permitted hosts in MV2 and MV3 — telemetry/exfiltration channel |
| `scripting` | High | Injects JS/CSS into any permitted host at runtime; with broad hosts it equals `<all_urls>` content scripts |
| `userScripts` | High | Runs arbitrary script code supplied at runtime; Chrome 138+ also requires a per-extension "Allow User Scripts" toggle. Expected only for user-script managers |
| `cookies` | High | Read/write cookies for any permitted domain — session hijacking vector |
| `nativeMessaging` | High | Communicates with native executables on the host — breaks the browser sandbox |
| `debugger` | High | Full Chrome DevTools Protocol access to any tab — equivalent to `<all_urls>` + JS execution |
| `proxy` | High | Routes all browser traffic through an attacker-controlled proxy |
| `downloads` | High | Can silently download files to the user's filesystem |
| `tabCapture` / `desktopCapture` | High | Captures tab audio/video or the screen (desktop capture shows a picker) |
| `identity` | Medium-High | Obtains OAuth tokens for the scopes in the manifest's `oauth2` key — rate by those scopes |
| `history` | Medium-High | Full browsing history access — privacy-sensitive |
| `webNavigation` | Medium | Every navigation URL in every tab — history-equivalent |
| `declarativeNetRequestWithHostAccess` | Medium | Network rules that redirect or rewrite headers on permitted hosts |
| `privacy` | Medium | Changes browser privacy settings (e.g. WebRTC IP handling) |
| `bookmarks` | Medium | Full bookmark tree access — privacy-sensitive |
| `tabs` | Medium | Enumerate all open tabs with URLs and titles — privacy-sensitive and phishing enabler |
| `clipboardRead` | Medium-High | Reads anything copied, incl. passwords and tokens — credential theft vector |
| `clipboardWrite` | Medium | Replaces clipboard content — paste-jacking (swapped addresses or commands) |
| `management` | Medium-High | Can enable/disable/uninstall other extensions |

### Medium-risk permissions

| Permission | Risk | Why |
|------------|------|-----|
| `activeTab` (with broad `host_permissions`) | Medium | `activeTab` alone is low risk, but combined with broad host_permissions it grants tab access on click across many sites |
| `notifications` | Low-Medium | Can display system notifications — social engineering vector |
| `offscreen` | Low-Medium | Hidden document with DOM access — note when the extension also fetches remote config |
| `contextMenus` | Low | Adds right-click menu items — low risk alone |
| Host patterns (specific) | Varies | `*://*.google.com/*` is narrower than `<all_urls>` but still grants full page access on matched domains |

### Low-risk permissions

| Permission | Risk | Why |
|------------|------|-----|
| `activeTab` (alone, no broad hosts) | Low | Only activates on user click, only for the current tab |
| `storage` / `unlimitedStorage` | Low | Extension-local storage only; the risk comes from permissions that can read pages or send data |
| `alarms` | Low | Scheduling — no data access |
| `idle` | Low | Detects user idle state — minimal privacy impact |
| `theme` | Low | Visual customization only |
| `declarativeNetRequest` (MV3) | Low-Medium | Rule-based network filtering — less powerful than `webRequestBlocking` by design |

### Scoring impact

- 0 high-risk permissions → neutral
- Permissions rated Medium or lower are notes; one counts as a MEDIUM flag only when the stated purpose does not need it
- 1 high-risk permission with clear justification → note, not a flag
- 1 high-risk permission without justification → MEDIUM flag
- 2+ high-risk permissions → HIGH flag unless the extension's purpose requires them (ad and content blockers need `webRequest`/`webRequestBlocking` or `declarativeNetRequest`, `webNavigation`, `privacy` and broad host access)
- `<all_urls>` or `*://*/*` without clear purpose → HIGH flag
- `scripting` or `userScripts` with broad hosts → rate as `<all_urls>` content-script reach
- Network rules that strip `Content-Security-Policy` or `X-Frame-Options` response headers without a stated purpose → HIGH flag
- `nativeMessaging` on any extension that doesn't explicitly need host communication → CRITICAL flag

## Data Disclosure

- **CWS:** listing "Privacy practices" = developer-declared collection; store policy requires single-purpose, disclosed collection.
- **Firefox:** extensions new to AMO since 2025-11-03 declare `browser_specific_settings.gecko.data_collection_permissions` (`none` if nothing), shown at install and on AMO. Older extensions may lack it — no flag alone.
- Declared none while source or reports show page content, prompts, history or identifiers leaving the browser → HIGH flag (deceptive disclosure).

## Manifest Version (MV2 vs MV3)

Vendor timelines move: confirm the current status on the vendor's MV2 page and cite it.

| Browser | MV2 status (as of 2026-10) | Interpretation |
|---------|----------------------------|----------------|
| Chrome | Unsupported since Chrome 139 (138 was the last release where enterprise policy could keep MV2); remaining MV2 items removed from CWS on 2026-08-31 | An MV2 extension cannot run on current Chrome. A request to install one implies outdated Chrome, Developer mode, or an off-store copy |
| Edge | Retiring: consumer phase-out began Aug 2026 (target: end of 2026); managed devices from early 2027 | Time-boxed — plan the MV3 replacement now |
| Firefox | Supported (incl. blocking `webRequest`), no announced end | Not a risk signal |
| Chromium forks (Brave, Opera, Vivaldi, Arc) | Vendor-specific (e.g. Brave self-hosts a few MV2 blockers) | Rate per the fork's current statement |

A CWS removal caused by MV2 retirement is not a removal for cause (`SKILL.md` Red Flags).

### Scoring impact

- MV3 = neutral (expected)
- MV2 targeted at Chrome = HIGH flag `unsupported MV2` (no updates, no security fixes) + Tier 3. Condition: the publisher's MV3 edition (e.g. uBlock Origin Lite) or a browser that supports MV2
- MV2 on Edge = MEDIUM flag `MV2 retiring`. Recommendation names the MV3 edition and Microsoft's cut-off
- MV2 on a Chromium fork = MEDIUM flag unless the fork documents continued support
- MV2 on Firefox = LOW note (acceptable — Firefox committed to MV2 support)

## Content Script Reach

Content scripts inject JavaScript/CSS into web pages. Their reach is the
most direct measure of an extension's attack surface.

| Pattern | Reach | Risk |
|---------|-------|------|
| `"matches": ["<all_urls>"]` | Every page | Critical — equivalent to `<all_urls>` permission |
| `"matches": ["*://*.google.com/*", ...]` (few specific domains) | Scoped | Low-Medium — proportional to domain count and sensitivity |
| Matches on AI-chat (e.g. `chatgpt.com`, `claude.ai`, `gemini.google.com`), webmail, banking, password-manager or sign-in domains | Sensitive | High unless the stated purpose is that site — prompts, mail and credentials are readable |
| `"matches": ["*://*/*"]` with `"exclude_matches"` | Broad with exclusions | High — exclusions reduce reach but default is still all HTTP(S) |
| `"world": "MAIN"` | Page context | Medium — shares the page's JS context and can hook its functions |
| No content scripts | None | Neutral |
| `"match_about_blank": true` | Extends to about:blank iframes | Medium — can inject into iframes on pages |

### Scoring impact

- Content scripts on `<all_urls>` = HIGH flag (must be justified by extension purpose)
- Content scripts on a handful of specific domains = proportional to domain sensitivity
- No content scripts = positive signal (extension works via popup/background only)

## Remote Code & Config

MV3 bans remotely hosted code, but a server can still steer behavior: sleeper extensions stay benign for months, then switch on via an update or a config fetch.

- Periodic remote config deciding what is injected, redirected or collected, with broad hosts → HIGH flag
- Fetched strings reaching `eval`, `new Function`, `userScripts.register`, `scripting.executeScript` or injected `<script>` → HIGH flag; toward REJECTED when no stated purpose explains it
- Obfuscation beyond minification (string encoding, `eval` loaders, invisible Unicode, homoglyph identifiers) → HIGH flag

## Version & Update Integrity (§4.6)

Plug-ins for `references/criteria.md` §4.6. Missing bullets → shared default.

- **V1** — Publish time: CWS listing "Updated" + "Version"; AMO version history; Edge listing; repo release tags as cross-check. Stores show dates, not times: "Updated" within the last 3 days counts as < 72 h. Version unit: the version string per store. No consumer cooldown exists — `fresh version` condition: wait until 72 h, then re-check; managed fleets may pin the previous version (V5).
- **V2** — Identity: store publisher account; expected identity = the vendor's own site or repo linking to this exact extension ID; badges per Store Trust Signals. Store package signatures (CRX3, AMO signing) prove the store served the file, not who wrote it. A brand-named listing whose brand site does not link to this ID → MEDIUM flag (impersonation).
- **V3** — Diff vs the prior version: permissions, host permissions, `content_scripts.matches`, `externally_connectable`, CSP, network rules, `update_url`. Sources: manifest at repo tags; older XPIs in AMO version history; closed-source CWS items: listing permissions + reviews reporting a new-permission prompt (Chrome disables an update until the user accepts new warnings). Ownership transfer (sale, developer name / website / contact domain change) → HIGH flag + Tier 3; plus a permission increase or new remote-config endpoint → toward REJECTED.
- **V4** — Incident sources: store takedowns (CWS malware disablement, Mozilla add-on blocklist, Edge removal); vendor reports naming the extension ID. MV2-retirement or inactivity removals are not compromises.
- **V5** — Consumer browsers auto-update store extensions; users cannot hold a version — say so and list triggers. Managed fleets: Chrome Enterprise version pin (Admin console); `ExtensionSettings` allow/block + `override_update_url` (Chrome, Edge); Firefox enterprise `ExtensionSettings`. Non-store, non-enterprise update URL (`update_url` in Chrome manifests; `browser_specific_settings.gecko.update_url` in Firefox) → HIGH flag: updates bypass store review. Triggers: new-permission prompt | developer / website / contact change | privacy-practices or `data_collection_permissions` change | badge removed.

## CVE Scope (§4.3)

- **Own code** = the extension's scripts, pages, service worker. **Third-party component** = bundled libraries (jQuery, React, SDKs) and WASM from other projects.
- Sources: GHSA, NVD, CISA KEV for the extension name; bundled-library versions from source or the unpacked package. Extension CVEs are rare — absence is not evidence.

## Tier Assignment Thresholds (Browser Extensions)

### Tier 1 — Quick Audit

ALL of these must hold:
- User count ≥ 100K on primary store
- AMO Recommended, CWS Featured or Edge Featured badge (Established Publisher alone does not count)
- Publisher is a known company or well-known open-source project
- No `<all_urls>` or `*://*/*` unless the extension's purpose is inherently
  broad (ad blocker, password manager, dev tools — and even then, note it)
- MV3 manifest version (or MV2 on Firefox with AMO Recommended)
- No known incidents or store removals in search results (a removal for MV2 retirement or inactivity does not count — § Manifest Version)
- Extension has been listed ≥ 1 year
- `references/criteria.md` §4.6 allows Tier 1 (version ≥ 7 days old, no V3 item, no past compromise)

### Tier 2 — Standard Audit (default)

Default when not all Tier 1 criteria are met:
- User count 1K–100K
- Identifiable publisher
- No known security incidents
- Listed > 30 days

### Tier 3 — Deep Audit

ANY of these triggers:
- User count < 1K
- No store listing (sideloaded .crx/.xpi, unlisted self-distributed .xpi, Developer mode "Load unpacked")
- Publisher unknown or anonymous
- `<all_urls>` + `cookies` or `webRequest` without obvious justification
- `userScripts` or `debugger` outside an extension whose purpose needs them
- Extension shared via direct link / chat (not store URL)
- Recent ownership transfer or developer change
- Known prior removal or policy violation from any store (an MV2-retirement or inactivity removal does not count)
- MV2 targeted at Chrome (unsupported)
- `nativeMessaging` permission present
- Self-hosted update URL
- A V3 HIGH item or a remote-config pattern from "Remote Code & Config"
