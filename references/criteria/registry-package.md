# Registry Package — Criteria Addendum

Per-subject scoring extensions for **Type 1: registry-package** audits. This
addendum layers on top of the shared rubric in `references/criteria.md`. When
a criterion below conflicts with the shared rubric, the more specific
(registry-package) guidance wins -- except `references/criteria.md` §4.6,
which this file only tightens or fills, and the §4.3 verdict classes.

Covers: npm, PyPI, crates.io, RubyGems, NuGet, Maven Central, Go modules,
Hex.pm, and IaC module registries (Terraform Registry, Ansible Galaxy,
Helm/Artifact Hub).

---

## Ecosystem Trust Signals

Each registry has its own identity mechanisms. They prove **who published** a
version (origin), never that its code is safe (`references/criteria.md` §4.6
V2). Credit one only when it is **verified**: present on the version to be
installed **and** naming the same identity as the previous release or the
project's documented release setup.

| Ecosystem | Identity signal | Where to check | What it proves |
|-----------|-----------------|----------------|----------------|
| npm | **Trusted publishing** (CI OIDC, no long-lived token) | `registry-lookup` `trustedPublisher` (`id`, `oidcConfigId`); npmjs.com package page | Version was published by the configured CI workflow |
| npm | **Provenance attestation** (Sigstore, SLSA) | `registry-lookup` `provenance`; source repo + workflow in the attestation (npmjs.com provenance panel or `dist.attestations.url`); `npm audit signatures` after install | Tarball was built by a named repo + workflow run |
| npm | Registry signatures | `npm audit signatures` | Tarball is what the registry signed; says nothing about the publisher |
| npm | Verified org / scope owner | npmjs.com org page | Org controls the scope |
| PyPI | **Trusted Publisher** + **PEP 740 attestations** | Simple API JSON (`Accept: application/vnd.pypi.simple.v1+json`): `files[].provenance` URL → `attestation_bundles[].publisher` (`kind`, `repository`, `workflow`) | File was uploaded by a named CI repo + workflow |
| PyPI | Mandatory 2FA | -- | Account-takeover resistance only |
| crates.io | **Trusted publishing** | `crates.io/api/v1/crates/<name>/<version>` `trustpub_data` (`provider`, `repository`, `sha`); `published_by` for token publishes | Version was published from a named repo + commit |
| crates.io | `cargo vet` audits by other orgs | audit imports | Third-party review of the source |
| RubyGems | **MFA required** on privileged operations (top gems); trusted publishing available | rubygems.org gem page | Account-takeover resistance; CI-published when TP is used |
| RubyGems | Gem signing (rare) | `gem cert` | Artifact integrity |
| NuGet | **Signed packages** (author + repository signatures); trusted publishing available | `dotnet nuget verify`; nuget.org package page | Unchanged since signing; author certificate subject |
| NuGet | Verified owner / reserved prefix | nuget.org package page | Org identity confirmed by NuGet |
| Maven Central | PGP-signed artifacts (mandatory); Sigstore bundles optional | `.asc` / `.sigstore.json` next to each artifact | Key holder signed it; check key continuity across versions |
| Maven Central | Namespace (groupId) ownership verification | central.sonatype.com | Publisher controls the domain/org behind the groupId |
| Go modules | Checksum database (`sum.golang.org`) | `go.sum`; `GOSUMDB` not `off`; no `GONOSUMDB` / `GOPRIVATE` pattern covering public modules | Everyone gets the same bytes for a version (consistency). **Not** identity or safety: the proxy keeps serving a cached version even if it is malicious |
| Hex.pm | Hex package signing | -- | Artifact integrity for Elixir/Erlang packages |
| Terraform Registry | Verified publisher badge | registry page | HashiCorp-reviewed org identity |
| Ansible Galaxy | Namespace ownership | Galaxy page | Collection publisher controls the namespace |

### Scoring impact

- **Verified** (matched to the previous release or project docs): positive
  note. Never lifts a §4.6 flag, and never enough on its own for Tier 1 or
  APPROVED.
- **Present but unmatched** (no previous release, attestation not opened):
  note only, no credit.
- **Dropped or changed** versus the previous release: §4.6 V3 HIGH, which
  bars Tier 1 and triggers Tier 3 (see "Version & Update Integrity (§4.6)"
  below).
- **Mechanism exists, package never used it**: minor note in the report; no
  flag, no condition, and it does not block Tier 1.
- **No mechanism in the ecosystem**: neutral.
- **Typosquats can carry valid provenance** from their own repo: the identity
  must match the *legitimate* project's repo, not merely exist.

---

## Tier Assignment Thresholds (Registry Packages)

These thresholds resolve the dispatcher's Open Question Q4 for Type 1
subjects. They specialize the generic tiers in `workflows/generic.md`.

### Tier 1 -- Quick Audit

**All** of the following must be true:

| Criterion | Threshold |
|-----------|-----------|
| Registry | Official public registry (npm, PyPI, crates.io, RubyGems, NuGet, Maven Central, Go proxy, Hex.pm, Terraform Registry) |
| Adoption | Above the Tier 1 bar in the adoption table below |
| Publisher | Verified org or well-known individual maintainer |
| CVEs in requested version | None (CRITICAL or HIGH) |
| Recent maintainer change | None in last 90 days |
| Package age | First publish >1 year ago |
| Version age (§4.6 V1) | Version to be installed published ≥ 7 days ago (`daysSincePublish` ≥ 7) |
| Identity (§4.6 V2) | Not required: missing trusted publishing or provenance does not block Tier 1. Present identity evidence earns no Tier 1 credit on its own |
| Continuity (§4.6 V3) | No change of signer, trusted-publisher config or publisher from the previous release, and no other V3 item |
| History (§4.6 V4) | No past compromise (V4 case c) |

**Adoption bars** use the field `registry-lookup` emits, in that field's own
time window. Do not convert between windows.

| Ecosystem | Field (window) | Tier 1 bar | Tier 3 trigger below |
|-----------|----------------|------------|----------------------|
| npm | `weeklyDownloads` (7 d) | > 1M | 1K |
| PyPI | `monthlyDownloads` (30 d, pypistats) | > 500K | 500 |
| crates.io | `recentDownloads` (90 d) | > 10M | 10K |
| RubyGems | `totalDownloads` (all time) | > 50M | 50K |
| NuGet | nuget.org total downloads (no script field) | > 50M | 50K |
| Others | the registry's own count | judgment: top few hundred of the ecosystem | judgment |

**Tier 1 examples:** `express`, `lodash`, `react`, `requests` (Python),
`flask`, `django`, `serde`, `tokio`, `rails`, `Newtonsoft.Json`,
`hashicorp/aws` (Terraform). Each still needs the per-version rows above
(age ≥ 7 d, no change from the previous release) at audit time.

### Tier 2 -- Standard Audit (default)

The package has *some* trust signals but does not meet all Tier 1 criteria:

| Criterion | Range |
|-----------|-------|
| Adoption | Between the Tier 3 trigger and the Tier 1 bar (adoption table above) |
| Publisher | Identifiable individual or small org with history |
| CVEs | None unpatched in requested version (patched older CVEs acceptable) |
| Package age | First publish >30 days ago |
| No red flags | None of the Tier 3 triggers below |

This is the **default tier**. When in doubt, use Tier 2.

### Tier 3 -- Deep Audit

**Any one** of the following triggers Tier 3:

| Trigger | Rationale |
|---------|-----------|
| Adoption below the Tier 3 trigger (adoption table) and not a known niche tool | Insufficient community vetting |
| First publish <30 days ago | Too new to have track record |
| Single anonymous/pseudonymous maintainer, new account (<6 months) | Account takeover or sockpuppet risk |
| Name similarity to a top-1000 package (edit distance <=2) | Typosquat candidate |
| Scope/namespace mismatch (e.g., `@express/core` by unknown org) | Brand impersonation candidate |
| User received the package link via DM, email, Slack, or chat | Social engineering vector |
| Package has `preinstall`/`postinstall` scripts with network or exec calls | Install-time code execution risk |
| Recent maintainer transfer from established to unknown account | Possible account compromise |
| Will run in CI/CD with access to secrets or production credentials | High blast radius |
| Version to be installed has a §4.6 V3 HIGH (identity dropped or changed, new install hook) or a publisher change from the previous release (V3 plug-in below) | Possible hijacked publish |

---

## CVE Scope (§4.3)

- **Own code** = the package's published contents: its own source plus any
  library it vendors into its tarball / wheel. An advisory filed against the
  package name is an own-code advisory, even when a vendored library is the
  root cause.
- **Third-party component** = everything resolved as a separate package:
  direct and transitive dependencies (`dep-scan` findings), and system
  libraries the package links against at runtime.
- **Scan sources:** `vuln-lookup` (OSV + GHSA) for own code, `dep-scan` for
  dependencies. Always pass `-Version` with the version to be installed;
  without it `riskLevel` covers every version.
- **KEV:** check CRITICALs from either source against the CISA KEV catalog.
- **VEX:** registry packages rarely publish VEX. Accept `not_affected` only on
  the §4.3 terms (publisher or component maintainer, names this version,
  gives a justification).

## Version & Update Integrity (§4.6)

Registry plug-ins for `references/criteria.md` §4.6. The version unit for
V1–V3 is the published version string. Registries never let a publisher
replace a published version's files, with one exception: PyPI accepts *new*
files for an existing release (see V1).

- **V1** -- publish time and cooldown.
  - npm, PyPI, crates.io, NuGet: `registry-lookup -Version <v>` `publishedAt` /
    `daysSincePublish`. Whole days, floored: 0–2 = < 72 h, 3–6 = 72 h – 7 d.
    For an unpinned request run it without `-Version`; it reports the version
    `latest` resolves to.
  - PyPI: the script dates a release by its first file. A file added later
    to an old release (e.g. a new platform wheel) is fresh: check the
    `upload-time` of the file the installer will pick (simple API JSON).
  - RubyGems: the script ignores `-Version` and reports the latest version.
    For a pinned version use `rubygems.org/api/v1/versions/<gem>.json`
    `created_at`.
  - Go: `proxy.golang.org/<module>/@v/<version>.info` `Time`. Maven, Hex, IaC
    registries: the registry page or API publish date.
  - Cooldown to cite in a `fresh version` condition (7 days):

    | Client | Setting | Unit | Since |
    |--------|---------|------|-------|
    | npm | `min-release-age=7` (`.npmrc`) | days | 11.10.0 |
    | pnpm | `minimumReleaseAge: 10080` (`pnpm-workspace.yaml`) | minutes | 10.16.0 (current pnpm also has a non-strict built-in 1440-minute default) |
    | Yarn (berry) | `npmMinimalAgeGate: 7d` (`.yarnrc.yml`) | duration | 4.10.x |
    | Bun | `minimumReleaseAge = 604800` (`bunfig.toml` `[install]`) | seconds | 1.3.0 |
    | uv | `exclude-newer = "7 days"` (or `--exclude-newer "7 days"`) | duration | checked in 0.11.32 |
    | pip | `--uploaded-prior-to P7D` | ISO-8601 days | 26.1 (26.0 takes a datetime only) |
    | cargo, gem, NuGet, Go, Maven | none known: exact pin + lockfile, plus the date the version turns 7 days old | -- | -- |

- **V2** -- identity mechanisms and verification: "Ecosystem Trust Signals"
  above.
  - **Expected identity** = the previous release's identity (`previousVersion`
    for npm; the previous release's attestation publisher on PyPI; the
    previous version's `trustpub_data` on crates.io), else the repository the
    project documents. A trusted publisher with the same `oidcConfigId` as
    the previous version counts as matched.
  - Absence is never a flag when the package never used the mechanism, and
    never blocks Tier 1. Only a change from the previous release counts
    (V3).
  - Verify command: `npm audit signatures` (registry signatures and
    provenance of installed packages; run it in a scratch project).
- **V3** -- diff against the previous release.
  - npm: compare `trustedPublisher`, `provenance`, `publisher` and
    `installScripts` with `previousVersion`. Trusted publisher or provenance
    present before and absent now, or a different `oidcConfigId` or
    attestation repo → HIGH.
  - Install hooks: a hook in `installScripts` missing from
    `previousVersion.installHooks` → HIGH unless the changelog explains it;
    explained → MEDIUM. A new `binding.gyp`, a new `.pth` file, or a new
    dependency with install scripts counts as a new hook.
  - **Publisher change** = the publishing account had never published this
    package before, or the maintainer/owner list changed. At least MEDIUM,
    and always a Tier 3 trigger (deep audit). Another long-standing
    maintainer pressing publish is not a change. Established → unknown
    account → HIGH.
  - PyPI, crates.io: same comparison by hand on attestation
    `publisher.repository` / `workflow` and on `trustpub_data.repository`.
  - Go: `.info` `Origin` names the VCS ref + hash. A version with no
    matching upstream tag → HIGH ("no matching upstream source tag").
  - Client guard to cite: pnpm `trustPolicy: no-downgrade` (10.21.0+) refuses
    versions whose trust evidence is weaker than earlier releases'.
  - **Release-pipeline exposure** (Tier 3, when provenance names a repo +
    workflow): skim the release workflow with the `workflows/ci-action.md`
    lens: `pull_request_target`, a shared cache restored in the publish job,
    unpinned actions in a job with `id-token: write`. Any → MEDIUM flag
    `release pipeline exposure`. A poisonable pipeline still produces valid
    provenance.
- **V4** -- incident sources (in addition to web search).
  - `vuln-lookup` `osvResults` with an `id` starting `MAL-` (OSV
    malicious-package record): case (a) when the version is in range, case
    (b) when the whole package is malicious.
  - npm "security holding package" (version `0.0.1-security`) → Red Flag
    "Removed for cause".
  - npm `removedVersions` (in `time`, no longer served): a removed version
    inside an advisory's range is evidence the bad versions were taken down
    (case c). It is not proof of remediation, so still cite the advisory.
  - PyPI simple API JSON `project-status` `quarantined` → case (a) while it
    lasts.
  - Case (c) lockfile check: `npm ls <pkg>`, `pip freeze`,
    `cargo tree -i <crate>`.
- **V5** -- triggers and update controls.
  - Subject triggers, added to the defaults: new install hook | identity drop
    | maintainer added or removed | deprecation or transfer notice.
  - Update controls: exact version + lockfile (`npm ci`,
    `pnpm install --frozen-lockfile`, `pip install --require-hashes`,
    `uv lock`, `Cargo.lock`, `go.sum`); the V1 cooldown; pnpm
    `trustPolicy: no-downgrade`. npm script approvals stay version-pinned
    (`allowScripts` `pkg@x.y.z`), so each new version's scripts need a fresh
    approval: keep it that way.

---

## Install Script Risk Patterns

Registry packages can execute arbitrary code at install time. These patterns
warrant scrutiny at Tier 2 and mandatory review at Tier 3.

### Client execution model

Whether install-time code runs depends on the client, so record the client
and version (workflow Identify, item 7).

| Client | Dependency install scripts by default | Approval mechanism |
|--------|---------------------------------------|--------------------|
| npm ≥ 12 | **Blocked** (`preinstall`, `install`, `postinstall`; `prepare` for non-registry sources) | `allowScripts` in `package.json` via `npm approve-scripts <pkg>` (writes version-pinned `pkg@x.y.z` entries); global installs and `npx`: `--allow-scripts=<pkg>` |
| npm ≤ 11, Yarn classic | Run | `--ignore-scripts` suppresses them |
| pnpm ≥ 10 | **Blocked** | `pnpm approve-builds` (writes `allowBuilds` in current pnpm) |
| Bun | Blocked except `trustedDependencies` (plus Bun's built-in default list) | `trustedDependencies` in `package.json` |
| pip / uv | sdist: the build backend runs on install; wheel: no install hook | `--only-binary :all:` avoids sdist builds |

- **Blocked by default → the decision is "will the user approve this
  package's scripts?"** Rate the scripts as if approved when the package needs
  them to work (native addons). Condition: approve only this package, pinned
  to the audited version. Never use name-only or blanket approval
  (`--no-allow-scripts-pin`, `npm approve-scripts --all`,
  `dangerouslyAllowAllBuilds`).
- **Client unknown → assume scripts run.**
- npm ≥ 12 defaults `allow-git` and `allow-remote` to `none`. If this package
  needs an opt-in for a git or URL dependency → MEDIUM flag: git dependencies
  can bring configuration the project does not control.
- Blocking scripts does not stop import-time or runtime code (`.pth` files,
  `__init__.py`, module top level, `bin` entries the user runs).

### npm lifecycle scripts

| Script | Risk | Review guidance |
|--------|------|-----------------|
| `preinstall` | HIGH | Runs before dependencies resolve -- can execute before lockfile integrity check |
| `install` | MEDIUM | Typically used for native addon compilation (node-gyp); verify it only compiles bundled source |
| `postinstall` | HIGH | Most common vector for supply chain attacks; check for `curl`, `wget`, encoded strings, `eval()` |
| `prepare` | LOW | Runs on `git` installs; usually build step |
| `binding.gyp` in package root, no `install`/`preinstall` | MEDIUM | npm and pnpm synthesize `install: node-gyp rebuild`; build code runs and needs approval like any `install` script. `gypfile: false` disables it |

### PyPI setup hooks

| Mechanism | Risk | Review guidance |
|-----------|------|-----------------|
| `setup.py` with `cmdclass` override | HIGH | Arbitrary code during `pip install`; check for network calls, file reads outside package dir |
| `pyproject.toml` build backends | MEDIUM | Less surface area than raw `setup.py` but still executes build code |
| `__init__.py` import-time side effects | MEDIUM | Code runs on first import, not install -- but still a supply chain vector |
| `.pth` file in a wheel (`*.pth` in the wheel's `RECORD`) | HIGH | Lines starting with `import` run at **every** Python interpreter start, not only on import or install. Any `.pth` beyond plain path entries needs a stated reason |
| sdist only (no wheel for the target platform) | MEDIUM | pip / uv run the build backend on the user's machine |

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
- **Second-stage droppers**: script downloads a runtime or binary and runs it
- **Persistence**: writes outside the package into IDE/agent or shell config
  (`.vscode/tasks.json`, `.claude/settings.json`, shell rc files, git hooks,
  cron / launch agents); survives uninstall
- **Token-triggered destruction**: deletes files when a token stops working.
  Follow the §4.6 V4 incident-response order (remove persistence before
  revoking credentials)

---

## Transitive Dependency Scanning

Run `scripts/dep-scan.py` to check direct (Tier 2) or full transitive (Tier 3, npm only)
dependencies for known CVEs via the OSV batch API. No package installation required.

### Invocation

```
# Tier 2 — direct deps from registry metadata (all ecosystems):
python3 scripts/dep-scan.py -Ecosystem <eco> -Name "<name>" [-Version "<version>"] -Tier 2

# Tier 3 — full tree resolution (npm only; auto-falls back to Tier 2):
python3 scripts/dep-scan.py -Ecosystem <eco> -Name "<name>" [-Version "<version>"] -Tier 3
```

> **PowerShell hosts:** each `scripts/<script>.py` has a `scripts/<script>.ps1` twin taking identical arguments (e.g. `.\scripts\vuln-lookup.ps1 -Ecosystem npm -Name "lodash"`).

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
| `high` | Third-party component (`references/criteria.md` §4.3) → HIGH flag → CONDITIONAL. Cite dep name(s) + CVE IDs. Condition: a version of this package, or a lockfile override, that resolves to the fixed dep version. |
| `critical` | Check each CRITICAL against CISA KEV. KEV-listed → REJECTED (Blocking CVE); name the fixed dep version. Otherwise HIGH flag → CONDITIONAL, same condition as `high`. |

**Transitive vs direct:** Use the `depth` field in each finding. Every dependency
is a third-party component under §4.3, so depth never makes a finding a Blocking
CVE (only KEV does). Depth shapes the condition: a `depth: 1` finding usually needs
a new release of this package or an override; a `depth > 1` finding warrants a
flag and citation — report it and let the reviewer weigh reachability. Tier 2
always emits `depth: 1`; Tier 3 reflects actual tree depth.

### Depth thresholds

| Signal | Risk level | Action |
|---|---|---|
| `directDepCount` > 50 | Medium | Flag dependency bloat; increased attack surface |
| Any dep with `severity: CRITICAL` | Critical | Flag regardless of depth |
| Any dep with `severity: HIGH` in `findings` | High | Flag; cite CVE IDs |

### Audit coverage row guidance

For the **Transitive dependencies** row in the Audit Coverage table:

- `Done -- dep-scan T2: 8 deps, none HIGH+ (OSV)`
- `Done -- dep-scan T2: 1 HIGH CVE in minimist@0.0.8 (CVE-2020-7598, OSV)`
- `Done -- dep-scan T3: 12 direct, 147 transitive, riskLevel: none (OSV)`
- `Done -- dep-scan T3→T2 fallback (npm CLI unavailable): 8 deps, none HIGH+ (OSV)`
- `Skipped -- Tier 1 quick audit`

---

## Typosquat Detection (Algorithmic + Manual)

For **npm** packages, run the algorithmic typosquat check before manual review:

```
python3 scripts/typosquat-check.py -Ecosystem npm -Name "<exact name>"
```

Add `-CompareTo "<known legitimate name>"` when the user or context supplies a
canonical package name to compare against.

The baseline is a bundled snapshot of the 1,000 most-downloaded unscoped npm
packages (`scripts/data/npm-popular.tsv`; refresh with
`python3 scripts/data/refresh-npm-popular.py`). A queried name that is itself in
the baseline is reported `low` without distance or combosquat scoring. Scoped
names are compared by unscoped basename only -- verify scope ownership manually
(see below).

### Interpreting script output

The script emits a JSON object with:

| Field | Meaning |
|-------|---------|
| `riskLevel` | `low` / `medium` / `high` / `critical` -- algorithmic risk assessment |
| `closestMatches` | Top packages by edit distance, with distance and weekly downloads (baseline snapshot; the best match gets the live count when the npm downloads API answers) |
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
  `Done — typosquat-check: low risk` or
  `Done — typosquat-check: high risk, manual review confirms squat`.
- **Other ecosystems**: Until script support is added, use manual comparison:
  `Done — manual character-by-character check`.

---

## Multi-Database CVE Correlation

Run `scripts/vuln-lookup.py` before web search to query structured vulnerability
databases for registry packages.

### Invocation

```
python3 scripts/vuln-lookup.py -Ecosystem <eco> -Name "<name>" [-Version "<version>"]
```

**Supported ecosystems:** npm, pypi, crates, rubygems, nuget, go, maven, hex.
IaC registries (Terraform, Ansible, Helm): fall back to web search — OSV/GHSA
ecosystem mapping for these is not yet established.

**GITHUB_TOKEN:** Set `GITHUB_TOKEN` (`export GITHUB_TOKEN=…`; PowerShell: `$env:GITHUB_TOKEN = '…'`) to raise GHSA rate limit from 60/hr to
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
| `high` | Cite CVE IDs and affected ranges. Fixed release exists → HIGH flag → CONDITIONAL (condition: install the fixed version; pin lockfile). No fixed release → Blocking CVE → REJECTED (`SKILL.md` Tree terms). |
| `critical` | Check CISA KEV first. KEV-listed → REJECTED even when fixed (name the fixed release). Not KEV: no fixed release → REJECTED; fixed release → HIGH flag → CONDITIONAL. A version affirmatively outside the affected range is unaffected — document the range check. |
| Discrepancy (one DB only) | Flag and investigate. May be ingestion lag or a withdrawn advisory. Document in Security row; do not silently discard. |

### When `-Version` is supplied

The script cross-checks each vulnerability's affected version ranges against the
requested version. Conservative: if range data is absent, the vulnerability is
included (not silently dropped). `riskLevel` reflects only vulns that affect the
specified version.

### Audit coverage row guidance

For the **CVE / vulnerability databases** row in the Audit Coverage table:

- Reference `vuln-lookup` output: e.g.,
  `Done -- vuln-lookup: none found (OSV, GHSA)` or
  `Done -- vuln-lookup: 2 CVEs (OSV: CVE-2021-23337, checked: OSV, GHSA)`.
- If GHSA was skipped: `Done -- vuln-lookup: none found (OSV only -- GHSA skipped)`.
- For IaC registries (script not yet supported): use web search and note it:
  `Done -- web search: no advisories found`.
