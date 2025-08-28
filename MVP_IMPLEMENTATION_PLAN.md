# MVP Implementation Plan - DSNY SOAP API Documentation

## Goal
Create comprehensive, living documentation for the DSNY SOAP API that focuses on the "why" behind the code, not just the "what".

## Constraints
- **No LLMs**: All extraction via deterministic patterns and SpaCy NLP
- **Sphinx HTML**: Primary output format
- **Living Documentation**: Auto-updates with code changes
- **Local Processing**: No external API dependencies

## Phase 1: Enhanced Java Parser (Day 1)

### 1.1 Upgrade Current Parser
```python
# Current: Basic endpoint extraction
# Target: Rich context extraction

class EnhancedJavaParser:
    def extract_endpoint_context(self):
        """Extract not just signature but surrounding context"""
        - Method Javadoc comments
        - Exception handling patterns
        - Business validation logic
        - Database operations called
        - Related service methods
```

### 1.2 SpaCy Integration for Business Logic
```python
import spacy

class BusinessLogicAnalyzer:
    def analyze_method_intent(self, method_name: str):
        """Extract business intent from method names"""
        # getWorkUnits → "Retrieve work units for reporting"
        # calculateQuota → "Calculate personnel quota based on rules"
        
    def extract_business_rules(self, method_body: str):
        """Find if/then patterns indicating business rules"""
        # if (overtime > 40) → "Overtime threshold rule"
        # if (location == "MANHATTAN") → "Location-specific logic"
        
    def identify_domain_entities(self, class_names: List[str]):
        """Build domain model relationships"""
        # PersonnelModel → Personnel entity
        # QuotaKey → Quota calculation key
```

### 1.3 Pattern Extractors
- **Validation Rules**: Extract from `if` statements and validators
- **Error Handling**: Document exception scenarios and recovery
- **Data Flow**: Track method calls to build sequence diagrams
- **Configuration**: Extract from properties and constants

## Phase 2: Documentation Generator (Day 1-2)

### 2.1 RST Template System
```rst
.. _soap-endpoint-{operation}:

{operation_name} Operation
===========================

**Business Purpose**
{extracted_business_purpose}

**When to Use**
{usage_scenarios}

**Request Structure**
.. code-block:: xml
   {request_example}

**Business Rules**
{foreach business_rule}
- {rule_description}: {rule_implementation}
{/foreach}

**Error Scenarios**
{foreach error}
- **{error_type}**: {when_occurs} → {how_to_handle}
{/foreach}

**Related Operations**
{cross_references}
```

### 2.2 Living Documentation Features
- **Change Detection**: Track what changed between versions
- **Auto-Cross-Reference**: Link related endpoints and models
- **Dependency Graph**: Show which endpoints use which services
- **Test Coverage**: Show which endpoints have tests

## Phase 3: Business Context Enrichment (Day 2)

### 3.1 Domain Model Documentation
```python
class DomainModelDocumentor:
    def document_model_relationships(self):
        """Create ER-style diagrams from Java models"""
        
    def extract_model_constraints(self):
        """Find validation annotations and rules"""
        
    def generate_example_data(self):
        """Create realistic examples for each model"""
```

### 3.2 Service Layer Analysis
```python
class ServiceAnalyzer:
    def extract_business_workflow(self):
        """Build workflow from service method calls"""
        
    def identify_transactions(self):
        """Find @Transactional boundaries"""
        
    def document_caching(self):
        """Find @Cacheable patterns"""
```

### 3.3 Repository Pattern Documentation
- MongoDB query patterns
- Data access patterns
- Performance considerations
- Index requirements

## Implementation Tasks

### Immediate (Today)
1. [ ] Enhance JavaASTExtractor with comment extraction
2. [ ] Add SpaCy pipeline for method name analysis
3. [ ] Create business rule pattern detector
4. [ ] Build RST template for rich endpoint docs

### Tomorrow
5. [ ] Implement service layer analyzer
6. [ ] Add domain model relationship mapper
7. [ ] Create change detection system
8. [ ] Build Sphinx theme customization

### Day 3 (Polish)
9. [ ] Add mermaid diagrams for workflows
10. [ ] Create example request/response pairs
11. [ ] Generate error handling matrix
12. [ ] Build living documentation hooks

## Success Metrics

### Quantitative
- **Coverage**: Document 100% of 7 SOAP endpoints
- **Context**: Extract 5+ business rules per endpoint
- **Relationships**: Map all service dependencies
- **Examples**: Generate 2+ examples per operation

### Qualitative
- **Clarity**: New developer can understand business logic
- **Completeness**: No need to read source code for common tasks
- **Maintainability**: Documentation updates automatically
- **Searchability**: Find answers to "where is X?" questions

## Technical Stack

### Core Dependencies
```toml
[dependency-groups]
nlp = [
    "spacy>=3.7.0",
    "spacy-lookups-data>=1.0.0",
]
parsing = [
    "javalang>=0.13.0",  # Already have
    "lxml>=5.0.0",       # For XML parsing
    "pygments>=2.17.0",  # For code highlighting
]
visualization = [
    "mermaid-cli>=0.3.0",  # For diagrams
    "graphviz>=0.20.0",   # For dependency graphs
]
```

### No External Dependencies
- ❌ No OpenAI/Anthropic APIs
- ❌ No cloud services
- ❌ No external databases
- ✅ Everything runs locally
- ✅ Deterministic outputs
- ✅ Version control friendly

## Example Output Preview

```rst
getWorkUnits Operation
======================

**Business Purpose**
Retrieves work unit assignments for personnel on a specific date, used for daily operational reporting and resource allocation.

**When to Use**
- Generating daily work reports
- Checking personnel assignments
- Validating resource allocation

**Request Structure**
.. code-block:: xml

    <soap:getWorkUnits>
        <queryDate>2024-03-15</queryDate>
    </soap:getWorkUnits>

**Response Structure**
Returns a list of WorkUnitModel objects containing:
- Personnel ID and name
- Assigned location
- Task details
- Shift information

**Business Rules**
- **Date Validation**: Query date cannot be more than 30 days in the past
- **Permission Check**: Caller must have VIEWER role or higher
- **Data Freshness**: Returns cached data if less than 5 minutes old

**Error Scenarios**
- **InvalidDateException**: Date is null or invalid format → Return 400 with date format guide
- **UnauthorizedException**: Insufficient permissions → Return 403 with required role
- **DataNotFoundException**: No data for date → Return 404 with available date range

**Performance Notes**
- Average response time: 200ms
- Caches results for 5 minutes
- Batch requests recommended for multiple dates

**Related Operations**
- :ref:`soap-endpoint-getPersonnel` - Get personnel details
- :ref:`soap-endpoint-getTasks` - Get task assignments
- :ref:`soap-endpoint-getLocations` - Get location hierarchy
```

## Next Steps

Ready to start implementation? I can begin with:

1. **Enhancing the JavaASTExtractor** to extract comments and business logic
2. **Setting up SpaCy** for method name and comment analysis
3. **Creating the RST templates** for rich documentation
4. **Building a proof-of-concept** with one endpoint fully documented

This approach gives us deterministic, testable, deployable documentation without any LLM dependencies!