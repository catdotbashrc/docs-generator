"""
Documentation Coverage Measurement
The core of DDD - measuring documentation completeness
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from ..specs import DAYLIGHTSpec, DimensionSpec


@dataclass
class CoverageResult:
    """Result of documentation coverage measurement"""
    
    overall_coverage: float
    passed: bool
    dimension_scores: Dict[str, float]
    missing_elements: Dict[str, List[str]]
    recommendations: List[str]
    
    def __str__(self) -> str:
        status = "✅ PASSED" if self.passed else "❌ FAILED"
        return f"{status} - Overall Coverage: {self.overall_coverage:.1%}"


class DocumentationCoverage:
    """
    Documentation Coverage Calculator
    The equivalent of code coverage for documentation
    """
    
    def __init__(self, spec: Optional[DAYLIGHTSpec] = None):
        self.spec = spec or DAYLIGHTSpec()
        
    def measure(self, extracted_docs: Dict) -> CoverageResult:
        """
        Measure documentation coverage against specification.
        This is the core DDD operation - like running tests in TDD.
        """
        dimension_scores = {}
        missing_elements = {}
        recommendations = []
        
        # Calculate coverage for each dimension
        for dim_name, dim_spec in self.spec.dimensions.items():
            dim_data = extracted_docs.get(dim_name, {})
            
            # Level 1: Element Coverage
            element_coverage = self._calculate_element_coverage(dim_spec, dim_data)
            
            # Level 2: Completeness Coverage
            completeness_coverage = self._calculate_completeness_coverage(dim_spec, dim_data)
            
            # Level 3: Usefulness Coverage (simplified for MVP)
            usefulness_coverage = self._calculate_usefulness_coverage(dim_spec, dim_data)
            
            # Weighted average for dimension
            dimension_score = (
                element_coverage * 0.3 +
                completeness_coverage * 0.4 +
                usefulness_coverage * 0.3
            )
            
            dimension_scores[dim_name] = dimension_score
            
            # Track what's missing
            coverage, missing = dim_spec.validate(dim_data)
            if missing:
                missing_elements[dim_name] = missing
                recommendations.append(f"Add documentation for {dim_name}: {', '.join(missing)}")
        
        # Calculate overall coverage with weights
        overall_coverage = sum(
            dimension_scores.get(dim, 0) * spec.weight 
            for dim, spec in self.spec.dimensions.items()
        )
        
        # Determine pass/fail
        passed = overall_coverage >= 0.85  # Default threshold
        
        return CoverageResult(
            overall_coverage=overall_coverage,
            passed=passed,
            dimension_scores=dimension_scores,
            missing_elements=missing_elements,
            recommendations=recommendations
        )
    
    def _calculate_element_coverage(self, spec: DimensionSpec, data: Dict) -> float:
        """Level 1: Does the documentation exist?"""
        if not data:
            return 0.0
            
        found = sum(1 for elem in spec.required_elements if elem in data and data[elem])
        total = len(spec.required_elements)
        
        return found / total if total > 0 else 0.0
    
    def _calculate_completeness_coverage(self, spec: DimensionSpec, data: Dict) -> float:
        """Level 2: Are all required fields present?"""
        if not data or not spec.required_fields:
            return 1.0 if not spec.required_fields else 0.0
        
        total_fields = 0
        found_fields = 0
        
        for item_type, required_fields in spec.required_fields.items():
            # Check if we have any items of this type
            items = data.get(item_type + 's', []) or data.get(item_type, [])
            if not items:
                continue
                
            for item in items if isinstance(items, list) else [items]:
                for field in required_fields:
                    total_fields += 1
                    if field in item:
                        found_fields += 1
        
        return found_fields / total_fields if total_fields > 0 else 0.5
    
    def _calculate_usefulness_coverage(self, spec: DimensionSpec, data: Dict) -> float:
        """Level 3: Can someone use this at 2AM?"""
        # Simplified for MVP - check for key usefulness indicators
        usefulness_indicators = {
            'dependencies': ['failure_impact', 'recovery_procedure'],
            'automation': ['failure_handling', 'purpose'],
            'integration': ['authentication', 'error_handling'],
            'lifecycle': ['rollback_procedure', 'deployment_steps']
        }
        
        indicators = usefulness_indicators.get(spec.name, [])
        if not indicators:
            return 1.0  # No specific usefulness criteria
            
        found = 0
        for indicator in indicators:
            if self._has_indicator(data, indicator):
                found += 1
                
        return found / len(indicators) if indicators else 1.0
    
    def _has_indicator(self, data: Dict, indicator: str) -> bool:
        """Check if data contains a usefulness indicator"""
        if indicator in data:
            return True
            
        # Check nested structures
        for key, value in data.items():
            if isinstance(value, dict) and indicator in value:
                return True
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict) and indicator in item:
                        return True
                        
        return False
    
    def assert_coverage(self, extracted_docs: Dict, minimum: float = 0.85):
        """
        Assert that documentation coverage meets minimum threshold.
        This is the DDD equivalent of test assertions.
        """
        result = self.measure(extracted_docs)
        
        if result.overall_coverage < minimum:
            raise AssertionError(
                f"Documentation coverage {result.overall_coverage:.1%} "
                f"below minimum {minimum:.1%}\n"
                f"Missing: {result.missing_elements}"
            )