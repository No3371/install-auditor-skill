# Execution Log: Transitive Dependency Scanning (registry-package v1)
Started: 20260411 09:00
Repo Root: C:/Users/BA/.claude/skills/install-auditor
Plan File: .projex/2604110900-transitive-dep-scan-plan.md
Base Branch: master

## Pre-Check Results
REPO_ROOT=C:/Users/BA/.claude/skills/install-auditor
BRANCH=master
PLAN_REL=.projex/2604110900-transitive-dep-scan-plan.md
WARN  Plan is not committed to branch 'master' - resolved by committing plan before proceeding
WARN  Working tree has 3 uncommitted change(s) - resolved by committing plan + nav; AGENTS.md unrelated to this execution

## Steps

### [20260411 09:10] - Step 1: Create scripts/dep-scan.ps1
**Action:** Created `scripts/dep-scan.ps1` (~260 lines). Added `scripts/.dep-scan-cache/` to `.gitignore`.
Script design: cache helpers (Get-CachePath/Get-CachedResult/Set-CachedResult, TTL 24hr), severity helpers
(Get-SeverityFromOsv/Normalize-Severity/Get-RiskLevel — same patterns as vuln-lookup.ps1), Get-NpmDeps
(registry.npmjs.org/<name>/<ver|latest> → .dependencies keys), Get-PypiDeps (pypi.org/pypi/<name>/json →
requires_dist parsing with extras+marker stripping), Get-NpmFullTree (npm install --package-lock-only in
temp dir, parsed package-lock.json v2/v1), Invoke-OsvBatch (POST /v1/querybatch, 1000-query chunking),
Get-DepFindings (HIGH/CRITICAL → findings with depth; MEDIUM/LOW → counters). Main: cache key
`<eco>-<name>[-<ver>]-t<tier>`, cache hit returns with cacheHit:true; Tier 3 attempts full tree then
falls back to Tier 2 on any failure with fallback:true + fallbackReason.
**Result:** File created. .gitignore updated.
**Status:** Success

### [20260412 09:30] - Step 2: Update workflows/registry-package.md
**Action:** Applied 4 targeted edits:
- Edit A: Inserted dep-scan invocation block (T2 + T3 code blocks) after the vuln-lookup review
  paragraph, before web search guidance.
- Edit B: §4.3 transitive bullet — replaced `npm audit` / `pip-audit` / equivalent with
  `dep-scan.ps1 -Tier 2` (Tier 2) or `dep-scan.ps1 -Tier 3` (Tier 3). Skip for Tier 1.
- Edit C: Added "Transitive dependencies row" guidance bullet to audit coverage tracking section
  after the CVE row note.
- Edit D: Tier-specific research scope — replaced `npm audit` / `pip-audit` in Tier 2 with
  `dep-scan.ps1 -Tier 2`; updated Tier 3 to reference `dep-scan.ps1 -Tier 3` in place of
  "manual review of direct dependency list".
**Result:** All 4 edits applied cleanly. No remaining `npm audit` / `pip-audit` references.
**Status:** Success

### [20260412 09:45] - Step 3: Update references/criteria/registry-package.md
**Action:** Replaced entire "Transitive Dependency Guidance" section (depth-thresholds table +
what-to-check + tier-applicability with npm audit/pip-audit references) with new
"Transitive Dependency Scanning" section. New section contains: invocation code block (T2 + T3),
output fields table, risk-level→verdict table with depth note, depth thresholds table,
and audit coverage row guidance with 5 example formats. No remaining npm audit / pip-audit
references in the criteria addendum.
**Result:** Section replaced. File updated.
**Status:** Success

### [20260412 09:55] - Step 4: Update references/criteria.md
**Action:** Added "Transitive Dependency Scan (registry packages)" subsection in §4.3 after
the "Vulnerability Database Lookup (registry packages)" subsection (line 153). Subsection
describes dep-scan.ps1 purpose, invocation timing (after vuln-lookup.ps1, Tier 1 skips),
and cross-references criteria addendum §Transitive Dependency Scanning for full details.
**Result:** Subsection inserted. No other changes to criteria.md.
**Status:** Success

### [20260412 10:05] - Step 5: Update evals/evals.json
**Action:** Verified assumptions via live npm registry + OSV before committing:
- coffee-script@1.12.0 → dependencies: {} (empty — plan assumption WRONG)
- mkdirp@0.5.1 → minimist: "0.0.8" (confirmed direct dep)
- minimist@0.0.8 → OSV returns CVE-2020-7598, CVE-2021-44906 (assumption confirmed)
- mkdirp@0.5.1 itself → 0 OSV vulns (clean)
- chalk@5.3.0 → 0 dependencies, 0 OSV vulns (confirmed clean)
Appended eval id 7 (mkdirp@0.5.1 with vulnerable minimist dep) and id 8 (chalk@5.3.0
zero-dep clean case). Ids 0–6 unchanged.
**Result:** evals.json updated with ids 7 and 8.
**Status:** Success

## Deviations

### Eval id 7: coffee-script → mkdirp@0.5.1
**Plan assumed:** coffee-script@1.12.0 has minimist@0.0.8 as a direct dep.
**Reality:** coffee-script@1.12.0 has empty dependencies ({}).
**Resolution:** Substituted mkdirp@0.5.1 — confirmed via npm registry: minimist: "0.0.8" is
a direct dep; OSV confirms CVE-2020-7598 on minimist@0.0.8. Same test scenario (clean package
with vulnerable direct dep), better-verified data. Prompt and expected_output updated.

### Eval id 8: chalk@5.3.0 has zero deps (not "real deps" as plan stated)
**Plan assumed:** chalk@5.3.0 is a "Tier 2 with real clean deps".
**Reality:** chalk@5.3.0 has 0 direct dependencies.
**Resolution:** Zero deps still satisfies the eval intent (dep-scan T2 returns directDepCount:0,
riskLevel:none, no false positives). Updated expected_output to reflect zero-dep reality. Test
still validates the no-false-positives path.

### [20260411 10:30] - Step 6: Verify acceptance criteria + bug fixes

**Acceptance test: mkdirp@0.5.1 T2**
Initial run: `riskLevel=none directDepCount=2 findings=[]` — wrong on all counts.

**Bug 1 found and fixed: PowerShell single-element array unwrapping**
`Get-NpmDeps` returns a 1-element array. PowerShell pipeline-unrolls it, so `$directDeps`
becomes the single `[ordered]@{Name=...; VersionRange=...}` hashtable directly.
- `$directDeps.Count` returns 2 (hashtable key count) → wrong `directDepCount`
- Piping hashtable through `ForEach-Object` enumerates `DictionaryEntry` key-value pairs
  → `$allDeps` contains 2 entries named "Name" and "VersionRange"
- OSV queries are sent for packages named "Name" and "VersionRange" → no vulns → `riskLevel=none`
**Fix:** Wrapped switch assignment with `@()`:
`$directDeps = @(switch ($Ecosystem) { ... })` — forces array regardless of element count.
Also simplified `$directDepCount = $directDeps.Count` (no longer needs truthy guard).

**After Bug 1 fix — mkdirp@0.5.1 T2:**
`directDepCount=1 riskLevel=critical findings=[{minimist@0.0.8, CVE-2020-7598, CVE-2021-44906, depth:1}]`

**Acceptance test: chalk@5.3.0 T2**
`directDepCount=0 riskLevel=none findings=[]` — correct (zero-dep, no false positives).

**Cache hit tests:**
mkdirp T2 second run: `cacheHit=true riskLevel=critical` ✓
chalk T2 second run: `cacheHit=true riskLevel=none` ✓

**T3 fallback (PyPI ecosystem):**
`fallback=true tier=2 fallbackReason="Tier 3 full-tree resolution is only supported for npm..."` ✓

**Acceptance test: mkdirp@0.5.1 T3 npm**
Initial run: fell back to T2 with `fallbackReason="The provided JSON includes a property
whose name is an empty string, this is only supported using the -AsHashTable switch."`

**Bug 2 found and fixed: ConvertFrom-Json rejects empty-string lockfile key**
npm lockfile v2 `packages` map has root entry `"": {...}` — valid JSON but rejected by
PowerShell's `ConvertFrom-Json` without `-AsHashTable`. The `if ($key -eq '') { continue }`
guard was never reached because the parse threw first.
**Fix:** Changed `ConvertFrom-Json` to `ConvertFrom-Json -AsHashTable` and switched
property iteration from `PSObject.Properties` → `GetEnumerator()` for both `packages`
and `dependencies` blocks.

**After Bug 2 fix — mkdirp@0.5.1 T3:**
`tier=3 fallback=false transitiveDepCount=2 directDepCount=1 riskLevel=critical
 findings=[{minimist@0.0.8, CVE-2020-7598, CVE-2021-44906, depth:1}]`

**All acceptance criteria met.**
**Status:** Success

## Issues Encountered

### Issue 1: directDepCount=2 / riskLevel=none on 1-dep package
See Bug 1 in Step 6 above.

### Issue 2: T3 npm fallback on ConvertFrom-Json empty-string key
See Bug 2 in Step 6 above.

## Data Gathered

- mkdirp@0.5.1 npm registry: 1 direct dep — minimist@0.0.8
- OSV querybatch for minimist (no version): stubs GHSA-vh95-rmgr-6w4m, GHSA-xvch-5gv4-984h
  (after enrichment: CVE-2020-7598, CVE-2021-44906; severity: critical)
- chalk@5.3.0: 0 direct deps, 0 OSV vulns
- requests PyPI T2: 6 direct deps (urllib3, certifi, chardet, idna, charset-normalizer, PySocks)
  riskLevel=critical (urllib3 has 17 CVEs across versions)
- mkdirp@0.5.1 T3 full tree: 2 packages (mkdirp + minimist)

## User Interventions

### [20260412 10:40] - Close gate prep
**Action:** Verified the repo is clean except unrelated untracked `AGENTS.md`. It will be
temporarily stashed before branch finalization, then restored after the squash merge to
keep the user's local file intact.
**Status:** Planned
