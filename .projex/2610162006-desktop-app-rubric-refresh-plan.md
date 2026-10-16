# Desktop-App Rubric Refresh

> **Status:** Ready
> **Author:** Claude (Opus)
> **Parent:** 2610161928-stewardship-review-container-cli-desktop-eval.md
> **Source:** 2610161928-stewardship-review-container-cli-desktop-eval.md (D1–D9; X1/X2 subject parts) | 2610161941-shared-version-integrity-floor-plan.md Hand-off rows "desktop-app" + "§4.3 plug-in … bundled runtimes" | human decision C6 (relayed by orchestrator 2026-10-16)
> **Related Projex:** 2610161941-shared-version-integrity-floor-plan.md (contract this fills; must be closed on base first) | sibling refresh plans for cli-binary (same review; owns Homebrew formulae/taps, `workflows/cli-binary.md`, `references/criteria/cli-binary.md`) and container-image | later eval-refresh plan (receives Notes → Eval hand-off)
> **Worktree:** Yes

---

## Summary

The desktop-app rubric dates from 2026-04-15 and its trust tables now lag the platforms. It grades non-notarized macOS apps as "Moderate", although Gatekeeper blocks them. It credits EV with instant SmartScreen reputation, which Microsoft removed in 2024. It treats every Microsoft Store listing as a sandboxed MSIX, though the Store accepts unpackaged Win32 installers. It says Homebrew casks have no signing gate, which Homebrew 5.0.0 changed. It rates an unsigned updater both "Medium-High" and "MEDIUM flag". Signatures earn credit merely for being present; the notarized MacSync dropper shows why that fails.

This plan rewrites the channel and signing tables and fixes the updater, installer and sandbox rows. It also fills the shared floor's plug-ins: `## Version & Update Integrity (§4.6)` (V1–V5) and the §4.3 own-code line, `## CVE Scope (§4.3)`. Finally it aligns `workflows/desktop-app.md` to the new addendum.

**Scope:** `references/criteria/desktop-app.md` | `workflows/desktop-app.md`. Nothing else.
**Estimated Changes:** 2 files. Addendum: 2 section rewrites, 15 replacements, 2 new sections (10,255 B → 22,632 B, simulated). Workflow: 28 replacements (16,915 B → 21,500 B, simulated).

---

## Objective

### Problem / Gap / Need

| ID | Gap (base `968e70f`) | Fix |
|---|---|---|
| D1 | `macOS — Developer ID only` = "Moderate … Gatekeeper allows with warning" (addendum L45). Gatekeeper blocks non-notarized software by default since 10.15. macOS 15 removed the Control-click override, so approval now goes through System Settings. | Weak + HIGH flag `not notarized`. Instructions to bypass Gatekeeper/SmartScreen are a lure (CRITICAL from an unverified source) |
| D2, X1 | Signing = "strong positive" on presence (addendum L54; workflow L349). Notarized MacSync dropper (Team ID `GNJLS3UYZ4`, 2025-12, revoked after report) | Credit only per §4.6 V2 (signer matches the vendor's documented or prior-release identity); revocation = CRITICAL; V2 plug-in names the commands |
| D3 | EV row: "SmartScreen reputation immediate" + "Hardware token required" (L41). Artifact Signing missing | EV keeps stricter vetting only. HSM/token storage applies to all public code-signing certs. ≤ 460-day certs (from 2026-03-01) + short-lived Artifact Signing certs → match the **subject**, not the thumbprint. Add an Artifact Signing row |
| D4 | "Microsoft Store (MSIX) … run in container" (L14); "signed by definition" (workflow L165); Tier 1 on a store listing alone | 3 Store rows: MSIX AppContainer, MSIX full trust, unpackaged Win32. Unpackaged scored as a vendor download. Full-trust MSIX ≠ sandbox |
| D5 | Cask "no signing gate" (L16); third-party taps absent | Official cask: Gatekeeper-passing expected; a deprecation/disable notice → scored as not notarized; `sha256 :no_check` → no checksum credit. Third-party tap = vendor-direct or repackager |
| D6 | Unsigned updater = "Medium-High" (L105) vs "MEDIUM flag" (L112). No updater-framework check | HIGH, both places (Notepad++ WinGUp < 8.8.9 hijack). Updater framework version vs signature-bypass advisories (electron-updater GHSA-9jxc-qjr9-vjxq) |
| D7 | Snap/Flathub legitimacy signals absent; Flatpak sandbox credit not tied to the runtime version | Confinement ≠ legitimacy. Flathub verified ✓ = identity, not review. Flatpak credit needs a patched host (CVE-2026-34078, fixed 1.16.4) and no host-escape permission |
| D8 | "EXE installer from known vendor → CONDITIONAL" (workflow L330), which latently contradicts eval 18 (Firefox winget = NSIS EXE per secondary source) | Signed EXE with matched signer = note. Unsigned/unmatched EXE = condition |
| D9 | Vendor APT key scope not distinguished | `signed-by=`-scoped key vs global keyring (trusted for every repo) → MEDIUM flag |
| Floor | No §4.6 plug-in. No §4.3 own-code line. Coverage table lacks the `Version integrity` row and drops canonical Required rows. Workflow heading `### 4.6 Alternatives` collides with the new `criteria.md` §4.6 | Add both plug-ins. Add the coverage rows plus a canonical-name map. Rename the heading to `### Alternatives …` |

### Success Criteria

- [ ] Addendum has `## Version & Update Integrity (§4.6)` with exactly one bullet each starting `- **V1 `…`- **V5 `, and `## CVE Scope (§4.3)`.
- [ ] Every `§4.6 V<n>` in both files names an existing `### V<n> ` heading in `references/criteria.md`.
- [ ] Stale phrases absent from both files (case-insensitive): `SmartScreen reputation immediate` | `Gatekeeper allows with warning` | `no signing gate` | `MSIX apps run in container` | `signed by definition` | `Unsigned update channel = MEDIUM` | `GitHub stars on` | `EXE installer from known vendor` | `Apple checks for malware` | `Hardware token required` | `### 4.6 Alternatives`.
- [ ] One severity for an unverified update channel: `HIGH` in the addendum table row, the scoring bullet and the workflow's Toward CONDITIONAL.
- [ ] Workflow coverage table has the `Version integrity (§4.6)` row (Required ×3) and the canonical-name map paragraph.
- [ ] The addendum leaves C6 verdict classes untouched: no `REJECTED` in `## CVE Scope (§4.3)`.
- [ ] `python3 evals/run_evals.py validate` passes. `python3 -m unittest discover -s evals -p "test_*.py"` passes with the Preflight test count.
- [ ] Paper traces P1–P10 give the stated outcomes.
- [ ] `git diff --stat <base>..HEAD` lists only the 2 files.

### Out of Scope

- `SKILL.md`, `references/criteria.md`, `references/report-template.md`, `references/classifier.md`: owned by the floor plan, which must already be closed.
- `evals/`: case and description changes go to the eval plan (Notes → Eval hand-off). No live `run`; the human decided on one paid run after all refreshes.
- Homebrew formulae, taps of formulae, `brew install <formula>` routing: cli-binary plan.
- Other workflows' `### 4.6 …` heading collisions (Notes → Cross-cutting).
- `STEWARDSHIP.md` (Last Reviewed dates and trigger text belong to the orchestrator).

---

## Context

### Current State

- `references/criteria/desktop-app.md` (10,255 B, 162 lines): channel table + scoring (L10–35); signing table + scoring (L37–57); installer (L59–80); sandbox (L82–97); auto-update (L99–113); telemetry; tiers (L130–162). Header L4: "More-specific guidance wins." No §4.6/§4.3 plug-ins.
- `workflows/desktop-app.md` (16,915 B, 358 lines, wrapped ~76 cols): Identify, Evidence A (tiers) / B (research, coverage table L193–206), Subject Rubric `### 4.1`…`### 4.6 Alternatives` (L291), Verdict Notes (L306–354).
- Neither file has changed in substance since 2026-04-15 (`git log`: `f957bc5`, `cb04a17`, `5c44b79` header-only).
- Shared floor (2610161941-shared-version-integrity-floor-plan.md) **closed onto base** as `20843cc` while this plan was drafted (walkthrough: no shipped-text deviation). Planning re-checked all 6 P0 floor counts at base `242310a` ✓. It adds `criteria.md` §4.6 V1–V5 (+ `**Curated pipelines:**`), the §4.3 C6 table + `**Addendum:**` line, `SKILL.md` "Blocking CVE" + "Confirmed supply chain compromise", and the precedence rule that addenda only tighten §4.6.
- Evals on this workflow: 18 (Firefox winget → exact APPROVED), 19 (fake VLC "Pro" mirror → exact REJECTED), 29 (OBS installer vs MS Store → APPROVED|CONDITIONAL). No assertion names a table row, a severity word or a heading.

### Key Files

| File | Role | Change Summary |
|---|---|---|
| `references/criteria/desktop-app.md` | Desktop scoring addendum | Channel + signing rewrites; installer/sandbox/updater rows; tiers; + `## CVE Scope (§4.3)`, `## Version & Update Integrity (§4.6)` |
| `workflows/desktop-app.md` | Desktop workflow | Identity-matching research, Store package kind, coverage rows, heading rename, verdict notes (D1/D2/D6/D8, V4) |

### Dependencies

- **Requires:** 2610161941-shared-version-integrity-floor-plan.md **closed onto base** `claude/youthful-dijkstra-5ov1kt` (satisfied at `20843cc`; P0 re-checks). The plan text cites `§4.6 V1–V5`, `**Curated pipelines:**`, `Blocking CVE`; without them the references dangle.
- **Concurrent (no file overlap):** the other per-subject refresh plans. The cli-binary plan shares the review: it owns formulae and taps, this plan owns casks, including casks from third-party taps.
- **Blocks:** the eval-refresh plan (desktop cases in Notes).

### Constraints

- Addendum tables stay one line per row; the workflow wraps at ~76 columns like the surrounding text.
- C6: the addendum names the own-code / third-party boundary and the sources only. It never restates or changes the REJECTED/CONDITIONAL classes.
- Floor precedence: the plug-ins may tighten §4.6 or fill what its `**Addendum:**` lines ask for; they never loosen it.
- Dated facts carry a year and stay out of thresholds (review Risk "dated specifics rot"). Versions appear only as examples.
- No projex filenames in shipped files.

### Assumptions

- **A1 (verify in P0):** floor closed on base with the headings above. If not → set this plan `Blocked`, stop.
- **A2:** `codesign -dv --verbose=4`, `spctl --assess --type execute -vv`, `pkgutil --check-signature` and `Get-AuthenticodeSignature` print signer + Team ID / subject, and `spctl` reports `source=Notarized Developer ID` and rejects revoked signatures. These are standard macOS/PowerShell tools, not re-checked on macOS 15+ (Sequoia reduced `spctl`'s rule-editing powers; assessment is assumed intact). The execution host (Linux) can't run them, so the step only quotes them.
- **A3:** eval 18's `Mozilla.Firefox` winget installers are NSIS EXE, from a Mozilla-owned URL (secondary source only; manifest not read). If the manifest instead shows MSI, D8 still holds and P1 just gets simpler.
- **A4:** `winget pin add --id <id>`, `choco pin add -n=<name>`, `apt-mark hold`, `snap refresh --hold <name>` and `flatpak mask <id>` hold updates. The snap and flatpak forms were confirmed (Canonical blog, flatpak-mask man page); the winget and choco forms come from memory.
- **A5:** Mac App Store and Microsoft Store offer only global auto-update control, and `brew pin` does not cover casks (cask pin: secondary source).

### Impact Analysis

- **Direct:** the 2 files.
- **Adjacent:** `SKILL.md` Step N consumes the new CRITICAL/HIGH ratings via "CRITICAL flag" and "HIGH-severity flags". `references/report-template.md` Post-Install line "Verify checksum/signature against the expected identity" (from the floor) is where the V2 file-level commands land when no file is at hand.
- **Downstream verdict changes:**
  - Non-notarized macOS apps: moderate positive → HIGH → CONDITIONAL.
  - Unverified update channels: MEDIUM → HIGH → CONDITIONAL.
  - Microsoft Store unpackaged Win32 apps: no Tier 1 on the listing alone.
  - Signed-EXE apps from matched vendors: no longer pushed to CONDITIONAL (helps eval 18).
  - Gatekeeper-bypass lures from unverified sources: → REJECTED.
  - Renewed certificates with the same subject: no V3 flag.

---

## Implementation

### Overview

P0 preflight → addendum (Steps 1–4) → workflow (Step 5). Each change is an exact `Before → After` pair, or one whole-section swap bounded by two quoted lines. All 44 Before strings and 3 section bounds were checked to occur exactly once. The target files are unchanged between `968e70f` and base `242310a`. A scratch simulation applied every step and passed the consistency script plus every per-step grep. Use Edit per pair. A miss means the base moved: re-read that region and re-anchor; don't rephrase.

### P0 Preflight (`<work-root>`)

```bash
grep -c "^## 4\.6 Version & Update Integrity (shared floor)" references/criteria.md   # 1
grep -c "^### V[1-5] " references/criteria.md                                         # 5
grep -c "^- \*\*Curated pipelines:\*\*" references/criteria.md                        # 1
grep -c "draws the own-code / third-party line" references/criteria.md                # 1 (§4.3 Addendum line)
grep -c "Blocking CVE" SKILL.md                                                       # ≥ 1
grep -c "Confirmed supply chain compromise" SKILL.md                                  # ≥ 1
git diff --stat 968e70f -- workflows/desktop-app.md references/criteria/desktop-app.md   # empty (else re-anchor)
python3 evals/run_evals.py validate | head -3                                         # pass
python3 -m unittest discover -s evals -p "test_*.py" 2>&1 | tail -3                   # record count
```

Any count mismatch in the first 6 lines → floor not landed → status `Blocked`, stop.

---

### Step 1: Addendum — header coverage + Distribution Channel section (D4, D5, D7, D9)

**Objective:** split the Store and cask rows, add the third-party APT row and its key-scope rule, and add legitimacy caveats.
**Confidence:** High (D4 MS Learn; D5 policy per brew.sh 5.0.0); Medium on cask enforcement — the rule keys on the notice, not a date.
**Depends on:** P0
**Do-Projex:** Encouraged

**Files:** `references/criteria/desktop-app.md`

**Changes:**

```markdown
// 1a Before:
Covers: Microsoft Store, Mac App Store, Homebrew cask, winget,
Chocolatey, Snap Store, Flathub, direct vendor download, third-party
mirrors. Cross-platform: Windows, macOS, Linux.
// 1a After:
Covers: Microsoft Store, Mac App Store, Homebrew cask (official and
third-party taps), winget, Chocolatey, Snap Store, Flathub, APT/YUM
repos, direct vendor download, third-party mirrors. Cross-platform:
Windows, macOS, Linux.
```

**1b:** replace the block from the line `## Distribution Channel Trust Signals` through the line `- Third-party mirror or repackager = strong negative (equivalent to sideloaded VSIX)` (base L10–L35, inclusive) with:

```markdown
## Distribution Channel Trust Signals

| Channel | Verification Gate | Adoption Metric | Trust Notes |
|---------|-------------------|-----------------|-------------|
| Microsoft Store — MSIX, AppContainer | Microsoft certification; Store-signed package | Ratings + install count | Strongest Windows signal; declared capabilities; sandboxed |
| Microsoft Store — MSIX, full trust | Microsoft certification; Store-signed package | Ratings + install count | Reviewed; clean install/uninstall; runs at medium integrity with file/registry virtualization — **not** AppContainer-sandboxed |
| Microsoft Store — unpackaged Win32 (MSI/EXE) | Certification of a publisher-hosted installer at a versioned URL; installer signed by the publisher | Ratings + install count | No package identity, no sandbox; the app updates itself. Trust ≈ direct vendor download of a signed installer; the listing confirms only the publisher account |
| Mac App Store | Apple review; Apple-signed; App Sandbox mandatory | Ratings | Strongest macOS signal |
| Homebrew Cask (official `homebrew/cask`) | Maintainer-reviewed cask; SHA-256 of the vendor-hosted file; must pass Gatekeeper (Homebrew 5.0.0, 2025-11: casks failing it are deprecated, then disabled) | Install analytics on `formulae.brew.sh` | Binary comes from the vendor URL; review covers cask metadata, not the app. `sha256 :no_check` (usually with `version :latest`) = no checksum gate |
| Homebrew Cask (third-party tap, `<user>/<tap>/<name>`) | Tap owner only | Tap repo activity | Outside homebrew-cask review and its Gatekeeper policy; trust = tap owner identity |
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
```

**Rationale:**
- **D4.** Microsoft Learn: packaged desktop apps run at medium integrity unless `TrustLevel="appContainer"`, and Store MSI/EXE installers are publisher-hosted and self-updating. The conservative default for an unknown package kind is unpackaged.
- **D5.** The cask rule keys on what the auditor can see (`brew info` notice, `:no_check`), not on whether the 2026-09-01 disable actually happened (unconfirmed).
- **D9.** Ships as a MEDIUM rather than a condition because the fix is cheap, and an unscoped key is a real but common legacy practice.
- **Adoption metric.** "GitHub stars on formula repo" measured the whole homebrew-cask repo. Per-cask install analytics are the real metric.

**Verification:** `grep -c "^| Microsoft Store — " references/criteria/desktop-app.md` → 3; `grep -ci "no signing gate\|MSIX apps run in container\|GitHub stars on" references/criteria/desktop-app.md` → 0; `grep -c "third-party tap" references/criteria/desktop-app.md` ≥ 2.

**If this fails:** `git -C <work-root> checkout -- references/criteria/desktop-app.md` and redo Step 1.

---

### Step 2: Addendum — Code Signing Standards section (D1, D2, D3, X1)

**Objective:** grade notarization as identity rather than safety, fix the non-notarized and EV rows, add Artifact Signing, and add identity-matched scoring, revocation and the bypass-lure rule.
**Confidence:** High (D1 Apple-change coverage; EV/SmartScreen on Microsoft Learn; CSC-31 460 d via CA posts; MacSync via Jamf). Medium on the exact Artifact Signing lifetime, so the text says only "days".
**Depends on:** Step 1 (references the channel table)
**Verify-Projex:** Encouraged (changes verdict classes for macOS)

**Files:** `references/criteria/desktop-app.md`

**Changes:** replace the block from the line `## Code Signing Standards` through the line `- Unsigned on any platform = HIGH flag (single strongest negative signal for desktop apps)` (base L37–L57, inclusive) with:

```markdown
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
```

**Rationale:**
- **D1.** Moving non-notarized from moderate positive to a HIGH flag matches what macOS actually enforces. The condition steers the user to a gated channel instead of a bypass.
- **Lure rule.** It covers the observed ClickFix / fake-brew.sh / MacSync delivery (review B4/D1). It is CRITICAL only when identity fails, so legitimate open-source apps documenting `xattr` for unsigned builds stay CONDITIONAL.
- **Thumbprint vs subject.** This is what keeps V3 from firing on every renewal under 460-day and few-day certificates.
- **Revocation = CRITICAL.** Apple revokes after malware reports (MacSync). A vendor-explained revocation is the only exit.

**Verification:** `grep -ci "SmartScreen reputation immediate\|Gatekeeper allows with warning\|Apple checks for malware\|Hardware token required" references/criteria/desktop-app.md` → 0; `grep -c "Artifact Signing" references/criteria/desktop-app.md` ≥ 2; `grep -c "not notarized" references/criteria/desktop-app.md` ≥ 2.

**If this fails:** restore the section from `git -C <work-root> show HEAD:references/criteria/desktop-app.md` and redo Step 2.

---

### Step 3: Addendum — installer, sandbox and auto-update rows (D4, D6, D7, D8)

**Objective:** split MSIX by trust level, give signed and unsigned EXE separate ratings, attach Flatpak/Snap caveats, and make the updater severity HIGH in both places.
**Confidence:** High (GHSA-9jxc-qjr9-vjxq on OSV; Notepad++ 8.8.9 notice; CVE-2026-34078 record "< 1.16.4")
**Depends on:** Step 2
**Do-Projex:** Encouraged

**Files:** `references/criteria/desktop-app.md`

**Changes:** 11 exact replacements.

```markdown
// 3a Before:
| MSIX / APPX | Windows | Low | Container-isolated; declared capabilities; clean uninstall |
// 3a After:
| MSIX / APPX | Windows | Low (AppContainer) / Low-Medium (full trust) | Declared capabilities; clean uninstall; container-isolated only as AppContainer (Sandboxing Assessment) |

// 3b Before:
| EXE (NSIS, Inno, etc.) | Windows | Medium-High | Opaque; can execute arbitrary code during install; bundleware/adware vector |
// 3b After:
| EXE (NSIS, Inno, etc.) | Windows | Medium (signer matched) / Medium-High (unsigned or unmatched) | Opaque; can execute arbitrary code during install; bundleware/adware vector. Most major Windows vendors ship signed EXE installers |

// 3c Before:
- MSIX/Snap-strict/Flatpak = positive (sandboxed, declared capabilities)
// 3c After:
- MSIX (AppContainer)/Snap-strict/Flatpak = positive (sandboxed, declared capabilities); full-trust MSIX = clean-install positive only

// 3d Before:
- EXE installer = elevated scrutiny (opaque, arbitrary code execution)
// 3d After:
- EXE installer whose signer matches the vendor (§4.6 V2) = note; check for bundled offers. Unsigned or unmatched EXE = elevated scrutiny (opaque, arbitrary code execution)

// 3e Before:
| MSIX container | Windows (MS Store) | Moderate-Strong | Virtual filesystem/registry; declared capabilities; clean uninstall |
// 3e After:
| MSIX AppContainer | Windows | Moderate-Strong | Declared capabilities; virtual filesystem/registry; clean uninstall |
| MSIX full trust (`runFullTrust`) | Windows | Weak | Medium integrity; file/registry virtualization only, not a security boundary. Package kind unknown → assume full trust |

// 3f Before:
| Flatpak sandbox | Linux | Moderate-Strong | Bubblewrap-based; XDG portals for controlled access; permissions in manifest |
// 3f After:
| Flatpak sandbox | Linux | Moderate-Strong | Bubblewrap-based; XDG portals for controlled access; permissions in manifest. Weakened by host-escape permissions (`--filesystem=host`/`home`, `--talk-name=org.freedesktop.Flatpak`, which can run host commands) and by an unpatched host Flatpak (e.g. CVE-2026-34078 sandbox escape, fixed in 1.16.4, 2026-04) |

// 3g Before:
| Snap strict confinement | Linux | Moderate-Strong | AppArmor-based; declared interfaces; auto-connecting interfaces reduce isolation |
// 3g After:
| Snap strict confinement | Linux | Moderate-Strong | AppArmor-based; declared interfaces; auto-connecting interfaces reduce isolation; confinement ≠ legitimacy (UI-based scams still work) |

// 3h Before:
- App Sandbox / MSIX container / Flatpak / Snap strict = positive signal
// 3h After:
- App Sandbox / MSIX AppContainer / Flatpak / Snap strict = positive signal (Flatpak: only with a patched host Flatpak and no host-escape permission)

// 3i Before:
| Signed auto-updater (Sparkle on macOS, Squirrel on Windows/Electron) | Low-Medium | Verify update server uses HTTPS + signature verification |
// 3i After:
| Signed auto-updater (Sparkle on macOS, Squirrel / electron-updater on Windows/Electron) | Low-Medium | Verify HTTPS + signature verification, and that the bundled updater version has no known signature-bypass advisory (e.g. electron-updater < 6.3.0-alpha.6, GHSA-9jxc-qjr9-vjxq) |

// 3j Before:
| Vendor-hosted updater with no signature verification | Medium-High | Update channel is a persistent attack surface; MITM possible |
// 3j After:
| Vendor-hosted updater with no signature verification | High | Persistent attack surface; hosting-level hijack exploited in the wild (Notepad++ WinGUp before 8.8.9, 2025) |

// 3k Before:
- Unsigned update channel = MEDIUM flag (persistent attack surface)
// 3k After:
- Update channel without signature verification, or an updater version with a known signature-bypass advisory = HIGH flag. Condition: turn off in-app auto-update and update only through a verified channel (store, package manager, signed vendor download), or install a release whose updater verifies
```

**Rationale:**
- **D6.** Pick HIGH: a real hijack (Notepad++) went through exactly this pattern, and the condition is actionable.
- **D8.** Signed-and-matched EXE is the norm for major vendors, so pushing all EXEs to CONDITIONAL contradicted eval 18.
- **D7.** Flatpak credit now depends on the host version and on `finish-args`, because `org.freedesktop.Flatpak` access permits `flatpak-spawn --host`.

**Verification:** `grep -c "Unsigned update channel = MEDIUM" references/criteria/desktop-app.md` → 0; `grep -c "| High | Persistent attack surface" references/criteria/desktop-app.md` → 1; `grep -c "^| MSIX " references/criteria/desktop-app.md` → 3.

**If this fails:** `git -C <work-root> diff references/criteria/desktop-app.md` and revert the failing pairs by hand (each pair is independent).

---

### Step 4: Addendum — precedence line, tiers, `## CVE Scope (§4.3)`, `## Version & Update Integrity (§4.6)`

**Objective:** subordinate the addendum to the floor, gate Tier 1 on V2/V1–V4, add the new Tier 3 triggers, and fill both plug-ins.
**Confidence:** High (structure follows the floor contract); Medium on A2/A4/A5 commands
**Depends on:** Steps 2–3 (cites their rows)
**Verify-Projex:** Encouraged (contract compliance; easy to loosen §4.6 by accident)

**Files:** `references/criteria/desktop-app.md`

**Changes:**

```markdown
// 4a Before:
Layers on top of `references/criteria.md`. More-specific guidance wins.
// 4a After:
Layers on top of `references/criteria.md`. More-specific guidance wins, except over its §4.6 floor (this file only tightens or fills it) and the §4.3 verdict classes.

// 4b Before:
- Distributed via official store (MS Store, Mac App Store) OR well-known package manager (Homebrew cask, winget, Chocolatey with high download count)
- Code signed (Authenticode, Apple Developer ID + notarization, or distro GPG)
- Publisher is a known company or well-known open-source project
- App has been available >= 1 year
- No known incidents, removals, or security controversies
// 4b After:
- Distributed via Mac App Store, Microsoft Store MSIX OR well-known package manager (official homebrew-cask, winget, Chocolatey with high download count). A Microsoft Store unpackaged Win32 listing does not qualify on the listing alone
- Code signed (Authenticode, Apple Developer ID + notarization, or distro GPG) with identity verified per §4.6 V2: the file's signer, or the channel binding (Version & Update Integrity, V2)
- Publisher is a known company or well-known open-source project
- App has been available >= 1 year, and `references/criteria.md` §4.6 V1–V4 leave Tier 1 available for this version
- No known incidents, removals, or security controversies

// 4c Before:
- Code signed (any level)
// 4c After:
- Code signed (any level; credited per §4.6 V2)

// 4d Before:
- Unsigned binary
// 4d After:
- Unsigned binary, or macOS app not notarized
- Signer identity differs from the vendor's documented or prior-release identity (§4.6 V3)
- Install instructions ask the user to override Gatekeeper or SmartScreen
```

**4e:** append after the last line (`- Bundleware or adware reports in web search results`), separated by one blank line:

````markdown
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
````

**Rationale:**
- **Channel binding.** It is a V2 match on the "publisher account" identity the floor lists. Without it, Tier 1 would need a downloaded file, which no Tier 1 quick audit has. The file-level check still happens, as a Post-Install step, so nothing goes unchecked.
- **Curated pipelines: none.** Stated explicitly so no auditor reads store review as the DOI-style hook.
- **CVE Scope.** Puts bundled Chromium/Electron on the third-party side, per C6 ("only own code rejects when unfixed"). The fixed-release rule makes the condition actionable, since a user can't patch a bundled runtime.

**Verification:** see the consistency script (Verification Plan); plus `grep -c "^- \*\*V[1-5] " references/criteria/desktop-app.md` → 5; `awk '/^## CVE Scope/,/^## Version/' references/criteria/desktop-app.md | grep -c REJECTED` → 0.

**If this fails:** `git -C <work-root> diff references/criteria/desktop-app.md`; revert 4a–4e and redo from the base text of those regions.

---

### Step 5: Workflow — align `workflows/desktop-app.md`

**Objective:** make the workflow ask for signer identity and Store package kind, carry the coverage rows, avoid the §4.6 heading collision, and route verdict notes to the new ratings.
**Confidence:** High
**Depends on:** Steps 1–4 (names their rows and plug-ins)
**Verify-Projex:** Encouraged (28 pairs; a dropped pair leaves an inconsistency)

**Files:** `workflows/desktop-app.md`

**Changes:** 28 exact replacements; keep ~76-column wrapping.

```markdown
// 5a Before:
specific desktop-app guidance wins.
// 5a After:
specific desktop-app guidance wins — except over the version-integrity
floor (`references/criteria.md` §4.6) and the §4.3 CVE verdict classes,
which the addendum only fills.

// 5b Before:
| Homebrew Cask | `brew install --cask <name>`, `formulae.brew.sh/cask/*` | GitHub stars on cask formula |
// 5b After:
| Homebrew Cask (official) | `brew install --cask <name>`, `formulae.brew.sh/cask/*` | Install analytics on formulae.brew.sh |
| Homebrew Cask (third-party tap) | `brew install --cask <user>/<tap>/<name>`, `brew tap <user>/<tap>` | Tap repo activity |

// 5c Before:
- **Version**: Current version (if determinable)
// 5c After:
- **Version**: Exact version + installer hash where the channel shows one
  (the §4.6 version unit; see the addendum's Version & Update Integrity)

// 5d Before:
- **Code signing status**: Signed (by whom), notarized (macOS), or unsigned
// 5d After:
- **Code signing status**: Signed (signer: Team ID / certificate subject /
  key fingerprint), notarized (macOS), or unsigned — plus the vendor's
  expected identity and where it is documented
- **Store package kind** (Microsoft Store): MSIX AppContainer, MSIX full
  trust, or unpackaged Win32 (MSI/EXE); unknown → treat as unpackaged

// 5e Before:
well-known package manager, code signed, known publisher, available >= 1
year, no incidents, low-risk installer type.
// 5e After:
well-known package manager, code signed with the identity verified
(`references/criteria.md` §4.6 V2), known publisher, available >= 1 year,
no incidents, low-risk installer type — and §4.6 leaves Tier 1 available
for this version.

// 5f Before:
Quick audit scope: confirm distribution channel + code signing status,
verify publisher identity, check for incidents.
// 5f After:
Quick audit scope: confirm distribution channel + signer identity against
the vendor's documented identity (channel binding suffices; see the
addendum's V2), check for incidents.

// 5g Before:
Any Tier 3 trigger from the addendum: unsigned, unknown source, third-party
mirror, EXE installer without signing, shared via chat, recent acquisition,
prior removal, admin privilege request, bundleware reports.
// 5g After:
Any Tier 3 trigger from the addendum: unsigned or not notarized, unknown
source, third-party mirror, EXE installer without signing, shared via chat,
recent acquisition, signer change, Gatekeeper/SmartScreen bypass
instructions, prior removal, admin privilege request, bundleware reports.

// 5h Before:
2. **Is the app code-signed?** What type of signing (Authenticode EV/
   standard, Apple Developer ID + notarization, distro GPG, vendor GPG)?
   Cross-reference against the code signing standards in
   `references/criteria/desktop-app.md`.
// 5h After:
2. **Is the app code-signed, and by whom?** Signing type (Authenticode
   EV/OV, Artifact Signing, Apple Developer ID + notarization, distro or
   vendor GPG) and the signer it names. Does the signer match the
   vendor's documented or prior-release identity, and is the signature
   still valid (not revoked)? Cross-reference the code signing standards
   and the V2 plug-in in `references/criteria/desktop-app.md`.

// 5i Before:
5. **Does the app run sandboxed?** App Sandbox (macOS App Store), MSIX
   container, Flatpak sandbox, Snap strict confinement, or unsandboxed?
// 5i After:
5. **Does the app run sandboxed?** App Sandbox (Mac App Store), MSIX
   AppContainer (full-trust MSIX is not sandboxed), Flatpak sandbox, Snap
   strict confinement, or unsandboxed?

// 5j Before:
7. **How does the app update?** Store-managed, signed auto-updater, vendor-
   hosted updater, manual download, or no updates?
// 5j After:
7. **How does the app update?** Store-managed, signed auto-updater (which
   framework and version?), vendor-hosted updater, manual download, or no
   updates? Does the updater verify signatures?

// 5k Before:
- Store listing (MS Store / Mac App Store apps are signed by definition)
- Package manager metadata (Homebrew cask checksums, winget manifests,
  Chocolatey verification)
// 5k After:
- Store listing: Mac App Store and Microsoft Store MSIX packages are
  store-signed; Microsoft Store unpackaged Win32 installers are signed by
  the publisher and fetched from the publisher's URL — verify that signer
  as for a direct download
- Package manager metadata (Homebrew cask `url` + checksum, winget
  manifest `Publisher` + `InstallerUrl`, Chocolatey verification). A
  checksum proves the file matches the manifest, not who built it

// 5l Before:
- Vendor documentation or security page
// 5l After:
- Vendor documentation or security page (source of the expected
  identity: Team ID, certificate subject, key fingerprint)
- When the file is at hand: the addendum's V2 commands (`codesign`,
  `spctl`, `pkgutil`, `Get-AuthenticodeSignature`); otherwise list them
  in the Post-Install Checklist as a before-first-launch step

// 5m Before:
- For EXE installers: is the installer framework known (NSIS, Inno Setup,
  WiX)? Does it bundle third-party software (toolbars, adware)?
// 5m After:
- For EXE installers: is the installer framework known (NSIS, Inno Setup,
  WiX)? Is it signed by the matched publisher? Does it bundle third-party
  software (toolbars, adware)?

// 5n Before:
| CVE / advisories | Required | Required | Required |
// 5n After:
| CVE / advisories | Required | Required | Required |
| Version integrity (§4.6) | Required | Required | Required |

// 5o Before:
| OpenSSF Scorecard | Optional | If repo known | Required |
// 5o After:
| OpenSSF Scorecard | Optional | Required (N/A if no public repo) | Required |
| Impersonation / name verification | Required | Required | Required |
| License compatibility | Required | Required | Required |
| Maintainer / activity / health | Brief | Required | Required |
| Bundled runtimes / dependencies | Tier-skip | Required | Required |

Canonical row names (`references/criteria.md` Audit Coverage): Registry /
metadata lookup = Distribution channel verification; Typosquat / name
verification = Impersonation / name verification; Install script review =
Installer type assessment; Permissions / least privilege = Sandboxing
evaluation + Privilege escalation assessment; Dependency tree = Bundled
runtimes / dependencies. Either name may label the report row.

// 5p Before:
- **Code signing certificate chain**: Who issued the certificate? Is it
  EV or standard (Windows)? Is it notarized (macOS)? Is it a distro
  maintainer key (Linux)?
// 5p After:
- **Signer identity**: Who signed (Team ID, certificate subject, key
  fingerprint), and does it match the vendor's documented or prior-release
  identity (`references/criteria.md` §4.6 V2)? EV, OV or Artifact Signing
  (Windows)? Notarized (macOS)? Distro maintainer key (Linux)?

// 5q Before:
- **CVEs**: Check NVD, GHSA, and vendor security advisories for the app
  name and version.
// 5q After:
- **CVEs**: Check NVD, GHSA, and vendor security advisories for the app
  version and its bundled runtimes (Electron/Chromium, Qt, Java, .NET).
  Rate per the addendum's CVE Scope (§4.3) and `SKILL.md` Blocking CVE.

// 5r Before:
- **Supply-chain incidents**: Has the vendor's signing key been
  compromised? Has the update mechanism been hijacked?
// 5r After:
- **Supply-chain incidents**: Has the vendor's signing key been
  compromised? Has the update mechanism been hijacked? Scope any hit by
  version or update window per `references/criteria.md` §4.6 V4.

// 5s Before:
- **Sandboxing**: Is the app sandboxed (App Sandbox, MSIX, Flatpak, Snap
  strict)? If not, note as an unrestricted-privilege data point.
// 5s After:
- **Sandboxing**: Is the app sandboxed (App Sandbox, MSIX AppContainer,
  Flatpak, Snap strict)? Full-trust MSIX and Snap classic are not. If not
  sandboxed, note as an unrestricted-privilege data point.

// 5t Before:
- **Auto-update reliability**: Does the auto-updater work without admin
  privileges? Does it verify update signatures?
// 5t After:
- **Auto-update reliability**: Does the auto-updater work without admin
  privileges? Does it verify update signatures, and is its framework
  version free of known signature-bypass advisories?

// 5u Before:
### 4.6 Alternatives (desktop-app-specialized)
// 5u After:
### Alternatives (desktop-app-specialized)

// 5v Before:
- **Unsigned binary from unknown source**: no code signing, no store
  listing, no verifiable publisher identity
// 5v After:
- **Unsigned or unmatched binary from unknown source**: no code signing,
  or a signature (even notarized) whose identity cannot be tied to the
  vendor; no store listing; no verifiable publisher identity

// 5w Before:
- **Recent acquisition + privilege escalation**: app acquired by new
  entity and simultaneously added elevated-privilege requirements
// 5w After:
- **Recent acquisition + privilege escalation**: app acquired by new
  entity and simultaneously added elevated-privilege requirements
- **Gatekeeper / SmartScreen bypass lure**: install instructions from a
  source whose identity does not verify tell the user to override OS
  protection (`xattr -d com.apple.quarantine`, "Open Anyway", a Terminal
  command "to verify", SmartScreen "Run anyway") — CRITICAL
- **Revoked signer or notarization**: the signature no longer validates
  because Apple or the CA revoked it — CRITICAL unless the vendor
  documents the revocation and ships a re-signed build
- **Compromised release or update channel**: the version or update path
  the user would get falls in a confirmed compromise's affected range or
  window (`references/criteria.md` §4.6 V4 case a)

// 5x Before:
- **EXE installer from known vendor**: Condition: verify installer is
  signed; check for bundleware; prefer MSI/MSIX if available
// 5x After:
- **EXE installer, signer not matched**: unsigned, or signed by someone
  other than the vendor's documented publisher. Condition: obtain a build
  whose signer matches; check for bundleware; prefer MSI/MSIX if
  available. A signed EXE whose signer matches the vendor (winget or
  vendor site) is a note, not a condition
- **macOS app not notarized**: HIGH flag. Condition: use a notarized
  build, the Mac App Store version or an official cask; never bypass
  Gatekeeper
- **Update channel without verified signatures** (unsigned vendor
  updater, or an updater version with a known bypass advisory): HIGH
  flag. Condition: turn off in-app auto-update and update through a
  verified channel

// 5y Before:
- **Direct download when store version exists**: Condition: prefer the
  store version for sandboxing and update guarantees
// 5y After:
- **Direct download when a sandboxed store version exists** (Mac App
  Store, Microsoft Store MSIX AppContainer): Condition: prefer the store
  version for sandboxing and update guarantees

// 5z Before:
- Code signed (Authenticode, Apple Developer ID + notarization, distro GPG)
// 5z After:
- Code signed, signer identity verified per `references/criteria.md`
  §4.6 V2 (Authenticode subject, Team ID + notarization, distro GPG)

// 5aa Before:
- Sandboxed if distributed via store (bonus for non-store)
// 5aa After:
- Sandboxed if the store package is sandboxed (Mac App Store, MSIX
  AppContainer); bonus for non-store

// 5ab Before:
- Healthy maintenance signals (recent updates, active development)
// 5ab After:
- Healthy maintenance signals (recent updates, active development)
- `references/criteria.md` §4.6 raises no flag for this version
```

**Rationale:**
- **5u.** The workflow's `### 4.1`–`### 4.5` mirror `criteria.md` §4.1–§4.5. A `### 4.6 Alternatives` next to `criteria.md` §4.6 *Version & Update Integrity* would make "§4.6" ambiguous in every reference this plan adds. Dropping the number is the smallest change; no file references the old heading (grep at planning).
- **5o.** Complies with the floor's row contract (workflow tables add rows, never drop a Required row), and maps names instead of renaming existing rows that auditors already use.
- **5v.** The MacSync shape (notarized, unknown vendor) previously matched no REJECTED bullet.

**Verification:** `grep -c "### 4.6" workflows/desktop-app.md` → 0; `grep -c "Version integrity (§4.6)" workflows/desktop-app.md` → 1; `grep -ci "signed by definition\|EXE installer from known vendor\|GitHub stars on" workflows/desktop-app.md` → 0.

**If this fails:** `git -C <work-root> checkout -- workflows/desktop-app.md` and redo Step 5.

---

## Verification Plan

### Automated Checks

- [ ] `python3 evals/run_evals.py validate` passes; unittest count = P0.
- [ ] Consistency script (run from `<work-root>`; not committed):

```bash
python3 - <<'EOF'
import re, pathlib
A = pathlib.Path("references/criteria/desktop-app.md").read_text(encoding="utf-8")
W = pathlib.Path("workflows/desktop-app.md").read_text(encoding="utf-8")
C = pathlib.Path("references/criteria.md").read_text(encoding="utf-8")
heads = set(re.findall(r"^### (V[1-5]) ", C, re.M)); assert heads == {"V1","V2","V3","V4","V5"}, heads
for name, t in (("addendum", A), ("workflow", W)):
    for v in re.findall(r"§4\.6 (V\d)", t): assert v in heads, (name, v)
    low = t.lower()
    for bad in ["smartscreen reputation immediate", "gatekeeper allows with warning", "no signing gate",
                "msix apps run in container", "signed by definition", "unsigned update channel = medium",
                "github stars on", "exe installer from known vendor", "apple checks for malware",
                "hardware token required", "### 4.6 alternatives"]:
        assert bad not in low, (name, bad)
assert A.count("\n## Version & Update Integrity (§4.6)\n") == 1 and A.count("\n## CVE Scope (§4.3)\n") == 1
assert [len(re.findall(rf"^- \*\*V{i} ", A, re.M)) for i in range(1, 6)] == [1]*5
cve = A.split("## CVE Scope (§4.3)")[1].split("## Version & Update Integrity")[0]; assert "REJECTED" not in cve
assert "| High | Persistent attack surface" in A and re.search(r"HIGH\s+flag\. Condition: turn off", W)
assert "| Version integrity (§4.6) | Required | Required | Required |" in W
assert W.count("Canonical row names") == 1 and "**Curated pipelines:** none" in A
print("OK")
EOF
```

- [ ] `git -C <work-root> diff --stat <base>..HEAD` → only the 2 files (+ execution log).

### Manual Verification (paper traces)

Walk each through `SKILL.md` Step N + addendum + §4.6; log the rule cited per hop.

| # | Case | Expected |
|---|---|---|
| P1 | eval 18: `winget install Mozilla.Firefox` | winget moderate+. V2 channel binding: manifest Publisher Mozilla + Mozilla URL (A3). NSIS EXE → Tier 1 barred by installer type → Tier 2. Matched signed EXE = note (3d/5x). Firefox updater verifies → no flag. **APPROVED** (V1 < 72 h on release days → CONDITIONAL; eval-plan hand-off) |
| P2 | eval 19: "VLC Pro" `.exe` from free-software-downloads.xyz via forum | mirror strong negative; signer unmatched/unsigned; Tier 3 → Toward REJECTED (5v + mirror) → **REJECTED** |
| P3 | eval 29: OBS official installer vs MS Store | official: signed, vendor domain; Store: package kind unknown → unpackaged → vendor-download scoring; neither sandboxed → **APPROVED or CONDITIONAL** ✓ |
| P4 | MacSync shape: notarized DMG from unknown site, Team ID tied to no vendor | V2 no match → no credit; Tier 3; 5v fires → **REJECTED** |
| P5 | Known OSS vendor, Developer ID only, README says `xattr -cr` | HIGH `not notarized`; vendor matched → no lure CRITICAL; report doesn't repeat bypass → **CONDITIONAL**. Same instructions from an unknown site → CRITICAL → **REJECTED** |
| P6 | MS Store unpackaged Win32 app, known vendor | scored as vendor download; Tier 1 barred (4b) → Tier 2 → APPROVED reachable only on file/channel identity match |
| P7 | `brew install --cask acme/tap/tool`, tap not documented by vendor | repackager → strong negative → Tier 3; documented by vendor → vendor-direct scoring |
| P8 | Windows app with unsigned vendor updater (Notepad++ < 8.8.9 shape) | HIGH (3j/3k) → **CONDITIONAL**, condition: disable in-app updates |
| P9 | Electron app: bundled Chromium HIGH (not KEV) fixed upstream, not yet in app release | CVE Scope: third-party → §4.3 HIGH flag → **CONDITIONAL** (fixed release = next app release). Same but KEV CRITICAL → §4.3 → REJECTED (class from §4.3, not addendum) |
| P10 | New build: Authenticode thumbprint + issuer changed (Artifact Signing migration), same subject | V3 note only; subject changed → V3 HIGH → ≥ CONDITIONAL |

### Acceptance Criteria Validation

| Criterion | How to Verify | Expected Result |
|---|---|---|
| Plug-ins present (V1–V5, CVE Scope) | consistency script | `OK` |
| §4.6 refs resolve | consistency script | `OK` |
| Stale phrases gone | consistency script | `OK` |
| Updater severity single | consistency script + Step 3 grep | HIGH everywhere |
| Coverage rows | consistency script | `OK` |
| C6 classes untouched | consistency script (no REJECTED in CVE Scope) | `OK` |
| Harness | validate + unittest | pass; same count |
| Traces | execution log P1–P10 | match table |
| Diff scope | `git diff --stat` | 2 files |

---

## Rollback Plan

1. Before close: `projex-abandon.sh <repo-root> claude/youthful-dijkstra-5ov1kt projex/2610162006-desktop-app-rubric-refresh --worktree`; base untouched.
2. After squash-close: `git -C <repo-root> revert <squash-sha>` (touches only the 2 files; nothing else depends on them except the eval plan's future desktop cases).

---

## Notes

### Eval hand-off (for the eval-refresh plan; `evals/` not edited here)

- **Eval 18 (Firefox winget):** the expected_output says "Tier 1 quick audit". With an NSIS EXE (A3) the addendum's installer-type rule bars Tier 1 → Tier 2. Only the description is affected; exact APPROVED stays reachable, made easier by D8. V1 time-dependence is already in the floor hand-off.
- **Eval 29 (OBS):** the expected_output assumes the MS Store version "may have sandbox restrictions … signed and reviewed". The package kind is unverified; if it is unpackaged Win32 or full-trust MSIX, that wording is wrong. Verdict assertion unaffected.
- **New cases:** P4 (notarized, unmatched identity → REJECTED) | P5 (non-notarized + `xattr` from known vendor → CONDITIONAL; from unknown site → REJECTED) | P6 (MS Store unpackaged → not Tier 1) | P7 (third-party cask tap) | P8 (unsigned updater → CONDITIONAL) | P10 (cert rotation ≠ V3 flag).

### Cross-cutting (orchestrator)

- **`### 4.6` heading collisions** remain in `workflows/registry-package.md` (L410), `browser-extension.md` (L302), `cli-binary.md` (L223 `§4.6 Alternatives & Ecosystem Fit`), `ide-plugin.md` (L295), `ci-action.md` (L188), `container-image.md` (L264 `4.6 Supply Chain`), `agent-extension.md` (L193 `§4.6 Maintenance & Ecosystem`) and `remote-integration.md` (L137 `§4.6 Integration Hygiene`). Each owning plan should drop the number or renumber. This plan fixes desktop only.
- **§4.3 plug-in heading:** the floor fixes the §4.6 plug-in heading but not the §4.3 one. This plan uses `## CVE Scope (§4.3)`, as do most sibling plans. 2610162006-cli-binary-rubric-refresh-plan.md uses `## Own Code vs Third-Party Components (§4.3)`; align one way before execution.
- **Classifier (cli-binary / classifier owner):** `brew install <name>` without `--cask` also installs a cask when no formula of that name exists (Homebrew behavior from memory; not re-verified). `references/classifier.md` routes bare `brew install` to cli-binary.
- **STEWARDSHIP.md** desktop trigger text could add "store packaging policy, Gatekeeper/notarization, CA/B code-signing ballots".

### Risks

- **More CONDITIONAL verdicts** (non-notarized macOS, unsigned updaters). Mitigation: both conditions are actionable; this is intended per D1/D6.
- **Channel binding read as presence.** Mitigation: it requires the publisher name and the URL domain to match the vendor's documentation, and the file-level check still lands in Post-Install.
- **Dated examples rot** (MacSync, Notepad++, CVE-2026-34078, electron-updater). Mitigation: each carries a year and sits in Trust Notes or examples, never in a threshold.
- **Commands unverified on current macOS (A2).** Mitigation: they appear as checks whose output the auditor compares, not as verdict gates. A failing command → `Not available` + note, not a flag.

### Open Questions

None. Unverified facts are recorded as A2–A5 and hedged in text. The C6 classes come from §4.3, not this plan.

### Split Decision

`No split — single scope, within size budget`. The plan is ~63 KB, but the size heuristic needs both size and > 5 steps, and there are 5. One `.projex/` scope; 2 coupled files (Step 5 names the rows Steps 1–4 create). Most of the bulk is verbatim After text, which an executor needs anyway.

### Sources (verified 2026-10-16)

Microsoft Learn code-signing options + SmartScreen reputation (EV change 2024) | Microsoft Learn Win32-in-Store + packaged-app integrity docs | Jamf Threat Labs MacSync post (Team ID, revocation) | Cult of Mac / The Hacker News 2024-08 (Sequoia Gatekeeper) | Notepad++ v8.8.9 release notice + Help Net Security 2026-02 | OSV GHSA-9jxc-qjr9-vjxq (CVE-2024-39698) | CVE-2026-34078 record (Flatpak < 1.16.4) | Microsoft Learn Artifact Signing FAQ + DevClass 2026-01 (lifetime conflicts: 3 d vs 24 h) | SSL.com / DigiCert CSC-31 posts (460 d) | brew.sh 5.0.0 + Homebrew cask issues (TomatoBar, CopyQ) | Flathub About page (verified ✓) | Snapcraft forum 2024-03 (new-name review) | Canonical blog (`snap refresh --hold`) | flatpak-mask man page.
