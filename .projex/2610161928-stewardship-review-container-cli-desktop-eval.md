# Stewardship Review — container-image, cli-binary, desktop-app

> **Status:** Draft
> **Author:** Claude (Opus)
> **Parent:** Orchestrator
> **Subject:** `workflows/container-image.md` + `references/criteria/container-image.md` | `workflows/cli-binary.md` + `references/criteria/cli-binary.md` | `workflows/desktop-app.md` + `references/criteria/desktop-app.md`
> **Type:** Gap Analysis (scheduled `STEWARDSHIP.md` review pass, checklist steps 1–3, step 4 offline)
> **Tier:** Standard (upper) — 3 subjects, live external research
> **Lenses Applied:** Inversion (2026 incidents vs. rubric) | Constraint Mapping (rubric vs. tree vs. evals) | Steel-Manning (keep-as-is case)
> **Related Projex:** 2610161852-dispatcher-rubric-consistency-walkthrough.md (prior follow-ups re-verified here) | 2604172000-stewardship-cadence-m63-walkthrough.md | 2604070218-install-auditor-subject-typed-redesign-nav.md (Phase 6 log owner) | sibling reviews 2610161927-registry-package-and-ci-action-stewardship-review-eval.md, 2610161927-browser-extension-ide-plugin-stewardship-review-eval.md, 2610161927-agent-extension-stewardship-review-eval.md, 2610161927-remote-integration-generic-stewardship-review-eval.md

---

## 1. Executive Summary

All six files were written 2026-04-15. The workflow files got only header/label edits on 2026-10-16, and the criteria files are untouched. Since April, six months of ecosystem change have broken several of their assumptions. **The main defect cuts across all three subjects.** The rubrics give credit when a signature, attestation or notarization is merely present. They never check *who* signed it, from *which* source, or *how new* the version is. The 2026 incidents get through exactly that gap: Trivy (Mar), Checkmarx KICS (Apr), and the notarized MacSync stealer (Dec 2025). **Some instructions are now stale or harmful:** `DOCKER_CONTENT_TRUST=1` now breaks Docker Official Image pulls, bare `cosign verify` fails for keyless signatures, `cosign download sbom` is deprecated and its output unsigned, and Volta is unmaintained but listed as an APPROVED exemplar. **Several trust tables are factually wrong now:** macOS non-notarized apps, EV SmartScreen behavior, Homebrew casks, Microsoft Store sandboxing, and Homebrew taps vs. core. Prior tensions (a)–(c) in the container rubric and the cli-binary "abandoned" conflict are all still present. Eval 26's description also contradicts the container tier thresholds. Offline eval checks pass: validate ✓, 12 self-tests ✓, prepare ✓; live run not approved. **Recommendation:** 1 cross-cutting plan, then 3 per-subject plans and 1 eval-case plan. Two policy decisions go to a human first (container CVE/VEX rule; DOI Tier 1 and rootful-dev grading).

## 2. Evaluation Scope

**Question:** Do these rubrics still reflect the ecosystems as of 2026-10-16? What is stale, missing, or wrong?

| Criterion | Weight | Description |
|---|---|---|
| Factual currency | High | Commands, tools, platform behavior, and policies match today's reality |
| Verdict safety | High | 2025–26 real attacks would not pass to APPROVED / CONDITIONAL-lite |
| Internal consistency | Med | Workflow ↔ addendum ↔ `SKILL.md` tree ↔ `references/criteria.md` ↔ evals agree |
| Coverage of new trust signals | Med | New signals (immutable releases, DHI, Artifact Signing, …) are scored |

**Out of scope:** editing rubric/STEWARDSHIP files (review rule: checklist step 5) | live `run` evals | other 7 subjects (sibling evals) | STEWARDSHIP steps 7–8 (date columns, nav log) — orchestrator-owned.

## 3. Context

- Files created 2026-04-15 (M3.2, M4.1, M4.2). Last edit was commit `5c44b79` on 2026-10-16: workflow header lines only, no rubric substance. Criteria addenda unchanged since creation. `STEWARDSHIP.md` cadence 120 d for all three; never reviewed (≈184 d elapsed → overdue).
- `5c44b79` removed the dispatcher's container-root Red Flag. The container workflow now owns that grading, so the container rubric's internal tensions now drive verdicts.
- Precedence (`SKILL.md` Tree terms): for subject-specific patterns, the workflow and addendum win over generic wording → errors in the addenda now flow straight into verdicts.

## 4. Foundations

**Principle:** a trust signal is worth something only if it binds an artifact to an *expected* identity. "Signed" only means "someone with a key or OIDC token signed this". Attackers with stolen publisher or CI credentials produce valid signatures and provenance.

| Assumption (embedded in rubrics) | Validity now | Risk if wrong | Flips rec? |
|---|---|---|---|
| Signature/attestation present ⇒ strong positive | ✗ (KICS, Trivy, MacSync) | Compromised releases graded APPROVED | Yes |
| Specific semver tag ≈ immutable | ✗ (KICS `v2.1.20` overwritten) | Tier 1 on a mutable ref | Yes |
| Project age is the freshness signal | ✗ (attack windows are hours on old projects) | Day-0 malicious version passes | Yes |
| Store listing ⇒ sandboxed + reviewed | Partial (MS Store Win32, Snap scams) | Overcredit | No (severity) |
| Notarization ⇒ Apple malware-scanned ⇒ strong | Partial (notarized MacSync) | Overcredit | No (severity) |
| Tool commands in rubrics are current | ✗ (DCT, cosign, slsa-github-generator) | Auditor errors / false "unsigned" | No |

**Prior work:** 2610161852-dispatcher-rubric-consistency-plan.md Out-of-Scope (a)–(c) + cli-binary "abandoned" — each re-checked below (C6, C7, C4, B5).

## 5. Analysis

Severity: **HIGH** = can produce a wrong verdict on a realistic attack or makes the auditor run a broken/harmful command | **MEDIUM** = wrong/stale fact or missing major signal that skews scoring | **LOW** = refinement.

### 5.X Cross-cutting

**X1 — Presence-based crediting; no identity binding.** HIGH | Conf H | Inversion.
- Rubric: `references/criteria/container-image.md` Signing scoring "Cosign keyless verify passes with Rekor inclusion = strong positive" (L45). The table shows `--certificate-identity-regexp ...` but never says what identity to expect. `references/criteria/cli-binary.md` L54 "GPG/Sigstore/Minisign signature + checksum = strong positive". `references/criteria/desktop-app.md` L54 "Apple Developer ID + notarization … = strong positive". Workflows: "Does `cosign verify-attestation` surface a build provenance document?" (`workflows/container-image.md` L194) — tests presence only.
- Evidence: KICS (2026-04-22): valid Checkmarx Docker Hub creds; tags overwritten; the provenance named a source repo created one day earlier, and that mismatch is how Docker spotted it. Trivy (2026-03-19→23): stolen creds → malicious v0.69.4 release, 76/77 `trivy-action` tags force-pushed, malicious 0.69.5/0.69.6 Hub images. MacSync (Dec 2025): dropper was signed **and notarized** (Team ID `GNJLS3UYZ4`), later revoked.
- Implication: every rubric needs one rule — **verify against the expected identity**. That means the signer identity/issuer (Fulcio SAN + OIDC issuer), the provenance source repo + workflow + ref, the macOS Team ID, and the Authenticode subject, each matched against the vendor's documented identity. Presence without a match = note only. Also add a revocation check (`spctl --assess -vv`, `codesign -dv --verbose=4`).

**X2 — No version-age (cooldown) signal.** HIGH | Conf H | Inversion.
- Rubric: `references/criteria/cli-binary.md` Tier 3 "First release < 30 days old" (L131) = *project* age. The Desktop Tier 1 rule "available ≥ 1 year" (L138) is also project-level. Container rubric has none. The `SKILL.md` Red Flag "Brand new + no history — < 72 h with no prior versions" excludes new versions of old projects.
- Evidence: Trivy malicious artifacts were live ~3 h (v0.69.4), ~12 h (`trivy-action`), ~4 h (`setup-trivy`). KICS counterfeit `v2.1.21` matched no upstream release.
- Implication: add "version published < N h/days, or tag with no matching upstream release/changelog → wait or pin previous known-good digest" (CONDITIONAL). N is a policy decision; 72 h is consistent with the Red Flag.

**X3 — Audit toolchain is itself an unpinned supply-chain dependency.** MEDIUM | Conf H.
- Rubric tells the auditor to run `trivy image`, `grype`, `syft`, `cosign`, `slsa-verifier` (`workflows/container-image.md` L148–156, `workflows/cli-binary.md` L139–145) with no version pin or verification. Trivy 0.69.4–0.69.6 stole CI secrets, SSH keys, and cloud creds.
- Implication: say "use a pinned, verified scanner version (known-good digest/release); prefer registry-side scan data when the local tool can't be verified".

### 5.C container-image

**C1 — Mutable tags credited as immutable / Tier-1 eligible.** HIGH | Conf H.
- `references/criteria/container-image.md` Tag table: `1.27.3-alpine` "Mostly immutable by convention … Low-Medium" (L145). Tier 1: "specific immutable tag variant from a publisher that pins conventionally" (L164). `workflows/container-image.md` Tier 1 + Toward APPROVED "Digest-pinned … OR specific immutable tag" (L84, L307).
- Evidence: KICS `v2.1.20`, `v2.1.20-debian`, `alpine`, `debian`, `latest` repointed via normal publish flow. Docker's own remediation: "Re-pull by digest and pin CI to that digest".
- Fix direction: only `@sha256:` is immutable on Docker Hub. A semver tag = moderate at most, never Tier 1. Exception: registries with enforced tag immutability (e.g. ECR immutable repos) — needs a verified per-registry statement.

**C2 — Docker Content Trust instructions now break pulls.** HIGH (harmful command) | Conf H.
- `workflows/container-image.md` L136 `DOCKER_CONTENT_TRUST=1 docker pull` ("deprecated"). `references/criteria/container-image.md` L41 "Still present for some older Docker Official tags".
- Evidence: Docker retired DCT (2025-07-29 post). Since 2025-08-08, DOI signing certs expire → DOI pulls with `DOCKER_CONTENT_TRUST=1` fail and `docker trust inspect` stops working. A follow-up post retires Notary v1 at `notary.docker.io`. ACR retires DCT 2028-03-31.
- Fix: remove DCT as a verification path. Treat it as "retired — absence carries no signal".

**C3 — Stale Sigstore/SBOM/provenance commands.** MEDIUM | Conf H (cosign identity flags from cosign ≥2.0 behavior, known), M (v3 defaults — secondary sources).
- Bare `cosign verify <image>` (`workflows/container-image.md` L112, L133) errors in keyless mode without `--certificate-identity[-regexp]` + `--certificate-oidc-issuer[-regexp]`. That failure also feeds the auditor a false "unsigned".
- Cosign v3: Sigstore bundle format is the default, and signatures are stored as OCI 1.1 referrers (sources conflict on the storage default). Rekor v2 GA 2025-10-10: tile log, no integrated time; RFC 3161 timestamp supplies time; old clients can't verify v2 entries.
- `cosign download sbom` is deprecated, and attached SBOMs are **unsigned** (cosign docs). Rubric uses it as Tier 1 evidence (`references/criteria/container-image.md` L166). It also conflates "attached" with "attestation" (L60, L64: "SBOM attached as Cosign attestation … strong positive"). Correct path: `cosign verify-attestation --type spdxjson|cyclonedx` with identity flags.
- `slsa-framework/slsa-github-generator` (workflow L117, L192) is reported in de-facto maintenance since 2025-02 (third-party note — Conf M). The mainstream path is `actions/attest-build-provenance` → `actions/attest`, verified with `gh attestation verify oci://<img> --owner|--repo`. That command is absent.
- Missing: `docker buildx imagetools inspect <img> --format '{{json .Provenance}}' / '{{json .SBOM}}'` for BuildKit attestations (DOI's main form).

**C4 — Tier 1 is unreachable for Docker Official Images; eval 26 contradicts the tier rules.** MEDIUM | Conf H (rubric trace), M (DOI signing state).
- Tier 1 needs (a) a digest or immutable tag and (b) a Cosign sig OR GitHub-attested SLSA (`references/criteria/container-image.md` L164–165). DOI: DCT retired; no Docker DOI Cosign replacement found (the 2023 OpenPubkey plan has no confirmed rollout). DOI attestations are BuildKit provenance/SBOM.
- Eval 26 (`docker pull redis`, dev) says "Tier 1 quick audit … APPROVED". Per rubric: no tag ≡ `:latest` (L148) → **Tier 3 trigger** (L183). Dev use → `:latest` "MEDIUM note" (L155). No `USER` → Medium-High pattern (L75). `workflows/container-image.md` Toward CONDITIONAL "Rootful image on developer workstation" (L298) → the rubric yields CONDITIONAL; the eval expects APPROVED. **Prior tension (b) confirmed, plus a new tier-label contradiction.**
- Also: the "no `USER` = root" heuristic misfires on images whose entrypoint drops privileges (e.g. `gosu`/`setpriv` patterns in some official DB images). Conf M — verify per image before codifying.
- Needs a **human policy decision**: do DOIs get a Tier 1 path without user-verifiable signatures (DOI pipeline trust + BuildKit attestations), and is rootful-on-dev a CONDITIONAL or a LOW note? Then align eval 26 text.

**C5 — Hardened-image catalogs missing; curated base list stale.** MEDIUM | Conf H.
- Docker Hardened Images: launched 2025-05; free + Apache-2.0 since 2025-12. >1,000 images, SBOM + SLSA Build L3 provenance + signed attestations + public CVE/VEX data; registry `dhi.io` (auth required). Docker reported the DHI Trivy image was unaffected by the March compromise.
- Caveat to encode: DHI attestations are not always in public Rekor. A default `cosign verify` then fails with "signature not found in transparency log", and an auditor could wrongly mark the image unsigned. Verify with Docker's published key, or with `docker scout attest get … --verify`.
- Base list (`references/criteria/container-image.md` L168) omits DHI, Chainguard/Wolfi, and similar. Scoring table has no hardened-catalog row.

**C6 — CVE rule tension; no VEX.** MEDIUM | Conf H.
- `workflows/container-image.md` Toward APPROVED "high CVEs have documented mitigations or are pending a patch in an acceptable window" (L309). The `SKILL.md` tree says "Any unpatched HIGH/CRITICAL CVE → REJECTED", and "unpatched" there means *no fixed release exists*. `references/criteria.md` L134 says "REJECTED if unpatched". **Prior tension (c) confirmed.**
- Worse than in April: OS-package HIGH CVEs with no distro fix are routine. Read literally, the tree rejects most Debian-based images, while precedence lets the workflow override — so the result swings on auditor judgment.
- Missing: VEX (OpenVEX/CSAF "not_affected"), which DHI and Scout now publish; reachability; "fixable vs. unfixable" split. Needs a human decision (same session as C4).

**C7 — Critical runtime flags graded three ways.** MEDIUM | Conf H.
- Addendum: "Any one critical-risk flag on an unverified image = HIGH flag" (L135) → CONDITIONAL. Workflow Toward REJECTED: "`--privileged` … on an unverified/untrusted image … near-automatic rejection" (L285). `references/criteria.md` L194: "Mounting `/var/run/docker.sock` → CRITICAL". Under precedence the addendum wins, so docker.sock + unverified image tops out at CONDITIONAL. **Prior tension (a) confirmed, plus a new leg (shared criteria).**
- Fix direction: critical runtime flag + unverified/unsigned image = CRITICAL; + verified publisher with documented need = HIGH.

**C8 — Catalog withdrawal / frozen namespaces; registry naming.** LOW-MEDIUM | Conf M-H.
- Bitnami: from 2025-08-28 most `docker.io/bitnami` images moved to `docker.io/bitnamilegacy`, which gets no updates. Public catalog removed ~2025-09-29. Free images are `latest`-only. Many Helm charts still reference the old paths. The rubric has no "frozen/legacy namespace" signal → `bitnamilegacy/*` looks like a recognized publisher.
- GCR: writes off 2025-03-18, reads off 2025-06-03; `gcr.io` is now served by Artifact Registry. Rubric's "(legacy)" label is fine; "Google Container Registry" naming is stale. LOW.

**C9 — Runtime / hygiene refinements.** LOW | Conf H.
- K8s user namespaces GA in v1.36 (`spec.hostUsers: false`; usable without a gate since 1.33) → a positive signal that namespaces caps like `NET_ADMIN`. Pod Security Standards `restricted` and seccomp `RuntimeDefault` are absent as baselines.
- Old-digest risk: Binarly (2025-08) found ≥35 Debian-derived Hub images still carrying the xz backdoor (CVE-2024-3094). A digest pin freezes risk too → pin + refresh cadence.
- Secrets in layers: Flare found 10,456 images leaking secrets (Nov 2025 uploads), with AI API keys the most common. Add a layer secret scan (`trivy image --scanners secret`, pinned per X3).

### 5.B cli-binary

**B1 — Homebrew taps not distinguished from homebrew-core; Homebrew trust model inaccurate.** HIGH | Conf M-H.
- Rubric has a single channel row "Homebrew core formula" (`references/criteria/cli-binary.md` L15) and Toward APPROVED "Homebrew core formula with build-from-source option" (`workflows/cli-binary.md` L257). `brew install <org>/<tap>/<name>` (third-party tap) has no row → likely misread as core.
- Evidence: in Trivy v0.69.4, the vendor's custom tap was compromised, while the homebrew-core formula (built by Homebrew CI from source) was not (secondary sources).
- Model fix: the default install is a **bottle** built and attested by homebrew-core CI (Sigstore build provenance, Trail of Bits/Sigstore 2024). The trust anchor is Homebrew CI, not "build-from-source option". Bottle attestation counts toward the Tier 1 "signature" requirement (eval 20 ripgrep). Whether verification is on by default is unverified (`HOMEBREW_VERIFY_ATTESTATIONS` / `HOMEBREW_NO_VERIFY_ATTESTATIONS` conflicting reports).

**B2 — GitHub immutable releases + release/artifact attestations missing.** MEDIUM | Conf H.
- Immutable releases GA 2025-10-28: assets can't be changed, tags can't move, and each release gets a Sigstore-bundle attestation. Verify with `gh release verify` / `gh release verify-asset` (gh ≥ 2.81.0). Only new releases are covered. Artifact attestations: `gh attestation verify <file> --owner|--repo`.
- Evidence it matters: Trivy's `trivy-action` v0.35.0 was the protected tag — immutable releases blocked the force-push.
- Rubric knows only `slsa-verifier` (`workflows/cli-binary.md` L113, L143) and treats a co-hosted checksum as the GitHub default.

**B3 — Language-version-manager facts wrong.** MEDIUM | Conf H (OpenJS), M-H (Volta).
- `workflows/cli-binary.md` L196 "Node.js Foundation for nvm": that foundation merged into the OpenJS Foundation in 2019; nvm is an OpenJS project.
- L259 Toward APPROVED "Well-known language-version manager (rustup, volta) from established foundation". Volta: maintainers declared it unmaintained (~Nov 2025, repo issue #2080) and recommend mise. It was never foundation-governed. The current text pushes an unmaintained tool toward APPROVED.
- Absent: mise, fnm, uv (curl-installed, very common in 2026).

**B4 — Install-script lures and server-side divergence.** MEDIUM | Conf H.
- Evidence: fake brew.sh typosquats via Google Ads and SEO, and "ClickFix" paste-into-Terminal pages, Oct 2025 → May 2026. Delivered AMOS, Odyssey, Cuckoo, MacSync; the payloads harvested macOS passwords and installed LaunchAgents.
- Rubric: "known vendor + HTTPS" (`references/criteria/cli-binary.md` L22). It doesn't require the exact install URL to be verified against the vendor's own docs/repo (not an ad or search result), and has no lure pattern ("paste this to verify", CAPTCHA-to-Terminal).
- "Download the script … Read it" (`workflows/cli-binary.md` L133) is weaker than it looks: servers can serve different bytes to a browser vs. a `curl | sh` pipe. Rule: inspect and hash the exact bytes you will execute (download to a file → read → run that file), or prefer a script pinned to a repo commit.

**B5 — "Abandoned" conflict (prior) still present.** LOW-MEDIUM | Conf H.
- `workflows/cli-binary.md` L242 Toward REJECTED "Project abandoned (no releases > 2 years …)". The tree says "Abandoned with no alternative → CONDITIONAL"; `references/criteria.md` L119 says "CONDITIONAL or REJECTED". Fix direction: abandoned alone → CONDITIONAL; REJECTED only with an unpatched vuln or compromise.

**B6 — Transport channel vs. verified bytes.** LOW-MEDIUM | Conf H.
- Eval 30 (terraform copy on a colleague's share → CONDITIONAL) vs. Toward REJECTED "Binary from third-party mirror or repackager". The rubric lacks a rule: if the bytes verify against the upstream *signed* checksum (e.g. vendor `SHA256SUMS` + `.sig`), downgrade channel risk to a note. Without that rule, the eval passes only on auditor judgment.

**B7 — Sigstore blob commands.** LOW | Conf M-H.
- `cosign verify-blob` (`workflows/cli-binary.md` L142) needs `--bundle <file>.sigstore.json` plus identity flags. GoReleaser now emits a single bundle per artifact (cosign v3). Fold into X1.

### 5.D desktop-app

**D1 — macOS "Developer ID only, not notarized" mis-graded.** MEDIUM-HIGH | Conf H.
- `references/criteria/desktop-app.md` L45: "Gatekeeper allows with warning on first run … Moderate". Since macOS 10.15, non-notarized Developer ID software from the internet is blocked by default. Since macOS 15 Sequoia the Control-click override is gone; users must approve in System Settings → Privacy & Security.
- Fix: weak/flag. Any instruction to bypass Gatekeeper (System Settings approval, `xattr -d com.apple.quarantine`, drag-to-Terminal) is itself a lure signal (see B4, MacSync).

**D2 — Notarization ≠ malware-free.** MEDIUM | Conf H. (Instance of X1.)
- MacSync dropper notarized (Dec 2025), Apple revoked after a report. 3CX (2023): vendor-signed trojan. Fix: Team ID must match the vendor's known Team ID, plus a current-revocation check. Notarization = identity + automated scan, not review.

**D3 — Windows signing table stale.** MEDIUM | Conf M (EV/SmartScreen — secondary, one contradicting vendor post), M-H (hardware key), H (460 d, Artifact Signing).
- EV row says "SmartScreen reputation immediate" (L41). Reported removed in 2024; EV builds reputation like OV.
- "Hardware token required" is not EV-specific: CA/B CSBR has required HSM/token key storage for all public code-signing certs since 2023-06-01.
- Max validity 460 days for certs issued from 2026-03-01 (CSC-31) → more frequent cert rotation. A new cert can reset reputation, and timestamping is now essential for signatures to outlive their certs.
- Missing: Azure **Artifact Signing** (formerly Trusted Signing, renamed ~Jan 2026) — Microsoft-managed identity-validated signing; should be a row.

**D4 — Microsoft Store overcredited.** MEDIUM | Conf H (unpackaged Win32 in Store), M (full-trust MSIX isolation detail).
- Rubric: "Microsoft Store (MSIX) … MSIX apps run in container" (L14). "MS Store / Mac App Store apps are signed by definition" (`workflows/desktop-app.md` L165). "Mac App Store or Microsoft Store = strong positive (store review + sandboxing)" (L28). Tier 1 is reachable on store listing alone.
- Reality: the Store accepts unpackaged MSI/EXE apps (no package identity; unrestricted file/registry/elevation). Full-trust MSIX desktop apps are not AppContainer-sandboxed. Fix: split rows into MS Store (MSIX/AppContainer) | MS Store (MSIX full-trust) | MS Store (unpackaged Win32).

**D5 — Homebrew cask "no signing gate" stale.** MEDIUM | Conf H (policy), M (enforcement on 2026-09-01 not confirmed).
- `references/criteria/desktop-app.md` L16 "no signing gate". Homebrew 5.0.0 (2025-11-12) deprecated `--no-quarantine`/`--quarantine` and deprecated unsigned casks. Casks failing Gatekeeper were scheduled for disable on 2026-09-01; live warnings were seen on the CopyQ and PowerShell casks. Third-party cask taps are not gated (`xattr` workarounds circulate).
- Fix: official homebrew-cask ⇒ Gatekeeper-passing expected. A cask that is disabled for failing Gatekeeper = flag. A third-party tap = vendor-direct trust.

**D6 — Update-channel grading inconsistent; framework caveats missing.** MEDIUM | Conf H.
- Notepad++ (Jun → Dec 2025): hosting-level hijack of update traffic. Updater pre-8.8.9 did not verify the integrity or authenticity of downloads. This is the rubric's own "vendor-hosted updater with no signature verification" pattern, but the table says Medium-High (L105) and the scoring says "MEDIUM flag" (L112). Pick one. Given a real state-actor exploit, HIGH is defensible.
- "Signed auto-updater (Sparkle/Squirrel) = Low-Medium": signature checks have been bypassed (e.g. electron-updater Windows verifier GHSA-9jxc-qjr9-vjxq; Electron CVE-2022-29257). Add an updater-framework version check.

**D7 — Linux store signals.** LOW-MEDIUM | Conf M.
- Snap: fake crypto-wallet snaps (2023–24) → manual review for new snap names and a crypto-wallet category restriction (current status unverified). Strict confinement does not prove legitimacy, since scam wallets steal the seed via the UI.
- Flathub "verified" badge = upstream-identity link, not a security review. Neither signal is in the table.
- Flatpak sandbox escape CVE-2026-34078 (reported ≤1.16.4; secondary, Conf L) → sandbox credit depends on the runtime version.

**D8 — "EXE installer from known vendor → CONDITIONAL" too blunt.** LOW-MEDIUM | Conf M.
- `workflows/desktop-app.md` L330. Most major Windows vendors ship signed NSIS/Inno/custom EXE installers. This can conflict with eval 18 (Firefox via winget → APPROVED) depending on the manifest's installer type (not verified here, Conf L). Fix: signed EXE from a verified publisher via winget/vendor = note; unsigned EXE = flag.

**D9 — APT vendor keys.** LOW | Conf H.
- Rubric's vendor-GPG row doesn't distinguish `signed-by=`-scoped keys from global keyrings (`apt-key` deprecated). An unscoped vendor key can sign packages for any configured repo.

### 5.E Step 4 (offline) — eval status + paper trace

- `python3 evals/run_evals.py validate` ✓. `python3 -m unittest discover -s evals -p "test_*.py"` → 12 tests OK. `prepare --workflow container-image|cli-binary|desktop-app` ✓ (workspace `../install-auditor-skill-workspace`, iterations 3–5; workspace shared with siblings). `run` not executed (cost not approved) → no `grade`/`summary` regression signal.
- Paper trace (rubric text → expected verdict):

| Eval | Subject | Expected | Rubric trace | Status |
|---|---|---|---|---|
| 12 | `nginx:latest` prod | APPROVED/CONDITIONAL | `:latest` prod = HIGH → CONDITIONAL | ✓ |
| 13 | unknown-registry cryptominer | REJECTED | Toward REJECTED + CRITICAL rating | ✓ |
| 26 | `redis` dev | APPROVED, "Tier 1" | No tag → Tier 3 trigger; rootful-dev → CONDITIONAL | ✗ tension (C4) |
| 38 | `acmecorp/invoice-api` | APPROVED/CONDITIONAL | Routing + Tier 2 | ✓ |
| 20 | `brew install ripgrep` | APPROVED | Tier 1 "signature" needs bottle attestation, which the rubric doesn't recognize (B1) → likely Tier 2, verdict still APPROVED | ✓ (weak) |
| 21 | `curl … \| sudo bash` unknown | REJECTED | Toward REJECTED | ✓ |
| 30 | terraform via colleague share | CONDITIONAL | Ambiguous: Toward REJECTED "mirror/repackager" vs Toward CONDITIONAL "informal channel" (B6) | ~ judgment |
| 18 | Firefox via winget | APPROVED | Depends on installer type; "EXE from known vendor → CONDITIONAL" (D8) | ~ latent |
| 19 | fake VLC "Pro" mirror | REJECTED | Toward REJECTED | ✓ |
| 29 | OBS official vs mirror | APPROVED/CONDITIONAL | ✓ | ✓ |

- Eval gaps (checklist step 6): no case covers any 2025–26 attack pattern. Candidates:
  - trusted-publisher tag overwrite / counterfeit tag (KICS-style) → not APPROVED
  - DHI image → APPROVED
  - third-party Homebrew tap of a known tool → not Tier 1
  - CLI version < 72 h old from a trusted org → CONDITIONAL (wait)
  - immutable + attested GitHub release → APPROVED
  - non-notarized macOS DMG → CONDITIONAL/REJECTED
  - MS Store unpackaged Win32 app → not Tier 1 on store alone
  - fake brew.sh / ClickFix paste command → REJECTED

## 6. Evidence Log

| # | Finding | Source | Type | Conf | Notes |
|---|---|---|---|---|---|
| 1 | Files unchanged in substance since 2026-04-15 | `git log` on 6 files | Primary | H | `5c44b79` header-only |
| 2 | Rubric line citations (all §5) | the 6 files, `SKILL.md`, `references/criteria.md` | Primary | H | line numbers at HEAD `d22b53c` |
| 3 | Prior tensions (a)–(c), abandoned | 2610161852-dispatcher-rubric-consistency-plan.md / -walkthrough.md | Secondary | H | all still present |
| 4 | Eval suite valid; 12 self-tests pass; prepare OK | `evals/run_evals.py`, unittest | Primary | H | no live run |
| 5 | DCT retired; DOI DCT pulls fail from 2025-08-08 | docker.com "Retiring Docker Content Trust"; InfoQ 2025-08 | Tertiary | H | |
| 6 | KICS tag overwrite 2026-04-22; provenance-repo mismatch | docker.com blog "Trivy, KICS, and the shape of supply chain attacks so far in 2026" | Tertiary | H | vendor primary account |
| 7 | Trivy compromise 2026-03-19→23; 76/77 action tags; tap; immutable v0.35.0 safe | Snyk, Wiz GHSA-69fq-xp46-6x23, Endor CVE-2026-33634, docker.com Trivy post | Tertiary | H/M | tap detail secondary |
| 8 | DHI free/Apache-2.0 Dec 2025; SLSA L3; Rekor caveat | InfoQ 2025-12; BleepingComputer; docs.docker.com/dhi | Tertiary | H | |
| 9 | Cosign v3 bundle default; referrers | GoReleaser cosign-v3 blog; secondary posts | Tertiary | M | storage default disputed |
| 10 | Rekor v2 GA 2025-10-10 | blog.sigstore.dev/rekor-v2-ga | Tertiary | H | |
| 11 | `cosign download sbom` deprecated; attachments unsigned | sigstore/cosign doc/cosign_download_sbom.md | Tertiary | H | removal date unconfirmed |
| 12 | slsa-github-generator de-facto maintenance | third-party release note; actions/attest README | Tertiary | M | no official notice found |
| 13 | Bitnami → bitnamilegacy, no updates | Northflank, Linuxiac, Rafay (Aug–Oct 2025) | Tertiary | M-H | |
| 14 | GCR shutdown timeline | cloud.google.com Container Registry deprecation | Tertiary | H | |
| 15 | xz-backdoor Debian images on Hub | Binarly via BleepingComputer 2025-08 | Tertiary | H | |
| 16 | 10,456 images leaking secrets | Flare 2025-12-10; The Register | Tertiary | H | vendor research |
| 17 | K8s user namespaces GA v1.36 | kubernetes.io blog 2026-04-23 | Tertiary | H | |
| 18 | GitHub immutable releases GA 2025-10-28; `gh release verify` | github.blog changelog; docs.github.com | Tertiary | H | |
| 19 | Homebrew 5.0.0 quarantine/cask policy; disable 2026-09-01 | brew.sh 2025-11-12; CopyQ/PowerShell issues | Tertiary | H/M | enforcement unconfirmed |
| 20 | Homebrew bottle attestations | Trail of Bits 2024-05; Sigstore blog | Tertiary | H | default-on unconfirmed |
| 21 | Volta unmaintained → mise | volta repo issue #2080 via secondary write-ups | Tertiary | M-H | |
| 22 | nvm under OpenJS Foundation | openjsf.org 2019 | Tertiary | H | |
| 23 | Fake Homebrew / ClickFix stealers Oct 2025–May 2026 | Hunt.io, Hive Pro, Moonlock, Aviatrix, BleepingComputer | Tertiary | H | |
| 24 | curl\|sh pipe-detection divergence | javapro.io 2026-03; DEF CON 29 talk | Tertiary | M | technique, not incident |
| 25 | Sequoia removed Control-click Gatekeeper override | AppleInsider, Cult of Mac 2024 | Tertiary | H | |
| 26 | Notarized MacSync dropper; cert revoked | The Hacker News 2025-12; Jamf via BleepingComputer | Tertiary | H | |
| 27 | EV no longer instant SmartScreen rep (2024) | ToDesktop PSA; MS Tech Community | Tertiary | M | ngrok 2026-02 contradicts |
| 28 | 460-day code-signing validity from 2026-03-01 | DigiCert, GlobalSign (CSC-31) | Tertiary | H | |
| 29 | Trusted Signing → Artifact Signing | azure.microsoft.com/products/artifact-signing | Tertiary | H | date community-reported |
| 30 | Notepad++ updater hijack Jun–Dec 2025 | The Register 2026-02-02; Help Net Security; THN | Tertiary | H | |
| 31 | MS Store accepts unpackaged Win32 | learn.microsoft.com packaging overview | Tertiary | H | |
| 32 | Snap crypto-scam review changes | Phoronix 2023; GamingOnLinux 2024 | Tertiary | M | current status unknown |
| 33 | Flathub verified ≠ security review | discourse.flathub.org | Tertiary | M | community |
| 34 | Flatpak CVE-2026-34078 | tproger.ru (secondary) | Tertiary | L | verify advisory |
| 35 | Cosign keyless needs identity+issuer flags | cosign ≥2.0 behavior; Sigstore verify docs | Tertiary | H | |
| 36 | HSM/token key storage for all code-signing certs since 2023-06 | CA/B CSBR (prior knowledge) | Tertiary | M-H | not re-fetched |

## 7. Evaluation Against Criteria

| Criterion | container-image | cli-binary | desktop-app | Rationale |
|---|---|---|---|---|
| Factual currency | Weak | Weak | Weak | C2/C3; B1/B3; D1/D3/D4/D5 |
| Verdict safety | Weak | Weak | Adequate | X1/X2/C1 let KICS/Trivy-class attacks through; desktop is partly protected by OS gates |
| Internal consistency | Weak | Adequate | Adequate | C4/C6/C7 three live conflicts; B5/B6; D6/D8 |
| New-signal coverage | Weak | Weak | Weak | DHI/VEX; immutable releases/attestations; Artifact Signing/cask gate |

**Overall:** structure is sound (tiers, coverage rows, verdict notes), but the trust tables lag ~6 months and the scoring model is presence-based. A rubric refresh is warranted for all three subjects, not a no-change log entry.

## 8. Challenges and Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Identity-binding rule makes audits impractical (expected identity unknown) | Med | Med | Fallback: "identity undeterminable" = note + CONDITIONAL condition, not REJECTED |
| Cooldown rule blocks urgent security patches | Med | Med | Exempt when the new version fixes a CVE affecting the installed one and identity verifies |
| Cross-cutting edits collide with sibling plans (shared `references/criteria.md`, `SKILL.md`) | High | Med | Orchestrator sequences one X-plan first; siblings reference it |
| Facts with Conf M (EV/SmartScreen, cask enforcement, DOI signing, Flatpak CVE) encoded wrong | Med | Low-Med | Plan step: re-verify each against a primary source before writing |
| Dated specifics rot again by next cycle | High | Low | Write rules as principles + "as of" dates; keep tool versions out of scoring tables |

## 9. Findings

| ID | Subject | Finding | Severity | Conf | Plan? |
|---|---|---|---|---|---|
| X1 | all | Presence-based signature/attestation/notarization credit; no expected-identity binding | HIGH | H | Yes — cross-cutting plan |
| X2 | all | No version-age cooldown (only project age) | HIGH | H | Yes — cross-cutting plan |
| X3 | container, cli | Audit scanners/tools unpinned (Trivy compromise) | MEDIUM | H | Yes — cross-cutting plan |
| C1 | container | Semver tags treated as immutable / Tier 1 eligible | HIGH | H | Yes — container plan |
| C2 | container | DCT instructions retired, now break DOI pulls | HIGH | H | Yes — container plan |
| C3 | container | Stale cosign/SBOM/SLSA commands; `download sbom` unsigned; no `gh attestation`/BuildKit inspect | MEDIUM | H/M | Yes — container plan |
| C4 | container | DOI Tier 1 unreachable; eval 26 contradicts tiers; rootful-dev (prior b) | MEDIUM | H | Yes — after human decision |
| C5 | container | Hardened catalogs (DHI etc.) missing; DHI Rekor caveat | MEDIUM | H | Yes — container plan |
| C6 | container | CVE rule conflict (prior c); no VEX | MEDIUM | H | Yes — after human decision |
| C7 | container | Critical runtime flags graded 3 ways (prior a + shared criteria) | MEDIUM | H | Yes — container plan |
| C8 | container | Frozen namespaces (bitnamilegacy); GCR naming | LOW-MED | M-H | Fold into container plan |
| C9 | container | userns/PSS positives; digest refresh; layer secret scan | LOW | H | Fold into container plan |
| B1 | cli | Homebrew taps vs core; bottle attestation model | HIGH | M-H | Yes — cli plan |
| B2 | cli | Immutable releases + `gh release/attestation verify` missing | MEDIUM | H | Yes — cli plan |
| B3 | cli | nvm "Node.js Foundation"; Volta unmaintained in APPROVED list | MEDIUM | H/M-H | Yes — cli plan |
| B4 | cli | Install-script lures (fake brew.sh, ClickFix); inspect-the-executed-bytes | MEDIUM | H | Yes — cli plan |
| B5 | cli | Abandoned → REJECTED vs tree CONDITIONAL (prior) | LOW-MED | H | Yes — cli plan |
| B6 | cli | Verified-bytes rule vs channel (eval 30 ambiguity) | LOW-MED | H | Fold into cli plan |
| B7 | cli | `cosign verify-blob --bundle` + identity | LOW | M-H | Fold into X plan |
| D1 | desktop | Non-notarized Developer ID graded Moderate (blocked since 10.15) | MED-HIGH | H | Yes — desktop plan |
| D2 | desktop | Notarization ≠ safe; Team ID + revocation check | MEDIUM | H | Yes — via X plan + desktop |
| D3 | desktop | EV/SmartScreen, HSM, 460-day validity, Artifact Signing | MEDIUM | M/H | Yes — desktop plan |
| D4 | desktop | MS Store overcredited (unpackaged Win32, full-trust MSIX) | MEDIUM | H/M | Yes — desktop plan |
| D5 | desktop | Homebrew cask now Gatekeeper-gated; taps not | MEDIUM | H/M | Yes — desktop plan |
| D6 | desktop | Updater severity inconsistent (Medium-High vs MEDIUM); framework caveats | MEDIUM | H | Yes — desktop plan |
| D7 | desktop | Snap/Flathub legitimacy signals; Flatpak version | LOW-MED | M/L | Fold into desktop plan |
| D8 | desktop | "EXE from known vendor → CONDITIONAL" too blunt (eval 18) | LOW-MED | M | Fold into desktop plan |
| D9 | desktop | APT `signed-by` scoping | LOW | H | Fold into desktop plan |

**Opportunities:** a single "Verification identity" term in `SKILL.md` Tree terms / `references/criteria.md` would serve all 10 subjects (siblings likely hit the same issue for npm/PyPI attestations and CI actions).

## 10. Recommendations

**Primary:** don't log this pass as no-change. File these plans, in order:
1. **Cross-cutting plan** (X1, X2, X3, B7): define "verified identity" and "version cooldown" once in `references/criteria.md` + `SKILL.md` Tree terms, then reference them from each addendum. Coordinate with sibling evals before planning, since it touches shared files.
2. **Human decision** (coach/interview, short) on C4 + C6: the DOI Tier 1 path, rootful-on-dev grading, and the container CVE rule (fixable/unfixable/VEX). These are rubric policy, not facts.
3. **Container plan** (C1–C3, C5, C7–C9 + C4/C6 per decision).
4. **cli-binary plan** (B1–B6).
5. **desktop-app plan** (D1–D9).
6. **Eval-case plan** (§5.E candidates; update eval 26 description to match the C4 decision).

**Conditional:** if the orchestrator wants a minimal patch first, the safe quick fixes are C2 (remove DCT), C3's bare `cosign verify` commands, B3 (Volta/OpenJS), and D1 (non-notarized grading). These are factual corrections that need no policy decision; they could go in one patch-projex.

**Next steps:**
- Immediate: orchestrator updates `STEWARDSHIP.md` Last Reviewed = 2026-10-16 for the three rows (step 7) and the nav Phase 6 log (step 8) — not done here by mandate.
- Short-term: plans 1–6.
- Long-term: move dated tool/command specifics into a single "verification commands" reference with an "as of" date, so future passes edit one file.

## 11. Open Questions

- [ ] Has Docker shipped a DOI signing replacement (OpenPubkey/Cosign) since July 2025? No source found.
- [ ] Did Homebrew actually disable failing casks on 2026-09-01, and is bottle attestation verification on by default?
- [ ] EV SmartScreen: Microsoft primary statement on the 2024 change?
- [ ] Cosign v3 default signature storage: referrers vs. tags?
- [ ] Is the Snap crypto-wallet restriction / manual new-name review still in force?
- [ ] Cooldown length (72 h? 7 d?) and its CVE-fix exemption — policy owner?
- [ ] Should "identity undeterminable" cap at CONDITIONAL or be a note?
- [ ] CVE-2026-34078 (Flatpak) — confirm advisory and fixed version.

## 12. Appendix

**Methodology:** read all 6 files end-to-end (checklist 1–2) plus `SKILL.md` Step N, `references/criteria.md` §4.3/§4.4, prior consistency plan/walkthrough. ~35 web searches + 1 primary fetch (Docker KICS post) for Apr–Oct 2026 changes (checklist 3). Offline eval validate/prepare/self-test + manual paper trace (checklist 4). Tier: Standard-upper (3 subjects, external research, no composed projex).

**Sources consulted (external):**
- https://www.docker.com/blog/retiring-docker-content-trust/ | https://www.infoq.com/news/2025/08/docker-content-trust-retired
- https://www.docker.com/blog/trivy-kics-and-the-shape-of-supply-chain-attacks-so-far-in-2026/ | https://www.docker.com/blog/trivy-supply-chain-compromise-what-docker-hub-users-should-know/
- https://snyk.io/articles/trivy-github-actions-supply-chain-compromise/ | https://www.wiz.io/vulnerability-database/cve/ghsa-69fq-xp46-6x23 | https://www.endorlabs.com/vulnerability/cve-2026-33634
- https://www.infoq.com/news/2025/12/docker-hardened-images | https://docs.docker.com/dhi/how-to/verify
- https://blog.sigstore.dev/rekor-v2-ga/ | https://goreleaser.com/blog/cosign-v3 | https://github.com/sigstore/cosign/blob/main/doc/cosign_download_sbom.md | https://blog.sigstore.dev/cosign-verify-end-user/
- https://slsa.dev/blog/2025/11/announce-slsa-v1.2
- https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations | https://github.blog/changelog/2025-10-28-immutable-releases-are-now-generally-available/
- https://northflank.com/blog/bitnami-deprecates-free-images-migration-steps-and-alternatives | https://docs.cloud.google.com/artifact-registry/docs/transition/prepare-gcr-shutdown
- https://bleepingcomputer.com/news/security/docker-hub-still-hosts-dozens-of-linux-images-with-the-xz-backdoor | https://flare.io/learn/resources/docker-hub-secrets-exposed
- https://kubernetes.io/blog/2026/04/23/kubernetes-v1-36-userns-ga/
- https://brew.sh/2025/11/12/homebrew-5.0.0 | https://blog.trailofbits.com/2024/05/14/a-peek-into-build-provenance-for-homebrew/
- https://hunt.io/blog/fake-homebrew-clickfix-cuckoo-stealer-macos | https://moonlock.com/homebrew-ads-spreading-macsync | https://thehackernews.com/2025/12/new-macsync-macos-stealer-uses-signed.html
- https://openjsf.org/blog/openjs-foundation-welcomes-first-project-node-version-manager-nvm | https://lilting.ch/en/articles/volta-discontinued-migration-guide
- https://javapro.io/2026/03/25/curl-bash-hacked-the-unseen-dangers-in-your-dev-lifecycle/
- https://appleinsider.com/inside/macos-sequoia/tips/whats-changed-in-runtime-protection-for-macos-sequoia
- https://www.todesktop.com/blog/posts/windows-apps-psa-ev-certs-do-not-grant-immediate-reputation-anymore | https://www.digicert.com/blog/understanding-the-new-code-signing-certificate-validity-change | https://azure.microsoft.com/en-us/products/artifact-signing
- https://www.theregister.com/2026/02/02/notepad_plusplus_intrusion/ | https://www.tenable.com/plugins/container-security/413351
- https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/packaging/
- https://www.phoronix.com/news/Snap-Store-Malicious-Apps | https://gamingonlinux.com/2024/03/oh-snap-canonical-now-doing-manual-reviews-for-new-packages-due-to-scam-apps | https://discourse.flathub.org/t/security-for-unverified-flatpak-applications/6634

**Dissenting view (steel-man "keep as is"):** The rubrics are heuristics for an LLM auditor, not policy engines. Adding identity binding and cooldowns makes audits slower, and fails when vendors don't publish expected identities. Most installs are benign, and the tree's conservative default ("Unknown ≠ safe") plus live incident search would catch KICS/Trivy-class events *after* disclosure. **Counter:** the exposure windows were hours, before disclosure. Incident search finds nothing then, and presence-based scoring pushes toward APPROVED exactly when risk peaks. The fallback "identity undeterminable → note + condition" keeps the cost bounded. Several findings (C2, C3, B3, D1) are plain factual errors that no heuristic framing excuses.

**Iteration history:**

| Date | Mode | Scope | Summary |
|---|---|---|---|
| 2026-10-16 | Initial | 3 subjects, checklist 1–4 (offline) | 28 findings: 5 HIGH (X1, X2, C1, C2, B1), 1 MED-HIGH (D1); 5 plans + 1 eval plan + 1 human decision recommended |
