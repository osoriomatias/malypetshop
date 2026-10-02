@echo off
title Pellegrini PetShop
echo ===================================================
echo  Iniciando Pellegrini PetShop con Base de Datos
echo ===================================================
python run.py
if errorlevel 1 (
    echo.
    echo Reintentando con el comando 'py'...
    py run.py
)
pause
