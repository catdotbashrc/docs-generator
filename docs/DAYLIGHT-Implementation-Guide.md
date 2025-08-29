# DAYLIGHT Implementation Guide
**Practical Guide to Building JavaScript/TypeScript Documentation Extractors**

## Table of Contents
- [Quick Start](#quick-start)
- [Extractor Development Pattern](#extractor-development-pattern)
- [File Pattern Matching](#file-pattern-matching)
- [Data Extraction Techniques](#data-extraction-techniques)
- [Error Handling Best Practices](#error-handling-best-practices)
- [Testing Implementation](#testing-implementation)
- [Performance Optimization](#performance-optimization)
- [Integration Examples](#integration-examples)

---

## Quick Start

### Setting Up a New Extractor

#### 1. Create Extractor Class Structure
```python
# automation/daylight_extractors.py

from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import re

class NewDimensionExtractor(DaylightExtractor):
    """
    Extract [DIMENSION] information for JavaScript/TypeScript projects.
    
    Static Analysis Coverage: [XX]% - What can be extracted without runtime
    Target Files: List the specific file patterns this extractor processes
    Maintenance Value: Explain what 2AM incident scenarios this helps with
    """
    
    def extract(self) -> Dict[str, Any]:
        """Extract all [DIMENSION] information."""
        self.results = {
            "dimension": "[DimensionName]",
            # Add dimension-specific fields here
        }
        
        # Implement extraction logic
        self.results["key_data"] = self._extract_key_data()
        
        return self.results
    
    def _extract_key_data(self) -> Dict[str, Any]:
        """Core extraction method - implement your logic here."""
        pass
```

#### 2. Add to Main Extraction Function
```python
# In run_daylight_extraction() function
extractors = {
    "dependencies": DependenciesExtractor(project_path),
    "automation": AutomationExtractor(project_path),
    "yearbook": YearbookExtractor(project_path),
    "lifecycle": LifecycleExtractor(project_path),
    "new_dimension": NewDimensionExtractor(project_path),  # Add your extractor
}
```

#### 3. Create Test Suite
```python
# tests/test_daylight_extractors.py

class TestNewDimensionExtractor:
    """Test the [DimensionName] extractor."""
    
    def test_extracts_basic_information(self, tmp_path):
        """
        DAYLIGHT [DimensionName] Test: Basic extraction works.
        
        Given: A JavaScript project with [specific files]
        When: [DimensionName] extractor runs
        Then: Key information is extracted correctly
        """
        # Arrange - create test project structure
        self._create_test_project(tmp_path)
        
        # Act - run extractor
        extractor = NewDimensionExtractor(str(tmp_path))
        results = extractor.extract()
        
        # Assert - verify results
        assert results["dimension"] == "[DimensionName]"
        assert len(extractor.errors) == 0
```

---

## Extractor Development Pattern

### The 5-Step Extractor Pattern

#### 1. Discovery Phase
```python
def _discover_target_files(self) -> List[Path]:
    """Find all files relevant to this dimension."""
    target_files = []
    
    # Direct file patterns
    for pattern in self.FILE_PATTERNS:
        matches = self.project_path.glob(pattern)
        target_files.extend(matches)
    
    # Directory-based discovery  
    for dir_pattern in self.DIRECTORY_PATTERNS:
        if (self.project_path / dir_pattern).exists():
            dir_files = (self.project_path / dir_pattern).rglob("*")
            target_files.extend([f for f in dir_files if f.is_file()])
    
    return target_files
```

#### 2. Parsing Phase
```python
def _parse_file_safely(self, file_path: Path) -> Optional[Dict]:
    """Parse file with comprehensive error handling."""
    try:
        if file_path.suffix == '.json':
            return self._parse_json_file(file_path)
        elif file_path.suffix in ['.yml', '.yaml']:
            return self._parse_yaml_file(file_path)
        elif file_path.suffix == '.js':
            return self._parse_js_file(file_path)
        else:
            return self._parse_text_file(file_path)
    except Exception as e:
        self.log_error(f"Failed to parse {file_path}: {e}", str(file_path))
        return None

def _parse_json_file(self, file_path: Path) -> Optional[Dict]:
    """JSON parsing with validation."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = json.load(f)
            return content if isinstance(content, dict) else {"content": content}
    except json.JSONDecodeError as e:
        self.log_error(f"Invalid JSON in {file_path}: {e}", str(file_path))
        return None
```

#### 3. Analysis Phase
```python
def _analyze_extracted_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """Transform raw parsed data into maintenance insights."""
    analyzed_data = {}
    
    # Count and categorize
    analyzed_data["counts"] = self._calculate_counts(raw_data)
    
    # Detect patterns
    analyzed_data["patterns"] = self._detect_patterns(raw_data)
    
    # Identify issues
    analyzed_data["issues"] = self._identify_potential_issues(raw_data)
    
    # Calculate metrics
    analyzed_data["metrics"] = self._calculate_metrics(raw_data)
    
    return analyzed_data

def _identify_potential_issues(self, data: Dict[str, Any]) -> List[Dict[str, str]]:
    """Identify potential maintenance issues."""
    issues = []
    
    # Example: Too many dependencies
    if data.get("dependency_count", 0) > 100:
        issues.append({
            "type": "maintenance_burden",
            "severity": "medium",
            "description": f"{data['dependency_count']} dependencies may impact maintainability",
            "recommendation": "Consider dependency audit and consolidation"
        })
    
    return issues
```

#### 4. Validation Phase
```python
def _validate_results(self, results: Dict[str, Any]) -> bool:
    """Validate extraction results before returning."""
    validation_errors = []
    
    # Schema validation
    if not self._validate_schema(results):
        validation_errors.append("Schema validation failed")
    
    # Required fields validation
    required_fields = ["dimension"]  # Add dimension-specific required fields
    for field in required_fields:
        if field not in results:
            validation_errors.append(f"Missing required field: {field}")
    
    # Data consistency validation
    consistency_errors = self._validate_data_consistency(results)
    validation_errors.extend(consistency_errors)
    
    # Log validation errors
    for error in validation_errors:
        self.log_error("VALIDATION_ERROR", error)
    
    return len(validation_errors) == 0
```

#### 5. Documentation Phase
```python
def _generate_maintenance_insights(self, data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate actionable maintenance insights."""
    insights = {
        "summary": self._create_summary(data),
        "quick_actions": self._suggest_quick_actions(data),
        "health_score": self._calculate_health_score(data),
        "alerts": self._generate_alerts(data)
    }
    
    return insights

def _suggest_quick_actions(self, data: Dict[str, Any]) -> List[Dict[str, str]]:
    """Suggest immediate actionable items for maintenance."""
    actions = []
    
    # Example logic for dependency dimension
    if data.get("outdated_packages"):
        actions.append({
            "action": "update_dependencies",
            "priority": "high",
            "description": f"Update {len(data['outdated_packages'])} outdated packages",
            "command": "npm update"
        })
    
    return actions
```

---

## File Pattern Matching

### Comprehensive File Pattern Library

#### JavaScript/TypeScript Project Files
```python
class FilePatterns:
    """Centralized file patterns for JavaScript/TypeScript projects."""
    
    # Core JavaScript files
    JS_TS_FILES = [
        "**/*.js", "**/*.jsx", "**/*.ts", "**/*.tsx",
        "**/*.mjs", "**/*.cjs", "**/*.vue"
    ]
    
    # Configuration files by category
    PACKAGE_MANAGEMENT = [
        "package.json", "yarn.lock", "package-lock.json", 
        "pnpm-lock.yaml", "npm-shrinkwrap.json", ".nvmrc"
    ]
    
    BUILD_TOOLS = [
        "webpack.config.js", "webpack.config.ts",
        "vite.config.js", "vite.config.ts", 
        "rollup.config.js", "rollup.config.ts",
        "next.config.js", "nuxt.config.js",
        "vue.config.js", "angular.json"
    ]
    
    TESTING_FILES = [
        "jest.config.js", "jest.config.json",
        "vitest.config.js", "vitest.config.ts",
        "cypress.config.js", "playwright.config.js",
        "**/*.test.js", "**/*.spec.js", 
        "**/*.test.ts", "**/*.spec.ts",
        "__tests__/**/*", "tests/**/*", "test/**/*"
    ]
    
    CI_CD_FILES = [
        ".github/workflows/*.yml", ".github/workflows/*.yaml",
        ".travis.yml", ".circleci/config.yml",
        "azure-pipelines.yml", "buildspec.yml", "Jenkinsfile"
    ]
    
    ENVIRONMENT_FILES = [
        ".env*", "config/**/*", "environments/**/*",
        "**/*.config.js", "**/*.config.json"
    ]
    
    LINTING_FILES = [
        ".eslintrc*", ".prettierrc*", ".editorconfig",
        "tsconfig.json", "jsconfig.json"
    ]
    
    DOCKER_FILES = [
        "Dockerfile*", "docker-compose*.yml", 
        "docker-compose*.yaml", ".dockerignore"
    ]

# Usage in extractors
class GovernanceExtractor(DaylightExtractor):
    def _get_target_files(self) -> List[Path]:
        """Get governance-related files."""
        target_files = []
        
        for pattern in FilePatterns.LINTING_FILES:
            matches = self.project_path.glob(pattern)
            target_files.extend(matches)
        
        return target_files
```

### Dynamic File Discovery
```python
def _discover_files_by_content(self, content_patterns: List[str]) -> List[Path]:
    """Discover files by content patterns, not just filename."""
    discovered_files = []
    
    # Search JavaScript/TypeScript files for content patterns
    for js_file in self.project_path.glob("**/*.{js,ts,jsx,tsx}"):
        try:
            content = js_file.read_text(encoding='utf-8')
            
            for pattern in content_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    discovered_files.append(js_file)
                    break  # Found match, move to next file
                    
        except Exception as e:
            self.log_error(f"Failed to read {js_file}: {e}")
    
    return discovered_files

# Example usage for API endpoint discovery
def _discover_api_files(self) -> List[Path]:
    """Find files that likely contain API endpoint definitions."""
    api_patterns = [
        r'app\.get\(|app\.post\(|app\.put\(|app\.delete\(',  # Express.js
        r'@Get\(|@Post\(|@Put\(|@Delete\(',                   # NestJS decorators
        r'router\.get|router\.post',                          # Router patterns
        r'export\s+const\s+\w+\s*=\s*async\s*\(',           # API functions
        r'api\.|fetch\(|axios\.',                             # API calls
    ]
    
    return self._discover_files_by_content(api_patterns)
```

---

## Data Extraction Techniques

### JSON/YAML Configuration Parsing
```python
class ConfigurationParser:
    """Robust configuration file parsing utilities."""
    
    @staticmethod
    def parse_package_json(file_path: Path) -> Dict[str, Any]:
        """Parse package.json with validation and error recovery."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Validate required fields
            if not isinstance(data, dict):
                raise ValueError("package.json must be a JSON object")
            
            # Normalize data structure
            normalized = {
                "name": data.get("name", "unknown"),
                "version": data.get("version", "0.0.0"),
                "description": data.get("description", ""),
                "dependencies": data.get("dependencies", {}),
                "devDependencies": data.get("devDependencies", {}),
                "scripts": data.get("scripts", {}),
                "engines": data.get("engines", {}),
            }
            
            return normalized
            
        except json.JSONDecodeError as e:
            # Try to recover partial data
            return ConfigurationParser._attempt_json_recovery(file_path, e)
    
    @staticmethod
    def _attempt_json_recovery(file_path: Path, error: json.JSONDecodeError) -> Dict:
        """Attempt to recover data from malformed JSON."""
        try:
            content = file_path.read_text()
            
            # Try to extract basic fields with regex
            name_match = re.search(r'"name":\s*"([^"]+)"', content)
            version_match = re.search(r'"version":\s*"([^"]+)"', content)
            
            recovery_data = {
                "name": name_match.group(1) if name_match else "unknown",
                "version": version_match.group(1) if version_match else "0.0.0",
                "_parse_error": str(error),
                "_partial_recovery": True
            }
            
            return recovery_data
            
        except Exception:
            return {"_parse_error": str(error), "_recovery_failed": True}
```

### JavaScript Code Analysis
```python
class JavaScriptAnalyzer:
    """Basic JavaScript/TypeScript code analysis without AST parsing."""
    
    def extract_imports_exports(self, file_path: Path) -> Dict[str, List[str]]:
        """Extract import/export statements from JavaScript files."""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Import patterns
            import_patterns = [
                r'import\s+.*?\s+from\s+[\'"]([^\'"]+)[\'"]',      # import x from 'module'
                r'import\s+[\'"]([^\'"]+)[\'"]',                   # import 'module'
                r'require\([\'"]([^\'"]+)[\'"]\)',                 # require('module')
            ]
            
            imports = []
            for pattern in import_patterns:
                matches = re.findall(pattern, content, re.MULTILINE)
                imports.extend(matches)
            
            # Export patterns
            export_patterns = [
                r'export\s+(?:default\s+)?(?:function|class|const|let|var)\s+(\w+)',
                r'export\s*{\s*([^}]+)\s*}',
                r'module\.exports\s*=\s*(\w+)',
            ]
            
            exports = []
            for pattern in export_patterns:
                matches = re.findall(pattern, content, re.MULTILINE)
                exports.extend(matches)
            
            return {
                "imports": imports,
                "exports": exports,
                "file_type": self._detect_file_type(content)
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def _detect_file_type(self, content: str) -> str:
        """Detect JavaScript file type based on content patterns."""
        if 'import React' in content or 'from "react"' in content:
            return "react"
        elif '@Component' in content or 'from "@angular' in content:
            return "angular"
        elif 'export default {' in content and 'methods:' in content:
            return "vue"
        elif 'export default' in content:
            return "module"
        else:
            return "script"
```

### Git Repository Analysis
```python
class GitAnalyzer:
    """Git repository analysis for Yearbook dimension."""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.git_available = (project_path / '.git').exists()
    
    def get_commit_statistics(self) -> Dict[str, Any]:
        """Get commit statistics safely."""
        if not self.git_available:
            return {"is_git_repo": False}
        
        try:
            import subprocess
            
            # Get commit count
            commit_count_result = subprocess.run(
                ["git", "rev-list", "--count", "HEAD"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            commit_count = int(commit_count_result.stdout.strip()) if commit_count_result.returncode == 0 else 0
            
            # Get contributors
            contributors_result = subprocess.run(
                ["git", "shortlog", "-sn", "--all"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=15
            )
            
            contributors = []
            if contributors_result.returncode == 0:
                for line in contributors_result.stdout.strip().split('\n')[:10]:
                    if '\t' in line:
                        commits, name = line.strip().split('\t', 1)
                        contributors.append({
                            "name": name,
                            "commits": int(commits)
                        })
            
            return {
                "is_git_repo": True,
                "total_commits": commit_count,
                "contributors": contributors
            }
            
        except subprocess.TimeoutExpired:
            return {"is_git_repo": True, "error": "Git commands timed out"}
        except Exception as e:
            return {"is_git_repo": True, "error": str(e)}
```

---

## Error Handling Best Practices

### Error Classification and Recovery
```python
class RobustExtractor(DaylightExtractor):
    """Example of robust error handling patterns."""
    
    def extract(self) -> Dict[str, Any]:
        """Extract with comprehensive error handling."""
        extraction_results = {
            "dimension": self.__class__.__name__.replace("Extractor", ""),
            "success": True,
            "errors": [],
            "warnings": []
        }
        
        # Critical extraction - failure prevents useful output
        try:
            critical_data = self._extract_critical_data()
            extraction_results.update(critical_data)
        except Exception as e:
            self.log_error("CRITICAL_EXTRACTION_FAILED", str(e))
            extraction_results["success"] = False
            return extraction_results
        
        # Optional extractions - failures reduce completeness but don't prevent output
        extraction_results["optional_data"] = self._extract_optional_data_safely()
        
        # Enhancement extractions - failures only reduce insights
        extraction_results["enhanced_insights"] = self._extract_enhancements_safely()
        
        return extraction_results
    
    def _extract_optional_data_safely(self) -> Dict[str, Any]:
        """Extract optional data with graceful degradation."""
        optional_data = {}
        
        # List of optional extraction methods
        optional_methods = [
            ("security_info", self._extract_security_info),
            ("performance_data", self._extract_performance_data), 
            ("quality_metrics", self._extract_quality_metrics)
        ]
        
        for data_key, extraction_method in optional_methods:
            try:
                result = extraction_method()
                optional_data[data_key] = result
            except Exception as e:
                self.log_error(f"OPTIONAL_EXTRACTION_FAILED", f"{data_key}: {e}")
                optional_data[data_key] = None  # Indicate attempted but failed
        
        return optional_data
    
    def _extract_enhancements_safely(self) -> Dict[str, Any]:
        """Extract enhancement data that improves insights but isn't essential."""
        enhancements = {}
        
        enhancement_methods = [
            ("trend_analysis", self._analyze_trends),
            ("optimization_suggestions", self._generate_optimization_suggestions),
            ("comparison_metrics", self._calculate_comparison_metrics)
        ]
        
        for enhancement_key, enhancement_method in enhancement_methods:
            try:
                result = enhancement_method()
                enhancements[enhancement_key] = result
            except Exception as e:
                # Log as warning, not error, since these are enhancements
                self.log_error(f"ENHANCEMENT_FAILED", f"{enhancement_key}: {e}")
                # Don't include failed enhancements in output
        
        return enhancements
```

### Context-Aware Error Messages
```python
def log_contextual_error(self, operation: str, error: Exception, 
                        context: Dict[str, Any] = None):
    """Log errors with rich context for debugging."""
    error_context = {
        "operation": operation,
        "error_type": type(error).__name__,
        "error_message": str(error),
        "project_path": str(self.project_path),
        "timestamp": datetime.now().isoformat()
    }
    
    if context:
        error_context.update(context)
    
    # Create actionable error message
    if isinstance(error, FileNotFoundError):
        suggestion = f"Ensure {error.filename} exists in the project directory"
    elif isinstance(error, json.JSONDecodeError):
        suggestion = f"Check JSON syntax in file around line {getattr(error, 'lineno', 'unknown')}"
    elif isinstance(error, PermissionError):
        suggestion = "Check file permissions and directory access rights"
    else:
        suggestion = "Review the error details and project structure"
    
    error_context["suggestion"] = suggestion
    
    self.log_error("CONTEXTUAL_ERROR", json.dumps(error_context, indent=2))
```

---

## Testing Implementation

### Test-Driven Development for Extractors

#### 1. Test Structure Pattern
```python
class TestDimensionExtractor:
    """Standard test class structure for DAYLIGHT extractors."""
    
    @pytest.fixture
    def minimal_js_project(self, tmp_path):
        """Create minimal JavaScript project for testing."""
        package_json = {
            "name": "test-project",
            "version": "1.0.0"
        }
        (tmp_path / "package.json").write_text(json.dumps(package_json))
        return tmp_path
    
    @pytest.fixture
    def complex_js_project(self, tmp_path):
        """Create complex JavaScript project with multiple configurations."""
        # Create package.json
        package_json = {
            "name": "complex-test-project",
            "version": "1.2.3",
            "scripts": {
                "start": "node server.js",
                "test": "jest",
                "build": "webpack --mode production"
            },
            "dependencies": {"express": "^4.18.0"},
            "devDependencies": {"jest": "^29.0.0"}
        }
        (tmp_path / "package.json").write_text(json.dumps(package_json, indent=2))
        
        # Create additional configuration files
        (tmp_path / "webpack.config.js").write_text("module.exports = {};")
        (tmp_path / ".eslintrc.js").write_text("module.exports = {};")
        
        # Create directory structures
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "index.js").write_text("console.log('Hello');")
        (tmp_path / "tests").mkdir()
        (tmp_path / "tests" / "index.test.js").write_text("test('example', () => {});")
        
        return tmp_path
    
    def test_extracts_from_minimal_project(self, minimal_js_project):
        """Test extraction works on minimal project."""
        extractor = DimensionExtractor(str(minimal_js_project))
        results = extractor.extract()
        
        assert results["dimension"] == "DimensionName"
        assert results["success"] == True
        assert len(extractor.errors) == 0
    
    def test_extracts_from_complex_project(self, complex_js_project):
        """Test extraction works on complex project with rich data."""
        extractor = DimensionExtractor(str(complex_js_project))
        results = extractor.extract()
        
        # Verify comprehensive extraction
        assert results["success"] == True
        assert len(results["key_data"]) > 0
        
        # Verify specific extracted data
        assert results["specific_field"] == "expected_value"
    
    def test_handles_missing_files_gracefully(self, tmp_path):
        """Test extractor handles missing files without crashing."""
        # Don't create any files - empty directory
        extractor = DimensionExtractor(str(tmp_path))
        results = extractor.extract()
        
        # Should not crash, but may have reduced functionality
        assert results["dimension"] == "DimensionName"
        # May have errors logged, but extraction should complete
    
    def test_handles_malformed_configs_gracefully(self, tmp_path):
        """Test extractor handles malformed configuration files."""
        # Create malformed package.json
        (tmp_path / "package.json").write_text('{"name": "test", invalid json}')
        
        extractor = DimensionExtractor(str(tmp_path))
        results = extractor.extract()
        
        # Should complete extraction with errors logged
        assert results["dimension"] == "DimensionName"
        assert len(extractor.errors) > 0
        assert any("parse" in error["error"].lower() for error in extractor.errors)
```

#### 2. Property-Based Testing
```python
from hypothesis import given, strategies as st
import json

class TestExtractorRobustness:
    """Property-based tests for extractor robustness."""
    
    @given(st.dictionaries(
        st.text(min_size=1, max_size=50),
        st.one_of(st.text(), st.integers(), st.lists(st.text()))
    ))
    def test_handles_arbitrary_package_json_data(self, package_data, tmp_path):
        """Test extractor handles arbitrary package.json content."""
        try:
            # Create package.json with arbitrary valid JSON data
            (tmp_path / "package.json").write_text(json.dumps(package_data))
            
            extractor = DependenciesExtractor(str(tmp_path))
            results = extractor.extract()
            
            # Should always return valid result structure
            assert "dimension" in results
            assert isinstance(results.get("errors", []), list)
            
        except Exception as e:
            # If extraction fails, should be a logged error, not unhandled exception
            assert False, f"Unhandled exception: {e}"
    
    @given(st.text(min_size=0, max_size=10000))
    def test_handles_arbitrary_file_content(self, file_content, tmp_path):
        """Test extractor handles arbitrary file content safely."""
        # Create file with arbitrary content
        (tmp_path / "config.js").write_text(file_content)
        
        extractor = AutomationExtractor(str(tmp_path))
        
        # Should not crash regardless of file content
        try:
            results = extractor.extract()
            assert isinstance(results, dict)
        except Exception as e:
            assert False, f"Extractor crashed on arbitrary content: {e}"
```

#### 3. Performance Testing
```python
class TestExtractionPerformance:
    """Performance tests for extractors."""
    
    def test_extraction_time_within_limits(self, complex_js_project):
        """Test extraction completes within reasonable time."""
        import time
        
        extractor = DimensionExtractor(str(complex_js_project))
        
        start_time = time.time()
        results = extractor.extract()
        end_time = time.time()
        
        extraction_time = end_time - start_time
        
        # Should complete within 5 seconds for typical project
        assert extraction_time < 5.0, f"Extraction took {extraction_time:.2f}s, expected < 5.0s"
    
    def test_memory_usage_reasonable(self, complex_js_project):
        """Test extraction doesn't consume excessive memory."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        memory_before = process.memory_info().rss / 1024 / 1024  # MB
        
        extractor = DimensionExtractor(str(complex_js_project))
        results = extractor.extract()
        
        memory_after = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = memory_after - memory_before
        
        # Should not increase memory by more than 50MB for typical project
        assert memory_increase < 50, f"Memory increased by {memory_increase:.1f}MB, expected < 50MB"
```

---

## Performance Optimization

### Caching and Memoization
```python
from functools import lru_cache
import hashlib

class OptimizedExtractor(DaylightExtractor):
    """Example of performance optimization techniques."""
    
    def __init__(self, project_path: str):
        super().__init__(project_path)
        self._file_cache = {}
        self._analysis_cache = {}
    
    @lru_cache(maxsize=128)
    def _get_file_hash(self, file_path: Path) -> str:
        """Get file hash for cache invalidation."""
        try:
            content = file_path.read_bytes()
            return hashlib.md5(content).hexdigest()
        except:
            return ""
    
    def _read_file_cached(self, file_path: Path) -> Optional[str]:
        """Read file with caching based on modification time."""
        try:
            file_hash = self._get_file_hash(file_path)
            cache_key = f"{file_path}:{file_hash}"
            
            if cache_key in self._file_cache:
                return self._file_cache[cache_key]
            
            content = file_path.read_text(encoding='utf-8')
            self._file_cache[cache_key] = content
            return content
            
        except Exception as e:
            self.log_error(f"Failed to read {file_path}: {e}")
            return None
    
    def _analyze_with_cache(self, analysis_key: str, 
                           analysis_func: callable, *args) -> Any:
        """Perform analysis with caching."""
        # Create cache key from function name and arguments
        cache_key = f"{analysis_key}:{hash(str(args))}"
        
        if cache_key in self._analysis_cache:
            return self._analysis_cache[cache_key]
        
        result = analysis_func(*args)
        self._analysis_cache[cache_key] = result
        return result
```

### Parallel Processing
```python
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Callable

class ParallelExtractor(DaylightExtractor):
    """Example of parallel processing for large projects."""
    
    def extract(self) -> Dict[str, Any]:
        """Extract using parallel processing for large file sets."""
        target_files = self._get_target_files()
        
        if len(target_files) < 10:
            # Use sequential processing for small projects
            return self._extract_sequential(target_files)
        else:
            # Use parallel processing for large projects
            return self._extract_parallel(target_files)
    
    def _extract_parallel(self, files: List[Path]) -> Dict[str, Any]:
        """Extract using parallel processing."""
        results = {"dimension": self.__class__.__name__.replace("Extractor", "")}
        
        # Process files in parallel
        with ThreadPoolExecutor(max_workers=4) as executor:
            # Submit all file processing jobs
            future_to_file = {
                executor.submit(self._process_file, file_path): file_path 
                for file_path in files
            }
            
            file_results = {}
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    file_result = future.result()
                    file_results[str(file_path)] = file_result
                except Exception as e:
                    self.log_error(f"Failed to process {file_path}: {e}")
        
        # Aggregate results from parallel processing
        results["processed_files"] = file_results
        results["file_count"] = len(file_results)
        
        # Perform analysis on aggregated data
        results["analysis"] = self._analyze_aggregated_data(file_results)
        
        return results
    
    def _process_file(self, file_path: Path) -> Dict[str, Any]:
        """Process individual file - designed for parallel execution."""
        try:
            # This method should be thread-safe
            content = file_path.read_text(encoding='utf-8')
            
            return {
                "size": len(content),
                "lines": content.count('\n'),
                "type": file_path.suffix,
                "analysis": self._analyze_file_content(content)
            }
        except Exception as e:
            return {"error": str(e)}
```

### Memory-Efficient Processing
```python
class MemoryEfficientExtractor(DaylightExtractor):
    """Example of memory-efficient processing for large projects."""
    
    def extract(self) -> Dict[str, Any]:
        """Extract using streaming and generator patterns."""
        results = {"dimension": self.__class__.__name__.replace("Extractor", "")}
        
        # Use generators to process files without loading all into memory
        file_generator = self._get_files_generator()
        
        # Process files in batches
        batch_size = 50
        batch_results = []
        
        current_batch = []
        for file_path in file_generator:
            current_batch.append(file_path)
            
            if len(current_batch) >= batch_size:
                batch_result = self._process_batch(current_batch)
                batch_results.append(batch_result)
                current_batch = []  # Clear batch to free memory
        
        # Process remaining files
        if current_batch:
            batch_result = self._process_batch(current_batch)
            batch_results.append(batch_result)
        
        # Aggregate batch results efficiently
        results.update(self._aggregate_batch_results(batch_results))
        
        return results
    
    def _get_files_generator(self):
        """Generator for files to avoid loading all paths into memory."""
        for pattern in self.FILE_PATTERNS:
            for file_path in self.project_path.glob(pattern):
                if file_path.is_file():
                    yield file_path
    
    def _process_batch(self, file_batch: List[Path]) -> Dict[str, Any]:
        """Process batch of files efficiently."""
        batch_summary = {
            "file_count": len(file_batch),
            "total_size": 0,
            "file_types": {},
            "analysis_summary": {}
        }
        
        for file_path in file_batch:
            try:
                # Process file without storing full content
                file_stats = self._get_file_stats(file_path)
                batch_summary["total_size"] += file_stats["size"]
                
                file_type = file_path.suffix
                batch_summary["file_types"][file_type] = batch_summary["file_types"].get(file_type, 0) + 1
                
            except Exception as e:
                self.log_error(f"Failed to process {file_path}: {e}")
        
        return batch_summary
```

---

## Integration Examples

### Complete Integration Example
```python
# Example: Implementing the Integration (I) dimension

class IntegrationExtractor(DaylightExtractor):
    """
    Extract Integration (I) dimension - API endpoints, external services, webhooks.
    
    Static Analysis Coverage: 70% - Can extract most API definitions and configurations
    Target Files: API route files, service configurations, OpenAPI specs
    Maintenance Value: Helps identify external dependencies and API surface area during incidents
    """
    
    def extract(self) -> Dict[str, Any]:
        """Extract all Integration information."""
        self.results = {
            "dimension": "Integration",
            "api_endpoints": self._extract_api_endpoints(),
            "external_services": self._extract_external_services(),
            "webhooks": self._extract_webhook_configs(),
            "database_connections": self._extract_database_configs(),
            "message_queues": self._extract_queue_configs()
        }
        
        # Calculate integration complexity
        self.results["integration_complexity"] = self._calculate_complexity_score()
        
        # Identify potential issues
        self.results["integration_issues"] = self._identify_integration_issues()
        
        return self.results
    
    def _extract_api_endpoints(self) -> List[Dict[str, Any]]:
        """Extract API endpoint definitions."""
        endpoints = []
        
        # Find API-related files
        api_files = self._discover_api_files()
        
        for file_path in api_files:
            try:
                content = self._read_file_cached(file_path)
                if content:
                    file_endpoints = self._parse_endpoints_from_content(content, file_path)
                    endpoints.extend(file_endpoints)
            except Exception as e:
                self.log_error(f"Failed to extract endpoints from {file_path}: {e}")
        
        return endpoints
    
    def _discover_api_files(self) -> List[Path]:
        """Find files that likely contain API endpoint definitions."""
        api_patterns = [
            r'app\.(get|post|put|delete|patch)\(',    # Express.js
            r'@(Get|Post|Put|Delete|Patch)\(',         # NestJS/Spring-like decorators
            r'router\.(get|post|put|delete)',          # Router patterns
            r'export\s+const\s+\w+\s*=\s*async\s*\(',  # API functions
        ]
        
        return self._discover_files_by_content(api_patterns)
    
    def _parse_endpoints_from_content(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """Parse API endpoints from file content."""
        endpoints = []
        
        # Express.js pattern: app.get('/path', handler)
        express_pattern = r'app\.(get|post|put|delete|patch)\([\'"]([^\'"]+)[\'"]'
        express_matches = re.findall(express_pattern, content)
        
        for method, path in express_matches:
            endpoints.append({
                "method": method.upper(),
                "path": path,
                "file": str(file_path),
                "framework": "express"
            })
        
        # Decorator pattern: @Get('/path')
        decorator_pattern = r'@(Get|Post|Put|Delete|Patch)\([\'"]([^\'"]+)[\'"]\)'
        decorator_matches = re.findall(decorator_pattern, content)
        
        for method, path in decorator_matches:
            endpoints.append({
                "method": method.upper(),
                "path": path,
                "file": str(file_path),
                "framework": "decorator-based"
            })
        
        return endpoints
    
    def _extract_external_services(self) -> List[Dict[str, Any]]:
        """Extract external service configurations and API calls."""
        external_services = []
        
        # Look for common external service patterns
        service_patterns = [
            (r'https?://api\.([^/\s\'"]+)', 'http_api'),
            (r'mongodb://|mongodb\+srv://', 'mongodb'),
            (r'redis://|rediss://', 'redis'),
            (r'postgres://|postgresql://', 'postgresql'),
            (r'mysql://|mysql2://', 'mysql'),
            (r'aws\.', 'aws'),
            (r'gcp\.|googleapis\.', 'gcp'),
            (r'azure\.|microsoft\.', 'azure')
        ]
        
        js_files = list(self.project_path.glob("**/*.{js,ts,jsx,tsx}"))
        
        for file_path in js_files:
            try:
                content = file_path.read_text(encoding='utf-8')
                
                for pattern, service_type in service_patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        external_services.append({
                            "service_type": service_type,
                            "pattern": match.group(0),
                            "file": str(file_path),
                            "line": content[:match.start()].count('\n') + 1
                        })
                        
            except Exception as e:
                self.log_error(f"Failed to analyze {file_path} for external services: {e}")
        
        return external_services
    
    def _calculate_complexity_score(self) -> float:
        """Calculate integration complexity score (0.0 - 1.0)."""
        api_count = len(self.results.get("api_endpoints", []))
        external_count = len(self.results.get("external_services", []))
        webhook_count = len(self.results.get("webhooks", []))
        
        # Simple complexity scoring
        total_integrations = api_count + external_count + webhook_count
        
        if total_integrations == 0:
            return 0.0
        elif total_integrations < 10:
            return 0.3
        elif total_integrations < 25:
            return 0.6
        else:
            return 1.0
    
    def _identify_integration_issues(self) -> List[Dict[str, str]]:
        """Identify potential integration maintenance issues."""
        issues = []
        
        # Check for high number of external services
        external_count = len(self.results.get("external_services", []))
        if external_count > 20:
            issues.append({
                "type": "high_external_dependency",
                "severity": "medium",
                "description": f"{external_count} external services detected",
                "recommendation": "Consider service consolidation and dependency mapping"
            })
        
        # Check for missing API documentation
        api_count = len(self.results.get("api_endpoints", []))
        openapi_files = list(self.project_path.glob("**/openapi.*")) + list(self.project_path.glob("**/swagger.*"))
        
        if api_count > 5 and not openapi_files:
            issues.append({
                "type": "missing_api_docs",
                "severity": "medium",
                "description": f"{api_count} API endpoints without OpenAPI documentation",
                "recommendation": "Add OpenAPI/Swagger documentation for API endpoints"
            })
        
        return issues

# Register the new extractor
def run_daylight_extraction(project_path: str) -> Dict[str, Any]:
    """Updated to include Integration extractor."""
    extractors = {
        "dependencies": DependenciesExtractor(project_path),
        "automation": AutomationExtractor(project_path),
        "yearbook": YearbookExtractor(project_path),
        "lifecycle": LifecycleExtractor(project_path),
        "integration": IntegrationExtractor(project_path),  # New extractor
    }
    
    # Rest of extraction logic remains the same
    ...
```

### Template Integration
```python
# Add to daylight-maintenance-docs.rst template

{% if dimensions.get('integration') %}
Integration (I)
===============

API Endpoints
-------------

{% if dimensions.integration.api_endpoints %}
{% set endpoints = dimensions.integration.api_endpoints %}
Detected **{{ endpoints|length }}** API endpoints:

{% for endpoint in endpoints[:10] %}
``{{ endpoint.method }} {{ endpoint.path }}``
    Framework: {{ endpoint.framework }}
    File: {{ endpoint.file }}

{% endfor %}
{% if endpoints|length > 10 %}
... and {{ endpoints|length - 10 }} more endpoints
{% endif %}
{% else %}
No API endpoints detected.
{% endif %}

External Services
-----------------

{% if dimensions.integration.external_services %}
{% set services = dimensions.integration.external_services %}
External service integrations: **{{ services|length }}**

{% set service_types = {} %}
{% for service in services %}
  {% set count = service_types.get(service.service_type, 0) + 1 %}
  {% set _ = service_types.update({service.service_type: count}) %}
{% endfor %}

Service breakdown:
{% for service_type, count in service_types.items() %}
* **{{ service_type }}**: {{ count }} integration{{ 's' if count != 1 else '' }}
{% endfor %}
{% else %}
No external service integrations detected.
{% endif %}

{% if dimensions.integration.integration_complexity %}
Integration Complexity
----------------------

:Complexity Score: {{ "%.1f"|format(dimensions.integration.integration_complexity * 10) }}/10
{% if dimensions.integration.integration_complexity > 0.7 %}
:Risk Level: **HIGH** - Complex integration architecture requiring careful maintenance
{% elif dimensions.integration.integration_complexity > 0.4 %}
:Risk Level: **MEDIUM** - Moderate integration complexity
{% else %}
:Risk Level: **LOW** - Simple integration architecture
{% endif %}
{% endif %}

{% if dimensions.integration.integration_issues %}
Integration Issues
------------------

Identified maintenance concerns:

{% for issue in dimensions.integration.integration_issues %}
* **{{ issue.type.replace('_', ' ').title() }}** ({{ issue.severity }})
  
  {{ issue.description }}
  
  *Recommendation*: {{ issue.recommendation }}

{% endfor %}
{% endif %}
{% endif %}
```

This implementation guide provides practical patterns for building DAYLIGHT extractors that are robust, performant, and maintainable. The examples show real-world implementation techniques that can be applied immediately to create working documentation systems.