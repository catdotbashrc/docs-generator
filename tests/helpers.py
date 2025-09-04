"""
Test helper utilities for DDD test suite.
Provides additional utilities beyond fixtures for test organization.
"""

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import yaml


class ModuleParser:
    """Parse and analyze Ansible modules for testing."""
    
    @staticmethod
    def extract_yaml_block(content: str, block_name: str) -> Optional[Dict]:
        """Extract and parse a YAML documentation block from module content."""
        pattern = rf'{block_name}\s*=\s*["\']{{3}}(.*?)["\']{{3}}'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            try:
                return yaml.safe_load(match.group(1))
            except yaml.YAMLError:
                return None
        return None
    
    @staticmethod
    def extract_boto3_calls(content: str) -> List[Tuple[str, str]]:
        """Extract boto3 service and method calls from module content."""
        calls = []
        
        # Pattern for client creation
        client_pattern = r'(\w+)\s*=\s*boto3\.client\(["\'](\w+)["\']\)'
        clients = {}
        for match in re.finditer(client_pattern, content):
            var_name, service = match.groups()
            clients[var_name] = service
        
        # Pattern for method calls
        method_pattern = r'(\w+)\.(\w+)\('
        for match in re.finditer(method_pattern, content):
            var_name, method = match.groups()
            if var_name in clients:
                calls.append((clients[var_name], method))
        
        return calls
    
    @staticmethod
    def extract_fail_json_calls(content: str) -> List[Dict[str, str]]:
        """Extract module.fail_json() error messages."""
        errors = []
        pattern = r'module\.fail_json\(msg\s*=\s*["\']([^"\']+)["\']\)'
        
        for match in re.finditer(pattern, content):
            errors.append({
                'message': match.group(1),
                'type': 'explicit_error'
            })
        
        return errors


class CoverageAnalyzer:
    """Analyze and report on coverage metrics."""
    
    @staticmethod
    def calculate_dimension_coverage(
        dimension_data: Dict[str, Any],
        required_elements: List[str]
    ) -> float:
        """Calculate coverage for a specific dimension."""
        if not required_elements:
            return 1.0 if dimension_data else 0.0
        
        found = sum(1 for elem in required_elements if elem in dimension_data)
        return found / len(required_elements)
    
    @staticmethod
    def generate_coverage_report(
        coverage_scores: Dict[str, float],
        threshold: float = 0.85
    ) -> Dict[str, Any]:
        """Generate detailed coverage report."""
        total_score = sum(coverage_scores.values()) / len(coverage_scores)
        passing_dimensions = {
            dim: score for dim, score in coverage_scores.items()
            if score >= threshold
        }
        failing_dimensions = {
            dim: score for dim, score in coverage_scores.items()
            if score < threshold
        }
        
        return {
            'overall_score': total_score,
            'passing': passing_dimensions,
            'failing': failing_dimensions,
            'meets_threshold': total_score >= threshold
        }


class TestFileManager:
    """Manage test file operations and organization."""
    
    @staticmethod
    def create_test_structure(base_path: Path) -> Dict[str, Path]:
        """Create standard test directory structure."""
        directories = {
            'red_phase': base_path / 'red_phase',
            'green_phase': base_path / 'green_phase',
            'refactor_phase': base_path / 'refactor_phase',
            'fixtures': base_path / 'fixtures',
            'fixtures_modules': base_path / 'fixtures' / 'modules',
            'fixtures_malformed': base_path / 'fixtures' / 'malformed',
            'fixtures_golden': base_path / 'fixtures' / 'golden',
            'benchmarks': base_path / 'benchmarks'
        }
        
        for dir_path in directories.values():
            dir_path.mkdir(parents=True, exist_ok=True)
        
        return directories
    
    @staticmethod
    def organize_existing_tests(base_path: Path) -> Dict[str, List[str]]:
        """Analyze and categorize existing test files."""
        test_files = list(base_path.glob('test_*.py'))
        
        categorized = {
            'unit': [],
            'integration': [],
            'performance': [],
            'red_phase': [],
            'green_phase': [],
            'refactor_phase': []
        }
        
        for test_file in test_files:
            content = test_file.read_text()
            
            # Categorize based on content patterns
            if 'test_extract' in content or 'test_parse' in content:
                categorized['red_phase'].append(test_file.name)
            elif 'test_integration' in content or 'test_real' in content:
                categorized['integration'].append(test_file.name)
            elif 'test_performance' in content or 'time.time()' in content:
                categorized['performance'].append(test_file.name)
            elif 'test_validate' in content or 'test_assert' in content:
                categorized['green_phase'].append(test_file.name)
            else:
                categorized['unit'].append(test_file.name)
        
        return categorized


class MockDataFactory:
    """Factory for creating mock data for various test scenarios."""
    
    @staticmethod
    def create_coverage_result(
        overall: float = 0.85,
        dimensions: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """Create mock coverage result data."""
        default_dimensions = {
            'dependencies': 0.9,
            'automation': 0.8,
            'yearbook': 0.85,
            'lifecycle': 0.75,
            'integration': 0.9,
            'governance': 0.8,
            'health': 0.85,
            'testing': 0.9
        }
        
        return {
            'overall_coverage': overall,
            'dimension_scores': dimensions or default_dimensions,
            'passed': overall >= 0.85,
            'missing_elements': []
        }
    
    @staticmethod
    def create_extraction_result(
        module_name: str = "test_module"
    ) -> Dict[str, Any]:
        """Create mock extraction result."""
        return {
            'module': module_name,
            'parameters': {
                'path': {
                    'type': 'path',
                    'required': True,
                    'description': 'Path to file'
                },
                'state': {
                    'type': 'str',
                    'choices': ['present', 'absent'],
                    'default': 'present'
                }
            },
            'permissions': [
                'ec2:DescribeInstances',
                'ec2:TerminateInstances'
            ],
            'error_patterns': [
                {
                    'message': 'File not found',
                    'recovery': 'Check file path'
                }
            ],
            'states': ['present', 'absent'],
            'check_mode': True
        }


class PerformanceValidator:
    """Validate performance requirements for MVP."""
    
    EXTRACTION_TIME_LIMIT = 5.0  # seconds
    MEMORY_LIMIT_MB = 500  # megabytes
    BATCH_TIME_PER_MODULE = 3.0  # seconds
    
    @classmethod
    def validate_extraction_time(cls, elapsed_time: float) -> bool:
        """Validate that extraction completed within time limit."""
        return elapsed_time < cls.EXTRACTION_TIME_LIMIT
    
    @classmethod
    def validate_memory_usage(cls, memory_mb: float) -> bool:
        """Validate that memory usage is within limits."""
        return memory_mb < cls.MEMORY_LIMIT_MB
    
    @classmethod
    def validate_batch_performance(
        cls,
        module_count: int,
        elapsed_time: float
    ) -> bool:
        """Validate batch extraction performance."""
        time_limit = module_count * cls.BATCH_TIME_PER_MODULE
        return elapsed_time < time_limit


class TestReporter:
    """Generate test reports and summaries."""
    
    @staticmethod
    def generate_test_summary(
        passed: int,
        failed: int,
        skipped: int = 0
    ) -> str:
        """Generate formatted test summary."""
        total = passed + failed + skipped
        pass_rate = (passed / total * 100) if total > 0 else 0
        
        return f"""
        Test Summary
        ============
        Total Tests: {total}
        Passed: {passed} ({pass_rate:.1f}%)
        Failed: {failed}
        Skipped: {skipped}
        
        Status: {'✅ PASS' if failed == 0 else '❌ FAIL'}
        """
    
    @staticmethod
    def generate_coverage_summary(
        coverage_data: Dict[str, float]
    ) -> str:
        """Generate coverage summary report."""
        lines = ["Coverage Summary", "================"]
        
        for dimension, score in coverage_data.items():
            status = "✅" if score >= 0.85 else "❌"
            lines.append(f"{dimension}: {score:.1%} {status}")
        
        overall = sum(coverage_data.values()) / len(coverage_data)
        lines.append(f"\nOverall: {overall:.1%}")
        
        return "\n".join(lines)


class ValidationHelpers:
    """Additional validation utilities."""
    
    @staticmethod
    def validate_module_structure(module_content: str) -> List[str]:
        """Validate that an Ansible module has required structure."""
        errors = []
        
        if 'DOCUMENTATION' not in module_content:
            errors.append("Missing DOCUMENTATION block")
        if 'EXAMPLES' not in module_content:
            errors.append("Missing EXAMPLES block")
        if 'RETURN' not in module_content:
            errors.append("Missing RETURN block")
        if 'AnsibleModule' not in module_content:
            errors.append("Missing AnsibleModule import")
        if 'def main():' not in module_content:
            errors.append("Missing main() function")
        
        return errors
    
    @staticmethod
    def validate_extraction_completeness(
        extracted_data: Dict[str, Any]
    ) -> List[str]:
        """Validate that extraction captured required information."""
        missing = []
        
        required_fields = [
            'module', 'parameters', 'permissions', 
            'error_patterns', 'states'
        ]
        
        for field in required_fields:
            if field not in extracted_data or not extracted_data[field]:
                missing.append(field)
        
        return missing


# Export commonly used items
__all__ = [
    'ModuleParser',
    'CoverageAnalyzer',
    'TestFileManager',
    'MockDataFactory',
    'PerformanceValidator',
    'TestReporter',
    'ValidationHelpers'
]