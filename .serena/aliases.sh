# DDD Workflow Aliases with Automation
# Source this file: source .serena/aliases.sh

alias ddd-measure='.serena/hooks/ddd_wrapper.sh measure'
alias ddd-assert='.serena/hooks/ddd_wrapper.sh assert-coverage'
alias ddd-demo='.serena/hooks/ddd_wrapper.sh demo'

# Quick commands with automatic memory optimization
alias ddd-check='ddd-measure . && echo "✅ Coverage tracked"'
alias ddd-validate='ddd-assert . && echo "✅ Validation tracked"'
alias ddd-show='ddd-demo . && echo "✅ Demo tracked"'

# Memory management shortcuts
alias ddd-memories='ls -la .serena/memories/*.md | tail -10'
alias ddd-clean='find .serena/memories -name "session_checkpoint_*" -mtime +7 -delete'
alias ddd-usage='du -sh .serena/memories'

echo "📊 DDD automation aliases loaded"
echo "   Memory optimization: ENABLED"
echo "   Context relevance: OPTIMIZED"
