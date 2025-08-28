# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## TEST-DRIVEN DEVELOPMENT (TDD) - CRITICAL PRINCIPLES

### TDD CORE RULES - NEVER VIOLATE

1. **RED-GREEN-REFACTOR**: Write failing test FIRST → Make it pass with minimal code → Refactor
   - ❌ NEVER modify tests to pass (e.g., adding sys.exit(0) just to pass)
   - ✅ ALWAYS fix the code to satisfy legitimate tests

2. **TEST STRINGENCY**: "DO NOT require the test to be less stringent! Unless it's literally impossible to pass the test, do not make the test less stringent. We make code pass the test, we don't adjust the test so the code passes."

3. **VERIFY FUNCTIONALITY**: Tests must verify actual behavior, not just exit codes
   - ✅ Check outputs, side effects, log files, data transformations
   - ❌ Don't just check return codes without verifying functionality

4. **FAIL APPROPRIATELY**: When things go wrong, fail with clear errors
   - ✅ raise ValueError("Specific error description")
   - ✅ sys.exit(1) with stderr message
   - ❌ sys.exit(0) to hide failures

5. **COVERAGE REQUIREMENTS**:
   - Minimum: 80% overall coverage
   - Critical paths: 95% coverage  
   - New features: 100% test coverage BEFORE merge

## Project Overview

Infrastructure Documentation Standards - An automated documentation system that solves the "Where is the config for X?" problem by generating comprehensive documentation from live infrastructure sources (Azure, SQL, Java APIs).

**Core Achievement**: Successfully implemented Java API documentation extraction that discovered and documented 7 SOAP endpoints in a production Spring Boot project, proving the system works.

## Commands

### Essential Development Commands

```bash
# Installation
uv pip install -e ".[dev]"       # Development install with all dependencies

# Documentation Operations
uv run docs-build                 # Build HTML documentation (uses sphinx -M mode with parallel processing)
uv run docs-build --format pdf    # Build PDF documentation
uv run docs-build --clean         # Clean and rebuild
uv run docs-serve                 # Development server with hot-reload
uv run docs-clean                 # Clean build artifacts

# Automation Commands (Implemented)
uv run java-docs --project-path /path/to/java/project --output docs/
                                  # Extract Java API documentation from source code

# Automation Commands (Planned)
uv run azure-docs                 # Generate Azure resource documentation
uv run sql-docs                   # Extract SQL database schemas
uv run deploy-itglue              # Deploy to IT Glue knowledge base
```

### Testing Single Components

```bash
# Test Java parser on specific project
python automation/java_parser.py /path/to/java/project -v

# Test Sphinx build with verbose output
python automation/build.py --verbose --clean

# Generate documentation for Java project example
uv run java-docs /path/to/java/project --output docs/source/examples/
```

## Architecture & Key Concepts

### High-Level Architecture

The system follows a **Discovery → Template → Generation** pipeline:

```
Infrastructure Source → Parser/Extractor → Template Engine → Sphinx Build → Multi-Format Output
         ↓                      ↓                 ↓               ↓              ↓
   (Azure/SQL/Java)     (automation/*.py)   (Jinja2+RST)    (build.py)    (HTML/PDF/ITGlue)
```

### Core Components

1. **Automation Scripts** (`automation/`)
   - `build.py`: Sphinx build system using official `-M` make-mode pattern with parallel processing
   - `java_parser.py`: Extracts SOAP/REST endpoints from Java source using regex patterns
   - Future: `azure.py`, `sql.py`, `deploy.py` for additional automation

2. **Template System** (`docs/source/_templates/`)
   - Jinja2-based RST templates for consistent documentation structure
   - Templates handle 80% automation, 20% manual customization
   - Current templates: `java-api-service.rst`, `azure-infrastructure.rst`, `sql-database-guide.rst`, `transition-checklist.rst`

3. **Custom Directives** (Future: `docs/source/_extensions/`)
   ```rst
   .. azure-inventory::          # Will query Azure resources
   .. sql-schema::               # Will extract database schemas  
   .. adf-pipeline-docs::        # Will document Data Factory
   ```

### Java API Parser Implementation

The `java_parser.py` module extracts API information through pattern matching:
- WebService and WebMethod annotations for SOAP endpoints
- Method signatures with parameters and return types
- Data models from model/domain packages
- Service and repository layers
- Configuration from application.properties

Key extraction patterns used:
- SOAP endpoint: `@WebMethod` with `operationName`
- Service detection: `@Service` or classes ending in `Service`
- Repository detection: `@Repository` or files ending in `Repository.java`

### Build System Architecture

The `build.py` follows Context7-recommended Sphinx patterns:
- Uses `sphinx -M` make-mode for consistent builds
- Enables parallel processing with `-j auto`
- Proper error handling and logging
- Clean build support with `--clean` flag

## Implementation Status

### ✅ Completed
- Java API documentation extraction (`java_parser.py`)
- Sphinx build system with Context7 patterns (`build.py`)
- Template foundation (4 templates ready)
- Production proof-of-concept (7 endpoints documented)

### 🔄 In Progress
- Azure resource discovery integration
- SQL schema extraction module
- IT Glue deployment automation

### 📋 Planned
- Custom Sphinx directives for auto-generation
- GCP integration
- REST/GraphQL API support
- CI/CD pipeline integration

## Integration Example

A complete working example demonstrates the system capabilities:
- Spring Boot SOAP web service with 7 endpoints
- Successfully extracted all endpoints with parameters and return types
- Generated comprehensive documentation with troubleshooting guides
- Proven pattern-based extraction approach

## Project-Specific Patterns

### Template Variable Structure

When creating new templates, use these standard variables:
```python
template_vars = {
    'client_name': str,           # Client identifier
    'service_name': str,          # Service/component name
    'environment': str,           # dev/staging/prod
    'base_url': str,              # Service endpoint
    'endpoints': List[Dict],      # API endpoints
    'data_models': List[Dict],    # Data structures
    'last_updated': str,          # ISO date
    'generation_date': str        # ISO date
}
```

### Error Handling Pattern

All automation scripts follow this pattern:
```python
try:
    # Operation
    result = perform_operation()
    logger.info(f"✅ Success: {result}")
except SpecificException as e:
    logger.error(f"❌ Failed: {e}")
    # Graceful fallback or manual input prompt
```

### Discovery Pattern

All parsers follow: Find → Parse → Extract → Transform → Generate:
1. Find relevant files using glob patterns
2. Parse content with regex/AST
3. Extract structured information
4. Transform to documentation format
5. Generate using Jinja2 templates