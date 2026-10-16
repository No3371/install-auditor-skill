# Shared Version-Integrity Floor

> **Status:** Ready
> **Author:** Claude (Opus)
> **Parent:** Orchestrator
> **Source:** Direct request (orchestrator): cross-subject response to 2610161927-registry-package-and-ci-action-stewardship-review-eval.md (RP-1/2/3) | 2610161927-browser-extension-ide-plugin-stewardship-review-eval.md (F1/A1/A3) | 2610161928-stewardship-review-container-cli-desktop-eval.md (X1/X2/X3, B5) | 2610161927-agent-extension-stewardship-review-eval.md (F4/F5, A9) | 2610161927-remote-integration-generic-stewardship-review-eval.md (RI-7, RI-1, G-2, G-4) | human decisions C4 + C6 (relayed by orchestrator 2026-10-16; see Revision Log)
> **Related Projex:** 2610161852-dispatcher-rubric-consistency-walkthrough.md (Red Flags + Tree terms this edits) | 2610161910-dispatcher-lean-report-and-trigger-walkthrough.md (report split; SKILL.md size budget) | 2610161926-lookup-script-correctness-fixes-plan.md (concurrent; no file overlap) | 2604070218-install-auditor-subject-typed-redesign-nav.md
> **Worktree:** Yes

---

## Summary

The five stewardship reviews of 2026-10-16 found one shared failure. Trust is scored **per subject** (adoption, badge, publisher, signature present). The 2025–26 attacks (TanStack, Nx Console, Trivy/KICS, ShadyPanda, chalk/debug, LiteLLM) are **per version**: a trusted subject ships one hijacked release, often with valid provenance or a verified badge. Each rubric's Tier 1 path approves that release. The reviews also found the reverse error: the unscoped "Confirmed supply chain attack" Red Flag and the registry workflow's "malware in any version" rule reject legitimate packages that once had a hijacked release (chalk). That contradicts evals 4 and 8.

This plan writes the rule once, as a **shared floor**: new `references/criteria.md` §4.6 *Version & Update Integrity*, sub-rules V1–V5, with named plug-in points for subject addenda. It then wires the floor into `SKILL.md` (precedence, Red Flag, coverage, skeleton), `references/report-template.md`, and the two callers that contradict it. Per-subject refresh plans fill the plug-ins later.

It also applies the human's **C6** decision to the shared CVE rule. The verdict tree's unpatched-CVE node becomes **"Blocking CVE"**: REJECTED only for a CRITICAL in CISA KEV, or an unfixed HIGH/CRITICAL in the subject's own code. Unfixed OS-package and third-party HIGH/CRITICAL become HIGH flags → CONDITIONAL, and VEX `not_affected` counts as evidence. The change covers `SKILL.md` Tree terms and `criteria.md` §4.3. Finally, it adds the hooks **C4** needs: a V1 version-unit hook and a V2 curated-pipeline hook give Docker Official Images a Tier 1 path without user-verifiable signatures.

**Scope:** `references/criteria.md` | `SKILL.md` | `references/report-template.md` | `workflows/registry-package.md` (§Toward REJECTED, 2 bullets) | `references/classifier.md` (1 bullet). No addenda, scripts, evals or `STEWARDSHIP.md`.
**Estimated Changes:** 5 files. 1 new section (~6.9 KB), §4.3 CVE mapping rewrite, plus 22 text replacements.

---

## Objective

### Problem / Gap / Need

| ID (source eval) | Gap | Shared-core fix |
|---|---|---|
| RP-1, F1/A1, X2 | No **version-age** signal. The only age rule is package-level ("Brand new + no history", < 72 h with no prior versions) | §4.6 **V1** cooldown table. Bars Tier 1; < 72 h → HIGH → CONDITIONAL |
| RP-2, X1, A3, D2 | Signatures, provenance, notarization and badges get credit when merely **present**. TanStack carried valid SLSA L3; Nx was a verified publisher; MacSync was notarized | §4.6 **V2**: credit only when matched to an expected identity; "origin, not safety"; never a Tier 1 or APPROVED basis alone |
| RP-2(b), A1, X2 (KICS) | No **continuity** check (provenance dropped, signer changed, no upstream release, permission delta) | §4.6 **V3** release-to-release diff → HIGH flags |
| RP-3 | Compromise rules not scoped by version: `SKILL.md` Red Flag "Confirmed supply chain attack" and `workflows/registry-package.md` "Known malware … in any version" / "Maintainer account compromise confirmed". Literal reading rejects chalk (evals 4, 8) | §4.6 **V4** cases a/b/c; Red Flag renamed + scoped; the 2 registry bullets scoped |
| F4/F5, RI-7, F7 | The verdict implicitly covers future updates (rug pulls, connector drift, extension auto-update). Re-audit trigger text is package-only ("major version bump or maintainer change") | §4.6 **V5** default triggers + update-control rule; skeleton/template text points to V5 |
| X3 | Auditor runs unpinned scanners (Trivy 0.69.4–0.69.6 was the malware) | "Audit tooling is itself a dependency" paragraph in `criteria.md` |
| RI-1, A9 | Canonical coverage rows are package-shaped; workflows drop Required rows | Contract: workflow tables add rows, never drop; non-applicable → `N/A (<reason>)`; T2/T3 CVE rule only with a versioned artifact |
| G-2 | `SKILL.md` confidence rule recognises only `Skipped (Tier N)`; generic's `Skipped (generic fallback)` is unrated | Confidence rule accepts workflow-defined skip reasons within a workflow-set cap |
| G-4 | Step 0 "never re-runs mid-audit" contradicts generic Phase 2 re-route | One-clause carve-out in `SKILL.md` + `classifier.md` |
| B5 (shared half) | `criteria.md` §4.2 "Abandoned → CONDITIONAL or REJECTED" vs tree "Abandoned → CONDITIONAL" | §4.2 aligned to tree |
| C6 (human decision) | Tree "Any unpatched HIGH/CRITICAL CVE → REJECTED" + §4.3 "REJECTED if unpatched". Read literally, these reject most Debian-based images over OS-package CVEs that have no distro fix, while workflows soften them inconsistently. No VEX | Tree node + term → **Blocking CVE** (KEV CRITICAL, or unfixed HIGH/CRITICAL in own code); everything else HIGH → CONDITIONAL; §4.3 table + own-code / fixed-release / KEV / VEX definitions + addendum hook |
| C4 (human decision; hooks only) | DOI Tier 1 was unreachable. With §4.6, the V2 "matched identity" rule and V1 rebuild churn would block it again | V1 version-unit hook names DOI base refreshes; V2 **Curated pipelines** hook lets an addendum accept a registry build program's attestations for Tier 1 identity |

### Success Criteria

- [ ] `references/criteria.md` has `## 4.6 Version & Update Integrity (shared floor)` with exactly 5 sub-headings `### V1`…`### V5`. Each sub-rule except the hosted-service note carries one `**Addendum:**` plug-in line.
- [ ] Every `§4.6 V<n>` reference in the 5 edited files names an existing V heading. No reference points to `§4.6 V6+`.
- [ ] `SKILL.md`: Red Flag reads "Confirmed supply chain compromise" and is version-scoped. Precedence names §4.6 as a never-downgraded floor. The Quick skeleton has a `Version integrity` row. Recommendation points to §4.6 V5. Confidence accepts workflow-defined skips. Step 0 has the generic Phase 2 carve-out.
- [ ] `SKILL.md` tree node reads `Any blocking CVE? (see Tree terms)`, with the art width unchanged (all REJECTED lines the same length). Tree term `**Blocking CVE**` states the two REJECT classes, the HIGH → CONDITIONAL rest, and VEX.
- [ ] `criteria.md` §4.3 CVE table encodes C6. It defines Own code / Third-party component, Fixed release (incl. KEV-with-fix → REJECTED + name the fix), KEV lookup and VEX `not_affected`. Its `**Addendum:**` line forbids changing the verdict classes.
- [ ] §4.6 V1 Addendum line covers the version unit for V1–V3 (DOI base refreshes named). The V2 `**Curated pipelines:**` bullet exists.
- [ ] `wc -c < SKILL.md` ≤ 15,500 (now 14,995; simulated result 15,484).
- [ ] Stale phrases gone from the 5 files (case-insensitive): `Confirmed supply chain attack` | `re-audit on major version bump or maintainer change` | `exfiltration in any version` | `CONDITIONAL or REJECTED` | `Tier-skipped checks do not count` | `if unpatched` | `Any unpatched HIGH/CRITICAL CVE` | `**Unpatched CVE**`.
- [ ] `python3 evals/run_evals.py validate` passes. `python3 -m unittest discover -s evals -p "test_*.py"` passes, with the same test count as Preflight.
- [ ] Paper traces T1–T11 (Verification Plan) produce the stated verdicts, with every rule cited by section.
- [ ] No diff outside the 5 files; `evals/evals.json` untouched.

### Out of Scope

- **Subject plug-ins.** Per-ecosystem publish-time sources, cooldown setting names (npm `min-release-age`, pnpm `minimumReleaseAge`, uv `exclude-newer` …), identity mechanisms/commands (cosign identity flags, `gh attestation verify`, Team ID, `npm audit signatures`), release-diff methods and update controls. Their facts are secondary-source and subject-specific, so they go to the per-subject plans. See Hand-off.
- **C4 subject rules** (decided: DOI pipeline + BuildKit attestations suffice for Tier 1; root on a dev workstation = LOW note, in production = CONDITIONAL; eval 26 stays APPROVED) → container plan. This plan only adds the V1/V2 hooks it needs. §4.1 "Docker Hub official images | High" row is untouched.
- **C6 subject mechanics** (container VEX sources and tooling such as Scout, DHI, `trivy --vex`; fixable/unfixable scan mechanics; the image own-code vs OS-layer boundary) → container plan, via the §4.3 Addendum hook. The other addenda's own-code boundaries → their plans.
- **Subject-specific text inside `criteria.md` §4.4** (browser permission table incl. `storage` LOW-vs-Medium; Docker `docker.sock` CRITICAL, C7). The browser and container plans own those subsections.
- `references/registries.md` (RP-6, Cursor row F11) → registry-package and ide-plugin plans.
- Scorecard host `api.securityscorecards.dev` → `api.scorecard.dev` (RP-8). The host is unverified and also appears in `scripts/registry-lookup.py` (concurrent plan's file) → separate patch-projex.
- `evals/evals.json`: no assertion becomes wrong (see Assumptions). Time-dependent effects go to the eval plan (Hand-off).
- `STEWARDSHIP.md` (concurrent plan edits it; review-date bookkeeping is the orchestrator's).
- Live `run_evals.py run`. The human decided on one paid live run, after all rubric refreshes; none in this plan.

---

## Context

### Current State

- `references/criteria.md` (11,232 B): tier intro; Audit Coverage canonical rows; §4.1 Provenance, §4.2 Maintenance, §4.3 Security, §4.4 Permissions, §4.5 Reliability, §4.7 Scorecard. **§4.6 does not exist**, so the new section fills the numbering gap. No version-level rule anywhere. Addenda open with "More-specific guidance wins" over this file.
- `SKILL.md` (14,995 B): Step 0 classifier; Step N tree + "Tree terms & precedence": Red Flags are never downgraded, and for subject-specific patterns the addendum wins. Tree node 2 is `Any unpatched HIGH/CRITICAL CVE? (see Tree terms) ──► REJECTED ❌`; its term **Unpatched CVE** = affects the version **and** no fixed release exists. Quick skeleton (Tier 1); Red Flags list.
- `criteria.md` §4.3 CVE Severity Mapping: Critical "Auto-REJECTED if unpatched"; High "REJECTED if unpatched; CONDITIONAL if patched in newer version". No own-code/component split, no KEV, no VEX. Workflows already diverge: `workflows/container-image.md` L239/L282 make "critical + known exploit" the REJECT trigger, and L309 accepts mitigated HIGHs. The registry addendum's `vuln-lookup` table makes `critical` a "REJECTED lean".
- `references/report-template.md` (2,840 B): T2/T3 skeleton; Post-Install Checklist has "Re-audit on major version bump or maintainer change".
- `workflows/registry-package.md` §Toward REJECTED (L437–451) includes the two unscoped bullets.
- `references/classifier.md` Edge-Case Discipline L121: "No re-classification mid-audit."
- `workflows/generic.md` Phase 2 (L39–42) re-routes after user clarification. L64 uses `Skipped (generic fallback)`.

### Key Files

| File | Role | Change Summary |
|---|---|---|
| `references/criteria.md` | Shared tier-aware rubric | + §4.6 V1–V5 (the contract, incl. C4 hooks); wire tier intro, tooling note, coverage row + row contract, §4.1 identity note, §4.2 abandoned, §4.3 scope note; §4.3 CVE mapping per C6 |
| `SKILL.md` | Dispatcher: tree, Red Flags, Quick skeleton | Precedence floor; Red Flag scoped; confidence skips; skeleton row + V5 pointer; Step 0 carve-out; tree node + term → Blocking CVE (C6) |
| `references/report-template.md` | T2/T3 skeleton | Version integrity row; identity-matched verify; V5 re-audit line |
| `workflows/registry-package.md` | Registry workflow | 2 §Toward REJECTED bullets version-scoped (caller migration for RP-3) |
| `references/classifier.md` | Full classifier rule | generic Phase 2 exception |

### Shared Contract (what per-subject plans build on)

| Name | Where | Plug-in point for subject plans |
|---|---|---|
| **§4.6 Version & Update Integrity (shared floor)** | `references/criteria.md` | Each addendum adds one section `## Version & Update Integrity (§4.6)` with bullets labelled `V1`–`V5`. It supplies only what each `**Addendum:**` line asks for. A missing bullet means the shared default applies |
| **V1 Version age** | §4.6 | Publish-time source; **version unit used by V1–V3** (may treat documented-pipeline rebuilds of an unchanged release, e.g. DOI base refreshes, as the same version; never new releases); client cooldown setting |
| **V2 Verified identity** | §4.6 | Identity mechanisms; expected-identity source; verify commands; whether *absence* is a flag; **curated pipelines** (registry build programs whose attestations stand in for a user-verifiable signature for Tier 1 identity: the C4 path for DOI) |
| **Blocking CVE** | `SKILL.md` Tree terms; `criteria.md` §4.3 | §4.3 `**Addendum:**` line: the own-code / third-party boundary for the artifact type, plus scan and VEX sources. Addenda **cannot** change the verdict classes |
| **V3 Continuity** | §4.6 | How to diff releases; ownership-transfer rating (≥ MEDIUM floor) |
| **V4 Version-scoped compromise** | §4.6 | Extra incident sources (OSV `MAL-`, store takedowns) |
| **V5 Updates & re-audit triggers** | §4.6 | Subject triggers; platform update controls |
| **`Version integrity` coverage row** | `criteria.md` rows table; `SKILL.md` Quick skeleton; report template | Workflow coverage tables must carry it (Required, all tiers; `N/A (hosted service)` when no versioned artifact) |
| **Floor precedence** | `SKILL.md` Tree terms → Precedence | Addenda may tighten §4.6, never loosen it. Their "More-specific guidance wins" headers do not apply to §4.6 |
| **Workflow-defined skips** | `SKILL.md` confidence; `criteria.md` row contract | A workflow may define `Skipped (<reason>)` values and a confidence cap for them (generic plan uses this for G-2) |
| **Red Flag "Confirmed supply chain compromise"** | `SKILL.md` | Version-scoped by V4. Workflows' REJECTED lists cite V4, not "any version" |

### Dependencies

- **Requires:** base `claude/youthful-dijkstra-5ov1kt` at or after `97f6bce` (the 5 eval docs committed; Red Flags/Tree terms per `5c44b79`; lean report per `d22b53c`).
- **Concurrent:** `2610161926-lookup-script-correctness-fixes-plan.md` (In Progress, branch `projex/2610161926-lookup-script-correctness-fixes`). Its files are `scripts/*`, `tests/`, `.gitignore`, `references/criteria/registry-package.md` and `STEWARDSHIP.md`. **Zero overlap** with this plan, so the two can execute in either order. If it closes first, rebase on it; no conflict expected.
- **Blocks:** the per-subject refresh plans (registry-package, ci-action, browser-extension, ide-plugin, container-image, cli-binary, desktop-app, agent-extension, remote-integration + generic) and the eval plan. All of them fill §4.6 plug-ins or assert on §4.6 behavior.

### Constraints

- `SKILL.md` ≤ 15,500 B. The lean-report plan cut it to 14,995 B and its ≤ 15,300 B check was that plan's own success criterion. This plan spends ≤ 505 B, because each byte here replaces a rule that would otherwise be repeated in 9 addenda. The result stays ≥ 1,590 B below the pre-lean 17,093 B.
- Shared text must stay ecosystem-neutral. No secondary-source product facts (version numbers, setting names, dates) go in §4.6.
- Preserve the parsed strings exactly: the verdict line, `## Audit Coverage`, `**Audit confidence (coverage):**` (`SKILL.md` Report → Shape).
- Prose only. The Source Hygiene rules don't bind `.md` docs, but no projex filenames go into shipped files.
- Markdown style per file: `SKILL.md` and `criteria.md` use long lines; `workflows/*.md` and `references/classifier.md` wrap at ~78 columns.

### Assumptions

- **A1:** Evals 4 and 8 stay correct. chalk's Sept-2025 hijack hit a bounded range of newer releases (5.6.1 from memory); 5.3.0 (2023) and today's latest are outside it. V4 case (c) gives a LOW flag, so APPROVED stays reachable. **Verify early:** OSV/GHSA lookup `chalk` shows a bounded affected range that excludes 5.3.0. If the range is unbounded, stop and report: eval 8 would then genuinely need review.
- **A2:** No eval assertion checks the Recommendation's re-audit wording, coverage row lists, or the Red Flag name. Verified at planning: no assertion contains "re-audit", and only eval 0 asserts on tier ("Tier 1 / Quick").
- **A3:** The registry addendum doesn't restate "any version" malware rules. Planning grep found `any version` only in `workflows/registry-package.md` L449; re-run it in Preflight.
- **A4:** Old strings below match exactly once in each file at base `97f6bce` (simulated at planning; all matched).
- **A5:** No CVE-bearing eval becomes wrong under C6. Eval 5 (`lodash@4.17.20`, HIGH fixed in 4.17.21) and eval 7 (`mkdirp@0.5.1`) accept `[CONDITIONAL, REJECTED]`; evals 12 (`nginx:latest`) and 38 accept `[APPROVED, CONDITIONAL]`. The new rule moves OS-package HIGHs toward CONDITIONAL, which those assertions accept. Eval 26 (redis, exact APPROVED) is consistent with C4 via the hooks.
- **A6 (reading of C6):** "REJECTED only for CRITICAL with known exploitation (CISA KEV)" carries no fixed/own-code qualifier. So a KEV-listed CRITICAL in the requested version rejects that version even when a fix exists or the CVE sits in an OS package; the Recommendation names the fixed release. A KEV-listed HIGH is not a REJECT class (HIGH flag). If the human meant otherwise, change only the Critical table cell and the Blocking CVE term.

### Impact Analysis

- **Direct:** the 5 files above.
- **Adjacent:** all 10 workflows tell the auditor to score with `references/criteria.md`, so §4.6 applies to them immediately via the Tier 1 intro bullet and the `SKILL.md` precedence. Addenda Tier 1 thresholds are now subordinate to V1–V3 bars. `workflows/generic.md`'s `Skipped (generic fallback)` now counts as a by-design skip (no cap until the generic plan sets one).
- **Downstream:** live audit verdicts change in these cases:
  - Versions < 72 h old → CONDITIONAL.
  - Versions < 7 d old, of unknown age, with a V3 break, or with a past compromise → no Tier 1. This lengthens some reports.
  - Packages with a resolved past compromise → no longer REJECTED.
  - (C6) Images and apps with unfixed OS-package or third-party HIGH/CRITICAL (not KEV) → CONDITIONAL instead of REJECTED. KEV-listed CRITICALs → REJECTED even when a fix exists (previously CONDITIONAL with an upgrade condition). The registry addendum's `vuln-lookup` "critical → REJECTED lean" is now stricter than C6 for non-KEV criticals that have a fix. §4.3's Addendum line says addenda cannot change the verdict classes, so §4.3 wins, and the registry plan aligns the text once the concurrent plan has released that file (Hand-off).
  - Evals with exact-APPROVED on unpinned subjects can flip to CONDITIONAL on dates when the latest release is < 72 h old, and eval 0's Tier 1 assertion can fail when express released < 7 d ago. This is time-dependent, not wrong; it goes to the eval plan (Hand-off).

---

## Implementation

### Overview

Preflight → write the contract (Step 1) → wire the shared rubric (Step 2) → wire the dispatcher (Step 3) → template (Step 4) → align the two contradicting callers (Step 5). Every replacement is an exact `old → new` string pair. Each old string occurs once (simulated). Use the Edit tool per pair. A miss means the base moved, so re-read that region and re-anchor; don't improvise wording.

**Preflight (worktree root = `<work-root>`):**
```bash
wc -c < SKILL.md                                    # expect 14995
python3 evals/run_evals.py validate | head -3       # expect pass
python3 -m unittest discover -s evals -p "test_*.py" 2>&1 | tail -3   # record test count
grep -rn "any version" workflows references SKILL.md                  # expect only workflows/registry-package.md (A3)
grep -n "^## 4\.\|^## Audit" references/criteria.md                   # expect no "## 4.6"
```
Verify A1 (chalk range) with `python3 scripts/vuln-lookup.py -Ecosystem npm -Name chalk -Version 5.3.0` or an OSV query. Log the result.

---

### Step 1: Add §4.6 Version & Update Integrity to `references/criteria.md`

**Objective:** write the shared contract: V1–V5, plug-in convention, hosted-service rule, and the C4 hooks (V1 version unit, V2 curated pipelines).
**Confidence:** High (wording); Medium (thresholds are policy; see Risks)
**Depends on:** Preflight
**Do-Projex:** Encouraged
**Verify-Projex:** Encouraged

**Files:** `references/criteria.md`

**Changes:** insert the block directly before `## 4.7 OpenSSF Scorecard (if available)`.

```markdown
// Before:
---

## 4.7 OpenSSF Scorecard (if available)

// After:
---

## 4.6 Version & Update Integrity (shared floor)

Applies to every subject at every tier. An audit approves one **version**: the exact release, digest, commit SHA or scope set the user will get (for an unpinned request, what it resolves to now). It does not approve later updates. These rules are a floor (`SKILL.md` Tree terms → Precedence): addenda may tighten them, never loosen them. Record the outcome in the **Version integrity** coverage row.

**Addendum plug-ins:** a `references/criteria/<type>.md` file supplies what the **Addendum:** lines below ask for, under one heading `## Version & Update Integrity (§4.6)` with bullets labelled `V1`–`V5`. No plug-in → the shared default applies.

**Hosted services** with no versioned artifact (most remote-integration subjects): V1–V3 → `N/A (hosted service)`; V4 and V5 apply.

### V1 Version age (cooldown)

Find when the version to be installed was published (registry metadata, release page, store "updated" date, image push time).

| Version age | Effect |
|---|---|
| < 72 h | HIGH flag `fresh version` → CONDITIONAL. Condition: install the previous release if it passes this audit, or wait until the version is 72 h old and re-check advisories. Tier 1 unavailable. The condition is time-bound, so this flag alone does not need the `SKILL.md` escalation notice. |
| 72 h – 7 d | Tier 1 unavailable; no flag on its own. |
| ≥ 7 d | No effect. |
| Unknown | Row `Not available (<why>)`; Tier 1 unavailable. |

- **Security-fix exemption:** a release that fixes a CVE affecting the version the user runs now → `fresh version` drops to MEDIUM if V2 verifies and V3 finds no break. Tier 1 stays unavailable.
- A subject with no prior versions at all is the `SKILL.md` Red Flag "Brand new + no history", not V1.
- **Addendum:** where the publish time comes from; the version unit V1–V3 use (it may treat automated rebuilds of an unchanged release that trace to the publisher's documented pipeline, e.g. Docker Official Images base refreshes, as the same version; never a new release); the client cooldown setting to cite in conditions.

### V2 Verified identity

Identity evidence: signatures, attestations/provenance, trusted publishing, notarization, Authenticode, verified-publisher badges.

- **Verified** = the check passed **and** the identity it names (signer subject + issuer, source repo + workflow + ref, Team ID, certificate subject, publisher account) matches the **expected identity**: the one the vendor documents, or the one prior releases carried. Record the expected identity and its source in the row.
- Evidence checked only for presence, or not matched to an expected identity → note only, no trust credit.
- Absent or undeterminable identity → no credit. Whether absence is itself a flag is the addendum's call.
- **Curated pipelines:** an addendum may name a registry-operated build program with documented review (e.g. Docker Official Images) whose own attestations stand in for a user-verifiable signature. It must say what the auditor checks instead (namespace, attestation present, pipeline source). A subject passing those checks counts as verified for the addendum's Tier 1 identity requirement; every other Tier 1 condition still applies.
- Verified identity proves **origin, not safety**: never enough on its own for APPROVED or Tier 1; never offsets another §4.6 flag or a Red Flag.
- **Addendum:** the identity mechanisms, where the expected identity is documented, and the verification commands.

### V3 Continuity with the prior release

Compare the version to be installed with the previous release:

- Identity evidence that prior releases carried is missing, or names a different signer / repo / workflow than prior releases or vendor docs → HIGH flag.
- No matching upstream source tag, release or changelog entry where the project normally publishes one → HIGH flag.
- Permission, scope, capability or tool-set increase that the changelog does not explain → HIGH flag. Explained increases → rated by the addendum.
- Publisher, maintainer or owner change since the prior release → at least MEDIUM; the addendum's ownership-transfer rules may rate it higher.
- Any V3 item → Tier 1 unavailable. Condition for a V3 HIGH: install the last release that passes V3; re-audit once the vendor explains the change.
- **Addendum:** how to diff releases (manifest permissions, MCP `tools/list`, OAuth scopes, image config) and its ownership-transfer rules.

### V4 Version-scoped compromise

**Confirmed compromise** = an advisory, security blog or vendor postmortem confirms malicious code was published under the subject's name (hijacked account, poisoned pipeline, stolen token). Cite the source and its affected range.

| Case | Rating |
|---|---|
| (a) The version to be installed is in the affected range; or no bounded range is stated; or the compromise is unresolved (bad versions still installable, no vendor remediation) | Red Flag "Confirmed supply chain compromise" → REJECTED + incident-response note |
| (b) Subject malicious by design (malware, typosquat) | Red Flags "Known malware" / "Confirmed typosquat" → REJECTED for every version |
| (c) Resolved: bad versions removed, vendor remediation published, version to be installed outside the range | LOW flag `past compromise (<range>, <date>)`; Tier 1 unavailable. Recommendation: pin the audited version; confirm lockfiles and caches do not resolve into the range |

**Incident-response note** (case a, or when the user already installed an affected version): check lockfiles, caches and hosts for the exposure window. Follow the advisory's clean-up order: some payloads destroy data when their tokens are revoked, so remove persistence first. Then rotate every credential the affected environment could reach.

- **Addendum:** extra incident sources for its ecosystem (e.g. OSV `MAL-` records, store takedown notices).

### V5 Updates & re-audit triggers

The verdict covers the audited version only. A later version is unaudited until it passes V1–V4 again.

- **Re-audit triggers (default):** new major version | publisher, maintainer or owner change (incl. acquisition) | identity change (V3) | new permissions, scopes, capabilities or tools | a confirmed incident naming the subject or its publisher.
- **Re-audit depth:** Tier 2 or deeper, diffed against the audited version.
- **Update control:** APPROVED and CONDITIONAL Recommendations name how to hold updates at the audited version where the platform allows it (exact pin, lockfile, digest, commit SHA, client cooldown, auto-update policy). Where updates cannot be held (hosted services, forced store updates), say so and list the triggers to watch.
- **Addendum:** subject triggers (e.g. ToS or sub-processor change, tool-description change) and the platform's update controls.

---

## 4.7 OpenSSF Scorecard (if available)
```

(The `---` before `## 4.6` is the existing separator after §4.5; the block ends with its own `---` so §4.7 keeps one.)

**Rationale:**
- **One floor, not nine copies.** Three reviews independently asked for this (browser eval Opportunities, container eval Rec. 1, registry eval RP-1–3), and the version unit is the only thing that differs per subject. Hence the explicit plug-in points.
- **Thresholds.** 72 h matches the existing Red Flag and catches the observed incident windows: Nx 11–36 min, Trivy 3–12 h, TanStack/ChainDrop < 24 h. 7 d is the cooldown norm the registry eval cites and bounds the Tier 1 fast path.
- **Why CONDITIONAL rather than an advisory MEDIUM.** All three reviewers asked for an enforceable cooldown condition, and a MEDIUM flag alone yields APPROVED with no condition.
- **Escalation exemption.** It keeps time-bound cooldowns from spamming "security review" notices.
- **C4 hooks.** Without them, DOI `docker pull redis` would lose Tier 1 twice:
  - V2 would deny identity credit, because DOI has no user-verifiable signature since DCT was retired.
  - V1/V3 would treat each base-layer rebuild digest as a fresh version.
  The hooks are scoped. The curated-pipeline credit only satisfies an addendum's Tier 1 identity requirement, so "origin, not safety", V1 age on real releases, CVEs and the other Tier 1 conditions still apply. A new upstream release (e.g. a new redis minor) is still a new version.
- **V4 case (c) is LOW, not MEDIUM.** Re-hijack risk is already covered by V1/V3/V5. A MEDIUM would push chalk-like packages toward cumulative CONDITIONAL for a past event that doesn't touch the audited artifact.
- **Rejected alternatives.**
  - A separate `references/version-integrity.md` file: every workflow already loads `criteria.md`, while a new file needs 10 new load instructions.
  - A `SKILL.md` section: over the byte budget, and `SKILL.md` already defers rubric detail to `criteria.md`.

**Verification:**
```bash
grep -c "^### V[1-5] " references/criteria.md          # 5
grep -c "^- \*\*Addendum:\*\*" references/criteria.md   # 5 after Step 1 (6 after Step 2 adds the §4.3 line)
grep -c "^- \*\*Curated pipelines:\*\*" references/criteria.md   # 1
grep -n "^## 4\." references/criteria.md               # 4.1 4.2 4.3 4.4 4.5 4.6 4.7 in order
```

**If this fails:** `git -C <work-root> checkout -- references/criteria.md`, then re-insert the block before the `## 4.7` heading.

---

### Step 2: Wire existing `references/criteria.md` sections to §4.6

**Objective:** make Tier 1, the coverage table, identity scoring, abandonment and supply-chain hits defer to §4.6. Add the tooling note (X3) and the coverage-row contract (RI-1/A9/G-2). Rewrite the §4.3 CVE mapping per C6 (2i, 2j).
**Confidence:** High (2a–2h); High for C6 wording, with one reading recorded as A6 (2i–2j)
**Depends on:** Step 1
**Do-Projex:** Encouraged
**Verify-Projex:** Encouraged (2i–2j encode a human policy decision)

**Files:** `references/criteria.md`

**Changes:** 10 exact replacements.

```markdown
// 2a Before (tier intro, L5):
- **Tier 1 (Quick):** Check 4.1 (provenance) and 4.3 (CVEs only). Skip deep rubric scoring — if the package is high-trust and no CVEs exist, a brief confirmation suffices.
// 2a After:
- **Tier 1 (Quick):** Check 4.1 (provenance), 4.3 (CVEs only) and 4.6 (version integrity; it can bar Tier 1 whatever the addendum's Tier 1 thresholds say). Skip deep rubric scoring — if the package is high-trust, no CVEs exist and §4.6 raises nothing, a brief confirmation suffices.

// 2b Before (end of L9 script paragraph):
this applies to every script named below.
// 2b After (same line, then new paragraph):
this applies to every script named below.

**Audit tooling is itself a dependency.** Third-party tools a workflow tells you to run (image scanners, SBOM generators, signature verifiers) can be hijacked like any installable. Use a release outside any known-compromised range whose identity verifies per §4.6 V2, and record tool + version in the coverage row's notes. If you cannot verify the tool, use registry- or vendor-side scan data instead and say so in the row. The bundled `scripts/` are stdlib-only and need no extra install.

// 2c Before (rows table):
| CVE / advisories (requested version) | Required | Required | Required | OSV, GHSA, registry advisory APIs — **critical** for T2/T3 |
// 2c After:
| CVE / advisories (requested version) | Required | Required | Required | OSV, GHSA, registry advisory APIs — **critical** for T2/T3 |
| Version integrity (§4.6) | Required | Required | Required | Version age, identity, continuity, compromise scope; `N/A (hosted service)` when no versioned artifact |

// 2d Before (Tier 1 row-set sentence fragment):
typically registry/metadata, typosquat, CVE/advisories, license, plus
// 2d After:
typically registry/metadata, typosquat, CVE/advisories, license, version integrity, plus

// 2e Before:
**Containers / images:** Include image configuration checks (user, capabilities) under permissions or as extra rows.
// 2e After:
**Containers / images:** Include image configuration checks (user, capabilities) under permissions or as extra rows.

**Workflow coverage tables** add subject rows to this table; they never drop a Required row. A Required row that cannot apply stays as `N/A (<reason>)` (e.g. `CVE / advisories — N/A (hosted service, no versioned artifact)`); the Tier 2/3 CVE rule under Critical checks applies only when a versioned artifact exists. A workflow may define its own `Skipped (<reason>)` values and cap Audit confidence for them (`SKILL.md` Step N).

// 2f Before (last row of §4.1 Publisher Verification table):
| No source code available | Very Low |
// 2f After:
| No source code available | Very Low |

Badges, verified-publisher status and signatures establish **identity**, not code integrity: credit them only per §4.6 V2, never against a §4.6 flag.

// 2g Before (§4.2):
**Score < -1 → Flag as Stale. Score < -2 → Flag as Abandoned → CONDITIONAL or REJECTED.**
// 2g After:
**Score < -1 → Flag as Stale. Score < -2 → Flag as Abandoned → CONDITIONAL** (`SKILL.md` tree: abandoned with no alternative). Abandonment reaches REJECTED only together with another REJECTED trigger (a `SKILL.md` Blocking CVE, §4.6 V4 case a).

// 2h Before (§4.3 Supply Chain Indicators, last bullet):
- "removed from npm/PyPI" + reason
// 2h After:
- "removed from npm/PyPI" + reason

Rate a confirmed hit by version scope per §4.6 V4: REJECTED only when the version to be installed is affected or the compromise is unresolved.

// 2i Before (§4.3 CVE Severity Mapping, table head + first two rows; heading line above stays):
| CVSS Score | Severity | Verdict Impact |
|---|---|---|
| 9.0–10.0 | Critical | Auto-REJECTED if unpatched |
| 7.0–8.9 | High | REJECTED if unpatched; CONDITIONAL if patched in newer version |
// 2i After (Medium and Low rows below stay unchanged):
`SKILL.md` "Blocking CVE" = the REJECTED cells below. Rate only CVEs that affect the version to be installed.

| CVSS Score | Severity | Verdict Impact |
|---|---|---|
| 9.0–10.0 | Critical | Listed in CISA KEV → REJECTED. Otherwise: in own code with no fixed release → REJECTED; else HIGH flag → CONDITIONAL |
| 7.0–8.9 | High | In own code with no fixed release → REJECTED; else (fixed release exists, or third-party component) HIGH flag → CONDITIONAL |

// 2j Before (line after the table):
**Always check:** Is the CVE in the version being requested, or only in older versions? If user is installing an old pinned version that has known CVEs, escalate.
// 2j After (same line kept, then a blank line and the definitions):
**Always check:** Is the CVE in the version being requested, or only in older versions? If user is installing an old pinned version that has known CVEs, escalate.

- **Own code** = what the subject's publisher writes and ships (the package, binary, extension, action or app itself, incl. components it forks and maintains). **Third-party component** = OS packages, base-image layers, bundled or transitive dependencies.
- **Fixed release** = a published version that removes the CVE. When one exists, the condition is: install it (and audit that version). A KEV-listed CRITICAL rejects the requested version even when a fix exists; the Recommendation names the fixed release. Third-party component with no fix → condition: the routed workflow's mitigations, plus re-audit when a fix ships.
- **KEV:** check each CRITICAL against the CISA Known Exploited Vulnerabilities catalog; record the result in the CVE row. If the catalog is unreachable, search for in-the-wild exploitation; credible reports count as listed.
- **VEX:** a `not_affected` statement (OpenVEX, CSAF or CycloneDX VEX) counts as evidence that the CVE does not apply if it names this version, gives a justification, and comes from the subject's publisher or the component's maintainer. Record source + justification in the CVE row and leave the CVE out of the rating. For a signed statement, check the signer per §4.6 V2. `affected` / `under_investigation` change nothing.
- **Addendum:** draws the own-code / third-party line for its artifact type and names its scan and VEX sources. It does not change the verdict classes above.
```

**Rationale:**
- 2a is the hook that makes §4.6 bind every workflow's tier triage without editing 10 workflows.
- 2e answers RI-1/A9/G-2 once. It restates the existing "do not omit tier-required rows" rule and adds the `N/A` path and workflow-defined skips.
- 2g fixes the shared half of B5. The cli-binary workflow line is left to the cli plan.
- 2b (X3) sits with the other tooling guidance at the top of the file, not in §4.6, because it governs the auditor's tools, not the subject.
- **2i/2j (C6)** follow the human's decision verbatim. The REJECT classes are (1) a CRITICAL in CISA KEV and (2) an unfixed HIGH/CRITICAL in own code; everything else HIGH/CRITICAL → HIGH flag → CONDITIONAL; VEX `not_affected` = evidence.
  - **Own code vs third-party is defined generically.** The decision names OS packages, and "only" excludes every other non-own-code case too, which covers bundled and transitive deps. Addenda draw the concrete line.
  - **VEX source restriction.** Statements must come from the publisher or the component maintainer, with a justification. This stops an arbitrary third party from waiving a CVE.
  - **KEV fallback.** If the catalog is unreachable, credible exploitation reports count as listed, keeping "Unknown ≠ safe".
  - The table keeps CVSS bands, so the Medium and Low rows and the tree's "medium CVEs → CONDITIONAL" node are untouched.

**Verification:** each `After` string present once (`grep -cF`); `grep -ci "CONDITIONAL or REJECTED\|if unpatched" references/criteria.md` → 0; `grep -c "^- \*\*Addendum:\*\*" references/criteria.md` → 6; `wc -c references/criteria.md` ≈ 21,455 (± 50).

**If this fails:** revert the file to its post-Step-1 state (`git -C <work-root> diff references/criteria.md` to inspect, or re-checkout and redo Step 1).

---

### Step 3: Wire `SKILL.md` (precedence, Red Flag, coverage, skeleton, Step 0)

**Objective:** make the dispatcher name §4.6 as a never-downgraded floor and scope the compromise Red Flag. Accept workflow-defined skips, add the skeleton row and V5 pointer, and carve out generic Phase 2. Replace the unpatched-CVE node and term with **Blocking CVE** (C6). Stay ≤ 15,500 B.
**Confidence:** High
**Depends on:** Steps 1–2 (references must resolve)
**Verify-Projex:** Encouraged

**Files:** `SKILL.md`

**Changes:** 9 exact replacements (simulated result 15,484 B).

```markdown
// 3a Before (Step 0, end of "User override" paragraph):
Classification is read-only and never re-runs mid-audit.
// 3a After:
Classification is read-only and never re-runs mid-audit (sole exception: `workflows/generic.md` Phase 2).

// 3b Before (Tree terms):
- **Precedence** — Red Flags are subject-independent and are never downgraded. For subject-specific patterns (Dockerfile instructions, ref pinning, permission scopes, documented exceptions) the routed workflow and its criteria addendum win over generic wording here or in `references/criteria.md`.
// 3b After:
- **Precedence** — Red Flags and the version-integrity floor in `references/criteria.md` §4.6 (it can bar Tier 1) are subject-independent and never downgraded; addenda only tighten §4.6 or fill its plug-ins. For other subject-specific patterns (Dockerfile instructions, ref pinning, permission scopes, documented exceptions) the routed workflow and its criteria addendum win over generic wording here or in `references/criteria.md`.

// 3c Before (Coverage gaps):
(failed API / 404 / timeout — **not** tier-skipped, **not** `N/A`), add a sentence to Recommendation that the audit has **reduced coverage**. Do **not** change the verdict label for coverage alone — the verdict still follows the tree above. Tier-skipped checks do not count toward this threshold.
// 3c After:
(failed API / 404 / timeout — **not** `Skipped`, **not** `N/A`), add a sentence to Recommendation that the audit has **reduced coverage**. Do **not** change the verdict label for coverage alone — the verdict still follows the tree above.

// 3d Before (Audit confidence, High):
legitimately **N/A**, or **Skipped (Tier N)** by design;
// 3d After:
legitimately **N/A**, or **Skipped** by design (`Skipped (Tier N)` or a workflow-defined reason, within its confidence cap);

// 3e Before (Quick skeleton table):
| License compatibility | Done | SPDX — Compatible |
// 3e After:
| License compatibility | Done | SPDX — Compatible |
| Version integrity | Done | §4.6: published <date>; identity <match / none> |

// 3f Before (Quick skeleton Recommendation):
pin to <package>@<version>; re-audit on major version bump or maintainer change.>
// 3f After:
pin to <package>@<version>; re-audit on any `references/criteria.md` §4.6 V5 trigger.>

// 3g Before (Red Flags):
- **Confirmed supply chain attack** — security blog or advisory confirms compromise
// 3g After:
- **Confirmed supply chain compromise** — advisory or vendor confirms malicious code in the version to be installed, or the affected range is unknown, or the compromise is unresolved (`references/criteria.md` §4.6 V4)

// 3h Before (verdict tree, node 2; ─ is U+2500, ► U+25BA):
Any unpatched HIGH/CRITICAL CVE? (see Tree terms) ──► REJECTED ❌
// 3h After (17 × ─ then ►; line stays 64 characters like the other REJECTED nodes):
Any blocking CVE? (see Tree terms) ─────────────────► REJECTED ❌

// 3i Before (Tree terms):
- **Unpatched CVE** — affects the version to be installed **and** no fixed release exists (`references/criteria.md` §4.3 CVE Severity Mapping). A CVE fixed in a newer release does not trigger this node; rate it per the routed workflow (typically HIGH → CONDITIONAL with an upgrade condition).
// 3i After:
- **Blocking CVE** — affects the version to be installed and is CRITICAL in CISA KEV, or HIGH/CRITICAL in the subject's own code with no fixed release. Any other HIGH/CRITICAL CVE (fixed upstream, or in an OS package / third-party component) is a HIGH flag → CONDITIONAL; VEX `not_affected` is evidence (`references/criteria.md` §4.3).
```

**Rationale:**
- **3g.** V4 states that a resolved past compromise isn't auto-rejected, so the Red Flag only points there (byte budget). The renamed Red Flag now matches the tree node text "Confirmed supply chain compromise?", so node 3 and the Red Flag read as one rule and the tree art needs no change.
- **3b.** Without it, addenda headers ("More-specific guidance wins") would let subject Tier 1 thresholds override V1–V3.
- **3c.** Drops a sentence that duplicated "not tier-skipped" (−~60 B) and generalises to any by-design skip, consistent with 3d.
- **3d.** Gives the generic plan (G-2) a sanctioned skip vocabulary; that plan sets the cap.
- **3a.** Takes the shortest wording that removes the G-4 contradiction.
- **3h/3i (C6).** "Blocking CVE" replaces "Unpatched CVE" because a KEV CRITICAL now blocks even when a fix exists, so "unpatched" would mislead. The node keeps the tree's fixed-width art. The term carries the whole decision in one line; §4.3 holds the definitions.
- **Byte budget.** Every clause was shortened in simulation: 15,595 → 15,460 B before C6, then 15,484 B with 3h/3i and the shortened 3g. That leaves 16 B of headroom.

**Verification:**
```bash
wc -c < SKILL.md                                   # ≤ 15500 (expect 15484)
grep -c "Confirmed supply chain attack\|Unpatched CVE\|unpatched HIGH/CRITICAL" SKILL.md   # 0
grep -c "§4.6" SKILL.md                            # 4  (3b, 3e, 3f, 3g)
grep -c "Blocking CVE\|blocking CVE" SKILL.md      # 2  (3h, 3i)
python3 -c "import re;L=[l for l in open('SKILL.md',encoding='utf-8').read().splitlines() if l.endswith('REJECTED ❌')];print(sorted({len(l) for l in L}))"   # [64]
grep -c "## Audit Coverage\|\*\*Audit confidence (coverage):\*\*\|\*\*Verdict: \[APPROVED" SKILL.md  # unchanged vs Preflight
```

**If this fails:** `git -C <work-root> checkout -- SKILL.md` and redo. If the size is over budget (e.g. the base moved), trim in this order before touching any other wording:
1. 3i: drop "; VEX `not_affected` is evidence" (−~40 B; §4.3 still carries it).
2. 3a: "(sole exception: `workflows/generic.md` Phase 2)" → "(except `workflows/generic.md` Phase 2)" (−~10 B).

---

### Step 4: Update `references/report-template.md`

**Objective:** T2/T3 skeleton carries the Version integrity row, identity-matched verification and V5 re-audit.
**Confidence:** High
**Depends on:** Step 1
**Do-Projex:** Encouraged

**Files:** `references/report-template.md`

**Changes:** 3 exact replacements.

```markdown
// 4a Before (coverage example table):
| CVE / advisories | Done, 0 results | OSV, GHSA |
// 4a After:
| CVE / advisories | Done, 0 results | OSV, GHSA |
| Version integrity | Done | §4.6: published <date> (<age>); identity matches <expected identity, source> |

// 4b Before (Post-Install Checklist):
- [ ] Verify checksum/signature if provided
// 4b After:
- [ ] Verify checksum/signature against the expected identity (`references/criteria.md` §4.6 V2)

// 4c Before:
- [ ] Re-audit on major version bump or maintainer change
// 4c After:
- [ ] Hold updates at the audited version where possible; re-audit on any `references/criteria.md` §4.6 V5 trigger
```

**Rationale:** the template is the T2/T3 equivalent of the Quick skeleton, so the same row and pointer keep both shapes consistent (the G-2 report-template gap). Parsed lines are untouched.

**Verification:** `grep -ci "re-audit on major version bump" references/report-template.md` → 0; `grep -c "§4.6" references/report-template.md` → 3.

**If this fails:** `git -C <work-root> checkout -- references/report-template.md`.

---

### Step 5: Align the contradicting callers (`workflows/registry-package.md`, `references/classifier.md`)

**Objective:** remove the two rules that would still override §4.6 V4 (RP-3: evals 4/8) and the classifier line that contradicts generic Phase 2 (G-4).
**Confidence:** High
**Depends on:** Steps 1, 3
**Verify-Projex:** Encouraged

**Files:** `workflows/registry-package.md` | `references/classifier.md`

**Changes:** 3 exact replacements; wrap at ~78 columns like the surrounding text.

```markdown
// 5a Before (workflows/registry-package.md §Toward REJECTED):
- **Maintainer account compromise confirmed**: Security advisory or blog post
  confirms the maintainer account was hijacked
// 5a After:
- **Maintainer account compromise confirmed**: Security advisory or blog post
  confirms the account was hijacked **and** the requested version is in the
  affected range, no bounded range is stated, or the compromise is unresolved
  (`references/criteria.md` §4.6 V4; a resolved past hijack is a LOW flag)

// 5b Before:
- **Known malware**: Confirmed cryptominer, credential stealer, or data
  exfiltration in any version
// 5b After:
- **Known malware**: Package malicious by design (cryptominer, credential
  stealer, data exfiltration). Malicious versions of a legitimate package are
  rated by version scope per `references/criteria.md` §4.6 V4

// 5c Before (references/classifier.md Edge-Case Discipline):
- **No re-classification mid-audit.** Once routed, the workflow owns the audit.
// 5c After:
- **No re-classification mid-audit.** Once routed, the workflow owns the audit.
  Sole exception: `workflows/generic.md` Phase 2 re-routes after the user
  confirms the type.
```

**Rationale:** under `SKILL.md` precedence the routed workflow wins on subject patterns. Leaving 5a/5b in place would keep the chalk over-rejection even after the Red Flag fix. These are the only "any version" or unscoped hijack rules found (Preflight grep re-checks). All other registry-package findings (RP-1/2/4–9) stay with the registry plan, which fills plug-ins rather than rewriting these bullets.

**Verification:** `grep -c "exfiltration in any version" workflows/registry-package.md` → 0; `grep -c "§4.6 V4" workflows/registry-package.md` → 2; `grep -c "Sole exception" references/classifier.md` → 1.

**If this fails:** `git -C <work-root> checkout -- workflows/registry-package.md references/classifier.md`.

---

## Verification Plan

### Automated Checks

- [ ] Harness: `python3 evals/run_evals.py validate` passes; `python3 -m unittest discover -s evals -p "test_*.py"` passes with the Preflight test count.
- [ ] Consistency script (run from `<work-root>`; not committed):
```bash
python3 - <<'EOF'
import re, pathlib
F = ["SKILL.md","references/criteria.md","references/report-template.md","workflows/registry-package.md","references/classifier.md"]
T = {f: pathlib.Path(f).read_text(encoding="utf-8") for f in F}
crit, skill = T["references/criteria.md"], T["SKILL.md"]
heads = set(re.findall(r"^### (V[1-5]) ", crit, re.M))
assert heads == {"V1","V2","V3","V4","V5"}, heads
assert "## 4.6 Version & Update Integrity (shared floor)" in crit
for f, t in T.items():
    for v in re.findall(r"§4\.6 (V\d)", t):
        assert v in heads, (f, v)
for f, t in T.items():
    low = t.lower()
    for bad in ["confirmed supply chain attack", "re-audit on major version bump or maintainer change",
                "exfiltration in any version", "conditional or rejected", "tier-skipped checks do not count",
                "if unpatched", "any unpatched high/critical cve", "**unpatched cve**"]:
        assert bad not in low, (f, bad)
assert len(pathlib.Path("SKILL.md").read_bytes()) <= 15500
assert "- **Blocking CVE**" in skill and "Any blocking CVE? (see Tree terms)" in skill
assert "Blocking CVE" in crit and "CISA KEV" in crit and "`not_affected`" in crit and "**Curated pipelines:**" in crit
assert len({len(l) for l in skill.splitlines() if l.endswith("REJECTED ❌")}) == 1   # tree art width intact
for s in ["## Audit Coverage", "**Audit confidence (coverage):**", "**Verdict: [APPROVED"]:
    assert s in skill and s in T["references/report-template.md"], s
assert "| Version integrity |" in skill and "| Version integrity |" in T["references/report-template.md"]
print("OK")
EOF
```
- [ ] `git -C <work-root> diff --stat <base>..HEAD` lists exactly the 5 files.

### Manual Verification (paper traces)

Walk each case through `SKILL.md` Step N + §4.6. Record the cited rule per hop in the execution log.

| # | Case | Expected |
|---|---|---|
| T1 | eval 8: `chalk@5.3.0` (2023; resolved 2025 hijack in a newer range) | V1 no effect; V4 (c) LOW; Tier 2 (Tier 1 barred by V4 c); 5a/5b don't fire → **APPROVED reachable** (eval 8 exact-APPROVED, eval 4 ✓) |
| T2 | TanStack-style: popular npm pkg, requested version 6 h old, valid SLSA provenance from the real pipeline | V1 HIGH `fresh version`; V2 verified but "origin, not safety" → no offset; Tier 1 barred → **CONDITIONAL** (cooldown condition; no escalation notice for this flag alone) |
| T3 | Nx Console-style: verified VS Code publisher, version minutes old, no matching upstream tag | V1 HIGH + V3 HIGH → **CONDITIONAL** with escalation notice (V3 HIGH isn't exempt); condition: last release passing V3 |
| T4 | User requests exactly a version listed in a malware advisory's affected range | V4 (a) → Red Flag → **REJECTED** + incident-response note |
| T5 | KICS-style: container tag repointed, provenance names a repo created yesterday | V2 mismatch → no credit; V3 HIGH (different repo) → ≥ **CONDITIONAL**; container plug-ins may tighten |
| T6 | SaaS OAuth connector (eval 24 shape) | V1–V3 `N/A (hosted service)`; V5: Recommendation says updates can't be held and lists triggers; verdict unchanged |
| T7 | Debian-based image, unfixed OS-package HIGH (not KEV), nothing else | §4.3: third-party component → HIGH flag → **CONDITIONAL** (mitigations + re-audit on fix). Not REJECTED (C6) |
| T8 | eval 5: `lodash@4.17.20`, HIGH in own code fixed in 4.17.21, not KEV | HIGH flag → **CONDITIONAL**, condition: install 4.17.21 (eval 5 accepts) |
| T9 | Own-code CRITICAL in the requested version, listed in CISA KEV, fixed in the next release | Blocking CVE → **REJECTED**; Recommendation names the fixed release to audit instead (A6 reading) |
| T10 | OS-package CRITICAL, KEV-listed, with publisher VEX `not_affected` + justification naming this image version | VEX = evidence → CVE left out of the rating; note in CVE row → not REJECTED on this CVE |
| T11 | eval 26: `docker pull redis` (DOI), dev, no new upstream release in 7 d, last base refresh 1 d ago | V1: the refresh is the same version unit (hook; container plan supplies the plug-in); V2: curated-pipeline hook can satisfy the Tier 1 identity requirement → **Tier 1 path open; APPROVED reachable** (C4). The rootful-dev LOW note comes from the container plan |

### Acceptance Criteria Validation

| Criterion | How to Verify | Expected Result |
|---|---|---|
| §4.6 with V1–V5 + 5 plug-in lines | Step 1 greps; consistency script | 5 / 5; `OK` |
| References resolve | consistency script | `OK` |
| `SKILL.md` wiring + size | Step 3 greps; `wc -c` | 0 stale; 4 × §4.6; ≤ 15,500 |
| Stale phrases gone | consistency script | `OK` |
| Harness green | validate + unittest | pass; same count |
| C6 encoded | Step 2/3 greps; consistency script; T7–T10 | `OK`; traces match |
| C4 not blocked | T11 | Tier 1 path open with hooks |
| Paper traces | execution log T1–T11 | match table |
| Only 5 files changed; evals untouched | `git diff --stat` | 5 files |

---

## Rollback Plan

1. Before close: `projex-abandon.sh <repo-root> claude/youthful-dijkstra-5ov1kt projex/2610161941-shared-version-integrity-floor --worktree`. Base is untouched.
2. After squash-close: `git -C <repo-root> revert <squash-sha>` (single commit; touches only the 5 files). Per-subject plans that already filled §4.6 plug-ins must be reverted first, or their plug-ins left as inert headings.

---

## Hand-off: per-subject findings deliberately left to per-subject plans

All refresh plans are planned and executed in this session (human decision). The single paid live eval run happens only after all of them close.

| Plan | Findings left (plug-ins to fill in **bold**) |
|---|---|
| registry-package | **C6 alignment:** the `vuln-lookup` "Risk level → verdict impact" table (`critical` = "REJECTED lean") and `workflows/registry-package.md` "Unpatched CRITICAL/HIGH CVE" bullet must match §4.3 (KEV / own code; `dep-scan` transitive hits = third-party component → HIGH flag). Edit the addendum only after 2610161926 closes. **§4.3 plug-in:** own-code line for packages · **V1** npm/pnpm/Yarn/Bun/uv/pip cooldown settings + `registry-lookup` `daysSincePublish` source (RP-1) · **V2** trusted-publishing/PEP 740/`npm audit signatures`, pnpm `trustPolicy` (RP-2a/b, RP-5) · **V3** provenance-drop / `_npmUser` diff (RP-2b) · RP-2c release-pipeline hygiene · RP-4 script model (npm v12, `.pth`, `binding.gyp`, droppers, IDE/agent persistence; incident-response order now generic in V4) · RP-5/RP-6 trust tables + `references/registries.md` · RP-7 tooling (after 2610161926) · RP-9 |
| ci-action | CI-1 cache-poisoning/OIDC chain · CI-2 immutable releases (**V2/V3** plug-ins) · CI-3 lockfiles/org pin policy (**V5** update controls) · CI-4 SHA-pin freshness (**V5**) · CI-5/6/8 · EV-1 eval 39 |
| browser-extension / ide-plugin | **V1** store "updated" dates; **V2** badge semantics (A3: Edge "Featured", CWS Established Publisher, JetBrains verified ≠ review); **V3** permission/`extensionPack` diff; **V5** `extensions.allowed`, update delay, enterprise policy (F7) · A2 MV2 · A4 Open VSX forks + `registries.md` Cursor row (F11) · A5 permission table + `criteria.md` §4.4 browser table incl. `storage` LOW/Medium (F11) · A6 AI surface · F10 evals |
| container-image | **C4 (decided):** DOI pipeline + BuildKit attestations suffice for Tier 1. Use the **V2 curated-pipeline** plug-in (name DOI; what to check: `library/` namespace, BuildKit provenance/SBOM via `docker buildx imagetools inspect`, docker-library source) and the **V1 version-unit** plug-in (DOI base refreshes = same version). Root on a dev workstation = LOW note; in production = CONDITIONAL. Eval 26 stays APPROVED; align its description only if it contradicts the new text · **C6 (subject part):** the **§4.3 plug-in**: image own code vs OS/base layers; VEX and scan sources (Docker Scout, DHI VEX, `trivy --vex`, Grype); fixable/unfixable mechanics; align `workflows/container-image.md` L239/L282/L309 and addendum L189 to Blocking CVE · **V2** cosign identity flags, `gh attestation`, DHI Rekor caveat (X1, C3, C5) · C1 tag immutability · C2 DCT removal · C7 incl. `criteria.md` §4.4 Docker lines · C8/C9 · **X3 pinned scanners** (cite the criteria tooling note) |
| cli-binary | **V2** `cosign verify-blob --bundle` + identity (B7), `gh release verify` (B2) · B1 taps vs core · B3 · B4 lures / executed-bytes rule · B5 `workflows/cli-binary.md` L242 abandoned line (shared half done here) · B6 |
| desktop-app | **V2** Team ID / Authenticode subject + revocation check (X1, D2) · D1, D3–D9 |
| agent-extension | **V3** `tools/list` + tool-description diff; **V5** tool-set change trigger + `npx -y` unpinned rule (F4/F5 subject parts) · tool poisoning / shadowing / trifecta / config hijack (F5) · transports/OAuth (F4) · F6 channels · A9/E5 coverage table must now carry the canonical Required rows (contract in `criteria.md` 2e) |
| remote-integration + generic | **V5** ToS/sub-processor/connector-drift triggers (RI-7) · RI-1 subject coverage rows (contract 2e) · RI-2..RI-6, RI-8..RI-10 · G-1, G-3 · **G-2** generic's tier/shape + confidence cap (vocabulary sanctioned in 3d/2e) |
| eval plan | Time-dependent V1 effects on exact-APPROVED evals with unpinned subjects (0, 11, 16, 18, 20, 22, 36, 37). rust-analyzer (37) ships weekly, so it is often < 72 h. Options: pin versions in prompts, or accept `[APPROVED, CONDITIONAL]` where the only condition is cooldown. Eval 0's Tier 1 assertion is barred when express is < 7 d old. New cases: fresh version, provenance-valid-but-malicious, chalk-shape past compromise, V3 identity drop |
| cli-binary / desktop-app / ide-plugin / browser-extension | **§4.3 plug-in:** own-code line for bundled runtimes and libs (e.g. Electron/Chromium, bundled LSP binaries) |
| tooling follow-on (optional) | KEV lookup in `scripts/vuln-lookup.*` (flag CRITICALs listed in the CISA catalog); same timing constraint as RP-7 |
| patch | RP-8 Scorecard host (`criteria.md` ×2, `workflows/registry-package.md`, `scripts/registry-lookup.py`), once the host is verified |
| STEWARDSHIP (orchestrator) | Last Reviewed dates; F-P1 watch list; optionally list `references/criteria.md` §4.6 as a shared row reviewed with any subject pass |

---

## Notes

### Risks

- **Thresholds are policy (72 h / 7 d).** A human may want different numbers. Mitigation: all numbers live in the V1 table only; retuning is a one-table edit.
- **Run-to-run verdict variance from V1.** Live evals and audits of fast-release subjects flip with the calendar. Mitigation: hand-off to the eval plan; the Recommendation states the date the cooldown ends.
- **Read cost.** `criteria.md` grows +8.0 KB (~2k tokens) and is read on most audits. Mitigation: §4.6 stays ecosystem-neutral and has no tables beyond V1/V4; subject detail goes to addenda.
- **"Resolved compromise" abuse.** V4(c) could be argued for risky packages. Mitigation: it requires a cited source with a bounded range plus a published remediation; otherwise case (a) applies.
- **Auditors may not find publish times** (browser eval open question). Mitigation: Unknown → `Not available` + no Tier 1. That is a cost increase, not a wrong verdict.
- **Concurrent plan rebase.** No file overlap; if it closes first, rebase this branch before close.
- **C6 reading (A6).** KEV CRITICAL rejects even when a fix exists. Mitigation: recorded as an assumption; reversing it touches one table cell + one term clause.
- **Interim inconsistency.** Until the container and registry plans run, their workflow/addendum CVE wording differs from §4.3. Mitigation: §4.3's Addendum line forbids changing the verdict classes, and the plans are already queued (Hand-off).
- **`SKILL.md` headroom is 16 B.** Mitigation: Step 3 lists ordered fallback trims. Later plans adding to `SKILL.md` must offset or justify their own budget.

### Open Questions

None.
- Thresholds (72 h / 7 d), the 15,500 B ceiling, the escalation exemption and the eval hand-off were confirmed by the orchestrator.
- C4 and C6 are decided by the human. The C6 shared part is in Steps 2–3; the C4 hooks are in Step 1; the C4/C6 subject parts are in the Hand-off.
- A1 is verified in Preflight with a stop rule.

### Revision Log

| Date | Trigger | Change |
|---|---|---|
| 2026-10-16 | Initial | V1–V5 floor, wiring, hand-off |
| 2026-10-16 | Human decisions C4 + C6 (via orchestrator); live evals once after all refreshes; all refresh plans executed this session | C6 shared part folded in: tree node + term → Blocking CVE (3h, 3i); §4.3 table + definitions (2i, 2j); 2g wording; 3g shortened for budget (15,460 → 15,484 B). C4 hooks: V1 version unit for V1–V3, V2 Curated pipelines. Out-of-scope, Assumptions (A5, A6), Impact, traces T7–T11, Hand-off (container C4/C6, registry C6 alignment, own-code plug-ins, KEV tooling), Risks updated |

### Split Decision

`No split — single scope, within size budget`. 5 steps, one `.projex/` scope. Spec-level text only, so no upstream/downstream mix. The steps are coupled: Steps 2–5 reference the headings Step 1 creates.
