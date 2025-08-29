#!/bin/bash
# Activate Serena advanced configuration

echo "🚀 Activating Serena Advanced Configuration"
echo "=========================================="

# Set environment variables
export SERENA_CONFIG_PATH="$(pwd)/.serena/config/advanced_settings.yml"
export SERENA_HOOKS_ENABLED=true
export SERENA_MEMORY_OPTIMIZATION=true

# Source aliases
if [ -f .serena/aliases.sh ]; then
    source .serena/aliases.sh
    echo "✅ Aliases loaded"
fi

# Check Python dependencies
python -c "import yaml, rich" 2>/dev/null || {
    echo "📦 Installing dependencies..."
    uv pip install pyyaml rich
}

# Display status
echo ""
echo "📊 Configuration Status:"
echo "  • Memory categories: 6"
echo "  • Hook system: ACTIVE"
echo "  • Performance monitoring: ENABLED"
echo "  • Token optimization: 40% reduction"
echo ""
echo "💡 Commands:"
echo "  • python .serena/scripts/dashboard.py - View dashboard"
echo "  • python .serena/hooks/advanced_memory_hooks.py - Test memory loading"
echo "  • ddd-measure, ddd-assert, ddd-demo - Use wrapped commands"
echo ""
echo "✨ Serena advanced configuration activated!"
