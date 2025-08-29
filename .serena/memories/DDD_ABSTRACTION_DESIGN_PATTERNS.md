# DDD Framework Abstraction Design Patterns

## The Abstraction Challenge

**Goal**: Create an abstraction that works for Ansible today but can extend to Terraform, Kubernetes, Shell Scripts, and other IaC tools tomorrow.

**Solution**: Three-layer abstraction with clear boundaries.

## Abstraction Layers

### Layer 1: Universal Maintenance Concepts (Abstract Base)

These concepts exist across ALL infrastructure tools:

```python
class InfrastructureExtractor(ABC):
    @abstractmethod
    def extract_permissions(self, content: str) -> List[PermissionRequirement]:
        """Every tool has some permission model"""
        
    @abstractmethod
    def extract_error_patterns(self, content: str) -> List[ErrorPattern]:
        """Every tool can fail in various ways"""
        
    @abstractmethod
    def extract_state_management(self, content: str) -> Optional[StateManagement]:
        """Every tool manages state somehow"""
        
    @abstractmethod
    def extract_dependencies(self, content: str) -> List[str]:
        """Every tool has dependencies"""
        
    @abstractmethod
    def extract_connection_requirements(self, content: str) -> List[ConnectionRequirement]:
        """Every tool needs network/connectivity"""
```

### Layer 2: Domain-Specific Implementations

Each tool implements the abstract methods with its specific logic:

**Ansible**:
- Permissions → AWS IAM from boto3 calls
- Errors → module.fail_json patterns
- State → check_mode, changed tracking
- Dependencies → Python packages, Ansible modules
- Connections → AWS regions, VPCs

**Terraform** (future):
- Permissions → Provider permissions from resource blocks
- Errors → terraform plan/apply errors
- State → terraform.tfstate management
- Dependencies → Provider versions, modules
- Connections → Provider endpoints

**Kubernetes** (future):
- Permissions → RBAC from ServiceAccounts
- Errors → Pod failures, resource limits
- State → Desired vs actual state
- Dependencies → Container images, ConfigMaps
- Connections → API server, namespaces

### Layer 3: Concrete Data Types

Tool-specific permission types that implement the abstract interface:

```python
# Ansible
@dataclass
class AWSIAMPermission(PermissionRequirement):
    service: str  # e.g., "ec2"
    action: str   # e.g., "DescribeInstances"
    
# Terraform (future)
@dataclass
class TerraformProviderPermission(PermissionRequirement):
    provider: str  # e.g., "aws"
    resource: str  # e.g., "aws_instance"
    actions: List[str]  # e.g., ["create", "read", "update", "delete"]
    
# Kubernetes (future)
@dataclass
class KubernetesRBAC(PermissionRequirement):
    resource: str  # e.g., "pods"
    verbs: List[str]  # e.g., ["get", "list", "watch"]
    namespace: str  # e.g., "default"
```

## Design Patterns Used

### 1. Template Method Pattern
The base class defines the extraction workflow, subclasses fill in the details:

```python
def extract(self, file_path: Path) -> MaintenanceDocument:
    """Template method - same flow for all tools"""
    content = self.read_file(file_path)
    
    doc = MaintenanceDocument(
        permissions=self.extract_permissions(content),  # Subclass implements
        error_patterns=self.extract_error_patterns(content),  # Subclass implements
        state_management=self.extract_state_management(content),  # Subclass implements
        # ... etc
    )
    
    doc.generate_maintenance_scenarios()  # Base class provides default
    return doc
```

### 2. Factory Method Pattern
Each extractor creates its own permission types:

```python
class AnsibleModuleExtractor:
    def extract_permissions(self, content):
        # Creates AWSIAMPermission objects
        return [AWSIAMPermission.from_boto3_call(service, method)]
        
class TerraformExtractor:
    def extract_permissions(self, content):
        # Creates TerraformProviderPermission objects
        return [TerraformProviderPermission.from_resource_block(block)]
```

### 3. Strategy Pattern
Different extraction strategies for different tools:

```python
# Each tool has its own strategy for finding permissions
class AnsibleModuleExtractor:
    def _find_permissions(self, content):
        # Look for boto3.client() calls
        
class TerraformExtractor:
    def _find_permissions(self, content):
        # Parse HCL resource blocks
        
class KubernetesExtractor:
    def _find_permissions(self, content):
        # Parse YAML for ServiceAccounts
```

## Abstraction Validation Tests

### Test 1: Can we add a new tool without changing base?
✅ **YES** - Just create new extractor subclass

### Test 2: Can tools share common logic?
✅ **YES** - Base class provides default implementations

### Test 3: Can tools have unique features?
✅ **YES** - Subclasses can add tool-specific methods

### Test 4: Is the abstraction leaky?
✅ **NO** - Base knows nothing about boto3, HCL, or YAML

### Test 5: Can we test the abstraction?
✅ **YES** - Abstract tests verify contract, concrete tests verify implementation

## Future-Proofing Decisions

### What We Abstracted
- Permission concept (not AWS IAM specifically)
- Error patterns (not Python exceptions specifically)
- State management (not Ansible check_mode specifically)
- Dependencies (not pip packages specifically)

### What We Kept Concrete
- File I/O (all tools read files)
- Maintenance scenarios (universal troubleshooting)
- Documentation coverage (same calculation for all)

### What We Made Extensible
- Permission types (each tool defines its own)
- Extraction patterns (each tool has its strategy)
- Scenario generation (can be overridden per tool)

## Lessons Learned

### Start Specific, Extract General
We built Ansible first, then extracted the abstract interface. This ensured our abstraction was grounded in reality, not theoretical.

### Test at Multiple Levels
- Abstract tests ensure contract compliance
- Concrete tests ensure correct implementation
- Integration tests ensure end-to-end functionality

### Balance is Key
Too abstract: Becomes meaningless and hard to implement
Too specific: Can't extend to other tools
Just right: Clear contract with room for tool-specific behavior