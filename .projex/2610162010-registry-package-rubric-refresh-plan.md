# Registry-Package Rubric Refresh

> **Status:** In Progress
> **Author:** Claude (Opus)
> **Parent:** 2610161927-registry-package-and-ci-action-stewardship-review-eval.md
> **Source:** 2610161927-registry-package-and-ci-action-stewardship-review-eval.md (RP-1, RP-2, RP-4, RP-5, RP-6, RP-7 npm part, RP-9) + Hand-off row "registry-package" of 2610161941-shared-version-integrity-floor-plan.md (C6 alignment, §4.3 / §4.6 plug-ins) + human decision on Tier 1 identity (2026-10-17, via orchestrator; see Revision Log)
> **Related Projex:** 2610161941-shared-version-integrity-floor-walkthrough.md (contract this builds on; closed `20843cc`) | 2610161926-lookup-script-correctness-fixes-walkthrough.md (last edit to the addendum + scripts) | 2604070218-install-auditor-subject-typed-redesign-nav.md | siblings in flight: 2610162005-ci-action-rubric-refresh-plan.md (owns `references/registries.md` §CI/CD) · 2610162003-ide-plugin-rubric-refresh-plan.md (owns Cursor row) · 2610162004-container-image-rubric-refresh-plan.md (owns §Container Images)
> **Worktree:** Yes

---

## Summary

The registry-package rubric still scores trust per **package** (adoption, age, "provenance present"). The 2025–26 attacks were per **version**: hijacked publishes of popular packages, often with valid provenance. The shared floor (`references/criteria.md` §4.6 V1–V5, §4.3 Blocking CVE) now states the rules. It leaves per-subject plug-ins empty, and the registry addendum still contradicts it in three places:
- `vuln-lookup` `critical` = "REJECTED lean"
- direct-dep CVE = "same weight as the package's own"
- "Missing provenance → CONDITIONAL"

This plan:
1. **Tooling (RP-7, npm only):** `registry-lookup` emits `publisher`, `trustedPublisher`, `provenance`, `previousVersion` and `removedVersions`. All are already in the fetched packument, so there are no new HTTP calls. Offline tests cover both twins.
2. **Addendum:**
   - Rewrites the trust-signal table (RP-5): PGP row dropped; trusted publishing for npm, PyPI, crates.io, RubyGems and NuGet; Go sumdb = consistency, not identity.
   - Scoring = §4.6 V2 "origin, not safety".
   - Tier 1 gains version-age and continuity rows (RP-1/RP-2). Per the human's decision, missing trusted publishing or provenance does **not** block Tier 1. A change of signer, trusted-publisher config or publisher from the previous release does block it, and a publisher change forces Tier 3.
   - Adoption bars use each script field's own time window (RP-9).
   - Adds the client execution model: npm 12 / pnpm 10 / Bun block dependency scripts. Adds the `binding.gyp`, `.pth`, dropper and persistence vectors (RP-4).
   - C6 alignment of both CVE tables.
   - New `## CVE Scope (§4.3)` (heading shared with the sibling addenda) and `## Version & Update Integrity (§4.6)` plug-ins: cooldown table, identity sources, diff rules, incident sources, update controls.
3. **Workflow:** wires the above into Identify, Tier 1/3, research, coverage and verdict notes.
4. **`references/registries.md`:** language-registry rows only (RP-6).

Every product fact below was checked against a primary source at planning time (2026-10-16): the clients' own shipped docs or changelogs, live registry API responses, or `go help environment`. The few from-memory facts are marked in Notes → Unverified.

**Scope:** `references/criteria/registry-package.md` | `workflows/registry-package.md` | `references/registries.md` (§JavaScript…§.NET rows only) | `scripts/registry-lookup.py` + `.ps1` (npm function only) | `tests/test_lookup_scripts.py`. No `SKILL.md`, `references/criteria.md`, `evals/`, `STEWARDSHIP.md`.
**Estimated Changes:** 6 files. Addendum ≈ +10 KB (17.2 → ~27 KB), workflow ≈ +3 KB, registries.md ≈ +1.2 KB, script +~45 lines per twin, tests +~45 lines.

---

## Objective

### Problem / Gap / Need

| ID | Gap (verified at planning) | Fix (step) |
|---|---|---|
| RP-1 | Tier 1 gates on *package* age. Triage runs `registry-lookup` without `-Version`, so a pinned request's age is never read | Tier 1 row `daysSincePublish ≥ 7`; triage passes `-Version`; V1 plug-in names source per ecosystem + client cooldowns (2, 3) |
| RP-2 | "+1 trust… strong positive" on mere presence; "Presence is a strong positive" in workflow §4.1; no continuity check; script has no identity fields | Scoring per V2; V3 diff rules; script emits identity of the version + previous version (1, 2, 3) |
| RP-4 | Rubric assumes scripts always run. npm 12.0.0 (2026-07-08) and pnpm ≥ 10 block dependency scripts until approved. The patterns list lacks `binding.gyp`, `.pth`, droppers and persistence | "Client execution model" + new rows/patterns (2, 3) |
| RP-5 | PyPI "PGP/Sigstore signature" row wrong; TP missing for npm/crates/RubyGems/NuGet; `GONOSUMCHECK` row (absent from `go help environment`, go1.24.7); Maven Sigstore missing | Trust table rewrite (2) |
| RP-6 | `registries.md`: PyPI "No mandatory publishing auth"; Go "High trust for modules in the index" + "Direct VCS installs bypass this" (they still hit sumdb unless `GONOSUMDB`/`GOPRIVATE`/`GOSUMDB=off`) | Row rewrites (4) |
| RP-7 (npm) | No `_npmUser`, `trustedPublisher`, `dist.attestations` in output | Script fields + tests (1) |
| RP-9 | "100K crates.io all-time" is meaningless: every Tier 1 example crate has > 1B total, e.g. serde 1.54B total / 368M per 90 d (live). Windows are mixed (weekly / monthly / all-time); the Tier 1 row says "weekly" for PyPI | Per-field adoption table (2) |
| C6 align | Addendum: `vuln-lookup` `critical` = "REJECTED lean", `high` = "CONDITIONAL lean" even when unfixed; `dep-scan` direct dep "same verdict weight as a CVE in the package itself"; workflow "Unpatched CRITICAL/HIGH CVE" | Rewrite to §4.3 classes; §4.3 boundary plug-in (2, 3) |
| Eval-8 contradiction | Workflow "Missing provenance when mechanism exists → CONDITIONAL" vs addendum "not auto-flag" vs eval 8 exact-APPROVED for chalk@5.3.0 (no TP/provenance, verified) | Never-used = note only (2, 3) |

### Success Criteria

- [ ] `registry-lookup` (both twins) npm output has keys `publisher`, `trustedPublisher` (`{id, oidcConfigId}` or null), `provenance` (predicateType or null), `previousVersion` (object or null) and `removedVersions` (array). Non-npm output is unchanged.
- [ ] `python3 -m unittest discover -s tests -p "test_*.py"` with pwsh on PATH: **23** tests, OK (baseline 19 + 4 new). Without pwsh: OK with the PowerShell classes skipped.
- [ ] Addendum has exactly one `## Version & Update Integrity (§4.6)` heading with bullets `**V1**`…`**V5**` in order, and exactly one `## CVE Scope (§4.3)` heading directly before it.
- [ ] Tier 1 (addendum table + workflow list):
  - identity evidence is **not required**
  - no change of signer, trusted-publisher config or publisher from the previous release
  - adoption above the Tier 1 bar
  - version ≥ 7 d
  - wording keeps §4.6 V2 ("verified identity never enough on its own for Tier 1 or APPROVED")

  A publisher change is a Tier 3 trigger in both files. The old Tier 1 identity requirement is gone ("Verified per "Ecosystem Trust Signals" OR ecosystem has no mechanism", "Identity verified per the addendum", "satisfies the Tier 1 identity row").
- [ ] Every `§4.6 V<n>` reference in the 3 doc files names V1–V5. Every script field named in docs exists in the Python npm output.
- [ ] Stale phrases gone from the 3 doc files (case-sensitive list in Verification Plan).
- [ ] `python3 evals/run_evals.py validate` passes; `python3 -m unittest discover -s evals -p "test_*.py"` → 12 tests OK.
- [ ] `git diff --stat <base>..HEAD` lists exactly the 6 files. `references/registries.md` diff touches only lines inside §JavaScript…§.NET.
- [ ] Paper traces R1–R10 produce the stated outcomes.

### Out of Scope

- `SKILL.md` Red Flags / tree (RP-3 done by the floor). `references/criteria.md` (shared; §4.6 and §4.3 already landed). `references/criteria.md` §4.1 Registry Source table: consistent with this plan, left alone.
- `references/registries.md` §CI/CD (ci-action plan), §Container Images (container plan), §IDE incl. the Cursor row (ide-plugin plan), §Browser.
- Scorecard host `api.securityscorecards.dev` (RP-8): separate patch-projex. The host is still unverified, and the string appears in the workflow, `criteria.md` and the script.
- PyPI provenance / `project-status` fields in the script. RubyGems `-Version` support: `lookup_rubygems` ignores `version` and always reports latest. Both are documented as manual checks here → tooling follow-on (Notes).
- `evals/` (needed changes listed in Notes → Eval hand-off). `STEWARDSHIP.md` dates + F-P1 watch list (orchestrator). Live eval run (human: once, after all refreshes).

---

## Context

### Current State

- **Base** `claude/youthful-dijkstra-5ov1kt` @ `8564410` (re-checked 2026-10-17). Floor squash-merged at `20843cc`, and all other subject refreshes have closed since. Between `20843cc` and `8564410` none of this plan's 6 files changed, except `references/registries.md`: the ide-plugin plan rewrote the Cursor row into L72–73, and the ci-action plan rewrote L80 and L86 (§IDE / §CI/CD). Both are outside Step 4's L5–38 hunks. Floor deltas in my files: `workflows/registry-package.md` §Toward REJECTED. The "Maintainer account compromise confirmed" and "Known malware" bullets (L444–452) are now V4-scoped; nothing else in my files changed.
- `references/criteria.md` now defines §4.6 V1–V5 with `**Addendum:**` lines and §4.3 Blocking CVE (own code / third-party / KEV / VEX). It also adds the `Version integrity (§4.6)` Required coverage row, all tiers. Plug-in convention: one `## Version & Update Integrity (§4.6)` section with bullets labelled `V1`–`V5`. For §4.3, the sibling addenda now on base (browser-extension, ci-action, container-image, desktop-app, ide-plugin) use `## CVE Scope (§4.3)`, placed directly before `## Version & Update Integrity (§4.6)` in most of them. This plan follows that convention.
- `references/criteria/registry-package.md` (17,237 B): §Ecosystem Trust Signals (3-col table + Scoring impact) | §Tier Assignment Thresholds | §Install Script Risk Patterns | §Transitive Dependency Scanning | §Typosquat Detection | §Multi-Database CVE Correlation. Opening paragraph: "the more specific (registry-package) guidance wins". That clause predates the floor; `SKILL.md` Precedence now overrides it for §4.6.
- `workflows/registry-package.md` (~23 KB, wrapped ~78 cols): Identify → Part A triage (Tier 1/2/3 lists) → Part B research → Subject Rubric 4.1–4.6 (its "4.6 Alternatives" is a workflow-local heading; not the criteria §4.6) → Verdict Notes.
- `scripts/registry-lookup.py` `lookup_npm`: fetches the full packument (`registry.npmjs.org/<name>`). It holds `versions[v]._npmUser` (incl. `trustedPublisher {id, oidcConfigId}` on TP publishes), `versions[v].dist.attestations {url, provenance.predicateType}`, and `time` (incl. removed versions). The `.ps1` twin must keep the same keys. pwsh `ConvertFrom-Json` turns `time` values into `[DateTime]` (verified pwsh 7.4.6).
- `tests/test_lookup_scripts.py`: 19 tests (6 PowerShell, skipped without pwsh). `RegistryLookupPython` patches `invoke_api`; `run_ps` runs the `.ps1` behind mocked `Invoke-RestMethod`.

### Verified facts this plan codifies (2026-10-16)

| Fact | Primary evidence |
|---|---|
| npm 12.0.0 published 2026-07-08; latest 12.2.0 | `npm view npm time` |
| npm ≥ 12: dependency install scripts blocked by default; `allowScripts` in package.json; `npm approve-scripts` writes version-pinned `pkg@x.y.z` entries (`--no-allow-scripts-pin` for name-only); `npm approve-scripts --all`; global/`npx` need `--allow-scripts=<pkg>`; covers `preinstall`, `install`, `postinstall`, and `prepare` for non-registry sources | npm 12.2.0 tarball `docs/content/commands/npm-approve-scripts.md`, `using-npm/config.md` |
| npm 12 `allow-git` and `allow-remote` default `none`; `allow-file`/`allow-directory` default `all` | same `config.md` |
| `min-release-age` = Number of **days**; added in 11.10.0 (absent in 11.9.0) | config.md in npm 11.9.0 / 11.10.0 / 12.2.0 tarballs |
| `binding.gyp` in package root without `install`/`preinstall` → npm defaults `install` to `node-gyp rebuild`; `gypfile: false` disables | npm 12 `using-npm/scripts.md`, `configuring-npm/package-json.md` |
| `npm audit signatures` verifies registry signatures **and** provenance attestations; `--json --include-attestations` | npm 12 `commands/npm-audit.md` |
| npm trusted publishing (`npm trust`, ≥ 11.15.0) and staged publishing (`npm stage`) exist | npm 12 `commands/npm-trust.md`, `npm-stage.md` |
| Packument per version: `_npmUser {name, trustedPublisher {id, oidcConfigId}}`, `dist.attestations {url, provenance {predicateType}}`; TP without provenance occurs (prettier 3.9.10) | live registry: `@tanstack/react-query`, `express`, `prettier` |
| Removed versions stay in `time` but leave `versions` (chalk `5.6.1`) | live `registry.npmjs.org/chalk` |
| npm "security holding package", versions `0.0.1-security` | live `crossenv`, `discord.dll` |
| pnpm `minimumReleaseAge` (minutes) from 10.16.0; `trustPolicy: no-downgrade` from 10.21.0; current pnpm (12.14.0) has a built-in non-strict 1440-minute default; `allowBuilds` / `pnpm approve-builds`; pnpm synthesizes `node-gyp rebuild` for `binding.gyp` | pnpm 10.15.1/10.16.0/10.20.0/10.21.0/12.14.0 tarballs + 12.14.0 `CHANGELOG.md` |
| Yarn berry `npmMinimalAgeGate` (DURATION, unit m, default `"1d"` for new projects); present 4.10.3, absent 4.9.4 | `@yarnpkg/cli-dist` 4.9.4 / 4.10.3 / 4.18.1 bundles |
| Bun `minimumReleaseAge` in **seconds** ("Expected number of seconds for minimumReleaseAge", `--minimum-release-age <NUM>`); present 1.3.0, absent 1.2.23 | `@oven/bun-linux-x64` binary strings (not executed) |
| uv `--exclude-newer` accepts RFC 3339, friendly (`1 week`, `30 days`) and ISO-8601 durations; compares per-file upload time | `uv help pip install`, uv 0.11.32 |
| pip `--uploaded-prior-to` from 26.0 (datetime); `P<n>D` duration from 26.1 | `pip/_internal/cli/cmdoptions.py` in pip 25.3/26.0/26.1/26.2.1 wheels |
| PyPI simple API JSON v1.4: `files[].provenance` URL, `files[].upload-time`, top-level `project-status`; integrity API bundle `publisher {kind, repository, workflow}` | live `pypi.org/simple/sampleproject/` + integrity URL |
| requests, flask newest files carry provenance; django, litellm do not | live simple API |
| crates.io per version: `trustpub_data {provider, repository, run_id, sha}`, `published_by`; serde/tokio `trustpub_data: null` | live `crates.io/api/v1/crates/{serde,tokio,uv-version}` |
| RubyGems per-version `created_at` via `/api/v1/versions/<gem>.json` | live `rails` |
| Go proxy `/@v/<ver>.info` → `Time` + `Origin {VCS, URL, Ref, Hash}` | live `proxy.golang.org/github.com/google/uuid/@v/v1.6.0.info` |
| `GONOSUMCHECK` not a Go env var; `GOINSECURE does not disable checksum database validation. GOPRIVATE or GONOSUMDB may be used to achieve that.` | `go help environment`, go1.24.7 |
| Maven Central: PGP still required; Sigstore bundles validated, optional (Jan 2025) | central.sonatype.org news 20250128 (via WebSearch, official) |
| NuGet.org trusted publishing (GitHub OIDC → short-lived key) | devblogs.microsoft.com, learn.microsoft.com (via WebSearch, official) |
| PyPI removed PGP signature support May 2023 | LWN coverage (via WebSearch); PyPI blog not surfaced |
| `vuln-lookup` passes every OSV `id` through unfiltered (so `MAL-` records appear) | `scripts/vuln-lookup.py` `invoke_osv_query` read |

### Key Files

| File | Role | Change Summary |
|---|---|---|
| `scripts/registry-lookup.py` | npm/PyPI/… metadata lookup | `lookup_npm` + 2 helpers: identity + previous/removed versions |
| `scripts/registry-lookup.ps1` | PowerShell twin | Same keys; 3 helpers |
| `tests/test_lookup_scripts.py` | Offline regression suite | 1 fixture, 4 tests, 2 asserts added to existing single-entry tests |
| `references/criteria/registry-package.md` | Registry addendum | Header precedence; trust table + scoring; Tier 1/3 + adoption; client model + vectors; C6 tables; §4.3 + §4.6 plug-ins |
| `workflows/registry-package.md` | Registry workflow | Identify item 7; triage `-Version`; Tier 1/3 lists + examples; research Q2/Q5; coverage row; verdict notes |
| `references/registries.md` | Cross-type registry guide | 9 language-registry lines |

### Dependencies

- **Requires:** floor closed on base: `20843cc` contains `## 4.6 Version & Update Integrity (shared floor)` in `references/criteria.md`; walkthrough in `.projex/closed/`. Also `7f137d1` (lookup-script fixes) on base. Preflight verifies both.
- **Siblings (all closed on base `8564410`):** their `references/registries.md` edits are in §IDE / §CI/CD. No file overlap otherwise. Nothing concurrent remains, so no rebase is expected.
- **Blocks:** eval-refresh plan (new registry cases, Notes → Eval hand-off). Optional tooling follow-on (PyPI provenance, RubyGems `-Version`).

### Constraints

- Shipped-doc style: `workflows/*.md` and addendum prose wrap at ~78 cols; tables are single long lines; addendum uses `--` and `—` interchangeably (keep surrounding style).
- Source Hygiene (scripts): no projex refs; rationale comments name the rejected alternative; twins keep identical JSON keys (`registry-lookup.py` docstring: "same flags, same JSON keys").
- Addenda may tighten §4.6 and fill its plug-ins, never loosen it. They cannot change the §4.3 verdict classes.
- Preserve parsed strings and coverage row labels (`Version integrity` label comes from `criteria.md`).
- No secondary-source product facts in shipped text without a hedge. Every product fact in the After blocks is in the Verified table, or listed in Notes → Unverified with its hedge.

### Assumptions

- **A1:** Before strings below match exactly once at `8564410` (re-simulated 2026-10-17: all edits applied in order to a scratch export of `8564410`). Execution: an Edit miss means the base moved, so re-read that region; don't improvise.
- **A2:** No eval assertion matches the changed wording. Checked: registry evals assert on verdicts, `## Audit Coverage`, `Audit confidence`, typosquat/dep-scan concepts and "Tier 1 / Quick" (eval 0 only). Tier 1 eligibility of express depends on the date (express 5.3.0 published 2026-10-09). That timing effect was already handed to the eval plan by the floor.
- **A3:** pwsh 7.4.6 is at `<scratchpad>/pwsh/pwsh` (prepend to PATH for the test run). Without it the PS tests skip and parity rests on review of Step 1's twin code.
- **A4:** `registry-lookup` `lookup_crates` without `-Version` reports `versions[0]` = newest (crates API returns newest first); its V1 use needs no change.

### Impact Analysis

- **Direct:** 6 files above.
- **Adjacent:**
  - `SKILL.md` Quick skeleton row `Version integrity`, and the report template, read the fields this plan names. No change needed.
  - `references/criteria.md` §4.6 `**Addendum:**` lines are now filled for registry packages.
  - The `dep-scan`/`vuln-lookup` scripts are unchanged; only the interpretation tables change.
- **Downstream (live verdicts):**
  - Popular packages without trusted publishing/provenance can now reach Tier 1, as long as nothing changed from the previous release and V1 holds. Checked: lodash, django, serde and tokio have no TP/provenance. Under the old npm/PyPI rule ("Attestation present OR no mechanism") they could not reach Tier 1.
  - Tier 1 is lost by: version < 7 d; any change of signer, trusted-publisher config or publisher; a past compromise.
  - A publisher change now forces Tier 3.
  - chalk-like packages no longer get a "missing provenance" CONDITIONAL.
  - Unfixed own-code HIGH → REJECTED. Fixed CRITICAL (non-KEV) → CONDITIONAL, not "REJECTED lean".
  - Dependency KEV CRITICAL → REJECTED. Other dependency HIGH/CRITICAL → CONDITIONAL.
  - npm 12 / pnpm users get a script-approval condition instead of an assumed-run rating.

---

## Implementation

### Overview

Preflight → Step 1 tooling (docs in Steps 2–3 name its fields) → Step 2 addendum → Step 3 workflow (references addendum section names) → Step 4 registries.md. Every edit is an exact `Before → After` pair applied with the Edit tool; Before strings occur once in their file.

**Preflight** (in `<work-root>`):
```bash
git merge-base --is-ancestor 20843cc HEAD && echo floor-on-base                         # floor-on-base
git merge-base --is-ancestor 8564410 HEAD && echo siblings-on-base                      # siblings-on-base (anchors re-checked here)
grep -c "^## 4.6 Version & Update Integrity (shared floor)" references/criteria.md     # 1
grep -c "^- \*\*Addendum:\*\*" references/criteria.md                                  # 6
ls .projex/closed/2610161941-shared-version-integrity-floor-walkthrough.md
grep -c "§4.6 V4" workflows/registry-package.md                                         # 2 (floor 5a/5b)
grep -c "Version & Update Integrity" references/criteria/registry-package.md            # 0
wc -c references/criteria/registry-package.md workflows/registry-package.md references/registries.md
PATH="<scratchpad>/pwsh:$PATH" python3 -m unittest discover -s tests -p "test_*.py" 2>&1 | tail -3   # Ran 19, OK
python3 -m unittest discover -s evals -p "test_*.py" 2>&1 | tail -3                     # Ran 12, OK
python3 evals/run_evals.py validate | tail -3                                           # pass
```
Any mismatch in the first five lines → stop: floor not landed or the base moved (report as Blocked).

---

### Step 1: npm identity + continuity fields in `registry-lookup` (both twins) + tests

**Objective:** emit what §4.6 V2/V3/V4 need for npm with no new HTTP calls.
**Confidence:** High. Logic prototyped against live chalk/lodash/express/react/prettier/@tanstack/react-query packuments at planning: chalk 5.6.2 → previous 5.6.0, skipping removed 5.6.1. pwsh `[DateTime]` typing confirmed.
**Depends on:** Preflight
**Verify-Projex:** Encouraged (twin parity is easy to get subtly wrong)

**Files:** `scripts/registry-lookup.py` | `scripts/registry-lookup.ps1` | `tests/test_lookup_scripts.py`

**Output contract (npm only; appended after `engines`):**

| Key | Value |
|---|---|
| `publisher` | `versions[v]._npmUser.name` or null |
| `trustedPublisher` | `{"id": …, "oidcConfigId": …}` from `_npmUser.trustedPublisher`, or null |
| `provenance` | `dist.attestations.provenance.predicateType` or null |
| `previousVersion` | null, or `{version, publishedAt, publisher, trustedPublisher, provenance, installHooks[]}` for the still-served version published immediately before `v` by `time`; prereleases skipped unless `v` is one |
| `removedVersions` | versions present in `time` but absent from `versions` (array, possibly empty) |

**Changes — Python (`scripts/registry-lookup.py`):**

```python
# 1a Before:
def lookup_npm(name, version):
    pkg = invoke_api("https://registry.npmjs.org/" + _enc(name))

# 1a After:
def _npm_identity(version_data):
    """Publisher account, trusted-publisher config and provenance type of one version."""
    user = version_data.get("_npmUser")
    user = user if isinstance(user, dict) else {}
    tp = user.get("trustedPublisher")
    att = (version_data.get("dist") or {}).get("attestations")
    prov = att.get("provenance") if isinstance(att, dict) else None
    return {
        "publisher": user.get("name"),
        "trustedPublisher": {"id": tp.get("id"), "oidcConfigId": tp.get("oidcConfigId")} if isinstance(tp, dict) else None,
        "provenance": prov.get("predicateType") if isinstance(prov, dict) else None,
    }


def _npm_previous_version(versions, time_map, current):
    """The still-served version published immediately before `current`.

    Prereleases are skipped unless `current` is one: canary builds often come from a
    different pipeline, so comparing a stable release with one reports false identity
    breaks. Versions missing from `versions` (unpublished or removed by the registry)
    are skipped because their metadata is gone; `removedVersions` lists them instead.
    """
    cur = _parse_dt(time_map.get(current))
    if cur is None:
        return None
    best = None
    for v, t in time_map.items():
        if v in ("created", "modified") or v == current or v not in versions:
            continue
        if "-" in v and "-" not in current:
            continue
        d = _parse_dt(t)
        if d is not None and d < cur and (best is None or d > best[1]):
            best = (v, d)
    return best[0] if best else None


def lookup_npm(name, version):
    pkg = invoke_api("https://registry.npmjs.org/" + _enc(name))
```

```python
# 1b Before (end of lookup_npm):
    repo = pkg.get("repository")
    repository = repo if isinstance(repo, str) else (repo.get("url") if isinstance(repo, dict) else None)

    return {

# 1b After:
    repo = pkg.get("repository")
    repository = repo if isinstance(repo, str) else (repo.get("url") if isinstance(repo, dict) else None)

    identity = _npm_identity(version_data)
    previous_version = None
    prev = _npm_previous_version(versions, time_map, latest)
    if prev:
        prev_data = versions.get(prev) or {}
        prev_scripts = prev_data.get("scripts") or {}
        prev_identity = _npm_identity(prev_data)
        previous_version = {
            "version": prev,
            "publishedAt": format_date_str(time_map.get(prev)),
            "publisher": prev_identity["publisher"],
            "trustedPublisher": prev_identity["trustedPublisher"],
            "provenance": prev_identity["provenance"],
            "installHooks": [h for h in ("preinstall", "install", "postinstall") if prev_scripts.get(h)],
        }
    removed_versions = [v for v in time_map if v not in ("created", "modified") and v not in versions]

    return {
```

```python
# 1c Before:
        "engines": version_data.get("engines"),
    }


def lookup_pypi(name, version):

# 1c After:
        "engines": version_data.get("engines"),
        "publisher": identity["publisher"],
        "trustedPublisher": identity["trustedPublisher"],
        "provenance": identity["provenance"],
        "previousVersion": previous_version,
        "removedVersions": removed_versions,
    }


def lookup_pypi(name, version):
```

**Changes — PowerShell (`scripts/registry-lookup.ps1`):**

```powershell
# 1d Before:
function Lookup-Npm {
    $pkg = Invoke-Api "https://registry.npmjs.org/$([Uri]::EscapeDataString($Name))"

# 1d After:
function ConvertTo-UtcDate {
    # ConvertFrom-Json already turns ISO-8601 strings into [DateTime], but a registry
    # that serves another shape still arrives as a string; parsing only strings would
    # silently drop every [DateTime] and find no previous version.
    param($Value)
    if ($null -eq $Value) { return $null }
    if ($Value -is [DateTime]) { return $Value.ToUniversalTime() }
    try {
        return ([DateTimeOffset]::Parse([string]$Value, [Globalization.CultureInfo]::InvariantCulture)).UtcDateTime
    } catch {
        return $null
    }
}

function Get-NpmIdentity {
    param($VersionData)
    $user = $VersionData.'_npmUser'
    $tp = if ($user) { $user.trustedPublisher } else { $null }
    $prov = if ($VersionData.dist -and $VersionData.dist.attestations) { $VersionData.dist.attestations.provenance } else { $null }
    return [ordered]@{
        publisher        = if ($user) { $user.name } else { $null }
        trustedPublisher = if ($tp) { [ordered]@{ id = $tp.id; oidcConfigId = $tp.oidcConfigId } } else { $null }
        provenance       = if ($prov) { $prov.predicateType } else { $null }
    }
}

function Get-NpmPreviousVersion {
    # Prereleases are skipped unless $Current is one: canary builds often come from a
    # different pipeline, so comparing a stable release with one reports false identity
    # breaks. Versions no longer served are skipped because their metadata is gone.
    param($Pkg, [string]$Current)
    if (-not $Current -or -not $Pkg.time) { return $null }
    $curT = ConvertTo-UtcDate $Pkg.time.$Current
    if (-not $curT) { return $null }
    $best = $null
    $bestT = $null
    foreach ($p in $Pkg.time.PSObject.Properties) {
        $v = $p.Name
        if ($v -in @('created','modified') -or $v -eq $Current) { continue }
        if (-not $Pkg.versions.PSObject.Properties[$v]) { continue }
        if ($v.Contains('-') -and -not $Current.Contains('-')) { continue }
        $t = ConvertTo-UtcDate $p.Value
        if ($t -and $t -lt $curT -and (-not $bestT -or $t -gt $bestT)) {
            $best = $v
            $bestT = $t
        }
    }
    return $best
}

function Lookup-Npm {
    $pkg = Invoke-Api "https://registry.npmjs.org/$([Uri]::EscapeDataString($Name))"
```

```powershell
# 1e Before:
    # Dependencies
    $deps = @()
    if ($versionData.dependencies) {
        $deps = @($versionData.dependencies.PSObject.Properties.Name)
    }

    return [ordered]@{
        ecosystem        = 'npm'

# 1e After:
    # Dependencies
    $deps = @()
    if ($versionData.dependencies) {
        $deps = @($versionData.dependencies.PSObject.Properties.Name)
    }

    $identity = Get-NpmIdentity $versionData
    $previousVersion = $null
    $prev = Get-NpmPreviousVersion $pkg $latest
    if ($prev) {
        $prevData = $pkg.versions.$prev
        $prevIdentity = Get-NpmIdentity $prevData
        $previousVersion = [ordered]@{
            version          = $prev
            publishedAt      = Format-DateStr $time.$prev
            publisher        = $prevIdentity.publisher
            trustedPublisher = $prevIdentity.trustedPublisher
            provenance       = $prevIdentity.provenance
            installHooks     = @(@('preinstall','install','postinstall') | Where-Object { $prevData.scripts.$_ })
        }
    }
    $removedVersions = @()
    if ($time) {
        $removedVersions = @($time.PSObject.Properties.Name | Where-Object { $_ -notin @('created','modified') -and -not $pkg.versions.PSObject.Properties[$_] })
    }

    return [ordered]@{
        ecosystem        = 'npm'
```

```powershell
# 1f Before:
        engines          = $versionData.engines
    }
}

# 1f After:
        engines          = $versionData.engines
        publisher        = $identity.publisher
        trustedPublisher = $identity.trustedPublisher
        provenance       = $identity.provenance
        previousVersion  = $previousVersion
        removedVersions  = $removedVersions
    }
}
```
(Direct assignment of an `@()` array into the ordered dict keeps 1-element and empty arrays as JSON arrays. Only `if`-as-value unrolls, per the existing `installScripts` comment. `ConvertTo-Json -Depth 5` already covers the 3-level `previousVersion.trustedPublisher`.)

**Changes — tests (`tests/test_lookup_scripts.py`):**

```python
# 1g Before:
BASELINE_TSV = """# fixture baseline

# 1g After:
NPM_IDENTITY_DRIFT = {
    "name": "fixpkg", "description": "fixture", "dist-tags": {"latest": "1.1.0"},
    "maintainers": [{"name": "solo"}],
    "versions": {
        "1.0.0": {"license": "MIT",
                  "_npmUser": {"name": "GitHub Actions",
                               "trustedPublisher": {"id": "github", "oidcConfigId": "cfg-1"}},
                  "dist": {"attestations": {"url": "https://registry.npmjs.org/-/npm/v1/attestations/fixpkg@1.0.0",
                                            "provenance": {"predicateType": "https://slsa.dev/provenance/v1"}}}},
        "1.1.0-beta.1": {"license": "MIT", "_npmUser": {"name": "canary-bot"}},
        "1.1.0": {"license": "MIT", "_npmUser": {"name": "solo"}, "scripts": {"preinstall": "node setup.js"}},
    },
    # 1.0.1 is in `time` but no longer served: removed, like a pulled malicious release.
    "time": {"created": "2020-01-01T00:00:00Z", "modified": "2020-03-01T00:00:00Z",
             "1.0.0": "2020-01-01T00:00:00Z", "1.0.1": "2020-01-15T00:00:00Z",
             "1.1.0-beta.1": "2020-02-01T00:00:00Z", "1.1.0": "2020-03-01T00:00:00Z"},
}
DRIFT_ROUTES = [{"match": "registry.npmjs.org", "body": NPM_IDENTITY_DRIFT}, {"match": "", "fail": True}]
DRIFT_PREVIOUS = {"version": "1.0.0", "publisher": "GitHub Actions",
                  "trustedPublisher": {"id": "github", "oidcConfigId": "cfg-1"},
                  "provenance": "https://slsa.dev/provenance/v1", "installHooks": []}


def without(d, *keys):
    return {k: v for k, v in d.items() if k not in keys}


BASELINE_TSV = """# fixture baseline
```

```python
# 1h Before (RegistryLookupPython):
    def test_single_entries_are_arrays(self):
        npm = run_main(self.mod, ["npm", "fixpkg"])
        self.assertEqual((npm["maintainers"], npm["maintainerCount"], npm["installScripts"]), (["solo"], 1, ONE_HOOK))
        pypi = run_main(self.mod, ["pypi", "fixpkg"])
        self.assertEqual((pypi["maintainers"], pypi["maintainerCount"]), (["solo"], 1))


@unittest.skipUnless(PWSH, "pwsh not on PATH")
class RegistryLookupPowerShell(unittest.TestCase):
    def test_single_entries_are_arrays(self):
        npm = run_ps("registry-lookup", {"Ecosystem": "npm", "Name": "fixpkg"}, REGISTRY_ROUTES)
        self.assertEqual((npm["maintainers"], npm["maintainerCount"], npm["installScripts"]), (["solo"], 1, ONE_HOOK))
        pypi = run_ps("registry-lookup", {"Ecosystem": "pypi", "Name": "fixpkg"}, REGISTRY_ROUTES)
        self.assertEqual((pypi["maintainers"], pypi["maintainerCount"]), (["solo"], 1))

# 1h After:
    def test_single_entries_are_arrays(self):
        npm = run_main(self.mod, ["npm", "fixpkg"])
        self.assertEqual((npm["maintainers"], npm["maintainerCount"], npm["installScripts"]), (["solo"], 1, ONE_HOOK))
        self.assertEqual((npm["previousVersion"], npm["removedVersions"], npm["trustedPublisher"]), (None, [], None))
        pypi = run_main(self.mod, ["pypi", "fixpkg"])
        self.assertEqual((pypi["maintainers"], pypi["maintainerCount"]), (["solo"], 1))
        self.assertNotIn("previousVersion", pypi)


class RegistryLookupNpmIdentityPython(unittest.TestCase):
    def setUp(self):
        self.mod = load("registry-lookup")

        def fake_invoke_api(url, timeout=15):
            for r in DRIFT_ROUTES:
                if r["match"] in url:
                    return None if r.get("fail") else r["body"]
        self.mod.invoke_api = fake_invoke_api

    def test_identity_drop_and_removed_version(self):
        out = run_main(self.mod, ["npm", "fixpkg"])
        self.assertEqual((out["publisher"], out["trustedPublisher"], out["provenance"]), ("solo", None, None))
        self.assertEqual(without(out["previousVersion"], "publishedAt"), DRIFT_PREVIOUS)
        self.assertEqual(out["previousVersion"]["publishedAt"], "2020-01-01")
        self.assertEqual(out["removedVersions"], ["1.0.1"])

    def test_prerelease_compares_with_any_earlier_version(self):
        out = run_main(self.mod, ["npm", "fixpkg", "1.1.0-beta.1"])
        self.assertEqual((out["publisher"], out["previousVersion"]["version"]), ("canary-bot", "1.0.0"))


@unittest.skipUnless(PWSH, "pwsh not on PATH")
class RegistryLookupPowerShell(unittest.TestCase):
    def test_single_entries_are_arrays(self):
        npm = run_ps("registry-lookup", {"Ecosystem": "npm", "Name": "fixpkg"}, REGISTRY_ROUTES)
        self.assertEqual((npm["maintainers"], npm["maintainerCount"], npm["installScripts"]), (["solo"], 1, ONE_HOOK))
        self.assertEqual((npm["previousVersion"], npm["removedVersions"], npm["trustedPublisher"]), (None, [], None))
        pypi = run_ps("registry-lookup", {"Ecosystem": "pypi", "Name": "fixpkg"}, REGISTRY_ROUTES)
        self.assertEqual((pypi["maintainers"], pypi["maintainerCount"]), (["solo"], 1))

    def test_identity_drop_and_removed_version(self):
        out = run_ps("registry-lookup", {"Ecosystem": "npm", "Name": "fixpkg"}, DRIFT_ROUTES)
        self.assertEqual((out["publisher"], out["trustedPublisher"], out["provenance"]), ("solo", None, None))
        self.assertEqual(without(out["previousVersion"], "publishedAt"), DRIFT_PREVIOUS)
        self.assertEqual(out["removedVersions"], ["1.0.1"])

    def test_prerelease_compares_with_any_earlier_version(self):
        out = run_ps("registry-lookup", {"Ecosystem": "npm", "Name": "fixpkg", "Version": "1.1.0-beta.1"}, DRIFT_ROUTES)
        self.assertEqual((out["publisher"], out["previousVersion"]["version"]), ("canary-bot", "1.0.0"))
```
(PS tests don't assert `publishedAt`: the twin's `Format-DateStr` round-trips `[DateTime]` through local culture, the existing behaviour, so the date is host-timezone dependent. The Python test pins it.)

**Rationale:**
- npm only, because the packument is already fetched (zero new requests, zero new failure modes).
- PyPI provenance needs 2 extra calls per version (simple API + integrity API), and RubyGems pinning needs a different endpoint. Both go to the follow-on; the addendum documents the manual checks.
- `previousVersion` "by publish time": the floor's V3 says "the previous release". Publish-time order matches what a user would have installed before. Semver order would compare a 4.x backport against 5.x (express 5.3.0 → 4.22.3 by time; both from the same TP pipeline, so no false break).
- `oidcConfigId` is exposed because TP-without-provenance (prettier) has no repo in the packument. "Same TP config as the previous version" is the only offline continuity signal there.

**Verification:**
```bash
PATH="<scratchpad>/pwsh:$PATH" python3 -m unittest discover -s tests -p "test_*.py" -v 2>&1 | tail -4   # Ran 23 ... OK
python3 -m unittest discover -s tests -p "test_*.py" 2>&1 | tail -2                                  # OK (skipped=8) without pwsh
git -C <work-root> status --porcelain scripts | grep -c __pycache__                                  # 0
# optional live smoke (network): both twins, same key set
python3 scripts/registry-lookup.py npm chalk | python3 -c "import json,sys;d=json.load(sys.stdin);print('5.6.1' in d['removedVersions'], d['previousVersion']['version'])"
```

**If this fails:** `git -C <work-root> checkout -- scripts/registry-lookup.py scripts/registry-lookup.ps1 tests/test_lookup_scripts.py`. A PS-only failure usually means array unrolling (single `removedVersions` element) or DateTime parsing. Inspect `run_ps` stderr and fix the twin, not the test expectations.

---

### Step 2: Addendum `references/criteria/registry-package.md`

**Objective:** fill the §4.3 and §4.6 plug-ins, align the CVE tables with C6, and fix RP-1/2/4/5/9 inside the addendum.
**Confidence:** High (facts verified; see table). Medium for the adoption bars, which are policy (see Risks). The Tier 1 identity rule follows the human decision verbatim.
**Depends on:** Step 1 (field names)
**Verify-Projex:** Encouraged (C6 + floor-tightening only; easy to loosen §4.6 by accident)

**Files:** `references/criteria/registry-package.md`

**Changes:** 13 replacements (2a–2m).

```markdown
// 2a Before (opening paragraph):
addendum layers on top of the shared rubric in `references/criteria.md`. When
a criterion below conflicts with the shared rubric, the more specific
(registry-package) guidance wins.

// 2a After:
addendum layers on top of the shared rubric in `references/criteria.md`. When
a criterion below conflicts with the shared rubric, the more specific
(registry-package) guidance wins -- except `references/criteria.md` §4.6,
which this file only tightens or fills, and the §4.3 verdict classes.
```

```markdown
// 2b Before (whole §Ecosystem Trust Signals body, from "Each registry" through the last Scoring impact bullet):
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

// 2b After:
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
```

```markdown
// 2c Before (Tier 1 table rows + equivalence + examples):
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

// 2c After:
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
```

```markdown
// 2d Before (Tier 2 table row):
| Weekly downloads (npm-equivalent) | 1K--1M npm / proportional in other ecosystems |

// 2d After:
| Adoption | Between the Tier 3 trigger and the Tier 1 bar (adoption table above) |
```

```markdown
// 2e Before (Tier 3 table, first row):
| Weekly downloads <1K (npm-equivalent) and not a known niche tool | Insufficient community vetting |

// 2e After:
| Adoption below the Tier 3 trigger (adoption table) and not a known niche tool | Insufficient community vetting |
```

```markdown
// 2f Before:
| Will run in CI/CD with access to secrets or production credentials | High blast radius |

// 2f After:
| Will run in CI/CD with access to secrets or production credentials | High blast radius |
| Version to be installed has a §4.6 V3 HIGH (identity dropped or changed, new install hook) or a publisher change from the previous release (V3 plug-in below) | Possible hijacked publish |
```

````markdown
// 2g Before (Install Script Risk Patterns intro + first sub-heading):
Registry packages can execute arbitrary code at install time. These patterns
warrant scrutiny at Tier 2 and mandatory review at Tier 3.

### npm lifecycle scripts

// 2g After:
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
````

```markdown
// 2h Before (npm table last row):
| `prepare` | LOW | Runs on `git` installs; usually build step |

// 2h After:
| `prepare` | LOW | Runs on `git` installs; usually build step |
| `binding.gyp` in package root, no `install`/`preinstall` | MEDIUM | npm and pnpm synthesize `install: node-gyp rebuild`; build code runs and needs approval like any `install` script. `gypfile: false` disables it |
```

```markdown
// 2i Before (PyPI table last row):
| `__init__.py` import-time side effects | MEDIUM | Code runs on first import, not install -- but still a supply chain vector |

// 2i After:
| `__init__.py` import-time side effects | MEDIUM | Code runs on first import, not install -- but still a supply chain vector |
| `.pth` file in a wheel (`*.pth` in the wheel's `RECORD`) | HIGH | Lines starting with `import` run at **every** Python interpreter start, not only on import or install. Any `.pth` beyond plain path entries needs a stated reason |
| sdist only (no wheel for the target platform) | MEDIUM | pip / uv run the build backend on the user's machine |
```

```markdown
// 2j Before (red-flag list, last bullet):
- **Exfiltration patterns**: HTTP POST with collected env vars or file contents

// 2j After:
- **Exfiltration patterns**: HTTP POST with collected env vars or file contents
- **Second-stage droppers**: script downloads a runtime or binary and runs it
- **Persistence**: writes outside the package into IDE/agent or shell config
  (`.vscode/tasks.json`, `.claude/settings.json`, shell rc files, git hooks,
  cron / launch agents); survives uninstall
- **Token-triggered destruction**: deletes files when a token stops working.
  Follow the §4.6 V4 incident-response order (remove persistence before
  revoking credentials)
```

```markdown
// 2k Before (dep-scan table rows + Transitive vs direct paragraph):
| `high` | CONDITIONAL lean. Cite affected dep name(s) + CVE IDs. Condition: update to patched transitive version. |
| `critical` | Strong CONDITIONAL. Must cite dep name + CVE IDs. Immediate upgrade path required. |

**Transitive vs direct:** Use the `depth` field in each finding. A finding with `depth: 1`
(direct dep) carries the same verdict weight as a CVE in the package itself. A finding
with `depth > 1` (transitive) warrants a flag and citation but not automatic verdict
escalation — report it and let the reviewer weigh reachability. Tier 2 always emits
`depth: 1`; Tier 3 reflects actual tree depth.

// 2k After:
| `high` | Third-party component (`references/criteria.md` §4.3) → HIGH flag → CONDITIONAL. Cite dep name(s) + CVE IDs. Condition: a version of this package, or a lockfile override, that resolves to the fixed dep version. |
| `critical` | Check each CRITICAL against CISA KEV. KEV-listed → REJECTED (Blocking CVE); name the fixed dep version. Otherwise HIGH flag → CONDITIONAL, same condition as `high`. |

**Transitive vs direct:** Use the `depth` field in each finding. Every dependency
is a third-party component under §4.3, so depth never makes a finding a Blocking
CVE (only KEV does). Depth shapes the condition: a `depth: 1` finding usually needs
a new release of this package or an override; a `depth > 1` finding warrants a
flag and citation — report it and let the reviewer weigh reachability. Tier 2
always emits `depth: 1`; Tier 3 reflects actual tree depth.
```

```markdown
// 2l Before (vuln-lookup table rows):
| `high` | Strong CONDITIONAL lean. Report must cite CVE IDs and affected ranges. Condition: upgrade to patched version; pin lockfile. |
| `critical` | REJECTED lean. Exception only if requested version is affirmatively outside affected range — document the version-range check. |
| Discrepancy (one DB only) | Flag and investigate. May be ingestion lag or a withdrawn advisory. Document in Security row; do not silently discard. |

// 2l After:
| `high` | Cite CVE IDs and affected ranges. Fixed release exists → HIGH flag → CONDITIONAL (condition: install the fixed version; pin lockfile). No fixed release → Blocking CVE → REJECTED (`SKILL.md` Tree terms). |
| `critical` | Check CISA KEV first. KEV-listed → REJECTED even when fixed (name the fixed release). Not KEV: no fixed release → REJECTED; fixed release → HIGH flag → CONDITIONAL. A version affirmatively outside the affected range is unaffected — document the range check. |
| Discrepancy (one DB only) | Flag and investigate. May be ingestion lag or a withdrawn advisory. Document in Security row; do not silently discard. |
```

````markdown
// 2m Before (section boundary before Install Script Risk Patterns):
| Will run in CI/CD with access to secrets or production credentials | High blast radius |
| Version to be installed has a §4.6 V3 HIGH (identity dropped or changed, new install hook) or a publisher change from the previous release (V3 plug-in below) | Possible hijacked publish |

---

## Install Script Risk Patterns

// 2m After (inserted between; apply after 2f, whose After text is this Before):
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
````

**Rationale:**
- **2b.** V2 says credit only for matched identity. The old "+1 trust / strong positive" is exactly what TanStack-style publishes exploit. The table gains a "Where to check" column so every signal names a concrete source verified at planning, and the stale rows (PGP, `GONOSUMCHECK`, crates "GitHub-linked ownership") go.
- **2c Tier 1 identity (human decision 2026-10-17).** "Relax: identity optional". Missing TP/provenance does not block Tier 1; Tier 1 still needs age ≥ 7 d, no signer or publisher change from the previous release, and big adoption, and a publisher change forces a deep audit.
  - **Consistent with §4.6:** V2 says identity can never justify Tier 1 or APPROVED on its own, and V2 also says "whether absence is itself a flag is the addendum's call". The row only stops *absence* from blocking; it grants no credit for presence.
  - **V3 stays a bar:** a dropped or changed signer/TP config/publisher removes Tier 1 (floor: any V3 item → Tier 1 unavailable) and triggers Tier 3 (2f).
  - **Old rows go:** the old addendum's "Provenance: Attestation present OR ecosystem has no mechanism" was stricter than the human's rule. The original Tier 1 example list is restored, because identity no longer filters it.
- **2c adoption bars.** npm/PyPI numbers are kept as-is: they can't be re-validated, since pypistats and the npm downloads API are blocked from the planning sandbox. Only their windows are made explicit. The crates bar is re-based to `recentDownloads`: 10M/90 d ≈ 0.8M/week, comparable to npm's 1M. Gem/NuGet bars use all-time totals because that is what the APIs give; Tier 1 also requires age > 1 y. The Tier 3 trigger = bar / 1000, matching npm's existing 1M / 1K ratio.
- **2g.** The facts (npm, pnpm, pip/uv) come from shipped docs and changelogs. Bun's default list is from memory (Notes). Yarn berry's script default is unverified, so Yarn berry is left out of the table.
- **2k/2l.** C6: §4.3 classes verbatim; no new verdict class. The direct-dep "same weight" sentence contradicted §4.3's third-party definition.
- **2m.** One plug-in section per the floor contract, placed after Tier Assignment because the Tier 1 rows point to it. `## CVE Scope (§4.3)` sits directly before it, matching the heading and placement in the sibling addenda on base (ide-plugin, ci-action, container-image, desktop-app), so one grep finds every subject's §4.3 plug-in. The 7-day cooldown matches V1's Tier 1 boundary.

**Verification:**
```bash
F=references/criteria/registry-package.md
grep -c "^## Version & Update Integrity (§4.6)$" $F                         # 1
grep -o "^- \*\*V[1-5]\*\*" $F | tr '\n' ' '                                # V1 V2 V3 V4 V5 (in order)
grep -c "^## CVE Scope (§4.3)$\|^### Client execution model$" $F         # 2
grep -A1 "^## CVE Scope (§4.3)$" $F | head -1                               # heading precedes §4.6 section (consistency script checks order)
grep -c "^| Identity (§4.6 V2) | Not required" $F                           # 1
grep -c "GONOSUMCHECK\|PGP/Sigstore signature on sdist\|REJECTED lean\|Strong CONDITIONAL\|same verdict weight as a CVE in the package itself\|+1 trust on Provenance\|100K crates.io all-time\|Attestation present OR ecosystem has no mechanism\|satisfies the Tier 1 identity row" $F   # 0
```

**If this fails:** `git -C <work-root> checkout -- references/criteria/registry-package.md` and reapply 2a–2m in order (2m's Before depends on 2f's After).

---

### Step 3: Workflow `workflows/registry-package.md`

**Objective:** route the auditor through the new plug-ins: client capture, version-pinned triage, Tier lists, research questions, coverage row, verdict notes.
**Confidence:** High
**Depends on:** Step 2 (section names it cites)
**Do-Projex:** Encouraged

**Files:** `workflows/registry-package.md`

**Changes:** 17 replacements (3a–3q); keep ~78-col wrapping.

````markdown
// 3a Before:
6. **Checksum / lockfile** -- is this going into a lockfile? Is there an
   integrity hash? (`npm` uses `sha512` in `package-lock.json`; `pip` uses
   hashes in `requirements.txt` with `--require-hashes`)

If any of 1--5 are missing, ask before proceeding. Item 6 is optional but its
presence increases trust.

// 3a After:
6. **Checksum / lockfile** -- is this going into a lockfile? Is there an
   integrity hash? (`npm` uses `sha512` in `package-lock.json`; `pip` uses
   hashes in `requirements.txt` with `--require-hashes`)
7. **Client and version** -- e.g. npm 12, pnpm 10, Bun, pip, uv. It decides
   whether install scripts run (addendum "Client execution model"). Unknown
   → assume they run.

If any of 1--5 are missing, ask before proceeding. Items 6--7 are optional;
a lockfile increases trust.

// 3b Before:
**Run the registry lookup script first** to get hard data:

```
python3 scripts/registry-lookup.py -Ecosystem <eco> -Name "<name>"
```

// 3b After:
**Run the registry lookup script first** to get hard data:

```
python3 scripts/registry-lookup.py -Ecosystem <eco> -Name "<name>" [-Version "<version>"]
```

Pass `-Version` when the user pinned one; otherwise the script reports the
version `latest` resolves to. Its `daysSincePublish` and, for npm,
`trustedPublisher`, `provenance` and `previousVersion` feed the Version
integrity row (addendum "Version & Update Integrity (§4.6)").
````

```markdown
// 3c Before:
- No CRITICAL or HIGH CVEs in requested version
- No maintainer changes in last 90 days
- First publish >1 year ago
- Provenance attestation present OR ecosystem has no mechanism

**Quick audit scope:** Confirm version is current, check for CVEs, verify the
name is not a typosquat, note the license, check for provenance attestation.
Write a short report. Takes ~2 minutes.

**Examples:** `express`, `lodash`, `react`, `requests`, `flask`, `django`,
`serde`, `tokio`, `rails`, `Newtonsoft.Json`, `hashicorp/aws` (Terraform).

// 3c After:
- No CRITICAL or HIGH CVEs in requested version
- No maintainer changes in last 90 days
- First publish >1 year ago
- Version to be installed published ≥ 7 days ago (`references/criteria.md`
  §4.6 V1)
- No change of signer, trusted-publisher config or publisher from the
  previous release, and no other §4.6 V3 item
- No past compromise (§4.6 V4 case c)

Trusted publishing or provenance is **not** required: its absence does not
block Tier 1, and its presence never qualifies a package on its own (§4.6
V2).

**Quick audit scope:** Confirm version is current, check for CVEs, verify the
name is not a typosquat, note the license, check version age and continuity
with the previous release (Version integrity row). Write a short report.
Takes ~2 minutes.

**Examples:** `express`, `lodash`, `react`, `requests`, `flask`, `django`,
`serde`, `tokio`, `rails`, `Newtonsoft.Json`, `hashicorp/aws` (Terraform),
when the version-level rows above hold at audit time.
```

```markdown
// 3d Before (Tier 2 list):
- Moderate adoption (1K--1M weekly npm / proportional)

// 3d After:
- Moderate adoption (between the addendum's Tier 3 trigger and Tier 1 bar)
```

```markdown
// 3e Before (Tier 3 list):
- Weekly downloads <1K (npm-equivalent) and not a known niche tool

// 3e After:
- Adoption below the addendum's Tier 3 trigger and not a known niche tool
```

```markdown
// 3f Before (Tier 3 list):
- Recent maintainer transfer from established to unknown account
- Will run in CI/CD with access to secrets or production credentials

// 3f After:
- Recent maintainer transfer from established to unknown account
- Will run in CI/CD with access to secrets or production credentials
- Version to be installed has a §4.6 V3 HIGH (trusted publisher or
  provenance dropped or changed, new install hook) or a publisher change
  from the previous release (addendum V3 plug-in)
```

```markdown
// 3g Before (Part B question 2):
2. **Does the publisher have provenance?** Check for ecosystem-specific trust
   signals (see `references/criteria/registry-package.md` "Ecosystem Trust
   Signals" table). Note presence or absence.

// 3g After:
2. **Does this version's identity verify and match the previous release?**
   Check the ecosystem's identity signals
   (`references/criteria/registry-package.md` "Ecosystem Trust Signals")
   against the previous release (`previousVersion` for npm). A drop or change
   is a §4.6 V3 HIGH; never used is a note.
```

```markdown
// 3h Before (Part B question 5):
5. **What happens at install time?** Review lifecycle scripts
   (`preinstall`/`postinstall` for npm, `setup.py` for PyPI, `build.rs` for
   crates, etc.). See the install script risk patterns in
   `references/criteria/registry-package.md`.

// 3h After:
5. **What happens at install time, and will it run?** Review lifecycle
   scripts (`preinstall`/`postinstall`/`binding.gyp` for npm, `setup.py` or
   wheel `.pth` files for PyPI, `build.rs` for crates, etc.) and whether the
   user's client runs them (npm ≥ 12 and pnpm ≥ 10 block dependency scripts
   until approved). See "Install Script Risk Patterns" in
   `references/criteria/registry-package.md`.
```

```markdown
// 3i Before (web search list):
- `"<package name>" maintainer compromise OR hijack`

// 3i After:
- `"<package name>" maintainer compromise OR hijack`
- `"<package name>" "<version>" malicious OR compromised` (version scope,
  `references/criteria.md` §4.6 V4)
```

```markdown
// 3j Before (Tier 3 install script review list):
- npm: Read `package.json` `scripts` block; inspect referenced files
- PyPI: Read `setup.py` or `setup.cfg`; check for `cmdclass` overrides

// 3j After:
- npm: Read `package.json` `scripts` block; inspect referenced files; a root
  `binding.gyp` means an implicit `node-gyp rebuild`
- PyPI: Read `setup.py` or `setup.cfg`; check for `cmdclass` overrides; list
  `*.pth` files in the wheel's `RECORD` (they run at every interpreter start)
```

```markdown
// 3k Before (coverage tracking, end of transitive bullet):
  If T3 fell back: note `T3→T2 fallback: <reason>`.
  For Tier 1: `Skipped -- Tier 1 quick audit`.

// 3k After:
  If T3 fell back: note `T3→T2 fallback: <reason>`.
  For Tier 1: `Skipped -- Tier 1 quick audit`.

- **Version integrity row** (all tiers): cite age, identity and continuity,
  e.g. `Done -- registry-lookup: 1.4.2 published 2026-09-30 (16 d); trusted
  publisher github, same config as 1.4.1; provenance SLSA v1; no past
  compromise`, or `Done -- 2.0.1 published 1 d ago; provenance on 2.0.0,
  absent on 2.0.1 (V3 HIGH)`.
```

```markdown
// 3l Before (Tier-specific research scope, Tier 1):
**Tier 1 (Quick):** Confirm no CVEs, verify not a typosquat, check license
compatibility, note provenance attestation status. Skip deep web research,
dependency tree audit, and install script review.

// 3l After:
**Tier 1 (Quick):** Confirm no CVEs, verify not a typosquat, check license
compatibility, check version age and identity continuity (§4.6). Skip deep
web research, dependency tree audit, and install script review.
```

```markdown
// 3m Before (Subject Rubric 4.1 bullet):
- **Provenance attestation**: Does the package use ecosystem-specific
  provenance? npm Sigstore provenance, PyPI Trusted Publishers, NuGet package
  signing, crates.io GitHub-linked ownership. Presence is a strong positive.
  Absence when the mechanism exists is a minor note.

// 3m After:
- **Provenance / trusted publishing**: Does this version carry the
  ecosystem's identity signal (npm trusted publishing or provenance, PyPI
  attestations, crates.io trusted publishing, NuGet author signature), and
  does it name the same repo / workflow as the previous release? Verified and
  continuous → positive note; it proves origin, not safety, and never on its
  own justifies Tier 1 or APPROVED (`references/criteria.md` §4.6 V2).
  Dropped or changed → §4.6 V3 HIGH (no Tier 1; Tier 3). Never used → minor
  note; does not block Tier 1.
```

```markdown
// 3n Before (Subject Rubric 4.4 bullet):
- **npm install scripts**: `preinstall`/`postinstall` hooks execute with the
  user's shell permissions. Flag if they spawn subprocesses, make network
  calls, or access files outside the package directory.

// 3n After:
- **npm install scripts**: `preinstall`/`postinstall` hooks execute with the
  user's shell permissions. Flag if they spawn subprocesses, make network
  calls, or access files outside the package directory. npm ≥ 12 and pnpm
  ≥ 10 run dependency hooks only after approval; rate them as if approved
  when the package needs them.
```

```markdown
// 3o Before (Toward REJECTED, last bullet):
- **Unpatched CRITICAL/HIGH CVE**: In the requested version with no fix
  available

// 3o After:
- **Blocking CVE** (`SKILL.md` Tree terms; `references/criteria.md` §4.3):
  CRITICAL listed in CISA KEV (in the package or a dependency), or
  HIGH/CRITICAL in the package's own code with no fixed release
- **Install-time persistence or dropper**: install script or `.pth` file that
  writes into IDE/agent or shell config (`.vscode/`, `.claude/`, shell rc
  files, git hooks) or downloads and runs a second-stage binary
```

```markdown
// 3p Before (Toward CONDITIONAL):
- **Missing provenance when mechanism exists**: Condition: verify checksum
  manually; pin to exact version

// 3p After:
- **Identity dropped or changed vs the previous release** (§4.6 V3 HIGH):
  Condition: install the last release that passes V3; re-audit when the
  maintainers explain the change. Never using an available mechanism is a
  note, not a condition
- **Fresh version** (§4.6 V1): Condition: install the previous release, or
  set the client cooldown from the addendum's V1 table
- **Install scripts need approval** (npm ≥ 12, pnpm ≥ 10): Condition: approve
  only this package, pinned to the audited version
- **Dependency HIGH/CRITICAL CVE, not in KEV** (third-party component,
  §4.3): Condition: a version or override that resolves to the fixed
  dependency
```

```markdown
// 3q Before (Toward APPROVED):
- No CVEs in requested version
- Provenance attestation present (or ecosystem has no mechanism)

// 3q After:
- No CVEs in requested version
- Version ≥ 72 h old with no §4.6 V3 item; identity continuous with the
  previous release where the package uses an identity mechanism
```

**Rationale:**
- **3b.** Without `-Version`, a pinned request's V1 age and V2/V3 identity are read from `latest`: wrong version, silently.
- **3p.** Removes the CONDITIONAL that contradicted the addendum ("not auto-flag") and eval 8. "Verify checksum manually" was not a meaningful condition: there is nothing to verify the checksum against.
- **3o.** The persistence/dropper bullet is malicious by design, so REJECTED is consistent with V4 (b). It sits in the subject notes, not `SKILL.md` (byte budget; subject pattern).
- **3c Tier 1 (human decision 2026-10-17).** Identity is optional, but continuity and age are required, which mirrors addendum 2c. The original example list is restored with a per-version caveat.

**Verification:**
```bash
F=workflows/registry-package.md
grep -c "Unpatched CRITICAL/HIGH CVE\|Missing provenance when mechanism exists\|Presence is a strong positive\|note provenance attestation status\|Provenance attestation present\|Identity verified per the addendum\|satisfies the Tier 1 identity row" $F   # 0
grep -c "§4.6 V[1-5]" $F                     # ≥ 8
grep -c '\[-Version "<version>"\]' $F         # 4 (triage + vuln + dep-scan T2/T3)
git -C <work-root> diff -U0 -- $F | grep '^+' | grep -v '^+++' | awk 'length > 80' | grep -v '^+python3'   # empty: no new prose line over ~78 cols
```

**If this fails:** `git -C <work-root> checkout -- workflows/registry-package.md` and reapply.

---

### Step 4: `references/registries.md` language-registry rows

**Objective:** RP-6. Correct the PyPI and Go claims; add identity and script-model notes. Touch only §JavaScript…§.NET.
**Confidence:** High
**Depends on:** Step 2 (cited section)
**Do-Projex:** Encouraged

**Files:** `references/registries.md`

**Changes:** 9 single-line replacements (whole line Before → whole line After).

```markdown
// 4a Before:
- **npmjs.com** — Official registry. Medium baseline trust. Verified publishers (scoped packages from known orgs) are higher trust.
// 4a After:
- **npmjs.com** — Official registry. Medium baseline trust. Verified publishers (scoped packages from known orgs) are higher trust. Trusted publishing and provenance show which CI workflow published a version — origin, not safety; check continuity across versions (`references/criteria/registry-package.md`).

// 4b Before:
**Red flags:** Packages with install scripts (`preinstall`, `postinstall`, `install`) that aren't from a known tool (e.g., node-gyp, esbuild). Always review what these scripts do.
// 4b After:
**Red flags:** Packages with install scripts (`preinstall`, `postinstall`, `install`, or an implicit `binding.gyp` build) that aren't from a known tool (e.g., node-gyp, esbuild). Always review what these scripts do — npm ≥ 12 and pnpm ≥ 10 block dependency scripts until the user approves them, so the approval request is the decision point. A version that drops the trusted publishing or provenance its predecessor had.

// 4c Before:
- **pypi.org** — Official. Medium baseline. No mandatory publishing auth; typosquatting common.
// 4c After:
- **pypi.org** — Official. Medium baseline. 2FA mandatory for all accounts; Trusted Publishers with PEP 740 attestations show which CI workflow uploaded a file. Typosquatting common.

// 4d Before:
**Red flags:** `setup.py` with `os.system()` calls, packages that shadow stdlib names.
// 4d After:
**Red flags:** `setup.py` with `os.system()` calls, packages that shadow stdlib names, `.pth` files in wheels (run at every interpreter start), projects marked `quarantined`.

// 4e Before:
- **rubygems.org** — Official. Similar trust profile to PyPI.
// 4e After:
- **rubygems.org** — Official. Medium baseline. MFA required for top gems; trusted publishing available.

// 4f Before:
- **crates.io** — Requires GitHub auth to publish. Higher baseline trust than npm/PyPI.
// 4f After:
- **crates.io** — Requires GitHub auth to publish. Higher baseline trust than npm/PyPI. Trusted publishing (`trustpub_data` per version) names the publishing repo + commit. `build.rs` runs at build time.

// 4g Before:
- **pkg.go.dev / go get** — Module proxy validates checksums via sumdb. High trust for modules in the index. Direct VCS installs bypass this — flag.
// 4g After:
- **pkg.go.dev / go get** — Module proxy + checksum DB (`sum.golang.org`) guarantee everyone gets the same bytes for a version: consistency, not author identity or safety (the proxy keeps serving a cached version even if it is malicious). Medium-High baseline. `GOSUMDB=off`, or a `GONOSUMDB` / `GOPRIVATE` pattern covering public modules, disables checksum verification — flag (`GOINSECURE` does not).

// 4h Before:
- **Maven Central** — Requires GPG signing. High trust.
// 4h After:
- **Maven Central** — Requires PGP signing (Sigstore bundles optional) and namespace verification. High trust. A signature proves the key holder, not safety — check key continuity across versions.

// 4i Before:
- **NuGet.org** — Microsoft-operated. Medium-high trust. Package signing available; check for signed packages.
// 4i After:
- **NuGet.org** — Microsoft-operated. Medium-high trust. Author signatures and trusted publishing (CI OIDC) identify the publisher — check the author certificate subject matches earlier versions.
```

**Rationale:**
- **4g.** Go "High" → "Medium-High": sumdb proves consistency, not safety (the review's boltdb-go case). "Direct VCS installs bypass this" was wrong: `GOPROXY=direct` still verifies against sumdb unless `GONOSUMDB`/`GOPRIVATE`/`GOSUMDB=off` (`go help environment`).
- **4b.** The trailing sentence is a red-flag item, matching the line's "Red flags:" list form.
- Other lines and sections are untouched to avoid sibling collisions.

**Verification:** `git -C <work-root> diff -U0 references/registries.md | grep '^@@'`: every hunk starts ≤ line 38. `grep -c "No mandatory publishing auth\|High trust for modules in the index\|Direct VCS installs bypass" references/registries.md` → 0.

**If this fails:** `git -C <work-root> checkout -- references/registries.md`.

---

## Verification Plan

### Automated Checks

- [ ] `PATH="<scratchpad>/pwsh:$PATH" python3 -m unittest discover -s tests -p "test_*.py"` → Ran 23, OK.
- [ ] `python3 -m unittest discover -s evals -p "test_*.py"` → Ran 12, OK; `python3 evals/run_evals.py validate` passes; `git diff --stat <base>..HEAD -- evals` empty.
- [ ] Consistency script (run from `<work-root>`; not committed):
```bash
python3 - <<'EOF'
import re, json, pathlib, importlib.util, io, contextlib, sys
sys.dont_write_bytecode = True
D = {f: pathlib.Path(f).read_text(encoding="utf-8") for f in
     ["references/criteria/registry-package.md", "workflows/registry-package.md", "references/registries.md"]}
add, wf, reg = D.values()
assert add.count("\n## Version & Update Integrity (§4.6)\n") == 1
sec = add.split("## Version & Update Integrity (§4.6)")[1].split("\n## ")[0]
assert re.findall(r"^- \*\*(V[1-5])\*\*", sec, re.M) == ["V1", "V2", "V3", "V4", "V5"]
assert add.count("\n## CVE Scope (§4.3)\n") == 1
assert add.index("\n## CVE Scope (§4.3)\n") < add.index("\n## Version & Update Integrity (§4.6)\n")
assert "Blocking CVE boundary" not in add
# Tier 1 (human decision 2026-10-17): identity optional; continuity + age required; publisher change -> Tier 3
t1 = add.split("### Tier 1 -- Quick Audit")[1].split("### Tier 2")[0]
assert "| Identity (§4.6 V2) | Not required" in t1
assert "No change of signer, trusted-publisher config or publisher from the previous release" in t1
assert "`daysSincePublish` ≥ 7" in t1 and "Above the Tier 1 bar" in t1
t3 = add.split("### Tier 3 -- Deep Audit")[1].split("\n## ")[0]
assert "publisher change from the previous release" in t3
wt1 = wf.split("### Tier 1 -- Quick Audit")[1].split("### Tier 2")[0]
assert "is **not** required" in wt1 and "No change of signer, trusted-publisher config or publisher" in wt1 and "≥ 7 days" in wt1
wt3 = wf.split("### Tier 3 -- Deep Audit")[1].split("\n---")[0]
assert "publisher change" in wt3
for s in ['Verified per "Ecosystem Trust Signals" OR ecosystem has no mechanism', "Identity verified per the addendum",
          "satisfies the Tier 1 identity row", "Attestation present OR ecosystem has no mechanism"]:
    assert s not in add and s not in wf, s
# §4.6 V2 wording kept: identity never sufficient on its own for Tier 1 / APPROVED
assert "never enough on its own for Tier 1 or" in add and "never on its" in wf
for f, t in D.items():
    for v in re.findall(r"§4\.6 (V\d)", t):
        assert v in {"V1", "V2", "V3", "V4", "V5"}, (f, v)
stale = ["GONOSUMCHECK", "PGP/Sigstore signature on sdist", "REJECTED lean", "Strong CONDITIONAL",
         "same verdict weight as a CVE in the package itself", "+1 trust on Provenance", "100K crates.io all-time",
         "Unpatched CRITICAL/HIGH CVE", "Missing provenance when mechanism exists", "Presence is a strong positive",
         "No mandatory publishing auth", "High trust for modules in the index", "Direct VCS installs bypass"]
for f, t in D.items():
    for s in stale:
        assert s not in t, (f, s)
# fields named in docs exist in script output
spec = importlib.util.spec_from_file_location("rl", "scripts/registry-lookup.py"); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
m.invoke_api = lambda url, timeout=15: ({"name": "x", "dist-tags": {"latest": "1.0.0"}, "versions": {"1.0.0": {}},
                                          "time": {"1.0.0": "2020-01-01T00:00:00Z"}} if "registry.npmjs.org" in url else None)
buf = io.StringIO()
with contextlib.redirect_stdout(buf): m.main(["npm", "x"])
keys = set(json.loads(buf.getvalue()))
for k in ["trustedPublisher", "provenance", "previousVersion", "removedVersions", "publisher", "daysSincePublish", "installScripts"]:
    assert k in keys, k
    assert f"`{k}`" in add + wf, ("doc never names", k)
print("OK")
EOF
```
- [ ] `git -C <work-root> diff --stat <base>..HEAD` → exactly the 6 files.

### Manual Verification (paper traces, cite rule per hop in the log)

| # | Case | Expected |
|---|---|---|
| R1 | eval 8 `chalk@5.3.0`: 2023; never used TP/provenance; same publisher as 5.2.0; 5.6.1 in `removedVersions` | V1 none; V2 never-used → note (2b), **no** CONDITIONAL (3p); V3 none; V4 (c) LOW → Tier 2; vuln/dep-scan clean → **APPROVED reachable** |
| R2 | eval 4 `chalk` (latest 6.0.1, 2026-09-27) | Same as R1 → APPROVED/CONDITIONAL ✓ |
| R3 | TanStack shape: TP same `oidcConfigId`, provenance, version 6 h old | V2 verified but no offset; V1 HIGH `fresh version` → **CONDITIONAL**; condition cites e.g. `min-release-age=7` / `minimumReleaseAge: 10080` |
| R4 | npm 2.0.1 with no TP/provenance; 2.0.0 had TP; published by an account that never published before | V3 HIGH (drop) + publisher change → Tier 3 (2f); **CONDITIONAL**: install 2.0.0 |
| R5 | eval 5 `lodash@4.17.20`: own-code HIGH fixed in 4.17.21, not KEV | 2l `high` + fixed → HIGH flag → **CONDITIONAL** (install 4.17.21) ✓ eval 5 |
| R6 | dep-scan: direct dep CRITICAL in KEV / not in KEV | 2k: **REJECTED** (name fixed dep) / **CONDITIONAL** |
| R7 | Own-code HIGH, no fixed release | 2l → Blocking CVE → **REJECTED** |
| R8 | npm 12 user, `sharp`-like native addon with benign `install` | 2g: rate as approved; **CONDITIONAL** "approve only this package, pinned" (or APPROVED with that condition named in Recommendation per tree) |
| R9 | eval 36 `prettier` 3.9.10 (TP, no provenance, same `oidcConfigId` as 3.9.9; published 2026-10-10) | V2 verified via `oidcConfigId` continuity (note only, no Tier 1 credit); V3 none. Age < 7 d → Tier 2; ≥ 7 d → **Tier 1**. **APPROVED reachable** either way ✓ |
| R10 | PyPI wheel adds a `.pth` that imports a module and contacts the network | 2i HIGH + V3 new hook HIGH; writes shell rc / drops binary → 3o **REJECTED**; else CONDITIONAL with Tier 3 review |
| R11 | Go module, user env `GONOSUMDB=github.com/*` | 2b/4g → flag; Recommendation: remove pattern for public modules |
| R12 | `lodash` latest 4.18.1: no TP/provenance on 4.18.1 or 4.18.0; both published by `jdalton`; published 2026-04-01; > 1M weekly | Identity row: not required (2c); V1 ≥ 7 d; V3 none (same publisher, nothing dropped) → **Tier 1 available**; clean CVEs → **APPROVED** (human decision: Quick audits stay fast for popular packages) |
| R13 | Popular npm package, never had TP/provenance; new version published by an account that never published it before; 20 d old | Identity absence: no effect. V3 publisher change (MEDIUM) → Tier 1 unavailable and **Tier 3** (2f / 3f) → deep audit; verdict per findings (≥ CONDITIONAL only if the deep audit adds flags) |

### Acceptance Criteria Validation

| Criterion | How to Verify | Expected Result |
|---|---|---|
| Script fields both twins | Step 1 tests | 23 OK |
| Plug-ins present | consistency script | `OK` |
| Stale phrases gone | consistency script; Step 2–4 greps | 0 |
| Harness green | evals unittest + validate | 12 OK; pass |
| Scope | `git diff --stat` + registries hunk lines | 6 files; hunks ≤ L38 |
| Tier 1 rule (human decision) | consistency script Tier 1 asserts; R9, R12, R13 | `OK`; traces match |
| Verdict behavior | R1–R13 in log | match table |

---

## Rollback Plan

1. Before close: `projex-abandon.sh <repo-root> claude/youthful-dijkstra-5ov1kt projex/2610162010-registry-package-rubric-refresh --worktree`. Base untouched.
2. After squash-close: `git -C <repo-root> revert <squash-sha>` (6 files, single commit). No other plan depends on these files' new text except the eval plan's future registry cases.

---

## Notes

### Risks

- **Tier 1 without identity evidence (human-accepted).** A stolen-token publish from the *same* account on a package that never used TP/provenance changes neither signer nor publisher. Tier 1 then rests on V1 alone (≥ 7 d cooldown), plus the incident search and CVE checks. Mitigation: the 2025–26 incidents were mostly caught within 7 d (review eval RP-1). A drop of TP/provenance that a package *had* still breaks V3. Accepted by the human: "Quick audits stay fast for popular packages."
- **Adoption bars are policy.** crates/gems/NuGet bars rest on live sanity data for top packages only, and npm/PyPI bars are unvalidated (APIs blocked in sandbox). Mitigation: all numbers live in one table; STEWARDSHIP review can retune.
- **Read cost.** Addendum +~10 KB, read on every registry audit. Mitigation: the new material is tables plus a single plug-in section; the workflow deltas stay small (eval risk "rubric bloat").
- **Publisher-change definition (V3).** "Long-standing co-maintainer ≠ change" could be argued to loosen V3's MEDIUM floor. It clarifies "publisher" as the publishing *party*; lodash 4.17.19→4.17.20 shows per-version `_npmUser` varies legitimately. It does not lower any rating for a new account or an owner-list change.
- **Twin drift.** The PS `publishedAt` for `previousVersion` inherits `Format-DateStr`'s culture round-trip. That is existing behaviour; Python is pinned by test.
- **Product facts age fast** (npm 12 / pnpm 12 / Yarn 4.18 at planning). Mitigation: each row carries a "Since" version; STEWARDSHIP watch-list (orchestrator, F-P1).
- **Sibling collisions on `references/registries.md`.** The siblings are closed and their edits are on base (L72–73, L80, L86). Step 4's hunks stay within L5–38, and the anchors were re-checked at `8564410`.

### Unverified (kept out or hedged in shipped text)

- **Bun.** Dependency scripts are blocked except `trustedDependencies`, plus a built-in default list. From memory, High; written as stated in 2g. Verify against bun.sh docs during execution if reachable, else keep it.
- **PyPI 2FA.** Mandatory for all accounts since 2024-01-01. From memory, High (4c, 2b: no date in shipped text).
- **RubyGems trusted publishing** (from memory, High) and NuGet `dotnet nuget verify` (from memory, High). The NuGet TP launch date is secondary-only (~Sep 2025), so no date in shipped text.
- **`oidcConfigId` semantics.** Assumed stable per TP configuration (observed identical across tanstack 5.104.x); not documented in the npm docs read.
- **OSV.** Assumed to include OpenSSF malicious-packages `MAL-` records for npm/PyPI (from memory, High). `api.osv.dev` was proxy-blocked at planning, so `vuln-lookup` couldn't be exercised live.
- **Yarn berry** script default: not verified. Omitted from the 2g table.
- **Dropped from the review as unverified:**
  - npm malware-scan gate on staged publishing (2026-09-03)
  - PyPI "14-day lock on new files to old releases"
  - bypass-2FA end date (Jan 2027)
  - specific incident names and counts (TanStack, ChainDrop, LiteLLM) in shipped text.
- **Primary sources not read.** The PyPI PGP removal (2023) was confirmed only via LWN coverage. Maven's PGP-required/Sigstore-optional status and NuGet TP were confirmed via official-domain search summaries, not page reads.

### Eval hand-off (for the eval-refresh plan; no `evals/` edits here)

- New registry cases:
  - fresh version (CONDITIONAL with client cooldown)
  - TP/provenance drop vs previous version (V3 → CONDITIONAL, Tier 3)
  - npm 12 script-approval context (condition names pinned approval)
  - wheel `.pth` / `binding.gyp`
  - dependency KEV CRITICAL → REJECTED vs non-KEV → CONDITIONAL
  - own-code unfixed HIGH → REJECTED
  - non-npm ecosystems: crates TP, Go `GONOSUMDB`, pinned RubyGems version age
  - PyPI quarantined project.
- Eval 0 (express Tier 1) and eval 36 (prettier exact APPROVED) are calendar-dependent via V1. Already in the floor hand-off; R9 shows APPROVED stays reachable.
- New Tier 1 cases from the human decision:
  - popular package without TP/provenance, ≥ 7 d, same publisher → Tier 1 / APPROVED (R12 shape)
  - publisher change → Tier 3 (R13 shape).
- Eval 8 `expected_output` "Tier 1 or Tier 2": unchanged and still true (Tier 2 now forced by V4 c).

### Coordination (orchestrator)

- **§4.3 plug-in heading:** resolved. The plan uses `## CVE Scope (§4.3)` directly before the §4.6 section, as most siblings do. cli-binary used `## Own Code vs Third-Party Components (§4.3)`, which is its owner's call.
- **Tooling follow-on** (optional patch/plan, `scripts/registry-lookup.*` + tests):
  - PyPI `provenance` / `project-status` via the simple API + integrity API
  - RubyGems `-Version` via `/api/v1/versions/<gem>.json`
  - optional KEV flag in `vuln-lookup` (floor hand-off).
- **RP-8 Scorecard host patch:** unchanged, still pending verification.
- **STEWARDSHIP:** registry-package Last Reviewed 2026-10-16 → Next Due 2027-01-14 (90 d); F-P1 watch list. Orchestrator-owned.

### Open Questions

None.
- Tier 1 identity was decided by the human on 2026-10-17 (Revision Log).
- The adoption bars, the narrowed "publisher change" rule, the removal of "missing provenance → CONDITIONAL" and the §4.3 heading were confirmed by the orchestrator on 2026-10-17.

### Revision Log

| Date | Trigger | Change |
|---|---|---|
| 2026-10-16 | Initial | Plan authored at base `20843cc` |
| 2026-10-17 | Human decision (verbatim, via orchestrator): "Relax: identity optional — Missing trusted publishing or provenance does not block Tier 1 if every other Tier 1 condition holds. These are still required: version at least 7 days old, no change of signer or publisher from the previous release, and big adoption. A publisher change still forces a deep audit. Quick audits stay fast for popular packages." | 2b scoring bullets (verified = note, never Tier 1 credit alone; never-used doesn't block Tier 1); 2c Tier 1 rows (Identity: not required; Continuity: no signer/TP-config/publisher change; History split out) + original example list restored; 2f/2m Tier 3 row adds publisher change; V2/V3 plug-in bullets (absence never blocks Tier 1; publisher change always Tier 3); 3c/3f/3m workflow mirrors; Impact, Risks, R9 updated, R12/R13 added; consistency script asserts the Tier 1/3 rule and V2 wording |
| 2026-10-17 | Orchestrator: prefer siblings' `## CVE Scope (§4.3)` | §4.3 block moved from 2l into 2m as a `##` section directly before `## Version & Update Integrity (§4.6)`; Step 2 greps and consistency script updated |
| 2026-10-17 | Base moved to `8564410` (all sibling refreshes closed) | All 47 anchors re-checked against `8564410` (only `references/registries.md` changed, outside Step 4 hunks); Dependencies/A1/Preflight updated; re-simulated |

### Split Decision

`No split — single scope; size heuristic not tripped` (it needs size AND > 5 steps). Size is ~1.5k lines / ~90 KB, almost all verbatim Before/After blocks, but there are only 4 steps, in one `.projex/` scope. Pre-validated at planning and re-validated 2026-10-17 at `8564410`: every Before matched exactly once (fence-aware parse, 47 edits). A scratch export with all edits applied passed `tests/` (23 OK with pwsh, 8 skipped without) and the consistency script (`OK`). `references/registries.md` hunks stayed at L6–38. The script change (upstream data) and the docs that name its fields ship together so the docs never cite fields that don't exist; splitting would create exactly that interim state.
