@echo off
chcp 65001 >nul
setlocal ENABLEDELAYEDEXPANSION

title Instalador do Projeto

set "DIR=windows_ricer"
set "SCRIPT=instalador.py"
set "RAW_URL=https://raw.githubusercontent.com/tsukum0/python-projects/refs/heads/main/rice-windows/resources/v1.py"
set "PYTHON_VERSION=3.11.9"
set "PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-amd64.exe"
set "PYTHON_INSTALLER=python_installer.exe"

python --version >nul 2>&1
if %errorlevel% NEQ 0 (
    echo [[31mFAIL[0m] Python nao encontrado neste sistema.

    set /p "baixar=Deseja baixar e instalar o Python %PYTHON_VERSION% agora? (s/n): "
    if /i "!baixar!"=="s" (
        echo [[33mINFO[0m] Baixando instalador do Python...
        curl -L -o %PYTHON_INSTALLER% %PYTHON_URL%
        echo [[33mINFO[0m] Abrindo instalador do Python. Siga as instrucoes na tela.
        start "" %PYTHON_INSTALLER%
        pause
    ) else (
        echo [[31mFAIL[0m] Instalacao cancelada pelo usuario.
        exit /b
    )
)

python --version >nul 2>&1
if %errorlevel% NEQ 0 (
    echo [[31mFAIL[0m] Python ainda nao esta instalado. Abortando.
    exit /b
)

echo [[32mOK[0m] Python detectado.

:: Verifica pip
pip --version >nul 2>&1
if %errorlevel% NEQ 0 (
    echo [INFO] pip nao encontrado. Instalando...
    python -m ensurepip --default-pip
    python -m pip install --upgrade pip
)

echo [OK] pip pronto.

:: Instalar dependencias: requests e colorama
echo [INFO] Instalando bibliotecas 'requests' e 'colorama'...
python -m pip install requests colorama
if %errorlevel% EQU 0 (
    echo [OK] Bibliotecas instaladas com sucesso.
) else (
    echo [FAIL] Falha ao instalar as bibliotecas.
    pause
    exit /b
)
:: Cria a pasta do projeto
if not exist %DIR% (
    mkdir %DIR%
    echo [+] Pasta %DIR% criada.
) else (
    echo [i] Pasta %DIR% ja existe.
)

:: Baixar instalador.py do GitHub Raw

set "FULLPATH=%DIR%\%SCRIPT%"
echo [[33mINFO[0m] Baixando %SCRIPT% do GitHub...
curl -L -o "!FULLPATH!" %RAW_URL%

if exist "!FULLPATH!" (
    echo [[32mOK[0m] Arquivo %SCRIPT% salvo com sucesso em !FULLPATH!
) else (
    echo [[31mFAIL[0m] Falha ao baixar %SCRIPT%. Verifique o link.
    pause
    exit /b
)

set /p "exec=Deseja executar o instalador agora? (s/n): "
if /i "!exec!"=="s" (
    python "!FULLPATH!"
)

echo.
echo [[32mOK[0m] Processo finalizado.
pause
