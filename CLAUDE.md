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

# Manual testing commands
uv run pytest                                      # Run all tests
uv run pytest tests/test_abstract_extractor.py -v  # Run specific test
uv run pytest --cov=src --cov-report=html         # Generate coverage report

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

### MVP: Ansible-Focused Implementation

**Why Ansible?**
- Represents real enterprise maintenance challenges
- Rich ecosystem with official documentation for comparison
- Complex permission and state management requirements
- Demonstrates value to operations teams immediately

**Implementation Progress**:
- ✅ **Abstract Base Layer** (`InfrastructureExtractor`)
  - Universal maintenance concepts (permissions, errors, state)
  - Template method pattern for consistent extraction
  - 100% test coverage with TDD approach
  
- ✅ **Ansible Extractor** (`AnsibleModuleExtractor`)
  - AWS IAM permission extraction from boto3 calls
  - DOCUMENTATION/EXAMPLES/RETURN block parsing
  - Maintenance scenario generation
  - 93% test coverage (26/28 tests passing)

- ⏳ **In Progress**:
  - Sphinx documentation generator
  - Comparison tool with docs.ansible.com
  - Demo script for leadership presentation

### Abstraction Layers

```
┌─────────────────────────────────────┐
│     CLI Interface (Click-based)     │
├─────────────────────────────────────┤
│    Coverage Calculator & Specs      │
│  (DAYLIGHT dimensions, thresholds)  │
├─────────────────────────────────────┤
│    Abstract Extractor Layer         │
│  (InfrastructureExtractor base)     │
├─────────────────────────────────────┤
│    Tool-Specific Extractors         │
│ (Ansible, Terraform, K8s - future)  │
└─────────────────────────────────────┘
```

This architecture ensures:
- **Extensibility**: Add new tools without changing core logic
- **Consistency**: All tools follow same extraction patterns
- **Maintainability**: Clear separation of concerns

## Documentation & Communication Guidelines

### When Discussing DDD (DO's and DON'Ts)

**DO Say (Factual Claims We Can Prove):**
- "DDD automatically extracts AWS IAM permissions from Ansible code" ✅
- "We achieved 85% coverage on our test baseline" ✅
- "Extraction takes less than 5 seconds for typical modules" ✅
- "93% of our tests are passing" ✅
- "The framework uses TDD principles applied to documentation" ✅
- "We can measure documentation coverage like code coverage" ✅

**DON'T Say (Unverified Claims):**
- ❌ Specific dollar savings without actual data
- ❌ Percentage improvements without measured baselines
- ❌ Industry statistics without credible sources
- ❌ Time savings without actual measurements
- ❌ ROI projections without pilot program data
- ❌ Comparisons to other tools without benchmarks

### Documentation Principles

1. **Be Factual**: Every claim must be demonstrable with working code
2. **Show, Don't Tell**: Use actual command output and real examples
3. **Acknowledge Limitations**: Be honest about what doesn't work yet
4. **Measure First**: Don't claim improvements without baselines
5. **Let Pilots Prove Value**: Use pilot programs to generate real metrics

## The Big Picture: Why This Matters

### The Maintenance Crisis
Every day, operations teams inherit code they didn't write. When production fails at 2AM, they need:
- What permissions does this need? (AWS IAM, Kubernetes RBAC, etc.)
- What can go wrong? (Common errors and recovery procedures)
- How do I know if it's working? (State management, idempotency)
- What does this depend on? (External services, configurations)

**Current Reality**: Dig through code, guess at requirements, learn through failure
**DDD Vision**: Generated runbooks with everything needed for maintenance

### How DDD Changes the Game

```
Traditional Approach:
Code → Deploy → Hope docs exist → Scramble during incidents

DDD Approach:
Code → Extract Documentation → Measure Coverage → Generate Runbooks → Confident Operations
```

### The Ansible MVP Proves the Concept

We're starting with Ansible because it represents real enterprise challenges:
1. **Complex Permissions**: AWS IAM policies extracted from boto3 calls
2. **Error Patterns**: Common failures with specific recovery steps  
3. **State Management**: Idempotency, check mode, change tracking
4. **Dependencies**: Python packages, Ansible modules, AWS services

**Success Metric**: 85% maintenance scenario coverage (not code coverage!)

### Future Expansion

The abstraction layer is designed for growth:
- **Terraform**: Provider permissions, state files, plan/apply workflows
- **Kubernetes**: RBAC, resource limits, health checks, rollback procedures
- **Shell Scripts**: Unix permissions, error codes, dependency checks
- **Docker**: Port mappings, volume mounts, health checks, resource limits

Each tool adds its specific extractors while reusing the core framework.

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