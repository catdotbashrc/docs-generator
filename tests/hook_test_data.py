#!/usr/bin/env python3
"""
Mock data for testing Claude Code hooks
Provides realistic test inputs for different hook scenarios
"""

# SessionStart hook test data
SESSION_START_INPUTS = [
    {
        "description": "Normal startup",
        "input": {
            "session_id": "abc123-def456",
            "transcript_path": "/Users/test/.claude/projects/test/transcript.jsonl",
            "hook_event_name": "SessionStart",
            "source": "startup"
        },
        "expected_output_contains": ["MASTER_INDEX", "PROJECT_MANIFEST", "Memory Architecture Active"]
    },
    {
        "description": "Resume session",
        "input": {
            "session_id": "xyz789-resume",
            "transcript_path": "/Users/test/.claude/projects/test/transcript-resume.jsonl",
            "hook_event_name": "SessionStart",
            "source": "resume"
        },
        "expected_output_contains": ["Quick Loading Patterns", "Core Memories Loading"]
    }
]

# UserPromptSubmit hook test data
USER_PROMPT_INPUTS = [
    {
        "description": "Analyze command with standard flag",
        "input": {
            "session_id": "test-123",
            "transcript_path": "/path/to/transcript.jsonl",
            "cwd": "/project",
            "hook_event_name": "UserPromptSubmit",
            "prompt": "/analyze architecture --standard"
        },
        "expected_decision": None,
        "expected_context_contains": ["PROJECT_MANIFEST", "architecture_analysis", "TECH_STACK"]
    },
    {
        "description": "Build command with ultra-compressed flag",
        "input": {
            "session_id": "test-123",
            "transcript_path": "/path/to/transcript.jsonl",
            "cwd": "/project",
            "hook_event_name": "UserPromptSubmit",
            "prompt": "/build new-feature --uc"
        },
        "expected_decision": None,
        "expected_context_contains": ["Ultra-compressed", "3K token limit"]
    },
    {
        "description": "Sensitive information detection",
        "input": {
            "session_id": "test-123",
            "transcript_path": "/path/to/transcript.jsonl",
            "cwd": "/project",
            "hook_event_name": "UserPromptSubmit",
            "prompt": "set password: mySecretPass123"
        },
        "expected_decision": "block",
        "expected_reason_contains": "Security policy"
    },
    {
        "description": "Java development task",
        "input": {
            "session_id": "test-123",
            "transcript_path": "/path/to/transcript.jsonl",
            "cwd": "/project",
            "hook_event_name": "UserPromptSubmit",
            "prompt": "fix the java parsing bug in the test suite"
        },
        "expected_decision": None,
        "expected_context_contains": ["JAVA_PATTERNS", "TDD_BEST_PRACTICES", "testing_patterns"]
    },
    {
        "description": "Plain conversation",
        "input": {
            "session_id": "test-123",
            "transcript_path": "/path/to/transcript.jsonl",
            "cwd": "/project",
            "hook_event_name": "UserPromptSubmit",
            "prompt": "hello, how are you today?"
        },
        "expected_decision": None,
        "expected_context_contains": []
    }
]

# PreToolUse hook test data
PRE_TOOL_USE_INPUTS = [
    {
        "description": "Reading Java file",
        "input": {
            "session_id": "test-123",
            "transcript_path": "/path/to/transcript.jsonl",
            "cwd": "/project",
            "hook_event_name": "PreToolUse",
            "tool_name": "Read",
            "tool_input": {
                "file_path": "/src/main/java/com/example/Service.java"
            }
        },
        "expected_decision": "allow",
        "expected_suggestions": ["JAVA_PATTERNS", "TDD_BEST_PRACTICES"]
    },
    {
        "description": "Editing test file",
        "input": {
            "session_id": "test-123",
            "transcript_path": "/path/to/transcript.jsonl",
            "cwd": "/project",
            "hook_event_name": "PreToolUse",
            "tool_name": "Edit",
            "tool_input": {
                "file_path": "/tests/test_feature.py",
                "old_string": "assert True",
                "new_string": "assert result == expected"
            }
        },
        "expected_decision": "allow",
        "expected_suggestions": ["TDD_BEST_PRACTICES", "testing_patterns"]
    },
    {
        "description": "Grep for business logic",
        "input": {
            "session_id": "test-123",
            "transcript_path": "/path/to/transcript.jsonl",
            "cwd": "/project",
            "hook_event_name": "PreToolUse",
            "tool_name": "Grep",
            "tool_input": {
                "pattern": "business.*logic|validation.*rule"
            }
        },
        "expected_decision": "allow",
        "expected_suggestions": ["business_logic_extraction_implementation"]
    }
]

# PostToolUse hook test data
POST_TOOL_USE_INPUTS = [
    {
        "description": "Memory write success",
        "input": {
            "session_id": "test-123",
            "transcript_path": "/path/to/transcript.jsonl",
            "cwd": "/project",
            "hook_event_name": "PostToolUse",
            "tool_name": "mcp__serena__write_memory",
            "tool_input": {
                "memory_name": "NEW_FEATURE_SPEC",
                "content": "Feature specification content"
            },
            "tool_response": {
                "success": True
            }
        },
        "expected_context_contains": ["NEW_FEATURE_SPEC", "created", "MASTER_INDEX"]
    },
    {
        "description": "Memory delete success",
        "input": {
            "session_id": "test-123",
            "transcript_path": "/path/to/transcript.jsonl",
            "cwd": "/project",
            "hook_event_name": "PostToolUse",
            "tool_name": "mcp__serena__delete_memory",
            "tool_input": {
                "memory_file_name": "OLD_SESSION_DATA"
            },
            "tool_response": {
                "success": True
            }
        },
        "expected_context_contains": ["OLD_SESSION_DATA", "deleted"]
    },
    {
        "description": "List memories response",
        "input": {
            "session_id": "test-123",
            "transcript_path": "/path/to/transcript.jsonl",
            "cwd": "/project",
            "hook_event_name": "PostToolUse",
            "tool_name": "mcp__serena__list_memories",
            "tool_input": {},
            "tool_response": [
                "PROJECT_MANIFEST",
                "CURRENT_SPRINT",
                "JAVA_PATTERNS",
                "TDD_BEST_PRACTICES"
            ]
        },
        "expected_context_contains": ["Listed 4 memories"]
    },
    {
        "description": "Non-Serena tool (should be ignored)",
        "input": {
            "session_id": "test-123",
            "transcript_path": "/path/to/transcript.jsonl",
            "cwd": "/project",
            "hook_event_name": "PostToolUse",
            "tool_name": "Read",
            "tool_input": {
                "file_path": "/some/file.txt"
            },
            "tool_response": "File content here"
        },
        "expected_context_contains": []
    }
]

# Edge cases and error scenarios
EDGE_CASE_INPUTS = [
    {
        "description": "Empty JSON input",
        "input": {},
        "expected_behavior": "Should not crash"
    },
    {
        "description": "Missing required fields",
        "input": {
            "session_id": "test-123"
            # Missing other fields
        },
        "expected_behavior": "Should handle gracefully"
    },
    {
        "description": "Malformed tool_input",
        "input": {
            "session_id": "test-123",
            "hook_event_name": "PreToolUse",
            "tool_name": "Read"
            # tool_input is missing
        },
        "expected_behavior": "Should not block operation"
    },
    {
        "description": "Unicode in prompt",
        "input": {
            "session_id": "test-123",
            "hook_event_name": "UserPromptSubmit",
            "prompt": "Test с кириллицей 测试中文 🚀"
        },
        "expected_behavior": "Should handle unicode correctly"
    },
    {
        "description": "Very long prompt",
        "input": {
            "session_id": "test-123",
            "hook_event_name": "UserPromptSubmit",
            "prompt": "x" * 10000  # 10K character prompt
        },
        "expected_behavior": "Should handle without performance issues"
    }
]

def get_test_data(hook_name):
    """Get test data for a specific hook"""
    mapping = {
        "SessionStart": SESSION_START_INPUTS,
        "UserPromptSubmit": USER_PROMPT_INPUTS,
        "PreToolUse": PRE_TOOL_USE_INPUTS,
        "PostToolUse": POST_TOOL_USE_INPUTS,
        "EdgeCases": EDGE_CASE_INPUTS
    }
    return mapping.get(hook_name, [])