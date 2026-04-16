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
