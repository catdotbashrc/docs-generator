# Code Style and Conventions

## Python Version
- Python 3.11+ required
- Type hints encouraged but not enforced

## Code Formatting
- **Black**: Line length 100, auto-formatting enforced
- **Ruff**: Linting with rules E, F, W, C90, I, N
- Ignore E501 (line too long) since Black handles this

## Project Structure Conventions
```python
# Module organization
src/
  ddd/
    specs/      # Specifications define requirements
    extractors/ # Extract documentation from codebases  
    coverage/   # Measure coverage against specs
    
# Each module has clear separation of concerns
```

## Naming Conventions
- **Classes**: PascalCase (e.g., `DocumentationCoverage`, `DependencyExtractor`)
- **Functions/Methods**: snake_case (e.g., `measure_coverage`, `extract_dependencies`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `DAYLIGHT_DIMENSIONS`)
- **Private methods**: Leading underscore (e.g., `_calculate_element_coverage`)

## Code Patterns

### Dataclass Usage
```python
@dataclass
class CoverageResult:
    """Use dataclasses for data structures"""
    passed: bool
    overall_score: float
    dimension_scores: Dict[str, float]
```

### Dict Type Hints
```python
def extract(self, project_path: str) -> Dict[str, Any]:
    """Always type hint Dict returns"""
```

### Error Handling
```python
# Graceful degradation with logging
try:
    data = extract_something()
except FileNotFoundError:
    # Return empty structure, not None
    return {}
```

## Documentation Strings
- All public functions/classes have docstrings
- Format: Brief description, no need for full Google/NumPy style
- Focus on clarity over verbosity

## Testing Conventions
- Test files: `test_*.py` in tests/ directory
- Test functions: `test_<specific_behavior>`
- Use pytest fixtures for setup
- Aim for descriptive test names over comments

## Import Organization
1. Standard library imports
2. Third-party imports
3. Local imports
(Separated by blank lines)

## TDD Discipline
- Write tests first (RED phase)
- Implement minimal code to pass (GREEN phase)
- Refactor for quality (REFACTOR phase)
- Never modify tests to make code pass
- Tests verify behavior, not implementation