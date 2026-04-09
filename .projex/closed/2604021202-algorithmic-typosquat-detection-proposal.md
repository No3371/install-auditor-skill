# Algorithmic Typosquatting Detection

> **Status:** Draft
> **Created:** 2026-04-02
> **Author:** Claude (Opus 4.6)
> **Related Projex:** 2604021200-reliability-accuracy-improvements-imagine.md, 2604021815-algorithmic-typosquat-detection-plan.md

---

## Summary

Replace the install-auditor's manual "compare name character by character" typosquatting check with algorithmic detection — edit-distance computation against popular packages, popularity-ratio analysis, and namespace verification. This eliminates dependence on the agent already knowing the legitimate package name and catches squats the agent wouldn't recognize by intuition.

---

## Problem Statement

### Current State

The `SKILL.md` instructs the agent to check for typosquatting by "comparing name character by character against the legitimate package." The `references/criteria.md` § 4.1 has a Typosquatting Check rubric marked CRITICAL. But the detection mechanism is entirely manual:

- The agent must already know (or guess) the legitimate package name to compare against
- No tooling computes edit distance or similarity scores
- No list of popular packages exists for baseline comparison
- Namespace confusion (`lodash` vs `@lodash/lodash`) and naming-convention variants (`react-native-community-async-storage` vs `@react-native-async-storage/async-storage`) aren't caught by character-level comparison

### Gap / Need / Opportunity

Typosquatting is the #1 red flag in the auditor's criteria — an automatic REJECTED. Yet the detection mechanism for this top-priority threat is the least rigorous of any check. The eval for typosquatting (eval id 2: `react-native-community-async-storage`) works because the agent happens to know the legitimate package — but for unfamiliar packages, there's no fallback.

An algorithmic approach would:
- Catch squats of packages the agent has never encountered
- Produce a quantitative similarity score (not just "seems suspicious")
- Work consistently regardless of the agent's training data

### Why Now?

Registry APIs already expose popularity/download data and search endpoints that can return top packages by popularity. The computation (Levenshtein distance) is trivial. The missing piece is a script that ties these together — no new external services needed.

---

## Proposed Change

### Overview

Create a typosquatting detection tool that takes a package name + ecosystem and returns: closest popular-package match, edit distance, download ratio, and a risk assessment. The agent interprets the output rather than doing character comparison manually.

### Approach Options

#### Option A: Standalone Script

- **Description:** New `scripts/typosquat-check.ps1` that fetches top-N popular packages from the registry, computes Levenshtein distance against each, and returns matches within threshold. Includes namespace normalization (strip scopes, normalize hyphens/underscores).
- **Pros:** Clean separation of concerns — `registry-lookup.ps1` stays focused on metadata, typosquat check is independent. Can be tested and evolved separately. Easy to swap implementations later.
- **Cons:** Two scripts to invoke per audit instead of one. Duplicates some registry API calls (fetching popular packages).
- **Effort:** Medium — new script, Levenshtein implementation in PowerShell, registry search API integration.

#### Option B: Integrate into registry-lookup.ps1

- **Description:** Add typosquat checking as an additional output section of the existing registry-lookup script. After fetching package metadata, also fetch popular packages and compute distances.
- **Pros:** Single script invocation. Can reuse the package metadata already fetched. Simpler agent workflow.
- **Cons:** registry-lookup.ps1 grows in scope and complexity. Harder to test the typosquat logic independently. Slower for Tier 1 audits where typosquat check may not need the full popular-package comparison.
- **Effort:** Medium — same logic, different location.

#### Option C: Hybrid — Detection Script + Registry Data

- **Description:** New `scripts/typosquat-check.ps1` for detection logic (edit distance, namespace analysis, risk scoring). Uses the registry search API to dynamically fetch popular packages. `registry-lookup.ps1` remains unchanged for metadata.
- **Pros:** Clean separation. Dynamic popular-package list (always current). Detection script can also accept a "known legitimate name" parameter for direct comparison when the user or agent already knows the target. Composable — Tier 1 can skip it, Tier 2/3 invoke it.
- **Cons:** Extra API call to fetch popular packages. Slightly more complex agent workflow (two scripts).
- **Effort:** Medium.

### Recommended Approach

**Option C (Hybrid).** Keeps `registry-lookup.ps1` focused and stable while adding a new, testable detection capability. The dynamic popular-package fetch via registry search API (e.g., npm: `/-/v1/search?text=&popularity=1.0&size=250`) ensures the comparison baseline is always current. The script accepts optional `--compare-to <name>` for direct comparison when the legitimate name is already known.

---

## Impact Analysis

### Affected Areas

- **`scripts/`** — New `typosquat-check.ps1` script
- **`SKILL.md` Step 3 (Research)** — Update to invoke typosquat-check as a structured step before manual inspection
- **`SKILL.md` Step 1 (Identify)** — Typosquat check should run immediately after gathering the package name, before deeper research
- **`references/criteria.md` § 4.1 Typosquatting Check** — Update rubric to reference algorithmic score alongside manual inspection
- **`evals/evals.json`** — Add eval cases: (1) known typosquat detection, (2) legitimate similar-named package (false positive test), (3) namespace confusion variant

### Dependencies

- Registry search APIs (npm, PyPI) — free, public, already used implicitly by web search
- PowerShell string operations for Levenshtein computation (no external dependencies)

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| False positives on legitimate similar names | High | Medium — could lead to unnecessary CONDITIONAL/REJECTED | Use popularity ratio as gating: only flag if the similar package has >100x more downloads. Legitimate packages in the same space typically have comparable adoption. |
| Registry search API rate limits | Low | Low — one call per audit | Cache popular-package list for 24 hours. Fall back to a bundled static list if API unavailable. |
| Combosquatting not caught by edit distance | Medium | Medium — `express-helper-utils` doesn't trigger distance check against `express` | Add prefix/suffix substring matching against top-100 packages as a supplementary check |
| Levenshtein distance threshold too tight or loose | Medium | Medium — too tight misses squats, too loose floods with false positives | Start with distance <= 2 AND popularity ratio >= 100x. Calibrate based on eval results. |

### Breaking Changes

None. Additive change. Existing audits continue to work — the agent gains a tool it can optionally invoke. The SKILL.md update would make invocation a standard part of the research phase.

---

## Open Questions

- [ ] What edit-distance threshold minimizes false positives while catching real squats? (Likely needs empirical calibration with a test set of known typosquats)
- [ ] Should the script normalize hyphens, underscores, and dots as equivalent before computing distance? (npm treats `my-pkg` and `my_pkg` differently, but squatters exploit this)
- [ ] How large should the dynamic popular-package list be? 250? 500? 1000? Larger lists catch more but cost more compute.
- [ ] Should the script support all ecosystems from day one, or start with npm/PyPI (highest typosquatting risk)?
- [ ] PowerShell vs. JavaScript/Python for the script? PowerShell matches the existing `registry-lookup.ps1`, but Levenshtein in PowerShell is verbose. A Node.js script could be simpler.

---

## Next Steps

If accepted:
1. **Plan created:** `2604021815-algorithmic-typosquat-detection-plan.md` — execute when ready (`/execute-projex`)
2. Build the Levenshtein + registry-search prototype for npm first (highest typosquatting volume)
3. Test against known typosquat incidents (`event-stream`, `ua-parser-js`, `colors`, `node-ipc`) and verify detection
4. Test against legitimate similar-named packages to calibrate false-positive rate
5. Extend to PyPI, then remaining ecosystems
6. Update SKILL.md and criteria.md to reference the new tool
