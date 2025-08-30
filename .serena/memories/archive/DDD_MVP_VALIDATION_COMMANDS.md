# SuperClaude Validation Commands for DDD MVP
Version: 1.0.0
Type: validation_strategy
Created: 2025-08-29
Status: READY
Purpose: Comprehensive validation of existing DDD implementation

## 🔍 Phase 1: Code Quality & Architecture Validation

### Analyze Existing Implementation
```bash
/analyze @src/ddd --focus architecture --ultrathink
```
**Validates**: Abstract design patterns, separation of concerns, extensibility
**Expected**: Clean architecture report, proper abstraction layers confirmed

### Deep Code Quality Assessment
```bash
/analyze @src/ddd/artifact_extractors --focus quality --think-hard
```
**Validates**: Code quality, SOLID principles, maintainability
**Expected**: High maintainability score, no major code smells

### Security & Vulnerability Check
```bash
/analyze @src --focus security --validate
```
**Validates**: No security vulnerabilities, safe file operations, input validation
**Expected**: Clean security report, proper path handling confirmed

## 🧪 Phase 2: Test Coverage & TDD Validation

### Test Suite Analysis
```bash
/test coverage --scope project --validate
```
**Validates**: Test coverage meets TDD standards (>90% for new code)
**Expected**: Coverage report showing 100% for base, 93% for Ansible extractor

### Test Quality Assessment
```bash
/analyze @tests --focus testing --think
```
**Validates**: Test quality, proper TDD cycle, comprehensive scenarios
**Expected**: 48 tests identified, proper RED-GREEN-REFACTOR patterns

### Run Full Test Suite with Validation
```bash
/test all --validate --safe-mode
```
**Validates**: All tests pass, no regressions, proper assertions
**Expected**: 48/48 tests passing (or 46/48 per last session)

## ⚡ Phase 3: Performance & Efficiency Validation

### Performance Benchmarking
```bash
/improve @src/ddd/artifact_extractors --focus performance --think
```
**Validates**: Extraction speed, memory efficiency, scalability
**Expected**: <1s extraction for typical modules, efficient memory usage

### Token Efficiency Analysis
```bash
/analyze @src --uc --focus efficiency
```
**Validates**: Code is optimized, no unnecessary complexity
**Expected**: Clean, efficient implementation patterns

## 🔧 Phase 4: Functional Validation

### CLI Command Testing
```bash
/test cli "ddd measure ./demo-project" --validate
```
**Validates**: CLI works correctly, proper output formatting
**Expected**: Rich console output with coverage metrics

### Coverage Assertion Testing
```bash
/test cli "ddd assert-coverage ./demo-project --threshold 85" --validate
```
**Validates**: Coverage calculation, threshold checking, exit codes
**Expected**: Proper pass/fail based on 85% threshold

### Demo Project Validation
```bash
/troubleshoot @demo-project --think
```
**Validates**: Demo project works as test case, proper structure
**Expected**: Demo project properly demonstrates DDD capabilities

## 📚 Phase 5: Documentation & Maintenance Validation

### Documentation Coverage Check
```bash
/analyze @src --focus documentation --validate
```
**Validates**: Code documentation, docstrings, type hints
**Expected**: Comprehensive docstrings, proper type annotations

### CLAUDE.md Validation
```bash
/explain @CLAUDE.md --validate
```
**Validates**: Development guide is accurate and complete
**Expected**: Clear instructions, accurate command examples

### README Completeness
```bash
/document @README.md --focus completeness --validate
```
**Validates**: User documentation complete, examples work
**Expected**: Clear value proposition, working examples

## 🏗️ Phase 6: Integration & Architecture Validation

### Abstraction Layer Testing
```bash
/analyze "InfrastructureExtractor inheritance" --think-hard
```
**Validates**: Proper abstraction, template method pattern works
**Expected**: Clean inheritance, proper abstract methods

### Ansible Extractor Validation
```bash
/test @src/ddd/artifact_extractors/ansible_extractor.py --comprehensive
```
**Validates**: AWS IAM extraction, YAML parsing, boto3 patterns
**Expected**: Proper permission extraction, DOCUMENTATION block parsing

### Plugin Architecture Validation
```bash
/analyze @src/ddd --focus extensibility --architect
```
**Validates**: New extractors can be added easily
**Expected**: Clear extension points, proper interfaces

## 🚀 Phase 7: End-to-End Validation

### Full Workflow Test
```bash
/workflow "RED-GREEN-REFACTOR demo" --validate
```
**Validates**: Complete DDD cycle works as intended
**Expected**: Proper progression through all phases

### Real Ansible Module Testing
```bash
/test @baseline --pattern "*.py" --validate
```
**Validates**: Works with real Ansible modules
**Expected**: Successful extraction from baseline modules

## 🎯 Phase 8: Continuous Validation

### Regression Testing
```bash
/git diff HEAD~1 --analyze --validate
```
**Validates**: Recent changes don't break existing functionality
**Expected**: No regressions identified

### Memory & Context Validation
```bash
/spawn validate-memories --scope project
```
**Validates**: Project memories accurate, context preserved
**Expected**: All DDD memories valid and current

## 📊 Summary Validation Command

### Complete MVP Validation Suite
```bash
/spawn validate-mvp --comprehensive --report
```
**Runs**: All validation phases with comprehensive reporting
**Output**: Full validation report with pass/fail for each component

## ⚠️ Critical Validation Points

1. **Abstract Base Class**: Must have 100% test coverage
2. **Ansible Extractor**: Must have >90% test coverage
3. **CLI Commands**: Must work with proper exit codes
4. **Coverage Calculation**: Must accurately measure DAYLIGHT dimensions
5. **TDD Compliance**: Every feature must have tests written first

## 🎬 Quick Validation Sequence

For rapid validation, run these in order:
```bash
# 1. Test suite validation
/test all --validate

# 2. Architecture check
/analyze @src --focus architecture --think

# 3. CLI functional test
/test cli "ddd measure ./demo-project"

# 4. Coverage assertion
/test cli "ddd assert-coverage ./demo-project"

# 5. Performance check
/improve @src --focus performance --validate
```

## 📈 Expected Validation Results

### Must Pass
- ✅ 48 tests (46-48 passing acceptable)
- ✅ >90% coverage on new code
- ✅ CLI commands execute successfully
- ✅ Coverage calculation works correctly
- ✅ Abstract patterns properly implemented

### Should Pass
- ✅ Performance <1s for typical modules
- ✅ Clean code quality metrics
- ✅ Comprehensive documentation
- ✅ No security vulnerabilities

### Nice to Have
- ✅ 100% test coverage on all modules
- ✅ Demo project fully functional
- ✅ All edge cases handled

## 🔄 Iterative Improvement

After validation, use:
```bash
/improve @src --loop --iterations 3
```
To iteratively enhance any components that need refinement.