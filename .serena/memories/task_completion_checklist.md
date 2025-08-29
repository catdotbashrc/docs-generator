# Task Completion Checklist

## Before Marking Any Task Complete

### 1. Code Quality Checks
```bash
# Format code (MANDATORY)
black src/ tests/ --line-length 100

# Lint code (MANDATORY)
ruff check src/ tests/

# Fix any linting issues
ruff check src/ tests/ --fix
```

### 2. Testing
```bash
# Run tests to ensure nothing broke (MANDATORY)
pytest

# If you modified code, check coverage
pytest --cov=src --cov-report=term

# For significant changes, run full test suite
pytest --cov=src --cov-report=html --cov-report=term -v
```

### 3. Documentation Updates
- [ ] Update docstrings if function signatures changed
- [ ] Update README.md if adding new features
- [ ] Update CLAUDE.md if development workflow changed
- [ ] Add comments for complex logic (sparingly)

### 4. Manual Testing
```bash
# Test your changes with the CLI
ddd measure ./demo-project
ddd assert-coverage ./demo-project

# If working on extractors, test with different project types
ddd measure ./path/to/test/project
```

### 5. Git Checks
```bash
# Review your changes
git status
git diff

# Stage changes selectively
git add -p

# Ensure commit message follows convention
# feat: for new features
# fix: for bug fixes
# docs: for documentation
# refactor: for code refactoring
# test: for test additions/changes
```

## Task-Specific Checklists

### When Adding New Extractor
1. Create extractor class inheriting from base
2. Implement extract() method
3. Add unit tests in tests/test_extractors.py
4. Test with real projects
5. Update documentation

### When Modifying Coverage Calculation
1. Update coverage logic
2. Run tests/test_coverage.py
3. Verify baseline Ansible still meets 90% target
4. Update specs if needed

### When Changing CLI Commands
1. Update cli.py with Click decorators
2. Test command manually
3. Add/update tests in tests/test_cli.py
4. Update suggested_commands.md memory
5. Update README.md examples

### When Fixing Bugs
1. Add failing test that reproduces the bug
2. Fix the bug
3. Ensure test now passes
4. Run full test suite
5. Document fix in commit message

## Final Verification
```bash
# One final check before considering task complete
black src/ tests/ --line-length 100 && \
ruff check src/ tests/ && \
pytest --no-cov -x

# If all pass, task is complete!
```

## Important Reminders
- **NEVER use pip**, always use `uv pip`
- **Line length** is 100 characters max
- **Exit code 1** on coverage failure is intentional
- **pathlib.Path** for file operations, not os.path
- **Rich console** for terminal output
- **85% coverage** is the default threshold