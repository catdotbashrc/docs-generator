#!/usr/bin/env python3
"""Refactor test files to use pathlib.write_text() instead of open/write patterns."""

import re
from pathlib import Path


def refactor_file(file_path: Path) -> int:
    """Refactor a single test file to use pathlib patterns."""
    content = file_path.read_text()
    original_content = content
    changes = 0
    
    # Pattern 1: Simple f.write with string literal
    # with open(var, "w") as f:
    #     f.write("content")
    pattern1 = re.compile(
        r'with open\(([\w_/\s]+),\s*["\']w["\']\)\s*as\s*f:\s*\n\s+f\.write\(([^)]+)\)',
        re.MULTILINE
    )
    
    def replace_simple_write(match):
        nonlocal changes
        file_var = match.group(1).strip()
        content_expr = match.group(2).strip()
        # Check if content needs fixing (unterminated string)
        if '\n"' in content_expr and not '\\n' in content_expr:
            content_expr = content_expr.replace('\n"', '\\n"')
        changes += 1
        return f'{file_var}.write_text({content_expr})'
    
    content = pattern1.sub(replace_simple_write, content)
    
    # Pattern 2: JSON dumps
    # with open(var, "w") as f:
    #     json.dump(data, f)
    pattern2 = re.compile(
        r'with open\(([\w_/\s]+),\s*["\']w["\']\)\s*as\s*f:\s*\n\s+json\.dump\(([^,]+),\s*f\)',
        re.MULTILINE
    )
    
    def replace_json_dump(match):
        nonlocal changes
        file_var = match.group(1).strip()
        json_var = match.group(2).strip()
        changes += 1
        # Check if we need to import json
        if 'import json' not in content:
            return f'{file_var}.write_text(json.dumps({json_var}, indent=2))'
        return f'{file_var}.write_text(json.dumps({json_var}, indent=2))'
    
    content = pattern2.sub(replace_json_dump, content)
    
    # Add json import if needed and not present
    if 'json.dumps' in content and 'import json' not in content:
        # Add after other imports
        if 'from pathlib import Path' in content:
            content = content.replace(
                'from pathlib import Path',
                'from pathlib import Path\nimport json'
            )
        elif 'import ' in content:
            # Find first import and add after
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('import ') or line.startswith('from '):
                    lines.insert(i + 1, 'import json')
                    content = '\n'.join(lines)
                    break
    
    # Fix any unterminated string literals
    # Pattern: "string content
    # "
    pattern3 = re.compile(r'f\.write\("([^"]+)\n"\)', re.MULTILINE)
    content = pattern3.sub(r'f.write("\1\\n")', content)
    
    if content != original_content:
        file_path.write_text(content)
        print(f"✅ Refactored {file_path.name}: {changes} changes")
        return changes
    return 0


def main():
    """Refactor all test files."""
    test_dir = Path("tests")
    if not test_dir.exists():
        print("❌ tests/ directory not found")
        return
    
    total_changes = 0
    test_files = list(test_dir.glob("test_*.py"))
    
    print(f"🔍 Found {len(test_files)} test files to check")
    
    for test_file in test_files:
        changes = refactor_file(test_file)
        total_changes += changes
    
    print(f"\n✨ Refactoring complete: {total_changes} total changes")
    
    # Run quick syntax check
    print("\n🧪 Running syntax check...")
    import ast
    import sys
    
    errors = []
    for test_file in test_files:
        try:
            ast.parse(test_file.read_text())
        except SyntaxError as e:
            errors.append(f"{test_file.name}: {e}")
    
    if errors:
        print("❌ Syntax errors found:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("✅ All files have valid syntax")


if __name__ == "__main__":
    main()