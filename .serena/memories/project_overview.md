# DDD Framework - Documentation Driven Development

## Purpose
Documentation Driven Development (DDD) Framework - A parallel to Test-Driven Development (TDD) for documentation. Just as TDD ensures code quality through tests, DDD ensures documentation quality through coverage metrics. It applies the RED-GREEN-REFACTOR cycle to documentation, treating documentation specs like tests and documentation coverage like code coverage.

## Core Philosophy
- **RED**: Define documentation requirements (what complete documentation looks like)Runtime/build dependencies, versions, package managers-
- **GREEN**: Extract documentation from codebase until specs pass (85% threshold)
- **REFACTOR**: Improve documentation quality while maintaining coverage

## Tech Stack

### Language & Runtime
- **Python 3.11+**: Core language requirement
- **Bash**: Automating various tasks
- **UV**: Package manager (not pip)

### Core Dependencies
- **PyYAML >= 6.0**: Configuration and spec files
- **Click >= 8.0**: CLI framework
- **Rich >= 13.0**: Terminal formatting and output
- **Jinja2 >= 3.0**: Template engine for reports
- **Sphinx**: For documentation generation and parsing
- **SpaCy**: Natural lagnauge processing for semantic analysis

### Development Dependencies
- **pytest >= 7.0**: Testing framework
- **pytest-cov >= 4.0**: Code coverage for tests
- **Black >= 23.0**: Code formatting (line length 100)
- **Ruff >= 0.1.0**: Linting and code quality

### Project Management
- **Git**: Version control with worktrees for isolated development
- **Configuration**: pyproject.toml (not setup.cfg)

## DAYLIGHT Dimensions
Documentation is measured across 8 dimensions:
- **D**ependencies: Runtime/build dependencies, versions, package managers
- **A**utomation: Scripts, CI/CD, build processes
- **Y**earbook: History, evolution, architectural decisions
- **L**ifecycle: Environments, deployment, configuration settings
- **I**ntegration: External services and APIs
- **G**overnance: Standards, audit trails, and compliance
- **H**ealth: Monitoring, performance, observability
- **T**esting: Test structure, strategies, and coverage

## Architecture
- **Specs**: Define what complete documentation looks like for each dimension
- **Extractors**: Parse codebases to extract existing documentation
- **Dataclasses**: For data structures (CoverageResult, DimensionSpec)
- **Type Hints**: Encouraged for function signatures
- **Modular Design**: Clear separation between specs, extractors, and coverage
- **Plugin Architecture**: Easy to add new language extractors

## Coverage Metrics
- **Completeness**: Can maintainers prevent and fix all critical issues?
- **Accuracy**: Do recovery procedures actually work?
- **Usability**: Can on-call fix production at 2AM?
- **Patterns**: Does it document patterns actually used in codebase?
- **Parameter Coverage**: Does it capture parameters and annotate their:
  1. sources
  2. type
  2. order
  3. optional/mandatory
- **Idempotency**: Same/equivalent code → same/equivalent docs

## Key Principle

***Documentation coverage isn't about what percentage of code we scanned - it's about what percentage of maintenance needs we met.***

## Session Discoveries

- Traditional metrics measure the wrong things
- Maintenance documentation ≠ API documentation
- Preventive work (60%) is as important as emergency response (40%)
- Some critical information requires human input
- Framework is sound, implementation needs pragmatism

## Current Status

### Minimum Viable Product
- Need to determine what it is
- Does NOT need to be comprehensive
- Needs to demonstrate value of project idea to senior company leaders
- Show them why this is worth investing time into as an internal project

### Other
- Dependencies extractor supports JavaScript/Python
- CLI with measure/assert/demo commands
- Other DAYLIGHT dimensions have specs but simplified extractors
