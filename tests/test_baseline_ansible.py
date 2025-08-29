"""
Test DDD framework against Ansible baseline
Ansible is our gold standard with ~90% DAYLIGHT coverage
"""

import sys
from pathlib import Path

import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ddd import DependencyExtractor, DocumentationCoverage


class TestAnsibleBaseline:
    """Test that our extractors work on Ansible (known good documentation)"""

    @pytest.fixture
    def ansible_path(self):
        """Path to Ansible baseline"""
        return Path(__file__).parent.parent / "baseline" / "ansible"

    def test_ansible_has_dependencies(self, ansible_path):
        """Ansible should have well-documented dependencies"""
        extractor = DependencyExtractor()
        deps = extractor.extract(str(ansible_path))

        # Ansible uses requirements.txt
        assert deps["runtime_dependencies"], "Should find Python dependencies"
        assert "jinja2" in deps["runtime_dependencies"], "Should find Jinja2 dependency"
        assert "PyYAML" in deps["runtime_dependencies"], "Should find PyYAML dependency"

    def test_ansible_dependency_coverage(self, ansible_path):
        """Ansible should have high dependency coverage"""
        extractor = DependencyExtractor()
        extracted = {"dependencies": extractor.extract(str(ansible_path))}

        coverage = DocumentationCoverage()
        result = coverage.measure(extracted)

        # Ansible should have good dependency documentation
        assert (
            result.dimension_scores.get("dependencies", 0) > 0.5
        ), f"Ansible dependency coverage too low: {result.dimension_scores.get('dependencies', 0):.1%}"

    def test_coverage_measurement_works(self):
        """Test that coverage measurement produces expected results"""
        # Perfect documentation
        perfect_docs = {
            "dependencies": {
                "runtime_dependencies": {
                    "express": {
                        "name": "express",
                        "version": "4.18.0",
                        "purpose": "Web server",
                        "failure_impact": "Service won't start",
                    }
                },
                "node_version": "18.0.0",
                "package_manager": "npm",
                "lock_file": "package-lock.json",
            }
        }

        coverage = DocumentationCoverage()
        result = coverage.measure(perfect_docs)

        assert result.dimension_scores["dependencies"] > 0.8, "Perfect docs should have high score"

        # Missing documentation
        missing_docs = {"dependencies": {}}

        result = coverage.measure(missing_docs)
        assert result.dimension_scores["dependencies"] < 0.2, "Missing docs should have low score"
        assert not result.passed, "Missing docs should fail"
        assert result.recommendations, "Should provide recommendations"
