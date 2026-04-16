# Walkthrough: Remote Integration Workflow — M4.4

> **Execution Date:** 2026-04-16
> **Completed By:** Claude (sonnet subagent, orchestrated)
> **Source Plan:** 2604161000-remote-integration-workflow-m44-plan.md
> **Result:** Success

---

## Summary

All four plan steps executed cleanly: `references/criteria/remote-integration.md` and `workflows/remote-integration.md` created, `SKILL.md` dispatch row 9 wired live, and evals 24–25 appended. Type 9 (remote-integration) now has a dedicated workflow — the last fallback route to `workflows/generic.md` for non-zero subject types is closed. Eval coverage grows from 24 to 26 cases.

---

## Objectives Completion

| Objective | Status | Notes |
|-----------|--------|-------|
| Create `workflows/remote-integration.md` | Complete | 176 lines — Identify / Evidence A+B / Rubric §4.1–4.6 / Verdict Notes |
| Create `references/criteria/remote-integration.md` | Complete | 91 lines — 5 sections with tables + scoring impact + tier thresholds |
| Update `SKILL.md` dispatch row 9 + Reference Files | Complete | 4 edits: signal table (pre-existing), dispatch row 9 Live, workflow bullet, addendum bullet |
| Add evals 24 and 25 | Complete | 26 total entries; ids 0–23 unchanged; JSON valid |

---

## Execution Detail

### Step 1: Create `references/criteria/remote-integration.md`

**Planned:** 5-section criteria addendum (~125–160 lines) with OAuth scope table, data residency table, ToS table, breach history table, tier thresholds.

**Actual:** Created with all 5 sections. File is 91 lines — shorter than the ~125–160 estimate because the tables are tighter than M4.3's capability-scope matrix. Tier Thresholds section has all 3 tiers with concrete examples.

**Deviation:** Line count (91 vs ~125–160 estimated). Content complete; no missing sections. Tighter tables are a valid execution of the same spec.

**Files Changed:**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `references/criteria/remote-integration.md` | Created | Yes | 91 lines — §1 OAuth Scope, §2 Data Residency, §3 ToS & Data Sharing, §4 Breach History & Security Posture, §5 Tier Thresholds |

**Verification:** File exists, all 5 sections present, tier thresholds cover Tier 1/2/3 with remote-integration-specific signals. ✓

---

### Step 2: Create `workflows/remote-integration.md`

**Planned:** ~200–300 lines, standard template shape — Identify (3 subsections) / Evidence Part A (5 checks) / Evidence Part B (5 checks) / Subject Rubric (6 sections §4.1–4.6) / Subject Verdict Notes.

**Actual:** Created, 176 lines. All template sections present. No sub-rubric labels (uniform trust model — matches M4.4 design decision). References `references/criteria/remote-integration.md` throughout.

**Deviation:** Line count (176 vs ~200–300 estimated). All sections present and correctly structured.

**Files Changed:**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `workflows/remote-integration.md` | Created | Yes | 176 lines — Identify/Evidence A+B/Rubric §4.1–§4.6/Verdict Notes |

**Verification:** `grep "^## " workflows/remote-integration.md` returns Identify, Evidence — Part A, Evidence — Part B, Subject Rubric, Subject Verdict Notes. Criteria addendum reference confirmed. ✓

---

### Step 3: Update `SKILL.md`

**Planned:** 3 edits — dispatch row 9 Live, workflow bullet in Reference Files, addendum bullet in Reference Files.

**Actual:** All 3 edits applied. `grep -n "remote-integration" SKILL.md` returns 4 hits: signal table row 9 (pre-existing), dispatch table row 9 → `workflows/remote-integration.md` Live, workflow reference bullet, addendum reference bullet.

**Deviation:** None.

**Files Changed:**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `SKILL.md` | Modified | Yes | Row 9: `workflows/generic.md` Fallback → `workflows/remote-integration.md` Live — Phase 4 (M4.4); 2 Reference Files bullets added |

**Verification:** `rg "remote-integration" SKILL.md` → 4 hits (line 42 signal table, line 70 dispatch, line 220 workflow bullet, line 230 addendum bullet). ✓

---

### Step 4: Update `evals/evals.json`

**Planned:** Append ids 24 (Slack official OAuth app, Tier 1 APPROVED) and 25 (unknown vendor with overprivileged Google scopes via phishing email, Tier 3 REJECTED). Total: 26 entries.

**Actual:** Both entries appended. JSON parses without errors. Count: 26. Ids 0–23 unchanged.

**Deviation:** None.

**Files Changed:**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `evals/evals.json` | Modified | Yes | ids 24 + 25 appended; 26 total entries |

**Verification:** `node -e "const d=JSON.parse(...); console.log(d.evals.length);"` → 26. Ids 24 + 25 confirmed present. ✓

---

## Complete Change Log

> **Derived from:** `git diff --stat master..HEAD`

### Files Created
| File | Purpose | Lines | In Plan? |
|------|---------|-------|----------|
| `workflows/remote-integration.md` | Type 9 subject workflow | 176 | Yes |
| `references/criteria/remote-integration.md` | Type 9 criteria addendum | 91 | Yes |
| `.projex/2604161000-remote-integration-workflow-m44-log.md` | Execution log | 56 | Yes (artifact of execute-projex) |

### Files Modified
| File | Changes | Lines Affected | In Plan? |
|------|---------|----------------|----------|
| `SKILL.md` | Dispatch row 9 Live + 2 Reference Files bullets | ~4 lines | Yes |
| `evals/evals.json` | ids 24 + 25 appended | +30 lines | Yes |
| `.projex/2604161000-remote-integration-workflow-m44-plan.md` | Status → Complete | 2 lines | Yes |

### Planned But Not Changed
*(none — all 4 plan steps executed as specified)*

---

## Success Criteria Verification

| Criterion | Method | Result | Evidence |
|-----------|--------|--------|----------|
| `workflows/remote-integration.md` exists with template sections | `grep "^## "` | Pass | Identify / Evidence A+B / Subject Rubric / Subject Verdict Notes ✓ |
| `references/criteria/remote-integration.md` exists with 5 sections | File read + section scan | Pass | §1–§5 all present ✓ |
| `SKILL.md` row 9 routes to `workflows/remote-integration.md` Live | `grep "remote-integration" SKILL.md` | Pass | Line 70: Live — Phase 4 (M4.4) ✓ |
| `SKILL.md` Reference Files lists both new files | `grep "remote-integration" SKILL.md` | Pass | Lines 220 + 230 ✓ |
| `evals/evals.json` has ids 24 and 25 | JSON parse + id lookup | Pass | Both present, 26 total ✓ |
| ids 0–23 unchanged | Count filter `e.id <= 23` | Pass | 24 entries ✓ |
| JSON parses without errors | `JSON.parse(FILE_CONTENT)` | Pass | No errors ✓ |

**Overall:** 7/7 criteria passed.

---

## Deviations from Plan

### Deviation 1: Criteria addendum shorter than estimated
- **Planned:** ~125–160 lines
- **Actual:** 91 lines
- **Reason:** Remote-integration criteria tables are narrower than agent-extension's capability-scope matrices. The 5 sections are complete; the content is denser, not missing.
- **Impact:** None — all required content present.
- **Recommendation:** No plan update needed; line-count estimates for criteria addenda vary by subject complexity.

### Deviation 2: Workflow shorter than estimated
- **Planned:** ~200–300 lines
- **Actual:** 176 lines
- **Reason:** Remote-integration has no sub-rubrics and no multi-channel distribution table (unlike cli-binary's 8-channel table). Uniform trust model = tighter Identify section.
- **Impact:** None — all template sections present and correctly structured.
- **Recommendation:** No plan update needed.

---

## Key Insights

### Lessons Learned

1. **Orchestration hand-off remains stable across M4.x.**
   - Context: Opus planner produced a complete plan; sonnet executor consumed it with no clarification rounds. Fourth consecutive milestone following this pattern.
   - Application: M4.5 eval gate can follow the same shape. Plan-then-execute split is now the confirmed default for Phase 4.

2. **Line-count estimates for Phase 4 workflows skew high.**
   - Context: M4.3 (agent-extension) was 230 lines / 125 lines; M4.4 came in at 176 / 91. Both complete. Estimates are conservative — simpler trust models yield tighter files.
   - Application: For M4.5 (eval gate) and Phase 5, don't use line count as a quality proxy. Section completeness is the right signal.

### Pattern Discoveries

1. **No-install subject types yield simpler workflow files.**
   - Observed in: M4.4 (remote-integration) vs M4.1 (desktop-app, 360 lines) and M4.2 (cli-binary, 264 lines).
   - Remote integrations have no code artifact, no install vector, no binary inspection — the Identify section is simpler and Evidence Part A has fewer automated checks.
   - Reuse potential: Future Type 9 expansions or similar "cloud-hosted service" types will inherit this shape.

2. **Uniform trust model → no sub-rubrics → shorter file.**
   - Observed in: M4.4. Unlike M4.3 (8a/8b/8c sub-rubrics for MCP/plugin/skill), remote integrations share a single credential-grant trust model. Zero sub-rubric labels needed.
   - Application: Plan the sub-rubric decision early — it's the biggest workflow structure choice per Phase 4 milestone.

### Gotchas / Pitfalls

1. **"No local code" doesn't mean "simple audit."**
   - Trap: Remote integrations look simpler because nothing installs locally. The audit is actually research-heavy (ToS review, breach history search, compliance doc hunting).
   - Evidence Part B (5 checks) is where most of the work happens — more web research than local artifact inspection.
   - Avoidance: Eval prompts for Type 9 should include realistic research complexity in `expected_output`.

---

## Recommendations

### Immediate Follow-ups
- [ ] M4.5 — Phase 4 eval gate (≥1 case per long-tail workflow; M4.1–M4.4 each have 2 already — M4.5 may be trivially satisfiable or require checking Type 9 specifically)
- [ ] Phase 5 M5.1 — Tighten classifier now that all 9 subject-specific workflows are live

### Future Considerations
- Eval harness gap persists (Phase 6 cross-phase concern). All eval verification remains manual JSON validation only.
- Phase 5 (default-off generic) now unblocked — all 9 specific workflows live.

### Plan Improvements
- Plan was well-scoped. Line-count estimates could be dropped in favor of "section completeness" as the acceptance signal — more reliable across subject types.
