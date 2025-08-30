# Critical Ansible Patterns for DDD Extraction

## Core Documentation Structure
Every Ansible module contains three YAML blocks that are ESSENTIAL for maintenance documentation:

### DOCUMENTATION Block
- **Location**: Always at module top after imports
- **Format**: YAML string literal with r""" delimiters
- **Required Fields**: module, short_description, description, options
- **Complex Structures**: Nested options, suboptions, version_added tracking
- **Example Path**: `/lib/ansible/modules/file.py` lines 10-126

### EXAMPLES Block  
- **Purpose**: Real usage patterns for maintenance scenarios
- **Format**: YAML with Jinja2 templating support
- **Patterns**: Loops, conditionals, variable references
- **Critical**: These become our maintenance runbook scenarios

### RETURN Block
- **Purpose**: Documents module outputs and state changes
- **Format**: Nested dictionaries with types and samples
- **Conditional Returns**: `returned: success`, `returned: changed`
- **Critical**: Understanding what changed is key for rollback procedures

## Parameter Specification Patterns

### Required vs Optional Logic
```python
# Pattern found in 70+ modules
argument_spec = dict(
    path=dict(type='path', required=True, aliases=['dest', 'name']),
    state=dict(type='str', choices=['absent', 'directory', 'file'], default='file'),
    mode=dict(type='raw'),  # Can be octal or symbolic
)
```

### Complex Relationships
- **mutually_exclusive**: [['src', 'content']]
- **required_together**: [['owner', 'group']]
- **required_by**: {'src': ['state']}
- **required_if**: [['state', 'present', ['path']]]

## Module Utils Import Patterns

### Universal Imports (found in 90%+ of modules)
```python
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_bytes, to_native
from ansible.module_utils._text import to_text
```

### Domain-Specific Utils
- AWS modules: `ansible.module_utils.ec2`
- Network modules: `ansible.module_utils.network`
- System modules: `ansible.module_utils.common.process`

## State Management Philosophy

### Idempotency is Sacred
- Every module MUST be idempotent
- Check current state before making changes
- Return `changed=False` if already in desired state
- Pattern: `if state == 'present' and path.exists(): return`

### Check Mode Support
```python
if module.check_mode:
    # Don't make actual changes
    # Return what WOULD change
    module.exit_json(changed=would_change, diff=diff)
```

## Error Handling Hierarchy

From `/lib/ansible/module_utils/errors.py`:
- **AnsibleValidationError**: Base validation error
- **AnsibleValidationErrorMultiple**: Batch error handling
- **ArgumentTypeError**: Wrong parameter type
- **ArgumentValueError**: Invalid parameter value
- **MutuallyExclusiveError**: Conflicting parameters
- **RequiredByError**: Missing dependent parameters
- **DeprecationError**: Using deprecated features

## Why This Matters for DDD

1. **Structured Documentation Exists**: Unlike most code, Ansible modules have embedded structured documentation we can extract
2. **Maintenance Scenarios Built-In**: EXAMPLES blocks are literally maintenance runbooks
3. **Error Patterns Are Systematic**: Consistent error handling makes extraction reliable
4. **State Management Is Explicit**: We can extract rollback procedures from state logic
5. **Dependencies Are Traceable**: Import patterns reveal actual dependencies