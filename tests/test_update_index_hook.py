#!/usr/bin/env python3
"""
Proper tests for update-index.py hook that verify actual functionality
Following TDD: tests should verify behavior, not just pass
"""
import json
import subprocess
import sys
import os
import tempfile
import unittest
from pathlib import Path

HOOKS_DIR = Path(__file__).parent.parent / '.claude' / 'hooks'
sys.path.insert(0, str(HOOKS_DIR))


class TestUpdateIndexHookFunctionality(unittest.TestCase):
    """Test that update-index.py actually works correctly"""
    
    def setUp(self):
        self.hook_path = HOOKS_DIR / 'update-index.py'
        self.log_file = os.path.expanduser("~/.claude/memory-index-updates.log")
        # Clean log before each test
        if os.path.exists(self.log_file):
            os.remove(self.log_file)
    
    def tearDown(self):
        # Clean up after tests
        if os.path.exists(self.log_file):
            os.remove(self.log_file)
    
    def test_write_memory_creates_correct_log_entry(self):
        """Writing memory should create proper log entry with all details"""
        test_input = {
            "session_id": "test-123",
            "hook_event_name": "PostToolUse",
            "tool_name": "mcp__serena__write_memory",
            "tool_input": {"memory_name": "TEST_MEMORY", "content": "test content"},
            "tool_response": {"success": True}
        }
        
        result = subprocess.run(
            ['python3', str(self.hook_path)],
            input=json.dumps(test_input),
            capture_output=True,
            text=True
        )
        
        # Should succeed
        self.assertEqual(result.returncode, 0, f"Hook failed: {result.stderr}")
        
        # Should create log file
        self.assertTrue(os.path.exists(self.log_file))
        
        # Verify log content
        with open(self.log_file, 'r') as f:
            log_content = f.read()
            log_entry = json.loads(log_content.strip())
            
            self.assertEqual(log_entry['operation'], 'created')
            self.assertEqual(log_entry['memory'], 'TEST_MEMORY')
            self.assertTrue(log_entry['success'])
            self.assertIn('timestamp', log_entry)
        
        # Verify output message
        output = json.loads(result.stdout)
        context = output['hookSpecificOutput']['additionalContext']
        self.assertIn('TEST_MEMORY created', context)
    
    def test_delete_memory_creates_correct_log_entry(self):
        """Deleting memory should create proper log entry"""
        test_input = {
            "tool_name": "mcp__serena__delete_memory",
            "tool_input": {"memory_file_name": "OLD_MEMORY"},
            "tool_response": {"success": True}
        }
        
        result = subprocess.run(
            ['python3', str(self.hook_path)],
            input=json.dumps(test_input),
            capture_output=True,
            text=True
        )
        
        self.assertEqual(result.returncode, 0)
        
        with open(self.log_file, 'r') as f:
            log_entry = json.loads(f.read().strip())
            self.assertEqual(log_entry['operation'], 'deleted')
            self.assertEqual(log_entry['memory'], 'OLD_MEMORY')
    
    def test_list_memories_logs_count_and_samples(self):
        """List operation should log count and sample of memories"""
        memories = ["MEM1", "MEM2", "MEM3", "MEM4", "MEM5", "MEM6", "MEM7"]
        test_input = {
            "tool_name": "mcp__serena__list_memories",
            "tool_input": {},
            "tool_response": memories
        }
        
        result = subprocess.run(
            ['python3', str(self.hook_path)],
            input=json.dumps(test_input),
            capture_output=True,
            text=True
        )
        
        self.assertEqual(result.returncode, 0)
        
        with open(self.log_file, 'r') as f:
            log_entry = json.loads(f.read().strip())
            self.assertEqual(log_entry['operation'], 'list')
            self.assertEqual(log_entry['count'], 7)
            # Should only log first 5
            self.assertEqual(len(log_entry['memories']), 5)
            self.assertEqual(log_entry['memories'], memories[:5])
    
    def test_missing_memory_name_fails_properly(self):
        """Missing required field should fail with clear error"""
        test_input = {
            "tool_name": "mcp__serena__write_memory",
            "tool_input": {"content": "test"},  # Missing memory_name
            "tool_response": {"success": True}
        }
        
        result = subprocess.run(
            ['python3', str(self.hook_path)],
            input=json.dumps(test_input),
            capture_output=True,
            text=True
        )
        
        # Should fail
        self.assertEqual(result.returncode, 1)
        # Should have clear error message
        self.assertIn("write_memory requires 'memory_name'", result.stderr)
        # Should NOT create log entry for failed operation
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as f:
                self.assertEqual(f.read(), "")
    
    def test_wrong_response_type_fails_properly(self):
        """Wrong response type should fail with clear error"""
        test_input = {
            "tool_name": "mcp__serena__list_memories",
            "tool_input": {},
            "tool_response": {"not": "a list"}  # Should be a list
        }
        
        result = subprocess.run(
            ['python3', str(self.hook_path)],
            input=json.dumps(test_input),
            capture_output=True,
            text=True
        )
        
        self.assertEqual(result.returncode, 1)
        self.assertIn("Expected list response", result.stderr)
    
    def test_non_serena_operations_ignored(self):
        """Non-Serena operations should be ignored silently"""
        test_input = {
            "tool_name": "Read",
            "tool_input": {"file_path": "/test.txt"},
            "tool_response": "file content"
        }
        
        result = subprocess.run(
            ['python3', str(self.hook_path)],
            input=json.dumps(test_input),
            capture_output=True,
            text=True
        )
        
        # Should exit cleanly
        self.assertEqual(result.returncode, 0)
        # Should not create log
        self.assertFalse(os.path.exists(self.log_file))
        # Should not produce output
        self.assertEqual(result.stdout, "")
    
    def test_multiple_operations_append_to_log(self):
        """Multiple operations should append to the same log file"""
        operations = [
            {
                "tool_name": "mcp__serena__write_memory",
                "tool_input": {"memory_name": "MEM1"},
                "tool_response": {"success": True}
            },
            {
                "tool_name": "mcp__serena__write_memory", 
                "tool_input": {"memory_name": "MEM2"},
                "tool_response": {"success": True}
            },
            {
                "tool_name": "mcp__serena__delete_memory",
                "tool_input": {"memory_file_name": "MEM1"},
                "tool_response": {"success": True}
            }
        ]
        
        for op in operations:
            subprocess.run(
                ['python3', str(self.hook_path)],
                input=json.dumps(op),
                capture_output=True,
                text=True
            )
        
        # Should have 3 log entries
        with open(self.log_file, 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 3)
            
            # Verify each operation
            log1 = json.loads(lines[0])
            self.assertEqual(log1['operation'], 'created')
            self.assertEqual(log1['memory'], 'MEM1')
            
            log2 = json.loads(lines[1])
            self.assertEqual(log2['operation'], 'created')
            self.assertEqual(log2['memory'], 'MEM2')
            
            log3 = json.loads(lines[2])
            self.assertEqual(log3['operation'], 'deleted')
            self.assertEqual(log3['memory'], 'MEM1')


if __name__ == '__main__':
    unittest.main(verbosity=2)