"""
Unit tests for DocumentationCoverage class
"""

from typing import Dict, List

import pytest

from ddd.coverage import CoverageResult, DocumentationCoverage
from ddd.specs import DAYLIGHTSpec, DimensionSpec


class TestCoverageResult:
    """Test CoverageResult dataclass"""

    def test_coverage_result_creation(self):
        """Test creating a CoverageResult instance"""
        result = CoverageResult(
            overall_coverage=0.85,
            passed=True,
            dimension_scores={"dependencies": 0.9, "automation": 0.8},
            missing_elements={"dependencies": ["lock_file"]},
            recommendations=["Add lock file documentation"],
        )

        assert result.overall_coverage == 0.85
        assert result.passed is True
        assert result.dimension_scores["dependencies"] == 0.9
        assert "lock_file" in result.missing_elements["dependencies"]
        assert len(result.recommendations) == 1

    def test_coverage_result_string_representation(self):
        """Test string representation of CoverageResult"""
        result_passed = CoverageResult(
            overall_coverage=0.9,
            passed=True,
            dimension_scores={},
            missing_elements={},
            recommendations=[],
        )
        assert "✅ PASSED" in str(result_passed)
        assert "90.0%" in str(result_passed)

        result_failed = CoverageResult(
            overall_coverage=0.5,
            passed=False,
            dimension_scores={},
            missing_elements={},
            recommendations=[],
        )
        assert "❌ FAILED" in str(result_failed)
        assert "50.0%" in str(result_failed)


class TestDocumentationCoverage:
    """Test DocumentationCoverage class"""

    @pytest.fixture
    def coverage_calculator(self):
        """Create a DocumentationCoverage instance"""
        return DocumentationCoverage()

    @pytest.fixture
    def sample_extracted_docs(self):
        """Sample extracted documentation data"""
        return {
            "dependencies": {
                "runtime_dependencies": {
                    "pytest": {
                        "name": "pytest",
                        "version": ">=7.0",
                        "purpose": "Testing framework",
                        "failure_impact": "Tests cannot run",
                    }
                },
                "node_version": None,
                "package_manager": "pip",
                "lock_file": "requirements.txt",
            }
        }

    @pytest.fixture
    def empty_extracted_docs(self):
        """Empty extracted documentation"""
        return {"dependencies": {}}

    def test_measure_with_good_coverage(self, coverage_calculator, sample_extracted_docs):
        """Test measuring documentation with good coverage"""
        result = coverage_calculator.measure(sample_extracted_docs)

        assert isinstance(result, CoverageResult)
        assert result.overall_coverage > 0
        assert "dependencies" in result.dimension_scores

    def test_measure_with_no_documentation(self, coverage_calculator, empty_extracted_docs):
        """Test measuring with no documentation"""
        result = coverage_calculator.measure(empty_extracted_docs)

        assert result.overall_coverage == 0
        assert result.passed is False
        assert len(result.missing_elements) > 0
        assert len(result.recommendations) > 0

    def test_element_coverage_calculation(self, coverage_calculator):
        """Test element coverage calculation"""
        spec = DimensionSpec(
            name="test",
            required_elements=["elem1", "elem2", "elem3"],
            required_fields={},
            minimum_coverage=0.8,
        )

        # All elements present
        data_full = {"elem1": "value1", "elem2": "value2", "elem3": "value3"}
        coverage = coverage_calculator._calculate_element_coverage(spec, data_full)
        assert coverage == 1.0

        # Partial elements
        data_partial = {"elem1": "value1", "elem2": "value2"}
        coverage = coverage_calculator._calculate_element_coverage(spec, data_partial)
        assert coverage == pytest.approx(2 / 3)

        # No elements
        coverage = coverage_calculator._calculate_element_coverage(spec, {})
        assert coverage == 0.0

    def test_completeness_coverage_calculation(self, coverage_calculator):
        """Test completeness coverage calculation"""
        spec = DimensionSpec(
            name="test",
            required_elements=[],
            required_fields={"dependency": ["name", "version", "purpose"]},
            minimum_coverage=0.8,
        )

        # Full fields
        data_full = {"dependencies": [{"name": "pytest", "version": "7.0", "purpose": "testing"}]}
        coverage = coverage_calculator._calculate_completeness_coverage(spec, data_full)
        assert coverage == 1.0

        # Missing fields
        data_partial = {
            "dependencies": [
                {
                    "name": "pytest",
                    "version": "7.0",
                    # missing 'purpose'
                }
            ]
        }
        coverage = coverage_calculator._calculate_completeness_coverage(spec, data_partial)
        assert coverage == pytest.approx(2 / 3)

    def test_usefulness_coverage_calculation(self, coverage_calculator):
        """Test usefulness coverage calculation"""
        spec = DimensionSpec(
            name="dependencies", required_elements=[], required_fields={}, minimum_coverage=0.8
        )

        # Has usefulness indicators
        data_with_indicators = {
            "failure_impact": "Service will not start",
            "recovery_procedure": "Reinstall dependencies",
        }
        coverage = coverage_calculator._calculate_usefulness_coverage(spec, data_with_indicators)
        assert coverage == 1.0

        # Missing indicators
        data_without = {"some_field": "value"}
        coverage = coverage_calculator._calculate_usefulness_coverage(spec, data_without)
        assert coverage == 0.0

    def test_has_indicator(self, coverage_calculator):
        """Test indicator detection in nested structures"""
        # Direct indicator
        data = {"failure_impact": "test"}
        assert coverage_calculator._has_indicator(data, "failure_impact") is True

        # Nested in dict
        data = {"dependency": {"failure_impact": "test"}}
        assert coverage_calculator._has_indicator(data, "failure_impact") is True

        # Nested in list
        data = {"deps": [{"failure_impact": "test"}]}
        assert coverage_calculator._has_indicator(data, "failure_impact") is True

        # Not present
        data = {"other": "value"}
        assert coverage_calculator._has_indicator(data, "failure_impact") is False

    def test_assert_coverage_passing(self, coverage_calculator):
        """Test assert_coverage when passing"""
        extracted = {
            "dependencies": {
                "runtime_dependencies": {
                    "pkg": {
                        "name": "pkg",
                        "version": "1.0",
                        "purpose": "test",
                        "failure_impact": "fail",
                    }
                },
                "node_version": "18",
                "package_manager": "npm",
                "lock_file": "package-lock.json",
            }
        }

        # Should not raise when coverage is high
        coverage_calculator.assert_coverage(extracted, minimum=0.5)

    def test_assert_coverage_failing(self, coverage_calculator, empty_extracted_docs):
        """Test assert_coverage when failing"""
        with pytest.raises(AssertionError) as exc_info:
            coverage_calculator.assert_coverage(empty_extracted_docs, minimum=0.85)

        assert "below minimum" in str(exc_info.value)

    def test_dimension_weights(self, coverage_calculator):
        """Test that dimension weights are applied correctly"""
        spec = coverage_calculator.spec

        # Check that weights sum to 1.0 (or close to it)
        total_weight = sum(dim.weight for dim in spec.dimensions.values())
        assert total_weight == pytest.approx(1.0, rel=0.01)

        # Check specific dimension weights
        assert spec.dimensions["dependencies"].weight == 0.15
        assert spec.dimensions["automation"].weight == 0.12
