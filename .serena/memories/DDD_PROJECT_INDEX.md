# DDD Framework - Complete Project Index
Generated: 2025-09-05
Status: Comprehensive documentation map with cross-references

## 📚 Documentation Structure

### Primary Documentation
- **README.md**: High-level overview and quick start guide
- **CLAUDE.md**: Development guidance for AI-assisted coding
- **docs/**: Sphinx-generated HTML documentation (when built)

### Project Memories (Serena)
35 memories organized by category:
- **Core**: DDD_CORE_PRINCIPLES, DDD_MISSION_AND_VISION
- **Architecture**: DDD_COMPLETE_EXTRACTOR_ARCHITECTURE, DDD_AST_ARCHITECTURE_DECISION
- **TDD Process**: DDD_TDD_RED_PHASE_COMPLETE, DDD_TDD_GREEN_PHASE_COMPLETE, DDD_REFACTOR_PHASE_COMPLETE
- **Implementation**: DDD_ANSIBLE_PATTERNS_CRITICAL, DDD_TECHNICAL_DISCOVERIES
- **Testing**: DDD_MVP_TEST_SUITE_COMPREHENSIVE, DDD_TEST_STRATEGY_MVP
- **Sessions**: DDD_CURRENT_STATE, DDD_SESSION_2025_09_04_REFACTOR

## 🏗️ Architecture Components

### Core Framework (`src/ddd/`)

#### 1. Coverage System (`coverage/`)
- **DocumentationCoverage**: Main coverage calculator
  - `measure()`: Calculate 3-tier coverage (Element/Completeness/Usefulness)
  - `assert_coverage()`: Validate against thresholds
- **CoverageResult**: Coverage metrics container

#### 2. Specification System (`specs/`)
- **DAYLIGHTSpec**: 8-dimension documentation requirements
  - Dependencies, Automation, Yearbook, Lifecycle
  - Integration, Governance, Health, Testing
- **DimensionSpec**: Individual dimension specifications

#### 3. Extraction System (`extractors/`)
- **DependencyExtractor**: JavaScript/Python dependency extraction
- **AdvancedAnsibleExtractor**: AST-based Ansible extraction (458 lines)
  - `extract_permissions()`: AWS IAM permissions
  - `extract_error_patterns()`: Error recovery hints
  - `extract_parameter_constraints()`: Parameter validation

#### 4. Generation System (`generators/`)
- **SphinxDocumentationGenerator**: HTML doc generation (447 lines)
  - `generate_module_documentation()`: Per-module docs
  - `generate_coverage_report()`: Coverage visualization
  - `build_html()`: Sphinx HTML compilation

#### 5. Artifact Extraction (`artifact_extractors/`)
- **InfrastructureExtractor**: Abstract base class (Template Method pattern)
- **AnsibleModuleExtractor**: Basic Ansible implementation
- **PythonArtifactExtractor**: Python code artifact extraction
- **JavaScriptArtifactExtractor**: JavaScript code artifact extraction

#### 6. Configuration Analysis (`config_extractors/`)
- **ConfigurationExtractor**: Configuration coverage analysis
- **ConfigCoverageCalculator**: Configuration completeness metrics

### CLI Interface (`src/cli.py`)
Commands:
- `measure`: Analyze documentation coverage
- `assert-coverage`: Validate coverage thresholds
- `demo`: Run configuration coverage demo
- `measure-artifacts`: Code artifact documentation
- `config-coverage`: Configuration documentation analysis

## 🧪 Test Infrastructure

### Test Organization (`tests/`)
- **150+ tests** across 8 test files
- **91.3% pass rate** (137/150 passing)
- **conftest.py**: 25+ centralized fixtures
- **helpers.py**: Test utilities and generators

### TDD Implementation (RED→GREEN→REFACTOR)
- **red_phase/**: Requirements tests
  - `test_core_extraction.py`
  - `test_permission_extraction.py`
  - `test_error_patterns.py`
- **Unit tests**: Component-level testing
- **Integration tests**: System-level validation

## 📊 Key Metrics & Performance

### Coverage Metrics
- **Baseline Coverage**: 37.9% (actual ~23% with bug)
- **Target Threshold**: 85% for production readiness
- **3-Tier Weighting**: Element (30%), Completeness (40%), Usefulness (30%)

### Performance Targets
- **Extraction Speed**: <1 second per module
- **Memory Usage**: <100MB for extraction
- **CLI Response**: <5 seconds for typical projects

## 🔄 Development Workflow

### Commands Reference
```bash
# Setup & Development
uv run invoke setup          # Complete dev setup
uv run invoke format         # Format with black/ruff
uv run invoke test           # Run all tests
uv run invoke test --critical # Critical tests only
uv run invoke docs --live    # Live documentation

# DDD Operations
uv run ddd measure ./path    # Measure coverage
uv run ddd assert-coverage   # Assert thresholds
uv run ddd config-coverage   # Config documentation
uv run ddd demo             # Run demo

# Testing
uv run pytest               # All tests
uv run pytest --cov=src     # Coverage report
```

## 🎯 Value Proposition

### Problem
- Maintenance teams inherit code without documentation
- No systematic way to measure "maintenance readiness"
- Documentation treated as afterthought

### Solution
- Apply TDD principles to documentation
- Measurable coverage targets (85% threshold)
- Automated extraction and generation

### Proof Points
- Ansible: 97% parameter docs but only 37% maintenance docs
- Extract 100% AWS IAM permissions automatically
- Generate maintenance runbooks with error recovery

## 🚀 Roadmap & Extensions

### Current MVP
- ✅ Ansible extractor with AST parsing
- ✅ Sphinx documentation generation
- ✅ 3-tier coverage measurement
- ⚠️ False positive bug (inflates ~30-40%)

### Future Extensions
- Terraform extractor (provider permissions, state)
- Kubernetes extractor (RBAC, health checks)
- Shell script analysis (Unix permissions, error codes)
- Docker analysis (ports, volumes, health)

## 📝 Known Issues & Limitations

1. **False Positive Bug**: Empty dimensions score 70% instead of 0%
2. **Language-Specific Specs**: Need language-aware dimension requirements
3. **Mock Safety**: Mock requires spec parameter for 'assert' methods

## 🔗 Cross-References

### Architecture Decisions
- AST over Regex (see: DDD_AST_ARCHITECTURE_DECISION)
- Template Method pattern (see: DDD_PATTERN_BASED_ARCHITECTURE)
- Plugin architecture (see: DDD_COMPLETE_EXTRACTOR_ARCHITECTURE)

### Implementation Guides
- Extractor development (see: DDD_EXTRACTOR_IMPLEMENTATION_GUIDE)
- Test strategy (see: DDD_TEST_STRATEGY_MVP)
- Maintenance scenarios (see: DDD_MAINTENANCE_SCENARIOS)