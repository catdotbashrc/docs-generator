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


class TestLanguageAwareExtraction:
    """Test language-aware extraction that doesn't penalize for missing irrelevant fields"""
    
    @pytest.fixture
    def extractor(self):
        """Create a DependencyExtractor instance"""
        return DependencyExtractor()
    
    @pytest.fixture
    def temp_project_dir(self):
        """Create a temporary project directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)
    
    def test_python_project_not_penalized_for_node_version(self, extractor, temp_project_dir):
        """Python projects should not be penalized for missing node_version."""
        # Create a Python-only project
        requirements_content = """
jinja2>=3.1.0
PyYAML>=5.1
cryptography
packaging
resolvelib>=0.5.3,<2.0.0
"""
        
        requirements_file = temp_project_dir / "requirements.txt"
        with open(requirements_file, "w") as f:
            f.write(requirements_content)
        
        pyproject_content = """
[project]
requires-python = ">=3.12"
"""
        pyproject_file = temp_project_dir / "pyproject.toml"
        with open(pyproject_file, "w") as f:
            f.write(pyproject_content)
        
        # Extract dependencies
        result = extractor.extract(str(temp_project_dir))
        
        # Verify Python-specific fields are present
        assert result["python_version"] == ">=3.12"
        assert result["package_manager"] == "pip"
        assert result["lock_file"] == "requirements.txt"
        
        # node_version should be None, not required for Python projects
        assert result["node_version"] is None
        
        # TODO: When language-aware specs are implemented, this should pass:
        # from ddd.coverage import DocumentationCoverage
        # coverage = DocumentationCoverage()
        # doc_result = coverage.measure({"dependencies": result})
        # assert doc_result.dimension_scores["dependencies"] > 0.8, \
        #     "Python project should not be penalized for missing node_version"
    
    def test_node_project_not_penalized_for_python_version(self, extractor, temp_project_dir):
        """Node.js projects should not be penalized for missing python_version."""
        # Create a Node.js-only project
        package_json = {
            "name": "node-project",
            "version": "1.0.0",
            "dependencies": {
                "express": "^4.18.0",
                "lodash": "^4.17.21",
                "axios": "^1.5.0"
            },
            "engines": {
                "node": ">=18.0.0"
            }
        }
        
        package_file = temp_project_dir / "package.json"
        with open(package_file, "w") as f:
            json.dump(package_json, f)
        
        # Create package-lock.json
        (temp_project_dir / "package-lock.json").touch()
        
        # Extract dependencies
        result = extractor.extract(str(temp_project_dir))
        
        # Verify Node.js-specific fields are present
        assert result["node_version"] == ">=18.0.0"
        assert result["package_manager"] == "npm"
        assert result["lock_file"] == "package-lock.json"
        
        # python_version should be None, not required for Node projects
        assert result["python_version"] is None
        
        # TODO: When language-aware specs are implemented, this should pass:
        # from ddd.coverage import DocumentationCoverage
        # coverage = DocumentationCoverage()
        # doc_result = coverage.measure({"dependencies": result})
        # assert doc_result.dimension_scores["dependencies"] > 0.8, \
        #     "Node.js project should not be penalized for missing python_version"
    
    def test_detect_project_language_context(self, extractor, temp_project_dir):
        """Extractor should detect the primary language context of a project."""
        # Test Python project detection
        requirements_file = temp_project_dir / "requirements.txt"
        with open(requirements_file, "w") as f:
            f.write("django==4.2.0
")
        
        result = extractor.extract(str(temp_project_dir))
        
        # TODO: Add language detection to extractor
        # assert result.get("detected_language") == "python"
        # assert result.get("language_context") == {"python": True, "node": False}
        
        # For now, verify Python indicators
        assert result["package_manager"] == "pip"
        assert result["python_version"] is None  # No explicit version, but pip detected
    
    def test_mixed_language_project_extracts_all(self, extractor, temp_project_dir):
        """Mixed-language projects should extract all relevant dependencies."""
        # Create both package.json and requirements.txt
        package_json = {
            "name": "mixed-project",
            "dependencies": {"react": "^18.0.0"},
            "engines": {"node": ">=16.0.0"}
        }
        with open(temp_project_dir / "package.json", "w") as f:
            json.dump(package_json, f)
        
        with open(temp_project_dir / "requirements.txt", "w") as f:
            f.write("flask==2.3.0
celery==5.3.0
")
        
        with open(temp_project_dir / "pyproject.toml", "w") as f:
            f.write('[project]
requires-python = ">=3.9"
')
        
        result = extractor.extract(str(temp_project_dir))
        
        # Should extract from both ecosystems
        assert "react" in result["runtime_dependencies"]
        assert "flask" in result["runtime_dependencies"]
        assert "celery" in result["runtime_dependencies"]
        
        # Should have both version requirements
        assert result["node_version"] == ">=16.0.0"
        assert result["python_version"] == ">=3.9"
        
        # TODO: Mixed projects need special handling in coverage calculation
        # Should not penalize for having both, should validate each independently
    
    def test_extractor_handles_missing_optional_fields(self, extractor, temp_project_dir):
        """Extractors should gracefully handle missing optional fields."""
        # Minimal package.json without engines or version constraints
        package_json = {
            "name": "minimal-project",
            "dependencies": {
                "express": "*",  # No version constraint
                "lodash": ""     # Empty version string
            }
        }
        
        with open(temp_project_dir / "package.json", "w") as f:
            json.dump(package_json, f)
        
        result = extractor.extract(str(temp_project_dir))
        
        # Should extract dependencies even without version constraints
        assert "express" in result["runtime_dependencies"]
        assert "lodash" in result["runtime_dependencies"]
        
        # Version constraints should be captured as-is or normalized
        assert result["runtime_dependencies"]["express"]["version"] == "*"
        assert result["runtime_dependencies"]["lodash"]["version"] == ""
        
        # Missing engines field should not cause failure
        assert result["node_version"] is None
        
        # TODO: Coverage calculation should handle missing version constraints
        # as a quality issue, not a completeness issue
    
    def test_language_specific_dependency_purposes(self, extractor):
        """Test that package purpose inference is language-aware."""
        # Python-specific packages
        assert extractor._infer_purpose("django") == "Web framework"
        assert extractor._infer_purpose("flask") == "Web framework"
        assert extractor._infer_purpose("pytest") == "Testing framework"
        assert extractor._infer_purpose("numpy") == "Numerical computing"
        assert extractor._infer_purpose("pandas") == "Data analysis"
        assert extractor._infer_purpose("sqlalchemy") == "Database ORM"
        
        # Node.js-specific packages
        assert extractor._infer_purpose("express") == "Web server framework"
        assert extractor._infer_purpose("react") == "UI framework"
        assert extractor._infer_purpose("vue") == "UI framework"
        assert extractor._infer_purpose("jest") == "Testing framework"
        assert extractor._infer_purpose("mocha") == "Testing framework"
        assert extractor._infer_purpose("webpack") == "Build tool"
        
        # Infrastructure/DevOps packages (cross-language)
        assert extractor._infer_purpose("ansible") == "Infrastructure automation"
        assert extractor._infer_purpose("terraform") == "Infrastructure as Code"
        assert extractor._infer_purpose("docker") == "Containerization"
        assert extractor._infer_purpose("kubernetes") == "Container orchestration"
    
    def test_extractor_version_constraint_normalization(self, extractor, temp_project_dir):
        """Test that version constraints are normalized for consistency."""
        # Create package.json with various version formats
        package_json = {
            "dependencies": {
                "exact": "1.2.3",
                "caret": "^2.0.0",
                "tilde": "~3.1.0",
                "range": ">=4.0.0 <5.0.0",
                "wildcard": "*",
                "latest": "latest",
                "empty": ""
            }
        }
        
        with open(temp_project_dir / "package.json", "w") as f:
            json.dump(package_json, f)
        
        result = extractor.extract(str(temp_project_dir))
        
        # Verify all version formats are captured
        deps = result["runtime_dependencies"]
        assert deps["exact"]["version"] == "1.2.3"
        assert deps["caret"]["version"] == "^2.0.0"
        assert deps["tilde"]["version"] == "~3.1.0"
        assert deps["range"]["version"] == ">=4.0.0 <5.0.0"
        assert deps["wildcard"]["version"] == "*"
        assert deps["latest"]["version"] == "latest"
        assert deps["empty"]["version"] == ""
        
        # TODO: Add version constraint quality scoring
        # Exact versions and ranges should score higher than wildcards


class TestExtractorExtensibility:
    """Test extractor extensibility for future language support"""
    
    def test_extractor_plugin_interface(self):
        """Test that new extractors can be added following the plugin pattern."""
        # TODO: When additional extractors are added, verify they follow the pattern
        from ddd.extractors import DependencyExtractor
        
        # Verify base interface exists
        assert hasattr(DependencyExtractor, 'extract')
        
        # Future extractors should implement:
        # - extract(project_path) -> dict
        # - _infer_purpose(package_name) -> str
        # - _detect_package_manager(project_path) -> str
        # - _parse_version_constraint(constraint) -> dict
    
    def test_future_ruby_extractor_requirements(self):
        """Document requirements for future Ruby extractor."""
        # TODO: Ruby extractor should handle:
        # - Gemfile parsing
        # - Gemfile.lock detection
        # - Ruby version from .ruby-version or Gemfile
        # - Bundler as package manager
        # - Gem purpose inference (rails, rspec, etc.)
        pass
    
    def test_future_go_extractor_requirements(self):
        """Document requirements for future Go extractor."""
        # TODO: Go extractor should handle:
        # - go.mod parsing
        # - go.sum detection
        # - Go version from go.mod
        # - Module dependencies with versions
        # - Purpose inference for common Go packages
        pass
    
    def test_future_rust_extractor_requirements(self):
        """Document requirements for future Rust extractor."""
        # TODO: Rust extractor should handle:
        # - Cargo.toml parsing
        # - Cargo.lock detection
        # - Rust version from rust-toolchain.toml
        # - Crate dependencies with versions
        # - Purpose inference for common crates
        pass
    
    def test_future_java_extractor_requirements(self):
        """Document requirements for future Java extractor."""
        # TODO: Java extractor should handle:
        # - pom.xml (Maven) parsing
        # - build.gradle (Gradle) parsing
        # - Java version detection
        # - Dependency management (Maven Central, etc.)
        # - Purpose inference for common Java libraries
        pass
    
    def test_language_detection_strategy(self):
        """Test strategy for detecting project language."""
        # TODO: Implement language detection based on:
        # 1. File presence priority:
        #    - package.json -> JavaScript/TypeScript
        #    - requirements.txt/pyproject.toml -> Python
        #    - Gemfile -> Ruby
        #    - go.mod -> Go
        #    - Cargo.toml -> Rust
        #    - pom.xml/build.gradle -> Java
        # 2. File extensions in project
        # 3. Configuration files
        # 4. Directory structure conventions
        pass
