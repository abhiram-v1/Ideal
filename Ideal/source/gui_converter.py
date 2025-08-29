#!/usr/bin/env python3
"""
ideal - Professional PDF Converter App
Modern, sleek interface for converting Jupyter Notebooks to PDFs
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import sys
import subprocess
from pathlib import Path
import threading
import random

class IdealPDFConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("ideal")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Set app icon if available - multiple attempts
        self.setup_icon()
        
        # Configure modern styling
        self.setup_styling()
        
        # File paths
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        
        # Status
        self.is_converting = False
        
        self.setup_ui()
        
    def setup_icon(self):
        """Setup the app icon with multiple fallback methods"""
        print("🔍 Setting up app icon...")
        
        # Try multiple icon sources in order of preference
        icon_sources = [
            ("app_icon.ico", "current directory ICO"),
            ("app_icon.png", "current directory PNG"),
            (Path(__file__).parent.parent / "app_icon.ico", "parent directory ICO"),
            (Path(__file__).parent.parent / "app_icon.png", "parent directory PNG"),
            (Path(__file__).parent / "app_icon.ico", "source directory ICO"),
            (Path(__file__).parent / "app_icon.png", "source directory PNG"),
        ]
        
        for icon_path, description in icon_sources:
            if self.try_load_icon(icon_path, description):
                return
        
        print("❌ Failed to load icon from all sources")
        print("⚠️ App will use default Windows icon")
    
    def try_load_icon(self, icon_path, description):
        """Try to load an icon from a specific path"""
        try:
            print(f"🔍 Trying {description}: {icon_path}")
            
            if not Path(icon_path).exists():
                print(f"   ❌ File does not exist")
                return False
            
            # Try to load the image
            if str(icon_path).endswith('.ico'):
                return self.load_ico_icon(icon_path, description)
            else:
                return self.load_png_icon(icon_path, description)
                
        except Exception as e:
            print(f"   ❌ Error loading {description}: {e}")
            return False
    
    def load_ico_icon(self, icon_path, description):
        """Load ICO icon file"""
        try:
            print(f"   🎯 Loading ICO icon...")
            
            # Method 1: Try iconbitmap first (works better for ICO files)
            self.root.iconbitmap(str(icon_path))
            print(f"   ✓ ICO icon set with iconbitmap")
            
            # Method 2: Also set with iconphoto for consistency
            icon_image = tk.PhotoImage(file=str(icon_path))
            self.root.iconphoto(True, icon_image)
            self.icon_image = icon_image
            print(f"   ✓ ICO icon also set with iconphoto")
            
            # Method 3: Set Windows taskbar ID
            self.set_windows_taskbar_id()
            
            print(f"   ✅ Successfully loaded icon from {description}")
            return True
            
        except Exception as e:
            print(f"   ❌ Failed to load ICO: {e}")
            return False
    
    def load_png_icon(self, icon_path, description):
        """Load PNG icon file"""
        try:
            print(f"   🎯 Loading PNG icon...")
            
            # Method 1: Set with iconphoto
            icon_image = tk.PhotoImage(file=str(icon_path))
            self.root.iconphoto(True, icon_image)
            self.icon_image = icon_image
            print(f"   ✓ PNG icon set with iconphoto")
            
            # Method 2: Try to convert PNG to ICO and set with iconbitmap
            try:
                from PIL import Image
                temp_ico = Path("temp_icon.ico")
                img = Image.open(icon_path)
                img.save(temp_ico, format='ICO')
                self.root.iconbitmap(str(temp_ico))
                print(f"   ✓ PNG converted to ICO and set with iconbitmap")
                
                # Clean up temp file
                if temp_ico.exists():
                    temp_ico.unlink()
                    
            except Exception as e:
                print(f"   ⚠️ Could not convert PNG to ICO: {e}")
            
            # Method 3: Set Windows taskbar ID
            self.set_windows_taskbar_id()
            
            print(f"   ✅ Successfully loaded icon from {description}")
            return True
            
        except Exception as e:
            print(f"   ❌ Failed to load PNG: {e}")
            return False
    
    def set_windows_taskbar_id(self):
        """Set Windows taskbar application ID"""
        try:
            import ctypes
            myappid = 'ideal.pdfconverter.1.0'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
            print(f"   ✓ Windows taskbar ID set: {myappid}")
        except Exception as e:
            print(f"   ⚠️ Could not set Windows taskbar ID: {e}")
    
    def setup_styling(self):
        """Setup modern, professional styling"""
        style = ttk.Style()
        
        # Modern color scheme
        self.colors = {
            'primary': '#2563eb',      # Modern blue
            'secondary': '#64748b',    # Slate gray
            'success': '#059669',      # Green
            'warning': '#d97706',      # Orange
            'error': '#dc2626',        # Red
            'background': '#f8fafc',   # Light gray
            'surface': '#ffffff',      # White
            'text': '#1e293b',        # Dark text
            'text_secondary': '#64748b' # Secondary text
        }
        
        # Configure styles
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 24, 'bold'), 
                       foreground=self.colors['primary'])
        
        style.configure('Heading.TLabel', 
                       font=('Segoe UI', 12, 'bold'), 
                       foreground=self.colors['text'])
        
        style.configure('Body.TLabel', 
                       font=('Segoe UI', 10), 
                       foreground=self.colors['text_secondary'])
        
        style.configure('Primary.TButton', 
                       font=('Segoe UI', 11, 'bold'),
                       background=self.colors['primary'])
        
        style.configure('Secondary.TButton', 
                       font=('Segoe UI', 10),
                       background=self.colors['secondary'])
        
        # Configure root background
        self.root.configure(bg=self.colors['background'])
        
    def get_random_greeting(self):
        """Get a random greeting message"""
        greetings = [
            "Welcome to ideal! ✨",
            "Ready to convert your notebooks! 🚀",
            "Let's make your work beautiful! 💫",
            "Time to transform ideas into PDFs! 🌟",
            "Your notebooks, our expertise! 🎯",
            "Making conversion simple and elegant! ✨",
            "Welcome back to ideal! 🎉",
            "Ready to work some magic? ✨",
            "Let's create something amazing! 🚀",
            "Your creative journey starts here! 💫"
        ]
        return random.choice(greetings)
        
    def setup_ui(self):
        """Setup the professional user interface"""
        # Main container with padding
        main_container = tk.Frame(self.root, bg=self.colors['background'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        # Header section
        self.setup_header(main_container)
        
        # Main content area
        content_frame = tk.Frame(main_container, bg=self.colors['background'])
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(30, 0))
        
        # File selection section
        self.setup_file_selection(content_frame)
        
        # Conversion section
        self.setup_conversion_section(content_frame)
        
        # Progress and status section
        self.setup_progress_section(content_frame)
        
        # Log section
        self.setup_log_section(content_frame)
        
        # Set default output path
        self.set_default_output()
        
    def setup_header(self, parent):
        """Setup the app header"""
        header_frame = tk.Frame(parent, bg=self.colors['background'])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # App title
        title_label = tk.Label(header_frame, 
                              text="ideal", 
                              font=('Segoe UI', 32, 'bold'),
                              fg=self.colors['primary'],
                              bg=self.colors['background'])
        title_label.pack()
        
        # Random greeting subtitle
        greeting_label = tk.Label(header_frame,
                                 text=self.get_random_greeting(),
                                 font=('Segoe UI', 14),
                                 fg=self.colors['text_secondary'],
                                 bg=self.colors['background'])
        greeting_label.pack(pady=(5, 0))
        
        # Store reference to update greeting later
        self.greeting_label = greeting_label
        
    def setup_file_selection(self, parent):
        """Setup file selection interface"""
        # Input file selection
        input_frame = tk.Frame(parent, bg=self.colors['background'])
        input_frame.pack(fill=tk.X, pady=(0, 25))
        
        # Input label
        input_label = tk.Label(input_frame, 
                              text="Input Notebook", 
                              font=('Segoe UI', 12, 'bold'),
                              fg=self.colors['text'],
                              bg=self.colors['background'])
        input_label.pack(anchor=tk.W, pady=(0, 8))
        
        # Input selection row
        input_row = tk.Frame(input_frame, bg=self.colors['background'])
        input_row.pack(fill=tk.X)
        
        # Input entry with modern styling
        input_entry = tk.Entry(input_row, 
                              textvariable=self.input_file,
                              font=('Segoe UI', 10),
                              bg=self.colors['surface'],
                              fg=self.colors['text'],
                              relief=tk.FLAT,
                              bd=0,
                              highlightthickness=1,
                              highlightcolor=self.colors['primary'],
                              highlightbackground='#e2e8f0')
        input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 15))
        
        # Browse button
        browse_btn = tk.Button(input_row,
                              text="Browse",
                              font=('Segoe UI', 10, 'bold'),
                              bg=self.colors['primary'],
                              fg='white',
                              relief=tk.FLAT,
                              bd=0,
                              padx=20,
                              pady=8,
                              cursor='hand2',
                              command=self.browse_input_file)
        browse_btn.pack(side=tk.RIGHT)
        
        # Output file selection
        output_frame = tk.Frame(parent, bg=self.colors['background'])
        output_frame.pack(fill=tk.X, pady=(0, 25))
        
        # Output label
        output_label = tk.Label(output_frame, 
                               text="Output Location", 
                               font=('Segoe UI', 12, 'bold'),
                               fg=self.colors['text'],
                               bg=self.colors['background'])
        output_label.pack(anchor=tk.W, pady=(0, 8))
        
        # Output selection row
        output_row = tk.Frame(output_frame, bg=self.colors['background'])
        output_row.pack(fill=tk.X)
        
        # Output entry
        output_entry = tk.Entry(output_row, 
                               textvariable=self.output_file,
                               font=('Segoe UI', 10),
                               bg=self.colors['surface'],
                               fg=self.colors['text'],
                               relief=tk.FLAT,
                               bd=0,
                               highlightthickness=1,
                               highlightcolor=self.colors['primary'],
                               highlightbackground='#e2e8f0')
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 15))
        
        # Quick save buttons frame
        quick_buttons_frame = tk.Frame(output_row, bg=self.colors['background'])
        quick_buttons_frame.pack(side=tk.RIGHT)
        
        # Desktop button
        desktop_btn = tk.Button(quick_buttons_frame,
                               text="Desktop",
                               font=('Segoe UI', 9, 'bold'),
                               bg=self.colors['secondary'],
                               fg='white',
                               relief=tk.FLAT,
                               bd=0,
                               padx=15,
                               pady=6,
                               cursor='hand2',
                               command=self.quick_desktop_save)
        desktop_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        # Current folder button
        current_btn = tk.Button(quick_buttons_frame,
                               text="Current",
                               font=('Segoe UI', 9, 'bold'),
                               bg=self.colors['secondary'],
                               fg='white',
                               relief=tk.FLAT,
                               bd=0,
                               padx=15,
                               pady=6,
                               cursor='hand2',
                               command=self.current_folder_save)
        current_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        # Browse output button
        browse_output_btn = tk.Button(quick_buttons_frame,
                                     text="Browse",
                                     font=('Segoe UI', 9, 'bold'),
                                     bg=self.colors['primary'],
                                     fg='white',
                                     relief=tk.FLAT,
                                     bd=0,
                                     padx=15,
                                     pady=6,
                                     cursor='hand2',
                                     command=self.browse_output_file)
        browse_output_btn.pack(side=tk.LEFT)
        
    def setup_conversion_section(self, parent):
        """Setup the conversion button section"""
        conversion_frame = tk.Frame(parent, bg=self.colors['background'])
        conversion_frame.pack(fill=tk.X, pady=(0, 25))
        
        # Convert button - large and prominent
        self.convert_button = tk.Button(conversion_frame,
                                       text="Convert to PDF",
                                       font=('Segoe UI', 14, 'bold'),
                                       bg=self.colors['primary'],
                                       fg='white',
                                       relief=tk.FLAT,
                                       bd=0,
                                       padx=40,
                                       pady=15,
                                       cursor='hand2',
                                       command=self.start_conversion)
        self.convert_button.pack()
        
    def setup_progress_section(self, parent):
        """Setup progress and status section"""
        progress_frame = tk.Frame(parent, bg=self.colors['background'])
        progress_frame.pack(fill=tk.X, pady=(0, 25))
        
        # Progress bar with modern styling
        self.progress = ttk.Progressbar(progress_frame, 
                                       mode='indeterminate',
                                       length=400)
        self.progress.pack(pady=(0, 15))
        
        # Status label
        self.status_label = tk.Label(progress_frame,
                                    text="Ready to convert",
                                    font=('Segoe UI', 11),
                                    fg=self.colors['success'],
                                    bg=self.colors['background'])
        self.status_label.pack()
        
    def setup_log_section(self, parent):
        """Setup the log section"""
        log_frame = tk.Frame(parent, bg=self.colors['background'])
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        # Log header
        log_header = tk.Frame(log_frame, bg=self.colors['background'])
        log_header.pack(fill=tk.X, pady=(0, 10))
        
        log_title = tk.Label(log_header,
                             text="Conversion Log",
                             font=('Segoe UI', 12, 'bold'),
                             fg=self.colors['text'],
                             bg=self.colors['background'])
        log_title.pack(side=tk.LEFT)
        
        clear_btn = tk.Button(log_header,
                              text="Clear Log",
                              font=('Segoe UI', 9),
                              bg=self.colors['secondary'],
                              fg='white',
                              relief=tk.FLAT,
                              bd=0,
                              padx=12,
                              pady=4,
                              cursor='hand2',
                              command=self.clear_log)
        clear_btn.pack(side=tk.RIGHT)
        
        # Log text area with modern styling
        log_container = tk.Frame(log_frame, bg=self.colors['surface'], relief=tk.FLAT, bd=1)
        log_container.pack(fill=tk.BOTH, expand=True)
        
        # Log text widget
        self.log_text = tk.Text(log_container,
                                height=8,
                                font=('Consolas', 9),
                                bg=self.colors['surface'],
                                fg=self.colors['text'],
                                relief=tk.FLAT,
                                bd=0,
                                padx=15,
                                pady=15,
                                wrap=tk.WORD)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(log_container, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        # Pack log elements
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def browse_input_file(self):
        """Browse for input notebook file"""
        filename = filedialog.askopenfilename(
            title="Select Jupyter Notebook",
            filetypes=[("Jupyter Notebooks", "*.ipynb"), ("All Files", "*.*")]
        )
        if filename:
            self.input_file.set(filename)
            self.set_default_output()
            self.log_message(f"📁 Selected input: {os.path.basename(filename)}")
    
    def quick_desktop_save(self):
        """Quick save to Desktop with auto-generated filename"""
        try:
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            if not os.path.exists(desktop):
                desktop = os.path.join(os.path.expanduser("~"), "Documents")
            
            if self.input_file.get():
                input_path = Path(self.input_file.get())
                filename = input_path.stem + '.pdf'
            else:
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"converted_notebook_{timestamp}.pdf"
            
            output_path = os.path.join(desktop, filename)
            self.output_file.set(output_path)
            self.log_message(f"📁 Quick save to Desktop: {filename}")
            
        except Exception as e:
            self.log_message(f"Error setting desktop path: {e}")
    
    def current_folder_save(self):
        """Quick save to current app folder with auto-generated filename"""
        try:
            current_folder = os.getcwd()
            
            if self.input_file.get():
                input_path = Path(self.input_file.get())
                filename = input_path.stem + '.pdf'
            else:
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"converted_notebook_{timestamp}.pdf"
            
            output_path = os.path.join(current_folder, filename)
            self.output_file.set(output_path)
            self.log_message(f"📂 Quick save to current folder: {filename}")
            
        except Exception as e:
            self.log_message(f"Error setting current folder path: {e}")
    
    def browse_output_file(self):
        """Browse for output folder and filename"""
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            filename = filedialog.askstring(
                "Enter PDF Filename",
                "Enter the name for your PDF file (without .pdf extension):",
                initialvalue="converted_file"
            )
            if filename:
                if not filename.endswith('.pdf'):
                    filename += '.pdf'
                
                full_path = os.path.join(folder, filename)
                self.output_file.set(full_path)
                self.log_message(f"📂 Selected output: {folder}")
                self.log_message(f"📄 Filename: {filename}")
            else:
                self.log_message("No filename entered")
        else:
            self.log_message("No output folder selected")
    
    def set_default_output(self):
        """Set default output path based on input file"""
        input_path = self.input_file.get()
        if input_path and os.path.exists(input_path):
            input_path = Path(input_path)
            filename = input_path.stem + '.pdf'
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            output_path = os.path.join(desktop, filename)
            self.output_file.set(output_path)
    
    def start_conversion(self):
        """Start the conversion process in a separate thread"""
        if self.is_converting:
            return
            
        # Validate inputs
        if not self.input_file.get():
            messagebox.showerror("Error", "Please select an input notebook file!")
            return
            
        if not self.output_file.get():
            messagebox.showerror("Error", "Please select an output PDF location!")
            return
            
        if not os.path.exists(self.input_file.get()):
            messagebox.showerror("Error", "Input file does not exist!")
            return
        
        # Start conversion in separate thread
        self.is_converting = True
        self.convert_button.config(state="disabled", text="Converting...")
        self.progress.start()
        self.status_label.config(text="Converting...", fg=self.colors['warning'])
        
        # Clear log
        self.clear_log()
        self.log_message("🚀 Starting conversion...")
        
        # Start conversion thread
        thread = threading.Thread(target=self.convert_notebook)
        thread.daemon = True
        thread.start()
    
    def convert_notebook(self):
        """Convert the notebook to PDF"""
        try:
            input_path = self.input_file.get()
            output_path = self.output_file.get()
            
            self.log_message(f"📁 Input: {os.path.basename(input_path)}")
            self.log_message(f"📄 Output: {os.path.basename(output_path)}")
            self.log_message("")
            
            # Step 1: Convert to HTML
            self.log_message("🔄 Step 1: Converting notebook to HTML...")
            html_file = self.convert_to_html(input_path)
            
            if not html_file:
                self.log_message("❌ HTML conversion failed!")
                self.conversion_finished(False)
                return
            
            self.log_message("✓ HTML conversion successful!")
            
            # Step 2: Apply styling
            self.log_message("🔄 Step 2: Applying aesthetic styling...")
            self.apply_styling(html_file)
            self.log_message("✓ Styling applied!")
            
            # Step 3: Convert to PDF
            self.log_message("🔄 Step 3: Converting HTML to PDF...")
            success = self.convert_html_to_pdf(html_file, output_path)
            
            if success:
                self.log_message("✓ PDF conversion successful!")
                self.log_message(f"🎉 Your PDF is ready: {os.path.basename(output_path)}")
                
                # Clean up HTML file
                try:
                    os.remove(html_file)
                    self.log_message("✓ Cleaned up temporary files")
                except:
                    pass
                
                self.conversion_finished(True)
            else:
                self.log_message("❌ PDF conversion failed!")
                self.log_message("💡 Try the manual conversion option")
                self.conversion_finished(False)
                
        except Exception as e:
            self.log_message(f"❌ Error during conversion: {e}")
            self.conversion_finished(False)
    
    def convert_to_html(self, notebook_path):
        """Convert notebook to HTML using nbconvert"""
        try:
            # Check if nbconvert is available
            try:
                import nbconvert
            except ImportError:
                self.log_message("📦 Installing nbconvert...")
                subprocess.run([sys.executable, "-m", "pip", "install", "nbconvert"], 
                             capture_output=True, check=True)
                self.log_message("✓ nbconvert installed")
            
            # Convert to HTML
            html_path = Path(notebook_path).with_suffix('.html')
            cmd = [sys.executable, "-m", "nbconvert", "--to", "html", notebook_path]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0 and html_path.exists():
                return str(html_path)
            else:
                self.log_message(f"Error: {result.stderr}")
                return None
                
        except Exception as e:
            self.log_message(f"Error: {e}")
            return None
    
    def apply_styling(self, html_file):
        """Apply aesthetic styling to HTML file"""
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Light aesthetic CSS
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
            
            # Insert CSS after opening <head> tag
            if '<head>' in html_content:
                html_content = html_content.replace('<head>', '<head>' + aesthetic_css)
            else:
                html_content = aesthetic_css + html_content
            
            # Write back to file
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
                
        except Exception as e:
            self.log_message(f"Warning: Could not apply styling: {e}")
    
    def convert_html_to_pdf(self, html_file, output_path):
        """Convert HTML to PDF using Chrome"""
        try:
            # Check if Chrome is available
            chrome_path = self.find_chrome()
            if not chrome_path:
                self.log_message("❌ Chrome not found - manual conversion required")
                return False
            
            # Create output directory if needed
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Chrome command for PDF generation
            cmd = [
                chrome_path,
                "--headless",
                "--disable-gpu",
                "--print-to-pdf=" + output_path,
                "--print-to-pdf-no-header",
                "--no-margins",
                "--disable-extensions",
                "--disable-plugins",
                "file://" + str(Path(html_file).absolute())
            ]
            
            self.log_message("Converting with Chrome...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and Path(output_path).exists():
                return True
            else:
                self.log_message(f"Chrome error: {result.stderr}")
                return False
                
        except Exception as e:
            self.log_message(f"Chrome conversion error: {e}")
            return False
    
    def find_chrome(self):
        """Find Chrome/Chromium executable"""
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
    
    def conversion_finished(self, success):
        """Handle conversion completion"""
        self.is_converting = False
        self.convert_button.config(state="normal", text="Convert to PDF")
        self.progress.stop()
        
        if success:
            self.status_label.config(text="Conversion completed successfully!", fg=self.colors['success'])
            messagebox.showinfo("Success", "Your notebook has been converted to PDF successfully!")
        else:
            self.status_label.config(text="Conversion failed", fg=self.colors['error'])
            messagebox.showerror("Error", "Conversion failed. Check the log for details.")
    
    def log_message(self, message):
        """Add message to log"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_log(self):
        """Clear the log text area"""
        self.log_text.delete(1.0, tk.END)

def main():
    """Main function"""
    root = tk.Tk()
    
    # Center window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (400)
    y = (root.winfo_screenheight() // 2) - (350)
    root.geometry(f"+{x}+{y}")
    
    app = IdealPDFConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
