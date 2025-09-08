# Documentation Schema Definition Language (DSDL) Specification v1.0

## Overview

DSDL is a YAML-based schema language for writing executable documentation that generates implementation code, tests, and monitoring configurations. It prioritizes maintenance and troubleshooting needs over API description.

## Core Principles

1. **Maintenance First**: Every element considers the 2AM debugging scenario
2. **Executable Specifications**: Documentation that generates working code
3. **Bidirectional Binding**: Code changes can update documentation
4. **Runtime Validation**: Continuous verification of documented behavior

## Schema Structure

### Root Elements

```yaml
# Required root elements
@service: ServiceName                    # Service identifier
@version: 1.0.0                          # Documentation version
@maintainer: team@company.com            # Primary contact
@2am-contact: +1-555-HELP               # Emergency contact

# Optional metadata
@tags: [critical, payment, customer-facing]
@sla: 99.99%
@runbook: https://wiki/runbooks/service
```

### Dependencies Section

```yaml
dependencies:
  runtime:                               # Required at runtime
    - name: PostgreSQL
      version: ">=13.0 <16.0"           # Semantic versioning
      connection: "${DATABASE_URL}"      # Environment variable
      health_check: "SELECT 1"           # Validation query
      timeout: 5000ms
      failure_mode: cascade              # cascade|degrade|fail
      recovery:                          # Recovery procedures
        - "Check connection pool"
        - "Restart database connection"
        - "Escalate to DBA if persists"
      
  services:                              # External service dependencies
    - name: PaymentGateway
      type: REST
      endpoint: "${PAYMENT_API_URL}"
      timeout: 30000ms
      retry: 
        attempts: 3
        backoff: exponential
      circuit_breaker:
        threshold: 5
        timeout: 60000ms
      fallback: "Queue for later processing"
      
  libraries:                             # Package dependencies
    - name: express
      version: "^4.18.0"
      purpose: "HTTP server framework"
      alternatives: ["fastify", "koa"]
```

### Operations Section

```yaml
operations:
  create_order:                          # Operation identifier
    description: "Creates a new order in the system"
    criticality: high                    # high|medium|low
    
    # Normal behavior baseline
    normal_behavior:
      response_time: 
        p50: 100ms
        p95: 200ms
        p99: 500ms
      success_rate: 99.9%
      throughput: 1000req/min
      
    # Input parameters with validation
    parameters:
      customer_id:
        type: uuid
        source: request.body             # request.body|request.query|request.header
        required: true
        validation:
          format: "UUID v4"
          exists_in: "customers table"
        sanitization:
          - trim
          - lowercase
        example: "123e4567-e89b-12d3-a456-426614174000"
        
      items:
        type: array
        source: request.body
        required: true
        validation:
          min_items: 1
          max_items: 100
        schema:
          product_id: 
            type: string
            validation: "exists in products"
          quantity:
            type: integer
            validation: "between 1 and 999"
    
    # State changes
    state_changes:
      creates:
        - entity: Order
          table: orders
          indexes: [order_id, customer_id, created_at]
      updates:
        - entity: Inventory
          table: inventory
          condition: "Decrements available quantity"
      publishes:
        - event: OrderCreated
          channel: orders.created
          format: CloudEvents
    
    # Error scenarios with troubleshooting
    error_scenarios:
      - code: ORD_001
        condition: "Customer not found"
        response: 
          status: 404
          body: {error: "Customer not found"}
        troubleshoot:
          - "Verify customer_id exists in customers table"
          - "Check if customer account is active"
          - "Verify customer service is responding"
        monitoring:
          metric: orders_customer_not_found_total
          log_level: warning
          
      - code: ORD_002
        condition: "Insufficient inventory"
        response:
          status: 409
          body: {error: "Insufficient inventory", available: <quantity>}
        troubleshoot:
          - "Check current inventory levels"
          - "Verify inventory service is synchronized"
          - "Check for pending inventory updates"
        recovery:
          - "Trigger inventory refresh"
          - "Notify customer of availability"
        monitoring:
          metric: orders_insufficient_inventory_total
          alert: "Rate > 10/min"
```

### Monitoring Section

```yaml
monitoring:
  # Metrics to collect
  metrics:
    - name: operation_duration_seconds
      type: histogram
      labels: [operation, status]
      buckets: [0.1, 0.25, 0.5, 1, 2.5, 5, 10]
      
    - name: operation_total
      type: counter
      labels: [operation, status, error_code]
      
    - name: active_connections
      type: gauge
      labels: [service]
  
  # Alerts configuration
  alerts:
    - name: HighErrorRate
      condition: "error_rate > 5%"
      window: 5m
      severity: warning
      notification:
        - pagerduty: platform-team
        - slack: #platform-alerts
      runbook: "https://wiki/runbooks/high-error-rate"
      
    - name: LatencyDegradation  
      condition: "p95_latency > 2 * baseline"
      window: 10m
      severity: critical
      notification:
        - pagerduty: on-call
      runbook: "https://wiki/runbooks/latency"
  
  # Distributed tracing
  tracing:
    enabled: true
    sample_rate: 0.1
    propagation: w3c
    exporter: jaeger
  
  # Logging configuration
  logging:
    level: info
    format: json
    fields:
      - timestamp
      - level
      - message
      - operation
      - trace_id
      - error_code
    never_log:
      - password
      - credit_card
      - ssn
```

### Validation Rules Section

```yaml
validation_rules:
  # Business rules that must hold
  invariants:
    - name: OrderTotalPositive
      rule: "order.total > 0"
      error: "Order total must be positive"
      
    - name: InventoryNonNegative  
      rule: "inventory.available >= 0"
      error: "Inventory cannot be negative"
      
  # Pre-conditions
  preconditions:
    - name: CustomerActive
      rule: "customer.status == 'active'"
      error: "Customer must be active"
      
  # Post-conditions  
  postconditions:
    - name: OrderCreatedEvent
      rule: "event.type == 'OrderCreated' was published"
      error: "OrderCreated event not published"
```

### Recovery Procedures Section

```yaml
recovery_procedures:
  database_connection_lost:
    symptoms:
      - "Connection timeout errors"
      - "ECONNREFUSED in logs"
      - "503 responses increasing"
    diagnosis:
      - "Check database process: `systemctl status postgresql`"
      - "Verify network connectivity: `ping db.internal`"
      - "Check connection pool: `SELECT count(*) FROM pg_stat_activity`"
    recovery:
      automatic:
        - "Reconnect with exponential backoff"
        - "Circuit breaker activates after 5 failures"
      manual:
        - "Restart application: `kubectl rollout restart deployment/app`"
        - "Reset connection pool: `psql -c 'SELECT pg_terminate_backend(pid)...'`"
        - "Escalate to DBA for database restart"
    prevention:
      - "Configure connection pool timeouts"
      - "Implement health checks"
      - "Set up connection pool monitoring"
```

## Type System

### Primitive Types
- `string`: UTF-8 text
- `integer`: 64-bit signed integer  
- `number`: 64-bit float
- `boolean`: true/false
- `uuid`: UUID v4 format
- `timestamp`: ISO-8601 format
- `duration`: ISO-8601 duration (e.g., PT5M)

### Complex Types
```yaml
types:
  Address:
    fields:
      street: string
      city: string
      postal_code: 
        type: string
        validation: "regex: ^[0-9]{5}$"
      country:
        type: string
        validation: "enum: [US, CA, MX]"
        
  Money:
    fields:
      amount:
        type: number
        validation: "precision: 2"
      currency:
        type: string
        validation: "ISO-4217 code"
```

## Code Generation Directives

### Implementation Hints
```yaml
operations:
  process_payment:
    implementation:
      language_hints:
        python:
          async: true
          framework: fastapi
          libraries: [stripe, sqlalchemy]
        typescript:
          async: true
          framework: express
          libraries: [stripe-node, typeorm]
      
      performance_hints:
        cache: 
          key: "payment:${customer_id}"
          ttl: 3600
        batch_size: 100
        parallelism: 4
```

### Test Generation
```yaml
operations:
  calculate_discount:
    test_cases:
      - name: "Regular customer discount"
        input: {customer_type: "regular", amount: 100}
        expected: {discount: 10, total: 90}
        
      - name: "VIP customer discount"  
        input: {customer_type: "vip", amount: 100}
        expected: {discount: 20, total: 80}
        
      edge_cases:
        - name: "Zero amount"
          input: {amount: 0}
          expected_error: "Amount must be positive"
```

## Maintenance Annotations

### Operational Metadata
```yaml
@maintenance:
  patch_window: "Sunday 2-4 AM UTC"
  restart_safe: true
  stateless: false
  data_retention: "90 days"
  backup_required: true
  
@deprecation:
  deprecated: "2024-01-01"
  sunset: "2024-07-01"  
  migration: "Use v2/orders instead"
  
@security:
  authentication: oauth2
  authorization: rbac
  rate_limit: "1000/hour per user"
  encryption: "TLS 1.3+"
```

## Validation Examples

### Contract Validation
```yaml
# DSDL Contract
operations:
  get_user:
    parameters:
      id: {type: uuid, required: true}
    normal_behavior:
      response_time: "<100ms"

# Generated validation
def validate_contract(implementation):
    # Parameter validation
    assert 'id' in implementation.parameters
    assert implementation.parameters['id'].type == UUID
    
    # Performance validation
    assert measure_response_time() < 100  # ms
```

### Runtime Validation
```yaml
# Runtime behavior monitoring
monitor:
  actual_response_time = measure_p95_latency()
  documented_response_time = dsdl.normal_behavior.response_time.p95
  
  if actual_response_time > documented_response_time * 1.2:
    alert("Performance degradation detected")
    propose_doc_update(actual_response_time)
```

## File Organization

### Recommended Structure
```
services/
├── orders/
│   ├── orders.dsdl.yaml           # Main service documentation
│   ├── types.dsdl.yaml           # Shared type definitions
│   └── recovery.dsdl.yaml        # Recovery procedures
├── payments/
│   ├── payments.dsdl.yaml
│   └── integration.dsdl.yaml     # Integration specifications
└── shared/
    ├── types.dsdl.yaml           # Cross-service types
    └── monitoring.dsdl.yaml      # Shared monitoring config
```

## Tools and Commands

### CLI Usage
```bash
# Validate DSDL files
dsdl validate services/**/*.dsdl.yaml

# Generate code from DSDL
dsdl generate orders.dsdl.yaml --language python --output src/

# Check implementation against documentation
dsdl verify src/orders.py --spec orders.dsdl.yaml

# Generate tests
dsdl generate-tests orders.dsdl.yaml --framework pytest

# Update documentation from runtime
dsdl update orders.dsdl.yaml --from-runtime prometheus

# Start documentation server
dsdl serve --port 8080
```

## Version History

- **v1.0.0** (2024-08): Initial specification
  - Core schema definition
  - Code generation support
  - Validation framework
  - Monitoring integration
