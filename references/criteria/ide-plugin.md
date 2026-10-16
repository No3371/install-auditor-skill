# IDE Plugin — Criteria Addendum

Per-subject scoring extensions for **Type 3: ide-plugin** audits.
Layers on top of `references/criteria.md`. More-specific guidance wins,
except over the §4.6 version-integrity floor, which this file only
tightens or fills (`## Version & Update Integrity (§4.6)` below).

Covers: VS Code Marketplace, Open VSX, VS Code forks (Cursor, Windsurf,
VSCodium and similar editors that install from Open VSX or their own
gallery), JetBrains Marketplace, Sublime Package Control, Neovim plugin
managers (lazy.nvim, vim-plug, built-in `vim.pack`; packer.nvim is
unmaintained). Depth is VS Code Marketplace-first.

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
| `*` or `onStartupFinished` activation event | Medium | Code runs on every editor start (`onStartupFinished` only defers it until startup finishes) |
| `extensionDependencies` / `extensionPack` | Medium-High | Installs other extensions, maybe from other publishers; a later update can add or swap one (delayed payload) |
| `languageModelTools` | Medium-High | Agent-invokable tools with full extension-host privileges; users can "Always Allow" past the per-call prompt |
| `mcpServerDefinitionProviders` | Medium-High | Registers MCP servers the agent runs; apply `workflows/agent-extension.md` 8a signals to each |
| `chatParticipants` / `chatAgents` / `chatInstructions` / `chatPromptFiles` / `chatSkills` | Medium | Injects prompts, instructions or agents into chat |
| `languageModelChatProviders` | Medium-High | Sends prompts and code context to the extension's model backend; may take API keys |

### JetBrains — extension points

| Capability | Risk | Why |
|------------|------|-----|
| Language support / inspections | Low | Static analysis; no external execution |
| Tool window / UI contributions | Low-Medium | UI modification only |
| Run configuration / external tools | Medium-High | Executes processes |
| Project-level hooks (postStartupActivity) | Medium | Runs on project open |
| Custom compiler / build tool integration | High | Executes build pipelines |
| Settings that accept AI-provider API keys or tokens | High | Attacker-preferred category (June 2026 campaign sent keys to its own server on "Apply"); check where the key is sent |

### Sublime / Neovim

Sublime plugins are Python scripts running in Sublime's embedded interpreter.
Neovim plugins are Lua/Vimscript running in-process or remote plugins over
RPC. Both have full host-process access; the risk is essentially
"what code runs and what does it call."

### Scoring impact

- Theme/syntax/snippet only = neutral
- Command-only activation with scoped triggers = low risk
- Debugger, task, terminal, or build-tool integration = elevated review
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

## Bundled Binary / Download-at-Runtime Risk

The dominant attack surface for IDE plugins: many plugins bundle or download
language servers, formatters, linters, or other executables.

| Pattern | Risk | Guidance |
|---------|------|----------|
| Plugin bundles compiled binary in VSIX/ZIP | Medium-High | Inspect binary provenance; check if it matches a known project release |
| Plugin downloads binary on first activation | High | Note the download URL; verify it points to a known project's release assets with checksums |
| Plugin invokes system-installed tool (`PATH` lookup) | Low-Medium | Relies on user-installed tool; note the dependency |
| Plugin compiles from source on install | Medium | Transparent but may execute untrusted build scripts |
| `scripts.vscode:uninstall` (VS Code) | Low-Medium | Runs a Node script on uninstall; check what it deletes or contacts. VS Code has no install hook: downloads happen in activation code |
| No binary component | Low | Pure JS/TS/Python/Lua plugin |

### Scoring impact

- No binary = positive signal
- Bundles binary from a known, tagged, signed upstream = moderate
- Downloads binary at runtime from author's server without checksum = high-risk finding
- Downloads binary from unknown/opaque URL = strong negative

## Tier Thresholds (IDE Plugins)

### Tier 1 — Quick Audit

ALL of these must hold:
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
