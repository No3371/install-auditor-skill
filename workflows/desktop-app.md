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
