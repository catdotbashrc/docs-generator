# Test-Driven Development Workflow for DDD Extractors

## Overview

The DDD framework practices what it preaches - using Test-Driven Development (TDD) to build Documentation-Driven Development. This document details our rigorous TDD workflow for creating and maintaining extractors.

## Core TDD Philosophy

### The Three Laws of TDD
1. **You may not write production code until you have written a failing test**
2. **You may not write more of a test than is sufficient to fail**
3. **You may not write more production code than is sufficient to pass**

### Applied to DDD
We apply these laws to documentation extraction:
- **RED**: Write tests that define what "complete documentation" looks like
- **GREEN**: Implement extractors until tests pass
- **REFACTOR**: Improve code quality while maintaining test coverage

## Test Structure

### Directory Organization
```
tests/
├── config_extractors/           # Configuration extraction tests
│   ├── red_phase/              # Failing tests (specifications)
│   │   ├── test_config_extraction_contract.py
│   │   ├── test_coverage_requirements.py
│   │   └── test_sensitive_data_detection.py
│   ├── green_phase/            # Passing tests (implementations)
│   │   ├── test_python_extractor.py
│   │   └── test_javascript_extractor.py
│   └── refactor_phase/         # Quality improvements
│       └── test_performance_optimization.py
├── red_phase/                  # Core framework RED tests
│   ├── test_core_extraction.py
│   ├── test_error_patterns.py
│   └── test_permission_extraction.py
├── green_phase/                # Core framework GREEN tests
│   └── test_sphinx_generator.py
└── test_*.py                   # Integration and system tests
```

### Test Categories

#### 1. Contract Tests (RED Phase)
Define the interface and behavior contracts:

```python
# tests/config_extractors/red_phase/test_config_extraction_contract.py

class TestConfigExtractionContract:
    """Define what configuration extraction MUST do"""
    
    def test_extractor_must_implement_extract_method(self):
        """Verify extract() method exists"""
        extractor = ConfigurationExtractor()
        assert hasattr(extractor, 'extract_configs')
        
    def test_must_return_config_artifacts(self):
        """Verify correct return type"""
        extractor = ConfigurationExtractor()
        result = extractor.extract_configs(Path("sample"))
        assert isinstance(result, list)
        assert all(isinstance(c, ConfigArtifact) for c in result)
        
    def test_must_identify_sensitive_data(self):
        """Verify security detection works"""
        content = 'API_KEY = "secret"'
        configs = extract_from_content(content)
        assert configs[0].is_sensitive == True
```

#### 2. Implementation Tests (GREEN Phase)
Verify specific functionality:

```python
# tests/config_extractors/green_phase/test_python_extractor.py

class TestPythonExtractor:
    """Test Python-specific extraction patterns"""
    
    def test_extract_os_environ_get(self):
        """Extract os.environ.get() patterns"""
        content = 'api_key = os.environ.get("API_KEY")'
        configs = extract_python_configs(content)
        
        assert len(configs) == 1
        assert configs[0].name == "API_KEY"
        assert configs[0].category == "env_var"
        
    def test_extract_django_settings(self):
        """Extract Django-style settings"""
        content = '''
        DEBUG = True
        SECRET_KEY = "django-secret"
        ALLOWED_HOSTS = ["localhost"]
        '''
        configs = extract_python_configs(content)
        
        assert len(configs) == 3
        assert "DEBUG" in [c.name for c in configs]
        assert all(c.category == "constant" for c in configs)
```

#### 3. Integration Tests
Test complete workflows:

```python
# tests/test_extractors.py

class TestExtractorIntegration:
    """Test complete extraction pipeline"""
    
    def test_full_project_extraction(self):
        """Test extraction from real project structure"""
        project = create_test_project()
        
        # Extract all documentation
        extractor = ConfigurationExtractor()
        configs = extractor.extract_configs(project.path)
        
        # Verify comprehensive extraction
        assert len(configs) > 0
        assert any(c.is_sensitive for c in configs)
        assert any(c.is_documented for c in configs)
        
        # Calculate coverage
        calculator = ConfigCoverageCalculator()
        coverage = calculator.calculate_coverage(configs)
        
        assert coverage.overall_coverage >= 0.0
        assert coverage.documented_count >= 0
```

## TDD Workflow Implementation

### Phase 1: RED - Write Failing Tests

#### Step 1: Define Requirements
```python
def test_must_extract_environment_variables():
    """Requirement: Must discover all environment variables"""
    # This test SHOULD FAIL initially
    code = 'database_url = os.environ["DATABASE_URL"]'
    result = extract_configs(code)
    assert "DATABASE_URL" in [c.name for c in result]  # FAILS
```

#### Step 2: Run and Verify Failure
```bash
$ uv run pytest tests/red_phase/test_new_feature.py
# ===== 1 failed =====
# AssertionError: assert "DATABASE_URL" in []
```

#### Step 3: Document Why It Should Pass
```python
def test_must_extract_environment_variables():
    """
    Requirement: Must discover all environment variables
    
    Why this matters:
    - Operations needs to know what env vars to set
    - Missing env vars cause deployment failures
    - Security requires tracking sensitive configs
    
    Expected behavior:
    - Parse os.environ access patterns
    - Extract variable names
    - Mark as environment variable category
    """
```

### Phase 2: GREEN - Make Tests Pass

#### Step 1: Implement Minimal Solution
```python
# src/ddd/config_extractors/__init__.py

def extract_configs(content: str) -> List[ConfigArtifact]:
    """Minimal implementation to pass test"""
    configs = []
    
    # Just enough to make test pass
    if 'os.environ["DATABASE_URL"]' in content:
        configs.append(ConfigArtifact(
            name="DATABASE_URL",
            category="env_var",
            # ... minimal fields
        ))
    
    return configs
```

#### Step 2: Verify Test Passes
```bash
$ uv run pytest tests/red_phase/test_new_feature.py
# ===== 1 passed =====
```

#### Step 3: Add More Test Cases
```python
def test_multiple_environ_patterns():
    """Test various os.environ access patterns"""
    test_cases = [
        ('os.environ["KEY"]', "KEY"),
        ('os.environ.get("KEY")', "KEY"),
        ('os.getenv("KEY")', "KEY"),
        ('os.environ.get("KEY", "default")', "KEY"),
    ]
    
    for code, expected in test_cases:
        result = extract_configs(code)
        assert expected in [c.name for c in result]
```

### Phase 3: REFACTOR - Improve Quality

#### Step 1: Generalize Solution
```python
# src/ddd/config_extractors/__init__.py

ENV_PATTERNS = {
    "python": [
        (r'os\.environ\[[\'"](\w+)[\'"]\]', "env_var"),
        (r'os\.environ\.get\([\'"](\w+)[\'"]', "env_var"),
        (r'os\.getenv\([\'"](\w+)[\'"]', "env_var"),
    ]
}

def extract_configs(content: str) -> List[ConfigArtifact]:
    """Robust pattern-based extraction"""
    configs = []
    
    for pattern, category in ENV_PATTERNS["python"]:
        for match in re.finditer(pattern, content):
            configs.append(ConfigArtifact(
                name=match.group(1),
                category=category,
                line_number=content[:match.start()].count('\n') + 1,
                context=content[max(0, match.start()-50):match.end()+50],
                # ... complete implementation
            ))
    
    return configs
```

#### Step 2: Add Performance Tests
```python
# tests/refactor_phase/test_performance.py

def test_extraction_performance():
    """Ensure extraction remains performant"""
    large_file = generate_large_python_file(lines=10000)
    
    start = time.time()
    configs = extract_configs(large_file)
    duration = time.time() - start
    
    assert duration < 1.0  # Must process in under 1 second
    assert len(configs) > 0  # Must find configurations
```

#### Step 3: Verify All Tests Still Pass
```bash
$ uv run pytest tests/
# ===== 156 passed =====
```

## Test Fixtures and Helpers

### Base Test Class
```python
# tests/config_extractors/base.py

class BaseExtractorTest:
    """Base class for extractor tests"""
    
    @pytest.fixture
    def sample_project(self, tmp_path):
        """Create a sample project structure"""
        project = tmp_path / "sample_project"
        project.mkdir()
        
        # Create Python files
        (project / "config.py").write_text('''
            DEBUG = True
            API_KEY = os.environ.get("API_KEY")
        ''')
        
        # Create .env file
        (project / ".env").write_text('''
            DATABASE_URL=postgresql://localhost/db
            SECRET_KEY=super-secret
        ''')
        
        return project
    
    def assert_config_valid(self, config: ConfigArtifact):
        """Validate configuration artifact"""
        assert config.name
        assert config.category in ["env_var", "constant", "config_param"]
        assert config.source_file
        assert config.line_number > 0
```

### Test Data Generators
```python
# tests/helpers.py

def create_python_config_file(configs: List[str]) -> str:
    """Generate Python file with configurations"""
    lines = []
    for config in configs:
        if config.startswith("ENV_"):
            lines.append(f'{config} = os.environ.get("{config}")')
        else:
            lines.append(f'{config} = "value"')
    return '\n'.join(lines)

def create_javascript_config_file(configs: List[str]) -> str:
    """Generate JavaScript file with configurations"""
    lines = []
    for config in configs:
        if config.startswith("REACT_APP_"):
            lines.append(f'const {config} = process.env.{config};')
        else:
            lines.append(f'const {config} = "value";')
    return '\n'.join(lines)
```

## Coverage Requirements

### Test Coverage Metrics
```bash
$ uv run pytest --cov=src --cov-report=term-missing

Name                                  Stmts   Miss  Cover   Missing
---------------------------------------------------------------------
src/ddd/__init__.py                      12      0   100%
src/ddd/config_extractors/__init__.py   234     18    92%   145-162
src/ddd/coverage/__init__.py            156      8    95%   234-241
src/ddd/extractors/ansible_advanced.py  432     26    94%   567-592
---------------------------------------------------------------------
TOTAL                                   2341    124    95%
```

### Coverage Thresholds
- **Minimum Overall**: 85%
- **Critical Modules**: 95%
- **New Code**: 100%

### Enforcing Coverage
```python
# pyproject.toml

[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*", "*/test_*.py"]

[tool.coverage.report]
fail_under = 85
show_missing = true
skip_covered = false

[tool.coverage.html]
directory = "htmlcov"
```

## Continuous Integration

### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml

repos:
  - repo: local
    hooks:
      - id: tests
        name: Run tests
        entry: uv run pytest
        language: system
        pass_filenames: false
        always_run: true
        
      - id: coverage
        name: Check coverage
        entry: uv run pytest --cov=src --cov-fail-under=85
        language: system
        pass_filenames: false
        always_run: true
```

### CI/CD Pipeline
```yaml
# .github/workflows/test.yml

name: Test Suite

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install uv
        uv pip install -e ".[dev]"
    
    - name: Run RED phase tests
      run: uv run pytest tests/red_phase -v
    
    - name: Run GREEN phase tests
      run: uv run pytest tests/green_phase -v
    
    - name: Run all tests with coverage
      run: |
        uv run pytest --cov=src --cov-report=xml
        
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

## Best Practices

### 1. Test Naming Conventions
```python
# Good test names
def test_extract_os_environ_with_default_value():
def test_sensitive_data_marked_correctly():
def test_coverage_fails_below_threshold():

# Bad test names
def test_1():
def test_config():
def test_it_works():
```

### 2. Assertion Messages
```python
# Good: Provides context on failure
assert config.is_sensitive, \
    f"Config '{config.name}' should be marked sensitive"

# Bad: No context
assert config.is_sensitive
```

### 3. Test Independence
```python
# Good: Each test is independent
def test_extract_single_config(tmp_path):
    project = create_test_project(tmp_path)
    # ... test logic

# Bad: Tests depend on shared state
class TestExtractor:
    project = None  # Shared state - BAD!
```

### 4. Test Documentation
```python
def test_complex_extraction_scenario():
    """
    Test extraction from multi-language project.
    
    Scenario:
    - Project has Python, JavaScript, and YAML configs
    - Some configs are sensitive (passwords, keys)
    - Some configs are documented in README
    
    Expected:
    - All configs extracted regardless of language
    - Sensitive configs marked appropriately
    - Documentation status correctly identified
    """
```

## Debugging Failed Tests

### Verbose Output
```bash
# Show detailed test output
$ uv run pytest -vv tests/failing_test.py

# Show print statements
$ uv run pytest -s tests/failing_test.py

# Show local variables on failure
$ uv run pytest -l tests/failing_test.py
```

### Using pytest.set_trace()
```python
def test_complex_extraction():
    result = extract_configs(content)
    
    import pytest; pytest.set_trace()  # Debugger breakpoint
    
    assert len(result) == expected_count
```

### Test Isolation
```bash
# Run single test
$ uv run pytest tests/test_file.py::TestClass::test_method

# Run tests matching pattern
$ uv run pytest -k "config_extraction"

# Run only failed tests
$ uv run pytest --lf
```

## Conclusion

Our TDD workflow ensures that every feature in the DDD framework is:
1. **Specified** through failing tests (RED)
2. **Implemented** to pass tests (GREEN)
3. **Optimized** while maintaining coverage (REFACTOR)

This rigorous approach guarantees that our documentation extraction is reliable, maintainable, and truly serves the needs of maintenance teams.

## Related Documentation

- [Configuration Extraction Module](./CONFIG_EXTRACTION_MODULE.md)
- [API Reference](./API_REFERENCE_EXTRACTORS.md)
- [ATDD Workflow Guide](./ATDD_WORKFLOW_GUIDE.md)
- [User Guide](./USER_GUIDE.md)