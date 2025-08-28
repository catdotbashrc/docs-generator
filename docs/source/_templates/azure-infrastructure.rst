[PROJECT_NAME] - Azure Infrastructure Documentation
=================================================

.. note::
   This document provides comprehensive infrastructure documentation for maintenance and troubleshooting.
   Generated from standardized templates to ensure consistency across all client projects.

Project Overview
---------------

:Client: [CLIENT_NAME]
:Project: [PROJECT_NAME]
:Environment: [ENVIRONMENT] (Development/Staging/Production)
:Azure Subscription: [SUBSCRIPTION_NAME] ([SUBSCRIPTION_ID])
:Resource Groups: [PRIMARY_RG], [SECONDARY_RG]
:Region(s): [PRIMARY_REGION], [BACKUP_REGION]
:Last Updated: [UPDATE_DATE]

.. warning::
   **Production Environment**: This documentation covers production infrastructure.
   All changes must follow established change management procedures.

Architecture Overview
--------------------

.. graphviz::

   digraph infrastructure {
       rankdir=TB;
       node [shape=rectangle, style=filled];
       
       // User Layer
       users [label="End Users", fillcolor=lightblue];
       
       // Network Layer  
       appgw [label="Application Gateway\n[APP_GW_NAME]", fillcolor=lightgreen];
       vnet [label="Virtual Network\n[VNET_NAME]\n[VNET_ADDRESS_SPACE]", fillcolor=lightgreen];
       
       // Application Layer
       webapp [label="Web App\n[WEBAPP_NAME]", fillcolor=orange];
       api [label="API App\n[API_NAME]", fillcolor=orange];
       
       // Data Layer
       sqldb [label="SQL Database\n[DATABASE_NAME]", fillcolor=yellow];
       storage [label="Storage Account\n[STORAGE_NAME]", fillcolor=yellow];
       
       // Monitoring
       appinsights [label="Application Insights\n[AI_NAME]", fillcolor=pink];
       
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
   * - [SP_NAME_1]
     - [APP_ID_1]
     - [PURPOSE_1]
   * - [SP_NAME_2]
     - [APP_ID_2]
     - [PURPOSE_2]

Key Vault Configuration
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   Key Vault: [KEY_VAULT_NAME]
   Resource Group: [KV_RESOURCE_GROUP]
   Location: [KV_LOCATION]
   
   Access Policies:
   - Principal: [PRINCIPAL_NAME]
     Permissions: 
       Secrets: [get, list]
       Keys: [get, decrypt, encrypt]
   
   Critical Secrets:
   - database-connection-string
   - api-key-external-service
   - ssl-certificate-password

.. warning::
   **Secret Rotation**: Database connection strings rotate every 90 days.
   API keys for external services rotate every 180 days.

Resource-Based Access Control (RBAC)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Production Resource Group Permissions
   :header-rows: 1
   :widths: 40 30 30

   * - Principal
     - Role
     - Scope
   * - [TEAM_NAME]
     - Contributor
     - [PRIMARY_RESOURCE_GROUP]
   * - [SERVICE_PRINCIPAL]
     - Reader
     - [DATABASE_RESOURCE]
   * - [MONITORING_SP]
     - Monitoring Reader
     - Entire Subscription

Network Configuration
--------------------

Virtual Network Details
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Virtual Network: [VNET_NAME]
   Address Space: [VNET_CIDR]
   DNS Servers: [DNS_SERVER_1], [DNS_SERVER_2]
   
   Subnets:
   - [SUBNET_1_NAME]: [SUBNET_1_CIDR] (Web Tier)
   - [SUBNET_2_NAME]: [SUBNET_2_CIDR] (Application Tier)  
   - [SUBNET_3_NAME]: [SUBNET_3_CIDR] (Database Tier)
   - [SUBNET_4_NAME]: [SUBNET_4_CIDR] (Management)

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
   * - [NSG_WEB]
     - Inbound
     - 443
     - Internet
     - HTTPS Traffic
   * - [NSG_APP]
     - Inbound
     - 8080
     - [WEB_SUBNET]
     - API Communication
   * - [NSG_DB]
     - Inbound
     - 1433
     - [APP_SUBNET]
     - Database Access

.. caution::
   **Firewall Change Process**: All NSG changes require approval from Security Team.
   Emergency changes must be documented within 24 hours.

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
     - [PLAN_NAME] ([PLAN_SKU])
     - Auto-scaling enabled
   * - Runtime Stack
     - [RUNTIME] [VERSION]
     - Keep updated per security policy
   * - Deployment Slots
     - staging, production
     - Blue-green deployment strategy
   * - Custom Domains
     - [DOMAIN_1], [DOMAIN_2]
     - SSL certificates in Key Vault

Environment Variables & App Settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Application Configuration
   ENVIRONMENT=[ENV_NAME]
   LOG_LEVEL=[LOG_LEVEL]
   
   # Database Connection (from Key Vault)
   DATABASE_CONNECTION_STRING=@Microsoft.KeyVault(SecretUri=[SECRET_URI])
   
   # External Service Configuration
   EXTERNAL_API_ENDPOINT=[API_ENDPOINT]
   EXTERNAL_API_KEY=@Microsoft.KeyVault(SecretUri=[API_KEY_URI])
   
   # Application Insights
   APPINSIGHTS_INSTRUMENTATIONKEY=[AI_KEY]
   APPINSIGHTS_CONNECTION_STRING=[AI_CONNECTION_STRING]

.. important::
   **Configuration Changes**: Environment variable changes require application restart.
   Coordinate changes during maintenance windows.

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
     - [SQL_SERVER_NAME].database.windows.net
   * - Database Name
     - [DATABASE_NAME]
   * - Service Tier
     - [SERVICE_TIER] ([DTU/vCores])
   * - Collation
     - [COLLATION]
   * - Backup Retention
     - [BACKUP_DAYS] days
   * - Geo-Replication
     - [ENABLED/DISABLED] - [SECONDARY_REGION]

Connection Strings
~~~~~~~~~~~~~~~~~

.. code-block:: text

   Production (Azure AD):
   Server=[SERVER_NAME];Database=[DB_NAME];Authentication=Active Directory Integrated;

   Development (SQL Auth):
   Server=[SERVER_NAME];Database=[DB_NAME];User ID=[USERNAME];Password=[FROM_KEY_VAULT];

.. warning::
   **Never store passwords in plain text**. All connection strings with passwords
   must reference Key Vault secrets.

Database Schema Overview
~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Critical Tables
   :header-rows: 1
   :widths: 25 25 50

   * - Table Name
     - Purpose
     - Dependencies
   * - [TABLE_1]
     - [PURPOSE_1]
     - [RELATED_TABLES]
   * - [TABLE_2] 
     - [PURPOSE_2]
     - [RELATED_TABLES]

Monitoring & Observability
-------------------------

Application Insights Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   Application Insights: [AI_NAME]
   Instrumentation Key: [AI_KEY]
   
   Key Metrics Tracked:
   - Request Response Time
   - Request Success Rate  
   - Database Query Performance
   - Custom Business Metrics
   
   Alerts Configured:
   - High Response Time (>2s)
   - Error Rate >5%
   - Database Connection Failures

Log Analytics Workspace
~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Log Sources
   :header-rows: 1
   :widths: 30 40 30

   * - Source
     - Log Type
     - Retention
   * - Web Apps
     - Application Logs
     - 90 days
   * - SQL Database
     - Query Performance
     - 30 days
   * - Network Security Groups
     - Flow Logs
     - 30 days

.. note::
   **Log Search**: Use Kusto Query Language (KQL) in Log Analytics.
   Common queries are saved in the [SHARED_QUERIES] folder.

Troubleshooting Guides
---------------------

Common Issues & Solutions
~~~~~~~~~~~~~~~~~~~~~~~~

Database Connection Timeouts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Symptoms**: Applications report database connection failures or timeouts.

**Investigation Steps**:

1. Check Application Insights for database dependency failures
2. Verify SQL Database DTU/CPU usage in Azure portal
3. Check if connection pooling is configured correctly
4. Verify network connectivity from app to database

.. code-block:: bash

   # Check database performance
   az sql db show-usage --name [DATABASE_NAME] --resource-group [RG_NAME] --server [SERVER_NAME]

**Resolution**: Scale up database tier if resource constrained, or optimize queries.

High Application Response Times  
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Symptoms**: Users report slow application performance.

**Investigation Steps**:

1. Check Application Insights performance blade
2. Review database query performance 
3. Check App Service Plan CPU/Memory usage
4. Verify CDN and caching configuration

.. code-block:: bash

   # Check app service metrics
   az webapp log deployment list --name [WEBAPP_NAME] --resource-group [RG_NAME]

SSL Certificate Renewal
^^^^^^^^^^^^^^^^^^^^^^

**Symptoms**: Certificate expiration warnings or HTTPS errors.

**Investigation Steps**:

1. Check certificate expiration date in Key Vault
2. Verify certificate binding in App Service
3. Update DNS records if using custom domains

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
     - [NAME]
     - [EMAIL]
     - [PHONE]
   * - Database Administrator
     - [NAME]
     - [EMAIL]
     - [PHONE]
   * - Security Contact
     - [NAME]
     - [EMAIL]
     - [PHONE]
   * - Business Owner
     - [NAME]
     - [EMAIL]
     - [PHONE]

**Escalation Path**:

1. **Severity 1** (Production Down): Immediate call to Primary Engineer + Business Owner
2. **Severity 2** (Degraded Performance): Email Primary Engineer, phone if no response in 30 min
3. **Severity 3** (Minor Issues): Email Primary Engineer during business hours

Change Management
----------------

.. warning::
   **All production changes must follow the established change management process.**

**Change Categories**:

* **Emergency**: Production outage, security vulnerability
* **Standard**: Pre-approved changes with documented procedures  
* **Normal**: All other changes requiring CAB approval

**Maintenance Windows**:

* **Weekly**: Sundays 2:00-6:00 AM [TIMEZONE] for standard changes
* **Monthly**: First Saturday 1:00-5:00 AM [TIMEZONE] for major updates

Links & References
-----------------

* **Azure Portal**: https://portal.azure.com
* **Application Insights**: [DIRECT_LINK_TO_AI]
* **Log Analytics**: [DIRECT_LINK_TO_LA]  
* **Key Vault**: [DIRECT_LINK_TO_KV]
* **Resource Group**: [DIRECT_LINK_TO_RG]
* **Change Management System**: [LINK_TO_CHANGE_SYSTEM]
* **Runbook Repository**: [LINK_TO_RUNBOOKS]

---

.. footer::

   *Document generated using Infrastructure Documentation Standards*
   
   :Template: azure-infrastructure.rst v1.0
   :Generated: [GENERATION_DATE]  
   :Next Review: [NEXT_REVIEW_DATE]
   :Contact: Infrastructure Documentation Team