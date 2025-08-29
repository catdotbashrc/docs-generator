#!/usr/bin/env python3
"""
Coverage Tracking Automation for DDD Framework
Works with Serena's memory system for automatic tracking
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

# Serena memory directory
MEMORY_DIR = Path(".serena/memories")
MEMORY_DIR.mkdir(parents=True, exist_ok=True)


def write_memory(name: str, content: Any) -> None:
    """Write a memory file for Serena"""
    memory_path = MEMORY_DIR / f"{name}.md"
    
    if isinstance(content, dict):
        content = json.dumps(content, indent=2)
    
    # Format as proper memory file
    memory_content = f"""# MEMORY: {name}
Version: 1.0.0
Type: tracking
Token_Count: ~1K
Last_Modified: {datetime.now().isoformat()}
Freshness: ✅ current

## CONTENT
{content}
"""
    
    memory_path.write_text(memory_content)
    print(f"✓ Updated memory: {name}")


def read_memory(name: str) -> Optional[str]:
    """Read a memory file"""
    memory_path = MEMORY_DIR / f"{name}.md"
    if memory_path.exists():
        content = memory_path.read_text()
        # Extract content after ## CONTENT
        if "## CONTENT" in content:
            return content.split("## CONTENT")[1].strip()
    return None


def run_coverage_analysis(project_path: str = ".") -> Dict[str, Any]:
    """Run ddd measure and capture results"""
    try:
        result = subprocess.run(
            ["python", "-m", "ddd", "measure", project_path],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Parse output for coverage metrics
        output = result.stdout
        
        # Extract coverage percentage (looking for pattern like "85.2%")
        import re
        coverage_match = re.search(r'(\d+\.?\d*)%', output)
        coverage = float(coverage_match.group(1)) / 100 if coverage_match else 0.0
        
        # Extract dimension scores if available
        dimension_scores = {}
        for line in output.split('\n'):
            if 'Dependencies' in line:
                score_match = re.search(r'(\d+\.?\d*)%', line)
                if score_match:
                    dimension_scores['Dependencies'] = float(score_match.group(1)) / 100
            # Add other dimensions as needed
        
        return {
            'success': True,
            'coverage': coverage,
            'dimension_scores': dimension_scores,
            'timestamp': datetime.now().isoformat(),
            'raw_output': output
        }
        
    except subprocess.CalledProcessError as e:
        return {
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat(),
            'stderr': e.stderr
        }


def update_coverage_tracking(result: Dict[str, Any]) -> None:
    """Update Serena memories with coverage results"""
    
    if result['success']:
        coverage = result['coverage']
        
        # Update current coverage
        write_memory("CURRENT_COVERAGE", {
            'coverage': f"{coverage:.1%}",
            'timestamp': result['timestamp'],
            'status': 'PASSING' if coverage >= 0.85 else 'FAILING',
            'dimension_scores': result.get('dimension_scores', {})
        })
        
        # Track coverage gaps if failing
        if coverage < 0.85:
            gap = 0.85 - coverage
            write_memory("COVERAGE_GAPS", {
                'gap': f"{gap:.1%} below threshold",
                'current': f"{coverage:.1%}",
                'required': "85.0%",
                'timestamp': result['timestamp'],
                'action_needed': "Improve documentation coverage"
            })
        else:
            # Clean up gaps memory if passing
            gaps_path = MEMORY_DIR / "COVERAGE_GAPS.md"
            if gaps_path.exists():
                gaps_path.unlink()
                print("✓ Removed COVERAGE_GAPS (now passing)")
        
        # Update coverage history
        history = read_memory("COVERAGE_HISTORY")
        if history:
            try:
                history_data = json.loads(history)
            except:
                history_data = []
        else:
            history_data = []
        
        history_data.append({
            'coverage': coverage,
            'timestamp': result['timestamp']
        })
        
        # Keep last 10 entries
        history_data = history_data[-10:]
        write_memory("COVERAGE_HISTORY", history_data)
        
        # Calculate trend
        if len(history_data) >= 2:
            trend = history_data[-1]['coverage'] - history_data[-2]['coverage']
            trend_symbol = "📈" if trend > 0 else "📉" if trend < 0 else "➡️"
            write_memory("COVERAGE_TREND", {
                'direction': trend_symbol,
                'change': f"{trend:+.1%}",
                'current': f"{coverage:.1%}",
                'previous': f"{history_data[-2]['coverage']:.1%}"
            })
        
    else:
        # Track extraction failure
        write_memory("EXTRACTION_ERROR", {
            'error': result.get('error', 'Unknown error'),
            'timestamp': result['timestamp'],
            'stderr': result.get('stderr', '')
        })


def run_test_tracking() -> None:
    """Track test results"""
    try:
        result = subprocess.run(
            ["pytest", "--tb=short", "-q"],
            capture_output=True,
            text=True
        )
        
        # Parse test results
        output = result.stdout
        passed = output.count(" passed")
        failed = output.count(" failed")
        
        test_status = {
            'passed': passed,
            'failed': failed,
            'total': passed + failed,
            'status': 'PASSING' if failed == 0 else 'FAILING',
            'timestamp': datetime.now().isoformat()
        }
        
        write_memory("TEST_STATUS", test_status)
        
        if failed > 0:
            # Extract failed test names
            failed_tests = []
            for line in output.split('\n'):
                if 'FAILED' in line:
                    failed_tests.append(line.strip())
            
            write_memory("TEST_FAILURES", {
                'count': failed,
                'tests': failed_tests[:10],  # Keep first 10
                'timestamp': datetime.now().isoformat()
            })
        else:
            # Clean up failures memory if all passing
            failures_path = MEMORY_DIR / "TEST_FAILURES.md"
            if failures_path.exists():
                failures_path.unlink()
                print("✓ Removed TEST_FAILURES (all passing)")
                
    except Exception as e:
        write_memory("TEST_ERROR", {
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        })


def create_session_checkpoint() -> None:
    """Create a session checkpoint"""
    checkpoint_name = f"SESSION_checkpoint_{datetime.now():%Y%m%d_%H%M}"
    
    # Gather current state
    current_coverage = read_memory("CURRENT_COVERAGE")
    test_status = read_memory("TEST_STATUS")
    
    checkpoint = {
        'timestamp': datetime.now().isoformat(),
        'coverage': current_coverage if current_coverage else "Not measured",
        'tests': test_status if test_status else "Not run",
    }
    
    write_memory(checkpoint_name, checkpoint)
    
    # Also update "latest" checkpoint
    write_memory("SESSION_latest", checkpoint)
    
    # Clean old checkpoints (keep last 5)
    checkpoints = sorted([f for f in MEMORY_DIR.glob("SESSION_checkpoint_*.md")])
    if len(checkpoints) > 5:
        for old_checkpoint in checkpoints[:-5]:
            old_checkpoint.unlink()
            print(f"✓ Cleaned old checkpoint: {old_checkpoint.name}")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="DDD Coverage Tracking Automation")
    parser.add_argument("command", choices=["coverage", "test", "checkpoint", "all"],
                       help="What to track")
    parser.add_argument("--path", default=".", help="Project path for coverage analysis")
    
    args = parser.parse_args()
    
    if args.command == "coverage":
        print("📊 Running coverage analysis...")
        result = run_coverage_analysis(args.path)
        update_coverage_tracking(result)
        
        if result['success']:
            coverage = result['coverage']
            status = "✅ PASSING" if coverage >= 0.85 else "❌ FAILING"
            print(f"\nCoverage: {coverage:.1%} - {status}")
        else:
            print(f"\n❌ Coverage analysis failed: {result.get('error')}")
    
    elif args.command == "test":
        print("🧪 Running test tracking...")
        run_test_tracking()
    
    elif args.command == "checkpoint":
        print("💾 Creating session checkpoint...")
        create_session_checkpoint()
    
    elif args.command == "all":
        print("🔄 Running complete tracking suite...")
        
        # Run coverage
        print("\n📊 Coverage analysis...")
        result = run_coverage_analysis(args.path)
        update_coverage_tracking(result)
        
        # Run tests
        print("\n🧪 Test tracking...")
        run_test_tracking()
        
        # Create checkpoint
        print("\n💾 Creating checkpoint...")
        create_session_checkpoint()
        
        print("\n✅ Complete tracking finished!")


if __name__ == "__main__":
    main()