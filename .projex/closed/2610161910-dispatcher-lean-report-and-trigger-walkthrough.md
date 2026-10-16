# Walkthrough: Dispatcher Lean Report, Output Location & Trigger Tuning

> **Execution Date:** 2026-10-16
> **Completed By:** Claude (executor subagent; Step 1 file written by orchestrator) | closed by close-projex subagent
> **Source Plan:** 2610161910-dispatcher-lean-report-and-trigger-plan.md
> **Parent:** 2610161910-dispatcher-lean-report-and-trigger-plan.md
> **Duration:** ~65 min (19:30–20:35 per execution log timestamps; includes a ~10 min Blocked interval)
> **Result:** Success (one measured-effect gap: trigger-description effect unmeasured — see Deviations)

---

## Summary

`SKILL.md` 17,093 B → 14,995 B (−2,098 B, −12%): tiered `### Report` section (compact Quick skeleton inline, full skeleton in new `references/report-template.md`), de-duplicated Reference Files (24 → 8 bullets), default report path `.install-audits/audit-<name>-<version>.md`, retuned frontmatter `description`, plus a 20-query trigger eval set. All 11 plan criteria pass offline; trigger-eval live run not performed (needs paid `claude -p`; not approved), so the description's trigger effect remains unmeasured.

---

## Objectives Completion

| Objective | Status | Notes |
|-----------|--------|-------|
| 1. Lean report: tiered skeleton + Reference Files de-dup + drop last `.ps1` in skeleton | Complete | Quick skeleton fence 33 lines; template 70 lines / 2,840 B; Reference Files 24 → 8 bullets; `.ps1` count in `SKILL.md` = 1 (script bullet only) |
| 2. Output location `.install-audits/audit-<name>-<version>.md`, caller-named location wins | Complete | Location rule in `SKILL.md` § Report; harness `rglob("audit-*.md")` verified to find reports under `.install-audits/` via grader probe |
| 3. Trigger tuning: description scoped to new third-party installables; labels fixed; trigger eval set | Complete (effect unmeasured) | Description 833 chars, `APPROVED/CONDITIONAL/REJECTED`; `evals/trigger-evals.json` 20 items 10/10; no `run_eval.py` run |

---

## Execution Detail

> Derived from git history (`6efffbc..projex/2610161910-dispatcher-lean-report-and-trigger`) and the execution log. Execution order differed from plan order (Steps 4 and 6 ran first while Step 1 was blocked).

### Preflight

**Planned:** python-ports merged check; heading grep; record B0; `validate` baseline.
**Actual:** `scripts/registry-lookup.py` present, script-bullet count 1, headings at L121/L198/L224, **B0 = 17,093 B**, `validate` = `41 evals, 248 assertions (82 deterministic, 166 model-graded)`. Plan status set `In Progress` on base (`6efffbc`).
**Deviation:** First `projex-worktree` call used a stray `-plan` branch suffix; removed before any commit, recreated as `projex/2610161910-dispatcher-lean-report-and-trigger`. No impact.

---

### Step 1: Create `references/report-template.md`

**Planned:** executor writes the full Tier 2/3 skeleton verbatim from the plan.
**Actual:** executor `Write` refused by the harness ("Subagents should return findings as text, not write report files."); not bypassed; plan/log set `Blocked` (`f0f6809`). Orchestrator wrote the file (plan lines 155–224 copied byte-for-byte with `sed`); executor re-verified identical to the committed plan block, contract-string grep = 3, `\.ps1\|Tier 1` grep = 1 (header prose only); committed `65cc99d`.
**Deviation:** Authored by orchestrator, not executor. Content unchanged.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `references/report-template.md` | Created | Yes | 70 lines, 2,840 B; full skeleton, Quick-only wording removed, confidence rules removed (moved to `SKILL.md`) |

**Verification:** diff vs plan block identical; greps 3 / 1.

---

### Step 2: Replace `SKILL.md` `### Report Skeleton` with `### Report`

**Planned:** Location + Shape + Audit-confidence bullets + Quick skeleton (≤ 40 lines).
**Actual:** Spliced via Python line-range replace with anchor asserts (old L122 heading, old L197 closing fence, old L199 `### Escalation`). `### Report` at L122; Quick skeleton fence 33 lines; `Rules of thumb for confidence` and `audit-<package-name>` gone; fence closes immediately before `### Escalation`. Commit `97ffb2a`.
**Deviation:** None.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `SKILL.md` | Modified | Yes | Report region L122–~164: new Location/Shape/confidence text + Quick skeleton replacing ~76-line single skeleton |

**Verification:** greps per plan all pass; Step N order Report → Escalation → Red Flags confirmed.

---

### Step 3: De-duplicate `SKILL.md` § Reference Files

**Planned:** 24 bullets → 8; script bullet byte-identical, last.
**Actual:** rewritten via Python; classifier, licenses, registries bullets carried verbatim; `workflows/<type>.md`, `references/criteria/<type>.md`, `references/report-template.md` bullets new; script bullet placed last. Existence loop silent (no MISSING); `grep -c '\.projex\|(Phase'` = 0. Commit `0287550`.
**Deviation:** None from plan. (Plan itself departs from 2610161852 walkthrough's "carry Reference Files text forward verbatim" — see Deviations.)

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `SKILL.md` | Modified | Yes | Reference Files section (end of file): 8 bullets; `SKILL.md` = 14,995 B |

**Verification:** 8 bullets; script bullet diff vs `6efffbc:SKILL.md` = same (re-verified at close).

---

### Step 4: Retune frontmatter `description`

**Planned:** plan's text (est. 834 chars).
**Actual:** folded scalar replaced (L4–12); PyYAML check prints `833 ok`. Commit `352960f`.
**Deviation:** length 833 vs 834 estimated (folded-scalar newline accounting). No impact.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `SKILL.md` | Modified | Yes | Lines 4–12 `description`; `name: install-auditor` unchanged |

**Verification:** name unchanged; ≤ 1024; no `<`/`>`; contains `APPROVED/CONDITIONAL/REJECTED`; no `PASS`/`FAIL`; `npm/pip/cargo/gem/go/nuget/maven` token intact. **Not verified:** actual trigger behavior.

---

### Step 5: Fix `references/criteria.md` stale Step pointer

**Planned / Actual:** L15 parenthetical `(see \`SKILL.md\` Step 6)` → `(see \`SKILL.md\` Step N → Report; Tier 2/3 skeleton in \`references/report-template.md\`)`; one hunk; commit `faa4d5b`.
**Deviation:** None.

| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `references/criteria.md` | Modified | Yes | L15 parenthetical only (1 line +/−) |

**Verification:** `grep -c 'Step 6'` = 0; 1 hunk.

---

### Step 6: Ship trigger eval set + STEWARDSHIP pointer

**Planned / Actual:** `evals/trigger-evals.json` (20 items, 10 true / 10 false, unique, keys exactly `query`/`should_trigger`) and one `Trigger evals:` paragraph in `STEWARDSHIP.md` § Running Evals. Commit `b3e93c2`. Optional `claude -p` run not executed.
**Deviation:** None (optional run skipped by design — not approved).

| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `evals/trigger-evals.json` | Created | Yes | 22 lines |
| `STEWARDSHIP.md` | Modified | Yes | +2 lines (paragraph + blank) |

**Verification:** one-liner `ok`; `grep -c 'trigger-evals.json' STEWARDSHIP.md` = 1.

---

## Complete Change Log

> **Derived from:** `git diff --numstat 6efffbc..projex/2610161910-dispatcher-lean-report-and-trigger` (before this close's doc moves).

### Files Created
| File | Purpose | Lines | In Plan? |
|------|---------|-------|----------|
| `references/report-template.md` | Full Tier 2/3 report skeleton | 70 | Yes |
| `evals/trigger-evals.json` | 20 trigger / no-trigger queries | 22 | Yes |
| `.projex/2610161910-dispatcher-lean-report-and-trigger-log.md` | Execution log | 100 (final entries after close) | Yes (process) |

### Files Modified
| File | Changes | Lines Affected | In Plan? |
|------|---------|----------------|----------|
| `SKILL.md` | description; `### Report`; Reference Files | +34 / −80 (hunks: L4–12, report region, Reference Files) | Yes |
| `references/criteria.md` | L15 pointer | +1 / −1 | Yes |
| `STEWARDSHIP.md` | Trigger-evals paragraph | +2 | Yes |
| `.projex/2610161910-dispatcher-lean-report-and-trigger-plan.md` | Status/Log header | +2 / −1 | Yes (process) |

### Files Deleted
None.

### Planned But Not Changed
None. Untouched by design (verified): `workflows/`, `scripts/`, `evals/evals.json`, `evals/run_evals.py`, Step 0, Dispatch Table, Step 1, Verdict Tree, Escalation, Red Flags, Behavioral Principles.

### Commits (execution branch)
`352960f` step 4 | `b3e93c2` step 6 | `f0f6809` block | `65cc99d` step 1 | `97ffb2a` step 2 | `0287550` step 3 | `faa4d5b` step 5 | `f448dc4` complete

---

## Success Criteria Verification

All re-run at close in the execution worktree unless marked (log).

| Criterion | Method | Result | Evidence |
|-----------|--------|--------|----------|
| `report-template.md` exists with 3 contract strings, no `.ps1`, no `Tier 1` in fence | grep | Pass | contract grep = 3; `\.ps1\|Tier 1` = 1 (header prose "Quick (Tier 1) skeleton" only, per plan) |
| `SKILL.md` `### Report` with Location/Shape/confidence rules + Quick skeleton ≤ 40 lines; no `### Report Skeleton` | grep/awk | Pass | heading L122; fence 33 lines; old heading count 0 |
| Default location names `.install-audits/`, `audit-<name>-<version>.md`; `audit-<package-name>.md` absent | grep | Pass | `.install-audits/` present at L124; `audit-<package-name>` count 0 |
| `grep -c '\.ps1' SKILL.md` = 1 | grep | Pass | 1; `python3 scripts/<script>.py` count 1 |
| Reference Files: backticked non-`<type>` paths exist; script bullet byte-identical to base | loop + diff | Pass | no MISSING; 8 bullets; script bullet same vs `6efffbc` |
| `SKILL.md` ≤ 15,300 B and ≥ 1,800 below B0 | `wc -c` | Pass | 14,995 B; B0 17,093; −2,098 |
| Frontmatter valid YAML, `name` unchanged, ≤ 1024, no `<>`, labels correct | PyYAML script | Pass | `833 ok` |
| `criteria.md` has no `Step 6` | grep | Pass | 0 |
| `trigger-evals.json` shape | Python one-liner | Pass | `ok` (20 / 10 true / unique) |
| `validate` exit 0; `unittest` OK; `prepare` snapshot has template | commands | Pass | `41 evals, 248 assertions (82 deterministic, 166 model-graded)`; `Ran 12 tests … OK`; snapshot `…/skill-snapshot/references/report-template.md` present |
| Untouched regions byte-identical; `workflows/ scripts/ evals.json run_evals.py` unchanged | region diff loop; `git diff --stat` | Pass | all 7 regions "same"; stat empty |
| Manual: grader probe eval 0 (log) | hand-written `.install-audits/audit-express-4.21.2.md` + `grade` | Pass | deterministic 3/3 (`exact_match`, `file_exists`, `line_count_max` 28 ≤ 79); `contains_concept` pending (model-graded, expected) |
| Optional: `run_eval.py` trigger run | — | Not run | needs `claude -p` auth; not approved; plan marked not a gate |

**Overall:** 11/11 gating criteria passed; 1 optional check not run. `git diff --check` clean; worktree fully clean.

---

## Deviations from Plan

### Deviation 1: Step 1 file written by orchestrator
- **Planned:** executor writes `references/report-template.md`.
- **Actual:** harness refused subagent write; orchestrator wrote it byte-for-byte from the plan; executor re-verified and committed; Steps 4 and 6 ran first, then 2, 3, 5.
- **Reason:** tool-layer guard (apparently filename/type heuristic on `*-template.md`/report-like content).
- **Impact:** none on content; ~10 min Blocked interval; plan/log briefly `Blocked`.
- **Recommendation:** future plans that create report/template-named files: expect to have the orchestrator write them, or name the executor-write fallback in the plan.

### Deviation 2: Reference Files trim vs 2610161852 walkthrough's verbatim ask (orchestrator decision)
- **Planned (by that walkthrough):** later compression carries Reference Files text forward verbatim.
- **Actual:** per-workflow and per-addendum bullets collapsed (24 → 8); classifier/licenses/registries/script bullets verbatim; no `(Phase N, Mx.y)` label or `.projex` pointer reintroduced.
- **Reason:** bullets duplicate the Dispatch Table and pointers each workflow already carries; −1,848 B on every audit. Orchestrator accepted.
- **Impact:** positive (size); the walkthrough's intent (no label/`.projex` regressions) honored.

### Deviation 3: In-repo `.install-audits/` report location (orchestrator decision)
- **Chosen:** `<project-root>/.install-audits/audit-<name>-<version>.md`, caller-named location wins.
- **Cost accepted:** one untracked folder appears in `git status`; `.gitignore` deliberately not edited. Rejected alternatives (cwd root, `~/.install-audits/`, OS temp, auto-`.gitignore`) recorded in plan Step 2 rationale.

### Deviation 4: Trigger effect unmeasured
- **Planned:** optional `run_eval.py` with `evals/trigger-evals.json`.
- **Actual:** not run (needs paid `claude -p`; not approved). Description's effect on over/under-triggering is unverified; the eval set ships for later runs.

### Deviation 5 (minor): description 833 chars vs planned 834; stray `-plan` branch suffix on first worktree attempt (removed pre-commit).

---

## Issues Encountered

### Issue 1: `Write` refused for `references/report-template.md`
- **Description:** subagent write blocked: "Subagents should return findings as text, not write report files."
- **Severity:** Medium (blocked 3 of 6 steps)
- **Resolution:** orchestrator-performed write; executor verified and resumed.
- **Time Impact:** ~10 min
- **Prevention:** see Deviation 1.

### Issue 2: Close tooling gaps (prior finding, re-verified)
- **`projex-tree.sh`:** fails — `python3: can't open file '<skill-dir>/.projex-tree.py': [Errno 2] No such file or directory` (helper missing from the synced skill directory). Advisory only per spec; close proceeded on direct git evidence.
- **`close-precheck.sh`:** `ERROR` when given the base-side plan path (`execution log is missing or inaccessible` — plan/log exist as tracked files only on the ephemeral branch, and the log's `Worktree Path` is repo-relative) ; with the worktree plan path it returns `RESULT=PASS` (gates ORIGIN_BASE and CHILD_WORKTREE PASS, 8 commits, no stashes). Earlier closers' "errors on repo-relative Worktree Path" was not reproduced for this invocation form.
- **Severity:** Low. **Prevention:** invoke `close-precheck.sh` with the plan path inside the worktree; restore `.projex-tree.py` in the skill directory.

---

## Key Insights

**Rationale promoted:** none needed — `SKILL.md` § Report states the Location rule and tier routing self-containedly; rejected location alternatives live in the plan's Step 2 rationale (workflow artifact, archivable). If future maintainers need the "why `.install-audits/`", promote a sentence to `STEWARDSHIP.md`.

### Lessons Learned

1. **Moving a mandatory section out saves nothing unless a smaller form stays inline**
   - Context: orchestrator claim "move skeleton → Tier 1 reads less" checked during planning.
   - Insight: every audit writes a report; whole-skeleton externalization is size-neutral +1 Read. Savings came from a compact inline Quick skeleton and from removing duplicated Reference Files bullets (−1,848 B, tier-independent).
   - Application: measure by tier before compressing; look for duplication first.

2. **Tier 2/3 now pay +741 B net and one extra Read**
   - Insight: accepted trade; Tier 1 audits (the common case) read −2.1 KB.
   - Application: Risk "agents skip reading the template on Tier 2/3" is untested; a later eval asserting Security/Reliability sections on a Tier 2 case would test it.

### Pattern Discoveries

1. **Contract strings duplicated across two skeletons** (`**Verdict: […]**`, `## Audit Coverage`, `**Audit confidence (coverage):**`) — graders parse them; template header states the identity rule; greps in this walkthrough check both. Consider a STEWARDSHIP drift check.
2. **Splice via Python with anchor asserts** for large block replacements in `SKILL.md` — safer than multi-hunk Edit; anchors fail loudly on drift.

### Gotchas / Pitfalls

1. **Subagent write guard on report-like filenames** — see Issue 1.
2. **`__pycache__` from `unittest`** pollutes the worktree and blocks close gates — run with `python3 -B` or delete `evals/__pycache__` (executor did).
3. **Skill-creator `quick_validate.py` on the repo directory** fails its single-`SKILL.md` rule because `.projexwt/` holds other `SKILL.md` files — validate a `git archive` export.

### Technical Insights

- `pathlib.rglob("audit-*.md")` traverses dot-directories, so the harness finds reports in `.install-audits/` without runner changes.
- Folded YAML scalar: never break a line inside a `/`-joined token.

---

## Recommendations

### Immediate Follow-ups
- [ ] Run `skill-creator` `run_eval.py --eval-set evals/trigger-evals.json --skill-path .` when `claude -p` auth is available; record per-query rates; tune description if false triggers/misses appear.
- [ ] Orchestrator pushes base (not done by close).

### Future Considerations
- Eval asserting the `.install-audits/` path and a Tier 2 case asserting full-template sections.
- STEWARDSHIP drift check for the two skeletons' shared contract lines.
- Slug collisions (`@a/b-c` vs `a-b/c`) accepted as rare.
- Remaining dispatcher compression candidates (Step 0 classifier, Red Flags relocation) stay out of scope; Red Flags needed during evidence gathering.

### Plan Improvements
- State an executor fallback for files whose names trip the write guard.
- Fix expected description length to the measured folded-scalar count.

---

## Related Projex Updates

### Documents to Update
| Document | Update Needed |
|----------|---------------|
| 2610161910-dispatcher-lean-report-and-trigger-plan.md | Status `Complete`; Completed/Walkthrough/Log links; move to `closed/` |
| 2610161910-dispatcher-lean-report-and-trigger-log.md | Status confirmed `Complete`; move to `closed/` |
| 2604070218-install-auditor-subject-typed-redesign-nav.md | Revision Log row, Recent Progress, Phase 6 checklist, § Priorities Deferred note (partly addressed); not closed |
| 2604170511-measure-read-cost-f7-m53-findings.md, 2610161852-dispatcher-rubric-consistency-*, 2610161849-python-script-ports-*, 2610161850-eval-runner-harness-* | Already closed; historical, unchanged |

### New Projex Suggested
| Type | Description |
|------|-------------|
| Plan | Trigger-eval live run + description tuning once `claude -p` auth exists |
| Plan | Evals for `.install-audits/` path and Tier 2 full-template sections |

---

## Appendix

### Close Evidence
```
close-precheck (worktree plan path): RESULT=PASS; ORIGIN_BASE PASS; CHILD_WORKTREE PASS; 8 commits; STASHES none
SKILL.md: 14995 B (B0 17093, -2098)  | ps1 count 1 | Report fence 33 lines
validate: 41 evals, 248 assertions (82 deterministic, 166 model-graded)
unittest: Ran 12 tests ... OK
prepare --ids 0: skill-snapshot/references/report-template.md present
untouched regions: same x7; workflows/ scripts/ evals.json run_evals.py: no diff
```

### References
- Base `claude/youthful-dijkstra-5ov1kt` at `6efffbc`; execution branch head `f448dc4`
- Execution log: 2610161910-dispatcher-lean-report-and-trigger-log.md
