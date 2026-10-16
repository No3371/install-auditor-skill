# Walkthrough: Dispatcher Rubric Consistency

> **Execution Date:** 2026-10-16
> **Completed By:** Claude (execute-projex subagent; closed by close-projex subagent under orchestrate-projex)
> **Source Plan:** 2610161852-dispatcher-rubric-consistency-plan.md
> **Parent:** 2610161852-dispatcher-rubric-consistency-plan.md
> **Log:** 2610161852-dispatcher-rubric-consistency-log.md
> **Duration:** ~25 min (18:55 → 19:20 UTC)
> **Result:** Success

---

## Summary

Dispatcher `SKILL.md` now agrees with its routed workflows and addenda. Red Flags rewritten (container-root item dropped; typosquat, removal, CI-ref items conditioned), tree terms + precedence block added, classifier rule promoted to shipped `references/classifier.md`, roadmap labels stripped from runtime files, taxonomy def repointed. 10/10 success criteria pass; 15/15 desk-check evals trace to expected verdicts. No scripts, evals, STEWARDSHIP, report skeleton, or frontmatter touched.

---

## Objectives Completion

| Objective | Status | Notes |
|-----------|--------|-------|
| C1 rootful container Red Flag removed | Complete | Container-root graded by `references/criteria/container-image.md` / workflow; precedence rule makes that authoritative |
| C2 typosquat Red Flag history-gated | Complete | "Confirmed typosquat / impersonation"; script `critical` qualifies, `high`/`medium` = flag only |
| C3 CI pin Red Flag aligned with workflow + addendum | Complete | "Mutable CI ref with privileged access"; tag-pinned verified → CONDITIONAL |
| C4 tree bridge to REJECTED | Complete | "CRITICAL flag" = Red Flag OR auditor-rated CRITICAL under routed workflow; recorded in Risk Flags |
| C5 "unpatched" defined | Complete | No fixed release; cites `references/criteria.md` §4.3 |
| C6 removal reason scoped | Complete | "Removed for cause" |
| C7 runtime → `.projex` dependency removed | Complete | `references/classifier.md` created; Homebrew formula → cli-binary corrected |
| C8 history labels stripped | Complete | 9 Reference Files labels, 9 workflow header comments, 2 "milestone scope" clauses, 1 addendum label |

---

## Execution Detail

> Derived from `git log`/`git diff` of `claude/youthful-dijkstra-5ov1kt..projex/2610161852-dispatcher-rubric-consistency` and the execution log.

### Step 1: Create `references/classifier.md` (a9be647)

**Planned:** New shipped file with exact plan body.

**Actual:** Created, 121 lines. Holds Rule, Tie-Breaking, Confidence Examples, Type 8 Sub-Rubric, Routing Overrides (incl. `brew install <formula>` → cli-binary, `--cask` → desktop-app), Extended Signal Patterns (rows 1–9 + 0), 5 Worked Hybrid Examples, Edge-Case Discipline.

**Deviation:** None.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `references/classifier.md` | Created | Yes | +121 lines |

**Verification:** `grep -cE '\.projex|Phase [0-9]|M[0-9]\.[0-9]|milestone'` → 0; `grep -c 'brew install <formula>'` → 2; 5 numbered examples.

**Issues:** None.

---

### Step 2: `SKILL.md` — pointer, signal row, tree terms, Red Flags, Reference Files (eda1d9d)

**Planned:** Sub-edits 2a–2e.

**Actual:** All five applied. 2a Step 0 rule paragraph → `references/classifier.md`. 2b row 7 gains `brew install <formula>` (Homebrew core; `--cask` → desktop-app). 2c tree nodes 1–2 reworded (`Any CRITICAL flag? (see Tree terms below)`, `Any unpatched HIGH/CRITICAL CVE? (see Tree terms)`); "Tree terms & precedence" block (3 bullets) at line 111, outside the fence. 2d Red Flags: 8 → 7 items (dropped "Dangerous container defaults"; "Unpinned CI action with secrets access" → "Mutable CI ref with privileged access"; "Typosquatting" → "Confirmed typosquat / impersonation"; "Removed from registry" → "Removed for cause"). 2e 9 history parentheticals stripped; `.projex` entry → `references/classifier.md`. `scripts/registry-lookup.ps1` line and Step 1 line 87 untouched (sibling-plan lines).

**Deviation:** None (SKILL.md was 242 lines, not 243; edits anchored on exact strings).

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `SKILL.md` | Modified | Yes | +25/−18: Step 0 paragraph, row 7, tree nodes (lines 96, 98), terms block (line 111+), Red Flags (line 202+), Reference Files |

**Verification:** Old Red Flag titles → 0; 4 new markers → 4; `.projex` → 0; `(Phase N, M` → 0; skeleton/`description` diff grep → empty; tree fence intact. Self-verified; no verify-projex subagent.

**Issues:** None.

---

### Step 3: Align ci-action workflow + addendum (ac047b8)

**Planned:** +1 Toward REJECTED bullet; tag-ref row + scoring bullet rewrite.

**Actual:** As planned. `workflows/ci-action.md` Toward REJECTED gains "Non-SHA ref from an unverified third-party publisher with write scopes, OIDC, package publish, or secret access". `references/criteria/ci-action.md` Ref Immutability Matrix tag row and Ref scoring impact bullet rewritten.

**Deviation:** None.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `workflows/ci-action.md` | Modified | Yes | +bullet at ~line 204 (net with Step 4: +3/−4) |
| `references/criteria/ci-action.md` | Modified | Yes | Matrix row ~35, scoring bullet ~45 (net with Step 4: +3/−3) |

**Verification:** `grep -c 'unverified third-party publisher'` → 1 in each of `workflows/ci-action.md`, `references/criteria/ci-action.md`, `SKILL.md`.

**Issues:** None.

---

### Step 4: Strip project-history labels (05534f6)

**Planned:** Remove `Phase N / Mx.y` label (+ preceding blank line) from 9 workflow header comments; 3 prose edits.

**Actual:** Done via byte-safe python3 script. `workflows/ci-action.md` and `references/criteria/ci-action.md` "milestone scope" clauses dropped; `references/criteria/remote-integration.md` header comment loses "Phase 4 / M4.4.". `workflows/generic.md` untouched.

**Deviation:** Script instead of nine manual edits (same net change).

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `workflows/{registry-package,browser-extension,container-image,ide-plugin,desktop-app,cli-binary,agent-extension,remote-integration}.md` | Modified | Yes | −2 each (blank + label line) |
| `workflows/ci-action.md` | Modified | Yes | label removed; "milestone scope" clause shortened |
| `references/criteria/ci-action.md` | Modified | Yes | "milestone scope" clause shortened |
| `references/criteria/remote-integration.md` | Modified | Yes | +1/−1 header comment |

**Verification:** label/milestone grep → empty; `grep -c '^## Phase' workflows/generic.md` → 4; `<!--`/`-->` balanced (1/1) in every workflow and the addendum.

**Issues:** First python3 attempt failed (`SyntaxError: bytes can only contain ASCII literal characters`, em dash in bytes regex) before any file change; retried with `\xe2\x80\x94`.

---

### Step 5: Update taxonomy def (8e7c5f0)

**Planned:** Last Revised bump; §6 Includes; §7 Homebrew route; Runtime-copy pointer; Open Question resolved; Revision Log row.

**Actual:** All applied in `.projex/2604070300-install-auditor-subject-type-taxonomy-def.md`; +7/−4.

**Deviation:** Runtime-copy note placed after the `> **Form:**` line separated by a blank line (own blockquote) to avoid merging into the preceding blockquote.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `.projex/2604070300-install-auditor-subject-type-taxonomy-def.md` | Modified | Yes | header date, §6, §7, pointer, Open Question, revision row |

**Verification:** `grep -c 'references/classifier.md'` → 3; stale `Homebrew core → **desktop-app` → 0.

**Issues:** None.

---

### Completion commit (3fdc7c2)

Plan status → `Complete`, plan `Log:` link, execution log → `Complete` (+92-line log). Verification + desk-check recorded in the log.

---

## Complete Change Log

> **Derived from:** `git diff --stat claude/youthful-dijkstra-5ov1kt..projex/2610161852-dispatcher-rubric-consistency` (16 files, +254/−47, before close commit)

### Files Created
| File | Purpose | Lines | In Plan? |
|------|---------|-------|----------|
| `references/classifier.md` | Shipped classifier rule | 121 | Yes |
| `.projex/2610161852-dispatcher-rubric-consistency-log.md` | Execution log | 92 | Yes (workflow artifact) |

### Files Modified
| File | Changes | Lines Affected | In Plan? |
|------|---------|----------------|----------|
| `SKILL.md` | Pointer, row 7, tree nodes, terms block, Red Flags, Reference Files | +25/−18 | Yes |
| `references/criteria/ci-action.md` | Tag-ref row, scoring bullet, milestone clause | +3/−3 | Yes |
| `references/criteria/remote-integration.md` | Header comment label | +1/−1 | Yes |
| `workflows/ci-action.md` | +REJECTED bullet, label, milestone clause | +3/−4 | Yes |
| `workflows/{agent-extension,browser-extension,cli-binary,container-image,desktop-app,ide-plugin,registry-package,remote-integration}.md` | Header label removed | −2 each | Yes |
| `.projex/2604070300-install-auditor-subject-type-taxonomy-def.md` | Runtime pointer, Homebrew fix | +7/−4 | Yes |
| `.projex/2610161852-dispatcher-rubric-consistency-plan.md` | Status Complete + links | +2/−1 (pre-close) | Yes (lifecycle) |

### Files Deleted
None.

### Planned But Not Changed
None. Deliberately untouched per plan: `evals/evals.json`, `scripts/*`, `STEWARDSHIP.md`, report skeleton, frontmatter `description`, `workflows/generic.md`.

---

## Success Criteria Verification

Re-run at close against the ephemeral worktree.

### Criterion 1 (SC1): Red Flags content

**Method:** `grep -c 'Dangerous container defaults\|Unpinned CI action with secrets' SKILL.md`; `grep -c 'Confirmed typosquat / impersonation\|Removed for cause\|Mutable CI ref with privileged access\|Tree terms & precedence' SKILL.md`

**Evidence:**
```
0
4
```
**Result:** PASS

### Criterion 2 (SC2): Terms & precedence block

**Method:** `grep -n 'Tree terms' SKILL.md`; read lines 96–114.

**Evidence:** tree nodes at lines 96/98 reference Tree terms; `**Tree terms & precedence:**` at line 111, outside fence, 3 bullets (CRITICAL flag, Unpatched CVE ← `references/criteria.md` §4.3, Precedence).

**Result:** PASS

### Criterion 3 (SC3): CI wording aligned

**Method:** `grep -c 'unverified third-party publisher' workflows/ci-action.md references/criteria/ci-action.md SKILL.md`; desk-check evals 27, 15, 14.

**Evidence:**
```
workflows/ci-action.md:1
references/criteria/ci-action.md:1
SKILL.md:1
```
Eval 27 → CONDITIONAL; eval 15 → REJECTED; eval 14 → APPROVED.

**Result:** PASS

### Criterion 4 (SC4): `references/classifier.md`

**Method:** file read + history-ref grep.

**Evidence:** 121 lines; `grep -cE '\.projex|Phase [0-9]|M[0-9]\.[0-9]|milestone'` → `0`; `grep -c 'brew install <formula>'` → `2`; sections Rule, Tie-Breaking, Confidence Examples, Type 8 Sub-Rubric, Routing Overrides, Extended Signal Patterns, Worked Hybrid Examples (5), Edge-Case Discipline.

**Result:** PASS

### Criterion 5 (SC5): no `.projex` in runtime

**Method:** `grep -rn '\.projex' SKILL.md workflows references scripts`

**Evidence:** no output.

**Result:** PASS

### Criterion 6 (SC6): labels stripped

**Method:** `grep -rnE 'Phase [0-9] / M|\(Phase [0-9], M|milestone' SKILL.md workflows references`; `grep -c '^## Phase' workflows/generic.md`

**Evidence:** no output; `4`.

**Result:** PASS

### Criterion 7 (SC7): Reference Files paths exist

**Method:** python3 path check from plan.

**Evidence:** `24 paths; missing: []`

**Result:** PASS

### Criterion 8 (SC8): taxonomy def

**Method:** greps on def.

**Evidence:** `grep -c 'references/classifier.md'` → 3; `grep -c 'Homebrew core → \*\*desktop-app'` → 0; Open Question marked `[x]`.

**Result:** PASS

### Criterion 9 (SC9): eval desk-check

**Method:** Executor traced each case through new `SKILL.md` Step N + routed workflow/addendum text, pulling prompts/expectations from `evals/evals.json` (full table in the execution log, § Completion). Close did not re-trace; it re-verified the structural checks above.

**Evidence:** evals 2, 3, 4, 5, 7, 9, 12, 13, 14, 15, 20, 25, 26, 27, 30 → all Pass (e.g. 27 → CONDITIONAL via verified-publisher tag pin; 15 → REJECTED via unverified publisher + secrets; 30 → CONDITIONAL since the bridge is auditor-rated; 7 and 5 → CONDITIONAL since fixed releases exist).

**Result:** PASS

### Criterion 10 (SC10): untouched files

**Method:** `git diff --stat` for `evals scripts STEWARDSHIP.md`; skeleton/`description` diff grep; new `.ps1` refs; JSON parse.

**Evidence:** 0 lines of diff stat; 0 skeleton/description hits; 0 new `.ps1` refs; `evals ok`.

**Result:** PASS

### Acceptance Criteria Summary

| Criterion | Method | Result | Evidence |
|-----------|--------|--------|----------|
| SC1 | grep pair | Pass | 0 / 4 |
| SC2 | read + grep | Pass | line 111 block |
| SC3 | grep + desk-check | Pass | 1/1/1 |
| SC4 | file checks | Pass | 121 lines, 0 history refs |
| SC5 | grep | Pass | no output |
| SC6 | grep | Pass | no output; 4 |
| SC7 | python3 | Pass | missing: [] |
| SC8 | grep | Pass | 3; 0 |
| SC9 | desk-check | Pass | 15/15 |
| SC10 | diff stat | Pass | untouched |

**Overall:** 10/10 criteria passed.

---

## Deviations from Plan

1. **Worktree header override** — Planned: `Worktree:` per plan (was `No`). Actual: orchestrator set `Yes` (concurrent sibling plans executing in own worktrees; main checkout stays on base). Impact: none; start-execution commit on base (48817d9) carries the flip.
2. **Do/Verify-Projex "Encouraged" not dispatched** — executed and self-verified directly. Impact: none; full desk-check recorded.
3. **Step 5 pointer blank line** — separate blockquote (see Step 5).
4. **Step 4 via script** — same net change.
5. **Close: nav entry added** — plan has no `Nav:` header; repo convention + plan's Out of Scope ("close-projex records the nav revision-log entry") → nav `2604070218-install-auditor-subject-typed-redesign-nav.md` updated at close (Last Revised, Recent Progress, Phase 6 maintenance bullet, Revision Log row).

---

## Issues Encountered

### Issue 1: python3 bytes regex SyntaxError
- **Description:** em dash in a bytes literal regex rejected (Step 4).
- **Severity:** Low
- **Resolution:** `\xe2\x80\x94` escape; no files changed by failed run.
- **Time Impact:** ~1 min
- **Prevention:** use `str` regex with explicit `encoding='utf-8', newline=''` for non-ASCII markdown.

### Issue 2: `close-precheck` / `projex-tree` unusable at close
- **Description:** `close-precheck.sh` returned `ERROR=recorded Worktree Path is missing or inaccessible` — the log's `Worktree Path` header is repo-relative (`install-auditor-skill/.projexwt/...`), not absolute. `projex-tree.sh` failed on a missing `.projex-tree.py` helper in the skills directory. Both are advisory; close proceeded on direct git evidence (ref-to-ref diff, commit list, worktree status).
- **Severity:** Low
- **Resolution:** manual verification.
- **Time Impact:** ~2 min
- **Prevention:** execute-projex should record `Worktree Path` absolute; framework install should ship `.projex-tree.py`.

---

## Key Insights

**Rationale promoted:** `references/classifier.md` (classifier rule + Homebrew boundary) and `SKILL.md` § Tree terms & precedence (Red Flag conditions, CRITICAL-flag bridge, "unpatched" definition, precedence) are the shipped homes for rationale that previously lived only in the taxonomy def / plan.

### Lessons Learned

1. **Red Flags drift from workflows silently**
   - Context: Red Flags predated subject workflows (dispatcher refactor carried them over from the monolith); addenda then graded the same patterns finer.
   - Insight: a subject-independent list must be conditioned to the strictest subject rubric's REJECTED path, or dropped.
   - Application: when a workflow's Toward REJECTED/CONDITIONAL changes, grep `SKILL.md` Red Flags for the same pattern.

2. **Auditor-rated bridge over mechanical mapping**
   - Context: eval 30 matches both a Toward REJECTED and a Toward CONDITIONAL bullet in cli-binary.
   - Insight: lists overlap; mechanical "every Toward REJECTED item = CRITICAL" would flip eval 30.
   - Application: keep tree node 1 judgment-based; record rating + reason in Risk Flags.

### Pattern Discoveries

1. **Promote-then-point** — design record (taxonomy def) keeps identity/history; shipped file is runtime-canonical; def carries a Runtime-copy pointer so drift is directional.

### Gotchas / Pitfalls

1. **Precheck path format**
   - Trap: relative `Worktree Path` in the log breaks `close-precheck`.
   - How encountered: precheck ERROR at close.
   - Avoidance: absolute path in the log header.

### Technical Insights

- `workflows/generic.md` "Phase 1–4" headings are runtime procedure steps; label greps must not touch them.
- Nav Revision Log is appended chronologically-by-landing, not by date sort; newest row is last.

---

## Recommendations

### Immediate Follow-ups
- [ ] Add evals: `preact` typosquat false-positive; tag-pinned verified action with secrets (deferred to avoid colliding with eval-runner plan's `evals.json` changes).
- [ ] Sibling plans (`2610161849-python-script-ports-plan.md`, `2610161850-eval-runner-harness-plan.md`) will conflict with this close in the nav (`2604070218-install-auditor-subject-typed-redesign-nav.md` header/Recent Progress/Revision Log); resolve by keeping both entries.

### Future Considerations
- Container-internal tensions (plan Out of Scope a–c) for the container-image stewardship review.
- `workflows/cli-binary.md` Toward REJECTED "Project abandoned" vs tree "Abandoned with no alternative → CONDITIONAL".
- Later dispatcher-compression plan must carry the new Red Flags / terms block / Reference Files text forward verbatim.

### Plan Improvements
- Add a `Nav:` header when the plan expects a nav entry at close, so close is not inferring it from Out of Scope prose.

---

## Related Projex Updates

### Documents to Update
| Document | Update Needed |
|----------|---------------|
| 2610161852-dispatcher-rubric-consistency-plan.md | Complete; moved to `closed/` |
| 2610161852-dispatcher-rubric-consistency-log.md | Complete; moved to `closed/` |
| 2604070218-install-auditor-subject-typed-redesign-nav.md | Revision Log + status entries (in place) |
| 2604070300-install-auditor-subject-type-taxonomy-def.md | Already updated by Step 5; stays in `.projex/` (never closed) |

### New Projex Suggested
| Type | Description |
|------|-------------|
| Plan | Add evals for typosquat false-positive and tag-pinned verified action with secrets |
| Plan | Dispatcher size compression (blocked-by this plan's text) |
| Review | Container-image stewardship: reconcile plan Out-of-Scope items a–c |

---

## Appendix

### Commits (ephemeral branch)
```
a9be647 projex: step 1 - add shipped classifier reference
eda1d9d projex: step 2 - dispatcher Red Flags, tree terms, classifier pointer
ac047b8 projex: step 3 - align ci-action pin rules with dispatcher
05534f6 projex: step 4 - strip roadmap labels from runtime files
8e7c5f0 projex: step 5 - taxonomy def runtime pointer and Homebrew fix
3fdc7c2 projex: complete dispatcher-rubric-consistency
```

### Close-time verification output
```
SC5: (no output)   SC6: (no output) / 4   SC7: 24 paths; missing: []
SC1: 0 / 4   SC3: 1/1/1   SC4: 0 / 2   SC8: 3 / 0   SC10: 0 / 0 / 0, evals ok
<!--/--> balance: 1/1 in all edited workflows + remote-integration addendum
```

### References
- Plan: 2610161852-dispatcher-rubric-consistency-plan.md
- Log: 2610161852-dispatcher-rubric-consistency-log.md
- Nav: 2604070218-install-auditor-subject-typed-redesign-nav.md
- Def: 2604070300-install-auditor-subject-type-taxonomy-def.md
- Siblings: 2610161849-python-script-ports-plan.md, 2610161850-eval-runner-harness-plan.md
