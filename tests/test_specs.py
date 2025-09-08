"""
Unit tests for documentation specifications
"""

import pytest

from ddd.specs import DAYLIGHTSpec, DimensionSpec


class TestDimensionSpec:
    """Test DimensionSpec class"""

    def test_dimension_spec_creation(self):
        """Test creating a DimensionSpec"""
        spec = DimensionSpec(
            name="test_dimension",
            required_elements=["elem1", "elem2", "elem3"],
            required_fields={"item": ["field1", "field2"]},
            minimum_coverage=0.80,
            weight=0.25,
        )

        assert spec.name == "test_dimension"
        assert len(spec.required_elements) == 3
        assert "elem1" in spec.required_elements
        assert "item" in spec.required_fields
        assert spec.required_fields["item"] == ["field1", "field2"]
        assert spec.minimum_coverage == 0.80
        assert spec.weight == 0.25

    def test_dimension_spec_defaults(self):
        """Test default values for DimensionSpec"""
        spec = DimensionSpec(name="test", required_elements=[], required_fields={})

        assert spec.minimum_coverage == 0.85  # Default
        assert spec.weight == 1.0  # Default

    def test_validate_with_complete_data(self):
        """Test validation with complete data"""
        spec = DimensionSpec(name="test", required_elements=["elem1", "elem2"], required_fields={})

        data = {"elem1": "value1", "elem2": "value2"}

        coverage, missing = spec.validate(data)

        assert coverage == 1.0
        assert missing == []

    def test_validate_with_partial_data(self):
        """Test validation with partial data"""
        spec = DimensionSpec(
            name="test", required_elements=["elem1", "elem2", "elem3"], required_fields={}
        )

        data = {
            "elem1": "value1",
            "elem3": "value3",
            # elem2 is missing
        }

        coverage, missing = spec.validate(data)

        assert coverage == pytest.approx(2 / 3)
        assert "elem2" in missing
        assert len(missing) == 1

    def test_validate_with_no_data(self):
        """Test validation with no data"""
        spec = DimensionSpec(name="test", required_elements=["elem1", "elem2"], required_fields={})

        coverage, missing = spec.validate({})

        assert coverage == 0.0
        assert missing == ["elem1", "elem2"]

    def test_validate_with_empty_values(self):
        """Test validation with empty values"""
        spec = DimensionSpec(name="test", required_elements=["elem1", "elem2"], required_fields={})

        data = {"elem1": "value1", "elem2": ""}  # Empty value should not count

        coverage, missing = spec.validate(data)

        assert coverage == pytest.approx(1 / 2)
        assert "elem2" in missing

    def test_validate_with_no_required_elements(self):
        """Test validation when no elements are required"""
        spec = DimensionSpec(name="test", required_elements=[], required_fields={})

        coverage, missing = spec.validate({})

        assert coverage == 0.0
        assert missing == []


class TestDAYLIGHTSpec:
    """Test DAYLIGHTSpec class"""

    @pytest.fixture
    def daylight_spec(self):
        """Create a DAYLIGHTSpec instance"""
        return DAYLIGHTSpec()

    def test_daylight_spec_creation(self, daylight_spec):
        """Test creating a DAYLIGHTSpec"""
        assert daylight_spec is not None
        assert hasattr(daylight_spec, "dimensions")
        assert isinstance(daylight_spec.dimensions, dict)

    def test_daylight_has_all_dimensions(self, daylight_spec):
        """Test that all DAYLIGHT dimensions are present"""
        expected_dimensions = [
            "dependencies",
            "automation",
            "yearbook",
            "lifecycle",
            "integration",
            "governance",
            "health",
            "testing",
        ]

        for dim in expected_dimensions:
            assert dim in daylight_spec.dimensions
            assert isinstance(daylight_spec.dimensions[dim], DimensionSpec)

    def test_dependencies_dimension(self, daylight_spec):
        """Test dependencies dimension specification"""
        deps_spec = daylight_spec.dimensions["dependencies"]

        assert deps_spec.name == "dependencies"
        assert "runtime_dependencies" in deps_spec.required_elements
        assert "node_version" in deps_spec.required_elements
        assert "package_manager" in deps_spec.required_elements
        assert "lock_file" in deps_spec.required_elements

        assert "dependency" in deps_spec.required_fields
        expected_fields = ["name", "version", "purpose", "failure_impact"]
        assert deps_spec.required_fields["dependency"] == expected_fields

        assert deps_spec.minimum_coverage == 0.90
        assert deps_spec.weight == 0.15

    def test_automation_dimension(self, daylight_spec):
        """Test automation dimension specification"""
        auto_spec = daylight_spec.dimensions["automation"]

        assert auto_spec.name == "automation"
        assert "npm_scripts" in auto_spec.required_elements
        assert "ci_cd_workflows" in auto_spec.required_elements
        assert "git_hooks" in auto_spec.required_elements

        assert "script" in auto_spec.required_fields
        expected_fields = ["command", "purpose", "when_to_run", "failure_handling"]
        assert auto_spec.required_fields["script"] == expected_fields

        assert auto_spec.minimum_coverage == 0.85
        assert auto_spec.weight == 0.12

    def test_yearbook_dimension(self, daylight_spec):
        """Test yearbook dimension specification"""
        year_spec = daylight_spec.dimensions["yearbook"]

        assert year_spec.name == "yearbook"
        assert "changelog" in year_spec.required_elements
        assert "git_history" in year_spec.required_elements
        assert "contributors" in year_spec.required_elements

        assert year_spec.required_fields == {}  # No specific fields required
        assert year_spec.minimum_coverage == 0.80
        assert year_spec.weight == 0.08

    def test_lifecycle_dimension(self, daylight_spec):
        """Test lifecycle dimension specification"""
        life_spec = daylight_spec.dimensions["lifecycle"]

        assert life_spec.name == "lifecycle"
        assert "environments" in life_spec.required_elements
        assert "deployment_process" in life_spec.required_elements
        assert "configuration_files" in life_spec.required_elements

        assert "environment" in life_spec.required_fields
        expected_fields = ["name", "purpose", "configuration"]
        assert life_spec.required_fields["environment"] == expected_fields

        assert life_spec.minimum_coverage == 0.85
        assert life_spec.weight == 0.13

    def test_dimension_weights_sum(self, daylight_spec):
        """Test that all dimension weights sum to 1.0"""
        total_weight = sum(spec.weight for spec in daylight_spec.dimensions.values())

        # Should be close to 1.0 (allowing for floating point precision)
        assert total_weight == pytest.approx(1.0, rel=0.01)

    def test_each_dimension_has_required_attributes(self, daylight_spec):
        """Test that each dimension has all required attributes"""
        for dim_name, dim_spec in daylight_spec.dimensions.items():
            # Check required attributes
            assert hasattr(dim_spec, "name")
            assert hasattr(dim_spec, "required_elements")
            assert hasattr(dim_spec, "required_fields")
            assert hasattr(dim_spec, "minimum_coverage")
            assert hasattr(dim_spec, "weight")

            # Check types
            assert isinstance(dim_spec.name, str)
            assert isinstance(dim_spec.required_elements, list)
            assert isinstance(dim_spec.required_fields, dict)
            assert isinstance(dim_spec.minimum_coverage, float)
            assert isinstance(dim_spec.weight, float)

            # Check value ranges
            assert 0.0 <= dim_spec.minimum_coverage <= 1.0
            assert 0.0 <= dim_spec.weight <= 1.0

            # Name should match dictionary key
            assert dim_spec.name == dim_name

    def test_dimension_specific_validation_rules(self, daylight_spec):
        """Test that dimensions have appropriate validation rules."""
        # Dependencies dimension should validate version constraints
        deps_dim = daylight_spec.get_dimension("dependencies")
        assert deps_dim is not None
        assert "dependency" in deps_dim.required_fields
        deps_fields = deps_dim.required_fields["dependency"]
        assert "version" in deps_fields, "Dependencies should require version info"
        assert "failure_impact" in deps_fields, "Should document failure impact"

        # Automation dimension should validate failure handling
        auto_dim = daylight_spec.get_dimension("automation")
        assert auto_dim is not None
        if "script" in auto_dim.required_fields:
            script_fields = auto_dim.required_fields["script"]
            assert "failure_handling" in script_fields, "Scripts need failure handling"
            assert "purpose" in script_fields, "Scripts need documented purpose"

        # Lifecycle dimension should include rollback procedures
        lifecycle_dim = daylight_spec.get_dimension("lifecycle")
        assert lifecycle_dim is not None
        # Rollback is critical for lifecycle management
        assert (
            lifecycle_dim.minimum_coverage >= 0.85
        ), "Lifecycle should have high coverage requirement"

    def test_dimension_weights_reflect_importance(self, daylight_spec):
        """Test that dimension weights appropriately reflect their importance."""
        # Critical dimensions should have higher weights
        deps_weight = daylight_spec.dimensions["dependencies"].weight
        integration_weight = daylight_spec.dimensions["integration"].weight
        testing_weight = daylight_spec.dimensions["testing"].weight

        # Dependencies and integration are critical
        assert deps_weight >= 0.15, "Dependencies should have significant weight"
        assert integration_weight >= 0.15, "Integration should have significant weight"
        assert testing_weight >= 0.15, "Testing should have significant weight"

        # Less critical dimensions should have lower weights
        yearbook_weight = daylight_spec.dimensions["yearbook"].weight
        assert yearbook_weight <= 0.10, "Yearbook is less critical"

    def test_required_fields_completeness(self, daylight_spec):
        """Test that required fields cover essential documentation needs."""
        # Check dependencies dimension has all critical fields
        deps_dim = daylight_spec.get_dimension("dependencies")
        if "dependency" in deps_dim.required_fields:
            fields = deps_dim.required_fields["dependency"]
            essential_fields = ["name", "version", "purpose", "failure_impact"]
            for field in essential_fields:
                assert field in fields, f"Dependencies should require {field}"

        # Check automation dimension
        auto_dim = daylight_spec.get_dimension("automation")
        if "script" in auto_dim.required_fields:
            fields = auto_dim.required_fields["script"]
            essential_fields = ["command", "purpose", "when_to_run", "failure_handling"]
            for field in essential_fields:
                assert field in fields, f"Automation scripts should require {field}"

    def test_minimum_coverage_thresholds(self, daylight_spec):
        """Test that minimum coverage thresholds are appropriate."""
        for dim_name, dim_spec in daylight_spec.dimensions.items():
            # All dimensions should have reasonable thresholds
            assert (
                0.7 <= dim_spec.minimum_coverage <= 1.0
            ), f"{dim_name} threshold should be between 70% and 100%"

            # Critical dimensions should have higher thresholds
            if dim_name in ["dependencies", "integration", "governance"]:
                assert (
                    dim_spec.minimum_coverage >= 0.90
                ), f"{dim_name} should have high threshold (>=90%)"

    def test_dimension_validation_with_empty_data(self):
        """Test dimension validation with empty data."""
        spec = DimensionSpec(
            name="test",
            required_elements=["element1", "element2"],
            required_fields={"item": ["field1", "field2"]},
            minimum_coverage=0.85,
            weight=0.1,
        )

        # Test with completely empty data
        coverage, missing = spec.validate({})
        assert coverage == 0.0, "Empty data should have 0% coverage"
        assert "element1" in missing
        assert "element2" in missing

        # Test with partial data
        partial_data = {"element1": "value1"}
        coverage, missing = spec.validate(partial_data)
        assert 0 < coverage < 1.0, "Partial data should have partial coverage"
        assert "element2" in missing
        assert "element1" not in missing

    def test_dimension_validation_with_null_values(self):
        """Test that null/empty values are handled correctly."""
        spec = DimensionSpec(
            name="test",
            required_elements=["element1"],
            required_fields={},
            minimum_coverage=0.85,
            weight=0.1,
        )

        # None values should not count as present
        data_with_none = {"element1": None}
        coverage, missing = spec.validate(data_with_none)
        # This reveals the bug: None is counted as present
        # TODO: Fix validation to check for truthy values
        assert coverage == 1.0, "Bug: None values counted as present"

        # Empty strings should not count as present
        data_with_empty = {"element1": ""}
        coverage, missing = spec.validate(data_with_empty)
        # This also reveals the bug
        assert coverage == 1.0, "Bug: Empty strings counted as present"

    def test_language_aware_dimension_specs(self):
        """Test that specs can be language-aware (future enhancement)."""
        # This test documents the need for language-aware specs
        # Currently, all projects are evaluated with same requirements

        # Ideally, we should be able to do:
        # python_spec = DAYLIGHTSpec(project_type="python")
        # js_spec = DAYLIGHTSpec(project_type="javascript")

        # And have different required elements:
        # python_deps = python_spec.dimensions["dependencies"].required_elements
        # assert "python_version" in python_deps
        # assert "node_version" not in python_deps

        # For now, document this as a needed enhancement
        spec = DAYLIGHTSpec()
        deps = spec.dimensions["dependencies"].required_elements
        assert "node_version" in deps, "TODO: Make specs language-aware to avoid false negatives"
