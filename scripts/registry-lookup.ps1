<#
.SYNOPSIS
    Registry Lookup — fetches package metadata from official registry APIs.

.DESCRIPTION
    Queries npm, PyPI, crates.io, RubyGems, NuGet, and OpenSSF Scorecard APIs
    to gather hard data for install audits (downloads, maintainers, vulnerabilities, etc.)

.PARAMETER Ecosystem
    One of: npm, pypi, crates, rubygems, nuget

.PARAMETER Name
    Package name (e.g., lodash, requests, serde)

.PARAMETER Version
    Optional. Specific version to check. Defaults to latest.

.EXAMPLE
    .\registry-lookup.ps1 npm lodash
    .\registry-lookup.ps1 npm lodash 4.17.21
    .\registry-lookup.ps1 pypi requests
    .\registry-lookup.ps1 crates serde
#>

param(
    [Parameter(Mandatory=$true, Position=0)]
    [ValidateSet('npm','pypi','crates','rubygems','nuget')]
    [string]$Ecosystem,

    [Parameter(Mandatory=$true, Position=1)]
    [string]$Name,

    [Parameter(Position=2)]
    [string]$Version
)

$ErrorActionPreference = 'Stop'

function Invoke-Api {
    param([string]$Url)
    try {
        $response = Invoke-RestMethod -Uri $Url -Headers @{ 'User-Agent' = 'install-auditor/1.0' } -TimeoutSec 15
        return $response
    } catch {
        return $null
    }
}

function Get-DaysSince {
    param([string]$DateStr)
    if (-not $DateStr) { return $null }
    try {
        $d = [DateTime]::Parse($DateStr)
        return [math]::Floor(((Get-Date) - $d).TotalDays)
    } catch {
        return $null
    }
}

function Format-DateStr {
    param([string]$DateStr)
    if (-not $DateStr) { return 'unknown' }
    try {
        return ([DateTime]::Parse($DateStr)).ToString('yyyy-MM-dd')
    } catch {
        return 'unknown'
    }
}

# ─── npm ─────────────────────────────────────────────────────────────────

function Lookup-Npm {
    $pkg = Invoke-Api "https://registry.npmjs.org/$([Uri]::EscapeDataString($Name))"
    if (-not $pkg) { throw "Package '$Name' not found on npm" }

    $latest = if ($Version) { $Version } else { $pkg.'dist-tags'.latest }
    $versionData = $pkg.versions.$latest
    $time = $pkg.time

    # Weekly downloads
    $weeklyDownloads = $null
    $dl = Invoke-Api "https://api.npmjs.org/downloads/point/last-week/$([Uri]::EscapeDataString($Name))"
    if ($dl) { $weeklyDownloads = $dl.downloads }

    # Maintainers
    $maintainers = @($pkg.maintainers | ForEach-Object { $_.name }) | Where-Object { $_ }

    # Install scripts
    $scripts = $versionData.scripts
    $installScripts = @()
    foreach ($hook in @('preinstall','install','postinstall')) {
        if ($scripts.$hook) {
            $installScripts += @{ hook = $hook; command = $scripts.$hook }
        }
    }

    # Dependencies
    $deps = @()
    if ($versionData.dependencies) {
        $deps = @($versionData.dependencies.PSObject.Properties.Name)
    }

    return [ordered]@{
        ecosystem        = 'npm'
        name             = $pkg.name
        version          = $latest
        description      = $pkg.description
        license          = if ($versionData.license) { $versionData.license } else { $pkg.license }
        homepage         = $pkg.homepage
        repository       = if ($pkg.repository -is [string]) { $pkg.repository } else { $pkg.repository.url }
        publishedAt      = Format-DateStr $time.$latest
        daysSincePublish = Get-DaysSince $time.$latest
        createdAt        = Format-DateStr $time.created
        lastModified     = Format-DateStr $time.modified
        maintainers      = $maintainers
        maintainerCount  = $maintainers.Count
        weeklyDownloads  = $weeklyDownloads
        versionCount     = @($pkg.versions.PSObject.Properties).Count
        deprecated       = if ($versionData.deprecated) { $versionData.deprecated } else { $null }
        installScripts   = if ($installScripts.Count -gt 0) { $installScripts } else { $null }
        dependencies     = $deps
        dependencyCount  = $deps.Count
        engines          = $versionData.engines
    }
}

# ─── PyPI ────────────────────────────────────────────────────────────────

function Lookup-Pypi {
    $url = if ($Version) {
        "https://pypi.org/pypi/$([Uri]::EscapeDataString($Name))/$Version/json"
    } else {
        "https://pypi.org/pypi/$([Uri]::EscapeDataString($Name))/json"
    }
    $pkg = Invoke-Api $url
    if (-not $pkg) { throw "Package '$Name' not found on PyPI" }

    $info = $pkg.info
    $urls = $pkg.urls

    # Monthly downloads
    $monthlyDownloads = $null
    $stats = Invoke-Api "https://pypistats.org/api/packages/$([Uri]::EscapeDataString($Name))/recent"
    if ($stats -and $stats.data) { $monthlyDownloads = $stats.data.last_month }

    # Maintainers
    $maintainers = @($info.author, $info.maintainer) | Where-Object { $_ }

    # Dependencies
    $deps = @()
    if ($info.requires_dist) {
        $deps = @($info.requires_dist | ForEach-Object { ($_ -split ' ')[0] })
    }

    $publishDate = if ($urls -and $urls.Count -gt 0) { $urls[0].upload_time_iso_8601 } else { $null }

    return [ordered]@{
        ecosystem        = 'pypi'
        name             = $info.name
        version          = $info.version
        description      = $info.summary
        license          = if ($info.license) { $info.license } else { 'unknown' }
        homepage         = if ($info.home_page) { $info.home_page } elseif ($info.project_urls.Homepage) { $info.project_urls.Homepage } else { $null }
        repository       = if ($info.project_urls.Source) { $info.project_urls.Source } elseif ($info.project_urls.Repository) { $info.project_urls.Repository } else { $null }
        publishedAt      = Format-DateStr $publishDate
        daysSincePublish = Get-DaysSince $publishDate
        maintainers      = $maintainers
        maintainerCount  = $maintainers.Count
        monthlyDownloads = $monthlyDownloads
        versionCount     = @($pkg.releases.PSObject.Properties).Count
        deprecated       = if ($info.classifiers -match 'Inactive') { $true } else { $null }
        requiresPython   = $info.requires_python
        dependencies     = $deps
        dependencyCount  = $deps.Count
    }
}

# ─── crates.io ───────────────────────────────────────────────────────────

function Lookup-Crates {
    $pkg = Invoke-Api "https://crates.io/api/v1/crates/$([Uri]::EscapeDataString($Name))"
    if (-not $pkg) { throw "Crate '$Name' not found" }

    $crate = $pkg.crate
    $versions = $pkg.versions
    $latest = if ($Version) {
        $versions | Where-Object { $_.num -eq $Version } | Select-Object -First 1
    } else {
        $versions | Select-Object -First 1
    }

    return [ordered]@{
        ecosystem       = 'crates.io'
        name            = $crate.name
        version         = if ($latest) { $latest.num } else { 'unknown' }
        description     = $crate.description
        license         = if ($latest) { $latest.license } else { 'unknown' }
        homepage        = $crate.homepage
        repository      = $crate.repository
        publishedAt     = if ($latest) { Format-DateStr $latest.created_at } else { 'unknown' }
        daysSincePublish = if ($latest) { Get-DaysSince $latest.created_at } else { $null }
        totalDownloads  = $crate.downloads
        recentDownloads = $crate.recent_downloads
        versionCount    = $versions.Count
    }
}

# ─── RubyGems ────────────────────────────────────────────────────────────

function Lookup-Rubygems {
    $pkg = Invoke-Api "https://rubygems.org/api/v1/gems/$([Uri]::EscapeDataString($Name)).json"
    if (-not $pkg) { throw "Gem '$Name' not found" }

    return [ordered]@{
        ecosystem        = 'rubygems'
        name             = $pkg.name
        version          = $pkg.version
        description      = $pkg.info
        license          = if ($pkg.licenses) { $pkg.licenses -join ', ' } else { 'unknown' }
        homepage         = $pkg.homepage_uri
        repository       = $pkg.source_code_uri
        publishedAt      = Format-DateStr $pkg.version_created_at
        daysSincePublish = Get-DaysSince $pkg.version_created_at
        totalDownloads   = $pkg.downloads
        versionDownloads = $pkg.version_downloads
    }
}

# ─── NuGet ───────────────────────────────────────────────────────────────

function Lookup-Nuget {
    $pkg = Invoke-Api "https://api.nuget.org/v3/registration5-gz-semver2/$($Name.ToLower())/index.json"
    if (-not $pkg) { throw "NuGet package '$Name' not found" }

    $pages = $pkg.items
    $lastPage = $pages[-1]
    # Some pages need fetching
    $items = if ($lastPage.items) { $lastPage.items } else {
        $page = Invoke-Api $lastPage.'@id'
        if ($page) { $page.items } else { @() }
    }

    $latest = if ($Version) {
        $items | Where-Object { $_.catalogEntry.version -eq $Version } | Select-Object -First 1
    } else {
        $items[-1]
    }
    $entry = $latest.catalogEntry

    return [ordered]@{
        ecosystem        = 'nuget'
        name             = if ($entry.id) { $entry.id } else { $Name }
        version          = if ($entry.version) { $entry.version } else { 'unknown' }
        description      = $entry.description
        license          = if ($entry.licenseExpression) { $entry.licenseExpression } elseif ($entry.licenseUrl) { $entry.licenseUrl } else { 'unknown' }
        homepage         = $entry.projectUrl
        publishedAt      = Format-DateStr $entry.published
        daysSincePublish = Get-DaysSince $entry.published
        listed           = $entry.listed -ne $false
        versionCount     = $items.Count
    }
}

# ─── OpenSSF Scorecard ───────────────────────────────────────────────────

function Lookup-OpenSSF {
    param([string]$RepoUrl)
    if (-not $RepoUrl) { return $null }

    if ($RepoUrl -match 'github\.com[/:]([^/]+/[^/.]+)') {
        $repo = $Matches[1] -replace '\.git$',''
    } else {
        return $null
    }

    $data = Invoke-Api "https://api.securityscorecards.dev/projects/github.com/$repo"
    if (-not $data) { return $null }

    $checks = @()
    if ($data.checks) {
        $checks = @($data.checks | ForEach-Object { @{ name = $_.name; score = $_.score } })
    }

    return [ordered]@{
        score  = $data.score
        date   = $data.date
        checks = $checks
    }
}

# ─── Main ────────────────────────────────────────────────────────────────

$result = switch ($Ecosystem) {
    'npm'      { Lookup-Npm }
    'pypi'     { Lookup-Pypi }
    'crates'   { Lookup-Crates }
    'rubygems' { Lookup-Rubygems }
    'nuget'    { Lookup-Nuget }
}

# Try OpenSSF scorecard if we found a repo URL
$repoUrl = $result.repository
if ($repoUrl) {
    $scorecard = Lookup-OpenSSF $repoUrl
    if ($scorecard) {
        $result['openssf'] = $scorecard
    }
}

$result | ConvertTo-Json -Depth 5
