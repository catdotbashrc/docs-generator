[DATABASE_NAME] - SQL Database Documentation
==========================================

.. note::
   This template provides standardized SQL database documentation for troubleshooting and maintenance.
   Critical for resolving "Where is the config for X?" scenarios.

Database Overview
----------------

:Database Name: [DATABASE_NAME]
:SQL Server: [SQL_SERVER_NAME].database.windows.net
:Resource Group: [RESOURCE_GROUP]
:Subscription: [SUBSCRIPTION_NAME]
:Service Tier: [SERVICE_TIER] ([DTU_VCORES])
:Location: [LOCATION]
:Collation: [COLLATION]
:Created Date: [CREATED_DATE]
:Last Updated: [UPDATE_DATE]

.. important::
   **Critical Database Information**: This section contains essential connection and configuration details
   required for application troubleshooting and maintenance operations.

Connection Information
---------------------

Connection Strings
~~~~~~~~~~~~~~~~~

.. tabs::

   .. tab:: Production (Azure AD)

      .. code-block:: text

         Server=[SQL_SERVER_NAME].database.windows.net;
         Database=[DATABASE_NAME];
         Authentication=Active Directory Integrated;
         Encrypt=True;
         TrustServerCertificate=False;
         Connection Timeout=30;

   .. tab:: Production (SQL Auth)

      .. code-block:: text

         Server=[SQL_SERVER_NAME].database.windows.net;
         Database=[DATABASE_NAME];
         User ID=[USERNAME];
         Password=[REFERENCE_KEY_VAULT];
         Encrypt=True;
         TrustServerCertificate=False;
         Connection Timeout=30;

   .. tab:: Application Config

      .. code-block:: bash

         # Environment variable (recommended)
         DATABASE_CONNECTION_STRING=@Microsoft.KeyVault(SecretUri=[SECRET_URI])
         
         # Direct reference (development only)
         DATABASE_CONNECTION_STRING="Server=[SERVER];Database=[DB];..."

Authentication & Access
~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Database Access Configuration
   :header-rows: 1
   :widths: 25 25 25 25

   * - Authentication Method
     - Principal
     - Role
     - Purpose
   * - Azure AD
     - [AAD_GROUP_NAME]
     - db_datareader, db_datawriter
     - Application runtime access
   * - SQL Authentication  
     - [SQL_USERNAME]
     - db_owner
     - Database administration
   * - Service Principal
     - [SP_NAME]
     - db_datareader
     - Monitoring and backup

.. warning::
   **Password Management**: SQL Authentication passwords are stored in Azure Key Vault: [KEY_VAULT_NAME]
   Secret Name: [SECRET_NAME] | Rotation Schedule: Every 90 days

Firewall & Network Access
~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Firewall Rules
   :header-rows: 1
   :widths: 30 25 25 20

   * - Rule Name
     - Start IP
     - End IP
     - Purpose
   * - AllowAzureServices
     - 0.0.0.0
     - 0.0.0.0
     - Azure services access
   * - [APP_SUBNET_RULE]
     - [START_IP]
     - [END_IP]
     - Application subnet access
   * - [MGMT_RULE]
     - [MGMT_IP]
     - [MGMT_IP]
     - Management access

Database Schema
--------------

Schema Overview
~~~~~~~~~~~~~~

.. list-table:: Database Objects Summary
   :header-rows: 1
   :widths: 30 20 50

   * - Object Type
     - Count
     - Notes
   * - User Tables
     - [TABLE_COUNT]
     - Core business data
   * - Views
     - [VIEW_COUNT]
     - Data access layer
   * - Stored Procedures
     - [SP_COUNT]
     - Business logic & data operations
   * - Functions
     - [FUNCTION_COUNT]
     - Utility and calculation functions
   * - Indexes
     - [INDEX_COUNT]
     - Performance optimization

Critical Tables
~~~~~~~~~~~~~~

.. list-table:: Core Business Tables
   :header-rows: 1
   :widths: 25 35 40

   * - Table Name
     - Purpose
     - Key Dependencies
   * - [TABLE_1_NAME]
     - [TABLE_1_PURPOSE]
     - [TABLE_1_DEPENDENCIES]
   * - [TABLE_2_NAME]
     - [TABLE_2_PURPOSE]
     - [TABLE_2_DEPENDENCIES]
   * - [TABLE_3_NAME]
     - [TABLE_3_PURPOSE]
     - [TABLE_3_DEPENDENCIES]

Entity Relationship Diagram
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. graphviz::

   digraph database_erd {
       rankdir=LR;
       node [shape=record, style=filled, fillcolor=lightblue];
       
       // Define tables with key fields
       table1 [label="{[TABLE_1]|[KEY_FIELDS]}"];
       table2 [label="{[TABLE_2]|[KEY_FIELDS]}"];
       table3 [label="{[TABLE_3]|[KEY_FIELDS]}"];
       
       // Define relationships
       table1 -> table2 [label="1:M"];
       table2 -> table3 [label="M:1"];
   }

Data Dictionary
~~~~~~~~~~~~~~

**[CRITICAL_TABLE_NAME]**

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Column Name
     - Data Type
     - Nullable
     - Description
   * - [COL_1]
     - [TYPE_1]
     - [NULL_1]
     - [DESC_1]
   * - [COL_2]
     - [TYPE_2]
     - [NULL_2]
     - [DESC_2]
   * - [COL_3]
     - [TYPE_3]
     - [NULL_3]
     - [DESC_3]

Performance Configuration
------------------------

Service Tier Details
~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   Current Configuration:
   - Service Tier: [SERVICE_TIER]
   - Compute Size: [COMPUTE_SIZE] 
   - Storage: [STORAGE_GB] GB
   - Max DTU/vCores: [MAX_DTU_VCORES]
   - Max Log Rate: [LOG_RATE] MB/s
   - Max Worker Threads: [MAX_WORKERS]
   
   Performance Baseline:
   - Average CPU: [AVG_CPU]%
   - Peak CPU: [PEAK_CPU]%
   - Average DTU/vCore Usage: [AVG_DTU]%
   - Peak DTU/vCore Usage: [PEAK_DTU]%

Indexing Strategy
~~~~~~~~~~~~~~~~

.. list-table:: Critical Indexes
   :header-rows: 1
   :widths: 30 25 45

   * - Index Name
     - Table
     - Columns
   * - [INDEX_1_NAME]
     - [TABLE_1]
     - [INDEX_1_COLUMNS]
   * - [INDEX_2_NAME]
     - [TABLE_2]
     - [INDEX_2_COLUMNS]

.. note::
   **Index Maintenance**: Index rebuild/reorganize occurs during Sunday maintenance window.
   Statistics are updated automatically but can be manually updated if query performance degrades.

Query Performance Insights
~~~~~~~~~~~~~~~~~~~~~~~~~

**Top Resource-Consuming Queries** (Last 7 days):

.. code-block:: sql

   -- Query 1: [DESCRIPTION]
   -- Average Duration: [AVG_DURATION]ms
   -- CPU Time: [CPU_TIME]ms
   -- Logical Reads: [LOGICAL_READS]
   
   [QUERY_TEXT_1]
   
   -- Query 2: [DESCRIPTION]  
   -- Average Duration: [AVG_DURATION]ms
   -- CPU Time: [CPU_TIME]ms
   -- Logical Reads: [LOGICAL_READS]
   
   [QUERY_TEXT_2]

Backup & Recovery
----------------

Backup Configuration
~~~~~~~~~~~~~~~~~~~

.. list-table:: Backup Settings
   :header-rows: 1
   :widths: 30 70

   * - Setting
     - Value
   * - Point-in-Time Restore
     - [PITR_RETENTION] days
   * - Long-term Retention (LTR)
     - Weekly: [WEEKLY_RETENTION], Monthly: [MONTHLY_RETENTION], Yearly: [YEARLY_RETENTION]
   * - Geo-Redundant Backup
     - [ENABLED/DISABLED]
   * - Backup Storage Redundancy
     - [LRS/GRS/RA-GRS]

Recovery Procedures
~~~~~~~~~~~~~~~~~~

**Point-in-Time Recovery**:

.. code-block:: bash

   # Restore database to specific point in time
   az sql db restore --resource-group [RG_NAME] \
                     --server [SERVER_NAME] \
                     --name [NEW_DB_NAME] \
                     --source-database [SOURCE_DB_NAME] \
                     --time "[RESTORE_TIME]"

**Geo-Restore** (Disaster Recovery):

.. code-block:: bash

   # Restore from geo-redundant backup
   az sql db restore --resource-group [RG_NAME] \
                     --server [DR_SERVER_NAME] \
                     --name [DB_NAME] \
                     --source-database [RESOURCE_ID] \
                     --edition [SERVICE_TIER]

.. warning::
   **Recovery Time Objective (RTO)**: [RTO_HOURS] hours
   **Recovery Point Objective (RPO)**: [RPO_MINUTES] minutes

Monitoring & Alerts
------------------

Performance Metrics
~~~~~~~~~~~~~~~~~~

.. list-table:: Key Performance Indicators
   :header-rows: 1
   :widths: 30 20 50

   * - Metric
     - Threshold
     - Alert Action
   * - DTU/vCore Percentage
     - >80%
     - Page DBA team
   * - CPU Percentage
     - >85%
     - Auto-scale if configured
   * - Database Size
     - >90% of limit
     - Email storage team
   * - Connection Count
     - >80% of limit
     - Investigation required
   * - Blocked Processes
     - >5 concurrent
     - Immediate DBA attention

Log Analytics Queries
~~~~~~~~~~~~~~~~~~~~

**Common Troubleshooting Queries**:

.. code-block:: kusto

   // Database connection failures
   AzureDiagnostics
   | where ResourceProvider == "MICROSOFT.SQL"
   | where Category == "DatabaseWaitStatistics"
   | where TimeGenerated > ago(1h)
   | project TimeGenerated, Resource, wait_type_s, wait_time_ms_d
   | order by TimeGenerated desc

   // Slow queries
   AzureDiagnostics  
   | where ResourceProvider == "MICROSOFT.SQL"
   | where Category == "QueryStoreRuntimeStatistics"
   | where avg_duration_d > 1000  // >1 second
   | project TimeGenerated, Resource, query_hash_s, avg_duration_d
   | order by avg_duration_d desc

Troubleshooting Guide
--------------------

Connection Issues
~~~~~~~~~~~~~~~~

**Symptom**: Application cannot connect to database

**Investigation Checklist**:

1. **Verify Connection String**
   
   .. code-block:: powershell

      # Test connection from application server
      Test-NetConnection -ComputerName [SQL_SERVER_NAME].database.windows.net -Port 1433

2. **Check Authentication**
   
   .. code-block:: sql

      -- Check if user exists and has proper permissions
      SELECT name, type_desc FROM sys.database_principals 
      WHERE name = '[USERNAME]'

3. **Review Firewall Rules**
   
   .. code-block:: bash

      # List current firewall rules
      az sql server firewall-rule list --resource-group [RG] --server [SERVER]

4. **Verify Service Availability**
   
   * Check Azure Status Dashboard
   * Review SQL Database service health in portal

Performance Issues
~~~~~~~~~~~~~~~~~

**Symptom**: Slow query performance or application timeouts

**Investigation Steps**:

1. **Check Resource Utilization**
   
   .. code-block:: sql

      -- Check current resource usage
      SELECT 
          avg_cpu_percent,
          avg_data_io_percent, 
          avg_log_write_percent,
          max_worker_percent,
          max_session_percent
      FROM sys.resource_stats 
      WHERE start_time > DATEADD(hour, -1, GETUTCDATE())
      ORDER BY start_time DESC

2. **Identify Blocking Processes**
   
   .. code-block:: sql

      -- Find blocking processes
      SELECT 
          session_id,
          blocking_session_id,
          wait_type,
          wait_resource,
          command
      FROM sys.dm_exec_requests 
      WHERE blocking_session_id > 0

3. **Review Query Store Data**
   
   .. code-block:: sql

      -- Top resource consuming queries
      SELECT TOP 10
          q.query_id,
          qt.query_sql_text,
          rs.avg_duration/1000.0 as avg_duration_sec,
          rs.avg_cpu_time/1000.0 as avg_cpu_sec
      FROM sys.query_store_query q
      JOIN sys.query_store_query_text qt ON q.query_text_id = qt.query_text_id  
      JOIN sys.query_store_runtime_stats rs ON q.query_id = rs.query_id
      WHERE rs.last_execution_time > DATEADD(hour, -1, GETUTCDATE())
      ORDER BY rs.avg_duration DESC

Storage Issues  
~~~~~~~~~~~~~

**Symptom**: Database approaching storage limits

**Investigation & Resolution**:

1. **Check Database Size**
   
   .. code-block:: sql

      -- Database size analysis
      SELECT 
          DB_NAME() as database_name,
          SUM(CAST(FILEPROPERTY(name, 'SpaceUsed') AS bigint) * 8192.) / 1024 / 1024 as used_mb,
          SUM(size * 8192.) / 1024 / 1024 as allocated_mb
      FROM sys.database_files
      WHERE type IN (0, 1)

2. **Identify Large Tables**
   
   .. code-block:: sql

      -- Table size analysis
      SELECT 
          t.NAME AS table_name,
          s.Name AS schema_name,
          SUM(a.total_pages) * 8 AS total_size_kb,
          SUM(a.used_pages) * 8 AS used_size_kb,
          (SUM(a.total_pages) - SUM(a.used_pages)) * 8 AS unused_size_kb
      FROM sys.tables t
      INNER JOIN sys.indexes i ON t.OBJECT_ID = i.object_id
      INNER JOIN sys.partitions p ON i.object_id = p.OBJECT_ID AND i.index_id = p.index_id
      INNER JOIN sys.allocation_units a ON p.partition_id = a.container_id
      LEFT OUTER JOIN sys.schemas s ON t.schema_id = s.schema_id
      GROUP BY t.Name, s.Name
      ORDER BY SUM(a.total_pages) DESC

Emergency Contacts
------------------

.. list-table:: Database Emergency Contacts
   :header-rows: 1
   :widths: 25 30 25 20

   * - Role
     - Name
     - Email
     - Phone
   * - Primary DBA
     - [DBA_NAME]
     - [DBA_EMAIL]
     - [DBA_PHONE]
   * - Backup DBA
     - [BACKUP_DBA_NAME]
     - [BACKUP_DBA_EMAIL]
     - [BACKUP_DBA_PHONE]
   * - Application Owner
     - [APP_OWNER_NAME]
     - [APP_OWNER_EMAIL]
     - [APP_OWNER_PHONE]
   * - Azure Support
     - Microsoft Support
     - Via Azure Portal
     - [SUPPORT_PLAN_LEVEL]

**Escalation Procedures**:

* **Severity 1** (Database Unavailable): Call Primary DBA + Application Owner immediately
* **Severity 2** (Performance Degradation): Email Primary DBA, escalate after 30 minutes
* **Severity 3** (Maintenance/Questions): Email Primary DBA during business hours

Maintenance & Change Control
---------------------------

**Regular Maintenance Tasks**:

* **Weekly**: Index maintenance and statistics updates (Sundays 2:00-4:00 AM)
* **Monthly**: Security patch review and application (First Saturday 1:00-5:00 AM)  
* **Quarterly**: Capacity planning and performance review

**Change Management**:

* **Schema Changes**: Require DBA approval and testing in development environment
* **Index Changes**: Must be reviewed for performance impact
* **Data Modifications**: Require business owner approval for production data

.. warning::
   **Production Change Freeze**: No changes during month-end processing (last business day of month)

Quick Reference
--------------

**Common Connection Strings**:

.. code-block:: bash

   # PowerShell/C# 
   "Server=[SERVER].database.windows.net;Database=[DB];Authentication=Active Directory Integrated;Encrypt=True;"
   
   # Python (pyodbc)
   "Driver={ODBC Driver 17 for SQL Server};Server=[SERVER].database.windows.net;Database=[DB];Authentication=ActiveDirectoryIntegrated;Encrypt=yes;"
   
   # Java (JDBC)
   "jdbc:sqlserver://[SERVER].database.windows.net:1433;database=[DB];authentication=ActiveDirectoryIntegrated;encrypt=true;"

**Emergency Commands**:

.. code-block:: sql

   -- Kill blocking session (use carefully!)
   KILL [SESSION_ID]
   
   -- Check database status
   SELECT state_desc FROM sys.databases WHERE name = '[DATABASE_NAME]'
   
   -- Check service tier and usage
   SELECT * FROM sys.resource_stats WHERE start_time > DATEADD(hour, -2, GETUTCDATE())

Links & Resources
----------------

* **Azure Portal Database**: [DIRECT_LINK_TO_DATABASE]
* **Query Performance Insight**: [LINK_TO_QPI] 
* **Backup Retention Policy**: [LINK_TO_BACKUP_POLICY]
* **Change Management System**: [LINK_TO_CHANGE_SYSTEM]
* **Database Documentation Repository**: [LINK_TO_DB_DOCS]

---

*Generated by Infrastructure Documentation Standards v0.1.0*
*Template: sql-database-guide.rst*
*Last Updated: [GENERATION_DATE]*
*Next Review: [NEXT_REVIEW_DATE]*