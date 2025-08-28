#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

def main():
    docs_dir = Path("docs")
    docs_dir.mkdir(exist_ok=True)
    
    # Run sphinx-quickstart with minimal prompts
    cmd = [
        "sphinx-quickstart",
        "--quiet",
        "--project=Infrastructure Documentation", 
        "--author=Infrastructure Team",
        "--release=1.0",
        "--language=en",
        "--suffix=.rst",
        "--ext-autodoc",
        "--ext-intersphinx",
        "--ext-graphviz",
        "docs"
    ]
    
    subprocess.run(cmd, check=True)
    print("Sphinx project initialized")

if __name__ == "__main__":
    main()
