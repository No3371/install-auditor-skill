# Walkthrough: Container-Image Rubric Refresh

> **Execution Date:** 2026-10-16
> **Completed By:** Claude (executor subagent) | closed by close-projex subagent
> **Source Plan:** 2610162004-container-image-rubric-refresh-plan.md
> **Parent:** 2610162004-container-image-rubric-refresh-plan.md
> **Duration:** ~60 min (20:10-21:10 per execution log timestamps)
> **Result:** Success

---

## Summary

Container-image rubric rewritten on the shared §4.6 floor, encoding the human decisions C4 (Docker Official Images reach Tier 1), C6 (Blocking CVE) and C7 (one rule for critical runtime flags). `references/criteria/container-image.md` 12,735 → 27,227 B (factual refresh of registries, signing and SBOM guidance; policy rows; new `## CVE Scope (§4.3)` and `## Version & Update Integrity (§4.6)` V1-V5 with `**Curated pipelines:**`; rewritten tiers). `workflows/container-image.md` 24,031 → 32,684 B (23 replacements/insertions). `references/criteria.md` §4.4 `### Docker Image Permissions` block 4 → 4 lines (21,455 → 21,925 B, one hunk). Consistency script `OK`; harness unchanged; traces T1-T12 match.

---

## Objectives Completion

| Objective | Status | Notes |
|-----------|--------|-------|
| C1 every tag mutable unless enforced; Tier 1 needs a digest (except C4 dev path) | Complete | Tag-vs-digest table and scoring; "specific immutable tag" removed |
| C2 Docker Content Trust retired | Complete | `DOCKER_CONTENT_TRUST` only on the Retired row |
| C3 identity-flagged `cosign verify`, `verify-attestation` for SBOMs, `gh attestation verify oci://`, BuildKit provenance | Complete | `cosign download sbom` only on deprecated lines; no bare `cosign verify <image>` |
| C4 DOI Tier 1 path | Complete | V2 `**Curated pipelines:**` + V1 version unit; `:latest` Tier 3 exception for DOI/hardened; T1 → Tier 1 → APPROVED |
| C5 hardened catalogs | Complete | DHI and other hardened-catalog rows, Rekor caveat |
| C6 Blocking CVE alignment | Complete | `## CVE Scope (§4.3)`; the 4 conflicting lines rewritten; T9-T10 match §4.3 |
| C7 one rule for critical flags | Complete | Unverified → CRITICAL; verified publisher → HIGH, identical in addendum, workflow, `criteria.md` §4.4 |
| C8 frozen namespaces, Artifact Registry naming | Complete | Frozen-namespace row (HIGH → CONDITIONAL) |
| C9 user-namespace / PSS positives, digest refresh, layer secret scan | Complete | Low-risk rows; V5 refresh rule; `trivy image --scanners secret` |
| X1 / X3 identity-matched signing; pinned scanners | Complete | V2 identity match; V3 HIGH on mismatch; audit-tooling note cited |
| Contract: coverage row + canonical-row mapping | Complete | `| Version integrity (§4.6) | Required | Required | Required |`; mapping paragraph |

---

## Execution Detail

> Derived from `git log`/`git diff` of `17fa9b1..projex/2610162004-container-image-rubric-refresh` (start commit) and the execution log.

### Setup and Preflight

**Planned:** start commit, worktree, shared-floor greps, harness baseline.
**Actual:** start commit `17fa9b1` on base; worktree created; no bootstrap needed. Floor greps all passed; container files unchanged since `97f6bce`; Docker block matched Step 4 Before (4 bullets). `validate` 41 evals / 248 assertions; unittest evals 12 OK; tests 19 OK (6 skipped). Optional fact probe: `docker buildx imagetools inspect redis --format '{{json .Provenance}}'` returned a non-empty per-platform SLSA provenance. Commit `a2d0795`.
**Deviation:** Base moved after planning (anchors verified at `242310a`, executed on `376ba86` + `17fa9b1`); anchors still matched.

### Step 1: Addendum factual refresh (header, registries, signing, SBOM)

**Planned:** 1a-1d.
**Actual:** After-blocks extracted programmatically (line-range replace with start/end anchor assertions, applied bottom-up). DCT/`Still present` → 0; Hardened/Frozen/Artifact Registry rows 3; `certificate-oidc-issuer` ≥ 1. Commit `5d07665`.
**Deviation:** Interim `cosign download sbom` count 2 (the old Tier 1 bullet still present until Step 2g); resolved at Step 2.

### Step 2: Addendum policy and plug-ins

**Planned:** 2a-2g.
**Actual:** root/entrypoint-drop/layer-secret rows, root-at-runtime scoring (dev LOW, non-dev HIGH), user-namespace and PSS low-risk rows, C7 runtime scoring, tag-vs-digest table, new `## CVE Scope (§4.3)` and `## Version & Update Integrity (§4.6)` before tiers, Tier 1/2/3 rewritten. Two plug-in headings; V1-V5 once each; `**Curated pipelines:** Docker Official Images` 1; stale phrases 0. Commit `a393495`.
**Deviation:** None.

### Step 3: Workflow alignment

**Planned:** 3a-3w (~22 replacements).
**Actual:** 23 replacements/insertions: intro, Identify table (DHI and Artifact Registry rows), tier bullets, research Q2/Q3/Q4/Q6/Q8, signature/SBOM/CVE blocks, runtime positives, provenance block, coverage table + mapping paragraph, Subject Rubric 4.1-4.6, Verdict Notes. Stale phrases 0; coverage row 1; `### 4.6 Supply Chain & Version Integrity` 1; file 317 → 349 lines. Commit `dcc2ba7`.
**Deviation:** None. Observation: the file's top HTML comment (line 3) still says "GCR" (see Recommendations).

### Step 4: `references/criteria.md` §4.4 Docker block

**Planned:** replace the 4 bullets under `### Docker Image Permissions` with a pointer line + 3 summary bullets.
**Actual:** one hunk `@@ -209,4 +209,4 @@`, entirely inside the Docker block. `CRITICAL on an image whose identity does not verify` 1. Commit `18dc1c9`; completion commit `58154a0`.
**Deviation:** None.

**Files Changed (ACTUAL):**
| File | Change Type | Planned? | Details |
|------|-------------|----------|---------|
| `references/criteria/container-image.md` | Modified | Yes | 26 hunks, lines 6-259; new sections at ~lines 184-220; 146 lines changed |
| `workflows/container-image.md` | Modified | Yes | ~45 hunks, lines 16-343; 162 lines changed |
| `references/criteria.md` | Modified | Yes | Lines 209-212 only (`### Docker Image Permissions`); 4 lines changed |

---

## Complete Change Log

> **Derived from:** `git diff --stat 17fa9b1..projex/2610162004-container-image-rubric-refresh`: 5 files changed, 312 insertions(+), 111 deletions(-) (including projex documents).

### Files Created
| File | Purpose | Lines | In Plan? |
|------|---------|-------|----------|
| `.projex/2610162004-container-image-rubric-refresh-log.md` | Execution log | 104 | Yes (implicit) |
| `.projex/closed/2610162004-container-image-rubric-refresh-walkthrough.md` | This walkthrough | - | Yes (close) |

### Files Modified
| File | Changes | Lines Affected | In Plan? |
|------|---------|----------------|----------|
| `references/criteria/container-image.md` | 7 rewritten sections + 2 new plug-in sections | 146 changed; 27,227 B | Yes |
| `workflows/container-image.md` | 23 replacements/insertions | 162 changed; 32,684 B | Yes |
| `references/criteria.md` | §4.4 Docker block only | 4 changed; 21,925 B | Yes |
| `.projex/2610162004-container-image-rubric-refresh-plan.md` | Status Complete, Log, Walkthrough link | 3 lines | Yes (close) |

### Files Deleted
None.

### Planned But Not Changed
None. `SKILL.md`, `references/registries.md`, `evals/`, `STEWARDSHIP.md` untouched, as scoped.

---

## Success Criteria Verification

| Criterion | Method | Result | Evidence |
|-----------|--------|--------|----------|
| CVE Scope + V&UI sections once; V1-V5 once each; `**Curated pipelines:**` names Docker Official Images | grep + consistency script | Pass | 2 headings; V1-V5 1 each; curated 1 |
| `§4.6 V<n>` references name V1-V5; one shared floor heading | consistency script | Pass | `OK` |
| Stale phrases gone; `cosign download sbom` only on "deprecated" lines; `DOCKER_CONTENT_TRUST` only on "retired" lines | grep | Pass | 0 stale; line 77 deprecated; line 57 Retired row |
| No bare `cosign verify <image>`; keyless examples carry both identity flags | grep | Pass | met |
| C7 identical across addendum, workflow, `criteria.md` | read-through | Pass | met |
| C4 encoded; T1 → Tier 1 → APPROVED | trace | Pass | T1 |
| C6 encoded; T9-T10 match §4.3 | trace | Pass | T9, T10 |
| Coverage row + mapping paragraph | grep | Pass | row 1 |
| `validate` + unittest with Preflight count | harness | Pass | 41 / 248; evals 12 OK; tests 19 OK (6 skipped) |
| Diff lists exactly the 3 files; `criteria.md` only the Docker block | `git diff --stat`, hunk check | Pass | one hunk `@@ -209,4 +209,4 @@` |

**Overall:** 10/10 criteria passed. Traces T1-T12 (T1, T1b, T1c, T2-T12) all match the plan's expected column (execution log "Post-execution").

---

## Deviations from Plan

### Deviation 1: Base moved after planning
- **Planned:** anchors verified at `242310a`.
- **Actual:** executed from `17fa9b1` (after sibling plans and start commits).
- **Reason:** concurrent orchestration.
- **Impact:** none; all anchors still matched.
- **Recommendation:** none.

### Deviation 2: No Verify-Projex / Do-Projex dispatch, no task tool
- **Planned:** Encouraged verification for Steps 1-3 and Do-Projex for Step 4.
- **Actual:** self-verified with verbatim After-text, the plan's greps, the consistency script and a diff read-through; the log served as the task ledger.
- **Reason:** no spawn or task tool in the executor's environment.
- **Impact:** none observed.
- **Recommendation:** none.

### Deviation 3: First log commit amended
- **Actual:** the executor amended its first log commit (`a2d0795`, local, never pushed) once to add the required attribution trailers. This close did not amend or rewrite any commit.

---

## Issues Encountered

### Issue 1: Interim Step 1 grep expectation
- **Description:** `cosign download sbom` matched the old Tier 1 bullet until Step 2g replaced it.
- **Severity:** Low
- **Resolution:** final-state check passes.

### Issue 2: Overlaps at close
- **Description:** the browser close earlier edited a different sub-table of `references/criteria.md` §4.4; other closes advanced base and the roadmap nav.
- **Severity:** Low
- **Resolution:** merged per hunk; nav add/add conflicts resolved by keeping both sides (see below).

### Close notes
- Nav `2604070218-install-auditor-subject-typed-redesign-nav.md` updated in the close commit, following earlier rubric-refresh closes (plan carries no `Nav:` field).

---

## Key Insights

**Rationale promoted:** none needed. Rationale ships in the addendum and workflow text; no shipped file carries projex references (grep clean).

### Lessons Learned

1. **Presence is not trust**
   - Context: signing, SBOM and tag checks were scored on presence.
   - Insight: credit only identity-matched signer/provenance (V2); a mismatch is V3 HIGH. Keyless `cosign` without both identity flags verifies nothing.
   - Application: other rubrics that credit signatures.

2. **Human decisions can collide with rule changes**
   - Context: "eval 26 stays APPROVED" (C4) vs Blocking CVE (C6): an unfixed OS HIGH in the current `redis` digest yields CONDITIONAL.
   - Insight: the collision is data-dependent; the eval plan must pick an option.
   - Application: see Eval hand-off below.

### Gotchas / Pitfalls

1. **Retired and broken commands**
   - Trap: `DOCKER_CONTENT_TRUST=1 docker pull` breaks DOI pulls; bare `cosign verify` and `cosign download sbom` are retired or broken.
   - Avoidance: rubric text now marks them retired/deprecated and gives the replacement commands.

### Technical Insights

- `docker buildx imagetools inspect <image> --format '{{json .Provenance}}'` returned non-empty SLSA provenance for the current `redis` index on 2026-10-16.

---

## Recommendations

### Immediate Follow-ups
- [ ] DOI provenance probe: output was non-empty but the builder/source fields were not inspected, so Curated pipelines check (3) is untested on a live digest; inspect them (plan Risk "check (3) shape").
- [ ] `workflows/container-image.md` line-3 HTML comment still lists "GCR" among registries; update to Artifact Registry naming (plan C8 listed only the intro and Identify rows).
- [ ] The addendum Medium-risk runtime table still rates `securityContext.runAsUser: 0` as Medium, contradicting the new root-in-production HIGH rule; reconcile the two rows (T12 passes via the root-at-runtime rule).
- [ ] Eval refresh plan: eval 26 (premises: no upstream redis release < 72 h; no unfixed OS HIGH; choose `[APPROVED, CONDITIONAL]`, pin a clean digest, or escalate; add to the time-dependent list; update description to "Tier 1 (Tier 2 if DOI attestations cannot be checked)"); eval 12 (`nginx:latest`; replace "immutable tag" with digest-only); new cases T5, T8, T6, T11, T9 (with and without VEX), T12.
- [ ] `references/registries.md` §Container Images (registry-package plan or a patch): add rows "Docker Hardened Images (`dhi.io`) | High" and "Frozen / legacy namespaces (e.g. `bitnamilegacy`) | Low (no updates)".
- [ ] STEWARDSHIP container row Watch column: DOI signing replacement (none confirmed as of 2026-10) | DHI verification flow | `cosign` / `gh attestation` flag changes.

### Future Considerations
- Align the §4.3 plug-in heading across addenda (`## CVE Scope (§4.3)` matches browser-extension and ci-action).

### Plan Improvements
- Order Step 1 grep expectations to the post-Step-2 state, or note which hits are transient.

---

## Related Projex Updates

### Documents to Update
| Document | Update Needed |
|----------|---------------|
| `2610162004-container-image-rubric-refresh-plan.md` | Status Complete; Walkthrough link; moved to closed |
| `2610162004-container-image-rubric-refresh-log.md` | Moved to closed |
| `2604070218-install-auditor-subject-typed-redesign-nav.md` | Recent Progress, checklist, Revision Log, Last Revised |
| `2610161928-stewardship-review-container-cli-desktop-eval.md` | Left active (cli-binary plan still pending) |

### New Projex Suggested
| Type | Description |
|------|-------------|
| Plan | Eval refresh covering eval 26 / eval 12 and the new container cases |
| Patch/Revise | Container consistency patch: line-3 "GCR" comment, `runAsUser: 0` row, DOI provenance field inspection |

---

## Appendix

### References
- Execution commits: `a2d0795` (log and preflight), `5d07665` (step 1), `a393495` (step 2), `dcc2ba7` (step 3), `18dc1c9` (step 4), `58154a0` (complete)
- Execution log: `2610162004-container-image-rubric-refresh-log.md`
