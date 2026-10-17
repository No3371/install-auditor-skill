# Eval iteration-6 fixes: harness script path, Conditions scope, eval texts

> **Status:** Ready
> **Author:** Claude (Opus)
> **Parent:** 2610171024-eval-run-iteration6-handoff-memo.md
> **Source:** 2610171024-eval-run-iteration6-handoff-memo.md § Proposed next step
> **Related Projex:** 2610171024-eval-run-iteration6-handoff-memo.md, 2604070218-install-auditor-subject-typed-redesign-nav.md, 2610170504-eval-suite-refresh-walkthrough.md
> **Worktree:** No

---

## Summary

Fix the three failure groups from live eval iteration-6 (348/362, 14 failures in 13 evals; memo triage names 11 of them — the per-workflow table implies one more registry-package and one more remote-integration failure, ids lost with the workspace) without live cost: (1) eval harness tells the auditor to call skill scripts by absolute path; (2) `SKILL.md` + report template say what may be a Condition; (3) four eval texts plus one shared assertion fixed so they test what the rubric says. Nav records results.

**Scope:** `evals/run_evals.py`, `evals/test_run_evals.py`, `evals/evals.json`, `SKILL.md`, `references/report-template.md`, nav. No rubric semantics change; no workflow / criteria addendum edits.
**Estimated Changes:** 6 files; 1 template string, 1 test, 2 SKILL.md paragraphs + 1 line, 2 template lines, 35 eval assertion / expected_output edits, 2 nav bullets.

---

## Objective

### Problem / Gap / Need

Failure groups (memo triage, re-checked here):

1. **Script calls denied → coverage gaps → CONDITIONAL** (evals 0, 5, 8, 18, 51). 23/52 Bash denials were `cd <snapshot> && python3 scripts/…`. Allowlist rule `Bash(python3 <snapshot>/scripts/:*)` matches only absolute-path calls. `SKILL.md` Reference Files shows `python3 scripts/<script>.py` (relative), which invites `cd`. Auditors then wrote "run `npm audit`" Conditions although Step N says coverage alone never changes the verdict.
2. **Hardening advice / MEDIUM notes listed as Conditions** (evals 16, 26, 37). `SKILL.md` and `references/report-template.md` never define what belongs under Conditions vs Recommendation / Post-Install Checklist.
3. **Eval text defects:**
   - Eval 8 assertion 3 text is only `Audit confidence`; same bare text in 24 evals (1–4, 7–25, 33). Grader has nothing to judge.
   - Eval 22 assertion 4 "transport (stdio) and isolation" — "isolation" undefined.
   - Eval 24 "official Slack app" names no app → auditor cannot identify publisher; `exact_match APPROVED` then contradicts `SKILL.md` Behavioral Principle 1 ("Unknown ≠ safe").
   - Eval 40 `@anthropic/some-code-skill` does not exist on npm → REJECTED / not-found is defensible; assertion allows only APPROVED/CONDITIONAL.
   - Eval 26 (redis): report cited CVE-2026-81934 (TLS use-after-free, fixed in 6.2.24 / 7.2.16 / 7.4.11 / 8.2.9 / 8.4.6 / 8.6.6 / 8.8.2 / 8.10.1; not in KEV as of 2026-09-02) and CVE-2026-23479 (blocked-client use-after-free, fixed in 7.2.14 / 7.4.9 / 8.2.6 / 8.4.3 / 8.6.3). Both real, own code, fixed upstream (web search 2026-10-17: Debian tracker, Tenable, action1, scworld). Per `references/criteria.md` §4.3 an own-code HIGH/CRITICAL CVE **with a fixed release** that affects the resolved version is a HIGH flag → CONDITIONAL (condition: install the fixed release). The shared trace assertion (8 evals: 0, 11, 16, 18, 20, 26, 36, 37) allows only V1 cooldown or third-party HIGH CVE → stricter than §4.3. Whether the iteration-6 redis digest was in the affected range cannot be re-judged: workspace lost.

### Success Criteria

- [ ] `prepare` writes task prompts that tell the auditor to call `python3 <snapshot>/scripts/…` by absolute path and not to `cd`; unit test asserts it
- [ ] `SKILL.md` Step N defines Conditions as fixes for the flags behind a CONDITIONAL verdict and routes coverage gaps / hardening / LOW notes to Recommendation or Post-Install Checklist; Reference Files run line names absolute-path invocation
- [ ] `references/report-template.md` Conditions placeholder and Quick skeleton Recommendation line carry the same rule
- [ ] Zero assertions with text exactly `Audit confidence`; 24 replaced by deterministic `contains_string` on `**Audit confidence (coverage):**`
- [ ] Trace assertion in 8 evals includes the §4.3 fixed-release case; matching `expected_output` sentences updated
- [ ] Evals 22, 24, 40 assertions and expected outputs updated per Step 4
- [ ] `python3 evals/run_evals.py validate` exits 0; `python3 -m unittest discover -s evals -p 'test_*.py'` passes
- [ ] Nav Known Blockers + Recent Progress record iteration-6 results and this plan

### Out of Scope

- Live re-run of the 13 failing evals (~$4; needs user approval)
- Proxy-blocked sources (api.osv.dev, GHSA, some docs) — environment, not repo (affects eval 5 CVE-query assertions even after Step 1)
- Allowlisting `cd … && …` compound commands (rejected; see Step 1 Rationale)
- Workflow / criteria addendum `Toward CONDITIONAL` wording (those name flag-driven conditions; consistent with new rule)
- Other memo follow-ups (Scorecard shape, chalk range, registry tooling, trigger evals, PS 5.1)

---

## Context

### Current State

- `evals/run_evals.py` `TASK_PROMPT_TEMPLATE` (lines 70–83): says relative skill paths resolve against the skill path; says nothing about how to run scripts. `default_allowed_tools` (440–447) allows `Bash(python3 {s}/scripts/:*)` + pwsh/powershell `-File {s}/scripts/` only. `build_exec_cmd` docstring: allowlist must exclude bare Bash / unrestricted shell prefixes (hostile prompts).
- `evals/test_run_evals.py` `test_prepare` (≈line 218): asserts snapshot path and eval prompt appear in `task_prompt.md`.
- `SKILL.md` Step N: line 118 defines CONDITIONAL; line 120 Coverage gaps rule; line 164 Quick skeleton Recommendation; line 204 script run line.
- `references/report-template.md` lines 57–58: `## Conditions (CONDITIONAL verdict only)` + `<Specific conditions that must be met before installation>`.
- `evals/evals.json`: 61 evals, 362 assertions. `contains_string` graded by substring over reports + response + assistant text (`grade_deterministic`).

### Key Files

| File | Role | Change Summary |
|------|------|----------------|
| `evals/run_evals.py` | eval harness | task prompt: absolute-path script rule |
| `evals/test_run_evals.py` | harness unit tests | assert new prompt line |
| `SKILL.md` | dispatcher + verdict tree | Conditions vs Recommendation rule; coverage-gap clause; script run line |
| `references/report-template.md` | Tier 2/3 skeleton | Conditions placeholder text |
| `evals/evals.json` | eval cases | 24 + 8 shared assertion edits; evals 22, 24, 40 |
| `.projex/2604070218-install-auditor-subject-typed-redesign-nav.md` | roadmap | record results |

### Dependencies

- **Requires:** branch carrying `claude/youthful-dijkstra-5ov1kt` history (eval refresh `e88e47f`, memo `b9810a9`)
- **Blocks:** optional re-run of failing evals (iteration-7)

### Constraints

- Allowlist stays free of bare Bash and `cd`-prefixed rules (hostile eval prompts)
- Verdict line, `## Audit Coverage`, `**Audit confidence (coverage):**` stay byte-identical (graders parse them)
- `SKILL.md` stays lean (15,488 B now); add ≤ 900 B

### Assumptions

- Claude Code `--allowedTools` prefix rules check each `&&` sub-command separately, so `cd <snap> && python3 scripts/x.py` needs a `cd` rule plus a relative `python3 scripts/` rule; the absolute-path form needs neither. (Consistent with 23 observed denials.)
- Model grader reads the new trace assertion's three-way OR as written (same pattern already used).

### Impact Analysis

- **Direct:** files above
- **Adjacent:** graders of the 24 evals now deterministic on the confidence line → a report that paraphrases the line now fails (intended: `SKILL.md` requires exact line)
- **Downstream:** iteration-6 numbers not comparable 1:1 with iteration-7 (assertion count 362 → 363)

---

## Implementation

### Overview

Prompt fix → skill wording → eval data → nav. Steps 1–4 independent; Step 5 last.

### Step 1: Task prompt — absolute-path script calls

**Objective:** stop `cd … && python3 scripts/…` denials.
**Confidence:** High
**Depends on:** None
Do-Projex: Encouraged

**Files:** `evals/run_evals.py`, `evals/test_run_evals.py`

**Changes:**

```python
# Before (TASK_PROMPT_TEMPLATE):
Read {snapshot}/SKILL.md first and follow it exactly. Relative paths in the skill (workflows/, references/, scripts/, .projex/) resolve against the skill path. Use only this copy of the skill, not any other installed install-auditor.

Working directory: {outputs}

# After:
Read {snapshot}/SKILL.md first and follow it exactly. Relative paths in the skill (workflows/, references/, scripts/, .projex/) resolve against the skill path. Use only this copy of the skill, not any other installed install-auditor.
Run the skill's scripts by absolute path, for example: python3 {snapshot}/scripts/vuln-lookup.py -Ecosystem npm -Name <name>. Do not cd into the skill path first; compound commands such as cd ... && python3 scripts/... are denied.

Working directory: {outputs}
```

```python
# test_prepare — after: self.assertIn(str(snap), prompt)
            self.assertIn(f"python3 {snap}/scripts/vuln-lookup.py", prompt)
```

(`prepare` formats the template with the `Path` itself, so `{snap}` renders identically.)

**Rationale:** Allowing `Bash(cd {s}:*)` + relative `Bash(python3 scripts/:*)` would let an auditor run any `scripts/*.py` it writes into its own working directory → breaks the hostile-prompt guard in `build_exec_cmd`. Prompt instruction keeps the allowlist unchanged.

**Verification:** unit tests pass; `python3 evals/run_evals.py prepare --workspace <scratch> --ids 0` → `task_prompt.md` contains the new line with the absolute snapshot path.

**If this fails:** revert the two hunks.

---

### Step 2: `SKILL.md` — script run line

**Objective:** skill itself steers to full-path calls (also helps installed-skill use outside evals).
**Confidence:** High
**Depends on:** None
Do-Projex: Encouraged

**Files:** `SKILL.md` (Reference Files, last bullet)

**Changes:**

```markdown
<!-- Before -->
… JSON to stdout. Run: `python3 scripts/<script>.py -Ecosystem <eco> -Name <name> [-Version <ver>]` (Python ≥3.8, stdlib only; Windows: `py -3`). …

<!-- After -->
… JSON to stdout. Run: `python3 <skill-dir>/scripts/<script>.py -Ecosystem <eco> -Name <name> [-Version <ver>]` by full path, without `cd` (Python ≥3.8, stdlib only; Windows: `py -3`). …
```

**Rationale:** relative example invites `cd <skill-dir> &&`, which permission allowlists commonly deny.

**Verification:** `grep -n "python3 <skill-dir>/scripts/" SKILL.md` → 1 hit.

**If this fails:** revert line.

---

### Step 3: Conditions vs Recommendation rule

**Objective:** coverage gaps and hardening advice never become Conditions.
**Confidence:** High
**Depends on:** None
Verify-Projex: Encouraged

**Files:** `SKILL.md` (Step N), `references/report-template.md`

**Changes:**

```markdown
<!-- SKILL.md Before (line 118) -->
**CONDITIONAL** means installation may proceed only after listed conditions are met (pin to safe version, disable permissions, sandbox only, etc.).

<!-- After -->
**CONDITIONAL** means installation may proceed only after listed conditions are met (pin to safe version, disable permissions, sandbox only, etc.).

**Conditions vs Recommendation:** a Condition clears a flag that put the verdict at CONDITIONAL in the tree (a HIGH flag, a medium CVE, the 3+ MEDIUM set, abandonment) — name the flag it clears. Coverage gaps and checks to re-run (e.g. "run `npm audit` first"), general hardening (least privilege, rootless runtime, telemetry opt-out), update-control advice, and LOW notes go in Recommendation or the Post-Install Checklist, never in Conditions. An APPROVED report has no Conditions; do not raise a verdict to CONDITIONAL to carry advice.
```

```markdown
<!-- SKILL.md Before (line 120) -->
… add a sentence to Recommendation that the audit has **reduced coverage**. Do **not** change the verdict label for coverage alone — the verdict still follows the tree above.

<!-- After -->
… add a sentence to Recommendation that the audit has **reduced coverage**. Do **not** change the verdict label or add Conditions for coverage alone — the verdict still follows the tree above.
```

```markdown
<!-- SKILL.md Quick skeleton Before (line 164) -->
<1–2 sentences. CONDITIONAL: list the conditions. APPROVED/CONDITIONAL: pin to <package>@<version>; re-audit on any `references/criteria.md` §4.6 V5 trigger.>

<!-- After -->
<1–2 sentences. CONDITIONAL: list the conditions, each naming the flag it clears. APPROVED/CONDITIONAL: pin to <package>@<version>; re-audit on any `references/criteria.md` §4.6 V5 trigger.>
```

```markdown
<!-- references/report-template.md Before (line 58) -->
<Specific conditions that must be met before installation>

<!-- After -->
<One condition per flag that made the verdict CONDITIONAL, naming that flag (`SKILL.md` Step N → Conditions vs Recommendation). Coverage gaps, hardening and LOW notes go in Recommendation or Post-Install Checklist.>
```

**Rationale:** one rule in Step N, referenced from template; no addendum edits (their `Toward CONDITIONAL` conditions are flag-driven already).

**Verification:** `wc -c SKILL.md` growth ≤ 900 B; `grep -c "Conditions vs Recommendation" SKILL.md references/report-template.md` → 1 each; verdict line / `## Audit Coverage` / `**Audit confidence (coverage):**` unchanged (`git diff` shows no hunk on them).

**If this fails:** revert both files.

---

### Step 4: Eval data fixes

**Objective:** assertions test what the rubric says.
**Confidence:** High (4a, 4b, 4c, 4e) | Medium (4d — judgment call, see Rationale)
**Depends on:** None
Verify-Projex: Encouraged

**Files:** `evals/evals.json`

**Changes:** edit with a one-off Python script (load → mutate → `json.dump(indent=2, ensure_ascii=False)` matching current formatting; if formatting differs, do exact string edits instead). Do not commit the script.

**4a — bare `Audit confidence` (24 evals):** every assertion `{"text": "Audit confidence", "type": "contains_concept"}` →
```json
{"text": "Report has the **Audit confidence (coverage):** line", "type": "contains_string", "value": "**Audit confidence (coverage):**"}
```

**4b — shared trace assertion (evals 0, 11, 16, 18, 20, 26, 36, 37):** text →
```
If the verdict is CONDITIONAL, every condition traces to a §4.6 V1 fresh-version cooldown (resolved release under 72 hours old), a §4.3 third-party / OS-package HIGH CVE that is not KEV-listed, or a §4.3 HIGH/CRITICAL CVE in the resolved version that has a fixed release and is not a KEV-listed CRITICAL (condition: install the fixed release); an APPROVED verdict passes this check
```
`expected_output` substring replacements:

| ids | Before | After |
|---|---|---|
| 0 | `every condition is a V1 cooldown or a non-KEV third-party HIGH CVE (§4.3)` | `every condition is a V1 cooldown, a non-KEV third-party HIGH CVE, or a CVE in the resolved version with a fixed release (not a KEV-listed CRITICAL; condition: install the fix) (§4.3)` |
| 11, 16, 20, 36, 37 | `CONDITIONAL only for a V1 cooldown or a non-KEV third-party HIGH CVE.` | `CONDITIONAL only for a V1 cooldown, a non-KEV third-party HIGH CVE, or a CVE in the resolved version with a fixed release (not a KEV-listed CRITICAL; condition: install the fix, §4.3).` |
| 18 | `CONDITIONAL only for a V1 cooldown (release under 72 hours old) or a non-KEV third-party HIGH CVE.` | `CONDITIONAL only for a V1 cooldown (release under 72 hours old), a non-KEV third-party HIGH CVE, or a CVE in the resolved version with a fixed release (not a KEV-listed CRITICAL; condition: install the fix, §4.3).` |
| 26 | `a V1 cooldown (new upstream redis release under 72 hours old) or an unfixed OS-package / third-party HIGH CVE that is not KEV-listed in the current digest (C6).` | `a V1 cooldown (new upstream redis release under 72 hours old), an unfixed OS-package / third-party HIGH CVE that is not KEV-listed in the current digest (C6), or a redis own-code CVE that affects the digest's redis version and has a fixed release (§4.3; e.g. CVE-2026-81934 or CVE-2026-23479 on a lagging digest; condition: pull a digest with the fix).` |

**4c — eval 22 assertion 4:** text `Report discusses transport (stdio) and isolation` → `Report identifies the transport as stdio: a local subprocess of the client with no network listener`.

**4d — eval 24:** replace assertion 5 `{"text": "Verdict is APPROVED", "type": "exact_match", "expected": "APPROVED"}` with two:
```json
{"text": "Verdict is APPROVED or CONDITIONAL (not REJECTED)", "type": "verdict_check", "expected": ["APPROVED", "CONDITIONAL"]},
{"text": "If the verdict is CONDITIONAL, its only conditions are to confirm which Slack Marketplace listing and publisher the app is (the request names no specific app); the three requested scopes raise no condition. An APPROVED verdict passes this check", "type": "contains_concept"}
```
`expected_output`: `Verdict should be APPROVED.` → `Verdict APPROVED; CONDITIONAL is acceptable only when the sole conditions are confirming the specific app listing and its publisher, since the request names no app.`

**4e — eval 40 assertion 4:** `{"text": "Verdict is CONDITIONAL or APPROVED", "type": "verdict_check", "expected": ["APPROVED", "CONDITIONAL"]}` →
```json
{"text": "Report states whether @anthropic/some-code-skill exists on npm. If it is not found, the verdict is CONDITIONAL or REJECTED and the report says there is nothing to install under that name; if it exists, the verdict is APPROVED or CONDITIONAL", "type": "contains_concept"}
```
`expected_output`: `Tier 2 audit. Verdict CONDITIONAL (skill content requires review of capability scope, but install gate is npm).` → `Tier 2 audit. Verdict CONDITIONAL (skill content requires review of capability scope, but install gate is npm). The example name may not exist on npm; then a not-found CONDITIONAL or REJECTED is correct and the routing assertions still apply.`

**Rationale:**
- 4a: `SKILL.md` requires the exact line; deterministic check removes grader guesswork. Applied to all 24, not only eval 8: same defect.
- 4b: aligns with `references/criteria.md` §4.3 table (fixed-release HIGH/CRITICAL → HIGH flag → CONDITIONAL).
- 4d: alternative — rename to a specific real Slack-built app. Rejected now: app identity and its scope set could not be verified (slack.com unreachable from this environment), and a wrong scope list would make a new false failure. If the user names an app with verifiable scopes, swap prompt and restore `exact_match APPROVED`.
- 4e: routing is the eval's purpose; verdict must not punish correct not-found handling.

**Verification:** `python3 evals/run_evals.py validate` → exit 0; script check: 0 assertions with text `Audit confidence`; 8 trace assertions contain `fixed release`; total assertions 363; `git diff --stat evals/evals.json` touches only expected lines.

**If this fails:** `git checkout -- evals/evals.json`.

---

### Step 5: Nav record

**Objective:** results survive (workspace lost).
**Confidence:** High
**Depends on:** Steps 1–4

**Files:** `.projex/2604070218-install-auditor-subject-typed-redesign-nav.md`

**Changes:**
- Known Blockers: replace bullet `**Step 4 live eval run** — iteration-6, 61 evals, in progress; results to follow.` with `**Eval iteration-6** — 61/61 ran, 348/362 assertions (96%), audit cost $17.28; failures triaged in 2610171024-eval-run-iteration6-handoff-memo.md and fixed (no live cost) by 2610171239-eval-iteration6-fixes-plan.md. Memo triage names 11 of the 13 failing evals (0, 5, 8, 16, 18, 22, 24, 26, 37, 40, 51); one registry-package and one remote-integration failure are unnamed (per-workflow table). Re-run of the failing evals not done (~$4, needs approval). Proxy-blocked OSV/GHSA still limits eval 5.`
- Recent Progress: new top entry dated 2026-10-17 summarizing Steps 1–4 (files, counts).

**Verification:** `grep -n "iteration-6" <nav>` shows both.

**If this fails:** revert nav hunk.

---

## Verification Plan

### Automated Checks
- [ ] `python3 -m unittest discover -s evals -p 'test_*.py'`
- [ ] `python3 evals/run_evals.py validate`
- [ ] `python3 -m unittest discover -s tests -p 'test_*.py'` (unchanged scripts; regression guard)

### Manual Verification
- [ ] Read rendered `task_prompt.md` from a scratch `prepare`
- [ ] Re-read `SKILL.md` Step N top to bottom: new paragraph does not contradict tree terms or Escalation

### Acceptance Criteria Validation
| Criterion | How to Verify | Expected Result |
|-----------|---------------|-----------------|
| Prompt rule | `test_prepare` | pass |
| Conditions rule | grep `Conditions vs Recommendation` | 1 hit per file |
| Bare confidence gone | JSON scan | 0 |
| Trace assertion | JSON scan | 8 contain `fixed release` |
| Evals valid | `validate` | exit 0 |

---

## Rollback Plan

1. `git revert` the execution squash commit on the base branch.
2. Nav: re-mark eval follow-up as open if only partially reverted.

---

## Notes

### Risks
- 4a stricter: reports that paraphrase the confidence line now fail. Mitigation: skill already mandates exact line; failure is a real defect.
- Step 1 relies on auditor obeying prompt; some denials may remain. Mitigation: re-run measures denials (`run` transcripts).
- Eval 26 true verdict unknown for iteration-6 digest; 4b makes either outcome gradable on re-run.

### Split Decision
`No split — single scope (.projex root), within size budget` (5 steps, < 500 lines).

### Open Questions
- [ ] *(none blocking)* 4d chosen over naming a specific Slack app — user may override.
