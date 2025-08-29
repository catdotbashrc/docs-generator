"""
Documentation Extractors
Extract documentation from codebases
"""

import json
from pathlib import Path
from typing import Dict


class DependencyExtractor:
    """
    Extract dependency documentation from JavaScript/Python projects.
    This is our first MVP extractor focusing on the Dependencies dimension.
    """

    def extract(self, project_path: str) -> Dict:
        """Extract dependency information from a project"""
        path = Path(project_path)
        result = {
            "runtime_dependencies": {},
            "node_version": None,
            "package_manager": None,
            "lock_file": None,
        }

        # Try JavaScript/Node.js first
        package_json = path / "package.json"
        if package_json.exists():
            result.update(self._extract_javascript_deps(path))

        # Try Python
        pyproject = path / "pyproject.toml"
        requirements = path / "requirements.txt"
        if pyproject.exists() or requirements.exists():
            result.update(self._extract_python_deps(path))

        return result

    def _extract_javascript_deps(self, path: Path) -> Dict:
        """Extract JavaScript/Node.js dependencies"""
        result = {}

        # Read package.json
        package_json = path / "package.json"
        if package_json.exists():
            with open(package_json) as f:
                data = json.load(f)

            # Extract runtime dependencies
            deps = {}
            for dep_name, version in data.get("dependencies", {}).items():
                deps[dep_name] = {
                    "name": dep_name,
                    "version": version,
                    "purpose": self._infer_purpose(dep_name),
                    "failure_impact": f"Application may fail if {dep_name} is unavailable",
                }
            result["runtime_dependencies"] = deps

            # Extract Node version
            if "engines" in data:
                result["node_version"] = data["engines"].get("node")

        # Check for lock files
        if (path / "package-lock.json").exists():
            result["package_manager"] = "npm"
            result["lock_file"] = "package-lock.json"
        elif (path / "yarn.lock").exists():
            result["package_manager"] = "yarn"
            result["lock_file"] = "yarn.lock"
        elif (path / "pnpm-lock.yaml").exists():
            result["package_manager"] = "pnpm"
            result["lock_file"] = "pnpm-lock.yaml"

        # Check for .nvmrc
        nvmrc = path / ".nvmrc"
        if nvmrc.exists() and not result.get("node_version"):
            result["node_version"] = nvmrc.read_text().strip()

        return result

    def _extract_python_deps(self, path: Path) -> Dict:
        """Extract Python dependencies"""
        result = {}
        deps = {}

        # Try pyproject.toml
        pyproject = path / "pyproject.toml"
        if pyproject.exists():
            import tomllib

            with open(pyproject, "rb") as f:
                data = tomllib.load(f)

            # Extract dependencies
            project_deps = data.get("project", {}).get("dependencies", [])
            for dep_str in project_deps:
                # Parse dependency string (simplified)
                if ">=" in dep_str:
                    name, version = dep_str.split(">=")
                elif "==" in dep_str:
                    name, version = dep_str.split("==")
                else:
                    name = dep_str
                    version = "*"

                deps[name] = {
                    "name": name.strip(),
                    "version": version.strip(),
                    "purpose": self._infer_purpose(name),
                    "failure_impact": f"Application may fail if {name} is unavailable",
                }

            # Get Python version
            python_version = data.get("project", {}).get("requires-python")
            if python_version:
                result["python_version"] = python_version

        # Try requirements.txt
        requirements = path / "requirements.txt"
        if requirements.exists() and not deps:
            with open(requirements) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        # Parse requirement (simplified)
                        if ">=" in line:
                            name, version = line.split(">=")
                        elif "==" in line:
                            name, version = line.split("==")
                        else:
                            name = line
                            version = "*"

                        deps[name] = {
                            "name": name.strip(),
                            "version": version.strip(),
                            "purpose": self._infer_purpose(name),
                            "failure_impact": f"Application may fail if {name} is unavailable",
                        }

        result["runtime_dependencies"] = deps

        # Check for lock files
        if (path / "poetry.lock").exists():
            result["package_manager"] = "poetry"
            result["lock_file"] = "poetry.lock"
        elif (path / "Pipfile.lock").exists():
            result["package_manager"] = "pipenv"
            result["lock_file"] = "Pipfile.lock"
        elif requirements.exists():
            result["package_manager"] = "pip"
            result["lock_file"] = "requirements.txt"

        return result

    def _infer_purpose(self, package_name: str) -> str:
        """Infer the purpose of a package from its name"""
        # Common package purposes (simplified for MVP)
        purposes = {
            "express": "Web server framework",
            "react": "UI framework",
            "jest": "Testing framework",
            "pytest": "Testing framework",
            "django": "Web framework",
            "flask": "Web microframework",
            "fastapi": "API framework",
            "numpy": "Numerical computing",
            "pandas": "Data analysis",
            "requests": "HTTP client",
            "axios": "HTTP client",
            "lodash": "Utility functions",
            "moment": "Date manipulation",
            "dotenv": "Environment configuration",
            "eslint": "Code linting",
            "prettier": "Code formatting",
            "webpack": "Module bundler",
            "babel": "JavaScript compiler",
        }

        return purposes.get(package_name.lower(), f"Provides {package_name} functionality")
