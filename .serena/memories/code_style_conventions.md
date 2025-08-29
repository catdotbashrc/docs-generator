# Code Style and Conventions

## Python Standards
- **Python Version**: 3.11+ required
- **Line Length**: 100 characters maximum
- **Formatting**: Black with line-length 100
- **Linting**: Ruff with E, F, W, C90, I, N rules
- **Type Hints**: Use where beneficial for clarity
- **Docstrings**: Follow Google style for classes/functions

## Project Structure
```
src/
├── ddd/
│   ├── coverage/        # Coverage measurement logic
│   ├── extractors/      # Documentation extractors (plugin architecture)
│   ├── specs/          # Documentation specifications
│   ├── artifact_extractors/  # Artifact extraction
│   └── config_extractors/    # Configuration extraction
├── cli.py              # CLI entry point (Click framework)
tests/                  # pytest test files
```

## Design Patterns
1. **Plugin Architecture**: Extractors are pluggable - add new language support via new extractor classes
2. **Specification Pattern**: DimensionSpec defines what "complete" documentation looks like
3. **Coverage Calculation**: Three-tiered measurement mimics code coverage tools
4. **CLI Integration**: Rich terminal output with Click framework

## Implementation Guidelines
- Use `pathlib.Path` for file operations (not os.path)
- Include error handling for malformed configuration files
- Return consistent Dict structure from extractors
- Use Rich console for formatted output (tables, panels, colors)
- Exit code 1 on coverage failure for CI/CD integration

## Naming Conventions
- Classes: PascalCase (e.g., `DependencyExtractor`)
- Functions: snake_case (e.g., `measure_coverage`)
- Constants: UPPER_SNAKE_CASE (e.g., `DEFAULT_THRESHOLD`)
- Files: snake_case (e.g., `test_coverage.py`)

## Testing Conventions
- Test files: `test_*.py` in tests/ directory
- Fixtures: Use pytest fixtures for reusable test data
- Coverage: Aim for >80% code coverage
- Test naming: `test_<what>_<condition>_<expected>`