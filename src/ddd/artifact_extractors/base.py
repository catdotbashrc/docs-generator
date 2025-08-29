"""
Abstract Base Extractor for Infrastructure as Code Tools

REFACTOR PHASE: Production-ready implementation with full documentation

This module provides the abstract interface that all infrastructure extractors
must implement, enabling consistent documentation extraction across different
IaC tools (Ansible, Terraform, Kubernetes, etc.) while allowing tool-specific
customization.

The abstraction focuses on maintenance enablement - extracting the information
needed for day-to-day operations, troubleshooting, and incident response.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class PermissionRequirement(ABC):
    """Abstract permission requirement that each tool implements differently.

    Each IaC tool has its own permission model:
    - Ansible: AWS IAM permissions from boto3 calls
    - Terraform: Provider permissions from resource declarations
    - Kubernetes: RBAC permissions from service accounts

    Subclasses must implement tool-specific extraction and documentation.
    """

    @abstractmethod
    def to_maintenance_doc(self) -> str:
        """Convert to human-readable maintenance documentation.

        Returns:
            String suitable for inclusion in maintenance runbooks
        """
        pass

    @abstractmethod
    def get_diagnostic_steps(self) -> List[str]:
        """Get diagnostic steps for troubleshooting permission issues.

        Returns:
            Ordered list of steps to diagnose permission problems
        """
        pass

    def __eq__(self, other) -> bool:
        """Compare permissions based on their documentation representation."""
        if not isinstance(other, PermissionRequirement):
            return False
        return self.to_maintenance_doc() == other.to_maintenance_doc()

    def __hash__(self) -> int:
        """Hash based on documentation representation for use in sets."""
        return hash(self.to_maintenance_doc())


@dataclass
class ErrorPattern:
    """Represents an error pattern found in infrastructure code"""

    pattern: str
    error_type: str
    severity: str  # low, medium, high, critical
    recovery_steps: List[str]

    def __post_init__(self):
        """Validate severity level"""
        valid_severities = ["low", "medium", "high", "critical"]
        if self.severity not in valid_severities:
            raise ValueError(
                f"Invalid severity: {self.severity}. Must be one of {valid_severities}"
            )


@dataclass
class StateManagement:
    """Represents how infrastructure state is managed"""

    state_type: str  # e.g., "persistent", "ephemeral", "managed"
    state_location: str  # e.g., "database", "file", "remote"
    idempotency_support: bool
    rollback_support: bool
    state_validation_steps: List[str]

    def get_drift_detection_guide(self) -> Dict[str, Any]:
        """Get guide for detecting state drift"""
        return {
            "detection_method": f"Compare {self.state_location} with actual state",
            "correction_steps": [
                f"1. Backup current {self.state_location}",
                "2. Run in check/plan mode to detect drift",
                "3. Review proposed changes",
                "4. Apply corrections if safe",
            ],
        }


@dataclass
class ConnectionRequirement:
    """Represents network/connection requirements"""

    requirement_type: str  # e.g., "network", "auth", "endpoint"
    description: str
    validation_steps: List[str]


@dataclass
class MaintenanceScenario:
    """Represents a maintenance scenario with steps"""

    name: str
    trigger: str
    diagnostic_steps: List[str]
    resolution_steps: List[str]
    preventive_measures: List[str]

    def __post_init__(self):
        """Validate scenario has required steps"""
        if not self.diagnostic_steps:
            raise ValueError(f"Scenario {self.name} must have diagnostic steps")
        if not self.resolution_steps:
            raise ValueError(f"Scenario {self.name} must have resolution steps")


@dataclass
class MaintenanceDocument:
    """Complete maintenance documentation for an infrastructure file.

    This document aggregates all maintenance-critical information extracted
    from an infrastructure file, providing a comprehensive view for operators
    and maintainers.

    Attributes:
        file_path: Source file this documentation was extracted from
        permissions: Required permissions for execution
        error_patterns: Common errors and recovery procedures
        state_management: How state is tracked and managed
        dependencies: External dependencies required
        connection_requirements: Network and connectivity needs
        maintenance_scenarios: Common maintenance situations and solutions
    """

    file_path: Path
    permissions: List[PermissionRequirement]
    error_patterns: List[ErrorPattern]
    state_management: Optional[StateManagement]
    dependencies: List[str]
    connection_requirements: List[ConnectionRequirement]
    maintenance_scenarios: List[MaintenanceScenario] = field(default_factory=list)

    def calculate_coverage(self) -> float:
        """Calculate documentation coverage score.

        Coverage is based on presence of key maintenance aspects:
        - Permissions (what access is needed?)
        - Error patterns (what can go wrong?)
        - State management (how is state tracked?)
        - Dependencies (what's required to run?)
        - Connection requirements (network needs?)
        - Maintenance scenarios (how to troubleshoot?)

        Returns:
            Float between 0.0 and 1.0 representing coverage percentage
        """
        aspects_covered = sum(
            [
                bool(self.permissions),
                bool(self.error_patterns),
                bool(self.state_management),
                bool(self.dependencies),
                bool(self.connection_requirements),
                bool(self.maintenance_scenarios),
            ]
        )

        total_aspects = 6
        return aspects_covered / total_aspects if total_aspects > 0 else 0

    def generate_maintenance_scenarios(self) -> None:
        """Auto-generate maintenance scenarios from extracted information.

        Creates common troubleshooting scenarios based on the extracted
        maintenance information. Only generates scenarios that don't
        already exist to avoid duplicates.
        """
        # Permission troubleshooting scenario
        if self.permissions and not self._has_scenario("permission_troubleshooting"):
            diagnostic_steps = []
            for perm in self.permissions[:3]:  # Use up to 3 permissions for examples
                steps = perm.get_diagnostic_steps()
                diagnostic_steps.append(steps[0] if steps else "Check permissions")

            self.maintenance_scenarios.append(
                MaintenanceScenario(
                    name="permission_troubleshooting",
                    trigger="Permission denied or unauthorized errors",
                    diagnostic_steps=diagnostic_steps or ["Check required permissions"],
                    resolution_steps=[
                        "Identify missing permissions from error messages",
                        "Grant required permissions to service account/role",
                        "Verify permissions are properly applied",
                        "Test access with updated permissions",
                    ],
                    preventive_measures=[
                        "Document required permissions in README",
                        "Implement permission validation checks",
                        "Regular permission audits",
                    ],
                )
            )

        # Error recovery scenario
        if self.error_patterns and not self._has_scenario("error_recovery"):
            # Collect unique recovery steps from error patterns
            recovery_steps = []
            seen_steps = set()
            for error_pattern in self.error_patterns:
                for step in error_pattern.recovery_steps[:2]:  # Take first 2 steps from each
                    if step not in seen_steps:
                        recovery_steps.append(step)
                        seen_steps.add(step)

            self.maintenance_scenarios.append(
                MaintenanceScenario(
                    name="error_recovery",
                    trigger="Execution failures or unexpected errors",
                    diagnostic_steps=[
                        "Check error logs for specific error messages",
                        "Identify error type and severity",
                        "Determine if error is transient or persistent",
                        "Check system resources and dependencies",
                    ],
                    resolution_steps=recovery_steps
                    or ["Follow error-specific recovery procedures"],
                    preventive_measures=[
                        "Implement comprehensive error handling",
                        "Add retry logic for transient failures",
                        "Set up monitoring and alerting",
                    ],
                )
            )

    def _has_scenario(self, scenario_name: str) -> bool:
        """Check if a scenario with the given name already exists."""
        return any(s.name == scenario_name for s in self.maintenance_scenarios)


class InfrastructureExtractor(ABC):
    """
    Abstract base class for all infrastructure-as-code extractors

    This class defines the contract that all infrastructure extractors must fulfill,
    whether they're for Ansible, Terraform, Kubernetes, or other IaC tools.
    """

    @abstractmethod
    def extract_permissions(self, content: str) -> List[PermissionRequirement]:
        """
        Extract permission requirements from infrastructure code

        Args:
            content: The file content to analyze

        Returns:
            List of permission requirements found
        """
        pass

    @abstractmethod
    def extract_error_patterns(self, content: str) -> List[ErrorPattern]:
        """
        Extract error handling patterns from infrastructure code

        Args:
            content: The file content to analyze

        Returns:
            List of error patterns found
        """
        pass

    @abstractmethod
    def extract_state_management(self, content: str) -> Optional[StateManagement]:
        """
        Extract state management information

        Args:
            content: The file content to analyze

        Returns:
            State management info if found, None otherwise
        """
        pass

    @abstractmethod
    def extract_dependencies(self, content: str) -> List[str]:
        """
        Extract dependencies (libraries, modules, providers)

        Args:
            content: The file content to analyze

        Returns:
            List of dependencies found
        """
        pass

    @abstractmethod
    def extract_connection_requirements(self, content: str) -> List[ConnectionRequirement]:
        """
        Extract network and connection requirements

        Args:
            content: The file content to analyze

        Returns:
            List of connection requirements found
        """
        pass

    def extract(self, file_path: Path) -> MaintenanceDocument:
        """
        Template method that orchestrates the extraction process

        This method defines the workflow that all extractors follow:
        1. Read the file
        2. Extract various maintenance aspects
        3. Generate maintenance scenarios
        4. Return complete documentation

        Args:
            file_path: Path to the infrastructure file

        Returns:
            Complete maintenance documentation

        Raises:
            FileNotFoundError: If file doesn't exist
            IOError: If file can't be read
        """
        # Validate file exists
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Check if it's actually a file
        if file_path.is_dir():
            raise IOError(f"Path is a directory, not a file: {file_path}")

        # Read file content
        try:
            content = file_path.read_text()
        except Exception as e:
            raise IOError(f"Failed to read file {file_path}: {e}")

        # Extract all maintenance aspects (template method pattern)
        doc = MaintenanceDocument(
            file_path=file_path,
            permissions=self.extract_permissions(content),
            error_patterns=self.extract_error_patterns(content),
            state_management=self.extract_state_management(content),
            dependencies=self.extract_dependencies(content),
            connection_requirements=self.extract_connection_requirements(content),
            maintenance_scenarios=[],
        )

        # Generate maintenance scenarios
        scenarios = self.generate_maintenance_scenarios(doc)
        if scenarios:
            doc.maintenance_scenarios = scenarios
        else:
            # Use default generation
            doc.generate_maintenance_scenarios()

        return doc

    def generate_maintenance_scenarios(self, doc: MaintenanceDocument) -> List[MaintenanceScenario]:
        """
        Generate maintenance scenarios from extracted information

        Subclasses can override this to provide custom scenario generation

        Args:
            doc: The maintenance document with extracted info

        Returns:
            List of maintenance scenarios
        """
        # Default implementation returns empty list, letting the document auto-generate
        return []
