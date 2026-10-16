# Walkthrough: IDE-Plugin Rubric Refresh

> **Execution Date:** 2026-10-16
> **Completed By:** Claude (executor subagent) | closed by close-projex subagent
> **Source Plan:** 2610162003-ide-plugin-rubric-refresh-plan.md
> **Parent:** 2610162003-ide-plugin-rubric-refresh-plan.md
> **Duration:** ~25 min (20:16-20:41 per execution log timestamps)
> **Result:** Success

---

## Summary

IDE-plugin rubric rewired to the registry the editor actually installs from and plugged into the shared §4.6 floor. `references/criteria/ide-plugin.md` 6,203 → 13,183 B (8 replacements: trust table, VS Code capability rows incl. AI contribution points, JetBrains AI-key row, scoring, tiers, `## CVE Scope (§4.3)`, `## Version & Update Integrity (§4.6)` V1-V5). `workflows/ide-plugin.md` 15,760 → 20,864 B (28 replacements). `references/registries.md` 4,413 → 4,664 B (Cursor row replaced by Open VSX and VS Code forks rows). All 37 Before strings matched exactly once; resulting sizes equal the plan's simulation byte-for-byte; consistency script `OK 13183 20864 4664`.

---

## Objectives Completion

| Objective | Status | Notes |
|-----------|--------|-------|
| F1 / A1 §4.6 plug-in; Tier 1 version check | Complete | Addendum V1-V5 (1h), Tier 1 bullet "§4.6 raises nothing" (1g); workflow version-integrity research and coverage row (2r, 2t) |
| F3 / A4 registry-aware trust; Open VSX semantics; dependency review at every tier | Complete | Fork row, `namespace mismatch` HIGH / Impersonation; install-registry rule; `extensionPack` / `extensionDependencies` scoring; registries rows |
| F4 / A3 identity-only badge framing | Complete | Marketplace Verified / JetBrains verified vendor = identity credit, moderate; stale "equivalent to AMO Recommended / CWS Featured" removed |
| F6 / A6 AI surface | Complete | `languageModelTools`, `mcpServerDefinitionProviders`, chat contributions; AI-key plugins; cross-link to `workflows/agent-extension.md` 8a |
| F7 / A7 enforceable controls | Complete | V5 (`extensions.autoUpdateDelay`, `extensions.allowed`, update controls); CONDITIONAL rewrites replace "monitor for" |
| F8 / A8 stale mechanics | Complete | `postInstall` and "rarely have formal CVEs" removed; `onStartupFinished` always-on; obfuscation check; packer wording |
| C6 CVE scope | Complete | `## CVE Scope (§4.3)`: bundled server is own code; points to `SKILL.md` "Blocking CVE" |
| A9 canonical coverage rows | Complete | Typosquat / impersonation, License compatibility, Version integrity (§4.6) Required; Extension dependency review Required if present |

---

## Execution Detail

> Derived from `git log`/`git diff` of `dea5ef3..projex/2610162003-ide-plugin-rubric-refresh` (start commit) and the execution log.

### Preflight

**Planned:** floor greps, B1-B3 assumption checks, harness and size baseline.
**Actual:** `## 4.6 … (shared floor)` 1; `### V1`-`### V5` 5; 6 `**Addendum:**` lines; `Blocking CVE` 1; 8a still defined in `workflows/agent-extension.md`; Cursor row 1; target files unchanged since planning commit. `validate` 41 evals / 248 assertions; unittest evals 12 OK; tests 19 OK (6 skipped). Baselines 6,203 / 15,760 / 4,413 B.
**Deviation:** None.

### Step 1: Addendum `references/criteria/ide-plugin.md`

**Planned:** 8 replacements 1a-1h.
**Actual:** applied with Edit in order; each Before matched once. Headings once each; V1-V5 bullets 5; stale phrases 0; 13,183 B (budget 13,400; simulation exact). Commit `78f06d1`.
**Deviation:** None.

### Step 2: Workflow `workflows/ide-plugin.md`

**Planned:** 28 replacements 2a-2ab.
**Actual:** applied in plan order; `| Version integrity (§4.6) | Required | Required | Required |` 1; `Resolve the install registry` 1; `rarely have formal cves`, `` `postinstall` ``, `monitor for` 0; non-table lines > 80 bytes 0; 20,864 B (budget 21,100; simulation exact). Commit `2a689d3`.
**Deviation:** None.

### Step 3: `references/registries.md`

**Planned:** replace the Cursor line with Open VSX and VS Code forks rows (3a).
**Actual:** +2/-1 inside `### IDE / Editor Plugins` only; 4,664 B. Anchor had not moved. Commit `c879e5f`; completion commit `0528bb0`.
**Deviation:** None.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `references/criteria/ide-plugin.md` | Modified | Yes | 14 hunks, lines 4-224; 117 insertions / 19 deletions in Step 1 diff; new `## CVE Scope (§4.3)` and `## Version & Update Integrity (§4.6)` at the tail (~lines 176-224) |
| `workflows/ide-plugin.md` | Modified | Yes | 35 hunks, lines 3-429; +130/-50; research questions, install-registry rule, coverage table, 4.1/4.4/4.5 rubric text, CONDITIONAL rewrites |
| `references/registries.md` | Modified | Yes | Line 72: Cursor row → Open VSX row + VS Code forks row |

---

## Complete Change Log

> **Derived from:** `git diff --stat dea5ef3..projex/2610162003-ide-plugin-rubric-refresh`

### Files Created
| File | Purpose | Lines | In Plan? |
|------|---------|-------|----------|
| `.projex/2610162003-ide-plugin-rubric-refresh-log.md` | Execution log | 95 | Yes (implicit) |
| `.projex/closed/2610162003-ide-plugin-rubric-refresh-walkthrough.md` | This walkthrough | - | Yes (close) |

### Files Modified
| File | Changes | Lines Affected | In Plan? |
|------|---------|----------------|----------|
| `references/criteria/ide-plugin.md` | Rubric refresh + two plug-ins | 136 changed; 13,183 B | Yes |
| `workflows/ide-plugin.md` | 28 replacements | 180 changed; 20,864 B | Yes |
| `references/registries.md` | Cursor row → 2 rows | +2/-1 | Yes |
| `.projex/2610162003-ide-plugin-rubric-refresh-plan.md` | Status Complete, Log, Walkthrough link | 3 lines | Yes (close) |

### Files Deleted
None.

### Planned But Not Changed
None. `SKILL.md`, `references/criteria.md`, `references/classifier.md`, `evals/`, `STEWARDSHIP.md` untouched, as scoped.

---

## Success Criteria Verification

| Criterion | Method | Result | Evidence |
|-----------|--------|--------|----------|
| One §4.6 heading with V1-V5 bullets; one CVE Scope heading | grep + consistency script | Pass | 1 / 5 / 1 |
| `§4.6 V<n>` references resolve against landed `references/criteria.md` | consistency script | Pass | `OK` |
| Stale phrases absent | consistency script | Pass | 0 hits |
| `registries.md`: Cursor line gone, two new rows, nothing else changed | `git diff --numstat` | Pass | +2/-1 |
| Coverage table rows (Version integrity, Typosquat, License; Dependency review Required if present) | grep | Pass | present |
| Byte budgets | `wc -c` | Pass | 13,183 ≤ 13,400; 20,864 ≤ 21,100 |
| Non-table workflow lines ≤ 80 columns | awk | Pass | 0 over |
| `validate` + unittest with Preflight count | harness | Pass | 41 / 248; evals 12 OK; tests 19 OK (6 skipped) |
| Paper traces | manual walk | Pass | I1-I11 all match (criterion text says I1-I10; the table has 11 and all were traced) |
| `git diff --stat` lists exactly 3 files | diff | Pass | 3 shipped files + log |

**Overall:** 10/10 criteria passed.

---

## Deviations from Plan

None. Verify-Projex was Encouraged and not dispatched; each step was self-verified, with byte-exact size equality to the plan's simulation as strong evidence of verbatim application.

---

## Issues Encountered

### Issue 1: Concurrent agents' files on the main checkout
- **Description:** Precheck WARN for uncommitted planning files of other agents.
- **Severity:** Low
- **Resolution:** Left untouched; explicit-path commits only.

### Issue 2: Base advanced during execution
- **Description:** Other agents' plan and close commits landed on base.
- **Severity:** Low
- **Resolution:** None touched these three files at execution time. At close, `references/registries.md` and the other subject files merged cleanly; only the roadmap nav conflicted (add/add), resolved keeping both sides.

### Close notes
- Nav `2604070218-install-auditor-subject-typed-redesign-nav.md` updated in the close commit, following earlier rubric-refresh closes (plan carries no `Nav:` field).
- The ci-action plan (still executing at close time) edits the CI block of `references/registries.md`; this plan edited only the IDE table rows. No overlap.

---

## Key Insights

**Rationale promoted:** none needed. Rationale ships in the addendum and workflow text; no shipped file carries projex references (grep clean).

### Lessons Learned

1. **Credit the registry the editor installs from**
   - Context: Cursor, Windsurf, VSCodium install from Open VSX, where Marketplace "Verified" does not apply.
   - Insight: Identity credit, install-count thresholds and namespace checks must all be evaluated on the install registry; `namespace mismatch` is HIGH.
   - Application: other rubrics with forked ecosystems should state the install-registry rule explicitly.

### Gotchas / Pitfalls

1. **Trusted publisher, hijacked version**
   - Trap: a verified publisher's single bad release (Nx Console 18.95.0, CVE-2026-48027) passes publisher-level trust.
   - Avoidance: V1 age, V3 upstream-tag continuity and V5 update controls (`extensions.autoUpdateDelay` ≥ 72; the 2 h default exempts trusted publishers).

2. **Dependency packs after review**
   - Trap: `extensionPack` / `extensionDependencies` pull payloads after review (GlassWorm).
   - Avoidance: dependency review at every tier; a failing pack member is HIGH.

---

## Recommendations

### Immediate Follow-ups
- [ ] `references/registries.md` JetBrains row ("Medium-High (JetBrains review process)") is arguably optimistic; revisit in the orchestrator consistency patch (the addendum wins for ide-plugin audits meanwhile).
- [ ] `references/classifier.md` still lists `packer spec` as an ide-plugin signal (and `vim.pack.add()` is the newer Neovim form); harmless for routing, harmonise in the consistency patch.
- [ ] Harmonise the §4.3 plug-in heading across addenda (`## CVE Scope (§4.3)` here).
- [ ] STEWARDSHIP: ide-plugin Last Reviewed 2026-10-16, Next Due 2027-02-13.
- [ ] Eval refresh plan: ide-plugin hand-off cases (plan Notes → Eval Hand-off).

### Future Considerations
- F9 coverage gaps deferred: Zed (WASM-sandboxed extensions), Emacs MELPA, Visual Studio and Eclipse marketplaces.
- Plan text says "traces I1-I10" while the table has I1-I11; fix the criterion wording if the plan is reused.

### Plan Improvements
- State the trace count once; keep simulated sizes (they made verbatim application checkable).

---

## Related Projex Updates

### Documents to Update
| Document | Update Needed |
|----------|---------------|
| `2610162003-ide-plugin-rubric-refresh-plan.md` | Status Complete; Walkthrough link; moved to closed |
| `2610162003-ide-plugin-rubric-refresh-log.md` | Moved to closed |
| `2604070218-install-auditor-subject-typed-redesign-nav.md` | Recent Progress, checklist, Revision Log, Last Revised |
| `2610161927-browser-extension-ide-plugin-stewardship-review-eval.md` | Left active (source eval of both plans; its remaining findings are the eval-refresh and follow-up items) |

### New Projex Suggested
| Type | Description |
|------|-------------|
| Plan | Eval refresh for ide-plugin cases |
| Patch/Revise | Orchestrator consistency patch (JetBrains row, classifier `packer` signal, §4.3 / §4.x heading harmonisation) |

---

## Appendix

### References
- Execution commits: `78f06d1` (step 1), `2a689d3` (step 2), `c879e5f` (step 3), `0528bb0` (complete)
- Execution log: `2610162003-ide-plugin-rubric-refresh-log.md`
