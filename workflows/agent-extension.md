<!--
This workflow replaces workflows/generic.md for Type 8 subjects. After
producing findings here, return to SKILL.md Step N for the shared verdict
tree and report shape. The Audit Coverage table and audit-confidence
assertion are owned by the dispatcher — do not duplicate them here.
-->

# Agent Extension Workflow (Type 8)

This workflow handles **Type 8: agent-extension** subjects — code or
content that extends an AI agent with tools, prompts, hooks, skills or
context and runs with access to the agent's capability surface:

- **8a · MCP server** — local (stdio) or remote (Streamable HTTP); any host
- **8b · Claude Code plugin** — a bundle that can hold skills, commands,
  agents, hooks, MCP and LSP servers, monitors, `bin/` executables and
  settings. Treat it as a container: 8a and 8c sub-audits plus its own
  shell surface
- **8c · Skill** — a `SKILL.md` directory (Agent Skills format) for Claude
  Code or another host that loads it

After completing all sections below, return to `SKILL.md` Step N for the
shared verdict tree and audit-coverage report shape. Sections follow the
standard workflow template: **Identify / Evidence / Subject Rubric /
Subject Verdict Notes**.

Use `references/criteria/agent-extension.md` (the addendum) for tiering
and scoring. When it conflicts with the shared rubric, the addendum wins,
except for `references/criteria.md` §4.6 and the §4.3 CVE verdict
classes, which it only tightens. Rate what the code and the host do, not
what manifests and READMEs claim.

## Identify

### 1. Determine sub-type and distribution channel

| Install pattern / signal | Sub-type | Channel (addendum row) |
|---|---|---|
| MCP config entry (`.mcp.json`, Claude Desktop config, `claude mcp add`) with `command` | 8a | Config-referenced; rate the code it launches |
| `npx -y <pkg>`, `uvx <pkg>`, `pipx run`, `docker run` in that entry | 8a | Package-launched server |
| MCP config entry with `url` (`--transport http`, `ws`, `sse`), or a connector added by URL | 8a remote | Vendor first-party or third-party hosted |
| `registry.modelcontextprotocol.io` entry / `server.json` | 8a | Official MCP Registry |
| mcp.so, Glama or Smithery listing | 8a | Aggregator — find the real source |
| `.mcpb` / `.dxt` file | 8a | MCPB bundle |
| `/plugin install <name>@<marketplace>`, `claude plugin install`, `enabledPlugins` entry, `.claude-plugin/plugin.json` or `marketplace.json` (any entry `source` type, incl. `npm`) | 8b | Anthropic-operated or third-party marketplace |
| `--plugin-dir`, `--plugin-url`, plugin directory under `.claude/skills/` | 8b | Local / repo |
| Directory with `SKILL.md` (`~/.claude/skills/`, `.claude/skills/`, skill hub, git clone) | 8c | Skill hub, GitHub repo, local |
| Repo carrying `.mcp.json`, `.claude/settings.json` or `.claude/skills/` | Per component | Repo-borne (see Evidence B) |
| MCP server or skill for another host (Cursor, VS Code, Codex, etc.) | 8a / 8c | Host-specific; same procedure |

Remote MCP servers and AI-assistant connectors that add tools the agent
calls route here as 8a even with no local code. Run the 8a remote steps;
rows that need a versioned artifact become `N/A (hosted service)` per the
row contract in `references/criteria.md`.

### 2. Gather required context

1. Name and exact version or pin: package version, commit SHA, archive
   `sha256`, image digest, or endpoint URL
2. Sub-type (8a / 8b / 8c)
3. Channel and source: marketplace name and its source; plugin entry
   `source` type with `ref` / `sha` / `sha256` / `version`; launch line
4. Publisher and where its expected identity is documented (V2)
5. Host(s) and run mode: interactive, or `claude -p` / Agent SDK / CI /
   cloud (approval prompts differ)

If 1–4 are missing, ask before proceeding. Capabilities, transport and
behavior come from Evidence, not from the user's description.

## Evidence — Part A

**Tier Triage** — enough to apply the addendum Tier Thresholds:

- Channel and publisher → addendum channel table; V2 identity
- Claimed inventory from config, manifest or frontmatter: tool list,
  component directories, hooks, `allowed-tools`, transport, credentials
- `references/criteria.md` §4.6: V1 version age and pin; V4 incident
  search "[extension name] security OR vulnerability OR malicious"
- Host advisories if the subject is repo-borne or relies on host
  enforcement (addendum Repo-Borne Surfaces)

Tier 1 when ALL addendum Tier 1 conditions hold and §4.6 does not bar it;
Tier 3 when ANY Tier 3 trigger fires; otherwise Tier 2. Re-tier upward if
Part B finds a Tier 3 trigger.

## Evidence — Part B

Depth by tier: Tier 1 confirms the claimed inventory; Tier 2 checks it
against source; Tier 3 reviews every executable component and every
model-facing string.

### 8a — MCP server

1. **Locate the code** behind the launch line or bundle: package + version,
   repo + SHA, bundle + digest. For a remote server, identify the operator
   (vendor or third-party host).
2. **Enumerate tools** from source (tool registration code), not the
   README. For a remote server, use the vendor's docs or the tool list the
   host shows after connecting. Do not run an unreviewed server outside a
   disposable sandbox without credentials. Note that the set can change at
   runtime (`list_changed`) and between releases (V3).
3. **Read every tool name, description, input schema and sample result**
   for the addendum behavioral indicators.
4. **Classify each tool** with the capability table: path scope, egress
   hosts, credentials used, commands run.
5. **Transport and auth** per the addendum table: bind address and
   `Origin` checks for loopback; TLS host, operator and auth mode for
   remote. For an OAuth grant, run the remote-integration grant checks as
   a sub-step: `references/criteria/remote-integration.md` §1 (scope
   classes), §5 (vendor data use incl. AI use) and §6 (token custody and
   consent path). Record the tool list as the V3/V5 baseline; destructive
   or outbound tools (delete, send, pay, share) need a stated purpose.
6. **Package layer:** apply `workflows/registry-package.md` or
   `workflows/container-image.md` sub-steps (install scripts, dependencies,
   CVEs) to the launched package or image.
7. **Pin:** exact version in the launch line? Else `unpinned launcher`
   (addendum V5).

### 8b — Claude Code plugin

1. **Marketplace:** name, source repo or URL, owner. Reserved official
   names are valid only from `github.com/anthropics/`; a name or
   description that presents as Anthropic or a vendor without a matching
   source owner is impersonation. Record its `autoUpdate` state.
2. **Plugin source and pin strength:** `sha` / archive `sha256` / exact npm
   version > tag `ref` > branch or default branch. `npm` sources are
   fetched with install scripts disabled. A `command` source runs a shell
   command on install, update and once per session (shell surface). Remote
   `archive` or `.mcpb` URLs need a pinned digest.
3. **Component inventory** — from `plugin.json`, the standard layout and
   the marketplace entry (with `strict` unset or `true`, the entry adds
   components): `skills/`, `commands/`, `agents/`, `hooks/hooks.json`,
   `.mcp.json` / `mcpServers` (incl. bundle paths and URLs), `.lsp.json`,
   `monitors/monitors.json`, `bin/`, `output-styles/`, `settings.json`,
   `userConfig` (note `sensitive` fields), `dependencies`, `channels`.
4. **Shell surface:** for every hook record event, matcher and handler
   type (`command` = shell; `http` = event data leaves the machine;
   `prompt` / `agent` / `mcp_tool` = model or tool call). Add monitors,
   `bin/` files, LSP commands, `headersHelper` and the scripts they call.
   Rate each with the addendum Shell-Surface Rating.
5. **Nested sub-audits:** each bundled MCP server → 8a steps; each skill,
   command and agent → 8c steps; each `dependencies` plugin → its own 8b
   inventory (dependencies start enabled with the plugin).
6. **Rating:** the plugin's rating is the highest component rating plus
   plugin-level flags (source pin, marketplace, impersonation).

### 8c — Skill

1. **Placement:** where it installs (managed, personal, project, plugin)
   and whether its name replaces a bundled skill or built-in command
   (shadowing).
2. **Frontmatter:** `allowed-tools` (pre-approves tools; not gated by
   workspace trust), `hooks` (active for the rest of the session),
   `context: fork` with `agent` (background subagent),
   `disable-model-invocation` / `user-invocable` (who can trigger it),
   `paths`, `shell`, `model`.
3. **Shell surface:** `` !`cmd` `` and ```` ```! ```` blocks run before the
   model sees the skill, without a prompt (permission rules still apply);
   scripts the body tells the agent to run; setup or "prerequisite" steps
   that fetch and run installers.
4. **Body review:** addendum behavioral indicators; paths outside the
   skill directory (`~/.ssh`, `.env`, other configs); egress instructions.
5. **Bundled files:** `scripts/`, `references/` and assets reviewed as
   code (Tier 2 skim, Tier 3 full).

### Repo-borne extensions

When the subject arrives inside a repository, inventory `.mcp.json`,
`.claude/settings.json` (`hooks`, `env`, `enabledPlugins`,
`extraKnownMarketplaces`, auto-approve keys) and `.claude/skills/`, then
audit each component by sub-type. Apply addendum Repo-Borne Surfaces:
headless and cloud runs load project servers without asking.

### Research guidance by channel

- **Package registries:** registry-package or container-image trust
  signals for the package layer; `scripts/registry-lookup`,
  `scripts/vuln-lookup`, `scripts/typosquat-check`.
- **Marketplaces:** the marketplace repo's owner, history and
  `marketplace.json` change log; there are no usage metrics.
- **MCP Registry:** namespace ↔ repo owner or domain; then the package.
- **GitHub repos:** owner, contributors, release history, security
  advisories, CI.
- **Skill hubs, shared configs, clones:** no independent verification;
  rely on code and content review.

### Audit coverage tracking table

Carries every canonical row from `references/criteria.md` (rows by tier)
and adds subject rows. Never drop a Required row; mark rows that cannot
apply `N/A (<reason>)`.

| Check | Tier 1 | Tier 2 | Tier 3 | Source |
|---|---|---|---|---|
| Registry / metadata lookup | Required | Required | Required | Package registry, MCP Registry, `marketplace.json` |
| Typosquat / name verification | Required | Required | Required | `typosquat-check` (package layer); reserved plugin and marketplace names; vendor impersonation |
| CVE / advisories (requested version) | Required | Required | Required | OSV, GHSA, repo advisories; `N/A (hosted service)` for URL-only servers |
| License compatibility | Required | Required | Required | `references/licenses.md` |
| Version integrity (§4.6) | Required | Required | Required | Addendum §4.6 plug-in; record pin and update control |
| Channel & publisher identity | Required | Required | Required | Addendum channel table; V2 |
| Capability / component inventory | Required | Required | Required | Source, not README |
| Permissions / least privilege | Required | Required | Required | Capability table; proportional to purpose |
| Shell surface | Required | Required | Required | Hooks, monitors, `bin/`, `!` blocks, scripts, `command` source; `N/A (none)` |
| Transport & auth | Required | Required | Required | 8a only; `N/A (8c)` |
| Behavioral surface | Skim | Required | Required | Tool descriptions, skill body, frontmatter |
| Web search — incidents & supply chain | Required | Required | Required | Web search; V4 sources |
| Maintainer / activity / health | Skipped (Tier 1) | Required | Required | Releases, issues |
| OpenSSF Scorecard | Optional | Required (Done or Not available) | Required | When repo known |
| Dependency tree / transitive risk | Skipped (Tier 1) | Required | Required | Package deps, plugin `dependencies`, nested servers |
| Install script review (`pre`/`postinstall`, etc.) | Skipped (Tier 1) | Required | Required | Package scripts, `command` source, bundles; `N/A` if none |
| Source code review (behavioral) | Skipped (Tier 1) | Skim | Required | All executable components |
| Repo-borne / host configuration | If applicable | If applicable | If applicable | Addendum Repo-Borne Surfaces |
| Network traffic analysis | Skip | Skip | If flagged | Manual |

## Subject Rubric

Sections mirror `references/criteria.md` §4.1–§4.6. Each notes where 8a,
8b and 8c differ.

### 4.1 Provenance & Identity

Apply the addendum channel table and V2. Identity proves origin, not
safety. **8a:** reference servers are maintained examples, not vendor
products; vendor first-party beats a community wrapper of the same API.
**8b:** rate the marketplace owner and the plugin source separately.
**8c:** skill hubs and scanner badges are weak signals.

### 4.2 Maintenance & Longevity

Last release, issue response, deprecated transport (legacy HTTP+SSE),
archived repo (archived reference servers point to a replacement —
recommend it).

### 4.3 Security Track Record

CVEs per `references/criteria.md` §4.3 with the addendum own-code line;
incidents per §4.6 V4; host advisories for repo-borne subjects.
Directory-scoping and path-validation advisories matter most for fs
servers: the requested version must be at or above the last fix.

### 4.4 Capability & Permissions

Primary axis. Classify every tool or component with the capability table;
apply Shell-Surface Rating; check proportionality to the stated purpose.
**8a:** declared scope vs implementation (e.g. path checks, symlinks).
**8b:** highest component wins; hooks that return permission decisions or
rewrite tool calls are interception. **8c:** `allowed-tools` grants and
file reach.

### 4.5 Behavioral & Model-Context Risk

Applies to all three sub-types. **8a:** tool descriptions and results are
model input (poisoning, shadowing, indirect injection). **8b:** hooks,
agents, output styles and skills. **8c:** the whole body, plus `!`
blocks and persistent hooks. Check the lethal trifecta within the subject
and, when the user's config is known, with their other servers.

### 4.6 Version & Update Integrity

The shared floor plus the addendum plug-in. Every Recommendation names
the update control (exact launch pin, source `sha` / `sha256`, marketplace
`autoUpdate` off) or states that updates cannot be held (remote servers,
`command` sources).

## Subject Verdict Notes

### Toward REJECTED

- Any addendum CRITICAL: unreviewed or remote-fetching shell surface;
  tool poisoning or exfiltration steering; "prerequisite" installer lure;
  config hijack; endpoint or credential redirection; other credentials,
  or any credential handed to an unverified publisher; lethal trifecta
  within one extension
- Impersonation of Anthropic, a reserved marketplace, or a vendor
- Shell-bearing component with no reviewable source
- Remote server over plain `http://` carrying credentials or private data
- §4.6 V4 case (a), a Blocking CVE, or any `SKILL.md` Red Flag

### Toward CONDITIONAL

- Unpinned launcher or source — condition: pin the exact version, SHA or
  digest; keep marketplace auto-update off
- Reviewed shell surface that runs unattended — condition: pin; re-audit
  on any hook, monitor or `bin/` change
- Own-service credential — condition: least-scope key in the host's
  secret store; rotate on removal
- Directory-scoped fs write — condition: narrowest directory; version at
  or above the last fixed advisory
- Self-granted tools or `!` blocks — condition: narrow them, or org
  `allowManagedPermissionRulesOnly` / `disableSkillShellExecution`
- Remote vendor server — condition: record issuer and scopes, pin scopes;
  move off legacy SSE where offered
- Indirect-injection tools — condition: keep them out of sessions that
  also hold private-data and egress tools
- Repo-borne config — condition: approve per server interactively; run
  headless with `--strict-mcp-config` or managed allow/deny lists
- Host below a fixed release for a relevant advisory — condition: upgrade

### Toward APPROVED

- Publisher identity verified (V2) and code reviewed at the tier's depth
- Capabilities Low or Medium and proportional to purpose; no shell
  surface, or reviewed shell that runs only when the user invokes it
- No behavioral indicator in descriptions, bodies or frontmatter
- stdio, or a vendor-operated remote endpoint with least-scope OAuth
- Exact pin and update control in place; §4.6 clean; no open CVE or
  incident
