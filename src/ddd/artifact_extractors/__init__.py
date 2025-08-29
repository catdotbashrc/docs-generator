"""
Artifact-based documentation coverage system.
Counts actual code artifacts (functions, classes, etc.) and measures how many are documented.
"""

import ast
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set
from abc import ABC, abstractmethod


@dataclass
class CodeArtifact:
    """Represents a documentable unit in code"""
    name: str
    type: str  # 'function', 'class', 'method', 'variable', 'constant', etc.
    file_path: str
    line_number: int
    signature: Optional[str] = None
    is_documented: bool = False
    documentation: Optional[str] = None
    is_public: bool = True  # Public API vs internal implementation
    parent: Optional[str] = None  # For methods, the parent class


@dataclass
class ArtifactCoverageResult:
    """Coverage result based on artifact documentation"""
    total_artifacts: int
    documented_artifacts: int
    coverage_percentage: float
    artifacts_by_type: Dict[str, List[CodeArtifact]] = field(default_factory=dict)
    undocumented_artifacts: List[CodeArtifact] = field(default_factory=list)
    
    @property
    def passed(self) -> bool:
        """Check if coverage meets minimum threshold"""
        return self.coverage_percentage >= 85.0


class BaseArtifactExtractor(ABC):
    """Base class for extracting code artifacts from source files"""
    
    @abstractmethod
    def extract_artifacts(self, file_path: Path) -> List[CodeArtifact]:
        """Extract all documentable artifacts from a file"""
        pass
    
    @abstractmethod
    def check_documentation(self, artifact: CodeArtifact, file_content: str) -> bool:
        """Check if an artifact is documented"""
        pass
    
    def should_document(self, artifact: CodeArtifact) -> bool:
        """Determine if an artifact should be documented"""
        # Skip private/internal items by default
        if artifact.name.startswith('_') and not artifact.name.startswith('__init__'):
            return False
        
        # Skip test files
        if 'test_' in artifact.file_path or '_test.' in artifact.file_path:
            return False
            
        return artifact.is_public


class PythonArtifactExtractor(BaseArtifactExtractor):
    """Extract artifacts from Python source files"""
    
    def extract_artifacts(self, file_path: Path) -> List[CodeArtifact]:
        """Extract all Python artifacts from a file"""
        artifacts = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
                tree = ast.parse(file_content)
            
            # Extract module-level artifacts
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    artifact = CodeArtifact(
                        name=node.name,
                        type='function',
                        file_path=str(file_path),
                        line_number=node.lineno,
                        signature=self._get_function_signature(node),
                        is_documented=self._has_docstring(node),
                        documentation=ast.get_docstring(node),
                        is_public=not node.name.startswith('_')
                    )
                    artifacts.append(artifact)
                    
                elif isinstance(node, ast.ClassDef):
                    # Add class artifact
                    class_artifact = CodeArtifact(
                        name=node.name,
                        type='class',
                        file_path=str(file_path),
                        line_number=node.lineno,
                        is_documented=self._has_docstring(node),
                        documentation=ast.get_docstring(node),
                        is_public=not node.name.startswith('_')
                    )
                    artifacts.append(class_artifact)
                    
                    # Add method artifacts
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            method_artifact = CodeArtifact(
                                name=item.name,
                                type='method',
                                file_path=str(file_path),
                                line_number=item.lineno,
                                signature=self._get_function_signature(item),
                                is_documented=self._has_docstring(item),
                                documentation=ast.get_docstring(item),
                                is_public=not item.name.startswith('_'),
                                parent=node.name
                            )
                            artifacts.append(method_artifact)
                            
                elif isinstance(node, ast.Assign):
                    # Module-level constants (UPPER_CASE variables)
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id.isupper():
                            artifacts.append(CodeArtifact(
                                name=target.id,
                                type='constant',
                                file_path=str(file_path),
                                line_number=node.lineno,
                                is_documented=self._has_comment_doc(file_content, node.lineno)
                            ))
                            
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            
        return artifacts
    
    def _has_docstring(self, node) -> bool:
        """Check if a node has a docstring"""
        return ast.get_docstring(node) is not None
    
    def _has_comment_doc(self, file_content: str, line_number: int) -> bool:
        """Check if a line has an inline or preceding comment"""
        lines = file_content.split('\n')
        if line_number > 0 and line_number <= len(lines):
            # Check current line for inline comment
            if '#' in lines[line_number - 1]:
                return True
            # Check previous line for comment
            if line_number > 1 and lines[line_number - 2].strip().startswith('#'):
                return True
        return False
    
    def _get_function_signature(self, node: ast.FunctionDef) -> str:
        """Extract function signature"""
        args = []
        for arg in node.args.args:
            args.append(arg.arg)
        return f"{node.name}({', '.join(args)})"
    
    def check_documentation(self, artifact: CodeArtifact, file_content: str) -> bool:
        """Check if artifact is documented (already done during extraction)"""
        return artifact.is_documented


class JavaScriptArtifactExtractor(BaseArtifactExtractor):
    """Extract artifacts from JavaScript source files"""
    
    def extract_artifacts(self, file_path: Path) -> List[CodeArtifact]:
        """Extract JavaScript artifacts using regex patterns"""
        artifacts = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Function patterns
            function_patterns = [
                (r'function\s+(\w+)\s*\([^)]*\)', 'function'),  # function declarations
                (r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>', 'function'),  # arrow functions
                (r'const\s+(\w+)\s*=\s*async\s*\([^)]*\)\s*=>', 'function'),  # async arrow
                (r'(\w+)\s*:\s*function\s*\([^)]*\)', 'method'),  # object methods
            ]
            
            # Class pattern
            class_pattern = r'class\s+(\w+)'
            
            # Check each pattern
            for line_no, line in enumerate(lines, 1):
                # Check for classes
                class_match = re.search(class_pattern, line)
                if class_match:
                    artifacts.append(CodeArtifact(
                        name=class_match.group(1),
                        type='class',
                        file_path=str(file_path),
                        line_number=line_no,
                        is_documented=self._has_jsdoc(lines, line_no - 1)
                    ))
                
                # Check for functions
                for pattern, artifact_type in function_patterns:
                    matches = re.finditer(pattern, line)
                    for match in matches:
                        artifacts.append(CodeArtifact(
                            name=match.group(1),
                            type=artifact_type,
                            file_path=str(file_path),
                            line_number=line_no,
                            is_documented=self._has_jsdoc(lines, line_no - 1) or self._has_comment(lines, line_no - 1)
                        ))
                
                # Check for exported constants
                const_match = re.match(r'export\s+const\s+([A-Z_]+)\s*=', line)
                if const_match:
                    artifacts.append(CodeArtifact(
                        name=const_match.group(1),
                        type='constant',
                        file_path=str(file_path),
                        line_number=line_no,
                        is_documented=self._has_comment(lines, line_no - 1)
                    ))
                    
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            
        return artifacts
    
    def _has_jsdoc(self, lines: List[str], line_index: int) -> bool:
        """Check if line has JSDoc comment above it"""
        if line_index < 0:
            return False
            
        # Look for JSDoc pattern /** ... */
        for i in range(max(0, line_index - 10), line_index + 1):
            if '/**' in lines[i]:
                return True
        return False
    
    def _has_comment(self, lines: List[str], line_index: int) -> bool:
        """Check for regular comments"""
        if line_index >= 0 and line_index < len(lines):
            line = lines[line_index].strip()
            return line.startswith('//') or line.startswith('/*')
        return False
    
    def check_documentation(self, artifact: CodeArtifact, file_content: str) -> bool:
        """Check if artifact is documented"""
        return artifact.is_documented


class ArtifactCoverageCalculator:
    """Calculate documentation coverage based on code artifacts"""
    
    def __init__(self):
        self.extractors = {
            '.py': PythonArtifactExtractor(),
            '.js': JavaScriptArtifactExtractor(),
            '.jsx': JavaScriptArtifactExtractor(),
            '.ts': JavaScriptArtifactExtractor(),
            '.tsx': JavaScriptArtifactExtractor(),
        }
    
    def calculate_coverage(self, project_path: str) -> ArtifactCoverageResult:
        """Calculate artifact-based documentation coverage for a project"""
        path = Path(project_path)
        all_artifacts = []
        
        # Find all source files
        for ext, extractor in self.extractors.items():
            for file_path in path.rglob(f'*{ext}'):
                # Skip node_modules, venv, etc.
                if any(skip in str(file_path) for skip in ['node_modules', 'venv', '.venv', '__pycache__', 'dist', 'build']):
                    continue
                    
                artifacts = extractor.extract_artifacts(file_path)
                # Filter to only artifacts that should be documented
                artifacts = [a for a in artifacts if extractor.should_document(a)]
                all_artifacts.extend(artifacts)
        
        # Calculate coverage
        total = len(all_artifacts)
        documented = sum(1 for a in all_artifacts if a.is_documented)
        coverage = (documented / total * 100) if total > 0 else 0.0
        
        # Group by type
        artifacts_by_type = {}
        for artifact in all_artifacts:
            if artifact.type not in artifacts_by_type:
                artifacts_by_type[artifact.type] = []
            artifacts_by_type[artifact.type].append(artifact)
        
        # Find undocumented artifacts
        undocumented = [a for a in all_artifacts if not a.is_documented]
        
        return ArtifactCoverageResult(
            total_artifacts=total,
            documented_artifacts=documented,
            coverage_percentage=coverage,
            artifacts_by_type=artifacts_by_type,
            undocumented_artifacts=undocumented
        )
    
    def generate_report(self, result: ArtifactCoverageResult) -> str:
        """Generate a human-readable coverage report"""
        report = []
        report.append(f"📊 Artifact-Based Documentation Coverage Report")
        report.append(f"{'=' * 50}")
        report.append(f"Overall Coverage: {result.coverage_percentage:.1f}%")
        report.append(f"Total Artifacts: {result.total_artifacts}")
        report.append(f"Documented: {result.documented_artifacts}")
        report.append(f"Status: {'✅ PASSED' if result.passed else '❌ FAILED'}")
        report.append("")
        
        # Coverage by type
        report.append("Coverage by Artifact Type:")
        report.append("-" * 30)
        for artifact_type, artifacts in result.artifacts_by_type.items():
            documented = sum(1 for a in artifacts if a.is_documented)
            total = len(artifacts)
            percentage = (documented / total * 100) if total > 0 else 0
            report.append(f"  {artifact_type.capitalize()}: {documented}/{total} ({percentage:.1f}%)")
        
        # List undocumented items
        if result.undocumented_artifacts:
            report.append("")
            report.append("Top Undocumented Artifacts (showing first 10):")
            report.append("-" * 30)
            for artifact in result.undocumented_artifacts[:10]:
                location = f"{artifact.file_path}:{artifact.line_number}"
                report.append(f"  ❌ {artifact.type}: {artifact.name} ({location})")
        
        return "\n".join(report)