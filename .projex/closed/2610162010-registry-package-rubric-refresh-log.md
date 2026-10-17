# Execution Log: Registry-Package Rubric Refresh

> **Status:** Complete
> **Started:** 20261017 04:48
> **Repo Root:** /home/user/install-auditor-skill
> **Plan File:** .projex/2610162010-registry-package-rubric-refresh-plan.md
> **Parent:** 2610162010-registry-package-rubric-refresh-plan.md
> **Base Branch:** claude/youthful-dijkstra-5ov1kt
> **Worktree Path:** .projexwt/2610162010-registry-package-rubric-refresh

## Pre-Check Results

```
PASS  Plan is committed (a2e1f87 projex: add plan - registry-package-rubric-refresh)
PASS  Working tree is clean
PRE-CHECK PASSED
```

Plan status commit on base: `3668e62` (projex: start execution of registry-package-rubric-refresh). Worktree created via projex-worktree.sh; no bootstrap needed (stdlib Python only). pwsh 7.4.6 put on PATH for test runs only.

## Steps

### [20261017 04:48] - Preflight
**Action:** Ran plan Preflight in the worktree: `merge-base --is-ancestor` for 20843cc and 8564410, floor/addendum greps, wc -c, tests (with pwsh), evals unittest, evals validate.
**Result:** floor-on-base | siblings-on-base | criteria.md floor heading count 1 | Addendum lines 6 | closed floor walkthrough present | `§4.6 V4` in workflow 2 | `Version & Update Integrity` in addendum 0 | sizes 17237 / 23201 / 4932 B | tests: Ran 19 OK (with pwsh) | evals unittest: Ran 12 OK | evals validate exit 0.
**Status:** Success

### [20261017 04:55] - Step 1: npm identity + continuity fields in registry-lookup (both twins) + tests
**Action:** Applied 1a-1c (Python: `_npm_identity`, `_npm_previous_version`, new npm keys), 1d-1f (PowerShell: `ConvertTo-UtcDate`, `Get-NpmIdentity`, `Get-NpmPreviousVersion`, same keys), 1g-1h (fixture `NPM_IDENTITY_DRIFT`, helper `without`, 2 asserts on existing single-entry tests, 2 new Python tests, 2 new PowerShell tests). All Before strings matched once; no improvisation.
**Result:** `tests` with pwsh 7.4.6 on PATH: Ran 23, OK. Without pwsh: Ran 23, OK (skipped=8). Direct parity check (ad hoc, not committed): Python and PowerShell npm output for the drift fixture have identical key sets and key order; `previousVersion.publishedAt` is 2020-01-01 in both. No `__pycache__` created (PYTHONDONTWRITEBYTECODE=1). Self-verified; verify-projex sub-subagent not used (Encouraged only).
**Status:** Success


### [20261017 05:03] - Step 2: Addendum references/criteria/registry-package.md
**Action:** Applied 2a-2m in order with a scratchpad helper that extracts each Before/After pair verbatim from the plan's Step 2 fences and requires exactly one match per Before (all-or-nothing write). 2m's Before (= 2f's After) matched because 2f was applied first.
**Result:** 13/13 applied, 0 misses. Step 2 greps: `## Version & Update Integrity (§4.6)` count 1 | bullets V1 V2 V3 V4 V5 in order | `## CVE Scope (§4.3)` + `### Client execution model` count 2, CVE Scope heading directly precedes the §4.6 section | `| Identity (§4.6 V2) | Not required` count 1 | stale-phrase count 0. File 17,237 B -> 30,112 B (plan estimate "~27 KB" was low; content is exactly the plan's After text). Reviewed Tier 1/2/3 tables in place: identity row optional, continuity row, publisher change in Tier 3 table. Self-verified; verify-projex sub-subagent not used (Encouraged only).
**Status:** Success

### [20261017 05:08] - Step 3: Workflow workflows/registry-package.md
**Action:** Applied 3a-3q in order with the same verbatim extractor (one match required per Before, all-or-nothing write).
**Result:** 17/17 applied, 0 misses. Step 3 greps: stale-phrase count 0 | `§4.6 V[1-5]` count 13 (>= 8) | `[-Version "<version>"]` count 4 | no added prose line over 78 characters (the plan's byte-based `awk length > 80` check flags 2 lines only because `→`/`≥` are multi-byte; a character-count check finds none). File 23,201 B -> 26,589 B. Self-verified (Do-Projex/verify sub-subagents not used; both Encouraged only).
**Status:** Success

### [20261017 05:12] - Step 4: references/registries.md language-registry rows
**Action:** Applied 4a-4i (whole-line replacements) with the verbatim extractor.
**Result:** 9/9 applied, 0 misses. `git diff -U0 references/registries.md` hunks start at lines 6, 11, 14, 20, 23, 26, 29, 32, 38 (all <= 38; nothing in §IDE / §CI/CD / §Container). Stale-phrase grep (`No mandatory publishing auth`, `High trust for modules in the index`, `Direct VCS installs bypass`) count 0. Plan consistency script (run from worktree, not committed): `OK`.
**Status:** Success

### [20261017 05:20] - Completion: full verification, criteria, paper traces, reviews
**Action:** Ran full verification from the worktree (pwsh 7.4.6 on PATH for the test run only), plan consistency script, scope checks, and paper traces R1-R13 against the final text.
**Result:**
- `python3 -m unittest discover -s tests -p "test_*.py"` with pwsh: Ran 23, OK. Without pwsh: Ran 23, OK (skipped=8). `.ps1` changes DID run under pwsh (4 PowerShell registry tests incl. 2 new, plus existing).
- `python3 -m unittest discover -s evals -p "test_*.py"`: Ran 12, OK. `python3 evals/run_evals.py validate`: exit 0. `git diff --stat <base>..HEAD -- evals`: empty.
- Consistency script: `OK`. Stale phrases: 0 in all 3 doc files. Old Tier 1 identity wording ("Verified per \"Ecosystem Trust Signals\" OR ...", "Identity verified per the addendum", "satisfies the Tier 1 identity row"): 0.
- `git diff --stat <base>..HEAD`: the 6 plan files plus this log (projex doc). `references/registries.md` hunks at lines 6-38 only.
- Paper traces (rule cited per hop): R1/R2 chalk: V1 none; never-used identity = note only (addendum Scoring impact "Mechanism exists, package never used it"), workflow "Missing provenance when mechanism exists" CONDITIONAL removed (3p); V3 none; V4(c) LOW -> Tier 2; clean CVEs -> APPROVED reachable (3q). R3 TanStack shape: V2 verified, no offset; V1 HIGH -> workflow "Fresh version" CONDITIONAL citing addendum V1 cooldown table (`min-release-age=7` / `minimumReleaseAge: 10080`). R4: V3 drop + publisher change -> addendum Tier 3 table row (2f) and workflow Tier 3 bullet (3f); CONDITIONAL "Identity dropped or changed" = install previous passing release. R5 lodash@4.17.20: `vuln-lookup` `high` + fixed release -> HIGH flag -> CONDITIONAL (install 4.17.21). R6: `dep-scan` `critical` KEV-listed -> REJECTED naming fixed dep; not KEV -> HIGH flag -> CONDITIONAL; depth never makes a Blocking CVE. R7: `high` with no fixed release -> Blocking CVE -> REJECTED. R8 npm 12 native addon: Client execution model -> rate as if approved; CONDITIONAL "approve only this package, pinned" (workflow "Install scripts need approval"). R9 prettier 3.9.10: V2 matched via same `oidcConfigId` (note only, no Tier 1 credit); V3 none; < 7 d Tier 2, >= 7 d Tier 1 (Version age row); APPROVED reachable. R10 PyPI `.pth`: addendum PyPI row HIGH + V3 new-hook HIGH; persistence/dropper -> workflow "Install-time persistence or dropper" REJECTED, else CONDITIONAL with Tier 3 review (2f trigger). R11 Go `GONOSUMDB=github.com/*`: addendum Go trust row and registries.md Go line flag it (the "remove the pattern" recommendation is implied by the row's "no GONOSUMDB / GOPRIVATE pattern covering public modules", not stated as a sentence). R12 lodash 4.18.1: Identity row "Not required", V1 >= 7 d, V3 none (same publisher, nothing dropped), adoption > 1M -> Tier 1 -> APPROVED. R13: new publisher account on popular package: V3 publisher change MEDIUM+, Continuity row fails -> no Tier 1; always Tier 3 (2f / 3f) -> deep audit.
- Spec compliance (criteria.md §4.6 V1-V5 and §4.3 classes, human Tier 1 decision): all requirements met; addendum only fills/tightens §4.6, no new verdict class, identity absence never blocks Tier 1, V2 "never enough on its own" wording kept in addendum and workflow, publisher change forces Tier 3.
- Quality review: twins have identical key sets/order (ad hoc parity check, Step 1); script comments carry rationale and no projex references; no dead code; no `__pycache__` or untracked artifacts in the worktree.
- Cleanup: nothing started (no servers/containers); scratch helper files live only in scratchpad `exec-registry-2610162010/` (outside repo), removed after this entry; no stash used; pwsh PATH override applied per command only.
**Status:** Success

## Deviations
- None to content: all 47 edits applied verbatim; every Before matched exactly once.
- Size estimates in the plan were low: addendum 17.2 -> 30.1 KB (plan "~27 KB"), workflow 23.2 -> 26.6 KB (plan "+~3 KB"). Content is exactly the plan's After text; no action taken.
- The plan's byte-based `awk length > 80` line-width check flags 2 workflow lines because `→`/`≥` are multi-byte; a character-count check finds none over 78.
- No task-list tool available in this environment; the plan steps and this log served as the tracking backbone.
- verify-projex / do-projex sub-subagents not used (both marked Encouraged, not Required); verification done by self with test runs, parity check and the plan's consistency script.

## Issues Encountered
None.

## Data Gathered
Not applicable (implementation plan).

## User Interventions
None.
