"""
Abstract base test classes for configuration extractor testing.

Provides reusable test patterns and abstractions for testing configuration
extraction across multiple languages and patterns.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pytest


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
            # For project path extraction, create temp file
            if hasattr(extractor, 'extract_configs') and callable(getattr(extractor, 'extract_configs')):
                # Check if method expects a path or string
                import inspect
                sig = inspect.signature(extractor.extract_configs)
                params = list(sig.parameters.keys())
                
                if params and 'project_path' in params[0].lower():
                    # Method expects a path - create temp project
                    import tempfile
                    with tempfile.TemporaryDirectory() as tmpdir:
                        test_file = Path(tmpdir) / f"test.{test_case.language}"
                        test_file.write_text(test_case.input_code)
                        result = extractor.extract_configs(tmpdir)
                else:
                    # Method expects code string
                    result = extractor.extract_configs(test_case.input_code)
            else:
                # Fallback for different method names
                result = []
            
            assert len(result) == len(test_case.expected_configs), \
                f"Expected {len(test_case.expected_configs)} configs, got {len(result)}"
            
            for expected in test_case.expected_configs:
                assert self._config_exists(result, expected), \
                    f"Expected config not found: {expected}"
    
    def test_no_false_positives(self):
        """Test that non-config patterns are not extracted"""
        extractor = self.get_extractor()
        non_config_code = self.get_non_config_samples()
        
        for sample in non_config_code:
            # Handle both path and string based extraction
            if hasattr(extractor, 'extract_configs'):
                import inspect
                sig = inspect.signature(extractor.extract_configs)
                params = list(sig.parameters.keys())
                
                if params and 'project_path' in params[0].lower():
                    import tempfile
                    with tempfile.TemporaryDirectory() as tmpdir:
                        test_file = Path(tmpdir) / "test.py"
                        test_file.write_text(sample)
                        result = extractor.extract_configs(tmpdir)
                else:
                    result = extractor.extract_configs(sample)
            else:
                result = []
            
            assert len(result) == 0, f"False positive in: {sample}"
    
    def test_sensitive_data_detection(self):
        """Test that sensitive configs are properly flagged"""
        extractor = self.get_extractor()
        sensitive_cases = self.get_sensitive_test_cases()
        
        for case in sensitive_cases:
            # Handle both path and string based extraction
            if hasattr(extractor, 'extract_configs'):
                import inspect
                sig = inspect.signature(extractor.extract_configs)
                params = list(sig.parameters.keys())
                
                if params and 'project_path' in params[0].lower():
                    import tempfile
                    with tempfile.TemporaryDirectory() as tmpdir:
                        test_file = Path(tmpdir) / f"test.{case.language}"
                        test_file.write_text(case.input_code)
                        result = extractor.extract_configs(tmpdir)
                else:
                    result = extractor.extract_configs(case.input_code)
            else:
                result = []
            
            sensitive_configs = [c for c in result if c.get('is_sensitive', False)]
            assert len(sensitive_configs) > 0, \
                f"No sensitive configs detected in: {case.name}"
    
    def _config_exists(self, configs: List, expected: Dict) -> bool:
        """Check if a config matching expected values exists in the list"""
        for config in configs:
            match = True
            for key, value in expected.items():
                config_value = config.get(key) if isinstance(config, dict) else getattr(config, key, None)
                if config_value != value:
                    match = False
                    break
            if match:
                return True
        return False
    
    @abstractmethod
    def get_non_config_samples(self) -> List[str]:
        """Return code samples that should NOT trigger extraction"""
        pass
    
    @abstractmethod
    def get_sensitive_test_cases(self) -> List[ExtractorTestCase]:
        """Return test cases with sensitive data"""
        pass


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
        
        if not hasattr(extractor, 'extract_from_code'):
            pytest.skip("Extractor doesn't support extract_from_code method")
        
        for pattern_code, expected_type in patterns:
            result = extractor.extract_from_code(
                pattern_code, 
                language=self.language
            )
            
            # Check if any result has the expected type
            found = False
            for item in result:
                if hasattr(item, 'type') and item.type == expected_type:
                    found = True
                    break
            
            assert found, f"Expected type {expected_type} not found in results"
    
    @abstractmethod
    def get_language_patterns(self) -> List[Tuple[str, str]]:
        """Return language-specific pattern test cases"""
        pass