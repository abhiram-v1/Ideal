#!/bin/bash

echo "========================================"
echo "  Jupyter Notebook to PDF Converter"
echo "========================================"
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "ERROR: Python is not installed"
        echo "Please install Python 3.7+ and try again"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# Check if notebook file exists
if [ -f "Lab_2.ipynb" ]; then
    echo "Found Lab_2.ipynb - Converting to PDF..."
    $PYTHON_CMD ultimate_converter.py
else
    echo "No Lab_2.ipynb found in current directory"
    echo
    echo "To convert a specific notebook:"
    echo "1. Run: $PYTHON_CMD ultimate_converter.py your_notebook.ipynb"
    echo "2. Or copy your .ipynb file here and rename it to Lab_2.ipynb"
    echo
fi

echo
echo "Conversion complete!"
