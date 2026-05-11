@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo ==========================================
echo   REINSTALAR DEPENDENCIAS - RIPPLE RADAR

echo ==========================================
echo.

if exist ".venv" (
    echo Eliminando .venv anterior...
    rmdir /s /q ".venv"
)
if exist ".deps_installed_v69.flag" del /f /q ".deps_installed_v69.flag"

echo Ahora ejecuta EJECUTAR_RADAR.bat
pause
endlocal
