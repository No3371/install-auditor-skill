# M6.2 — Hybrid-Subject Eval Cases

> **Status:** Complete
> **Created:** 2026-04-17
> **Completed:** 2026-04-17
> **Author:** Claude (Opus 4.6)
> **Source:** Direct request — nav M6.2 milestone
> **Nav:** 2604070218-install-auditor-subject-typed-redesign-nav.md
> **Related Projex:** 2604171500-per-workflow-eval-bundles-m61-plan.md (predecessor), 2604070300-install-auditor-subject-type-taxonomy-def.md (classifier rule source)
> **Walkthrough:** 2604171700-hybrid-subject-eval-cases-m62-walkthrough.md
> **Worktree:** No

---

## Summary

Add eval cases to `evals/evals.json` that exercise the "innermost trust boundary" classifier rule for hybrid/ambiguous subjects. These cases test that the dispatcher correctly identifies the innermost boundary and routes to the right workflow, rather than misrouting to an outer wrapper type or a naive surface-level match.

**Scope:** 5 new eval cases (ids 36-40) in `evals/evals.json` — one per worked hybrid example in the taxonomy def's classifier section.
**Estimated Changes:** 1 file, ~90 lines appended.

---

## Objective

### Problem / Gap / Need

Existing 36 evals (ids 0-35) test single-type classification — each subject clearly maps to one type. None exercise the classifier's hybrid-subject resolution logic. The innermost trust boundary rule (taxonomy def M0.2) has 5 worked examples but zero eval coverage. A misclassification regression for hybrid subjects would go undetected.

### Success Criteria

- [ ] `evals/evals.json` contains 41 cases (ids 0-40), sequential, no duplicates
- [ ] 3 canonical hybrid cases from nav spec present: npm-distributed CLI, container-wrapped npm app, VS Code extension wrapping binary
- [ ] 2 additional hybrid cases from taxonomy worked examples: GitHub Action pulling Docker, Claude Code skill via npm
- [ ] Each hybrid case has assertion testing correct innermost-boundary type classification
- [ ] Each hybrid case has assertion testing that the wrong outer-type is NOT the classification
- [ ] All cases are structurally valid JSON (parseable, correct field schema)

### Out of Scope

- Running or validating eval cases against the live skill (no eval runner yet)
- Modifying the classifier rule, taxonomy def, or any workflow file
- Adding non-hybrid eval cases
- Eval runner tooling (remains deferred per nav)

---

## Context

### Current State

`evals/evals.json`: 36 cases (ids 0-35). All 10 workflows at >=3 cases (M6.1 complete). Three generic-fallback cases (ids 33-35) test low-confidence scenarios. No hybrid-subject cases exist.

The taxonomy def's "Worked hybrid examples" section defines 5 canonical hybrids with expected classifications:

| # | Hybrid | Outer type | Correct innermost type | Confidence |
|---|--------|-----------|----------------------|------------|
| 1 | npm package whose `bin` ships a CLI | cli-binary (7) | **registry-package (1)** | high |
| 2 | VS Code extension wrapping a binary | cli-binary (7) | **ide-plugin (3)** | high |
| 3 | Docker image whose entrypoint is npm app | registry-package (1) | **container-image (4)** | high |
| 4 | GitHub Action that pulls Docker internally | container-image (4) | **ci-action (5)** | high |
| 5 | Claude Code skill distributed via npm | agent-extension (8) | **registry-package (1)** | high |

### Key Files

| File | Role | Change Summary |
|------|------|----------------|
| `evals/evals.json` | Eval case registry | Append 5 hybrid cases (ids 36-40) |

### Dependencies

- **Requires:** M6.1 complete (ids 0-35 present) — confirmed 2026-04-17
- **Blocks:** Nothing — M6.3 is independent

### Constraints

- IDs must be sequential (next = 36)
- JSON must parse cleanly — trailing comma discipline
- Assertion types limited to existing vocabulary: `contains_concept`, `exact_match`, `contains_string`, `verdict_check`, `file_exists`, `line_count_max`

### Assumptions

- The 5 worked hybrid examples in the taxonomy def are the canonical set; no additional hybrid patterns warrant eval coverage at this time
- Each hybrid case should be high-confidence classification (per taxonomy def) — they test that the classifier gets it RIGHT, not that it falls back to generic

### Impact Analysis

- **Direct:** `evals/evals.json` — 5 new entries
- **Adjacent:** None — eval cases are data-only
- **Downstream:** Future eval runner will execute these cases

---

## Implementation

### Overview

Append 5 eval cases to `evals/evals.json`, one per taxonomy worked hybrid example. Each case uses a realistic user prompt that surfaces the hybrid ambiguity, and assertions that validate both (a) correct innermost-type classification and (b) that the report addresses the hybrid nature.

### Step 1: Add 5 hybrid eval cases to evals.json

**Objective:** Append ids 36-40 to the `evals` array.
**Confidence:** High
**Depends on:** None

**Files:**
- `evals/evals.json`

**Changes:**

Append after id 35's closing `}` (before the final `]}`):

```json
    {
      "id": 36,
      "prompt": "I want to install Prettier for code formatting — npm install -g prettier. I know it installs a CLI binary. Should I think of this as a CLI tool audit or an npm package audit?",
      "expected_output": "Routes to registry-package workflow (Type 1), not cli-binary. The innermost trust boundary is the npm registry — the CLI binary exists only because npm delivered it. The trust gate is npm's publishing process; the binary is downstream. Standard/Tier 1 audit. Prettier is high-trust (massive downloads, well-known maintainers). Verdict APPROVED.",
      "files": [],
      "assertions": [
        {"text": "Subject type is registry-package", "type": "contains_concept"},
        {"text": "Report routes to registry-package workflow, not cli-binary", "type": "contains_concept"},
        {"text": "Report explains innermost trust boundary is npm registry", "type": "contains_concept"},
        {"text": "Verdict is APPROVED", "type": "exact_match"},
        {"text": "Report is saved to a .md file", "type": "file_exists"},
        {"text": "## Audit Coverage", "type": "contains_string"}
      ]
    },
    {
      "id": 37,
      "prompt": "I want to install the rust-analyzer VS Code extension. I know it downloads a native binary (the LSP server) under the hood. Should this be audited as a binary download or as a VS Code extension?",
      "expected_output": "Routes to ide-plugin workflow (Type 3), not cli-binary. The innermost trust boundary is the VS Code Marketplace — the user clicks 'Install' in VS Code, and the marketplace is the verification layer. The bundled LSP binary is downstream, audited under the ide-plugin rubric. Standard/Tier 1 audit. rust-analyzer is well-known, high installs, active maintainers. Verdict APPROVED.",
      "files": [],
      "assertions": [
        {"text": "Subject type is ide-plugin", "type": "contains_concept"},
        {"text": "Report routes to ide-plugin workflow, not cli-binary", "type": "contains_concept"},
        {"text": "Report explains innermost trust boundary is VS Code Marketplace", "type": "contains_concept"},
        {"text": "Report mentions the bundled binary is audited within the ide-plugin rubric", "type": "contains_concept"},
        {"text": "Verdict is APPROVED", "type": "exact_match"},
        {"text": "## Audit Coverage", "type": "contains_string"}
      ]
    },
    {
      "id": 38,
      "prompt": "Our team publishes a Node.js microservice as a Docker image on Docker Hub: docker pull acmecorp/invoice-api. The image is just an Express app with npm dependencies baked into the layer. Should I audit the npm packages or the Docker image?",
      "expected_output": "Routes to container-image workflow (Type 4), not registry-package. The innermost trust boundary is the container registry — the user runs docker pull, and Docker Hub is the trust gate the user personally crosses. The npm packages inside are audited as a sub-step within the container-image workflow if they warrant separate attention. Tier 2 audit. Verdict CONDITIONAL (review image provenance, Dockerfile best practices, and whether baked-in npm dependencies introduce known vulnerabilities).",
      "files": [],
      "assertions": [
        {"text": "Subject type is container-image", "type": "contains_concept"},
        {"text": "Report routes to container-image workflow, not registry-package", "type": "contains_concept"},
        {"text": "Report explains innermost trust boundary is the container registry", "type": "contains_concept"},
        {"text": "Report mentions npm dependencies as sub-step or secondary concern", "type": "contains_concept"},
        {"text": "Verdict is APPROVED or CONDITIONAL", "type": "verdict_check"},
        {"text": "## Audit Coverage", "type": "contains_string"}
      ]
    },
    {
      "id": 39,
      "prompt": "I want to use the docker/build-push-action GitHub Action in our CI pipeline. I see it pulls a Docker image internally to do the build. Should I audit the Docker image or the GitHub Action itself?",
      "expected_output": "Routes to ci-action workflow (Type 5), not container-image. The innermost trust boundary is the GitHub Actions marketplace — the user writes `uses: docker/build-push-action@v5` in their workflow file. The Docker image pulled internally is an implementation detail covered by the ci-action workflow's transitive-action surface analysis. Tier 1/2 audit. docker/build-push-action is a Docker-verified, widely-used action. Verdict APPROVED.",
      "files": [],
      "assertions": [
        {"text": "Subject type is ci-action", "type": "contains_concept"},
        {"text": "Report routes to ci-action workflow, not container-image", "type": "contains_concept"},
        {"text": "Report explains innermost trust boundary is the GitHub Actions marketplace", "type": "contains_concept"},
        {"text": "Report mentions Docker image as implementation detail or transitive concern", "type": "contains_concept"},
        {"text": "Verdict is APPROVED", "type": "exact_match"},
        {"text": "## Audit Coverage", "type": "contains_string"}
      ]
    },
    {
      "id": 40,
      "prompt": "I found a Claude Code skill on npm — npm install -g @anthropic/some-code-skill. It contains SKILL.md and scripts/. Should I audit this as a Claude Code skill (agent-extension) or as an npm package?",
      "expected_output": "Routes to registry-package workflow (Type 1), not agent-extension. The innermost trust boundary is the npm registry — the user runs npm install, so npm's publishing process is the trust gate. The skill content (SKILL.md, scripts/) is downstream and audited within the registry-package workflow. The workflow may invoke agent-extension sub-rubric signals for the skill content if warranted. Tier 2 audit. Verdict CONDITIONAL (skill content requires review of capability scope, but install gate is npm).",
      "files": [],
      "assertions": [
        {"text": "Subject type is registry-package", "type": "contains_concept"},
        {"text": "Report routes to registry-package workflow, not agent-extension", "type": "contains_concept"},
        {"text": "Report explains innermost trust boundary is npm registry", "type": "contains_concept"},
        {"text": "Report mentions skill content as downstream concern", "type": "contains_concept"},
        {"text": "Verdict is CONDITIONAL or APPROVED", "type": "verdict_check"},
        {"text": "## Audit Coverage", "type": "contains_string"}
      ]
    }
```

**Rationale:** Each case maps 1:1 to a taxonomy worked hybrid example. Prompts are written to explicitly surface the hybrid ambiguity (user asks "should I treat this as X or Y?"), forcing the classifier to reason through the innermost-boundary rule rather than defaulting to surface-level keyword matching. Assertions test both positive routing (correct type) and negative routing (not the decoy type).

**Verification:** `node -e "JSON.parse(require('fs').readFileSync('evals/evals.json'))"` — must parse without error. Count entries: 41. Last id: 40.

**If this fails:** Revert evals.json to pre-edit state via git checkout.

---

## Verification Plan

### Automated Checks

- [ ] `evals/evals.json` parses as valid JSON
- [ ] 41 entries total with sequential ids 0-40
- [ ] No duplicate ids

### Manual Verification

- [ ] Each hybrid case prompt explicitly surfaces the dual-type ambiguity
- [ ] Each case's `expected_output` names the correct innermost type per taxonomy worked examples
- [ ] Each case has at least one assertion testing correct type classification
- [ ] Each case has at least one assertion testing the decoy type is not chosen

### Acceptance Criteria Validation

| Criterion | How to Verify | Expected Result |
|-----------|---------------|-----------------|
| 41 cases, sequential ids | `jq '.evals | length' evals/evals.json` | 41 |
| 3 nav-specified hybrids | Ids 36 (npm CLI), 37 (VS Code+binary), 38 (Docker+npm) | Present with correct types |
| 2 additional hybrids | Ids 39 (Action+Docker), 40 (skill via npm) | Present with correct types |
| Correct innermost type in assertions | Manual review of `contains_concept` assertions | Each names the right type |

---

## Rollback Plan

1. `git checkout -- evals/evals.json` — restores to M6.1 state (36 cases)

---

## Notes

### Risks

- **Prompt phrasing biases classifier:** Prompts explicitly mention both types, which could make classification "too easy." Mitigation: this is intentional for v1 — the prompts test that the rule is applied, not that the classifier can infer type from minimal context. Harder "stealth hybrid" cases can follow in M6.3.

### Open Questions

None.
