"""
Sphinx configuration for DDD Framework documentation.
Auto-generates API docs from source code.
"""

import os
import sys
from pathlib import Path

# Add source to path for autodoc
sys.path.insert(0, os.path.abspath('../src'))

# Project information
project = 'DDD Framework'
copyright = '2024, DDD Team'
author = 'DDD Team'
release = '0.1.0'

# Extensions for auto-documentation
extensions = [
    'sphinx.ext.autodoc',        # Auto-generate from docstrings
    'sphinx.ext.napoleon',       # Google/NumPy style docstrings
    'sphinx.ext.viewcode',       # Add source code links
    'sphinx.ext.intersphinx',    # Link to other projects
    'sphinx.ext.coverage',       # Documentation coverage
    'sphinx.ext.todo',           # TODO directives
    'myst_parser',               # Markdown support
    'sphinx_autodoc2',           # Better autodoc
]

# Autodoc settings - extract everything!
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'private-members': False,
    'special-members': '__init__',
    'inherited-members': True,
    'show-inheritance': True,
}

# Napoleon settings for docstring parsing
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True

# MyST parser for Markdown files
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# Theme configuration
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'navigation_depth': 4,
    'collapse_navigation': False,
    'sticky_navigation': True,
    'includehidden': True,
    'titles_only': False,
}

# Static files
html_static_path = ['_static']
templates_path = ['_templates']

# Output settings
html_title = "DDD Framework Documentation"
html_short_title = "DDD"
html_show_sourcelink = True
html_show_sphinx = False
html_show_copyright = True

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'click': ('https://click.palletsprojects.com/en/8.1.x/', None),
    'rich': ('https://rich.readthedocs.io/en/stable/', None),
}

# Exclude patterns
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# TODO extension
todo_include_todos = True

# Coverage extension
coverage_show_missing_items = True