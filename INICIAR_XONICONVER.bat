@echo off
title XONICONVER v3.2 - Conversor Universal de Archivos
color 0A

:: ============================================================
:: SOLICITAR PERMISOS DE ADMINISTRADOR
:: ============================================================
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Solicitando permisos de administrador...
    echo.
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B
)

:: ============================================================
:: EJECUTAR start.py CON PERMISOS DE ADMINISTRADOR
:: ============================================================
cls
echo ============================================================
echo           XONICONVER v3.2 - Conversor Universal
echo              (Modo Administrador)
echo ============================================================
echo.
echo [OK] Permisos de administrador obtenidos
echo.
echo Iniciando XONICONVER...
echo.
echo [INFO] Conversor de archivos universal
echo [INFO] Funcionalidades disponibles:
echo   • Imagenes → PDF
echo   • Unir PDFs (sin duplicacion)
echo   • PDF → Word (.docx)
echo.
echo [INFO] Accede desde:
echo   • Local: http://localhost:5050
echo   • Red:   http://[TU-IP]:5050
echo.
echo Presiona Ctrl+C para detener el servidor
echo ============================================================
echo.

python start.py

pause
