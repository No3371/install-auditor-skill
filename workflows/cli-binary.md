<!--
workflows/cli-binary.md - Type 7 subject-specific workflow.
Handles CLI tools and standalone binaries distributed via GitHub
Releases, vendor-hosted downloads, Homebrew formulae (homebrew/core
and third-party taps), language-version and toolchain managers (nvm,
pyenv, rustup, mise, fnm, uv), install scripts (curl-pipe-bash), and
GoReleaser-built releases.
Cross-platform: Windows, macOS, Linux.

This workflow replaces workflows/generic.md for Type 7 subjects. After
producing findings here, return to SKILL.md Step N for the shared verdict
tree and report shape. The Audit Coverage table and audit-confidence
assertion are owned by the dispatcher — do not duplicate them here.
-->

# CLI Binary Workflow (Type 7)

This workflow handles **Type 7: cli-binary** subjects — standalone
executables installed onto `$PATH` (or equivalent), distributed outside
any registry that scores publisher trust. Covers GitHub Releases
binaries, vendor-hosted executables, Homebrew formulae (homebrew/core
and third-party taps; casks are desktop-app), language-version and
toolchain managers, install scripts (curl-pipe-bash), and
GoReleaser-built releases.

After completing all sections below, return to `SKILL.md` Step N for the
shared verdict tree and audit-coverage report shape.

Sections follow the standard workflow template: **Identify / Evidence /
Subject Rubric / Subject Verdict Notes**.

Use `references/criteria/cli-binary.md` for cli-binary-specific
tiering and scoring. When it conflicts with the shared rubric, the more
specific cli-binary guidance wins — except `references/criteria.md`
§4.6 (version-integrity floor) and the §4.3 Blocking CVE classes, which
it only tightens or fills.

## Identify

### 1. Determine the distribution channel and binary identity

| Channel | URL / command pattern | Adoption metric |
|---------|---------------------|-----------------|
| Homebrew core formula | `brew install <name>` resolving to tap `homebrew/core`; `formulae.brew.sh/formula/*` | Install count (analytics) |
| Homebrew third-party tap | `brew install <user>/<tap>/<name>`; `brew tap <user>/<tap>` then `brew install <name>` | Tap repo stars |
| GitHub Releases (org) | `github.com/<org>/<repo>/releases`, download from Releases page | Download count per asset |
| GitHub Releases (personal) | `github.com/<user>/<repo>/releases` | Download count per asset |
| GoReleaser | Release assets with `checksums.txt`, multiple OS/arch binaries | Download count |
| Vendor-hosted binary | Vendor website download page, `get.<vendor>.com` | Website traffic / brand |
| Language-version / toolchain manager | `curl … \| sh` (rustup, nvm, mise, fnm, uv), `pyenv install` | GitHub stars + community |
| Install script (curl-pipe-bash) | `curl -sSL <url> \| sh`, `wget -qO- <url> \| bash`; PowerShell `irm <url> \| iex`, `iwr <url> \| iex`, `iex ((New-Object Net.WebClient).DownloadString('<url>'))` | Script source reputation |
| Third-party mirror / shared copy | Non-vendor download site, forum link, file host, network share, chat attachment | None |

For each subject, record:
- **Binary name + version** (or "latest" if unversioned)
- **Distribution channel** (from table above)
- **Homebrew tap** — for `brew install`: `brew info <name>` prints a
  `From:` URL; `Homebrew/homebrew-core` = core. A fully qualified
  `<user>/<tap>/<name>` is never core
- **Source URL** (GitHub repo, vendor site, or install script URL)
- **Install-command source** — where the user got the command (vendor
  docs or repo README, ad, search result, forum, chat, AI answer, a page
  asking them to paste it to "verify")
- **Target platform** (OS + architecture)
- **Install command** (exact command the user will run)

### 2. Extract available metadata

From the distribution channel, collect:
- **Author / organization** — GitHub org, vendor name, project maintainers
- **Repository** — source code location (if open-source)
- **Release date** — when this version was published (§4.6 V1)
- **Release assets** — list of files (binaries, checksums, signatures)
- **License** — from repo or release notes
- **Checksum file** — presence of SHA-256/SHA-512 checksum file in release assets
- **Signature / attestation** — GPG `.asc`/`.sig`, Minisign `.minisig`,
  Sigstore bundle, GitHub artifact or release attestation (immutable
  release), SLSA provenance
- **Expected identity** — the repo, release workflow, key fingerprint
  or Homebrew tap the vendor documents (§4.6 V2), and where it says so
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

**Tier 1 — Quick Audit:** Well-known project, Homebrew core formula or
established GitHub org, checksum + identity verified per §4.6 V2
(homebrew/core counts via its curated pipeline), project >= 1yr old,
no incidents, `references/criteria.md` §4.6 raises nothing that bars
Tier 1, no install-script-only distribution. Scope: §4.1 Provenance +
§4.3 Security (CVEs) + §4.6 Version integrity.

**Tier 2 — Standard Audit (default):** Recognizable channel (incl. a
Homebrew tap the vendor documents), checksum available, identifiable
author, no unresolved incidents, project > 30 days old. Scope: all §4.x
sections per shared rubric.

**Tier 3 — Deep Audit:** Any red-flag trigger (curl-pipe-sh or
PowerShell `irm | iex`, no checksum/signature, unknown source,
third-party mirror or undocumented tap, chat-shared, install command
from an ad / search result / paste-to-verify page, identity mismatch
with vendor docs or the previous release, new project, prior incident,
privilege request). Scope: all §4.x + full install-script review +
provenance deep-dive + alternatives assessment.

## Evidence — Part B: Research & Verification

### Core research questions

Answer these for every CLI binary audit (depth scales by tier):

1. **Who published this binary?** Identify the author/org. Verify GitHub
   org membership or vendor identity. Is the publisher the same as the
   upstream project author? Is the install command or URL the one in the
   vendor's own docs or repo README, reached directly?
2. **Is the source code available?** Open-source repo? Does the release
   tag match the source? Can the binary be built from source?
3. **Is a checksum provided?** SHA-256/SHA-512 file in release assets?
   Is the checksum file served from the same origin as the binary, or
   from a separate trust channel? Is the checksum file itself signed?
4. **Is the binary signed or attested?** GPG, Minisign, Sigstore bundle,
   GitHub artifact or release attestation, SLSA provenance? Does
   verification pass **and** name the expected identity (§4.6 V2)?
5. **Is the release immutable?** `gh release view <tag> -R
   <owner>/<repo> --json isImmutable,publishedAt,author`.
6. **Is the install method a pipe-to-shell script?** If yes: is the
   script auditable? Is it served over HTTPS? What does it actually do?
   Does it download a binary and verify its checksum, or does it execute
   arbitrary code without verification? Apply the executed-bytes rule
   (`references/criteria/cli-binary.md` Install Script Risk).
7. **What does the binary do at runtime?** Network access, file system
   writes, privilege escalation, persistent services? Does it phone home?
8. **Are there known CVEs or security incidents?** Search OSV, GHSA,
   vendor advisories, and web for the binary name + "vulnerability" or
   "compromise". Classify each CVE as own code or third-party component
   (addendum §4.3 plug-in).
9. **Is it actively maintained?** Last release date, commit frequency,
   issue responsiveness. Have the maintainers declared it unmaintained?
10. **How does this version differ from the previous release?** Signer,
    release author, asset set, install-script behavior (§4.6 V3).
11. **Are there alternatives?** Package-manager-distributed alternatives
    (brew, apt, cargo install) that provide stronger provenance?

### Distribution channel research

- **Homebrew core formula:** Confirm the tap (`brew info <name>` `From:` line). Read the formula in `Homebrew/homebrew-core`: `url` points at the upstream project's documented source, `sha256` is pinned, and recent formula commits don't change the `url` host or owner. Bottles are built and attested by Homebrew CI; if `gh` is available, verify with `HOMEBREW_VERIFY_ATTESTATIONS=1` (opt-in as of 2026-10).
- **Homebrew third-party tap:** Identify the tap owner and whether the upstream project's own docs name this tap. Read the formula Ruby, which runs with the user's privileges when loaded: `url`, `sha256`, `install` / `post_install` blocks. Homebrew does not review taps; `brew trust` (Homebrew 6.0.0+) only records the user's consent.
- **GitHub Releases:** Check release page: author, tag, CI artifacts, checksum file, signature/attestation files. Compare release author to repo owner. Check if release was created by GitHub Actions (CI-built) or manually uploaded, and whether it is immutable.
- **Vendor-hosted:** Verify the download URL against the vendor's documented domain, reached directly rather than via an ad or search result. Check for HTTPS. Look for a checksum/signature on the download page.
- **Install script (incl. PowerShell `irm … | iex` forms):** Download the script to a file (do NOT pipe to shell), read that file, and record its SHA-256; if approved, the user runs that same file. Assess: what URLs does it fetch? Does it verify checksums? Does it require sudo / an Administrator session? What does it install and where? Are there any obfuscated or encoded sections? A URL shortener, redirector, paste site, raw IP or plain-HTTP URL is an unverifiable source; expand a shortener only to report its target, never to run it.
- **Mirror / shared copy:** Hash the file and compare with the vendor's signed checksum file for that exact version (verify the checksum file's signature first). Match → channel risk is a note. No match or no signed checksum → rate as third-party mirror.

### Checksum & signature verification

For every tier (Tier 1 needs verified identity or the homebrew/core
curated pipeline), verify or document inability to verify. Commands and
identity values: `references/criteria/cli-binary.md` Signature &
Checksum Standards.

1. Download the checksum file (e.g., `checksums.txt`, `SHA256SUMS`)
2. Verify the binary's hash matches the checksum file entry
3. Verify identity with the method's command, bound to the expected
   identity: `gh release verify` / `gh release verify-asset`,
   `gh attestation verify --repo`, `cosign verify-blob --bundle` with
   `--certificate-identity` + `--certificate-oidc-issuer`,
   `slsa-verifier verify-artifact --source-uri`, or a GPG/Minisign key
   matched against vendor docs
4. Record the expected identity, its source and the result in the
   Version integrity row. Presence alone earns no credit
5. Run these tools under the audit-tooling note in
   `references/criteria.md`; if you cannot, record
   `Not available (<why>)`

### Incident & reputation research

- Search: `"<binary-name>" vulnerability`, `"<binary-name>" compromise`, `"<binary-name>" malware`
- Check GitHub Security Advisories for the repo
- Check if the project has been transferred, archived, or changed ownership recently
- For a past compromise, record its affected range and remediation (§4.6 V4)
- For language-version managers: check for known supply-chain incidents in their install pipeline

### Audit coverage tracking

Track which checks were performed per tier (guide, not output — the
Audit Coverage table itself is in `SKILL.md` Step N):

| Check | Tier 1 | Tier 2 | Tier 3 |
|-------|--------|--------|--------|
| Binary identity + channel (incl. Homebrew tap) | Yes | Yes | Yes |
| Install-command source (vendor docs vs ad / search / lure) | Yes | Yes | Yes |
| Author/org verification | Brief | Yes | Deep |
| Checksum verification | Yes | Yes | Yes |
| Identity verification (§4.6 V2) | Match expected identity (or homebrew/core pipeline) | Verify if available | Verify or flag absence |
| SLSA provenance | Covered by identity row | Check | Verify |
| Version integrity (§4.6 V1, V3–V5) | Age + quick V3 check | Yes | Full diff vs previous release |
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

- **Primary axis: checksum + identity verification** matched to the
  expected identity (§4.6 V2). A verified, checksummed binary from a
  known author/org is the strongest provenance signal; a signature that
  is present but unverified or unmatched earns nothing. An unsigned
  binary with no checksum from an unknown source is the weakest.
- Assess the release pipeline: CI-built (strong) vs manual upload
  (weaker); an immutable release is a further positive.
- GitHub: verify release author matches repo org/owner. Check for branch
  protection and required CI checks.
- Install scripts: assess the script's own provenance (URL traced to
  vendor docs? HTTPS? auditable content?) and apply the executed-bytes
  rule.
- Homebrew core: trust comes from maintainer review + the Homebrew CI
  bottle build (curated pipeline), not from the user's option to build
  from source. Third-party tap: trust = the tap owner (vendor-documented
  tap → vendor channel; otherwise repackager).
- Mirror / shared copy: bytes verified against the vendor's signed
  checksum → channel risk is a note.

### §4.2 Maintenance & Project Health

- Last release date, commit frequency, open issue responsiveness.
- Bus factor: single maintainer vs team/org.
- For language-version managers: assess the governing project (e.g. the
  Rust project for rustup; nvm is an OpenJS Foundation project).
  Governance is a maintenance signal, not install-time verification.
- A project its maintainers declare unmaintained (e.g. Volta, Nov 2025)
  is Abandoned; name the successor they recommend.
- Archived or transferred repos are strong negative signals.

### §4.3 Security — Vulnerabilities & Incidents

- Check OSV/GHSA for the binary name and its source repo.
- Search for prior supply-chain compromises (especially for install scripts
  and widely-used binaries).
- Assess dependency chain if the binary is a compiled artifact (Go, Rust
  binaries ship their deps statically).
- Classify CVEs as own code or third-party component per
  `references/criteria/cli-binary.md` Own Code vs Third-Party Components
  (§4.3); verdict classes per `SKILL.md` "Blocking CVE".
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

### §4.6 Version & Update Integrity

- Apply `references/criteria.md` §4.6 with the plug-ins in
  `references/criteria/cli-binary.md` Version & Update Integrity (§4.6).
- Version age from the release date (Homebrew core: the upstream
  release date); identity per V2; diff against the previous release
  (V3); scope any past compromise by version (V4).
- Recommendation names the update control: the pinned tag's assets,
  `brew pin`, or the toolchain pin file (V5).

### Alternatives & Ecosystem Fit

- Is there a package-manager-distributed alternative (brew, apt, cargo install)?
- Is there a containerized alternative (docker run)?
- Does the project offer multiple install methods? (Binary download, package
  manager, build from source — breadth of options is a positive signal.)
- For language-version managers: are there alternatives with better provenance
  or security posture?

## Subject Verdict Notes

### Toward REJECTED

- Install script (`curl | sudo sh`) from unknown or unverifiable source
- Pipe-to-shell in any shell (`curl … | sh`, PowerShell `irm … | iex`,
  `iex (… DownloadString …)`) from a URL that hides the publisher
  (shortener, redirector, paste site, raw IP) or uses plain HTTP
- Install-command lure: reached via ad or sponsored result, or presented
  as a paste-to-verify / fix-an-error step, and not the vendor's
  documented command
- Install URL on a lookalike of the vendor's domain (`SKILL.md` Red Flag
  "Confirmed typosquat / impersonation")
- No checksum AND no signature AND no package-manager alternative
- Binary from third-party mirror or repackager (not original author)
  whose bytes cannot be verified against the author's signed checksum
- Supply-chain compromise that covers the version to be installed, has
  no bounded range, or is unresolved (`references/criteria.md` §4.6 V4
  case a)
- Binary requires root/admin with no clear justification
- Obfuscated or encoded sections in install script

### Toward CONDITIONAL

- Install script from known vendor (note pipe-to-shell risk; recommend
  the executed-bytes rule: download, inspect, hash, run that file)
- Checksum available but no signature (note: integrity without authenticity)
- Legitimate binary via an informal channel (shared drive, Slack, forum,
  mirror) whose bytes are not yet verified — condition: verify its
  SHA-256 against the vendor's signed checksum for that version, or
  reinstall from the official source. Once verified, the channel is a
  note
- Single maintainer project with no CI (note bus factor + build provenance risk)
- Vendor-hosted binary unsigned but from known, reputable vendor
- Homebrew third-party tap the vendor documents, with no verified
  identity
- Project recently changed ownership or was transferred (§4.6 V3)
- Project abandoned (no releases > 2 years, archived repo, unresponsive
  maintainer, or declared unmaintained) — CONDITIONAL per the
  `SKILL.md` tree; condition names a maintained alternative. REJECTED
  only together with another REJECTED trigger (Blocking CVE, §4.6 V4
  case a)
- Version < 72 h old, or identity evidence missing or changed vs the
  previous release (§4.6 V1, V3)

### Toward APPROVED

- Homebrew core formula (tap `homebrew/core`) whose `url` is the
  upstream project's documented source (curated pipeline, §4.6 V2)
- GitHub Releases from established org with CI-built artifacts +
  checksum + signature or attestation verified against the project's
  repo and release workflow (immutable release a plus)
- Well-known, maintained language-version manager (e.g. rustup, nvm,
  mise) from an established project
- Established project (>= 1yr, broad adoption, active maintenance)
- Multiple install methods available (binary, package manager, source)
- SLSA L2+ provenance verified against the project repo
