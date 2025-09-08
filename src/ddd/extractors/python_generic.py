"""
GREEN Phase: Minimal implementation to pass tests

Just enough code to make the tests pass, nothing more.
"""

import ast
from dataclasses import dataclass
from typing import List, Optional

from ddd.artifact_extractors.base import (
    ConnectionRequirement,
    ErrorPattern,
    InfrastructureExtractor,
    MaintenanceScenario,
    PermissionRequirement,
    StateManagement,
)


@dataclass
class PythonResourcePermission(PermissionRequirement):
    """Minimal permission class for Python resources"""

    resource_type: str
    operation: str
    target: Optional[str] = None

    def to_maintenance_doc(self) -> str:
        return f"Python {self.resource_type} permission: {self.operation}"

    def get_diagnostic_steps(self) -> List[str]:
        return [f"Check {self.operation} access to {self.resource_type}"]


class GenericPythonExtractor(InfrastructureExtractor):
    """Minimal implementation to pass tests"""

    def extract_permissions(self, content: str) -> List[PermissionRequirement]:
        """Extract permissions - just enough to pass tests"""
        permissions = []
        try:
            tree = ast.parse(content)

            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    # File operations
                    if hasattr(node.func, "id") and node.func.id == "open":
                        permissions.append(PythonResourcePermission("filesystem", "open"))
                    elif hasattr(node.func, "attr"):
                        if node.func.attr in ["read", "write_text", "unlink", "exists"]:
                            permissions.append(
                                PythonResourcePermission("filesystem", node.func.attr)
                            )
                        elif node.func.attr in ["get", "post", "urlopen"]:
                            permissions.append(PythonResourcePermission("network", node.func.attr))
                        elif node.func.attr in ["execute", "commit", "connect"]:
                            permissions.append(PythonResourcePermission("database", node.func.attr))
        except (SyntaxError, AttributeError):
            pass

        # Deduplicate permissions
        seen = set()
        unique_perms = []
        for perm in permissions:
            key = (perm.resource_type, perm.operation, perm.target)
            if key not in seen:
                seen.add(key)
                unique_perms.append(perm)

        return unique_perms

    def extract_error_patterns(self, content: str) -> List[ErrorPattern]:
        """Extract Python error handling patterns"""
        patterns = []

        try:
            tree = ast.parse(content)

            for node in ast.walk(tree):
                if isinstance(node, ast.Raise):
                    if node.exc and hasattr(node.exc, "func") and hasattr(node.exc.func, "id"):
                        patterns.append(
                            ErrorPattern(
                                pattern=node.exc.func.id,
                                error_type="exception",
                                severity="high",
                                recovery_steps=["Check exception handling", "Review error logs"],
                            )
                        )
                elif isinstance(node, ast.ExceptHandler):
                    if node.type and hasattr(node.type, "id"):
                        patterns.append(
                            ErrorPattern(
                                pattern=node.type.id,
                                error_type="handled_exception",
                                severity="medium",
                                recovery_steps=["Exception already handled", "Check handler logic"],
                            )
                        )
        except (SyntaxError, AttributeError):
            pass

        return patterns

    def extract_dependencies(self, content: str) -> List[str]:
        """Extract dependencies - minimal implementation"""
        deps = []
        try:
            tree = ast.parse(content)

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        deps.append(name.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        deps.append(node.module)
        except (SyntaxError, AttributeError):
            pass

        return list(set(deps))

    def extract_state_management(self, content: str) -> Optional[StateManagement]:
        """Extract state management - minimal implementation"""
        try:
            tree = ast.parse(content)

            has_global = False
            has_redis = False

            for node in ast.walk(tree):
                if isinstance(node, ast.Global):
                    has_global = True
                elif isinstance(node, ast.Import):
                    for name in node.names:
                        if "redis" in name.name:
                            has_redis = True

            if has_global or has_redis:
                return StateManagement(
                    idempotent=not has_global,
                    check_mode_supported=False,
                    change_tracking="redis" if has_redis else "memory",
                )
        except (SyntaxError, AttributeError):
            pass

        return None

    def extract_connection_requirements(self, content: str) -> List[ConnectionRequirement]:
        """Extract connections - minimal implementation"""
        requirements = []

        if "requests" in content or "urllib" in content:
            requirements.append(
                ConnectionRequirement(
                    requirement_type="HTTP/HTTPS",
                    description="Network required",
                    validation_steps=["Check API keys"],
                )
            )

        if "boto3" in content:
            requirements.append(
                ConnectionRequirement(
                    requirement_type="AWS",
                    description="AWS services",
                    validation_steps=["AWS credentials"],
                )
            )

        if "psycopg2" in content:
            requirements.append(
                ConnectionRequirement(
                    requirement_type="Database (PostgreSQL)",
                    description="PostgreSQL database",
                    validation_steps=["Database credentials"],
                )
            )

        if "azure" in content:
            requirements.append(
                ConnectionRequirement(
                    requirement_type="Azure",
                    description="Azure services",
                    validation_steps=["Azure credentials"],
                )
            )

        return requirements

    def generate_maintenance_scenarios(self, doc) -> List[MaintenanceScenario]:
        """Generate scenarios - minimal implementation"""
        scenarios = super().generate_maintenance_scenarios(doc)

        # Add scenarios based on what we found
        if any("database" in str(p).lower() for p in doc.permissions):
            scenarios.append(
                MaintenanceScenario(
                    name="Database Connection Failure",
                    trigger="Database unavailable",
                    diagnostic_steps=["Check database"],
                    resolution_steps=["Restart after fix"],
                    preventive_measures=["Monitor database health"],
                )
            )

        if any("network" in str(p).lower() for p in doc.permissions):
            scenarios.append(
                MaintenanceScenario(
                    name="API Endpoint Unavailable",
                    trigger="API down",
                    diagnostic_steps=["Check API"],
                    resolution_steps=["Retry with backoff"],
                    preventive_measures=["Implement circuit breaker"],
                )
            )

        if len(doc.dependencies) > 5:
            scenarios.append(
                MaintenanceScenario(
                    name="Dependency Version Conflict",
                    trigger="Version conflicts",
                    diagnostic_steps=["Check versions"],
                    resolution_steps=["Pin versions"],
                    preventive_measures=["Use dependency lock file"],
                )
            )

        return scenarios
