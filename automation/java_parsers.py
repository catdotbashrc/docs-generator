"""
Specialized parser classes for different aspects of Java source code.

This module contains focused parser classes that handle specific types of 
Java code elements, promoting single responsibility and testability.
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Union
from dataclasses import dataclass

from automation.filesystem.abstract import FileSystem, FileSystemError
from automation.java_parser_patterns import PATTERNS, TYPE_MAPPINGS, DIRECTORIES
from automation.java_parser_exceptions import (
    JavaParserError, JavaSyntaxError, AnnotationParsingError, 
    JavaParserFileSystemError
)

logger = logging.getLogger(__name__)


@dataclass
class ParsedEndpoint:
    """Data class for parsed SOAP/REST endpoints."""
    operation_name: str
    method_signature: str
    parameters: List[Dict]
    return_type: str
    namespace: str = ""
    service_name: str = ""
    interface_name: str = ""
    file_path: str = ""


@dataclass
class ParsedModel:
    """Data class for parsed data models."""
    class_name: str
    package: str
    file_path: str
    fields: List[Dict]
    purpose: str = ""


@dataclass
class ParsedService:
    """Data class for parsed service classes."""
    name: str
    interface_name: str = ""
    impl_name: str = ""
    file_path: str = ""
    repositories: List[str] = None
    
    def __post_init__(self):
        if self.repositories is None:
            self.repositories = []


class WebServiceParser:
    """Parser specialized for SOAP web services and endpoints."""
    
    def __init__(self, filesystem: FileSystem):
        self.fs = filesystem
    
    def parse_webservice_file(self, file_path: Union[str, Path]) -> List[ParsedEndpoint]:
        """Parse a Java file containing @WebService annotations."""
        endpoints = []
        
        try:
            content = self.fs.read_text(file_path)
            
            # Extract basic service information
            namespace = self._extract_namespace(content)
            service_name = self._extract_service_name(content)
            interface_name = self._extract_interface_name(content)
            
            # Find all WebMethod annotations
            for method_match in PATTERNS.WEBMETHOD_OPERATION.finditer(content):
                try:
                    operation_name = method_match.group(1)
                    method_signature = method_match.group(2).strip()
                    
                    # Parse method details
                    parameters = self._parse_method_parameters(method_signature, content)
                    return_type = self._extract_return_type(method_signature)
                    
                    endpoint = ParsedEndpoint(
                        operation_name=operation_name,
                        method_signature=method_signature,
                        parameters=parameters,
                        return_type=return_type,
                        namespace=namespace,
                        service_name=service_name,
                        interface_name=interface_name,
                        file_path=str(file_path)
                    )
                    
                    endpoints.append(endpoint)
                    
                except Exception as e:
                    raise AnnotationParsingError(
                        "WebMethod", str(file_path), f"Error parsing method: {e}"
                    )
        
        except FileSystemError as e:
            raise JavaParserFileSystemError(e, "parsing webservice", str(file_path))
        except Exception as e:
            logger.error(f"Error parsing webservice file {file_path}: {e}")
            raise JavaParserError(f"Failed to parse webservice file {file_path}: {e}")
        
        return endpoints
    
    def _extract_namespace(self, content: str) -> str:
        """Extract namespace from @WebService annotation."""
        match = PATTERNS.WEBSERVICE_NAMESPACE.search(content)
        return match.group(1) if match else ""
    
    def _extract_service_name(self, content: str) -> str:
        """Extract service name from @WebService annotation."""
        match = PATTERNS.WEBSERVICE_NAME.search(content)
        return match.group(1) if match else ""
    
    def _extract_interface_name(self, content: str) -> str:
        """Extract interface name from class declaration."""
        match = PATTERNS.PUBLIC_INTERFACE.search(content)
        return match.group(1) if match else ""
    
    def _parse_method_parameters(self, method_signature: str, full_content: str) -> List[Dict]:
        """Extract parameter information from method signature."""
        params = []
        
        for param_match in PATTERNS.WEBPARAM.finditer(full_content):
            param_name = param_match.group(1)
            param_type = param_match.group(2)
            param_var = param_match.group(3)
            
            params.append({
                'name': param_name,
                'type': param_type,
                'variable_name': param_var,
                'example_value': TYPE_MAPPINGS.get_example_value(param_type),
                'description': TYPE_MAPPINGS.get_parameter_description(param_type)
            })
        
        return params
    
    def _extract_return_type(self, method_signature: str) -> str:
        """Extract return type from method signature."""
        match = PATTERNS.METHOD_RETURN_TYPE.match(method_signature)
        return match.group(1) if match else "void"


class ModelParser:
    """Parser specialized for Java data models and DTOs."""
    
    def __init__(self, filesystem: FileSystem):
        self.fs = filesystem
    
    def parse_model_file(self, file_path: Union[str, Path]) -> Optional[ParsedModel]:
        """Parse a single model class file."""
        try:
            content = self.fs.read_text(file_path)
            
            # Extract class name
            class_match = PATTERNS.PUBLIC_CLASS.search(content)
            if not class_match:
                return None
            
            class_name = class_match.group(1)
            
            # Extract package
            package_match = PATTERNS.PACKAGE_DECLARATION.search(content)
            package = package_match.group(1) if package_match else ""
            
            # Extract fields
            fields = self._extract_class_fields(content)
            
            return ParsedModel(
                class_name=class_name,
                package=package,
                file_path=str(file_path),
                fields=fields,
                purpose=f"Data model for {class_name}"
            )
        
        except FileSystemError as e:
            raise JavaParserFileSystemError(e, "parsing model", str(file_path))
        except Exception as e:
            logger.error(f"Error parsing model file {file_path}: {e}")
            return None
    
    def parse_model_directory(self, model_path: Path) -> List[ParsedModel]:
        """Parse all model classes in a directory."""
        models = []
        
        try:
            java_files = self.fs.glob(str(model_path / "**/*.java"))
            for java_file in java_files:
                model_info = self.parse_model_file(java_file)
                if model_info:
                    models.append(model_info)
        
        except FileSystemError as e:
            raise JavaParserFileSystemError(e, "listing model directory", str(model_path))
        
        return models
    
    def _extract_class_fields(self, content: str) -> List[Dict]:
        """Extract field information from class content."""
        fields = []
        
        for field_match in PATTERNS.FIELD_DECLARATION.finditer(content):
            visibility = field_match.group(1)
            field_type = field_match.group(2)
            field_name = field_match.group(3)
            
            fields.append({
                'name': field_name,
                'type': field_type,
                'visibility': visibility,
                'description': TYPE_MAPPINGS.get_field_description(
                    field_name, field_type, visibility
                )
            })
        
        return fields


class ServiceParser:
    """Parser specialized for Spring services and repositories."""
    
    def __init__(self, filesystem: FileSystem):
        self.fs = filesystem
    
    def parse_service_file(self, file_path: Union[str, Path]) -> Optional[ParsedService]:
        """Parse a service class file."""
        try:
            content = self.fs.read_text(file_path)
            
            # Extract class name
            class_match = PATTERNS.PUBLIC_CLASS.search(content)
            if not class_match:
                return None
            
            class_name = class_match.group(1)
            
            # Find corresponding interface if exists
            interface_name = self._infer_interface_name(class_name)
            
            # Extract repository dependencies
            repositories = self._extract_repository_dependencies(content)
            
            return ParsedService(
                name=class_name,
                interface_name=interface_name,
                impl_name=class_name,
                file_path=str(file_path),
                repositories=repositories
            )
        
        except FileSystemError as e:
            raise JavaParserFileSystemError(e, "parsing service", str(file_path))
        except Exception as e:
            logger.error(f"Error parsing service file {file_path}: {e}")
            return None
    
    def parse_repository_file(self, file_path: Union[str, Path]) -> Optional[ParsedService]:
        """Parse a repository/DAO class file."""
        try:
            content = self.fs.read_text(file_path)
            
            # Extract class/interface name
            class_match = PATTERNS.PUBLIC_CLASS.search(content)
            if not class_match:
                interface_match = PATTERNS.PUBLIC_INTERFACE.search(content)
                if not interface_match:
                    return None
                class_name = interface_match.group(1)
            else:
                class_name = class_match.group(1)
            
            return ParsedService(
                name=class_name,
                file_path=str(file_path)
            )
        
        except FileSystemError as e:
            raise JavaParserFileSystemError(e, "parsing repository", str(file_path))
        except Exception as e:
            logger.error(f"Error parsing repository file {file_path}: {e}")
            return None
    
    def _infer_interface_name(self, class_name: str) -> str:
        """Infer interface name from implementation class name."""
        if class_name.endswith("Impl"):
            return class_name[:-4]  # Remove "Impl" suffix
        elif class_name.endswith("Implementation"):
            return class_name[:-14]  # Remove "Implementation" suffix
        return class_name
    
    def _extract_repository_dependencies(self, content: str) -> List[str]:
        """Extract repository dependencies from @Autowired annotations."""
        repositories = []
        for repo_match in PATTERNS.AUTOWIRED_REPOSITORY.finditer(content):
            repositories.append(repo_match.group(1))
        return repositories


class ConfigurationParser:
    """Parser specialized for configuration files (properties, gradle)."""
    
    def __init__(self, filesystem: FileSystem):
        self.fs = filesystem
    
    def parse_properties_file(self, file_path: Union[str, Path]) -> Dict:
        """Parse a Java properties file."""
        properties = {}
        
        try:
            content = self.fs.read_text(file_path)
            for line in content.split('\n'):
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        properties[key.strip()] = value.strip()
        
        except FileSystemError as e:
            raise JavaParserFileSystemError(e, "parsing properties", str(file_path))
        except Exception as e:
            logger.error(f"Error parsing properties file {file_path}: {e}")
        
        return properties
    
    def parse_gradle_file(self, file_path: Union[str, Path]) -> Dict:
        """Extract basic info from build.gradle."""
        gradle_info = {}
        
        try:
            content = self.fs.read_text(file_path)
            
            # Extract version
            version_match = PATTERNS.GRADLE_VERSION.search(content)
            if version_match:
                gradle_info['version'] = version_match.group(1)
            
            # Extract group
            group_match = PATTERNS.GRADLE_GROUP.search(content)
            if group_match:
                gradle_info['group'] = group_match.group(1)
        
        except FileSystemError as e:
            raise JavaParserFileSystemError(e, "parsing gradle", str(file_path))
        except Exception as e:
            logger.error(f"Error parsing gradle file {file_path}: {e}")
        
        return gradle_info


class FileFinder:
    """Utility class for finding Java files with specific patterns."""
    
    def __init__(self, filesystem: FileSystem):
        self.fs = filesystem
    
    def find_files_with_pattern(self, search_dir: Path, pattern: str) -> List[Path]:
        """Find Java files containing specific patterns."""
        matching_files = []
        
        try:
            java_files = self.fs.glob(str(search_dir / "**/*.java"))
            for java_file in java_files:
                try:
                    content = self.fs.read_text(java_file)
                    if PATTERNS.__dict__.get(pattern) and PATTERNS.__dict__[pattern].search(content):
                        matching_files.append(java_file)
                    elif pattern and pattern in content:  # Fallback to string search
                        matching_files.append(java_file)
                except FileSystemError as e:
                    logger.warning(f"Could not read {java_file}: {e}")
        
        except FileSystemError as e:
            raise JavaParserFileSystemError(e, "finding files", str(search_dir))
        
        return matching_files
    
    def find_directory_by_name(self, search_root: Path, dir_name: str) -> Optional[Path]:
        """Find first directory matching the given name."""
        try:
            # This is a simplified approach - in practice, we'd need better directory traversal
            for candidate_dir in DIRECTORIES.MODEL_DIRECTORIES:
                if candidate_dir.lower() == dir_name.lower():
                    potential_path = search_root / candidate_dir
                    if self.fs.exists(potential_path):
                        return potential_path
        except FileSystemError as e:
            raise JavaParserFileSystemError(e, "finding directory", str(search_root))
        
        return None