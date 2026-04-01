# Reliability & Accuracy Improvements for Install Auditor

> **Created:** 2026-04-02
> **Author:** Claude (Opus 4.6)
> **Seed:** "Opportunities to improve reliability and accuracy" of the install-auditor skill
> **Type:** Extension
> **Related Projex:** (none — first projex for this skill)

---

## Essence

The install-auditor's value proposition is trust: when it says APPROVED, that means something; when it says REJECTED, there's evidence behind it. Every gap in data collection, every subjective judgment call without grounding, every ecosystem it can't reach — these are cracks in that trust. The irreducible core of this imagination is: **make every claim in the audit report verifiable, and make the absence of data visible rather than silent.**

---

## Vision

An install-auditor that produces reports where every factual claim links to a concrete data source. Where "no vulnerabilities found" means "I checked these 4 databases and found nothing" rather than "I didn't find anything in a web search." Where typosquatting detection is algorithmic, not eyeballed. Where the dependency tree is traced, not just counted. Where the same package audited last week doesn't start from zero — but stale cached data is flagged, not silently trusted.

The auditor becomes a *layered evidence machine*: structured API queries form the foundation, web intelligence fills the gaps, and the report makes the evidence chain explicit so a human reviewer knows exactly what was checked and what wasn't.

---

## Possibility Space

### Dimensions

1. **Data source breadth** — how many independent sources are consulted per claim
2. **Data source depth** — how deeply each source is mined (metadata vs. dependency tree vs. source code)
3. **Automation vs. judgment** — which checks are algorithmic vs. relying on agent interpretation
4. **Ecosystem coverage** — which package managers, registries, and artifact types are supported
5. **Temporal awareness** — how the auditor handles recency, staleness, and change-over-time
6. **Transparency** — how clearly the report communicates what was checked and what wasn't

### Directions Explored

#### Direction 1: Multi-Database Vulnerability Correlation

Instead of relying on a single registry API plus web search, query multiple vulnerability databases and cross-reference:

- **OSV.dev** — Google's open-source vulnerability database. Single API, covers npm, PyPI, crates, Go, Maven, NuGet, and more. Query: `POST https://api.osv.dev/v1/query` with `{"package": {"name": "X", "ecosystem": "Y"}}`. Returns structured CVE/GHSA data.
- **GitHub Advisory Database (GHSA)** — GraphQL API. Covers the same ecosystems. Different maintainers sometimes report different things.
- **NVD (National Vulnerability Database)** — NIST's database. Broader than OSV but noisier. REST API with CPE matching.
- **Snyk Vulnerability DB** — commercial but has a free tier API. Sometimes catches things others miss.

**The reliability gain:** When 0/4 databases report a vulnerability, confidence in "clean" is much higher than when 0/1 do. When 1/4 reports something the others don't, that's a signal worth surfacing (possible false positive, or early detection).

**Concrete implementation:** Add an `osv-lookup` function to the registry-lookup script (or a separate script). For each audit, query OSV + GHSA at minimum. Report which databases were consulted in the Sources section. Flag discrepancies.

**Evidence chain in report:**
```
| CVEs / Advisories | None found (checked: OSV, GHSA, npm audit) |
```

#### Direction 2: Algorithmic Typosquatting Detection

The current approach — "compare name character by character against the legitimate package" — depends entirely on the agent already knowing the legitimate name. This fails for:
- Packages the agent hasn't encountered before
- Subtle variations (`react-native-community-async-storage` vs `@react-native-async-storage/async-storage` — different naming convention, not just character swaps)
- Namespace confusion (`lodash` vs `@lodash/lodash`)

**A more reliable approach:**

1. **Edit distance check** — Compute Levenshtein distance against top-1000 packages in the same ecosystem (available from registry download stats). Flag if distance <= 2 from a much-more-popular package.
2. **Popularity ratio** — If a package name is very similar to another and has 100x fewer downloads, flag it regardless of edit distance.
3. **Namespace verification** — For scoped packages (`@org/pkg`), verify the org exists and is the expected publisher. For unscoped packages that *should* be scoped (like the React Native example), flag the mismatch.
4. **Known-package list** — Maintain a curated list of commonly typosquatted packages per ecosystem (the top 200 by downloads). Check against this list first — it catches the highest-risk cases with zero false positives.

**Concrete implementation:** A `typosquat-check.ps1` (or JS equivalent) that takes a package name + ecosystem, fetches the top-N popular packages from the registry, and computes edit distances. Returns: closest match, distance, download ratio. The agent interprets the output rather than doing character comparison manually.

#### Direction 3: Transitive Dependency Auditing

The current script reports `dependencyCount` but doesn't look inside those dependencies. A package with 3 direct dependencies might pull in 400 transitive ones — any of which could be compromised.

**Layered approach:**

1. **Shallow scan (Tier 2):** Query OSV for each direct dependency (not just the target package). Flag any with known vulnerabilities. This is 5-20 API calls, feasible in a standard audit.
2. **Deep scan (Tier 3):** Resolve the full dependency tree (npm: `npm ls --all --json`, pip: `pipdeptree --json`, etc.), then batch-query OSV for all transitive dependencies. Flag any with known issues, especially those that are deeply nested (hard for users to notice).
3. **Dependency age heuristic:** Flag transitive dependencies that haven't been updated in 3+ years — they accumulate unpatched vulnerabilities silently.

**Evidence chain in report:**
```
| Dependency Risk | Low — 12 direct deps, 47 transitive. 0/47 have known CVEs (OSV batch query). Oldest transitive dep: `qs@6.5.3` (2019, no CVEs). |
```

#### Direction 4: Confidence & Coverage Metadata in Reports

The single highest-leverage change for accuracy: **make the report say what it didn't check.** Currently, if a web search fails or returns nothing, the report says "None found" — which reads identically to "checked thoroughly and confirmed clean."

**Proposed additions to every report:**

```markdown
## Audit Coverage
| Check | Status | Source |
|-------|--------|--------|
| Registry metadata | Done | npm API via registry-lookup.ps1 |
| CVE scan | Done | OSV, GHSA |
| Typosquat check | Done | Edit distance vs top-500 npm |
| Dependency tree | Skipped (Tier 2) | — |
| Source code review | Skipped (Tier 2) | — |
| OpenSSF Scorecard | Not available | api.securityscorecards.dev returned 404 |
| Web search: incidents | Done, 0 results | "express npm vulnerability 2026" |
| Install script review | N/A (no scripts) | package.json |
```

This transforms "None found" from ambiguous to precise. A reviewer can see at a glance: the audit checked 6 sources, skipped 2 (appropriate for tier), and 1 was unavailable.

### Directions Noted but Not Explored

- **Install script sandboxed execution** — Actually run `npm pack` + extract + analyze install scripts in a sandbox. High value for Tier 3 but complex to implement safely. Deserves its own imagination.
- **Continuous monitoring / re-audit triggers** — Watch for new CVEs affecting previously-approved packages. Crosses into a different product (ongoing monitoring vs. point-in-time audit).
- **Machine-readable report format** — JSON output alongside markdown for programmatic consumption. Useful but orthogonal to reliability.
- **Multi-platform registry-lookup** — Rewrite the PowerShell script in JavaScript/Python for cross-platform support. Important for adoption but not for accuracy.
- **Community signal aggregation** — Scrape GitHub issues, Reddit, Hacker News for sentiment. High noise, uncertain value.

---

## Texture & Detail

### What an Improved Tier 2 Audit Actually Looks Like

Today's Tier 2 flow:
1. Run `registry-lookup.ps1` → get metadata
2. Web search for CVEs and incidents
3. Agent synthesizes into report

Improved Tier 2 flow:
1. Run `registry-lookup.ps1` → get metadata + repo URL
2. Query OSV API for target package → structured vulnerability data
3. Query OSV API for each direct dependency (batch) → transitive risk signal
4. Run `typosquat-check` → algorithmic similarity score
5. Check OpenSSF Scorecard → automated trust signal
6. Web search for incidents (targeted: package name + "vulnerability" / "malware" / "supply chain")
7. Agent synthesizes with **coverage table** showing exactly what was checked

Steps 2-5 are deterministic — same input, same output. This eliminates variability from the agent's web search quality for the most critical checks. Web search (step 6) remains for intelligence that structured APIs can't provide, but it's no longer the *only* source for vulnerability data.

### What a Failed Lookup Looks Like in the Report

Today: If the OpenSSF Scorecard API returns nothing, the report either omits the section or says "Not available." There's no way to know if it was checked.

Improved: The coverage table shows `OpenSSF Scorecard | Not available | api.securityscorecards.dev returned 404 for github.com/org/repo`. The verdict logic treats this as "no data" (neutral) rather than "no problems" (positive). The distinction matters for borderline cases.

### How the Typosquat Checker Handles Edge Cases

- **Scoped vs. unscoped:** `lodash` and `@lodash/lodash` — the checker strips scopes before comparing, but also flags unscoped packages that shadow scoped ones.
- **Hyphen/underscore equivalence:** `my-package` and `my_package` — treated as distance 0 for comparison purposes (registries often normalize these).
- **Prefix/suffix squatting:** `express-js`, `node-express`, `expressjs` — edit distance might be high, but substring matching catches these against the known-popular list.

---

## Challenges & Tensions

### API Rate Limits & Availability

Querying 4 vulnerability databases + registry API + OpenSSF Scorecard per audit means 6+ external API calls at minimum. For Tier 3 with dependency tree scanning, this could be 50+ calls. Rate limits (especially NVD: 5 requests/30s without API key) could slow audits or cause incomplete results.

**Tension:** Thoroughness vs. speed. A Tier 1 "quick audit" that takes 2 minutes because it's waiting on API rate limits defeats its purpose.

**Resolution direction:** Tiered API usage — Tier 1 uses only the registry API (already fast). Tier 2 adds OSV (generous limits). Tier 3 adds everything. Cache results aggressively.

### Known-Package Lists Go Stale

A curated list of "top 200 packages per ecosystem" for typosquatting comparison needs maintenance. The npm top 200 shifts over months. A stale list gives false confidence.

**Tension:** Maintaining accuracy requires periodic updates, but the skill is a static set of files with no update mechanism.

**Resolution direction:** Fetch the popular-package list dynamically from the registry API at audit time (npm: `/-/v1/search?text=&popularity=1.0&size=250`). Costs one extra API call but is always current. Fall back to a cached list if the API is unavailable.

### False Confidence from More Data Sources

Querying 4 databases that all say "no vulnerabilities" feels more authoritative — but if the vulnerability hasn't been reported to *any* database yet (zero-day, or recently discovered), 4 "clean" results are no better than 1. The danger is that a longer coverage table creates an illusion of completeness.

**Tension:** More sources increase reliability for *known* issues but don't help with *unknown* ones. The coverage table must communicate this honestly.

**Resolution direction:** The coverage table's "Status" column should distinguish "No issues found" from "No issues reported." The report's confidence statement should explicitly note: "This audit checks known vulnerability databases. Zero-day or unreported issues are outside its scope."

### Dependency Tree Explosion

Some packages have enormous dependency trees (e.g., `create-react-app` pulls 1,400+ packages). Batch-querying OSV for all of them is feasible (OSV supports batch queries) but the report becomes unwieldy if multiple transitive deps have issues.

**Tension:** Completeness vs. actionability. A report that lists 12 medium-severity CVEs in transitive dependencies — none of which the user can directly fix — creates noise without clear action.

**Resolution direction:** For transitive deps, report only HIGH/CRITICAL CVEs. Summarize medium issues as a count. Focus the narrative on: "Are any of these actively exploited?" and "Can the user pin a version that avoids them?"

### Open Unknowns

- **How reliable is OSV for non-npm ecosystems?** Coverage varies — npm and PyPI are strong, others less so. Needs empirical testing.
- **What's the right threshold for typosquat edit distance?** Distance 1 catches obvious squats but misses namespace confusion. Distance 3 creates too many false positives. Needs calibration against real-world typosquat datasets.
- **How do users actually use audit reports?** If they skip to the verdict and ignore the coverage table, the transparency gains are wasted. Needs UX validation.
- **Should the auditor cache results across sessions?** Caching improves speed but introduces staleness. The right TTL depends on the threat model — hours for a security-sensitive org, days for a solo developer.

---

## Connections

### Feeds Into

- **Proposal:** Concrete changes to the registry-lookup script (add OSV integration, typosquat checker)
- **Plan:** Implementation of coverage metadata in report template
- **Plan:** New `typosquat-check` script
- **Eval expansion:** New eval cases testing multi-database correlation accuracy
- **Further imagination:** Install script sandboxed analysis for Tier 3 audits
- **Further imagination:** Continuous monitoring / re-audit triggering system

### Draws From

- Current install-auditor skill (SKILL.md, criteria.md, registries.md, registry-lookup.ps1)
- Existing evals (evals.json — only 3 cases, a clear gap)
- OSV.dev API documentation
- OpenSSF Scorecard API
- Real-world typosquatting incidents (e.g., `event-stream`, `ua-parser-js`, `colors`)

---

## Seeds for Further Imagination

1. **"The auditor that explains its uncertainty"** — What if the verdict included a confidence interval? "APPROVED (confidence: high — 6/6 checks passed)" vs. "APPROVED (confidence: moderate — 4/6 checks passed, 2 unavailable)"
2. **"Sandboxed install script analysis"** — Run `npm pack`, extract, analyze preinstall/postinstall scripts for suspicious patterns (network calls, env var reads, obfuscated code) in a disposable sandbox
3. **"Audit memory"** — A persistent cache of past audit results that makes re-audits fast and makes "what changed since last audit" a first-class question
4. **"The dependency graph as a visual artifact"** — Generate a dependency tree visualization highlighting risky nodes, so reviewers can see the attack surface at a glance
5. **"Ecosystem-specific deep checks"** — Docker: analyze Dockerfile layers. GitHub Actions: trace data flow through action inputs/outputs. Browser extensions: parse manifest.json permissions programmatically
