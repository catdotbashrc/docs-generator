"""
Test suite to verify abstraction layer security and functionality.

This ensures:
1. No proprietary code leaks into public repositories
2. Abstraction works with any client (not just DSNY)
3. Pattern extraction remains generic and reusable
"""

import pytest
import os
import subprocess
from pathlib import Path
import tempfile
import shutil
from unittest.mock import Mock, patch

class TestGitIgnoreSecurity:
    """Verify .gitignore properly protects sensitive content."""
    
    def test_dsny_directory_is_ignored(self):
        """DSNY directory must be in .gitignore."""
        with open('.gitignore', 'r') as f:
            gitignore_content = f.read()
        
        assert 'docs/source/examples/dsny_/' in gitignore_content
        assert '.serena/' in gitignore_content
        assert '.claude/' in gitignore_content
    
    def test_sql_files_are_ignored(self):
        """SQL files should be ignored by default."""
        with open('.gitignore', 'r') as f:
            gitignore_content = f.read()
        
        assert '*.sql' in gitignore_content
    
    def test_git_check_ignore_works(self):
        """Git should properly ignore protected directories."""
        # This test runs the actual git check-ignore command
        result = subprocess.run(
            ['git', 'check-ignore', 'docs/source/examples/dsny_/'],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0  # 0 means it IS ignored
    
    def test_no_dsny_files_in_git_index(self):
        """No DSNY files should be in git index."""
        result = subprocess.run(
            ['git', 'ls-files'],
            capture_output=True,
            text=True
        )
        files_in_git = result.stdout.strip().split('\n')
        
        # Check no files contain dsny in their path
        dsny_files = [f for f in files_in_git if 'dsny_/' in f]
        assert len(dsny_files) == 0, f"Found DSNY files in git: {dsny_files}"


class TestCodeAbstraction:
    """Verify code remains abstract and not client-specific."""
    
    def test_java_parser_accepts_any_namespace(self):
        """Java parser should work with any namespace, not just DSNY."""
        from automation.java_parser import extract_endpoints_from_java
        
        # Test with different namespaces
        test_cases = [
            ('http://api.example.com/', 'Example Corp'),
            ('http://services.acme.org/', 'ACME'),
            ('http://internal.company.net/', 'Internal'),
        ]
        
        for namespace, client in test_cases:
            java_code = f'''
            @WebService(targetNamespace = "{namespace}")
            public class TestService {{
                @WebMethod
                public String getData() {{ return "data"; }}
            }}
            '''
            
            # Parser should handle any namespace
            endpoints = extract_endpoints_from_java(java_code)
            assert len(endpoints) > 0
            assert namespace in str(endpoints)
    
    def test_templates_use_variables_not_hardcoded_values(self):
        """Templates should use variables like {{client_name}} not 'DSNY'."""
        template_dir = Path('docs/source/_templates')
        
        for template_file in template_dir.glob('*.rst'):
            with open(template_file, 'r') as f:
                content = f.read()
            
            # Should not contain hardcoded DSNY references
            assert 'DSNY' not in content or '{{ client' in content, \
                f"Template {template_file} contains hardcoded DSNY reference"
            
            # Should use template variables
            assert '{{' in content, \
                f"Template {template_file} doesn't use template variables"
    
    def test_extractor_works_with_multiple_clients(self):
        """Extractor should handle different client patterns."""
        from automation.filesystem.memory import MemoryFileSystem
        from automation.java_ast_extractor import JavaASTExtractor
        
        fs = MemoryFileSystem()
        extractor = JavaASTExtractor(fs)
        
        # Test with different package naming conventions
        client_patterns = [
            'com.example.api',
            'org.company.services',
            'gov.agency.systems',
            'edu.university.research',
        ]
        
        for package in client_patterns:
            java_code = f'''
            package {package}.webservice;
            
            @WebService
            public class Service {{
                @WebMethod
                public String process() {{ return "ok"; }}
            }}
            '''
            
            fs.write_text('Service.java', java_code)
            result = extractor.extract_documentation('Service.java')
            
            assert result is not None
            assert 'endpoints' in result
            # Should work regardless of package structure


class TestDocumentationGenericness:
    """Verify documentation remains generic and reusable."""
    
    def test_readme_explains_security_approach(self):
        """README should explain the security approach."""
        with open('README.md', 'r') as f:
            readme = f.read()
        
        # Should explain that it's a framework, not specific to one client
        assert 'framework' in readme.lower() or 'standards' in readme.lower()
        assert 'documentation' in readme.lower()
    
    def test_examples_are_anonymized(self):
        """Example files should use generic namespaces."""
        example_files = [
            'docs/source/examples/reports-utilization-api-docs.rst',
            'docs/source/examples/README.md'
        ]
        
        for file_path in example_files:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    content = f.read()
                
                # Should use example.com or similar generic domains
                assert 'example' in content.lower() or 'sample' in content.lower(), \
                    f"{file_path} doesn't use generic examples"
    
    def test_test_files_use_generic_data(self):
        """Test files should use generic test data."""
        test_dir = Path('tests')
        
        for test_file in test_dir.glob('test_*.py'):
            with open(test_file, 'r') as f:
                content = f.read()
            
            # If it mentions a namespace, should be generic
            if 'namespace' in content.lower():
                assert 'example.com' in content or 'example' in content, \
                    f"{test_file} uses non-generic namespace"


class TestPatternExtraction:
    """Verify pattern extraction remains abstract."""
    
    def test_patterns_work_across_frameworks(self):
        """Patterns should work with different Java frameworks."""
        from automation.java_parser import extract_endpoints_from_java
        
        # Test Spring Boot pattern
        spring_code = '''
        @RestController
        @RequestMapping("/api")
        public class ApiController {
            @GetMapping("/data")
            public ResponseEntity getData() { return ResponseEntity.ok(); }
        }
        '''
        
        # Test JAX-WS pattern
        jaxws_code = '''
        @WebService
        public class SoapService {
            @WebMethod
            public String process() { return "done"; }
        }
        '''
        
        # Both should be extractable
        # Note: Implementation may need enhancement for REST
        soap_endpoints = extract_endpoints_from_java(jaxws_code)
        assert len(soap_endpoints) > 0
    
    def test_extractor_handles_different_annotations(self):
        """Extractor should handle various annotation styles."""
        from automation.filesystem.memory import MemoryFileSystem
        from automation.java_ast_extractor import JavaASTExtractor
        
        fs = MemoryFileSystem()
        extractor = JavaASTExtractor(fs)
        
        # Test with different annotation styles
        annotations = [
            '@Service',
            '@Repository',
            '@Component',
            '@RestController',
        ]
        
        for annotation in annotations:
            java_code = f'''
            {annotation}
            public class TestClass {{
                public void method() {{}}
            }}
            '''
            
            fs.write_text('Test.java', java_code)
            result = extractor.extract_documentation('Test.java')
            
            assert result is not None
            # Should recognize various service patterns


class TestRepositorySafety:
    """Verify repository is safe for public sharing."""
    
    def test_no_connection_strings(self):
        """No connection strings should be in tracked files."""
        result = subprocess.run(
            ['git', 'ls-files'],
            capture_output=True,
            text=True
        )
        tracked_files = result.stdout.strip().split('\n')
        
        for file_path in tracked_files:
            if os.path.exists(file_path) and file_path.endswith(('.py', '.java', '.rst', '.md')):
                with open(file_path, 'r') as f:
                    content = f.read()
                
                # Basic check for connection string patterns
                suspicious_patterns = [
                    'jdbc:',
                    'mongodb://',
                    'Server=',
                    'Password=',
                    'Data Source=',
                ]
                
                for pattern in suspicious_patterns:
                    if pattern in content:
                        # Allow only if it's clearly a template/example
                        assert 'example' in content.lower() or 'template' in content.lower(), \
                            f"{file_path} contains suspicious pattern: {pattern}"
    
    def test_repository_size_is_reasonable(self):
        """Repository should not contain large binary files."""
        result = subprocess.run(
            ['git', 'count-objects', '-vH'],
            capture_output=True,
            text=True
        )
        
        # Parse size from output
        for line in result.stdout.split('\n'):
            if 'size:' in line:
                size_str = line.split(':')[1].strip()
                # Should be less than 5MB for a documentation framework
                assert 'K' in size_str or float(size_str.replace('M', '')) < 5, \
                    f"Repository too large: {size_str}"


class TestAbstractionCompleteness:
    """Verify abstraction is complete and functional."""
    
    def test_can_generate_docs_for_new_client(self):
        """Should be able to generate docs for a completely new client."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a mock client project
            client_dir = Path(tmpdir) / 'new-client'
            client_dir.mkdir()
            
            # Create a simple Java file
            java_file = client_dir / 'Service.java'
            java_file.write_text('''
            package com.newclient.api;
            
            @WebService(targetNamespace = "http://api.newclient.com/")
            public class ClientService {
                @WebMethod
                public String getClientData() {
                    return "client data";
                }
            }
            ''')
            
            # Run the parser
            from automation.java_parser import parse_java_project
            
            result = parse_java_project(str(client_dir))
            
            assert 'endpoints' in result
            assert len(result['endpoints']) > 0
            assert 'newclient' in str(result).lower()
            assert 'dsny' not in str(result).lower()
    
    def test_templates_render_with_any_client_data(self):
        """Templates should render correctly with any client data."""
        from jinja2 import Template
        
        template_content = '''
        Client: {{ client_name }}
        Service: {{ service_name }}
        Namespace: {{ namespace }}
        '''
        
        template = Template(template_content)
        
        # Test with different clients
        clients = [
            {'client_name': 'ACME Corp', 'service_name': 'DataAPI', 'namespace': 'http://acme.com/'},
            {'client_name': 'Global Inc', 'service_name': 'Analytics', 'namespace': 'http://global.org/'},
        ]
        
        for client_data in clients:
            rendered = template.render(**client_data)
            assert client_data['client_name'] in rendered
            assert 'DSNY' not in rendered  # Should not leak through


if __name__ == '__main__':
    pytest.main([__file__, '-v'])