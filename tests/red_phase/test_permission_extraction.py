#!/usr/bin/env python3
"""
RED Phase Tests: AWS IAM Permission Extraction Requirements
These tests define HOW we want to extract AWS permissions from boto3 calls.
They will FAIL until we implement the permission extraction logic.
"""

import pytest

# This import will fail initially - that's the RED phase!
from ddd.extractors.ansible_advanced import AdvancedAnsibleExtractor


class TestPermissionExtractionRequirements:
    """Define how AWS IAM permissions must be detected."""

    def test_extract_boto3_client_permissions(self):
        """Must detect all boto3 client method calls and map to IAM."""
        content = """
import boto3

def main():
    ec2_client = boto3.client('ec2')
    instances = ec2_client.describe_instances()
    ec2_client.terminate_instances(InstanceIds=ids)
    
    # Should also handle direct calls
    boto3.client('s3').list_buckets()
"""
        extractor = AdvancedAnsibleExtractor()
        permissions = extractor.extract_permissions(content)

        # Must find all permissions
        assert "ec2:DescribeInstances" in permissions
        assert "ec2:TerminateInstances" in permissions
        assert "s3:ListBuckets" in permissions

        # Must not have duplicates
        assert len(permissions) == len(set(permissions))

    def test_extract_boto3_resource_permissions(self):
        """Must handle boto3 resource API patterns."""
        content = """
import boto3

def main():
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('my-bucket')
    bucket.upload_file(local_file, key)
    
    # Table operations
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('my-table')
    table.put_item(Item={'id': '123'})
    table.get_item(Key={'id': '123'})
"""
        extractor = AdvancedAnsibleExtractor()
        permissions = extractor.extract_permissions(content)

        assert "s3:PutObject" in permissions
        assert "dynamodb:PutItem" in permissions
        assert "dynamodb:GetItem" in permissions

    def test_extract_service_specific_patterns(self):
        """Must handle service-specific permission patterns."""
        test_cases = [
            ("iam.create_role(RoleName='test')", ["iam:CreateRole"]),
            ("lambda_client.invoke(FunctionName='test')", ["lambda:InvokeFunction"]),
            ("sns.publish(TopicArn='arn')", ["sns:Publish"]),
            ("sqs.send_message(QueueUrl='url')", ["sqs:SendMessage"]),
            ("cloudformation.create_stack(StackName='test')", ["cloudformation:CreateStack"]),
            ("rds.create_db_instance()", ["rds:CreateDBInstance"]),
            ("ecs.run_task(taskDefinition='task')", ["ecs:RunTask"]),
        ]

        extractor = AdvancedAnsibleExtractor()

        for code, expected_permissions in test_cases:
            perms = extractor.extract_permissions(code)
            for expected_perm in expected_permissions:
                assert expected_perm in perms, f"Missing {expected_perm} from: {code}"

    def test_extract_complex_permission_chains(self):
        """Must detect permission dependencies and chains."""
        content = """
# Creating an EC2 instance requires multiple permissions
ec2.run_instances(ImageId='ami-123', MinCount=1, MaxCount=1)
ec2.create_tags(Resources=[instance_id], Tags=[{'Key': 'Name', 'Value': 'test'}])

# S3 operations often need multiple permissions
s3.put_object(Bucket='test', Key='file', ServerSideEncryption='AES256')
s3.put_object_acl(Bucket='test', Key='file', ACL='public-read')
"""
        extractor = AdvancedAnsibleExtractor()
        permissions = extractor.extract_permissions(content)

        # EC2 instance creation chain
        assert "ec2:RunInstances" in permissions
        assert "ec2:CreateTags" in permissions

        # S3 upload chain
        assert "s3:PutObject" in permissions
        assert "s3:PutObjectAcl" in permissions

        # Should detect encryption permissions
        assert extractor.detects_encryption_requirement(content) is True

    def test_extract_assume_role_permissions(self):
        """Must detect STS assume role patterns."""
        content = """
sts = boto3.client('sts')
assumed_role = sts.assume_role(
    RoleArn='arn:aws:iam::123456789012:role/MyRole',
    RoleSessionName='MySession'
)
"""
        extractor = AdvancedAnsibleExtractor()
        permissions = extractor.extract_permissions(content)

        assert "sts:AssumeRole" in permissions

        # Should also extract the role ARN for documentation
        role_requirements = extractor.extract_role_requirements(content)
        assert "arn:aws:iam::123456789012:role/MyRole" in role_requirements

    def test_extract_wildcard_permissions(self):
        """Must detect when wildcard permissions might be needed."""
        content = """
# Listing operations often need wildcards
ec2.describe_instances()  # Could be * or specific instance IDs
s3.list_objects_v2(Bucket='bucket', Prefix='path/')  # Needs path/*
"""
        extractor = AdvancedAnsibleExtractor()
        permission_details = extractor.extract_permission_details(content)

        # Should indicate resource constraints
        ec2_perm = next(p for p in permission_details if p["action"] == "ec2:DescribeInstances")
        assert ec2_perm["resource_constraint"] == "*" or ec2_perm["resource_constraint"] is None

        s3_perm = next(p for p in permission_details if p["action"] == "s3:ListBucket")
        assert "path/*" in s3_perm.get("condition", "") or s3_perm.get("requires_prefix") is True

    def test_permission_extraction_with_try_except(self):
        """Must extract permissions even when wrapped in error handling."""
        content = """
try:
    ec2.describe_instances()
    ec2.stop_instances(InstanceIds=ids)
except ClientError as e:
    if e.response['Error']['Code'] == 'UnauthorizedOperation':
        # This tells us what permission was missing!
        module.fail_json(msg="Missing EC2 permissions")
"""
        extractor = AdvancedAnsibleExtractor()
        permissions = extractor.extract_permissions(content)

        assert "ec2:DescribeInstances" in permissions
        assert "ec2:StopInstances" in permissions

        # Should also extract permission error patterns
        error_hints = extractor.extract_permission_errors(content)
        assert any("UnauthorizedOperation" in hint for hint in error_hints)
