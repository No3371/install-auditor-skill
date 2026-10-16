# Dispatcher Rubric Consistency — Red Flags, Verdict-Tree Terms, Shipped Classifier Reference

> **Status:** In Progress
> **Author:** Claude (Opus)
> **Parent:** Orchestrator
> **Source:** Direct request (orchestrated: "It's been a while. What can we do to improve this?" → "orchestarte it"; items 3a, 3b, 5, 7a + conflict survey)
> **Related Projex:** 2604070218-install-auditor-subject-typed-redesign-nav.md | 2604070300-install-auditor-subject-type-taxonomy-def.md | 2604082335-dispatcher-refactor-m11-m12-plan.md (origin of `.projex` link-back) | 2604151500-cli-binary-workflow-m42-plan.md (Homebrew boundary) | 2604172000-stewardship-cadence-m63-plan.md (`STEWARDSHIP.md`: rubric changes via plan-projex) | siblings: 2610161849-python-script-ports-plan.md, 2610161850-eval-runner-harness-plan.md
> **Worktree:** Yes

---

## Summary

Dispatcher `SKILL.md` contradicts its own routed workflows and criteria addenda. Its Red Flags (auto-REJECTED) list auto-rejects rootful container images, any name within 1–2 chars of a popular one, and any non-SHA CI ref with secrets. The workflows, addenda, and evals all grade these cases lower (CONDITIONAL/APPROVED). The tree's first node only reaches REJECTED through that 8-item list, so subject-level `Toward REJECTED` findings (e.g. eval 25 phishing OAuth) have no stated path to REJECTED. Step 0 also sends the runtime agent to a `.projex/` planning artifact for the full classifier rule. That file is not part of the shipped skill, and it is stale on the Homebrew boundary. Runtime files also carry roadmap labels ("Phase N / M x.y").

This plan does four things. It rewrites Red Flags to subject-independent, fully conditioned items. It defines the tree's terms (CRITICAL flag, unpatched CVE) and a precedence rule. It promotes the classifier rule into shipped `references/classifier.md`. It strips the history labels.

**Scope:** `SKILL.md` Step 0 + Step N text (Red Flags, tree terms, Reference Files) | new `references/classifier.md` | ci-action workflow + addendum pin wording | header labels in 9 workflows + 2 addenda | taxonomy def pointer + Homebrew fix.
**Estimated Changes:** 14 files (1 new, 13 edited). No scripts, no evals, no report skeleton.

---

## Objective

### Problem / Gap / Need

Verified against the corpus on 2026-10-16:

| # | Conflict | Dispatcher (`SKILL.md`) | Workflow / addendum / evals | Verdict at stake |
|---|---|---|---|---|
| C1 (3a) | Rootful container | Red Flag "Dangerous container defaults — image runs as root with no USER switch, unjustified" → auto-REJECTED | `references/criteria/container-image.md` Layer Risk: `USER root` (or no `USER`) = **Medium-High**. `workflows/container-image.md` §4.4: "Tier 2 flag"; Toward CONDITIONAL: "Rootful image on developer workstation". `references/criteria.md` §4.4: "`USER root` … → flag". Docker Official `nginx` / `redis` Dockerfiles set no `USER` | eval 12 (nginx:latest → CONDITIONAL/APPROVED), eval 26 (redis → APPROVED) |
| C2 (3b) | Typosquat | Red Flag "name differs from legitimate package by 1–2 characters" (no history gate) | `references/criteria.md` §4.1: "Auto-REJECT if ≤2 chars from top-1000 package **with no prior history**". `workflows/registry-package.md` Toward REJECTED: "Confirmed typosquat … **and no established history**". `references/criteria/registry-package.md`: script `critical` → REJECTED unless proven legit; `high` → strong CONDITIONAL; `medium` → investigate. Literal Red Flag rejects legit pairs (`preact`/`react`) | evals 2, 3, 9 (REJECTED or CONDITIONAL), eval 4 (chalk, not REJECTED) |
| C3 | CI pinning | Red Flag "not pinned to commit SHA while accessing secrets" → auto-REJECTED | `workflows/ci-action.md` Toward CONDITIONAL: "Trusted action but tag-pinned instead of SHA-pinned"; Toward REJECTED only for **branch/`main`** pins with privileged access. `references/criteria/ci-action.md` Ref matrix: tag → "reject when paired with secrets, write perms" (agrees with Red Flag, contradicts workflow + eval 27) | eval 27 (`docker/build-push-action@v5` + `packages: write` → **CONDITIONAL**) |
| C4 | Tree bridge | Node 1 "Any CRITICAL red flag? (see Red Flags below)". Nothing else reaches REJECTED except CVE / confirmed compromise | Every workflow lists `Toward REJECTED` items not on the Red Flag list (phishing OAuth link, unknown-registry `cryptominer`, `pull_request_target` + `secrets: inherit`) | evals 13, 15, 17, 19, 21, 23, 25, 34 expect REJECTED |
| C5 | "Unpatched" undefined | Node 2 "Any unpatched CVE (HIGH or CRITICAL severity)? → REJECTED" | `references/criteria.md` §4.3 already defines: HIGH "REJECTED if unpatched; CONDITIONAL if patched in newer version". `workflows/registry-package.md`: REJECTED only "with no fix available"; "Patched CVE exists but user requests old version" → CONDITIONAL | eval 5 (lodash@4.17.20), eval 7 (mkdirp@0.5.1 → minimist HIGH, expects **CONDITIONAL**) |
| C6 | Removal reason | Red Flag "Removed from registry — previously removed from …" (any reason) | `workflows/registry-package.md`: "yanked/removed **for security reasons**". `workflows/browser-extension.md`: "removed … for injecting ads, stealing data, cryptomining" | false REJECTED on author-unpublished / renamed packages |
| C7 (5) | Runtime → `.projex` | Step 0 rule paragraph + Reference Files point at `.projex/2604070300-install-auditor-subject-type-taxonomy-def.md` | `.projex/` is authoring layer (SKILL.md § Source Hygiene rule 1: promote load-bearing rationale into shipped docs). Def is also **stale**: routes "CLI via Homebrew core → desktop-app", but M4.1/M4.2 decided `brew install <formula>` → cli-binary (`workflows/cli-binary.md` lines 4, 42). Def §9 "split audit" contradicts its own edge-case rule "never split at classification" | classifier correctness when shipped without `.projex/` (eval 20 `brew install ripgrep`) |
| C8 (7a) | History labels | Reference Files: 9 × "(Phase N, Mx.y)" | 9 workflow header comments "Phase N / Mx.y — nth subject-specific workflow…"; `workflows/ci-action.md` + `references/criteria/ci-action.md` "milestone scope"; `references/criteria/remote-integration.md` comment "Phase 4 / M4.4" | noise for the runtime agent |

**Orchestrator claim corrected:** `workflows/generic.md` "Phase 1–4" headings are its **runtime procedure steps** (Probe → Clarify → Defensive Audit → Warning), not roadmap labels. They stay.

### Success Criteria

- [ ] SC1: `SKILL.md` Red Flags contains no container-root item; contains "Confirmed typosquat / impersonation" (history-gated, script-level aware), "Removed for cause", "Mutable CI ref with privileged access" (branch/unknown ref or unverified publisher; tag-pinned verified → CONDITIONAL)
- [ ] SC2: `SKILL.md` Step N has a "Tree terms & precedence" block defining CRITICAL flag (Red Flag OR auditor-rated CRITICAL under routed workflow), unpatched CVE (← `references/criteria.md` §4.3), and precedence (Red Flags floor; routed workflow/addendum win for subject-specific patterns)
- [ ] SC3: `references/criteria/ci-action.md` tag-ref row + scoring bullet and `workflows/ci-action.md` Toward REJECTED agree with the new CI Red Flag. Eval 27 traces to CONDITIONAL, eval 15 to REJECTED
- [ ] SC4: `references/classifier.md` exists. It holds the rule, tie-breaking, confidence examples, Type 8 sub-rubric, routing overrides (Homebrew formula → cli-binary, cask → desktop-app), extended signal table, 5 worked hybrid examples, and edge-case discipline. It has no `.projex`/Phase/milestone references
- [ ] SC5: `grep -rn '\.projex' SKILL.md workflows references scripts` → 0 hits
- [ ] SC6: `grep -rnE 'Phase [0-9] / M|\(Phase [0-9], M|milestone' SKILL.md workflows references` → 0 hits. `workflows/generic.md` Phase 1–4 headings unchanged
- [ ] SC7: every backticked path in `SKILL.md` § Reference Files exists on disk
- [ ] SC8: taxonomy def points to `references/classifier.md` as the runtime-canonical rule. Its Homebrew routing is corrected and the Homebrew Open Question is resolved
- [ ] SC9: desk-check table (Verification Plan) passes for evals 2, 3, 4, 5, 7, 9, 12, 13, 15, 20, 25, 26, 27, 30. No traced verdict contradicts its eval assertion
- [ ] SC10: `evals/evals.json`, `scripts/*`, `STEWARDSHIP.md`, report skeleton, and frontmatter `description` are byte-unchanged (`git diff --stat` shows none of them)

### Out of Scope

- Eval runner (sibling plan) | PowerShell-script portability (sibling plan)
- Dispatcher size compression / moving the report skeleton out of `SKILL.md` / frontmatter `description` trigger tuning / report output location (later plan). This plan edits only Step 0 rule paragraph + cli-binary signal row, the tree's first two nodes + new terms block, Red Flags, and Reference Files.
- New eval cases (e.g. `preact` typosquat false-positive, tag-pinned verified action with secrets). These are deferred to avoid colliding with the eval-runner plan's possible `evals.json` changes. Recommended follow-up.
- Container-internal tensions found during survey (follow-up for the container-image stewardship review): (a) addendum "critical-risk runtime flag on an unverified image = HIGH flag" vs workflow "`--privileged` on unverified image → near-automatic rejection"; (b) workflow Toward CONDITIONAL "Rootful image on developer workstation" vs eval 26 (redis dev → APPROVED); (c) Toward APPROVED "high CVEs … pending a patch" vs `references/criteria.md` §4.3 "HIGH: REJECTED if unpatched". The precedence rule in Step 2 makes the workflow's documented allowance authoritative; tightening it is a rubric decision.
- `workflows/cli-binary.md` Toward REJECTED "Project abandoned" vs tree node "Abandoned with no alternative → CONDITIONAL". This is left as judgment, because the bridge stays auditor-rated (see Step 2 rationale). Follow-up for the cli-binary stewardship review.
- Nav doc / `STEWARDSHIP.md` date updates. close-projex records the nav revision-log entry.

---

## Context

### Current State

- `SKILL.md` (243 lines). Step 0 (lines 24–81): rule paragraph line 26 links to the `.projex` def; signal table lines 40–53; output shape. Step N (lines 91–242): tree lines 95–109; coverage-gaps; report skeleton lines 115–190; Escalation; Red Flags lines 196–205; Behavioral Principles; Reference Files lines 217–242.
- The Red Flags list predates the subject workflows. It was carried over from the monolith in dispatcher refactor `2604082335-dispatcher-refactor-m11-m12-plan.md`, and "Dangerous container defaults" was added before the container-image workflow (M3.2) existed. Subject addenda later graded the same patterns more finely, but nobody reconciled the dispatcher.
- Addenda already claim precedence over the shared rubric ("When guidance here conflicts with the shared rubric, the more specific … guidance wins" — `references/criteria/ci-action.md` line 5, `workflows/ci-action.md` line 29, `references/criteria/remote-integration.md` line 2). No rule covers dispatcher text vs addendum.
- The taxonomy def's Classifier Rule section (lines 151–281) holds the rule, the 6-step procedure, a full signal table, confidence examples, Type 8 sub-rubric criteria, 5 worked examples, edge-case discipline, and an escalation path (authoring-only). Per-type "Routes elsewhere" lists sit in §§1–9 (lines 49–147).
- No eval asserts on the `.projex` path or on Red Flag wording (`grep projex evals/evals.json` → 0).

### Key Files

| File | Role | Change Summary |
|------|------|----------------|
| `references/classifier.md` | NEW shipped classifier reference | Promoted rule + overrides + signals + examples + discipline |
| `SKILL.md` | Dispatcher | Step 0 pointer + cli-binary signal; tree nodes 1–2 + terms block; Red Flags rewrite; Reference Files relabel |
| `workflows/ci-action.md` | Type 5 workflow | +1 Toward REJECTED bullet; drop "milestone scope"; drop header label |
| `references/criteria/ci-action.md` | Type 5 addendum | Tag-ref row + scoring bullet aligned; drop "milestone scope" |
| `references/criteria/remote-integration.md` | Type 9 addendum | Drop "Phase 4 / M4.4." from header comment |
| `workflows/{registry-package,browser-extension,container-image,ide-plugin,desktop-app,cli-binary,agent-extension,remote-integration}.md` | Workflows | Drop header-comment history line |
| `.projex/2604070300-install-auditor-subject-type-taxonomy-def.md` | Taxonomy definition | Runtime-canonical pointer; Homebrew fix; Open Question resolved; revision log |

### Dependencies

- **Requires:** none. Base `claude/youthful-dijkstra-5ov1kt` at `428e70e` or later.
- **Blocks:** later dispatcher-compression plan. It must carry the new Red Flags / terms block / Reference Files text forward verbatim when it relocates content.

### Constraints

- `STEWARDSHIP.md`: rubric changes go through plan-projex. This plan is that vehicle.
- Report skeleton (`SKILL.md` lines 115–190) is load-bearing for evals (`## Audit Coverage`, `Audit confidence`). Do not touch it.
- Source Hygiene (SKILL.md of projex framework) rule 1: shipped files carry no projex IDs/filenames. Applies to `SKILL.md`, `workflows/`, and `references/`. The taxonomy def (inside `.projex/`) may reference shipped files.
- Box-drawing tree in `SKILL.md` stays a fenced code block; arrows end in `► VERDICT`.
- No PowerShell on the execution host; verification uses `grep`/`python3` only.

### Assumptions

- Docker Official `nginx` and `redis` images declare no `USER` instruction (nginx master runs as root; redis drops privileges through `gosu` in its entrypoint). If wrong, C1 still stands on the rubric-text contradiction alone.
- The runtime agent rates findings itself. "Rated CRITICAL by the auditor under the routed workflow" is an acceptable bridge, so no mechanical `Toward REJECTED` → CRITICAL mapping is required (see Step 2 rationale).
- The sibling eval-runner plan does not edit `SKILL.md` Step N text. The PS-portability plan may edit the `scripts/registry-lookup.ps1` Reference Files line (line 241). This plan does not touch line 241, so a serial rebase stays conflict-free.

### Impact Analysis

- **Direct:** files in Key Files.
- **Adjacent:** `references/criteria.md` §4.1/§4.3/§4.4 (unchanged; now cited by the tree terms). `references/criteria/registry-package.md` typosquat + CVE tables (unchanged; now cited by the Red Flag). `workflows/generic.md` (unchanged; reaches Step N like every workflow).
- **Downstream:** all 41 evals read the dispatcher. The desk-check covers every case whose verdict a changed rule can move. Read cost: `SKILL.md` grows by ~1 KB net. `references/classifier.md` (~6 KB) is read only on unclear classification, the same trigger as today's def read (~25 KB), so read cost falls on that path.

---

## Implementation

### Overview

1. Promote the classifier rule into a shipped reference.
2. Repoint Step 0, add the Homebrew-formula signal, and relabel Reference Files.
3. Rewrite the Step N tree nodes, add the terms/precedence block, and rewrite Red Flags.
4. Align the ci-action workflow and addendum.
5. Strip history labels.
6. Update the taxonomy def.

Order: 1 before 2 (the pointer target must exist). Step 3 before 4 (the addendum quotes the Red Flag). Steps 5 and 6 are independent.

---

### Step 1: Create `references/classifier.md`

**Objective:** Shipped, runtime-canonical copy of the classifier rule. It replaces the `.projex` dependency and fixes the stale Homebrew and split-audit statements.
**Confidence:** High
**Depends on:** None
**Do-Projex:** Encouraged

**Files:**
- `references/classifier.md` (new)

**Changes:** create the file with exactly this content:

````markdown
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

- **8a · MCP server** — standalone process / binary / script advertising MCP
  tools, referenced from an MCP config (`.mcp.json`, Claude Desktop config)
- **8b · Claude Code plugin** — plugin bundle (`plugin.json` + commands /
  hooks / agents) distributed for Claude Code
- **8c · Claude Code skill** — directory containing `SKILL.md` (plus optional
  `scripts/`, `references/`, `evals/`)

## Routing Overrides

| Subject | Routes to | Why |
|---|---|---|
| Registry package whose `bin` ships a CLI (`prettier`, `typescript`) | registry-package | Registry publish is the gate; the CLI is downstream |
| Package consumed only as a transitive dependency | registry-package (parent audit's transitive surface) | Not a separate install |
| Electron / desktop app shipped through npm | registry-package | Innermost gate is the registry |
| Claude Code skill or plugin distributed via npm | registry-package | `npm install` is the gate; skill content is reviewed inside the registry-package audit |
| Browser extension that wraps a CLI binary | browser-extension | The store is the install pipe |
| VS Code extension wrapping a binary (`rust-analyzer`) | ide-plugin | Marketplace is the verification layer |
| MCP server installed via a VS Code extension | ide-plugin | Marketplace is innermost; the MCP server is downstream |
| Claude Code plugin or skill installed directly | agent-extension | Distinct boundary from IDE marketplaces |
| Container image whose entrypoint is an npm app | container-image | The registry pull is the gate; npm review is a sub-step |
| GitHub Action that pulls a container image | ci-action | The `uses:` reference is the install surface |
| CLI via Homebrew core (`brew install <formula>`) | cli-binary | Formula review + checksum + build-from-source; casks route to desktop-app |
| App via Homebrew cask (`brew install --cask`) | desktop-app | Cask installs a packaged application |
| SaaS that also installs a local agent | The component this request installs or connects | Classify one primary boundary; name the other component in the report and recommend a separate audit (one report per installable) |

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
| 7 | cli-binary | `curl … \| sh`, `wget … \| bash`, GitHub Releases binary, `brew install <formula>` (Homebrew core), version managers (nvm / pyenv / rustup / volta), direct executable URL, checksum / signature file beside a binary | `github.com/*/releases/download/*`, `formulae.brew.sh/formula/*`, `get.<vendor>.sh`-style install scripts, vendor-hosted binary URLs |
| 8 | agent-extension | MCP server manifest / stdio spec; Claude Code plugin bundle; Claude Code skill with `SKILL.md`; agent host context (Cursor, Cline, Continue) | `.mcp.json` entries, `.claude/skills/*`, `claude-code/plugins/*`, `modelcontextprotocol.io/*`, `mcp.so/*` |
| 9 | remote-integration | OAuth flow, API key exchange, webhook endpoint, "Connect to <service>", no local code install | Vendor OAuth URLs, `hooks.slack.com/*`, vendor integrations pages, `api.*.com/*` key-exchange endpoints |
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
5. **Claude Code skill distributed via npm** → **registry-package**, high. If the
   skill content is the main concern, the registry-package audit may apply
   agent-extension 8c signals as a sub-rubric.

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
````

**Rationale:** The def section mixes runtime rule with authoring history (milestones, escalation path, Q-numbers), so a verbatim copy would import noise and stale claims. This file keeps every runtime-relevant statement. The Homebrew override is corrected per `workflows/cli-binary.md` lines 4/42 and `workflows/desktop-app.md` line 42. The def's §9 "split audit" is replaced with its own edge-case rule plus Behavioral Principle 5 ("One report per installable"). The extended signal table keeps URL patterns that Step 0's summary omits (`rubygems.org`, `pkg.go.dev`, `artifacthub.io`, `.mcp.json`, `.claude/skills/*`, …), so the runtime agent loses nothing it previously reached through the def.

**Verification:** File exists. `grep -cE '\.projex|Phase [0-9]|M[0-9]\.[0-9]|milestone' references/classifier.md` → `0`. `grep -c 'brew install <formula>' references/classifier.md` → ≥2. Five numbered worked examples present.

**If this fails:** `git rm --cached` / delete `references/classifier.md`; nothing else depends on it until Step 2.

---

### Step 2: `SKILL.md` — Step 0 pointer, cli-binary signal, tree terms, Red Flags, Reference Files

**Objective:** Remove the `.projex` runtime dependency. Make the tree's first two nodes well-defined. State precedence. Rewrite Red Flags to subject-independent, fully conditioned items. Strip history labels from Reference Files.
**Confidence:** High (C1, C2, C6, C7, C8) | Medium (C3/C4/C5 wording — semantic but aligned with existing addendum text)
**Depends on:** Step 1
**Verify-Projex:** Encouraged (verdict-semantics change; desk-check in Verification Plan)

**Files:**
- `SKILL.md`

**Changes:**

**2a — Step 0 rule paragraph (line 26):**

```markdown
// Before:
**Rule:** classify by the **innermost trust boundary the user is crossing** — the last verification gate between the user and the code that will actually execute. Full rule, worked hybrid examples, and edge-case discipline live in `.projex/2604070300-install-auditor-subject-type-taxonomy-def.md` under "Classifier Rule — Innermost Trust Boundary". Read that section when the rule does not resolve cleanly on its own.

// After:
**Rule:** classify by the **innermost trust boundary the user is crossing** — the last verification gate between the user and the code that will actually execute. Full rule, routing overrides, extended signals, worked hybrid examples, and edge-case discipline live in `references/classifier.md`. Read it when the rule does not resolve cleanly on its own.
```

**2b — signal table row 7 (line 50):**

```markdown
// Before:
| 7 | cli-binary | `curl … \| sh`, GitHub Releases binary, nvm/pyenv/rustup, vendor-hosted executable URLs |

// After:
| 7 | cli-binary | `curl … \| sh`, GitHub Releases binary, `brew install <formula>` (Homebrew core; `--cask` → desktop-app), nvm/pyenv/rustup, vendor-hosted executable URLs |
```

**2c — verdict tree nodes 1–2 (lines 96–98) + new terms block inserted after the tree's closing fence (line 109) and before `**CONDITIONAL** means …` (line 111):**

````markdown
// Before (inside the tree fence):
Any CRITICAL red flag? (see Red Flags below) ───────► REJECTED ❌
  │ No
Any unpatched CVE (HIGH or CRITICAL severity)? ────► REJECTED ❌

// After (inside the tree fence):
Any CRITICAL flag? (see Tree terms below) ──────────► REJECTED ❌
  │ No
Any unpatched HIGH/CRITICAL CVE? (see Tree terms) ──► REJECTED ❌
````

Insert immediately after the closing ```` ``` ```` of the tree and before the `**CONDITIONAL** means` paragraph:

```markdown
**Tree terms & precedence:**

- **CRITICAL flag** — any Red Flag below, **or** a finding the auditor rates CRITICAL using the routed workflow's addendum and its `Toward REJECTED` notes. Record each rating and its reason in the report's Risk Flags so the verdict is traceable.
- **Unpatched CVE** — affects the version to be installed **and** no fixed release exists (`references/criteria.md` §4.3 CVE Severity Mapping). A CVE fixed in a newer release does not trigger this node; rate it per the routed workflow (typically HIGH → CONDITIONAL with an upgrade condition).
- **Precedence** — Red Flags are subject-independent and are never downgraded. For subject-specific patterns (Dockerfile instructions, ref pinning, permission scopes, documented exceptions) the routed workflow and its criteria addendum win over generic wording here or in `references/criteria.md`.
```

**2d — Red Flags block (lines 196–205):**

```markdown
// Before:
### Red Flags — Automatic REJECTED

- **Typosquatting** — name differs from legitimate package by 1–2 characters
- **Brand new + no history** — published < 72 hours ago with no prior versions
- **Removed from registry** — previously removed from Chrome Web Store, npm, PyPI, etc.
- **Confirmed supply chain attack** — security blog or advisory confirms compromise
- **Excessive permissions** — browser extension reads all history/cookies/clipboard with no justification
- **Dangerous container defaults** — image runs as root with no USER switch, unjustified
- **Unpinned CI action with secrets access** — not pinned to commit SHA while accessing secrets
- **Known malware** — confirmed cryptominer, credential stealer, or data exfiltration

// After:
### Red Flags — Automatic REJECTED

Subject-independent. Each applies only when its full condition holds; partial matches are rated by the routed workflow, not auto-rejected.

- **Confirmed typosquat / impersonation** — name, scope, or namespace imitates a legitimate subject (edit distance ≤2 from a top-1000 package, combosquat, homoglyph, or namespace impersonation such as `someuser/nginx` vs official `nginx`) **and** the subject has no independent legitimate history. For npm, a `typosquat-check` script result of `riskLevel: critical` qualifies unless legitimacy is affirmatively proven. Similarity alone (script `high`/`medium`, or a name merely close to a popular one) is a HIGH/MEDIUM flag per `references/criteria/registry-package.md`.
- **Brand new + no history** — published < 72 hours ago with no prior versions
- **Removed for cause** — previously removed from Chrome Web Store, npm, PyPI, etc. for malicious behavior, compromise, or a security-policy violation (not author unpublish, rename, or naming dispute)
- **Confirmed supply chain attack** — security blog or advisory confirms compromise
- **Excessive permissions** — browser extension reads all history/cookies/clipboard with no justification
- **Mutable CI ref with privileged access** — action or reusable workflow referenced by branch, default branch, or unknown ref — or by any non-SHA ref from an unverified third-party publisher — in a job holding secrets, a write-scoped token, `id-token: write`, or publish rights. Tag-pinned actions from official/verified publishers are HIGH → CONDITIONAL (pin to SHA) per `workflows/ci-action.md`.
- **Known malware** — confirmed cryptominer, credential stealer, or data exfiltration
```

**2e — Reference Files (lines 220–228, 242):** strip history parentheticals; replace the `.projex` entry.

```markdown
// Before:
- `workflows/registry-package.md` — Type 1 registry-package workflow (Phase 2, M2.1)
- `workflows/browser-extension.md` — Type 2 browser-extension workflow (Phase 3, M3.1)
- `workflows/container-image.md` — Type 4 container-image workflow (Phase 3, M3.2)
- `workflows/ci-action.md` — Type 5 ci-action workflow (Phase 3, M3.3)
- `workflows/ide-plugin.md` — Type 3 ide-plugin workflow (Phase 3, M3.4)
- `workflows/desktop-app.md` — Type 6 desktop-app workflow (Phase 4, M4.1)
- `workflows/cli-binary.md` — Type 7 cli-binary workflow (Phase 4, M4.2)
- `workflows/agent-extension.md` — Type 8 agent-extension workflow (Phase 4, M4.3)
- `workflows/remote-integration.md` — Type 9 remote-integration workflow (Phase 4, M4.4)
...
- `.projex/2604070300-install-auditor-subject-type-taxonomy-def.md` — Locked 10-type taxonomy + full Classifier Rule

// After:
- `workflows/registry-package.md` — Type 1 registry-package workflow
- `workflows/browser-extension.md` — Type 2 browser-extension workflow
- `workflows/container-image.md` — Type 4 container-image workflow
- `workflows/ci-action.md` — Type 5 ci-action workflow
- `workflows/ide-plugin.md` — Type 3 ide-plugin workflow
- `workflows/desktop-app.md` — Type 6 desktop-app workflow
- `workflows/cli-binary.md` — Type 7 cli-binary workflow
- `workflows/agent-extension.md` — Type 8 agent-extension workflow
- `workflows/remote-integration.md` — Type 9 remote-integration workflow
...
- `references/classifier.md` — Full classifier rule: tie-breaking, routing overrides, extended signals, worked hybrid examples, edge-case discipline
```

(`...` = lines 229–241 unchanged, including the `scripts/registry-lookup.ps1` line.)

**Rationale:**
- *C1:* the container-root item is dropped, not reworded. Every container-runtime pattern is already graded in `references/criteria/container-image.md`, and precedence now makes that grading authoritative. A reworded "privileged + unverified" Red Flag would add a third, conflicting grade (the addendum says HIGH, the workflow says near-automatic REJECTED). That tension is listed in Out of Scope.
- *C2:* the new wording is the union of `references/criteria.md` §4.1 (history gate) and the addendum's script-level table. It is not new policy.
- *C3:* the new wording matches the workflow's own split (branch → REJECTED, tag + trusted → CONDITIONAL) and eval 27. The unverified-publisher clause keeps eval 15 at REJECTED and matches the addendum Tier 3 trigger "Unverified third-party action with secrets or write permissions".
- *C4:* the bridge is **auditor-rated**, not a mechanical "every `Toward REJECTED` item = CRITICAL". The mechanical form was rejected: `Toward REJECTED` lists overlap with `Toward CONDITIONAL` lists. Eval 30 (terraform copied to a shared drive) matches cli-binary's "Binary from third-party mirror" (Toward REJECTED) and also "legitimate but distributed via informal channel" (Toward CONDITIONAL), and expects CONDITIONAL. A mechanical bridge would flip it to REJECTED.
- *C5:* the definition is cited from `references/criteria.md` §4.3. It is not restated as new policy, which keeps one source.
- *C6:* scoped to match the workflows' "for security reasons" wording.
- Tree arrow lines are re-padded so `►` stays visually aligned. This is cosmetic, and the exact dash count is not load-bearing.

**Verification:**
- `grep -c 'Dangerous container defaults\|Unpinned CI action with secrets' SKILL.md` → `0`
- `grep -c 'Confirmed typosquat / impersonation\|Removed for cause\|Mutable CI ref with privileged access\|Tree terms & precedence' SKILL.md` → `4`
- `grep -c '\.projex' SKILL.md` → `0`; `grep -cE '\(Phase [0-9], M' SKILL.md` → `0`
- `sed -n '/^## Step N/,/^### Report Skeleton/p' SKILL.md` shows the tree fence intact (opening and closing ```` ``` ````), with the terms block outside the fence
- Report skeleton region unchanged: `git diff -U0 SKILL.md | grep -E '^[-+]' | grep -E 'Install Audit:|## Audit Coverage|Audit confidence'` → no output

**If this fails:** `git checkout -- SKILL.md` and reapply sub-edits 2a–2e one at a time.

---

### Step 3: Align ci-action workflow + addendum with the CI Red Flag

**Objective:** One consistent pin rule across dispatcher, workflow, and addendum.
**Confidence:** High
**Depends on:** Step 2 (quotes the Red Flag)
**Do-Projex:** Encouraged

**Files:**
- `workflows/ci-action.md`
- `references/criteria/ci-action.md`

**Changes:**

`workflows/ci-action.md` — Toward REJECTED (lines 202–203), append one bullet:

```markdown
// Before:
- Branch or `main` pin on an action with write scopes, OIDC, package publish,
  or secret access
- Unknown transitive child introduced by composite or reusable workflow

// After:
- Branch or `main` pin on an action with write scopes, OIDC, package publish,
  or secret access
- Non-SHA ref from an unverified third-party publisher with write scopes,
  OIDC, package publish, or secret access
- Unknown transitive child introduced by composite or reusable workflow
```

`references/criteria/ci-action.md` — Ref Immutability Matrix (line 35):

```markdown
// Before:
| Release tag (`v4`, `v1.2.3`) | Mutable | Usually CONDITIONAL; reject when paired with secrets, write perms, or untrusted code paths |

// After:
| Release tag (`v4`, `v1.2.3`) | Mutable | CONDITIONAL from official/verified publishers (condition: pin to SHA); reject when the publisher is unverified and the job holds secrets, write perms, OIDC, or publish rights, or on untrusted code paths |
```

`references/criteria/ci-action.md` — Ref scoring impact (line 45):

```markdown
// Before:
- Secret-bearing or write-capable third-party code not pinned to SHA = high-risk finding

// After:
- Secret-bearing or write-capable code not pinned to SHA = HIGH finding (official/verified publisher, tag ref) | CRITICAL (branch/unknown ref, or unverified third-party publisher — `SKILL.md` Red Flags)
```

**Rationale:** The workflow already distinguishes branch pins (REJECTED) from trusted tag pins (CONDITIONAL). Only the unverified-publisher case was missing. The addendum's tag row was the stricter outlier and contradicted eval 27 (`docker/build-push-action@v5`, verified publisher, `packages: write` → CONDITIONAL).

**Verification:** `grep -n 'unverified third-party publisher' workflows/ci-action.md references/criteria/ci-action.md SKILL.md` → ≥1 hit in each file. Eval 27 / 15 / 14 traces in the desk-check.

**If this fails:** `git checkout -- workflows/ci-action.md references/criteria/ci-action.md`.

---

### Step 4: Strip project-history labels from runtime files

**Objective:** Remove roadmap noise ("Phase N / Mx.y", "milestone scope") from shipped files.
**Confidence:** High
**Depends on:** None (Step 3 also edits `workflows/ci-action.md`; apply Step 3 first or re-read the file)
**Do-Projex:** Encouraged

**Files and exact edits** (each removes the blank line before the label and the label line itself, so the comment closes right after the preceding paragraph):

| File | Remove (exact line) |
|---|---|
| `workflows/registry-package.md` | `Phase 2 / M2.1 — first subject-specific workflow.` |
| `workflows/browser-extension.md` | `Phase 3 / M3.1 — second subject-specific workflow (first Phase 3).` |
| `workflows/container-image.md` | `Phase 3 / M3.2 — third subject-specific workflow (second Phase 3).` |
| `workflows/ci-action.md` | `Phase 3 / M3.3 - fourth subject-specific workflow (third Phase 3).` |
| `workflows/ide-plugin.md` | `Phase 3 / M3.4 - fifth subject-specific workflow (fourth Phase 3).` |
| `workflows/desktop-app.md` | `Phase 4 / M4.1 — sixth subject-specific workflow (first Phase 4).` |
| `workflows/cli-binary.md` | `Phase 4 / M4.2 — seventh subject-specific workflow (second Phase 4).` |
| `workflows/agent-extension.md` | `Phase 4 / M4.3 — eighth subject-specific workflow (third Phase 4).` |
| `workflows/remote-integration.md` | `Phase 4 / M4.4 — ninth subject-specific workflow (fourth Phase 4).` |

Example (`workflows/registry-package.md`, lines 9–13):

```markdown
// Before:
tree and report shape. The Audit Coverage table and audit-confidence
assertion are owned by the dispatcher — do not duplicate them here.

Phase 2 / M2.1 — first subject-specific workflow.
-->

// After:
tree and report shape. The Audit Coverage table and audit-confidence
assertion are owned by the dispatcher — do not duplicate them here.
-->
```

Prose edits:

```markdown
// workflows/ci-action.md lines 18–20 — Before:
CI-imported automation referenced from pipeline config. Primary depth in
v1 is GitHub Actions / reusable workflows because the repo's trust
references and milestone scope are GitHub-first.
// After:
CI-imported automation referenced from pipeline config. Primary depth in
v1 is GitHub Actions / reusable workflows.

// references/criteria/ci-action.md lines 9–10 — Before:
orbs, and equivalent CI-imported automation. Depth is GitHub Actions-first
in v1 because the repo's current refs and milestone scope are GitHub-heavy.
// After:
orbs, and equivalent CI-imported automation. Depth is GitHub Actions-first
in v1.

// references/criteria/remote-integration.md lines 1–3 — Before:
<!-- Remote-integration criteria addendum. Supplements references/criteria.md
     for Type 9 subjects. When guidance here conflicts with the shared rubric,
     this more-specific addendum wins. Phase 4 / M4.4. -->
// After:
<!-- Remote-integration criteria addendum. Supplements references/criteria.md
     for Type 9 subjects. When guidance here conflicts with the shared rubric,
     this more-specific addendum wins. -->
```

**Not edited:** `workflows/generic.md` "## Phase 1 — Subject Probe" … "## Phase 4 — Low-Confidence Warning" and "After completing Phases 1-4". These are runtime procedure steps, not roadmap labels.

**Rationale:** The labels encode roadmap position, which means nothing to a runtime agent and goes stale as the nav evolves. The "milestone scope" clauses justify scope by project history; dropping the "because" keeps the scope statement and loses nothing.

**Verification:** `grep -rnE 'Phase [0-9] / M|\(Phase [0-9], M|milestone' SKILL.md workflows references` → no output. `grep -c '^## Phase' workflows/generic.md` → `4`. Each edited workflow's first `-->` still closes the opening `<!--` (`python3 -c` check in Verification Plan).

**If this fails:** `git checkout --` the offending file and redo its single edit.

---

### Step 5: Update taxonomy def — runtime pointer, Homebrew fix

**Objective:** Prevent dual-source drift. The def becomes the design record and points to the shipped canonical rule. Fix the stale Homebrew routing.
**Confidence:** High
**Depends on:** Step 1
**Do-Projex:** Encouraged

**Files:**
- `.projex/2604070300-install-auditor-subject-type-taxonomy-def.md`

**Changes:**

Header line 3:

```markdown
// Before:
> **Created:** 2026-04-07 | **Last Revised:** 2026-04-08
// After:
> **Created:** 2026-04-07 | **Last Revised:** 2026-10-16
```

§6 Includes (line 104):

```markdown
// Before:
- **Includes:** Signed and unsigned installers, store and non-store distribution, package managers that score publisher trust (Homebrew core/cask, winget, choco)
// After:
- **Includes:** Signed and unsigned installers, store and non-store distribution, package managers that score publisher trust (Homebrew cask, winget, choco)
```

§7 Routes elsewhere (line 116):

```markdown
// Before:
  - A CLI distributed via Homebrew core → **desktop-app** (Homebrew acts as a trust authority)
// After:
  - A CLI distributed via Homebrew core (`brew install <formula>`) → **still cli-binary** (boundary confirmed during M4.1/M4.2; `brew install --cask` → desktop-app)
```

Under the `## Classifier Rule — Innermost Trust Boundary` heading, after the `> **Form:** …` line (line 155), insert:

```markdown
> **Runtime copy:** promoted to shipped `references/classifier.md` (2026-10-16, `2610161852-dispatcher-rubric-consistency-plan.md`). That file is canonical for runtime classification; this section is the design record. Change the rule there first, then mirror material changes here.
```

Open Questions (line 384):

```markdown
// Before:
- [ ] **CLI vs desktop-app boundary at Homebrew.** Homebrew is currently routed to desktop-app on the basis that Homebrew scores publisher trust. Confirm during Phase 4 M4.1/M4.2 authoring; revisit if Homebrew core formulae and casks diverge in audit shape.
// After:
- [x] **CLI vs desktop-app boundary at Homebrew.** *Resolved in M4.1/M4.2:* `brew install <formula>` (core) → cli-binary; `brew install --cask` → desktop-app. Recorded in `references/classifier.md` Routing Overrides (2026-10-16).
```

Revision Log — append row:

```markdown
| 2026-10-16 | Classifier rule promoted to shipped `references/classifier.md` (runtime-canonical); `SKILL.md` no longer links into `.projex/`. Homebrew boundary corrected to match M4.1/M4.2 (formula → cli-binary, cask → desktop-app); Open Question resolved. §9 "split audit" superseded at runtime by edge-case discipline (one primary type; other component noted for a separate audit). Plan: `2610161852-dispatcher-rubric-consistency-plan.md`. |
```

**Rationale:** Without the pointer, a future author edits the def and the runtime silently diverges. The Homebrew fix keeps the def from contradicting shipped workflows. The def is not concluded/retired, because it still owns the taxonomy identity, extension procedure, and future splits.

**Verification:** `grep -c 'references/classifier.md' .projex/2604070300-install-auditor-subject-type-taxonomy-def.md` → ≥3. `grep -n 'Homebrew core → \*\*desktop-app' …def.md` → no output.

**If this fails:** `git checkout -- .projex/2604070300-install-auditor-subject-type-taxonomy-def.md`.

---

## Verification Plan

### Automated Checks

- [ ] `grep -rn '\.projex' SKILL.md workflows references scripts` → no output (SC5)
- [ ] `grep -rnE 'Phase [0-9] / M|\(Phase [0-9], M|milestone' SKILL.md workflows references` → no output (SC6)
- [ ] `grep -c '^## Phase' workflows/generic.md` → `4` (SC6)
- [ ] Reference-path existence (SC7):
  ```bash
  python3 -c "import re,os;t=open('SKILL.md').read().split('### Reference Files')[1];p=re.findall(r'^- \`([^\`]+)\`',t,re.M);m=[x for x in p if not os.path.exists(x)];print(len(p),'paths; missing:',m)"
  ```
  → `missing: []`
- [ ] HTML comment balance in edited workflows:
  ```bash
  python3 -c "import glob;[print(f, open(f).read().count('<!--'), open(f).read().count('-->')) for f in sorted(glob.glob('workflows/*.md'))+['references/criteria/remote-integration.md']]"
  ```
  → equal counts per file
- [ ] `python3 -c "import json;json.load(open('evals/evals.json'))"` succeeds, and `git diff --stat` lists none of `evals/evals.json`, `scripts/`, `STEWARDSHIP.md` (SC10)
- [ ] No new `.ps1` refs (sibling-plan compatibility): `git diff -U0 -- SKILL.md workflows references | grep '^+' | grep -c '\.ps1'` → `0`
- [ ] Report skeleton + frontmatter untouched: `git diff -U0 SKILL.md | grep -E '^[-+]' | grep -E 'Install Audit:|## Audit Coverage|Audit confidence|^[-+]description:'` → no output (SC10)

### Manual Verification — Eval Desk-Check (SC9)

Trace each case through the **new** `SKILL.md` Step N + routed workflow text. Record pass/fail in the execution log.

| Eval | Subject | Expected | Trace under new text | Pass if |
|---|---|---|---|---|
| 2 | `react-native-community-async-storage` (npm, Slack) | REJECTED or CONDITIONAL | Combosquat of `@react-native-async-storage/async-storage`; Red Flag if no independent history, else HIGH | either verdict |
| 3 | `expresss` | REJECTED or CONDITIONAL | Distance 1 from `express`; script `critical` → Red Flag unless proven; `high` → CONDITIONAL | either |
| 4 | `chalk` | not REJECTED | It is the legitimate package; Red Flag condition fails | APPROVED/CONDITIONAL |
| 9 | `requers` (PyPI) | REJECTED or strong CONDITIONAL | Real project with own history → similarity alone → HIGH flag → CONDITIONAL (or REJECTED if auditor rates impersonation CRITICAL) | either |
| 5 | `lodash@4.17.20` | CONDITIONAL or REJECTED | HIGH CVE fixed in 4.17.21 → not "unpatched" → HIGH → CONDITIONAL (upgrade) | CONDITIONAL |
| 7 | `mkdirp@0.5.1` → `minimist@0.0.8` | CONDITIONAL (expected_output) | Direct-dep CVE fixed upstream → not "unpatched" → CONDITIONAL | CONDITIONAL |
| 12 | `nginx:latest` prod | not REJECTED | No container-root Red Flag; `:latest` on prod = HIGH (addendum) → CONDITIONAL | CONDITIONAL |
| 26 | `redis` dev | APPROVED | No Red Flag fires; root graded by container workflow, not auto-REJECT | not forced to REJECTED |
| 13 | `someunknownregistry.io/cryptominer:latest` | REJECTED | Auditor rates CRITICAL under container Toward REJECTED "Unknown registry + suspicious naming" → node 1 | REJECTED |
| 14 | `actions/checkout@<sha>` read-only | APPROVED | SHA pin, no privilege → no flag | APPROVED |
| 15 | `vendor/release-workflow@v2` + `pull_request_target` + `secrets: inherit` + child `@main` | REJECTED | Unverified third-party non-SHA ref with secrets → Red Flag; child `@main` also qualifies | REJECTED |
| 27 | `docker/build-push-action@v5` + `packages: write` | CONDITIONAL | Verified publisher tag pin → HIGH (not Red Flag) → CONDITIONAL (pin to SHA) | CONDITIONAL |
| 20 | `brew install ripgrep` | APPROVED, routes cli-binary | Step 0 row 7 now names `brew install <formula>` → cli-binary, high | routes cli-binary |
| 25 | phishing OAuth `superproductivity-ai.xyz` | REJECTED | Auditor rates CRITICAL under remote-integration Toward REJECTED (phishing link, suspicious TLD) → node 1 now explicitly covers it | REJECTED |
| 30 | terraform via shared drive | CONDITIONAL | Bridge is auditor-rated; "legitimate but informal channel" → HIGH → CONDITIONAL; not forced to REJECTED | CONDITIONAL |

### Acceptance Criteria Validation

| Criterion | How to Verify | Expected Result |
|-----------|---------------|-----------------|
| SC1 | Step 2 grep pair | 0 old items, 4 new markers |
| SC2 | Read `SKILL.md` Step N | Terms block present after tree fence, three bullets |
| SC3 | Step 3 grep + desk-check rows 14/15/27 | Aligned; traces pass |
| SC4 | Step 1 checks | File present, no history refs, Homebrew overrides |
| SC5 | grep `.projex` | No output |
| SC6 | grep labels + generic heading count | No output; `4` |
| SC7 | python path check | `missing: []` |
| SC8 | Step 5 greps | Pointer ≥3 refs; stale Homebrew line gone |
| SC9 | Desk-check table | All rows pass |
| SC10 | `git diff --stat` + skeleton grep | Untouched |

---

## Rollback Plan

Per-step rollback is noted in each step above. To abandon the whole change:

1. `projex-abandon` the ephemeral branch (checkout mode), or `git checkout -- <files>` for the 13 edited files and delete `references/classifier.md`.
2. No data migrations, script changes, or eval changes need reversing.

---

## Notes

### Risks

- **Red Flag narrowing lets a real attack through:** typosquat / CI / removal items are now conditioned. Mitigation: each still matches its addendum's REJECTED path. Precedence keeps Red Flags un-downgradable. Auditor-rated CRITICAL still reaches node 1.
- **Auditor-rated bridge is judgment-dependent:** no worse than today's implicit behavior, and now explicit and recorded in Risk Flags. Mechanical mapping rejected (eval 30 counterexample).
- **Collision with later dispatcher-compression plan:** that plan will move Step N content. Mitigation: Dependencies → Blocks names it; this plan adds no new sections beyond one terms block.
- **Sibling `2610161849-python-script-ports-plan.md` edits `SKILL.md` lines 87 + 241 and asserts no new `.ps1` refs in `SKILL.md`/`workflows/`/`references/`:** this plan leaves both lines alone (Step 2e `...`) and names the typosquat script by stem (`typosquat-check`, no extension), so it adds no `.ps1` ref. Either plan can execute first. The line numbers shift, but both plans anchor on exact strings.
- **`references/classifier.md` drifts from def:** mitigated by the def's runtime-copy pointer (shipped file is canonical).

### Open Questions

None.

### Split Decision

`No split — heuristic tripped but steps tightly coupled`. Size: ~700 lines / ~52 KB, which trips the size limb. The step limb is not tripped (5 steps; the auto-suggest needs >5). About 150 lines are the verbatim new-file body for `references/classifier.md` (Step 1). The steps are coupled: Step 2 points at Step 1's file, Step 3 quotes Step 2's Red Flag, and Step 5 points at Step 1. A split would ship a dispatcher pointing at a missing file, or a CI addendum contradicting the dispatcher. All files sit in the repo's single `.projex/` scope. There is no upstream/downstream mixing: the skill's rubric text is one layer.
