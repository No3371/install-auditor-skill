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
