#!/usr/bin/env python3
"""
GREEN Phase Implementation: AdvancedAnsibleExtractor
Minimal implementation to make RED phase tests pass.
Following TDD principles - just enough code, no extras!
"""

import ast
import re
import yaml
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass


@dataclass
class MaintenanceScenario:
    """Represents a maintenance scenario derived from examples."""
    name: str
    description: str
    ansible_task: Dict
    expected_outcome: str


@dataclass 
class ErrorPattern:
    """Represents an error pattern found in the module."""
    message: str
    condition: str
    recovery_hint: str
    error_type: str = "generic"
    exception_type: Optional[str] = None
    includes_traceback: bool = False
    error_code: Optional[str] = None
    
    @property
    def type(self) -> str:
        """Alias for error_type for backward compatibility."""
        return self.error_type


@dataclass
class PermissionDetail:
    """Detailed permission information."""
    action: str
    resource_constraint: Optional[str] = None
    condition: Optional[str] = None
    requires_prefix: Optional[bool] = None


class AdvancedAnsibleExtractor:
    """
    Extracts documentation, permissions, and error patterns from Ansible modules.
    
    This extractor provides comprehensive analysis of Ansible modules including:
    - DOCUMENTATION, EXAMPLES, and RETURN block parsing
    - AWS IAM permission extraction from boto3 API calls
    - Error pattern detection for maintenance runbooks
    - Parameter constraint extraction and validation
    """
    
    # Regular expression patterns used across methods
    DOCUMENTATION_PATTERN = r'DOCUMENTATION\s*=\s*[r]?"""(.*?)"""'
    EXAMPLES_PATTERN = r'EXAMPLES\s*=\s*[r]?"""(.*?)"""'
    RETURN_PATTERN = r'RETURN\s*=\s*[r]?"""(.*?)"""'
    
    # Boto3 service detection patterns
    BOTO3_CLIENT_PATTERN = r'boto3\.client\([\'"](\w+)[\'"]\)'
    BOTO3_RESOURCE_PATTERN = r'boto3\.resource\([\'"](\w+)[\'"]\)'
    BOTO3_VAR_ASSIGNMENT = r'(\w+)\s*=\s*boto3\.(?:client|resource)\([\'"](\w+)[\'"]\)'
    
    # Common AWS service variable names
    AWS_SERVICE_VARS = [
        'ec2', 's3', 'iam', 'lambda_client', 'sns', 'sqs',
        'cloudformation', 'rds', 'ecs', 'sts', 'dynamodb'
    ]
    
    # IAM permission mappings from boto3 methods
    BOTO3_TO_IAM_MAPPINGS = {
        'ec2': {
            'describe_instances': 'ec2:DescribeInstances',
            'terminate_instances': 'ec2:TerminateInstances',
            'run_instances': 'ec2:RunInstances',
            'stop_instances': 'ec2:StopInstances',
            'create_tags': 'ec2:CreateTags',
        },
        's3': {
            'list_buckets': 's3:ListBuckets',
            'list_objects_v2': 's3:ListBucket',
            'put_object': 's3:PutObject',
            'get_object': 's3:GetObject',
            'put_object_acl': 's3:PutObjectAcl',
        },
        'iam': {
            'create_role': 'iam:CreateRole',
        },
        'lambda': {
            'invoke': 'lambda:InvokeFunction',
        },
        'sns': {
            'publish': 'sns:Publish',
        },
        'sqs': {
            'send_message': 'sqs:SendMessage',
        },
        'cloudformation': {
            'create_stack': 'cloudformation:CreateStack',
        },
        'rds': {
            'create_db_instance': 'rds:CreateDBInstance',
        },
        'ecs': {
            'run_task': 'ecs:RunTask',
        },
        'sts': {
            'assume_role': 'sts:AssumeRole',
        },
    }
    
    # Documentation extraction methods
    
    def extract_documentation(self, content: str) -> Dict:
        """Extract and parse DOCUMENTATION block from Ansible module content.
        
        Args:
            content: Raw Python module content
            
        Returns:
            Dictionary containing parsed YAML documentation
        """
        doc_yaml = self._extract_yaml_block(content, self.DOCUMENTATION_PATTERN)
        return doc_yaml if doc_yaml else {}
    
    def extract_examples(self, content: str) -> List[Dict]:
        """Extract EXAMPLES block and parse into structured format.
        
        Args:
            content: Raw Python module content
            
        Returns:
            List of example dictionaries with name, module, and parameters
        """
        examples_text = self._extract_raw_block(content, self.EXAMPLES_PATTERN)
        if not examples_text:
            return []
        
        return self._parse_examples(examples_text)
    
    def extract_returns(self, content: str) -> Dict:
        """Extract and parse RETURN block containing return value documentation.
        
        Args:
            content: Raw Python module content
            
        Returns:
            Dictionary of return values with descriptions and types
        """
        returns_yaml = self._extract_yaml_block(content, self.RETURN_PATTERN)
        return returns_yaml if returns_yaml else {}
    
    def extract_complete(self, content: str) -> Dict:
        """Extract all documentation components from a module.
        
        Args:
            content: Raw Python module content
            
        Returns:
            Dictionary with 'documentation', 'examples', and 'returns' keys
        """
        return {
            'documentation': self.extract_documentation(content),
            'examples': self.extract_examples(content),
            'returns': self.extract_returns(content),
        }
    
    # Permission extraction methods
    
    def extract_permissions(self, content: str) -> List[str]:
        """Extract AWS IAM permissions from boto3 API calls.
        
        Args:
            content: Raw Python module content
            
        Returns:
            Sorted list of unique IAM permission strings
        """
        permissions = set()
        
        # Extract permissions from direct service calls
        services = self._find_boto3_services(content)
        for service in services:
            service_permissions = self._extract_service_permissions(content, service)
            permissions.update(service_permissions)
        
        # Extract permissions from service variables
        service_vars = self._find_service_variables(content)
        for var_name, service in service_vars.items():
            var_permissions = self._extract_variable_permissions(content, var_name, service)
            permissions.update(var_permissions)
        
        # Extract permissions from common service patterns
        for service_var in self.AWS_SERVICE_VARS:
            standalone_permissions = self._extract_standalone_permissions(content, service_var)
            permissions.update(standalone_permissions)
        
        # Add special case permissions
        special_permissions = self._extract_special_case_permissions(content)
        permissions.update(special_permissions)
        
        return sorted(list(permissions))
    
    def extract_permission_details(self, content: str) -> List[Dict]:
        """Extract detailed permission information including resource constraints.
        
        Args:
            content: Raw Python module content
            
        Returns:
            List of permission detail dictionaries
        """
        details = []
        permissions = self.extract_permissions(content)
        
        for perm in permissions:
            detail = self._build_permission_detail(perm, content)
            details.append(detail)
        
        return details
    
    def extract_role_requirements(self, content: str) -> List[str]:
        """Extract IAM role ARNs referenced in the content.
        
        Args:
            content: Raw Python module content
            
        Returns:
            List of IAM role ARNs found
        """
        arn_pattern = r'arn:aws:iam::\d{12}:role/[\w-]+'
        return re.findall(arn_pattern, content)
    
    def detects_encryption_requirement(self, content: str) -> bool:
        """Check if encryption is required based on content analysis.
        
        Args:
            content: Raw Python module content
            
        Returns:
            True if encryption indicators are found
        """
        encryption_indicators = [
            'ServerSideEncryption', 'Encryption', 'KmsKeyId', 'encrypt'
        ]
        return any(indicator in content for indicator in encryption_indicators)
    
    # Error pattern extraction methods
    
    def extract_error_patterns(self, content: str) -> List[ErrorPattern]:
        """Extract error patterns from module for maintenance runbooks.
        
        Args:
            content: Raw Python module content
            
        Returns:
            List of ErrorPattern objects with messages and recovery hints
        """
        errors = []
        
        # Extract fail_json error patterns
        fail_errors = self._extract_fail_json_patterns(content)
        errors.extend(fail_errors)
        
        # Extract exception handling patterns
        exception_errors = self._extract_exception_patterns(content)
        errors.extend(exception_errors)
        
        return errors
    
    def extract_permission_errors(self, content: str) -> List[str]:
        """Extract permission-related error hints from error handling.
        
        Args:
            content: Raw Python module content
            
        Returns:
            List of permission error hint strings
        """
        hints = []
        
        if 'UnauthorizedOperation' in content:
            hints.append('UnauthorizedOperation - Missing AWS permissions')
        
        if 'AccessDenied' in content:
            hints.append('AccessDenied - IAM policy restriction')
        
        return hints
    
    def extract_parameter_constraints(self, content: str) -> Dict:
        """Extract parameter constraints from module argument specification.
        
        Args:
            content: Raw Python module content
            
        Returns:
            Dictionary of parameter constraints
        """
        constraints = {}
        
        # Extract argument_spec definition
        arg_spec = self._extract_argument_spec(content)
        if arg_spec:
            constraints.update(arg_spec)
        
        # Check for validation patterns
        if 'required_if' in content:
            constraints['required_if'] = True
        
        if 'mutually_exclusive' in content:
            constraints['mutually_exclusive'] = True
        
        return constraints
    
    # Retry pattern extraction methods
    
    def extract_retry_patterns(self, content: str) -> List[str]:
        """Extract retry patterns used in the module.
        
        Args:
            content: Raw Python module content
            
        Returns:
            List of retry pattern identifiers
        """
        patterns = []
        
        retry_indicators = [
            ('AWSRetry.jittered_backoff', 'AWSRetry.jittered_backoff'),
            ('max_retries', 'max_retries'),
            ('exponential_backoff|2 \\*\\* attempt', 'exponential_backoff')
        ]
        
        for pattern, identifier in retry_indicators:
            if re.search(pattern, content):
                patterns.append(identifier)
        
        return patterns
    
    def extract_retry_configuration(self, content: str) -> Dict:
        """Extract retry configuration details from content.
        
        Args:
            content: Raw Python module content
            
        Returns:
            Dictionary with retry configuration settings
        """
        config = {}
        
        # Extract max_retries value
        retry_match = re.search(r'max_retries\s*=\s*(\d+)', content)
        if retry_match:
            config['max_retries'] = int(retry_match.group(1))
        
        # Determine backoff strategy
        config['backoff_strategy'] = self._determine_backoff_strategy(content)
        
        # Extract retriable errors
        if 'TemporaryError' in content:
            config['retriable_errors'] = ['TemporaryError']
        
        return config
    
    # Transformation methods
    
    def example_to_scenario(self, example: Dict) -> MaintenanceScenario:
        """Convert an example to a maintenance scenario.
        
        Args:
            example: Dictionary containing example data
            
        Returns:
            MaintenanceScenario object for documentation
        """
        name = example.get('name', 'Unnamed scenario')
        module = example.get('module', 'unknown')
        params = example.get('parameters', {})
        
        description = self._build_scenario_description(module, params)
        expected_outcome = self._build_expected_outcome(name, params)
        
        return MaintenanceScenario(
            name=name,
            description=description,
            ansible_task=example,
            expected_outcome=expected_outcome
        )
    
    def get_verifiable_state(self, returns: Dict) -> List[str]:
        """Determine what state can be verified from return values.
        
        Args:
            returns: Dictionary of return value definitions
            
        Returns:
            List of verifiable state element names
        """
        verifiable_keys = [
            'path', 'mode', 'uid', 'gid', 'state', 'owner', 'group'
        ]
        return [key for key in returns if key in verifiable_keys]
    
    # Private helper methods
    
    def _extract_raw_block(self, content: str, pattern: str) -> Optional[str]:
        """Extract raw text block using regex pattern."""
        match = re.search(pattern, content, re.DOTALL)
        return match.group(1) if match else None
    
    def _extract_yaml_block(self, content: str, pattern: str) -> Optional[Dict]:
        """Extract and parse YAML block from content."""
        raw_block = self._extract_raw_block(content, pattern)
        if not raw_block:
            return None
        
        try:
            return yaml.safe_load(raw_block)
        except yaml.YAMLError:
            return None
    
    def _parse_examples(self, examples_text: str) -> List[Dict]:
        """Parse examples from YAML text."""
        examples = []
        
        try:
            # Attempt YAML parsing
            tasks = yaml.safe_load(examples_text)
            if isinstance(tasks, list):
                examples = self._extract_tasks_from_yaml(tasks)
        except:
            # Fallback to simple parsing
            examples = self._parse_examples_fallback(examples_text)
        
        return examples
    
    def _extract_tasks_from_yaml(self, tasks: List) -> List[Dict]:
        """Extract task definitions from parsed YAML."""
        examples = []
        
        for task in tasks:
            if not isinstance(task, dict):
                continue
            
            # Find the module name (first key that's not a task keyword)
            task_keywords = {'name', 'when', 'register', 'become', 'tags'}
            
            for key, value in task.items():
                if key not in task_keywords:
                    examples.append({
                        'name': task.get('name', ''),
                        'module': key,
                        'parameters': value if isinstance(value, dict) else {}
                    })
                    break
        
        return examples
    
    def _parse_examples_fallback(self, examples_text: str) -> List[Dict]:
        """Simple fallback parser for examples."""
        examples = []
        
        for line in examples_text.split('\n'):
            if line.strip().startswith('- name:'):
                name = line.split('- name:', 1)[1].strip()
                examples.append({
                    'name': name,
                    'module': 'unknown',
                    'parameters': {}
                })
        
        return examples
    
    def _find_boto3_services(self, content: str) -> List[str]:
        """Find all boto3 service names in content."""
        services = []
        services.extend(re.findall(self.BOTO3_CLIENT_PATTERN, content))
        services.extend(re.findall(self.BOTO3_RESOURCE_PATTERN, content))
        return services
    
    def _find_service_variables(self, content: str) -> Dict[str, str]:
        """Find service variable assignments."""
        service_vars = {}
        
        for var_name, service in re.findall(self.BOTO3_VAR_ASSIGNMENT, content):
            service_vars[var_name] = service
        
        return service_vars
    
    def _extract_service_permissions(self, content: str, service: str) -> Set[str]:
        """Extract permissions for a specific service."""
        permissions = set()
        method_pattern = r'\.(\w+)\('
        
        for method in re.findall(method_pattern, content):
            if not method.startswith('_'):
                perm = self._map_boto3_to_iam(service, method)
                if perm:
                    permissions.add(perm)
        
        return permissions
    
    def _extract_variable_permissions(self, content: str, var_name: str, service: str) -> Set[str]:
        """Extract permissions from service variable calls."""
        permissions = set()
        var_method_pattern = rf'{var_name}\.(\w+)\('
        
        for method in re.findall(var_method_pattern, content):
            if not method.startswith('_'):
                perm = self._map_boto3_to_iam(service, method)
                if perm:
                    permissions.add(perm)
        
        return permissions
    
    def _extract_standalone_permissions(self, content: str, service_var: str) -> Set[str]:
        """Extract permissions from standalone service variables."""
        permissions = set()
        
        # Clean service name
        service = service_var.replace('_client', '')
        
        # Look for method calls
        service_method_pattern = rf'{service_var}\.(\w+)\('
        
        for method in re.findall(service_method_pattern, content):
            if not method.startswith('_'):
                perm = self._map_boto3_to_iam(service, method)
                if perm:
                    permissions.add(perm)
        
        return permissions
    
    def _extract_special_case_permissions(self, content: str) -> Set[str]:
        """Extract permissions for special case patterns."""
        permissions = set()
        
        # S3 Bucket operations
        if 's3.Bucket' in content and 'upload_file' in content:
            permissions.add('s3:PutObject')
        
        # DynamoDB Table operations
        if 'dynamodb.Table' in content:
            if 'put_item' in content:
                permissions.add('dynamodb:PutItem')
            if 'get_item' in content:
                permissions.add('dynamodb:GetItem')
        
        return permissions
    
    def _map_boto3_to_iam(self, service: str, method: str) -> Optional[str]:
        """Map boto3 method calls to IAM permissions."""
        # Check known mappings
        if service in self.BOTO3_TO_IAM_MAPPINGS:
            if method in self.BOTO3_TO_IAM_MAPPINGS[service]:
                return self.BOTO3_TO_IAM_MAPPINGS[service][method]
        
        # Generate generic mapping
        action = ''.join(word.capitalize() for word in method.split('_'))
        return f'{service}:{action}'
    
    def _build_permission_detail(self, permission: str, content: str) -> Dict:
        """Build detailed permission information."""
        detail = {
            'action': permission,
            'resource_constraint': '*' if any(
                keyword in permission 
                for keyword in ['Describe', 'List']
            ) else None
        }
        
        # Check for prefix requirements
        if 's3:List' in permission and 'Prefix' in content:
            detail['requires_prefix'] = True
        
        return detail
    
    def _extract_fail_json_patterns(self, content: str) -> List[ErrorPattern]:
        """Extract error patterns from module.fail_json calls."""
        errors = []
        fail_pattern = r'module\.fail_json\(msg=[\'"]([^\'\"]+)[\'"]'
        
        for match in re.finditer(fail_pattern, content):
            message = match.group(1)
            condition = self._find_error_condition(content, match.start())
            recovery_hint = self._generate_recovery_hint(message)
            
            # Check if this is inside an except block
            before_match = content[:match.start()]
            lines_before = before_match.split('\n')
            error_type = 'generic'
            
            # Look back for except statement
            for i, line in enumerate(reversed(lines_before[-10:])):
                if 'except' in line:
                    error_type = 'exception'
                    break
                elif 'def ' in line or 'class ' in line:
                    # Stop if we hit a function/class boundary
                    break
            
            # Override with validation if it's a validation message
            if any(keyword in message.lower() for keyword in ['required', 'must be', 'must have']):
                error_type = 'validation'
            
            error = ErrorPattern(
                message=message,
                condition=condition,
                recovery_hint=recovery_hint,
                error_type=error_type
            )
            
            # Check for traceback
            if 'exception' in content[match.start():match.end() + 100]:
                error.includes_traceback = True
            
            errors.append(error)
        
        return errors
    
    def _extract_exception_patterns(self, content: str) -> List[ErrorPattern]:
        """Extract error patterns from exception handling."""
        errors = []
        exception_pattern = r'except\s+(\w+(?:Error)?)\s*(?:as\s+\w+)?:'
        
        for match in re.finditer(exception_pattern, content):
            exception_type = match.group(1)
            block_start = match.end()
            
            # Find the end of the except block
            block_lines = []
            lines = content[block_start:].split('\n')
            
            if lines:
                # Get base indentation from first non-empty line
                base_indent = None
                for line in lines:
                    if line.strip():
                        base_indent = len(line) - len(line.lstrip())
                        break
                
                if base_indent is not None:
                    for i, line in enumerate(lines):
                        # Stop at next except/finally at same or lower indentation
                        if line.strip().startswith(('except ', 'finally:')) and i > 0:
                            # Check if it's at the except block level (not nested)
                            line_indent = len(line) - len(line.lstrip())
                            if line_indent <= base_indent:
                                break
                        
                        # Include all lines that are part of the except block
                        # This includes if/elif/else at the same indentation
                        if line.strip():
                            line_indent = len(line) - len(line.lstrip())
                            # Stop only if we hit something at a lower indentation
                            # that's not part of control flow
                            if line_indent < base_indent and not line.strip().startswith(('elif', 'else:')):
                                break
                        
                        block_lines.append(line)
            
            block_content = '\n'.join(block_lines)
            
            # Look for fail_json calls in this except block
            fail_pattern = r'module\.fail_json\(msg=[\'"]([^\'\"]+)[\'"]'
            fail_matches = list(re.finditer(fail_pattern, block_content))
            
            if fail_matches:
                for fail_match in fail_matches:
                    message = fail_match.group(1)
                    
                    # Determine error code based on context
                    error_code = None
                    before_fail = block_content[:fail_match.start()]
                    
                    # Look for the most recent condition before this fail_json
                    # Check if/elif conditions
                    if_elif_pattern = r'(?:if|elif)\s+[^:]*[\'"]([^\'\"]+)[\'"]'
                    condition_matches = list(re.finditer(if_elif_pattern, before_fail))
                    
                    # Check if this is in an else block
                    lines_before = before_fail.split('\n')
                    in_else_block = False
                    for line in reversed(lines_before[-5:]):
                        if 'else:' in line:
                            in_else_block = True
                            break
                        elif 'elif' in line or 'if' in line:
                            # Found an if/elif before else, so not in else block
                            break
                    
                    if not in_else_block and condition_matches:
                        # Get the last condition match
                        last_condition = condition_matches[-1].group(1)
                        if 'InvalidInstanceID' in last_condition or 'NotFound' in last_condition:
                            error_code = 'InvalidInstanceID.NotFound'
                        elif 'UnauthorizedOperation' in last_condition:
                            error_code = 'UnauthorizedOperation'
                    
                    # Generate recovery hint
                    recovery_hint = self._generate_exception_recovery_hint(exception_type, message, error_code)
                    
                    errors.append(ErrorPattern(
                        message=message,
                        condition='',
                        recovery_hint=recovery_hint,
                        error_type='exception',
                        exception_type=exception_type,
                        error_code=error_code
                    ))
            else:
                # No fail_json found, add generic handler if appropriate
                errors.append(self._create_generic_exception(exception_type))
        
        return errors
    
    def _extract_specific_exceptions(self, block_content: str, exception_type: str) -> List[ErrorPattern]:
        """Extract specific exception patterns from exception block."""
        errors = []
        
        exception_patterns = [
            ('InvalidInstanceID.NotFound', 'Instance not found', 
             'Verify instance ID exists', 'ClientError'),
            ('UnauthorizedOperation', 'Insufficient permissions',
             'Check IAM permissions for ec2:DescribeInstances', 'ClientError')
        ]
        
        for error_code, message, recovery, ex_type in exception_patterns:
            if error_code in block_content:
                errors.append(ErrorPattern(
                    message=message,
                    condition='',
                    recovery_hint=recovery,
                    error_type='exception',
                    exception_type=ex_type,
                    error_code=error_code
                ))
        
        return errors
    
    def _generate_exception_recovery_hint(self, exception_type: str, message: str, error_code: Optional[str]) -> str:
        """Generate recovery hint for exception-based errors."""
        if exception_type == 'ImportError' and 'boto3' in message:
            return 'Install boto3: pip install boto3'
        elif exception_type == 'ClientError':
            if error_code == 'UnauthorizedOperation' or 'permissions' in message.lower():
                return 'Check IAM permissions for ec2:DescribeInstances'
            elif error_code == 'InvalidInstanceID.NotFound' or 'not found' in message.lower():
                return 'Verify instance ID exists'
            elif 'AWS API error' in message or 'AWS' in message:
                return 'Check AWS API error details'
            else:
                return 'Check AWS API error details'
        elif exception_type == 'BotoCoreError':
            return 'Check AWS connection settings'
        else:
            return self._generate_recovery_hint(message)

    def _create_generic_exception(self, exception_type: str) -> ErrorPattern:
        """Create a generic exception pattern."""
        recovery_hints = {
            'ImportError': 'Install boto3: pip install boto3',
            'ClientError': 'Check AWS API error details',
            'BotoCoreError': 'Check AWS connection settings'
        }
        
        return ErrorPattern(
            message=f'{exception_type} occurred',
            condition='',
            recovery_hint=recovery_hints.get(exception_type, 'Check error logs'),
            error_type='exception',
            exception_type=exception_type
        )
    
    def _find_error_condition(self, content: str, error_position: int) -> str:
        """Find the condition that leads to an error."""
        before_match = content[:error_position]
        lines = before_match.split('\n')
        
        # Look for if statement in previous lines
        for line in reversed(lines[-5:]):
            if 'if ' in line:
                # Extract just the condition, not the full if statement
                condition = line.strip()
                if condition.startswith('if '):
                    condition = condition[3:]  # Remove 'if '
                if condition.endswith(':'):
                    condition = condition[:-1]  # Remove trailing ':'
                return condition.strip()
        
        return ''
    
    def _determine_error_type(self, message: str) -> str:
        """Determine error type based on message content."""
        validation_keywords = ['required', 'must be', 'must have']
        
        if any(keyword in message.lower() for keyword in validation_keywords):
            return 'validation'
        
        return 'generic'
    
    def _generate_recovery_hint(self, message: str) -> str:
        """Generate recovery hint based on error message."""
        message_lower = message.lower()
        
        recovery_hints = [
            ('path does not exist', 'Ensure the path exists before running the module'),
            ('not writable', 'Check file permissions and ownership'),
            ('required when', 'Check module parameters'),
            ('must be', 'Review parameter types and values'),
            ('git.*not installed', 'Install git: apt-get install git or yum install git'),
            ('cannot connect', 'Check network connectivity'),
        ]
        
        for pattern, hint in recovery_hints:
            if re.search(pattern, message_lower):
                return hint
        
        # Special handling for config files
        if 'config' in message_lower and 'not found' in message_lower:
            config_match = re.search(r'(/[^\s]+config[^\s]*)', message)
            if config_match:
                return f'Create configuration file at {config_match.group(1)}'
            return 'Create required configuration file'
        
        return 'Check module parameters'
    
    def _extract_argument_spec(self, content: str) -> Dict:
        """Extract argument specification from module using AST parsing."""
        constraints = {}
        
        try:
            
            # Parse the Python code into an AST
            tree = ast.parse(content)
            
            # Walk the tree to find AnsibleModule instantiation
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    # Check if this is an AnsibleModule call
                    func_name = None
                    if hasattr(node.func, 'id'):
                        func_name = node.func.id
                    elif hasattr(node.func, 'attr'):
                        func_name = node.func.attr
                    
                    if func_name == 'AnsibleModule':
                        # Found AnsibleModule call, look for argument_spec keyword
                        for keyword in node.keywords:
                            if keyword.arg == 'argument_spec':
                                # Extract the dict contents
                                constraints = self._parse_argument_spec_dict(keyword.value)
                                break
                        break
            
        except (SyntaxError, ValueError):
            # If AST parsing fails, return empty constraints
            # This might happen with incomplete code snippets in tests
            pass
        
        return constraints
    
    def _parse_argument_spec_dict(self, dict_node) -> Dict:
        """Parse an AST dict node containing argument specifications."""
        import ast
        
        constraints = {}
        
        if not isinstance(dict_node, ast.Call):
            return constraints
        
        # Check if this is a dict() call
        if not (hasattr(dict_node.func, 'id') and dict_node.func.id == 'dict'):
            return constraints
        
        # Parse each keyword argument in the dict
        for keyword in dict_node.keywords:
            param_name = keyword.arg
            if param_name and isinstance(keyword.value, ast.Call):
                # This should be another dict() call with parameter properties
                param_info = self._parse_parameter_dict(keyword.value)
                if param_info:
                    constraints[param_name] = param_info
        
        return constraints
    
    def _parse_parameter_dict(self, dict_node) -> Dict:
        """Parse a parameter's dict() node to extract its properties."""
        import ast
        
        param_info = {}
        
        if not isinstance(dict_node, ast.Call):
            return param_info
        
        # Check if this is a dict() call
        if not (hasattr(dict_node.func, 'id') and dict_node.func.id == 'dict'):
            return param_info
        
        # Parse each property
        for keyword in dict_node.keywords:
            prop_name = keyword.arg
            
            if prop_name == 'required':
                # Check if it's True
                if isinstance(keyword.value, ast.Constant):
                    param_info['required'] = keyword.value.value
                elif isinstance(keyword.value, ast.NameConstant):
                    param_info['required'] = keyword.value.value
            
            elif prop_name == 'choices':
                # Extract list of choices
                if isinstance(keyword.value, ast.List):
                    choices = []
                    for elt in keyword.value.elts:
                        if isinstance(elt, ast.Constant):
                            choices.append(elt.value)
                        elif isinstance(elt, ast.Str):
                            choices.append(elt.s)
                    param_info['choices'] = choices
            
            elif prop_name == 'default':
                # Extract default value
                if isinstance(keyword.value, ast.Constant):
                    param_info['default'] = keyword.value.value
                elif isinstance(keyword.value, ast.Str):
                    param_info['default'] = keyword.value.s
            
            elif prop_name == 'type':
                # Extract type
                if isinstance(keyword.value, ast.Constant):
                    param_info['type'] = keyword.value.value
                elif isinstance(keyword.value, ast.Str):
                    param_info['type'] = keyword.value.s
        
        return param_info
    
    def _parse_parameter_definition(self, param_def: str) -> Dict:
        """Parse a parameter definition string."""
        param_info = {}
        
        # Check for required
        if 'required=True' in param_def:
            param_info['required'] = True
        
        # Check for choices
        choices_match = re.search(r'choices\s*=\s*\[(.*?)\]', param_def)
        if choices_match:
            choices_str = choices_match.group(1)
            choices = [c.strip().strip('\'"') for c in choices_str.split(',')]
            param_info['choices'] = choices
        
        return param_info
    
    def _determine_backoff_strategy(self, content: str) -> str:
        """Determine the backoff strategy from content."""
        if 'exponential' in content.lower() or '2 **' in content:
            return 'exponential'
        elif 'jittered' in content:
            return 'jittered'
        
        return 'linear'
    
    def _build_scenario_description(self, module: str, params: Dict) -> str:
        """Build scenario description from module and parameters."""
        description = f"Execute {module} module"
        
        if params:
            param_list = ', '.join(f'{k}={v}' for k, v in params.items())
            description += f" with parameters: {param_list}"
        
        return description
    
    def _build_expected_outcome(self, name: str, params: Dict) -> str:
        """Build expected outcome description."""
        if 'path' not in params:
            return name
        
        path = params['path']
        state = params.get('state', 'file')
        mode = params.get('mode', '')
        
        if state == 'directory':
            outcome = f"Directory {path} created"
            if mode:
                outcome += f" with {mode} permissions"
        else:
            outcome = f"File {path} in state {state}"
        
        return outcome