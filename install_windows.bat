@echo off
echo ========================================
echo   IKER2YT - INSTALADOR AUTOMATICO
echo ========================================
echo.
echo Instalando Python y dependencias...
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo Python no encontrado. Descargando e instalando...
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe' -OutFile 'python-installer.exe'"
    python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python-installer.exe
)

echo Instalando dependencias...
pip install yt-dlp

echo.
echo ¡Instalación completada!
echo.
echo Para usar: Ejecuta "run_iker2yt.bat"
echo.
pause
