# DDD Framework Core Principles

## 1. Maintenance-First Philosophy
"We measure documentation by maintenance enablement, not code coverage"
- Don't count docstrings, count maintenance capabilities
- Focus on the 2AM test: Can someone fix this without the original developer?
- A function with no docstring but clear configuration is better than documented code with hidden dependencies

## 2. Evidence-Based Gap Analysis
"Every gap we report has file:line evidence"
- No vague "documentation is poor" assessments
- Specific findings: "DATABASE_URL used at app.py:45 but not documented"
- Actionable reports with exact locations

## 3. Scenario Coverage, Not Code Coverage
"We measure % of maintenance scenarios enabled, not % of code documented"
- Can you update dependencies? ✅/❌
- Can you restore from backup? ✅/❌
- Can you debug production errors? ✅/❌
- Not: "47% of functions have docstrings"

## 4. Handoff Completeness Score
"A complete handoff means the receiving team can operate independently"
- Score based on operational readiness
- Weighted by criticality (production deployment > code formatting)
- Binary per scenario: either you can do it or you can't

## 5. Detection + Inference = Intelligence
"We detect what's there and infer what's missing"
- Find boto3.client('s3') → Infer AWS credentials needed
- Find @retry(attempts=3) → Infer failure scenarios exist
- Find if os.getenv('DEBUG') → Infer multiple environments

## Technical Differentiators

### Multi-Layer Analysis
- Layer 1: Structure (AST) - Code artifacts
- Layer 2: Patterns (Regex + Heuristics) - Integration points
- Layer 3: Inference (Logic) - Missing documentation

### Scenario-Based Scoring
Instead of counting docstrings, check operational capabilities

### Evidence Chain
Every finding has traceable evidence with file:line references