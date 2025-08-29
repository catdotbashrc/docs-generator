# ATDD Implementation Guide for Claude Code

## Quick Start

### 1. Install ATDD Enforcement Hooks

Create `.claude/hooks/atdd_enforcer.py`:

```python
#!/usr/bin/env python3
"""
ATDD Enforcement Hook for Claude Code
Ensures test-driven development discipline in AI workflows
"""

import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

class ATDDEnforcer:
    """Enforces Agentic TDD principles during development."""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.test_dir = self.project_root / "tests"
        self.coverage_threshold = 80
        
    def check_phase(self) -> str:
        """Determine current TDD phase based on project state."""
        # Check for .atdd_state file
        state_file = self.project_root / ".atdd_state"
        if state_file.exists():
            with open(state_file) as f:
                state = json.load(f)
                return state.get("phase", "SPECIFY")
        return "SPECIFY"
    
    def verify_test_exists(self, module_name: str) -> bool:
        """Verify that tests exist for a module before allowing code generation."""
        test_file = self.test_dir / f"test_{module_name}.py"
        return test_file.exists()
    
    def check_tests_failing(self) -> Tuple[bool, List[str]]:
        """Verify that tests are currently failing (RED phase)."""
        try:
            result = subprocess.run(
                ["python", "-m", "pytest", "-q"],
                capture_output=True,
                text=True
            )
            # Tests should fail in RED phase
            if result.returncode != 0:
                failures = [line for line in result.stdout.split('\n') 
                          if 'FAILED' in line]
                return True, failures
            return False, []
        except Exception as e:
            print(f"Error running tests: {e}")
            return False, []
    
    def check_coverage(self) -> Tuple[bool, float]:
        """Check if coverage meets threshold."""
        try:
            result = subprocess.run(
                ["python", "-m", "pytest", "--cov=.", "--cov-report=json", "-q"],
                capture_output=True,
                text=True
            )
            
            coverage_file = self.project_root / "coverage.json"
            if coverage_file.exists():
                with open(coverage_file) as f:
                    data = json.load(f)
                    percent = data["totals"]["percent_covered"]
                    return percent >= self.coverage_threshold, percent
            return False, 0.0
        except Exception as e:
            print(f"Error checking coverage: {e}")
            return False, 0.0
    
    def enforce_tdd_phase(self, context: Dict) -> bool:
        """Main enforcement logic based on current phase."""
        current_phase = self.check_phase()
        action = context.get("action", "")
        target = context.get("target", "")
        
        print(f"🎯 ATDD Phase: {current_phase}")
        
        if current_phase == "SPECIFY":
            if action == "generate_code":
                print("❌ STOP: Requirements must be specified first")
                print("   Required: Create requirement specification")
                return False
            elif action == "write_requirements":
                print("✅ Proceed: Specifying requirements")
                return True
                
        elif current_phase == "GENERATE":
            if action == "generate_code":
                print("❌ STOP: Tests must be written first")
                print("   Required: Write failing tests")
                return False
            elif action == "write_tests":
                print("✅ Proceed: Writing tests")
                return True
                
        elif current_phase == "FAIL":
            tests_failing, failures = self.check_tests_failing()
            if not tests_failing:
                print("❌ STOP: Tests must fail before implementation")
                print("   Required: Ensure tests are failing")
                return False
            print(f"✅ RED Phase confirmed: {len(failures)} tests failing")
            return True
            
        elif current_phase == "IMPLEMENT":
            if action != "generate_code":
                print("❌ STOP: Must implement code to pass tests")
                return False
            if not self.verify_test_exists(target):
                print(f"❌ STOP: No tests found for {target}")
                return False
            print("✅ Proceed: Implementing minimal code")
            return True
            
        elif current_phase == "VERIFY":
            meets_coverage, percent = self.check_coverage()
            if not meets_coverage:
                print(f"❌ Coverage {percent:.1f}% below threshold {self.coverage_threshold}%")
                return False
            print(f"✅ Coverage {percent:.1f}% meets threshold")
            return True
            
        return True
    
    def update_phase(self, new_phase: str):
        """Update the current TDD phase."""
        state_file = self.project_root / ".atdd_state"
        state = {"phase": new_phase, "timestamp": str(Path.cwd())}
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2)
        print(f"📍 Phase updated to: {new_phase}")

def main():
    """Main entry point for the hook."""
    # Get context from environment or arguments
    context = {
        "action": sys.argv[1] if len(sys.argv) > 1 else "",
        "target": sys.argv[2] if len(sys.argv) > 2 else ""
    }
    
    enforcer = ATDDEnforcer()
    
    # Enforce TDD phase rules
    if not enforcer.enforce_tdd_phase(context):
        sys.exit(1)  # Block the action
    
    sys.exit(0)  # Allow the action

if __name__ == "__main__":
    main()
```

### 2. Configure ATDD Settings

Create `.claude/ATDD.yaml`:

```yaml
# Agentic TDD Configuration for Claude Code
atdd:
  version: "1.0.0"
  enforcement: strict
  
  # Coverage thresholds
  coverage:
    line: 80
    branch: 70
    mutation: 60
    new_code: 100  # New features require 100% coverage initially
  
  # Phase management
  phases:
    enabled: true
    sequence:
      - SPECIFY
      - VALIDATE
      - GENERATE
      - FAIL
      - IMPLEMENT
      - VERIFY
      - REFACTOR
      - DOCUMENT
      - COMMIT
    
    indicators:
      SPECIFY: "📋 SPECIFICATION"
      VALIDATE: "📝 VALIDATION"
      GENERATE: "🧪 TEST GENERATION"
      FAIL: "🔴 RED PHASE"
      IMPLEMENT: "🟡 IMPLEMENTATION"
      VERIFY: "✅ VERIFICATION"
      REFACTOR: "🔄 REFACTORING"
      DOCUMENT: "📚 DOCUMENTATION"
      COMMIT: "💾 CHECKPOINT"
  
  # Enforcement hooks
  hooks:
    pre_code_generation:
      script: .claude/hooks/atdd_enforcer.py
      args: ["generate_code"]
      blocking: true
    
    post_test_creation:
      script: .claude/hooks/atdd_enforcer.py
      args: ["verify_tests"]
      blocking: false
    
    pre_commit:
      script: .claude/hooks/atdd_enforcer.py
      args: ["check_coverage"]
      blocking: true
  
  # AI-specific settings
  ai_agent:
    claude_code:
      enforce_minimal_code: true
      require_test_evidence: true
      auto_generate_properties: true
      suggest_refactorings: true
    
    prohibited_actions:
      - generate_code_without_tests
      - modify_tests_to_pass
      - skip_coverage_check
      - commit_without_green_state
    
    required_evidence:
      - test_execution_output
      - coverage_report
      - mutation_testing_results
  
  # Quality gates
  quality_gates:
    commit:
      - all_tests_pass
      - coverage_threshold_met
      - no_todo_in_code
      - documentation_complete
    
    pull_request:
      - all_quality_gates_pass
      - peer_review_complete
      - ci_pipeline_green
    
    deploy:
      - production_tests_pass
      - performance_benchmarks_met
      - security_scan_clean

# Session state tracking
session:
  track_tdd_cycles: true
  preserve_phase_across_sessions: true
  evidence_retention: 30_days
  
# Metrics collection
metrics:
  enabled: true
  track:
    - tdd_cycle_time
    - test_first_compliance
    - coverage_trend
    - defect_escape_rate
    - refactoring_frequency
```

### 3. Create ATDD Templates

#### Test Contract Template
Create `.claude/templates/test_contract.py`:

```python
"""
ATDD Test Contract Template
Use this template to define test contracts before implementation
"""

import pytest
from typing import Any, List, Dict, Optional
from hypothesis import given, strategies as st

class Test{FeatureName}Contract:
    """Test contract for {FeatureName} - NO IMPLEMENTATION YET"""
    
    # Phase: VALIDATE - Defining test contracts
    
    def test_requirement_1_contract(self):
        """
        Contract: {Requirement 1 description}
        Given: {Initial conditions}
        When: {Action taken}
        Then: {Expected outcome}
        """
        raise NotImplementedError("Awaiting RED phase")
    
    def test_requirement_2_contract(self):
        """
        Contract: {Requirement 2 description}
        Given: {Initial conditions}
        When: {Action taken}
        Then: {Expected outcome}
        """
        raise NotImplementedError("Awaiting RED phase")
    
    def test_edge_case_contract(self):
        """
        Contract: Handle edge case {description}
        """
        raise NotImplementedError("Awaiting RED phase")
    
    def test_error_handling_contract(self):
        """
        Contract: Proper error handling for {error scenario}
        """
        raise NotImplementedError("Awaiting RED phase")
    
    @given(st.integers())  # Property-based test contract
    def test_property_contract(self, value: int):
        """
        Contract: Property {property name} always holds
        """
        raise NotImplementedError("Awaiting RED phase")
```

#### Minimal Implementation Template
Create `.claude/templates/minimal_implementation.py`:

```python
"""
ATDD Minimal Implementation Template
Generate ONLY enough code to make tests pass
"""

class {ClassName}:
    """Minimal implementation to pass current tests."""
    
    def {method_name}(self, {parameters}) -> {return_type}:
        """
        Implements ONLY the behavior required by test:
        - test_{test_name}
        
        NO additional features or nice-to-haves.
        """
        # Minimal code to pass test
        {minimal_implementation}
    
    # STOP: No additional methods until tests require them
```

### 4. AI Agent Instructions

Create `.claude/ATDD_INSTRUCTIONS.md`:

```markdown
# ATDD Instructions for Claude Code

## You MUST follow these ATDD principles:

### 🔴 Phase Enforcement
1. **SPECIFY Phase**: Understand requirements before ANY action
2. **VALIDATE Phase**: Write test contracts before tests
3. **GENERATE Phase**: Write complete failing tests
4. **FAIL Phase**: Verify all tests fail before coding
5. **IMPLEMENT Phase**: Write MINIMAL code to pass tests
6. **VERIFY Phase**: Check coverage meets thresholds
7. **REFACTOR Phase**: Improve code keeping tests green
8. **DOCUMENT Phase**: Document decisions and evidence
9. **COMMIT Phase**: Create checkpoint with semantic message

### ⚠️ Enforcement Rules
- **BLOCKED**: Cannot write code without failing tests
- **BLOCKED**: Cannot modify tests to make them pass
- **BLOCKED**: Cannot commit with failing tests
- **BLOCKED**: Cannot commit if coverage drops
- **BLOCKED**: Cannot skip any phase

### 📊 Required Evidence
For EVERY code generation, you must show:
```bash
# 1. Test execution results
$ pytest test_feature.py -v

# 2. Coverage report
$ pytest --cov=module --cov-report=term-missing

# 3. Phase status
$ cat .atdd_state
```

### 🎯 Example Workflow
```python
# Phase 1: SPECIFY
"""
Requirement: Calculate tax based on income brackets
- 0-10k: 10%
- 10k-50k: 20%
- 50k+: 30%
"""

# Phase 2: VALIDATE (test contract)
def test_tax_calculation_contract():
    """Contract: Calculate tax based on brackets"""
    raise NotImplementedError("Awaiting RED phase")

# Phase 3: GENERATE (failing test)
def test_tax_calculation():
    assert calculate_tax(5000) == 500  # 10%
    assert calculate_tax(25000) == 4000  # 20% 
    assert calculate_tax(75000) == 14000  # 30%

# Phase 4: FAIL (verify red)
$ pytest test_tax.py  # ❌ FAILED (expected)

# Phase 5: IMPLEMENT (minimal code)
def calculate_tax(income):
    if income <= 10000:
        return income * 0.1
    elif income <= 50000:
        return 2000 + (income - 10000) * 0.2
    else:
        return 10000 + (income - 50000) * 0.3

# Phase 6: VERIFY (check coverage)
$ pytest --cov=tax  # ✅ 100% coverage

# Continue through remaining phases...
```

### 🚫 Anti-Patterns to AVOID
1. Writing implementation before tests
2. Writing more code than tests require
3. Adding untested helper methods
4. Modifying tests to pass
5. Skipping coverage verification
```

### 5. CI/CD Pipeline Integration

Create `.github/workflows/atdd.yml`:

```yaml
name: ATDD Enforcement Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  atdd-enforcement:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install pytest pytest-cov pytest-timeout
        pip install mutation pytest-mutation
        pip install -e ".[dev]"
    
    - name: Check ATDD Phase
      run: |
        python .claude/hooks/atdd_enforcer.py check_phase
    
    - name: Run Tests (Must Pass)
      run: |
        pytest tests/ -v --tb=short
    
    - name: Check Coverage
      run: |
        pytest --cov=. --cov-report=term-missing --cov-report=json
        python -c "import json; data=json.load(open('coverage.json')); assert data['totals']['percent_covered'] >= 80"
    
    - name: Mutation Testing
      run: |
        pytest --mutation
    
    - name: Generate Evidence Report
      run: |
        echo "## ATDD Evidence Report" > atdd_evidence.md
        echo "### Test Results" >> atdd_evidence.md
        pytest --tb=no --co -q >> atdd_evidence.md
        echo "### Coverage Report" >> atdd_evidence.md
        pytest --cov=. --cov-report=term >> atdd_evidence.md
        
    - name: Upload Evidence
      uses: actions/upload-artifact@v3
      with:
        name: atdd-evidence
        path: atdd_evidence.md
```

## Usage Examples

### Example 1: Starting a New Feature

```bash
# Claude Code conversation
User: "Implement user authentication feature"

# ATDD Phase: SPECIFY
Claude: 📋 SPECIFICATION Phase
Let me first understand the requirements:
- User registration with email/password
- Login with credentials
- Password hashing with bcrypt
- Session management with JWT

Creating requirement specification...

# ATDD Phase: VALIDATE
Claude: 📝 VALIDATION Phase
Writing test contracts first:
[Creates test_auth_contract.py with contract definitions]

# ATDD Phase: GENERATE  
Claude: 🧪 TEST GENERATION Phase
Implementing failing tests:
[Creates test_auth.py with complete test suite]

# ATDD Phase: FAIL
Claude: 🔴 RED Phase - Verifying tests fail:
$ pytest test_auth.py
===== 5 failed in 0.03s =====
✅ All tests failing correctly

# ATDD Phase: IMPLEMENT
Claude: 🟡 IMPLEMENTATION Phase
Writing minimal code to pass tests:
[Creates auth.py with minimal implementation]

# And so on through all phases...
```

### Example 2: Handling Phase Violations

```bash
User: "Just implement the login function quickly"

Claude: ❌ ATDD ENFORCEMENT: Cannot proceed
Current Phase: SPECIFY
Required: Must complete specification phase first

Let me help you follow ATDD properly:
1. First, let's specify the requirements
2. Then we'll write test contracts
3. Only then can we implement

Shall we start with the requirements specification?
```

## Monitoring and Metrics

### ATDD Dashboard
Create `atdd_metrics.py`:

```python
import json
from pathlib import Path
from datetime import datetime, timedelta

class ATDDMetrics:
    def __init__(self):
        self.metrics_file = Path(".atdd_metrics.json")
        
    def track_cycle(self, feature_name: str, phase_times: dict):
        """Track time spent in each ATDD phase."""
        metrics = self.load_metrics()
        metrics["cycles"].append({
            "feature": feature_name,
            "timestamp": datetime.now().isoformat(),
            "phase_times": phase_times,
            "total_time": sum(phase_times.values())
        })
        self.save_metrics(metrics)
    
    def calculate_compliance(self):
        """Calculate ATDD compliance rate."""
        metrics = self.load_metrics()
        total_features = len(metrics["cycles"])
        compliant = sum(1 for c in metrics["cycles"] 
                       if c.get("test_first", False))
        return (compliant / total_features * 100) if total_features > 0 else 0
    
    def generate_report(self):
        """Generate ATDD compliance report."""
        metrics = self.load_metrics()
        report = {
            "compliance_rate": self.calculate_compliance(),
            "average_cycle_time": self.calculate_avg_cycle_time(),
            "coverage_trend": self.get_coverage_trend(),
            "test_first_rate": self.calculate_test_first_rate()
        }
        return report
```

## Success Criteria

The ATDD methodology is successfully implemented when:

1. **100% Test-First Compliance**: No production code without failing tests
2. **80%+ Coverage Maintained**: Coverage never drops below threshold
3. **Evidence Trail Complete**: All phases documented with evidence
4. **Cycle Time Optimized**: Average cycle time < 30 minutes
5. **Zero Test Modifications**: Tests never modified to pass

## Conclusion

This implementation guide provides everything needed to enforce ATDD discipline in Claude Code workflows. The combination of enforcement hooks, templates, and CI/CD integration ensures that AI-assisted development maintains the highest quality standards through rigorous test-driven practices.