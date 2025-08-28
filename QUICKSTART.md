# Quick Start Guide - Infrastructure Documentation Standards

Get up and running with the Infrastructure Documentation Standards system in under 10 minutes.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [First Documentation Build](#first-documentation-build)
- [Java API Documentation](#java-api-documentation)
- [Common Workflows](#common-workflows)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements
- **Python**: 3.11 or higher
- **Memory**: 2GB RAM minimum
- **Disk**: 500MB free space
- **OS**: Windows, macOS, or Linux

### Required Software
```bash
# Check Python version
python --version  # Should be 3.11+

# Install UV package manager (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or on Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Optional Software (for full functionality)
- **Azure CLI**: For Azure resource discovery
- **SQL Server drivers**: For database documentation
- **Java 8+**: For parsing Java source code

---

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd infrastructure-documentation-standards
```

### 2. Install Dependencies with UV
```bash
# Install all dependencies (recommended)
uv sync --all-groups

# Or install core dependencies only
uv sync
```

### 3. Verify Installation
```bash
# Test the CLI commands
uv run docs-build --help

# Should display:
# Usage: docs-build [OPTIONS]
# Build Sphinx documentation in various formats...
```

---

## First Documentation Build

### Build HTML Documentation (Default)
```bash
# Build documentation with default settings
uv run docs-build

# Output will be in docs/build/html/
# Open docs/build/html/index.html in your browser
```

### Serve Documentation Locally
```bash
# Start development server with hot-reload
uv run docs-serve

# Visit http://127.0.0.1:8000 in your browser
# Documentation auto-rebuilds when you save changes
```

### Build Different Formats
```bash
# Build PDF documentation
uv run docs-build --format pdf

# Clean and rebuild
uv run docs-build --clean

# Verbose output for debugging
uv run docs-build --verbose
```

---

## Java API Documentation

### Extract Documentation from Java Project
```bash
# Basic usage
uv run java-docs /path/to/java/project --output docs/api/

# With specific format
uv run java-docs ./src/main/java --format json > api.json

# Recursive processing
uv run java-docs ./MyProject --recursive --verbose
```

### Example: Document DSNY Project
```bash
# Run the included example
uv run java-docs /path/to/java/project --output docs/source/examples/

# This will extract:
# - 7 SOAP endpoints
# - Service classes
# - Data models
# - Repository interfaces
```

### Understanding the Output
```json
{
  "language": "java",
  "endpoints": [
    {
      "type": "SOAP",
      "operation": "getWorkUnits",
      "method_name": "getWorkUnits",
      "return_type": "List<WorkUnitModel>",
      "parameters": [
        {"name": "queryDate", "type": "String"}
      ]
    }
  ],
  "services": [...],
  "models": [...]
}
```

---

## Common Workflows

### 1. Starting a New Documentation Project

```bash
# Step 1: Create project structure
mkdir -p docs/source/{_templates,_static,examples}

# Step 2: Initialize Sphinx configuration (if needed)
uv run docs-setup

# Step 3: Extract API documentation
uv run java-docs ./src --output docs/source/api/

# Step 4: Build and serve
uv run docs-build
uv run docs-serve
```

### 2. Updating Existing Documentation

```bash
# Clean previous build
uv run docs-clean

# Re-extract API documentation
uv run java-docs ./src --output docs/source/api/ --format rst

# Rebuild with verbose output
uv run docs-build --verbose --clean

# Deploy to IT Glue (when implemented)
# uv run deploy-itglue
```

### 3. Development Workflow

```bash
# Install development dependencies
uv sync --group dev

# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=automation

# Format code
uv run black automation/
uv run isort automation/

# Run linting
uv run ruff check automation/
```

### 4. Using the Filesystem Abstraction

```python
from automation.filesystem.factory import FileSystemFactory

# Create filesystem instance
fs = FileSystemFactory.create("local", root="/project/root")

# Basic operations
content = fs.read_text("config.yaml")
fs.write_text("output.txt", "Hello World")
files = fs.list_files("src", pattern="*.py", recursive=True)

# Check existence
if fs.exists("important.conf"):
    size = fs.get_size("important.conf")
```

### 5. Testing with In-Memory Filesystem

```python
from automation.filesystem.memory import MemoryFileSystem

# Create test filesystem
fs = MemoryFileSystem()

# Use for testing without touching disk
fs.write_text("test.txt", "test content")
assert fs.exists("test.txt")
assert fs.read_text("test.txt") == "test content"
```

---

## Troubleshooting

### Common Issues and Solutions

#### 1. UV Installation Fails
```bash
# Alternative: Use pip with virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

#### 2. Sphinx Build Errors
```bash
# Clear cache and rebuild
uv run docs-clean --all
uv run docs-build --clean --verbose

# Check for missing dependencies
uv sync --all-groups
```

#### 3. Java Parser Not Finding Files
```bash
# Verify Java files exist
ls -la /path/to/java/project/**/*.java

# Use verbose mode to see what's being processed
uv run java-docs /path/to/project -v

# Check for correct package structure
# Should have: src/main/java/com/example/...
```

#### 4. Permission Errors
```bash
# Ensure write permissions
chmod -R u+w docs/build/

# Run with elevated permissions if needed (not recommended)
sudo uv run docs-build
```

#### 5. Import Errors
```python
# If automation module not found
uv pip install -e .

# Verify installation
python -c "import automation; print(automation.__file__)"
```

### Debug Mode

Enable detailed logging for troubleshooting:

```python
# In your Python scripts
import logging
logging.basicConfig(level=logging.DEBUG)

# Or set environment variable
export PYTHONPATH=.
export DEBUG=1
uv run java-docs ./src --verbose
```

### Getting Help

1. **Check Logs**: Look in `docs/build/` for Sphinx build logs
2. **Verbose Mode**: Add `--verbose` to any command
3. **Test Individual Components**:
   ```bash
   # Test Java parser directly
   python automation/java_parser.py /path/to/file.java
   
   # Test build system
   python automation/build.py --verbose
   ```

4. **Report Issues**: Include:
   - Python version (`python --version`)
   - UV version (`uv --version`)
   - Full error message
   - Steps to reproduce

---

## Next Steps

Once you have the basic system running:

1. **Implement Azure Discovery** (Critical Path)
   - See `docs/architecture/PROJECT_SPECIFICATION.md` for requirements
   - Module location: `automation/azure.py` (to be created)

2. **Implement SQL Discovery** (Critical Path)
   - See API_REFERENCE.md for planned structure
   - Module location: `automation/sql.py` (to be created)

3. **Customize Templates**
   - Edit templates in `docs/source/_templates/`
   - Add client-specific branding
   - Create custom Sphinx directives

4. **Set Up CI/CD**
   - Configure automated documentation builds
   - Schedule regular infrastructure discovery
   - Set up deployment to IT Glue

5. **Review Architecture**
   - Read `ARCHITECTURE_ANALYSIS_REPORT.md`
   - Understand the 25% implementation status
   - Focus on critical path modules

---

## Example: Complete Workflow

Here's a complete example documenting a Java microservice:

```bash
# 1. Setup project
git clone <repo>
cd infrastructure-documentation-standards
uv sync --all-groups

# 2. Extract Java API documentation
uv run java-docs ~/projects/my-service/src/main/java \
  --output docs/source/api/ \
  --format rst \
  --verbose

# 3. Build documentation
uv run docs-build --clean

# 4. Serve locally
uv run docs-serve --open

# 5. Generate PDF for client
uv run docs-build --format pdf

# 6. Deploy (when implemented)
# export ITGLUE_API_KEY="your-key"
# uv run deploy-itglue

# Documentation is now available at:
# - HTML: docs/build/html/index.html
# - PDF: docs/build/latex/*.pdf
```

---

## Support

- **Documentation**: See [PROJECT_INDEX.md](PROJECT_INDEX.md) for complete overview
- **API Reference**: See [API_REFERENCE.md](docs/API_REFERENCE.md) for detailed API docs
- **Architecture**: See [ARCHITECTURE_ANALYSIS_REPORT.md](docs/architecture/ARCHITECTURE_ANALYSIS_REPORT.md)
- **Issues**: Report at [GitHub Issues](https://github.com/your-org/infrastructure-docs-template/issues)

---

**Last Updated**: 2025-08-27  
**Version**: 0.1.0  
**Status**: Ready for Development (25% Complete - Azure/SQL modules needed)