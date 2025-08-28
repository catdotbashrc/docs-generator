#!/usr/bin/env python3
"""
Java API Parser for Sphinx Documentation

Extracts API endpoints, data models, and service information from Java source code
to generate comprehensive documentation automatically.
"""

import os
import re
import ast
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class JavaApiParser:
    """Parse Java source code to extract API documentation information."""
    
    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)
        self.src_root = self.project_root / "src" / "main" / "java"
        self.resources_root = self.project_root / "src" / "main" / "resources"
    
    def extract_api_info(self) -> Dict:
        """Extract complete API information from Java project."""
        logger.info(f"Scanning Java project at {self.project_root}")
        
        api_info = {
            'endpoints': [],
            'data_models': [],
            'services': [],
            'repositories': [],
            'configuration': {},
            'base_info': {}
        }
        
        # Extract base project information
        api_info['base_info'] = self._extract_base_info()
        
        # Find and parse web service endpoints
        api_info['endpoints'] = self._extract_endpoints()
        
        # Extract data models
        api_info['data_models'] = self._extract_data_models()
        
        # Extract service layer information
        api_info['services'] = self._extract_services()
        
        # Extract repository information
        api_info['repositories'] = self._extract_repositories()
        
        # Parse configuration files
        api_info['configuration'] = self._extract_configuration()
        
        return api_info
    
    def _extract_base_info(self) -> Dict:
        """Extract basic project information."""
        base_info = {}
        
        # Try to extract from build.gradle or pom.xml
        gradle_file = self.project_root / "build.gradle"
        if gradle_file.exists():
            base_info.update(self._parse_gradle_file(gradle_file))
        
        # Extract from application.properties
        props_file = self.resources_root / "application.properties"
        if props_file.exists():
            base_info.update(self._parse_properties_file(props_file))
        
        return base_info
    
    def _extract_endpoints(self) -> List[Dict]:
        """Extract SOAP/REST endpoints from Java source."""
        endpoints = []
        
        # Find files with @WebService annotation
        webservice_files = self._find_files_with_pattern(
            self.src_root, 
            r"@WebService"
        )
        
        for file_path in webservice_files:
            endpoints.extend(self._parse_webservice_file(file_path))
        
        return endpoints
    
    def _extract_data_models(self) -> List[Dict]:
        """Extract data model classes."""
        models = []
        
        # Look for classes in model/domain packages
        model_dirs = [
            "model", "models", "domain", "dto", "entity", "entities"
        ]
        
        for model_dir in model_dirs:
            model_path = self._find_directory_by_name(self.src_root, model_dir)
            if model_path:
                models.extend(self._parse_model_directory(model_path))
        
        return models
    
    def _extract_services(self) -> List[Dict]:
        """Extract service layer classes."""
        services = []
        
        # Find service classes
        service_files = self._find_files_with_pattern(
            self.src_root,
            r"@Service|class \w*Service"
        )
        
        for file_path in service_files:
            service_info = self._parse_service_file(file_path)
            if service_info:
                services.append(service_info)
        
        return services
    
    def _extract_repositories(self) -> List[Dict]:
        """Extract repository/DAO classes."""
        repositories = []
        
        # Find repository classes
        repo_files = self._find_files_with_pattern(
            self.src_root,
            r"@Repository|Repository\.java|DAO\.java"
        )
        
        for file_path in repo_files:
            repo_info = self._parse_repository_file(file_path)
            if repo_info:
                repositories.append(repo_info)
        
        return repositories
    
    def _extract_configuration(self) -> Dict:
        """Extract configuration from properties files."""
        config = {}
        
        # Parse application.properties
        props_file = self.resources_root / "application.properties"
        if props_file.exists():
            config['application'] = self._parse_properties_file(props_file)
        
        # Look for other config files
        for config_file in self.resources_root.glob("*.properties"):
            if config_file.name != "application.properties":
                config[config_file.stem] = self._parse_properties_file(config_file)
        
        return config
    
    def _parse_webservice_file(self, file_path: Path) -> List[Dict]:
        """Parse a Java file containing @WebService annotations."""
        endpoints = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract namespace from @WebService annotation
            namespace_match = re.search(
                r'@WebService\([^)]*targetNamespace\s*=\s*"([^"]*)"',
                content
            )
            namespace = namespace_match.group(1) if namespace_match else ""
            
            # Extract service name
            service_match = re.search(
                r'@WebService\([^)]*serviceName\s*=\s*"([^"]*)"',
                content
            )
            service_name = service_match.group(1) if service_match else ""
            
            # Extract interface name
            interface_match = re.search(r'public interface (\w+)', content)
            interface_name = interface_match.group(1) if interface_match else ""
            
            # Find all @WebMethod annotations
            method_pattern = r'@WebMethod\([^)]*operationName\s*=\s*"([^"]*)"[^)]*\)[^{]*?(\w+\s+\w+\([^)]*\))'
            methods = re.finditer(method_pattern, content, re.MULTILINE | re.DOTALL)
            
            for method in methods:
                operation_name = method.group(1)
                method_signature = method.group(2).strip()
                
                # Parse method signature to extract parameters
                params = self._parse_method_parameters(method_signature, content)
                return_type = self._extract_return_type(method_signature)
                
                endpoint = {
                    'operation_name': operation_name,
                    'method_signature': method_signature,
                    'parameters': params,
                    'return_type': return_type,
                    'namespace': namespace,
                    'service_name': service_name,
                    'interface_name': interface_name,
                    'file_path': str(file_path.relative_to(self.project_root))
                }
                
                endpoints.append(endpoint)
        
        except Exception as e:
            logger.error(f"Error parsing webservice file {file_path}: {e}")
        
        return endpoints
    
    def _parse_method_parameters(self, method_signature: str, full_content: str) -> List[Dict]:
        """Extract parameter information from method signature."""
        params = []
        
        # Extract parameters from method signature
        param_pattern = r'@WebParam\([^)]*name\s*=\s*"([^"]*)"[^)]*\)\s*(\w+)\s+(\w+)'
        param_matches = re.finditer(param_pattern, full_content)
        
        for param_match in param_matches:
            param_name = param_match.group(1)
            param_type = param_match.group(2)
            param_var = param_match.group(3)
            
            params.append({
                'name': param_name,
                'type': param_type,
                'variable_name': param_var,
                'example_value': self._generate_example_value(param_type),
                'description': f"Parameter of type {param_type}"
            })
        
        return params
    
    def _extract_return_type(self, method_signature: str) -> str:
        """Extract return type from method signature."""
        # Simple regex to extract return type
        match = re.match(r'(\w+(?:<[^>]+>)?)\s+\w+\s*\(', method_signature)
        return match.group(1) if match else "void"
    
    def _generate_example_value(self, param_type: str) -> str:
        """Generate example values for parameters based on type."""
        type_examples = {
            'String': 'example_string',
            'int': '123',
            'Integer': '123', 
            'long': '123456789',
            'Long': '123456789',
            'boolean': 'true',
            'Boolean': 'true',
            'Date': '2024-01-01',
            'LocalDate': '2024-01-01',
            'LocalDateTime': '2024-01-01T10:00:00'
        }
        
        return type_examples.get(param_type, f'example_{param_type.lower()}')
    
    def _parse_model_directory(self, model_path: Path) -> List[Dict]:
        """Parse all model classes in a directory."""
        models = []
        
        for java_file in model_path.glob("**/*.java"):
            model_info = self._parse_model_file(java_file)
            if model_info:
                models.append(model_info)
        
        return models
    
    def _parse_model_file(self, file_path: Path) -> Optional[Dict]:
        """Parse a single model class file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract class name
            class_match = re.search(r'public class (\w+)', content)
            if not class_match:
                return None
            
            class_name = class_match.group(1)
            
            # Extract package
            package_match = re.search(r'package ([^;]+);', content)
            package = package_match.group(1) if package_match else ""
            
            # Extract fields
            fields = self._extract_class_fields(content)
            
            return {
                'class_name': class_name,
                'package': package,
                'file_path': str(file_path.relative_to(self.project_root)),
                'fields': fields,
                'purpose': f"Data model for {class_name}"
            }
        
        except Exception as e:
            logger.error(f"Error parsing model file {file_path}: {e}")
            return None
    
    def _extract_class_fields(self, content: str) -> List[Dict]:
        """Extract field information from class content."""
        fields = []
        
        # Pattern to match field declarations
        field_pattern = r'(private|public|protected)\s+(\w+(?:<[^>]+>)?)\s+(\w+)\s*[;=]'
        field_matches = re.finditer(field_pattern, content)
        
        for field_match in field_matches:
            visibility = field_match.group(1)
            field_type = field_match.group(2)
            field_name = field_match.group(3)
            
            fields.append({
                'name': field_name,
                'type': field_type,
                'visibility': visibility,
                'description': f"{visibility} field of type {field_type}"
            })
        
        return fields
    
    def _parse_service_file(self, file_path: Path) -> Optional[Dict]:
        """Parse a service class file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract class name
            class_match = re.search(r'public class (\w+)', content)
            if not class_match:
                return None
            
            class_name = class_match.group(1)
            
            # Find corresponding interface if exists
            interface_name = class_name.replace("Impl", "").replace("Implementation", "")
            
            # Extract repository dependencies
            repo_deps = re.findall(r'@Autowired[^;]*?(\w*Repository|\w*DAO)\s+(\w+)', content)
            
            return {
                'name': class_name,
                'interface_name': interface_name,
                'impl_name': class_name,
                'file_path': str(file_path.relative_to(self.project_root)),
                'repositories': [repo[0] for repo in repo_deps]
            }
        
        except Exception as e:
            logger.error(f"Error parsing service file {file_path}: {e}")
            return None
    
    def _parse_repository_file(self, file_path: Path) -> Optional[Dict]:
        """Parse a repository/DAO class file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract class/interface name
            class_match = re.search(r'public (?:class|interface) (\w+)', content)
            if not class_match:
                return None
            
            class_name = class_match.group(1)
            
            return {
                'name': class_name,
                'file_path': str(file_path.relative_to(self.project_root))
            }
        
        except Exception as e:
            logger.error(f"Error parsing repository file {file_path}: {e}")
            return None
    
    def _parse_properties_file(self, file_path: Path) -> Dict:
        """Parse a Java properties file."""
        properties = {}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if '=' in line:
                            key, value = line.split('=', 1)
                            properties[key.strip()] = value.strip()
        
        except Exception as e:
            logger.error(f"Error parsing properties file {file_path}: {e}")
        
        return properties
    
    def _parse_gradle_file(self, file_path: Path) -> Dict:
        """Extract basic info from build.gradle."""
        gradle_info = {}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract version
            version_match = re.search(r"version\s*=\s*['\"]([^'\"]*)['\"]", content)
            if version_match:
                gradle_info['version'] = version_match.group(1)
            
            # Extract group
            group_match = re.search(r"group\s*=\s*['\"]([^'\"]*)['\"]", content)
            if group_match:
                gradle_info['group'] = group_match.group(1)
        
        except Exception as e:
            logger.error(f"Error parsing gradle file {file_path}: {e}")
        
        return gradle_info
    
    def _find_files_with_pattern(self, search_dir: Path, pattern: str) -> List[Path]:
        """Find Java files containing specific patterns."""
        matching_files = []
        
        for java_file in search_dir.glob("**/*.java"):
            try:
                with open(java_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if re.search(pattern, content):
                        matching_files.append(java_file)
            except Exception as e:
                logger.warning(f"Could not read {java_file}: {e}")
        
        return matching_files
    
    def _find_directory_by_name(self, search_root: Path, dir_name: str) -> Optional[Path]:
        """Find first directory matching the given name."""
        for item in search_root.rglob("*"):
            if item.is_dir() and item.name.lower() == dir_name.lower():
                return item
        return None


def generate_java_api_docs(project_path: str, output_dir: str) -> str:
    """
    Generate Sphinx documentation for Java API project.
    
    Args:
        project_path: Path to Java project root
        output_dir: Directory to write generated documentation
    
    Returns:
        Path to generated documentation file
    """
    project_root = Path(project_path)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Parse Java project
    parser = JavaApiParser(project_root)
    api_info = parser.extract_api_info()
    
    # Generate documentation using template
    from jinja2 import Template
    
    template_path = Path(__file__).parent.parent / "docs" / "source" / "_templates" / "java-api-service.rst"
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    template = Template(template_content)
    
    # Prepare template variables
    template_vars = {
        'client_name': 'DSNY',
        'service_name': 'UtilizationService',
        'environment': 'Production',
        'base_url': 'http://localhost:8080',
        'service_type': 'SOAP Web Service',
        'namespace': api_info['endpoints'][0]['namespace'] if api_info['endpoints'] else 'http://example.com',
        'port': api_info['configuration'].get('application', {}).get('server.port', '8080'),
        'endpoints': api_info['endpoints'],
        'data_models': api_info['data_models'],
        'services': api_info['services'],
        'repositories': api_info['repositories'],
        'last_updated': '2024-01-01',
        'generation_date': '2024-01-01',
        'next_review_date': '2024-04-01'
    }
    
    # Render template
    rendered_doc = template.render(**template_vars)
    
    # Write output file
    output_file = output_path / f"{project_root.name}-api-docs.rst"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(rendered_doc)
    
    logger.info(f"Generated Java API documentation: {output_file}")
    return str(output_file)


if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate Java API documentation')
    parser.add_argument('project_path', help='Path to Java project')
    parser.add_argument('--output', '-o', default='./docs', help='Output directory')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose logging')
    
    args = parser.parse_args()
    
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    try:
        output_file = generate_java_api_docs(args.project_path, args.output)
        print(f"Successfully generated documentation: {output_file}")
    except Exception as e:
        print(f"Error generating documentation: {e}")
        sys.exit(1)