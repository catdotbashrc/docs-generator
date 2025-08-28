"""
Documentation Specifications
Define what complete documentation looks like
"""

from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class DimensionSpec:
    """Specification for a single DAYLIGHT dimension"""
    
    name: str
    required_elements: List[str]
    required_fields: Dict[str, List[str]]
    minimum_coverage: float = 0.85
    weight: float = 1.0
    
    def validate(self, extracted_data: Dict) -> tuple[float, List[str]]:
        """
        Validate extracted data against this specification.
        Returns (coverage_score, missing_elements)
        """
        if not extracted_data:
            return 0.0, self.required_elements
        
        missing = []
        found_count = 0
        
        for element in self.required_elements:
            if element in extracted_data and extracted_data[element]:
                found_count += 1
            else:
                missing.append(element)
        
        coverage = found_count / len(self.required_elements) if self.required_elements else 0
        return coverage, missing


class DAYLIGHTSpec:
    """Complete DAYLIGHT documentation specification"""
    
    def __init__(self):
        self.dimensions = {
            'dependencies': DimensionSpec(
                name='dependencies',
                required_elements=[
                    'runtime_dependencies',
                    'node_version',
                    'package_manager',
                    'lock_file'
                ],
                required_fields={
                    'dependency': ['name', 'version', 'purpose', 'failure_impact']
                },
                minimum_coverage=0.90,
                weight=0.15
            ),
            'automation': DimensionSpec(
                name='automation',
                required_elements=[
                    'npm_scripts',
                    'ci_cd_workflows',
                    'git_hooks'
                ],
                required_fields={
                    'script': ['command', 'purpose', 'when_to_run', 'failure_handling']
                },
                minimum_coverage=0.85,
                weight=0.12
            ),
            'yearbook': DimensionSpec(
                name='yearbook',
                required_elements=[
                    'changelog',
                    'git_history',
                    'contributors'
                ],
                required_fields={},
                minimum_coverage=0.80,
                weight=0.08
            ),
            'lifecycle': DimensionSpec(
                name='lifecycle',
                required_elements=[
                    'environments',
                    'deployment_process',
                    'configuration_files'
                ],
                required_fields={
                    'environment': ['name', 'purpose', 'configuration']
                },
                minimum_coverage=0.85,
                weight=0.13
            ),
            'integration': DimensionSpec(
                name='integration',
                required_elements=[
                    'api_endpoints',
                    'external_services',
                    'webhooks'
                ],
                required_fields={
                    'endpoint': ['url', 'method', 'purpose', 'authentication']
                },
                minimum_coverage=0.90,
                weight=0.15
            ),
            'governance': DimensionSpec(
                name='governance',
                required_elements=[
                    'code_standards',
                    'review_process',
                    'security_policies'
                ],
                required_fields={},
                minimum_coverage=0.95,
                weight=0.10
            ),
            'health': DimensionSpec(
                name='health',
                required_elements=[
                    'test_coverage',
                    'performance_baseline',
                    'monitoring_setup'
                ],
                required_fields={},
                minimum_coverage=0.85,
                weight=0.12
            ),
            'testing': DimensionSpec(
                name='testing',
                required_elements=[
                    'test_structure',
                    'test_commands',
                    'coverage_reports'
                ],
                required_fields={},
                minimum_coverage=0.90,
                weight=0.15
            )
        }
    
    def get_dimension(self, name: str) -> Optional[DimensionSpec]:
        """Get specification for a specific dimension"""
        return self.dimensions.get(name)