# Tighten the Classifier (M5.1)

> **Status:** Complete
> **Created:** 2026-04-16
> **Completed:** 2026-04-16
> **Author:** projex-agent
> **Source:** Nav M5.1 — Phase 5 "Default-Off Generic"
> **Nav:** 2604070218-install-auditor-subject-typed-redesign-nav.md
> **Related Projex:** 2604070300-install-auditor-subject-type-taxonomy-def.md
> **Walkthrough:** 2604160430-tighten-classifier-m51-walkthrough.md
> **Worktree:** No

---

## Summary

Rewire the Step 0 classifier procedure so that `medium` confidence routes to a specific workflow (not generic), and only `low` confidence falls back to `generic.md`. All 9 specific workflows are live; the current procedure only distinguishes high vs low, meaning any ambiguity drops to generic even when a reasonable match exists. After this change, `generic.md` triggers only for truly unclassifiable subjects.

**Scope:** `SKILL.md` Step 0 — Procedure paragraph, dispatch table metadata, stale Phase 2 note.
**Estimated Changes:** 1 file, 3 regions.

---

## Objective

### Problem / Gap / Need

The Step 0 Procedure (line 28) defines a binary confidence model: one strong signal match = `high`, anything else = `low` (→ generic). The output shape includes `medium` but the procedure never produces it. With all 9 workflows live, subjects with partial or multiple weak signals should route to their best-match specific workflow at `medium` confidence instead of falling back to the generic monolith.

Additionally:
- The Phase 2 note (line 73) is stale — all workflows are live, not just registry-package.
- The dispatch table "Phase 1 Status" column header is a vestige; all rows are now "Live".

### Success Criteria

- [x] Procedure defines three confidence tiers: `high` (strong match), `medium` (partial/weak match, single best candidate), `low` (no match or unresolved conflict)
- [x] Only `low` confidence routes to `generic.md`; `medium` routes to the best-match specific workflow
- [x] Phase 2 note removed
- [x] Dispatch table column updated from "Phase 1 Status" to "Status"; all rows show "Live" (drop milestone references)
- [x] Generic row description updated: "Low-confidence fallback only"
- [x] Existing 26 eval cases still classify correctly (no regressions — all named-type evals had high confidence, so the new medium tier doesn't affect them)

### Out of Scope

- Trimming `generic.md` content (that's M5.2)
- Read-cost measurement (that's M5.3)
- Adding new eval cases for medium-confidence scenarios (future work)
- Changing the signal table entries
- Changing the innermost-trust-boundary rule

---

## Context

### Current State

`SKILL.md` Step 0 Procedure (line 28):
```
(1) read URL + install command + manifest + user intent (read-only);
(2) match against the signal table below;
(3) one strong match → high confidence;
(4) multiple matches → apply the innermost-boundary rule to pick the last gate the user personally crosses;
(5) no strong match OR conflict unresolved after the rule → generic (type 0) at low confidence, naming the conflict;
(6) emit the structured output and route.
Low confidence routes to generic, never to a best-guess specific type.
```

Problems:
- Step (3) only yields `high`. Step (5) only yields `low`. No `medium` path.
- Step (4) resolves multi-match via the boundary rule but doesn't state the resulting confidence — implicitly `high` if it resolves, `low` if not.
- The final sentence "Low confidence routes to generic, never to a best-guess specific type" is the Phase 1 safety net. With all workflows live, `medium` should route to a specific workflow.

### Key Files

| File | Role | Change Summary |
|------|------|----------------|
| `SKILL.md` | Dispatcher — Step 0 classifier + dispatch table | Rewrite Procedure paragraph; update dispatch table; remove Phase 2 note |

### Dependencies

- **Requires:** All 9 specific workflows live (confirmed Phase 4 complete)
- **Blocks:** M5.2 (trim generic.md — depends on generic being rare first)

### Constraints

- Must not change signal table content (signals are locked per taxonomy def)
- Must not change the innermost-trust-boundary rule itself
- Output shape stays identical (already includes `medium`)

### Assumptions

- All 26 existing eval cases classify at `high` confidence — the new `medium` tier won't affect their routing
- The taxonomy def's "Classifier Rule" section doesn't contradict the addition of a medium tier (it already mentions confidence levels plural)

### Impact Analysis

- **Direct:** `SKILL.md` Step 0 — procedure text, dispatch table, Phase 2 note
- **Adjacent:** `generic.md` usage frequency drops (by design)
- **Downstream:** Future evals should include medium-confidence test cases (out of scope for this plan)

---

## Implementation

### Overview

Single-file edit to `SKILL.md` with three targeted changes: (1) rewrite the Procedure paragraph to define three confidence tiers, (2) update the dispatch table metadata, (3) remove the stale Phase 2 note.

### Step 1: Rewrite the Procedure Paragraph

**Objective:** Replace the binary high/low confidence model with a three-tier model where `medium` routes to specific workflows.
**Confidence:** High
**Depends on:** None

**Files:**
- `SKILL.md` (line 28)

**Changes:**

```markdown
// Before (line 28):
**Procedure:** (1) read URL + install command + manifest + user intent (read-only); (2) match against the signal table below; (3) one strong match → **high** confidence; (4) multiple matches → apply the innermost-boundary rule to pick the last gate the user personally crosses; (5) no strong match OR conflict unresolved after the rule → **`generic` (type 0) at low confidence**, naming the conflict; (6) emit the structured output and route. **Low confidence routes to `generic`, never to a best-guess specific type.**

// After:
**Procedure:** (1) read URL + install command + manifest + user intent (read-only); (2) match against the signal table below; (3) apply confidence:

| Condition | Confidence | Routes to |
|-----------|------------|-----------|
| One strong signal match | **high** | `workflows/<matched-type>.md` |
| Multiple strong matches → innermost-boundary rule resolves to one type | **high** | `workflows/<resolved-type>.md` |
| Weak/partial signals point to a single best-candidate type | **medium** | `workflows/<best-candidate>.md` — note the uncertainty in Rationale |
| Multiple weak matches, no single best candidate after the boundary rule | **low** | `workflows/generic.md` — name the conflict in Rationale |
| No signals fire at all | **low** | `workflows/generic.md` |

(4) emit the structured output and route. **Only `low` confidence routes to `generic.md`. Medium-confidence subjects route to their best-match specific workflow — the workflow itself handles residual uncertainty via its tier system.**
```

**Rationale:** The three-tier model keeps the safety net (low → generic) while unlocking specific workflows for partial matches. The boundary rule is unchanged — it still resolves multi-match conflicts. The new medium tier covers the gap between "perfect signal" and "no signal at all." Workflows already have tier systems (Tier 1/2/3) that handle uncertainty within their domain, so medium-confidence routing to a specific workflow is safe.

**Verification:** Re-read the procedure and confirm: (a) high → specific, (b) medium → specific with rationale note, (c) low → generic. Check that the output shape still works (it already includes medium).

**If this fails:** Revert `SKILL.md` line 28 to the original single-paragraph procedure.

---

### Step 2: Update Dispatch Table Metadata

**Objective:** Remove Phase 1 vestiges from the dispatch table — rename column, simplify status values.
**Confidence:** High
**Depends on:** None (independent of Step 1)

**Files:**
- `SKILL.md` (lines 60–73)

**Changes:**

```markdown
// Before (lines 60–73):
| # | Type | Workflow | Phase 1 Status |
|---|---|---|---|
| 1 | registry-package | `workflows/registry-package.md` | Live — Phase 2 (M2.1) |
| 2 | browser-extension | `workflows/browser-extension.md` | Live — Phase 3 (M3.1) |
| 3 | ide-plugin | `workflows/ide-plugin.md` | Live — Phase 3 (M3.4) |
| 4 | container-image | `workflows/container-image.md` | Live — Phase 3 (M3.2) |
| 5 | ci-action | `workflows/ci-action.md` | Live — Phase 3 (M3.3) |
| 6 | desktop-app | `workflows/desktop-app.md` | Live — Phase 4 (M4.1) |
| 7 | cli-binary | `workflows/cli-binary.md` | Live — Phase 4 (M4.2) |
| 8 | agent-extension | `workflows/agent-extension.md` | Live — Phase 4 (M4.3); 8a/8b/8c resolved at classification |
| 9 | remote-integration | `workflows/remote-integration.md` | Live — Phase 4 (M4.4) |
| 0 | generic | `workflows/generic.md` | Universal fallback; also the home for truly unclassifiable subjects |

> **Phase 2 note:** `workflows/registry-package.md` is live (M2.1). Remaining 9 types still route to `workflows/generic.md`; specific workflows land in Phases 2--4 and this table updates per milestone. Do **not** create a workflow file before its owning phase.

// After:
| # | Type | Workflow | Status |
|---|---|---|---|
| 1 | registry-package | `workflows/registry-package.md` | Live |
| 2 | browser-extension | `workflows/browser-extension.md` | Live |
| 3 | ide-plugin | `workflows/ide-plugin.md` | Live |
| 4 | container-image | `workflows/container-image.md` | Live |
| 5 | ci-action | `workflows/ci-action.md` | Live |
| 6 | desktop-app | `workflows/desktop-app.md` | Live |
| 7 | cli-binary | `workflows/cli-binary.md` | Live |
| 8 | agent-extension | `workflows/agent-extension.md` | Live; 8a/8b/8c resolved at classification |
| 9 | remote-integration | `workflows/remote-integration.md` | Live |
| 0 | generic | `workflows/generic.md` | Low-confidence fallback only |
```

**Rationale:** Phase references are historical — every workflow is live. The Phase 2 note is factually wrong (says remaining types route to generic, but they don't). Cleaning this removes confusion for the LLM reading the dispatcher at audit time.

**Verification:** Confirm table has 10 rows, all specific types say "Live", generic says "Low-confidence fallback only", Phase 2 note is gone.

**If this fails:** Restore original table and note from git.

---

## Verification Plan

### Automated Checks

- [ ] `SKILL.md` parses as valid markdown (no broken tables)
- [ ] All 10 workflow files still referenced in dispatch table

### Manual Verification

- [ ] Re-read Step 0 top-to-bottom: procedure → signal table → output shape → dispatch table flow is coherent
- [ ] Dry-run eval case 0 (express): strong npm signals → high confidence → registry-package.md (unchanged)
- [ ] Dry-run eval case 1 (Wappalyzer): strong browser-extension signals → high confidence → browser-extension.md (unchanged)
- [ ] Thought-experiment: a subject with weak Docker signals but no Dockerfile → medium confidence → container-image.md (new behavior, was generic before)
- [ ] Thought-experiment: a subject with zero install signals → low confidence → generic.md (unchanged)

### Acceptance Criteria Validation

| Criterion | How to Verify | Expected Result |
|-----------|---------------|-----------------|
| Three confidence tiers defined | Read Procedure section | high/medium/low with routing rules |
| Only low → generic | Read Procedure table | medium routes to specific workflow |
| Phase 2 note removed | Search for "Phase 2 note" | Not found |
| Dispatch table column updated | Read table header | "Status" not "Phase 1 Status" |
| Generic row description | Read row 0 | "Low-confidence fallback only" |
| No eval regressions | Dry-run 2-3 named-type evals | Same classification as before |

---

## Rollback Plan

Single-file change — `git checkout HEAD -- SKILL.md` restores the pre-change state.

---

## Notes

### Risks

- **Medium-confidence misrouting:** A subject could be routed to the wrong specific workflow at medium confidence. Mitigated by: (a) the workflow's own tier system catches low-signal subjects and applies appropriate scrutiny, (b) user override remains available, (c) future eval cases can test medium paths.
- **Procedure readability:** The table format is longer than the original paragraph. Trade-off: clarity and precision outweigh brevity here since this is the decision logic that runs every audit.

### Open Questions

None — all resolved during research.
