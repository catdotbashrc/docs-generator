"""
In-memory filesystem implementation for testing.

This module provides a pure in-memory implementation of the FileSystem interface,
perfect for unit testing and scenarios where no actual disk I/O is desired.
"""

import fnmatch
import io
import time
from pathlib import Path
from typing import Union, List, Dict, Any, Optional
from dataclasses import dataclass, field
from copy import deepcopy
import threading

from .abstract import FileSystem, FileSystemError


@dataclass
class FileNode:
    """Represents a file in the memory filesystem."""
    content: bytes
    created_at: float = field(default_factory=time.time)
    modified_at: float = field(default_factory=time.time)
    
    @property
    def size(self) -> int:
        """Get the size of the file in bytes."""
        return len(self.content)


class MemoryFileSystem(FileSystem):
    """
    In-memory filesystem implementation.
    
    This implementation stores all files in memory, making it perfect
    for unit testing and scenarios where actual disk I/O is not needed.
    Thread-safe for concurrent operations.
    """
    
    def __init__(self):
        """Initialize an empty memory filesystem."""
        self._files: Dict[Path, FileNode] = {}
        self._lock = threading.RLock()
    
    def _normalize_path(self, path: Union[str, Path]) -> Path:
        """
        Normalize and validate a path.
        
        Args:
            path: Path to normalize
            
        Returns:
            Normalized Path object
        """
        validated = self.validate_path(path)
        # Remove any leading/trailing separators
        normalized = Path(str(validated).strip('/\\'))
        return normalized
    
    def read_text(self, path: Union[str, Path], encoding: str = 'utf-8') -> str:
        """Read text content from a file."""
        normalized = self._normalize_path(path)
        
        with self._lock:
            if normalized not in self._files:
                raise FileSystemError(f"File not found: {path}")
            
            node = self._files[normalized]
            try:
                return node.content.decode(encoding)
            except UnicodeDecodeError as e:
                raise FileSystemError(f"Failed to decode file {path} with encoding {encoding}: {e}")
    
    def write_text(self, path: Union[str, Path], content: str, encoding: str = 'utf-8') -> None:
        """Write text content to a file."""
        normalized = self._normalize_path(path)
        
        with self._lock:
            # Create parent directories implicitly
            self._ensure_parent_dirs(normalized)
            
            try:
                encoded = content.encode(encoding)
            except UnicodeEncodeError as e:
                raise FileSystemError(f"Failed to encode content for {path}: {e}")
            
            if normalized in self._files:
                # Update existing file
                node = self._files[normalized]
                node.content = encoded
                node.modified_at = time.time()
            else:
                # Create new file
                self._files[normalized] = FileNode(content=encoded)
    
    def read_bytes(self, path: Union[str, Path]) -> bytes:
        """Read binary content from a file."""
        normalized = self._normalize_path(path)
        
        with self._lock:
            if normalized not in self._files:
                raise FileSystemError(f"File not found: {path}")
            
            return self._files[normalized].content
    
    def write_bytes(self, path: Union[str, Path], content: bytes) -> None:
        """Write binary content to a file."""
        normalized = self._normalize_path(path)
        
        with self._lock:
            # Create parent directories implicitly
            self._ensure_parent_dirs(normalized)
            
            if normalized in self._files:
                # Update existing file
                node = self._files[normalized]
                node.content = content
                node.modified_at = time.time()
            else:
                # Create new file
                self._files[normalized] = FileNode(content=content)
    
    def exists(self, path: Union[str, Path]) -> bool:
        """Check if a file or directory exists."""
        normalized = self._normalize_path(path)
        
        with self._lock:
            # Check if it's a file
            if normalized in self._files:
                return True
            
            # Check if it's a directory (has children)
            path_str = str(normalized)
            for file_path in self._files:
                file_str = str(file_path)
                if file_str.startswith(path_str + '/') or file_str.startswith(path_str + '\\'):
                    return True
            
            return False
    
    def delete(self, path: Union[str, Path]) -> None:
        """Delete a file or directory."""
        normalized = self._normalize_path(path)
        
        with self._lock:
            # Try to delete as a file
            if normalized in self._files:
                del self._files[normalized]
                return
            
            # Try to delete as a directory
            path_str = str(normalized)
            files_to_delete = []
            
            for file_path in self._files:
                file_str = str(file_path)
                if file_str.startswith(path_str + '/') or file_str.startswith(path_str + '\\'):
                    files_to_delete.append(file_path)
            
            if not files_to_delete and normalized not in self._files:
                raise FileSystemError(f"Path not found: {path}")
            
            # Delete all files in the directory
            for file_path in files_to_delete:
                del self._files[file_path]
    
    def list_files(self, directory: Union[str, Path], recursive: bool = False) -> List[Path]:
        """List files in a directory."""
        normalized = self._normalize_path(directory) if directory != '.' else Path()
        
        with self._lock:
            # Check if directory exists
            if normalized != Path() and not self.exists(normalized):
                raise FileSystemError(f"Directory not found: {directory}")
            
            files = []
            dir_str = str(normalized) if normalized != Path() else ''
            
            for file_path in self._files:
                file_str = str(file_path)
                
                # Check if file is in the directory
                if dir_str:
                    if not (file_str.startswith(dir_str + '/') or file_str.startswith(dir_str + '\\')):
                        continue
                    # Get relative path from directory
                    try:
                        relative = file_path.relative_to(normalized)
                    except ValueError:
                        continue
                else:
                    relative = file_path
                
                # Check recursion
                if not recursive:
                    # Only include direct children
                    if len(relative.parts) == 1:
                        files.append(relative)
                else:
                    files.append(relative)
            
            return sorted(files)
    
    def create_directory(self, path: Union[str, Path]) -> None:
        """Create a directory (no-op in memory, directories are implicit)."""
        # In memory filesystem, directories are implicit
        # Just validate the path
        self._normalize_path(path)
    
    def copy(self, src: Union[str, Path], dst: Union[str, Path]) -> None:
        """Copy a file from source to destination."""
        src_normalized = self._normalize_path(src)
        dst_normalized = self._normalize_path(dst)
        
        with self._lock:
            if src_normalized not in self._files:
                raise FileSystemError(f"Source file not found: {src}")
            
            # Create parent directories for destination
            self._ensure_parent_dirs(dst_normalized)
            
            # Deep copy the file node
            src_node = self._files[src_normalized]
            self._files[dst_normalized] = FileNode(
                content=src_node.content,
                created_at=time.time(),
                modified_at=time.time()
            )
    
    def move(self, src: Union[str, Path], dst: Union[str, Path]) -> None:
        """Move a file from source to destination."""
        src_normalized = self._normalize_path(src)
        dst_normalized = self._normalize_path(dst)
        
        with self._lock:
            if src_normalized not in self._files:
                raise FileSystemError(f"Source file not found: {src}")
            
            # Create parent directories for destination
            self._ensure_parent_dirs(dst_normalized)
            
            # Move the file (rename in dictionary)
            self._files[dst_normalized] = self._files[src_normalized]
            del self._files[src_normalized]
    
    def get_size(self, path: Union[str, Path]) -> int:
        """Get the size of a file in bytes."""
        normalized = self._normalize_path(path)
        
        with self._lock:
            if normalized not in self._files:
                raise FileSystemError(f"File not found: {path}")
            
            return self._files[normalized].size
    
    def get_modification_time(self, path: Union[str, Path]) -> float:
        """Get the modification time of a file."""
        normalized = self._normalize_path(path)
        
        with self._lock:
            if normalized not in self._files:
                raise FileSystemError(f"File not found: {path}")
            
            return self._files[normalized].modified_at
    
    def glob(self, pattern: str) -> List[Path]:
        """Find files matching a glob pattern."""
        with self._lock:
            matches = []
            
            for file_path in self._files:
                file_str = str(file_path)
                
                # Handle recursive patterns
                if '**' in pattern:
                    # Convert ** to match any path depth
                    regex_pattern = pattern.replace('**/', '*').replace('**\\', '*')
                else:
                    regex_pattern = pattern
                
                # Check if file matches pattern
                if fnmatch.fnmatch(file_str, regex_pattern):
                    matches.append(file_path)
            
            return sorted(matches)
    
    def _ensure_parent_dirs(self, path: Path) -> None:
        """Ensure parent directories exist (implicit in memory)."""
        # In memory filesystem, directories are implicit, so this is a no-op
        pass
    
    def clear(self) -> None:
        """Clear all files from the filesystem."""
        with self._lock:
            self._files.clear()
    
    def export_state(self) -> Dict[str, Any]:
        """
        Export the current state of the filesystem.
        
        Returns:
            Dictionary containing all files and their metadata
        """
        with self._lock:
            state = {}
            for path, node in self._files.items():
                state[str(path)] = {
                    'content': node.content.hex(),  # Store as hex string
                    'created_at': node.created_at,
                    'modified_at': node.modified_at,
                }
            return state
    
    def import_state(self, state: Dict[str, Any]) -> None:
        """
        Import a previously exported filesystem state.
        
        Args:
            state: State dictionary from export_state()
        """
        with self._lock:
            self._files.clear()
            
            for path_str, data in state.items():
                path = Path(path_str)
                content = bytes.fromhex(data['content'])
                
                self._files[path] = FileNode(
                    content=content,
                    created_at=data['created_at'],
                    modified_at=data['modified_at']
                )