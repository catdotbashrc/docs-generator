"""
Filesystem abstraction layer for the Infrastructure Documentation Standards project.

This package provides a clean abstraction over filesystem operations, allowing
for easy testing, cloud storage integration, and improved maintainability.
"""

from .abstract import FileSystem, FileSystemError
from .local import LocalFileSystem
from .memory import MemoryFileSystem
from .factory import FileSystemFactory

__all__ = [
    'FileSystem',
    'FileSystemError',
    'LocalFileSystem',
    'MemoryFileSystem',
    'FileSystemFactory',
]

__version__ = '1.0.0'