#!/usr/bin/env python3
"""
Documentation Build Automation

Clean Sphinx build script following official patterns.
Builds HTML and PDF documentation with proper error handling.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import argparse
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def get_project_root():
    """Get the project root directory."""
    return Path(__file__).parent.parent


def build_documentation(output_format="html", clean=False):
    """
    Build documentation using sphinx-build directly.
    Uses the -M option for make-mode as recommended by Context7.
    """
    project_root = get_project_root()
    docs_dir = project_root / "docs"
    source_dir = docs_dir / "source"
    build_dir = docs_dir / "build"
    
    # Verify source directory exists
    if not source_dir.exists():
        logger.error(f"Source directory not found: {source_dir}")
        return False
    
    # Clean build directory if requested
    if clean and build_dir.exists():
        logger.info("Cleaning build directory")
        shutil.rmtree(build_dir)
    
    # Build command using -M make-mode (Context7 recommended pattern)
    cmd = [
        sys.executable, "-m", "sphinx",
        "-M", output_format,
        str(source_dir),
        str(build_dir)
    ]
    
    # Add parallel processing if available
    cmd.extend(["-j", "auto"])
    
    logger.info(f"Building {output_format} documentation...")
    logger.debug(f"Command: {' '.join(cmd)}")
    
    try:
        # Run in docs directory for proper path resolution
        result = subprocess.run(
            cmd, 
            check=True, 
            capture_output=True, 
            text=True, 
            cwd=docs_dir
        )
        
        logger.info(f"✅ {output_format.upper()} build successful")
        if result.stdout.strip():
            logger.debug(f"Build output:\n{result.stdout}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ {output_format.upper()} build failed")
        logger.error(f"Exit code: {e.returncode}")
        if e.stderr:
            logger.error(f"Error output:\n{e.stderr}")
        if e.stdout:
            logger.error(f"Build output:\n{e.stdout}")
        return False


def validate_environment():
    """Validate that Sphinx is available and source directory exists."""
    # Check if sphinx is available
    try:
        result = subprocess.run(
            [sys.executable, "-m", "sphinx", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        logger.info(f"Using {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.error("Sphinx not found. Install with: pip install sphinx")
        return False
    
    # Check source directory
    project_root = get_project_root()
    source_dir = project_root / "docs" / "source"
    if not source_dir.exists():
        logger.error(f"Source directory not found: {source_dir}")
        return False
    
    # Check for conf.py
    conf_file = source_dir / "conf.py"
    if not conf_file.exists():
        logger.error(f"Configuration file not found: {conf_file}")
        return False
    
    return True


def show_build_results(output_format):
    """Show the location of built documentation."""
    project_root = get_project_root()
    build_path = project_root / "docs" / "build" / output_format
    
    if build_path.exists():
        logger.info(f"📄 Documentation built at: {build_path}")
        
        # Show specific entry points
        if output_format == "html":
            index_file = build_path / "index.html"
            if index_file.exists():
                logger.info(f"🌐 Open in browser: file://{index_file.absolute()}")
        
        elif output_format == "latex":
            tex_files = list(build_path.glob("*.tex"))
            if tex_files:
                logger.info(f"📝 LaTeX files: {[f.name for f in tex_files]}")
        
        elif output_format == "latexpdf":
            pdf_files = list(build_path.glob("*.pdf"))
            if pdf_files:
                logger.info(f"📋 PDF files: {[f.name for f in pdf_files]}")


def main():
    """Main entry point for documentation building."""
    parser = argparse.ArgumentParser(
        description='Build infrastructure documentation using Sphinx',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s                    # Build HTML documentation  
  %(prog)s --format pdf       # Build PDF documentation
  %(prog)s --clean            # Clean and rebuild
  %(prog)s --format latexpdf  # Build LaTeX and PDF
        '''
    )
    
    parser.add_argument(
        '--format', 
        default='html',
        choices=['html', 'latex', 'latexpdf', 'epub', 'text'],
        help='Output format (default: html)'
    )
    parser.add_argument(
        '--clean', 
        action='store_true',
        help='Clean build directory before building'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true', 
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logger.info("🚀 Starting documentation build process")
    
    # Validate environment
    if not validate_environment():
        sys.exit(1)
    
    # Build documentation
    if not build_documentation(args.format, args.clean):
        logger.error("💥 Build failed")
        sys.exit(1)
    
    # Show results
    show_build_results(args.format)
    
    logger.info("✨ Build completed successfully")


if __name__ == "__main__":
    main()