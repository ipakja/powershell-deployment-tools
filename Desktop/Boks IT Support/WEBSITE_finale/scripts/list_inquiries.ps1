<#
.SYNOPSIS
  List recent BIT inquiry leads from the protected /api/inquiries endpoint.

.PARAMETER Token
  Value of INQUIRY_VIEW_TOKEN (or INQUIRY_DIAG_TOKEN fallback).

.PARAMETER Limit
  Number of recent keys (1–50). Default 20.

.PARAMETER BaseUrl
  Site origin. Default https://boksitsupport.ch
#>
param(
  [Parameter(Mandatory = $true)]
  [string]$Token,

  [ValidateRange(1, 50)]
  [int]$Limit = 20,

  [string]$BaseUrl = "https://boksitsupport.ch"
)

$ErrorActionPreference = "Stop"
$uri = "{0}/api/inquiries?token={1}&limit={2}" -f $BaseUrl.TrimEnd("/"), [uri]::EscapeDataString($Token), $Limit

Write-Host "GET $BaseUrl/api/inquiries?limit=$Limit …"

$response = Invoke-RestMethod -Method Get -Uri $uri -Headers @{
  "Cache-Control" = "no-store"
  "Pragma"        = "no-cache"
}

if (-not $response.ok) {
  Write-Error ("API returned ok=false: " + ($response | ConvertTo-Json -Compress))
  exit 1
}

Write-Host ("count={0}" -f $response.count)
Write-Host ""

foreach ($item in $response.items) {
  Write-Host ("---- {0}" -f $item.key)
  Write-Host ("  receivedAt : {0}" -f $item.receivedAt)
  Write-Host ("  requestId  : {0}" -f $item.requestId)
  Write-Host ("  company    : {0}" -f $item.company)
  Write-Host ("  contact    : {0}" -f $item.contact)
  Write-Host ("  email      : {0}" -f $item.email)
  Write-Host ("  area       : {0}" -f $item.area)
  Write-Host ("  start      : {0}" -f $item.start)
  Write-Host ("  description: {0}" -f $item.description)
  Write-Host ""
}
