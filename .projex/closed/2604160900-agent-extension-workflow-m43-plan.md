# Agent Extension Workflow — M4.3

> **Status:** Planned
> **Created:** 2026-04-16
> **Author:** Claude (Opus 4.6)
> **Source:** [2604070218-install-auditor-subject-typed-redesign-nav.md](2604070218-install-auditor-subject-typed-redesign-nav.md) Phase 4, M4.3
> **Related Projex:**
> - **Roadmap:** [2604070218-install-auditor-subject-typed-redesign-nav.md](2604070218-install-auditor-subject-typed-redesign-nav.md)
> - **Framing eval:** [2604070217-subject-typed-audit-dispatch-eval.md](2604070217-subject-typed-audit-dispatch-eval.md)
> - **Taxonomy spec:** [2604070300-install-auditor-subject-type-taxonomy-def.md](2604070300-install-auditor-subject-type-taxonomy-def.md)
> - **Pattern precedent (M4.2):** [closed/2604151500-cli-binary-workflow-m42-plan.md](closed/2604151500-cli-binary-workflow-m42-plan.md)
> **Worktree:** No

---

## Summary

Create the Type 8 subject-specific workflow at `workflows/agent-extension.md` and its criteria addendum at `references/criteria/agent-extension.md`, then wire Type 8 routing and eval coverage. M4.3 closes the third Phase 4 gap: agent extensions (MCP servers, Claude Code plugins, Claude Code skills) still fall through to `workflows/generic.md`, which knows nothing about capability surface assessment, transport security (stdio vs HTTP vs SSE), prompt/behavioral injection risk, MCP capability negotiation, permission models, or the three distinct sub-rubric profiles (8a/8b/8c) that the taxonomy spec defines.

**Scope:** Type 8 agent-extension audits — workflow file, criteria addendum, dispatcher wiring, eval coverage.
**Estimated Changes:** 4 files (2 new, 2 modified), ~550–750 lines.

---

## Objective

### Problem / Gap / Need

Type 8 (`agent-extension`) routes to `workflows/generic.md`. Current guidance is inadequate:

1. `workflows/generic.md` has no agent-extension-specific checks. No capability surface assessment (what tools/resources does it expose), no transport security evaluation (stdio local vs HTTP remote vs SSE), no prompt injection surface analysis, no MCP capability negotiation review.
2. Triage thresholds (`>100K weekly downloads`) are npm-specific. Agent extensions use MCP registry presence, GitHub stars, Anthropic official status, community adoption signals, and Claude Code marketplace metrics — different metrics entirely.
3. No treatment of prompt/behavioral risk — skills and plugins that inject prompts or modify agent behavior have a unique attack surface (behavioral override, exfiltration via shaped prompts) that generic.md cannot evaluate.
4. No coverage of distribution channels specific to agent extensions: MCP registries (mcp.so, Smithery), GitHub repos, npm packages wrapping MCP servers, Claude Code marketplace/community, shared `.mcp.json` configs, git-cloned skill directories.
5. No guidance on capability scope classification — an MCP server exposing `shell_exec` + filesystem read/write + network access is categorically different from one exposing a read-only weather API, yet generic.md treats both identically.
6. No review path for transport and isolation — stdio transport (local, process-isolated) has a fundamentally different risk profile than HTTP/SSE transport (network-exposed, potentially remote).
7. No sub-rubric differentiation — MCP servers (8a), Claude Code plugins (8b), and Claude Code skills (8c) have distinct risk profiles that require labeled sections where they diverge.

The taxonomy spec (§8) defines: "Code that extends an AI agent's capabilities — adding tools, prompts, hooks, skills, or context — and runs with access to the agent's capability surface."

### Success Criteria

- [ ] `workflows/agent-extension.md` exists and follows Identify / Evidence / Subject Rubric / Subject Verdict Notes template, with labeled sub-rubric sections for 8a/8b/8c
- [ ] `references/criteria/agent-extension.md` exists and defines agent-extension-specific scoring for distribution/discovery channel trust, capability scope classification, transport & isolation assessment, prompt/behavioral risk, and tier thresholds
- [ ] `SKILL.md` dispatch table row 8 routes to `workflows/agent-extension.md`
- [ ] `SKILL.md` Reference Files includes `workflows/agent-extension.md` and `references/criteria/agent-extension.md`
- [ ] `evals/evals.json` gains at least 2 Type 8 cases: one well-known Tier 1 positive path (id 22), one unknown high-risk Tier 3 negative path (id 23)
- [ ] No regressions in eval ids 0–21
- [ ] Sub-rubric labels 8a/8b/8c appear in workflow rubric sections where risk profiles diverge

### Out of Scope

- New helper scripts for MCP manifest parsing or capability enumeration
- Broad rewrites to `references/criteria.md` or `references/registries.md`
- Agent extensions distributed primarily via a registry (e.g., MCP server published as npm package where npm is the innermost boundary) — those route to Type 1 (registry-package) per taxonomy
- IDE plugins that register an MCP server — those route to Type 3 (ide-plugin) per taxonomy; innermost boundary is the marketplace
- Phase 4 M4.4–M4.5 workflows (remote-integration, eval gate)
- Runtime sandboxing implementation or MCP capability enforcement tooling

---

## Steps

### Step 1: Create `references/criteria/agent-extension.md`

**Objective:** Author the agent-extension criteria addendum covering distribution/discovery channel trust, capability scope classification, transport & isolation assessment, prompt/behavioral risk, and tier thresholds calibrated for agent extensions.
**Confidence:** High
**Depends on:** None

**Files:**
- `references/criteria/agent-extension.md` (new)

**Changes:**

Create a new addendum with this structure:

```markdown
# Agent Extension — Criteria Addendum

Per-subject scoring extensions for **Type 8: agent-extension** audits.
Layers on top of `references/criteria.md`. More-specific guidance wins.

Covers: MCP servers (8a), Claude Code plugins (8b), Claude Code skills
(8c), and agent extensions for other harnesses (Cursor, Cline, Continue).
Three labeled sub-rubrics where risk profiles diverge.

## Distribution / Discovery Channel Trust Signals

| Channel | Trust Signal | Verification | Notes |
|---------|-------------|--------------|-------|
| Anthropic official / first-party | Anthropic-maintained; official docs | anthropic.com, docs.anthropic.com | Highest trust: vendor-maintained |
| MCP registry (mcp.so, Smithery) | Registry-listed; community review | Registry listing + metadata | Moderate: registries vary in curation depth |
| Claude Code marketplace / community | Marketplace listing; usage metrics | Marketplace presence | Moderate: depends on review/curation process |
| GitHub repo (established org) | Org-maintained; stars, contributors | GitHub metadata | Moderate: open-source review possible |
| GitHub repo (personal/new) | Individual maintainer; limited history | GitHub metadata | Low-Moderate: limited review surface |
| npm package wrapping MCP server | npm registry trust signals apply | npm metadata + MCP manifest | Moderate: npm trust + MCP-specific checks |
| Shared .mcp.json config | Peer-shared; no registry gate | Config file inspection | Low: no independent verification |
| Git clone from unknown source | No registry; no curation | Manual review only | Lowest: zero independent verification |

### Scoring impact

- Anthropic official = strong positive (vendor-maintained, documented)
- MCP registry with reviews + usage = moderate positive
- Claude Code marketplace listed = moderate positive
- GitHub org repo with stars/CI = moderate positive
- GitHub personal repo, recent = weak positive at best
- npm-wrapped MCP with good npm signals = moderate positive (defer to registry-package for npm layer)
- Shared config / Slack-shared = LOW-MEDIUM flag (no verification gate)
- Unknown git clone = HIGH flag (zero provenance)

## Capability Scope Classification

| Capability | Risk Level | Why |
|-----------|-----------|-----|
| Read-only data (weather, time, static lookups) | Low | No mutation; limited exfiltration surface |
| File-system read | Medium | Can access sensitive files; exfiltration vector |
| File-system write | High | Can modify code, configs, credentials |
| Shell / command execution | Critical | Arbitrary code execution; full system access |
| Network requests (outbound) | High | Data exfiltration; C2 channel potential |
| Database access | High | Data access; mutation risk depends on permissions |
| Prompt/context injection (skills, plugins) | High | Behavioral override; indirect prompt injection |
| Secret/credential access | Critical | Direct credential theft vector |
| Multi-capability (shell + network + fs) | Critical | Combined attack surface; assume worst-case |

### Scoring impact

- Read-only, single-purpose tools = strong positive (minimal attack surface)
- File-system read-only = moderate flag (review what paths are accessible)
- File-system write = HIGH flag unless scoped to specific directories
- Shell execution = CRITICAL flag unless vendor-trusted + well-documented
- Network + file-system combined = CRITICAL flag (exfiltration pipeline)
- Prompt injection surface (8b/8c) = HIGH flag; requires behavioral review

## Transport & Isolation Assessment

| Transport | Isolation | Risk | Notes |
|-----------|-----------|------|-------|
| stdio (local) | Process-isolated; same-machine | Low-Medium | Default MCP transport; limited to local |
| HTTP (localhost) | Process-isolated; localhost-bound | Medium | Network stack exposed but localhost-only |
| HTTP (remote) | Network-exposed; remote server | High | Data leaves machine; server trust required |
| SSE (remote) | Network-exposed; persistent connection | High | Persistent channel; data streaming risk |
| In-process (skills/plugins) | Runs in agent process | Medium-High | No process isolation; direct agent access |

### Scoring impact

- stdio local = neutral to weak positive (standard, expected)
- HTTP localhost = weak flag (unnecessary network exposure for local use)
- HTTP/SSE remote = MEDIUM-HIGH flag (data transit, server trust, TLS required)
- In-process (skills/plugins) = MEDIUM flag (no isolation from agent)

## Prompt / Behavioral Risk (8b and 8c primarily)

| Risk Vector | Severity | Description |
|------------|----------|-------------|
| Prompt injection via skill content | High | Skill markdown can contain instructions that override agent behavior |
| Behavioral override via hooks | High | Plugin hooks can intercept and modify agent actions |
| Settings injection | Medium | Plugin settings can alter agent configuration |
| Context pollution | Medium | Skills that inject large context blocks can crowd out user intent |
| Exfiltration via shaped prompts | High | Behavioral instructions that cause agent to leak sensitive data |
| Slash command hijacking | Medium | Plugin slash commands that shadow built-in or other commands |

### Scoring impact

- No prompt/behavioral surface (pure tool server, 8a) = not applicable
- Minimal behavioral surface (read-only prompts) = weak flag
- Behavioral override capability (hooks, settings injection) = HIGH flag
- Prompt content with exfiltration potential = CRITICAL flag

## Tier Thresholds

### Tier 1 — Quick Audit

ALL of the following must be true:
- Anthropic official OR well-established MCP registry listing with significant usage
- Capability scope: read-only or low-risk tools only (no shell, no fs-write, no network-out)
- Transport: stdio or localhost HTTP
- No prompt/behavioral injection surface (8a only, or 8b/8c with minimal surface)
- Known, reputable publisher/maintainer
- Available >= 6 months OR Anthropic-maintained
- No known security incidents

### Tier 2 — Standard Audit

ANY of the following triggers Tier 2 (but none of the Tier 3 triggers):
- MCP registry or GitHub listing with moderate usage but not Tier 1 trust level
- Capability scope includes file-system read OR limited network access
- Transport includes localhost HTTP
- Some prompt/behavioral surface (8b/8c with documented scope)
- Maintainer is known but not top-tier
- Available < 6 months but > 1 month

### Tier 3 — Deep Audit

ANY of the following triggers Tier 3:
- No registry listing; shared via config, Slack, or unknown git clone
- Capability scope includes shell execution, fs-write, network-out, or credential access
- Transport includes remote HTTP/SSE
- Significant prompt/behavioral injection surface (hooks, settings override, large context injection)
- Unknown or anonymous maintainer
- Available < 1 month or no version history
- Any prior security incident
- Multi-capability with combined attack surface
```

**Rationale:** Agent extensions have a unique risk profile centered on capability surface, transport security, and prompt/behavioral risk that no existing addendum covers. The three sub-rubric profiles (8a MCP server / 8b Claude Code plugin / 8c Claude Code skill) share distribution and capability concerns but diverge on transport isolation and prompt injection surface.

**Verification:** File exists and contains all 5 sections: Distribution/Discovery Channel Trust Signals, Capability Scope Classification, Transport & Isolation Assessment, Prompt/Behavioral Risk, Tier Thresholds. Each section has a table + scoring impact subsection.

**If this fails:** No downstream dependency breaks; Steps 2–4 can proceed with a placeholder reference. However, the workflow's rubric guidance will be incomplete without the addendum.

---

### Step 2: Create `workflows/agent-extension.md`

**Objective:** Author the Type 8 agent-extension workflow following Identify / Evidence Part A / Evidence Part B / Subject Rubric / Subject Verdict Notes template, with labeled sub-rubric sections for 8a/8b/8c where risk profiles diverge.
**Confidence:** High
**Depends on:** Step 1

**Files:**
- `workflows/agent-extension.md` (new)

**Changes:**

Create the workflow file with this structure:

```markdown
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
```

The Identify section must include:

**1. Determine sub-type and distribution channel** — a table mapping install patterns to sub-types and distribution channels:

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

**2. Extract available metadata** — collect from the distribution channel:
- **Extension name** — as listed in registry/marketplace/repo
- **Publisher/maintainer** — organization or individual
- **Sub-type** — 8a (MCP server), 8b (Claude Code plugin), or 8c (Claude Code skill)
- **Distribution channel** — from the table above
- **Capabilities exposed** — tools, resources, prompts (enumerate from manifest/config)
- **Transport** — stdio, HTTP (localhost or remote), SSE, in-process
- **Permission model** — what the extension can access (fs, network, shell, secrets)

**3. Gather required context** — checklist of what must be collected before proceeding:
1. Extension name and version (if available)
2. Sub-type classification (8a/8b/8c)
3. Distribution channel and provenance
4. Full capability manifest (tools, resources, prompts exposed)
5. Transport type and isolation level
6. Permission scope (file-system, network, shell, credentials)

If any of 1–6 are missing, ask before proceeding.

**Evidence — Part A: Tier Triage** — gather distribution and capability data:
- Extension presence on MCP registries, Claude Code marketplace, or GitHub
- Publisher/maintainer identity and reputation
- Capability scope assessment (classify each exposed tool/resource by risk level per addendum)
- Transport security assessment
- Brief search for "[extension name] security OR vulnerability OR malicious" for prior incidents

Apply the agent-extension-specific tier thresholds from `references/criteria/agent-extension.md`:

- **Tier 1 — Quick Audit:** When ALL Tier 1 criteria from the addendum are met: Anthropic official or well-established, read-only/low-risk capabilities, stdio/localhost transport, no prompt injection surface, known publisher, no incidents.
- **Tier 2 — Standard Audit:** When any Tier 2 trigger fires but no Tier 3 trigger.
- **Tier 3 — Deep Audit:** When any Tier 3 trigger fires: shell/fs-write/network capabilities, remote transport, prompt injection surface, unknown publisher, no registry listing.

**Evidence — Part B: Research & Verification** — core research questions (adapt depth to tier):

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

Distribution channel research guidance:
- **MCP registries (mcp.so, Smithery):** Check listing metadata, user reviews, usage counts, last updated
- **GitHub repos:** Stars, contributors, commit frequency, issue tracker, CI/CD, release history
- **npm-wrapped MCP servers:** Apply registry-package trust signals for the npm layer; then MCP-specific checks for capability surface
- **Claude Code marketplace:** Listing status, usage metrics, review process
- **Shared configs / git clones:** No independent verification available; rely on code review + capability assessment

Capability audit procedure:
- Enumerate all exposed tools from manifest/config
- Classify each by risk level per addendum table
- For shell/exec tools: document exact commands accessible
- For file-system tools: document path scope (restricted directory vs full fs)
- For network tools: document endpoints accessible (localhost only vs arbitrary)
- For prompt/behavioral tools (8b/8c): document injection surface

Audit coverage tracking table:

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

**Subject Rubric (§4.1–4.6 agent-extension-specialized):**

§4.1 Capability Surface (primary axis for agent extensions):
- Enumerate all tools/resources/prompts exposed
- Classify each by risk level: Low (read-only data) / Medium (fs-read, limited network) / High (fs-write, broad network, prompt injection) / Critical (shell exec, credential access, multi-capability)
- **8a divergence:** MCP servers expose tools + resources via manifest; capability is declarative and enumerable
- **8b divergence:** Claude Code plugins expose slash commands + hooks + settings; hooks can intercept agent actions
- **8c divergence:** Claude Code skills inject markdown + scripts into agent context; behavioral-shaping risk is primary concern

§4.2 Transport & Isolation:
- Classify transport: stdio / HTTP localhost / HTTP remote / SSE remote / in-process
- Assess isolation level: process-isolated (8a stdio) / network-isolated (8a HTTP localhost) / network-exposed (8a HTTP/SSE remote) / no isolation (8b/8c in-process)
- **8a divergence:** Transport is configurable and varies; stdio is safest, remote HTTP/SSE highest risk
- **8b divergence:** Runs in agent process; no transport isolation; direct host access
- **8c divergence:** Loaded into agent context; no process isolation; shapes agent behavior directly

§4.3 Provenance & Distribution:
- Distribution channel trust (per addendum table)
- Publisher verification depth
- Source code availability and reviewability
- Version history and release cadence

§4.4 Permission Model & Scope:
- What permissions does the extension request/require?
- MCP capability negotiation (8a): what capabilities are advertised?
- Claude Code permission settings (8b): what settings does it inject/modify?
- File-system reach (8c): what files/directories does the skill reference?
- Is the permission scope proportional to stated purpose?

§4.5 Prompt & Behavioral Risk (8b/8c primarily):
- Does it inject prompts into agent context?
- Can it override agent behavior (hooks, settings)?
- Does it have exfiltration potential via shaped prompts?
- Is the behavioral surface documented and auditable?
- **8a:** Typically N/A (tool servers don't shape agent behavior)
- **8b:** HIGH relevance (hooks, settings, slash commands can modify behavior)
- **8c:** HIGHEST relevance (entire skill is behavioral shaping by definition)

§4.6 Maintenance & Ecosystem:
- Last update, commit frequency, issue responsiveness
- Community adoption (registry usage, GitHub stars, marketplace downloads)
- Dependency chain health (for npm-wrapped MCP servers)

**Subject Verdict Notes:**

Toward REJECTED:
- Shell/command execution capability with unknown or untrusted publisher
- Remote HTTP/SSE transport with no TLS or unknown server
- Prompt injection surface with exfiltration potential
- No source code, no registry listing, no provenance trail
- Multi-capability (shell + network + fs) from non-Anthropic source
- Known security incident or community warning

Toward CONDITIONAL:
- File-system write capability — condition: restrict to specific directories
- Network outbound capability — condition: document and monitor endpoints
- Prompt/behavioral surface — condition: review and approve injected content
- Remote transport — condition: verify TLS, server identity, data handling
- Moderate-risk capabilities from known publisher — condition: pin version, monitor updates

Toward APPROVED:
- Anthropic official or well-established community tool
- Read-only / low-risk capabilities proportional to stated purpose
- stdio or localhost transport with process isolation
- No prompt/behavioral injection surface (or minimal, well-documented)
- Source code available and reviewed
- Active maintenance, known publisher, no incidents

**Rationale:** Agent extensions represent a novel and rapidly evolving attack surface that generic.md cannot evaluate. The three sub-types (8a/8b/8c) share distribution and capability concerns but diverge significantly on transport isolation, prompt injection risk, and permission models. The workflow must label these divergences explicitly so the auditor knows which sub-rubric sections to weight for each sub-type.

**Verification:** File exists. `grep "^## " workflows/agent-extension.md` returns: Identify, Evidence — Part A, Evidence — Part B, Subject Rubric, Subject Verdict Notes. `grep "8a\|8b\|8c" workflows/agent-extension.md` returns hits in the rubric sections showing sub-rubric differentiation.

**If this fails:** Type 8 continues routing to `workflows/generic.md`. No regression.

---

### Step 3: Update `SKILL.md`

**Objective:** Wire dispatch table row 8 and add reference file bullets.
**Confidence:** High
**Depends on:** Steps 1–2

**Files:**
- `SKILL.md`

**Changes:**

**3a. Dispatch table row 8:**

```markdown
// Before:
| 8 | agent-extension | `workflows/generic.md` | Fallback — specific workflow lands in Phase 4 (M4.3); 8a/8b/8c resolved at classification |

// After:
| 8 | agent-extension | `workflows/agent-extension.md` | Live — Phase 4 (M4.3); 8a/8b/8c resolved at classification |
```

**3b. Reference Files — workflow bullet (insert after `workflows/cli-binary.md` line):**

```markdown
// Before:
- `workflows/cli-binary.md` — Type 7 cli-binary workflow (Phase 4, M4.2)
- `references/criteria.md` — Shared tier-aware scoring rubric

// After:
- `workflows/cli-binary.md` — Type 7 cli-binary workflow (Phase 4, M4.2)
- `workflows/agent-extension.md` — Type 8 agent-extension workflow (Phase 4, M4.3)
- `references/criteria.md` — Shared tier-aware scoring rubric
```

**3c. Reference Files — addendum bullet (insert after `references/criteria/cli-binary.md` line):**

```markdown
// Before:
- `references/criteria/cli-binary.md` — CLI-binary criteria addendum (distribution channel trust, signature/checksum standards, install-script risk, provenance, tier thresholds)
- `references/licenses.md` — License compatibility matrix

// After:
- `references/criteria/cli-binary.md` — CLI-binary criteria addendum (distribution channel trust, signature/checksum standards, install-script risk, provenance, tier thresholds)
- `references/criteria/agent-extension.md` — Agent-extension criteria addendum (distribution/discovery channel trust, capability scope classification, transport & isolation, prompt/behavioral risk, tier thresholds)
- `references/licenses.md` — License compatibility matrix
```

**Rationale:** Dispatcher routing and reference-file index are the only `SKILL.md` edits needed. All subject logic lives in the new workflow and addendum.

**Verification:** `rg -n "agent-extension" SKILL.md` shows: signal table row 8 (already present), dispatch table row 8 -> live route, workflow reference bullet, addendum reference bullet. Total: 4+ hits with the new additions.

**If this fails:** Revert row and remove bullets; Type 8 continues routing through `workflows/generic.md`.

---

### Step 4: Update `evals/evals.json`

**Objective:** Add Type 8 eval coverage — one positive Tier 1, one negative Tier 3.
**Confidence:** High
**Depends on:** Steps 1–3

**Files:**
- `evals/evals.json`

**Changes:**

Append two entries to the `evals` array (after id 21):

```json
    {
      "id": 22,
      "prompt": "Is it safe to use the Anthropic-maintained MCP filesystem server? I'd configure it in my .mcp.json like: { \"mcpServers\": { \"filesystem\": { \"command\": \"npx\", \"args\": [\"-y\", \"@modelcontextprotocol/server-filesystem\", \"/Users/me/projects\"] } } }",
      "expected_output": "Tier 1 quick audit. Routes to agent-extension workflow, sub-rubric 8a (MCP server). Should recognize @modelcontextprotocol/server-filesystem as an Anthropic-maintained official MCP server, distributed via npm under the @modelcontextprotocol scope. stdio transport (local, process-isolated). Capabilities: file-system read/write scoped to the specified directory argument. Should note that while fs-write is generally a High-risk capability, the directory scoping plus Anthropic-official provenance mitigates significantly. Verdict should be APPROVED with a note about directory scope.",
      "files": [],
      "assertions": [
        {"text": "Subject type is agent-extension", "type": "contains_concept"},
        {"text": "Sub-rubric is 8a or MCP server", "type": "contains_concept"},
        {"text": "Report identifies Anthropic or @modelcontextprotocol as the official publisher", "type": "contains_concept"},
        {"text": "Report discusses capability surface (file-system access)", "type": "contains_concept"},
        {"text": "Report discusses transport (stdio) and isolation", "type": "contains_concept"},
        {"text": "Report notes directory scoping as a mitigation", "type": "contains_concept"},
        {"text": "Verdict is APPROVED", "type": "exact_match"},
        {"text": "Audit confidence", "type": "contains_concept"}
      ]
    },
    {
      "id": 23,
      "prompt": "Someone on Discord shared an MCP server config for a 'universal AI assistant' tool: { \"mcpServers\": { \"universal-ai\": { \"command\": \"npx\", \"args\": [\"-y\", \"universal-ai-mcp-server\"], \"env\": { \"OPENAI_API_KEY\": \"...\", \"ANTHROPIC_API_KEY\": \"...\" } } } } — the GitHub repo (github.com/randomuser42/universal-ai-mcp) has 3 stars and was created last week. Should I add this?",
      "expected_output": "Tier 3 deep audit. Routes to agent-extension workflow, sub-rubric 8a (MCP server). Should flag multiple critical risks: unknown publisher (randomuser42), brand-new repo (created last week, 3 stars), Discord-shared provenance (no registry gate), requires API keys in env (credential exposure — CRITICAL capability), unknown capability surface (cannot verify what tools are exposed without inspection), npx execution of unvetted package. Should flag the API key requirement as a critical credential-theft vector. Verdict must be REJECTED.",
      "files": [],
      "assertions": [
        {"text": "Subject type is agent-extension", "type": "contains_concept"},
        {"text": "Sub-rubric is 8a or MCP server", "type": "contains_concept"},
        {"text": "Report flags unknown or unverified publisher", "type": "contains_concept"},
        {"text": "Report flags the new/low-star GitHub repo", "type": "contains_concept"},
        {"text": "Report flags API key or credential exposure as critical risk", "type": "contains_concept"},
        {"text": "Report flags Discord or social-media shared provenance", "type": "contains_concept"},
        {"text": "Verdict is REJECTED", "type": "exact_match"},
        {"text": "## Audit Coverage", "type": "contains_string"},
        {"text": "Audit confidence", "type": "contains_concept"}
      ]
    }
```

**Rationale:** Two cases exercise the Type 8 workflow's boundary conditions: id 22 tests a well-known Anthropic-official MCP server with scoped fs capabilities (Tier 1 positive path), and id 23 tests an unknown MCP server with credential-access risk shared via Discord (Tier 3 negative path). Both target sub-rubric 8a since MCP servers are the most common Type 8 subject. Future milestones can add 8b/8c eval cases.

**Verification:**
- `node -e "const d=JSON.parse(require('fs').readFileSync('evals/evals.json','utf8')); console.log(d.evals.length);"` → 24
- `node -e "const d=JSON.parse(require('fs').readFileSync('evals/evals.json','utf8')); console.log(d.evals[22].id, d.evals[23].id);"` → 22 23
- JSON parses without errors
- ids 0–21 are unchanged

**If this fails:** Remove the two new entries; eval coverage remains at 22. Type 8 workflow still functions but lacks eval validation.

---

## Verification Plan

### Automated Checks

- [ ] `workflows/agent-extension.md` exists and is non-empty
- [ ] `references/criteria/agent-extension.md` exists and is non-empty
- [ ] `evals/evals.json` is valid JSON with 24 entries
- [ ] `grep agent-extension SKILL.md` returns 4+ hits (signal, dispatch, workflow ref, addendum ref)

### Manual Verification

- [ ] Workflow follows Identify / Evidence Part A / Evidence Part B / Subject Rubric / Subject Verdict Notes structure
- [ ] Workflow contains labeled sub-rubric sections for 8a/8b/8c where risk profiles diverge
- [ ] Criteria addendum covers all 5 sections (distribution/discovery channel trust, capability scope, transport & isolation, prompt/behavioral risk, tier thresholds)
- [ ] Dispatch table row 8 routes to `workflows/agent-extension.md` with "Live — Phase 4 (M4.3)"
- [ ] Eval id 22 (Anthropic MCP filesystem server) tests the positive Tier 1 path for 8a
- [ ] Eval id 23 (unknown Discord-shared MCP server with credential access) tests the negative Tier 3 path for 8a
- [ ] ids 0–21 are unchanged in `evals/evals.json`

### Acceptance Criteria Validation

| Criterion | How to Verify | Expected Result |
|-----------|---------------|-----------------|
| Workflow exists with template | `grep "^## " workflows/agent-extension.md` | Identify, Evidence — Part A, Evidence — Part B, Subject Rubric, Subject Verdict Notes |
| Sub-rubric labels present | `grep "8a\|8b\|8c" workflows/agent-extension.md` | Multiple hits in rubric sections |
| Criteria addendum exists | File read; section scan | 5 sections present with tables + scoring impact |
| Dispatch row 8 | `grep "agent-extension.*agent-extension.md" SKILL.md` | Row 8 routes to `workflows/agent-extension.md` |
| Reference Files bullets | `grep "agent-extension" SKILL.md` | 4+ total hits |
| Eval coverage | JSON parse + id count | 24 total entries, ids 0–23 |
| Eval id 22 (positive) | Read eval prompt + assertions | Anthropic MCP filesystem server, APPROVED expected |
| Eval id 23 (negative) | Read eval prompt + assertions | Unknown MCP server, REJECTED expected |
| No regressions | Diff ids 0–21 against pre-change | Zero diff |

---

## Rollback Plan

Per-step rollback is noted in each step. If the overall implementation must be abandoned:

1. Delete `workflows/agent-extension.md`
2. Delete `references/criteria/agent-extension.md`
3. Revert `SKILL.md` edits (dispatch table row 8, reference file bullets)
4. Remove eval ids 22 and 23 from `evals/evals.json`
5. All changes are in 4 files; `git checkout -- <files>` restores clean state

---

## Risk Assessment

### Risks

- **Sub-rubric complexity:** Type 8 is the first type with three labeled sub-rubrics (8a/8b/8c) inside one workflow file. This adds structural complexity compared to prior single-profile types. Mitigation: use clear labeled sections with explicit "divergence" callouts at each rubric point; follow the taxonomy spec's guidance that 8a/8b/8c share one workflow with labeled sections.
- **Rapidly evolving ecosystem:** MCP and Claude Code plugins/skills are actively evolving; capability surfaces, permission models, and distribution channels may change. Mitigation: v1 focuses on stable, structural risk factors (capability scope, transport, provenance) rather than implementation details that may shift. Future revisions can update specific channel trust signals.
- **Prompt/behavioral risk novelty:** Evaluating prompt injection and behavioral override risk in skills/plugins is a novel audit dimension with no established methodology. Mitigation: frame as surface-area assessment (what can be injected, what hooks are available) rather than trying to detect specific attacks; flag the surface and let the auditor assess.
- **Capability enumeration depth:** Fully enumerating what an MCP server can do requires reading its manifest or source code, which may not always be available. Mitigation: treat unenumerable capabilities as HIGH risk by default; the audit should require manifest/source inspection for Tier 2+ rather than assuming the stated description is complete.
- **Eval case coverage:** Both eval cases target sub-rubric 8a (MCP servers). 8b (plugins) and 8c (skills) lack dedicated eval cases. Mitigation: 8a is the most common sub-type and exercises the core workflow; 8b/8c eval cases can be added in a future eval-expansion milestone without blocking M4.3 closure.

### Open Questions

- **MCP registry curation depth:** mcp.so and Smithery have different curation models that may evolve. The addendum treats them as "moderate" trust; this may need revisiting as registries mature.
- **Claude Code marketplace maturity:** The marketplace review process may not be fully established. Trust signals for 8b may need updating as the marketplace matures.
- **Future sub-type separation:** The taxonomy spec notes that 8a/8b/8c may eventually warrant separate workflow files if their risk profiles diverge further. M4.3 authors them as labeled sub-rubrics per the current taxonomy decision; separation is a future consideration.
