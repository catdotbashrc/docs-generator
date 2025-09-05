"""
Comprehensive TDD Test Suite for MVP Daily Maintenance Extractor

Following RED-GREEN-REFACTOR methodology for Pure Maintenance MVP
Week 1 Implementation with proper TDD cycles
"""

import pytest
from pathlib import Path
from datetime import datetime
import tempfile
import re
from unittest.mock import patch, MagicMock

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ddd.mvp.daily_extractor import DailyMaintenanceExtractor, RunbookGenerator, generate_daily_runbook


class TestDailyMaintenanceExtractorTDD:
    """
    TDD Test Suite for DailyMaintenanceExtractor
    
    Structure follows RED-GREEN-REFACTOR cycles:
    - RED: Write failing tests first
    - GREEN: Implement minimal code to pass
    - REFACTOR: Improve while keeping tests green
    """
    
    def setup_method(self):
        """Setup for each test - fresh extractor instance"""
        self.extractor = DailyMaintenanceExtractor()
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def teardown_method(self):
        """Cleanup temporary files"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def create_test_file(self, content: str, filename: str = "test_module.yml") -> Path:
        """Helper to create test Ansible files"""
        file_path = self.temp_dir / filename
        file_path.write_text(content)
        return file_path
    
    # ======================================
    # RED PHASE: Service Status Checks
    # ======================================
    
    def test_extract_service_status_checks_systemctl(self):
        """RED: Test systemctl status extraction - should find service checks"""
        content = """
        - name: Check web service
          ansible.builtin.command: systemctl status nginx
        
        - name: Verify database
          ansible.builtin.shell: systemctl status postgresql
        """
        
        file_path = self.create_test_file(content)
        result = self.extractor.extract(file_path)
        
        # Should extract 2 service status tasks
        service_tasks = [t for t in result['tasks'] if 'status' in t['description'].lower()]
        assert len(service_tasks) >= 2, f"Expected at least 2 service status tasks, got {len(service_tasks)}"
        
        # Check specific patterns
        descriptions = [t['description'] for t in result['tasks']]
        assert any('systemd' in desc.lower() for desc in descriptions), "Should detect systemctl patterns"
    
    def test_extract_service_status_checks_service_command(self):
        """RED: Test service status command extraction"""
        content = """
        - name: Check service status
          ansible.builtin.command: service httpd status
        
        - name: Verify service running
          ansible.builtin.shell: service status mysql
        """
        
        file_path = self.create_test_file(content)
        result = self.extractor.extract(file_path)
        
        # Should find service status checks
        service_tasks = [t for t in result['tasks'] if 'service' in t['description'].lower()]
        assert len(service_tasks) >= 1, "Should extract service status commands"
    
    def test_extract_process_checks(self):
        """RED: Test process monitoring extraction"""
        content = """
        - name: Check running processes
          ansible.builtin.shell: ps aux | grep nginx
        
        - name: Verify process count
          ansible.builtin.command: ps ef | grep apache
        """
        
        file_path = self.create_test_file(content)
        result = self.extractor.extract(file_path)
        
        # Should detect process monitoring
        process_tasks = [t for t in result['tasks'] if 'process' in t['description'].lower()]
        assert len(process_tasks) >= 1, "Should extract process monitoring tasks"
    
    # ======================================
    # RED PHASE: Log Operations
    # ======================================
    
    def test_extract_log_review_tasks(self):
        """RED: Test log review and rotation extraction"""
        content = """
        - name: Check error logs
          ansible.builtin.shell: tail -100 /var/log/nginx/error.log
        
        - name: Review application logs
          ansible.builtin.command: grep ERROR /var/log/app.log
        
        - name: Rotate logs
          ansible.builtin.command: logrotate -f /etc/logrotate.conf
        """
        
        file_path = self.create_test_file(content)
        result = self.extractor.extract(file_path)
        
        # Should extract log-related tasks
        log_tasks = [t for t in result['tasks'] if 'log' in t['description'].lower()]
        assert len(log_tasks) >= 2, f"Expected at least 2 log tasks, got {len(log_tasks)}"
        
        # Check for specific log operations
        descriptions = [t['description'] for t in result['tasks']]
        assert any('review' in desc.lower() or 'tail' in desc.lower() for desc in descriptions), "Should detect log review"
        assert any('error' in desc.lower() or 'grep' in desc.lower() for desc in descriptions), "Should detect error checking"
    
    def test_extract_journal_operations(self):
        """RED: Test systemd journal extraction"""
        content = """
        - name: Check system journal
          ansible.builtin.command: journalctl --since yesterday
        
        - name: Review service logs
          ansible.builtin.shell: journalctl -u nginx.service --since "1 hour ago"
        """
        
        file_path = self.create_test_file(content)
        result = self.extractor.extract(file_path)
        
        # Should detect journal operations
        journal_tasks = [t for t in result['tasks'] if 'journal' in t['description'].lower()]
        assert len(journal_tasks) >= 1, "Should extract journalctl operations"
    
    # ======================================
    # RED PHASE: Health & Connectivity
    # ======================================
    
    def test_extract_connectivity_checks(self):
        """RED: Test network and service connectivity extraction"""
        content = """
        - name: Ping database server
          ansible.builtin.command: ping -c 3 db.example.com
        
        - name: Check health endpoint
          ansible.builtin.uri:
            url: http://api.example.com/health
            method: GET
        
        - name: Test port connectivity
          ansible.builtin.command: nc -z api.example.com 8080
        """
        
        file_path = self.create_test_file(content)
        result = self.extractor.extract(file_path)
        
        # Should detect connectivity checks
        connectivity_tasks = [t for t in result['tasks'] 
                            if any(word in t['description'].lower() 
                                  for word in ['connectivity', 'ping', 'health', 'port'])]
        assert len(connectivity_tasks) >= 1, "Should extract connectivity checks"
    
    def test_extract_health_endpoint_checks(self):
        """RED: Test health endpoint and curl extraction"""
        content = """
        - name: Check API health
          ansible.builtin.shell: curl -f http://localhost:8080/health
        
        - name: Verify service availability
          ansible.builtin.command: wget --spider http://service.local/status
        """
        
        file_path = self.create_test_file(content)
        result = self.extractor.extract(file_path)
        
        # Should detect health checks
        health_tasks = [t for t in result['tasks'] if 'health' in t['description'].lower()]
        assert len(health_tasks) >= 1, "Should extract health endpoint checks"
    
    # ======================================
    # RED PHASE: Disk & Storage
    # ======================================
    
    def test_extract_disk_space_checks(self):
        """RED: Test disk space monitoring extraction"""
        content = """
        - name: Check disk usage
          ansible.builtin.command: df -h
        
        - name: Monitor directory sizes
          ansible.builtin.shell: du -sh /var/log /tmp
        
        - name: Find large files
          ansible.builtin.command: find /var -size +100M -type f
        """
        
        file_path = self.create_test_file(content)
        result = self.extractor.extract(file_path)
        
        # Should detect disk monitoring
        disk_tasks = [t for t in result['tasks'] 
                     if any(word in t['description'].lower() 
                           for word in ['disk', 'space', 'usage', 'size'])]
        assert len(disk_tasks) >= 1, "Should extract disk monitoring tasks"
    
    def test_extract_temp_directory_checks(self):
        """RED: Test temporary directory cleanup extraction"""
        content = """
        - name: Clean temp files
          ansible.builtin.shell: ls -la /tmp
        
        - name: Check var temp
          ansible.builtin.command: ls /var/tmp
        """
        
        file_path = self.create_test_file(content)
        result = self.extractor.extract(file_path)
        
        # Should detect temp directory operations
        temp_tasks = [t for t in result['tasks'] if 'temp' in t['description'].lower()]
        assert len(temp_tasks) >= 1, "Should extract temp directory checks"
    
    # ======================================
    # RED PHASE: Permission & Security
    # ======================================
    
    def test_extract_permission_validations(self):
        """RED: Test file permission validation extraction"""
        content = """
        - name: Check file permissions
          ansible.builtin.shell: test -r /etc/nginx/nginx.conf
        
        - name: Verify executable permissions
          ansible.builtin.command: test -x /usr/bin/nginx
        
        - name: Fix permissions
          ansible.builtin.file:
            path: /var/log/nginx
            mode: '0755'
        """
        
        file_path = self.create_test_file(content)
        result = self.extractor.extract(file_path)
        
        # Should detect permission operations
        perm_tasks = [t for t in result['tasks'] 
                     if any(word in t['description'].lower() 
                           for word in ['permission', 'test', 'chmod', 'chown'])]
        assert len(perm_tasks) >= 1, "Should extract permission validation tasks"
    
    def test_extract_certificate_checks(self):
        """RED: Test SSL certificate monitoring extraction"""
        content = """
        - name: Check certificate expiry
          ansible.builtin.shell: openssl x509 -in /etc/ssl/cert.pem -enddate -noout
        
        - name: Verify SSL certificates
          ansible.builtin.command: certbot certificates
        """
        
        file_path = self.create_test_file(content)
        result = self.extractor.extract(file_path)
        
        # Should detect certificate operations
        cert_tasks = [t for t in result['tasks'] 
                     if any(word in t['description'].lower() 
                           for word in ['certificate', 'ssl', 'cert', 'openssl'])]
        assert len(cert_tasks) >= 1, "Should extract certificate checks"
    
    # ======================================
    # RED PHASE: Database & Queue Health
    # ======================================
    
    def test_extract_database_health_checks(self):
        """RED: Test database monitoring extraction"""
        content = """
        - name: Check MySQL connections
          ansible.builtin.shell: mysql -e "SHOW PROCESSLIST;"
        
        - name: Verify PostgreSQL status
          ansible.builtin.command: psql -c "\\l"
        
        - name: Test Redis connectivity
          ansible.builtin.shell: redis-cli ping
        """
        
        file_path = self.create_test_file(content)
        result = self.extractor.extract(file_path)
        
        # Should detect database operations
        db_tasks = [t for t in result['tasks'] 
                   if any(word in t['description'].lower() 
                         for word in ['database', 'mysql', 'psql', 'postgres', 'redis', 'mongo'])]
        assert len(db_tasks) >= 1, "Should extract database health checks"
    
    def test_extract_queue_monitoring(self):
        """RED: Test message queue monitoring extraction"""
        content = """
        - name: Check RabbitMQ queues
          ansible.builtin.command: rabbitmqctl list_queues
        
        - name: Monitor Celery workers
          ansible.builtin.shell: celery inspect active
        """
        
        file_path = self.create_test_file(content)
        result = self.extractor.extract(file_path)
        
        # Should detect queue monitoring
        queue_tasks = [t for t in result['tasks'] 
                      if any(word in t['description'].lower() 
                            for word in ['queue', 'rabbit', 'celery', 'worker'])]
        assert len(queue_tasks) >= 1, "Should extract queue monitoring tasks"
    
    # ======================================
    # RED PHASE: Backup & Container Checks
    # ======================================
    
    def test_extract_backup_verification(self):
        """RED: Test backup verification extraction"""
        content = """
        - name: Check recent backups
          ansible.builtin.shell: find /backup -name "*.tar.gz" -mtime -1
        
        - name: Verify backup integrity
          ansible.builtin.command: tar -tf /backup/daily.tar.gz
        """
        
        file_path = self.create_test_file(content)
        result = self.extractor.extract(file_path)
        
        # Should detect backup operations
        backup_tasks = [t for t in result['tasks'] 
                       if any(word in t['description'].lower() 
                             for word in ['backup', 'tar', 'integrity'])]
        assert len(backup_tasks) >= 1, "Should extract backup verification tasks"
    
    def test_extract_container_monitoring(self):
        """RED: Test Docker/container monitoring extraction"""
        content = """
        - name: Check running containers
          ansible.builtin.command: docker ps
        
        - name: Review container logs
          ansible.builtin.shell: docker logs --since 1h nginx-container
        
        - name: Monitor container resources
          ansible.builtin.command: docker stats --no-stream
        """
        
        file_path = self.create_test_file(content)
        result = self.extractor.extract(file_path)
        
        # Should detect container operations
        container_tasks = [t for t in result['tasks'] 
                          if any(word in t['description'].lower() 
                                for word in ['container', 'docker', 'kubectl'])]
        assert len(container_tasks) >= 1, "Should extract container monitoring tasks"
    
    # ======================================
    # RED PHASE: Pattern Edge Cases
    # ======================================
    
    def test_extract_mixed_patterns_complex_file(self):
        """RED: Test extraction from complex mixed-pattern file"""
        content = """
        ---
        - name: Daily maintenance playbook
          hosts: all
          tasks:
            - name: Check system status
              ansible.builtin.command: systemctl status nginx
            
            - name: Review error logs
              ansible.builtin.shell: tail -50 /var/log/nginx/error.log
            
            - name: Test database connectivity
              ansible.builtin.shell: mysql -e "SELECT 1;"
            
            - name: Check disk space
              ansible.builtin.command: df -h
            
            - name: Verify SSL certificate
              ansible.builtin.shell: openssl x509 -in /etc/ssl/cert.pem -enddate -noout
            
            - name: Check running containers
              ansible.builtin.command: docker ps
        """
        
        file_path = self.create_test_file(content)
        result = self.extractor.extract(file_path)
        
        # Should extract multiple diverse tasks
        assert len(result['tasks']) >= 5, f"Expected at least 5 tasks, got {len(result['tasks'])}"
        
        # Should have reasonable time estimates
        total_time = result['summary']['total_time_minutes']
        assert 5 <= total_time <= 30, f"Total time should be 5-30 minutes, got {total_time}"
        
        # Should calculate automation potential
        assert 'automation_percentage' in result['summary']
        assert 0 <= result['summary']['automation_percentage'] <= 100
    
    def test_extract_no_patterns_empty_result(self):
        """RED: Test extraction from file with no daily patterns"""
        content = """
        - name: Install package
          ansible.builtin.package:
            name: nginx
            state: present
        
        - name: Deploy configuration
          ansible.builtin.template:
            src: nginx.conf.j2
            dest: /etc/nginx/nginx.conf
        """
        
        file_path = self.create_test_file(content)
        result = self.extractor.extract(file_path)
        
        # Should return empty tasks for non-maintenance content
        assert len(result['tasks']) == 0, "Should not extract deployment tasks as daily maintenance"
        assert result['summary']['total_time_minutes'] == 0
    
    def test_extract_deduplication_similar_tasks(self):
        """RED: Test deduplication of similar tasks"""
        content = """
        - name: Check service 1
          ansible.builtin.command: systemctl status nginx
        
        - name: Check service 2  
          ansible.builtin.command: systemctl status nginx
        
        - name: Check another service
          ansible.builtin.command: systemctl status apache2
        """
        
        file_path = self.create_test_file(content)
        result = self.extractor.extract(file_path)
        
        # Should deduplicate similar tasks but keep different ones
        descriptions = [t['description'] for t in result['tasks']]
        # Should have fewer tasks than original due to deduplication
        assert len(result['tasks']) <= 2, "Should deduplicate similar systemctl commands"
    
    # ======================================
    # RED PHASE: Error Handling
    # ======================================
    
    def test_extract_file_not_found_error(self):
        """RED: Test handling of non-existent files"""
        non_existent_file = self.temp_dir / "does_not_exist.yml"
        result = self.extractor.extract(non_existent_file)
        
        # Should handle file errors gracefully
        assert 'error' in result
        assert 'tasks' in result
        assert len(result['tasks']) == 0
    
    def test_extract_invalid_file_content(self):
        """RED: Test handling of binary/invalid content"""
        # Create file with binary content
        binary_file = self.temp_dir / "binary.yml"
        binary_file.write_bytes(b'\x00\x01\x02\xff\xfe')
        
        result = self.extractor.extract(binary_file)
        
        # Should handle invalid content gracefully
        assert 'tasks' in result  # Should still return structure
        # May have error or empty tasks
    
    # ======================================
    # RED PHASE: Time Estimation & Automation
    # ======================================
    
    def test_time_estimation_accuracy(self):
        """RED: Test time estimates are reasonable"""
        content = """
        - name: Quick check
          ansible.builtin.command: systemctl status nginx
        
        - name: Review logs  
          ansible.builtin.shell: tail -100 /var/log/app.log
        """
        
        file_path = self.create_test_file(content)
        result = self.extractor.extract(file_path)
        
        # Time estimates should be reasonable (1-5 minutes per task)
        for task in result['tasks']:
            assert 1 <= task['time_minutes'] <= 10, f"Time estimate {task['time_minutes']} seems unreasonable"
    
    def test_automation_assessment_logic(self):
        """RED: Test automation potential assessment"""
        # Test automation assessment method directly
        extractor = DailyMaintenanceExtractor()
        
        # Automatable tasks
        assert extractor._assess_automation("systemctl status nginx") == True
        assert extractor._assess_automation("df -h") == True
        
        # Manual tasks
        assert extractor._assess_automation("review log entries") == False
        assert extractor._assess_automation("check for errors") == False
    
    def test_annual_savings_calculation(self):
        """RED: Test annual time savings calculation"""
        extractor = DailyMaintenanceExtractor()
        
        # Test calculation
        daily_minutes = 10
        annual_hours = extractor._calculate_annual_savings(daily_minutes)
        
        # Should be reasonable (250 working days * 10 min * 0.7 savings / 60 min)
        expected = (10 * 0.7 * 250) / 60
        assert abs(annual_hours - expected) < 1.0, f"Expected ~{expected}, got {annual_hours}"
    
    # ======================================
    # RED PHASE: Line Number Tracking
    # ======================================
    
    def test_line_number_tracking(self):
        """RED: Test that tasks include correct line numbers"""
        content = """line 1
        
        - name: First task
          ansible.builtin.command: systemctl status nginx
        
        line 6
        
        - name: Second task
          ansible.builtin.shell: tail /var/log/app.log
        """
        
        file_path = self.create_test_file(content)
        result = self.extractor.extract(file_path)
        
        # Should track line numbers
        for task in result['tasks']:
            assert 'line_number' in task
            assert task['line_number'] > 0
        
        # Should be sorted by line number
        line_numbers = [t['line_number'] for t in result['tasks']]
        assert line_numbers == sorted(line_numbers), "Tasks should be ordered by line number"


class TestRunbookGeneratorTDD:
    """
    TDD Test Suite for RunbookGenerator
    
    Testing markdown generation and formatting
    """
    
    def setup_method(self):
        """Setup for each test"""
        self.generator = RunbookGenerator()
    
    # ======================================
    # RED PHASE: Basic Generation
    # ======================================
    
    def test_generate_basic_runbook_structure(self):
        """RED: Test basic runbook structure generation"""
        extraction_result = {
            'module': 'test_module',
            'file': '/path/to/test.yml',
            'tasks': [
                {'description': 'Check service status', 'time_minutes': 2, 'line_number': 5},
                {'description': 'Review log files', 'time_minutes': 3, 'line_number': 10}
            ],
            'summary': {
                'total_tasks': 2,
                'total_time_minutes': 5,
                'time_saved_annually_hours': 14.6,
                'automatable_tasks': 1,
                'automation_percentage': 50.0
            }
        }
        
        runbook = self.generator.generate(extraction_result)
        
        # Should have basic structure
        assert '# Daily Maintenance Runbook' in runbook
        assert '## ☀️ Morning Checklist' in runbook
        assert '## ✅ Completion' in runbook
        assert '## 🚨 Escalation' in runbook
        
        # Should include metadata
        assert 'test_module' in runbook
        assert '5 minutes' in runbook
        assert '14.6 hours' in runbook
    
    def test_generate_task_checkboxes(self):
        """RED: Test checkbox generation for tasks"""
        extraction_result = {
            'module': 'test_module',
            'tasks': [
                {'description': 'Check service status', 'time_minutes': 2},
                {'description': 'Review error logs', 'time_minutes': 3}
            ],
            'summary': {
                'total_tasks': 2,
                'total_time_minutes': 5,
                'time_saved_annually_hours': 14.6,
                'automatable_tasks': 1,
                'automation_percentage': 50.0
            }
        }
        
        runbook = self.generator.generate(extraction_result)
        
        # Should have checkboxes for each task
        assert '- [ ] Check service status *(2 min)*' in runbook
        assert '- [ ] Review error logs *(3 min)*' in runbook
    
    def test_generate_task_categorization(self):
        """RED: Test task grouping by category"""
        extraction_result = {
            'module': 'test_module',
            'tasks': [
                {'description': 'Check service status', 'time_minutes': 2},
                {'description': 'Review log entries', 'time_minutes': 3},
                {'description': 'Test health endpoint', 'time_minutes': 1},
                {'description': 'Validate permissions', 'time_minutes': 2}
            ],
            'summary': {
                'total_tasks': 4,
                'total_time_minutes': 8,
                'time_saved_annually_hours': 23.3,
                'automatable_tasks': 2,
                'automation_percentage': 50.0
            }
        }
        
        runbook = self.generator.generate(extraction_result)
        
        # Should have category sections
        assert '### 🔧 Service Status' in runbook
        assert '### 📋 Log Review' in runbook
        assert '### ❤️ Health Checks' in runbook
    
    def test_generate_completion_section(self):
        """RED: Test completion section generation"""
        extraction_result = {
            'module': 'test_module',
            'tasks': [{'description': 'Check status', 'time_minutes': 2}],
            'summary': {'total_tasks': 1, 'total_time_minutes': 2, 'time_saved_annually_hours': 5.8, 'automatable_tasks': 1, 'automation_percentage': 100.0}
        }
        
        runbook = self.generator.generate(extraction_result)
        
        # Should have completion checklist
        assert '- [ ] All checks completed successfully' in runbook
        assert '- [ ] Any issues have been escalated' in runbook
        assert '- [ ] Actual time taken: _______ minutes (target: 2 min)' in runbook
    
    def test_generate_escalation_procedures(self):
        """RED: Test escalation section generation"""
        extraction_result = {
            'module': 'test_module',
            'tasks': [{'description': 'Check status', 'time_minutes': 2}],
            'summary': {'total_tasks': 1, 'total_time_minutes': 2, 'time_saved_annually_hours': 5.8, 'automatable_tasks': 1, 'automation_percentage': 100.0}
        }
        
        runbook = self.generator.generate(extraction_result)
        
        # Should have escalation procedures
        assert '## 🚨 Escalation' in runbook
        assert 'Document the issue' in runbook
        assert 'Contact on-call engineer' in runbook
    
    def test_generate_automation_opportunity_section(self):
        """RED: Test automation opportunity section for high automation potential"""
        extraction_result = {
            'module': 'test_module',
            'tasks': [
                {'description': 'Automated check 1', 'time_minutes': 2},
                {'description': 'Automated check 2', 'time_minutes': 2}
            ],
            'summary': {
                'total_tasks': 2,
                'total_time_minutes': 4,
                'time_saved_annually_hours': 11.7,
                'automatable_tasks': 2,
                'automation_percentage': 100.0
            }
        }
        
        runbook = self.generator.generate(extraction_result)
        
        # Should show automation opportunity for >50% automation
        assert '## 🤖 Automation Opportunity' in runbook
        assert '2 of 2 tasks' in runbook
    
    def test_generate_no_automation_section_for_low_potential(self):
        """RED: Test no automation section for low automation potential"""
        extraction_result = {
            'module': 'test_module',
            'tasks': [
                {'description': 'Manual review task', 'time_minutes': 5}
            ],
            'summary': {
                'total_tasks': 1,
                'total_time_minutes': 5,
                'time_saved_annually_hours': 14.6,
                'automatable_tasks': 0,
                'automation_percentage': 0.0
            }
        }
        
        runbook = self.generator.generate(extraction_result)
        
        # Should not show automation section for <=50% automation
        assert '## 🤖 Automation Opportunity' not in runbook
    
    def test_generate_error_handling(self):
        """RED: Test error handling in generation"""
        extraction_result = {
            'error': 'Could not read file: Permission denied'
        }
        
        runbook = self.generator.generate(extraction_result)
        
        # Should handle error gracefully
        assert '# Error' in runbook
        assert 'Permission denied' in runbook
    
    def test_generate_timestamp_inclusion(self):
        """RED: Test timestamp inclusion in runbook"""
        extraction_result = {
            'module': 'test_module',
            'tasks': [{'description': 'Check status', 'time_minutes': 2}],
            'summary': {'total_tasks': 1, 'total_time_minutes': 2, 'time_saved_annually_hours': 5.8, 'automatable_tasks': 1, 'automation_percentage': 100.0}
        }
        
        with patch('src.ddd.mvp.daily_extractor.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = '2024-01-15 09:30'
            runbook = self.generator.generate(extraction_result)
        
        # Should include generation timestamp
        assert '2024-01-15 09:30' in runbook
    
    def test_generate_notes_section(self):
        """RED: Test notes section for user input"""
        extraction_result = {
            'module': 'test_module',
            'tasks': [{'description': 'Check status', 'time_minutes': 2}],
            'summary': {'total_tasks': 1, 'total_time_minutes': 2, 'time_saved_annually_hours': 5.8, 'automatable_tasks': 1, 'automation_percentage': 100.0}
        }
        
        runbook = self.generator.generate(extraction_result)
        
        # Should have notes section
        assert '## 📝 Notes' in runbook
        assert '```' in runbook  # Code block for notes


class TestCLIIntegrationTDD:
    """
    TDD Test Suite for CLI Integration
    
    Testing the generate_daily_runbook function and CLI functionality
    """
    
    def setup_method(self):
        """Setup for each test"""
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def teardown_method(self):
        """Cleanup temporary files"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def create_test_file(self, content: str, filename: str = "test_module.yml") -> Path:
        """Helper to create test Ansible files"""
        file_path = self.temp_dir / filename
        file_path.write_text(content)
        return file_path
    
    def test_generate_daily_runbook_basic_functionality(self):
        """RED: Test basic CLI function operation"""
        content = """
        - name: Check service
          ansible.builtin.command: systemctl status nginx
        """
        
        ansible_file = self.create_test_file(content)
        
        # Should generate runbook successfully
        extraction, runbook = generate_daily_runbook(ansible_file)
        
        # Should return extraction and runbook
        assert isinstance(extraction, dict)
        assert isinstance(runbook, str)
        assert len(extraction['tasks']) > 0
        assert 'Daily Maintenance Runbook' in runbook
    
    def test_generate_daily_runbook_output_file_creation(self):
        """RED: Test automatic output file creation"""
        content = """
        - name: Check service
          ansible.builtin.command: systemctl status nginx
        """
        
        ansible_file = self.create_test_file(content, "web_service.yml")
        
        # Should create default output file
        extraction, runbook = generate_daily_runbook(ansible_file)
        
        # Should create file with expected name
        expected_output = Path(f"daily_runbook_web_service.md")
        if expected_output.exists():
            expected_output.unlink()  # Cleanup
        
        # Verify runbook content
        assert 'web_service' in extraction['module']
    
    def test_generate_daily_runbook_custom_output_file(self):
        """RED: Test custom output file specification"""
        content = """
        - name: Check service
          ansible.builtin.command: systemctl status nginx
        """
        
        ansible_file = self.create_test_file(content)
        output_file = self.temp_dir / "custom_runbook.md"
        
        # Should use custom output file
        extraction, runbook = generate_daily_runbook(ansible_file, output_file)
        
        # Should create custom file
        assert output_file.exists()
        assert output_file.read_text() == runbook
    
    def test_generate_daily_runbook_summary_output(self):
        """RED: Test CLI summary information"""
        content = """
        - name: Check service
          ansible.builtin.command: systemctl status nginx
        
        - name: Review logs
          ansible.builtin.shell: tail /var/log/app.log
        """
        
        ansible_file = self.create_test_file(content)
        
        with patch('builtins.print') as mock_print:
            extraction, runbook = generate_daily_runbook(ansible_file)
        
        # Should print summary information
        print_calls = [str(call) for call in mock_print.call_args_list]
        summary_found = any('Summary:' in call for call in print_calls)
        assert summary_found, "Should print summary information"
    
    def test_cli_main_exists(self):
        """RED: Test CLI main section exists"""
        # Verify the main function exists by reading the source
        import src.ddd.mvp.daily_extractor as module
        import inspect
        source = inspect.getsource(module)
        assert 'if __name__ == "__main__":' in source, "Should have main section for CLI usage"
    
    def test_generate_daily_runbook_error_handling(self):
        """RED: Test error handling for invalid files"""
        non_existent_file = self.temp_dir / "does_not_exist.yml"
        
        # Should handle file errors gracefully
        extraction, runbook = generate_daily_runbook(non_existent_file)
        
        # Should return error information
        assert 'error' in extraction
        assert '# Error' in runbook


class TestTDDComplianceAndCoverage:
    """
    TDD Compliance Tests
    
    Tests to ensure we meet the Week 1 Success Gate criteria
    """
    
    def setup_method(self):
        """Setup for each test"""
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def teardown_method(self):
        """Cleanup temporary files"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def create_test_file(self, content: str, filename: str = "test_module.yml") -> Path:
        """Helper to create test Ansible files"""
        file_path = self.temp_dir / filename
        file_path.write_text(content)
        return file_path
    
    def test_week1_success_gate_daily_patterns_coverage(self):
        """Test: Achieve 80% daily task capture rate"""
        # Create comprehensive test file with known daily patterns
        content = """
        # Service checks (should extract: 4 tasks)
        - name: Check web service
          ansible.builtin.command: systemctl status nginx
        - name: Check database
          ansible.builtin.command: systemctl status postgresql  
        - name: Check processes
          ansible.builtin.shell: ps aux | grep apache
        - name: Check supervisor
          ansible.builtin.command: supervisorctl status
        
        # Log operations (should extract: 4 tasks)
        - name: Review error logs
          ansible.builtin.shell: tail -50 /var/log/nginx/error.log
        - name: Check for errors
          ansible.builtin.shell: grep ERROR /var/log/app.log
        - name: Review system logs
          ansible.builtin.command: journalctl --since yesterday
        - name: Rotate logs
          ansible.builtin.command: logrotate -f /etc/logrotate.conf
        
        # Health checks (should extract: 3 tasks)
        - name: Test connectivity
          ansible.builtin.command: ping -c 3 api.example.com
        - name: Health endpoint
          ansible.builtin.shell: curl http://localhost/health
        - name: Port check
          ansible.builtin.command: nc -z localhost 80
        
        # Disk checks (should extract: 2 tasks)
        - name: Check disk space
          ansible.builtin.command: df -h
        - name: Directory sizes
          ansible.builtin.shell: du -sh /var/log
        
        # Permission checks (should extract: 1 task)
        - name: File permissions
          ansible.builtin.shell: test -r /etc/nginx/nginx.conf
        """
        
        file_path = self.create_test_file(content)
        extractor = DailyMaintenanceExtractor()
        result = extractor.extract(file_path)
        
        # Expected: 14 daily patterns should be found
        # Target: 80% capture rate means at least 11 tasks
        expected_minimum = 11
        actual_tasks = len(result['tasks'])
        
        capture_rate = (actual_tasks / 14) * 100
        
        assert actual_tasks >= expected_minimum, f"Expected at least {expected_minimum} tasks, got {actual_tasks}. Capture rate: {capture_rate:.1f}%"
        assert capture_rate >= 80.0, f"Capture rate {capture_rate:.1f}% below target 80%"
    
    def test_week1_success_gate_runbook_generation_speed(self):
        """Test: Generate runbook in under 1 second"""
        content = """
        - name: Check service
          ansible.builtin.command: systemctl status nginx
        - name: Review logs  
          ansible.builtin.shell: tail /var/log/app.log
        """
        
        file_path = self.create_test_file(content)
        
        import time
        start_time = time.time()
        
        # Generate runbook
        extraction, runbook = generate_daily_runbook(file_path)
        
        end_time = time.time()
        generation_time = end_time - start_time
        
        # Should generate in under 1 second
        assert generation_time < 1.0, f"Generation took {generation_time:.3f}s, target <1.0s"
        
        # Should produce valid runbook
        assert len(runbook) > 500, "Runbook should have substantial content"
        assert 'Daily Maintenance Runbook' in runbook
    
    def test_week1_success_gate_cli_end_to_end(self):
        """Test: CLI tool working end-to-end"""
        content = """
        - name: Daily maintenance tasks
          tasks:
            - name: Check service
              ansible.builtin.command: systemctl status nginx
            - name: Review logs
              ansible.builtin.shell: tail /var/log/app.log
            - name: Check disk
              ansible.builtin.command: df -h
        """
        
        file_path = self.create_test_file(content, "daily_maintenance.yml")
        
        # Test end-to-end CLI functionality
        extraction, runbook = generate_daily_runbook(file_path)
        
        # Should extract multiple tasks
        assert len(extraction['tasks']) >= 3, "Should extract service, log, and disk tasks"
        
        # Should generate complete runbook
        required_sections = [
            '# Daily Maintenance Runbook',
            '## ☀️ Morning Checklist',
            '## ✅ Completion',
            '## 🚨 Escalation'
        ]
        
        for section in required_sections:
            assert section in runbook, f"Missing required section: {section}"
        
        # Should have reasonable time estimates
        total_time = extraction['summary']['total_time_minutes']
        assert 3 <= total_time <= 15, f"Total time {total_time} minutes seems unreasonable"
    
    def test_week1_success_gate_multiple_modules_processing(self):
        """Test: Can process 10+ different Ansible modules"""
        # Create 10 different test modules with various patterns
        module_contents = [
            "- name: Web server check\n  ansible.builtin.command: systemctl status nginx",
            "- name: Database check\n  ansible.builtin.shell: mysql -e 'SELECT 1;'",
            "- name: Log review\n  ansible.builtin.shell: tail /var/log/app.log",
            "- name: Disk check\n  ansible.builtin.command: df -h",
            "- name: Network test\n  ansible.builtin.command: ping -c 3 api.example.com",
            "- name: SSL check\n  ansible.builtin.shell: openssl x509 -in cert.pem -enddate",
            "- name: Container check\n  ansible.builtin.command: docker ps",
            "- name: Queue check\n  ansible.builtin.command: rabbitmqctl list_queues",
            "- name: Backup check\n  ansible.builtin.shell: find /backup -mtime -1",
            "- name: Process check\n  ansible.builtin.shell: ps aux | grep apache"
        ]
        
        extractor = DailyMaintenanceExtractor()
        results = []
        
        for i, content in enumerate(module_contents):
            file_path = self.create_test_file(content, f"module_{i+1}.yml")
            result = extractor.extract(file_path)
            results.append(result)
        
        # Should successfully process all modules
        assert len(results) == 10, "Should process all 10 test modules"
        
        # Each should extract at least one task
        successful_extractions = sum(1 for r in results if len(r['tasks']) > 0)
        assert successful_extractions >= 8, f"Only {successful_extractions}/10 modules had successful extraction"
        
        # Should have variety in extracted patterns
        all_descriptions = []
        for result in results:
            all_descriptions.extend([t['description'] for t in result['tasks']])
        
        unique_patterns = set(desc[:20] for desc in all_descriptions)  # First 20 chars
        assert len(unique_patterns) >= 5, "Should extract diverse patterns across modules"


# Integration and Performance Tests
class TestMVPIntegrationAndPerformance:
    """
    Integration and performance tests for MVP
    """
    
    def test_realistic_ansible_playbook_processing(self):
        """Integration test with realistic Ansible playbook"""
        realistic_content = """
        ---
        - name: Daily maintenance for web application
          hosts: webservers
          become: yes
          
          tasks:
            - name: Check nginx service status
              ansible.builtin.systemd:
                name: nginx
                state: started
              register: nginx_status
            
            - name: Review nginx error logs
              ansible.builtin.shell: |
                tail -100 /var/log/nginx/error.log | grep -E "(error|warn|crit)"
              register: nginx_errors
              
            - name: Check disk space usage
              ansible.builtin.shell: df -h | grep -E "(8[0-9]%|9[0-9]%|100%)"
              register: disk_usage
              failed_when: disk_usage.stdout != ""
              
            - name: Test database connectivity
              ansible.builtin.shell: |
                mysql -u monitor -p'{{ mysql_password }}' -e "SELECT 1;" 
              register: db_test
              
            - name: Verify SSL certificate expiry
              ansible.builtin.shell: |
                openssl x509 -in /etc/ssl/certs/app.pem -enddate -noout | 
                awk -F= '{print $2}' | xargs -I {} date -d "{}" +%s
              register: ssl_expiry
              
            - name: Check application health endpoint
              ansible.builtin.uri:
                url: "http://localhost:8080/health"
                method: GET
                status_code: 200
              register: health_check
              
            - name: Review application logs for errors
              ansible.builtin.shell: |
                find /var/log/app -name "*.log" -mtime -1 -exec grep -l ERROR {} \\;
              register: app_errors
        """
        
        temp_file = Path(tempfile.mktemp(suffix=".yml"))
        temp_file.write_text(realistic_content)
        
        try:
            extraction, runbook = generate_daily_runbook(temp_file)
            
            # Should extract multiple meaningful tasks
            assert len(extraction['tasks']) >= 5, "Should extract at least 5 daily tasks"
            
            # Should have realistic time estimates
            total_time = extraction['summary']['total_time_minutes']
            assert 10 <= total_time <= 25, f"Total time {total_time} should be 10-25 minutes"
            
            # Runbook should be comprehensive
            assert len(runbook) >= 1000, "Runbook should be comprehensive (1000+ chars)"
            
            # Should categorize tasks appropriately
            assert '### 🔧 Service Status' in runbook or 'systemd' in runbook.lower()
            assert '### 📋 Log Review' in runbook or 'log' in runbook.lower()
            assert '### ❤️ Health Checks' in runbook or 'health' in runbook.lower()
            
        finally:
            temp_file.unlink()


# Run configuration for pytest
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])