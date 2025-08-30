# DDD MVP Configuration Strategy
Version: 1.0.0
Type: configuration
Created: 2025-08-29
Purpose: Lean configuration focused on leadership demo success

## Core Philosophy
"Demonstrate value first, engineer perfection later"

## Essential Configuration

### Environment Variables (Minimal)
```bash
# .env.example
DDD_PROJECT_ROOT=/path/to/test/project
DDD_BASELINE_PATH=./baseline/ansible
DDD_OUTPUT_DIR=./docs/generated
DDD_COVERAGE_THRESHOLD=85
DDD_VERBOSE=false
```

### Enhanced pyproject.toml
```toml
[project]
name = "ddd-framework"
version = "0.1.0"
description = "Documentation Driven Development - TDD for documentation coverage"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "pyyaml>=6.0",
    "click>=8.0",
    "rich>=13.0",
    "jinja2>=3.0",
    "sphinx>=7.0",           # For doc generation
    "sphinx-autodoc2>=0.5",  # Better API docs
    "myst-parser>=2.0",      # Markdown support
    "python-dotenv>=1.0",    # .env file support
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "black>=23.0",
    "ruff>=0.1.0",
    "pre-commit>=3.0",
    "sphinx-autobuild>=2021.0",  # Live doc preview
]

[project.scripts]
ddd = "cli:main"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
addopts = "-v --cov=src --cov-report=html --cov-report=term"
# MVP: Fail if coverage drops below 80%
required_test_coverage = 80

[tool.coverage.run]
branch = true
source = ["src"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
]
fail_under = 80  # MVP target

[tool.black]
line-length = 100
target-version = ["py311"]

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "W", "I"]  # Keep it simple for MVP
ignore = ["E501"]  # Line length (black handles)

[tool.sphinx]
# Auto-generate API docs from docstrings
autodoc_default_options = {
    "members": true,
    "undoc-members": true,
    "show-inheritance": true,
    "special-members": "__init__",
}
```

### Pre-commit Hooks (Minimal Friction)
```yaml
# .pre-commit-config.yaml
repos:
  # Auto-format (no friction, just fix it)
  - repo: https://github.com/psf/black
    rev: 23.12.0
    hooks:
      - id: black
        args: [--line-length=100]

  # Catch real problems only
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff
        args: [--fix]  # Auto-fix what we can

  # Security/safety only
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: check-yaml
      - id: detect-private-key
      - id: check-merge-conflict
      
  # MVP: Ensure tests pass before commit
  - repo: local
    hooks:
      - id: pytest-check
        name: pytest-check
        entry: uv run pytest -q --tb=short
        language: system
        types: [python]
        pass_filenames: false
        stages: [commit]
```

## Documentation Strategy (Auto-Generate Everything!)

### 1. API Documentation
```python
# docs/conf.py
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',  # Google/NumPy docstrings
    'sphinx.ext.viewcode',  # Source links
    'sphinx.ext.intersphinx',  # Link to Python docs
    'sphinx_autodoc_typehints',  # Type hints in docs
    'myst_parser',  # Markdown support
]

# Auto-generate from source
autodoc_mock_imports = []  # MVP: Don't mock anything
```

### 2. Maintenance Runbooks (Core DDD Value)
```python
# src/ddd/generators/sphinx_generator.py
class SphinxRunbookGenerator:
    """Auto-generates maintenance runbooks from extracted docs"""
    
    def generate(self, maintenance_doc: MaintenanceDocument):
        # Creates beautiful Sphinx docs showing:
        # - Required permissions (with examples)
        # - Common errors (with solutions)
        # - State management (idempotency info)
        # - Dependencies (with versions)
        # - Troubleshooting scenarios
```

### 3. Coverage Reports (Visual Impact)
```python
# Auto-generate coverage badges and reports
# Show leadership the "85% Documentation Coverage" badge
# Visual proof of maintenance readiness
```

## Demo Preparation Checklist

### Before Leadership Demo
```bash
# 1. Clean up code
black src/ tests/
ruff check --fix src/ tests/

# 2. Ensure high test coverage
uv run pytest --cov=src
# Should show 80-90%

# 3. Generate beautiful docs
cd docs && make html
# Shows auto-generated API docs

# 4. Prepare demo project
uv run ddd measure ./baseline/ansible
# Shows current coverage

# 5. Generate runbooks
uv run ddd generate-docs ./baseline/ansible
# Creates professional maintenance docs
```

## Leadership Talking Points

1. **"We're applying TDD principles to documentation"**
   - Show 85% test coverage → 85% doc coverage parallel

2. **"Auto-generated runbooks from code"**
   - Demo Sphinx-generated maintenance guides
   - "2AM-ready documentation"

3. **"Measurable documentation quality"**
   - Show coverage metrics
   - Compare to current (probably 0%) state

4. **"ROI: 50% reduction in handoff time"**
   - Quantify maintenance scenarios covered
   - Show time saved in incident response

## What to Skip for MVP Demo

❌ CI/CD setup (add after approval)
❌ Multi-Python version testing
❌ Performance benchmarking
❌ Complex pre-commit hooks
❌ Poetry/tox migration
❌ PyPI packaging

## Success Metrics for Demo

✅ 85% documentation coverage on baseline
✅ Auto-generated runbooks in <5 seconds
✅ Beautiful Sphinx documentation
✅ Clear before/after comparison
✅ Working CLI with rich output