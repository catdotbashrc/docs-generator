# SpaCy Integration Design for Semantic Analysis

## Executive Summary

This document outlines the design for integrating SpaCy NLP capabilities into the Infrastructure Documentation Standards system to extract semantic meaning from business logic and API documentation, enabling abstract pattern recognition across different enterprise domains.

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Input Layer                               │
├────────────────┬────────────────┬────────────────┬──────────────┤
│   Java AST     │   SOAP WSDL     │  REST OpenAPI  │  SQL Schema │
│   Extractor    │    Parser        │    Parser      │   Parser    │
└────────┬───────┴────────┬────────┴────────┬───────┴──────┬───────┘
         │                 │                 │               │
         v                 v                 v               v
┌─────────────────────────────────────────────────────────────────┐
│                    NLP Processing Pipeline                       │
├───────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────┐        │
│  │ Tokenization │→ │ POS Tagging  │→ │ Named Entity   │        │
│  │              │  │              │  │ Recognition    │        │
│  └──────────────┘  └──────────────┘  └────────────────┘        │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────┐        │
│  │ Dependency   │→ │ Pattern      │→ │ Semantic       │        │
│  │ Parsing      │  │ Matching     │  │ Analysis       │        │
│  └──────────────┘  └──────────────┘  └────────────────┘        │
└─────────────────────────────┬───────────────────────────────────┘
                              v
┌─────────────────────────────────────────────────────────────────┐
│                 Pattern Abstraction Layer                        │
├───────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────┐        │
│  │ Business     │  │ Cross-Domain │  │ Pattern        │        │
│  │ Logic Maps   │  │ Translation  │  │ Library        │        │
│  └──────────────┘  └──────────────┘  └────────────────┘        │
└─────────────────────────────┬───────────────────────────────────┘
                              v
┌─────────────────────────────────────────────────────────────────┐
│                    Documentation Generation                      │
├───────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────┐        │
│  │ Template     │  │ Cross-Domain │  │ Sphinx         │        │
│  │ Engine       │  │ Examples     │  │ Builder        │        │
│  └──────────────┘  └──────────────┘  └────────────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

## Component Design

### 1. NLP Extractor Module (`automation/nlp/`)

```python
automation/nlp/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── pipeline.py          # Main NLP pipeline orchestrator
│   ├── tokenizer.py         # Custom tokenization for code
│   └── analyzer.py          # Semantic analysis engine
├── patterns/
│   ├── __init__.py
│   ├── business_logic.py    # Business logic pattern matchers
│   ├── api_patterns.py      # API semantic patterns
│   └── cross_domain.py      # Cross-domain mapping logic
├── extractors/
│   ├── __init__.py
│   ├── soap_extractor.py    # SOAP-specific semantics
│   ├── rest_extractor.py    # REST API semantics
│   └── sql_extractor.py     # Database semantics
└── models/
    ├── __init__.py
    └── custom_models.py      # Custom SpaCy models
```

### 2. Core NLP Pipeline (`pipeline.py`)

```python
import spacy
from spacy.language import Language
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class SemanticPattern:
    """Represents an abstract semantic pattern"""
    pattern_type: str
    domain_specific: Dict[str, Any]
    abstract_concept: str
    confidence: float
    cross_domain_examples: List[Dict[str, str]]

class NLPPipeline:
    """
    Main NLP processing pipeline for semantic extraction.
    """
    
    def __init__(self, model_name: str = "en_core_web_md"):
        """
        Initialize with SpaCy model and custom components.
        
        Args:
            model_name: SpaCy model to use (medium or large recommended)
        """
        self.nlp = spacy.load(model_name)
        self._add_custom_components()
        self.pattern_library = PatternLibrary()
        
    def _add_custom_components(self):
        """Add custom pipeline components"""
        # Add business logic recognizer
        @Language.component("business_logic_recognizer")
        def business_logic_recognizer(doc):
            # Custom logic for recognizing business patterns
            return doc
            
        self.nlp.add_pipe("business_logic_recognizer", after="ner")
        
    def analyze_code_element(self, 
                            code: str, 
                            context: Dict[str, Any]) -> SemanticPattern:
        """
        Analyze a code element for semantic patterns.
        
        Args:
            code: Source code snippet
            context: Additional context (method name, class, etc.)
            
        Returns:
            SemanticPattern with extracted semantics
        """
        doc = self.nlp(code)
        
        # Extract various semantic features
        intent = self._extract_intent(doc, context)
        entities = self._extract_business_entities(doc)
        relationships = self._extract_relationships(doc)
        
        # Map to abstract pattern
        pattern = self.pattern_library.map_to_abstract(
            intent, entities, relationships
        )
        
        return pattern
```

### 3. Business Logic Pattern Matcher (`patterns/business_logic.py`)

```python
from spacy.matcher import Matcher
from typing import List, Dict, Any

class BusinessLogicPatternMatcher:
    """
    Matches and classifies business logic patterns.
    """
    
    def __init__(self, nlp):
        self.nlp = nlp
        self.matcher = Matcher(nlp.vocab)
        self._initialize_patterns()
        
    def _initialize_patterns(self):
        """Initialize pattern matching rules"""
        
        # Threshold decision pattern
        threshold_pattern = [
            {"LOWER": {"IN": ["if", "when", "check"]}},
            {"POS": {"IN": ["NOUN", "PROPN"]}},
            {"LEMMA": {"IN": ["be", "exceed", "equal", "greater", "less"]}},
            {"LIKE_NUM": True, "OP": "?"},
            {"POS": "NUM", "OP": "?"}
        ]
        self.matcher.add("THRESHOLD_DECISION", [threshold_pattern])
        
        # Validation pattern
        validation_pattern = [
            {"LEMMA": {"IN": ["validate", "verify", "check", "ensure"]}},
            {"POS": {"IN": ["NOUN", "PROPN"]}, "OP": "+"}
        ]
        self.matcher.add("VALIDATION_RULE", [validation_pattern])
        
        # Calculation pattern
        calculation_pattern = [
            {"LEMMA": {"IN": ["calculate", "compute", "derive", "determine"]}},
            {"POS": {"IN": ["NOUN", "PROPN"]}, "OP": "+"}
        ]
        self.matcher.add("CALCULATION", [calculation_pattern])
        
    def extract_patterns(self, text: str) -> List[Dict[str, Any]]:
        """Extract business logic patterns from text"""
        doc = self.nlp(text)
        matches = self.matcher(doc)
        
        patterns = []
        for match_id, start, end in matches:
            pattern_type = self.nlp.vocab.strings[match_id]
            span = doc[start:end]
            
            patterns.append({
                'type': pattern_type,
                'text': span.text,
                'semantic_role': self._determine_semantic_role(pattern_type, span),
                'abstract_concept': self._map_to_abstract(pattern_type)
            })
            
        return patterns
```

### 4. SOAP Semantic Extractor (`extractors/soap_extractor.py`)

```python
from typing import Dict, List, Any
import re

class SOAPSemanticExtractor:
    """
    Extracts semantic meaning from SOAP endpoints.
    """
    
    def __init__(self, nlp_pipeline):
        self.nlp = nlp_pipeline
        self.operation_classifier = OperationClassifier()
        
    def extract_endpoint_semantics(self, 
                                  method_name: str,
                                  parameters: List[Dict],
                                  annotations: Dict) -> Dict[str, Any]:
        """
        Extract semantic meaning from SOAP endpoint.
        
        Args:
            method_name: Name of the web method
            parameters: List of parameter definitions
            annotations: SOAP annotations (@WebService, @WebMethod)
            
        Returns:
            Semantic analysis of the endpoint
        """
        # Classify operation intent
        intent = self.operation_classifier.classify(method_name)
        
        # Analyze parameter semantics
        param_semantics = self._analyze_parameters(parameters)
        
        # Extract business domain
        domain = self._extract_domain_context(method_name, annotations)
        
        # Generate abstract pattern
        abstract_pattern = self._generate_abstract_pattern(
            intent, param_semantics, domain
        )
        
        # Create cross-domain examples
        examples = self._generate_cross_domain_examples(abstract_pattern)
        
        return {
            'operation_intent': intent,
            'parameter_semantics': param_semantics,
            'domain_context': domain,
            'abstract_pattern': abstract_pattern,
            'cross_domain_examples': examples
        }
    
    def _analyze_parameters(self, parameters: List[Dict]) -> List[Dict]:
        """Analyze semantic meaning of parameters"""
        semantic_params = []
        
        for param in parameters:
            name = param['name']
            param_type = param['type']
            
            # Use NLP to understand parameter purpose
            doc = self.nlp.nlp(name)
            
            semantic_type = self._classify_parameter_type(name, param_type)
            purpose = self._infer_parameter_purpose(name, semantic_type)
            
            semantic_params.append({
                'name': name,
                'type': param_type,
                'semantic_type': semantic_type,
                'purpose': purpose,
                'constraints': self._infer_constraints(name, param_type)
            })
            
        return semantic_params
    
    def _classify_parameter_type(self, name: str, java_type: str) -> str:
        """Classify parameter into semantic categories"""
        name_lower = name.lower()
        
        # Temporal parameters
        if any(term in name_lower for term in ['date', 'time', 'period', 'when']):
            return 'TEMPORAL_CONSTRAINT'
            
        # Spatial parameters  
        if any(term in name_lower for term in ['location', 'place', 'where', 'site']):
            return 'SPATIAL_CONSTRAINT'
            
        # Identity parameters
        if any(term in name_lower for term in ['id', 'identifier', 'key', 'code']):
            return 'IDENTIFIER'
            
        # Quantity parameters
        if any(term in name_lower for term in ['amount', 'count', 'quantity', 'total']):
            return 'QUANTITY'
            
        # Status parameters
        if any(term in name_lower for term in ['status', 'state', 'flag', 'enabled']):
            return 'STATUS_INDICATOR'
            
        return 'GENERIC_PARAMETER'
```

### 5. Cross-Domain Pattern Mapper (`patterns/cross_domain.py`)

```python
class CrossDomainMapper:
    """
    Maps domain-specific patterns to abstract concepts and generates
    examples for other domains.
    """
    
    DOMAIN_MAPPINGS = {
        'FILTERED_RETRIEVAL': {
            'abstract': 'Retrieve entities with constraints',
            'domains': {
                'waste_management': {
                    'example': 'getWorkUnits(date, location)',
                    'entities': ['work units', 'routes', 'vehicles']
                },
                'healthcare': {
                    'example': 'getAppointments(date, clinic)',
                    'entities': ['appointments', 'patients', 'providers']
                },
                'finance': {
                    'example': 'getTransactions(date, account)',
                    'entities': ['transactions', 'accounts', 'branches']
                },
                'logistics': {
                    'example': 'getShipments(date, warehouse)',
                    'entities': ['shipments', 'packages', 'routes']
                }
            }
        },
        'THRESHOLD_DECISION': {
            'abstract': 'Execute action when value exceeds boundary',
            'domains': {
                'waste_management': {
                    'example': 'if (overtime > 40) applyOvertimeRate()',
                    'thresholds': ['overtime hours', 'route distance', 'vehicle capacity']
                },
                'healthcare': {
                    'example': 'if (bloodPressure > 140) flagHighRisk()',
                    'thresholds': ['vital signs', 'lab values', 'wait times']
                },
                'finance': {
                    'example': 'if (balance < minimum) chargeOverdraftFee()',
                    'thresholds': ['account balance', 'credit limit', 'transaction amount']
                },
                'logistics': {
                    'example': 'if (weight > limit) requireSpecialHandling()',
                    'thresholds': ['package weight', 'delivery distance', 'storage capacity']
                }
            }
        }
    }
    
    def map_to_abstract(self, domain_pattern: Dict) -> Dict:
        """Map a domain-specific pattern to abstract concept"""
        pattern_type = self._identify_pattern_type(domain_pattern)
        
        if pattern_type in self.DOMAIN_MAPPINGS:
            mapping = self.DOMAIN_MAPPINGS[pattern_type]
            return {
                'pattern_type': pattern_type,
                'abstract_description': mapping['abstract'],
                'confidence': self._calculate_confidence(domain_pattern, pattern_type)
            }
        
        return self._create_new_pattern(domain_pattern)
```

### 6. Integration Interface (`automation/java_ast_extractor.py`)

```python
# Modified JavaASTExtractor to integrate NLP
from automation.nlp.core.pipeline import NLPPipeline
from automation.nlp.extractors.soap_extractor import SOAPSemanticExtractor

class JavaASTExtractor:
    """
    Enhanced Java AST extractor with NLP semantic analysis.
    """
    
    def __init__(self, filesystem: FileSystem, enable_nlp: bool = True):
        """
        Initialize with optional NLP enhancement.
        
        Args:
            filesystem: FileSystem implementation
            enable_nlp: Enable semantic analysis via SpaCy
        """
        self.fs = filesystem
        self.language = "java"
        
        # Initialize NLP pipeline if enabled
        self.nlp_enabled = enable_nlp
        if enable_nlp:
            try:
                self.nlp_pipeline = NLPPipeline()
                self.soap_extractor = SOAPSemanticExtractor(self.nlp_pipeline)
            except Exception as e:
                print(f"NLP initialization failed: {e}")
                self.nlp_enabled = False
    
    def extract_documentation(self, filepath: str) -> Dict[str, Any]:
        """Extract documentation with semantic enhancement"""
        # Existing AST extraction
        base_extraction = self._extract_ast_documentation(filepath)
        
        # Enhance with NLP if available
        if self.nlp_enabled:
            base_extraction = self._enhance_with_semantics(base_extraction)
        
        return base_extraction
    
    def _enhance_with_semantics(self, extraction: Dict) -> Dict:
        """Enhance extraction with semantic analysis"""
        # Process endpoints
        if 'endpoints' in extraction:
            for endpoint in extraction['endpoints']:
                semantic_info = self.soap_extractor.extract_endpoint_semantics(
                    endpoint['name'],
                    endpoint.get('parameters', []),
                    endpoint.get('annotations', {})
                )
                endpoint['semantic_analysis'] = semantic_info
        
        # Process business logic
        if 'business_logic' in extraction:
            extraction['business_logic'] = self._enhance_business_logic(
                extraction['business_logic']
            )
        
        return extraction
```

## Implementation Phases

### Phase 1: Core NLP Infrastructure (Week 1-2)
1. Set up SpaCy environment and dependencies
2. Implement basic NLP pipeline
3. Create pattern matching framework
4. Unit tests for NLP components

### Phase 2: Semantic Extractors (Week 3-4)
1. Implement SOAP semantic extractor
2. Add business logic pattern matcher
3. Create cross-domain mapper
4. Integration tests

### Phase 3: Integration (Week 5)
1. Integrate with JavaASTExtractor
2. Update templates for semantic output
3. End-to-end testing
4. Documentation

## Configuration

### SpaCy Model Selection

```yaml
# config/nlp_config.yaml
nlp:
  model: "en_core_web_md"  # Medium model for balance
  # model: "en_core_web_lg"  # Large model for better accuracy
  
  custom_models:
    - "models/enterprise_patterns.pkl"
    - "models/api_semantics.pkl"
  
  extraction:
    confidence_threshold: 0.75
    enable_cross_domain: true
    max_examples_per_pattern: 3
```

### Dependencies

```toml
# pyproject.toml
[project.optional-dependencies]
nlp = [
    "spacy>=3.7.0",
    "spacy-transformers>=1.3.0",  # For BERT integration
    "pandas>=2.0.0",  # For pattern analysis
]

# Download required models
# python -m spacy download en_core_web_md
```

## Testing Strategy

### Unit Tests

```python
# tests/test_nlp_extraction.py
def test_soap_semantic_extraction():
    """Test SOAP endpoint semantic extraction"""
    extractor = SOAPSemanticExtractor(NLPPipeline())
    
    result = extractor.extract_endpoint_semantics(
        method_name="getWorkUnits",
        parameters=[
            {"name": "queryDate", "type": "String"},
            {"name": "location", "type": "String"}
        ],
        annotations={"namespace": "http://api.dsny.gov/"}
    )
    
    assert result['operation_intent'] == 'FILTERED_RETRIEVAL'
    assert result['parameter_semantics'][0]['semantic_type'] == 'TEMPORAL_CONSTRAINT'
    assert len(result['cross_domain_examples']) >= 3
```

### Integration Tests

```python
def test_java_ast_with_nlp():
    """Test JavaASTExtractor with NLP enhancement"""
    fs = MemoryFileSystem()
    extractor = JavaASTExtractor(fs, enable_nlp=True)
    
    java_code = """
    @WebService
    public class ReportService {
        @WebMethod
        public List<Report> getMonthlyReports(String month, String department) {
            if (reports.size() > 100) {
                return filterLargeDataset(reports);
            }
            return reports;
        }
    }
    """
    
    fs.write_text("ReportService.java", java_code)
    result = extractor.extract_documentation("ReportService.java")
    
    # Check semantic enhancement
    assert 'semantic_analysis' in result['endpoints'][0]
    assert result['business_logic']['patterns'][0]['abstract_concept'] == 'THRESHOLD_DECISION'
```

## Performance Considerations

- **Model Loading**: Cache SpaCy models in memory
- **Batch Processing**: Process multiple files in batches
- **Async Processing**: Use async for large codebases
- **Selective Enhancement**: Allow disabling NLP for performance-critical paths

## Security Considerations

- **Input Validation**: Sanitize code inputs before NLP processing
- **Model Security**: Use verified SpaCy models only
- **PII Detection**: Implement filters for sensitive data
- **Rate Limiting**: Limit NLP processing for resource protection

## Success Metrics

1. **Semantic Accuracy**: 85%+ correct pattern classification
2. **Cross-Domain Relevance**: 90%+ meaningful examples generated
3. **Processing Speed**: <100ms per endpoint for semantic analysis
4. **Abstraction Quality**: Zero domain-specific hardcoding in patterns

## Future Enhancements

1. **Custom SpaCy Models**: Train on enterprise code patterns
2. **Multi-Language Support**: Extend beyond Java
3. **Real-Time Analysis**: IDE integration for live semantic feedback
4. **Pattern Learning**: ML-based pattern discovery from new domains