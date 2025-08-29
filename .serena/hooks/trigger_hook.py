#!/usr/bin/env python3
"""
Hook trigger for DDD automation
Optimized for memory efficiency and context relevance
"""

import sys
import json
from pathlib import Path
from datetime import datetime

def trigger_hook(hook_name: str, *args):
    """Trigger a specific hook with memory optimization"""
    
    # Import automation module
    sys.path.insert(0, str(Path(__file__).parent))
    from ddd_automation import DddWorkflowAutomation
    
    automation = DddWorkflowAutomation(Path.cwd())
    
    # Map hook names to methods
    hook_map = {
        "post_measure": automation.on_measure_command,
        "post_assert_failure": automation.on_assert_coverage,
        "post_demo": automation.on_demo_command
    }
    
    if hook_name in hook_map:
        target_path = args[0] if args else "."
        hook_map[hook_name](target_path)
        
        # Log hook execution (memory efficient - rolling log)
        log_file = Path(".serena/hooks/automation.log")
        log_entry = f"{datetime.now().isoformat()} - {hook_name} - {target_path}\n"
        
        # Keep only last 100 lines (memory efficiency)
        if log_file.exists():
            lines = log_file.read_text().split('\n')[-99:]
            log_file.write_text('\n'.join(lines) + '\n' + log_entry)
        else:
            log_file.write_text(log_entry)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        trigger_hook(sys.argv[1], *sys.argv[2:])
