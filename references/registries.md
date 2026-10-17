# Registry & Source Trust Guide

## Trusted Registries by Ecosystem

### JavaScript / Node.js
- **npmjs.com** — Official registry. Medium baseline trust. Verified publishers (scoped packages from known orgs) are higher trust. Trusted publishing and provenance show which CI workflow published a version — origin, not safety; check continuity across versions (`references/criteria/registry-package.md`).
- **GitHub Packages (npm)** — Packages tied to GitHub org identity. Higher trust for known orgs.
- **jsr.io** — Deno/JSR registry. Newer, requires GitHub auth, moderate trust.
- **Unpkg / CDN links** — Never install from CDN links directly in package.json; flag immediately.

**Red flags:** Packages with install scripts (`preinstall`, `postinstall`, `install`, or an implicit `binding.gyp` build) that aren't from a known tool (e.g., node-gyp, esbuild). Always review what these scripts do — npm ≥ 12 and pnpm ≥ 10 block dependency scripts until the user approves them, so the approval request is the decision point. A version that drops the trusted publishing or provenance its predecessor had.

### Python
- **pypi.org** — Official. Medium baseline. 2FA mandatory for all accounts; Trusted Publishers with PEP 740 attestations show which CI workflow uploaded a file. Typosquatting common.
- **conda-forge** — Community-reviewed conda packages. Higher trust.
- **Anaconda repository** — Curated. Higher trust.
- **GitHub releases (wheel/sdist)** — Acceptable if from verified org; check checksums.
- **Direct git installs (`pip install git+...`)** — Flag; commit SHA pinning required.

**Red flags:** `setup.py` with `os.system()` calls, packages that shadow stdlib names, `.pth` files in wheels (run at every interpreter start), projects marked `quarantined`.

### Ruby
- **rubygems.org** — Official. Medium baseline. MFA required for top gems; trusted publishing available.

### Rust
- **crates.io** — Requires GitHub auth to publish. Higher baseline trust than npm/PyPI. Trusted publishing (`trustpub_data` per version) names the publishing repo + commit. `build.rs` runs at build time.

### Go
- **pkg.go.dev / go get** — Module proxy + checksum DB (`sum.golang.org`) guarantee everyone gets the same bytes for a version: consistency, not author identity or safety (the proxy keeps serving a cached version even if it is malicious). Medium-High baseline. `GOSUMDB=off`, or a `GONOSUMDB` / `GOPRIVATE` pattern covering public modules, disables checksum verification — flag; Recommendation: remove the setting, or narrow the pattern to private module paths (`GOINSECURE` does not disable it).

### Java / JVM
- **Maven Central** — Requires PGP signing (Sigstore bundles optional) and namespace verification. High trust. A signature proves the key holder, not safety — check key continuity across versions.
- **JCenter** — Deprecated (shut down); any dependency still pointing here is a flag.
- **Custom Artifactory/Nexus** — Organization-controlled; verify org controls it.
- **Jitpack** — Builds from GitHub directly. Lower trust.

### .NET
- **NuGet.org** — Microsoft-operated. Medium-high trust. Author signatures and trusted publishing (CI OIDC) identify the publisher — check the author certificate subject matches earlier versions.

### Container Images
| Source | Trust |
|---|---|
| Official Docker Hub images (library/) | High |
| Hardened catalogs (Docker Hardened Images `dhi.io`, Chainguard `cgr.dev`) | High — when signed attestations verify against the publisher's documented key or identity |
| Docker Hub verified publishers | Medium-High |
| Docker Hub community images | Low-Medium |
| GitHub Container Registry (ghcr.io) from known orgs | Medium-High |
| Amazon ECR Public | Medium |
| Quay.io (Red Hat) | Medium |
| Random Docker Hub with <100 pulls | Low |
| Self-hosted registry (unknown) | Low — verify provenance |
| Frozen / legacy namespace (e.g. `bitnamilegacy`) | Low — no further updates; HIGH flag `frozen namespace` (`references/criteria/container-image.md`) |

**Always check:** Use `docker scout` or Trivy scan results if available. Image digest pinning preferred over tag pinning.

### Browser Extensions
| Store | Trust |
|---|---|
| Chrome Web Store | Medium (Google review process exists but is imperfect) |
| Firefox Add-ons (AMO) | Medium-High (stronger review process) |
| Edge Add-ons | Medium (mirrors Chrome Web Store largely) |
| Safari Extensions (Mac App Store) | Medium-High |
| Sideloaded / unpacked | LOW — major flag; requires explicit justification |

**Chrome Web Store red flags:** Extensions with very high permissions + low user count + recent publication + no privacy policy.

### IDE / Editor Plugins
| Marketplace | Trust |
|---|---|
| VS Code Marketplace (marketplace.visualstudio.com) | Medium (Microsoft-operated) |
| JetBrains Marketplace | Medium (manual listing review; the Plugin Verifier checks compatibility, not malware — see `references/criteria/ide-plugin.md`) |
| Vim / Neovim plugins from GitHub (vim-plug, lazy.nvim, `vim.pack`) | Low-Medium (no central review; trust the repo and the pinned commit) |
| Emacs MELPA | Low-Medium (community-maintained) |
| Open VSX (open-vsx.org) | Low-Medium (Eclipse-operated; operator-configured publish checks; confirm the namespace is *verified*) |
| VS Code forks (Cursor, Windsurf, VSCodium, …) | Trust of the registry the fork installs from — usually Open VSX, **not** VS Code Marketplace (see `references/criteria/ide-plugin.md`) |

### CI/CD
| Source | Trust |
|---|---|
| GitHub Actions (actions/) official | High |
| GitHub Actions marketplace (verified creator) | Medium-High |
| GitHub Actions marketplace (unverified) | Medium-Low — pin to SHA |
| CircleCI Orbs (certified) | Medium-High |
| CircleCI Orbs (community) | Medium |
| Jenkins plugins (official) | Medium |
| Custom/third-party scripts | Low — code review required |

**Critical rule for GitHub Actions:** pin any action or reusable workflow that runs in a job holding secrets, a write-scoped token, `id-token: write`, or publish rights to a full commit SHA from the action's own repo (not a fork); tags and branches can be moved. Format: `uses: <owner>/<action>@<40-char SHA> # v<x.y.z>`. Ratings, immutable releases and lockfiles: `workflows/ci-action.md` and `references/criteria/ci-action.md`. The auto-REJECT case is the `SKILL.md` Red Flag "Mutable CI ref with privileged access".

## Untrusted / Always-Flag Sources
- Direct downloads from personal websites with no code signing
- Discord/Slack shared files
- Torrents or file sharing sites
- "Cracked" or "patched" versions of paid tools
- Packages that redirect to another package on install
- Any source where checksums are not verifiable
