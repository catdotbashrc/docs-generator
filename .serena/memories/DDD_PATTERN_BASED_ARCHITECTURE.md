# Pattern-Based Architecture for DDD - Universal Infrastructure Patterns

## The Problem with Tool-Specific Abstractions

Current architecture is tool-centric:
- `AnsibleModuleExtractor` knows Ansible-specific syntax
- `TerraformExtractor` knows HCL syntax
- Adding a new pattern means updating EVERY tool extractor
- Patterns discovered in Ansible don't automatically apply to Terraform

## Better Architecture: Pattern-First, Tool-Second

### Core Insight
**Maintenance patterns are universal across ALL infrastructure code:**
- **Permissions** exist in Ansible (IAM), Terraform (provider perms), K8s (RBAC)
- **Error handling** exists everywhere (try/except, error blocks, catch)
- **State management** exists everywhere (present/absent, create/destroy, apply/delete)
- **Dependencies** exist everywhere (imports, requires, depends_on)

### New Architecture Layers

```
┌─────────────────────────────────────────────────────────┐
│                 Pattern Orchestrator                     │
│  (Combines all patterns for complete documentation)      │
└─────────────────────────────────────────────────────────┘
                            │
                  ┌─────────┴─────────┐
                  │   Pattern Registry │
                  │  (Manages patterns) │
                  └─────────┬─────────┘
                            │
    ┌───────────┬───────────┼───────────┬───────────┐
    ▼           ▼           ▼           ▼           ▼
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│Permission│ │Error    │ │State    │ │Dependency│ │Document │
│Pattern   │ │Pattern  │ │Pattern  │ │Pattern   │ │Pattern  │
│Extractor │ │Extractor│ │Extractor│ │Extractor │ │Extractor│
└─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘
    │           │           │           │           │
    └───────────┴───────────┼───────────┴───────────┘
                            ▼
                  ┌─────────────────┐
                  │ Language Parser  │
                  │ (Syntax Agnostic)│
                  └─────────────────┘
                     Python | YAML | HCL | JSON
```

## Pattern Extractor Design

### Base Pattern Class
```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class Pattern:
    """Universal pattern found in code."""
    pattern_type: str
    confidence: float  # 0.0 to 1.0
    location: tuple[int, int]  # start_line, end_line
    raw_content: str
    extracted_data: Dict[str, Any]
    
class PatternExtractor(ABC):
    """Base class for all pattern extractors."""
    
    @abstractmethod
    def identify_patterns(self, ast_or_tokens: Any) -> List[Pattern]:
        """Identify patterns in parsed code structure."""
        pass
    
    @abstractmethod
    def extract_pattern_data(self, pattern: Pattern) -> Dict[str, Any]:
        """Extract maintenance-relevant data from pattern."""
        pass
    
    @abstractmethod
    def pattern_signatures(self) -> List[str]:
        """Return signatures this extractor can identify."""
        pass
```

### Concrete Pattern Extractors

```python
class PermissionPatternExtractor(PatternExtractor):
    """Extracts permission patterns regardless of tool."""
    
    PERMISSION_INDICATORS = [
        # AWS/Cloud patterns
        "iam", "role", "policy", "permission", "assume_role",
        "credentials", "access_key", "secret_key",
        # File system patterns
        "mode", "owner", "group", "chmod", "chown",
        # Kubernetes patterns
        "rbac", "serviceaccount", "rolebinding", "clusterrole",
        # Generic patterns
        "auth", "grant", "deny", "allow", "privilege"
    ]
    
    def identify_patterns(self, ast_or_tokens: Any) -> List[Pattern]:
        patterns = []
        
        # Look for permission indicators in any syntax
        for indicator in self.PERMISSION_INDICATORS:
            if self._find_indicator(ast_or_tokens, indicator):
                pattern = self._extract_permission_pattern(ast_or_tokens, indicator)
                patterns.append(pattern)
        
        return patterns
    
    def _extract_permission_pattern(self, ast, indicator: str) -> Pattern:
        # Extract pattern regardless of syntax
        if indicator in ["mode", "owner", "group"]:
            return self._extract_file_permission(ast)
        elif indicator in ["iam", "role", "policy"]:
            return self._extract_cloud_permission(ast)
        elif indicator in ["rbac", "serviceaccount"]:
            return self._extract_k8s_permission(ast)
```

```python
class StatePatternExtractor(PatternExtractor):
    """Extracts state management patterns."""
    
    STATE_INDICATORS = [
        # Ansible patterns
        "state", "present", "absent", "started", "stopped",
        # Terraform patterns
        "create", "destroy", "taint", "lifecycle",
        # Kubernetes patterns
        "apply", "delete", "patch", "replace",
        # Generic patterns
        "ensure", "exists", "running", "deleted"
    ]
    
    def identify_patterns(self, ast_or_tokens: Any) -> List[Pattern]:
        patterns = []
        
        # State machines are universal
        for indicator in self.STATE_INDICATORS:
            if self._find_state_pattern(ast_or_tokens, indicator):
                pattern = Pattern(
                    pattern_type="state_management",
                    confidence=self._calculate_confidence(indicator),
                    location=self._get_location(ast_or_tokens, indicator),
                    raw_content=self._get_raw(ast_or_tokens, indicator),
                    extracted_data={
                        "state": indicator,
                        "transitions": self._find_transitions(ast_or_tokens, indicator),
                        "idempotent": self._is_idempotent(ast_or_tokens, indicator)
                    }
                )
                patterns.append(pattern)
        
        return patterns
```

```python
class DocumentationPatternExtractor(PatternExtractor):
    """Extracts structured documentation patterns."""
    
    DOC_INDICATORS = [
        # Ansible
        "DOCUMENTATION", "EXAMPLES", "RETURN",
        # Python
        "__doc__", "\"\"\"", "'''",
        # Terraform
        "description", "/*", "//",
        # YAML/JSON
        "description", "summary", "notes"
    ]
    
    def identify_patterns(self, ast_or_tokens: Any) -> List[Pattern]:
        patterns = []
        
        # Look for structured docs in any format
        for indicator in self.DOC_INDICATORS:
            doc_block = self._find_doc_block(ast_or_tokens, indicator)
            if doc_block:
                pattern = Pattern(
                    pattern_type="documentation",
                    confidence=1.0 if self._is_structured(doc_block) else 0.5,
                    location=doc_block.location,
                    raw_content=doc_block.content,
                    extracted_data=self._parse_documentation(doc_block)
                )
                patterns.append(pattern)
        
        return patterns
```

## Language Parser Layer

```python
class LanguageParser:
    """Parses different languages into universal AST-like structure."""
    
    @staticmethod
    def parse(content: str, file_extension: str) -> Any:
        """Parse content based on file type."""
        if file_extension in ['.py']:
            return PythonParser().parse(content)
        elif file_extension in ['.yml', '.yaml']:
            return YAMLParser().parse(content)
        elif file_extension in ['.tf', '.hcl']:
            return HCLParser().parse(content)
        elif file_extension in ['.json']:
            return JSONParser().parse(content)
        else:
            return TokenParser().parse(content)  # Fallback

class PythonParser:
    """Python-specific parsing."""
    def parse(self, content: str):
        import ast
        tree = ast.parse(content)
        # Convert to universal structure
        return self._normalize_ast(tree)

class YAMLParser:
    """YAML-specific parsing."""
    def parse(self, content: str):
        import yaml
        data = yaml.safe_load(content)
        # Convert to universal structure
        return self._normalize_yaml(data)
```

## Pattern Orchestrator

```python
class PatternOrchestrator:
    """Orchestrates all pattern extractors."""
    
    def __init__(self):
        self.pattern_extractors = [
            PermissionPatternExtractor(),
            StatePatternExtractor(),
            ErrorPatternExtractor(),
            DependencyPatternExtractor(),
            DocumentationPatternExtractor(),
            ParameterPatternExtractor(),
            TestPatternExtractor(),
        ]
        self.parser = LanguageParser()
    
    def extract_all_patterns(self, file_path: Path) -> MaintenanceDocument:
        """Extract all patterns from a file."""
        content = file_path.read_text()
        
        # Parse into universal structure
        parsed = self.parser.parse(content, file_path.suffix)
        
        # Extract all patterns
        all_patterns = []
        for extractor in self.pattern_extractors:
            patterns = extractor.identify_patterns(parsed)
            all_patterns.extend(patterns)
        
        # Convert patterns to maintenance document
        return self._patterns_to_document(all_patterns, file_path)
    
    def _patterns_to_document(self, patterns: List[Pattern], file_path: Path) -> MaintenanceDocument:
        """Convert patterns to maintenance documentation."""
        doc = MaintenanceDocument(file_path=file_path)
        
        for pattern in patterns:
            if pattern.pattern_type == "permission":
                doc.permissions.append(self._to_permission_requirement(pattern))
            elif pattern.pattern_type == "error":
                doc.error_patterns.append(self._to_error_pattern(pattern))
            elif pattern.pattern_type == "state_management":
                doc.state_management = self._to_state_management(pattern)
            # ... etc
        
        return doc
```

## Why This Architecture Is Superior

### 1. Pattern Reusability
Patterns discovered in Ansible automatically work for Terraform:
```python
# This pattern works for ANY infrastructure code:
class IdempotencyPattern(PatternExtractor):
    """Detects idempotency patterns in any tool."""
    
    IDEMPOTENCY_INDICATORS = [
        "check_mode", "changed_when", "creates",  # Ansible
        "lifecycle.create_before_destroy",         # Terraform
        "immutable", "replace",                    # Kubernetes
    ]
```

### 2. Easy Pattern Addition
Add new patterns without touching existing code:
```python
# Just add a new pattern extractor
class CompliancePatternExtractor(PatternExtractor):
    """Detects compliance and governance patterns."""
    
    COMPLIANCE_INDICATORS = [
        "compliance", "audit", "policy", "standard",
        "sox", "pci", "hipaa", "gdpr"
    ]
```

### 3. Easy Tool Addition
Add new tools without changing patterns:
```python
# Just add a new parser
class CloudFormationParser:
    """Parse CloudFormation templates."""
    def parse(self, content: str):
        # Convert to universal structure
        return self._normalize_cloudformation(content)
```

### 4. Pattern Learning
Patterns can be discovered and refined:
```python
class PatternLearner:
    """Learns new patterns from codebases."""
    
    def discover_patterns(self, codebase_path: Path):
        # Analyze codebase for recurring patterns
        # Add to pattern registry
        pass
```

## Implementation Priority

### Phase 1: Core Pattern Extractors
1. **DocumentationPatternExtractor** - Structured docs are universal
2. **ParameterPatternExtractor** - All tools have parameters
3. **ErrorPatternExtractor** - All tools handle errors

### Phase 2: Operational Patterns
4. **StatePatternExtractor** - State machines everywhere
5. **PermissionPatternExtractor** - Security is universal
6. **DependencyPatternExtractor** - All code has dependencies

### Phase 3: Advanced Patterns
7. **TestPatternExtractor** - Testing patterns
8. **CompliancePatternExtractor** - Governance patterns
9. **PerformancePatternExtractor** - Optimization patterns

## Pattern Registry

```python
class PatternRegistry:
    """Central registry of all known patterns."""
    
    def __init__(self):
        self.patterns = {}
        self._load_builtin_patterns()
        self._load_learned_patterns()
    
    def register_pattern(self, pattern_type: str, signature: Dict):
        """Register a new pattern signature."""
        self.patterns[pattern_type] = signature
    
    def get_pattern_signatures(self, pattern_type: str) -> List[Dict]:
        """Get all signatures for a pattern type."""
        return self.patterns.get(pattern_type, [])
    
    def _load_builtin_patterns(self):
        """Load patterns we've discovered from Ansible analysis."""
        self.patterns['permission'] = [
            {"indicator": "mode", "type": "file_permission"},
            {"indicator": "iam", "type": "aws_permission"},
            {"indicator": "rbac", "type": "k8s_permission"},
        ]
        # ... load all discovered patterns
```

## Benefits

1. **Future-Proof**: Patterns learned today apply to tools created tomorrow
2. **Maintainable**: Single place to update each pattern
3. **Testable**: Test patterns independently of tools
4. **Extensible**: Add patterns or tools without breaking existing code
5. **Discoverable**: Can learn new patterns from codebases automatically

This architecture truly captures the universal patterns in infrastructure code!