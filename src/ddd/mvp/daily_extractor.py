"""
MVP Daily Maintenance Extractor - Stripped down for pure velocity.

This is the 2-week sprint version. Just daily tasks. Just Ansible. Just ship it.
"""

import re
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


class DailyMaintenanceExtractor:
    """
    Ultra-simple daily task extractor - MVP version.
    
    Philosophy: If it runs daily, we extract it. That's it.
    """
    
    # Daily task patterns with descriptions and time estimates
    DAILY_PATTERNS = [
        # Service & Process Checks (most common daily tasks)
        (r'service[:\s]+.*status', 'Check {match} service status', 2),
        (r'systemctl.*status', 'Verify systemd service status', 2),
        (r'ps\s+(aux|ef).*grep', 'Check running processes', 1),
        (r'supervisorctl.*status', 'Check supervisor services', 2),
        
        # Log Operations (critical daily maintenance)
        (r'tail.*\.(log|err|out)', 'Review recent log entries', 3),
        (r'grep.*error.*log', 'Check logs for errors', 3),
        (r'journalctl.*--since', 'Review system journal', 2),
        (r'find.*\.(log|err).*-mtime', 'Check for old log files', 2),
        (r'logrotate|rotate.*log', 'Verify log rotation', 1),
        (r'du\s+-.*log', 'Check log disk usage', 1),
        
        # Health & Connectivity Checks
        (r'ping\s+-[cn]', 'Test network connectivity', 2),
        (r'curl.*health|healthcheck', 'Run health check endpoint', 2),
        (r'wget.*status', 'Check service availability', 2),
        (r'nc\s+-[zv].*port', 'Test port connectivity', 1),
        (r'telnet\s+\w+\s+\d+', 'Verify service port', 1),
        
        # Disk & Storage Checks
        (r'df\s+-[hH]', 'Check disk space usage', 1),
        (r'du\s+-s', 'Check directory sizes', 2),
        (r'find.*-size\s+\+', 'Find large files', 2),
        (r'ls.*\s+/tmp|\s+/var/tmp', 'Check temporary directories', 1),
        
        # Permission & Security Validations
        (r'test\s+-[rwx]', 'Validate file permissions', 2),
        (r'stat\s+(-c|--format)', 'Check file attributes', 1),
        (r'chmod\s+\d{3,4}', 'Fix file permissions', 1),
        (r'chown\s+\w+:\w+', 'Fix file ownership', 1),
        (r'find.*-perm', 'Audit file permissions', 3),
        
        # Certificate & SSL Checks
        (r'openssl.*x509.*-enddate', 'Check certificate expiry', 2),
        (r'certbot.*certificates', 'Review SSL certificates', 2),
        (r'ssl.*expire|expiry', 'Validate SSL expiration', 2),
        
        # Database Health (daily for production)
        (r'mysql.*processlist', 'Check database connections', 2),
        (r'psql.*\\\\l|pg_stat', 'Check PostgreSQL status', 2),
        (r'mongo.*serverStatus', 'Check MongoDB health', 2),
        (r'redis-cli.*ping', 'Test Redis connectivity', 1),
        
        # Backup Verification
        (r'ls.*backup|find.*backup.*-mtime\s+-1', 'Verify recent backups', 3),
        (r'test.*backup.*exist', 'Check backup existence', 2),
        (r'tar\s+-t.*backup', 'Validate backup integrity', 3),
        
        # Queue & Job Monitoring
        (r'rabbitmqctl.*list', 'Check message queues', 2),
        (r'celery.*inspect', 'Monitor Celery workers', 2),
        (r'crontab\s+-l', 'Verify cron jobs', 1),
        (r'at\s+-l|atq', 'Check scheduled jobs', 1),
        
        # Container & Orchestration (if using Docker/K8s)
        (r'docker\s+ps', 'Check running containers', 2),
        (r'docker.*logs.*--since', 'Review container logs', 3),
        (r'kubectl.*get\s+pods', 'Check Kubernetes pods', 2),
        (r'docker.*stats', 'Monitor container resources', 2),
    ]
    
    def extract(self, file_path: Path) -> Dict[str, Any]:
        """
        Extract daily maintenance tasks from an Ansible file.
        
        This is the MVP version - we just pattern match and return tasks.
        No fancy AST parsing, no complex logic. Just ship it.
        """
        try:
            content = file_path.read_text()
        except Exception as e:
            return {'error': f"Could not read file: {e}", 'tasks': []}
        
        # Extract module name for context
        module_name = file_path.stem
        
        # Find all daily patterns
        tasks = []
        seen_tasks = set()  # Dedup similar tasks
        
        for pattern, description_template, time_minutes in self.DAILY_PATTERNS:
            matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
            
            for match in matches:
                # Create specific description from template
                match_text = match.group(0)[:50]  # First 50 chars for context
                description = description_template.replace('{match}', match_text)
                
                # Simple dedup based on description start
                task_key = description[:30]
                if task_key not in seen_tasks:
                    seen_tasks.add(task_key)
                    tasks.append({
                        'description': description,
                        'time_minutes': time_minutes,
                        'line_number': content[:match.start()].count('\n') + 1,
                        'pattern_matched': pattern,
                        'automation_potential': self._assess_automation(match_text)
                    })
        
        # Sort by line number (order in file)
        tasks.sort(key=lambda x: x['line_number'])
        
        # Calculate totals
        total_time = sum(t['time_minutes'] for t in tasks)
        automatable = sum(1 for t in tasks if t['automation_potential'])
        
        return {
            'module': module_name,
            'file': str(file_path),
            'tasks': tasks,
            'summary': {
                'total_tasks': len(tasks),
                'total_time_minutes': total_time,
                'time_saved_annually_hours': self._calculate_annual_savings(total_time),
                'automatable_tasks': automatable,
                'automation_percentage': (automatable / len(tasks) * 100) if tasks else 0
            }
        }
    
    def _assess_automation(self, task_text: str) -> bool:
        """
        Quick heuristic: can this be automated?
        
        Most daily checks can be automated. Manual review tasks cannot.
        """
        manual_indicators = ['review', 'check', 'verify', 'inspect', 'audit']
        task_lower = task_text.lower()
        
        # If it's just checking status or running commands, probably automatable
        if any(word in task_lower for word in manual_indicators):
            return False
        return True
    
    def _calculate_annual_savings(self, daily_minutes: int) -> float:
        """
        Calculate annual time savings in hours.
        
        Assumes 250 working days per year (roughly 5 days/week * 50 weeks).
        """
        working_days = 250
        
        # If we can reduce time by 70% through runbook
        time_saved_daily = daily_minutes * 0.7
        annual_hours = (time_saved_daily * working_days) / 60
        
        return round(annual_hours, 1)


class RunbookGenerator:
    """
    Dead simple markdown runbook generator - MVP version.
    
    Just output a checklist. Make it useful Day 1.
    """
    
    def generate(self, extraction_result: Dict[str, Any]) -> str:
        """
        Generate a simple, immediately usable daily maintenance runbook.
        """
        if 'error' in extraction_result:
            return f"# Error\n\n{extraction_result['error']}"
        
        tasks = extraction_result['tasks']
        summary = extraction_result['summary']
        module = extraction_result.get('module', 'Unknown')
        
        # Build the runbook
        runbook = []
        
        # Header with metadata
        runbook.append("# Daily Maintenance Runbook\n")
        runbook.append(f"**Module**: {module}  ")
        runbook.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  ")
        runbook.append(f"**Estimated Time**: {summary['total_time_minutes']} minutes  ")
        runbook.append(f"**Potential Annual Savings**: {summary['time_saved_annually_hours']} hours  \n")
        
        # Morning checklist
        runbook.append("## ☀️ Morning Checklist\n")
        runbook.append("*Check each item as you complete it:*\n")
        
        # Group tasks by category for better organization
        service_tasks = [t for t in tasks if 'service' in t['description'].lower() or 'status' in t['description'].lower()]
        log_tasks = [t for t in tasks if 'log' in t['description'].lower()]
        health_tasks = [t for t in tasks if 'health' in t['description'].lower() or 'check' in t['description'].lower()]
        other_tasks = [t for t in tasks if t not in service_tasks + log_tasks + health_tasks]
        
        # Service checks first (most critical)
        if service_tasks:
            runbook.append("### 🔧 Service Status\n")
            for task in service_tasks:
                runbook.append(f"- [ ] {task['description']} *({task['time_minutes']} min)*")
            runbook.append("")
        
        # Log reviews
        if log_tasks:
            runbook.append("### 📋 Log Review\n")
            for task in log_tasks:
                runbook.append(f"- [ ] {task['description']} *({task['time_minutes']} min)*")
            runbook.append("")
        
        # Health checks
        if health_tasks:
            runbook.append("### ❤️ Health Checks\n")
            for task in health_tasks:
                runbook.append(f"- [ ] {task['description']} *({task['time_minutes']} min)*")
            runbook.append("")
        
        # Everything else
        if other_tasks:
            runbook.append("### 📌 Other Tasks\n")
            for task in other_tasks:
                runbook.append(f"- [ ] {task['description']} *({task['time_minutes']} min)*")
            runbook.append("")
        
        # Completion section
        runbook.append("## ✅ Completion\n")
        runbook.append("- [ ] All checks completed successfully")
        runbook.append("- [ ] Any issues have been escalated")
        runbook.append(f"- [ ] Actual time taken: _______ minutes (target: {summary['total_time_minutes']} min)\n")
        
        # Escalation
        runbook.append("## 🚨 Escalation\n")
        runbook.append("If any check fails or shows concerning results:")
        runbook.append("1. Document the issue in the incident log")
        runbook.append("2. Check runbook addendum for specific recovery procedures")
        runbook.append("3. Contact on-call engineer if severity > low")
        runbook.append("4. Create ticket for non-urgent issues\n")
        
        # Notes section
        runbook.append("## 📝 Notes\n")
        runbook.append("*Space for observations, issues, or improvements:*")
        runbook.append("```")
        runbook.append("")
        runbook.append("")
        runbook.append("```\n")
        
        # Automation opportunity
        if summary['automation_percentage'] > 50:
            runbook.append("## 🤖 Automation Opportunity\n")
            runbook.append(f"**{summary['automatable_tasks']} of {summary['total_tasks']} tasks** could be automated.")
            runbook.append("Consider scripting the routine checks to save additional time.\n")
        
        return '\n'.join(runbook)


# CLI Integration
def generate_daily_runbook(ansible_file: Path, output_file: Path = None, quiet: bool = False):
    """
    Main entry point for the MVP.
    
    Usage:
        python daily_extractor.py /path/to/ansible/module.yml
    """
    extractor = DailyMaintenanceExtractor()
    generator = RunbookGenerator()
    
    # Extract daily tasks
    if not quiet:
        print(f"🔍 Analyzing {ansible_file.name}...")
    extraction = extractor.extract(ansible_file)
    
    # Generate runbook
    if not quiet:
        print(f"📝 Generating runbook...")
    runbook = generator.generate(extraction)
    
    # Output
    if output_file:
        output_file.write_text(runbook)
        if not quiet:
            print(f"✅ Runbook saved to {output_file}")
    else:
        # Default output name
        output = Path(f"daily_runbook_{ansible_file.stem}.md")
        output.write_text(runbook)
        if not quiet:
            print(f"✅ Runbook saved to {output}")
    
    # Show summary
    if not quiet and 'summary' in extraction and extraction['summary']:
        summary = extraction['summary']
        print(f"\n📊 Summary:")
        print(f"   • Found {summary['total_tasks']} daily tasks")
        print(f"   • Estimated time: {summary['total_time_minutes']} minutes")
        print(f"   • Annual savings potential: {summary['time_saved_annually_hours']} hours")
        print(f"   • Automation potential: {summary['automation_percentage']:.0f}%")
    elif not quiet and 'error' in extraction:
        print(f"\n⚠️  Warning: {extraction['error']}")
    
    return extraction, runbook


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python daily_extractor.py <ansible_file>")
        sys.exit(1)
    
    ansible_file = Path(sys.argv[1])
    if not ansible_file.exists():
        print(f"Error: File {ansible_file} not found")
        sys.exit(1)
    
    generate_daily_runbook(ansible_file)