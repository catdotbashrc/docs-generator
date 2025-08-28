# Configuration file for the Sphinx documentation builder.
# Infrastructure Documentation Standards

import os
import sys
from datetime import datetime

# Add extensions path
sys.path.insert(0, os.path.abspath('_extensions'))

# Project information
project = 'Infrastructure Documentation Standards'
copyright = f'{datetime.now().year}, Infrastructure Team'
author = 'Infrastructure Team'
release = '0.1.0'

# Extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode', 
    'sphinx.ext.napoleon',
    'sphinx.ext.graphviz',
    'sphinx_tabs.tabs',
]

# Templates path
templates_path = ['_templates']

# Source file extensions
source_suffix = '.rst'

# Master document
master_doc = 'index'

# Language
language = 'en'

# Files to exclude
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# HTML theme
html_theme = 'furo'
html_static_path = ['_static']
html_title = f'{project} Documentation'

# HTML theme options
html_theme_options = {
    "sidebar_hide_name": True,
    "light_css_variables": {
        "color-brand-primary": "#2563eb",  # Blue
        "color-brand-content": "#1e40af",
    },
    "dark_css_variables": {
        "color-brand-primary": "#3b82f6",
        "color-brand-content": "#60a5fa", 
    },
}

# PDF output configuration
latex_elements = {
    'papersize': 'letterpaper',
    'pointsize': '10pt',
    'preamble': r'''
\usepackage{charter}
\usepackage[defaultsans]{lato}
\usepackage{inconsolata}
''',
}

# Grouping the document tree into LaTeX files
latex_documents = [
    (master_doc, 'infrastructure-docs.tex', 
     'Infrastructure Documentation Standards', 'Infrastructure Team', 'manual'),
]

# Graphviz configuration
graphviz_output_format = 'svg'