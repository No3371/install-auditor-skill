# Walkthrough: Desktop App Workflow M4.1

> **Execution Date:** 2026-04-15
> **Completed By:** Claude (Sonnet 4.6 — executor) + Claude (Opus 4.6 — planner/closer)
> **Source Plan:** [2604151200-desktop-app-workflow-m41-plan.md](2604151200-desktop-app-workflow-m41-plan.md)
> **Duration:** Single session
> **Result:** Success

---

## Summary

Created Type 6 desktop-app workflow (`workflows/desktop-app.md`, 360 lines) and criteria addendum (`references/criteria/desktop-app.md`, 162 lines). Wired `SKILL.md` dispatch table row 6 and added 2 eval cases (ids 18, 19). All 7 success criteria passed. First Phase 4 deliverable — desktop apps no longer fall through to `workflows/generic.md`.

---

## Objectives Completion

| Objective | Status | Notes |
|-----------|--------|-------|
| Create `workflows/desktop-app.md` | Complete | 360 lines, 4 template sections, cross-platform (Win/Mac/Linux) |
| Create `references/criteria/desktop-app.md` | Complete | 162 lines, 7 sections (channel trust, signing, installer risk, sandbox, auto-update, telemetry, tiers) |
| Wire SKILL.md dispatch row 6 | Complete | `generic.md` → `desktop-app.md` (Live — Phase 4 M4.1) |
| Add Type 6 evals | Complete | id 18 (Firefox/winget APPROVED), id 19 (fake VLC Pro REJECTED) |
| Homebrew boundary clarification | Complete | `brew install --cask` → Type 6; `brew install` (formulae) → Type 7 |

---

## Execution Detail

### Step 1: Create `references/criteria/desktop-app.md`

**Planned:** New addendum with 7 sections covering distribution channel trust signals, code signing standards, installer type risk, sandboxing, auto-update risk, telemetry, tier thresholds.

**Actual:** Created as planned. 162 lines. 7 sections present: Distribution Channel Trust Signals (11-row table), Code Signing Standards (10-row table), Installer Type Risk Classification (10-row table), Sandboxing Assessment (6-row table), Auto-Update Mechanism Risk (5-row table), Telemetry & Data Collection, Tier Thresholds (Tier 1/2/3 with specific criteria). Each section includes scoring impact guidance.

**Deviation:** None.

**Files Changed:**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `references/criteria/desktop-app.md` | Created | Yes | 162 lines, complete addendum |

**Verification:** File exists; all 7 sections present. Commit f957bc5.

---

### Step 2: Create `workflows/desktop-app.md`

**Planned:** Type 6 workflow following Identify / Evidence / Subject Rubric / Subject Verdict Notes template.

**Actual:** Created as planned. 360 lines. Structure: HTML comment header → intro → Identify (3 sub-sections: distribution channel table with 11 rows, metadata extraction, required context checklist) → Evidence Part A (tier triage with Tier 1/2/3 guidance) → Evidence Part B (10 core research questions, research methodology for distribution channel/signing/installer/incidents, 12-row audit coverage tracking table) → Subject Rubric (§4.1–4.6 desktop-app-specialized) → Subject Verdict Notes (toward REJECTED/CONDITIONAL/APPROVED with specific triggers).

**Deviation:** None. Content matches plan specification.

**Files Changed:**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `workflows/desktop-app.md` | Created | Yes | 360 lines, all 4 template sections |

**Verification:** `grep "^## " workflows/desktop-app.md` confirms all required sections. Commit cb04a17.

---

### Step 3: Update `SKILL.md`

**Planned:** Dispatch table row 6 → `desktop-app.md`; add 2 Reference Files bullets.

**Actual:** Executed as planned. Row 6 changed from `generic.md (Fallback)` to `desktop-app.md (Live — Phase 4 M4.1)`. Two Reference Files bullets inserted after the ide-plugin entries: workflow bullet after `workflows/ide-plugin.md` line, addendum bullet after `references/criteria/ide-plugin.md` line.

**Deviation:** None.

**Files Changed:**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `SKILL.md` | Modified | Yes | Line 67: row 6 routing; Lines 217, 224: reference bullets |

**Verification:** `grep desktop-app SKILL.md` shows 4 hits (classifier, dispatch, 2 reference bullets). Commit e0bf7ce.

---

### Step 4: Update `evals/evals.json`

**Planned:** Add eval ids 18 and 19 for positive and negative Type 6 paths.

**Actual:** Appended both entries to the evals array. id 18: `winget install Mozilla.Firefox` with 6 assertions (subject type, vendor, channel, signing, APPROVED verdict, audit confidence). id 19: fake VLC Pro from `free-software-downloads.xyz` with 7 assertions (subject type, third-party source, repackaged branding, unsigned exe, REJECTED verdict, audit coverage, audit confidence). Total evals: 20. ids 0–17 unchanged.

**Deviation:** None.

**Files Changed:**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `evals/evals.json` | Modified | Yes | +29 lines; ids 18, 19 appended |

**Verification:** JSON valid; 20 total evals; ids 18/19 present with correct assertions. Commit af578dd.

---

## Complete Change Log

> Derived from: `git diff --stat 1050b81..2f9948d`

### Files Created
| File | Purpose | Lines | In Plan? |
|------|---------|-------|----------|
| `workflows/desktop-app.md` | Type 6 subject-specific workflow | 360 | Yes |
| `references/criteria/desktop-app.md` | Type 6 criteria addendum | 162 | Yes |
| `.projex/2604151200-desktop-app-workflow-m41-log.md` | Execution log | 41 | Yes (workflow artifact) |

### Files Modified
| File | Changes | Lines Affected | In Plan? |
|------|---------|----------------|----------|
| `SKILL.md` | Dispatch row 6 + 2 reference bullets | 4 lines (+4, -2) | Yes |
| `evals/evals.json` | Eval ids 18, 19 | +29 lines | Yes |
| `.projex/2604151200-desktop-app-workflow-m41-plan.md` | Status: Ready → In Progress → Complete | 2 lines | Yes (workflow) |

### Files Deleted
None.

### Planned But Not Changed
None — all planned files were changed.

---

## Success Criteria Verification

| Criterion | Method | Result | Evidence |
|-----------|--------|--------|----------|
| `workflows/desktop-app.md` exists with correct template | `grep "^## " workflows/desktop-app.md` | PASS | Identify / Evidence Part A / Evidence Part B / Subject Rubric / Subject Verdict Notes |
| `references/criteria/desktop-app.md` exists with desktop-app scoring | File read; section scan | PASS | 7 sections: channel trust, signing, installer risk, sandbox, auto-update, telemetry, tiers |
| `SKILL.md` dispatch row 6 routes to `desktop-app.md` | `grep desktop-app SKILL.md` | PASS | Row 6 → `workflows/desktop-app.md` (Live — Phase 4 M4.1) |
| `SKILL.md` Reference Files includes workflow + addendum | `grep desktop-app SKILL.md` | PASS | 2 bullets present |
| `evals/evals.json` gains 2 Type 6 cases | JSON parse + id check | PASS | ids 18 (APPROVED), 19 (REJECTED); total 20 |
| No regressions in eval ids 0–17 | Diff shows only appended entries | PASS | ids 0–17 unchanged |
| Homebrew boundary clarified | Workflow Identify table | PASS | `brew install --cask` listed as desktop-app channel |

**Overall:** 7/7 criteria passed.

---

## Deviations from Plan

None. All 4 steps executed as specified. Content matches plan code blocks. No scope creep.

---

## Issues Encountered

None. Clean execution across all 4 steps.

---

## Key Insights

### Lessons Learned

1. **Cross-platform scope increases addendum complexity**
   - Context: Desktop apps span 3 OS families with distinct signing, installer, and distribution models
   - Insight: The universal-concept-first organization (signing, channel trust, sandboxing) with platform-specific tables worked well — avoided the explosion of platform-first sections
   - Application: Apply same pattern to cli-binary (M4.2), which also spans platforms

2. **Code signing as primary trust axis**
   - Context: Unlike browser extensions (permissions) and IDE plugins (capabilities), desktop apps have no permission gate
   - Insight: Code signing serves as the de facto trust gate — unsigned desktop apps are categorically high-risk. This is the single strongest differentiator from other subject types
   - Application: M4.2 (cli-binary) will share this emphasis on signing + provenance

### Pattern Discoveries

1. **Phase 4 workflow shape stabilizes**
   - The Phase 3 template (Identify / Evidence Part A / Evidence Part B / Subject Rubric / Subject Verdict Notes) carries directly to Phase 4. No structural innovations needed — the variation is all in the domain-specific content (channels, signing standards, installer types).

---

## Recommendations

### Immediate Follow-ups
- [ ] Update navigation file with M4.1 completion status
- [ ] Proceed to M4.2 (`workflows/cli-binary.md`) — shares Homebrew boundary clarification from M4.1

### Future Considerations
- Programmatic code signing verification (Authenticode/codesign/GPG) could be a Phase 6 script addition
- The Homebrew `--cask` vs formulae boundary should be documented in the taxonomy def's open questions as resolved

---

## Related Projex Updates

| Document | Update Needed |
|----------|---------------|
| `2604070218-install-auditor-subject-typed-redesign-nav.md` | M4.1 checkbox, Current Position, Active Work, Priorities → M4.2 |
| `2604151200-desktop-app-workflow-m41-plan.md` | Moved to closed/, status Complete |

---

## Appendix

### Execution Commits
```
f957bc5 projex: desktop-app-workflow-m41 step 1 - create references/criteria/desktop-app.md
cb04a17 projex: desktop-app-workflow-m41 step 2 - create workflows/desktop-app.md
e0bf7ce projex: desktop-app-workflow-m41 step 3 - wire SKILL.md dispatch row 6 and reference files
af578dd projex: desktop-app-workflow-m41 step 4 - add Type 6 evals 18 and 19
845a15c projex: desktop-app-workflow-m41 - Phase 4 M4.1 complete, Phase 4 started
2f9948d projex: desktop-app-workflow-m41 - merge Phase 4 M4.1
```
