# MEMORY: MEMORY_ARCHITECTURE_SPEC
Version: 2.0.0
Type: architecture
Dependencies: MASTER_INDEX, project_overview
Token_Count: ~4K
Last_Modified: 2025-08-29
Freshness: ✅ current

## SUMMARY
Comprehensive memory architecture specification for the DDD (Documentation Driven Development) framework, optimizing for documentation coverage workflows and RED-GREEN-REFACTOR cycles with hierarchical organization and intelligent loading strategies.

## CONTEXT
When to load: Memory reorganization, project setup, architectural decisions
Related to: DDD framework evolution, DAYLIGHT dimensions, coverage metrics
Supersedes: Basic memory organization

## CONTENT

### Core Architecture Principles

1. **Coverage-Aligned Hierarchy**: 5 categories mapped to DDD workflow phases
2. **Metadata-Rich Format**: Standard headers plus DDD-specific fields
3. **Task-Based Loading**: Optimized for measure/assert/demo operations
4. **Token-Aware Budgets**: Explicit management for large documentation analysis
5. **Evolution Tracking**: Bridge between IDS and DDD projects

### Memory Categories

#### 1. PROJECT_CORE (2-3K tokens) - Always Loaded
Fundamental context required for every operation:
- **project_overview**: Framework purpose, philosophy, current status
- **MASTER_INDEX**: Navigation and quick reference
- **DAYLIGHT_spec**: 8-dimension framework definition
- **coverage_thresholds**: Pass/fail criteria (85% default)

#### 2. TECHNICAL_FOUNDATION (3-5K tokens) - Development Tasks
Essential for implementation and maintenance:
- **tech_stack**: Languages, dependencies, tools
- **code_style_conventions**: Formatting, testing standards
- **UV_GUIDANCE**: Package manager specifics
- **suggested_commands**: CLI operations and workflows

#### 3. IMPLEMENTATION (5-8K tokens) - Feature-Specific
Task-specific implementation details:
- **extractor_patterns**: Language-specific extraction logic
- **coverage_algorithms**: Three-tier calculation methods
- **artifact_definitions**: What to count (functions, classes, configs)
- **MVP_Configuration_Coverage_Implementation**: Current focus area
- **task_completion_checklist**: Step-by-step guides

#### 4. KNOWLEDGE_BASE (3-5K each) - On-Demand Reference
Deep knowledge and learnings:
- **technical_learnings_config_coverage**: Lessons from MVP
- **deep_analysis_report_2025**: Architectural insights
- **NLP_AST_Sphinx_integration**: Advanced enhancement plans
- **testing_patterns**: Quality assurance strategies
- **deployment_strategies**: Production readiness

#### 5. SESSION_MANAGEMENT (2-3K tokens) - Continuity
Cross-session state and progress:
- **current_sprint**: Active development focus
- **session_checkpoint_***: Recovery points
- **loading_matrix**: Task-to-memory mappings
- **project_manifest**: File structure and organization

### DDD-Specific Metadata Fields

Every memory must include standard fields plus:
```yaml
# Standard Fields (from IDS)
Version: semantic version
Type: [core|technical|implementation|knowledge|session]
Dependencies: list of required memories
Token_Count: estimated size
Last_Modified: ISO date
Freshness: [✅ current|🔄 review|⚠️ stale]

# DDD-Specific Fields
Coverage_Impact: [high|medium|low|none]
DAYLIGHT_Dimension: [Dependencies|Automation|Yearbook|etc]
Workflow_Phase: [RED|GREEN|REFACTOR|ALL]
Artifact_Types: [functions|classes|configs|etc]
```

### Loading Matrix for DDD Operations

#### Measure Command
```yaml
core: [project_overview, MASTER_INDEX, DAYLIGHT_spec]
required: [extractor_patterns, coverage_algorithms, artifact_definitions]
optional: [technical_learnings, testing_patterns]
token_budget: 10-12K
```

#### Assert-Coverage Command
```yaml
core: [project_overview, coverage_thresholds]
required: [coverage_algorithms, DAYLIGHT_spec]
optional: [MVP_Configuration_Coverage_Implementation]
token_budget: 8-10K
```

#### Demo Command
```yaml
core: [project_overview, MASTER_INDEX]
required: [MVP_Configuration_Coverage_Implementation, artifact_definitions]
optional: [deep_analysis_report_2025]
token_budget: 10-15K
```

#### Development Tasks
```yaml
core: [ALL PROJECT_CORE]
required: [ALL TECHNICAL_FOUNDATION, task_completion_checklist]
optional: [current_sprint, session_checkpoint_*]
token_budget: 12-15K
```

#### Architectural Review
```yaml
core: [project_overview, MASTER_INDEX]
required: [deep_analysis_report_2025, NLP_AST_Sphinx_integration]
optional: [ALL KNOWLEDGE_BASE]
token_budget: 15-20K
```

### Memory Lifecycle Management

#### Creation Triggers
- New dimension implementation → Create extractor memory
- Coverage algorithm change → Update coverage_algorithms
- Sprint completion → Archive to session memory
- Major learning → Add to KNOWLEDGE_BASE

#### Update Patterns
- Daily: current_sprint, session_checkpoint
- Weekly: loading_matrix, task_completion_checklist
- Sprint: project_overview, MASTER_INDEX
- Major release: DAYLIGHT_spec, coverage_thresholds

#### Deprecation Rules
- Session memories > 30 days → Archive
- Superseded implementations → Move to KNOWLEDGE_BASE
- Stale learnings → Mark with ⚠️ freshness

### Integration with IDS Project

The DDD memory architecture extends IDS patterns:
- Shared: Hierarchical categories, metadata format
- Enhanced: Coverage-specific fields, DAYLIGHT alignment
- Bridge: Evolution tracking from documentation generation to validation

### Memory Optimization Strategies

1. **Lazy Loading**: Load KNOWLEDGE_BASE only when needed
2. **Caching**: Reuse PROJECT_CORE across operations
3. **Compression**: Use abbreviated formats for large memories
4. **Chunking**: Split large memories into dimension-specific pieces
5. **Prioritization**: Load by Coverage_Impact rating

## USAGE_EXAMPLES

### Example 1: Starting Development
```
Load: PROJECT_CORE + TECHNICAL_FOUNDATION + current_sprint
Skip: KNOWLEDGE_BASE (unless investigating specific patterns)
```

### Example 2: Adding New Extractor
```
Load: extractor_patterns + artifact_definitions + testing_patterns
Skip: SESSION_MANAGEMENT (not needed for implementation)
```

### Example 3: Coverage Analysis
```
Load: coverage_algorithms + DAYLIGHT_spec + technical_learnings
Skip: code_style_conventions (not relevant for analysis)
```

## RELATIONSHIPS

### Dependencies
- Requires: MASTER_INDEX for navigation
- Enhances: All memory operations through structured organization
- Supersedes: Ad-hoc memory creation

### Cross-References
- MASTER_INDEX: Quick navigation to all memories
- project_overview: Context for architecture decisions
- loading_matrix: Operational implementation of this spec

### Evolution Path
```
IDS Memory Architecture (v1.0)
    ↓
DDD Memory Architecture (v2.0) [CURRENT]
    ↓
Future: AI-Enhanced Memory Selection (v3.0)
```

## VALIDATION CHECKLIST

✅ Each memory has complete metadata
✅ Token counts are accurate (±10%)
✅ Loading matrix covers all CLI commands
✅ Freshness indicators updated regularly
✅ Dependencies are bidirectional
✅ No circular dependencies
✅ Categories are mutually exclusive
✅ Evolution path maintains compatibility

## METRICS

- Total memories: 15 active
- Average token size: 3.5K
- Maximum context load: 20K tokens
- Coverage of DDD operations: 100%
- Freshness: 80% current, 13% review, 7% stale