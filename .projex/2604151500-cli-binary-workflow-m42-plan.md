# CLI Binary Workflow — M4.2

> **Status:** In Progress
> **Created:** 2026-04-15
> **Author:** Claude (Opus 4.6)
> **Source:** [2604070218-install-auditor-subject-typed-redesign-nav.md](2604070218-install-auditor-subject-typed-redesign-nav.md) Phase 4, M4.2
> **Related Projex:**
> - **Roadmap:** [2604070218-install-auditor-subject-typed-redesign-nav.md](2604070218-install-auditor-subject-typed-redesign-nav.md)
> - **Framing eval:** [2604070217-subject-typed-audit-dispatch-eval.md](2604070217-subject-typed-audit-dispatch-eval.md)
> - **Taxonomy spec:** [2604070300-install-auditor-subject-type-taxonomy-def.md](2604070300-install-auditor-subject-type-taxonomy-def.md)
> - **Pattern precedent (M4.1):** [closed/2604151200-desktop-app-workflow-m41-plan.md](closed/2604151200-desktop-app-workflow-m41-plan.md)
> **Worktree:** No

---

## Summary

Create the Type 7 subject-specific workflow at `workflows/cli-binary.md` and its criteria addendum at `references/criteria/cli-binary.md`, then wire Type 7 routing and eval coverage. M4.2 closes the second Phase 4 gap: CLI binaries still fall through to `workflows/generic.md`, which knows nothing about checksum verification, GPG/Sigstore signatures, GitHub Releases provenance, install-script review (curl-pipe-bash detection), language-version managers (nvm, pyenv, rustup, volta), or the Homebrew formulae boundary (confirmed in M4.1: `brew install` formulae = Type 7).

**Scope:** Type 7 cli-binary audits — workflow file, criteria addendum, dispatcher wiring, eval coverage.
**Estimated Changes:** 4 files (2 new, 2 modified), ~500–650 lines.

---

## Objective

### Problem / Gap / Need

Type 7 (`cli-binary`) routes to `workflows/generic.md`. Current guidance is inadequate:

1. `workflows/generic.md` has no cli-binary-specific checks. No checksum verification guidance, no signature verification (GPG/Sigstore/Minisign), no GitHub Releases provenance assessment, no install-script review framework.
2. Triage thresholds (`>100K weekly downloads`) are npm-specific. CLI binaries use GitHub release download counts, Homebrew formula install counts, and vendor adoption signals — different metrics entirely.
3. No treatment of install-script risk — `curl … | sh` / `wget … | bash` patterns are the single most dangerous install vector for CLI binaries, yet generic.md says nothing about them.
4. No coverage of distribution channels specific to CLI binaries: GitHub Releases, vendor-hosted binaries, Homebrew core formulae, language-version managers (nvm/pyenv/rustup/volta/sdkman), GoReleaser/goreleaser-built releases.
5. No guidance on binary provenance: reproducible builds, SLSA attestations, build-from-source availability, pre-built vs build-from-source trust trade-offs.
6. No review path for signature/checksum verification — GPG detached signatures, Sigstore cosign, Minisign, SHA-256/SHA-512 checksum files alongside release assets.
7. Homebrew boundary confirmed in M4.1: `brew install` (core formulae) → Type 7; `brew install --cask` → Type 6.

The taxonomy spec (§7) defines: "A standalone executable installed onto `$PATH` (or equivalent), distributed outside any registry that scores publisher trust."

### Success Criteria

- [ ] `workflows/cli-binary.md` exists and follows Identify / Evidence / Subject Rubric / Subject Verdict Notes template
- [ ] `references/criteria/cli-binary.md` exists and defines cli-binary-specific scoring for distribution channel trust, signature/checksum standards, install-script risk, provenance assessment, and tier thresholds
- [ ] `SKILL.md` dispatch table row 7 routes to `workflows/cli-binary.md`
- [ ] `SKILL.md` Reference Files includes `workflows/cli-binary.md` and `references/criteria/cli-binary.md`
- [ ] `evals/evals.json` gains at least 2 Type 7 cases: one well-known signed/checksummed Tier 1 positive path, one curl-pipe-bash or unsigned binary Tier 3 negative path
- [ ] No regressions in eval ids 0–19
- [ ] Homebrew formulae boundary wired: `brew install <formula>` routes to cli-binary workflow

### Out of Scope

- New helper scripts for checksum/signature verification or install-script static analysis
- Broad rewrites to `references/criteria.md` or `references/registries.md`
- CLI tools distributed via a registry's `bin` (e.g., `npx prettier`) — those route to Type 1 (registry-package) per taxonomy
- CLI tools distributed via `brew install --cask` — those route to Type 6 (desktop-app) per M4.1
- Phase 4 M4.3–M4.5 workflows (agent-extension, remote-integration, eval gate)

---

## Context

### Current State

`SKILL.md` classifies Type 7 correctly (`curl … | sh`, GitHub Releases binary, nvm/pyenv/rustup, vendor-hosted executable URLs) but dispatches to `workflows/generic.md`. The generic workflow has no cli-binary-specific fragments — zero checksum verification, zero signature verification, zero install-script review, zero provenance assessment.

`references/registries.md` has no cli-binary distribution channel trust baseline. The taxonomy definition provides identity, examples, and routing rules, but no audit mechanics.

There is no existing Type 7 criteria addendum, no Type 7 workflow, and no Type 7 eval coverage.

### Key Files

| File | Role | Change Summary |
|------|------|----------------|
| `workflows/cli-binary.md` | **New.** Type 7 workflow | Create distribution-channel-aware workflow: binary identity extraction, checksum/signature verification, install-script review, provenance assessment, verdict notes |
| `references/criteria/cli-binary.md` | **New.** Type 7 criteria addendum | Create cli-binary-specific scoring: distribution channel trust signals, signature/checksum standards, install-script risk classification, provenance assessment, tier thresholds |
| `SKILL.md` | Dispatcher + reference-file index | Row 7 → `workflows/cli-binary.md`; add 2 Reference Files bullets |
| `evals/evals.json` | Regression + new Type 7 coverage | Add ids 20 and 21 for positive and negative Type 7 paths |

### Dependencies

- **Requires:** Phase 4 M4.1 complete (Homebrew boundary confirmed); dispatcher architecture stable; taxonomy Type 7 definition locked
- **Blocks:** Phase 4 M4.5 (eval gate); Phase 4 completion gate

### Constraints

- Workflow must use the standard 4-section template (Identify / Evidence / Subject Rubric / Subject Verdict Notes)
- Audit Coverage table and audit-confidence statement owned by `SKILL.md` Step N
- No scripts in M4.2; evidence acquisition is doc/web/release-page inspection + checksum/signature manual verification guidance
- Cross-platform: Windows, macOS, Linux binary formats and distribution channels all in scope
- Repo is clean; worktree not needed

### Assumptions

- CLI binaries span multiple distribution shapes: GitHub Releases (most common), vendor-hosted binaries, Homebrew core formulae, language-version managers (nvm/pyenv/rustup/volta), GoReleaser-style release automation, and curl-pipe-bash install scripts. The workflow must cover all without becoming unwieldy.
- Checksum + signature verification is the primary trust signal for CLI binaries (analogous to code signing for desktop apps). A binary with no checksum and no signature is categorically higher-risk.
- Install scripts (`curl … | sh`) are the single most dangerous distribution vector — they execute arbitrary code with the user's privileges before any verification. The workflow must assess install scripts distinctly from pre-built binaries.
- GitHub Releases provenance (release author, tag vs branch, CI-built attestation, asset checksums) serves as the secondary trust signal. Official org releases with CI-built artifacts and checksum files are higher trust than personal-fork releases.
- Language-version managers (nvm, pyenv, rustup, volta) are a special case: the manager itself is a cli-binary install, but packages it manages are downstream. The workflow audits the manager's own install, not the runtimes it installs.
- Homebrew core formulae act as a community trust layer (formula review, checksums, build-from-source option) and map to Type 7 per the M4.1 boundary confirmation.

### Impact Analysis

- **Direct:** New workflow, new criteria addendum, dispatcher wiring, eval additions
- **Adjacent:** `workflows/generic.md` no longer handles Type 7 once M4.2 lands, but needs no edits. `workflows/desktop-app.md` unaffected (Homebrew cask boundary already confirmed).
- **Downstream:** Phase 4 M4.5 eval gate moves one step closer. Phase 5 (default-off generic) benefits from another type leaving the fallback.

---

## Implementation

### Overview

4 steps: addendum first, workflow second, dispatcher wiring third, evals fourth. Same sequence as M4.1.

### Step 1: Create `references/criteria/cli-binary.md`

**Objective:** Define cli-binary-specific scoring extensions the workflow can cite.
**Confidence:** High
**Depends on:** None

**Files:**
- `references/criteria/cli-binary.md` (new)

**Changes:**

Create a new addendum with this structure:

```markdown
# CLI Binary — Criteria Addendum

Per-subject scoring extensions for **Type 7: cli-binary** audits.
Layers on top of `references/criteria.md`. More-specific guidance wins.

Covers: GitHub Releases binaries, vendor-hosted executables, Homebrew
core formulae, language-version managers (nvm, pyenv, rustup, volta),
install scripts (curl-pipe-bash), and GoReleaser-built releases.
Cross-platform: Windows, macOS, Linux.

## Distribution Channel Trust Signals

| Channel | Verification Gate | Adoption Metric | Trust Notes |
|---------|-------------------|-----------------|-------------|
| Homebrew core formula | Community-reviewed formula; build-from-source option; SHA-256 checksum | Install count via `brew analytics` / GitHub stars | Strong community trust; formula builds from source or verifies checksum; auditable formula file |
| GitHub Releases (org-owned, CI-built) | GitHub Actions / CI provenance; release signed by org; checksum file in assets | Download count per asset | Org-owned repo + CI-built release + checksum/signature = highest GitHub trust signal |
| GitHub Releases (personal, manual) | Author-uploaded assets; no CI provenance | Download count per asset | Lower trust — single author, no build reproducibility guarantee |
| GoReleaser / release automation | CI-built; checksums.txt auto-generated; optional Sigstore signing | Download count | Reproducible build pipeline; checksum file standard; Sigstore optional |
| Vendor-hosted binary (signed) | Vendor website + GPG/Sigstore/Minisign signature | Website traffic / brand | Trust = vendor identity + signature verifiability |
| Vendor-hosted binary (unsigned) | Vendor website only; no signature | Website traffic / brand | Trust depends entirely on vendor identity; no cryptographic verification |
| Language-version manager (rustup, volta, nvm, pyenv) | Foundation/community-maintained; well-known install script | GitHub stars + community adoption | Established tools with broad adoption; install scripts are auditable |
| Install script (curl-pipe-bash) — known vendor | Vendor provides install script at known URL | Script content auditable | Risk: pipe-to-shell bypasses verification; mitigated by vendor reputation + HTTPS |
| Install script (curl-pipe-bash) — unknown source | Unknown or unverified source | None | Highest risk: arbitrary code execution, no verification, no rollback |
| Third-party binary mirror | Non-vendor distribution site | None | Highest risk; binary provenance unverifiable; may inject payloads |

### Scoring impact

- Homebrew core formula = strong positive (community review + build-from-source + checksum)
- GitHub Releases org/CI-built with checksums = strong positive
- GoReleaser with checksums.txt = moderate-strong positive (reproducible pipeline)
- Language-version manager (established) = moderate positive (broad adoption + auditable)
- Vendor-hosted with valid signature = moderate positive (trust = vendor identity + crypto)
- GitHub Releases personal/manual with checksums = moderate positive
- Vendor-hosted unsigned = weak positive at best (vendor reputation only)
- curl-pipe-bash from known vendor = LOW-MEDIUM flag (pipe-to-shell risk, mitigated by vendor)
- curl-pipe-bash from unknown source = HIGH flag (arbitrary code execution, zero verification)
- Third-party mirror = strong negative (equivalent to unsigned .exe from unknown site)

## Signature & Checksum Standards

| Method | Strength | Verification |
|--------|----------|--------------|
| GPG detached signature (.asc/.sig) | Strong | Verify with vendor's published GPG public key; key must be available from a trusted source (keyserver, vendor site, GitHub) |
| Sigstore cosign (keyless) | Strong | Transparency log (Rekor) provides audit trail; no key management needed |
| Minisign | Strong | Ed25519-based; simpler than GPG; verify with vendor's published public key |
| SLSA provenance attestation | Strong | Build provenance chain; verify via `slsa-verifier`; strongest supply-chain signal |
| SHA-256 checksum file | Moderate | Integrity check only (no authenticity); depends on checksum file's own provenance |
| SHA-512 checksum file | Moderate | Same as SHA-256 with larger hash; same provenance caveat |
| MD5 checksum | Weak | Collision-vulnerable; legacy only; treat as absent if no SHA-256+ alternative |
| No checksum or signature | Absent | No verification possible; binary provenance unknowable |

### Scoring impact

- GPG/Sigstore/Minisign signature + checksum = strong positive
- SLSA attestation = strong positive (strongest supply-chain signal)
- SHA-256/SHA-512 checksum only (served over HTTPS from same origin) = moderate positive
- Checksum hosted separately from binary (different domain/channel) = stronger than co-hosted
- MD5 only = weak positive (note collision vulnerability)
- No checksum or signature = MEDIUM-HIGH flag (no verification path)

## Install Script Risk Classification

| Pattern | Risk | Guidance |
|---------|------|---------|
| `curl -sSL <url> \| sh` (or `bash`) | High | Arbitrary code execution; no verification before execution; MITM risk if not HTTPS; audit the script content before piping |
| `curl -sSL <url> \| sudo sh` | Critical | Same as above + root privileges; any compromise has full system access |
| `wget -qO- <url> \| sh` | High | Same risk profile as curl-pipe-sh |
| Download script → inspect → execute | Medium | User can audit before running; risk is in the auditing quality |
| Installer binary (self-extracting) | Medium | Opaque; runs arbitrary code; better than pipe-to-shell only because it can be scanned |
| Package manager install (brew, apt, dnf) | Low | Package manager mediates: formula review, checksum, sandboxing (if any) |
| Build from source | Low | User controls compilation; risk is in the build system (Makefile, cargo, go build) |

### Scoring impact

- `curl … | sudo sh` from unknown source = automatic Tier 3, push toward REJECTED
- `curl … | sh` from known vendor = Tier 2 minimum, note pipe-to-shell risk
- Download-then-inspect = moderate (depends on script complexity)
- Build from source available = positive signal (verifiable, auditable)
- Package manager mediation = positive signal (community review layer)

## Provenance Assessment

Assess binary provenance via these signals:

| Signal | Positive indicator | Negative indicator |
|--------|-------------------|-------------------|
| Build system | CI-built (GitHub Actions, etc.) with public workflow | Manual build, no CI, no build config in repo |
| Reproducible builds | Documented build process; deterministic output | "Trust me" binary with no build info |
| Source availability | Open-source repo with matching release tags | Closed-source, no repo, no tag correspondence |
| Release process | Tagged release → CI builds → signed artifacts → checksum file | Manual upload of pre-built binary |
| SLSA level | SLSA L2+ (build service generates provenance) | No SLSA attestation |
| Release frequency | Regular releases with changelogs | Sporadic or abandoned releases |

### Scoring impact

- CI-built + open-source + tagged release + signed = strongest provenance
- Open-source + manual release + checksum = moderate provenance
- Closed-source + vendor-hosted + signed = moderate provenance (vendor trust)
- No source + no CI + no signature = weakest provenance, strong negative

## Tier Thresholds (CLI Binaries)

### Tier 1 — Quick Audit

ALL of these must hold:
- Distributed via Homebrew core formula OR GitHub Releases from a well-known org/project
- Binary has checksum file AND at least one signature method (GPG/Sigstore/Minisign)
- Project is established (>= 1 year old, >= 1K GitHub stars or equivalent adoption)
- Maintained: release within last 12 months
- No known security incidents or supply-chain compromises
- No install-script-only distribution (binary download available)

### Tier 2 — Standard Audit (default)

Default when not all Tier 1 criteria are met:
- Distributed via a recognizable channel (GitHub Releases, vendor site, Homebrew)
- Checksum available (signature not required)
- Identifiable author or organization
- No known security incidents
- Available > 30 days

### Tier 3 — Deep Audit

ANY of these triggers:
- Install via `curl … | sh` or `curl … | sudo sh` from any source
- No checksum and no signature for binary download
- Binary from unknown or unverifiable source
- Third-party mirror or repackager (not original author/org)
- Shared via chat/email/forum link (not discovered via official channel)
- Single-author project with no CI and no release automation
- First release < 30 days old
- Known prior security incident or supply-chain compromise
- Binary requests elevated privileges (sudo/admin) with unclear justification
```

**Rationale:** Shared rubric has no cli-binary coverage. This addendum becomes the single reference for distribution channel trust, signature/checksum standards, install-script risk, provenance assessment, and tier thresholds calibrated to CLI binary distribution patterns.

**Verification:** File exists. Sections present: distribution channel trust signals, signature & checksum standards, install script risk classification, provenance assessment, tier thresholds.

**If this fails:** Delete `references/criteria/cli-binary.md`.

---

### Step 2: Create `workflows/cli-binary.md`

**Objective:** Author the Type 7 workflow with cross-platform CLI binary evidence and verdict guidance.
**Confidence:** High
**Depends on:** Step 1

**Files:**
- `workflows/cli-binary.md` (new)

**Changes:**

Create the workflow with this structure:

```markdown
<!--
workflows/cli-binary.md - Type 7 subject-specific workflow.
Handles CLI tools and standalone binaries distributed via GitHub
Releases, vendor-hosted downloads, Homebrew core formulae,
language-version managers (nvm, pyenv, rustup, volta), install
scripts (curl-pipe-bash), and GoReleaser-built releases.
Cross-platform: Windows, macOS, Linux.

This workflow replaces workflows/generic.md for Type 7 subjects. After
producing findings here, return to SKILL.md Step N for the shared verdict
tree and report shape. The Audit Coverage table and audit-confidence
assertion are owned by the dispatcher — do not duplicate them here.

Phase 4 / M4.2 — seventh subject-specific workflow (second Phase 4).
-->

# CLI Binary Workflow (Type 7)

This workflow handles **Type 7: cli-binary** subjects — standalone
executables installed onto `$PATH` (or equivalent), distributed outside
any registry that scores publisher trust. Covers GitHub Releases
binaries, vendor-hosted executables, Homebrew core formulae,
language-version managers, install scripts (curl-pipe-bash), and
GoReleaser-built releases.

After completing all sections below, return to `SKILL.md` Step N for the
shared verdict tree and audit-coverage report shape.

Sections follow the standard workflow template: **Identify / Evidence /
Subject Rubric / Subject Verdict Notes**.

Use `references/criteria/cli-binary.md` for cli-binary-specific
tiering and scoring. When it conflicts with the shared rubric, the more
specific cli-binary guidance wins.

## Identify

### 1. Determine the distribution channel and binary identity

| Channel | URL / command pattern | Adoption metric |
|---------|---------------------|-----------------|
| Homebrew core formula | `brew install <name>`, `formulae.brew.sh/formula/*` | Install count + formula stars |
| GitHub Releases (org) | `github.com/<org>/<repo>/releases`, download from Releases page | Download count per asset |
| GitHub Releases (personal) | `github.com/<user>/<repo>/releases` | Download count per asset |
| GoReleaser | Release assets with `checksums.txt`, multiple OS/arch binaries | Download count |
| Vendor-hosted binary | Vendor website download page, `get.<vendor>.com` | Website traffic / brand |
| Language-version manager | `curl … | sh` (rustup, nvm, volta), `pyenv install` | GitHub stars + community |
| Install script (curl-pipe-bash) | `curl -sSL <url> | sh`, `wget -qO- <url> | bash` | Script source reputation |
| Third-party mirror | Non-vendor download site, forum link, file host | None |

For each subject, record:
- **Binary name + version** (or "latest" if unversioned)
- **Distribution channel** (from table above)
- **Source URL** (GitHub repo, vendor site, or install script URL)
- **Target platform** (OS + architecture)
- **Install command** (exact command the user will run)

### 2. Extract available metadata

From the distribution channel, collect:
- **Author / organization** — GitHub org, vendor name, project maintainers
- **Repository** — source code location (if open-source)
- **Release date** — when this version was published
- **Release assets** — list of files (binaries, checksums, signatures)
- **License** — from repo or release notes
- **Checksum file** — presence of SHA-256/SHA-512 checksum file in release assets
- **Signature** — presence of GPG `.asc`/`.sig`, Sigstore cosign, Minisign `.minisig`
- **SLSA attestation** — presence of provenance attestation
- **Install script** — if distribution is via script, note the script URL

### 3. Required context (ask the user if not stated)

- What is the intended use? (development tool, system utility, one-shot task)
- Is this being installed system-wide or per-user?
- Will it run with elevated privileges (sudo/admin)?
- Who recommended it? (official docs, coworker, forum, search result)
- Is there a package-manager alternative? (`brew install`, `apt install`, etc.)

## Evidence — Part A: Tier Triage

Assign an audit tier using `references/criteria/cli-binary.md` Tier
Thresholds:

**Tier 1 — Quick Audit:** Well-known project, Homebrew formula or
established GitHub org, checksum + signature, >= 1yr old, no incidents,
no install-script-only distribution. Scope: §4.1 Provenance + §4.3
Security (checksum/signature verification only).

**Tier 2 — Standard Audit (default):** Recognizable channel, checksum
available, identifiable author, no incidents, > 30 days old. Scope: all
§4.x sections per shared rubric.

**Tier 3 — Deep Audit:** Any red-flag trigger (curl-pipe-sh, no
checksum/signature, unknown source, third-party mirror, chat-shared,
new project, prior incident, privilege request). Scope: all §4.x + full
install-script review + provenance deep-dive + alternatives assessment.

## Evidence — Part B: Research & Verification

### Core research questions

Answer these for every CLI binary audit (depth scales by tier):

1. **Who published this binary?** Identify the author/org. Verify GitHub
   org membership or vendor identity. Is the publisher the same as the
   upstream project author?
2. **Is the source code available?** Open-source repo? Does the release
   tag match the source? Can the binary be built from source?
3. **Is a checksum provided?** SHA-256/SHA-512 file in release assets?
   Is the checksum file served from the same origin as the binary, or
   from a separate trust channel?
4. **Is the binary signed?** GPG, Sigstore, Minisign? Is the public key
   available from a trusted source? Does verification pass?
5. **Is there SLSA provenance?** SLSA attestation in release assets?
   Can it be verified with `slsa-verifier`?
6. **Is the install method a pipe-to-shell script?** If yes: is the
   script auditable? Is it served over HTTPS? What does it actually do?
   Does it download a binary and verify its checksum, or does it execute
   arbitrary code without verification?
7. **What does the binary do at runtime?** Network access, file system
   writes, privilege escalation, persistent services? Does it phone home?
8. **Are there known CVEs or security incidents?** Search OSV, GHSA,
   vendor advisories, and web for the binary name + "vulnerability" or
   "compromise".
9. **Is it actively maintained?** Last release date, commit frequency,
   issue responsiveness.
10. **Are there alternatives?** Package-manager-distributed alternatives
    (brew, apt, cargo install) that provide stronger provenance?

### Distribution channel research

- **Homebrew formula:** Read the formula file on GitHub (`Homebrew/homebrew-core`). Check: source URL, checksum, build-from-source steps, dependencies, caveats. Verify the formula hasn't been recently modified in a suspicious way.
- **GitHub Releases:** Check release page: author, tag, CI artifacts, checksum file, signature file. Compare release author to repo owner. Check if release was created by GitHub Actions (CI-built) or manually uploaded.
- **Vendor-hosted:** Verify the download URL matches the vendor's known domain. Check for HTTPS. Look for a checksum/signature on the download page.
- **Install script:** Download the script (do NOT pipe to shell). Read it. Assess: what URLs does it fetch? Does it verify checksums? Does it require sudo? What does it install and where? Are there any obfuscated or encoded sections?

### Checksum & signature verification

For Tier 2+ audits, verify (or document inability to verify):

1. Download the checksum file (e.g., `checksums.txt`, `SHA256SUMS`)
2. Verify the binary's hash matches the checksum file entry
3. If signed: download the signature/public key, verify the signature
4. If Sigstore: verify via `cosign verify-blob` or transparency log
5. If SLSA: verify via `slsa-verifier verify-artifact`
6. Document verification result in findings

### Incident & reputation research

- Search: `"<binary-name>" vulnerability`, `"<binary-name>" compromise`, `"<binary-name>" malware`
- Check GitHub Security Advisories for the repo
- Check if the project has been transferred, archived, or changed ownership recently
- For language-version managers: check for known supply-chain incidents in their install pipeline

### Audit coverage tracking

Track which checks were performed per tier (guide, not output — the
Audit Coverage table itself is in `SKILL.md` Step N):

| Check | Tier 1 | Tier 2 | Tier 3 |
|-------|--------|--------|--------|
| Binary identity + channel | Yes | Yes | Yes |
| Author/org verification | Brief | Yes | Deep |
| Checksum verification | Yes | Yes | Yes |
| Signature verification | Note presence | Verify if available | Verify or flag absence |
| SLSA provenance | Note presence | Check | Verify |
| Install script review | N/A (no script) | If applicable | Full review |
| Source code availability | Note | Review repo | Deep review |
| CVE / incident search | Quick | Standard | Comprehensive |
| Runtime behavior | Skip | Brief | Deep |
| Alternatives assessment | Skip | Note | Full comparison |
| Maintenance status | Note | Check | Deep review |
| Build provenance | Note | Check CI | Verify pipeline |

## Subject Rubric

Apply `references/criteria.md` with these cli-binary-specific
overrides. Cite `references/criteria/cli-binary.md` for detailed
scoring.

### §4.1 Provenance — Binary Authenticity

- **Primary axis: checksum + signature verification.** A signed, checksummed
  binary from a known author/org is the strongest provenance signal. An
  unsigned binary with no checksum from an unknown source is the weakest.
- Assess the release pipeline: CI-built (strong) vs manual upload (weaker).
- GitHub: verify release author matches repo org/owner. Check for branch
  protection and required CI checks.
- Install scripts: assess the script's own provenance (HTTPS? known domain?
  auditable content?).
- Homebrew: formula review + build-from-source option = strong provenance.

### §4.2 Maintenance & Project Health

- Last release date, commit frequency, open issue responsiveness.
- Bus factor: single maintainer vs team/org.
- For language-version managers: assess the governing body (Rust Foundation
  for rustup, Node.js Foundation for nvm, etc.).
- Archived or transferred repos are strong negative signals.

### §4.3 Security — Vulnerabilities & Incidents

- Check OSV/GHSA for the binary name and its source repo.
- Search for prior supply-chain compromises (especially for install scripts
  and widely-used binaries).
- Assess dependency chain if the binary is a compiled artifact (Go, Rust
  binaries ship their deps statically).
- For install scripts: the script itself is the primary attack surface.

### §4.4 Permissions & Access

- What privileges does the binary require? User-level, root/admin, or mixed?
- Does the install script require `sudo`? Is the elevated access justified?
- Does the binary create persistent services (daemons, launch agents, systemd units)?
- Does the binary modify system paths, shell configs, or environment variables?
- Network access: does it phone home, check for updates, send telemetry?

### §4.5 Reliability & Stability

- Is the binary statically linked or does it pull runtime dependencies?
- Does it work across the target platform versions?
- Is there an uninstall/removal path?
- For install scripts: is there an uninstall script or documented removal steps?

### §4.6 Alternatives & Ecosystem Fit

- Is there a package-manager-distributed alternative (brew, apt, cargo install)?
- Is there a containerized alternative (docker run)?
- Does the project offer multiple install methods? (Binary download, package
  manager, build from source — breadth of options is a positive signal.)
- For language-version managers: are there alternatives with better provenance
  or security posture?

## Subject Verdict Notes

### Toward REJECTED

- Install script (`curl | sudo sh`) from unknown or unverifiable source
- No checksum AND no signature AND no package-manager alternative
- Binary from third-party mirror or repackager (not original author)
- Known prior supply-chain compromise with no remediation
- Binary requires root/admin with no clear justification
- Obfuscated or encoded sections in install script
- Project abandoned (no releases > 2 years, archived repo, unresponsive maintainer)

### Toward CONDITIONAL

- Install script from known vendor (note pipe-to-shell risk; recommend
  download-then-inspect)
- Checksum available but no signature (note: integrity without authenticity)
- Binary is legitimate but distributed via informal channel (Slack, forum)
  — recommend official source
- Single maintainer project with no CI (note bus factor + build provenance risk)
- Vendor-hosted binary unsigned but from known, reputable vendor
- Project recently changed ownership or was transferred

### Toward APPROVED

- Homebrew core formula with build-from-source option
- GitHub Releases from established org with CI-built artifacts + checksum + GPG/Sigstore
- Well-known language-version manager (rustup, volta) from established foundation
- Established project (>= 1yr, broad adoption, active maintenance)
- Multiple install methods available (binary, package manager, source)
- SLSA L2+ provenance attestation verified
```

**Rationale:** Follows the standard template (Identify / Evidence Part A / Evidence Part B / Subject Rubric / Subject Verdict Notes) used by all Phase 3–4 workflows. Key differentiators from desktop-app: checksum/signature verification replaces code signing as primary trust axis, install-script review is a first-class concern (desktop-app has no equivalent), provenance assessment is deeper (CI-built vs manual release), and Homebrew formula replaces Homebrew cask.

**Verification:** File exists. `grep "^## " workflows/cli-binary.md` confirms: Identify / Evidence — Part A / Evidence — Part B / Subject Rubric / Subject Verdict Notes.

**If this fails:** Delete `workflows/cli-binary.md`.

---

### Step 3: Update `SKILL.md`

**Objective:** Wire dispatch table row 7 and add reference file bullets.
**Confidence:** High
**Depends on:** Steps 1–2

**Files:**
- `SKILL.md`

**Changes:**

**3a. Dispatch table row 7:**

```markdown
// Before:
| 7 | cli-binary | `workflows/generic.md` | Fallback — specific workflow lands in Phase 4 (M4.2) |

// After:
| 7 | cli-binary | `workflows/cli-binary.md` | Live — Phase 4 (M4.2) |
```

**3b. Reference Files — workflow bullet (insert after `workflows/desktop-app.md` line):**

```markdown
// Before:
- `workflows/desktop-app.md` — Type 6 desktop-app workflow (Phase 4, M4.1)
- `references/criteria.md` — Shared tier-aware scoring rubric

// After:
- `workflows/desktop-app.md` — Type 6 desktop-app workflow (Phase 4, M4.1)
- `workflows/cli-binary.md` — Type 7 cli-binary workflow (Phase 4, M4.2)
- `references/criteria.md` — Shared tier-aware scoring rubric
```

**3c. Reference Files — addendum bullet (insert after `references/criteria/desktop-app.md` line):**

```markdown
// Before:
- `references/criteria/desktop-app.md` — Desktop-app criteria addendum (distribution channel trust, code signing, installer risk, sandboxing, tier thresholds)
- `references/licenses.md` — License compatibility matrix

// After:
- `references/criteria/desktop-app.md` — Desktop-app criteria addendum (distribution channel trust, code signing, installer risk, sandboxing, tier thresholds)
- `references/criteria/cli-binary.md` — CLI-binary criteria addendum (distribution channel trust, signature/checksum standards, install-script risk, provenance, tier thresholds)
- `references/licenses.md` — License compatibility matrix
```

**Rationale:** Follows the exact same pattern used in M4.1 (row update + 2 reference bullets inserted in type-number order).

**Verification:** `grep cli-binary SKILL.md` should show 4 hits: signal table row 7, dispatch table row 7, workflow reference bullet, addendum reference bullet.

**If this fails:** Revert the three edits to `SKILL.md`.

---

### Step 4: Update `evals/evals.json`

**Objective:** Add Type 7 eval coverage — one positive Tier 1, one negative Tier 3.
**Confidence:** High
**Depends on:** Steps 1–3

**Files:**
- `evals/evals.json`

**Changes:**

Append two entries to the `evals` array (after id 19):

```json
    {
      "id": 20,
      "prompt": "I want to install ripgrep. Is it safe? I'd run: brew install ripgrep",
      "expected_output": "Tier 1 quick audit. Routes to cli-binary workflow. Should recognize ripgrep (rg) as a well-known open-source search tool by BurntSushi (Andrew Gallant), distributed via Homebrew core formula with build-from-source option, also available on GitHub Releases with checksums. Rust-based, actively maintained, broad adoption. Verdict should be APPROVED.",
      "files": [],
      "assertions": [
        {"text": "Subject type is cli-binary", "type": "contains_concept"},
        {"text": "Report identifies ripgrep as a well-known or established project", "type": "contains_concept"},
        {"text": "Report notes Homebrew core formula as distribution channel", "type": "contains_concept"},
        {"text": "Report discusses checksum or signature availability", "type": "contains_concept"},
        {"text": "Verdict is APPROVED", "type": "exact_match"},
        {"text": "Audit confidence", "type": "contains_concept"}
      ]
    },
    {
      "id": 21,
      "prompt": "A blog post says to run this to install a cool productivity tool: curl -sSL https://totally-legit-tools.xyz/install.sh | sudo bash — should I?",
      "expected_output": "Tier 3 deep audit. Routes to cli-binary workflow. Should flag multiple critical risks: curl-pipe-sudo-bash is the most dangerous install pattern, unknown domain (totally-legit-tools.xyz), elevated privileges via sudo, no checksum or signature verification, blog-post distribution channel. Verdict must be REJECTED.",
      "files": [],
      "assertions": [
        {"text": "Subject type is cli-binary", "type": "contains_concept"},
        {"text": "Report flags curl-pipe-bash or pipe-to-shell as high risk", "type": "contains_concept"},
        {"text": "Report flags sudo or elevated privileges", "type": "contains_concept"},
        {"text": "Report flags unknown or unverifiable source", "type": "contains_concept"},
        {"text": "Verdict is REJECTED", "type": "exact_match"},
        {"text": "## Audit Coverage", "type": "contains_string"},
        {"text": "Audit confidence", "type": "contains_concept"}
      ]
    }
```

**Rationale:** Follows the Phase 4 eval pattern from M4.1 — one Tier 1 well-known positive case (ripgrep via Homebrew, analogous to Firefox via winget) and one Tier 3 red-flag negative case (curl-pipe-sudo-bash from unknown domain, analogous to fake VLC Pro). Eval id 20 tests the Homebrew formulae → cli-binary routing confirmed in M4.1. Eval id 21 tests the install-script risk assessment that is the signature concern for cli-binary.

**Verification:** JSON valid. 22 total evals (ids 0–21). ids 0–19 unchanged. ids 20 and 21 present with correct assertions.

**If this fails:** Remove the two appended entries from `evals/evals.json`.

---

## Verification Plan

### Automated Checks

- [ ] `workflows/cli-binary.md` exists and is non-empty
- [ ] `references/criteria/cli-binary.md` exists and is non-empty
- [ ] `evals/evals.json` is valid JSON with 22 entries
- [ ] `grep cli-binary SKILL.md` returns 4 hits (signal, dispatch, workflow ref, addendum ref)

### Manual Verification

- [ ] Workflow follows Identify / Evidence Part A / Evidence Part B / Subject Rubric / Subject Verdict Notes structure
- [ ] Criteria addendum covers all 5 sections (distribution channels, signature/checksum, install-script risk, provenance, tiers)
- [ ] Dispatch table row 7 routes to `workflows/cli-binary.md` with "Live — Phase 4 (M4.2)"
- [ ] Eval id 20 (ripgrep/Homebrew) tests the positive Tier 1 path
- [ ] Eval id 21 (curl-pipe-sudo-bash) tests the negative Tier 3 path
- [ ] ids 0–19 are unchanged in `evals/evals.json`

### Acceptance Criteria Validation

| Criterion | How to Verify | Expected Result |
|-----------|---------------|-----------------|
| Workflow exists with template | `grep "^## " workflows/cli-binary.md` | Identify, Evidence — Part A, Evidence — Part B, Subject Rubric, Subject Verdict Notes |
| Criteria addendum exists | File read; section scan | 5 sections present |
| Dispatch row 7 | `grep "cli-binary.*cli-binary.md" SKILL.md` | Row 7 routes to `workflows/cli-binary.md` |
| Reference Files bullets | `grep "cli-binary" SKILL.md` | 4 total hits |
| Eval coverage | JSON parse + id count | 22 total; ids 20, 21 present |
| No regressions | `diff` prior evals (ids 0–19) | Unchanged |
| Homebrew formula routing | Workflow Identify table | `brew install <name>` listed as cli-binary channel |

---

## Rollback Plan

Per-step rollback is noted in each step. If the overall implementation must be abandoned:

1. Delete `workflows/cli-binary.md`
2. Delete `references/criteria/cli-binary.md`
3. Revert `SKILL.md` edits (dispatch table row 7, reference file bullets)
4. Remove eval ids 20 and 21 from `evals/evals.json`
5. All changes are in 4 files; `git checkout -- <files>` restores clean state

---

## Notes

### Risks

- **Install-script content scope:** The workflow tells the agent to "read" install scripts, but scripts can be arbitrarily complex. The guidance should be sufficient for the agent to flag obvious red flags (sudo, obfuscation, unknown URLs) without requiring deep static analysis. Mitigated by the graduated tier system — only Tier 3 audits do full script review.
- **Homebrew formula trust:** The workflow treats Homebrew core formulae as strong positive trust, but Homebrew has had supply-chain incidents (e.g., audit-related PRs). Mitigated by the formula-inspection guidance in Evidence Part B.
- **Cross-platform binary format divergence:** Windows (.exe/.msi CLI tools), macOS (universal binaries), Linux (ELF, static/dynamic linking) have different audit surfaces. The workflow uses a distribution-channel-first approach that abstracts over binary formats, focusing on provenance rather than format-specific inspection.

### Open Questions

- *(none — all scope questions resolved by taxonomy def §7 and M4.1 Homebrew boundary)*
