# Registry & Source Trust Guide

## Trusted Registries by Ecosystem

### JavaScript / Node.js
- **npmjs.com** — Official registry. Medium baseline trust. Verified publishers (scoped packages from known orgs) are higher trust.
- **GitHub Packages (npm)** — Packages tied to GitHub org identity. Higher trust for known orgs.
- **jsr.io** — Deno/JSR registry. Newer, requires GitHub auth, moderate trust.
- **Unpkg / CDN links** — Never install from CDN links directly in package.json; flag immediately.

**Red flags:** Packages with install scripts (`preinstall`, `postinstall`, `install`) that aren't from a known tool (e.g., node-gyp, esbuild). Always review what these scripts do.

### Python
- **pypi.org** — Official. Medium baseline. No mandatory publishing auth; typosquatting common.
- **conda-forge** — Community-reviewed conda packages. Higher trust.
- **Anaconda repository** — Curated. Higher trust.
- **GitHub releases (wheel/sdist)** — Acceptable if from verified org; check checksums.
- **Direct git installs (`pip install git+...`)** — Flag; commit SHA pinning required.

**Red flags:** `setup.py` with `os.system()` calls, packages that shadow stdlib names.

### Ruby
- **rubygems.org** — Official. Similar trust profile to PyPI.

### Rust
- **crates.io** — Requires GitHub auth to publish. Higher baseline trust than npm/PyPI.

### Go
- **pkg.go.dev / go get** — Module proxy validates checksums via sumdb. High trust for modules in the index. Direct VCS installs bypass this — flag.

### Java / JVM
- **Maven Central** — Requires GPG signing. High trust.
- **JCenter** — Deprecated (shut down); any dependency still pointing here is a flag.
- **Custom Artifactory/Nexus** — Organization-controlled; verify org controls it.
- **Jitpack** — Builds from GitHub directly. Lower trust.

### .NET
- **NuGet.org** — Microsoft-operated. Medium-high trust. Package signing available; check for signed packages.

### Container Images
| Source | Trust |
|---|---|
| Official Docker Hub images (library/) | High |
| Docker Hub verified publishers | Medium-High |
| Docker Hub community images | Low-Medium |
| GitHub Container Registry (ghcr.io) from known orgs | Medium-High |
| Amazon ECR Public | Medium |
| Quay.io (Red Hat) | Medium |
| Random Docker Hub with <100 pulls | Low |
| Self-hosted registry (unknown) | Low — verify provenance |

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
| JetBrains Marketplace | Medium-High (JetBrains review process) |
| Vim-Plug / GitHub-sourced Vim plugins | Low-Medium (no central review) |
| Emacs MELPA | Low-Medium (community-maintained) |
| Cursor extensions (VS Code compatible) | Same as VS Code Marketplace |

### CI/CD
| Source | Trust |
|---|---|
| GitHub Actions (actions/) official | High |
| GitHub Actions marketplace (verified creator) | Medium-High |
| GitHub Actions marketplace (unverified) | Medium — pin to SHA |
| CircleCI Orbs (certified) | Medium-High |
| CircleCI Orbs (community) | Medium |
| Jenkins plugins (official) | Medium |
| Custom/third-party scripts | Low — code review required |

**Critical rule for GitHub Actions:** Any action that accesses `secrets.*` MUST be pinned to a commit SHA, not a tag. Tags can be moved. Example: `uses: actions/checkout@v4` → should be `uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683`.

## Untrusted / Always-Flag Sources
- Direct downloads from personal websites with no code signing
- Discord/Slack shared files
- Torrents or file sharing sites
- "Cracked" or "patched" versions of paid tools
- Packages that redirect to another package on install
- Any source where checksums are not verifiable
