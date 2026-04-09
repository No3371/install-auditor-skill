# Definition: install-auditor Subject-Type Taxonomy

> **Created:** 2026-04-07 | **Last Revised:** 2026-04-08
> **Author:** Claude (Opus 4.6)
> **Scope:** The locked v1 subject-type taxonomy that the `install-auditor` dispatcher routes audits against. Defines each type's identity, boundaries, examples, target workflow file, and the rules for adding/splitting types over time. Excludes the classifier rule itself (M0.2) and per-type Tier 1/2/3 thresholds (Q4).
> **Status:** Stabilizing
> **Parent Navigation:** [2604070218-install-auditor-subject-typed-redesign-nav.md](2604070218-install-auditor-subject-typed-redesign-nav.md)
> **Source eval:** [2604070217-subject-typed-audit-dispatch-eval.md](2604070217-subject-typed-audit-dispatch-eval.md) (§5.3)
> **Milestone:** M0.1 + M0.2 of Phase 0 (Taxonomy & Classifier Lock-In)

---

## Identity

The subject-type taxonomy is the closed-but-extensible enumeration of installable categories that the `install-auditor` dispatcher uses to route an audit to exactly one workflow file. Each type names a distinct **trust boundary the user must cross** when installing an artifact of that category. The taxonomy is the first-class spec that the dispatcher, every `workflows/<type>.md` file, the classifier rule, `references/criteria.md`, and `evals/evals.json` all reference.

It exists because audits of fundamentally different installables (an npm package vs a browser extension vs a container image) demand fundamentally different evidence sources and rubrics, and conflating them inside a single monolith dilutes both signal and read-cost. The taxonomy is the spine that lets the redesign be additive instead of dilutive.

---

## Boundaries

**Is:**
- An enumeration of subject types, each with identity, scope, examples, and a target workflow file
- The single source of truth for which `workflows/<type>.md` files exist
- Closed at any given version (currently v1 = 10 types) but open across versions via a documented extension procedure
- The codomain of the future classifier rule (M0.2)
- The keys against which `references/criteria.md` rubrics and `evals/evals.json` cases are bucketed

**Is not:**
- The classifier rule itself ("innermost trust boundary") — that is M0.2, authored as a section in this file later
- Per-type Tier 1/2/3 thresholds — those are Q4, defined inside each workflow file
- A scoring rubric or evidence acquisition spec
- A statement about audit depth or PASS/CONDITIONAL/FAIL semantics
- A list of which workflow files currently exist on disk (most do not yet — they are authored in Phases 2–4)

---

## Subject Types (v1, locked)

Each type entry uses a uniform structure:

- **Identity** — one-sentence definition of the trust boundary
- **Examples** — concrete distribution channels covered
- **Workflow file** — target file under `workflows/`
- **Includes** — what is in scope, including any explicit absorptions (e.g. IaC under registry-package)
- **Routes elsewhere** — known overlap cases that the classifier should send to a different type, with reasoning

### 1. Registry-distributed library / package

- **Identity:** Source code library installed via a language ecosystem's package registry. Trust boundary is the registry's publishing process and the package's maintainer chain.
- **Examples:** npm, PyPI, RubyGems, crates.io, Maven Central, NuGet, Go modules, Hex
- **Workflow file:** `workflows/registry-package.md`
- **Includes (v1):**
  - All ecosystems supported by `scripts/registry-lookup.ps1` (npm, PyPI, RubyGems, crates.io, Maven, NuGet, Go)
  - **Infrastructure-as-code modules distributed via registries** — Terraform Registry, Ansible Galaxy, Helm charts via Artifact Hub. They share registry-package's evidence shape (versions, downloads, maintainers, CVE feeds). See Future Splits.
- **Routes elsewhere:**
  - A package whose `bin` ships a CLI you invoke standalone → **still registry-package**: the registry is the trust boundary, not the binary
  - A package consumed only as a transitive dep → handled inside `registry-package.md`'s transitive-dependency surface, not routed elsewhere

### 2. Browser extension

- **Identity:** Code that loads inside a browser, granted browser-mediated permissions over web content, history, cookies, storage, or DOM.
- **Examples:** Chrome Web Store, Firefox Add-ons, Edge Add-ons, side-loaded `.crx`
- **Workflow file:** `workflows/browser-extension.md`
- **Includes:** MV2 and MV3 manifests, all major stores, side-loaded extensions
- **Routes elsewhere:**
  - A browser extension that wraps a CLI binary → **still browser-extension**: the install pipe (the store) is the trust boundary

### 3. IDE / editor plugin

- **Identity:** Code loaded by a code editor or IDE that runs in-process or in a child process under the editor's privileges.
- **Examples:** VS Code Marketplace, Open VSX, JetBrains Marketplace, Sublime Package Control, Neovim plugins (vim-plug, lazy.nvim, packer, etc.)
- **Workflow file:** `workflows/ide-plugin.md`
- **Includes:** Marketplace + non-marketplace plugins; per-editor package managers (Sublime/Neovim)
- **Routes elsewhere:**
  - A VS Code extension that wraps a binary → **still ide-plugin**
  - An MCP server installed *via* a VS Code extension → **ide-plugin** (the marketplace is the trust boundary; the MCP is downstream)
  - A Claude Code plugin or skill → **agent-extension** (different trust boundary; see §8)

### 4. Container image

- **Identity:** A pre-built container image pulled by a runtime. Trust boundary is the registry's signing/authorship layer plus the image's lineage.
- **Examples:** Docker Hub, GHCR, Quay, ECR, GCR
- **Workflow file:** `workflows/container-image.md`
- **Includes:** All tags (including `:latest`), signed and unsigned images, public and private registries, base images and application images
- **Routes elsewhere:**
  - A container image whose entrypoint is an npm app → **still container-image**: the registry is the trust boundary; the npm package is downstream

### 5. CI/CD action or workflow

- **Identity:** Reusable CI/CD step distributed via a vendor's marketplace, executed inside a CI runner with access to repository contents and configured secrets.
- **Examples:** GitHub Actions (Marketplace + non-marketplace), GitLab CI components, CircleCI orbs, reusable workflows
- **Workflow file:** `workflows/ci-action.md`
- **Includes:** SHA-pinned, tag-pinned, and version-pinned actions; transitive actions called by other actions
- **Routes elsewhere:**
  - A GitHub Action that pulls a container image as part of its work → **still ci-action**: the action wrapper is the trust boundary

### 6. Desktop application

- **Identity:** A standalone application installed onto a user's OS, gaining process- or user-level privileges.
- **Examples:** Vendor-hosted installer, Microsoft Store, Mac App Store, Homebrew cask, winget, choco, `.deb` / `.rpm`
- **Workflow file:** `workflows/desktop-app.md`
- **Includes:** Signed and unsigned installers, store and non-store distribution, package managers that score publisher trust (Homebrew core/cask, winget, choco)
- **Routes elsewhere:**
  - A desktop app distributed via a registry-package's `bin` (e.g. an Electron app shipped through npm) → **registry-package** (innermost is the registry)

### 7. CLI tool / binary

- **Identity:** A standalone executable installed onto `$PATH` (or equivalent), distributed outside any registry that scores publisher trust.
- **Examples:** GitHub Releases binaries, vendor install scripts (curl-pipe-bash), language-version managers (nvm, pyenv, rustup), one-shot installers
- **Workflow file:** `workflows/cli-binary.md`
- **Includes:** Binaries with checksums or signatures, install scripts, language version managers
- **Routes elsewhere:**
  - A CLI distributed via a registry's `bin` → **registry-package**
  - A CLI distributed via Homebrew core → **desktop-app** (Homebrew acts as a trust authority)

### 8. MCP server / agent extension

- **Identity:** Code that extends an AI agent's capabilities — adding tools, prompts, hooks, skills, or context — and runs with access to the agent's capability surface.
- **Examples:** MCP servers, Claude Code plugins, Claude Code skills, agent extensions for other harnesses
- **Workflow file:** `workflows/agent-extension.md`
- **Includes (v1) — three labeled sub-rubrics inside one workflow file:**
  - **8a · MCP servers** — separate-process tool servers; capability negotiation; transports (stdio / HTTP / SSE); network reach
  - **8b · Claude Code plugins** — slash commands, hooks, settings injection, marketplace metadata
  - **8c · Claude Code skills** — markdown + scripts loaded into agent context; behavioral-shaping risk; file-system and tool reach via the host agent
- **Routes elsewhere:**
  - An IDE plugin that registers an MCP server → **ide-plugin** (innermost is the marketplace)
  - A Claude Code skill distributed via npm → **registry-package** (innermost is the npm registry)
- **Note:** The seam to split sub-rubrics 8a / 8b / 8c into their own workflow files is preserved. See Future Splits for trigger conditions.

### 9. SaaS / remote integration

- **Identity:** A third-party network service connected to a development workflow via OAuth, webhooks, or API key. No local code is installed; trust is delegated to a remote operator.
- **Examples:** OAuth-connected services, webhook receivers, third-party APIs that sit in dev workflow (e.g. Sentry, Datadog, PagerDuty)
- **Workflow file:** `workflows/remote-integration.md`
- **Includes:** OAuth scopes, data residency, breach history, terms of service, third-party API trust
- **Routes elsewhere:**
  - A SaaS that *also* installs a local agent → **split audit**: remote integration here AND the local agent under `cli-binary` or `desktop-app` (whichever fits the agent's distribution shape)

### 0. Generic / unknown (fallback)

- **Identity:** The dispatcher's safety net for any subject the classifier cannot route with sufficient confidence, or any artifact type not yet covered by the taxonomy.
- **Examples:** Anything the classifier flags low-confidence; novel artifact types pending an extension-procedure pass
- **Workflow file:** `workflows/generic.md`
- **Includes (Phase 1 only):** Verbatim Steps 1–4 of the pre-pivot `SKILL.md` monolith — the safe-default audit. Trimmed to a true low-confidence fallback in Phase 5 (M5.2).
- **Routes elsewhere:** N/A — generic is the terminal fallback. After Phase 5, generic should be rare; the classifier should usually route to a specific type.

---

## Classifier Rule — Innermost Trust Boundary

> **Milestone:** M0.2 of Phase 0 (Taxonomy & Classifier Lock-In)
> **Resolves:** Q2 (classifier location — prose vs helper script), eval gap G4 (hybrid-subject handling)
> **Form:** Pure prose (v1). The LLM running the dispatcher reads this section and applies it contextually. A helper script for high-confidence URL-pattern pre-checks is an explicit escalation path (see Escalation at the end of this section), not a v1 deliverable.

### Purpose

When the dispatcher receives an audit request, it must route the audit to exactly one workflow file. The classifier rule is the procedure the dispatcher follows to make that routing choice. It sits between the taxonomy (what types exist) and the workflow files (how each type is audited), and it is the single place where hybrid and ambiguous cases are resolved.

### The rule

**Classify an installable by the innermost trust boundary the user is crossing when they perform the install action.**

A *trust boundary* is a verification and gating layer the installable must pass through before landing on the user's system. When multiple boundaries are nested (an npm package shipped inside a container image; a VS Code extension wrapping a binary; a CLI tool pulled via a CI action), the classifier picks the **innermost** — the last verification gate between the user and the code actually executing.

**Why innermost, not outermost.** The outermost boundary tends to be the biggest-brand trust authority (Docker Hub, GitHub). The innermost boundary is where the actual authorship decision is made, and that is where the audit's rubric needs to be calibrated. A compromised npm package inside a Docker image is a registry-package problem, not a container-image problem, because the image is only as trustworthy as the packages it bundles — but the trust gate the user personally clicked through was the image registry, not the npm registry, so the *classification* is Type 4 (container-image) while the npm-level audit happens as a sub-step of the container-image workflow.

### Decision procedure

For each audit request, the classifier runs these steps in order and emits the first confident match:

1. **Read the install artifact.** Collect URL, package name, manifest file, install command, distribution channel, and user-stated intent. Do not run anything; classification is read-only.
2. **Identify candidate types** using the signal table below.
3. **If exactly one type matches with strong signals** → classify as that type with **high** confidence.
4. **If multiple types match** → apply the innermost-trust-boundary rule: pick the type whose boundary the user crosses last before the code runs. If the rule resolves the tie cleanly → high confidence. If the rule narrows but does not fully resolve → **medium** confidence.
5. **If no type matches strongly**, or multiple types remain in conflict after the trust-boundary rule → classify as **Type 0 (generic) with low confidence**, and name the missing or conflicting signal in the rationale.
6. **Emit the classification** in the output format below.

### Signal table (classifier's eyes)

Scannable reference for step 2. Each type lists the top signals that should trigger a candidate match. Strong URL/path patterns give high-confidence hits; primary signals are the contextual cues to check when URLs alone are ambiguous.

| Type | Primary signals | Strong URL / path patterns |
|---|---|---|
| **1 · registry-package** | `npm install`, `pip install`, `cargo add`, `gem install`, `go get`, `nuget add`, `mvn dependency`, `composer require`; presence of `package.json` / `pyproject.toml` / `Cargo.toml` / `Gemfile` / `go.mod` / `*.csproj` / `pom.xml`; IaC manifests referencing Terraform Registry / Ansible Galaxy / Artifact Hub | `npmjs.com/package/*`, `pypi.org/project/*`, `rubygems.org/gems/*`, `crates.io/crates/*`, `central.sonatype.com/*`, `nuget.org/packages/*`, `pkg.go.dev/*`, `registry.terraform.io/*`, `galaxy.ansible.com/*`, `artifacthub.io/*` |
| **2 · browser-extension** | Manifest with `manifest_version` + `permissions` + `host_permissions`; mention of "browser extension", "add-on", "MV2/MV3", "content script" | `chromewebstore.google.com/*`, `addons.mozilla.org/*`, `microsoftedge.microsoft.com/addons/*`, any `.crx` / `.xpi` file |
| **3 · ide-plugin** | `code --install-extension`, VSIX file, JetBrains plugin ID, Sublime Package Control manifest, vim-plug / lazy.nvim / packer plugin spec, MELPA recipe | `marketplace.visualstudio.com/items*`, `open-vsx.org/extension/*`, `plugins.jetbrains.com/plugin/*`, `packagecontrol.io/packages/*` |
| **4 · container-image** | `docker pull`, `docker run`, `podman pull`, `FROM` line in a Dockerfile, image tag with `:`; image digest starting with `sha256:` | `hub.docker.com/*`, `ghcr.io/*`, `quay.io/*`, `*.dkr.ecr.*.amazonaws.com`, `gcr.io/*`, `public.ecr.aws/*` |
| **5 · ci-action** | `uses:` in `.github/workflows/*.yml`, GitLab `include:` component, CircleCI `orbs:` stanza, reusable workflow reference | `github.com/<owner>/<action>@<ref>` (GitHub Actions), `gitlab.com/.../components/*`, `circleci.com/orbs/*` |
| **6 · desktop-app** | `.msi` / `.dmg` / `.deb` / `.rpm` / `.pkg` / `.appx` installer; `brew install --cask`, `winget install`, `choco install`; OS-level package manager context | `apps.microsoft.com/*`, `apps.apple.com/*`, `formulae.brew.sh/cask/*`, `winget.run/pkg/*`, `community.chocolatey.org/packages/*` |
| **7 · cli-binary** | `curl … \| sh`, `wget … \| bash`, GitHub Releases binary download, language version manager (nvm / pyenv / rustup / volta), direct URL to an executable, checksum / signature file alongside binary | `github.com/*/releases/download/*`, `get.<vendor>.sh` style install scripts, vendor-hosted binary URLs |
| **8 · agent-extension** | MCP server manifest / stdio spec; Claude Code plugin bundle (slash commands, hooks, settings); Claude Code skill with `SKILL.md` + scripts; agent host runtime context (Cursor, Cline, Continue) | `.mcp.json` entries, `.claude/skills/*` directories, `claude-code/plugins/*`, `modelcontextprotocol.io/*`, `mcp.so/*` |
| **9 · remote-integration** | OAuth flow, API key exchange, webhook endpoint, "Connect to <service>" UI, no local code install, credentials-based trust delegation | Vendor OAuth provider URLs, `hooks.slack.com/*`, vendor "integrations" pages, `api.*.com/*` key-exchange endpoints |
| **0 · generic** | *No specific-type signals fire with sufficient strength, or multiple conflict after the trust-boundary rule is applied* | *(none)* |

For Type 8, the sub-rubric flag (8a / 8b / 8c) is resolved at classification time:

- **8a (MCP server)** — artifact is a standalone process / binary / script advertising MCP tools, referenced from an MCP config file
- **8b (Claude Code plugin)** — artifact is a plugin bundle (`plugin.json` + commands / hooks / agents) distributed for Claude Code
- **8c (Claude Code skill)** — artifact is a directory containing `SKILL.md` (plus optional `scripts/`, `references/`, `evals/`)

### Confidence levels

| Level | Meaning | Example |
|---|---|---|
| **High** | Unambiguous URL or manifest signal; a single type fires with strong signals; innermost boundary is obvious | User provides `https://www.npmjs.com/package/express` → Type 1, high |
| **Medium** | Signals are present but partial or indirect (README says "install via npm" but the URL is a GitHub repo); innermost boundary inferred rather than directly stated | User provides `github.com/owner/repo` that publishes to npm → Type 1, medium |
| **Low** | No strong signals fire, or strong signals for multiple types conflict even after applying the trust-boundary rule | Novel or ambiguous artifact → Type 0, low |

**Fallback discipline.** Low confidence **routes to Type 0 (generic)**, never to a best-guess specific type. A confident misroute dilutes the per-type workflow's rubric; generic is designed to carry ambiguous cases without loss of rigor. A Type 0 classification with a precise "signals conflict because X" rationale is more useful to downstream workflow authors than a Type 3 classification that turns out wrong two steps into the audit.

### Classifier output format

Every classification emits a structured decision. This is the contract between the classifier and the workflow loader; downstream eval cases assert against this shape.

```
Subject type:   <type-id> (<type-name>)
Confidence:     high | medium | low
Trust boundary: <one-line: what the user is crossing>
Rationale:      <1–3 sentences: which signals triggered the choice>
Routes to:      workflows/<type>.md
Sub-rubric:     <only for Type 8: 8a | 8b | 8c>
```

Worked output for a canonical case:

```
Subject type:   1 (registry-package)
Confidence:     high
Trust boundary: npmjs.com registry — maintainer-signed publish
Rationale:      URL is npmjs.com/package/express; stated install command is `npm install express`; package.json resolution applies.
Routes to:      workflows/registry-package.md
```

### Worked hybrid examples

Canonical walkthroughs showing the innermost-trust-boundary rule in action. These double as classification regression eval seeds for Phase 1 M1.3.

**Example 1 — npm package whose `bin` ships a CLI** (e.g. `prettier`, `typescript`)
- Boundaries crossed: npm registry (outer) → package maintainer publishing (inner)
- **Classification:** Type 1 (registry-package), high
- **Why:** The CLI exists only because npm delivered it. The trust gate is the registry's publishing process; the CLI binary is downstream of that gate, not a separate install.

**Example 2 — VS Code extension that wraps a binary** (e.g. `rust-analyzer`'s VS Code extension bundling the LSP binary)
- Boundaries crossed: VS Code Marketplace (outer) → extension maintainer (inner)
- **Classification:** Type 3 (ide-plugin), high
- **Why:** The user clicks "Install" in VS Code; the marketplace is the verification layer. The bundled binary is downstream and audited under the ide-plugin rubric.

**Example 3 — Docker image whose entrypoint is an npm app**
- Boundaries crossed: Container registry (outer) → image author assembling layers (inner)
- **Classification:** Type 4 (container-image), high
- **Why:** The user runs `docker pull`; the registry is the trust gate the user personally crosses. The npm package inside is audited as a sub-step *within* `container-image.md` if it warrants separate attention.

**Example 4 — GitHub Action that pulls a Docker image internally**
- Boundaries crossed: Action marketplace (outer) → action author (inner)
- **Classification:** Type 5 (ci-action), high
- **Why:** The user writes `uses: owner/action@sha` in a workflow; the action is the install surface. The Docker image is an implementation detail `ci-action.md` covers via its transitive-action surface.

**Example 5 — Claude Code skill distributed via npm**
- Boundaries crossed: npm registry (outer) → skill author publishing (inner)
- **Classification:** Type 1 (registry-package), high
- **Why:** The skill's install gate is `npm install`, not a skill-specific marketplace. The skill *content* (markdown, scripts) is downstream and audited within `registry-package.md`. If the skill content is the primary concern, the registry-package workflow may invoke Type 8's skill-flavor signals as a sub-rubric.

### Edge-case discipline

- **Prefer generic with a quality rationale over a confident misroute.** A Type 0 classification carrying `"signals conflict: X vs Y, cannot resolve via trust-boundary rule"` is always more useful than a high-confidence route that turns out wrong mid-audit.
- **Never split an audit across two types at the classification layer.** If an installable truly needs two rubrics (e.g. a SaaS that also installs a local agent), the classifier picks the *primary* type — the one whose trust boundary the user is actually crossing — and the chosen workflow decides whether to sub-audit the secondary component. Splitting at classification would violate the "one installable → one type" invariant.
- **User override is always honored.** If the user explicitly states `treat this as <type>`, the classifier emits that type at high confidence with `user override: <verbatim statement>` in the Rationale field. Never argue with an explicit override.
- **Classification is read-only.** The classifier never modifies the installable, runs install scripts, or executes probe commands. All signals come from URLs, manifests, package names, and stated intent. Evidence acquisition begins *inside* the chosen workflow, after routing.
- **No re-classification mid-audit.** Once a workflow has been routed to, it owns the audit. A workflow may invoke sibling workflow sub-steps, but it does not hand the audit back to the classifier. This matches the "one installable → one type" constraint and prevents routing loops.

### Escalation path (not v1)

If classification precision drifts below an acceptable rate during Phase 2+ execution (trigger: ≥2 eval regressions attributable to misclassification, or user reports consistent misroutes), add a thin helper script `scripts/classify-prescan.ps1` (or `.sh`) that:

1. Accepts an installable spec (URL, command, or file path).
2. Runs a deterministic URL-pattern pre-check against the Strong URL/path patterns column above.
3. Emits either `{type, confidence: "high", rationale: "<pattern matched>"}` for unambiguous matches, or `null` when the prose classifier should take over.

The helper is additive — it short-circuits the obvious cases and leaves ambiguous ones to the prose classifier. It does **not** replace this section. Adding the helper is itself a patch-projex against this file (no taxonomy-version bump required; the helper is a classifier implementation detail, not a type change).

---

## Constraints & Invariants

- **Closed at any given version, open across versions.** v1 has exactly 10 types. New types are added through the documented extension procedure, never silently.
- **One installable → one type.** An installable resolves to exactly one type at audit time. Hybrid subjects (npm-distributed CLI, container wrapping npm app, IDE plugin wrapping a binary) are routed via the classifier's "innermost trust boundary" rule (M0.2).
- **Each type has exactly one workflow file** under `workflows/`. Sub-rubrics inside a workflow (e.g. 8a/8b/8c inside `agent-extension.md`) are an internal organization choice, not separate types.
- **Generic is the only fallback.** No type may be marked as TBD or skipped; if a subject doesn't fit any specific type, the classifier routes to generic.
- **A workflow file may delegate sub-steps to a sibling workflow** (e.g. `container-image.md` may invoke a `registry-package.md` sub-step when auditing a layered npm app), but its routing identity remains its own type.
- **Type identifiers are stable.** Once a type is locked, its workflow file name does not change without a taxonomy version bump and migration entry in the Revision Log.

---

## Relationships

| Related entity | Relationship | Description |
|---|---|---|
| `install-auditor` dispatcher (`SKILL.md` post-Phase 1) | depended on by | Dispatcher reads this taxonomy to know what types exist and which workflow file to load |
| `workflows/<type>.md` files | depended on by | Each workflow file is the implementation of exactly one type entry here |
| Classifier rule (this file's "Classifier Rule" section) | depends on | The rule operates over the type set defined here; without a locked taxonomy the rule has no codomain |
| `scripts/classify-prescan.*` (hypothetical, not v1) | depended on by | Escalation path documented at the end of the classifier section; added only if classification precision drifts |
| `references/criteria.md` (post Q6 decision) | depended on by | Criteria.md's Tier 1/2/3 rubrics specialize per type; the type list here is the key set |
| `evals/evals.json` | depended on by | Each eval case carries an expected subject type drawn from this list |
| Queued retargeting plans (typosquat, multi-DB CVE, transitive deps) | depended on by | Their target file (`registry-package.md`) is named here as Type 1 |
| Parent navigation (`...redesign-nav.md`) | child of | This definition is the M0.1 deliverable consumed by Phase 0 sign-off |

---

## Extension Procedure (open-ended)

Adding an 11th, 12th, ... type — or splitting an existing one — is supported via the following procedure. The intent is that growth is explicit, reviewed, and traceable, not silent.

### Adding a new type

1. **Justify.** Show the new type cannot be routed satisfactorily through any existing type. The signal that it deserves its own type: placing it in the closest existing workflow would require an `if subject == X` branch inside that workflow's evidence acquisition or rubric — that branch is the smell.
2. **Draft definition entry.** Add a new section to this file matching the existing per-type structure (Identity / Examples / Workflow file / Includes / Routes elsewhere).
3. **Update parent navigation.** Add a milestone to the relevant phase of the parent nav (typically Phase 4 long-tail, or a new sub-phase).
4. **Author the workflow file.** Create `workflows/<new-type>.md` following the standard workflow template defined in Phase 1 (Identify / Evidence / Subject Rubric / Subject Verdict Notes).
5. **Add eval coverage.** At least one positive + one negative case in `evals/evals.json` before the type is considered Live.
6. **Bump classifier.** Update the classifier rule (the M0.2 section in this file) so the dispatcher recognizes the new type's distinguishing signals.
7. **Increment taxonomy version.** Bump v1 → v2 in this file's frontmatter; append a Revision Log entry summarizing what changed.

### Splitting an existing type

Same as above, plus a migration step:

- Partition the existing workflow file's content into the new files
- Re-bucket existing eval cases against the new type set
- Record the split in the parent nav's revision log
- Keep the old type entry under a "Deprecated" subsection of this file for one full phase as a redirect, then remove

---

## Future Splits (anticipated, not yet performed)

Documented so the structural seams are visible to future authors before they need them.

- **Type 8 (agent-extension) → 8a/8b/8c as separate workflow files.**
  - **Trigger:** Either (a) ≥30% of `agent-extension.md` content becomes sub-rubric-specific, or (b) any sub-rubric needs a distinct classifier signal that the unified workflow can't carry cleanly, or (c) read-cost per audit grows past the per-workflow budget set in Phase 5.
  - **Result:** `workflows/mcp-server.md`, `workflows/claude-code-plugin.md`, `workflows/claude-code-skill.md`. Taxonomy moves from 10 to 12 types (8 retired, 8a/8b/8c added).

- **Type 1 (registry-package) → split out `iac-module.md`.**
  - **Trigger:** Rubric pressure during Phase 2 M2.1 — IaC modules (Terraform / Ansible / Helm) often touch cloud credentials and modify state directly, which may diverge enough from library-package risk that shared rubrics become noisy.
  - **Result:** `workflows/registry-package.md` retains language ecosystems; new `workflows/iac-module.md` covers Terraform Registry, Ansible Galaxy, Artifact Hub. Taxonomy moves from 10 to 11.

Both splits are **anticipated, not committed.** They activate only if their triggers fire during execution.

---

## States & Lifecycle (per type)

| State | Description | Transitions To |
|---|---|---|
| **Proposed** | Type is suggested via the extension procedure step 1 | Locked (after user sign-off) |
| **Locked** | Type is in the canonical list above; workflow file may or may not exist yet | Live |
| **Live** | Workflow file exists, classifier routes to it, evals cover it | Deprecated (only) |
| **Deprecated** | Type still defined for historical reference but no longer routed; workflow file moved to archive | (terminal) |

**Current status of v1 types:**

| Type | State | Notes |
|---|---|---|
| 0 — generic | Locked → Live (Phase 1) | Receives the verbatim monolith content as a safe fallback in Phase 1; trimmed in Phase 5 |
| 1 — registry-package | Locked, not yet Live | Becomes Live in Phase 2 M2.1 |
| 2 — browser-extension | Locked, not yet Live | Becomes Live in Phase 3 M3.1 |
| 3 — ide-plugin | Locked, not yet Live | Becomes Live in Phase 3 M3.4 |
| 4 — container-image | Locked, not yet Live | Becomes Live in Phase 3 M3.2 |
| 5 — ci-action | Locked, not yet Live | Becomes Live in Phase 3 M3.3 |
| 6 — desktop-app | Locked, not yet Live | Becomes Live in Phase 4 M4.1 |
| 7 — cli-binary | Locked, not yet Live | Becomes Live in Phase 4 M4.2 |
| 8 — agent-extension | Locked, not yet Live | Becomes Live in Phase 4 M4.3; sub-rubrics 8a/8b/8c authored in same milestone |
| 9 — remote-integration | Locked, not yet Live | Becomes Live in Phase 4 M4.4 |

---

## Open Questions

- [x] **M0.2 — Classifier rule prose.** *Resolved 2026-04-07 (PM).* Authored in the Classifier Rule section above. Form: pure prose (Q2 = option a). Helper script is a documented escalation path, not a v1 deliverable.
- [ ] **Q4 — Per-type Tier 1/2/3 thresholds.** Out of scope for this definition; defined inside each workflow file as it is authored. *Tracked in parent nav; first concrete instance is Phase 2 M2.1 for registry-package.*
- [ ] **Q5 follow-up — Agent-extension sub-rubric depth.** Sub-rubrics 8a/8b/8c are placeholders here; their full evidence-source list is authored in Phase 4 M4.3.
- [ ] **IaC routing re-validation.** Type 1 currently absorbs Terraform / Ansible / Helm. Re-validate during Phase 2 M2.1 — if `registry-package.md`'s evidence shape doesn't fit, trigger the split-out per Future Splits.
- [ ] **CLI vs desktop-app boundary at Homebrew.** Homebrew is currently routed to desktop-app on the basis that Homebrew scores publisher trust. Confirm during Phase 4 M4.1/M4.2 authoring; revisit if Homebrew core formulae and casks diverge in audit shape.
- [ ] **Versioning policy.** Should the taxonomy carry a semver-style version (v1 → v1.1 → v2)? Which kinds of changes bump major vs minor (add vs split vs rename)? Address once a second type is added or split.
- [ ] **Type-stability guarantee for downstream consumers.** Should `references/criteria.md` and `evals/evals.json` use the workflow filename (`registry-package`) or a stable type ID (`type-1`) as their key? Bears on rename safety during future splits.

---

## Revision Log

| Date | Summary |
|---|---|
| 2026-04-07 | Initial definition created. Locks v1 10-type taxonomy: registry-package, browser-extension, ide-plugin, container-image, ci-action, desktop-app, cli-binary, agent-extension, remote-integration, generic. Decisions baked in: ide-plugin and agent-extension stay separate (Q1 confirmed); agent-extension uses one workflow with three labeled sub-rubrics 8a/8b/8c for MCP-server / Claude Code plugin / Claude Code skill (Q5 = option c); IaC modules (Terraform / Ansible / Helm) route through registry-package as Type 1 (scope gap = option b); taxonomy is closed-at-version, open-across-versions with documented extension procedure (taxonomy stance = open-ended). Excluded by scope: classifier rule (M0.2) and per-type Tier 1/2/3 thresholds (Q4). Future splits documented: agent-extension → 8a/8b/8c separation; registry-package → iac-module extraction. Both anticipated but not committed. |
| 2026-04-08 | **M0.2 complete.** Added Classifier Rule — Innermost Trust Boundary section between Subject Types and Constraints & Invariants. Decisions: Q2 = option (a) pure prose; structured output format `{type, confidence, boundary, rationale, routes, sub-rubric}`; signal table lives inside the classifier section as condensed per-type signals + strong URL patterns (option a). Section contents: purpose, rule statement, 6-step decision procedure, signal table (10 types), confidence level definitions, output format with worked example, 5 worked hybrid examples (npm-with-bin, VS Code wrap, Docker wrapping npm, GitHub Action pulling Docker, Claude Code skill via npm), edge-case discipline (prefer generic over misroute, no split-classification, user override honored, read-only, no re-classification mid-audit), escalation path for optional future URL-pattern helper script `scripts/classify-prescan.*`. Updated Relationships table and M0.2 Open Question → resolved. |
