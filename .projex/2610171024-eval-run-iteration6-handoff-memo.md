# Memo: Eval run iteration-6 results + handoff of open work

> **Status:** Draft
> **Author:** Claude (Opus), orchestrator
> **Parent:** Orchestrator
> **Source Type:** Deferred
> **Origin:** Orchestrated session 2026-10-16/17 ("What can we do to improve this?" → "orchestarte it" → "handoff")
> **Related Projex:** 2604070218-install-auditor-subject-typed-redesign-nav.md, 2610170504-eval-suite-refresh-walkthrough.md, 2610170541-stewardship-review-pass-record-patch.md

---

## Source

User, verbatim: "handoff". Session stopped after the first live eval run (STEWARDSHIP checklist step 4) and before the proposed fix plan. Results below are copied here because the eval workspace (`../install-auditor-skill-workspace/iteration-6/`, outside the repo) lives in an ephemeral container and will be lost.

### Done this session (all closed, on `claude/youthful-dijkstra-5ov1kt`)

- Rubric consistency + `references/classifier.md` (`2610161852-*`) | eval runner `evals/run_evals.py` (`2610161850-*`) | Python twins of lookup scripts (`2610161849-*`) | lean report template + `.install-audits/` + description retune (`2610161910-*`) | script bug fixes: typosquat baseline, OSV `introduced: "0"`, `.ps1` array unrolling (`2610161926-*`)
- Stewardship review pass: 5 review evals (`2610161927-*`, `2610161928-*`, now closed) → shared §4.6 version-integrity floor + Blocking-CVE rule (`2610161941-*`) → 10 subject refreshes (`26101620xx-*`) → cross-plan consistency (`2610170500-*`) → eval refresh 41→61 evals (`2610170504-*`) → STEWARDSHIP dates (`2610170541-*`)
- Human decisions in force: C4 "Allow Tier 1" (Docker Official Images) | C6 "Split by risk" (Blocking CVE = KEV-listed CRITICAL or unfixed HIGH/CRITICAL in own code) | registry "Relax: identity optional" for Tier 1 | full live run approved

### Live run iteration-6 (2026-10-17)

- 61/61 evals ran, 0 run errors. Audit cost $17.28 (estimate was $12–15). Model-grading cost not recorded by the harness.
- Assertions: **348/362 pass (96%)**, 14 failures in 13 evals.

| workflow | evals | passed/total |
|---|---|---|
| agent-extension | 7 | 42/43 |
| browser-extension | 5 | 30/30 |
| ci-action | 7 | 41/41 |
| cli-binary | 6 | 34/35 |
| container-image | 5 | 31/32 |
| desktop-app | 4 | 23/24 |
| generic | 3 | 18/18 |
| ide-plugin | 5 | 29/31 |
| registry-package | 13 | 67/73 |
| remote-integration | 6 | 33/35 |

Failures, grouped by orchestrator triage (not yet verified by a plan):

1. **Harness blocked scripts / proxy-blocked sources → coverage-gap CONDITIONALs** — evals 0, 5, 8, 18, 51. 52 Bash denials total; 23 were `cd <skill-snapshot> && python3 scripts/…`, which the `run` allowlist (`Bash(python3 <abs-snapshot>/scripts/:*)`) does not match. OSV/GHSA/some docs pages also blocked by the sandbox proxy. Auditors then added "run `npm audit`" conditions, contrary to `SKILL.md` Step N ("Do not change the verdict label for coverage alone").
2. **Hardening advice / MEDIUM accumulation turned into Conditions where APPROVED expected** — evals 16, 26, 37. Skill does not say clearly what belongs in Conditions vs Recommendation / Post-Install Checklist. Eval 26 report cited Redis own-code RCE CVEs (CVE-2026-81934, CVE-2026-23479) — unverified; if real and unfixed, CONDITIONAL may be correct and the eval assertion too strict.
3. **Eval wording** — eval 8 assertion 3 text is only "Audit confidence" (no expected content) | eval 24 "official Slack app" names no app → auditor treated vendor as unidentified | eval 40 package does not exist on npm → REJECTED is defensible, assertion allows only APPROVED/CONDITIONAL | eval 22 "transport and isolation" assertion too vague.

### Proposed next step (not started; user has not approved)

One plan, no live cost: (a) harness — allow the `cd <snapshot> && python3 scripts/…` form or instruct absolute-path invocation in the task prompt; (b) skill — coverage gaps and hardening advice go in Recommendation / checklist, never Conditions; (c) fix eval texts 8, 22, 24, 40 and re-judge 26 after verifying the Redis CVEs; (d) record results in the nav. Then optional re-run of the 13 failing evals (~$4; user approval needed).

---

## Context

- Other open follow-ups (also listed in nav § Known Blockers): Scorecard `api.scorecard.dev` response shape unverified (proxy 403) | chalk 5.6.1 advisory range verified only via secondary sources | registry tooling follow-on (PyPI provenance, RubyGems `-Version`, KEV flag) | trigger-eval live run (`evals/trigger-evals.json`) not done | Windows PowerShell 5.1 checked statically only.
- Next scheduled stewardship review: agent-extension 2026-12-15 (see `STEWARDSHIP.md`).
- Environment notes for the next session: `claude -p` authenticates in this cloud environment; no `pwsh` unless installed (official 7.4.6 tarball worked into the scratchpad); proxy blocks api.osv.dev, api.npmjs.org downloads, pypistats.org, Scorecard hosts. Framework quirks: `new-projex.sh` with absolute `--projex-dir` nests the file; `close-precheck.sh` needs repo-relative `Worktree Path`; `projex-tree.sh` lacks its `.projex-tree.py` helper; a harness guard once refused a subagent `Write` of `references/report-template.md`.
- No PR opened for `claude/youthful-dijkstra-5ov1kt`.
