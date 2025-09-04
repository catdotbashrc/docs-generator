"""
Centralized pytest fixtures and configuration for DDD test suite.
Following TDD best practices with RED-GREEN-REFACTOR phases.
"""

import json
import tempfile
import textwrap
from pathlib import Path
from typing import Any, Dict, List
from unittest.mock import MagicMock

import pytest
import yaml
from click.testing import CliRunner

from ddd import DocumentationCoverage
from ddd.artifact_extractors import ArtifactCoverageCalculator
from ddd.artifact_extractors.ansible_extractor import AnsibleModuleExtractor
from ddd.config_extractors import ConfigCoverageCalculator
from ddd.extractors import DependencyExtractor
from ddd.specs import DAYLIGHTSpec, DimensionSpec


# ===========================
# Test Configuration
# ===========================

@pytest.fixture(scope="session")
def test_data_dir() -> Path:
    """Path to test data directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture(scope="session")
def baseline_ansible_path() -> Path:
    """Path to Ansible baseline modules for integration testing."""
    baseline = Path("baseline/ansible/lib/ansible/modules")
    if baseline.exists():
        return baseline
    # Skip tests if baseline not available
    pytest.skip("Ansible baseline not available")


# ===========================
# CLI Testing Fixtures
# ===========================

@pytest.fixture
def runner() -> CliRunner:
    """Create a Click CLI test runner."""
    return CliRunner()


@pytest.fixture
def temp_project(tmp_path) -> Path:
    """Create a temporary project directory with basic structure."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    
    # Create basic project files
    (project_dir / "package.json").write_text(json.dumps({
        "name": "test-project",
        "version": "1.0.0",
        "dependencies": {
            "express": "^4.18.0"
        }
    }, indent=2))
    
    (project_dir / "pyproject.toml").write_text(textwrap.dedent("""
        [project]
        name = "test-project"
        version = "0.1.0"
        dependencies = [
            "pytest>=7.0",
            "click>=8.0"
        ]
    """))
    
    (project_dir / "README.md").write_text("# Test Project\nA sample project for testing.")
    
    return project_dir


# ===========================
# Coverage Testing Fixtures
# ===========================

@pytest.fixture
def coverage_calculator() -> DocumentationCoverage:
    """Create a DocumentationCoverage instance."""
    return DocumentationCoverage()


@pytest.fixture
def daylight_spec() -> DAYLIGHTSpec:
    """Create a DAYLIGHT spec instance."""
    return DAYLIGHTSpec()


@pytest.fixture
def sample_extracted_docs() -> Dict[str, Any]:
    """Sample extracted documentation data with good coverage."""
    return {
        "dependencies": {
            "runtime_dependencies": {
                "pytest": {
                    "name": "pytest",
                    "version": ">=7.0",
                    "purpose": "Testing framework",
                    "failure_impact": "Tests cannot run",
                    "recovery_procedure": "Install with: pip install pytest>=7.0"
                },
                "click": {
                    "name": "click",
                    "version": ">=8.0",
                    "purpose": "CLI framework",
                    "failure_impact": "CLI commands unavailable",
                }
            },
            "python_version": ">=3.11",
            "package_manager": "pip",
            "lock_file": "requirements.txt",
        },
        "automation": {
            "ci_cd_pipelines": ["GitHub Actions"],
            "deployment_scripts": ["deploy.sh"],
            "purpose": "Automated testing and deployment",
            "failure_handling": "Rollback on test failure"
        },
        "yearbook": {
            "team_members": ["John Doe", "Jane Smith"],
            "changelog": "Version 1.0.0 - Initial release"
        }
    }


@pytest.fixture
def empty_extracted_docs() -> Dict[str, Any]:
    """Empty extracted documentation for testing zero coverage."""
    return {
        "dependencies": {},
        "automation": {},
        "yearbook": {},
        "lifecycle": {},
        "integration": {},
        "governance": {},
        "health": {},
        "testing": {}
    }


# ===========================
# Extractor Testing Fixtures
# ===========================

@pytest.fixture
def dependency_extractor() -> DependencyExtractor:
    """Create a DependencyExtractor instance."""
    return DependencyExtractor()


@pytest.fixture
def ansible_extractor() -> AnsibleModuleExtractor:
    """Create an AnsibleModuleExtractor instance."""
    return AnsibleModuleExtractor()


@pytest.fixture
def artifact_calculator() -> ArtifactCoverageCalculator:
    """Create an ArtifactCoverageCalculator instance."""
    return ArtifactCoverageCalculator()


@pytest.fixture
def config_calculator() -> ConfigCoverageCalculator:
    """Create a ConfigCoverageCalculator instance."""
    return ConfigCoverageCalculator()


# ===========================
# Ansible Module Fixtures
# ===========================

@pytest.fixture
def sample_ansible_module() -> str:
    """Provide a minimal but complete Ansible module for testing."""
    return textwrap.dedent('''
        DOCUMENTATION = """
        ---
        module: sample
        short_description: Sample module for testing
        version_added: "2.9"
        description:
            - This is a sample module for testing extraction
        options:
            path:
                description: Path to file
                required: true
                type: path
            state:
                description: Desired state
                choices: [present, absent]
                default: present
                type: str
            mode:
                description: File permissions
                required: false
                type: str
        author:
            - Test Author (@testauthor)
        """
        
        EXAMPLES = """
        - name: Ensure file exists
          sample:
            path: /tmp/test.txt
            state: present
            
        - name: Remove file
          sample:
            path: /tmp/test.txt
            state: absent
        """
        
        RETURN = """
        path:
            description: Path to the managed file
            returned: success
            type: str
            sample: /tmp/test.txt
        changed:
            description: Whether the file was changed
            returned: always
            type: bool
            sample: true
        """
        
        from ansible.module_utils.basic import AnsibleModule
        import os
        import boto3
        
        def main():
            module = AnsibleModule(
                argument_spec=dict(
                    path=dict(type='path', required=True),
                    state=dict(choices=['present', 'absent'], default='present'),
                    mode=dict(type='str', required=False)
                ),
                supports_check_mode=True
            )
            
            path = module.params['path']
            state = module.params['state']
            mode = module.params.get('mode')
            
            # Check mode support
            if module.check_mode:
                module.exit_json(changed=True, path=path)
            
            # AWS operations for testing permission extraction
            ec2 = boto3.client('ec2')
            instances = ec2.describe_instances()
            
            # State management
            if not os.path.exists(path):
                if state == 'present':
                    # Create file
                    try:
                        open(path, 'a').close()
                        module.exit_json(changed=True, path=path)
                    except IOError as e:
                        module.fail_json(msg=f"Failed to create file: {e}")
                else:
                    module.exit_json(changed=False, path=path)
            else:
                if state == 'absent':
                    try:
                        os.remove(path)
                        module.exit_json(changed=True, path=path)
                    except Exception as e:
                        module.fail_json(msg=f"Failed to remove file: {e}")
                else:
                    module.exit_json(changed=False, path=path)
        
        if __name__ == '__main__':
            main()
    ''')


@pytest.fixture
def sample_ansible_module_with_errors() -> str:
    """Ansible module with various error patterns for testing."""
    return textwrap.dedent('''
        from ansible.module_utils.basic import AnsibleModule
        
        def main():
            module = AnsibleModule(argument_spec=dict())
            
            # Validation errors
            if not path:
                module.fail_json(msg="path is required when state=present")
            
            if mode and not isinstance(mode, str):
                module.fail_json(msg="mode must be a string")
            
            # Exception handling
            try:
                result = risky_operation()
            except PermissionError as e:
                module.fail_json(msg=f"Permission denied: {e}")
            except Exception as e:
                module.fail_json(msg=f"Operation failed: {e}")
            
            # Retry patterns
            for attempt in range(3):
                try:
                    connect()
                    break
                except ConnectionError:
                    if attempt == 2:
                        module.fail_json(msg="Failed after 3 retries")
                    time.sleep(1)
    ''')


# ===========================
# Test Data Generators
# ===========================

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
        
        # Build DOCUMENTATION section
        doc_yaml = {
            "module": name,
            "short_description": f"Test module {name}",
            "options": {}
        }
        
        for param in parameters:
            doc_yaml["options"][param["name"]] = {
                "description": f"Parameter {param['name']}",
                "type": param.get("type", "str"),
                "required": param.get("required", False),
                "choices": param.get("choices"),
            }
        
        # Build module code
        aws_code = ""
        if aws_operations:
            aws_imports = "import boto3\n"
            aws_client = "    ec2 = boto3.client('ec2')\n"
            aws_calls = "\n".join([
                f"    ec2.{op}()" for op in aws_operations
            ])
            aws_code = aws_imports + "\ndef main():\n" + aws_client + aws_calls
        
        return textwrap.dedent(f'''
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
            {aws_code if aws_operations else ""}
            
            def main():
                module = AnsibleModule(argument_spec=dict())
                {'    ' + aws_code if aws_operations else ''}
                module.exit_json(changed=True)
            
            if __name__ == '__main__':
                main()
        ''')
    
    @staticmethod
    def generate_package_json(
        name: str = "test-project",
        dependencies: Dict[str, str] = None
    ) -> str:
        """Generate a package.json file."""
        deps = dependencies or {
            "express": "^4.18.0",
            "lodash": "^4.17.21"
        }
        return json.dumps({
            "name": name,
            "version": "1.0.0",
            "dependencies": deps
        }, indent=2)
    
    @staticmethod
    def generate_pyproject_toml(
        name: str = "test-project",
        dependencies: List[str] = None
    ) -> str:
        """Generate a pyproject.toml file."""
        deps = dependencies or [
            "pytest>=7.0",
            "click>=8.0"
        ]
        return textwrap.dedent(f'''
            [project]
            name = "{name}"
            version = "0.1.0"
            dependencies = {json.dumps(deps)}
        ''')


@pytest.fixture
def test_data_generator() -> TestDataGenerator:
    """Provide test data generator instance."""
    return TestDataGenerator()


# ===========================
# Custom Assertion Helpers
# ===========================

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
    
    @staticmethod
    def assert_dimension_complete(dimension_data: Dict[str, Any], spec: DimensionSpec):
        """Assert that dimension data meets specification requirements."""
        # Check required elements
        for element in spec.required_elements:
            assert element in dimension_data, \
                f"Missing required element: {element}"
        
        # Check required fields
        for element_type, fields in spec.required_fields.items():
            if element_type in dimension_data:
                element_data = dimension_data[element_type]
                for field in fields:
                    assert field in element_data, \
                        f"Missing required field {field} in {element_type}"


@pytest.fixture
def assertion_helpers() -> AssertionHelpers:
    """Provide assertion helpers instance."""
    return AssertionHelpers()


# ===========================
# Mock Factory
# ===========================

@pytest.fixture
def mock_factory():
    """Factory for creating properly configured mocks."""
    def create_mock(spec_class=None, **kwargs):
        """Create a MagicMock with optional spec and configuration."""
        if spec_class:
            mock = MagicMock(spec=spec_class)
        else:
            mock = MagicMock()
        
        # Configure any additional attributes
        for key, value in kwargs.items():
            setattr(mock, key, value)
        
        return mock
    
    return create_mock


# ===========================
# Pytest Marks
# ===========================

def pytest_configure(config):
    """Register custom pytest markers."""
    config.addinivalue_line(
        "markers", "critical: mark test as critical for MVP (must pass)"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "requires_baseline: mark test as requiring Ansible baseline"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as unit test"
    )


# ===========================
# Test Directory Fixtures
# ===========================

@pytest.fixture
def temp_python_file(tmp_path) -> Path:
    """Create a temporary Python file for testing."""
    python_file = tmp_path / "test_module.py"
    python_file.write_text(textwrap.dedent("""
        def test_function():
            return "test"
        
        class TestClass:
            def test_method(self):
                pass
        
        TEST_CONSTANT = "constant"
    """))
    return python_file


@pytest.fixture
def temp_javascript_file(tmp_path) -> Path:
    """Create a temporary JavaScript file for testing."""
    js_file = tmp_path / "test_module.js"
    js_file.write_text(textwrap.dedent("""
        function testFunction() {
            return "test";
        }
        
        class TestClass {
            testMethod() {}
        }
        
        const TEST_CONSTANT = "constant";
    """))
    return js_file


# ===========================
# Performance Testing Fixtures
# ===========================

@pytest.fixture
def performance_timer():
    """Context manager for timing operations."""
    import time
    
    class PerformanceTimer:
        def __init__(self):
            self.start_time = None
            self.end_time = None
            self.elapsed = None
        
        def __enter__(self):
            self.start_time = time.time()
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            self.end_time = time.time()
            self.elapsed = self.end_time - self.start_time
        
        def assert_under(self, seconds: float):
            """Assert that elapsed time is under specified seconds."""
            assert self.elapsed < seconds, \
                f"Operation took {self.elapsed:.2f}s, expected < {seconds}s"
    
    return PerformanceTimer()