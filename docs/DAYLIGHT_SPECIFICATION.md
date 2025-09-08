# DAYLIGHT Framework Specification

## Overview

DAYLIGHT is a comprehensive framework for measuring documentation coverage across 8 critical maintenance dimensions. Each dimension represents essential knowledge needed for operations teams to maintain systems effectively.

**Core Principle**: Documentation should answer the questions ops teams ask at 2AM during incidents.

## The 8 DAYLIGHT Dimensions

### D - Dependencies
**What does this need to run?**

Required documentation:
- External service dependencies
- Package/library requirements  
- API dependencies and versions
- Infrastructure prerequisites

Coverage weight: 1.0 | Minimum threshold: 85%

### A - Automation
**How do I deploy and operate this?**

Required documentation:
- Deployment procedures
- Automation scripts/playbooks
- CI/CD pipeline configuration
- Operational runbooks

Coverage weight: 1.0 | Minimum threshold: 85%

### Y - Yearbook  
**Who owns this and why does it exist?**

Required documentation:
- Team ownership
- Business purpose
- Historical context
- Architectural decisions

Coverage weight: 0.8 | Minimum threshold: 75%

### L - Lifecycle
**How does this evolve?**

Required documentation:
- State transitions
- Data lifecycle
- Backup/restore procedures
- Upgrade/migration paths

Coverage weight: 1.0 | Minimum threshold: 80%

### I - Integration
**How does this connect to other systems?**

Required documentation:
- API endpoints
- Event streams
- Data flows
- Integration points

Coverage weight: 0.9 | Minimum threshold: 80%

### G - Governance
**What are the security and compliance requirements?**

Required documentation:
- IAM permissions required
- Security controls
- Compliance requirements
- Audit procedures

Coverage weight: 1.3 | Minimum threshold: 90%

### H - Health
**How do I know it's working?**

Required documentation:
- Health check endpoints
- Key metrics
- Alert thresholds
- Troubleshooting guides

Coverage weight: 1.0 | Minimum threshold: 85%

### T - Testing
**How do I verify it works correctly?**

Required documentation:
- Test procedures
- Validation scripts
- Expected behaviors
- Test data requirements

Coverage weight: 1.1 | Minimum threshold: 85%

## Coverage Calculation Model

### Three-Tier Measurement

Documentation coverage is measured at three levels:

1. **Element Coverage (30%)**: Does the documentation exist?
   - Binary check for presence of required elements
   - Score = (elements_present / elements_required)

2. **Completeness Coverage (40%)**: Are required fields populated?
   - Checks if documentation contains necessary details
   - Score = (fields_populated / fields_required)

3. **Usefulness Coverage (30%)**: Is it actionable at 2AM?
   - Validates practical usability during incidents
   - Score = (actionable_items / total_items)

### Overall Score Calculation

```python
dimension_score = (
    element_coverage * 0.3 +
    completeness_coverage * 0.4 +
    usefulness_coverage * 0.3
) * dimension_weight

overall_score = sum(dimension_scores) / sum(dimension_weights)
```

### Pass/Fail Criteria

- **Overall threshold**: 85% minimum
- **Per-dimension thresholds**: Specified above
- **Both must pass** for successful validation

## Implementation Requirements

### For Extractors

Each extractor must return documentation structured by DAYLIGHT dimensions:

```python
{
    "dependencies": {
        "packages": [...],
        "services": [...],
        "apis": [...]
    },
    "automation": {
        "deployment": "...",
        "scripts": [...]
    },
    "governance": {
        "permissions": ["iam:CreateRole", "s3:GetObject"],
        "security": {...}
    },
    # ... other dimensions
}
```

### For Coverage Validation

The coverage calculator:
1. Loads the DAYLIGHTSpec with dimension requirements
2. Evaluates extracted documentation against each dimension
3. Calculates three-tier scores per dimension
4. Applies dimension weights
5. Determines pass/fail status

## Practical Example

For an Ansible module managing EC2 instances:

```yaml
Dependencies:
  - boto3 >= 1.26.0
  - AWS credentials configured
  - VPC and subnet IDs

Automation:
  - Playbook: ec2_deploy.yml
  - Variables: instance_type, ami_id

Governance:
  - IAM Permissions:
    - ec2:RunInstances
    - ec2:TerminateInstances
    - ec2:DescribeInstances

Health:
  - Check: instance.state == 'running'
  - Metric: CPU utilization < 80%
  - Alert: Instance unreachable

Integration:
  - Output: instance_id, public_ip
  - Depends on: VPC module
  - Used by: Load balancer module
```

## Current Implementation Status

### Fully Implemented
- ✅ Dependencies dimension (Python, JavaScript)
- ✅ Governance dimension (IAM permissions)
- ✅ Configuration extraction
- ✅ Coverage calculation engine

### MVP Simplified
- ⚠️ Other dimensions have specs but basic extractors
- ⚠️ Ansible as reference implementation
- ⚠️ Limited language support

## Usage with DDD CLI

```bash
# Measure coverage against DAYLIGHT spec
ddd measure ./project

# Output shows per-dimension scores
✅ Dependencies: 92%
✅ Automation: 85%
⚠️ Yearbook: 72%
✅ Governance: 94%

Overall: 87.5% PASSED
```

## Future Enhancements

1. **More extractors**: Terraform, CloudFormation, Kubernetes
2. **Richer extraction**: Deeper AST analysis
3. **Custom dimensions**: Project-specific requirements
4. **IDE integration**: Real-time coverage feedback

---

*DAYLIGHT Framework v1.0 - Making maintenance documentation measurable*