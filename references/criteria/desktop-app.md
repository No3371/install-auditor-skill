# Desktop App — Criteria Addendum

Per-subject scoring extensions for **Type 6: desktop-app** audits.
Layers on top of `references/criteria.md`. More-specific guidance wins, except over its §4.6 floor (this file only tightens or fills it) and the §4.3 verdict classes.

Covers: Microsoft Store, Mac App Store, Homebrew cask (official and
third-party taps), winget, Chocolatey, Snap Store, Flathub, APT/YUM
repos, direct vendor download, third-party mirrors. Cross-platform:
Windows, macOS, Linux.

## Distribution Channel Trust Signals

| Channel | Verification Gate | Adoption Metric | Trust Notes |
|---------|-------------------|-----------------|-------------|
| Microsoft Store — MSIX, AppContainer | Microsoft certification; Store-signed package | Ratings + install count | Strongest Windows signal; declared capabilities; sandboxed |
| Microsoft Store — MSIX, full trust | Microsoft certification; Store-signed package | Ratings + install count | Reviewed; clean install/uninstall; runs at medium integrity with file/registry virtualization — **not** AppContainer-sandboxed |
| Microsoft Store — unpackaged Win32 (MSI/EXE) | Certification of a publisher-hosted installer at a versioned URL; installer signed by the publisher | Ratings + install count | No package identity, no sandbox; the app updates itself. Trust ≈ direct vendor download of a signed installer; the listing confirms only the publisher account |
| Mac App Store | Apple review; Apple-signed; App Sandbox mandatory | Ratings | Strongest macOS signal |
| Homebrew Cask (official `homebrew/cask`) | Maintainer-reviewed cask; SHA-256 of the vendor-hosted file; must pass Gatekeeper (Homebrew 5.0.0, 2025-11: casks failing it are deprecated, then disabled) | Install analytics on `formulae.brew.sh` | Binary comes from the vendor URL; review covers cask metadata, not the app. `sha256 :no_check` (usually with `version :latest`) = no checksum gate |
| Homebrew Cask (third-party tap, `<user>/<tap>/<name>`) | Tap owner only | Tap repo activity | Outside homebrew-cask review and its Gatekeeper policy; trust = tap owner identity. `brew trust` (Homebrew 6.0.0+) records consent, not review |
| winget | Manifest PR validation (schema, URL, hash, automated checks) | Manifest presence | Microsoft-operated repo; binary from the manifest's `InstallerUrl`. Many manifests are bot-submitted, so the hash binds whatever the URL served at submission |
| Chocolatey (community repo) | Moderation + automated virus scan; package scripts reviewed | Download count | Package maintainer is often not the vendor; scripts fetch the vendor binary with a checksum |
| Snap Store (strict) | Canonical-operated; automated review + confinement | Install count | Strict confinement limits system access, not what the app asks the user for: scam wallet snaps stole seeds through the UI |
| Snap Store (classic) | Canonical-operated; manual review for classic | Install count | Classic confinement = no sandbox |
| Flathub | Built from a public manifest (which may repackage the vendor binary); Flatpak sandbox | Install count | Verified ✓ = developer identity linked to the app ID's website or code host — identity, not a security review. Unverified apps may come from unaffiliated repackagers |
| APT/YUM official repos | Distro maintainer-reviewed; GPG-signed repo | Part of OS package set | Strongest Linux traditional signal; distro stands behind the package |
| APT/YUM third-party repo | Vendor GPG key | Download count (if available) | Key scope matters: an APT key bound with `signed-by=` signs only that repo; a key in the global keyring (`/etc/apt/trusted.gpg`, `trusted.gpg.d/`, legacy `apt-key`) is trusted for every configured repo |
| Direct vendor download | Vendor website only; no third-party review | Website traffic / brand recognition | Trust = vendor identity + signer match. Take the URL from the vendor's own docs or repo, not an ad or search result |
| Third-party mirror / repackager | None | None | Highest risk; binary provenance unverifiable; repackaging may inject payloads |

### Scoring impact

- Mac App Store or Microsoft Store MSIX (AppContainer) = strong positive (store review + sandboxing)
- Microsoft Store MSIX full trust = moderate positive (review, no sandbox)
- Microsoft Store unpackaged Win32 = score as a direct vendor download; the listing confirms the publisher account only. Package kind unknown → score as unpackaged
- APT/YUM official distro repo = strong positive (distro-maintained, GPG-signed)
- Official homebrew-cask / winget / Chocolatey = moderate positive (manifest review + checksum). A checksum proves the file matches the manifest, not who built it; signer identity is scored separately (Code Signing Standards, §4.6 V2)
- Cask with `sha256 :no_check` = no checksum credit (score as direct vendor download)
- Cask carrying a Gatekeeper deprecation or disable notice (`brew info --cask <name>`) = score as macOS not notarized (Code Signing Standards)
- Third-party cask tap = direct vendor download when the vendor documents the tap as its own; otherwise third-party repackager
- Snap strict / Flathub = moderate positive (sandboxed + review); Snap publisher ✓ and Flathub verified ✓ count only as identity evidence (§4.6 V2)
- Snap classic = weak positive (no sandbox; manual review exists)
- Vendor APT repo with a `signed-by=`-scoped key = moderate positive. Vendor instructions that install the key globally = MEDIUM flag; Recommendation: move the key to `/etc/apt/keyrings/` and reference it with `signed-by=`
- Direct vendor download with valid code signing = neutral (trust = vendor identity)
- Direct vendor download unsigned = strong negative
- Third-party mirror or repackager = strong negative (equivalent to sideloaded VSIX)
- Store or cask listing whose publisher or download URL does not match the vendor = impersonation check (Tier 3)

## Code Signing Standards

| Platform | Signing Method | Strength | Verification |
|----------|---------------|----------|--------------|
| Windows — Authenticode EV | EV code signing certificate | Strong (identity) | Stricter CA vetting of the publisher. No longer grants immediate SmartScreen reputation (removed 2024) |
| Windows — Authenticode OV (standard) | Standard code signing certificate | Moderate (identity) | Publisher identity validated by CA; SmartScreen may warn on low reputation |
| Windows — Azure Artifact Signing (formerly Trusted Signing) | Microsoft-managed identity validation; certificates valid only days | Strong (identity) | Subject = the validated organization or individual; signatures must be timestamped |
| Windows — unsigned | None | Absent | SmartScreen blocks or warns; no publisher identity |
| macOS — Developer ID + notarization | Developer ID certificate (Team ID) + Apple notarization | Strong (identity) | Notarization = identity + automated malware scan, not human review: notarized malware has shipped (MacSync dropper, 2025-12, revoked after report). Notarized apps pass Gatekeeper |
| macOS — Developer ID, not notarized | Developer ID certificate only | Weak | Gatekeeper blocks it by default (macOS 10.15+); since macOS 15 the user must approve it in System Settings → Privacy & Security (Control-click override removed) |
| macOS — unsigned / ad-hoc | None or self-signed | Absent | Gatekeeper blocks by default; user must override system security |
| Linux — GPG (distro key) | Distribution maintainer GPG key | Strong | Part of distro trust chain; `apt`/`dnf` verify automatically |
| Linux — GPG (vendor key) | Vendor-provided GPG key for third-party repo | Moderate | Match the key fingerprint to the vendor's docs; key scope matters (Distribution Channel table) |
| Linux — Sigstore / cosign | Sigstore keyless signing | Moderate-Strong | Credit only with certificate identity + OIDC issuer matched (§4.6 V2) |
| Linux — unsigned | None | Absent | No verification; binary provenance unknowable |

Publicly trusted code-signing keys must sit in an HSM or hardware token (CA/B Forum Code Signing Baseline Requirements, since 2023), so a hardware key is not EV-specific. Certificates issued from 2026-03-01 last ≤ 460 days, and Artifact Signing certificates only days. Signer **thumbprints** therefore rotate routinely: match the certificate **subject** (and the macOS Team ID), not the thumbprint. A renewed certificate can restart SmartScreen reputation, so an "unrecognized app" prompt on a correctly signed new build is a note, not a flag.

### Scoring impact

- Credit a signature only per `references/criteria.md` §4.6 V2: the signer (Team ID, certificate subject, GPG fingerprint, Sigstore identity) matches the vendor's documented or prior-release identity. Signed but not matched = note only
- Matched EV Authenticode, Artifact Signing, Developer ID + notarization or distro GPG = strong positive (origin, not safety)
- Matched OV Authenticode, vendor GPG or Sigstore = moderate positive
- macOS Developer ID without notarization = HIGH flag `not notarized`. Condition: use a notarized build, the Mac App Store version or an official cask; never bypass Gatekeeper
- Unsigned on any platform = HIGH flag (single strongest negative signal for desktop apps)
- Revoked signing certificate or notarization (assessment rejects a previously valid signature) = CRITICAL flag, unless the vendor documents the revocation and ships a re-signed build (then audit that build)
- Install instructions that tell the user to override Gatekeeper or SmartScreen (`xattr -d com.apple.quarantine`, `xattr -cr`, "Open Anyway" in System Settings, pasting a Terminal command "to verify", SmartScreen "Run anyway" on an unsigned file): from a source whose identity does not verify = CRITICAL flag (stealer lure). From a matched vendor about its own build = rate the underlying signing gap; the report never repeats the bypass as an instruction

## Installer Type Risk Classification

| Installer Type | Platform | Risk | Why |
|----------------|----------|------|-----|
| MSIX / APPX | Windows | Low (AppContainer) / Low-Medium (full trust) | Declared capabilities; clean uninstall; container-isolated only as AppContainer (Sandboxing Assessment) |
| MSI | Windows | Low-Medium | Structured installer format; auditable via `msiexec` logs; custom actions can run arbitrary code |
| EXE (NSIS, Inno, etc.) | Windows | Medium (signer matched) / Medium-High (unsigned or unmatched) | Opaque; can execute arbitrary code during install; bundleware/adware vector. Most major Windows vendors ship signed EXE installers |
| DMG (drag-to-Applications) | macOS | Low-Medium | Simple copy; no installer scripts; app bundle structure is inspectable |
| PKG (macOS) | macOS | Medium | Can run pre/post-install scripts with elevated privileges |
| AppImage | Linux | Low-Medium | Self-contained; no system integration; runs in user space; not sandboxed by default |
| Snap (strict) | Linux | Low | Sandboxed; declared interfaces; auto-update |
| Snap (classic) | Linux | Medium | No sandbox; full system access; manual review gate |
| Flatpak | Linux | Low | Sandboxed by default; declared permissions; portal-mediated access |
| .deb / .rpm | Linux | Medium | Can run pre/post-install scripts as root; risk depends on source repo trust |

### Scoring impact

- MSIX (AppContainer)/Snap-strict/Flatpak = positive (sandboxed, declared capabilities); full-trust MSIX = clean-install positive only
- MSI/DMG/AppImage = neutral-to-low-risk (structured or simple; inspectable)
- PKG/.deb/.rpm = note install scripts; risk depends on source trust
- EXE installer whose signer matches the vendor (§4.6 V2) = note; check for bundled offers. Unsigned or unmatched EXE = elevated scrutiny (opaque, arbitrary code execution)
- Snap classic = note lack of sandbox

## Sandboxing Assessment

| Sandbox Model | Platform | Strength | Notes |
|---------------|----------|----------|-------|
| App Sandbox | macOS (App Store) | Strong | Mandatory for Mac App Store; declared entitlements; limited file/network/hardware access |
| MSIX AppContainer | Windows | Moderate-Strong | Declared capabilities; virtual filesystem/registry; clean uninstall |
| MSIX full trust (`runFullTrust`) | Windows | Weak | Medium integrity; file/registry virtualization only, not a security boundary. Package kind unknown → assume full trust |
| Flatpak sandbox | Linux | Moderate-Strong | Bubblewrap-based; XDG portals for controlled access; permissions in manifest. Weakened by host-escape permissions (`--filesystem=host`/`home`, `--talk-name=org.freedesktop.Flatpak`, which can run host commands) and by an unpatched host Flatpak (e.g. CVE-2026-34078 sandbox escape, fixed in 1.16.4, 2026-04) |
| Snap strict confinement | Linux | Moderate-Strong | AppArmor-based; declared interfaces; auto-connecting interfaces reduce isolation; confinement ≠ legitimacy (UI-based scams still work) |
| Snap classic confinement | Linux | Absent | No meaningful sandbox; equivalent to traditional install |
| None (traditional install) | All | Absent | Full user-level (or root) access; no confinement |

### Scoring impact

- App Sandbox / MSIX AppContainer / Flatpak / Snap strict = positive signal (Flatpak: only with a patched host Flatpak and no host-escape permission)
- No sandboxing (traditional install, Snap classic) = neutral for well-known vendors, negative for unknown vendors
- Sandboxing is a bonus, not a requirement — many legitimate desktop apps run unsandboxed

## Auto-Update Mechanism Risk

| Pattern | Risk | Guidance |
|---------|------|----------|
| Store-managed updates (MS Store, Mac App Store, Snap, Flatpak) | Low | Updates go through store review pipeline |
| Signed auto-updater (Sparkle on macOS, Squirrel / electron-updater on Windows/Electron) | Low-Medium | Verify HTTPS + signature verification, and that the bundled updater version has no known signature-bypass advisory (e.g. electron-updater < 6.3.0-alpha.6, GHSA-9jxc-qjr9-vjxq) |
| Vendor-hosted updater with no signature verification | High | Persistent attack surface; hosting-level hijack exploited in the wild (Notepad++ WinGUp before 8.8.9, 2025) |
| No auto-update (manual download of new version) | Low (update) / Medium (staleness) | No update-channel risk, but user may run stale versions with known CVEs |
| Disabled or opt-out auto-update | Low-Medium | User controls update timing; staleness risk if updates are never applied |

### Scoring impact

- Store-managed or signed auto-updater = neutral (expected pattern)
- Update channel without signature verification, or an updater version with a known signature-bypass advisory = HIGH flag. Condition: turn off in-app auto-update and update only through a verified channel (store, package manager, signed vendor download), or install a release whose updater verifies
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
- Distributed via Mac App Store, Microsoft Store MSIX OR well-known package manager (official homebrew-cask, winget, Chocolatey with high download count). A Microsoft Store unpackaged Win32 listing does not qualify on the listing alone
- Code signed (Authenticode, Apple Developer ID + notarization, or distro GPG) with identity verified per §4.6 V2: the file's signer, or the channel binding (Version & Update Integrity, V2)
- Publisher is a known company or well-known open-source project
- App has been available >= 1 year, and `references/criteria.md` §4.6 V1–V4 leave Tier 1 available for this version
- No known incidents, removals, or security controversies
- Installer type is low-risk (MSIX, MSI, DMG, snap-strict, flatpak)

### Tier 2 — Standard Audit (default)

Default when not all Tier 1 criteria are met:
- Distributed via a recognized channel (including direct vendor download)
- Code signed (any level; credited per §4.6 V2)
- Identifiable publisher
- No known security incidents
- Available > 30 days

### Tier 3 — Deep Audit

ANY of these triggers:
- Unsigned binary, or macOS app not notarized
- Signer identity differs from the vendor's documented or prior-release identity (§4.6 V3)
- Install instructions ask the user to override Gatekeeper or SmartScreen
- Direct download from unknown or unverifiable source
- Third-party mirror or repackager (not original vendor)
- EXE installer from non-store source with no code signing
- Shared via chat/email/forum link (not discovered via official channel)
- Recent acquisition or publisher change
- Known prior removal from store or security incident
- App requests admin/root privileges with unclear justification
- Bundleware or adware reports in web search results

## CVE Scope (§4.3)

Fills the `references/criteria.md` §4.3 **Addendum:** line. The verdict classes stay as §4.3 and `SKILL.md` "Blocking CVE" define them.

- **Own code:** the app's own binaries, plus components the vendor forks and maintains.
- **Third-party component:** bundled runtimes and libraries (Electron/Chromium, Qt, .NET, Java runtime, OpenSSL, media codecs), Snap base snaps and Flatpak runtimes, and distro packages a `.deb`/`.rpm` depends on. A bundled component is fixed for the user only when a vendor release ships the fixed version; that release is the **fixed release** to name in the condition.
- **Scan sources:** NVD (app CPE), vendor security advisories, OSV/GHSA for open-source apps. For a bundled runtime, find its version (release notes, About dialog; for Electron apps the bundled Electron version) and check that runtime's advisories. Distro security trackers for repo packages.
- **VEX sources:** vendor CSAF/VEX feeds where published (common for Linux distro packages).

## Version & Update Integrity (§4.6)

Fills the `references/criteria.md` §4.6 plug-ins. Anything not listed → shared default.

- **V1 Version age:** age = time since the vendor published this version (release notes, GitHub release, store "updated" date). If the channel's manifest for that version changed later (new `InstallerUrl` / cask `url` or SHA-256 under the same version string), age counts from that change and V3 applies. Version unit = version string + installer hash per architecture; store-managed apps use the store build. A cask with `version :latest` + `sha256 :no_check` has no version unit → V1 `Unknown`. Desktop channels have no client cooldown setting: the condition is "install the previous version and hold it" (V5 controls).
- **V2 Verified identity:** mechanisms: macOS Team ID + notarization; Authenticode certificate subject (incl. Artifact Signing); MSIX package publisher; distro or vendor GPG fingerprint; Snap publisher ✓; Flathub verified ✓. Expected identity: the vendor's download, security or verification page; else the identity on the vendor's prior releases. Two ways to verify:
  - **Channel binding** (enough for Tier 1; no file needed): the store listing, cask or winget manifest names the vendor's documented publisher **and** its download URL is on the vendor's documented domain or release host.
  - **File-level** (Tier 2/3 when the file is at hand; otherwise a Post-Install Checklist step before first launch): the signer printed by these commands matches the expected identity.

    ```
    codesign -dv --verbose=4 <path>/<App>.app 2>&1 | grep -E 'Authority|TeamIdentifier'
    spctl --assess --type execute -vv <path>/<App>.app    # expect accepted, source=Notarized Developer ID
    pkgutil --check-signature <file>.pkg
    Get-AuthenticodeSignature <file> | Format-List Status,SignerCertificate,TimeStamperCertificate
    ```

  Absence: unsigned = HIGH flag (Code Signing Standards). Signed, but no expected identity can be found = note, no credit, Tier 1 unavailable. Manifest checksums (cask, winget, Chocolatey) are transport integrity, not identity. **Curated pipelines:** none. App stores review submissions but do not build them, so the developer's Team ID or store publisher remains the identity to match.
- **V3 Continuity:** compare with the prior release:
  - signer subject / Team ID; a thumbprint or issuer change with the same subject = note (routine rotation or CA migration)
  - notarization present → absent
  - package kind or confinement (MSIX → unpackaged, AppContainer → full trust, strict → classic snap)
  - manifest `InstallerUrl` or cask `url` domain
  - entitlements (`codesign -d --entitlements - <path>/<App>.app`), MSIX capabilities, snap plugs, Flatpak permissions (`flatpak info --show-permissions <id>`)
  - new privileged components (driver, kernel/system extension, privileged helper, launch daemon, SYSTEM service)

  Unexplained items rate per §4.6 V3; explained privilege increases rate per the workflow's §4.4 Permissions. Ownership transfer: store publisher or Team ID change after an acquisition = MEDIUM; with new elevated privileges = the workflow's Toward REJECTED "Recent acquisition + privilege escalation".
- **V4 Incident sources:** Apple revocation (assessment newly rejects); store takedowns (Microsoft Store, Mac App Store, Snap Store, Flathub); a cask's disable reason (`brew info --cask <name>`); removal PRs in `microsoft/winget-pkgs`; Microsoft Defender detections; vendor postmortems on compromised update servers or signing keys. For an update-channel compromise the affected range is the delivery window: a user who updated through that channel inside the window gets the incident-response note.
- **V5 Updates:** extra triggers: updater framework or update URL change | new privileged component | package kind, confinement or notarization change | store publisher change | privacy-policy change that expands collection.
  - Update controls to name in the Recommendation: `winget pin add --id <id>` | `choco pin add -n=<name>` | `apt-mark hold <pkg>` | `snap refresh --hold <name>` | `flatpak mask <id>` | the app's own auto-update setting (Sparkle, Squirrel, electron-updater) | MDM policy where managed.
  - No per-app hold: Homebrew casks (`brew pin` covers formulae only, and casks marked `auto_updates true` update themselves); Mac App Store and Microsoft Store (global auto-update setting only). Say so, and list the triggers to watch.
