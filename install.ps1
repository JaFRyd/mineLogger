#Requires -Version 5.1
<#
.SYNOPSIS
    Installs mineLogger for the current user (no admin rights required).

.DESCRIPTION
    - Creates a Python virtual environment in .venv
    - Installs dependencies from requirements.txt
    - Writes a port.txt configuration file
    - Adds a Windows registry Run key so mineLogger starts silently at login
    - Creates a Start Menu shortcut to open the UI

.PARAMETER Port
    Port the web server listens on. Defaults to 5001.

.EXAMPLE
    .\install.ps1
    .\install.ps1 -Port 8080
#>

param(
    [ValidateRange(1024, 65535)]
    [int]$Port = 5001
)

$ErrorActionPreference = "Stop"
$AppName    = "mineLogger"
$InstallDir = $PSScriptRoot

Write-Host ""
Write-Host "============================================================"
Write-Host "  mineLogger Setup"
Write-Host "============================================================"
Write-Host ""

# ------------------------------------------------------------------
# [1/5] Check Python
# ------------------------------------------------------------------
Write-Host "[1/5] Checking Python..."
try {
    $pyVersion = & python --version 2>&1
    Write-Host "  OK  $pyVersion"
} catch {
    Write-Error "Python not found on PATH. Install Python 3.8+ and try again."
}

# ------------------------------------------------------------------
# [2/5] Create / update virtual environment
# ------------------------------------------------------------------
Write-Host "[2/5] Setting up virtual environment..."
$VenvDir  = Join-Path $InstallDir ".venv"
$PipExe   = Join-Path $VenvDir "Scripts\pip.exe"
$PythonExe = Join-Path $VenvDir "Scripts\python.exe"

if (-not (Test-Path $VenvDir)) {
    & python -m venv $VenvDir
    Write-Host "  Created .venv"
} else {
    Write-Host "  Already exists, skipping"
}

# ------------------------------------------------------------------
# [3/5] Install dependencies
# ------------------------------------------------------------------
Write-Host "[3/5] Installing dependencies..."
& $PipExe install -r (Join-Path $InstallDir "requirements.txt") --quiet
Write-Host "  OK"

# ------------------------------------------------------------------
# [4/5] Write port.txt
# ------------------------------------------------------------------
Write-Host "[4/5] Configuring port..."
$Port | Out-File -FilePath (Join-Path $InstallDir "port.txt") -Encoding ASCII -NoNewline
Write-Host "  OK  Using port $Port"

# ------------------------------------------------------------------
# [5/5] Autostart registry key + Start Menu shortcut
# ------------------------------------------------------------------
Write-Host "[5/5] Setting up autostart and Start Menu shortcut..."

$MainPy = Join-Path $InstallDir "main.py"

# VBS that starts the server silently (no window) — used for autostart
$SilentVbs = Join-Path $InstallDir "start-python-silent.vbs"
@"
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run """$PythonExe"" ""$MainPy"" ui --no-browser --port $Port", 0, False
"@ | Set-Content -Path $SilentVbs -Encoding ASCII

# VBS that starts the server and opens the browser — used for Start Menu
$UiVbs = Join-Path $InstallDir "start-python-ui.vbs"
@"
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run """$PythonExe"" ""$MainPy"" ui --port $Port", 0, False
WScript.Sleep 2000
WshShell.Run "explorer ""http://localhost:$Port""", 0, False
"@ | Set-Content -Path $UiVbs -Encoding ASCII

# Registry Run key (current user — no admin needed)
$RegPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
Set-ItemProperty -Path $RegPath -Name $AppName -Value "wscript.exe ""$SilentVbs"""
Write-Host "  OK  Autostart registry key set"

# Start Menu shortcut
$ShortcutDir = Join-Path ([Environment]::GetFolderPath("Programs")) $AppName
if (-not (Test-Path $ShortcutDir)) {
    New-Item -ItemType Directory -Path $ShortcutDir | Out-Null
}
$WshShell  = New-Object -ComObject WScript.Shell
$Shortcut  = $WshShell.CreateShortcut((Join-Path $ShortcutDir "$AppName.lnk"))
$Shortcut.TargetPath      = "wscript.exe"
$Shortcut.Arguments       = """$UiVbs"""
$Shortcut.WorkingDirectory = $InstallDir
$Shortcut.Description     = "Open mineLogger web UI"
$Shortcut.Save()
Write-Host "  OK  Start Menu shortcut created"

Write-Host ""
Write-Host "============================================================"
Write-Host "  Installation complete!"
Write-Host ""
Write-Host "  mineLogger will start automatically at next login."
Write-Host "  Use the Start Menu shortcut to open the UI at any time."
Write-Host "  URL: http://localhost:$Port"
Write-Host "============================================================"
Write-Host ""
