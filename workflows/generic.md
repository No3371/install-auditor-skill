<!-- workflows/generic.md - Low-confidence fallback. Routes here only when Step 0
classifier produces LOW confidence (conflicting signals or no signals). Every
resolved subject type has its own specific workflow (Types 1-9). -->

# Generic Fallback Workflow (Low-Confidence Only)

> **WARNING — Low-confidence classification.** The dispatcher could not
> confidently identify the subject type. This workflow attempts to resolve the
> ambiguity; if it cannot, it runs a defensive minimum audit sized for the
> subjects that land here (scripts, portals, certificates, multi-component
> repos, not only packages). Reports produced here carry a low-confidence
> warning.

After completing all sections below, return to `SKILL.md` Step N for the
shared verdict tree and audit-coverage report shape.

---

## Phase 1 — Subject Probe

Examine available signals (read-only):

1. **Read the classifier output** — the `Rationale` field names which signals
   fired and which types were candidates. Record the top 1-2 candidates.
2. **Inspect the install artifact** — URL, command, manifest, or file extension.
   A signal the classifier missed goes into the Phase 2 question; it never
   re-routes on its own.
3. **Check the user's stated purpose** — often reveals the subject type even
   when technical signals are ambiguous.
4. **Name what the install action does** — runs code, grants trust or access,
   or only stores a link. Phase 3 starts from this.

---

## Phase 2 — User Clarification

Present findings from Phase 1 and ask the user to resolve the ambiguity:

> "The classifier could not confidently determine the subject type. Based on
> available signals, the best candidates are **[candidate 1]** and
> **[candidate 2]**. Can you confirm which type this is, or provide additional
> context (e.g., where you found it, what it does, how it installs)?"

**If the user clarifies before Phase 3 starts** → re-route. This is the only
re-route allowed after Step 0 (`SKILL.md` Step 0; `references/classifier.md`
Edge-Case Discipline):
- Update the classifier output to reflect the user-confirmed type
- Set confidence to `high` with `user override: <verbatim>` in Rationale
- Route to `workflows/<confirmed-type>.md` and restart the audit there
- **Do not continue in this file**

**If the user cannot clarify** (or context is non-interactive) → proceed to
Phase 3 and keep the question for the report (Phase 4). A clarification that
arrives after Phase 3 starts does not re-route: finish here and recommend a
re-audit under the confirmed type.

---

## Phase 3 — Defensive Minimum Audit

Run a reduced checklist: enough signal for the verdict tree, nothing more.
Gather evidence without executing anything: resolve redirects and download
scripts or manifests to read them; never run them.

**Subject checks** (run first; they decide most generic verdicts):

| Check | What to do |
|-------|------------|
| **Execution & trust grant** | List what the install action executes or grants: code run without review (pipe-to-shell, `iex`, `make install`, setup scripts); privilege elevation (sudo, admin, UAC); trust-store change (root CA, certificate install, configuration / MDM profile, proxy settings); persistence (services, scheduled tasks, login items, shell profile edits); network exposure (listeners, tunnels, remote access); credential or data grant (OAuth, API keys, tokens). Rate each item per Subject Verdict Notes |
| **Source provenance** | Where the subject came from: URL shortener or redirector, plain HTTP, raw IP or paste site, lookalike or newly registered domain, unsolicited forum / chat / email origin, link not on the publisher's own domain. Rate per Subject Verdict Notes |

Where a candidate type's workflow covers one component (e.g. the
install-script review in `workflows/cli-binary.md` for a Makefile target or
setup script), run that review as a sub-step without re-routing.

**Canonical rows** (`references/criteria.md` rows table). Never drop a
Required row; use `N/A (<reason>)` when it cannot apply:

| Row | Generic handling |
|-----|------------------|
| Registry / metadata lookup | Registry, store or release page exists → look it up; else `N/A (no registry)` |
| Typosquat / name verification | Name, publisher and domain vs plausible legitimate ones, incl. lookalike domains |
| CVE / advisories | Named, versioned artifact → OSV, GHSA, NVD; artifact exists but unidentifiable → `Not available (<why>)`; no artifact → `N/A (no versioned artifact)`. Always search incidents for the publisher or domain |
| Version integrity | `references/criteria.md` §4.6 for a versioned artifact; same `Not available` / `N/A` split as the CVE row |
| License compatibility | When code is distributed; else `N/A (no distributed code)` |
| Maintainer / activity / health | Brief: last release or commit, maintainer count; flag abandoned (>24 months) or single anonymous maintainer |
| Permissions / least privilege | If applicable: requested access vs stated purpose |
| OpenSSF Scorecard; Dependency tree / transitive risk; Source code review (behavioral) | `Skipped (generic fallback)` |

Also skip tier triage, deep rubric scoring and alternatives comparison; they
belong in specific workflows.

**Report shape and confidence:**

- **Shape:** Quick skeleton from `SKILL.md`, with
  `**Audit tier:** Quick (generic fallback)`. If any check raises a HIGH or
  CRITICAL flag, use the full `references/report-template.md` skeleton with
  `**Audit tier:** Standard (generic fallback)` instead.
- **Confidence cap:** Audit confidence is **Moderate** at most, because the
  subject type (and so the right rubric) is unconfirmed; say so in the
  confidence reason. `Skipped (generic fallback)` rows are by-design skips:
  they do not count as **Not available** and do not lower the rating
  further. Rate lower per `SKILL.md` when other gaps apply.

---

## Phase 4 — Low-Confidence Warning

Stamp the following in the report:

- **Report header:** add `**Classification confidence:** Low — generic fallback` below the Subject type line
- **Recommendation section:** prepend: *"This audit used the generic fallback
  workflow (low classification confidence). Coverage is reduced. Consider
  re-running with an explicit subject type for full coverage."* If Phase 2
  went unanswered, add its question and the candidate types so a reviewer can
  re-route.

---

## Subject Verdict Notes

These ratings feed the `SKILL.md` Step N tree like any workflow's notes.

### Toward REJECTED

- Code that executes unread **and** comes from a source with any provenance
  smell, or from no identifiable publisher (e.g. pipe-to-shell behind a URL
  shortener) — CRITICAL. Recommend obtaining the tool from its publisher's
  own channel and auditing that instead.
- Root CA or trust-store addition from an unknown or unsolicited issuer —
  CRITICAL: the holder can intercept all TLS traffic.

### Toward CONDITIONAL

- Code that executes but can be read first (script, Makefile target) and was
  not reviewed by report time — HIGH. Condition: review it, then re-audit.
- Root CA or trust-store addition from a claimed internal or vendor issuer
  not yet confirmed — HIGH. Condition: check the fingerprint with the issuer
  out of band, or install through managed device policy.
- One-site certificate exception — MEDIUM. Condition: ask the operator for a
  certificate from a publicly trusted or org-managed CA.
- Privilege elevation, persistence or network exposure that the stated
  purpose does not explain — HIGH; explained → MEDIUM.
- Credential or data grant — rate scope against stated purpose with the
  `workflows/remote-integration.md` scope checks (sub-step, no re-route).
- Each provenance smell — MEDIUM; HIGH when the delivered content executes.

### Toward APPROVED

- Nothing executes and no trust is granted (e.g. a bookmark), or every item
  above is explained, confirmed with its issuer, and low-impact.
