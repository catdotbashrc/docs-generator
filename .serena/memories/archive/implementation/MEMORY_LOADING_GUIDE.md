# MEMORY: MEMORY_LOADING_GUIDE
Version: 1.0.0
Type: operational
Dependencies: SERENA_OPTIMIZATION_STRATEGY
Token_Count: ~2K
Last_Modified: 2025-08-29
Freshness: ✅ current

## SUMMARY
Practical guide for managing memory loading in Serena for the DDD project, working within Serena's actual constraints where all memories load on project activation.

## CONTEXT
When to load: Every session start, memory management tasks
Purpose: Optimize memory usage within Serena's loading model

## CONTENT

### Understanding Serena's Memory Model

**Key Facts:**
- All memories in `.serena/memories/` load when project activates
- No selective loading or lazy loading built-in
- Memory management is about organization, not loading control
- Focus on memory size and relevance

### Memory Organization Strategy

#### 1. Size-Based Organization
Keep memories focused and small:
- **CORE memories**: <2K tokens each
- **IMPLEMENTATION memories**: <4K tokens each
- **SESSION memories**: <1K tokens each
- **Total target**: <20K tokens for all memories

#### 2. Naming for Mental Model
Since we can't control loading, use names that help YOU understand when to mentally access them:

```
CORE_philosophy.md          # Always relevant
EXTRACT_python.md           # When extracting Python
CALC_coverage.md            # When calculating coverage
SESSION_20250829.md         # Today's context
ARCHIVE_old_analysis.md     # Historical reference
```

#### 3. Memory Chunking
Split large concepts across multiple small memories:
```
COVERAGE_1_element.md       # Element coverage (30%)
COVERAGE_2_completeness.md  # Completeness coverage (40%)
COVERAGE_3_usefulness.md    # Usefulness coverage (30%)
```

### Practical Workflow

#### Session Start
1. Check what memories exist:
   ```python
   list_memories()
   ```

2. Read current state:
   ```python
   read_memory("SESSION_current")
   read_memory("CORE_status")
   ```

3. Mental filtering - focus on relevant memories for current task

#### During Work
1. Update progress regularly:
   ```python
   write_memory("SESSION_current", current_task)
   ```

2. Track important findings:
   ```python
   write_memory("FINDINGS_coverage", gaps_found)
   ```

3. Create task-specific memories as needed

#### Session End
1. Consolidate session memories:
   ```python
   write_memory("SESSION_summary", key_outcomes)
   ```

2. Clean up temporary memories:
   ```python
   delete_memory("SESSION_temp")
   ```

3. Update status memories:
   ```python
   write_memory("CORE_status", current_state)
   ```

### Memory Patterns for DDD Tasks

#### Pattern 1: Coverage Analysis
```
Mentally focus on:
- CORE_three_tier_model
- EXTRACT_patterns
- CALC_algorithms
Ignore:
- SESSION_* (unless recent)
- IMPL_* (unless implementing)
```

#### Pattern 2: Implementation
```
Mentally focus on:
- IMPL_task_checklist
- CORE_conventions
- EXTRACT_patterns
Ignore:
- CALC_* (unless testing calculations)
- ARCHIVE_*
```

#### Pattern 3: Debugging
```
Mentally focus on:
- SESSION_recent_errors
- CORE_philosophy
- CALC_algorithms
Ignore:
- IMPL_guides
- ARCHIVE_*
```

### Memory Maintenance

#### Daily
- Update SESSION_current
- Clean old SESSION_* files
- Update CORE_status

#### Weekly
- Archive old sessions
- Consolidate learnings
- Update documentation

#### Monthly
- Full memory audit
- Remove redundant memories
- Optimize memory sizes

### Quick Reference Commands

```python
# Check all memories
list_memories()

# Read specific memory
read_memory("CORE_philosophy")

# Update memory
write_memory("SESSION_current", "Working on extractors")

# Delete old memory
delete_memory("SESSION_20250822")

# Check memory freshness
for memory in list_memories():
    # Mental note of which are current vs stale
```

## RELATIONSHIPS
- Implements: Practical aspects of SERENA_OPTIMIZATION_STRATEGY
- Works within: Serena's actual memory loading model
- Guides: Daily workflow optimization