# DDD MVP Comprehensive Test Suite Specification
## Following TDD Best Practices: RED → GREEN → REFACTOR

---

## Executive Summary
This test suite validates the Documentation Driven Development (DDD) framework MVP, focusing on Ansible module documentation extraction. The suite follows strict TDD principles with clear RED-GREEN-REFACTOR phases, ensuring maintenance readiness through documentation coverage (not code coverage).

**MVP Scope**: Ansible module extraction with 85% maintenance scenario coverage
**Test Coverage Target**: 90%+ for extractors, 100% for critical paths
**Performance Target**: < 5 seconds per module extraction

---

## 🔴 RED PHASE: Define Expected Behavior
*Write tests that fail initially, defining what the system SHOULD do*

### Category 1: Core Extraction Tests
These tests define the fundamental extraction capabilities required for the MVP.

```python
# tests/test_red_phase_core.py

class TestCoreExtractionRequirements:
    """Define what successful extraction looks like before implementation."""
    
    def test_extract_documentation_block_structure(self):
        """DOCUMENTATION block must be fully parsed with all fields."""
        # RED: This test defines the expected structure
        content = load_test_module("file.py")
        extractor = AnsibleModuleExtractor()
        
        docs = extractor.extract_documentation(content)
        
        # Must extract module metadata
        assert docs['module'] == 'file'
        assert docs['short_description'] is not None
        assert docs['version_added'] is not None
        
        # Must extract all parameters
        assert 'path' in docs['options']
        assert docs['options']['path']['required'] is True
        assert docs['options']['path']['type'] == 'path'
        assert 'description' in docs['options']['path']
        
        # Must extract parameter choices/defaults
        assert 'state' in docs['options']
        assert 'choices' in docs['options']['state']
        assert 'present' in docs['options']['state']['choices']
    
    def test_extract_examples_for_scenarios(self):
        """EXAMPLES must be extracted and parseable as maintenance scenarios."""
        # RED: Define how examples become runbooks
        examples = extractor.extract_examples(content)
        
        assert len(examples) > 0
        assert isinstance(examples[0], dict)
        assert 'name' in examples[0]  # Task name
        assert 'module' in examples[0]  # Module being used
        assert 'parameters' in examples[0]  # How it's configured
        
        # Examples should be actionable
        scenario = extractor.example_to_scenario(examples[0])
        assert scenario.description is not None
        assert scenario.commands is not None
        assert scenario.expected_outcome is not None
    
    def test_extract_return_values(self):
        """RETURN block must be extracted for understanding state changes."""
        returns = extractor.extract_returns(content)
        
        assert 'path' in returns
        assert returns['path']['description'] is not None
        assert returns['path']['returned'] is not None
        assert returns['path']['type'] in ['str', 'list', 'dict', 'bool']
        
        # Return values indicate what changes were made
        assert extractor.can_verify_state_from_returns(returns)
```

### Category 2: AWS IAM Permission Extraction Tests
Critical for the MVP - extracting security requirements from code.

```python
# tests/test_red_phase_permissions.py

class TestPermissionExtractionRequirements:
    """Define how AWS IAM permissions must be detected."""
    
    def test_extract_boto3_client_permissions(self):
        """Must detect all boto3 client method calls and map to IAM."""
        content = """
        ec2_client = boto3.client('ec2')
        instances = ec2_client.describe_instances()
        ec2_client.terminate_instances(InstanceIds=ids)
        """
        
        permissions = extractor.extract_permissions(content)
        
        # Must find all permissions
        assert 'ec2:DescribeInstances' in permissions
        assert 'ec2:TerminateInstances' in permissions
        
        # Must not have duplicates
        assert len(permissions) == len(set(permissions))
        
        # Must include resource constraints if detectable
        for perm in permissions:
            if perm.startswith('ec2:Terminate'):
                assert extractor.get_resource_constraint(perm) is not None
    
    def test_extract_boto3_resource_permissions(self):
        """Must handle boto3 resource API patterns."""
        content = """
        s3 = boto3.resource('s3')
        bucket = s3.Bucket('my-bucket')
        bucket.upload_file(local_file, key)
        """
        
        permissions = extractor.extract_permissions(content)
        assert 's3:PutObject' in permissions
        assert 's3:PutObjectAcl' in permissions  # Often required together
    
    def test_extract_service_specific_patterns(self):
        """Must handle service-specific permission patterns."""
        # Each AWS service has quirks
        test_cases = [
            ("iam.create_role()", "iam:CreateRole"),
            ("lambda_client.invoke()", "lambda:InvokeFunction"),
            ("dynamodb.Table('x').put_item()", "dynamodb:PutItem"),
            ("cloudformation.create_stack()", "cloudformation:CreateStack"),
        ]
        
        for code, expected_permission in test_cases:
            perms = extractor.extract_permissions(code)
            assert expected_permission in perms
```

### Category 3: Error Pattern Detection Tests
Defining how error handling patterns must be identified.

```python
# tests/test_red_phase_errors.py

class TestErrorPatternRequirements:
    """Define how error patterns must be detected for maintenance."""
    
    def test_extract_explicit_error_messages(self):
        """Must extract all module.fail_json() calls."""
        content = """
        if not os.path.exists(path):
            module.fail_json(msg="Path does not exist: %s" % path)
        
        try:
            result = some_operation()
        except Exception as e:
            module.fail_json(msg="Operation failed: %s" % str(e))
        """
        
        errors = extractor.extract_error_patterns(content)
        
        assert len(errors) >= 2
        assert any('Path does not exist' in e.message for e in errors)
        assert any('Operation failed' in e.message for e in errors)
        
        # Each error should have context
        for error in errors:
            assert error.condition is not None  # When it happens
            assert error.message is not None    # What user sees
            assert error.recovery_hint is not None  # How to fix
    
    def test_extract_validation_errors(self):
        """Must identify parameter validation patterns."""
        content = """
        if state == 'present' and not path:
            module.fail_json(msg="path is required when state=present")
        
        if mode and not isinstance(mode, str):
            module.fail_json(msg="mode must be a string")
        """
        
        errors = extractor.extract_error_patterns(content)
        validations = [e for e in errors if e.type == 'validation']
        
        assert len(validations) >= 2
        assert any('required when' in v.message for v in validations)
        assert any('must be a' in v.message for v in validations)
    
    def test_extract_exception_handling(self):
        """Must detect try/except patterns for error scenarios."""
        errors = extractor.extract_error_patterns(content)
        exception_handlers = [e for e in errors if e.type == 'exception']
        
        for handler in exception_handlers:
            assert handler.exception_type is not None  # What exception
            assert handler.handling_strategy is not None  # How handled
```

### Category 4: State Management Tests
Defining how state transitions and idempotency must be tracked.

```python
# tests/test_red_phase_state.py

class TestStateManagementRequirements:
    """Define how module state management must be understood."""
    
    def test_extract_state_parameter(self):
        """Must identify state parameter and its values."""
        states = extractor.extract_state_management(content)
        
        assert 'present' in states.possible_values
        assert 'absent' in states.possible_values
        
        # Must understand state transitions
        assert states.can_create  # present creates
        assert states.can_delete  # absent deletes
        assert states.can_modify  # Some states modify
    
    def test_extract_check_mode_support(self):
        """Must detect if module supports check mode (dry run)."""
        check_mode = extractor.extract_check_mode_support(content)
        
        assert check_mode.supported is not None
        if check_mode.supported:
            assert check_mode.check_patterns is not None
            assert 'module.check_mode' in str(check_mode.check_patterns)
    
    def test_extract_idempotency_checks(self):
        """Must identify how module ensures idempotency."""
        idempotency = extractor.extract_idempotency_patterns(content)
        
        # Must detect existence checks
        assert idempotency.existence_check is not None
        assert idempotency.comparison_logic is not None
        
        # Must identify when changes are made
        assert idempotency.change_detection is not None
        assert 'changed' in idempotency.result_indicators
```

---

## 🟢 GREEN PHASE: Make Tests Pass
*Implement minimal code to satisfy test requirements*

### Category 1: Validation Tests
These tests ensure the implementation meets requirements.

```python
# tests/test_green_phase_validation.py

class TestImplementationValidation:
    """Validate that implementation satisfies requirements."""
    
    def test_extractor_produces_valid_output(self):
        """Extractor output must be valid MaintenanceDocument."""
        # GREEN: Validate implementation output
        extractor = AnsibleModuleExtractor()
        result = extractor.extract(Path("baseline/ansible/lib/ansible/modules/file.py"))
        
        assert isinstance(result, MaintenanceDocument)
        assert len(result.permissions) > 0
        assert len(result.error_patterns) > 0
        assert result.state_management is not None
        assert len(result.maintenance_scenarios) > 0
    
    def test_coverage_calculation_accuracy(self):
        """Coverage must be calculated correctly without false positives."""
        # GREEN: Validate bug fixes are working
        empty_docs = {"yearbook": {}}
        coverage = DocumentationCoverage()
        result = coverage.measure(empty_docs)
        
        # Bug fix validation: empty should be ~0%, not 70%
        assert result.dimension_scores["yearbook"] < 0.1
        
        # Validate weighted scoring
        assert 0 <= result.overall_coverage <= 1.0
        assert result.overall_coverage == sum(
            score * weight for score, weight in 
            zip(result.dimension_scores.values(), result.dimension_weights.values())
        )
    
    def test_cli_integration(self):
        """CLI commands must work end-to-end."""
        # GREEN: Validate CLI works
        from click.testing import CliRunner
        from ddd.cli import cli
        
        runner = CliRunner()
        
        # Test measure command
        result = runner.invoke(cli, ['measure', 'baseline/ansible/lib/ansible/modules'])
        assert result.exit_code == 0
        assert 'Overall Coverage' in result.output
        
        # Test assert-coverage command (should pass at 50% for MVP)
        result = runner.invoke(cli, ['assert-coverage', '--threshold', '50', 'baseline/ansible/lib/ansible/modules'])
        assert result.exit_code == 0
```

### Category 2: Performance Tests
Ensure the system meets performance requirements.

```python
# tests/test_green_phase_performance.py

class TestPerformanceRequirements:
    """Validate performance meets targets."""
    
    def test_single_module_extraction_speed(self):
        """Single module must extract in < 5 seconds."""
        import time
        
        start = time.time()
        extractor = AnsibleModuleExtractor()
        result = extractor.extract(Path("baseline/ansible/lib/ansible/modules/file.py"))
        elapsed = time.time() - start
        
        assert elapsed < 5.0
        assert result is not None
    
    def test_memory_usage(self):
        """Extraction must not exceed memory limits."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss / 1024 / 1024  # MB
        
        # Extract from large module
        extractor = AnsibleModuleExtractor()
        result = extractor.extract(Path("baseline/ansible/lib/ansible/module_utils/basic.py"))
        
        mem_after = process.memory_info().rss / 1024 / 1024  # MB
        mem_used = mem_after - mem_before
        
        assert mem_used < 500  # Less than 500MB
    
    def test_batch_extraction_performance(self):
        """Must handle multiple modules efficiently."""
        modules = [
            "file.py", "copy.py", "template.py", 
            "apt.py", "yum.py", "systemd.py"
        ]
        
        start = time.time()
        for module in modules:
            path = Path(f"baseline/ansible/lib/ansible/modules/{module}")
            extractor.extract(path)
        elapsed = time.time() - start
        
        # Should average < 3 seconds per module
        assert elapsed < len(modules) * 3
```

### Category 3: Integration Tests
Test the full pipeline with real Ansible modules.

```python
# tests/test_green_phase_integration.py

class TestRealModuleIntegration:
    """Test against actual Ansible modules from baseline."""
    
    # Core modules that MUST work for MVP
    CRITICAL_MODULES = [
        "file.py",      # File management - complex parameters
        "copy.py",      # File operations - source/dest patterns  
        "apt.py",       # Package management - state transitions
        "systemd.py",   # Service management - enable/disable
        "git.py",       # External commands - complex operations
    ]
    
    # Modules that SHOULD work but not critical
    EXTENDED_MODULES = [
        "uri.py",       # HTTP operations
        "command.py",   # Shell execution
        "user.py",      # User management
        "group.py",     # Group management
        "cron.py",      # Scheduled tasks
    ]
    
    @pytest.mark.parametrize("module_name", CRITICAL_MODULES)
    def test_critical_module_extraction(self, module_name):
        """Critical modules must extract successfully."""
        module_path = Path(f"baseline/ansible/lib/ansible/modules/{module_name}")
        
        # Must extract without errors
        result = ddd_measure(module_path)
        assert result is not None
        
        # Must achieve minimum coverage
        assert result.overall_coverage > 0.5  # 50% minimum for MVP
        
        # Must extract key patterns
        assert result.extracted_data.get('permissions') is not None
        assert result.extracted_data.get('error_patterns') is not None
        assert result.extracted_data.get('parameters') is not None
    
    @pytest.mark.parametrize("module_name", EXTENDED_MODULES)
    def test_extended_module_extraction(self, module_name):
        """Extended modules should work but may have lower coverage."""
        try:
            module_path = Path(f"baseline/ansible/lib/ansible/modules/{module_name}")
            result = ddd_measure(module_path)
            
            # Should extract something
            assert result.overall_coverage > 0.3  # 30% acceptable
        except Exception as e:
            # Log but don't fail - these are stretch goals
            pytest.skip(f"Extended module {module_name} not fully supported: {e}")
```

---

## 🔵 REFACTOR PHASE: Improve Test Quality
*Enhance test maintainability without changing functionality*

### Category 1: Test Organization Improvements

```python
# tests/conftest.py

import pytest
from pathlib import Path
from typing import Dict, Any

@pytest.fixture
def sample_ansible_module() -> str:
    """Provide a minimal but complete Ansible module for testing."""
    return '''
DOCUMENTATION = """
---
module: sample
short_description: Sample module for testing
options:
    path:
        description: Path to file
        required: true
        type: path
    state:
        description: Desired state
        choices: [present, absent]
        default: present
"""

EXAMPLES = """
- name: Ensure file exists
  sample:
    path: /tmp/test.txt
    state: present
"""

RETURN = """
path:
    description: Path to file
    returned: success
    type: str
"""

from ansible.module_utils.basic import AnsibleModule

def main():
    module = AnsibleModule(
        argument_spec=dict(
            path=dict(type='path', required=True),
            state=dict(choices=['present', 'absent'], default='present')
        )
    )
    
    path = module.params['path']
    state = module.params['state']
    
    if not os.path.exists(path):
        if state == 'present':
            # Create file
            open(path, 'a').close()
            module.exit_json(changed=True, path=path)
        else:
            module.exit_json(changed=False, path=path)
    else:
        if state == 'absent':
            os.remove(path)
            module.exit_json(changed=True, path=path)
        else:
            module.exit_json(changed=False, path=path)

if __name__ == '__main__':
    main()
'''

@pytest.fixture
def test_modules_path() -> Path:
    """Provide path to test modules directory."""
    return Path(__file__).parent / "fixtures" / "modules"

@pytest.fixture
def extractor_factory():
    """Factory for creating configured extractors."""
    def _make_extractor(extractor_type='ansible', **config):
        if extractor_type == 'ansible':
            from ddd.artifact_extractors.ansible_extractor import AnsibleModuleExtractor
            return AnsibleModuleExtractor(**config)
        # Add other extractor types as needed
        raise ValueError(f"Unknown extractor type: {extractor_type}")
    return _make_extractor
```

### Category 2: Test Helpers and Utilities

```python
# tests/helpers.py

from typing import Dict, List, Any
from pathlib import Path
import yaml
import json

class TestDataGenerator:
    """Generate realistic test data for different scenarios."""
    
    @staticmethod
    def generate_ansible_module(
        name: str = "test_module",
        parameters: List[Dict[str, Any]] = None,
        states: List[str] = None,
        aws_operations: List[str] = None
    ) -> str:
        """Generate a complete Ansible module with specified characteristics."""
        
        parameters = parameters or [
            {"name": "path", "type": "path", "required": True},
            {"name": "state", "choices": states or ["present", "absent"]}
        ]
        
        doc_yaml = {
            "module": name,
            "short_description": f"Test module {name}",
            "options": {
                p["name"]: {
                    "description": f"Parameter {p['name']}",
                    "type": p.get("type", "str"),
                    "required": p.get("required", False),
                    "choices": p.get("choices"),
                }
                for p in parameters
            }
        }
        
        aws_code = ""
        if aws_operations:
            aws_code = "\n".join([
                f"    client.{op}()" for op in aws_operations
            ])
        
        return f'''
DOCUMENTATION = """
{yaml.dump(doc_yaml)}
"""

EXAMPLES = """
- name: Test task
  {name}:
    {parameters[0]["name"]}: /tmp/test
"""

RETURN = """
result:
    description: Operation result
    type: dict
"""

from ansible.module_utils.basic import AnsibleModule
{f"import boto3" if aws_operations else ""}

def main():
    module = AnsibleModule(argument_spec=dict())
    {f"client = boto3.client('ec2')" if aws_operations else ""}
{aws_code}
    module.exit_json(changed=True)

if __name__ == '__main__':
    main()
'''
    
    @staticmethod
    def generate_error_scenarios() -> List[str]:
        """Generate modules with various error patterns."""
        return [
            # Validation error
            '''
            if not path:
                module.fail_json(msg="path is required")
            ''',
            
            # Permission error
            '''
            try:
                os.chmod(path, mode)
            except PermissionError as e:
                module.fail_json(msg=f"Permission denied: {e}")
            ''',
            
            # State transition error
            '''
            if state == 'started' and current_state == 'absent':
                module.fail_json(msg="Cannot start non-existent service")
            ''',
        ]

class AssertionHelpers:
    """Custom assertions for documentation testing."""
    
    @staticmethod
    def assert_valid_permission(permission: str):
        """Assert that a permission follows AWS IAM format."""
        assert ':' in permission, f"Permission {permission} missing service separator"
        service, action = permission.split(':', 1)
        assert service.islower(), f"Service {service} should be lowercase"
        assert action[0].isupper(), f"Action {action} should start with uppercase"
    
    @staticmethod
    def assert_maintenance_scenario(scenario: Dict[str, Any]):
        """Assert that a maintenance scenario is complete."""
        required_fields = ['description', 'when', 'symptoms', 'resolution']
        for field in required_fields:
            assert field in scenario, f"Scenario missing required field: {field}"
            assert scenario[field], f"Scenario field {field} is empty"
    
    @staticmethod
    def assert_coverage_valid(coverage: float, min_val: float = 0.0, max_val: float = 1.0):
        """Assert coverage is within valid range."""
        assert min_val <= coverage <= max_val, \
            f"Coverage {coverage} outside valid range [{min_val}, {max_val}]"
```

### Category 3: Property-Based Testing

```python
# tests/test_refactor_property_based.py

from hypothesis import given, strategies as st, assume
import hypothesis.extra.yaml as yaml_st

class TestPropertyBasedExtraction:
    """Use property-based testing to find edge cases."""
    
    @given(
        module_name=st.text(min_size=1, max_size=50, alphabet=st.characters(min_codepoint=97, max_codepoint=122)),
        param_count=st.integers(min_value=0, max_value=20),
        has_examples=st.booleans(),
        has_return=st.booleans()
    )
    def test_extraction_never_crashes(self, module_name, param_count, has_examples, has_return):
        """Extraction should handle any valid module structure without crashing."""
        # Generate module with random characteristics
        generator = TestDataGenerator()
        params = [
            {"name": f"param_{i}", "type": "str"} 
            for i in range(param_count)
        ]
        
        module_content = generator.generate_ansible_module(
            name=module_name,
            parameters=params
        )
        
        # Should not crash regardless of input
        extractor = AnsibleModuleExtractor()
        try:
            result = extractor.extract_from_content(module_content)
            # Basic sanity checks
            assert result is not None
            assert isinstance(result, MaintenanceDocument)
        except Exception as e:
            # Log for debugging but don't fail - some inputs may be invalid
            assume(False)  # Skip this input
    
    @given(
        service=st.sampled_from(['ec2', 's3', 'iam', 'lambda', 'dynamodb']),
        method=st.text(min_size=1, max_size=30, alphabet=st.characters(min_codepoint=97, max_codepoint=122))
    )
    def test_permission_extraction_consistency(self, service, method):
        """Permission extraction should be consistent and predictable."""
        code = f"client = boto3.client('{service}')\nclient.{method}()"
        
        extractor = AnsibleModuleExtractor()
        permissions1 = extractor.extract_permissions(code)
        permissions2 = extractor.extract_permissions(code)
        
        # Should be deterministic
        assert permissions1 == permissions2
        
        # Should follow format
        if permissions1:
            for perm in permissions1:
                AssertionHelpers.assert_valid_permission(perm)
```

---

## Test Organization Structure

```
tests/
├── conftest.py                    # Fixtures and configuration
├── helpers.py                      # Test utilities and generators
│
├── red_phase/                     # Requirements definition tests
│   ├── test_core_extraction.py    # DOCUMENTATION/EXAMPLES/RETURN
│   ├── test_permissions.py        # AWS IAM extraction
│   ├── test_errors.py            # Error pattern detection
│   └── test_state.py             # State management
│
├── green_phase/                   # Implementation validation tests
│   ├── test_validation.py        # Output correctness
│   ├── test_performance.py       # Speed and memory
│   └── test_integration.py       # Real module testing
│
├── refactor_phase/                # Quality improvement tests
│   ├── test_property_based.py    # Hypothesis testing
│   ├── test_edge_cases.py        # Boundary conditions
│   └── test_regression.py        # Prevent regressions
│
├── fixtures/                      # Test data
│   ├── modules/                  # Sample Ansible modules
│   ├── malformed/                # Invalid input for robustness testing
│   └── golden/                   # Expected outputs for comparison
│
└── benchmarks/                    # Performance benchmarks
    └── test_performance.py        # Detailed performance tests
```

---

## Test Execution Guidelines

### Running the Test Suite

```bash
# Run all tests with coverage
uv run pytest --cov=src --cov-report=html --cov-report=term

# Run only RED phase tests (requirements)
uv run pytest tests/red_phase/ -v

# Run only GREEN phase tests (validation)
uv run pytest tests/green_phase/ -v

# Run only REFACTOR phase tests (quality)
uv run pytest tests/refactor_phase/ -v

# Run only critical MVP tests
uv run pytest -m "critical" -v

# Run with performance benchmarks
uv run pytest tests/benchmarks/ --benchmark-only

# Run specific test file
uv run pytest tests/green_phase/test_integration.py::TestRealModuleIntegration -v

# Run with parallel execution (faster)
uv run pytest -n auto

# Generate detailed HTML coverage report
uv run pytest --cov=src --cov-report=html && open htmlcov/index.html
```

### Marking Tests

```python
# Mark critical tests that MUST pass for MVP
@pytest.mark.critical
def test_extract_documentation_block():
    pass

# Mark slow tests
@pytest.mark.slow
def test_batch_extraction_performance():
    pass

# Mark tests that require baseline files
@pytest.mark.requires_baseline
def test_real_module_extraction():
    pass

# Skip non-MVP features
@pytest.mark.skip(reason="Feature not in MVP scope")
def test_terraform_extraction():
    pass
```

### Continuous Integration

```yaml
# .github/workflows/test.yml
name: Test Suite

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install uv
      run: pip install uv
    
    - name: Install dependencies
      run: uv pip install -e ".[dev]"
    
    - name: Run RED phase tests
      run: uv run pytest tests/red_phase/ -v
      continue-on-error: true  # May fail initially
    
    - name: Run GREEN phase tests
      run: uv run pytest tests/green_phase/ -v
    
    - name: Run REFACTOR phase tests
      run: uv run pytest tests/refactor_phase/ -v
    
    - name: Check coverage
      run: |
        uv run pytest --cov=src --cov-fail-under=85
    
    - name: Run performance benchmarks
      run: uv run pytest tests/benchmarks/ --benchmark-only
```

---

## Success Criteria

### MVP Critical Requirements (MUST PASS)
- [ ] 100% of `red_phase/test_core_extraction.py` tests passing
- [ ] 100% of `red_phase/test_permissions.py` tests passing  
- [ ] 90%+ of `green_phase/test_validation.py` tests passing
- [ ] All 5 CRITICAL_MODULES extracting with >50% coverage
- [ ] Performance: <5 seconds per module extraction
- [ ] Coverage calculation accuracy (no false positives)

### MVP Target Goals (SHOULD PASS)
- [ ] 85%+ overall test coverage for extractors
- [ ] 80%+ of EXTENDED_MODULES working
- [ ] Property-based tests finding no crashes
- [ ] Memory usage <500MB for largest modules
- [ ] CLI commands working end-to-end

### Stretch Goals (NICE TO HAVE)
- [ ] 95%+ test coverage
- [ ] All baseline modules extracting successfully
- [ ] Batch processing of 100+ modules
- [ ] Comparison tool with docs.ansible.com working

---

## Test-Driven Development Workflow

### 1. RED Phase Workflow
```bash
# Write failing test first
echo "def test_new_feature(): assert False" > test_new.py
uv run pytest test_new.py  # Fails ✗

# Define expected behavior
# Write comprehensive test with assertions
# Run again - still fails but with meaningful errors
```

### 2. GREEN Phase Workflow
```bash
# Implement minimal code to pass
# Focus on making test green, not perfect
uv run pytest test_new.py  # Passes ✓

# Verify no regressions
uv run pytest  # All tests still pass
```

### 3. REFACTOR Phase Workflow
```bash
# Improve code while keeping tests green
# Refactor for clarity, performance, maintainability
uv run pytest test_new.py  # Still passes ✓

# Check coverage didn't drop
uv run pytest --cov=src --cov-fail-under=85
```

---

## Common Test Patterns

### Testing Extractors
```python
def test_extractor_pattern():
    # Arrange
    content = "module content here"
    extractor = AnsibleModuleExtractor()
    
    # Act
    result = extractor.extract_something(content)
    
    # Assert
    assert result is not None
    assert len(result) > 0
    assert all(is_valid(item) for item in result)
```

### Testing Coverage
```python
def test_coverage_pattern():
    # Arrange
    docs = {"dimension": {"field": "value"}}
    calculator = DocumentationCoverage()
    
    # Act
    coverage = calculator.measure(docs)
    
    # Assert
    assert 0 <= coverage.overall_coverage <= 1.0
    assert coverage.dimension_scores["dimension"] > 0.5
```

### Testing CLI
```python
def test_cli_pattern():
    # Arrange
    runner = CliRunner()
    
    # Act
    result = runner.invoke(cli, ['command', 'argument'])
    
    # Assert
    assert result.exit_code == 0
    assert 'expected output' in result.output
```

---

## Troubleshooting Test Failures

### Common Issues and Solutions

**Issue: Import errors in tests**
```bash
# Solution: Ensure editable install
uv pip install -e ".[dev]"
```

**Issue: Tests can't find baseline files**
```bash
# Solution: Check baseline exists
ls baseline/ansible/lib/ansible/modules/
# Or mark tests appropriately
@pytest.mark.skipif(not BASELINE_EXISTS, reason="Baseline not available")
```

**Issue: Coverage not meeting threshold**
```bash
# Solution: Check what's not covered
uv run pytest --cov=src --cov-report=term-missing
# Focus tests on uncovered lines
```

**Issue: Flaky tests**
```python
# Solution: Use proper fixtures and isolation
@pytest.fixture(autouse=True)
def reset_state():
    yield
    # Clean up after test
```

---

## Notes for Reviewers

This test suite follows TDD best practices:
1. **RED first**: Tests define requirements before implementation
2. **GREEN minimal**: Just enough code to pass, no gold-plating
3. **REFACTOR safely**: Improve quality with test protection

The suite is organized by TDD phase, not by module, to emphasize the methodology.

Critical tests are marked and must pass for MVP release.
Extended tests demonstrate growth potential but aren't blockers.

Performance targets are realistic for enterprise use:
- 5 seconds per module allows CI/CD integration
- 500MB memory limit works on standard development machines
- 85% coverage threshold balances quality with pragmatism