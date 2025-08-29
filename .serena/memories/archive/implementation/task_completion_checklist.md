# Task Completion Checklist

## When Implementing New Features

### 1. Follow TDD Workflow
- [ ] Write failing test first (RED phase)
- [ ] Implement minimal code to pass test (GREEN phase)
- [ ] Refactor while keeping tests green (REFACTOR phase)

### 2. Run Quality Checks
```bash
# Run all tests
uv run pytest

# Format code
uv run black src/ tests/

# Check linting
uv run ruff src/ tests/
```

### 3. Validate Implementation
```bash
# Test on example project
ddd measure examples/javascript-project

# Compare against baseline
ddd measure baseline/ansible

# Ensure coverage threshold met
ddd assert-coverage examples/javascript-project --min-coverage 0.30
```

### 4. Update Documentation
- [ ] Update README.md if adding new features
- [ ] Update QUICKSTART.md if changing usage
- [ ] Add docstrings to new functions/classes

### 5. Commit Standards
```bash
# Stage all changes
git add -A

# Commit with conventional format
git commit -m "feat: <description>"  # New feature
git commit -m "fix: <description>"   # Bug fix
git commit -m "docs: <description>"  # Documentation
git commit -m "test: <description>"  # Tests only
git commit -m "refactor: <description>"  # Code improvement
```

## Before Marking Task Complete

### Must Pass
- ✅ All tests passing (`uv run pytest`)
- ✅ Code formatted (`uv run black --check src/ tests/`)
- ✅ No linting errors (`uv run ruff src/ tests/`)
- ✅ Coverage maintained or improved

### Should Have
- 📝 Docstrings for public APIs
- 🧪 Tests for new functionality
- 📊 Coverage >80% for new code

## Common Issues to Check

1. **Import Errors**: Ensure all dependencies in pyproject.toml
2. **Path Issues**: Use Path from pathlib, not string concatenation
3. **Type Hints**: Add for function parameters and returns
4. **Empty Catches**: Avoid bare except, specify exception types
5. **Magic Numbers**: Extract to named constants

## Final Verification
```bash
# Clean install test
uv pip install -e ".[dev]"

# Full test suite
uv run pytest -v

# Manual smoke test
ddd measure /path/to/test/project
```