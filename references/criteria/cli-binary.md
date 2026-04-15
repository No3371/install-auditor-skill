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
