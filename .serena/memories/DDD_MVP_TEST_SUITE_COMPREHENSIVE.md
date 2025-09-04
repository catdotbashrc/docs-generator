# DDD MVP Comprehensive Test Suite - TDD Implementation Guide

## Overview
Created comprehensive test suite specification following strict TDD principles (RED→GREEN→REFACTOR) for the DDD MVP focused on Ansible module documentation extraction.

## Key Design Principles

### RED Phase (Requirements Definition)
- **Core Extraction Tests**: DOCUMENTATION, EXAMPLES, RETURN block parsing
- **AWS IAM Permission Tests**: boto3 call detection and IAM mapping
- **Error Pattern Tests**: fail_json calls, exceptions, validation errors
- **State Management Tests**: State transitions, idempotency, check mode

### GREEN Phase (Implementation Validation)
- **Validation Tests**: Ensure extractors produce valid MaintenanceDocuments
- **Performance Tests**: <5 seconds per module, <500MB memory
- **Integration Tests**: Real Ansible modules from baseline (file.py, apt.py, systemd.py)
- **Coverage Accuracy**: No false positives (empty dimensions = 0%, not 70%)

### REFACTOR Phase (Quality Improvements)
- **Test Organization**: Fixtures, helpers, generators for maintainability
- **Property-Based Testing**: Hypothesis framework for edge cases
- **Custom Assertions**: Domain-specific validation helpers

## Test Structure
```
tests/
├── red_phase/          # Requirements tests (define behavior)
├── green_phase/        # Validation tests (verify implementation)
├── refactor_phase/     # Quality tests (improve maintainability)
├── fixtures/           # Test data and samples
└── benchmarks/         # Performance testing
```

## Success Criteria

### MVP Critical (MUST PASS)
- 100% RED phase core extraction tests
- 100% AWS IAM permission extraction tests
- 90%+ GREEN phase validation tests
- 5 critical modules >50% coverage
- <5 seconds extraction time

### MVP Target (SHOULD PASS)
- 85%+ extractor code coverage
- 80%+ extended modules working
- No crashes in property tests
- <500MB memory usage
- CLI end-to-end working

## Execution Commands
```bash
# Full suite with coverage
uv run pytest --cov=src --cov-report=html

# Phase-specific testing
uv run pytest tests/red_phase/ -v      # Requirements
uv run pytest tests/green_phase/ -v    # Implementation
uv run pytest tests/refactor_phase/ -v # Quality

# Critical tests only
uv run pytest -m "critical" -v

# Performance benchmarks
uv run pytest tests/benchmarks/ --benchmark-only
```

## File Location
`tests/MVP_TEST_SUITE_SPECIFICATION.md` - Complete 400+ line specification with code examples

## Integration Points
- Aligns with existing test structure (130/150 passing)
- Addresses identified bugs (false positive coverage)
- Focuses on MVP scope (Ansible extraction)
- Provides clear path for extensibility