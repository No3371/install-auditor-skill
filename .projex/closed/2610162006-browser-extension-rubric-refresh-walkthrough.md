# Walkthrough: Browser-Extension Rubric Refresh

> **Execution Date:** 2026-10-16
> **Completed By:** Claude (executor subagent) | closed by close-projex subagent
> **Source Plan:** 2610162006-browser-extension-rubric-refresh-plan.md
> **Parent:** 2610162006-browser-extension-rubric-refresh-plan.md
> **Duration:** ~21 min (20:12-20:33 per execution log timestamps)
> **Result:** Success

---

## Summary

Browser-extension rubric refreshed to the 2026-10 ecosystem and plugged into the shared §4.6 floor. `references/criteria/browser-extension.md` 8,565 → 15,641 B (rewrite: `## Version & Update Integrity (§4.6)` V1-V5, `## CVE Scope (§4.3)`, per-browser MV2 table, Data Disclosure, Content Script Reach, Remote Code & Config). `workflows/browser-extension.md` 17,250 → 18,471 B (21 exact replacements). `references/criteria.md` §4.4 browser sub-table realigned row-for-row with the addendum (21,455 → 22,035 B). All three files hash-match the plan blocks; consistency script `OK`; harness unchanged.

---

## Objectives Completion

| Objective | Status | Notes |
|-----------|--------|-------|
| F1 / A1 §4.6 plug-in, one ownership-transfer rule | Complete | Addendum V1-V5; Tier 1 bullet "§4.6 allows Tier 1"; ownership transfer = HIGH + Tier 3; workflow row `Version integrity (§4.6)` |
| F2 / A2 MV2 per-browser reality | Complete | Chrome `unsupported MV2` HIGH + Tier 3; Edge retiring MEDIUM; Firefox LOW; MV2-retirement removal ≠ "Removed for cause" |
| F4 / A3 badge facts | Complete | Edge "Certified" removed; CWS Featured manual; Established Publisher added, excluded from Tier 1 alone |
| F5 / A5 permission coverage | Complete | `scripting`, `userScripts`, observe-only `webRequest`, `identity`, capture APIs, etc.; `storage` → LOW |
| F6 / A6 AI-chat reach + disclosure | Complete | Content-script "Sensitive" row; `## Data Disclosure`; workflow research Q8 |
| F7 / A7 enforceable controls | Complete | V5 (enterprise version pin, `ExtensionSettings`, `override_update_url`); workflow CONDITIONAL bullets |
| F8 / A8 stale sources, sideload | Complete | crxcavator removed; `gecko.update_url` attribution fixed; `### Install path`; `## Remote Code & Config` |
| C6 CVE scope | Complete | `## CVE Scope (§4.3)`; workflow 4.3 adds CISA KEV |
| F11 §4.4 matrix alignment | Complete | 11 rows equal addendum ratings; pointer sentence; no Docker lines touched |

---

## Execution Detail

> Derived from `git log`/`git diff` of `claude/youthful-dijkstra-5ov1kt...projex/2610162006-browser-extension-rubric-refresh` (merge base `8ff2e7a`) and the execution log.

### Preflight

**Planned:** shared-floor greps, size and hash baseline, harness baseline.
**Actual:** floor greps 1 / 5 / 6 / 1 / 2 / 1 as expected; sizes 8565 / 17250 / 21455; `awk length>79` = 3 (pre-existing); `run_evals.py validate` OK; evals unittest 12 OK.
**Deviation:** None.

### Step 1: Rewrite `references/criteria/browser-extension.md`

**Planned:** whole-file replacement with the plan block.
**Actual:** block extracted by `sed` from plan lines 172-379 (no retyping). sha256 `588866ba9615efd0e0daaaf9b8b2db7eee01eef4980c177e31cffa91939a04a8` matches; 15,641 B (cap 15,800). One `## Version & Update Integrity (§4.6)` heading, 5 V-bullets, `## CVE Scope (§4.3)`. Commit `e185bf4`.
**Deviation:** None.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `references/criteria/browser-extension.md` | Modified | Yes | Whole-file rewrite; ~117 lines touched across hunks at lines 6-208 |

**Verification:** sha256 equality; heading and bullet greps; stale-string grep = 0.

### Step 2: Update `workflows/browser-extension.md`

**Planned:** 21 exact `Before → After` replacements (2a-2u).
**Actual:** pairs parsed from plan fences by a scratch script outside the repo; each `Before` asserted to occur exactly once at application time; 21/21 applied. sha256 `1510a4b60104a01a639df76024b051a9ca6255a1dc86c284ad7a4092d7129afb` matches; 18,471 B (cap 18,600); lines > 79 cols = 3 (pre-existing). Commit `e9e82ce`.
**Deviation:** None.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `workflows/browser-extension.md` | Modified | Yes | Hunks at lines 47-374: Identify/store data, Tier thresholds, research Q8, manifest sources/keys, source review, coverage row `Version integrity (§4.6)`, permission/CVE/verdict text; 111 lines changed |

**Verification:** hash match; `Version integrity (§4.6)` row = 1; stale strings = 0; `gecko.update_url|CISA KEV` lines = 3.

### Step 3: Align §4.4 browser sub-table in `references/criteria.md`

**Planned:** replace sub-table (heading through `activeTab` row) with plan After block; add pointer sentence.
**Actual:** applied via scratch script with exact-once anchor assertion. sha256 `3ca4bd20c443fbe6cd0f06fa9bd9e8d3ffd1050f3b5ba95c31cf691a6a0faf35` matches plan (no sibling had changed the file before). Diff 12+/9-, hunks at lines 187-199; Docker/privileged lines in diff = 0. Commit `9fb8932`.
**Deviation:** None.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `references/criteria.md` | Modified | Yes | §4.4 browser sub-table: 11 rows realigned (observe-only `webRequest` split from blocking; `history`, `downloads`, `tabs`, `<all_urls>`, `storage` ratings); 1 pointer sentence |

**Verification:** consistency script (plan Verification Plan) printed `OK`; `run_evals.py validate` OK; evals unittest 12 OK; tests unittest 19 OK (6 skipped).

### Completion commit

Commit `bd7d647` set plan Status `Complete`, `Log:` field, and the execution log.

---

## Complete Change Log

> **Derived from:** `git diff --stat claude/youthful-dijkstra-5ov1kt...projex/2610162006-browser-extension-rubric-refresh`

### Files Created
| File | Purpose | Lines | In Plan? |
|------|---------|-------|----------|
| `.projex/2610162006-browser-extension-rubric-refresh-log.md` | Execution log | 97 | Yes (implicit) |
| `.projex/closed/2610162006-browser-extension-rubric-refresh-walkthrough.md` | This walkthrough | - | Yes (close) |

### Files Modified
| File | Changes | Lines Affected | In Plan? |
|------|---------|----------------|----------|
| `references/criteria/browser-extension.md` | Rewrite on §4.6 floor | 117 changed lines (+ side larger) | Yes |
| `workflows/browser-extension.md` | 21 replacements | 111 changed lines | Yes |
| `references/criteria.md` | §4.4 browser sub-table | 12+/9- | Yes |
| `.projex/2610162006-browser-extension-rubric-refresh-plan.md` | Status Complete, Log, Walkthrough link | 3 lines | Yes (close) |

### Files Deleted
None.

### Planned But Not Changed
None. `evals/`, `SKILL.md`, `STEWARDSHIP.md`, `references/registries.md`, `references/classifier.md` untouched, as scoped.

---

## Success Criteria Verification

| Criterion | Method | Result | Evidence |
|-----------|--------|--------|----------|
| Preflight confirms shared floor | Preflight greps | Pass | 1 / 5 / 6 / 1 / 2 / 1 |
| Addendum byte-identical; one §4.6 heading, V1-V5, CVE Scope | sha256 + greps | Pass | `588866ba…` match; heading 1, bullets 5 |
| Stale strings gone | consistency script | Pass | 0 hits in both subject files |
| Required new strings present | consistency script | Pass | all addendum and workflow strings found |
| `criteria.md` §4.4 sub-table = Step 3 block; 11 rows equal addendum | sha256 + row-equality script | Pass | `3ca4bd20…` match; `OK` |
| §4.6 V<n> / §4.3 references resolve | consistency script | Pass | `OK` |
| Sizes within caps | `wc -c`, `awk` | Pass | 15,641 ≤ 15,800; 18,471 ≤ 18,600; long lines 3 = pre-existing |
| Harness | `validate` + unittest | Pass | validate OK; evals 12 OK; tests 19 OK (6 skipped) |
| Paper traces T1-T10 | manual walk of verdict tree | Pass | all ten produce plan's stated verdicts (log "Verification: paper traces") |
| Planning simulation reproduced | real execution hashes | Pass | all three sha256 values reproduced |
| `git diff --stat` = exactly 3 files + log; `evals/` untouched | diff stat | Pass | 3 shipped files + plan/log |

**Overall:** 11/11 criteria passed.

---

## Deviations from Plan

None. All three blocks applied byte-exact.

---

## Issues Encountered

### Issue 1: Precheck WARN on untracked sibling plans
- **Description:** 6 untracked sibling-planner plans in the main checkout at execution start.
- **Severity:** Low
- **Resolution:** Not part of this execution; left untouched.

### Issue 2: Base moved during execution
- **Description:** Sibling plans and starts were committed to base while this ran.
- **Severity:** Low
- **Resolution:** `criteria.md` unchanged by others at Step 3, so the full-file hash check applied. At close, base had advanced further; squash merged cleanly on the subject files (see Close notes).

### Close notes
- Nav `2604070218-install-auditor-subject-typed-redesign-nav.md` updated in the close commit (Last Revised, Recent Progress, maintenance checklist, Revision Log); the plan carries no `Nav:` field but each prior rubric-refresh close updated it, so this close follows that precedent. Add/add conflicts against base's concurrent nav entries are resolved by keeping both sides.

---

## Key Insights

**Rationale promoted:** none needed. The rationale (3-day V1 rule, Established Publisher excluded from Tier 1 alone, ownership transfer = HIGH, Edge MV2 = MEDIUM) ships in the addendum text itself; no source files carry projex references.

### Lessons Learned

1. **Extract plan blocks mechanically**
   - Context: Steps 1-3 embed exact content blocks and 21 `Before/After` pairs.
   - Insight: `sed` extraction plus a hash check removes transcription error; per-pair exact-once assertions catch base drift at application time.
   - Application: keep embedding hash-pinned blocks in rubric-refresh plans.

### Gotchas / Pitfalls

1. **Unqualified "removal" in tier bullets**
   - Trap: Tier 3 trigger "Known prior removal or policy violation from any store" and Tier 1 bullet "No known incidents or store removals" lack the MV2-retirement carve-out that lives only in the MV2 section.
   - How encountered: paper trace T1 (Firefox uBO: CWS removal 2026-08-31 could be read as a Tier 3 trigger).
   - Avoidance: add a one-clause qualifier to both bullets (follow-up below). Verdict stays reachable meanwhile, since Tier 3 does not force CONDITIONAL.

---

## Recommendations

### Immediate Follow-ups
- [ ] Revise addendum: add MV2-retirement carve-out to the Tier 1 "No known incidents or store removals" bullet and the Tier 3 "Known prior removal or policy violation" trigger (orchestrator consistency patch).
- [ ] T10 note: "No store listing (sideloaded) = strong negative" names no flag level; CONDITIONAL follows from Tier 3 + unmet V1/V2 evidence. Consider naming the level.
- [ ] Orchestrator harmonises the §4.3 plug-in heading across addenda (this plan uses `## CVE Scope (§4.3)`).
- [ ] STEWARDSHIP: browser-extension Last Reviewed = 2026-10-16.

### Future Considerations
- Eval refresh plan: new cases (a)-(g) listed in the plan's Eval hand-off; eval 11 time dependence under V1.
- F9 deferred: Safari Web Extensions; Chromium-fork MV2 detail beyond one table row.
- Container plan will later edit the Docker lines of `references/criteria.md` §4.4 (different hunk).

### Plan Improvements
- State the MV2-retirement carve-out in every bullet that mentions store removal, not only in the MV2 section.

---

## Related Projex Updates

### Documents to Update
| Document | Update Needed |
|----------|---------------|
| `2610162006-browser-extension-rubric-refresh-plan.md` | Status Complete; Walkthrough link; moved to closed |
| `2610162006-browser-extension-rubric-refresh-log.md` | Moved to closed |
| `2604070218-install-auditor-subject-typed-redesign-nav.md` | Recent Progress, checklist, Revision Log, Last Revised |
| `2610161927-browser-extension-ide-plugin-stewardship-review-eval.md` | Left active (IDE plan still pending); no link change needed |

### New Projex Suggested
| Type | Description |
|------|-------------|
| Revise/Patch | Tier 1 / Tier 3 MV2-retirement carve-out (orchestrator consistency patch) |
| Plan | Eval refresh for browser-extension cases (a)-(g) |

---

## Appendix

### References
- Execution commits: `e185bf4` (step 1), `e9e82ce` (step 2), `9fb8932` (step 3), `bd7d647` (complete)
- Execution log: `2610162006-browser-extension-rubric-refresh-log.md`
