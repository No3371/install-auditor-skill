# IDE-Plugin Rubric Refresh

> **Status:** Complete
> **Completed:** 2026-10-16
> **Walkthrough:** 2610162003-ide-plugin-rubric-refresh-walkthrough.md
> **Author:** Claude (Opus)
> **Parent:** 2610161927-browser-extension-ide-plugin-stewardship-review-eval.md
> **Source:** 2610161927-browser-extension-ide-plugin-stewardship-review-eval.md (F1, F3, F4, F6, F7, F8, F10-IDE, F11 Cursor row) | 2610161941-shared-version-integrity-floor-plan.md (Hand-off rows "browser-extension / ide-plugin" + "§4.3 plug-in") | human decision C6 (via orchestrator)
> **Related Projex:** 2610161941-shared-version-integrity-floor-plan.md (Requires; the §4.6 / §4.3 contract) | 2610161927-agent-extension-stewardship-review-eval.md (agent-extension owns the 8a/8c rubric this plan cross-links) | 2610161927-registry-package-and-ci-action-stewardship-review-eval.md (registry plan owns other `references/registries.md` rows) | 2604070218-install-auditor-subject-typed-redesign-nav.md
> **Worktree:** Yes
> **Log:** 2610162003-ide-plugin-rubric-refresh-log.md

---

## Summary

The ide-plugin rubric scores trust per extension: installs, "Verified" badge, publisher. Two 2025–26 patterns defeat that. (1) A trusted publisher ships one hijacked version (Nx Console 18.95.0, May 2026: verified publisher, CVE-2026-48027, CISA KEV). (2) VS Code forks (Cursor, Windsurf, VSCodium) install from **Open VSX**, where Marketplace "Verified" does not apply and namespaces can be unclaimed or squatted; GlassWorm used `extensionPack` / `extensionDependencies` there to pull payloads after review. The rubric also lacks VS Code's AI contribution points, cites stale mechanics (`postInstall`, packer, "IDE plugins rarely have CVEs"), and offers "monitor" conditions while VS Code now has enforceable controls (`extensions.allowed`, `extensions.autoUpdateDelay`).

This plan fills the ide-plugin plug-ins of the shared §4.6 floor and §4.3 CVE scope, rewires trust signals to the **registry the editor actually installs from**, adds AI-surface and dependency-pack scoring, replaces "monitor" conditions with update controls, and fixes the `references/registries.md` Cursor row. All VS Code / Open VSX / Neovim platform facts were checked against primary docs at planning (see Fact Ledger).

**Scope:** `references/criteria/ide-plugin.md` | `workflows/ide-plugin.md` | `references/registries.md` (Cursor row only). No `SKILL.md`, `references/criteria.md`, evals, scripts or `STEWARDSHIP.md`.
**Estimated Changes:** 3 files, 37 exact replacements. Addendum 6,203 → 13,183 B; workflow 15,760 → 20,864 B; registries 4,413 → 4,664 B (simulated).

---

## Objective

### Problem / Gap / Need

| ID (review) | Gap | Fix (step) |
|---|---|---|
| F1 / A1 | Tier 1 has no version check; addendum has no §4.6 plug-ins | Addendum `## Version & Update Integrity (§4.6)` V1–V5 (1h); Tier 1 bullet "§4.6 raises nothing" (1g); workflow version-integrity research + coverage row (2r, 2t) |
| F3 / A4 | Fork installs credited with Marketplace "Verified"; Open VSX "slightly higher trust"; dependency review Tier-skipped; `registries.md` Cursor = VS Code Marketplace | Trust table: fork row, Open VSX verified/unverified semantics, `namespace mismatch` HIGH / Impersonation (1b); install-registry rule (2d, 2e); Tier 1 install count + identity on install registry (1g); dependency/pack review at every tier (1c, 1e, 2q, 2t); registries rows (3a) |
| F4 / A3 | JetBrains verified vendor = "AMO Recommended"; VS Code Verified = "CWS Featured"; badges over-weighted | Identity-only framing, V2 weights, JetBrains vendor → moderate (1b); 4.1 bullet (2u) |
| F6 / A6 | No `languageModelTools` / `mcpServerDefinitionProviders` / chat contributions; no MCP pointer despite classifier routing MCP-via-extension → ide-plugin; AI-key plugins | Capability rows (1c, 1d), scoring (1e), Tier 1/3 (1g, 1h), Q2/Q9 (2l, 2p), 4.4 (2w), CONDITIONAL rows (2z); cross-link `workflows/agent-extension.md` 8a |
| F7 / A7 | "Monitor" conditions; no update controls | V5 controls (1h); CONDITIONAL rewrites (2z); 4.5 (2x) |
| F8 / A8 | `postInstall`; `onStartupFinished` missing as always-on; packer current; "rarely have formal CVEs"; no obfuscation check | 2m, 1c/1e/2q/2w, 1a/2b, 2v, 2r |
| C6 (shared) | Addendum has no own-code / third-party line | `## CVE Scope (§4.3)` (1h); 2v points to it and to `SKILL.md` "Blocking CVE" |
| A9 (shared contract) | Workflow coverage table lacks canonical Required rows (typosquat, license) | 2t adds them + mapping note for the rest |

### Success Criteria

- [ ] `references/criteria/ide-plugin.md` has exactly one `## Version & Update Integrity (§4.6)` heading with one bullet each `- **V1** —` … `- **V5** —`, and exactly one `## CVE Scope (§4.3)` heading.
- [ ] Every `§4.6 V<n>` reference in the 3 files names V1–V5, and those headings exist in the landed `references/criteria.md` §4.6.
- [ ] Stale phrases absent from addendum + workflow (case-insensitive, whitespace-normalized): `rarely have formal CVEs` | `` `postInstall` `` | `slightly higher trust` | `(equivalent to AMO Recommended)` | `(equivalent to CWS Featured)` | `DNS-linked namespace` | `increases confidence` | `monitor for incidents` | `monitor for supply-chain` | `monitor for acquisition` | `vim-plug, packer)` | `/ packer)` | `in v1`.
- [ ] `references/registries.md` no longer contains `Cursor extensions (VS Code compatible)`; it has the `Open VSX (open-vsx.org)` and `VS Code forks (Cursor, Windsurf, VSCodium, …)` rows; no other line of that file changed.
- [ ] Workflow coverage table carries `Version integrity (§4.6)`, `Typosquat / impersonation check`, `License compatibility` (Required ×3) and `Extension dependency review` = `Required if present` ×3.
- [ ] Byte budget: addendum ≤ 13,400 B; workflow ≤ 21,100 B (simulated 13,183 / 20,864; ~220 B slack each).
- [ ] Workflow prose lines (non-table) ≤ 80 columns.
- [ ] `python3 evals/run_evals.py validate` passes; `python3 -m unittest discover -s evals -p "test_*.py"` passes with the Preflight test count.
- [ ] Paper traces I1–I10 produce the stated verdicts.
- [ ] `git diff --stat <base>..HEAD` lists exactly the 3 files.

### Out of Scope

- `references/criteria.md`, `SKILL.md`, `references/report-template.md` (shared plan 2610161941; this plan only consumes its contract).
- Other rows of `references/registries.md`, incl. the IDE table's VS Code Marketplace / JetBrains rows (registry-package plan owns package rows; the JetBrains "Medium-High (JetBrains review process)" row is arguably optimistic, flagged to the orchestrator, not edited — the addendum wins for ide-plugin audits anyway).
- `references/classifier.md` (still lists `packer spec` as an ide-plugin signal — harmless as a routing signal; flagged, not edited).
- The agent-extension rubric itself (8a/8c content). This plan only points to `workflows/agent-extension.md` 8a.
- F9 coverage gaps: Zed (WASM-sandboxed extensions), Emacs MELPA, Visual Studio / Eclipse marketplaces → defer; scope decision for the orchestrator.
- `evals/` (eval-refresh plan; see Notes → Eval Hand-off). No live `run_evals.py run` (one paid run after all refreshes, per human decision).
- `STEWARDSHIP.md` inventory dates (orchestrator).

---

## Context

### Current State

- `references/criteria/ide-plugin.md` (6,203 B, unchanged in substance since 2026-04-15): trust table with Marketplace badge as the trust unit, Open VSX "slightly higher trust", JetBrains verified vendor = "AMO Recommended"; VS Code capability table without AI contribution points, `extensionPack`/`extensionDependencies` or `onStartupFinished`; Tier 1 = 500K installs + verified publisher + 1 y; no §4.6 / §4.3 plug-in.
- `workflows/ide-plugin.md` (15,760 B): Identify table has no fork row and no "which registry" rule; Q4 cites `postInstall`; Q5 says cross-listing "increases confidence"; 4.3 says plugins "rarely have formal CVEs"; coverage table Tier-skips dependency review at Tier 1 and lacks typosquat / license / version rows; conditions say "monitor".
- `references/registries.md:72`: `| Cursor extensions (VS Code compatible) | Same as VS Code Marketplace |`.
- Shared contract (2610161941; it landed on base as `20843cc` and closed while this plan was drafted, so the headings below were re-checked against the landed `references/criteria.md`): adds `references/criteria.md` §4.6 V1–V5 with `**Addendum:**` plug-in lines, the per-addendum heading `## Version & Update Integrity (§4.6)` with bullets `V1`–`V5`, §4.3 C6 table + `**Addendum:**` line ("draws the own-code / third-party line … names its scan and VEX sources"), `SKILL.md` "Blocking CVE", Tier 1 intro hook, and the coverage-row contract (workflow tables add rows, never drop Required ones). It does not name a heading for the §4.3 plug-in; this plan uses `## CVE Scope (§4.3)`, the name most sibling refresh plans use.
- `references/classifier.md` routes "MCP server installed via a VS Code extension" → ide-plugin and lets the routed workflow borrow sibling sub-steps without re-routing.
- Evals on ide-plugin: 16 Prettier (exact APPROVED), 17 sideloaded VSIX (exact REJECTED), 28 GitLens (APPROVED|CONDITIONAL), 37 rust-analyzer (exact APPROVED). None asserts on tier names, coverage rows or trust-table wording.

### Fact Ledger (verified at planning, 2026-10-16)

Primary = vendor docs read directly (`microsoft/vscode-docs` clone, last commit 2026-10-16; `eclipse/openvsx.wiki` clone, 2026-10-01; `neovim` tag `v0.12.0` `runtime/doc`; `wbthomason/packer.nvim` README). Secondary = search-engine summaries of news / vendor blogs.

| Fact used in rubric | Source | Type |
|---|---|---|
| Verified publisher = domain ownership + ≥ 6 months good standing | vscode-docs `extension-runtime-security.md`, `publishing-extension.md` | Primary |
| Publisher-trust prompt since 1.97; CLI installs not auto-trusted; trusting a pack's publisher trusts its dependencies' publishers | `extension-runtime-security.md` | Primary |
| Marketplace: malware scan per new version + update, dynamic detection, name-squat protection, block list with auto-uninstall, Marketplace signs every package, secret scanning | `extension-runtime-security.md` | Primary |
| `extensions.allowed` since 1.96: publisher / extension / version / platform; no ranges; `"stable"`; `AllowedExtensions` policy | vscode-docs `docs/enterprise/extensions.md` | Primary |
| 1.123 (2026-06-03): 2-h auto-update delay; trusted publishers (Microsoft, GitHub, OpenAI) exempt | `release-notes/v1_123.md` | Primary |
| 1.125 (2026-06-17): `extensions.autoUpdateDelay` (hours, default 2); `extensions.autoUpdate` = `on`/`off`; both policy-manageable | `release-notes/v1_125.md` | Primary |
| Contribution points `languageModelTools`, `languageModelChatProviders` (API-key config), `chatAgents`, `chatInstructions`, `chatPromptFiles`, `chatSkills`; `chatParticipants`; `mcpServerDefinitionProviders` | `api/references/contribution-points.md`, `api/extension-guides/ai/chat.md`, `.../ai/mcp.md` | Primary |
| Extension tools always get a confirmation dialog; user can "Always Allow" | `api/extension-guides/ai/tools.md` | Primary |
| `onStartupFinished` ≈ `*` but deferred | `api/references/activation-events.md` | Primary |
| No install hook; `vscode:uninstall` script; `vscode:prepublish` | `api/references/extension-manifest.md` | Primary |
| Open VSX verified = publishing user is member of a namespace with ≥ 1 owner; else unverified + warning; creating a namespace ≠ ownership; `@open-vsx` service account republishes upstream extensions | openvsx.wiki `Namespace-Access.md`, `Publishing-Extensions.md` | Primary |
| Open VSX publish checks: secret detection, hash blocklist, namespace similarity; operator-configured, may be monitor-only | openvsx.wiki `Extension-Scanning.md` | Primary |
| Neovim 0.12 `vim.pack` (experimental), lockfile `$XDG_CONFIG_HOME/nvim/nvim-pack-lock.json` | neovim `v0.12.0` `runtime/doc/pack.txt` | Primary |
| packer.nvim unmaintained since Aug 2023 | packer.nvim README | Primary |
| Cursor's in-app library uses Open VSX (mid-2025); same ID can differ per registry; vendor ("Anysphere") rebuilds of some extensions | Cursor forum + cursor.com docs via search summary | Secondary (multiple) |
| VSCodium defaults to Open VSX; Windsurf docs point to Open VSX; Antigravity likely Open VSX | VSCodium docs, Windsurf docs via search; Antigravity single blog | Secondary (Antigravity weak → not named in rubric) |
| Nx Console 18.95.0 hijack (May 2026), CVE-2026-48027, CISA KEV | MITRE CVE API entry + aggregators via search | Secondary (multiple) |
| GlassWorm `extensionPack`/`extensionDependencies` delayed payload on Open VSX (2026) | THN / Socket, CSA, InfoWorld via search | Secondary (multiple) |
| Fork recommendation lists → unclaimed Open VSX namespaces (Koi, Dec 2025) | BleepingComputer via search | Secondary |
| JetBrains: 15 AI-key-stealing plugins, 7 vendor accounts (June 2026); Plugin Verifier = compatibility checker | JetBrains blog, BleepingComputer, THN via search | Secondary (multiple, incl. vendor) |

Rubric text names only primary-verified product facts with versions/settings; secondary facts appear as patterns without dates, except the Nx and JetBrains examples, which multiple independent sources confirm.

### Key Files

| File | Role | Change Summary |
|------|------|----------------|
| `references/criteria/ide-plugin.md` | ide-plugin scoring addendum | Header precedence; trust table + identity scoring; capability rows (activation, deps/packs, AI); JetBrains AI-key row; binary uninstall-hook row; Tier 1/3; new `## CVE Scope (§4.3)` + `## Version & Update Integrity (§4.6)` |
| `workflows/ide-plugin.md` | Type 3 workflow | Install-registry rule + fork row; version metadata; research Q1/Q2/Q4/Q5/Q6/Q9; manifest keys; version-integrity research; coverage table; 4.1/4.3/4.4/4.5; verdict notes |
| `references/registries.md` | Shared source-trust table | Cursor row → Open VSX row + VS Code forks row |

### Dependencies

- **Requires:** 2610161941-shared-version-integrity-floor-plan.md executed and closed onto base `claude/youthful-dijkstra-5ov1kt`. Satisfied at planning (`20843cc`; walkthrough in `.projex/closed/`); Preflight re-checks. Its contract headings are referenced verbatim.
- **Concurrent (file-adjacent):** registry-package refresh plan (edits other `references/registries.md` rows; this plan replaces only the Cursor line — on conflict keep both sides); browser-extension refresh plan (edits browser rows of the same file); agent-extension refresh plan (owns `workflows/agent-extension.md`; this plan depends only on the 8a sub-type label existing).
- **Blocks:** eval-refresh plan (new ide-plugin cases, Notes → Eval Hand-off); the single paid live eval run.

### Constraints

- Read cost: both files load on every ide-plugin audit. Budget fixed in Success Criteria; trims were already applied in simulation (incident narratives removed from tables, V-bullets compressed).
- §4.6 is a floor: the addendum may only tighten or fill plug-ins (shared contract, `SKILL.md` Precedence).
- §4.3 Addendum line: may draw the own-code line and name sources, may not change verdict classes.
- Style: workflow prose wraps ≤ 80 cols (tables exempt); addendum tables are long-line, prose wraps ~76.
- No projex filenames in shipped files.

### Assumptions

- **B1:** The shared plan lands with its planned headings: `## 4.6 Version & Update Integrity (shared floor)`, `### V1`…`### V5`, §4.3 `**Addendum:**` line, `SKILL.md` "Blocking CVE". **Verify in Preflight;** a renamed heading → re-anchor references here (text-only), a missing section → stop (Blocked).
- **B2:** No other plan edits `workflows/ide-plugin.md` or `references/criteria/ide-plugin.md` before execution; registry / browser plans touch only their own `references/registries.md` lines. All 37 old strings matched exactly once at `cdd8ee2` (simulated). A miss → re-read that region and re-anchor, don't improvise wording.
- **B3:** `workflows/agent-extension.md` still defines sub-type "8a" (MCP server) after the agent-extension refresh. If renamed, update the two pointers (1c, 2l) to the new label.
- **B4:** No eval assertion depends on removed wording (verified: ide-plugin assertions are concept-level on routing, verdict, sideload, GitKraken, bundled binary).

### Impact Analysis

- **Direct:** the 3 files.
- **Adjacent:** `references/classifier.md` edge case "MCP server via VS Code extension → ide-plugin" now has a rubric path (8a sub-rubric); `references/criteria.md` §4.6/§4.3 now have ide-plugin plug-ins.
- **Downstream (live audit behavior):**
  - Fork installs (Cursor etc.) are scored on the Open VSX listing: lower install counts → more Tier 2; unverified namespace → MEDIUM; mismatched owner → HIGH / REJECTED as impersonation.
  - Extensions with `languageModelTools` / `mcpServerDefinitionProviders` or AI-key collection lose Tier 1.
  - Extension packs / dependencies are reviewed at every tier.
  - JetBrains vendor accounts weigh moderate, not strong.
  - Conditions now name enforceable controls instead of "monitor".
  - Evals 16/37 stay APPROVED (no AI surface, Marketplace install, own-code bundled binary); 28 stays in APPROVED|CONDITIONAL; 17 stays REJECTED. Time-dependent V1 effects are the shared plan's hand-off.

---

## Implementation

### Overview

Preflight → addendum (Step 1: the rules) → workflow (Step 2: the procedure that cites them) → `registries.md` row (Step 3). Every change is an exact `Before → After` pair; apply with the Edit tool per pair, in order. Each Before occurs exactly once in its file at `cdd8ee2` (simulated, all 37 matched). "Before" blocks are verbatim file text; the leading `// Before:` / `// After:` labels are not file content.

**Preflight** (run from `<work-root>` after rebasing / creating the worktree on the post-2610161941 base):

```bash
ls .projex/closed/ | grep 2610161941-shared-version-integrity-floor        # plan + walkthrough present
grep -c "^## 4.6 Version & Update Integrity (shared floor)" references/criteria.md   # 1
grep -c "^### V[1-5] " references/criteria.md                              # 5
grep -n "^- \*\*Addendum:\*\*" references/criteria.md                      # 6 lines; one in §4.3
grep -c "Blocking CVE" SKILL.md                                            # ≥ 1
grep -n "Version & Update Integrity (§4.6)" references/criteria.md         # plug-in heading convention as planned
grep -n "8a" workflows/agent-extension.md | head -3                        # B3
grep -c "Cursor extensions (VS Code compatible)" references/registries.md  # 1
git log --oneline cdd8ee2..HEAD -- workflows/ide-plugin.md references/criteria/ide-plugin.md   # empty (B2)
python3 evals/run_evals.py validate | head -3                              # pass
python3 -m unittest discover -s evals -p "test_*.py" 2>&1 | tail -3        # record test count
```

**Stop rule:** §4.6 heading or V-headings missing → set this plan `Blocked` (waiting on 2610161941) and do not edit. Plug-in heading convention differs from `## Version & Update Integrity (§4.6)` → use the landed one in 1a/1h and the consistency script. Shared plan names a heading for the §4.3 plug-in → use it instead of `## CVE Scope (§4.3)` (1h, 2v).

---

### Step 1: Addendum `references/criteria/ide-plugin.md`

**Objective:** encode the rules: install-registry trust, identity-only badge weights, AI / dependency capability rows, Tier 1/3 changes, §4.3 and §4.6 plug-ins.
**Confidence:** High (facts primary-verified); Medium for risk levels and the Open VSX weights (policy judgment; see Risks)
**Depends on:** Preflight
**Do-Projex:** Encouraged
**Verify-Projex:** Encouraged

**Files:** `references/criteria/ide-plugin.md`

**Changes:** 8 exact replacements.

**1a — header**

````markdown
// Before:
Per-subject scoring extensions for **Type 3: ide-plugin** audits.
Layers on top of `references/criteria.md`. More-specific guidance wins.

Covers: VS Code Marketplace, Open VSX, JetBrains Marketplace, Sublime
Package Control, Neovim plugin managers (lazy.nvim, vim-plug, packer).
Depth is VS Code Marketplace-first in v1.

// After:
Per-subject scoring extensions for **Type 3: ide-plugin** audits.
Layers on top of `references/criteria.md`. More-specific guidance wins,
except over the §4.6 version-integrity floor, which this file only
tightens or fills (`## Version & Update Integrity (§4.6)` below).

Covers: VS Code Marketplace, Open VSX, VS Code forks (Cursor, Windsurf,
VSCodium and similar editors that install from Open VSX or their own
gallery), JetBrains Marketplace, Sublime Package Control, Neovim plugin
managers (lazy.nvim, vim-plug, built-in `vim.pack`; packer.nvim is
unmaintained). Depth is VS Code Marketplace-first.
````

**1b — Marketplace Trust Signals table + its Scoring impact**

````markdown
// Before:
## Marketplace Trust Signals

| Marketplace | Verified Publisher Signal | Adoption Metric | Trust Notes |
|-------------|--------------------------|-----------------|-------------|
| VS Code Marketplace | "Verified" badge (DNS-linked namespace) | Install count + rating | Microsoft-operated; largest catalog; review exists but is not exhaustive |
| Open VSX | Namespace ownership (Eclipse Foundation) | Install count | Open-source alternative; cross-listed extensions slightly higher trust |
| JetBrains Marketplace | "JetBrains" badge (first-party), verified vendor | Downloads + rating | JetBrains review process; paid plugins undergo additional review |
| Sublime Package Control | None (community index) | GitHub stars / installs shown on packagecontrol.io | No publisher verification; relies on community policing |
| Neovim (lazy.nvim / vim-plug / packer) | None (GitHub-sourced) | GitHub stars + forks | No marketplace; trust derived entirely from repo reputation |
| Sideloaded (VSIX / ZIP / manual) | None | None | No marketplace verification; highest baseline risk |

### Scoring impact

- VS Code "Verified" publisher = moderate positive (equivalent to CWS Featured)
- JetBrains first-party or verified vendor = strong positive (equivalent to AMO Recommended)
- Open VSX namespace + VS Code Marketplace cross-listing = moderate positive
- Sublime Package Control listing = weak positive (no verification gate)

// After:
## Marketplace Trust Signals

Read trust signals from the registry the **target editor installs from**,
for the version to be installed. A badge on another registry does not
transfer.

| Marketplace | Identity signal (§4.6 V2) | Adoption Metric | Trust Notes |
|-------------|---------------------------|-----------------|-------------|
| VS Code Marketplace | "Verified": domain ownership + ≥ 6 months good standing | Install count + rating | Microsoft-operated; malware scan per version; block list auto-uninstalls. Package signature = registry integrity, not authorship |
| Open VSX | *Verified* only if the publishing user belongs to a namespace with an owner; else *unverified* + warning | Install count | Eclipse Foundation. Creating a namespace grants no ownership. Publish checks are operator-configured, may be monitor-only; weaker than Marketplace review |
| VS Code forks (Cursor, Windsurf, VSCodium, …) | Those of the fork's registry (usually Open VSX), **never** Marketplace "Verified" | Install count on that registry | Check which registry the editor uses. One `publisher.name` can mean different code, or an editor-vendor rebuild, per registry |
| JetBrains Marketplace | "JetBrains" (first-party); vendor account | Downloads + rating | Manual review, but the Plugin Verifier is a compatibility checker, not anti-malware (JetBrains, June 2026) |
| Sublime Package Control | None (community index) | GitHub stars / installs shown on packagecontrol.io | No publisher verification; relies on community policing |
| Neovim (lazy.nvim / vim-plug / `vim.pack`) | GitHub owner only | GitHub stars + forks | No marketplace; trust derived from repo reputation and the pinned commit |
| Sideloaded (VSIX / ZIP / manual) | None | None | No marketplace verification; highest baseline risk |

### Scoring impact

Badges and namespaces establish **identity**, not code integrity
(`references/criteria.md` §4.6 V2). None offsets a §4.6 flag or a Red Flag.

- VS Code "Verified" publisher = moderate positive
- JetBrains first-party = strong positive; JetBrains vendor account =
  moderate positive (identity only, not a code review)
- Open VSX *verified* namespace owned by the same entity as the
  Marketplace publisher of the same ID = moderate positive
- Open VSX *unverified* version = no credit + MEDIUM flag
  `unverified namespace`
- Namespace owned (or version published) by an account other than the
  Marketplace publisher of the same ID or a near-identical name = HIGH
  flag `namespace mismatch` (squat pattern; a squatter can hold a
  *verified* namespace). If the user asked for the well-known plugin, it
  is the workflow's Impersonation case → REJECTED
- Published by the `@open-vsx` service account (upstream republish) = no
  Tier 1 identity credit; Tier 2 confirms the upstream repo and tag
- Sublime Package Control listing = weak positive (no verification gate)
````

**1c — VS Code capability table: activation row + new rows**

````markdown
// Before:
| Custom editor / webview | Medium | Renders arbitrary HTML/JS inside the editor |
| `*` activation event | Medium | Plugin loads on every editor start (broader attack surface than targeted activation) |

// After:
| Custom editor / webview | Medium | Renders arbitrary HTML/JS inside the editor |
| `*` or `onStartupFinished` activation event | Medium | Code runs on every editor start (`onStartupFinished` only defers it until startup finishes) |
| `extensionDependencies` / `extensionPack` | Medium-High | Installs other extensions, maybe from other publishers; a later update can add or swap one (delayed payload) |
| `languageModelTools` | Medium-High | Agent-invokable tools with full extension-host privileges; users can "Always Allow" past the per-call prompt |
| `mcpServerDefinitionProviders` | Medium-High | Registers MCP servers the agent runs; apply `workflows/agent-extension.md` 8a signals to each |
| `chatParticipants` / `chatAgents` / `chatInstructions` / `chatPromptFiles` / `chatSkills` | Medium | Injects prompts, instructions or agents into chat |
| `languageModelChatProviders` | Medium-High | Sends prompts and code context to the extension's model backend; may take API keys |
````

**1d — JetBrains capability table: AI-key row**

````markdown
// Before:
| Custom compiler / build tool integration | High | Executes build pipelines |

// After:
| Custom compiler / build tool integration | High | Executes build pipelines |
| Settings that accept AI-provider API keys or tokens | High | Attacker-preferred category (June 2026 campaign sent keys to its own server on "Apply"); check where the key is sent |
````

**1e — capability Scoring impact bullets**

````markdown
// Before:
- `*` activation (VS Code) or `postStartupActivity` (JetBrains) = note
  as always-active
- Remote plugin / RPC (Neovim) = medium — inspect what processes are spawned

// After:
- `*` / `onStartupFinished` activation (VS Code) or `postStartupActivity`
  (JetBrains) = note as always-active
- Remote plugin / RPC (Neovim) = medium — inspect what processes are spawned
- `extensionDependencies` / `extensionPack` present = review every listed
  extension at the same tier, identity (§4.6 V2) included; one from a
  different publisher that fails that review = HIGH flag
- AI surface (`languageModelTools`, `mcpServerDefinitionProviders`, chat
  contributions, model providers) = elevated review; agent-reachable tools
  or servers the stated purpose does not explain = HIGH flag
- Plugin collects AI-provider API keys or tokens (any editor) = check where
  the key is sent; an endpoint other than the provider's documented API,
  or a publisher who is neither the provider nor a known project = HIGH
  flag
````

**1f — binary table: uninstall-script row**

````markdown
// Before:
| Plugin compiles from source on install | Medium | Transparent but may execute untrusted build scripts |

// After:
| Plugin compiles from source on install | Medium | Transparent but may execute untrusted build scripts |
| `scripts.vscode:uninstall` (VS Code) | Low-Medium | Runs a Node script on uninstall; check what it deletes or contacts. VS Code has no install hook: downloads happen in activation code |
````

**1g — Tier 1 criteria**

````markdown
// Before:
- Install count >= 500K on primary marketplace
- Verified publisher (VS Code) or JetBrains first-party / verified vendor
- Publisher is a known company or well-known open-source project
- Capabilities are proportional to stated purpose
- No bundled/downloaded binary with opaque provenance
- No known incidents or marketplace removals
- Listed >= 1 year

// After:
- Install count >= 500K on the registry the target editor installs from
- Identity credit on that registry: VS Code "Verified" publisher,
  JetBrains first-party / vendor account, or (Open VSX / forks) a
  *verified* namespace owned by the Marketplace publisher of the same ID
- Publisher is a known company or well-known open-source project
- Capabilities are proportional to stated purpose
- No bundled/downloaded binary with opaque provenance
- No `extensionDependencies` / `extensionPack`, or each listed extension
  meets Tier 1 itself
- No agent-reachable AI surface (`languageModelTools`,
  `mcpServerDefinitionProviders`) and no AI-provider key collection
- No known incidents or marketplace removals
- Listed >= 1 year
- `references/criteria.md` §4.6 raises nothing (it bars Tier 1 for a
  version < 7 d old, of unknown age, or with a continuity break)
````

**1h — Tier 3 triggers + new §4.3 / §4.6 plug-in sections (end of file)**

````markdown
// Before:
- Plugin requests `*` activation with broad capability scope
- Plugin integrates debugger/terminal/task runner with unclear justification

// After:
- Plugin requests `*` or `onStartupFinished` activation with broad
  capability scope
- Plugin integrates debugger/terminal/task runner with unclear justification
- `namespace mismatch` flag (Open VSX / fork registry)
- Plugin collects AI-provider API keys and the publisher is neither the
  provider nor a known project
- `extensionDependencies` / `extensionPack` names an extension from a
  different, unverified publisher

## CVE Scope (§4.3)

- **Own code:** the plugin bundle its publisher ships, plus binaries the
  same project builds and bundles (e.g. rust-analyzer's language server).
- **Third-party component:** bundled libraries (npm, Maven, PyPI) and
  binaries from other projects that the plugin bundles or downloads.
- **Sources:** GHSA / OSV / NVD for the plugin and bundled libraries;
  CISA KEV for every CRITICAL (a hijacked extension release can be
  KEV-listed); publisher advisories (VEX only if they meet the §4.3 test).

## Version & Update Integrity (§4.6)

- **V1** — Publish time: the version's date on the install registry
  (Marketplace version history, Open VSX version page, JetBrains
  "Versions" tab; tag/commit date for Git-sourced plugins). Version unit:
  `publisher.name@x.y.z` (platform-specific VSIX builds = one unit);
  JetBrains plugin version; commit SHA for Git-sourced plugins. Cooldown:
  VS Code `extensions.autoUpdateDelay` (hours; VS Code ≥ 1.125). Its 2 h
  default is below 72 h and exempts trusted publishers (e.g. Microsoft,
  GitHub), so set it explicitly; on a fork that ignores it, turn
  auto-update off.
- **V2** — Mechanisms and weights: `## Marketplace Trust Signals`.
  Expected identity: the publisher ID / Open VSX namespace owner of prior
  versions, or the one the upstream repo names. Marketplace package
  signature → note only. Absence: *unverified* namespace = MEDIUM;
  `namespace mismatch` = HIGH. No curated pipelines.
- **V3** — Diff `package.json` / `plugin.xml` against the prior release
  (repo tags, or both packages; a VSIX is a ZIP): new `contributes`
  (above all AI surface, `terminal`, `debuggers`, `taskDefinitions`),
  broader `activationEvents`, changed `extensionDependencies` /
  `extensionPack`, new binaries or download URLs. Publisher or namespace
  transfer = MEDIUM; HIGH with a capability increase in the same release.
- **V4** — Extra sources: Marketplace block-list removals, Open VSX /
  Eclipse takedowns, JetBrains Marketplace security posts, security-vendor
  research on extension campaigns.
- **V5** — Triggers: new AI-surface contribution; changed
  `extensionDependencies` / `extensionPack`; namespace or publisher
  transfer; switching to an editor on another registry. Update controls:
  VS Code `extensions.allowed` (≥ 1.96; exact versions, no ranges; org-wide
  via the `AllowedExtensions` policy), `extensions.autoUpdate` off or
  `extensions.autoUpdateDelay`; JetBrains / Sublime: automatic plugin
  updates off; Neovim: committed `lazy-lock.json` / `nvim-pack-lock.json`
  or a vim-plug `commit` / `tag` pin.
````

**Rationale:**
- **1b — install-registry rule + identity framing.** The A4 failure is a category error: Marketplace "Verified" was credited for installs that come from Open VSX. Weights now attach to the registry the editor uses. Badges stay as information (steel-man in review A3) but carry only identity weight, so they never offset a §4.6 flag.
- **Open VSX weights.** *Unverified* is common for legitimate extensions (e.g. `@open-vsx` republishes), so it is MEDIUM, not HIGH. The attack pattern (namespace squatting on a Marketplace ID) is the owner mismatch → HIGH, and REJECTED via Impersonation when the user asked for the well-known plugin.
- **JetBrains vendor → moderate.** A vendor account is identity; the June 2026 campaign passed review under 7 vendor accounts. First-party stays strong.
- **1c/1e AI rows.** All contribution names were checked in the current VS Code docs. Tools and MCP servers are Medium-High, not High: every extension already runs with full host privileges. The new risk is agent reachability (prompt injection) plus "Always Allow". HIGH is reserved for "unexplained by the stated purpose".
- **1g Tier 1.** Install count on the install registry: Marketplace adoption says nothing about the code Open VSX serves for that ID. Packs and AI surface leave Tier 1 because both are the 2026 attack paths and need more than a glance.
- **1h V1.** The 2-h VS Code default is far below the 72-h floor and exempts trusted publishers, so the condition must set the delay explicitly.
- **1h V2.** No curated pipelines for ide-plugin: the Marketplace signature is registry-level and was present on the hijacked Nx release.
- **CVE Scope.** rust-analyzer's server is the same project's code, so it is own code; eval 37 stays consistent.
- **Rejected alternatives.**
  - A separate "AI surface" section: more bytes, and it duplicates the capability table's purpose.
  - Naming Antigravity: single weak source.
  - Pinning Open VSX scanning dates: the Eclipse rollout and the Koi bypass are secondary, and the wiki says checks are operator-configured.

**Verification:**
```bash
grep -c "^## Version & Update Integrity (§4.6)$" references/criteria/ide-plugin.md   # 1
grep -c "^## CVE Scope (§4.3)$" references/criteria/ide-plugin.md                  # 1
grep -cE "^- \*\*V[1-5]\*\* — " references/criteria/ide-plugin.md                   # 5
grep -ci "slightly higher trust\|equivalent to amo recommended)\|dns-linked" references/criteria/ide-plugin.md   # 0
wc -c < references/criteria/ide-plugin.md                                          # ≤ 13400 (sim 13183)
```

**If this fails:** `git -C <work-root> checkout -- references/criteria/ide-plugin.md`, then redo the pairs in order.

---

### Step 2: Workflow `workflows/ide-plugin.md`

**Objective:** make the procedure resolve the install registry, collect version data, inspect AI and dependency surface, carry the canonical and §4.6 coverage rows, and state enforceable conditions.
**Confidence:** High
**Depends on:** Step 1 (it references the addendum's headings, flags and plug-ins)
**Verify-Projex:** Encouraged

**Files:** `workflows/ide-plugin.md`

**Changes:** 28 exact replacements (2a–2ab). Wrap ≤ 80 columns, as written.

**2a — header comment**

````markdown
// Before:
Handles IDE/editor plugins from VS Code Marketplace, Open VSX, JetBrains
Marketplace, Sublime Package Control, and Neovim plugin managers.
VS Code Marketplace-first in v1.

// After:
Handles IDE/editor plugins from VS Code Marketplace, Open VSX (incl. VS
Code forks such as Cursor), JetBrains Marketplace, Sublime Package
Control, and Neovim plugin managers. VS Code Marketplace-first.
````

**2b — intro**

````markdown
// Before:
This workflow handles **Type 3: ide-plugin** subjects from VS Code
Marketplace, Open VSX, JetBrains Marketplace, Sublime Package Control,
and Neovim plugin managers (lazy.nvim, vim-plug, packer). Primary depth
in v1 is VS Code Marketplace because it is the largest ecosystem and
the repo's trust references are VS Code-heavy.

// After:
This workflow handles **Type 3: ide-plugin** subjects from VS Code
Marketplace, Open VSX (usually the registry behind VS Code forks such as
Cursor, Windsurf and VSCodium), JetBrains Marketplace, Sublime Package
Control, and Neovim plugin managers (lazy.nvim, vim-plug, built-in
`vim.pack`). Primary depth is VS Code Marketplace because it is the
largest ecosystem and the repo's trust references are VS Code-heavy.
````

**2c — addendum precedence**

````markdown
// Before:
and scoring. When it conflicts with the shared rubric, the more specific
ide-plugin guidance wins.

// After:
and scoring. When it conflicts with the shared rubric, the more specific
ide-plugin guidance wins, except that it can only tighten the
`references/criteria.md` §4.6 version-integrity floor.
````

**2d — Identify table: fork row**

````markdown
// Before:
| Open VSX | `open-vsx.org/extension/*/*` | Install count |

// After:
| Open VSX | `open-vsx.org/extension/*/*` | Install count |
| VS Code fork (Cursor, Windsurf, VSCodium, …) | Editor's extension view, usually backed by Open VSX | Install count on that registry |
````

**2e — install-registry paragraph**

````markdown
// Before:
If the user provides a marketplace URL, extract the plugin name and
publisher from the listing page. If they provide a name only, search
the relevant marketplace.

// After:
If the user provides a marketplace URL, extract the plugin name and
publisher from the listing page. If they provide a name only, search
the relevant marketplace.

**Resolve the install registry.** Only the trust signals on the registry
the target editor installs from count. For a VS Code fork, find its
configured registry (usually Open VSX) and look the plugin up there by
the same ID; a VS Code Marketplace listing alone is no evidence for a
fork install. Record both listings when both exist.
````

**2f — metadata: version + badges**

````markdown
// Before:
- **Version**: Current marketplace version
- **Marketplace badges**: VS Code "Verified" publisher, JetBrains
  "JetBrains" / verified vendor

// After:
- **Version**: Exact version to be installed and its publish date on the
  install registry, plus the prior version's (for §4.6 V1/V3)
- **Marketplace badges**: VS Code "Verified" publisher, Open VSX
  *verified* / *unverified* namespace state, JetBrains "JetBrains" /
  vendor
````

**2g — context: target editor**

````markdown
// Before:
5. **Target editor** — VS Code, Cursor, JetBrains IDE (which one),
   Sublime Text, Neovim, other

// After:
5. **Target editor** — VS Code, a VS Code fork (Cursor, Windsurf,
   VSCodium, …; note its extension registry), JetBrains IDE (which one),
   Sublime Text, Neovim, other
````

**2h — triage: version publish date**

````markdown
// Before:
- First listed date (if available)

// After:
- First listed date (if available)
- Publish date of the version to be installed (§4.6 V1)
````

**2i — Tier 1 summary**

````markdown
// Before:
Use when ALL Tier 1 criteria from the addendum are met: >= 500K installs,
verified publisher, known company/project, proportional capabilities,
no opaque binaries, no incidents, listed >= 1 year.

// After:
Use when ALL Tier 1 criteria from the addendum are met: >= 500K installs
and identity credit on the install registry, known company/project,
proportional capabilities, no opaque binaries, no dependencies/packs or AI
surface beyond the addendum's limits, no incidents, listed >= 1 year, and
`references/criteria.md` §4.6 raises nothing.
````

**2j — Tier 3 summary**

````markdown
// Before:
publisher, runtime binary download, ownership change, prior removal,
broad activation with unclear justification.

// After:
publisher, runtime binary download, ownership change, prior removal,
broad activation with unclear justification, Open VSX namespace
mismatch, AI-key collection by an unknown publisher, dependency on an
unverified publisher's extension.
````

**2k — Q1 publisher**

````markdown
// Before:
   project? Is the publisher the same entity on VS Code Marketplace and
   Open VSX? Check for impersonation (same name, different publisher).

// After:
   project? Is the publisher the same entity on VS Code Marketplace and
   Open VSX, and is the Open VSX namespace *verified* and owned by that
   entity? Check for impersonation (same name or ID, different
   publisher).
````

**2l — Q2 capabilities**

````markdown
// Before:
   or equivalent. Cross-reference against the capability risk
   classification in `references/criteria/ide-plugin.md`.

// After:
   or equivalent. Cross-reference against the capability risk
   classification in `references/criteria/ide-plugin.md`. Include the AI
   surface (`languageModelTools`, `mcpServerDefinitionProviders`, chat
   contributions, `languageModelChatProviders`). For MCP servers, apply
   `workflows/agent-extension.md` 8a signals as a sub-rubric without
   re-routing.
````

**2m — Q4 install hook**

````markdown
// Before:
   - `postInstall` or activation-time download logic

// After:
   - Activation-time download logic (VS Code has no install hook: code
     first runs at activation; `scripts.vscode:uninstall` runs on
     uninstall)
````

**2n — Q5 cross-listing**

````markdown
// Before:
5. **Is the plugin on multiple marketplaces?** Cross-listing (VS Code
   Marketplace + Open VSX, or VS Code + JetBrains equivalent) increases
   confidence.

// After:
5. **Is the plugin on multiple marketplaces?** Cross-listing is a
   consistency check, not a trust boost: the same ID must name the same
   publisher (Open VSX namespace owner = Marketplace publisher) and a
   comparable version. A mismatch is the addendum's `namespace mismatch`
   flag.
````

**2o — Q6 incidents**

````markdown
// Before:
6. **Are there known security incidents?** Search for prior marketplace
   removals, malware reports, supply-chain compromises.

// After:
6. **Are there known security incidents?** Search for prior marketplace
   removals, malware reports, supply-chain compromises. Rate any hit by
   version scope (`references/criteria.md` §4.6 V4).
````

**2p — Q9 AI keys**

````markdown
// Before:
   Note the repo URL. Closed-source = note as a data point.

// After:
   Note the repo URL. Closed-source = note as a data point.
9. **Does the plugin handle AI-provider API keys or tokens?** If it asks
   for one, where is it sent? Only the provider's documented API is
   expected.
````

**2q — manifest keys**

````markdown
// Before:
- `contributes` — commands, debuggers, languages, taskDefinitions,
  terminal, customEditors, webviews, configuration
- `activationEvents` — `*` (always active), `onLanguage:*`,
  `onCommand:*`, `onStartupFinished`, `workspaceContains:*`
- `extensionDependencies` — other extensions this plugin requires
- `extensionPack` — bundled extensions

// After:
- `contributes` — commands, debuggers, languages, taskDefinitions,
  terminal, customEditors, webviews, configuration; AI surface:
  languageModelTools, mcpServerDefinitionProviders, chatParticipants,
  chatAgents, chatInstructions, chatPromptFiles, chatSkills,
  languageModelChatProviders
- `activationEvents` — `*` and `onStartupFinished` (both always active),
  `onLanguage:*`, `onCommand:*`, `workspaceContains:*`
- `extensionDependencies` — other extensions this plugin requires
- `extensionPack` — bundled extensions (whenever either key is present,
  review each listed extension, at every tier)
- `scripts` — `vscode:uninstall` (runs a Node script on uninstall)
````

**2r — Version integrity research block**

````markdown
// Before:
- For compiled-from-source: review the build script

// After:
- For compiled-from-source: review the build script

**Version integrity** (all tiers): apply `references/criteria.md` §4.6
with the addendum's plug-ins: publish dates, identity on the install
registry, and (Tier 2/3) the manifest diff against the prior release.
Source review (Tier 3, or Tier 2 when the diff is unexplained): look for
minified-only code with no source, invisible Unicode (zero-width,
variation selectors) hiding code, and network calls at activation.
````

**2s — incident queries**

````markdown
// Before:
- `"<plugin name>" compromise OR supply-chain`

// After:
- `"<plugin name>" compromise OR supply-chain`
- `"<plugin name>" <version>` (version-specific advisories)
````

**2t — coverage table + canonical-row mapping**

````markdown
// Before:
| Marketplace listing / metadata | Required | Required | Required |
| Publisher verification | Required | Required | Required |
| Capability / activation analysis | Brief | Required | Required |
| Bundled binary / download review | If present | Required | Required |
| CVE / advisories | Required | Required | Required |
| Web search - incidents & removal | Brief | Required | Required |
| Source code review | Tier-skip | If open source | Required |
| Cross-marketplace listing check | Optional | Required | Required |
| Extension dependency review | Tier-skip | If present | Required |
| OpenSSF Scorecard | Optional | If repo known | Required |

// After:
| Marketplace listing / metadata (install registry) | Required | Required | Required |
| Publisher verification (install registry) | Required | Required | Required |
| Typosquat / impersonation check | Required | Required | Required |
| Version integrity (§4.6) | Required | Required | Required |
| Capability / activation analysis | Brief | Required | Required |
| AI / agent surface | If present | Required if present | Required if present |
| Bundled binary / download review | If present | Required | Required |
| CVE / advisories (incl. KEV) | Required | Required | Required |
| License compatibility | Required | Required | Required |
| Web search - incidents & removal | Brief | Required | Required |
| Source code review | Tier-skip | If open source | Required |
| Cross-marketplace listing check | Optional | Required | Required |
| Extension dependency review | Required if present | Required if present | Required if present |
| OpenSSF Scorecard | Optional | If repo known | Required |

Other canonical rows map here: `Registry / metadata lookup` → marketplace
listing; `Maintainer / activity / health` → §4.2 below; `Permissions` →
capability / activation analysis; `Dependency tree` → extension
dependency review + bundled libraries; `Install script review` →
`N/A (no install hook)` for VS Code, else capability / activation
analysis.
````

**2u — 4.1 badge bullet**

````markdown
// Before:
- **Verified publisher badge**: VS Code "Verified" (DNS-linked namespace),
  JetBrains first-party or verified vendor, Open VSX namespace ownership.

// After:
- **Verified publisher badge**: VS Code "Verified" (domain ownership +
  ≥ 6 months good standing), JetBrains first-party or vendor account,
  Open VSX *verified* namespace. Identity only: credit per the addendum's
  Scoring impact and `references/criteria.md` §4.6 V2, and only on the
  registry the editor installs from.
````

**2v — 4.3 CVEs**

````markdown
// Before:
- **CVEs**: IDE plugins rarely have formal CVEs, but check GHSA and NVD
  for the plugin name and bundled dependencies.

// After:
- **CVEs**: Check GHSA, NVD and OSV for the plugin name and bundled
  dependencies, and CISA KEV for every CRITICAL (a hijacked extension
  release can get a CVE and a KEV entry). Classify own code vs
  third-party per the addendum's `## CVE Scope (§4.3)`; the verdict
  follows `SKILL.md` "Blocking CVE".
````

**2w — 4.4 activation + AI surface**

````markdown
// Before:
- **Activation breadth**: Does it activate on `*` (every editor start)
  or only on specific triggers?

// After:
- **Activation breadth**: Does it activate on `*` or `onStartupFinished`
  (every editor start) or only on specific triggers?
- **AI / agent surface**: Does it give the chat agent tools or MCP
  servers, inject prompts or instructions, or route prompts to its own
  model backend? The agent can invoke those tools and servers, so
  prompt-injected content can reach them.
````

**2x — 4.5 auto-update**

````markdown
// Before:
- **Auto-update behavior**: Marketplace plugins auto-update by default.
  Same risk pattern as browser extensions — new owner can push
  malicious update to entire install base.

// After:
- **Auto-update behavior**: Marketplace plugins auto-update by default;
  a hijacked publisher account or new owner can push a malicious update
  to the whole install base within hours. The verdict covers the audited
  version only (`references/criteria.md` §4.6 V5); name the addendum's V5
  update controls in the Recommendation.
````

**2y — Toward REJECTED: impersonation + compromised version**

````markdown
// Before:
- **Impersonation**: plugin name/icon mimics a well-known plugin but
  from a different, unverified publisher

// After:
- **Impersonation**: plugin name/icon mimics a well-known plugin but
  from a different, unverified publisher, including an Open VSX / fork
  listing under a namespace the well-known plugin's publisher does not
  own (addendum `namespace mismatch`)
- **Version in a confirmed compromise range**: `references/criteria.md`
  §4.6 V4 case (a)
````

**2z — Toward CONDITIONAL: enforceable conditions**

````markdown
// Before:
  debugger + task + terminal integration — Condition: understand scope;
  re-audit on ownership changes
- **Bundled binary from known upstream with no checksum**: Condition:
  verify binary matches upstream release; monitor for supply-chain
  incidents
- **Closed-source with broad activation**: Condition: monitor for
  incidents; identify open-source alternative
- **Single developer with no org backing**: Condition: monitor for
  acquisition; re-audit if publisher changes

// After:
  debugger + task + terminal integration — Condition: understand scope;
  hold updates at the audited version (addendum V5 controls); re-audit on
  any §4.6 V5 trigger
- **Bundled binary from known upstream with no checksum**: Condition:
  verify binary matches upstream release; hold updates at the audited
  version
- **Closed-source with broad activation**: Condition: hold updates at the
  audited version; identify open-source alternative
- **Single developer with no org backing**: Condition: hold updates at
  the audited version; re-audit if publisher changes
- **Agent-reachable AI surface that fits the stated purpose**: Condition:
  review the tool / server list; keep per-call confirmation (no "Always
  Allow") for tools that write files, run commands or send data off-host
- **AI-provider key entry, known publisher**: Condition: use a scoped,
  revocable key with a spend limit; confirm traffic goes only to the
  provider's API
````

**2aa — Toward APPROVED: registry**

````markdown
// Before:
- Listed on a major marketplace with verified publisher badge

// After:
- Listed on the registry the target editor installs from, with identity
  credit there (addendum Scoring impact)
````

**2ab — Toward APPROVED: §4.6**

````markdown
// Before:
- No known incidents or marketplace removals
- No opaque binary downloads

// After:
- No known incidents or marketplace removals; no §4.6 flag above LOW on
  the audited version
- No opaque binary downloads
````

**Rationale:**
- **2e "Resolve the install registry"** is the single most important procedural fix (A4). It sits in Identify so every tier does it.
- **2t coverage table.**
  - Adds the canonical Required rows the shared contract demands: typosquat and license were missing before this plan, and version integrity is new.
  - Raises dependency review to "Required if present" at every tier (GlassWorm's vector).
  - Maps the remaining canonical rows in one sentence rather than adding duplicate rows (read cost).
- **2z conditions.** "Monitor" is replaced with controls the user can actually apply (review A7). The AI rows give the CONDITIONAL path for legitimate AI extensions, so they are not pushed toward REJECTED.
- **2m.** Code first runs at activation. The `vscode:uninstall` hook is real and runs code, so it is named.
- **2r** points to the addendum instead of restating V1–V3 (read cost). It adds the invisible-Unicode check (review A8), phrased as a check, not a dated claim.

**Verification:**
```bash
grep -c "| Version integrity (§4.6) | Required | Required | Required |" workflows/ide-plugin.md   # 1
grep -c "Resolve the install registry" workflows/ide-plugin.md            # 1
grep -ci "rarely have formal cves\|\`postinstall\`\|monitor for" workflows/ide-plugin.md          # 0
awk '!/^\|/ && length > 80' workflows/ide-plugin.md | wc -l               # 0
wc -c < workflows/ide-plugin.md                                           # ≤ 21100 (sim 20864)
```

**If this fails:** `git -C <work-root> checkout -- workflows/ide-plugin.md`, redo in order.

---

### Step 3: `references/registries.md` Cursor row

**Objective:** stop the shared trust table from equating fork installs with VS Code Marketplace (review F11).
**Confidence:** High
**Depends on:** Step 1 (row points to the addendum)
**Do-Projex:** Encouraged

**Files:** `references/registries.md`

**Changes:** 1 replacement (one line → two lines, IDE table only).

**3a — Cursor row**

````markdown
// Before:
| Cursor extensions (VS Code compatible) | Same as VS Code Marketplace |

// After:
| Open VSX (open-vsx.org) | Low-Medium (Eclipse-operated; operator-configured publish checks; confirm the namespace is *verified*) |
| VS Code forks (Cursor, Windsurf, VSCodium, …) | Trust of the registry the fork installs from — usually Open VSX, **not** VS Code Marketplace (see `references/criteria/ide-plugin.md`) |
````

**Rationale:**
- **Open VSX gets its own row** because the table had none, while it is the registry behind every fork row.
- **Low-Medium rating.** Its review is weaker than the Marketplace's ("Medium"): operator-configured checks vs malware scanning + dynamic analysis. The 2026 campaigns ran there.
- **The fork row defers** to the addendum instead of a fixed rating, because the registry varies by editor.

**Verification:** `git -C <work-root> diff references/registries.md` shows exactly −1 / +2 lines inside `### IDE / Editor Plugins`.

**If this fails:** `git -C <work-root> checkout -- references/registries.md`. On a merge conflict with a sibling plan's edit of the same table, keep both sides; this plan owns only these two rows.

---

## Verification Plan

### Automated Checks

- [ ] Harness: `python3 evals/run_evals.py validate` passes; unittest count = Preflight count.
- [ ] Consistency script (run from `<work-root>`; not committed):

```bash
python3 - <<'EOF'
import re, pathlib
A = pathlib.Path("references/criteria/ide-plugin.md").read_text(encoding="utf-8")
W = pathlib.Path("workflows/ide-plugin.md").read_text(encoding="utf-8")
R = pathlib.Path("references/registries.md").read_text(encoding="utf-8")
C = pathlib.Path("references/criteria.md").read_text(encoding="utf-8")
heads = set(re.findall(r"^### (V[1-5]) ", C, re.M))
assert heads == {"V1","V2","V3","V4","V5"}, heads
for t in (A, W, R):
    for v in re.findall(r"§4\.6 (V\d)", t):
        assert v in heads, v
assert len(re.findall(r"^## Version & Update Integrity \(§4\.6\)$", A, re.M)) == 1
assert len(re.findall(r"^## CVE Scope \(§4\.3\)$", A, re.M)) == 1
for v in "12345":
    assert len(re.findall(rf"^- \*\*V{v}\*\* — ", A, re.M)) == 1, v
norm = lambda s: re.sub(r"\s+", " ", s).lower()
for name, t in (("A", A), ("W", W)):
    for bad in ["rarely have formal cves", "`postinstall`", "slightly higher trust", "(equivalent to amo recommended)",
                "(equivalent to cws featured)", "dns-linked namespace", "increases confidence", "monitor for incidents",
                "monitor for supply-chain", "monitor for acquisition", "vim-plug, packer)", "/ packer)", "in v1"]:
        assert bad not in norm(t), (name, bad)
for row in ["| Version integrity (§4.6) | Required | Required | Required |",
            "| Typosquat / impersonation check | Required | Required | Required |",
            "| License compatibility | Required | Required | Required |",
            "| Extension dependency review | Required if present | Required if present | Required if present |"]:
    assert row in W, row
assert "workflows/agent-extension.md" in A and "workflows/agent-extension.md" in W
assert "Cursor extensions (VS Code compatible)" not in R and "| Open VSX (open-vsx.org) |" in R and "| VS Code forks (Cursor" in R
assert len(A.encode()) <= 13400 and len(W.encode()) <= 21100, (len(A.encode()), len(W.encode()))
assert not [l for l in W.splitlines() if not l.startswith("|") and len(l) > 80]
print("OK")
EOF
```
- [ ] `git -C <work-root> diff --stat <base>..HEAD` lists exactly the 3 files; `evals/` untouched.

### Manual Verification (paper traces)

Walk each case through the workflow → addendum → `SKILL.md` Step N + `references/criteria.md` §4.3/§4.6. Record the cited rule per hop in the execution log.

| # | Case | Expected |
|---|---|---|
| I1 | eval 16: Prettier, VS Code, verified publisher, version ≥ 7 d, no AI surface / packs | Tier 1 (all 1g bullets hold) → **APPROVED** |
| I2 | Nx-shape: verified publisher, 2M installs, version 20 min old, no matching repo tag, before any advisory | V1 HIGH `fresh version` + V3 HIGH → Tier 1 barred → **CONDITIONAL**: install prior release, set `extensions.autoUpdateDelay` ≥ 72 or pin via `extensions.allowed`; escalation notice (V3 HIGH) |
| I3 | Same, after the advisory names the version | §4.6 V4 (a) → Red Flag → **REJECTED** + incident-response note (2y bullet) |
| I4 | Cursor user asks for well-known extension ID X; Open VSX namespace owned by an account ≠ Marketplace publisher | 2e resolves Open VSX; 1b `namespace mismatch` → Impersonation (2y) → **REJECTED** |
| I5 | Cursor user; Open VSX *verified* namespace owned by the Marketplace publisher; 300K Open VSX installs | Tier 1 fails install-count bullet → Tier 2 → **APPROVED** reachable |
| I6 | JetBrains "AI code review" plugin, 5K downloads, vendor account, asks for an OpenAI key, sends it to a non-OpenAI host | Tier 3 (installs < 10K + key collection); 1e HIGH → ≥ **CONDITIONAL**; confirmed exfiltration = Known malware → **REJECTED** |
| I7 | VS Code extension with `extensionPack` naming an extension from a different, unverified publisher | Tier 3 trigger; 1e HIGH if that extension fails review → ≥ **CONDITIONAL** |
| I8 | VS Code extension contributing `mcpServerDefinitionProviders` (classifier edge case) | Stays ide-plugin; 2l applies agent-extension 8a signals; Tier 1 barred (1g) → verdict per 8a findings + this rubric |
| I9 | eval 37: rust-analyzer, bundled server | Bundled server = own code (CVE Scope); Marketplace = trust boundary unchanged → **APPROVED** (Tier 1 or 2 depending on V1 age; < 72 h case is the shared eval hand-off) |
| I10 | eval 17: sideloaded `.vsix` via Slack | Unchanged path → **REJECTED** |
| I11 | eval 28: GitLens (GitKraken sign-in; may contribute AI features) | Tier 2 regardless; AI rows → CONDITIONAL row 2z if agent-reachable → **CONDITIONAL / APPROVED** (eval accepts both) |

### Acceptance Criteria Validation

| Criterion | How to Verify | Expected Result |
|---|---|---|
| Plug-in sections | Step 1 greps; consistency script | 1 / 1 / 5; `OK` |
| References resolve | consistency script | `OK` |
| Stale phrases gone | consistency script | `OK` |
| registries row | Step 3 diff | −1 / +2 lines in IDE table |
| Coverage rows | consistency script | `OK` |
| Byte budget + wrap | Step 1/2 `wc -c`, awk | ≤ 13,400 / ≤ 21,100; 0 long lines |
| Harness green | validate + unittest | pass; same count |
| Traces | execution log I1–I11 | match table |
| Only 3 files | `git diff --stat` | 3 files |

---

## Rollback Plan

1. Before close: `projex-abandon.sh <repo-root> claude/youthful-dijkstra-5ov1kt projex/<this-plan> --worktree` — base untouched.
2. After squash-close: `git -C <repo-root> revert <squash-sha>` (touches only the 3 files). The shared §4.6 floor still applies without the plug-ins (shared defaults).

---

## Notes

### Risks

- **Read cost +~11.3 KB (~2.8k tokens) per ide-plugin audit.**
  - Mitigation: already trimmed once in simulation (−2.2 KB), and the workflow points to the addendum instead of restating it. Further trim order, if the orchestrator sets a tighter budget:
    1. Drop the 2t mapping sentence (−~0.4 KB).
    2. Compress 2z to two AI rows of one line each (−~0.3 KB).
    3. Merge the 1e AI bullets into the 1c table "Why" cells (−~0.4 KB).
- **Policy judgment on weights** (Open VSX Low-Medium, unverified = MEDIUM, tools/MCP = Medium-High, JetBrains vendor = moderate). Mitigation: each value lives in one table cell or bullet. The traces show eval verdicts unchanged.
- **More Tier 2 audits for fork users** (install counts on Open VSX are lower). This is accepted: it is the intended correction, not a regression.
- **Platform drift** (VS Code ships weekly; setting names changed in 1.125). Mitigation: settings carry their minimum version. STEWARDSHIP 120-day cadence plus an event trigger on VS Code extension-security release notes (suggest to orchestrator).
- **Concurrent edits to `references/registries.md`.** Mitigation: single-line anchor; keep-both-sides rule.
- **B1 heading drift** in the shared plan. Mitigation: Preflight stop / re-anchor rule.

### Eval Hand-off (for the eval-refresh plan; do not edit `evals/` here)

New ide-plugin cases (STEWARDSHIP step 6; review F10):

| Proposed case | Prompt shape | Expected |
|---|---|---|
| Fresh hijacked version | "Nx Console just updated to <ver> an hour ago, OK to keep auto-updating?" (or a fictional ID to avoid date drift) | CONDITIONAL (fresh version / continuity); mentions update delay or pin; or REJECTED if prompt states an advisory names the version |
| Fork namespace squat | "In Cursor, install `<publisher>.<ext>` from Open VSX; namespace shows unverified, different owner from Marketplace" | REJECTED (impersonation / namespace mismatch); report names Open VSX as trust boundary |
| Fork, verified namespace | "Install Prettier in Cursor" | APPROVED or CONDITIONAL; report reads Open VSX listing, not Marketplace badge |
| JetBrains AI-key plugin | Low-download JetBrains "AI assistant" asking for an OpenAI key, unknown vendor | Tier 3; CONDITIONAL or REJECTED; mentions key destination |
| MCP via VS Code extension | Extension that registers an MCP server (`mcpServerDefinitionProviders`) | Routes ide-plugin (not agent-extension); applies MCP/8a signals; Tier 1 not used |
| Extension pack | Pack pulling extensions from several publishers | Reviews each member; Tier 2+ |

Existing: eval 37 prompt says rust-analyzer "downloads a native binary"; it ships platform-specific VSIX with the bundled server (review A10, prior knowledge, Medium) — reword prompt. Evals 16 / 37 exact-APPROVED + V1 timing → already in the shared plan's eval hand-off.

### Orchestrator Flags (outside this plan's ownership)

- `references/registries.md` JetBrains row "Medium-High (JetBrains review process)": consider "Medium" (Plugin Verifier ≠ anti-malware). Owner: registry plan or orchestrator.
- `references/classifier.md` lists `packer spec` as an ide-plugin signal; consider adding `vim.pack.add()` / `nvim-pack-lock.json`. Owner: orchestrator (shared file).
- F9 scope: Zed (WASM-sandboxed, permission-gated extensions per secondary sources), MELPA, Visual Studio / Eclipse marketplaces → `generic` or a later ide-plugin cycle.
- §4.3 plug-in heading: this plan uses `## CVE Scope (§4.3)`; harmonize across sibling addenda.
- STEWARDSHIP: ide-plugin Last Reviewed 2026-10-16 → Next Due 2027-02-13 on close; add VS Code extension-security release notes and Open VSX wiki as event triggers.

### Open Questions

None blocking. Resolved at planning: Open VSX trusted publishing (OIDC) exists (wiki 2026-10) and the Marketplace now recommends Entra ID workload identity (global Azure DevOps PATs retire 2026-12-01), but neither is a consumer-visible per-version signal, so the rubric does not use them. Review OQ "can an auditor get version publish times" → yes for Marketplace (version history), Open VSX (version page), JetBrains (Versions tab); otherwise §4.6 V1 "Unknown" applies.

### Split Decision

`No split — single scope, within size budget`. 3 steps + Preflight, one `.projex/` scope, prose-only rubric files (no upstream/downstream mix). Plan length exceeds 500 lines only because Before/After blocks are verbatim; step count (3) is under the > 5 threshold. Steps are coupled (Step 2 and 3 cite Step 1 headings).

### Revision Log

| Date | Trigger | Change |
|---|---|---|
| 2026-10-16 | Initial (orchestrator dispatch) | Plan authored; facts verified against vscode-docs / openvsx.wiki / neovim primaries; 37 pairs simulated at `cdd8ee2` |
