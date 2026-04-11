# Transitive Dependency Scanning (registry-package v1)

> **Status:** Complete
> **Completed:** 2026-04-12
> **Walkthrough:** 2604110900-transitive-dep-scan-walkthrough.md
> **Created:** 2026-04-11
> **Author:** Claude (Sonnet 4.6)
> **Source:** 2604021203-transitive-dependency-auditing-proposal.md
> **Related Projex:** 2604021203-transitive-dependency-auditing-proposal.md, 2604070218-install-auditor-subject-typed-redesign-nav.md (Phase 2 M2.4)
> **Worktree:** No

---

## Summary

Add `scripts/dep-scan.ps1` to scan direct (Tier 2) or full transitive (Tier 3) dependencies
for known CVEs via the OSV batch API — no package installation required. Replace the
aspirational `npm audit` / `pip-audit` references in `§4.3 Transitive dependency risk`
and `references/criteria/registry-package.md` §Transitive Dependency Guidance with a
structured, scripted check that produces citable output. Update `workflows/registry-package.md`
to invoke the script as an Evidence Part B step after `vuln-lookup.ps1`. Expand
`evals/evals.json` with a vulnerable-transitive-dep case and a clean Tier 2 dep-scan case.

**Scope:** `scripts/` (1 new file), `workflows/registry-package.md`,
`references/criteria/registry-package.md`, `references/criteria.md`, `evals/evals.json`.
No changes to `SKILL.md` or `workflows/generic.md`.

**Estimated Changes:** 1 new script (~280 lines), 4 document edits.

---

## Objective

### Problem / Gap / Need

`workflows/registry-package.md` §4.3 Subject Rubric "Transitive dependency risk" instructs:
"Run `npm audit` / `pip-audit` / equivalent. Flag HIGH+ CVEs in transitive dependencies."
Both tools require the package to be *installed* first — which directly contradicts the
core requirement of auditing *before* installation. `references/criteria/registry-package.md`
"Transitive Dependency Guidance" §Tier applicability repeats the same aspirational
references with no script path. The Audit Coverage "Transitive dependencies" row has no
structured source to cite — the agent either skips it or fills in a vague impression.

The OSV batch API (`POST /v1/querybatch`) supports up to 1,000 package queries per call.
Registry metadata APIs (npm `registry.npmjs.org`, PyPI `pypi.org/pypi`) expose direct
dependency lists without installation. For Tier 3 (npm), a temp `package.json` +
`npm install --package-lock-only --ignore-scripts` resolves the full dependency tree
without touching the user's project. Direct deps → OSV batch = installation-free,
reproducible, citable.

### Success Criteria

- [ ] `dep-scan.ps1 -Ecosystem npm -Name "coffee-script" -Version "1.12.0" -Tier 2` prints
  valid JSON with `riskLevel: "high"` or `"critical"` and `findings` containing `minimist`
  with CVE-2020-7598 (coffee-script@1.12.0 depends directly on minimist@0.0.8).
- [ ] `dep-scan.ps1 -Ecosystem npm -Name "express" -Tier 2` prints valid JSON with
  `riskLevel: "none"` or `"low"` (no critical transitive CVEs in current version).
- [ ] `dep-scan.ps1 -Ecosystem pypi -Name "requests" -Tier 2` prints valid JSON (PyPI
  direct-dep resolution path).
- [ ] `dep-scan.ps1 -Ecosystem npm -Name "<package>" -Tier 3` performs full tree scan when
  `npm` is available, or degrades to Tier 2 with `fallback: true` when it isn't.
- [ ] `workflows/registry-package.md` Evidence Part B invokes `dep-scan.ps1` after
  `vuln-lookup.ps1`, with tier-conditioned invocation for Tier 2 and Tier 3.
- [ ] Audit Coverage "Transitive dependencies" row guidance cites `dep-scan.ps1` output format.
- [ ] `references/criteria/registry-package.md` "Transitive Dependency Guidance" section
  is replaced by a "Transitive Dependency Scanning" section with `dep-scan.ps1` invocation,
  output fields table, risk-level-to-verdict table, and audit coverage row guidance. No
  remaining `npm audit` / `pip-audit` references.
- [ ] `references/criteria.md` §4.3 has a "Transitive Dependency Scan (registry packages)"
  subsection cross-referencing `dep-scan.ps1`.
- [ ] `evals/evals.json` contains ids 7 and 8; ids 0–6 unchanged.

### Out of Scope

- Tier 3 full-tree resolution for PyPI, crates.io, Go, etc. — deferred to v2 (requires
  separate package manager support; Tier 2 covers the direct-dep surface).
- Reachability analysis — flag all HIGH/CRITICAL in the dep tree; leave reachability
  judgment to the human reviewer.
- Merging logic into `vuln-lookup.ps1` or `registry-lookup.ps1` — composable scripts preferred.
- Changes to `SKILL.md` or `workflows/generic.md`.

---

## Context

### Current State

`workflows/registry-package.md` §4.3 "Transitive dependency risk": "Run `npm audit` /
`pip-audit` / equivalent. Flag HIGH+ CVEs in transitive dependencies. See transitive
guidance in criteria addendum." No script invocation. `references/criteria/registry-package.md`
"Transitive Dependency Guidance" tier applicability: Tier 2 = "Run `npm audit` / `pip-audit`
/ equivalent"; Tier 3 = "Manual review + automated scan of full tree; flag single-maintainer
critical transitives." Both require installation. `evals/evals.json` has 7 cases (ids 0–6);
none exercise dep-scan behavior.

### Key Files

| File | Role | Change Summary |
|---|---|---|
| `scripts/dep-scan.ps1` | New tool | Direct + transitive dep scan via OSV batch API; installation-free; 24-hr cache; JSON stdout |
| `.gitignore` | Cache exclusion | Add `scripts/.dep-scan-cache/` |
| `workflows/registry-package.md` | Registry-package workflow | Add dep-scan invocation in Evidence Part B; update coverage row guidance; update §4.3 transitive risk bullet |
| `references/criteria/registry-package.md` | Per-subject criteria addendum | Replace "Transitive Dependency Guidance" section with "Transitive Dependency Scanning" section + verdict table |
| `references/criteria.md` | Shared rubric core | Add "Transitive Dependency Scan (registry packages)" subsection in §4.3 |
| `evals/evals.json` | Regression prompts | Add ids 7 and 8 |

### Dependencies

- **Requires:** M2.3 complete (✓ `vuln-lookup.ps1` establishes the OSV query pattern, cache
  convention, and `riskLevel` vocabulary this script follows).
- **Blocks:** Phase 2 M2.5 (eval gate) — depends on dep-scan being in place.

### Constraints

- Script must never install the audited package — all data sourced from registry HTTP APIs
  and `npm install --package-lock-only --ignore-scripts` in a temp dir (Tier 3 npm only).
- Tier 3 must degrade gracefully to Tier 2 when `npm` is unavailable, with `fallback: true`
  and `fallbackReason` in JSON output.
- `riskLevel` vocabulary must match `vuln-lookup.ps1`'s: `none` / `low` / `medium` /
  `high` / `critical`.
- Audit Coverage row label must match the canonical label in `references/criteria.md`
  Audit Coverage Checklist.
- No changes to `SKILL.md` — dispatcher stays subject-agnostic.

### Assumptions

- OSV `/v1/querybatch` accepts an array of `{package: {ecosystem, name}, version}` queries
  (up to 1,000) and returns `{results: [{vulns: [...]}, ...]}` in matching order.
- npm registry API (`registry.npmjs.org/<name>/<version>`) returns a `dependencies` map
  for the requested version manifest.
- PyPI JSON API (`pypi.org/pypi/<name>[/<version>]/json`) returns `requires_dist` strings
  from which dep names can be parsed (e.g., `"requests>=2.0"` → name `"requests"`).
- `npm install --package-lock-only --ignore-scripts` in a temp dir resolves the full tree
  to `package-lock.json` without executing install scripts or modifying the user's project.
  Requires npm 6+; fail gracefully with `fallbackReason: "npm CLI unavailable or too old"`
  if the command isn't found or returns a non-zero exit. **Verify in Step 1** before
  finalizing the T3 implementation.
- `.gitignore` cache entry follows the same pattern as `.vuln-cache/` added in M2.3.
- `coffee-script@1.12.0` lists `minimist@0.0.8` as a direct dependency in its npm manifest,
  and `minimist@0.0.8` has CVE-2020-7598 in OSV at execution time. **Verify both in Step 5**
  before finalizing eval id 7 — if the dep relationship or CVE has changed, substitute a
  confirmed vulnerable package+version pair.

### Impact Analysis

- **Direct:** `scripts/dep-scan.ps1` (new), `workflows/registry-package.md` (evidence
  + coverage + §4.3 rubric), `references/criteria/registry-package.md` (section
  replacement), `references/criteria.md` (one subsection), `evals/evals.json` (2 entries).
- **Adjacent:** Agents dispatching to `workflows/registry-package.md` will start invoking
  `dep-scan.ps1` as part of the updated Tier 2/3 Evidence steps.
- **Downstream:** Eval runner exercising evals 7 and 8 requires the updated workflow +
  script. M2.5 eval gate depends on this milestone being complete.

---

## Implementation

### Overview

Five sequential steps. Steps 2–4 depend on Step 1 (prose must reference the script's
actual parameter names and output fields). Steps 2 and 3 can execute in either order
after Step 1. Step 4 (criteria.md) depends on Step 3 (subsection name used there).
Step 5 is last — eval assertions only meaningful once workflow and criteria are in place.

---

### Step 1: Create `scripts/dep-scan.ps1`

**Objective:** New PowerShell script performing installation-free dependency vulnerability scan.
**Confidence:** High — OSV batch endpoint is documented; same `Invoke-RestMethod` cache
pattern as `vuln-lookup.ps1`; npm `--package-lock-only` flag is stable.
**Depends on:** None.

**Files:**
- `scripts/dep-scan.ps1` (create, ~280 lines)
- `.gitignore` (add `scripts/.dep-scan-cache/`)

**Script design:**

```powershell
<#
.SYNOPSIS
  Scans direct (Tier 2) or full transitive (Tier 3, npm only) dependencies for known
  CVEs via the OSV batch API. Never installs the audited package.
.PARAMETER Ecosystem
  ValidateSet: npm, pypi, crates, rubygems, nuget, go, maven, hex
.PARAMETER Name
  Target package name (required).
.PARAMETER Version
  Target package version (optional). Selects the correct version manifest when fetching deps.
.PARAMETER Tier
  2 (default) — scan direct deps from registry metadata.
  3 — resolve full dep tree (npm: package-lock-only in temp dir), then batch-scan;
      falls back to Tier 2 with fallback:true if npm CLI unavailable.
.OUTPUTS
  JSON to stdout:
  {
    ecosystem, package, version?,
    tier,
    directDepCount,
    transitiveDepCount?,    # present and non-null for successful Tier 3 only
    findings: [             # HIGH and CRITICAL only; MEDIUM/LOW summarized in riskLevel
      { name, ecosystem, version, severity, cveIds[], depth }
      # depth: 1 = direct dep; 2+ = transitive (T3 only; always 1 for T2)
    ],
    mediumCount,            # count of MEDIUM-severity dep CVEs (not enumerated)
    lowCount,               # count of LOW-severity dep CVEs
    riskLevel,              # "none"|"low"|"medium"|"high"|"critical"
    fallback,               # true if Tier 3 fell back to Tier 2
    fallbackReason?,
    sources: ["OSV"],
    cacheHit
  }
  Cache: scripts/.dep-scan-cache/<eco>-<name>[-<ver>]-t<tier>.json, TTL 24 hr.
#>
param(
    [Parameter(Mandatory)]
    [ValidateSet('npm','pypi','crates','rubygems','nuget','go','maven','hex')]
    [string]$Ecosystem,
    [Parameter(Mandatory)][string]$Name,
    [string]$Version,
    [ValidateSet(2, 3)][int]$Tier = 2
)
```

**Key implementation notes:**

1. **Cache:** Same pattern as `vuln-lookup.ps1` — `Get-CachePath`, `Get-CachedResult`,
   `Set-CachedResult` helpers. Cache key: `<eco>-<name>[-<ver>]-t<tier>`.

2. **Fetch direct deps:**
   - **npm:** `GET https://registry.npmjs.org/<name>/<version|latest>` → `.dependencies`
     keys (devDependencies excluded; peerDependencies excluded from scan scope).
   - **PyPI:** `GET https://pypi.org/pypi/<name>[/<version>]/json` → `.info.requires_dist`
     array. Parse package name carefully: strip extras bracket first (`package[extra]` →
     `package`), then split on the first PEP 508 comparator or `;` marker. Bare names with
     no comparator (e.g., `"coverage;python_version<'3'"`) also need the `;` split.
   - **Other ecosystems:** Return `directDepCount: 0`, `findings: []`, note limitation in
     a `limitationNote` field. Do not error.

3. **Tier 3 npm full-tree resolution:**
   - Create temp dir via `[System.IO.Path]::GetTempPath()` + GUID
   - Write `{"dependencies": {"<name>": "<version|*>"}}`  to `package.json`
   - Run `npm install --package-lock-only --ignore-scripts --silent` in temp dir
   - Parse `package-lock.json` `packages` map to collect all `{name, version}` pairs
     (exclude `"" ` root entry; strip `node_modules/` prefix from keys)
   - On any failure (npm not found, non-zero exit, missing lock): set `fallback: true`,
     `fallbackReason`, proceed with Tier 2 direct-dep path
   - Remove temp dir in `finally` block

4. **OSV batch query:**
   ```
   POST https://api.osv.dev/v1/querybatch
   Content-Type: application/json
   Body: {"queries": [{"package": {"ecosystem": "<OSV-eco>", "name": "<dep>"}, "version": "<ver>"}, ...]}
   ```
   OSV ecosystem name mapping: reuse the mapping table already defined in `vuln-lookup.ps1`
   (npm→`npm`, pypi→`PyPI`, crates→`crates.io`, rubygems→`RubyGems`, nuget→`NuGet`,
   go→`Go`, maven→`Maven`, hex→`Hex`). Do not re-derive it.
   If query list > 1,000 entries: split into batches of 1,000, merge results.
   Response: `{"results": [{vulns: [...]}, ...]}` in matching query order.

5. **Severity and riskLevel:** Re-use same `Normalize-Severity` and `Get-RiskLevel`
   patterns from `vuln-lookup.ps1`. Enumerate findings only for HIGH and CRITICAL.
   Count MEDIUM and LOW separately. `riskLevel` is the maximum severity across all findings.

---

### Step 2: Update `workflows/registry-package.md`

**Objective:** Insert dep-scan invocation block after `vuln-lookup.ps1`; update §4.3
transitive bullet; update audit coverage row guidance; update tier-specific research scope.
**Confidence:** High — surgical edits, same pattern as M2.2 and M2.3.
**Depends on:** Step 1.

**Files:**
- `workflows/registry-package.md`

**Changes (4 targeted edits):**

**Edit A — Evidence Part B "How to research" block.** After the `vuln-lookup.ps1`
invocation block (ending with the "Audit Coverage CVE row" note), insert:

```
**Then run the transitive dependency scan** for Tier 2 and Tier 3 packages (skip for Tier 1):

For Tier 2 — direct deps only (default):
.\scripts\dep-scan.ps1 -Ecosystem <eco> -Name "<name>" [-Version "<version>"] -Tier 2

For Tier 3 — full tree (npm); falls back to Tier 2 if npm is unavailable:
.\scripts\dep-scan.ps1 -Ecosystem <eco> -Name "<name>" [-Version "<version>"] -Tier 3

Record `riskLevel`, `directDepCount`, and any HIGH/CRITICAL `findings` in the Audit
Coverage transitive dependencies row.
```

**Edit B — §4.3 Subject Rubric "Transitive dependency risk" bullet.** Replace:

> `Run \`npm audit\` / \`pip-audit\` / equivalent.`

With:

> `Run \`dep-scan.ps1 -Tier 2\` (Tier 2) or \`dep-scan.ps1 -Tier 3\` (Tier 3). Skip for Tier 1.`

Keep the trailing "See transitive guidance in criteria addendum" cross-reference.

**Edit C — Audit coverage tracking section.** Add guidance bullet for the
"Transitive dependencies" row:

```
- **Transitive dependencies row**: Reference `dep-scan.ps1` output — e.g.,
  `Done — dep-scan.ps1 T2: 8 deps, none HIGH+ (OSV)` or
  `Done — dep-scan.ps1 T2: 1 HIGH CVE in minimist@0.0.8 (CVE-2020-7598, OSV)`.
  If T3 fell back: note `T3→T2 fallback: <reason>`.
  For Tier 1: `Skipped — Tier 1 quick audit`.
```

**Edit D — Tier-specific research scope section.** Replace the Tier 2 and Tier 3
reference to `npm audit` / `pip-audit` with `dep-scan.ps1 -Tier 2` and
`dep-scan.ps1 -Tier 3` respectively.

---

### Step 3: Update `references/criteria/registry-package.md`

**Objective:** Replace the aspirational "Transitive Dependency Guidance" section with a
"Transitive Dependency Scanning" section that mirrors the "Multi-Database CVE Correlation"
section format: invocation, output fields table, risk-to-verdict table, coverage guidance.
**Confidence:** High — clean section replacement with well-defined boundaries.
**Depends on:** Step 1.

**Files:**
- `references/criteria/registry-package.md`

**Changes:**

Replace the entire "Transitive Dependency Guidance" section (from `## Transitive Dependency
Guidance` through the end of `### Tier applicability`) with:

```markdown
## Transitive Dependency Scanning

Run `scripts/dep-scan.ps1` to check direct (Tier 2) or full transitive (Tier 3, npm only)
dependencies for known CVEs via the OSV batch API. No package installation required.

### Invocation

```
# Tier 2 — direct deps from registry metadata (all ecosystems):
.\scripts\dep-scan.ps1 -Ecosystem <eco> -Name "<name>" [-Version "<version>"] -Tier 2

# Tier 3 — full tree resolution (npm only; auto-falls back to Tier 2):
.\scripts\dep-scan.ps1 -Ecosystem <eco> -Name "<name>" [-Version "<version>"] -Tier 3
```

Skip for Tier 1 packages.

### Output fields

| Field | Description |
|---|---|
| `directDepCount` | Number of direct dependencies resolved from registry API |
| `transitiveDepCount` | Full tree size (Tier 3 successful only; null otherwise) |
| `findings` | HIGH/CRITICAL deps: `[{name, ecosystem, version, severity, cveIds[], depth}]` — `depth` 1 = direct, 2+ = transitive (T3 only; always 1 for T2) |
| `mediumCount` / `lowCount` | Count of MEDIUM/LOW-severity dep CVEs (not enumerated) |
| `riskLevel` | Maximum severity across all findings: `none`/`low`/`medium`/`high`/`critical` |
| `fallback` | `true` if Tier 3 fell back to Tier 2 |
| `fallbackReason` | e.g. `"npm CLI unavailable"` or `"lock generation failed"` |

### Risk level → verdict impact

| `riskLevel` | Verdict guidance |
|---|---|
| `none` | Note "X deps checked, none with HIGH+ CVEs (OSV)" in transitive row. Proceed. |
| `low` | Note findings count. Does not change verdict alone. |
| `medium` | Note MEDIUM count. Soft CONDITIONAL signal if multiple findings in direct deps. |
| `high` | CONDITIONAL lean. Cite affected dep name(s) + CVE IDs. Condition: update to patched transitive version. |
| `critical` | Strong CONDITIONAL. Must cite dep name + CVE IDs. Immediate upgrade path required. |

**Transitive vs direct:** Use the `depth` field in each finding. A finding with `depth: 1`
(direct dep) carries the same verdict weight as a CVE in the package itself. A finding
with `depth > 1` (transitive) warrants a flag and citation but not automatic verdict
escalation — report it and let the reviewer weigh reachability. Tier 2 always emits
`depth: 1`; Tier 3 reflects actual tree depth.

### Depth thresholds

| Signal | Risk level | Action |
|---|---|---|
| `directDepCount` > 50 | Medium | Flag dependency bloat; increased attack surface |
| Any dep with `severity: CRITICAL` | Critical | Flag regardless of depth |
| Any dep with `severity: HIGH` in `findings` | High | Flag; cite CVE IDs |

### Audit coverage row guidance

For the **Transitive dependencies** row in the Audit Coverage table:

- `Done — dep-scan.ps1 T2: 8 deps, none HIGH+ (OSV)`
- `Done — dep-scan.ps1 T2: 1 HIGH CVE in minimist@0.0.8 (CVE-2020-7598, OSV)`
- `Done — dep-scan.ps1 T3: 12 direct, 147 transitive, riskLevel: none (OSV)`
- `Done — dep-scan.ps1 T3→T2 fallback (npm CLI unavailable): 8 deps, none HIGH+ (OSV)`
- `Skipped — Tier 1 quick audit`
```

---

### Step 4: Update `references/criteria.md`

**Objective:** Add "Transitive Dependency Scan (registry packages)" subsection in §4.3,
parallel to the "Vulnerability Database Lookup" subsection added in M2.3.
**Confidence:** High — additive insertion, defined location.
**Depends on:** Step 3 (subsection name in cross-reference must match).

**Files:**
- `references/criteria.md`

**Changes:**

In §4.3 Security Track Record, after the "Vulnerability Database Lookup (registry packages)"
subsection, insert:

```markdown
### Transitive Dependency Scan (registry packages)

Run `scripts/dep-scan.ps1` to check direct (Tier 2) or full transitive (Tier 3, npm only)
dependencies for known CVEs via the OSV batch API — no package installation required.
Invoke after `vuln-lookup.ps1` in the Evidence step for supported ecosystems. Tier 1
packages skip this step. Full risk-level-to-verdict guidance and output field reference
in `references/criteria/registry-package.md` §Transitive Dependency Scanning.
```

---

### Step 5: Update `evals/evals.json`

**Objective:** Add two cases exercising dep-scan: one where the package is clean itself but
has a vulnerable direct dependency (confirms dep-scan T2 detection path, distinct from
vuln-lookup), one clean Tier 2 package with real deps (confirms no false positives when
dep-scan T2 runs and returns clean).
**Confidence:** Medium — dep relationship and CVE state must be verified against live OSV
before committing.
**Depends on:** Steps 1–4.

**Files:**
- `evals/evals.json`

**Changes:**

Append ids 7 and 8 to the `evals` array. Ids 0–6 unchanged.

```json
{
  "id": 7,
  "prompt": "I want to use npm install coffee-script@1.12.0 for my build tooling. Is it safe?",
  "expected_output": "Tier 3 / Deep Audit (Slack source likely absent; but old, deprecated package + low downloads = Tier 3 or Tier 2). coffee-script@1.12.0 itself has no direct CVEs but depends on minimist@0.0.8 which has CVE-2020-7598 (prototype pollution). dep-scan.ps1 should flag the minimist dep with HIGH riskLevel. vuln-lookup.ps1 should return clean for coffee-script itself. Verdict CONDITIONAL with dep CVE cited in report. Transitive dependencies row references dep-scan.ps1 output.",
  "files": [],
  "assertions": [
    {"text": "dep-scan.ps1 invoked OR transitive/dependency scan explicitly performed", "type": "contains_concept"},
    {"text": "minimist or CVE-2020-7598 or prototype pollution mentioned as a dependency vulnerability", "type": "contains_concept"},
    {"text": "Verdict is CONDITIONAL or REJECTED", "type": "verdict_check"},
    {"text": "## Audit Coverage", "type": "contains_string"},
    {"text": "Audit confidence", "type": "contains_concept"}
  ]
},
{
  "id": 8,
  "prompt": "Can I npm install chalk@5.3.0 for terminal color output in my CLI tool?",
  "expected_output": "Tier 1 or Tier 2 audit. chalk@5.3.0 is a well-maintained package with a small number of clean direct dependencies. dep-scan.ps1 Tier 2 should run and return riskLevel: none. Verdict APPROVED. Verifies dep-scan T2 path runs on a real-dependency package and returns clean without false positives.",
  "files": [],
  "assertions": [
    {"text": "Verdict is APPROVED", "type": "exact_match"},
    {"text": "Report does not flag false transitive vulnerabilities for chalk", "type": "contains_concept"},
    {"text": "## Audit Coverage", "type": "contains_string"},
    {"text": "Audit confidence", "type": "contains_concept"}
  ]
}
```

**Before committing:** Verify both assumptions in Step 5:
1. `dep-scan.ps1 -Ecosystem npm -Name "coffee-script" -Version "1.12.0" -Tier 2` returns findings containing `minimist` with CVE-2020-7598.
2. `dep-scan.ps1 -Ecosystem npm -Name "chalk" -Version "5.3.0" -Tier 2` returns `riskLevel: "none"`.
If either assumption fails, substitute confirmed alternatives (e.g., id 7 → `grunt@0.4.5` which has known transitive CVEs; id 8 → `ms@2.1.3` which is a tiny clean utility with no deps).

---

## Acceptance Criteria

| Check | Pass condition |
|---|---|
| Script exits cleanly | `dep-scan.ps1 -Ecosystem npm -Name "express" -Tier 2` exits 0, valid JSON |
| T2 CVE detection | `dep-scan.ps1 -Ecosystem npm -Name "coffee-script" -Version "1.12.0" -Tier 2` → `riskLevel: "high"` or `"critical"`, `findings` contains `minimist` |
| T3 fallback | `dep-scan.ps1 ... -Tier 3` with npm unavailable → `fallback: true`, exit 0 |
| PyPI direct-dep path | `dep-scan.ps1 -Ecosystem pypi -Name "requests" -Tier 2` → valid JSON |
| Cache hit | Second invocation of same params returns faster with `cacheHit: true` |
| Workflow invocation present | Evidence Part B has `dep-scan.ps1` block after `vuln-lookup.ps1` block |
| §4.3 rubric updated | "Transitive dependency risk" bullet no longer references `npm audit` / `pip-audit` |
| Coverage row guided | Audit Coverage tracking section has `dep-scan.ps1` row format guidance |
| Criteria addendum updated | "Transitive Dependency Scanning" section present with output fields table + verdict table; no `npm audit` / `pip-audit` references remain |
| Criteria core updated | §4.3 has "Transitive Dependency Scan (registry packages)" subsection |
| Evals added | ids 7 + 8 present in evals array; ids 0–6 unchanged |
| Cache excluded | `.dep-scan-cache/` present in `.gitignore` |

---

## Rollback

1. Delete `scripts/dep-scan.ps1`.
2. Remove `scripts/.dep-scan-cache/` line from `.gitignore`.
3. Revert `workflows/registry-package.md`: remove dep-scan invocation block (Edit A);
   restore §4.3 transitive bullet to `Run \`npm audit\` / \`pip-audit\` / equivalent`
   (Edit B); remove dep-scan coverage row guidance (Edit C); restore tier-scope lines
   (Edit D).
4. Revert `references/criteria/registry-package.md`: restore original "Transitive
   Dependency Guidance" section (depth-thresholds table + tier applicability with
   `npm audit` / `pip-audit` references).
5. Revert `references/criteria.md`: remove "Transitive Dependency Scan" subsection
   from §4.3.
6. Revert `evals/evals.json` to 7 entries (ids 0–6).

---

## Revision History

| Date | Change |
|---|---|
| 2026-04-11 | Draft created |
| 2026-04-11 | Revised after in-place review: eval id 7 changed from minimist@0.0.8 (direct CVE, wrong path) to coffee-script@1.12.0 (clean package with vulnerable dep minimist@0.0.8); eval id 8 changed from has-flag@4.0.0 (zero-dep Tier 1, skips dep-scan) to chalk@5.3.0 (Tier 2 with real clean deps); `depth` field added to findings schema and verdict guidance; PyPI extras/marker parsing complexity noted; OSV ecosystem mapping delegated to vuln-lookup.ps1 table; npm 6+ requirement added to Assumptions |
