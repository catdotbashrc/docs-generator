# API Reference - Infrastructure Documentation Standards

## Table of Contents
- [Automation Module](#automation-module)
  - [Filesystem Abstraction](#filesystem-abstraction)
  - [Java AST Extractor](#java-ast-extractor)
  - [Build System](#build-system)
- [CLI Commands](#cli-commands)
- [Configuration](#configuration)

---

## Automation Module

### Filesystem Abstraction

#### `automation.filesystem.abstract.FileSystem`

**Base abstract class for all filesystem operations**

```python
class FileSystem(ABC):
    """Abstract base class for filesystem operations."""
    
    @abstractmethod
    def read_text(path: Union[str, Path], encoding: str = 'utf-8') -> str:
        """Read text content from a file."""
        
    @abstractmethod
    def write_text(path: Union[str, Path], content: str, encoding: str = 'utf-8') -> None:
        """Write text content to a file."""
        
    @abstractmethod
    def read_bytes(path: Union[str, Path]) -> bytes:
        """Read binary content from a file."""
        
    @abstractmethod
    def write_bytes(path: Union[str, Path], content: bytes) -> None:
        """Write binary content to a file."""
        
    @abstractmethod
    def exists(path: Union[str, Path]) -> bool:
        """Check if a file or directory exists."""
        
    @abstractmethod
    def delete(path: Union[str, Path]) -> None:
        """Delete a file or directory."""
        
    @abstractmethod
    def list_files(path: Union[str, Path], pattern: str = "*", 
                   recursive: bool = False) -> List[Path]:
        """List files in a directory."""
        
    @abstractmethod
    def create_directory(path: Union[str, Path]) -> None:
        """Create a directory (including parents)."""
        
    @abstractmethod
    def copy(src: Union[str, Path], dst: Union[str, Path]) -> None:
        """Copy a file from source to destination."""
        
    @abstractmethod
    def move(src: Union[str, Path], dst: Union[str, Path]) -> None:
        """Move a file from source to destination."""
        
    @abstractmethod
    def get_size(path: Union[str, Path]) -> int:
        """Get the size of a file in bytes."""
        
    @abstractmethod
    def get_modification_time(path: Union[str, Path]) -> float:
        """Get the modification time as a Unix timestamp."""
        
    @abstractmethod
    def glob(pattern: str) -> List[Path]:
        """Find files matching a glob pattern."""
```

#### `automation.filesystem.local.LocalFileSystem`

**Local filesystem implementation**

```python
class LocalFileSystem(FileSystem):
    """Local filesystem implementation."""
    
    def __init__(self, root: Optional[Path] = None):
        """
        Initialize with optional root directory.
        
        Args:
            root: Root directory for all operations (defaults to current directory)
        
        Raises:
            FileSystemError: If root doesn't exist or isn't a directory
        """
```

**Example Usage:**
```python
from automation.filesystem.local import LocalFileSystem

# Create filesystem with root
fs = LocalFileSystem(root="/project/root")

# Read file
content = fs.read_text("config.yaml")

# Write file
fs.write_text("output.txt", "Hello World")

# List files
files = fs.list_files("src", pattern="*.py", recursive=True)

# Check existence
if fs.exists("important.conf"):
    size = fs.get_size("important.conf")
```

#### `automation.filesystem.memory.MemoryFileSystem`

**In-memory filesystem for testing**

```python
class MemoryFileSystem(FileSystem):
    """In-memory filesystem implementation for testing."""
    
    def __init__(self):
        """Initialize empty in-memory filesystem."""
        
    def clear(self) -> None:
        """Clear all files from memory."""
        
    def export_state(self) -> Dict[str, Any]:
        """Export filesystem state for serialization."""
        
    def import_state(self, state: Dict[str, Any]) -> None:
        """Import filesystem state from serialization."""
```

**Example Usage:**
```python
from automation.filesystem.memory import MemoryFileSystem

# Create in-memory filesystem
fs = MemoryFileSystem()

# Use for testing
fs.write_text("test.txt", "test content")
assert fs.exists("test.txt")
assert fs.read_text("test.txt") == "test content"

# Export/import state
state = fs.export_state()
new_fs = MemoryFileSystem()
new_fs.import_state(state)
```

#### `automation.filesystem.factory.FileSystemFactory`

**Factory for creating filesystem instances**

```python
class FileSystemFactory:
    """Factory for creating filesystem instances."""
    
    @staticmethod
    def create(fs_type: str, **kwargs) -> FileSystem:
        """
        Create a filesystem instance.
        
        Args:
            fs_type: Type of filesystem ("local" or "memory")
            **kwargs: Additional arguments for filesystem constructor
            
        Returns:
            FileSystem instance
            
        Raises:
            ValueError: If fs_type is not supported
        """
    
    @staticmethod
    def register(name: str, cls: Type[FileSystem]) -> None:
        """Register a custom filesystem implementation."""
    
    @staticmethod
    def from_config(config: Dict[str, Any]) -> FileSystem:
        """Create filesystem from configuration dictionary."""
```

**Example Usage:**
```python
from automation.filesystem.factory import FileSystemFactory

# Create local filesystem
fs = FileSystemFactory.create("local", root="/data")

# Create memory filesystem
test_fs = FileSystemFactory.create("memory")

# Register custom implementation
FileSystemFactory.register("custom", CustomFileSystem)
fs = FileSystemFactory.create("custom")

# From configuration
config = {"type": "local", "root": "/project"}
fs = FileSystemFactory.from_config(config)
```

---

### Java AST Extractor

#### `automation.java_ast_extractor.JavaASTExtractor`

**Extract documentation from Java source code using AST analysis**

```python
class JavaASTExtractor:
    """Extracts API documentation from Java source using AST analysis."""
    
    def __init__(self, filesystem: FileSystem):
        """
        Initialize extractor with filesystem.
        
        Args:
            filesystem: FileSystem instance for file operations
        """
    
    def extract_documentation(self, source_path: str) -> Dict[str, Any]:
        """
        Extract comprehensive documentation from Java source.
        
        Args:
            source_path: Path to Java source file or directory
            
        Returns:
            Dictionary containing:
                - language: "java"
                - endpoints: List of API endpoints
                - services: List of service classes
                - models: List of data models
                - repositories: List of repository classes
        """
    
    def extract_endpoints(self, tree: CompilationUnit) -> List[Dict[str, Any]]:
        """Extract SOAP/REST endpoints from Java AST."""
    
    def extract_services(self, tree: CompilationUnit) -> List[Dict[str, Any]]:
        """Extract service classes and methods."""
    
    def extract_models(self, tree: CompilationUnit) -> List[Dict[str, Any]]:
        """Extract data model classes."""
```

**Example Usage:**
```python
from automation.java_ast_extractor import JavaASTExtractor
from automation.filesystem.local import LocalFileSystem

# Setup
fs = LocalFileSystem()
extractor = JavaASTExtractor(fs)

# Extract documentation
docs = extractor.extract_documentation("src/main/java/com/example/api/")

# Access extracted information
for endpoint in docs["endpoints"]:
    print(f"Endpoint: {endpoint['operation']}")
    print(f"  Method: {endpoint['method_name']}")
    print(f"  Return: {endpoint['return_type']}")
    for param in endpoint['parameters']:
        print(f"  Param: {param['name']}: {param['type']}")
```

**Extracted Structure:**
```python
{
    "language": "java",
    "endpoints": [
        {
            "type": "SOAP",
            "operation": "getWorkUnits",
            "method_name": "getWorkUnits",
            "return_type": "List<WorkUnitModel>",
            "parameters": [
                {"name": "queryDate", "type": "String"}
            ],
            "namespace": "http://example.com/api",
            "annotations": ["@WebMethod", "@WebResult"]
        }
    ],
    "services": [
        {
            "name": "UserService",
            "type": "service",
            "methods": [
                {
                    "name": "findUserById",
                    "return_type": "User",
                    "parameters": [{"name": "id", "type": "Long"}]
                }
            ]
        }
    ],
    "models": [
        {
            "name": "User",
            "type": "class",
            "fields": [
                {"name": "id", "type": "Long"},
                {"name": "username", "type": "String"}
            ]
        }
    ]
}
```

---

### Build System

#### `automation.build.build_docs`

**Main documentation build function**

```python
def build_docs(
    source_dir: str = "docs/source",
    build_dir: str = "docs/build",
    format: str = "html",
    clean: bool = False,
    verbose: bool = False,
    parallel: bool = True
) -> int:
    """
    Build Sphinx documentation.
    
    Args:
        source_dir: Source directory containing conf.py
        build_dir: Output directory for built documentation
        format: Output format (html, pdf, epub, latex)
        clean: Clean build directory before building
        verbose: Enable verbose output
        parallel: Enable parallel build
        
    Returns:
        Exit code (0 for success, non-zero for failure)
    """
```

**Example Usage:**
```python
from automation.build import build_docs

# Build HTML documentation
result = build_docs(format="html", clean=True)

# Build PDF with verbose output
result = build_docs(format="pdf", verbose=True)

# Custom directories
result = build_docs(
    source_dir="custom/source",
    build_dir="custom/build"
)
```

---

## CLI Commands

### Documentation Commands

#### `docs-build`
Build Sphinx documentation in various formats.

```bash
uv run docs-build [OPTIONS]

Options:
  --format TEXT      Output format (html, pdf, epub, latex) [default: html]
  --clean           Clean build directory before building
  --verbose         Enable verbose output
  --no-parallel     Disable parallel build
  --source TEXT     Source directory [default: docs/source]
  --output TEXT     Output directory [default: docs/build]
```

#### `docs-serve`
Serve documentation locally with hot reload.

```bash
uv run docs-serve [OPTIONS]

Options:
  --port INT        Port to serve on [default: 8000]
  --host TEXT       Host to bind to [default: 127.0.0.1]
  --no-reload       Disable auto-reload
  --open           Open browser automatically
```

#### `docs-clean`
Clean documentation build artifacts.

```bash
uv run docs-clean [OPTIONS]

Options:
  --all            Clean all build artifacts
  --cache          Clean only cache files
  --output TEXT    Build directory to clean [default: docs/build]
```

### Discovery Commands

#### `java-docs`
Extract Java API documentation.

```bash
uv run java-docs SOURCE [OPTIONS]

Arguments:
  SOURCE           Path to Java source code

Options:
  --output TEXT    Output directory for documentation
  --format TEXT    Output format (json, rst, markdown) [default: rst]
  --recursive      Process directories recursively
  --verbose        Enable verbose output
```

**Example:**
```bash
# Extract documentation from Java project
uv run java-docs ./src/main/java --output ./docs/api/

# Extract as JSON for processing
uv run java-docs ./MyService.java --format json > api.json
```

#### `azure-docs` (Planned)
Generate Azure infrastructure documentation.

```bash
uv run azure-docs [OPTIONS]

Options:
  --subscription TEXT   Azure subscription ID
  --resource-group TEXT Resource group to document
  --output TEXT        Output directory
  --format TEXT        Output format (rst, markdown)
```

#### `sql-docs` (Planned)
Extract SQL database documentation.

```bash
uv run sql-docs CONNECTION_STRING [OPTIONS]

Arguments:
  CONNECTION_STRING    SQL Server connection string

Options:
  --output TEXT       Output directory
  --include-views     Include views in documentation
  --include-procs     Include stored procedures
  --generate-erd      Generate entity relationship diagram
```

---

## Configuration

### pyproject.toml Configuration

```toml
[tool.uv]
# UV-specific settings
package = true

# Constraint dependencies
constraint-dependencies = [
    "docutils<0.21",
    "azure-core<2.0.0",
]

# Cache configuration
cache-keys = [
    { file = "pyproject.toml" },
    { file = "automation/**/*.py" },
    { git = { commit = true } },
]

# Index configuration
[[tool.uv.index]]
name = "pypi"
url = "https://pypi.org/simple"
default = true
```

### Environment Variables

```bash
# Azure configuration
export AZURE_SUBSCRIPTION_ID="your-subscription-id"
export AZURE_TENANT_ID="your-tenant-id"
export AZURE_CLIENT_ID="your-client-id"
export AZURE_CLIENT_SECRET="your-secret"

# SQL configuration
export SQL_CONNECTION_STRING="Server=...;Database=...;UID=...;PWD=..."

# IT Glue configuration
export ITGLUE_API_KEY="your-api-key"
export ITGLUE_ORG_ID="your-org-id"

# Documentation settings
export DOCS_OUTPUT_DIR="/path/to/output"
export DOCS_FORMAT="html"
```

### Configuration File (Planned)

```yaml
# config.yaml
azure:
  subscription_id: ${AZURE_SUBSCRIPTION_ID}
  tenant_id: ${AZURE_TENANT_ID}
  resource_groups:
    - production-rg
    - staging-rg

sql:
  connections:
    - name: primary
      connection_string: ${SQL_CONNECTION_STRING}
    - name: reporting
      server: reporting.database.windows.net
      database: ReportingDB

output:
  directory: docs/generated
  formats:
    - html
    - pdf
  
deployment:
  itglue:
    api_key: ${ITGLUE_API_KEY}
    org_id: ${ITGLUE_ORG_ID}
```

---

## Error Handling

### Exception Hierarchy

```python
FileSystemError          # Base filesystem exception
├── FileNotFoundError    # File or directory not found
├── PermissionError      # Insufficient permissions
└── ValidationError      # Invalid path or operation

DiscoveryError          # Base discovery exception (planned)
├── AzureDiscoveryError # Azure-specific errors
├── SQLDiscoveryError   # SQL-specific errors
└── ConfigurationError  # Configuration issues
```

### Error Codes

| Code | Description | Resolution |
|------|-------------|------------|
| FS001 | File not found | Verify file path exists |
| FS002 | Permission denied | Check file permissions |
| FS003 | Invalid path | Ensure path doesn't contain invalid characters |
| AZ001 | Azure authentication failed | Verify credentials |
| AZ002 | Resource not found | Check resource exists in subscription |
| SQL001 | Connection failed | Verify connection string |
| SQL002 | Schema extraction failed | Check database permissions |

---

**API Version**: 0.1.0  
**Last Updated**: 2025-08-27