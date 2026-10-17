# CLI Binary — Criteria Addendum

Per-subject scoring extensions for **Type 7: cli-binary** audits.
Layers on top of `references/criteria.md`. More-specific guidance wins,
except over the §4.6 version-integrity floor and the §4.3 Blocking CVE
classes: this file only tightens or fills those.

Covers: GitHub Releases binaries, vendor-hosted executables, Homebrew
formulae (homebrew/core and third-party taps), language-version and
toolchain managers (nvm, pyenv, rustup, mise, fnm, uv), install
scripts (curl-pipe-bash), and GoReleaser-built releases.
Cross-platform: Windows, macOS, Linux. Homebrew casks are desktop-app.

Platform facts below are as of 2026-10; re-check them at each
stewardship review.

## Distribution Channel Trust Signals

| Channel | Verification Gate | Adoption Metric | Trust Notes |
|---------|-------------------|-----------------|-------------|
| Homebrew core formula (name resolves to tap `homebrew/core`) | Every formula change is a PR reviewed and merged by a Homebrew maintainer; source `sha256` pinned in the reviewed formula; bottles built from source by Homebrew CI and attested | Install count via `brew` analytics | Trust anchor = Homebrew review + Homebrew CI build, not an upstream-uploaded binary. Formula installs never use `sudo`. Curated pipeline for §4.6 V2 (§ Version & Update Integrity) |
| Homebrew third-party tap (`brew install <user>/<tap>/<name>`, or `brew tap <user>/<tap>` then the short name) | None from Homebrew: the tap is its owner's GitHub repo, its Ruby runs with the user's privileges when loaded, and Homebrew calls third-party taps unsupported. Since Homebrew 6.0.0 untrusted taps are not loaded until trusted (`brew trust`; a fully qualified install trusts that one item) | Tap repo stars | Trust = the tap owner. Tap named in the upstream project's own docs → rate as that vendor's GitHub Releases / vendor-hosted channel. Any other tap → third-party repackager. `brew trust` records consent, not review |
| GitHub Releases (org-owned, CI-built) | CI-built assets; checksum file; signature or attestation | Download count per asset | Highest GitHub trust once identity verifies per §4.6 V2 (the project's repo + release workflow). Immutable release = assets and tag cannot change after publish |
| GitHub Releases (personal, manual) | Author-uploaded assets; no CI provenance | Download count per asset | Lower trust — single author, no build reproducibility guarantee |
| GoReleaser / release automation | CI-built; `checksums.txt` auto-generated; optional Sigstore signing | Download count | Standard checksum file; signing optional — credit only verified identity |
| Vendor-hosted binary (signed) | Vendor website + GPG/Sigstore/Minisign signature | Website traffic / brand | Trust = vendor identity + a signature that verifies against the vendor-documented key or identity |
| Vendor-hosted binary (unsigned) | Vendor website only; no signature | Website traffic / brand | Trust depends entirely on vendor identity; no cryptographic verification |
| Language-version / toolchain manager (rustup, nvm, pyenv, mise, fnm, uv) | Project-maintained installer (e.g. rustup: Rust project; nvm: OpenJS Foundation project) | GitHub stars + community adoption | Governance is a maintenance signal, not install-time verification: rate the installer as an install script (§ Install Script Risk) and by §4.6 V2. Check maintenance status — Volta's maintainers declared it unmaintained (README, Nov 2025) and recommend mise |
| Install script (curl-pipe-bash) — known vendor | Script URL listed in the vendor's own docs or repo README | Script content auditable | Pipe-to-shell bypasses verification, and a server can send different bytes to `curl \| sh` than to a browser. Mitigated only by a URL traced to vendor docs + the executed-bytes rule (§ Install Script Risk) |
| Install script (curl-pipe-bash) — unknown source | Unknown or unverified source | None | Highest risk: arbitrary code execution, no verification, no rollback |
| Third-party mirror / repackager / shared copy (file host, network share, chat attachment) | Non-vendor distribution | None | Unverified bytes = highest risk. Bytes whose SHA-256 matches the vendor's **signed** checksum file for that exact version (signature verified per §4.6 V2) → channel risk drops to a note |

### Scoring impact

- Homebrew core formula = strong positive (maintainer review + Homebrew CI build + pinned checksum); counts as verified identity for Tier 1 via the curated pipeline (§ Version & Update Integrity, V2)
- Homebrew third-party tap = no Homebrew credit; score as the tap owner's channel (vendor-documented tap → vendor channel; otherwise third-party repackager)
- GitHub Releases org/CI-built with checksums and identity verified (§4.6 V2) = strong positive; immutable release = additional positive
- GitHub Releases org/CI-built with checksums, identity not verifiable = moderate positive
- GoReleaser with checksums.txt = moderate positive; strong only with verified identity
- Language-version / toolchain manager (maintained, established) = moderate positive; declared unmaintained = Abandoned (`references/criteria.md` §4.2 → CONDITIONAL)
- Vendor-hosted with signature verified against the vendor-documented key or identity = moderate positive
- GitHub Releases personal/manual with checksums = moderate positive
- Vendor-hosted unsigned = weak positive at best (vendor reputation only)
- curl-pipe-bash from known vendor, URL traced to vendor docs = LOW-MEDIUM flag (pipe-to-shell risk, mitigated by vendor)
- curl-pipe-bash from unknown source, or URL not traceable to vendor docs = HIGH flag
- Install-command lure (§ Install Script Risk) = CRITICAL; lookalike vendor domain = `SKILL.md` Red Flag "Confirmed typosquat / impersonation"
- Third-party mirror / shared copy, bytes unverified = strong negative; bytes verified against the vendor's signed checksum = note only

## Signature & Checksum Standards

Credit a signature or attestation only when it verifies **and** names the expected identity (§4.6 V2; § Version & Update Integrity says where that identity comes from). `<owner>/<repo>` below = the repo the vendor documents as the source.

| Method | Strength | Verification |
|--------|----------|--------------|
| GitHub release attestation (immutable release) | Strong | `gh release verify <tag> -R <owner>/<repo>`, then `gh release verify-asset <tag> <file> -R <owner>/<repo>`. Covers only releases published while immutability was enabled; source zip/tarball not covered. `gh release view <tag> -R <owner>/<repo> --json isImmutable` shows the state |
| GitHub artifact attestation (`actions/attest`) | Strong | `gh attestation verify <file> --repo <owner>/<repo>`; add `--signer-workflow <owner>/<repo>/.github/workflows/<file>` when the vendor documents its release workflow (for a reusable workflow, `--signer-workflow` or `--signer-repo` is required) |
| Sigstore bundle / cosign keyless | Strong | `cosign verify-blob --bundle <bundle> --certificate-identity <identity> --certificate-oidc-issuer <issuer> <file>`. For GitHub Actions signing: identity = `https://github.com/<owner>/<repo>/.github/workflows/<file>@refs/tags/<tag>`, issuer = `https://token.actions.githubusercontent.com`. A transparency-log (Rekor) entry alone only shows that *someone* signed |
| SLSA provenance attestation | Strong | `slsa-verifier verify-artifact <file> --provenance-path <provenance> --source-uri github.com/<owner>/<repo>` (add `--source-tag <tag>`) |
| Homebrew bottle attestation | Strong | Homebrew checks bottles against the `Homebrew/homebrew-core` CI identity only when `HOMEBREW_VERIFY_ATTESTATIONS` is set (needs `gh`; opt-in as of 2026-10). Third-party tap bottles verify only against the tap's own repo |
| GPG detached signature (.asc/.sig) | Strong | Verify with the vendor's key; match its fingerprint against vendor docs reached on a channel other than the download server |
| Minisign | Strong | Ed25519; verify with the public key the vendor publishes in its docs or repo, not only beside the binary |
| Signed checksum file (e.g. `SHA256SUMS` + `.sig`) | Strong | Verify the checksum file's signature per its method's row, then the binary's hash against it |
| SHA-256 checksum file | Moderate | Integrity check only (no authenticity); depends on checksum file's own provenance |
| SHA-512 checksum file | Moderate | Same as SHA-256 with larger hash; same provenance caveat |
| MD5 checksum | Weak | Collision-vulnerable; legacy only; treat as absent if no SHA-256+ alternative |
| No checksum or signature | Absent | No verification possible; binary provenance unknowable |

Run `gh`, `cosign`, `slsa-verifier`, `gpg` and `minisign` under the audit-tooling note in `references/criteria.md`. If you cannot run a check, record `Not available (<why>)` and give no identity credit.

### Scoring impact

- Signature/attestation verified against the expected identity + checksum = strong positive (origin, not safety: never enough alone for APPROVED or Tier 1)
- Verified SLSA provenance or GitHub artifact/release attestation = strong positive
- Signature/attestation present but unverified, or identity not matched = note only, no credit
- Identity names a different repo, workflow, key or signer than vendor docs or the previous release = HIGH flag (§4.6 V3)
- Signed checksum file verified = strong positive
- SHA-256/SHA-512 checksum only (served over HTTPS from same origin) = moderate positive
- Checksum hosted separately from binary (different domain/channel) = stronger than co-hosted
- MD5 only = weak positive (note collision vulnerability)
- No checksum or signature = MEDIUM-HIGH flag (no verification path)

## Install Script Risk Classification

| Pattern | Risk | Guidance |
|---------|------|---------|
| `curl -sSL <url> \| sh` (or `bash`) | High | Arbitrary code execution; no verification before execution; MITM risk if not HTTPS; the bytes piped can differ from what a browser shows |
| `curl -sSL <url> \| sudo sh` | Critical | Same as above + root privileges; any compromise has full system access |
| `wget -qO- <url> \| sh` | High | Same risk profile as curl-pipe-sh |
| PowerShell `irm <url> \| iex`, `iwr <url> \| iex`, `iex (irm <url>)`, `iex ((New-Object Net.WebClient).DownloadString('<url>'))` | High | PowerShell pipe-to-shell: same risk profile as curl-pipe-sh; in an elevated (Administrator) session = Critical |
| Download script → inspect → execute **that same file** | Medium | User can audit before running; risk is in the auditing quality |
| Script pinned to a commit (raw URL at a commit SHA) or with a vendor-published checksum/signature | Medium-Low | The audited bytes are the executed bytes |
| Installer binary (self-extracting) | Medium | Opaque; runs arbitrary code; better than pipe-to-shell only because it can be scanned |
| Package manager install (homebrew/core, distro repos) | Low | Package manager mediates: maintainer review, pinned checksum, sandboxing (if any). A third-party Homebrew tap is not mediation (§ Distribution Channel) |
| Build from source | Low | User controls compilation; risk is in the build system (Makefile, cargo, go build) |

**Install-URL provenance.** The exact command and URL must appear in the vendor's own docs or repo README, reached directly. A copy from an ad, sponsored search result, forum, chat or AI answer doesn't count until it matches. A URL that hides the publisher (shortener, redirector, paste site, raw IP) or uses plain HTTP is an unverifiable source: expand a shortener only to report where it points, never to run it. Lookalike of the vendor domain → `SKILL.md` Red Flag "Confirmed typosquat / impersonation".

**Lure patterns (CRITICAL → Toward REJECTED).** The command reached the user via an ad or sponsored result, or a page presents it as a step to paste into Terminal / PowerShell / the Run dialog to "verify you are human", fix an error or unlock content, **and** it is not the vendor's documented install command.

**Executed-bytes rule.** Audit and run the same bytes:
1. Download the script to a file (`curl -fsSLo install.sh <url>`; PowerShell: `Invoke-WebRequest <url> -OutFile install.ps1`).
2. Read that file and record its SHA-256 (`sha256sum` / `Get-FileHash`) in the Version integrity row.
3. If approved, run that file (`sh ./install.sh` / `& .\install.ps1`), never a fresh `curl | sh` or `irm | iex`.
4. Apply the binary rules to anything the script downloads: does it pin a version and check a checksum or signature?

### Scoring impact

- `curl … | sudo sh` from unknown source = automatic Tier 3, push toward REJECTED
- `curl … | sh` from known vendor = Tier 3 (Tier 3 trigger: pipe-to-shell from any source), note pipe-to-shell risk; condition or recommendation = executed-bytes rule
- Install-command lure = CRITICAL
- Pipe-to-shell (any shell, incl. PowerShell `iex`) from a URL that hides the publisher or uses plain HTTP = CRITICAL
- `irm … | iex` from known vendor, URL traced to vendor docs = same as `curl … | sh` from known vendor
- Script fetches and runs further remote code with no checksum or signature check = HIGH flag
- Download-then-inspect = moderate (depends on script complexity)
- Build from source available = positive signal (verifiable, auditable)
- Package manager mediation (homebrew/core, distro repos) = positive signal (review layer)

## Provenance Assessment

Assess binary provenance via these signals:

| Signal | Positive indicator | Negative indicator |
|--------|-------------------|-------------------|
| Build system | CI-built (GitHub Actions, etc.) with public workflow | Manual build, no CI, no build config in repo |
| Reproducible builds | Documented build process; deterministic output | "Trust me" binary with no build info |
| Source availability | Open-source repo with matching release tags | Closed-source, no repo, no tag correspondence |
| Release process | Tagged release → CI builds → signed/attested artifacts → checksum file; immutable release | Manual upload of pre-built binary; release author switches between CI and a human (§4.6 V3) |
| SLSA level | SLSA L2+ provenance verified against the project repo | No SLSA attestation |
| Release frequency | Regular releases with changelogs | Sporadic or abandoned releases; release with no matching tag or changelog (§4.6 V3) |

### Scoring impact

- CI-built + open-source + tagged release + identity verified = strongest provenance
- Open-source + manual release + checksum = moderate provenance
- Closed-source + vendor-hosted + signed (identity verified) = moderate provenance (vendor trust)
- No source + no CI + no signature = weakest provenance, strong negative

## Tier Thresholds (CLI Binaries)

### Tier 1 — Quick Audit

ALL of these must hold:
- Distributed via Homebrew core formula (tap `homebrew/core`; never a third-party tap) OR GitHub Releases from a well-known org/project
- Identity verified per §4.6 V2: checksum AND a signature or attestation matched to the expected identity, or the homebrew/core curated pipeline (§ Version & Update Integrity)
- Project is established (>= 1 year old, >= 1K GitHub stars or equivalent adoption)
- Maintained: release within last 12 months
- No known security incidents or supply-chain compromises (a resolved past compromise also bars Tier 1: §4.6 V4 case c)
- `references/criteria.md` §4.6 raises nothing that bars Tier 1 (publish time known and >= 7 days; no V3 item)
- No install-script-only distribution (binary download available)

### Tier 2 — Standard Audit (default)

Default when not all Tier 1 criteria are met:
- Distributed via a recognizable channel (GitHub Releases, vendor site, Homebrew core, or a Homebrew tap the vendor documents)
- Checksum available (signature not required)
- Identifiable author or organization
- No unresolved security incidents
- Project available > 30 days

### Tier 3 — Deep Audit

ANY of these triggers:
- Install via `curl … | sh`, `curl … | sudo sh` or PowerShell `irm … | iex` (any variant) from any source
- No checksum and no signature for binary download
- Binary from unknown or unverifiable source
- Third-party mirror or repackager (not original author/org), incl. a Homebrew tap the upstream project does not document
- Shared via chat/email/forum link (not discovered via official channel)
- Install command reached via ad, sponsored result or a paste-to-verify page (§ Install Script Risk)
- Single-author project with no CI and no release automation
- First release < 30 days old (project age; version age is §4.6 V1)
- Known prior security incident or supply-chain compromise
- Identity evidence differs from vendor docs or the previous release (§4.6 V3)
- Binary requests elevated privileges (sudo/admin) with unclear justification

## CVE Scope (§4.3)

Plug-in for `references/criteria.md` §4.3. The verdict classes stay as defined there and in `SKILL.md` "Blocking CVE".

- **Own code:** the project's own source as shipped in the binary (incl. forks it maintains) and the project's install script.
- **Third-party component:** statically linked or vendored libraries (Go modules, Rust crates, bundled C libraries), bundled runtimes or interpreters, and Homebrew dependency formulae.
- **Fixed release:** for a third-party component, a release of this binary (or an update of the Homebrew dependency formula) that ships the fixed component. An upstream library fix that no binary release ships yet is not a fixed release of the subject.
- **Third-party component, no fixed release (not KEV):** HIGH flag per `references/criteria.md` §4.3. Condition: avoid the affected feature or input the advisory names; run without sudo / Administrator; no network-exposed or long-running use of the affected path; pin the audited release; re-audit when a binary release ships the fix. A scanner's "not called" reachability result supports the condition as a note, not as VEX.
- **Scan sources:** OSV / GHSA for the repo and for the dependency versions in its `go.mod` / `Cargo.lock` at the release tag; vendor advisories. Where available, scanners that read a binary's embedded dependency metadata (`govulncheck -mode=binary <file>` for Go; `cargo audit bin <file>` for Rust binaries built with `cargo auditable`). The audit-tooling note in `references/criteria.md` applies.
- **VEX sources:** only the project's own VEX documents or advisory statements that name the version. Reachability output from a scanner you run (e.g. govulncheck reporting a vulnerable symbol as not called) is a note, not VEX evidence.

## Version & Update Integrity (§4.6)

Plug-ins for `references/criteria.md` §4.6. Shared rules and thresholds apply unchanged; these bullets only fill them.

- **V1** — *Publish time:* GitHub Releases → `publishedAt` (`gh release view <tag> -R <owner>/<repo> --json publishedAt`); Homebrew core → the upstream release date of the formula's version (Homebrew's review delay does not count toward V1); vendor-hosted → release notes or changelog date; install script → the release the script installs today. None found → `Not available`. *Version unit:* release tag + asset SHA-256; for an install script, script SHA-256 + the binary version it resolves to; a Homebrew core `revision` or bottle `rebuild` bump with unchanged source `url` and `sha256` is the same version (a Homebrew CI rebuild of an unchanged upstream release); a new upstream version is always a new version. *Condition wording:* these channels have no client cooldown setting, so name the previous release to install (exact tag asset, or a versioned formula `<name>@<version>` where Homebrew has one) or the date the version turns 72 h old.
- **V2** — *Mechanisms and commands:* § Signature & Checksum Standards. *Expected identity:* the repo, release workflow, key fingerprint or tap named in the vendor's own install/verification docs or README; else the identity the previous release carried. Record it and its source in the Version integrity row. *Absence:* the existing scoring stands (checksum only = moderate; no checksum or signature = MEDIUM-HIGH flag); absence where prior releases carried identity evidence is V3. *Curated pipeline — Homebrew core:* counts as verified for the Tier 1 identity requirement when (1) the name resolves to tap `homebrew/core` (`brew info <name>` prints a `From:` URL under `Homebrew/homebrew-core`; a `<user>/<tap>/<name>` install never qualifies) and (2) the formula's `url` points at the upstream project's documented source or release location. If `gh` is available, also verify the bottle attestation (`HOMEBREW_VERIFY_ATTESTATIONS=1`, identity `Homebrew/homebrew-core`); a failed verification is a V3 HIGH flag. Third-party taps are never curated pipelines.
- **V3** — *Diff against the previous release on the same channel:* signing method or signer (key fingerprint, attestation repo/workflow) | checksum file present | release author (CI bot vs manual upload) | immutability (prior releases immutable, this one not) | asset set (new installer types, post-install scripts) | install script: new domains fetched, new `sudo`, new persistence (LaunchAgent, systemd unit, shell rc edits) | Homebrew: formula `url` host or owner change, new `post_install`. *Ownership transfer:* repo transferred or renamed to a different owner, or a new publishing org → HIGH flag (tightens the shared ≥ MEDIUM floor).
- **V4** — *Incident sources:* the repo's GitHub Security Advisories; the vendor's security page or blog; `Homebrew/homebrew-core` issues and PRs that revert, disable or pin back the formula; OSV for the repo and its module/crate ecosystem.
- **V5** — *Triggers:* install script URL or domain change | signing key or attestation identity rotation | binary adds self-update, telemetry or a persistent service | Homebrew core formula disabled, deprecated or renamed. *Update controls:* download the audited tag's assets, never `latest`; Homebrew: `brew pin <formula>` holds `brew upgrade`; version and toolchain managers: pin the version in project config (e.g. `rust-toolchain.toml`, `.nvmrc`, `mise.toml`) and turn off built-in self-update where the tool offers it. For a binary that self-updates with no off switch, say updates cannot be held and list the triggers.
