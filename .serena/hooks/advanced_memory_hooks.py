#!/usr/bin/env python3
"""
Advanced Memory Management Hooks for Serena MCP
Implements intelligent memory loading, caching, and lifecycle management
"""

import json
import hashlib
import time
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import re


@dataclass
class MemoryMetadata:
    """Metadata for memory files"""
    name: str
    category: str
    version: str
    token_count: int
    last_modified: datetime
    freshness: str
    dependencies: List[str]
    relevance_score: float = 0.0
    access_count: int = 0
    last_accessed: Optional[datetime] = None


class AdvancedMemoryManager:
    """Advanced memory management with intelligent loading and caching"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.memories_dir = project_root / ".serena" / "memories"
        self.cache_dir = project_root / ".serena" / "cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Load configuration
        self.config = self._load_config()
        
        # Initialize caches
        self.memory_cache: Dict[str, str] = {}
        self.metadata_cache: Dict[str, MemoryMetadata] = {}
        self.relevance_scores: Dict[str, float] = {}
        
        # Performance metrics
        self.metrics = {
            "load_times": [],
            "cache_hits": 0,
            "cache_misses": 0,
            "total_tokens_loaded": 0,
            "relevance_scores": []
        }
    
    def _load_config(self) -> Dict:
        """Load advanced configuration"""
        config_path = self.project_root / ".serena" / "config" / "advanced_settings.yml"
        if config_path.exists():
            import yaml
            with open(config_path) as f:
                return yaml.safe_load(f)
        return {}
    
    def select_memories_for_context(self, 
                                   command: str, 
                                   current_file: Optional[str] = None,
                                   max_tokens: int = 15000) -> List[str]:
        """
        Intelligently select memories based on context
        Implements multi-factor scoring and priority loading
        """
        start_time = time.time()
        
        # 1. Analyze context
        context = self._analyze_context(command, current_file)
        
        # 2. Get candidate memories
        candidates = self._get_candidate_memories(context)
        
        # 3. Score memories for relevance
        scored_memories = self._score_memories(candidates, context)
        
        # 4. Apply token budget optimization
        selected = self._optimize_token_budget(scored_memories, max_tokens)
        
        # 5. Update metrics
        load_time = time.time() - start_time
        self.metrics["load_times"].append(load_time)
        
        return selected
    
    def _analyze_context(self, command: str, current_file: Optional[str]) -> Dict:
        """Analyze command and file context"""
        context = {
            "command": command,
            "command_type": self._classify_command(command),
            "file": current_file,
            "file_type": self._get_file_type(current_file) if current_file else None,
            "timestamp": datetime.now(),
            "session_age": self._get_session_age()
        }
        
        # Add DDD-specific context
        if "measure" in command:
            context["operation"] = "coverage_measurement"
            context["needs"] = ["extractors", "algorithms", "specs"]
        elif "assert" in command:
            context["operation"] = "coverage_validation"
            context["needs"] = ["thresholds", "algorithms"]
        elif "demo" in command:
            context["operation"] = "demonstration"
            context["needs"] = ["mvp", "risk_scoring", "examples"]
        
        return context
    
    def _get_candidate_memories(self, context: Dict) -> List[Path]:
        """Get candidate memories based on context"""
        candidates = []
        
        # Always include core memories
        core_dir = self.memories_dir / "core"
        if core_dir.exists():
            candidates.extend(core_dir.glob("*.md"))
        
        # Add category-specific memories based on operation
        if context.get("operation") == "coverage_measurement":
            coverage_dir = self.memories_dir / "coverage"
            if coverage_dir.exists():
                candidates.extend(coverage_dir.glob("*.md"))
        
        if context.get("operation") == "demonstration":
            impl_dir = self.memories_dir / "implementation"
            if impl_dir.exists():
                candidates.extend(impl_dir.glob("*.md"))
        
        # Add recent session memories if needed
        if context.get("session_age", 0) < 3600:  # Within last hour
            sessions_dir = self.memories_dir / "sessions"
            if sessions_dir.exists():
                recent = sorted(sessions_dir.glob("*.md"), 
                              key=lambda p: p.stat().st_mtime)[-1:]
                candidates.extend(recent)
        
        return candidates
    
    def _score_memories(self, candidates: List[Path], context: Dict) -> List[Tuple[Path, float]]:
        """Score memories for relevance"""
        scored = []
        
        for memory_path in candidates:
            score = 0.0
            
            # Parse metadata
            metadata = self._parse_memory_metadata(memory_path)
            
            # Factor 1: Command relevance (40%)
            if self._matches_command_pattern(memory_path.name, context["command"]):
                score += 0.4
            
            # Factor 2: Recency (20%)
            if metadata and metadata.freshness == "✅ current":
                score += 0.2
            elif metadata and metadata.freshness == "🔄 review":
                score += 0.1
            
            # Factor 3: Dependency satisfaction (20%)
            if metadata and context.get("needs"):
                for need in context["needs"]:
                    if need in memory_path.stem.lower():
                        score += 0.2 / len(context["needs"])
            
            # Factor 4: Access patterns (10%)
            if metadata and metadata.access_count > 5:
                score += 0.1
            
            # Factor 5: Category match (10%)
            category = memory_path.parent.name
            if category in ["core"]:
                score += 0.1  # Core always relevant
            elif context.get("operation") and category in context["operation"]:
                score += 0.1
            
            scored.append((memory_path, score))
        
        # Sort by score descending
        return sorted(scored, key=lambda x: x[1], reverse=True)
    
    def _optimize_token_budget(self, 
                              scored_memories: List[Tuple[Path, float]], 
                              max_tokens: int) -> List[str]:
        """Optimize memory selection within token budget"""
        selected = []
        used_tokens = 0
        
        for memory_path, score in scored_memories:
            # Skip if relevance too low
            if score < 0.3:
                continue
            
            # Get token count
            metadata = self._parse_memory_metadata(memory_path)
            tokens = metadata.token_count if metadata else 1000  # Default estimate
            
            # Check if fits in budget
            if used_tokens + tokens <= max_tokens:
                selected.append(str(memory_path.relative_to(self.memories_dir)))
                used_tokens += tokens
                self.relevance_scores[memory_path.name] = score
            elif score > 0.8:  # High relevance - try compression
                compressed = self._compress_memory(memory_path)
                if compressed and len(compressed) < tokens * 0.6:
                    selected.append(f"compressed:{memory_path.name}")
                    used_tokens += int(tokens * 0.6)
        
        self.metrics["total_tokens_loaded"] = used_tokens
        self.metrics["relevance_scores"] = list(self.relevance_scores.values())
        
        return selected
    
    def _compress_memory(self, memory_path: Path) -> Optional[str]:
        """Compress memory while preserving key information"""
        try:
            content = memory_path.read_text()
            
            # Extract key sections
            summary = self._extract_section(content, "SUMMARY")
            key_points = self._extract_section(content, "KEY")
            usage = self._extract_section(content, "USAGE")
            
            compressed = f"# {memory_path.stem} (Compressed)\n"
            if summary:
                compressed += f"\n{summary}\n"
            if key_points:
                compressed += f"\n## Key Points\n{key_points}\n"
            if usage:
                compressed += f"\n## Usage\n{usage}\n"
            
            return compressed if len(compressed) < len(content) * 0.6 else None
            
        except Exception:
            return None
    
    def _extract_section(self, content: str, section: str) -> Optional[str]:
        """Extract a section from memory content"""
        pattern = rf"##\s*{section}.*?\n(.*?)(?=\n##|\Z)"
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else None
    
    def _parse_memory_metadata(self, memory_path: Path) -> Optional[MemoryMetadata]:
        """Parse metadata from memory file"""
        if memory_path in self.metadata_cache:
            return self.metadata_cache[memory_path]
        
        try:
            content = memory_path.read_text()
            lines = content.split('\n')[:20]  # Check first 20 lines
            
            metadata = MemoryMetadata(
                name=memory_path.stem,
                category=memory_path.parent.name,
                version="1.0.0",
                token_count=len(content) // 4,  # Rough estimate
                last_modified=datetime.fromtimestamp(memory_path.stat().st_mtime),
                freshness="✅ current",
                dependencies=[]
            )
            
            # Parse metadata fields
            for line in lines:
                if line.startswith("Version:"):
                    metadata.version = line.split(":", 1)[1].strip()
                elif line.startswith("Token_Count:"):
                    count = line.split(":", 1)[1].strip()
                    metadata.token_count = int(re.search(r'\d+', count).group())
                elif line.startswith("Freshness:"):
                    metadata.freshness = line.split(":", 1)[1].strip()
                elif line.startswith("Dependencies:"):
                    deps = line.split(":", 1)[1].strip()
                    metadata.dependencies = [d.strip() for d in deps.split(",") if d.strip()]
            
            self.metadata_cache[memory_path] = metadata
            return metadata
            
        except Exception:
            return None
    
    def _classify_command(self, command: str) -> str:
        """Classify command type"""
        if "measure" in command:
            return "measure"
        elif "assert" in command:
            return "assert"
        elif "demo" in command:
            return "demo"
        elif "test" in command or "pytest" in command:
            return "test"
        else:
            return "general"
    
    def _get_file_type(self, file_path: str) -> str:
        """Get file type from path"""
        if not file_path:
            return "unknown"
        
        ext = Path(file_path).suffix
        return {
            ".py": "python",
            ".md": "markdown",
            ".yml": "yaml",
            ".yaml": "yaml",
            ".json": "json",
            ".sh": "shell"
        }.get(ext, "other")
    
    def _get_session_age(self) -> int:
        """Get current session age in seconds"""
        session_file = self.memories_dir / "sessions" / "SESSION_latest.md"
        if session_file.exists():
            return int(time.time() - session_file.stat().st_mtime)
        return 0
    
    def _matches_command_pattern(self, memory_name: str, command: str) -> bool:
        """Check if memory matches command pattern"""
        # DDD-specific patterns
        patterns = {
            "measure": ["extractor", "artifact", "coverage", "algorithm"],
            "assert": ["threshold", "validation", "coverage"],
            "demo": ["mvp", "config", "risk", "example"]
        }
        
        cmd_type = self._classify_command(command)
        if cmd_type in patterns:
            return any(p in memory_name.lower() for p in patterns[cmd_type])
        return False
    
    def cleanup_old_memories(self) -> Dict[str, int]:
        """Clean up old session memories and archives"""
        cleanup_stats = {
            "deleted": 0,
            "archived": 0,
            "compressed": 0
        }
        
        # Clean old sessions
        sessions_dir = self.memories_dir / "sessions"
        if sessions_dir.exists():
            cutoff = datetime.now() - timedelta(days=7)
            for session_file in sessions_dir.glob("*.md"):
                if datetime.fromtimestamp(session_file.stat().st_mtime) < cutoff:
                    session_file.unlink()
                    cleanup_stats["deleted"] += 1
        
        # Archive stale memories
        for category in ["coverage", "extraction", "implementation"]:
            cat_dir = self.memories_dir / category
            if cat_dir.exists():
                for memory_file in cat_dir.glob("*.md"):
                    metadata = self._parse_memory_metadata(memory_file)
                    if metadata and metadata.freshness == "⚠️ stale":
                        archive_dir = self.memories_dir / "archive"
                        archive_dir.mkdir(exist_ok=True)
                        memory_file.rename(archive_dir / memory_file.name)
                        cleanup_stats["archived"] += 1
        
        return cleanup_stats
    
    def get_performance_metrics(self) -> Dict:
        """Get performance metrics"""
        if self.metrics["load_times"]:
            avg_load_time = sum(self.metrics["load_times"]) / len(self.metrics["load_times"])
        else:
            avg_load_time = 0
        
        total_requests = self.metrics["cache_hits"] + self.metrics["cache_misses"]
        cache_hit_rate = self.metrics["cache_hits"] / total_requests if total_requests > 0 else 0
        
        avg_relevance = (sum(self.metrics["relevance_scores"]) / len(self.metrics["relevance_scores"])
                        if self.metrics["relevance_scores"] else 0)
        
        return {
            "average_load_time_ms": avg_load_time * 1000,
            "cache_hit_rate": cache_hit_rate,
            "average_relevance_score": avg_relevance,
            "total_tokens_loaded": self.metrics["total_tokens_loaded"],
            "memories_in_cache": len(self.memory_cache)
        }


# Hook integration functions
def on_command_execution(command: str, project_root: Path = Path.cwd()):
    """Hook for command execution - intelligent memory loading"""
    manager = AdvancedMemoryManager(project_root)
    
    # Select memories
    memories = manager.select_memories_for_context(command)
    
    # Log selection
    log_file = project_root / ".serena" / "logs" / "memory_loading.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(log_file, "a") as f:
        f.write(f"{datetime.now().isoformat()} - Command: {command}\n")
        f.write(f"  Loaded: {', '.join(memories)}\n")
        f.write(f"  Metrics: {manager.get_performance_metrics()}\n\n")
    
    return memories


def on_session_end(project_root: Path = Path.cwd()):
    """Hook for session end - cleanup and metrics"""
    manager = AdvancedMemoryManager(project_root)
    
    # Cleanup
    cleanup_stats = manager.cleanup_old_memories()
    
    # Save metrics
    metrics_file = project_root / ".serena" / "metrics" / "performance.json"
    metrics_file.parent.mkdir(parents=True, exist_ok=True)
    
    metrics = manager.get_performance_metrics()
    metrics["cleanup"] = cleanup_stats
    metrics["timestamp"] = datetime.now().isoformat()
    
    with open(metrics_file, "w") as f:
        json.dump(metrics, f, indent=2)
    
    return metrics


if __name__ == "__main__":
    # Test the advanced memory manager
    manager = AdvancedMemoryManager(Path.cwd())
    
    # Test different commands
    test_commands = [
        "ddd measure src/",
        "ddd assert-coverage .",
        "ddd demo demo-project/",
        "pytest tests/"
    ]
    
    print("🧪 Testing Advanced Memory Management")
    print("=" * 50)
    
    for cmd in test_commands:
        print(f"\nCommand: {cmd}")
        memories = manager.select_memories_for_context(cmd)
        print(f"Selected {len(memories)} memories:")
        for mem in memories[:5]:
            print(f"  • {mem}")
    
    print("\n📊 Performance Metrics:")
    metrics = manager.get_performance_metrics()
    for key, value in metrics.items():
        print(f"  {key}: {value}")