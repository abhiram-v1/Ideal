#!/usr/bin/env python3
"""
Build Script for PDF Converter App
Converts the Python GUI to a standalone .exe file
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_pyinstaller():
    """Install PyInstaller if not available"""
    try:
        import PyInstaller
        print("✓ PyInstaller already installed")
        return True
    except ImportError:
        print("📦 Installing PyInstaller...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], 
                         check=True, capture_output=True)
            print("✓ PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install PyInstaller: {e}")
            return False

def build_exe():
    """Build the standalone .exe file"""
    print("🔨 Building standalone .exe file...")
    
    # PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                    # Single .exe file
        "--windowed",                   # No console window
        "--name=PDF_Converter_App",     # App name
        "--icon=NONE",                  # No icon (can add later)
        "--add-data=README.md;.",       # Include README
        "--add-data=requirements.txt;.", # Include requirements
        "--add-data=config.py;.",       # Include config
        "--hidden-import=tkinter",      # Ensure tkinter is included
        "--hidden-import=tkinter.ttk",  # Include ttk widgets
        "--hidden-import=tkinter.filedialog", # Include file dialogs
        "--hidden-import=tkinter.messagebox", # Include message boxes
        "gui_converter.py"              # Main script
    ]
    
    try:
        print("Running PyInstaller...")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✓ PyInstaller completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ PyInstaller failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_installer():
    """Create a simple installer package"""
    print("📦 Creating installer package...")
    
    # Create dist folder structure
    dist_dir = Path("dist/PDF_Converter_App")
    dist_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy .exe file
    exe_file = Path("dist/PDF_Converter_App.exe")
    if exe_file.exists():
        shutil.copy2(exe_file, dist_dir / "PDF_Converter_App.exe")
        print("✓ .exe file copied")
    else:
        print("❌ .exe file not found")
        return False
    
    # Copy supporting files
    files_to_copy = [
        "README.md",
        "requirements.txt", 
        "config.py",
        "app_info.txt"
    ]
    
    for file in files_to_copy:
        if Path(file).exists():
            shutil.copy2(file, dist_dir)
            print(f"✓ {file} copied")
    
    # Create launcher batch file
    launcher_content = """@echo off
echo ========================================
echo   PDF Converter App - Launcher
echo ========================================
echo.
echo Starting PDF Converter App...
echo.

REM Launch the app
start "" "PDF_Converter_App.exe"

echo App launched! Check your taskbar.
echo.
pause
"""
    
    with open(dist_dir / "Launch_App.bat", "w") as f:
        f.write(launcher_content)
    print("✓ Launcher batch file created")
    
    # Create README for users
    user_readme = """# 🚀 PDF Converter App - Standalone Version

## 🎯 What You Have
This is a **standalone Windows application** that converts Jupyter Notebooks to PDFs.

## 🚀 How to Use
1. **Double-click `PDF_Converter_App.exe`** to launch the app
2. **Or double-click `Launch_App.bat`** for easy launching
3. **No Python installation required!**

## ✨ Features
- 🖥️ Beautiful GUI interface
- 📁 Easy file selection
- 🎨 Professional PDF output with styling
- 🚀 Fast conversion with Chrome
- 💾 Multiple save location options

## 📁 Files Included
- `PDF_Converter_App.exe` - Main application
- `Launch_App.bat` - Easy launcher
- `README.md` - Detailed documentation
- `config.py` - Configuration options
- `app_info.txt` - App information

## 🆘 Troubleshooting
- **If the app doesn't start**: Right-click and "Run as Administrator"
- **If Chrome is missing**: Install Google Chrome for best results
- **For help**: Check README.md for detailed instructions

## 🎉 Enjoy Your PDF Converter!
Made with ❤️ for the Jupyter community
"""
    
    with open(dist_dir / "USER_README.txt", "w", encoding="utf-8") as f:
        f.write(user_readme)
    print("✓ User README created")
    
    return True

def main():
    """Main build process"""
    print("🚀 PDF Converter App - .exe Builder")
    print("=" * 50)
    
    # Step 1: Install PyInstaller
    if not install_pyinstaller():
        print("❌ Cannot proceed without PyInstaller")
        return False
    
    # Step 2: Build .exe
    if not build_exe():
        print("❌ .exe build failed")
        return False
    
    # Step 3: Create installer package
    if not create_installer():
        print("❌ Installer package creation failed")
        return False
    
    print("\n🎉 BUILD COMPLETED SUCCESSFULLY!")
    print("=" * 50)
    print("📁 Your standalone app is ready in: dist/PDF_Converter_App/")
    print("📱 Users can now:")
    print("   ✅ Download and run without Python")
    print("   ✅ Double-click to launch")
    print("   ✅ Use like any other Windows app")
    print("   ✅ Distribute to others easily")
    
    # Show the output location
    dist_path = Path("dist/PDF_Converter_App").absolute()
    print(f"\n📂 App location: {dist_path}")
    print("🚀 Ready to distribute!")
    
    return True

if __name__ == "__main__":
    main()
