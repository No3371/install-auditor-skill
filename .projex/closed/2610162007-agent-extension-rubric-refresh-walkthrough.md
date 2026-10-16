# Walkthrough: Agent-Extension Rubric Refresh (8a MCP / 8b Plugin / 8c Skill)

> **Execution Date:** 2026-10-16
> **Completed By:** Claude (executor subagent) | closed by close-projex subagent
> **Source Plan:** 2610162007-agent-extension-rubric-refresh-plan.md
> **Parent:** 2610162007-agent-extension-rubric-refresh-plan.md
> **Duration:** ~16 min (19:30-19:46 per execution log timestamps)
> **Result:** Success

---

## Summary

Type 8 rubric pair rewritten against primary sources as two whole-file replacements, byte-identical to the plan blocks. `references/criteria/agent-extension.md` 6,932 → 15,098 B (channel trust signals, capability scope and shell-surface rating, 8a transport and auth, behavioral and model-context risk, repo-borne surfaces, `## Version & Update Integrity (§4.6)` V1-V5 with the §4.3 own-code line, disjoint tier thresholds). `workflows/agent-extension.md` 12,907 → 16,586 B (sub-type and channel identification, per-sub-type evidence for 8a/8b/8c and repo-borne extensions, 12 canonical coverage rows plus 6 subject rows, rubric renumbered to mirror `references/criteria.md` §4.1-§4.6). Consistency script `OK`; harness unchanged; traces T1-T10 match.

---

## Objectives Completion

| Objective | Status | Notes |
|-----------|--------|-------|
| F4 8a is runtime-enumerated; transport table (Streamable HTTP, legacy SSE flag, loopback bind / `Origin`); remote auth modes; remote 8a with no local code | Complete | Addendum Transport & Auth (8a); workflow Identify note and 8a steps; OAuth grant cites remote-integration §1/§5/§6 |
| F5 behavioral risk for all sub-types | Complete | Tool poisoning, exfil steering, prerequisite lure, config hijack, endpoint redirection, shadowing, persistence, indirect injection, trifecta |
| F1 8b is a container | Complete | Component inventory, hook handler types, shell-surface rating, nested 8a/8c sub-audits, `dependencies` |
| F2 marketplace model | Complete | Owner and reserved names; source types and pin strength; `command` source; auto-update defaults |
| F3 8c frontmatter and shell injection | Complete | `allowed-tools` not trust-gated, `hooks`, `context: fork`, `!` shell injection, prerequisite lures, shadowing |
| F6 channel table | Complete | Anthropic-operated marketplace, vendor first-party, MCP reference server ("not production-ready"), official MCP Registry (identity only), aggregators, third-party hosts, skill hubs, MCPB |
| F7 repo-borne surfaces | Complete | Addendum Repo-Borne Surfaces and workflow sub-section |
| F11 disjoint tiers | Complete | Tier 1 ALL / Tier 3 ANY / Tier 2 = rest; directory-scoped fs write = Tier 2 |
| F12 canonical coverage rows | Complete | 12/12 canonical rows (exact labels) + 6 subject rows |
| F14 stale doc references removed | Complete | `docs.anthropic.com`, `claude-code/plugins` gone from both files |
| Floor plug-in and heading collision | Complete | V1-V5 + own-code line; no `### §4.` headings remain in the workflow |

---

## Execution Detail

> Derived from `git log`/`git diff` of `1c498a7..projex/2610162007-agent-extension-rubric-refresh` (start commit) and the execution log.

### Preflight

**Planned:** floor and dependency checks, baseline.
**Actual:** `20843cc` reachable; `### V[1-5] ` 5; `## 4.6 Version & Update Integrity (shared floor)` 1; `Workflow coverage tables` 1; `Blocking CVE` 1; remote-integration §1/§5/§6 headings 3 (sibling landed `dcb8398`); target files last changed at `5c44b79` (no sibling edits). Baselines 12,907 / 6,932 B; `validate` 41 evals / 248 assertions; unittest evals 12 OK; tests 19 OK (6 skipped).
**Deviation:** None.

### Step 1: Replace `references/criteria/agent-extension.md`

**Planned:** whole-file replacement with plan block 1.
**Actual:** extracted with the plan's own awk; `diff` vs block 1 empty; 15,098 B (cap 15,500); one §4.6 heading; V1-V5 once each. Commit `de9b553`.
**Deviation:** None.

### Step 2: Replace `workflows/agent-extension.md`

**Planned:** whole-file replacement with plan block 2.
**Actual:** extracted with the plan's awk; `diff` empty; 16,586 B (cap 17,000); `^### §4\.` 0; template headings 5. Plan consistency script `OK` (12/12 canonical rows, addendum headings, V1-V5 + own-code line, remote-integration cross-refs, stale strings absent, sizes, no projex references). Commit `c48f92a`; completion commit `5a61152`.
**Deviation:** None.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `references/criteria/agent-extension.md` | Modified | Yes | Whole-file replacement (210 lines; 7 diff hunks vs start commit); 293 lines changed |
| `workflows/agent-extension.md` | Modified | Yes | Whole-file replacement (25 diff hunks vs start commit); 427 lines changed |

---

## Complete Change Log

> **Derived from:** `git diff --stat 1c498a7..projex/2610162007-agent-extension-rubric-refresh`: 4 files changed, 522 insertions(+), 279 deletions(-) (including projex documents).

### Files Created
| File | Purpose | Lines | In Plan? |
|------|---------|-------|----------|
| `.projex/2610162007-agent-extension-rubric-refresh-log.md` | Execution log | 78 | Yes (implicit) |
| `.projex/closed/2610162007-agent-extension-rubric-refresh-walkthrough.md` | This walkthrough | - | Yes (close) |

### Files Modified
| File | Changes | Lines Affected | In Plan? |
|------|---------|----------------|----------|
| `references/criteria/agent-extension.md` | Full replacement | 293 changed; 15,098 B | Yes |
| `workflows/agent-extension.md` | Full replacement | 427 changed; 16,586 B | Yes |
| `.projex/2610162007-agent-extension-rubric-refresh-plan.md` | Status Complete, Completed, Walkthrough link | 3 lines | Yes (close) |

### Files Deleted
None.

### Planned But Not Changed
None. `SKILL.md`, `references/classifier.md`, `references/criteria.md`, `evals/` untouched, as scoped.

---

## Success Criteria Verification

| Criterion | Method | Result | Evidence |
|-----------|--------|--------|----------|
| Both files byte-identical to plan blocks | `diff` against plan blocks | Pass | `same` x2 |
| One §4.6 heading, V1-V5 once each, one `**§4.3 own-code line**` | grep + script | Pass | 1 / 5 / 1 |
| 12/12 canonical coverage rows verbatim | consistency script | Pass | `OK` |
| Cited addendum headings and remote-integration §1/§5/§6 exist | script | Pass | `OK` |
| Stale strings absent | script, case-insensitive | Pass | 0 |
| `§4.6 V<n>` refs V1-V5 only; no `### §4.` headings | script | Pass | `OK` |
| Sizes | `wc -c` | Pass | 15,098 ≤ 15,500; 16,586 ≤ 17,000 |
| `validate` + unittest with Preflight count | harness | Pass | 41 / 248; evals 12 OK; tests 19 OK (6 skipped) |
| Paper traces T1-T10 | manual walk | Pass | all match (execution log "Verification: paper traces") |
| Diff scope: 2 shipped files + projex docs; protected files untouched | `git diff --stat` | Pass | met |

**Overall:** 10/10 criteria passed.

---

## Deviations from Plan

None. Both steps applied as whole-file replacements byte-identical to plan blocks 1 and 2. Process notes (not deviations): no sub-subagents dispatched (do-projex / verify-projex are Encouraged); no task tool available; the log `Worktree Path` is repo-relative per the orchestrator note.

---

## Issues Encountered

### Issue 1: Untracked sibling plan in the main checkout
- **Description:** `.projex/2610162010-registry-package-rubric-refresh-plan.md` (precheck WARN).
- **Severity:** Low
- **Resolution:** not this plan's; left untouched and never staged.

### Close notes
- Nav `2604070218-install-auditor-subject-typed-redesign-nav.md` updated in the close commit, following earlier rubric-refresh closes (plan carries no `Nav:` field). Add/add conflicts with base's concurrent entries resolved by keeping both sides.
- The parent eval `2610161927-agent-extension-stewardship-review-eval.md` is left active: the eval-refresh work (F8-F10) and classifier work (F13) it recommends remain open.
- Calibration choices accepted by the orchestrator: an unpinned `npx -y` launch is HIGH (`unpinned launcher`), so eval 22 becomes CONDITIONAL; that eval change belongs to the later eval-refresh plan.

---

## Key Insights

**Rationale promoted:** none needed. Rationale ships in the addendum and workflow text; no shipped file carries projex references (consistency script check).

### Lessons Learned

1. **Whole-file replacement beats pairwise edits for stale models**
   - Context: the 8a/8b/8c models (static manifest, in-process plugin, behavioral-only skill) were wrong at the structural level.
   - Insight: plan-embedded verbatim blocks, extracted with a script and `diff`-checked, make a rewrite verifiable at near-zero cost.
   - Application: use for any rubric whose model, not just facts, changed.

### Gotchas / Pitfalls

1. **Tier overlap**
   - Trap: localhost HTTP was both Tier 1-allowed and a Tier 2 trigger; fs-write was Tier 3 while eval 22 expected Tier 1.
   - Avoidance: disjoint tiers (Tier 1 ALL / Tier 3 ANY / Tier 2 = rest).

2. **Auto-loading repo config**
   - Trap: headless `claude -p` loads repo `.mcp.json` without asking; auto-approve keys remove the prompt.
   - Avoidance: Repo-Borne Surfaces rows (auto-approve key HIGH; `--strict-mcp-config` / managed lists as controls).

---

## Recommendations

### Immediate Follow-ups
- [ ] Eval refresh plan: eval 22 (premise "MCP reference server (steering group)"; expected Tier 2, CONDITIONAL because the unpinned `npx -y` launch is HIGH; replace exact APPROVED with `[CONDITIONAL]` or pin a version and accept `[APPROVED, CONDITIONAL]`); eval 31 (official `@brave/brave-search-mcp-server`; Tier 2; CONDITIONAL for env-held key); new cases T5-T10 plus a tool-poisoning description case; consider ≥ 1 case per 8a/8b/8c in `validate`.
- [ ] Classifier sibling asks if not covered: `/plugin install <name>@<marketplace>` → 8b whatever the `source` type (keep direct `npm install -g` → registry-package, eval 40); remote MCP by URL → 8a.
- [ ] Keep remote-integration §1/§5/§6 heading names stable (this addendum cites them) or revise this plan if renamed.
- [ ] STEWARDSHIP: agent-extension Last Reviewed 2026-10-16, Next Due 2026-12-15; add event triggers (MCP spec revision; Claude Code plugin/skill/MCP docs changes to component types, source types or trust gating).

### Future Considerations
- Per-sub-type addendum split (review Open Question 1) decided against; revisit if read cost grows.
- Harness-specific fixed versions for Claude Code CVEs left out (sources disagree); the rubric names the check.

### Plan Improvements
- None.

---

## Related Projex Updates

### Documents to Update
| Document | Update Needed |
|----------|---------------|
| `2610162007-agent-extension-rubric-refresh-plan.md` | Status Complete; Walkthrough link; moved to closed |
| `2610162007-agent-extension-rubric-refresh-log.md` | Moved to closed |
| `2604070218-install-auditor-subject-typed-redesign-nav.md` | Recent Progress, checklist, Revision Log, Last Revised |
| `2610161927-agent-extension-stewardship-review-eval.md` | Left active (eval and classifier follow-ups open) |

### New Projex Suggested
| Type | Description |
|------|-------------|
| Plan | Eval refresh for agent-extension (evals 22, 31, 23; new 8a/8b/8c, remote, poisoning, repo-borne cases) |

---

## Appendix

### References
- Execution commits: `de9b553` (step 1), `c48f92a` (step 2), `5a61152` (complete)
- Execution log: `2610162007-agent-extension-rubric-refresh-log.md`
