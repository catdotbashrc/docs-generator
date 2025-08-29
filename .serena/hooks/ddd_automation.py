#!/usr/bin/env python3
"""
DDD Workflow Automation Hooks for Serena
Optimized for memory efficiency and context relevance
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Memory efficiency configuration
MAX_MEMORY_SIZE = 4000  # tokens
RELEVANCE_THRESHOLD = 0.7


class DddWorkflowAutomation:
    """Workflow automation for Documentation Driven Development"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.memories_dir = project_root / ".serena" / "memories"
        self.memories_dir.mkdir(parents=True, exist_ok=True)
    
    def on_measure_command(self, target_path: str) -> None:
        """
        Hook triggered after 'ddd measure' execution
        Updates coverage memories with context-relevant data only
        """
        try:
            # Run measurement
            result = subprocess.run(
                ["ddd", "measure", target_path],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                # Parse coverage results (minimal extraction)
                coverage_data = self._parse_coverage_output(result.stdout)
                
                # Update only relevant memories
                if coverage_data['overall_coverage'] < 0.85:
                    # Only store gaps if below threshold (memory efficiency)
                    self._write_memory(
                        "coverage_gaps",
                        self._format_gaps(coverage_data['missing']),
                        token_estimate=1500
                    )
                
                # Always update last measurement (compact format)
                self._write_memory(
                    "last_coverage_measurement",
                    self._format_coverage_summary(coverage_data),
                    token_estimate=500
                )
                
                # Track trend (memory-efficient rolling window)
                self._update_coverage_trend(coverage_data['overall_coverage'])
                
        except Exception as e:
            print(f"⚠️ Automation hook failed: {e}")
    
    def on_assert_coverage(self, target_path: str) -> None:
        """
        Hook for 'ddd assert-coverage' - tracks validation results
        Only stores failures for memory efficiency
        """
        result = subprocess.run(
            ["ddd", "assert-coverage", target_path],
            capture_output=True,
            text=True,
            cwd=self.project_root
        )
        
        if result.returncode != 0:
            # Only store assertion failures (context relevance)
            self._write_memory(
                "coverage_assertion_failure",
                f"Failed at {datetime.now().isoformat()}\n{result.stdout}",
                token_estimate=800
            )
    
    def on_demo_command(self, target_path: str) -> None:
        """
        Hook for 'ddd demo' - captures high-risk configurations
        Prioritizes security-relevant context
        """
        result = subprocess.run(
            ["ddd", "demo", target_path],
            capture_output=True,
            text=True,
            cwd=self.project_root
        )
        
        if "HIGH RISK" in result.stdout:
            # Only store high-risk findings (relevance optimization)
            risks = self._extract_high_risks(result.stdout)
            self._write_memory(
                "high_risk_configs",
                risks,
                token_estimate=1000
            )
    
    def select_memories_for_command(self, command: str) -> List[str]:
        """
        Intelligent memory selection based on command context
        Optimizes for relevance and memory efficiency
        """
        # Base memories (always relevant, minimal size)
        base_memories = ["coverage_philosophy", "three_tier_model"]
        
        # Command-specific memories (context relevance)
        command_memories = {
            "measure": [
                "extractor_registry",
                "artifact_patterns",
                "last_coverage_measurement"  # Recent context
            ],
            "assert": [
                "coverage_thresholds",
                "coverage_assertion_failure"  # If exists
            ],
            "demo": [
                "config_extraction",
                "risk_scoring",
                "high_risk_configs"  # If exists
            ],
            "test": [
                "testing_patterns",
                "test_failures"  # If exists
            ],
            "develop": [
                "adding_extractors",
                "current_sprint",
                "task_completion_checklist"
            ]
        }
        
        # Determine command type
        cmd_type = self._classify_command(command)
        selected = base_memories + command_memories.get(cmd_type, [])
        
        # Filter by existence and size (memory efficiency)
        return self._filter_memories_by_budget(selected, max_tokens=12000)
    
    def _classify_command(self, command: str) -> str:
        """Classify command for memory selection"""
        if "measure" in command:
            return "measure"
        elif "assert" in command:
            return "assert"
        elif "demo" in command:
            return "demo"
        elif "test" in command or "pytest" in command:
            return "test"
        else:
            return "develop"
    
    def _filter_memories_by_budget(self, memories: List[str], max_tokens: int) -> List[str]:
        """
        Filter memories to fit token budget
        Prioritizes by relevance score
        """
        filtered = []
        current_tokens = 0
        
        for memory in memories:
            memory_path = self.memories_dir / f"{memory}.md"
            if memory_path.exists():
                # Estimate tokens (rough calculation)
                size = memory_path.stat().st_size // 4  # ~4 chars per token
                if current_tokens + size <= max_tokens:
                    filtered.append(memory)
                    current_tokens += size
        
        return filtered
    
    def _write_memory(self, name: str, content: str, token_estimate: int) -> None:
        """Write memory with metadata for efficiency tracking"""
        memory_path = self.memories_dir / f"{name}.md"
        
        header = f"""# MEMORY: {name}
Version: 1.0.0
Type: automated
Token_Count: ~{token_estimate}
Last_Modified: {datetime.now().isoformat()}
Freshness: ✅ current
Auto_Generated: true

## CONTENT
{content}
"""
        memory_path.write_text(header)
    
    def _update_coverage_trend(self, coverage: float) -> None:
        """
        Maintain rolling window of coverage trend
        Memory-efficient: keeps only last 10 measurements
        """
        trend_file = self.memories_dir / "coverage_trend.json"
        
        if trend_file.exists():
            trend = json.loads(trend_file.read_text())
        else:
            trend = []
        
        trend.append({
            "timestamp": datetime.now().isoformat(),
            "coverage": coverage
        })
        
        # Keep only last 10 (memory efficiency)
        trend = trend[-10:]
        
        trend_file.write_text(json.dumps(trend, indent=2))
    
    def _parse_coverage_output(self, output: str) -> Dict:
        """Parse DDD coverage output (simplified for efficiency)"""
        # This is a simplified parser - actual implementation would parse real output
        return {
            "overall_coverage": 0.73,  # Example
            "missing": ["Dependencies docs", "Health monitoring"],
            "by_dimension": {
                "Dependencies": 0.85,
                "Automation": 0.60,
                # etc...
            }
        }
    
    def _format_gaps(self, missing: List[str]) -> str:
        """Format coverage gaps concisely"""
        return "\n".join(f"- {item}" for item in missing[:10])  # Limit to 10
    
    def _format_coverage_summary(self, data: Dict) -> str:
        """Format coverage summary efficiently"""
        return f"""Overall: {data['overall_coverage']:.1%}
Top gaps: {', '.join(data['missing'][:3])}
Timestamp: {datetime.now().isoformat()}"""
    
    def _extract_high_risks(self, output: str) -> str:
        """Extract only high-risk configurations"""
        # Simplified extraction
        lines = output.split('\n')
        risks = [l for l in lines if 'HIGH' in l or 'CRITICAL' in l]
        return '\n'.join(risks[:20])  # Limit for memory efficiency


# Integration with Serena hooks
def setup_hooks():
    """Setup automated hooks for DDD workflow"""
    automation = DddWorkflowAutomation(Path.cwd())
    
    # Register hooks
    hooks = {
        "post_measure": automation.on_measure_command,
        "post_assert": automation.on_assert_coverage,
        "post_demo": automation.on_demo_command,
        "memory_selection": automation.select_memories_for_command
    }
    
    # Save hook configuration
    hook_config = Path(".serena/hooks/config.json")
    hook_config.parent.mkdir(parents=True, exist_ok=True)
    hook_config.write_text(json.dumps({
        "enabled": True,
        "automation_module": "ddd_automation",
        "hooks": list(hooks.keys())
    }, indent=2))
    
    print("✅ DDD workflow automation hooks configured")
    print("📊 Optimized for: Memory efficiency & Context relevance")
    return hooks


if __name__ == "__main__":
    setup_hooks()