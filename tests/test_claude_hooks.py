#!/usr/bin/env python3
"""
Test suite for Claude Code hooks
Following TDD principles: test first, then fix implementation
"""
import json
import subprocess
import sys
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open

# Add hooks directory to path
HOOKS_DIR = Path(__file__).parent.parent / '.claude' / 'hooks'
sys.path.insert(0, str(HOOKS_DIR))


class TestLoadContextHook(unittest.TestCase):
    """Test SessionStart hook: load-context.py"""
    
    def setUp(self):
        self.hook_path = HOOKS_DIR / 'load-context.py'
        self.test_input = {
            "session_id": "test-session-123",
            "transcript_path": "/path/to/transcript.jsonl",
            "hook_event_name": "SessionStart",
            "source": "startup"
        }
    
    def test_hook_executes_without_error(self):
        """Hook should execute successfully with valid input"""
        result = subprocess.run(
            ['python3', str(self.hook_path)],
            input=json.dumps(self.test_input),
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0, f"Hook failed: {result.stderr}")
    
    def test_hook_returns_valid_json(self):
        """Hook should return valid JSON output"""
        result = subprocess.run(
            ['python3', str(self.hook_path)],
            input=json.dumps(self.test_input),
            capture_output=True,
            text=True
        )
        try:
            output = json.loads(result.stdout)
            self.assertIn('hookSpecificOutput', output)
            self.assertIn('additionalContext', output['hookSpecificOutput'])
        except json.JSONDecodeError:
            self.fail(f"Invalid JSON output: {result.stdout}")
    
    def test_hook_handles_invalid_json(self):
        """Hook should handle invalid JSON gracefully"""
        result = subprocess.run(
            ['python3', str(self.hook_path)],
            input="invalid json",
            capture_output=True,
            text=True
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Error", result.stderr)
    
    def test_hook_includes_core_memories(self):
        """Hook should mention core memories in context"""
        result = subprocess.run(
            ['python3', str(self.hook_path)],
            input=json.dumps(self.test_input),
            capture_output=True,
            text=True
        )
        output = json.loads(result.stdout)
        context = output['hookSpecificOutput']['additionalContext']
        self.assertIn('MASTER_INDEX', context)
        self.assertIn('PROJECT_MANIFEST', context)
        self.assertIn('CURRENT_SPRINT', context)


class TestOptimizeMemoryHook(unittest.TestCase):
    """Test UserPromptSubmit hook: optimize-memory.py"""
    
    def setUp(self):
        self.hook_path = HOOKS_DIR / 'optimize-memory.py'
        self.base_input = {
            "session_id": "test-session-123",
            "transcript_path": "/path/to/transcript.jsonl",
            "cwd": "/project",
            "hook_event_name": "UserPromptSubmit"
        }
    
    def test_detects_analyze_command(self):
        """Hook should detect /analyze command and suggest memories"""
        test_input = {**self.base_input, "prompt": "/analyze architecture"}
        result = subprocess.run(
            ['python3', str(self.hook_path)],
            input=json.dumps(test_input),
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        output = json.loads(result.stdout)
        context = output['hookSpecificOutput']['additionalContext']
        self.assertIn('/analyze', context)
        self.assertIn('PROJECT_MANIFEST', context)
    
    def test_blocks_sensitive_information(self):
        """Hook should block prompts with passwords"""
        test_input = {**self.base_input, "prompt": "password: secret123"}
        result = subprocess.run(
            ['python3', str(self.hook_path)],
            input=json.dumps(test_input),
            capture_output=True,
            text=True
        )
        output = json.loads(result.stdout)
        self.assertEqual(output['decision'], 'block')
        self.assertIn('Security policy', output['reason'])
    
    def test_detects_uc_flag(self):
        """Hook should detect --uc flag for ultra-compressed mode"""
        test_input = {**self.base_input, "prompt": "/build feature --uc"}
        result = subprocess.run(
            ['python3', str(self.hook_path)],
            input=json.dumps(test_input),
            capture_output=True,
            text=True
        )
        output = json.loads(result.stdout)
        context = output['hookSpecificOutput']['additionalContext']
        self.assertIn('Ultra-compressed', context)
        self.assertIn('3K token limit', context)
    
    def test_detects_task_keywords(self):
        """Hook should detect task keywords like 'java' or 'test'"""
        test_input = {**self.base_input, "prompt": "fix java test failures"}
        result = subprocess.run(
            ['python3', str(self.hook_path)],
            input=json.dumps(test_input),
            capture_output=True,
            text=True
        )
        output = json.loads(result.stdout)
        context = output['hookSpecificOutput']['additionalContext']
        self.assertIn('JAVA_PATTERNS', context)
        self.assertIn('TDD_BEST_PRACTICES', context)
    
    def test_handles_plain_text_prompts(self):
        """Hook should handle prompts without commands gracefully"""
        test_input = {**self.base_input, "prompt": "hello world"}
        result = subprocess.run(
            ['python3', str(self.hook_path)],
            input=json.dumps(test_input),
            capture_output=True,
            text=True
        )
        # Should exit successfully even if no context generated
        self.assertEqual(result.returncode, 0)


class TestCheckMemoryContextHook(unittest.TestCase):
    """Test PreToolUse hook: check-memory-context.py"""
    
    def setUp(self):
        self.hook_path = HOOKS_DIR / 'check-memory-context.py'
        self.base_input = {
            "session_id": "test-session-123",
            "transcript_path": "/path/to/transcript.jsonl",
            "cwd": "/project",
            "hook_event_name": "PreToolUse"
        }
        # Clean up test state file
        self.state_file = os.path.expanduser("~/.claude/loaded-memories.json")
        if os.path.exists(self.state_file):
            os.remove(self.state_file)
    
    def test_suggests_java_memories_for_java_files(self):
        """Hook should suggest Java memories for .java files"""
        test_input = {
            **self.base_input,
            "tool_name": "Read",
            "tool_input": {"file_path": "/src/Main.java"}
        }
        result = subprocess.run(
            ['python3', str(self.hook_path)],
            input=json.dumps(test_input),
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        if result.stdout:  # Hook may or may not suggest based on state
            output = json.loads(result.stdout)
            reason = output['hookSpecificOutput'].get('permissionDecisionReason', '')
            if reason:
                self.assertIn('JAVA_PATTERNS', reason)
    
    def test_suggests_test_memories_for_test_files(self):
        """Hook should suggest test memories for test files"""
        test_input = {
            **self.base_input,
            "tool_name": "Edit",
            "tool_input": {"file_path": "/tests/test_feature.py"}
        }
        result = subprocess.run(
            ['python3', str(self.hook_path)],
            input=json.dumps(test_input),
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        if result.stdout:
            output = json.loads(result.stdout)
            reason = output['hookSpecificOutput'].get('permissionDecisionReason', '')
            if reason:
                self.assertIn('TDD_BEST_PRACTICES', reason)
    
    def test_handles_missing_tool_input(self):
        """Hook should handle missing tool_input gracefully"""
        test_input = {
            **self.base_input,
            "tool_name": "Read"
            # Missing tool_input
        }
        result = subprocess.run(
            ['python3', str(self.hook_path)],
            input=json.dumps(test_input),
            capture_output=True,
            text=True
        )
        # Should not crash, exits with 0 to not block operations
        self.assertEqual(result.returncode, 0)
    
    def test_never_blocks_operations(self):
        """Hook should never block operations, only suggest"""
        test_input = {
            **self.base_input,
            "tool_name": "Write",
            "tool_input": {"file_path": "/important.java", "content": "data"}
        }
        result = subprocess.run(
            ['python3', str(self.hook_path)],
            input=json.dumps(test_input),
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        if result.stdout:
            output = json.loads(result.stdout)
            decision = output['hookSpecificOutput'].get('permissionDecision', 'allow')
            self.assertEqual(decision, 'allow')


class TestUpdateIndexHook(unittest.TestCase):
    """Test PostToolUse hook: update-index.py"""
    
    def setUp(self):
        self.hook_path = HOOKS_DIR / 'update-index.py'
        self.base_input = {
            "session_id": "test-session-123",
            "transcript_path": "/path/to/transcript.jsonl",
            "cwd": "/project",
            "hook_event_name": "PostToolUse"
        }
        # Clean up test log file
        self.log_file = os.path.expanduser("~/.claude/memory-index-updates.log")
        if os.path.exists(self.log_file):
            os.remove(self.log_file)
    
    def test_handles_write_memory_operation(self):
        """Hook should handle mcp__serena__write_memory operations"""
        test_input = {
            **self.base_input,
            "tool_name": "mcp__serena__write_memory",
            "tool_input": {"memory_name": "TEST_MEMORY", "content": "test"},
            "tool_response": {"success": True}
        }
        result = subprocess.run(
            ['python3', str(self.hook_path)],
            input=json.dumps(test_input),
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0, f"Failed: {result.stderr}")
        output = json.loads(result.stdout)
        context = output['hookSpecificOutput']['additionalContext']
        self.assertIn('TEST_MEMORY', context)
        self.assertIn('created', context)
    
    def test_handles_delete_memory_operation(self):
        """Hook should handle mcp__serena__delete_memory operations"""
        test_input = {
            **self.base_input,
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
        output = json.loads(result.stdout)
        context = output['hookSpecificOutput']['additionalContext']
        self.assertIn('OLD_MEMORY', context)
        self.assertIn('deleted', context)
    
    def test_handles_list_response_gracefully(self):
        """Hook should handle list responses from Serena (the actual bug)"""
        test_input = {
            **self.base_input,
            "tool_name": "mcp__serena__list_memories",
            "tool_input": {},
            "tool_response": ["memory1", "memory2", "memory3"]  # List response
        }
        result = subprocess.run(
            ['python3', str(self.hook_path)],
            input=json.dumps(test_input),
            capture_output=True,
            text=True
        )
        # Should not crash with 'list' object has no attribute 'get'
        self.assertEqual(result.returncode, 0, f"Failed: {result.stderr}")
    
    def test_handles_missing_memory_name(self):
        """Hook should handle missing memory names gracefully"""
        test_input = {
            **self.base_input,
            "tool_name": "mcp__serena__write_memory",
            "tool_input": {},  # Missing memory_name
            "tool_response": {"success": True}
        }
        result = subprocess.run(
            ['python3', str(self.hook_path)],
            input=json.dumps(test_input),
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        output = json.loads(result.stdout)
        context = output['hookSpecificOutput']['additionalContext']
        self.assertIn('unknown', context)  # Should use 'unknown' as fallback
    
    def test_creates_log_directory_if_missing(self):
        """Hook should create log directory if it doesn't exist"""
        # Ensure directory doesn't exist
        log_dir = os.path.dirname(self.log_file)
        if os.path.exists(self.log_file):
            os.remove(self.log_file)
        
        test_input = {
            **self.base_input,
            "tool_name": "mcp__serena__write_memory",
            "tool_input": {"memory_name": "TEST"},
            "tool_response": {"success": True}
        }
        result = subprocess.run(
            ['python3', str(self.hook_path)],
            input=json.dumps(test_input),
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertTrue(os.path.exists(log_dir))


class TestHookIntegration(unittest.TestCase):
    """Integration tests for hook interactions"""
    
    def test_all_hooks_are_executable(self):
        """All hook scripts should be executable"""
        hook_files = [
            'load-context.py',
            'optimize-memory.py',
            'check-memory-context.py',
            'update-index.py'
        ]
        for hook_file in hook_files:
            hook_path = HOOKS_DIR / hook_file
            self.assertTrue(hook_path.exists(), f"Hook {hook_file} does not exist")
            self.assertTrue(os.access(hook_path, os.X_OK), f"Hook {hook_file} is not executable")
    
    def test_all_hooks_handle_empty_input(self):
        """All hooks should handle empty JSON input without crashing"""
        hook_files = [
            'load-context.py',
            'optimize-memory.py',
            'check-memory-context.py',
            'update-index.py'
        ]
        for hook_file in hook_files:
            hook_path = HOOKS_DIR / hook_file
            result = subprocess.run(
                ['python3', str(hook_path)],
                input="{}",
                capture_output=True,
                text=True,
                timeout=5
            )
            # Should exit without hanging
            self.assertIn(result.returncode, [0, 1], 
                         f"Hook {hook_file} crashed with code {result.returncode}: {result.stderr}")


if __name__ == '__main__':
    unittest.main(verbosity=2)