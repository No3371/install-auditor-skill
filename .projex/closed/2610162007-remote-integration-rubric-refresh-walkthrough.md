# Walkthrough: Remote-Integration Rubric Refresh

> **Execution Date:** 2026-10-16
> **Completed By:** Claude (executor subagent) | closed by close-projex subagent
> **Source Plan:** 2610162007-remote-integration-rubric-refresh-plan.md
> **Parent:** 2610162007-remote-integration-rubric-refresh-plan.md
> **Duration:** ~11 min (20:11–20:22 per execution log timestamps)
> **Result:** Success (one verification caveat: several `[verify]` assumptions only partly verified — see Issues)

---

## Summary

Both Type 9 files fully rewritten on the landed §4.6 shared floor. `references/criteria/remote-integration.md` 5,419 → 19,860 B (provider-neutral scope classes, non-OAuth credentials, OAuth flow hygiene, custody and consent path, webhooks, AI-use rows, §4.6 plug-in, §4.3 CVE note). `workflows/remote-integration.md` 10,323 → 13,774 B (Tier Triage, 11 numbered checks, coverage table with all 11 canonical Required rows, rubric renumbered 4.1–4.6). Both files byte-identical to plan content (sha256 match); no shipped sentence needed an assumption-driven edit.

---

## Objectives Completion

| Objective | Status | Notes |
|-----------|--------|-------|
| RI-1 Tier Triage + coverage rows | Complete | Workflow "Evidence — Part A: Tier Triage"; "Audit coverage tracking" carries 11 canonical Required rows + subject rows |
| RI-2 Scope table correctness + provider maps | Complete | Addendum §1: Low / Elevated / High classes, standing-grant modifier, GitHub/Google/Microsoft/Slack maps; stale literals gone |
| RI-3 Token custody + consent path | Complete | Addendum §6 |
| RI-4 RFC 9700 anchoring | Complete | Addendum §3; loopback / private-use callbacks no longer flagged (RFC 8252) |
| RI-5 API key / SA key scoring | Complete | Addendum §2 |
| RI-6 Webhook norms | Complete | Addendum §9 |
| RI-7 AI data use + connector drift | Complete | Addendum §5 + `## Version & Update Integrity (§4.6)` plug-in (V1–V5 bullets) |
| RI-9 Stale names / verification signals | Complete | Addendum §7; workflow uses "Slack Marketplace" |
| RI-10 GDPR transfer row | Complete | Addendum §4 |
| Heading collision with shared §4.6 | Complete | Workflow rubric renumbered 4.1 Provenance … 4.6 Version & Update Integrity |
| C6 CVE row | Complete | Addendum §8; hosted → `N/A (hosted service, no versioned artifact)`; verdict classes untouched |

---

## Execution Detail

> Derived from git history (`5f93c73..projex/2610162007-remote-integration-rubric-refresh`) and the execution log.

### Preflight

**Planned:** floor greps, blob hashes, harness baseline.
**Actual:** floor commit `20843cc` reachable; all greps as expected (4.6 heading 1, `### V[1-5]` 5, Hosted services 1, coverage tables 1, Version integrity row 1, Blocking CVE 1). Blobs `5e062e5b…` (workflow) and `ef950a95…` (addendum) matched. `run_evals.py validate`: 41 evals, 248 assertions. unittest evals: 12 OK; tests: 19 OK (skipped=6).
**Deviation:** None.

### Assumption re-check

**Planned:** re-check `[verify]` items (A1, A2, A8, A10) if network allows.
**Actual:** WebSearch summaries only. A1 verified except no-read-only-private-repo-scope and `sudo`/`admin:*` non-existence (prior knowledge kept). A2 partly (`gmail.readonly`, `drive.readonly` restricted; full `drive` from prior knowledge). A8 partly (Entra verified-publisher consent and admin consent workflow; Google Workspace, Slack, GitHub org, Salesforce controls unchecked). A10 verified for Slack scope names; Graph `User.Read` not directly confirmed. A3–A7, A9, A11 not re-checked online (A11 by paper trace).
**Deviation:** None; no shipped sentence edited.

### Step 1: Rewrite `references/criteria/remote-integration.md`

**Planned:** whole-file replacement with the plan block (§1–§10 + §4.6 plug-in).
**Actual:** block extracted by `sed` (no retyping); 19,860 B, 362 lines, 10 `## §N — ` headings, sha256 `2206909f…af04a` matches. Commit `eef9f2b`.
**Deviation:** None.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `references/criteria/remote-integration.md` | Modified | Yes | Full rewrite, 91 → 362 lines |

**Verification:** `wc -c`, heading counts, stale-literal grep (0), sha256.

### Step 2: Rewrite `workflows/remote-integration.md`

**Planned:** whole-file replacement with the plan block.
**Actual:** block extracted by `sed`; 13,774 B, 267 lines, one Tier Triage heading, six `### 4.N` headings, sha256 `71cda01a…a9f8` matches. Commit `4321e5b`.
**Deviation:** None.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `workflows/remote-integration.md` | Modified | Yes | Full rewrite, 173 → 267 lines |

**Verification:** consistency script `OK 13774 19860 canonical required rows: 11`; validate; both unittest suites equal Preflight.

### Completion

**Actual:** paper traces P1–P10 walked, plan status → Complete, `Log:` header added, execution log committed (`a09e11a`).

---

## Complete Change Log

> **Derived from:** `git diff --stat 5f93c73..projex/2610162007-remote-integration-rubric-refresh` — authoritative record.

### Files Created
| File | Purpose | Lines | In Plan? |
|------|---------|-------|----------|
| `.projex/2610162007-remote-integration-rubric-refresh-log.md` | Execution log | 97 | Yes (required by execute workflow) |

### Files Modified
| File | Changes | Lines Affected | In Plan? |
|------|---------|----------------|----------|
| `references/criteria/remote-integration.md` | Full rewrite | +381 / − (net 91 → 362 lines) | Yes |
| `workflows/remote-integration.md` | Full rewrite | +336 / − (net 173 → 267 lines) | Yes |
| `.projex/2610162007-remote-integration-rubric-refresh-plan.md` | Status → Complete; `Log:` header | 3 | Yes (lifecycle) |

### Files Deleted
None.

### Planned But Not Changed
None. `evals/`, `SKILL.md`, `references/criteria.md`, `references/classifier.md` untouched, as planned.

---

## Success Criteria Verification

### Criterion 1: Addendum byte-for-byte (19,860 B, sha256 `2206909f…`)
**Verification Method:** `wc -c`, `sha256sum` (re-run at close).
**Evidence:** `19860 references/criteria/remote-integration.md`; `2206909f4a74566be652e2234ce9b3b0c002e9ddd1a045c7aed96236f99af04a`.
**Result:** PASS

### Criterion 2: Workflow matches (13,774 B, sha256 `71cda01a…`)
**Evidence:** `13774 workflows/remote-integration.md`; `71cda01a5f801bc395dea7eadba21fd1934e9fe8686d3e22855c68591034a9f8`.
**Result:** PASS

### Criterion 3: Consistency script prints `OK`
**Evidence:** `OK 13774 19860 canonical required rows: 11` (re-run at close).
**Result:** PASS

### Criterion 4: Harness green, test counts equal Preflight
**Evidence:** `41 evals, 248 assertions (82 deterministic, 166 model-graded)`; evals `Ran 12 tests … OK`; tests `Ran 19 tests … OK (skipped=6)` (re-run at close).
**Result:** PASS

### Criterion 5: Paper traces P1–P10 reach stated verdict/tier
**Evidence:** log "Paper traces P1-P10": P1 APPROVED Tier 1; P2 REJECTED Tier 3; P3 CONDITIONAL Tier 2; P4 REJECTED; P5 CONDITIONAL; P6 CONDITIONAL; P7 APPROVED with MEDIUM noted (unresolved → REJECTED); P8 CONDITIONAL; P9 no flag; P10 REJECTED.
**Result:** PASS

### Criterion 6: Diff lists exactly the 2 shipped files; protected files untouched
**Evidence:** `git diff --stat 5f93c73..branch` → addendum, workflow, plus projex log/plan only; no `evals/`, `SKILL.md`, `references/criteria.md`, `references/classifier.md`.
**Result:** PASS

### Acceptance Criteria Summary

| Criterion | Method | Result | Evidence |
|-----------|--------|--------|----------|
| Addendum matches | wc + sha256 | Pass | above |
| Workflow matches | wc + sha256 | Pass | above |
| Consistency script | python3 | Pass | `OK … 11` |
| Harness green | validate + unittest | Pass | 12 / 19 (skipped 6) |
| Paper traces | manual | Pass | P1–P10 |
| Only 2 shipped files | git diff --stat | Pass | above |

**Overall:** 6/6 criteria passed.

---

## Deviations from Plan

None. Content byte-identical to plan blocks; no Assumption-driven edits.

---

## Issues Encountered

### Issue 1: `[verify]` assumptions only partly verified
- **Description:** Network re-check limited to WebSearch summaries (WebFetch blocked by project routing; `ctx_*` tools unavailable to executor). Unchecked: official Standard Webhooks spec, RFC pages, GCP and Salesforce docs, Google Workspace / Slack / GitHub org consent controls, Graph `User.Read`; no-read-only-private-repo scope, full `drive` restricted status held from prior knowledge.
- **Severity:** Low (maps are labeled examples; unknown scope defaults to High; wrong example name is a one-line revise)
- **Resolution:** Shipped text unchanged; gaps listed in log. A1, A2, A8, A10 remain candidates for a later verification pass.
- **Time Impact:** None
- **Prevention:** Give executors a fetch-capable tool, or accept search-summary verification up front.

### Issue 2: Start-commit trailers
- **Description:** Base start commit first created without trailers; amended (`3a1f684` → `5f93c73`) while still unpushed HEAD.
- **Severity:** Low
- **Resolution:** Amended pre-push, no downstream impact.

### Issue 3: Precheck WARN
- **Description:** `execute-precheck` warned about uncommitted changes in the main checkout (sibling planners' untracked plan files).
- **Severity:** Low
- **Resolution:** Ignored by design; worktree mode left the main checkout untouched.

---

## Key Insights

**Rationale promoted:** none needed (spec-only change; rationale lives in the shipped addendum text itself).

### Lessons Learned

1. **Embedding full file content in the plan makes execution mechanical**
   - Context: both steps were `sed` extractions with hash checks.
   - Insight: byte-identical hashes remove drift risk and make review trivial.
   - Application: keep for prose-only rewrites; costs a >1000-line plan.

2. **Paper traces double as eval-preservation proof**
   - Context: P1–P3 mirror evals 24 / 25 / 32.
   - Insight: expected verdicts survive a large rubric change without a live paid eval run.
   - Application: reuse for sibling refreshes.

### Pattern Discoveries

1. **Provider-neutral class plus example maps**
   - Observed in: addendum §1.
   - Description: rules live in Low / Elevated / High classes; provider scope names are labeled examples.
   - Reuse potential: other credential-grant rubrics.

### Gotchas / Pitfalls

1. **Heading collisions with shared criteria numbering**
   - Trap: addendum/workflow `§4.6` meant a different thing than shared `references/criteria.md` §4.6.
   - How encountered: found at planning.
   - Avoidance: align per-type rubric numbering with the shared 4.1–4.6.

### Technical Insights

- Pure Python repo; no bootstrap needed in worktree. Test runs create ignored `__pycache__/` dirs that must be removed before close.

---

## Recommendations

### Immediate Follow-ups
- [ ] Eval refresh plan: add Type 9 cases per plan Hand-off (device-code vishing → REJECTED; GCP SA key → CONDITIONAL; AI connector with LLM sub-processor + `offline_access` → CONDITIONAL; unresolved token-custody incident → REJECTED; unsigned inbound webhook → CONDITIONAL); update eval 24 wording "Slack App Directory" → "Slack Marketplace"; note eval 32 `repo` is read and write.
- [ ] Orchestrator: STEWARDSHIP Type 9 row (Last Reviewed 2026-10-16; watch list OAuth 2.1 RFC status, MCP authorization spec, Slack/Google API-terms changes, CASA program).
- [ ] RI-8 routing for hosted MCP connectors lives in the generic/classifier sibling plan; do not edit Type 9 files there.

### Future Considerations
- Addendum is 19.9 KB (~5k tokens per Type 9 audit); if trimming is wanted, cut the provider maps first.
- One live eval run after all refreshes (human decision).

### Plan Improvements
- Specify which verification tools the executor must have for `[verify]` items.

---

## Related Projex Updates

### Documents to Update
| Document | Update Needed |
|----------|---------------|
| 2610162007-remote-integration-rubric-refresh-plan.md | Marked Complete; walkthrough link; moved to `closed/` |
| 2610162007-remote-integration-rubric-refresh-log.md | Moved to `closed/` |
| 2604070218-install-auditor-subject-typed-redesign-nav.md | Maintenance-pass entry (header, Recent Progress, checklist, Revision Log) |
| 2610161927-remote-integration-generic-stewardship-review-eval.md | Source eval; left active (Plan B / generic work and eval refresh still open) |

### New Projex Suggested
| Type | Description |
|------|-------------|
| Plan | Eval refresh: Type 9 cases and eval 24 / 32 wording (see Immediate Follow-ups) |

---

## Appendix

### References
- Commits on `projex/2610162007-remote-integration-rubric-refresh`: `eef9f2b` (step 1), `4321e5b` (step 2), `a09e11a` (complete)
- Base at branch point: `5f93c73`
