#!/usr/bin/env python3
"""
RED Phase Tests: Error Pattern Detection Requirements
These tests define HOW we want to extract error patterns for maintenance runbooks.
They will FAIL until we implement the error detection logic.
"""

import pytest

# This import will fail initially - that's the RED phase!
from ddd.extractors.ansible_advanced import AdvancedAnsibleExtractor


class TestErrorPatternRequirements:
    """Define how error patterns must be detected for maintenance."""

    def test_extract_explicit_error_messages(self):
        """Must extract all module.fail_json() calls."""
        content = """
def main():
    module = AnsibleModule(...)
    
    if not os.path.exists(path):
        module.fail_json(msg="Path does not exist: %s" % path)
    
    if not os.access(path, os.W_OK):
        module.fail_json(msg="Path is not writable: %s" % path)
    
    try:
        result = some_operation()
    except Exception as e:
        module.fail_json(msg="Operation failed: %s" % str(e), exception=traceback.format_exc())
"""
        extractor = AdvancedAnsibleExtractor()
        errors = extractor.extract_error_patterns(content)

        assert len(errors) >= 3

        # Find specific error patterns
        path_not_exist = next(e for e in errors if "Path does not exist" in e.message)
        assert path_not_exist.condition == "not os.path.exists(path)"
        assert path_not_exist.recovery_hint == "Ensure the path exists before running the module"

        not_writable = next(e for e in errors if "not writable" in e.message)
        assert not_writable.condition == "not os.access(path, os.W_OK)"
        assert not_writable.recovery_hint == "Check file permissions and ownership"

        operation_failed = next(e for e in errors if "Operation failed" in e.message)
        assert operation_failed.includes_traceback is True
        assert operation_failed.error_type == "exception"

    def test_extract_validation_errors(self):
        """Must identify parameter validation patterns."""
        content = """
def main():
    module = AnsibleModule(
        argument_spec=dict(
            path=dict(required=True, type='path'),
            state=dict(choices=['present', 'absent'], default='present'),
            mode=dict(type='raw'),
        ),
        required_if=[
            ('state', 'present', ['path', 'mode']),
        ],
        mutually_exclusive=[
            ['source', 'content'],
        ],
    )
    
    # Custom validations
    if state == 'present' and not path:
        module.fail_json(msg="path is required when state=present")
    
    if mode and not isinstance(mode, str):
        module.fail_json(msg="mode must be a string or octal number")
    
    if age and age < 0:
        module.fail_json(msg="age must be a positive number")
"""
        extractor = AdvancedAnsibleExtractor()
        errors = extractor.extract_error_patterns(content)
        validations = [e for e in errors if e.type == "validation"]

        assert len(validations) >= 3

        # Should extract parameter constraints
        constraints = extractor.extract_parameter_constraints(content)
        assert constraints["state"]["choices"] == ["present", "absent"]
        assert constraints["path"]["required"] is True
        assert "required_if" in constraints
        assert "mutually_exclusive" in constraints

    def test_extract_exception_handling(self):
        """Must detect try/except patterns for error scenarios."""
        content = """
try:
    import boto3
    ec2 = boto3.client('ec2')
except ImportError as e:
    module.fail_json(msg="boto3 is required for this module", exception=str(e))

try:
    response = ec2.describe_instances(InstanceIds=[instance_id])
except ClientError as e:
    error_code = e.response['Error']['Code']
    if error_code == 'InvalidInstanceID.NotFound':
        module.fail_json(msg="Instance %s not found" % instance_id)
    elif error_code == 'UnauthorizedOperation':
        module.fail_json(msg="Insufficient permissions to describe instances")
    else:
        module.fail_json(msg="AWS API error: %s" % str(e))
except BotoCoreError as e:
    module.fail_json(msg="AWS connection error: %s" % str(e))
"""
        extractor = AdvancedAnsibleExtractor()
        errors = extractor.extract_error_patterns(content)
        exception_handlers = [e for e in errors if e.type == "exception"]

        # Should categorize different exception types
        import_error = next(e for e in exception_handlers if e.exception_type == "ImportError")
        assert "boto3 is required" in import_error.message
        assert import_error.recovery_hint == "Install boto3: pip install boto3"

        client_errors = [e for e in exception_handlers if e.exception_type == "ClientError"]
        assert len(client_errors) >= 3  # NotFound, Unauthorized, generic

        # Should extract error codes
        not_found = next(e for e in client_errors if "InvalidInstanceID.NotFound" in e.error_code)
        assert "not found" in not_found.message.lower()

        unauthorized = next(e for e in client_errors if "UnauthorizedOperation" in e.error_code)
        assert "permissions" in unauthorized.message.lower()
        assert unauthorized.recovery_hint == "Check IAM permissions for ec2:DescribeInstances"

    def test_extract_retry_patterns(self):
        """Must detect retry and backoff patterns."""
        content = """
from ansible.module_utils.aws.core import AWSRetry

@AWSRetry.jittered_backoff()
def describe_instances_with_retry(ec2_client, instance_ids):
    return ec2_client.describe_instances(InstanceIds=instance_ids)

# Manual retry pattern
max_retries = 3
for attempt in range(max_retries):
    try:
        result = perform_operation()
        break
    except TemporaryError as e:
        if attempt == max_retries - 1:
            module.fail_json(msg="Operation failed after %d retries" % max_retries)
        time.sleep(2 ** attempt)  # Exponential backoff
"""
        extractor = AdvancedAnsibleExtractor()
        errors = extractor.extract_error_patterns(content)

        # Should detect retry decorators
        retry_patterns = extractor.extract_retry_patterns(content)
        assert any("AWSRetry.jittered_backoff" in p for p in retry_patterns)

        # Should detect manual retry loops
        assert any("max_retries" in p for p in retry_patterns)

        # Should extract retry configuration
        retry_config = extractor.extract_retry_configuration(content)
        assert retry_config["max_retries"] == 3
        assert retry_config["backoff_strategy"] == "exponential"
        assert retry_config["retriable_errors"] == ["TemporaryError"]

    def test_extract_error_recovery_steps(self):
        """Must generate actionable recovery steps for each error."""
        content = """
if not shutil.which('git'):
    module.fail_json(msg="git is not installed")

if not os.path.exists('/etc/app/config.yml'):
    module.fail_json(msg="Configuration file not found at /etc/app/config.yml")

try:
    requests.get('https://api.example.com/health')
except requests.ConnectionError:
    module.fail_json(msg="Cannot connect to API at api.example.com")
"""
        extractor = AdvancedAnsibleExtractor()
        errors = extractor.extract_error_patterns(content)

        # Each error should have recovery steps
        git_error = next(e for e in errors if "git" in e.message)
        assert (
            "apt-get install git" in git_error.recovery_hint
            or "yum install git" in git_error.recovery_hint
        )

        config_error = next(e for e in errors if "config.yml" in e.message)
        assert "Create configuration file at /etc/app/config.yml" in config_error.recovery_hint

        connection_error = next(e for e in errors if "Cannot connect" in e.message)
        assert any(
            hint in connection_error.recovery_hint
            for hint in [
                "Check network connectivity",
                "Verify API endpoint",
                "Check firewall rules",
            ]
        )
