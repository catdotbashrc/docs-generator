# UV PYTHONPATH Guidance
Date: 2025-08-28
Type: implementation
Dependencies: []

## Key Learning: UV Handles PYTHONPATH Automatically

When using `uv run`, the tool automatically manages the Python path and environment. DO NOT prefix commands with `PYTHONPATH=.` when using UV.

### Correct Usage
```bash
# ✅ CORRECT - UV handles environment setup
uv run pytest tests/test_file.py -v

# ✅ CORRECT - UV ensures proper module resolution
uv run python -m module_name
```

### Incorrect Usage
```bash
# ❌ WRONG - Do not add PYTHONPATH manually
PYTHONPATH=. uv run pytest tests/test_file.py -v
```

### Why UV Doesn't Need PYTHONPATH

1. **Automatic Environment Management**: `uv run` ensures the lockfile and environment are synchronized with `pyproject.toml` before execution
2. **Project Context**: UV automatically sets up the project environment including proper Python paths
3. **Virtual Environment Integration**: UV manages the `VIRTUAL_ENV` environment variable and ensures proper module resolution
4. **Consistent Execution**: Guarantees a consistent and locked execution context without manual environment configuration

### Related Environment Variables UV Manages
- `VIRTUAL_ENV`: Automatically set by `uv run`
- `UV`: Path to UV binary propagated to subprocesses
- `UV_PROJECT_ENVIRONMENT`: Can override project venv path if needed

This approach ensures consistent test execution across different environments without manual PYTHONPATH configuration.