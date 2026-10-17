# Browser-Extension + IDE-Plugin Stewardship Review

> **Status:** Complete
> **Author:** Claude (Opus)
> **Parent:** Orchestrator
> **Subject:** `workflows/browser-extension.md`, `references/criteria/browser-extension.md`, `workflows/ide-plugin.md`, `references/criteria/ide-plugin.md` — first scheduled `STEWARDSHIP.md` review pass (checklist steps 1–3; step 4 offline only)
> **Type:** Gap Analysis (Status Quo vs ecosystem reality as of 2026-10-16)
> **Tier:** Standard
> **Lenses Applied:** Inversion (pre-mortem on Tier 1 fast path) | Constraint Mapping | Steel-Manning
> **Related Projex:** 2604070218-install-auditor-subject-typed-redesign-nav.md | 2604172000-stewardship-cadence-m63-walkthrough.md | 2610161852-dispatcher-rubric-consistency-walkthrough.md | 2610161850-eval-runner-harness-walkthrough.md

---

## Executive Summary

Both rubrics were authored ~2026-04-14/15; only roadmap-label comments changed since (commit `5c44b79`). Six months of ecosystem change make them materially stale. Dominant gap, shared by both subjects: trust is scored **per extension** (installs, badge, publisher), but the 2025–2026 incident pattern is **per version** — a verified, high-adoption extension ships one malicious update (Nx Console May 2026, ShadyPanda, QuickLens). The current Tier 1 fast path would rate those APPROVED. Also stale: MV2 status (Chrome MV2 is gone, not "deprecating"; Edge consumer retirement began Aug 2026), badge semantics (Edge "Certified" doesn't exist; CWS Featured isn't algorithmic; badges were carried by malicious extensions), and the IDE rubric's silence on AI-editor forks that pull from Open VSX, where GlassWorm ran. Offline evals: `validate` passes; 7 cases prepare cleanly; none of the 7 exercises the new failure modes. Recommendation: two plan-projex (one per subject), with a shared "version-integrity" pattern coordinated with sibling registry-package review.

---

## Evaluation Scope

**Questions:** Do the rubrics reflect the ecosystems as of 2026-10-16? What is stale, missing, or wrong? Which gaps warrant a plan-projex?

| Criterion | Weight | Description |
|---|---|---|
| Verdict correctness | High | Would the rubric produce the right verdict on current real-world cases? |
| Factual currency | High | Platform facts (MV2, badges, store policies, tooling) match today |
| Coverage | Medium | Ecosystems/sources users actually install from are covered |
| Actionable conditions | Medium | CONDITIONAL outputs use controls platforms now provide |
| Eval coverage | Medium | Eval cases exercise the current failure modes |

**Out of scope:** editing workflow/criteria/STEWARDSHIP files (review-only per STEWARDSHIP step 5); live `run` of evals (costs money, not approved); other subjects (sibling evals); STEWARDSHIP steps 7–8 (inventory date + nav log) — left to orchestrator.

---

## Context Analysis

- **Current state:** Type 2 / Type 3 workflows follow Identify → Evidence (Triage, Research) → Subject Rubric → Verdict Notes; addenda hold trust-signal tables, risk classifications, tier thresholds. Content dates to M3.1 (2026-04-14) and M3.4 (2026-04-15).
- **Since then (on base):** dispatcher Red Flags reconciled (`5c44b79`), eval harness added, Python script twins, lean report tier. None touched rubric substance for these subjects.
- **Constraints:** Rubrics are prose read by an agent at audit time — every added check costs read tokens (see 2604170511-measure-read-cost-f7-m53-walkthrough.md). Web research during audits is search-only; agent cannot install/inspect live.
- **Network note (this review):** `developer.chrome.com` and `code.visualstudio.com` did not resolve from this sandbox (DNS `ENOTFOUND`); vendor facts below come from search-engine summaries of those pages plus secondary reporting. Confidence marked accordingly.

---

## Foundations

**Principle:** an install audit is a point-in-time trust decision about code that will auto-update. Its value depends on (a) signals that predict *future* versions' safety and (b) conditions that bound damage if prediction fails.

| Assumption (embedded in rubrics) | Validity now | Risk if wrong | Sensitivity |
|---|---|---|---|
| High installs + badge + known publisher ⇒ low risk (Tier 1) | Weak — compromised-publisher and sleeper patterns defeat it | APPROVED on a trojanized version | Flips verdict |
| Badges are review signals (Featured/Recommended/Verified) | Partial — identity/quality signals, not code-integrity | Over-weighted trust | Flips tier |
| MV2 on Chrome is "approaching EOL" | False — EOL passed | Wrong flag severity; misses "how is this even running?" | Changes conditions |
| VS Code Marketplace is the IDE trust boundary | Partial — forks use Open VSX | Badge/verification that doesn't apply is credited | Flips tier |
| No IDE permission model ⇒ capability table suffices | Partial — new AI contribution points missing | Misses agent/MCP/LLM-tool surface | Moderate |
| Auto-update is uncontrollable | Stale — VS Code allowlist, publisher trust, 2-h delay exist | Weaker conditions than available | Low (conditions only) |

**Prior work:** rubrics derived from 2604070217-subject-typed-audit-dispatch-eval.md; no prior stewardship pass (inventory shows `—`).

---

## Analysis

### A1. Version-level compromise blind spot (both subjects) — Confidence: High — Lens: Inversion

**Finding:** Tier 1 criteria (browser: ≥100K users, badge, known publisher, ≥1 y; IDE: ≥500K installs, verified publisher, ≥1 y) contain no check on the *version* being installed. Pre-mortem: "Tier 1 APPROVED Nx Console on 2026-05-18" — every Tier 1 box was ticked (2.2M installs, verified `nrwl` publisher, years listed, no prior incidents).

**Evidence:**
- Nx Console `nrwl.angular-console` 18.95.0 published 2026-05-18 with stolen publish credential (`VSCE_PAT`) outside CI; live ~11–18 min on VS Marketplace, ~36 min on Open VSX; led to ~3,800 GitHub internal repos exfiltrated; CVE-2026-48027, added to CISA KEV. (StepSecurity, Nx postmortem, THN, CSA)
- ShadyPanda: extensions benign since 2018, some with Featured/Verified badges, flipped in mid-2024 update to hourly remote JS; ~4.3M Chrome/Edge users. (Koi via BleepingComputer, Infosecurity, Dec 2025)
- QuickLens / ShotBird: sold, then turned malicious via 2026-02-17 update (CSP stripping, remote JS every 5 min). (THN Mar 2026)
- Cyberhaven (Dec 2024): CWS developer account OAuth-phished, malicious version pushed (prior knowledge; Medium).

**Implication:** Rubrics already model *ownership transfer*, but not *publisher-credential compromise* or *sleeper update*. Missing signals: version age (hours/days since publish), version matches a tagged upstream release / CI provenance, unusual version jump, recent permission/capability delta vs prior version, active advisories naming the version. Missing conditions: pin version / delay updates / allowlist.

### A2. MV2 status stale (browser-extension) — Confidence: Medium-High — Lens: Constraint Mapping

**Finding:** Criteria say "MV2 — Chrome deprecating (timeline shifting but direction clear)"; scoring "MV2 on Chrome = MEDIUM flag (EOL risk, not a security flag)"; Verdict Notes condition "monitor Chrome's MV2 deprecation timeline". All stale.

**Evidence (Chrome MV2 timeline page, via search summary):** MV2 disabled for all users ~2025-07-24 (Chrome 138 last w/ enterprise policy); `ExtensionManifestV2Availability` policy removed in Chrome 139; remaining MV2 items scheduled for CWS removal 2026-08-31. Edge: consumer MV2 retirement started Aug 2026, managed devices early 2027 (Windows Report, BetaNews — secondary). Firefox: still supports MV2 + blocking `webRequest`, no end date (Mozilla 2025; no 2026 change found).

**Implication:** On current Chrome an MV2 extension cannot run; a user asking to install one implies outdated Chrome, a Chromium fork, dev-mode "Load unpacked", or a stale listing → should be Tier 3 / unsupported, not a MEDIUM EOL note. Edge MV2 = time-boxed (months). Tier 3 trigger "MV2 with `webRequestBlocking` on Chrome" is now unreachable on stock Chrome. Firefox MV2 guidance remains correct; eval 11 (uBO on Firefox → APPROVED) remains valid.

### A3. Badge semantics wrong / over-weighted (both) — Confidence: Medium-High — Lens: Steel-Manning

**Finding:**
- Browser rubric names **Edge "Certified"** — Edge's badge is **"Featured"** (Microsoft docs); no "Certified" publisher badge found.
- Rubric calls CWS **Featured "algorithmic, not human-reviewed"** — Google docs: Featured is hand-reviewed by Chrome team; **"Established Publisher"** (automatic: verified identity + policy compliance record) is the second CWS badge and is absent from the rubric.
- Badges carried malicious code: Urban VPN Proxy (Featured, 6M users) harvested AI-chat prompts from v5.5.0 (Jul 2025), 7 sibling extensions (Koi, Dec 2025; G Data Jun 2026); ShadyPanda had Featured/Verified items.
- IDE criteria: "JetBrains first-party **or verified vendor** = strong positive (equivalent to AMO Recommended)". June 2026: 15 JetBrains Marketplace plugins (~70K installs, 7 vendor accounts) stole AI API keys past manual review; JetBrains stated Plugin Verifier is a compatibility checker, not anti-malware (JetBrains blog, THN, BleepingComputer). Verified vendor = identity, not code review.
- VS Code "Verified" = domain ownership + ≥6 months good standing (VS Code docs) — identity signal; Nx was verified.

**Steel-man for current weighting:** badges still correlate with lower base rates; removing them loses information. **Counter:** keep them, but cap their effect — badge may lift Tier 2→Tier 1 only together with version-integrity checks (A1), and never offsets a version-level red flag. AMO Recommended remains the strongest (per-version human review for Recommended add-ons) — that equivalence is fine; JetBrains verified vendor should drop to moderate.

### A4. AI-editor forks & Open VSX trust model (ide-plugin) — Confidence: High — Lens: Constraint Mapping

**Finding:** Workflow lists "Cursor" as a target editor but assumes VS Code Marketplace trust signals. Cursor, Windsurf, Google Antigravity, VSCodium, etc. install from **Open VSX** (or a mirror), where Marketplace "Verified" does not apply and namespaces can be unclaimed. Criteria score "Open VSX namespace + VS Code cross-listing = moderate positive" and call Open VSX "slightly higher trust" — not supported by 2026 events.

**Evidence:**
- Koi (Dec 2025): forks inherit hardcoded Marketplace recommendation lists; recommended extensions absent on Open VSX had unclaimed namespaces; >1,000 installs of Koi's placeholders via IDE recommendation. Cursor fixed by Dec 1; Google partial Dec 26; Windsurf no response reported.
- GlassWorm on Open VSX: ≥72 malicious extensions 2026-01-31→03-13; used `extensionPack`/`extensionDependencies` to pull payload *after* review; 73 "sleeper" extensions reported late Apr 2026 (Socket via THN, CSA).
- Eclipse Foundation: pre-publish malware scanning announced Feb 2026, enforcement ~Mar 2026 (THN, Hackmag — secondary); Oct 2025 leaked-token revocation + shorter token lifetimes.
- Nx malicious version lived longer on Open VSX (~36 min) than Marketplace (~11 min).
- Repo-wide: `references/registries.md` row "Cursor extensions (VS Code compatible) | Same as VS Code Marketplace" is wrong for the same reason (shared file, outside this subject — flag to orchestrator).

**Implication:** Identify step must resolve *which registry the target editor actually pulls from*. Verify the Open VSX namespace owner equals the Marketplace publisher. `extensionDependencies`/`extensionPack` review must be Required whenever present (currently Tier-skip at Tier 1), because a dependency can be swapped by any later update.

### A5. Browser permission table gaps (browser-extension) — Confidence: High — Lens: First-principles check vs current Chrome/Firefox API surface

**Finding:** Missing from the risk table: `scripting` (MV3 code injection; with broad hosts ≈ `<all_urls>` JS execution), `userScripts` (arbitrary user-script execution), non-blocking `webRequest` (still present in MV3; observes all URLs → exfil/telemetry), `declarativeNetRequestWithHostAccess`, `webNavigation`, `identity` (OAuth token access), `tabCapture`/`desktopCapture` (screen capture), `privacy`, `offscreen`. Table row `webRequest + webRequestBlocking ... (MV2 only)` implies `webRequest` is harmless in MV3. Inconsistency: addendum rates `storage` Medium; `references/criteria.md` rates it LOW (shared file).
**Implication:** Permission-justification scoring under-flags MV3-era injection paths — the ones ShadyPanda/QuickLens-style payloads use alongside remote config.

### A6. AI surface missing (both) — Confidence: Medium-High

**Finding:**
- IDE capability table lacks VS Code AI contribution points: `languageModelTools` (auto-available to agent mode on install, full extension-API access), `mcpServerDefinitionProviders` (extension registers MCP servers), `chatParticipants`. `references/classifier.md` routes "MCP server installed via a VS Code extension" → ide-plugin, but the ide-plugin rubric has no MCP row and no pointer to `workflows/agent-extension.md` sub-rubric. JetBrains AI-key theft (A3) shows "plugin handles AI provider API keys" is an attacker-preferred category.
- Browser: dominant 2025–26 theme is AI-chat harvesting (Urban VPN; LayerX Feb 2026 ~287 fake "AI assistant" extensions — aggregator, Low-Medium) and CWS July 2026 policy (data minimization, disclose post-install data-handling changes, ban on circumventing AI-service safeguards; enforcement from 2026-08-01). Content scripts matching AI-chat domains (chatgpt.com, claude.ai, gemini.google.com…) are not called out as sensitive reach.

### A7. Platform controls absent from conditions (both) — Confidence: Medium (vendor docs via search)

**Finding:** CONDITIONAL outputs say "monitor for incidents / re-audit on ownership change" while platforms now offer enforceable controls:
- VS Code: `extensions.allowed` allowlist (1.96, can pin versions); publisher-trust prompt on first install from a new publisher (1.97; CLI installs don't auto-trust); **2-hour auto-update hold** for new versions (1.123, 2026-06-03; exempt for trusted publishers e.g. Microsoft/GitHub/OpenAI) — THN, InfoQ.
- Firefox: `browser_specific_settings.gecko.data_collection_permissions` required for new extensions since 2025-11-03; shown in install prompt + AMO listing — a new manifest key to inspect and a declared-vs-observed check.
- Chrome/Edge: enterprise `ExtensionSettings` (allow/block, pin via self-hosted) — prior knowledge, Medium.
- Neovim 0.12 (2026-03-29) ships `vim.pack` with lockfile `nvim-pack-lock.json`; lazy.nvim has `lazy-lock.json` → "pin to commit" is now native.

### A8. Stale/incorrect research mechanics (both) — Confidence: Medium (per item)

| Item | Location | Issue | Conf. |
|---|---|---|---|
| `crxcavator.io` as manifest source | browser workflow § Manifest analysis | Reported defunct (Spin.ai 2024; blog 2026 "CRXcavator is dead") — vendor-sourced | Low-Med |
| `update_url (MV2 Firefox)` | browser workflow + addendum | `update_url` is a Chrome manifest key (MV2 & MV3); Firefox uses `browser_specific_settings.gecko.update_url`. Self-distribution exists on both | Medium |
| Sideloaded `.crx` treated as just "no store" | browser addendum | Chrome Win/macOS blocks off-store CRX except enterprise policy or dev-mode unpacked (no auto-update); release Firefox requires Mozilla signing (unlisted signed XPI still passed automated review). Install path is itself the signal | Medium |
| `postInstall` download logic | IDE workflow Q4 | VS Code extensions have no install hook; downloads occur at activation | Medium |
| Activation `*` only as always-on | IDE addendum | `onStartupFinished` is also effectively always-on | High |
| `packer` listed as current manager | both IDE files | packer.nvim unmaintained (README notice; prior knowledge); `vim.pack` now built-in | Medium |
| "IDE plugins rarely have formal CVEs" | IDE workflow 4.3 | Nx got CVE + CISA KEV — check KEV too | High |
| Obfuscation guidance | browser 4.3, IDE none | GlassWorm used invisible Unicode to hide code (Oct 2025, prior knowledge) — add to source-review checklist | Medium |

### A9. Coverage gaps (low priority) — Confidence: Medium

- Browser: Safari Web Extensions (listed in `references/registries.md`, not in workflow); Chromium forks (Brave/Arc/Opera) MV2 behavior differs.
- IDE: Zed (WASM-sandboxed extensions — genuinely different, capability-limited model), Emacs MELPA (classifier signal exists, workflow silent), Visual Studio (IDE) Marketplace, Eclipse Marketplace.

### A10. Eval coverage (step 4, offline) — Confidence: High (Primary)

- `python3 evals/run_evals.py validate` → 41 evals, 248 assertions; browser-extension 3, ide-plugin 4; passes.
- `prepare --workflow browser-extension,ide-plugin` → 7 evals (ids 1, 10, 11, 16, 17, 28, 37), 33-file snapshot; `run --dry-run` builds commands. No live run (not approved) → **no regression verdict possible**; deterministic `grade` requires responses.
- Gaps: no case for compromised/fresh version of a trusted extension, ownership-transfer, MV2-on-Chrome, Edge MV2, Open VSX/fork install, JetBrains plugin, AI-key/AI-chat surface, MCP-via-extension.
- Eval 37 premise "rust-analyzer … downloads a native binary" — rust-analyzer ships platform-specific VSIX with bundled server (prior knowledge, Medium); assertion "bundled binary audited within ide-plugin rubric" still fine; prompt wording slightly inaccurate.
- Existing expected verdicts (Wappalyzer, uBO-Firefox, Prettier, GitLens, rust-analyzer → APPROVED/CONDITIONAL; YouTube Downloader / sideloaded VSIX → REJECTED/CONDITIONAL) remain plausible; none invalidated by findings.

---

## Evidence Log

| # | Finding | Source | Type | Conf. | Notes |
|---|---|---|---|---|---|
| 1 | Rubric content unchanged since 2026-04-14/15 except comment strip | `git log` on 4 files; `git show 5c44b79` | Primary | High | |
| 2 | Tier 1 has no version-level check | `references/criteria/*` § Tier thresholds | Primary | High | |
| 3 | Nx Console 18.95.0 compromise, CVE-2026-48027, KEV | stepsecurity.io; nx.dev postmortem; thehackernews.com 2026/05; labs.cloudsecurityalliance.org | Tertiary | High | Multiple independent |
| 4 | ShadyPanda sleeper w/ badges | bleepingcomputer.com; infosecurity-magazine.com (Dec 2025) | Tertiary | High | |
| 5 | QuickLens/ShotBird sold→malicious | thehackernews.com 2026/03 | Tertiary | Medium | |
| 6 | Chrome MV2 disabled 2025; policy gone Chrome 139; CWS removal 2026-08-31 | developer.chrome.com mv2 timeline (search summary; fetch DNS-blocked) | Tertiary | Medium-High | Removal completion unverified |
| 7 | Edge consumer MV2 retire Aug 2026; enterprise early 2027 | windowsreport.com; betanews.com | Tertiary | Medium | No MS primary |
| 8 | Firefox MV2 continues | Mozilla 2025 via bleepingcomputer/osnews | Tertiary | High | No 2026 change found |
| 9 | CWS Featured manual; Established Publisher automatic | developer.chrome.com/docs/webstore/discovery; blog.google 2022 | Tertiary | High | |
| 10 | Edge badge = Featured; re-evaluated; no "Certified" found | learn.microsoft.com Edge extensions | Tertiary | Medium-High | Absence-of-evidence for "Certified" |
| 11 | Urban VPN Featured harvesting AI chats | infosecurity-magazine.com; thehackernews.com 2025/12; G Data 2026/06 | Tertiary | High | |
| 12 | CWS July 2026 policy update | developer.chrome.com/blog/cws-policy-updates-2026; cyberinsider.com | Tertiary | Medium-High | |
| 13 | Firefox `data_collection_permissions` from 2025-11-03 | blog.mozilla.org/addons 2025/10/23; cyberinsider.com | Tertiary | High | |
| 14 | JetBrains 15 AI-key-stealing plugins; verifier not anti-malware | blog.jetbrains.com/platform/2026/06; thehackernews.com 2026/06; bleepingcomputer.com | Tertiary | High | |
| 15 | Fork recommendation / Open VSX namespace squat | koi.ai blog; bleepingcomputer.com | Tertiary | High | |
| 16 | GlassWorm Open VSX via extensionPack/Dependencies | thehackernews.com 2026/03; labs.cloudsecurityalliance.org | Tertiary | High | |
| 17 | Open VSX pre-publish scanning Feb/Mar 2026 | thehackernews.com 2026/02; hackmag.com | Tertiary | Medium | No Eclipse primary found |
| 18 | VS Code allowlist 1.96, trust prompt 1.97, verified = domain + 6 mo | code.visualstudio.com docs (search summary; fetch DNS-blocked) | Tertiary | Medium-High | |
| 19 | VS Code 1.123 2-h auto-update hold | thehackernews.com 2026/06; infoq.com 2026/06 | Tertiary | Medium-High | No MS release-note primary |
| 20 | VS Code AI contribution points | code.visualstudio.com/api/extension-guides/ai | Tertiary | High | Risk framing is inference |
| 21 | Neovim 0.12 `vim.pack` 2026-03-29 | alternativeto.net; heise.de | Tertiary | High | |
| 22 | CRXcavator defunct | spin.ai; thenextgennexus.com 2026 | Tertiary | Low-Med | Vendor-interested sources |
| 23 | Firefox wallet-stealer waves Aug + Oct 2026 (impersonation, homoglyph) | thehackernews.com 2026/08, 2026/10 | Tertiary | High | Supports impersonation check; rubric already has it |
| 24 | Eval validate/prepare/dry-run OK; 7 cases | local run, scratch workspace | Primary | High | No live run |
| 25 | `registries.md` Cursor row; `criteria.md` storage LOW vs addendum Medium | `references/registries.md:72`; `references/criteria.md:177` vs addendum | Primary | High | Shared files — out of subject scope |

---

## Evaluation Against Criteria

| Criterion | Browser-ext | IDE-plugin | Conf. | Rationale |
|---|---|---|---|---|
| Verdict correctness | Weak | Weak | High | Tier 1 APPROVES compromised-version / sleeper cases (A1); fork installs mis-credited (A4) |
| Factual currency | Weak | Adequate− | Medium-High | MV2, badges, crxcavator, update_url (browser); packer, postInstall, CVE claim (IDE) |
| Coverage | Adequate | Adequate− | Medium | Core stores covered; forks/Open VSX trust, AI surface, Zed/MELPA missing |
| Actionable conditions | Weak | Weak | Medium | "Monitor" conditions while enforceable controls exist (A7) |
| Eval coverage | Weak | Weak | High | 0 of 7 cases test 2026 failure modes |

**Overall:** structure sound (sections, tiering, permission/capability framing remain right); trust-signal weighting and platform facts need a targeted refresh. Not a rewrite.

---

## Challenges and Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Version-integrity checks bloat Tier 1 (read cost, audit time) | Medium | Medium | Single compact "version freshness + provenance" row; skip deep checks unless a trigger fires |
| Version-age signals unobtainable via web search (CWS shows "Updated" date; Marketplace shows "Last updated") | Medium | Medium | Use listing date fields + GitHub release tag comparison; mark "unverified" in Audit Coverage rather than block |
| Over-correcting badges → false REJECTED on mainstream tools | Low-Med | Medium | Cap, don't remove; badge never alone decisive either way |
| Secondary-source facts (Edge dates, Open VSX enforcement, 2-h delay) drift or are wrong | Medium | Low-Med | Plan step: verify against vendor primary pages from a network that resolves them; phrase rubric as "check current status" not hard dates where uncertain |
| Duplicate work with sibling registry-package review (same version-integrity theme for npm/PyPI) | High | Low | Orchestrator dedupes: put shared pattern in `references/criteria.md` once, subject addenda reference it |
| Ecosystem keeps moving before plan lands | High | Low | Event-based triggers in STEWARDSHIP already apply; keep dates in one place per addendum |

---

## Findings

| # | Finding | Severity | Conf. | Plan-projex? |
|---|---|---|---|---|
| F1 | Version-level compromise blind spot: Tier 1 approves trojanized versions of trusted extensions (Nx, ShadyPanda, QuickLens, Cyberhaven); no version-age/provenance/permission-delta signal; no pin/delay condition | **High** | High | **Yes** (both; coordinate shared pattern) |
| F2 | MV2 facts stale: Chrome MV2 already disabled + policy removed + CWS removal 2026-08-31; Edge retiring now; Chrome MV2 should mean Tier 3/unsupported, not MEDIUM EOL note | **High** | Medium-High | **Yes** (browser) |
| F3 | AI-editor forks install from Open VSX: Marketplace verification credited wrongly; namespace-squat + GlassWorm transitive-dependency attacks; Open VSX "slightly higher trust" unsupported; dependency review Tier-skipped | **High** | High | **Yes** (IDE) |
| F4 | Badge semantics wrong/over-weighted: Edge "Certified" → "Featured"; CWS Featured is manual + Established Publisher missing; badges carried malware; JetBrains verified vendor ≠ AMO Recommended | Medium-High | Medium-High | **Yes** (both) |
| F5 | Browser permission table misses MV3 injection/observation APIs (`scripting`, `userScripts`, `webRequest` non-blocking, `identity`, `webNavigation`, capture APIs…) | Medium | High | **Yes** (browser) |
| F6 | AI surface missing: VS Code `languageModelTools` / `mcpServerDefinitionProviders` / `chatParticipants` + agent-extension cross-ref; AI-key-handling plugins; browser content scripts on AI-chat domains; CWS July 2026 policy | Medium | Medium-High | **Yes** (both) |
| F7 | Conditions ignore enforceable controls: VS Code `extensions.allowed`, publisher trust, 2-h hold; Firefox `data_collection_permissions`; enterprise extension policies; `vim.pack`/lazy lockfiles | Medium | Medium | **Yes** (fold into F1 plans) |
| F8 | Stale mechanics: crxcavator, `update_url` misattribution, sideload realities, `postInstall`, `onStartupFinished`, packer, CVE/KEV, invisible-Unicode obfuscation | Low-Medium | Medium | **Yes** (fold into subject plans) |
| F9 | Coverage gaps: Safari, Chromium forks, Zed, MELPA, Visual Studio/Eclipse marketplaces | Low | Medium | No — memo/defer; Zed + MELPA worth a later scope decision |
| F10 | Eval gaps: no case for compromised version, ownership transfer, MV2-Chrome, Open VSX/fork, JetBrains, AI/MCP surface; eval 37 premise wording | Medium | High | **Yes** (STEWARDSHIP step 6, inside subject plans) |
| F11 | Shared-file defects found in passing: `references/registries.md` Cursor = VS Code Marketplace; `storage` LOW vs Medium mismatch | Low-Medium | High | Hand to orchestrator (shared scope, not this subject) |

**Opportunities:** a single cross-subject "Update & Version Integrity" section in `references/criteria.md` would serve browser-extension, ide-plugin, registry-package, ci-action and agent-extension at once.

---

## Recommendations

**Primary:** file two plan-projex — `browser-extension-rubric-refresh` (F1, F2, F4, F5, F6, F7, F8, F10-browser) and `ide-plugin-rubric-refresh` (F1, F3, F4, F6, F7, F8, F10-IDE). Each: edit workflow + addendum, add ≥2 eval cases, keep Tier 1 lean. Precede with (or include as step 1) a shared version-integrity block in `references/criteria.md` if the orchestrator confirms sibling evals found the same pattern.

**Conditional:**
- If sibling registry-package/ci-action evals report the same version-integrity gap → one shared plan first, subject plans reference it.
- If read-cost budget is tight → F1/F2/F3 only in this cycle; F5/F6/F8 next cycle.
- If live eval runs get approved → run 7 existing cases as baseline before editing, to separate regressions from rubric changes.

**Next steps:**
- Immediate (orchestrator): accept/reject findings; update STEWARDSHIP inventory (steps 7) and nav Phase 6 log (step 8) — this review did not edit them. Note `browser-extension` / `ide-plugin` Last Reviewed = 2026-10-16, Next Due = 2027-01-14 / 2027-02-13 on acceptance.
- Short-term: author the two plans; verify secondary-sourced facts (#6, #7, #17, #18, #19, #22) against vendor primaries from a network that resolves them.
- Long-term: decide Zed/MELPA/Safari scope; consider an event-trigger watchlist (KEV entries for extensions, store policy blogs) in STEWARDSHIP.

---

## Open Questions

- [ ] Has CWS actually completed MV2 removal (2026-08-31), or slipped?
- [ ] Exact Edge MV2 consumer/enterprise dates from Microsoft primary docs?
- [ ] Is Open VSX pre-publish scanning enforced today, and does it cover updates + dependency packs?
- [ ] Does VS Code Marketplace now offer CI-bound / trusted publishing (no PAT) post-Nx? None found.
- [ ] Is CRXcavator truly offline; which free manifest/CRX inspection path should the rubric name?
- [ ] Should Zed (sandboxed model) and MELPA be in ide-plugin scope or `generic`?
- [ ] Can an auditing agent reliably obtain "version published at" timestamps via search for CWS/AMO/Marketplace/Open VSX?

---

## Appendix

**Methodology:** STEWARDSHIP checklist steps 1–2 (read all four files end-to-end), step 3 (web search: 25+ queries on MV2, store policies, takeover/compromise campaigns, marketplace security features, forks, JetBrains, Neovim), step 4 offline (`validate`, `prepare --workflow browser-extension,ide-plugin`, `run --dry-run` into a scratch workspace outside the repo). Standard tier: moderate stakes (verdict correctness of two live workflows), significant ecosystem uncertainty, bounded scope.

**Sources consulted (external):** developer.chrome.com (MV2 timeline; CWS discovery; CWS policy updates 2026) · blog.google (CWS badges) · learn.microsoft.com (Edge extensions / Featured badge) · windowsreport.com, betanews.com (Edge MV2) · blog.mozilla.org/addons (data consent) · bleepingcomputer.com · thehackernews.com · infosecurity-magazine.com · stepsecurity.io · nx.dev postmortem · labs.cloudsecurityalliance.org · koi.ai · blog.jetbrains.com · code.visualstudio.com (runtime security, enterprise, AI extensibility) · infoq.com · alternativeto.net, heise.de (Neovim 0.12) · spin.ai, thenextgennexus.com (CRXcavator) · gdatasoftware.com · cyberinsider.com. Two vendor domains DNS-blocked from sandbox; their content seen only via search summaries.

**Dissenting view (steel-man):** "Rubrics are adequate; compromised-version attacks are rare, short-lived (Nx: minutes), and no install audit can predict them — adding checks just costs tokens." Partly valid: an audit cannot catch a version published after it runs. But (a) audits happen *at* install time, often minutes after a release — exactly the window; (b) the rubric's CONDITIONAL output is the right place to impose pinning/delay controls that *do* bound future-version risk; (c) ShadyPanda/Urban VPN were malicious for months while badged — not short-lived. Hence F1 stays High but the fix should be lean.

**Bias check:** reviewer primed toward finding staleness (task framing); mitigated by noting what still holds (Firefox MV2, permission framing, impersonation checks, all 7 eval expectations).

**Iteration history:**

| Date | Mode | Scope | Summary |
|---|---|---|---|
| 2026-10-16 | Initial | browser-extension + ide-plugin stewardship pass | 11 findings; 2 subject plans recommended |
