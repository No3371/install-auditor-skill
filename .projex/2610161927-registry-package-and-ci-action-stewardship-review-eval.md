# registry-package and ci-action stewardship review

> **Status:** Complete
> **Author:** Claude (Opus)
> **Parent:** Orchestrator
> **Subject:** `workflows/registry-package.md` + `references/criteria/registry-package.md` + `references/registries.md` | `workflows/ci-action.md` + `references/criteria/ci-action.md`
> **Type:** Gap Analysis (scheduled `STEWARDSHIP.md` review pass, checklist steps 1–3 + step 4 offline)
> **Tier:** Standard (external research-heavy; primary-source fetch blocked → WebSearch-only, see Appendix)
> **Lenses Applied:** Inversion (how would a 2026 attack pass this rubric?) | Constraint Mapping | Steel-Manning
> **Related Projex:** `2604070218-install-auditor-subject-typed-redesign-nav.md` (Phase 6 log target) | `2610161852-dispatcher-rubric-consistency-walkthrough.md` (Red Flags rewrite) | `2610161849-python-script-ports-walkthrough.md` | `2610161926-lookup-script-correctness-fixes-plan.md` (sibling; script bugs out of scope here) | `2604172000-stewardship-cadence-m63-walkthrough.md` (created STEWARDSHIP.md)

---

## 1. Executive Summary

Both rubrics were last edited April 2026. Since then the ecosystem's dominant attack pattern was **hijacked publishes of new versions of popular, provenance-bearing packages**, often by worms riding CI credentials. Examples: Shai-Hulud waves, the TanStack compromise on 2026-05-11 (84 versions with valid SLSA L3 provenance), and ChainDrop on 2026-08-04 (444 packages in <4 h). The registry-package rubric **lets exactly this pattern through**. Its Tier 1 gate rewards high adoption, package age >1 y and provenance presence, then skips install-script review. It never checks the *requested version's* age or whether provenance stayed the same across versions. Its "malware in any version → REJECTED" rule plus the dispatcher's unscoped "Confirmed supply chain attack" Red Flag would now reject chalk, debug, axios, @tanstack/* and litellm. That contradicts evals 4 and 8.

The ci-action rubric's core SHA-pinning rule held up: it was confirmed again by the trivy-action tag rewrite (2026-03-19). But the rubric misses the **cache-poisoning → OIDC-theft** chain used in the TanStack compromise. It also has no model of GitHub's new controls: immutable releases (GA), workflow lockfiles (preview 2026-10-14), and the checkout v7 refusal of untrusted fork checkouts, a fix that SHA pins do *not* inherit.

**Recommendation:** two rubric-refresh plan-projex (registry-package, ci-action) plus one eval plan. The registry plan must also touch `SKILL.md` Red Flags (compromise scoping). Total 5 HIGH, 9 MEDIUM, 7 LOW/INFO findings. No in-place edits were made.

## 2. Evaluation Scope

**Questions:** Do these rubrics reflect the ecosystems as of 2026-10-16? What is stale, missing, or wrong? Which gaps warrant a plan-projex?

| Criterion | Weight | Description |
|---|---|---|
| Verdict correctness vs current attacks | High | Would a 2025–26 real-world attack be routed and rated correctly? |
| Trust-signal accuracy | High | Are the named mechanisms real, current, and weighted right? |
| Tooling alignment | Medium | Can the scripts and commands the rubric names answer what it asks? |
| Eval consistency | Medium | Do eval expectations agree with the rubric? |
| Reference freshness | Low | URLs, versions, examples |

**Out of scope:** known script bugs (typosquat baseline query, OSV `introduced:"0"`, `.ps1` counting; see `2610161926-lookup-script-correctness-fixes-plan.md`) | other subjects (sibling evals) | editing workflow/criteria/STEWARDSHIP files | live `run_evals.py run`.

## 3. Context Analysis

- **Last edits:** registry-package criteria/workflow core from 2604-era milestones (M2.3 vuln-lookup 2026-04-10, dep-scan 2026-04-12); ci-action workflow added 2026-04-15 (m33). Today's closed work touched only the Red Flags, ci-action alignment (`2610161852-…`) and Python-first commands (`2610161849-…`).
- **STEWARDSHIP.md:** registry-package 90 d, ci-action 120 d, never reviewed. Several §Event-Based Triggers fired since April and none of them caused a review (see F-P1).
- **Constraint:** the rubric is executed by an LLM auditor at install time with web search plus 4 lookup scripts. Signals must be cheap to check.

## 4. Foundations

| Assumption (embedded in rubric) | Validity now | Risk if wrong | Flips recommendation? |
|---|---|---|---|
| Popular + old + provenance ⇒ low risk (Tier 1) | **Broken** for version-level hijacks | Quick audit approves a malicious fresh version | Yes |
| Provenance ⇒ trustworthy artifact | **Broken**: TanStack shipped valid SLSA L3 on malware | Malware gets a +1 trust | Yes |
| Install scripts run on install | **Weakening**: npm v12 / pnpm 10 block dep scripts by default | Mis-weighted risk; decision point missed | Partly |
| Any compromise in history ⇒ reject | **Over-broad** after the 2025–26 waves | Rejects much of the top-1000 | Yes |
| Tags mutable, SHA immutable ⇒ SHA is always best | Mostly holds; immutable releases and the checkout v7 backport add nuance | SHA pins go stale and miss safety fixes | No (refine) |
| Trust boundary = trigger + perms + secrets | Incomplete: shared Actions cache and runner memory | Cache-poison chain unmodelled | Yes |

**Prior work:** the subject-typed redesign (`2604070217-…-eval.md`) set the tier structure; the rubric was built around the 2024-era threat model (typosquats, malicious postinstall, maintainer takeover). That model is still valid, but the attack centre of mass has moved to **legitimate-identity, legitimate-pipeline publishes**.

## 5. Analysis

### 5.1 Registry package

**RP-1 — No version-age gate; Tier 1 waves fresh hijacked versions through.** Severity **HIGH** | Confidence H | Lens: Inversion.
- Tier 1 (`workflows/registry-package.md` §Tier 1; criteria §Tier Assignment) checks *package* first-publish >1 y and adoption. It never checks the requested or latest version's publish age. Tier 1 skips install-script review and dep-scan.
- 2025–26 incidents were almost all new versions of old, popular packages: TanStack 2026-05-11 (84 versions / 42 pkgs in 6 min); ChainDrop 2026-08-04 (444 pkgs, 2,212 versions, preinstall dropper); LiteLLM 1.82.7/1.82.8 on 2026-03-24; axios (Mar 2026); the Shai-Hulud series since 2025-09. Most were caught within hours to days.
- SKILL.md's "Brand new + no history (<72 h, no prior versions)" Red Flag is package-level only.
- Tooling already supports a fix: `scripts/registry-lookup.py` emits `publishedAt` / `daysSincePublish` for the resolved version (npm path). The rubric just never uses it.
- **Fix direction:** if the requested version is younger than N days (7 suggested), the audit cannot be Tier 1 and gets a cooldown condition. Name the client cooldown settings: npm `min-release-age` (11.10.0+; sources disagree on days vs minutes), pnpm `minimumReleaseAge` (10.16), Yarn `npmMinimalAgeGate` (4.10), Bun `minimumReleaseAge` (1.3), uv `exclude-newer` (relative since 0.9.17), pip `--uploaded-prior-to` (26.0). Unpinned requests ("npm install chalk") resolve to latest, so the age check applies to the resolved version.
- **Plan:** yes.

**RP-2 — Provenance is over-weighted and has no continuity check.** Severity **HIGH** | Confidence H | Lens: Inversion + Steel-man.
- Current rules: "+1 trust… strong positive" (criteria §Scoring impact); a Tier 1 requirement; on the APPROVED list.
- TanStack's malicious versions were published through the project's legitimate GitHub-OIDC trusted publisher and carried **valid SLSA Build L3 provenance**. Sigstore verification passed because the build really ran in the real pipeline. PyPI's own security model states that Trusted Publishing does not assert code safety.
- Steel-man for keeping it: provenance still defeats stolen-token publishes from laptops, and absence on a package that used to have it is a strong signal. So the fix is to **reframe, not remove**.
- **Fix direction:**
  - (a) Provenance proves *origin*, not *safety*: necessary-not-sufficient, never a Tier 1 shortcut on its own.
  - (b) Add **continuity** checks: same source repo and workflow as prior versions. Provenance or trusted-publisher *dropped* between versions = HIGH flag. pnpm reportedly ships a `trustPolicy: no-downgrade` setting for this (from memory, Medium; verify).
  - (c) Cross-check the publisher's release-pipeline hygiene with the ci-action lens (see CI-1): `pull_request_target` or cache use in the release repo.
- **Plan:** yes (merge with RP-5).

**RP-3 — Compromise / malware rules lack version and remediation scoping.** Severity **HIGH** | Confidence H | Lens: Inversion.
- `workflows/registry-package.md` §Toward REJECTED: "Known malware: confirmed … in any version". `SKILL.md` Red Flags: "Confirmed supply chain attack — security blog or advisory confirms compromise" (no scope).
- After the 2025–26 waves, chalk, debug, @tanstack/*, axios, litellm, mistralai, etc. all have confirmed malicious versions in their history.
- A literal reading auto-REJECTs them, which contradicts evals 4 and 8 (chalk → APPROVED / not REJECTED). Graders will see inconsistent verdicts depending on whether the auditor's web search surfaces the September 2025 incident.
- **Fix direction:** three cases.
  - (a) Malicious by design or unresolved active compromise → REJECTED.
  - (b) Legitimate package with past hijacked versions that were removed, the maintainer remediated, and the requested version is outside the bad range → not auto-REJECT. CONDITIONAL or APPROVED with conditions: pin a known-good version, check lockfiles and hosts for the exposure window, rotate credentials if it was installed.
  - (c) Requested version *is* a bad version → REJECTED + incident-response note.
- `SKILL.md` Red Flags is dispatcher-owned, so the plan must include it.
- **Plan:** yes.

**RP-4 — Install-time execution model is outdated; new vectors are missing.** Severity **HIGH** | Confidence M (npm v12 details from secondary sources).
- Client defaults have changed:
  - npm v12 (reported shipped 2026-07-08) no longer runs dependency lifecycle scripts unless they are allowlisted (`allowScripts` in package.json, `npm approve-scripts` / `npm deny-scripts`; warnings from 11.16.0).
  - `--allow-git=none` becomes the default. This flag exists because a git dependency's `.npmrc` can override the git executable even with `--ignore-scripts`. Related flags `--allow-file`, `--allow-remote` and `--allow-directory` arrived in 11.15.0.
  - pnpm 10 also blocks dependency build scripts by default (from memory, M).
  - **The real decision point is now "will the user approve scripts for this package?"** The rubric assumes scripts always run and never asks for the client or version.
- Vectors missing from §Install Script Risk Patterns:
  - `binding.gyp` → implicit `node-gyp rebuild` (June 2026 campaign, `@vapi-ai/server-sdk` start).
  - Python **`.pth` files in wheels**: run at every interpreter start, not just on import (litellm 1.82.8 `litellm_init.pth`). Strictly worse than the listed `__init__.py` MEDIUM.
  - Preinstall droppers that fetch a second-stage runtime (Bun, in ChainDrop).
  - **Persistence into IDE/agent config** (`.claude/settings.json`, `.vscode/tasks.json`) that survives uninstall (Mini Shai-Hulud).
  - A destructive dead-man switch (`rm -rf ~/` on token revocation) affects the incident-response advice order: disarm before revoking.
- **Plan:** yes.

**RP-5 — Ecosystem Trust Signals table is stale or wrong.** Severity **MEDIUM** | Confidence M–H.
- **npm:** missing trusted publishing (GA 2025-07-31). Missing staged publishing (GA 2026-05-22, CLI 11.15.0, 2FA-approved promotion; malware-scan gate before approval from 2026-09-03, secondary source). Missing the token regime: classic tokens revoked Dec 2025; write tokens default to 2FA, ≤90 d; direct publish via bypass-2FA tokens targeted to end Jan 2027.
- **PyPI:** row "PGP/Sigstore signature on sdist/wheel" is **wrong**. PyPI removed PGP signature support (2023, from memory, M). The right row is **PEP 740 attestations** (default with `pypa/gh-action-pypi-publish` + TP; 17% of 2025 uploads; >50k projects on TP). Also add: mandatory 2FA, quarantine status (litellm), and the 14-day lock on new files to old releases (Jul 2026).
- **crates.io:** TP (Jul 2025, `rust-lang/crates-io-auth-action`). **RubyGems:** TP (Dec 2023). **NuGet:** TP (Sep 2025). All missing.
- **Maven:** "PGP mandatory" still true. OSSRH sunset 2025-06-30 → Central Portal. Sigstore bundles validated but optional since Jan 2025.
- **Go:** row names `GONOSUMCHECK`. Its existence is unconfirmed (L); the well-known knobs are `GONOSUMDB`, `GOSUMDB=off`, `GOPRIVATE`, `GOINSECURE`. Wording should say sumdb proves *consistency*, not safety: boltdb-go was served from the module proxy cache for 3+ years.
- **Plan:** yes (with RP-2).

**RP-6 — `references/registries.md` contradicts the rubric and reality.** Severity **MEDIUM** | Confidence H.
- PyPI: "No mandatory publishing auth" is wrong (2FA mandatory; TP).
- Go: "High trust for modules in the index" is overstated (see RP-5).
- §CI/CD "Critical rule" (pin to SHA if `secrets.*` is used) is narrower than the `SKILL.md` Red Flag, which also covers write token, `id-token: write` and publish rights.
- The example SHA is checkout v4.2.2 under `@v4`, now several majors old. Avoid hard-coded SHAs, or label them illustrative.
- **Plan:** yes (fold into the RP plan, CI line into the CI plan).

**RP-7 — Tooling can't answer the provenance questions the rubric asks.** Severity **MEDIUM** | Confidence H (code read).
- `scripts/registry-lookup.py` emits no attestation or provenance fields (npm version `dist.attestations` / `registry.npmjs.org/-/npm/v1/attestations/<pkg>@<ver>`; PyPI integrity/provenance API).
- It emits no per-version publisher (`_npmUser`) and no trusted-publisher identity, so RP-2 continuity checks fall to unrecorded manual work.
- The consumer-side verification command `npm audit signatures` is not named anywhere.
- **Plan:** yes, as a follow-on to (not inside) `2610161926-lookup-script-correctness-fixes-plan.md`.

**RP-8 — Scorecard host moved.** Severity **LOW** | Confidence M.
- `api.securityscorecards.dev` (registry workflow §How to research; `references/criteria.md` row) → `api.scorecard.dev`. Migration was announced Mar 2024 with a 12-month dual-host window; the current redirect is unverified.
- **Plan:** no; patch-projex.

**RP-9 — Cross-ecosystem download equivalence mixes time windows.** Severity **LOW** | Confidence M.
- "1M npm weekly ~ 500K PyPI monthly ~ 100K crates.io all-time ~ 50K gems weekly" compares weekly, monthly and all-time figures. Even if the ratios are defensible, the result is hard to apply and to grade. Threshold values were not re-validated (needs live data).
- **Plan:** fold into the RP plan if convenient; otherwise no.

### 5.2 CI action

**CI-1 — Cache-poisoning → OIDC-theft trust boundary is unmodelled.** Severity **HIGH** | Confidence M–H.
- The TanStack chain: a fork PR ran in a `pull_request_target` workflow → poisoned the shared Actions (pnpm-store) cache → the release workflow restored the cache → the attacker read the OIDC token from runner memory → published via trusted publishing.
- §Trigger & Secret Exposure Matrix covers checkout of fork code but not: cache restore in privileged or release jobs; cache scope shared with lower-trust triggers; release/publish jobs with `id-token: write` as crown jewels; CI tools installed outside `uses:` (`apt install trivy` unpinned in LiteLLM's CircleCI → stolen PyPI token).
- Also add `allow-unsafe-pr-checkout: true` (checkout v7 opt-out) as a red-flag string.
- **Plan:** yes.

**CI-2 — Immutable releases (GA 2025-10-28) not modelled.** Severity **MEDIUM** | Confidence H.
- The Ref Immutability Matrix treats all tags as mutable. A tag backed by an **immutable release** cannot be moved and carries a Sigstore release attestation.
- In the trivy-action rewrite (75/76 tags force-pushed), only immutable `v0.35.0` survived. Floating majors (`v4`) are by design never immutable.
- **Fix:** a new matrix row. Immutable-release tag = moderate positive (verify the attestation); SHA is still preferred.
- **Plan:** yes.

**CI-3 — Workflow lockfiles and org pinning policies not recognised.** Severity **MEDIUM** | Confidence H.
- Public preview 2026-10-14 (GHEC only): `.github/workflows/actions.lock` via `gh actions-lock`, which pins direct **and transitive** actions and reusable workflows to SHAs, plus a "Require lockfile" policy. This directly closes the rubric's transitive-visibility gap (§Transitive Action Audit Guidance).
- Also unused: the org/enterprise "require SHA pinning" policy (Aug 2025), adopted at scale by e.g. Kubernetes (Apr 2026). Treat it as a context signal and a valid CONDITIONAL condition. Preview status: recommend it, don't require it.
- **Plan:** yes.

**CI-4 — SHA-pin freshness trade-off is ignored.** Severity **MEDIUM** | Confidence M (dates vary by source).
- checkout v7 (2026-06-18) refuses fork-PR checkout under `pull_request_target` / `workflow_run`(PR). It was backported 2026-07-16 to **floating majors only**; SHA and minor/patch pins don't get it.
- The rubric's APPROVED path (full SHA + official) never asks whether pins are updated. Stale SHA pins miss safety fixes.
- **Fix:** the APPROVED shape = SHA pin **+** update automation (Dependabot/Renovate, ideally with cooldown). Pre-fix SHAs in privileged triggers = flag.
- **Plan:** yes.

**CI-5 — Runtime deprecation check is vague.** Severity **MEDIUM** | Confidence M.
- §4.5 "Action runtime / deprecation state" names no concrete check. Node 20 was removed from runners (scheduled 2026-09-23 after several slips; Node 24 default from 2026-06-16).
- **Fix:** add a concrete check. `runs.using: node20` (or `node16`) means stale or broken; the `ACTIONS_ALLOW_USE_UNSECURE_NODE_VERSION` opt-out = flag; ARM32 / old macOS self-hosted runners are affected.
- **Plan:** fold into the CI plan.

**CI-6 — `pull_request_target` semantics changed 2025-12-08.** Severity **LOW** | Confidence H.
- The workflow file and checkout ref now always come from the default branch, so stale vulnerable workflows on other branches are no longer reachable. The trigger stays privileged.
- **Fix:** notes only; the matrix risk is unchanged.
- **Plan:** fold.

**CI-7 — Mutable-tag Red Flag re-validated.** Severity **INFO** | Confidence H.
- trivy-action/setup-trivy (2026-03-19) repeated the tj-actions pattern (2025-03). Security-tooling actions are high-value targets. No rule change needed; cite as examples.
- **Plan:** no.

**CI-8 — No static-analysis helper named.** Severity **LOW** | Confidence M.
- Workflow linters such as `zizmor` cover pwn-request, cache-poisoning and unpinned-`uses:` checks offline. They suit Tier 2/3 evidence.
- **Plan:** optional fold.

### 5.3 Evals (checklist step 4, offline)

**EV-1 — Eval 39 expects a verdict the rubric forbids.** Severity **MEDIUM** | Confidence H.
- `evals/evals.json` id 39 (docker/build-push-action; expected_output says `@v5`; no ref or permissions in the prompt) expects `exact_match APPROVED`.
- The Ref Immutability Matrix gives tag → CONDITIONAL. "Unknown/omitted" ref → treat as mutable. Eval 27 (same action `@v5`) expects CONDITIONAL.
- A rubric-correct response **fails** eval 39: a standing false-regression signal.
- **Fix:** `verdict_check [APPROVED, CONDITIONAL]` (it is a routing eval), or put a SHA in the prompt.
- **Plan:** yes (eval plan).

**EV-2 — Coverage gaps against current threats.** Severity **MEDIUM** | Confidence H.
- **ci-action:** 4 cases (14, 15, 27, 39). None cover cache poisoning, `workflow_run` artifacts, self-hosted runners, immutable-release tags, lockfiles, `allow-unsafe-pr-checkout`, or stale SHAs.
- **registry-package:** 11 cases, all npm/PyPI. None cover a fresh version of a popular package, provenance-present-but-malicious, a package with a remediated past compromise (chalk shape), `.pth`/binding.gyp, crates/NuGet/Go/IaC, or the npm v12 script-approval context.
- **Plan:** yes (eval plan; STEWARDSHIP step 6).

**EV-3 — Step 4 result: no regression signal either way.** Severity **INFO**.
- `validate` ✓ (registry-package 11, ci-action 4); `python3 -m unittest` 12/12 ✓.
- `prepare --workflow registry-package` → `iteration-1`, `prepare --workflow ci-action` → `iteration-2` in the shared `install-auditor-skill-workspace/`. Parallel siblings may interleave iteration numbers.
- `run`/`grade`/`summary` were not executed (live run not approved).

### 5.4 Process

**F-P1 — Event triggers fired without a review.** Severity **LOW** | Confidence H.
- Since April, these events all match `STEWARDSHIP.md` §Event-Based Triggers, yet none produced an out-of-cycle review: npm staged publishing, npm v12 script blocking, immutable releases, checkout v7, and workflow lockfiles.
- No watch-list of sources exists.
- **Fix:** add a short per-subject changelog watch list (GitHub changelog npm/actions tags, blog.pypi.org, Rust/RubyGems/NuGet blogs) to STEWARDSHIP.md.
- **Plan:** fold into either plan (doc-only).

## 6. Evidence Log

| # | Finding | Source | Type | Conf | Notes |
|---|---|---|---|---|---|
| 1 | Tier 1 gates on package age, not version age; Tier 1 skips install-script review | `workflows/registry-package.md` §Tier 1, §Tier-specific scope; criteria §Tier 1 | Primary | H | |
| 2 | `registry-lookup.py` emits `publishedAt`/`daysSincePublish`, no attestation fields | `scripts/registry-lookup.py` npm return dict | Primary | H | |
| 3 | TanStack 2026-05-11: 84 versions / 42 pkgs, valid SLSA L3, via legit OIDC TP; cache poisoning via `pull_request_target`; CVE-2026-45321 | Snyk, ThreatLocker, Endor Labs, SafeDep, HeroDevs (via WebSearch) | Tertiary | H | multiple concordant vendors |
| 4 | ChainDrop 2026-08-04: 444 pkgs / 2,212 versions <4 h, preinstall Bun dropper | Datadog, StepSecurity (via WebSearch) | Tertiary | M | counts vary |
| 5 | LiteLLM 1.82.7/1.82.8 2026-03-24, `.pth` payload, PyPI quarantine; Trivy-chain origin | The Register, Datadog, BoostSecurity | Tertiary | H | |
| 6 | trivy-action 75/76 tags force-pushed 2026-03-19; only immutable v0.35.0 safe | Wiz, Phoenix Security | Tertiary | M | 75/76 vs 76/77 |
| 7 | npm TP GA 2025-07-31; classic tokens revoked (Nov/Dec 2025); write tokens 2FA + 90 d | GitHub changelog 2025-07-31, 2025-09-29, 2025-11-05 | Tertiary (official) | H | |
| 8 | npm staged publishing GA 2026-05-22 (CLI 11.15.0); `--allow-file/remote/directory` | GitHub changelog 2026-05-22 | Tertiary (official) | H | URL copies with 2025 date are mislabelled |
| 9 | npm v12 (2026-07-08): dep scripts off by default, `allowScripts`, `--allow-git=none` | GitHub changelog 2026-02-18 + dev.to/ecorpit/corgea | Tertiary | M | v12 ship date secondary-only |
| 10 | npm multi-TP (≤10), malware-scan gate on staged approval (2026-09-03); bypass-2FA direct publish end Jan 2027 | refontelearning, aicybr, digitalapplied | Tertiary | L–M | not seen in primary |
| 11 | npm `min-release-age` 11.10.0; pnpm/yarn/bun/uv/pip/deno cooldown settings | mcollina gist, Simon Willison 2026-03-24 | Tertiary | M | units disagree |
| 12 | PyPI: PEP 740 final, 17% uploads attested, >50k TP projects; 14-day upload lock Jul 2026 | blog.pypi.org 2025 review; Help Net Security 2026-07-23 | Tertiary | H/M | |
| 13 | crates.io TP Jul 2025; RubyGems TP Dec 2023; NuGet TP Sep 2025 | Alpha-Omega, guides.rubygems.org, devblogs.microsoft.com | Tertiary | M | dates from roundups |
| 14 | Maven OSSRH sunset 2025-06-30; Sigstore optional, PGP retained | central.sonatype.org news 20250326, 20250128 | Tertiary (official) | H | |
| 15 | boltdb-go typosquat cached by Go proxy 3+ years | Socket via InfoWorld, heise | Tertiary | H | |
| 16 | `GONOSUMCHECK` existence unconfirmed | search found none | — | L | verify in plan |
| 17 | Immutable releases GA 2025-10-28 | GitHub changelog, docs | Tertiary (official) | H | |
| 18 | Workflow lockfiles public preview 2026-10-14, GHEC, `actions.lock`, `gh actions-lock`, Require-lockfile policy | GitHub changelog 2026-10-14, docs.github.com | Tertiary (official) | H | |
| 19 | SHA-pinning enforcement policy Aug 2025; Kubernetes mandate Apr 2026 | GitHub changelog 2025-08-15; k8s dev list | Tertiary | H | |
| 20 | checkout v7 2026-06-18 refuses fork checkout; backport to floating majors 2026-07-16, not SHA pins | GitHub changelog 2026-06-18, The Hacker News | Tertiary | M | 07-16 vs 07-20 |
| 21 | `pull_request_target` uses default-branch workflow from 2025-12-08 | GitHub changelog 2025-11-07 | Tertiary (official) | H | |
| 22 | Node 20 removal 2026-09-23, Node 24 default 2026-06-16 | GitHub changelog (multiple editions) | Tertiary (official) | M | dates slipped repeatedly |
| 23 | Scorecard API host → api.scorecard.dev | OpenSSF blog 2024-03, ossf/scorecard README | Tertiary | M | |
| 24 | Eval 39 expects APPROVED for tag/omitted ref; eval 27 CONDITIONAL for same action @v5 | `evals/evals.json` ids 27, 39 | Primary | H | |
| 25 | Evals 4/8 expect chalk ≠ REJECTED vs "malware in any version → REJECTED" | `evals/evals.json` ids 4, 8; workflow §Toward REJECTED; SKILL.md Red Flags | Primary | H | chalk 2025-09 hijack from memory (H) |
| 26 | Offline evals: validate ✓, unittest 12/12 ✓, prepare ✓ | local run | Primary | H | |

## 7. Evaluation Against Criteria

| Criterion | registry-package | ci-action | Rationale |
|---|---|---|---|
| Verdict correctness vs current attacks | **Weak** (H) | Adequate (M) | RP-1/2/3 let the dominant 2026 pattern pass or over-reject; CI misses only the cache/OIDC chain |
| Trust-signal accuracy | Weak (M) | Adequate (H) | PyPI PGP row wrong; TP missing in 3 ecosystems; CI lacks immutable releases and lockfiles |
| Tooling alignment | Weak (H) | Adequate (M) | No provenance in script output; CI has no tooling (manual by design) |
| Eval consistency | Adequate (H) | Weak (H) | chalk vs malware rule; eval 39 contradiction |
| Reference freshness | Adequate (M) | Adequate (M) | Scorecard host; checkout example; Node runtime |

**Overall:** the registry-package rubric is **materially stale** and needs a substantive refresh. The ci-action rubric is **structurally sound** but needs a targeted additive update.

## 8. Challenges and Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Version-age gate over-escalates every routine upgrade to Tier 2 | M | M (cost/latency) | Gate on age only; keep Tier 2 light; allow a documented exemption for security patches |
| Demoting provenance confuses auditors ("is it good or not?") | M | M | Phrase as "required-where-available, never sufficient"; make *drop* the strong signal |
| Compromise-scoping rule gets abused to approve risky packages | L | H | Require evidence: bad-version range removed, maintainer remediation post, requested version outside |
| npm v12 / pnpm facts mis-stated (secondary sources) | M | L–M | Plan step: verify against docs.npmjs.com before writing |
| Lockfile feature changes (preview) | M | L | Phrase as optional evidence / condition, not a requirement |
| Rubric bloat beyond the LLM's attention budget | M | M | Put new material in addenda tables; keep workflow-step deltas small |

## 9. Findings

| ID | Severity | Plan-projex? | One-line |
|---|---|---|---|
| RP-1 | HIGH | Yes (RP plan) | No requested-version age gate; Tier 1 passes fresh hijacked versions |
| RP-2 | HIGH | Yes (RP plan) | Provenance over-weighted; add continuity/drop checks |
| RP-3 | HIGH | Yes (RP plan, touches SKILL.md Red Flags) | Malware/compromise rules unscoped by version → over-reject; conflicts with evals 4/8 |
| RP-4 | HIGH | Yes (RP plan) | Script model outdated (npm v12/pnpm defaults); missing `.pth`, `binding.gyp`, dropper, IDE/agent persistence |
| CI-1 | HIGH | Yes (CI plan) | Cache-poisoning → OIDC-theft chain and non-`uses:` tool installs unmodelled |
| RP-5 | MEDIUM | Yes (with RP-2) | Trust-signal table: PyPI PGP wrong; TP missing for npm/crates/RubyGems/NuGet; Maven/Go rows stale |
| RP-6 | MEDIUM | Yes (with RP-5) | `registries.md`: PyPI auth claim wrong, Go overstated, CI rule narrower than Red Flag |
| RP-7 | MEDIUM | Yes (tooling follow-on) | Scripts don't surface attestations/publisher identity |
| CI-2 | MEDIUM | Yes (CI plan) | Immutable releases absent from ref matrix |
| CI-3 | MEDIUM | Yes (CI plan) | Workflow lockfiles + org SHA-pin policy not recognised |
| CI-4 | MEDIUM | Yes (CI plan) | SHA pins without update automation miss safety backports |
| CI-5 | MEDIUM | Fold (CI plan) | Node 20 removal: concrete runtime check |
| EV-1 | MEDIUM | Yes (eval plan) | Eval 39 expects APPROVED contrary to rubric/eval 27 |
| EV-2 | MEDIUM | Yes (eval plan) | No evals for 2026 attack shapes; ci-action only 4 cases |
| RP-8 | LOW | No — patch | Scorecard host |
| RP-9 | LOW | Fold/optional | Download-equivalence time windows mixed |
| CI-6 | LOW | Fold | `pull_request_target` default-branch semantics |
| CI-8 | LOW | Fold/optional | Name a workflow linter (zizmor) |
| F-P1 | LOW | Fold | STEWARDSHIP event triggers have no watch list |
| CI-7 | INFO | No | Mutable-tag Red Flag re-validated (trivy-action) |
| EV-3 | INFO | No | Offline step 4 clean; live run not done |

**Gaps:** version-level risk | provenance semantics | compromise lifecycle | CI cache/memory trust boundary | eval coverage for all of the above.
**Opportunities:** script data for version age already exists (cheap win); GitHub lockfiles and immutable releases give auditors new positive evidence to accept as conditions.

## 10. Recommendations

**Primary:** file three plan-projex.
1. **Registry-package rubric refresh**: RP-1–RP-6 (+RP-9 optional). Scope: `workflows/registry-package.md`, `references/criteria/registry-package.md`, `references/registries.md`, `SKILL.md` Red Flags (RP-3 wording only, coordinated with the dispatcher owner). Verify the npm v12, pnpm and PyPI-PGP facts against primary docs as step 0.
2. **ci-action rubric refresh**: CI-1–CI-6 (+CI-8 optional), `registries.md` §CI/CD line.
3. **Evals**: EV-1, EV-2; new cases tagged `workflow` per `validate`.

**Conditional:**
- If the orchestrator prefers fewer artifacts → merge plan 3 into plans 1 and 2 (STEWARDSHIP step 6 allows either).
- If RP-7 tooling work is accepted → a separate plan after `2610161926-lookup-script-correctness-fixes-plan.md` lands (same files; avoid conflicts).
- RP-8 → patch-projex any time.

**STEWARDSHIP bookkeeping (steps 7–8, not done here; edits barred):**
- On acceptance: registry-package Last Reviewed 2026-10-16, Next Due **2027-01-14** (90 d). ci-action Last Reviewed 2026-10-16, Next Due **2027-02-13** (120 d).
- Add a nav Phase 6 log line in `2604070218-install-auditor-subject-typed-redesign-nav.md` citing this eval.
- Steps 4 (live) and 6 remain open until the eval plan runs.

## 11. Open Questions

- [ ] npm v12 ship date and exact `allowScripts` semantics: confirm on docs.npmjs.com (secondary sources only).
- [ ] npm `min-release-age` unit: days or minutes?
- [ ] Does `GONOSUMCHECK` exist? (Go modules reference)
- [ ] pnpm `trustPolicy: no-downgrade`: confirm name/version.
- [ ] Is GitHub fork-scoped cache-write isolation now enforced, and since when? (secondary sources disagree)
- [ ] Does `api.securityscorecards.dev` still serve or redirect?
- [ ] Version-age threshold: 7 d vs 3 d vs ecosystem-specific? (Most 2026 waves were caught in <24 h; a 7 d norm matches the cooldown guidance cited.)
- [ ] Live eval run (step 4 proper): budget approval needed.

## 12. Appendix

**Methodology:**
- Read all 5 subject files end-to-end, plus `SKILL.md` Red Flags, `references/criteria.md` §4.1/4.3/4.7, `scripts/registry-lookup.py` (npm path) and `evals/evals.json` cases for both workflows.
- Ran offline `validate`, unittest, and `prepare` ×2.
- WebSearch: ~20 queries covering registry auth/provenance, the 2026 incident series, GitHub Actions features, and per-ecosystem TP.
- **Limitation:** WebFetch failed DNS for every host (`getaddrinfo ENOTFOUND`) and `gh` repo access was not enabled. All external facts therefore come from search-result summaries, not page reads; confidence was downgraded where only one non-official source supported a claim. Items marked "from memory" are pre-cutoff knowledge, not re-verified.

**Sources consulted (via WebSearch):**
- npm / GitHub changelogs: github.blog/changelog 2025-07-31 (npm TP GA), 2025-08-15 (Actions SHA-pin policy), 2025-09-29 & 2025-11-05 (npm tokens), 2025-10-28 (immutable releases), 2025-11-07 (`pull_request_target`), 2026-02-18 (npm bulk TP / script security), 2026-05-22 (staged publishing), 2026-06-18 (checkout v7), 2026-10-14 (workflow lockfiles), Node 20 deprecation series; docs.github.com lock-workflow-dependencies; docs.npmjs.com npm-audit, viewing-package-provenance.
- PyPI: blog.pypi.org 2025-12-31 year in review; peps.python.org/pep-0740; helpnetsecurity.com 2026-07-23.
- Other registries: central.sonatype.org news 20250326 / 20250128; guides.rubygems.org trusted-publishing; devblogs.microsoft.com NuGet TP; alpha-omega.dev crates TP.
- Incidents: snyk.io tanstack-npm-packages-compromised; endorlabs.com; safedep.io; threatlocker.com; securitylabs.datadoghq.com (npm worm, litellm); theregister.com 2026-03-24; wiz.io trivy-compromised; phoenix.security; unit42.paloaltonetworks.com; InfoWorld/heise (boltdb-go).
- Cooldowns: simonwillison.net 2026-03-24; gist mcollina; pydevtools dependency-cooldown.
- OpenSSF: openssf.org Scorecard API move post.

**Dissenting view (steel-man):** "Rubrics should stay simple; version-age gates and provenance continuity add friction an LLM auditor will apply inconsistently, and most installs are routine upgrades." Partly accepted: the recommendations keep each new check to a single field already present in script output (version age), or a single comparison (provenance present on previous version?). Rejected as a whole: the 2026 incident record shows the current simplicity routes the most common real attack straight to the Quick path.

**Iteration history:**

| Date | Mode | Scope | Summary |
|---|---|---|---|
| 2026-10-16 | Initial | registry-package + ci-action | Scheduled stewardship pass; 5 HIGH / 9 MEDIUM / 7 LOW-INFO |
