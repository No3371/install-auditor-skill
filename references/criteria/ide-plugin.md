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
