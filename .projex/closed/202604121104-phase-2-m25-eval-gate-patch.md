# Patch: Close Phase 2 M2.5 Eval Gate

> **Date:** 2026-04-12
> **Author:** Codex (patch-projex, GPT-5)
> **Directive:** Phase 2 M2.5 of `2604070218-install-auditor-subject-typed-redesign-nav.md` — close the registry-package eval gate by adding the missing PyPI typo case, dry-running the full Phase 2 regression set, syncing nav state, and stopping if the walkthrough exposes a runtime gap.
> **Source Plan / Nav:** [`.projex/2604070218-install-auditor-subject-typed-redesign-nav.md`](../2604070218-install-auditor-subject-typed-redesign-nav.md) — Phase 2 M2.5
> **Result:** Success

---

## Summary

Closed Phase 2 by adding eval id 9 for the PyPI `requers` vs `requests` name-confusion case, then running a manual dry-run walkthrough across the full Phase 2 registry-package coverage set. Scope guard passed: the missing work was eval/documentation only, so no changes were needed in runtime files (`SKILL.md`, `workflows/registry-package.md`, `references/criteria*.md`, `scripts/*`).

The nav now reflects Phase 2 as complete on 2026-04-12 and moves roadmap focus to Phase 3 M3.1 (`workflows/browser-extension.md`). This patch is the sole walkthrough artifact for M2.5.

---

## Changes

### Eval Coverage: `evals/evals.json`

**Change Type:** Modified
**What Changed:**
- Appended **id 9**: `pip install requers` with explicit user intent that they expected `requests`.
- Locked the expected behavior to **PyPI manual/canonical name verification**, not npm-only `typosquat-check.ps1`.
- Added assertions for PyPI identification, likely-intended `requests`, manual/canonical verification language, strong `REJECTED`/`CONDITIONAL` verdict guard, `## Audit Coverage`, and `Audit confidence`.

**Why:**
M2.5 was partially complete after id 6 (`requests`) but still lacked the promised PyPI typosquat-style case. `requers` is a real PyPI package as of 2026-04-12 and explicitly positions itself as requests-like, which makes it a good regression for likely-intended-package reasoning without requiring new script support.

---

### Navigation: `.projex/2604070218-install-auditor-subject-typed-redesign-nav.md`

**Change Type:** Modified
**What Changed:**
- **Current Position** — eval coverage `9 cases (0–8)` → `10 cases (0–9)`; M2.5 completion text added.
- **Phase status line** — `Phase 2 is in progress` → `Phase 2 is complete`.
- **Recent Progress** — added 2026-04-12 M2.5 completion entry.
- **Active Work** — rewrote from "remaining Phase 2 milestone" to "Phases 0–2 complete" and Phase 3 M3.1 as next action.
- **Known Blockers** — kept `*(none)*`, retargeted wording from M2.5 readiness to Phase 3 readiness.
- **Phase 2 header** — `Status: Current` → `Status: Complete (2026-04-12)`.
- **M2.5 milestone row** — `[ ]` → `[x]`; replaced future-tense partial-progress text with completion summary and patch link.
- **Priorities** — current focus/next up now point to Phase 3 M3.1.
- **Revision Log** — appended 2026-04-12 row for M2.5 closure and Phase 2 close-out.

**Why:**
The nav is the roadmap source of truth. Once the eval gate passed, Phase 2 could not remain "current" without becoming stale and misleading.

---

### Patch Artifact: `.projex/closed/202604121104-phase-2-m25-eval-gate-patch.md`

**Change Type:** Created
**What Changed:**
- Recorded directive, scope guard result, exact files changed, regression walkthrough, and nav-status effects.

**Why:**
Patch workflow requires one closed record that doubles as the walkthrough.

---

## Verification

**Method:** Static JSON validation + manual dry-run walkthrough + nav state review.

### 1. Eval File Checks

- `evals/evals.json` parses as valid JSON.
- Eval ids are `0,1,2,3,4,5,6,7,8,9` with no duplicates.
- New id 9 contains:
  - PyPI / pip identification
  - likely-intended `requests`
  - manual or canonical name verification wording
  - `REJECTED` or strong `CONDITIONAL` verdict guard
  - `## Audit Coverage`
  - `Audit confidence`

### 2. Manual Dry-Run Walkthrough

- **id 0 — express:** Type 1 registry package; still fits Tier 1/Quick path in `workflows/registry-package.md`.
- **id 1 — Wappalyzer:** Type 2 browser extension; remains the non-registry control case and should not route through `registry-package.md`.
- **id 2 — react-native-community-async-storage:** Type 1 registry package; still fits deep registry flow with Slack-source/name-mismatch concerns.
- **id 3 — expresss:** Type 1 npm typo case; still fits npm algorithmic typosquat path.
- **id 4 — chalk:** Type 1 npm legitimate near-name control; still fits npm false-positive guard path.
- **id 5 — lodash@4.17.20:** Type 1 npm CVE case; still fits vuln lookup path.
- **id 6 — requests:** Type 1 PyPI positive/control case; still fits vuln lookup path and preserves the first PyPI eval.
- **id 7 — mkdirp@0.5.1:** Type 1 npm transitive-vuln case; still fits dep-scan path.
- **id 8 — chalk@5.3.0:** Type 1 npm clean dep-scan case; still fits zero-dependency clean path.
- **id 9 — requers while expecting requests:** Type 1 PyPI name-confusion case; fits existing non-npm manual/canonical name-verification guidance without any workflow or criteria edits.

### 3. Scope Guard Result

- No runtime gap found.
- No edits required in:
  - `SKILL.md`
  - `workflows/registry-package.md`
  - `references/criteria.md`
  - `references/criteria/registry-package.md`
  - `scripts/*`

### 4. Nav Checks

- Phase 2 shows **Complete (2026-04-12)**.
- M2.5 checkbox is checked.
- Priorities now point to Phase 3 M3.1.
- Revision Log includes a 2026-04-12 M2.5 close-out row.

**Status:** PASS

---

## Impact on Related Projex

| Document | Relationship | Update Made |
|----------|-------------|-------------|
| [`.projex/2604070218-install-auditor-subject-typed-redesign-nav.md`](../2604070218-install-auditor-subject-typed-redesign-nav.md) | Governing nav | Phase 2 status → Complete; M2.5 checked off; priorities shifted to Phase 3 |
| `evals/evals.json` | Regression coverage | Added id 9 for PyPI `requers` vs `requests`; ids 0–8 preserved |
| [`.projex/closed/2604110900-transitive-dep-scan-walkthrough.md`](2604110900-transitive-dep-scan-walkthrough.md) | Upstream close-out | Its immediate follow-up ("Execute M2.5 eval gate") is now resolved by this patch |

---

## Notes

- **Patch vs plan-execute:** Patch was the correct workflow. Scope stayed to one eval file, one nav file, and one closed patch record; the dry-run exposed no need for runtime changes.
- **Live-package caveat handled:** The PyPI package choice was re-validated at execution time. If `requers` had disappeared or stopped being a plausible `requests` confusion case, this patch would have stopped instead of silently swapping cases.
- **Dirty worktree note:** Pre-existing untracked `AGENTS.md` was left untouched and excluded from staging.
