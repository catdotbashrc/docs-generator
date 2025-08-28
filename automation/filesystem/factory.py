"""
Factory for creating filesystem implementations.

This module provides a factory pattern for creating appropriate filesystem
implementations based on configuration or runtime needs.
"""

from pathlib import Path
from typing import Type, Union, Dict, Any, Optional

from .abstract import FileSystem
from .local import LocalFileSystem
from .memory import MemoryFileSystem


class FileSystemFactory:
    """
    Factory for creating filesystem implementations.
    
    This factory allows registration of custom implementations and
    provides a unified interface for creating filesystem instances.
    """
    
    # Registry of filesystem implementations
    _implementations: Dict[str, Type[FileSystem]] = {
        'local': LocalFileSystem,
        'memory': MemoryFileSystem,
    }
    
    @classmethod
    def create(cls, fs_type: str, **kwargs) -> FileSystem:
        """
        Create a filesystem instance of the specified type.
        
        Args:
            fs_type: Type of filesystem ('local', 'memory', etc.)
            **kwargs: Arguments to pass to the filesystem constructor
            
        Returns:
            FileSystem instance
            
        Raises:
            ValueError: If filesystem type is not supported
        """
        if fs_type not in cls._implementations:
            available = ', '.join(cls._implementations.keys())
            raise ValueError(
                f"Unsupported filesystem type: {fs_type}. "
                f"Available types: {available}"
            )
        
        implementation = cls._implementations[fs_type]
        
        # Handle path conversion for local filesystem
        if fs_type == 'local' and 'root' in kwargs and isinstance(kwargs['root'], str):
            kwargs['root'] = Path(kwargs['root'])
        
        return implementation(**kwargs)
    
    @classmethod
    def register(cls, name: str, implementation: Type[FileSystem]) -> None:
        """
        Register a custom filesystem implementation.
        
        Args:
            name: Name to register the implementation under
            implementation: FileSystem subclass to register
            
        Raises:
            TypeError: If implementation is not a FileSystem subclass
        """
        if not issubclass(implementation, FileSystem):
            raise TypeError(
                f"Implementation must be a FileSystem subclass, "
                f"got {implementation.__name__}"
            )
        
        cls._implementations[name] = implementation
    
    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> FileSystem:
        """
        Create a filesystem from a configuration dictionary.
        
        Args:
            config: Configuration dictionary with 'type' key and optional parameters
            
        Returns:
            FileSystem instance
            
        Raises:
            ValueError: If configuration is invalid
        """
        if 'type' not in config:
            raise ValueError("Configuration must include 'type' field")
        
        fs_type = config['type']
        kwargs = {k: v for k, v in config.items() if k != 'type'}
        
        return cls.create(fs_type, **kwargs)
    
    @classmethod
    def get_default(cls, for_testing: bool = False) -> FileSystem:
        """
        Get a default filesystem instance.
        
        Args:
            for_testing: If True, returns MemoryFileSystem; otherwise LocalFileSystem
            
        Returns:
            FileSystem instance
        """
        if for_testing:
            return cls.create('memory')
        else:
            return cls.create('local')
    
    @classmethod
    def list_available(cls) -> list:
        """
        List all available filesystem types.
        
        Returns:
            List of registered filesystem type names
        """
        return list(cls._implementations.keys())