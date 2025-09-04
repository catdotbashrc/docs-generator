# DDD Framework: Technical Discoveries & Patterns
Version: 1.0.0
Type: technical_learnings
Created: 2025-08-29
Status: ACTIVE

## Discovered Patterns

### 🎯 AST Architecture Decision (PIVOTAL)

**The Revelation**: Abstract Syntax Trees are THE standard for parsing code - not regex.
- **Python**: `ast` module for proper code structure parsing
- **Future**: Each language gets its AST (JS→Babel, Java→JavaParser, etc.)
- **Impact**: 50 lines complex regex → 30 lines clean AST, zero edge cases
- **Rule**: Use AST for code structure, regex only for simple strings

### Testing Architecture Insights

**Two-Tier Testing Strategy**
- **Critical Tests**: Core abstractions that MUST work (blocks commits)
- **Full Suite**: Comprehensive testing (warnings only)
- **Implementation**: Pre-commit hooks with different severity levels
- **Benefit**: Development velocity without sacrificing quality

**Current Test Distribution**
- Abstract extractor tests: 20 (all passing)
- Ansible extractor tests: 28 (26 passing)
- Coverage tests: 11 (8 passing)
- CLI tests: 12 (mostly passing)
- Total: 115 tests, 89.6% pass rate

### Documentation Extraction Capabilities

**What DDD Actually Extracts** (Verified):
1. **AWS IAM Permissions**: From boto3 client calls
   - Pattern: `client.method()` → `service:Method` permission
   - Example: `ec2.describe_instances()` → `ec2:DescribeInstances`

2. **Error Patterns**: From exception handling
   - Finds try/except blocks
   - Extracts error codes and recovery procedures

3. **State Management**: From code analysis
   - Idempotency detection
   - Check mode support
   - Rollback capabilities

4. **Dependencies**: From imports and configs
   - Python imports → package requirements
   - Configuration files → version constraints

### Coverage Calculation Formula

```python
# Three-tier coverage measurement
element_coverage = 0.3      # Does it exist?
completeness_coverage = 0.4  # Required fields present?
usefulness_coverage = 0.3    # 2AM test - actually useful?

# DAYLIGHT dimension weights
dependencies: 0.15
automation: 0.15
yearbook: 0.05
lifecycle: 0.15
integration: 0.10
governance: 0.10
health: 0.15
testing: 0.15
# Total: 1.0
```

### Task Automation Insights

**Invoke vs Make**
- Invoke: Python-native, better error handling, cross-platform
- Make: Unix-specific, less Python integration
- Decision: Invoke for Python projects

**Pre-commit Hook Strategy**
```yaml
# Order matters!
1. Auto-formatting (always fix)
2. Linting (fix what's possible)
3. Security checks (block on issues)
4. Critical tests (block on failure)
5. Full tests (warn only)
```

### Documentation Principles (Critical)

**Factual Claims Only**
- Every statistic must be measurable
- Every benefit must be demonstrable
- Every comparison needs benchmarks
- Pilot programs generate real metrics

**What We Can Actually Claim**:
- Extraction works (demonstrable)
- Coverage measurable (show metrics)
- Performance <5 seconds (timed)
- 85% coverage achievable (proven on baseline)

### Package Management Insights

**UV Package Manager Benefits**
- Faster than pip (10x on large installs)
- Proper dev dependency management
- Lock file generation
- Consistent environment setup

**Proper Dependency Addition**
```bash
# Wrong
uv pip install package

# Right
uv add package          # For dependencies
uv add package --dev    # For dev dependencies
```

### Sphinx Documentation Setup

**Auto-generation Configuration**
```python
# Key extensions for full automation
extensions = [
    'sphinx.ext.autodoc',      # From docstrings
    'sphinx.ext.napoleon',     # Google/NumPy style
    'sphinx.ext.viewcode',     # Source links
    'myst_parser',            # Markdown support
    'sphinx_autodoc2',        # Better extraction
]
```

### Performance Observations

**Current Performance Metrics**
- Test suite: 0.82s for 115 tests
- CLI startup: <1s
- Extraction: <5s for typical module
- Documentation generation: Not yet measured

### Architecture Strengths

**Plugin Architecture Success**
- Abstract base class pattern works well
- Template method for consistent extraction
- Easy to add new extractors
- Clean separation of concerns

**DAYLIGHT Dimensions**
- Good coverage of maintenance needs
- Weights allow customization
- Missing elements clearly identified
- Actionable recommendations generated

## Technical Debt Identified

1. **Code Formatting**: 17 files need black formatting
2. **Linting Issues**: 842 issues (777 auto-fixable)
3. **Test Failures**: 12 tests failing (edge cases)
4. **Coverage**: Overall 72% (target 80%)

## Optimization Opportunities

1. **Parallel Extraction**: Could process multiple files simultaneously
2. **Caching**: Repeated extractions could be cached
3. **Incremental Updates**: Only re-extract changed files
4. **Performance Profiling**: Haven't measured bottlenecks yet

## Reusable Patterns

### Error Handling Pattern
```python
try:
    result = extractor.extract(path)
except ExtractionError as e:
    # Log but continue
    logger.warning(f"Failed to extract {path}: {e}")
    continue
```

### Coverage Assertion Pattern
```python
def assert_coverage(data, threshold=0.85):
    result = measure(data)
    if result.overall_coverage < threshold:
        raise AssertionError(
            f"Coverage {result.overall_coverage:.1%} "
            f"below {threshold:.1%}"
        )
```

### Task Definition Pattern
```python
@task
def command(c, flag=False):
    """Docstring becomes help text."""
    print(f"{Colors.YELLOW}Status...{Colors.NC}")
    c.run("actual command")
    print(f"{Colors.GREEN}✅ Done{Colors.NC}")
```

## Next Technical Challenges

1. **Sphinx Integration**: Generate runbooks from MaintenanceDocument
2. **Comparison Tool**: Scrape and compare with official docs
3. **Performance**: Ensure scales to large codebases
4. **Accuracy**: Validate extraction against manual documentation