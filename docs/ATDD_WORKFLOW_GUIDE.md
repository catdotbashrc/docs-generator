# ATDD Workflow Guide for Infrastructure Documentation Standards

## Overview

This guide documents the implementation of **Acceptance Test-Driven Development (ATDD)** methodology in the Infrastructure Documentation Standards project. ATDD ensures that all features are driven by acceptance criteria defined BEFORE implementation.

## The 9-Phase ATDD Workflow

```
SPECIFY → VALIDATE → GENERATE → FAIL → IMPLEMENT → VERIFY → REFACTOR → DOCUMENT → COMMIT
```

### Phase 1: SPECIFY - Define Requirements
**Before writing ANY code**, clearly specify what you're building:
- Document acceptance criteria in test docstrings
- Use Given-When-Then format for clarity
- Define measurable success criteria

### Phase 2: VALIDATE - Write Test Contracts
Create test files with method signatures but no implementation:
```python
def test_extract_soap_endpoints_for_documentation(self, tmp_path):
    """
    Acceptance: System must identify all SOAP web service endpoints
    for accurate API documentation.
    """
    # Test will be implemented in Phase 3
    pass
```

### Phase 3: GENERATE - Write Complete Tests
Implement the full test logic:
```python
def test_extract_soap_endpoints_for_documentation(self, tmp_path):
    # Arrange - Setup test data
    java_content = '...'
    
    # Act - Run the system under test
    parser = JavaAPIExtractor(str(tmp_path))
    endpoints = parser.extract_soap_endpoints()
    
    # Assert - Verify acceptance criteria
    assert len(endpoints) == 3
```

### Phase 4: FAIL - Verify RED State
Run tests to ensure they fail:
```bash
uv run pytest tests/test_java_parser_acceptance.py -v
# Should see FAILED status - this is good!
```

### Phase 5: IMPLEMENT - Write Minimal Code
Write ONLY enough code to make tests pass:
- No extra features
- No premature optimization
- Focus on passing acceptance criteria

### Phase 6: VERIFY - Check Coverage
Ensure coverage meets thresholds:
```bash
uv run pytest --cov=automation --cov-fail-under=80
```

### Phase 7: REFACTOR - Improve Code Quality
With tests passing, safely refactor:
- Apply SOLID principles
- Remove duplication
- Improve naming and structure
- Tests must stay GREEN

### Phase 8: DOCUMENT - Create Evidence Trail
Generate evidence of ATDD compliance:
```python
python automation/atdd_enforcer.py
# Generates evidence report
```

### Phase 9: COMMIT - Version Control Checkpoint
Create a git commit with meaningful message:
```bash
git add .
git commit -m "feat: Implement Java parser with ATDD methodology

- Added acceptance tests for SOAP endpoint extraction
- Implemented minimal parser to meet acceptance criteria
- Coverage: 85% (exceeds 80% threshold)
- All acceptance tests passing"
```

## Project Structure for ATDD

```
infrastructure-documentation-standards/
├── automation/
│   ├── atdd_enforcer.py      # ATDD enforcement engine
│   └── java_parser.py         # Implementation (Phase 5)
├── tests/
│   └── test_java_parser_acceptance.py  # Acceptance tests (Phase 2-3)
├── .git/hooks/
│   └── pre-commit             # ATDD git hook enforcement
└── pyproject.toml             # ATDD configuration
```

## ATDD Configuration

In `pyproject.toml`:
```toml
[tool.atdd]
enforcement = "strict"
phases_required = ["SPECIFY", "VALIDATE", "GENERATE", "FAIL", 
                  "IMPLEMENT", "VERIFY", "REFACTOR", "DOCUMENT", "COMMIT"]

[tool.atdd.coverage]
line = 80
branch = 70
new_code = 100
never_decrease = true
```

## Enforcement Mechanisms

### 1. Git Pre-commit Hook
Automatically enforces ATDD before commits:
- Checks tests exist for changed files
- Verifies coverage hasn't decreased
- Ensures acceptance criteria are met

### 2. ATDD Enforcer
Python module that blocks violations:
```python
from automation.atdd_enforcer import ATDDEnforcer

enforcer = ATDDEnforcer()
enforcer.before_code_generation(context)  # Blocks if tests don't exist
enforcer.after_implementation(context)    # Checks coverage
```

### 3. CI/CD Integration
Tests run automatically in pipeline:
```yaml
- name: Run ATDD Acceptance Tests
  run: uv run pytest tests/ --cov-fail-under=80
```

## Real Example: Java Parser Implementation

### Step 1: Write Acceptance Test (RED)
```python
def test_extract_soap_endpoints_for_documentation(self, tmp_path):
    """
    Acceptance: System must identify all SOAP web service endpoints
    """
    # Test implementation that defines what we need
```

### Step 2: Run Test - Verify Failure
```bash
$ uv run pytest tests/test_java_parser_acceptance.py
FAILED - TypeError: JavaApiParser.__init__() missing argument
```

### Step 3: Implement Minimal Code (GREEN)
Write just enough code in `java_parser.py` to make test pass

### Step 4: Verify Coverage
```bash
$ uv run pytest --cov=automation
Coverage: 85% ✅
```

## Benefits Realized

1. **Quality First**: 80%+ coverage enforced
2. **Clear Requirements**: Acceptance criteria in tests
3. **Safety Net**: Refactor with confidence
4. **Documentation**: Tests serve as living documentation
5. **No Regression**: Coverage never decreases

## Common ATDD Patterns

### Pattern 1: Acceptance-Driven Features
```python
class TestFeatureAcceptance:
    def test_user_story_acceptance(self):
        """
        Acceptance: As a DevOps engineer
        I want automated documentation extraction
        So that documentation stays current
        """
        # Test implementation
```

### Pattern 2: Edge Case Coverage
```python
def test_handle_malformed_files_gracefully(self):
    """
    Acceptance: System must not crash on invalid input
    """
    # Create invalid input
    # Verify graceful handling
```

### Pattern 3: Performance Criteria
```python
def test_performance_requirements(self):
    """
    Acceptance: Parse 1000 files in under 10 seconds
    """
    # Performance test implementation
```

## Troubleshooting

### Issue: Tests Not Failing Initially
**Solution**: Ensure you're testing behavior, not implementation
```python
# Bad - Testing implementation
assert parser._internal_method() == expected

# Good - Testing behavior/acceptance
assert len(parser.extract_endpoints()) == 3
```

### Issue: Coverage Dropping
**Solution**: Pre-commit hook blocks commits
```bash
❌ COMMIT BLOCKED - Coverage dropping from 85% to 75%
Fix coverage before committing
```

### Issue: Over-Engineering
**Solution**: ATDD enforces minimal implementation
- Write only enough to pass tests
- Add features only when new tests require them

## Best Practices

1. **Write Tests First**: Always start with acceptance tests
2. **One Feature at a Time**: Small, focused cycles
3. **Commit Often**: Create checkpoints at GREEN states
4. **Document Acceptance**: Clear criteria in test docstrings
5. **Maintain Coverage**: Never let it drop below 80%

## Next Steps

1. Apply ATDD to remaining modules:
   - `build.py` (needs 80% coverage)
   - `setup.py` (needs 80% coverage)
   - `nlp_extractor.py` (needs acceptance tests)

2. Integrate with CI/CD:
   - Add GitHub Actions workflow
   - Enforce ATDD in pull requests
   - Generate coverage badges

3. Monitor Metrics:
   - Track test-first compliance
   - Measure defect reduction
   - Monitor cycle time improvements

## Conclusion

ATDD transforms the development process from "code-first" to "acceptance-first", ensuring that every line of code has purpose and is validated by tests. This methodology is particularly powerful for infrastructure documentation systems where accuracy and reliability are critical.

The combination of acceptance tests, enforcement mechanisms, and git hooks creates a system where quality is built-in, not bolted-on. By following this ATDD workflow, the Infrastructure Documentation Standards project maintains high quality while enabling rapid, confident development.