# DDD Framework Development Guide

## TDD Workflow for Documentation

Just as Test-Driven Development ensures code quality, Documentation Driven Development ensures maintenance readiness through the RED-GREEN-REFACTOR cycle.

### The Cycle

#### 1. RED Phase - Define Requirements
Write failing tests that define what complete documentation looks like:

```python
def test_extract_permissions():
    """Test that IAM permissions are extracted"""
    extractor = AnsibleModuleExtractor()
    content = "ec2_client.describe_instances()"
    result = extractor.extract(content)
    assert "ec2:DescribeInstances" in result["governance"]["permissions"]  # FAILS
```

#### 2. GREEN Phase - Implement Extraction
Write minimal code to make tests pass:

```python
class AnsibleModuleExtractor:
    def extract(self, content):
        permissions = []
        if "describe_instances" in content:
            permissions.append("ec2:DescribeInstances")
        return {"governance": {"permissions": permissions}}  # PASSES
```

#### 3. REFACTOR Phase - Improve Quality
Enhance implementation while keeping tests green:

```python
class AnsibleModuleExtractor:
    BOTO3_PATTERN = re.compile(r'(\w+)\.(\w+)\(')
    
    def extract(self, content):
        permissions = set()
        for match in self.BOTO3_PATTERN.finditer(content):
            service, action = match.groups()
            permissions.add(f"{service}:{self._to_iam_action(action)}")
        return {"governance": {"permissions": sorted(permissions)}}
```

## Creating New Extractors

### Step 1: Write Contract Tests

All extractors must pass the base contract tests:

```python
# tests/test_extractor_contract.py
def test_extractor_returns_dict(extractor_class):
    """Verify extractor returns dictionary"""
    extractor = extractor_class()
    result = extractor.extract("sample content")
    assert isinstance(result, dict)

def test_extractor_has_daylight_dimensions(extractor_class):
    """Verify DAYLIGHT dimensions present"""
    extractor = extractor_class()
    result = extractor.extract("sample content")
    for dimension in ["dependencies", "governance", "health"]:
        assert dimension in result
```

### Step 2: Implement Base Class

```python
from ddd.artifact_extractors.base import BaseExtractor

class MyExtractor(BaseExtractor):
    def extract(self, source: Union[str, Path]) -> Dict[str, Any]:
        """Extract documentation from source"""
        return {
            "dependencies": self._extract_dependencies(source),
            "governance": self._extract_governance(source),
            "health": self._extract_health(source),
            # ... other DAYLIGHT dimensions
        }
```

### Step 3: Add Pattern Matching

```python
class MyExtractor(BaseExtractor):
    # Define patterns for your language/framework
    PATTERNS = {
        "imports": re.compile(r'import\s+(\S+)'),
        "config": re.compile(r'config\[["\'](.*?)["\']\]'),
        "errors": re.compile(r'except\s+(\w+)')
    }
    
    def _extract_dependencies(self, content):
        imports = self.PATTERNS["imports"].findall(content)
        return {"packages": imports}
```

## Testing Guidelines

### Unit Tests
Test individual extraction methods:

```python
def test_extract_imports():
    extractor = MyExtractor()
    content = "import boto3\nimport json"
    deps = extractor._extract_dependencies(content)
    assert deps["packages"] == ["boto3", "json"]
```

### Integration Tests
Test full extraction workflow:

```python
def test_full_extraction():
    extractor = MyExtractor()
    result = extractor.extract("./sample_file.py")
    
    # Verify all dimensions present
    assert all(dim in result for dim in DAYLIGHT_DIMENSIONS)
    
    # Verify coverage threshold
    coverage = DocumentationCoverage()
    score = coverage.calculate(result, DAYLIGHTSpec())
    assert score.overall_score >= 0.85
```

### Coverage Tests
Ensure extraction meets coverage requirements:

```python
def test_coverage_calculation():
    docs = {"governance": {"permissions": ["s3:GetObject"]}}
    coverage = DocumentationCoverage()
    result = coverage.calculate(docs, DAYLIGHTSpec())
    
    assert 0.0 <= result.overall_score <= 1.0
    assert result.passed == (result.overall_score >= 0.85)
```

## Code Style & Quality

### Standards
- **Line length**: 100 characters max
- **Formatting**: Black with default settings
- **Linting**: Ruff for style enforcement
- **Type hints**: Required for public methods

### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    hooks:
      - id: black
        args: [--line-length=100]
  
  - repo: https://github.com/charliermarsh/ruff-pre-commit
    hooks:
      - id: ruff
        args: [--fix]
```

### Running Quality Checks
```bash
# Format code
uv run black src/ tests/

# Lint code
uv run ruff check src/ tests/ --fix

# Run tests with coverage
uv run pytest --cov=src --cov-report=term-missing

# Run only critical tests
uv run pytest tests/test_extractor_contract.py -v
```

## Project Structure

```
src/ddd/
├── artifact_extractors/     # Infrastructure extractors
│   ├── base.py             # Abstract base class
│   └── ansible_extractor.py # Ansible implementation
├── config_extractors/       # Configuration discovery
├── coverage/               # Coverage calculation
├── specs/                  # DAYLIGHT specifications
└── extractors/             # Additional extractors

tests/
├── test_extractor_contract.py  # Contract tests (must pass)
├── config_extractors/          # Config extractor tests
└── test_coverage.py           # Coverage calculation tests
```

## Contributing Checklist

- [ ] Write RED phase tests first
- [ ] Implement minimal GREEN solution
- [ ] REFACTOR for quality
- [ ] Pass all contract tests
- [ ] Achieve 85% documentation coverage
- [ ] Format with Black
- [ ] Pass Ruff linting
- [ ] Add integration tests
- [ ] Update API documentation

## Common Patterns

### Pattern: Multi-language Support
```python
class MultiLanguageExtractor:
    EXTRACTORS = {
        ".py": PythonExtractor(),
        ".js": JavaScriptExtractor(),
        ".yml": YamlExtractor()
    }
    
    def extract(self, file_path: Path):
        ext = file_path.suffix
        if ext in self.EXTRACTORS:
            return self.EXTRACTORS[ext].extract(file_path)
```

### Pattern: AST-based Extraction
```python
import ast

class ASTExtractor:
    def extract(self, source_code: str):
        tree = ast.parse(source_code)
        visitor = MyASTVisitor()
        visitor.visit(tree)
        return visitor.get_documentation()
```

### Pattern: Sensitive Data Detection
```python
SENSITIVE_PATTERNS = [
    "password", "secret", "key", "token", "credential"
]

def is_sensitive(name: str) -> bool:
    return any(pattern in name.lower() 
              for pattern in SENSITIVE_PATTERNS)
```

## Debugging Tips

1. **Use verbose test output**: `pytest -vvs`
2. **Check pattern matches**: Test regex patterns at regex101.com
3. **Validate against real files**: Use actual project files for testing
4. **Log extraction steps**: Add debug logging to trace extraction flow

---

*Follow the RED-GREEN-REFACTOR cycle and maintain 85% documentation coverage*