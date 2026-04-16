# M4.3 Walkthrough — `workflows/agent-extension.md`

> **Date:** 2026-04-16
> **Milestone:** Phase 4 M4.3
> **Plan:** [2604160900-agent-extension-workflow-m43-plan.md](../2604160900-agent-extension-workflow-m43-plan.md)
> **Parent Nav:** [2604070218-install-auditor-subject-typed-redesign-nav.md](../2604070218-install-auditor-subject-typed-redesign-nav.md)
> **Orchestration:** Opus subagent planned, Sonnet subagent executed, orchestrator (Opus) closed.

---

## Summary

Created Type 8 agent-extension workflow (`workflows/agent-extension.md`, 230 lines) and criteria addendum (`references/criteria/agent-extension.md`, 125 lines). Wired `SKILL.md` dispatch table row 8 and added 2 eval cases (ids 22, 23). All success criteria passed. Third Phase 4 deliverable — agent extensions (MCP servers, Claude Code plugins, Claude Code skills) no longer fall through to `workflows/generic.md`. One workflow file with three labeled sub-rubrics (8a/8b/8c) per M0.1 lock-in; 31 sub-rubric label occurrences across the workflow.

---

## Execution Detail

### Step 1: Create `references/criteria/agent-extension.md`

**Planned:** New addendum with 5 sections covering distribution/discovery channel trust, capability scope classification, transport & isolation assessment, prompt/behavioral risk, and tier thresholds.

**Actual:** Created as planned. 125 lines. 5 sections present: Distribution / Discovery Channel Trust Signals (table covering MCP registries, GitHub repos, npm, Claude Code marketplace, community shared, unknown), Capability Scope Classification (tool types × risk levels — shell execution, file system, network, data read, prompt injection), Transport & Isolation Assessment (stdio local vs HTTP remote vs SSE, sandboxing, process isolation), Prompt / Behavioral Risk (8b and 8c primarily — behavioral shaping, prompt injection surface, settings override), Tier Thresholds (Tier 1/2/3 with trigger conditions).

**Deviation:** None.

**Files Changed:**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `references/criteria/agent-extension.md` | Created | Yes | 125 lines, complete addendum |

**Verification:** File exists; all 5 sections present with scoring impact subsections.

### Step 2: Create `workflows/agent-extension.md`

**Planned:** Type 8 workflow following Identify / Evidence Part A / Evidence Part B / Subject Rubric / Subject Verdict Notes template with three labeled sub-rubrics 8a/8b/8c throughout.

**Actual:** Created as planned. 230 lines. Structure: HTML comment header → intro → Identify (3 sub-sections: sub-type classification table for 8a MCP / 8b CC plugin / 8c CC skill, metadata extraction, required context checklist) → Evidence Part A (tier triage with capability-scope-first criteria) → Evidence Part B (core research questions, capability audit, transport audit, prompt/behavioral audit, audit coverage tracking table) → Subject Rubric (§4.1–4.6 agent-extension-specialized with labeled 8a/8b/8c divergence points across all rubric axes; capability scope as primary §4.4 axis) → Subject Verdict Notes (toward REJECTED/CONDITIONAL/APPROVED with concrete triggers per sub-type).

**Deviation:** None.

**Files Changed:**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `workflows/agent-extension.md` | Created | Yes | 230 lines, all 5 template sections, 31 sub-rubric labels |

**Verification:** `grep "^## " workflows/agent-extension.md` confirms all required sections (Identify, Evidence — Part A, Evidence — Part B, Subject Rubric, Subject Verdict Notes). Sub-rubric count: 31 occurrences of 8a/8b/8c labels.

### Step 3: Update `SKILL.md`

**Planned:** Dispatch table row 8 → `agent-extension.md`; add 2 Reference Files bullets in type-number order.

**Actual:** Executed as planned. Row 8 changed from `generic.md (Fallback)` to `agent-extension.md (Live — Phase 4 M4.3)`. Two Reference Files bullets inserted after the cli-binary entries.

**Deviation:** None.

**Files Changed:**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `SKILL.md` | Modified | Yes | Line 41: signal row 8; Line 69: dispatch row 8; Line 219: workflow bullet; Line 228: addendum bullet |

**Verification:** `grep agent-extension SKILL.md` returns 4 hits (signal row, dispatch row, workflow ref, addendum ref).

### Step 4: Update `evals/evals.json`

**Planned:** Append ids 22 (Tier 1 positive) and 23 (Tier 3 negative).

**Actual:** Appended id 22 (Anthropic MCP filesystem server, Tier 1 APPROVED, assertions include agent-extension type + established/official + APPROVED verdict) and id 23 (Discord-shared unknown MCP server with credential/API key access, Tier 3 REJECTED, assertions include agent-extension type + capability risk + unknown source + REJECTED verdict). JSON valid. Ids 0–21 unchanged.

**Deviation:** None.

**Files Changed:**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `evals/evals.json` | Modified | Yes | +2 entries appended; total 24 evals |

**Verification:** JSON valid. 24 total evals. ids 22, 23 confirmed present with correct assertions.

---

## Verification Summary

| Criterion | Result |
|-----------|--------|
| Workflow exists with template sections | PASS — 5 sections (Identify, Evidence A, Evidence B, Subject Rubric, Subject Verdict Notes) |
| Sub-rubrics 8a/8b/8c labeled throughout | PASS — 31 occurrences |
| Criteria addendum exists with 5 sections | PASS — 125 lines, all sections present |
| Dispatch row 8 routes to agent-extension.md | PASS — "Live — Phase 4 (M4.3)" |
| Reference Files bullets present | PASS — 4 total `agent-extension` hits in SKILL.md |
| Eval coverage (ids 22, 23) | PASS — positive (Tier 1 APPROVED) + negative (Tier 3 REJECTED) |
| No regressions (ids 0–21) | PASS — unchanged |
| Total eval count | PASS — 24 |

---

## Recommendations

### Immediate Follow-ups
- [ ] M4.4 — `workflows/remote-integration.md` (OAuth scopes, data residency, ToS, breach history)
- [ ] M4.5 — Phase 4 eval gate (≥1 case per long-tail workflow; M4.1–M4.3 each have 2)

### Future Considerations
- Eval harness gap persists (Phase 6 cross-phase concern). Regression verification remains manual/JSON-only until a runner lands.
- Phase 5 (default-off generic) gets closer with each long-tail workflow — only Type 9 (remote-integration) still falls back.
- Both eval cases target 8a (MCP servers) as the most common sub-type; 8b/8c eval cases could be added in M4.5 or Phase 6.
- Future split triggers (≥30% sub-rubric-specific content, distinct classifier signal, read-cost budget) should be monitored as MCP ecosystem matures.

### Plan Improvements
- Plan was well-scoped. No changes needed for M4.4 to reuse the same shape.
