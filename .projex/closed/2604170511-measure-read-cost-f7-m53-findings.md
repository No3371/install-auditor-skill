# Findings: Measure Read-Cost Claim (Eval F7) — M5.3

> **Status:** Complete
> **Created:** 2026-04-17
> **Author:** Claude (projex agent)
> **Source Plan:** `2604170511-measure-read-cost-f7-m53-plan.md`
> **Nav:** `2604070218-install-auditor-subject-typed-redesign-nav.md`
> **Related Eval:** `2604070217-subject-typed-audit-dispatch-eval.md` (F7 claim origin)

---

## Executive Summary

**F7 is refuted.** Per-audit read cost rises 20–150% under dispatch vs the old monolith for every subject type. The smallest per-audit read under dispatch (dispatcher + generic.md = 18,973 B) already exceeds the old monolith (15,851 B) by 3,122 B (+20%). The heaviest type (container-image) reads 39,692 B — 2.5× the monolith.

The efficiency argument for dispatch does not hold on raw byte cost. Dispatch retains qualitative benefits independent of this finding.

---

## Measurements

### Baselines

| Snapshot | Lines | Bytes | Notes |
|---|---:|---:|---|
| Old monolith SKILL.md (`1b02882`) | 306 | 15,851 | Pre-refactor; single file per audit |
| Phase 1 dispatcher SKILL.md (`3842b76`) | 218 | 13,126 | First dispatcher, before M5.1 classifier tightening |
| Current dispatcher SKILL.md (HEAD) | 242 | 15,272 | After M5.1 classifier tightening (+2,146 B) |

### Workflow Files

| Workflow | Lines | Bytes |
|---|---:|---:|
| `generic.md` | 80 | 3,701 |
| `ci-action.md` | 219 | 8,019 |
| `remote-integration.md` | 175 | 10,568 |
| `agent-extension.md` | 230 | 12,977 |
| `cli-binary.md` | 264 | 13,393 |
| `ide-plugin.md` | 358 | 16,186 |
| `desktop-app.md` | 360 | 17,344 |
| `browser-extension.md` | 369 | 17,689 |
| `registry-package.md` | 488 | 23,304 |
| `container-image.md` | 319 | 24,420 |
| **Total** | **2,862** | **147,601** |

---

## Comparison Table

Per-audit read cost: old monolith (15,851 B) vs current dispatcher SKILL.md (15,272 B) + workflow.

| Subject Type | Dispatcher (B) | Workflow (B) | Combined (B) | vs Monolith | Delta | Verdict |
|---|---:|---:|---:|---:|---:|---|
| generic | 15,272 | 3,701 | 18,973 | 15,851 | +3,122 (+20%) | WORSE |
| ci-action | 15,272 | 8,019 | 23,291 | 15,851 | +7,440 (+47%) | WORSE |
| remote-integration | 15,272 | 10,568 | 25,840 | 15,851 | +9,989 (+63%) | WORSE |
| agent-extension | 15,272 | 12,977 | 28,249 | 15,851 | +12,398 (+78%) | WORSE |
| cli-binary | 15,272 | 13,393 | 28,665 | 15,851 | +12,814 (+81%) | WORSE |
| ide-plugin | 15,272 | 16,186 | 31,458 | 15,851 | +15,607 (+98%) | WORSE |
| desktop-app | 15,272 | 17,344 | 32,616 | 15,851 | +16,765 (+106%) | WORSE |
| browser-extension | 15,272 | 17,689 | 32,961 | 15,851 | +17,110 (+108%) | WORSE |
| registry-package | 15,272 | 23,304 | 38,576 | 15,851 | +22,725 (+143%) | WORSE |
| container-image | 15,272 | 24,420 | 39,692 | 15,851 | +23,841 (+150%) | WORSE |

**Range:** +20% (generic) to +150% (container-image). All 10 types worse.

### Phase 1 Baseline Check

Even at the smaller Phase 1 dispatcher (13,126 B) before M5.1 added ~2 KB, every combo still exceeds the monolith:

- Smallest: 13,126 + 3,701 (generic) = **16,827 B** — exceeds monolith by 976 B (+6.2%)
- All other types: larger workflows → larger excess

F7 refuted under both Phase 1 and current baselines.

---

## Root Cause

The F7 claim assumed the dispatcher SKILL.md would compress to ~4 KB — much smaller than the 15,851 B monolith — so adding any workflow would still net less. That compression target was missed.

The dispatcher SKILL.md retained load-bearing content from the monolith:

- **Step N verdict tree** — full structured audit logic, cannot be removed without losing audit capability
- **Audit-coverage report skeleton** — required output format for every audit, blocks compression
- **Red flags table and subject-type routing logic** — classifier content grew further in M5.1

Result: dispatcher SKILL.md (15,272 B) is nearly as large as the old monolith (15,851 B), leaving only 579 B of headroom. Adding any workflow immediately exceeds the monolith. M5.1 classifier tightening added ~2,146 B (13,126 → 15,272), shrinking that headroom further from what Phase 1 had.

This deviation was noted in the M1.1 execution log: Step N's report skeleton was identified as the primary blocker to dispatcher compression at the time of the refactor.

---

## Nuance

Raw read cost is not the only dimension. Dispatch retains real qualitative benefits independent of F7:

- **Subject-specific rubrics** — each workflow has tailored audit criteria vs the monolith's generic checks
- **Maintainability** — workflow files can be updated independently without touching the core dispatcher
- **Extensibility** — new subject types require only a new workflow file, not monolith surgery
- **Cognitive focus** — the model reads only one subject's workflow, not all subject content at once (even if byte count is higher)

F7 as stated ("per-audit read cost drops under dispatch") is false. The dispatch architecture's other value claims remain valid.

---

## Recommendation

Two options, both viable:

1. **Accept the trade-off.** Document F7 as refuted. Keep the dispatch architecture for its qualitative benefits. The per-audit read cost increase is real but bounded (~20–150%) and the subject-specific quality improvement may justify it.

2. **Pursue dispatcher compression.** Future milestone: aggressively compress SKILL.md by externalizing the Step N report skeleton and red flags table into a shared utilities file loaded alongside the workflow. Target: reduce dispatcher to ~6–8 KB. This would make F7 true for smaller workflows (generic, ci-action) at minimum.

Option 1 is recommended as the default — the architecture decision stands; only the efficiency claim needs honest correction. Option 2 is a future-phase enhancement, not a correctness fix.

---

## Conclusion

F7 — "per-audit read cost drops under dispatch even though total file count rises" — is **empirically refuted**. Byte measurements confirm per-audit read cost rises 20–150% across all 10 subject types. The dispatch architecture provides subject-specific quality and maintainability benefits that stand on their own merits, but the raw efficiency claim does not hold.
