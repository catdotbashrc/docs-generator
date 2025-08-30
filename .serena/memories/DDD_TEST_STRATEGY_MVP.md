# DDD MVP Test Strategy - Actionable Plan

## Phase 1: Core Extraction Tests (Week 1)
**Goal**: Validate basic documentation extraction works

### Must-Have Tests
```python
def test_parse_documentation_block():
    """Extract DOCUMENTATION from real Ansible module."""
    content = read_file("baseline/ansible/lib/ansible/modules/file.py")
    docs = extractor.extract_documentation(content)
    assert docs['module'] == 'file'
    assert 'path' in docs['options']
    assert docs['options']['path']['required'] is True

def test_parse_examples_block():
    """Extract EXAMPLES for scenario generation."""
    # EXAMPLES become our maintenance runbooks
    examples = extractor.extract_examples(content)
    assert len(examples) > 0
    assert 'ansible.builtin.file' in examples[0]

def test_parse_return_block():
    """Extract RETURN for understanding state changes."""
    returns = extractor.extract_returns(content)
    assert 'path' in returns
    assert returns['path']['returned'] == 'success'
```

### Edge Cases to Test
- Missing DOCUMENTATION block (some internal modules)
- Malformed YAML (happens in older modules)
- Unicode in documentation (international contributions)
- Extremely long descriptions (>1000 lines)

## Phase 2: Pattern Recognition Tests (Week 2)
**Goal**: Extract maintenance-critical patterns

### Dependency Extraction
```python
def test_extract_module_dependencies():
    """Identify what the module needs to run."""
    deps = extractor.extract_dependencies(content)
    assert 'ansible.module_utils.basic' in deps
    # This tells us the module needs Ansible core

def test_extract_python_requirements():
    """Find Python version and library requirements."""
    # Look for version checks and conditional imports
    reqs = extractor.extract_requirements(content)
    assert reqs['python_version'] >= '3.6'
```

### State Management Extraction
```python
def test_extract_state_patterns():
    """Identify how module manages state transitions."""
    states = extractor.extract_states(content)
    assert 'absent' in states  # Can delete
    assert 'present' in states  # Can create
    # Each state = potential maintenance scenario
```

## Phase 3: Bug Fixes and Accuracy (Week 3)
**Goal**: Fix identified bugs, improve accuracy

### Fix Coverage Calculation Bugs
```python
def test_empty_dimension_scores_zero():
    """Empty dimensions must score 0%, not 70%."""
    empty_docs = {"yearbook": {}}
    result = coverage.measure(empty_docs)
    assert result.dimension_scores["yearbook"] < 0.1  # Not 0.7!

def test_language_aware_scoring():
    """Python projects shouldn't need node_version."""
    python_docs = {
        "dependencies": {
            "runtime_dependencies": ["ansible", "jinja2"],
            "python_version": ">=3.6",
            # No node_version - that's OK for Python!
        }
    }
    result = coverage.measure(python_docs)
    assert result.dimension_scores["dependencies"] > 0.8
```

## Phase 4: Integration Tests (Week 4)
**Goal**: Validate full pipeline with real modules

### Real Module Validation Suite
```python
TEST_MODULES = [
    "file.py",      # Complex parameters, multiple states
    "apt.py",       # Package management patterns
    "systemd.py",   # Service management
    "git.py",       # External command execution
    "uri.py",       # Network operations
]

def test_real_module_extraction():
    """Test against actual Ansible modules."""
    for module_name in TEST_MODULES:
        module_path = f"baseline/ansible/lib/ansible/modules/{module_name}"
        result = ddd.measure(module_path)
        
        # Should extract meaningful documentation
        assert result.overall_coverage > 0.5
        
        # Should identify key patterns
        assert result.extracted_data.get('parameters')
        assert result.extracted_data.get('error_patterns')
        assert result.extracted_data.get('states')
```

## Performance Benchmarks

### Target Metrics
- **Single Module**: < 5 seconds extraction time
- **100 Modules**: < 5 minutes total
- **Memory Usage**: < 500MB for largest modules
- **Accuracy**: 95% for parameter extraction

### Performance Test
```python
def test_extraction_performance():
    """Ensure extraction is fast enough for CI/CD."""
    import time
    start = time.time()
    
    # Extract from large module (basic.py is 3000+ lines)
    result = extractor.extract("baseline/ansible/lib/ansible/module_utils/basic.py")
    
    elapsed = time.time() - start
    assert elapsed < 5.0  # Must be under 5 seconds
    assert result is not None  # Must produce output
```

## Test Data Sources

### Primary Test Files
1. `/lib/ansible/modules/file.py` - Gold standard for parameters
2. `/lib/ansible/modules/apt.py` - Package management patterns  
3. `/lib/ansible/module_utils/basic.py` - Core utilities
4. `/lib/ansible/module_utils/errors.py` - Error patterns

### Pattern Libraries to Build
```python
ANSIBLE_PATTERNS = {
    'imports': [
        'from ansible.module_utils.basic import AnsibleModule',
        'from ansible.module_utils._text import to_text',
    ],
    'error_calls': [
        'module.fail_json(msg=',
        'raise AnsibleValidationError(',
    ],
    'state_checks': [
        "if state == 'present'",
        "if module.check_mode:",
    ]
}
```

## Success Criteria

1. **Coverage**: 90%+ code coverage on extractors
2. **Accuracy**: Zero false positives on parameter requirements
3. **Robustness**: Handle malformed code gracefully
4. **Performance**: Meet all benchmark targets
5. **Real-World**: Successfully extract from 5+ production modules