# Beispiel PowerShell-Script – installiere Tools mit winget
$apps = @("Google.Chrome", "Microsoft.VisualStudioCode", "7zip.7zip")
foreach ($app in $apps) {
    winget install --id=$app --accept-source-agreements --accept-package-agreements
}
