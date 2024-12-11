@echo off

rem Set the environment name
set ENV_NAME=pyoccenv

rem Check if the conda environment exists
call conda env list | findstr /r /c:"^%ENV_NAME% " >nul
if %ERRORLEVEL% equ 0 (
    echo Environment '%ENV_NAME%' exists. Activating...
    call conda activate %ENV_NAME%
) else (
    echo Adding conda-forge channel...
    call conda config --add channels conda-forge
    echo Environment '%ENV_NAME%' does not exist. Creating...
    call conda create --name %ENV_NAME% python=3.9 --yes
    echo Environment created, activating...
    call conda activate %ENV_NAME%
    echo ...and installing packages...
    call conda install pythonocc-core --yes -c conda-forge
    call pip install -r requirements.txt
    echo Environment setup complete.
)

uvicorn app:app --host 0.0.0.0 --port 8000