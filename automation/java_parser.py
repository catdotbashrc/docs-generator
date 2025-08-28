#!/usr/bin/env python3
"""
Java API Parser for Sphinx Documentation - Refactored Version

Extracts API endpoints, data models, and service information from Java source code
to generate comprehensive documentation automatically.

This refactored version uses:
- Dependency injection for FileSystem operations
- Extracted constants and patterns for testability
- Specialized parser classes for single responsibility
- Comprehensive error handling
- Configurable defaults instead of hard-coded values
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Union
from datetime import datetime

from automation.filesystem.abstract import FileSystem, FileSystemError
from automation.filesystem.factory import FileSystemFactory
from automation.java_parsers import (
    WebServiceParser, ModelParser, ServiceParser, ConfigurationParser, FileFinder
)
from automation.java_parser_patterns import CONFIG, DIRECTORIES, PATTERNS
from automation.java_parser_exceptions import (
    JavaParserError, JavaProjectStructureError, JavaParserFileSystemError,
    UnsafeFilenameError, JavaFileTooLargeError
)

logger = logging.getLogger(__name__)

class JavaApiParser:
    """Parse Java source code to extract API documentation information.
    
    This refactored version uses dependency injection and specialized parsers
    for improved testability and maintainability.
    """
    
    def __init__(self, filesystem: FileSystem, project_root: Union[str, Path]):
        """Initialize JavaApiParser with dependency injection.
        
        Args:
            filesystem: FileSystem implementation for file operations
            project_root: Path to Java project root directory
        """
        self.fs = filesystem
        self.project_root = Path(project_root)
        
        # Validate project root exists
        if not self.fs.exists(self.project_root):
            raise JavaProjectStructureError(
                f"Project root does not exist", str(self.project_root)
            )
        
        # Standard Maven/Gradle project structure
        self.src_root = self.project_root / CONFIG.DEFAULT_SOURCE_PATH
        self.resources_root = self.project_root / CONFIG.DEFAULT_RESOURCES_PATH
        
        # Initialize specialized parsers
        self.webservice_parser = WebServiceParser(self.fs)
        self.model_parser = ModelParser(self.fs)
        self.service_parser = ServiceParser(self.fs)
        self.config_parser = ConfigurationParser(self.fs)
        self.file_finder = FileFinder(self.fs)
    
    @classmethod
    def from_local_path(cls, project_root: Union[str, Path]) -> 'JavaApiParser':
        """Create JavaApiParser with local filesystem.
        
        Args:
            project_root: Path to Java project root directory
            
        Returns:
            JavaApiParser instance configured for local filesystem
        """
        filesystem = FileSystemFactory.get_default(for_testing=False)
        return cls(filesystem, project_root)
    
    def extract_api_info(self) -> Dict:
        """Extract complete API information from Java project.
        
        Returns:
            Dictionary containing extracted API information with structure:
            - endpoints: List of SOAP/REST endpoints
            - data_models: List of data model classes
            - services: List of service classes
            - repositories: List of repository classes
            - configuration: Configuration from properties files
            - base_info: Basic project information
            
        Raises:
            JavaProjectStructureError: If project structure is invalid
            JavaParserError: If parsing fails
        """
        logger.info(f"Scanning Java project at {self.project_root}")
        
        try:
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
            
            logger.info(f"Successfully extracted API info: {len(api_info['endpoints'])} endpoints, "
                       f"{len(api_info['data_models'])} models, {len(api_info['services'])} services")
            
            return api_info
            
        except Exception as e:
            logger.error(f"Failed to extract API info from {self.project_root}: {e}")
            raise JavaParserError(f"API extraction failed: {e}") from e
    
    def _extract_base_info(self) -> Dict:
        """Extract basic project information from build files and configuration.
        
        Returns:
            Dictionary with project metadata like version, group, etc.
        """
        base_info = {}
        
        try:
            # Try to extract from build.gradle
            gradle_file = self.project_root / "build.gradle"
            if self.fs.exists(gradle_file):
                gradle_info = self.config_parser.parse_gradle_file(gradle_file)
                base_info.update(gradle_info)
            
            # Extract from application.properties
            props_file = self.resources_root / "application.properties"
            if self.fs.exists(props_file):
                props_info = self.config_parser.parse_properties_file(props_file)
                base_info.update(props_info)
                
        except Exception as e:
            logger.warning(f"Could not extract base project info: {e}")
        
        return base_info
    
    def _extract_endpoints(self) -> List[Dict]:
        """Extract SOAP/REST endpoints from Java source.
        
        Returns:
            List of endpoint dictionaries with operation details
        """
        endpoints = []
        
        if not self.fs.exists(self.src_root):
            logger.warning(f"Source directory not found: {self.src_root}")
            return endpoints
        
        try:
            # Find files with @WebService annotation using string pattern
            webservice_files = self.file_finder.find_files_with_pattern(
                self.src_root, 
                "@WebService"
            )
            
            for file_path in webservice_files:
                try:
                    parsed_endpoints = self.webservice_parser.parse_webservice_file(file_path)
                    # Convert dataclass to dict for compatibility
                    for endpoint in parsed_endpoints:
                        endpoints.append({
                            'operation_name': endpoint.operation_name,
                            'method_signature': endpoint.method_signature,
                            'parameters': endpoint.parameters,
                            'return_type': endpoint.return_type,
                            'namespace': endpoint.namespace,
                            'service_name': endpoint.service_name,
                            'interface_name': endpoint.interface_name,
                            'file_path': endpoint.file_path
                        })
                except Exception as e:
                    logger.error(f"Failed to parse webservice file {file_path}: {e}")
                    # Continue processing other files
                    
        except Exception as e:
            logger.error(f"Failed to extract endpoints: {e}")
            
        return endpoints
    
    def _extract_data_models(self) -> List[Dict]:
        """Extract data model classes from standard model directories.
        
        Returns:
            List of model dictionaries with class and field information
        """
        models = []
        
        if not self.fs.exists(self.src_root):
            logger.warning(f"Source directory not found: {self.src_root}")
            return models
        
        try:
            # Look for classes in model/domain packages
            for model_dir in DIRECTORIES.MODEL_DIRECTORIES:
                model_path = self.file_finder.find_directory_by_name(self.src_root, model_dir)
                if model_path:
                    try:
                        parsed_models = self.model_parser.parse_model_directory(model_path)
                        # Convert dataclass to dict for compatibility
                        for model in parsed_models:
                            models.append({
                                'class_name': model.class_name,
                                'package': model.package,
                                'file_path': model.file_path,
                                'fields': model.fields,
                                'purpose': model.purpose
                            })
                    except Exception as e:
                        logger.error(f"Failed to parse model directory {model_path}: {e}")
                        # Continue with other directories
                        
        except Exception as e:
            logger.error(f"Failed to extract data models: {e}")
            
        return models
    
    def _extract_services(self) -> List[Dict]:
        """Extract service layer classes.
        
        Returns:
            List of service dictionaries with class and dependency information
        """
        services = []
        
        if not self.fs.exists(self.src_root):
            logger.warning(f"Source directory not found: {self.src_root}")
            return services
        
        try:
            # Find service classes using pattern matching
            service_files = self.file_finder.find_files_with_pattern(
                self.src_root,
                "@Service"
            )
            
            # Also find files ending with "Service.java"
            service_pattern_files = self.file_finder.find_files_with_pattern(
                self.src_root,
                "Service"
            )
            
            # Combine and deduplicate
            all_service_files = list(set(service_files + service_pattern_files))
            
            for file_path in all_service_files:
                try:
                    service_info = self.service_parser.parse_service_file(file_path)
                    if service_info:
                        services.append({
                            'name': service_info.name,
                            'interface_name': service_info.interface_name,
                            'impl_name': service_info.impl_name,
                            'file_path': service_info.file_path,
                            'repositories': service_info.repositories
                        })
                except Exception as e:
                    logger.error(f"Failed to parse service file {file_path}: {e}")
                    # Continue with other files
                    
        except Exception as e:
            logger.error(f"Failed to extract services: {e}")
            
        return services
    
    def _extract_repositories(self) -> List[Dict]:
        """Extract repository/DAO classes.
        
        Returns:
            List of repository dictionaries with class information
        """
        repositories = []
        
        if not self.fs.exists(self.src_root):
            logger.warning(f"Source directory not found: {self.src_root}")
            return repositories
        
        try:
            # Find repository classes
            repo_annotation_files = self.file_finder.find_files_with_pattern(
                self.src_root,
                "@Repository"
            )
            
            repo_name_files = self.file_finder.find_files_with_pattern(
                self.src_root,
                "Repository"
            )
            
            dao_files = self.file_finder.find_files_with_pattern(
                self.src_root,
                "DAO"
            )
            
            # Combine and deduplicate
            all_repo_files = list(set(repo_annotation_files + repo_name_files + dao_files))
            
            for file_path in all_repo_files:
                try:
                    repo_info = self.service_parser.parse_repository_file(file_path)
                    if repo_info:
                        repositories.append({
                            'name': repo_info.name,
                            'file_path': repo_info.file_path
                        })
                except Exception as e:
                    logger.error(f"Failed to parse repository file {file_path}: {e}")
                    # Continue with other files
                    
        except Exception as e:
            logger.error(f"Failed to extract repositories: {e}")
            
        return repositories
    
    def _extract_configuration(self) -> Dict:
        """Extract configuration from properties files.
        
        Returns:
            Dictionary with configuration from various properties files
        """
        config = {}
        
        if not self.fs.exists(self.resources_root):
            logger.warning(f"Resources directory not found: {self.resources_root}")
            return config
        
        try:
            # Parse application.properties
            props_file = self.resources_root / "application.properties"
            if self.fs.exists(props_file):
                config['application'] = self.config_parser.parse_properties_file(props_file)
            
            # Look for other config files
            try:
                property_files = self.fs.glob(str(self.resources_root / "*.properties"))
                for config_file in property_files:
                    file_path = Path(config_file)
                    if file_path.name != "application.properties":
                        config[file_path.stem] = self.config_parser.parse_properties_file(file_path)
            except FileSystemError as e:
                logger.warning(f"Could not list configuration files: {e}")
                
        except Exception as e:
            logger.error(f"Failed to extract configuration: {e}")
            
        return config


def generate_java_api_docs(
    project_path: str, 
    output_dir: str, 
    template_vars: Optional[Dict] = None,
    filesystem: Optional[FileSystem] = None
) -> str:
    """
    Generate Sphinx documentation for Java API project.
    
    Args:
        project_path: Path to Java project root
        output_dir: Directory to write generated documentation
        template_vars: Optional dictionary of template variables to override defaults
        filesystem: Optional filesystem implementation (defaults to LocalFileSystem)
    
    Returns:
        Path to generated documentation file
        
    Raises:
        JavaParserError: If parsing or generation fails
        TemplateRenderingError: If template rendering fails
    """
    from automation.java_parser_exceptions import TemplateRenderingError
    from jinja2 import Template
    
    project_root = Path(project_path)
    output_path = Path(output_dir)
    
    # Use provided filesystem or create default
    if filesystem is None:
        filesystem = FileSystemFactory.get_default(for_testing=False)
    
    try:
        # Ensure output directory exists
        filesystem.create_directory(output_path)
        
        # Parse Java project with dependency injection
        parser = JavaApiParser(filesystem, project_root)
        api_info = parser.extract_api_info()
        
        # Load template
        template_path = Path(__file__).parent.parent / "docs" / "source" / "_templates" / "java-api-service.rst"
        template_content = filesystem.read_text(template_path)
        template = Template(template_content)
        
        # Prepare template variables with configurable defaults
        defaults = CONFIG.get_template_defaults()
        
        # Build template variables
        final_template_vars = {
            'client_name': 'Generated Client',  # Configurable, not hard-coded
            'service_name': project_root.name.title() + 'Service',  # Derive from project name
            'environment': defaults['environment'],
            'base_url': defaults['base_url'],
            'service_type': defaults['service_type'],
            'namespace': api_info['endpoints'][0]['namespace'] if api_info['endpoints'] else 'http://example.com/services/',
            'port': api_info['configuration'].get('application', {}).get('server.port', defaults['port']),
            'endpoints': api_info['endpoints'],
            'data_models': api_info['data_models'],
            'services': api_info['services'],
            'repositories': api_info['repositories'],
            'last_updated': datetime.now().strftime('%Y-%m-%d'),
            'generation_date': datetime.now().strftime('%Y-%m-%d'),
            'next_review_date': datetime.now().strftime('%Y-%m-%d')  # Would calculate proper review date
        }
        
        # Override with provided template variables
        if template_vars:
            final_template_vars.update(template_vars)
        
        # Render template
        try:
            rendered_doc = template.render(**final_template_vars)
        except Exception as e:
            raise TemplateRenderingError("java-api-service.rst", str(e))
        
        # Write output file
        output_file = output_path / f"{project_root.name}-api-docs.rst"
        filesystem.write_text(output_file, rendered_doc)
        
        logger.info(f"Generated Java API documentation: {output_file}")
        return str(output_file)
        
    except Exception as e:
        if isinstance(e, (JavaParserError, TemplateRenderingError)):
            raise
        raise JavaParserError(f"Documentation generation failed: {e}") from e


if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate Java API documentation')
    parser.add_argument('project_path', help='Path to Java project')
    parser.add_argument('--output', '-o', default='./docs', help='Output directory')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose logging')
    parser.add_argument('--client-name', help='Override client name in documentation')
    parser.add_argument('--service-name', help='Override service name in documentation')
    parser.add_argument('--environment', help='Override environment name')
    
    args = parser.parse_args()
    
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    try:
        # Build template variable overrides
        template_overrides = {}
        if args.client_name:
            template_overrides['client_name'] = args.client_name
        if args.service_name:
            template_overrides['service_name'] = args.service_name
        if args.environment:
            template_overrides['environment'] = args.environment
        
        output_file = generate_java_api_docs(
            args.project_path, 
            args.output,
            template_vars=template_overrides if template_overrides else None
        )
        print(f"Successfully generated documentation: {output_file}")
    except Exception as e:
        print(f"Error generating documentation: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)