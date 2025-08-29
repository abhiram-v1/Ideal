@echo off
echo ========================================
echo   PDF Converter App - .exe Builder
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

echo Building standalone .exe file...
echo This will create a Windows app that runs without Python!
echo.

REM Run the build script
python build_exe.py

echo.
echo Build process completed!
echo Check the 'dist' folder for your .exe file.
echo.
pause
