<#
.SYNOPSIS
    Queries OSV.dev and GitHub Advisory Database for known vulnerabilities.

.DESCRIPTION
    Runs structured CVE lookups against OSV.dev and GHSA for registry packages.
    Normalizes results, filters by version if supplied, detects cross-DB discrepancies,
    and emits a JSON risk assessment to stdout.

    GITHUB_TOKEN: set $env:GITHUB_TOKEN to raise GHSA rate limit 60 -> 5000/hr.
    If unset or rate-limited, GHSA is skipped and OSV-only results are returned.
    Cache: scripts/.vuln-cache/<eco>-<name>[-<ver>].json, TTL 24 hr.

.PARAMETER Ecosystem
    Registry ecosystem. Supported: npm, pypi, crates, rubygems, nuget, go, maven, hex.

.PARAMETER Name
    Package name (required).

.PARAMETER Version
    Optional. Filters results to vulns affecting this version. Conservative:
    includes vuln if version-range data is absent.

.OUTPUTS
    JSON to stdout:
    {
      ecosystem, package, version?,
      osvResults:  [{id, aliases[], summary, severity, affectedVersions[]}],
      ghsaResults: [{id, aliases[], summary, severity, affectedVersions[]}],
      summary: {totalCount, osvCount, ghsaCount, highestSeverity},
      discrepancies: {onlyInOsv[], onlyInGhsa[]},
      sources: [],
      ghsaNote?,
      riskLevel
    }
#>
param(
    [Parameter(Mandatory)]
    [ValidateSet('npm', 'pypi', 'crates', 'rubygems', 'nuget', 'go', 'maven', 'hex')]
    [string]$Ecosystem,

    [Parameter(Mandatory)]
    [string]$Name,

    [string]$Version
)

$OsvEcoMap  = @{ npm='npm'; pypi='PyPI'; crates='crates.io'; rubygems='RubyGems';
                 nuget='NuGet'; go='Go'; maven='Maven'; hex='Hex' }
$GhsaEcoMap = @{ npm='npm'; pypi='pip'; crates='rust'; rubygems='rubygems';
                 nuget='nuget'; go='go'; maven='maven'; hex='erlang' }

# ─── Cache ───────────────────────────────────────────────────────────────────

function Get-CachePath($Key) {
    $cacheDir = Join-Path $PSScriptRoot '.vuln-cache'
    if (-not (Test-Path $cacheDir)) {
        New-Item -ItemType Directory -Path $cacheDir -Force | Out-Null
    }
    return Join-Path $cacheDir "$Key.json"
}

function Get-CachedResult($Key) {
    $path = Get-CachePath $Key
    if (-not (Test-Path $path)) { return $null }
    $age = (Get-Date) - (Get-Item $path).LastWriteTime
    if ($age.TotalHours -gt 24) { return $null }
    try { return Get-Content $path -Raw | ConvertFrom-Json }
    catch { return $null }
}

function Set-CachedResult($Key, $Data) {
    try {
        $path = Get-CachePath $Key
        $Data | ConvertTo-Json -Depth 8 | Set-Content -Path $path -Force
    } catch {
        # Cache write failure is non-fatal
    }
}

# ─── Severity helpers ────────────────────────────────────────────────────────

function Get-SeverityFromOsv($Vuln) {
    # Prefer database_specific.severity (HIGH/MODERATE/LOW/CRITICAL)
    if ($Vuln.database_specific -and $Vuln.database_specific.severity) {
        return Normalize-Severity $Vuln.database_specific.severity
    }
    # Try numeric CVSS score in severity array
    if ($Vuln.severity) {
        foreach ($s in $Vuln.severity) {
            if ($s.score -match '^\d+(\.\d+)?$') {
                $score = [double]$s.score
                if ($score -ge 9.0) { return 'critical' }
                if ($score -ge 7.0) { return 'high' }
                if ($score -ge 4.0) { return 'medium' }
                return 'low'
            }
        }
    }
    return 'medium'
}

function Normalize-Severity($Sev) {
    switch ($Sev.ToLower()) {
        'critical' { return 'critical' }
        'high'     { return 'high' }
        'moderate' { return 'medium' }
        'medium'   { return 'medium' }
        'low'      { return 'low' }
        default    { return 'medium' }
    }
}

# ─── Version range checking ──────────────────────────────────────────────────

function Compare-SemVer($A, $B) {
    # Returns -1, 0, 1. Returns 0 (equal = conservative include) if unparseable.
    if ($A -eq $B) { return 0 }
    if (-not $A -or $A -eq '0') { return -1 }
    try {
        $va = [System.Version]($A -replace '^v', '' -replace '[-+].*$', '')
        $vb = [System.Version]($B -replace '^v', '' -replace '[-+].*$', '')
        return $va.CompareTo($vb)
    } catch {
        return 0   # conservative
    }
}

function Test-OsvVersionAffected($Ver, $Ranges, $VersionsList) {
    if ((-not $Ranges -or $Ranges.Count -eq 0) -and
        (-not $VersionsList -or $VersionsList.Count -eq 0)) {
        return $true   # no range data — conservative include
    }
    # Check explicit versions list first
    if ($VersionsList -and $VersionsList.Count -gt 0) {
        if ($Ver -in $VersionsList) { return $true }
    }
    # Check semver/ecosystem ranges
    if ($Ranges) {
        foreach ($range in $Ranges) {
            if ($range.type -notin @('SEMVER', 'ECOSYSTEM')) { continue }
            $events = $range.events
            if (-not $events) { return $true }
            $introduced = $null
            foreach ($event in $events) {
                if ($null -ne $event.introduced) { $introduced = $event.introduced }
                if ($null -ne $event.fixed -and $null -ne $introduced) {
                    if ((Compare-SemVer $Ver $introduced) -ge 0 -and
                        (Compare-SemVer $Ver $event.fixed) -lt 0) { return $true }
                    $introduced = $null
                }
                if ($null -ne $event.last_affected -and $null -ne $introduced) {
                    if ((Compare-SemVer $Ver $introduced) -ge 0 -and
                        (Compare-SemVer $Ver $event.last_affected) -le 0) { return $true }
                    $introduced = $null
                }
            }
            # Open-ended range (introduced, no fixed)
            if ($null -ne $introduced) {
                $floor = if ($introduced -eq '0') { -1 } else { Compare-SemVer $Ver $introduced }
                if ($floor -ge 0) { return $true }
            }
        }
    }
    return $false
}

function Test-GhsaVersionAffected($Ver, $RangeStrings) {
    # GHSA ranges like "< 4.17.21" or ">= 4.0.0, < 4.17.21"
    foreach ($rangeStr in $RangeStrings) {
        $parts = $rangeStr -split ',' | ForEach-Object { $_.Trim() }
        $inRange = $true
        foreach ($part in $parts) {
            if ($part -match '^(>=|<=|>|<|=)\s*(.+)$') {
                $op    = $Matches[1]
                $bound = $Matches[2].Trim()
                $cmp   = Compare-SemVer $Ver $bound
                $ok    = switch ($op) {
                    '>=' { $cmp -ge 0 }; '<=' { $cmp -le 0 }
                    '>'  { $cmp -gt 0 }; '<'  { $cmp -lt 0 }
                    '='  { $cmp -eq 0 }; default { $true }
                }
                if (-not $ok) { $inRange = $false; break }
            } else { return $true }   # unparseable — conservative
        }
        if ($inRange) { return $true }
    }
    return $false
}

# ─── OSV query ───────────────────────────────────────────────────────────────

function Invoke-OsvQuery {
    $body = @{ package = @{ name = $Name; ecosystem = $OsvEcoMap[$Ecosystem] } } |
            ConvertTo-Json -Depth 3
    $resp = Invoke-RestMethod -Uri 'https://api.osv.dev/v1/query' `
        -Method POST -ContentType 'application/json' -Body $body `
        -Headers @{ 'User-Agent' = 'install-auditor/1.0' } -TimeoutSec 20

    $results = @()
    if (-not $resp.vulns) { return $results }

    foreach ($v in $resp.vulns) {
        $affectedRanges   = @()
        $affectedVersions = @()
        foreach ($a in $v.affected) {
            if ($a.package.name -eq $Name) {
                if ($a.ranges)   { $affectedRanges   += $a.ranges }
                if ($a.versions) { $affectedVersions += $a.versions }
            }
        }
        $include = if ($Version) {
            Test-OsvVersionAffected $Version $affectedRanges $affectedVersions
        } else { $true }

        if ($include) {
            $results += [ordered]@{
                id               = $v.id
                aliases          = @($v.aliases | Where-Object { $_ })
                summary          = $v.summary
                severity         = Get-SeverityFromOsv $v
                affectedVersions = $affectedVersions
            }
        }
    }
    return $results
}

# ─── GHSA query ──────────────────────────────────────────────────────────────

function Invoke-GhsaQuery {
    $eco     = $GhsaEcoMap[$Ecosystem]
    $encoded = [Uri]::EscapeDataString($Name)
    $uri     = "https://api.github.com/advisories?affects=$encoded&ecosystem=$eco&per_page=100"
    $headers = @{
        'User-Agent' = 'install-auditor/1.0'
        'Accept'     = 'application/vnd.github+json'
    }
    if ($env:GITHUB_TOKEN) { $headers['Authorization'] = "Bearer $env:GITHUB_TOKEN" }

    try {
        $resp    = Invoke-RestMethod -Uri $uri -Headers $headers -TimeoutSec 20
        $results = @()
        foreach ($adv in $resp) {
            $affectedRanges = @()
            $relevant       = $false
            foreach ($vuln in $adv.vulnerabilities) {
                if ($vuln.package.name -eq $Name) {
                    $relevant = $true
                    if ($vuln.vulnerable_version_range) {
                        $affectedRanges += $vuln.vulnerable_version_range
                    }
                }
            }
            if (-not $relevant) { continue }

            $include = if ($Version -and $affectedRanges.Count -gt 0) {
                Test-GhsaVersionAffected $Version $affectedRanges
            } else { $true }

            if ($include) {
                $aliases = @()
                if ($adv.cve_id) { $aliases += $adv.cve_id }
                $sev = if ($adv.severity) { Normalize-Severity $adv.severity } else { 'medium' }
                $results += [ordered]@{
                    id               = $adv.ghsa_id
                    aliases          = $aliases
                    summary          = $adv.summary
                    severity         = $sev
                    affectedVersions = $affectedRanges
                }
            }
        }
        return $results
    } catch {
        return $null   # graceful degradation
    }
}

# ─── Discrepancy detection ───────────────────────────────────────────────────

function Get-Discrepancies($OsvResults, $GhsaResults) {
    $osvCves  = @{}
    $ghsaCves = @{}
    foreach ($r in $OsvResults) {
        foreach ($alias in $r.aliases) {
            if ($alias -match '^CVE-') { $osvCves[$alias] = $r.id }
        }
    }
    foreach ($r in $GhsaResults) {
        foreach ($alias in $r.aliases) {
            if ($alias -match '^CVE-') { $ghsaCves[$alias] = $r.id }
        }
    }
    return [ordered]@{
        onlyInOsv  = @($osvCves.Keys  | Where-Object { -not $ghsaCves.ContainsKey($_) })
        onlyInGhsa = @($ghsaCves.Keys | Where-Object { -not $osvCves.ContainsKey($_) })
    }
}

# ─── Risk level ──────────────────────────────────────────────────────────────

function Get-RiskLevel($Results) {
    $order = @{ none = 0; low = 1; medium = 2; high = 3; critical = 4 }
    $highest = 'none'
    foreach ($r in $Results) {
        if ($order[$r.severity] -gt $order[$highest]) { $highest = $r.severity }
    }
    return $highest
}

# ─── Main ────────────────────────────────────────────────────────────────────

$cacheKey = "$Ecosystem-$Name$(if ($Version) { "-$Version" })"
$cached   = Get-CachedResult $cacheKey
if ($cached) { $cached | ConvertTo-Json -Depth 8; exit 0 }

try {
    $osvResults  = Invoke-OsvQuery
    $ghsaResults = Invoke-GhsaQuery
    $sources     = @('OSV')
    $ghsaNote    = $null

    if ($null -eq $ghsaResults) {
        $ghsaNote    = 'skipped — query failed or rate-limited'
        $ghsaResults = @()
    } else {
        $sources += 'GHSA'
    }

    $allResults   = @($osvResults) + @($ghsaResults)
    $discrepancies = Get-Discrepancies $osvResults $ghsaResults
    $riskLevel    = Get-RiskLevel $allResults

    $output = [ordered]@{
        ecosystem     = $Ecosystem
        package       = $Name
        osvResults    = $osvResults
        ghsaResults   = $ghsaResults
        summary       = [ordered]@{
            totalCount      = $allResults.Count
            osvCount        = $osvResults.Count
            ghsaCount       = $ghsaResults.Count
            highestSeverity = $riskLevel
        }
        discrepancies = $discrepancies
        sources       = $sources
        riskLevel     = $riskLevel
    }
    if ($Version)  { $output['version']  = $Version }
    if ($ghsaNote) { $output['ghsaNote'] = $ghsaNote }

    Set-CachedResult $cacheKey $output
    $output | ConvertTo-Json -Depth 8
} catch {
    [ordered]@{
        ecosystem = $Ecosystem
        package   = $Name
        error     = $_.Exception.Message
        riskLevel = 'unknown'
    } | ConvertTo-Json -Depth 3
}
