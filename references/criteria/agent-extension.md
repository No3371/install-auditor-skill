# Agent Extension — Criteria Addendum

Per-subject scoring extensions for **Type 8: agent-extension** audits.
Layers on top of `references/criteria.md`. More-specific guidance wins,
except that `references/criteria.md` §4.6 (version-integrity floor) and the
§4.3 CVE verdict classes are only tightened here, never loosened.

Covers: MCP servers (8a, local or remote), Claude Code plugins (8b) and
skills in the Agent Skills `SKILL.md` format (8c, any host that loads them).
An 8b plugin is a container: rate its bundled MCP servers under 8a, its
skills, commands and agents under 8c, and its own shell-bearing components
under Capability Scope below.

**Declared ≠ enforced.** Registry `server.json`, MCPB `manifest.json`,
marketplace entries, `plugin.json` and README tool lists are publisher
claims. MCP servers expose tools at runtime and may change them while
connected (`list_changed`). Rate what the code and the host actually do.

## Distribution / Discovery Channel Trust Signals

| Channel | Signal / how to verify | Rating |
|---|---|---|
| Anthropic-operated marketplace | Reserved name (e.g. `claude-plugins-official`) whose marketplace source is under `github.com/anthropics/`; check the source in `/plugin` → Marketplaces | Strong positive for the catalog; still rate each listed plugin's own author and source |
| Vendor first-party | Published by the service's own org (e.g. `@brave/brave-search-mcp-server`), or a remote endpoint on the vendor's documented domain | Strong positive for identity (V2 expected identity = vendor docs) |
| MCP reference server | `github.com/modelcontextprotocol/servers` (npm `@modelcontextprotocol/server-*`, PyPI `mcp-server-*`); maintained by the MCP steering group (project under the Linux Foundation's Agentic AI Foundation since Dec 2025); README calls them educational reference implementations, not production-ready | Moderate positive identity. Not a Tier 1 basis for Medium-or-higher capabilities; CVE row mandatory (scoping-bypass advisories exist) |
| Official MCP Registry | `registry.modelcontextprotocol.io` (preview at last review); namespace ownership checked at publish (GitHub OAuth/OIDC, DNS or HTTP) | Identity signal only: `io.github.<owner>/*` = that GitHub account, reverse-DNS = domain owner. No documented code review; rate the package layer by its registry |
| Aggregator directory | mcp.so, Glama, Smithery listings | Discovery only; neutral. Find the real source and rate that |
| Third-party hosted server | A platform runs someone else's server for you | The host operator is an extra party seeing all traffic and credentials: MEDIUM flag unless the operator is the vendor |
| Third-party plugin marketplace | Any repo or URL serving `.claude-plugin/marketplace.json`; the owner of that repo controls the catalog | Rate as the repo owner (GitHub org vs personal rows). Auto-update is off by default for third-party marketplaces |
| Skill marketplace / registry | Community skill hubs; "scanned" or "verified" badges | Low. Mass-malware campaigns hit these (e.g. ClawHavoc on ClawHub, Feb 2026, hundreds of skills) and scanner bypasses are reported; a scan pass is a weak signal at most |
| Package-launched server | `npx`/`uvx`/`pipx`/`docker run` line in an MCP config | Rate the package or image layer with `references/criteria/registry-package.md` or `container-image.md`, then the MCP surface here |
| MCPB / `.dxt` bundle | One-click desktop bundle, or a plugin `mcpServers` path/URL ending `.mcpb`/`.dxt` | Bundle manifest declares, does not sandbox. Rate the bundle's source; a URL without a pinned digest = unpinned |
| GitHub repo, established org | Org-maintained; release history; CI | Moderate positive |
| GitHub repo, personal / new | Individual; little history | Weak positive at best |
| Repo-borne config | `.mcp.json`, `.claude/settings.json`, `.claude/skills/` arriving with a cloned repo | Low: the only gate is the host's trust and approval prompts (see Repo-Borne Surfaces) |
| Peer-shared config / unknown clone | Slack, Discord, paste, gist; no listing | HIGH flag; lowest provenance |

## Capability Scope Classification

**Risk is the default flag level** for the finding; Notes say what lowers
or raises it.

| Capability | Risk | Notes |
|---|---|---|
| Read-only data (time, static lookups, public docs) | Low | |
| File-system read | Medium | Record path scope |
| File-system write | High | MEDIUM when scoped to a user-named directory and the version is at or above the last fixed path-validation advisory |
| Network outbound to arbitrary hosts | High | Fixed vendor API host only = part of own-service row |
| Database access | High | Mutation depends on grants |
| Own-service credential | High | Least-scope key or token for the one service the extension fronts, from a V2-verified publisher. MEDIUM when the host keeps it in a secret store (OAuth token store, keychain, plugin `userConfig` `sensitive`) rather than a config file or `env` line |
| Other credentials | Critical | Keys for other services, credential stores, broad env or dotfile reads, or **any** credential handed to code from an unverified publisher |
| Shell surface | Critical | MCP tools that run commands; plugin hooks (`type: command`), monitors, `bin/` executables, LSP server commands, `headersHelper`; `command` plugin sources; skill `` !`cmd` `` / ```` ```! ```` injection; scripts a skill tells the agent to run. Rate with Shell-Surface Rating |
| Self-granted tool permission | High | Skill `allowed-tools`, command `allowedTools`: pre-approves tools without prompting, and workspace trust does not gate skill `allowed-tools`. Critical when it covers Bash/Write and the body directs shell use |
| Tool-call interception | High | Hooks returning permission decisions, rewriting tool input (`updatedInput`) or output (`updatedToolOutput`), or injecting `additionalContext`; `type: http` hooks send event data off-machine |
| Lethal trifecta in one extension | Critical | Private-data read + untrusted-content ingestion + egress. When the user's other servers complete it: HIGH |

### Shell-Surface Rating

- **CRITICAL** — not reviewed; or it downloads and runs remote code, is
  obfuscated, reads credentials beyond its own, or writes agent/host
  config outside its own directory.
- **HIGH** — reviewed; runs only bundled or named local tools; but runs
  unattended (session-start hooks, `PreToolUse` on broad matchers,
  monitors, `bin/` on `PATH`, a `command` source that re-runs each
  session). Condition: install the reviewed version pinned; re-audit
  on any shell-component change.
- **MEDIUM** — reviewed; bounded commands that run only when the user
  invokes them (slash command, user-invoked skill).

## Transport & Auth (8a)

| Transport | Flag | Check |
|---|---|---|
| stdio (local process) | None | Runs with the user's privileges; the capability table governs |
| Streamable HTTP, loopback | LOW | Spec: bind to `127.0.0.1` and validate `Origin`. Bound to `0.0.0.0` or no `Origin` check → HIGH (network or DNS-rebinding reach) |
| Streamable HTTP, remote, vendor-operated | MEDIUM | TLS host = vendor's documented domain; OAuth or least-scope token |
| Streamable HTTP, remote, other operator | HIGH | Operator sees all traffic and credentials |
| WebSocket (host-supported) | As the HTTP rows, by address and operator | Not a core MCP transport; check host docs |
| HTTP+SSE (legacy) | +MEDIUM `legacy transport` | Deprecated in the MCP spec and in Claude Code; signals an unmaintained server |
| `http://` or `ws://` to a non-loopback host | HIGH; CRITICAL with credentials or private data | No TLS |

Remote auth modes: **none** (HIGH unless public read-only data) |
**static token** (MEDIUM; literal token in a committed file = HIGH) |
**OAuth** (issuer must be the vendor's documented authorization server;
pin scopes where the host allows, e.g. `oauth.scopes`; rate scopes, vendor
data use and token custody with `references/criteria/remote-integration.md`
§1, §5 and §6). A `headersHelper` is shell surface.

## Behavioral & Model-Context Risk (all sub-types)

Tool names, descriptions, input schemas and results enter model context, as
do skill bodies, agents, output styles and hook `additionalContext`.

| Indicator | Rating |
|---|---|
| Tool poisoning: hidden or imperative instructions in names, descriptions, schemas or results (read files, call other tools, hide actions from the user) | CRITICAL |
| Exfiltration steering: instructions that move user data, secrets or code to the extension or a third party | CRITICAL |
| "Prerequisite" lure: instructions to download and run an installer, paste a command, or pipe a URL to a shell | CRITICAL |
| Config hijack: writes other servers' or hosts' configs, `settings.json`, shell rc files, or adds MCP servers | CRITICAL |
| Endpoint or credential redirection: `env` that overrides API base URLs, proxies or credential helpers | CRITICAL |
| Shadowing: descriptions that redefine other tools' behavior; a skill or command named like a bundled or built-in one (it replaces it) | HIGH |
| Persistence: skill `hooks` (active for the rest of the session), monitors, session-start hooks, background `context: fork` runs | HIGH |
| Indirect-injection channel: tools returning untrusted external content (web, email, issues, documents) | MEDIUM alone; part of the trifecta |
| Context crowding or output-style override | MEDIUM |

## Repo-Borne Surfaces

A cloned repository can carry `.mcp.json`, `.claude/settings.json` (hooks,
`env`, `enabledPlugins`, `extraKnownMarketplaces`,
`enableAllProjectMcpServers`, `enabledMcpjsonServers`) and `.claude/skills/`.

- Interactive Claude Code asks for workspace trust and per-server approval
  of project `.mcp.json` servers. In `claude -p`, Agent SDK and cloud
  sessions, project servers load **without asking**, and project skills'
  `allowed-tools` apply even in an untrusted folder. Rate repo-borne
  extensions as installed for any headless or CI use.
- Auto-approve keys committed to the repo = HIGH (they take effect once
  the folder is trusted).
- **Harness version:** check the host's security advisories (for Claude
  Code, `github.com/anthropics/claude-code/security/advisories`). Past
  releases fixed trust-dialog and plugin-pin bypasses; a host below a
  fixed release for an advisory that touches this subject = HIGH;
  condition: upgrade.
- **Controls to cite in conditions:** `disabledMcpjsonServers`,
  `--strict-mcp-config`, `--setting-sources`; managed `allowedMcpServers` /
  `deniedMcpServers` / `managed-mcp.json`; `allowManagedPermissionRulesOnly`
  (ignores skill `allowed-tools`); `disableSkillShellExecution`;
  `strictKnownMarketplaces` / `blockedMarketplaces`;
  `disableCommandPluginSources`; deny rules such as `Skill(name *)`.

## Version & Update Integrity (§4.6)

- **V1** — Publish time: package registry time for package-launched
  servers (`scripts/registry-lookup`); commit or tag date of the pinned
  SHA for git sources; release-asset date for bundles and archives.
  Version unit: content identity (package version, commit SHA, archive
  `sha256`, image digest). A plugin `version` string is not one — it can
  stay the same across commits. Hosted remote servers: per the floor's
  hosted-services rule.
- **V2** — Expected identity: the package publisher and provenance repo
  (registry-package rules); MCP Registry namespace; the vendor docs page
  naming the package or endpoint; marketplace source owner
  (`github.com/anthropics/` for reserved names); TLS host and OAuth issuer
  for remote servers. Claude Code plugins and skills have no documented
  signing, so absence of a signature is not a flag; identity rests on
  source owner + pin.
- **V3** — Diff against the prior release: tool names, descriptions and
  input schemas (source registration code, or the host's tool list for a
  remote server); plugin component inventory (new hooks, monitors, `bin/`,
  `mcpServers`, `dependencies`, `userConfig` secrets); skill frontmatter
  (`allowed-tools`, `hooks`, `context`); OAuth scopes. A marketplace entry
  re-pointed to a different repo or source type = HIGH.
- **V4** — Extra incident sources: host and server repo security advisories
  (GHSA), OSV `MAL-` for the package layer, marketplace delistings (Claude
  Code lists plugins it uninstalled after a delisting as Flagged),
  skill-hub takedowns.
- **V5** — Triggers: tool-set or tool-description change; new plugin
  component type or dependency; new skill `allowed-tools` or `hooks`;
  marketplace source change; OAuth scope change; remote operator or terms
  change. Update controls: exact version in the launch line
  (`npx -y <pkg>@<x.y.z>`, `uvx <pkg>==<x.y.z>`, image digest); plugin
  source `sha` or `archive` `sha256`; marketplace `autoUpdate` off (default
  off for third-party marketplaces; on for `claude-plugins-official` and
  marketplaces added from claude.ai). A launch line or plugin
  source without an exact pin is HIGH `unpinned launcher` (a later launch
  or update can run an unaudited release) → condition: pin. A `command`
  source re-runs every session and cannot be held; say so. Remote servers
  cannot be held: list the triggers.
- **§4.3 own-code line** — Own code: the extension publisher's server,
  plugin components, skill scripts and bundled MCP servers they author.
  Third-party: package dependencies, base images, bundled servers by other
  publishers (sub-audit those as their own subjects). The host harness is
  not part of the subject; its advisories go under Repo-Borne Surfaces.

## Tier Thresholds

### Tier 1 — Quick Audit

ALL must hold:
- Publisher identity verified (V2): Anthropic-operated, vendor
  first-party, MCP reference server, or established org with ≥ 6 months
  of releases
- Every capability Low; no shell surface, self-granted tools, hooks or
  credentials
- stdio transport (8a), or a skill with no frontmatter grants (8c)
- No behavioral indicator; launch line or source pinned to an exact
  version
- §4.6 does not bar Tier 1; no CVE in the requested version; no incident

### Tier 2 — Standard Audit

Anything that is neither Tier 1 nor Tier 3. Typical: Medium/High
capabilities without shell surface (fs read, directory-scoped fs write,
own-service credential, outbound to a fixed vendor API); reference servers
above Low capability; loopback HTTP; remote Streamable HTTP to a vendor
first-party endpoint with OAuth; unpinned launcher; legacy SSE; available
1–6 months.

### Tier 3 — Deep Audit

ANY triggers it:
- Shell surface of any kind; other credentials; lethal trifecta in one
  extension; fs write outside a user-named directory
- Publisher unknown or unverified; peer-shared config; unknown clone;
  skill-hub listing with no verified author; repo-borne config the user
  did not write
- Remote server with no auth, plain `http://`, or a third-party operator
- Any CRITICAL behavioral indicator seen at triage
- `command` plugin source; bundle or archive URL without a pinned digest
- Any §4.6 V3 HIGH or V4 finding; available < 1 month or no version history
