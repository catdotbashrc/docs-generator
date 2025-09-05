"""
Temporal Maintenance Extractor - Extract time-based maintenance patterns from code.

This extractor identifies daily, weekly, and monthly maintenance requirements
by analyzing temporal patterns, lifecycle keywords, and conditional triggers.
"""

import ast
import re
from typing import Dict, List, Any, Optional
from pathlib import Path
from dataclasses import dataclass
from datetime import timedelta


@dataclass
class MaintenanceProcedure:
    """Represents a maintenance procedure with temporal context."""
    name: str
    frequency: str  # daily, weekly, monthly, quarterly, annual, conditional
    description: str
    steps: List[str]
    validation: Optional[str] = None
    escalation: Optional[str] = None
    automation_potential: bool = False
    estimated_duration: Optional[timedelta] = None


class TemporalMaintenanceExtractor:
    """Extract temporal maintenance patterns from code and documentation."""
    
    # Temporal indicators mapped to maintenance frequencies
    TEMPORAL_PATTERNS = {
        'daily': [
            r'\bdaily\b', r'\bevery\s+day\b', r'\b24\s*hours?\b',
            r'\bnightly\b', r'\bdiurnal\b', r'0\s+0\s+\*\s+\*\s+\*',  # cron
        ],
        'weekly': [
            r'\bweekly\b', r'\bevery\s+week\b', r'\b7\s*days?\b',
            r'\b168\s*hours?\b', r'0\s+0\s+\*\s+\*\s+[0-6]',  # cron
        ],
        'monthly': [
            r'\bmonthly\b', r'\bevery\s+month\b', r'\b30\s*days?\b',
            r'\b4\s*weeks?\b', r'0\s+0\s+[0-9]+\s+\*\s+\*',  # cron
        ],
        'quarterly': [
            r'\bquarterly\b', r'\bevery\s+quarter\b', r'\b3\s*months?\b',
            r'\b90\s*days?\b', r'\bQ[1-4]\b',
        ],
        'annual': [
            r'\bannual(?:ly)?\b', r'\byearly\b', r'\bevery\s+year\b',
            r'\b365\s*days?\b', r'\b12\s*months?\b',
        ]
    }
    
    # Lifecycle verbs indicating maintenance actions
    LIFECYCLE_VERBS = [
        'rotate', 'expire', 'refresh', 'backup', 'archive',
        'cleanup', 'purge', 'audit', 'review', 'verify',
        'validate', 'check', 'monitor', 'update', 'patch',
        'renew', 'rollover', 'compact', 'optimize', 'reindex'
    ]
    
    # Conditional trigger patterns
    CONDITIONAL_TRIGGERS = [
        r'if\s+.*(?:exceeds?|reaches?|falls?\s+below)',
        r'when\s+.*(?:expires?|fails?|timeout)',
        r'before\s+.*(?:expires?|ends?|closes?)',
        r'after\s+.*(?:days?|hours?|minutes?)',
        r'threshold\s*[:=]\s*\d+',
        r'limit\s*[:=]\s*\d+',
        r'max(?:imum)?\s+.*\s*[:=]\s*\d+',
    ]
    
    def extract(self, file_path: Path) -> Dict[str, Any]:
        """
        Extract temporal maintenance patterns from a file.
        
        Args:
            file_path: Path to the file to analyze
            
        Returns:
            Dictionary containing maintenance procedures organized by frequency
        """
        content = file_path.read_text()
        
        # Extract based on file type
        if file_path.suffix == '.py':
            return self._extract_from_python(content, file_path)
        elif file_path.suffix in ['.yml', '.yaml']:
            return self._extract_from_yaml(content, file_path)
        elif file_path.suffix == '.sh':
            return self._extract_from_shell(content, file_path)
        else:
            return self._extract_from_text(content, file_path)
    
    def _extract_from_python(self, content: str, file_path: Path) -> Dict[str, Any]:
        """Extract maintenance patterns from Python code using AST."""
        procedures = {
            'daily': [],
            'weekly': [],
            'monthly': [],
            'quarterly': [],
            'annual': [],
            'conditional': []
        }
        
        try:
            tree = ast.parse(content)
            
            # Walk the AST looking for maintenance patterns
            for node in ast.walk(tree):
                # Check function/method names and docstrings
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    proc = self._analyze_function(node, content)
                    if proc:
                        procedures[proc.frequency].append(proc)
                
                # Check string literals for temporal patterns
                elif isinstance(node, ast.Constant) and isinstance(node.value, str):
                    freq = self._detect_frequency(node.value)
                    if freq and self._contains_lifecycle_verb(node.value):
                        proc = self._create_procedure_from_string(node.value, freq)
                        if proc:
                            procedures[freq].append(proc)
        
        except SyntaxError:
            # Fallback to text-based extraction if AST parsing fails
            return self._extract_from_text(content, file_path)
        
        return self._organize_procedures(procedures)
    
    def _analyze_function(self, node: ast.FunctionDef, content: str) -> Optional[MaintenanceProcedure]:
        """Analyze a function for maintenance patterns."""
        func_name = node.name.lower()
        
        # Check if function name contains lifecycle verbs
        if not any(verb in func_name for verb in self.LIFECYCLE_VERBS):
            return None
        
        # Get docstring
        docstring = ast.get_docstring(node) or ""
        
        # Detect frequency from docstring or function name
        freq = self._detect_frequency(func_name + " " + docstring)
        if not freq:
            # Check for conditional patterns
            if self._contains_conditional_trigger(docstring):
                freq = 'conditional'
            else:
                return None
        
        # Extract procedure details
        return MaintenanceProcedure(
            name=node.name,
            frequency=freq,
            description=self._extract_description(docstring),
            steps=self._extract_steps(docstring),
            validation=self._extract_validation(docstring),
            escalation=self._extract_escalation(node, content),
            automation_potential=self._assess_automation_potential(node)
        )
    
    def _detect_frequency(self, text: str) -> Optional[str]:
        """Detect maintenance frequency from text."""
        text_lower = text.lower()
        
        for frequency, patterns in self.TEMPORAL_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    return frequency
        
        return None
    
    def _contains_lifecycle_verb(self, text: str) -> bool:
        """Check if text contains lifecycle maintenance verbs."""
        text_lower = text.lower()
        return any(verb in text_lower for verb in self.LIFECYCLE_VERBS)
    
    def _contains_conditional_trigger(self, text: str) -> bool:
        """Check if text contains conditional trigger patterns."""
        for pattern in self.CONDITIONAL_TRIGGERS:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
    
    def _extract_description(self, docstring: str) -> str:
        """Extract procedure description from docstring."""
        lines = docstring.strip().split('\n')
        if lines:
            # First non-empty line is usually the description
            for line in lines:
                cleaned = line.strip()
                if cleaned and not cleaned.startswith(':'):
                    return cleaned
        return "Maintenance procedure"
    
    def _extract_steps(self, docstring: str) -> List[str]:
        """Extract procedure steps from docstring."""
        steps = []
        in_steps_section = False
        
        for line in docstring.split('\n'):
            line = line.strip()
            
            # Look for steps section
            if re.match(r'^(steps?|procedure|process):?\s*$', line, re.IGNORECASE):
                in_steps_section = True
                continue
            
            # Extract numbered or bulleted steps
            if in_steps_section:
                if re.match(r'^(\d+\.|-|\*)\s+', line):
                    steps.append(re.sub(r'^(\d+\.|-|\*)\s+', '', line))
                elif not line:
                    in_steps_section = False
        
        return steps if steps else ["Review and execute maintenance procedure"]
    
    def _extract_validation(self, docstring: str) -> Optional[str]:
        """Extract validation criteria from docstring."""
        patterns = [
            r'validat(?:e|ion):\s*(.+)',
            r'verif(?:y|ication):\s*(.+)',
            r'check:\s*(.+)',
            r'ensure:\s*(.+)',
            r'confirm:\s*(.+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, docstring, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    def _extract_escalation(self, node: ast.FunctionDef, content: str) -> Optional[str]:
        """Extract escalation procedure from function."""
        # Look for error handling and logging
        for child in ast.walk(node):
            if isinstance(child, ast.Raise):
                return "Raise exception to caller"
            elif isinstance(child, ast.Call):
                if hasattr(child.func, 'attr'):
                    if child.func.attr in ['error', 'critical', 'fatal', 'alert']:
                        return f"Log {child.func.attr} and notify on-call"
        
        return None
    
    def _assess_automation_potential(self, node: ast.FunctionDef) -> bool:
        """Assess if procedure can be automated."""
        # Look for indicators of automation potential
        automation_indicators = [
            'automat', 'script', 'cron', 'schedule',
            'unattended', 'batch', 'job'
        ]
        
        func_name = node.name.lower()
        docstring = ast.get_docstring(node) or ""
        
        # Check function name and docstring
        combined_text = func_name + " " + docstring.lower()
        if any(indicator in combined_text for indicator in automation_indicators):
            return True
        
        # Check for interactive elements (reduces automation potential)
        interactive_indicators = ['input', 'prompt', 'confirm', 'ask', 'manual']
        if any(indicator in combined_text for indicator in interactive_indicators):
            return False
        
        # If it's a simple function without user interaction, probably automatable
        return not self._has_user_interaction(node)
    
    def _has_user_interaction(self, node: ast.FunctionDef) -> bool:
        """Check if function has user interaction."""
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if hasattr(child.func, 'id') and child.func.id == 'input':
                    return True
                if hasattr(child.func, 'attr') and 'input' in child.func.attr.lower():
                    return True
        return False
    
    def _create_procedure_from_string(self, text: str, frequency: str) -> Optional[MaintenanceProcedure]:
        """Create a maintenance procedure from a text string."""
        # Extract the core maintenance action
        action = None
        for verb in self.LIFECYCLE_VERBS:
            if verb in text.lower():
                action = verb
                break
        
        if not action:
            return None
        
        return MaintenanceProcedure(
            name=f"{action}_{frequency}",
            frequency=frequency,
            description=text.strip()[:100],  # First 100 chars as description
            steps=[f"Execute {action} procedure as documented"],
            automation_potential=True  # Assume scriptable by default
        )
    
    def _extract_from_yaml(self, content: str, file_path: Path) -> Dict[str, Any]:
        """Extract maintenance patterns from YAML configuration."""
        procedures = {
            'daily': [],
            'weekly': [],
            'monthly': [],
            'quarterly': [],
            'annual': [],
            'conditional': []
        }
        
        # Look for cron expressions
        cron_pattern = r'cron:\s*["\']?([^"\'\n]+)["\']?'
        for match in re.finditer(cron_pattern, content):
            cron_expr = match.group(1)
            freq = self._parse_cron_frequency(cron_expr)
            if freq:
                proc = MaintenanceProcedure(
                    name=f"scheduled_task_{freq}",
                    frequency=freq,
                    description=f"Scheduled {freq} task: {cron_expr}",
                    steps=["Execute scheduled task"],
                    automation_potential=True
                )
                procedures[freq].append(proc)
        
        # Look for maintenance-related keys
        maintenance_keys = [
            'backup', 'cleanup', 'rotate', 'archive',
            'audit', 'maintenance', 'schedule'
        ]
        
        for key in maintenance_keys:
            pattern = fr'{key}:\s*\n((?:\s+.+\n?)+)'
            for match in re.finditer(pattern, content, re.MULTILINE):
                config_block = match.group(1)
                freq = self._detect_frequency(config_block) or 'daily'
                
                proc = MaintenanceProcedure(
                    name=f"{key}_maintenance",
                    frequency=freq,
                    description=f"{key.capitalize()} maintenance configuration",
                    steps=self._extract_yaml_steps(config_block),
                    automation_potential=True
                )
                procedures[freq].append(proc)
        
        return self._organize_procedures(procedures)
    
    def _parse_cron_frequency(self, cron_expr: str) -> Optional[str]:
        """Parse cron expression to determine frequency."""
        parts = cron_expr.strip().split()
        if len(parts) < 5:
            return None
        
        minute, hour, day, month, weekday = parts[:5]
        
        # Daily: runs at specific time every day
        if day == '*' and month == '*' and weekday == '*':
            return 'daily'
        
        # Weekly: runs on specific weekday
        if day == '*' and month == '*' and weekday != '*':
            return 'weekly'
        
        # Monthly: runs on specific day of month
        if day != '*' and month == '*':
            return 'monthly'
        
        # Annual: runs on specific month
        if month != '*':
            return 'annual'
        
        return 'daily'  # Default to daily if pattern unclear
    
    def _extract_yaml_steps(self, config_block: str) -> List[str]:
        """Extract steps from YAML configuration block."""
        steps = []
        for line in config_block.split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                # Remove YAML syntax
                line = re.sub(r'^-\s*', '', line)
                line = re.sub(r':\s*$', '', line)
                if line:
                    steps.append(line)
        
        return steps if steps else ["Execute maintenance task"]
    
    def _extract_from_shell(self, content: str, file_path: Path) -> Dict[str, Any]:
        """Extract maintenance patterns from shell scripts."""
        procedures = {
            'daily': [],
            'weekly': [], 
            'monthly': [],
            'quarterly': [],
            'annual': [],
            'conditional': []
        }
        
        # Look for maintenance-related functions
        func_pattern = r'function\s+(\w+)|(\w+)\s*\(\)\s*\{'
        for match in re.finditer(func_pattern, content):
            func_name = match.group(1) or match.group(2)
            if any(verb in func_name.lower() for verb in self.LIFECYCLE_VERBS):
                # Extract function body
                start_pos = match.end()
                # Simple extraction - find matching closing brace
                brace_count = 1
                end_pos = start_pos
                
                for i in range(start_pos, len(content)):
                    if content[i] == '{':
                        brace_count += 1
                    elif content[i] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            end_pos = i
                            break
                
                func_body = content[start_pos:end_pos] if end_pos > start_pos else ""
                freq = self._detect_frequency(func_name + " " + func_body) or 'daily'
                
                proc = MaintenanceProcedure(
                    name=func_name,
                    frequency=freq,
                    description=f"Shell maintenance function: {func_name}",
                    steps=self._extract_shell_steps(func_body),
                    automation_potential=True
                )
                procedures[freq].append(proc)
        
        # Look for cron job comments
        cron_comment_pattern = r'#\s*cron:\s*(.+)'
        for match in re.finditer(cron_comment_pattern, content):
            cron_desc = match.group(1)
            freq = self._detect_frequency(cron_desc) or 'daily'
            
            proc = MaintenanceProcedure(
                name="cron_job",
                frequency=freq,
                description=cron_desc,
                steps=["Execute cron job as scheduled"],
                automation_potential=True
            )
            procedures[freq].append(proc)
        
        return self._organize_procedures(procedures)
    
    def _extract_shell_steps(self, func_body: str) -> List[str]:
        """Extract steps from shell function body."""
        steps = []
        
        # Look for echo/printf statements that describe steps
        echo_pattern = r'(?:echo|printf)\s+["\']([^"\']+)["\']'
        for match in re.finditer(echo_pattern, func_body):
            step_desc = match.group(1)
            if not step_desc.startswith('$'):  # Avoid variable echoes
                steps.append(step_desc)
        
        # Look for comments describing steps
        comment_pattern = r'#\s*([A-Z].+)'  # Comments starting with capital letter
        for match in re.finditer(comment_pattern, func_body):
            steps.append(match.group(1))
        
        return steps if steps else ["Execute shell maintenance procedure"]
    
    def _extract_from_text(self, content: str, file_path: Path) -> Dict[str, Any]:
        """Fallback text-based extraction for any file type."""
        procedures = {
            'daily': [],
            'weekly': [],
            'monthly': [],
            'quarterly': [],
            'annual': [],
            'conditional': []
        }
        
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            # Check each line for temporal patterns and lifecycle verbs
            freq = self._detect_frequency(line)
            if freq and self._contains_lifecycle_verb(line):
                # Look for surrounding context
                context_start = max(0, i - 2)
                context_end = min(len(lines), i + 3)
                context = '\n'.join(lines[context_start:context_end])
                
                proc = MaintenanceProcedure(
                    name=f"maintenance_proc_line_{i}",
                    frequency=freq,
                    description=line.strip()[:100],
                    steps=self._extract_text_steps(context),
                    automation_potential=self._assess_text_automation(context)
                )
                procedures[freq].append(proc)
            
            # Check for conditional patterns
            elif self._contains_conditional_trigger(line):
                proc = MaintenanceProcedure(
                    name=f"conditional_proc_line_{i}",
                    frequency='conditional',
                    description=line.strip()[:100],
                    steps=["Monitor condition and execute when triggered"],
                    automation_potential=True
                )
                procedures['conditional'].append(proc)
        
        return self._organize_procedures(procedures)
    
    def _extract_text_steps(self, context: str) -> List[str]:
        """Extract steps from text context."""
        steps = []
        
        # Look for numbered lists
        numbered_pattern = r'^\s*\d+[.)]\s+(.+)'
        for line in context.split('\n'):
            match = re.match(numbered_pattern, line)
            if match:
                steps.append(match.group(1))
        
        # Look for bullet points
        if not steps:
            bullet_pattern = r'^\s*[-*•]\s+(.+)'
            for line in context.split('\n'):
                match = re.match(bullet_pattern, line)
                if match:
                    steps.append(match.group(1))
        
        return steps if steps else ["Follow documented procedure"]
    
    def _assess_text_automation(self, context: str) -> bool:
        """Assess automation potential from text context."""
        # Simple heuristic: if it mentions scripts or automation, likely automatable
        automation_keywords = [
            'automat', 'script', 'cron', 'schedule',
            'programmatic', 'api', 'cli'
        ]
        
        context_lower = context.lower()
        return any(keyword in context_lower for keyword in automation_keywords)
    
    def _organize_procedures(self, procedures: Dict[str, List]) -> Dict[str, Any]:
        """Organize procedures into final structure with metadata."""
        total_procedures = sum(len(procs) for procs in procedures.values())
        automatable = sum(
            1 for procs in procedures.values() 
            for proc in procs if proc.automation_potential
        )
        
        return {
            'temporal_maintenance': {
                'procedures': procedures,
                'statistics': {
                    'total_procedures': total_procedures,
                    'by_frequency': {
                        freq: len(procs) for freq, procs in procedures.items()
                    },
                    'automation_potential': {
                        'count': automatable,
                        'percentage': (automatable / total_procedures * 100) if total_procedures > 0 else 0
                    }
                },
                'coverage': self._calculate_maintenance_coverage(procedures)
            }
        }
    
    def _calculate_maintenance_coverage(self, procedures: Dict[str, List]) -> Dict[str, float]:
        """Calculate maintenance coverage scores."""
        # Define expected maintenance tasks per frequency
        expected = {
            'daily': 5,  # health checks, log rotation, backups, monitoring, cleanup
            'weekly': 3,  # updates, deep backups, performance review
            'monthly': 2,  # audits, compliance checks
            'quarterly': 1,  # major reviews
            'annual': 1,  # disaster recovery, major updates
        }
        
        coverage = {}
        for freq, expected_count in expected.items():
            actual_count = len(procedures.get(freq, []))
            coverage[freq] = min(100, (actual_count / expected_count * 100)) if expected_count > 0 else 0
        
        # Overall coverage is weighted average
        weights = {'daily': 0.4, 'weekly': 0.3, 'monthly': 0.2, 'quarterly': 0.05, 'annual': 0.05}
        overall = sum(coverage[freq] * weights.get(freq, 0) for freq in coverage)
        coverage['overall'] = overall
        
        return coverage


# Integration with existing extractors
class MaintenanceAwareAnsibleExtractor:
    """Ansible extractor enhanced with temporal maintenance extraction."""
    
    def __init__(self, base_extractor, temporal_extractor: TemporalMaintenanceExtractor):
        self.base_extractor = base_extractor
        self.temporal_extractor = temporal_extractor
    
    def extract(self, file_path: Path) -> Dict[str, Any]:
        """Extract both traditional and temporal maintenance documentation."""
        # Get base extraction
        base_result = self.base_extractor.extract(file_path)
        
        # Add temporal maintenance extraction
        temporal_result = self.temporal_extractor.extract(file_path)
        
        # Merge results
        base_result.update(temporal_result)
        
        # Calculate combined maintenance readiness score
        base_result['maintenance_readiness'] = self._calculate_readiness(base_result)
        
        return base_result
    
    def _calculate_readiness(self, result: Dict[str, Any]) -> Dict[str, float]:
        """Calculate maintenance readiness score."""
        scores = {
            'documentation': result.get('documentation_coverage', 0),
            'temporal': result.get('temporal_maintenance', {}).get('coverage', {}).get('overall', 0),
            'error_recovery': len(result.get('error_patterns', [])) * 10,  # 10% per documented error
            'automation': result.get('temporal_maintenance', {}).get('statistics', {}).get('automation_potential', {}).get('percentage', 0)
        }
        
        # Weighted average
        weights = {
            'documentation': 0.2,
            'temporal': 0.4,
            'error_recovery': 0.2,
            'automation': 0.2
        }
        
        overall = sum(scores[key] * weights[key] for key in scores)
        scores['overall'] = overall
        
        return scores