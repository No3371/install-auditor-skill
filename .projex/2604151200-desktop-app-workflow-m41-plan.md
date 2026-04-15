# Desktop App Workflow — M4.1

> **Status:** Complete
> **Created:** 2026-04-15
> **Author:** Claude (Opus 4.6)
> **Source:** [2604070218-install-auditor-subject-typed-redesign-nav.md](2604070218-install-auditor-subject-typed-redesign-nav.md) Phase 4, M4.1
> **Related Projex:**
> - **Roadmap:** [2604070218-install-auditor-subject-typed-redesign-nav.md](2604070218-install-auditor-subject-typed-redesign-nav.md)
> - **Framing eval:** [2604070217-subject-typed-audit-dispatch-eval.md](2604070217-subject-typed-audit-dispatch-eval.md)
> - **Taxonomy spec:** [2604070300-install-auditor-subject-type-taxonomy-def.md](2604070300-install-auditor-subject-type-taxonomy-def.md)
> - **Pattern precedent (M3.4):** [closed/2604150312-ide-plugin-workflow-m34-plan.md](closed/2604150312-ide-plugin-workflow-m34-plan.md)
> **Worktree:** No

---

## Summary

Create the Type 6 subject-specific workflow at `workflows/desktop-app.md` and its criteria addendum at `references/criteria/desktop-app.md`, then wire Type 6 routing and eval coverage. M4.1 closes the first Phase 4 gap: desktop apps still fall through `workflows/generic.md`, which knows nothing about code signing (Authenticode, Apple codesign, GPG), installer types (MSI/EXE/DMG/pkg/AppImage/snap/flatpak/.deb/.rpm), distribution channel provenance (MS Store, Mac App Store, Homebrew cask, winget, Chocolatey, Snap Store, Flathub, direct download), sandboxing models, or auto-update mechanisms.

**Scope:** Type 6 desktop-app audits — workflow file, criteria addendum, dispatcher wiring, eval coverage.
**Estimated Changes:** 4 files (2 new, 2 modified), ~550-700 lines.

---

## Objective

### Problem / Gap / Need

Type 6 (`desktop-app`) routes to `workflows/generic.md`. Current guidance is inadequate:

1. `workflows/generic.md` has no desktop-app-specific checks. No code signing verification, no installer type risk assessment, no distribution channel provenance, no sandboxing evaluation.
2. Triage thresholds (`>100K weekly downloads`) are npm-specific. Desktop apps use distribution channel reputation, code signing status, and vendor identity — fundamentally different signals.
3. `references/registries.md` has no desktop-app distribution channel trust table. No coverage of MS Store, Mac App Store, Homebrew cask, winget, Chocolatey, Snap Store, Flathub, or direct download provenance.
4. No review path for code signing verification — Authenticode (standard vs EV), Apple Developer ID + notarization, GPG/Sigstore for Linux packages.
5. No treatment of installer type risk — MSI/MSIX (structured, auditable) vs bare EXE (opaque, arbitrary code) vs DMG/pkg vs AppImage/snap/flatpak vs .deb/.rpm.
6. No guidance on sandboxing assessment — App Sandbox (macOS), MSIX container (Windows), Flatpak/Snap sandboxing (Linux), or lack thereof.
7. No coverage of auto-update mechanisms — silent updates, update server provenance, update signing.
8. Taxonomy open question: "CLI vs desktop-app boundary at Homebrew" — confirm during this milestone that Homebrew cask routes to desktop-app and Homebrew core formulae route to cli-binary (Type 7).

The taxonomy spec (§6) defines: "A standalone application installed onto a user's OS, gaining process- or user-level privileges."

### Success Criteria

- [ ] `workflows/desktop-app.md` exists and follows Identify / Evidence / Subject Rubric / Subject Verdict Notes template
- [ ] `references/criteria/desktop-app.md` exists and defines desktop-app-specific scoring for distribution channel trust, code signing standards, installer type risk, sandboxing, auto-update risk, and tier thresholds
- [ ] `SKILL.md` dispatch table row 6 routes to `workflows/desktop-app.md`
- [ ] `SKILL.md` Reference Files includes `workflows/desktop-app.md` and `references/criteria/desktop-app.md`
- [ ] `evals/evals.json` gains at least 2 Type 6 cases: one well-known store/signed Tier 1 positive path, one unsigned/repackaged/unknown Tier 3 negative path
- [ ] No regressions in eval ids 0-17
- [ ] Homebrew boundary clarified: `brew install --cask` → desktop-app; `brew install` (formulae) → cli-binary

### Out of Scope

- New helper scripts for code signing verification or installer inspection
- Broad rewrites to `references/criteria.md` or `references/registries.md`
- Mobile app coverage (iOS/Android apps are a different trust boundary — not Type 6)
- Phase 4 M4.2-M4.4 workflows (cli-binary, agent-extension, remote-integration)

---

## Context

### Current State

`SKILL.md` classifies Type 6 correctly (`.msi/.dmg/.deb/.rpm/.pkg`, `brew install --cask`, `winget`, `choco`, MS/Mac App Store URLs) but dispatches to `workflows/generic.md`. The generic workflow has no desktop-app-specific fragments — zero code signing verification, zero installer type assessment, zero distribution channel provenance checks.

`references/registries.md` does not contain a desktop-app distribution channel trust baseline. The taxonomy definition provides the identity, examples, and routing rules, but no audit mechanics.

There is no existing Type 6 criteria addendum, no Type 6 workflow, and no Type 6 eval coverage.

### Key Files

| File | Role | Change Summary |
|------|------|----------------|
| `workflows/desktop-app.md` | **New.** Type 6 workflow | Create distribution-channel-aware workflow: app identity extraction, code signing verification, installer type risk, sandboxing assessment, auto-update review, verdict notes |
| `references/criteria/desktop-app.md` | **New.** Type 6 criteria addendum | Create desktop-app-specific scoring: distribution channel trust signals, code signing standards, installer type risk classification, sandboxing assessment, auto-update risk, tier thresholds |
| `SKILL.md` | Dispatcher + reference-file index | Row 6 -> `workflows/desktop-app.md`; add 2 Reference Files bullets |
| `evals/evals.json` | Regression + new Type 6 coverage | Add ids 18 and 19 for positive and negative Type 6 paths |

### Dependencies

- **Requires:** Phase 3 complete (M3.5 eval gate passed); dispatcher architecture stable; taxonomy Type 6 definition locked
- **Blocks:** Phase 4 M4.2 (cli-binary) — M4.2 needs the Homebrew boundary clarification from M4.1; Phase 4 completion gate

### Constraints

- Workflow must use the standard 4-section template (Identify / Evidence / Subject Rubric / Subject Verdict Notes)
- Audit Coverage table and audit-confidence statement owned by `SKILL.md` Step N
- No scripts in M4.1; evidence acquisition is doc/web/store inspection
- Cross-platform coverage: Windows, macOS, Linux installer types and distribution channels all in scope
- Repo is clean; worktree not needed

### Assumptions

- Desktop apps are diverse: Windows-dominant (MSI/EXE via winget/choco/direct), macOS (DMG/pkg via App Store/Homebrew cask/direct), Linux (.deb/.rpm/snap/flatpak/AppImage via repos/stores/direct). The workflow must cover all three OS families without becoming unwieldy.
- Code signing is the primary trust signal for desktop apps (replaces manifest permissions for browser extensions and capability declarations for IDE plugins). Unsigned apps are the single strongest negative signal.
- Distribution channel provenance is the secondary trust signal. Official stores (MS Store, Mac App Store) apply review + signing gates. Package managers (Homebrew cask, winget, Chocolatey) apply community review + manifest verification. Direct download relies entirely on vendor identity + code signing.
- `brew install --cask` → Type 6 (desktop-app) because casks install full macOS applications. `brew install` (core formulae) → Type 7 (cli-binary) per the taxonomy open question. This boundary is confirmed by this milestone.
- Sandboxing varies dramatically: macOS App Sandbox (App Store apps), MSIX container (MS Store), Flatpak (by design), Snap (strict vs classic confinement), traditional installers (no sandboxing). The workflow must assess but not require sandboxing.
- Auto-update mechanisms are common and represent an ongoing trust surface. Unlike browser extensions (store-mediated updates), desktop apps often self-update from vendor-controlled servers with varying levels of signature verification.

### Impact Analysis

- **Direct:** New workflow, new criteria addendum, dispatcher wiring, eval additions
- **Adjacent:** `workflows/generic.md` no longer handles Type 6 once M4.1 lands, but needs no edits. Homebrew boundary confirmed for M4.2.
- **Downstream:** Phase 4 M4.2 (cli-binary) benefits from the Homebrew boundary clarification. Phase 4 completion gate moves one step closer.

---

## Implementation

### Overview

4 steps: addendum first, workflow second, dispatcher wiring third, evals fourth. Same sequence as M3.1-M3.4.

### Step 1: Create `references/criteria/desktop-app.md`

**Objective:** Define desktop-app-specific scoring extensions the workflow can cite.
**Confidence:** High
**Depends on:** None

**Files:**
- `references/criteria/desktop-app.md` (new)

**Changes:**

Create a new addendum with this structure:

```markdown
# Desktop App — Criteria Addendum

Per-subject scoring extensions for **Type 6: desktop-app** audits.
Layers on top of `references/criteria.md`. More-specific guidance wins.

Covers: Microsoft Store, Mac App Store, Homebrew cask, winget,
Chocolatey, Snap Store, Flathub, direct vendor download, third-party
mirrors. Cross-platform: Windows, macOS, Linux.

## Distribution Channel Trust Signals

| Channel | Verification Gate | Adoption Metric | Trust Notes |
|---------|-------------------|-----------------|-------------|
| Microsoft Store (MSIX) | Microsoft review + signing | Ratings + install count | Strongest Windows signal; MSIX apps run in container; review process exists |
| Mac App Store | Apple review + notarization + App Sandbox | Ratings + install count | Strongest macOS signal; mandatory sandboxing; human review |
| Homebrew Cask | Community-reviewed cask formula; SHA-256 checksum | GitHub stars on formula repo | Community trust; formula points to vendor-hosted binary; no signing gate |
| winget | Community-reviewed manifest; SHA-256 checksum | Package manifest presence | Microsoft-operated repo; manifest review exists; binary from vendor URL |
| Chocolatey | Community moderation; automated virus scan | Download count | Package scripts reviewed for public packages; checksum verification |
| Snap Store (strict) | Canonical-operated; auto-review + confinement | Install count | Strict confinement = sandboxed; auto-update via Canonical |
| Snap Store (classic) | Canonical-operated; manual review for classic | Install count | Classic confinement = no sandbox; manual review gate |
| Flathub | Community-reviewed; Flatpak sandbox by design | Install count | Sandboxed by default; permissions declared in manifest |
| APT/YUM official repos | Distro maintainer-reviewed; GPG-signed repo | Part of OS package set | Strongest Linux traditional signal; distro stands behind the package |
| Direct vendor download | Vendor website only; no third-party review | Website traffic / brand recognition | Trust depends entirely on vendor identity + code signing |
| Third-party mirror / repackager | None | None | Highest risk; binary provenance unverifiable; repackaging may inject payloads |

### Scoring impact

- Mac App Store or Microsoft Store = strong positive (store review + sandboxing)
- APT/YUM official distro repo = strong positive (distro-maintained, GPG-signed)
- Homebrew cask / winget / Chocolatey = moderate positive (community review + checksum)
- Snap strict / Flathub = moderate positive (sandboxed + community review)
- Snap classic = weak positive (no sandbox; manual review exists)
- Direct vendor download with valid code signing = neutral (trust = vendor identity)
- Direct vendor download unsigned = strong negative
- Third-party mirror or repackager = strong negative (equivalent to sideloaded VSIX)

## Code Signing Standards

| Platform | Signing Method | Strength | Verification |
|----------|---------------|----------|--------------|
| Windows — Authenticode EV | EV code signing certificate | Strong | Hardware token required; publisher identity verified by CA; SmartScreen reputation immediate |
| Windows — Authenticode standard | Standard code signing certificate | Moderate | Publisher identity verified by CA; SmartScreen may warn on low reputation |
| Windows — unsigned | None | Absent | SmartScreen blocks or warns; no publisher identity |
| macOS — Developer ID + notarization | Apple Developer ID + Apple notarization service | Strong | Apple checks for malware; notarized apps pass Gatekeeper without warning |
| macOS — Developer ID only | Apple Developer ID without notarization | Moderate | Gatekeeper allows with warning on first run; no Apple malware scan |
| macOS — unsigned / ad-hoc | None or self-signed | Absent | Gatekeeper blocks by default; user must override system security |
| Linux — GPG (distro key) | Distribution maintainer GPG key | Strong | Part of distro trust chain; `apt`/`yum` verify automatically |
| Linux — GPG (vendor key) | Vendor-provided GPG key for third-party repo | Moderate | User must import and trust vendor key; key provenance matters |
| Linux — Sigstore / cosign | Sigstore keyless signing | Moderate-Strong | Emerging standard; transparency log provides audit trail |
| Linux — unsigned | None | Absent | No verification; binary provenance unknowable |

### Scoring impact

- EV Authenticode or Apple Developer ID + notarization or distro GPG = strong positive
- Standard Authenticode or Apple Developer ID-only or vendor GPG = moderate positive
- Sigstore = moderate positive (emerging; log provides auditability)
- Unsigned on any platform = HIGH flag (single strongest negative signal for desktop apps)

## Installer Type Risk Classification

| Installer Type | Platform | Risk | Why |
|----------------|----------|------|-----|
| MSIX / APPX | Windows | Low | Container-isolated; declared capabilities; clean uninstall |
| MSI | Windows | Low-Medium | Structured installer format; auditable via `msiexec` logs; custom actions can run arbitrary code |
| EXE (NSIS, Inno, etc.) | Windows | Medium-High | Opaque; can execute arbitrary code during install; bundleware/adware vector |
| DMG (drag-to-Applications) | macOS | Low-Medium | Simple copy; no installer scripts; app bundle structure is inspectable |
| PKG (macOS) | macOS | Medium | Can run pre/post-install scripts with elevated privileges |
| AppImage | Linux | Low-Medium | Self-contained; no system integration; runs in user space; not sandboxed by default |
| Snap (strict) | Linux | Low | Sandboxed; declared interfaces; auto-update |
| Snap (classic) | Linux | Medium | No sandbox; full system access; manual review gate |
| Flatpak | Linux | Low | Sandboxed by default; declared permissions; portal-mediated access |
| .deb / .rpm | Linux | Medium | Can run pre/post-install scripts as root; risk depends on source repo trust |

### Scoring impact

- MSIX/Snap-strict/Flatpak = positive (sandboxed, declared capabilities)
- MSI/DMG/AppImage = neutral-to-low-risk (structured or simple; inspectable)
- PKG/.deb/.rpm = note install scripts; risk depends on source trust
- EXE installer = elevated scrutiny (opaque, arbitrary code execution)
- Snap classic = note lack of sandbox

## Sandboxing Assessment

| Sandbox Model | Platform | Strength | Notes |
|---------------|----------|----------|-------|
| App Sandbox | macOS (App Store) | Strong | Mandatory for Mac App Store; declared entitlements; limited file/network/hardware access |
| MSIX container | Windows (MS Store) | Moderate-Strong | Virtual filesystem/registry; declared capabilities; clean uninstall |
| Flatpak sandbox | Linux | Moderate-Strong | Bubblewrap-based; XDG portals for controlled access; permissions in manifest |
| Snap strict confinement | Linux | Moderate-Strong | AppArmor-based; declared interfaces; auto-connecting interfaces reduce isolation |
| Snap classic confinement | Linux | Absent | No meaningful sandbox; equivalent to traditional install |
| None (traditional install) | All | Absent | Full user-level (or root) access; no confinement |

### Scoring impact

- App Sandbox / MSIX container / Flatpak / Snap strict = positive signal
- No sandboxing (traditional install, Snap classic) = neutral for well-known vendors, negative for unknown vendors
- Sandboxing is a bonus, not a requirement — many legitimate desktop apps run unsandboxed

## Auto-Update Mechanism Risk

| Pattern | Risk | Guidance |
|---------|------|----------|
| Store-managed updates (MS Store, Mac App Store, Snap, Flatpak) | Low | Updates go through store review pipeline |
| Signed auto-updater (Sparkle on macOS, Squirrel on Windows/Electron) | Low-Medium | Verify update server uses HTTPS + signature verification |
| Vendor-hosted updater with no signature verification | Medium-High | Update channel is a persistent attack surface; MITM possible |
| No auto-update (manual download of new version) | Low (update) / Medium (staleness) | No update-channel risk, but user may run stale versions with known CVEs |
| Disabled or opt-out auto-update | Low-Medium | User controls update timing; staleness risk if updates are never applied |

### Scoring impact

- Store-managed or signed auto-updater = neutral (expected pattern)
- Unsigned update channel = MEDIUM flag (persistent attack surface)
- No auto-update on security-sensitive software = note staleness risk

## Telemetry & Data Collection

Desktop apps often collect telemetry. Assess:
- Is telemetry disclosed in privacy policy?
- Is telemetry opt-in or opt-out?
- What data is collected (crash reports, usage analytics, personal data)?
- Does the app phone home on first launch?

### Scoring impact

- Transparent opt-in telemetry = neutral
- Opt-out telemetry with clear disclosure = LOW note
- Undisclosed or opaque data collection = MEDIUM flag
- Known data exfiltration or privacy violation = HIGH flag

## Tier Thresholds (Desktop Apps)

### Tier 1 — Quick Audit

ALL of these must hold:
- Distributed via official store (MS Store, Mac App Store) OR well-known package manager (Homebrew cask, winget, Chocolatey with high download count)
- Code signed (Authenticode, Apple Developer ID + notarization, or distro GPG)
- Publisher is a known company or well-known open-source project
- App has been available >= 1 year
- No known incidents, removals, or security controversies
- Installer type is low-risk (MSIX, MSI, DMG, snap-strict, flatpak)

### Tier 2 — Standard Audit (default)

Default when not all Tier 1 criteria are met:
- Distributed via a recognized channel (including direct vendor download)
- Code signed (any level)
- Identifiable publisher
- No known security incidents
- Available > 30 days

### Tier 3 — Deep Audit

ANY of these triggers:
- Unsigned binary
- Direct download from unknown or unverifiable source
- Third-party mirror or repackager (not original vendor)
- EXE installer from non-store source with no code signing
- Shared via chat/email/forum link (not discovered via official channel)
- Recent acquisition or publisher change
- Known prior removal from store or security incident
- App requests admin/root privileges with unclear justification
- Bundleware or adware reports in web search results
```

**Rationale:** Shared rubric has no desktop-app coverage. This addendum becomes the single reference for distribution channel trust, code signing standards, installer type risk, sandboxing assessment, auto-update risk, and tier thresholds calibrated to desktop app distribution patterns.

**Verification:** File exists. Sections present: distribution channel trust signals, code signing standards, installer type risk classification, sandboxing assessment, auto-update mechanism risk, telemetry/data collection, tier thresholds.

**If this fails:** Delete `references/criteria/desktop-app.md`.

---

### Step 2: Create `workflows/desktop-app.md`

**Objective:** Author the Type 6 workflow with cross-platform desktop app evidence and verdict guidance.
**Confidence:** High
**Depends on:** Step 1

**Files:**
- `workflows/desktop-app.md` (new)

**Changes:**

Create the workflow with this structure:

```markdown
<!--
workflows/desktop-app.md - Type 6 subject-specific workflow.
Handles desktop applications from Microsoft Store, Mac App Store,
Homebrew cask, winget, Chocolatey, Snap Store, Flathub, APT/YUM
repos, and direct vendor downloads. Cross-platform: Windows, macOS,
Linux.

This workflow replaces workflows/generic.md for Type 6 subjects. After
producing findings here, return to SKILL.md Step N for the shared verdict
tree and report shape. The Audit Coverage table and audit-confidence
assertion are owned by the dispatcher — do not duplicate them here.

Phase 4 / M4.1 — sixth subject-specific workflow (first Phase 4).
-->

# Desktop App Workflow (Type 6)

This workflow handles **Type 6: desktop-app** subjects — standalone
applications installed onto a user's OS, gaining process- or user-level
privileges. Covers Microsoft Store, Mac App Store, Homebrew cask,
winget, Chocolatey, Snap Store, Flathub, APT/YUM official repos,
direct vendor downloads, and third-party mirrors.

After completing all sections below, return to `SKILL.md` Step N for the
shared verdict tree and audit-coverage report shape.

Sections follow the standard workflow template: **Identify / Evidence /
Subject Rubric / Subject Verdict Notes**.

Use `references/criteria/desktop-app.md` for desktop-app-specific
tiering and scoring. When it conflicts with the shared rubric, the more
specific desktop-app guidance wins.

## Identify

### 1. Determine the distribution channel and app identity

| Channel | URL / command pattern | Adoption metric |
|---------|---------------------|-----------------|
| Microsoft Store | `apps.microsoft.com/detail/*`, `ms-windows-store://pdp/*` | Ratings + install count |
| Mac App Store | `apps.apple.com/*/app/*` | Ratings + install count |
| Homebrew Cask | `brew install --cask <name>`, `formulae.brew.sh/cask/*` | GitHub stars on cask formula |
| winget | `winget install <id>`, `winget.run/pkg/*` | Manifest presence + community activity |
| Chocolatey | `choco install <name>`, `community.chocolatey.org/packages/*` | Download count |
| Snap Store | `snap install <name>`, `snapcraft.io/<name>` | Install count |
| Flathub | `flatpak install flathub <id>`, `flathub.org/apps/*` | Install count |
| APT/YUM official repo | `apt install <name>`, `dnf install <name>` | Part of distro package set |
| APT/YUM third-party repo | PPA, COPR, vendor repo added via `add-apt-repository` or `.repo` file | Download count (if available) |
| Direct vendor download | Vendor website download page | Website traffic / brand recognition |
| Third-party mirror | Non-vendor download site, file-sharing, forum link | None |

If the user provides a store/package-manager command, extract the app
name and channel. If they provide a URL, identify whether it is an
official store, vendor site, or third-party mirror. If they provide
an app name only, determine the intended distribution channel.

### 2. Extract app name and metadata

- **App name**: Exact name as listed in store/package manager/vendor site
- **Publisher/vendor**: Company or individual behind the app
- **Version**: Current version (if determinable)
- **Distribution channel**: From the table above
- **Code signing status**: Signed (by whom), notarized (macOS), or unsigned
- **Installer type**: MSI, MSIX, EXE, DMG, PKG, AppImage, snap, flatpak,
  .deb, .rpm, or other

### 3. Gather required context

Collect before proceeding:

1. **App name and version** — exact name + version if known
2. **Distribution channel** — which channel (from table above)
3. **Installation method** — store install, package manager command, direct
   download + manual install, script-based install
4. **Stated purpose** — what the user needs this app for
5. **Target OS** — Windows, macOS, Linux (which distro if relevant)
6. **Installer type** — obtained during research if not immediately available

If any of 1–5 are missing, ask before proceeding.

## Evidence — Part A: Tier Triage

Gather distribution channel and vendor data via web search:
- App presence on official stores or package managers
- Publisher/vendor identity and reputation
- Code signing status (if determinable from store listing or web search)
- Brief search for "[app name] malware OR security OR bundleware OR
  adware" for prior incidents

Apply the desktop-app-specific tier thresholds from
`references/criteria/desktop-app.md`:

### Tier 1 — Quick Audit (well-known, high-trust)

Use when ALL Tier 1 criteria from the addendum are met: official store or
well-known package manager, code signed, known publisher, available >= 1
year, no incidents, low-risk installer type.

Quick audit scope: confirm distribution channel + code signing status,
verify publisher identity, check for incidents. Proceed to Subject Verdict
Notes with minimal ceremony.

### Tier 2 — Standard Audit (default)

Default depth. Full code signing review, installer type assessment,
distribution channel verification, incident search, sandboxing assessment,
auto-update review.

### Tier 3 — Deep Audit (any red flag)

Any Tier 3 trigger from the addendum: unsigned, unknown source, third-party
mirror, EXE installer without signing, shared via chat, recent acquisition,
prior removal, admin privilege request, bundleware reports.

Deep audit scope: full signing verification + installer behavior analysis +
source code review (if open source) + network behavior assessment +
sandboxing evaluation + update mechanism inspection.

## Evidence — Part B: Research

### Core research questions (all tiers)

Answer every question that applies to the assigned tier:

1. **Who publishes this app?** Known company, individual, or open-source
   project? Can the publisher be verified through the distribution channel,
   code signing certificate, or website?
2. **Is the app code-signed?** What type of signing (Authenticode EV/
   standard, Apple Developer ID + notarization, distro GPG, vendor GPG)?
   Cross-reference against the code signing standards in
   `references/criteria/desktop-app.md`.
3. **What is the installer type?** MSI/MSIX/EXE/DMG/PKG/AppImage/snap/
   flatpak/.deb/.rpm? Cross-reference against the installer type risk
   classification in the addendum.
4. **What distribution channel delivers the app?** Official store, package
   manager, vendor download, or third-party mirror? Is the download URL
   the vendor's official domain?
5. **Does the app run sandboxed?** App Sandbox (macOS App Store), MSIX
   container, Flatpak sandbox, Snap strict confinement, or unsandboxed?
6. **What privileges does the app request?** Does it need admin/root for
   install or runtime? Does it install system services, kernel extensions,
   or drivers?
7. **How does the app update?** Store-managed, signed auto-updater, vendor-
   hosted updater, manual download, or no updates?
8. **Are there known security incidents?** Search for store removals,
   malware reports, bundleware/adware reports, data breaches, privacy
   violations.
9. **Does the app collect telemetry?** Is collection disclosed, opt-in or
   opt-out, and what data is collected?
10. **Is the source code available?** Open-source apps can be audited.
    Note the repo URL. Closed-source = note as a data point.

### How to research

**Distribution channel verification** (all tiers):

Web search for the app on official stores and package managers. Extract:
- Store listing presence and metadata (ratings, reviews, install count)
- Publisher name and any verification badge
- Code signing status (visible on macOS Gatekeeper prompts, Windows
  SmartScreen, store listings)
- Download URL domain matches vendor's official domain

**Code signing inspection** (Tier 2 and Tier 3):

Determine signing status via:
- Store listing (MS Store / Mac App Store apps are signed by definition)
- Package manager metadata (Homebrew cask checksums, winget manifests,
  Chocolatey verification)
- Web search for "[app name] code signing" or "authenticode" or
  "notarized"
- Vendor documentation or security page

**Installer behavior assessment** (Tier 2 and Tier 3):

- Identify installer type from file extension and distribution channel
- For EXE installers: is the installer framework known (NSIS, Inno Setup,
  WiX)? Does it bundle third-party software (toolbars, adware)?
- For PKG/.deb/.rpm: does it run pre/post-install scripts? What do they do?
- For snap/flatpak: what interfaces/permissions are declared?

**Incident and reputation search** (all tiers, depth varies):

Web search queries:
- `"<app name>" malware OR security OR vulnerability OR breach`
- `"<app name>" bundleware OR adware OR PUP`
- `"<publisher name>" security OR malware OR breach`
- For Tier 3: `"<app name>" site:reddit.com` and
  `"<app name>" site:virustotal.com`

### Audit coverage tracking

Map evidence to the Audit Coverage rows expected by `SKILL.md` Step N:

| Check | Tier 1 | Tier 2 | Tier 3 |
|-------|--------|--------|--------|
| Distribution channel verification | Required | Required | Required |
| Publisher / vendor identity | Required | Required | Required |
| Code signing status | Required | Required | Required |
| Installer type assessment | Brief | Required | Required |
| Sandboxing evaluation | Brief | Required | Required |
| CVE / advisories | Required | Required | Required |
| Web search — incidents & bundleware | Brief | Required | Required |
| Auto-update mechanism review | Tier-skip | Required | Required |
| Telemetry / data collection | Tier-skip | Note | Required |
| Source code review | Tier-skip | If open source | Required |
| Privilege escalation assessment | Tier-skip | If elevated | Required |
| OpenSSF Scorecard | Optional | If repo known | Required |

## Subject Rubric — Evaluate

Score against the shared rubric in `references/criteria.md` AND the
desktop-app addendum in `references/criteria/desktop-app.md`. Sections
below specialize the shared criteria for desktop app context.

### 4.1 Provenance & Identity (desktop-app-specialized)

- **Distribution channel verification**: Is the app distributed via an
  official store or well-known package manager? Is it the vendor's
  official listing (not a third-party repackaging)?
- **Publisher identity**: Can the publisher be linked to a real company
  or known open-source project? Check the store listing, code signing
  certificate subject, and vendor website.
- **Code signing certificate chain**: Who issued the certificate? Is it
  EV or standard (Windows)? Is it notarized (macOS)? Is it a distro
  maintainer key (Linux)?
- **Impersonation check**: Are there similarly-named apps from different
  publishers? Repackaged versions on third-party download sites?
- **Cross-channel consistency**: If available on multiple channels (e.g.,
  MS Store + winget + direct download), is the publisher the same entity?

### 4.2 Maintenance & Longevity (desktop-app-specialized)

- **Last update date**: When was the last version released? Desktop apps
  with network-facing components stale faster than offline tools.
- **Update mechanism**: Does the app auto-update? Is the update channel
  signed? Store-managed updates are safest.
- **Vendor viability**: Is the company/project active? Abandoned desktop
  apps accumulate unpatched CVEs faster than simpler tools.
- **Review sentiment**: Recent reviews on stores or forums reporting
  suspicious behavior, bundleware, crashes, or privacy concerns.
- **OS version compatibility**: Does the app support the user's current
  OS version?

### 4.3 Security Track Record (desktop-app-specialized)

- **Store removal history**: Has this app been removed from any store for
  policy violations, malware, or bundleware?
- **CVEs**: Check NVD, GHSA, and vendor security advisories for the app
  name and version.
- **Bundleware / adware history**: Has the installer been reported to
  bundle unwanted software? Check web search + VirusTotal community
  reports.
- **Data breach history**: Has the vendor suffered data breaches affecting
  user data collected by the app?
- **Supply-chain incidents**: Has the vendor's signing key been
  compromised? Has the update mechanism been hijacked?

### 4.4 Permissions & Access (desktop-app-specialized)

**Desktop apps run with process- or user-level OS privileges.** The risk
axes differ from browser extensions (manifest permissions) and IDE plugins
(capability declarations):

- **Install-time privilege**: Does the installer require admin/root? Is
  this justified (system service, driver) or unnecessary?
- **Runtime privilege**: Does the app run elevated? Does it install a
  system service that runs as SYSTEM/root?
- **File system access**: Does the app access files outside its own
  directory and user documents? Configuration files, credentials, SSH
  keys?
- **Network access**: Does the app make network calls? To what endpoints?
  Telemetry? License verification? Data sync?
- **Kernel extensions / drivers**: Does the app install kernel-level
  components (Windows filter drivers, macOS kexts/system extensions)?
  This is the highest-privilege surface.
- **Sandboxing**: Is the app sandboxed (App Sandbox, MSIX, Flatpak, Snap
  strict)? If not, note as an unrestricted-privilege data point.

### 4.5 Reliability & Compatibility (desktop-app-specialized)

- **OS compatibility**: Minimum supported OS version. Apps requiring very
  old OS versions may lack modern security features (ASLR, sandboxing).
- **Architecture**: Does the app support the user's CPU architecture
  (x64, ARM64, universal binary)?
- **Dependency chain**: Does the app require runtimes (.NET, Java,
  Electron) or system libraries? Are those dependencies current?
- **Uninstall cleanliness**: Does the app uninstall cleanly (MSIX/Flatpak/
  Snap = yes by design; EXE installers vary)?
- **Auto-update reliability**: Does the auto-updater work without admin
  privileges? Does it verify update signatures?

### 4.6 Alternatives (desktop-app-specialized)

- Is there a store-distributed version of the same app (if the user is
  installing via direct download)?
- Is there a sandboxed version (Flatpak, Snap strict, MSIX) if the user
  is installing a traditional unsandboxed package?
- Is there an open-source alternative if the app is closed-source?
- Is there a web-based alternative that eliminates the need for a local
  install?

## Subject Verdict Notes

Desktop-app-specific guidance for how findings map to verdicts. These
notes supplement the shared verdict tree in `SKILL.md` Step N.

### Toward REJECTED

Any one of these pushes strongly toward REJECTED:

- **Known malware / store removal for malicious behavior**: app removed
  from store for data exfiltration, cryptomining, credential theft,
  or bundleware
- **Unsigned binary from unknown source**: no code signing, no store
  listing, no verifiable publisher identity
- **Third-party repackaged installer**: app downloaded from a mirror or
  file-sharing site rather than the vendor's official channel, with no
  way to verify binary integrity
- **Known bundleware / adware**: installer reported to bundle unwanted
  software (toolbars, browser hijackers, PUPs)
- **Kernel-level component from unverified vendor**: app installs drivers
  or kernel extensions without established vendor trust
- **Recent acquisition + privilege escalation**: app acquired by new
  entity and simultaneously added elevated-privilege requirements

### Toward CONDITIONAL

- **Unsigned but from known vendor via official channel**: Condition:
  verify download URL is vendor's official domain; monitor for signing
  adoption
- **EXE installer from known vendor**: Condition: verify installer is
  signed; check for bundleware; prefer MSI/MSIX if available
- **Broad system access with justification**: antivirus, backup, VPN
  apps legitimately need deep system access — Condition: understand
  scope; verify vendor trust
- **Closed-source with network access**: Condition: review privacy policy;
  monitor for incidents; note telemetry behavior
- **Direct download when store version exists**: Condition: prefer the
  store version for sandboxing and update guarantees
- **Snap classic confinement**: Condition: understand why strict was not
  used; evaluate if alternatives with sandboxing exist
- **3+ MEDIUM flags accumulated**: cumulative risk per shared verdict tree

### Toward APPROVED

All of the following support APPROVED:

- All tier-appropriate checks completed with no flags
- Distributed via official store or well-known package manager
- Code signed (Authenticode, Apple Developer ID + notarization, distro GPG)
- Publisher is identified (known company or project)
- No known incidents, store removals, or bundleware reports
- Installer type is low-risk or justified
- Sandboxed if distributed via store (bonus for non-store)
- Healthy maintenance signals (recent updates, active development)

After completing the Subject Rubric and noting verdict-relevant findings,
**return to `SKILL.md` Step N** for the shared verdict tree, report
skeleton, and escalation guidance.
```

**Rationale:** Mirrors the established Phase 3 workflow shape. The critical distinction from browser extensions (permissions) and IDE plugins (capabilities) is that desktop apps' primary risk axes are **code signing**, **distribution channel provenance**, **installer type**, and **sandboxing** — reflecting the diverse install surfaces across Windows, macOS, and Linux. Code signing is elevated to the single most important trust signal because desktop apps run with full OS-level privileges and have no browser/editor mediated permission gate.

**Verification:** File exists. Contains the 4 required sections (Identify / Evidence / Subject Rubric / Subject Verdict Notes). References `references/criteria/desktop-app.md`. Does not duplicate dispatcher-owned final report text.

**If this fails:** Delete `workflows/desktop-app.md`.

---

### Step 3: Update `SKILL.md`

**Objective:** Route Type 6 to the new workflow and index new reference files.
**Confidence:** High
**Depends on:** Step 2

**Files:**
- `SKILL.md`

**Changes:**

Dispatch table row:

```markdown
// Before:
| 6 | desktop-app | `workflows/generic.md` | Fallback — specific workflow lands in Phase 4 (M4.1) |

// After:
| 6 | desktop-app | `workflows/desktop-app.md` | Live — Phase 4 (M4.1) |
```

Reference Files list — two insertions to maintain the existing grouping:

```markdown
// Insert workflow bullet after ide-plugin workflow bullet (after the line
// `- `workflows/ide-plugin.md` — Type 3 ide-plugin workflow (Phase 3, M3.4)`):
- `workflows/desktop-app.md` — Type 6 desktop-app workflow (Phase 4, M4.1)

// Insert addendum bullet after ide-plugin addendum bullet (after the line
// `- `references/criteria/ide-plugin.md` — IDE-plugin criteria addendum ...`):
- `references/criteria/desktop-app.md` — Desktop-app criteria addendum (distribution channel trust, code signing, installer risk, sandboxing, tier thresholds)
```

**Rationale:** Dispatcher routing and reference-file index are the only `SKILL.md` edits needed. All subject logic lives in the new workflow and addendum.

**Verification:** `rg -n "desktop-app|workflows/desktop-app.md|references/criteria/desktop-app.md" SKILL.md` shows row 6 -> live route plus two reference-file bullets.

**If this fails:** Revert row and remove bullets; Type 6 continues routing through `workflows/generic.md`.

---

### Step 4: Update `evals/evals.json`

**Objective:** Add positive and negative Type 6 regression coverage.
**Confidence:** High
**Depends on:** Steps 2-3

**Files:**
- `evals/evals.json`

**Changes:**

Add id 18 — clean positive path (well-known desktop app via package manager):

```json
{
  "id": 18,
  "prompt": "Is it safe to install Firefox via winget? I want to run: winget install Mozilla.Firefox",
  "expected_output": "Tier 1 quick audit. Routes to desktop-app workflow. Should recognize Firefox as a well-known open-source browser from Mozilla (established vendor), note winget as a recognized distribution channel with community-reviewed manifest, confirm the app is code-signed (Authenticode), and return APPROVED.",
  "files": [],
  "assertions": [
    {"text": "Subject type is desktop-app", "type": "contains_concept"},
    {"text": "Report identifies Mozilla/Firefox as a known vendor or project", "type": "contains_concept"},
    {"text": "Report notes winget as a recognized distribution channel", "type": "contains_concept"},
    {"text": "Report discusses code signing status", "type": "contains_concept"},
    {"text": "Verdict is APPROVED", "type": "exact_match"},
    {"text": "Audit confidence", "type": "contains_concept"}
  ]
}
```

Add id 19 — negative repackaged/unknown path:

```json
{
  "id": 19,
  "prompt": "A forum post linked to a site called free-software-downloads.xyz where I can get a 'Pro' version of VLC media player as a .exe file. Should I install it?",
  "expected_output": "Tier 3 deep audit. Routes to desktop-app workflow. Should flag the third-party mirror (not VideoLAN's official site), the repackaged 'Pro' branding (VLC is free/open-source — there is no Pro version), the .exe installer from an unknown source, and the forum-link distribution. Verdict must be REJECTED.",
  "files": [],
  "assertions": [
    {"text": "Subject type is desktop-app", "type": "contains_concept"},
    {"text": "Report flags the third-party or unofficial download source", "type": "contains_concept"},
    {"text": "Report flags the repackaged or fake 'Pro' version as suspicious", "type": "contains_concept"},
    {"text": "Report flags the .exe installer from unknown source", "type": "contains_concept"},
    {"text": "Verdict is REJECTED", "type": "exact_match"},
    {"text": "## Audit Coverage", "type": "contains_string"},
    {"text": "Audit confidence", "type": "contains_concept"}
  ]
}
```

Do not rewrite existing ids 0-17.

**Rationale:** These two evals force the workflow to prove the two core M4.1 promises: it can approve a well-known code-signed app from a recognized channel and reject a repackaged installer from an unknown third-party mirror.

**Verification:** `python -c "import json; json.load(open('evals/evals.json', encoding='utf-8'))"` succeeds. IDs 18 and 19 exist. Total eval count becomes 20.

**If this fails:** Revert `evals/evals.json`.

---

## Verification Plan

### Automated Checks

- [ ] `python -c "import json; json.load(open('evals/evals.json', encoding='utf-8'))"`
- [ ] `rg -n "desktop-app|workflows/desktop-app.md|references/criteria/desktop-app.md" SKILL.md`
- [ ] `rg -n "^## " workflows/desktop-app.md` shows Identify / Evidence / Subject Rubric / Subject Verdict Notes
- [ ] File exists: `workflows/desktop-app.md`
- [ ] File exists: `references/criteria/desktop-app.md`

### Manual Verification

- [ ] Read `references/criteria/desktop-app.md` end-to-end; confirm distribution channel trust, code signing standards, installer type risk, sandboxing, auto-update risk, and tier thresholds are internally consistent
- [ ] Read `workflows/desktop-app.md` end-to-end; confirm it handles all three OS families (Windows, macOS, Linux) with appropriate depth
- [ ] Mental-trace eval id 18 through the workflow; confirm APPROVED is reachable because Firefox is a known vendor, winget is a recognized channel, and the app is code-signed
- [ ] Mental-trace eval id 19 through the workflow; confirm REJECTED follows from third-party mirror, repackaged branding, unknown source, .exe installer without provenance

### Acceptance Criteria Validation

| Criterion | How to Verify | Expected Result |
|-----------|---------------|-----------------|
| Workflow exists with correct template | Read `workflows/desktop-app.md` | 4 required sections present |
| Addendum exists with desktop-app scoring | Read `references/criteria/desktop-app.md` | Distribution channel, code signing, installer risk, sandboxing, auto-update, tier sections present |
| Dispatcher routes Type 6 correctly | Grep `SKILL.md` | Row 6 -> `workflows/desktop-app.md`; Reference Files bullets added |
| Positive Type 6 eval exists | Read `evals/evals.json` | id 18 present; APPROVED path assertions intact |
| Negative Type 6 eval exists | Read `evals/evals.json` | id 19 present; third-party mirror + repackaged assertions intact |
| No regressions | Diff `evals/evals.json` | ids 0-17 unchanged |
| Homebrew boundary clarified | Workflow Identify table | `brew install --cask` listed as desktop-app channel |

---

## Rollback Plan

1. Revert `SKILL.md` row 6 and remove the two Type 6 Reference Files bullets so Type 6 falls back to `workflows/generic.md`.
2. Revert `evals/evals.json` to remove ids 18 and 19.
3. Delete `workflows/desktop-app.md`.
4. Delete `references/criteria/desktop-app.md`.

Rollback order front-loads routing: restore `SKILL.md` first so unfinished Type 6 docs never become live.

---

## Notes

### Risks

- **Cross-platform breadth:** Type 6 spans Windows, macOS, and Linux with dramatically different installer types, signing models, and distribution channels. Mitigation: organize by universal concepts (signing, channel trust, sandboxing) with platform-specific tables, not platform-first sections.
- **Homebrew boundary ambiguity:** `brew install --cask` = desktop-app (Type 6); `brew install` (core formulae) = cli-binary (Type 7). This is now confirmed in the workflow's Identify table and the taxonomy open question. Edge case: some formulae install GUI apps — these should route by the `--cask` vs non-cask command, not by the app's nature.
- **Code signing verification depth:** Verifying Authenticode or Apple notarization programmatically requires local tools (`signtool`, `codesign`, `spctl`). Mitigation: v1 relies on web search and store listing signals for signing status; programmatic verification is out of scope.
- **Installer type opacity:** EXE installers are inherently opaque. Mitigation: classify by installer framework (NSIS, Inno Setup, WiX) when identifiable; flag unknown EXE installers as elevated risk.
- **Auto-update diversity:** Desktop app update mechanisms are vendor-specific and often undocumented. Mitigation: classify by pattern (store-managed, signed updater, unsigned updater, manual) rather than exhaustively cataloging every framework.

### Open Questions

- **Homebrew boundary status:** Confirmed by this plan. `brew install --cask` → Type 6. `brew install` (core formulae) → Type 7. Update the taxonomy open question to resolved during execution.
