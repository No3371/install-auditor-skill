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
