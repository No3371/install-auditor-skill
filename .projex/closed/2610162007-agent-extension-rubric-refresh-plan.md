# Agent-Extension Rubric Refresh (8a MCP / 8b Plugin / 8c Skill)

> **Status:** Complete
> **Completed:** 2026-10-16
> **Walkthrough:** 2610162007-agent-extension-rubric-refresh-walkthrough.md
> **Log:** 2610162007-agent-extension-rubric-refresh-log.md
> **Author:** Claude (Opus)
> **Parent:** 2610161927-agent-extension-stewardship-review-eval.md
> **Source:** 2610161927-agent-extension-stewardship-review-eval.md (P1: F1–F7, F11, F12, F14; Open Questions 1, 3, 4, 6) on top of 2610161941-shared-version-integrity-floor-plan.md (§4.6 contract, closed — landed as `20843cc`)
> **Related Projex:** 2610161941-shared-version-integrity-floor-plan.md | 2610161941-shared-version-integrity-floor-walkthrough.md | 2604160900-agent-extension-workflow-m43-plan.md | 2604170511-measure-read-cost-f7-m53-findings.md | 2610162004-generic-fallback-and-classifier-refresh-plan.md (sibling; owns classifier Type-8 rows, F13; routes remote MCP connectors → 8a and `/plugin install` with any source → 8b) | 2610162007-remote-integration-rubric-refresh-plan.md (sibling; defines remote-integration addendum §1/§5/§6 this plan cites) | 2604070218-install-auditor-subject-typed-redesign-nav.md
> **Worktree:** Yes

---

## Summary

Rewrites the Type 8 rubric pair against primary sources (Claude Code plugin, marketplace, plugin-loading, skills, hooks and MCP docs; MCP spec changelog 2026-07-28; `modelcontextprotocol/servers` README and advisories; MCP Registry README; Anthropic AAIF announcement — all fetched 2026-10-16). Fixes the three stale models: 8a as a static manifest with SSE as a peer transport, 8b as "commands + hooks + settings, in-process", 8c as behavioral-only. Adds threat classes (tool poisoning, shadowing, prerequisite lures, config hijack, trifecta), repo-borne surfaces, disjoint tier triggers, the canonical coverage rows, and the addendum's `## Version & Update Integrity (§4.6)` plug-in.

**Scope:** `references/criteria/agent-extension.md` + `workflows/agent-extension.md` only — two full-file replacements.
**Estimated Changes:** 2 files. Addendum 6,932 → 15,098 B; workflow 12,907 → 16,586 B (combined +11.8 KB; below the registry-package pair at 40.1 KB and container-image at 36.8 KB).

---

## Objective

### Problem / Gap / Need

| Finding | Gap (current text) | Fix (where) |
|---|---|---|
| F4 | 8a "declarative and enumerable … read the manifest"; SSE peer transport; remote check = "TLS, server identity" | Runtime tool enumeration from source, `list_changed` note; transport table with Streamable HTTP, legacy SSE flag, loopback bind/`Origin`; remote auth modes; remote 8a with no local code accepted; OAuth grant rated by citing remote-integration addendum §1/§5/§6 (sibling hand-offs) (addendum Transport & Auth; workflow Identify note, 8a steps 2, 5) |
| F5 | 8a behavioral "Typically N/A" | Behavioral table for all sub-types: poisoning, exfil steering, prerequisite lure, config hijack, endpoint redirection, shadowing, persistence, indirect injection, trifecta |
| F1 | 8b = "slash commands + hooks + settings", "Runs in agent process" | 8b = container; full component inventory; hook handler types; shell-surface rating; nested 8a/8c sub-audits; `dependencies` |
| F2 | "Claude Code marketplace … usage metrics" | Marketplace owner + reserved names; source types + pin strength; `command` source; auto-update defaults |
| F3 | 8c "SYSTEM_PROMPT", behavioral-only, "In-process Medium" | Frontmatter audit (`allowed-tools` not trust-gated, `hooks`, `context: fork`), `!` shell injection, prerequisite lures, shadowing; Agent Skills format, any host |
| F6 | "Anthropic official — anthropic.com, docs.anthropic.com" top anchor; registries = mcp.so/Smithery | Channel table: Anthropic-operated marketplace, vendor first-party, MCP reference server (steering group, "not production-ready"), official MCP Registry (identity only), aggregators, third-party hosts, skill hubs, MCPB |
| F7 | No repo-borne surface | Addendum Repo-Borne Surfaces (headless auto-load, auto-approve keys, host advisories, controls) + workflow sub-section |
| F11 | localhost HTTP both Tier 1-allowed and Tier 2 trigger; fs-write Tier 3 vs eval 22 Tier 1 | Disjoint tiers: Tier 1 ALL / Tier 3 ANY / Tier 2 = rest; directory-scoped fs write = Tier 2 |
| F12 | Coverage table lacks canonical CVE / typosquat / license / version-integrity rows | Table carries all 12 canonical rows (exact labels) + 6 subject rows |
| F14 | `docs.anthropic.com`, `claude-code/plugins/*` | Removed from the two files (classifier copy → sibling) |
| Floor | No §4.6 plug-in; workflow "§4.6 Maintenance & Ecosystem" collides with shared §4.6 | Addendum `## Version & Update Integrity (§4.6)` V1–V5 + §4.3 own-code line; workflow rubric renumbered to mirror `criteria.md` §4.1–§4.6 |

### Success Criteria

- [ ] Both files replaced with the exact content in Steps 1–2 (`diff` against the plan blocks is empty).
- [ ] Addendum has exactly one `## Version & Update Integrity (§4.6)` heading, bullets `**V1**`…`**V5**` once each, and one `**§4.3 own-code line**` bullet.
- [ ] Workflow coverage table contains every row label from `references/criteria.md` "Rows by tier" verbatim (12) — consistency script.
- [ ] Every addendum section the workflow names exists as a heading (`Tier Thresholds`, `Shell-Surface Rating`, `Repo-Borne Surfaces`, `Version & Update Integrity (§4.6)`, `Transport & Auth (8a)`, `Behavioral & Model-Context Risk`), and `references/criteria/remote-integration.md` has `## §1 — Scope & Permission Assessment`, `## §5 — Terms, Data Sharing & AI Use`, `## §6 — Token Custody & Consent Path`.
- [ ] Stale strings absent from both files (case-insensitive): `SYSTEM_PROMPT` | `SSE (remote)` | `HTTP/SSE` | `claude-code/plugins` | `docs.anthropic.com` | `In-process (skills/plugins)` | `Typically N/A` | `Listing status, usage metrics` | `Anthropic official / first-party` | `§4.6 Maintenance`.
- [ ] Every `§4.6 V<n>` reference names V1–V5 only; no `### §4.` headings remain in the workflow.
- [ ] Sizes: addendum ≤ 15,500 B; workflow ≤ 17,000 B.
- [ ] `python3 evals/run_evals.py validate` passes; `python3 -m unittest discover -s evals -p "test_*.py"` passes with the Preflight test count.
- [ ] Paper traces T1–T10 (Verification Plan) give the stated tier + verdict, citing the rule per hop.
- [ ] `git diff --stat <base>..HEAD` lists only the 2 files plus this plan's projex log/plan files; `SKILL.md`, `references/classifier.md`, `references/criteria.md`, `evals/` untouched.

### Out of Scope

- `references/classifier.md` Type-8 rows, `SKILL.md` Step 0 signal/sub-rubric labels (F13; remote-MCP routing) → sibling 2610162004-generic-fallback-and-classifier-refresh-plan.md. Requirements in Notes → Hand-off.
- `workflows/remote-integration.md` / its addendum (remote-MCP OAuth grant posture if routed there) → 2610162007-remote-integration-rubric-refresh-plan.md.
- `evals/evals.json` (F8–F10: evals 22, 31, new 8b/8c/remote/poisoning/repo-borne cases) → eval-refresh plan; see Hand-off. No live `run_evals.py run` (human: one paid run after all refreshes).
- `STEWARDSHIP.md` inventory dates, nav log (orchestrator, checklist steps 7–8).
- Splitting the addendum per sub-type (review Open Question 1) — decided against; see Notes → Decisions.
- Harness-specific fixed versions for Claude Code CVEs (sources disagree) — rubric names the check, not version numbers.

---

## Context

### Current State

- `workflows/agent-extension.md` (12,907 B, 228 lines): Identify (sub-type table with `claude-code/plugins/*`, "MCP manifest"), Evidence A/B, coverage table (12 rows, no CVE/typosquat/license/version-integrity), Subject Rubric `§4.1`–`§4.6` (its `§4.6 Maintenance & Ecosystem` now collides with `criteria.md` §4.6), Verdict Notes. Only edit since creation: `5c44b79` (comment strip).
- `references/criteria/agent-extension.md` (6,932 B, 125 lines): channel table (Anthropic official top; mcp.so/Smithery; "usage metrics"), capability table, transport table (SSE peer, "In-process"), prompt/behavioral table (8a N/A), overlapping tier lists.
- Shared floor landed on base `claude/youthful-dijkstra-5ov1kt` at `20843cc`: `references/criteria.md` (21,455 B) §4.6 V1–V5 with `**Addendum:**` lines, `Version integrity (§4.6)` canonical row, "Workflow coverage tables add subject rows … never drop a Required row" contract, §4.3 Blocking-CVE table + `**Addendum:**` own-code line; `SKILL.md` (15,484 B) Precedence floor, Blocking CVE term, Red Flag "Confirmed supply chain compromise".
- Eval cases on this workflow: 22 (fs reference server, exact APPROVED), 23 (Discord-shared, exact REJECTED), 31 (Brave, `[APPROVED, CONDITIONAL]`); 40 routes to registry-package. `validate` reads only `evals.json` + `SNAPSHOT_DIRS` paths; no harness code parses these two files.

### Key Files

| File | Role | Change Summary |
|---|---|---|
| `references/criteria/agent-extension.md` | Type 8 scoring addendum | Full replacement: channels, capability + shell rating, transport/auth, behavioral, repo-borne, §4.6 plug-in, disjoint tiers |
| `workflows/agent-extension.md` | Type 8 workflow | Full replacement: Identify signals, per-sub-type evidence procedures, canonical coverage table, rubric 4.1–4.6, verdict notes |

### Primary-Source Facts Codified (verified 2026-10-16)

| Fact | Source |
|---|---|
| Plugin components: skills, commands, agents, hooks, `.mcp.json`/`mcpServers` (`.mcpb`/`.dxt` paths **and https URLs**, downloaded), `.lsp.json`, monitors ("Shell command … persistent background process"), `bin/` ("on the Bash tool's `PATH`"), output styles, workflows, themes, `settings.json` (only `agent`, `subagentStatusLine`), `userConfig` (`sensitive` → secure storage), `dependencies`, `channels`; manifest optional; reserved-name check is validator-only — "Claude Code still installs and loads a plugin whose name they refuse" | code.claude.com/docs/en/plugins-reference |
| Plugin sources: relative, `github`/`url`/`git-subdir` (`ref`, `sha`), `npm` (install scripts never run), `archive` (`sha256`), `command` (runs on install/update and once per session); reserved marketplace names valid only from `github.com/anthropics/`; impersonating marketplace names refused; `strict` entry adds components; policy keys `strictKnownMarketplaces`, `blockedMarketplaces`, `disableCommandPluginSources` | code.claude.com/docs/en/plugins/marketplace-reference |
| Version = manifest `version` > entry `version` > commit SHA / sha256; auto-update default on for `claude-plugins-official` and claude.ai-added marketplaces, off for every other (incl. `knowledge-work-plugins`, `first-party-plugins`); dependency plugins start enabled; project-scope plugins load only after workspace trust (their MCPB servers and monitors are skipped); delisted plugins uninstalled → Flagged | code.claude.com/docs/en/plugins/loading |
| Hook handler types `command`, `http`, `mcp_tool`, `prompt`, `agent`; `PreToolUse` can deny and rewrite `updatedInput`; `PostToolUse` `updatedToolOutput`; `additionalContext` injects into context | code.claude.com/docs/en/hooks |
| Skills: `allowed-tools` — "Workspace trust doesn't gate this field … even in a `-p` run in a folder you've never trusted"; `` !`cmd` `` runs before Claude sees the skill, "never prompt[s] … checks each one against your permission rules"; frontmatter `hooks` active rest of session; `context: fork` background subagent; same-name skill replaces bundled/built-in command; controls `disableSkillShellExecution`, `allowManagedPermissionRulesOnly`, `Skill(name *)`; follows the Agent Skills open standard | code.claude.com/docs/en/skills |
| MCP in Claude Code: SSE "deprecated"; WebSocket supported; project `.mcp.json` servers prompt interactively but load without asking in `-p`, Agent SDK, cloud; project-committed `enableAllProjectMcpServers`/`enabledMcpjsonServers` ignored in untrusted folders; `managedMcpServers`, `allowedMcpServers`, `deniedMcpServers`, `managed-mcp.json`; `headersHelper` = "arbitrary shell command"; `oauth.scopes`; `list_changed` refreshes tools | code.claude.com/docs/en/mcp |
| MCP 2026-07-28 (current, released 2026-07-28): HTTP+SSE deprecated; sessions/`Mcp-Session-Id` removed (stateless); DCR deprecated for Client ID Metadata Documents; clients MUST validate `iss`; Roots/Sampling/Logging deprecated | spec repo changelog.mdx; MCP blog |
| Streamable HTTP: servers MUST validate `Origin`, SHOULD bind `127.0.0.1` (2025-11-25 transports; 2026-07-28 page not fetchable at that path) | spec repo 2025-11-25 transports.mdx |
| Reference servers: "reference implementations … educational examples … not as production-ready solutions", "maintained by the MCP steering group"; current set Everything, Fetch, Filesystem, Git, Memory, Sequential Thinking, Time; Brave archived → `@brave/brave-search-mcp-server` | servers README |
| Filesystem server GHSA-q66q-fx2p-7w4m / CVE-2025-53109 (symlink; High 8.4 v4) + GHSA-hc55-p739-j48w (prefix collision), Jul 2025; fixed release listed inconsistently (0.6.3 vs 0.6.4; 2025.7.01) → rubric says "at or above the last fixed advisory", no number | GitHub advisories, `modelcontextprotocol/servers` |
| MCP Registry: "launched in preview"; namespace ownership validated via GitHub OAuth/OIDC, DNS, HTTP | `modelcontextprotocol/registry` README |
| MCP donated to AAIF (Linux Foundation directed fund), 2025-12-09; governance unchanged | anthropic.com announcement |
| ClawHavoc: Koi Security, Feb 2026, 341 of 2,857 ClawHub skills malicious, fake "Prerequisites" installing AMOS; Antiy counts ≥ 1,184 historically | The Hacker News; Antiy |
| Claude Code advisories include GHSA-pq7j-f95f-qfcv (plugin commit-SHA pin bypass, < 2.1.179) and CVE-2025-59536 (pre-trust execution; CVE record: < 1.0.111) | github.com/anthropics/claude-code/security/advisories; CVE record |

### Dependencies

- **Requires:** base at or after `20843cc` (§4.6 floor). Preflight verifies.
- **Requires (cross-reference):** 2610162007-remote-integration-rubric-refresh-plan.md closed on base, so `references/criteria/remote-integration.md` carries §1 Scope & Permission Assessment, §5 Terms, Data Sharing & AI Use, §6 Token Custody & Consent Path (cited by addendum Transport & Auth and workflow 8a step 5). Preflight verifies; if not yet landed → Blocked (do not ship dangling section references).
- **Aligned with:** 2610162004-generic-fallback-and-classifier-refresh-plan.md (Ready/In Progress) — its 8a/8b/8c definitions and overrides (remote MCP connector → 8a borrowing remote-integration OAuth/data sub-step; `/plugin install` with any `source` → 8b). This plan's Identify table matches; no ordering dependency (either may land first).
- **Concurrent:** ~9 sibling refresh plans; none owns these 2 files (Preflight greps). 2610162004-generic-fallback-and-classifier-refresh-plan.md edits `references/classifier.md`, which this plan does not touch.
- **Blocks:** the eval-refresh plan's agent-extension cases (they assert behavior defined here).

### Constraints

- Two shipped files only; no projex filenames inside them.
- Wrapping: workflow and addendum prose at ~76 columns; tables single-line (existing convention).
- Preserve the workflow's leading HTML comment and the template headings `## Identify`, `## Evidence — Part A`, `## Evidence — Part B`, `## Subject Rubric`, `## Subject Verdict Notes`.
- Rubric names checks and concepts, not Claude Code version numbers (docs version-gate fields weekly — review §8 risk).
- §4.6 floor: tighten only. Addendum V-bullets supply only what the floor's `**Addendum:**` lines ask for.

### Assumptions

- **AS1:** Project-committed auto-approve keys take effect once the folder is trusted (docs only state they are ignored in untrusted folders). Rated HIGH either way; verify wording if docs change.
- **AS2:** Claude Code plugins/skills have no signing mechanism (none in the plugins-reference, marketplace-reference, loading or skills pages). V2 says "no documented signing".
- **AS3:** `npx -y <pkg>` without a version can resolve a newer release on a later launch (cache eviction, new machine). Rule wording ("a later launch or update can run an unaudited release") holds without relying on exact npx cache semantics.
- **AS4:** No sibling plan rewrites these files before execution (Preflight check; re-anchor = re-apply whole-file content, since both steps are full replacements).

### Impact Analysis

- **Direct:** the 2 files.
- **Adjacent:** `workflows/registry-package.md` audits of npm-shipped skills (classifier example 5) may borrow the 8c steps — now richer. `workflows/remote-integration.md` may borrow 8a remote steps 2–5 if the sibling routes connectors there.
- **Downstream (live verdict changes):**
  - Package-launched MCP servers with an unpinned launch line → HIGH `unpinned launcher` → CONDITIONAL (eval 22's exact APPROVED fails live → Hand-off).
  - Reference servers above Low capability lose Tier 1.
  - Plugins with any shell surface → Tier 3; unattended reviewed hooks → HIGH → CONDITIONAL; unreviewed or remote-fetching → REJECTED.
  - Skills with `!` blocks, broad `allowed-tools` or prerequisite installers → Tier 3 / CRITICAL.
  - Remote vendor servers with OAuth in a secret store → Tier 2, APPROVED reachable (2 MEDIUM).

---

## Implementation

### Overview

Preflight → Step 1 replace addendum → Step 2 replace workflow. Both are whole-file writes of the content blocks below (verbatim; the blocks use `~~~` fences because the content contains backtick fences). Then run the Verification Plan. Rationale for structure: both files are rewritten in >80% of their lines, so whole-file content is less error-prone than ~60 anchored replacements.

**Preflight (`<work-root>`):**
```bash
git log --oneline -1 20843cc                                   # floor commit reachable
git merge-base --is-ancestor 20843cc HEAD && echo floor-ok     # floor-ok
grep -c "^### V[1-5] " references/criteria.md                  # 5
grep -c "^## 4.6 Version & Update Integrity (shared floor)" references/criteria.md   # 1
grep -c "Workflow coverage tables" references/criteria.md      # 1
grep -c "Blocking CVE" SKILL.md                                # ≥ 1
grep -c "^## §1 — Scope & Permission Assessment\|^## §5 — Terms, Data Sharing & AI Use\|^## §6 — Token Custody & Consent Path" references/criteria/remote-integration.md   # 3
git log --oneline -1 -- workflows/agent-extension.md references/criteria/agent-extension.md   # 5c44b79 (AS4)
wc -c workflows/agent-extension.md references/criteria/agent-extension.md                    # 12907 / 6932
python3 evals/run_evals.py validate | head -3                  # pass
python3 -m unittest discover -s evals -p "test_*.py" 2>&1 | tail -3   # record count
```
Any mismatch on the first five → stop: the floor contract is missing (Blocked). Remote-integration count ≠ 3 → Blocked until 2610162007-remote-integration-rubric-refresh-plan.md closes (or its headings were renamed: re-anchor the two `§1, §5 and §6` citations to the new names and log it). A newer commit on the two files (AS4) → read it; if a sibling changed them, merge its intent into the blocks below before writing and log it.

---

### Step 1: Replace `references/criteria/agent-extension.md`

**Objective:** sourced scoring addendum: channel trust, capability + shell rating, transport/auth, behavioral indicators, repo-borne surfaces, §4.6 plug-in, disjoint tiers.
**Confidence:** High (facts primary-sourced); Medium on flag-level calibration (policy; see Risks)
**Depends on:** Preflight
**Do-Projex:** Encouraged
**Verify-Projex:** Encouraged (encodes verdict policy; tier disjointness and trace outcomes are easy to get subtly wrong)

**Files:** `references/criteria/agent-extension.md`

**Changes:** Before: current 125-line file (6,932 B). After: the whole file is exactly:

~~~markdown
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
~~~

**Rationale:**
- **Container model for 8b** (F1): the plugin docs show every 8a/8c surface can ship inside a plugin, so nested sub-audits avoid a fourth parallel rubric.
- **"Risk = default flag level"** fixes the old ambiguity between risk level and flag level. Named lowering conditions (scoped fs write, secret-store credential, vendor remote) keep eval 31 and vendor OAuth connectors out of mandatory CONDITIONAL, and keep APPROVED reachable for a pinned eval-22 shape (2 MEDIUM).
- **Shell-Surface Rating** (three levels) instead of "shell = CRITICAL": most real plugins carry `command` hooks; a blanket CRITICAL would REJECT them all, and the old "In-process Medium-High" under-rated them. Review state + trigger mode are the discriminators the docs support (session-start/monitor/`bin/` = unattended).
- **Credentials split** (own-service vs other / unverified publisher) keeps eval 23 REJECTED (keys handed to an unverified publisher = Critical) and eval 31 CONDITIONAL.
- **Unpinned launcher = HIGH** (tightens floor V5): an MCP launch line re-resolves at launch, so the floor's "audit what resolves now" covers only today's run. Pinning is a cheap condition.
- **Reference servers** keep moderate identity credit but no Tier 1 above Low capability (review Open Question 3: answered "no" for Medium+; yes for Low, e.g. Time).
- **No version numbers for harness CVEs** (Open Question 4): sources disagree (CVE-2025-59536: 1.0.111 vs 2.0.65); the rubric points to the advisories page instead.
- **Host-agnostic 8c** (Open Question 6): Agent Skills format; Claude Code specifics named as such.
- **Rejected alternatives:** per-sub-type addendum files (8b needs 8a + 8c anyway; extra load instructions; classifier/SKILL.md reference one file); keeping SSE as a peer (deprecated in spec and host).

**Verification:**
```bash
diff <(awk '/^~~~markdown$/{n++; on=1; next} /^~~~$/{on=0; next} on && n==1' .projex/2610162007-agent-extension-rubric-refresh-plan.md) references/criteria/agent-extension.md && echo same   # same
wc -c < references/criteria/agent-extension.md      # ≤ 15500 (expect 15098)
grep -c "^## Version & Update Integrity (§4.6)" references/criteria/agent-extension.md   # 1
grep -c "^- \*\*V[1-5]\*\* —" references/criteria/agent-extension.md                       # 5
```

**If this fails:** `git -C <work-root> checkout -- references/criteria/agent-extension.md` and rewrite from the block.

---

### Step 2: Replace `workflows/agent-extension.md`

**Objective:** per-sub-type procedures (8a / 8b / 8c / repo-borne), canonical coverage table, rubric sections mirroring `criteria.md` §4.1–§4.6, verdict notes aligned to the addendum.
**Confidence:** High
**Depends on:** Step 1 (section names it cites)
**Do-Projex:** Encouraged
**Verify-Projex:** Encouraged (coverage-row contract and cross-references)

**Files:** `workflows/agent-extension.md`

**Changes:** Before: current 228-line file (12,907 B). After: the whole file is exactly:

~~~markdown
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
~~~

**Rationale:**
- **Rubric renumbered 4.1–4.6** to mirror `criteria.md` (sibling workflows use the same numbering); the old `§4.6 Maintenance & Ecosystem` would otherwise point readers at the wrong §4.6.
- **Coverage table uses exact canonical labels** so graders and the row contract match; `Permissions / least privilege` and `Web search` are tightened to Required at every tier (every Type 8 subject has a capability surface; incident search was already Required here).
- **Evidence by sub-type, not by question list:** the old 10-question list repeated the rubric; procedures carry the new checks once.
- **No running of unreviewed servers outside a sandbox** — consistent with the classifier's read-only stance and the "declared ≠ enforced" principle.
- Template headings and the leading HTML comment are kept so `SKILL.md` Step 1 instructions still map.

**Verification:**
```bash
diff <(awk '/^~~~markdown$/{n++; on=1; next} /^~~~$/{on=0; next} on && n==2' .projex/2610162007-agent-extension-rubric-refresh-plan.md) workflows/agent-extension.md && echo same   # same
wc -c < workflows/agent-extension.md               # ≤ 17000 (expect 16586)
grep -c "^### §4\." workflows/agent-extension.md   # 0
grep -c "^## Identify$\|^## Evidence — Part A$\|^## Evidence — Part B$\|^## Subject Rubric$\|^## Subject Verdict Notes$" workflows/agent-extension.md   # 5
```
**If this fails:** `git -C <work-root> checkout -- workflows/agent-extension.md` and rewrite from the block.

---

## Verification Plan

### Automated Checks

- [ ] `python3 evals/run_evals.py validate` passes; unittest passes with the Preflight count.
- [ ] Consistency script (run from `<work-root>`; not committed):
```bash
python3 - <<'EOF'
import re, pathlib
crit = pathlib.Path("references/criteria.md").read_text(encoding="utf-8")
add  = pathlib.Path("references/criteria/agent-extension.md").read_text(encoding="utf-8")
wf   = pathlib.Path("workflows/agent-extension.md").read_text(encoding="utf-8")
# canonical rows present verbatim
sec = crit.split("### Rows by tier")[1].split("**Tier 1 (Quick):**")[0]
canon = [l.split("|")[1].strip() for l in sec.splitlines() if l.startswith("| ") and not l.startswith("| Check")]
tbl = wf.split("### Audit coverage tracking table")[1].split("## Subject Rubric")[0]
labels = [l.split("|")[1].strip() for l in tbl.splitlines() if l.startswith("| ")]
assert len(canon) == 12 and not [c for c in canon if c not in labels], [c for c in canon if c not in labels]
# addendum sections the workflow cites
for h in ["## Tier Thresholds", "### Shell-Surface Rating", "## Repo-Borne Surfaces",
          "## Version & Update Integrity (§4.6)", "## Transport & Auth (8a)", "## Behavioral & Model-Context Risk"]:
    assert h in add, h
assert all(add.count(f"- **V{i}** —") == 1 for i in range(1, 6)) and add.count("**§4.3 own-code line**") == 1
ri = pathlib.Path("references/criteria/remote-integration.md").read_text(encoding="utf-8")
for h in ["## §1 — Scope & Permission Assessment", "## §5 — Terms, Data Sharing & AI Use", "## §6 — Token Custody & Consent Path"]:
    assert h in ri, h
assert "remote-integration.md` §1" in wf and "remote-integration.md`\n§1, §5 and §6" in add
# floor references resolve
for t in (add, wf):
    for v in re.findall(r"§4\.6 (V\d)", t):
        assert v in {"V1","V2","V3","V4","V5"}, v
# stale strings gone
for t in (add, wf):
    low = t.lower()
    for bad in ["system_prompt", "sse (remote)", "http/sse", "claude-code/plugins", "docs.anthropic.com",
                "in-process (skills/plugins)", "typically n/a", "listing status, usage metrics",
                "anthropic official / first-party", "§4.6 maintenance"]:
        assert bad not in low, bad
assert not re.search(r"^### §4\.", wf, re.M)
assert len(add.encode()) <= 15500 and len(wf.encode()) <= 17000
assert ".projex" not in add + wf and not re.search(r"\d{10}-[a-z0-9-]+-(plan|eval)\.md", add + wf)
print("OK")
EOF
```
- [ ] `git -C <work-root> diff --stat <base>..HEAD` → only the 2 files + this plan's projex files.

### Manual Verification (paper traces)

Walk each case through the workflow → addendum → `SKILL.md` Step N + `criteria.md` §4.6. Record the cited rule per hop in the execution log.

| # | Case | Expected |
|---|---|---|
| T1 | eval 22: `npx -y @modelcontextprotocol/server-filesystem /Users/me/projects` | Reference server (moderate identity); fs read MEDIUM + scoped fs write MEDIUM (if current ≥ last fix) → capabilities not Low → **Tier 2** (not Tier 3: no shell, scoped). Unpinned launcher HIGH → **CONDITIONAL**: pin exact version at/above last fixed advisory. Pinned variant → 2 MEDIUM → APPROVED reachable |
| T2 | eval 23: Discord-shared `universal-ai-mcp-server`, 3-star week-old repo, OpenAI + Anthropic keys in `env` | Peer-shared HIGH; unknown publisher → **Tier 3**; credentials to unverified publisher = Critical → **REJECTED** |
| T3 | eval 31: Brave Search MCP, API key in env | Vendor first-party `@brave/brave-search-mcp-server` (strong identity); own-service key in config `env` HIGH; outbound to fixed vendor API → **Tier 2**, **CONDITIONAL** (key scope + secret store; pin) |
| T4 | eval 40: `npm install -g @anthropic/some-code-skill` | Classifier routes registry-package (unchanged); that workflow may borrow 8c steps 2–4. No change |
| T5 | Third-party marketplace plugin, `github` source without `sha`, `SessionStart` `command` hook running a bundled, reviewed formatter | Shell surface → **Tier 3**; reviewed + unattended → HIGH; unpinned source HIGH → **CONDITIONAL**: pin `sha`, auto-update off, re-audit on hook change |
| T6 | Same plugin, hook runs `curl … \| sh` | Shell-Surface CRITICAL (downloads and runs remote code) → **REJECTED** |
| T7 | Skill from a skill hub: `allowed-tools: Bash`, body "Prerequisites: run this installer" | Tier 3 (skill hub, shell surface); prerequisite lure CRITICAL → **REJECTED** |
| T8 | Markdown-only style-guide skill from an Anthropic-operated marketplace, no frontmatter grants, pinned | All Tier 1 conditions; §4.6 clean → **Tier 1**, APPROVED reachable |
| T9 | Remote vendor MCP connector by URL (no local code), OAuth with proportional scopes in host token store | Routed 8a (classifier sibling override). Transport MEDIUM; credential MEDIUM (secret store); OAuth scopes/data use/custody per remote-integration §1/§5/§6 add no HIGH → **Tier 2**; V1–V3 `N/A (hosted service)`; tool list recorded as V3/V5 baseline; V5: cannot hold, list triggers → **APPROVED** reachable (2 MEDIUM) |
| T10 | Cloned repo with `.mcp.json` (unknown server) + project `enableAllProjectMcpServers`, used in CI via `claude -p` | Repo-borne: loads without asking in `-p`; auto-approve key HIGH; unknown server → Tier 3 per 8a; condition `--strict-mcp-config` / managed deny list, or REJECTED if the server itself rates CRITICAL |

### Acceptance Criteria Validation

| Criterion | How to Verify | Expected Result |
|---|---|---|
| Exact content | Step `diff`s | `same` ×2 |
| Plug-in + own-code line | consistency script | `OK` |
| Canonical rows | consistency script | `OK` (12/12) |
| Cross-refs, stale strings, sizes, no projex refs | consistency script | `OK` |
| Harness green | validate + unittest | pass; same count |
| Calibration | T1–T10 in log | match table |
| Scope | `git diff --stat` | 2 shipped files |

---

## Rollback Plan

1. Before close: `projex-abandon.sh <repo-root> claude/youthful-dijkstra-5ov1kt projex/2610162007-agent-extension-rubric-refresh --worktree`. Base untouched.
2. After squash-close: `git -C <repo-root> revert <squash-sha>` (touches only the 2 files). If the eval-refresh plan already asserts the new behavior, revert it first.

---

## Notes

### Decisions

- **Single addendum, not per-sub-type files** (review OQ1): 8b audits need 8a + 8c rules; one more load path costs more than ~8 KB of growth; both files stay below sibling pairs.
- **Reference/vendor servers and Tier 1** (OQ3): Tier 1 only with Low capability.
- **Host scope** (OQ6): host-agnostic 8c/8a wording; Claude Code controls named as examples.
- **Remote MCP** (OQ2): decided by the classifier sibling — tool-bearing remote MCP / AI-assistant connectors → 8a; OAuth-only SaaS apps without agent tools stay Type 9. This plan accepts no-local-code 8a and rates the OAuth grant by citing remote-integration addendum §1/§5/§6 (not copying), per both siblings' Hand-off rows.

### Hand-off

| Owner | Requirement |
|---|---|
| Classifier sibling (2610162004-generic-fallback-and-classifier-refresh-plan.md) — F13 | Already planned there (verified 2026-10-16: overrides for remote MCP → 8a and `/plugin install` any source → 8b; refreshed row 8 signals; 8a/8b/8c definitions). Remaining asks, only if not covered: (a) `/plugin install <name>@<marketplace>` / `claude plugin install` → agent-extension 8b whatever the entry's `source` type (incl. `npm`: fetched by Claude Code with scripts off; the marketplace + loader is the gate). Keep direct `npm install -g` → registry-package (eval 40). (b) Remote MCP by URL / connector → agent-extension 8a (decided there; this plan's workflow accepts no-local-code 8a and cites remote-integration §1/§5/§6 for the grant). (c) Signals: add `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `/plugin install`, `claude plugin install`, `claude mcp add`, `registry.modelcontextprotocol.io/*`, `*.mcpb` / `*.dxt`, `github.com/modelcontextprotocol/servers`; drop `claude-code/plugins/*` and `modelcontextprotocol.io/*` as a code signal (docs site); widen host list beyond Cursor/Cline/Continue. (d) Optional label "8c · Claude Code skill" → "8c · Skill (Agent Skills format)" — `SKILL.md` has 16 B headroom, so only byte-neutral edits there |
| Remote-integration sibling (2610162007-remote-integration-rubric-refresh-plan.md) | Keep the §1 / §5 / §6 heading names stable (this plan cites them); if renamed, request a revise of this plan. Its Type 9 tool-capability depth should cite this addendum's Capability Scope and Behavioral tables |
| Eval-refresh plan — F8 | Eval 22: premise "Anthropic-maintained" → "MCP reference server (steering group)"; expected Tier 2, CONDITIONAL (unpinned `npx -y`; pin at/above last fixed advisory). Replace exact_match APPROVED with verdict_check `[CONDITIONAL]`, or pin a version in the prompt and accept `[APPROVED, CONDITIONAL]`. Keep "directory scoping" assertion but add "version at/above fixed advisory" |
| Eval-refresh plan — F9 | Eval 31: expected_output → official `@brave/brave-search-mcp-server` (vendor first-party); Tier 2; CONDITIONAL for env-held key; assertions unchanged |
| Eval-refresh plan — F10 | New cases from T5/T6 (8b hook + unpinned source; remote-fetching hook → REJECTED), T7 (8c prerequisite lure → REJECTED), T8 (8c Tier 1 APPROVED), T9 (remote vendor OAuth), T10 (repo-borne `.mcp.json` in `-p`), plus a tool-poisoning description case (CRITICAL → REJECTED). Eval 23: optionally assert credential-to-unverified-publisher rationale. `validate`'s ≥ 3/workflow invariant hides sub-type coverage — consider ≥ 1 per 8a/8b/8c |
| Orchestrator / STEWARDSHIP | Record review (Last Reviewed 2026-10-16, Next Due 2026-12-15); add event triggers: MCP spec revision; Claude Code plugin/skill/MCP docs changes to component types, source types or trust gating |

### Risks

- **Flag calibration is policy** (unpinned = HIGH; unattended reviewed shell = HIGH; scoped fs write = MEDIUM). Mitigation: each lives in one table row or rating bullet; retune = one-line edits. T1–T10 pin current intent.
- **Doc churn** (Claude Code docs version-gate fields weekly). Mitigation: rubric encodes concepts (shell-bearing components, pin strength, trust gating), cites no Claude Code version numbers.
- **Read cost** +11.8 KB per Type 8 audit. Mitigation: no duplicated tables between workflow and addendum; coverage table is the only list both need.
- **Live eval 22 regresses** until the eval plan lands (exact APPROVED vs new CONDITIONAL). Intended; Hand-off F8. No live run before all refreshes (human decision).
- **Overfit to Claude Code** (review bias check). Mitigation: 8a/8c host-agnostic; Claude Code specifics labelled.

### Unverified / Hedged (kept out of rubric or hedged in it)

- MCP Registry GA status (README says preview; may be stale) → "preview at last review".
- Registry code scanning: not documented either way → "No documented code review".
- Plugin/skill signing absence (AS2) → "no documented signing".
- Auto-approve keys honored after trust (AS1).
- `Origin`/localhost rule verified on the 2025-11-25 transports page only.
- Claude Code CVE fixed versions (CVE-2025-59536, CVE-2026-21852) — not cited.
- Incident counts (ClawHavoc 341 vs ≥ 1,184), postmark-mcp, SANDWORM_MODE, AgentBaiting, Smithery hosting traversal, OWASP MCP/AST numbering, SkillCloak/Trail of Bits scanner bypass — only ClawHavoc named (hedged "hundreds"); others omitted.
- Whether `claude-plugins-official` lists third-party-authored plugins — hedged as "still rate each listed plugin's own author and source".

### Open Questions

None blocking. Calibration choices above are recorded as Decisions/Risks for the orchestrator to override before execution.

### Split Decision

`No split — heuristic tripped but steps tightly coupled (rationale: > 50 KB only because both target files are embedded verbatim; 2 steps + preflight, so the > 5-step half does not trip; one .projex scope; the workflow cites addendum headings).`

### Revision Log

| Date | Trigger | Change |
|---|---|---|
| 2026-10-16 | Initial | Full rewrite plan for both files; primary sources fetched |
| 2026-10-16 | Sibling hand-offs via orchestrator (2610162004-generic-fallback-and-classifier-refresh-plan.md, 2610162007-remote-integration-rubric-refresh-plan.md) | Remote no-local-code 8a accepted in Identify; 8a step 5 + addendum OAuth line cite remote-integration addendum §1/§5/§6; Preflight + consistency script check those headings; Dependencies gained the cross-reference requirement |
| 2026-10-16 | Sibling note (cli-binary planner): workflow `### §4.6 Maintenance & Ecosystem` clashes with shared §4.6 | Confirmed already handled: rubric renumbered to `### 4.1`–`### 4.6` mirroring `criteria.md`, with `4.6 Version & Update Integrity`; script asserts no `### §4.` and no `§4.6 Maintenance` |
