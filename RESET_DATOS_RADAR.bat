@echo off
cd /d "%~dp0"
echo ==========================================
echo   RESET DATOS - RIPPLE RADAR PRO
echo ==========================================
echo.
echo Esto borra la base local y el radar empezara desde cero.
echo Cierra Streamlit antes de continuar.
echo.
pause
if exist "ripple_radar_advanced.sqlite" del /f /q "ripple_radar_advanced.sqlite"
if exist "ripple_radar_advanced.sqlite-wal" del /f /q "ripple_radar_advanced.sqlite-wal"
if exist "ripple_radar_advanced.sqlite-shm" del /f /q "ripple_radar_advanced.sqlite-shm"
if exist "ripple_radar_advanced.sqlite-journal" del /f /q "ripple_radar_advanced.sqlite-journal"
if exist "__pycache__" rmdir /s /q "__pycache__"
echo.
echo Base borrada. Arranca EJECUTAR_RADAR.bat para crear una nueva.
echo.
pause
