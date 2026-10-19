@echo off
setlocal EnableExtensions
title Py2EXE Studio - Requirements Installer
cd /d "%~dp0"

echo.
echo  ============================================
echo       Py2EXE Studio - Setup Requirements
echo  ============================================
echo.

REM Check that Python is installed and available.
where py >nul 2>nul
if %errorlevel%==0 (
    set "PY=py"
    goto :python_found
)

where python >nul 2>nul
if %errorlevel%==0 (
    set "PY=python"
    goto :python_found
)

echo [ERROR] Python was not found.
echo Install Python 3.10 or newer from https://www.python.org/downloads/windows/
echo During installation, enable "Add Python to PATH".
echo Then run this file again.
echo.
pause
exit /b 1

:python_found
echo [1/4] Checking Python...
%PY% --version
if errorlevel 1 (
    echo [ERROR] Python could not be started.
    pause
    exit /b 1
)

echo.
echo [2/4] Updating pip...
%PY% -m pip install --upgrade pip
if errorlevel 1 (
    echo [WARNING] pip upgrade failed. Continuing with the current pip...
)

echo.
echo [3/4] Installing project requirements...
if exist "requirements.txt" (
    %PY% -m pip install -r "requirements.txt"
    if errorlevel 1 (
        echo [ERROR] One or more packages from requirements.txt could not be installed.
        echo Check your internet connection and the error messages above.
        pause
        exit /b 1
    )
) else (
    echo requirements.txt was not found. Installing the required build package directly...
    %PY% -m pip install "pyinstaller>=6.0,<7.0"
    if errorlevel 1 (
        echo [ERROR] PyInstaller installation failed.
        pause
        exit /b 1
    )
)

echo.
echo [4/4] Verifying PyInstaller...
%PY% -m PyInstaller --version
if errorlevel 1 (
    echo [ERROR] PyInstaller verification failed.
    pause
    exit /b 1
)

echo.
echo  ============================================
echo          Setup completed successfully!
echo  ============================================
echo.
echo You can now run the app with:
echo     %PY% main.py
echo.
echo To build Py2EXE Studio into an EXE, run:
echo     %PY% -m PyInstaller --noconfirm --clean --onefile --windowed --name "Py2EXE-Studio" main.py
echo.
pause
exit /b 0
