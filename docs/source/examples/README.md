# Example Projects

This directory contains sanitized example projects that demonstrate the Infrastructure Documentation Standards system in action.

## Important Note on Proprietary Code

**⚠️ SECURITY NOTICE**: Actual client code and proprietary examples are excluded from this public repository. The examples shown here are anonymized templates that demonstrate the documentation extraction patterns without exposing client-specific implementations.

## Available Examples

### 1. Sample Java API Project
- **Location**: `sample-java-api/` (template structure only)
- **Purpose**: Demonstrates Java API documentation extraction
- **Features**:
  - SOAP endpoint discovery
  - Service layer documentation
  - Data model extraction
  - Repository pattern detection

### 2. Reports Utilization API Documentation
- **File**: `reports-utilization-api-docs.rst`
- **Purpose**: Example of generated API documentation
- **Content**: Shows the output format for discovered endpoints

## How to Use These Examples

1. **As Templates**: Use these structures as templates for your own projects
2. **For Testing**: Create test fixtures based on these patterns
3. **For Learning**: Understand how the extraction system works

## Creating Your Own Examples

When adding new examples, ensure you:
1. Remove all client-specific namespaces and identifiers
2. Replace real URLs with `example.com` domains
3. Use generic package names like `com.example`
4. Strip out any business logic that reveals proprietary algorithms
5. Keep only the structural patterns that demonstrate the documentation system

## Excluded Content

The following directories are intentionally excluded from version control:
- `dsny_/` - Contains proprietary DSNY code
- Any directory matching pattern `*client*/`
- Files containing connection strings or credentials

## Documentation Extraction Patterns

The system successfully extracts:
- **SOAP Endpoints**: `@WebService` and `@WebMethod` annotations
- **REST APIs**: `@RestController` and mapping annotations
- **Service Layers**: `@Service` annotated classes
- **Data Models**: Domain objects and DTOs
- **Repositories**: Data access patterns

For more information on the extraction patterns, see the main project documentation.