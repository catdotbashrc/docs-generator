#!/usr/bin/env python3
"""
RED Phase Tests: Core Extraction Requirements
These tests define WHAT we want to extract before we implement HOW.
They will FAIL until we write the code to make them pass.
"""

from pathlib import Path

import pytest

# These imports will fail initially - that's the RED phase!
# We're defining what we WANT to exist
from ddd.extractors.ansible_advanced import AdvancedAnsibleExtractor


class TestCoreExtractionRequirements:
    """Define what successful extraction looks like before implementation."""

    def test_extract_documentation_block_structure(self):
        """DOCUMENTATION block must be fully parsed with all fields."""
        # RED: This test defines the expected structure
        content = '''
DOCUMENTATION = """
---
module: file
short_description: Manage files and file properties
version_added: "0.1"
description:
  - Set file attributes
  - Create files, directories, hard links, symlinks
options:
  path:
    description: Path to the file being managed
    required: true
    type: path
  state:
    description: State of the file
    choices: [absent, directory, file, hard, link, touch]
    default: file
  mode:
    description: Permissions of the file
    type: raw
  owner:
    description: Owner of the file
    type: str
requirements:
  - python >= 3.6
"""
'''
        extractor = AdvancedAnsibleExtractor()
        docs = extractor.extract_documentation(content)

        # Must extract module metadata
        assert docs["module"] == "file"
        assert docs["short_description"] == "Manage files and file properties"
        assert docs["version_added"] == "0.1"

        # Must extract all parameters
        assert "path" in docs["options"]
        assert docs["options"]["path"]["required"] is True
        assert docs["options"]["path"]["type"] == "path"
        assert "description" in docs["options"]["path"]

        # Must extract parameter choices/defaults
        assert "state" in docs["options"]
        assert "choices" in docs["options"]["state"]
        assert "file" in docs["options"]["state"]["choices"]
        assert docs["options"]["state"]["default"] == "file"

        # Must extract requirements
        assert "requirements" in docs
        assert "python >= 3.6" in docs["requirements"]

    def test_extract_examples_for_scenarios(self):
        """EXAMPLES must be extracted and parseable as maintenance scenarios."""
        content = '''
EXAMPLES = """
- name: Create a directory
  file:
    path: /etc/app
    state: directory
    mode: '0755'

- name: Touch a file with specific permissions
  file:
    path: /etc/app/config.yml
    state: touch
    mode: '0644'
    owner: app
    group: app
"""
'''
        extractor = AdvancedAnsibleExtractor()
        examples = extractor.extract_examples(content)

        assert len(examples) >= 2
        assert isinstance(examples[0], dict)
        assert examples[0]["name"] == "Create a directory"
        assert examples[0]["module"] == "file"
        assert examples[0]["parameters"]["path"] == "/etc/app"
        assert examples[0]["parameters"]["state"] == "directory"

        # Examples should be convertible to maintenance scenarios
        scenario = extractor.example_to_scenario(examples[0])
        assert scenario.name == "Create a directory"
        assert scenario.description is not None
        assert scenario.ansible_task is not None
        assert scenario.expected_outcome == "Directory /etc/app created with 0755 permissions"

    def test_extract_return_values(self):
        """RETURN block must be extracted for understanding state changes."""
        content = '''
RETURN = """
path:
    description: Path to the file being managed
    returned: always
    type: str
    sample: /path/to/file.txt
changed:
    description: Whether the module changed anything
    returned: always
    type: bool
    sample: true
uid:
    description: Owner ID of the file
    returned: success
    type: int
    sample: 1000
gid:
    description: Group ID of the file  
    returned: success
    type: int
    sample: 1000
mode:
    description: Permissions of the file
    returned: success
    type: str
    sample: "0644"
state:
    description: State of the target
    returned: success
    type: str
    sample: file
"""
'''
        extractor = AdvancedAnsibleExtractor()
        returns = extractor.extract_returns(content)

        # Must extract all return values with metadata
        assert "path" in returns
        assert returns["path"]["description"] == "Path to the file being managed"
        assert returns["path"]["returned"] == "always"
        assert returns["path"]["type"] == "str"

        assert "changed" in returns
        assert returns["changed"]["type"] == "bool"

        # Return values should indicate what can be verified
        verifiable_state = extractor.get_verifiable_state(returns)
        assert "path" in verifiable_state  # Can verify path exists
        assert "mode" in verifiable_state  # Can verify permissions
        assert "uid" in verifiable_state  # Can verify ownership
        assert "state" in verifiable_state  # Can verify file type

    def test_full_module_extraction(self):
        """Must handle complete module with all blocks."""
        # Using a minimal but complete module
        content = '''
#!/usr/bin/python
DOCUMENTATION = """
---
module: test_module
short_description: Test module for TDD
options:
  name:
    required: true
    type: str
"""

EXAMPLES = """
- name: Test example
  test_module:
    name: test
"""

RETURN = """
result:
    description: Test result
    type: str
    returned: always
"""

def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(required=True, type='str')
        )
    )
    module.exit_json(changed=True, result="success")
'''
        extractor = AdvancedAnsibleExtractor()

        # Should extract all components
        result = extractor.extract_complete(content)

        assert result["documentation"] is not None
        assert result["examples"] is not None
        assert result["returns"] is not None
        assert result["documentation"]["module"] == "test_module"
        assert len(result["examples"]) >= 1
        assert "result" in result["returns"]
