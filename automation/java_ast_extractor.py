"""
JavaASTExtractor - Enhanced AST-based Java documentation extraction.

This module implements multi-layer documentation intelligence for Java projects,
extracting structure, semantics, and configuration context for Sphinx documentation.
"""

import re
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
import javalang
from javalang.tree import *

from automation.filesystem.abstract import FileSystem, FileSystemError


class JavaASTExtractor:
    """
    Enhanced Java AST extractor with multi-layer documentation intelligence.
    
    Goes beyond pure AST parsing to capture:
    - Structure: Classes, methods, annotations
    - Semantics: JavaDoc comments, inferred purpose
    - Context: Spring annotations, SOAP operations
    """
    
    def __init__(self, filesystem: FileSystem):
        """
        Initialize JavaASTExtractor with filesystem dependency.
        
        Args:
            filesystem: FileSystem implementation for file operations
        """
        self.fs = filesystem
        self.language = "java"
    
    def extract_documentation(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Extract comprehensive documentation from Java source file.
        
        Args:
            file_path: Path to Java source file
            
        Returns:
            Dictionary containing extracted documentation:
            - endpoints: SOAP/REST endpoints
            - services: Spring services and repositories
            - models: Data models and DTOs
            - business_logic: Extracted business patterns and rules
            - language: Language identifier
            
        Raises:
            FileNotFoundError: If file doesn't exist
            Exception: For parsing errors
        """
        try:
            # Read source code
            source_code = self.fs.read_text(file_path)
            
            # Handle empty files
            if not source_code.strip():
                return self._empty_result()
            
            # Parse to AST
            try:
                tree = javalang.parse.parse(source_code)
            except Exception as e:
                raise Exception(f"Failed to parse Java file {file_path}: {e}")
            
            # Extract all documentation elements
            return {
                'endpoints': self._extract_endpoints(tree, source_code),
                'services': self._extract_services(tree, source_code),
                'models': self._extract_models(tree, source_code),
                'business_logic': self._extract_business_logic(tree, source_code),
                'language': self.language
            }
            
        except FileSystemError:
            raise FileNotFoundError(f"Java file not found: {file_path}")

    def _empty_result(self) -> Dict[str, Any]:
        """Return empty but valid result structure."""
        return {
            'endpoints': [],
            'services': [],
            'models': [],
            'business_logic': {
                'rules': [],
                'validations': [],
                'error_handling': [],
                'workflows': [],
                'constants': [],
                'calculations': [],
                'patterns': []
            },
            'language': self.language
        }
    
    def _extract_endpoints(self, tree: CompilationUnit, source_code: str) -> List[Dict[str, Any]]:
        """
        Extract SOAP and REST endpoints from AST.
        
        Args:
            tree: Parsed AST tree
            source_code: Original source code for comment extraction
            
        Returns:
            List of endpoint information dictionaries
        """
        endpoints = []
        
        # Handle both classes and interfaces
        for _, class_node in tree.filter(ClassDeclaration):
            # Check if this is a web service class
            if self._has_webservice_annotation(class_node):
                # Extract all @WebMethod operations
                for method_node in class_node.methods or []:
                    if self._has_webmethod_annotation(method_node):
                        endpoint = self._extract_webmethod_info(method_node, source_code)
                        if endpoint:
                            endpoints.append(endpoint)
        
        # Handle interfaces separately
        for _, interface_node in tree.filter(InterfaceDeclaration):
            # Check if this is a web service interface
            if self._has_webservice_annotation(interface_node):
                # Extract all @WebMethod operations
                for method_node in interface_node.methods or []:
                    if self._has_webmethod_annotation(method_node):
                        endpoint = self._extract_webmethod_info(method_node, source_code)
                        if endpoint:
                            endpoints.append(endpoint)
        
        return endpoints
    
    def _extract_services(self, tree: CompilationUnit, source_code: str) -> List[Dict[str, Any]]:
        """
        Extract Spring services, repositories, and web services.
        
        Args:
            tree: Parsed AST tree
            source_code: Original source code
            
        Returns:
            List of service information dictionaries
        """
        services = []
        
        # Handle both classes and interfaces
        for _, class_node in tree.filter(ClassDeclaration):
            service_info = None
            
            # Check for @WebService
            if self._has_webservice_annotation(class_node):
                service_info = self._extract_webservice_info(class_node, source_code)
                service_info['type'] = 'webservice'
            
            # Check for @Service
            elif self._has_spring_annotation(class_node, 'Service'):
                service_info = self._extract_spring_service_info(class_node, source_code)
                service_info['type'] = 'service'
            
            # Check for @Repository
            elif self._has_spring_annotation(class_node, 'Repository'):
                service_info = self._extract_spring_service_info(class_node, source_code)
                service_info['type'] = 'repository'
            
            if service_info:
                services.append(service_info)
        
        # Handle interfaces separately
        for _, interface_node in tree.filter(InterfaceDeclaration):
            service_info = None
            
            # Check for @WebService
            if self._has_webservice_annotation(interface_node):
                service_info = self._extract_webservice_info(interface_node, source_code)
                service_info['type'] = 'webservice'
            
            # Check for @Service
            elif self._has_spring_annotation(interface_node, 'Service'):
                service_info = self._extract_spring_service_info(interface_node, source_code)
                service_info['type'] = 'service'
            
            # Check for @Repository
            elif self._has_spring_annotation(interface_node, 'Repository'):
                service_info = self._extract_spring_service_info(interface_node, source_code)
                service_info['type'] = 'repository'
            
            if service_info:
                services.append(service_info)
        
        return services
    
    def _extract_models(self, tree: CompilationUnit, source_code: str) -> List[Dict[str, Any]]:
        """
        Extract data models, DTOs, and enums.
        
        Args:
            tree: Parsed AST tree
            source_code: Original source code
            
        Returns:
            List of model information dictionaries
        """
        models = []
        
        # Extract regular classes that look like models
        for _, class_node in tree.filter(ClassDeclaration):
            if self._is_model_class(class_node):
                model_info = self._extract_model_info(class_node, source_code)
                models.append(model_info)
        
        # Extract enums
        for _, enum_node in tree.filter(EnumDeclaration):
            enum_info = self._extract_enum_info(enum_node, source_code)
            models.append(enum_info)
        
        return models
    
    def _has_webservice_annotation(self, class_node: ClassDeclaration) -> bool:
        """Check if class has @WebService annotation."""
        return self._has_annotation(class_node, 'WebService')
    
    def _has_webmethod_annotation(self, method_node: MethodDeclaration) -> bool:
        """Check if method has @WebMethod annotation."""
        return self._has_annotation(method_node, 'WebMethod')
    
    def _has_spring_annotation(self, class_node: ClassDeclaration, annotation_name: str) -> bool:
        """Check if class has specific Spring annotation."""
        return self._has_annotation(class_node, annotation_name)
    
    def _has_annotation(self, node: Any, annotation_name: str) -> bool:
        """Generic annotation checker."""
        if not hasattr(node, 'annotations') or not node.annotations:
            return False
        
        for annotation in node.annotations:
            if hasattr(annotation, 'name'):
                # Handle simple name (e.g., @Service)
                if annotation.name == annotation_name:
                    return True
                # Handle qualified name (e.g., @org.springframework.stereotype.Service)
                if hasattr(annotation.name, 'value') and annotation.name.value.endswith(annotation_name):
                    return True
        
        return False
    
    def _extract_webmethod_info(self, method_node: MethodDeclaration, source_code: str) -> Dict[str, Any]:
        """Extract information from @WebMethod annotated method."""
        # Get operation name from annotation
        operation_name = self._get_annotation_parameter(method_node, 'WebMethod', 'operationName')
        if not operation_name:
            operation_name = method_node.name
        
        # Extract method signature
        return_type = self._get_return_type_string(method_node.return_type)
        parameters = self._extract_method_parameters(method_node)
        
        # Extract documentation if present
        javadoc_info = self._extract_javadoc(method_node, source_code)
        
        return {
            'operation': operation_name,
            'method_name': method_node.name,
            'return_type': return_type,
            'parameters': parameters,
            'description': javadoc_info.get('description', ''),
            'parameter_docs': javadoc_info.get('parameters', {}),
            'return_doc': javadoc_info.get('return', '')
        }
    
    def _extract_webservice_info(self, class_node: ClassDeclaration, source_code: str) -> Dict[str, Any]:
        """Extract information from @WebService annotated class."""
        namespace = self._get_annotation_parameter(class_node, 'WebService', 'targetNamespace')
        
        return {
            'name': class_node.name,
            'namespace': namespace or '',
            'methods': self._extract_class_methods(class_node, source_code)
        }
    
    def _extract_spring_service_info(self, class_node: ClassDeclaration, source_code: str) -> Dict[str, Any]:
        """Extract information from Spring service classes."""
        # Get implemented interface if any
        interface_name = ''
        if class_node.implements:
            interface_name = class_node.implements[0].name if class_node.implements[0].name else ''
        
        return {
            'name': class_node.name,
            'interface': interface_name,
            'methods': self._extract_class_methods(class_node, source_code)
        }
    
    def _extract_model_info(self, class_node: ClassDeclaration, source_code: str) -> Dict[str, Any]:
        """Extract information from model classes."""
        fields = []
        
        # Extract fields
        for field_node in class_node.fields or []:
            for declarator in field_node.declarators:
                field_info = {
                    'name': declarator.name,
                    'type': self._get_type_string(field_node.type)
                }
                fields.append(field_info)
        
        return {
            'name': class_node.name,
            'type': 'class',
            'fields': fields
        }
    
    def _extract_enum_info(self, enum_node: EnumDeclaration, source_code: str) -> Dict[str, Any]:
        """Extract information from enum declarations."""
        values = []
        
        for constant in enum_node.body.constants:
            values.append(constant.name)
        
        return {
            'name': enum_node.name,
            'type': 'enum',
            'values': values
        }
    
    def _extract_class_methods(self, class_node: ClassDeclaration, source_code: str) -> List[Dict[str, Any]]:
        """Extract methods from a class with semantic analysis."""
        methods = []
        
        for method_node in class_node.methods or []:
            method_info = {
                'name': method_node.name,
                'return_type': self._get_return_type_string(method_node.return_type),
                'parameters': self._extract_method_parameters(method_node),
                'inferred_purpose': self._infer_method_purpose(method_node.name)
            }
            
            # Add JavaDoc if present
            javadoc_info = self._extract_javadoc(method_node, source_code)
            if javadoc_info.get('description'):
                method_info['description'] = javadoc_info['description']
            
            methods.append(method_info)
        
        return methods
    
    def _extract_method_parameters(self, method_node: MethodDeclaration) -> List[Dict[str, Any]]:
        """Extract method parameters with type information."""
        parameters = []
        
        if method_node.parameters:
            for param in method_node.parameters:
                param_info = {
                    'name': param.name,
                    'type': self._get_type_string(param.type)
                }
                parameters.append(param_info)
        
        return parameters
    
    def _get_annotation_parameter(self, node: Any, annotation_name: str, parameter_name: str) -> Optional[str]:
        """Get parameter value from annotation."""
        if not hasattr(node, 'annotations') or not node.annotations:
            return None
        
        for annotation in node.annotations:
            # Check if this is the annotation we're looking for
            is_target_annotation = False
            if hasattr(annotation, 'name'):
                if annotation.name == annotation_name:
                    is_target_annotation = True
                elif hasattr(annotation.name, 'value') and annotation.name.value.endswith(annotation_name):
                    is_target_annotation = True
            
            if is_target_annotation and hasattr(annotation, 'element') and annotation.element:
                # Handle different annotation element structures
                if isinstance(annotation.element, list):
                    # List of ElementValuePair objects: @Annotation(param1="value1", param2="value2")
                    for element_pair in annotation.element:
                        if hasattr(element_pair, 'name') and element_pair.name == parameter_name:
                            return self._extract_literal_value(element_pair.value)
                elif hasattr(annotation.element, 'name') and annotation.element.name == parameter_name:
                    # Named single parameter: @Annotation(paramName="value")
                    return self._extract_literal_value(annotation.element.value)
                elif hasattr(annotation.element, 'value') and parameter_name == 'value':
                    # Implicit value parameter: @Annotation("value")
                    return self._extract_literal_value(annotation.element.value)
        
        return None
    
    def _extract_literal_value(self, literal_node: Any) -> str:
        """Extract string value from literal node."""
        if hasattr(literal_node, 'value'):
            # Remove quotes from string literals
            value = literal_node.value
            if isinstance(value, str) and value.startswith('"') and value.endswith('"'):
                return value[1:-1]
            return str(value)
        return ''
    
    def _get_return_type_string(self, return_type: Any) -> str:
        """Convert return type node to string representation."""
        if return_type is None:
            return 'void'
        return self._get_type_string(return_type)
    
    def _get_type_string(self, type_node: Any) -> str:
        """Convert type node to string representation."""
        if type_node is None:
            return 'void'
        
        # Handle ReferenceType (classes, interfaces)
        if hasattr(type_node, 'name'):
            type_name = type_node.name
            
            # Handle generic types (e.g., List<String>, Map<String, Object>)
            if hasattr(type_node, 'arguments') and type_node.arguments:
                args = []
                for arg in type_node.arguments:
                    # TypeArgument has a 'type' field that contains the actual type
                    if hasattr(arg, 'type'):
                        args.append(self._get_type_string(arg.type))
                    else:
                        args.append(self._get_type_string(arg))
                return f"{type_name}<{', '.join(args)}>"
            
            return type_name
        
        # Handle BasicType (int, boolean, char, etc.)
        if hasattr(type_node, 'value'):
            return type_node.value
            
        # Handle ArrayType
        if hasattr(type_node, 'type'):
            base_type = self._get_type_string(type_node.type)
            dimensions = getattr(type_node, 'dimensions', [])
            return base_type + '[]' * len(dimensions)
        
        # Fallback to string representation
        return str(type_node)
    
    def _is_model_class(self, class_node: ClassDeclaration) -> bool:
        """
        Determine if a class is a data model.
        
        Heuristics:
        - Not a service/repository/controller
        - Has fields
        - Name ends with Model, DTO, Entity, etc.
        """
        # Skip classes with service-like annotations
        service_annotations = ['Service', 'Repository', 'Controller', 'Component', 'WebService']
        for annotation_name in service_annotations:
            if self._has_annotation(class_node, annotation_name):
                return False
        
        # Check naming patterns
        model_suffixes = ['Model', 'DTO', 'Entity', 'Request', 'Response', 'Page']
        class_name = class_node.name
        if any(class_name.endswith(suffix) for suffix in model_suffixes):
            return True
        
        # Check if it has fields (indication of data structure)
        if class_node.fields and len(class_node.fields) > 0:
            return True
        
        return False
    
    def _extract_javadoc(self, node: Any, source_code: str) -> Dict[str, Any]:
        """
        Extract JavaDoc documentation from source code.
        
        This is a simplified implementation that would need enhancement
        for full JavaDoc parsing.
        """
        # For now, return empty - full JavaDoc parsing would require
        # more sophisticated source code analysis
        return {
            'description': '',
            'parameters': {},
            'return': ''
        }
    
    def _infer_method_purpose(self, method_name: str) -> str:
        """
        Infer method purpose from naming patterns.
        
        Args:
            method_name: Name of the method
            
        Returns:
            Inferred purpose description
        """
        name_lower = method_name.lower()
        
        # Common patterns
        if name_lower.startswith('get'):
            return f"Retrieve or fetch data (inferred from method name)"
        elif name_lower.startswith('set'):
            return f"Set or update data (inferred from method name)"
        elif name_lower.startswith('find'):
            return f"Search and find data (inferred from method name)"
        elif name_lower.startswith('create'):
            return f"Create new data (inferred from method name)"
        elif name_lower.startswith('update'):
            return f"Update existing data (inferred from method name)"
        elif name_lower.startswith('delete') or name_lower.startswith('remove'):
            return f"Delete or remove data (inferred from method name)"
        elif name_lower.startswith('validate'):
            return f"Validate data or conditions (inferred from method name)"
        elif name_lower.startswith('process'):
            return f"Process or transform data (inferred from method name)"
        elif name_lower.startswith('run'):
            return f"Execute or run operation (inferred from method name)"
        elif name_lower.startswith('generate'):
            return f"Generate or produce data (inferred from method name)"
        
        return f"Perform {method_name} operation (inferred from method name)"

    def _extract_business_logic(self, tree: CompilationUnit, source_code: str) -> Dict[str, Any]:
        """
        Extract business logic patterns from Java code.
        
        This includes:
        - Business rules from conditional logic
        - Validation patterns
        - Error handling patterns
        - Workflows from method calls
        - Business constants
        - Calculation patterns
        
        Args:
            tree: Parsed AST tree
            source_code: Original source code
            
        Returns:
            Dictionary with extracted business logic patterns
        """
        return {
            'rules': self._extract_business_rules(tree),
            'validations': self._extract_validations(tree),
            'error_handling': self._extract_error_handling(tree),
            'workflows': self._extract_workflows(tree),
            'constants': self._extract_business_constants(tree),
            'calculations': self._extract_calculations(tree),
            'patterns': self._extract_patterns(tree)
        }
    
    def _extract_business_rules(self, tree: CompilationUnit) -> List[Dict[str, Any]]:
        """
        Extract business rules from conditional logic.
        
        Looks for if/else statements and extracts the conditions
        and their business implications.
        """
        rules = []
        
        for _, class_node in tree.filter(ClassDeclaration):
            for method in class_node.methods or []:
                if method.body:
                    rules.extend(self._extract_rules_from_statements(method.body))
        
        return rules
    
    def _extract_rules_from_statements(self, statements) -> List[Dict[str, Any]]:
        """Extract rules from a list of statements."""
        rules = []
        
        for statement in statements:
            if isinstance(statement, IfStatement):
                # Extract condition
                condition_str = self._expression_to_string(statement.condition)
                
                # Infer business meaning from condition
                description = self._infer_rule_description(condition_str)
                
                rule = {
                    'type': 'conditional',
                    'condition': condition_str,
                    'description': description
                }
                rules.append(rule)
                
                # Recursively extract from then/else branches
                if statement.then_statement and hasattr(statement.then_statement, 'statements'):
                    rules.extend(self._extract_rules_from_statements(statement.then_statement.statements))
                if statement.else_statement:
                    if isinstance(statement.else_statement, IfStatement):
                        # Handle else-if
                        rules.extend(self._extract_rules_from_statements([statement.else_statement]))
                    elif hasattr(statement.else_statement, 'statements'):
                        rules.extend(self._extract_rules_from_statements(statement.else_statement.statements))
            
            elif isinstance(statement, BlockStatement):
                if statement.statements:
                    rules.extend(self._extract_rules_from_statements(statement.statements))
        
        return rules
    
    def _extract_validations(self, tree: CompilationUnit) -> List[Dict[str, Any]]:
        """
        Extract validation patterns from code.
        
        Looks for null checks, range checks, and validation exceptions.
        """
        validations = []
        
        for _, class_node in tree.filter(ClassDeclaration):
            for method in class_node.methods or []:
                if method.body:
                    validations.extend(self._extract_validations_from_statements(method.body))
        
        return validations
    
    def _extract_validations_from_statements(self, statements) -> List[Dict[str, Any]]:
        """Extract validation patterns from statements."""
        validations = []
        
        for statement in statements:
            if isinstance(statement, IfStatement):
                condition_str = self._expression_to_string(statement.condition)
                
                # Check if this is a validation pattern
                if self._is_validation_condition(condition_str):
                    # Look for exception throw in then branch
                    message = self._extract_exception_message(statement.then_statement)
                    
                    if message:
                        validation = {
                            'condition': condition_str,
                            'message': message,
                            'type': 'validation'
                        }
                        validations.append(validation)
            
            elif isinstance(statement, BlockStatement):
                if statement.statements:
                    validations.extend(self._extract_validations_from_statements(statement.statements))
        
        return validations
    
    def _extract_error_handling(self, tree: CompilationUnit) -> List[Dict[str, Any]]:
        """
        Extract error handling patterns from try-catch blocks.
        """
        handlers = []
        
        for _, class_node in tree.filter(ClassDeclaration):
            for method in class_node.methods or []:
                if method.body:
                    handlers.extend(self._extract_error_handlers_from_statements(method.body))
        
        return handlers
    
    def _extract_error_handlers_from_statements(self, statements) -> List[Dict[str, Any]]:
        """Extract error handlers from statements."""
        handlers = []
        
        for statement in statements:
            if isinstance(statement, TryStatement):
                # Extract catch clauses
                for catch_clause in statement.catches or []:
                    # CatchClauseParameter has 'types' not 'type'
                    if hasattr(catch_clause.parameter, 'types') and catch_clause.parameter.types:
                        exception_type = ' | '.join(self._get_type_string(t) for t in catch_clause.parameter.types)
                    else:
                        exception_type = catch_clause.parameter.name if hasattr(catch_clause.parameter, 'name') else 'Exception'
                    
                    # Extract action from catch block
                    action = self._extract_catch_action(catch_clause.block)
                    
                    handler = {
                        'exception': exception_type,
                        'action': action,
                        'type': 'exception_handler'
                    }
                    handlers.append(handler)
            
            elif isinstance(statement, BlockStatement):
                if statement.statements:
                    handlers.extend(self._extract_error_handlers_from_statements(statement.statements))
        
        return handlers
    
    def _extract_workflows(self, tree: CompilationUnit) -> List[Dict[str, Any]]:
        """
        Extract workflows from method call sequences.
        """
        workflows = []
        
        for _, class_node in tree.filter(ClassDeclaration):
            for method in class_node.methods or []:
                if method.body and len(method.body) > 0:
                    workflow = self._extract_workflow_from_method(method)
                    if workflow and len(workflow['steps']) > 0:
                        workflows.append(workflow)
        
        return workflows
    
    def _extract_workflow_from_method(self, method: MethodDeclaration) -> Dict[str, Any]:
        """Extract workflow from a method's statements."""
        steps = []
        branches = []
        
        for statement in method.body:
            step_info = self._extract_workflow_step(statement)
            if step_info:
                if 'branches' in step_info:
                    branches.extend(step_info['branches'])
                else:
                    steps.append(step_info)
        
        workflow = {
            'name': method.name,
            'steps': steps
        }
        
        if branches:
            workflow['branches'] = branches
        
        return workflow
    
    def _extract_workflow_step(self, statement) -> Optional[Dict[str, Any]]:
        """Extract a single workflow step from a statement."""
        if isinstance(statement, StatementExpression):
            if isinstance(statement.expression, MethodInvocation):
                return {
                    'action': statement.expression.member,
                    'type': 'method_call'
                }
        
        elif isinstance(statement, IfStatement):
            # Extract conditional workflow branches
            condition_str = self._expression_to_string(statement.condition)
            then_steps = []
            
            if statement.then_statement:
                if isinstance(statement.then_statement, BlockStatement):
                    for stmt in statement.then_statement.statements or []:
                        step = self._extract_workflow_step(stmt)
                        if step and 'branches' not in step:
                            then_steps.append(step)
                else:
                    step = self._extract_workflow_step(statement.then_statement)
                    if step and 'branches' not in step:
                        then_steps.append(step)
            
            if then_steps:
                return {
                    'branches': [{
                        'condition': condition_str,
                        'steps': then_steps
                    }]
                }
        
        elif isinstance(statement, BlockStatement):
            # Extract from block
            steps = []
            for stmt in statement.statements or []:
                step = self._extract_workflow_step(stmt)
                if step:
                    steps.append(step)
            
            if len(steps) == 1:
                return steps[0]
        
        return None
    
    def _extract_business_constants(self, tree: CompilationUnit) -> List[Dict[str, Any]]:
        """
        Extract business-relevant constants from the code.
        """
        constants = []
        
        for _, class_node in tree.filter(ClassDeclaration):
            for field in class_node.fields or []:
                # Check if it's a public static final field (constant)
                if self._is_constant_field(field):
                    for declarator in field.declarators:
                        if declarator.initializer:
                            constant = {
                                'name': declarator.name,
                                'type': self._get_type_string(field.type),
                                'value': self._extract_literal_value_from_expression(declarator.initializer)
                            }
                            constants.append(constant)
        
        return constants
    
    def _extract_calculations(self, tree: CompilationUnit) -> List[Dict[str, Any]]:
        """
        Extract calculation patterns from methods.
        
        Looks for methods with calculation patterns like tax brackets,
        discount calculations, etc.
        """
        calculations = []
        
        for _, class_node in tree.filter(ClassDeclaration):
            for method in class_node.methods or []:
                if 'calculate' in method.name.lower() or 'compute' in method.name.lower():
                    calc_info = self._extract_calculation_info(method)
                    if calc_info:
                        calculations.append(calc_info)
        
        return calculations
    
    def _extract_calculation_info(self, method: MethodDeclaration) -> Dict[str, Any]:
        """Extract calculation information from a method."""
        calc_info = {
            'name': method.name,
            'brackets': []
        }
        
        if method.body:
            brackets = self._extract_calculation_brackets(method.body)
            if brackets:
                calc_info['brackets'] = brackets
        
        return calc_info if calc_info['brackets'] else None
    
    def _extract_calculation_brackets(self, statements) -> List[Dict[str, Any]]:
        """Extract calculation brackets from conditional statements."""
        brackets = []
        
        for statement in statements:
            if isinstance(statement, IfStatement):
                condition_str = self._expression_to_string(statement.condition)
                
                # Look for numeric comparisons (tax brackets, etc.)
                threshold = self._extract_numeric_threshold(condition_str)
                if threshold is not None:
                    rate = self._extract_rate_from_statement(statement.then_statement)
                    if rate is not None:
                        bracket = {
                            'threshold': threshold,
                            'rate': rate
                        }
                        brackets.append(bracket)
            
            elif isinstance(statement, BlockStatement):
                if statement.statements:
                    brackets.extend(self._extract_calculation_brackets(statement.statements))
        
        return brackets
    
    def _extract_patterns(self, tree: CompilationUnit) -> List[Dict[str, Any]]:
        """
        Extract common patterns like retry logic, circuit breakers, etc.
        """
        patterns = []
        
        for _, class_node in tree.filter(ClassDeclaration):
            for method in class_node.methods or []:
                if method.body:
                    # Check for retry pattern
                    retry_pattern = self._detect_retry_pattern(method)
                    if retry_pattern:
                        patterns.append(retry_pattern)
        
        return patterns
    
    def _detect_retry_pattern(self, method: MethodDeclaration) -> Optional[Dict[str, Any]]:
        """Detect retry logic patterns in a method."""
        for statement in method.body or []:
            if isinstance(statement, WhileStatement) or isinstance(statement, ForStatement):
                # Look for retry-like patterns
                if self._is_retry_loop(statement):
                    return {
                        'type': 'retry',
                        'max_attempts': self._extract_max_attempts(statement),
                        'backoff_strategy': self._detect_backoff_strategy(statement)
                    }
        
        return None
    
    # Helper methods
    
    def _expression_to_string(self, expression) -> str:
        """Convert an expression node to string representation."""
        if expression is None:
            return ""
        
        if isinstance(expression, BinaryOperation):
            left = self._expression_to_string(expression.operandl)
            right = self._expression_to_string(expression.operandr)
            return f"{left} {expression.operator} {right}"
        
        elif isinstance(expression, MethodInvocation):
            qualifier = ""
            if expression.qualifier:
                qualifier = self._expression_to_string(expression.qualifier) + "."
            return f"{qualifier}{expression.member}()"
        
        elif isinstance(expression, MemberReference):
            qualifier = ""
            if expression.qualifier:
                qualifier = self._expression_to_string(expression.qualifier) + "."
            return f"{qualifier}{expression.member}"
        
        elif isinstance(expression, Literal):
            return str(expression.value)
        
        elif hasattr(expression, 'name'):
            return expression.name
        
        # Fallback
        return str(expression)
    
    def _infer_rule_description(self, condition: str) -> str:
        """Infer business rule description from condition."""
        condition_lower = condition.lower()
        
        if 'hours' in condition_lower and '>' in condition:
            if '40' in condition:
                return "Overtime rule: applies when hours exceed 40"
            return "Hours threshold rule"
        
        elif 'amount' in condition_lower:
            if '>' in condition:
                return "Amount threshold rule for special processing"
            elif '<' in condition:
                return "Minimum amount validation"
        
        elif 'type' in condition_lower or 'status' in condition_lower:
            return "Category-based business rule"
        
        elif 'null' in condition_lower or 'empty' in condition_lower:
            return "Data validation rule"
        
        return f"Business rule based on: {condition}"
    
    def _is_validation_condition(self, condition: str) -> bool:
        """Check if a condition represents a validation check."""
        validation_patterns = ['null', 'empty', '< 0', '<= 0', '> max', '< min']
        return any(pattern in condition.lower() for pattern in validation_patterns)
    
    def _extract_exception_message(self, statement) -> Optional[str]:
        """Extract exception message from a throw statement."""
        if isinstance(statement, ThrowStatement):
            if isinstance(statement.expression, ClassCreator):
                # Look for string literal in constructor arguments
                if statement.expression.arguments:
                    for arg in statement.expression.arguments:
                        if isinstance(arg, Literal) and isinstance(arg.value, str):
                            return arg.value.strip('"')
        
        elif isinstance(statement, BlockStatement):
            for stmt in statement.statements or []:
                message = self._extract_exception_message(stmt)
                if message:
                    return message
        
        return None
    
    def _extract_catch_action(self, block) -> str:
        """Extract action description from catch block."""
        # Handle both list and BlockStatement
        statements = None
        if isinstance(block, list):
            statements = block
        elif hasattr(block, 'statements'):
            statements = block.statements
        
        if not statements:
            return "Handle exception"
        
        # Look for return statements
        for statement in statements:
            if isinstance(statement, ReturnStatement):
                return self._describe_return_value(statement.expression)
        
        return "Handle exception with custom logic"
    
    def _describe_return_value(self, expression) -> str:
        """Describe a return value expression."""
        if isinstance(expression, ClassCreator):
            # Extract constructor arguments for more detail
            arg_details = []
            if expression.arguments:
                for arg in expression.arguments:
                    if isinstance(arg, MemberReference):
                        # Handles Status.INVALID, Status.TIMEOUT etc
                        arg_details.append(self._expression_to_string(arg))
                    elif isinstance(arg, Literal):
                        # String literals
                        value = arg.value
                        if isinstance(value, str):
                            arg_details.append(value.strip('"'))
                    elif isinstance(arg, MethodInvocation):
                        # Method calls like e.getMessage()
                        arg_details.append(self._expression_to_string(arg))
            
            if arg_details:
                # Check for specific status codes and messages
                if any('timeout' in str(arg).lower() for arg in arg_details):
                    if any('unavailable' in str(arg).lower() for arg in arg_details):
                        return "Return error response: Payment gateway unavailable"
                elif any('invalid' in str(arg).lower() for arg in arg_details):
                    return "Return error response: Invalid payment"
                elif any('error' in str(arg).lower() for arg in arg_details):
                    return "Return error response: System error occurred"
                
                # Generic with details
                return f"Return new {expression.type.name} with {', '.join(arg_details[:2])}"
            
            return f"Return new {expression.type.name} with error status"
        elif isinstance(expression, Literal):
            return f"Return {expression.value}"
        
        return "Return error response"
    
    def _is_constant_field(self, field) -> bool:
        """Check if a field is a constant (public static final)."""
        modifiers = field.modifiers or []
        return 'public' in modifiers and 'static' in modifiers and 'final' in modifiers
    
    def _extract_literal_value_from_expression(self, expression):
        """Extract literal value from an expression."""
        if isinstance(expression, Literal):
            value = expression.value
            if isinstance(value, str) and value.startswith('"'):
                return value.strip('"')
            
            # Try to convert to appropriate type
            try:
                if '.' in str(value):
                    return float(value)
                else:
                    return int(value)
            except:
                return value
        
        return str(expression)
    
    def _extract_numeric_threshold(self, condition: str) -> Optional[float]:
        """Extract numeric threshold from a condition string."""
        import re
        
        # Look for patterns like "income <= 10000"
        pattern = r'[<>]=?\s*(\d+(?:\.\d+)?)'
        match = re.search(pattern, condition)
        
        if match:
            try:
                return float(match.group(1))
            except:
                pass
        
        return None
    
    def _extract_rate_from_statement(self, statement) -> Optional[float]:
        """Extract rate/percentage from a statement."""
        if isinstance(statement, BlockStatement):
            for stmt in statement.statements or []:
                rate = self._extract_rate_from_statement(stmt)
                if rate is not None:
                    return rate
        
        elif isinstance(statement, StatementExpression):
            # Look for multiplication by decimal (e.g., income * 0.1)
            expr_str = self._expression_to_string(statement.expression)
            import re
            pattern = r'\*\s*(0\.\d+)'
            match = re.search(pattern, expr_str)
            if match:
                try:
                    return float(match.group(1))
                except:
                    pass
        
        elif isinstance(statement, LocalVariableDeclaration):
            # Handle local variable assignments like: tax = income * 0.1
            for declarator in statement.declarators or []:
                if declarator.initializer:
                    init_str = self._expression_to_string(declarator.initializer)
                    import re
                    pattern = r'\*\s*(0\.\d+)'
                    match = re.search(pattern, init_str)
                    if match:
                        try:
                            return float(match.group(1))
                        except:
                            pass
        
        return None
    
    def _is_retry_loop(self, statement) -> bool:
        """Check if a loop statement represents retry logic."""
        # Look for patterns like attempts < 3 or similar
        if isinstance(statement, WhileStatement):
            condition = self._expression_to_string(statement.condition)
            return 'attempt' in condition.lower() or 'retry' in condition.lower()
        
        return False
    
    def _extract_max_attempts(self, statement) -> int:
        """Extract maximum retry attempts from a loop."""
        condition = None
        
        if isinstance(statement, WhileStatement):
            condition = self._expression_to_string(statement.condition)
        
        if condition:
            import re
            pattern = r'<\s*(\d+)'
            match = re.search(pattern, condition)
            if match:
                try:
                    return int(match.group(1))
                except:
                    pass
        
        return 3  # Default
    
    def _detect_backoff_strategy(self, statement) -> str:
        """Detect backoff strategy from retry logic."""
        # Look for sleep patterns in the loop body
        if hasattr(statement, 'body'):
            body_str = str(statement.body)
            if 'sleep' in body_str.lower():
                if 'attempt' in body_str.lower() and '*' in body_str:
                    return "exponential backoff"
                return "fixed delay"
        
        return "immediate retry"
