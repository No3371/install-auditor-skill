# Walkthrough: IDE Plugin Workflow — M3.4

> **Execution Date:** 2026-04-15
> **Completed By:** Claude (Opus 4.6) — orchestrated; Claude (Sonnet 4.6) — executed
> **Source Plan:** [2604150312-ide-plugin-workflow-m34-plan.md](2604150312-ide-plugin-workflow-m34-plan.md)
> **Duration:** Single session (~12 min)
> **Result:** Success

---

## Summary

Created the Type 3 ide-plugin audit pipeline: criteria addendum (126 lines), workflow file (358 lines), dispatcher wiring, and two eval cases. All 6 success criteria passed. No deviations from plan. Verification caveat same as M3.3: no runnable local eval harness, so regression checking used JSON validation + id preservation.

---

## Objectives Completion

| Objective | Status | Notes |
|-----------|--------|-------|
| Create `references/criteria/ide-plugin.md` | Complete | 126 lines; marketplace trust, capability risk, bundled-binary patterns, tier thresholds |
| Create `workflows/ide-plugin.md` | Complete | 358 lines; all 4 required sections present |
| Route Type 3 through `SKILL.md` | Complete | Row 3 → `workflows/ide-plugin.md`; 2 reference-file bullets added |
| Add Type 3 eval coverage | Complete | ids 16 and 17 added |
| Preserve prior eval coverage | Complete | ids 0–15 unchanged; `evals/evals.json` parses cleanly |

---

## Execution Detail

### Step 1: Create `references/criteria/ide-plugin.md`

**Planned:** Type 3 criteria addendum covering marketplace trust signals, capability risk classification, bundled-binary risk, tier thresholds.

**Actual:** Created the addendum. 6-marketplace trust table (VS Code, Open VSX, JetBrains, Sublime, Neovim, Sideloaded) with scoring impacts. VS Code `contributes`/activation event risk table. JetBrains extension point risk table. Sublime/Neovim notes. Bundled-binary/download-at-runtime 5-pattern table. Tier thresholds calibrated to install-count scale (500K+ = Tier 1, 10K–500K = Tier 2, <10K or sideloaded = Tier 3).

**Deviation:** None.

**Files Changed:**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `references/criteria/ide-plugin.md` | Created | Yes | 126 lines |

**Verification:** Reviewed sections — all 4 required areas present and internally consistent.

---

### Step 2: Create `workflows/ide-plugin.md`

**Planned:** Type 3 workflow using Identify / Evidence / Subject Rubric / Subject Verdict Notes template, VS Code Marketplace-first.

**Actual:** Created the workflow. Identify section: marketplace identity table, metadata extraction checklist, required context (6 items). Evidence Part A: tier triage linked to addendum criteria. Evidence Part B: 8 core research questions, marketplace/capability/binary/incident research guides, audit coverage tracking table (10 checks × 3 tiers). Subject Rubric: 6 ide-plugin-specialized sections (4.1 Provenance — impersonation check + cross-marketplace consistency; 4.2 Maintenance — install trend, review sentiment; 4.3 Security — marketplace removal history, supply-chain incidents; 4.4 Permissions — capability scope, activation breadth, binary execution, network/filesystem/terminal access; 4.5 Reliability — editor compatibility, auto-update risk; 4.6 Alternatives). Subject Verdict Notes: REJECTED/CONDITIONAL/APPROVED triggers.

**Deviation:** None.

**Files Changed:**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `workflows/ide-plugin.md` | Created | Yes | 358 lines |

**Verification:** `grep "^## " workflows/ide-plugin.md` confirmed 5 top-level sections (Identify, Evidence A, Evidence B, Subject Rubric, Subject Verdict Notes). File references `references/criteria/ide-plugin.md` and returns to `SKILL.md` Step N.

---

### Step 3: Update `SKILL.md`

**Planned:** Route Type 3 to new workflow; add 2 reference-file bullets.

**Actual:** Applied 3 edits: dispatch table row 3 changed from `workflows/generic.md` (Fallback) to `workflows/ide-plugin.md` (Live — Phase 3 M3.4); inserted workflow bullet after ci-action workflow bullet; inserted addendum bullet after ci-action addendum bullet.

**Deviation:** None.

**Files Changed:**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `SKILL.md` | Modified | Yes | Row 3 route changed; 2 reference-file bullets added |

**Verification:** `grep -n "ide-plugin" SKILL.md` matched row 3 route (line 64) and both reference-file bullets (lines 216, 222).

---

### Step 4: Update `evals/evals.json`

**Planned:** Add one positive (Prettier, APPROVED) and one negative (sideloaded VSIX, REJECTED) Type 3 case.

**Actual:** Added id 16 (Prettier VS Code extension — verified publisher, high installs, proportional capabilities → Tier 1 → APPROVED) and id 17 (sideloaded `super-intellisense-pro.vsix` shared via Slack — no marketplace, unknown publisher → Tier 3 → REJECTED). Both use `contains_concept` and `exact_match` assertion types.

**Deviation:** None.

**Files Changed:**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `evals/evals.json` | Modified | Yes | +29 lines; ids 16 and 17 added; ids 0–15 unchanged |

**Verification:** JSON validation passed (node.js). 18 total evals. Ids 0–15 preserved.

---

## Complete Change Log

> **Derived from:** `git diff --stat master..HEAD`
> 6 files changed, 569 insertions(+), 2 deletions(-)

### Files Created
| File | Purpose | Lines | In Plan? |
|------|---------|-------|----------|
| `references/criteria/ide-plugin.md` | Type 3 scoring addendum | 126 | Yes |
| `workflows/ide-plugin.md` | Type 3 subject-specific workflow | 358 | Yes |
| `.projex/2604150312-ide-plugin-workflow-m34-log.md` | Execution log | 53 | Yes (structural) |

### Files Modified
| File | Changes | Lines Affected | In Plan? |
|------|---------|----------------|----------|
| `SKILL.md` | Row 3 route updated; 2 Type 3 reference-file bullets added | 4 lines | Yes |
| `evals/evals.json` | ids 16 and 17 appended | +29/-0 | Yes |
| `.projex/2604150312-ide-plugin-workflow-m34-plan.md` | Status → Complete | 1 line | Yes (structural) |

### Planned But Not Changed

None — all planned targets changed.

---

## Success Criteria Verification

### Acceptance Criteria Summary

| Criterion | Method | Result | Evidence |
|-----------|--------|--------|----------|
| `workflows/ide-plugin.md` exists with 4 template sections | Read file; grep headings | **PASS** | Identify / Evidence A / Evidence B / Subject Rubric / Subject Verdict Notes present |
| `references/criteria/ide-plugin.md` exists with IDE scoring | Read file | **PASS** | Marketplace trust, capability risk, bundled-binary, tier sections present |
| `SKILL.md` routes Type 3 correctly | Grep `SKILL.md` | **PASS** | Row 3 → `workflows/ide-plugin.md`; reference-file bullets added |
| Positive Type 3 eval exists | Read `evals/evals.json` | **PASS** | id 16 present; APPROVED path |
| Negative Type 3 eval exists | Read `evals/evals.json` | **PASS** | id 17 present; REJECTED path |
| No regressions in ids 0–15 | JSON validation + diff | **PASS** | ids 0–15 preserved; no local eval harness |

**Overall: 6/6 criteria passed.**

---

## Deviations from Plan

None. All 4 steps executed as specified.

---

## Issues Encountered

None.

---

## Key Insights

### Pattern Discoveries

1. **IDE plugin risk is capability-scope-first, not permission-first**
   - Observed in: `workflows/ide-plugin.md` §4.4 and `references/criteria/ide-plugin.md`
   - Description: Unlike browser extensions (manifest permissions) or CI actions (trigger/secret context), IDE plugins have no granular permission model. Risk is measured by what capabilities the plugin *declares* (debuggers, tasks, terminals), what binaries it *downloads*, and how broadly it *activates*.
   - Reuse potential: Future Type 8 (agent-extension) workflows face a similar no-permission-gate problem — capability scope + execution behavior will likely be the dominant axes there too.

2. **Bundled-binary provenance is the dominant attack surface**
   - Observed in: `references/criteria/ide-plugin.md` § Bundled Binary
   - Description: Many popular IDE plugins (language servers, formatters, linters) bundle or download-at-runtime compiled binaries. This is the primary vector for supply-chain compromise in the IDE plugin ecosystem — more so than malicious code in the plugin's JS/TS itself.
   - Reuse potential: Type 6 (desktop-app) and Type 7 (cli-binary) will share this concern; the binary-provenance rubric pattern can be lifted.

### Technical Insights

- M3.4 follows the same 4-step pattern as M3.1–M3.3 cleanly. The Phase 3 workflow template is now proven across 4 executions.
- Tier thresholds needed marketplace-specific calibration (install count vs. npm downloads) — this confirms the framing eval's observation (§5.1) that shared thresholds don't work across subject types.
- Five live subject-specific workflows now exist (registry-package + browser-extension + container-image + ci-action + ide-plugin). Only `generic.md` fallback remains for Types 6–9.

---

## Recommendations

### Immediate Follow-ups
- [ ] Update nav doc `2604070218-install-auditor-subject-typed-redesign-nav.md` — mark M3.4 complete, update Current Position, advance focus to M3.5
- [ ] M3.5 eval gate: ide-plugin eval coverage (ids 16–17) now satisfies the Type 3 portion; verify all 4 Phase 3 types have ≥1 positive + ≥1 negative case

### Future Considerations
- Eval runner remains undocumented — same caveat as M3.3
- Type 8 (agent-extension) will likely reuse ide-plugin's capability-scope framing — consider cross-referencing when M4.3 planning begins
