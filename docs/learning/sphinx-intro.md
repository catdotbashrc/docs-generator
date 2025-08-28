# Comprehensive Sphinx Guide for Infrastructure Documentation

## Table of Contents

1. [What is Sphinx?](#what-is-sphinx)
2. [Why Sphinx for Infrastructure Documentation?](#why-sphinx-for-infrastructure-documentation)
3. [Installation & Getting Started](#installation--getting-started)
4. [Core Features for Infrastructure Teams](#core-features-for-infrastructure-teams)
5. [Template System](#template-system)
6. [Automation Capabilities](#automation-capabilities)
7. [Infrastructure-Specific Implementation](#infrastructure-specific-implementation)
8. [Cross-Project References](#cross-project-references)
9. [Advanced Customizations](#advanced-customizations)
10. [CI/CD Integration](#cicd-integration)
11. [Best Practices](#best-practices)

## What is Sphinx?

Sphinx is a documentation generation system originally created for Python projects
but now used across the tech industry for technical documentation.
It excels at creating comprehensive, cross-referenced, automatically-updated documentation from multiple sources.

### Key Characteristics

- **Source format**: RestructuredText (RST) or Markdown
- **Output formats**: HTML, PDF, EPUB, LaTeX, man pages
- **Extensible**: Rich ecosystem of extensions and custom directive support
- **Automation-focused**: Generate documentation from code, APIs, databases, infrastructure
- **Cross-referencing**: Link between related documentation automatically

## Why Sphinx for Infrastructure Documentation?

### Infrastructure Documentation Challenges

Infrastructure and data engineering teams face unique documentation requirements:
- **Multiple interconnected systems** (databases, APIs, cloud resources, pipelines)
- **Configuration complexity** (network settings, security policies, resource dependencies)
- **Rapid change cycles** (infrastructure as code updates, schema changes)
- **Cross-team dependencies** (shared resources, external APIs, compliance requirements)

### Sphinx Advantages for Infrastructure

#### Automation from Infrastructure Sources

- Auto-generate Azure/GCP resource inventories from CLI tools
- Extract database schemas from SQL system tables
- Parse Data Factory pipelines from JSON exports
- Generate network diagrams from cloud resource metadata

#### Visual Documentation

- Built-in Graphviz support for network diagrams and data flow charts
- Inheritance diagrams for system dependencies
- Custom diagram generation from infrastructure data

#### Cross-System Intelligence

- Link related infrastructure components automatically
- Track dependencies between databases, APIs, and cloud resources
- Unified search across all infrastructure documentation
- **Saves our team a ton of time and effort in the long run**
- Consistent and standardized product across projects
- Could even eventually be the Resultant standard

#### Version Control Integration

- Documentation lives with infrastructure code
- Track changes to systems and their documentation together
- Automated updates via CI/CD pipelines
- Every second we invest up front, is ten seconds saved in the future


## Installation & Getting Started

### Basic Installation

Currently working on this as a UV project for portability


### Build Documentation

```bash
# Build HTML documentation
make html
# or
sphinx-build -M html source build

# View results
open build/html/index.html
```

## Core Features for Infrastructure Teams

### 1. Auto-Documentation (autodoc/autosummary)

Generate documentation automatically from Python scripts:

```rst
API Documentation
=================

.. autosummary::
   :toctree: generated

   deployment_scripts.azure_setup
   monitoring.log_analyzer
   database.schema_manager
```

### 2. Network Diagrams (Graphviz)

Create infrastructure diagrams directly in documentation:

```rst
Network Architecture
====================

.. graphviz::
   :caption: Production Network Layout

   digraph network {
       rankdir=LR;
       
       internet [label="Internet", shape=cloud];
       firewall [label="Azure Firewall", shape=box];
       vnet [label="Production VNet\n10.0.0.0/16", shape=ellipse];
       subnet1 [label="Web Subnet\n10.0.1.0/24"];
       subnet2 [label="Database Subnet\n10.0.2.0/24"];
       
       internet -> firewall;
       firewall -> vnet;
       vnet -> subnet1;
       vnet -> subnet2;
   }
```

### 3. Cross-References

Link related systems and components:

```rst
Database Configuration
======================

This database is used by :doc:`data-factory/etl-pipeline` and 
monitored by :ref:`monitoring-setup`.

See also: :doc:`../networking/database-security` for security configuration.
```

### 4. Include External Files

Include configuration files and scripts directly:

```rst
Server Configuration
====================

Current production configuration:

.. literalinclude:: ../configs/production.json
   :language: json
   :linenos:

Deployment script:

.. literalinclude:: ../scripts/deploy.py
   :language: python
   :lines: 1-20
```

## Template System

### Master Template Structure

Create reusable templates for different project types:

```
infrastructure-docs-template/
├── source/
│   ├── _templates/
│   │   ├── infrastructure-project.rst
│   │   ├── data-pipeline-project.rst
│   │   └── database-project.rst
│   ├── _extensions/
│   │   ├── azure_inventory.py
│   │   ├── sql_schema.py
│   │   └── adf_pipeline.py
│   └── conf.py
└── scripts/
    ├── setup_new_project.py
    └── generate_docs.py
```

### Infrastructure Project Template

```jinja2
{{ project_name | escape | underline}}

Project Overview
================

:Type: {{ project_type }}
:Environment: {{ environment }}
:Owner: {{ owner }}
:Last Updated: {{ last_updated }}

System Architecture
===================

.. graphviz::
   :caption: {{ project_name }} Architecture

   {{ architecture_diagram }}

{% if azure_resources %}
Azure Resources
===============

.. azure-inventory:: {{ resource_group }}
{% endif %}

{% if databases %}
Database Documentation
======================

{% for db in databases %}
.. sql-schema:: {{ db.connection_string }}
   :database: {{ db.name }}
{% endfor %}
{% endif %}

{% if data_factory_pipelines %}
Data Factory Pipelines
======================

.. adf-pipeline-docs:: {{ data_factory_name }}
{% endif %}

Monitoring & Troubleshooting
=============================

**Key Metrics**: {{ monitoring_dashboard_url }}

**Log Locations**:
{% for log in log_locations %}
- {{ log.name }}: {{ log.location }}
{% endfor %}

**Common Issues**:
{% for issue in common_issues %}
- **{{ issue.title }}**: {{ issue.solution }}
{% endfor %}

Emergency Contacts
==================

{% for contact in emergency_contacts %}
- **{{ contact.role }}**: {{ contact.name }} ({{ contact.email }})
{% endfor %}
```

## Automation Capabilities

### Custom Azure Resource Extension

```python
# _extensions/azure_inventory.py
from sphinx.util.docutils import SphinxDirective
from docutils import nodes
import subprocess
import json

class AzureInventoryDirective(SphinxDirective):
    required_arguments = 1  # Resource group name
    option_spec = {
        'type': lambda x: x,  # Resource type filter
        'location': lambda x: x,  # Location filter
    }
    
    def run(self):
        resource_group = self.arguments[0]
        
        # Build Azure CLI command
        cmd = [
            "az", "resource", "list",
            "--resource-group", resource_group,
            "--output", "json"
        ]
        
        # Add filters if specified
        if 'type' in self.options:
            cmd.extend(["--resource-type", self.options['type']])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            resources = json.loads(result.stdout)
            
            # Generate table
            table = nodes.table()
            tgroup = nodes.tgroup(cols=4)
            table += tgroup
            
            # Add column specs
            for width in [25, 25, 25, 25]:
                tgroup += nodes.colspec(colwidth=width)
            
            # Add header
            thead = nodes.thead()
            tgroup += thead
            header_row = nodes.row()
            thead += header_row
            
            for header in ['Name', 'Type', 'Location', 'Status']:
                entry = nodes.entry()
                entry += nodes.paragraph(text=header)
                header_row += entry
            
            # Add body
            tbody = nodes.tbody()
            tgroup += tbody
            
            for resource in resources:
                row = nodes.row()
                tbody += row
                
                for value in [resource.get('name', ''), 
                             resource.get('type', '').split('/')[-1],
                             resource.get('location', ''),
                             'Active']:  # Could query actual status
                    entry = nodes.entry()
                    entry += nodes.paragraph(text=value)
                    row += entry
            
            return [table]
            
        except subprocess.CalledProcessError as e:
            error = nodes.error()
            error += nodes.paragraph(text=f"Failed to query Azure resources: {e.stderr}")
            return [error]

def setup(app):
    app.add_directive('azure-inventory', AzureInventoryDirective)
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
```

### SQL Schema Documentation Extension

```python
# _extensions/sql_schema.py
from sphinx.util.docutils import SphinxDirective
from docutils import nodes
import pyodbc
import json

class SQLSchemaDirective(SphinxDirective):
    required_arguments = 1  # Connection string or database name
    option_spec = {
        'tables': lambda x: x.split(','),  # Specific tables to document
        'exclude': lambda x: x.split(','), # Tables to exclude
    }
    
    def run(self):
        connection_string = self.arguments[0]
        
        try:
            # Connect and query schema
            conn = pyodbc.connect(connection_string)
            cursor = conn.cursor()
            
            # Get table information
            schema_query = """
            SELECT 
                t.TABLE_NAME,
                c.COLUMN_NAME,
                c.DATA_TYPE,
                c.IS_NULLABLE,
                c.COLUMN_DEFAULT
            FROM INFORMATION_SCHEMA.TABLES t
            JOIN INFORMATION_SCHEMA.COLUMNS c ON t.TABLE_NAME = c.TABLE_NAME
            WHERE t.TABLE_TYPE = 'BASE TABLE'
            ORDER BY t.TABLE_NAME, c.ORDINAL_POSITION
            """
            
            cursor.execute(schema_query)
            results = cursor.fetchall()
            
            # Organize by table
            tables = {}
            for row in results:
                table_name = row.TABLE_NAME
                if table_name not in tables:
                    tables[table_name] = []
                
                tables[table_name].append({
                    'column': row.COLUMN_NAME,
                    'type': row.DATA_TYPE,
                    'nullable': row.IS_NULLABLE,
                    'default': row.COLUMN_DEFAULT
                })
            
            # Filter tables if specified
            if 'tables' in self.options:
                tables = {k: v for k, v in tables.items() 
                         if k in self.options['tables']}
            
            if 'exclude' in self.options:
                tables = {k: v for k, v in tables.items() 
                         if k not in self.options['exclude']}
            
            # Generate documentation nodes
            result_nodes = []
            
            for table_name, columns in tables.items():
                # Table section
                section = nodes.section()
                section += nodes.title(text=table_name)
                
                # Column table
                table_node = self._create_column_table(columns)
                section += table_node
                
                result_nodes.append(section)
            
            return result_nodes
            
        except Exception as e:
            error = nodes.error()
            error += nodes.paragraph(text=f"Database connection failed: {str(e)}")
            return [error]
    
    def _create_column_table(self, columns):
        # Create table with column information
        table = nodes.table()
        tgroup = nodes.tgroup(cols=4)
        table += tgroup
        
        # Column specifications
        for width in [25, 20, 15, 40]:
            tgroup += nodes.colspec(colwidth=width)
        
        # Header
        thead = nodes.thead()
        tgroup += thead
        header_row = nodes.row()
        thead += header_row
        
        for header in ['Column', 'Type', 'Nullable', 'Default']:
            entry = nodes.entry()
            entry += nodes.paragraph(text=header)
            header_row += entry
        
        # Body
        tbody = nodes.tbody()
        tgroup += tbody
        
        for column in columns:
            row = nodes.row()
            tbody += row
            
            for value in [column['column'], column['type'], 
                         column['nullable'], str(column['default'] or '')]:
                entry = nodes.entry()
                entry += nodes.paragraph(text=value)
                row += entry
        
        return table

def setup(app):
    app.add_directive('sql-schema', SQLSchemaDirective)
    return {
        'version': '0.1',
        'parallel_read_safe': False,  # Database connections not thread-safe
        'parallel_write_safe': True,
    }
```

### Data Factory Pipeline Documentation

```python
# _extensions/adf_pipeline.py
from sphinx.util.docutils import SphinxDirective
from docutils import nodes
import json
import requests

class ADFPipelineDirective(SphinxDirective):
    required_arguments = 1  # Data Factory name
    option_spec = {
        'subscription': lambda x: x,
        'resource-group': lambda x: x,
        'pipeline': lambda x: x,  # Specific pipeline name
    }
    
    def run(self):
        data_factory_name = self.arguments[0]
        
        try:
            # Use Azure REST API or az cli to get pipeline info
            pipelines = self._get_pipeline_info(data_factory_name)
            
            result_nodes = []
            
            for pipeline in pipelines:
                # Pipeline section
                section = nodes.section()
                section += nodes.title(text=f"Pipeline: {pipeline['name']}")
                
                # Description
                if pipeline.get('description'):
                    desc = nodes.paragraph()
                    desc += nodes.Text(pipeline['description'])
                    section += desc
                
                # Pipeline flow diagram
                if pipeline.get('activities'):
                    diagram = self._generate_pipeline_diagram(pipeline['activities'])
                    section += diagram
                
                # Activities table
                activities_table = self._create_activities_table(pipeline['activities'])
                section += activities_table
                
                result_nodes.append(section)
            
            return result_nodes
            
        except Exception as e:
            error = nodes.error()
            error += nodes.paragraph(text=f"Failed to retrieve ADF pipelines: {str(e)}")
            return [error]
    
    def _get_pipeline_info(self, data_factory_name):
        # Implement Azure API calls or az cli execution
        # This would use Azure SDK or subprocess calls to az cli
        return []  # Placeholder
    
    def _generate_pipeline_diagram(self, activities):
        # Generate Graphviz diagram from pipeline activities
        graphviz_code = "digraph pipeline {\n"
        graphviz_code += "  rankdir=LR;\n"
        
        for i, activity in enumerate(activities):
            graphviz_code += f'  {activity["name"]} [label="{activity["name"]}\\n({activity["type"]})"];\n'
            if i > 0:
                graphviz_code += f'  {activities[i-1]["name"]} -> {activity["name"]};\n'
        
        graphviz_code += "}"
        
        # Return graphviz node
        graphviz_node = nodes.raw('', f'.. graphviz::\n\n{graphviz_code}', format='rst')
        return graphviz_node
    
    def _create_activities_table(self, activities):
        # Create table documenting each activity
        # Implementation similar to other table creation methods
        return nodes.paragraph(text="Activities table here")

def setup(app):
    app.add_directive('adf-pipeline-docs', ADFPipelineDirective)
    return {
        'version': '0.1',
        'parallel_read_safe': False,
        'parallel_write_safe': True,
    }
```

## Infrastructure-Specific Implementation

### Project Structure for Infrastructure Documentation

```
project-alpha-infrastructure/
├── source/
│   ├── conf.py
│   ├── index.rst
│   ├── infrastructure/
│   │   ├── azure-resources.rst      # Auto-generated
│   │   ├── networking.rst           # Network topology
│   │   ├── security.rst             # Security policies
│   │   └── cost-management.rst      # Resource costs
│   ├── data-engineering/
│   │   ├── data-factory.rst         # ADF pipelines
│   │   ├── databases.rst            # SQL Server schemas
│   │   ├── external-apis.rst        # API documentation
│   │   └── data-lineage.rst         # Data flow mapping
│   ├── operations/
│   │   ├── monitoring.rst           # Dashboards & alerts
│   │   ├── backup-recovery.rst      # Backup procedures
│   │   ├── troubleshooting.rst      # Known issues
│   │   └── runbooks.rst             # Operational procedures
│   └── _templates/
│       └── infrastructure/
│           ├── base.rst
│           ├── azure-project.rst
│           └── gcp-project.rst
└── automation/
    ├── generate_azure_docs.py
    ├── update_sql_schemas.py
    └── deploy_to_itglue.py
```

### Azure Resources Documentation

```rst
# azure-resources.rst
Azure Infrastructure
====================

Resource Groups
---------------

.. azure-inventory:: prod-rg-eastus2
   :type: Microsoft.Compute/virtualMachines

.. azure-inventory:: prod-rg-eastus2
   :type: Microsoft.Storage/storageAccounts

Network Configuration
--------------------

.. graphviz::
   :caption: Network Topology

   digraph network {
       compound=true;
       
       subgraph cluster_vnet {
           label="Production VNet (10.0.0.0/16)";
           
           subgraph cluster_web {
               label="Web Subnet (10.0.1.0/24)";
               vm1 [label="Web Server 1"];
               vm2 [label="Web Server 2"];
           }
           
           subgraph cluster_data {
               label="Data Subnet (10.0.2.0/24)";
               sql1 [label="SQL Server"];
               storage1 [label="Storage Account"];
           }
       }
       
       internet [shape=cloud, label="Internet"];
       gateway [label="VPN Gateway"];
       
       internet -> gateway [ltail=cluster_vnet];
       vm1 -> sql1;
       vm2 -> sql1;
   }

Security Configuration
----------------------

**Network Security Groups**:

.. azure-nsg:: web-nsg
.. azure-nsg:: data-nsg

**Key Vault Secrets**:

.. azure-keyvault:: prod-kv-secrets
   :show-names-only:
```

### Database Documentation

```rst
# databases.rst
Database Documentation
======================

Production SQL Server
--------------------

.. sql-schema:: production-connection
   :tables: users,orders,products,inventory
   :exclude: temp_tables,log_tables

**Connection Details**:
- Server: prod-sql-01.database.windows.net
- Authentication: Azure AD Managed Identity
- Backup Schedule: Daily at 2 AM UTC

Data Dictionary
---------------

.. sql-data-dictionary:: production-connection
   :include-relationships: true
   :include-constraints: true

Performance Monitoring
---------------------

**Key Metrics Dashboard**: `Azure Monitor Dashboard <https://portal.azure.com/...>`_

**Alert Thresholds**:
- CPU > 80% for 5 minutes
- Connections > 90% of max
- Blocking processes > 10 seconds

Maintenance Windows
------------------

- **Weekly Index Maintenance**: Sundays 3-4 AM UTC
- **Monthly Statistics Update**: First Sunday 2-3 AM UTC
- **Quarterly Full Backup**: See :doc:`../operations/backup-recovery`
```

## Cross-Project References

### Intersphinx Configuration

Link between separate project documentation:

```python
# conf.py - Enable cross-project linking
extensions = [
    'sphinx.ext.intersphinx',
]

# Map external documentation
intersphinx_mapping = {
    'shared-infrastructure': ('https://itglue.company.com/docs/shared-infra', None),
    'data-platform': ('https://itglue.company.com/docs/data-platform', None),
    'security-policies': ('https://itglue.company.com/docs/security', None),
}
```

### Cross-Reference Examples

```rst
Network Configuration
====================

This project uses the shared network infrastructure documented in 
:external:doc:`shared-infrastructure:networking/production-vnet`.

Database connections follow security policies defined in 
:external:ref:`security-policies:database-access-controls`.

For troubleshooting database connectivity issues, see 
:external:doc:`data-platform:troubleshooting/sql-connection-issues`.
```


## CI/CD Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/docs.yml
name: Build and Deploy Documentation

on:
  push:
    branches: [main]
    paths: ['docs/**', 'infrastructure/**']
  
jobs:
  build-docs:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install sphinx furo
        pip install -r docs/requirements.txt
    
    - name: Setup Azure CLI
      uses: azure/CLI@v1
      with:
        azcliversion: latest
    
    - name: Login to Azure
      uses: azure/login@v1
      with:
        creds: ${{ secrets.AZURE_CREDENTIALS }}
    
    - name: Generate infrastructure documentation
      run: |
        cd docs
        python automation/generate_azure_docs.py
        python automation/update_sql_schemas.py
    
    - name: Build documentation
      run: |
        cd docs
        make html
    
    - name: Deploy to IT Glue
      run: |
        cd docs
        python automation/deploy_to_itglue.py
      env:
        ITGLUE_API_KEY: ${{ secrets.ITGLUE_API_KEY }}
```

### Azure DevOps Pipeline

```yaml
# azure-pipelines-docs.yml
trigger:
  branches:
    include:
    - main
  paths:
    include:
    - docs/*
    - infrastructure/*

pool:
  vmImage: 'ubuntu-latest'

variables:
  pythonVersion: '3.11'

steps:
- task: UsePythonVersion@0
  inputs:
    versionSpec: '$(pythonVersion)'
  displayName: 'Use Python $(pythonVersion)'

- script: |
    pip install sphinx furo
    pip install -r docs/requirements.txt
  displayName: 'Install Sphinx dependencies'

- task: AzureCLI@2
  inputs:
    azureSubscription: 'infrastructure-docs-service-connection'
    scriptType: 'bash'
    scriptLocation: 'inlineScript'
    inlineScript: |
      cd docs
      python automation/generate_azure_docs.py
      python automation/update_sql_schemas.py
  displayName: 'Generate infrastructure documentation'

- script: |
    cd docs
    make html
  displayName: 'Build Sphinx documentation'

- task: PublishBuildArtifacts@1
  inputs:
    PathtoPublish: 'docs/build/html'
    ArtifactName: 'documentation'
  displayName: 'Publish documentation artifacts'

- script: |
    cd docs
    python automation/deploy_to_itglue.py
  env:
    ITGLUE_API_KEY: $(ITGLUE_API_KEY)
  displayName: 'Deploy to IT Glue'
```

## Best Practices

### 1. Template Development

**Infrastructure Project Template (conf.py)**:
```python
import sys
from pathlib import Path

# Add custom extensions
sys.path.append(str(Path('_extensions').resolve()))

project = '{{ project_name }}'
author = 'Infrastructure Team'

extensions = [
    'sphinx.ext.graphviz',
    'sphinx.ext.intersphinx',
    'azure_inventory',
    'sql_schema',
    'adf_pipeline',
    'infrastructure_summary',
]

# Cross-project linking
intersphinx_mapping = {
    'shared-infra': ('https://itglue.company.com/docs/shared-infrastructure', None),
    'security-standards': ('https://itglue.company.com/docs/security', None),
}

# Theme configuration
html_theme = 'furo'
html_title = f'{project} Infrastructure Documentation'

# Custom template variables for infrastructure projects
html_context = {
    'project_type': '{{ project_type }}',
    'environment': '{{ environment }}',
    'last_updated': '{{ last_updated }}',
}
```

### 2. Automation Scripts

**Azure Documentation Generator**:
```python
# automation/generate_azure_docs.py
import subprocess
import json
import sys
from pathlib import Path

def generate_resource_inventory():
    """Generate Azure resource documentation"""
    
    # Get all resource groups
    cmd = ["az", "group", "list", "--output", "json"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error getting resource groups: {result.stderr}")
        return
    
    resource_groups = json.loads(result.stdout)
    
    # Generate documentation for each resource group
    for rg in resource_groups:
        rg_name = rg['name']
        
        # Create RST file for this resource group
        rst_content = f"""
{rg_name} Resources
{'=' * (len(rg_name) + 10)}

.. azure-inventory:: {rg_name}

Network Resources
-----------------

.. azure-inventory:: {rg_name}
   :type: Microsoft.Network/*

Compute Resources  
-----------------

.. azure-inventory:: {rg_name}
   :type: Microsoft.Compute/*

Storage Resources
-----------------

.. azure-inventory:: {rg_name}
   :type: Microsoft.Storage/*
"""
        
        # Write to appropriate location
        output_path = Path(f"source/infrastructure/{rg_name.lower()}-resources.rst")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            f.write(rst_content)
        
        print(f"Generated documentation for {rg_name}")

if __name__ == "__main__":
    generate_resource_inventory()
```

### 3. Template Usage

**Creating New Project Documentation**:
```bash
# setup_new_project.py
#!/usr/bin/env python3

import shutil
import sys
from pathlib import Path
from datetime import datetime

def setup_new_project(project_name, project_type, environment):
    """Set up new project documentation from template"""
    
    template_dir = Path("infrastructure-docs-template")
    project_dir = Path(f"{project_name}-infrastructure-docs")
    
    # Copy template
    shutil.copytree(template_dir, project_dir)
    
    # Customize configuration
    conf_path = project_dir / "source" / "conf.py"
    
    # Read template and substitute variables
    with open(conf_path, 'r') as f:
        conf_content = f.read()
    
    replacements = {
        '{{ project_name }}': project_name,
        '{{ project_type }}': project_type,
        '{{ environment }}': environment,
        '{{ last_updated }}': datetime.now().isoformat(),
    }
    
    for placeholder, value in replacements.items():
        conf_content = conf_content.replace(placeholder, value)
    
    with open(conf_path, 'w') as f:
        f.write(conf_content)
    
    print(f"Created {project_name} documentation project")
    print(f"Next steps:")
    print(f"  cd {project_dir}")
    print(f"  python -m venv .venv")
    print(f"  source .venv/bin/activate")
    print(f"  pip install -r requirements.txt")
    print(f"  make html")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: setup_new_project.py <project_name> <project_type> <environment>")
        print("Example: setup_new_project.py alpha-data-platform data-engineering production")
        sys.exit(1)
    
    setup_new_project(sys.argv[1], sys.argv[2], sys.argv[3])
```

### 4. Documentation Standards Compliance

**Pre-commit Hook for Documentation Requirements**:
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Check for required documentation files
required_files=(
    "source/index.rst"
    "source/infrastructure/azure-resources.rst"
    "source/operations/monitoring.rst"
    "source/operations/emergency-contacts.rst"
)

missing_files=()
for file in "${required_files[@]}"; do
    if [[ ! -f "$file" ]]; then
        missing_files+=("$file")
    fi
done

if [[ ${#missing_files[@]} -gt 0 ]]; then
    echo "Error: Required documentation files are missing:"
    printf '  %s\n' "${missing_files[@]}"
    echo ""
    echo "Please create these files before committing."
    echo "Use the documentation templates in _templates/infrastructure/"
    exit 1
fi

# Build documentation to check for errors
cd docs
if ! make html > /dev/null 2>&1; then
    echo "Error: Documentation build failed"
    echo "Run 'cd docs && make html' to see detailed errors"
    exit 1
fi

echo "Documentation requirements satisfied"
```

### 5. IT Glue Integration

**Automated Upload Script**:
```python
# automation/deploy_to_itglue.py
import requests
import os
import zipfile
from pathlib import Path

class ITGlueUploader:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    def upload_documentation(self, project_name, html_dir):
        """Upload Sphinx HTML documentation to IT Glue"""
        
        # Create zip file of HTML documentation
        zip_path = Path(f"{project_name}-docs.zip")
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in Path(html_dir).rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(html_dir)
                    zipf.write(file_path, arcname)
        
        # Upload to IT Glue
        # (Implementation depends on IT Glue API)
        print(f"Uploading {zip_path} to IT Glue...")
        
        # Create or update IT Glue entry
        self._create_itglue_entry(project_name, zip_path)
        
        # Clean up
        zip_path.unlink()
    
    def _create_itglue_entry(self, project_name, zip_path):
        """Create or update IT Glue configuration entry"""
        
        entry_data = {
            'name': f"{project_name} Infrastructure Documentation",
            'notes': f"Auto-generated Sphinx documentation for {project_name}",
            'configuration_type': 'Infrastructure Documentation',
        }
        
        # Upload zip as attachment
        # (IT Glue API implementation)
        print(f"Created IT Glue entry for {project_name}")

if __name__ == "__main__":
    uploader = ITGlueUploader(
        api_key=os.environ['ITGLUE_API_KEY'],
        base_url=os.environ.get('ITGLUE_BASE_URL', 'https://api.itglue.com')
    )
    
    project_name = sys.argv[1] if len(sys.argv) > 1 else 'infrastructure-project'
    html_dir = Path('build/html')
    
    uploader.upload_documentation(project_name, html_dir)
```

## Quick Start for Your Team

### 1. Set Up Master Template

```bash
# Clone or create master template repository
git clone <your-template-repo> infrastructure-docs-template
cd infrastructure-docs-template

# Set up Python environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install sphinx furo pyodbc pyyaml azure-cli
pip freeze > requirements.txt
```

### 2. Create Your First Project

```bash
# Use setup script
python scripts/setup_new_project.py \
    "alpha-data-platform" \
    "data-engineering" \
    "production"

cd alpha-data-platform-infrastructure-docs
source .venv/bin/activate
pip install -r requirements.txt

# Build documentation
make html
open build/html/index.html
```

### 3. Customize for Your Infrastructure

Edit the generated project files:
- `source/infrastructure/azure-resources.rst` - Add your Azure resource groups
- `source/data-engineering/databases.rst` - Add your SQL Server connections  
- `source/operations/monitoring.rst` - Link to your Azure Monitor dashboards

### 4. Automate Updates

Set up CI/CD pipeline to automatically update documentation when infrastructure changes.

## Implementation Timeline

**Week 1-2: Foundation**
- Install Sphinx and create master template
- Develop basic Azure resource inventory extension
- Create first project documentation as proof of concept

**Week 3-4: Core Extensions**
- Build SQL schema documentation automation
- Create Data Factory pipeline documentation extension  
- Implement graphviz network diagram generation

**Week 5-6: Integration & Polish**
- Set up CI/CD automation
- Create IT Glue upload scripts
- Establish cross-project referencing

**Week 7-8: Team Rollout**
- Train team on template usage
- Document best practices and workflows
- Establish ongoing maintenance processes

## Success Metrics

- **Documentation Coverage**: 80% of operational requirements documented automatically
- **Setup Time**: New project documentation created in under 2 hours
- **Update Frequency**: Infrastructure changes reflected in documentation within 24 hours
- **Cross-References**: Related systems properly linked and discoverable
- **Team Adoption**: 90% of new projects use standardized templates

Sphinx provides the perfect foundation for achieving these goals through its powerful automation capabilities, template system, and extensive customization options.
