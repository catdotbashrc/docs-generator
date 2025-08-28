# Infrastructure Documentation Standards - Project Index

> **Automated infrastructure documentation system solving "Where is the config for X?"**

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://python.org)
[![UV](https://img.shields.io/badge/UV-Package%20Manager-green)](https://github.com/astral-sh/uv)
[![Sphinx](https://img.shields.io/badge/Sphinx-Documentation-orange)](https://www.sphinx-doc.org/)
[![Architecture](https://img.shields.io/badge/Architecture-7.2%2F10-yellow)](docs/architecture/ARCHITECTURE_ANALYSIS_REPORT.md)

## 📚 Table of Contents

- [Project Overview](#project-overview)
- [Current Status](#current-status)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Components](#components)
- [CLI Commands](#cli-commands)
- [Development](#development)
- [Testing](#testing)
- [Documentation](#documentation)
- [Roadmap](#roadmap)

## 🎯 Project Overview

### Problem Statement
Our 10-person consulting team manages 10+ clients across healthcare, logistics, and public sectors. The recurring challenge **"Where is the config for X?"** causes:
- Extended incident response times
- Inconsistent project handoffs
- Manual documentation overhead
- Knowledge silos

### Solution
An automated Sphinx-based documentation system that:
- **Discovers** infrastructure configurations automatically
- **Generates** standardized documentation
- **Maintains** up-to-date technical references
- **Delivers** professional client documentation

### Business Impact
- **40% reduction** in incident response time
- **8 hours → 2-3 hours** for project handoffs
- **Automated** daily documentation updates
- **Professional** client deliverables

## 📊 Current Status

**Implementation Progress: 25% Complete**

| Component | Status | Progress | Priority |
|-----------|--------|----------|----------|
| **Core Infrastructure** | ✅ Complete | 100% | - |
| **Java API Parser** | ✅ Complete | 100% | Medium |
| **Filesystem Abstraction** | ✅ Complete | 100% | Low |
| **Azure Discovery** | ❌ Not Started | 0% | **CRITICAL** |
| **SQL Discovery** | ❌ Not Started | 0% | **CRITICAL** |
| **GCP Discovery** | ❌ Not Started | 0% | Medium |
| **Deployment** | ❌ Not Started | 0% | Low |

**Architecture Score**: 7.2/10 - Strong foundation, incomplete implementation

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- UV package manager
- Azure CLI (for Azure discovery)
- SQL Server drivers (for SQL discovery)

### Installation

```bash
# Clone repository
git clone <repository-url>
cd infrastructure-documentation-standards

# Install UV package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync --all-groups

# Verify installation
uv run docs-build --help
```

### Basic Usage

```bash
# Build documentation
uv run docs-build

# Serve documentation locally
uv run docs-serve

# Extract Java API documentation
uv run java-docs /path/to/java/project --output docs/

# Clean build artifacts
uv run docs-clean
```

## 📁 Project Structure

```
infrastructure-documentation-standards/
│
├── automation/                 # Core automation modules
│   ├── filesystem/            # Filesystem abstraction layer
│   │   ├── abstract.py       # Base filesystem interface
│   │   ├── local.py          # Local filesystem implementation
│   │   ├── memory.py         # In-memory filesystem
│   │   └── factory.py        # Filesystem factory
│   │
│   ├── java_ast_extractor.py # Java API documentation extractor
│   ├── java_parser.py        # Java source parser
│   ├── build.py              # Sphinx build orchestration
│   └── setup.py              # Initial setup utilities
│
├── docs/                      # Documentation
│   ├── architecture/         # Architecture documents
│   ├── claude-reports/       # AI-generated analysis
│   ├── learning/            # Educational materials
│   └── source/              # Sphinx source files
│       ├── _templates/      # Documentation templates
│       ├── conf.py         # Sphinx configuration
│       └── examples/       # Example projects (DSNY)
│
├── tests/                    # Test suite
│   ├── test_filesystem_abstraction.py
│   ├── test_java_ast_extractor.py
│   └── test_example_integration.py
│
├── scripts/                  # Utility scripts
│   └── setup_sphinx.py
│
├── pyproject.toml           # Project configuration
├── uv.lock                  # Dependency lock file
├── README.md               # Project readme
└── CLAUDE.md              # Claude AI instructions
```

## 🔧 Components

### Implemented Components

#### 1. Filesystem Abstraction Layer
**Location**: `automation/filesystem/`
- Abstract base class defining filesystem operations
- Local filesystem implementation
- Memory filesystem for testing
- Factory pattern for instantiation

```python
from automation.filesystem.factory import FileSystemFactory

# Create filesystem instance
fs = FileSystemFactory.create("local", root="/path/to/root")

# Use filesystem operations
content = fs.read_text("config.yaml")
fs.write_text("output.txt", content)
```

#### 2. Java API Documentation Extractor
**Location**: `automation/java_ast_extractor.py`
- AST-based Java source analysis
- SOAP/REST endpoint extraction
- Spring annotation support
- Data model discovery

```python
from automation.java_ast_extractor import JavaASTExtractor
from automation.filesystem.local import LocalFileSystem

fs = LocalFileSystem()
extractor = JavaASTExtractor(fs)
docs = extractor.extract_documentation("src/main/java/")
```

#### 3. Sphinx Documentation Builder
**Location**: `automation/build.py`
- Automated Sphinx build orchestration
- Multiple output formats (HTML, PDF)
- Parallel build support
- Clean build capability

### Planned Components (Critical Path)

#### 1. Azure Discovery Module 🚨
**Location**: `automation/azure.py` (to be created)
```python
class AzureDiscovery:
    """Discover Azure resources and configurations"""
    - Resource Groups
    - Virtual Machines
    - Storage Accounts
    - Networks & Subnets
    - Key Vaults
```

#### 2. SQL Discovery Module 🚨
**Location**: `automation/sql.py` (to be created)
```python
class SQLDiscovery:
    """Extract SQL Server schemas and metadata"""
    - Tables & Columns
    - Views & Procedures
    - Relationships
    - ERD Generation
```

## 📋 CLI Commands

### Available Commands

| Command | Purpose | Status |
|---------|---------|--------|
| `docs-build` | Build Sphinx documentation | ✅ Working |
| `docs-serve` | Serve documentation locally | ✅ Working |
| `docs-clean` | Clean build artifacts | ✅ Working |
| `docs-setup` | Initial setup wizard | ✅ Working |
| `java-docs` | Extract Java API docs | ✅ Working |
| `azure-docs` | Generate Azure docs | ❌ Not Implemented |
| `sql-docs` | Generate SQL docs | ❌ Not Implemented |
| `deploy-itglue` | Deploy to IT Glue | ❌ Not Implemented |

### Command Examples

```bash
# Build documentation with specific format
uv run docs-build --format pdf

# Extract Java documentation
uv run java-docs ./src --output ./docs/api/

# Serve documentation with hot reload
uv run docs-serve --port 8080

# Clean all build artifacts
uv run docs-clean --all
```

## 🧪 Testing

### Test Coverage
- **Current Coverage**: ~80%
- **Test Framework**: pytest
- **Test Types**: Unit, Integration, Contract

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=automation --cov-report=html

# Run specific test file
uv run pytest tests/test_java_ast_extractor.py

# Run with verbose output
uv run pytest -v --tb=short
```

### Test Organization

```
tests/
├── test_filesystem_abstraction.py  # 15 contract tests
├── test_java_ast_extractor.py     # 15 comprehensive tests
└── test_example_integration.py   # Real-world integration test
```

## 📖 Documentation

### Documentation Types

| Type | Location | Purpose |
|------|----------|---------|
| **Architecture** | `docs/architecture/` | System design and technical decisions |
| **API Reference** | Generated via CLI | Automated API documentation |
| **User Guides** | `docs/learning/` | Tutorials and how-to guides |
| **Templates** | `docs/source/_templates/` | Reusable documentation templates |

### Building Documentation

```bash
# Build HTML documentation
uv run docs-build

# Build PDF documentation
uv run docs-build --format pdf

# Build with specific theme
uv run docs-build --theme furo
```

## 🗺️ Roadmap

### Phase 1: Critical Path (Weeks 1-2) 🚨

**Goal**: Deliver MVP with core discovery functionality

- [ ] Implement Azure Discovery Module
  - [ ] Resource enumeration
  - [ ] Configuration extraction
  - [ ] Template integration
  
- [ ] Implement SQL Discovery Module
  - [ ] Schema extraction
  - [ ] Relationship mapping
  - [ ] ERD generation

### Phase 2: Configuration & Error Handling (Weeks 3-4)

**Goal**: Production-ready configuration and resilience

- [ ] Configuration Management System
  - [ ] Pydantic models
  - [ ] Environment variables
  - [ ] Secrets management
  
- [ ] Error Handling Framework
  - [ ] Exception hierarchy
  - [ ] Retry decorators
  - [ ] Circuit breakers

### Phase 3: Optimization (Month 2)

**Goal**: Scale and performance improvements

- [ ] Async Processing
  - [ ] Parallel discovery
  - [ ] Worker pools
  - [ ] Progress tracking
  
- [ ] Caching Layer
  - [ ] API response caching
  - [ ] TTL management
  - [ ] Cache warming

### Phase 4: Extension (Quarter 2)

**Goal**: Multi-cloud and automation

- [ ] GCP Support
- [ ] Deployment Automation
- [ ] Real-time Updates
- [ ] Webhook Integration

## 🛠️ Development

### Environment Setup

```bash
# Create virtual environment with UV
uv venv

# Install development dependencies
uv sync --group dev

# Install pre-commit hooks
pre-commit install
```

### Code Quality Tools

| Tool | Purpose | Command |
|------|---------|---------|
| **Black** | Code formatting | `uv run black .` |
| **isort** | Import sorting | `uv run isort .` |
| **Ruff** | Linting | `uv run ruff check .` |
| **MyPy** | Type checking | `uv run mypy .` |

### Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/azure-discovery`)
3. Implement with tests
4. Run quality checks (`uv run pytest && uv run ruff check`)
5. Submit pull request

## 🔗 Links & Resources

### Project Documentation
- [Architecture Analysis](docs/architecture/ARCHITECTURE_ANALYSIS_REPORT.md)
- [Project Specification](docs/architecture/PROJECT_SPECIFICATION.md)
- [Filesystem Abstraction Design](docs/architecture/FILESYSTEM_ABSTRACTION_DESIGN.md)
- [Test Suite Architecture](docs/architecture/TEST_SUITE_ARCHITECTURE.md)

### External Resources
- [UV Package Manager](https://github.com/astral-sh/uv)
- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [Azure SDK for Python](https://docs.microsoft.com/en-us/python/azure/)
- [PyODBC Documentation](https://github.com/mkleehammer/pyodbc)

## 📈 Metrics & Goals

### Success Metrics
- **Incident Response**: 40% reduction in response time
- **Handoff Time**: From 8 hours to 2-3 hours
- **Documentation Coverage**: 100% of infrastructure components
- **Update Frequency**: Daily automated updates

### Quality Metrics
- **Test Coverage**: Maintain >80%
- **Code Quality**: Architecture score >7/10
- **Performance**: Discovery <5 minutes for typical infrastructure
- **Reliability**: 99.9% uptime for documentation portal

---

**Last Updated**: 2025-08-27
**Version**: 0.1.0
**Status**: Active Development - Critical Path Focus on Azure/SQL Discovery