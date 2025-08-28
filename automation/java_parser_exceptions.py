"""
Exception hierarchy for Java parser operations.

This module defines specific exceptions for different types of parsing failures,
enabling better error handling and debugging.
"""

from automation.filesystem.abstract import FileSystemError


class JavaParserError(Exception):
    """Base exception for all Java parser operations."""
    pass


class JavaSyntaxError(JavaParserError):
    """Raised when Java source code contains syntax errors."""
    
    def __init__(self, message: str, file_path: str = None, line_number: int = None):
        self.file_path = file_path
        self.line_number = line_number
        
        error_msg = f"Java syntax error: {message}"
        if file_path:
            error_msg += f" in {file_path}"
        if line_number:
            error_msg += f" at line {line_number}"
            
        super().__init__(error_msg)


class JavaParsingTimeoutError(JavaParserError):
    """Raised when parsing operations exceed timeout limits."""
    
    def __init__(self, file_path: str, timeout_seconds: int):
        self.file_path = file_path
        self.timeout_seconds = timeout_seconds
        super().__init__(f"Parsing timeout after {timeout_seconds}s for {file_path}")


class JavaFileTooLargeError(JavaParserError):
    """Raised when Java files exceed size limits."""
    
    def __init__(self, file_path: str, size_mb: float, limit_mb: int):
        self.file_path = file_path
        self.size_mb = size_mb
        self.limit_mb = limit_mb
        super().__init__(
            f"File {file_path} ({size_mb:.1f}MB) exceeds size limit ({limit_mb}MB)"
        )


class UnsafeFilenameError(JavaParserError):
    """Raised when filenames contain potentially unsafe characters."""
    
    def __init__(self, filename: str):
        self.filename = filename
        super().__init__(f"Unsafe filename: {filename}")


class JavaProjectStructureError(JavaParserError):
    """Raised when Java project structure is invalid or unexpected."""
    
    def __init__(self, message: str, project_path: str = None):
        self.project_path = project_path
        error_msg = f"Project structure error: {message}"
        if project_path:
            error_msg += f" in {project_path}"
        super().__init__(error_msg)


class AnnotationParsingError(JavaParserError):
    """Raised when annotation parsing fails."""
    
    def __init__(self, annotation_name: str, file_path: str = None, details: str = None):
        self.annotation_name = annotation_name
        self.file_path = file_path
        self.details = details
        
        error_msg = f"Failed to parse @{annotation_name} annotation"
        if file_path:
            error_msg += f" in {file_path}"
        if details:
            error_msg += f": {details}"
            
        super().__init__(error_msg)


class TemplateRenderingError(JavaParserError):
    """Raised when template rendering fails."""
    
    def __init__(self, template_name: str, error_details: str):
        self.template_name = template_name
        self.error_details = error_details
        super().__init__(f"Template rendering failed for {template_name}: {error_details}")


# Custom exception for filesystem integration
class JavaParserFileSystemError(JavaParserError):
    """Wrapper for filesystem errors with Java parser context."""
    
    def __init__(self, original_error: FileSystemError, operation: str, file_path: str):
        self.original_error = original_error
        self.operation = operation
        self.file_path = file_path
        super().__init__(
            f"Filesystem error during {operation} on {file_path}: {original_error}"
        )