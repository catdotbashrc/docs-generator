"""
Unit tests for artifact-based documentation coverage
"""

import pytest
import tempfile
from pathlib import Path
from ddd.artifact_extractors import (
    CodeArtifact,
    ArtifactCoverageResult,
    PythonArtifactExtractor,
    JavaScriptArtifactExtractor,
    ArtifactCoverageCalculator
)


class TestCodeArtifact:
    """Test CodeArtifact dataclass"""
    
    def test_artifact_creation(self):
        """Test creating a CodeArtifact"""
        artifact = CodeArtifact(
            name="test_function",
            type="function",
            file_path="/path/to/file.py",
            line_number=10,
            signature="test_function(arg1, arg2)",
            is_documented=True,
            documentation="Test function documentation",
            is_public=True,
            parent=None
        )
        
        assert artifact.name == "test_function"
        assert artifact.type == "function"
        assert artifact.line_number == 10
        assert artifact.is_documented is True
        assert artifact.is_public is True
    
    def test_artifact_with_parent(self):
        """Test artifact with parent class"""
        artifact = CodeArtifact(
            name="method",
            type="method",
            file_path="/path/to/file.py",
            line_number=20,
            parent="TestClass"
        )
        
        assert artifact.parent == "TestClass"


class TestArtifactCoverageResult:
    """Test ArtifactCoverageResult dataclass"""
    
    def test_coverage_result_creation(self):
        """Test creating coverage result"""
        result = ArtifactCoverageResult(
            total_artifacts=100,
            documented_artifacts=85,
            coverage_percentage=85.0,
            artifacts_by_type={},
            undocumented_artifacts=[]
        )
        
        assert result.total_artifacts == 100
        assert result.documented_artifacts == 85
        assert result.coverage_percentage == 85.0
        assert result.passed is True
    
    def test_coverage_result_failed(self):
        """Test failed coverage result"""
        result = ArtifactCoverageResult(
            total_artifacts=100,
            documented_artifacts=50,
            coverage_percentage=50.0,
            artifacts_by_type={},
            undocumented_artifacts=[]
        )
        
        assert result.passed is False


class TestPythonArtifactExtractor:
    """Test PythonArtifactExtractor"""
    
    @pytest.fixture
    def extractor(self):
        """Create a PythonArtifactExtractor instance"""
        return PythonArtifactExtractor()
    
    @pytest.fixture
    def temp_python_file(self):
        """Create a temporary Python file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('''
"""Module docstring"""

def documented_function(arg1, arg2):
    """This function has a docstring"""
    return arg1 + arg2

def undocumented_function(x):
    return x * 2

class DocumentedClass:
    """This class has a docstring"""
    
    def __init__(self):
        """Constructor with docstring"""
        pass
    
    def documented_method(self):
        """Method with docstring"""
        pass
    
    def undocumented_method(self):
        return None
    
    def _private_method(self):
        """Private method"""
        pass

class UndocumentedClass:
    def method(self):
        pass

# This is a constant
CONSTANT_VALUE = 42

UNDOCUMENTED_CONSTANT = 100
''')
            temp_path = Path(f.name)
        
        yield temp_path
        temp_path.unlink()  # Clean up
    
    def test_extract_python_functions(self, extractor, temp_python_file):
        """Test extracting Python functions"""
        artifacts = extractor.extract_artifacts(temp_python_file)
        
        # Find function artifacts
        functions = [a for a in artifacts if a.type == 'function']
        func_names = [f.name for f in functions]
        
        assert 'documented_function' in func_names
        assert 'undocumented_function' in func_names
        
        # Check documentation status
        doc_func = next(f for f in functions if f.name == 'documented_function')
        assert doc_func.is_documented is True
        assert doc_func.documentation is not None
        
        undoc_func = next(f for f in functions if f.name == 'undocumented_function')
        assert undoc_func.is_documented is False
    
    def test_extract_python_classes(self, extractor, temp_python_file):
        """Test extracting Python classes"""
        artifacts = extractor.extract_artifacts(temp_python_file)
        
        # Find class artifacts
        classes = [a for a in artifacts if a.type == 'class']
        class_names = [c.name for c in classes]
        
        assert 'DocumentedClass' in class_names
        assert 'UndocumentedClass' in class_names
        
        # Check documentation
        doc_class = next(c for c in classes if c.name == 'DocumentedClass')
        assert doc_class.is_documented is True
        
        undoc_class = next(c for c in classes if c.name == 'UndocumentedClass')
        assert undoc_class.is_documented is False
    
    def test_extract_python_methods(self, extractor, temp_python_file):
        """Test extracting Python methods"""
        artifacts = extractor.extract_artifacts(temp_python_file)
        
        # Find method artifacts
        methods = [a for a in artifacts if a.type == 'method']
        
        # Check __init__ method
        init_methods = [m for m in methods if m.name == '__init__']
        assert len(init_methods) > 0
        assert init_methods[0].is_documented is True
        
        # Check parent association
        doc_method = next((m for m in methods if m.name == 'documented_method'), None)
        assert doc_method is not None
        assert doc_method.parent == 'DocumentedClass'
        assert doc_method.is_documented is True
    
    def test_extract_python_constants(self, extractor, temp_python_file):
        """Test extracting Python constants"""
        artifacts = extractor.extract_artifacts(temp_python_file)
        
        # Find constant artifacts
        constants = [a for a in artifacts if a.type == 'constant']
        const_names = [c.name for c in constants]
        
        assert 'CONSTANT_VALUE' in const_names
        assert 'UNDOCUMENTED_CONSTANT' in const_names
        
        # Check documentation (via comment)
        doc_const = next(c for c in constants if c.name == 'CONSTANT_VALUE')
        assert doc_const.is_documented is True  # Has preceding comment
    
    def test_should_document(self, extractor):
        """Test should_document logic"""
        # Public function should be documented
        public_func = CodeArtifact(
            name="public_function",
            type="function",
            file_path="/src/module.py",
            line_number=1
        )
        assert extractor.should_document(public_func) is True
        
        # Private function should not be documented
        private_func = CodeArtifact(
            name="_private_function",
            type="function",
            file_path="/src/module.py",
            line_number=1
        )
        assert extractor.should_document(private_func) is False
        
        # Test file should not be documented
        test_func = CodeArtifact(
            name="test_function",
            type="function",
            file_path="/tests/test_module.py",
            line_number=1
        )
        assert extractor.should_document(test_func) is False


class TestJavaScriptArtifactExtractor:
    """Test JavaScriptArtifactExtractor"""
    
    @pytest.fixture
    def extractor(self):
        """Create a JavaScriptArtifactExtractor instance"""
        return JavaScriptArtifactExtractor()
    
    @pytest.fixture
    def temp_js_file(self):
        """Create a temporary JavaScript file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write('''
/**
 * Documented function with JSDoc
 * @param {string} name - The name
 * @returns {string} The greeting
 */
function documentedFunction(name) {
    return `Hello, ${name}!`;
}

// Regular comment
function commentedFunction() {
    return true;
}

function undocumentedFunction() {
    return false;
}

/**
 * Documented class
 */
class DocumentedClass {
    constructor() {
        this.value = 0;
    }
    
    /**
     * Documented method
     */
    documentedMethod() {
        return this.value;
    }
    
    undocumentedMethod() {
        return null;
    }
}

class UndocumentedClass {
    method() {
        return 42;
    }
}

// Arrow function with comment
const arrowFunction = (x) => x * 2;

const undocumentedArrow = async (y) => {
    return y + 1;
};

// Exported constant
export const API_KEY = 'secret';

export const UNDOCUMENTED_CONST = 100;

const obj = {
    // Object method
    objectMethod: function(z) {
        return z;
    }
};
''')
            temp_path = Path(f.name)
        
        yield temp_path
        temp_path.unlink()  # Clean up
    
    def test_extract_javascript_functions(self, extractor, temp_js_file):
        """Test extracting JavaScript functions"""
        artifacts = extractor.extract_artifacts(temp_js_file)
        
        # Find function artifacts
        functions = [a for a in artifacts if a.type == 'function']
        func_names = [f.name for f in functions]
        
        assert 'documentedFunction' in func_names
        assert 'commentedFunction' in func_names
        assert 'undocumentedFunction' in func_names
        assert 'arrowFunction' in func_names
        assert 'undocumentedArrow' in func_names
        
        # Check JSDoc documentation
        doc_func = next(f for f in functions if f.name == 'documentedFunction')
        assert doc_func.is_documented is True
        
        # Check comment documentation
        comment_func = next(f for f in functions if f.name == 'commentedFunction')
        assert comment_func.is_documented is True
        
        # Check undocumented
        undoc_func = next(f for f in functions if f.name == 'undocumentedFunction')
        assert undoc_func.is_documented is False
    
    def test_extract_javascript_classes(self, extractor, temp_js_file):
        """Test extracting JavaScript classes"""
        artifacts = extractor.extract_artifacts(temp_js_file)
        
        # Find class artifacts
        classes = [a for a in artifacts if a.type == 'class']
        class_names = [c.name for c in classes]
        
        assert 'DocumentedClass' in class_names
        assert 'UndocumentedClass' in class_names
        
        # Check documentation
        doc_class = next(c for c in classes if c.name == 'DocumentedClass')
        assert doc_class.is_documented is True
        
        undoc_class = next(c for c in classes if c.name == 'UndocumentedClass')
        assert undoc_class.is_documented is False
    
    def test_extract_javascript_constants(self, extractor, temp_js_file):
        """Test extracting JavaScript constants"""
        artifacts = extractor.extract_artifacts(temp_js_file)
        
        # Find constant artifacts
        constants = [a for a in artifacts if a.type == 'constant']
        const_names = [c.name for c in constants]
        
        assert 'API_KEY' in const_names
        assert 'UNDOCUMENTED_CONST' in const_names
        
        # Check documentation
        doc_const = next(c for c in constants if c.name == 'API_KEY')
        assert doc_const.is_documented is True
    
    def test_extract_object_methods(self, extractor, temp_js_file):
        """Test extracting object methods"""
        artifacts = extractor.extract_artifacts(temp_js_file)
        
        # Find method artifacts
        methods = [a for a in artifacts if a.type == 'method']
        method_names = [m.name for m in methods]
        
        assert 'objectMethod' in method_names


class TestArtifactCoverageCalculator:
    """Test ArtifactCoverageCalculator"""
    
    @pytest.fixture
    def calculator(self):
        """Create an ArtifactCoverageCalculator instance"""
        return ArtifactCoverageCalculator()
    
    @pytest.fixture
    def temp_project(self):
        """Create a temporary project with mixed files"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            
            # Create Python file
            py_file = project_path / "module.py"
            py_file.write_text('''
def documented_func():
    """Has docstring"""
    pass

def undocumented_func():
    pass

class TestClass:
    """Test class"""
    pass
''')
            
            # Create JavaScript file
            js_file = project_path / "script.js"
            js_file.write_text('''
/**
 * JSDoc comment
 */
function documentedJS() {
    return true;
}

function undocumentedJS() {
    return false;
}
''')
            
            # Create test file (should be excluded)
            test_file = project_path / "test_module.py"
            test_file.write_text('''
def test_something():
    pass
''')
            
            yield project_path
    
    def test_calculate_coverage(self, calculator, temp_project):
        """Test calculating coverage for a project"""
        result = calculator.calculate_coverage(str(temp_project))
        
        assert isinstance(result, ArtifactCoverageResult)
        assert result.total_artifacts > 0
        assert result.documented_artifacts >= 0
        assert 0 <= result.coverage_percentage <= 100
        
        # Check artifacts by type
        assert 'function' in result.artifacts_by_type or 'method' in result.artifacts_by_type
        assert len(result.artifacts_by_type) > 0
    
    def test_generate_report(self, calculator, temp_project):
        """Test generating a coverage report"""
        result = calculator.calculate_coverage(str(temp_project))
        report = calculator.generate_report(result)
        
        assert "Artifact-Based Documentation Coverage Report" in report
        assert "Overall Coverage:" in report
        assert "Total Artifacts:" in report
        
        if result.passed:
            assert "✅ PASSED" in report
        else:
            assert "❌ FAILED" in report
        
        # Check for artifact type breakdown
        assert "Coverage by Artifact Type:" in report
    
    def test_skip_node_modules(self, calculator):
        """Test that node_modules is skipped"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            
            # Create node_modules directory
            node_modules = project_path / "node_modules"
            node_modules.mkdir()
            
            # Create file in node_modules (should be skipped)
            (node_modules / "lib.js").write_text('function skip() {}')
            
            # Create file outside node_modules
            (project_path / "app.js").write_text('function include() {}')
            
            result = calculator.calculate_coverage(str(project_path))
            
            # Should only find the function outside node_modules
            all_artifacts = []
            for artifacts in result.artifacts_by_type.values():
                all_artifacts.extend(artifacts)
            
            artifact_names = [a.name for a in all_artifacts]
            assert 'include' in artifact_names
            assert 'skip' not in artifact_names