# DDD Framework API Reference - Extractors

## Table of Contents
- [Core Extractors](#core-extractors)
  - [BaseExtractor](#baseextractor)
  - [ConfigurationExtractor](#configurationextractor)
  - [DependencyExtractor](#dependencyextractor)
  - [AnsibleModuleExtractor](#ansiblemoduleextractor)
  - [AdvancedAnsibleExtractor](#advancedansibleextractor)
- [Coverage Calculators](#coverage-calculators)
  - [DocumentationCoverage](#documentationcoverage)
  - [ConfigCoverageCalculator](#configcoveragecalculator)
- [Specifications](#specifications)
  - [DimensionSpec](#dimensionspec)
  - [DAYLIGHTSpec](#daylightspec)

---

## Core Extractors

### BaseExtractor

**Module**: `ddd.extractors.base`

Abstract base class for all documentation extractors.

#### Class Definition
```python
class BaseExtractor(ABC):
    """Base class for documentation extractors"""
    
    @abstractmethod
    def extract(self, source: Union[str, Path]) -> Dict[str, Any]:
        """Extract documentation from source"""
        pass
```

#### Methods

##### extract(source: Union[str, Path]) → Dict[str, Any]
Abstract method that must be implemented by subclasses.

**Parameters:**
- `source`: File path or content to extract documentation from

**Returns:**
- Dictionary containing extracted documentation organized by DAYLIGHT dimensions

**Example:**
```python
extractor = ConcreteExtractor()
docs = extractor.extract("./my_module.py")
```

---

### ConfigurationExtractor

**Module**: `ddd.config_extractors`

Extracts configuration parameters from source code and configuration files.

#### Class Definition
```python
class ConfigurationExtractor:
    """Multi-language configuration extraction engine"""
    
    ENV_PATTERNS: Dict[str, List[Tuple[str, str]]]
    SENSITIVE_PATTERNS: List[str]
    CONNECTION_PATTERNS: List[str]
```

#### Methods

##### extract_configs(project_path: Path) → List[ConfigArtifact]
Main entry point for configuration extraction across a project.

**Parameters:**
- `project_path`: Root directory of the project to analyze

**Returns:**
- List of ConfigArtifact objects representing discovered configurations

**Example:**
```python
extractor = ConfigurationExtractor()
configs = extractor.extract_configs(Path("./my_project"))
for config in configs:
    print(f"{config.name}: {config.category}")
```

##### extract_from_file(file_path: Path, patterns: List[Tuple[str, str]]) → List[ConfigArtifact]
Extract configuration from a single source file using language-specific patterns.

**Parameters:**
- `file_path`: Path to the file to analyze
- `patterns`: List of (regex_pattern, category) tuples

**Returns:**
- List of ConfigArtifact objects found in the file

**Example:**
```python
patterns = extractor.get_patterns_for_project(project_path)
configs = extractor.extract_from_file(
    Path("config.py"), 
    patterns["python"]
)
```

##### extract_from_env_files(project_path: Path) → List[ConfigArtifact]
Parse .env and similar environment files.

**Parameters:**
- `project_path`: Root directory to search for .env files

**Returns:**
- List of ConfigArtifact objects from environment files

**Supported Files:**
- `.env`
- `.env.example`
- `.env.local`
- `.env.development`
- `.env.production`
- `.env.test`

##### extract_from_config_files(project_path: Path) → List[ConfigArtifact]
Extract configuration from JSON, YAML, and TOML files.

**Parameters:**
- `project_path`: Root directory to search for config files

**Returns:**
- List of ConfigArtifact objects from configuration files

**Supported Formats:**
- JSON (.json)
- YAML (.yml, .yaml)
- TOML (.toml)

##### check_documentation(config: ConfigArtifact, project_path: Path) → bool
Verify if a configuration item is documented.

**Parameters:**
- `config`: ConfigArtifact to check
- `project_path`: Project root for searching documentation

**Returns:**
- True if configuration is documented, False otherwise

##### get_patterns_for_project(project_path: Path) → Dict[str, List[Tuple[str, str]]]
Determine applicable patterns based on project languages.

**Parameters:**
- `project_path`: Project root directory

**Returns:**
- Dictionary mapping languages to their pattern lists

---

### DependencyExtractor

**Module**: `ddd.extractors`

Extracts dependency information from package management files.

#### Class Definition
```python
class DependencyExtractor:
    """Extract dependencies from various package managers"""
    
    def extract(self, project_path: Path) -> Dict[str, Any]:
        """Extract all dependencies from a project"""
```

#### Methods

##### extract(project_path: Path) → Dict[str, Any]
Extract dependencies from all supported package managers.

**Parameters:**
- `project_path`: Root directory of the project

**Returns:**
- Dictionary with structure:
  ```python
  {
      "dependencies": {
          "runtime": [...],
          "development": [...],
          "optional": [...]
      }
  }
  ```

**Supported Package Managers:**
- **Python**: pyproject.toml, requirements.txt, setup.py
- **JavaScript**: package.json, yarn.lock
- **Ruby**: Gemfile
- **Go**: go.mod
- **Rust**: Cargo.toml

---

### AnsibleModuleExtractor

**Module**: `ddd.artifact_extractors.ansible_extractor`

Specialized extractor for Ansible modules and playbooks.

#### Class Definition
```python
class AnsibleModuleExtractor(InfrastructureExtractor):
    """Extract documentation from Ansible modules"""
    
    BOTO3_IAM_MAPPING: Dict[str, str]
    EC2_PERMISSION_MAPPING: Dict[str, List[str]]
```

#### Methods

##### extract_permissions(content: str) → List[str]
Extract AWS IAM permissions from boto3 API calls.

**Parameters:**
- `content`: Python source code containing boto3 calls

**Returns:**
- List of required IAM permissions (e.g., ["ec2:DescribeInstances"])

**Example:**
```python
extractor = AnsibleModuleExtractor()
code = "ec2.describe_instances()"
permissions = extractor.extract_permissions(code)
# Returns: ["ec2:DescribeInstances"]
```

##### extract_documentation_block(content: str) → Optional[Dict]
Parse Ansible DOCUMENTATION YAML block.

**Parameters:**
- `content`: Module source code

**Returns:**
- Parsed DOCUMENTATION dictionary or None

##### extract_examples_block(content: str) → Optional[str]
Extract EXAMPLES section from Ansible module.

**Parameters:**
- `content`: Module source code

**Returns:**
- EXAMPLES content as string or None

##### extract_return_block(content: str) → Optional[Dict]
Parse RETURN YAML block describing module outputs.

**Parameters:**
- `content`: Module source code

**Returns:**
- Parsed RETURN dictionary or None

##### generate_maintenance_scenarios(doc: Dict) → List[MaintenanceScenario]
Generate maintenance scenarios from extracted documentation.

**Parameters:**
- `doc`: Extracted documentation dictionary

**Returns:**
- List of MaintenanceScenario objects

---

### AdvancedAnsibleExtractor

**Module**: `ddd.extractors.ansible_advanced`

Enhanced Ansible extractor using AST parsing for deeper analysis.

#### Class Definition
```python
class AdvancedAnsibleExtractor:
    """Advanced extraction using Python AST parsing"""
    
    def extract_from_module(self, file_path: Path) -> Dict[str, Any]:
        """Deep extraction from Ansible module"""
```

#### Methods

##### extract_from_module(file_path: Path) → Dict[str, Any]
Comprehensive extraction using AST analysis.

**Parameters:**
- `file_path`: Path to Ansible module file

**Returns:**
- Dictionary containing:
  - permissions: Required IAM permissions
  - error_handling: Error patterns and recovery
  - state_management: Idempotency information
  - maintenance_scenarios: Generated scenarios
  - parameters: Module parameters
  - examples: Usage examples
  - return_values: Module outputs

##### extract_error_patterns(tree: ast.AST) → List[Dict]
Extract error handling patterns from AST.

**Parameters:**
- `tree`: Python AST of the module

**Returns:**
- List of error pattern dictionaries

##### extract_state_checks(tree: ast.AST) → Dict
Analyze state management and idempotency.

**Parameters:**
- `tree`: Python AST of the module

**Returns:**
- Dictionary describing state management

---

## Coverage Calculators

### DocumentationCoverage

**Module**: `ddd.coverage`

Main coverage calculation engine for the DDD framework.

#### Class Definition
```python
class DocumentationCoverage:
    """Calculate documentation coverage metrics"""
    
    def calculate_coverage(
        self, 
        spec: DAYLIGHTSpec, 
        extracted_data: Dict
    ) -> CoverageResult:
        """Calculate coverage against specification"""
```

#### Methods

##### calculate_coverage(spec: DAYLIGHTSpec, extracted_data: Dict) → CoverageResult
Calculate three-tier coverage metrics.

**Parameters:**
- `spec`: DAYLIGHT specification defining requirements
- `extracted_data`: Dictionary of extracted documentation

**Returns:**
- CoverageResult with metrics:
  - overall_coverage: Weighted average (0.0-1.0)
  - dimension_coverage: Coverage per dimension
  - missing_elements: List of missing items
  - recommendations: Improvement suggestions

**Coverage Tiers:**
1. **Element Coverage (30%)**: Documentation exists
2. **Completeness Coverage (40%)**: Required fields present
3. **Usefulness Coverage (30%)**: Quality and actionability

**Example:**
```python
coverage_calc = DocumentationCoverage()
result = coverage_calc.calculate_coverage(
    spec=DAYLIGHTSpec(),
    extracted_data=extracted_docs
)
print(f"Overall: {result.overall_coverage:.1%}")
```

---

### ConfigCoverageCalculator

**Module**: `ddd.config_extractors`

Specialized coverage calculator for configuration documentation.

#### Class Definition
```python
class ConfigCoverageCalculator:
    """Calculate configuration documentation coverage"""
    
    def calculate_coverage(
        self, 
        artifacts: List[ConfigArtifact]
    ) -> ConfigCoverageResult:
        """Calculate configuration coverage metrics"""
```

#### Methods

##### calculate_coverage(artifacts: List[ConfigArtifact]) → ConfigCoverageResult
Calculate configuration-specific coverage metrics.

**Parameters:**
- `artifacts`: List of discovered configuration items

**Returns:**
- ConfigCoverageResult containing:
  - overall_coverage: Percentage (0.0-1.0)
  - documented_count: Number of documented configs
  - undocumented_count: Number lacking documentation
  - sensitive_count: Number of sensitive configs
  - sensitive_undocumented: Sensitive without docs

---

## Specifications

### DimensionSpec

**Module**: `ddd.specs`

Specification for a single DAYLIGHT dimension.

#### Class Definition
```python
@dataclass
class DimensionSpec:
    """Specification for a documentation dimension"""
    
    name: str
    required_elements: List[str]
    required_fields: Dict[str, List[str]]
    minimum_coverage: float = 0.85
    weight: float = 1.0
```

#### Attributes

- **name**: Dimension identifier (e.g., "dependencies")
- **required_elements**: List of required documentation elements
- **required_fields**: Dictionary of element → required fields
- **minimum_coverage**: Threshold for passing (default: 0.85)
- **weight**: Relative importance in overall calculation

#### Methods

##### validate(data: Dict) → ValidationResult
Validate extracted data against specification.

**Parameters:**
- `data`: Extracted documentation for this dimension

**Returns:**
- ValidationResult with pass/fail status and details

---

### DAYLIGHTSpec

**Module**: `ddd.specs`

Complete DAYLIGHT framework specification.

#### Class Definition
```python
class DAYLIGHTSpec:
    """Complete DAYLIGHT documentation specification"""
    
    dimensions: Dict[str, DimensionSpec]
    
    def __init__(self):
        """Initialize with default DAYLIGHT dimensions"""
```

#### Default Dimensions

1. **Dependencies** (weight: 1.0)
   - External dependencies
   - Version requirements
   - Optional dependencies

2. **Automation** (weight: 1.2)
   - CI/CD requirements
   - Deployment scripts
   - Automation prerequisites

3. **Yearbook** (weight: 0.8)
   - Change history
   - Migration guides
   - Version compatibility

4. **Lifecycle** (weight: 1.0)
   - Startup procedures
   - Shutdown processes
   - State transitions

5. **Integration** (weight: 1.1)
   - API contracts
   - Service dependencies
   - Integration points

6. **Governance** (weight: 1.3)
   - Security policies
   - Compliance requirements
   - Access controls

7. **Health** (weight: 1.2)
   - Health checks
   - Monitoring setup
   - Alert definitions

8. **Testing** (weight: 1.0)
   - Test requirements
   - Test data setup
   - Validation procedures

#### Methods

##### get_dimension(name: str) → DimensionSpec
Retrieve specification for a dimension.

**Parameters:**
- `name`: Dimension name

**Returns:**
- DimensionSpec object

**Raises:**
- KeyError if dimension not found

##### calculate_weighted_coverage(coverages: Dict[str, float]) → float
Calculate overall weighted coverage.

**Parameters:**
- `coverages`: Dictionary of dimension → coverage percentage

**Returns:**
- Weighted average coverage (0.0-1.0)

---

## Usage Examples

### Complete Extraction Pipeline
```python
from pathlib import Path
from ddd.config_extractors import ConfigurationExtractor
from ddd.extractors import DependencyExtractor
from ddd.coverage import DocumentationCoverage
from ddd.specs import DAYLIGHTSpec

# 1. Extract configurations
config_extractor = ConfigurationExtractor()
configs = config_extractor.extract_configs(Path("./project"))

# 2. Extract dependencies
dep_extractor = DependencyExtractor()
deps = dep_extractor.extract(Path("./project"))

# 3. Combine extractions
extracted_data = {
    "dependencies": deps,
    "integration": {
        "configurations": [c.__dict__ for c in configs]
    }
}

# 4. Calculate coverage
spec = DAYLIGHTSpec()
coverage_calc = DocumentationCoverage()
result = coverage_calc.calculate_coverage(spec, extracted_data)

# 5. Report results
print(f"Documentation Coverage: {result.overall_coverage:.1%}")
for dim, cov in result.dimension_coverage.items():
    print(f"  {dim}: {cov:.1%}")
```

### Custom Dimension Specification
```python
from ddd.specs import DimensionSpec, DAYLIGHTSpec

# Create custom dimension
custom_dim = DimensionSpec(
    name="performance",
    required_elements=["benchmarks", "optimization_guides"],
    required_fields={
        "benchmarks": ["metric", "threshold", "measurement"],
        "optimization_guides": ["technique", "impact", "tradeoffs"]
    },
    minimum_coverage=0.90,
    weight=1.5
)

# Add to specification
spec = DAYLIGHTSpec()
spec.dimensions["performance"] = custom_dim
```

### Error Handling
```python
from ddd.extractors.ansible_advanced import AdvancedAnsibleExtractor

extractor = AdvancedAnsibleExtractor()

try:
    result = extractor.extract_from_module(Path("module.py"))
except FileNotFoundError:
    print("Module file not found")
except SyntaxError as e:
    print(f"Invalid Python syntax: {e}")
except Exception as e:
    print(f"Extraction failed: {e}")
```

## Performance Characteristics

| Operation | Performance | Complexity |
|-----------|------------|------------|
| Configuration extraction | ~1000 files/sec | O(n) |
| Dependency extraction | ~100 packages/sec | O(n) |
| Coverage calculation | ~10ms/dimension | O(n*m) |
| AST parsing | ~50 files/sec | O(n²) |
| Pattern matching | ~5000 lines/sec | O(n*p) |

Where:
- n = number of files/items
- m = number of requirements
- p = number of patterns

## See Also

- [Configuration Extraction Module](./CONFIG_EXTRACTION_MODULE.md)
- [TDD Workflow Guide](./TDD_WORKFLOW_EXTRACTORS.md)
- [User Guide](./USER_GUIDE.md)
- [DAYLIGHT Framework](./DAYLIGHT-Framework-Specifications.md)