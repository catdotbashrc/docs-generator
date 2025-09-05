"""
Sphinx configuration for DDD Framework documentation.

This configuration enables comprehensive documentation generation including:
- Automatic API documentation from source code
- Support for both RST and Markdown formats
- Google/NumPy style docstring parsing
- Cross-project linking via intersphinx
- Documentation coverage reporting

Configuration follows Sphinx best practices for maintainability and extensibility.
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# ==================== PATH CONFIGURATION ====================
# Add source to path for autodoc
PROJECT_ROOT = Path(__file__).parent.parent
SRC_PATH = PROJECT_ROOT / 'src'
sys.path.insert(0, str(SRC_PATH.absolute()))

# ==================== PROJECT INFORMATION ====================
project = 'Documentation Driven Development (DDD) Framework'
copyright = f'2024-{datetime.now().year}, DDD Team'
author = 'DDD Team'

# Version information
version = '1.0.0'  # Short version
release = '1.0.0-beta'  # Full version including alpha/beta/rc tags

# Language settings
language = 'en'
master_doc = 'index'  # Main documentation file
source_suffix = {'.rst': 'restructuredtext', '.md': 'markdown'}

# ==================== SPHINX EXTENSIONS ====================
extensions = [
    # Core Sphinx extensions
    'sphinx.ext.autodoc',        # Auto-generate from docstrings
    'sphinx.ext.autodoc.typehints',  # Type hint support
    'sphinx.ext.napoleon',       # Google/NumPy style docstrings
    'sphinx.ext.viewcode',       # Add source code links
    'sphinx.ext.intersphinx',    # Link to other projects
    'sphinx.ext.coverage',       # Documentation coverage
    'sphinx.ext.todo',           # TODO directives
    'sphinx.ext.githubpages',    # GitHub Pages support
    
    # Third-party extensions (optional - install if needed)
    # 'myst_parser',             # Markdown support (requires: pip install myst-parser)
    # 'sphinx_autodoc2',         # Enhanced autodoc (requires: pip install sphinx-autodoc2)
    # 'sphinx_copybutton',       # Copy button for code blocks
    # 'sphinx_design',           # Cards, tabs, grids
]

# ==================== AUTODOC CONFIGURATION ====================
autodoc_default_options = {
    'members': True,              # Document all members
    'undoc-members': True,        # Include members without docstrings
    'private-members': False,     # Skip private members (_name)
    'special-members': '__init__, __str__, __repr__',  # Include special methods
    'inherited-members': True,    # Show inherited members
    'show-inheritance': True,     # Display inheritance diagrams
    'member-order': 'bysource',   # Preserve source code order
    'exclude-members': '__weakref__, __module__, __dict__',  # Skip noise
}

# Type hints configuration
autodoc_typehints = 'description'  # Show type hints in description
autodoc_typehints_format = 'short'  # Use short form for types
autodoc_type_aliases = {  # Custom type aliases
    'Path': 'pathlib.Path',
    'Dict': 'dict',
    'List': 'list',
}

# Mock imports for build without dependencies
autodoc_mock_imports = [
    'ansible',
    'boto3',
    'botocore',
]

# ==================== NAPOLEON CONFIGURATION ====================
# Support for Google and NumPy style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = True
napoleon_type_aliases = None
napoleon_attr_annotations = True

# ==================== HTML THEME CONFIGURATION ====================
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    # Navigation behavior
    'navigation_depth': 4,          # Maximum depth for navigation tree
    'collapse_navigation': False,   # Don't collapse navigation by default
    'sticky_navigation': True,      # Navigation stays visible when scrolling
    'includehidden': True,          # Include hidden toctrees in navigation
    'titles_only': False,           # Show section headers in navigation
    
    # Display options
    'display_version': True,        # Show version number
    'prev_next_buttons_location': 'bottom',  # Navigation button placement
    'style_external_links': True,   # Mark external links with icon
    
    # Analytics (optional - uncomment if needed)
    # 'analytics_id': 'G-XXXXXXXXXX',  # Google Analytics ID
    # 'analytics_anonymize_ip': True,   # Anonymize visitor IP
}

# HTML output options
html_title = "DDD Framework Documentation"
html_short_title = "DDD"
html_logo = None  # Path to logo (e.g., '_static/logo.png')
html_favicon = None  # Path to favicon (e.g., '_static/favicon.ico')
html_show_sourcelink = True      # Show "View page source" link
html_show_sphinx = False         # Hide "Created using Sphinx" footer
html_show_copyright = True       # Show copyright notice
html_last_updated_fmt = '%b %d, %Y'  # Date format for last updated

# Static files and templates
html_static_path = ['_static']
templates_path = ['_templates']

# Additional CSS files
html_css_files = [
    # 'custom.css',  # Custom CSS overrides
]

# Additional JavaScript files
html_js_files = [
    # 'custom.js',  # Custom JavaScript
]

# ==================== INTERSPHINX CONFIGURATION ====================
# Links to other project documentation
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'click': ('https://click.palletsprojects.com/en/8.1.x/', None),
    'rich': ('https://rich.readthedocs.io/en/stable/', None),
    'pytest': ('https://docs.pytest.org/en/stable/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
    'pyyaml': ('https://pyyaml.org/wiki/', None),
}

# ==================== BUILD CONFIGURATION ====================
# Patterns to exclude from build
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    '**/__pycache__',
    '**.pyc',
    '**/*.egg-info',
    '.venv',
    'venv',
]

# Suppress specific warnings
suppress_warnings = [
    'image.nonlocal_uri',  # Allow external images
    # 'app.add_directive',  # Allow directive overrides
]

# ==================== TODO EXTENSION ====================
# Include TODO directives in output
todo_include_todos = True
todo_emit_warnings = True  # Warn about TODOs in console

# ==================== COVERAGE EXTENSION ====================
# Documentation coverage settings
coverage_show_missing_items = True
coverage_skip_undoc_in_source = False  # Don't skip undocumented items
coverage_write_headline = True  # Write module headlines
coverage_statistics_to_report = True  # Add statistics to report
coverage_statistics_to_stdout = True  # Print statistics to console

# ==================== ADDITIONAL SETTINGS ====================
# Nitpicky mode - warn about broken references
nitpicky = False  # Set True for strict builds
nitpick_ignore = [
    ('py:class', 'type'),
    ('py:class', 'module'),
]

# Figure numbering
numfig = True
numfig_format = {
    'figure': 'Figure %s',
    'table': 'Table %s',
    'code-block': 'Listing %s',
}

# Code highlighting
pygments_style = 'sphinx'  # Syntax highlighting theme
highlight_language = 'python'  # Default language for code blocks

# Keep warnings as errors for CI/CD
keep_warnings = True
warning_is_error = False  # Set True for strict CI builds