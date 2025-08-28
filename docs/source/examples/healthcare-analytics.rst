HealthCorp Analytics Platform - Azure Infrastructure Documentation
================================================================

.. note::
   This document provides comprehensive infrastructure documentation for maintenance and troubleshooting.
   Generated from standardized templates to ensure consistency across all client projects.

Project Overview
---------------

:Client: HealthCorp Regional Medical Center
:Project: Patient Analytics Platform
:Environment: Production
:Azure Subscription: HealthCorp-Production (hc-prod-12345)
:Resource Groups: rg-healthcorp-analytics-prod, rg-healthcorp-shared-prod
:Region(s): East US 2, West US 2
:Last Updated: 2025-08-27

.. warning::
   **Production Environment**: This documentation covers production infrastructure.
   All changes must follow established change management procedures.
   **HIPAA Compliance**: This system processes PHI - follow all security protocols.

Architecture Overview
--------------------

.. graphviz::

   digraph infrastructure {
       rankdir=TB;
       node [shape=rectangle, style=filled];
       
       // User Layer
       users [label="Healthcare Staff\n(Internal Network Only)", fillcolor=lightblue];
       
       // Network Layer  
       appgw [label="Application Gateway\napg-healthcorp-prod\nWAF Enabled", fillcolor=lightgreen];
       vnet [label="Virtual Network\nvnet-healthcorp-prod\n10.10.0.0/16", fillcolor=lightgreen];
       
       // Application Layer
       webapp [label="Analytics Dashboard\napp-healthcorp-analytics\nASP.NET Core", fillcolor=orange];
       api [label="Patient Data API\napp-healthcorp-api\nC# Web API", fillcolor=orange];
       
       // Data Layer
       sqldb [label="Patient Database\nsql-healthcorp-prod\nPatientAnalytics", fillcolor=yellow];
       storage [label="Data Lake Storage\nsahealthcorpprod\nHL7 Messages", fillcolor=yellow];
       
       // Monitoring
       appinsights [label="Application Insights\nai-healthcorp-prod", fillcolor=pink];
       
       users -> appgw;
       appgw -> webapp;
       webapp -> api;
       api -> sqldb;
       api -> storage;
       webapp -> appinsights;
       api -> appinsights;
   }

Security Configuration
---------------------

Azure Active Directory
~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Service Principals & App Registrations
   :header-rows: 1
   :widths: 30 30 40

   * - Name
     - Application ID
     - Purpose
   * - HealthCorp-Analytics-API
     - a1b2c3d4-e5f6-7890-abcd-ef1234567890
     - API authentication and SQL access
   * - HealthCorp-PowerBI-Reader
     - b2c3d4e5-f6g7-8901-bcde-f23456789012
     - PowerBI data source connection

Key Vault Configuration
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   Key Vault: kv-healthcorp-prod-eastus2
   Resource Group: rg-healthcorp-shared-prod
   Location: East US 2
   
   Access Policies:
   - Principal: HealthCorp Analytics Team
     Permissions: 
       Secrets: [get, list]
       Keys: [get, decrypt, encrypt]
   
   Critical Secrets:
   - sql-patient-db-connection-string
   - external-hl7-api-key
   - powerbi-service-account-password

.. warning::
   **Secret Rotation**: Database connection strings rotate every 90 days.
   HL7 API keys rotate every 180 days. PowerBI service account password rotates every 60 days per HIPAA compliance.

Resource-Based Access Control (RBAC)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Production Resource Group Permissions
   :header-rows: 1
   :widths: 40 30 30

   * - Principal
     - Role
     - Scope
   * - HealthCorp IT Team
     - Contributor
     - rg-healthcorp-analytics-prod
   * - HealthCorp-Analytics-API
     - SQL DB Contributor
     - PatientAnalytics Database
   * - Azure Monitor Service
     - Monitoring Reader
     - Entire Subscription

Network Configuration
--------------------

Virtual Network Details
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Virtual Network: vnet-healthcorp-prod
   Address Space: 10.10.0.0/16
   DNS Servers: 10.10.1.4, 10.10.1.5 (Domain Controllers)
   
   Subnets:
   - snet-web: 10.10.1.0/24 (Web Tier)
   - snet-app: 10.10.2.0/24 (Application Tier)  
   - snet-data: 10.10.3.0/24 (Database Tier)
   - snet-mgmt: 10.10.100.0/24 (Management)

Network Security Groups
~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Critical Firewall Rules
   :header-rows: 1
   :widths: 20 20 20 20 20

   * - NSG Name
     - Direction
     - Port
     - Source
     - Purpose
   * - nsg-web-tier
     - Inbound
     - 443
     - 10.0.0.0/8
     - HTTPS from internal network only
   * - nsg-app-tier
     - Inbound
     - 8080
     - 10.10.1.0/24
     - API Communication from web tier
   * - nsg-data-tier
     - Inbound
     - 1433
     - 10.10.2.0/24
     - Database Access from app tier only

.. caution::
   **HIPAA Compliance**: All external access blocked. VPN required for remote access.
   NSG changes require Security Team + HIPAA Officer approval.

Application Services
-------------------

Web Applications
~~~~~~~~~~~~~~~

.. list-table:: App Service Configuration
   :header-rows: 1
   :widths: 25 25 50

   * - Property
     - Value
     - Notes
   * - App Service Plan
     - ASP-HealthCorp-Prod (P2V3)
     - Auto-scaling enabled (2-10 instances)
   * - Runtime Stack
     - .NET 8.0
     - LTS version for stability
   * - Deployment Slots
     - staging, production
     - Blue-green deployment strategy
   * - Custom Domains
     - analytics.healthcorp.local
     - Internal domain with SSL from internal CA

Environment Variables & App Settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Application Configuration
   ASPNETCORE_ENVIRONMENT=Production
   LOG_LEVEL=Information
   
   # Database Connection (from Key Vault)
   CONNECTION_STRING=@Microsoft.KeyVault(SecretUri=https://kv-healthcorp-prod.vault.azure.net/secrets/sql-patient-db-connection-string)
   
   # HL7 Integration Service
   HL7_API_ENDPOINT=https://hl7-gateway.healthcorp.local/api/v2
   HL7_API_KEY=@Microsoft.KeyVault(SecretUri=https://kv-healthcorp-prod.vault.azure.net/secrets/external-hl7-api-key)
   
   # Application Insights
   APPINSIGHTS_INSTRUMENTATIONKEY=12345678-1234-1234-1234-123456789012
   APPINSIGHTS_CONNECTION_STRING=InstrumentationKey=12345678-1234-1234-1234-123456789012

.. important::
   **HIPAA Requirement**: All configuration changes must be logged and approved.
   Application restart required for environment variable changes.

Database Configuration
---------------------

SQL Database Details
~~~~~~~~~~~~~~~~~~~

.. list-table:: Database Information
   :header-rows: 1
   :widths: 30 70

   * - Property
     - Value
   * - Server Name
     - sql-healthcorp-prod.database.windows.net
   * - Database Name
     - PatientAnalytics
   * - Service Tier
     - Premium P4 (500 DTU)
   * - Collation
     - SQL_Latin1_General_CP1_CI_AS
   * - Backup Retention
     - 35 days (HIPAA requirement)
   * - Geo-Replication
     - ENABLED - West US 2

Connection Strings
~~~~~~~~~~~~~~~~~

.. code-block:: text

   Production (Azure AD):
   Server=sql-healthcorp-prod.database.windows.net;Database=PatientAnalytics;Authentication=Active Directory Integrated;

   Service Principal (API):
   Server=sql-healthcorp-prod.database.windows.net;Database=PatientAnalytics;Authentication=Active Directory Service Principal;

.. warning::
   **HIPAA Compliance**: All database connections must use encryption.
   Connection strings stored in Key Vault only. No plaintext credentials allowed.

Database Schema Overview
~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Critical Tables
   :header-rows: 1
   :widths: 25 25 50

   * - Table Name
     - Purpose
     - Dependencies
   * - Patients
     - Patient demographics (PHI)
     - None (root table)
   * - Encounters 
     - Hospital visits and admissions
     - FK to Patients
   * - LabResults
     - Laboratory test results
     - FK to Encounters, LabTests
   * - Medications
     - Patient medication history
     - FK to Patients, DrugCatalog

.. important::
   **PHI Data**: Tables containing PHI are encrypted at rest and in transit.
   Access logging enabled for all PHI queries per HIPAA requirements.

Monitoring & Observability
-------------------------

Application Insights Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   Application Insights: ai-healthcorp-prod
   Instrumentation Key: 12345678-1234-1234-1234-123456789012
   
   Key Metrics Tracked:
   - API Response Time (target: <500ms)
   - Database Query Performance
   - Patient Record Access Patterns
   - HIPAA Audit Events
   
   Alerts Configured:
   - API Response Time >1s (Critical)
   - Database Connection Failures (Critical)
   - Unauthorized PHI Access Attempts (Critical)
   - Failed Authentication >10/hour (High)

Log Analytics Workspace
~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Log Sources
   :header-rows: 1
   :widths: 30 40 30

   * - Source
     - Log Type
     - Retention
   * - Web Apps
     - Application + Security Logs
     - 7 years (HIPAA)
   * - SQL Database
     - Query Performance + Access Logs
     - 7 years (HIPAA)
   * - Network Security Groups
     - Flow Logs
     - 1 year

.. note::
   **HIPAA Requirement**: All PHI access must be logged and retained for 7 years.
   Log Analytics configured for long-term retention and audit compliance.

Troubleshooting Guides
---------------------

Common Issues & Solutions
~~~~~~~~~~~~~~~~~~~~~~~~

Database Connection Timeouts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Symptoms**: Applications report database connection failures during peak hours (8-10 AM).

**Investigation Steps**:

1. Check Application Insights for database dependency failures
2. Verify SQL Database DTU usage (should be <80% during peak)
3. Check connection pool configuration in application
4. Verify network connectivity from app subnet to database

.. code-block:: bash

   # Check database performance
   az sql db show-usage --name PatientAnalytics --resource-group rg-healthcorp-analytics-prod --server sql-healthcorp-prod

**Resolution**: Identified connection pool exhaustion during morning patient rounds. Increased max pool size from 100 to 200 connections.

Slow Report Generation
^^^^^^^^^^^^^^^^^^^^^^

**Symptoms**: Monthly compliance reports taking >10 minutes to generate.

**Investigation Steps**:

1. Check Application Insights performance blade for slow queries
2. Review database query execution plans for report queries
3. Check if maintenance tasks are running during report generation
4. Verify PowerBI refresh schedules don't conflict

.. code-block:: sql

   -- Check long-running queries during report generation
   SELECT 
       r.session_id,
       r.command,
       r.total_elapsed_time/1000.0 as elapsed_seconds,
       t.text as query_text
   FROM sys.dm_exec_requests r
   CROSS APPLY sys.dm_exec_sql_text(r.sql_handle) t
   WHERE r.total_elapsed_time > 30000  -- >30 seconds
   ORDER BY r.total_elapsed_time DESC

**Resolution**: Added covering index on Patients(AdmitDate, DischargeDate) including frequently accessed columns.

HIPAA Audit Alert
^^^^^^^^^^^^^^^^

**Symptoms**: Automated alert for unusual PHI access pattern.

**Investigation Steps**:

1. Check Application Insights for authentication events
2. Review SQL Database audit logs for PHI table access
3. Verify user permissions and access patterns
4. Check for service account or application authentication issues

.. warning::
   **HIPAA Incident**: All PHI access alerts must be investigated within 1 hour.
   Document findings in HIPAA incident log regardless of outcome.

Emergency Contacts & Escalation
------------------------------

.. list-table:: Contact Information
   :header-rows: 1
   :widths: 25 35 20 20

   * - Role
     - Name
     - Email
     - Phone
   * - Primary Engineer
     - Sarah Johnson
     - sarah.johnson@yourcompany.com
     - (555) 123-4567
   * - Database Administrator
     - Mike Chen
     - mike.chen@yourcompany.com
     - (555) 234-5678
   * - Security/HIPAA Officer
     - Lisa Rodriguez
     - lisa.rodriguez@yourcompany.com
     - (555) 345-6789
   * - HealthCorp IT Director
     - Dr. Robert Smith
     - robert.smith@healthcorp.org
     - (555) 456-7890

**Escalation Path**:

1. **Severity 1** (PHI Breach/System Down): Immediate call to Primary Engineer + Security Officer + Client IT Director
2. **Severity 2** (Performance Issues): Email Primary Engineer + DBA, escalate after 30 min
3. **Severity 3** (Minor Issues): Email Primary Engineer during business hours (7 AM - 6 PM EST)

.. danger::
   **HIPAA Breach Protocol**: Any suspected PHI exposure requires immediate notification
   of Security Officer and client HIPAA Officer within 15 minutes.

Change Management
----------------

.. warning::
   **All production changes must follow the established change management process.**
   **HIPAA Requirement**: All changes to PHI systems require documented approval.

**Change Categories**:

* **Emergency**: PHI exposure, production outage
* **Standard**: Pre-approved changes with documented procedures  
* **Normal**: All other changes requiring CAB + HIPAA Officer approval

**Maintenance Windows**:

* **Weekly**: Sundays 2:00-6:00 AM EST for standard maintenance
* **Monthly**: First Saturday 11:00 PM - 3:00 AM EST for major updates
* **HIPAA Freeze**: No changes during month-end reporting period (last 3 business days)

**Approval Requirements**:
* Database changes: DBA + Security Officer
* Application changes: Primary Engineer + Security Officer  
* Network changes: Network Team + Security Officer + HIPAA Officer

Links & References
-----------------

* **Azure Portal**: https://portal.azure.com
* **Application Insights**: https://portal.azure.com/#@healthcorp.org/resource/subscriptions/12345/resourceGroups/rg-healthcorp-analytics-prod/providers/Microsoft.Insights/components/ai-healthcorp-prod
* **Key Vault**: https://portal.azure.com/#@healthcorp.org/resource/subscriptions/12345/resourceGroups/rg-healthcorp-shared-prod/providers/Microsoft.KeyVault/vaults/kv-healthcorp-prod
* **SQL Database**: https://portal.azure.com/#@healthcorp.org/resource/subscriptions/12345/resourceGroups/rg-healthcorp-analytics-prod/providers/Microsoft.Sql/servers/sql-healthcorp-prod/databases/PatientAnalytics
* **Change Management System**: https://servicedesk.yourcompany.com/changes
* **HIPAA Incident Log**: https://compliance.yourcompany.com/hipaa-incidents

---

.. footer::

   *Document generated using Infrastructure Documentation Standards*
   
   :Template: azure-infrastructure.rst v1.0
   :Generated: 2025-08-27 14:30:00
   :Next Review: 2025-11-27
   :Contact: Infrastructure Documentation Team
   :HIPAA Classification: Business Associate Documentation