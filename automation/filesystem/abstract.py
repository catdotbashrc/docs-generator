"""
Abstract base class defining the filesystem interface.

This module provides the contract that all filesystem implementations must follow,
ensuring consistent behavior across different storage backends.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union, List, Optional, Any, Dict
import time


class FileSystemError(Exception):
    """Base exception for filesystem operations."""
    pass


class FileSystem(ABC):
    """
    Abstract base class for filesystem operations.
    
    This interface defines the contract for all filesystem implementations,
    whether they're local disk, memory-based, or cloud storage.
    """
    
    @abstractmethod
    def read_text(self, path: Union[str, Path], encoding: str = 'utf-8') -> str:
        """
        Read text content from a file.
        
        Args:
            path: Path to the file to read
            encoding: Text encoding (default: utf-8)
            
        Returns:
            The content of the file as a string
            
        Raises:
            FileSystemError: If file not found or read fails
        """
        pass
    
    @abstractmethod
    def write_text(self, path: Union[str, Path], content: str, encoding: str = 'utf-8') -> None:
        """
        Write text content to a file.
        
        Args:
            path: Path to the file to write
            content: Text content to write
            encoding: Text encoding (default: utf-8)
            
        Raises:
            FileSystemError: If write fails
        """
        pass
    
    @abstractmethod
    def read_bytes(self, path: Union[str, Path]) -> bytes:
        """
        Read binary content from a file.
        
        Args:
            path: Path to the file to read
            
        Returns:
            The content of the file as bytes
            
        Raises:
            FileSystemError: If file not found or read fails
        """
        pass
    
    @abstractmethod
    def write_bytes(self, path: Union[str, Path], content: bytes) -> None:
        """
        Write binary content to a file.
        
        Args:
            path: Path to the file to write
            content: Binary content to write
            
        Raises:
            FileSystemError: If write fails
        """
        pass
    
    @abstractmethod
    def exists(self, path: Union[str, Path]) -> bool:
        """
        Check if a file or directory exists.
        
        Args:
            path: Path to check
            
        Returns:
            True if the path exists, False otherwise
        """
        pass
    
    @abstractmethod
    def delete(self, path: Union[str, Path]) -> None:
        """
        Delete a file or directory.
        
        Args:
            path: Path to delete
            
        Raises:
            FileSystemError: If deletion fails or path not found
        """
        pass
    
    @abstractmethod
    def list_files(self, directory: Union[str, Path], recursive: bool = False) -> List[Path]:
        """
        List files in a directory.
        
        Args:
            directory: Directory to list
            recursive: If True, list files recursively
            
        Returns:
            List of file paths relative to the directory
            
        Raises:
            FileSystemError: If directory not found
        """
        pass
    
    @abstractmethod
    def create_directory(self, path: Union[str, Path]) -> None:
        """
        Create a directory, including parent directories if needed.
        
        Args:
            path: Directory path to create
            
        Raises:
            FileSystemError: If creation fails
        """
        pass
    
    @abstractmethod
    def copy(self, src: Union[str, Path], dst: Union[str, Path]) -> None:
        """
        Copy a file from source to destination.
        
        Args:
            src: Source file path
            dst: Destination file path
            
        Raises:
            FileSystemError: If copy fails or source not found
        """
        pass
    
    @abstractmethod
    def move(self, src: Union[str, Path], dst: Union[str, Path]) -> None:
        """
        Move a file from source to destination.
        
        Args:
            src: Source file path
            dst: Destination file path
            
        Raises:
            FileSystemError: If move fails or source not found
        """
        pass
    
    @abstractmethod
    def get_size(self, path: Union[str, Path]) -> int:
        """
        Get the size of a file in bytes.
        
        Args:
            path: File path
            
        Returns:
            Size in bytes
            
        Raises:
            FileSystemError: If file not found
        """
        pass
    
    @abstractmethod
    def get_modification_time(self, path: Union[str, Path]) -> float:
        """
        Get the modification time of a file.
        
        Args:
            path: File path
            
        Returns:
            Modification time as Unix timestamp
            
        Raises:
            FileSystemError: If file not found
        """
        pass
    
    @abstractmethod
    def glob(self, pattern: str) -> List[Path]:
        """
        Find files matching a glob pattern.
        
        Args:
            pattern: Glob pattern (e.g., "*.txt", "**/*.py")
            
        Returns:
            List of matching file paths
        """
        pass
    
    def validate_path(self, path: Union[str, Path]) -> Path:
        """
        Validate and normalize a path for security.
        
        Args:
            path: Path to validate
            
        Returns:
            Normalized Path object
            
        Raises:
            FileSystemError: If path is invalid or attempts directory traversal
        """
        path = Path(path)
        
        # Convert to string for validation
        path_str = str(path)
        
        # Check for directory traversal attempts
        if '..' in path.parts:
            raise FileSystemError(f"Invalid path - directory traversal not allowed: {path}")
        
        # Check for absolute paths (security risk)
        if path.is_absolute():
            raise FileSystemError(f"Invalid path - absolute paths not allowed: {path}")
        
        # Check for home directory expansion
        if path_str.startswith('~'):
            raise FileSystemError(f"Invalid path - home directory expansion not allowed: {path}")
        
        return path
    
    def read_json(self, path: Union[str, Path]) -> Dict[str, Any]:
        """
        Convenience method to read JSON file.
        
        Args:
            path: Path to JSON file
            
        Returns:
            Parsed JSON data
            
        Raises:
            FileSystemError: If file not found or invalid JSON
        """
        import json
        
        try:
            content = self.read_text(path)
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise FileSystemError(f"Invalid JSON in {path}: {e}")
    
    def write_json(self, path: Union[str, Path], data: Dict[str, Any], indent: int = 2) -> None:
        """
        Convenience method to write JSON file.
        
        Args:
            path: Path to write to
            data: Data to serialize as JSON
            indent: JSON indentation (default: 2)
            
        Raises:
            FileSystemError: If write fails
        """
        import json
        
        try:
            content = json.dumps(data, indent=indent, ensure_ascii=False)
            self.write_text(path, content)
        except (TypeError, ValueError) as e:
            raise FileSystemError(f"Cannot serialize data to JSON: {e}")
    
    def read_yaml(self, path: Union[str, Path]) -> Dict[str, Any]:
        """
        Convenience method to read YAML file.
        
        Args:
            path: Path to YAML file
            
        Returns:
            Parsed YAML data
            
        Raises:
            FileSystemError: If file not found or invalid YAML
        """
        import yaml
        
        try:
            content = self.read_text(path)
            return yaml.safe_load(content)
        except yaml.YAMLError as e:
            raise FileSystemError(f"Invalid YAML in {path}: {e}")
    
    def write_yaml(self, path: Union[str, Path], data: Dict[str, Any]) -> None:
        """
        Convenience method to write YAML file.
        
        Args:
            path: Path to write to
            data: Data to serialize as YAML
            
        Raises:
            FileSystemError: If write fails
        """
        import yaml
        
        try:
            content = yaml.safe_dump(data, default_flow_style=False, allow_unicode=True)
            self.write_text(path, content)
        except yaml.YAMLError as e:
            raise FileSystemError(f"Cannot serialize data to YAML: {e}")