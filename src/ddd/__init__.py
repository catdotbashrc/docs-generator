"""
Documentation Driven Development Framework
TDD for documentation coverage
"""

__version__ = "0.1.0"

from .coverage import DocumentationCoverage, CoverageResult
from .specs import DAYLIGHTSpec, DimensionSpec
from .extractors import DependencyExtractor

__all__ = [
    "DocumentationCoverage",
    "CoverageResult",
    "DAYLIGHTSpec",
    "DimensionSpec",
    "DependencyExtractor",
]