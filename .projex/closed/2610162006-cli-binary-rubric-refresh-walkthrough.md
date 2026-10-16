# Walkthrough: cli-binary Rubric Refresh

> **Execution Date:** 2026-10-16
> **Completed By:** Claude (executor subagent) | closed by close-projex subagent
> **Source Plan:** 2610162006-cli-binary-rubric-refresh-plan.md
> **Parent:** 2610162006-cli-binary-rubric-refresh-plan.md
> **Duration:** ~33 min (20:15-20:48 per execution log timestamps, plus verification)
> **Result:** Success

---

## Summary

cli-binary rubric refreshed to Oct 2026 and plugged into the shared floor. `references/criteria/cli-binary.md` 8,755 → 21,841 B (channel trust signals split core vs tap, identity-bound signature standards, install-script risk with URL provenance and executed-bytes rule, provenance assessment, tiers, `## Own Code vs Third-Party Components (§4.3)`, `## Version & Update Integrity (§4.6)` V1-V5). `workflows/cli-binary.md` 13,057 → 20,053 B (header, Identify, Evidence, coverage table, Subject Rubric, Verdict Notes; heading collision with shared §4.6 fixed). Consistency script `OK`; harness unchanged; paper traces T1-T14 match. Two logged deviations, both accepted by the orchestrator (Step 5d rewrap; Step 6 grep count).

---

## Objectives Completion

| Objective | Status | Notes |
|-----------|--------|-------|
| X1 / B7 credit only identity-matched verification | Complete | Per-method commands with identity flags (`cosign verify-blob --bundle` with `--certificate-identity` + `--certificate-oidc-issuer`, `slsa-verifier verify-artifact --source-uri`) |
| X2 version-level age | Complete | V1 plug-in (publish-time source, version unit, condition wording) |
| X3 pinned audit tooling | Complete | Cites the `references/criteria.md` audit-tooling note |
| B1 core vs tap | Complete | Separate `Homebrew core formula` / `Homebrew third-party tap` rows in both files; core = V2 curated pipeline |
| B2 immutable releases and attestations | Complete | `gh release verify`, `gh release verify-asset`, `gh attestation verify` rows and commands |
| B3 nvm / rustup / Volta facts | Complete | OpenJS Foundation nvm; Volta unmaintained → Abandoned (mise / fnm / uv named) |
| B4 install-command lures, executed bytes | Complete | Install-URL provenance, lure patterns (→ CRITICAL), executed-bytes rule |
| B5 abandoned ≠ REJECTED | Complete | Moved to Toward CONDITIONAL; REJECTED only with another REJECTED trigger |
| B6 verified copy vs unverifiable mirror | Complete | Verified-bytes rule |
| C6 own-code / third-party line | Complete | `## Own Code vs Third-Party Components (§4.3)` |
| Heading collision | Complete | `### §4.6 Alternatives & Ecosystem Fit` → `### Alternatives & Ecosystem Fit`; `### §4.6 Version & Update Integrity` added |
| G-3 PowerShell pipe-to-shell / eval 34 | Complete | PowerShell rows, executed-bytes commands, opaque / plain-HTTP-URL pipe-to-shell bullet → CRITICAL |

---

## Execution Detail

> Derived from `git log`/`git diff` of `f04068c..projex/2610162006-cli-binary-rubric-refresh` (merge base) and the execution log. The named base advanced during execution; the merge-base comparison is the scope-correct one.

### Preflight

**Planned:** floor checks, line counts, harness baseline.
**Actual:** floor checks all 1/1/1/1/1; "Abandoned → CONDITIONAL" present in `references/criteria.md`; `wc -l` 262 / 133; `validate` 41 evals / 248 assertions; unittest evals 12 OK; tests 19 OK (6 skipped). Plan status set to In Progress on base (`ff2d0c8`).
**Deviation:** None.

### Step 1: Addendum header + Distribution Channel Trust Signals

**Planned:** splice After block over addendum L1-L37.
**Actual:** block extracted programmatically from the plan; 37 → 47 lines. `Homebrew third-party tap` 2; `build-from-source option` / `Node.js Foundation` 0. Commit `8f079d3`.
**Deviation:** None.

### Step 2: Addendum Signature & Checksum Standards

**Planned:** splice over `## Signature & Checksum Standards` region.
**Actual:** 21 → 32 lines. Command-name greps 4 (≥ 4); `provides audit trail` 0. Commit `c06b709`.
**Deviation:** None.

### Step 3: Addendum Install Script Risk + Provenance Assessment

**Planned:** splice over both sections.
**Actual:** 39 → 55 lines. `Executed-bytes rule` / `Lure patterns` / `Install-URL provenance` = 3. Commit `d267467`.
**Deviation:** None.

### Step 4: Addendum Tier Thresholds + §4.3 and §4.6 plug-ins

**Planned:** splice over Tier Thresholds to EOF; check A2 scanner names.
**Actual:** A2 confirmed: `govulncheck -mode=binary` (govulncheck `-h`) and `cargo audit bin` (cargo-audit 0.22.2 README). 33 → 56 lines. §4.6 heading 1; `- **V1**`..`- **V5**` 5; §4.3 heading 1; `Curated pipeline — Homebrew core` 1. Addendum now 193 lines. Commit `02f55cf`.
**Deviation:** None.

### Step 5: Workflow header, Identify, Evidence

**Planned:** five After blocks 5a-5e.
**Actual:** spliced bottom-up between exact anchors (5e 50 → 69 lines, 5d 13 → 19, 5c 7 → 10, 5b 17 → 24, 5a 32 → 36). `Homebrew third-party tap` 2; old `verify-blob or transparency log` step gone. Commit `483a80a`.
**Deviation:** Deviation 1 (5d rewrap), below.

### Step 6: Workflow coverage table, Subject Rubric, Verdict Notes

**Planned:** splice over `| Check | Tier 1 | Tier 2 | Tier 3 |` to EOF.
**Actual:** 105 → 158 lines; workflow 354 lines. Toward REJECTED "abandon" 0; `### §4.6 Version & Update Integrity` + `### Alternatives & Ecosystem Fit` 2; stale strings 0. Commit `3e155a4`; completion commit `592080f`.
**Deviation:** Deviation 2 (grep count), below.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `references/criteria/cli-binary.md` | Modified | Yes | ~35 hunks across lines 4-193 (header, channel signals, signature standards, install-script risk, provenance, tiers, new §4.3 and §4.6 sections at the tail, lines ~174-193); 148 lines changed |
| `workflows/cli-binary.md` | Modified | Yes | ~40 hunks across lines 4-354 (header, Identify, Evidence Parts A+B, coverage table, Subject Rubric, Verdict Notes); 228 lines changed |

---

## Complete Change Log

> **Derived from:** `git diff --stat f04068c..projex/2610162006-cli-binary-rubric-refresh`: 4 files changed, 380 insertions(+), 113 deletions(-) (including projex documents).

### Files Created
| File | Purpose | Lines | In Plan? |
|------|---------|-------|----------|
| `.projex/2610162006-cli-binary-rubric-refresh-log.md` | Execution log | 114 | Yes (implicit) |
| `.projex/closed/2610162006-cli-binary-rubric-refresh-walkthrough.md` | This walkthrough | - | Yes (close) |

### Files Modified
| File | Changes | Lines Affected | In Plan? |
|------|---------|----------------|----------|
| `references/criteria/cli-binary.md` | Rewrite of 4 sections + 2 new plug-in sections | 148 changed; 21,841 B | Yes |
| `workflows/cli-binary.md` | 2 regions rewritten plus header and Identify | 228 changed; 20,053 B | Yes |
| `.projex/2610162006-cli-binary-rubric-refresh-plan.md` | Status Complete, Log, Walkthrough link | 3 lines | Yes (close) |

### Files Deleted
None.

### Planned But Not Changed
None. `evals/`, `SKILL.md`, `references/criteria.md`, `references/classifier.md` untouched, as scoped.

---

## Success Criteria Verification

| Criterion | Method | Result | Evidence |
|-----------|--------|--------|----------|
| One §4.6 heading with V1-V5; one §4.3 heading | grep | Pass | 1 / 5 / 1 |
| V2 names the curated pipeline with the auditor's checks | grep | Pass | `Curated pipeline — Homebrew core` 1 |
| Separate core / tap channel rows in both files | script | Pass | met |
| Required commands present | script + grep | Pass | `gh release verify`, `verify-asset`, `gh attestation verify`, `cosign verify-blob --bundle` + identity flags, `slsa-verifier verify-artifact --source-uri` |
| Stale strings gone | script | Pass | 0 |
| Toward REJECTED has no "abandon"; Toward CONDITIONAL has it with the clause | awk + script | Pass | see Deviation 2 for the line-count artifact |
| Every `§4.6 V<n>` is V1-V5 | script | Pass | `OK` |
| `validate` + unittest with Preflight count | harness | Pass | 41 / 248; evals 12 OK; tests 19 OK (6 skipped) |
| Paper traces T1-T14 | manual walk | Pass | all match (execution log "Paper traces") |
| Exactly 2 files in scope; protected files untouched | `git diff --stat <base>...HEAD` | Pass | 2 shipped files + log |

**Overall:** 10/10 criteria passed.

---

## Deviations from Plan

### Deviation 1: Step 5d Tier 3 paragraph rewrapped
- **Planned:** verbatim After block.
- **Actual:** one paragraph of the 5d block contained a 97-column prose line, breaking the plan's own wrap constraint (~72-75 cols). Rewrapped at ~72 cols; word-for-word identical.
- **Reason:** plan internal inconsistency (constraint vs verbatim text).
- **Impact:** none on content.
- **Recommendation:** none; orchestrator accepted.

### Deviation 2: Step 6 `grep -c "REJECTED"` count
- **Planned:** count of 1 over the Toward CONDITIONAL section.
- **Actual:** 2. The plan's verbatim text wraps the "REJECTED only together with another REJECTED trigger" clause across two lines of one bullet.
- **Reason:** line-wrap artifact of the plan's check, not a text defect; Success Criteria bullet 6 (section contains "abandoned" with the clause) holds.
- **Impact:** none; text left verbatim.
- **Recommendation:** use a multi-line-aware check in future plans; orchestrator accepted.

### Deviation 3: No task-list tool
- Step discipline tracked through per-step log entries and commits. No impact.

---

## Issues Encountered

### Issue 1: Precheck WARN on other plans' files
- **Description:** uncommitted entries in the main checkout belonged to other plans.
- **Severity:** Low
- **Resolution:** untouched.

### Issue 2: Base advanced during execution
- **Description:** worktree cut from `f04068c`; other plans closed onto base afterward.
- **Severity:** Low
- **Resolution:** scope verified against the merge base; no overlap with the two cli-binary files; this close squash-merged them without conflict (only the roadmap nav conflicted, resolved keeping both sides).

### Close notes
- Nav `2604070218-install-auditor-subject-typed-redesign-nav.md` updated in the close commit, following earlier rubric-refresh closes (plan carries no `Nav:` field).

---

## Key Insights

**Rationale promoted:** none needed. Rationale ships in the addendum and workflow text; no shipped file carries projex references (grep clean).

### Lessons Learned

1. **Keep plan checks consistent with plan constraints**
   - Context: Deviations 1 and 2 both arose from the plan's own text conflicting with its own check or wrap rule.
   - Insight: verbatim After blocks should be lint-checked against the plan's constraints at planning time.
   - Application: add a wrap/grep dry-run to the planning simulation.

### Gotchas / Pitfalls

1. **A signature that is merely present**
   - Trap: Rekor / signature presence credited as an audit trail.
   - Avoidance: credit only identity-matched verification (V2); a different repo, workflow, key or signer is HIGH (V3).

2. **Paste-to-verify lures**
   - Trap: install commands that look like a vendor's documented command.
   - Avoidance: lure pattern requires both lure framing and a command that is not the vendor's documented one, then CRITICAL.

---

## Recommendations

### Immediate Follow-ups
- [ ] T11: `references/criteria.md` §4.3 says the third-party-no-fix condition is "the routed workflow's mitigations", but the cli-binary workflow has no explicit mitigation list, so the auditor composes one in the Recommendation (least privilege, sandbox, pin). Add an explicit mitigation list.
- [ ] The PowerShell Tier 3 trigger ("`irm | iex` from any source") does not match the Scoring impact "Tier 2 minimum" for the known-vendor form (the same pairing existed for `curl | sh` in the base text). Reconcile.
- [ ] Classifier hand-offs pending (`references/classifier.md` / `SKILL.md` Type 7 row; classifier owner): route `brew install <user>/<tap>/<formula>` (third-party tap) to cli-binary (a tap `--cask` → desktop-app); replace the `volta` example with `mise`; change "Formula review + checksum + build-from-source" to "maintainer review + Homebrew CI bottle".
- [ ] Observation: the addendum's "strong negative" for an unverified shared copy (T3) is a score, while the verdict is fixed by the Verdict Notes (CONDITIONAL); consider wording to avoid misreading it as CRITICAL.
- [ ] Orchestrator: relay `### §4.6 …` heading collisions in `workflows/agent-extension.md` and `workflows/remote-integration.md`; update the `STEWARDSHIP.md` cli-binary row dates.
- [ ] Eval plan: eval 20 description ("homebrew/core (maintainer-reviewed; bottle built and attested by Homebrew CI)"; Tier 1 / APPROVED is time-dependent on ripgrep's latest release age); new cases from T4-T9 (T4 verified share copy → APPROVED; T5/T6 tap → not Tier 1; T7 lure → REJECTED; T8 immutable + attested → APPROVED; T9 fresh + signer drift → CONDITIONAL).
- [ ] Desktop-app planner: Homebrew's own security doc is a primary source for D5 (cask Gatekeeper rule; `brew trust` for third-party taps since Homebrew 6.0.0).

### Future Considerations
- The tension between "known-vendor install script → CONDITIONAL" and "language-version manager → APPROVED" predates this plan and is left as-is.
- Facts hedged or not verified (immutable-release coverage details; exact `gh` version introducing `release verify`; GoReleaser per-artifact bundles; `brew verify` without developer mode) are listed in the plan Notes.

### Plan Improvements
- Dry-run the plan's greps and wrap constraint against its own After blocks.

---

## Related Projex Updates

### Documents to Update
| Document | Update Needed |
|----------|---------------|
| `2610162006-cli-binary-rubric-refresh-plan.md` | Status Complete; Walkthrough link; moved to closed |
| `2610162006-cli-binary-rubric-refresh-log.md` | Moved to closed |
| `2604070218-install-auditor-subject-typed-redesign-nav.md` | Recent Progress, checklist, Revision Log, Last Revised |
| `2610161928-stewardship-review-container-cli-desktop-eval.md` | All three subject plans (container, desktop, cli-binary) are now closed, but the eval also carries other findings (X-series, eval hand-offs); left active for the orchestrator to close |

### New Projex Suggested
| Type | Description |
|------|-------------|
| Plan | Eval refresh for cli-binary (eval 20, new cases T4-T9) |
| Patch/Revise | Classifier hand-offs; cli-binary consistency patch (mitigation list, PowerShell tier wording) |

---

## Appendix

### References
- Execution commits: `8f079d3` (step 1), `c06b709` (step 2), `d267467` (step 3), `02f55cf` (step 4), `483a80a` (step 5), `3e155a4` (step 6), `592080f` (complete)
- Execution log: `2610162006-cli-binary-rubric-refresh-log.md`
