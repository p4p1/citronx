# sf_check.ps1
# A powershell script to run on a citrix Store Front Server
# to enumerate the citrix storefronts running in the environment


Write-Host "===================================================" -ForegroundColor Green
Write-Host " Store Front Version "
Write-Host "===================================================" -ForegroundColor Green

Get-STFVersion | Select-Object Major,Minor,Build,Revision

Write-Host "===================================================" -ForegroundColor Green
	Write-Host " Authentication Protocols Available "
Write-Host "===================================================" -ForegroundColor Green

Get-STFAuthenticationProtocolsAvailable

