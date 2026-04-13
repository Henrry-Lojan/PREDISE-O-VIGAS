@echo off
title Lanzador de Suite Estructural - Henrry Lojan
echo ==========================================
echo    INICIANDO SUITE ESTRUCTURAL PROFESIONAL
echo ==========================================
echo.
echo [1/2] Limpiando procesos anteriores...
taskkill /f /im python.exe >nul 2>&1
echo [2/2] Arrancando servidor local en Puerto 3000...
start /b python -m http.server 3000
timeout /t 2 /nobreak >nul
echo.
echo Lanzando Suite en Chrome...
start chrome http://localhost:3000/Suite_Estructural_Unificada.html
echo.
echo [LISTO] No cierres esta ventana mientras uses la Suite.
echo ==========================================
pause
