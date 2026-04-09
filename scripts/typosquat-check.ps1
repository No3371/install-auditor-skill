<#
.SYNOPSIS
    Typosquat Check — algorithmic similarity detection for registry packages.

.DESCRIPTION
    Fetches a popular-package baseline from the npm search API, computes
    Levenshtein edit distance between the queried name and popular packages,
    detects combosquat patterns (prefix/suffix overlap), compares download
    counts, and emits a structured JSON risk assessment to stdout.

    npm v1 — other ecosystems will be added in future versions.

.PARAMETER Ecosystem
    Registry ecosystem. Currently only 'npm' is supported.

.PARAMETER Name
    Exact package name to check (e.g., 'expresss', '@scope/pkg').

.PARAMETER CompareTo
    Optional. Known legitimate package name to compare against directly.

.PARAMETER Size
    Number of popular packages to fetch from the search API baseline.
    Default: 250.

.PARAMETER CacheHours
    Hours to cache the popular-package baseline. Default: 24.

.PARAMETER NoCache
    Skip cache — always fetch fresh baseline from the API.

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
    [int]$Size = 250,

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

# ─── Cache ──────────────────────────────────────────────────────────────

function Get-CachePath {
    $cacheDir = Join-Path $PSScriptRoot '.typosquat-cache'
    if (-not (Test-Path $cacheDir)) {
        New-Item -ItemType Directory -Path $cacheDir -Force | Out-Null
    }
    $dayBucket = (Get-Date).ToString('yyyy-MM-dd')
    $key = "$Ecosystem-$Size-$dayBucket"
    return Join-Path $cacheDir "$key.json"
}

function Get-CachedBaseline {
    if ($NoCache) { return $null }
    $path = Get-CachePath
    if (-not (Test-Path $path)) { return $null }
    $fileAge = (Get-Date) - (Get-Item $path).LastWriteTime
    if ($fileAge.TotalHours -gt $CacheHours) { return $null }
    try {
        $raw = Get-Content -Path $path -Raw
        return ($raw | ConvertFrom-Json)
    } catch {
        return $null
    }
}

function Set-CachedBaseline {
    param($Data)
    $path = Get-CachePath
    try {
        $Data | ConvertTo-Json -Depth 6 | Set-Content -Path $path -Force
    } catch {
        # Cache write failure is non-fatal
    }
}

# ─── npm Baseline Fetch ─────────────────────────────────────────────────

function Get-NpmPopularBaseline {
    $cached = Get-CachedBaseline
    if ($cached) { return $cached }

    # Fetch popular packages via npm search API sorted by popularity
    $url = "https://registry.npmjs.org/-/v1/search?text=boost-exact:false&size=$Size&popularity=1.0"
    $searchResult = Invoke-Api $url
    if (-not $searchResult -or -not $searchResult.objects) {
        # Return empty baseline on API failure
        return @()
    }

    $baseline = @()
    foreach ($obj in $searchResult.objects) {
        $pkg = $obj.package
        $downloads = 0
        if ($obj.score -and $obj.score.detail -and $obj.score.detail.popularity) {
            # Popularity is a 0-1 score; we'll fetch actual downloads for close matches
            $downloads = [math]::Floor($obj.score.detail.popularity * 10000000)
        }
        $baseline += @{
            name      = $pkg.name
            downloads = $downloads
        }
    }

    # Sort by downloads descending (approximation from popularity score)
    $baseline = @($baseline | Sort-Object { $_.downloads } -Descending)

    Set-CachedBaseline $baseline
    return $baseline
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

# ─── Core Analysis ──────────────────────────────────────────────────────

function Invoke-TyposquatAnalysis {
    $normalizedName = Get-ComparisonToken $Name

    # Fetch baseline
    $baseline = Get-NpmPopularBaseline
    if (-not $baseline -or $baseline.Count -eq 0) {
        # API failure fallback: still check CompareTo if provided
        $baseline = @()
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

    if ($bestCompare) {
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

    # Package existence check: if queried name does not resolve on npm, note it
    $queriedExists = $null -ne (Get-NpmWeeklyDownloads $Name)

    # Build human-readable summary
    $details = if ($riskReasons.Count -gt 0) {
        "Risk factors: $($riskReasons -join '; '). "
    } else {
        "No close matches found in top-$Size popular packages. "
    }
    if (-not $queriedExists) {
        $details += "Note: '$Name' does not appear to exist on npm (0 download data). "
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
