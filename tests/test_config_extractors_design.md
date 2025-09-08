# Configuration Extractor Test Suite Design

## Overview

This document defines a comprehensive, abstractified test suite for the DDD Configuration Extractors module, following TDD principles and addressing the 87% coverage gap identified in the quality review.

## Design Principles

### 1. **Abstraction First**
- Base test classes for reusable test patterns
- Parametrized tests for multiple languages
- Fixture factories for test data generation

### 2. **TDD Compliance**
- RED: Define behavior through failing tests
- GREEN: Minimal implementation to pass
- REFACTOR: Improve quality maintaining green

### 3. **Robustness**
- Edge case coverage
- Error recovery scenarios
- Performance boundaries
- Security validation

## Test Architecture

```
tests/
├── config_extractors/
│   ├── __init__.py
│   ├── conftest.py                    # Shared fixtures and utilities
│   ├── base.py                        # Abstract test base classes
│   │
│   ├── red_phase/                     # Failing tests defining behavior
│   │   ├── test_config_extraction_contract.py
│   │   ├── test_sensitive_data_detection.py
│   │   └── test_coverage_requirements.py
│   │
│   ├── green_phase/                   # Implementation verification
│   │   ├── test_env_var_extraction.py
│   │   ├── test_connection_string_extraction.py
│   │   ├── test_config_param_extraction.py
│   │   └── test_documentation_detection.py
│   │
│   ├── refactor_phase/                # Quality and performance
│   │   ├── test_extraction_performance.py
│   │   ├── test_multi_language_support.py
│   │   └── test_edge_cases.py
│   │
│   └── integration/                   # Cross-module testing
│       ├── test_cli_integration.py
│       └── test_coverage_integration.py
```

## Abstract Base Test Classes

### 1. BaseConfigExtractorTest

```python
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional
import pytest
from dataclasses import dataclass

@dataclass
class ExtractorTestCase:
    """Represents a test case for configuration extraction"""
    name: str
    input_code: str
    expected_configs: List[Dict]
    language: str
    description: str

class BaseConfigExtractorTest(ABC):
    """Abstract base class for all configuration extractor tests"""
    
    @abstractmethod
    def get_test_cases(self) -> List[ExtractorTestCase]:
        """Return test cases for this extractor type"""
        pass
    
    @abstractmethod
    def get_extractor(self):
        """Return the extractor instance to test"""
        pass
    
    def test_extraction_accuracy(self):
        """Test that all expected configs are extracted correctly"""
        extractor = self.get_extractor()
        for test_case in self.get_test_cases():
            result = extractor.extract_configs(test_case.input_code)
            assert len(result) == len(test_case.expected_configs)
            for expected in test_case.expected_configs:
                assert self._config_exists(result, expected)
    
    def test_no_false_positives(self):
        """Test that non-config patterns are not extracted"""
        extractor = self.get_extractor()
        non_config_code = self.get_non_config_samples()
        for sample in non_config_code:
            result = extractor.extract_configs(sample)
            assert len(result) == 0, f"False positive in: {sample}"
    
    def test_sensitive_data_detection(self):
        """Test that sensitive configs are properly flagged"""
        extractor = self.get_extractor()
        sensitive_cases = self.get_sensitive_test_cases()
        for case in sensitive_cases:
            result = extractor.extract_configs(case.input_code)
            sensitive_configs = [c for c in result if c.is_sensitive]
            assert len(sensitive_configs) > 0
    
    @abstractmethod
    def get_non_config_samples(self) -> List[str]:
        """Return code samples that should NOT trigger extraction"""
        pass
    
    @abstractmethod
    def get_sensitive_test_cases(self) -> List[ExtractorTestCase]:
        """Return test cases with sensitive data"""
        pass
```

### 2. BaseLanguageExtractorTest

```python
class BaseLanguageExtractorTest(BaseConfigExtractorTest):
    """Base class for language-specific extractor tests"""
    
    @property
    @abstractmethod
    def language(self) -> str:
        """The language this test covers"""
        pass
    
    @property
    @abstractmethod
    def file_extensions(self) -> List[str]:
        """File extensions for this language"""
        pass
    
    def test_language_specific_patterns(self):
        """Test language-specific configuration patterns"""
        patterns = self.get_language_patterns()
        extractor = self.get_extractor()
        
        for pattern_code, expected_type in patterns:
            result = extractor.extract_from_code(
                pattern_code, 
                language=self.language
            )
            assert result.type == expected_type
    
    @abstractmethod
    def get_language_patterns(self) -> List[Tuple[str, str]]:
        """Return language-specific pattern test cases"""
        pass
```

## RED Phase Tests (Behavior Definition)

### test_config_extraction_contract.py

```python
"""
RED Phase: Define the contract for configuration extraction
These tests MUST fail initially, defining expected behavior
"""

import pytest
from ddd.config_extractors import ConfigurationExtractor, ConfigArtifact

class TestConfigExtractionContract:
    """Define the configuration extraction contract"""
    
    def test_extractor_must_handle_all_config_types(self):
        """Extractor must handle all defined configuration types"""
        extractor = ConfigurationExtractor()
        config_types = [
            'env_var', 
            'connection_string', 
            'api_key', 
            'config_param', 
            'feature_flag'
        ]
        
        for config_type in config_types:
            # This should fail until implementation supports all types
            assert extractor.supports_type(config_type), \
                f"Extractor must support {config_type}"
    
    def test_extractor_must_detect_documentation(self):
        """Extractor must detect if configs are documented"""
        extractor = ConfigurationExtractor()
        
        documented_code = '''
        # DATABASE_URL - Production database connection
        DATABASE_URL = os.environ.get('DATABASE_URL')
        '''
        
        result = extractor.extract_configs(documented_code)
        assert result[0].is_documented == True
        assert result[0].documentation is not None
    
    def test_extractor_must_calculate_coverage(self):
        """Extractor must calculate documentation coverage"""
        extractor = ConfigurationExtractor()
        project_path = Path("test_project")
        
        result = extractor.calculate_coverage(project_path)
        
        assert hasattr(result, 'coverage_percentage')
        assert hasattr(result, 'risk_score')
        assert result.coverage_percentage >= 0
        assert result.coverage_percentage <= 100
    
    def test_extractor_must_identify_critical_configs(self):
        """Extractor must identify critical undocumented configs"""
        extractor = ConfigurationExtractor()
        
        code_with_critical = '''
        API_SECRET = os.environ.get('API_SECRET')  # No documentation
        DEBUG = os.environ.get('DEBUG', 'false')   # No documentation
        '''
        
        result = extractor.analyze_critical_configs(code_with_critical)
        
        # API_SECRET should be critical (sensitive + undocumented)
        assert 'API_SECRET' in [c.name for c in result.critical_undocumented]
        # DEBUG is not critical
        assert 'DEBUG' not in [c.name for c in result.critical_undocumented]
```

### test_sensitive_data_detection.py

```python
"""
RED Phase: Define sensitive data detection requirements
"""

class TestSensitiveDataDetection:
    """Define requirements for detecting sensitive configuration"""
    
    @pytest.mark.parametrize("config_name,should_be_sensitive", [
        ("DATABASE_PASSWORD", True),
        ("API_SECRET_KEY", True),
        ("AWS_ACCESS_KEY_ID", True),
        ("GITHUB_TOKEN", True),
        ("STRIPE_PRIVATE_KEY", True),
        ("JWT_SECRET", True),
        ("ENCRYPTION_SALT", True),
        ("SSL_CERT_PATH", True),
        ("DEBUG_MODE", False),
        ("LOG_LEVEL", False),
        ("APP_NAME", False),
        ("MAX_RETRIES", False),
    ])
    def test_sensitive_pattern_detection(self, config_name, should_be_sensitive):
        """Test that sensitive patterns are correctly identified"""
        extractor = ConfigurationExtractor()
        
        is_sensitive = extractor.is_sensitive_config(config_name)
        assert is_sensitive == should_be_sensitive, \
            f"{config_name} sensitivity detection failed"
    
    def test_sensitive_configs_never_show_values(self):
        """Sensitive config values must always be redacted"""
        extractor = ConfigurationExtractor()
        
        sensitive_code = '''
        PASSWORD = "actual_password_123"
        API_KEY = "sk_live_abcd1234"
        '''
        
        results = extractor.extract_configs(sensitive_code)
        
        for config in results:
            if config.is_sensitive:
                assert config.default_value == "[REDACTED]"
                assert "actual_password" not in str(config)
                assert "sk_live" not in str(config)
```

## GREEN Phase Tests (Implementation Verification)

### test_env_var_extraction.py

```python
"""
GREEN Phase: Verify environment variable extraction works correctly
"""

from tests.config_extractors.base import BaseLanguageExtractorTest

class TestPythonEnvVarExtraction(BaseLanguageExtractorTest):
    """Test Python environment variable extraction"""
    
    @property
    def language(self):
        return "python"
    
    @property
    def file_extensions(self):
        return [".py"]
    
    def get_test_cases(self):
        return [
            ExtractorTestCase(
                name="os.environ.get pattern",
                input_code='db_url = os.environ.get("DATABASE_URL")',
                expected_configs=[{
                    "name": "DATABASE_URL",
                    "type": "env_var",
                    "line_number": 1
                }],
                language="python",
                description="Standard os.environ.get pattern"
            ),
            ExtractorTestCase(
                name="os.environ bracket notation",
                input_code='api_key = os.environ["API_KEY"]',
                expected_configs=[{
                    "name": "API_KEY",
                    "type": "env_var",
                    "line_number": 1
                }],
                language="python",
                description="Bracket notation access"
            ),
            ExtractorTestCase(
                name="os.getenv pattern",
                input_code='debug = os.getenv("DEBUG", "false")',
                expected_configs=[{
                    "name": "DEBUG",
                    "type": "env_var",
                    "line_number": 1,
                    "default_value": "false"
                }],
                language="python",
                description="os.getenv with default"
            )
        ]
    
    def get_non_config_samples(self):
        return [
            'print("This is not a config")',
            'def get_environ(): pass',
            '# os.environ.get("COMMENTED_OUT")',
            'config_string = "os.environ.get(FAKE)"'
        ]
    
    def get_sensitive_test_cases(self):
        return [
            ExtractorTestCase(
                name="Password environment variable",
                input_code='pwd = os.environ.get("DB_PASSWORD")',
                expected_configs=[{
                    "name": "DB_PASSWORD",
                    "type": "env_var",
                    "is_sensitive": True
                }],
                language="python",
                description="Password should be marked sensitive"
            )
        ]

class TestJavaScriptEnvVarExtraction(BaseLanguageExtractorTest):
    """Test JavaScript environment variable extraction"""
    
    @property
    def language(self):
        return "javascript"
    
    def get_test_cases(self):
        return [
            ExtractorTestCase(
                name="process.env pattern",
                input_code='const apiUrl = process.env.API_URL;',
                expected_configs=[{
                    "name": "API_URL",
                    "type": "env_var"
                }],
                language="javascript",
                description="Node.js process.env pattern"
            ),
            ExtractorTestCase(
                name="import.meta.env pattern",
                input_code='const viteVar = import.meta.env.VITE_API_KEY;',
                expected_configs=[{
                    "name": "VITE_API_KEY",
                    "type": "env_var"
                }],
                language="javascript",
                description="Vite environment variable"
            )
        ]
```

### test_connection_string_extraction.py

```python
"""
GREEN Phase: Verify connection string extraction
"""

class TestConnectionStringExtraction:
    """Test extraction of database and service connection strings"""
    
    @pytest.mark.parametrize("connection_string,expected_type", [
        ("mongodb://localhost:27017/mydb", "connection_string"),
        ("postgresql://user:pass@localhost/db", "connection_string"),
        ("redis://localhost:6379", "connection_string"),
        ("amqp://guest:guest@localhost:5672/", "connection_string"),
        ("mysql://root:password@localhost:3306/database", "connection_string"),
    ])
    def test_url_based_connection_strings(self, connection_string, expected_type):
        """Test URL-based connection string detection"""
        extractor = ConfigurationExtractor()
        
        code = f'CONN = "{connection_string}"'
        result = extractor.extract_configs(code)
        
        assert len(result) == 1
        assert result[0].type == expected_type
        assert result[0].is_sensitive == True
    
    def test_sql_server_connection_string(self):
        """Test SQL Server style connection strings"""
        extractor = ConfigurationExtractor()
        
        conn_str = 'Data Source=server;Initial Catalog=db;User ID=user;Password=pass'
        code = f'connectionString = "{conn_str}"'
        
        result = extractor.extract_configs(code)
        
        assert len(result) == 1
        assert result[0].type == "connection_string"
        assert result[0].is_sensitive == True
```

## REFACTOR Phase Tests (Quality & Performance)

### test_extraction_performance.py

```python
"""
REFACTOR Phase: Performance and optimization tests
"""

import time
import tempfile
from pathlib import Path

class TestExtractionPerformance:
    """Test performance characteristics of config extraction"""
    
    def test_large_file_performance(self):
        """Extraction should handle large files efficiently"""
        extractor = ConfigurationExtractor()
        
        # Generate a large file with many configs
        large_code = "\n".join([
            f'VAR_{i} = os.environ.get("VAR_{i}")'
            for i in range(1000)
        ])
        
        start_time = time.time()
        result = extractor.extract_configs(large_code)
        elapsed = time.time() - start_time
        
        assert elapsed < 1.0, f"Extraction took {elapsed}s, should be < 1s"
        assert len(result) == 1000
    
    def test_memory_efficiency(self):
        """Test memory usage stays within bounds"""
        import psutil
        import os
        
        extractor = ConfigurationExtractor()
        process = psutil.Process(os.getpid())
        
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Process many files
        for i in range(100):
            code = f'CONFIG_{i} = os.environ.get("CONFIG_{i}")'
            extractor.extract_configs(code)
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        assert memory_increase < 50, f"Memory increased by {memory_increase}MB"
    
    @pytest.mark.timeout(5)
    def test_extraction_timeout(self):
        """Extraction should not hang on malformed input"""
        extractor = ConfigurationExtractor()
        
        # Potentially problematic patterns
        malformed_inputs = [
            "os.environ.get(" * 1000,  # Nested patterns
            "/*" * 10000,  # Comment bombs
            "\\" * 10000,  # Escape sequences
        ]
        
        for malformed in malformed_inputs:
            # Should complete without hanging
            result = extractor.extract_configs(malformed)
            assert result is not None
```

### test_edge_cases.py

```python
"""
REFACTOR Phase: Edge case and error handling tests
"""

class TestEdgeCases:
    """Test edge cases and error conditions"""
    
    def test_unicode_handling(self):
        """Test extraction with Unicode characters"""
        extractor = ConfigurationExtractor()
        
        unicode_code = '''
        # 配置文件 (Chinese: configuration file)
        数据库_URL = os.environ.get("DATABASE_URL")
        API_KEY = os.environ.get("API_キー")  # Japanese
        '''
        
        result = extractor.extract_configs(unicode_code)
        assert len(result) == 2
    
    def test_multiline_patterns(self):
        """Test extraction across multiple lines"""
        extractor = ConfigurationExtractor()
        
        multiline_code = '''
        config = {
            "database": os.environ.get(
                "DATABASE_URL",
                "postgresql://localhost/test"
            ),
            "api_key": os.environ.get(
                "API_KEY"
            )
        }
        '''
        
        result = extractor.extract_configs(multiline_code)
        assert len(result) == 2
        assert "DATABASE_URL" in [c.name for c in result]
        assert "API_KEY" in [c.name for c in result]
    
    def test_nested_quotes(self):
        """Test handling of nested quotes"""
        extractor = ConfigurationExtractor()
        
        nested_quotes = '''
        single = os.environ.get('SINGLE_QUOTE')
        double = os.environ.get("DOUBLE_QUOTE")
        mixed = os.environ.get("MIXED'QUOTE")
        escaped = os.environ.get("ESCAPED\\"QUOTE")
        '''
        
        result = extractor.extract_configs(nested_quotes)
        assert len(result) == 4
    
    def test_empty_and_none_handling(self):
        """Test handling of empty and None values"""
        extractor = ConfigurationExtractor()
        
        # Empty string
        assert extractor.extract_configs("") == []
        
        # None input
        assert extractor.extract_configs(None) == []
        
        # Whitespace only
        assert extractor.extract_configs("   \n\t  ") == []
```

## Integration Tests

### test_cli_integration.py

```python
"""
Integration tests for CLI commands with config extraction
"""

import subprocess
from pathlib import Path

class TestCLIIntegration:
    """Test config extraction through CLI interface"""
    
    def test_measure_command_with_configs(self, tmp_path):
        """Test ddd measure includes config coverage"""
        # Create test project with configs
        project = tmp_path / "test_project"
        project.mkdir()
        
        (project / "app.py").write_text('''
        import os
        DATABASE_URL = os.environ.get("DATABASE_URL")
        API_KEY = os.environ.get("API_KEY")
        ''')
        
        (project / "README.md").write_text('''
        # Configuration
        - DATABASE_URL: PostgreSQL connection string
        ''')
        
        # Run measure command
        result = subprocess.run(
            ["uv", "run", "ddd", "measure", str(project)],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert "Configuration" in result.stdout
        assert "50.0%" in result.stdout  # One of two configs documented
    
    def test_assert_coverage_with_configs(self, tmp_path):
        """Test assert-coverage fails on undocumented configs"""
        project = tmp_path / "test_project"
        project.mkdir()
        
        (project / "settings.py").write_text('''
        PASSWORD = os.environ.get("PASSWORD")  # Critical, undocumented
        ''')
        
        result = subprocess.run(
            ["uv", "run", "ddd", "assert-coverage", str(project)],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 1  # Should fail
        assert "Critical undocumented" in result.stdout
```

## Test Fixtures and Utilities

### conftest.py

```python
"""
Shared fixtures and utilities for config extractor tests
"""

import pytest
from pathlib import Path
import tempfile
from typing import Dict, List

@pytest.fixture
def sample_project(tmp_path):
    """Create a sample multi-language project structure"""
    project = tmp_path / "sample_project"
    project.mkdir()
    
    # Python files
    (project / "app.py").write_text('''
    import os
    DATABASE_URL = os.environ.get("DATABASE_URL")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    ''')
    
    # JavaScript files
    (project / "config.js").write_text('''
    module.exports = {
        apiUrl: process.env.API_URL,
        apiKey: process.env.API_KEY
    };
    ''')
    
    # .env file
    (project / ".env.example").write_text('''
    # Database configuration
    DATABASE_URL=postgresql://localhost/myapp
    # API configuration  
    API_URL=https://api.example.com
    API_KEY=your-api-key-here
    ''')
    
    # Documentation
    (project / "README.md").write_text('''
    # Configuration
    
    The following environment variables are required:
    - DATABASE_URL: PostgreSQL connection string
    - API_URL: External API endpoint
    ''')
    
    return project

@pytest.fixture
def config_factory():
    """Factory for creating test ConfigArtifact instances"""
    def _create_config(**kwargs):
        defaults = {
            "name": "TEST_CONFIG",
            "type": "env_var",
            "file_path": "test.py",
            "line_number": 1,
            "is_documented": False,
            "is_sensitive": False
        }
        defaults.update(kwargs)
        return ConfigArtifact(**defaults)
    
    return _create_config

@pytest.fixture
def mock_extractor(mocker):
    """Mock extractor for testing"""
    mock = mocker.Mock(spec=ConfigurationExtractor)
    mock.extract_configs.return_value = []
    return mock

class ConfigTestHelpers:
    """Helper methods for config testing"""
    
    @staticmethod
    def create_test_file(content: str, language: str = "python") -> Path:
        """Create a temporary test file with content"""
        ext_map = {
            "python": ".py",
            "javascript": ".js",
            "typescript": ".ts",
            "java": ".java"
        }
        
        with tempfile.NamedTemporaryFile(
            suffix=ext_map.get(language, ".txt"),
            mode="w",
            delete=False
        ) as f:
            f.write(content)
            return Path(f.name)
    
    @staticmethod
    def assert_config_equal(actual: ConfigArtifact, expected: Dict):
        """Assert a ConfigArtifact matches expected values"""
        for key, value in expected.items():
            assert getattr(actual, key) == value, \
                f"Config.{key} = {getattr(actual, key)}, expected {value}"
```

## Test Execution Strategy

### Phase 1: RED (Week 1, Days 1-2)
1. Write all contract tests that define expected behavior
2. All tests should FAIL initially
3. Focus on clear specifications, not implementation

### Phase 2: GREEN (Week 1, Days 3-4)
1. Implement minimal code to make tests pass
2. Don't worry about optimization
3. Focus on correctness

### Phase 3: REFACTOR (Week 1, Day 5)
1. Improve code quality while keeping tests green
2. Add performance optimizations
3. Enhance error handling

## Coverage Targets

| Module | Current | Target | Priority |
|--------|---------|--------|----------|
| ConfigurationExtractor | 13% | 80% | Critical |
| ConfigArtifact | 0% | 95% | High |
| ConfigCoverageResult | 0% | 95% | High |
| Edge Cases | 0% | 70% | Medium |
| Performance | 0% | 60% | Low |

## Success Metrics

1. **Coverage**: Achieve 80% overall coverage for config_extractors module
2. **Test Stability**: 100% pass rate after GREEN phase
3. **Performance**: All extraction <1s for files <10MB
4. **Security**: All sensitive data properly identified and redacted
5. **Documentation**: 100% of configs detected as documented/undocumented

## Risk Mitigation

1. **Pattern Complexity**: Use regex101.com for pattern validation
2. **Language Support**: Start with Python/JS, add others incrementally
3. **Performance**: Profile before optimizing
4. **False Positives**: Maintain negative test cases
5. **Integration**: Test with real projects early

This comprehensive test design addresses all identified gaps while maintaining TDD principles and creating a robust, maintainable test suite.