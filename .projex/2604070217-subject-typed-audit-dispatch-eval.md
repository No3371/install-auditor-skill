---
created: 2026-04-07
author: Claude (Opus 4.6)
subject: install-auditor SKILL — redesign around subject-type-first dispatch into per-type audit workflows
type: Status Quo + Gap Analysis + Comparative
tier: Standard
lenses_applied: First Principles, Constraint Mapping, Inversion
related_projex:
  - .projex/2604021200-reliability-accuracy-improvements-imagine.md
  - .projex/2604021201-multi-db-vulnerability-correlation-proposal.md
  - .projex/2604021202-algorithmic-typosquat-detection-proposal.md
  - .projex/2604021203-transitive-dependency-auditing-proposal.md
  - .projex/2604021204-audit-coverage-confidence-metadata-proposal.md
  - .projex/2604021815-algorithmic-typosquat-detection-plan.md
  - .projex/closed/2604021605-audit-coverage-confidence-metadata-walkthrough.md
consumed_by:
  - .projex/2604070218-install-auditor-subject-typed-redesign-nav.md  # Roadmap built from this eval
prepares: navigate-projex (next invocation) — to draft a living roadmap for the redesigned skill
---

# Subject-Typed Audit Dispatch — install-auditor Redesign Evaluation

## 1. Executive Summary

The install-auditor skill is a single monolithic `SKILL.md` (≈14 KB across Steps 1–6) that applies one workflow — *identify → triage tier → research → score → verdict → report* — to **every** kind of installable, from npm packages and Docker images to browser extensions and GitHub Actions. The shared pipeline pretends these are the same audit problem; in practice the **trust signals, threat models, data sources, and verdict heuristics differ fundamentally** across subject types.

This evaluation finds that the monolithic design has reached its scaling ceiling. Four queued proposals (typosquat detection, multi-DB CVE correlation, transitive dep auditing, audit-coverage metadata) each want to extend the same shared steps, and each will further dilute non-applicable flows. The recommended pivot is a **dispatcher SKILL.md + per-subject-type workflow files**: classify the subject in the first 30 seconds, then load *only* the workflow that fits. This preserves the existing scoring rubric and registry-lookup script as shared primitives while letting subject-specific logic live where it belongs.

This evaluation is the framing document for the next step — a `/navigate-projex` invocation that will turn these findings into a living roadmap with phases, milestones, and child plans.

---

## 2. Evaluation Scope

### Subject
The install-auditor skill at `C:/Users/BA/.claude/skills/install-auditor/`, comprising:
- `SKILL.md` — 6-step monolithic workflow
- `references/criteria.md` — shared scoring rubrics
- `references/licenses.md`, `references/registries.md` — shared lookup tables
- `scripts/registry-lookup.ps1` — PowerShell registry data fetcher
- `evals/evals.json` — regression cases (express, Wappalyzer, async-storage typosquat)
- `.projex/` — five queued proposals plus one closed walkthrough

### Questions Addressed
1. What does the current install-auditor actually do and where does the design strain?
2. Are installables a single audit problem or several distinct problems wearing one hat?
3. Would a subject-type-first dispatch architecture better fit what the skill is being asked to do?
4. What subject-type taxonomy is workable for v1?
5. How do the queued proposals slot into the new architecture?

### Evaluation Criteria

| Criterion | Weight | Description |
|---|---|---|
| Specificity | High | Does the design let subject-specific risks (extension permissions, image signing, SHA-pinning) be expressed natively? |
| Cognitive load | High | How many steps must the agent read on a Tier-1 quick audit? |
| Extensibility | High | Cost to add a new subject type or a new audit signal |
| Reusability | Medium | Are shared primitives (rubrics, registry-lookup, license matrix) reused, not duplicated |
| Migration cost | Medium | Effort to move existing content + close out queued proposals |
| Backward compatibility | Low | Existing evals must still pass after the move |

### Out of Scope
- Implementing the new workflow files themselves (that is `/plan-projex` work, downstream of navigation)
- Re-scoring or extending the rubric content in `criteria.md`
- Cross-skill reorganization (browser-ext-only skill, etc.) — explicitly rejected, see §6 Option C
- Choice of language/runtime for any new helper scripts

---

## 3. Context Analysis

### 3.1 Current State (Primary Evidence)

`SKILL.md` defines six numbered steps applied uniformly:

| Step | Purpose | Subject-aware? |
|---|---|---|
| 1 — Identify the installable | Collect name, version, source, purpose, target env | No — same six fields for every subject |
| 2 — Triage tier (Tier 1/2/3) | Decide audit depth | Partial — uses adoption thresholds tuned for *registry packages* |
| 3 — Research | Web/API research, run `registry-lookup.ps1` | Tilted strongly toward npm/PyPI/etc. |
| 4 — Evaluate | Score §4.1 Provenance, §4.2 Maintenance, §4.3 Security, §4.4 Permissions, §4.5 Reliability, §4.6 Alternatives | Generic, subject-agnostic |
| 5 — Verdict | APPROVED / CONDITIONAL / REJECTED via decision tree | Generic |
| 6 — Report | Structured markdown report with audit-coverage table | Generic |

`registry-lookup.ps1` covers npm, PyPI, RubyGems, crates.io, Maven Central, NuGet, Go proxy. It does **not** know about Chrome Web Store, Firefox Add-ons, VS Code Marketplace, JetBrains Marketplace, Docker Hub / GHCR, GitHub Actions Marketplace, MS Store, Homebrew, vendor-hosted binaries. For those subjects the agent improvises with web search.

`criteria.md` is uniformly tier-aware (`Tier 1: §4.1 + §4.3`; `Tier 2: all`; `Tier 3: all + behavioral`) but **subject-agnostic** — §4.4 Permissions reads as written for browser extensions, not for Docker images or CLI binaries.

`evals/evals.json` tellingly mixes a registry package (express), a browser extension (Wappalyzer), and a typosquat scenario (react-native-community-async-storage) and expects all three to use the same flow. The expected outputs reveal subject-specific reasoning the agent has to *invent* each run.

### 3.2 Pressure From Queued Work

Five proposals sit unexecuted in `.projex/`:

| Proposal | What it adds | Where it wants to live |
|---|---|---|
| Algorithmic typosquat detection (npm v1) | `scripts/typosquat-check.ps1` + `SKILL.md` Step 3 hook | Inside Step 3 of the shared workflow |
| Multi-DB vulnerability correlation | Cross-source CVE merging | Inside Step 3 / §4.3 |
| Transitive dependency auditing | Recurse into deps | Inside Step 3 — only meaningful for registry packages |
| Reliability/accuracy improvements (imagine) | Various | Across all of SKILL.md |
| Audit coverage + confidence metadata | Already partly closed | Step 6 reporting |

Of these, **three are only meaningful for registry packages** (typosquat, transitive deps, parts of multi-DB correlation). Bolting them into the shared `SKILL.md` will make non-registry flows skim past sections marked "skip if not npm/PyPI/etc." That is exactly the symptom this redesign is meant to cure.

### 3.3 Constraints

- **Hard:** Skill must remain a single Anthropic skill (`SKILL.md` is the entrypoint Claude loads). No multi-skill split.
- **Hard:** Existing evals at `evals/evals.json` must still pass.
- **Soft:** PowerShell remains the scripting language for cross-platform parity with `registry-lookup.ps1`.
- **Soft:** No new dependencies on registry-specific SDKs.
- **Self-imposed:** Keep the dispatcher SKILL.md short — load cost matters since it is read every time the skill triggers.

### 3.4 Stakeholders

- **Primary user:** developer/agent about to install something on a dev machine. Wants a fast verdict that reflects subject-relevant risks.
- **Skill author (BA):** wants the queued proposals to land cleanly without further bloating SKILL.md.
- **Future maintainers:** need to extend with new subject types (e.g. MCP servers, Claude Code plugins) without rewriting the spine.

---

## 4. Foundations

### 4.1 First Principles

What is an "audit"? At root: *acquire enough subject-specific evidence to defend a verdict on a defined risk surface.* Two properties of that definition matter:

1. **Risk surface is subject-specific.** A browser extension's risk surface is dominated by manifest permissions, content-script reach, and update auto-push. A Docker image's risk surface is dominated by base image provenance, signing, layer scanning, and runtime privileges. An npm package's risk surface is dominated by transitive deps, install scripts, and maintainer compromise. These are *different surfaces*, not different intensities of the same surface.

2. **Evidence sources are subject-specific.** "Run `registry-lookup.ps1`" is a no-op for a Chrome extension. "Read the manifest permissions" is a no-op for a Go module. A workflow that pretends one toolset fits all forces the agent into improvisation precisely where rigor matters most.

The current SKILL.md collapses (1) and (2) into a generic spine because *some* steps (verdict tree, report shape) are genuinely shared. The redesign needs to preserve the shared spine while letting subject-specific logic be first-class.

### 4.2 Key Assumptions

| # | Assumption | Validity | Risk if Wrong | Recommendation Sensitive? |
|---|---|---|---|---|
| A1 | Subject types form a discrete, recognizable taxonomy with stable boundaries | Medium-High | Edge cases (hybrid installables) confuse the dispatcher | Yes — taxonomy granularity matters |
| A2 | A single SKILL.md dispatcher of ≈3–4 KB can reliably classify subjects from natural-language requests | Medium | Misclassification routes to the wrong workflow | Yes — falls back to generic if uncertain |
| A3 | Subject-specific workflows can share rubric, license matrix, and verdict tree without duplication | High | Drift between workflows | Low — shared `references/` already exists |
| A4 | Per-subject workflow files are easier to reason about than tier-branched monolith | High | None — this is a maintainability claim | Low |
| A5 | Queued proposals can be retargeted into the new architecture without rewrites | Medium | Some plan re-work needed | Medium |
| A6 | Existing evals can be re-mapped to subject-typed workflows without behavioral change | High | Small adjustments to expected outputs | Low |

### 4.3 Prior Work / Why the Monolith Existed

The monolithic design was the right v0: **discover what an audit even looks like across subjects** before factoring. The closed walkthrough (`audit-coverage-confidence-metadata`) shows the skill in active iteration and recently grew an audit-coverage table — additive, generic, fits the monolith. Now that five proposals want subject-specific extensions in the same shared steps, the centripetal force has flipped to centrifugal. This is the natural moment to factor.

---

## 5. Critical Analysis

### 5.1 Inversion — How Does the Status Quo Fail?

Concrete failure modes today:

1. **Wasted ceremony on the wrong subject.** A Chrome extension audit walks through Step 3's "run registry-lookup.ps1" instruction that does nothing for Web Store entries. The agent silently skips it, but the SKILL.md cost is paid every load.
2. **Missed subject-native checks.** Step 4.4 Permissions is the most important rubric for browser extensions, yet it sits as one bullet alongside five others. There is no checklist of *which* manifest permissions are dangerous, no MV2 vs MV3 awareness, no "host_permissions vs activeTab" guidance.
3. **Docker image audits have no native treatment.** No mention of Cosign/Sigstore signatures, no SBOM check, no base image lineage, no `:latest` warning, no rootful/rootless distinction. The agent improvises.
4. **GitHub Actions audits have no native treatment.** No SHA-pinning rule, no `pull_request_target` warning, no marketplace verification, no transitive action audit. The agent improvises.
5. **Triage-tier thresholds (>100K weekly downloads) are npm-specific** but live in the shared step. They make no sense for a VS Code extension whose adoption signal is install count from the marketplace.
6. **Queued proposals will dilute further.** Adding typosquat-check + multi-DB CVE + transitive deps to Step 3 will make the shared step ~3× longer, of which only the npm-relevant fraction applies on any given audit.

### 5.2 Constraint Mapping — What Gives if We Pivot?

| Constraint | Hard? | What changes under the new design |
|---|---|---|
| Single SKILL.md file as entrypoint | Hard | Remains. Becomes a dispatcher. |
| Under ~4 KB read cost on every invocation | Self-imposed | Achievable: dispatcher is Step 0 (classify) + reference table to workflows |
| Reuse `references/criteria.md` and `licenses.md` | Soft | Workflows reference these, and may layer subject-specific addenda |
| Reuse `scripts/registry-lookup.ps1` | Soft | Stays a shared primitive — only registry-package workflow invokes it |
| Existing evals must pass | Hard | Achievable: each eval routes to its subject's workflow, which produces equivalent output |
| Queued proposals must have a clean home | Hard | Each proposal retargets into one workflow file (typosquat → registry-package; transitive deps → registry-package; multi-DB → registry-package; coverage metadata → shared report layer) |

No constraint is broken by the pivot. The only "give" is migration effort.

### 5.3 Subject-Type Taxonomy (Draft for navigate-projex)

A workable v1 taxonomy — narrow enough to dispatch reliably, broad enough to cover the queued evals plus the highest-volume real-world cases:

| # | Subject Type | Examples | Workflow file (proposed) |
|---|---|---|---|
| 1 | Registry-distributed library / package | npm, PyPI, RubyGems, crates.io, Maven Central, NuGet, Go modules, Hex | `workflows/registry-package.md` |
| 2 | Browser extension | Chrome Web Store, Firefox Add-ons, Edge Add-ons, user-side .crx | `workflows/browser-extension.md` |
| 3 | IDE / editor plugin | VS Code Marketplace, Open VSX, JetBrains Marketplace, Sublime Package Control, Neovim plugins | `workflows/ide-plugin.md` |
| 4 | Container image | Docker Hub, GHCR, Quay, ECR, GCR | `workflows/container-image.md` |
| 5 | CI/CD action or workflow | GitHub Actions, GitLab CI components, CircleCI orbs | `workflows/ci-action.md` |
| 6 | Desktop application | Vendor-hosted installer, MS Store, Mac App Store, Homebrew cask, winget, choco, .deb/.rpm | `workflows/desktop-app.md` |
| 7 | CLI tool / binary | GitHub Releases binary, install scripts, language-version managers | `workflows/cli-binary.md` |
| 8 | MCP server / agent plugin | MCP servers, Claude Code skills/plugins, agent extensions | `workflows/agent-extension.md` |
| 9 | SaaS / remote integration | OAuth-connected services, webhooks, third-party APIs that sit in dev workflow | `workflows/remote-integration.md` |
| 0 | Generic / unknown | Fallback when classifier is uncertain | `workflows/generic.md` (current monolith content trimmed) |

**Hybrid handling.** Some subjects span types (an npm package whose `bin` ships a CLI; a VS Code extension that wraps a binary; a Docker image whose entrypoint is an npm app). The dispatcher's job is to pick the **innermost trust boundary the user is crossing** — in those examples: npm, VS Code Marketplace, Docker Hub respectively. The chosen workflow can call out to a sibling workflow as a sub-step where appropriate.

### 5.4 Architecture Sketch

```
install-auditor/
├── SKILL.md                          # Dispatcher: Step 0 classify → load workflow file
├── workflows/
│   ├── registry-package.md           # npm/PyPI/etc. — typosquat, transitive, multi-DB CVE all live here
│   ├── browser-extension.md          # manifest, permissions, MV2/MV3, host_permissions
│   ├── ide-plugin.md                 # marketplace verification, capabilities
│   ├── container-image.md            # Cosign, SBOM, base image, layers, runtime privileges
│   ├── ci-action.md                  # SHA-pin, pull_request_target, marketplace verification
│   ├── desktop-app.md                # code signing, vendor identity, installer behavior
│   ├── cli-binary.md                 # checksum, signature, release provenance
│   ├── agent-extension.md            # MCP/skill/plugin — capability scope, prompts, network access
│   ├── remote-integration.md         # OAuth scopes, data residency, terms, breach history
│   └── generic.md                    # Fallback when classification is low-confidence
├── references/
│   ├── criteria.md                   # Shared rubric — workflows reference + extend
│   ├── licenses.md                   # Shared
│   └── registries.md                 # Shared
├── scripts/
│   ├── registry-lookup.ps1           # Shared, used by registry-package workflow
│   └── (typosquat-check.ps1)         # Lands in registry-package only
└── evals/
    └── evals.json                    # Re-mapped per subject; subject-typed assertions added
```

`SKILL.md` becomes:

```
Step 0 — Classify subject (one of 10 types) — keep this short and decisive
Step 1 — Load and follow workflows/<type>.md
Step 2 — Use shared verdict tree + report shape (still in SKILL.md)
```

The verdict tree, audit-coverage table format, and report skeleton stay in `SKILL.md` so workflows don't redefine them. Workflows fill in the *evidence acquisition* and *subject-specific scoring*.

### 5.5 Steel-Man for the Status Quo

> "The monolith works. The agent is smart enough to skip irrelevant steps. Adding workflow files is added load — nine files instead of one — and only one is read per audit but all must be maintained."

Counter: file count is not the bottleneck — *load cost per audit* is. With dispatch, an audit reads `SKILL.md` (smaller) + one workflow (the relevant one). Total tokens read per audit go *down*, not up. Maintenance burden is real but accepted: today, each new feature touches the shared SKILL.md and risks all flows; under dispatch, each new feature touches one workflow and risks only that flow. Blast radius shrinks.

---

## 6. Comparative Evaluation of Approaches

| Option | Description | Specificity | Cog. load | Extensibility | Reusability | Migration | Verdict |
|---|---|---|---|---|---|---|---|
| **A. Status quo + targeted patches** | Keep monolith; land queued proposals as Step-3 additions | Weak | Worsens | Poor — every add bloats shared step | Strong | None | Reject |
| **B. Dispatcher SKILL.md + per-type workflows** *(recommended)* | Step 0 classify, load `workflows/<type>.md` | Strong | Improves per-audit | Strong — one file per type | Strong via shared `references/` | Medium | **Accept** |
| **C. Multiple sibling skills** | One Anthropic skill per subject type | Strongest | Best per-audit | Strong | Weak — refs duplicated across skills | High | Reject — fragmentation, eval ownership unclear |
| **D. Single big SKILL.md with conditional sections** | Keep one file but tag sections by subject | Medium | Worse | Medium | Strong | Low | Reject — same monolith, more conditionals |

Option B is the only one that scales the design without fragmenting the skill or duplicating shared assets.

---

## 7. Findings

| # | Finding | Confidence | Lens | Source |
|---|---|---|---|---|
| F1 | The current SKILL.md applies one workflow to fundamentally different risk surfaces | **High** | First Principles | `SKILL.md` Steps 1–6 read end-to-end |
| F2 | Subject-specific risks (extension permissions, image signing, action SHA-pinning) are absent or under-specified | **High** | Inversion | `criteria.md` §4.4, `SKILL.md` Step 3 |
| F3 | Three of five queued proposals are registry-package-only and will dilute non-registry flows if added to shared steps | **High** | Constraint Mapping | `.projex/` proposal docs |
| F4 | Triage-tier thresholds (downloads, GitHub stars) are npm-shaped and don't translate to other subjects | **High** | First Principles | `SKILL.md` Step 2 |
| F5 | A 10-type taxonomy covers the existing eval set and the highest-volume real-world cases without forcing edge-case proliferation | **Medium** | Constraint Mapping | §5.3 above + eval review |
| F6 | Shared primitives (`criteria.md`, `licenses.md`, `registry-lookup.ps1`, verdict tree, report shape) survive intact under dispatch | **High** | Constraint Mapping | §5.4 architecture sketch |
| F7 | Per-audit *read cost* drops under dispatch even though *total file count* rises | **Medium-High** | Inversion | Reasoning, not measurement — flag for navigate-projex to validate |
| F8 | The four open queued proposals retarget cleanly: typosquat / transitive / multi-DB → `registry-package.md`; coverage metadata → shared report layer in SKILL.md | **High** | Constraint Mapping | Cross-reading proposal scope sections |

### Gaps Identified

- **G1** No subject-classifier prompt exists today; one must be authored as part of the dispatcher.
- **G2** No browser-extension, container-image, CI-action, or agent-extension content exists today; these workflow files are net-new authoring.
- **G3** `evals/evals.json` lacks coverage of container images, CI actions, agent extensions — expand alongside the workflows.
- **G4** No guidance for hybrid subjects (npm-distributed CLI, container-wrapped npm app); needs an explicit "innermost trust boundary" rule in the dispatcher.

---

## 8. Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Misclassification routes to wrong workflow | Medium | High — wrong rubric applied | Dispatcher must offer a `generic.md` fallback when confidence is low; eval cases for ambiguous subjects |
| Workflows drift apart in style/structure | Medium | Medium — harder to maintain | Standard workflow template with required sections (Identify / Evidence / Subject Rubric / Subject Verdict Notes) |
| Migration leaves orphaned content in old SKILL.md | Low | Low | Plan a single migration commit; old monolith content moves into `workflows/generic.md` verbatim, then trimmed |
| Queued proposals' plans become stale | Medium | Medium | Re-link each proposal to its target workflow file before navigate-projex closes |
| Per-audit read cost actually rises (false F7) | Low-Medium | Medium | Measure dispatcher + one workflow vs current SKILL.md during execution; reject the pivot if measurement disagrees |
| MCP servers / Claude Code plugins are a moving target | Medium | Low (initially) | Keep `agent-extension.md` deliberately small in v1; iterate |

---

## 9. Recommendations

**Primary recommendation: Adopt Option B — dispatcher SKILL.md + per-subject-type workflow files.**

The pivot is justified by F1–F4 (current design is the wrong shape for the work) and F8 (the queued backlog already wants this shape). It is feasible under every hard constraint (§5.2). It is the *only* option that scales the skill without fragmenting it (§6).

### Conditional recommendations

- **If** the dispatcher's subject-classifier proves unreliable in eval testing → reduce taxonomy to fewer, broader buckets and add a strong `generic.md` fallback rather than expanding rules.
- **If** workflow files start duplicating large sections → extract those into `references/` rather than letting drift grow.
- **If** read-cost measurement (F7) disagrees with prediction → re-evaluate before merging; the redesign's value depends on this.

### Next Steps — Handoff to navigate-projex

This evaluation is the framing input for `/navigate-projex`. The roadmap should include at minimum:

1. **Phase 0 — Taxonomy lock-in.** Confirm the 10-type list (or revise). Define the "innermost trust boundary" classifier rule. Outcome: a one-page subject-type spec.
2. **Phase 1 — Dispatcher refactor.** Trim `SKILL.md` to Step 0 (classify) + Step N (shared verdict/report). Move existing monolith content into `workflows/generic.md` as the safe fallback. Existing evals must pass.
3. **Phase 2 — `registry-package.md` extraction.** First real workflow file. Lands the three retargeted proposals (typosquat, multi-DB CVE, transitive deps). Validates the shared/per-workflow seam.
4. **Phase 3 — High-volume subjects.** Author `browser-extension.md`, `container-image.md`, `ci-action.md`, `ide-plugin.md` with subject-native rubrics. Add evals per type.
5. **Phase 4 — Long-tail subjects.** `desktop-app.md`, `cli-binary.md`, `agent-extension.md`, `remote-integration.md`.
6. **Phase 5 — Retire generic.md as default.** Once subject coverage is confident, classifier defaults shift; `generic.md` only triggers on low-confidence classifications.
7. **Phase 6 — Eval expansion.** Add subject-typed regression cases for every workflow.

Each phase becomes one or more `/plan-projex` documents under the navigation.

### Queued Proposal Retargeting

| Proposal | New target | Action when navigation lands |
|---|---|---|
| `2604021202-algorithmic-typosquat-detection-proposal` | `workflows/registry-package.md` | Update plan `2604021815` to point at the new file |
| `2604021201-multi-db-vulnerability-correlation-proposal` | `workflows/registry-package.md` (CVE section) | Re-scope inside Phase 2 |
| `2604021203-transitive-dependency-auditing-proposal` | `workflows/registry-package.md` | Re-scope inside Phase 2 |
| `2604021204-audit-coverage-confidence-metadata-proposal` (closed walkthrough) | Shared report layer in `SKILL.md` | No re-work — already shared |
| `2604021200-reliability-accuracy-improvements-imagine` | Cross-cutting; redistribute per workflow | Re-read at Phase 0 to split |

---

## 10. Open Questions for navigate-projex

- [ ] Q1 — Is the 10-type taxonomy the right granularity, or should some be merged (e.g. ide-plugin + agent-extension)?
- [ ] Q2 — Where does the "innermost trust boundary" classifier rule go — dispatcher prose, or a small classifier helper script?
- [ ] Q3 — Should each workflow file embed its own report template, or strictly inherit the shared one?
- [ ] Q4 — How does Tier 1/2/3 triage map per subject? (Each workflow likely needs its own thresholds.)
- [ ] Q5 — Do MCP servers, Claude Code plugins, and Claude Code skills warrant *one* workflow or three?
- [ ] Q6 — Should `references/criteria.md` be split into a shared core + per-subject addenda, or stay monolithic?
- [ ] Q7 — What is the empty-state of `workflows/generic.md` once specific workflows exist — verbatim old monolith, or a "ask user to clarify subject" probe?
- [ ] Q8 — Migration: one big PR or phase-by-phase with eval gates between?

---

## 11. Appendix

### Methodology

- **Sources consulted:**
  - `SKILL.md` (full read)
  - `references/criteria.md` (head + structure)
  - `references/registries.md` (ecosystem coverage)
  - `evals/evals.json` (full)
  - `scripts/registry-lookup.ps1` (existence + ecosystem coverage from criteria.md)
  - All five `.projex/` proposals + closed walkthrough
  - `projex/eval-projex.md` and `projex/navigate-projex.md` for output format
- **Lenses used:** First Principles (§4.1, §5), Inversion (§5.1), Constraint Mapping (§5.2, §5.3)
- **Tier rationale:** Standard. Stakes are moderate (skill is in active use, queued backlog is real, but no production blast radius), uncertainty is moderate (taxonomy granularity is the main unknown), and the recommendation is a structural one — not a stake-the-house decision.

### Dissenting View (Steel-Manning Counter)

The strongest argument for keeping the monolith — that a smart agent skips what doesn't apply — is real but loses to the *queued backlog*. Each new proposal makes the shared spine harder to read, harder to test, and forces every subject to pay the cognitive cost of features only some subjects need. The monolith was right for v0 discovery; the pivot is right for v1 scaling.

### Iteration History

| Date | Mode | Scope | Summary |
|---|---|---|---|
| 2026-04-07 | Initial | Full evaluation | First draft framing the redesign for navigate-projex handoff |

---

**Handoff:** Run `/navigate-projex install-auditor subject-typed redesign` next, referencing this eval. The navigation document should consume Findings F1–F8, the taxonomy in §5.3, the architecture sketch in §5.4, and the phased Next Steps in §9 as its starting roadmap.

**Status (2026-04-07):** Consumed by [.projex/2604070218-install-auditor-subject-typed-redesign-nav.md](2604070218-install-auditor-subject-typed-redesign-nav.md). The 6 phases + continuous Phase 6, the 8 open questions, and the risk register have all been carried into the navigation. Phase 0 (taxonomy & classifier lock-in) is the current focus.
