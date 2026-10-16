# Agent-Extension Rubric — Stewardship Review (2026-10-16)

> **Status:** Draft
> **Author:** Claude (Opus)
> **Parent:** Orchestrator
> **Subject:** `workflows/agent-extension.md` + `references/criteria/agent-extension.md` (8a MCP / 8b Claude Code plugin / 8c Claude Code skill)
> **Type:** Gap Analysis (scheduled `STEWARDSHIP.md` review, checklist steps 1–4; step 4 offline only)
> **Tier:** Standard (Primary + Secondary in-repo, Tertiary live web research)
> **Lenses Applied:** Constraint Mapping | Inversion | Steel-Manning
> **Related Projex:** 2604160900-agent-extension-workflow-m43-plan.md | 2604160900-agent-extension-workflow-m43-walkthrough.md | 2604172000-stewardship-cadence-m63-walkthrough.md | 2604070218-install-auditor-subject-typed-redesign-nav.md | 2610161852-dispatcher-rubric-consistency-walkthrough.md | 2610161927-browser-extension-ide-plugin-stewardship-review-eval.md | 2610161927-registry-package-and-ci-action-stewardship-review-eval.md | 2610161927-remote-integration-generic-stewardship-review-eval.md | 2610161928-stewardship-review-container-cli-desktop-eval.md | 2610162007-agent-extension-rubric-refresh-plan.md (P1)

---

## 1. Executive Summary

Rubric written 2026-04-16 from an early-2025 mental model; 60-day cadence never exercised (6 months, ~3 missed cycles). Verdict: **materially stale on all three sub-rubrics**. 8a treats MCP as a static "manifest" with SSE as a peer transport — MCP has no static manifest (runtime `tools/list`, mutable), HTTP+SSE is deprecated, and the 2026-07-28 spec went stateless and tightened OAuth. 8b models plugins as "slash commands + hooks + settings, in-process"; real plugins bundle skills, agents, hooks, MCP servers (incl. downloadable `.mcpb`), LSP servers, background monitors, `bin/` executables — i.e. **shell execution**, routinely — fetched from decentralized marketplaces with six source types, some unpinned or command-driven. 8c misses `allowed-tools` (not gated by workspace trust), `` !`cmd` `` shell injection, skill-scoped hooks, and the cross-harness Agent Skills standard whose marketplaces had documented mass-malware (ClawHavoc, Feb 2026). Trust anchor "Anthropic official" is outdated (MCP → Linux Foundation AAIF, Dec 2025; reference servers self-describe as "educational examples"). Two of three eval cases have stale premises (Brave server now first-party; filesystem server's directory scoping had a CVSS 9.6 bypass). Zero eval cases exercise 8b or 8c. **Recommend 3 plan-projex** (rubric rewrite, eval refresh, classifier Type-8 signals) — no in-place edits per checklist step 5.

## 2. Evaluation Scope

**Subject:** Type 8 workflow (228 lines) + criteria addendum (125 lines); touches `references/classifier.md` Type-8 rows and `evals/evals.json` cases 22, 23, 31, 40.

**Questions:** (Q1) Stale commands/URLs/versions? (Q2) Tier thresholds match ecosystem norms? (Q3) Security-relevant ecosystem changes since 2026-04-16 (and pre-existing ones the rubric never absorbed)? (Q4) Do eval cases still match reality (offline)?

| Criterion | Weight | Description |
|---|---|---|
| Ecosystem accuracy | High | Rubric's model of MCP/plugins/skills matches current specs + docs |
| Threat coverage | High | Known attack classes + incidents representable as flags |
| Verdict calibration | High | Tier/verdict rules yield correct outcomes on canonical cases |
| Internal consistency | Medium | Tier triggers non-contradictory; aligns with shared `references/criteria.md` rows |
| Eval fidelity | Medium | Cases cover 8a/8b/8c; expectations factually current |
| Actionability | Medium | Auditor can execute checks with available signals |

**Out of scope:** edits to workflow/criteria/STEWARDSHIP (step 5 → plans); live `run_evals.py run` (not approved); steps 7–8 (inventory/nav log updates — orchestrator/plan owns); other subjects; script bugs.

## 3. Context Analysis

- **Current state:** Workflow Identify → Evidence A/B → §4.1–4.6 → Verdict Notes; addendum: channel trust | capability risk | transport | behavioral risk | tiers. Only edit since creation: 2026-10-16 roadmap-label strip (`5c44b79`, comment only).
- **History:** Born M4.3 (`2604160900-agent-extension-workflow-m43-plan.md`). Plan Problem §4 enumerated channels as "MCP registries (mcp.so, Smithery), GitHub, npm, Claude Code marketplace/community, shared `.mcp.json`, git-cloned skills" — no primary-source research recorded; walkthrough flagged eval harness gap only.
- **Constraints:** Hard — rubric is markdown read by an agent at audit time (must stay compact; F7 read-cost finding `2604170511-measure-read-cost-f7-m53-findings.md`). Soft — 8a/8b/8c three-way split; one-installable-one-type rule. Self-imposed — "Anthropic official" as top trust anchor.
- **Stakeholders:** devs/agents asking "is this MCP/plugin/skill safe"; security reviewers consuming reports; eval graders.
- **Ecosystem velocity (why 60 d was right):** MCP spec revisions 2025-03-26 → 2025-06-18 → 2025-11-25 → **2026-07-28**; Claude Code plugin system went from bundle concept to marketplace w/ policy controls, npm/archive/command sources, monitors, LSP, `bin/`; Agent Skills became an open cross-vendor standard.

## 4. Foundations

**Principles:** innermost-trust-boundary classification (`references/classifier.md`); capability-scoped risk (least privilege); provenance > popularity; declared ≠ enforced (claims must be verified against implementation).

| Assumption (embedded in rubric) | Validity now | Risk if wrong | Sensitivity |
|---|---|---|---|
| A1 MCP servers have a declarative, enumerable manifest | ✗ — tools discovered at runtime via `tools/list`; can change post-approval; `server.json`/MCPB `manifest.json` are publisher claims, unenforced | Rug pulls + undeclared tools missed | Flips 8a evidence procedure |
| A2 SSE is a current remote transport | ✗ — HTTP+SSE deprecated (spec 2026-07-28; Claude Code docs) | Wrong transport taxonomy; legacy SSE not flagged | Low on verdicts, High on accuracy |
| A3 8a has ~no prompt/behavioral surface | ✗ — tool names/descriptions/results enter model context (tool poisoning, OWASP MCP Top 10 beta) | Tool-poisoned servers rated Low behavioral | Flips verdict on poisoning cases |
| A4 8b plugins = commands + hooks + settings, in-process | ✗ — also skills, agents, MCP servers, LSP, monitors, `bin/`, userConfig secrets, deps; hooks/monitors are shell processes | Shell-exec capability under-rated as "Medium-High in-process" | Flips Tier + verdict for most plugins |
| A5 "Claude Code marketplace" = curated listing w/ usage metrics | ✗ — decentralized `marketplace.json` catalogs; official ones under `github.com/anthropics/`; no usage metrics | Unverifiable trust signal; mis-scored provenance | High |
| A6 8c risk is behavioral only | ✗ — `allowed-tools` self-grants tools (not gated by workspace trust), `` !`cmd` `` runs shell pre-render, skill `hooks` persist for session, bundled scripts | Skills with shell surface rated non-Critical | Flips verdict |
| A7 "Anthropic official" = highest trust anchor | Partial — MCP governance → AAIF/LF (Dec 2025); reference servers "educational examples, not production-ready"; Anthropic marketplaces still Anthropic | Over-trust of reference servers (CVE history) | Flips eval 22 APPROVED→CONDITIONAL plausibly |
| A8 Registries (mcp.so, Smithery) are the MCP registry landscape | ✗ — official MCP Registry (preview, namespace-verified) missing; skill marketplaces (skills.sh, ClawHub) missing | Wrong channel scoring | Medium |
| A9 Agent-extension coverage rows can replace shared canonical rows | ✗ — omits CVE/advisories, typosquat/name, license rows that `references/criteria.md` marks Required for all tiers | Reports fail shared-row expectations; impersonation unchecked | Medium |

**Prior work:** M4.3 plan/walkthrough (no external sourcing recorded); M6.3 stewardship cadence (60 d interval, never run). No prior review entry.

## 5. Analysis

### 5.1 8a MCP model vs current spec — Confidence H — Lens: Constraint Mapping

- **Finding:** Workflow §4.1 "capability is declarative and enumerable. Start by reading the manifest" (`workflows/agent-extension.md:144`) and Identify row "`github.com/<org>/<repo>` with MCP manifest" (:35) assume a static manifest. MCP exposes tools at runtime (`tools/list`); 2026-07-28 adds `server/discover`, stable ordering, caching hints (`ttlMs`/`cacheScope`), `subscriptions/listen` for change notifications ([changelog](https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/docs/specification/2026-07-28/changelog.mdx)). Declarative artifacts that do exist: registry `server.json`, MCPB `manifest.json` — neither enforces permissions.
- **Transport:** addendum table (`references/criteria/agent-extension.md:59-65`) lists "SSE (remote)" as peer. Spec 2026-07-28: "HTTP+SSE transport is deprecated. Migrate to Streamable HTTP"; sessions/`Mcp-Session-Id` removed; Claude Code docs: "The SSE … transport is deprecated", also supports WebSocket. Correct taxonomy: stdio | Streamable HTTP (loopback) | Streamable HTTP (remote) | WebSocket (host-specific) | legacy HTTP+SSE (flag: unmaintained).
- **Auth:** rubric remote-transport check is "verify TLS, server identity" only. Spec now: OAuth 2.1 resource server, Client ID Metadata Documents preferred, Dynamic Client Registration deprecated, RFC 9207 `iss` validation required of clients, credentials bound to issuer. Remote 8a audit should check auth mode (none | static header token | OAuth) and token scope.
- **Deprecated primitives:** Roots (a fs-scoping signal), Sampling, Logging deprecated (12-month window). Rubric doesn't use them yet — but a future "scoping via Roots" check must not be added.
- **Implication:** 8a Identify + §4.1/§4.2 + transport table need rewrite; add "tool set can change after approval → pin version + re-review on update" rule.

### 5.2 8a behavioral surface / threat classes — Confidence H — Lens: Inversion

- **Finding:** §4.5 "Typically N/A — tool servers … do not shape agent behavior proactively" (:187); addendum "No prompt/behavioral surface (pure tool server, 8a) = not applicable" (:87). Inversion ("how does a malicious 8a server win?"): (a) **tool poisoning** — hidden instructions in tool descriptions (OWASP MCP Top 10 beta, MCP03); (b) **rug pull** — descriptions/behaviour mutate after approval; (c) **shadowing / cross-server** — one server's description steers use of another's tools; (d) **indirect prompt injection** via fetched content (Claude Code MCP docs warn explicitly); (e) **config hijack** — SANDWORM_MODE (Feb 2026) dropped a rogue server and edited several agent-tool configs; (f) **lethal-trifecta** combos: private-data read + untrusted input + egress.
- **Incidents to anchor flags:** postmark-mcp (Sep 2025, malicious npm version BCC-exfiltrated mail); AgentBaiting/FakeGit (2026, ~800 fake skill/MCP repos — vendor-reported, Medium conf).
- **Implication:** move tool descriptions into 8a behavioral surface (read every description for imperative/hidden text); add rug-pull + trifecta rules to verdict notes.

### 5.3 8b plugin model — Confidence H — Lens: Constraint Mapping

- **Finding:** Rubric (:36-37, :146, :157, :189) — "slash commands + hooks + settings", "Runs in agent process; no transport isolation", path signal `claude-code/plugins/*`. Primary docs ([manifest ref](https://code.claude.com/docs/en/plugins-reference)): manifest `.claude-plugin/plugin.json` (optional); components `skills/` `commands/` `agents/` `hooks/hooks.json` `.mcp.json` `.lsp.json` `output-styles/` `workflows/` `themes/` `monitors/monitors.json` `bin/` `settings.json`; `mcpServers` accepts `.mcpb`/`.dxt` bundles **and `https://` bundle URLs** (downloaded at load); `experimental.monitors` = "Shell command Claude Code runs as a persistent background process"; `bin/` = "on the Bash tool's `PATH`"; `userConfig` w/ `sensitive` secrets; `dependencies` = transitive plugins; `version` unset → not pinned. `settings` only honors `agent`, `subagentStatusLine` — so "settings injection" risk row is mostly obsolete for plugins (but project `.claude/settings.json` is not — see 5.6).
- **Consequence:** 8b is a **container of 8a + 8c + shell**. Hooks (`type: command`) are shell execution on lifecycle events (`PreToolUse`, `PostToolUse`, `SessionStart`, …) → addendum "Shell / command execution = Critical", not "In-process Medium-High".
- **Implication:** 8b procedure = enumerate every component type; apply 8a sub-audit per bundled MCP server, 8c per bundled skill; rate hooks/monitors/`bin/`/LSP as shell capability; flag remote `.mcpb` URLs and unpinned versions.

### 5.4 8b distribution & provenance — Confidence H — Lens: Constraint Mapping

- **Finding:** Rubric channel row "Claude Code marketplace / community — Marketplace listing; usage metrics" (:16) and research guidance "Listing status, usage metrics, review process" (workflow :103). Reality ([marketplace ref](https://code.claude.com/docs/en/plugins/marketplace-reference)): any repo/URL hosting `.claude-plugin/marketplace.json`; official names (`claude-plugins-official`, `anthropic-agent-skills`, `knowledge-work-plugins`, …) reserved to `github.com/anthropics/`; community names (`claude-plugins-community`) likewise; impersonating names refused. Plugin sources: relative | `github` (`ref`,`sha`) | `url` | `git-subdir` | `npm` (install scripts never run) | `archive` (`sha256`) | `command` (runs a shell command on user machine at install **and once per session**). Org controls: `strictKnownMarketplaces`, `blockedMarketplaces`, `disableCommandPluginSources`. Anthropic directory has submission flow; third-party guidance (Medium conf) reports Anthropic disclaims verifying marketplace plugins and no plugin binary signing.
- **Trust signals now available:** marketplace source host/owner; Anthropic-reserved marketplace vs third-party; source pin strength (`sha`/`sha256`/exact version > tag > branch/default); `command` source = Critical-adjacent; `forceRemoveDeletedPlugins`/auto-update behaviour.
- **Incident:** Prompt Security/SentinelOne (Jan 2026) — benign-looking marketplace plugin whose dependency skill redirected Python installs to attacker source (dependency hijack).
- **Implication:** replace "usage metrics" row with marketplace-identity + pin-strength rows; add `command`/`archive`-without-`sha256`/unpinned-`ref` flags.

### 5.5 8c skill model — Confidence H — Lens: Inversion

- **Finding:** Rubric frames 8c as "markdown + scripts … behavioral-shaping risk is primary", "Risk is behavioral rather than network-based" (:148, :159), and cites non-existent "SYSTEM_PROMPT files" (:175, :191). Primary docs ([skills](https://code.claude.com/docs/en/skills)):
  - `allowed-tools`: "Workspace trust doesn't gate this field … A skill can grant itself broad tool access" — even in `-p` runs in untrusted folders.
  - `` !`<command>` `` / ```` ```! ```` dynamic context injection runs shell before the model sees the skill; "Injected commands never prompt for permission while the skill renders" (still checked against permission rules).
  - `hooks` frontmatter: registered on invoke, active rest of session.
  - `context: fork` background runs edit outside checkpoints.
  - Locations: enterprise | personal | project | nested | `--add-dir` | plugin | claude.ai-synced; precedence enterprise > personal > project; a skill can replace a bundled skill/command of same name (shadowing).
  - Controls: `disableSkillShellExecution`, `allowManagedPermissionRulesOnly` (ignores skill `allowed-tools`), deny rules `Skill(name *)`.
  - Open standard: Agent Skills (agentskills.io) — same `SKILL.md` format consumed by other harnesses.
- **Ecosystem incidents:** ClawHavoc (ClawHub, Feb 2026 — 341+ malicious skills per Koi, counts vary up to 1,184); OWASP Agentic Skills Top 10 (AST01 Malicious Skills); scanner bypass research — Trail of Bits bypassed ClawHub/Cisco/skills.sh detectors (CSA note 2026-06-10), SkillCloak >90% evasion across 8 scanners (CSA 2026-07-06; AI-assisted note, Medium conf). → registry "scanned" badge is weak positive at most.
- **Implication:** 8c needs a frontmatter audit (`allowed-tools`, `hooks`, `context`, `disable-model-invocation`, `paths`), a shell-surface audit (`!` blocks + `scripts/`), name-shadowing check, and a "scanner pass ≠ safe" note. Classify skill with shell surface as Critical capability, not "In-process Medium".

### 5.6 Repo-borne / auto-loaded surfaces — Confidence H — Lens: Inversion

- **Finding:** Rubric treats install as deliberate action. Real attack path: clone a repo containing `.mcp.json`, `.claude/settings.json` (hooks, `env`), `.claude/skills/`. Claude Code CVE-2025-59536 (CVSS 8.7, project hooks/MCP executing before trust prompt; `enableAllProjectMcpServers`/`enabledMcpjsonServers` auto-approve) and CVE-2026-21852 (project `ANTHROPIC_BASE_URL` → API key exfil before trust warning) — Check Point; fixed versions vary by source (Medium conf on versions). MCP docs: in `claude -p`, SDK and cloud sessions project-scoped servers load **without asking**. Org controls: `managedMcpServers`, `deniedMcpServers`, `managed-mcp.json`.
- **Implication:** add "repo-borne extension" sub-pattern (Identify) + CONDITIONAL mitigations referencing managed settings; flag auto-approve keys; require harness version ≥ fixed release in conditions.

### 5.7 Channel trust table — Confidence H (structure) / M (some rows) — Lens: Constraint Mapping

| Current row | Status | Correction |
|---|---|---|
| Anthropic official — "anthropic.com, docs.anthropic.com" | Stale | Split: (a) Anthropic-operated marketplaces/plugins (`github.com/anthropics/*`); (b) MCP reference servers (`modelcontextprotocol/servers`, steering-group maintained, LF/AAIF governance, README: "educational examples … not as production-ready solutions"); (c) **vendor first-party** server (e.g. `@brave/brave-search-mcp-server`). Claude Code docs now at `code.claude.com/docs` |
| MCP registry (mcp.so, Smithery) | Incomplete | Add **official MCP Registry** (`registry.modelcontextprotocol.io`, preview; namespace proof via GitHub OAuth/OIDC or DNS; no code scanning — delegates to npm/PyPI/Docker); keep aggregators (mcp.so, Glama) as discovery-only; Smithery hosted = remote-trust (Jun 2025 build-pipeline path traversal exposed Fly.io token → 3,000+ hosted apps, patched, no exploitation found) |
| Claude Code marketplace / community | Wrong | See 5.4 |
| — (missing) | Add | Skill marketplaces: skills.sh (third-party scanners, bypassable), ClawHub (documented mass malware) → Low; scanner results = weak signal |
| — (missing) | Add | MCPB/`.dxt` bundle (one-click Desktop; manifest declares, does not sandbox) |
| npm-wrapped MCP | OK, extend | Add `npx -y <pkg>` unpinned = auto-latest → HIGH (rug-pull/hijack window) unless version pinned |

### 5.8 Tier thresholds & internal consistency — Confidence H — Lens: Steel-Manning

- **Contradictions:** (i) localhost HTTP is Tier-1-allowed (`criteria/agent-extension.md:99`) **and** a Tier 2 trigger (:110). (ii) fs-write is a Tier 3 trigger (:119) yet eval 22 (fs read/write server) expects Tier 1. (iii) Workflow coverage table omits `CVE / advisories`, `Typosquat / name verification`, `License compatibility` — Required at every tier in `references/criteria.md` §rows; dispatcher says addendum wins on subject patterns, but these are canonical rows, not patterns.
- **Steel-man (keep Tier 1 for eval 22):** official reference server, directory-scoped, stdio, huge adoption — forcing Tier 3 on every fs-write server wastes effort on the ecosystem's most-used servers. **Counter:** that server shipped CVE-2025-53109 (CVSS 9.6 symlink escape) + CVE-2025-53110 (prefix bypass) defeating exactly the scoping mitigation, fixed 2025.7.1 (sources vary: 2025.7.1 vs 2025.7.01; legacy 0.6.3 vs 0.6.4); sibling `mcp-server-git` had CVE-2025-68143/68144/68145 (fixed by 2025.12.18) + CVE-2026-27735 (2026.1.14). Resolution: explicit carve-out — "reference/vendor-official server with directory-scoped fs-write, stdio, version ≥ last fixed advisory → Tier 2 minimum; CVE row mandatory" — rather than Tier 1.
- **Implication:** rewrite tier lists so triggers are disjoint; restore canonical rows; add advisory-version gate.

### 5.9 Classifier Type-8 signals — Confidence M-H — Lens: Constraint Mapping

- (a) Override "Claude Code skill or plugin distributed via npm → registry-package" (`references/classifier.md:65`, worked example 5) holds for direct `npm install -g`; **not** for `/plugin install x@mkt` whose marketplace entry has `source: npm` — Claude Code fetches with scripts disabled; marketplace + Claude Code loader is the innermost gate → agent-extension 8b. Eval 40 tests only the direct-npm case (still correct).
- (b) Remote MCP server added by URL / OAuth connector (no local code): matches Type 8 (MCP) and Type 9 ("OAuth flow … no local code install"); no override; `workflows/remote-integration.md` never mentions MCP. Risk: inconsistent routing.
- (c) Signals stale: `claude-code/plugins/*` → `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `/plugin install`, `claude plugin install`, `claude mcp add`, `registry.modelcontextprotocol.io/*`, `*.mcpb`/`*.dxt`, `skills.sh/*`, `npx skills add`. Host list "Cursor / Cline / Continue" → Agent Skills + MCP now consumed by Codex, Copilot/VS Code, Gemini, ChatGPT, OpenClaw (Medium conf on exact list).
- **Ownership:** classifier is dispatcher-level, edited today by `2610161852-dispatcher-rubric-consistency-plan.md`; Type-8 rows are this subject's — recommend a separate small plan to avoid colliding with sibling evals.

### 5.10 Eval cases (checklist step 4, offline) — Confidence H

- **Run:** `validate` ✓ (41 evals, 248 assertions; agent-extension 3 ≥ min 3); `prepare --workflow agent-extension` ✓ (evals 22, 23, 31 → scratch workspace outside repo); `grade`/`summary` → 0 graded (no responses; live `run` not approved). `unittest` 12/12 ✓. **No regression signal obtainable** — absence ≠ pass.
- **Eval 22** (filesystem server, expects Tier 1 APPROVED): premise "Anthropic-maintained" stale (5.7); expected rationale treats directory scoping as mitigation without version gate (5.8); `npx -y` unpinned not mentioned. Assertion "Verdict is APPROVED" (exact_match) will **penalize** a correct CONDITIONAL ("pin ≥ 2025.7.1") answer. Stale → fix.
- **Eval 31** (Brave Search MCP): expected_output "community-maintained (not first-party from Brave)" is **now false** — reference `server-brave-search` archived, "replaced by the official server, `@brave/brave-search-mcp-server`" (servers README). Assertions (CONDITIONAL|APPROVED, API-key concern) still pass either way, but model-grader context and the case's teaching value are wrong.
- **Eval 23** (Discord-shared unknown server w/ API keys → REJECTED): still valid; could add `npx -y` unpinned + config-hijack angle.
- **Coverage gap:** 3/3 cases are 8a stdio. Zero 8b, zero 8c, zero remote Streamable HTTP/OAuth, zero tool-poisoning/rug-pull, zero repo-borne `.mcp.json`/hooks. `validate`'s ≥3/workflow invariant masks sub-rubric coverage.

## 6. Evidence Log

| # | Finding | Source | Type | Conf | Notes |
|---|---|---|---|---|---|
| E1 | Rubric assumes MCP manifest; SSE peer transport; 8a behavioral N/A | `workflows/agent-extension.md:35,144,187`; `references/criteria/agent-extension.md:59-65,87` | Primary | H | Direct read |
| E2 | 8b = commands+hooks+settings, in-process; `claude-code/plugins/*` | `workflows/agent-extension.md:36-37,146,157`; `references/classifier.md:89` | Primary | H | |
| E3 | "SYSTEM_PROMPT" term; 8c behavioral-only | `workflows/agent-extension.md:159,175,191` | Primary | H | |
| E4 | Tier contradictions (localhost HTTP; fs-write vs eval 22) | `references/criteria/agent-extension.md:99,110,119`; `evals/evals.json` id 22 | Primary | H | |
| E5 | Coverage table lacks CVE/typosquat/license rows | `workflows/agent-extension.md:117-130` vs `references/criteria.md` rows table | Primary | H | |
| E6 | Eval run offline: validate ✓, prepare ✓, 0 graded | `python3 evals/run_evals.py validate|prepare|grade|summary` | Primary | H | Live run not approved |
| E7 | MCP 2026-07-28: stateless, SSE deprecated, OAuth tightening, Roots/Sampling/Logging deprecated | [spec changelog (GitHub raw)](https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/docs/specification/2026-07-28/changelog.mdx) | Tertiary (primary-spec) | H | modelcontextprotocol.io DNS-blocked via proxy; read repo source |
| E8 | Plugin components incl. monitors, `bin/`, `.mcpb` URLs, userConfig, deps, reserved names | [plugins-reference](https://code.claude.com/docs/en/plugins-reference) | Tertiary (vendor doc) | H | |
| E9 | Marketplace sources (github/url/git-subdir/npm/archive/command), reserved official names, policy keys | [marketplace-reference](https://code.claude.com/docs/en/plugins/marketplace-reference) | Tertiary (vendor doc) | H | |
| E10 | Skill `allowed-tools` not trust-gated; `!` shell injection; skill hooks; controls; Agent Skills standard | [skills](https://code.claude.com/docs/en/skills) | Tertiary (vendor doc) | H | |
| E11 | SSE deprecated in Claude Code; project servers auto-load in `-p`/SDK/cloud; managed MCP lists | [mcp](https://code.claude.com/docs/en/mcp) | Tertiary (vendor doc) | H | |
| E12 | MCP donated to AAIF/LF, Dec 9 2025 | [Anthropic announcement](https://anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation) | Tertiary | H | |
| E13 | Reference servers: "educational examples", steering-group maintained; Brave archived → official `@brave/brave-search-mcp-server` | [servers README](https://raw.githubusercontent.com/modelcontextprotocol/servers/main/README.md) | Tertiary (primary repo) | H | |
| E14 | Filesystem server CVE-2025-53109/53110, fix 2025.7.1 (version discrepancy) | [GitLab advisory](https://advisories.gitlab.com/pkg/npm/@modelcontextprotocol/server-filesystem/CVE-2025-53109/) ; OSV | Tertiary | H (CVE) / M (fix ver) | |
| E15 | mcp-server-git CVE-2025-68143/4/5, CVE-2026-27735 | [The Hacker News](https://thehackernews.com/2026/01/three-flaws-in-anthropic-mcp-git-server.html); vulners | Tertiary | M-H | Fix versions vary |
| E16 | Claude Code CVE-2025-59536, CVE-2026-21852 (Check Point) | [action1](https://www.action1.com/vulnerabilities/cve-2026-21852/); secondary coverage | Tertiary | M | Fixed versions inconsistent across sources |
| E17 | Official MCP Registry preview; namespace verification; no scanning | Search results citing `modelcontextprotocol.io/registry/about` (DNS-blocked) | Tertiary | M | Not fetched directly |
| E18 | ClawHavoc, skill-scanner bypass (Trail of Bits; SkillCloak), OWASP Agentic Skills Top 10 | [CSA bypass note](https://labs.cloudsecurityalliance.org/research/csa-research-note-ai-agent-skill-scanner-bypass-20260610-csa/); [CSA SkillCloak](https://labs.cloudsecurityalliance.org/research/csa-research-note-skillcloak-agent-skill-evasion-20260706-cs/); [OWASP AST01](https://owasp.org/www-project-agentic-skills-top-10/ast01.html) | Tertiary | M | Counts disagree |
| E19 | Plugin dependency-hijack skill (Jan 2026) | [SentinelOne/Prompt Security](https://www.sentinelone.com/blog/marketplace-skills-and-dependency-hijack-in-claude-code) | Tertiary | M | Not fetched; from search summary |
| E20 | Tool poisoning / rug pull; OWASP MCP Top 10 (beta, numbering unsettled) | [CSA tool poisoning](https://labs.cloudsecurityalliance.org/research/csa-research-note-mcp-tool-poisoning-ai-agent-exfiltration-2/) | Tertiary | M | |
| E21 | Smithery hosting path traversal (Jun 2025) | [SC World](https://scworld.com/news/smithery-ai-fixes-path-traversal-flaw-that-exposed-3000-mcp-servers) | Tertiary | M-H | |
| E22 | postmark-mcp, SANDWORM_MODE, AgentBaiting | Search summaries (Snyk, vendor blogs) | Tertiary | M-L | Not individually verified |
| E23 | M4.3 plan channel list had no recorded primary research | `2604160900-agent-extension-workflow-m43-plan.md` Problem §4 | Secondary | H | |

## 7. Evaluation Against Criteria

| Criterion | Score | Conf | Rationale |
|---|---|---|---|
| Ecosystem accuracy | Weak | H | All three sub-rubric models materially wrong (5.1, 5.3, 5.5) |
| Threat coverage | Weak | H | Tool poisoning, rug pull, repo-borne auto-load, `allowed-tools`, command sources absent (5.2, 5.5, 5.6) |
| Verdict calibration | Weak | M | Plugins with hooks/monitors under-rated; reference servers over-trusted (5.3, 5.8) |
| Internal consistency | Adequate→Weak | H | Tier trigger overlap; canonical rows missing (5.8) |
| Eval fidelity | Weak | H | 2/3 stale premises; 0 8b/8c cases (5.10) |
| Actionability | Adequate | M | Structure (Identify/Evidence/Rubric/Verdict) sound; capability-risk table reusable |

**Overall:** structure keeps; content needs a sourced rewrite. Not an emergency for 8a stdio audits from known publishers (core logic still yields roughly right verdicts); significant for 8b/8c and remote MCP.

## 8. Challenges and Risks

- **Size pressure (Medium):** adding 8b/8c detail inflates per-audit read cost (F7 finding). Mitigate: move sub-rubric detail into per-sub-type sections or split addendum (`agent-extension-8b.md`?) loaded on demand.
- **Doc churn (High likelihood):** Claude Code plugin/skill docs change weekly (version-gated fields v2.1.2xx). Mitigate: rubric names concepts + checks, links docs, avoids version-specific field minutiae.
- **Cross-subject overlap (Medium):** remote MCP vs remote-integration; npm-sourced plugins vs registry-package — needs coordination with sibling evals/classifier owner.

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Plugin w/ malicious hook APPROVED as "in-process Medium" | Medium | High | 8b rewrite: hooks/monitors/`bin/` = shell = Critical capability |
| Reference server APPROVED on vulnerable version | Medium | High | Mandatory CVE row + version gate; eval 22 rewrite |
| Rewrite overfits to Claude Code, misses Codex/Cursor skill hosts | Medium | Medium | Frame 8c as Agent Skills standard; host-specific addenda notes |
| Rubric goes stale again (cadence unexercised 6 mo) | High | Medium | Orchestrator records review in STEWARDSHIP inventory (step 7) + nav log (step 8) |
| Live evals never run → no regression baseline | High | Medium | Approve one paid `run` for agent-extension after eval refresh |

## 9. Findings

| ID | Finding | Severity | Conf | Plan-projex? |
|---|---|---|---|---|
| F1 | 8b plugin model wrong: omits skills/agents/MCP/LSP/monitors/`bin/`/userConfig/deps; hooks+monitors are shell, not "in-process" | High | H | Yes — P1 |
| F2 | 8b provenance stale: no "usage metrics" marketplace; decentralized catalogs, 7 source types (`command`, `archive`, unpinned `ref`), reserved official names, org policy keys | High | H | Yes — P1 |
| F3 | 8c skill model stale: `allowed-tools` (not trust-gated), `` !`cmd` `` shell, skill hooks, fork, shadowing; Agent Skills cross-harness; "SYSTEM_PROMPT" fictional | High | H | Yes — P1 |
| F4 | 8a model stale vs MCP spec: no static manifest (runtime/mutable tools), HTTP+SSE deprecated, stateless 2026-07-28, OAuth 2.1/CIMD/`iss` checks absent | High | H | Yes — P1 |
| F5 | Threat classes missing: tool poisoning, rug pull, shadowing, indirect injection, config hijack, lethal trifecta; 8a behavioral "N/A" wrong | High | H | Yes — P1 |
| F6 | Channel trust table stale: official MCP Registry, skill marketplaces, MCPB, vendor-first-party tier missing; "Anthropic official" anchor outdated (AAIF; reference servers "educational") | High | H | Yes — P1 |
| F7 | Repo-borne auto-load surfaces (`.mcp.json`, project hooks/env, `.claude/skills/`) + Claude Code trust-bypass CVEs + managed-settings mitigations absent | High | H (surface) / M (CVE versions) | Yes — P1 |
| F8 | Eval 22 stale: "Anthropic-maintained"; directory scoping treated as mitigation despite CVE-2025-53109/53110; exact_match APPROVED penalizes correct version-gated CONDITIONAL | High | H | Yes — P2 |
| F9 | Eval 31 expected_output false: Brave server now first-party (`@brave/brave-search-mcp-server`) | Medium | H | Yes — P2 |
| F10 | Eval coverage: 0 cases for 8b, 8c, remote/OAuth MCP, tool poisoning, repo-borne config | High | H | Yes — P2 |
| F11 | Tier triggers overlap (localhost HTTP; fs-write vs eval 22 Tier 1) | Medium | H | Yes — fold into P1 |
| F12 | Coverage table omits canonical CVE / typosquat-name / license rows (impersonation e.g. reserved plugin names unchecked) | Medium | H | Yes — fold into P1 |
| F13 | Classifier Type-8: npm-sourced marketplace plugins misrouted; remote MCP vs Type 9 ambiguous; stale path/URL signals & host list | Medium | M-H | Yes — P3 (classifier, coordinate w/ dispatcher owner) |
| F14 | Stale URL refs: `docs.anthropic.com` for Claude Code → `code.claude.com/docs`; `claude-code/plugins/*` | Low | H | No — fold into P1/P3 |
| F15 | Step 4 incomplete: no live run → no regression evidence; 60-day cadence missed ~3× | Medium | H | No — needs human approval for paid run + steps 7–8 by orchestrator |

**Opportunities:** reuse capability-risk table as-is (still sound); add "declared vs enforced" principle across sub-types; use Anthropic-reserved marketplace/plugin names as a crisp anti-impersonation signal; managed-settings controls give concrete CONDITIONAL conditions.

## 10. Recommendations

**Primary:** file three plans (checklist steps 5–6), no in-place edits.

- **P1 — `agent-extension-rubric-refresh` plan** (F1–F7, F11, F12, F14): rewrite Identify signals; per-sub-type evidence procedures (8a runtime tool enumeration + description review + version pin; 8b component inventory w/ nested 8a/8c sub-audits + source-pin strength; 8c frontmatter + shell-surface audit); replace transport table (Streamable HTTP, legacy SSE flag, auth mode); rebuild channel table (5.7); add threat-class flags + repo-borne pattern + managed-settings mitigations; disjoint tier triggers w/ reference-server carve-out; restore canonical coverage rows. Keep compact — consider splitting addendum by sub-type.
- **P2 — `agent-extension-eval-refresh` plan** (F8–F10): rewrite eval 22 (version-gated; accept CONDITIONAL|APPROVED or pin version in prompt), fix eval 31 rationale (first-party Brave), add ≥1 8b case (plugin with `SessionStart` hook + unpinned github source), ≥1 8c case (skill w/ broad `allowed-tools` + `!` command), ≥1 remote Streamable-HTTP/OAuth MCP case, ≥1 tool-poisoning or repo-borne `.mcp.json` case. Sequence after P1.
- **P3 — `classifier-type8-signals` plan** (F13): npm-sourced marketplace plugin override; remote-MCP vs remote-integration tie-break; refresh Type-8 signal rows. Coordinate with `2610161927-remote-integration-generic-stewardship-review-eval.md` and the dispatcher owner.

**Conditional:** if read-cost budget forbids growth → split addendum into `agent-extension.md` (shared) + sub-type sections loaded per `Sub-rubric:`. If orchestrator prefers one plan → merge P1+P3, keep P2 separate (eval changes must follow rubric).

**Next steps:** Immediate — orchestrator records this pass in `STEWARDSHIP.md` inventory (Last Reviewed 2026-10-16; Next Due 2026-12-15) + nav Phase 6 log (steps 7–8). Short-term — P1 → P2 → P3. Long-term — after P2, one approved live `run --workflow agent-extension` to establish a baseline; keep 60-day cadence and add an event trigger on each MCP spec revision.

## 11. Open Questions

- [ ] Split agent-extension addendum per sub-type, or keep single file? (read-cost trade-off)
- [ ] Remote MCP server via URL/OAuth: Type 8 (8a-remote) or Type 9? (needs dispatcher decision)
- [ ] Should a vendor-first-party or reference MCP server ever be Tier 1 given CVE history?
- [ ] Exact fixed versions for CVE-2025-59536 / CVE-2026-21852 (sources disagree) — check Anthropic GHSA before citing in rubric
- [ ] Official MCP Registry GA status (docs DNS-blocked here; reported still preview)
- [ ] Include non-Claude hosts (Codex, Cursor, Copilot) explicitly in 8c, or keep host-agnostic wording?
- [ ] Approve a paid live eval run for agent-extension after P2?

## 12. Appendix

**Methodology:** STEWARDSHIP checklist 1 (workflow read end-to-end) → 2 (criteria read; tier check) → 3 (live web: ~15 searches, 6 primary fetches) → 4 offline (`validate`, `prepare --workflow agent-extension`, `grade`, `summary`, unittest). Tier Standard: moderate-high stakes, external evidence needed, no composed projex. Lenses: Constraint Mapping (model vs reality), Inversion (attacker paths), Steel-Manning (eval 22 Tier 1).

**Sources consulted:** see Evidence Log URLs. Blocked: `modelcontextprotocol.io`, `modelcontextprotocol.net` (DNS via proxy); `gh api` to modelcontextprotocol repos (not attached). Worked around via `raw.githubusercontent.com`.

**Dissenting views:** (1) "Rubric is fine for its common case" — most real audits are npm-launched stdio MCP servers from known orgs; 8a core logic (capability risk × provenance) still produces sane verdicts there. Accepted partially → severity of 8a findings High for accuracy, verdict impact Medium. (2) "Don't chase Claude Code doc minutiae" — accepted; P1 should encode concepts (shell-bearing components, pin strength, trust-gating) not version-gated fields.

**Bias check:** reviewer is a Claude model auditing a rubric about Claude Code extensions — risk of over-weighting Claude Code specifics vs other hosts; mitigated by framing 8c on Agent Skills standard. Vendor-blog incident counts treated Medium/Low.

**Process note (out of subject):** `new-projex.sh --projex-dir <absolute path>` created the file under `<repo>/home/user/...` (prefixed absolute path with repo root); file moved manually to `.projex/`.

| Date | Mode | Scope | Summary |
|---|---|---|---|
| 2026-10-16 | Initial | Full | First stewardship pass; 15 findings, 3 plans recommended |
