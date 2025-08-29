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
