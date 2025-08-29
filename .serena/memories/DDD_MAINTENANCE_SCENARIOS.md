# DDD Maintenance Scenarios Framework

## Maintenance Work Distribution

### Proactive Maintenance (70%) - Planned Work
Scheduled, preventable tasks that keep systems healthy:

#### 1. Patching & Updates
- Security patches
- Dependency updates
- OS/kernel updates
- Certificate renewals

#### 2. Monitoring & Observability
- Metric collection setup
- Alert threshold configuration
- Dashboard creation
- Log aggregation

#### 3. Access & Permissions
- Cloud IAM configurations
- Service account management
- SSH/RDP access setup
- API key rotation

#### 4. Infrastructure Management
- Network topology understanding
- Load balancer configuration
- Firewall rules
- DNS management

### Reactive Maintenance (30%) - Unplanned Work
Incident response and troubleshooting tasks:

#### 5. Service Connectivity
- How to connect to services
- Debugging connection issues
- Service discovery

#### 6. Business Logic Understanding
- What the service actually does
- Critical business flows
- Data flow and dependencies

#### 7. Incident Response
- Error diagnosis procedures
- Rollback processes
- Recovery procedures

## Scenario Detection Patterns

### What Static Analysis CAN Detect
- Import statements and dependencies
- Environment variable usage
- API client instantiations
- Database connections
- Error handling blocks
- Configuration file references

### What Requires Inference
- Required IAM permissions from API calls
- Failure scenarios from retry logic
- Environment differences from conditionals
- Business rules from validation patterns

### What Requires Human Input
- Business context and intent
- Recovery time objectives
- Scaling triggers and thresholds
- Edge case handling
- Upstream/downstream impacts