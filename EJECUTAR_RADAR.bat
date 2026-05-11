@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo ==========================================
echo   RIPPLE RADAR PRO - v69 LIMPIO
echo ==========================================
echo.

where py >nul 2>nul
if not errorlevel 1 (
    set "PYTHON_CMD=py -3"
) else (
    set "PYTHON_CMD=python"
)

if not exist ".venv" (
    echo Creando entorno virtual .venv ...
    %PYTHON_CMD% -m venv .venv
)

call .venv\Scripts\activate.bat

if not exist ".deps_installed_v69.flag" (
    echo Instalando dependencias ...
    python -m pip install --upgrade pip setuptools wheel
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo ERROR instalando dependencias. Revisa tu conexion o Python.
        pause
        exit /b 1
    )
    echo ok > .deps_installed_v69.flag
)

echo.
echo Abriendo radar...
echo Si la app no se abre sola, copia la URL que aparezca en consola.
echo.
streamlit run ripple_radar_pro_route_engine_v69_DEDUCTIVE_ENGINE_PROOFS.py

pause
endlocal
