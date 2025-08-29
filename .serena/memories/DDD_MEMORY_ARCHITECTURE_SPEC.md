# MEMORY: DDD_MEMORY_ARCHITECTURE_SPEC
Version: 1.0.0
Type: architecture
Dependencies: None
Token_Count: ~4K
Last_Modified: 2025-08-29
Freshness: ✅ current

## SUMMARY
Memory architecture specification for the Documentation Driven Development (DDD) framework, optimized for documentation coverage measurement workflows using RED-GREEN-REFACTOR cycles and artifact-based analysis.

## CONTEXT
When to load: Setting up project memories, architectural decisions, memory reorganization
Related to: Documentation coverage metrics, artifact extractors, DAYLIGHT dimensions
Purpose: Define how DDD project memories should be structured for optimal LLM context usage

## CONTENT

### Core Architecture Principles

1. **Coverage-Centric Organization**: Memories organized around documentation coverage workflows
2. **Artifact-Based Structure**: Focus on countable documentation artifacts (functions, classes, configs)
3. **RED-GREEN-REFACTOR Alignment**: Memory categories map to TDD-inspired cycles
4. **Three-Tier Coverage Model**: Support Element/Completeness/Usefulness measurement
5. **DAYLIGHT Integration**: Eight-dimension framework as organizing principle

### Memory Categories for DDD

#### 1. COVERAGE_CORE (2-3K tokens) - Always Loaded
Essential coverage framework context:
- **coverage_philosophy**: RED-GREEN-REFACTOR for documentation
- **three_tier_model**: Element (30%), Completeness (40%), Usefulness (30%)
- **daylight_dimensions**: 8-dimension framework with weights
- **coverage_thresholds**: Pass/fail criteria (85% default)
- **artifact_taxonomy**: What we count and why

#### 2. EXTRACTION_ENGINE (4-6K tokens) - Measurement Operations
Documentation extraction and analysis:
- **extractor_registry**: Available extractors by language/framework
- **artifact_patterns**: Recognition patterns for countable items
- **dependency_extraction**: Package.json, requirements.txt, pyproject.toml
- **config_extraction**: Environment variables, connection strings, API keys
- **ast_extraction**: Function/class/method parsing strategies

#### 3. COVERAGE_CALCULATION (3-5K tokens) - Assessment Logic
Coverage computation and reporting:
- **coverage_algorithms**: Three-tier calculation methods
- **weighting_system**: Dimension weights and rationale
- **aggregation_rules**: How to combine coverage scores
- **risk_scoring**: Security and operational risk calculations
- **report_templates**: Output formats for different audiences

#### 4. IMPLEMENTATION_GUIDES (5-8K tokens) - Development Tasks
Practical implementation knowledge:
- **adding_extractors**: Step-by-step for new language support
- **dimension_implementation**: How to implement each DAYLIGHT dimension
- **testing_extractors**: Validation and accuracy measurement
- **cli_extension**: Adding new commands and options
- **integration_patterns**: CI/CD, IDE, and tool integration

#### 5. EVOLUTION_TRACKING (2-4K tokens) - Project Journey
Historical context and future direction:
- **ids_to_ddd_evolution**: Journey from "where is config" to coverage metrics
- **paradigm_shift**: Code coverage vs documentation coverage
- **mvp_decisions**: Why configuration coverage for demos
- **enhancement_roadmap**: NLP, AST, Sphinx integration plans
- **lesson_learned**: What worked, what didn't, why

### DDD-Specific Memory Fields

```yaml
# Standard Metadata
MEMORY: descriptive_name
Version: semantic versioning
Type: [coverage_core|extraction|calculation|implementation|evolution]
Dependencies: list of required memories
Token_Count: estimated size
Last_Modified: ISO date
Freshness: [✅ current|🔄 review|⚠️ stale]

# DDD-Specific Metadata
Coverage_Domain: [measurement|extraction|reporting|all]
Artifact_Focus: [functions|classes|configs|dependencies|all]
DAYLIGHT_Relevance: [dimension name or 'cross-cutting']
Maturity_Level: [experimental|mvp|stable|deprecated]
Business_Value: [immediate|short-term|long-term]
```

### Loading Strategies by DDD Task

#### `ddd measure` Command
```yaml
essential:
  - coverage_philosophy
  - three_tier_model
  - daylight_dimensions
required:
  - extractor_registry
  - artifact_patterns
  - coverage_algorithms
optional:
  - report_templates
  - enhancement_roadmap
token_budget: 12-15K
```

#### `ddd assert-coverage` Command
```yaml
essential:
  - coverage_thresholds
  - three_tier_model
required:
  - coverage_algorithms
  - aggregation_rules
  - risk_scoring
optional:
  - testing_extractors
token_budget: 8-10K
```

#### `ddd demo` Command
```yaml
essential:
  - coverage_philosophy
  - mvp_decisions
required:
  - config_extraction
  - risk_scoring
  - report_templates
optional:
  - ids_to_ddd_evolution
  - business_value_metrics
token_budget: 10-12K
```

#### Adding New Extractor
```yaml
essential:
  - artifact_taxonomy
  - extractor_registry
required:
  - adding_extractors
  - testing_extractors
  - artifact_patterns
optional:
  - ast_extraction (if using AST)
  - lesson_learned
token_budget: 10-15K
```

#### Architectural Review
```yaml
essential:
  - coverage_philosophy
  - paradigm_shift
required:
  - ids_to_ddd_evolution
  - enhancement_roadmap
  - three_tier_model
optional:
  - all EVOLUTION_TRACKING
token_budget: 15-20K
```

### Memory Lifecycle for DDD

#### Creation Triggers
- New language support → Create extractor memory
- New DAYLIGHT dimension → Create dimension guide
- Coverage algorithm improvement → Update calculation memory
- Major insight → Add to evolution tracking
- Sprint completion → Create checkpoint memory

#### Update Frequency
- Per commit: artifact_patterns (when adding patterns)
- Per sprint: extractor_registry, implementation_guides
- Per release: coverage_philosophy, daylight_dimensions
- Quarterly: evolution_tracking, lesson_learned

#### Deprecation Strategy
- Old extractors → Archive with deprecation notice
- Superseded algorithms → Move to evolution_tracking
- Abandoned approaches → Document in lesson_learned
- Stale sessions → Delete after 30 days

### The 2AM Test for Memories

Each memory should answer: "Can someone fix the DDD framework at 2AM using this?"

Examples:
- **coverage_algorithms**: YES - Contains complete calculation logic
- **adding_extractors**: YES - Step-by-step implementation guide
- **paradigm_shift**: NO - Philosophical context, not operational
- **mvp_decisions**: PARTIAL - Explains why, not how to fix

### Integration Points

#### With Infrastructure Documentation Standards
- Shared concepts: DAYLIGHT dimensions, extraction patterns
- Divergence: IDS generates docs, DDD measures coverage
- Bridge: Common extractor interfaces, shared configuration

#### With CI/CD Systems
- Memory: integration_patterns
- Purpose: Fail builds on low documentation coverage
- Key data: Thresholds, report formats, exit codes

#### With IDEs
- Memory: ide_integration (future)
- Purpose: Real-time documentation coverage feedback
- Key data: LSP protocols, extension APIs

### Memory Optimization for DDD

1. **Artifact Caching**: Store extracted artifact lists between runs
2. **Incremental Loading**: Load extractors only for detected languages
3. **Lazy Evaluation**: Calculate coverage only for changed files
4. **Template Reuse**: Cache rendered report templates
5. **Batch Processing**: Group similar extraction operations

## USAGE_EXAMPLES

### Starting Fresh DDD Development
```python
load_memories([
    "coverage_philosophy",  # Understand the why
    "three_tier_model",     # Know the how
    "artifact_taxonomy",    # Know what to count
    "adding_extractors"     # Implementation guide
])
```

### Debugging Coverage Calculation
```python
load_memories([
    "coverage_algorithms",  # Calculation logic
    "aggregation_rules",   # How scores combine
    "testing_extractors",  # Validation methods
    "lesson_learned"       # Known issues
])
```

### Presenting to Stakeholders
```python
load_memories([
    "paradigm_shift",      # The big picture
    "mvp_decisions",       # Why config coverage
    "risk_scoring",        # Business impact
    "report_templates"     # Professional output
])
```

## RELATIONSHIPS

### Core Dependencies
- coverage_philosophy → three_tier_model → coverage_algorithms
- artifact_taxonomy → extractor_registry → artifact_patterns
- daylight_dimensions → aggregation_rules → report_templates

### Enhancement Path
```
Current MVP (Config Coverage)
    ↓
AST Integration (95% accuracy)
    ↓
NLP Enhancement (Semantic understanding)
    ↓
Sphinx Reporting (Professional docs)
    ↓
AI Suggestions (Documentation improvement)
```

### Memory Graph
```
COVERAGE_CORE
    ├── EXTRACTION_ENGINE
    │   ├── Language Extractors
    │   └── Pattern Matchers
    ├── COVERAGE_CALCULATION
    │   ├── Algorithms
    │   └── Reporting
    └── IMPLEMENTATION_GUIDES
        ├── Development
        └── Integration
```

## VALIDATION CHECKLIST

✅ Each memory answers "what" or "how" for DDD tasks
✅ Token counts respect context window limits
✅ Loading strategies cover all CLI commands
✅ No circular dependencies in memory graph
✅ Evolution tracking captures key decisions
✅ 2AM test considered for each memory
✅ Business value clearly articulated

## METRICS

- Coverage of DDD operations: 100%
- Average memory size: 3.5K tokens
- Maximum load for any operation: 15K tokens
- Memory categories: 5 distinct domains
- Extraction languages supported: 4 (Python, JS, Java, .NET)
- DAYLIGHT dimensions covered: 8/8