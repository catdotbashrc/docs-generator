"""
RED Phase: Test-Driven Development for GenericPythonExtractor

Following the same TDD approach as test_ansible_extractor.py.
These tests prove DDD's extensibility beyond Ansible.
"""

from pathlib import Path
from textwrap import dedent

import pytest

from ddd.artifact_extractors.base import ConnectionRequirement, ErrorPattern, StateManagement
from ddd.extractors.python_generic import GenericPythonExtractor, PythonResourcePermission


class TestGenericPythonExtractor:
    """
    RED Phase: Define expectations for generic Python extraction
    """

    @pytest.fixture
    def extractor(self):
        """Create a GenericPythonExtractor instance"""
        return GenericPythonExtractor()

    @pytest.fixture
    def temp_python_file(self, tmp_path):
        """Create a temporary Python file for testing"""

        def _create_file(content: str, filename: str = "test.py"):
            file_path = tmp_path / filename
            file_path.write_text(content)
            return file_path

        return _create_file

    # RED Test 1: Extract import dependencies
    def test_extract_dependencies_from_imports(self, extractor, temp_python_file):
        """Should extract all import dependencies from Python code"""
        content = dedent(
            """
            import os
            import sys
            from pathlib import Path
            from typing import List, Optional
            import requests
            from flask import Flask, jsonify
        """
        )

        file_path = temp_python_file(content)
        doc = extractor.extract(file_path)

        # Expect both standard library and third-party dependencies
        assert "os" in doc.dependencies
        assert "sys" in doc.dependencies
        assert "pathlib" in doc.dependencies
        assert "typing" in doc.dependencies
        assert "requests" in doc.dependencies
        assert "flask" in doc.dependencies

        # Should be deduplicated
        assert len(doc.dependencies) == len(set(doc.dependencies))

    # RED Test 2: Extract file system permissions
    def test_extract_filesystem_permissions(self, extractor, temp_python_file):
        """Should identify file system operations as permissions"""
        content = dedent(
            """
            def process_file(filename):
                with open(filename, 'r') as f:
                    data = f.read()
                
                output_path = Path('output.txt')
                output_path.write_text(data)
                
                if output_path.exists():
                    output_path.unlink()
        """
        )

        file_path = temp_python_file(content)
        doc = extractor.extract(file_path)

        # Should find file permissions
        assert len(doc.permissions) > 0

        # Check for specific file operations
        fs_perms = [
            p
            for p in doc.permissions
            if isinstance(p, PythonResourcePermission) and p.resource_type == "filesystem"
        ]
        assert len(fs_perms) > 0

        # Should find read, write, and delete operations
        operations = [p.operation for p in fs_perms]
        assert "open" in operations or "read" in operations
        assert "write_text" in operations or "write" in operations
        assert "unlink" in operations or "delete" in operations

    # RED Test 3: Extract network permissions
    def test_extract_network_permissions(self, extractor, temp_python_file):
        """Should identify network operations as permissions"""
        content = dedent(
            """
            import requests
            import urllib.request
            
            def fetch_data():
                response = requests.get('https://api.example.com/data')
                data = response.json()
                
                with urllib.request.urlopen('https://example.com') as resp:
                    html = resp.read()
                
                requests.post('https://api.example.com/submit', json=data)
        """
        )

        file_path = temp_python_file(content)
        doc = extractor.extract(file_path)

        # Should find network permissions
        network_perms = [
            p
            for p in doc.permissions
            if isinstance(p, PythonResourcePermission) and p.resource_type == "network"
        ]
        assert len(network_perms) > 0

        # Should identify different HTTP methods
        operations = [p.operation for p in network_perms]
        assert "get" in operations
        assert "post" in operations

    # RED Test 4: Extract database permissions
    def test_extract_database_permissions(self, extractor, temp_python_file):
        """Should identify database operations as permissions"""
        content = dedent(
            """
            import sqlite3
            
            def query_database():
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()
                
                cursor.execute("SELECT * FROM users")
                results = cursor.fetchall()
                
                cursor.execute("INSERT INTO users VALUES (?, ?)", (name, email))
                conn.commit()
                
                conn.close()
        """
        )

        file_path = temp_python_file(content)
        doc = extractor.extract(file_path)

        # Should find database permissions
        db_perms = [
            p
            for p in doc.permissions
            if isinstance(p, PythonResourcePermission) and p.resource_type == "database"
        ]
        assert len(db_perms) > 0

        # Should identify SQL operations
        operations = [p.operation for p in db_perms]
        assert "execute" in operations or "query" in operations
        assert "commit" in operations or "write" in operations

    # RED Test 5: Extract error patterns
    def test_extract_error_patterns(self, extractor, temp_python_file):
        """Should extract exception patterns from Python code"""
        content = dedent(
            """
            def risky_operation(data):
                if not data:
                    raise ValueError("Data cannot be empty")
                
                try:
                    result = process(data)
                except FileNotFoundError as e:
                    print(f"File not found: {e}")
                    raise
                except ConnectionError:
                    return None
                except Exception as e:
                    logger.error(f"Unexpected error: {e}")
                    raise RuntimeError("Processing failed") from e
                
                return result
        """
        )

        file_path = temp_python_file(content)
        doc = extractor.extract(file_path)

        # Should find raised exceptions
        assert len(doc.error_patterns) > 0

        error_types = [e.pattern for e in doc.error_patterns]
        assert "ValueError" in error_types
        assert "RuntimeError" in error_types

        # Should find handled exceptions
        assert "FileNotFoundError" in error_types
        assert "ConnectionError" in error_types

        # Should have recovery hints
        for pattern in doc.error_patterns:
            assert len(pattern.recovery_hints) > 0

    # RED Test 6: Extract connection requirements
    def test_extract_connection_requirements(self, extractor, temp_python_file):
        """Should identify external connection requirements"""
        content = dedent(
            """
            import requests
            import psycopg2
            import boto3
            from azure.storage import BlobServiceClient
            
            def cloud_operations():
                # AWS
                s3 = boto3.client('s3')
                
                # Database
                conn = psycopg2.connect("dbname=test user=postgres")
                
                # HTTP API
                response = requests.get('https://api.example.com')
                
                # Azure
                blob_service = BlobServiceClient.from_connection_string(conn_str)
        """
        )

        file_path = temp_python_file(content)
        doc = extractor.extract(file_path)

        # Should find multiple connection types
        assert len(doc.connection_requirements) > 0

        conn_types = [c.type for c in doc.connection_requirements]

        # Should identify cloud services
        assert any("AWS" in t for t in conn_types)
        assert any("Azure" in t for t in conn_types)

        # Should identify database connections
        assert any("PostgreSQL" in t or "Database" in t for t in conn_types)

        # Should identify HTTP connections
        assert any("HTTP" in t for t in conn_types)

        # Should have authentication details
        for conn in doc.connection_requirements:
            assert conn.authentication is not None
            assert len(conn.authentication) > 0

    # RED Test 7: Extract state management
    def test_extract_state_management(self, extractor, temp_python_file):
        """Should identify state management patterns"""
        content = dedent(
            """
            import redis
            
            class UserSession:
                def __init__(self):
                    self.session_data = {}
                    self.redis_client = redis.Redis()
                    self.modified = False
                
                def set_value(self, key, value):
                    self.session_data[key] = value
                    self.modified = True
                    self.redis_client.set(f"session:{key}", value)
                
                def save(self):
                    if self.modified:
                        # Save to database
                        pass
            
            # Global state
            active_sessions = {}
        """
        )

        file_path = temp_python_file(content)
        doc = extractor.extract(file_path)

        # Should detect state management
        assert doc.state_management is not None

        # Should identify non-idempotent operations (due to global state)
        assert doc.state_management.idempotent is False

        # Should identify change tracking mechanism
        assert (
            "cache" in doc.state_management.change_tracking.lower()
            or "redis" in doc.state_management.change_tracking.lower()
        )

    # RED Test 8: Generate maintenance scenarios
    def test_generate_python_specific_scenarios(self, extractor, temp_python_file):
        """Should generate Python-specific maintenance scenarios"""
        content = dedent(
            """
            import requests
            import psycopg2
            import pandas as pd
            import numpy as np
            from flask import Flask
            
            app = Flask(__name__)
            
            def data_pipeline():
                # Database operation
                conn = psycopg2.connect("dbname=analytics")
                
                # API call
                response = requests.get("https://api.data.com/metrics")
                
                # Data processing
                df = pd.DataFrame(response.json())
                result = df.groupby('category').sum()
                
                return result
        """
        )

        file_path = temp_python_file(content)
        doc = extractor.extract(file_path)

        # Should generate maintenance scenarios
        assert len(doc.maintenance_scenarios) > 0

        scenario_names = [s.name for s in doc.maintenance_scenarios]

        # Should include database-specific scenarios
        assert any("database" in name.lower() for name in scenario_names)

        # Should include API-specific scenarios
        assert any("api" in name.lower() for name in scenario_names)

        # Should include dependency scenarios (many imports)
        assert any(
            "dependency" in name.lower() or "version" in name.lower() for name in scenario_names
        )

        # Each scenario should have steps and recovery procedure
        for scenario in doc.maintenance_scenarios:
            assert len(scenario.steps) > 0
            assert scenario.recovery_procedure is not None

    # RED Test 9: Work on DDD's own codebase
    def test_analyze_ddd_codebase(self, extractor):
        """Should successfully analyze DDD's own Python code"""
        # Try to analyze the base extractor itself
        base_file = Path("src/ddd/artifact_extractors/base.py")

        if base_file.exists():
            doc = extractor.extract(base_file)

            # Should extract meaningful data from DDD's code
            assert len(doc.dependencies) > 0
            assert "abc" in doc.dependencies  # We know base.py imports ABC
            assert "dataclasses" in doc.dependencies
            assert "pathlib" in doc.dependencies
            assert "typing" in doc.dependencies

            # Should find error patterns (base.py has error handling)
            assert len(doc.error_patterns) > 0

            # Should identify file operations (base.py reads files)
            fs_perms = [
                p
                for p in doc.permissions
                if isinstance(p, PythonResourcePermission) and p.resource_type == "filesystem"
            ]
            assert len(fs_perms) > 0

    # RED Test 10: Prove extensibility - no Ansible coupling
    def test_no_ansible_specific_behavior(self, extractor, temp_python_file):
        """GenericPythonExtractor should have ZERO Ansible-specific behavior"""
        # Create a file with boto3 calls (what Ansible extractor looks for)
        content = dedent(
            """
            import boto3
            
            def aws_operations():
                ec2 = boto3.client('ec2')
                instances = ec2.describe_instances()
                
                s3 = boto3.client('s3')
                s3.list_buckets()
        """
        )

        file_path = temp_python_file(content)
        doc = extractor.extract(file_path)

        # Should NOT extract AWS IAM permissions like Ansible extractor
        # Should treat these as generic network/API calls
        aws_iam_perms = [
            p for p in doc.permissions if hasattr(p, "service") and hasattr(p, "action")
        ]
        assert len(aws_iam_perms) == 0  # No AWS-specific permission objects

        # Should identify boto3 as a dependency
        assert "boto3" in doc.dependencies

        # Should identify AWS connection requirement
        aws_conns = [c for c in doc.connection_requirements if "AWS" in c.type]
        assert len(aws_conns) > 0
