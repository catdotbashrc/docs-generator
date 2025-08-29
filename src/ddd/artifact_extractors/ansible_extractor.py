"""
Ansible Module Extractor Implementation

GREEN PHASE: Minimal implementation to pass tests
Extracts maintenance-critical information from Ansible modules
"""

import re
from dataclasses import dataclass
from typing import Dict, List, Optional

import yaml

from ddd.artifact_extractors.base import (
    ConnectionRequirement,
    ErrorPattern,
    InfrastructureExtractor,
    PermissionRequirement,
    StateManagement,
)


@dataclass
class AWSIAMPermission(PermissionRequirement):
    """AWS IAM permission requirement for Ansible modules"""

    service: str
    action: str

    def to_maintenance_doc(self) -> str:
        """Convert to AWS IAM permission format"""
        return f"AWS IAM Permission: {self.service}:{self.action}"

    def __hash__(self) -> int:
        """Hash based on service and action for use in sets"""
        return hash((self.service, self.action))

    def get_diagnostic_steps(self) -> List[str]:
        """AWS-specific diagnostic steps"""
        return [
            f"Check IAM policy for {self.service}:{self.action} permission",
            "Verify AWS credentials are configured correctly",
            "Ensure using correct AWS account and region",
            "Check for explicit deny policies that might override allows",
        ]

    @classmethod
    def from_boto3_call(cls, service: str, method: str) -> "AWSIAMPermission":
        """Create permission from boto3 method call"""
        # Convert snake_case to PascalCase for AWS actions
        action = "".join(word.capitalize() for word in method.split("_"))
        return cls(service=service, action=action)


@dataclass
class AnsibleStateManagement(StateManagement):
    """Ansible-specific state management"""

    supports_check_mode: bool = False
    tracks_changed: bool = False

    def __post_init__(self):
        """Set Ansible-specific defaults"""
        if not self.state_type:
            self.state_type = "check_mode" if self.supports_check_mode else "stateless"
        if not self.state_location:
            self.state_location = "module_params"


class AnsibleModuleExtractor(InfrastructureExtractor):
    """Extract documentation from Ansible modules"""

    def extract_permissions(self, content: str) -> List[PermissionRequirement]:
        """Extract AWS IAM permissions from boto3 calls"""
        permissions = set()

        # Find boto3 client creations
        client_pattern = r"boto3\.client\(['\"](\w+)['\"]"
        services = re.findall(client_pattern, content)

        # Find boto3 resource creations
        resource_pattern = r"boto3\.resource\(['\"](\w+)['\"]"
        services.extend(re.findall(resource_pattern, content))

        # For each service, find method calls
        for service in services:
            # Pattern for client.method() calls
            method_pattern = r"client\.(\w+)\("
            methods = re.findall(method_pattern, content)

            for method in methods:
                perm = AWSIAMPermission.from_boto3_call(service, method)
                permissions.add(perm)

        # Also check for specific service variable patterns
        # e.g., ec2 = boto3.client('ec2'); ec2.describe_instances()
        service_var_pattern = r"(\w+)\s*=\s*boto3\.(?:client|resource)\(['\"](\w+)['\"]"
        for var_name, service in re.findall(service_var_pattern, content):
            var_method_pattern = rf"{var_name}\.(\w+)\("
            methods = re.findall(var_method_pattern, content)

            for method in methods:
                if not method.startswith("_"):  # Skip private methods
                    perm = AWSIAMPermission.from_boto3_call(service, method)
                    permissions.add(perm)

        # Handle s3.Bucket() special case
        if "s3.Bucket" in content:
            permissions.add(AWSIAMPermission("s3", "PutObject"))

        return list(permissions)

    def extract_error_patterns(self, content: str) -> List[ErrorPattern]:
        """Extract error handling patterns from Ansible modules"""
        patterns = []

        # Extract module.fail_json patterns
        fail_json_pattern = r"module\.fail_json\(msg=['\"]([^'\"]+)['\"]"
        for match in re.finditer(fail_json_pattern, content):
            patterns.append(
                ErrorPattern(
                    pattern=match.group(1),
                    error_type="validation",
                    severity="high",
                    recovery_steps=["Check module parameters", "Review error message"],
                )
            )

        # Extract exception handling
        exception_pattern = r"except\s+(\w+(?:Error)?)\s*(?:as\s+\w+)?:"
        for match in re.finditer(exception_pattern, content):
            error_class = match.group(1)
            error_type = (
                "aws_error" if error_class in ["ClientError", "BotoCoreError"] else "exception"
            )
            patterns.append(
                ErrorPattern(
                    pattern=error_class,
                    error_type=error_type,
                    severity="high" if "Error" in error_class else "medium",
                    recovery_steps=(
                        ["Check AWS credentials", "Verify permissions"]
                        if error_type == "aws_error"
                        else ["Check error logs", "Review stack trace"]
                    ),
                )
            )

        # Detect retry patterns
        if "retry" in content.lower() or "exponential_backoff" in content:
            patterns.append(
                ErrorPattern(
                    pattern="exponential_backoff" if "exponential_backoff" in content else "retry",
                    error_type="retry",
                    severity="medium",
                    recovery_steps=["Check for transient errors", "Review retry configuration"],
                )
            )

        return patterns

    def extract_state_management(self, content: str) -> Optional[StateManagement]:
        """Extract state management information"""
        supports_check_mode = "supports_check_mode=True" in content
        tracks_changed = "changed = False" in content or "changed=False" in content

        if not supports_check_mode and not tracks_changed and "current" not in content.lower():
            return None

        validation_steps = []
        if "check_mode" in content:
            validation_steps.append("Check mode supported for dry runs")
        if tracks_changed or "changed" in content:
            validation_steps.append("Tracks changed state")
        if "current" in content.lower() and "desired" in content.lower():
            validation_steps.append("Compare current state with desired state")

        return AnsibleStateManagement(
            state_type="check_mode" if supports_check_mode else "comparison",
            state_location="module_params",
            idempotency_support=True,
            rollback_support=False,
            state_validation_steps=validation_steps,
            supports_check_mode=supports_check_mode,
            tracks_changed=tracks_changed,
        )

    def extract_dependencies(self, content: str) -> List[str]:
        """Extract module dependencies"""
        deps = []

        # Extract Python imports
        import_pattern = r"(?:from|import)\s+([\w\.]+)"
        for match in re.finditer(import_pattern, content):
            module = match.group(1).split(".")[0]
            # Filter out standard library and ansible internals
            if module not in [
                "json",
                "os",
                "sys",
                "re",
                "time",
                "ansible",
            ] and not module.startswith("_"):
                deps.append(module)

        # Extract from DOCUMENTATION requirements
        if "requirements:" in content:
            req_pattern = r"requirements:\s*\n((?:\s*-[^\n]+\n)+)"
            match = re.search(req_pattern, content)
            if match:
                req_text = match.group(1)
                for line in req_text.split("\n"):
                    line = line.strip()
                    if line.startswith("- "):
                        deps.append(line[2:].strip())

        # Add AWS-related if using boto3
        if "boto3" in content or "botocore" in content:
            if "boto3" not in deps:
                deps.append("boto3")
            if "botocore" not in deps:
                deps.append("botocore")

        # Identify AWS module utils
        if "ansible.module_utils.aws" in content or "ansible.module_utils.ec2" in content:
            deps.append("ansible-aws-modules")

        return list(set(deps))  # Remove duplicates

    def extract_connection_requirements(self, content: str) -> List[ConnectionRequirement]:
        """Extract connection requirements"""
        reqs = []

        # AWS region requirement
        if "region" in content or "get_aws_connection_info" in content:
            reqs.append(
                ConnectionRequirement(
                    requirement_type="aws_config",
                    description="AWS region configuration",
                    validation_steps=[
                        "Check AWS_REGION environment variable",
                        "Verify region parameter",
                    ],
                )
            )

        # Custom endpoint
        if "endpoint_url" in content:
            reqs.append(
                ConnectionRequirement(
                    requirement_type="endpoint",
                    description="Custom endpoint URL support",
                    validation_steps=["Verify endpoint URL is reachable", "Check SSL certificates"],
                )
            )

        # VPC/Network requirements
        if "vpc" in content.lower() or "subnet" in content or "security_group" in content:
            reqs.append(
                ConnectionRequirement(
                    requirement_type="network",
                    description="VPC and network configuration",
                    validation_steps=["Verify VPC connectivity", "Check security group rules"],
                )
            )

        return reqs

    def extract_documentation_block(self, content: str) -> Optional[Dict]:
        """Extract and parse DOCUMENTATION block"""
        # Handle triple quotes properly
        pattern = r'DOCUMENTATION\s*=\s*[r]?"""(.*?)"""'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            try:
                return yaml.safe_load(match.group(1))
            except yaml.YAMLError:
                return None
        return None

    def extract_examples_block(self, content: str) -> Optional[str]:
        """Extract EXAMPLES block"""
        pattern = r'EXAMPLES\s*=\s*[r]?"""(.*?)"""'
        match = re.search(pattern, content, re.DOTALL)
        return match.group(1) if match else None

    def extract_return_block(self, content: str) -> Optional[Dict]:
        """Extract and parse RETURN block"""
        pattern = r'RETURN\s*=\s*[r]?"""(.*?)"""'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            try:
                return yaml.safe_load(match.group(1))
            except yaml.YAMLError:
                return None
        return None
