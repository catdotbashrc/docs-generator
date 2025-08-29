# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Documentation Driven Development (DDD) Framework - A parallel to Test-Driven Development (TDD) for documentation. This framework measures documentation completeness using coverage metrics, similar to how TDD uses test coverage for code quality.

**Core Philosophy**: Apply RED-GREEN-REFACTOR cycle to documentation:
1. RED: Define documentation specifications (what complete documentation looks like)
2. GREEN: Extract documentation from codebase until specs pass  
3. REFACTOR: Improve documentation quality while maintaining coverage

## Development Commands

```bash
# Install dependencies (using uv package manager - NOT pip)
uv venv
uv pip install -e .
uv pip install -e ".[dev]"  # Include dev dependencies

# Run the CLI tool
ddd measure ./path/to/project              # Measure documentation coverage
ddd assert-coverage ./path/to/project      # Assert coverage meets threshold (85% default)
ddd demo ./path/to/project                 # Run RED-GREEN-REFACTOR demo

# Testing
pytest                                      # Run all tests
pytest tests/test_baseline_ansible.py -v   # Run specific test
pytest --cov=src --cov-report=html        # Generate coverage report

# Code Quality
black src/ tests/ --line-length 100        # Format code
ruff check src/ tests/                     # Lint code
```

## Architecture Overview

The framework implements a plugin-based architecture for extensibility:

### Core Components

**DocumentationCoverage** (`src/ddd/coverage/__init__.py`)
- Central coverage calculator implementing 3-level measurement:
  - Element Coverage (30%): Documentation exists
  - Completeness Coverage (40%): Required fields present
  - Usefulness Coverage (30%): "2AM test" - usable during emergencies
- Weighted scoring across DAYLIGHT dimensions
- Pass/fail threshold: 85% default

**DimensionSpec & DAYLIGHTSpec** (`src/ddd/specs/__init__.py`)
- Define documentation requirements for 8 DAYLIGHT dimensions:
  - Dependencies, Automation, Yearbook, Lifecycle, Integration, Governance, Health, Testing
- Each dimension has required elements, fields, minimum coverage, and weight
- Specs validate extracted documentation against requirements

**DependencyExtractor** (`src/ddd/extractors/__init__.py`)
- Extract dependency information from projects (MVP implementation)
- Supports JavaScript/Node.js (package.json) and Python (pyproject.toml, requirements.txt)
- Pattern for future extractors: inherit common interface, implement extract() method

### Key Design Patterns

1. **Plugin Architecture**: Extractors are designed to be pluggable - add new language support by creating new extractor classes
2. **Specification Pattern**: DimensionSpec defines what "complete" looks like for each documentation dimension
3. **Coverage Calculation**: Three-tiered coverage measurement mimics code coverage tools
4. **CLI Integration**: Rich terminal output using Click framework with color coding and tables

## Technical Constraints

- **Python 3.11+** required
- **UV package manager** (not pip) for dependency management
- **100-character line length** for code formatting
- **pyproject.toml** for all project configuration (not setup.cfg)

## Current Implementation Status

**MVP Phase** - Focus on Dependencies dimension:
- ✅ Dependencies extractor (JavaScript/Python)
- ✅ Coverage measurement engine
- ✅ CLI with measure/assert commands
- ⚠️ Other DAYLIGHT dimensions have specs but simplified extractors
- ❌ Comprehensive test coverage needed

**Baseline Reference**: Ansible project (in `baseline/ansible/` as git submodule) serves as reference implementation with 90% DAYLIGHT coverage target.

## Key Implementation Details

When modifying extractors:
- File operations should use `pathlib.Path` objects
- Include error handling for malformed configuration files
- Return consistent Dict structure with dimension data

When working with coverage calculations:
- Weights are configurable per dimension in DAYLIGHTSpec
- Overall coverage uses weighted average across dimensions
- Missing elements tracked for actionable recommendations

CLI command structure:
- Commands defined in `src/cli.py` using Click decorators
- Rich console for formatted output (tables, panels, colors)
- Exit code 1 on coverage failure for CI/CD integration