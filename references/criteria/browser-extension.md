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
