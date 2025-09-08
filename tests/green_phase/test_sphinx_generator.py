#!/usr/bin/env python3
"""
GREEN Phase Test: Sphinx Documentation Generator
Verify that the generator creates proper documentation structure.
"""

import shutil
import tempfile
from pathlib import Path

import pytest

from ddd.extractors.ansible_advanced import AdvancedAnsibleExtractor
from ddd.generators.sphinx_generator import SphinxDocumentationGenerator


class TestSphinxGenerator:
    """Test the Sphinx documentation generator."""

    def test_generate_documentation_structure(self):
        """Test that proper Sphinx structure is created."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "docs"
            generator = SphinxDocumentationGenerator(output_dir)

            # Setup project
            generator.setup_sphinx_project()

            # Check structure
            assert (output_dir / "source").exists()
            assert (output_dir / "build").exists()
            assert (output_dir / "source" / "conf.py").exists()
            assert (output_dir / "source" / "_static").exists()
            assert (output_dir / "source" / "_templates").exists()

    def test_generate_module_documentation(self):
        """Test generating documentation for a module."""
        # Sample module content
        module_content = '''
#!/usr/bin/python
DOCUMENTATION = """
module: test_module
short_description: Test module for Sphinx generation
description:
  - This module tests documentation generation
  - It includes all standard blocks
options:
  path:
    description: Path to file
    required: true
    type: path
  state:
    description: State of file
    choices: [present, absent]
    default: present
"""

EXAMPLES = """
- name: Create a file
  test_module:
    path: /tmp/test.txt
    state: present
"""

RETURN = """
path:
    description: Path to the file
    type: str
    returned: always
changed:
    description: Whether module made changes
    type: bool
    returned: always
"""

import boto3

def main():
    ec2 = boto3.client('ec2')
    ec2.describe_instances()
    
    if not os.path.exists(path):
        module.fail_json(msg="Path does not exist")
'''

        # Extract data
        extractor = AdvancedAnsibleExtractor()
        extracted = extractor.extract_complete(module_content)
        extracted["permissions"] = extractor.extract_permissions(module_content)
        extracted["error_patterns"] = extractor.extract_error_patterns(module_content)

        # Generate documentation
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "docs"
            generator = SphinxDocumentationGenerator(output_dir)
            generator.setup_sphinx_project()

            # Generate module doc
            generator.generate_module_documentation("test_module", extracted)

            # Check file exists
            module_file = output_dir / "source" / "modules" / "test_module.rst"
            assert module_file.exists()

            # Check content
            content = module_file.read_text()
            assert "test_module" in content
            assert "Test module for Sphinx generation" in content
            assert "AWS IAM Permissions Required" in content
            assert "ec2:DescribeInstances" in content
            assert "Path does not exist" in content
            assert "Parameters" in content
            assert "Usage Examples" in content
            assert "HUMAN INPUT NEEDED" in content

    def test_generate_index(self):
        """Test index generation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "docs"
            generator = SphinxDocumentationGenerator(output_dir)
            generator.setup_sphinx_project()

            # Generate index
            modules = ["file", "copy", "template", "systemd"]
            generator.generate_index(modules)

            # Check index exists
            index_file = output_dir / "source" / "index.rst"
            assert index_file.exists()

            # Check content
            content = index_file.read_text()
            assert "Ansible Module Maintenance Documentation" in content
            assert "modules/file" in content
            assert "modules/copy" in content
            assert "HUMAN INPUT NEEDED" in content

    def test_complete_workflow(self):
        """Test complete documentation generation workflow."""
        # Multiple modules
        modules_data = {
            "test_module": {
                "documentation": {
                    "module": "test_module",
                    "short_description": "Test module",
                    "options": {"path": {"required": True, "type": "path"}},
                },
                "permissions": ["ec2:DescribeInstances", "s3:PutObject"],
                "examples": [{"name": "Test", "module": "test_module", "parameters": {}}],
                "returns": {"path": {"type": "str", "returned": "always"}},
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "docs"
            generator = SphinxDocumentationGenerator(output_dir)

            # Generate complete documentation (without HTML build)
            generator.setup_sphinx_project()
            for module_name, data in modules_data.items():
                generator.generate_module_documentation(module_name, data)
            generator.generate_index(list(modules_data.keys()))

            # Check all files exist
            assert (output_dir / "source" / "index.rst").exists()
            assert (output_dir / "source" / "modules" / "test_module.rst").exists()
            assert (output_dir / "source" / "conf.py").exists()
