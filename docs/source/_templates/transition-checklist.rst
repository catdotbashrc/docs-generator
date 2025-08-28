Transition Documentation Checklist
==================================

.. note::
   This template provides a standardized checklist for client project handoffs.
   Use this to ensure all critical information is available for maintenance and troubleshooting.

Client Information
-----------------

:Client Name: [CLIENT_NAME]
:Project Name: [PROJECT_NAME]
:Environment Type: [Azure/GCP/Hybrid]
:Handoff Date: [DATE]
:Primary Contact: [CONTACT_INFO]
:Emergency Escalation: [24/7_CONTACT]

Documentation Status
-------------------

.. raw:: html

   <style>
   .checklist-status { font-weight: bold; }
   .status-complete { color: #28a745; }
   .status-partial { color: #ffc107; }
   .status-missing { color: #dc3545; }
   .status-unknown { color: #6c757d; }
   </style>

Legend:
  * ✅ **Complete**: Information available and up-to-date
  * ⚠️ **Partial**: Information exists but incomplete/outdated  
  * ❌ **Missing**: Critical gap requiring immediate attention
  * 🔍 **Unknown**: Need to investigate/discover

Security & Access
----------------

.. list-table::
   :header-rows: 1
   :widths: 40 15 45

   * - Documentation Item
     - Status
     - Notes/Location
   * - Azure AD/Entra ID Configurations
     - [ ]
     - Service principals, app registrations
   * - Key Vault Inventory & Access Policies
     - [ ]
     - Secret names, access patterns, rotation schedule
   * - Resource Group Permissions (RBAC)
     - [ ]
     - Who has what access, service accounts
   * - Network Security Groups & Firewall Rules
     - [ ]
     - Inbound/outbound rules, exceptions
   * - Database Authentication Methods
     - [ ]
     - SQL Auth vs Azure AD, connection strings location

**Critical Security Questions:**
  * Who has production access and why?
  * Where are secrets stored and how are they rotated?
  * What compliance requirements apply (HIPAA, SOX, etc.)?

Networking & Connectivity
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 15 45

   * - Documentation Item
     - Status
     - Notes/Location
   * - Virtual Network Configuration
     - [ ]
     - VNet address spaces, subnets, peering
   * - Private Endpoints & Service Endpoints
     - [ ]
     - Which services, DNS configurations
   * - DNS Configurations & Custom Domains
     - [ ]
     - Public DNS, private DNS zones
   * - Load Balancer & Application Gateway
     - [ ]
     - Health probes, backend pools, SSL certs
   * - ExpressRoute/VPN Connections
     - [ ]
     - Circuit details, BGP configurations

**Critical Network Questions:**
  * How does traffic flow between components?
  * What are the backup connectivity options?
  * Are there firewall change procedures?

Data & Database
--------------

.. list-table::
   :header-rows: 1
   :widths: 40 15 45

   * - Documentation Item
     - Status
     - Notes/Location
   * - SQL Server Connection Strings
     - [ ]
     - Dev/Staging/Prod environments
   * - Database Schemas & Data Dictionary
     - [ ]
     - Table relationships, business rules
   * - Backup & Recovery Procedures
     - [ ]
     - Schedule, retention, tested restore process
   * - Performance Monitoring & Indexing
     - [ ]
     - Query performance, optimization strategy
   * - Data Classification & Compliance
     - [ ]
     - PII locations, retention policies

**Critical Data Questions:**
  * What happens if the database goes down?
  * Where is sensitive data and how is it protected?
  * Who approves schema changes?

Applications & Services  
----------------------

.. list-table::
   :header-rows: 1
   :widths: 40 15 45

   * - Documentation Item
     - Status
     - Notes/Location
   * - Azure App Services Configuration
     - [ ]
     - Deployment slots, scaling rules
   * - Environment Variables & App Settings
     - [ ]
     - All environments, sensitive vs non-sensitive
   * - API Documentation & Endpoints
     - [ ]
     - Swagger/OpenAPI, rate limits, auth
   * - Monitoring & Logging (App Insights)
     - [ ]
     - Alerts, dashboards, log retention
   * - CI/CD Pipeline Documentation
     - [ ]
     - Deployment process, rollback procedures

**Critical Application Questions:**
  * How do you deploy changes safely?
  * What monitoring alerts exist and who responds?
  * Where are application logs stored and searched?

Gap Assessment Summary
---------------------

.. code-block:: text

   CRITICAL GAPS (❌): [COUNT]
   - [List items that will block troubleshooting]

   PARTIAL DOCUMENTATION (⚠️): [COUNT]  
   - [List items needing completion]

   INVESTIGATION NEEDED (🔍): [COUNT]
   - [List items requiring discovery]

Next Steps
----------

1. **Immediate Actions**: Address critical gaps that block handoff
2. **Investigation Plan**: Schedule discovery sessions for unknown items
3. **Documentation Updates**: Complete partial items within [TIMEFRAME]
4. **Handoff Meeting**: Schedule technical walkthrough with [TEAM_MEMBERS]

.. warning::
   **HANDOFF CRITERIA**: All ❌ Critical items must be resolved before accepting project responsibility.

Contact Information
------------------

:Development Team Lead: [NAME] - [EMAIL] - [PHONE]
:Infrastructure Contact: [NAME] - [EMAIL] - [PHONE]
:Database Administrator: [NAME] - [EMAIL] - [PHONE]
:Security Contact: [NAME] - [EMAIL] - [PHONE]
:Business Stakeholder: [NAME] - [EMAIL] - [PHONE]

---

*Generated by Infrastructure Documentation Standards v0.1.0*
*Template: transition-checklist.rst*
*Date: [GENERATION_DATE]*