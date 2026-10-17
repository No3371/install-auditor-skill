# Walkthrough: Runtime Cross-Plan Consistency Pass

> **Execution Date:** 2026-10-17
> **Completed By:** Claude (executor subagent; close by projex close subagent)
> **Source Plan:** 2610170500-runtime-cross-plan-consistency-plan.md
> **Parent:** 2610170500-runtime-cross-plan-consistency-plan.md
> **Duration:** ~45 min (05:10 → 05:55 execution; close afterwards)
> **Result:** Success — one live-verification gap (Scorecard response shape, see Deviations)

---

## Summary

Reconciled the skill's runtime files after the ten subject rubric refreshes. 19 shipped files edited (SKILL.md, references, workflows, 2 lookup scripts, STEWARDSHIP.md); no rating semantics changed, `evals/` untouched. All 12 plan success criteria pass on offline evidence. The Scorecard host change (`api.scorecard.dev`) is applied, but the live JSON shape is **unverified**: the session egress proxy returned 403 for both Scorecard hosts.

---

## Objectives Completion

| Objective (plan Success Criteria) | Status | Notes |
|---|---|---|
| One `## CVE Scope (§4.3)` heading in 7 addenda; no `Own Code vs Third-Party` | Complete | cli-binary renamed; counts 7 × 1, 0 old-name hits |
| No `4.6` heading clash; no `### §` in workflows | Complete | 4 Alternatives headings renamed, 6 cli-binary `### §4.n` → `### 4.n` |
| Classifier: tap row, bare-cask row; no `build-from-source` / `volta`; `vim.pack.add()` | Complete | Cell counts 5×2, 22×3, 12×4 as planned |
| `SKILL.md` ≤ 15,500 B; `Mutable tag-pinned actions`; `(not a cask)` | Complete | 15,488 B (base 15,482) |
| `registries.md`: JetBrains, hardened + frozen rows, Go fix | Complete | `dhi.io`, `bitnamilegacy`, `remove the setting` present; `Medium-High (JetBrains` 0 |
| Browser MV2 carve-out ×3 | Complete | Tier 1, Tier 3, workflow APPROVED bullet; MV2 counts 15 → 17 and 11 → 12 |
| Container `GCR,` 0; `runAsUser: 0` not Medium | Complete | Follows root-at-runtime rule |
| cli-binary `Tier 2 minimum` 0; no-fix bullet; shared §4.3 default mitigations | Complete | |
| remote-integration `**Scope:**` note → agent-extension 8a | Complete | Plus Identify-row note |
| 0 × `securityscorecards` | Complete (code) / Unverified (live) | 5 occurrences replaced; live shape not confirmed |
| STEWARDSHIP `### Watch List`, inventory untouched | Complete | 11 rows; `## Workflow Inventory` section hash-identical |
| Offline suites unchanged vs base | Complete | validate 41 evals / 248 assertions; evals unittest 12 OK; tests 23 OK |

---

## Execution Detail

> Derived from `git log` / `git diff 01f8390..projex/2610170500-runtime-cross-plan-consistency` and the execution log. Commit SHAs are pre-squash.

### Step 1: Harmonise §4.3 plug-in and workflow section headings (`5b39fc9`)

**Planned:** Rename cli-binary plug-in heading to `CVE Scope (§4.3)`; add heading contract to `references/criteria.md` §4.3; `§4.n` → `4.n` in cli-binary workflow; drop `4.6` from four Alternatives headings.

**Actual:** As planned. `workflows/cli-binary.md` citation rewrapped shorter (two lines, ≤ 80 cols).

**Deviation:** None.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|---|---|---|---|
| `references/criteria/cli-binary.md` | Modified | Yes | L175 heading → `## CVE Scope (§4.3)` |
| `references/criteria.md` | Modified | Yes | L153 Addendum bullet names the heading, no-fix mitigations, no-plug-in default |
| `workflows/cli-binary.md` | Modified | Yes | L220/241/252/264/272/279 `### §4.n` → `### 4.n`; L260-261 citation |
| `workflows/browser-extension.md` | Modified | Yes | L314 `### Alternatives (browser-extension-specialized)` |
| `workflows/ci-action.md` | Modified | Yes | L224 `### Alternatives` |
| `workflows/ide-plugin.md` | Modified | Yes | L362 `### Alternatives (ide-plugin-specialized)` |
| `workflows/registry-package.md` | Modified | Yes | L451 `### Alternatives (registry-specialized)` |

**Verification:** `grep -c '^## CVE Scope (§4.3)$'` = 1 for 7 addenda, 0 for agent-extension / remote-integration; `grep -rn 'Own Code vs Third-Party'` empty; `grep -n '^### §' workflows/*.md` empty.

**Issues:** Plan grep `grep -nE '^### §?4\.6 '` returns nothing in the default C locale (`§?` quantifies one byte of a two-byte char); with `LC_ALL=C.UTF-8` it returns the four expected workflows.

---

### Step 2: Homebrew and Neovim routing (`5fbe1ff`)

**Planned:** Reword core row; add third-party-tap and bare-name cask rows; refresh signal rows 3/6/7; desktop-app identify row; `brew trust` note on tap-cask row.

**Actual:** As planned.

**Deviation:** None.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|---|---|---|---|
| `references/classifier.md` | Modified | Yes | L81 core row (bottle built and attested by Homebrew CI); +2 rows after cask row (tap formula → cli-binary; bare cask name → desktop-app); signal rows 3 (`vim.pack.add()`), 6 (bare-name cask), 7 (tap; `volta` → `mise`) |
| `workflows/desktop-app.md` | Modified | Yes | L42 Homebrew Cask identify row |
| `references/criteria/desktop-app.md` | Modified | Yes | L20 tap-cask note: `brew trust` (Homebrew 6.0.0+) records consent, not review |

**Verification:** `build-from-source|volta` = 0; `third-party tap` = 2; `vim.pack.add()` = 1; cell-count distribution before 5×2, 20×3, 12×4 → after 5×2, 22×3, 12×4.

---

### Step 3: SKILL.md row 7 and CI Red Flag (`c2245bd`)

**Planned:** `(not `--cask`)` → `(not a cask)`; `Tag-pinned actions` → `Mutable tag-pinned actions`; byte ceiling 15,500.

**Actual:** As planned; `SKILL.md` L51 and L182.

**Deviation:** None.

**Verification:** `wc -c SKILL.md` = 15488 (re-checked at close); both greps = 1.

---

### Step 4: `references/registries.md` rows (`0e611ff`)

**Planned:** Go fix, hardened catalogs row, frozen namespace row, JetBrains → Medium, Vim/Neovim row.

**Actual:** As planned (L29, +L44, +L52, L71-72).

**Deviation:** None.

**Verification:** `dhi.io|bitnamilegacy|remove the setting` matches 3 lines; `Medium-High (JetBrains` = 0; new rows cross-checked against `references/criteria/container-image.md` and `references/criteria/ide-plugin.md`.

---

### Step 5: Subject-file contradictions (`ce12a1a`)

**Planned:** 5a browser MV2 carve-out ×3; 5b container header + `runAsUser: 0`; 5c cli-binary Tier 3 + no-fix bullet + shared default mitigations; 5d remote-integration Scope note.

**Actual:** As planned.

**Deviation:** None.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|---|---|---|---|
| `references/criteria/browser-extension.md` | Modified | Yes | L182 Tier 1, L204 Tier 3 carve-outs |
| `workflows/browser-extension.md` | Modified | Yes | L379-380 APPROVED bullet, two wrapped lines |
| `workflows/container-image.md` | Modified | Yes | L3-4 header comment: Docker Hardened Images, Google Artifact Registry (incl. legacy `gcr.io`) |
| `references/criteria/container-image.md` | Modified | Yes | L108 Scoring-impact bullet names `runAsUser: 0`; L141 row rated by root-at-runtime rule |
| `references/criteria/cli-binary.md` | Modified | Yes | L109 `Tier 2 minimum` → Tier 3; +L182 no-fix mitigation bullet |
| `references/criteria.md` | Modified | Yes | L150 Fixed-release bullet: default mitigation set |
| `workflows/remote-integration.md` | Modified | Yes | +L26-32 `**Scope:**` paragraph; L51 Identify row |

**Verification:** MV2 counts 15 → 17 / 11 → 12; `GCR,` = 0; `runAsUser: 0` row no longer `Medium`; `Tier 2 minimum` = 0; `no fixed release (not KEV)` = 1; `default when neither names any` = 1; `^\*\*Scope:\*\*` in remote-integration = 1; remote-integration `## §` headings unchanged vs base. Paper traces: cli T14 → Tier 3, same verdict; container T12 production root → HIGH → CONDITIONAL, dev root → LOW note.

---

### Step 6: OpenSSF Scorecard API host (`2442914`)

**Planned:** `api.securityscorecards.dev` → `api.scorecard.dev` in 5 places; one live GET if network allows.

**Actual:** All 5 replaced. Live probe attempted through the repo's own `http_json` (curl / WebFetch / inline HTTP are blocked by project routing rules): both Scorecard hosts returned `URLError: Tunnel connection failed: 403 Forbidden` from the session egress proxy; control `registry.npmjs.org` succeeded. Not retried, not worked around.

**Deviation:** Live response shape **unverified** (plan fallback "record unverified live and proceed" applied).

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|---|---|---|---|
| `references/criteria.md` | Modified | Yes | L48 table row, L317 |
| `workflows/registry-package.md` | Modified | Yes | L276 (rewrap unchanged) |
| `scripts/registry-lookup.py` | Modified | Yes | L341 `lookup_openssf` URL |
| `scripts/registry-lookup.ps1` | Modified | Yes | L353 `Lookup-OpenSSF` URL |

**Verification:** `grep -rn 'securityscorecards' SKILL.md references workflows scripts` = 0; `unittest discover -s tests` = 23 OK (tests route non-registry hosts to a failing stub, so the change is test-neutral).

---

### Step 7: STEWARDSHIP watch list (`d436192`)

**Planned:** `### Watch List` section (11 rows) + checklist step 3 pointer; inventory untouched.

**Actual:** As planned (+18 lines at L38-55; step 3 line edited).

**Deviation:** None.

**Verification:** `^### Watch List` = 1; 11 data rows; `## Workflow Inventory` section hash identical before/after.

---

### Completion (`e995595`)

Plan status set `Complete`, execution log finalized. Full verification sweep recorded in the log. At close, `SKILL.md` size, the Scorecard grep, `evals/run_evals.py validate` and the evals unittest were re-run in the worktree; the `tests` suite re-ran 23 OK with 8 skipped (pwsh not on PATH in the close environment; execution run had pwsh 7.4.6 and 0 skipped).

---

## Complete Change Log

> **Derived from:** `git diff --stat 01f8390..projex/2610170500-runtime-cross-plan-consistency` (21 files, +154 / −41, includes the plan status edit and the execution log). Close commit adds the projex moves, walkthrough and nav update. The two-dot diff against the current base tip (`28ad836`) also lists `.projex/2610170504-eval-suite-refresh-plan.md` as deleted: the base gained that file after execution started; the squash is computed against the merge base and does not touch it.

### Files Created
| File | Purpose | Lines | In Plan? |
|---|---|---|---|
| `.projex/closed/2610170500-runtime-cross-plan-consistency-log.md` | Execution log | 80 | Yes (process) |
| `.projex/closed/2610170500-runtime-cross-plan-consistency-walkthrough.md` | This record | — | Yes (process) |

### Files Modified
| File | Changes | Lines Affected | In Plan? |
|---|---|---|---|
| `SKILL.md` | Row 7; Red Flag | 51, 182 | Yes |
| `STEWARDSHIP.md` | Watch List; step 3 | 38-55, 64 | Yes |
| `references/classifier.md` | Core row; +2 routing rows; signal rows 3/6/7 | 81-83, 97-101 | Yes |
| `references/criteria.md` | §4.3 contract + mitigations; Scorecard ×2 | 48, 150, 153, 317 | Yes |
| `references/criteria/browser-extension.md` | MV2 carve-outs | 182, 204 | Yes |
| `references/criteria/cli-binary.md` | Heading; Tier 3; no-fix bullet | 109, 175, 182 | Yes |
| `references/criteria/container-image.md` | `runAsUser: 0` | 108, 141 | Yes |
| `references/criteria/desktop-app.md` | `brew trust` note | 20 | Yes |
| `references/registries.md` | Go, container ×2, JetBrains, Vim | 29, 44, 52, 71-72 | Yes |
| `scripts/registry-lookup.py` / `.ps1` | Scorecard host | 341 / 353 | Yes |
| `workflows/browser-extension.md` | Heading; APPROVED carve-out | 314, 379-380 | Yes |
| `workflows/ci-action.md` | Heading | 224 | Yes |
| `workflows/cli-binary.md` | 6 headings; §4.3 citation | 220-279 | Yes |
| `workflows/container-image.md` | Header comment | 3-4 | Yes |
| `workflows/desktop-app.md` | Cask identify row | 42 | Yes |
| `workflows/ide-plugin.md` | Heading | 362 | Yes |
| `workflows/registry-package.md` | Scorecard; heading | 276, 451 | Yes |
| `workflows/remote-integration.md` | Scope note; Identify row | 26-32, 51 | Yes |
| `.projex/2604070218-install-auditor-subject-typed-redesign-nav.md` | Revision header, Recent Progress, Revision Log row | — | Yes (orchestrator instruction) |

### Files Deleted
None.

### Planned But Not Changed
None. `evals/**` and STEWARDSHIP inventory dates were out of scope by design.

---

## Success Criteria Verification

All 12 criteria verified by command output recorded in the execution log (Completion entry) and re-checked at close where noted.

| Criterion | Method | Result | Evidence |
|---|---|---|---|
| `CVE Scope (§4.3)` ×7; 0 old-name | grep per addendum | Pass | Log Step 1 |
| `4.6` headings only in 4 workflows; 0 `### §` | grep (UTF-8 locale) | Pass | Log Step 1 |
| Classifier rows / greps | grep + cell-count script | Pass | Log Step 2 |
| `SKILL.md` ≤ 15,500 B, two phrases | `wc -c`, grep | Pass | 15488 (re-run at close) |
| registries rows | grep | Pass | Log Step 4 |
| Browser MV2 carve-outs ×3 | grep -c MV2 | Pass | 15 → 17, 11 → 12 |
| Container `GCR,` / `runAsUser: 0` | grep | Pass | Log Step 5 |
| cli-binary Tier 3 / bullets / shared default | grep | Pass | Log Step 5 |
| remote-integration Scope note | grep | Pass | Log Step 5 |
| 0 × `securityscorecards` | grep | Pass | 0 (re-run at close) |
| Watch List; inventory untouched | grep + section hash | Pass | Log Step 7 |
| Three offline suites unchanged | validate / unittest | Pass | validate 41 evals, 248 assertions; evals 12 OK (re-run at close); tests 23 OK at execution |

**Overall:** 12/12 passed. Live Scorecard response shape is an unverified Assumption, not a criterion (see Deviations).

---

## Deviations from Plan

### Deviation 1: Scorecard live response shape unverified
- **Planned:** One GET of `https://api.scorecard.dev/projects/github.com/ossf/scorecard`; "unverified live" accepted if blocked.
- **Actual:** Session egress proxy returned `403 Forbidden` on both `api.scorecard.dev` and `api.securityscorecards.dev`; the host change shipped on primary-source evidence only (ossf/scorecard README, 2024 governance notes).
- **Reason:** Policy denial by the proxy; not retried or bypassed.
- **Impact:** If the new host's JSON differs from `score`, `date`, `checks[].name/score`, `lookup_openssf` / `Lookup-OpenSSF` return degraded data. The scripts tolerate missing fields (`data.get(...)`), so failure mode is a missing Scorecard row, not a crash.
- **Recommendation:** One human GET with open network. If the shape differs, revert only the two `scripts/registry-lookup.*` edits and keep the doc edits.

### Deviation 2: Verify-Projex / Do-Projex not dispatched
- **Planned:** Both marked "Encouraged" on several steps.
- **Actual:** Executed and verified directly with diff and grep evidence; no sub-subagent spawned.
- **Impact:** None on outcome; independent re-verification was by the same executor plus the close re-run.

### Deviation 3: Plan grep needs a UTF-8 locale
- **Planned:** `grep -nE '^### §?4\.6 ' workflows/*.md`.
- **Actual:** Matches only with `LC_ALL=C.UTF-8`. No edit change.

### Deviation 4 (process): base advanced during execution
- **Actual:** Base moved `01f8390` → `28ad836` (`projex: add plan - eval-suite-refresh`) between execution start and close. The commit adds only `.projex/2610170504-eval-suite-refresh-plan.md`; no file overlap with this execution. Squash is by merge base.

---

## Issues Encountered

### Issue 1: Scorecard hosts denied by egress proxy
- **Description:** See Deviation 1.
- **Severity:** Low (documented fallback).
- **Resolution:** Recorded; follow-up queued below.
- **Time Impact:** Minimal.
- **Prevention:** Planner could pre-verify a live shape from a networked session before queuing a host change.

### Issue 2: Close environment lacks pwsh
- **Description:** `tests` suite at close skipped 8 pwsh-twin tests.
- **Severity:** Low. Execution-time run had pwsh 7.4.6 and 0 skipped (23 OK).
- **Resolution:** Execution-time result used as the authoritative pwsh evidence.

---

## Key Insights

**Rationale promoted:** none needed — all edits are to shipped docs; no source-comment rationale lived only in projex documents.

### Lessons Learned

1. **Reconciliation plans work best as exact-string edits**
   - Context: 42 edits across 19 files, each restating a rule another file already stated.
   - Insight: asserting "old string occurs once" per edit made the pass mechanical and verification grep-able.
   - Application: reuse for future post-refresh consistency passes.

2. **Gate network-dependent assumptions early**
   - Context: Scorecard shape check blocked by proxy.
   - Insight: a planning-time assumption that needs the network will be unverifiable in a sandboxed executor.
   - Application: list such checks as human follow-ups in the plan, not executor steps.

### Pattern Discoveries

1. **Heading contracts mirrored across sections**
   - Observed in: `references/criteria.md` §4.3 now mirrors the §4.6 heading-name contract.
   - Reuse potential: any shared section with per-addendum plug-ins.

### Gotchas / Pitfalls

1. **Multibyte `?` in grep -E under the C locale**
   - Trap: `§?` matches one byte of a two-byte char.
   - Avoidance: `LC_ALL=C.UTF-8` for greps over `§`.

### Technical Insights

- `SKILL.md` has 12 B of headroom under its 15,500 B ceiling; any further dispatcher edit needs a byte budget first.
- Plan-step commits per step made the squash history reviewable; the squash message preserves them.

---

## Recommendations

### Immediate Follow-ups
- [ ] One human GET of `https://api.scorecard.dev/projects/github.com/ossf/scorecard` confirming `score`, `date`, `checks[].name/score`; else revert only `scripts/registry-lookup.py` and `.ps1` host edits.
- [ ] Eval refresh (plan `2610170504-eval-suite-refresh-plan.md`, Ready) should take the plan's eval hand-offs: tap and bare-cask routing cases, Tier 3 depth for known-vendor `curl | sh` / `irm | iex`, eval 20 wording ("bottle built and attested by Homebrew CI").
- [ ] Orchestrator: STEWARDSHIP inventory Last Reviewed / Next Due dates (out of this plan's scope).

### Future Considerations
- Name a flag level for "strong negative" signals (browser T10 sideloaded; cli-binary T3 shared copy) at the next subject review (rejected here as a new rating).
- Nav Phase 6 remains continuous; no closure candidate.

### Plan Improvements
- Use a UTF-8-safe grep form in plan verification commands.
- Mark network-dependent verifications as human follow-ups.

---

## Related Projex Updates

### Documents to Update
| Document | Update Needed |
|---|---|
| `2610170500-runtime-cross-plan-consistency-plan.md` | Marked Complete; walkthrough + log linked; moved to `closed/` |
| `2610170500-runtime-cross-plan-consistency-log.md` | Status Complete; moved to `closed/` |
| `2604070218-install-auditor-subject-typed-redesign-nav.md` | Updated in place: Recent Progress, Revision Log, Last Revised (not closed) |

### New Projex Suggested
| Type | Description |
|---|---|
| Patch | Revert Scorecard script edits only, if the human GET shows a shape mismatch |

---

## Appendix

### References
- Execution log: `2610170500-runtime-cross-plan-consistency-log.md`
- Execution commits (squashed at close): `5b39fc9` step 1, `5fbe1ff` step 2, `c2245bd` step 3, `0e611ff` step 4, `ce12a1a` step 5, `2442914` step 6, `d436192` step 7, `e995595` complete
- Base at execution start: `01f8390`; base at close: `28ad836`
