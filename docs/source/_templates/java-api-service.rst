Java API Service Documentation Template
=====================================

.. note::
   **Purpose**: Eliminate "shooting in the dark" at API endpoints by documenting Java web services systematically.
   Generated from standardized templates to ensure comprehensive API documentation across all projects.

Project Overview
---------------

:Client: {{ client_name }}
:Service: {{ service_name }}
:Environment: {{ environment }}
:Base URL: {{ base_url }}
:Service Type: {{ service_type }}
:Last Updated: {{ last_updated }}

.. warning::
   **Service Dependencies**: This documentation covers API endpoints and their expected behavior.
   Test all endpoints in non-production environments first.

API Endpoints
------------

SOAP Web Service
~~~~~~~~~~~~~~~

.. list-table:: Service Configuration
   :header-rows: 1
   :widths: 30 70

   * - Property
     - Value
   * - WSDL URL
     - {{ base_url }}/{{ service_name }}?wsdl
   * - Namespace  
     - {{ namespace }}
   * - Service Name
     - {{ service_name }}
   * - Port
     - {{ port }}

Endpoint Reference
~~~~~~~~~~~~~~~~~

{% for endpoint in endpoints %}
**{{ endpoint.operation_name }}**

.. code-block:: xml

   <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:util="{{ namespace }}">
      <soap:Header/>
      <soap:Body>
         <util:{{ endpoint.operation_name }}>
            {% for param in endpoint.parameters %}
            <util:{{ param.name }}>{{ param.example_value }}</util:{{ param.name }}>
            {% endfor %}
         </util:{{ endpoint.operation_name }}>
      </soap:Body>
   </soap:Envelope>

*Parameters:*

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Parameter
     - Type  
     - Description
   {% for param in endpoint.parameters %}
   * - {{ param.name }}
     - {{ param.type }}
     - {{ param.description | default('TODO: Document parameter usage') }}
   {% endfor %}

*Returns:* {{ endpoint.return_type }}

*Purpose:* {{ endpoint.purpose | default('TODO: Document endpoint purpose') }}

{% endfor %}

Data Models
----------

{% for model in data_models %}
**{{ model.class_name }}**

*Package:* ``{{ model.package }}``

*Purpose:* {{ model.purpose | default('TODO: Document model purpose') }}

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   {% for field in model.fields %}
   * - {{ field.name }}
     - {{ field.type }}
     - {{ field.description | default('TODO: Document field purpose') }}
   {% endfor %}

{% endfor %}

Service Architecture
-------------------

Application Structure
~~~~~~~~~~~~~~~~~~~~

.. graphviz::

   digraph service_architecture {
       rankdir=TB;
       node [shape=rectangle, style=filled];
       
       // Presentation Layer
       endpoint [label="SOAP Endpoints\\n{{ namespace }}", fillcolor=lightblue];
       
       // Service Layer  
       {% for service in services %}
       {{ service.name|lower }} [label="{{ service.name }}\\n{{ service.impl_name }}", fillcolor=lightgreen];
       {% endfor %}
       
       // Repository Layer
       {% for repo in repositories %}  
       {{ repo.name|lower }} [label="{{ repo.name }}", fillcolor=yellow];
       {% endfor %}
       
       // External Systems
       database [label="Database\\n{{ database_name | default('Unknown') }}", fillcolor=pink];
       
       // Connections
       endpoint -> {% for service in services %}{{ service.name|lower }}{% if not loop.last %};
       endpoint -> {% endif %}{% endfor %};
       {% for service in services %}
       {% for repo in service.repositories %}
       {{ service.name|lower }} -> {{ repo|lower }};
       {% endfor %}
       {% endfor %}
       {% for repo in repositories %}
       {{ repo.name|lower }} -> database;
       {% endfor %}
   }

Configuration Files
~~~~~~~~~~~~~~~~~~

.. list-table:: Key Configuration Locations
   :header-rows: 1
   :widths: 40 60

   * - File
     - Purpose
   * - ``application.properties``
     - Server port, context path, JMX settings
   * - ``logback.xml``
     - Logging configuration
   * - ``web.xml`` (if present)
     - Web application deployment descriptor

Environment Variables
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Server Configuration
   SERVER_PORT={{ port | default('8080') }}
   SERVER_CONTEXT_PATH={{ context_path | default('/') }}
   
   # Database Configuration (if applicable)
   DB_URL={{ db_url | default('TODO: Add database URL') }}
   DB_USERNAME={{ db_username | default('TODO: Add database username') }}
   DB_PASSWORD={{ db_password | default('TODO: Add database password') }}
   
   # Logging Configuration
   LOG_LEVEL={{ log_level | default('INFO') }}

.. important::
   **Configuration Management**: All sensitive configuration should be externalized.
   Never hardcode credentials or environment-specific values.

Testing & Usage Examples
-----------------------

Testing Strategy
~~~~~~~~~~~~~~~

.. list-table:: Testing Approaches
   :header-rows: 1
   :widths: 30 70

   * - Test Type
     - Approach
   * - Unit Testing
     - Test service layer methods with mocked dependencies
   * - Integration Testing
     - Test complete endpoint-to-database flow
   * - SOAP Testing
     - Use SoapUI or Postman with WSDL import
   * - Load Testing
     - Test endpoint performance under expected load

SOAP Client Examples
~~~~~~~~~~~~~~~~~~~

**Java Client Example:**

.. code-block:: java

   // Using JAX-WS
   {{ service_name }} service = new {{ service_name }}();
   {{ service_name }}PortType port = service.get{{ service_name }}HttpPort();
   
   // Example call
   {% for endpoint in endpoints[:1] %}
   {{ endpoint.return_type }} result = port.{{ endpoint.operation_name }}({{ endpoint.sample_params }});
   {% endfor %}

**Python Client Example:**

.. code-block:: python

   from zeep import Client
   
   client = Client('{{ base_url }}/{{ service_name }}?wsdl')
   
   # Example call
   {% for endpoint in endpoints[:1] %}
   result = client.service.{{ endpoint.operation_name }}({{ endpoint.python_params }})
   {% endfor %}

**cURL Example:**

.. code-block:: bash

   curl -X POST "{{ base_url }}/{{ service_name }}" \
        -H "Content-Type: text/xml; charset=utf-8" \
        -H "SOAPAction: \"{{ namespace }}/{{ endpoints[0].operation_name }}\"" \
        -d @request.xml

Common Issues & Troubleshooting
------------------------------

Endpoint Issues
~~~~~~~~~~~~~~

**Service Unavailable (503)**

*Symptoms:* Endpoint returns 503 or connection refused

*Investigation Steps:*

1. Check if service is running: ``ps aux | grep java``
2. Verify port is listening: ``netstat -tlnp | grep {{ port }}``
3. Check application logs for startup errors
4. Verify database connectivity (if applicable)

.. code-block:: bash

   # Check service status
   curl -I {{ base_url }}/actuator/health  # If Spring Boot Actuator enabled
   
   # Check WSDL availability
   curl {{ base_url }}/{{ service_name }}?wsdl

**SOAP Fault Responses**

*Symptoms:* Receiving SOAP fault instead of expected response

*Investigation Steps:*

1. Validate request XML against WSDL schema
2. Check parameter data types and required fields
3. Verify namespace declarations in request
4. Review application logs for detailed error messages

.. warning::
   **SOAP Debugging**: Always validate your SOAP requests against the WSDL schema.
   Use tools like SoapUI for request validation and testing.

Performance Issues
~~~~~~~~~~~~~~~~~

**Slow Response Times**

*Symptoms:* Endpoints taking >5 seconds to respond

*Investigation Steps:*

1. Check database query performance (if applicable)
2. Monitor JVM garbage collection
3. Review connection pool configuration
4. Check for deadlocks in application logs

.. code-block:: bash

   # Monitor JVM performance
   jstat -gc [pid] 5s
   
   # Check database connections (if applicable)
   # Application-specific monitoring commands

Data Issues
~~~~~~~~~~

**Invalid Response Format**

*Symptoms:* Unexpected response structure or missing fields

*Investigation Steps:*

1. Verify data model mappings in service layer
2. Check for null handling in response objects
3. Validate database schema matches model expectations
4. Review serialization configuration

Deployment & Maintenance
-----------------------

.. warning::
   **All production changes must follow established change management process.**

**Deployment Checklist:**

* ✅ Service builds successfully with ``./gradlew build``
* ✅ Unit tests pass with ``./gradlew test``
* ✅ Integration tests pass in staging environment
* ✅ WSDL is accessible after deployment
* ✅ Health checks return successful status
* ✅ Database migrations completed (if applicable)
* ✅ Configuration files updated for target environment

**Maintenance Tasks:**

* **Weekly**: Review application logs for errors and warnings
* **Monthly**: Check JVM memory usage and garbage collection performance  
* **Quarterly**: Review endpoint performance metrics and optimize slow queries

Emergency Contacts & Escalation
------------------------------

.. list-table:: Contact Information
   :header-rows: 1
   :widths: 25 35 20 20

   * - Role
     - Name
     - Email
     - Phone
   * - Lead Developer
     - {{ lead_developer | default('TBD') }}
     - {{ lead_email | default('TBD') }}
     - {{ lead_phone | default('TBD') }}
   * - System Administrator
     - {{ sysadmin | default('TBD') }}
     - {{ sysadmin_email | default('TBD') }}
     - {{ sysadmin_phone | default('TBD') }}
   * - Client Technical Contact
     - {{ client_contact | default('TBD') }}
     - {{ client_email | default('TBD') }}
     - {{ client_phone | default('TBD') }}

**Escalation Path:**

1. **Severity 1** (Service Down): Immediate call to Lead Developer + System Administrator
2. **Severity 2** (Performance Issues): Email Lead Developer, escalate after 2 hours  
3. **Severity 3** (Minor Issues): Email Lead Developer during business hours

Links & References
-----------------

* **Service WSDL**: {{ base_url }}/{{ service_name }}?wsdl
* **Source Code**: {{ source_repo | default('TBD') }}
* **Build System**: {{ build_system | default('TBD') }}
* **Monitoring**: {{ monitoring_url | default('TBD') }}
* **Issue Tracking**: {{ issue_tracker | default('TBD') }}

---

.. footer::

   *Document generated using Infrastructure Documentation Standards*
   
   :Template: java-api-service.rst v1.0
   :Generated: {{ generation_date }}
   :Next Review: {{ next_review_date }}
   :Contact: Infrastructure Documentation Team