"""
Local filesystem implementation.

This module provides a concrete implementation of the FileSystem interface
for local disk operations, with proper error handling and security validation.
"""

import os
import shutil
import glob as glob_module
from pathlib import Path
from typing import Union, List, Optional
import time
import tempfile

from .abstract import FileSystem, FileSystemError


class LocalFileSystem(FileSystem):
    """
    Local filesystem implementation.
    
    This implementation works with the local disk, providing all standard
    filesystem operations with proper error handling and security validation.
    """
    
    def __init__(self, root: Optional[Union[str, Path]] = None):
        """
        Initialize LocalFileSystem.
        
        Args:
            root: Root directory for all operations. If None, uses current directory.
                 Must exist.
            
        Raises:
            FileSystemError: If root directory doesn't exist
        """
        if root is None:
            self.root = Path.cwd()
        else:
            self.root = Path(root).resolve()
            
        if not self.root.exists():
            raise FileSystemError(f"Root directory does not exist: {self.root}")
        
        if not self.root.is_dir():
            raise FileSystemError(f"Root path is not a directory: {self.root}")
    
    def _resolve_path(self, path: Union[str, Path]) -> Path:
        """
        Resolve a path relative to the root directory.
        
        Args:
            path: Path to resolve
            
        Returns:
            Absolute path within the root directory
            
        Raises:
            FileSystemError: If path validation fails
        """
        # Validate the path first
        validated = self.validate_path(path)
        
        # Resolve relative to root
        resolved = (self.root / validated).resolve()
        
        # Ensure the resolved path is within root (prevent escape)
        try:
            resolved.relative_to(self.root)
        except ValueError:
            raise FileSystemError(f"Path escapes root directory: {path}")
        
        return resolved
    
    def read_text(self, path: Union[str, Path], encoding: str = 'utf-8') -> str:
        """Read text content from a file."""
        resolved = self._resolve_path(path)
        
        if not resolved.exists():
            raise FileSystemError(f"File not found: {path}")
        
        if not resolved.is_file():
            raise FileSystemError(f"Path is not a file: {path}")
        
        try:
            return resolved.read_text(encoding=encoding)
        except Exception as e:
            raise FileSystemError(f"Failed to read file {path}: {e}")
    
    def write_text(self, path: Union[str, Path], content: str, encoding: str = 'utf-8') -> None:
        """Write text content to a file atomically."""
        resolved = self._resolve_path(path)
        
        # Ensure parent directory exists
        resolved.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            # Use atomic write with temporary file
            with tempfile.NamedTemporaryFile(
                mode='w',
                encoding=encoding,
                dir=resolved.parent,
                delete=False
            ) as tmp_file:
                tmp_file.write(content)
                tmp_path = Path(tmp_file.name)
            
            # Atomic rename
            tmp_path.replace(resolved)
            
        except Exception as e:
            # Clean up temporary file if it exists
            if 'tmp_path' in locals() and tmp_path.exists():
                tmp_path.unlink()
            raise FileSystemError(f"Failed to write file {path}: {e}")
    
    def read_bytes(self, path: Union[str, Path]) -> bytes:
        """Read binary content from a file."""
        resolved = self._resolve_path(path)
        
        if not resolved.exists():
            raise FileSystemError(f"File not found: {path}")
        
        if not resolved.is_file():
            raise FileSystemError(f"Path is not a file: {path}")
        
        try:
            return resolved.read_bytes()
        except Exception as e:
            raise FileSystemError(f"Failed to read file {path}: {e}")
    
    def write_bytes(self, path: Union[str, Path], content: bytes) -> None:
        """Write binary content to a file atomically."""
        resolved = self._resolve_path(path)
        
        # Ensure parent directory exists
        resolved.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            # Use atomic write with temporary file
            with tempfile.NamedTemporaryFile(
                mode='wb',
                dir=resolved.parent,
                delete=False
            ) as tmp_file:
                tmp_file.write(content)
                tmp_path = Path(tmp_file.name)
            
            # Atomic rename
            tmp_path.replace(resolved)
            
        except Exception as e:
            # Clean up temporary file if it exists
            if 'tmp_path' in locals() and tmp_path.exists():
                tmp_path.unlink()
            raise FileSystemError(f"Failed to write file {path}: {e}")
    
    def exists(self, path: Union[str, Path]) -> bool:
        """Check if a file or directory exists."""
        try:
            resolved = self._resolve_path(path)
            return resolved.exists()
        except FileSystemError:
            # Path validation failed (e.g., invalid path)
            return False
    
    def delete(self, path: Union[str, Path]) -> None:
        """Delete a file or directory."""
        resolved = self._resolve_path(path)
        
        if not resolved.exists():
            raise FileSystemError(f"Path not found: {path}")
        
        try:
            if resolved.is_file():
                resolved.unlink()
            elif resolved.is_dir():
                shutil.rmtree(resolved)
            else:
                raise FileSystemError(f"Unknown path type: {path}")
        except Exception as e:
            raise FileSystemError(f"Failed to delete {path}: {e}")
    
    def list_files(self, directory: Union[str, Path], recursive: bool = False) -> List[Path]:
        """List files in a directory."""
        resolved = self._resolve_path(directory)
        
        if not resolved.exists():
            raise FileSystemError(f"Directory not found: {directory}")
        
        if not resolved.is_dir():
            raise FileSystemError(f"Path is not a directory: {directory}")
        
        try:
            files = []
            
            if recursive:
                # Recursive listing
                for root, _, filenames in os.walk(resolved):
                    root_path = Path(root)
                    for filename in filenames:
                        file_path = root_path / filename
                        # Return relative path from the directory
                        relative = file_path.relative_to(resolved)
                        files.append(relative)
            else:
                # Non-recursive listing
                for item in resolved.iterdir():
                    if item.is_file():
                        files.append(Path(item.name))
            
            return sorted(files)
            
        except Exception as e:
            raise FileSystemError(f"Failed to list files in {directory}: {e}")
    
    def create_directory(self, path: Union[str, Path]) -> None:
        """Create a directory, including parent directories."""
        resolved = self._resolve_path(path)
        
        try:
            resolved.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise FileSystemError(f"Failed to create directory {path}: {e}")
    
    def copy(self, src: Union[str, Path], dst: Union[str, Path]) -> None:
        """Copy a file from source to destination."""
        src_resolved = self._resolve_path(src)
        dst_resolved = self._resolve_path(dst)
        
        if not src_resolved.exists():
            raise FileSystemError(f"Source file not found: {src}")
        
        if not src_resolved.is_file():
            raise FileSystemError(f"Source is not a file: {src}")
        
        # Ensure destination directory exists
        dst_resolved.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            shutil.copy2(src_resolved, dst_resolved)
        except Exception as e:
            raise FileSystemError(f"Failed to copy {src} to {dst}: {e}")
    
    def move(self, src: Union[str, Path], dst: Union[str, Path]) -> None:
        """Move a file from source to destination."""
        src_resolved = self._resolve_path(src)
        dst_resolved = self._resolve_path(dst)
        
        if not src_resolved.exists():
            raise FileSystemError(f"Source file not found: {src}")
        
        # Ensure destination directory exists
        dst_resolved.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            shutil.move(str(src_resolved), str(dst_resolved))
        except Exception as e:
            raise FileSystemError(f"Failed to move {src} to {dst}: {e}")
    
    def get_size(self, path: Union[str, Path]) -> int:
        """Get the size of a file in bytes."""
        resolved = self._resolve_path(path)
        
        if not resolved.exists():
            raise FileSystemError(f"File not found: {path}")
        
        if not resolved.is_file():
            raise FileSystemError(f"Path is not a file: {path}")
        
        try:
            return resolved.stat().st_size
        except Exception as e:
            raise FileSystemError(f"Failed to get size of {path}: {e}")
    
    def get_modification_time(self, path: Union[str, Path]) -> float:
        """Get the modification time of a file."""
        resolved = self._resolve_path(path)
        
        if not resolved.exists():
            raise FileSystemError(f"File not found: {path}")
        
        try:
            return resolved.stat().st_mtime
        except Exception as e:
            raise FileSystemError(f"Failed to get modification time of {path}: {e}")
    
    def glob(self, pattern: str) -> List[Path]:
        """Find files matching a glob pattern."""
        # Resolve the pattern relative to root
        if '/' in pattern or os.sep in pattern:
            # Pattern includes directory
            full_pattern = str(self.root / pattern)
        else:
            # Pattern is just for files in root
            full_pattern = str(self.root / pattern)
        
        try:
            matches = glob_module.glob(full_pattern, recursive=True)
            
            # Convert to Path objects and make relative to root
            result = []
            for match in matches:
                match_path = Path(match)
                if match_path.is_file():
                    try:
                        relative = match_path.relative_to(self.root)
                        result.append(relative)
                    except ValueError:
                        # Skip files outside root
                        pass
            
            return sorted(result)
            
        except Exception as e:
            raise FileSystemError(f"Failed to glob pattern {pattern}: {e}")