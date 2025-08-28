# DDD Framework Quick Start

## Installation

```bash
# Using uv (recommended)
uv venv
uv pip install -e .

# Using pip
pip install -e .
```

## Basic Usage

### 1. Measure Documentation Coverage

```bash
# Measure any project
ddd measure /path/to/project

# Save results to JSON
ddd measure /path/to/project -o coverage.json
```

### 2. Assert Coverage (CI/CD)

```bash
# Fail if coverage < 85% (default)
ddd assert-coverage /path/to/project

# Custom threshold
ddd assert-coverage /path/to/project --min-coverage 0.90
```

### 3. See the DDD Workflow

```bash
# RED → GREEN → REFACTOR demo
ddd demo /path/to/project
```

## Understanding Coverage

Documentation coverage measures three levels:

1. **Element Coverage (30%)**: Does the documentation exist?
2. **Completeness Coverage (40%)**: Are required fields present?
3. **Usefulness Coverage (30%)**: Can someone use this at 2AM?

## Example Output

```
📊 Measuring documentation coverage for my-project

✅ Documentation Coverage PASSED
Overall Coverage: 87.5%

Coverage by Dimension
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Dimension     Coverage   Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Dependencies     92%       ✅
Automation       85%       ✅
Yearbook         80%       ⚠️
Lifecycle        88%       ✅
```

## The DDD Philosophy

Just like TDD:
- **TDD**: Write tests → Code fails → Fix code → Tests pass
- **DDD**: Define doc spec → Docs incomplete → Extract docs → Coverage passes

## Current Status

This is an MVP focusing on:
- **Dependencies dimension** (fully implemented)
- Other dimensions have specs but simplified extractors
- Ansible serves as our baseline reference

## Next Steps

1. Implement extractors for all 8 DAYLIGHT dimensions
2. Add more language support (currently JS/Python)
3. Create CI/CD integrations
4. Build visual coverage reports