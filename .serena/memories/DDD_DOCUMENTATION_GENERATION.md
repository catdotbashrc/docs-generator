# DDD Documentation Generation Strategy

## Core Generation Philosophy
"Generative to the largest degree possible with clear human input markers"

## Template-Based Generation Approach

### What We Auto-Generate
1. **Dependency Documentation**
   - Package lists from imports
   - Version requirements from lock files
   - Update commands based on package manager
   - Dependency tree visualization

2. **Configuration Documentation**
   - Environment variable lists from code
   - Configuration file references
   - Default values when detectable
   - Configuration parameter types

3. **Integration Documentation**
   - API endpoints from code
   - Database connection patterns
   - External service dependencies
   - Authentication methods used

4. **Error Handling Documentation**
   - Error patterns from try/catch blocks
   - Retry logic from decorators
   - Timeout configurations
   - Fallback mechanisms

5. **Infrastructure Documentation**
   - Network calls from code
   - Port usage from configurations
   - Protocol usage (HTTP/HTTPS/gRPC)
   - Service discovery patterns

### Human Input Markers

Every template includes clear markers:
```
🚨 HUMAN INPUT NEEDED 🚨
[HUMAN: Specific question or requirement]
```

### Template Example - Patching Procedure
```markdown
# Patching & Update Procedures

## Automated Discovery
### Dependencies Found
- boto3==1.26.0 (from requirements.txt)
- ansible==2.9.0 (from setup.py)
- requests>=2.28.0 (from imports)

### Update Commands
\`\`\`bash
# Python dependencies
pip install --upgrade -r requirements.txt

# System packages  
apt-get update && apt-get upgrade
\`\`\`

## 🚨 HUMAN INPUT NEEDED 🚨

### Pre-Update Checklist
- [ ] [HUMAN: Backup procedures completed?]
- [ ] [HUMAN: Maintenance window scheduled?]
- [ ] [HUMAN: Rollback plan prepared?]

### Post-Update Verification
[HUMAN: How do you verify the update was successful?]

### Known Issues
[HUMAN: What breaks when updating? Any version incompatibilities?]
```

## Quality Dimensions

### Two-Dimensional Scoring System
1. **Existence Score (40%)**: Is it documented at all?
2. **Quality Score (60%)**: How good is the documentation?

### Quality Metrics
- Has examples: 20 points
- Has all parameters: 20 points
- Has prerequisites: 15 points
- Has verification steps: 15 points
- Has troubleshooting: 15 points
- Is current/updated: 15 points

### Visual Rating System
```
📊 Patching & Updates
   Existence: ████████░░ 80%
   Quality:   ████░░░░░░ 40%
   Overall:   🟡 Needs Improvement
```

## Business Logic Inference

### Pattern Recognition
- Payment processing from function names
- Authentication from auth patterns
- Data transformation from CRUD operations
- State machines from status transitions
- Validation from constraint checking

### Inference Rules
```python
if 'payment' in function_name:
    purpose = "Payment processing logic"
if contains_pattern(['INSERT', 'UPDATE']):
    purpose = f"Data modification for {table_name}"
if is_api_endpoint():
    purpose = f"{method} operation on {route}"
```

### Generated Business Logic Template
```markdown
## Business Logic Documentation

### Automated Analysis
**Inferred Purpose**: Payment processing logic
**Detected Patterns**: API call, database write, validation
**Data Flow**: Input → Validation → Processing → Storage

### 🚨 REQUIRES HUMAN REVIEW 🚨

**Business Context**: 
[HUMAN INPUT NEEDED: What business problem does this solve?]

**Critical Business Rules**:
[HUMAN INPUT NEEDED: What are the non-obvious constraints?]

**Expected Behavior**:
- Input: Credit card details (detected)
- Processing: Charge via Stripe API (detected)
- Output: Transaction ID (detected)
- Side Effects: [HUMAN INPUT NEEDED: What else happens?]
```