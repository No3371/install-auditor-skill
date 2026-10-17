# Runtime Cross-Plan Consistency Pass

> **Status:** Ready
> **Author:** Claude (Opus)
> **Parent:** Orchestrator
> **Source:** Direct request (orchestrator) — follow-ups from the ten 2026-10-16 rubric-refresh walkthroughs + five stewardship review evals
> **Related Projex:** 2610161941-shared-version-integrity-floor-walkthrough.md | 2610162003-ide-plugin-rubric-refresh-walkthrough.md | 2610162004-container-image-rubric-refresh-walkthrough.md | 2610162004-generic-fallback-and-classifier-refresh-walkthrough.md | 2610162005-ci-action-rubric-refresh-walkthrough.md | 2610162006-browser-extension-rubric-refresh-walkthrough.md | 2610162006-cli-binary-rubric-refresh-walkthrough.md | 2610162006-desktop-app-rubric-refresh-walkthrough.md | 2610162007-agent-extension-rubric-refresh-walkthrough.md | 2610162007-remote-integration-rubric-refresh-walkthrough.md | 2610162010-registry-package-rubric-refresh-walkthrough.md | 2610161927-registry-package-and-ci-action-stewardship-review-eval.md | 2604070218-install-auditor-subject-typed-redesign-nav.md
> **Worktree:** Yes

---

## Summary

Reconciles the skill's runtime files after the ten subject refreshes: one §4.3 plug-in heading name, no `4.6` section headings that clash with shared §4.6, Homebrew routing that matches the cli-binary / desktop-app rubrics, shared `references/registries.md` rows that match the addenda, five subject-file contradictions, the moved OpenSSF Scorecard API host, and a STEWARDSHIP watch list. No rating semantics of the closed plans change; each edit makes one file agree with the rule another file already states.

**Scope:** `SKILL.md`, `references/**`, `workflows/**`, `scripts/registry-lookup.{py,ps1}` (Scorecard host only), `STEWARDSHIP.md` (new Watch List + checklist step 3 only). Not `evals/`, not STEWARDSHIP inventory dates.
**Estimated Changes:** 19 files, ~45 text edits (no logic change; 2 URL constants in scripts).

---

## Objective

### Problem / Gap / Need

Ten plans edited overlapping files in parallel on 2026-10-16. Their walkthroughs left cross-file follow-ups (verified against base `99de6f7` in Context below):

- cli-binary addendum calls its §4.3 plug-in `## Own Code vs Third-Party Components (§4.3)`; six addenda use `## CVE Scope (§4.3)`; `references/criteria.md` §4.3 names no heading (it does for §4.6).
- Four workflows still title their alternatives section `### 4.6 Alternatives`, while shared §4.6 is Version & Update Integrity (desktop-app / cli-binary already dropped the number). cli-binary alone prefixes its section headings with `§`.
- `references/classifier.md` routes only Homebrew **core** formulae; says core is "build-from-source" (bottles are built by Homebrew CI); lists `volta` (declared unmaintained, cli-binary T10) and no `vim.pack`; ignores bare `brew install <name>` that installs a cask. `SKILL.md` row 7 says "(not `--cask`)", which misroutes that case.
- `references/registries.md`: JetBrains "Medium-High (JetBrains review process)" contradicts the ide-plugin addendum (Plugin Verifier = compatibility, not anti-malware); container table lacks hardened catalogs and frozen namespaces; Go row flags `GONOSUMDB` but gives no fix.
- `SKILL.md` Red Flag sentence "Tag-pinned actions … HIGH" reads as covering immutable-release tags that the ci-action addendum rates LOW.
- Browser addendum Tier 1 / Tier 3 and workflow APPROVED bullets count every store removal, though its MV2 section says an MV2-retirement removal is not for cause.
- Container: workflow HTML comment still says "GCR"; addendum rates `securityContext.runAsUser: 0` Medium vs the root-at-runtime rule (dev LOW / production HIGH).
- cli-binary: Scoring impact "`curl … | sh` from known vendor = Tier 2 minimum" vs Tier 3 trigger "pipe-to-shell … from any source"; `references/criteria.md` §4.3 defers third-party no-fix conditions to "the routed workflow's mitigations", but only container names any.
- `workflows/remote-integration.md` lists "Add connector" (remote MCP) with no note that tool-adding connectors route to agent-extension 8a.
- Scorecard API host `api.securityscorecards.dev` → `api.scorecard.dev` (verified, see Context).
- STEWARDSHIP has event triggers but no source watch list (F-P1; container / remote-integration / agent-extension / desktop-app walkthroughs each proposed items).

### Success Criteria

- [ ] `grep -c '^## CVE Scope (§4.3)$' references/criteria/*.md` → 1 for each of browser-extension, ci-action, cli-binary, container-image, desktop-app, ide-plugin, registry-package; `grep -rn 'Own Code vs Third-Party' SKILL.md references workflows` → 0 hits
- [ ] `grep -nE '^### §?4\.6 ' workflows/*.md` → only `agent-extension.md`, `cli-binary.md`, `remote-integration.md` (`4.6 Version & Update Integrity`) and `container-image.md` (`4.6 Supply Chain & Version Integrity …`); `grep -n '^### §' workflows/*.md` → 0 hits
- [ ] `references/classifier.md` has a third-party-tap row and a bare-name cask row; no `build-from-source`, no `volta`; row 3 contains `vim.pack.add()`
- [ ] `SKILL.md` ≤ 15,500 B (expected 15,488); contains `Mutable tag-pinned actions` and `(not a cask)`
- [ ] `references/registries.md`: no `Medium-High (JetBrains review process)`; has `dhi.io` and `bitnamilegacy` rows; Go row contains `remove the setting`
- [ ] Browser addendum lines for Tier 1 / Tier 3 removal and workflow APPROVED removal bullet each carry the MV2-retirement carve-out
- [ ] `grep -c 'GCR,' workflows/container-image.md` → 0; `runAsUser: 0` row no longer rated `Medium`
- [ ] `grep -c 'Tier 2 minimum' references/criteria/cli-binary.md` → 0; cli-binary CVE Scope has a no-fix mitigation bullet; `references/criteria.md` §4.3 names a default mitigation set
- [ ] `workflows/remote-integration.md` has a `**Scope:**` note naming agent-extension 8a
- [ ] `grep -rn 'securityscorecards' SKILL.md references workflows scripts` → 0 hits
- [ ] `STEWARDSHIP.md` has `## Watch List` with one row per inventory workflow + a shared row; inventory table byte-identical to base
- [ ] `python3 evals/run_evals.py validate`, `python3 -m unittest discover -s evals -p "test_*.py"`, `python3 -m unittest discover -s tests` all pass, results unchanged vs base

### Out of Scope

- `evals/**` (sibling eval-refresh planner owns it; hand-offs in Notes)
- STEWARDSHIP inventory Last Reviewed / Next Due columns and the nav Phase 6 log (orchestrator)
- New rating rules, new flag levels, threshold changes (e.g. naming a level for "strong negative" — see Notes → Rejected)
- `.projex/` closed documents (point-in-time records)
- Plan-text count errors in closed plans (I1–I10, R1–R10)

---

## Context

### Current State

Verified against `99de6f7` on 2026-10-17. Line numbers are base positions; anchor edits on the quoted text, not the number.

- §4.3 plug-ins: `## CVE Scope (§4.3)` in browser-extension:166, ci-action:209, container-image:184, desktop-app:185, ide-plugin:182, registry-package:134; cli-binary:175 `## Own Code vs Third-Party Components (§4.3)`, cited by `workflows/cli-binary.md:259-261`. agent-extension and remote-integration have no §4.3 plug-in (shared default applies). `references/criteria.md:153` Addendum line names no heading; `:249` names the §4.6 heading.
- `### 4.6 Alternatives…`: browser-extension:314, ci-action:224, ide-plugin:362, registry-package:451. desktop-app:333 `### Alternatives (desktop-app-specialized)`, cli-binary:289 `### Alternatives & Ecosystem Fit` (already renamed). cli-binary:220/241/252/264/272/279 use `### §4.n`; all other workflows use `### 4.n`. No file outside `.projex/` cites any of these heading strings (grep checked); no test parses headings.
- Homebrew: `references/classifier.md:81` core row ("Formula review + checksum + build-from-source"), `:82` cask row; signal rows `:95` (ide-plugin, "packer spec"), `:98` (desktop-app), `:99` (cli-binary, "Homebrew core", "volta"). `SKILL.md:51` row 7 "(not `--cask`)". `workflows/cli-binary.md:44-45` and `references/criteria/cli-binary.md:21-22` already split core vs third-party tap and use "bottles built … by Homebrew CI". `workflows/desktop-app.md:42-43` cask rows; `references/criteria/desktop-app.md:20` tap-cask row lacks the `brew trust` note cli-binary carries.
- Homebrew facts (primary source, `Homebrew/brew` repo via GitHub code search 2026-10-17): `manpages/brew.1` / completions: `install` = "Install a formula or cask"; `Library/Homebrew/cli/named_args.rb`: when a name matches both, Homebrew treats it as a formula and tells the user to "specify the `--cask` flag"; `docs/Tap-Trust.md`: `brew trust --formula|--cask user/repository/item`.
- `SKILL.md` = 15,482 B; ceiling 15,500 B (set in `2610161941-shared-version-integrity-floor-plan.md`). Planned edits: −2 B (row 7) + 8 B (Red Flag) = 15,488 B (simulated).
- `references/registries.md`: JetBrains `:69`, Vim `:70`, container table `:41-50`, Go `:29`. ide-plugin addendum `:25` JetBrains = "Manual review, but the Plugin Verifier is a compatibility checker, not anti-malware"; container addendum `:22-23` hardened catalogs, `:29`/`:40` frozen namespace = HIGH flag; registry addendum `:39` Go check; registry plan trace R11 expects "Recommendation: remove pattern for public modules".
- Browser addendum `:117` "A CWS removal caused by MV2 retirement is not a removal for cause", `:163` "MV2-retirement or inactivity removals are not compromises"; uncarved bullets `:182` (Tier 1), `:204` (Tier 3); workflow `:379` (Toward APPROVED).
- Container workflow `:3` comment "ECR, GCR,"; addendum `:108` root-at-runtime rule ("This row is rated only by this rule"), `:141` `runAsUser: 0` = Medium.
- cli-binary addendum `:109` "Tier 2 minimum", `:112` irm = same as curl, `:163` Tier 3 trigger "from any source"; cli plan trace T14 expects "Tier 2+" (Tier 3 satisfies it). `references/criteria.md:150` "the routed workflow's mitigations"; only container addendum `:194` lists mitigations.
- remote-integration workflow `:22-25` addendum paragraph, `:44` "Add connector" row; classifier `:77` routes tool-adding connectors to 8a; agent-extension workflow `:108-109` cites remote-integration addendum §1/§5/§6 (headings must not change).
- Scorecard: `references/criteria.md:48`, `:317`; `workflows/registry-package.md:276`; `scripts/registry-lookup.py:341`; `scripts/registry-lookup.ps1:353`. Primary source (`ossf/scorecard` README @ `337101f`): "To query pre-calculated scores of OSS projects, use the [REST API](https://api.scorecard.dev)"; badge path `https://api.scorecard.dev/projects/github.com/ossf/scorecard/badge` (same `/projects/github.com/<owner>/<repo>` shape); `governance/meetings/2024.md`: old host kept 12 months from March 2024, then redirects. Tests route all non-registry hosts to a failing stub (`tests/test_lookup_scripts.py:241`), so the URL change is test-neutral.

### Key Files

| File | Role | Change Summary |
|------|------|----------------|
| `SKILL.md` | Dispatcher | Row 7 "(not a cask)"; Red Flag "Mutable tag-pinned" |
| `references/criteria.md` | Shared rubric | §4.3 heading contract + default mitigations; Scorecard host ×2 |
| `references/classifier.md` | Routing rule | Tap + bare-cask rows; core wording; signal rows 3/6/7 |
| `references/registries.md` | Shared trust table | JetBrains, Vim/Neovim, hardened + frozen container rows, Go fix |
| `references/criteria/cli-binary.md` | Addendum | §4.3 heading; no-fix mitigation bullet; Tier 3 wording |
| `references/criteria/browser-extension.md` | Addendum | MV2 carve-out ×2 |
| `references/criteria/container-image.md` | Addendum | `runAsUser: 0` follows root rule |
| `references/criteria/desktop-app.md` | Addendum | Tap-cask `brew trust` note |
| `workflows/{browser-extension,ci-action,ide-plugin,registry-package}.md` | Workflows | Drop `4.6` from Alternatives heading |
| `workflows/cli-binary.md` | Workflow | `§4.n` → `4.n`; §4.3 plug-in citation |
| `workflows/browser-extension.md` | Workflow | MV2 carve-out in APPROVED bullet |
| `workflows/container-image.md` | Workflow | Header comment registries |
| `workflows/desktop-app.md` | Workflow | Bare-name cask signal |
| `workflows/remote-integration.md` | Workflow | Scope note → agent-extension 8a |
| `workflows/registry-package.md` | Workflow | Scorecard host |
| `scripts/registry-lookup.py`, `scripts/registry-lookup.ps1` | Lookup scripts | Scorecard host constant |
| `STEWARDSHIP.md` | Review cadence | `## Watch List`; checklist step 3 pointer |

### Dependencies
- **Requires:** base `claude/youthful-dijkstra-5ov1kt` at `99de6f7` or later with all ten refresh plans closed (true now).
- **Blocks:** nothing hard. The sibling eval-refresh plan may cite the renamed headings; it edits only `evals/`, so no file overlap. The orchestrator's later STEWARDSHIP date edit touches the inventory table only (this plan adds a separate section).

### Constraints
- `SKILL.md` ≤ 15,500 B (UTF-8 bytes).
- Keep each file's wrap style: hard-wrapped workflows (`browser-extension`, `ci-action`, `cli-binary`, `ide-plugin`, `registry-package`, `remote-integration`, `desktop-app` prose) stay ≤ 80 columns per wrapped line; table rows and unwrapped files stay single-line.
- Do not rename remote-integration addendum `## §n — …` headings (agent-extension cites §1/§5/§6).
- Reconcile only: every After text restates a rule already in another file or adds a wording carve-out that file already states elsewhere.
- Source Hygiene: no projex IDs/filenames in edited files.

### Assumptions
- No external consumer parses workflow heading text (verified for repo: no hits in `evals/`, `tests/`, `scripts/`).
- `api.scorecard.dev` serves the same JSON shape (`score`, `date`, `checks[].name/score`) as the old host — the 2024 notice describes a redirect of the same API, and the README badge path matches. Executor: if network allows, one GET of `https://api.scorecard.dev/projects/github.com/ossf/scorecard` confirms; if blocked, record "unverified live" in the log and proceed.
- Homebrew 6.0.0 as the `brew trust` introduction version is carried from the closed cli-binary plan; this plan only copies that existing claim.

### Impact Analysis
- **Direct:** files in Key Files.
- **Adjacent:** eval prompts/assertions that quote `Tier 2 minimum`, `Medium-High`, heading names, or `build-from-source` (none found except eval 20 description wording, already handed to the eval planner).
- **Downstream:** auditors reading the skill: cli-binary known-vendor pipe-to-shell audits now always run at Tier 3 depth (verdict unchanged; T14 "Tier 2+" holds); bare `brew install <cask-only-name>` now routes to desktop-app.

---

## Implementation

### Overview

Seven independent text-edit steps grouped by concern, then one verification sweep. Steps touch disjoint hunks; order only matters for Step 3's byte check. Use exact-string edits (each old string occurs once in its file).

### Step 1: Harmonise §4.3 plug-in and workflow section headings

**Objective:** One plug-in heading name; no clash with shared §4.6; uniform `4.n` prefix.
**Confidence:** High
**Depends on:** None
**Do-Projex:** Encouraged

**Files:**
- `references/criteria/cli-binary.md`
- `references/criteria.md`
- `workflows/cli-binary.md`, `workflows/browser-extension.md`, `workflows/ci-action.md`, `workflows/ide-plugin.md`, `workflows/registry-package.md`

**Changes:**

```markdown
<!-- references/criteria/cli-binary.md -->
// Before:
## Own Code vs Third-Party Components (§4.3)
// After:
## CVE Scope (§4.3)

<!-- references/criteria.md §4.3 (line ~153) -->
// Before:
- **Addendum:** draws the own-code / third-party line for its artifact type and names its scan and VEX sources. It does not change the verdict classes above.
// After:
- **Addendum:** under one heading `## CVE Scope (§4.3)`, draws the own-code / third-party line for its artifact type, names its scan and VEX sources, and may name mitigations for a third-party component with no fix. It does not change the verdict classes above. No plug-in → the definitions above apply.

<!-- workflows/cli-binary.md (§4.3 section) -->
// Before:
- Classify CVEs as own code or third-party component per
  `references/criteria/cli-binary.md` Own Code vs Third-Party Components
  (§4.3); verdict classes per `SKILL.md` "Blocking CVE".
// After:
- Classify CVEs as own code or third-party component per
  `references/criteria/cli-binary.md` CVE Scope (§4.3); verdict classes
  per `SKILL.md` "Blocking CVE".

<!-- workflows/cli-binary.md headings -->
### §4.1 Provenance — Binary Authenticity      → ### 4.1 Provenance — Binary Authenticity
### §4.2 Maintenance & Project Health          → ### 4.2 Maintenance & Project Health
### §4.3 Security — Vulnerabilities & Incidents → ### 4.3 Security — Vulnerabilities & Incidents
### §4.4 Permissions & Access                  → ### 4.4 Permissions & Access
### §4.5 Reliability & Stability               → ### 4.5 Reliability & Stability
### §4.6 Version & Update Integrity            → ### 4.6 Version & Update Integrity

<!-- Alternatives headings -->
workflows/browser-extension.md: ### 4.6 Alternatives (browser-extension-specialized) → ### Alternatives (browser-extension-specialized)
workflows/ci-action.md:         ### 4.6 Alternatives                                → ### Alternatives
workflows/ide-plugin.md:        ### 4.6 Alternatives (ide-plugin-specialized)       → ### Alternatives (ide-plugin-specialized)
workflows/registry-package.md:  ### 4.6 Alternatives (registry-specialized)         → ### Alternatives (registry-specialized)
```

**Rationale:** `CVE Scope (§4.3)` is the majority name (6 of 7) and already cited by browser-extension; the §4.6 contract sentence is mirrored for §4.3. Dropping the number (as desktop-app and cli-binary did) keeps `4.6` meaning Version & Update Integrity everywhere. The mitigation clause in the contract prepares Step 5c.

**Verification:** `grep -c '^## CVE Scope (§4.3)$' references/criteria/*.md` (7 files = 1, agent-extension / remote-integration = 0); `grep -rn 'Own Code vs Third-Party' SKILL.md references workflows` empty; `grep -nE '^### (§|4\.6 Alt)' workflows/*.md` empty.

**If this fails:** `git checkout -- <file>` for the affected file and redo the exact-string edit.

---

### Step 2: Homebrew and Neovim routing in the classifier and desktop-app files

**Objective:** Classifier routes third-party-tap formulae and bare cask names the way the cli-binary and desktop-app rubrics already describe; stale signals refreshed.
**Confidence:** High
**Depends on:** None
**Verify-Projex:** Encouraged (routing text; misplacement silently misroutes audits)

**Files:**
- `references/classifier.md`
- `workflows/desktop-app.md`
- `references/criteria/desktop-app.md`

**Changes:**

```markdown
<!-- references/classifier.md Routing Overrides: replace the core row, keep the cask row, add two rows after it -->
// Before:
| CLI via Homebrew core (`brew install <formula>`) | cli-binary | Formula review + checksum + build-from-source; casks route to desktop-app |
| App via Homebrew cask (`brew install --cask`) | desktop-app | Cask installs a packaged application |
// After:
| CLI via Homebrew core (`brew install <formula>`) | cli-binary | Maintainer-reviewed formula + pinned source checksum + bottle built and attested by Homebrew CI; casks route to desktop-app |
| App via Homebrew cask (`brew install --cask`) | desktop-app | Cask installs a packaged application |
| Formula from a third-party tap (`brew install <user>/<tap>/<formula>`, or `brew tap <user>/<tap>` then the short name) | cli-binary | Same install pipe as core, but the gate is the tap owner's repo, not Homebrew review; `workflows/cli-binary.md` rates the tap. A tap cask (`--cask <user>/<tap>/<cask>`) routes to desktop-app |
| Bare `brew install <name>` where no formula has that name but a cask does (`formulae.brew.sh/cask/<name>`) | desktop-app | `brew install` installs a formula or a cask; a formula wins when both exist (Homebrew then points to `--cask`) |

<!-- references/classifier.md Extended Signal Patterns -->
// Row 3, Before:  … Sublime Package Control manifest, vim-plug / lazy.nvim / packer spec, MELPA recipe …
// Row 3, After:   … Sublime Package Control manifest, vim-plug / lazy.nvim / packer spec, Neovim `vim.pack.add()`, MELPA recipe …
// Row 6, Before:  … `brew install --cask`, `winget install`, …
// Row 6, After:   … `brew install --cask` (or a bare name that resolves only to a cask), `winget install`, …
// Row 7, Before:  … `brew install <formula>` (Homebrew core), version managers (nvm / pyenv / rustup / volta), …
// Row 7, After:   … `brew install <formula>` (Homebrew core or third-party tap `<user>/<tap>/<formula>`), version managers (nvm / pyenv / rustup / mise), …

<!-- workflows/desktop-app.md Identify table -->
// Before:
| Homebrew Cask (official) | `brew install --cask <name>`, `formulae.brew.sh/cask/*` | Install analytics on formulae.brew.sh |
// After:
| Homebrew Cask (official) | `brew install --cask <name>` (or bare `brew install <name>` when only a cask has that name), `formulae.brew.sh/cask/*` | Install analytics on formulae.brew.sh |

<!-- references/criteria/desktop-app.md tap-cask row, last cell -->
// Before: … | Outside homebrew-cask review and its Gatekeeper policy; trust = tap owner identity |
// After:  … | Outside homebrew-cask review and its Gatekeeper policy; trust = tap owner identity. `brew trust` (Homebrew 6.0.0+) records consent, not review |
```

**Rationale:** cli-binary already rates taps (`workflows/cli-binary.md:45`, addendum `:22`) and desktop-app already rates tap casks; only the router lacked the rows. Homebrew facts come from `Homebrew/brew` sources (Context). `packer` kept as a signal (existing configs still use it) — `vim.pack.add()` added. `volta` → `mise` per cli-binary T10 (Volta unmaintained).

**Verification:** `grep -c 'build-from-source\|volta' references/classifier.md` → 0; `grep -c 'third-party tap' references/classifier.md` ≥ 2; `grep -c 'vim.pack.add()' references/classifier.md` → 1; cell counts per table row (escaped `\|` ignored): `python3 -c "import re;[print(n,len(re.split(r'(?<!\\\\)\|',l.rstrip()))-2) for n,l in enumerate(open('references/classifier.md',encoding='utf-8'),1) if l.startswith('|')]"` → Confidence Examples rows 2, Routing Overrides rows 3, Extended Signal rows 4 (base distribution: 5×2, 20×3, 12×4; after: 5×2, 22×3, 12×4).

**If this fails:** `git checkout -- references/classifier.md workflows/desktop-app.md references/criteria/desktop-app.md`.

---

### Step 3: `SKILL.md` row 7 and CI Red Flag (byte ceiling)

**Objective:** Step 0 summary stops excluding only `--cask`; Red Flag tag sentence names mutable tags only.
**Confidence:** High
**Depends on:** None (byte check after both edits)
**Do-Projex:** Encouraged

**Files:**
- `SKILL.md`

**Changes:**

```markdown
// Row 7, Before:
| 7 | cli-binary | `curl … \| sh`, `irm … \| iex`, GitHub Releases binary, `brew install <formula>` (not `--cask`), nvm/pyenv/rustup, vendor-hosted executables |
// Row 7, After:
| 7 | cli-binary | `curl … \| sh`, `irm … \| iex`, GitHub Releases binary, `brew install <formula>` (not a cask), nvm/pyenv/rustup, vendor-hosted executables |

// Red Flag sentence, Before:
… Tag-pinned actions from official/verified publishers are HIGH → CONDITIONAL (pin to SHA) per `workflows/ci-action.md`.
// After:
… Mutable tag-pinned actions from official/verified publishers are HIGH → CONDITIONAL (pin to SHA) per `workflows/ci-action.md`.
```

**Rationale:** "(not a cask)" covers bare names that resolve to a cask (Step 2) and saves 2 B; "Mutable" matches the Red Flag title and the ci-action addendum's LOW rating for verified immutable-release tags (ci-action plan note, +8 B).

**Verification:** `wc -c SKILL.md` → 15488 (must be ≤ 15500); `grep -c 'Mutable tag-pinned actions' SKILL.md` → 1; `grep -c '(not a cask)' SKILL.md` → 1.

**If this fails:** over ceiling → drop the Red Flag edit (keep row 7) and record it in the log; `git checkout -- SKILL.md` to restart.

---

### Step 4: `references/registries.md` rows match the addenda

**Objective:** Shared trust table stops contradicting the ide-plugin, container-image and registry-package addenda.
**Confidence:** High
**Depends on:** None
**Do-Projex:** Encouraged

**Files:**
- `references/registries.md`

**Changes:**

```markdown
<!-- Go row, end of line -->
// Before: … disables checksum verification — flag (`GOINSECURE` does not).
// After:  … disables checksum verification — flag; Recommendation: remove the setting, or narrow the pattern to private module paths (`GOINSECURE` does not disable it).

<!-- Container Images table: insert after the "Official Docker Hub images (library/)" row -->
| Hardened catalogs (Docker Hardened Images `dhi.io`, Chainguard `cgr.dev`) | High — when signed attestations verify against the publisher's documented key or identity |

<!-- Container Images table: insert after the "Self-hosted registry (unknown)" row -->
| Frozen / legacy namespace (e.g. `bitnamilegacy`) | Low — no further updates; HIGH flag `frozen namespace` (`references/criteria/container-image.md`) |

<!-- IDE / Editor Plugins table -->
// Before:
| JetBrains Marketplace | Medium-High (JetBrains review process) |
| Vim-Plug / GitHub-sourced Vim plugins | Low-Medium (no central review) |
// After:
| JetBrains Marketplace | Medium (manual listing review; the Plugin Verifier checks compatibility, not malware — see `references/criteria/ide-plugin.md`) |
| Vim / Neovim plugins from GitHub (vim-plug, lazy.nvim, `vim.pack`) | Low-Medium (no central review; trust the repo and the pinned commit) |
```

**Rationale:** Each new value restates the addendum (ide-plugin `:25`, `:27`; container `:22-23`, `:29`, `:35`, `:40`; registry-package R11 trace). JetBrains moves to the VS Code Marketplace level, the closest addendum-equivalent.

**Verification:** `grep -c 'dhi.io\|bitnamilegacy\|remove the setting' references/registries.md` → 3; `grep -c 'Medium-High (JetBrains' references/registries.md` → 0.

**If this fails:** `git checkout -- references/registries.md`.

---

### Step 5: Subject-file contradictions (browser, container, cli-binary, remote-integration, shared §4.3)

**Objective:** Remove the five in-file / cross-file contradictions left by the refreshes.
**Confidence:** High (5a, 5b, 5d) | Medium (5c — wording of the default mitigation set)
**Depends on:** Step 1 (5c fills the plug-in clause Step 1 adds)
**Verify-Projex:** Encouraged (5c touches verdict-adjacent text)

**Files:**
- `references/criteria/browser-extension.md`, `workflows/browser-extension.md`
- `references/criteria/container-image.md`, `workflows/container-image.md`
- `references/criteria/cli-binary.md`, `references/criteria.md`
- `workflows/remote-integration.md`

**Changes:**

```markdown
<!-- 5a. references/criteria/browser-extension.md Tier 1 -->
// Before: - No known incidents or store removals in search results
// After:  - No known incidents or store removals in search results (a removal for MV2 retirement or inactivity does not count — § Manifest Version)
<!-- 5a. references/criteria/browser-extension.md Tier 3 -->
// Before: - Known prior removal or policy violation from any store
// After:  - Known prior removal or policy violation from any store (an MV2-retirement or inactivity removal does not count)
<!-- 5a. workflows/browser-extension.md Toward APPROVED -->
// Before: - No known incidents or store removals
// After:  - No known incidents or store removals (MV2-retirement or inactivity
//           removals excepted)
//         (two wrapped lines, continuation indented two spaces)

<!-- 5b. workflows/container-image.md header comment -->
// Before:
Handles OCI/Docker container images from Docker Hub, GHCR, Quay, ECR, GCR,
and other registries, whether pulled directly (`docker pull`), referenced
// After:
Handles OCI/Docker container images from Docker Hub, Docker Hardened
Images, GHCR, Quay, ECR, Google Artifact Registry (incl. legacy `gcr.io`)
and other registries, whether pulled directly (`docker pull`), referenced
<!-- 5b. references/criteria/container-image.md Medium-risk runtime table -->
// Before:
| `securityContext.runAsUser: 0` | Medium | Explicit root; prefer a non-zero UID |
// After:
| `securityContext.runAsUser: 0` | LOW on a dev workstation; HIGH in production (Layer Risk Patterns → Scoring impact) | Explicit root at runtime; rated only by the root-at-runtime rule, like `USER root` |
<!-- 5b. references/criteria/container-image.md Layer Risk Patterns → Scoring impact, first bullet start -->
// Before: - Root at runtime (first row): dev workstation = …
// After:  - Root at runtime (first row, or `securityContext.runAsUser: 0` in a manifest): dev workstation = …

<!-- 5c. references/criteria/cli-binary.md Install Script Risk → Scoring impact -->
// Before: - `curl … | sh` from known vendor = Tier 2 minimum, note pipe-to-shell risk; condition or recommendation = executed-bytes rule
// After:  - `curl … | sh` from known vendor = Tier 3 (Tier 3 trigger: pipe-to-shell from any source), note pipe-to-shell risk; condition or recommendation = executed-bytes rule
<!-- 5c. references/criteria/cli-binary.md CVE Scope (§4.3): insert after the "**Fixed release:**" bullet -->
- **Third-party component, no fixed release (not KEV):** HIGH flag per `references/criteria.md` §4.3. Condition: avoid the affected feature or input the advisory names; run without sudo / Administrator; no network-exposed or long-running use of the affected path; pin the audited release; re-audit when a binary release ships the fix. A scanner's "not called" reachability result supports the condition as a note, not as VEX.
<!-- 5c. references/criteria.md §4.3 Fixed release bullet, last sentence -->
// Before: Third-party component with no fix → condition: the routed workflow's mitigations, plus re-audit when a fix ships.
// After:  Third-party component with no fix → condition: the mitigations the routed workflow or addendum names (default when neither names any: keep untrusted input away from the affected component, run with least privilege, pin the audited version; list them in the Recommendation), plus re-audit when a fix ships.

<!-- 5d. workflows/remote-integration.md: insert a paragraph after "`references/criteria.md` §4.6, which it only tightens." (before the `---`) -->

**Scope:** a remote MCP server or AI-assistant connector that adds tools
the assistant calls routes to `workflows/agent-extension.md` (8a;
`references/classifier.md` Routing Overrides). That audit runs this
workflow's grant checks (addendum §1, §5, §6) as a sub-step. Audit here
grants that expose no tools to the user's agent, incl. AI apps that read
your data.

<!-- 5d. workflows/remote-integration.md Identify table row -->
// Before: | "Add connector" in an AI assistant (remote MCP over HTTP + OAuth, no local code) | AI connector | Usually OAuth |
// After:  | "Add connector" in an AI assistant (remote MCP over HTTP + OAuth, no local code; tool-adding connectors are audited under agent-extension 8a — see Scope) | AI connector | Usually OAuth |
```

**Rationale:**
- 5a: browser addendum `:117` / `:163` already exempt MV2-retirement and inactivity removals; the walkthrough's Plan Improvement asks for the carve-out in every removal bullet.
- 5b: container addendum `:108` says root at runtime is rated only by the dev/production rule; `runAsUser: 0` is the manifest form of the same fact. Header comment matches the intro (`:16-18`).
- 5c: Tier 3 trigger is the stricter, explicit threshold in both workflow (`:107-113`) and addendum (`:163`); "Tier 2 minimum" is satisfied by Tier 3, and T14 ("Tier 2+") holds — depth changes, verdict does not. The mitigation bullet mirrors container `:194` for binaries; the shared default closes the dangling "routed workflow's mitigations" reference for addenda that name none. Neither changes a verdict class (§4.3 table untouched).
- 5d: classifier `:77` and worked example 7 already route tool-adding connectors to 8a; no remote-integration heading changes.

**Verification:** `grep -c 'MV2' references/criteria/browser-extension.md` 15 → 17, `workflows/browser-extension.md` 11 → 12; `grep -c 'GCR,' workflows/container-image.md` → 0; `grep -n 'runAsUser: 0' references/criteria/container-image.md` shows no `| Medium |`; `grep -c 'Tier 2 minimum' references/criteria/cli-binary.md` → 0; `grep -c 'no fixed release (not KEV)' references/criteria/cli-binary.md` → 1; `grep -c 'default when neither names any' references/criteria.md` → 1; `grep -c '^\*\*Scope:\*\*' workflows/remote-integration.md` → 1; `grep -n '^## §' references/criteria/remote-integration.md` unchanged vs base. Paper trace: cli T14 (`irm … | iex` from vendor page) → Tier 3, LOW-MEDIUM flag, CONDITIONAL-leaning per Verdict Notes — same verdict as plan T14; container T12 (production root) → HIGH → CONDITIONAL, dev root via `runAsUser: 0` → LOW note.

**If this fails:** `git checkout -- <file>` per sub-step; sub-steps are independent.

---

### Step 6: OpenSSF Scorecard API host

**Objective:** Point all Scorecard references at the current host.
**Confidence:** High (primary source verified; live response shape unverified — see Assumptions)
**Depends on:** None
**Do-Projex:** Encouraged

**Files:**
- `references/criteria.md` (2 places), `workflows/registry-package.md`, `scripts/registry-lookup.py`, `scripts/registry-lookup.ps1`

**Changes:**

```text
api.securityscorecards.dev  →  api.scorecard.dev   (all 5 occurrences; path /projects/github.com/<owner>/<repo> unchanged)
```

`workflows/registry-package.md` After (rewrap kept ≤ 80 cols):

```markdown
**Check the OpenSSF Scorecard** if a source repository is known:
`api.scorecard.dev/projects/github.com/<owner>/<repo>`. Scores
below 4/10 are a significant negative signal.
```

**Rationale:** ossf/scorecard README names `https://api.scorecard.dev` as the REST API; the old host only redirects (2024 governance notes). Scripts using the canonical host avoid depending on redirect handling in `invoke_api` / `Invoke-Api`.

**Verification:** `grep -rn 'securityscorecards' SKILL.md references workflows scripts` → empty; `python3 -m unittest discover -s tests` passes (same count as base).

**If this fails:** `git checkout -- <file>`; if the executor finds a live response shape mismatch, revert the two scripts only, keep the doc edits, and log it.

---

### Step 7: STEWARDSHIP watch list

**Objective:** Give each scheduled review a short list of sources and events to scan (F-P1 and four walkthrough proposals), without touching inventory dates.
**Confidence:** High
**Depends on:** Step 6 (shared row names the new Scorecard host)
**Do-Projex:** Encouraged

**Files:**
- `STEWARDSHIP.md`

**Changes:**

```markdown
<!-- Re-Evaluation Checklist step 3 -->
// Before: 3. Check ecosystem changelogs/announcements since last review for security-relevant changes
// After:  3. Check ecosystem changelogs/announcements since last review for security-relevant changes (start from § Watch List)

<!-- Insert after the Event-Based Triggers bullet list, before its closing `---` -->

### Watch List

Sources to scan at checklist step 3 and between reviews for the triggers above. As of 2026-10; prune or extend at each review.

| Workflow | Watch |
|---|---|
| `registry-package.md` | GitHub changelog (npm) and npm CLI releases: script approval, trusted publishing, staged publishing · blog.pypi.org: attestations, quarantine · crates.io, RubyGems and NuGet blogs: trusted publishing |
| `browser-extension.md` | Chrome and Edge MV2 timeline pages · Chrome Web Store and AMO policy posts · CISA KEV entries naming extensions |
| `container-image.md` | Docker Official Images signing replacement (none confirmed as of 2026-10) · Docker Hardened Images verification flow · `cosign` / `gh attestation` flag changes · publisher namespace freezes (e.g. `bitnamilegacy`) |
| `ci-action.md` | GitHub changelog (Actions): immutable releases, workflow lockfiles, `actions/checkout` majors |
| `ide-plugin.md` | VS Code Marketplace block-list and security posts · Open VSX / Eclipse takedowns · JetBrains Marketplace security posts |
| `desktop-app.md` | Store packaging policies (Microsoft Store, Mac App Store, Snap Store, Flathub) · Gatekeeper / notarization changes · CA/Browser Forum code-signing ballots · Homebrew cask policy |
| `cli-binary.md` | Homebrew releases: `brew trust`, `HOMEBREW_VERIFY_ATTESTATIONS` default · GitHub immutable releases and `gh release verify` |
| `agent-extension.md` | MCP spec revisions · Claude Code plugin / skill / MCP docs: component types, marketplace source types, trust gating |
| `remote-integration.md` | OAuth 2.1 RFC status · MCP authorization spec · Slack / Google API-terms changes · Google CASA program |
| `generic.md` | New installable kinds no type covers; classifier routing-override changes |
| Shared (`references/criteria.md` §4.3, §4.6, §4.7) | CISA KEV catalog · package-manager cooldown settings · OpenSSF Scorecard API (`api.scorecard.dev`) |
```

**Rationale:** Items come from: registry/ci eval F-P1; container, remote-integration, agent-extension, desktop-app walkthroughs; browser/ide eval long-term note; ide-plugin addendum V4 sources; cli-binary addendum `:59` / workflow `:157`. A separate `###` section under Event-Based Triggers leaves the inventory table (orchestrator-owned dates) untouched.

**Verification:** `grep -c '^### Watch List' STEWARDSHIP.md` → 1; table has 11 data rows; `git diff STEWARDSHIP.md` shows no change inside `## Workflow Inventory`.

**If this fails:** `git checkout -- STEWARDSHIP.md`.

---

## Verification Plan

> Per-step checks confirm each edit. This section confirms the set.

### Automated Checks
- [ ] `python3 evals/run_evals.py validate` → pass, same eval/assertion counts as base
- [ ] `python3 -m unittest discover -s evals -p "test_*.py"` → pass
- [ ] `python3 -m unittest discover -s tests` → pass, same test count as base (pwsh twins skip if absent)
- [ ] `wc -c SKILL.md` ≤ 15500
- [ ] All Success Criteria greps (Objective) return the stated values
- [ ] `git diff --stat` lists only Key Files; `git diff -- evals` empty

### Manual Verification
- [ ] Every relative reference in edited text resolves: `references/criteria/ide-plugin.md`, `references/criteria/container-image.md`, `workflows/agent-extension.md`, `workflows/cli-binary.md`, `references/classifier.md` exist; cited section names (`Manifest Version`, `Layer Risk Patterns`, `CVE Scope (§4.3)`, `Routing Overrides`, `Watch List`) exist in their files
- [ ] Hard-wrapped workflow edits: no wrapped prose line > 80 cols (`awk 'length>80 && !/^\|/' <file>` shows no new lines vs base)
- [ ] Classifier tables: edited rows keep their table's cell count
- [ ] Source Hygiene: `git diff | grep -E '^\+.*(26[01][0-9]{7}|projex)'` → empty

### Acceptance Criteria Validation
| Criterion | How to Verify | Expected Result |
|-----------|---------------|-----------------|
| One §4.3 plug-in name | grep in Step 1 | 7 × `CVE Scope (§4.3)`, 0 × old name |
| No `4.6` clash | `grep -nE '^### §?4\.6 ' workflows/*.md` | 4 files, all Version-integrity headings |
| Homebrew routing | Step 2 greps + read rows | tap + bare-cask rows present |
| SKILL.md ceiling | `wc -c` | 15488 |
| Registries agree | Step 4 greps | as stated |
| Contradictions gone | Step 5 greps + traces | as stated |
| Scorecard host | Step 6 grep | 0 old-host hits |
| Watch list | Step 7 grep | section present, inventory untouched |
| No regressions | 3 offline suites | pass, counts unchanged |

---

## Rollback Plan

1. Worktree mode: `projex-abandon.sh <repo-root> <base> projex/2610170500-runtime-cross-plan-consistency --worktree` discards everything.
2. Checkout mode: `git -C <work-root> checkout -- <Key Files>` before commit, or revert the execution commit(s) after.

---

## Notes

### Rejected / deferred candidate items
- **"`### §4.6 …` heading collisions" in agent-extension / remote-integration** (cli-binary walkthrough): not a collision — both read `### 4.6 Version & Update Integrity`, matching shared §4.6. Only cli-binary's `§` prefix differed; normalised in Step 1.
- **Naming a flag level for "strong negative"** (browser T10 sideloaded; cli-binary T3 shared copy): would set a new rating, not reconcile. Leave to the next subject review.
- **`brew install <name>` routing check inside cli-binary** (re-route mid-audit when `brew info` shows a cask): conflicts with classifier Edge-Case Discipline (no re-classification mid-audit); handled at classification (Step 2) instead.
- **SKILL.md row 7 additions (tap pattern, `mise`)**: byte budget (+13 B) would exceed 15,500 with the Red Flag edit; the full list lives in `references/classifier.md` and "(not a cask)" already covers taps.
- **STEWARDSHIP inventory row for shared `references/criteria.md` §4.6**: would touch the date-bearing table; a shared Watch List row covers it.
- **Plan-text count fixes (I1–I10, R1–R10)**: closed documents; out of scope.
- **Live Scorecard response check**: network fetch is not available to the planner; executor tries once (Assumptions).

### Eval hand-off (for the sibling eval-refresh plan; no `evals/` edits here)
- New routing cases worth adding: `brew install someuser/tools/<cli>` → cli-binary; bare `brew install <cask-only app>` (e.g. a GUI app with no formula) → desktop-app.
- Known-vendor `curl | sh` / `irm | iex` cases should expect Tier 3 depth (verdict unchanged).
- Eval 20 description: replace "build-from-source" wording if present ("bottle built and attested by Homebrew CI").

### Risks
- Concurrent edits by the eval planner or orchestrator: disjoint files/sections (`evals/`; STEWARDSHIP inventory). Mitigation: worktree execution; rebase before close.
- Classifier misroute from a mistyped row: Verify-Projex on Step 2; cell-count check.
- Scorecard JSON shape differs on the new host: scripts tolerate missing fields (`data.get(...)`); revert scripts only if a live check shows breakage.

### Split decision
`No split — heuristic tripped but steps tightly coupled` (540 lines / 42 KB, 7 steps; one `.projex/` scope). Rationale: Step 1 and 5c edit the same `references/criteria.md` §4.3 contract; Steps 2 and 3 are one Homebrew routing change split only for the `SKILL.md` byte check; Step 7 cites Step 6's host; all steps share one offline verification sweep, and the orchestrator scoped a single reconciliation plan. Each step is small and independently revertible, so execution can still checkpoint per step.

### Open Questions
- None.
