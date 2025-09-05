# DDD Extractor Implementation - Maintenance Focus
Updated: 2025-09-05
Priority: Extract maintenance procedures, not just API documentation

## Extractor Architecture Evolution

### Layer 1: Maintenance Pattern Extractors (NEW PRIORITY)

#### DailyMaintenanceExtractor
```python
class DailyMaintenanceExtractor(BaseExtractor):
    """Extracts patterns for daily operational tasks"""
    
    def extract_health_checks(self, code: str) -> Dict:
        """Find health verification patterns"""
        patterns = {
            'status_checks': self._find_status_patterns(code),
            'resource_monitors': self._find_resource_checks(code),
            'validation_methods': self._find_validation_patterns(code),
            'log_locations': self._find_logging_patterns(code)
        }
        return patterns
    
    def extract_monitoring_points(self, code: str) -> Dict:
        """Find what should be monitored"""
        return {
            'metrics': self._find_metric_patterns(code),
            'thresholds': self._find_threshold_values(code),
            'alert_conditions': self._find_alert_patterns(code)
        }
    
    def generate_daily_runbook(self, patterns: Dict) -> str:
        """Generate daily maintenance runbook"""
        # Template-based generation
        return self._fill_daily_template(patterns)
```

#### WeeklyMaintenanceExtractor
```python
class WeeklyMaintenanceExtractor(BaseExtractor):
    """Extracts patterns for weekly maintenance tasks"""
    
    def extract_update_procedures(self, code: str) -> Dict:
        """Find update/patch patterns"""
        return {
            'pre_update_checks': self._find_validation_patterns(code),
            'backup_procedures': self._find_backup_patterns(code),
            'update_sequence': self._find_update_order(code),
            'rollback_triggers': self._find_rollback_conditions(code)
        }
    
    def extract_configuration_management(self, code: str) -> Dict:
        """Find configuration parameters and requirements"""
        return {
            'parameters': self._find_config_params(code),
            'safe_ranges': self._infer_safe_values(code),
            'restart_required': self._find_restart_patterns(code),
            'hot_reload': self._find_reload_patterns(code)
        }
```

#### MonthlyMaintenanceExtractor
```python
class MonthlyMaintenanceExtractor(BaseExtractor):
    """Extracts patterns for monthly/quarterly tasks"""
    
    def extract_capacity_planning(self, code: str) -> Dict:
        """Find resource growth patterns"""
        return {
            'resource_limits': self._find_limits(code),
            'scaling_triggers': self._find_scale_patterns(code),
            'growth_indicators': self._find_growth_patterns(code),
            'cleanup_procedures': self._find_cleanup_patterns(code)
        }
    
    def extract_compliance_requirements(self, code: str) -> Dict:
        """Find audit and compliance needs"""
        return {
            'audit_logs': self._find_audit_patterns(code),
            'required_evidence': self._find_evidence_patterns(code),
            'retention_policies': self._find_retention_patterns(code)
        }
```

### Layer 2: Traditional Extractors (UPDATED)

#### PermissionExtractor (Enhanced)
```python
class PermissionExtractor(BaseExtractor):
    """Now focuses on operational permissions"""
    
    def extract_operational_permissions(self, code: str) -> Dict:
        """Extract permissions needed for maintenance"""
        return {
            'daily_tasks': self._permissions_for_routine(code),
            'weekly_tasks': self._permissions_for_updates(code),
            'emergency_tasks': self._permissions_for_recovery(code),
            'escalation_required': self._permissions_needing_escalation(code)
        }
```

#### ErrorPatternExtractor (Enhanced)
```python
class ErrorPatternExtractor(BaseExtractor):
    """Now generates recovery procedures"""
    
    def extract_error_recovery(self, code: str) -> Dict:
        """Extract errors AND their recovery procedures"""
        errors = self._find_error_patterns(code)
        for error in errors:
            error['recovery_procedure'] = self._generate_recovery(error)
            error['escalation_trigger'] = self._determine_escalation(error)
            error['prevention_steps'] = self._generate_prevention(error)
        return errors
```

### Layer 3: Maintenance Scenario Generators (NEW)

#### ScenarioGenerator
```python
class MaintenanceScenarioGenerator:
    """Generates maintenance scenarios from extracted patterns"""
    
    def generate_routine_scenarios(self, patterns: Dict) -> List[Dict]:
        """Generate routine maintenance scenarios"""
        scenarios = []
        
        # Daily scenarios
        scenarios.extend(self._generate_daily_scenarios(patterns['daily']))
        
        # Weekly scenarios  
        scenarios.extend(self._generate_weekly_scenarios(patterns['weekly']))
        
        # Monthly scenarios
        scenarios.extend(self._generate_monthly_scenarios(patterns['monthly']))
        
        return scenarios
    
    def generate_validation_procedures(self, operations: List) -> Dict:
        """For each operation, generate validation steps"""
        validations = {}
        for op in operations:
            validations[op] = {
                'pre_checks': self._generate_pre_checks(op),
                'post_validation': self._generate_post_validation(op),
                'success_criteria': self._define_success(op)
            }
        return validations
```

## Pattern Recognition Updates

### What We Now Look For

#### Health Check Patterns
```python
HEALTH_PATTERNS = [
    r'\.status\(\)',
    r'\.is_alive\(\)',
    r'\.ping\(\)',
    r'health_check',
    r'verify_.*\(\)',
    r'check_.*\(\)',
    r'test_connection'
]
```

#### Configuration Patterns
```python
CONFIG_PATTERNS = [
    r'DEFAULT_\w+\s*=',
    r'\.get\(["\'].*?["\']\s*,\s*.*?\)',  # config.get('key', default)
    r'environ\[',
    r'getenv\(',
    r'config\[',
    r'settings\.'
]
```

#### Update/Rollback Patterns
```python
UPDATE_PATTERNS = [
    r'backup',
    r'snapshot',
    r'rollback',
    r'restore',
    r'upgrade',
    r'update',
    r'patch',
    r'migrate'
]
```

## AST-Based Extraction (Following DDD_AST_ARCHITECTURE_DECISION)

```python
class ASTMaintenanceExtractor:
    """Uses AST for reliable pattern extraction"""
    
    def extract_maintenance_patterns(self, source: str) -> Dict:
        tree = ast.parse(source)
        
        patterns = {
            'health_checks': [],
            'config_params': [],
            'error_handlers': [],
            'resource_checks': []
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if 'check' in node.name or 'verify' in node.name:
                    patterns['health_checks'].append(self._extract_function_pattern(node))
            
            elif isinstance(node, ast.Assign):
                if self._is_config_assignment(node):
                    patterns['config_params'].append(self._extract_config(node))
            
            elif isinstance(node, ast.Try):
                patterns['error_handlers'].append(self._extract_error_handling(node))
        
        return patterns
```

## Output Format Evolution

### Old Output (API Documentation)
```yaml
function: getUserData
parameters:
  - name: userId
    type: string
returns: UserObject
description: Retrieves user data by ID
```

### New Output (Maintenance Documentation)
```yaml
daily_maintenance:
  health_check:
    procedure: "GET /health/user-service"
    expected: "200 OK with {status: 'healthy'}"
    timeout: 5s
    failure_action: "Check database connectivity"
    
weekly_maintenance:
  update_procedure:
    pre_check: "Verify <50 active sessions"
    backup: "pg_dump users > backup_$(date).sql"
    update: "npm update user-service"
    validation: "Run smoke tests"
    rollback: "npm install user-service@previous"
    
monthly_maintenance:
  capacity_check:
    metric: "user_table_size"
    threshold: "80% of max"
    action: "Archive users inactive >1 year"
```

## Integration with Coverage Calculator

```python
class MaintenanceCoverageCalculator:
    """Calculates maintenance readiness, not documentation coverage"""
    
    def calculate_coverage(self, extracted: Dict) -> Dict:
        return {
            'daily_readiness': self._calc_daily_coverage(extracted),
            'weekly_readiness': self._calc_weekly_coverage(extracted),
            'monthly_readiness': self._calc_monthly_coverage(extracted),
            'overall': self._calc_overall_maintenance_readiness(extracted),
            'risk_areas': self._identify_maintenance_gaps(extracted)
        }
    
    def _calc_daily_coverage(self, extracted: Dict) -> float:
        """
        Daily readiness = 
        - Has health checks: 25%
        - Has monitoring points: 25%
        - Has validation methods: 25%
        - Has escalation triggers: 25%
        """
        score = 0.0
        if extracted.get('health_checks'): score += 0.25
        if extracted.get('monitoring'): score += 0.25
        if extracted.get('validation'): score += 0.25
        if extracted.get('escalation'): score += 0.25
        return score
```

## Priority Implementation Order

1. **Week 1-2**: DailyMaintenanceExtractor (highest value)
2. **Week 3-4**: WeeklyMaintenanceExtractor (update procedures)
3. **Week 5-6**: ErrorRecoveryExtractor (prevention focus)
4. **Week 7-8**: ComplianceExtractor (audit readiness)
5. **Week 9-10**: ScenarioGenerator (tie it all together)

This implementation shifts DDD from measuring "what's documented" to enabling "what's maintainable".