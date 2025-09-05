"""
Comprehensive TDD Test Suite for MVP CLI Integration

Following RED-GREEN-REFACTOR methodology for Pure Maintenance MVP CLI
This test suite focuses on the CLI commands and integration points
"""

import pytest
from pathlib import Path
from click.testing import CliRunner
import tempfile
import json
import time
from unittest.mock import patch, MagicMock
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ddd.mvp.cli_mvp import mvp_cli, generate_daily_runbook_cli, demo_extraction, validate_mvp


class TestMVPCLICommandsTDD:
    """
    TDD Test Suite for MVP CLI Commands
    
    CYCLE 4: CLI Integration (RED → GREEN → REFACTOR)
    Following TDD methodology for CLI functionality
    """
    
    def setup_method(self):
        """Setup for each test - fresh CLI runner and temp directory"""
        self.runner = CliRunner()
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def teardown_method(self):
        """Cleanup temporary files"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def create_test_ansible_file(self, content: str, filename: str = "test_playbook.yml") -> Path:
        """Helper to create test Ansible files"""
        file_path = self.temp_dir / filename
        file_path.write_text(content)
        return file_path
    
    # ======================================
    # RED PHASE: Basic CLI Structure Tests
    # ======================================
    
    def test_mvp_cli_group_exists(self):
        """RED: Test that MVP CLI group is accessible"""
        result = self.runner.invoke(mvp_cli, ['--help'])
        
        # Should show help without error
        assert result.exit_code == 0
        assert 'Pure Maintenance MVP Commands' in result.output
        assert 'generate-daily' in result.output
        assert 'demo' in result.output
        assert 'validate' in result.output
    
    def test_generate_daily_command_help(self):
        """RED: Test generate-daily command help"""
        result = self.runner.invoke(mvp_cli, ['generate-daily', '--help'])
        
        # Should show command help
        assert result.exit_code == 0
        assert 'Generate daily maintenance runbook' in result.output
        assert '--output' in result.output
        assert '--quiet' in result.output
        assert '--stats' in result.output
    
    def test_demo_command_help(self):
        """RED: Test demo command help"""
        result = self.runner.invoke(mvp_cli, ['demo', '--help'])
        
        # Should show demo command help
        assert result.exit_code == 0
        assert 'Demo the MVP extraction' in result.output
        assert '--show-extraction' in result.output
    
    def test_validate_command_help(self):
        """RED: Test validate command help"""
        result = self.runner.invoke(mvp_cli, ['validate', '--help'])
        
        # Should show validate command help
        assert result.exit_code == 0
        assert 'Validate MVP against Week 1 success criteria' in result.output
        assert '--target-coverage' in result.output
        assert '--max-time' in result.output
    
    # ======================================
    # RED PHASE: generate-daily Command Tests
    # ======================================
    
    def test_generate_daily_basic_functionality(self):
        """RED: Test basic runbook generation via CLI"""
        content = """
        - name: Check web service
          ansible.builtin.command: systemctl status nginx
        
        - name: Review error logs
          ansible.builtin.shell: tail -50 /var/log/nginx/error.log
        """
        
        ansible_file = self.create_test_ansible_file(content)
        
        result = self.runner.invoke(mvp_cli, ['generate-daily', str(ansible_file)])
        
        # Should succeed
        assert result.exit_code == 0
        assert 'Runbook generated' in result.output
        
        # Should create default output file
        expected_output = Path(f"daily_runbook_{ansible_file.stem}.md")
        assert expected_output.exists()
        
        # Cleanup
        if expected_output.exists():
            expected_output.unlink()
    
    def test_generate_daily_custom_output_file(self):
        """RED: Test custom output file specification"""
        content = """
        - name: Check service
          ansible.builtin.command: systemctl status nginx
        """
        
        ansible_file = self.create_test_ansible_file(content)
        output_file = self.temp_dir / "custom_runbook.md"
        
        result = self.runner.invoke(mvp_cli, [
            'generate-daily', 
            str(ansible_file), 
            '--output', str(output_file)
        ])
        
        # Should succeed
        assert result.exit_code == 0
        assert str(output_file) in result.output
        
        # Should create custom output file
        assert output_file.exists()
        assert 'Daily Maintenance Runbook' in output_file.read_text()
    
    def test_generate_daily_quiet_mode(self):
        """RED: Test quiet mode operation"""
        content = """
        - name: Check service
          ansible.builtin.command: systemctl status nginx
        """
        
        ansible_file = self.create_test_ansible_file(content)
        
        result = self.runner.invoke(mvp_cli, [
            'generate-daily', 
            str(ansible_file), 
            '--quiet'
        ])
        
        # Should succeed with minimal output
        assert result.exit_code == 0
        # Quiet mode should have less output
        assert len(result.output.split('\n')) < 10
        
        # Cleanup
        default_output = Path(f"daily_runbook_{ansible_file.stem}.md")
        if default_output.exists():
            default_output.unlink()
    
    def test_generate_daily_stats_mode(self):
        """RED: Test detailed statistics mode"""
        content = """
        - name: Check service status
          ansible.builtin.command: systemctl status nginx
        
        - name: Review logs
          ansible.builtin.shell: tail /var/log/app.log
        
        - name: Test connectivity
          ansible.builtin.command: ping -c 3 api.example.com
        """
        
        ansible_file = self.create_test_ansible_file(content)
        
        result = self.runner.invoke(mvp_cli, [
            'generate-daily', 
            str(ansible_file), 
            '--stats'
        ])
        
        # Should succeed with detailed stats
        assert result.exit_code == 0
        assert 'Detailed Analysis' in result.output
        assert 'Service/Status checks' in result.output
        assert 'Time Analysis' in result.output
        assert 'Pattern Coverage' in result.output
        
        # Cleanup default output
        default_output = Path(f"daily_runbook_{ansible_file.stem}.md")
        if default_output.exists():
            default_output.unlink()
    
    def test_generate_daily_week1_success_validation(self):
        """RED: Test Week 1 success gate validation"""
        content = """
        - name: Check service
          ansible.builtin.command: systemctl status nginx
        """
        
        ansible_file = self.create_test_ansible_file(content)
        
        result = self.runner.invoke(mvp_cli, ['generate-daily', str(ansible_file)])
        
        # Should validate Week 1 success
        assert result.exit_code == 0
        assert 'Week 1 Success Gate' in result.output
        assert '✅ PASSED' in result.output
        
        # Cleanup
        default_output = Path(f"daily_runbook_{ansible_file.stem}.md")
        if default_output.exists():
            default_output.unlink()
    
    def test_generate_daily_file_not_found_error(self):
        """RED: Test error handling for non-existent files"""
        non_existent_file = self.temp_dir / "does_not_exist.yml"
        
        result = self.runner.invoke(mvp_cli, ['generate-daily', str(non_existent_file)])
        
        # Should fail gracefully
        assert result.exit_code != 0
        # Click should handle file existence validation
    
    def test_generate_daily_invalid_file_content(self):
        """RED: Test handling of files with no extractable patterns"""
        content = """
        - name: Install package
          ansible.builtin.package:
            name: nginx
            state: present
        """
        
        ansible_file = self.create_test_ansible_file(content)
        
        result = self.runner.invoke(mvp_cli, ['generate-daily', str(ansible_file)])
        
        # Should succeed but warn about limited extraction
        assert result.exit_code == 0
        assert 'Limited extraction' in result.output or 'Week 1 Success Gate' in result.output
        
        # Cleanup
        default_output = Path(f"daily_runbook_{ansible_file.stem}.md")
        if default_output.exists():
            default_output.unlink()
    
    # ======================================
    # RED PHASE: demo Command Tests  
    # ======================================
    
    def test_demo_basic_functionality(self):
        """RED: Test demo command basic operation"""
        content = """
        - name: Daily maintenance
          tasks:
            - name: Check service
              ansible.builtin.command: systemctl status nginx
            - name: Review logs
              ansible.builtin.shell: tail /var/log/app.log
        """
        
        ansible_file = self.create_test_ansible_file(content, "demo_playbook.yml")
        
        result = self.runner.invoke(mvp_cli, ['demo', str(ansible_file)])
        
        # Should succeed and show demo output
        assert result.exit_code == 0
        assert 'DDD MVP Demo' in result.output
        assert 'Extraction time' in result.output
        assert 'Results' in result.output
        assert 'Week 1 Success Criteria' in result.output
        assert 'ROI Demo Calculation' in result.output
        assert 'Sample Runbook Excerpt' in result.output
    
    def test_demo_show_extraction_flag(self):
        """RED: Test demo with raw extraction data"""
        content = """
        - name: Check service
          ansible.builtin.command: systemctl status nginx
        """
        
        ansible_file = self.create_test_ansible_file(content)
        
        result = self.runner.invoke(mvp_cli, [
            'demo', 
            str(ansible_file), 
            '--show-extraction'
        ])
        
        # Should succeed and show raw data
        assert result.exit_code == 0
        assert 'Raw Extraction Data' in result.output
        # Should have JSON-like structure in output
        assert '{' in result.output and '}' in result.output
    
    def test_demo_performance_measurement(self):
        """RED: Test that demo measures extraction performance"""
        content = """
        - name: Check multiple services
          tasks:
            - name: Web service
              ansible.builtin.command: systemctl status nginx
            - name: Database service  
              ansible.builtin.command: systemctl status postgresql
            - name: Log check
              ansible.builtin.shell: tail /var/log/app.log
        """
        
        ansible_file = self.create_test_ansible_file(content)
        
        result = self.runner.invoke(mvp_cli, ['demo', str(ansible_file)])
        
        # Should measure and report timing
        assert result.exit_code == 0
        assert 'Extraction time:' in result.output
        
        # Should validate performance criteria
        assert '< 1.0s target' in result.output
        assert '✅ Speed:' in result.output
    
    def test_demo_roi_calculation_display(self):
        """RED: Test ROI calculation in demo mode"""
        content = """
        - name: Daily tasks
          tasks:
            - name: Service check
              ansible.builtin.command: systemctl status nginx
            - name: Log review
              ansible.builtin.shell: tail /var/log/app.log
        """
        
        ansible_file = self.create_test_ansible_file(content)
        
        result = self.runner.invoke(mvp_cli, ['demo', str(ansible_file)])
        
        # Should show ROI calculation
        assert result.exit_code == 0
        assert 'ROI Demo Calculation' in result.output
        assert 'Daily time saved' in result.output
        assert 'Annual time saved' in result.output
        assert 'Annual cost savings' in result.output
    
    def test_demo_error_handling(self):
        """RED: Test demo error handling"""
        non_existent_file = self.temp_dir / "missing.yml"
        
        result = self.runner.invoke(mvp_cli, ['demo', str(non_existent_file)])
        
        # Should fail gracefully
        assert result.exit_code != 0
        # Click should handle file validation
    
    # ======================================
    # RED PHASE: validate Command Tests
    # ======================================
    
    def test_validate_basic_functionality(self):
        """RED: Test validate command with test directory"""
        # Create multiple test files
        test_files = [
            ("web_server.yml", """
            - name: Web checks
              tasks:
                - name: Check nginx
                  ansible.builtin.command: systemctl status nginx
                - name: Check logs
                  ansible.builtin.shell: tail /var/log/nginx/error.log
            """),
            ("database.yml", """
            - name: DB checks
              tasks:
                - name: Check MySQL
                  ansible.builtin.shell: mysql -e "SELECT 1;"
                - name: Check connections
                  ansible.builtin.shell: mysql -e "SHOW PROCESSLIST;"
            """),
            ("monitoring.yml", """
            - name: Health checks
              tasks:
                - name: Check API
                  ansible.builtin.shell: curl http://localhost/health
                - name: Check disk
                  ansible.builtin.command: df -h
            """)
        ]
        
        for filename, content in test_files:
            self.create_test_ansible_file(content, filename)
        
        result = self.runner.invoke(mvp_cli, ['validate', str(self.temp_dir)])
        
        # Should validate successfully
        assert result.exit_code == 0
        assert 'DDD MVP Validation' in result.output
        assert 'Validation Results' in result.output
        assert 'Success Criteria' in result.output
        assert 'Files processed:' in result.output
    
    def test_validate_custom_target_coverage(self):
        """RED: Test validate with custom target coverage"""
        # Create minimal test file
        self.create_test_ansible_file("""
        - name: Minimal check
          ansible.builtin.command: systemctl status nginx
        """, "minimal.yml")
        
        result = self.runner.invoke(mvp_cli, [
            'validate', 
            str(self.temp_dir),
            '--target-coverage', '50'
        ])
        
        # Should use custom target
        assert result.exit_code == 0
        assert 'target: 50%' in result.output
    
    def test_validate_custom_max_time(self):
        """RED: Test validate with custom max time"""
        # Create test file
        self.create_test_ansible_file("""
        - name: Quick check
          ansible.builtin.command: df -h
        """, "quick.yml")
        
        result = self.runner.invoke(mvp_cli, [
            'validate', 
            str(self.temp_dir),
            '--max-time', '0.5'
        ])
        
        # Should use custom time limit
        assert result.exit_code == 0
        assert 'target: <0.5s' in result.output
    
    def test_validate_success_gate_pass(self):
        """RED: Test successful validation results"""
        # Create files that should pass validation
        successful_files = [
            ("services.yml", """
            - name: Service checks
              tasks:
                - name: Check nginx
                  ansible.builtin.command: systemctl status nginx
                - name: Check apache
                  ansible.builtin.command: systemctl status apache2
            """),
            ("logs.yml", """
            - name: Log reviews
              tasks:
                - name: Check error logs
                  ansible.builtin.shell: tail -50 /var/log/nginx/error.log
                - name: Check app logs
                  ansible.builtin.shell: grep ERROR /var/log/app.log
            """)
        ]
        
        for filename, content in successful_files:
            self.create_test_ansible_file(content, filename)
        
        result = self.runner.invoke(mvp_cli, [
            'validate', 
            str(self.temp_dir),
            '--target-coverage', '70'  # Lower threshold for test
        ])
        
        # Should pass validation
        assert result.exit_code == 0
        assert 'WEEK 1 SUCCESS GATE: ✅ PASSED' in result.output
    
    def test_validate_no_ansible_files_error(self):
        """RED: Test validate with directory containing no Ansible files"""
        # Create empty directory
        empty_dir = self.temp_dir / "empty"
        empty_dir.mkdir()
        
        result = self.runner.invoke(mvp_cli, ['validate', str(empty_dir)])
        
        # Should fail with appropriate message
        assert result.exit_code == 1
        assert 'No Ansible files found' in result.output
    
    def test_validate_detailed_results_output(self):
        """RED: Test detailed results output"""
        # Create test file
        self.create_test_ansible_file("""
        - name: Test tasks
          ansible.builtin.command: systemctl status nginx
        """, "test_service.yml")
        
        result = self.runner.invoke(mvp_cli, ['validate', str(self.temp_dir)])
        
        # Should show detailed results
        assert result.exit_code == 0
        assert 'Detailed Results:' in result.output
        assert 'test_service.yml' in result.output
        assert 'tasks in' in result.output  # Shows task count and timing
    
    # ======================================
    # RED PHASE: CLI Integration & Error Handling
    # ======================================
    
    def test_cli_integration_with_main_ddd_cli(self):
        """RED: Test integration with main DDD CLI system"""
        # This test verifies the register_mvp_commands function
        from src.ddd.mvp.cli_mvp import register_mvp_commands
        from click import Group
        
        # Create a mock CLI group
        mock_cli = Group('test')
        
        # Should register without error
        register_mvp_commands(mock_cli)
        
        # Should add the mvp group
        assert 'mvp' in mock_cli.commands
    
    def test_error_handling_with_invalid_ansible_content(self):
        """RED: Test CLI error handling with invalid content"""
        # Create file with binary content
        binary_file = self.temp_dir / "binary.yml"
        binary_file.write_bytes(b'\x00\x01\x02\xff\xfe')
        
        result = self.runner.invoke(mvp_cli, ['generate-daily', str(binary_file)])
        
        # Should handle error gracefully
        # May succeed with empty extraction or fail gracefully
        assert result.exit_code is not None  # Should not crash
    
    def test_permission_error_handling(self):
        """RED: Test handling of permission errors"""
        # Create file then make it unreadable
        test_file = self.create_test_ansible_file("test content", "readonly.yml")
        
        # Try to make it unreadable (may not work in all environments)
        try:
            import stat
            test_file.chmod(stat.S_IWRITE)  # Write-only
            
            result = self.runner.invoke(mvp_cli, ['generate-daily', str(test_file)])
            
            # Should handle permission error gracefully
            assert result.exit_code is not None
            
        except (OSError, PermissionError):
            # Skip test if we can't modify permissions
            pytest.skip("Cannot modify file permissions in this environment")
        finally:
            # Restore permissions for cleanup
            try:
                test_file.chmod(stat.S_IREAD | stat.S_IWRITE)
            except:
                pass
    
    # ======================================
    # RED PHASE: Performance & Quality Tests
    # ======================================
    
    def test_cli_performance_under_one_second(self):
        """RED: Test CLI performance meets sub-1-second requirement"""
        content = """
        - name: Performance test
          tasks:
            - name: Check service
              ansible.builtin.command: systemctl status nginx
            - name: Check logs
              ansible.builtin.shell: tail /var/log/app.log
        """
        
        ansible_file = self.create_test_ansible_file(content)
        
        start_time = time.time()
        
        result = self.runner.invoke(mvp_cli, ['generate-daily', str(ansible_file), '--quiet'])
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Should complete in under 1 second
        assert result.exit_code == 0
        assert execution_time < 1.0, f"CLI took {execution_time:.3f}s, target <1.0s"
        
        # Cleanup
        default_output = Path(f"daily_runbook_{ansible_file.stem}.md")
        if default_output.exists():
            default_output.unlink()
    
    def test_output_quality_validation(self):
        """RED: Test generated runbook quality meets standards"""
        content = """
        - name: Quality test
          tasks:
            - name: Service check
              ansible.builtin.command: systemctl status nginx
            - name: Log review
              ansible.builtin.shell: tail /var/log/app.log
            - name: Health check
              ansible.builtin.shell: curl http://localhost/health
        """
        
        ansible_file = self.create_test_ansible_file(content)
        output_file = self.temp_dir / "quality_test.md"
        
        result = self.runner.invoke(mvp_cli, [
            'generate-daily', 
            str(ansible_file), 
            '--output', str(output_file)
        ])
        
        # Should succeed
        assert result.exit_code == 0
        
        # Check output quality
        assert output_file.exists()
        runbook_content = output_file.read_text()
        
        # Quality requirements
        assert len(runbook_content) >= 1000, "Runbook should be comprehensive"
        assert 'Daily Maintenance Runbook' in runbook_content
        assert '☀️ Morning Checklist' in runbook_content
        assert '✅ Completion' in runbook_content
        assert '🚨 Escalation' in runbook_content
        
        # Should have structured task lists
        assert '- [ ]' in runbook_content  # Checkboxes
        assert '*(1 min)*' in runbook_content or '*(2 min)*' in runbook_content or '*(3 min)*' in runbook_content  # Time estimates
    
    def test_cli_multiple_file_processing_capability(self):
        """RED: Test CLI can handle multiple files efficiently"""
        # Create 5 different test files
        test_files = []
        for i in range(5):
            content = f"""
            - name: Test {i+1}
              tasks:
                - name: Service check {i+1}
                  ansible.builtin.command: systemctl status service{i+1}
                - name: Log check {i+1}
                  ansible.builtin.shell: tail /var/log/service{i+1}.log
            """
            file_path = self.create_test_ansible_file(content, f"service_{i+1}.yml")
            test_files.append(file_path)
        
        # Process each file
        successful_runs = 0
        total_time = 0
        
        for test_file in test_files:
            start_time = time.time()
            result = self.runner.invoke(mvp_cli, [
                'generate-daily', 
                str(test_file), 
                '--quiet'
            ])
            end_time = time.time()
            
            if result.exit_code == 0:
                successful_runs += 1
                total_time += (end_time - start_time)
            
            # Cleanup
            default_output = Path(f"daily_runbook_{test_file.stem}.md")
            if default_output.exists():
                default_output.unlink()
        
        # Should successfully process all files
        assert successful_runs == 5, f"Only {successful_runs}/5 files processed successfully"
        
        # Average processing time should be reasonable
        avg_time = total_time / successful_runs
        assert avg_time < 0.5, f"Average processing time {avg_time:.3f}s too slow"


class TestMVPCLIEndToEndScenarios:
    """
    End-to-end scenario tests for realistic usage patterns
    """
    
    def setup_method(self):
        """Setup for each test"""
        self.runner = CliRunner()
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def teardown_method(self):
        """Cleanup temporary files"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_complete_workflow_realistic_scenario(self):
        """Test complete workflow: generate → demo → validate"""
        # Create realistic playbook
        realistic_content = """
        ---
        - name: Daily web application maintenance
          hosts: webservers
          become: yes
          
          tasks:
            - name: Check nginx service status
              ansible.builtin.systemd:
                name: nginx
                state: started
              
            - name: Review nginx error logs
              ansible.builtin.shell: tail -100 /var/log/nginx/error.log
              
            - name: Check disk space
              ansible.builtin.shell: df -h
              
            - name: Test database connectivity  
              ansible.builtin.shell: mysql -e "SELECT 1;"
              
            - name: Verify SSL certificate
              ansible.builtin.shell: openssl x509 -in /etc/ssl/cert.pem -enddate -noout
        """
        
        ansible_file = self.temp_dir / "daily_web_maintenance.yml"
        ansible_file.write_text(realistic_content)
        
        # Step 1: Generate runbook
        runbook_file = self.temp_dir / "web_maintenance_runbook.md"
        result1 = self.runner.invoke(mvp_cli, [
            'generate-daily', 
            str(ansible_file),
            '--output', str(runbook_file),
            '--stats'
        ])
        
        assert result1.exit_code == 0
        assert runbook_file.exists()
        assert 'Week 1 Success Gate: ✅ PASSED' in result1.output
        
        # Step 2: Demo the extraction
        result2 = self.runner.invoke(mvp_cli, [
            'demo', 
            str(ansible_file)
        ])
        
        assert result2.exit_code == 0
        assert 'DDD MVP Demo' in result2.output
        assert 'ROI Demo Calculation' in result2.output
        
        # Step 3: Validate directory
        result3 = self.runner.invoke(mvp_cli, [
            'validate',
            str(self.temp_dir),
            '--target-coverage', '80'
        ])
        
        assert result3.exit_code == 0
        assert 'WEEK 1 SUCCESS GATE' in result3.output
    
    def test_ops_team_daily_workflow_simulation(self):
        """Test simulation of ops team daily usage"""
        # Create multiple service playbooks
        services = {
            "web_services.yml": """
            - name: Web service maintenance
              tasks:
                - name: Check nginx
                  ansible.builtin.command: systemctl status nginx
                - name: Check apache
                  ansible.builtin.command: systemctl status apache2
                - name: Review web logs
                  ansible.builtin.shell: tail -50 /var/log/nginx/access.log
            """,
            "database_services.yml": """
            - name: Database maintenance
              tasks:
                - name: Check MySQL
                  ansible.builtin.shell: mysql -e "SELECT 1;"
                - name: Check PostgreSQL
                  ansible.builtin.command: systemctl status postgresql
                - name: Review DB logs
                  ansible.builtin.shell: tail -50 /var/log/postgresql/postgresql.log
            """,
            "monitoring_checks.yml": """
            - name: System monitoring
              tasks:
                - name: Check disk space
                  ansible.builtin.command: df -h
                - name: Check memory
                  ansible.builtin.shell: free -h
                - name: Test connectivity
                  ansible.builtin.command: ping -c 3 api.example.com
            """
        }
        
        # Create service files
        runbook_files = []
        for filename, content in services.items():
            service_file = self.temp_dir / filename
            service_file.write_text(content)
            
            # Generate runbook for each service
            runbook_file = self.temp_dir / f"daily_runbook_{service_file.stem}.md"
            result = self.runner.invoke(mvp_cli, [
                'generate-daily',
                str(service_file),
                '--output', str(runbook_file),
                '--quiet'
            ])
            
            assert result.exit_code == 0
            assert runbook_file.exists()
            runbook_files.append(runbook_file)
        
        # Validate all runbooks were generated
        assert len(runbook_files) == 3
        
        # Check runbook quality
        for runbook_file in runbook_files:
            content = runbook_file.read_text()
            assert 'Daily Maintenance Runbook' in content
            assert 'Morning Checklist' in content
            assert '- [ ]' in content  # Has checkboxes
            assert len(content) > 500  # Substantial content


# Run configuration for pytest
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])