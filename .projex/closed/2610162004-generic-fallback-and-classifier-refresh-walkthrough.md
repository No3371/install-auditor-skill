# Walkthrough: Generic Fallback + Classifier Refresh

> **Execution Date:** 2026-10-16
> **Completed By:** Claude (executor subagent) | closed by close-projex subagent
> **Source Plan:** 2610162004-generic-fallback-and-classifier-refresh-plan.md
> **Parent:** 2610162004-generic-fallback-and-classifier-refresh-plan.md
> **Duration:** ~21 min (20:12–20:33 per execution log timestamps)
> **Result:** Success

---

## Summary

Classifier, `SKILL.md` Step 0 rows and the generic fallback refit in one routing contract. `references/classifier.md` gained 8 exact edits (Type 8 sub-rubric definitions, narrowed npm override, remote-MCP / OAuth-only / `source: npm` / PowerShell pipe-to-shell / portal overrides, signal rows 7–9, worked examples 5–8). `SKILL.md` Step 0 rows 7, 8, 9, 0 reworded (15,484 → 15,482 B). `workflows/generic.md` fully rewritten (80 → 151 lines) with Execution & trust grant and Source provenance checks, Quick-by-default / Standard-on-HIGH shape, Moderate confidence cap, and a re-route window. Orchestrator-accepted decisions encoded: hosted MCP connector adding tools → agent-extension 8a; eval 34 → cli-binary medium.

---

## Objectives Completion

| Objective | Status | Notes |
|-----------|--------|-------|
| G-1 Generic Phase 3 refit (execution/trust grant, provenance) | Complete | Canonical rows get generic handling; ratings as `Toward …` notes |
| G-2 Shape + confidence cap | Complete | Quick default, Standard on any HIGH/CRITICAL; Audit confidence `Moderate` at most; `Skipped (generic fallback)` |
| G-3 PowerShell pipe-to-shell signals + eval 34 route | Complete | Signals in `SKILL.md` row 7 and `classifier.md`; opaque-URL pipe-to-shell → cli-binary, medium (override + example 8) |
| G-4 Phase 2 as sole re-route | Complete | Names itself the only re-route; window closes when Phase 3 starts |
| G-5 Unanswered clarification recorded | Complete | Phase 4 Recommendation records question + candidates |
| RI-8 / F13(b) remote MCP / connector routing | Complete | Tool-adding connector → agent-extension 8a + remote-integration OAuth sub-step; OAuth-only SaaS/AI app → remote-integration |
| F13(a) npm override narrowed | Complete | "installed with `npm install`"; `source: npm` marketplace plugin → 8b (example 6) |
| F13(c) / F14 stale Type 8 signals | Complete | "MCP manifest", `claude-code/plugins/*`, stale host list removed |

---

## Execution Detail

> Derived from git history (`242310a..projex/2610162004-generic-fallback-and-classifier-refresh`) and the execution log.

### Preflight

**Planned:** shared-plan outputs present, A2 no-overlap check, baselines.
**Actual:** shared walkthrough present; no `projex/2610161941*` branch; carve-out greps 1 and 1; `Sole exception` 1; skip wording 1; `criteria.md` skip contract 1; `git log 20843cc..HEAD` over the 3 files empty. S0 = 15,484 B. Baseline: `41 evals, 248 assertions (82 deterministic, 166 model-graded)`; evals 12 OK; tests 19 OK (skipped=6).
**Deviation:** None.

### Step 1: Refresh `references/classifier.md`

**Planned:** 8 exact replacements C1–C8.
**Actual:** all 8 matched once, no re-anchoring. Result 150 lines / 12,904 B (= simulated). Commit `f7a7cd1`.
**Deviation:** None.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `references/classifier.md` | Modified | Yes | 123 → 150 lines: 8a/8b/8c definitions; npm override narrowed; new overrides; signal rows 7/8/9; worked examples 5 reworded, 6–8 added |

**Verification:** stale strings 0; route strings 4; worked examples 8; `irm … \| iex` 2; `Sole exception` 1.

### Step 2: Refresh `SKILL.md` Step 0 rows 7, 8, 9, 0

**Planned:** 4 exact replacements S1–S4, net −2 B.
**Actual:** all 4 matched once; done directly with Edit (no do-projex dispatch; step marked Encouraged). 15,482 B. Commit `a32e02f`.
**Deviation:** None.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `SKILL.md` | Modified | Yes | Step 0 signal-table rows 7, 8, 9, 0 only (4+/4−) |

**Verification:** `wc -c` 15,482 (≤ 15,500, ≤ S0); `MCP manifest` 0; `no local code or MCP server` 1.

### Step 3: Rewrite `workflows/generic.md`

**Planned:** full replacement with the plan block.
**Actual:** block extracted programmatically from the plan; plan's exact-equality check printed `True`. 151 lines / 7,970 B (≤ 160). Four `## Phase N — ` headers; three `### Toward …` headings. Commit `0144ff7`.
**Deviation:** None.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `workflows/generic.md` | Modified | Yes | 80 → 151 lines, full rewrite |

**Verification:** all required phrases present once; old "No subject-specific verdict overrides" 0.

### Completion

**Actual:** consistency script, harness, diff-stat and paper traces T1–T9; plan status → Complete, `Log:` header added; execution log committed (`b9764a3`). Worktree `__pycache__` dirs from harness runs removed.

---

## Complete Change Log

> **Derived from:** `git diff --stat 242310a..projex/2610162004-generic-fallback-and-classifier-refresh` — authoritative record.

### Files Created
| File | Purpose | Lines | In Plan? |
|------|---------|-------|----------|
| `.projex/2610162004-generic-fallback-and-classifier-refresh-log.md` | Execution log | 73 | Yes (required by execute workflow) |

### Files Modified
| File | Changes | Lines Affected | In Plan? |
|------|---------|----------------|----------|
| `references/classifier.md` | 8 exact edits | +51/− (123 → 150 lines) | Yes |
| `SKILL.md` | Step 0 rows 7, 8, 9, 0 | 4+/4− | Yes |
| `workflows/generic.md` | Full rewrite | +111/− (80 → 151 lines) | Yes |
| `.projex/2610162004-generic-fallback-and-classifier-refresh-plan.md` | Status → Complete; `Log:` header | 3 | Yes (lifecycle) |

### Files Deleted
None.

### Planned But Not Changed
None. `evals/` untouched, as planned.

---

## Success Criteria Verification

### Criterion 1: `generic.md` equals Step 3 text, ≤ 160 lines, required phrases
**Evidence:** plan's exact-equality check `True`; 151 lines; all 10 required phrases present once.
**Result:** PASS

### Criterion 2: `generic.md` keeps Phase 4 literal and four Phase headers
**Evidence:** `**Classification confidence:** Low — generic fallback` x1; `## Phase N — ` x4.
**Result:** PASS

### Criterion 3: `classifier.md` After strings present once; stale strings absent; examples 1–8; `Sole exception` intact
**Evidence:** consistency script `OK` (re-run at close); worked examples 8; stale strings 0.
**Result:** PASS

### Criterion 4: `SKILL.md` rows; budget
**Evidence:** `15482 SKILL.md` (≤ 15,500; ≤ S0 15,484).
**Result:** PASS

### Criterion 5: Only 3 files change; `evals/` untouched; harness green
**Evidence:** `git diff --stat 242310a..branch` → `SKILL.md`, `references/classifier.md`, `workflows/generic.md` + log/plan; `evals/` 0 paths. `41 evals, 248 assertions (82 deterministic, 166 model-graded)`; evals 12 OK; tests 19 OK (skipped=6) — re-run at close.
**Result:** PASS

### Criterion 6: Paper traces T1–T9
**Evidence:** log "Full verification": T1 agent-extension 8a high; T2 remote-integration high; T3 agent-extension 8b high; T4 registry-package (eval 40 unchanged); T5 cli-binary medium → REJECTED; T6 generic low → CONDITIONAL, confidence ≤ Moderate; T7 generic low → CONDITIONAL; T8 generic low → REJECTED; T9 cli-binary high.
**Result:** PASS

### Acceptance Criteria Summary

| Criterion | Method | Result | Evidence |
|-----------|--------|--------|----------|
| generic rewrite exact + contents | equality check + greps | Pass | above |
| classifier edits | greps + consistency script | Pass | `OK` |
| `SKILL.md` rows + budget | greps + `wc -c` | Pass | 15,482 B |
| Only 3 files; evals untouched | `git diff --stat` | Pass | above |
| Harness green | validate + unittest x2 | Pass | 12 / 19 (skipped 6) |
| Routing + verdict behaviour | T1–T9 | Pass | log |

**Overall:** 6/6 criteria passed.

---

## Deviations from Plan

None. All 8 + 4 exact replacements matched at first attempt; Step 3 byte-identical to the plan block; no sibling plan touched the three files.

---

## Issues Encountered

### Issue 1: Precheck WARN
- **Description:** `execute-precheck` warned about 8 uncommitted changes in the main checkout (sibling planners' untracked plan files).
- **Severity:** Low
- **Resolution:** Ignored by design.

### Issue 2: Cosmetic BrokenPipeError
- **Description:** `run_evals.py validate | head -1` raised `BrokenPipeError` when the pipe closed early; first line correct.
- **Severity:** Low
- **Resolution:** None needed.

### Issue 3: Base advanced during execution
- **Description:** Sibling plans' status commits landed on base while this ran.
- **Severity:** Low
- **Resolution:** No overlap with the three files; no conflicts at squash.

---

## Key Insights

**Rationale promoted:** none needed (routing rationale lives in the shipped `references/classifier.md` overrides and worked examples).

### Lessons Learned

1. **Exact old → new pairs make multi-file edits conflict-free**
   - Context: 12 string replacements plus one full-file block, all matched first time.
   - Insight: planning-time simulation against base removes re-anchoring work.
   - Application: keep for concurrent-sibling refreshes.

### Pattern Discoveries

1. **Rule in classifier, summary in dispatcher**
   - Observed in: Step 1 before Step 2.
   - Description: put detail in `references/classifier.md` and keep `SKILL.md` rows net-zero in size.
   - Reuse potential: any future signal-table change under the `SKILL.md` size ceiling.

### Gotchas / Pitfalls

1. **Routing change leaves eval 34 stale**
   - Trap: eval 34's `workflow: generic` and routing assertion no longer match; removing it leaves generic with 2 cases (`MIN_CASES_PER_WORKFLOW = 3`), so `validate` fails unless the eval plan adds a generic case in the same change.
   - How encountered: planning (Impact Analysis), confirmed in T5.
   - Avoidance: eval plan must re-expect eval 34 and add a generic case together.

### Technical Insights

- Harness runs create ignored `__pycache__/` dirs in the worktree; remove before close.

---

## Recommendations

### Immediate Follow-ups
- [ ] Eval plan: eval 34 `workflow` → `cli-binary`, routing assertion → "Subject type is cli-binary", expected_output → cli-binary medium + REJECTED, keep REJECTED / iex / shortener assertions; add at least one generic case in the same change (suggest T8 unsolicited root CA → REJECTED); optional eval 33 certificate-issuer concept; new routing cases for T1 (remote MCP → 8a), T3 (`source: npm` plugin → 8b), T9 (vendor `irm | iex` → cli-binary high); generic reports may now use the full template.
- [ ] agent-extension refresh: accept remote 8a with no local code and `.mcpb` / `.dxt`; run remote-integration grant checks as an OAuth sub-step (cite its addendum §1, §5, §6 by section); accept `/plugin install` from marketplaces of any `source`; align wording to `classifier.md` 8a/8b/8c.
- [ ] cli-binary refresh: name PowerShell pipe-to-shell forms and URL shorteners / paste sites as unverifiable sources in Identify and Distribution research.
- [ ] Remote-integration scope note (hand-off item, not yet applied): the Type 9 workflow Identify row "Add connector" (remote MCP over HTTP + OAuth, no local code) is route-agnostic, so nothing contradicts, but a short note that tool-adding connectors route to agent-extension 8a would align it with this decision (revise of the closed remote-integration plan output).
- [ ] Orchestrator: STEWARDSHIP note for the generic and classifier rows (both refreshed 2026-10-16).

### Future Considerations
- Rating thresholds (root-CA tiers, provenance MEDIUM/HIGH) are policy and sit in Subject Verdict Notes for local retuning.
- MCP authorization details (CIMD, RFC 9728 / 8707) deliberately not encoded; belong in the agent-extension / remote-integration rubrics once verified.

### Plan Improvements
- None.

---

## Related Projex Updates

### Documents to Update
| Document | Update Needed |
|----------|---------------|
| 2610162004-generic-fallback-and-classifier-refresh-plan.md | Marked Complete; walkthrough link; moved to `closed/` |
| 2610162004-generic-fallback-and-classifier-refresh-log.md | Moved to `closed/` |
| 2604070218-install-auditor-subject-typed-redesign-nav.md | Maintenance-pass entry (header, Recent Progress, checklist, Revision Log) |
| 2610161927-remote-integration-generic-stewardship-review-eval.md | Source eval; left active (eval refresh still open) |

### New Projex Suggested
| Type | Description |
|------|-------------|
| Plan | Eval refresh covering eval 34 re-expectation, generic case count and new routing cases (see Immediate Follow-ups) |

---

## Appendix

### References
- Commits on `projex/2610162004-generic-fallback-and-classifier-refresh`: `f7a7cd1` (step 1), `a32e02f` (step 2), `0144ff7` (step 3), `b9764a3` (complete)
- Base at branch point: `242310a`
