<!--
workflows/registry-package.md - Type 1 subject-specific workflow.
Handles registry packages from npm, PyPI, crates.io, RubyGems, NuGet,
Maven Central, Go modules, Hex.pm, and IaC module registries (Terraform
Registry, Ansible Galaxy, Helm/Artifact Hub).

This workflow replaces workflows/generic.md for Type 1 subjects. After
producing findings here, return to SKILL.md Step N for the shared verdict
tree and report shape. The Audit Coverage table and audit-confidence
assertion are owned by the dispatcher — do not duplicate them here.

Phase 2 / M2.1 — first subject-specific workflow.
-->

# Registry Package Workflow (Type 1)

This workflow handles **Type 1: registry-package** subjects, including IaC
modules (Terraform, Ansible, Helm) per taxonomy v1. It specializes the
generic evidence acquisition and scoring pipeline for registry package
concerns: ecosystem detection, provenance attestation, install script review,
and transitive dependency risk.

After completing all sections below, return to `SKILL.md` Step N for the
shared verdict tree and audit-coverage report shape.

Sections follow the standard workflow template: **Identify / Evidence /
Subject Rubric / Subject Verdict Notes**.

---

## Identify

### 1. Detect the ecosystem and registry

Determine which package ecosystem the subject belongs to. This drives which
lookup APIs, trust signals, and install-script patterns apply.

| Ecosystem | Registry URL pattern | Script support |
|-----------|---------------------|----------------|
| npm | `npmjs.com/package/*`, `npm install <pkg>` | `registry-lookup.ps1 -Ecosystem npm` |
| PyPI | `pypi.org/project/*`, `pip install <pkg>` | `registry-lookup.ps1 -Ecosystem pypi` |
| crates.io | `crates.io/crates/*`, `cargo add <pkg>` | `registry-lookup.ps1 -Ecosystem crates` |
| RubyGems | `rubygems.org/gems/*`, `gem install <pkg>` | `registry-lookup.ps1 -Ecosystem rubygems` |
| NuGet | `nuget.org/packages/*`, `dotnet add package <pkg>` | `registry-lookup.ps1 -Ecosystem nuget` |
| Maven Central | `search.maven.org`, `mvnrepository.com` | Not yet in script -- query API manually |
| Go modules | `pkg.go.dev/*`, `go get <module>` | Not yet in script -- query `pkg.go.dev` API |
| Hex.pm | `hex.pm/packages/*`, `mix deps.get` | Not yet in script -- query `hex.pm/api` |
| Terraform Registry | `registry.terraform.io/modules/*` or `providers/*` | Not yet in script -- query registry API |
| Ansible Galaxy | `galaxy.ansible.com`, `ansible-galaxy install` | Not yet in script -- query Galaxy API |
| Helm (Artifact Hub) | `artifacthub.io/packages/helm/*` | Not yet in script -- query Artifact Hub API |

> **Script coverage note:** `scripts/registry-lookup.ps1` currently supports
> npm, pypi, crates, rubygems, and nuget. For Go, Maven, Hex, and IaC
> registries, query their APIs directly or use web search. File an
> enhancement request if you need script support for these ecosystems.

### 2. Extract the exact package name

- **Scoped names**: npm uses `@scope/name` (e.g., `@babel/core`). The scope
  is part of the identity -- `@babel/core` and `babel-core` are different
  packages. Preserve the full scoped name.
- **Namespace packages**: PyPI normalizes `-` and `_` (e.g., `my-package` ==
  `my_package`). Verify against the canonical name shown on PyPI.
- **Case sensitivity**: npm names are lowercase. PyPI is case-insensitive but
  has a canonical form. crates.io is case-sensitive. RubyGems is
  case-sensitive. NuGet is case-insensitive.
- **IaC modules**: Terraform modules use `namespace/name/provider` format
  (e.g., `hashicorp/consul/aws`). Helm charts use `repo/chart`.

### 3. Gather required context

Collect before proceeding (same as generic, specialized for registry context):

1. **Full name and version** -- exact package name including scope/namespace,
   pinned version or range
2. **Registry** -- which ecosystem (from table above)
3. **Installation command** -- the exact `npm install`, `pip install`, etc.
   command the user will run
4. **Stated purpose** -- what the user needs this package for
5. **Target environment** -- dev machine, CI server, Docker build, production
   server, browser bundle
6. **Checksum / lockfile** -- is this going into a lockfile? Is there an
   integrity hash? (`npm` uses `sha512` in `package-lock.json`; `pip` uses
   hashes in `requirements.txt` with `--require-hashes`)

If any of 1--5 are missing, ask before proceeding. Item 6 is optional but its
presence increases trust.

---

## Evidence -- Part A: Triage (Pick the Audit Tier)

**Run the registry lookup script first** to get hard data:

```
.\scripts\registry-lookup.ps1 -Ecosystem <eco> -Name "<name>"
```

**For npm packages, run the typosquat check** immediately after the name is
known:

```
.\scripts\typosquat-check.ps1 -Ecosystem npm -Name "<exact name>"
```

If the user supplied a canonical name to compare against (or context strongly
implies one), add `-CompareTo "<known legitimate name>"`. Review the JSON
output -- if `riskLevel` is `critical` or `high`, this may short-circuit the
audit toward REJECTED/CONDITIONAL before completing full research (see
`references/criteria/registry-package.md` "Typosquat Detection" for
interpretation).

If the ecosystem is not supported by the script (Go, Maven, Hex, IaC
registries), query the registry API directly or use web search to obtain:
downloads/adoption, maintainer info, last publish date, and vulnerability
data.

Then apply the **registry-package-specific tier thresholds** from
`references/criteria/registry-package.md` (section "Tier Assignment
Thresholds"):

### Tier 1 -- Quick Audit (well-known, high-trust)

**All** of the following must be true:
- Official public registry
- Verified org or well-known maintainer
- High adoption (>1M weekly npm / cross-ecosystem equivalent -- see addendum)
- No CRITICAL or HIGH CVEs in requested version
- No maintainer changes in last 90 days
- First publish >1 year ago
- Provenance attestation present OR ecosystem has no mechanism

**Quick audit scope:** Confirm version is current, check for CVEs, verify the
name is not a typosquat, note the license, check for provenance attestation.
Write a short report. Takes ~2 minutes.

**Examples:** `express`, `lodash`, `react`, `requests`, `flask`, `django`,
`serde`, `tokio`, `rails`, `Newtonsoft.Json`, `hashicorp/aws` (Terraform).

### Tier 2 -- Standard Audit (default)

Use when the package has some trust signals but does not meet all Tier 1
criteria:
- Moderate adoption (1K--1M weekly npm / proportional)
- Identifiable publisher with history
- No unpatched CVEs in requested version
- First publish >30 days ago
- None of the Tier 3 triggers

**Standard audit scope:** Full research (Part B below) + structured report.
This is the default tier.

### Tier 3 -- Deep Audit (any red flag)

**Any one** of the following triggers Tier 3:
- Weekly downloads <1K (npm-equivalent) and not a known niche tool
- First publish <30 days ago
- Single anonymous/pseudonymous maintainer, account <6 months old
- Name similarity to a top-1000 package (edit distance <=2)
- Scope/namespace mismatch (e.g., `@express/core` by unknown org)
- User received the package link via DM, email, Slack, or chat
- `preinstall`/`postinstall` scripts with network or exec calls
- Recent maintainer transfer from established to unknown account
- Will run in CI/CD with access to secrets or production credentials

**Deep audit scope:** Everything in Standard, plus: install script source
review, dependency tree audit, behavioral analysis of source code, and
explicit alternatives comparison.

---

## Evidence -- Part B: Research

The goal is to answer these questions with *current* data (not training data
alone), specialized for registry package risk:

1. **Is this the real package?** For npm, start with the algorithmic check:
   review `typosquat-check.ps1` output (`riskLevel`, `closestMatches`,
   `combosquatHints`, `downloadRatio`). Then supplement with manual checks:
   compare name character by character against the legitimate package, check
   for homoglyphs, dash insertion/removal, scope impersonation. See
   `references/criteria/registry-package.md` "Typosquat Detection" for
   interpretation and `references/criteria.md` 4.1 for the substitution table.
2. **Does the publisher have provenance?** Check for ecosystem-specific trust
   signals (see `references/criteria/registry-package.md` "Ecosystem Trust
   Signals" table). Note presence or absence.
3. **Are there known vulnerabilities?** CVEs, security advisories, supply
   chain incidents affecting this package or its maintainer account.
4. **Who maintains it and are they still active?** Maintainer identity,
   account age, other packages by same maintainer, ownership transfers.
5. **What happens at install time?** Review lifecycle scripts
   (`preinstall`/`postinstall` for npm, `setup.py` for PyPI, `build.rs` for
   crates, etc.). See the install script risk patterns in
   `references/criteria/registry-package.md`.
6. **What does the dependency tree look like?** Direct dependency count,
   transitive depth, known-bad transitives. See transitive guidance in
   `references/criteria/registry-package.md`.
7. **Is anyone reporting problems?** Malware reports, data collection
   concerns, registry removal, deprecation.
8. **Is the project healthy?** Last publish date, commit recency, issue
   responsiveness, deprecation notices.

### How to research

**Start with the registry-lookup script** -- it provides downloads,
maintainer count, last publish date, dependency list, and vulnerability data
from official APIs.

```
.\scripts\registry-lookup.ps1 -Ecosystem <eco> -Name "<name>"
```

**Then run the structured CVE lookup** for supported ecosystems (npm, PyPI,
crates, RubyGems, NuGet, Go, Maven, Hex):

```
.\scripts\vuln-lookup.ps1 -Ecosystem <eco> -Name "<name>" [-Version "<version>"]
```

Review `riskLevel` and `summary.highestSeverity`. Check `discrepancies` -- an
advisory present in one DB but not the other may indicate a recently ingested
or recently withdrawn advisory; flag and investigate. Note `sources` for the
Audit Coverage CVE row. Web search follows for incidents not yet in structured
DBs (maintainer compromise, registry removal, behavioral reports).

**Then use web search** for things APIs do not cover:
- `"<package name>" vulnerability OR malware OR "supply chain"`
- `"<package name>" deprecated OR abandoned OR alternative`
- `"<package name>" maintainer compromise OR hijack`
- For IaC modules: `"<module name>" misconfiguration OR insecure default`

**Check the OpenSSF Scorecard** if a source repository is known:
`api.securityscorecards.dev/projects/github.com/<owner>/<repo>`. Scores
below 4/10 are a significant negative signal.

**For Tier 3 -- install script review:**
- npm: Read `package.json` `scripts` block; inspect referenced files
- PyPI: Read `setup.py` or `setup.cfg`; check for `cmdclass` overrides
- crates.io: Read `build.rs` if present
- RubyGems: Read `extconf.rb` if present
- NuGet: Check for `.targets`, `.props`, `init.ps1`, `install.ps1`
- Flag any pattern from the red-flag list in
  `references/criteria/registry-package.md` "Install Script Risk Patterns"

**Collect all source URLs** as you research -- they go in the report's
Sources section.

### Audit coverage tracking

As you run each check, record its outcome for the **Audit Coverage** table
(rendered in the dispatcher at `SKILL.md` Step N):

- Use the canonical row labels from `references/criteria.md` **Audit Coverage
  Checklist** for this tier and installable type.
- For each row: **Status** (`Done`, `Done, N results`, `Skipped (...)`,
  `Not available (...)`, `N/A (...)`) plus **Source or notes** (script name,
  API, search query, or why skipped).
- **Tier-skipped** checks are not the same as **Not available** -- the latter
  means you tried and could not get data.
- **Typosquat row (npm)**: When the ecosystem is npm, reference
  `typosquat-check.ps1` output in the Source/notes column -- e.g.,
  `typosquat-check.ps1: low risk` or `typosquat-check.ps1: high risk,
  investigated and confirmed legitimate`. For non-npm ecosystems, note manual
  comparison was used.

- **CVE / vulnerability databases row**: Reference `vuln-lookup.ps1` output --
  e.g., `Done -- vuln-lookup.ps1: none found (OSV, GHSA)` or
  `Done -- vuln-lookup.ps1: 2 CVEs (OSV: CVE-2021-23337, GHSA:
  GHSA-29mw-wpgm-hmr9, checked: OSV, GHSA)`. If GHSA was skipped:
  `Done -- vuln-lookup.ps1: none found (OSV only -- GHSA skipped)`. For IaC
  registries (not yet script-supported), use web search and note it:
  `Done -- web search: no advisories found`.

### Tier-specific research scope

**Tier 1 (Quick):** Confirm no CVEs, verify not a typosquat, check license
compatibility, note provenance attestation status. Skip deep web research,
dependency tree audit, and install script review.

**Tier 2 (Standard):** All of the above plus: full web search for incidents,
maintainer/activity assessment, OpenSSF Scorecard lookup, dependency tree
scan (`npm audit` / `pip-audit` / equivalent), install script existence check
(flag if scripts exist, but full source review is Tier 3).

**Tier 3 (Deep):** Everything in Standard plus: install script source code
review with red-flag pattern matching, manual review of direct dependency
list, behavioral analysis of source code (credential harvesting, network
calls, obfuscation), and explicit alternatives comparison.

---

## Subject Rubric -- Evaluate

Score against the shared rubric in `references/criteria.md` AND the
registry-package addendum in `references/criteria/registry-package.md`. The
sections below specialize the shared criteria for registry package context.

### 4.1 Provenance & Identity (registry-specialized)

- **Registry verification**: Is the package on an official public registry?
  Is the publisher verified by the registry (npm verified publisher, NuGet
  reserved prefix, Terraform verified publisher)?
- **Publisher identity**: Can the publisher be linked to a real organization
  or known individual? Check the registry profile, linked GitHub org, and
  publishing history.
- **Provenance attestation**: Does the package use ecosystem-specific
  provenance? npm Sigstore provenance, PyPI Trusted Publishers, NuGet package
  signing, crates.io GitHub-linked ownership. Presence is a strong positive.
  Absence when the mechanism exists is a minor note.
- **Typosquatting**: Character-by-character comparison against the legitimate
  package name. For scoped packages, also verify the scope owner (`@babel`
  vs `@bable`). Apply the substitution table from `references/criteria.md`
  4.1.
- **Version anomalies**: Is the requested version the latest stable? Are
  there gaps in the version sequence? Was there a sudden major version jump
  with no changelog? These can indicate hijacked publish.

### 4.2 Maintenance & Longevity (registry-specialized)

- **Last publish date**: When was the most recent version published to the
  registry? Use the date from the registry API (via script output), not the
  GitHub commit date -- they can diverge.
- **Commit recency**: Is the source repo active? A package last published 2
  years ago but with recent commits may have an unreleased fix, or may be
  abandoned on the registry side.
- **Issue responsiveness**: Are maintainers responding to issues and PRs?
  Check last 90 days.
- **Ownership continuity**: Has the package changed hands? npm `maintainers`
  array, PyPI project owners, crates.io owners -- compare current to
  historical if suspicious.
- **Deprecation signals**: Does the registry page show a deprecation notice?
  Does the README say "use X instead"? Is there a successor package?
- **IaC module specifics**: For Terraform modules, check provider version
  constraints and compatibility with current provider versions.

### 4.3 Security Track Record (registry-specialized)

- **CVEs in current version**: Check OSV, GHSA, npm advisories, PyPI
  advisories, RustSec, RubySec. The script output includes known
  vulnerabilities for supported ecosystems.
- **Supply chain history**: Has this package or its maintainer been involved
  in a supply chain incident? Check Snyk, Socket.dev, Sonatype advisories.
- **Install script review** (Tier 2: existence check; Tier 3: full review):
  Apply the risk patterns from `references/criteria/registry-package.md`
  "Install Script Risk Patterns". Any network fetch, env var harvesting, or
  obfuscated code in install scripts is a HIGH flag.
- **Transitive dependency risk**: Run `npm audit` / `pip-audit` / equivalent.
  Flag HIGH+ CVEs in transitive dependencies. See transitive guidance in
  addendum.

### 4.4 Permissions & Access (registry-specialized)

Registry packages do not have a formal permission model like browser
extensions, but they can access anything the installing user/process can.
Evaluate behavioral permissions:

- **npm install scripts**: `preinstall`/`postinstall` hooks execute with the
  user's shell permissions. Flag if they spawn subprocesses, make network
  calls, or access files outside the package directory.
- **Native addons**: Packages requiring `node-gyp`, C extensions (Python),
  or Rust FFI compile and link native code. This is normal for performance
  packages but increases the attack surface -- note it.
- **Network access patterns**: Does the package phone home at runtime?
  Telemetry, analytics, license checks. Note if opt-out is available.
- **File system access**: Does the package read/write outside its working
  directory? Access to `~/.ssh`, `~/.aws`, `~/.npmrc`, env files?
- **CI/CD context**: If the package will run in CI with secrets access,
  elevate scrutiny on all behavioral permissions. A package that reads
  `process.env` in CI can exfiltrate tokens.

### 4.5 Reliability & Compatibility (registry-specialized)

- **License compatibility**: Check against `references/licenses.md`. Pay
  attention to copyleft licenses (GPL, AGPL) in transitive dependencies that
  may not be obvious from the top-level package license.
- **Adoption signal**: Downloads/week, dependents count, GitHub stars. Use
  the interpretation table in `references/criteria.md` 4.5. Cross-check
  downloads with GitHub activity -- high downloads with zero GitHub stars or
  issues may indicate bot inflation.
- **OS/runtime compatibility**: Check `engines` (npm), `python_requires`
  (PyPI), Rust edition, .NET target framework. Does the package support the
  user's target environment?
- **Bundle/install size**: Abnormally large packages for their stated
  function can indicate bundled binaries or data exfiltration payloads.
  Compare to alternatives.

### 4.6 Alternatives (registry-specialized)

- **Same-function packages**: Search `"<package name> vs"` or
  `"<package name> alternative"`. Check the package's README for "similar
  projects" or "alternatives" sections.
- **Built-in alternatives**: Is this functionality available in the standard
  library or runtime? (e.g., `node:fs/promises` vs a wrapper package,
  `pathlib` vs `os.path` in Python)
- **Security-motivated alternatives**: If the package has security concerns,
  is there a drop-in replacement with better security posture? (e.g.,
  `node-fetch` vs built-in `fetch` in Node 18+)
- **IaC alternatives**: For Terraform modules, is there an official
  HashiCorp-maintained module vs a community module?

When flagging an alternative, briefly compare: security posture, maintenance
status, adoption level, and migration effort.

---

## Subject Verdict Notes

Registry-package-specific guidance for how findings map to verdicts. These
notes supplement the shared verdict tree in `SKILL.md` Step N -- they do not
replace it.

### Toward REJECTED

Any one of the following pushes strongly toward REJECTED for registry
packages:

- **Confirmed typosquat**: Name differs by <=2 characters from a top-1000
  package and the package has no established history of its own
- **Install script with exfiltration pattern**: `postinstall` script that
  reads env vars or `~/.ssh` and sends them to an external URL
- **Maintainer account compromise confirmed**: Security advisory or blog post
  confirms the maintainer account was hijacked
- **Package removed from registry**: Previously yanked/removed for security
  reasons (and re-published or accessed via cache)
- **Known malware**: Confirmed cryptominer, credential stealer, or data
  exfiltration in any version
- **Unpatched CRITICAL/HIGH CVE**: In the requested version with no fix
  available

### Toward CONDITIONAL

These findings push toward CONDITIONAL (installation may proceed with listed
conditions):

- **Patched CVE exists but user requests old version**: Condition: upgrade to
  patched version
- **Install scripts present but benign**: Condition: review script output
  after install; pin to exact version
- **Single maintainer with history**: Condition: pin version; re-audit on
  maintainer change
- **Moderate transitive risk**: Condition: run `npm audit` / equivalent
  before each update; pin lockfile
- **Missing provenance when mechanism exists**: Condition: verify checksum
  manually; pin to exact version
- **Stale but not abandoned**: Condition: monitor for deprecation; identify
  successor package
- **3+ MEDIUM flags accumulated**: Cumulative risk triggers CONDITIONAL per
  shared verdict tree

### Toward APPROVED

All of the following support APPROVED:

- All tier-appropriate checks completed with no flags
- Publisher is verified or well-known
- No CVEs in requested version
- Provenance attestation present (or ecosystem has no mechanism)
- Healthy maintenance signals
- License is compatible
- Adoption level appropriate for stated use case
- Install scripts absent or benign (native compilation only, no network/exec)

After completing the Subject Rubric and noting verdict-relevant findings,
**return to `SKILL.md` Step N** for the shared verdict tree, report
skeleton, and escalation guidance.
