# Subject Classifier — Innermost Trust Boundary

Companion to `SKILL.md` Step 0. Step 0 holds the procedure, confidence
table, signal summary, and required output shape. This file holds the full
rule: tie-breaking, per-type routing overrides, extended signals, worked
hybrid examples, and edge-case discipline. Read it when Step 0 does not
resolve cleanly on its own.

## The Rule

**Classify an installable by the innermost trust boundary the user is
crossing when they perform the install action.**

A *trust boundary* is a verification and gating layer the installable passes
through before landing on the user's system. When boundaries nest (an npm
package shipped inside a container image; a VS Code extension wrapping a
binary; a CLI pulled via a CI action), pick the **innermost** — the last
verification gate between the user and the code that actually executes, i.e.
the gate the user personally crosses for this install action.

Everything nested beneath that gate (bundled packages, wrapped binaries,
images pulled internally) is downstream. The chosen workflow audits it as a
sub-step; it is never a reason to re-classify. The outermost boundary is
usually the biggest brand (Docker Hub, GitHub) and is the wrong place to
calibrate the rubric.

## Tie-Breaking

1. Exactly one type matches with strong signals → that type, **high**.
2. Several types match → pick the type whose boundary the user crosses last
   before the code runs. Resolves cleanly → **high**. Narrows to a single
   best candidate without fully resolving → **medium**: route to that
   workflow and state the uncertainty in Rationale.
3. No strong match, or the conflict survives the rule → `generic`, **low**.
   Name the missing or conflicting signal in Rationale.

## Confidence Examples

| Level | Example |
|---|---|
| High | `https://www.npmjs.com/package/express` → registry-package |
| Medium | `github.com/owner/repo` whose README says it publishes to npm → registry-package (boundary inferred, not stated) |
| Low | Monorepo shipping a Dockerfile, an npm package, and a VS Code extension behind `make install` → generic (rule cannot separate them) |

Prefer a `generic` route with a precise "signals conflict: X vs Y" rationale
over a confident misroute — a misroute applies the wrong rubric for the
whole audit.

## Type 8 Sub-Rubric

- **8a · MCP server** — process / binary / script advertising MCP tools,
  referenced from an MCP config (`.mcp.json`, Claude Desktop config,
  `claude mcp add`) or shipped as an `.mcpb` / `.dxt` bundle; **or** a remote
  MCP endpoint the agent host connects to by URL (Streamable HTTP, legacy
  SSE), incl. AI-assistant "custom connectors" — no local code
- **8b · Claude Code plugin** — plugin (`.claude-plugin/plugin.json`;
  commands, skills, agents, hooks, MCP / LSP servers, `bin/`) installed with
  `/plugin install` / `claude plugin install` from a marketplace
  (`.claude-plugin/marketplace.json`) or loaded from a local directory
- **8c · Claude Code skill** — directory containing `SKILL.md` (plus optional
  `scripts/`, `references/`, `evals/`); the Agent Skills format, also loaded
  by other agent hosts

## Routing Overrides

| Subject | Routes to | Why |
|---|---|---|
| Registry package whose `bin` ships a CLI (`prettier`, `typescript`) | registry-package | Registry publish is the gate; the CLI is downstream |
| Package consumed only as a transitive dependency | registry-package (parent audit's transitive surface) | Not a separate install |
| Electron / desktop app shipped through npm | registry-package | Innermost gate is the registry |
| Claude Code skill or plugin installed with `npm install` | registry-package | `npm install` is the gate; skill content is reviewed inside the registry-package audit |
| Browser extension that wraps a CLI binary | browser-extension | The store is the install pipe |
| VS Code extension wrapping a binary (`rust-analyzer`) | ide-plugin | Marketplace is the verification layer |
| MCP server installed via a VS Code extension | ide-plugin | Marketplace is innermost; the MCP server is downstream |
| Claude Code plugin or skill installed directly | agent-extension | Distinct boundary from IDE marketplaces |
| Claude Code plugin from a marketplace whose entry has `source: npm` (or any other source type) | agent-extension (8b) | `/plugin install` is the gate: the marketplace entry picks the source and Claude Code fetches it; npm is transport, not the boundary the user crosses |
| Remote MCP server or AI-assistant connector that adds tools the assistant calls (custom connector by URL, connector directory entry, `claude mcp add --transport http`) | agent-extension (8a) | The agent host's MCP connection is the innermost gate: tool descriptions enter the model's context and tools act for the user. Audit any OAuth grant and the operator's data handling as a sub-step borrowed from `workflows/remote-integration.md` |
| SaaS or AI app that gets OAuth / API-key access to your data and exposes no tools to your agent (incl. "AI over your Slack / Drive" apps) | remote-integration | The consent grant is the gate; AI sub-processing and data use are rated there |
| Container image whose entrypoint is an npm app | container-image | The registry pull is the gate; npm review is a sub-step |
| GitHub Action that pulls a container image | ci-action | The `uses:` reference is the install surface |
| CLI via Homebrew core (`brew install <formula>`) | cli-binary | Formula review + checksum + build-from-source; casks route to desktop-app |
| App via Homebrew cask (`brew install --cask`) | desktop-app | Cask installs a packaged application |
| SaaS that also installs a local agent | The component this request installs or connects | Classify one primary boundary; name the other component in the report and recommend a separate audit (one report per installable) |
| Pipe-to-shell (`curl … \| sh`, `irm … \| iex`) whose URL hides the publisher (shortener, paste site, raw IP) | cli-binary, **medium** | The pipe-to-shell is the install pipe; the unknown payload is residual uncertainty that the workflow's install-script review handles (download, read, never pipe) |
| Web portal, bookmark or certificate prompt with no installable artifact named | generic, **low** | No type covers trust-store or certificate changes; `workflows/generic.md` Phase 3 rates the trust grant |

## Extended Signal Patterns

Full pattern list behind Step 0's signal summary.

| # | Type | Primary signals | Strong URL / path patterns |
|---|---|---|---|
| 1 | registry-package | `npm install`, `pip install`, `cargo add`, `gem install`, `go get`, `nuget add`, `mvn dependency`, `composer require`; `package.json` / `pyproject.toml` / `Cargo.toml` / `Gemfile` / `go.mod` / `*.csproj` / `pom.xml`; IaC manifests referencing Terraform Registry / Ansible Galaxy / Artifact Hub | `npmjs.com/package/*`, `pypi.org/project/*`, `rubygems.org/gems/*`, `crates.io/crates/*`, `central.sonatype.com/*`, `nuget.org/packages/*`, `pkg.go.dev/*`, `registry.terraform.io/*`, `galaxy.ansible.com/*`, `artifacthub.io/*` |
| 2 | browser-extension | Manifest with `manifest_version` + `permissions` + `host_permissions`; "browser extension", "add-on", "MV2/MV3", "content script" | `chromewebstore.google.com/*`, `addons.mozilla.org/*`, `microsoftedge.microsoft.com/addons/*`, `.crx` / `.xpi` files |
| 3 | ide-plugin | `code --install-extension`, VSIX file, JetBrains plugin ID, Sublime Package Control manifest, vim-plug / lazy.nvim / packer spec, MELPA recipe | `marketplace.visualstudio.com/items*`, `open-vsx.org/extension/*`, `plugins.jetbrains.com/plugin/*`, `packagecontrol.io/packages/*` |
| 4 | container-image | `docker pull`, `docker run`, `podman pull`, `FROM` in a Dockerfile, `image:tag`, `sha256:` digest | `hub.docker.com/*`, `ghcr.io/*`, `quay.io/*`, `*.dkr.ecr.*.amazonaws.com`, `gcr.io/*`, `public.ecr.aws/*` |
| 5 | ci-action | `uses:` in `.github/workflows/*.yml`, GitLab `include:` component, CircleCI `orbs:`, reusable workflow reference | `github.com/<owner>/<action>@<ref>`, `gitlab.com/.../components/*`, `circleci.com/orbs/*` |
| 6 | desktop-app | `.msi` / `.dmg` / `.deb` / `.rpm` / `.pkg` / `.appx`; `brew install --cask`, `winget install`, `choco install`; OS package-manager context | `apps.microsoft.com/*`, `apps.apple.com/*`, `formulae.brew.sh/cask/*`, `winget.run/pkg/*`, `community.chocolatey.org/packages/*` |
| 7 | cli-binary | `curl … \| sh`, `wget … \| bash`, `sh -c "$(curl …)"`, `bash <(curl …)`; PowerShell `irm … \| iex`, `iwr … \| iex`, `iex (irm …)`, `Invoke-Expression` over `(New-Object Net.WebClient).DownloadString(…)`; GitHub Releases binary, `brew install <formula>` (Homebrew core), version managers (nvm / pyenv / rustup / volta), direct executable URL, checksum / signature file beside a binary | `github.com/*/releases/download/*`, `formulae.brew.sh/formula/*`, `get.<vendor>.sh`-style install scripts, `*.ps1` install-script URLs, vendor-hosted binary URLs |
| 8 | agent-extension | MCP server config / stdio command, `claude mcp add`, remote MCP URL (Streamable HTTP / SSE) or AI-assistant custom connector, `.mcpb` / `.dxt` bundle; Claude Code plugin (`.claude-plugin/plugin.json`), `/plugin install`, `claude plugin install`, `/plugin marketplace add`; skill with `SKILL.md`, `npx skills add`; agent host context (Claude Code / Desktop, Cursor, Codex, VS Code agent mode, other MCP or Agent Skills hosts) | `.mcp.json` entries, `.claude-plugin/marketplace.json`, `.claude/skills/*`, `registry.modelcontextprotocol.io/*`, `modelcontextprotocol.io/*`, `mcp.so/*`, `skills.sh/*` |
| 9 | remote-integration | OAuth flow, API key or service-account key exchange, webhook endpoint, "Connect to <service>"; no local code install and no MCP tools exposed to the user's agent | Vendor OAuth URLs, `hooks.slack.com/*`, vendor integrations / marketplace pages, `api.*.com/*` key-exchange endpoints |
| 0 | generic | No specific-type signal fires strongly, or conflict survives the rule | — |

## Worked Hybrid Examples

1. **npm package whose `bin` ships a CLI** (`prettier`) → **registry-package**,
   high. The CLI exists only because npm delivered it.
2. **VS Code extension wrapping a binary** (`rust-analyzer` + LSP server) →
   **ide-plugin**, high. The user clicks Install in VS Code; the bundled binary
   is audited under the ide-plugin rubric.
3. **Docker image whose entrypoint is an npm app** → **container-image**, high.
   The user runs `docker pull`; npm packages inside are a sub-step of
   `workflows/container-image.md` when they warrant attention.
4. **GitHub Action that pulls a Docker image internally**
   (`docker/build-push-action`) → **ci-action**, high. The image is an
   implementation detail covered by the transitive surface of
   `workflows/ci-action.md`.
5. **Claude Code skill installed with `npm install`** → **registry-package**,
   high. If the skill content is the main concern, the registry-package audit
   may apply agent-extension 8c signals as a sub-rubric.
6. **Claude Code plugin from a marketplace entry with `source: npm`**
   (`/plugin install x@mkt`) → **agent-extension** (8b), high. The user
   crosses the marketplace + `/plugin install` gate; npm is only how Claude
   Code fetches the files. Contrast example 5, where `npm install` is the gate.
7. **Remote MCP connector added to an AI assistant by URL, with OAuth
   sign-in** → **agent-extension** (8a), high. No local code; the host loads
   the server's tools into the model's context. The 8a audit covers the tool
   surface and transport; OAuth scopes and the operator's data handling are a
   sub-step borrowed from `workflows/remote-integration.md`. A SaaS app that
   only gets OAuth access to your data, with no tools for your agent, stays
   **remote-integration**.
8. **PowerShell one-liner behind a URL shortener**
   (`iex ((New-Object Net.WebClient).DownloadString('http://bit.ly/…'))`) →
   **cli-binary**, medium. Pipe-to-shell is the install pipe even when the
   payload is unknown; `workflows/cli-binary.md` rates an unverifiable install
   script toward REJECTED.

## Edge-Case Discipline

- **One installable → one type.** Never split an audit at classification. The
  routed workflow decides whether to sub-audit a secondary component and may
  borrow a sibling workflow's sub-steps without re-routing.
- **User override is honored.** "Treat this as `<type>`" → that type at high
  confidence, Rationale `user override: <verbatim>`.
- **Read-only.** Signals come only from URLs, manifests, names, and stated
  intent. Never run install scripts or probes to classify; evidence
  acquisition starts inside the routed workflow.
- **No re-classification mid-audit.** Once routed, the workflow owns the audit.
  Sole exception: `workflows/generic.md` Phase 2 re-routes after the user
  confirms the type.
