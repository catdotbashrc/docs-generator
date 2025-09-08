# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

### What is Documentation Driven Development (DDD)?

Documentation Driven Development (DDD) Framework - A revolutionary approach that applies Test-Driven Development principles to documentation. Just as TDD ensures code quality through tests, DDD ensures maintenance readiness through documentation coverage.

**The Problem We're Solving**: 
- Development teams create solutions, maintenance teams inherit them
- Critical maintenance knowledge is lost in handoffs
- No systematic way to measure "maintenance readiness"
- Documentation is treated as an afterthought, not a deliverable

**The DDD Solution**:
- Treat documentation as code with measurable coverage
- Focus on maintenance scenarios, not code coverage
- Extract actionable documentation from existing code
- Generate maintenance runbooks automatically

### Core Philosophy: RED-GREEN-REFACTOR for Documentation

1. **RED**: Define what "complete" maintenance documentation looks like
   - Specifications for each maintenance dimension (permissions, errors, state, etc.)
   - Minimum coverage thresholds (85% default)
   - Maintenance scenario requirements

2. **GREEN**: Extract documentation until specifications pass
   - Parse code for maintenance-critical information
   - Generate scenarios from patterns
   - Measure coverage against specifications

3. **REFACTOR**: Improve quality while maintaining coverage
   - Enhance extracted documentation
   - Add human insights where automation falls short
   - Optimize for 2AM emergency use

## Development Commands

### Using Invoke (Recommended Python Task Runner)

```bash
# Install dependencies (using uv package manager - NOT pip)
uv add --dev invoke  # Add invoke to dev dependencies
uv pip install -e ".[dev]"  # Install all dev dependencies

# View all available tasks
uv run invoke --list

# Common development tasks
uv run invoke setup          # Complete dev environment setup
uv run invoke format         # Format code with black and ruff
uv run invoke test           # Run all tests
uv run invoke test --critical  # Run only critical tests (must pass)
uv run invoke test --coverage  # Run with coverage report
uv run invoke docs           # Build Sphinx documentation
uv run invoke docs --live    # Live-reload documentation server
uv run invoke demo-prep      # Prepare everything for demo

# Pre-commit hooks (automatic formatting and testing)
uv run invoke hooks          # Install pre-commit hooks
uv run invoke pre-commit     # Run pre-commit checks manually

# Cleanup
uv run invoke clean          # Remove all generated files
```

### Direct CLI Commands

```bash
# Run the DDD CLI tool
uv run ddd measure ./path/to/project              # Measure documentation coverage
uv run ddd assert-coverage ./path/to/project      # Assert coverage meets threshold (85% default)
uv run ddd config-coverage ./path/to/project      # Check configuration documentation
uv run ddd demo ./path/to/project                 # Run RED-GREEN-REFACTOR demo

# Testing commands
uv run pytest                                      # Run all tests
uv run pytest tests/test_extractor_contract.py -v # Run contract tests (most important)
uv run pytest tests/config_extractors/ -v         # Run config extractor tests
uv run pytest tests/red_phase/ -v                 # Run RED phase tests (should fail initially)
uv run pytest tests/green_phase/ -v               # Run GREEN phase tests (should pass)
uv run pytest tests/test_coverage.py -v           # Run coverage calculation tests
uv run pytest --cov=src --cov-report=html         # Generate HTML coverage report
uv run pytest -k "config" -v                      # Run tests matching pattern
uv run pytest --lf                                # Run only failed tests from last run

# Manual formatting
black src/ tests/ --line-length 100               # Format code
ruff check src/ tests/ --fix                      # Lint and fix code
```

## Our TDD Development Workflow

### How We Build DDD (Using TDD)

We practice what we preach - using Test-Driven Development to build Documentation Driven Development:

1. **RED Phase**: Write failing tests first
   ```python
   # First, define what we expect
   def test_extract_aws_permissions():
       extractor = AnsibleModuleExtractor()
       content = "client.describe_instances()"
       permissions = extractor.extract_permissions(content)
       assert "ec2:DescribeInstances" in permissions  # FAILS
   ```

2. **GREEN Phase**: Implement minimal code to pass
   ```python
   # Then, make it work
   def extract_permissions(self, content):
       # Just enough code to pass the test
       return ["ec2:DescribeInstances"]
   ```

3. **REFACTOR Phase**: Improve while keeping tests green
   ```python
   # Finally, make it right
   def extract_permissions(self, content):
       # Robust pattern matching, deduplication, etc.
       permissions = self._parse_boto3_calls(content)
       return self._deduplicate(permissions)
   ```

**Current Test Coverage**: 48 tests across base and Ansible extractors

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

**ConfigurationExtractor** (`src/ddd/config_extractors/__init__.py`)
- NEW: Multi-language configuration discovery system
- Extracts environment variables, config files, and constants
- Security-aware: Automatically flags sensitive data
- Supports Python, JavaScript, YAML, JSON, TOML, .env files
- Pattern-based extraction with language-specific rules

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

1. **Plugin Architecture**: All extractors inherit from base classes
   - `InfrastructureExtractor` for tool-specific extraction (Ansible, Terraform)
   - `ConfigurationExtractor` for configuration discovery
   - New extractors: inherit base, implement `extract()` method

2. **Test-Driven Development Structure**:
   ```
   tests/
   ├── red_phase/     # Tests that define requirements (fail first)
   ├── green_phase/   # Tests that verify implementation 
   └── refactor_phase/  # Tests for optimization
   ```
   Always write RED phase tests before implementing features

3. **Coverage Calculation Flow**:
   - Extract documentation → Apply DAYLIGHT specs → Calculate 3-tier coverage
   - Each dimension weighted differently (Governance: 1.3, Yearbook: 0.8)
   - Overall threshold: 85% for passing

## Technical Constraints

- **Python 3.11+** required
- **UV package manager** (not pip) for dependency management
- **100-character line length** for code formatting
- **pyproject.toml** for all project configuration (not setup.cfg)

## Troubleshooting

### Common Issues and Solutions

**Import Errors**
```bash
# Wrong: Using pip
pip install -e .

# Correct: Using uv
uv pip install -e .
uv pip install -e ".[dev]"  # Include dev dependencies
```

**Test Failures**
```bash
# Clean test artifacts
rm -rf .pytest_cache/
rm /tmp/test_*.txt  # Remove temporary test files

# Run with verbose output
uv run pytest -v --tb=short
```

**Coverage Report Issues**
```bash
# Ensure dev dependencies installed
uv pip install -e ".[dev]"

# Use correct coverage path
uv run pytest --cov=src --cov-report=html  # Not --cov=ddd
```

**Module Not Found**
```bash
# Ensure editable install
uv pip install -e .

# Check Python path
python -c "import sys; print(sys.path)"
```

## Current Implementation Status

### Completed Extractors
- **AnsibleModuleExtractor**: AWS IAM permissions from boto3 calls
- **ConfigurationExtractor**: Multi-language config discovery 
- **GenericPythonExtractor**: Python filesystem/network operations
- **AdvancedAnsibleExtractor**: AST-based deep extraction

### Test Coverage Status
- 208 total tests across all modules
- 95% test coverage on core modules
- Contract tests: 27/28 passing (96.4%)







## Key Implementation Details

**When creating new extractors:**
- Inherit from `InfrastructureExtractor` or `ConfigurationExtractor`
- Implement `extract()` method returning Dict with DAYLIGHT dimensions
- Write RED phase tests first in `tests/red_phase/`
- Use `pathlib.Path` for file operations

**Critical patterns to follow:**
- Configuration extraction uses regex patterns in `ENV_PATTERNS` dict
- Sensitive data detection checks against `SENSITIVE_PATTERNS` list
- Coverage calculation follows 3-tier model (element/completeness/usefulness)
- All extractors must pass contract tests in `test_extractor_contract.py`