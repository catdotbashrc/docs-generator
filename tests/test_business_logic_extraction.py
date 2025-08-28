"""
Test suite for business logic pattern extraction from Java code.

Following TDD principles:
1. Tests written first (RED phase)
2. Minimal implementation to pass (GREEN phase)
3. Refactor for clarity (REFACTOR phase)
"""

import pytest
from pathlib import Path

from automation.java_ast_extractor import JavaASTExtractor
from automation.filesystem.memory import MemoryFileSystem


class TestBusinessLogicExtraction:
    """Test business logic pattern extraction capabilities."""
    
    @pytest.fixture
    def extractor(self):
        """Create JavaASTExtractor with memory filesystem."""
        fs = MemoryFileSystem()
        return JavaASTExtractor(fs), fs
    
    # ===== CONDITIONAL LOGIC TESTS =====
    
    def test_extract_simple_if_condition(self, extractor):
        """Test extraction of simple if conditions as business rules."""
        java_ast, fs = extractor
        
        # Create test Java file with if condition
        test_code = """
        public class OvertimeService {
            public double calculatePay(Employee employee) {
                double pay = employee.getBasePay();
                if (employee.getHours() > 40) {
                    pay += (employee.getHours() - 40) * employee.getOvertimeRate();
                }
                return pay;
            }
        }
        """
        
        fs.write_text("OvertimeService.java", test_code)
        result = java_ast.extract_documentation("OvertimeService.java")
        
        # Verify business logic extraction
        assert 'business_logic' in result
        assert len(result['business_logic']['rules']) > 0
        
        # Check if overtime rule was extracted
        overtime_rule = result['business_logic']['rules'][0]
        assert 'condition' in overtime_rule
        assert 'getHours() > 40' in overtime_rule['condition']
        assert overtime_rule['type'] == 'conditional'
        assert 'overtime' in overtime_rule['description'].lower()
    
    def test_extract_nested_conditions(self, extractor):
        """Test extraction of nested if-else conditions."""
        java_ast, fs = extractor
        
        test_code = """
        public class DiscountService {
            public double applyDiscount(Customer customer, double amount) {
                if (customer.getType() == CustomerType.GOLD) {
                    if (amount > 1000) {
                        return amount * 0.8;  // 20% discount
                    } else {
                        return amount * 0.9;  // 10% discount
                    }
                } else if (customer.getType() == CustomerType.SILVER) {
                    return amount * 0.95;  // 5% discount
                }
                return amount;
            }
        }
        """
        
        fs.write_text("DiscountService.java", test_code)
        result = java_ast.extract_documentation("DiscountService.java")
        
        rules = result['business_logic']['rules']
        assert len(rules) >= 3  # At least 3 discount rules
        
        # Check for gold customer rule
        gold_rules = [r for r in rules if 'GOLD' in r['condition']]
        assert len(gold_rules) > 0
    
    def test_extract_validation_patterns(self, extractor):
        """Test extraction of validation conditions."""
        java_ast, fs = extractor
        
        test_code = """
        public class ValidationService {
            public boolean validateOrder(Order order) {
                if (order == null || order.getItems().isEmpty()) {
                    throw new InvalidOrderException("Order must have items");
                }
                if (order.getTotalAmount() < 0) {
                    throw new InvalidOrderException("Amount cannot be negative");
                }
                if (order.getCustomerId() == null) {
                    throw new InvalidOrderException("Customer ID required");
                }
                return true;
            }
        }
        """
        
        fs.write_text("ValidationService.java", test_code)
        result = java_ast.extract_documentation("ValidationService.java")
        
        validations = result['business_logic']['validations']
        assert len(validations) >= 3
        
        # Check validation messages were extracted
        validation_messages = [v['message'] for v in validations]
        assert any('items' in msg.lower() for msg in validation_messages)
        assert any('negative' in msg.lower() for msg in validation_messages)
    
    # ===== EXCEPTION HANDLING TESTS =====
    
    def test_extract_exception_handling(self, extractor):
        """Test extraction of exception handling patterns."""
        java_ast, fs = extractor
        
        test_code = """
        public class PaymentService {
            public PaymentResult processPayment(Payment payment) {
                try {
                    validatePayment(payment);
                    return gateway.process(payment);
                } catch (InvalidPaymentException e) {
                    return new PaymentResult(Status.INVALID, e.getMessage());
                } catch (GatewayTimeoutException e) {
                    return new PaymentResult(Status.TIMEOUT, "Payment gateway unavailable");
                } catch (Exception e) {
                    logger.error("Unexpected error", e);
                    return new PaymentResult(Status.ERROR, "System error occurred");
                }
            }
        }
        """
        
        fs.write_text("PaymentService.java", test_code)
        result = java_ast.extract_documentation("PaymentService.java")
        
        error_handlers = result['business_logic']['error_handling']
        assert len(error_handlers) >= 3
        
        # Check specific exception handling
        timeout_handler = next((h for h in error_handlers 
                               if 'GatewayTimeoutException' in h['exception']), None)
        assert timeout_handler is not None
        assert 'unavailable' in timeout_handler['action'].lower()
    
    def test_extract_retry_patterns(self, extractor):
        """Test extraction of retry logic patterns."""
        java_ast, fs = extractor
        
        test_code = """
        public class RetryService {
            public Result executeWithRetry(Operation operation) {
                int attempts = 0;
                Exception lastException = null;
                
                while (attempts < 3) {
                    try {
                        return operation.execute();
                    } catch (TransientException e) {
                        lastException = e;
                        attempts++;
                        Thread.sleep(1000 * attempts);
                    }
                }
                throw new MaxRetriesExceededException(lastException);
            }
        }
        """
        
        fs.write_text("RetryService.java", test_code)
        result = java_ast.extract_documentation("RetryService.java")
        
        patterns = result['business_logic']['patterns']
        retry_pattern = next((p for p in patterns if p['type'] == 'retry'), None)
        assert retry_pattern is not None
        assert retry_pattern['max_attempts'] == 3
        assert 'exponential' in retry_pattern['backoff_strategy'].lower()
    
    # ===== WORKFLOW PATTERN TESTS =====
    
    def test_extract_method_call_workflow(self, extractor):
        """Test extraction of workflow from sequential method calls."""
        java_ast, fs = extractor
        
        test_code = """
        public class OrderProcessor {
            public OrderResult processOrder(Order order) {
                validateOrder(order);
                checkInventory(order);
                calculateTotals(order);
                applyDiscounts(order);
                chargePayment(order);
                updateInventory(order);
                sendConfirmation(order);
                return new OrderResult(order);
            }
        }
        """
        
        fs.write_text("OrderProcessor.java", test_code)
        result = java_ast.extract_documentation("OrderProcessor.java")
        
        workflows = result['business_logic']['workflows']
        assert len(workflows) > 0
        
        order_workflow = workflows[0]
        assert order_workflow['name'] == 'processOrder'
        assert len(order_workflow['steps']) == 7
        assert order_workflow['steps'][0]['action'] == 'validateOrder'
        assert order_workflow['steps'][-1]['action'] == 'sendConfirmation'
    
    def test_extract_conditional_workflow(self, extractor):
        """Test extraction of conditional workflow branches."""
        java_ast, fs = extractor
        
        test_code = """
        public class ApprovalService {
            public ApprovalResult processApproval(Request request) {
                validateRequest(request);
                
                if (request.getAmount() > 10000) {
                    requireManagerApproval(request);
                    notifyManager(request);
                } else {
                    autoApprove(request);
                }
                
                logApproval(request);
                return createResult(request);
            }
        }
        """
        
        fs.write_text("ApprovalService.java", test_code)
        result = java_ast.extract_documentation("ApprovalService.java")
        
        workflows = result['business_logic']['workflows']
        approval_workflow = workflows[0]
        
        assert 'branches' in approval_workflow
        assert len(approval_workflow['branches']) > 0
        
        high_amount_branch = approval_workflow['branches'][0]
        assert 'getAmount() > 10000' in high_amount_branch['condition']
        assert any('manager' in step['action'].lower() 
                  for step in high_amount_branch['steps'])
    
    # ===== BUSINESS CONSTANTS TESTS =====
    
    def test_extract_business_constants(self, extractor):
        """Test extraction of business-relevant constants."""
        java_ast, fs = extractor
        
        test_code = """
        public class BusinessConstants {
            public static final double OVERTIME_THRESHOLD = 40.0;
            public static final double TAX_RATE = 0.25;
            public static final int MAX_RETRY_ATTEMPTS = 3;
            public static final String DEFAULT_CURRENCY = "USD";
            
            private static final String INTERNAL_KEY = "secret";  // Should not be extracted
        }
        """
        
        fs.write_text("BusinessConstants.java", test_code)
        result = java_ast.extract_documentation("BusinessConstants.java")
        
        constants = result['business_logic']['constants']
        assert len(constants) >= 4
        
        # Check specific constants
        overtime_const = next((c for c in constants 
                              if c['name'] == 'OVERTIME_THRESHOLD'), None)
        assert overtime_const is not None
        assert overtime_const['value'] == 40.0
        assert overtime_const['type'] == 'double'
    
    # ===== CALCULATION PATTERN TESTS =====
    
    def test_extract_calculation_patterns(self, extractor):
        """Test extraction of business calculations."""
        java_ast, fs = extractor
        
        test_code = """
        public class TaxCalculator {
            public double calculateTax(double income) {
                double tax = 0;
                if (income <= 10000) {
                    tax = income * 0.1;
                } else if (income <= 50000) {
                    tax = 1000 + (income - 10000) * 0.2;
                } else {
                    tax = 9000 + (income - 50000) * 0.3;
                }
                return tax;
            }
        }
        """
        
        fs.write_text("TaxCalculator.java", test_code)
        result = java_ast.extract_documentation("TaxCalculator.java")
        
        calculations = result['business_logic']['calculations']
        assert len(calculations) > 0
        
        tax_calc = calculations[0]
        assert tax_calc['name'] == 'calculateTax'
        assert len(tax_calc['brackets']) == 3
        assert tax_calc['brackets'][0]['threshold'] == 10000
        assert tax_calc['brackets'][0]['rate'] == 0.1
    
    # ===== INTEGRATION TEST =====
    
    def test_extract_complex_business_logic(self, extractor):
        """Test extraction from a complex service with multiple patterns."""
        java_ast, fs = extractor
        
        test_code = """
        @Service
        public class LoanApprovalService {
            private static final double MIN_CREDIT_SCORE = 650;
            private static final double MAX_DTI_RATIO = 0.43;
            
            public LoanDecision evaluateLoan(LoanApplication app) {
                // Step 1: Validate application
                if (app.getCreditScore() < MIN_CREDIT_SCORE) {
                    return new LoanDecision(Status.REJECTED, "Credit score too low");
                }
                
                // Step 2: Calculate DTI
                double dti = calculateDTI(app.getMonthlyDebt(), app.getMonthlyIncome());
                if (dti > MAX_DTI_RATIO) {
                    return new LoanDecision(Status.REJECTED, "DTI ratio too high");
                }
                
                // Step 3: Determine loan terms
                try {
                    double rate = determineInterestRate(app.getCreditScore());
                    int term = determineLoanTerm(app.getRequestedAmount());
                    
                    // Step 4: Final approval
                    approveLoan(app, rate, term);
                    notifyApplicant(app);
                    recordDecision(app);
                    
                    return new LoanDecision(Status.APPROVED, rate, term);
                    
                } catch (UnderwritingException e) {
                    return new LoanDecision(Status.MANUAL_REVIEW, e.getMessage());
                }
            }
            
            private double calculateDTI(double debt, double income) {
                if (income == 0) {
                    throw new InvalidApplicationException("Income cannot be zero");
                }
                return debt / income;
            }
        }
        """
        
        fs.write_text("LoanApprovalService.java", test_code)
        result = java_ast.extract_documentation("LoanApprovalService.java")
        
        logic = result['business_logic']
        
        # Check constants extracted
        assert len(logic['constants']) >= 2
        assert any('CREDIT_SCORE' in c['name'] for c in logic['constants'])
        
        # Check rules extracted
        assert len(logic['rules']) >= 2
        credit_rule = next((r for r in logic['rules'] 
                           if 'credit' in r['description'].lower()), None)
        assert credit_rule is not None
        
        # Check workflow extracted
        assert len(logic['workflows']) > 0
        loan_workflow = logic['workflows'][0]
        assert len(loan_workflow['steps']) >= 4
        
        # Check error handling
        assert len(logic['error_handling']) > 0
        
        # Check validations
        assert len(logic['validations']) > 0