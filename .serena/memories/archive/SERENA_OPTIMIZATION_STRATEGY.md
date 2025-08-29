# MEMORY: SERENA_OPTIMIZATION_STRATEGY
Version: 1.0.0
Type: configuration
Dependencies: project_overview, DDD_MEMORY_ARCHITECTURE_SPEC
Token_Count: ~3K
Last_Modified: 2025-08-29
Freshness: ✅ current

## SUMMARY
Practical optimization strategy for Serena configuration in the DDD project, focusing on memory efficiency, context relevance, and workflow automation using Serena's actual capabilities.

## CONTEXT
When to load: Serena configuration optimization, workflow setup, memory management
Related to: DDD workflow automation, coverage tracking, memory efficiency

## CONTENT

### Current Serena Configuration Analysis

**What We Have:**
- Basic `project.yml` with Python language setting
- 17 memories in `.serena/memories/`
- Default tool configuration (all tools enabled)
- Empty initial_prompt field

**Optimization Opportunities:**
1. Better initial_prompt for immediate DDD context
2. Strategic memory organization
3. Intelligent ignored_paths configuration
4. Workflow automation through memory patterns

### Immediate Optimizations

#### 1. Enhanced Initial Prompt
Already implemented in project.yml:
- DDD workflow context (RED-GREEN-REFACTOR)
- Coverage targets and key operations
- Focus on context optimization

#### 2. Ignored Paths Configuration
Already added to reduce noise:
- `baseline/ansible/**` - Large reference project
- Generated files (htmlcov, __pycache__, etc.)
- Build artifacts and dependencies

### Memory Organization Strategy

#### Memory Naming Conventions
Use prefixes for automatic categorization:
- `CORE_*` - Always loaded fundamentals
- `EXTRACT_*` - Extraction-related memories
- `CALC_*` - Coverage calculation logic
- `IMPL_*` - Implementation guides
- `SESSION_*` - Temporary session state

#### Memory Loading Pattern
Since Serena loads memories on project activation, organize by:
1. **Size**: Keep individual memories under 5K tokens
2. **Relevance**: Name memories to indicate when they're needed
3. **Freshness**: Regular cleanup of SESSION_* memories

### Workflow Automation Without Hooks

Since Serena doesn't have built-in hooks like Claude Code, implement automation through:

#### 1. Command Memories
Create memories that track command patterns:
```markdown
# MEMORY: COMMAND_PATTERNS
Track frequently used commands and their contexts:
- `ddd measure`: Load extraction memories
- `ddd assert-coverage`: Load validation memories
- `pytest`: Load testing patterns
```

#### 2. Checkpoint System
Regular memory updates for continuity:
```python
# After significant operations
write_memory("SESSION_checkpoint_YYYYMMDD_HHMM", current_state)
```

#### 3. Status Tracking
Maintain status memories:
- `CURRENT_COVERAGE` - Latest coverage metrics
- `TEST_STATUS` - Test results
- `PENDING_ANALYSIS` - Files needing reanalysis

### Smart Memory Management

#### Memory Lifecycle
1. **Creation**: When new insights or patterns emerge
2. **Update**: After significant changes or milestones
3. **Compression**: When memories exceed 4K tokens
4. **Deletion**: SESSION_* memories older than 7 days

#### Memory Prioritization
Load order based on task:
```yaml
measure_task:
  priority_1: [CORE_coverage_philosophy, CORE_three_tier_model]
  priority_2: [EXTRACT_patterns, CALC_algorithms]
  priority_3: [IMPL_guides, SESSION_checkpoint]
```

### Context Optimization Techniques

#### 1. Lazy Loading Simulation
Structure memories with clear indicators:
```markdown
# MEMORY: EXTRACT_python_patterns
LOAD_WHEN: Python extraction needed
SIZE: 3K tokens
CONTENT: [Actual patterns]
```

#### 2. Memory Compression
For large memories, create summaries:
```markdown
# MEMORY: ANALYSIS_summary
FULL_VERSION: ANALYSIS_detailed_20250829
KEY_POINTS:
- Point 1
- Point 2
```

#### 3. Cross-Reference System
Link related memories:
```markdown
# MEMORY: COVERAGE_algorithms
RELATED: [three_tier_model, aggregation_rules, risk_scoring]
DEPENDS: [daylight_dimensions]
```

### Practical Implementation Steps

#### Phase 1: Memory Reorganization (Immediate)
1. Rename existing memories with prefixes
2. Split large memories (>5K tokens)
3. Create MASTER_INDEX with loading guidance

#### Phase 2: Workflow Memories (Next Session)
1. Create COMMAND_PATTERNS memory
2. Implement checkpoint system
3. Add status tracking memories

#### Phase 3: Automation Scripts (Future)
1. Create Python scripts for memory management
2. Implement coverage tracking automation
3. Add memory compression utilities

### Command-Specific Optimizations

#### For `ddd measure`
```python
# Pre-load relevant memories
memories_needed = [
    "CORE_coverage_philosophy",
    "EXTRACT_patterns",
    "CALC_algorithms"
]
```

#### For `ddd assert-coverage`
```python
# Focus on validation
memories_needed = [
    "CORE_thresholds",
    "CALC_aggregation",
    "CALC_risk_scoring"
]
```

#### For Development Tasks
```python
# Load development context
memories_needed = [
    "IMPL_task_checklist",
    "CORE_code_conventions",
    "SESSION_current_sprint"
]
```

### Performance Monitoring

Track these metrics:
1. **Memory Load Time**: Time to read all memories
2. **Context Usage**: Tokens used vs available
3. **Memory Relevance**: Which memories are actually accessed
4. **Session Continuity**: Success rate of checkpoint recovery

### Integration with DDD Workflow

#### RED Phase (Specification)
- Load: CORE_philosophy, SPEC_dimensions
- Create: New specification memories
- Track: Coverage requirements

#### GREEN Phase (Extraction)
- Load: EXTRACT_*, CALC_*
- Update: Coverage metrics
- Track: Extraction progress

#### REFACTOR Phase (Quality)
- Load: Quality guidelines, best practices
- Update: Improvement tracking
- Track: Quality metrics

## USAGE_EXAMPLES

### Starting New Session
```bash
# Serena automatically loads memories
# Check current status
read_memory("SESSION_last_checkpoint")
read_memory("CURRENT_COVERAGE")
```

### After Coverage Run
```python
# Update coverage memory
write_memory("CURRENT_COVERAGE", f"{coverage:.2%} at {timestamp}")
write_memory("COVERAGE_GAPS", missing_elements)
```

### Session End
```python
# Create checkpoint
write_memory(f"SESSION_checkpoint_{timestamp}", {
    "tasks_completed": completed,
    "coverage": current_coverage,
    "next_steps": pending
})
```

## RELATIONSHIPS
- Implements: DDD_MEMORY_ARCHITECTURE_SPEC principles
- Enhances: project.yml configuration
- Complements: existing memory structure
- Enables: workflow automation without hooks