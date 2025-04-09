# ddc_check.ps1
# A powershell script to run on a citrix ddc to enumerate the citrix instance

asnp Citrix.*

Write-Host "===================================================" -ForegroundColor Green
Write-Host " Citrix Version "
Write-Host "===================================================" -ForegroundColor Green

Get-BrokerController | Select-Object ControllerVersion

Write-Host "===================================================" -ForegroundColor Green
Write-Host " Database Connection String "
Write-Host "===================================================" -ForegroundColor Green

Get-BrokerDBConnection

Write-Host "===================================================" -ForegroundColor Green
Write-Host " Unconfigured Machines "
Write-Host "===================================================" -ForegroundColor Green

Get-BrokerUnconfiguredMachine

Write-Host "===================================================" -ForegroundColor Green
Write-Host " Admin Folder "
Write-Host "===================================================" -ForegroundColor Green

Get-BrokerAdminFolder

Write-Host "===================================================" -ForegroundColor Green
Write-Host " Access Policy Rules "
Write-Host "===================================================" -ForegroundColor Green

Get-BrokerAccessPolicyRule

Write-Host "===================================================" -ForegroundColor Green
Write-Host " Reboot Schedule "
Write-Host "===================================================" -ForegroundColor Green

Get-BrokerRebootScheduleV2

Write-Host "===================================================" -ForegroundColor Green
Write-Host " Application List "
Write-Host " Saving results to c:\windows\temp\citrix_apps.csv "
Write-Host "===================================================" -ForegroundColor Green

Get-BrokerApplication -MaxRecordCount 1000 | Select-Object * | ForEach-Object {
	foreach ($property in $_.PSObject.Properties) {
		if ($property.Value -is [array]) {
			$property.Value = $property.Value -join ','
		}
	}
	$_
} | Export-Csv -Path "c:\windows\temp\citrix_apps.csv" -NoTypeInformation
