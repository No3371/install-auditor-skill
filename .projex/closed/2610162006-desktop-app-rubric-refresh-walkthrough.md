# Walkthrough: Desktop-App Rubric Refresh

> **Execution Date:** 2026-10-16
> **Completed By:** Claude (executor subagent) | closed by close-projex subagent
> **Source Plan:** 2610162006-desktop-app-rubric-refresh-plan.md
> **Parent:** 2610162006-desktop-app-rubric-refresh-plan.md
> **Duration:** ~25 min (20:30-20:55 per execution log timestamps)
> **Result:** Success

---

## Summary

Desktop-app rubric rewritten on the shared §4.6 floor. `references/criteria/desktop-app.md` 10,255 → 22,632 B (channel table, code-signing standards, installer/sandbox/updater rows, tiers, `## CVE Scope (§4.3)`, `## Version & Update Integrity (§4.6)` V1-V5). `workflows/desktop-app.md` 16,915 → 21,500 B (28 replacements). Sizes equal the plan's simulated sizes; every Before anchor (44 pairs, 3 section bounds) occurred exactly once; consistency script `OK`; paper traces P1-P10 match; harness unchanged.

---

## Objectives Completion

| Objective | Status | Notes |
|-----------|--------|-------|
| D1 non-notarized macOS = weak + HIGH `not notarized`; bypass instructions are a lure | Complete | Addendum Code Signing Standards + Scoring |
| D2 / X1 signature credit only per V2 (signer matched to vendor identity) | Complete | Scoring bullet "Credit a signature only per V2"; V2 plug-in names the commands |
| D3 EV / HSM / short-lived certs; Artifact Signing row | Complete | EV row corrected; subject-not-thumbprint matching; `Artifact Signing` x3 |
| D4 Microsoft Store: three rows (MSIX AppContainer, full trust, unpackaged Win32) | Complete | `^| Microsoft Store — ` = 3; Tier 1 not on a listing alone |
| D5 cask gate + third-party taps | Complete | `third-party tap` x2; `sha256 :no_check` = no checksum credit |
| D6 unverified updater = HIGH everywhere; updater-framework advisories | Complete | One severity in table row, scoring bullet, workflow Toward CONDITIONAL |
| D7 Snap/Flathub legitimacy vs confinement; Flatpak runtime version | Complete | Step 1b/3 rows |
| D8 signed EXE with matched signer = note | Complete | Workflow "EXE installer from known vendor" removed |
| D9 APT `signed-by=` scoped vs global key | Complete | MEDIUM flag for global keyring |
| Floor plug-ins + coverage rows + heading collision | Complete | V1-V5, CVE Scope, `Version integrity (§4.6)` row, canonical-name map; `### 4.6 Alternatives` → `### Alternatives …` |

---

## Execution Detail

> Derived from `git log`/`git diff` of `fc4a6d8..projex/2610162006-desktop-app-rubric-refresh` (branch point) and the execution log.

### P0 Preflight

**Planned:** floor greps, empty diff on target files since `968e70f`, harness baseline.
**Actual:** `## 4.6 … (shared floor)` 1 | `### V[1-5] ` 5 | `Curated pipelines` 1 | own-code line 1 | `Blocking CVE` 1 | `Confirmed supply chain compromise` 2. Target files unchanged since `968e70f`. `validate`: 41 evals, 248 assertions. unittest evals 12 OK; tests 19 OK (6 skipped). Baseline sizes 10,255 / 16,915. Commit `67f60f1`.
**Deviation:** None.

### Step 1: Addendum header coverage + Distribution Channel section

**Planned:** pair 1a and whole-section swap 1b (`## Distribution Channel Trust Signals` through the third-party mirror bullet).
**Actual:** After text extracted verbatim from the plan by script; every Before/bound asserted once. `^| Microsoft Store — ` = 3; stale phrases = 0; `third-party tap` = 2. Commit `9dd968b`.
**Deviation:** None.

### Step 2: Addendum Code Signing Standards section

**Planned:** swap block `## Code Signing Standards` through "Unsigned on any platform = HIGH flag …".
**Actual:** applied verbatim; stale phrases 0; `Artifact Signing` 3; `not notarized` 3. Commit `e86400d`.
**Deviation:** None.

### Step 3: Addendum installer, sandbox, auto-update rows

**Planned:** 11 exact replacements 3a-3k.
**Actual:** 11/11 applied without a miss. `Unsigned update channel = MEDIUM` 0; `| High | Persistent attack surface` 1; `^| MSIX ` 3. Commit `77cc856`.
**Deviation:** None.

### Step 4: Addendum precedence line, tiers, CVE Scope, Version & Update Integrity

**Planned:** 4a-4d exact pairs; append 4e (two new sections).
**Actual:** applied; `^- \*\*V[1-5] ` = 5; no `REJECTED` inside `## CVE Scope`; both headings once. Commit `42e595e`.
**Deviation:** None.

### Step 5: Workflow alignment

**Planned:** 28 exact replacements 5a-5ab to `workflows/desktop-app.md`.
**Actual:** 28/28 applied, ~76-col wrapping preserved. `### 4.6` 0; `Version integrity (§4.6)` 1; `signed by definition` / `EXE installer from known vendor` / `GitHub stars on` 0. Commit `48d5a55`; completion commit `2c372c6`.
**Deviation:** None.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `references/criteria/desktop-app.md` | Modified | Yes | Hunks across lines 4-224: header coverage, channel table (Store/cask/tap/winget/Snap/Flathub rows), code-signing table and scoring, installer/sandbox/updater rows, tier lists, new `## CVE Scope (§4.3)` and `## Version & Update Integrity (§4.6)` (lines ~184-224); 145 lines changed |
| `workflows/desktop-app.md` | Modified | Yes | 28 hunks at lines 30-422: identify/channel, research questions, signing and installer checks, coverage table + canonical-name map, Verdict Notes, `### Alternatives` heading; 153 lines changed |

**Verification:** see Success Criteria below.

---

## Complete Change Log

> **Derived from:** `git diff --stat fc4a6d8..projex/2610162006-desktop-app-rubric-refresh` (branch point; the named base advanced mid-execution with unrelated files)

### Files Created
| File | Purpose | Lines | In Plan? |
|------|---------|-------|----------|
| `.projex/2610162006-desktop-app-rubric-refresh-log.md` | Execution log | 86 | Yes (implicit) |
| `.projex/closed/2610162006-desktop-app-rubric-refresh-walkthrough.md` | This walkthrough | - | Yes (close) |

### Files Modified
| File | Changes | Lines Affected | In Plan? |
|------|---------|----------------|----------|
| `references/criteria/desktop-app.md` | Rewrite of channel/signing sections, row fixes, two new plug-in sections | 145 changed; 22,632 B | Yes |
| `workflows/desktop-app.md` | 28 replacements | 153 changed; 21,500 B | Yes |
| `.projex/2610162006-desktop-app-rubric-refresh-plan.md` | Status Complete, Log, Walkthrough link | 3 lines | Yes (close) |

### Files Deleted
None.

### Planned But Not Changed
None. `SKILL.md`, `references/criteria.md`, `references/report-template.md`, `references/classifier.md`, `evals/`, `STEWARDSHIP.md` untouched, as scoped.

---

## Success Criteria Verification

| Criterion | Method | Result | Evidence |
|-----------|--------|--------|----------|
| Addendum has `## Version & Update Integrity (§4.6)` with one bullet each V1-V5 and `## CVE Scope (§4.3)` | grep + consistency script | Pass | `^- \*\*V[1-5] ` = 5; headings once each |
| Every `§4.6 V<n>` resolves to a `### V<n> ` heading in `references/criteria.md` | consistency script | Pass | `OK` |
| Stale phrases absent (11 listed) | consistency script, case-insensitive | Pass | 0 hits in both files |
| One severity (HIGH) for unverified update channel in table row, scoring bullet, workflow | grep | Pass | `| High | Persistent attack surface` 1; `HIGH flag. Condition: turn off` present |
| Coverage table has `Version integrity (§4.6)` row (Required x3) + canonical-name map | grep | Pass | row 1, `Canonical row names` 1 |
| No `REJECTED` in CVE Scope | script | Pass | 0 |
| `validate` + unittest with Preflight count | harness | Pass | 41 evals / 248 assertions; evals 12 OK; tests 19 OK (6 skipped) |
| Paper traces P1-P10 | manual walk | Pass | all ten match (execution log "Verification") |
| `git diff --stat` lists only the 2 files | `fc4a6d8..HEAD` | Pass | 2 shipped files + log (+ plan status) |

**Overall:** 9/9 criteria passed.

---

## Deviations from Plan

None. Verify-Projex (Encouraged on Steps 2, 4, 5) and Do-Projex (Encouraged on Steps 1, 3) were not delegated because the executor had no subagent tool at its depth; each step was self-verified with machine-extracted, byte-exact text plus grep/diff evidence.

---

## Issues Encountered

### Issue 1: Base advanced mid-execution
- **Description:** Named base moved from `fc4a6d8` to `dcb8398` (remote-integration close) and later commits during execution.
- **Severity:** Low
- **Resolution:** No file overlap with the two target files; branch point `fc4a6d8` used for comparison. Close squash merged the subject files cleanly.

### Issue 2: Precheck WARN on other agents' documents
- **Description:** Uncommitted projex documents belonging to other agents on the main checkout.
- **Severity:** Low
- **Resolution:** Left untouched, never staged.

### Close notes
- Nav `2604070218-install-auditor-subject-typed-redesign-nav.md` updated in the close commit, following the precedent of earlier rubric-refresh closes (plan carries no `Nav:` field). Add/add conflicts with base's concurrent entries resolved by keeping both sides.

---

## Key Insights

**Rationale promoted:** none needed. Rationale ships in the addendum and workflow text; no source files carry projex references (grep for `projex` / `2610` in both files empty).

### Lessons Learned

1. **Machine-extract plan blocks**
   - Context: 44 Before/After pairs plus section swaps across two files.
   - Insight: extracting After text verbatim and asserting each Before occurs exactly once makes drift visible immediately; resulting sizes matched the plan's simulation to the byte.
   - Application: keep simulation sizes in rubric-refresh plans as a cheap integrity check.

### Gotchas / Pitfalls

1. **Heading collisions with the shared §4.6**
   - Trap: workflow headings `### 4.6 …` collide with `references/criteria.md` §4.6; other workflows still carry them (registry-package, browser-extension, cli-binary, ide-plugin, ci-action, container-image, agent-extension, remote-integration per the plan's Cross-cutting note).
   - Avoidance: each owning plan renumbers or drops the number; desktop is fixed here.

### Technical Insights

- The notarized MacSync dropper (2025-12) shows signature presence is not trust; V2 identity matching is the credit gate.
- Platform facts (Gatekeeper, SmartScreen/EV, Store packaging, Homebrew 5.0.0 cask gate) were re-verified 2026-10-16 per the plan's Sources; A2/A4/A5 commands were quoted, not run (Linux host).

---

## Recommendations

### Immediate Follow-ups
- [ ] Eval refresh plan: eval 18 description (NSIS EXE → Tier 2, APPROVED still reachable), eval 29 wording (package kind unverified), new cases P4-P8 and P10 (plan Notes → Eval hand-off).
- [ ] Orchestrator: align the §4.3 plug-in heading across addenda (desktop uses `## CVE Scope (§4.3)`; the cli-binary plan uses `## Own Code vs Third-Party Components (§4.3)`).
- [ ] Classifier owner: bare `brew install <name>` may install a cask when no formula exists; `references/classifier.md` routes bare `brew install` to cli-binary (Homebrew behavior from memory, not re-verified).
- [ ] STEWARDSHIP: desktop-app Last Reviewed = 2026-10-16; trigger text could add store packaging policy, Gatekeeper/notarization, CA/B code-signing ballots.

### Future Considerations
- V1 (< 72 h) time dependence on winget/Store apps (eval 18) belongs to the eval plan.

### Plan Improvements
- None beyond keeping simulated sizes and exact-once anchors.

---

## Related Projex Updates

### Documents to Update
| Document | Update Needed |
|----------|---------------|
| `2610162006-desktop-app-rubric-refresh-plan.md` | Status Complete; Walkthrough link; moved to closed |
| `2610162006-desktop-app-rubric-refresh-log.md` | Moved to closed |
| `2604070218-install-auditor-subject-typed-redesign-nav.md` | Recent Progress, checklist, Revision Log, Last Revised |
| `2610161928-stewardship-review-container-cli-desktop-eval.md` | Left active (container and cli-binary plans still pending) |

### New Projex Suggested
| Type | Description |
|------|-------------|
| Plan | Eval refresh covering desktop cases P4-P8, P10 and eval 18 / 29 wording |

---

## Appendix

### References
- Execution commits: `67f60f1` (preflight), `9dd968b` (step 1), `e86400d` (step 2), `77cc856` (step 3), `42e595e` (step 4), `48d5a55` (step 5), `2c372c6` (complete)
- Execution log: `2610162006-desktop-app-rubric-refresh-log.md`
