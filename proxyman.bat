@echo off
REM ProxyMan Windows - Batch launcher
REM This batch file allows easy execution of ProxyMan on Windows

cd /d "%~dp0"
python proxyman.py %*

REM If Python is not in PATH, try py launcher
if %ERRORLEVEL% neq 0 (
    py proxyman.py %*
)

pause
