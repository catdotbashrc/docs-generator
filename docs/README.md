# DDD Framework Documentation

## Quick Links

- **[User Guide](USER_GUIDE.md)** - Getting started and CLI usage
- **[API Reference](API_REFERENCE.md)** - Complete API documentation
- **[DAYLIGHT Specification](DAYLIGHT_SPECIFICATION.md)** - The 8 dimensions of documentation coverage
- **[Development Guide](DEVELOPMENT_GUIDE.md)** - Contributing and creating extractors

## What is DDD?

Documentation Driven Development applies Test-Driven Development principles to documentation. Just as TDD ensures code quality through tests, DDD ensures maintenance readiness through measurable documentation coverage.

## Quick Start

```bash
# Install
uv pip install -e .

# Measure coverage
ddd measure ./my-project

# Assert in CI/CD
ddd assert-coverage ./my-project --threshold 0.85
```

## The Problem We Solve

At 2AM during an incident, ops teams need answers:
- What IAM permissions does this need?
- What can go wrong?
- How do I know if it's working?
- What does this depend on?

DDD automatically extracts this information and measures completeness.

## Documentation Structure

```
docs/
├── README.md                    # This file
├── USER_GUIDE.md               # Complete usage guide
├── API_REFERENCE.md            # API documentation
├── DAYLIGHT_SPECIFICATION.md   # Coverage framework spec
├── DEVELOPMENT_GUIDE.md        # Contributing guide
└── archive/                    # Historical documentation
    ├── research/               # Academic papers
    ├── case-studies/          # Implementation examples
    ├── historical/            # Previous versions
    └── legacy-specs/          # Old specifications
```

## Key Features

- **85% Coverage Threshold** - Measurable documentation quality
- **8 DAYLIGHT Dimensions** - Comprehensive coverage model
- **Auto-Extraction** - Generate docs from code automatically
- **CI/CD Ready** - Fail builds on insufficient documentation

## Current Status

- ✅ Python support (11 modules)
- ✅ Ansible IAM extraction
- ✅ Configuration discovery
- ✅ Coverage calculation engine
- 🚧 Terraform support (coming soon)
- 🚧 Kubernetes support (planned)

---

*Making maintenance documentation as tested as your code*