#!/usr/bin/env python3
"""Test JavaASTExtractor with actual DSNY project files."""

from automation.filesystem.local import LocalFileSystem
from automation.java_ast_extractor import JavaASTExtractor
import json

def main():
    # Initialize with local filesystem
    fs = LocalFileSystem()
    extractor = JavaASTExtractor(fs)
    
    # Path to the DSNY UtilizationEndpoint.java
    dsny_endpoint_path = "docs/source/examples/dsny_/reports-utilization/src/main/java/gov/nyc/dsny/reports/utilization/webservice/UtilizationEndpoint.java"
    
    print("🔍 Testing JavaASTExtractor with DSNY UtilizationEndpoint...")
    print(f"📁 File: {dsny_endpoint_path}")
    print("=" * 60)
    
    try:
        # Extract documentation from the real DSNY file
        result = extractor.extract_documentation(dsny_endpoint_path)
        
        print("📊 EXTRACTION RESULTS:")
        print(f"   Language: {result['language']}")
        print(f"   Endpoints: {len(result['endpoints'])}")
        print(f"   Services: {len(result['services'])}")  
        print(f"   Models: {len(result['models'])}")
        print()
        
        # Show detailed endpoint information
        if result['endpoints']:
            print("🔗 SOAP ENDPOINTS:")
            for i, endpoint in enumerate(result['endpoints'], 1):
                print(f"   {i}. {endpoint['operation']}")
                print(f"      Method: {endpoint['method_name']}")
                print(f"      Return Type: {endpoint['return_type']}")
                print(f"      Parameters: {len(endpoint['parameters'])}")
                for param in endpoint['parameters']:
                    print(f"         - {param['name']}: {param['type']}")
                print()
        
        # Show service information  
        if result['services']:
            print("⚙️ SERVICES:")
            for i, service in enumerate(result['services'], 1):
                print(f"   {i}. {service['name']} ({service['type']})")
                print(f"      Namespace: {service.get('namespace', 'N/A')}")
                print(f"      Methods: {len(service.get('methods', []))}")
                print()
        
        # Show models
        if result['models']:
            print("📋 DATA MODELS:")
            for i, model in enumerate(result['models'], 1):
                print(f"   {i}. {model['name']} ({model['type']})")
                if model['type'] == 'class':
                    print(f"      Fields: {len(model.get('fields', []))}")
                elif model['type'] == 'enum':
                    print(f"      Values: {len(model.get('values', []))}")
                print()
        
        print("✅ SUCCESS: JavaASTExtractor successfully processed DSNY project!")
        print(f"📈 Discovered: {len(result['endpoints'])} endpoints, {len(result['services'])} services, {len(result['models'])} models")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())