# Registry Package — Criteria Addendum

Per-subject scoring extensions for **Type 1: registry-package** audits. This
addendum layers on top of the shared rubric in `references/criteria.md`. When
a criterion below conflicts with the shared rubric, the more specific
(registry-package) guidance wins.

Covers: npm, PyPI, crates.io, RubyGems, NuGet, Maven Central, Go modules,
Hex.pm, and IaC module registries (Terraform Registry, Ansible Galaxy,
Helm/Artifact Hub).

---

## Ecosystem Trust Signals

Each registry has its own verification and provenance mechanisms. Presence of
these signals raises trust; absence does not automatically lower it but should
be noted.

| Ecosystem | Trust Signal | What it proves |
|-----------|-------------|----------------|
| npm | **Provenance attestation** (`--provenance` flag, Sigstore) | Build artifact traces to a specific CI run and source commit |
| npm | Verified publisher badge / scope owner | Org identity confirmed by npm |
| PyPI | **Trusted Publisher** (OIDC from GitHub/GitLab CI) | Upload was automated from a known repo, not a local machine |
| PyPI | PGP/Sigstore signature on sdist/wheel | Artifact integrity (rare but strong) |
| crates.io | GitHub-linked ownership | Publish requires authenticated GitHub account; crate owners are public |
| crates.io | `cargo vet` audits by other orgs | Third-party attestation of reviewed source |
| RubyGems | **MFA required on privileged operations** | Account takeover resistance (mandatory for top gems since 2022) |
| RubyGems | Gem signing (rare) | Artifact integrity |
| NuGet | **Signed packages** (author + repository signing) | Package has not been tampered with post-build |
| NuGet | Verified owner / reserved prefix | Org identity confirmed by NuGet |
| Maven Central | PGP-signed artifacts (mandatory) | All Central artifacts are signed; verify key continuity |
| Maven Central | Namespace (groupId) ownership verification | Publisher controls the domain/org behind the groupId |
| Go modules | `GONOSUMCHECK` bypass absent, checksum DB match | Module integrity verified by `sum.golang.org` |
| Hex.pm | Hex package signing | Artifact integrity for Elixir/Erlang packages |
| Terraform Registry | Verified publisher badge | HashiCorp-reviewed org identity |
| Ansible Galaxy | Namespace ownership | Collection publisher controls the namespace |

### Scoring impact

- **Provenance attestation present** (npm provenance, PyPI Trusted Publisher, NuGet signing): +1 trust on Provenance (4.1). This is a strong positive signal.
- **Provenance mechanism available for ecosystem but not used**: Note as a minor negative. Not auto-flag, but mention in report.
- **No provenance mechanism exists for the ecosystem**: Neutral -- do not penalize.

---

## Tier Assignment Thresholds (Registry Packages)

These thresholds resolve the dispatcher's Open Question Q4 for Type 1
subjects. They specialize the generic tiers in `workflows/generic.md`.

### Tier 1 -- Quick Audit

**All** of the following must be true:

| Criterion | Threshold |
|-----------|-----------|
| Registry | Official public registry (npm, PyPI, crates.io, RubyGems, NuGet, Maven Central, Go proxy, Hex.pm, Terraform Registry) |
| Weekly downloads (npm-equivalent) | >1M npm / >500K PyPI / >100K crates / >50K gems / >100K NuGet / equivalent high adoption |
| Publisher | Verified org or well-known individual maintainer |
| CVEs in requested version | None (CRITICAL or HIGH) |
| Recent maintainer change | None in last 90 days |
| Package age | First publish >1 year ago |
| Provenance | Attestation present OR ecosystem has no mechanism |

**Cross-ecosystem download equivalence** (rough): 1M npm weekly ~ 500K PyPI
monthly ~ 100K crates.io all-time ~ 50K gems weekly ~ 100K NuGet weekly. Use
judgment for ecosystems without direct weekly counts.

**Tier 1 examples:** `express`, `lodash`, `react`, `requests` (Python),
`flask`, `django`, `serde`, `tokio`, `rails`, `Newtonsoft.Json`,
`hashicorp/aws` (Terraform).

### Tier 2 -- Standard Audit (default)

The package has *some* trust signals but does not meet all Tier 1 criteria:

| Criterion | Range |
|-----------|-------|
| Weekly downloads (npm-equivalent) | 1K--1M npm / proportional in other ecosystems |
| Publisher | Identifiable individual or small org with history |
| CVEs | None unpatched in requested version (patched older CVEs acceptable) |
| Package age | First publish >30 days ago |
| No red flags | None of the Tier 3 triggers below |

This is the **default tier**. When in doubt, use Tier 2.

### Tier 3 -- Deep Audit

**Any one** of the following triggers Tier 3:

| Trigger | Rationale |
|---------|-----------|
| Weekly downloads <1K (npm-equivalent) and not a known niche tool | Insufficient community vetting |
| First publish <30 days ago | Too new to have track record |
| Single anonymous/pseudonymous maintainer, new account (<6 months) | Account takeover or sockpuppet risk |
| Name similarity to a top-1000 package (edit distance <=2) | Typosquat candidate |
| Scope/namespace mismatch (e.g., `@express/core` by unknown org) | Brand impersonation candidate |
| User received the package link via DM, email, Slack, or chat | Social engineering vector |
| Package has `preinstall`/`postinstall` scripts with network or exec calls | Install-time code execution risk |
| Recent maintainer transfer from established to unknown account | Possible account compromise |
| Will run in CI/CD with access to secrets or production credentials | High blast radius |

---

## Install Script Risk Patterns

Registry packages can execute arbitrary code at install time. These patterns
warrant scrutiny at Tier 2 and mandatory review at Tier 3.

### npm lifecycle scripts

| Script | Risk | Review guidance |
|--------|------|-----------------|
| `preinstall` | HIGH | Runs before dependencies resolve -- can execute before lockfile integrity check |
| `install` | MEDIUM | Typically used for native addon compilation (node-gyp); verify it only compiles bundled source |
| `postinstall` | HIGH | Most common vector for supply chain attacks; check for `curl`, `wget`, encoded strings, `eval()` |
| `prepare` | LOW | Runs on `git` installs; usually build step |

### PyPI setup hooks

| Mechanism | Risk | Review guidance |
|-----------|------|-----------------|
| `setup.py` with `cmdclass` override | HIGH | Arbitrary code during `pip install`; check for network calls, file reads outside package dir |
| `pyproject.toml` build backends | MEDIUM | Less surface area than raw `setup.py` but still executes build code |
| `__init__.py` import-time side effects | MEDIUM | Code runs on first import, not install -- but still a supply chain vector |

### Other ecosystems

| Ecosystem | Install-time execution | Notes |
|-----------|----------------------|-------|
| RubyGems | `extconf.rb` (native extensions) | Review for network calls or system command execution |
| crates.io | `build.rs` (build script) | Runs at compile time; check for `Command::new()` calls |
| NuGet | `.targets`/`.props` MSBuild imports, `init.ps1`/`install.ps1` | PowerShell scripts run in VS Package Manager Console |
| Go | None (no install hooks) | Go modules have no install-time execution -- positive signal |
| Maven | Plugin execution during build phases | Review `pom.xml` for unusual plugins |

### Red-flag patterns in install scripts

Flag and document any of the following:

- **Network fetches**: `curl`, `wget`, `fetch()`, `requests.get()`, `http.get()` to external URLs
- **Encoded/obfuscated strings**: Base64 blobs, hex-encoded strings, `eval()` on decoded content
- **Environment variable harvesting**: Reading `HOME`, `SSH_KEY`, `AWS_SECRET`, `NPM_TOKEN`, `GITHUB_TOKEN`
- **File system scanning**: `readdir` on `~`, `~/.ssh`, `~/.aws`, `~/.npmrc`
- **Process spawning**: `child_process.exec()`, `subprocess.run()`, `os.system()` with dynamic input
- **Exfiltration patterns**: HTTP POST with collected env vars or file contents

---

## Transitive Dependency Guidance

### Depth thresholds

| Metric | Concern level | Action |
|--------|--------------|--------|
| Direct dependencies <10 | Normal | Standard review |
| Direct dependencies 10--50 | Elevated | Note in report; check for known-bad transitives |
| Direct dependencies >50 | High | Flag dependency bloat; increased attack surface |
| Transitive tree >200 packages | Elevated | Note in report |
| Transitive tree >500 packages | High | Flag; recommend `npm audit` / `pip-audit` / equivalent |
| Any transitive dependency with known CVE (HIGH+) | Critical | Flag even if not direct dependency |

### What to check

- **Known-bad transitives**: Cross-reference against recent supply chain incident lists (e.g., `event-stream`, `ua-parser-js`, `colors`/`faker`, `node-ipc`)
- **Single-maintainer deep dependencies**: A critical transitive dep maintained by one person is a bus-factor risk
- **Deprecated transitives**: Dependencies pulling in deprecated packages that have known successors
- **Duplicate functionality**: Multiple packages in the tree doing the same thing (signals poor curation)

### Tier applicability

- **Tier 1**: Skip transitive audit (trust established at top level)
- **Tier 2**: Run `npm audit` / `pip-audit` / equivalent; flag HIGH+ CVEs in transitives
- **Tier 3**: Manual review of direct dependency list; automated scan of full tree; flag single-maintainer critical transitives

---

## Typosquat Detection (Algorithmic + Manual)

For **npm** packages, run the algorithmic typosquat check before manual review:

```
.\scripts\typosquat-check.ps1 -Ecosystem npm -Name "<exact name>"
```

Add `-CompareTo "<known legitimate name>"` when the user or context supplies a
canonical package name to compare against.

### Interpreting script output

The script emits a JSON object with:

| Field | Meaning |
|-------|---------|
| `riskLevel` | `low` / `medium` / `high` / `critical` -- algorithmic risk assessment |
| `closestMatches` | Top packages by edit distance, with distance and download counts |
| `combosquatHints` | Popular package names that are a prefix/suffix of the queried name |
| `downloadRatio` | Weekly downloads of queried vs closest match (ratio > 100x is suspicious) |
| `details` | Human-readable summary of risk factors |

### Risk level thresholds and verdict impact

| Script risk level | Audit action |
|-------------------|-------------|
| **critical** | Auto-**REJECTED** unless the auditor can affirmatively prove the package is legitimate (e.g., it IS the popular package). Document override reasoning if proceeding. |
| **high** | Strong **CONDITIONAL** lean. Must investigate thoroughly -- verify publisher identity, check if package has independent history, compare repository URLs. Only APPROVE with explicit justification. |
| **medium** | Investigate further. Check publisher, repository, README, and download trends. May be a legitimate similarly-named package. Document findings either way. |
| **low** | Note the check was run and passed. Proceed with normal audit flow. |

### Manual and homoglyph checks (complement algorithmic)

The script catches edit-distance and combosquat patterns but cannot detect:

- **Homoglyph substitution**: Cyrillic `a` (U+0430) vs Latin `a` (U+0061),
  Cyrillic `e` vs Latin `e`, etc. Visually inspect the name for non-ASCII
  characters, especially in scoped names.
- **Semantic confusion**: `lodash-utils` vs `lodash.utils` -- packages that
  look related but are by different publishers.
- **Scope impersonation**: `@babel/core` (official) vs `@bable/core` (squat).
  The script compares unscoped basenames; manually verify the scope owner.
- **Registry context**: A package name that is legitimate on one registry but
  a squat on another (cross-ecosystem confusion).

Always perform a manual visual check in addition to the script, especially for
scoped packages and names with non-ASCII characters.

### Audit coverage row guidance

For the **Typosquat / name verification** row in the Audit Coverage table:

- **npm packages**: Status should reference the script: e.g.,
  `Done — typosquat-check.ps1: low risk` or
  `Done — typosquat-check.ps1: high risk, manual review confirms squat`.
- **Other ecosystems**: Until script support is added, use manual comparison:
  `Done — manual character-by-character check`.

---

## Multi-Database CVE Correlation

Run `scripts/vuln-lookup.ps1` before web search to query structured vulnerability
databases for registry packages.

### Invocation

```
.\scripts\vuln-lookup.ps1 -Ecosystem <eco> -Name "<name>" [-Version "<version>"]
```

**Supported ecosystems:** npm, pypi, crates, rubygems, nuget, go, maven, hex.
IaC registries (Terraform, Ansible, Helm): fall back to web search — OSV/GHSA
ecosystem mapping for these is not yet established.

**GITHUB_TOKEN:** Set `$env:GITHUB_TOKEN` to raise GHSA rate limit from 60/hr to
5,000/hr. If unset or rate-limited, the script continues with OSV only (`sources:
["OSV"]`). The audit is never blocked by token absence.

### Output fields

| Field | Meaning |
|---|---|
| `riskLevel` | `none` / `low` / `medium` / `high` / `critical` |
| `osvResults` | Vulnerabilities from OSV.dev |
| `ghsaResults` | Vulnerabilities from GitHub Advisory Database |
| `discrepancies` | Advisories present in one source but not the other |
| `sources` | Which DBs were actually queried (e.g., `["OSV","GHSA"]`) |
| `ghsaNote` | Present when GHSA was skipped; explains why |

### Risk level → verdict impact

| `riskLevel` | Audit action |
|---|---|
| `none` | Note "None found (checked: OSV, GHSA)" in CVE row. Proceed. |
| `low` | Note finding; verify version-range scope. Does not shift verdict alone. |
| `medium` | Investigate — check if requested version is in affected range. May push toward CONDITIONAL. |
| `high` | Strong CONDITIONAL lean. Report must cite CVE IDs and affected ranges. Condition: upgrade to patched version; pin lockfile. |
| `critical` | REJECTED lean. Exception only if requested version is affirmatively outside affected range — document the version-range check. |
| Discrepancy (one DB only) | Flag and investigate. May be ingestion lag or a withdrawn advisory. Document in Security row; do not silently discard. |

### When `-Version` is supplied

The script cross-checks each vulnerability's affected version ranges against the
requested version. Conservative: if range data is absent, the vulnerability is
included (not silently dropped). `riskLevel` reflects only vulns that affect the
specified version.

### Audit coverage row guidance

For the **CVE / vulnerability databases** row in the Audit Coverage table:

- Reference `vuln-lookup.ps1` output: e.g.,
  `Done -- vuln-lookup.ps1: none found (OSV, GHSA)` or
  `Done -- vuln-lookup.ps1: 2 CVEs (OSV: CVE-2021-23337, checked: OSV, GHSA)`.
- If GHSA was skipped: `Done -- vuln-lookup.ps1: none found (OSV only -- GHSA skipped)`.
- For IaC registries (script not yet supported): use web search and note it:
  `Done -- web search: no advisories found`.
