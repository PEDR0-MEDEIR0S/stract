@echo off
REM Exibe uma mensagem de início
echo Iniciando a instalação das dependências...

REM Verifica se o Python 3 está instalado
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python 3 não encontrado. Por favor, instale o Python 3.
    exit /b 1
)

REM Verifica se o pip está instalado
pip --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Pip não encontrado. Instalando pip...
    python -m ensurepip --upgrade
)

REM Cria um ambiente virtual (opcional, mas recomendado)
echo Criando ambiente virtual...
python -m venv venv

REM Ativa o ambiente virtual
echo Ativando o ambiente virtual...
call venv\Scripts\activate.bat

REM Instala as dependências do requirements.txt
IF EXIST requirements.txt (
    echo Instalando dependências do requirements.txt...
    pip install -r requirements.txt
) ELSE (
    echo Arquivo requirements.txt não encontrado.
    exit /b 1
)

REM Mensagem de conclusão
echo Dependências instaladas com sucesso!

REM Sugestão para rodar o servidor
echo Para rodar o servidor, use o comando:
echo venv\Scripts\activate.bat && python app.py

pause
