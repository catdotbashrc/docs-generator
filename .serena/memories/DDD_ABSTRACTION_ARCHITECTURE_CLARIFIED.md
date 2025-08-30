# DDD Abstraction Architecture - How It Actually Works

## The Real Architecture (Not 10 Separate Extractors!)

After examining the existing `InfrastructureExtractor` base class, here's how the abstraction actually works:

### Layer 1: Abstract Base Class (Already Exists)
```python
class InfrastructureExtractor(ABC):
    """Base class defining the contract ALL tool extractors must fulfill."""
    
    # 5 Core Abstract Methods - Every tool MUST implement these
    @abstractmethod
    def extract_permissions(self, content: str) -> List[PermissionRequirement]
    
    @abstractmethod
    def extract_error_patterns(self, content: str) -> List[ErrorPattern]
    
    @abstractmethod
    def extract_state_management(self, content: str) -> Optional[StateManagement]
    
    @abstractmethod
    def extract_dependencies(self, content: str) -> List[str]
    
    @abstractmethod
    def extract_connection_requirements(self, content: str) -> List[ConnectionRequirement]
    
    # Template Method - Orchestrates the extraction workflow
    def extract(self, file_path: Path) -> MaintenanceDocument:
        """Calls all abstract methods and generates scenarios"""
```

### Layer 2: Tool-Specific Implementations
Each IaC tool gets ONE concrete implementation:

```python
class AnsibleModuleExtractor(InfrastructureExtractor):
    """Ansible-specific implementation of the extractor contract."""
    
    def extract_permissions(self, content: str) -> List[PermissionRequirement]:
        # Internally uses multiple extraction strategies:
        permissions = []
        permissions.extend(self._extract_aws_iam_permissions(content))
        permissions.extend(self._extract_file_permissions(content))
        permissions.extend(self._extract_user_requirements(content))
        return permissions
    
    def extract_error_patterns(self, content: str) -> List[ErrorPattern]:
        # Combines multiple error extraction patterns:
        errors = []
        errors.extend(self._extract_fail_json_patterns(content))
        errors.extend(self._extract_exception_handlers(content))
        errors.extend(self._extract_validation_errors(content))
        return errors
    
    def extract_state_management(self, content: str) -> Optional[StateManagement]:
        # Ansible-specific state extraction
        return self._extract_ansible_states(content)
    
    def extract_dependencies(self, content: str) -> List[str]:
        # Combines multiple dependency types:
        deps = []
        deps.extend(self._extract_module_utils(content))
        deps.extend(self._extract_python_imports(content))
        deps.extend(self._extract_system_packages(content))
        return deps
    
    def extract_connection_requirements(self, content: str) -> List[ConnectionRequirement]:
        # Network and auth requirements
        return self._extract_connection_patterns(content)
```

### Layer 3: Internal Helper Methods (Not Separate Classes!)
The "10 extractors" I mentioned are actually HELPER METHODS within each implementation:

```python
class AnsibleModuleExtractor(InfrastructureExtractor):
    # Helper methods for comprehensive extraction:
    
    def _extract_documentation_block(self, content: str) -> Dict:
        """Extract DOCUMENTATION YAML block"""
        
    def _extract_examples_block(self, content: str) -> List[str]:
        """Extract EXAMPLES for scenarios"""
        
    def _extract_return_block(self, content: str) -> Dict:
        """Extract RETURN specifications"""
        
    def _extract_parameter_specs(self, content: str) -> Dict:
        """Extract argument_spec with validation rules"""
        
    def _extract_aws_iam_permissions(self, content: str) -> List[AWSPermission]:
        """Extract AWS permissions from boto3 calls"""
        
    def _extract_fail_json_patterns(self, content: str) -> List[ErrorPattern]:
        """Extract module.fail_json() error patterns"""
        
    def _extract_ansible_states(self, content: str) -> StateManagement:
        """Extract state parameter patterns"""
        
    def _extract_module_utils(self, content: str) -> List[str]:
        """Extract ansible.module_utils dependencies"""
        
    def _extract_changelog_entries(self, content: str) -> List[Dict]:
        """Extract version_added and deprecated info"""
        
    def _extract_test_patterns(self, content: str) -> Dict:
        """Extract testing requirements from module"""
```

## How DAYLIGHT Dimensions Are Covered

The 5 abstract methods map to DAYLIGHT dimensions, but each method aggregates multiple extraction patterns:

| Abstract Method | DAYLIGHT Coverage | Internal Extractors Used |
|----------------|-------------------|--------------------------|
| `extract_dependencies()` | **D**ependencies | - Python imports<br>- Module utils<br>- System packages<br>- External services |
| `extract_connection_requirements()` | **A**utomation, **I**ntegration | - API endpoints<br>- Auth requirements<br>- Network needs |
| `extract_state_management()` | **L**ifecycle, **Y**earbook | - State transitions<br>- Version history<br>- Changelog |
| `extract_permissions()` | **G**overnance | - File permissions<br>- IAM/RBAC<br>- Certificates |
| `extract_error_patterns()` | **H**ealth, **T**esting | - Error handlers<br>- Test patterns<br>- Recovery procedures |

## The Correct Implementation Strategy

### Phase 1: Implement AnsibleModuleExtractor
```python
class AnsibleModuleExtractor(InfrastructureExtractor):
    """Complete Ansible implementation with all helper methods."""
    
    def extract_permissions(self, content: str) -> List[PermissionRequirement]:
        # Implement using helper methods
        
    def extract_error_patterns(self, content: str) -> List[ErrorPattern]:
        # Implement using helper methods
        
    # ... implement all 5 abstract methods
```

### Phase 2: Add More Tool Extractors
```python
class TerraformExtractor(InfrastructureExtractor):
    """Terraform-specific implementation."""
    # Different internal helpers for HCL parsing
    
class KubernetesExtractor(InfrastructureExtractor):
    """Kubernetes manifest extractor."""
    # Different internal helpers for YAML manifests
```

## Why This Design Is Better

1. **Single Responsibility**: Each class has one job - extract from one tool type
2. **Consistent Interface**: All tools expose same 5 methods via base class
3. **Tool-Specific Logic**: Internal implementation can vary wildly per tool
4. **Extensible**: Add new tools by creating new implementations
5. **Testable**: Test against the interface, not implementation details

## What This Means for Testing

Test the CONTRACT, not the helpers:
```python
def test_ansible_extractor_contract():
    """Test that AnsibleModuleExtractor fulfills the contract."""
    extractor = AnsibleModuleExtractor()
    content = read_file("baseline/ansible/lib/ansible/modules/file.py")
    
    # Test all 5 required methods
    permissions = extractor.extract_permissions(content)
    assert isinstance(permissions, list)
    assert all(isinstance(p, PermissionRequirement) for p in permissions)
    
    errors = extractor.extract_error_patterns(content)
    assert isinstance(errors, list)
    
    state = extractor.extract_state_management(content)
    assert state is None or isinstance(state, StateManagement)
    
    deps = extractor.extract_dependencies(content)
    assert isinstance(deps, list)
    
    connections = extractor.extract_connection_requirements(content)
    assert isinstance(connections, list)
```

## Implementation Priority

1. **Week 1**: Implement AnsibleModuleExtractor with all 5 methods
2. **Week 2**: Add comprehensive helper methods for deep extraction
3. **Week 3**: Test against real Ansible modules
4. **Week 4**: Start TerraformExtractor (if time permits)

The "10 extractors" become helper methods WITHIN AnsibleModuleExtractor, not separate classes!