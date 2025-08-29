# DDD Framework - Development Commands

## Installation & Setup
```bash
# Install with development dependencies
uv pip install -e ".[dev]"

# Verify installation
ddd --help
```

## Core DDD Commands
```bash
# Measure documentation coverage for any project
ddd measure /path/to/project

# Save coverage results to JSON
ddd measure /path/to/project -o coverage.json

# Assert minimum coverage (fails if below threshold)
ddd assert-coverage /path/to/project --min-coverage 0.85

# See the RED-GREEN-REFACTOR workflow in action
ddd demo /path/to/project
```

## Testing Commands
```bash
# Run all tests with coverage
uv run pytest

# Run specific test file
uv run pytest tests/test_baseline_ansible.py

# Run with verbose output
uv run pytest -v

# Generate HTML coverage report
uv run pytest --cov=src --cov-report=html
```

## Code Quality Commands
```bash
# Format code with Black
uv run black src/ tests/

# Check formatting without changes
uv run black --check src/ tests/

# Run linting with Ruff
uv run ruff src/ tests/

# Fix auto-fixable issues
uv run ruff --fix src/ tests/
```

## Development Workflow
```bash
# 1. Make changes to code
# 2. Run tests to ensure nothing breaks
uv run pytest

# 3. Format code
uv run black src/ tests/

# 4. Check linting
uv run ruff src/ tests/

# 5. Test on example project
ddd measure examples/javascript-project

# 6. Test on baseline (Ansible)
ddd measure baseline/ansible
```

## Git Commands
```bash
# Check status
git status

# Stage changes
git add -A

# Commit with descriptive message
git commit -m "feat: Add new documentation extractor"

# Push to remote
git push origin main
```

## Project Structure Navigation
```bash
# Key directories
src/ddd/specs/       # Documentation specifications
src/ddd/extractors/  # Language-specific extractors
src/ddd/coverage/    # Coverage measurement engine
tests/               # Test files
baseline/ansible/    # Reference baseline project
examples/            # Example projects for testing
```

## Debugging & Development
```bash
# Run CLI directly for debugging
python src/cli.py measure /path/to/project

# Verbose output for debugging
ddd measure /path/to/project --verbose

# Check Python version (requires 3.11+)
python --version
```