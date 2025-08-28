#!/usr/bin/env python3
"""
Project Setup Automation

Creates new infrastructure documentation projects from standardized templates.
Handles client-specific customization and gap assessment initialization.
"""

import os
import sys
import shutil
import argparse
import logging
from pathlib import Path
from datetime import datetime
import yaml

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_project_root():
    """Get the project root directory."""
    return Path(__file__).parent.parent

class ProjectSetup:
    """Handles creation of new infrastructure documentation projects."""
    
    def __init__(self):
        self.project_root = get_project_root()
        self.templates_dir = self.project_root / "docs" / "source" / "_templates"
        
    def get_available_templates(self):
        """Get list of available documentation templates."""
        if not self.templates_dir.exists():
            logger.error(f"Templates directory not found: {self.templates_dir}")
            return []
        
        templates = []
        for template_file in self.templates_dir.glob("*.rst"):
            template_name = template_file.stem
            templates.append(template_name)
        
        return sorted(templates)
    
    def collect_project_info(self, args):
        """Collect project information for template customization."""
        project_info = {}
        
        # Basic project information
        project_info['client_name'] = args.client or input("Client Name: ")
        project_info['project_name'] = args.project or input("Project Name: ")
        project_info['environment'] = args.environment or self._prompt_choice(
            "Environment Type", ["Development", "Staging", "Production"], "Production"
        )
        
        # Azure-specific information
        if args.template in ['azure-infrastructure', 'transition-checklist']:
            project_info.update(self._collect_azure_info(args))
        
        # Database-specific information  
        if args.template in ['sql-database-guide', 'transition-checklist']:
            project_info.update(self._collect_database_info(args))
        
        # Contact information
        project_info.update(self._collect_contact_info(args))
        
        return project_info
    
    def _collect_azure_info(self, args):
        """Collect Azure-specific configuration information."""
        azure_info = {}
        
        azure_info['subscription_name'] = args.subscription or input("Azure Subscription Name: ")
        azure_info['subscription_id'] = input("Azure Subscription ID (optional): ") or "[SUBSCRIPTION_ID]"
        azure_info['resource_group'] = args.resource_group or input("Primary Resource Group: ") or "[PRIMARY_RG]"
        azure_info['region'] = args.region or input("Primary Azure Region: ") or "[PRIMARY_REGION]"
        
        # Optional secondary region for DR
        secondary_region = input("Secondary Region (DR) [optional]: ")
        azure_info['secondary_region'] = secondary_region or "[BACKUP_REGION]"
        
        return azure_info
    
    def _collect_database_info(self, args):
        """Collect database-specific configuration information."""
        db_info = {}
        
        db_info['sql_server_name'] = args.sql_server or input("SQL Server Name: ") or "[SQL_SERVER_NAME]"
        db_info['database_name'] = args.database or input("Database Name: ") or "[DATABASE_NAME]"
        db_info['service_tier'] = input("Service Tier (e.g., Standard S2): ") or "[SERVICE_TIER]"
        
        return db_info
    
    def _collect_contact_info(self, args):
        """Collect emergency contact and escalation information."""
        contact_info = {}
        
        print("\\nContact Information:")
        contact_info['primary_engineer_name'] = input("Primary Engineer Name: ") or "[NAME]"
        contact_info['primary_engineer_email'] = input("Primary Engineer Email: ") or "[EMAIL]"
        contact_info['primary_engineer_phone'] = input("Primary Engineer Phone: ") or "[PHONE]"
        
        contact_info['dba_name'] = input("Database Administrator Name [optional]: ") or "[NAME]"
        contact_info['dba_email'] = input("Database Administrator Email [optional]: ") or "[EMAIL]"
        
        return contact_info
    
    def _prompt_choice(self, prompt, choices, default=None):
        """Prompt user to select from a list of choices."""
        print(f"\\n{prompt}:")
        for i, choice in enumerate(choices, 1):
            marker = " (default)" if choice == default else ""
            print(f"  {i}. {choice}{marker}")
        
        while True:
            try:
                selection = input("Select option [1-{}]: ".format(len(choices)))
                if not selection and default:
                    return default
                
                index = int(selection) - 1
                if 0 <= index < len(choices):
                    return choices[index]
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Please enter a number.")
    
    def customize_template(self, template_path, output_path, project_info):
        """Customize template with project-specific information."""
        logger.info(f"Customizing template: {template_path}")
        
        # Read template content
        with open(template_path, 'r') as f:
            content = f.read()
        
        # Replace placeholders
        replacements = {
            '[CLIENT_NAME]': project_info.get('client_name', '[CLIENT_NAME]'),
            '[PROJECT_NAME]': project_info.get('project_name', '[PROJECT_NAME]'),
            '[ENVIRONMENT]': project_info.get('environment', '[ENVIRONMENT]'),
            '[DATE]': datetime.now().strftime('%Y-%m-%d'),
            '[GENERATION_DATE]': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '[NEXT_REVIEW_DATE]': (datetime.now().replace(month=datetime.now().month+3) if datetime.now().month <= 9 
                                  else datetime.now().replace(year=datetime.now().year+1, month=datetime.now().month-9)).strftime('%Y-%m-%d'),
            
            # Azure-specific replacements
            '[SUBSCRIPTION_NAME]': project_info.get('subscription_name', '[SUBSCRIPTION_NAME]'),
            '[SUBSCRIPTION_ID]': project_info.get('subscription_id', '[SUBSCRIPTION_ID]'),
            '[PRIMARY_RG]': project_info.get('resource_group', '[PRIMARY_RG]'),
            '[PRIMARY_REGION]': project_info.get('region', '[PRIMARY_REGION]'),
            '[BACKUP_REGION]': project_info.get('secondary_region', '[BACKUP_REGION]'),
            
            # Database-specific replacements
            '[SQL_SERVER_NAME]': project_info.get('sql_server_name', '[SQL_SERVER_NAME]'),
            '[DATABASE_NAME]': project_info.get('database_name', '[DATABASE_NAME]'),
            '[SERVICE_TIER]': project_info.get('service_tier', '[SERVICE_TIER]'),
            
            # Contact information
            '[PRIMARY_ENGINEER_NAME]': project_info.get('primary_engineer_name', '[NAME]'),
            '[PRIMARY_ENGINEER_EMAIL]': project_info.get('primary_engineer_email', '[EMAIL]'),
            '[PRIMARY_ENGINEER_PHONE]': project_info.get('primary_engineer_phone', '[PHONE]'),
            '[DBA_NAME]': project_info.get('dba_name', '[NAME]'),
            '[DBA_EMAIL]': project_info.get('dba_email', '[EMAIL]'),
        }
        
        # Apply replacements
        for placeholder, value in replacements.items():
            content = content.replace(placeholder, value)
        
        # Write customized content
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(content)
        
        logger.info(f"Generated customized documentation: {output_path}")
    
    def create_project_structure(self, project_info, template_name):
        """Create directory structure for the new project."""
        client_name = project_info['client_name'].lower().replace(' ', '-')
        project_name = project_info['project_name'].lower().replace(' ', '-')
        
        project_dir = self.project_root / "docs" / "source" / "projects" / client_name / project_name
        project_dir.mkdir(parents=True, exist_ok=True)
        
        # Create standard subdirectories
        subdirs = ['infrastructure', 'databases', 'applications', 'monitoring', 'troubleshooting']
        for subdir in subdirs:
            (project_dir / subdir).mkdir(exist_ok=True)
        
        logger.info(f"Created project structure: {project_dir}")
        return project_dir
    
    def generate_project_index(self, project_dir, project_info, template_name):
        """Generate a project-specific index file."""
        index_content = f'''
{project_info['project_name']} - Infrastructure Documentation
{'=' * (len(project_info['project_name']) + 34)}

.. note::
   Infrastructure documentation for **{project_info['client_name']}** - **{project_info['project_name']}**
   
   :Environment: {project_info['environment']}
   :Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
   :Template: {template_name}

Project Overview
---------------

This documentation provides comprehensive infrastructure information for maintenance and troubleshooting.

**Critical Information**:

* All configuration details required for system maintenance
* Emergency contact information and escalation procedures  
* Troubleshooting guides for common issues
* Gap assessment checklist to identify missing documentation

Documentation Sections
---------------------

.. toctree::
   :maxdepth: 2
   
   main-documentation
   infrastructure/index
   databases/index
   applications/index
   monitoring/index
   troubleshooting/index

Quick Access
-----------

**Emergency Contacts**: See :ref:`emergency-contacts` section
**Connection Strings**: See :ref:`database-connections` section
**Troubleshooting**: See :ref:`common-issues` section

Gap Assessment
-------------

.. include:: gap-assessment.rst

---

*Generated by Infrastructure Documentation Standards v0.1.0*
*Template: {template_name}*
*Client: {project_info['client_name']}*
'''
        
        index_file = project_dir / "index.rst"
        with open(index_file, 'w') as f:
            f.write(index_content)
        
        logger.info(f"Generated project index: {index_file}")
    
    def create_gap_assessment(self, project_dir):
        """Create a gap assessment checklist for the project."""
        gap_content = '''Gap Assessment Checklist
========================

.. note::
   Use this checklist to identify missing critical documentation.
   Mark each item as Complete (✅), Partial (⚠️), Missing (❌), or Unknown (🔍).

Security & Access
----------------

.. list-table::
   :header-rows: 1
   :widths: 50 15 35

   * - Item
     - Status  
     - Notes
   * - Azure AD/Service Principal Documentation
     - [ ]
     - 
   * - Key Vault Secret Inventory
     - [ ]
     - 
   * - RBAC Permission Matrix
     - [ ]
     - 
   * - Network Security Rules
     - [ ]
     - 
   * - Database Access Configuration
     - [ ]
     - 

Networking & Connectivity
------------------------

.. list-table::
   :header-rows: 1
   :widths: 50 15 35

   * - Item
     - Status
     - Notes
   * - Virtual Network Configuration
     - [ ]
     - 
   * - DNS Configuration
     - [ ]
     - 
   * - Load Balancer Settings
     - [ ]
     - 
   * - Firewall Rules Documentation
     - [ ]
     - 

Data & Databases
---------------

.. list-table::
   :header-rows: 1
   :widths: 50 15 35

   * - Item
     - Status
     - Notes
   * - Database Connection Strings
     - [ ]
     - 
   * - Schema Documentation
     - [ ]
     - 
   * - Backup Procedures
     - [ ]
     - 
   * - Performance Baselines
     - [ ]
     - 

Applications & Services
----------------------

.. list-table::
   :header-rows: 1
   :widths: 50 15 35

   * - Item
     - Status
     - Notes
   * - Application Configuration
     - [ ]
     - 
   * - Environment Variables
     - [ ]
     - 
   * - API Documentation
     - [ ]
     - 
   * - Monitoring Configuration
     - [ ]
     - 
   * - Deployment Procedures
     - [ ]
     - 

Summary
-------

**Critical Gaps (❌)**: [COUNT]

**Items Needing Completion (⚠️)**: [COUNT]

**Investigation Required (🔍)**: [COUNT]

**Action Items**:

1. [List critical gaps that must be addressed before handoff]
2. [List investigation tasks]
3. [List completion tasks]
'''
        
        gap_file = project_dir / "gap-assessment.rst"
        with open(gap_file, 'w') as f:
            f.write(gap_content)
        
        logger.info(f"Created gap assessment: {gap_file}")
    
    def setup_new_project(self, args):
        """Set up a new infrastructure documentation project."""
        # Check if template exists
        template_path = self.templates_dir / f"{args.template}.rst"
        if not template_path.exists():
            logger.error(f"Template not found: {args.template}")
            available = self.get_available_templates()
            logger.info(f"Available templates: {', '.join(available)}")
            return False
        
        # Collect project information
        logger.info(f"Setting up new project using template: {args.template}")
        project_info = self.collect_project_info(args)
        
        # Create project structure
        project_dir = self.create_project_structure(project_info, args.template)
        
        # Customize main template
        main_doc_path = project_dir / "main-documentation.rst"
        self.customize_template(template_path, main_doc_path, project_info)
        
        # Generate project index
        self.generate_project_index(project_dir, project_info, args.template)
        
        # Create gap assessment
        self.create_gap_assessment(project_dir)
        
        # Create project metadata file
        metadata = {
            'client': project_info['client_name'],
            'project': project_info['project_name'], 
            'template': args.template,
            'created': datetime.now().isoformat(),
            'project_info': project_info
        }
        
        metadata_file = project_dir / "project-metadata.yaml"
        with open(metadata_file, 'w') as f:
            yaml.dump(metadata, f, default_flow_style=False)
        
        logger.info("Project setup completed successfully!")
        logger.info(f"Project location: {project_dir}")
        logger.info(f"Next steps:")
        logger.info(f"  1. Review and complete gap assessment: {project_dir}/gap-assessment.rst")
        logger.info(f"  2. Customize main documentation: {project_dir}/main-documentation.rst")
        logger.info(f"  3. Build documentation: docs-build")
        
        return True

def main():
    """Main entry point for project setup."""
    setup = ProjectSetup()
    available_templates = setup.get_available_templates()
    
    parser = argparse.ArgumentParser(description='Setup new infrastructure documentation project')
    parser.add_argument('--template', choices=available_templates, required=True,
                        help='Documentation template to use')
    parser.add_argument('--client', help='Client name')
    parser.add_argument('--project', help='Project name')
    parser.add_argument('--environment', choices=['Development', 'Staging', 'Production'],
                        help='Environment type')
    
    # Azure-specific options
    parser.add_argument('--subscription', help='Azure subscription name')
    parser.add_argument('--resource-group', help='Primary Azure resource group')
    parser.add_argument('--region', help='Primary Azure region')
    
    # Database-specific options
    parser.add_argument('--sql-server', help='SQL Server name')
    parser.add_argument('--database', help='Database name')
    
    args = parser.parse_args()
    
    if not available_templates:
        logger.error("No templates found. Please check your installation.")
        sys.exit(1)
    
    if setup.setup_new_project(args):
        logger.info("Project setup completed successfully")
    else:
        logger.error("Project setup failed")
        sys.exit(1)

if __name__ == "__main__":
    main()