@echo off
setlocal ENABLEDELAYEDEXPANSION

title Instalador do Projeto

:: Configurações
set "DIR=meu_projeto"
set "SCRIPT=instalador.py"
set "RAW_URL=https://raw.githubusercontent.com/tsukum0/python-projects/refs/heads/main/rice-windows/resources/v1.py"
set "PYTHON_VERSION=3.11.9"
set "PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-amd64.exe"
set "PYTHON_INSTALLER=python_installer.exe"

:: Verifica se Python está instalado
python --version >nul 2>&1
if %errorlevel% NEQ 0 (
    echo [!] Python nao encontrado neste sistema.

    set /p baixar=Deseja baixar e instalar o Python %PYTHON_VERSION% agora? (s/n): 
    if /i "!baixar!"=="s" (
        echo [*] Baixando instalador do Python...
        curl -L -o %PYTHON_INSTALLER% %PYTHON_URL%
        echo [*] Abrindo instalador do Python. Siga as instrucoes na tela.
        start "" %PYTHON_INSTALLER%
        pause
    ) else (
        echo [X] Instalacao cancelada pelo usuario.
        exit /b
    )
)

:: Verifica novamente
python --version >nul 2>&1
if %errorlevel% NEQ 0 (
    echo [X] Python ainda nao esta instalado. Abortando.
    exit /b
)

echo [✓] Python detectado.

:: Verifica pip
pip --version >nul 2>&1
if %errorlevel% NEQ 0 (
    echo [!] pip nao encontrado. Instalando...
    python -m ensurepip --default-pip
    python -m pip install --upgrade pip
)

echo [✓] pip pronto.

:: Cria a pasta do projeto
if not exist %DIR% (
    mkdir %DIR%
    echo [+] Pasta %DIR% criada.
) else (
    echo [i] Pasta %DIR% ja existe.
)

:: Baixar instalador.py do GitHub Raw
set "FULLPATH=%DIR%\%SCRIPT%"
echo [*] Baixando %SCRIPT% do GitHub...
curl -L -o "!FULLPATH!" %RAW_URL%

if exist "!FULLPATH!" (
    echo [✓] Arquivo %SCRIPT% salvo com sucesso em !FULLPATH!
) else (
    echo [X] Falha ao baixar %SCRIPT%. Verifique o link.
    pause
    exit /b
)

:: Executar?
set /p exec=Deseja executar o instalador agora? (s/n): 
if /i "!exec!"=="s" (
    python "!FULLPATH!"
)

echo.
echo [✓] Processo finalizado.
pause
