@echo off

REM Set the environment name
set ENV_NAME=pyoccenv

REM Check if the conda environment exists
conda env list | findstr /r /c:"^%ENV_NAME% " >nul
if %ERRORLEVEL% equ 0 (
    echo "Environment '%ENV_NAME%' exists. Activating..."
    call conda activate %ENV_NAME%
) else (
    echo "Adding conda-forge channel..."
    conda config --add channels conda-forge
    echo "Environment '%ENV_NAME%' does not exist. Creating..."
    conda create --name %ENV_NAME% --yes
    echo "Environment created, activating..."
    call conda activate %ENV_NAME%
    echo "...and installing packages..."
    conda install --file requirements.txt --yes -c conda-forge
    echo "Environment setup complete."
)
python script.py