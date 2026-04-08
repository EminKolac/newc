<#
.SYNOPSIS
    Turn OFF BlockDownloadPolicy on Kalam III sites ONLY.
    Then videos are protected by preventsDownload links only.

.USAGE
    Connect-SPOService -Url https://usulacademy-admin.sharepoint.com
    .\fix_kalam3_policy.ps1
    .\fix_kalam3_policy.ps1 -DryRun    # preview only
#>

param(
    [switch]$DryRun
)

Write-Host "`n[*] Fetching all SharePoint sites..." -ForegroundColor Cyan
$sites = Get-SPOSite -Limit ALL

# Filter for Kalam sites
$kalamSites = $sites | Where-Object { $_.Title -match "(?i)kalam" }

Write-Host "[*] Found $($kalamSites.Count) Kalam site(s):" -ForegroundColor Cyan
foreach ($site in $kalamSites) {
    Write-Host "  - $($site.Title) ($($site.Url))" -ForegroundColor Yellow
}

if ($kalamSites.Count -eq 0) {
    Write-Host "`n[!] No Kalam sites found. Listing all sites:" -ForegroundColor Red
    foreach ($site in $sites) {
        Write-Host "  - $($site.Title) ($($site.Url))"
    }
    exit
}

$success = 0
$errors = 0

foreach ($site in $kalamSites) {
    $url = $site.Url
    $title = $site.Title

    if ($DryRun) {
        Write-Host "  [DRY-RUN] Would DISABLE BlockDownloadPolicy on: $title" -ForegroundColor Yellow
        $success++
    } else {
        try {
            # Turn OFF BlockDownloadPolicy — users can download again
            Set-SPOSite -Identity $url -BlockDownloadPolicy $false
            Write-Host "  [OK] DISABLED BlockDownloadPolicy on: $title" -ForegroundColor Green
            $success++
        } catch {
            Write-Host "  [ERROR] $title : $_" -ForegroundColor Red
            $errors++
        }
    }
}

Write-Host "`n============================================================"
Write-Host "  RESULT: BlockDownloadPolicy OFF on $success Kalam site(s)"
Write-Host "  Errors: $errors"
Write-Host "============================================================"
Write-Host "`n  Students can now VIEW and DOWNLOAD all files." -ForegroundColor Green
Write-Host "  Videos are still protected by preventsDownload links." -ForegroundColor Yellow
Write-Host "  (Students can stream videos but cannot download them)" -ForegroundColor Yellow
