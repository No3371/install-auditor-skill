# IDE Plugin Workflow — M3.4

> **Status:** In Progress
> **Created:** 2026-04-15
> **Author:** Claude (Opus 4.6)
> **Source:** [2604070218-install-auditor-subject-typed-redesign-nav.md](2604070218-install-auditor-subject-typed-redesign-nav.md) Phase 3, M3.4
> **Related Projex:**
> - **Roadmap:** [2604070218-install-auditor-subject-typed-redesign-nav.md](2604070218-install-auditor-subject-typed-redesign-nav.md)
> - **Framing eval:** [2604070217-subject-typed-audit-dispatch-eval.md](2604070217-subject-typed-audit-dispatch-eval.md)
> - **Taxonomy spec:** [2604070300-install-auditor-subject-type-taxonomy-def.md](2604070300-install-auditor-subject-type-taxonomy-def.md)
> - **Pattern precedent (M3.1):** [2604141200-browser-extension-workflow-m31-plan.md](closed/2604141200-browser-extension-workflow-m31-plan.md)
> - **Pattern precedent (M3.2):** [2604141800-container-image-workflow-m32-plan.md](closed/2604141800-container-image-workflow-m32-plan.md)
> - **Pattern precedent (M3.3):** [2604150048-ci-action-workflow-m33-plan.md](closed/2604150048-ci-action-workflow-m33-plan.md)
> **Worktree:** No

---

## Summary

Create the Type 3 subject-specific workflow at `workflows/ide-plugin.md` and its criteria addendum at `references/criteria/ide-plugin.md`, then wire Type 3 routing and eval coverage. M3.4 closes the last Phase 3 gap: IDE plugins still fall through `workflows/generic.md`, which knows nothing about marketplace verification, capability/activation-event declarations, verified-publisher badges, or the divergent trust models across VS Code Marketplace, Open VSX, JetBrains Marketplace, Sublime Package Control, and Neovim plugin managers.

**Scope:** Type 3 IDE-plugin audits — workflow file, criteria addendum, dispatcher wiring, eval coverage.
**Estimated Changes:** 4 files (2 new, 2 modified), ~550-700 lines.

---

## Objective

### Problem / Gap / Need

Type 3 (`ide-plugin`) routes to `workflows/generic.md`. Current guidance is inadequate:

1. `workflows/generic.md` has no IDE-plugin-specific checks. No marketplace verification, no capability/activation-event review, no verified-publisher awareness.
2. Triage thresholds (`>100K weekly downloads`) are npm-specific. IDE plugins use install count from marketplaces — different scale, different signal.
3. `references/registries.md` has a brief IDE/Editor Plugins trust table (VS Code Marketplace = Medium, JetBrains = Medium-High, Vim-Plug = Low-Medium, MELPA = Low-Medium) but no scoring mechanics.
4. No review path for plugin capability declarations — `contributes` in VS Code (`commands`, `debuggers`, `languages`, `taskDefinitions`), JetBrains extension points, Sublime commands/keybindings.
5. No treatment of the marketplace-vs-sideload trust gap (VSIX file, manual JetBrains ZIP, GitHub-sourced vim plugin with no marketplace listing).
6. No guidance on verified-publisher signals per marketplace (VS Code "Verified" badge, JetBrains "JetBrains" / verified vendor, Open VSX namespace ownership).
7. No coverage of plugins that bundle or download binaries (LSP servers, formatters, linters) — the dominant attack surface for IDE plugins.

The framing eval (§5.1) flags: "Triage-tier thresholds (>100K weekly downloads) are npm-specific but live in the shared step. They make no sense for a VS Code extension whose adoption signal is install count from the marketplace."

### Success Criteria

- [ ] `workflows/ide-plugin.md` exists and follows Identify / Evidence / Subject Rubric / Subject Verdict Notes template
- [ ] `references/criteria/ide-plugin.md` exists and defines IDE-plugin-specific scoring for marketplace trust, capability risk, verified-publisher signals, bundled-binary risk, and tier thresholds
- [ ] `SKILL.md` dispatch table row 3 routes to `workflows/ide-plugin.md`
- [ ] `SKILL.md` Reference Files includes `workflows/ide-plugin.md` and `references/criteria/ide-plugin.md`
- [ ] `evals/evals.json` gains at least 2 Type 3 cases: one well-known verified-publisher Tier 1 positive path, one unknown sideloaded/low-trust negative path
- [ ] No regressions in eval ids 0-15

### Out of Scope

- New helper scripts for marketplace API lookup or VSIX inspection
- Broad rewrites to `references/criteria.md` or `references/registries.md` unless execution finds a factual gap blocking the workflow
- Full Emacs MELPA / Atom (discontinued) parity beyond note-level mapping
- Phase 4+ workflows (desktop-app, cli-binary, agent-extension, remote-integration)

---

## Context

### Current State

`SKILL.md` classifies Type 3 correctly (`code --install-extension`, VSIX, `marketplace.visualstudio.com/*`, `open-vsx.org/*`, `plugins.jetbrains.com/*`) but dispatches to `workflows/generic.md`. The generic workflow has no IDE-plugin-specific fragments — zero marketplace verification, zero capability review, zero verified-publisher checks.

`references/registries.md` already contains the core IDE plugin trust baseline:

- VS Code Marketplace = Medium (Microsoft-operated)
- JetBrains Marketplace = Medium-High (JetBrains review process)
- Vim-Plug / GitHub-sourced Vim plugins = Low-Medium (no central review)
- Emacs MELPA = Low-Medium (community-maintained)
- Cursor extensions = same as VS Code Marketplace

There is no existing Type 3 criteria addendum, no Type 3 workflow, and no Type 3 eval coverage.

### Key Files

| File | Role | Change Summary |
|------|------|----------------|
| `workflows/ide-plugin.md` | **New.** Type 3 workflow | Create marketplace-aware workflow: plugin identity extraction, capability/activation review, verified-publisher check, bundled-binary audit, verdict notes |
| `references/criteria/ide-plugin.md` | **New.** Type 3 criteria addendum | Create IDE-plugin-specific scoring: marketplace trust signals, capability risk classification, verified-publisher signals, bundled-binary risk, tier thresholds |
| `SKILL.md` | Dispatcher + reference-file index | Row 3 -> `workflows/ide-plugin.md`; add 2 Reference Files bullets |
| `evals/evals.json` | Regression + new Type 3 coverage | Add ids 16 and 17 for positive and negative Type 3 paths |

### Dependencies

- **Requires:** Phase 3 M3.1-M3.3 complete; dispatcher architecture stable; `references/registries.md` IDE table present
- **Blocks:** Phase 3 M3.5 eval gate; Phase 3 exit criterion that `generic.md` no longer handles high-volume Type 3 subjects

### Constraints

- Workflow must use the standard 4-section template (Identify / Evidence / Subject Rubric / Subject Verdict Notes)
- Audit Coverage table and audit-confidence statement owned by `SKILL.md` Step N
- No scripts in M3.4; evidence acquisition is doc/web/marketplace inspection
- v1 depth is VS Code Marketplace-first (largest ecosystem), with JetBrains second and Sublime/Neovim at note-level mapping
- Repo is clean; worktree not needed

### Assumptions

- VS Code Marketplace is the dominant Type 3 path worth optimizing first; JetBrains Marketplace is second; Sublime Package Control and Neovim plugin managers (lazy.nvim, vim-plug, packer) inherit the same trust principles with shorter notes
- Open VSX is the open-source mirror of VS Code Marketplace; extensions on both VS Code Marketplace and Open VSX are slightly higher trust (cross-listed)
- The primary risk surface for IDE plugins is **capability scope + bundled-binary behavior**, not permissions in the browser-extension sense — IDE plugins run with the editor's full process privileges, so the question is what they *activate* and what they *download/execute*, not what API permissions they request
- "Verified Publisher" on VS Code Marketplace means the publisher namespace is linked to a verified DNS domain; on JetBrains it means JetBrains-developed or verified vendor
- Install count is the primary adoption metric for IDE plugins (replaces npm weekly downloads)

### Impact Analysis

- **Direct:** New workflow, new criteria addendum, dispatcher wiring, eval additions
- **Adjacent:** `workflows/generic.md` no longer handles Type 3 once M3.4 lands, but needs no edits
- **Downstream:** M3.5 eval gate becomes fully reachable (last Phase 3 type); Phase 4 long-tail work opens cleanly

---

## Implementation

### Overview

4 steps: addendum first, workflow second, dispatcher wiring third, evals fourth. Same sequence as M3.1-M3.3. No shared-core doc changes expected.

### Step 1: Create `references/criteria/ide-plugin.md`

**Objective:** Define IDE-plugin-specific scoring extensions the workflow can cite.
**Confidence:** High
**Depends on:** None

**Files:**
- `references/criteria/ide-plugin.md` (new)

**Changes:**

Create a new addendum with this structure:

```markdown
# IDE Plugin — Criteria Addendum

Per-subject scoring extensions for **Type 3: ide-plugin** audits.
Layers on top of `references/criteria.md`. More-specific guidance wins.

Covers: VS Code Marketplace, Open VSX, JetBrains Marketplace, Sublime
Package Control, Neovim plugin managers (lazy.nvim, vim-plug, packer).
Depth is VS Code Marketplace-first in v1.

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
- Neovim GitHub-sourced with >1K stars = weak positive
- Sideloaded VSIX/ZIP with no marketplace listing = strong negative

## Capability Risk Classification

IDE plugins declare capabilities differently per editor. The key risk axis
is what the plugin can *activate* and what it *executes*, because plugins
run with the host editor's full process-level privileges.

### VS Code — `contributes` and activation events

| Capability | Risk | Why |
|------------|------|-----|
| `commands` only | Low | User-triggered actions; scoped |
| `languages` / `grammars` / `snippets` | Low | Syntax support; no code execution |
| `themes` / `iconThemes` | Low | Visual only |
| `debuggers` | Medium-High | Spawns debug adapter processes; can execute arbitrary code |
| `taskDefinitions` | Medium | Defines build/run tasks that execute shell commands |
| `terminal` | Medium-High | Can create and write to integrated terminal |
| Custom editor / webview | Medium | Renders arbitrary HTML/JS inside the editor |
| `*` activation event | Medium | Plugin loads on every editor start (broader attack surface than targeted activation) |

### JetBrains — extension points

| Capability | Risk | Why |
|------------|------|-----|
| Language support / inspections | Low | Static analysis; no external execution |
| Tool window / UI contributions | Low-Medium | UI modification only |
| Run configuration / external tools | Medium-High | Executes processes |
| Project-level hooks (postStartupActivity) | Medium | Runs on project open |
| Custom compiler / build tool integration | High | Executes build pipelines |

### Sublime / Neovim

Sublime plugins are Python scripts running in Sublime's embedded interpreter.
Neovim plugins are Lua/Vimscript running in-process or remote plugins over
RPC. Both have full host-process access; the risk is essentially
"what code runs and what does it call."

### Scoring impact

- Theme/syntax/snippet only = neutral
- Command-only activation with scoped triggers = low risk
- Debugger, task, terminal, or build-tool integration = elevated review
- `*` activation (VS Code) or `postStartupActivity` (JetBrains) = note
  as always-active
- Remote plugin / RPC (Neovim) = medium — inspect what processes are spawned

## Bundled Binary / Download-at-Runtime Risk

The dominant attack surface for IDE plugins: many plugins bundle or download
language servers, formatters, linters, or other executables.

| Pattern | Risk | Guidance |
|---------|------|----------|
| Plugin bundles compiled binary in VSIX/ZIP | Medium-High | Inspect binary provenance; check if it matches a known project release |
| Plugin downloads binary on first activation | High | Note the download URL; verify it points to a known project's release assets with checksums |
| Plugin invokes system-installed tool (`PATH` lookup) | Low-Medium | Relies on user-installed tool; note the dependency |
| Plugin compiles from source on install | Medium | Transparent but may execute untrusted build scripts |
| No binary component | Low | Pure JS/TS/Python/Lua plugin |

### Scoring impact

- No binary = positive signal
- Bundles binary from a known, tagged, signed upstream = moderate
- Downloads binary at runtime from author's server without checksum = high-risk finding
- Downloads binary from unknown/opaque URL = strong negative

## Tier Thresholds (IDE Plugins)

### Tier 1 — Quick Audit

ALL of these must hold:
- Install count >= 500K on primary marketplace
- Verified publisher (VS Code) or JetBrains first-party / verified vendor
- Publisher is a known company or well-known open-source project
- Capabilities are proportional to stated purpose
- No bundled/downloaded binary with opaque provenance
- No known incidents or marketplace removals
- Listed >= 1 year

### Tier 2 — Standard Audit (default)

Default when not all Tier 1 criteria are met:
- Install count 10K-500K
- Identifiable publisher
- No known security incidents
- Listed > 30 days

### Tier 3 — Deep Audit

ANY of these triggers:
- Install count < 10K
- No marketplace listing (sideloaded VSIX/ZIP, direct GitHub install)
- Publisher unknown or anonymous
- Plugin downloads binaries at runtime from author-controlled server
- Recent ownership transfer or publisher change
- Known prior removal or policy violation
- Plugin requests `*` activation with broad capability scope
- Plugin integrates debugger/terminal/task runner with unclear justification
```

**Rationale:** Shared rubric and `references/registries.md` provide only a brief trust table. This addendum becomes the single reference for marketplace-specific trust signals, capability risk classification, bundled-binary patterns, and tier thresholds calibrated to IDE-plugin adoption scales.

**Verification:** File exists. Sections present: marketplace trust signals, capability risk classification, bundled-binary risk, tier thresholds.

**If this fails:** Delete `references/criteria/ide-plugin.md`.

---

### Step 2: Create `workflows/ide-plugin.md`

**Objective:** Author the Type 3 workflow with VS Code Marketplace-first evidence and verdict guidance.
**Confidence:** High
**Depends on:** Step 1

**Files:**
- `workflows/ide-plugin.md` (new)

**Changes:**

Create the workflow with this structure:

```markdown
<!--
workflows/ide-plugin.md - Type 3 subject-specific workflow.
Handles IDE/editor plugins from VS Code Marketplace, Open VSX, JetBrains
Marketplace, Sublime Package Control, and Neovim plugin managers.
VS Code Marketplace-first in v1.

This workflow replaces workflows/generic.md for Type 3 subjects. After
producing findings here, return to SKILL.md Step N for the shared verdict
tree and report shape. The Audit Coverage table and audit-confidence
assertion are owned by the dispatcher - do not duplicate them here.

Phase 3 / M3.4 - fifth subject-specific workflow (fourth Phase 3).
-->

# IDE Plugin Workflow (Type 3)

This workflow handles **Type 3: ide-plugin** subjects from VS Code
Marketplace, Open VSX, JetBrains Marketplace, Sublime Package Control,
and Neovim plugin managers (lazy.nvim, vim-plug, packer). Primary depth
in v1 is VS Code Marketplace because it is the largest ecosystem and
the repo's trust references are VS Code-heavy.

After completing all sections below, return to `SKILL.md` Step N for the
shared verdict tree and audit-coverage report shape.

Sections follow the standard workflow template: **Identify / Evidence /
Subject Rubric / Subject Verdict Notes**.

Use `references/criteria/ide-plugin.md` for ide-plugin-specific tiering
and scoring. When it conflicts with the shared rubric, the more specific
ide-plugin guidance wins.

## Identify

### 1. Determine the marketplace and plugin identity

| Marketplace | URL pattern | Adoption metric |
|-------------|-------------|-----------------|
| VS Code Marketplace | `marketplace.visualstudio.com/items?itemName=*` | Install count |
| Open VSX | `open-vsx.org/extension/*/*` | Install count |
| JetBrains Marketplace | `plugins.jetbrains.com/plugin/*` | Downloads |
| Sublime Package Control | `packagecontrol.io/packages/*` | Installs (approx) |
| Neovim (GitHub) | `github.com/<owner>/<repo>` | Stars + forks |
| Sideloaded | `.vsix` file, ZIP, manual clone | None |

If the user provides a marketplace URL, extract the plugin name and
publisher from the listing page. If they provide a name only, search
the relevant marketplace.

### 2. Extract plugin name and metadata

- **Plugin name**: Exact name as listed
- **Publisher**: Namespace owner (VS Code `publisher.name`), vendor
  (JetBrains), or GitHub owner (Neovim/Sublime)
- **Plugin ID**: VS Code uses `publisher.extensionName`; JetBrains uses
  numeric plugin ID; Sublime uses package name; Neovim uses `owner/repo`
- **Version**: Current marketplace version
- **Marketplace badges**: VS Code "Verified" publisher, JetBrains
  "JetBrains" / verified vendor
- **Install count and rating**: Primary adoption metric

### 3. Gather required context

Collect before proceeding:

1. **Full name and marketplace ID** — exact plugin name + marketplace
   identifier
2. **Source marketplace** — which marketplace (from table above), or
   sideloaded
3. **Installation method** — marketplace install, `code --install-extension`,
   `ext install`, JetBrains plugin manager, Sublime Package Control,
   lazy.nvim/vim-plug spec, or manual VSIX/ZIP sideload
4. **Stated purpose** — what the user needs this plugin for
5. **Target editor** — VS Code, Cursor, JetBrains IDE (which one),
   Sublime Text, Neovim, other
6. **Capability scope** — what the plugin declares it can do (contributes,
   extension points, commands) — obtained during research if not
   immediately available

If any of 1-5 are missing, ask before proceeding.

## Evidence - Part A: Tier Triage

Gather marketplace listing data via web search:
- Install count, rating, review count
- Publisher name and verification badges
- First listed date (if available)
- Brief search for "[plugin name] malware OR removed OR security OR
  vulnerability" for prior incidents

Apply the ide-plugin-specific tier thresholds from
`references/criteria/ide-plugin.md`:

### Tier 1 - Quick Audit (well-known, high-trust)

Use when ALL Tier 1 criteria from the addendum are met: >= 500K installs,
verified publisher, known company/project, proportional capabilities,
no opaque binaries, no incidents, listed >= 1 year.

Quick audit scope: confirm marketplace presence + publisher verification,
note capabilities at a glance, check for incidents, verify publisher.
Proceed to Subject Verdict Notes with minimal ceremony.

### Tier 2 - Standard Audit (default)

Default depth. Full capability review, publisher verification, bundled-
binary inspection, incident search, source code spot-check if open source.

### Tier 3 - Deep Audit (any red flag)

Any Tier 3 trigger from the addendum: low installs, sideloaded, unknown
publisher, runtime binary download, ownership change, prior removal,
broad activation with unclear justification.

Deep audit scope: full capability review + binary provenance audit +
source code review (if available) + activation event analysis + network
behavior patterns.

## Evidence - Part B: Research

### Core research questions (all tiers)

Answer every question that applies to the assigned tier:

1. **Who publishes this plugin?** Company, individual, or open-source
   project? Is the publisher the same entity on VS Code Marketplace and
   Open VSX? Check for impersonation (same name, different publisher).
2. **What capabilities does the plugin declare?** Read `package.json`
   `contributes` (VS Code), `plugin.xml` extension points (JetBrains),
   or equivalent. Cross-reference against the capability risk
   classification in `references/criteria/ide-plugin.md`.
3. **Does the capability set match the stated purpose?** A theme plugin
   registering `debuggers` + `taskDefinitions` is suspicious. A language
   server registering `languages` + `debuggers` is expected.
4. **Does the plugin bundle or download binaries?** Check for:
   - Compiled binaries in the VSIX/package
   - `postInstall` or activation-time download logic
   - Language server binaries (LSP), formatters, linters
   - If yes: what is the binary, where does it come from, is it
     checksummed or signed?
5. **Is the plugin on multiple marketplaces?** Cross-listing (VS Code
   Marketplace + Open VSX, or VS Code + JetBrains equivalent) increases
   confidence.
6. **Are there known security incidents?** Search for prior marketplace
   removals, malware reports, supply-chain compromises.
7. **What is the update cadence?** Frequent updates = active maintenance.
   Stale (>2 years) with active dependency on external tools/APIs is
   a concern.
8. **Is the source code available?** Open-source plugins can be audited.
   Note the repo URL. Closed-source = note as a data point.

### How to research

**Marketplace listing inspection** (all tiers):

Web search for the plugin's marketplace page. Extract:
- Install count, rating, review count
- Publisher name + verification badge
- Capability summary (VS Code shows "Feature Contributions" on the
  listing page; JetBrains shows plugin description + change notes)
- Repository link (most VS Code extensions link to GitHub)
- Reviews mentioning security, privacy, or suspicious behavior

**Capability analysis** (Tier 2 and Tier 3):

Obtain `package.json` (VS Code) or `plugin.xml` (JetBrains) via:
- The plugin's open-source repository
- VS Code Marketplace listing (feature contributions tab)
- Direct VSIX download + unzip (VSIX is a ZIP)
- JetBrains plugin page description

Inspect these keys (VS Code `package.json`):
- `contributes` — commands, debuggers, languages, taskDefinitions,
  terminal, customEditors, webviews, configuration
- `activationEvents` — `*` (always active), `onLanguage:*`,
  `onCommand:*`, `onStartupFinished`, `workspaceContains:*`
- `extensionDependencies` — other extensions this plugin requires
- `extensionPack` — bundled extensions
- `engines.vscode` — minimum VS Code version

For JetBrains `plugin.xml`:
- `<extensions>` — declared extension points
- `<actions>` — menu/toolbar actions
- `<depends>` — platform and plugin dependencies
- `<applicationListeners>`, `<projectListeners>` — lifecycle hooks

**Binary provenance inspection** (Tier 2 if binary present, always Tier 3):

If the plugin ships or downloads a binary:
- Identify the binary: what project is it from?
- Trace the download URL: does it point to the official project's
  release page (e.g., GitHub Releases)?
- Check for checksums or signatures in the download logic
- Verify the binary version matches a known release
- For compiled-from-source: review the build script

**Incident and reputation search** (all tiers, depth varies):

Web search queries:
- `"<plugin name>" malware OR removed OR security OR vulnerability`
- `"<plugin name>" compromise OR supply-chain`
- `"<publisher name>" extension OR plugin OR malware`
- For Tier 3: `"<plugin name>" site:reddit.com` and
  `"<plugin name>" site:github.com`

### Audit coverage tracking

Map evidence to the Audit Coverage rows expected by `SKILL.md` Step N:

| Check | Tier 1 | Tier 2 | Tier 3 |
|-------|--------|--------|--------|
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

## Subject Rubric - Evaluate

Score against the shared rubric in `references/criteria.md` AND the
ide-plugin addendum in `references/criteria/ide-plugin.md`. Sections
below specialize the shared criteria for IDE plugin context.

### 4.1 Provenance & Identity (ide-plugin-specialized)

- **Marketplace verification**: Is the plugin listed on an official
  marketplace? Which ones? Are the listings consistent?
- **Publisher identity**: Can the publisher be linked to a real company
  or known open-source project? Check the marketplace publisher page,
  linked website, and GitHub org.
- **Verified publisher badge**: VS Code "Verified" (DNS-linked namespace),
  JetBrains first-party or verified vendor, Open VSX namespace ownership.
- **Impersonation check**: Are there similarly-named plugins by different
  publishers? Search the marketplace for the plugin name and check for
  copycats.
- **Cross-marketplace consistency**: If listed on multiple marketplaces,
  is the publisher the same entity?

### 4.2 Maintenance & Longevity (ide-plugin-specialized)

- **Last update date**: When was the last version published? Plugins
  that depend on external tools (LSP servers, APIs) stale faster than
  pure-syntax plugins.
- **Install count trend**: Growing, stable, or declining?
- **Review sentiment**: Recent reviews reporting issues, breakage, or
  suspicious behavior.
- **Open-source activity**: If public repo, check commit recency, issue
  responsiveness, contributor count.
- **Editor version compatibility**: Does the plugin work on the user's
  current editor version?

### 4.3 Security Track Record (ide-plugin-specialized)

- **Marketplace removal history**: Has this plugin been removed for
  policy violations?
- **CVEs**: IDE plugins rarely have formal CVEs, but check GHSA and NVD
  for the plugin name and bundled dependencies.
- **Supply-chain incidents**: Has the publisher had other plugins
  compromised? Has the bundled binary's upstream project had incidents?
- **Dependency vulnerabilities**: Check `package.json` dependencies
  (VS Code) or bundled libraries for known CVEs.

### 4.4 Permissions & Access (ide-plugin-specialized)

**IDE plugins run with the editor's full process privileges.** There is
no granular permission model like browser extensions. The risk axes are:

- **Capability scope**: What features does the plugin contribute?
  Score against the capability risk classification in the addendum.
- **Activation breadth**: Does it activate on `*` (every editor start)
  or only on specific triggers?
- **Binary execution**: Does it spawn processes, download executables,
  or invoke system tools? This is the dominant risk surface.
- **Network access**: Does the plugin make network calls? To what
  endpoints? Telemetry collection? Data exfiltration potential?
- **File system access**: Does it read/write outside the workspace?
  Configuration files, credentials, SSH keys?
- **Terminal access**: Can it create or write to integrated terminals?

### 4.5 Reliability & Compatibility (ide-plugin-specialized)

- **Editor compatibility**: Minimum supported editor version. Plugins
  targeting very old APIs may break or lack modern sandboxing.
- **Dependency chain**: Does the plugin require other extensions?
  Are those dependencies well-maintained?
- **Binary compatibility**: If the plugin bundles binaries, are they
  available for the user's OS/architecture?
- **Auto-update behavior**: Marketplace plugins auto-update by default.
  Same risk pattern as browser extensions — new owner can push
  malicious update to entire install base.

### 4.6 Alternatives (ide-plugin-specialized)

- Are there alternative plugins with narrower capabilities for the
  same purpose?
- Is there a built-in editor feature that eliminates the need?
- For language support: is there a first-party extension from the
  language maintainer?
- If closed-source, is there an open-source alternative?

## Subject Verdict Notes

IDE-plugin-specific guidance for how findings map to verdicts. These
notes supplement the shared verdict tree in `SKILL.md` Step N.

### Toward REJECTED

Any one of these pushes strongly toward REJECTED:

- **Known malware / marketplace removal for malicious behavior**: plugin
  removed for data exfiltration, cryptomining, credential theft
- **Opaque binary download from unknown server**: plugin downloads
  executables at runtime from unverifiable source without checksums
- **Sideloaded with no source or provenance**: VSIX/ZIP from unknown
  origin, no marketplace listing, no source code, no publisher identity
- **Recent acquisition + capability escalation**: plugin acquired by
  new entity and simultaneously added high-risk capabilities
- **Impersonation**: plugin name/icon mimics a well-known plugin but
  from a different, unverified publisher

### Toward CONDITIONAL

- **Broad capabilities with justification**: language server needing
  debugger + task + terminal integration — Condition: understand scope;
  re-audit on ownership changes
- **Bundled binary from known upstream with no checksum**: Condition:
  verify binary matches upstream release; monitor for supply-chain
  incidents
- **Closed-source with broad activation**: Condition: monitor for
  incidents; identify open-source alternative
- **Single developer with no org backing**: Condition: monitor for
  acquisition; re-audit if publisher changes
- **Neovim/Sublime plugin from low-star GitHub repo**: Condition:
  review source code before use; pin to specific commit/tag
- **3+ MEDIUM flags accumulated**: cumulative risk per shared
  verdict tree

### Toward APPROVED

All of the following support APPROVED:

- All tier-appropriate checks completed with no flags
- Listed on a major marketplace with verified publisher badge
- Capabilities proportional to stated purpose
- Publisher is identified (company or known project)
- No known incidents or marketplace removals
- No opaque binary downloads
- Open source (bonus, not required)
- Healthy maintenance signals (recent updates, active repo)

After completing the Subject Rubric and noting verdict-relevant findings,
**return to `SKILL.md` Step N** for the shared verdict tree, report
skeleton, and escalation guidance.
```

**Rationale:** Mirrors the established Phase 3 workflow shape. The critical distinction from browser-extension (Type 2) is that IDE plugins lack a granular permission model — risk is measured by *capability declarations*, *binary bundling/download behavior*, and *activation breadth* rather than manifest permissions. The workflow makes bundled-binary provenance a first-class audit surface because it is the dominant real-world attack vector for IDE plugins.

**Verification:** File exists. Contains the 4 required sections (Identify / Evidence / Subject Rubric / Subject Verdict Notes). References `references/criteria/ide-plugin.md`. Does not duplicate dispatcher-owned final report text.

**If this fails:** Delete `workflows/ide-plugin.md`.

---

### Step 3: Update `SKILL.md`

**Objective:** Route Type 3 to the new workflow and index new reference files.
**Confidence:** High
**Depends on:** Step 2

**Files:**
- `SKILL.md`

**Changes:**

Dispatch table row:

```markdown
// Before:
| 3 | ide-plugin | `workflows/generic.md` | Fallback — specific workflow lands in Phase 3 (M3.4) |

// After:
| 3 | ide-plugin | `workflows/ide-plugin.md` | Live — Phase 3 (M3.4) |
```

Reference Files list — two insertions to maintain the existing grouping:

```markdown
// Insert workflow bullet after ci-action workflow bullet (after the line
// `- `workflows/ci-action.md` — Type 5 ci-action workflow (Phase 3, M3.3)`):
- `workflows/ide-plugin.md` — Type 3 ide-plugin workflow (Phase 3, M3.4)

// Insert addendum bullet after ci-action addendum bullet (after the line
// `- `references/criteria/ci-action.md` — CI-action criteria addendum ...`):
- `references/criteria/ide-plugin.md` — IDE-plugin criteria addendum (marketplace trust, capability risk, bundled-binary provenance, tier thresholds)
```

**Rationale:** Dispatcher routing and reference-file index are the only `SKILL.md` edits needed. All subject logic lives in the new workflow and addendum.

**Verification:** `rg -n "ide-plugin|workflows/ide-plugin.md|references/criteria/ide-plugin.md" SKILL.md` shows row 3 -> live route plus two reference-file bullets.

**If this fails:** Revert row and remove bullets; Type 3 continues routing through `workflows/generic.md`.

---

### Step 4: Update `evals/evals.json`

**Objective:** Add positive and negative Type 3 regression coverage.
**Confidence:** High
**Depends on:** Steps 2-3

**Files:**
- `evals/evals.json`

**Changes:**

Add id 16 — clean positive path (well-known VS Code extension):

```json
{
  "id": 16,
  "prompt": "Is the Prettier VS Code extension safe to install? I want to use it for code formatting. The extension is published by 'Prettier' on the VS Code Marketplace.",
  "expected_output": "Tier 1 quick audit. Routes to ide-plugin workflow. Should recognize Prettier as a well-known open-source project with a verified publisher on VS Code Marketplace, note the high install count (tens of millions), confirm capabilities are proportional (formatting commands, language support), and return APPROVED.",
  "files": [],
  "assertions": [
    {"text": "Subject type is ide-plugin", "type": "contains_concept"},
    {"text": "Report identifies Prettier as a known project or verified publisher", "type": "contains_concept"},
    {"text": "Report notes high install count or widespread adoption", "type": "contains_concept"},
    {"text": "Report notes capabilities are proportional to stated purpose (formatting)", "type": "contains_concept"},
    {"text": "Verdict is APPROVED", "type": "exact_match"},
    {"text": "Audit confidence", "type": "contains_concept"}
  ]
}
```

Add id 17 — negative sideloaded/unknown path:

```json
{
  "id": 17,
  "prompt": "A colleague sent me a .vsix file called 'super-intellisense-pro.vsix' over Slack. They said it makes autocomplete way better. Should I install it?",
  "expected_output": "Tier 3 deep audit. Routes to ide-plugin workflow. Should flag the sideloaded distribution (no marketplace listing), Slack-shared provenance, unknown publisher, inability to verify capabilities or binary contents without manual VSIX inspection. Verdict must be REJECTED.",
  "files": [],
  "assertions": [
    {"text": "Subject type is ide-plugin", "type": "contains_concept"},
    {"text": "Report flags sideloaded or non-marketplace distribution as high risk", "type": "contains_concept"},
    {"text": "Report flags unknown publisher or unverifiable provenance", "type": "contains_concept"},
    {"text": "Report flags Slack-shared or direct-file distribution", "type": "contains_concept"},
    {"text": "Verdict is REJECTED", "type": "exact_match"},
    {"text": "## Audit Coverage", "type": "contains_string"},
    {"text": "Audit confidence", "type": "contains_concept"}
  ]
}
```

Do not rewrite existing ids 0-15.

**Rationale:** These two evals force the workflow to prove the two core M3.4 promises: it can approve a well-known verified-publisher plugin and reject a sideloaded unknown-provenance plugin shared via chat.

**Verification:** `python -c "import json; json.load(open('evals/evals.json', encoding='utf-8'))"` succeeds. IDs 16 and 17 exist. Total eval count becomes 18.

**If this fails:** Revert `evals/evals.json`.

---

## Verification Plan

### Automated Checks

- [ ] `python -c "import json; json.load(open('evals/evals.json', encoding='utf-8'))"`
- [ ] `rg -n "ide-plugin|workflows/ide-plugin.md|references/criteria/ide-plugin.md" SKILL.md`
- [ ] `rg -n "^## " workflows/ide-plugin.md` shows Identify / Evidence / Subject Rubric / Subject Verdict Notes
- [ ] File exists: `workflows/ide-plugin.md`
- [ ] File exists: `references/criteria/ide-plugin.md`

### Manual Verification

- [ ] Read `references/criteria/ide-plugin.md` end-to-end; confirm marketplace trust signals, capability risk, bundled-binary patterns, and tier thresholds are internally consistent
- [ ] Read `workflows/ide-plugin.md` end-to-end; confirm it handles non-VS-Code editors with reduced-confidence notes rather than pretending full parity
- [ ] Mental-trace eval id 16 through the workflow; confirm APPROVED is reachable because Prettier is verified-publisher, high installs, proportional capabilities
- [ ] Mental-trace eval id 17 through the workflow; confirm REJECTED follows from sideloaded VSIX, Slack-shared, unknown publisher without needing extra assumptions

### Acceptance Criteria Validation

| Criterion | How to Verify | Expected Result |
|-----------|---------------|-----------------|
| Workflow exists with correct template | Read `workflows/ide-plugin.md` | 4 required sections present |
| Addendum exists with IDE scoring | Read `references/criteria/ide-plugin.md` | Marketplace trust, capability risk, bundled-binary, tier sections present |
| Dispatcher routes Type 3 correctly | Grep `SKILL.md` | Row 3 -> `workflows/ide-plugin.md`; Reference Files bullets added |
| Positive Type 3 eval exists | Read `evals/evals.json` | id 16 present; APPROVED path assertions intact |
| Negative Type 3 eval exists | Read `evals/evals.json` | id 17 present; sideloaded VSIX + unknown publisher assertions intact |
| No regressions | Diff `evals/evals.json` | ids 0-15 unchanged |

---

## Rollback Plan

1. Revert `SKILL.md` row 3 and remove the two Type 3 Reference Files bullets so Type 3 falls back to `workflows/generic.md`.
2. Revert `evals/evals.json` to remove ids 16 and 17.
3. Delete `workflows/ide-plugin.md`.
4. Delete `references/criteria/ide-plugin.md`.

Rollback order front-loads routing: restore `SKILL.md` first so unfinished Type 3 docs never become live.

---

## Notes

### Risks

- **VS Code-first bias:** Type 3 includes JetBrains, Sublime, and Neovim, but milestone wording and local trust references are VS Code-native. Mitigation: state v1 is VS Code-first; map non-VS-Code marketplaces by equivalent trust concepts; mark confidence lower when marketplace-specific evidence is thin.
- **Bundled-binary inspection depth:** Many popular plugins (rust-analyzer, Pylance, Go) bundle or download substantial binaries. Mitigation: audit the provenance and download mechanism, not the binary contents; full binary analysis is out of scope for v1.
- **No granular permission model:** Unlike browser extensions, IDE plugins have no manifest-permission gate — they run with editor privileges. Mitigation: shift the risk axis to capability declarations, activation events, and binary behavior rather than pretending permissions exist where they don't.
- **Marketplace badge drift:** "Verified publisher" criteria may change. Mitigation: use badge as one signal, not the only one; corroborate with repo ownership, org identity, and install history.

### Open Questions

None. Scope bounded, precedent exists from M3.1-M3.3, and local source set contains minimum trust data needed.
