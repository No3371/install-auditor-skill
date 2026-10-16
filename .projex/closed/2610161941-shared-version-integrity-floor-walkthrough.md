# Walkthrough: Shared Version-Integrity Floor

> **Execution Date:** 2026-10-16
> **Completed By:** Claude (executor subagent) | closed by close-projex subagent
> **Source Plan:** 2610161941-shared-version-integrity-floor-plan.md
> **Parent:** 2610161941-shared-version-integrity-floor-plan.md
> **Duration:** ~32 min (19:58–20:30 per execution log timestamps)
> **Result:** Success (one verification caveat: A1 chalk range confirmed via secondary sources only — see Issues)

---

## Summary

Added `references/criteria.md` §4.6 *Version & Update Integrity (shared floor)* (V1 age/cooldown, V2 verified identity incl. curated-pipeline hook, V3 continuity, V4 version-scoped compromise, V5 updates/re-audit) and wired it into the dispatcher (`SKILL.md`), the report template, the registry workflow and the classifier. Human decisions C4 and C6 are encoded: tree node/term "Unpatched CVE" → **Blocking CVE** (KEV CRITICAL, or unfixed HIGH/CRITICAL in own code; all else HIGH flag → CONDITIONAL; VEX `not_affected` = evidence); C4 gets V1 version-unit and V2 curated-pipeline hooks. All 10 plan criteria pass; 41 evals / 248 assertions validate; 12 + 19 unit tests unchanged from Preflight.

**Human decisions recorded (relayed by orchestrator):**
- **C4 "Allow Tier 1 (Recommended)"** — Docker Official Images reach Tier 1 via pipeline + BuildKit attestations; hooks only here, subject rules → container plan.
- **C6 "Split by risk (Recommended)"** — REJECTED only for KEV CRITICAL or unfixed own-code HIGH/CRITICAL.
- **A6 literal KEV reading accepted by orchestrator** — a KEV-listed CRITICAL rejects the requested version even when a fix exists or it sits in an OS package; Recommendation names the fixed release. KEV-listed HIGH is not a REJECT class. Reversal = one table cell + one term clause.

---

## Objectives Completion

| Objective | Status | Notes |
|-----------|--------|-------|
| Write shared floor §4.6 V1–V5 with plug-in convention + hosted-service rule | Complete | Step 1; +70 lines in `references/criteria.md` |
| Wire criteria sections (tier intro, tooling note, coverage row + contract, §4.1, §4.2, §4.3) | Complete | Step 2; 10 replacements 2a–2j |
| Apply C6 to CVE mapping (§4.3 table + Own code / Fixed release / KEV / VEX definitions) | Complete | 2i/2j; Addendum line forbids changing verdict classes |
| Wire `SKILL.md` (precedence floor, Red Flag scope, confidence skips, skeleton row, V5 pointer, Step 0 carve-out, Blocking CVE) | Complete | Step 3; 9 replacements; 15,484 B ≤ 15,500 |
| Template carries Version integrity row, identity-matched verify, V5 re-audit | Complete | Step 4; 3 replacements |
| Align contradicting callers (registry "any version" rules; classifier no-reclassify line) | Complete | Step 5; 3 replacements |
| C4 hooks (V1 version unit, V2 curated pipelines) | Complete | In Step 1 text; subject plug-ins deferred to container plan by design |

---

## Execution Detail

> **NOTE:** Derived from git history (`968e70f..projex/2610161941-shared-version-integrity-floor`) and the execution log.

### Preflight

**Planned:** Baselines (SKILL.md size, validate, unittest counts, `any version` grep, `## 4.6` absence) + A1 chalk range check.
**Actual:** SKILL.md 14,995 B; validate 41 evals / 248 assertions; evals unittest 12 tests; tests unittest 19 (6 skipped); `any version` only at `workflows/registry-package.md:449` (A3 holds); criteria.md had no `## 4.6`. Base had moved (`7f137d1` lookup-script fixes) with no overlap on the 5 target files. A1: `scripts/vuln-lookup.py` and a direct OSV query denied by egress proxy (403); advisories API blocked; not retried. Fallback WebSearch: several secondary sources name chalk@5.6.1 as the single malicious version (removed within hours), 5.6.0 last known good → bounded range, excludes 5.3.0.
**Deviation:** A1 verified via secondary sources only (see Deviations).
**Files Changed:** none (log entry rode in Step 1 commit).

### Step 1: Add §4.6 to `references/criteria.md` (commit `0b30c32`)

**Planned:** Insert V1–V5 block before `## 4.7 OpenSSF Scorecard`.
**Actual:** Block inserted verbatim: plug-in convention, hosted-service rule, V1 table (< 72 h HIGH `fresh version` → CONDITIONAL; 72 h–7 d and Unknown bar Tier 1; ≥ 7 d none), V2 verified-identity rule + `**Curated pipelines:**` bullet, V3 continuity bullets, V4 cases a/b/c + incident-response note, V5 triggers/depth/update control. Before-anchor matched once.
**Deviation:** None.

| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `references/criteria.md` | Modified | Yes | +70 lines, new `## 4.6` at L242–L311 (post-Step 2 numbering); `## 4.7` now L312 |

**Verification:** `^### V[1-5] ` = 5; `^- \*\*Addendum:\*\*` = 5; Curated pipelines = 1; `^## 4\.` order 4.1–4.7.

### Step 2: Wire criteria sections + C6 CVE mapping (commit `9f9eb34`)

**Planned:** 10 replacements 2a–2j.
**Actual:** 2a tier intro adds 4.6; 2b "Audit tooling is itself a dependency" paragraph (X3); 2c Version integrity coverage row; 2d Tier 1 row-set text; 2e row contract (add rows, never drop; `N/A (<reason>)`; workflow-defined `Skipped (<reason>)`); 2f §4.1 identity-not-integrity note; 2g §4.2 abandoned → CONDITIONAL (reaches REJECTED only with another trigger); 2h §4.3 supply-chain scope note → V4; 2i CVE table (Critical: KEV → REJECTED, own code unfixed → REJECTED, else HIGH flag; High: own code unfixed → REJECTED, else HIGH flag); 2j Own code / Fixed release / KEV / VEX definitions + Addendum line.
**Deviation:** None.

| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `references/criteria.md` | Modified | Yes | +22/−5 in this commit; final file 21,455 B (plan ~21,455) |

**Verification:** `CONDITIONAL or REJECTED|if unpatched` = 0; Addendum lines = 6.

### Step 3: Wire `SKILL.md` (commit `be755d1`)

**Planned:** 9 replacements 3a–3i, ≤ 15,500 B.
**Actual:** 3a Step 0 generic Phase 2 carve-out; 3b Precedence names §4.6 floor; 3c/3d confidence accepts workflow-defined skips; 3e Version integrity skeleton row; 3f Recommendation → V5; 3g Red Flag "Confirmed supply chain compromise" version-scoped; 3h tree node `Any blocking CVE? (see Tree terms) ─────────────────► REJECTED ❌`; 3i **Blocking CVE** term. Fallback trims not needed.
**Deviation:** None.

| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `SKILL.md` | Modified | Yes | +9/−8; 14,995 → 15,484 B (headroom 16 B) |

**Verification:** stale-phrase grep 0; `§4.6` ×4; `Blocking CVE|blocking CVE` ×2; REJECTED-line widths `[64]`; parsed strings count unchanged (4).

### Step 4: Update `references/report-template.md` (commit `b6621d2`)

**Planned:** 4a–4c. **Actual:** as planned. **Deviation:** None.

| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `references/report-template.md` | Modified | Yes | +3/−2; Version integrity row; verify against expected identity (V2); hold updates + re-audit on V5 trigger |

**Verification:** `re-audit on major version bump` = 0; `§4.6` ×3.

### Step 5: Align contradicting callers (commit `282f7bf`)

**Planned:** 5a/5b registry bullets, 5c classifier. **Actual:** as planned, wrapped ~78 cols. **Deviation:** None.

| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `workflows/registry-package.md` | Modified | Yes | +6/−3; maintainer-compromise bullet scoped by affected range; known-malware bullet = malicious by design, else V4 |
| `references/classifier.md` | Modified | Yes | +2; generic Phase 2 sole exception to no-reclassify |

**Verification:** `exfiltration in any version` = 0; `§4.6 V4` in registry-package ×2; `Sole exception` ×1.

### Post-steps (execute) and close-time re-verification

Executor ran harness, consistency script and T1–T11 paper traces (all match plan; see Appendix). Closer re-ran the checks on the final branch head — results in Success Criteria below. Executor removed agent-created `evals/__pycache__` and `tests/__pycache__`; closer removed the leftover empty `scripts/.vuln-cache/` dir before finalization.

---

## Complete Change Log

> **Derived from:** `git diff --stat 968e70f..projex/2610161941-shared-version-integrity-floor` — authoritative.

### Files Created
| File | Purpose | Lines | In Plan? |
|------|---------|-------|----------|
| `.projex/2610161941-shared-version-integrity-floor-log.md` (now `.projex/closed/`) | Execution log | 87 | Yes (execute-projex artifact) |

### Files Modified
| File | Changes | Lines Affected | In Plan? |
|------|---------|----------------|----------|
| `references/criteria.md` | §4.6 V1–V5; wiring 2a–2j; C6 CVE table + definitions | +92/−5 | Yes |
| `SKILL.md` | 3a–3i | +9/−8 | Yes |
| `workflows/registry-package.md` | 5a/5b | +6/−3 | Yes |
| `references/report-template.md` | 4a–4c | +3/−2 | Yes |
| `references/classifier.md` | 5c | +2/−0 | Yes |
| `.projex/2610161941-shared-version-integrity-floor-plan.md` | Status → Complete, `Log:` field (execute); `Completed:`/`Walkthrough:` (close) | +2/−1 at execute | Yes |

### Files Deleted
None.

### Planned But Not Changed
None. Out-of-scope files untouched: `evals/evals.json` (0 diff lines), `STEWARDSHIP.md`, `scripts/*`, `references/registries.md`, addenda under `references/criteria/`.

---

## Success Criteria Verification

Re-verified by closer on branch head `ad9346f` in the execution worktree (before the close commit).

| Criterion | Method | Result | Evidence |
|-----------|--------|--------|----------|
| `criteria.md` has `## 4.6 …` with exactly 5 `### V1`…`### V5`, each (except hosted-service note) with one `**Addendum:**` line | grep counts | PASS | headings 5; `^- \*\*Addendum:\*\*` 6 (5 in §4.6 + 1 in §4.3); `## 4.6` at L242 |
| Every `§4.6 V<n>` reference resolves; none to V6+ | consistency script | PASS | `OK` |
| `SKILL.md` wiring: Red Flag renamed + scoped; Precedence floor; skeleton row; V5 pointer; confidence skips; Step 0 carve-out | grep + consistency script | PASS | `§4.6` ×4; `OK` |
| Tree node reads `Any blocking CVE? (see Tree terms)`; art width unchanged; term states REJECT classes, HIGH → CONDITIONAL, VEX | consistency script | PASS | REJECTED-line widths `{64}` single value |
| §4.3 table encodes C6; defines Own code / Third-party / Fixed release (KEV-with-fix) / KEV / VEX; Addendum forbids changing classes | read + grep | PASS | `CISA KEV`, `` `not_affected` `` present; 2i/2j in commit `9f9eb34` |
| V1 Addendum covers version unit (DOI base refreshes); V2 `**Curated pipelines:**` bullet exists | grep | PASS | Curated pipelines ×1 |
| `wc -c < SKILL.md` ≤ 15,500 | wc | PASS | 15484 |
| Stale phrases gone from the 5 files | consistency script | PASS | `OK` |
| Harness green with Preflight test count | validate + unittest | PASS | validate: 41 evals, 248 assertions; evals 12 tests OK (= Preflight 12); tests 19 OK, skipped=6 (= Preflight) |
| Paper traces T1–T11 give stated verdicts, rules cited | execution log walk | PASS | Log Post-steps entry; all 11 match |
| No diff outside the 5 files; `evals/evals.json` untouched | `git diff --name-only` | PASS | 5 shipped files + plan/log only; `evals/` 0 lines |

**Overall:** 11/11 passed.

---

## Deviations from Plan

### Deviation 1: A1 verified only via secondary sources
- **Planned:** Verify early via `scripts/vuln-lookup.py` or OSV/GHSA query that chalk's affected range is bounded and excludes 5.3.0.
- **Actual:** Live OSV/GHSA lookups were blocked (proxy 403 policy denial); WebSearch secondary sources (Semgrep, Cycode, mate.security, proarch) name chalk@5.6.1 as the sole malicious version, 5.6.0 last known good. No GHSA ID surfaced.
- **Reason:** Sandbox egress policy.
- **Impact:** A1 is **unconfirmed against a primary advisory**. The plan's stop rule (unbounded range → stop) was not triggered by any evidence found, but T1/eval 8 reachability of APPROVED rests on secondary sources.
- **Recommendation:** Confirm chalk's OSV/GHSA record from an unrestricted network before the single paid live eval run; no plan text change.

### Deviation 2: Step commit grouping (process, no content effect)
- **Planned:** Per-step commits.
- **Actual:** Steps 1–5 each own commit; Preflight log entry rode in Step 1 commit; final `projex: complete …` commit set plan status/`Log:` and the log.
- **Impact:** None.

### Deviation 3: Log `Worktree Path` header normalized at close
- **Planned/Actual:** Log recorded `install-auditor-skill/.projexwt/2610161941-shared-version-integrity-floor` (repo-name-prefixed), which `close-precheck.sh` cannot resolve. Closer rewrote it to repo-relative `.projexwt/2610161941-shared-version-integrity-floor` in the close commit.
- **Impact:** Doc-only; precheck then returned `PASS_WITH_WARNINGS` (warnings: that header edit uncommitted at the time; leftover empty ignored `scripts/.vuln-cache/`, removed).

No deviation from plan text in any shipped-file change; every Before string matched exactly once.

---

## Issues Encountered

### Issue 1: Egress proxy blocks OSV/GHSA
- **Description:** `vuln-lookup.py` and direct OSV query returned 403; `gh api /advisories` also denied.
- **Severity:** Medium (affects one verification, not shipped content).
- **Resolution:** Not retried per proxy policy; secondary-source fallback (Deviation 1).
- **Time Impact:** Minor.
- **Prevention:** Run A1-style advisory checks outside the sandbox, or pre-record primary source IDs in the plan.

### Issue 2: Tooling gaps in the close environment
- **Description:** `projex-tree.sh` fails (`.projex-tree.py` helper missing from the framework directory) — advisory only per spec. `close-precheck.sh` takes a plan path (not repo-root + filename) and must be run from the execution worktree; it needs the log's `Worktree Path` repo-relative.
- **Severity:** Low.
- **Resolution:** Ran precheck from worktree after header fix; skipped tree context.
- **Prevention:** Execute step should record `Worktree Path` repo-relative (`.projexwt/<name>`).

---

## Key Insights

**Rationale promoted:** none needed — all load-bearing rationale (thresholds, escalation exemption, KEV fallback, VEX source restriction, curated-pipeline scoping) is already written into shipped `references/criteria.md` §4.6/§4.3 and `SKILL.md` Tree terms; plan-only rationale (byte-budget trims) is non-load-bearing for the product.

### Lessons Learned

1. **Exact old→new replacement plans execute cleanly**
   - Context: 22 replacements across 5 files with simulated sizes.
   - Insight: Plan-time simulation gave byte-exact result (SKILL.md 15,484 B, criteria.md 21,455 B); no improvisation needed even though base moved.
   - Application: keep simulating size-budgeted edits at plan time.

2. **Unrelated concurrent base movement is safe when file sets are disjoint**
   - Context: `7f137d1` landed between plan and execute.
   - Insight: Disjoint-file declaration in Dependencies held; only per-step Before-anchor rechecks were needed.
   - Application: keep declaring file sets for concurrent plans.

### Pattern Discoveries

1. **Shared floor + addendum plug-ins**
   - Observed in: §4.6 with `**Addendum:**` lines and "addenda may tighten, never loosen" precedence.
   - Description: write a cross-subject rule once; subject files fill named plug-in points instead of copying the rule.
   - Reuse potential: any future cross-subject rule (e.g. KEV tooling follow-on).

### Gotchas / Pitfalls

1. **`SKILL.md` has 16 B headroom**
   - Trap: any later addition to `SKILL.md` breaches the 15,500 B ceiling.
   - How encountered: byte budget drove 3g shortening.
   - Avoidance: later plans must offset or justify their budget; Step 3's ordered trims are the first resort.

2. **Escalation text vs V1 exemption**
   - Trap: `SKILL.md` Escalation still says CONDITIONAL with HIGH flags gets an escalation notice; the `fresh version` exemption lives only in `criteria.md` V1 (plan decision, budget-driven).
   - Avoidance: if auditors over-escalate in live runs, fold the exemption into `SKILL.md` and trim elsewhere.

### Technical Insights

- Interim inconsistency is expected: addenda and `workflows/container-image.md` / registry `vuln-lookup` table still carry pre-C6 CVE wording until the per-subject plans run. §4.3's Addendum line makes §4.3 win in the interim.
- Live verdicts become calendar-dependent (V1 cooldown); the eval plan owns this.

---

## Recommendations

### Immediate Follow-ups
- [ ] Confirm chalk affected range from a primary advisory (OSV/GHSA) outside the sandbox (A1).
- [ ] Run the queued per-subject refresh plans against the §4.6 plug-ins (see plan Hand-off): registry-package (incl. C6 alignment after the lookup-script plan, now closed), ci-action, browser-extension/ide-plugin, container-image (C4/C6 subject parts), cli-binary, desktop-app, agent-extension, remote-integration + generic.
- [ ] Eval plan: time-dependent V1 effects on exact-APPROVED evals (0, 11, 16, 18, 20, 22, 36, 37); add cases for fresh version, provenance-valid-but-malicious, chalk-shape past compromise, V3 identity drop. One paid live eval run after all refreshes.

### Future Considerations
- Optional KEV lookup in `scripts/vuln-lookup.*`.
- RP-8 Scorecard host patch once verified.
- STEWARDSHIP (orchestrator): Last Reviewed dates; optionally list `references/criteria.md` §4.6 as a shared row.

### Plan Improvements
- Have the plan state that the executor should write `Worktree Path` repo-relative in the log.
- Pre-record primary advisory IDs for assumption checks that depend on a blocked network.

---

## Related Projex Updates

### Documents to Update
| Document | Update Needed |
|----------|---------------|
| 2610161941-shared-version-integrity-floor-plan.md | Complete; `Completed:` + `Walkthrough:` + `Log:` — done at close |
| 2610161941-shared-version-integrity-floor-log.md | Status Complete; moved to `closed/` — done at close |
| 2604070218-install-auditor-subject-typed-redesign-nav.md | Phase 6 milestone, Recent Progress entry, Revision Log row — done at close (stays open) |

Source evals (2610161927-*-stewardship-review-eval.md ×4, 2610161928-stewardship-review-container-cli-desktop-eval.md) stay active: they carry per-subject findings still open for the refresh plans. Not moved.

### New Projex Suggested
| Type | Description |
|------|-------------|
| Plan | Per-subject refresh plans filling §4.6 plug-ins (list above) |
| Plan | Eval plan for V1 time-dependence and new §4.6 cases |
| Patch | RP-8 Scorecard host, after host verification |

---

## Appendix

### Commits (ephemeral branch, base `968e70f`)
```
ad9346f projex: complete shared-version-integrity-floor
282f7bf projex: step 5 - scope registry compromise rules by version and add generic re-route exception
b6621d2 projex: step 4 - add version integrity row and V5 re-audit to report template
be755d1 projex: step 3 - wire SKILL.md to §4.6 floor and Blocking CVE
9f9eb34 projex: step 2 - wire criteria sections to §4.6 and Blocking CVE mapping
0b30c32 projex: step 1 - add criteria §4.6 version and update integrity
```

### Paper traces T1–T11 (from execution log)
- T1 chalk@5.3.0: V1 none; V4(c) LOW; Tier 1 barred; registry 5a/5b silent → APPROVED reachable.
- T2 6 h old + valid SLSA: V1 HIGH; V2 no offset → CONDITIONAL, no escalation notice.
- T3 verified publisher, minutes old, no upstream tag: V1 HIGH + V3 HIGH → CONDITIONAL with escalation notice.
- T4 version in malware advisory range: V4(a) Red Flag → REJECTED + incident-response note.
- T5 KICS-style repoint: V2 mismatch no credit; V3 HIGH → ≥ CONDITIONAL.
- T6 hosted OAuth connector: V1–V3 `N/A (hosted service)`; V5 lists triggers; verdict unchanged.
- T7 unfixed OS-package HIGH, non-KEV → CONDITIONAL.
- T8 lodash@4.17.20 → CONDITIONAL, install 4.17.21.
- T9 own-code KEV CRITICAL with fix → REJECTED, Recommendation names fix (A6).
- T10 OS-package KEV CRITICAL with applicable publisher VEX `not_affected` → left out of rating, not REJECTED on this CVE.
- T11 DOI redis dev → Tier 1 path open via the two hooks (container plan fills plug-ins).

### Verification output (closer, branch head `ad9346f`)
```
SKILL.md 15484 B; references/criteria.md 21455 B
validate: 41 evals, 248 assertions (82 deterministic, 166 model-graded)
unittest evals: Ran 12 tests OK; unittest tests: Ran 19 tests OK (skipped=6)
consistency script: OK
git diff --stat 968e70f..ad9346f: 7 files changed, 201 insertions(+), 19 deletions(-)
```

### Pre-close precheck
`close-precheck.sh`: first runs `ERROR` (log missing from base checkout; then `Worktree Path` unresolvable); after header fix and run from worktree → `PASS_WITH_WARNINGS` (ORIGIN_BASE PASS; no stashes).

### References
- Plan: 2610161941-shared-version-integrity-floor-plan.md
- Log: 2610161941-shared-version-integrity-floor-log.md
- Nav: 2604070218-install-auditor-subject-typed-redesign-nav.md
- Source evals: 2610161927-registry-package-and-ci-action-stewardship-review-eval.md | 2610161927-browser-extension-ide-plugin-stewardship-review-eval.md | 2610161928-stewardship-review-container-cli-desktop-eval.md | 2610161927-agent-extension-stewardship-review-eval.md | 2610161927-remote-integration-generic-stewardship-review-eval.md
