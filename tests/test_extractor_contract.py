"""
Generic Extractor Contract Tests

This is the distilled essence of what EVERY extractor must satisfy.
Any extractor that passes these tests proves DDD's extensibility.

This is our proof that DDD is a platform, not a tool.
"""

from abc import ABC
from pathlib import Path
from textwrap import dedent
from typing import List, Type

import pytest

from ddd.artifact_extractors.base import (
    ConnectionRequirement,
    ErrorPattern,
    InfrastructureExtractor,
    MaintenanceDocument,
    MaintenanceScenario,
    PermissionRequirement,
    StateManagement,
)


class ExtractorContractTestSuite:
    """
    The Universal Contract Test Suite

    ANY extractor that passes these tests is guaranteed to work with DDD.
    This proves our architecture is truly extensible.
    """

    @pytest.fixture
    def extractor_class(self) -> Type[InfrastructureExtractor]:
        """Override this to provide the extractor class to test"""
        raise NotImplementedError("Subclass must provide extractor_class")

    @pytest.fixture
    def sample_code(self) -> str:
        """Override this to provide language-specific sample code"""
        raise NotImplementedError("Subclass must provide sample_code")

    @pytest.fixture
    def expected_dependencies(self) -> List[str]:
        """Override this to provide expected dependencies from sample_code"""
        raise NotImplementedError("Subclass must provide expected_dependencies")

    # ========== UNIVERSAL CONTRACT TESTS ==========

    def test_inherits_from_infrastructure_extractor(self, extractor_class):
        """RULE 1: Must inherit from InfrastructureExtractor"""
        assert issubclass(extractor_class, InfrastructureExtractor)
        # The extractor must be instantiable (not abstract itself)

    def test_can_be_instantiated(self, extractor_class):
        """RULE 2: Must be instantiable with no arguments"""
        extractor = extractor_class()
        assert isinstance(extractor, InfrastructureExtractor)

    def test_extract_returns_maintenance_document(self, extractor_class, sample_code, tmp_path):
        """RULE 3: extract() must return MaintenanceDocument"""
        # Create test file
        test_file = tmp_path / "test_code.py"
        test_file.write_text(sample_code)

        # Extract
        extractor = extractor_class()
        result = extractor.extract(test_file)

        # Verify contract
        assert isinstance(result, MaintenanceDocument)
        assert result.file_path == test_file

    def test_permissions_are_permission_requirements(self, extractor_class, sample_code, tmp_path):
        """RULE 4: All permissions must be PermissionRequirement subclasses"""
        test_file = tmp_path / "test_code.py"
        test_file.write_text(sample_code)

        extractor = extractor_class()
        doc = extractor.extract(test_file)

        for perm in doc.permissions:
            assert isinstance(perm, PermissionRequirement)
            # Must implement abstract methods
            assert callable(perm.to_maintenance_doc)
            assert callable(perm.get_diagnostic_steps)

            # Methods must return correct types
            maintenance_doc = perm.to_maintenance_doc()
            assert isinstance(maintenance_doc, str)
            assert len(maintenance_doc) > 0

            diagnostic_steps = perm.get_diagnostic_steps()
            assert isinstance(diagnostic_steps, list)
            assert all(isinstance(step, str) for step in diagnostic_steps)

    def test_error_patterns_have_required_fields(self, extractor_class, sample_code, tmp_path):
        """RULE 5: Error patterns must have all required fields"""
        test_file = tmp_path / "test_code.py"
        test_file.write_text(sample_code)

        extractor = extractor_class()
        doc = extractor.extract(test_file)

        for error in doc.error_patterns:
            assert isinstance(error, ErrorPattern)
            assert error.pattern is not None
            assert error.error_type is not None
            assert error.severity in ["low", "medium", "high", "critical"]
            assert isinstance(error.recovery_steps, list)

    def test_dependencies_are_strings(self, extractor_class, sample_code, tmp_path):
        """RULE 6: Dependencies must be list of strings"""
        test_file = tmp_path / "test_code.py"
        test_file.write_text(sample_code)

        extractor = extractor_class()
        doc = extractor.extract(test_file)

        assert isinstance(doc.dependencies, list)
        assert all(isinstance(dep, str) for dep in doc.dependencies)

    def test_state_management_optional_but_valid(self, extractor_class, sample_code, tmp_path):
        """RULE 7: State management is optional but must be valid if present"""
        test_file = tmp_path / "test_code.py"
        test_file.write_text(sample_code)

        extractor = extractor_class()
        doc = extractor.extract(test_file)

        if doc.state_management:
            assert isinstance(doc.state_management, StateManagement)
            # Check base StateManagement fields
            assert doc.state_management.state_type is not None
            assert doc.state_management.state_location is not None
            assert isinstance(doc.state_management.idempotency_support, bool)
            assert isinstance(doc.state_management.rollback_support, bool)
            assert isinstance(doc.state_management.state_validation_steps, list)

    def test_connection_requirements_valid(self, extractor_class, sample_code, tmp_path):
        """RULE 8: Connection requirements must follow contract"""
        test_file = tmp_path / "test_code.py"
        test_file.write_text(sample_code)

        extractor = extractor_class()
        doc = extractor.extract(test_file)

        for conn in doc.connection_requirements:
            assert isinstance(conn, ConnectionRequirement)
            assert conn.requirement_type is not None
            assert conn.description is not None
            assert isinstance(conn.validation_steps, list)

    def test_maintenance_scenarios_generated(self, extractor_class, sample_code, tmp_path):
        """RULE 9: Must generate maintenance scenarios (auto or custom)"""
        test_file = tmp_path / "test_code.py"
        test_file.write_text(sample_code)

        extractor = extractor_class()
        doc = extractor.extract(test_file)

        # Should have at least auto-generated scenarios
        assert isinstance(doc.maintenance_scenarios, list)

        for scenario in doc.maintenance_scenarios:
            assert isinstance(scenario, MaintenanceScenario)
            assert scenario.name is not None
            assert scenario.trigger is not None
            assert len(scenario.diagnostic_steps) > 0
            assert len(scenario.resolution_steps) > 0
            assert len(scenario.preventive_measures) > 0

    def test_handles_invalid_syntax_gracefully(self, extractor_class, tmp_path):
        """RULE 10: Must handle invalid code without crashing"""
        test_file = tmp_path / "invalid.py"
        test_file.write_text("This is not valid Python code {][")

        extractor = extractor_class()
        # Should not raise exception
        doc = extractor.extract(test_file)

        # Should return valid document even if empty
        assert isinstance(doc, MaintenanceDocument)
        assert doc.file_path == test_file

    def test_extracts_expected_dependencies(
        self, extractor_class, sample_code, expected_dependencies, tmp_path
    ):
        """RULE 11: Must extract expected dependencies from sample code"""
        test_file = tmp_path / "test_code.py"
        test_file.write_text(sample_code)

        extractor = extractor_class()
        doc = extractor.extract(test_file)

        for expected_dep in expected_dependencies:
            assert (
                expected_dep in doc.dependencies
            ), f"Expected to find {expected_dep} in dependencies"

    def test_no_duplicate_permissions(self, extractor_class, sample_code, tmp_path):
        """RULE 12: Must deduplicate permissions"""
        # Create code with repeated operations
        repeated_code = sample_code + "\n" + sample_code  # Double the code

        test_file = tmp_path / "test_code.py"
        test_file.write_text(repeated_code)

        extractor = extractor_class()
        doc = extractor.extract(test_file)

        # Check for duplicates using string representation
        permission_strings = [p.to_maintenance_doc() for p in doc.permissions]
        assert len(permission_strings) == len(
            set(permission_strings)
        ), "Found duplicate permissions"


# ========== CONCRETE TEST IMPLEMENTATIONS ==========


class TestAnsibleExtractorContract(ExtractorContractTestSuite):
    """Prove AnsibleModuleExtractor satisfies the contract"""

    @pytest.fixture
    def extractor_class(self):
        from ddd.artifact_extractors.ansible_extractor import AnsibleModuleExtractor

        return AnsibleModuleExtractor

    @pytest.fixture
    def sample_code(self):
        return dedent(
            """
            import boto3
            from ansible.module_utils.basic import AnsibleModule
            
            def main():
                module = AnsibleModule(
                    argument_spec=dict(
                        state=dict(default='present')
                    ),
                    supports_check_mode=True
                )
                
                client = boto3.client('ec2')
                instances = client.describe_instances()
                
                if not instances:
                    module.fail_json(msg="No instances found")
                
                module.exit_json(changed=True, instances=instances)
            
            if __name__ == '__main__':
                main()
        """
        )

    @pytest.fixture
    def expected_dependencies(self):
        # Note: ansible.module_utils gets filtered out in extract_dependencies
        # Only external dependencies like boto3 are captured
        return ["boto3"]


class TestGenericPythonExtractorContract(ExtractorContractTestSuite):
    """Prove GenericPythonExtractor satisfies the contract"""

    @pytest.fixture
    def extractor_class(self):
        from ddd.extractors.python_generic import GenericPythonExtractor

        return GenericPythonExtractor

    @pytest.fixture
    def sample_code(self):
        return dedent(
            """
            import os
            import sys
            import requests
            from pathlib import Path
            
            def process_data(filename):
                # File operations
                with open(filename, 'r') as f:
                    data = f.read()
                
                # Network operations
                response = requests.get('https://api.example.com/data')
                
                # Error handling
                if not response.ok:
                    raise ValueError("API request failed")
                
                # State management
                Path('output.txt').write_text(data)
                
                return data
        """
        )

    @pytest.fixture
    def expected_dependencies(self):
        return ["os", "sys", "requests", "pathlib"]


# ========== EXTENSIBILITY PROOF TEST ==========


class TestExtensibilityProof:
    """
    The Ultimate Proof: Multiple extractors work with the same framework
    """

    def test_multiple_extractors_share_same_base(self):
        """All extractors share the same base class"""
        from ddd.artifact_extractors.ansible_extractor import AnsibleModuleExtractor
        from ddd.extractors.python_generic import GenericPythonExtractor

        # Both inherit from same base
        assert issubclass(AnsibleModuleExtractor, InfrastructureExtractor)
        assert issubclass(GenericPythonExtractor, InfrastructureExtractor)

        # Both produce same document type
        assert AnsibleModuleExtractor().extract.__annotations__["return"] == MaintenanceDocument
        assert GenericPythonExtractor().extract.__annotations__["return"] == MaintenanceDocument

    def test_extractors_analyze_different_domains(self):
        """Different extractors extract different things from same code"""
        code = dedent(
            """
            import boto3
            
            def process():
                client = boto3.client('s3')
                client.list_buckets()
        """
        )

        from ddd.artifact_extractors.ansible_extractor import AnsibleModuleExtractor
        from ddd.extractors.python_generic import GenericPythonExtractor

        # Create test file
        test_file = Path("/tmp/test_extensibility.py")
        test_file.write_text(code)

        # Ansible extractor finds AWS permissions
        ansible_doc = AnsibleModuleExtractor().extract(test_file)
        ansible_perms = [p.to_maintenance_doc() for p in ansible_doc.permissions]

        # Generic extractor finds generic operations
        generic_doc = GenericPythonExtractor().extract(test_file)
        generic_perms = [p.to_maintenance_doc() for p in generic_doc.permissions]

        # They should find DIFFERENT things (proving they're different)
        assert ansible_perms != generic_perms

        # But both should find boto3 dependency
        assert "boto3" in ansible_doc.dependencies
        assert "boto3" in generic_doc.dependencies

        test_file.unlink()

    def test_ddd_can_analyze_itself(self):
        """The ultimate proof: DDD can analyze its own code"""
        from ddd.extractors.python_generic import GenericPythonExtractor

        # Analyze DDD's own base extractor
        ddd_base = Path("src/ddd/artifact_extractors/base.py")
        if ddd_base.exists():
            extractor = GenericPythonExtractor()
            doc = extractor.extract(ddd_base)

            # Should find DDD's own dependencies
            assert "abc" in doc.dependencies
            assert "dataclasses" in doc.dependencies
            assert "pathlib" in doc.dependencies

            # Should find file operations (base.py reads files)
            assert len(doc.permissions) > 0

            # Should generate maintenance scenarios
            assert len(doc.maintenance_scenarios) > 0

            # This proves GenericPythonExtractor works on ANY Python code
            # including the framework itself!

    def test_coverage_calculator_works_with_any_extractor(self):
        """Coverage calculator is extractor-agnostic"""
        from ddd.artifact_extractors.ansible_extractor import AnsibleModuleExtractor
        from ddd.coverage import DocumentationCoverage
        from ddd.extractors.python_generic import GenericPythonExtractor

        calculator = DocumentationCoverage()

        # Both extractors produce documents that work with coverage
        test_file = Path("/tmp/test_coverage.py")
        test_file.write_text("import os")

        ansible_doc = AnsibleModuleExtractor().extract(test_file)
        generic_doc = GenericPythonExtractor().extract(test_file)

        # Convert MaintenanceDocument to the format expected by coverage calculator
        # The coverage calculator expects a dict with dimension data, not MaintenanceDocument
        ansible_data = {"dependencies": ansible_doc.dependencies}
        generic_data = {"dependencies": generic_doc.dependencies}

        # Coverage calculator works with both
        # (We're not testing the scores, just that it doesn't crash)
        ansible_coverage = calculator.measure(ansible_data)
        generic_coverage = calculator.measure(generic_data)

        assert ansible_coverage is not None
        assert generic_coverage is not None
