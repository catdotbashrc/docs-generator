# DDD Framework API Reference

## Core Classes

### `DocumentationCoverage`
Main coverage calculator implementing 3-level measurement system.

```python
from ddd.coverage import DocumentationCoverage

coverage = DocumentationCoverage()
result = coverage.measure(extracted_data)
```

#### Methods

##### `measure(extracted_data: Dict) -> CoverageResult`
Calculate documentation coverage across DAYLIGHT dimensions.

**Parameters:**
- `extracted_data`: Dictionary containing extracted documentation

**Returns:**
- `CoverageResult`: Object containing coverage scores and recommendations

**Example:**
```python
result = coverage.measure({
    'dependencies': {'npm': ['react', 'express']},
    'automation': {'scripts': ['test', 'build']},
    # ... other dimensions
})
print(f"Coverage: {result.overall_coverage}%")
```

##### `assert_coverage(extracted_data: Dict, minimum: float = 0.85)`
Assert documentation meets minimum threshold.

**Parameters:**
- `extracted_data`: Extracted documentation dictionary
- `minimum`: Minimum coverage threshold (0.0-1.0)

**Raises:**
- `AssertionError`: If coverage below minimum

---

### `InfrastructureExtractor`
Abstract base class for tool-specific extractors.

```python
from ddd.artifact_extractors.base import InfrastructureExtractor

class MyExtractor(InfrastructureExtractor):
    def extract_permissions(self, content: str):
        # Implementation
        pass
```

#### Abstract Methods (Must Implement)

##### `extract_permissions(content: str) -> List[PermissionRequirement]`
Extract permission requirements from code.

##### `extract_error_patterns(content: str) -> List[ErrorPattern]`
Extract common error patterns and recovery procedures.

##### `extract_state_management(content: str) -> StateManagement`
Extract state management information (idempotency, rollback).

##### `extract_dependencies(content: str) -> List[Dependency]`
Extract external dependencies and versions.

##### `extract_connection_requirements(content: str) -> List[ConnectionRequirement]`
Extract network and connection requirements.

#### Concrete Methods

##### `extract(file_path: Path) -> MaintenanceDocument`
Template method orchestrating extraction process.

**Parameters:**
- `file_path`: Path to file to extract from

**Returns:**
- `MaintenanceDocument`: Complete extracted documentation

---

### `AnsibleModuleExtractor`
Concrete implementation for Ansible modules.

```python
from ddd.artifact_extractors.ansible_extractor import AnsibleModuleExtractor

extractor = AnsibleModuleExtractor()
doc = extractor.extract(Path("deploy.yml"))
```

#### Additional Methods

##### `extract_documentation_block(content: str) -> Dict`
Extract DOCUMENTATION block from Ansible module.

##### `extract_examples_block(content: str) -> List[str]`
Extract EXAMPLES block with usage examples.

##### `extract_return_block(content: str) -> Dict`
Extract RETURN block with output documentation.

---

## Data Classes

### `PermissionRequirement`
Abstract base for permission requirements.

```python
@dataclass(frozen=True)
class PermissionRequirement(ABC):
    service: str
    resource: str
    action: str
    
    @abstractmethod
    def to_iam_policy(self) -> str:
        """Convert to IAM policy statement."""
        pass
```

### `AWSIAMPermission`
AWS-specific permission implementation.

```python
@dataclass(frozen=True)
class AWSIAMPermission(PermissionRequirement):
    service: str
    action: str
    resource: str = "*"
    
    @classmethod
    def from_boto3_call(cls, service: str, method: str):
        """Create from boto3 client method call."""
        return cls(
            service=service,
            action=f"{service}:{method}",
            resource="*"
        )
```

### `ErrorPattern`
Represents an error pattern with recovery procedure.

```python
@dataclass
class ErrorPattern:
    error_type: str
    description: str
    recovery_procedure: str
    frequency: Optional[str] = None
    severity: str = "medium"
```

### `StateManagement`
State management information.

```python
@dataclass
class StateManagement:
    idempotent: bool
    rollback_capable: bool
    check_mode_supported: bool
    state_tracking_method: str
    drift_detection: Optional[str] = None
```

### `MaintenanceDocument`
Complete maintenance documentation.

```python
@dataclass
class MaintenanceDocument:
    permissions: List[PermissionRequirement]
    error_patterns: List[ErrorPattern]
    state_management: StateManagement
    dependencies: List[Dependency]
    connection_requirements: List[ConnectionRequirement]
    maintenance_scenarios: List[MaintenanceScenario] = field(default_factory=list)
    
    def to_markdown(self) -> str:
        """Convert to Markdown documentation."""
        pass
    
    def to_html(self) -> str:
        """Convert to HTML documentation."""
        pass
```

---

## Specifications

### `DimensionSpec`
Specification for a documentation dimension.

```python
@dataclass
class DimensionSpec:
    name: str
    required_elements: List[str]
    minimum_coverage: float = 0.7
    weight: float = 0.125
    
    def validate(self, data: Dict) -> ValidationResult:
        """Validate dimension data against spec."""
        pass
```

### `DAYLIGHTSpec`
Complete DAYLIGHT dimensions specification.

```python
class DAYLIGHTSpec:
    dimensions = {
        'dependencies': DimensionSpec(
            name='Dependencies',
            required_elements=['runtime', 'development', 'versions'],
            weight=0.15
        ),
        'automation': DimensionSpec(
            name='Automation',
            required_elements=['scripts', 'ci_cd', 'deployment'],
            weight=0.15
        ),
        # ... other dimensions
    }
```

---

## CLI Module

### Main Entry Point

```python
import click
from ddd.cli import main

@click.group()
def cli():
    """DDD Framework CLI."""
    pass

@cli.command()
@click.argument('project_path')
@click.option('--threshold', default=0.85)
def measure(project_path, threshold):
    """Measure documentation coverage."""
    # Implementation
```

---

## Exceptions

### `ExtractionError`
Raised when extraction fails.

```python
class ExtractionError(Exception):
    """Failed to extract documentation."""
    pass
```

### `CoverageError`
Raised when coverage validation fails.

```python
class CoverageError(Exception):
    """Documentation coverage below threshold."""
    pass
```

---

## Usage Examples

### Complete Extraction Pipeline

```python
from pathlib import Path
from ddd.artifact_extractors.ansible_extractor import AnsibleModuleExtractor
from ddd.coverage import DocumentationCoverage

# Extract documentation
extractor = AnsibleModuleExtractor()
doc = extractor.extract(Path("playbook.yml"))

# Convert to dictionary
extracted_data = doc.to_dict()

# Measure coverage
coverage = DocumentationCoverage()
result = coverage.measure(extracted_data)

# Check if passes
if result.passed:
    print(f"✅ Coverage: {result.overall_coverage}%")
else:
    print(f"❌ Coverage: {result.overall_coverage}%")
    print("Missing:", result.missing_elements)
```

### Custom Extractor Implementation

```python
from ddd.artifact_extractors.base import InfrastructureExtractor
from typing import List
import re

class TerraformExtractor(InfrastructureExtractor):
    
    def extract_permissions(self, content: str) -> List[PermissionRequirement]:
        # Extract AWS provider permissions
        permissions = []
        
        # Find resource declarations
        resources = re.findall(r'resource "aws_(\w+)"', content)
        for resource_type in resources:
            # Map to IAM permissions
            permissions.append(
                AWSIAMPermission(
                    service=resource_type.split('_')[0],
                    action=f"{resource_type}:*",
                    resource="*"
                )
            )
        
        return permissions
    
    def extract_state_management(self, content: str) -> StateManagement:
        return StateManagement(
            idempotent=True,  # Terraform is idempotent
            rollback_capable=True,  # Via state file
            check_mode_supported=True,  # terraform plan
            state_tracking_method="terraform.tfstate"
        )
```

### Programmatic Coverage Assertion

```python
from ddd.coverage import DocumentationCoverage

def validate_documentation(project_path: Path, threshold: float = 0.85):
    """Validate project documentation in CI/CD."""
    
    coverage = DocumentationCoverage()
    extractor = get_extractor_for_project(project_path)
    
    for file in project_path.glob("**/*"):
        if should_extract(file):
            doc = extractor.extract(file)
            data = doc.to_dict()
            
            try:
                coverage.assert_coverage(data, minimum=threshold)
                print(f"✅ {file}: Passed")
            except AssertionError as e:
                print(f"❌ {file}: {e}")
                return False
    
    return True
```

---

## Configuration API

### Loading Configuration

```python
from ddd.config import load_config

config = load_config(".ddd.yml")
threshold = config.get("coverage.threshold", 0.85)
```

### Custom Dimension Weights

```python
from ddd.specs import DAYLIGHTSpec

# Customize weights
DAYLIGHTSpec.dimensions['dependencies'].weight = 0.2
DAYLIGHTSpec.dimensions['testing'].weight = 0.2
# Weights must sum to 1.0
```

---

## Extension Points

### Adding New Extractors

1. Inherit from `InfrastructureExtractor`
2. Implement abstract methods
3. Register in extractor factory

```python
from ddd.extractors.factory import register_extractor

@register_extractor("kubernetes")
class KubernetesExtractor(InfrastructureExtractor):
    # Implementation
    pass
```

### Custom Coverage Dimensions

```python
from ddd.specs import DimensionSpec, register_dimension

custom_dimension = DimensionSpec(
    name="Security",
    required_elements=["encryption", "authentication", "audit"],
    weight=0.1
)

register_dimension("security", custom_dimension)
```