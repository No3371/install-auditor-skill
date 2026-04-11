<#
.SYNOPSIS
  Scans direct (Tier 2) or full transitive (Tier 3, npm only) dependencies for known
  CVEs via the OSV batch API. Never installs the audited package.

.PARAMETER Ecosystem
  Registry ecosystem. Supported: npm, pypi, crates, rubygems, nuget, go, maven, hex.

.PARAMETER Name
  Target package name (required).

.PARAMETER Version
  Target package version (optional). Selects the correct version manifest when fetching deps.

.PARAMETER Tier
  2 (default) — scan direct deps from registry metadata.
  3 — resolve full dep tree (npm: package-lock-only in temp dir); falls back to Tier 2
      if npm CLI unavailable or lock generation fails.

.OUTPUTS
  JSON to stdout:
  {
    ecosystem, package, version?,
    tier, directDepCount,
    transitiveDepCount?,        # present for successful Tier 3 only
    findings: [                 # HIGH and CRITICAL only
      { name, ecosystem, version, severity, cveIds[], depth }
      # depth: 1 = direct dep; 2+ = transitive (Tier 3 only; always 1 for Tier 2)
    ],
    mediumCount, lowCount,
    riskLevel,                  # "none"|"low"|"medium"|"high"|"critical"
    fallback,                   # true if Tier 3 fell back to Tier 2
    fallbackReason?,
    sources: ["OSV"],
    cacheHit,
    limitationNote?             # present when ecosystem dep resolution is unsupported
  }
  Cache: scripts/.dep-scan-cache/<eco>-<name>[-<ver>]-t<tier>.json, TTL 24 hr.
#>
param(
    [Parameter(Mandatory)]
    [ValidateSet('npm','pypi','crates','rubygems','nuget','go','maven','hex')]
    [string]$Ecosystem,

    [Parameter(Mandatory)]
    [string]$Name,

    [string]$Version,

    [ValidateSet(2, 3)]
    [int]$Tier = 2
)

$OsvEcoMap = @{ npm='npm'; pypi='PyPI'; crates='crates.io'; rubygems='RubyGems';
                nuget='NuGet'; go='Go'; maven='Maven'; hex='Hex' }

# ─── Cache ────────────────────────────────────────────────────────────────────

function Get-CachePath($Key) {
    $cacheDir = Join-Path $PSScriptRoot '.dep-scan-cache'
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
    } catch {}
}

# ─── Severity helpers ─────────────────────────────────────────────────────────

function Get-SeverityFromOsv($Vuln) {
    if ($Vuln.database_specific -and $Vuln.database_specific.severity) {
        return Normalize-Severity $Vuln.database_specific.severity
    }
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

function Get-RiskLevel($Severities) {
    $order   = @{ none = 0; low = 1; medium = 2; high = 3; critical = 4 }
    $highest = 'none'
    foreach ($s in $Severities) {
        if ($s -and $order.ContainsKey($s) -and $order[$s] -gt $order[$highest]) {
            $highest = $s
        }
    }
    return $highest
}

# ─── Registry dep fetchers ────────────────────────────────────────────────────

function Get-NpmDeps($PkgName, $PkgVersion) {
    # npm registry accepts the literal package name (including @ and / for scoped packages)
    $ver = if ($PkgVersion) { $PkgVersion } else { 'latest' }
    $uri = "https://registry.npmjs.org/$PkgName/$ver"
    $resp = Invoke-RestMethod -Uri $uri -TimeoutSec 20 `
        -Headers @{ 'User-Agent' = 'install-auditor/1.0' }
    $deps = @()
    if ($resp.dependencies) {
        foreach ($key in $resp.dependencies.PSObject.Properties.Name) {
            $deps += [ordered]@{ Name = $key; VersionRange = $resp.dependencies.$key }
        }
    }
    return $deps
}

function Get-PypiDeps($PkgName, $PkgVersion) {
    $seg = if ($PkgVersion) { "$PkgVersion/" } else { '' }
    $uri = "https://pypi.org/pypi/$PkgName/${seg}json"
    $resp = Invoke-RestMethod -Uri $uri -TimeoutSec 20 `
        -Headers @{ 'User-Agent' = 'install-auditor/1.0' }
    $deps = @()
    $requires = $resp.info.requires_dist
    if (-not $requires) { return $deps }
    foreach ($req in $requires) {
        $r       = $req -replace '\[[^\]]*\]', ''    # strip extras: pkg[extra] → pkg
        $r       = ($r -split ';')[0].Trim()          # strip env markers: req ; marker
        $depName = ($r -split '[>=<!~\s]')[0].Trim()  # strip version specifiers
        if ($depName) {
            $deps += [ordered]@{ Name = $depName; VersionRange = $null }
        }
    }
    return $deps
}

# ─── Tier 3: npm full-tree resolution ────────────────────────────────────────

function Get-NpmFullTree($PkgName, $PkgVersion) {
    # Returns array of { Name, Version } for all packages in the full dep tree.
    # Throws a descriptive string on failure for the caller to set as fallbackReason.

    $npmCmd = Get-Command npm -ErrorAction SilentlyContinue
    if (-not $npmCmd) { throw 'npm CLI unavailable' }

    try {
        $npmVer = (& npm --version 2>&1).Trim()
        $major  = [int]($npmVer -split '\.')[0]
        if ($major -lt 6) { throw "npm $npmVer is below minimum required version 6" }
    } catch {
        throw "npm version check failed: $($_.Exception.Message)"
    }

    $tempDir = Join-Path ([System.IO.Path]::GetTempPath()) ([System.Guid]::NewGuid().ToString())
    try {
        New-Item -ItemType Directory -Path $tempDir -Force | Out-Null

        # Write minimal package.json for the target package
        $pkgVer  = if ($PkgVersion) { $PkgVersion } else { '*' }
        $pkgJson = @{ dependencies = @{ $PkgName = $pkgVer } } | ConvertTo-Json -Depth 3
        Set-Content -Path (Join-Path $tempDir 'package.json') -Value $pkgJson -Encoding UTF8

        # Resolve full tree to package-lock.json without touching node_modules
        Push-Location $tempDir
        try {
            $null = & npm install --package-lock-only --ignore-scripts --silent 2>&1
            if ($LASTEXITCODE -ne 0) {
                throw "npm install --package-lock-only failed (exit $LASTEXITCODE)"
            }
        } finally {
            Pop-Location
        }

        $lockPath = Join-Path $tempDir 'package-lock.json'
        if (-not (Test-Path $lockPath)) { throw 'package-lock.json was not generated' }

        # -AsHashTable is required: ConvertFrom-Json rejects empty-string property names
        # (the lockfile root entry "": {...}) without it.
        $lock     = Get-Content $lockPath -Raw | ConvertFrom-Json -AsHashTable
        $packages = @()

        if ($lock.packages) {
            # Lockfile v2/v3: packages map with keys like "node_modules/foo"
            # or "node_modules/@scope/name" or "node_modules/a/node_modules/b"
            foreach ($entry in $lock.packages.GetEnumerator()) {
                $key = $entry.Key
                if ($key -eq '') { continue }   # root entry
                # Extract just the package name: strip up to and including last "node_modules/"
                $depName = $key -replace '^(.*node_modules/)', ''
                $depVer  = $entry.Value.version
                if ($depName -and $depVer) {
                    $packages += [ordered]@{ Name = $depName; Version = $depVer }
                }
            }
        } elseif ($lock.dependencies) {
            # Lockfile v1 fallback: flat dependency map
            foreach ($entry in $lock.dependencies.GetEnumerator()) {
                if ($entry.Value.version) {
                    $packages += [ordered]@{ Name = $entry.Key; Version = $entry.Value.version }
                }
            }
        }

        return $packages
    } finally {
        Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue
    }
}

# ─── OSV batch query ──────────────────────────────────────────────────────────

function Invoke-OsvBatch($Queries) {
    # $Queries: array of { Name, Ecosystem, Version? }
    # Returns an array parallel to $Queries; each element is the OSV result object.
    if (-not $Queries -or $Queries.Count -eq 0) { return @() }

    $allResults = [System.Collections.Generic.List[object]]::new()
    $batchSize  = 1000

    for ($i = 0; $i -lt $Queries.Count; $i += $batchSize) {
        $end   = [Math]::Min($i + $batchSize - 1, $Queries.Count - 1)
        $batch = @($Queries[$i..$end])

        $queryObjs = @($batch | ForEach-Object {
            $q = [ordered]@{ package = [ordered]@{ ecosystem = $_.Ecosystem; name = $_.Name } }
            if ($_.Version) { $q['version'] = $_.Version }
            $q
        })

        $body = ([ordered]@{ queries = $queryObjs }) | ConvertTo-Json -Depth 6 -Compress
        $resp = Invoke-RestMethod -Uri 'https://api.osv.dev/v1/querybatch' `
            -Method POST -ContentType 'application/json' -Body $body `
            -Headers @{ 'User-Agent' = 'install-auditor/1.0' } -TimeoutSec 30

        $rawResults = if ($resp.results) {
            @($resp.results)
        } else {
            # Maintain parallel alignment on unexpected empty response
            @($batch | ForEach-Object { [PSCustomObject]@{ vulns = @() } })
        }

        # OSV querybatch returns stub objects {id, modified} only — not full vuln records.
        # Enrich any stub by fetching full details from /v1/vulns/{id}.
        $enrichCache = @{}
        $enrichedBatch = @($rawResults | ForEach-Object {
            $result   = $_
            $rawVulns = if ($result.vulns) { @($result.vulns) } else { @() }
            $fullVulns = @($rawVulns | ForEach-Object {
                $v      = $_
                $isStub = $v.id -and (-not $v.database_specific) -and (-not $v.severity) -and (-not $v.aliases)
                if ($isStub) {
                    if (-not $enrichCache.ContainsKey($v.id)) {
                        try {
                            $enrichCache[$v.id] = Invoke-RestMethod `
                                -Uri "https://api.osv.dev/v1/vulns/$($v.id)" `
                                -TimeoutSec 15 -Headers @{ 'User-Agent' = 'install-auditor/1.0' }
                        } catch {
                            $enrichCache[$v.id] = $v  # keep stub on error; severity defaults to 'medium'
                        }
                    }
                    $enrichCache[$v.id]
                } else {
                    $v  # already a full record
                }
            })
            [PSCustomObject]@{ vulns = $fullVulns }
        })

        foreach ($r in $enrichedBatch) { $allResults.Add($r) }
    }

    return @($allResults)
}

# ─── Process OSV results into findings ───────────────────────────────────────

function Get-DepFindings($Deps, $OsvResults) {
    # Returns @{ Findings; MediumCount; LowCount; AllSeverities }
    $findings      = [System.Collections.Generic.List[object]]::new()
    $mediumCount   = 0
    $lowCount      = 0
    $allSeverities = [System.Collections.Generic.List[string]]::new()

    for ($i = 0; $i -lt $Deps.Count; $i++) {
        $dep    = $Deps[$i]
        $result = if ($i -lt $OsvResults.Count) { $OsvResults[$i] } else { $null }
        $vulns  = if ($result -and $result.vulns) { @($result.vulns) } else { @() }
        if ($vulns.Count -eq 0) { continue }

        $depSevs  = @($vulns | ForEach-Object { Get-SeverityFromOsv $_ })
        $cveIds   = @($vulns | ForEach-Object {
            if ($_.aliases) { @($_.aliases) | Where-Object { $_ -match '^CVE-' } }
        } | Sort-Object -Unique)
        $depWorst = Get-RiskLevel $depSevs
        $allSeverities.Add($depWorst)

        if ($depWorst -in @('high', 'critical')) {
            $version = if ($dep.Version)      { $dep.Version }
                       elseif ($dep.VersionRange) { $dep.VersionRange }
                       else                   { $null }
            $findings.Add([ordered]@{
                name      = $dep.Name
                ecosystem = $Ecosystem
                version   = $version
                severity  = $depWorst
                cveIds    = $cveIds
                depth     = $dep.Depth
            })
        } elseif ($depWorst -eq 'medium') {
            $mediumCount++
        } elseif ($depWorst -eq 'low') {
            $lowCount++
        }
    }

    return @{
        Findings      = @($findings)
        MediumCount   = $mediumCount
        LowCount      = $lowCount
        AllSeverities = @($allSeverities)
    }
}

# ─── Main ─────────────────────────────────────────────────────────────────────

$cacheKey = "$Ecosystem-$Name$(if ($Version) { "-$Version" })-t$Tier"
$cached   = Get-CachedResult $cacheKey
if ($cached) {
    $cached | Add-Member -NotePropertyName cacheHit -NotePropertyValue $true -Force
    $cached | ConvertTo-Json -Depth 8
    exit 0
}

$fallback           = $false
$fallbackReason     = $null
$limitationNote     = $null
$transitiveDepCount = $null

try {
    # ── Fetch direct deps from registry metadata ───────────────────────────────
    # @() wrapper is required: a 1-dep return gets pipeline-unrolled to the single
    # hashtable; iterating a hashtable enumerates DictionaryEntry key-value pairs
    # ("Name", "VersionRange") instead of dep objects — corrupting OSV queries.
    $directDeps = @(switch ($Ecosystem) {
        'npm'   { Get-NpmDeps  $Name $Version }
        'pypi'  { Get-PypiDeps $Name $Version }
        default {
            $limitationNote = "Direct dep resolution is not supported for ecosystem '$Ecosystem'. Supported: npm, pypi."
        }
    })
    $directDepCount = $directDeps.Count

    # ── Tier 3: attempt full-tree resolution (npm only) ────────────────────────
    $allDeps = $null
    if ($Tier -eq 3) {
        if ($Ecosystem -ne 'npm') {
            $fallback       = $true
            $fallbackReason = "Tier 3 full-tree resolution is only supported for npm; falling back to Tier 2 direct-dep scan."
        } else {
            try {
                $treePackages       = Get-NpmFullTree $Name $Version
                $transitiveDepCount = $treePackages.Count
                $directNames        = @{}
                foreach ($d in $directDeps) { $directNames[$d.Name] = $true }
                $allDeps = @($treePackages | ForEach-Object {
                    [ordered]@{
                        Name         = $_.Name
                        Version      = $_.Version
                        VersionRange = $null
                        Depth        = if ($directNames.ContainsKey($_.Name)) { 1 } else { 2 }
                    }
                })
            } catch {
                $fallback       = $true
                $fallbackReason = $_.Exception.Message
            }
        }
    }

    # ── Use direct deps for Tier 2 or after Tier 3 fallback ───────────────────
    if ($null -eq $allDeps) {
        $allDeps = @($directDeps | ForEach-Object {
            [ordered]@{
                Name         = $_.Name
                Version      = $null
                VersionRange = $_.VersionRange
                Depth        = 1
            }
        })
    }

    # ── Build and execute OSV batch queries ───────────────────────────────────
    $osvEco  = $OsvEcoMap[$Ecosystem]
    $queries = @($allDeps | ForEach-Object {
        [ordered]@{ Name = $_.Name; Ecosystem = $osvEco; Version = $_.Version }
    })

    $osvResults = if ($queries.Count -gt 0) { Invoke-OsvBatch $queries } else { @() }

    # ── Process into findings ──────────────────────────────────────────────────
    $processed = Get-DepFindings $allDeps $osvResults
    $riskLevel = Get-RiskLevel $processed.AllSeverities

    # ── Assemble output ────────────────────────────────────────────────────────
    $effectiveTier = if ($fallback -and $Tier -eq 3) { 2 } else { $Tier }
    $output = [ordered]@{
        ecosystem      = $Ecosystem
        package        = $Name
        tier           = $effectiveTier
        directDepCount = $directDepCount
        findings       = $processed.Findings
        mediumCount    = $processed.MediumCount
        lowCount       = $processed.LowCount
        riskLevel      = $riskLevel
        fallback       = $fallback
        sources        = @('OSV')
        cacheHit       = $false
    }
    if ($Version)                      { $output['version']            = $Version }
    if ($null -ne $transitiveDepCount) { $output['transitiveDepCount'] = $transitiveDepCount }
    if ($fallbackReason)               { $output['fallbackReason']     = $fallbackReason }
    if ($limitationNote)               { $output['limitationNote']     = $limitationNote }

    Set-CachedResult $cacheKey $output
    $output | ConvertTo-Json -Depth 8

} catch {
    [ordered]@{
        ecosystem = $Ecosystem
        package   = $Name
        tier      = $Tier
        error     = $_.Exception.Message
        riskLevel = 'unknown'
        fallback  = $false
        cacheHit  = $false
    } | ConvertTo-Json -Depth 3
}
