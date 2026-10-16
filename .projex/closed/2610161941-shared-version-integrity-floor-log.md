# Execution Log: Shared Version-Integrity Floor

> **Status:** Complete
> **Started:** 20261016 19:58
> **Repo Root:** /home/user/install-auditor-skill
> **Plan File:** .projex/2610161941-shared-version-integrity-floor-plan.md
> **Parent:** 2610161941-shared-version-integrity-floor-plan.md
> **Base Branch:** claude/youthful-dijkstra-5ov1kt
> **Worktree Path:** .projexwt/2610161941-shared-version-integrity-floor

## Pre-Check Results
```
PASS  Plan is committed (826bb3d projex: add plan - shared-version-integrity-floor)
PASS  Working tree is clean
PRE-CHECK PASSED
```

## Steps

### [20261016 19:58] - Preflight
**Action:** In worktree: `wc -c < SKILL.md`; `run_evals.py validate`; evals unittest; tests unittest; `grep -rn "any version"`; `grep "^## 4\.\|^## Audit" criteria.md`; A1 chalk range check.
**Result:** SKILL.md = 14995 B (as expected). validate: 41 evals, 248 assertions pass. `unittest discover -s evals -p "test_*.py"`: Ran 12 tests OK (record count: 12). `unittest discover -s tests`: Ran 19 tests OK (skipped=6). `any version` only at workflows/registry-package.md:449 (A3 holds). criteria.md has no `## 4.6` (4.5 then 4.7). Parsed-string count grep on SKILL.md (`## Audit Coverage|Audit confidence (coverage)|Verdict: [APPROVED`) = 4. Base moved since plan (7f137d1 lookup-script fixes) - no overlap with the 5 target files; Before strings re-checked per step.
A1: `scripts/vuln-lookup.py` and a direct OSV query both failed (proxy 403 policy denial on api.osv.dev; gh advisories path blocked) - not retried per proxy policy. Fallback WebSearch: multiple secondary sources (Semgrep, Cycode, mate.security, proarch) list the Sept-2025 chalk compromise as the single malicious version chalk@5.6.1 (malicious versions removed within hours). Range is bounded and excludes 5.3.0. No GHSA ID surfaced; one guide names 5.6.0 as last known good.
**Status:** Success (A1 verified via secondary sources only; live OSV/GHSA lookup unavailable in sandbox)

### [20261016 20:03] - Step 1: Add §4.6 Version & Update Integrity to criteria.md
**Action:** Inserted plan's §4.6 block (V1-V5, plug-in convention, hosted-service rule, C4 hooks) before `## 4.7` in references/criteria.md. Before-anchor matched exactly (base drift from 7f137d1 did not touch this file).
**Result:** `grep -c "^### V[1-5] "` = 5; `^- \*\*Addendum:\*\*` = 5; `Curated pipelines` bullet = 1; `^## 4\.` order 4.1 4.2 4.3 4.4 4.5 4.6 4.7; diff = +70 lines, only criteria.md; criteria.md 18,069 B. Self-verified (diff read; verify-projex sub-subagent not used - Encouraged only).
**Status:** Success


### [20261016 20:08] - Step 2: Wire existing criteria.md sections to §4.6 (incl. C6 CVE mapping)
**Action:** Applied the 10 exact replacements 2a-2j in references/criteria.md via Edit (tier intro, tooling note, Version integrity row, Tier 1 row-set text, row contract, §4.1 identity note, §4.2 abandoned, §4.3 supply-chain scope note, §4.3 CVE table, §4.3 own-code/fixed/KEV/VEX definitions). All Before strings matched once at current base.
**Result:** `grep -ci "CONDITIONAL or REJECTED\|if unpatched"` = 0; `^- \*\*Addendum:\*\*` = 6; criteria.md = 21,455 B (plan expected ~21,455); diff +22/-5. Self-verified by diff read.
**Status:** Success

### [20261016 20:14] - Step 3: Wire SKILL.md (precedence, Red Flag, coverage, skeleton, Step 0, Blocking CVE)
**Action:** Applied 9 exact replacements 3a-3i in SKILL.md via Edit. All Before strings matched once at current base.
**Result:** `wc -c < SKILL.md` = 15484 (<= 15500, equals plan's simulated result); stale-phrase grep = 0; `§4.6` count = 4; `Blocking CVE|blocking CVE` count = 2; REJECTED-line widths = [64]; parsed-string count unchanged (4). Fallback trims not needed. Self-verified.
**Status:** Success

### [20261016 20:18] - Step 4: Update references/report-template.md
**Action:** Applied 3 exact replacements 4a-4c (Version integrity row, identity-matched verify, V5 re-audit line).
**Result:** `grep -ci "re-audit on major version bump"` = 0; `grep -c "§4.6"` = 3. Parsed lines untouched. Self-verified.
**Status:** Success

### [20261016 20:20] - Step 5: Align contradicting callers (registry-package workflow, classifier)
**Action:** Applied 5a/5b to workflows/registry-package.md (Toward REJECTED: maintainer-compromise and known-malware bullets version-scoped) and 5c to references/classifier.md (generic Phase 2 exception). Wrapped at ~78 cols as in plan.
**Result:** `grep -c "exfiltration in any version"` registry-package.md = 0; `grep -c "§4.6 V4"` registry-package.md = 2; `grep -c "Sole exception"` classifier.md = 1. Self-verified.
**Status:** Success

### [20261016 20:30] - Post-steps: full verification, paper traces, reviews
**Action:** Ran harness + consistency script + diff scope check; walked paper traces T1-T11 through SKILL.md Step N and criteria.md §4.6/§4.3; spec-compliance and quality review of the diff; removed `evals/__pycache__` and `tests/__pycache__` (created by test runs; ignored, agent-created) from the worktree.
**Result:**
- `run_evals.py validate`: 41 evals, 248 assertions OK. `unittest discover -s evals -p "test_*.py"`: 12 tests OK (== Preflight 12). `unittest discover -s tests`: 19 tests OK (skipped=6, == Preflight).
- Consistency script: `OK` (V1-V5 headings, every `§4.6 V<n>` resolves, stale phrases gone in all 5 files, SKILL.md <= 15,500 B, Blocking CVE terms, REJECTED widths equal, parsed strings kept, Version integrity rows).
- `git diff --stat 968e70f..HEAD`: exactly SKILL.md, references/criteria.md, references/report-template.md, references/classifier.md, workflows/registry-package.md (+ this log). evals/ untouched (0 lines).
- Final sizes: SKILL.md 15,484 B (headroom 16 B), criteria.md 21,455 B.
- Paper traces (rule cited per hop):
  - T1 chalk@5.3.0: V1 >= 7 d no effect; V4 (c) LOW `past compromise` (bounded range 5.6.1, resolved - A1); Tier 1 barred by V4 c -> Tier 2; registry-package 5a/5b do not fire (version outside range, not malicious by design); Red Flag requires version in range -> no REJECT -> APPROVED reachable. OK.
  - T2 6 h old, valid SLSA: V1 < 72 h HIGH `fresh version`; V2 verified but "origin, not safety" never offsets a flag; Tier 1 unavailable; tree node "Any HIGH-severity flags" -> CONDITIONAL, V1 time-bound condition, no escalation notice for this flag alone. OK.
  - T3 verified publisher, minutes old, no upstream tag: V1 HIGH + V3 bullet 2 HIGH; V2 badge no offset; tree -> CONDITIONAL; V3 HIGH not exempt -> escalation notice; condition = last release passing V3. OK.
  - T4 version in malware advisory range: V4 (a) -> Red Flag "Confirmed supply chain compromise" -> tree node 3 -> REJECTED + incident-response note. OK.
  - T5 KICS-style: V2 provenance names repo not expected -> no credit (note only); V3 bullet 1 HIGH (different repo) + Tier 1 barred -> >= CONDITIONAL. OK.
  - T6 SaaS OAuth connector: §4.6 hosted-service rule V1-V3 `N/A (hosted service)`; V4/V5 apply; V5 update-control says updates cannot be held and lists triggers; verdict unchanged. OK.
  - T7 Debian image, unfixed OS-package HIGH, non-KEV: §4.3 High row: not own code -> HIGH flag -> CONDITIONAL; Blocking CVE term (SKILL.md) not met. OK.
  - T8 lodash@4.17.20 HIGH fixed in 4.17.21, non-KEV: High row "fixed release exists" -> HIGH flag -> CONDITIONAL; Fixed release definition -> condition install 4.17.21. OK.
  - T9 own-code KEV CRITICAL with fix: Critical row "Listed in CISA KEV -> REJECTED"; Fixed release bullet: KEV rejects even when a fix exists, Recommendation names fixed release (A6). OK.
  - T10 OS-package KEV CRITICAL with publisher VEX not_affected naming this image version + justification: VEX bullet -> evidence, CVE left out of rating, recorded in CVE row; not Blocking. OK.
  - T11 DOI redis, dev: V1 Addendum hook (DOI base refresh = same version unit) keeps age effect off refresh churn; V2 Curated pipelines bullet lets an addendum accept DOI attestations for Tier 1 identity; other Tier 1 conditions still apply -> Tier 1 path open, APPROVED reachable. Depends on the container plan filling the two plug-ins (hooks exist, subject text deferred by design). OK.
- Spec compliance: plan linked no external spec; every plan Success Criterion met (see plan list; V1 Addendum line + Curated pipelines bullet present; 6 `**Addendum:**` lines incl. §4.3).
- Quality review observations (no fix; within plan design): (1) SKILL.md Escalation text still says CONDITIONAL-with-HIGH-flags gets an escalation notice; the time-bound `fresh version` exemption lives only in criteria.md V1 (plan decision; 16 B SKILL.md headroom). (2) `references/criteria/registry-package.md` and other addenda still carry pre-C6 CVE wording until the per-subject plans run (plan Hand-off). (3) Live OSV/GHSA lookup for A1 was blocked in the sandbox; A1 rests on secondary sources.
**Status:** Success

## Deviations
None to plan text. Base had moved (7f137d1, lookup-script fixes) but touched none of the 5 target files; every Before string matched once.
Step commits were grouped by plan step (Step 4 and Step 5 each their own commit); the preflight log entry rode in the Step 1 commit.

## Issues Encountered
- A1 live lookup: `scripts/vuln-lookup.py`, direct OSV query and `gh api /advisories` all denied by the egress proxy (403 policy). Not retried. Resolved via WebSearch: secondary sources name chalk@5.6.1 as the sole malicious chalk version (bounded range, removed within hours); 5.3.0 outside it. No GHSA ID surfaced.
- Base-checkout CLAUDE.md asks for ctx_* MCP tools; none are available to this subagent, so plain Bash/Read/Edit were used.

## Data Gathered
Preflight baselines: SKILL.md 14,995 B; evals unittest 12 tests; tests unittest 19 (6 skipped); validate 41 evals / 248 assertions.

## User Interventions
None.
