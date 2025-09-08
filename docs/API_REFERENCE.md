# DDD Framework API Reference

## Overview

The DDD Framework provides extractors to automatically generate maintenance documentation from code. This API reference covers all implemented classes and methods.

## Core Modules

### DocumentationCoverage
**Module**: `ddd.coverage`

Main coverage calculator implementing the 3-tier measurement model.

```python
class DocumentationCoverage:
    def calculate(self, documentation: Dict, spec: DAYLIGHTSpec) -> CoverageResult:
        """Calculate documentation coverage against DAYLIGHT specifications"""
        # Returns CoverageResult with overall_score, dimension_scores, and pass/fail
```

**Key Methods:**
- `calculate()`: Compute coverage scores (element 30%, completeness 40%, usefulness 30%)
- Returns `CoverageResult` with score between 0.0-1.0

---

### Extractors

#### BaseExtractor
**Module**: `ddd.artifact_extractors.base`

Abstract base for all extractors.

```python
class BaseExtractor(ABC):
    @abstractmethod
    def extract(self, source: Union[str, Path]) -> Dict[str, Any]:
        """Extract documentation from source"""
```

#### AnsibleModuleExtractor  
**Module**: `ddd.artifact_extractors.ansible_extractor`

Extracts AWS IAM permissions from Ansible playbooks.

```python
class AnsibleModuleExtractor(BaseExtractor):
    def extract(self, content: str) -> Dict[str, Any]:
        """Extract IAM permissions from boto3 calls"""
        # Returns: {"permissions": ["ec2:DescribeInstances", ...]}
```

**Pattern Matching:**
- Boto3 client calls: `client.describe_instances()` → `ec2:DescribeInstances`
- Service detection from `boto3.client('service_name')`

#### AdvancedAnsibleExtractor
**Module**: `ddd.extractors.ansible_advanced`

AST-based deep extraction for Ansible modules.

```python
class AdvancedAnsibleExtractor:
    def extract_from_ansible_module(self, file_path: Path) -> Dict:
        """Advanced extraction using AST parsing"""
        # Returns comprehensive DAYLIGHT dimension data
```

**Capabilities:**
- AST parsing for accurate extraction
- Error scenario detection
- State management patterns
- Rollback behavior identification

#### GenericPythonExtractor
**Module**: `ddd.extractors.python_generic`

Extracts filesystem and network operations from Python code.

```python
class GenericPythonExtractor:
    def extract(self, source_code: str) -> Dict[str, Any]:
        """Extract Python operations documentation"""
        # Returns filesystem ops, network calls, error handling
```

#### ConfigurationExtractor
**Module**: `ddd.config_extractors`

Multi-language configuration discovery.

```python
class ConfigurationExtractor:
    def extract_configs(self, project_path: Path) -> List[ConfigArtifact]:
        """Extract all configuration from project"""
        # Returns list of ConfigArtifact objects
```

**Supported Formats:**
- Environment variables (`.env`, shell scripts)
- Python (`settings.py`, constants)
- JavaScript/TypeScript (config objects)
- YAML, JSON, TOML configuration files

**Security Features:**
- Automatic sensitive data detection
- Connection string identification
- API key pattern matching

---

### Specifications

#### DAYLIGHTSpec
**Module**: `ddd.specs`

Defines the 8 DAYLIGHT documentation dimensions.

```python
class DAYLIGHTSpec:
    dimensions = {
        "dependencies": DimensionSpec(weight=1.0, min_coverage=0.85),
        "automation": DimensionSpec(weight=1.0, min_coverage=0.85),
        "yearbook": DimensionSpec(weight=0.8, min_coverage=0.75),
        "lifecycle": DimensionSpec(weight=1.0, min_coverage=0.80),
        "integration": DimensionSpec(weight=0.9, min_coverage=0.80),
        "governance": DimensionSpec(weight=1.3, min_coverage=0.90),
        "health": DimensionSpec(weight=1.0, min_coverage=0.85),
        "testing": DimensionSpec(weight=1.1, min_coverage=0.85)
    }
```

#### DimensionSpec
**Module**: `ddd.specs`

Specification for a single DAYLIGHT dimension.

```python
class DimensionSpec:
    required_elements: List[str]  # Must-have documentation elements
    min_coverage: float           # Minimum acceptable coverage (0.0-1.0)
    weight: float                 # Importance weight for scoring
```

---

## CLI Interface

### Main Commands

```bash
# Measure documentation coverage
ddd measure <project_path> [--output json]

# Assert coverage meets threshold
ddd assert-coverage <project_path> [--threshold 0.85]

# Check configuration documentation
ddd config-coverage <project_path>

# Run RED-GREEN-REFACTOR demo
ddd demo <project_path>
```

### Return Codes
- `0`: Success (coverage meets threshold)
- `1`: Failure (coverage below threshold)
- `2`: Error (invalid input or processing error)

---

## Usage Examples

### Basic Coverage Measurement
```python
from ddd.coverage import DocumentationCoverage
from ddd.specs import DAYLIGHTSpec

coverage = DocumentationCoverage()
spec = DAYLIGHTSpec()
result = coverage.calculate(extracted_docs, spec)

if result.passed:
    print(f"✅ Coverage: {result.overall_score:.1%}")
else:
    print(f"❌ Coverage: {result.overall_score:.1%} (below 85%)")
```

### Extract Ansible Documentation
```python
from ddd.artifact_extractors.ansible_extractor import AnsibleModuleExtractor

extractor = AnsibleModuleExtractor()
docs = extractor.extract(ansible_content)
print(f"Required IAM permissions: {docs['permissions']}")
```

### Configuration Discovery
```python
from ddd.config_extractors import ConfigurationExtractor
from pathlib import Path

extractor = ConfigurationExtractor()
configs = extractor.extract_configs(Path("./my_project"))

for config in configs:
    if config.is_sensitive:
        print(f"⚠️ Sensitive: {config.name}")
    else:
        print(f"Config: {config.name} = {config.default_value}")
```

---

## Data Models

### CoverageResult
```python
@dataclass
class CoverageResult:
    overall_score: float          # 0.0-1.0
    dimension_scores: Dict[str, float]
    passed: bool                  # True if >= threshold
    details: Dict[str, Any]      # Detailed breakdown
```

### ConfigArtifact
```python
@dataclass
class ConfigArtifact:
    name: str                     # Variable/setting name
    category: str                 # Type of configuration
    source_file: Path            # Where it was found
    line_number: int             # Location in file
    default_value: Optional[str] # Default if specified
    is_sensitive: bool           # Contains secrets?
    validation_rules: List[str]  # Validation requirements
```

---

## Error Handling

All extractors follow consistent error handling:

- **FileNotFoundError**: Source file doesn't exist
- **ValueError**: Invalid input format or content
- **ExtractionError**: Unable to parse or extract documentation

Example:
```python
try:
    docs = extractor.extract(source_file)
except FileNotFoundError:
    print(f"Source file not found: {source_file}")
except ExtractionError as e:
    print(f"Extraction failed: {e}")
```

---

## Version Information

- **Current Version**: 0.1.0 (MVP)
- **Python Support**: 3.11+
- **License**: MIT

For complete examples and tutorials, see the [User Guide](USER_GUIDE.md).