# Dispatcher Lean Report, Output Location & Trigger Tuning

> **Status:** Complete
> **Author:** Claude (Opus 5.5), plan-projex subagent
> **Parent:** Orchestrator
> **Source:** Direct request (orchestrated: "It's been a while. What can we do to improve this?" → "orchestrate it"; candidates 6, 7b, 7c + deferred `SKILL.md:156`)
> **Related Projex:** 2604170511-measure-read-cost-f7-m53-findings.md (Option 2 "dispatcher compression", deferred) | 2604070218-install-auditor-subject-typed-redesign-nav.md (§ Priorities "Dispatcher compression … future enhancement") | 2610161852-dispatcher-rubric-consistency-plan.md + its walkthrough (Red Flags / tree terms / Reference Files text on base; "later compression plan must carry … forward") | 2610161849-python-script-ports-plan.md (owns `SKILL.md` Step 1 sentence + Reference Files script bullet; deferred `SKILL.md:156` here) | 2610161850-eval-runner-harness-plan.md + walkthrough (landed: `evals/run_evals.py` graders parse report strings)
> **Worktree:** Yes
> **Completed:** 2026-10-16
> **Walkthrough:** 2610161910-dispatcher-lean-report-and-trigger-walkthrough.md
> **Log:** 2610161910-dispatcher-lean-report-and-trigger-log.md

---

## Summary

Three dispatcher (`SKILL.md`) improvements, one plan because all land in the same ~120 lines of `SKILL.md`:

1. **Lean report (item 6):** Step N report skeleton split by tier — compact **Quick skeleton** stays inline for Tier 1; full skeleton moves to new `references/report-template.md`, read only by Tier 2/3. Reference Files list de-duplicated (per-workflow/per-addendum bullets already covered by Dispatch Table + each workflow's own pointer). Last `.ps1` mention in the skeleton (`SKILL.md:156`) dropped.
2. **Output location (item 7c):** default report path `<project-root>/.install-audits/audit-<name>-<version>.md` instead of `audit-<package-name>.md` in cwd; caller-named location wins.
3. **Trigger tuning (item 7b):** frontmatter `description` scoped to *new* third-party installables + major-version/maintainer changes, explicit skip cases (lockfile reinstall, first-party, package-manager debugging); fixes stale `PASS/CONDITIONAL/FAIL` labels → `APPROVED/CONDITIONAL/REJECTED`. Ships a 20-query trigger eval set for skill-creator's description-eval tooling.

**Measured effect (scratch simulation on post-python-ports `SKILL.md`, 2026-10-16):** `SKILL.md` 17,093 B → 14,994 B (−2,099 B, −12%). Tier 1 audit reads −2.1 KB. Tier 2/3 audits read +741 B net (14,994 + 2,840 B template) and one extra Read. Byte breakdown: report section 3,165 → 2,818 B (includes +~640 B new location rule) | Reference Files 3,250 → 1,402 B | frontmatter 801 → 897 B.

**Scope:** `SKILL.md` (frontmatter, Step N `### Report Skeleton` block, `### Reference Files`) | new `references/report-template.md` | `references/criteria.md` line 15 pointer | new `evals/trigger-evals.json` | `STEWARDSHIP.md` one sentence.
**Estimated Changes:** 2 new files, 3 edited files; ~130 lines of `SKILL.md` touched, no workflow files.

---

## Objective

### Problem / Gap / Need

- **Read cost.** m53 findings: dispatcher `SKILL.md` ~15 KB "retained load-bearing content … Audit-coverage report skeleton — required output format for every audit, blocks compression"; Option 2 (externalize skeleton) deferred. Re-verified 2026-10-16: `SKILL.md` = 16,766 B on base (17,093 B after python-ports merge); skeleton block lines 121–196 = 3,165 B incl. confidence rules embedded inside the template fence; Reference Files lines 224–249 = 2,948 B (3,250 B post-ports).
- **Orchestrator claim checked ("move skeleton → Tier 1 reads less"): partly true.** Every audit writes a report, so moving the *whole* skeleton out saves nothing (same bytes + 1 Read). Savings exist only if Tier 1 gets a smaller skeleton: Quick skeleton inline + full skeleton in a reference saves Tier 1 ~350 B net of the new location rule. The larger, tier-independent win is the Reference Files duplication (−1,848 B): its 9 workflow bullets restate the Dispatch Table; its 9 addendum bullets restate pointers every workflow already carries (verified: each non-generic `workflows/<type>.md` cites `references/criteria/<type>.md` 2–9×).
- **Tier 1 concision.** Eval 0 (express, Quick) expects "short APPROVED report without excessive ceremony", `line_count_max` 79. The single skeleton has 11 sections; Tier 1 guidance is one sentence ("doesn't need every section filled out").
- **Over-triggering.** `description` says "Use this skill whenever … wants to install, add, or enable anything … npm/pip/gem packages … Trigger this skill before allowing any installation to proceed." → routine `npm ci` / `pip install -r requirements.txt` / package-manager error fixing in ordinary coding tasks match. Also names verdicts `PASS/CONDITIONAL/FAIL`; the skill emits `APPROVED/CONDITIONAL/REJECTED`.
- **Litter.** `SKILL.md:123` "Write the report to `audit-<package-name>.md`" → file in cwd (usually the user's repo root), one per audit, no version in name (re-audit of a new version overwrites the old evidence).
- **Stale refs.** `SKILL.md:162` `registry-lookup.ps1` in skeleton example (python-ports left it here; its plan cites `:156`, pre-2610161852 numbering; python-ports' one-line edits do not shift it). `references/criteria.md:15` "see `SKILL.md` Step 6" — no Step 6 exists (dispatcher uses Step 0 / 1 / N).

### Success Criteria

- [ ] `references/report-template.md` exists; holds the full skeleton; contains `**Verdict: [APPROVED ✅ | CONDITIONAL ⚠️ | REJECTED ❌]**`, `## Audit Coverage`, `**Audit confidence (coverage):**`; no `.ps1`; no `Tier 1` text inside its fence.
- [ ] `SKILL.md` Step N has `### Report` with Location, Shape, Audit-confidence rules, and a fenced Quick skeleton of ≤ 40 lines containing the same three strings; no `### Report Skeleton` heading remains.
- [ ] `SKILL.md` default location text names `.install-audits/` and `audit-<name>-<version>.md`; `audit-<package-name>.md` absent.
- [ ] `grep -c '\.ps1' SKILL.md` = 1 (the python-ports script bullet's twin mention only).
- [ ] `SKILL.md` § Reference Files: every backticked path without `<type>` exists on disk; script bullet byte-identical to base at execution start.
- [ ] `SKILL.md` bytes ≤ 15,300 and ≥ 1,800 below baseline B0 recorded in Preflight.
- [ ] Frontmatter parses as YAML; `name: install-auditor` unchanged; description ≤ 1024 chars, no `<`/`>`, contains `APPROVED/CONDITIONAL/REJECTED`, no `PASS`/`FAIL`.
- [ ] `references/criteria.md` has no `Step 6`.
- [ ] `evals/trigger-evals.json`: JSON array, 20 items, keys exactly `query`,`should_trigger`, 10 true / 10 false, unique queries.
- [ ] `python3 evals/run_evals.py validate` exit 0 (`41 evals, 248 assertions …`); `python3 -m unittest discover -s evals -p "test_*.py"` OK; `prepare` snapshot contains `references/report-template.md`.
- [ ] Untouched: Step 0, Dispatch Table, Step 1, Verdict Tree + Tree terms, Coverage gaps, Escalation, Red Flags, Behavioral Principles (diff hunks only in frontmatter, report block, Reference Files); `workflows/`, `scripts/`, `evals/evals.json` byte-unchanged.

### Out of Scope

- Red Flags / Verdict Tree / Tree terms relocation — needed during evidence gathering (early-exit on red flags), not only at report time; text owned by closed 2610161852 plan, kept verbatim.
- Step 0 classifier compression or Dispatch Table removal (classifier semantics owned by 2610161852; `references/classifier.md` already holds the long form).
- Workflow files: their "return to `SKILL.md` Step N for … report skeleton / report shape" pointers stay valid (Step N routes to the right skeleton). No edits.
- New eval cases (e.g. asserting `.install-audits/` path) and changes to `evals/evals.json` / `evals/run_evals.py`.
- Running the description-optimization loop (`run_loop.py`) — needs `claude -p` auth, absent on this host; trigger set is shipped for later runs.
- Editing users' `.gitignore`; this repo's `.gitignore`.
- Nav doc revision log (close-projex / orchestrator).

---

## Context

### Current State

`SKILL.md` on base `claude/youthful-dijkstra-5ov1kt` (`3abdc75`; eval-runner merged, python-ports **not yet**): 250 lines, 16,766 B. Sections (line: bytes): frontmatter 1–12: 801 | Step 0 24: 3,364 | Dispatch Table 68: 733 | Step 1 85: 469 | Verdict Tree 93: 2,200 (incl. Tree terms, Coverage gaps) | **Report Skeleton 121–196: ~3,165** | Escalation 198 | Red Flags 202: 1,726 | Principles 214: 550 | **Reference Files 224–249: 2,948**.

Report Skeleton block specifics:
- L123: `Write the report to \`audit-<package-name>.md\`. Adapt depth to audit tier — a Tier 1 quick audit doesn't need every section filled out.`
- L125–196: one fenced template; inside it L158 disclaimer sentence (report text) and L169–173 "Rules of thumb for confidence" (auditor guidance accidentally inside the template fence); L162 `e.g., registry-lookup.ps1 / npm API`.

python-ports (`projex/2610161849-python-script-ports`, execution complete at `0178221`, awaiting close) changes exactly: L87 tail → `…and may invoke the lookup scripts in \`scripts/\` (see Reference Files). Then return here for Step N.` and replaces the `scripts/registry-lookup.ps1` Reference Files bullet with a `scripts/registry-lookup.py | … dep-scan.py` bullet (~640 B; still the only `.ps1` mention: "same-named `.ps1` twin"). Its branch predates 2610161852's Reference Files edit, so the merged Reference Files list = base list with the script bullet swapped. `references/criteria.md` L9/39/63/151/157/159 edited by python-ports; L15 not.

eval-runner (landed `3abdc75`) contracts this plan must keep:
- `collect()` → `out.rglob("audit-*.md")` (pathlib rglob traverses dot-dirs — verified: finds `o/.install-audits/audit-x-1.0.md`); `file_exists` glob `audit-*.md`; `line_count_max` 79 on eval 0.
- `VERDICT_RE` `^[ \t>*_]*Verdict[ \t]*[:*]+[ \t*]*(APPROVED|CONDITIONAL|REJECTED)\b` — skeleton placeholder `**Verdict: [APPROVED …` must not match (`[` blocks) — unchanged.
- `contains_string` value `## Audit Coverage` in 32 evals; `Audit confidence` is a `contains_concept` assertion (model-graded) in most evals.
- `skill_frontmatter_name()` regex `^---\s*\n(.*?)\n---` then `^name:\s*(\S+)\s*$`.
- `prepare` snapshot = `SKILL.md` + git-tracked `workflows/`, `references/`, `scripts/` → new `references/report-template.md` included once tracked (working-tree copy; must be `git add`ed or committed before `prepare`).
- task prompt: "Write every file you produce, including the audit report, into the working directory." → caller-named location → report lands in `outputs/`.

Scratch simulation (repo clone + python-ports SKILL.md edits + this plan's texts): `unittest` 12 OK, `validate` exit 0, skill-creator `quick_validate.py` "Skill is valid!", Quick skeleton fence 33 lines.

### Key Files

| File | Role | Change Summary |
|------|------|----------------|
| `SKILL.md` | Dispatcher, loaded on every trigger | Frontmatter description; `### Report Skeleton` → `### Report`; Reference Files de-dup |
| `references/report-template.md` | New | Full (Tier 2/3) skeleton, moved from `SKILL.md` |
| `references/criteria.md` | Shared rubric | L15 `Step 6` → Step N Report pointer |
| `evals/trigger-evals.json` | New | 20 should/should-not trigger queries |
| `STEWARDSHIP.md` | Review guide | One sentence on trigger evals in § Running Evals |

### Dependencies

- **Requires:** 2610161849-python-script-ports-plan.md closed and merged to base (Preflight checks). eval-runner merged (done).
- **Blocks:** none. Future plans adding evals for `.install-audits/` or Tier 1 shape build on this.

### Constraints

- Red Flags, Tree terms & precedence, Verdict Tree, Coverage gaps, Escalation, Behavioral Principles, Step 0, Dispatch Table, Step 1: byte-identical.
- Script bullet in Reference Files: carry byte-identical from base at execution time (python-ports owns its wording).
- Report contract strings identical in both skeletons: `**Verdict: [APPROVED ✅ | CONDITIONAL ⚠️ | REJECTED ❌]**`, `## Audit Coverage`, `**Audit confidence (coverage):**`.
- Report filename must start `audit-` and end `.md` (eval glob).
- Frontmatter description: ≤ 1024 chars, no `<`/`>` (skill-creator `quick_validate.py` rules), `name` unchanged.

### Assumptions

- python-ports merges with SKILL.md diff limited to L87 + the script bullet (verify in Preflight).
- Agents reading `SKILL.md` at report time know the final tier (workflows triage tier in Evidence Part A before reporting; "any red flag" → Tier 3).
- `git rev-parse --show-toplevel` is available wherever audits run in a repo; outside a repo the rule falls back to cwd.
- Description wording reduces over-triggering without under-triggering genuine new installs — unverified here (no `claude -p` auth); the trigger set makes it testable later.

### Impact Analysis

- **Direct:** 5 files above.
- **Adjacent:** 10 workflows point to "`SKILL.md` Step N … report skeleton / report shape" — still correct (Step N routes). `references/criteria.md` L35/L51 "per Tier 1 rules in `SKILL.md`" — still correct (Quick skeleton inline). `workflows/cli-binary.md:156` "Audit Coverage table itself is in `SKILL.md` Step N" — still reachable via Step N.
- **Downstream:** report files move from cwd to `.install-audits/` for users; eval runs unaffected (caller names working dir). Fewer false triggers on lockfile installs.

---

## Implementation

### Overview

Preflight → template file first (so `SKILL.md` never points at a missing file) → `SKILL.md` report block → Reference Files → frontmatter → small pointer/doc edits. All text below is final; paste exactly.

### Preflight (no file changes; record results in execution log)

```bash
test -f scripts/registry-lookup.py && grep -c 'python3 scripts/<script>.py' SKILL.md   # expect file present, count 1
grep -n '^### Report Skeleton$\|^### Reference Files$\|^### Escalation$' SKILL.md     # 3 hits
wc -c < SKILL.md                                                                       # record as B0 (expect ~17,093)
python3 evals/run_evals.py validate | head -1                                          # 41 evals, 248 assertions …
```

Missing `scripts/registry-lookup.py` or count ≠ 1 → python-ports not merged → stop, mark plan `Blocked`.

---

### Step 1: Create `references/report-template.md`

**Objective:** Full skeleton for Tier 2/3 in its own reference, derived from `SKILL.md` L125–196.
**Confidence:** High
**Depends on:** Preflight
**Do-Projex:** Encouraged

**Files:** `references/report-template.md` (new)

**Changes:** new file, exact content:

````markdown
# Report Template — Full (Tier 2 / Tier 3)

Full report skeleton for Standard and Deep audits. File location, Audit confidence rating rules, and the Quick (Tier 1) skeleton live in `SKILL.md` Step N → Report. Keep the verdict line, the `## Audit Coverage` heading, and the `**Audit confidence (coverage):**` line identical to the Quick skeleton; graders and tooling parse them.

```
# Install Audit: <name> v<version>

**Verdict: [APPROVED ✅ | CONDITIONAL ⚠️ | REJECTED ❌]**
**Audit tier:** [Standard | Deep]
**Subject type:** <from Step 0 classifier output>
**Date:** <today's date>

## Summary
<2–4 sentences: what this is, who makes it, key finding.>

## Security
| Area | Finding |
|------|---------|
| CVEs / Advisories | None found · or · list with IDs and severity |
| Supply Chain Risk | Low / Medium / High — reason |
| Permissions | Acceptable · or · Concerns: list |
| Telemetry/Privacy | None · Opt-out · Always-on |
| Dependency Risk | Low / Medium / High — reason |

## Reliability
| Area | Finding |
|------|---------|
| Maintenance | Active / Stale / Abandoned / Archived |
| Last Release | date |
| Publisher Trust | Verified / Unverified / Anonymous |
| Adoption | downloads/week, stars, etc. |
| License | SPDX — Compatible / Review needed / Incompatible |

## Audit Coverage

**Audit confidence (coverage):** [ High | Moderate | Low ] — [short reason: e.g., "8/9 checks Done, 1 Not available"]

Audit confidence measures **how completely the tier-appropriate checklist was executed** — **not** whether the installable is free of vulnerabilities. Unknown issues remain possible even when coverage is High.

| Check | Status | Source or notes |
|-------|--------|-----------------|
| Registry / metadata lookup | Done | e.g., registry-lookup / npm API |
| Typosquat / name verification | Done | compared to `<legitimate name>` |
| CVE / advisories | Done, 0 results | OSV, GHSA |
| OpenSSF Scorecard | Not available | no repo for Scorecard API |
| Source code review (behavioral) | Skipped (Tier 2) | Tier 3 only |
| *(add rows from `references/criteria.md` for this tier)* | | |

## Risk Flags
<List each, or "None identified">
- [CRITICAL/HIGH/MEDIUM/LOW] description

## Alternatives
<1–3 alternatives if concerning, or "No better alternative identified">

## Conditions (CONDITIONAL verdict only)
<Specific conditions that must be met before installation>

## Recommendation
<1–3 sentences. Clear guidance on what to do.>

## Post-Install Checklist (APPROVED/CONDITIONAL only)
- [ ] Pin to exact audited version (<package>@<version>)
- [ ] Verify checksum/signature if provided
- [ ] Check lock file for unexpected entries after install
- [ ] Review post-install script output if applicable
- [ ] Re-audit on major version bump or maintainer change

**Sources:** <URLs consulted>
```
````

Diff vs `SKILL.md` L125–196 (intended, nothing else): `Audit tier` drops `Quick` | confidence example reason `7/9 … 2 Skipped (Tier 1)` → `8/9 … 1 Not available` | row `Deep web / incident search | Skipped (Tier 1) | —` → `Source code review (behavioral) | Skipped (Tier 2) | Tier 3 only` (Tier-skip at T2 per `references/criteria.md` rows table) | last row drops `; Tier 1: keep to ~3–6 rows — minimal set only` | `registry-lookup.ps1` → `registry-lookup` (python-ports stem convention) | "Rules of thumb for confidence" block (L169–173) removed — moves to `SKILL.md` § Report (this plan's Step 2).

**Rationale:** Tier 2/3 workflows already read several references; one more costs ~2.8 KB on 25–40 KB audits. Tier-1-only wording removed so the template does not contradict the Quick skeleton.

**Verification:**
```bash
grep -c 'Verdict: \[APPROVED ✅ | CONDITIONAL ⚠️ | REJECTED ❌\]\*\*\|^## Audit Coverage$\|^\*\*Audit confidence (coverage):\*\*' references/report-template.md   # 3
grep -c '\.ps1\|Tier 1' references/report-template.md   # 1 (header prose "Quick (Tier 1) skeleton" only)
```

**If this fails:** delete the file; nothing references it yet.

---

### Step 2: Replace `SKILL.md` `### Report Skeleton` with `### Report`

**Objective:** Location rule, tier routing, confidence rules (moved out of the template fence), inline Quick skeleton.
**Confidence:** High
**Depends on:** Step 1
**Verify-Projex:** Encouraged

**Files:** `SKILL.md`

**Changes:** replace everything from the line `### Report Skeleton` through the closing fence line after `**Sources:** <URLs consulted>` (base L121–196; the blank line before `### Escalation` stays) with:

````markdown
// Before (head and tail of the replaced block):
### Report Skeleton

Write the report to `audit-<package-name>.md`. Adapt depth to audit tier — a Tier 1 quick audit doesn't need every section filled out.

```
# Install Audit: <name> v<version>
… (L126–194 unchanged template incl. "Rules of thumb for confidence") …
**Sources:** <URLs consulted>
```

// After:
### Report

**Location:** if the user or calling prompt names an output file or directory, write there. Otherwise write to `.install-audits/` at the project root (`git rev-parse --show-toplevel` from the current directory; outside a repo, the current directory), creating the folder if needed. File name: `audit-<name>-<version>.md`, lowercased, with `@`, `/`, `:` and spaces turned into `-` and no leading `-` (`@types/node` 20.11.0 → `audit-types-node-20.11.0.md`); drop `-<version>` when the subject has none. Do not edit `.gitignore` or commit the report. Finish by telling the user the verdict, the report path, and any conditions.

**Shape:** by final tier, after any mid-audit escalation. Tier 1 (Quick) uses the Quick skeleton below; keep it under 80 lines. Tier 2 and Tier 3 read `references/report-template.md` and fill its full skeleton. Every report keeps the verdict line, the `## Audit Coverage` heading, and the `**Audit confidence (coverage):**` line exactly as written; graders and tooling parse them.

**Audit confidence** measures how completely the tier-appropriate checklist was executed, not whether the installable is free of vulnerabilities. Rate it:

- **High:** All tier-required checks are Done, legitimately **N/A**, or **Skipped (Tier N)** by design; at most one **Not available** on a non-critical row.
- **Moderate:** One–two **Not available** rows that are not solely tier-skips, or a critical-adjacent gap.
- **Low:** Three or more **Not available**, or any tier-required check missing without a valid **Skipped** / **N/A** reason — especially **CVE / advisories** unavailable for Tier 2 or Tier 3.

**Quick skeleton (Tier 1):**

```
# Install Audit: <name> v<version>

**Verdict: [APPROVED ✅ | CONDITIONAL ⚠️ | REJECTED ❌]**
**Audit tier:** Quick
**Subject type:** <from Step 0 classifier output>
**Date:** <today's date>

## Summary
<2–3 sentences: what this is, who makes it, key finding.>

## Audit Coverage

**Audit confidence (coverage):** [ High | Moderate | Low ] — [short reason: e.g., "4/4 Tier 1 checks Done"]

| Check | Status | Source or notes |
|-------|--------|-----------------|
| Registry / metadata lookup | Done | e.g., registry-lookup / npm API |
| Typosquat / name verification | Done | compared to `<legitimate name>` |
| CVE / advisories | Done, 0 results | OSV, GHSA |
| License compatibility | Done | SPDX — Compatible |
| *(Tier 1 minimal set from `references/criteria.md`, ~3–6 rows; deeper rows `Skipped (Tier 1)` or omitted)* | | |

## Risk Flags
<"None identified", or one line per flag: - [HIGH/MEDIUM/LOW] description>

## Recommendation
<1–2 sentences. CONDITIONAL: list the conditions. APPROVED/CONDITIONAL: pin to <package>@<version>; re-audit on major version bump or maintainer change.>

**Sources:** <URLs consulted>
```
````

The three confidence bullets are the base L171–173 bullets verbatim (moved, not reworded).

**Rationale:**
- Quick skeleton = 6 sections (header, Summary, Audit Coverage, Risk Flags, Recommendation, Sources); folds Conditions + the two load-bearing post-install items (pin, re-audit) into Recommendation → matches eval 0 "without excessive ceremony", < 80 lines. Tier 1 rows mirror `references/criteria.md` Tier 1 Required set (registry, typosquat, CVE, license).
- Confidence rules leave the template fence: they are auditor guidance, needed by both tiers, and `references/criteria.md` L31 points to `SKILL.md` for them.
- **Location decision.** Chosen: `<project-root>/.install-audits/` — one contained folder; reviewable/committable as approval evidence (description: report "to review before installing"); survives in-repo PR review. Rejected: cwd root (current — one stray file per audit in repo root) | `~/.install-audits/` (outside the project's review flow; lost in ephemeral cloud sandboxes) | OS temp (lost) | auto-adding to `.gitignore` (mutates user config unasked; some teams want reports committed). Version in filename keeps prior-version evidence on re-audit. Caller-named location first keeps eval runs (`task_prompt.md` names the working directory) and team conventions working.

**Verification:**
```bash
grep -c '^### Report Skeleton$\|audit-<package-name>' SKILL.md     # 0
grep -n '^### Report$\|\.install-audits/\|references/report-template.md' SKILL.md   # heading + location + shape (+ Reference Files after Step 3)
awk '/^\*\*Quick skeleton/{f=1} f&&/^```$/{c++} f{n++} c==2{print n; exit}' SKILL.md   # ≤ 40 (sim: 33)
grep -c 'Rules of thumb for confidence' SKILL.md                   # 0
git diff -U0 SKILL.md | grep '^@@'                                 # hunks only inside old L121–196 region
```

**If this fails:** `git checkout -- SKILL.md`; redo from the Before anchor.

---

### Step 3: De-duplicate `SKILL.md` § Reference Files

**Objective:** One bullet per file *kind*; keep every file reachable; keep the script bullet verbatim.
**Confidence:** High
**Depends on:** Step 1 (new reference listed)
**Do-Projex:** Encouraged

**Files:** `SKILL.md`

**Changes:** replace all bullets under `### Reference Files` **except** the bullet starting `` - `scripts/registry-lookup.py` `` (copy that line byte-identical from the file, place it last). Base after python-ports merge has 24 bullets (generic + 9 workflows + criteria.md + 9 addenda + licenses + registries + script + classifier, script second-to-last) → 8 after.

````markdown
// Before (shape):
### Reference Files

- `workflows/generic.md` — Low-confidence fallback (subject probe + user clarification + defensive minimum audit)
- `workflows/registry-package.md` — Type 1 registry-package workflow
… (8 more workflow bullets, `references/criteria.md`, 9 `references/criteria/<type>.md` addendum bullets, licenses, registries) …
- `scripts/registry-lookup.py` | `typosquat-check.py` | `vuln-lookup.py` | `dep-scan.py` — … (python-ports text)
- `references/classifier.md` — Full classifier rule: tie-breaking, routing overrides, extended signals, worked hybrid examples, edge-case discipline

// After:
### Reference Files

- `workflows/<type>.md` — per-type workflow, one per Dispatch Table row; `workflows/generic.md` is the low-confidence fallback (subject probe + user clarification + defensive minimum audit)
- `references/classifier.md` — Full classifier rule: tie-breaking, routing overrides, extended signals, worked hybrid examples, edge-case discipline
- `references/criteria.md` — Shared tier-aware scoring rubric and canonical Audit Coverage rows
- `references/criteria/<type>.md` — Per-type criteria addendum (types 1–9); each workflow names its own and when to read it
- `references/report-template.md` — Full report skeleton for Tier 2 / Tier 3 audits
- `references/licenses.md` — License compatibility matrix
- `references/registries.md` — Trusted vs. untrusted registries per ecosystem
- `scripts/registry-lookup.py` | `typosquat-check.py` | `vuln-lookup.py` | `dep-scan.py` — … (byte-identical python-ports bullet)
````

File ends with the script bullet + single trailing newline.

**Rationale:** Workflow paths are fully determined by the Dispatch Table; addendum paths by `references/criteria/<type>.md` + the pointer each workflow carries. Classifier, generic-fallback and licenses/registries descriptions kept verbatim. Departure from the 2610161852 walkthrough note ("carry … Reference Files text forward verbatim"): that note guards the label cleanup it did (no `(Phase N, Mx.y)` labels, no `.projex` runtime pointer); both stay honored — no label or `.projex` path reintroduced; only duplicated per-file bullets are removed. Saves 1,848 B on every audit.

**Verification:**
```bash
sed -n '/^### Reference Files$/,$p' SKILL.md | grep -o '`[a-z][a-zA-Z0-9/._-]*`' | tr -d '`' | grep -E '^(workflows|references|scripts)/' | while read p; do [ -e "$p" ] || echo "MISSING $p"; done   # no output (filter skips API hosts like api.osv.dev/v1/query in the script bullet)
sed -n '/^### Reference Files$/,$p' SKILL.md | grep -c '^- '      # 8
diff <(git show HEAD:SKILL.md | grep '^- `scripts/registry-lookup.py`') <(grep '^- `scripts/registry-lookup.py`' SKILL.md) && echo same   # same
grep -c '\.projex\|(Phase' SKILL.md                               # 0
```

**If this fails:** restore the section from `git show HEAD:SKILL.md`.

---

### Step 4: Retune frontmatter `description`

**Objective:** Trigger on new third-party installables and risk-changing upgrades; skip lockfile reinstalls, first-party packages, package-manager debugging; correct verdict labels.
**Confidence:** Medium (triggering effect unmeasured without `claude -p`)
**Depends on:** None
**Do-Projex:** Encouraged

**Files:** `SKILL.md` (lines 1–12)

**Changes:**

```yaml
# Before:
---
name: install-auditor
description: >
  Mandatory security and reliability audit for any installable in software development environments.
  Use this skill whenever an employee, developer, or agent wants to install, add, or enable anything
  to a development system — including browser extensions, VS Code/IDE plugins, npm/pip/gem packages,
  desktop applications, CLI tools, Docker images, GitHub Actions, or any third-party software.
  Trigger this skill before allowing any installation to proceed. Also trigger when someone asks
  "is it safe to install X", "can I add X to my dev environment", "should I use X package",
  or "audit this extension/plugin/tool". This skill produces a structured PASS/CONDITIONAL/FAIL
  audit report that must be reviewed before installation is approved.
---

# After:
---
name: install-auditor
description: >
  Security and reliability audit to run before any new third-party installable enters a dev
  environment. Use it whenever a user or agent is about to add an npm/pip/cargo/gem/go/nuget/maven
  dependency, browser extension, IDE plugin, desktop app, CLI tool or curl-pipe-to-shell installer,
  Docker image, CI action, MCP server, Claude Code plugin or skill, or OAuth/API-key integration;
  for a major-version upgrade or maintainer change of an existing dependency; and when asked
  "is X safe to install", "should we use X", or "audit this extension/plugin/tool". Skip it when only
  reinstalling what a lockfile or manifest already pins (npm ci, pip install -r with nothing new),
  for first-party or workspace packages, and for debugging package-manager errors. Produces an
  APPROVED/CONDITIONAL/REJECTED audit report to review before installing.
---
```

Folded scalar: never break a line inside a `/`-joined token (`npm/pip/…/maven` stays on one line).

**Rationale:** Keeps skill-creator's "pushy" guidance ("Use it whenever …", broad installable list incl. types 8/9 that the old text omitted: MCP/plugins/skills, OAuth integrations, curl-pipe installers) while adding near-miss exclusions that drive false triggers in coding sessions. Re-audit trigger mirrors the report's own "Re-audit on major version bump or maintainer change". Minor/patch bumps deliberately not excluded (compromised patch releases are a known supply-chain vector; "err on the side of caution"). "Mandatory" dropped — the gate is conveyed by "before … enters"; the word pushed blanket triggering. 834 chars (old 737); parsed with PyYAML during planning.

**Verification:**
```bash
python3 - <<'EOF'
import re, yaml
t = open("SKILL.md", encoding="utf-8").read()
fm = yaml.safe_load(re.match(r"^---\s*\n(.*?)\n---", t, re.S).group(1))
d = fm["description"]
assert fm["name"] == "install-auditor" and len(d) <= 1024 and "<" not in d and ">" not in d
assert "APPROVED/CONDITIONAL/REJECTED" in d and "PASS" not in d and "FAIL" not in d
assert "npm/pip/cargo/gem/go/nuget/maven" in d
print(len(d), "ok")
EOF
```
(`yaml` = PyYAML; present on this host. Absent → `python3 evals/run_evals.py validate` still proves `name:` parses.) Optional: skill-creator `scripts/quick_validate.py` on a clean export (`git archive HEAD | tar -x -C <tmp>`; the repo dir itself fails its single-`SKILL.md` rule because `.projexwt/` worktrees hold other `SKILL.md` files).

**If this fails:** restore lines 1–12 from `git show HEAD:SKILL.md`.

---

### Step 5: Fix `references/criteria.md` stale Step pointer

**Objective:** Point Audit Coverage requirement at the real report section.
**Confidence:** High
**Depends on:** Steps 1–2
**Do-Projex:** Encouraged

**Files:** `references/criteria.md` (L15 only)

**Changes:**

```markdown
// Before:
Reports must include an **Audit Coverage** table (see `SKILL.md` Step 6). Row labels below …
// After:
Reports must include an **Audit Coverage** table (see `SKILL.md` Step N → Report; Tier 2/3 skeleton in `references/report-template.md`). Row labels below …
```

Only the parenthetical changes; rest of the line byte-identical.

**Verification:** `grep -c 'Step 6' references/criteria.md` → 0; `git diff -U0 references/criteria.md | grep -c '^@@'` → 1.

**If this fails:** `git checkout -- references/criteria.md`.

---

### Step 6: Ship trigger eval set + STEWARDSHIP pointer

**Objective:** Make description changes testable with skill-creator's `run_eval.py` / `run_loop.py` (format: JSON array of `{query, should_trigger}`).
**Confidence:** High
**Depends on:** Step 4
**Do-Projex:** Encouraged

**Files:** `evals/trigger-evals.json` (new), `STEWARDSHIP.md`

**Changes:** `evals/trigger-evals.json`, exact content (UTF-8, trailing newline):

```json
[
  {"query": "can you add zod to the api package? I want schema validation on the POST /orders handler in src/routes/orders.ts", "should_trigger": true},
  {"query": "found a chrome extension called JSON Viewer Pro that pretty-prints API responses — ok to put it on my work laptop?", "should_trigger": true},
  {"query": "wire up the postgres MCP server from github.com/somedev/postgres-mcp in my claude config so you can query staging", "should_trigger": true},
  {"query": "bump react from 17 to 18 in apps/web and fix whatever breaks", "should_trigger": true},
  {"query": "their README says run curl -fsSL https://get.tooldev.sh/install.sh | sh to get the CLI. should I?", "should_trigger": true},
  {"query": "add peaceiris/actions-gh-pages to .github/workflows/deploy.yml so the docs publish on merge", "should_trigger": true},
  {"query": "pull bitnami/redis:latest and add it to docker-compose.yml for local dev", "should_trigger": true},
  {"query": "IT says we can self-install Insomnia with brew install --cask insomnia on our macs — anything to check before I do?", "should_trigger": true},
  {"query": "install the GitLens and Error Lens VS Code extensions in our .devcontainer/devcontainer.json for the team", "should_trigger": true},
  {"query": "our lead wants to connect Linear to the GitHub org through their OAuth app — what access does it get and is it safe?", "should_trigger": true},
  {"query": "npm install fails with ERESOLVE unable to resolve dependency tree after I pulled main — can you fix it?", "should_trigger": false},
  {"query": "just cloned the repo — run npm ci and then the jest suite and tell me what fails", "should_trigger": false},
  {"query": "pip install -r requirements.txt into the venv, then run pytest -k checkout", "should_trigger": false},
  {"query": "remove moment from package.json, switch the two call sites in src/utils/date.ts to Intl.DateTimeFormat, and update the lockfile", "should_trigger": false},
  {"query": "add our internal workspace package @acme/ui-tokens as a dependency of apps/web in the pnpm monorepo", "should_trigger": false},
  {"query": "change the cron in .github/workflows/nightly.yml to run at 02:00 UTC instead of midnight", "should_trigger": false},
  {"query": "how do I publish my own npm package with provenance enabled from GitHub Actions?", "should_trigger": false},
  {"query": "uninstall eslint-plugin-foo and delete its rules from .eslintrc.json", "should_trigger": false},
  {"query": "point npm at our internal Artifactory registry by editing .npmrc, keep the auth token in an env var", "should_trigger": false},
  {"query": "what is the difference between npm install and npm ci, and when should CI use each?", "should_trigger": false}
]
```

`STEWARDSHIP.md` § Running Evals — insert after the paragraph starting `New eval cases must carry` (base L69), separated by one blank line:

```markdown
Trigger evals: `evals/trigger-evals.json` (should / should-not trigger queries for the `SKILL.md` `description`). After editing the description, run skill-creator's `scripts/run_eval.py --eval-set evals/trigger-evals.json --skill-path .` (needs `claude -p` auth); add near-miss queries when a false trigger is reported.
```

**Rationale:** Negatives are near-misses sharing install vocabulary (skill-creator guidance), each matching an exclusion in the new description; positives cover all 9 subject types (registry twice: new dep + major upgrade). File is outside `evals.json` → `run_evals.py validate` and `prepare` (snapshot excludes `evals/`) unaffected.

**Verification:**
```bash
python3 -c "import json;d=json.load(open('evals/trigger-evals.json',encoding='utf-8'));assert len(d)==20 and all(set(x)=={'query','should_trigger'} for x in d) and sum(x['should_trigger'] for x in d)==10 and len({x['query'] for x in d})==20;print('ok')"
grep -c 'trigger-evals.json' STEWARDSHIP.md   # 1
```

**If this fails:** delete `evals/trigger-evals.json`; `git checkout -- STEWARDSHIP.md`.

---

## Verification Plan

### Automated Checks

- [ ] Per-step greps above all pass.
- [ ] `wc -c < SKILL.md` ≤ 15,300 and ≤ B0 − 1,800 (sim: 14,994 vs 17,093).
- [ ] `grep -c '\.ps1' SKILL.md` = 1; `grep -c 'python3 scripts/<script>.py' SKILL.md` = 1 (python-ports Step 5 invariant kept).
- [ ] `git diff -U0 HEAD -- SKILL.md | grep '^@@'` → hunks only in frontmatter (L1–12), the Report block, Reference Files. Explicit byte check of untouched regions:
  ```bash
  for h in '## Step 0' '### Dispatch Table' '## Step 1' '### Verdict Tree' '### Escalation' '### Red Flags' '### Behavioral Principles'; do
    diff <(git show HEAD:SKILL.md | awk -v h="$h" 'index($0,h)==1{f=1;print;next} f&&/^##/{exit} f') \
         <(awk -v h="$h" 'index($0,h)==1{f=1;print;next} f&&/^##/{exit} f' SKILL.md) >/dev/null && echo "same: $h" || echo "CHANGED: $h"
  done   # all "same"
  ```
- [ ] `git diff --stat HEAD -- workflows scripts evals/evals.json evals/run_evals.py` → empty.
- [ ] `python3 evals/run_evals.py validate` → exit 0, `41 evals, 248 assertions (82 deterministic, 166 model-graded)`.
- [ ] `python3 -m unittest discover -s evals -p "test_*.py"` → OK.
- [ ] After `git add references/report-template.md evals/trigger-evals.json` (or commit): `python3 evals/run_evals.py prepare --workspace <tmp-outside-repo> --ids 0` → `<tmp>/iteration-1/skill-snapshot/references/report-template.md` exists; delete `<tmp>` afterwards.
- [ ] `git diff --check` clean.

### Manual Verification

- [ ] Read rendered `SKILL.md` Step N: Report → Escalation → Red Flags order; Quick skeleton fence closes before `### Escalation`.
- [ ] Offline grader probe (reuse the `prepare --ids 0` workspace): hand-write `audit-express-4.21.2.md` from the Quick skeleton (verdict `**Verdict: APPROVED ✅**`, 4 coverage rows) into `<tmp>/iteration-1/eval-0/with_skill/run-1/outputs/.install-audits/` and a one-line `<tmp>/iteration-1/eval-0/with_skill/run-1/response.md` → `python3 evals/run_evals.py grade --workspace <tmp>` → eval 0 `grading.json` deterministic 3/3 pass (`exact_match`, `file_exists`, `line_count_max`). Delete `<tmp>` afterwards.
- [ ] Optional (needs `claude -p` auth): skill-creator `run_eval.py` with `evals/trigger-evals.json`; record per-query trigger rates in the execution log; not a gate.

### Acceptance Criteria Validation

| Criterion | How to Verify | Expected Result |
|-----------|---------------|-----------------|
| Full template file | Step 1 greps | 3 contract strings; only header mentions Tier 1; no `.ps1` |
| Report section + Quick skeleton | Step 2 greps/awk | `### Report`; fence ≤ 40 lines; no old heading |
| Default location | `grep '.install-audits/'` | present; `audit-<package-name>` absent |
| `.ps1` residue | `grep -c '\.ps1' SKILL.md` | 1 |
| Reference Files | Step 3 loop + count | no MISSING; 8 bullets; script bullet same |
| Size | `wc -c` | ≤ 15,300 and ≤ B0 − 1,800 |
| Frontmatter | Step 4 script | `ok` |
| criteria.md pointer | grep | no `Step 6` |
| Trigger set | Step 6 one-liner | `ok` |
| Harness compat | validate + unittest + prepare + grade probe | exit 0 / OK / file present / 3/3 |
| Untouched regions | region diff loop + diff --stat | all "same"; empty stat |

---

## Rollback Plan

1. Abandon ephemeral branch (`projex-abandon`): all changes are on it.
2. Partial: `git checkout -- SKILL.md references/criteria.md STEWARDSHIP.md`; delete `references/report-template.md`, `evals/trigger-evals.json`. Steps 4 and 6 (description + trigger set) are independent of Steps 1–3/5 and can be kept or dropped alone.

---

## Notes

### Risks

- **Agents skip reading `references/report-template.md` on Tier 2/3** → reports in Quick shape. Mitigation: Shape line names the file; eval-runner `contains_string "## Audit Coverage"` still passes either way; reviewers see `Audit tier: Standard|Deep`. A later eval could assert Security/Reliability sections on a Tier 2 case.
- **Two skeletons drift** (shared lines: verdict line, Audit Coverage heading + confidence line, first 3 coverage rows). Mitigation: template header states the identity rule; Acceptance greps check the 3 contract strings in both. Consider a STEWARDSHIP check later.
- **Description under-triggers** on phrasings like "set up X" without "install/add". Mitigation: broad installable list + "is about to add"; trigger set includes "wire up", "pull", "connect", "bump" phrasings; run `run_eval.py` when auth exists.
- **`.install-audits/` still appears in `git status`** as one untracked folder. Accepted (contained, deliberate, versioned evidence); the closing chat message names the path; users choose commit vs ignore.
- **python-ports close changes the script bullet or L87 differently than its plan** → Step 3 copies the bullet from the file, not from this plan; Preflight count catches a missing merge.
- **Slug collisions** (`@a/b-c` vs `a-b/c`) → same filename; rare; overwrite of an audit of a different subject would lose evidence. Accepted; report header names the exact subject.

### Split Decision

`No split — heuristic tripped but scope set by orchestrator (rationale: ~600 lines / ~42 KB and 6 steps trips the size heuristic; the orchestrator asked for one plan covering items 6, 7b, 7c; all files in root `.projex` scope; no upstream/downstream mix; much of the length is paste-ready final text, not extra work).` Separable slice if the orchestrator prefers: Steps 4 + 6 (description + trigger set) touch only frontmatter, `evals/trigger-evals.json`, `STEWARDSHIP.md` and depend on nothing in Steps 1–3/5 — can be executed or reverted alone without edits.

### Open Questions

(none)
