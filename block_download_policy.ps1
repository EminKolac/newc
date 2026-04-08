<#
.SYNOPSIS
    Enable/Disable BlockDownloadPolicy on ALL SharePoint sites for Usul Academy.
    Site owners are always excluded (can still download).

.DESCRIPTION
    - ON:  Blocks download for all non-owner users on every site
    - OFF: Removes the block, restoring normal download for everyone

.USAGE
    # First time: install the module
    Install-Module -Name Microsoft.Online.SharePoint.PowerShell -Force

    # Connect (you'll be prompted to sign in as admin)
    Connect-SPOService -Url https://usulacademy-admin.sharepoint.com

    # Enable block on all sites
    .\block_download_policy.ps1 -Action ON

    # Disable block on all sites (undo)
    .\block_download_policy.ps1 -Action OFF

    # Preview only (no changes)
    .\block_download_policy.ps1 -Action ON -DryRun

.NOTES
    Requires: SharePoint Online Management Shell
    Admin URL: https://usulacademy-admin.sharepoint.com
    This blocks ALL file types (not just videos).
    Site owners are excluded via -ExcludeBlockDownloadPolicySiteOwners
#>

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("ON", "OFF")]
    [string]$Action,

    [switch]$DryRun
)

# ── Get all sites ──
Write-Host "`n[*] Fetching all SharePoint sites..." -ForegroundColor Cyan
$sites = Get-SPOSite -Limit ALL

Write-Host "[*] Found $($sites.Count) sites" -ForegroundColor Cyan

$successCount = 0
$errorCount = 0
$skippedCount = 0
$logEntries = @()

foreach ($site in $sites) {
    $url = $site.Url
    $title = $site.Title

    # Skip admin, search, and system sites
    if ($url -match "-admin\.sharepoint\.com|search\.sharepoint\.com|\.sharepoint\.com/portals|\.sharepoint\.com/sites/appcatalog") {
        Write-Host "  [SKIP] $title ($url) - system site" -ForegroundColor DarkGray
        $skippedCount++
        continue
    }

    if ($Action -eq "ON") {
        if ($DryRun) {
            Write-Host "  [DRY-RUN] Would ENABLE BlockDownloadPolicy on: $title ($url)" -ForegroundColor Yellow
            $successCount++
        } else {
            try {
                Set-SPOSite -Identity $url -BlockDownloadPolicy $true -ExcludeBlockDownloadPolicySiteOwners $true
                Write-Host "  [OK] ENABLED BlockDownloadPolicy on: $title" -ForegroundColor Green
                $successCount++
                $logEntries += @{
                    action = "enabled"
                    site = $title
                    url = $url
                    timestamp = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
                }
            } catch {
                Write-Host "  [ERROR] Failed on $title : $_" -ForegroundColor Red
                $errorCount++
                $logEntries += @{
                    action = "error_enable"
                    site = $title
                    url = $url
                    error = $_.ToString()
                    timestamp = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
                }
            }
        }
    } else {
        # Action = OFF
        if ($DryRun) {
            Write-Host "  [DRY-RUN] Would DISABLE BlockDownloadPolicy on: $title ($url)" -ForegroundColor Yellow
            $successCount++
        } else {
            try {
                Set-SPOSite -Identity $url -BlockDownloadPolicy $false
                Write-Host "  [OK] DISABLED BlockDownloadPolicy on: $title" -ForegroundColor Green
                $successCount++
                $logEntries += @{
                    action = "disabled"
                    site = $title
                    url = $url
                    timestamp = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
                }
            } catch {
                Write-Host "  [ERROR] Failed on $title : $_" -ForegroundColor Red
                $errorCount++
                $logEntries += @{
                    action = "error_disable"
                    site = $title
                    url = $url
                    error = $_.ToString()
                    timestamp = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
                }
            }
        }
    }
}

# ── Save log ──
if (-not $DryRun -and $logEntries.Count -gt 0) {
    $logFile = "block_download_policy_log.json"
    $logEntries | ConvertTo-Json -Depth 3 | Out-File -FilePath $logFile -Encoding UTF8
    Write-Host "`n[*] Log saved to $logFile" -ForegroundColor Cyan
}

# ── Summary ──
$modeText = if ($DryRun) { " (DRY RUN)" } else { "" }
Write-Host "`n============================================================" -ForegroundColor White
Write-Host "  BLOCK DOWNLOAD POLICY - $Action$modeText" -ForegroundColor White
Write-Host "============================================================" -ForegroundColor White
Write-Host "  Total sites:    $($sites.Count)"
Write-Host "  Processed:      $successCount"
Write-Host "  Skipped:        $skippedCount (system sites)"
Write-Host "  Errors:         $errorCount"
Write-Host "============================================================" -ForegroundColor White

if ($Action -eq "ON") {
    Write-Host "`n  All non-owner users are now BLOCKED from downloading ANY file." -ForegroundColor Yellow
    Write-Host "  Site owners can still download." -ForegroundColor Green
    Write-Host "  To undo: .\block_download_policy.ps1 -Action OFF" -ForegroundColor Cyan
} else {
    Write-Host "`n  Download policy REMOVED from all sites." -ForegroundColor Green
    Write-Host "  All users can download again." -ForegroundColor Yellow
}
