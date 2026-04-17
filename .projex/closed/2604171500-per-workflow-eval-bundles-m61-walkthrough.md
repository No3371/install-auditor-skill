# Walkthrough: Per-Workflow Eval Bundles (M6.1)

> **Execution Date:** 2026-04-17
> **Completed By:** Claude (orchestrate-projex)
> **Source Plan:** 2604171500-per-workflow-eval-bundles-m61-plan.md
> **Duration:** ~10 min
> **Result:** Success

---

## Summary

Added 10 new eval cases (ids 26-35) to `evals/evals.json`, bringing total to 36 and giving every workflow file ≥3 cases (positive, negative, edge). All success criteria passed. No deviations from plan.

---

## Objectives Completion

| Objective | Status | Notes |
|-----------|--------|-------|
| Every workflow has ≥3 eval cases | Complete | All 10 workflows now at ≥3 |
| Pos/neg/edge coverage per workflow | Complete | container-image gained positive; 7 workflows gained edge; generic gained all 3 |
| Valid JSON, existing evals unchanged | Complete | Parsed clean; ids 0-25 untouched |
| Total count = 36 | Complete | Confirmed via node parse |

---

## Execution Detail

### Step 1: Add Edge-Case Evals for 7 Workflows (ids 26-32)

**Planned:** Append 7 edge-case evals — one per workflow missing an edge case, plus one container-image positive.

**Actual:** Appended ids 26-32 exactly as specced: container-image Tier 1 APPROVED (redis), ci-action CONDITIONAL (docker/build-push-action packages:write), ide-plugin CONDITIONAL (GitLens/GitKraken account), desktop-app CONDITIONAL (OBS dual-distribution), cli-binary CONDITIONAL (terraform shared-drive provenance), agent-extension CONDITIONAL (Brave Search MCP API key), remote-integration CONDITIONAL (Zapier org-wide GitHub read).

**Deviation:** None.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `evals/evals.json` | Modified | Yes | Appended ids 26-32 (7 entries) |

**Verification:** JSON parsed cleanly; ids 0-32 sequential, unique.

**Issues:** None.

---

### Step 2: Add Generic Fallback Evals (ids 33-35)

**Planned:** Append 3 generic.md fallback evals — positive (ambiguous-safe), negative (ambiguous-risky), edge (ambiguous-unclear).

**Actual:** Appended ids 33-35 exactly as specced: id 33 (internal web portal mistaken for installable — APPROVED/CONDITIONAL, only trust boundary is cert acceptance), id 34 (PowerShell iex + shortened-URL one-liner — REJECTED, remote code execution), id 35 (monorepo with Dockerfile+npm+vsix — ambiguous, requires clarification).

**Deviation:** None.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `evals/evals.json` | Modified | Yes | Appended ids 33-35 (3 entries) |

**Verification:** JSON parsed cleanly; ids 0-35 sequential, unique; generic prompts contain no strong single-workflow routing signals.

**Issues:** None.

---

## Complete Change Log

> **Derived from:** `git diff --stat master..projex/2604171500-per-workflow-eval-bundles-m61`

### Files Modified
| File | Changes | Lines Affected | In Plan? |
|------|---------|----------------|----------|
| `evals/evals.json` | Appended 10 eval objects | +134 lines | Yes |

### Files Created
| File | Purpose | Lines | In Plan? |
|------|---------|-------|----------|
| `.projex/2604171500-per-workflow-eval-bundles-m61-log.md` | Execution log | 37 | Yes (by execute-projex workflow) |

---

## Success Criteria Verification

| Criterion | Method | Result | Evidence |
|-----------|--------|--------|----------|
| Every workflow has ≥3 evals | Count by workflow | Pass | All 10 workflows: registry-package(9), browser-extension(3), container-image(3), ci-action(3), ide-plugin(3), desktop-app(3), cli-binary(3), agent-extension(3), remote-integration(3), generic(3) |
| Pos/neg/edge per workflow | Inspect expected_output + assertions | Pass | Each workflow set spans Tier 1 APPROVED, Tier 3 REJECTED, and CONDITIONAL/ambiguous |
| Valid JSON | `node -e "JSON.parse(...)"` | Pass | Parsed cleanly post-step 1 and post-step 2 |
| Existing evals unchanged | IDs 0-25 inspected | Pass | Sequential, untouched |
| Total = 36 | Array length | Pass | 36 confirmed |

**Overall: 5/5 criteria passed.**

---

## Key Insights

### Lessons Learned

1. **Generic prompts require deliberate signal-scrubbing** — Prompts for ids 33-35 needed explicit removal of `npm install`, `docker pull`, etc. to avoid high-confidence routing. Worth adding a checklist item to future eval plans: "confirm no strong-signal keywords in low-confidence prompts."

### Technical Insights

- The 7 edge-case evals all land as CONDITIONAL rather than the existing binary APPROVED/REJECTED — this is the underexercised tier in the current eval suite.
- Generic.md now has baseline coverage for its three key failure modes: non-traditional "installs", obfuscated execution one-liners, and multi-subject-type ambiguity.

---

## Recommendations

### Immediate Follow-ups
- [ ] M6.2 — Hybrid-subject eval cases (innermost trust boundary: npm-distributed CLI, container-wrapped npm app, VS Code extension wrapping a binary)

### Future Considerations
- Eval runner tooling remains absent — manual JSON validation + dry-run is the only harness. Phase 6 gap, tracked in nav.

---

## Related Projex Updates

| Document | Update |
|----------|--------|
| `2604171500-per-workflow-eval-bundles-m61-plan.md` | Status → Complete; walkthrough linked |
| `2604070218-install-auditor-subject-typed-redesign-nav.md` | M6.1 ✓; revision log entry added |
