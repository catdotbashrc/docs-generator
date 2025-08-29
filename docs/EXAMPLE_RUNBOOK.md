# Example: Auto-Generated Maintenance Runbook

*This is an actual example of documentation that DDD extracts from Ansible code*

## Source: EC2 Instance Management Playbook

### What DDD Found Automatically

#### Required AWS IAM Permissions
Extracted from boto3 API calls in the code:
```
ec2:DescribeInstances
ec2:RunInstances
ec2:TerminateInstances
ec2:DescribeSecurityGroups
ec2:AuthorizeSecurityGroupIngress
iam:PassRole
```

**How this helps**: Operations team knows exactly what IAM permissions to grant, preventing "Access Denied" errors during deployment.

#### Error Patterns Detected
Found in exception handling blocks:
```python
# From the actual code:
except ClientError as e:
    if e.response['Error']['Code'] == 'InsufficientInstanceCapacity':
        # Retry in different AZ
```

**Generated Documentation**:
- **Error**: InsufficientInstanceCapacity
- **Recovery**: Retry in different availability zone
- **Source**: Lines 45-48 in ec2_deploy.py

#### State Management Information
Extracted from module implementation:
- **Idempotent**: Yes (checked via instance tags)
- **Check Mode**: Supported (--check flag works)
- **Rollback**: Manual (no automatic rollback detected)

#### Dependencies Found
From import statements and requirements:
```
boto3>=1.26.0
botocore>=1.29.0
ansible>=2.9
python>=3.8
```

### Before DDD vs After DDD

#### Before (Manual Documentation)
```markdown
# Deploy Script
Deploys stuff to AWS.
Contact Joe if it breaks (Joe left 6 months ago).
```

#### After (DDD-Generated)
```markdown
# EC2 Instance Management Runbook

## Quick Troubleshooting
If deployment fails, check:
1. IAM permissions (need ec2:RunInstances)
2. Instance capacity in target AZ
3. Security group exists
4. AMI is available in region

## Required Setup
- AWS credentials configured
- boto3 >= 1.26.0 installed
- Target VPC and subnet specified

## Common Issues
- InsufficientInstanceCapacity: Try us-east-1b if us-east-1a fails
- RequestLimitExceeded: Implement exponential backoff
- InvalidAMIID: Verify AMI exists in target region
```

### Real Coverage Metrics

Running `ddd measure` on this Ansible playbook:

```
Dependencies:     80% (found Python deps, missing Ansible Galaxy deps)
Automation:       60% (found some scripts, missing CI/CD config)
Yearbook:         40% (has git history, missing CHANGELOG)
Lifecycle:        70% (found dev/prod configs, missing staging)
Integration:      50% (found AWS endpoints, missing webhook docs)
Governance:       30% (missing security policies)
Health:           20% (no monitoring setup documented)
Testing:          60% (found test commands, missing coverage reports)

Overall: 51.25% - Below 85% threshold ❌
```

### What This Demonstrates

1. **DDD extracts real, verifiable information** from code
2. **Coverage scores are calculated** based on actual findings
3. **Gaps are clearly identified** for improvement
4. **No assumptions or guesses** - only what's in the code

### The Value Is Clear

- **Without DDD**: New team member reads "Deploy stuff to AWS"
- **With DDD**: New team member has permissions, error handling, dependencies

This isn't hypothetical - this is what DDD does today with the MVP.