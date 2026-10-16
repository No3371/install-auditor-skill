# Browser-Extension Rubric Refresh

> **Status:** Complete
> **Completed:** 2026-10-16
> **Walkthrough:** 2610162006-browser-extension-rubric-refresh-walkthrough.md
> **Log:** 2610162006-browser-extension-rubric-refresh-log.md
> **Author:** Claude (Opus)
> **Parent:** 2610161927-browser-extension-ide-plugin-stewardship-review-eval.md
> **Source:** 2610161927-browser-extension-ide-plugin-stewardship-review-eval.md (F1, F2, F4, F5, F6, F7, F8, F11-storage; F10 → eval plan) | shared contract 2610161941-shared-version-integrity-floor-plan.md (Hand-off row "browser-extension / ide-plugin") | human decision C6 (via orchestrator)
> **Related Projex:** 2610161941-shared-version-integrity-floor-plan.md (contract; landed on base as `20843cc`) | 2610162003-ide-plugin-rubric-refresh-plan.md (sibling; no file overlap) | 2610162004-container-image-rubric-refresh-plan.md (owns Docker lines in `criteria.md` §4.4) | 2604141200-browser-extension-workflow-m31-plan.md (original authoring) | 2604170511-measure-read-cost-f7-m53-findings.md (read-cost baseline)
> **Worktree:** Yes

---

## Summary

Refresh the browser-extension rubric to the 2026-10 ecosystem and plug it into the shared version-integrity floor (`references/criteria.md` §4.6). The addendum gains a `## Version & Update Integrity (§4.6)` plug-in (V1–V5) and a `## CVE Scope (§4.3)` plug-in, so a badged, high-install extension that ships one bad update no longer reaches Tier 1 / APPROVED (ShadyPanda, QuickLens, Cyberhaven shape). It also fixes stale facts: Chrome MV2 is unsupported, not "deprecating"; Edge's badge is "Featured", not "Certified"; CWS "Featured" is manual and "Established Publisher" exists; `update_url` attribution was wrong; crxcavator is no longer named. It adds the MV3 injection/observation permissions (`scripting`, `userScripts`, observe-only `webRequest`, `identity`, capture APIs, …), AI-chat content-script reach, data-disclosure checks (CWS Privacy practices, Firefox `data_collection_permissions`), the remote-config sleeper pattern, and enterprise update controls. The shared `references/criteria.md` §4.4 browser sub-table is realigned row-for-row with the addendum (observe-only `webRequest` split from blocking; `history`, `downloads`, `tabs`, `<all_urls>`, `storage` ratings match), so no disagreement is left to precedence.

**Scope:** `references/criteria/browser-extension.md` (rewrite) | `workflows/browser-extension.md` (21 exact replacements) | `references/criteria.md` §4.4 browser sub-table (11 rows + 1 pointer sentence; Docker lines untouched).
**Estimated Changes:** 3 files. Addendum 8,565 → 15,641 B; workflow 17,250 → 18,471 B; `criteria.md` 21,455 → 22,035 B.

---

## Objective

### Problem / Gap / Need

| ID (eval) | Gap | Fix (where) |
|---|---|---|
| F1 / A1 | Tier 1 has no version-level check; "Auto-Update Risk" treats updates as uncontrollable; ownership transfer rated CRITICAL in one table and MEDIUM-HIGH in another | Addendum `## Version & Update Integrity (§4.6)` V1–V5; Tier 1 bullet "§4.6 allows Tier 1"; ownership transfer = HIGH + Tier 3 (one rule); workflow coverage row `Version integrity (§4.6)` |
| F2 / A2 | MV2 "Chrome deprecating"; MV2-on-Chrome = MEDIUM EOL note; Tier 3 trigger "MV2 + `webRequestBlocking` on Chrome" unreachable; verdict condition "monitor timeline" | Addendum MV2 table per browser (Chrome unsupported → HIGH + Tier 3; Edge retiring → MEDIUM; Firefox → LOW; forks per vendor); MV2-retirement removal ≠ "Removed for cause"; workflow Verdict Notes |
| F4 / A3 | Edge "Certified" doesn't exist; CWS Featured called "algorithmic"; Established Publisher missing; badges over-weighted | Addendum Store Trust Signals rewrite + "never offset a §4.6 flag"; Tier 1 badge list excludes Established Publisher alone; workflow Identify + 4.1 |
| F5 / A5 | Permission table misses `scripting`, `userScripts`, observe-only `webRequest`, `declarativeNetRequestWithHostAccess`, `webNavigation`, `identity`, `tabCapture`/`desktopCapture`, `privacy`, `offscreen`; `storage` Medium vs shared LOW | Addendum permission rows + scoring bullets (injection APIs = `<all_urls>` reach; CSP-stripping rules → HIGH); `storage` → LOW in both files |
| F6 / A6 | No AI-chat reach or data-flow check; CWS 2026 data policy; Firefox data consent | Addendum content-script row "Sensitive" (AI-chat/webmail/banking/sign-in) + `## Data Disclosure`; workflow research Q8 |
| F7 / A7 | Conditions say "monitor" while enforceable controls exist | Addendum V5 (Chrome Enterprise version pin, `ExtensionSettings`, `override_update_url`, Firefox `ExtensionSettings`); workflow CONDITIONAL bullets |
| F8 / A8 | crxcavator named; `update_url (MV2 Firefox)` wrong; sideload realities missing; obfuscation guidance thin | Addendum `### Install path` + `## Remote Code & Config`; workflow manifest sources/keys, source review |
| C6 (human) | Shared §4.3 Blocking CVE needs the own-code line per artifact type | Addendum `## CVE Scope (§4.3)`; workflow 4.3 adds CISA KEV |
| F11 (§4.4 matrix) | `criteria.md` §4.4 browser matrix disagrees with the addendum: `storage` LOW vs Medium, `webRequest` + `<all_urls>` "Full MITM" (wrong for observe-only MV3), `<all_urls>`, `history`, `downloads`, `tabs` | Step 3 replaces the sub-table; ratings copied from the addendum; script asserts row equality |

### Success Criteria

- [ ] Preflight confirms the shared floor on base: `## 4.6 Version & Update Integrity (shared floor)`, `### V1`–`### V5` headings, 6 `- **Addendum:**` lines, `Blocking CVE` in `SKILL.md`, and the Red Flag "Confirmed supply chain compromise".
- [ ] `references/criteria/browser-extension.md` is byte-identical to the Step 1 block (sha256 check) and has exactly one `## Version & Update Integrity (§4.6)` heading with bullets `**V1**`…`**V5**`, plus `## CVE Scope (§4.3)`.
- [ ] Stale strings gone from both subject files (case-insensitive): `Edge "Certified"` | `"Certified" publisher` | `algorithmic` | `crxcavator` | `(MV2 Firefox)` | `deprecating` | `deprecation timeline` | MV2-with-`webRequestBlocking`-on-Chrome trigger. (The addendum's `No "Certified" badge exists` is intended.)
- [ ] Required new strings present: addendum has `` `scripting` ``, `` `userScripts` ``, `` `webRequest` (observe only) ``, `Established Publisher`, `data_collection_permissions`, `unsupported MV2`, `2026-08-31`, `Remote Code & Config`; workflow has `| Version integrity (§4.6) | Required | Required | Required |`, `gecko.update_url`, `CISA KEV`.
- [ ] `references/criteria.md` §4.4 browser sub-table equals the Step 3 block: 11 rows, each with the same rating (case-insensitive) as the identically named addendum row; pointer sentence present. Only the browser sub-table changed in `criteria.md` (Docker/runtime lines untouched).
- [ ] Every `§4.6 V<n>` and `§4.3` reference in the 2 subject files names an existing heading in `references/criteria.md`.
- [ ] Sizes: addendum ≤ 15,800 B; workflow ≤ 18,600 B; workflow lines ≤ 79 columns except lines already longer at base.
- [ ] `python3 evals/run_evals.py validate` passes; `python3 -m unittest discover -s evals -p "test_*.py"` passes with the Preflight count (12 at planning).
- [ ] Paper traces T1–T10 produce the stated verdicts.
- [ ] Planning simulation: applying Steps 1–3 from this document's own blocks to a copy of base `20843cc` reproduced all three sha256 values (addendum, workflow, `criteria.md`), the consistency script (incl. §4.4 row equality) printed `OK`, and the `criteria.md` diff touched only the browser sub-table; harness green (in a git checkout — `prepare` tests read git state).
- [ ] `git diff --stat <base>..HEAD` lists exactly the 3 files (+ this plan's log); `evals/` untouched.

### Out of Scope

- `evals/evals.json` and new eval cases (F10) → eval-refresh plan; list in Notes → Eval hand-off.
- `references/criteria.md` §4.4 Docker lines (container plan), §4.3/§4.6 (shared plan, done).
- `references/registries.md` browser rows; `SKILL.md`; `references/classifier.md`; `STEWARDSHIP.md` (inventory dates are the orchestrator's).
- IDE-plugin files (sibling plan). Safari Web Extensions and Chromium-fork depth (F9: deferred).
- Live `run_evals.py run` (one paid run after all refreshes — not here).

---

## Context

### Current State

- `references/criteria/browser-extension.md` (8,565 B, authored 2026-04-14, unchanged since except `5c44b79` comment strip): Store Trust Signals (Edge "Certified", CWS Featured "algorithmic"), Permission Risk Classification (no MV3 injection APIs; `storage` Medium), MV2 table ("Chrome deprecating"), Content Script Reach, Auto-Update Risk ("no user-side mechanism"; ownership CRITICAL vs MEDIUM-HIGH; `update_url` "MV2 Firefox"), Tier thresholds (no version check; "MV2 with `webRequestBlocking` on Chrome"). Header: "more specific (browser-extension) guidance wins" — no §4.6 exception.
- `workflows/browser-extension.md` (17,250 B, wraps at ≤ 79 columns): Identify / Triage / Research / Subject Rubric 4.1–4.6 / Verdict Notes. Names crxcavator; badge line repeats "Certified"/"algorithmic"; coverage table has "Auto-update risk | Tier-skip | Note | Required" and no Version integrity row; MV2 condition "monitor Chrome's MV2 deprecation timeline".
- `references/criteria.md` (21,455 B on base `20843cc`): §4.4 browser matrix line `` | `storage` | LOW | Local extension storage only | ``; §4.6 V1–V5 with `**Addendum:**` lines; §4.3 Blocking CVE table + `**Addendum:**` own-code line; §4.1 badge = identity note; canonical row `Version integrity (§4.6)` Required at every tier.
- `SKILL.md` (15,484 B): Precedence names §4.6 as a floor addenda only tighten; Red Flag "Removed for cause" excludes non-security removals; "Confirmed supply chain compromise" scoped by V4; tree: single MEDIUM ≠ CONDITIONAL (needs 3+), any HIGH → CONDITIONAL.
- Evals: 1 (Wappalyzer/Chrome → `[APPROVED, CONDITIONAL]`), 10 (YouTube Video Downloader Pro via Slack → `[CONDITIONAL, REJECTED]`), 11 (uBlock Origin/Firefox → exact `APPROVED`).

### Verified facts (2026-10-16 web search; primary where noted)

| Fact | Source | Confidence |
|---|---|---|
| Chrome 139+ has no MV2; 138 was the last with the enterprise policy; CWS removed remaining MV2 items 2026-08-31 (incl. uBlock Origin) | developer.chrome.com MV2 timeline (search summary) + 9to5Google, CyberInsider, AlternativeTo | High |
| Edge consumer MV2 phase-out began Aug 2026, target end-2026; managed devices Jan–Apr 2027 with `ExtensionManifestV2Availability` | Microsoft quote via PCWorld; M365 message center MC1467356; Windows Report | Medium-High (no Learn page retrieved) |
| CWS "Featured" = manual review by Chrome team (practices, UX, privacy); "Established Publisher" = automatic (verified identity + policy record), ~75 % of extensions | developer.chrome.com/docs/webstore/discovery | High (primary) |
| Edge badge = "Featured", re-evaluated periodically; newer docs describe automated signals; no "Certified" found | learn.microsoft.com Edge extensions overview (versions differ) | Medium-High |
| AMO Recommended: every new version gets full technical review before appearing on AMO | extensionworkshop.com Recommended Extensions (support article is vaguer) | Medium-High |
| Firefox `browser_specific_settings.gecko.data_collection_permissions` required for new extensions from 2025-11-03; existing add-ons exempt initially; H1 2026 extension to all was planned | blog.mozilla.org/addons 2025-10-23; extensionworkshop.com | High (2026 extension unverified) |
| Chrome 138+ `userScripts` needs per-extension "Allow User Scripts" toggle | developer.chrome.com/blog/chrome-userscript | High (primary) |
| CWS policy update (published 2026-07-01, enforced 2026-08-01): single-purpose data minimization, disclosure incl. post-install changes, ban on bypassing AI-service safeguards | developer.chrome.com/blog/cws-policy-updates-2026 + CyberInsider | High |
| Chrome Enterprise can pin an extension version (Admin console); `ExtensionSettings.override_update_url` self-hosts updates | developer.chrome.com extensions update lifecycle; support.google.com/chrome/a | High |
| Brave self-hosts a few MV2 blockers (uBO, AdGuard, uMatrix, NoScript) | BetaNews, PiunikaWeb, Brave community | Medium |
| CRXcavator offline (one blog says 2023, Cisco/Duo) | thenextgennexus.com (single, vendor-adjacent) | Low → rubric no longer names any specific viewer |

### Key Files

| File | Role | Change Summary |
|------|------|----------------|
| `references/criteria/browser-extension.md` | Browser scoring addendum | Rewrite (Step 1): badges, install path, permissions, data disclosure, MV2, AI reach, remote config, §4.6 + §4.3 plug-ins, tiers |
| `workflows/browser-extension.md` | Browser workflow | 21 exact replacements (Step 2): identity/version, triage, research Q6/Q8, manifest sources/keys, coverage row, 4.1/4.3/4.4/4.5, verdict notes |
| `references/criteria.md` | Shared rubric | §4.4 browser sub-table realigned to the addendum (Step 3) |

### Dependencies

- **Requires:** 2610161941-shared-version-integrity-floor-plan.md closed on base (landed as `20843cc` during planning; Preflight re-checks).
- **Concurrent:** sibling refresh plans (ide-plugin, container-image, ci-action, generic, …). File overlap: only `references/criteria.md` — container plan edits §4.4 Docker lines; this plan replaces the §4.4 browser matrix. Different hunks; rebase if either closes first.
- **Blocks:** eval-refresh plan (browser cases), orchestrator STEWARDSHIP inventory update.

### Constraints

- §4.6 is a floor: the plug-in may tighten (3-day date rule, ownership HIGH, Tier 3 triggers), never loosen.
- Read cost: the browser path was already +108 % vs generic (2604170511-measure-read-cost-f7-m53-findings.md). Growth here (+8.2 KB across 2 files) is bounded by the size criteria; the workflow defers detail to the addendum instead of restating it.
- Preserve parsed strings: the workflow's `### Audit coverage tracking` is guidance, not the dispatcher's `## Audit Coverage` (M3.1 walkthrough Issue 1).
- Platform dates live only in the addendum MV2 table ("as of 2026-10") and Data Disclosure — one place to update next pass.
- No projex filenames in shipped files.

### Assumptions

- **A1:** Shared floor text on base equals the landed `20843cc` (verified at planning). Preflight stops if the §4.6 heading or V headings changed.
- **A2:** Chrome/Edge on Windows and macOS block off-store `.crx` installs except via enterprise policy or Developer mode (prior knowledge, Medium-High; not re-verified for Edge). If wrong, only the `### Install path` first bullet needs softening.
- **A3:** In Chrome MV3, `webRequestBlocking` is available only to policy-installed extensions (prior knowledge, Medium-High). Wording sits in one table cell.
- **A4:** Chrome disables an updated extension until the user accepts new permission warnings (long-standing behavior, High).
- **A5:** No eval assertion checks badge names, MV2 wording, or permission table rows (verified: assertions for 1/10/11 are concept/verdict checks only).
- **A6:** Eval 11 (uBO/Firefox, exact APPROVED) stays reachable: uBO's permissions are covered by the ad/content-blocker justification bullet (`webRequest`/`webRequestBlocking`, `webNavigation`, `privacy`, broad hosts) and the "Medium-or-lower are notes" bullet (`tabs`). Time dependence (uBO releases often → V1) is already in the shared plan's eval hand-off.

### Impact Analysis

- **Direct:** the 3 files.
- **Adjacent:** `SKILL.md` Red Flags "Removed for cause" / "Excessive permissions" unchanged but now read alongside the MV2-removal carve-out; classifier routing unchanged.
- **Downstream:** live browser audits change:
  - Store version "Updated" within 3 days → CONDITIONAL (wait 72 h); within 7 days → no Tier 1.
  - CWS listing with only "Established Publisher" → no Tier 1 (Tier 2 can still APPROVE).
  - MV2 for Chrome → HIGH + Tier 3 → CONDITIONAL (MV3 edition); Edge MV2 → MEDIUM.
  - `scripting`/`userScripts`/observe-only `webRequest` now rated; ad blockers stay justified.
  - Ownership transfer → HIGH + Tier 3 (was CRITICAL in one table) — CONDITIONAL rather than auto-REJECTED unless combined with a permission increase / remote config.

---

## Implementation

### Overview

Preflight → Step 1 replace the addendum with the exact block → Step 2 apply 21 exact `old → new` pairs to the workflow (each old string occurs once at base, simulated) → Step 3 replace the §4.4 browser sub-table of `criteria.md` (exact block). Use Edit per pair. A miss means the base moved: re-read that region and re-anchor; don't improvise wording.

**Preflight (`<work-root>`):**
```bash
grep -c "^## 4\.6 Version & Update Integrity (shared floor)" references/criteria.md   # 1
grep -c "^### V[1-5] " references/criteria.md                                       # 5
grep -c "^- \*\*Addendum:\*\*" references/criteria.md                              # 6
grep -c "Blocking CVE" SKILL.md                                                    # ≥ 1
grep -c "Confirmed supply chain compromise" SKILL.md                               # ≥ 1
grep -c '| `storage` | LOW | Local extension storage only |' references/criteria.md  # 1
wc -c references/criteria/browser-extension.md workflows/browser-extension.md      # 8565 / 17250
awk 'length>79' workflows/browser-extension.md | wc -l                            # 3 (pre-existing)
python3 evals/run_evals.py validate | tail -2                                      # pass
python3 -m unittest discover -s evals -p "test_*.py" 2>&1 | tail -3                # record count (12)
```
Any mismatch in the first five → stop: the shared floor is not on base as assumed (A1). Size mismatch on the subject files → a sibling touched them: re-read and re-anchor before Step 2.

---

### Step 1: Rewrite `references/criteria/browser-extension.md`

**Objective:** deliver the browser plug-ins for §4.6 (V1–V5) and §4.3, and fix badges, MV2, permissions, AI reach, data disclosure, install path and remote-config rules.
**Confidence:** High (structure, permission facts); Medium-High (Edge dates, AMO per-version review — hedged in text)
**Depends on:** Preflight
**Do-Projex:** Encouraged
**Verify-Projex:** Encouraged

**Files:** `references/criteria/browser-extension.md`

**Changes:** replace the whole file with the block below (sections kept: Content Script Reach scoring, Tier 2; all others rewritten or added). Section order: header → Store Trust Signals (+ Install path) → Permission Risk Classification → Data Disclosure → Manifest Version → Content Script Reach → Remote Code & Config → Version & Update Integrity (§4.6) → CVE Scope (§4.3) → Tier Assignment Thresholds.

```
// Before: current file (8,565 B; sha256 at base = aea934ae5c4a42b3371f3f394300612eaf8f0342eec0ea51cfb9194a12719947)
// After (15,641 B; sha256 = 588866ba9615efd0e0daaaf9b8b2db7eee01eef4980c177e31cffa91939a04a8):
```

````markdown
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
- No known incidents or store removals in search results
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
- Known prior removal or policy violation from any store
- MV2 targeted at Chrome (unsupported)
- `nativeMessaging` permission present
- Self-hosted update URL
- A V3 HIGH item or a remote-config pattern from "Remote Code & Config"
````

**Rationale:**
- **One §4.6 plug-in section, V-labelled bullets** — the shared contract's required shape. "Auto-Update Risk" is folded in (its open-source and self-hosted rows become V3 sources and the V5 HIGH flag), removing the CRITICAL vs MEDIUM-HIGH ownership contradiction.
- **3-day date rule (V1)** — stores show dates, not times, so "Updated" within 3 days is the conservative reading of < 72 h; a tightening the floor allows. Consumers cannot install a previous store version, so the condition is "wait", not "install the previous release".
- **Badges capped, not removed** (eval steel-man): AMO Recommended stays strongest (per-version review per Mozilla's developer docs); Established Publisher alone no longer opens Tier 1 because ~75 % of CWS extensions carry it.
- **MV2 by browser** — Chrome MV2 cannot run on current Chrome, so HIGH + Tier 3 with an MV3-edition condition; Edge MEDIUM (single MEDIUM ≠ CONDITIONAL in the tree, so it's a Recommendation item); the MV2-removal ≠ "Removed for cause" sentence prevents a false Red Flag on uBO-style subjects.
- **`storage` → LOW** — Chrome shows no install warning for it; the risk is what else the extension can read or send, which the other rows rate.
- **`clipboardRead` split from `clipboardWrite`** — read = Medium-High (copied passwords/tokens; matches the shared row and the "reads clipboard" Red Flag), write = Medium (paste-jacking).
- **Dates hedged** — the MV2 table says "as of 2026-10" and tells the auditor to confirm and cite the vendor page; Edge "Featured" says "partly automated" (Microsoft's docs disagree across versions).
- **No crxcavator** — unverifiable status; the rubric names AMO version history (primary) and "a CRX download/viewer tool (label as secondary)".
- **Rejected alternatives:** (a) per-section edit pairs — 9 of 10 sections change, so pairs would be longer and riskier than one exact block; (b) moving permission rows into `criteria.md` — §4.4 shared matrix is not this plan's to restructure.

**Verification:**
```bash
sha256sum references/criteria/browser-extension.md          # = 588866ba9615efd0e0daaaf9b8b2db7eee01eef4980c177e31cffa91939a04a8
wc -c < references/criteria/browser-extension.md            # 15641 (≤ 15800)
grep -c "^## Version & Update Integrity (§4.6)$" references/criteria/browser-extension.md   # 1
grep -c "^- \*\*V[1-5]\*\* — " references/criteria/browser-extension.md                     # 5
grep -c "^## CVE Scope (§4.3)$" references/criteria/browser-extension.md                   # 1
grep -ci "edge \"certified\"\|\"certified\" publisher\|algorithmic\|crxcavator\|(MV2 Firefox)\|deprecating" references/criteria/browser-extension.md   # 0
```

**If this fails:** `git -C <work-root> checkout -- references/criteria/browser-extension.md`, then re-write the block exactly.

---

### Step 2: Update `workflows/browser-extension.md` (21 exact replacements)

**Objective:** make the workflow collect version age and diff, name correct badges, sources and manifest keys, carry the Version integrity coverage row, defer scoring detail to the addendum, and fix the Verdict Notes.
**Confidence:** High
**Depends on:** Step 1 (pointers must resolve)
**Do-Projex:** Encouraged
**Verify-Projex:** Encouraged

**Files:** `workflows/browser-extension.md`

**Changes:** apply in order; each `Before` occurs exactly once at base (simulated). Keep wrapping ≤ 79 columns.

**2a** (Identify §2 — version + badges)

````markdown
// Before:
- **Version**: Current store version (extensions auto-update; users rarely
  pin versions)
- **Store badges**: Chrome "Featured", Firefox "Recommended", Edge "Certified"
// After:
- **Version**: Current store version **and its "Updated" date** — needed
  for `references/criteria.md` §4.6 V1 (extensions auto-update; consumers
  cannot pin versions)
- **Store badges**: Chrome "Featured" / "Established Publisher", Firefox
  "Recommended", Edge "Featured" — meanings in the addendum
````

**2b** (Identify §3 item 5)

````markdown
// Before:
5. **Target browser** — Chrome, Firefox, Edge, Brave, Arc, etc.
// After:
5. **Target browser** — Chrome, Firefox, Edge, Brave, Arc, etc. (MV2 runs
   only where the browser still supports it — see addendum)
````

**2c** (Triage gather list)

````markdown
// Before:
- First listed date (if available from store or web archive)
// After:
- First listed date (if available from store or web archive)
- Current version, its "Updated" date, and any publisher / website change
  (§4.6 V1, V3)
````

**2d** (Tier 1 text)

````markdown
// Before:
Use when ALL Tier 1 criteria from the addendum are met: ≥100K users, store
badge, known publisher, reasonable permissions for stated purpose, MV3 (or
MV2 on Firefox with Recommended), no incidents, listed ≥1 year.

**Quick audit scope:** Confirm store presence + badge, note permissions at
a glance, check for recent incidents, verify publisher. No deep manifest
analysis. If everything checks out, proceed directly to Subject Verdict
Notes with minimal ceremony.
// After:
Use when ALL Tier 1 criteria from the addendum are met, including the
`references/criteria.md` §4.6 bars (version ≥ 7 days old, no continuity
break, no past compromise).

**Quick audit scope:** Confirm store presence + badge, version age,
permissions at a glance, recent incidents, publisher. No deep manifest
analysis. If everything checks out, proceed directly to Subject Verdict
Notes with minimal ceremony.
````

**2e** (Tier 3 text)

````markdown
// Before:
Any Tier 3 trigger from the addendum: low users, sideloaded, unknown
publisher, dangerous permission combinations, ownership change, prior
removal, self-hosted updates, `nativeMessaging`.
// After:
Any Tier 3 trigger from the addendum (e.g. sideloaded or Developer mode
install, ownership change, MV2 targeted at Chrome, remote-config pattern,
`nativeMessaging`).
````

**2f** (Research Q6–Q8)

````markdown
// Before:
6. **What is the update cadence?** Frequent updates = active maintenance.
   No updates in >1 year = stale but not necessarily dangerous (simple
   extensions may not need updates).
7. **Is the source code available?** Open-source extensions can be audited;
   closed-source cannot. Note the repo URL if available.
// After:
6. **What is the update cadence, and what changed in this version?**
   Frequent updates = active maintenance; no updates in >1 year = stale but
   not necessarily dangerous. Record version age + diff (addendum V1/V3).
7. **Is the source code available?** Open-source extensions can be audited;
   closed-source cannot. Note the repo URL if available.
8. **Where does page data go?** For extensions reading pages or AI-chat
   prompts, compare observed endpoints with declared data practices
   (addendum "Data Disclosure").
````

**2g** (Manifest sources)

````markdown
// Before:
- Chrome Web Store source viewer (crxcavator.io or similar)
- `about:debugging` in Firefox → inspect installed extension → manifest
- Direct .crx/.xpi download + unzip (ZIP format)
// After:
- AMO version history (current and prior XPIs — also feeds the V3 diff);
  for CWS, a CRX download/viewer tool (third-party — label as secondary)
- `about:debugging` in Firefox → inspect installed extension → manifest
- Direct .crx/.xpi download + unzip (ZIP format; CRX adds a header)
````

**2h** (Manifest key: content_scripts)

````markdown
// Before:
- `content_scripts` → `matches` — which pages get injected JS/CSS
// After:
- `content_scripts` → `matches` (and `world`) — which pages get injected
  JS/CSS, and whether it runs in the page's own context (`"MAIN"`)
````

**2i** (Manifest keys: CSP → update_url)

````markdown
// Before:
- `content_security_policy` — custom CSP (relaxed CSP = risk signal)
- `update_url` (MV2 Firefox) — self-hosted update server (bypasses store
  review)
// After:
- `content_security_policy` — custom CSP (relaxed CSP = risk signal)
- `declarative_net_request` rules — header rewrites (e.g. CSP removal)
- `oauth2.scopes` — what `identity` can obtain
- `update_url` (Chrome) / `browser_specific_settings.gecko.update_url`
  (Firefox) — a non-store update server bypasses store review
- `gecko.data_collection_permissions` (Firefox) — declared data collection
````

**2j** (Source review: obfuscation)

````markdown
// Before:
- Obfuscation: Is the code minified/obfuscated? Minification is normal for
  build output; heavy obfuscation (eval-based, string encoding) in a
  browser extension is a red flag.
// After:
- Remote config and obfuscation: rate per addendum "Remote Code &
  Config" (minification is normal; eval loaders, string encoding, invisible
  Unicode are not).
````

**2k** (Coverage table row)

````markdown
// Before:
| Auto-update risk | Tier-skip | Note | Required |
// After:
| Version integrity (§4.6) | Required | Required | Required |
````

**2l** (4.1 Store badge)

````markdown
// Before:
- **Store badge**: Firefox "Recommended" (strongest signal — human review),
  Chrome "Featured" (moderate — algorithmic), Edge "Certified" (moderate).
// After:
- **Store badge**: rate per addendum "Store Trust Signals"; badges never
  offset a version-level flag (§4.6 V2).
````

**2m** (4.3 CVEs)

````markdown
// Before:
- **CVEs**: Browser extensions rarely have formal CVEs, but check GHSA and
  NVD for the extension name and any bundled libraries.
// After:
- **CVEs**: Browser extensions rarely have formal CVEs, but check GHSA,
  NVD and CISA KEV for the extension name and any bundled libraries
  (own-code line: addendum "CVE Scope (§4.3)").
````

**2n** (4.4 MV2 APIs → injection APIs)

````markdown
// Before:
- **MV2 powerful APIs**: If MV2, does the extension use `webRequestBlocking`,
  persistent background pages, or other APIs being removed in MV3? These are
  more powerful and less constrained.
// After:
- **Injection APIs**: `scripting` or `userScripts` with broad hosts equal
  `<all_urls>` content scripts. Is runtime injection needed, or would
  static, scoped `content_scripts` do?
````

**2o** (4.5 Manifest version)

````markdown
// Before:
- **Manifest version**: MV3 is current. MV2 is legacy — Chrome deprecation
  timeline is shifting but direction is clear. MV2 on Firefox is explicitly
  supported long-term.
// After:
- **Manifest version**: rate per the addendum's MV2 table (Chrome:
  unsupported; Edge: retiring; Firefox: supported).
````

**2p** (4.5 Auto-update risk)

````markdown
// Before:
- **Auto-update risk**: Extensions auto-update silently. Is the extension
  open source (updates auditable)? Has the extension changed ownership
  recently? See addendum for scoring.
// After:
- **Auto-update risk**: Extensions auto-update silently. Rate per the
  addendum's §4.6 plug-ins (V3 ownership transfer, V5 update controls).
````

**2q** (REJECTED: store removal)

````markdown
// Before:
- **Known malware / store removal for malicious behavior**: Extension was
  removed from any store for injecting ads, stealing data, cryptomining, or
  similar
// After:
- **Known malware / store removal for malicious behavior**: Extension was
  removed from any store for injecting ads, stealing data, cryptomining, or
  similar (not an MV2-retirement removal)
````

**2r** (REJECTED: self-hosted updates)

````markdown
// Before:
- **Self-hosted updates from unknown server**: MV2 extension with
  `update_url` pointing to an unverified server (bypasses store review)
// After:
- **Self-hosted updates from unknown server**: `update_url` (Chrome) or
  `gecko.update_url` (Firefox) pointing to an unverified server (bypasses
  store review)
- **Unexplained remote code path** (addendum "Remote Code & Config")
````

**2s** (CONDITIONAL: broad perms + MV2)

````markdown
// Before:
  broad access (ad blocker, password manager, dev tools) — Condition:
  understand and accept the access scope; re-audit on ownership changes
- **MV2 on Chrome**: Condition: monitor Chrome's MV2 deprecation timeline;
  identify MV3 alternative
// After:
  broad access (ad blocker, password manager, dev tools) — Condition:
  understand and accept the access scope; re-audit on any §4.6 V5 trigger;
  managed fleets: allowlist + version pin
- **Fresh version** (§4.6 V1): Condition: wait until the version is 72 h
  old, then re-check advisories before installing
- **MV2 on Chrome (unsupported)**: Condition: the publisher's MV3 edition,
  or a browser that still supports MV2 (Edge MV2 = MEDIUM flag only)
````

**2t** (CONDITIONAL: single developer)

````markdown
// Before:
- **Single developer with no org backing**: Condition: monitor for
  acquisition; re-audit if publisher changes
// After:
- **Single developer with no org backing**: Condition: re-audit if the
  publisher, website or contact changes (common sign of a sale)
````

**2u** (APPROVED: badge)

````markdown
// Before:
- Listed on at least one major store with verification badge
// After:
- Listed on at least one major store with verification badge (never
  sufficient alone — §4.6 V2)
- `references/criteria.md` §4.6 raises no flag
````

**Rationale:**
- 2a/2c/2f: V1/V3 need the version's "Updated" date and its diff — collected at Identify/Triage, so Tier 1 can be barred before a quick audit starts.
- 2d/2e: Tier lists now point to the addendum instead of restating it (read-cost offset; one source of truth).
- 2g–2j: F8 fixes (crxcavator dropped, `update_url` attribution, new keys: `world`, DNR rules, `oauth2.scopes`, `data_collection_permissions`).
- 2k: the shared contract requires the `Version integrity (§4.6)` row at every tier; it replaces "Auto-update risk", now part of V3/V5.
- 2l/2m/2o/2p: rubric bullets defer to the addendum (badges, CVE scope, MV2, update risk).
- 2n: "MV2 powerful APIs" is moot on Chrome; least-privilege now targets runtime injection APIs.
- 2q–2u: Verdict Notes match the addendum (MV2-retirement carve-out, Firefox `gecko.update_url`, remote code path, fresh-version condition, Chrome MV2 condition with Edge as MEDIUM only, V5 triggers, badge never sufficient alone).

**Verification:**
```bash
grep -c "| Version integrity (§4.6) | Required | Required | Required |" workflows/browser-extension.md   # 1
grep -ci "crxcavator\|algorithmic\|(MV2 Firefox)\|deprecation timeline\|certified" workflows/browser-extension.md   # 0
grep -c "gecko.update_url\|CISA KEV" workflows/browser-extension.md        # ≥ 2
wc -c < workflows/browser-extension.md                                     # 18471 (≤ 18600)
awk 'length>79' workflows/browser-extension.md | wc -l                     # 3 (same 3 pre-existing lines as base)
sha256sum workflows/browser-extension.md                                   # = 1510a4b60104a01a639df76024b051a9ca6255a1dc86c284ad7a4092d7129afb
```

**If this fails:** `git -C <work-root> checkout -- workflows/browser-extension.md` and re-apply the pairs.

---

### Step 3: Align the browser sub-table of `references/criteria.md` §4.4

**Objective:** close F11 fully: the shared §4.4 browser matrix states the same rating as the addendum for every row it lists, so nothing is left to precedence. Docker/runtime lines in §4.4 are the container plan's and stay untouched.
**Confidence:** High
**Depends on:** Step 1 (ratings are copied from its Permission Risk Classification)
**Do-Projex:** Encouraged
**Verify-Projex:** Encouraged (row-by-row equality is checked by the consistency script)

**Files:** `references/criteria.md`

**Changes:** replace the sub-table from its `###` heading through the `activeTab` row; the `**Red flag:**` paragraph after it stays.

````markdown
// Before (§4.4):
### Browser Extension Permissions — Risk Matrix
| Permission | Risk Level | Notes |
|---|---|---|
| `<all_urls>` | HIGH | Can read/modify all web traffic |
| `webRequest` + `<all_urls>` | CRITICAL | Full MITM capability |
| `cookies` (all domains) | HIGH | Can exfiltrate all session cookies |
| `history` | HIGH | Full browsing history access |
| `clipboardRead` | MEDIUM-HIGH | Can read anything copied |
| `nativeMessaging` | HIGH | Can communicate with local apps |
| `downloads` | MEDIUM | Can write files to disk |
| `storage` | LOW | Local extension storage only |
| `tabs` | LOW-MEDIUM | Tab titles/URLs |
| `activeTab` | LOW | Only current tab when user clicks |
// After:
### Browser Extension Permissions — Risk Matrix
| Permission | Risk Level | Notes |
|---|---|---|
| `<all_urls>` / `*://*/*` | CRITICAL | Read/modify every page the user visits |
| `webRequestBlocking` (with `webRequest`) | CRITICAL | Full MITM: intercept, modify or block all HTTP traffic (MV2; Chrome MV3 only for policy-installed extensions) |
| `webRequest` (observe only) | HIGH | Sees every request URL and header on permitted hosts (MV2 and MV3); cannot modify |
| `cookies` | HIGH | Read/write cookies for permitted domains — session theft |
| `history` | MEDIUM-HIGH | Full browsing history access |
| `clipboardRead` | MEDIUM-HIGH | Can read anything copied |
| `nativeMessaging` | HIGH | Talks to native executables — leaves the browser sandbox |
| `downloads` | HIGH | Can silently download files to disk |
| `storage` / `unlimitedStorage` | LOW | Extension-local storage only; risk comes from permissions that read pages or send data |
| `tabs` | MEDIUM | URLs and titles of every open tab |
| `activeTab` (alone, no broad hosts) | LOW | Only current tab when user clicks |

Ratings mirror `references/criteria/browser-extension.md` § Permission Risk Classification, which holds the full list and scoring rules; change both together.
````

| Row | Before | After (= addendum) | Why |
|---|---|---|---|
| `<all_urls>` | HIGH | CRITICAL; adds `*://*/*` | Addendum rates full page access Critical; same permission, two spellings |
| `webRequest` + `<all_urls>` "Full MITM" | CRITICAL | split: `webRequestBlocking` CRITICAL / `webRequest` (observe only) HIGH | MITM needs blocking; observe-only MV3 `webRequest` cannot modify traffic but still sees every URL/header |
| `cookies` (all domains) | HIGH | HIGH; cell → `cookies` | Same rating; scope follows host permissions |
| `history` | HIGH | MEDIUM-HIGH | Addendum value; history read is privacy-sensitive, not code execution (Red Flag "Excessive permissions" still covers unjustified history access) |
| `clipboardRead` | MEDIUM-HIGH | MEDIUM-HIGH | Kept; the addendum now splits `clipboardRead` (Medium-High) from `clipboardWrite` (Medium) to match |
| `nativeMessaging` | HIGH | HIGH | Same |
| `downloads` | MEDIUM | HIGH | Addendum value: silent download to disk is a payload-drop path |
| `storage` | LOW | LOW; adds `unlimitedStorage` | Addendum moved to Low (was Medium) |
| `tabs` | LOW-MEDIUM | MEDIUM | Addendum value: URL+title of every tab enables phishing/history-equivalent tracking |
| `activeTab` | LOW | LOW; cell → "(alone, no broad hosts)" | Addendum rates `activeTab` + broad hosts Medium separately |

**Rationale:** the shared table keeps the most-asked rows for quick reads; the pointer sentence makes the addendum the single source of truth for the full list. Ratings were copied from the addendum, not re-derived, and the consistency script asserts each row's equality. Rejected: deleting the shared table for a pointer only — other readers (dispatcher Red Flags, Tier 1 quick reads) use it.

**Verification:**
```bash
sha256sum references/criteria.md   # = 3ca4bd20c443fbe6cd0f06fa9bd9e8d3ffd1050f3b5ba95c31cf691a6a0faf35 (only if no sibling has changed criteria.md since 20843cc; otherwise rely on the two checks below)
git -C <work-root> diff -U0 -- references/criteria.md | grep '^[-+][^-+]' | grep -vc '^[-+]|'   # 1 (the pointer sentence; every other changed line is a table row)
git -C <work-root> diff -U0 -- references/criteria.md | grep -c 'docker\|USER root\|privileged\|SYS_ADMIN'   # 0
```

**If this fails:** `git -C <work-root> checkout -- references/criteria.md`, then re-apply the block.

---

## Verification Plan

### Automated Checks

- [ ] `python3 evals/run_evals.py validate` passes; `python3 -m unittest discover -s evals -p "test_*.py"` passes with the Preflight count.
- [ ] Consistency script (run from `<work-root>`; not committed):
```bash
python3 - <<'EOF'
import re, pathlib
crit = pathlib.Path("references/criteria.md").read_text(encoding="utf-8")
add  = pathlib.Path("references/criteria/browser-extension.md").read_text(encoding="utf-8")
wf   = pathlib.Path("workflows/browser-extension.md").read_text(encoding="utf-8")
heads = set(re.findall(r"^### (V[1-5]) ", crit, re.M))
assert heads == {"V1","V2","V3","V4","V5"}, heads
for name, t in [("add", add), ("wf", wf)]:
    for v in re.findall(r"§4\.6 (V\d)", t):
        assert v in heads, (name, v)
    low = t.lower()
    for bad in ["algorithmic", "crxcavator", "(mv2 firefox)", "deprecating", "deprecation timeline",
                "mv2 with `webrequestblocking` on chrome", "edge \"certified\"", "\"certified\" publisher"]:
        assert bad not in low, (name, bad)
assert add.count("## Version & Update Integrity (§4.6)") == 1
assert len(re.findall(r"^- \*\*V[1-5]\*\* — ", add, re.M)) == 5
assert "## CVE Scope (§4.3)" in add and "Blocking CVE" in pathlib.Path("SKILL.md").read_text(encoding="utf-8")
for s in ["`scripting`", "`userScripts`", "`webRequest` (observe only)", "Established Publisher",
          "data_collection_permissions", "unsupported MV2", "2026-08-31", "Remote Code & Config"]:
    assert s in add, s
assert re.search(r"^\| `storage` / `unlimitedStorage` \| Low \|", add, re.M)
assert crit.count("| `storage` / `unlimitedStorage` | LOW |") == 1
sec  = add.split("## Permission Risk Classification")[1].split("## Data Disclosure")[0]
sub  = crit.split("### Browser Extension Permissions — Risk Matrix")[1].split("**Red flag:**")[0]
row  = re.compile(r"^\| (`[^|]+?) \| ([A-Za-z-]+) \|", re.M)
arows, srows = dict(row.findall(sec)), row.findall(sub)
assert len(srows) == 11, len(srows)
for p, r in srows:
    assert p in arows and arows[p].lower() == r.lower(), (p, r, arows.get(p))
assert "Ratings mirror `references/criteria/browser-extension.md`" in sub
assert "| `webRequest` + `<all_urls>` |" not in crit
assert wf.count("| Version integrity (§4.6) | Required | Required | Required |") == 1
assert "## Audit Coverage" not in wf   # dispatcher owns it
assert len(add.encode()) <= 15800 and len(wf.encode()) <= 18600
print("OK")
EOF
```
- [ ] `git -C <work-root> diff --stat <base>..HEAD` lists only the 3 files (plus the execution log).

### Manual Verification (paper traces)

Walk each case through `SKILL.md` Step N + `references/criteria.md` §4.3/§4.6 + the new addendum; log the cited rule per hop.

| # | Case | Expected |
|---|---|---|
| T1 | eval 11: uBlock Origin on Firefox, AMO Recommended, current version > 7 d old | MV2 Firefox LOW note; ad-blocker bullet justifies `webRequest`/`webRequestBlocking`/`webNavigation`/`privacy`/broad hosts; `tabs` note; Tier 1 open → **APPROVED** (eval 11 ✓; < 72 h → CONDITIONAL is the known time dependence) |
| T2 | eval 1: Wappalyzer on Chrome (MV3, broad hosts justified by purpose) | Tier 1 or 2 depending on badge/age → **APPROVED or CONDITIONAL** (eval 1 ✓) |
| T3 | eval 10: "YouTube Video Downloader Pro" shared in Slack | Tier 3 (direct-link share); permissions vs purpose; → **CONDITIONAL or REJECTED** (eval 10 ✓) |
| T4 | ShadyPanda/QuickLens shape: CWS Featured, 500K users, "Updated" yesterday, adds `scripting` + `<all_urls>` with no changelog | V1 HIGH `fresh version` (3-day rule) + V3 HIGH (unexplained permission increase) → Tier 3 → **CONDITIONAL** with escalation (V3 HIGH not exempt); badge offsets nothing. If source shows fetched strings reaching `eval`/`userScripts` → toward **REJECTED** |
| T5 | Full uBlock Origin (MV2) requested for Chrome 141 | `unsupported MV2` HIGH + Tier 3; CWS removal 2026-08-31 is retirement, not "Removed for cause" → **CONDITIONAL**, condition: uBlock Origin Lite (MV3) or a browser that supports MV2 |
| T6 | MV2 ad blocker on consumer Edge, otherwise clean, version > 7 d | `MV2 retiring` MEDIUM (single) → **APPROVED** with Recommendation naming the MV3 edition + Microsoft's cut-off; 3+ MEDIUMs would make it CONDITIONAL |
| T7 | Extension sold last month: developer name + website changed; no permission change | V3 ownership transfer → HIGH + Tier 3 → **CONDITIONAL** (re-audit on V5 triggers); with a simultaneous permission increase or new remote-config endpoint → toward **REJECTED** |
| T8 | "AI sidebar" with content scripts on `chatgpt.com`/`claude.ai`, Firefox `data_collection_permissions: none`, source posts prompts to a third-party endpoint | Sensitive reach HIGH + deceptive disclosure HIGH → **CONDITIONAL** at best with escalation; a vendor report confirming harvesting → Red Flag "Known malware" → **REJECTED** |
| T9 | Tampermonkey on Chrome (`userScripts`, broad hosts, Featured, > 1 M users, version > 7 d) | `userScripts` justified (user-script manager) → no Tier 3 trigger; Tier 1 open → **APPROVED** reachable |
| T10 | Extension loaded via Developer mode "Load unpacked" from a GitHub release | Install path → Tier 3; no auto-update (frozen, no fixes); V2 identity = repo owner matches vendor site → **CONDITIONAL** (re-check releases manually; prefer the store listing) |

### Acceptance Criteria Validation

| Criterion | How to Verify | Expected Result |
|-----------|---------------|-----------------|
| Shared floor present | Preflight greps | 1 / 5 / 6 / ≥1 / ≥1 |
| Addendum exact | sha256 + Step 1 greps | match; 1 / 5 / 1 / 0 |
| Workflow exact | sha256 + Step 2 greps | match; 1 / 0 / ≥2 / 3 |
| §4.4 sub-table aligned | Step 3 checks + script row equality | 1 non-row line; 0 Docker lines; `OK` |
| References resolve; stale gone; sizes | consistency script | `OK` |
| Harness | validate + unittest | pass; same count |
| Verdict behavior | T1–T10 log | matches table |
| Scope | `git diff --stat` | 3 files |

---

## Rollback Plan

1. Before close: `projex-abandon.sh <repo-root> claude/youthful-dijkstra-5ov1kt projex/2610162006-browser-extension-rubric-refresh --worktree` — base untouched.
2. After squash-close: `git -C <repo-root> revert <squash-sha>` (3 files; the `criteria.md` hunk is confined to the browser sub-table, so it reverts cleanly even after the container plan's §4.4 Docker edits).

---

## Notes

### Risks

- **Read cost +8.2 KB (~2k tokens) on browser audits.** Mitigation: size caps in criteria; workflow defers to the addendum. Ordered trims if a later budget demands it: (1) addendum `### Install path` third bullet; (2) `## Data Disclosure` first bullet; (3) the `offscreen` row.
- **Platform dates drift** (Edge cut-off, Firefox consent rollout). Mitigation: dates in one table with "as of 2026-10" and an instruction to cite the vendor page; STEWARDSHIP 90-day cadence.
- **3-day date rule over-triggers** on frequently released extensions (uBO, Wappalyzer) → more CONDITIONALs. Mitigation: condition is time-bound (no escalation for V1 alone per §4.6); eval effects go to the eval plan.
- **Heading names for the §4.3 plug-in may differ across sibling plans** (shared contract fixes only the §4.6 heading). This plan uses `## CVE Scope (§4.3)`. Mitigation: orchestrator harmonizes (Orchestrator hand-off).
- **Concurrent `criteria.md` edits.** Hunk confined to the browser sub-table; container plan's Docker hunk is a separate subsection. Rebase before close if the container plan closes first.

### Eval hand-off (for the eval-refresh plan; do not edit `evals/` here)

- New cases: (a) badged CWS extension whose current version is < 72 h old and adds permissions → CONDITIONAL; (b) ownership transfer + permission increase → REJECTED or CONDITIONAL; (c) MV2 extension requested for Chrome → CONDITIONAL (MV3 edition), not REJECTED for "removed"; (d) Edge MV2 → APPROVED/CONDITIONAL with MV3 note; (e) AI-chat sidebar with declared `none` data collection but prompt exfiltration → CONDITIONAL/REJECTED; (f) `userScripts` manager (Tampermonkey) → APPROVED reachable; (g) Developer mode unpacked install → CONDITIONAL.
- Existing: eval 11 (uBO/Firefox, exact APPROVED) is time-dependent under V1 (already listed in the shared plan's eval row); consider `[APPROVED, CONDITIONAL]` with a cooldown-only condition, or pinning the version in the prompt. Evals 1 and 10 unaffected.

### Orchestrator hand-off

- Harmonize the §4.3 plug-in heading across addenda (this plan: `## CVE Scope (§4.3)`).
- STEWARDSHIP: browser-extension Last Reviewed = 2026-10-16 on close.
- Deferred (F9): Safari Web Extensions; Chromium-fork MV2 detail beyond the one table row.

### Unverified / hedged facts

- Edge exact MV2 dates (no Microsoft Learn primary retrieved) — table hedged "as of 2026-10", told to confirm.
- Whether Mozilla extended `data_collection_permissions` to all extensions in 2026 — text says older extensions "may lack it", no flag.
- AMO per-version review: Extension Workshop says every version; the SUMO article is vaguer — text says "Mozilla documents".
- Edge off-store `.crx` blocking (A2) and Chrome MV3 `webRequestBlocking` policy-only (A3): prior knowledge.
- CRXcavator status: unverified — removed from the rubric rather than replaced by a named tool.
- Vendor-sourced incident examples (ShadyPanda, QuickLens, Urban VPN) appear only in this plan's rationale, not in shipped text.

### Open Questions

None. Policy choices (3-day rule, Established Publisher excluded from Tier 1, ownership transfer = HIGH, Edge MV2 = MEDIUM) are recorded in Rationale and reversible as single-line edits.

### Split Decision

`No split — heuristic tripped but steps tightly coupled (rationale: ~922 lines / ~65 KB, almost all embedded exact blocks; 3 steps only, so the "> 5 steps" half of the heuristic does not hold; one .projex scope; Step 2 pointers depend on Step 1 headings)`.

### Revision Log

| Date | Trigger | Change |
|---|---|---|
| 2026-10-16 | Initial | Plan authored on base `20843cc` (shared floor landed during planning) |
| 2026-10-16 | Orchestrator: this plan now owns the whole §4.4 browser sub-table (Docker lines stay with container) | Step 3 rewritten: full sub-table replaced, ratings = addendum, pointer sentence; addendum splits `clipboardRead` (Medium-High) / `clipboardWrite` (Medium) → new addendum sha/size; F11 row, criteria, script (row-equality check), Out of Scope, hand-off, rollback, risks updated; simulation re-run |
