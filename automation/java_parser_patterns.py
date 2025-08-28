"""
Regex patterns and constants extracted from java_parser.py for testability.

This module contains all regex patterns, configuration constants, and type mappings
used in Java source code parsing, extracted into testable components.
"""

import re
from typing import Dict, List, Pattern
from dataclasses import dataclass


@dataclass
class RegexPatterns:
    """Compiled regex patterns for Java source code parsing."""
    
    # WebService patterns
    WEBSERVICE_NAMESPACE = re.compile(
        r'@WebService\([^)]*targetNamespace\s*=\s*"([^"]*)"',
        re.MULTILINE
    )
    
    WEBSERVICE_NAME = re.compile(
        r'@WebService\([^)]*serviceName\s*=\s*"([^"]*)"',
        re.MULTILINE
    )
    
    # Interface and class patterns
    PUBLIC_INTERFACE = re.compile(r'public interface (\w+)')
    PUBLIC_CLASS = re.compile(r'public class (\w+)')
    
    # WebMethod patterns
    WEBMETHOD_OPERATION = re.compile(
        r'@WebMethod\([^)]*operationName\s*=\s*"([^"]*)"[^)]*\)[^{]*?(\w+\s+\w+\([^)]*\))',
        re.MULTILINE | re.DOTALL
    )
    
    WEBPARAM = re.compile(
        r'@WebParam\([^)]*name\s*=\s*"([^"]*)"[^)]*\)\s*(\w+)\s+(\w+)'
    )
    
    # Package and field patterns
    PACKAGE_DECLARATION = re.compile(r'package ([^;]+);')
    
    FIELD_DECLARATION = re.compile(
        r'(private|public|protected)\s+(\w+(?:<[^>]+>)?)\s+(\w+)\s*[;=]'
    )
    
    # Spring annotations
    SERVICE_ANNOTATION = re.compile(r'@Service|class \w*Service')
    REPOSITORY_ANNOTATION = re.compile(r'@Repository|Repository\.java|DAO\.java')
    
    # Dependency injection
    AUTOWIRED_REPOSITORY = re.compile(r'@Autowired[^;]*?(\w*Repository|\w*DAO)\s+(\w+)')
    
    # Build file patterns
    GRADLE_VERSION = re.compile(r"version\s*=\s*['\"]([^'\"]*)['\"]")
    GRADLE_GROUP = re.compile(r"group\s*=\s*['\"]([^'\"]*)['\"]")
    
    # Return type extraction
    METHOD_RETURN_TYPE = re.compile(r'(\w+(?:<[^>]+>)?)\s+\w+\s*\(')


@dataclass
class DirectoryPatterns:
    """Directory names to search for different types of Java classes."""
    
    MODEL_DIRECTORIES: List[str] = None
    
    def __post_init__(self):
        if self.MODEL_DIRECTORIES is None:
            self.MODEL_DIRECTORIES = [
                "model", "models", "domain", "dto", "entity", "entities"
            ]


@dataclass
class TypeMappings:
    """Type mappings for generating example values and descriptions."""
    
    EXAMPLE_VALUES: Dict[str, str] = None
    
    def __post_init__(self):
        if self.EXAMPLE_VALUES is None:
            self.EXAMPLE_VALUES = {
                'String': 'example_string',
                'int': '123',
                'Integer': '123', 
                'long': '123456789',
                'Long': '123456789',
                'boolean': 'true',
                'Boolean': 'true',
                'Date': '2024-01-01',
                'LocalDate': '2024-01-01',
                'LocalDateTime': '2024-01-01T10:00:00',
                'double': '123.45',
                'Double': '123.45',
                'float': '123.4f',
                'Float': '123.4f',
                'BigDecimal': '1234.56'
            }
    
    def get_example_value(self, param_type: str) -> str:
        """Generate example value for a parameter type."""
        return self.EXAMPLE_VALUES.get(param_type, f'example_{param_type.lower()}')
    
    def get_field_description(self, field_name: str, field_type: str, visibility: str) -> str:
        """Generate field description."""
        return f"{visibility} field of type {field_type}"
    
    def get_parameter_description(self, param_type: str) -> str:
        """Generate parameter description."""
        return f"Parameter of type {param_type}"


@dataclass  
class JavaParserConfig:
    """Configuration settings for Java parser with secure defaults."""
    
    # Default project structure
    DEFAULT_SOURCE_PATH: str = "src/main/java"
    DEFAULT_RESOURCES_PATH: str = "src/main/resources"
    
    # File encoding
    DEFAULT_ENCODING: str = "utf-8"
    
    # Template generation defaults (configurable, not hard-coded)
    DEFAULT_ENVIRONMENT: str = "Development"
    DEFAULT_SERVICE_TYPE: str = "Java Service"
    DEFAULT_BASE_URL: str = "http://localhost:8080"
    DEFAULT_PORT: str = "8080"
    
    # Error handling
    MAX_FILE_SIZE_MB: int = 10
    PARSING_TIMEOUT_SECONDS: int = 30
    
    # Validation patterns
    SAFE_FILENAME_PATTERN: Pattern = re.compile(r'^[a-zA-Z0-9._-]+\.java$')
    
    def validate_filename(self, filename: str) -> bool:
        """Validate that filename is safe for processing."""
        return bool(self.SAFE_FILENAME_PATTERN.match(filename))
    
    def get_template_defaults(self) -> Dict[str, str]:
        """Get template default values that can be overridden."""
        return {
            'environment': self.DEFAULT_ENVIRONMENT,
            'service_type': self.DEFAULT_SERVICE_TYPE,
            'base_url': self.DEFAULT_BASE_URL,
            'port': self.DEFAULT_PORT
        }


# Module-level instances for backward compatibility
PATTERNS = RegexPatterns()
DIRECTORIES = DirectoryPatterns()
TYPE_MAPPINGS = TypeMappings()
CONFIG = JavaParserConfig()