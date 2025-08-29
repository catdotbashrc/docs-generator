"""
Unit tests for Abstract Infrastructure Extractor Base Class

Following TDD: RED phase - write failing tests first
These tests define the contract that all infrastructure extractors must fulfill
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import pytest

# These imports will fail initially (RED phase)
from ddd.artifact_extractors.base import (
    ConnectionRequirement,
    ErrorPattern,
    InfrastructureExtractor,
    MaintenanceDocument,
    MaintenanceScenario,
    PermissionRequirement,
    StateManagement,
)


class TestInfrastructureExtractorContract:
    """Test the abstract contract all infrastructure extractors must fulfill"""

    def test_abstract_base_cannot_be_instantiated(self):
        """Abstract base class should not be directly instantiable"""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            InfrastructureExtractor()

    def test_subclass_must_implement_abstract_methods(self):
        """Subclasses must implement all abstract methods"""

        # Create incomplete implementation
        class IncompleteExtractor(InfrastructureExtractor):
            pass

        # Should fail to instantiate without all abstract methods
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            IncompleteExtractor()

    def test_extract_method_returns_maintenance_document(self):
        """Main extract method should return MaintenanceDocument"""

        # Create minimal valid implementation
        class MinimalExtractor(InfrastructureExtractor):
            def extract_permissions(self, content: str) -> List[PermissionRequirement]:
                return []

            def extract_error_patterns(self, content: str) -> List[ErrorPattern]:
                return []

            def extract_state_management(self, content: str) -> Optional[StateManagement]:
                return None

            def extract_dependencies(self, content: str) -> List[str]:
                return []

            def extract_connection_requirements(self, content: str) -> List[ConnectionRequirement]:
                return []

        # Create a test file
        test_file = Path("/tmp/test_minimal.txt")
        test_file.write_text("test content")

        extractor = MinimalExtractor()
        result = extractor.extract(test_file)

        assert isinstance(result, MaintenanceDocument)
        assert hasattr(result, "permissions")
        assert hasattr(result, "error_patterns")
        assert hasattr(result, "state_management")
        assert hasattr(result, "dependencies")
        assert hasattr(result, "connection_requirements")
        assert hasattr(result, "maintenance_scenarios")

        # Clean up
        test_file.unlink()


class TestPermissionRequirement:
    """Test the PermissionRequirement abstract interface"""

    def test_permission_requirement_is_abstract(self):
        """PermissionRequirement should be abstract"""
        with pytest.raises(TypeError):
            PermissionRequirement()

    def test_permission_has_required_methods(self):
        """Permission must have to_maintenance_doc method"""

        class ConcretePermission(PermissionRequirement):
            def to_maintenance_doc(self) -> str:
                return "permission doc"

            def get_diagnostic_steps(self) -> List[str]:
                return ["check permission"]

        perm = ConcretePermission()
        assert perm.to_maintenance_doc() == "permission doc"
        assert len(perm.get_diagnostic_steps()) > 0

    def test_permission_equality(self):
        """Permissions should be comparable"""

        class TestPermission(PermissionRequirement):
            def __init__(self, name: str):
                self.name = name

            def to_maintenance_doc(self) -> str:
                return f"Permission: {self.name}"

            def get_diagnostic_steps(self) -> List[str]:
                return [f"Check {self.name}"]

        p1 = TestPermission("read")
        p2 = TestPermission("read")
        p3 = TestPermission("write")

        assert p1 == p2
        assert p1 != p3


class TestErrorPattern:
    """Test the ErrorPattern data structure"""

    def test_error_pattern_creation(self):
        """ErrorPattern should capture error information"""
        error = ErrorPattern(
            pattern="ConnectionTimeout",
            error_type="timeout",
            severity="high",
            recovery_steps=["Check network", "Retry connection"],
        )

        assert error.pattern == "ConnectionTimeout"
        assert error.error_type == "timeout"
        assert error.severity == "high"
        assert len(error.recovery_steps) == 2

    def test_error_pattern_validation(self):
        """ErrorPattern should validate severity levels"""
        valid_severities = ["low", "medium", "high", "critical"]

        for severity in valid_severities:
            error = ErrorPattern(
                pattern="test", error_type="test", severity=severity, recovery_steps=[]
            )
            assert error.severity in valid_severities

        # Invalid severity should raise
        with pytest.raises(ValueError, match="Invalid severity"):
            ErrorPattern(pattern="test", error_type="test", severity="invalid", recovery_steps=[])


class TestStateManagement:
    """Test the StateManagement structure"""

    def test_state_management_creation(self):
        """StateManagement should capture state handling info"""
        state = StateManagement(
            state_type="persistent",
            state_location="database",
            idempotency_support=True,
            rollback_support=True,
            state_validation_steps=["Check current state", "Compare with desired"],
        )

        assert state.state_type == "persistent"
        assert state.state_location == "database"
        assert state.idempotency_support is True
        assert state.rollback_support is True
        assert len(state.state_validation_steps) == 2

    def test_state_management_drift_detection(self):
        """StateManagement should support drift detection info"""
        state = StateManagement(
            state_type="managed",
            state_location="terraform.tfstate",
            idempotency_support=True,
            rollback_support=False,
            state_validation_steps=[],
        )

        drift_info = state.get_drift_detection_guide()
        assert isinstance(drift_info, dict)
        assert "detection_method" in drift_info
        assert "correction_steps" in drift_info


class TestMaintenanceScenario:
    """Test the MaintenanceScenario generation"""

    def test_scenario_creation(self):
        """MaintenanceScenario should have required fields"""
        scenario = MaintenanceScenario(
            name="permission_denied",
            trigger="Access denied error",
            diagnostic_steps=["Check IAM role", "Verify credentials"],
            resolution_steps=["Add required permission", "Test access"],
            preventive_measures=["Regular permission audits"],
        )

        assert scenario.name == "permission_denied"
        assert scenario.trigger == "Access denied error"
        assert len(scenario.diagnostic_steps) == 2
        assert len(scenario.resolution_steps) == 2
        assert len(scenario.preventive_measures) == 1

    def test_scenario_validation(self):
        """Scenarios must have at least diagnostic and resolution steps"""
        # Invalid: no steps
        with pytest.raises(ValueError, match="must have diagnostic steps"):
            MaintenanceScenario(
                name="test",
                trigger="test",
                diagnostic_steps=[],  # Empty!
                resolution_steps=["fix"],
                preventive_measures=[],
            )

        # Invalid: no resolution
        with pytest.raises(ValueError, match="must have resolution steps"):
            MaintenanceScenario(
                name="test",
                trigger="test",
                diagnostic_steps=["diagnose"],
                resolution_steps=[],  # Empty!
                preventive_measures=[],
            )


class TestMaintenanceDocument:
    """Test the complete MaintenanceDocument structure"""

    def test_document_creation(self):
        """MaintenanceDocument should aggregate all maintenance info"""
        doc = MaintenanceDocument(
            file_path=Path("test.py"),
            permissions=[],
            error_patterns=[],
            state_management=None,
            dependencies=[],
            connection_requirements=[],
            maintenance_scenarios=[],
        )

        assert doc.file_path == Path("test.py")
        assert doc.permissions == []
        assert doc.error_patterns == []
        assert doc.maintenance_scenarios == []

    def test_document_coverage_calculation(self):
        """Document should calculate its own coverage score"""
        doc = MaintenanceDocument(
            file_path=Path("test.py"),
            permissions=["perm1"],  # Has permissions
            error_patterns=[],  # No error patterns
            state_management=None,  # No state management
            dependencies=["dep1"],  # Has dependencies
            connection_requirements=[],  # No connection requirements
            maintenance_scenarios=[],  # No scenarios
        )

        coverage = doc.calculate_coverage()

        # Should have partial coverage (2/6 aspects covered)
        assert 0 < coverage < 1
        assert coverage == pytest.approx(2 / 6, rel=0.01)

    def test_document_scenario_generation(self):
        """Document should auto-generate scenarios from extracted info"""

        # Create permission requirement
        class TestPermission(PermissionRequirement):
            def to_maintenance_doc(self) -> str:
                return "test:permission"

            def get_diagnostic_steps(self) -> List[str]:
                return ["Check permission"]

        doc = MaintenanceDocument(
            file_path=Path("test.py"),
            permissions=[TestPermission()],
            error_patterns=[ErrorPattern("timeout", "network", "high", ["retry"])],
            state_management=StateManagement("persistent", "file", True, False, []),
            dependencies=["requests"],
            connection_requirements=[],
            maintenance_scenarios=[],
        )

        # Should auto-generate scenarios
        doc.generate_maintenance_scenarios()

        assert len(doc.maintenance_scenarios) > 0

        # Should have permission troubleshooting scenario
        permission_scenarios = [
            s for s in doc.maintenance_scenarios if s.name == "permission_troubleshooting"
        ]
        assert len(permission_scenarios) == 1

        # Should have error recovery scenario
        error_scenarios = [s for s in doc.maintenance_scenarios if s.name == "error_recovery"]
        assert len(error_scenarios) == 1


class TestExtractorTemplateMethod:
    """Test the template method pattern in base extractor"""

    def test_extract_follows_template_pattern(self):
        """Extract method should follow defined workflow"""
        call_order = []

        class TestExtractor(InfrastructureExtractor):
            def extract_permissions(self, content: str) -> List[PermissionRequirement]:
                call_order.append("permissions")
                return []

            def extract_error_patterns(self, content: str) -> List[ErrorPattern]:
                call_order.append("errors")
                return []

            def extract_state_management(self, content: str) -> Optional[StateManagement]:
                call_order.append("state")
                return None

            def extract_dependencies(self, content: str) -> List[str]:
                call_order.append("dependencies")
                return []

            def extract_connection_requirements(self, content: str) -> List[ConnectionRequirement]:
                call_order.append("connections")
                return []

        # Create a test file
        test_file = Path("/tmp/test_extract.txt")
        test_file.write_text("test content")

        extractor = TestExtractor()
        doc = extractor.extract(test_file)

        # Verify extraction order
        assert call_order == ["permissions", "errors", "state", "dependencies", "connections"]

        # Verify scenarios were generated
        assert hasattr(doc, "maintenance_scenarios")

        # Clean up
        test_file.unlink()

    def test_extract_handles_missing_file(self):
        """Extract should handle missing files gracefully"""

        class TestExtractor(InfrastructureExtractor):
            def extract_permissions(self, content: str) -> List[PermissionRequirement]:
                return []

            def extract_error_patterns(self, content: str) -> List[ErrorPattern]:
                return []

            def extract_state_management(self, content: str) -> Optional[StateManagement]:
                return None

            def extract_dependencies(self, content: str) -> List[str]:
                return []

            def extract_connection_requirements(self, content: str) -> List[ConnectionRequirement]:
                return []

        extractor = TestExtractor()

        with pytest.raises(FileNotFoundError):
            extractor.extract(Path("/nonexistent/file.txt"))

    def test_extract_handles_read_errors(self):
        """Extract should handle file read errors"""

        class TestExtractor(InfrastructureExtractor):
            def extract_permissions(self, content: str) -> List[PermissionRequirement]:
                return []

            def extract_error_patterns(self, content: str) -> List[ErrorPattern]:
                return []

            def extract_state_management(self, content: str) -> Optional[StateManagement]:
                return None

            def extract_dependencies(self, content: str) -> List[str]:
                return []

            def extract_connection_requirements(self, content: str) -> List[ConnectionRequirement]:
                return []

        # Create unreadable file (directory)
        test_dir = Path("/tmp/test_dir")
        test_dir.mkdir(exist_ok=True)

        extractor = TestExtractor()

        with pytest.raises(IOError):
            extractor.extract(test_dir)

        # Clean up
        test_dir.rmdir()


class TestExtractorExtensibility:
    """Test that the base class is properly extensible"""

    def test_subclass_can_add_tool_specific_methods(self):
        """Subclasses should be able to add their own methods"""

        class AnsibleExtractor(InfrastructureExtractor):
            def extract_permissions(self, content: str) -> List[PermissionRequirement]:
                return self.extract_boto3_permissions(content)

            def extract_boto3_permissions(self, content: str) -> List[PermissionRequirement]:
                """Ansible-specific method"""
                return []  # Ansible-specific implementation

            def extract_error_patterns(self, content: str) -> List[ErrorPattern]:
                return []

            def extract_state_management(self, content: str) -> Optional[StateManagement]:
                return None

            def extract_dependencies(self, content: str) -> List[str]:
                return []

            def extract_connection_requirements(self, content: str) -> List[ConnectionRequirement]:
                return []

        extractor = AnsibleExtractor()

        # Should have both base and specific methods
        assert hasattr(extractor, "extract")  # From base
        assert hasattr(extractor, "extract_boto3_permissions")  # Ansible-specific

    def test_subclass_can_override_scenario_generation(self):
        """Subclasses should be able to customize scenario generation"""

        class CustomExtractor(InfrastructureExtractor):
            def extract_permissions(self, content: str) -> List[PermissionRequirement]:
                return []

            def extract_error_patterns(self, content: str) -> List[ErrorPattern]:
                return []

            def extract_state_management(self, content: str) -> Optional[StateManagement]:
                return None

            def extract_dependencies(self, content: str) -> List[str]:
                return []

            def extract_connection_requirements(self, content: str) -> List[ConnectionRequirement]:
                return []

            def generate_maintenance_scenarios(
                self, doc: MaintenanceDocument
            ) -> List[MaintenanceScenario]:
                """Custom scenario generation"""
                return [
                    MaintenanceScenario(
                        name="custom_scenario",
                        trigger="custom trigger",
                        diagnostic_steps=["custom diagnostic"],
                        resolution_steps=["custom resolution"],
                        preventive_measures=[],
                    )
                ]

        test_file = Path("/tmp/test.txt")
        test_file.write_text("test")

        extractor = CustomExtractor()
        doc = extractor.extract(test_file)

        # Should use custom scenario generation
        assert len(doc.maintenance_scenarios) == 1
        assert doc.maintenance_scenarios[0].name == "custom_scenario"

        # Clean up
        test_file.unlink()
