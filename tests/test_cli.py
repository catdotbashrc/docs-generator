"""
Unit tests for CLI commands
"""

import pytest
import json
import tempfile
from pathlib import Path
from click.testing import CliRunner
from unittest.mock import patch, MagicMock
from cli import cli, measure, assert_coverage, demo, measure_artifacts
from ddd.coverage import CoverageResult


class TestCLICommands:
    """Test CLI commands"""
    
    @pytest.fixture
    def runner(self):
        """Create a CLI test runner"""
        return CliRunner()
    
    @pytest.fixture
    def temp_project(self):
        """Create a temporary project directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            
            # Create a sample package.json
            package_json = {
                "name": "test-project",
                "dependencies": {
                    "express": "^4.18.0"
                }
            }
            
            with open(project_path / "package.json", 'w') as f:
                json.dump(package_json, f)
            
            yield project_path
    
    def test_cli_help(self, runner):
        """Test CLI help command"""
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert "Documentation Driven Development" in result.output
        assert "measure" in result.output
        assert "assert-coverage" in result.output
        assert "demo" in result.output
    
    def test_measure_command(self, runner, temp_project):
        """Test measure command"""
        result = runner.invoke(measure, [str(temp_project)])
        
        # Check output contains expected elements
        assert "Measuring documentation coverage" in result.output
        assert "Coverage by Dimension" in result.output
        
        # Should show dependencies dimension
        assert "Dependencies" in result.output or "dependencies" in result.output
    
    def test_measure_with_output_file(self, runner, temp_project):
        """Test measure command with output file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            output_file = f.name
        
        try:
            result = runner.invoke(measure, [
                str(temp_project),
                '--output', output_file
            ])
            
            # Check file was created
            assert Path(output_file).exists()
            
            # Check JSON content
            with open(output_file) as f:
                data = json.load(f)
            
            assert 'overall_coverage' in data
            assert 'passed' in data
            assert 'dimension_scores' in data
            assert 'missing_elements' in data
            assert 'recommendations' in data
            
        finally:
            Path(output_file).unlink(missing_ok=True)
    
    def test_measure_verbose(self, runner, temp_project):
        """Test measure command with verbose flag"""
        result = runner.invoke(measure, [
            str(temp_project),
            '--verbose'
        ])
        
        assert result.exit_code in [0, 1]  # May pass or fail depending on coverage
        assert "Measuring documentation coverage" in result.output
    
    @patch('cli.DocumentationCoverage')
    def test_assert_coverage_passing(self, mock_coverage_class, runner, temp_project):
        """Test assert-coverage command when passing"""
        # Mock the coverage to pass
        mock_coverage = MagicMock()
        mock_coverage.assert_coverage.return_value = None  # No exception
        mock_coverage_class.return_value = mock_coverage
        
        result = runner.invoke(assert_coverage, [
            str(temp_project),
            '--min-coverage', '0.5'
        ])
        
        assert result.exit_code == 0
        assert "Coverage assertion passed" in result.output
    
    @patch('cli.DocumentationCoverage')
    def test_assert_coverage_failing(self, mock_coverage_class, runner, temp_project):
        """Test assert-coverage command when failing"""
        # Mock the coverage to fail
        mock_coverage = MagicMock()
        mock_coverage.assert_coverage.side_effect = AssertionError(
            "Documentation coverage 0.4 below minimum 0.85"
        )
        mock_coverage_class.return_value = mock_coverage
        
        result = runner.invoke(assert_coverage, [str(temp_project)])
        
        assert result.exit_code == 1
        assert "Coverage assertion failed" in result.output
        assert "below minimum" in result.output
    
    def test_assert_coverage_custom_threshold(self, runner, temp_project):
        """Test assert-coverage with custom threshold"""
        result = runner.invoke(assert_coverage, [
            str(temp_project),
            '--min-coverage', '0.95'
        ])
        
        # Should likely fail with high threshold
        assert result.exit_code in [0, 1]
        assert "Asserting documentation coverage >= 95%" in result.output
    
    @patch('cli.DependencyExtractor')
    @patch('cli.DocumentationCoverage')
    def test_demo_command(self, mock_coverage_class, mock_extractor_class, runner, temp_project):
        """Test demo command"""
        # Mock extractor
        mock_extractor = MagicMock()
        mock_extractor.extract.return_value = {
            'runtime_dependencies': {'express': {'name': 'express'}},
            'package_manager': 'npm'
        }
        mock_extractor_class.return_value = mock_extractor
        
        # Mock coverage
        mock_coverage = MagicMock()
        mock_coverage.measure.return_value = CoverageResult(
            overall_coverage=0.75,
            passed=False,
            dimension_scores={'dependencies': 0.75},
            missing_elements={},
            recommendations=[]
        )
        mock_coverage_class.return_value = mock_coverage
        
        result = runner.invoke(demo, [str(temp_project)])
        
        assert result.exit_code == 0
        assert "Documentation Driven Development Demo" in result.output
        assert "RED Phase" in result.output
        assert "GREEN Phase" in result.output
        assert "REFACTOR Phase" in result.output
        assert "Initial coverage:" in result.output
        assert "Extracted coverage:" in result.output
        assert "Final Coverage:" in result.output
    
    def test_measure_artifacts_command(self, runner, temp_project):
        """Test measure-artifacts command"""
        # Create a Python file in the project
        py_file = temp_project / "module.py"
        py_file.write_text('''
def documented():
    """Has docs"""
    pass

def undocumented():
    pass
''')
        
        result = runner.invoke(measure_artifacts, [str(temp_project)])
        
        # Check output
        assert "Artifact-Based Documentation Coverage" in result.output
        assert "Coverage by Artifact Type" in result.output
        
        # Should show function coverage
        assert "Function" in result.output or "function" in result.output
    
    def test_measure_artifacts_with_output(self, runner, temp_project):
        """Test measure-artifacts with output file"""
        # Create a simple Python file
        (temp_project / "test.py").write_text('def func(): pass')
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            output_file = f.name
        
        try:
            result = runner.invoke(measure_artifacts, [
                str(temp_project),
                '--output', output_file
            ])
            
            # Check file was created
            assert Path(output_file).exists()
            
            # Check JSON content
            with open(output_file) as f:
                data = json.load(f)
            
            assert 'coverage_percentage' in data
            assert 'total_artifacts' in data
            assert 'documented_artifacts' in data
            assert 'passed' in data
            assert 'artifacts_by_type' in data
            
        finally:
            Path(output_file).unlink(missing_ok=True)
    
    def test_measure_artifacts_custom_threshold(self, runner, temp_project):
        """Test measure-artifacts with custom minimum coverage"""
        # Create undocumented Python file
        (temp_project / "undoc.py").write_text('''
def func1(): pass
def func2(): pass
def func3(): pass
''')
        
        result = runner.invoke(measure_artifacts, [
            str(temp_project),
            '--min-coverage', '90'
        ])
        
        # Should fail with high threshold and no docs
        assert result.exit_code == 1
        assert "FAILED" in result.output
        assert "minimum: 90" in result.output
    
    def test_invalid_project_path(self, runner):
        """Test with invalid project path"""
        result = runner.invoke(measure, ['/nonexistent/path'])
        
        assert result.exit_code != 0
        assert "does not exist" in result.output or "Error" in result.output