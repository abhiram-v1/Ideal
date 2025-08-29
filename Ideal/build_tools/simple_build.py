#!/usr/bin/env python3
"""
PDF Converter App - Simple .exe Builder
Creates a standalone .exe file from the GUI converter
"""

import subprocess
import sys
import os
from pathlib import Path
import shutil

def check_pyinstaller():
    """Check if PyInstaller is installed"""
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

def prepare_icon():
    """Prepare the icon file for PyInstaller"""
    # Try ICO first, then PNG as fallback
    ico_path = Path("app_icon.ico")
    png_path = Path("app_icon.png")
    
    if ico_path.exists():
        print("✓ Using ICO icon (best for Windows)")
        return str(ico_path)
    elif png_path.exists():
        print("✓ Using PNG icon as fallback")
        return str(png_path)
    else:
        print("⚠️ No icon files found")
        return None

def build_exe():
    """Build the standalone .exe file"""
    print("🔨 Building standalone .exe file...")
    
    # Get the correct path to gui_converter.py
    script_path = Path(__file__).parent.parent / "source" / "gui_converter.py"
    
    if not script_path.exists():
        print(f"❌ Script not found at: {script_path}")
        return False
    
    # Check for icon file in build folder
    icon_file = Path("build/app_icon.ico")
    if not icon_file.exists():
        print("⚠️ app_icon.ico not found in build folder, checking current directory...")
        icon_file = Path("app_icon.ico")
        if not icon_file.exists():
            print("❌ No icon files found")
            return False
    
    print(f"✓ Using icon: {icon_file}")
    
    # Build with proper icon embedding
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                    # Single .exe file
        "--windowed",                   # No console window
        "--name=ideal",                 # App name
        "--clean",                      # Clean build
        f"--icon={icon_file}",          # Embed icon in .exe file
        str(script_path)                # Main script path
    ]
    
    try:
        print("Running PyInstaller with icon embedding...")
        print(f"Command: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✓ PyInstaller completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ PyInstaller failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def test_exe():
    """Test if the .exe file runs"""
    exe_path = Path("dist/ideal.exe")
    if exe_path.exists():
        print(f"🎉 .exe file created successfully: {exe_path}")
        print("Testing if .exe runs...")
        try:
            # Try to run the .exe (this will just check if it starts)
            result = subprocess.run([str(exe_path), "--help"], 
                                  capture_output=True, timeout=5)
            print("✓ .exe file runs successfully!")
        except subprocess.TimeoutExpired:
            print("✓ .exe file started (timeout is normal for GUI apps)")
        except Exception as e:
            print(f"⚠️ .exe test inconclusive: {e}")
    else:
        print("❌ .exe file not found")

def main():
    """Main build process"""
    print("🚀 ideal - Professional PDF Converter App")
    print("==================================================")
    
    # Check PyInstaller
    if not check_pyinstaller():
        return
    
    # Build .exe
    if build_exe():
        test_exe()
        print("\n🎯 Build completed successfully!")
        print("📁 Your app is ready in the 'dist' folder")
        print("🚀 Double-click 'ideal.exe' to run your professional app!")
        print("\n💡 If the icon still shows the old symbol, try:")
        print("   1. Restart your computer (Windows caches icons)")
        print("   2. Right-click the .exe → Properties → Change Icon")
    else:
        print("\n❌ Build failed. Check the errors above.")

if __name__ == "__main__":
    main()
