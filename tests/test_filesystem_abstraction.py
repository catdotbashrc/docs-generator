"""
Test suite for filesystem abstraction layer following TDD principles.

This module tests all filesystem implementations to ensure they conform
to the FileSystem interface contract and behave consistently.
"""

import pytest
from pathlib import Path
import tempfile
import shutil
from typing import Optional
from unittest.mock import Mock, patch

# Import the abstractions we're about to build
from automation.filesystem.abstract import FileSystem, FileSystemError
from automation.filesystem.local import LocalFileSystem
from automation.filesystem.memory import MemoryFileSystem
from automation.filesystem.factory import FileSystemFactory


class FileSystemContractTests:
    """
    Base test class that defines the contract all FileSystem implementations
    must satisfy. Each implementation should inherit from this class.
    """
    
    @pytest.fixture
    def fs(self) -> FileSystem:
        """Must be overridden by subclasses to provide their implementation."""
        raise NotImplementedError
    
    @pytest.fixture
    def test_content(self) -> str:
        """Sample content for testing."""
        return "Hello, World!\nThis is a test file."
    
    def test_write_and_read_text(self, fs: FileSystem, test_content: str):
        """Test basic write and read operations."""
        path = "test_file.txt"
        
        # Write content
        fs.write_text(path, test_content)
        
        # Read it back
        result = fs.read_text(path)
        assert result == test_content
    
    def test_write_and_read_bytes(self, fs: FileSystem):
        """Test binary write and read operations."""
        path = "test_binary.bin"
        content = b"\x00\x01\x02\x03\x04"
        
        fs.write_bytes(path, content)
        result = fs.read_bytes(path)
        assert result == content
    
    def test_exists(self, fs: FileSystem):
        """Test file existence checking."""
        path = "test_exists.txt"
        
        # File doesn't exist initially
        assert not fs.exists(path)
        
        # Create file
        fs.write_text(path, "content")
        
        # Now it exists
        assert fs.exists(path)
    
    def test_delete_file(self, fs: FileSystem):
        """Test file deletion."""
        path = "test_delete.txt"
        
        # Create file
        fs.write_text(path, "content")
        assert fs.exists(path)
        
        # Delete it
        fs.delete(path)
        assert not fs.exists(path)
    
    def test_delete_nonexistent_file_raises_error(self, fs: FileSystem):
        """Test that deleting non-existent file raises appropriate error."""
        with pytest.raises(FileSystemError) as exc:
            fs.delete("nonexistent.txt")
        assert "not found" in str(exc.value).lower()
    
    def test_read_nonexistent_file_raises_error(self, fs: FileSystem):
        """Test that reading non-existent file raises appropriate error."""
        with pytest.raises(FileSystemError) as exc:
            fs.read_text("nonexistent.txt")
        assert "not found" in str(exc.value).lower()
    
    def test_list_files(self, fs: FileSystem):
        """Test listing files in a directory."""
        # Create some files
        fs.write_text("dir/file1.txt", "content1")
        fs.write_text("dir/file2.txt", "content2")
        fs.write_text("dir/subdir/file3.txt", "content3")
        
        # List files in dir (non-recursive)
        files = fs.list_files("dir")
        assert len(files) == 2
        assert Path("file1.txt") in files
        assert Path("file2.txt") in files
    
    def test_list_files_recursive(self, fs: FileSystem):
        """Test recursive file listing."""
        # Create nested structure
        fs.write_text("root/a.txt", "a")
        fs.write_text("root/sub1/b.txt", "b")
        fs.write_text("root/sub1/sub2/c.txt", "c")
        
        # List recursively
        files = fs.list_files("root", recursive=True)
        assert len(files) == 3
        
        # Convert to strings for easier comparison
        file_strs = [str(f) for f in files]
        assert "a.txt" in file_strs
        assert str(Path("sub1/b.txt")) in file_strs
        assert str(Path("sub1/sub2/c.txt")) in file_strs
    
    def test_create_directory(self, fs: FileSystem):
        """Test directory creation."""
        dir_path = "test_dir/nested/deep"
        
        # Create nested directories
        fs.create_directory(dir_path)
        
        # Verify by writing a file in the directory
        fs.write_text(f"{dir_path}/test.txt", "content")
        assert fs.exists(f"{dir_path}/test.txt")
    
    def test_copy_file(self, fs: FileSystem):
        """Test file copying."""
        src = "source.txt"
        dst = "destination.txt"
        content = "test content"
        
        # Create source file
        fs.write_text(src, content)
        
        # Copy it
        fs.copy(src, dst)
        
        # Both should exist with same content
        assert fs.exists(src)
        assert fs.exists(dst)
        assert fs.read_text(src) == content
        assert fs.read_text(dst) == content
    
    def test_move_file(self, fs: FileSystem):
        """Test file moving."""
        src = "source.txt"
        dst = "destination.txt"
        content = "test content"
        
        # Create source file
        fs.write_text(src, content)
        assert fs.exists(src)
        
        # Move it
        fs.move(src, dst)
        
        # Source gone, destination exists
        assert not fs.exists(src)
        assert fs.exists(dst)
        assert fs.read_text(dst) == content
    
    def test_get_size(self, fs: FileSystem):
        """Test getting file size."""
        path = "test_size.txt"
        content = "Hello, World!"
        
        fs.write_text(path, content)
        size = fs.get_size(path)
        assert size == len(content.encode('utf-8'))
    
    def test_get_modification_time(self, fs: FileSystem):
        """Test getting file modification time."""
        import time
        
        path = "test_mtime.txt"
        
        # Create file
        before = time.time()
        fs.write_text(path, "content")
        time.sleep(0.01)  # Small delay to ensure time difference
        after = time.time()
        
        # Get modification time
        mtime = fs.get_modification_time(path)
        
        # Should be between before and after (with a small tolerance)
        assert before - 0.1 <= mtime <= after + 0.1
    
    def test_glob_pattern_matching(self, fs: FileSystem):
        """Test glob pattern matching for files."""
        # Create files with different extensions
        fs.write_text("test1.txt", "text")
        fs.write_text("test2.txt", "text")
        fs.write_text("test.py", "python")
        fs.write_text("data.json", "json")
        
        # Match txt files
        txt_files = fs.glob("*.txt")
        assert len(txt_files) == 2
        assert Path("test1.txt") in txt_files
        assert Path("test2.txt") in txt_files
        
        # Match all test files
        test_files = fs.glob("test*")
        assert len(test_files) == 3
    
    def test_path_validation(self, fs: FileSystem):
        """Test that path validation prevents directory traversal."""
        # These should raise security errors
        dangerous_paths = [
            "../etc/passwd",
            "../../sensitive",
            "/etc/passwd",
            "~/.ssh/id_rsa",
        ]
        
        for path in dangerous_paths:
            with pytest.raises(FileSystemError) as exc:
                fs.write_text(path, "dangerous")
            assert "invalid" in str(exc.value).lower() or "security" in str(exc.value).lower()
    
    def test_encoding_support(self, fs: FileSystem):
        """Test different text encodings."""
        path = "test_encoding.txt"
        content = "Héllo, Wörld! 你好世界"
        
        # Write and read UTF-8
        fs.write_text(path, content, encoding='utf-8')
        result = fs.read_text(path, encoding='utf-8')
        assert result == content
    
    def test_atomic_writes(self, fs: FileSystem):
        """Test that writes are atomic (all-or-nothing)."""
        path = "test_atomic.txt"
        original = "original content"
        
        # Write original content
        fs.write_text(path, original)
        
        # Simulate a write that might fail partway through
        # The implementation should use atomic writes
        try:
            # This is a conceptual test - implementations should ensure atomicity
            fs.write_text(path, "new content")
            assert fs.read_text(path) == "new content"
        except Exception:
            # If write fails, original should be intact
            assert fs.read_text(path) == original


class TestLocalFileSystem(FileSystemContractTests):
    """Test LocalFileSystem implementation."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        # Cleanup
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def fs(self, temp_dir) -> FileSystem:
        """Provide LocalFileSystem instance."""
        return LocalFileSystem(root=temp_dir)
    
    def test_local_specific_root_validation(self, temp_dir):
        """Test that LocalFileSystem validates root directory."""
        # Should work with existing directory
        fs = LocalFileSystem(root=temp_dir)
        assert fs.root == temp_dir
        
        # Should fail with non-existent directory
        with pytest.raises(FileSystemError):
            LocalFileSystem(root=temp_dir / "nonexistent")
    
    def test_local_specific_permissions(self, fs: LocalFileSystem):
        """Test file permissions handling."""
        import os
        import stat
        
        path = "test_perms.txt"
        fs.write_text(path, "content")
        
        # Get the actual file path
        actual_path = fs.root / path
        
        # Check we can modify permissions
        os.chmod(actual_path, stat.S_IRUSR | stat.S_IWUSR)  # 600
        
        # Should still be able to read/write as owner
        assert fs.read_text(path) == "content"
        fs.write_text(path, "new content")


class TestMemoryFileSystem(FileSystemContractTests):
    """Test MemoryFileSystem implementation."""
    
    @pytest.fixture
    def fs(self) -> FileSystem:
        """Provide MemoryFileSystem instance."""
        return MemoryFileSystem()
    
    def test_memory_specific_isolation(self):
        """Test that different instances are isolated."""
        fs1 = MemoryFileSystem()
        fs2 = MemoryFileSystem()
        
        fs1.write_text("test.txt", "fs1 content")
        
        # fs2 should not see fs1's files
        assert not fs2.exists("test.txt")
    
    def test_memory_specific_clear_all(self):
        """Test clearing all files from memory."""
        fs = MemoryFileSystem()
        
        # Create some files
        fs.write_text("file1.txt", "content1")
        fs.write_text("file2.txt", "content2")
        fs.write_text("dir/file3.txt", "content3")
        
        # Clear all
        fs.clear()
        
        # Everything should be gone
        assert not fs.exists("file1.txt")
        assert not fs.exists("file2.txt")
        assert not fs.exists("dir/file3.txt")
    
    def test_memory_specific_export_import(self):
        """Test exporting and importing filesystem state."""
        fs1 = MemoryFileSystem()
        
        # Create some content
        fs1.write_text("test.txt", "content")
        fs1.write_text("dir/nested.txt", "nested content")
        
        # Export state
        state = fs1.export_state()
        
        # Import into new instance
        fs2 = MemoryFileSystem()
        fs2.import_state(state)
        
        # Should have same content
        assert fs2.read_text("test.txt") == "content"
        assert fs2.read_text("dir/nested.txt") == "nested content"


class TestFileSystemFactory:
    """Test FileSystemFactory."""
    
    def test_create_local_filesystem(self, tmp_path):
        """Test creating LocalFileSystem via factory."""
        fs = FileSystemFactory.create("local", root=tmp_path)
        assert isinstance(fs, LocalFileSystem)
        assert fs.root == tmp_path
    
    def test_create_memory_filesystem(self):
        """Test creating MemoryFileSystem via factory."""
        fs = FileSystemFactory.create("memory")
        assert isinstance(fs, MemoryFileSystem)
    
    def test_create_with_invalid_type_raises_error(self):
        """Test that invalid filesystem type raises error."""
        with pytest.raises(ValueError) as exc:
            FileSystemFactory.create("invalid")
        assert "unsupported" in str(exc.value).lower()
    
    def test_register_custom_filesystem(self):
        """Test registering custom filesystem implementation."""
        
        class CustomFileSystem(MemoryFileSystem):
            """Custom implementation for testing."""
            pass
        
        # Register custom type
        FileSystemFactory.register("custom", CustomFileSystem)
        
        # Should be able to create it
        fs = FileSystemFactory.create("custom")
        assert isinstance(fs, CustomFileSystem)
    
    def test_factory_with_config(self, tmp_path):
        """Test creating filesystem with configuration."""
        config = {
            "type": "local",
            "root": str(tmp_path),
        }
        
        fs = FileSystemFactory.from_config(config)
        assert isinstance(fs, LocalFileSystem)
        assert fs.root == tmp_path


class TestFileSystemIntegration:
    """Integration tests for filesystem abstraction."""
    
    def test_migration_from_direct_io(self, tmp_path):
        """Test migrating code from direct I/O to abstraction."""
        # Old way (direct I/O)
        file_path = tmp_path / "test.txt"
        file_path.write_text("old way")
        content = file_path.read_text()
        assert content == "old way"
        
        # New way (abstraction)
        fs = LocalFileSystem(root=tmp_path)
        fs.write_text("test2.txt", "new way")
        content = fs.read_text("test2.txt")
        assert content == "new way"
        
        # Both can coexist during migration
        assert file_path.exists()
        assert fs.exists("test2.txt")
    
    def test_dependency_injection_pattern(self, tmp_path):
        """Test using filesystem with dependency injection."""
        
        class DocumentGenerator:
            def __init__(self, fs: FileSystem):
                self.fs = fs
            
            def generate(self, content: str) -> None:
                self.fs.write_text("output.txt", content)
            
            def read_output(self) -> str:
                return self.fs.read_text("output.txt")
        
        # Test with real filesystem
        real_fs = LocalFileSystem(root=tmp_path)
        gen = DocumentGenerator(real_fs)
        gen.generate("test content")
        assert gen.read_output() == "test content"
        
        # Test with memory filesystem (for unit tests)
        mem_fs = MemoryFileSystem()
        gen = DocumentGenerator(mem_fs)
        gen.generate("test content")
        assert gen.read_output() == "test content"
    
    def test_parallel_operations(self):
        """Test that filesystem handles parallel operations safely."""
        import threading
        import time
        
        fs = MemoryFileSystem()
        results = []
        
        def write_file(n):
            path = f"file_{n}.txt"
            content = f"content_{n}"
            fs.write_text(path, content)
            time.sleep(0.01)  # Simulate some work
            read_back = fs.read_text(path)
            results.append(read_back == content)
        
        # Create threads
        threads = []
        for i in range(10):
            t = threading.Thread(target=write_file, args=(i,))
            threads.append(t)
            t.start()
        
        # Wait for all to complete
        for t in threads:
            t.join()
        
        # All operations should have succeeded
        assert all(results)
        assert len(results) == 10


class TestErrorHandling:
    """Test error handling across implementations."""
    
    def test_filesystem_error_hierarchy(self):
        """Test that FileSystemError is properly structured."""
        base_error = FileSystemError("base error")
        assert isinstance(base_error, Exception)
        assert str(base_error) == "base error"
        
        # Should be able to catch as Exception
        try:
            raise FileSystemError("test")
        except Exception as e:
            assert isinstance(e, FileSystemError)
    
    def test_error_messages_are_informative(self):
        """Test that errors include helpful information."""
        fs = MemoryFileSystem()
        
        # Try to read non-existent file
        with pytest.raises(FileSystemError) as exc:
            fs.read_text("nonexistent.txt")
        
        error_msg = str(exc.value)
        assert "nonexistent.txt" in error_msg  # Should include the path
        assert "not found" in error_msg.lower()  # Should explain the problem


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])