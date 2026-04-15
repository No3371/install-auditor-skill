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
