#Requires -Version 5.1
<#
.SYNOPSIS
    Removes the mineLogger autostart entry and Start Menu shortcut.

.DESCRIPTION
    Removes the Windows registry Run key and Start Menu shortcut created by
    install.ps1. Your data (~/.minelogger/minelogger.db) is never touched.
#>

$ErrorActionPreference = "Stop"
$AppName = "mineLogger"

Write-Host ""
Write-Host "Uninstalling $AppName autostart and shortcuts..."
Write-Host ""

# Registry Run key
$RegPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
if (Get-ItemProperty -Path $RegPath -Name $AppName -ErrorAction SilentlyContinue) {
    Remove-ItemProperty -Path $RegPath -Name $AppName
    Write-Host "  OK  Autostart registry key removed"
} else {
    Write-Host "  --  No autostart key found"
}

# Start Menu shortcut folder
$ShortcutDir = Join-Path ([Environment]::GetFolderPath("Programs")) $AppName
if (Test-Path $ShortcutDir) {
    Remove-Item -Recurse -Force $ShortcutDir
    Write-Host "  OK  Start Menu shortcut removed"
} else {
    Write-Host "  --  No Start Menu shortcut found"
}

# Generated VBS launchers
foreach ($vbs in @("start-python-silent.vbs", "start-python-ui.vbs")) {
    $path = Join-Path $PSScriptRoot $vbs
    if (Test-Path $path) {
        Remove-Item $path
        Write-Host "  OK  Removed $vbs"
    }
}

Write-Host ""
Write-Host "Done. Your data (~/.minelogger/) was not touched."
Write-Host ""
