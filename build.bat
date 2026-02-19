@echo off
setlocal enabledelayedexpansion

:: Usage: build.bat <version>
:: Example: build.bat 1.0.0

set VERSION=%~1
if "%VERSION%"=="" (
    echo Usage: build.bat ^<version^>
    echo Example: build.bat 1.0.0
    exit /b 1
)

echo.
echo ============================================================
echo  mineLogger Windows Installer Build  v%VERSION%
echo ============================================================
echo.

:: ------------------------------------------------------------
:: [1/5] Preflight checks
:: ------------------------------------------------------------
echo [1/5] Running preflight checks...

python --version >nul 2>&1
if errorlevel 1 (
    echo   ERROR: python not found on PATH.
    exit /b 1
)
echo   OK  python

pyinstaller --version >nul 2>&1
if errorlevel 1 (
    echo   ERROR: pyinstaller not found. Run: pip install pyinstaller
    exit /b 1
)
echo   OK  pyinstaller

set ISCC_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe
if not exist "%ISCC_PATH%" (
    set ISCC_PATH=C:\Program Files\Inno Setup 6\ISCC.exe
)
if not exist "%ISCC_PATH%" (
    echo   ERROR: Inno Setup 6 not found at default paths.
    echo          Install from https://jrsoftware.org/isinfo.php
    exit /b 1
)
echo   OK  Inno Setup 6

if not exist "minelogger.spec" (
    echo   ERROR: minelogger.spec not found in current directory.
    exit /b 1
)
echo   OK  minelogger.spec

if not exist "installer.iss" (
    echo   ERROR: installer.iss not found in current directory.
    exit /b 1
)
echo   OK  installer.iss

echo.

:: ------------------------------------------------------------
:: [2/5] Clean previous artifacts
:: ------------------------------------------------------------
echo [2/5] Cleaning build/, dist/, installer_output/...

if exist build\          rmdir /s /q build
if exist dist\           rmdir /s /q dist
if exist installer_output\ rmdir /s /q installer_output

echo   Done.
echo.

:: ------------------------------------------------------------
:: [3/5] PyInstaller — build onedir bundle
:: ------------------------------------------------------------
echo [3/5] Running PyInstaller...

python -m PyInstaller minelogger.spec --noconfirm
if errorlevel 1 (
    echo   ERROR: PyInstaller failed.
    exit /b 1
)

if not exist "dist\minelogger\minelogger.exe" (
    echo   ERROR: Expected dist\minelogger\minelogger.exe not found after build.
    exit /b 1
)
echo   OK  dist\minelogger\ created.
echo.

:: ------------------------------------------------------------
:: [4/5] Inno Setup — create installer
:: ------------------------------------------------------------
echo [4/5] Running Inno Setup...

"%ISCC_PATH%" installer.iss /DMyAppVersion=%VERSION%
if errorlevel 1 (
    echo   ERROR: Inno Setup failed.
    exit /b 1
)
echo   OK  Inno Setup complete.
echo.

:: ------------------------------------------------------------
:: [5/5] Report
:: ------------------------------------------------------------
echo [5/5] Build complete.
echo.
echo   Output: installer_output\minelogger-setup.exe
echo.

if exist "installer_output\minelogger-setup.exe" (
    for %%F in ("installer_output\minelogger-setup.exe") do (
        set SIZE=%%~zF
        set /a SIZE_KB=!SIZE! / 1024
        echo   Size:   !SIZE_KB! KB
    )
)

echo.
echo ============================================================
endlocal
