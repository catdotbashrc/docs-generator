"""
Test suite for NLP-based business logic extraction.

Following TDD principles:
1. RED: Write failing tests first
2. GREEN: Make tests pass with minimal code
3. REFACTOR: Improve code while keeping tests green
"""

import pytest
from unittest.mock import Mock, patch, MagicMock

# This import will fail initially (RED phase)
from automation.nlp_extractor import (
    BusinessLogicNLPExtractor,
    AbstractPattern
)


class TestBusinessLogicNLPExtractor:
    """Test the NLP extractor for semantic pattern recognition."""
    
    def test_extractor_initializes_without_spacy(self):
        """Should gracefully degrade when SpaCy is unavailable."""
        with patch('automation.nlp_extractor.spacy.load', side_effect=Exception("No model")):
            extractor = BusinessLogicNLPExtractor(enable_nlp=True)
            
            assert extractor.enable_nlp == False  # Should fallback
            assert extractor.nlp is None
            assert extractor.matcher is None
    
    def test_extractor_initializes_with_spacy(self):
        """Should initialize NLP when SpaCy is available."""
        mock_nlp = MagicMock()
        mock_matcher = MagicMock()
        
        with patch('automation.nlp_extractor.spacy.load', return_value=mock_nlp):
            with patch('automation.nlp_extractor.Matcher', return_value=mock_matcher):
                extractor = BusinessLogicNLPExtractor(enable_nlp=True)
                
                assert extractor.enable_nlp == True
                assert extractor.nlp is not None
                assert extractor.matcher is not None
    
    def test_extract_threshold_pattern_without_nlp(self):
        """Should detect threshold patterns using basic matching."""
        extractor = BusinessLogicNLPExtractor(enable_nlp=False)
        
        code = "if (hours > 40) { applyOvertimeRate(); }"
        patterns = extractor.extract_patterns(code)
        
        assert len(patterns) > 0
        assert any(p.pattern_type == 'THRESHOLD_DECISION' for p in patterns)
        
        # Check pattern has correct structure
        threshold_pattern = next(p for p in patterns if p.pattern_type == 'THRESHOLD_DECISION')
        assert threshold_pattern.description == 'Decision based on numeric boundary'
        assert threshold_pattern.confidence <= 0.5  # Basic matching has lower confidence
        assert 'DSNY' in threshold_pattern.examples
        assert 'Healthcare' in threshold_pattern.examples
    
    def test_extract_validation_pattern_without_nlp(self):
        """Should detect validation patterns using basic matching."""
        extractor = BusinessLogicNLPExtractor(enable_nlp=False)
        
        code = "validateWorkOrder(order)"
        patterns = extractor.extract_patterns(code)
        
        assert len(patterns) > 0
        assert any(p.pattern_type == 'VALIDATION_RULE' for p in patterns)
        
        validation_pattern = next(p for p in patterns if p.pattern_type == 'VALIDATION_RULE')
        assert validation_pattern.abstract_concept == 'validation rule'
    
    def test_extract_retrieval_pattern_without_nlp(self):
        """Should detect retrieval patterns using basic matching."""
        extractor = BusinessLogicNLPExtractor(enable_nlp=False)
        
        code = "List<WorkUnit> units = getWorkUnits(queryDate, location);"
        patterns = extractor.extract_patterns(code)
        
        assert len(patterns) > 0
        assert any(p.pattern_type == 'FILTERED_RETRIEVAL' for p in patterns)
    
    def test_extract_calculation_pattern_without_nlp(self):
        """Should detect calculation patterns using basic matching."""
        extractor = BusinessLogicNLPExtractor(enable_nlp=False)
        
        code = "double overtime = calculateOvertimePay(hours, rate);"
        patterns = extractor.extract_patterns(code)
        
        assert len(patterns) > 0
        assert any(p.pattern_type == 'CALCULATION_RULE' for p in patterns)
    
    def test_extract_workflow_pattern_without_nlp(self):
        """Should detect workflow patterns using basic matching."""
        extractor = BusinessLogicNLPExtractor(enable_nlp=False)
        
        code = "processWorkOrder(); then reviewWorkOrder(); after that approveWorkOrder();"
        patterns = extractor.extract_patterns(code)
        
        assert len(patterns) > 0
        assert any(p.pattern_type == 'WORKFLOW_SEQUENCE' for p in patterns)
    
    @patch('automation.nlp_extractor.spacy.load')
    def test_extract_patterns_with_nlp(self, mock_load):
        """Should use NLP for enhanced pattern detection."""
        # Setup mock SpaCy
        mock_nlp = MagicMock()
        mock_doc = MagicMock()
        mock_nlp.return_value = mock_doc
        mock_load.return_value = mock_nlp
        
        # Setup matcher mock
        mock_matcher = MagicMock()
        mock_matcher.return_value = [(123, 0, 5)]  # Mock match
        
        with patch('automation.nlp_extractor.Matcher', return_value=mock_matcher):
            extractor = BusinessLogicNLPExtractor(enable_nlp=True)
            
            # Mock the necessary attributes
            extractor.nlp.vocab.strings = {123: "THRESHOLD_PATTERN"}
            mock_doc.__getitem__ = MagicMock()
            mock_span = MagicMock()
            mock_span.text = "if hours exceeds 40"
            mock_doc.__getitem__.return_value = mock_span
            
            code = "if hours exceeds 40 then applyOvertime"
            patterns = extractor.extract_patterns(code)
            
            # Should call NLP pipeline
            mock_nlp.assert_called()
    
    def test_enhance_soap_endpoint_without_nlp(self):
        """Should enhance SOAP endpoint info even without NLP."""
        extractor = BusinessLogicNLPExtractor(enable_nlp=False)
        
        endpoint_info = {
            'operation_name': 'getWorkUnits',
            'method_code': 'public List<WorkUnit> getWorkUnits(String date, String location) {...}',
            'parameters': [
                {'name': 'queryDate', 'type': 'String'},
                {'name': 'location', 'type': 'String'}
            ]
        }
        
        enhanced = extractor.enhance_soap_endpoint(endpoint_info)
        
        assert 'semantic_analysis' in enhanced
        assert enhanced['semantic_analysis']['operation_type'] in ['QUERY', 'FILTERED_RETRIEVAL']
        assert 'enhanced_parameters' in enhanced['semantic_analysis']
        
        # Check parameter enhancement
        date_param = next(p for p in enhanced['semantic_analysis']['enhanced_parameters'] 
                         if p['name'] == 'queryDate')
        assert date_param['semantic_type'] == 'TEMPORAL_CONSTRAINT'
        assert date_param['purpose'] == 'Filters or specifies time-based constraints'
    
    def test_cross_domain_example_generation(self):
        """Should generate examples for other domains."""
        extractor = BusinessLogicNLPExtractor(enable_nlp=False)
        
        endpoint_info = {
            'operation_name': 'getWorkUnits',
            'method_code': 'public List<WorkUnit> getWorkUnits(String date, String location) {}'
        }
        
        enhanced = extractor.enhance_soap_endpoint(endpoint_info)
        examples = enhanced['semantic_analysis']['cross_domain_examples']
        
        # Should have examples for different domains
        assert 'Healthcare' in examples
        assert 'Finance' in examples
        assert 'Logistics' in examples
    
    def test_abstract_pattern_dataclass(self):
        """Should create proper AbstractPattern objects."""
        pattern = AbstractPattern(
            pattern_type='THRESHOLD_DECISION',
            description='Decision based on numeric boundary',
            domain_terms=['overtime', 'hours'],
            abstract_concept='threshold decision',
            confidence=0.75,
            examples={'DSNY': 'if overtime > 40'}
        )
        
        assert pattern.pattern_type == 'THRESHOLD_DECISION'
        assert pattern.confidence == 0.75
        assert 'DSNY' in pattern.examples
    
    def test_domain_term_extraction(self):
        """Should extract domain-specific terms from code."""
        extractor = BusinessLogicNLPExtractor(enable_nlp=False)
        
        code = "validateWorkOrder(order); calculateOvertimePay(hours, rate);"
        patterns = extractor.extract_patterns(code)
        
        # Should extract domain terms
        assert any(patterns)
        for pattern in patterns:
            assert isinstance(pattern.domain_terms, list)
            # Should filter out common programming terms
            assert 'public' not in pattern.domain_terms
            assert 'void' not in pattern.domain_terms
    
    def test_confidence_scoring(self):
        """Should assign appropriate confidence scores."""
        extractor = BusinessLogicNLPExtractor(enable_nlp=False)
        
        # Clear pattern should have higher confidence
        clear_code = "if (temperature > 100) { triggerAlarm(); }"
        clear_patterns = extractor.extract_patterns(clear_code)
        
        # Ambiguous pattern should have lower confidence  
        ambiguous_code = "check something maybe"
        ambiguous_patterns = extractor.extract_patterns(ambiguous_code)
        
        if clear_patterns and ambiguous_patterns:
            assert clear_patterns[0].confidence >= ambiguous_patterns[0].confidence
    
    def test_operation_classification(self):
        """Should classify SOAP operations correctly."""
        extractor = BusinessLogicNLPExtractor(enable_nlp=False)
        
        test_cases = [
            ('getWorkUnits', 'QUERY'),
            ('validateOrder', 'VALIDATION'),
            ('calculateTotal', 'CALCULATION'),
            ('processPayment', 'WORKFLOW'),
            ('createUser', 'CREATE'),
            ('updateProfile', 'UPDATE'),
            ('deleteRecord', 'DELETE')
        ]
        
        for operation_name, expected_type in test_cases:
            endpoint = {'operation_name': operation_name}
            enhanced = extractor.enhance_soap_endpoint(endpoint)
            
            assert enhanced['semantic_analysis']['operation_type'] == expected_type
    
    def test_parameter_semantic_classification(self):
        """Should classify parameter semantics correctly."""
        extractor = BusinessLogicNLPExtractor(enable_nlp=False)
        
        parameters = [
            {'name': 'startDate', 'type': 'String'},
            {'name': 'userId', 'type': 'Long'},
            {'name': 'departmentCode', 'type': 'String'},
            {'name': 'locationAddress', 'type': 'String'},
            {'name': 'totalAmount', 'type': 'Double'}
        ]
        
        endpoint = {
            'operation_name': 'testOperation',
            'parameters': parameters
        }
        
        enhanced = extractor.enhance_soap_endpoint(endpoint)
        enhanced_params = enhanced['semantic_analysis']['enhanced_parameters']
        
        # Check semantic types
        date_param = next(p for p in enhanced_params if p['name'] == 'startDate')
        assert date_param['semantic_type'] == 'TEMPORAL_CONSTRAINT'
        
        id_param = next(p for p in enhanced_params if p['name'] == 'userId')
        assert id_param['semantic_type'] == 'IDENTIFIER'
        
        dept_param = next(p for p in enhanced_params if p['name'] == 'departmentCode')
        assert dept_param['semantic_type'] == 'IDENTIFIER'  # 'code' triggers identifier
        
        location_param = next(p for p in enhanced_params if p['name'] == 'locationAddress')
        assert location_param['semantic_type'] == 'SPATIAL_CONSTRAINT'
        
        amount_param = next(p for p in enhanced_params if p['name'] == 'totalAmount')
        assert amount_param['semantic_type'] == 'QUANTITATIVE_VALUE'