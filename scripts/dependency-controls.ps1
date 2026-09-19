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
