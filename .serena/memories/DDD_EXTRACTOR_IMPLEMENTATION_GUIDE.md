# DDD Extractor Implementation Guide - From Ansible Analysis

## Core Extractor Architecture Pattern

### Base Extractor Class Structure
```python
class AnsibleModuleExtractor(InfrastructureExtractor):
    """Extract maintenance documentation from Ansible modules."""
    
    def extract(self, file_path: str) -> Dict:
        """Main extraction entry point."""
        content = self._read_file(file_path)
        
        return {
            'documentation': self._extract_documentation_block(content),
            'examples': self._extract_examples_block(content),
            'returns': self._extract_return_block(content),
            'parameters': self._extract_parameters(content),
            'dependencies': self._extract_dependencies(content),
            'error_patterns': self._extract_error_patterns(content),
            'states': self._extract_state_management(content),
            'permissions': self._extract_permission_requirements(content),
        }
```

## Pattern Detection Regular Expressions

### Documentation Block Patterns
```python
# DOCUMENTATION block extraction
DOCUMENTATION_PATTERN = r'DOCUMENTATION\s*=\s*r?["\']{{3}}(.*?)["\']{{3}}'
EXAMPLES_PATTERN = r'EXAMPLES\s*=\s*r?["\']{{3}}(.*?)["\']{{3}}'
RETURN_PATTERN = r'RETURN\s*=\s*r?["\']{{3}}(.*?)["\']{{3}}'

# Import patterns for dependency extraction
IMPORT_PATTERNS = [
    r'^from\s+([\w\.]+)\s+import',
    r'^import\s+([\w\.]+)',
    r'ansible\.module_utils\.([\w\.]+)',
]

# Error handling patterns
ERROR_PATTERNS = [
    r'module\.fail_json\s*\((.*?)\)',
    r'raise\s+(\w+Error)\s*\(',
    r'except\s+(\w+)\s+as',
]

# State management patterns
STATE_PATTERNS = [
    r'state\s*=\s*["\'](\w+)["\']',
    r'if\s+state\s*==\s*["\'](\w+)["\']',
    r'state\s+in\s+\[(.*?)\]',
]
```

## Extraction Method Implementations

### Extract Documentation Block
```python
def _extract_documentation_block(self, content: str) -> Dict:
    """Extract and parse DOCUMENTATION block."""
    match = re.search(self.DOCUMENTATION_PATTERN, content, re.DOTALL)
    if not match:
        return {}
    
    yaml_content = match.group(1)
    try:
        docs = yaml.safe_load(yaml_content)
        return self._normalize_documentation(docs)
    except yaml.YAMLError as e:
        # Log error but don't fail
        return {'parse_error': str(e), 'raw': yaml_content}
```

### Extract Parameters with Validation Rules
```python
def _extract_parameters(self, content: str) -> Dict:
    """Extract parameter specifications and validation rules."""
    params = {}
    
    # Look for argument_spec definition
    arg_spec_match = re.search(
        r'argument_spec\s*=\s*dict\((.*?)\)',
        content,
        re.DOTALL
    )
    
    if arg_spec_match:
        # Parse parameter definitions
        param_text = arg_spec_match.group(1)
        
        # Extract each parameter
        param_pattern = r'(\w+)\s*=\s*dict\((.*?)\)'
        for match in re.finditer(param_pattern, param_text, re.DOTALL):
            param_name = match.group(1)
            param_spec = match.group(2)
            
            params[param_name] = {
                'required': 'required=True' in param_spec,
                'type': self._extract_type(param_spec),
                'default': self._extract_default(param_spec),
                'choices': self._extract_choices(param_spec),
                'aliases': self._extract_aliases(param_spec),
            }
    
    # Also extract validation relationships
    params['_validation'] = {
        'mutually_exclusive': self._extract_mutex(content),
        'required_together': self._extract_required_together(content),
        'required_by': self._extract_required_by(content),
    }
    
    return params
```

### Extract Error Patterns for Maintenance
```python
def _extract_error_patterns(self, content: str) -> List[Dict]:
    """Extract error handling patterns for troubleshooting."""
    errors = []
    
    # Find all fail_json calls
    for match in re.finditer(r'module\.fail_json\((.*?)\)', content, re.DOTALL):
        error_args = match.group(1)
        
        # Extract error message
        msg_match = re.search(r'msg\s*=\s*["\']([^"\']+)["\']', error_args)
        if msg_match:
            errors.append({
                'type': 'fail_json',
                'message': msg_match.group(1),
                'context': self._get_context(content, match.start()),
            })
    
    # Find exception handling
    for match in re.finditer(r'except\s+(\w+)\s+as\s+\w+:(.*?)(?=except|\Z)', content, re.DOTALL):
        exception_type = match.group(1)
        handler_body = match.group(2)
        
        errors.append({
            'type': 'exception',
            'exception': exception_type,
            'handler': handler_body.strip()[:200],  # First 200 chars
        })
    
    return errors
```

### Extract State Management Logic
```python
def _extract_state_management(self, content: str) -> Dict:
    """Extract state transitions and idempotency logic."""
    states = {
        'supported_states': set(),
        'default_state': None,
        'state_transitions': [],
        'check_mode_support': False,
    }
    
    # Find all state values
    for match in re.finditer(r'state\s*==\s*["\'](\w+)["\']', content):
        states['supported_states'].add(match.group(1))
    
    # Check for check mode support
    if 'module.check_mode' in content:
        states['check_mode_support'] = True
    
    # Look for state transition logic
    transition_pattern = r'if\s+state\s*==\s*["\']([\w]+)["\'](.*?)(?=if\s+state|elif|else|\Z)'
    for match in re.finditer(transition_pattern, content, re.DOTALL):
        from_state = match.group(1)
        logic = match.group(2)[:500]  # First 500 chars of logic
        
        states['state_transitions'].append({
            'from': from_state,
            'logic_summary': self._summarize_logic(logic),
        })
    
    return states
```

## Maintenance Scenario Generation

### Generate Scenarios from Extracted Data
```python
def generate_maintenance_scenarios(extracted_data: Dict) -> List[Dict]:
    """Generate maintenance scenarios from extracted patterns."""
    scenarios = []
    
    # Error recovery scenarios
    for error in extracted_data.get('error_patterns', []):
        scenarios.append({
            'type': 'error_recovery',
            'trigger': error['message'],
            'procedure': f"1. Check {error['context']}\n2. Verify parameters\n3. Review logs",
            'automation_ready': True,
        })
    
    # State change scenarios
    for state in extracted_data.get('states', {}).get('supported_states', []):
        scenarios.append({
            'type': 'state_change',
            'operation': f"Change to {state}",
            'pre_checks': f"Verify current state is not {state}",
            'rollback': f"Revert to previous state",
            'automation_ready': True,
        })
    
    # Permission denied scenarios
    if extracted_data.get('permissions'):
        scenarios.append({
            'type': 'permission_issue',
            'trigger': 'Permission denied error',
            'procedure': f"1. Check required permissions: {extracted_data['permissions']}\n2. Verify user/service account\n3. Update IAM/filesystem permissions",
            'automation_ready': False,
        })
    
    return scenarios
```

## Validation and Quality Checks

### Validate Extracted Documentation
```python
def validate_extraction(extracted_data: Dict) -> Dict:
    """Validate extraction quality and completeness."""
    validation_results = {
        'score': 0,
        'missing': [],
        'warnings': [],
    }
    
    # Check for required documentation elements
    if not extracted_data.get('documentation'):
        validation_results['missing'].append('DOCUMENTATION block')
    
    if not extracted_data.get('parameters'):
        validation_results['missing'].append('Parameter specifications')
    
    # Check for maintenance-critical patterns
    if not extracted_data.get('error_patterns'):
        validation_results['warnings'].append('No error handling patterns found')
    
    if not extracted_data.get('states'):
        validation_results['warnings'].append('No state management found')
    
    # Calculate quality score
    score = 100
    score -= len(validation_results['missing']) * 20
    score -= len(validation_results['warnings']) * 10
    validation_results['score'] = max(0, score)
    
    return validation_results
```

## Performance Optimization Tips

### Caching and Memoization
```python
class OptimizedExtractor:
    def __init__(self):
        self._pattern_cache = {}
        self._yaml_cache = {}
    
    @lru_cache(maxsize=128)
    def _compile_pattern(self, pattern: str):
        """Cache compiled regex patterns."""
        return re.compile(pattern, re.DOTALL)
    
    def _parse_yaml_cached(self, yaml_content: str):
        """Cache parsed YAML to avoid re-parsing."""
        content_hash = hash(yaml_content)
        if content_hash not in self._yaml_cache:
            self._yaml_cache[content_hash] = yaml.safe_load(yaml_content)
        return self._yaml_cache[content_hash]
```

### Batch Processing
```python
def extract_batch(self, file_paths: List[str]) -> Dict:
    """Extract from multiple files efficiently."""
    results = {}
    
    # Use multiprocessing for CPU-bound extraction
    with multiprocessing.Pool() as pool:
        extraction_results = pool.map(self.extract, file_paths)
    
    for path, result in zip(file_paths, extraction_results):
        results[path] = result
    
    return results
```

## Integration with DDD Framework

### Coverage Calculation Integration
```python
def calculate_ansible_coverage(extracted_data: Dict) -> float:
    """Calculate documentation coverage for Ansible module."""
    weights = {
        'documentation': 0.3,
        'examples': 0.2,
        'parameters': 0.2,
        'error_patterns': 0.1,
        'states': 0.1,
        'dependencies': 0.1,
    }
    
    score = 0
    for key, weight in weights.items():
        if extracted_data.get(key):
            # Simple presence check - can be more sophisticated
            score += weight
    
    return score
```

## Common Pitfalls to Avoid

1. **Don't assume YAML is well-formed** - Always use try/except
2. **Handle missing blocks gracefully** - Not all modules have all blocks
3. **Watch for performance** - Regex on large files can be slow
4. **Preserve formatting** - Maintain original indentation in extracted examples
5. **Version compatibility** - Patterns change between Ansible versions
6. **Unicode handling** - International contributors use various encodings