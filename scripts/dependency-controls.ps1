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

function Get-Decision0004CatalogEntry {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][string]$Version,
        [AllowNull()][string]$License
    )

    # Decision Record 0004 permits only these seven literal scanner values.
    # The pip_api metadata is represented losslessly to preserve its full
    # reviewed value, including whitespace; no installed license file is read
    # or parsed to classify a future package.
    $pipApiGateValue = [System.Text.Encoding]::UTF8.GetString(
        [System.Convert]::FromBase64String("QXBhY2hlIExpY2Vuc2UKICAgICAgICAgICAgICAgICAgICAgICAgVmVyc2lvbiAyLjAsIEphbnVhcnkgMjAwNAogICAgICAgICAgICAgICAgICAgICBodHRwczovL3d3dy5hcGFjaGUub3JnL2xpY2Vuc2VzLwoKVEVSTVMgQU5EIENPTkRJVElPTlMgRk9SIFVTRSwgUkVQUk9EVUNUSU9OLCBBTkQgRElTVFJJQlVUSU9OCgoxLiBEZWZpbml0aW9ucy4KCiAgICJMaWNlbnNlIiBzaGFsbCBtZWFuIHRoZSB0ZXJtcyBhbmQgY29uZGl0aW9ucyBmb3IgdXNlLCByZXByb2R1Y3Rpb24sCiAgIGFuZCBkaXN0cmlidXRpb24gYXMgZGVmaW5lZCBieSBTZWN0aW9ucyAxIHRocm91Z2ggOSBvZiB0aGlzIGRvY3VtZW50LgoKICAgIkxpY2Vuc29yIiBzaGFsbCBtZWFuIHRoZSBjb3B5cmlnaHQgb3duZXIgb3IgZW50aXR5IGF1dGhvcml6ZWQgYnkKICAgdGhlIGNvcHlyaWdodCBvd25lciB0aGF0IGlzIGdyYW50aW5nIHRoZSBMaWNlbnNlLgoKICAgIkxlZ2FsIEVudGl0eSIgc2hhbGwgbWVhbiB0aGUgdW5pb24gb2YgdGhlIGFjdGluZyBlbnRpdHkgYW5kIGFsbAogICBvdGhlciBlbnRpdGllcyB0aGF0IGNvbnRyb2wsIGFyZSBjb250cm9sbGVkIGJ5LCBvciBhcmUgdW5kZXIgY29tbW9uCiAgIGNvbnRyb2wgd2l0aCB0aGF0IGVudGl0eS4gRm9yIHRoZSBwdXJwb3NlcyBvZiB0aGlzIGRlZmluaXRpb24sCiAgICJjb250cm9sIiBtZWFucyAoaSkgdGhlIHBvd2VyLCBkaXJlY3Qgb3IgaW5kaXJlY3QsIHRvIGNhdXNlIHRoZQogICBkaXJlY3Rpb24gb3IgbWFuYWdlbWVudCBvZiBzdWNoIGVudGl0eSwgd2hldGhlciBieSBjb250cmFjdCBvcgogICBvdGhlcndpc2UsIG9yIChpaSkgb3duZXJzaGlwIG9mIGZpZnR5IHBlcmNlbnQgKDUwJSkgb3IgbW9yZSBvZiB0aGUKICAgb3V0c3RhbmRpbmcgc2hhcmVzLCBvciAoaWlpKSBiZW5lZmljaWFsIG93bmVyc2hpcCBvZiBzdWNoIGVudGl0eS4KCiAgICJZb3UiIChvciAiWW91ciIpIHNoYWxsIG1lYW4gYW4gaW5kaXZpZHVhbCBvciBMZWdhbCBFbnRpdHkKICAgZXhlcmNpc2luZyBwZXJtaXNzaW9ucyBncmFudGVkIGJ5IHRoaXMgTGljZW5zZS4KCiAgICJTb3VyY2UiIGZvcm0gc2hhbGwgbWVhbiB0aGUgcHJlZmVycmVkIGZvcm0gZm9yIG1ha2luZyBtb2RpZmljYXRpb25zLAogICBpbmNsdWRpbmcgYnV0IG5vdCBsaW1pdGVkIHRvIHNvZnR3YXJlIHNvdXJjZSBjb2RlLCBkb2N1bWVudGF0aW9uCiAgIHNvdXJjZSwgYW5kIGNvbmZpZ3VyYXRpb24gZmlsZXMuCgogICAiT2JqZWN0IiBmb3JtIHNoYWxsIG1lYW4gYW55IGZvcm0gcmVzdWx0aW5nIGZyb20gbWVjaGFuaWNhbAogICB0cmFuc2Zvcm1hdGlvbiBvciB0cmFuc2xhdGlvbiBvZiBhIFNvdXJjZSBmb3JtLCBpbmNsdWRpbmcgYnV0CiAgIG5vdCBsaW1pdGVkIHRvIGNvbXBpbGVkIG9iamVjdCBjb2RlLCBnZW5lcmF0ZWQgZG9jdW1lbnRhdGlvbiwKICAgYW5kIGNvbnZlcnNpb25zIHRvIG90aGVyIG1lZGlhIHR5cGVzLgoKICAgIldvcmsiIHNoYWxsIG1lYW4gdGhlIHdvcmsgb2YgYXV0aG9yc2hpcCwgd2hldGhlciBpbiBTb3VyY2Ugb3IKICAgT2JqZWN0IGZvcm0sIG1hZGUgYXZhaWxhYmxlIHVuZGVyIHRoZSBMaWNlbnNlLCBhcyBpbmRpY2F0ZWQgYnkgYQogICBjb3B5cmlnaHQgbm90aWNlIHRoYXQgaXMgaW5jbHVkZWQgaW4gb3IgYXR0YWNoZWQgdG8gdGhlIHdvcmsKICAgKGFuIGV4YW1wbGUgaXMgcHJvdmlkZWQgaW4gdGhlIEFwcGVuZGl4IGJlbG93KS4KCiAgICJEZXJpdmF0aXZlIFdvcmtzIiBzaGFsbCBtZWFuIGFueSB3b3JrLCB3aGV0aGVyIGluIFNvdXJjZSBvciBPYmplY3QKICAgZm9ybSwgdGhhdCBpcyBiYXNlZCBvbiAob3IgZGVyaXZlZCBmcm9tKSB0aGUgV29yayBhbmQgZm9yIHdoaWNoIHRoZQogICBlZGl0b3JpYWwgcmV2aXNpb25zLCBhbm5vdGF0aW9ucywgZWxhYm9yYXRpb25zLCBvciBvdGhlciBtb2RpZmljYXRpb25zCiAgIHJlcHJlc2VudCwgYXMgYSB3aG9sZSwgYW4gb3JpZ2luYWwgd29yayBvZiBhdXRob3JzaGlwLiBGb3IgdGhlIHB1cnBvc2VzCiAgIG9mIHRoaXMgTGljZW5zZSwgRGVyaXZhdGl2ZSBXb3JrcyBzaGFsbCBub3QgaW5jbHVkZSB3b3JrcyB0aGF0IHJlbWFpbgogICBzZXBhcmFibGUgZnJvbSwgb3IgbWVyZWx5IGxpbmsgKG9yIGJpbmQgYnkgbmFtZSkgdG8gdGhlIGludGVyZmFjZXMgb2YsCiAgIHRoZSBXb3JrIGFuZCBEZXJpdmF0aXZlIFdvcmtzIHRoZXJlb2YuCgogICAiQ29udHJpYnV0aW9uIiBzaGFsbCBtZWFuIGFueSB3b3JrIG9mIGF1dGhvcnNoaXAsIGluY2x1ZGluZwogICB0aGUgb3JpZ2luYWwgdmVyc2lvbiBvZiB0aGUgV29yayBhbmQgYW55IG1vZGlmaWNhdGlvbnMgb3IgYWRkaXRpb25zCiAgIHRvIHRoYXQgV29yayBvciBEZXJpdmF0aXZlIFdvcmtzIHRoZXJlb2YsIHRoYXQgaXMgaW50ZW50aW9uYWxseQogICBzdWJtaXR0ZWQgdG8gTGljZW5zb3IgZm9yIGluY2x1c2lvbiBpbiB0aGUgV29yayBieSB0aGUgY29weXJpZ2h0IG93bmVyCiAgIG9yIGJ5IGFuIGluZGl2aWR1YWwgb3IgTGVnYWwgRW50aXR5IGF1dGhvcml6ZWQgdG8gc3VibWl0IG9uIGJlaGFsZiBvZgogICB0aGUgY29weXJpZ2h0IG93bmVyLiBGb3IgdGhlIHB1cnBvc2VzIG9mIHRoaXMgZGVmaW5pdGlvbiwgInN1Ym1pdHRlZCIKICAgbWVhbnMgYW55IGZvcm0gb2YgZWxlY3Ryb25pYywgdmVyYmFsLCBvciB3cml0dGVuIGNvbW11bmljYXRpb24gc2VudAogICB0byB0aGUgTGljZW5zb3Igb3IgaXRzIHJlcHJlc2VudGF0aXZlcywgaW5jbHVkaW5nIGJ1dCBub3QgbGltaXRlZCB0bwogICBjb21tdW5pY2F0aW9uIG9uIGVsZWN0cm9uaWMgbWFpbGluZyBsaXN0cywgc291cmNlIGNvZGUgY29udHJvbCBzeXN0ZW1zLAogICBhbmQgaXNzdWUgdHJhY2tpbmcgc3lzdGVtcyB0aGF0IGFyZSBtYW5hZ2VkIGJ5LCBvciBvbiBiZWhhbGYgb2YsIHRoZQogICBMaWNlbnNvciBmb3IgdGhlIHB1cnBvc2Ugb2YgZGlzY3Vzc2luZyBhbmQgaW1wcm92aW5nIHRoZSBXb3JrLCBidXQKICAgZXhjbHVkaW5nIGNvbW11bmljYXRpb24gdGhhdCBpcyBjb25zcGljdW91c2x5IG1hcmtlZCBvciBvdGhlcndpc2UKICAgZGVzaWduYXRlZCBpbiB3cml0aW5nIGJ5IHRoZSBjb3B5cmlnaHQgb3duZXIgYXMgIk5vdCBhIENvbnRyaWJ1dGlvbi4iCgogICAiQ29udHJpYnV0b3IiIHNoYWxsIG1lYW4gTGljZW5zb3IgYW5kIGFueSBpbmRpdmlkdWFsIG9yIExlZ2FsIEVudGl0eQogICBvbiBiZWhhbGYgb2Ygd2hvbSBhIENvbnRyaWJ1dGlvbiBoYXMgYmVlbiByZWNlaXZlZCBieSBMaWNlbnNvciBhbmQKICAgc3Vic2VxdWVudGx5IGluY29ycG9yYXRlZCB3aXRoaW4gdGhlIFdvcmsuCgoyLiBHcmFudCBvZiBDb3B5cmlnaHQgTGljZW5zZS4gU3ViamVjdCB0byB0aGUgdGVybXMgYW5kIGNvbmRpdGlvbnMgb2YKICAgdGhpcyBMaWNlbnNlLCBlYWNoIENvbnRyaWJ1dG9yIGhlcmVieSBncmFudHMgdG8gWW91IGEgcGVycGV0dWFsLAogICB3b3JsZHdpZGUsIG5vbi1leGNsdXNpdmUsIG5vLWNoYXJnZSwgcm95YWx0eS1mcmVlLCBpcnJldm9jYWJsZQogICBjb3B5cmlnaHQgbGljZW5zZSB0byByZXByb2R1Y2UsIHByZXBhcmUgRGVyaXZhdGl2ZSBXb3JrcyBvZiwKICAgcHVibGljbHkgZGlzcGxheSwgcHVibGljbHkgcGVyZm9ybSwgc3VibGljZW5zZSwgYW5kIGRpc3RyaWJ1dGUgdGhlCiAgIFdvcmsgYW5kIHN1Y2ggRGVyaXZhdGl2ZSBXb3JrcyBpbiBTb3VyY2Ugb3IgT2JqZWN0IGZvcm0uCgozLiBHcmFudCBvZiBQYXRlbnQgTGljZW5zZS4gU3ViamVjdCB0byB0aGUgdGVybXMgYW5kIGNvbmRpdGlvbnMgb2YKICAgdGhpcyBMaWNlbnNlLCBlYWNoIENvbnRyaWJ1dG9yIGhlcmVieSBncmFudHMgdG8gWW91IGEgcGVycGV0dWFsLAogICB3b3JsZHdpZGUsIG5vbi1leGNsdXNpdmUsIG5vLWNoYXJnZSwgcm95YWx0eS1mcmVlLCBpcnJldm9jYWJsZQogICAoZXhjZXB0IGFzIHN0YXRlZCBpbiB0aGlzIHNlY3Rpb24pIHBhdGVudCBsaWNlbnNlIHRvIG1ha2UsIGhhdmUgbWFkZSwKICAgdXNlLCBvZmZlciB0byBzZWxsLCBzZWxsLCBpbXBvcnQsIGFuZCBvdGhlcndpc2UgdHJhbnNmZXIgdGhlIFdvcmssCiAgIHdoZXJlIHN1Y2ggbGljZW5zZSBhcHBsaWVzIG9ubHkgdG8gdGhvc2UgcGF0ZW50IGNsYWltcyBsaWNlbnNhYmxlCiAgIGJ5IHN1Y2ggQ29udHJpYnV0b3IgdGhhdCBhcmUgbmVjZXNzYXJpbHkgaW5mcmluZ2VkIGJ5IHRoZWlyCiAgIENvbnRyaWJ1dGlvbihzKSBhbG9uZSBvciBieSBjb21iaW5hdGlvbiBvZiB0aGVpciBDb250cmlidXRpb24ocykKICAgd2l0aCB0aGUgV29yayB0byB3aGljaCBzdWNoIENvbnRyaWJ1dGlvbihzKSB3YXMgc3VibWl0dGVkLiBJZiBZb3UKICAgaW5zdGl0dXRlIHBhdGVudCBsaXRpZ2F0aW9uIGFnYWluc3QgYW55IGVudGl0eSAoaW5jbHVkaW5nIGEKICAgY3Jvc3MtY2xhaW0gb3IgY291bnRlcmNsYWltIGluIGEgbGF3c3VpdCkgYWxsZWdpbmcgdGhhdCB0aGUgV29yawogICBvciBhIENvbnRyaWJ1dGlvbiBpbmNvcnBvcmF0ZWQgd2l0aGluIHRoZSBXb3JrIGNvbnN0aXR1dGVzIGRpcmVjdAogICBvciBjb250cmlidXRvcnkgcGF0ZW50IGluZnJpbmdlbWVudCwgdGhlbiBhbnkgcGF0ZW50IGxpY2Vuc2VzCiAgIGdyYW50ZWQgdG8gWW91IHVuZGVyIHRoaXMgTGljZW5zZSBmb3IgdGhhdCBXb3JrIHNoYWxsIHRlcm1pbmF0ZQogICBhcyBvZiB0aGUgZGF0ZSBzdWNoIGxpdGlnYXRpb24gaXMgZmlsZWQuCgo0LiBSZWRpc3RyaWJ1dGlvbi4gWW91IG1heSByZXByb2R1Y2UgYW5kIGRpc3RyaWJ1dGUgY29waWVzIG9mIHRoZQogICBXb3JrIG9yIERlcml2YXRpdmUgV29ya3MgdGhlcmVvZiBpbiBhbnkgbWVkaXVtLCB3aXRoIG9yIHdpdGhvdXQKICAgbW9kaWZpY2F0aW9ucywgYW5kIGluIFNvdXJjZSBvciBPYmplY3QgZm9ybSwgcHJvdmlkZWQgdGhhdCBZb3UKICAgbWVldCB0aGUgZm9sbG93aW5nIGNvbmRpdGlvbnM6CgogICAoYSkgWW91IG11c3QgZ2l2ZSBhbnkgb3RoZXIgcmVjaXBpZW50cyBvZiB0aGUgV29yayBvcgogICAgICAgRGVyaXZhdGl2ZSBXb3JrcyBhIGNvcHkgb2YgdGhpcyBMaWNlbnNlOyBhbmQKCiAgIChiKSBZb3UgbXVzdCBjYXVzZSBhbnkgbW9kaWZpZWQgZmlsZXMgdG8gY2FycnkgcHJvbWluZW50IG5vdGljZXMKICAgICAgIHN0YXRpbmcgdGhhdCBZb3UgY2hhbmdlZCB0aGUgZmlsZXM7IGFuZAoKICAgKGMpIFlvdSBtdXN0IHJldGFpbiwgaW4gdGhlIFNvdXJjZSBmb3JtIG9mIGFueSBEZXJpdmF0aXZlIFdvcmtzCiAgICAgICB0aGF0IFlvdSBkaXN0cmlidXRlLCBhbGwgY29weXJpZ2h0LCBwYXRlbnQsIHRyYWRlbWFyaywgYW5kCiAgICAgICBhdHRyaWJ1dGlvbiBub3RpY2VzIGZyb20gdGhlIFNvdXJjZSBmb3JtIG9mIHRoZSBXb3JrLAogICAgICAgZXhjbHVkaW5nIHRob3NlIG5vdGljZXMgdGhhdCBkbyBub3QgcGVydGFpbiB0byBhbnkgcGFydCBvZgogICAgICAgdGhlIERlcml2YXRpdmUgV29ya3M7IGFuZAoKICAgKGQpIElmIHRoZSBXb3JrIGluY2x1ZGVzIGEgIk5PVElDRSIgdGV4dCBmaWxlIGFzIHBhcnQgb2YgaXRzCiAgICAgICBkaXN0cmlidXRpb24sIHRoZW4gYW55IERlcml2YXRpdmUgV29ya3MgdGhhdCBZb3UgZGlzdHJpYnV0ZSBtdXN0CiAgICAgICBpbmNsdWRlIGEgcmVhZGFibGUgY29weSBvZiB0aGUgYXR0cmlidXRpb24gbm90aWNlcyBjb250YWluZWQKICAgICAgIHdpdGhpbiBzdWNoIE5PVElDRSBmaWxlLCBleGNsdWRpbmcgdGhvc2Ugbm90aWNlcyB0aGF0IGRvIG5vdAogICAgICAgcGVydGFpbiB0byBhbnkgcGFydCBvZiB0aGUgRGVyaXZhdGl2ZSBXb3JrcywgaW4gYXQgbGVhc3Qgb25lCiAgICAgICBvZiB0aGUgZm9sbG93aW5nIHBsYWNlczogd2l0aGluIGEgTk9USUNFIHRleHQgZmlsZSBkaXN0cmlidXRlZAogICAgICAgYXMgcGFydCBvZiB0aGUgRGVyaXZhdGl2ZSBXb3Jrczsgd2l0aGluIHRoZSBTb3VyY2UgZm9ybSBvcgogICAgICAgZG9jdW1lbnRhdGlvbiwgaWYgcHJvdmlkZWQgYWxvbmcgd2l0aCB0aGUgRGVyaXZhdGl2ZSBXb3Jrczsgb3IsCiAgICAgICB3aXRoaW4gYSBkaXNwbGF5IGdlbmVyYXRlZCBieSB0aGUgRGVyaXZhdGl2ZSBXb3JrcywgaWYgYW5kCiAgICAgICB3aGVyZXZlciBzdWNoIHRoaXJkLXBhcnR5IG5vdGljZXMgbm9ybWFsbHkgYXBwZWFyLiBUaGUgY29udGVudHMKICAgICAgIG9mIHRoZSBOT1RJQ0UgZmlsZSBhcmUgZm9yIGluZm9ybWF0aW9uYWwgcHVycG9zZXMgb25seSBhbmQKICAgICAgIGRvIG5vdCBtb2RpZnkgdGhlIExpY2Vuc2UuIFlvdSBtYXkgYWRkIFlvdXIgb3duIGF0dHJpYnV0aW9uCiAgICAgICBub3RpY2VzIHdpdGhpbiBEZXJpdmF0aXZlIFdvcmtzIHRoYXQgWW91IGRpc3RyaWJ1dGUsIGFsb25nc2lkZQogICAgICAgb3IgYXMgYW4gYWRkZW5kdW0gdG8gdGhlIE5PVElDRSB0ZXh0IGZyb20gdGhlIFdvcmssIHByb3ZpZGVkCiAgICAgICB0aGF0IHN1Y2ggYWRkaXRpb25hbCBhdHRyaWJ1dGlvbiBub3RpY2VzIGNhbm5vdCBiZSBjb25zdHJ1ZWQKICAgICAgIGFzIG1vZGlmeWluZyB0aGUgTGljZW5zZS4KCiAgIFlvdSBtYXkgYWRkIFlvdXIgb3duIGNvcHlyaWdodCBzdGF0ZW1lbnQgdG8gWW91ciBtb2RpZmljYXRpb25zIGFuZAogICBtYXkgcHJvdmlkZSBhZGRpdGlvbmFsIG9yIGRpZmZlcmVudCBsaWNlbnNlIHRlcm1zIGFuZCBjb25kaXRpb25zCiAgIGZvciB1c2UsIHJlcHJvZHVjdGlvbiwgb3IgZGlzdHJpYnV0aW9uIG9mIFlvdXIgbW9kaWZpY2F0aW9ucywgb3IKICAgZm9yIGFueSBzdWNoIERlcml2YXRpdmUgV29ya3MgYXMgYSB3aG9sZSwgcHJvdmlkZWQgWW91ciB1c2UsCiAgIHJlcHJvZHVjdGlvbiwgYW5kIGRpc3RyaWJ1dGlvbiBvZiB0aGUgV29yayBvdGhlcndpc2UgY29tcGxpZXMgd2l0aAogICB0aGUgY29uZGl0aW9ucyBzdGF0ZWQgaW4gdGhpcyBMaWNlbnNlLgoKNS4gU3VibWlzc2lvbiBvZiBDb250cmlidXRpb25zLiBVbmxlc3MgWW91IGV4cGxpY2l0bHkgc3RhdGUgb3RoZXJ3aXNlLAogICBhbnkgQ29udHJpYnV0aW9uIGludGVudGlvbmFsbHkgc3VibWl0dGVkIGZvciBpbmNsdXNpb24gaW4gdGhlIFdvcmsKICAgYnkgWW91IHRvIHRoZSBMaWNlbnNvciBzaGFsbCBiZSB1bmRlciB0aGUgdGVybXMgYW5kIGNvbmRpdGlvbnMgb2YKICAgdGhpcyBMaWNlbnNlLCB3aXRob3V0IGFueSBhZGRpdGlvbmFsIHRlcm1zIG9yIGNvbmRpdGlvbnMuCiAgIE5vdHdpdGhzdGFuZGluZyB0aGUgYWJvdmUsIG5vdGhpbmcgaGVyZWluIHNoYWxsIHN1cGVyc2VkZSBvciBtb2RpZnkKICAgdGhlIHRlcm1zIG9mIGFueSBzZXBhcmF0ZSBsaWNlbnNlIGFncmVlbWVudCB5b3UgbWF5IGhhdmUgZXhlY3V0ZWQKICAgd2l0aCBMaWNlbnNvciByZWdhcmRpbmcgc3VjaCBDb250cmlidXRpb25zLgoKNi4gVHJhZGVtYXJrcy4gVGhpcyBMaWNlbnNlIGRvZXMgbm90IGdyYW50IHBlcm1pc3Npb24gdG8gdXNlIHRoZSB0cmFkZQogICBuYW1lcywgdHJhZGVtYXJrcywgc2VydmljZSBtYXJrcywgb3IgcHJvZHVjdCBuYW1lcyBvZiB0aGUgTGljZW5zb3IsCiAgIGV4Y2VwdCBhcyByZXF1aXJlZCBmb3IgcmVhc29uYWJsZSBhbmQgY3VzdG9tYXJ5IHVzZSBpbiBkZXNjcmliaW5nIHRoZQogICBvcmlnaW4gb2YgdGhlIFdvcmsgYW5kIHJlcHJvZHVjaW5nIHRoZSBjb250ZW50IG9mIHRoZSBOT1RJQ0UgZmlsZS4KCjcuIERpc2NsYWltZXIgb2YgV2FycmFudHkuIFVubGVzcyByZXF1aXJlZCBieSBhcHBsaWNhYmxlIGxhdyBvcgogICBhZ3JlZWQgdG8gaW4gd3JpdGluZywgTGljZW5zb3IgcHJvdmlkZXMgdGhlIFdvcmsgKGFuZCBlYWNoCiAgIENvbnRyaWJ1dG9yIHByb3ZpZGVzIGl0cyBDb250cmlidXRpb25zKSBvbiBhbiAiQVMgSVMiIEJBU0lTLAogICBXSVRIT1VUIFdBUlJBTlRJRVMgT1IgQ09ORElUSU9OUyBPRiBBTlkgS0lORCwgZWl0aGVyIGV4cHJlc3Mgb3IKICAgaW1wbGllZCwgaW5jbHVkaW5nLCB3aXRob3V0IGxpbWl0YXRpb24sIGFueSB3YXJyYW50aWVzIG9yIGNvbmRpdGlvbnMKICAgb2YgVElUTEUsIE5PTi1JTkZSSU5HRU1FTlQsIE1FUkNIQU5UQUJJTElUWSwgb3IgRklUTkVTUyBGT1IgQQogICBQQVJUSUNVTEFSIFBVUlBPU0UuIFlvdSBhcmUgc29sZWx5IHJlc3BvbnNpYmxlIGZvciBkZXRlcm1pbmluZyB0aGUKICAgYXBwcm9wcmlhdGVuZXNzIG9mIHVzaW5nIG9yIHJlZGlzdHJpYnV0aW5nIHRoZSBXb3JrIGFuZCBhc3N1bWUgYW55CiAgIHJpc2tzIGFzc29jaWF0ZWQgd2l0aCBZb3VyIGV4ZXJjaXNlIG9mIHBlcm1pc3Npb25zIHVuZGVyIHRoaXMgTGljZW5zZS4KCjguIExpbWl0YXRpb24gb2YgTGlhYmlsaXR5LiBJbiBubyBldmVudCBhbmQgdW5kZXIgbm8gbGVnYWwgdGhlb3J5LAogICB3aGV0aGVyIGluIHRvcnQgKGluY2x1ZGluZyBuZWdsaWdlbmNlKSwgY29udHJhY3QsIG9yIG90aGVyd2lzZSwKICAgdW5sZXNzIHJlcXVpcmVkIGJ5IGFwcGxpY2FibGUgbGF3IChzdWNoIGFzIGRlbGliZXJhdGUgYW5kIGdyb3NzbHkKICAgbmVnbGlnZW50IGFjdHMpIG9yIGFncmVlZCB0byBpbiB3cml0aW5nLCBzaGFsbCBhbnkgQ29udHJpYnV0b3IgYmUKICAgbGlhYmxlIHRvIFlvdSBmb3IgZGFtYWdlcywgaW5jbHVkaW5nIGFueSBkaXJlY3QsIGluZGlyZWN0LCBzcGVjaWFsLAogICBpbmNpZGVudGFsLCBvciBjb25zZXF1ZW50aWFsIGRhbWFnZXMgb2YgYW55IGNoYXJhY3RlciBhcmlzaW5nIGFzIGEKICAgcmVzdWx0IG9mIHRoaXMgTGljZW5zZSBvciBvdXQgb2YgdGhlIHVzZSBvciBpbmFiaWxpdHkgdG8gdXNlIHRoZQogICBXb3JrIChpbmNsdWRpbmcgYnV0IG5vdCBsaW1pdGVkIHRvIGRhbWFnZXMgZm9yIGxvc3Mgb2YgZ29vZHdpbGwsCiAgIHdvcmsgc3RvcHBhZ2UsIGNvbXB1dGVyIGZhaWx1cmUgb3IgbWFsZnVuY3Rpb24sIG9yIGFueSBhbmQgYWxsCiAgIG90aGVyIGNvbW1lcmNpYWwgZGFtYWdlcyBvciBsb3NzZXMpLCBldmVuIGlmIHN1Y2ggQ29udHJpYnV0b3IKICAgaGFzIGJlZW4gYWR2aXNlZCBvZiB0aGUgcG9zc2liaWxpdHkgb2Ygc3VjaCBkYW1hZ2VzLgoKOS4gQWNjZXB0aW5nIFdhcnJhbnR5IG9yIEFkZGl0aW9uYWwgTGlhYmlsaXR5LiBXaGlsZSByZWRpc3RyaWJ1dGluZwogICB0aGUgV29yayBvciBEZXJpdmF0aXZlIFdvcmtzIHRoZXJlb2YsIFlvdSBtYXkgY2hvb3NlIHRvIG9mZmVyLAogICBhbmQgY2hhcmdlIGEgZmVlIGZvciwgYWNjZXB0YW5jZSBvZiBzdXBwb3J0LCB3YXJyYW50eSwgaW5kZW1uaXR5LAogICBvciBvdGhlciBsaWFiaWxpdHkgb2JsaWdhdGlvbnMgYW5kL29yIHJpZ2h0cyBjb25zaXN0ZW50IHdpdGggdGhpcwogICBMaWNlbnNlLiBIb3dldmVyLCBpbiBhY2NlcHRpbmcgc3VjaCBvYmxpZ2F0aW9ucywgWW91IG1heSBhY3Qgb25seQogICBvbiBZb3VyIG93biBiZWhhbGYgYW5kIG9uIFlvdXIgc29sZSByZXNwb25zaWJpbGl0eSwgbm90IG9uIGJlaGFsZgogICBvZiBhbnkgb3RoZXIgQ29udHJpYnV0b3IsIGFuZCBvbmx5IGlmIFlvdSBhZ3JlZSB0byBpbmRlbW5pZnksCiAgIGRlZmVuZCwgYW5kIGhvbGQgZWFjaCBDb250cmlidXRvciBoYXJtbGVzcyBmb3IgYW55IGxpYWJpbGl0eQogICBpbmN1cnJlZCBieSwgb3IgY2xhaW1zIGFzc2VydGVkIGFnYWluc3QsIHN1Y2ggQ29udHJpYnV0b3IgYnkgcmVhc29uCiAgIG9mIHlvdXIgYWNjZXB0aW5nIGFueSBzdWNoIHdhcnJhbnR5IG9yIGFkZGl0aW9uYWwgbGlhYmlsaXR5Lgo=")
    )
    $entries = @{
        "defusedxml|0.7.1|PSFL" = @{
            Role = "transitive defensive-XML support in the pip-audit CycloneDX-support chain"
            ReReview = "Re-review on any version, gate value, role, modification, vendoring, or distribution change; retain applicable license text and notices before distribution."
        }
        "markdown-it-py|4.2.0|MIT License" = @{
            Role = "transitive markdown rendering for pip-audit console presentation"
            ReReview = "Re-review on any version, gate value, role, modification, vendoring, or distribution change; retain the license and copyright notice before distribution."
        }
        "mdurl|0.1.2|MIT License" = @{
            Role = "transitive URL parsing for the pip-audit markdown-rendering chain"
            ReReview = "Re-review on any version, gate value, role, modification, vendoring, or distribution change; retain the license and copyright notice before distribution."
        }
        "pip_audit|2.10.1|Apache Software License" = @{
            Role = "direct development dependency used only by deps:audit and the CI advisory-control job"
            ReReview = "Re-review on any version, gate value, role, modification, vendoring, or distribution change; retain the license and any applicable NOTICE material before distribution."
        }
        "sortedcontainers|2.4.0|Apache 2.0" = @{
            Role = "transitive sorted-collection support in the pip-audit CycloneDX-support chain"
            ReReview = "Re-review on any version, gate value, role, modification, vendoring, or distribution change; retain the license and any applicable NOTICE material before distribution."
        }
        "tomli_w|1.2.0|MIT License" = @{
            Role = "transitive TOML-writing support in the pip-audit dependency chain"
            ReReview = "Re-review on any version, gate value, role, modification, vendoring, or distribution change; retain the license and copyright notice before distribution."
        }
    }
    $entries["pip_api|0.0.35|$pipApiGateValue"] = @{
        Role = "transitive pip-environment access within pip-audit"
        ReReview = "Re-review on any version, gate value, role, modification, vendoring, or distribution change; retain the license and any applicable NOTICE material before distribution."
    }

    $key = "$Name|$Version|$License"
    if (-not $entries.ContainsKey($key)) {
        return $null
    }

    return [pscustomobject]@{
        RecordId = "0004"
        Role = $entries[$key].Role
        ReReview = $entries[$key].ReReview
    }
}

function Get-Decision0005CatalogEntry {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][string]$Version,
        [AllowNull()][string]$License
    )

    # Decision Record 0005 permits only these two literal runtime values for
    # the Phase 3 slice. The scipy metadata is represented losslessly (46,555
    # UTF-8 bytes including one trailing line feed) and must match the
    # recorded SHA-256 before it can be used; on a mismatch the entry is
    # omitted and the gate fails closed.
    $scipyGateBytes = [System.Convert]::FromBase64String("Q29weXJpZ2h0IChjKSAyMDAxLTIwMDIgRW50aG91Z2h0LCBJbmMuIDIwMDMsIFNjaVB5IERldmVsb3BlcnMuCiBBbGwgcmlnaHRzIHJlc2VydmVkLgoKIFJlZGlzdHJpYnV0aW9uIGFuZCB1c2UgaW4gc291cmNlIGFuZCBiaW5hcnkgZm9ybXMsIHdpdGggb3Igd2l0aG91dAogbW9kaWZpY2F0aW9uLCBhcmUgcGVybWl0dGVkIHByb3ZpZGVkIHRoYXQgdGhlIGZvbGxvd2luZyBjb25kaXRpb25zCiBhcmUgbWV0OgoKIDEuIFJlZGlzdHJpYnV0aW9ucyBvZiBzb3VyY2UgY29kZSBtdXN0IHJldGFpbiB0aGUgYWJvdmUgY29weXJpZ2h0CiAgICBub3RpY2UsIHRoaXMgbGlzdCBvZiBjb25kaXRpb25zIGFuZCB0aGUgZm9sbG93aW5nIGRpc2NsYWltZXIuCgogMi4gUmVkaXN0cmlidXRpb25zIGluIGJpbmFyeSBmb3JtIG11c3QgcmVwcm9kdWNlIHRoZSBhYm92ZQogICAgY29weXJpZ2h0IG5vdGljZSwgdGhpcyBsaXN0IG9mIGNvbmRpdGlvbnMgYW5kIHRoZSBmb2xsb3dpbmcKICAgIGRpc2NsYWltZXIgaW4gdGhlIGRvY3VtZW50YXRpb24gYW5kL29yIG90aGVyIG1hdGVyaWFscyBwcm92aWRlZAogICAgd2l0aCB0aGUgZGlzdHJpYnV0aW9uLgoKIDMuIE5laXRoZXIgdGhlIG5hbWUgb2YgdGhlIGNvcHlyaWdodCBob2xkZXIgbm9yIHRoZSBuYW1lcyBvZiBpdHMKICAgIGNvbnRyaWJ1dG9ycyBtYXkgYmUgdXNlZCB0byBlbmRvcnNlIG9yIHByb21vdGUgcHJvZHVjdHMgZGVyaXZlZAogICAgZnJvbSB0aGlzIHNvZnR3YXJlIHdpdGhvdXQgc3BlY2lmaWMgcHJpb3Igd3JpdHRlbiBwZXJtaXNzaW9uLgoKIFRISVMgU09GVFdBUkUgSVMgUFJPVklERUQgQlkgVEhFIENPUFlSSUdIVCBIT0xERVJTIEFORCBDT05UUklCVVRPUlMKICJBUyBJUyIgQU5EIEFOWSBFWFBSRVNTIE9SIElNUExJRUQgV0FSUkFOVElFUywgSU5DTFVESU5HLCBCVVQgTk9UCiBMSU1JVEVEIFRPLCBUSEUgSU1QTElFRCBXQVJSQU5USUVTIE9GIE1FUkNIQU5UQUJJTElUWSBBTkQgRklUTkVTUyBGT1IKIEEgUEFSVElDVUxBUiBQVVJQT1NFIEFSRSBESVNDTEFJTUVELiBJTiBOTyBFVkVOVCBTSEFMTCBUSEUgQ09QWVJJR0hUCiBPV05FUiBPUiBDT05UUklCVVRPUlMgQkUgTElBQkxFIEZPUiBBTlkgRElSRUNULCBJTkRJUkVDVCwgSU5DSURFTlRBTCwKIFNQRUNJQUwsIEVYRU1QTEFSWSwgT1IgQ09OU0VRVUVOVElBTCBEQU1BR0VTIChJTkNMVURJTkcsIEJVVCBOT1QKIExJTUlURUQgVE8sIFBST0NVUkVNRU5UIE9GIFNVQlNUSVRVVEUgR09PRFMgT1IgU0VSVklDRVM7IExPU1MgT0YgVVNFLAogREFUQSwgT1IgUFJPRklUUzsgT1IgQlVTSU5FU1MgSU5URVJSVVBUSU9OKSBIT1dFVkVSIENBVVNFRCBBTkQgT04gQU5ZCiBUSEVPUlkgT0YgTElBQklMSVRZLCBXSEVUSEVSIElOIENPTlRSQUNULCBTVFJJQ1QgTElBQklMSVRZLCBPUiBUT1JUCiAoSU5DTFVESU5HIE5FR0xJR0VOQ0UgT1IgT1RIRVJXSVNFKSBBUklTSU5HIElOIEFOWSBXQVkgT1VUIE9GIFRIRSBVU0UKIE9GIFRISVMgU09GVFdBUkUsIEVWRU4gSUYgQURWSVNFRCBPRiBUSEUgUE9TU0lCSUxJVFkgT0YgU1VDSCBEQU1BR0UuCgogLS0tLQoKCiAtLS0tCgogVGhpcyBiaW5hcnkgZGlzdHJpYnV0aW9uIG9mIFNjaVB5IGNhbiBhbHNvIGJ1bmRsZSB0aGUgZm9sbG93aW5nIHNvZnR3YXJlCiAoZGVwZW5kaW5nIG9uIHRoZSBidWlsZCk6CgoKIE5hbWU6IE9wZW5CTEFTCiBGaWxlczogc2NpcHkubGlic1xsaWJzY2lweV9vcGVuYmxhcyouZGxsCiBEZXNjcmlwdGlvbjogYnVuZGxlZCBhcyBhIGR5bmFtaWNhbGx5IGxpbmtlZCBsaWJyYXJ5CiBBdmFpbGFiaWxpdHk6IGh0dHBzOi8vZ2l0aHViLmNvbS9PcGVuTWF0aExpYi9PcGVuQkxBUy8KIExpY2Vuc2U6IEJTRC0zLUNsYXVzZQogICBDb3B5cmlnaHQgKGMpIDIwMTEtMjAxNCwgVGhlIE9wZW5CTEFTIFByb2plY3QKICAgQWxsIHJpZ2h0cyByZXNlcnZlZC4KCiAgIFJlZGlzdHJpYnV0aW9uIGFuZCB1c2UgaW4gc291cmNlIGFuZCBiaW5hcnkgZm9ybXMsIHdpdGggb3Igd2l0aG91dAogICBtb2RpZmljYXRpb24sIGFyZSBwZXJtaXR0ZWQgcHJvdmlkZWQgdGhhdCB0aGUgZm9sbG93aW5nIGNvbmRpdGlvbnMgYXJlCiAgIG1ldDoKCiAgICAgIDEuIFJlZGlzdHJpYnV0aW9ucyBvZiBzb3VyY2UgY29kZSBtdXN0IHJldGFpbiB0aGUgYWJvdmUgY29weXJpZ2h0CiAgICAgICAgIG5vdGljZSwgdGhpcyBsaXN0IG9mIGNvbmRpdGlvbnMgYW5kIHRoZSBmb2xsb3dpbmcgZGlzY2xhaW1lci4KCiAgICAgIDIuIFJlZGlzdHJpYnV0aW9ucyBpbiBiaW5hcnkgZm9ybSBtdXN0IHJlcHJvZHVjZSB0aGUgYWJvdmUgY29weXJpZ2h0CiAgICAgICAgIG5vdGljZSwgdGhpcyBsaXN0IG9mIGNvbmRpdGlvbnMgYW5kIHRoZSBmb2xsb3dpbmcgZGlzY2xhaW1lciBpbgogICAgICAgICB0aGUgZG9jdW1lbnRhdGlvbiBhbmQvb3Igb3RoZXIgbWF0ZXJpYWxzIHByb3ZpZGVkIHdpdGggdGhlCiAgICAgICAgIGRpc3RyaWJ1dGlvbi4KICAgICAgMy4gTmVpdGhlciB0aGUgbmFtZSBvZiB0aGUgT3BlbkJMQVMgcHJvamVjdCBub3IgdGhlIG5hbWVzIG9mIAogICAgICAgICBpdHMgY29udHJpYnV0b3JzIG1heSBiZSB1c2VkIHRvIGVuZG9yc2Ugb3IgcHJvbW90ZSBwcm9kdWN0cyAKICAgICAgICAgZGVyaXZlZCBmcm9tIHRoaXMgc29mdHdhcmUgd2l0aG91dCBzcGVjaWZpYyBwcmlvciB3cml0dGVuIAogICAgICAgICBwZXJtaXNzaW9uLgoKICAgVEhJUyBTT0ZUV0FSRSBJUyBQUk9WSURFRCBCWSBUSEUgQ09QWVJJR0hUIEhPTERFUlMgQU5EIENPTlRSSUJVVE9SUyAiQVMgSVMiCiAgIEFORCBBTlkgRVhQUkVTUyBPUiBJTVBMSUVEIFdBUlJBTlRJRVMsIElOQ0xVRElORywgQlVUIE5PVCBMSU1JVEVEIFRPLCBUSEUKICAgSU1QTElFRCBXQVJSQU5USUVTIE9GIE1FUkNIQU5UQUJJTElUWSBBTkQgRklUTkVTUyBGT1IgQSBQQVJUSUNVTEFSIFBVUlBPU0UKICAgQVJFIERJU0NMQUlNRUQuIElOIE5PIEVWRU5UIFNIQUxMIFRIRSBDT1BZUklHSFQgT1dORVIgT1IgQ09OVFJJQlVUT1JTIEJFCiAgIExJQUJMRSBGT1IgQU5ZIERJUkVDVCwgSU5ESVJFQ1QsIElOQ0lERU5UQUwsIFNQRUNJQUwsIEVYRU1QTEFSWSwgT1IgQ09OU0VRVUVOVElBTAogICBEQU1BR0VTIChJTkNMVURJTkcsIEJVVCBOT1QgTElNSVRFRCBUTywgUFJPQ1VSRU1FTlQgT0YgU1VCU1RJVFVURSBHT09EUyBPUgogICBTRVJWSUNFUzsgTE9TUyBPRiBVU0UsIERBVEEsIE9SIFBST0ZJVFM7IE9SIEJVU0lORVNTIElOVEVSUlVQVElPTikgSE9XRVZFUgogICBDQVVTRUQgQU5EIE9OIEFOWSBUSEVPUlkgT0YgTElBQklMSVRZLCBXSEVUSEVSIElOIENPTlRSQUNULCBTVFJJQ1QgTElBQklMSVRZLAogICBPUiBUT1JUIChJTkNMVURJTkcgTkVHTElHRU5DRSBPUiBPVEhFUldJU0UpIEFSSVNJTkcgSU4gQU5ZIFdBWSBPVVQgT0YgVEhFCiAgIFVTRSBPRiBUSElTIFNPRlRXQVJFLCBFVkVOIElGIEFEVklTRUQgT0YgVEhFIFBPU1NJQklMSVRZIE9GIFNVQ0ggREFNQUdFLgoKCiBOYW1lOiBMQVBBQ0sKIEZpbGVzOiBzY2lweS5saWJzXGxpYnNjaXB5X29wZW5ibGFzKi5kbGwKIERlc2NyaXB0aW9uOiBidW5kbGVkIGluIE9wZW5CTEFTCiBBdmFpbGFiaWxpdHk6IGh0dHBzOi8vZ2l0aHViLmNvbS9PcGVuTWF0aExpYi9PcGVuQkxBUy8KIExpY2Vuc2U6IEJTRC0zLUNsYXVzZS1PcGVuLU1QSQogICBDb3B5cmlnaHQgKGMpIDE5OTItMjAxMyBUaGUgVW5pdmVyc2l0eSBvZiBUZW5uZXNzZWUgYW5kIFRoZSBVbml2ZXJzaXR5CiAgICAgICAgICAgICAgICAgICAgICAgICAgIG9mIFRlbm5lc3NlZSBSZXNlYXJjaCBGb3VuZGF0aW9uLiAgQWxsIHJpZ2h0cwogICAgICAgICAgICAgICAgICAgICAgICAgICByZXNlcnZlZC4KICAgQ29weXJpZ2h0IChjKSAyMDAwLTIwMTMgVGhlIFVuaXZlcnNpdHkgb2YgQ2FsaWZvcm5pYSBCZXJrZWxleS4gQWxsCiAgICAgICAgICAgICAgICAgICAgICAgICAgIHJpZ2h0cyByZXNlcnZlZC4KICAgQ29weXJpZ2h0IChjKSAyMDA2LTIwMTMgVGhlIFVuaXZlcnNpdHkgb2YgQ29sb3JhZG8gRGVudmVyLiAgQWxsIHJpZ2h0cwogICAgICAgICAgICAgICAgICAgICAgICAgICByZXNlcnZlZC4KCiAgICRDT1BZUklHSFQkCgogICBBZGRpdGlvbmFsIGNvcHlyaWdodHMgbWF5IGZvbGxvdwoKICAgJEhFQURFUiQKCiAgIFJlZGlzdHJpYnV0aW9uIGFuZCB1c2UgaW4gc291cmNlIGFuZCBiaW5hcnkgZm9ybXMsIHdpdGggb3Igd2l0aG91dAogICBtb2RpZmljYXRpb24sIGFyZSBwZXJtaXR0ZWQgcHJvdmlkZWQgdGhhdCB0aGUgZm9sbG93aW5nIGNvbmRpdGlvbnMgYXJlCiAgIG1ldDoKCiAgIC0gUmVkaXN0cmlidXRpb25zIG9mIHNvdXJjZSBjb2RlIG11c3QgcmV0YWluIHRoZSBhYm92ZSBjb3B5cmlnaHQKICAgICBub3RpY2UsIHRoaXMgbGlzdCBvZiBjb25kaXRpb25zIGFuZCB0aGUgZm9sbG93aW5nIGRpc2NsYWltZXIuCgogICAtIFJlZGlzdHJpYnV0aW9ucyBpbiBiaW5hcnkgZm9ybSBtdXN0IHJlcHJvZHVjZSB0aGUgYWJvdmUgY29weXJpZ2h0CiAgICAgbm90aWNlLCB0aGlzIGxpc3Qgb2YgY29uZGl0aW9ucyBhbmQgdGhlIGZvbGxvd2luZyBkaXNjbGFpbWVyIGxpc3RlZAogICAgIGluIHRoaXMgbGljZW5zZSBpbiB0aGUgZG9jdW1lbnRhdGlvbiBhbmQvb3Igb3RoZXIgbWF0ZXJpYWxzCiAgICAgcHJvdmlkZWQgd2l0aCB0aGUgZGlzdHJpYnV0aW9uLgoKICAgLSBOZWl0aGVyIHRoZSBuYW1lIG9mIHRoZSBjb3B5cmlnaHQgaG9sZGVycyBub3IgdGhlIG5hbWVzIG9mIGl0cwogICAgIGNvbnRyaWJ1dG9ycyBtYXkgYmUgdXNlZCB0byBlbmRvcnNlIG9yIHByb21vdGUgcHJvZHVjdHMgZGVyaXZlZCBmcm9tCiAgICAgdGhpcyBzb2Z0d2FyZSB3aXRob3V0IHNwZWNpZmljIHByaW9yIHdyaXR0ZW4gcGVybWlzc2lvbi4KCiAgIFRoZSBjb3B5cmlnaHQgaG9sZGVycyBwcm92aWRlIG5vIHJlYXNzdXJhbmNlcyB0aGF0IHRoZSBzb3VyY2UgY29kZQogICBwcm92aWRlZCBkb2VzIG5vdCBpbmZyaW5nZSBhbnkgcGF0ZW50LCBjb3B5cmlnaHQsIG9yIGFueSBvdGhlcgogICBpbnRlbGxlY3R1YWwgcHJvcGVydHkgcmlnaHRzIG9mIHRoaXJkIHBhcnRpZXMuICBUaGUgY29weXJpZ2h0IGhvbGRlcnMKICAgZGlzY2xhaW0gYW55IGxpYWJpbGl0eSB0byBhbnkgcmVjaXBpZW50IGZvciBjbGFpbXMgYnJvdWdodCBhZ2FpbnN0CiAgIHJlY2lwaWVudCBieSBhbnkgdGhpcmQgcGFydHkgZm9yIGluZnJpbmdlbWVudCBvZiB0aGF0IHBhcnRpZXMKICAgaW50ZWxsZWN0dWFsIHByb3BlcnR5IHJpZ2h0cy4KCiAgIFRISVMgU09GVFdBUkUgSVMgUFJPVklERUQgQlkgVEhFIENPUFlSSUdIVCBIT0xERVJTIEFORCBDT05UUklCVVRPUlMKICAgIkFTIElTIiBBTkQgQU5ZIEVYUFJFU1MgT1IgSU1QTElFRCBXQVJSQU5USUVTLCBJTkNMVURJTkcsIEJVVCBOT1QKICAgTElNSVRFRCBUTywgVEhFIElNUExJRUQgV0FSUkFOVElFUyBPRiBNRVJDSEFOVEFCSUxJVFkgQU5EIEZJVE5FU1MgRk9SCiAgIEEgUEFSVElDVUxBUiBQVVJQT1NFIEFSRSBESVNDTEFJTUVELiBJTiBOTyBFVkVOVCBTSEFMTCBUSEUgQ09QWVJJR0hUCiAgIE9XTkVSIE9SIENPTlRSSUJVVE9SUyBCRSBMSUFCTEUgRk9SIEFOWSBESVJFQ1QsIElORElSRUNULCBJTkNJREVOVEFMLAogICBTUEVDSUFMLCBFWEVNUExBUlksIE9SIENPTlNFUVVFTlRJQUwgREFNQUdFUyAoSU5DTFVESU5HLCBCVVQgTk9UCiAgIExJTUlURUQgVE8sIFBST0NVUkVNRU5UIE9GIFNVQlNUSVRVVEUgR09PRFMgT1IgU0VSVklDRVM7IExPU1MgT0YgVVNFLAogICBEQVRBLCBPUiBQUk9GSVRTOyBPUiBCVVNJTkVTUyBJTlRFUlJVUFRJT04pIEhPV0VWRVIgQ0FVU0VEIEFORCBPTiBBTlkKICAgVEhFT1JZIE9GIExJQUJJTElUWSwgV0hFVEhFUiBJTiBDT05UUkFDVCwgU1RSSUNUIExJQUJJTElUWSwgT1IgVE9SVAogICAoSU5DTFVESU5HIE5FR0xJR0VOQ0UgT1IgT1RIRVJXSVNFKSBBUklTSU5HIElOIEFOWSBXQVkgT1VUIE9GIFRIRSBVU0UKICAgT0YgVEhJUyBTT0ZUV0FSRSwgRVZFTiBJRiBBRFZJU0VEIE9GIFRIRSBQT1NTSUJJTElUWSBPRiBTVUNIIERBTUFHRS4KCgogTmFtZTogR0NDIHJ1bnRpbWUgbGlicmFyeQogRmlsZXM6IHNjaXB5LmxpYnNcbGlic2NpcHlfb3BlbmJsYXMqLmRsbAogRGVzY3JpcHRpb246IHN0YXRpY2FsbHkgbGlua2VkIHRvIGZpbGVzIGNvbXBpbGVkIHdpdGggZ2NjCiBBdmFpbGFiaWxpdHk6IGh0dHBzOi8vZ2NjLmdudS5vcmcvZ2l0Lz9wPWdjYy5naXQ7YT10cmVlO2Y9bGliZ2ZvcnRyYW4KIExpY2Vuc2U6IEdQTC0zLjAtb3ItbGF0ZXIgV0lUSCBHQ0MtZXhjZXB0aW9uLTMuMQogICBDb3B5cmlnaHQgKEMpIDIwMDItMjAxNyBGcmVlIFNvZnR3YXJlIEZvdW5kYXRpb24sIEluYy4KCiAgIExpYmdmb3J0cmFuIGlzIGZyZWUgc29mdHdhcmU7IHlvdSBjYW4gcmVkaXN0cmlidXRlIGl0IGFuZC9vciBtb2RpZnkKICAgaXQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBHTlUgR2VuZXJhbCBQdWJsaWMgTGljZW5zZSBhcyBwdWJsaXNoZWQgYnkKICAgdGhlIEZyZWUgU29mdHdhcmUgRm91bmRhdGlvbjsgZWl0aGVyIHZlcnNpb24gMywgb3IgKGF0IHlvdXIgb3B0aW9uKQogICBhbnkgbGF0ZXIgdmVyc2lvbi4KCiAgIExpYmdmb3J0cmFuIGlzIGRpc3RyaWJ1dGVkIGluIHRoZSBob3BlIHRoYXQgaXQgd2lsbCBiZSB1c2VmdWwsCiAgIGJ1dCBXSVRIT1VUIEFOWSBXQVJSQU5UWTsgd2l0aG91dCBldmVuIHRoZSBpbXBsaWVkIHdhcnJhbnR5IG9mCiAgIE1FUkNIQU5UQUJJTElUWSBvciBGSVRORVNTIEZPUiBBIFBBUlRJQ1VMQVIgUFVSUE9TRS4gIFNlZSB0aGUKICAgR05VIEdlbmVyYWwgUHVibGljIExpY2Vuc2UgZm9yIG1vcmUgZGV0YWlscy4KCiAgIFVuZGVyIFNlY3Rpb24gNyBvZiBHUEwgdmVyc2lvbiAzLCB5b3UgYXJlIGdyYW50ZWQgYWRkaXRpb25hbAogICBwZXJtaXNzaW9ucyBkZXNjcmliZWQgaW4gdGhlIEdDQyBSdW50aW1lIExpYnJhcnkgRXhjZXB0aW9uLCB2ZXJzaW9uCiAgIDMuMSwgYXMgcHVibGlzaGVkIGJ5IHRoZSBGcmVlIFNvZnR3YXJlIEZvdW5kYXRpb24uCgogICBZb3Ugc2hvdWxkIGhhdmUgcmVjZWl2ZWQgYSBjb3B5IG9mIHRoZSBHTlUgR2VuZXJhbCBQdWJsaWMgTGljZW5zZSBhbmQKICAgYSBjb3B5IG9mIHRoZSBHQ0MgUnVudGltZSBMaWJyYXJ5IEV4Y2VwdGlvbiBhbG9uZyB3aXRoIHRoaXMgcHJvZ3JhbTsKICAgc2VlIHRoZSBmaWxlcyBDT1BZSU5HMyBhbmQgQ09QWUlORy5SVU5USU1FIHJlc3BlY3RpdmVseS4gIElmIG5vdCwgc2VlCiAgIDxodHRwOi8vd3d3LmdudS5vcmcvbGljZW5zZXMvPi4KCgogLS0tLQoKIEZ1bGwgdGV4dCBvZiBsaWNlbnNlIHRleHRzIHJlZmVycmVkIHRvIGFib3ZlIGZvbGxvd3MgKHRoYXQgdGhleSBhcmUKIGxpc3RlZCBiZWxvdyBkb2VzIG5vdCBuZWNlc3NhcmlseSBpbXBseSB0aGUgY29uZGl0aW9ucyBhcHBseSB0byB0aGUKIHByZXNlbnQgYmluYXJ5IHJlbGVhc2UpOgoKIC0tLS0KCiBHQ0MgUlVOVElNRSBMSUJSQVJZIEVYQ0VQVElPTgoKIFZlcnNpb24gMy4xLCAzMSBNYXJjaCAyMDA5CgogQ29weXJpZ2h0IChDKSAyMDA5IEZyZWUgU29mdHdhcmUgRm91bmRhdGlvbiwgSW5jLiA8aHR0cDovL2ZzZi5vcmcvPgoKIEV2ZXJ5b25lIGlzIHBlcm1pdHRlZCB0byBjb3B5IGFuZCBkaXN0cmlidXRlIHZlcmJhdGltIGNvcGllcyBvZiB0aGlzCiBsaWNlbnNlIGRvY3VtZW50LCBidXQgY2hhbmdpbmcgaXQgaXMgbm90IGFsbG93ZWQuCgogVGhpcyBHQ0MgUnVudGltZSBMaWJyYXJ5IEV4Y2VwdGlvbiAoIkV4Y2VwdGlvbiIpIGlzIGFuIGFkZGl0aW9uYWwKIHBlcm1pc3Npb24gdW5kZXIgc2VjdGlvbiA3IG9mIHRoZSBHTlUgR2VuZXJhbCBQdWJsaWMgTGljZW5zZSwgdmVyc2lvbgogMyAoIkdQTHYzIikuIEl0IGFwcGxpZXMgdG8gYSBnaXZlbiBmaWxlICh0aGUgIlJ1bnRpbWUgTGlicmFyeSIpIHRoYXQKIGJlYXJzIGEgbm90aWNlIHBsYWNlZCBieSB0aGUgY29weXJpZ2h0IGhvbGRlciBvZiB0aGUgZmlsZSBzdGF0aW5nIHRoYXQKIHRoZSBmaWxlIGlzIGdvdmVybmVkIGJ5IEdQTHYzIGFsb25nIHdpdGggdGhpcyBFeGNlcHRpb24uCgogV2hlbiB5b3UgdXNlIEdDQyB0byBjb21waWxlIGEgcHJvZ3JhbSwgR0NDIG1heSBjb21iaW5lIHBvcnRpb25zIG9mCiBjZXJ0YWluIEdDQyBoZWFkZXIgZmlsZXMgYW5kIHJ1bnRpbWUgbGlicmFyaWVzIHdpdGggdGhlIGNvbXBpbGVkCiBwcm9ncmFtLiBUaGUgcHVycG9zZSBvZiB0aGlzIEV4Y2VwdGlvbiBpcyB0byBhbGxvdyBjb21waWxhdGlvbiBvZgogbm9uLUdQTCAoaW5jbHVkaW5nIHByb3ByaWV0YXJ5KSBwcm9ncmFtcyB0byB1c2UsIGluIHRoaXMgd2F5LCB0aGUKIGhlYWRlciBmaWxlcyBhbmQgcnVudGltZSBsaWJyYXJpZXMgY292ZXJlZCBieSB0aGlzIEV4Y2VwdGlvbi4KCiAwLiBEZWZpbml0aW9ucy4KCiBBIGZpbGUgaXMgYW4gIkluZGVwZW5kZW50IE1vZHVsZSIgaWYgaXQgZWl0aGVyIHJlcXVpcmVzIHRoZSBSdW50aW1lCiBMaWJyYXJ5IGZvciBleGVjdXRpb24gYWZ0ZXIgYSBDb21waWxhdGlvbiBQcm9jZXNzLCBvciBtYWtlcyB1c2Ugb2YgYW4KIGludGVyZmFjZSBwcm92aWRlZCBieSB0aGUgUnVudGltZSBMaWJyYXJ5LCBidXQgaXMgbm90IG90aGVyd2lzZSBiYXNlZAogb24gdGhlIFJ1bnRpbWUgTGlicmFyeS4KCiAiR0NDIiBtZWFucyBhIHZlcnNpb24gb2YgdGhlIEdOVSBDb21waWxlciBDb2xsZWN0aW9uLCB3aXRoIG9yIHdpdGhvdXQKIG1vZGlmaWNhdGlvbnMsIGdvdmVybmVkIGJ5IHZlcnNpb24gMyAob3IgYSBzcGVjaWZpZWQgbGF0ZXIgdmVyc2lvbikgb2YKIHRoZSBHTlUgR2VuZXJhbCBQdWJsaWMgTGljZW5zZSAoR1BMKSB3aXRoIHRoZSBvcHRpb24gb2YgdXNpbmcgYW55CiBzdWJzZXF1ZW50IHZlcnNpb25zIHB1Ymxpc2hlZCBieSB0aGUgRlNGLgoKICJHUEwtY29tcGF0aWJsZSBTb2Z0d2FyZSIgaXMgc29mdHdhcmUgd2hvc2UgY29uZGl0aW9ucyBvZiBwcm9wYWdhdGlvbiwKIG1vZGlmaWNhdGlvbiBhbmQgdXNlIHdvdWxkIHBlcm1pdCBjb21iaW5hdGlvbiB3aXRoIEdDQyBpbiBhY2NvcmQgd2l0aAogdGhlIGxpY2Vuc2Ugb2YgR0NDLgoKICJUYXJnZXQgQ29kZSIgcmVmZXJzIHRvIG91dHB1dCBmcm9tIGFueSBjb21waWxlciBmb3IgYSByZWFsIG9yIHZpcnR1YWwKIHRhcmdldCBwcm9jZXNzb3IgYXJjaGl0ZWN0dXJlLCBpbiBleGVjdXRhYmxlIGZvcm0gb3Igc3VpdGFibGUgZm9yCiBpbnB1dCB0byBhbiBhc3NlbWJsZXIsIGxvYWRlciwgbGlua2VyIGFuZC9vciBleGVjdXRpb24KIHBoYXNlLiBOb3R3aXRoc3RhbmRpbmcgdGhhdCwgVGFyZ2V0IENvZGUgZG9lcyBub3QgaW5jbHVkZSBkYXRhIGluIGFueQogZm9ybWF0IHRoYXQgaXMgdXNlZCBhcyBhIGNvbXBpbGVyIGludGVybWVkaWF0ZSByZXByZXNlbnRhdGlvbiwgb3IgdXNlZAogZm9yIHByb2R1Y2luZyBhIGNvbXBpbGVyIGludGVybWVkaWF0ZSByZXByZXNlbnRhdGlvbi4KCiBUaGUgIkNvbXBpbGF0aW9uIFByb2Nlc3MiIHRyYW5zZm9ybXMgY29kZSBlbnRpcmVseSByZXByZXNlbnRlZCBpbgogbm9uLWludGVybWVkaWF0ZSBsYW5ndWFnZXMgZGVzaWduZWQgZm9yIGh1bWFuLXdyaXR0ZW4gY29kZSwgYW5kL29yIGluCiBKYXZhIFZpcnR1YWwgTWFjaGluZSBieXRlIGNvZGUsIGludG8gVGFyZ2V0IENvZGUuIFRodXMsIGZvciBleGFtcGxlLAogdXNlIG9mIHNvdXJjZSBjb2RlIGdlbmVyYXRvcnMgYW5kIHByZXByb2Nlc3NvcnMgbmVlZCBub3QgYmUgY29uc2lkZXJlZAogcGFydCBvZiB0aGUgQ29tcGlsYXRpb24gUHJvY2Vzcywgc2luY2UgdGhlIENvbXBpbGF0aW9uIFByb2Nlc3MgY2FuIGJlCiB1bmRlcnN0b29kIGFzIHN0YXJ0aW5nIHdpdGggdGhlIG91dHB1dCBvZiB0aGUgZ2VuZXJhdG9ycyBvcgogcHJlcHJvY2Vzc29ycy4KCiBBIENvbXBpbGF0aW9uIFByb2Nlc3MgaXMgIkVsaWdpYmxlIiBpZiBpdCBpcyBkb25lIHVzaW5nIEdDQywgYWxvbmUgb3IKIHdpdGggb3RoZXIgR1BMLWNvbXBhdGlibGUgc29mdHdhcmUsIG9yIGlmIGl0IGlzIGRvbmUgd2l0aG91dCB1c2luZyBhbnkKIHdvcmsgYmFzZWQgb24gR0NDLiBGb3IgZXhhbXBsZSwgdXNpbmcgbm9uLUdQTC1jb21wYXRpYmxlIFNvZnR3YXJlIHRvCiBvcHRpbWl6ZSBhbnkgR0NDIGludGVybWVkaWF0ZSByZXByZXNlbnRhdGlvbnMgd291bGQgbm90IHF1YWxpZnkgYXMgYW4KIEVsaWdpYmxlIENvbXBpbGF0aW9uIFByb2Nlc3MuCgogMS4gR3JhbnQgb2YgQWRkaXRpb25hbCBQZXJtaXNzaW9uLgoKIFlvdSBoYXZlIHBlcm1pc3Npb24gdG8gcHJvcGFnYXRlIGEgd29yayBvZiBUYXJnZXQgQ29kZSBmb3JtZWQgYnkKIGNvbWJpbmluZyB0aGUgUnVudGltZSBMaWJyYXJ5IHdpdGggSW5kZXBlbmRlbnQgTW9kdWxlcywgZXZlbiBpZiBzdWNoCiBwcm9wYWdhdGlvbiB3b3VsZCBvdGhlcndpc2UgdmlvbGF0ZSB0aGUgdGVybXMgb2YgR1BMdjMsIHByb3ZpZGVkIHRoYXQKIGFsbCBUYXJnZXQgQ29kZSB3YXMgZ2VuZXJhdGVkIGJ5IEVsaWdpYmxlIENvbXBpbGF0aW9uIFByb2Nlc3Nlcy4gWW91CiBtYXkgdGhlbiBjb252ZXkgc3VjaCBhIGNvbWJpbmF0aW9uIHVuZGVyIHRlcm1zIG9mIHlvdXIgY2hvaWNlLAogY29uc2lzdGVudCB3aXRoIHRoZSBsaWNlbnNpbmcgb2YgdGhlIEluZGVwZW5kZW50IE1vZHVsZXMuCgogMi4gTm8gV2Vha2VuaW5nIG9mIEdDQyBDb3B5bGVmdC4KCiBUaGUgYXZhaWxhYmlsaXR5IG9mIHRoaXMgRXhjZXB0aW9uIGRvZXMgbm90IGltcGx5IGFueSBnZW5lcmFsCiBwcmVzdW1wdGlvbiB0aGF0IHRoaXJkLXBhcnR5IHNvZnR3YXJlIGlzIHVuYWZmZWN0ZWQgYnkgdGhlIGNvcHlsZWZ0CiByZXF1aXJlbWVudHMgb2YgdGhlIGxpY2Vuc2Ugb2YgR0NDLgoKIC0tLS0KCiAgICAgICAgICAgICAgICAgICAgIEdOVSBHRU5FUkFMIFBVQkxJQyBMSUNFTlNFCiAgICAgICAgICAgICAgICAgICAgICAgIFZlcnNpb24gMywgMjkgSnVuZSAyMDA3CgogIENvcHlyaWdodCAoQykgMjAwNyBGcmVlIFNvZnR3YXJlIEZvdW5kYXRpb24sIEluYy4gPGh0dHA6Ly9mc2Yub3JnLz4KICBFdmVyeW9uZSBpcyBwZXJtaXR0ZWQgdG8gY29weSBhbmQgZGlzdHJpYnV0ZSB2ZXJiYXRpbSBjb3BpZXMKICBvZiB0aGlzIGxpY2Vuc2UgZG9jdW1lbnQsIGJ1dCBjaGFuZ2luZyBpdCBpcyBub3QgYWxsb3dlZC4KCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgUHJlYW1ibGUKCiAgIFRoZSBHTlUgR2VuZXJhbCBQdWJsaWMgTGljZW5zZSBpcyBhIGZyZWUsIGNvcHlsZWZ0IGxpY2Vuc2UgZm9yCiBzb2Z0d2FyZSBhbmQgb3RoZXIga2luZHMgb2Ygd29ya3MuCgogICBUaGUgbGljZW5zZXMgZm9yIG1vc3Qgc29mdHdhcmUgYW5kIG90aGVyIHByYWN0aWNhbCB3b3JrcyBhcmUgZGVzaWduZWQKIHRvIHRha2UgYXdheSB5b3VyIGZyZWVkb20gdG8gc2hhcmUgYW5kIGNoYW5nZSB0aGUgd29ya3MuICBCeSBjb250cmFzdCwKIHRoZSBHTlUgR2VuZXJhbCBQdWJsaWMgTGljZW5zZSBpcyBpbnRlbmRlZCB0byBndWFyYW50ZWUgeW91ciBmcmVlZG9tIHRvCiBzaGFyZSBhbmQgY2hhbmdlIGFsbCB2ZXJzaW9ucyBvZiBhIHByb2dyYW0tLXRvIG1ha2Ugc3VyZSBpdCByZW1haW5zIGZyZWUKIHNvZnR3YXJlIGZvciBhbGwgaXRzIHVzZXJzLiAgV2UsIHRoZSBGcmVlIFNvZnR3YXJlIEZvdW5kYXRpb24sIHVzZSB0aGUKIEdOVSBHZW5lcmFsIFB1YmxpYyBMaWNlbnNlIGZvciBtb3N0IG9mIG91ciBzb2Z0d2FyZTsgaXQgYXBwbGllcyBhbHNvIHRvCiBhbnkgb3RoZXIgd29yayByZWxlYXNlZCB0aGlzIHdheSBieSBpdHMgYXV0aG9ycy4gIFlvdSBjYW4gYXBwbHkgaXQgdG8KIHlvdXIgcHJvZ3JhbXMsIHRvby4KCiAgIFdoZW4gd2Ugc3BlYWsgb2YgZnJlZSBzb2Z0d2FyZSwgd2UgYXJlIHJlZmVycmluZyB0byBmcmVlZG9tLCBub3QKIHByaWNlLiAgT3VyIEdlbmVyYWwgUHVibGljIExpY2Vuc2VzIGFyZSBkZXNpZ25lZCB0byBtYWtlIHN1cmUgdGhhdCB5b3UKIGhhdmUgdGhlIGZyZWVkb20gdG8gZGlzdHJpYnV0ZSBjb3BpZXMgb2YgZnJlZSBzb2Z0d2FyZSAoYW5kIGNoYXJnZSBmb3IKIHRoZW0gaWYgeW91IHdpc2gpLCB0aGF0IHlvdSByZWNlaXZlIHNvdXJjZSBjb2RlIG9yIGNhbiBnZXQgaXQgaWYgeW91CiB3YW50IGl0LCB0aGF0IHlvdSBjYW4gY2hhbmdlIHRoZSBzb2Z0d2FyZSBvciB1c2UgcGllY2VzIG9mIGl0IGluIG5ldwogZnJlZSBwcm9ncmFtcywgYW5kIHRoYXQgeW91IGtub3cgeW91IGNhbiBkbyB0aGVzZSB0aGluZ3MuCgogICBUbyBwcm90ZWN0IHlvdXIgcmlnaHRzLCB3ZSBuZWVkIHRvIHByZXZlbnQgb3RoZXJzIGZyb20gZGVueWluZyB5b3UKIHRoZXNlIHJpZ2h0cyBvciBhc2tpbmcgeW91IHRvIHN1cnJlbmRlciB0aGUgcmlnaHRzLiAgVGhlcmVmb3JlLCB5b3UgaGF2ZQogY2VydGFpbiByZXNwb25zaWJpbGl0aWVzIGlmIHlvdSBkaXN0cmlidXRlIGNvcGllcyBvZiB0aGUgc29mdHdhcmUsIG9yIGlmCiB5b3UgbW9kaWZ5IGl0OiByZXNwb25zaWJpbGl0aWVzIHRvIHJlc3BlY3QgdGhlIGZyZWVkb20gb2Ygb3RoZXJzLgoKICAgRm9yIGV4YW1wbGUsIGlmIHlvdSBkaXN0cmlidXRlIGNvcGllcyBvZiBzdWNoIGEgcHJvZ3JhbSwgd2hldGhlcgogZ3JhdGlzIG9yIGZvciBhIGZlZSwgeW91IG11c3QgcGFzcyBvbiB0byB0aGUgcmVjaXBpZW50cyB0aGUgc2FtZQogZnJlZWRvbXMgdGhhdCB5b3UgcmVjZWl2ZWQuICBZb3UgbXVzdCBtYWtlIHN1cmUgdGhhdCB0aGV5LCB0b28sIHJlY2VpdmUKIG9yIGNhbiBnZXQgdGhlIHNvdXJjZSBjb2RlLiAgQW5kIHlvdSBtdXN0IHNob3cgdGhlbSB0aGVzZSB0ZXJtcyBzbyB0aGV5CiBrbm93IHRoZWlyIHJpZ2h0cy4KCiAgIERldmVsb3BlcnMgdGhhdCB1c2UgdGhlIEdOVSBHUEwgcHJvdGVjdCB5b3VyIHJpZ2h0cyB3aXRoIHR3byBzdGVwczoKICgxKSBhc3NlcnQgY29weXJpZ2h0IG9uIHRoZSBzb2Z0d2FyZSwgYW5kICgyKSBvZmZlciB5b3UgdGhpcyBMaWNlbnNlCiBnaXZpbmcgeW91IGxlZ2FsIHBlcm1pc3Npb24gdG8gY29weSwgZGlzdHJpYnV0ZSBhbmQvb3IgbW9kaWZ5IGl0LgoKICAgRm9yIHRoZSBkZXZlbG9wZXJzJyBhbmQgYXV0aG9ycycgcHJvdGVjdGlvbiwgdGhlIEdQTCBjbGVhcmx5IGV4cGxhaW5zCiB0aGF0IHRoZXJlIGlzIG5vIHdhcnJhbnR5IGZvciB0aGlzIGZyZWUgc29mdHdhcmUuICBGb3IgYm90aCB1c2VycycgYW5kCiBhdXRob3JzJyBzYWtlLCB0aGUgR1BMIHJlcXVpcmVzIHRoYXQgbW9kaWZpZWQgdmVyc2lvbnMgYmUgbWFya2VkIGFzCiBjaGFuZ2VkLCBzbyB0aGF0IHRoZWlyIHByb2JsZW1zIHdpbGwgbm90IGJlIGF0dHJpYnV0ZWQgZXJyb25lb3VzbHkgdG8KIGF1dGhvcnMgb2YgcHJldmlvdXMgdmVyc2lvbnMuCgogICBTb21lIGRldmljZXMgYXJlIGRlc2lnbmVkIHRvIGRlbnkgdXNlcnMgYWNjZXNzIHRvIGluc3RhbGwgb3IgcnVuCiBtb2RpZmllZCB2ZXJzaW9ucyBvZiB0aGUgc29mdHdhcmUgaW5zaWRlIHRoZW0sIGFsdGhvdWdoIHRoZSBtYW51ZmFjdHVyZXIKIGNhbiBkbyBzby4gIFRoaXMgaXMgZnVuZGFtZW50YWxseSBpbmNvbXBhdGlibGUgd2l0aCB0aGUgYWltIG9mCiBwcm90ZWN0aW5nIHVzZXJzJyBmcmVlZG9tIHRvIGNoYW5nZSB0aGUgc29mdHdhcmUuICBUaGUgc3lzdGVtYXRpYwogcGF0dGVybiBvZiBzdWNoIGFidXNlIG9jY3VycyBpbiB0aGUgYXJlYSBvZiBwcm9kdWN0cyBmb3IgaW5kaXZpZHVhbHMgdG8KIHVzZSwgd2hpY2ggaXMgcHJlY2lzZWx5IHdoZXJlIGl0IGlzIG1vc3QgdW5hY2NlcHRhYmxlLiAgVGhlcmVmb3JlLCB3ZQogaGF2ZSBkZXNpZ25lZCB0aGlzIHZlcnNpb24gb2YgdGhlIEdQTCB0byBwcm9oaWJpdCB0aGUgcHJhY3RpY2UgZm9yIHRob3NlCiBwcm9kdWN0cy4gIElmIHN1Y2ggcHJvYmxlbXMgYXJpc2Ugc3Vic3RhbnRpYWxseSBpbiBvdGhlciBkb21haW5zLCB3ZQogc3RhbmQgcmVhZHkgdG8gZXh0ZW5kIHRoaXMgcHJvdmlzaW9uIHRvIHRob3NlIGRvbWFpbnMgaW4gZnV0dXJlIHZlcnNpb25zCiBvZiB0aGUgR1BMLCBhcyBuZWVkZWQgdG8gcHJvdGVjdCB0aGUgZnJlZWRvbSBvZiB1c2Vycy4KCiAgIEZpbmFsbHksIGV2ZXJ5IHByb2dyYW0gaXMgdGhyZWF0ZW5lZCBjb25zdGFudGx5IGJ5IHNvZnR3YXJlIHBhdGVudHMuCiBTdGF0ZXMgc2hvdWxkIG5vdCBhbGxvdyBwYXRlbnRzIHRvIHJlc3RyaWN0IGRldmVsb3BtZW50IGFuZCB1c2Ugb2YKIHNvZnR3YXJlIG9uIGdlbmVyYWwtcHVycG9zZSBjb21wdXRlcnMsIGJ1dCBpbiB0aG9zZSB0aGF0IGRvLCB3ZSB3aXNoIHRvCiBhdm9pZCB0aGUgc3BlY2lhbCBkYW5nZXIgdGhhdCBwYXRlbnRzIGFwcGxpZWQgdG8gYSBmcmVlIHByb2dyYW0gY291bGQKIG1ha2UgaXQgZWZmZWN0aXZlbHkgcHJvcHJpZXRhcnkuICBUbyBwcmV2ZW50IHRoaXMsIHRoZSBHUEwgYXNzdXJlcyB0aGF0CiBwYXRlbnRzIGNhbm5vdCBiZSB1c2VkIHRvIHJlbmRlciB0aGUgcHJvZ3JhbSBub24tZnJlZS4KCiAgIFRoZSBwcmVjaXNlIHRlcm1zIGFuZCBjb25kaXRpb25zIGZvciBjb3B5aW5nLCBkaXN0cmlidXRpb24gYW5kCiBtb2RpZmljYXRpb24gZm9sbG93LgoKICAgICAgICAgICAgICAgICAgICAgICAgVEVSTVMgQU5EIENPTkRJVElPTlMKCiAgIDAuIERlZmluaXRpb25zLgoKICAgIlRoaXMgTGljZW5zZSIgcmVmZXJzIHRvIHZlcnNpb24gMyBvZiB0aGUgR05VIEdlbmVyYWwgUHVibGljIExpY2Vuc2UuCgogICAiQ29weXJpZ2h0IiBhbHNvIG1lYW5zIGNvcHlyaWdodC1saWtlIGxhd3MgdGhhdCBhcHBseSB0byBvdGhlciBraW5kcyBvZgogd29ya3MsIHN1Y2ggYXMgc2VtaWNvbmR1Y3RvciBtYXNrcy4KCiAgICJUaGUgUHJvZ3JhbSIgcmVmZXJzIHRvIGFueSBjb3B5cmlnaHRhYmxlIHdvcmsgbGljZW5zZWQgdW5kZXIgdGhpcwogTGljZW5zZS4gIEVhY2ggbGljZW5zZWUgaXMgYWRkcmVzc2VkIGFzICJ5b3UiLiAgIkxpY2Vuc2VlcyIgYW5kCiAicmVjaXBpZW50cyIgbWF5IGJlIGluZGl2aWR1YWxzIG9yIG9yZ2FuaXphdGlvbnMuCgogICBUbyAibW9kaWZ5IiBhIHdvcmsgbWVhbnMgdG8gY29weSBmcm9tIG9yIGFkYXB0IGFsbCBvciBwYXJ0IG9mIHRoZSB3b3JrCiBpbiBhIGZhc2hpb24gcmVxdWlyaW5nIGNvcHlyaWdodCBwZXJtaXNzaW9uLCBvdGhlciB0aGFuIHRoZSBtYWtpbmcgb2YgYW4KIGV4YWN0IGNvcHkuICBUaGUgcmVzdWx0aW5nIHdvcmsgaXMgY2FsbGVkIGEgIm1vZGlmaWVkIHZlcnNpb24iIG9mIHRoZQogZWFybGllciB3b3JrIG9yIGEgd29yayAiYmFzZWQgb24iIHRoZSBlYXJsaWVyIHdvcmsuCgogICBBICJjb3ZlcmVkIHdvcmsiIG1lYW5zIGVpdGhlciB0aGUgdW5tb2RpZmllZCBQcm9ncmFtIG9yIGEgd29yayBiYXNlZAogb24gdGhlIFByb2dyYW0uCgogICBUbyAicHJvcGFnYXRlIiBhIHdvcmsgbWVhbnMgdG8gZG8gYW55dGhpbmcgd2l0aCBpdCB0aGF0LCB3aXRob3V0CiBwZXJtaXNzaW9uLCB3b3VsZCBtYWtlIHlvdSBkaXJlY3RseSBvciBzZWNvbmRhcmlseSBsaWFibGUgZm9yCiBpbmZyaW5nZW1lbnQgdW5kZXIgYXBwbGljYWJsZSBjb3B5cmlnaHQgbGF3LCBleGNlcHQgZXhlY3V0aW5nIGl0IG9uIGEKIGNvbXB1dGVyIG9yIG1vZGlmeWluZyBhIHByaXZhdGUgY29weS4gIFByb3BhZ2F0aW9uIGluY2x1ZGVzIGNvcHlpbmcsCiBkaXN0cmlidXRpb24gKHdpdGggb3Igd2l0aG91dCBtb2RpZmljYXRpb24pLCBtYWtpbmcgYXZhaWxhYmxlIHRvIHRoZQogcHVibGljLCBhbmQgaW4gc29tZSBjb3VudHJpZXMgb3RoZXIgYWN0aXZpdGllcyBhcyB3ZWxsLgoKICAgVG8gImNvbnZleSIgYSB3b3JrIG1lYW5zIGFueSBraW5kIG9mIHByb3BhZ2F0aW9uIHRoYXQgZW5hYmxlcyBvdGhlcgogcGFydGllcyB0byBtYWtlIG9yIHJlY2VpdmUgY29waWVzLiAgTWVyZSBpbnRlcmFjdGlvbiB3aXRoIGEgdXNlciB0aHJvdWdoCiBhIGNvbXB1dGVyIG5ldHdvcmssIHdpdGggbm8gdHJhbnNmZXIgb2YgYSBjb3B5LCBpcyBub3QgY29udmV5aW5nLgoKICAgQW4gaW50ZXJhY3RpdmUgdXNlciBpbnRlcmZhY2UgZGlzcGxheXMgIkFwcHJvcHJpYXRlIExlZ2FsIE5vdGljZXMiCiB0byB0aGUgZXh0ZW50IHRoYXQgaXQgaW5jbHVkZXMgYSBjb252ZW5pZW50IGFuZCBwcm9taW5lbnRseSB2aXNpYmxlCiBmZWF0dXJlIHRoYXQgKDEpIGRpc3BsYXlzIGFuIGFwcHJvcHJpYXRlIGNvcHlyaWdodCBub3RpY2UsIGFuZCAoMikKIHRlbGxzIHRoZSB1c2VyIHRoYXQgdGhlcmUgaXMgbm8gd2FycmFudHkgZm9yIHRoZSB3b3JrIChleGNlcHQgdG8gdGhlCiBleHRlbnQgdGhhdCB3YXJyYW50aWVzIGFyZSBwcm92aWRlZCksIHRoYXQgbGljZW5zZWVzIG1heSBjb252ZXkgdGhlCiB3b3JrIHVuZGVyIHRoaXMgTGljZW5zZSwgYW5kIGhvdyB0byB2aWV3IGEgY29weSBvZiB0aGlzIExpY2Vuc2UuICBJZgogdGhlIGludGVyZmFjZSBwcmVzZW50cyBhIGxpc3Qgb2YgdXNlciBjb21tYW5kcyBvciBvcHRpb25zLCBzdWNoIGFzIGEKIG1lbnUsIGEgcHJvbWluZW50IGl0ZW0gaW4gdGhlIGxpc3QgbWVldHMgdGhpcyBjcml0ZXJpb24uCgogICAxLiBTb3VyY2UgQ29kZS4KCiAgIFRoZSAic291cmNlIGNvZGUiIGZvciBhIHdvcmsgbWVhbnMgdGhlIHByZWZlcnJlZCBmb3JtIG9mIHRoZSB3b3JrCiBmb3IgbWFraW5nIG1vZGlmaWNhdGlvbnMgdG8gaXQuICAiT2JqZWN0IGNvZGUiIG1lYW5zIGFueSBub24tc291cmNlCiBmb3JtIG9mIGEgd29yay4KCiAgIEEgIlN0YW5kYXJkIEludGVyZmFjZSIgbWVhbnMgYW4gaW50ZXJmYWNlIHRoYXQgZWl0aGVyIGlzIGFuIG9mZmljaWFsCiBzdGFuZGFyZCBkZWZpbmVkIGJ5IGEgcmVjb2duaXplZCBzdGFuZGFyZHMgYm9keSwgb3IsIGluIHRoZSBjYXNlIG9mCiBpbnRlcmZhY2VzIHNwZWNpZmllZCBmb3IgYSBwYXJ0aWN1bGFyIHByb2dyYW1taW5nIGxhbmd1YWdlLCBvbmUgdGhhdAogaXMgd2lkZWx5IHVzZWQgYW1vbmcgZGV2ZWxvcGVycyB3b3JraW5nIGluIHRoYXQgbGFuZ3VhZ2UuCgogICBUaGUgIlN5c3RlbSBMaWJyYXJpZXMiIG9mIGFuIGV4ZWN1dGFibGUgd29yayBpbmNsdWRlIGFueXRoaW5nLCBvdGhlcgogdGhhbiB0aGUgd29yayBhcyBhIHdob2xlLCB0aGF0IChhKSBpcyBpbmNsdWRlZCBpbiB0aGUgbm9ybWFsIGZvcm0gb2YKIHBhY2thZ2luZyBhIE1ham9yIENvbXBvbmVudCwgYnV0IHdoaWNoIGlzIG5vdCBwYXJ0IG9mIHRoYXQgTWFqb3IKIENvbXBvbmVudCwgYW5kIChiKSBzZXJ2ZXMgb25seSB0byBlbmFibGUgdXNlIG9mIHRoZSB3b3JrIHdpdGggdGhhdAogTWFqb3IgQ29tcG9uZW50LCBvciB0byBpbXBsZW1lbnQgYSBTdGFuZGFyZCBJbnRlcmZhY2UgZm9yIHdoaWNoIGFuCiBpbXBsZW1lbnRhdGlvbiBpcyBhdmFpbGFibGUgdG8gdGhlIHB1YmxpYyBpbiBzb3VyY2UgY29kZSBmb3JtLiAgQQogIk1ham9yIENvbXBvbmVudCIsIGluIHRoaXMgY29udGV4dCwgbWVhbnMgYSBtYWpvciBlc3NlbnRpYWwgY29tcG9uZW50CiAoa2VybmVsLCB3aW5kb3cgc3lzdGVtLCBhbmQgc28gb24pIG9mIHRoZSBzcGVjaWZpYyBvcGVyYXRpbmcgc3lzdGVtCiAoaWYgYW55KSBvbiB3aGljaCB0aGUgZXhlY3V0YWJsZSB3b3JrIHJ1bnMsIG9yIGEgY29tcGlsZXIgdXNlZCB0bwogcHJvZHVjZSB0aGUgd29yaywgb3IgYW4gb2JqZWN0IGNvZGUgaW50ZXJwcmV0ZXIgdXNlZCB0byBydW4gaXQuCgogICBUaGUgIkNvcnJlc3BvbmRpbmcgU291cmNlIiBmb3IgYSB3b3JrIGluIG9iamVjdCBjb2RlIGZvcm0gbWVhbnMgYWxsCiB0aGUgc291cmNlIGNvZGUgbmVlZGVkIHRvIGdlbmVyYXRlLCBpbnN0YWxsLCBhbmQgKGZvciBhbiBleGVjdXRhYmxlCiB3b3JrKSBydW4gdGhlIG9iamVjdCBjb2RlIGFuZCB0byBtb2RpZnkgdGhlIHdvcmssIGluY2x1ZGluZyBzY3JpcHRzIHRvCiBjb250cm9sIHRob3NlIGFjdGl2aXRpZXMuICBIb3dldmVyLCBpdCBkb2VzIG5vdCBpbmNsdWRlIHRoZSB3b3JrJ3MKIFN5c3RlbSBMaWJyYXJpZXMsIG9yIGdlbmVyYWwtcHVycG9zZSB0b29scyBvciBnZW5lcmFsbHkgYXZhaWxhYmxlIGZyZWUKIHByb2dyYW1zIHdoaWNoIGFyZSB1c2VkIHVubW9kaWZpZWQgaW4gcGVyZm9ybWluZyB0aG9zZSBhY3Rpdml0aWVzIGJ1dAogd2hpY2ggYXJlIG5vdCBwYXJ0IG9mIHRoZSB3b3JrLiAgRm9yIGV4YW1wbGUsIENvcnJlc3BvbmRpbmcgU291cmNlCiBpbmNsdWRlcyBpbnRlcmZhY2UgZGVmaW5pdGlvbiBmaWxlcyBhc3NvY2lhdGVkIHdpdGggc291cmNlIGZpbGVzIGZvcgogdGhlIHdvcmssIGFuZCB0aGUgc291cmNlIGNvZGUgZm9yIHNoYXJlZCBsaWJyYXJpZXMgYW5kIGR5bmFtaWNhbGx5CiBsaW5rZWQgc3VicHJvZ3JhbXMgdGhhdCB0aGUgd29yayBpcyBzcGVjaWZpY2FsbHkgZGVzaWduZWQgdG8gcmVxdWlyZSwKIHN1Y2ggYXMgYnkgaW50aW1hdGUgZGF0YSBjb21tdW5pY2F0aW9uIG9yIGNvbnRyb2wgZmxvdyBiZXR3ZWVuIHRob3NlCiBzdWJwcm9ncmFtcyBhbmQgb3RoZXIgcGFydHMgb2YgdGhlIHdvcmsuCgogICBUaGUgQ29ycmVzcG9uZGluZyBTb3VyY2UgbmVlZCBub3QgaW5jbHVkZSBhbnl0aGluZyB0aGF0IHVzZXJzCiBjYW4gcmVnZW5lcmF0ZSBhdXRvbWF0aWNhbGx5IGZyb20gb3RoZXIgcGFydHMgb2YgdGhlIENvcnJlc3BvbmRpbmcKIFNvdXJjZS4KCiAgIFRoZSBDb3JyZXNwb25kaW5nIFNvdXJjZSBmb3IgYSB3b3JrIGluIHNvdXJjZSBjb2RlIGZvcm0gaXMgdGhhdAogc2FtZSB3b3JrLgoKICAgMi4gQmFzaWMgUGVybWlzc2lvbnMuCgogICBBbGwgcmlnaHRzIGdyYW50ZWQgdW5kZXIgdGhpcyBMaWNlbnNlIGFyZSBncmFudGVkIGZvciB0aGUgdGVybSBvZgogY29weXJpZ2h0IG9uIHRoZSBQcm9ncmFtLCBhbmQgYXJlIGlycmV2b2NhYmxlIHByb3ZpZGVkIHRoZSBzdGF0ZWQKIGNvbmRpdGlvbnMgYXJlIG1ldC4gIFRoaXMgTGljZW5zZSBleHBsaWNpdGx5IGFmZmlybXMgeW91ciB1bmxpbWl0ZWQKIHBlcm1pc3Npb24gdG8gcnVuIHRoZSB1bm1vZGlmaWVkIFByb2dyYW0uICBUaGUgb3V0cHV0IGZyb20gcnVubmluZyBhCiBjb3ZlcmVkIHdvcmsgaXMgY292ZXJlZCBieSB0aGlzIExpY2Vuc2Ugb25seSBpZiB0aGUgb3V0cHV0LCBnaXZlbiBpdHMKIGNvbnRlbnQsIGNvbnN0aXR1dGVzIGEgY292ZXJlZCB3b3JrLiAgVGhpcyBMaWNlbnNlIGFja25vd2xlZGdlcyB5b3VyCiByaWdodHMgb2YgZmFpciB1c2Ugb3Igb3RoZXIgZXF1aXZhbGVudCwgYXMgcHJvdmlkZWQgYnkgY29weXJpZ2h0IGxhdy4KCiAgIFlvdSBtYXkgbWFrZSwgcnVuIGFuZCBwcm9wYWdhdGUgY292ZXJlZCB3b3JrcyB0aGF0IHlvdSBkbyBub3QKIGNvbnZleSwgd2l0aG91dCBjb25kaXRpb25zIHNvIGxvbmcgYXMgeW91ciBsaWNlbnNlIG90aGVyd2lzZSByZW1haW5zCiBpbiBmb3JjZS4gIFlvdSBtYXkgY29udmV5IGNvdmVyZWQgd29ya3MgdG8gb3RoZXJzIGZvciB0aGUgc29sZSBwdXJwb3NlCiBvZiBoYXZpbmcgdGhlbSBtYWtlIG1vZGlmaWNhdGlvbnMgZXhjbHVzaXZlbHkgZm9yIHlvdSwgb3IgcHJvdmlkZSB5b3UKIHdpdGggZmFjaWxpdGllcyBmb3IgcnVubmluZyB0aG9zZSB3b3JrcywgcHJvdmlkZWQgdGhhdCB5b3UgY29tcGx5IHdpdGgKIHRoZSB0ZXJtcyBvZiB0aGlzIExpY2Vuc2UgaW4gY29udmV5aW5nIGFsbCBtYXRlcmlhbCBmb3Igd2hpY2ggeW91IGRvCiBub3QgY29udHJvbCBjb3B5cmlnaHQuICBUaG9zZSB0aHVzIG1ha2luZyBvciBydW5uaW5nIHRoZSBjb3ZlcmVkIHdvcmtzCiBmb3IgeW91IG11c3QgZG8gc28gZXhjbHVzaXZlbHkgb24geW91ciBiZWhhbGYsIHVuZGVyIHlvdXIgZGlyZWN0aW9uCiBhbmQgY29udHJvbCwgb24gdGVybXMgdGhhdCBwcm9oaWJpdCB0aGVtIGZyb20gbWFraW5nIGFueSBjb3BpZXMgb2YKIHlvdXIgY29weXJpZ2h0ZWQgbWF0ZXJpYWwgb3V0c2lkZSB0aGVpciByZWxhdGlvbnNoaXAgd2l0aCB5b3UuCgogICBDb252ZXlpbmcgdW5kZXIgYW55IG90aGVyIGNpcmN1bXN0YW5jZXMgaXMgcGVybWl0dGVkIHNvbGVseSB1bmRlcgogdGhlIGNvbmRpdGlvbnMgc3RhdGVkIGJlbG93LiAgU3VibGljZW5zaW5nIGlzIG5vdCBhbGxvd2VkOyBzZWN0aW9uIDEwCiBtYWtlcyBpdCB1bm5lY2Vzc2FyeS4KCiAgIDMuIFByb3RlY3RpbmcgVXNlcnMnIExlZ2FsIFJpZ2h0cyBGcm9tIEFudGktQ2lyY3VtdmVudGlvbiBMYXcuCgogICBObyBjb3ZlcmVkIHdvcmsgc2hhbGwgYmUgZGVlbWVkIHBhcnQgb2YgYW4gZWZmZWN0aXZlIHRlY2hub2xvZ2ljYWwKIG1lYXN1cmUgdW5kZXIgYW55IGFwcGxpY2FibGUgbGF3IGZ1bGZpbGxpbmcgb2JsaWdhdGlvbnMgdW5kZXIgYXJ0aWNsZQogMTEgb2YgdGhlIFdJUE8gY29weXJpZ2h0IHRyZWF0eSBhZG9wdGVkIG9uIDIwIERlY2VtYmVyIDE5OTYsIG9yCiBzaW1pbGFyIGxhd3MgcHJvaGliaXRpbmcgb3IgcmVzdHJpY3RpbmcgY2lyY3VtdmVudGlvbiBvZiBzdWNoCiBtZWFzdXJlcy4KCiAgIFdoZW4geW91IGNvbnZleSBhIGNvdmVyZWQgd29yaywgeW91IHdhaXZlIGFueSBsZWdhbCBwb3dlciB0byBmb3JiaWQKIGNpcmN1bXZlbnRpb24gb2YgdGVjaG5vbG9naWNhbCBtZWFzdXJlcyB0byB0aGUgZXh0ZW50IHN1Y2ggY2lyY3VtdmVudGlvbgogaXMgZWZmZWN0ZWQgYnkgZXhlcmNpc2luZyByaWdodHMgdW5kZXIgdGhpcyBMaWNlbnNlIHdpdGggcmVzcGVjdCB0bwogdGhlIGNvdmVyZWQgd29yaywgYW5kIHlvdSBkaXNjbGFpbSBhbnkgaW50ZW50aW9uIHRvIGxpbWl0IG9wZXJhdGlvbiBvcgogbW9kaWZpY2F0aW9uIG9mIHRoZSB3b3JrIGFzIGEgbWVhbnMgb2YgZW5mb3JjaW5nLCBhZ2FpbnN0IHRoZSB3b3JrJ3MKIHVzZXJzLCB5b3VyIG9yIHRoaXJkIHBhcnRpZXMnIGxlZ2FsIHJpZ2h0cyB0byBmb3JiaWQgY2lyY3VtdmVudGlvbiBvZgogdGVjaG5vbG9naWNhbCBtZWFzdXJlcy4KCiAgIDQuIENvbnZleWluZyBWZXJiYXRpbSBDb3BpZXMuCgogICBZb3UgbWF5IGNvbnZleSB2ZXJiYXRpbSBjb3BpZXMgb2YgdGhlIFByb2dyYW0ncyBzb3VyY2UgY29kZSBhcyB5b3UKIHJlY2VpdmUgaXQsIGluIGFueSBtZWRpdW0sIHByb3ZpZGVkIHRoYXQgeW91IGNvbnNwaWN1b3VzbHkgYW5kCiBhcHByb3ByaWF0ZWx5IHB1Ymxpc2ggb24gZWFjaCBjb3B5IGFuIGFwcHJvcHJpYXRlIGNvcHlyaWdodCBub3RpY2U7CiBrZWVwIGludGFjdCBhbGwgbm90aWNlcyBzdGF0aW5nIHRoYXQgdGhpcyBMaWNlbnNlIGFuZCBhbnkKIG5vbi1wZXJtaXNzaXZlIHRlcm1zIGFkZGVkIGluIGFjY29yZCB3aXRoIHNlY3Rpb24gNyBhcHBseSB0byB0aGUgY29kZTsKIGtlZXAgaW50YWN0IGFsbCBub3RpY2VzIG9mIHRoZSBhYnNlbmNlIG9mIGFueSB3YXJyYW50eTsgYW5kIGdpdmUgYWxsCiByZWNpcGllbnRzIGEgY29weSBvZiB0aGlzIExpY2Vuc2UgYWxvbmcgd2l0aCB0aGUgUHJvZ3JhbS4KCiAgIFlvdSBtYXkgY2hhcmdlIGFueSBwcmljZSBvciBubyBwcmljZSBmb3IgZWFjaCBjb3B5IHRoYXQgeW91IGNvbnZleSwKIGFuZCB5b3UgbWF5IG9mZmVyIHN1cHBvcnQgb3Igd2FycmFudHkgcHJvdGVjdGlvbiBmb3IgYSBmZWUuCgogICA1LiBDb252ZXlpbmcgTW9kaWZpZWQgU291cmNlIFZlcnNpb25zLgoKICAgWW91IG1heSBjb252ZXkgYSB3b3JrIGJhc2VkIG9uIHRoZSBQcm9ncmFtLCBvciB0aGUgbW9kaWZpY2F0aW9ucyB0bwogcHJvZHVjZSBpdCBmcm9tIHRoZSBQcm9ncmFtLCBpbiB0aGUgZm9ybSBvZiBzb3VyY2UgY29kZSB1bmRlciB0aGUKIHRlcm1zIG9mIHNlY3Rpb24gNCwgcHJvdmlkZWQgdGhhdCB5b3UgYWxzbyBtZWV0IGFsbCBvZiB0aGVzZSBjb25kaXRpb25zOgoKICAgICBhKSBUaGUgd29yayBtdXN0IGNhcnJ5IHByb21pbmVudCBub3RpY2VzIHN0YXRpbmcgdGhhdCB5b3UgbW9kaWZpZWQKICAgICBpdCwgYW5kIGdpdmluZyBhIHJlbGV2YW50IGRhdGUuCgogICAgIGIpIFRoZSB3b3JrIG11c3QgY2FycnkgcHJvbWluZW50IG5vdGljZXMgc3RhdGluZyB0aGF0IGl0IGlzCiAgICAgcmVsZWFzZWQgdW5kZXIgdGhpcyBMaWNlbnNlIGFuZCBhbnkgY29uZGl0aW9ucyBhZGRlZCB1bmRlciBzZWN0aW9uCiAgICAgNy4gIFRoaXMgcmVxdWlyZW1lbnQgbW9kaWZpZXMgdGhlIHJlcXVpcmVtZW50IGluIHNlY3Rpb24gNCB0bwogICAgICJrZWVwIGludGFjdCBhbGwgbm90aWNlcyIuCgogICAgIGMpIFlvdSBtdXN0IGxpY2Vuc2UgdGhlIGVudGlyZSB3b3JrLCBhcyBhIHdob2xlLCB1bmRlciB0aGlzCiAgICAgTGljZW5zZSB0byBhbnlvbmUgd2hvIGNvbWVzIGludG8gcG9zc2Vzc2lvbiBvZiBhIGNvcHkuICBUaGlzCiAgICAgTGljZW5zZSB3aWxsIHRoZXJlZm9yZSBhcHBseSwgYWxvbmcgd2l0aCBhbnkgYXBwbGljYWJsZSBzZWN0aW9uIDcKICAgICBhZGRpdGlvbmFsIHRlcm1zLCB0byB0aGUgd2hvbGUgb2YgdGhlIHdvcmssIGFuZCBhbGwgaXRzIHBhcnRzLAogICAgIHJlZ2FyZGxlc3Mgb2YgaG93IHRoZXkgYXJlIHBhY2thZ2VkLiAgVGhpcyBMaWNlbnNlIGdpdmVzIG5vCiAgICAgcGVybWlzc2lvbiB0byBsaWNlbnNlIHRoZSB3b3JrIGluIGFueSBvdGhlciB3YXksIGJ1dCBpdCBkb2VzIG5vdAogICAgIGludmFsaWRhdGUgc3VjaCBwZXJtaXNzaW9uIGlmIHlvdSBoYXZlIHNlcGFyYXRlbHkgcmVjZWl2ZWQgaXQuCgogICAgIGQpIElmIHRoZSB3b3JrIGhhcyBpbnRlcmFjdGl2ZSB1c2VyIGludGVyZmFjZXMsIGVhY2ggbXVzdCBkaXNwbGF5CiAgICAgQXBwcm9wcmlhdGUgTGVnYWwgTm90aWNlczsgaG93ZXZlciwgaWYgdGhlIFByb2dyYW0gaGFzIGludGVyYWN0aXZlCiAgICAgaW50ZXJmYWNlcyB0aGF0IGRvIG5vdCBkaXNwbGF5IEFwcHJvcHJpYXRlIExlZ2FsIE5vdGljZXMsIHlvdXIKICAgICB3b3JrIG5lZWQgbm90IG1ha2UgdGhlbSBkbyBzby4KCiAgIEEgY29tcGlsYXRpb24gb2YgYSBjb3ZlcmVkIHdvcmsgd2l0aCBvdGhlciBzZXBhcmF0ZSBhbmQgaW5kZXBlbmRlbnQKIHdvcmtzLCB3aGljaCBhcmUgbm90IGJ5IHRoZWlyIG5hdHVyZSBleHRlbnNpb25zIG9mIHRoZSBjb3ZlcmVkIHdvcmssCiBhbmQgd2hpY2ggYXJlIG5vdCBjb21iaW5lZCB3aXRoIGl0IHN1Y2ggYXMgdG8gZm9ybSBhIGxhcmdlciBwcm9ncmFtLAogaW4gb3Igb24gYSB2b2x1bWUgb2YgYSBzdG9yYWdlIG9yIGRpc3RyaWJ1dGlvbiBtZWRpdW0sIGlzIGNhbGxlZCBhbgogImFnZ3JlZ2F0ZSIgaWYgdGhlIGNvbXBpbGF0aW9uIGFuZCBpdHMgcmVzdWx0aW5nIGNvcHlyaWdodCBhcmUgbm90CiB1c2VkIHRvIGxpbWl0IHRoZSBhY2Nlc3Mgb3IgbGVnYWwgcmlnaHRzIG9mIHRoZSBjb21waWxhdGlvbidzIHVzZXJzCiBiZXlvbmQgd2hhdCB0aGUgaW5kaXZpZHVhbCB3b3JrcyBwZXJtaXQuICBJbmNsdXNpb24gb2YgYSBjb3ZlcmVkIHdvcmsKIGluIGFuIGFnZ3JlZ2F0ZSBkb2VzIG5vdCBjYXVzZSB0aGlzIExpY2Vuc2UgdG8gYXBwbHkgdG8gdGhlIG90aGVyCiBwYXJ0cyBvZiB0aGUgYWdncmVnYXRlLgoKICAgNi4gQ29udmV5aW5nIE5vbi1Tb3VyY2UgRm9ybXMuCgogICBZb3UgbWF5IGNvbnZleSBhIGNvdmVyZWQgd29yayBpbiBvYmplY3QgY29kZSBmb3JtIHVuZGVyIHRoZSB0ZXJtcwogb2Ygc2VjdGlvbnMgNCBhbmQgNSwgcHJvdmlkZWQgdGhhdCB5b3UgYWxzbyBjb252ZXkgdGhlCiBtYWNoaW5lLXJlYWRhYmxlIENvcnJlc3BvbmRpbmcgU291cmNlIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGlzIExpY2Vuc2UsCiBpbiBvbmUgb2YgdGhlc2Ugd2F5czoKCiAgICAgYSkgQ29udmV5IHRoZSBvYmplY3QgY29kZSBpbiwgb3IgZW1ib2RpZWQgaW4sIGEgcGh5c2ljYWwgcHJvZHVjdAogICAgIChpbmNsdWRpbmcgYSBwaHlzaWNhbCBkaXN0cmlidXRpb24gbWVkaXVtKSwgYWNjb21wYW5pZWQgYnkgdGhlCiAgICAgQ29ycmVzcG9uZGluZyBTb3VyY2UgZml4ZWQgb24gYSBkdXJhYmxlIHBoeXNpY2FsIG1lZGl1bQogICAgIGN1c3RvbWFyaWx5IHVzZWQgZm9yIHNvZnR3YXJlIGludGVyY2hhbmdlLgoKICAgICBiKSBDb252ZXkgdGhlIG9iamVjdCBjb2RlIGluLCBvciBlbWJvZGllZCBpbiwgYSBwaHlzaWNhbCBwcm9kdWN0CiAgICAgKGluY2x1ZGluZyBhIHBoeXNpY2FsIGRpc3RyaWJ1dGlvbiBtZWRpdW0pLCBhY2NvbXBhbmllZCBieSBhCiAgICAgd3JpdHRlbiBvZmZlciwgdmFsaWQgZm9yIGF0IGxlYXN0IHRocmVlIHllYXJzIGFuZCB2YWxpZCBmb3IgYXMKICAgICBsb25nIGFzIHlvdSBvZmZlciBzcGFyZSBwYXJ0cyBvciBjdXN0b21lciBzdXBwb3J0IGZvciB0aGF0IHByb2R1Y3QKICAgICBtb2RlbCwgdG8gZ2l2ZSBhbnlvbmUgd2hvIHBvc3Nlc3NlcyB0aGUgb2JqZWN0IGNvZGUgZWl0aGVyICgxKSBhCiAgICAgY29weSBvZiB0aGUgQ29ycmVzcG9uZGluZyBTb3VyY2UgZm9yIGFsbCB0aGUgc29mdHdhcmUgaW4gdGhlCiAgICAgcHJvZHVjdCB0aGF0IGlzIGNvdmVyZWQgYnkgdGhpcyBMaWNlbnNlLCBvbiBhIGR1cmFibGUgcGh5c2ljYWwKICAgICBtZWRpdW0gY3VzdG9tYXJpbHkgdXNlZCBmb3Igc29mdHdhcmUgaW50ZXJjaGFuZ2UsIGZvciBhIHByaWNlIG5vCiAgICAgbW9yZSB0aGFuIHlvdXIgcmVhc29uYWJsZSBjb3N0IG9mIHBoeXNpY2FsbHkgcGVyZm9ybWluZyB0aGlzCiAgICAgY29udmV5aW5nIG9mIHNvdXJjZSwgb3IgKDIpIGFjY2VzcyB0byBjb3B5IHRoZQogICAgIENvcnJlc3BvbmRpbmcgU291cmNlIGZyb20gYSBuZXR3b3JrIHNlcnZlciBhdCBubyBjaGFyZ2UuCgogICAgIGMpIENvbnZleSBpbmRpdmlkdWFsIGNvcGllcyBvZiB0aGUgb2JqZWN0IGNvZGUgd2l0aCBhIGNvcHkgb2YgdGhlCiAgICAgd3JpdHRlbiBvZmZlciB0byBwcm92aWRlIHRoZSBDb3JyZXNwb25kaW5nIFNvdXJjZS4gIFRoaXMKICAgICBhbHRlcm5hdGl2ZSBpcyBhbGxvd2VkIG9ubHkgb2NjYXNpb25hbGx5IGFuZCBub25jb21tZXJjaWFsbHksIGFuZAogICAgIG9ubHkgaWYgeW91IHJlY2VpdmVkIHRoZSBvYmplY3QgY29kZSB3aXRoIHN1Y2ggYW4gb2ZmZXIsIGluIGFjY29yZAogICAgIHdpdGggc3Vic2VjdGlvbiA2Yi4KCiAgICAgZCkgQ29udmV5IHRoZSBvYmplY3QgY29kZSBieSBvZmZlcmluZyBhY2Nlc3MgZnJvbSBhIGRlc2lnbmF0ZWQKICAgICBwbGFjZSAoZ3JhdGlzIG9yIGZvciBhIGNoYXJnZSksIGFuZCBvZmZlciBlcXVpdmFsZW50IGFjY2VzcyB0byB0aGUKICAgICBDb3JyZXNwb25kaW5nIFNvdXJjZSBpbiB0aGUgc2FtZSB3YXkgdGhyb3VnaCB0aGUgc2FtZSBwbGFjZSBhdCBubwogICAgIGZ1cnRoZXIgY2hhcmdlLiAgWW91IG5lZWQgbm90IHJlcXVpcmUgcmVjaXBpZW50cyB0byBjb3B5IHRoZQogICAgIENvcnJlc3BvbmRpbmcgU291cmNlIGFsb25nIHdpdGggdGhlIG9iamVjdCBjb2RlLiAgSWYgdGhlIHBsYWNlIHRvCiAgICAgY29weSB0aGUgb2JqZWN0IGNvZGUgaXMgYSBuZXR3b3JrIHNlcnZlciwgdGhlIENvcnJlc3BvbmRpbmcgU291cmNlCiAgICAgbWF5IGJlIG9uIGEgZGlmZmVyZW50IHNlcnZlciAob3BlcmF0ZWQgYnkgeW91IG9yIGEgdGhpcmQgcGFydHkpCiAgICAgdGhhdCBzdXBwb3J0cyBlcXVpdmFsZW50IGNvcHlpbmcgZmFjaWxpdGllcywgcHJvdmlkZWQgeW91IG1haW50YWluCiAgICAgY2xlYXIgZGlyZWN0aW9ucyBuZXh0IHRvIHRoZSBvYmplY3QgY29kZSBzYXlpbmcgd2hlcmUgdG8gZmluZCB0aGUKICAgICBDb3JyZXNwb25kaW5nIFNvdXJjZS4gIFJlZ2FyZGxlc3Mgb2Ygd2hhdCBzZXJ2ZXIgaG9zdHMgdGhlCiAgICAgQ29ycmVzcG9uZGluZyBTb3VyY2UsIHlvdSByZW1haW4gb2JsaWdhdGVkIHRvIGVuc3VyZSB0aGF0IGl0IGlzCiAgICAgYXZhaWxhYmxlIGZvciBhcyBsb25nIGFzIG5lZWRlZCB0byBzYXRpc2Z5IHRoZXNlIHJlcXVpcmVtZW50cy4KCiAgICAgZSkgQ29udmV5IHRoZSBvYmplY3QgY29kZSB1c2luZyBwZWVyLXRvLXBlZXIgdHJhbnNtaXNzaW9uLCBwcm92aWRlZAogICAgIHlvdSBpbmZvcm0gb3RoZXIgcGVlcnMgd2hlcmUgdGhlIG9iamVjdCBjb2RlIGFuZCBDb3JyZXNwb25kaW5nCiAgICAgU291cmNlIG9mIHRoZSB3b3JrIGFyZSBiZWluZyBvZmZlcmVkIHRvIHRoZSBnZW5lcmFsIHB1YmxpYyBhdCBubwogICAgIGNoYXJnZSB1bmRlciBzdWJzZWN0aW9uIDZkLgoKICAgQSBzZXBhcmFibGUgcG9ydGlvbiBvZiB0aGUgb2JqZWN0IGNvZGUsIHdob3NlIHNvdXJjZSBjb2RlIGlzIGV4Y2x1ZGVkCiBmcm9tIHRoZSBDb3JyZXNwb25kaW5nIFNvdXJjZSBhcyBhIFN5c3RlbSBMaWJyYXJ5LCBuZWVkIG5vdCBiZQogaW5jbHVkZWQgaW4gY29udmV5aW5nIHRoZSBvYmplY3QgY29kZSB3b3JrLgoKICAgQSAiVXNlciBQcm9kdWN0IiBpcyBlaXRoZXIgKDEpIGEgImNvbnN1bWVyIHByb2R1Y3QiLCB3aGljaCBtZWFucyBhbnkKIHRhbmdpYmxlIHBlcnNvbmFsIHByb3BlcnR5IHdoaWNoIGlzIG5vcm1hbGx5IHVzZWQgZm9yIHBlcnNvbmFsLCBmYW1pbHksCiBvciBob3VzZWhvbGQgcHVycG9zZXMsIG9yICgyKSBhbnl0aGluZyBkZXNpZ25lZCBvciBzb2xkIGZvciBpbmNvcnBvcmF0aW9uCiBpbnRvIGEgZHdlbGxpbmcuICBJbiBkZXRlcm1pbmluZyB3aGV0aGVyIGEgcHJvZHVjdCBpcyBhIGNvbnN1bWVyIHByb2R1Y3QsCiBkb3VidGZ1bCBjYXNlcyBzaGFsbCBiZSByZXNvbHZlZCBpbiBmYXZvciBvZiBjb3ZlcmFnZS4gIEZvciBhIHBhcnRpY3VsYXIKIHByb2R1Y3QgcmVjZWl2ZWQgYnkgYSBwYXJ0aWN1bGFyIHVzZXIsICJub3JtYWxseSB1c2VkIiByZWZlcnMgdG8gYQogdHlwaWNhbCBvciBjb21tb24gdXNlIG9mIHRoYXQgY2xhc3Mgb2YgcHJvZHVjdCwgcmVnYXJkbGVzcyBvZiB0aGUgc3RhdHVzCiBvZiB0aGUgcGFydGljdWxhciB1c2VyIG9yIG9mIHRoZSB3YXkgaW4gd2hpY2ggdGhlIHBhcnRpY3VsYXIgdXNlcgogYWN0dWFsbHkgdXNlcywgb3IgZXhwZWN0cyBvciBpcyBleHBlY3RlZCB0byB1c2UsIHRoZSBwcm9kdWN0LiAgQSBwcm9kdWN0CiBpcyBhIGNvbnN1bWVyIHByb2R1Y3QgcmVnYXJkbGVzcyBvZiB3aGV0aGVyIHRoZSBwcm9kdWN0IGhhcyBzdWJzdGFudGlhbAogY29tbWVyY2lhbCwgaW5kdXN0cmlhbCBvciBub24tY29uc3VtZXIgdXNlcywgdW5sZXNzIHN1Y2ggdXNlcyByZXByZXNlbnQKIHRoZSBvbmx5IHNpZ25pZmljYW50IG1vZGUgb2YgdXNlIG9mIHRoZSBwcm9kdWN0LgoKICAgIkluc3RhbGxhdGlvbiBJbmZvcm1hdGlvbiIgZm9yIGEgVXNlciBQcm9kdWN0IG1lYW5zIGFueSBtZXRob2RzLAogcHJvY2VkdXJlcywgYXV0aG9yaXphdGlvbiBrZXlzLCBvciBvdGhlciBpbmZvcm1hdGlvbiByZXF1aXJlZCB0byBpbnN0YWxsCiBhbmQgZXhlY3V0ZSBtb2RpZmllZCB2ZXJzaW9ucyBvZiBhIGNvdmVyZWQgd29yayBpbiB0aGF0IFVzZXIgUHJvZHVjdCBmcm9tCiBhIG1vZGlmaWVkIHZlcnNpb24gb2YgaXRzIENvcnJlc3BvbmRpbmcgU291cmNlLiAgVGhlIGluZm9ybWF0aW9uIG11c3QKIHN1ZmZpY2UgdG8gZW5zdXJlIHRoYXQgdGhlIGNvbnRpbnVlZCBmdW5jdGlvbmluZyBvZiB0aGUgbW9kaWZpZWQgb2JqZWN0CiBjb2RlIGlzIGluIG5vIGNhc2UgcHJldmVudGVkIG9yIGludGVyZmVyZWQgd2l0aCBzb2xlbHkgYmVjYXVzZQogbW9kaWZpY2F0aW9uIGhhcyBiZWVuIG1hZGUuCgogICBJZiB5b3UgY29udmV5IGFuIG9iamVjdCBjb2RlIHdvcmsgdW5kZXIgdGhpcyBzZWN0aW9uIGluLCBvciB3aXRoLCBvcgogc3BlY2lmaWNhbGx5IGZvciB1c2UgaW4sIGEgVXNlciBQcm9kdWN0LCBhbmQgdGhlIGNvbnZleWluZyBvY2N1cnMgYXMKIHBhcnQgb2YgYSB0cmFuc2FjdGlvbiBpbiB3aGljaCB0aGUgcmlnaHQgb2YgcG9zc2Vzc2lvbiBhbmQgdXNlIG9mIHRoZQogVXNlciBQcm9kdWN0IGlzIHRyYW5zZmVycmVkIHRvIHRoZSByZWNpcGllbnQgaW4gcGVycGV0dWl0eSBvciBmb3IgYQogZml4ZWQgdGVybSAocmVnYXJkbGVzcyBvZiBob3cgdGhlIHRyYW5zYWN0aW9uIGlzIGNoYXJhY3Rlcml6ZWQpLCB0aGUKIENvcnJlc3BvbmRpbmcgU291cmNlIGNvbnZleWVkIHVuZGVyIHRoaXMgc2VjdGlvbiBtdXN0IGJlIGFjY29tcGFuaWVkCiBieSB0aGUgSW5zdGFsbGF0aW9uIEluZm9ybWF0aW9uLiAgQnV0IHRoaXMgcmVxdWlyZW1lbnQgZG9lcyBub3QgYXBwbHkKIGlmIG5laXRoZXIgeW91IG5vciBhbnkgdGhpcmQgcGFydHkgcmV0YWlucyB0aGUgYWJpbGl0eSB0byBpbnN0YWxsCiBtb2RpZmllZCBvYmplY3QgY29kZSBvbiB0aGUgVXNlciBQcm9kdWN0IChmb3IgZXhhbXBsZSwgdGhlIHdvcmsgaGFzCiBiZWVuIGluc3RhbGxlZCBpbiBST00pLgoKICAgVGhlIHJlcXVpcmVtZW50IHRvIHByb3ZpZGUgSW5zdGFsbGF0aW9uIEluZm9ybWF0aW9uIGRvZXMgbm90IGluY2x1ZGUgYQogcmVxdWlyZW1lbnQgdG8gY29udGludWUgdG8gcHJvdmlkZSBzdXBwb3J0IHNlcnZpY2UsIHdhcnJhbnR5LCBvciB1cGRhdGVzCiBmb3IgYSB3b3JrIHRoYXQgaGFzIGJlZW4gbW9kaWZpZWQgb3IgaW5zdGFsbGVkIGJ5IHRoZSByZWNpcGllbnQsIG9yIGZvcgogdGhlIFVzZXIgUHJvZHVjdCBpbiB3aGljaCBpdCBoYXMgYmVlbiBtb2RpZmllZCBvciBpbnN0YWxsZWQuICBBY2Nlc3MgdG8gYQogbmV0d29yayBtYXkgYmUgZGVuaWVkIHdoZW4gdGhlIG1vZGlmaWNhdGlvbiBpdHNlbGYgbWF0ZXJpYWxseSBhbmQKIGFkdmVyc2VseSBhZmZlY3RzIHRoZSBvcGVyYXRpb24gb2YgdGhlIG5ldHdvcmsgb3IgdmlvbGF0ZXMgdGhlIHJ1bGVzIGFuZAogcHJvdG9jb2xzIGZvciBjb21tdW5pY2F0aW9uIGFjcm9zcyB0aGUgbmV0d29yay4KCiAgIENvcnJlc3BvbmRpbmcgU291cmNlIGNvbnZleWVkLCBhbmQgSW5zdGFsbGF0aW9uIEluZm9ybWF0aW9uIHByb3ZpZGVkLAogaW4gYWNjb3JkIHdpdGggdGhpcyBzZWN0aW9uIG11c3QgYmUgaW4gYSBmb3JtYXQgdGhhdCBpcyBwdWJsaWNseQogZG9jdW1lbnRlZCAoYW5kIHdpdGggYW4gaW1wbGVtZW50YXRpb24gYXZhaWxhYmxlIHRvIHRoZSBwdWJsaWMgaW4KIHNvdXJjZSBjb2RlIGZvcm0pLCBhbmQgbXVzdCByZXF1aXJlIG5vIHNwZWNpYWwgcGFzc3dvcmQgb3Iga2V5IGZvcgogdW5wYWNraW5nLCByZWFkaW5nIG9yIGNvcHlpbmcuCgogICA3LiBBZGRpdGlvbmFsIFRlcm1zLgoKICAgIkFkZGl0aW9uYWwgcGVybWlzc2lvbnMiIGFyZSB0ZXJtcyB0aGF0IHN1cHBsZW1lbnQgdGhlIHRlcm1zIG9mIHRoaXMKIExpY2Vuc2UgYnkgbWFraW5nIGV4Y2VwdGlvbnMgZnJvbSBvbmUgb3IgbW9yZSBvZiBpdHMgY29uZGl0aW9ucy4KIEFkZGl0aW9uYWwgcGVybWlzc2lvbnMgdGhhdCBhcmUgYXBwbGljYWJsZSB0byB0aGUgZW50aXJlIFByb2dyYW0gc2hhbGwKIGJlIHRyZWF0ZWQgYXMgdGhvdWdoIHRoZXkgd2VyZSBpbmNsdWRlZCBpbiB0aGlzIExpY2Vuc2UsIHRvIHRoZSBleHRlbnQKIHRoYXQgdGhleSBhcmUgdmFsaWQgdW5kZXIgYXBwbGljYWJsZSBsYXcuICBJZiBhZGRpdGlvbmFsIHBlcm1pc3Npb25zCiBhcHBseSBvbmx5IHRvIHBhcnQgb2YgdGhlIFByb2dyYW0sIHRoYXQgcGFydCBtYXkgYmUgdXNlZCBzZXBhcmF0ZWx5CiB1bmRlciB0aG9zZSBwZXJtaXNzaW9ucywgYnV0IHRoZSBlbnRpcmUgUHJvZ3JhbSByZW1haW5zIGdvdmVybmVkIGJ5CiB0aGlzIExpY2Vuc2Ugd2l0aG91dCByZWdhcmQgdG8gdGhlIGFkZGl0aW9uYWwgcGVybWlzc2lvbnMuCgogICBXaGVuIHlvdSBjb252ZXkgYSBjb3B5IG9mIGEgY292ZXJlZCB3b3JrLCB5b3UgbWF5IGF0IHlvdXIgb3B0aW9uCiByZW1vdmUgYW55IGFkZGl0aW9uYWwgcGVybWlzc2lvbnMgZnJvbSB0aGF0IGNvcHksIG9yIGZyb20gYW55IHBhcnQgb2YKIGl0LiAgKEFkZGl0aW9uYWwgcGVybWlzc2lvbnMgbWF5IGJlIHdyaXR0ZW4gdG8gcmVxdWlyZSB0aGVpciBvd24KIHJlbW92YWwgaW4gY2VydGFpbiBjYXNlcyB3aGVuIHlvdSBtb2RpZnkgdGhlIHdvcmsuKSAgWW91IG1heSBwbGFjZQogYWRkaXRpb25hbCBwZXJtaXNzaW9ucyBvbiBtYXRlcmlhbCwgYWRkZWQgYnkgeW91IHRvIGEgY292ZXJlZCB3b3JrLAogZm9yIHdoaWNoIHlvdSBoYXZlIG9yIGNhbiBnaXZlIGFwcHJvcHJpYXRlIGNvcHlyaWdodCBwZXJtaXNzaW9uLgoKICAgTm90d2l0aHN0YW5kaW5nIGFueSBvdGhlciBwcm92aXNpb24gb2YgdGhpcyBMaWNlbnNlLCBmb3IgbWF0ZXJpYWwgeW91CiBhZGQgdG8gYSBjb3ZlcmVkIHdvcmssIHlvdSBtYXkgKGlmIGF1dGhvcml6ZWQgYnkgdGhlIGNvcHlyaWdodCBob2xkZXJzIG9mCiB0aGF0IG1hdGVyaWFsKSBzdXBwbGVtZW50IHRoZSB0ZXJtcyBvZiB0aGlzIExpY2Vuc2Ugd2l0aCB0ZXJtczoKCiAgICAgYSkgRGlzY2xhaW1pbmcgd2FycmFudHkgb3IgbGltaXRpbmcgbGlhYmlsaXR5IGRpZmZlcmVudGx5IGZyb20gdGhlCiAgICAgdGVybXMgb2Ygc2VjdGlvbnMgMTUgYW5kIDE2IG9mIHRoaXMgTGljZW5zZTsgb3IKCiAgICAgYikgUmVxdWlyaW5nIHByZXNlcnZhdGlvbiBvZiBzcGVjaWZpZWQgcmVhc29uYWJsZSBsZWdhbCBub3RpY2VzIG9yCiAgICAgYXV0aG9yIGF0dHJpYnV0aW9ucyBpbiB0aGF0IG1hdGVyaWFsIG9yIGluIHRoZSBBcHByb3ByaWF0ZSBMZWdhbAogICAgIE5vdGljZXMgZGlzcGxheWVkIGJ5IHdvcmtzIGNvbnRhaW5pbmcgaXQ7IG9yCgogICAgIGMpIFByb2hpYml0aW5nIG1pc3JlcHJlc2VudGF0aW9uIG9mIHRoZSBvcmlnaW4gb2YgdGhhdCBtYXRlcmlhbCwgb3IKICAgICByZXF1aXJpbmcgdGhhdCBtb2RpZmllZCB2ZXJzaW9ucyBvZiBzdWNoIG1hdGVyaWFsIGJlIG1hcmtlZCBpbgogICAgIHJlYXNvbmFibGUgd2F5cyBhcyBkaWZmZXJlbnQgZnJvbSB0aGUgb3JpZ2luYWwgdmVyc2lvbjsgb3IKCiAgICAgZCkgTGltaXRpbmcgdGhlIHVzZSBmb3IgcHVibGljaXR5IHB1cnBvc2VzIG9mIG5hbWVzIG9mIGxpY2Vuc29ycyBvcgogICAgIGF1dGhvcnMgb2YgdGhlIG1hdGVyaWFsOyBvcgoKICAgICBlKSBEZWNsaW5pbmcgdG8gZ3JhbnQgcmlnaHRzIHVuZGVyIHRyYWRlbWFyayBsYXcgZm9yIHVzZSBvZiBzb21lCiAgICAgdHJhZGUgbmFtZXMsIHRyYWRlbWFya3MsIG9yIHNlcnZpY2UgbWFya3M7IG9yCgogICAgIGYpIFJlcXVpcmluZyBpbmRlbW5pZmljYXRpb24gb2YgbGljZW5zb3JzIGFuZCBhdXRob3JzIG9mIHRoYXQKICAgICBtYXRlcmlhbCBieSBhbnlvbmUgd2hvIGNvbnZleXMgdGhlIG1hdGVyaWFsIChvciBtb2RpZmllZCB2ZXJzaW9ucyBvZgogICAgIGl0KSB3aXRoIGNvbnRyYWN0dWFsIGFzc3VtcHRpb25zIG9mIGxpYWJpbGl0eSB0byB0aGUgcmVjaXBpZW50LCBmb3IKICAgICBhbnkgbGlhYmlsaXR5IHRoYXQgdGhlc2UgY29udHJhY3R1YWwgYXNzdW1wdGlvbnMgZGlyZWN0bHkgaW1wb3NlIG9uCiAgICAgdGhvc2UgbGljZW5zb3JzIGFuZCBhdXRob3JzLgoKICAgQWxsIG90aGVyIG5vbi1wZXJtaXNzaXZlIGFkZGl0aW9uYWwgdGVybXMgYXJlIGNvbnNpZGVyZWQgImZ1cnRoZXIKIHJlc3RyaWN0aW9ucyIgd2l0aGluIHRoZSBtZWFuaW5nIG9mIHNlY3Rpb24gMTAuICBJZiB0aGUgUHJvZ3JhbSBhcyB5b3UKIHJlY2VpdmVkIGl0LCBvciBhbnkgcGFydCBvZiBpdCwgY29udGFpbnMgYSBub3RpY2Ugc3RhdGluZyB0aGF0IGl0IGlzCiBnb3Zlcm5lZCBieSB0aGlzIExpY2Vuc2UgYWxvbmcgd2l0aCBhIHRlcm0gdGhhdCBpcyBhIGZ1cnRoZXIKIHJlc3RyaWN0aW9uLCB5b3UgbWF5IHJlbW92ZSB0aGF0IHRlcm0uICBJZiBhIGxpY2Vuc2UgZG9jdW1lbnQgY29udGFpbnMKIGEgZnVydGhlciByZXN0cmljdGlvbiBidXQgcGVybWl0cyByZWxpY2Vuc2luZyBvciBjb252ZXlpbmcgdW5kZXIgdGhpcwogTGljZW5zZSwgeW91IG1heSBhZGQgdG8gYSBjb3ZlcmVkIHdvcmsgbWF0ZXJpYWwgZ292ZXJuZWQgYnkgdGhlIHRlcm1zCiBvZiB0aGF0IGxpY2Vuc2UgZG9jdW1lbnQsIHByb3ZpZGVkIHRoYXQgdGhlIGZ1cnRoZXIgcmVzdHJpY3Rpb24gZG9lcwogbm90IHN1cnZpdmUgc3VjaCByZWxpY2Vuc2luZyBvciBjb252ZXlpbmcuCgogICBJZiB5b3UgYWRkIHRlcm1zIHRvIGEgY292ZXJlZCB3b3JrIGluIGFjY29yZCB3aXRoIHRoaXMgc2VjdGlvbiwgeW91CiBtdXN0IHBsYWNlLCBpbiB0aGUgcmVsZXZhbnQgc291cmNlIGZpbGVzLCBhIHN0YXRlbWVudCBvZiB0aGUKIGFkZGl0aW9uYWwgdGVybXMgdGhhdCBhcHBseSB0byB0aG9zZSBmaWxlcywgb3IgYSBub3RpY2UgaW5kaWNhdGluZwogd2hlcmUgdG8gZmluZCB0aGUgYXBwbGljYWJsZSB0ZXJtcy4KCiAgIEFkZGl0aW9uYWwgdGVybXMsIHBlcm1pc3NpdmUgb3Igbm9uLXBlcm1pc3NpdmUsIG1heSBiZSBzdGF0ZWQgaW4gdGhlCiBmb3JtIG9mIGEgc2VwYXJhdGVseSB3cml0dGVuIGxpY2Vuc2UsIG9yIHN0YXRlZCBhcyBleGNlcHRpb25zOwogdGhlIGFib3ZlIHJlcXVpcmVtZW50cyBhcHBseSBlaXRoZXIgd2F5LgoKICAgOC4gVGVybWluYXRpb24uCgogICBZb3UgbWF5IG5vdCBwcm9wYWdhdGUgb3IgbW9kaWZ5IGEgY292ZXJlZCB3b3JrIGV4Y2VwdCBhcyBleHByZXNzbHkKIHByb3ZpZGVkIHVuZGVyIHRoaXMgTGljZW5zZS4gIEFueSBhdHRlbXB0IG90aGVyd2lzZSB0byBwcm9wYWdhdGUgb3IKIG1vZGlmeSBpdCBpcyB2b2lkLCBhbmQgd2lsbCBhdXRvbWF0aWNhbGx5IHRlcm1pbmF0ZSB5b3VyIHJpZ2h0cyB1bmRlcgogdGhpcyBMaWNlbnNlIChpbmNsdWRpbmcgYW55IHBhdGVudCBsaWNlbnNlcyBncmFudGVkIHVuZGVyIHRoZSB0aGlyZAogcGFyYWdyYXBoIG9mIHNlY3Rpb24gMTEpLgoKICAgSG93ZXZlciwgaWYgeW91IGNlYXNlIGFsbCB2aW9sYXRpb24gb2YgdGhpcyBMaWNlbnNlLCB0aGVuIHlvdXIKIGxpY2Vuc2UgZnJvbSBhIHBhcnRpY3VsYXIgY29weXJpZ2h0IGhvbGRlciBpcyByZWluc3RhdGVkIChhKQogcHJvdmlzaW9uYWxseSwgdW5sZXNzIGFuZCB1bnRpbCB0aGUgY29weXJpZ2h0IGhvbGRlciBleHBsaWNpdGx5IGFuZAogZmluYWxseSB0ZXJtaW5hdGVzIHlvdXIgbGljZW5zZSwgYW5kIChiKSBwZXJtYW5lbnRseSwgaWYgdGhlIGNvcHlyaWdodAogaG9sZGVyIGZhaWxzIHRvIG5vdGlmeSB5b3Ugb2YgdGhlIHZpb2xhdGlvbiBieSBzb21lIHJlYXNvbmFibGUgbWVhbnMKIHByaW9yIHRvIDYwIGRheXMgYWZ0ZXIgdGhlIGNlc3NhdGlvbi4KCiAgIE1vcmVvdmVyLCB5b3VyIGxpY2Vuc2UgZnJvbSBhIHBhcnRpY3VsYXIgY29weXJpZ2h0IGhvbGRlciBpcwogcmVpbnN0YXRlZCBwZXJtYW5lbnRseSBpZiB0aGUgY29weXJpZ2h0IGhvbGRlciBub3RpZmllcyB5b3Ugb2YgdGhlCiB2aW9sYXRpb24gYnkgc29tZSByZWFzb25hYmxlIG1lYW5zLCB0aGlzIGlzIHRoZSBmaXJzdCB0aW1lIHlvdSBoYXZlCiByZWNlaXZlZCBub3RpY2Ugb2YgdmlvbGF0aW9uIG9mIHRoaXMgTGljZW5zZSAoZm9yIGFueSB3b3JrKSBmcm9tIHRoYXQKIGNvcHlyaWdodCBob2xkZXIsIGFuZCB5b3UgY3VyZSB0aGUgdmlvbGF0aW9uIHByaW9yIHRvIDMwIGRheXMgYWZ0ZXIKIHlvdXIgcmVjZWlwdCBvZiB0aGUgbm90aWNlLgoKICAgVGVybWluYXRpb24gb2YgeW91ciByaWdodHMgdW5kZXIgdGhpcyBzZWN0aW9uIGRvZXMgbm90IHRlcm1pbmF0ZSB0aGUKIGxpY2Vuc2VzIG9mIHBhcnRpZXMgd2hvIGhhdmUgcmVjZWl2ZWQgY29waWVzIG9yIHJpZ2h0cyBmcm9tIHlvdSB1bmRlcgogdGhpcyBMaWNlbnNlLiAgSWYgeW91ciByaWdodHMgaGF2ZSBiZWVuIHRlcm1pbmF0ZWQgYW5kIG5vdCBwZXJtYW5lbnRseQogcmVpbnN0YXRlZCwgeW91IGRvIG5vdCBxdWFsaWZ5IHRvIHJlY2VpdmUgbmV3IGxpY2Vuc2VzIGZvciB0aGUgc2FtZQogbWF0ZXJpYWwgdW5kZXIgc2VjdGlvbiAxMC4KCiAgIDkuIEFjY2VwdGFuY2UgTm90IFJlcXVpcmVkIGZvciBIYXZpbmcgQ29waWVzLgoKICAgWW91IGFyZSBub3QgcmVxdWlyZWQgdG8gYWNjZXB0IHRoaXMgTGljZW5zZSBpbiBvcmRlciB0byByZWNlaXZlIG9yCiBydW4gYSBjb3B5IG9mIHRoZSBQcm9ncmFtLiAgQW5jaWxsYXJ5IHByb3BhZ2F0aW9uIG9mIGEgY292ZXJlZCB3b3JrCiBvY2N1cnJpbmcgc29sZWx5IGFzIGEgY29uc2VxdWVuY2Ugb2YgdXNpbmcgcGVlci10by1wZWVyIHRyYW5zbWlzc2lvbgogdG8gcmVjZWl2ZSBhIGNvcHkgbGlrZXdpc2UgZG9lcyBub3QgcmVxdWlyZSBhY2NlcHRhbmNlLiAgSG93ZXZlciwKIG5vdGhpbmcgb3RoZXIgdGhhbiB0aGlzIExpY2Vuc2UgZ3JhbnRzIHlvdSBwZXJtaXNzaW9uIHRvIHByb3BhZ2F0ZSBvcgogbW9kaWZ5IGFueSBjb3ZlcmVkIHdvcmsuICBUaGVzZSBhY3Rpb25zIGluZnJpbmdlIGNvcHlyaWdodCBpZiB5b3UgZG8KIG5vdCBhY2NlcHQgdGhpcyBMaWNlbnNlLiAgVGhlcmVmb3JlLCBieSBtb2RpZnlpbmcgb3IgcHJvcGFnYXRpbmcgYQogY292ZXJlZCB3b3JrLCB5b3UgaW5kaWNhdGUgeW91ciBhY2NlcHRhbmNlIG9mIHRoaXMgTGljZW5zZSB0byBkbyBzby4KCiAgIDEwLiBBdXRvbWF0aWMgTGljZW5zaW5nIG9mIERvd25zdHJlYW0gUmVjaXBpZW50cy4KCiAgIEVhY2ggdGltZSB5b3UgY29udmV5IGEgY292ZXJlZCB3b3JrLCB0aGUgcmVjaXBpZW50IGF1dG9tYXRpY2FsbHkKIHJlY2VpdmVzIGEgbGljZW5zZSBmcm9tIHRoZSBvcmlnaW5hbCBsaWNlbnNvcnMsIHRvIHJ1biwgbW9kaWZ5IGFuZAogcHJvcGFnYXRlIHRoYXQgd29yaywgc3ViamVjdCB0byB0aGlzIExpY2Vuc2UuICBZb3UgYXJlIG5vdCByZXNwb25zaWJsZQogZm9yIGVuZm9yY2luZyBjb21wbGlhbmNlIGJ5IHRoaXJkIHBhcnRpZXMgd2l0aCB0aGlzIExpY2Vuc2UuCgogICBBbiAiZW50aXR5IHRyYW5zYWN0aW9uIiBpcyBhIHRyYW5zYWN0aW9uIHRyYW5zZmVycmluZyBjb250cm9sIG9mIGFuCiBvcmdhbml6YXRpb24sIG9yIHN1YnN0YW50aWFsbHkgYWxsIGFzc2V0cyBvZiBvbmUsIG9yIHN1YmRpdmlkaW5nIGFuCiBvcmdhbml6YXRpb24sIG9yIG1lcmdpbmcgb3JnYW5pemF0aW9ucy4gIElmIHByb3BhZ2F0aW9uIG9mIGEgY292ZXJlZAogd29yayByZXN1bHRzIGZyb20gYW4gZW50aXR5IHRyYW5zYWN0aW9uLCBlYWNoIHBhcnR5IHRvIHRoYXQKIHRyYW5zYWN0aW9uIHdobyByZWNlaXZlcyBhIGNvcHkgb2YgdGhlIHdvcmsgYWxzbyByZWNlaXZlcyB3aGF0ZXZlcgogbGljZW5zZXMgdG8gdGhlIHdvcmsgdGhlIHBhcnR5J3MgcHJlZGVjZXNzb3IgaW4gaW50ZXJlc3QgaGFkIG9yIGNvdWxkCiBnaXZlIHVuZGVyIHRoZSBwcmV2aW91cyBwYXJhZ3JhcGgsIHBsdXMgYSByaWdodCB0byBwb3NzZXNzaW9uIG9mIHRoZQogQ29ycmVzcG9uZGluZyBTb3VyY2Ugb2YgdGhlIHdvcmsgZnJvbSB0aGUgcHJlZGVjZXNzb3IgaW4gaW50ZXJlc3QsIGlmCiB0aGUgcHJlZGVjZXNzb3IgaGFzIGl0IG9yIGNhbiBnZXQgaXQgd2l0aCByZWFzb25hYmxlIGVmZm9ydHMuCgogICBZb3UgbWF5IG5vdCBpbXBvc2UgYW55IGZ1cnRoZXIgcmVzdHJpY3Rpb25zIG9uIHRoZSBleGVyY2lzZSBvZiB0aGUKIHJpZ2h0cyBncmFudGVkIG9yIGFmZmlybWVkIHVuZGVyIHRoaXMgTGljZW5zZS4gIEZvciBleGFtcGxlLCB5b3UgbWF5CiBub3QgaW1wb3NlIGEgbGljZW5zZSBmZWUsIHJveWFsdHksIG9yIG90aGVyIGNoYXJnZSBmb3IgZXhlcmNpc2Ugb2YKIHJpZ2h0cyBncmFudGVkIHVuZGVyIHRoaXMgTGljZW5zZSwgYW5kIHlvdSBtYXkgbm90IGluaXRpYXRlIGxpdGlnYXRpb24KIChpbmNsdWRpbmcgYSBjcm9zcy1jbGFpbSBvciBjb3VudGVyY2xhaW0gaW4gYSBsYXdzdWl0KSBhbGxlZ2luZyB0aGF0CiBhbnkgcGF0ZW50IGNsYWltIGlzIGluZnJpbmdlZCBieSBtYWtpbmcsIHVzaW5nLCBzZWxsaW5nLCBvZmZlcmluZyBmb3IKIHNhbGUsIG9yIGltcG9ydGluZyB0aGUgUHJvZ3JhbSBvciBhbnkgcG9ydGlvbiBvZiBpdC4KCiAgIDExLiBQYXRlbnRzLgoKICAgQSAiY29udHJpYnV0b3IiIGlzIGEgY29weXJpZ2h0IGhvbGRlciB3aG8gYXV0aG9yaXplcyB1c2UgdW5kZXIgdGhpcwogTGljZW5zZSBvZiB0aGUgUHJvZ3JhbSBvciBhIHdvcmsgb24gd2hpY2ggdGhlIFByb2dyYW0gaXMgYmFzZWQuICBUaGUKIHdvcmsgdGh1cyBsaWNlbnNlZCBpcyBjYWxsZWQgdGhlIGNvbnRyaWJ1dG9yJ3MgImNvbnRyaWJ1dG9yIHZlcnNpb24iLgoKICAgQSBjb250cmlidXRvcidzICJlc3NlbnRpYWwgcGF0ZW50IGNsYWltcyIgYXJlIGFsbCBwYXRlbnQgY2xhaW1zCiBvd25lZCBvciBjb250cm9sbGVkIGJ5IHRoZSBjb250cmlidXRvciwgd2hldGhlciBhbHJlYWR5IGFjcXVpcmVkIG9yCiBoZXJlYWZ0ZXIgYWNxdWlyZWQsIHRoYXQgd291bGQgYmUgaW5mcmluZ2VkIGJ5IHNvbWUgbWFubmVyLCBwZXJtaXR0ZWQKIGJ5IHRoaXMgTGljZW5zZSwgb2YgbWFraW5nLCB1c2luZywgb3Igc2VsbGluZyBpdHMgY29udHJpYnV0b3IgdmVyc2lvbiwKIGJ1dCBkbyBub3QgaW5jbHVkZSBjbGFpbXMgdGhhdCB3b3VsZCBiZSBpbmZyaW5nZWQgb25seSBhcyBhCiBjb25zZXF1ZW5jZSBvZiBmdXJ0aGVyIG1vZGlmaWNhdGlvbiBvZiB0aGUgY29udHJpYnV0b3IgdmVyc2lvbi4gIEZvcgogcHVycG9zZXMgb2YgdGhpcyBkZWZpbml0aW9uLCAiY29udHJvbCIgaW5jbHVkZXMgdGhlIHJpZ2h0IHRvIGdyYW50CiBwYXRlbnQgc3VibGljZW5zZXMgaW4gYSBtYW5uZXIgY29uc2lzdGVudCB3aXRoIHRoZSByZXF1aXJlbWVudHMgb2YKIHRoaXMgTGljZW5zZS4KCiAgIEVhY2ggY29udHJpYnV0b3IgZ3JhbnRzIHlvdSBhIG5vbi1leGNsdXNpdmUsIHdvcmxkd2lkZSwgcm95YWx0eS1mcmVlCiBwYXRlbnQgbGljZW5zZSB1bmRlciB0aGUgY29udHJpYnV0b3IncyBlc3NlbnRpYWwgcGF0ZW50IGNsYWltcywgdG8KIG1ha2UsIHVzZSwgc2VsbCwgb2ZmZXIgZm9yIHNhbGUsIGltcG9ydCBhbmQgb3RoZXJ3aXNlIHJ1biwgbW9kaWZ5IGFuZAogcHJvcGFnYXRlIHRoZSBjb250ZW50cyBvZiBpdHMgY29udHJpYnV0b3IgdmVyc2lvbi4KCiAgIEluIHRoZSBmb2xsb3dpbmcgdGhyZWUgcGFyYWdyYXBocywgYSAicGF0ZW50IGxpY2Vuc2UiIGlzIGFueSBleHByZXNzCiBhZ3JlZW1lbnQgb3IgY29tbWl0bWVudCwgaG93ZXZlciBkZW5vbWluYXRlZCwgbm90IHRvIGVuZm9yY2UgYSBwYXRlbnQKIChzdWNoIGFzIGFuIGV4cHJlc3MgcGVybWlzc2lvbiB0byBwcmFjdGljZSBhIHBhdGVudCBvciBjb3ZlbmFudCBub3QgdG8KIHN1ZSBmb3IgcGF0ZW50IGluZnJpbmdlbWVudCkuICBUbyAiZ3JhbnQiIHN1Y2ggYSBwYXRlbnQgbGljZW5zZSB0byBhCiBwYXJ0eSBtZWFucyB0byBtYWtlIHN1Y2ggYW4gYWdyZWVtZW50IG9yIGNvbW1pdG1lbnQgbm90IHRvIGVuZm9yY2UgYQogcGF0ZW50IGFnYWluc3QgdGhlIHBhcnR5LgoKICAgSWYgeW91IGNvbnZleSBhIGNvdmVyZWQgd29yaywga25vd2luZ2x5IHJlbHlpbmcgb24gYSBwYXRlbnQgbGljZW5zZSwKIGFuZCB0aGUgQ29ycmVzcG9uZGluZyBTb3VyY2Ugb2YgdGhlIHdvcmsgaXMgbm90IGF2YWlsYWJsZSBmb3IgYW55b25lCiB0byBjb3B5LCBmcmVlIG9mIGNoYXJnZSBhbmQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoaXMgTGljZW5zZSwgdGhyb3VnaCBhCiBwdWJsaWNseSBhdmFpbGFibGUgbmV0d29yayBzZXJ2ZXIgb3Igb3RoZXIgcmVhZGlseSBhY2Nlc3NpYmxlIG1lYW5zLAogdGhlbiB5b3UgbXVzdCBlaXRoZXIgKDEpIGNhdXNlIHRoZSBDb3JyZXNwb25kaW5nIFNvdXJjZSB0byBiZSBzbwogYXZhaWxhYmxlLCBvciAoMikgYXJyYW5nZSB0byBkZXByaXZlIHlvdXJzZWxmIG9mIHRoZSBiZW5lZml0IG9mIHRoZQogcGF0ZW50IGxpY2Vuc2UgZm9yIHRoaXMgcGFydGljdWxhciB3b3JrLCBvciAoMykgYXJyYW5nZSwgaW4gYSBtYW5uZXIKIGNvbnNpc3RlbnQgd2l0aCB0aGUgcmVxdWlyZW1lbnRzIG9mIHRoaXMgTGljZW5zZSwgdG8gZXh0ZW5kIHRoZSBwYXRlbnQKIGxpY2Vuc2UgdG8gZG93bnN0cmVhbSByZWNpcGllbnRzLiAgIktub3dpbmdseSByZWx5aW5nIiBtZWFucyB5b3UgaGF2ZQogYWN0dWFsIGtub3dsZWRnZSB0aGF0LCBidXQgZm9yIHRoZSBwYXRlbnQgbGljZW5zZSwgeW91ciBjb252ZXlpbmcgdGhlCiBjb3ZlcmVkIHdvcmsgaW4gYSBjb3VudHJ5LCBvciB5b3VyIHJlY2lwaWVudCdzIHVzZSBvZiB0aGUgY292ZXJlZCB3b3JrCiBpbiBhIGNvdW50cnksIHdvdWxkIGluZnJpbmdlIG9uZSBvciBtb3JlIGlkZW50aWZpYWJsZSBwYXRlbnRzIGluIHRoYXQKIGNvdW50cnkgdGhhdCB5b3UgaGF2ZSByZWFzb24gdG8gYmVsaWV2ZSBhcmUgdmFsaWQuCgogICBJZiwgcHVyc3VhbnQgdG8gb3IgaW4gY29ubmVjdGlvbiB3aXRoIGEgc2luZ2xlIHRyYW5zYWN0aW9uIG9yCiBhcnJhbmdlbWVudCwgeW91IGNvbnZleSwgb3IgcHJvcGFnYXRlIGJ5IHByb2N1cmluZyBjb252ZXlhbmNlIG9mLCBhCiBjb3ZlcmVkIHdvcmssIGFuZCBncmFudCBhIHBhdGVudCBsaWNlbnNlIHRvIHNvbWUgb2YgdGhlIHBhcnRpZXMKIHJlY2VpdmluZyB0aGUgY292ZXJlZCB3b3JrIGF1dGhvcml6aW5nIHRoZW0gdG8gdXNlLCBwcm9wYWdhdGUsIG1vZGlmeQogb3IgY29udmV5IGEgc3BlY2lmaWMgY29weSBvZiB0aGUgY292ZXJlZCB3b3JrLCB0aGVuIHRoZSBwYXRlbnQgbGljZW5zZQogeW91IGdyYW50IGlzIGF1dG9tYXRpY2FsbHkgZXh0ZW5kZWQgdG8gYWxsIHJlY2lwaWVudHMgb2YgdGhlIGNvdmVyZWQKIHdvcmsgYW5kIHdvcmtzIGJhc2VkIG9uIGl0LgoKICAgQSBwYXRlbnQgbGljZW5zZSBpcyAiZGlzY3JpbWluYXRvcnkiIGlmIGl0IGRvZXMgbm90IGluY2x1ZGUgd2l0aGluCiB0aGUgc2NvcGUgb2YgaXRzIGNvdmVyYWdlLCBwcm9oaWJpdHMgdGhlIGV4ZXJjaXNlIG9mLCBvciBpcwogY29uZGl0aW9uZWQgb24gdGhlIG5vbi1leGVyY2lzZSBvZiBvbmUgb3IgbW9yZSBvZiB0aGUgcmlnaHRzIHRoYXQgYXJlCiBzcGVjaWZpY2FsbHkgZ3JhbnRlZCB1bmRlciB0aGlzIExpY2Vuc2UuICBZb3UgbWF5IG5vdCBjb252ZXkgYSBjb3ZlcmVkCiB3b3JrIGlmIHlvdSBhcmUgYSBwYXJ0eSB0byBhbiBhcnJhbmdlbWVudCB3aXRoIGEgdGhpcmQgcGFydHkgdGhhdCBpcwogaW4gdGhlIGJ1c2luZXNzIG9mIGRpc3RyaWJ1dGluZyBzb2Z0d2FyZSwgdW5kZXIgd2hpY2ggeW91IG1ha2UgcGF5bWVudAogdG8gdGhlIHRoaXJkIHBhcnR5IGJhc2VkIG9uIHRoZSBleHRlbnQgb2YgeW91ciBhY3Rpdml0eSBvZiBjb252ZXlpbmcKIHRoZSB3b3JrLCBhbmQgdW5kZXIgd2hpY2ggdGhlIHRoaXJkIHBhcnR5IGdyYW50cywgdG8gYW55IG9mIHRoZQogcGFydGllcyB3aG8gd291bGQgcmVjZWl2ZSB0aGUgY292ZXJlZCB3b3JrIGZyb20geW91LCBhIGRpc2NyaW1pbmF0b3J5CiBwYXRlbnQgbGljZW5zZSAoYSkgaW4gY29ubmVjdGlvbiB3aXRoIGNvcGllcyBvZiB0aGUgY292ZXJlZCB3b3JrCiBjb252ZXllZCBieSB5b3UgKG9yIGNvcGllcyBtYWRlIGZyb20gdGhvc2UgY29waWVzKSwgb3IgKGIpIHByaW1hcmlseQogZm9yIGFuZCBpbiBjb25uZWN0aW9uIHdpdGggc3BlY2lmaWMgcHJvZHVjdHMgb3IgY29tcGlsYXRpb25zIHRoYXQKIGNvbnRhaW4gdGhlIGNvdmVyZWQgd29yaywgdW5sZXNzIHlvdSBlbnRlcmVkIGludG8gdGhhdCBhcnJhbmdlbWVudCwKIG9yIHRoYXQgcGF0ZW50IGxpY2Vuc2Ugd2FzIGdyYW50ZWQsIHByaW9yIHRvIDI4IE1hcmNoIDIwMDcuCgogICBOb3RoaW5nIGluIHRoaXMgTGljZW5zZSBzaGFsbCBiZSBjb25zdHJ1ZWQgYXMgZXhjbHVkaW5nIG9yIGxpbWl0aW5nCiBhbnkgaW1wbGllZCBsaWNlbnNlIG9yIG90aGVyIGRlZmVuc2VzIHRvIGluZnJpbmdlbWVudCB0aGF0IG1heQogb3RoZXJ3aXNlIGJlIGF2YWlsYWJsZSB0byB5b3UgdW5kZXIgYXBwbGljYWJsZSBwYXRlbnQgbGF3LgoKICAgMTIuIE5vIFN1cnJlbmRlciBvZiBPdGhlcnMnIEZyZWVkb20uCgogICBJZiBjb25kaXRpb25zIGFyZSBpbXBvc2VkIG9uIHlvdSAod2hldGhlciBieSBjb3VydCBvcmRlciwgYWdyZWVtZW50IG9yCiBvdGhlcndpc2UpIHRoYXQgY29udHJhZGljdCB0aGUgY29uZGl0aW9ucyBvZiB0aGlzIExpY2Vuc2UsIHRoZXkgZG8gbm90CiBleGN1c2UgeW91IGZyb20gdGhlIGNvbmRpdGlvbnMgb2YgdGhpcyBMaWNlbnNlLiAgSWYgeW91IGNhbm5vdCBjb252ZXkgYQogY292ZXJlZCB3b3JrIHNvIGFzIHRvIHNhdGlzZnkgc2ltdWx0YW5lb3VzbHkgeW91ciBvYmxpZ2F0aW9ucyB1bmRlciB0aGlzCiBMaWNlbnNlIGFuZCBhbnkgb3RoZXIgcGVydGluZW50IG9ibGlnYXRpb25zLCB0aGVuIGFzIGEgY29uc2VxdWVuY2UgeW91IG1heQogbm90IGNvbnZleSBpdCBhdCBhbGwuICBGb3IgZXhhbXBsZSwgaWYgeW91IGFncmVlIHRvIHRlcm1zIHRoYXQgb2JsaWdhdGUgeW91CiB0byBjb2xsZWN0IGEgcm95YWx0eSBmb3IgZnVydGhlciBjb252ZXlpbmcgZnJvbSB0aG9zZSB0byB3aG9tIHlvdSBjb252ZXkKIHRoZSBQcm9ncmFtLCB0aGUgb25seSB3YXkgeW91IGNvdWxkIHNhdGlzZnkgYm90aCB0aG9zZSB0ZXJtcyBhbmQgdGhpcwogTGljZW5zZSB3b3VsZCBiZSB0byByZWZyYWluIGVudGlyZWx5IGZyb20gY29udmV5aW5nIHRoZSBQcm9ncmFtLgoKICAgMTMuIFVzZSB3aXRoIHRoZSBHTlUgQWZmZXJvIEdlbmVyYWwgUHVibGljIExpY2Vuc2UuCgogICBOb3R3aXRoc3RhbmRpbmcgYW55IG90aGVyIHByb3Zpc2lvbiBvZiB0aGlzIExpY2Vuc2UsIHlvdSBoYXZlCiBwZXJtaXNzaW9uIHRvIGxpbmsgb3IgY29tYmluZSBhbnkgY292ZXJlZCB3b3JrIHdpdGggYSB3b3JrIGxpY2Vuc2VkCiB1bmRlciB2ZXJzaW9uIDMgb2YgdGhlIEdOVSBBZmZlcm8gR2VuZXJhbCBQdWJsaWMgTGljZW5zZSBpbnRvIGEgc2luZ2xlCiBjb21iaW5lZCB3b3JrLCBhbmQgdG8gY29udmV5IHRoZSByZXN1bHRpbmcgd29yay4gIFRoZSB0ZXJtcyBvZiB0aGlzCiBMaWNlbnNlIHdpbGwgY29udGludWUgdG8gYXBwbHkgdG8gdGhlIHBhcnQgd2hpY2ggaXMgdGhlIGNvdmVyZWQgd29yaywKIGJ1dCB0aGUgc3BlY2lhbCByZXF1aXJlbWVudHMgb2YgdGhlIEdOVSBBZmZlcm8gR2VuZXJhbCBQdWJsaWMgTGljZW5zZSwKIHNlY3Rpb24gMTMsIGNvbmNlcm5pbmcgaW50ZXJhY3Rpb24gdGhyb3VnaCBhIG5ldHdvcmsgd2lsbCBhcHBseSB0byB0aGUKIGNvbWJpbmF0aW9uIGFzIHN1Y2guCgogICAxNC4gUmV2aXNlZCBWZXJzaW9ucyBvZiB0aGlzIExpY2Vuc2UuCgogICBUaGUgRnJlZSBTb2Z0d2FyZSBGb3VuZGF0aW9uIG1heSBwdWJsaXNoIHJldmlzZWQgYW5kL29yIG5ldyB2ZXJzaW9ucyBvZgogdGhlIEdOVSBHZW5lcmFsIFB1YmxpYyBMaWNlbnNlIGZyb20gdGltZSB0byB0aW1lLiAgU3VjaCBuZXcgdmVyc2lvbnMgd2lsbAogYmUgc2ltaWxhciBpbiBzcGlyaXQgdG8gdGhlIHByZXNlbnQgdmVyc2lvbiwgYnV0IG1heSBkaWZmZXIgaW4gZGV0YWlsIHRvCiBhZGRyZXNzIG5ldyBwcm9ibGVtcyBvciBjb25jZXJucy4KCiAgIEVhY2ggdmVyc2lvbiBpcyBnaXZlbiBhIGRpc3Rpbmd1aXNoaW5nIHZlcnNpb24gbnVtYmVyLiAgSWYgdGhlCiBQcm9ncmFtIHNwZWNpZmllcyB0aGF0IGEgY2VydGFpbiBudW1iZXJlZCB2ZXJzaW9uIG9mIHRoZSBHTlUgR2VuZXJhbAogUHVibGljIExpY2Vuc2UgIm9yIGFueSBsYXRlciB2ZXJzaW9uIiBhcHBsaWVzIHRvIGl0LCB5b3UgaGF2ZSB0aGUKIG9wdGlvbiBvZiBmb2xsb3dpbmcgdGhlIHRlcm1zIGFuZCBjb25kaXRpb25zIGVpdGhlciBvZiB0aGF0IG51bWJlcmVkCiB2ZXJzaW9uIG9yIG9mIGFueSBsYXRlciB2ZXJzaW9uIHB1Ymxpc2hlZCBieSB0aGUgRnJlZSBTb2Z0d2FyZQogRm91bmRhdGlvbi4gIElmIHRoZSBQcm9ncmFtIGRvZXMgbm90IHNwZWNpZnkgYSB2ZXJzaW9uIG51bWJlciBvZiB0aGUKIEdOVSBHZW5lcmFsIFB1YmxpYyBMaWNlbnNlLCB5b3UgbWF5IGNob29zZSBhbnkgdmVyc2lvbiBldmVyIHB1Ymxpc2hlZAogYnkgdGhlIEZyZWUgU29mdHdhcmUgRm91bmRhdGlvbi4KCiAgIElmIHRoZSBQcm9ncmFtIHNwZWNpZmllcyB0aGF0IGEgcHJveHkgY2FuIGRlY2lkZSB3aGljaCBmdXR1cmUKIHZlcnNpb25zIG9mIHRoZSBHTlUgR2VuZXJhbCBQdWJsaWMgTGljZW5zZSBjYW4gYmUgdXNlZCwgdGhhdCBwcm94eSdzCiBwdWJsaWMgc3RhdGVtZW50IG9mIGFjY2VwdGFuY2Ugb2YgYSB2ZXJzaW9uIHBlcm1hbmVudGx5IGF1dGhvcml6ZXMgeW91CiB0byBjaG9vc2UgdGhhdCB2ZXJzaW9uIGZvciB0aGUgUHJvZ3JhbS4KCiAgIExhdGVyIGxpY2Vuc2UgdmVyc2lvbnMgbWF5IGdpdmUgeW91IGFkZGl0aW9uYWwgb3IgZGlmZmVyZW50CiBwZXJtaXNzaW9ucy4gIEhvd2V2ZXIsIG5vIGFkZGl0aW9uYWwgb2JsaWdhdGlvbnMgYXJlIGltcG9zZWQgb24gYW55CiBhdXRob3Igb3IgY29weXJpZ2h0IGhvbGRlciBhcyBhIHJlc3VsdCBvZiB5b3VyIGNob29zaW5nIHRvIGZvbGxvdyBhCiBsYXRlciB2ZXJzaW9uLgoKICAgMTUuIERpc2NsYWltZXIgb2YgV2FycmFudHkuCgogICBUSEVSRSBJUyBOTyBXQVJSQU5UWSBGT1IgVEhFIFBST0dSQU0sIFRPIFRIRSBFWFRFTlQgUEVSTUlUVEVEIEJZCiBBUFBMSUNBQkxFIExBVy4gIEVYQ0VQVCBXSEVOIE9USEVSV0lTRSBTVEFURUQgSU4gV1JJVElORyBUSEUgQ09QWVJJR0hUCiBIT0xERVJTIEFORC9PUiBPVEhFUiBQQVJUSUVTIFBST1ZJREUgVEhFIFBST0dSQU0gIkFTIElTIiBXSVRIT1VUIFdBUlJBTlRZCiBPRiBBTlkgS0lORCwgRUlUSEVSIEVYUFJFU1NFRCBPUiBJTVBMSUVELCBJTkNMVURJTkcsIEJVVCBOT1QgTElNSVRFRCBUTywKIFRIRSBJTVBMSUVEIFdBUlJBTlRJRVMgT0YgTUVSQ0hBTlRBQklMSVRZIEFORCBGSVRORVNTIEZPUiBBIFBBUlRJQ1VMQVIKIFBVUlBPU0UuICBUSEUgRU5USVJFIFJJU0sgQVMgVE8gVEhFIFFVQUxJVFkgQU5EIFBFUkZPUk1BTkNFIE9GIFRIRSBQUk9HUkFNCiBJUyBXSVRIIFlPVS4gIFNIT1VMRCBUSEUgUFJPR1JBTSBQUk9WRSBERUZFQ1RJVkUsIFlPVSBBU1NVTUUgVEhFIENPU1QgT0YKIEFMTCBORUNFU1NBUlkgU0VSVklDSU5HLCBSRVBBSVIgT1IgQ09SUkVDVElPTi4KCiAgIDE2LiBMaW1pdGF0aW9uIG9mIExpYWJpbGl0eS4KCiAgIElOIE5PIEVWRU5UIFVOTEVTUyBSRVFVSVJFRCBCWSBBUFBMSUNBQkxFIExBVyBPUiBBR1JFRUQgVE8gSU4gV1JJVElORwogV0lMTCBBTlkgQ09QWVJJR0hUIEhPTERFUiwgT1IgQU5ZIE9USEVSIFBBUlRZIFdITyBNT0RJRklFUyBBTkQvT1IgQ09OVkVZUwogVEhFIFBST0dSQU0gQVMgUEVSTUlUVEVEIEFCT1ZFLCBCRSBMSUFCTEUgVE8gWU9VIEZPUiBEQU1BR0VTLCBJTkNMVURJTkcgQU5ZCiBHRU5FUkFMLCBTUEVDSUFMLCBJTkNJREVOVEFMIE9SIENPTlNFUVVFTlRJQUwgREFNQUdFUyBBUklTSU5HIE9VVCBPRiBUSEUKIFVTRSBPUiBJTkFCSUxJVFkgVE8gVVNFIFRIRSBQUk9HUkFNIChJTkNMVURJTkcgQlVUIE5PVCBMSU1JVEVEIFRPIExPU1MgT0YKIERBVEEgT1IgREFUQSBCRUlORyBSRU5ERVJFRCBJTkFDQ1VSQVRFIE9SIExPU1NFUyBTVVNUQUlORUQgQlkgWU9VIE9SIFRISVJECiBQQVJUSUVTIE9SIEEgRkFJTFVSRSBPRiBUSEUgUFJPR1JBTSBUTyBPUEVSQVRFIFdJVEggQU5ZIE9USEVSIFBST0dSQU1TKSwKIEVWRU4gSUYgU1VDSCBIT0xERVIgT1IgT1RIRVIgUEFSVFkgSEFTIEJFRU4gQURWSVNFRCBPRiBUSEUgUE9TU0lCSUxJVFkgT0YKIFNVQ0ggREFNQUdFUy4KCiAgIDE3LiBJbnRlcnByZXRhdGlvbiBvZiBTZWN0aW9ucyAxNSBhbmQgMTYuCgogICBJZiB0aGUgZGlzY2xhaW1lciBvZiB3YXJyYW50eSBhbmQgbGltaXRhdGlvbiBvZiBsaWFiaWxpdHkgcHJvdmlkZWQKIGFib3ZlIGNhbm5vdCBiZSBnaXZlbiBsb2NhbCBsZWdhbCBlZmZlY3QgYWNjb3JkaW5nIHRvIHRoZWlyIHRlcm1zLAogcmV2aWV3aW5nIGNvdXJ0cyBzaGFsbCBhcHBseSBsb2NhbCBsYXcgdGhhdCBtb3N0IGNsb3NlbHkgYXBwcm94aW1hdGVzCiBhbiBhYnNvbHV0ZSB3YWl2ZXIgb2YgYWxsIGNpdmlsIGxpYWJpbGl0eSBpbiBjb25uZWN0aW9uIHdpdGggdGhlCiBQcm9ncmFtLCB1bmxlc3MgYSB3YXJyYW50eSBvciBhc3N1bXB0aW9uIG9mIGxpYWJpbGl0eSBhY2NvbXBhbmllcyBhCiBjb3B5IG9mIHRoZSBQcm9ncmFtIGluIHJldHVybiBmb3IgYSBmZWUuCgogICAgICAgICAgICAgICAgICAgICAgRU5EIE9GIFRFUk1TIEFORCBDT05ESVRJT05TCgogICAgICAgICAgICAgSG93IHRvIEFwcGx5IFRoZXNlIFRlcm1zIHRvIFlvdXIgTmV3IFByb2dyYW1zCgogICBJZiB5b3UgZGV2ZWxvcCBhIG5ldyBwcm9ncmFtLCBhbmQgeW91IHdhbnQgaXQgdG8gYmUgb2YgdGhlIGdyZWF0ZXN0CiBwb3NzaWJsZSB1c2UgdG8gdGhlIHB1YmxpYywgdGhlIGJlc3Qgd2F5IHRvIGFjaGlldmUgdGhpcyBpcyB0byBtYWtlIGl0CiBmcmVlIHNvZnR3YXJlIHdoaWNoIGV2ZXJ5b25lIGNhbiByZWRpc3RyaWJ1dGUgYW5kIGNoYW5nZSB1bmRlciB0aGVzZSB0ZXJtcy4KCiAgIFRvIGRvIHNvLCBhdHRhY2ggdGhlIGZvbGxvd2luZyBub3RpY2VzIHRvIHRoZSBwcm9ncmFtLiAgSXQgaXMgc2FmZXN0CiB0byBhdHRhY2ggdGhlbSB0byB0aGUgc3RhcnQgb2YgZWFjaCBzb3VyY2UgZmlsZSB0byBtb3N0IGVmZmVjdGl2ZWx5CiBzdGF0ZSB0aGUgZXhjbHVzaW9uIG9mIHdhcnJhbnR5OyBhbmQgZWFjaCBmaWxlIHNob3VsZCBoYXZlIGF0IGxlYXN0CiB0aGUgImNvcHlyaWdodCIgbGluZSBhbmQgYSBwb2ludGVyIHRvIHdoZXJlIHRoZSBmdWxsIG5vdGljZSBpcyBmb3VuZC4KCiAgICAgPG9uZSBsaW5lIHRvIGdpdmUgdGhlIHByb2dyYW0ncyBuYW1lIGFuZCBhIGJyaWVmIGlkZWEgb2Ygd2hhdCBpdCBkb2VzLj4KICAgICBDb3B5cmlnaHQgKEMpIDx5ZWFyPiAgPG5hbWUgb2YgYXV0aG9yPgoKICAgICBUaGlzIHByb2dyYW0gaXMgZnJlZSBzb2Z0d2FyZTogeW91IGNhbiByZWRpc3RyaWJ1dGUgaXQgYW5kL29yIG1vZGlmeQogICAgIGl0IHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgR05VIEdlbmVyYWwgUHVibGljIExpY2Vuc2UgYXMgcHVibGlzaGVkIGJ5CiAgICAgdGhlIEZyZWUgU29mdHdhcmUgRm91bmRhdGlvbiwgZWl0aGVyIHZlcnNpb24gMyBvZiB0aGUgTGljZW5zZSwgb3IKICAgICAoYXQgeW91ciBvcHRpb24pIGFueSBsYXRlciB2ZXJzaW9uLgoKICAgICBUaGlzIHByb2dyYW0gaXMgZGlzdHJpYnV0ZWQgaW4gdGhlIGhvcGUgdGhhdCBpdCB3aWxsIGJlIHVzZWZ1bCwKICAgICBidXQgV0lUSE9VVCBBTlkgV0FSUkFOVFk7IHdpdGhvdXQgZXZlbiB0aGUgaW1wbGllZCB3YXJyYW50eSBvZgogICAgIE1FUkNIQU5UQUJJTElUWSBvciBGSVRORVNTIEZPUiBBIFBBUlRJQ1VMQVIgUFVSUE9TRS4gIFNlZSB0aGUKICAgICBHTlUgR2VuZXJhbCBQdWJsaWMgTGljZW5zZSBmb3IgbW9yZSBkZXRhaWxzLgoKICAgICBZb3Ugc2hvdWxkIGhhdmUgcmVjZWl2ZWQgYSBjb3B5IG9mIHRoZSBHTlUgR2VuZXJhbCBQdWJsaWMgTGljZW5zZQogICAgIGFsb25nIHdpdGggdGhpcyBwcm9ncmFtLiAgSWYgbm90LCBzZWUgPGh0dHA6Ly93d3cuZ251Lm9yZy9saWNlbnNlcy8+LgoKIEFsc28gYWRkIGluZm9ybWF0aW9uIG9uIGhvdyB0byBjb250YWN0IHlvdSBieSBlbGVjdHJvbmljIGFuZCBwYXBlciBtYWlsLgoKICAgSWYgdGhlIHByb2dyYW0gZG9lcyB0ZXJtaW5hbCBpbnRlcmFjdGlvbiwgbWFrZSBpdCBvdXRwdXQgYSBzaG9ydAogbm90aWNlIGxpa2UgdGhpcyB3aGVuIGl0IHN0YXJ0cyBpbiBhbiBpbnRlcmFjdGl2ZSBtb2RlOgoKICAgICA8cHJvZ3JhbT4gIENvcHlyaWdodCAoQykgPHllYXI+ICA8bmFtZSBvZiBhdXRob3I+CiAgICAgVGhpcyBwcm9ncmFtIGNvbWVzIHdpdGggQUJTT0xVVEVMWSBOTyBXQVJSQU5UWTsgZm9yIGRldGFpbHMgdHlwZSBgc2hvdyB3Jy4KICAgICBUaGlzIGlzIGZyZWUgc29mdHdhcmUsIGFuZCB5b3UgYXJlIHdlbGNvbWUgdG8gcmVkaXN0cmlidXRlIGl0CiAgICAgdW5kZXIgY2VydGFpbiBjb25kaXRpb25zOyB0eXBlIGBzaG93IGMnIGZvciBkZXRhaWxzLgoKIFRoZSBoeXBvdGhldGljYWwgY29tbWFuZHMgYHNob3cgdycgYW5kIGBzaG93IGMnIHNob3VsZCBzaG93IHRoZSBhcHByb3ByaWF0ZQogcGFydHMgb2YgdGhlIEdlbmVyYWwgUHVibGljIExpY2Vuc2UuICBPZiBjb3Vyc2UsIHlvdXIgcHJvZ3JhbSdzIGNvbW1hbmRzCiBtaWdodCBiZSBkaWZmZXJlbnQ7IGZvciBhIEdVSSBpbnRlcmZhY2UsIHlvdSB3b3VsZCB1c2UgYW4gImFib3V0IGJveCIuCgogICBZb3Ugc2hvdWxkIGFsc28gZ2V0IHlvdXIgZW1wbG95ZXIgKGlmIHlvdSB3b3JrIGFzIGEgcHJvZ3JhbW1lcikgb3Igc2Nob29sLAogaWYgYW55LCB0byBzaWduIGEgImNvcHlyaWdodCBkaXNjbGFpbWVyIiBmb3IgdGhlIHByb2dyYW0sIGlmIG5lY2Vzc2FyeS4KIEZvciBtb3JlIGluZm9ybWF0aW9uIG9uIHRoaXMsIGFuZCBob3cgdG8gYXBwbHkgYW5kIGZvbGxvdyB0aGUgR05VIEdQTCwgc2VlCiA8aHR0cDovL3d3dy5nbnUub3JnL2xpY2Vuc2VzLz4uCgogICBUaGUgR05VIEdlbmVyYWwgUHVibGljIExpY2Vuc2UgZG9lcyBub3QgcGVybWl0IGluY29ycG9yYXRpbmcgeW91ciBwcm9ncmFtCiBpbnRvIHByb3ByaWV0YXJ5IHByb2dyYW1zLiAgSWYgeW91ciBwcm9ncmFtIGlzIGEgc3Vicm91dGluZSBsaWJyYXJ5LCB5b3UKIG1heSBjb25zaWRlciBpdCBtb3JlIHVzZWZ1bCB0byBwZXJtaXQgbGlua2luZyBwcm9wcmlldGFyeSBhcHBsaWNhdGlvbnMgd2l0aAogdGhlIGxpYnJhcnkuICBJZiB0aGlzIGlzIHdoYXQgeW91IHdhbnQgdG8gZG8sIHVzZSB0aGUgR05VIExlc3NlciBHZW5lcmFsCiBQdWJsaWMgTGljZW5zZSBpbnN0ZWFkIG9mIHRoaXMgTGljZW5zZS4gIEJ1dCBmaXJzdCwgcGxlYXNlIHJlYWQKIDxodHRwOi8vd3d3LmdudS5vcmcvcGhpbG9zb3BoeS93aHktbm90LWxncGwuaHRtbD4uCg==")
    $hasher = [System.Security.Cryptography.SHA256]::Create()
    try {
        $scipyGateDigest = [System.BitConverter]::ToString($hasher.ComputeHash($scipyGateBytes)).Replace("-", "")
    }
    finally {
        $hasher.Dispose()
    }
    $reReview = "Re-review on any version, gate value, role, modification, vendoring, packaging, or distribution change; retain all license files and bundled notices before any distribution."
    $entries = @{
        "numpy|2.5.3|BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0" = @{
            Role = "transitive numeric runtime for the Phase 3 slice's scikit-learn operations"
            ReReview = $reReview
        }
    }
    if ($scipyGateDigest -eq "7F2F9E131A09F25323E392AAC37FB2E263C600BB9D1FFC7C3B6CA3E1D017573E") {
        $scipyGateValue = [System.Text.Encoding]::UTF8.GetString($scipyGateBytes)
        $entries["scipy|1.18.1|$scipyGateValue"] = @{
            Role = "transitive scientific runtime for scikit-learn in the Phase 3 slice"
            ReReview = $reReview
        }
    }

    $key = "$Name|$Version|$License"
    if (-not $entries.ContainsKey($key)) {
        return $null
    }

    return [pscustomobject]@{
        RecordId = "0005"
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
    if ($null -eq $catalogEntry) {
        $catalogEntry = Get-Decision0004CatalogEntry -Name $Name -Version $Version -License $License
    }
    if ($null -eq $catalogEntry) {
        $catalogEntry = Get-Decision0005CatalogEntry -Name $Name -Version $Version -License $License
    }
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
