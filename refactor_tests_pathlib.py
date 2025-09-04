#!/usr/bin/env python3
"""Refactor test files to use pathlib.write_text() instead of open/write patterns."""

import re
from pathlib import Path
import json


def refactor_file(file_path: Path) -> int:
    """Refactor a single test file to use pathlib patterns."""
    content = file_path.read_text()
    original_content = content
    changes = 0
    
    # Pattern 1: with open(..., "w") as f: f.write(...)
    # Replace with: (...).write_text(...)
    lines = content.split('\n')
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check for "with open" pattern
        if 'with open(' in line and '"w"' in line:
            # Extract the file path variable
            match = re.search(r'with open\(([\w_/.]+(?:\s*/\s*[\w"\'.\[\]]+)*),\s*["\']w["\']\)\s*as\s*f:', line)
            if match:
                file_var = match.group(1).strip()
                
                # Look at next line
                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    
                    # Check for f.write pattern
                    write_match = re.search(r'^\s+f\.write\((.*)\)$', next_line)
                    if write_match:
                        write_content = write_match.group(1)
                        # Fix multiline strings
                        if i + 2 < len(lines) and '")' in lines[i + 2]:
                            # Multiline string case
                            write_content = write_content.rstrip('"').rstrip("'") + '\\n"'
                            new_lines.append(f'        {file_var}.write_text({write_content})')
                            i += 3  # Skip the three lines
                            changes += 1
                            continue
                        else:
                            # Single line write
                            indent = len(next_line) - len(next_line.lstrip())
                            new_lines.append(' ' * indent + f'{file_var}.write_text({write_content})')
                            i += 2  # Skip both lines
                            changes += 1
                            continue
                    
                    # Check for json.dump pattern
                    json_match = re.search(r'^\s+json\.dump\((.*),\s*f\)$', next_line)
                    if json_match:
                        json_var = json_match.group(1).strip()
                        indent = len(next_line) - len(next_line.lstrip())
                        new_lines.append(' ' * indent + f'{file_var}.write_text(json.dumps({json_var}, indent=2))')
                        i += 2  # Skip both lines
                        changes += 1
                        continue
        
        new_lines.append(line)
        i += 1
    
    content = '\n'.join(new_lines)
    
    # Fix any remaining unterminated string literals
    content = re.sub(r'f\.write\("([^"]+)\n"\)', r'f.write("\1\\n")', content)
    
    if content != original_content:
        file_path.write_text(content)
        return changes
    return 0


def main():
    """Refactor all test files."""
    test_dir = Path("tests")
    if not test_dir.exists():
        print("❌ tests/ directory not found")
        return
    
    # Target test files that need refactoring
    test_files = [
        "test_extractors.py",
    ]
    
    print(f"🔍 Refactoring {len(test_files)} test file(s)")
    
    total_changes = 0
    for test_file_name in test_files:
        test_file = test_dir / test_file_name
        if test_file.exists():
            changes = refactor_file(test_file)
            total_changes += changes
            if changes > 0:
                print(f"✅ Refactored {test_file_name}: {changes} changes")
            else:
                print(f"ℹ️  No changes needed in {test_file_name}")
    
    print(f"\n✨ Refactoring complete: {total_changes} total changes")
    
    # Run syntax check
    print("\n🧪 Running syntax check...")
    import ast
    import sys
    
    errors = []
    for test_file_name in test_files:
        test_file = test_dir / test_file_name
        if test_file.exists():
            try:
                ast.parse(test_file.read_text())
                print(f"✅ {test_file_name}: Valid syntax")
            except SyntaxError as e:
                errors.append(f"{test_file_name}: Line {e.lineno}: {e.msg}")
    
    if errors:
        print("\n❌ Syntax errors found:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("\n✅ All files have valid syntax")


if __name__ == "__main__":
    main()