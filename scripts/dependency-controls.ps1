[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("inventory", "license", "audit")]
    [string]$Mode,

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$RemainingArguments
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if ($null -ne $RemainingArguments -and $RemainingArguments.Count -gt 0) {
    throw "dependency-controls.ps1 accepts only one explicit mode."
}

$repoRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$pythonDirectory = Join-Path $repoRoot "python"
$nodeLicenseTool = Join-Path $repoRoot "node_modules\\.bin\\license-checker-rseidelsohn.cmd"

function Get-RelativeDiagnosticPath {
    param([AllowNull()][string]$Path)

    if ([string]::IsNullOrWhiteSpace($Path)) {
        return "(not reported)"
    }

    try {
        $resolved = [System.IO.Path]::GetFullPath($Path)
        if ($resolved.StartsWith($repoRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
            return [System.IO.Path]::GetRelativePath($repoRoot, $resolved)
        }
    } catch {
        return "(unavailable)"
    }

    return "(outside checkout)"
}

function Assert-BoundedAuditDirectory {
    param(
        [Parameter(Mandatory = $true)][string]$AuditDirectory,
        [Parameter(Mandatory = $true)][string]$ExpectedParent,
        [Parameter(Mandatory = $true)][string]$ExpectedName
    )

    Assert-SafeAuditTemporaryRoot -TemporaryRoot $ExpectedParent
    $parent = [System.IO.Path]::GetFullPath($ExpectedParent)
    if (-not $parent.EndsWith([System.IO.Path]::DirectorySeparatorChar)) {
        $parent += [System.IO.Path]::DirectorySeparatorChar
    }
    $candidate = [System.IO.Path]::GetFullPath($AuditDirectory)

    if (-not $candidate.StartsWith($parent, [System.StringComparison]::OrdinalIgnoreCase) -or
        [System.IO.Path]::GetFileName($candidate) -ne $ExpectedName) {
        throw "Refusing an audit path outside the expected temporary-directory child."
    }
}

function Assert-SafeAuditTemporaryRoot {
    param(
        [Parameter(Mandatory = $true)][string]$TemporaryRoot
    )

    $root = [System.IO.Path]::GetFullPath($TemporaryRoot)
    if (-not (Test-Path -LiteralPath $root)) {
        throw "Refusing a missing temporary-directory root."
    }

    $item = Get-Item -LiteralPath $root -Force
    if (-not $item.PSIsContainer -or ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint)) {
        throw "Refusing a non-directory or reparse-point temporary-directory root."
    }

    $rootWithSeparator = $root
    if (-not $rootWithSeparator.EndsWith([System.IO.Path]::DirectorySeparatorChar)) {
        $rootWithSeparator += [System.IO.Path]::DirectorySeparatorChar
    }
    $protectedRoots = [System.Collections.Generic.List[string]]::new()
    $protectedRoots.Add([System.IO.Path]::GetFullPath($repoRoot))
    foreach ($oneDriveVariable in @("OneDrive", "OneDriveConsumer", "OneDriveCommercial")) {
        $oneDrivePath = [Environment]::GetEnvironmentVariable($oneDriveVariable)
        if (-not [string]::IsNullOrWhiteSpace($oneDrivePath)) {
            $protectedRoots.Add([System.IO.Path]::GetFullPath($oneDrivePath))
        }
    }

    foreach ($protectedRoot in $protectedRoots | Sort-Object -Unique) {
        $protectedWithSeparator = $protectedRoot
        if (-not $protectedWithSeparator.EndsWith([System.IO.Path]::DirectorySeparatorChar)) {
            $protectedWithSeparator += [System.IO.Path]::DirectorySeparatorChar
        }
        if ($root.Equals($protectedRoot, [System.StringComparison]::OrdinalIgnoreCase) -or
            $rootWithSeparator.StartsWith($protectedWithSeparator, [System.StringComparison]::OrdinalIgnoreCase)) {
            throw "Refusing a temporary-directory root inside the checkout or OneDrive."
        }
    }
}

function Assert-SafeAuditCleanupTarget {
    param(
        [Parameter(Mandatory = $true)][string]$AuditDirectory,
        [Parameter(Mandatory = $true)][string]$ExpectedParent,
        [Parameter(Mandatory = $true)][string]$ExpectedName
    )

    Assert-BoundedAuditDirectory -AuditDirectory $AuditDirectory -ExpectedParent $ExpectedParent -ExpectedName $ExpectedName
    if (-not (Test-Path -LiteralPath $AuditDirectory)) {
        return $false
    }

    $item = Get-Item -LiteralPath $AuditDirectory -Force
    if (-not $item.PSIsContainer -or ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint)) {
        throw "Refusing to recursively delete a non-directory or reparse point."
    }

    return $true
}

function Get-LicenseDisposition {
    param([AllowNull()][string]$License)

    $value = if ($null -eq $License) { "" } else { $License.Trim() }
    if ([string]::IsNullOrWhiteSpace($value) -or $value -match "unknown|none|unlicensed|custom|\*|see license") {
        return "prohibited"
    }

    $allowed = @(
        "MIT", "BSD-2-Clause", "BSD-3-Clause", "ISC", "Apache-2.0", "0BSD",
        "Zlib", "PSF-2.0", "CC0-1.0", "MIT-0"
    )
    if ($allowed -contains $value) {
        return "allowed"
    }

    if ($value -match "MPL|Mozilla Public License|EPL|Eclipse Public License|LGPL|Lesser General Public|CDDL|Artistic|Unicode|dual|multi|;|\||/|data|generated|native|binary|notice") {
        return "review-required"
    }

    if ($value -match "AGPL|Affero|SSPL|Server Side Public|Commons Clause|Business Source|BUSL|non-commercial|no derivatives|GPL|GNU General Public") {
        return "prohibited"
    }

    return "prohibited"
}

function Get-Decision0003CatalogEntry {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][string]$Version,
        [AllowNull()][string]$License
    )

    # This is deliberately a literal three-part catalog. Do not generalize these
    # entries: Decision Record 0003 permits no ranges, prefixes, wildcards, or
    # role inference.
    $entries = @{
        "@csstools/color-helpers|6.1.1|MIT-0" = @{
            Role = "test-only DOM/CSS-color emulation support"
            ReReview = "Re-review before distribution of the package or its data, or on any version, license, or role change."
        }
        "@csstools/css-syntax-patches-for-csstree|1.1.14|MIT-0" = @{
            Role = "test-only DOM CSS-parser compatibility data"
            ReReview = "Re-review before distribution of the package or its data, or on any version, license, or role change."
        }
        "colorama|0.4.6|BSD License" = @{
            Role = "development/test quality tooling"
            ReReview = "Re-review before distribution, or on any version, license, or role change."
        }
        "packaging|26.3|Apache-2.0 OR BSD-2-Clause" = @{
            Role = "development/test quality tooling"
            ReReview = "Re-review before distribution, or on any version, license, or role change."
        }
        "lightningcss|1.33.0|MPL-2.0" = @{
            Role = "Vite unchanged build-only CSS-processing capability; current project has no CSS processing or output"
            ReReview = "Re-review before CSS processing, a desktop or installer deliverable, packaged node modules, or distribution containing this code or native binary."
        }
        "lightningcss-win32-x64-msvc|1.33.0|MPL-2.0" = @{
            Role = "Vite unchanged build-only CSS-processing capability; current project has no CSS processing or output"
            ReReview = "Re-review before CSS processing, a desktop or installer deliverable, packaged node modules, or distribution containing this code or native binary."
        }
        "certifi|2026.7.22|MPL-2.0" = @{
            Role = "development/integration HTTP-advisory CA bundle only; no application import or output"
            ReReview = "Re-review if a Python environment, runtime, or certificate bundle is distributed."
        }
        "pathspec|1.1.1|Mozilla Public License 2.0 (MPL 2.0)" = @{
            Role = "development/test quality tooling"
            ReReview = "Re-review before distribution, or on any version, license, or role change."
        }
        "chownr|3.0.0|BlueOak-1.0.0" = @{
            Role = "development/test/quality/local dependency-control tooling"
            ReReview = "Re-review before code distribution; Central must record notice and link treatment."
        }
        "common-ancestor-path|2.0.0|BlueOak-1.0.0" = @{
            Role = "development/test/quality/local dependency-control tooling"
            ReReview = "Re-review before code distribution; Central must record notice and link treatment."
        }
        "glob|13.0.6|BlueOak-1.0.0" = @{
            Role = "development/test/quality/local dependency-control tooling"
            ReReview = "Re-review before code distribution; Central must record notice and link treatment."
        }
        "isexe|4.0.0|BlueOak-1.0.0" = @{
            Role = "development/test/quality/local dependency-control tooling"
            ReReview = "Re-review before code distribution; Central must record notice and link treatment."
        }
        "lru-cache|11.5.2|BlueOak-1.0.0" = @{
            Role = "development/test/quality/local dependency-control tooling"
            ReReview = "Re-review before code distribution; Central must record notice and link treatment."
        }
        "minimatch|10.2.6|BlueOak-1.0.0" = @{
            Role = "development/test/quality/local dependency-control tooling"
            ReReview = "Re-review before code distribution; Central must record notice and link treatment."
        }
        "minipass|7.1.3|BlueOak-1.0.0" = @{
            Role = "development/test/quality/local dependency-control tooling"
            ReReview = "Re-review before code distribution; Central must record notice and link treatment."
        }
        "minipass-flush|1.0.7|BlueOak-1.0.0" = @{
            Role = "development/test/quality/local dependency-control tooling"
            ReReview = "Re-review before code distribution; Central must record notice and link treatment."
        }
        "path-scurry|2.0.2|BlueOak-1.0.0" = @{
            Role = "development/test/quality/local dependency-control tooling"
            ReReview = "Re-review before code distribution; Central must record notice and link treatment."
        }
        "tar|7.5.22|BlueOak-1.0.0" = @{
            Role = "development/test/quality/local dependency-control tooling"
            ReReview = "Re-review before code distribution; Central must record notice and link treatment."
        }
        "yallist|5.0.0|BlueOak-1.0.0" = @{
            Role = "development/test/quality/local dependency-control tooling"
            ReReview = "Re-review before code distribution; Central must record notice and link treatment."
        }
        "caniuse-lite|1.0.30001810|CC-BY-4.0" = @{
            Role = "development-only browser-compatibility data"
            ReReview = "Re-review before distributing this data."
        }
        "spdx-exceptions|2.5.0|CC-BY-3.0" = @{
            Role = "local dependency-control tooling"
            ReReview = "Re-review attribution treatment before distributing this data."
        }
        "spdx-ranges|2.1.1|(MIT AND CC-BY-3.0)" = @{
            Role = "local dependency-control tooling"
            ReReview = "Re-review before distributing this data or code; retain both license components."
        }
    }

    $key = "$Name|$Version|$License"
    if (-not $entries.ContainsKey($key)) {
        return $null
    }

    return [pscustomobject]@{
        RecordId = "0003"
        Role = $entries[$key].Role
        ReReview = $entries[$key].ReReview
    }
}

function Get-LicensePolicyResult {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][string]$Version,
        [AllowNull()][string]$License
    )

    $catalogEntry = Get-Decision0003CatalogEntry -Name $Name -Version $Version -License $License
    if ($null -ne $catalogEntry) {
        return [pscustomobject]@{ Disposition = "allowed"; CatalogEntry = $catalogEntry }
    }

    return [pscustomobject]@{ Disposition = (Get-LicenseDisposition -License $License); CatalogEntry = $null }
}

function Get-LicenseDiagnosticValue {
    param([AllowNull()][string]$License)

    $compact = if ($null -eq $License) { "" } else { ($License -replace "\s+", " ").Trim() }
    if ($compact.Length -gt 120) {
        return $compact.Substring(0, 117) + "..."
    }
    return $compact
}

function Invoke-Inventory {
    $npmJson = & npm.cmd ls --all --json
    $npmExit = $LASTEXITCODE
    if ($npmExit -ne 0) {
        throw "npm inventory failed with exit code $npmExit. Run the locked setup task first."
    }
    $npmTree = $npmJson | ConvertFrom-Json
    $npmRows = [System.Collections.Generic.List[string]]::new()
    function Add-NpmInventoryRows {
        param($Dependencies, [string]$Relation)
        if ($null -eq $Dependencies) { return }
        foreach ($property in $Dependencies.PSObject.Properties | Sort-Object Name) {
            $name = $property.Name
            $entry = $property.Value
            $versionProperty = $entry.PSObject.Properties["version"]
            if ($null -ne $versionProperty -and -not [string]::IsNullOrWhiteSpace([string]$versionProperty.Value)) {
                $npmRows.Add("npm $Relation $name@$($versionProperty.Value)")
            }
            $childDependencies = $entry.PSObject.Properties["dependencies"]
            if ($null -ne $childDependencies) {
                Add-NpmInventoryRows -Dependencies $childDependencies.Value -Relation "transitive"
            }
        }
    }
    Add-NpmInventoryRows -Dependencies $npmTree.dependencies -Relation "direct"

    $pythonJson = & uv --directory $pythonDirectory run --locked python -c "import importlib.metadata as m, json; print(json.dumps(sorted((d.metadata['Name'], d.version) for d in m.distributions()), separators=(',', ':')))"
    $pythonExit = $LASTEXITCODE
    if ($pythonExit -ne 0) {
        throw "Python inventory failed with exit code $pythonExit. Run the locked setup task first."
    }
    $pythonRows = $pythonJson | ConvertFrom-Json

    Write-Output "Locked installed dependency inventory (review evidence; not an SBOM):"
    $npmRows | Sort-Object -Unique | Write-Output
    foreach ($row in $pythonRows) {
        Write-Output "python installed $($row[0])@$($row[1])"
    }
}

function Invoke-LicenseCheck {
    if (-not (Test-Path -LiteralPath $nodeLicenseTool)) {
        throw "The locked Node license tool is unavailable. Run the locked setup task first."
    }

    $failures = [System.Collections.Generic.List[string]]::new()
    $allowedCount = 0
    $projectPackage = Get-Content -Raw -LiteralPath (Join-Path $repoRoot "package.json") | ConvertFrom-Json
    $projectKey = "$($projectPackage.name)@$($projectPackage.version)"
    $nodeJson = & $nodeLicenseTool --json
    $nodeExit = $LASTEXITCODE
    if ($nodeExit -ne 0) {
        throw "Node license inventory failed with exit code $nodeExit."
    }
    $nodePackages = $nodeJson | ConvertFrom-Json
    foreach ($property in $nodePackages.PSObject.Properties | Sort-Object Name) {
        if ($property.Name -eq $projectKey) {
            continue
        }
        $package = $property.Value
        $licenseProperty = $package.PSObject.Properties["licenses"]
        $license = if ($null -eq $licenseProperty) { "" } else { [string]$licenseProperty.Value }
        $separator = $property.Name.LastIndexOf("@")
        if ($separator -le 0) {
            throw "Node license inventory reported an unparseable package key."
        }
        $name = $property.Name.Substring(0, $separator)
        $version = $property.Name.Substring($separator + 1)
        $policyResult = Get-LicensePolicyResult -Name $name -Version $version -License $license
        $disposition = $policyResult.Disposition
        $displayLicense = Get-LicenseDiagnosticValue -License $license
        $pathProperty = $package.PSObject.Properties["path"]
        $path = if ($null -eq $pathProperty) { "(not reported)" } else { Get-RelativeDiagnosticPath -Path ([string]$pathProperty.Value) }
        if ($disposition -eq "allowed") {
            $allowedCount++
            if ($null -ne $policyResult.CatalogEntry) {
                Write-Output "npm allowed $($property.Name) license=$displayLicense record=$($policyResult.CatalogEntry.RecordId) role=$($policyResult.CatalogEntry.Role) re-review=$($policyResult.CatalogEntry.ReReview)"
            }
        } else {
            Write-Output "npm $disposition $($property.Name) license=$displayLicense path=$path"
            $failures.Add("npm $disposition $($property.Name) license=$displayLicense path=$path")
        }
    }

    $pythonJson = & uv --directory $pythonDirectory run --locked pip-licenses --from=all --format=json
    $pythonExit = $LASTEXITCODE
    if ($pythonExit -ne 0) {
        throw "Python license inventory failed with exit code $pythonExit."
    }
    $pythonPackages = $pythonJson | ConvertFrom-Json
    foreach ($package in $pythonPackages | Sort-Object Name) {
        $expression = $package.PSObject.Properties["License-Expression"]
        $metadata = $package.PSObject.Properties["License-Metadata"]
        $classifier = $package.PSObject.Properties["License-Classifier"]
        $license = ""
        # pip-licenses exposes fields in decreasing declaration authority. Never
        # search later fields for an allowed value: a generic or conflicting
        # higher-priority claim must remain an unapproved finding.
        foreach ($candidate in @($expression, $metadata, $classifier)) {
            if ($null -ne $candidate -and -not [string]::IsNullOrWhiteSpace([string]$candidate.Value) -and [string]$candidate.Value -ne "UNKNOWN") {
                $license = [string]$candidate.Value
                break
            }
        }
        $name = [string]$package.PSObject.Properties["Name"].Value
        $version = [string]$package.PSObject.Properties["Version"].Value
        $policyResult = Get-LicensePolicyResult -Name $name -Version $version -License $license
        $disposition = $policyResult.Disposition
        $displayLicense = Get-LicenseDiagnosticValue -License $license
        if ($disposition -eq "allowed") {
            $allowedCount++
            if ($null -ne $policyResult.CatalogEntry) {
                Write-Output "python allowed $name@$version license=$displayLicense record=$($policyResult.CatalogEntry.RecordId) role=$($policyResult.CatalogEntry.Role) re-review=$($policyResult.CatalogEntry.ReReview)"
            }
        } else {
            Write-Output "python $disposition $name@$version license=$displayLicense source=installed-metadata"
            $failures.Add("python $disposition $name@$version license=$displayLicense source=installed-metadata")
        }
    }

    if ($failures.Count -gt 0) {
        Write-Error "License policy failed closed. Review-required, prohibited, unknown, ambiguous, custom, generated, native, or material-notice findings require Central action; automated classification is not legal advice."
        $failures | ForEach-Object { Write-Error $_ }
        exit 1
    }

    Write-Output "License policy passed for $allowedCount installed locked packages. Automated classification is review evidence, not legal advice."
}

function Invoke-DependencyAudit {
    $isCi = $env:GITHUB_ACTIONS -eq "true"
    if ($isCi) {
        if ([string]::IsNullOrWhiteSpace($env:RUNNER_TEMP)) {
            throw "RUNNER_TEMP is required for CI audit output."
        }
        $tempRoot = [System.IO.Path]::GetFullPath($env:RUNNER_TEMP)
        $auditName = "vidap-pip-audit"
        $auditDirectory = Join-Path $tempRoot $auditName
    } elseif ($env:VIDAP_AUDIT_DIR) {
        $tempRoot = [System.IO.Path]::GetFullPath([System.IO.Path]::GetTempPath())
        $auditDirectory = [System.IO.Path]::GetFullPath($env:VIDAP_AUDIT_DIR)
        $auditName = [System.IO.Path]::GetFileName($auditDirectory)
        if ($auditName -notmatch "^vidap-pip-audit-[0-9a-f]{32}$") {
            throw "VIDAP_AUDIT_DIR must use the exact new vidap-pip-audit-<32 lowercase hex> name."
        }
    } else {
        $tempRoot = [System.IO.Path]::GetFullPath([System.IO.Path]::GetTempPath())
        $auditName = "vidap-pip-audit-" + [guid]::NewGuid().ToString("N")
        $auditDirectory = Join-Path $tempRoot $auditName
    }

    Assert-BoundedAuditDirectory -AuditDirectory $auditDirectory -ExpectedParent $tempRoot -ExpectedName $auditName
    if (Test-Path -LiteralPath $auditDirectory) {
        throw "Refusing to reuse a pre-existing audit directory."
    }

    New-Item -ItemType Directory -Path $auditDirectory -ErrorAction Stop | Out-Null
    $createdAuditDirectory = $true
    $requirements = Join-Path $auditDirectory "uv-lock.requirements.txt"
    $httpCache = Join-Path $auditDirectory "http-cache"
    $pythonReport = Join-Path $auditDirectory "pip-audit.json"
    $npmExit = 1
    $pythonExit = 1

    try {
        $npmOutput = & npm.cmd audit --json 2>&1
        $npmExit = $LASTEXITCODE
        $npmOutput | Write-Output

        & uv --directory $pythonDirectory export --locked --no-cache --all-extras --all-groups --no-emit-project --format requirements.txt --output-file $requirements | Out-Null
        $exportExit = $LASTEXITCODE
        if ($exportExit -ne 0) {
            throw "Lock-faithful Python requirements export failed with exit code $exportExit."
        }

        & uv --directory $pythonDirectory run --locked --no-sync -- pip-audit --requirement $requirements --require-hashes --disable-pip --strict --cache-dir $httpCache --format json --output $pythonReport
        $pythonExit = $LASTEXITCODE
        if (Test-Path -LiteralPath $pythonReport) {
            Write-Output "Python advisory JSON was produced at the bounded temporary location."
        }
    } finally {
        if (-not $isCi -and $createdAuditDirectory) {
            if (Assert-SafeAuditCleanupTarget -AuditDirectory $auditDirectory -ExpectedParent $tempRoot -ExpectedName $auditName) {
                Remove-Item -LiteralPath $auditDirectory -Recurse -Force -ErrorAction Stop
            }
        }
    }

    if ($npmExit -ne 0 -or $pythonExit -ne 0) {
        Write-Error "Dependency advisory policy reported a nonzero scanner result; no fix, resolution, or lock rewrite was attempted."
        exit 1
    }

    Write-Output "Dependency advisory scans completed without findings. Scanner results are evidence, not a safety guarantee."
}

switch ($Mode) {
    "inventory" { Invoke-Inventory }
    "license" { Invoke-LicenseCheck }
    "audit" { Invoke-DependencyAudit }
    default { throw "Unsupported dependency-control mode." }
}
