"""
Unit tests for DependencyExtractor and other extractors
"""

import json
import tempfile
from pathlib import Path

import pytest

from ddd.extractors import DependencyExtractor


class TestDependencyExtractor:
    """Test DependencyExtractor class"""

    @pytest.fixture
    def extractor(self):
        """Create a DependencyExtractor instance"""
        return DependencyExtractor()

    @pytest.fixture
    def temp_project_dir(self):
        """Create a temporary project directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    def test_extract_javascript_dependencies(self, extractor, temp_project_dir):
        """Test extracting JavaScript/Node.js dependencies"""
        # Create a package.json file
        package_json = {
            "name": "test-project",
            "version": "1.0.0",
            "dependencies": {"express": "^4.18.0", "lodash": "^4.17.21"},
            "engines": {"node": ">=18.0.0"},
        }

        package_file = temp_project_dir / "package.json"
        with open(package_file, "w") as f:
            json.dump(package_json, f)

        # Create a package-lock.json
        (temp_project_dir / "package-lock.json").touch()

        # Extract dependencies
        result = extractor.extract(str(temp_project_dir))

        assert "runtime_dependencies" in result
        assert "express" in result["runtime_dependencies"]
        assert result["runtime_dependencies"]["express"]["version"] == "^4.18.0"
        assert result["runtime_dependencies"]["express"]["purpose"] == "Web server framework"
        assert result["node_version"] == ">=18.0.0"
        assert result["package_manager"] == "npm"
        assert result["lock_file"] == "package-lock.json"

    def test_extract_python_dependencies_pyproject(self, extractor, temp_project_dir):
        """Test extracting Python dependencies from pyproject.toml"""
        # Create a pyproject.toml file
        pyproject_content = """
[project]
name = "test-project"
version = "1.0.0"
requires-python = ">=3.11"
dependencies = [
    "pytest>=7.0",
    "requests==2.31.0",
    "flask"
]
"""

        pyproject_file = temp_project_dir / "pyproject.toml"
        with open(pyproject_file, "w") as f:
            f.write(pyproject_content)

        # Extract dependencies
        result = extractor.extract(str(temp_project_dir))

        assert "runtime_dependencies" in result
        assert "pytest" in result["runtime_dependencies"]
        assert result["runtime_dependencies"]["pytest"]["version"] == "7.0"
        assert result["runtime_dependencies"]["pytest"]["purpose"] == "Testing framework"
        assert "requests" in result["runtime_dependencies"]
        assert result["runtime_dependencies"]["requests"]["version"] == "2.31.0"
        assert result["python_version"] == ">=3.11"

    def test_extract_python_dependencies_requirements(self, extractor, temp_project_dir):
        """Test extracting Python dependencies from requirements.txt"""
        # Create a requirements.txt file
        requirements_content = """
django==4.2.0
numpy>=1.24.0
pandas
# This is a comment
pytest==7.4.0
"""

        requirements_file = temp_project_dir / "requirements.txt"
        with open(requirements_file, "w") as f:
            f.write(requirements_content)

        # Extract dependencies
        result = extractor.extract(str(temp_project_dir))

        assert "runtime_dependencies" in result
        assert "django" in result["runtime_dependencies"]
        assert result["runtime_dependencies"]["django"]["version"] == "4.2.0"
        assert result["runtime_dependencies"]["django"]["purpose"] == "Web framework"
        assert "numpy" in result["runtime_dependencies"]
        assert result["runtime_dependencies"]["numpy"]["version"] == "1.24.0"
        assert result["package_manager"] == "pip"
        assert result["lock_file"] == "requirements.txt"

    def test_extract_with_yarn_lock(self, extractor, temp_project_dir):
        """Test detecting yarn as package manager"""
        # Create package.json
        package_json = {"name": "test", "dependencies": {}}
        with open(temp_project_dir / "package.json", "w") as f:
            json.dump(package_json, f)

        # Create yarn.lock
        (temp_project_dir / "yarn.lock").touch()

        result = extractor.extract(str(temp_project_dir))
        assert result["package_manager"] == "yarn"
        assert result["lock_file"] == "yarn.lock"

    def test_extract_with_pnpm_lock(self, extractor, temp_project_dir):
        """Test detecting pnpm as package manager"""
        # Create package.json
        package_json = {"name": "test", "dependencies": {}}
        with open(temp_project_dir / "package.json", "w") as f:
            json.dump(package_json, f)

        # Create pnpm-lock.yaml
        (temp_project_dir / "pnpm-lock.yaml").touch()

        result = extractor.extract(str(temp_project_dir))
        assert result["package_manager"] == "pnpm"
        assert result["lock_file"] == "pnpm-lock.yaml"

    def test_extract_with_poetry_lock(self, extractor, temp_project_dir):
        """Test detecting poetry as package manager"""
        # Create pyproject.toml
        pyproject_content = """
[project]
dependencies = []
"""
        with open(temp_project_dir / "pyproject.toml", "w") as f:
            f.write(pyproject_content)

        # Create poetry.lock
        (temp_project_dir / "poetry.lock").touch()

        result = extractor.extract(str(temp_project_dir))
        assert result["package_manager"] == "poetry"
        assert result["lock_file"] == "poetry.lock"

    def test_extract_with_nvmrc(self, extractor, temp_project_dir):
        """Test reading Node version from .nvmrc"""
        # Create .nvmrc
        with open(temp_project_dir / ".nvmrc", "w") as f:
            f.write("18.17.0\n")

        # Create package.json without engines
        package_json = {"name": "test", "dependencies": {}}
        with open(temp_project_dir / "package.json", "w") as f:
            json.dump(package_json, f)

        result = extractor.extract(str(temp_project_dir))
        assert result["node_version"] == "18.17.0"

    def test_extract_empty_project(self, extractor, temp_project_dir):
        """Test extracting from empty project"""
        result = extractor.extract(str(temp_project_dir))

        assert result["runtime_dependencies"] == {}
        assert result["node_version"] is None
        assert result["package_manager"] is None
        assert result["lock_file"] is None

    def test_infer_purpose(self, extractor):
        """Test package purpose inference"""
        assert extractor._infer_purpose("express") == "Web server framework"
        assert extractor._infer_purpose("react") == "UI framework"
        assert extractor._infer_purpose("jest") == "Testing framework"
        assert extractor._infer_purpose("pytest") == "Testing framework"
        assert extractor._infer_purpose("django") == "Web framework"
        assert extractor._infer_purpose("numpy") == "Numerical computing"
        assert (
            extractor._infer_purpose("unknown-package") == "Provides unknown-package functionality"
        )

    def test_mixed_project(self, extractor, temp_project_dir):
        """Test project with both JavaScript and Python dependencies"""
        # Create package.json
        package_json = {"dependencies": {"express": "^4.18.0"}}
        with open(temp_project_dir / "package.json", "w") as f:
            json.dump(package_json, f)

        # Create requirements.txt
        with open(temp_project_dir / "requirements.txt", "w") as f:
            f.write("flask==2.3.0\n")

        result = extractor.extract(str(temp_project_dir))

        # Should have both JavaScript and Python dependencies
        assert "express" in result["runtime_dependencies"]
        assert "flask" in result["runtime_dependencies"]
