# Algorithmic Typosquat Detection (npm v1)

> **Status:** Executed — 2026-04-09
> **Created:** 2026-04-02
> **Last Revised:** 2026-04-09
> **Author:** Claude (plan-projex)
> **Source:** `2604021202-algorithmic-typosquat-detection-proposal.md`
> **Related Projex:** `2604021202-algorithmic-typosquat-detection-proposal.md`, `2604021200-reliability-accuracy-improvements-imagine.md`, `2604070218-install-auditor-subject-typed-redesign-nav.md` (Phase 2 M2.2)
> **Walkthrough:** `2604090330-algorithmic-typosquat-detection-walkthrough.md`
> **Worktree:** No

---

## Blocked On

- **Phase 2 M2.1** of the [subject-typed redesign nav](2604070218-install-auditor-subject-typed-redesign-nav.md): `workflows/registry-package.md` must exist before this plan can execute. Every "Files" reference below that previously targeted `SKILL.md` now targets `workflows/registry-package.md`, which **does not exist yet** — it is the first deliverable of Phase 2 M2.1. Do not attempt execution until that file is authored. This plan is scheduled as Phase 2 M2.2.
- **Proposal acceptance.** `2604021202-algorithmic-typosquat-detection-proposal.md` is still **Draft**. Confirm acceptance or explicit execute override before running.

---

## Summary

Add `scripts/typosquat-check.ps1`: npm-only v1 that pulls a dynamic popular-package baseline (registry search API), computes Levenshtein distance plus optional prefix/suffix “combosquat” hints, compares download counts when both names resolve, and emits structured JSON for the agent. Update `workflows/registry-package.md` and `references/criteria.md` (or the registry-package addendum at `references/criteria/registry-package.md` — whichever Phase 2 M2.1 establishes as the single source of truth for registry-package rubrics) so typosquat verification is tool-assisted, not purely manual. Extend `evals/evals.json` with cases for squat vs legitimate similar name vs scoped-name confusion.

**Scope:** `scripts/` (new script + optional cache file path documented — scripts live at the skill root, not per workflow), `workflows/registry-package.md`, `references/criteria.md` (and/or `references/criteria/registry-package.md` if the per-subject addendum has landed), `evals/evals.json`. **No changes** to `registry-lookup.ps1` (Option C hybrid). **No changes** to `SKILL.md` — after the Phase 1 dispatcher refactor, `SKILL.md` is the dispatcher shell and contains no registry-package workflow steps to modify.

**Estimated Changes:** 4 artifacts (~1 new script 200–350 lines, 3 doc/config edits).

---

## Objective

### Problem / Gap / Need
Typosquatting is CRITICAL in the rubric, but the skill still relies on the agent knowing the “legitimate” name for character-by-character comparison. There is no shared algorithmic signal or popularity ratio.

### Success Criteria
- [ ] `typosquat-check.ps1` runs for `npm` with `-Name` (and optional `-CompareTo`, `-Size` for baseline list size) and prints **valid JSON** to stdout: at minimum `ecosystem`, `targetName`, `candidates` (top matches with `distance`, `normalizedTarget`, `normalizedCandidate`, npm names), `downloadRatio` where both packages exist, and a `riskHint` (`low` | `elevated` | `high`) from documented rules.
- [ ] Baseline list comes from **live** npm search (not only a static file); **24-hour JSON cache** in a path under the repo (e.g. `scripts/.typosquat-cache/`) with fallback behavior if the API fails (clear error JSON + optional bundled minimal stub documented in script header).
- [ ] **Normalization** documented and implemented: scope stripping for comparison, hyphen/underscore folding for *comparison strings* (keep raw names in output), plus **prefix/suffix** overlap check against top-N names for combosquat hints.
- [ ] `workflows/registry-package.md` instructs agents to run typosquat-check for **npm registry packages** (and other ecosystems the workflow owns) after the name is known — in the workflow's Identify / Evidence step — and to cite its output in research / coverage. (Retargeted from `SKILL.md` Step 3 per Phase 1 M1.4.)
- [ ] `references/criteria.md` § 4.1 — and, if the registry-package addendum at `references/criteria/registry-package.md` exists by the time this plan executes, that addendum too — plus the Audit Coverage row for typosquat reference algorithmic checks alongside judgment.
- [ ] `evals/evals.json` adds at least two new eval entries: (1) obvious npm typosquat or ultra-low-download doppelgänger vs popular package, (2) legitimate similarly named package that should **not** be flagged as typosquat-only (false-positive guardrail wording in `expected_output`).

### Out of Scope
- PyPI, crates.io, RubyGems, NuGet in v1 (proposal defers; separate plan later).
- Changing `registry-lookup.ps1` behavior or merging typosquat into it.
- Machine-learning or non-Levenshtein similarity beyond stated prefix/suffix heuristics.
- Automatic verdict changes (still agent interpretation; script is advisory).

---

## Context

### Current State
- **Architectural note (2026-04-08):** After Phase 1 of the subject-typed redesign, `SKILL.md` is the **dispatcher** — Step 0 classifier + Step 1 workflow loader + Step N shared verdict/report skeleton. The old monolithic Steps 1–4 (which previously contained the typosquat language) now live in `workflows/generic.md` as the Phase 1 universal fallback. In Phase 2, registry-package audits will route to a new `workflows/registry-package.md` file that does not yet exist. This plan targets that future file.
- `workflows/generic.md` (formerly `SKILL.md` Step 3 research item 1) still says typosquatting check is **character-by-character** against the legitimate package. The algorithmic replacement wording will land in `workflows/registry-package.md` when that file is authored — this plan does **not** modify `workflows/generic.md` because registry-package audits will no longer route through it after Phase 2.
- `scripts/registry-lookup.ps1` uses `Invoke-RestMethod`, `User-Agent: install-auditor/1.0`, per-ecosystem lookup, JSON to stdout — **no** search/popular list today.
- `references/criteria.md` § 4.1 describes manual comparison and “≤2 characters from top-1000” without saying how “top-1000” is obtained. Per Phase 0 M0.3, a per-subject addendum at `references/criteria/registry-package.md` may also exist by the time this plan executes.
- `evals/evals.json` id 2 covers Slack + `react-native-community-async-storage` but does not test algorithmic tool output.

### Key Files

| File | Role | Change Summary |
|------|------|----------------|
| `scripts/typosquat-check.ps1` | New tool | Parameters, npm search fetch, cache, Levenshtein, normalization, combosquat hints, JSON output. Scripts live at the skill root — path is unchanged by the subject-typed redesign. |
| `workflows/registry-package.md` | Registry-package workflow (does **not** yet exist — Phase 2 M2.1 deliverable) | When/how to invoke typosquat-check inside the registry-package audit flow; align wording with criteria. **Retargeted from `SKILL.md` per Phase 1 M1.4.** |
| `references/criteria.md` | Shared rubrics core | Cross-subject Typosquatting Check guidance + coverage row: tool + judgment |
| `references/criteria/registry-package.md` *(if present by execution time — per Phase 0 M0.3 addendum plan)* | Registry-package rubric addendum | Registry-package-specific typosquat wording tied to script flags |
| `evals/evals.json` | Regression prompts | New evals for tool-assisted scenarios |

### Dependencies
- **Requires:**
  - **Phase 2 M2.1** — `workflows/registry-package.md` must exist (it does not as of 2026-04-08). Until that file is authored, this plan has no destination for the workflow edits in Step 3.
  - Proposal accepted or explicit execute override (proposal still **Draft**).
- **Blocks:** None.
- **Scheduled as:** Phase 2 **M2.2** of [2604070218-install-auditor-subject-typed-redesign-nav.md](2604070218-install-auditor-subject-typed-redesign-nav.md).

### Constraints
- Must follow **CLAUDE.md** / context-mode: no raw `curl` in agent workflows; implementation *inside* the script using `Invoke-RestMethod` is fine for humans/agents running the script.
- Risk hints must not substitute for human verdict; avoid words that imply automatic REJECTED in script output (use `riskHint` / `elevated` only).
- Cache directory should be **gitignored** if written under repo (add `.gitignore` entry only if the plan creates a cache path inside the repo).

### Assumptions
- npm search endpoint shape remains `GET https://registry.npmjs.org/-/v1/search?text=...&size=...&popularity=1.0` (verify during Step 1; adjust query params if API response differs).
- Starting thresholds: **distance ≤ 2** and **download ratio ≥ 100×** (when downloads known) for `elevated`/`high` — tune in script as constants with comments pointing to calibration.

### Impact Analysis
- **Direct:** New script; skill and criteria alignment; eval coverage.
- **Adjacent:** Future PyPI support reuses normalization helpers (copy or dot-source later).
- **Downstream:** Agents must run one more command for npm audits; Tier 1 remains short if output is summarized in one coverage row.

---

## Implementation

### Overview
Implement `typosquat-check.ps1` first (core behavior + JSON contract). Then update criteria (single source of truth for rubric language). Then SKILL (workflow order and coverage). Then evals. Add `.gitignore` for cache folder if needed.

### Step 1: `scripts/typosquat-check.ps1` (npm v1)

**Objective:** Deliver the JSON tool with caching, Levenshtein, normalization, and risk hints.

**Confidence:** Medium (npm search API details need verification on first run)

**Depends on:** None

**Files:**
- `scripts/typosquat-check.ps1`
- `.gitignore` (only if cache lives under repo)

**Changes:**

- **Parameters:** `[ValidateSet('npm')]`, mandatory `-Name`, optional `-CompareTo` (string), `-Size` (default 250), `-CacheHours` (default 24), `-NoCache` switch.
- **Reuse style** from `registry-lookup.ps1`: `$ErrorActionPreference = 'Stop'`, `Invoke-RestMethod` with same `User-Agent`, 15s timeout, try/catch returning structured error in JSON on fatal failure.
- **Popular baseline:** Fetch search results; extract package names (and downloads if present in objects). Merge with **scoped name** list derived from the same query text as the unscoped basename if `-Name` is `@scope/pkg`.
- **Normalization:** Functions e.g. `Get-ComparisonToken` that lowercases, replaces `_`/`-` with a single separator for distance, and compares **unscoped** basename vs scoped variants as proposal describes.
- **Levenshtein:** Classic O(m·n) two-row implementation in PowerShell (no external modules).
- **Combosquat:** For each of top **100** names (by popularity order from API if available), test whether target string starts/ends with that name or vice versa beyond trivial equality; add `combosquatHints` array in JSON.
- **Downloads:** For candidate vs target, call npm download point API (same pattern as `registry-lookup.ps1`) for ratio when both names exist.
- **Output:** Single JSON document via `ConvertTo-Json -Depth 6` to stdout; stderr reserved for optional minimal progress (prefer none for machine parsing).
- **Cache:** Key by ecosystem + size + day bucket; store under `scripts/.typosquat-cache/` (add to `.gitignore`).

**Rationale:** Matches Option C; keeps registry lookup unchanged; testable in isolation.

**Verification:** 
```powershell
.\scripts\typosquat-check.ps1 -Ecosystem npm -Name "lodash" 
.\scripts\typosquat-check.ps1 -Ecosystem npm -Name "react-native-community-async-storage" -CompareTo "@react-native-async-storage/async-storage"
```
Expect valid JSON, low risk for `lodash`, elevated/high hint for async-storage example.

**If this fails:** Revert new files; remove `.gitignore` lines if added.

---

### Step 2: `references/criteria.md` — Typosquat rubric & coverage

**Objective:** Align CRITICAL typosquat guidance with the tool.

**Confidence:** High

**Depends on:** Step 1 (wording references actual flags/fields)

**Files:**
- `references/criteria.md`

**Changes:**
- In **Audit Coverage** table row for typosquat (or equivalent): require **script + judgment** — e.g. “`typosquat-check.ps1` (npm) + name verification.”
- In **§ 4.1 Typosquatting Check**: Replace pure “character by character” with: run **`typosquat-check.ps1`** for npm when auditing npm packages; use **edit distance**, **download ratio**, and **scoped-name / combosquat hints**; keep manual checks for homoglyphs and context; retain “Auto-REJECT if…” but tie “top packages” to **script baseline** or explicit registry data, not intuition.

**Rationale:** Criteria are cited by agents; must match executable behavior.

**Verification:** Grep for “character by character” — should be gone or qualified as supplementary.

**If this fails:** Restore section from git.

---

### Step 3: `workflows/registry-package.md` — Workflow integration *(retargeted 2026-04-08 from `SKILL.md` per Phase 1 M1.4)*

**Objective:** Mandate tool use inside the registry-package workflow without bloating non-registry workflows. After the Phase 1 dispatcher refactor, `SKILL.md` is the dispatcher shell and contains no per-subject workflow steps — all registry-package workflow logic will live in `workflows/registry-package.md` once Phase 2 M2.1 authors it.

**Confidence:** High (once target file exists)

**Depends on:** Step 2 **and** Phase 2 M2.1 (`workflows/registry-package.md` must exist).

**Files:**
- `workflows/registry-package.md` *(does not yet exist — Phase 2 M2.1 deliverable)*

**Changes:**
- In the workflow's **Identify / Evidence** step, after package name + registry are known for **npm** (and any other registry ecosystems the workflow owns), add a bullet: run `.\scripts\typosquat-check.ps1 -Ecosystem npm -Name "<exact name>"` (and `-CompareTo` if user supplied canonical name).
- In the workflow's research / rubric pass corresponding to typosquatting (the formerly-known-as "Step 3 research list item 1"): describe algorithmic check first, manual/homoglyph second.
- In any **Audit coverage** guidance the workflow emits before returning to dispatcher Step N: add row note for typosquat to reference script output when npm. (The dispatcher in `SKILL.md` Step N owns the shared audit-coverage table format; this plan must not change that shape.)
- **Do NOT modify `SKILL.md`** — the dispatcher is subject-agnostic and the classifier / verdict tree / shared report skeleton must not pick up registry-package-specific content.
- **Do NOT modify `workflows/generic.md`** — the Phase 1 universal fallback receives no new registry-specific content; registry-package audits stop routing through it once Phase 2 M2.1 lands.

**Rationale:** Proposal asked for early identification; placing the call inside the registry-package workflow's Identify/Evidence step keeps the tool scoped to subjects where it applies and avoids useless runs for non-registry installables. Matches the subject-typed redesign's core principle (per-subject behavior lives in per-subject workflow files).

**Verification:** Read the workflow end-to-end for internal consistency. Confirm no typosquat-specific language has leaked into `SKILL.md` or `workflows/generic.md`.

**If this fails:** Revert `workflows/registry-package.md` to its pre-plan state.

---

### Step 4: `evals/evals.json` — New eval cases

**Objective:** Regression-test prompts that expect typosquat tool usage in narrative and coverage.

**Confidence:** Medium

**Depends on:** Step 3

**Files:**
- `evals/evals.json`

**Changes:**
- Add **eval id 3**: prompt installing a **suspicious npm name** clearly distance-1 from a mega-popular package (synthetic name ok in prompt) — expect REJECTED/CONDITIONAL and mention algorithmic/similarity/tool.
- Add **eval id 4**: prompt for a **legitimate** package whose name is close to another (document in `expected_output` that CONDITIONAL/APPROVED is ok if script shows low risk and rationale is sound — avoids brittle exact verdict).

**Rationale:** Covers squat detection and false-positive calibration paths from the proposal.

**Verification:** Valid JSON; `id` unique; assertions match strings present in skill.

**If this fails:** Revert `evals/evals.json`.

---

## Verification Plan

### Automated Checks
- [ ] `Get-Content .\scripts\typosquat-check.ps1 | Out-Null` — script parses
- [ ] Run script twice: second run hits cache (timestamp or log in JSON `cache` field optional)
- [ ] `evals/evals.json` valid JSON (parse in PowerShell)

### Manual Verification
- [ ] Async-storage scenario: output lists scoped canonical package as strong candidate
- [ ] Tier 1 path: agent can summarize typosquat row in one line from JSON

### Acceptance Criteria Validation

| Criterion | How to Verify | Expected Result |
|-----------|---------------|-----------------|
| JSON contract | Run script for npm names | stdout is single JSON object with required keys |
| Cache | Two runs within 24h | No duplicate network fetch for baseline (or documented cache hit) |
| Docs aligned | Read criteria + `workflows/registry-package.md` | npm typosquat uses script + judgment; `SKILL.md` dispatcher and `workflows/generic.md` remain unchanged |
| Evals | Read new prompts | Distinct squat vs legitimate-similar cases |

---

## Rollback Plan

1. Delete `scripts/typosquat-check.ps1` and cache dir; remove `.gitignore` entries if added.
2. Restore `workflows/registry-package.md`, `references/criteria.md` (and `references/criteria/registry-package.md` if touched), `evals/evals.json` from base branch.
3. `SKILL.md` and `workflows/generic.md` should not need restoring — this plan does not touch them.

---

## Notes

### Risks
- **npm search API changes:** Mitigation — versioned comment in script; fallback error JSON.
- **False positives:** Mitigation — download ratio + distance gates; eval 4 guards wording.

### Open Questions
- [ ] Accept proposal formally or treat this plan as the acceptance artifact?
- [ ] Exact npm search `text=` query: empty vs `.` vs basename — resolve in Step 1 implementation (must return diverse popular packages).

---

## Relationships

Update `2604021202-algorithmic-typosquat-detection-proposal.md` **Next Steps** to reference this plan filename when committing docs.

---

## Revision History

| Date | Summary of Changes |
|------|--------------------|
| 2026-04-02 | Initial plan drafted (plan-projex). Targets monolithic `SKILL.md` Step 3. Status: Ready. |
| 2026-04-08 | **Retargeted from monolithic `SKILL.md` Step 3 to `workflows/registry-package.md` per Phase 1 M1.4 of the [subject-typed redesign nav](2604070218-install-auditor-subject-typed-redesign-nav.md).** Patch-projex applied. Changes: added "Blocked On" section citing Phase 2 M2.1 dependency; rewrote Summary, Current State, Key Files table, Success Criteria item 4, Step 3 title + body + depends-on + files, Acceptance Criteria row 3, and Rollback step 2 to target `workflows/registry-package.md` and (where present) `references/criteria/registry-package.md` instead of `SKILL.md`; explicitly listed `SKILL.md` and `workflows/generic.md` as **do-not-touch** under the new architecture; Dependencies section now lists Phase 2 M2.1 as a hard requirement and scheduling as Phase 2 M2.2. Status changed from **Ready** → **Blocked — awaiting Phase 2 M2.1**. Typosquat detection logic, thresholds, scoring, eval coverage, and close criteria are unchanged. |
