"""
Unit tests for Ansible Module Extractor

Following TDD: RED phase - write failing tests for Ansible-specific implementation
Tests both the abstract contract fulfillment and Ansible-specific features
"""

from pathlib import Path
from textwrap import dedent
from typing import List

import pytest

from ddd.artifact_extractors.ansible_extractor import (
    AnsibleModuleExtractor,
    AnsibleStateManagement,
    AWSIAMPermission,
)

# These imports will fail initially (RED phase)
from ddd.artifact_extractors.base import (
    ErrorPattern,
    InfrastructureExtractor,
    MaintenanceDocument,
    PermissionRequirement,
    StateManagement,
)


class TestAnsibleModuleExtractor:
    """Test Ansible-specific extractor implementation"""

    def test_ansible_extractor_inherits_from_base(self):
        """Ansible extractor should inherit from InfrastructureExtractor"""
        assert issubclass(AnsibleModuleExtractor, InfrastructureExtractor)

    def test_ansible_extractor_can_be_instantiated(self):
        """Should be able to create AnsibleModuleExtractor instance"""
        extractor = AnsibleModuleExtractor()
        assert isinstance(extractor, InfrastructureExtractor)
        assert isinstance(extractor, AnsibleModuleExtractor)


class TestAWSIAMPermission:
    """Test AWS IAM permission implementation for Ansible"""

    def test_iam_permission_creation(self):
        """Should create IAM permission with service and action"""
        perm = AWSIAMPermission(service="ec2", action="DescribeInstances")
        assert perm.service == "ec2"
        assert perm.action == "DescribeInstances"

    def test_iam_permission_to_maintenance_doc(self):
        """Should format permission for maintenance documentation"""
        perm = AWSIAMPermission(service="ec2", action="TerminateInstances")
        doc = perm.to_maintenance_doc()

        assert "ec2:TerminateInstances" in doc
        assert isinstance(doc, str)

    def test_iam_permission_diagnostic_steps(self):
        """Should provide AWS-specific diagnostic steps"""
        perm = AWSIAMPermission(service="s3", action="GetObject")
        steps = perm.get_diagnostic_steps()

        assert len(steps) > 0
        assert any("IAM" in step for step in steps)
        assert any("policy" in step.lower() for step in steps)

    def test_iam_permission_from_boto3_call(self):
        """Should create permission from boto3 method call"""
        perm = AWSIAMPermission.from_boto3_call("ec2", "describe_instances")

        assert perm.service == "ec2"
        assert perm.action == "DescribeInstances"  # Should convert to PascalCase

    def test_iam_permission_equality(self):
        """Should compare permissions correctly"""
        perm1 = AWSIAMPermission("ec2", "DescribeInstances")
        perm2 = AWSIAMPermission("ec2", "DescribeInstances")
        perm3 = AWSIAMPermission("ec2", "TerminateInstances")

        assert perm1 == perm2
        assert perm1 != perm3


class TestAnsiblePermissionExtraction:
    """Test permission extraction from Ansible modules"""

    def test_extract_boto3_client_permissions(self):
        """Should extract permissions from boto3 client calls"""
        content = dedent(
            """
            import boto3

            def main():
                client = boto3.client('ec2')
                instances = client.describe_instances()
                client.terminate_instances(InstanceIds=['i-123'])
        """
        )

        extractor = AnsibleModuleExtractor()
        permissions = extractor.extract_permissions(content)

        assert len(permissions) == 2
        assert any(p.action == "DescribeInstances" for p in permissions)
        assert any(p.action == "TerminateInstances" for p in permissions)

    def test_extract_resource_permissions(self):
        """Should extract permissions from boto3 resource calls"""
        content = dedent(
            """
            import boto3

            def main():
                s3 = boto3.resource('s3')
                bucket = s3.Bucket('my-bucket')
                bucket.upload_file('local.txt', 'remote.txt')
        """
        )

        extractor = AnsibleModuleExtractor()
        permissions = extractor.extract_permissions(content)

        assert len(permissions) > 0
        assert any("s3" in p.service for p in permissions)

    def test_extract_multiple_service_permissions(self):
        """Should handle multiple AWS services"""
        content = dedent(
            """
            import boto3

            ec2 = boto3.client('ec2')
            s3 = boto3.client('s3')
            iam = boto3.client('iam')

            ec2.describe_instances()
            s3.list_buckets()
            iam.list_users()
        """
        )

        extractor = AnsibleModuleExtractor()
        permissions = extractor.extract_permissions(content)

        services = {p.service for p in permissions}
        assert "ec2" in services
        assert "s3" in services
        assert "iam" in services

    def test_no_duplicate_permissions(self):
        """Should not return duplicate permissions"""
        content = dedent(
            """
            client = boto3.client('ec2')
            client.describe_instances()
            client.describe_instances()  # Called twice
            client.describe_instances()  # Called three times
        """
        )

        extractor = AnsibleModuleExtractor()
        permissions = extractor.extract_permissions(content)

        describe_perms = [p for p in permissions if p.action == "DescribeInstances"]
        assert len(describe_perms) == 1  # Should deduplicate


class TestAnsibleErrorPatternExtraction:
    """Test error pattern extraction from Ansible modules"""

    def test_extract_module_fail_json(self):
        """Should extract module.fail_json patterns"""
        content = dedent(
            """
            if not instance_id:
                module.fail_json(msg="instance_id is required")

            if state not in ['present', 'absent']:
                module.fail_json(msg="Invalid state: %s" % state)
        """
        )

        extractor = AnsibleModuleExtractor()
        patterns = extractor.extract_error_patterns(content)

        assert len(patterns) >= 2
        assert any("instance_id is required" in p.pattern for p in patterns)
        assert any(p.error_type == "validation" for p in patterns)

    def test_extract_exception_handling(self):
        """Should extract exception handling patterns"""
        content = dedent(
            """
            try:
                response = client.describe_instances()
            except ClientError as e:
                module.fail_json(msg="Failed to describe instances: %s" % e)
            except BotoCoreError as e:
                module.fail_json(msg="AWS connection error: %s" % e)
        """
        )

        extractor = AnsibleModuleExtractor()
        patterns = extractor.extract_error_patterns(content)

        assert any("ClientError" in p.pattern for p in patterns)
        assert any("BotoCoreError" in p.pattern for p in patterns)
        assert any(p.error_type == "aws_error" for p in patterns)

    def test_extract_retry_patterns(self):
        """Should identify retry logic"""
        content = dedent(
            """
            @AWSRetry.exponential_backoff()
            def describe_with_retry():
                return client.describe_instances()

            for attempt in range(max_retries):
                try:
                    result = client.get_object()
                    break
                except ClientError:
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(2 ** attempt)
        """
        )

        extractor = AnsibleModuleExtractor()
        patterns = extractor.extract_error_patterns(content)

        assert any(p.error_type == "retry" for p in patterns)
        assert any("exponential_backoff" in p.pattern for p in patterns)


class TestAnsibleStateManagement:
    """Test state management extraction for Ansible"""

    def test_extract_check_mode_support(self):
        """Should detect check mode support"""
        content = dedent(
            """
            module = AnsibleModule(
                argument_spec=dict(
                    state=dict(default='present', choices=['present', 'absent'])
                ),
                supports_check_mode=True
            )

            if module.check_mode:
                module.exit_json(changed=True)
        """
        )

        extractor = AnsibleModuleExtractor()
        state = extractor.extract_state_management(content)

        assert state is not None
        assert state.idempotency_support is True
        assert "check_mode" in state.state_type

    def test_extract_changed_tracking(self):
        """Should detect changed state tracking"""
        content = dedent(
            """
            changed = False

            if current_state != desired_state:
                apply_changes()
                changed = True

            module.exit_json(changed=changed, instance=result)
        """
        )

        extractor = AnsibleModuleExtractor()
        state = extractor.extract_state_management(content)

        assert state is not None
        assert state.idempotency_support is True
        assert any("changed" in step.lower() for step in state.state_validation_steps)

    def test_extract_state_comparison(self):
        """Should detect state comparison logic"""
        content = dedent(
            """
            current_tags = instance.get('Tags', {})
            desired_tags = module.params.get('tags', {})

            if current_tags != desired_tags:
                update_tags(instance_id, desired_tags)
                changed = True
        """
        )

        extractor = AnsibleModuleExtractor()
        state = extractor.extract_state_management(content)

        assert state is not None
        assert any("current" in step.lower() for step in state.state_validation_steps)
        assert any(
            "compare" in step.lower() or "desired" in step.lower()
            for step in state.state_validation_steps
        )


class TestAnsibleDependencyExtraction:
    """Test dependency extraction from Ansible modules"""

    def test_extract_python_imports(self):
        """Should extract Python library dependencies"""
        content = dedent(
            """
            import json
            import boto3
            from botocore.exceptions import ClientError, BotoCoreError
            from ansible.module_utils.basic import AnsibleModule
            from ansible.module_utils.ec2 import boto3_conn
            import requests
        """
        )

        extractor = AnsibleModuleExtractor()
        deps = extractor.extract_dependencies(content)

        assert "boto3" in deps
        assert "botocore" in deps
        assert "requests" in deps
        # Standard library and ansible internals might be filtered

    def test_extract_requirements_from_documentation(self):
        """Should extract requirements from DOCUMENTATION block"""
        content = dedent(
            '''
            DOCUMENTATION = """
            module: ec2_instance
            requirements:
                - boto3 >= 1.16.0
                - botocore >= 1.19.0
            """
        '''
        )

        extractor = AnsibleModuleExtractor()
        deps = extractor.extract_dependencies(content)

        assert any("boto3" in d for d in deps)
        assert any("1.16.0" in d for d in deps)

    def test_extract_ansible_module_utils(self):
        """Should identify ansible module utilities used"""
        content = dedent(
            """
            from ansible.module_utils.basic import AnsibleModule
            from ansible.module_utils.aws.core import AnsibleAWSModule
            from ansible.module_utils.ec2 import boto3_conn, get_aws_connection_info
        """
        )

        extractor = AnsibleModuleExtractor()
        deps = extractor.extract_dependencies(content)

        # Should identify AWS-related module utils
        assert any("aws" in d.lower() or "ec2" in d.lower() for d in deps)


class TestAnsibleConnectionRequirements:
    """Test connection requirement extraction"""

    def test_extract_aws_region_requirement(self):
        """Should detect AWS region requirements"""
        content = dedent(
            """
            region, ec2_url, aws_connect_params = get_aws_connection_info(module, boto3=True)
            client = boto3_conn(module, conn_type='client', resource='ec2',
                               region=region, endpoint=ec2_url, **aws_connect_params)
        """
        )

        extractor = AnsibleModuleExtractor()
        reqs = extractor.extract_connection_requirements(content)

        assert any("region" in r.description.lower() for r in reqs)
        assert any(r.requirement_type == "aws_config" for r in reqs)

    def test_extract_endpoint_requirements(self):
        """Should detect custom endpoint requirements"""
        content = dedent(
            """
            if module.params.get('endpoint_url'):
                client = boto3.client('s3', endpoint_url=module.params['endpoint_url'])
        """
        )

        extractor = AnsibleModuleExtractor()
        reqs = extractor.extract_connection_requirements(content)

        assert any("endpoint" in r.description.lower() for r in reqs)

    def test_extract_vpc_requirements(self):
        """Should detect VPC/network requirements"""
        content = dedent(
            """
            vpc_id = module.params.get('vpc_id')
            subnet_id = module.params.get('subnet_id')
            security_groups = module.params.get('security_groups', [])
        """
        )

        extractor = AnsibleModuleExtractor()
        reqs = extractor.extract_connection_requirements(content)

        assert any(
            "vpc" in r.description.lower() or "network" in r.description.lower() for r in reqs
        )


class TestAnsibleMaintenanceScenarios:
    """Test maintenance scenario generation for Ansible"""

    def test_generate_aws_permission_scenario(self):
        """Should generate AWS-specific permission troubleshooting"""
        test_file = Path("/tmp/test_ansible.py")
        test_file.write_text(
            dedent(
                """
            import boto3
            client = boto3.client('ec2')
            client.describe_instances()
            client.terminate_instances()
        """
            )
        )

        extractor = AnsibleModuleExtractor()
        doc = extractor.extract(test_file)

        perm_scenarios = [s for s in doc.maintenance_scenarios if "permission" in s.name]
        assert len(perm_scenarios) > 0

        scenario = perm_scenarios[0]
        assert any("IAM" in step for step in scenario.diagnostic_steps)
        assert any("policy" in step.lower() for step in scenario.resolution_steps)

        test_file.unlink()

    def test_generate_ansible_specific_scenarios(self):
        """Should include Ansible-specific troubleshooting"""
        test_file = Path("/tmp/test_ansible2.py")
        test_file.write_text(
            dedent(
                """
            module = AnsibleModule(
                supports_check_mode=True
            )

            try:
                client = boto3.client('ec2')
            except ClientError as e:
                module.fail_json(msg=str(e))
        """
            )
        )

        extractor = AnsibleModuleExtractor()
        doc = extractor.extract(test_file)

        # Should have scenarios for both AWS errors and Ansible features
        assert len(doc.maintenance_scenarios) > 0
        assert any(
            "AWS" in s.trigger or "permission" in s.trigger for s in doc.maintenance_scenarios
        )

        test_file.unlink()


class TestAnsibleDocumentationBlocks:
    """Test extraction of Ansible DOCUMENTATION blocks"""

    def test_extract_documentation_block(self):
        """Should extract and parse DOCUMENTATION YAML"""
        content = dedent(
            '''
            DOCUMENTATION = """
            module: ec2_instance
            short_description: Create & manage EC2 instances
            version_added: "2.5"
            options:
              instance_id:
                description: Instance ID to manage
                required: false
                type: str
              state:
                description: Goal state for the instance
                choices: [present, absent, stopped, running]
                default: present
            requirements:
              - boto3 >= 1.16.0
            """
        '''
        )

        extractor = AnsibleModuleExtractor()
        doc_block = extractor.extract_documentation_block(content)

        assert doc_block is not None
        assert doc_block.get("module") == "ec2_instance"
        assert "options" in doc_block
        assert "instance_id" in doc_block["options"]

    def test_extract_examples_block(self):
        """Should extract EXAMPLES block"""
        content = dedent(
            '''
            EXAMPLES = """
            - name: Launch EC2 instance
              ec2_instance:
                instance_id: i-1234567
                state: present
                region: us-east-1
            """
        '''
        )

        extractor = AnsibleModuleExtractor()
        examples = extractor.extract_examples_block(content)

        assert examples is not None
        assert "Launch EC2 instance" in examples
        assert "ec2_instance:" in examples

    def test_extract_return_block(self):
        """Should extract and parse RETURN block"""
        content = dedent(
            '''
            RETURN = """
            instance:
                description: Details about the instance
                type: dict
                returned: success
                sample: {
                    "instance_id": "i-1234567",
                    "state": "running"
                }
            changed:
                description: Whether the module changed anything
                type: bool
                returned: always
            """
        '''
        )

        extractor = AnsibleModuleExtractor()
        return_block = extractor.extract_return_block(content)

        assert return_block is not None
        assert "instance" in return_block
        assert "changed" in return_block
        assert return_block["instance"]["type"] == "dict"
