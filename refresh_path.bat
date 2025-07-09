@echo off
REM ProxyManX PATH Refresh Script
REM Run this if 'proxymanx' command is not recognized after installation

echo Refreshing PATH environment variable...

REM Refresh PATH for current session
for /f "tokens=2*" %%A in ('reg query "HKCU\Environment" /v PATH 2^>nul') do set "userpath=%%B"
for /f "tokens=2*" %%A in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PATH 2^>nul') do set "systempath=%%B"

if defined userpath (
    if defined systempath (
        set "PATH=%userpath%;%systempath%"
    ) else (
        set "PATH=%userpath%"
    )
) else (
    if defined systempath (
        set "PATH=%systempath%"
    )
)

echo PATH refreshed successfully!
echo.
echo Testing ProxyManX command...
proxymanx --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ ProxyManX command is now working!
    echo You can now use: proxymanx help
) else (
    echo ✗ ProxyManX command still not found
    echo Please restart your terminal or use: .\proxymanx.bat
)
echo.
pause
