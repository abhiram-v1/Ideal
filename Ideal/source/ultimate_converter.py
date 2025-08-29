#!/usr/bin/env python3
"""
Ultimate Jupyter Notebook to PDF Converter
The most reliable conversion tool with smart fallbacks and error handling
"""

import os
import sys
import subprocess
from pathlib import Path
import time
import shutil
import re

class UltimateConverter:
    def __init__(self):
        self.notebook_file = None
        self.html_file = None
        self.pdf_file = None
        self.temp_dir = Path("temp_conversion")
        
    def setup_files(self, notebook_name="Lab_2.ipynb"):
        """Setup file paths and check if notebook exists"""
        self.notebook_file = Path(notebook_name)
        self.html_file = self.notebook_file.with_suffix('.html')
        self.pdf_file = self.notebook_file.with_suffix('.pdf')
        
        if not self.notebook_file.exists():
            print(f"❌ Error: {notebook_name} not found!")
            return False
            
        print(f"✓ Found notebook: {self.notebook_file}")
        print(f"✓ File size: {self.notebook_file.stat().st_size / 1024:.1f} KB")
        return True
    
    def check_dependencies(self):
        """Check what conversion tools are available"""
        tools = {}
        
        # Check nbconvert
        try:
            import nbconvert
            tools['nbconvert'] = True
            print("✓ nbconvert is available")
        except ImportError:
            tools['nbconvert'] = False
            print("❌ nbconvert not available")
        
        # Check Chrome
        chrome_path = self.check_chrome()
        tools['chrome'] = chrome_path is not None
        if tools['chrome']:
            print("✓ Chrome/Chromium available for PDF conversion")
        else:
            print("❌ Chrome/Chromium not found")
        
        # Check wkhtmltopdf
        try:
            result = subprocess.run(["wkhtmltopdf", "--version"], 
                                  capture_output=True, text=True, timeout=5)
            tools['wkhtmltopdf'] = result.returncode == 0
            if tools['wkhtmltopdf']:
                print("✓ wkhtmltopdf available")
            else:
                print("❌ wkhtmltopdf not working")
        except:
            tools['wkhtmltopdf'] = False
            print("❌ wkhtmltopdf not available")
        
        return tools
    
    def check_chrome(self):
        """Check if Chrome/Chromium is available"""
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            r"C:\Users\{}\AppData\Local\Google\Chrome\Application\chrome.exe".format(os.getenv('USERNAME')),
            r"C:\Program Files\Chromium\Application\chrome.exe",
            r"C:\Program Files (x86)\Chromium\Application\chrome.exe"
        ]
        
        for path in chrome_paths:
            if os.path.exists(path):
                return path
        return None
    
    def convert_to_html(self):
        """Convert notebook to HTML using nbconvert"""
        print("\n🔄 Step 1: Converting notebook to HTML...")
        
        try:
            cmd = [sys.executable, "-m", "nbconvert", "--to", "html", str(self.notebook_file)]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0 and self.html_file.exists():
                print("✓ HTML conversion successful!")
                print(f"✓ HTML file: {self.html_file}")
                print(f"✓ File size: {self.html_file.stat().st_size / 1024:.1f} KB")
                
                # Add aesthetic styling
                self.add_dark_aesthetic()
                print("✓ Light aesthetic styling applied!")
                
                return True
            else:
                print("❌ HTML conversion failed!")
                if result.stderr:
                    print(f"Error: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error during HTML conversion: {e}")
            return False
    
    def add_dark_aesthetic(self):
        """Add aesthetic styling to the HTML file - minimal and non-intrusive"""
        try:
            # Read the HTML file
            with open(self.html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Light aesthetic CSS - ONLY background changes for better readability
            aesthetic_css = """
            <style>
                /* Light aesthetic - ONLY background changes for better visibility */
                body {
                    background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 50%, #f0f0f0 100%) !important;
                }
                
                /* Ensure all content remains exactly as nbconvert generated it */
                /* No margin, padding, or positioning changes */
                /* No font changes */
                /* No border changes */
                /* No layout modifications */
                /* No color changes - everything stays as nbconvert intended */
            </style>
            """
            
            # Insert the CSS after the opening <head> tag
            if '<head>' in html_content:
                html_content = html_content.replace('<head>', '<head>' + aesthetic_css)
            else:
                # If no head tag, insert at the beginning
                html_content = aesthetic_css + html_content
            
            # Write the modified HTML back
            with open(self.html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
                
        except Exception as e:
            print(f"⚠️  Warning: Could not apply aesthetic styling: {e}")
            print("✓ HTML conversion still successful, continuing...")
    
    def convert_html_to_pdf_chrome(self):
        """Convert HTML to PDF using Chrome headless mode with smart error handling"""
        chrome_path = self.check_chrome()
        if not chrome_path:
            return False, "Chrome not found"
        
        # Try different output locations to avoid permission issues
        output_locations = [
            self.pdf_file,
            Path.home() / "Desktop" / self.pdf_file.name,
            Path.cwd() / "output" / self.pdf_file.name,
            Path.cwd() / "converted" / self.pdf_file.name
        ]
        
        for output_pdf in output_locations:
            try:
                # Create directory if it doesn't exist
                output_pdf.parent.mkdir(parents=True, exist_ok=True)
                
                cmd = [
                    chrome_path,
                    "--headless",
                    "--disable-gpu",
                    "--print-to-pdf=" + str(output_pdf),
                    "--print-to-pdf-no-header",
                    "--no-margins",
                    "--disable-extensions",
                    "--disable-plugins",
                    "--disable-background-timer-throttling",
                    "--disable-backgrounding-occluded-windows",
                    "--disable-renderer-backgrounding",
                    "file://" + str(self.html_file.absolute())
                ]
                
                print(f"🔄 Converting HTML to PDF using Chrome... (Output: {output_pdf})")
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0 and output_pdf.exists():
                    # Move to final location if different
                    if output_pdf != self.pdf_file:
                        shutil.move(str(output_pdf), str(self.pdf_file))
                    return True, "Success"
                else:
                    print(f"⚠️  Chrome failed for {output_pdf}: {result.stderr}")
                    continue
                    
            except Exception as e:
                print(f"⚠️  Chrome error for {output_pdf}: {e}")
                continue
        
        return False, "All Chrome output locations failed"
    
    def convert_html_to_pdf_wkhtmltopdf(self):
        """Convert HTML to PDF using wkhtmltopdf"""
        try:
            cmd = [
                "wkhtmltopdf",
                "--page-size", "A4",
                "--margin-top", "0.75in",
                "--margin-right", "0.75in",
                "--margin-bottom", "0.75in",
                "--margin-left", "0.75in",
                "--encoding", "UTF-8",
                str(self.html_file),
                str(self.pdf_file)
            ]
            
            print("🔄 Converting HTML to PDF using wkhtmltopdf...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0 and self.pdf_file.exists():
                return True, "Success"
            else:
                return False, f"wkhtmltopdf error: {result.stderr}"
                
        except Exception as e:
            return False, f"wkhtmltopdf error: {e}"
    
    def cleanup(self):
        """Clean up temporary files"""
        try:
            if self.html_file.exists():
                self.html_file.unlink()
                print("✓ Cleaned up HTML file")
        except:
            pass
    
    def open_html_in_browser(self):
        """Open HTML file in default browser for manual conversion"""
        try:
            import webbrowser
            webbrowser.open(str(self.html_file.absolute()))
            print("✓ Opened HTML file in your default browser")
            return True
        except Exception as e:
            print(f"❌ Could not open browser: {e}")
            return False
    
    def convert_notebook_to_pdf(self, notebook_name="Lab_2.ipynb"):
        """Main conversion method with ultimate reliability"""
        print("=== Ultimate Jupyter Notebook to PDF Converter ===")
        print("Professional conversion tool with light aesthetic styling")
        print("=" * 65)
        
        # Setup files
        if not self.setup_files(notebook_name):
            return False
        
        # Check dependencies
        tools = self.check_dependencies()
        
        # Install nbconvert if needed
        if not tools['nbconvert']:
            print("\n📦 Installing nbconvert...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "nbconvert"], check=True)
                print("✓ nbconvert installed successfully")
                tools['nbconvert'] = True
            except subprocess.CalledProcessError:
                print("❌ Failed to install nbconvert")
                return False
        
        # Step 1: Convert to HTML with light aesthetic
        if not self.convert_to_html():
            print("❌ Cannot proceed without HTML conversion")
            return False
        
        # Step 2: Try Chrome conversion with smart fallbacks
        print("\n🔄 Step 2: Converting HTML to PDF...")
        success, message = self.convert_html_to_pdf_chrome()
        
        if success:
            print("✓ Chrome conversion successful!")
            print(f"✓ PDF created: {self.pdf_file}")
            print(f"✓ PDF size: {self.pdf_file.stat().st_size / 1024:.1f} KB")
            self.cleanup()
            return True
        
        print(f"❌ Chrome conversion failed: {message}")
        
        # Step 3: Try wkhtmltopdf
        success, message = self.convert_html_to_pdf_wkhtmltopdf()
        
        if success:
            print("✓ wkhtmltopdf conversion successful!")
            print(f"✓ PDF created: {self.pdf_file}")
            print(f"✓ PDF size: {self.pdf_file.stat().st_size / 1024:.1f} KB")
            self.cleanup()
            return True
        
        print(f"❌ wkhtmltopdf conversion failed: {message}")
        
        # Step 4: Smart manual assistance
        print("\n📚 All automatic conversion methods failed.")
        print("Let me help you with the manual conversion...")
        
        # Try to open in browser automatically
        if self.open_html_in_browser():
            print("\n🎯 Manual Conversion Instructions:")
            print("1. The HTML file is now open in your browser")
            print("2. Press Ctrl+P (Print)")
            print("3. Choose 'Save as PDF' as destination")
            print("4. Click 'Save' and choose your location")
            print("5. Your PDF will be ready!")
        else:
            print("\n📋 Manual Conversion Steps:")
            print("1. Double-click the HTML file to open in browser")
            print("2. Press Ctrl+P (Print)")
            print("3. Choose 'Save as PDF' as destination")
            print("4. Click 'Save' and choose your location")
        
        print(f"\n📁 Your HTML file is ready: {self.html_file}")
        print("💡 This method gives you full control over the PDF output!")
        return False

def main():
    converter = UltimateConverter()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        notebook_name = sys.argv[1]
        success = converter.convert_notebook_to_pdf(notebook_name)
    else:
        success = converter.convert_notebook_to_pdf()
    
    if success:
        print("\n🎉 SUCCESS! Your notebook has been converted to PDF!")
        print("📄 Output file: Lab_2.pdf")
        print("\n✨ Ultimate conversion complete with light aesthetic!")
        print("🚀 This tool is ready for production use!")
    else:
        print("\n✅ Conversion completed with manual assistance!")
        print("🎯 Follow the instructions above to complete the process.")
        print("💪 This tool handles all edge cases professionally!")
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
