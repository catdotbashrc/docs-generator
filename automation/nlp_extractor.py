"""
NLP-based business logic extraction for semantic understanding.
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

try:
    import spacy
    from spacy.matcher import Matcher
except ImportError:
    spacy = None
    Matcher = None

logger = logging.getLogger(__name__)

@dataclass
class AbstractPattern:
    """Represents an abstract business logic pattern."""
    pattern_type: str
    description: str
    domain_terms: List[str]
    abstract_concept: str
    confidence: float
    examples: Dict[str, str]

class BusinessLogicNLPExtractor:
    """Extracts abstract business logic patterns using NLP."""
    
    ABSTRACT_PATTERNS = {
        'THRESHOLD_DECISION': {
            'description': 'Decision based on numeric boundary',
            'indicators': ['if', 'when', 'check', 'exceeds', 'above', 'below', 'greater', 'less', 'threshold'],
            'examples': {
                'DSNY': 'if (overtime > 40) applyOvertimeRate()',
                'Healthcare': 'if (bloodPressure > 140) flagHighRisk()',
                'Finance': 'if (balance < 100) applyOverdraftFee()',
                'Logistics': 'if (distance > 50) assignAdditionalVehicle()'
            }
        },
        'VALIDATION_RULE': {
            'description': 'Input validation with business constraint',
            'indicators': ['validate', 'verify', 'check', 'confirm', 'ensure', 'valid', 'invalid'],
            'examples': {
                'DSNY': 'validateWorkOrder(order)',
                'Healthcare': 'validatePatientEligibility(patient)',
                'Finance': 'validateTransaction(payment)',
                'Logistics': 'validateShipmentContents(package)'
            }
        },
        'FILTERED_RETRIEVAL': {
            'description': 'Retrieve entities with constraints',
            'indicators': ['get', 'fetch', 'retrieve', 'find', 'query', 'search', 'filter', 'by', 'with'],
            'examples': {
                'DSNY': 'getWorkUnits(date, location)',
                'Healthcare': 'getAppointments(date, clinic)',
                'Finance': 'getTransactions(date, account)',
                'Logistics': 'getDeliveries(date, warehouse)'
            }
        },
        'CALCULATION_RULE': {
            'description': 'Business calculation or computation',
            'indicators': ['calculate', 'compute', 'total', 'sum', 'average', 'rate', 'percentage'],
            'examples': {
                'DSNY': 'calculateOvertimePay(hours, rate)',
                'Healthcare': 'calculateDosage(weight, age)',
                'Finance': 'calculateInterest(principal, rate)',
                'Logistics': 'calculateShippingCost(weight, distance)'
            }
        },
        'WORKFLOW_SEQUENCE': {
            'description': 'Sequential business process',
            'indicators': ['process', 'workflow', 'step', 'then', 'after', 'before', 'sequence', 'stage'],
            'examples': {
                'DSNY': 'submitWorkOrder() -> reviewWorkOrder() -> approveWorkOrder()',
                'Healthcare': 'registerPatient() -> triagePatient() -> assignDoctor()',
                'Finance': 'submitLoan() -> reviewCredit() -> approveLoan()',
                'Logistics': 'receivePackage() -> sortPackage() -> routePackage()'
            }
        }
    }
    
    def __init__(self, enable_nlp: bool = True):
        """Initialize the NLP extractor."""
        self.enable_nlp = enable_nlp
        self.nlp = None
        self.matcher = None
        
        if enable_nlp:
            try:
                if spacy is None:
                    raise ImportError("SpaCy not available")
                self.nlp = spacy.load("en_core_web_sm")
                self.matcher = Matcher(self.nlp.vocab)
                self._setup_matchers()
                logger.info("✅ NLP extractor initialized with SpaCy")
            except Exception as e:
                logger.warning(f"⚠️ NLP initialization failed: {e}. Falling back to basic extraction.")
                self.enable_nlp = False
    
    def _setup_matchers(self):
        """Setup SpaCy pattern matchers."""
        if not self.matcher:
            return
    
    def extract_patterns(self, code: str, context: Optional[str] = None) -> List[AbstractPattern]:
        """Extract abstract business logic patterns from code."""
        if not self.enable_nlp:
            return self._extract_patterns_basic(code, context)
        
        # NLP extraction would go here, but for now fallback to basic
        return self._extract_patterns_basic(code, context)
    
    def _extract_patterns_basic(self, code: str, context: Optional[str]) -> List[AbstractPattern]:
        """Basic pattern extraction without NLP (fallback)."""
        patterns = []
        text = f"{context or ''} {code}".lower()
        
        for pattern_type, pattern_def in self.ABSTRACT_PATTERNS.items():
            if any(indicator in text for indicator in pattern_def['indicators']):
                pattern = AbstractPattern(
                    pattern_type=pattern_type,
                    description=pattern_def['description'],
                    domain_terms=self._extract_domain_terms(text),
                    abstract_concept=pattern_type.lower().replace('_', ' '),
                    confidence=0.5,
                    examples=pattern_def['examples']
                )
                patterns.append(pattern)
        
        return patterns
    
    def _extract_domain_terms(self, text: str) -> List[str]:
        """Extract domain-specific terms from text."""
        common_terms = {'if', 'else', 'for', 'while', 'return', 'public', 'private', 
                       'void', 'int', 'string', 'boolean', 'class', 'interface', 'import'}
        
        words = text.split()
        domain_terms = []
        
        for word in words:
            word_clean = word.strip('(){}[].,;:').lower()
            if (len(word_clean) > 3 and 
                word_clean not in common_terms and 
                not word_clean.startswith('_') and
                word_clean.isalpha()):
                domain_terms.append(word_clean)
        
        return list(set(domain_terms))[:10]
    
    def enhance_soap_endpoint(self, endpoint_info: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance SOAP endpoint information with semantic understanding."""
        if not self.enable_nlp:
            # Still provide basic enhancement
            operation_name = endpoint_info.get('operation_name', '')
            method_code = endpoint_info.get('method_code', '')
            
            patterns = self.extract_patterns(method_code, operation_name)
            operation_type = self._classify_operation(operation_name, patterns)
            
            enhanced_params = []
            for param in endpoint_info.get('parameters', []):
                enhanced_params.append(self._enhance_parameter(param))
            
            endpoint_info['semantic_analysis'] = {
                'operation_type': operation_type,
                'abstract_patterns': [p.__dict__ for p in patterns],
                'enhanced_parameters': enhanced_params,
                'cross_domain_examples': self._generate_cross_domain_examples(operation_type)
            }
        
        return endpoint_info
    
    def _classify_operation(self, operation_name: str, patterns: List[AbstractPattern]) -> str:
        """Classify the operation type."""
        operation_lower = operation_name.lower()
        
        # Check patterns first
        if patterns:
            pattern_types = [p.pattern_type for p in patterns]
            if 'FILTERED_RETRIEVAL' in pattern_types:
                return 'QUERY'
            elif 'VALIDATION_RULE' in pattern_types:
                return 'VALIDATION'
            elif 'CALCULATION_RULE' in pattern_types:
                return 'CALCULATION'
            elif 'WORKFLOW_SEQUENCE' in pattern_types:
                return 'WORKFLOW'
        
        # Name-based classification
        if any(word in operation_lower for word in ['get', 'find', 'search', 'query', 'list', 'retrieve']):
            return 'QUERY'
        elif any(word in operation_lower for word in ['create', 'add', 'insert', 'new']):
            return 'CREATE'
        elif any(word in operation_lower for word in ['update', 'modify', 'change', 'set']):
            return 'UPDATE'
        elif any(word in operation_lower for word in ['delete', 'remove', 'destroy']):
            return 'DELETE'
        elif any(word in operation_lower for word in ['validate', 'verify', 'check', 'confirm']):
            return 'VALIDATION'
        elif any(word in operation_lower for word in ['calculate', 'compute', 'total']):
            return 'CALCULATION'
        elif any(word in operation_lower for word in ['process', 'execute', 'run', 'perform']):
            return 'WORKFLOW'
        else:
            return 'UNKNOWN'
    
    def _enhance_parameter(self, param: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance parameter with semantic understanding."""
        param_name = param.get('name', '').lower()
        
        semantic_type = 'UNKNOWN'
        purpose = 'General parameter'
        
        if any(word in param_name for word in ['date', 'time', 'when', 'timestamp', 'period']):
            semantic_type = 'TEMPORAL_CONSTRAINT'
            purpose = 'Filters or specifies time-based constraints'
        elif any(word in param_name for word in ['id', 'identifier', 'key', 'code', 'number']):
            semantic_type = 'IDENTIFIER'
            purpose = 'Uniquely identifies a specific entity'
        elif any(word in param_name for word in ['unit', 'department', 'division', 'group', 'team']):
            semantic_type = 'ORGANIZATIONAL_SCOPE'
            purpose = 'Limits scope to organizational boundaries'
        elif any(word in param_name for word in ['location', 'place', 'address', 'site', 'area']):
            semantic_type = 'SPATIAL_CONSTRAINT'
            purpose = 'Specifies geographical or spatial constraints'
        elif any(word in param_name for word in ['amount', 'quantity', 'count', 'total', 'number']):
            semantic_type = 'QUANTITATIVE_VALUE'
            purpose = 'Specifies numeric quantities or amounts'
        
        return {
            **param,
            'semantic_type': semantic_type,
            'purpose': purpose,
            'abstract_concept': semantic_type.lower().replace('_', ' ')
        }
    
    def _generate_cross_domain_examples(self, operation_type: str) -> Dict[str, str]:
        """Generate cross-domain examples for an operation."""
        examples = {
            'QUERY': {
                'Healthcare': 'getAvailableAppointments',
                'Finance': 'getAccountTransactions',
                'Logistics': 'getShipmentStatus',
                'Education': 'getStudentRecords'
            },
            'VALIDATION': {
                'Healthcare': 'validatePatientInsurance',
                'Finance': 'validatePaymentMethod',
                'Logistics': 'validateDeliveryAddress',
                'Education': 'validateEnrollmentEligibility'
            },
            'CALCULATION': {
                'Healthcare': 'calculateTreatmentCost',
                'Finance': 'calculateLoanInterest',
                'Logistics': 'calculateShippingFee',
                'Education': 'calculateGradeAverage'
            },
            'WORKFLOW': {
                'Healthcare': 'processPatientAdmission',
                'Finance': 'processLoanApplication',
                'Logistics': 'processShipmentReturn',
                'Education': 'processCourseRegistration'
            }
        }
        
        return examples.get(operation_type, {})