# DDD Framework: AST Architecture Decision
Version: 1.0.0
Type: architectural_decision
Created: 2025-09-04
Status: PIVOTAL

## 🎯 The AST Revelation

**Core Insight**: Abstract Syntax Trees (AST) are THE standard for code parsing - not regex patterns.

## Why This Matters

**Regex Approach (Wrong Tool)**:
- Fragile with nested structures
- Complex patterns for simple tasks
- Edge cases multiply exponentially
- Language-specific syntax nightmares

**AST Approach (Right Tool)**:
- Designed for parsing code
- Handles ALL syntax correctly
- Language-agnostic pattern
- Scales to any language

## Implementation Strategy

### Current (Python/Ansible Focus)
```python
import ast
# Parse Python code structures properly
tree = ast.parse(content)
# Walk tree to find patterns - no regex!
```

### Future Scaling Pattern
```
Python → ast (built-in)
JavaScript → Babel/ESTree/Acorn
Java → JavaParser/Eclipse JDT
Go → go/ast package
Ruby → Parser gem
C# → Roslyn
```

## Architectural Impact

1. **Extractor Design**: Each language gets its own AST-based extractor
2. **Base Class**: Abstract methods expect AST operations, not string parsing
3. **Testing**: Test AST extraction logic, not regex patterns
4. **Performance**: AST parsing is faster for complex structures
5. **Maintenance**: Dramatically reduced edge cases

## The Refactor That Proved It

**Before (Regex)**:
- 50+ lines of complex regex patterns
- Multiple iterations debugging edge cases
- Still failing on nested dict() calls
- Going in circles trying to fix

**After (AST)**:
- 30 lines of clean tree traversal
- Worked first time for all cases
- Handles any valid Python syntax
- No edge cases to debug

## Quick Reference

**When to use AST**:
- Parsing code structure (parameters, functions, classes)
- Extracting code patterns (API calls, error handling)
- Understanding code relationships (dependencies, calls)
- Any structured code analysis

**When regex is still OK**:
- Simple string extraction (DOCUMENTATION blocks)
- Log file parsing
- Configuration files (non-code)
- Comments and docstrings

## Token-Efficient Summary for Context Loading

💡 **AST Standard**: Use language ASTs (Python ast, JS Babel, Java Parser) not regex for code parsing. Scales cleanly across languages. Proven in refactor: 50 lines regex→30 lines AST, zero edge cases.