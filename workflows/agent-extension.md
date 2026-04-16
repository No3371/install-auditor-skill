<!--
This workflow replaces workflows/generic.md for Type 8 subjects. After
producing findings here, return to SKILL.md Step N for the shared verdict
tree and report shape. The Audit Coverage table and audit-confidence
assertion are owned by the dispatcher — do not duplicate them here.

Phase 4 / M4.3 — eighth subject-specific workflow (third Phase 4).
-->

# Agent Extension Workflow (Type 8)

This workflow handles **Type 8: agent-extension** subjects — code that
extends an AI agent's capabilities by adding tools, prompts, hooks,
skills, or context, running with access to the agent's capability
surface. Covers MCP servers (8a), Claude Code plugins (8b), Claude Code
skills (8c), and agent extensions for other harnesses.

After completing all sections below, return to `SKILL.md` Step N for the
shared verdict tree and audit-coverage report shape.

Sections follow the standard workflow template: **Identify / Evidence /
Subject Rubric / Subject Verdict Notes**.

Use `references/criteria/agent-extension.md` for agent-extension-specific
tiering and scoring. When it conflicts with the shared rubric, the more
specific agent-extension guidance wins.

## Identify

### 1. Determine sub-type and distribution channel

| Install Pattern / Signal | Sub-type | Distribution Channel |
|--------------------------|----------|---------------------|
| `.mcp.json` config with stdio/HTTP transport | 8a · MCP server | Config-referenced |
| `npx @modelcontextprotocol/server-*` | 8a · MCP server | npm (MCP official) |
| `mcp.so/*` or `smithery.ai/*` listing | 8a · MCP server | MCP registry |
| `github.com/<org>/<repo>` with MCP manifest | 8a · MCP server | GitHub repo |
| Claude Code plugin bundle (slash commands, hooks, settings) | 8b · Claude Code plugin | Claude Code marketplace / manual |
| `claude-code/plugins/*` directory | 8b · Claude Code plugin | Local / shared |
| `.claude/skills/*` directory with `SKILL.md` | 8c · Claude Code skill | Local / shared / git clone |
| Skill referenced in Claude Code settings | 8c · Claude Code skill | Settings-referenced |
| Agent extension for Cursor / Cline / Continue | 8a variant | Host-specific channel |

### 2. Extract available metadata

Collect from the distribution channel:

- **Extension name** — as listed in registry/marketplace/repo
- **Publisher/maintainer** — organization or individual
- **Sub-type** — 8a (MCP server), 8b (Claude Code plugin), or 8c (Claude Code skill)
- **Distribution channel** — from the table above
- **Capabilities exposed** — tools, resources, prompts (enumerate from manifest/config)
- **Transport** — stdio, HTTP (localhost or remote), SSE, in-process
- **Permission model** — what the extension can access (fs, network, shell, secrets)

### 3. Gather required context

Checklist of what must be collected before proceeding:

1. Extension name and version (if available)
2. Sub-type classification (8a/8b/8c)
3. Distribution channel and provenance
4. Full capability manifest (tools, resources, prompts exposed)
5. Transport type and isolation level
6. Permission scope (file-system, network, shell, credentials)

If any of 1–6 are missing, ask before proceeding.

## Evidence — Part A

**Tier Triage** — gather distribution and capability data:

- Extension presence on MCP registries, Claude Code marketplace, or GitHub
- Publisher/maintainer identity and reputation
- Capability scope assessment (classify each exposed tool/resource by risk level per addendum)
- Transport security assessment
- Brief search for "[extension name] security OR vulnerability OR malicious" for prior incidents

Apply the agent-extension-specific tier thresholds from `references/criteria/agent-extension.md`:

- **Tier 1 — Quick Audit:** When ALL Tier 1 criteria from the addendum are met: Anthropic official or well-established, read-only/low-risk capabilities, stdio/localhost transport, no prompt injection surface, known publisher, no incidents.
- **Tier 2 — Standard Audit:** When any Tier 2 trigger fires but no Tier 3 trigger.
- **Tier 3 — Deep Audit:** When any Tier 3 trigger fires: shell/fs-write/network capabilities, remote transport, prompt injection surface, unknown publisher, no registry listing.

## Evidence — Part B

**Core Research Questions** — adapt depth to tier:

1. **Provenance:** Where was this extension acquired? Official registry, community share, git clone, config snippet?
2. **Publisher identity:** Who maintains it? Anthropic, known org, community member, anonymous?
3. **Capability inventory:** What tools/resources/prompts does it expose? Enumerate each.
4. **Capability risk:** For each capability, what is the risk classification per the addendum?
5. **Transport security:** What transport is used? Is data leaving the local machine?
6. **Permission scope:** What can this extension access? File system, network, shell, secrets?
7. **Prompt/behavioral surface (8b/8c):** Does it inject prompts, modify agent behavior, register hooks?
8. **Code review (Tier 2+):** Is source code available? Any obvious red flags in implementation?
9. **Incident history:** Any reported security issues, CVEs, or community warnings?
10. **Update mechanism:** How are updates delivered? Auto-update, manual, git pull?

**Distribution channel research guidance:**

- **MCP registries (mcp.so, Smithery):** Check listing metadata, user reviews, usage counts, last updated
- **GitHub repos:** Stars, contributors, commit frequency, issue tracker, CI/CD, release history
- **npm-wrapped MCP servers:** Apply registry-package trust signals for the npm layer; then MCP-specific checks for capability surface
- **Claude Code marketplace:** Listing status, usage metrics, review process
- **Shared configs / git clones:** No independent verification available; rely on code review + capability assessment

**Capability audit procedure:**

- Enumerate all exposed tools from manifest/config
- Classify each by risk level per addendum table
- For shell/exec tools: document exact commands accessible
- For file-system tools: document path scope (restricted directory vs full fs)
- For network tools: document endpoints accessible (localhost only vs arbitrary)
- For prompt/behavioral tools (8b/8c): document injection surface

**Audit coverage tracking table:**

| Check | Tier 1 | Tier 2 | Tier 3 | Source |
|-------|--------|--------|--------|--------|
| Distribution channel verification | Required | Required | Required | Registry/marketplace/repo |
| Publisher/maintainer identity | Required | Required | Required | Web search |
| Capability inventory | Required | Required | Required | Manifest/config/source |
| Capability risk classification | Required | Required | Required | Addendum table |
| Transport assessment | Required | Required | Required | Config/manifest |
| Permission scope review | Skim | Required | Required | Config/source |
| Prompt/behavioral surface (8b/8c) | Skim | Required | Required | Source review |
| Code review | Skip | Skim | Required | Source code |
| Incident search | Required | Required | Required | Web search |
| Dependency audit | Skip | Skim | Required | package.json / deps |
| Update mechanism review | Skip | Skim | Required | Docs/source |
| Network traffic analysis | Skip | Skip | If flagged | Manual |

## Subject Rubric

§4.1–§4.6 agent-extension-specialized sections follow. Each section notes
where 8a/8b/8c risk profiles diverge.

### §4.1 Capability Surface

Primary axis for agent extensions.

- Enumerate all tools/resources/prompts exposed
- Classify each by risk level: Low (read-only data) / Medium (fs-read, limited network) / High (fs-write, broad network, prompt injection) / Critical (shell exec, credential access, multi-capability)

**8a divergence:** MCP servers expose tools + resources via manifest; capability is declarative and enumerable. Start by reading the manifest — it defines the full tool list. Unknown or undocumented tools are a HIGH flag.

**8b divergence:** Claude Code plugins expose slash commands + hooks + settings; hooks can intercept agent actions before and after execution. Enumerate all registered hooks and their trigger conditions.

**8c divergence:** Claude Code skills inject markdown + scripts into agent context; behavioral-shaping risk is primary concern. The SKILL.md itself is the capability surface — read it fully before classifying risk.

### §4.2 Transport & Isolation

- Classify transport: stdio / HTTP localhost / HTTP remote / SSE remote / in-process
- Assess isolation level: process-isolated (8a stdio) / network-isolated (8a HTTP localhost) / network-exposed (8a HTTP/SSE remote) / no isolation (8b/8c in-process)

**8a divergence:** Transport is configurable and varies; stdio is safest, remote HTTP/SSE highest risk. Check the `.mcp.json` or server launch config for the actual transport. Mismatch between stated "local tool" and remote HTTP transport is a HIGH flag.

**8b divergence:** Runs in agent process; no transport isolation; direct host access. The plugin can read agent state, intercept calls, and modify outputs without network exposure being the threat model.

**8c divergence:** Loaded into agent context; no process isolation; shapes agent behavior directly. Risk is behavioral rather than network-based. Evaluate context injection surface rather than transport.

### §4.3 Provenance & Distribution

- Distribution channel trust (per addendum table)
- Publisher verification depth
- Source code availability and reviewability
- Version history and release cadence

Apply addendum Distribution/Discovery Channel Trust Signals table. Anthropic-official is the highest trust anchor. Anonymous or Discord-shared with no registry listing is the lowest.

### §4.4 Permission Model & Scope

- What permissions does the extension request/require?
- **8a:** MCP capability negotiation — what capabilities are advertised in the manifest? Does declared scope match observed implementation?
- **8b:** Claude Code permission settings — what settings does it inject or modify? Does it request broader agent permissions than its stated function requires?
- **8c:** File-system reach — what files/directories does the skill reference? Does the skill SYSTEM_PROMPT or scripts access paths beyond its working directory?
- Is the permission scope proportional to stated purpose?

### §4.5 Prompt & Behavioral Risk

Primarily relevant for 8b and 8c; typically N/A for pure tool servers (8a).

- Does it inject prompts into agent context?
- Can it override agent behavior (hooks, settings)?
- Does it have exfiltration potential via shaped prompts?
- Is the behavioral surface documented and auditable?

**8a:** Typically N/A — tool servers respond to tool calls but do not shape agent behavior proactively. Flag if the server's tool responses contain embedded instructions.

**8b:** HIGH relevance — hooks, settings, and slash commands can modify agent behavior at interception points. Enumerate all hooks and their declared behaviors. Behavioral override without user visibility = HIGH flag.

**8c:** HIGHEST relevance — the entire skill is behavioral shaping by definition. The SKILL.md content, SYSTEM_PROMPT files, and any scripts are the attack surface. Review for: prompt injection instructions, exfiltration triggers, behavioral overrides that persist beyond the skill's stated scope.

### §4.6 Maintenance & Ecosystem

- Last update, commit frequency, issue responsiveness
- Community adoption (registry usage, GitHub stars, marketplace downloads)
- Dependency chain health (for npm-wrapped MCP servers)

For npm-wrapped MCP servers, apply registry-package dependency audit signals for the npm layer in addition to the MCP-specific checks above.

## Subject Verdict Notes

### Toward REJECTED

- Shell/command execution capability with unknown or untrusted publisher
- Remote HTTP/SSE transport with no TLS or unknown server
- Prompt injection surface with exfiltration potential
- No source code, no registry listing, no provenance trail
- Multi-capability (shell + network + fs) from non-Anthropic source
- Known security incident or community warning
- API key or credential access with no clear justification

### Toward CONDITIONAL

- File-system write capability — condition: restrict to specific directories
- Network outbound capability — condition: document and monitor endpoints
- Prompt/behavioral surface — condition: review and approve injected content
- Remote transport — condition: verify TLS, server identity, data handling
- Moderate-risk capabilities from known publisher — condition: pin version, monitor updates

### Toward APPROVED

- Anthropic official or well-established community tool
- Read-only / low-risk capabilities proportional to stated purpose
- stdio or localhost transport with process isolation
- No prompt/behavioral injection surface (or minimal, well-documented)
- Source code available and reviewed
- Active maintenance, known publisher, no incidents
