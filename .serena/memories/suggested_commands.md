# Suggested Commands for DDD Framework Development

## Environment Setup
```bash
# CRITICAL: Use UV package manager, NOT pip
uv venv                           # Create virtual environment
source .venv/bin/activate         # Activate venv (Linux/Mac)
uv pip install -e .              # Install package in editable mode
uv pip install -e ".[dev]"       # Install with dev dependencies
```

## Running the DDD Tool
```bash
# Main CLI commands
ddd measure ./path/to/project              # Measure documentation coverage
ddd assert-coverage ./path/to/project      # Assert coverage meets threshold (85% default)
ddd demo ./path/to/project                 # Run RED-GREEN-REFACTOR demo
ddd measure-artifacts ./path/to/project    # Measure artifact coverage
ddd config-coverage ./path/to/project      # Measure configuration coverage

# With options
ddd measure ./project --verbose             # Verbose output
ddd assert-coverage ./project --min-coverage 90  # Custom threshold
```

## Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_coverage.py -v

# Run with coverage report
pytest --cov=src --cov-report=html --cov-report=term

# Run specific test
pytest tests/test_baseline_ansible.py::test_ansible_coverage -v

# Quick test run without coverage
pytest -x --no-cov
```

## Code Quality
```bash
# Format code (MUST run before committing)
black src/ tests/ --line-length 100

# Lint code
ruff check src/ tests/

# Fix linting issues automatically
ruff check src/ tests/ --fix

# Type checking (if using type hints)
mypy src/ --ignore-missing-imports
```

## Git Operations
```bash
# Check current branch
git branch

# Create feature branch
git checkout -b feature/your-feature-name

# Stage changes
git add -p  # Interactive staging

# Commit with conventional message
git commit -m "feat: add new extractor for Go projects"
git commit -m "fix: handle missing package.json gracefully"
git commit -m "docs: update DAYLIGHT dimension descriptions"

# Check status
git status --short

# View diff
git diff --staged
```

## Development Workflow
```bash
# 1. Start development
source .venv/bin/activate
git checkout -b feature/new-feature

# 2. Make changes and test locally
ddd measure ./demo-project
pytest tests/ -x

# 3. Format and lint
black src/ tests/ --line-length 100
ruff check src/ tests/

# 4. Run full test suite
pytest --cov=src --cov-report=term

# 5. Commit changes
git add -p
git commit -m "feat: description"
```

## System Utilities (Linux)
```bash
# Navigate directories
cd src/ddd/extractors
ls -la

# Search for patterns
grep -r "DependencyExtractor" src/
find . -name "*.py" -type f

# View file content
cat src/cli.py
less README.md

# Monitor processes
ps aux | grep python
htop  # If available

# File operations
cp file.py file_backup.py
mv old_name.py new_name.py
rm -i unnecessary_file.py  # -i for interactive confirmation
```

## Project-Specific Utilities
```bash
# Analyze baseline Ansible project
ddd measure baseline/ansible/

# Test against example projects
ddd measure examples/javascript-project/

# Generate coverage report for inspection
pytest --cov=src --cov-report=html
open htmlcov/index.html  # Mac
xdg-open htmlcov/index.html  # Linux
```