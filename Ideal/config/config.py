#!/usr/bin/env python3
"""
Configuration file for PDF Converter App
Customize settings without modifying the main code
"""

# =============================================================================
# CONVERSION SETTINGS
# =============================================================================

# Default notebook name to look for
DEFAULT_NOTEBOOK = "Lab_2.ipynb"

# Output directory for generated PDFs
OUTPUT_DIR = "output"

# Temporary files directory
TEMP_DIR = "temp"

# =============================================================================
# STYLING SETTINGS
# =============================================================================

# Background gradient colors (RGB values)
BACKGROUND_COLORS = {
    "light": {
        "start": "#f5f5f5",    # Light gray
        "middle": "#e8e8e8",   # Medium gray
        "end": "#f0f0f0"      # Light gray
    },
    "dark": {
        "start": "#1a1a1a",    # Dark gray
        "middle": "#2d2d2d",   # Medium dark gray
        "end": "#1a1a1a"      # Dark gray
    },
    "blue": {
        "start": "#f0f8ff",    # Alice blue
        "middle": "#e6f3ff",   # Light blue
        "end": "#f0f8ff"      # Alice blue
    },
    "green": {
        "start": "#f0fff0",    # Honeydew
        "middle": "#e6ffe6",   # Light green
        "end": "#f0fff0"      # Honeydew
    }
}

# Current theme to use
CURRENT_THEME = "light"

# =============================================================================
# CHROME SETTINGS
# =============================================================================

# Chrome command line arguments for PDF generation
CHROME_ARGS = [
    "--headless",
    "--disable-gpu",
    "--print-to-pdf-no-header",
    "--no-margins",
    "--disable-extensions",
    "--disable-plugins",
    "--disable-background-timer-throttling",
    "--disable-backgrounding-occluded-windows",
    "--disable-renderer-backgrounding"
]

# Chrome timeout in seconds
CHROME_TIMEOUT = 30

# =============================================================================
# WKHTMLTOPDF SETTINGS
# =============================================================================

# wkhtmltopdf page settings
WKHTMLTOPDF_SETTINGS = {
    "page_size": "A4",
    "margin_top": "0.75in",
    "margin_right": "0.75in",
    "margin_bottom": "0.75in",
    "margin_left": "0.75in",
    "encoding": "UTF-8"
}

# wkhtmltopdf timeout in seconds
WKHTMLTOPDF_TIMEOUT = 60

# =============================================================================
# NBCOVERT SETTINGS
# =============================================================================

# nbconvert timeout in seconds
NBCONVERT_TIMEOUT = 60

# HTML export options
HTML_EXPORT_OPTIONS = {
    "template": "classic",  # or "lab" for JupyterLab style
    "embed_images": True,
    "embed_widgets": True
}

# =============================================================================
# LOGGING SETTINGS
# =============================================================================

# Enable verbose logging
VERBOSE_LOGGING = True

# Log file path
LOG_FILE = "converter.log"

# =============================================================================
# ADVANCED SETTINGS
# =============================================================================

# Maximum file size for conversion (in MB)
MAX_FILE_SIZE_MB = 100

# Enable automatic dependency installation
AUTO_INSTALL_DEPS = True

# Enable automatic cleanup of temporary files
AUTO_CLEANUP = True

# Retry attempts for failed conversions
MAX_RETRY_ATTEMPTS = 3

# =============================================================================
# THEME FUNCTIONS
# =============================================================================

def get_background_css(theme_name=None):
    """Get CSS for the specified theme"""
    if theme_name is None:
        theme_name = CURRENT_THEME
    
    if theme_name not in BACKGROUND_COLORS:
        theme_name = "light"  # fallback to light theme
    
    colors = BACKGROUND_COLORS[theme_name]
    
    return f"""
    <style>
        /* {theme_name.title()} aesthetic - ONLY background changes for better visibility */
        body {{
            background: linear-gradient(135deg, {colors['start']} 0%, {colors['middle']} 50%, {colors['end']} 100%) !important;
        }}
        
        /* Ensure all content remains exactly as nbconvert generated it */
        /* No margin, padding, or positioning changes */
        /* No font changes */
        /* No border changes */
        /* No layout modifications */
        /* No color changes - everything stays as nbconvert intended */
    </style>
    """

def list_available_themes():
    """List all available themes"""
    return list(BACKGROUND_COLORS.keys())

def add_custom_theme(name, start_color, middle_color, end_color):
    """Add a custom theme"""
    BACKGROUND_COLORS[name] = {
        "start": start_color,
        "middle": middle_color,
        "end": end_color
    }
    return f"Custom theme '{name}' added successfully!"
