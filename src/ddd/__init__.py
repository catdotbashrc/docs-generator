"""
Documentation Driven Development Framework
TDD for documentation coverage
"""

__version__ = "0.1.0"

from .coverage import CoverageResult, DocumentationCoverage
from .extractors import DependencyExtractor
from .specs import DAYLIGHTSpec, DimensionSpec

__all__ = [
    "DocumentationCoverage",
    "CoverageResult",
    "DAYLIGHTSpec",
    "DimensionSpec",
    "DependencyExtractor",
]
