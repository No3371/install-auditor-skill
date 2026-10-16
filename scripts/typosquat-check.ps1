<#
.SYNOPSIS
    Typosquat Check — algorithmic similarity detection for registry packages.

.DESCRIPTION
    Loads the bundled popular-package baseline (data/npm-popular.tsv: unscoped
    npm packages ranked by weekly downloads), computes Levenshtein edit distance
    between the queried name and baseline packages, detects combosquat patterns
    (prefix/suffix overlap), compares live download counts, and emits a
    structured JSON risk assessment to stdout. A queried name that is itself in
    the baseline is reported low risk. Refresh the baseline with
    data/refresh-npm-popular.py.

    npm v1 — other ecosystems will be added in future versions.

.PARAMETER Ecosystem
    Registry ecosystem. Currently only 'npm' is supported.

.PARAMETER Name
    Exact package name to check (e.g., 'expresss', '@scope/pkg').

.PARAMETER CompareTo
    Optional. Known legitimate package name to compare against directly.

.PARAMETER Size
    Number of baseline packages to use, from the top of data/npm-popular.tsv.
    Default: 1000.

.PARAMETER CacheHours
    Ignored. Accepted so existing invocations keep working (the baseline is a bundled file).

.PARAMETER NoCache
    Ignored. Accepted so existing invocations keep working (the baseline is a bundled file).

.EXAMPLE
    .\typosquat-check.ps1 -Ecosystem npm -Name "expresss"
    .\typosquat-check.ps1 -Ecosystem npm -Name "lodahs" -CompareTo "lodash"
    .\typosquat-check.ps1 -Ecosystem npm -Name "chalk" -Size 500
#>

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('npm')]
    [string]$Ecosystem,

    [Parameter(Mandatory=$true)]
    [string]$Name,

    [Parameter()]
    [string]$CompareTo,

    [Parameter()]
    [int]$Size = 1000,

    [Parameter()]
    [int]$CacheHours = 24,

    [switch]$NoCache
)

$ErrorActionPreference = 'Stop'

# ─── Helpers ────────────────────────────────────────────────────────────

function Invoke-Api {
    param([string]$Url)
    try {
        $response = Invoke-RestMethod -Uri $Url -Headers @{ 'User-Agent' = 'install-auditor/1.0' } -TimeoutSec 15
        return $response
    } catch {
        return $null
    }
}

function Get-ComparisonToken {
    <#
    .SYNOPSIS
        Normalize a package name for comparison: lowercase, fold separators,
        strip scope prefix for cross-format matching.
    #>
    param([string]$RawName)
    $n = $RawName.ToLower().Trim()
    # Strip @scope/ prefix for comparison (keep raw name elsewhere)
    if ($n -match '^@[^/]+/(.+)$') {
        $n = $Matches[1]
    }
    # Fold hyphens and underscores to a single separator
    $n = $n -replace '[-_]+', '-'
    return $n
}

function Get-LevenshteinDistance {
    <#
    .SYNOPSIS
        Classic O(m*n) two-row Levenshtein distance. No external modules.
    #>
    param(
        [string]$Source,
        [string]$Target
    )
    $m = $Source.Length
    $n = $Target.Length

    if ($m -eq 0) { return $n }
    if ($n -eq 0) { return $m }

    # Two-row approach
    [int[]]$prev = 0..$n
    [int[]]$curr = [int[]]::new($n + 1)

    for ($i = 1; $i -le $m; $i++) {
        $curr[0] = $i
        for ($j = 1; $j -le $n; $j++) {
            $cost = if ($Source[$i - 1] -eq $Target[$j - 1]) { 0 } else { 1 }
            $curr[$j] = [math]::Min(
                [math]::Min($curr[$j - 1] + 1, $prev[$j] + 1),
                $prev[$j - 1] + $cost
            )
        }
        # Swap rows
        $temp = $prev
        $prev = $curr
        $curr = $temp
    }
    return $prev[$n]
}

# ─── npm Baseline Fetch ─────────────────────────────────────────────────

function Get-NpmPopularBaseline {
    # Returns the first $Size rows of the bundled baseline as @{ name; downloads }; empty if unreadable.
    # The leading comma keeps a 0- or 1-row result an array instead of letting the pipeline unroll it.
    $path = Join-Path (Join-Path $PSScriptRoot 'data') 'npm-popular.tsv'
    if (-not (Test-Path $path)) { return ,@() }
    $rows = foreach ($line in (Get-Content -Path $path -Encoding UTF8)) {
        $t = $line.Trim()
        if (-not $t -or $t.StartsWith('#')) { continue }
        $f = $t -split "`t", 2
        $dl = [long]0
        if ($f.Count -gt 1) { [void][long]::TryParse($f[1].Trim(), [ref]$dl) }
        @{ name = $f[0].Trim(); downloads = $dl }
    }
    return ,@($rows | Select-Object -First ([math]::Max($Size, 0)))
}

# ─── npm Download Count ─────────────────────────────────────────────────

function Get-NpmWeeklyDownloads {
    param([string]$PackageName)
    $encoded = [Uri]::EscapeDataString($PackageName)
    $dl = Invoke-Api "https://api.npmjs.org/downloads/point/last-week/$encoded"
    if ($dl -and $null -ne $dl.downloads) {
        return [long]$dl.downloads
    }
    return $null
}

function Test-NpmPackageExists {
    # $true if the registry has the package, $false on HTTP 404, $null when the registry is unreachable.
    param([string]$PackageName)
    $encoded = [Uri]::EscapeDataString($PackageName)
    try {
        Invoke-WebRequest -Uri "https://registry.npmjs.org/$encoded" -Method Head -UseBasicParsing `
            -Headers @{ 'User-Agent' = 'install-auditor/1.0' } -TimeoutSec 15 | Out-Null
        return $true
    } catch {
        $status = $null
        if ($_.Exception.Response) { $status = [int]$_.Exception.Response.StatusCode }
        if ($status -eq 404) { return $false }
        return $null
    }
}

# ─── Core Analysis ──────────────────────────────────────────────────────

function Invoke-TyposquatAnalysis {
    $normalizedName = Get-ComparisonToken $Name

    # Fetch baseline
    $baseline = Get-NpmPopularBaseline
    if (-not $baseline -or $baseline.Count -eq 0) {
        # API failure fallback: still check CompareTo if provided
        $baseline = @()
    }

    # Exact raw-name match, not the normalized token: "@evil/chalk" normalizes to "chalk"
    # but is not the baseline package.
    $knownPopular = $false
    foreach ($b in $baseline) {
        if ($b.name -eq $Name) { $knownPopular = $true; break }
    }

    # If -CompareTo is provided, ensure it's in the candidate list
    $candidates = [System.Collections.ArrayList]@()
    if ($CompareTo) {
        $compareNorm = Get-ComparisonToken $CompareTo
        $alreadyInBaseline = $false
        foreach ($b in $baseline) {
            if ($b.name -eq $CompareTo) { $alreadyInBaseline = $true; break }
        }
        if (-not $alreadyInBaseline) {
            [void]$candidates.Add(@{ name = $CompareTo; downloads = 0 })
        }
    }
    foreach ($b in $baseline) {
        [void]$candidates.Add($b)
    }

    # ── Levenshtein matching ────────────────────────────────────────────
    $closestMatches = @()
    foreach ($c in $candidates) {
        $cNorm = Get-ComparisonToken $c.name
        # Skip self
        if ($cNorm -eq $normalizedName) { continue }
        $dist = Get-LevenshteinDistance $normalizedName $cNorm
        if ($dist -le 3) {
            $closestMatches += @{
                name     = $c.name
                distance = $dist
                downloads = $c.downloads
            }
        }
    }
    # Sort by distance, then by downloads descending
    $closestMatches = @($closestMatches | Sort-Object { $_.distance }, { -$_.downloads })
    # Keep top 10
    if ($closestMatches.Count -gt 10) {
        $closestMatches = $closestMatches[0..9]
    }

    # ── Combosquat detection ────────────────────────────────────────────
    $combosquatHints = @()
    $top100 = if ($baseline.Count -gt 100) { $baseline[0..99] } else { $baseline }
    foreach ($b in $top100) {
        $bNorm = Get-ComparisonToken $b.name
        # Skip trivial equality
        if ($bNorm -eq $normalizedName) { continue }
        # Skip very short names (< 3 chars) to reduce noise
        if ($bNorm.Length -lt 3) { continue }
        # Check if target starts/ends with popular name or vice versa
        $isCombo = $false
        if ($normalizedName.Length -gt $bNorm.Length) {
            if ($normalizedName.StartsWith($bNorm) -or $normalizedName.EndsWith($bNorm)) {
                $isCombo = $true
            }
        }
        if ($bNorm.Length -gt $normalizedName.Length) {
            if ($bNorm.StartsWith($normalizedName) -or $bNorm.EndsWith($normalizedName)) {
                $isCombo = $true
            }
        }
        if ($isCombo) {
            $combosquatHints += $b.name
        }
    }

    # ── Download ratio ──────────────────────────────────────────────────
    $downloadRatio = $null
    $bestCompare = $null

    if ($CompareTo) {
        $bestCompare = $CompareTo
    } elseif ($closestMatches.Count -gt 0) {
        $bestCompare = $closestMatches[0].name
    }

    if ($bestCompare -and -not $knownPopular) {
        $queriedDl = Get-NpmWeeklyDownloads $Name
        $closestDl = Get-NpmWeeklyDownloads $bestCompare
        if ($null -ne $queriedDl -and $null -ne $closestDl -and $queriedDl -ge 0) {
            $ratio = if ($queriedDl -gt 0) {
                [math]::Round($closestDl / $queriedDl, 2)
            } else {
                # Queried package has 0 downloads
                if ($closestDl -gt 0) { [double]::PositiveInfinity } else { 1.0 }
            }
            # Handle infinity for JSON
            $ratioValue = if ([double]::IsInfinity($ratio)) { -1 } else { $ratio }
            $downloadRatio = @{
                queried = $queriedDl
                closest = $closestDl
                ratio   = $ratioValue
            }

            # Update closest match download count with real data
            foreach ($cm in $closestMatches) {
                if ($cm.name -eq $bestCompare) {
                    $cm.downloads = $closestDl
                    break
                }
            }
        }
    }

    # ── Risk scoring ────────────────────────────────────────────────────
    $riskLevel = 'low'
    $riskReasons = @()

    $minDist = if ($closestMatches.Count -gt 0) { $closestMatches[0].distance } else { 999 }
    $hasExplicitCompare = [bool]$CompareTo

    # Distance-based risk
    if ($minDist -eq 1) {
        $riskLevel = 'high'
        $riskReasons += "Edit distance 1 from '$($closestMatches[0].name)'"
    } elseif ($minDist -eq 2) {
        $riskLevel = 'medium'
        $riskReasons += "Edit distance 2 from '$($closestMatches[0].name)'"
    } elseif ($minDist -eq 3) {
        if ($riskLevel -eq 'low') { $riskLevel = 'low' }
        $riskReasons += "Edit distance 3 from '$($closestMatches[0].name)' (borderline)"
    }

    # Download ratio escalation
    if ($downloadRatio -and $downloadRatio.ratio -ne $null) {
        $r = $downloadRatio.ratio
        if ($r -eq -1 -or $r -ge 1000) {
            # Infinite or 1000x+ ratio — very suspicious
            if ($minDist -le 2) {
                $riskLevel = 'critical'
                $riskReasons += "Download ratio >= 1000x (queried: $($downloadRatio.queried), closest: $($downloadRatio.closest))"
            }
        } elseif ($r -ge 100) {
            if ($riskLevel -eq 'high' -or $minDist -le 1) {
                $riskLevel = 'critical'
            } elseif ($riskLevel -ne 'critical') {
                $riskLevel = 'high'
            }
            $riskReasons += "Download ratio >= 100x (queried: $($downloadRatio.queried), closest: $($downloadRatio.closest))"
        } elseif ($r -ge 10) {
            if ($riskLevel -eq 'medium') {
                $riskLevel = 'high'
            }
            $riskReasons += "Download ratio >= 10x (queried: $($downloadRatio.queried), closest: $($downloadRatio.closest))"
        }
    }

    # Explicit -CompareTo escalation: if user suspects a squat, raise floor
    if ($hasExplicitCompare -and $minDist -le 2 -and $riskLevel -eq 'medium') {
        $riskLevel = 'high'
        $riskReasons += "Explicit -CompareTo provided with close edit distance"
    }

    # Combosquat adds to risk
    if ($combosquatHints.Count -gt 0) {
        if ($riskLevel -eq 'low') { $riskLevel = 'medium' }
        $riskReasons += "Combosquat pattern detected: name overlaps with $($combosquatHints -join ', ')"
    }

    if ($knownPopular) {
        # Baseline members sit within edit distance 2 of each other (chalk/chai, react/redux)
        # and prefix each other (react/react-dom); scoring them would flag every popular package.
        $riskLevel       = 'low'
        $riskReasons     = @()
        $combosquatHints = @()
    }

    $queriedExists = if ($knownPopular) { $true } else { Test-NpmPackageExists $Name }

    # Build human-readable summary
    $details = if ($knownPopular) {
        "'$Name' is in the bundled top-$($baseline.Count) popular npm package baseline; distance and combosquat signals are not scored. "
    } elseif ($riskReasons.Count -gt 0) {
        "Risk factors: $($riskReasons -join '; '). "
    } else {
        "No close matches found in top-$($baseline.Count) popular packages. "
    }
    if ($baseline.Count -eq 0) {
        $details += "Popular-package baseline (data/npm-popular.tsv) missing or unreadable; only -CompareTo was checked. "
    }
    if ($queriedExists -eq $false) {
        $details += "Note: '$Name' does not exist on npm (registry returned 404). "
    } elseif ($null -eq $queriedExists) {
        $details += "Note: could not confirm '$Name' exists on npm (registry unreachable). "
    }
    if ($combosquatHints.Count -gt 0) {
        $details += "Combosquat hints: $($combosquatHints -join ', '). "
    }

    # ── Build output ────────────────────────────────────────────────────
    $output = [ordered]@{
        ecosystem       = $Ecosystem
        queriedName     = $Name
        normalizedName  = $normalizedName
        compareTo       = if ($CompareTo) { $CompareTo } else { $null }
        riskLevel       = $riskLevel
        closestMatches  = $closestMatches
        combosquatHints = $combosquatHints
        downloadRatio   = $downloadRatio
        details         = $details.Trim()
    }

    return $output
}

# ─── Main ────────────────────────────────────────────────────────────────

try {
    $result = Invoke-TyposquatAnalysis
    $result | ConvertTo-Json -Depth 6
} catch {
    # Structured error output for machine parsing
    [ordered]@{
        ecosystem   = $Ecosystem
        queriedName = $Name
        error       = $_.Exception.Message
        riskLevel   = 'unknown'
    } | ConvertTo-Json -Depth 3
}
