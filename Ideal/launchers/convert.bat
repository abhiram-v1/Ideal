@echo off
echo ========================================
echo   Jupyter Notebook to PDF Converter
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

REM Check if notebook file exists
if exist "Lab_2.ipynb" (
    echo Found Lab_2.ipynb - Converting to PDF...
    python ultimate_converter.py
) else (
    echo No Lab_2.ipynb found in current directory
    echo.
    echo To convert a specific notebook:
    echo 1. Drag and drop your .ipynb file onto this .bat file
    echo 2. Or run: python ultimate_converter.py your_notebook.ipynb
    echo.
    pause
)

echo.
echo Conversion complete! Press any key to exit...
pause >nul
