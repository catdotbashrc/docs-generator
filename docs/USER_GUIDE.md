# DDD Framework User Guide

## Quick Start

### Installation

```bash
# Using uv (recommended)
uv venv
uv pip install -e .

# Using pip
pip install -e .
```

### Your First Coverage Check

```bash
# Measure any project's documentation coverage
ddd measure ./my-project

# You'll see output like:
📊 Documentation Coverage Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Overall Coverage: 87.5% ✅ PASSED

Dependencies    92% ✅
Automation      85% ✅  
Governance      94% ✅
Health          81% ⚠️
```

## Core Concepts

### What is Documentation Coverage?

Just like code coverage measures how much of your code is tested, documentation coverage measures how much of your maintenance knowledge is documented.

**The Problem**: At 2AM during an incident, ops teams need answers:
- What IAM permissions does this need?
- What can go wrong?
- How do I know if it's working?
- What does this depend on?

**The Solution**: DDD automatically extracts this information and measures completeness.

### The DAYLIGHT Dimensions

DDD measures documentation across 8 dimensions (DAYLIGHT):
- **D**ependencies - What does this need to run?
- **A**utomation - How do I deploy this?
- **Y**earbook - Who owns this and why?
- **L**ifecycle - How does this evolve?
- **I**ntegration - How does this connect?
- **G**overnance - What permissions/security?
- **H**ealth - How do I know it's working?
- **T**esting - How do I verify it works?

## CLI Commands

### measure - Check Documentation Coverage

```bash
# Basic measurement
ddd measure ./project

# Save results to JSON
ddd measure ./project --output coverage.json

# Verbose output with details
ddd measure ./project --verbose
```

### assert-coverage - CI/CD Integration

```bash
# Fail if coverage < 85% (default)
ddd assert-coverage ./project

# Custom threshold
ddd assert-coverage ./project --threshold 0.90

# Use in CI/CD pipeline
ddd assert-coverage . || exit 1
```

### config-coverage - Configuration Documentation

```bash
# Check configuration documentation specifically
ddd config-coverage ./project

# Shows extracted configs:
✅ Found 23 configuration parameters
⚠️ 5 sensitive values detected (masked)
📝 Environment variables documented: 18/23
```

### demo - See RED-GREEN-REFACTOR in Action

```bash
# Watch the TDD cycle for documentation
ddd demo ./project

# Shows:
🔴 RED: Documentation incomplete (65%)
🟢 GREEN: Extracting documentation...
♻️ REFACTOR: Optimizing quality...
✅ Coverage: 87% PASSED
```

## Configuration

### Project Configuration

Create `.ddd.yml` in your project root:

```yaml
# .ddd.yml
coverage:
  threshold: 0.85  # Minimum acceptable coverage
  weights:
    governance: 1.3  # Increase importance of security docs
    yearbook: 0.5    # Decrease importance of ownership docs

extractors:
  - ansible
  - python
  - config

output:
  format: json
  file: coverage.json
```

### Environment Variables

```bash
# Set default threshold
export DDD_COVERAGE_THRESHOLD=0.90

# Set output format
export DDD_OUTPUT_FORMAT=json

# Enable debug logging
export DDD_DEBUG=1
```

## Practical Examples

### Example 1: Python Project

```bash
$ ddd measure ./my-python-app

📊 Analyzing Python project...

✅ Extracted:
- 12 package dependencies
- 8 environment variables
- 15 error scenarios
- 3 API endpoints

Coverage by Dimension:
Dependencies    95% ✅ (pip requirements found)
Configuration   88% ✅ (env vars documented)
Governance      73% ⚠️ (missing IAM docs)

Overall: 85.3% ✅ PASSED
```

### Example 2: Ansible Playbook

```bash
$ ddd measure ./ansible-playbooks

📊 Analyzing Ansible playbooks...

✅ Extracted:
- 23 IAM permissions needed
- 5 AWS services used
- 8 error handlers
- 12 variables required

Coverage by Dimension:
Governance     98% ✅ (IAM permissions complete)
Automation     92% ✅ (playbooks documented)
Dependencies   89% ✅ (requirements specified)

Overall: 93.1% ✅ PASSED
```

### Example 3: CI/CD Pipeline Integration

```yaml
# .github/workflows/documentation.yml
name: Documentation Coverage

on: [push, pull_request]

jobs:
  coverage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Install DDD
        run: |
          pip install ddd-framework
      
      - name: Check Documentation Coverage
        run: |
          ddd assert-coverage . --threshold 0.85
```

## Understanding Coverage Scores

### Three Levels of Measurement

1. **Element Coverage (30%)**: Does it exist?
   - Binary check - documentation present or not

2. **Completeness (40%)**: Is it complete?
   - Required fields populated
   - No placeholders or TODOs

3. **Usefulness (30%)**: Can someone use it at 2AM?
   - Clear, actionable instructions
   - Examples and error handling

### Interpreting Results

- **90-100%**: Excellent - Production ready
- **85-90%**: Good - Meets standards  
- **75-85%**: Fair - Needs improvement
- **Below 75%**: Poor - Significant gaps

## Troubleshooting

### Common Issues

**No documentation found**
```bash
# Check supported file types
ddd measure . --verbose

# Ensure files aren't gitignored
git check-ignore your-file.py
```

**Coverage below threshold**
```bash
# See detailed breakdown
ddd measure . --verbose

# Focus on specific dimension
ddd measure . --dimension governance
```

**Extractor not recognizing patterns**
```bash
# Enable debug mode
DDD_DEBUG=1 ddd measure .

# Check extractor patterns
ddd show-patterns --extractor ansible
```

## Supported Languages & Frameworks

### Currently Supported
- ✅ **Python**: Dependencies, configs, error handling
- ✅ **JavaScript/Node**: package.json, configs
- ✅ **Ansible**: IAM permissions, AWS resources
- ✅ **Configuration files**: YAML, JSON, TOML, .env

### Coming Soon
- 🚧 Terraform
- 🚧 CloudFormation  
- 🚧 Kubernetes
- 🚧 Docker

## Best Practices

1. **Run in CI/CD**: Make documentation coverage a gate
2. **Start with 75%**: Gradually increase threshold
3. **Focus on Governance**: Security docs are critical
4. **Document configs**: Environment variables matter
5. **Update regularly**: Keep docs in sync with code

## Getting Help

```bash
# Show help
ddd --help

# Show version
ddd --version

# Enable debug output
DDD_DEBUG=1 ddd measure .
```

## Next Steps

1. [Read the API Reference](API_REFERENCE_UNIFIED.md) for programmatic usage
2. [See DAYLIGHT Specification](DAYLIGHT_SPECIFICATION.md) for dimension details
3. [Contributing Guide](DEVELOPMENT_GUIDE.md) to add extractors

---

*Make your documentation as tested as your code - maintain 85% coverage!*