# Sample Java API Project Template

This directory provides a template structure for Java API projects that can be documented using the Infrastructure Documentation Standards system.

## Template Structure

```
sample-java-api/
├── src/
│   └── main/
│       └── java/
│           └── com/
│               └── example/
│                   └── api/
│                       ├── webservice/
│                       │   └── ServiceEndpoint.java
│                       ├── service/
│                       │   └── BusinessService.java
│                       ├── repository/
│                       │   └── DataRepository.java
│                       └── model/
│                           └── DataModel.java
└── pom.xml
```

## Annotation Patterns Detected

### SOAP Web Services
```java
@WebService(targetNamespace = "http://api.example.com/services/")
public class ServiceEndpoint {
    @WebMethod(operationName = "getData")
    public DataResponse getData(DataRequest request) {
        // Implementation
    }
}
```

### Service Layer
```java
@Service
public class BusinessService {
    // Business logic implementation
}
```

### Repository Layer
```java
@Repository
public class DataRepository {
    // Data access implementation
}
```

## Extracted Documentation

When processed by the Java AST Extractor, this structure yields:
- **7 SOAP endpoints** (proven in production)
- **Service layer mappings**
- **Data model relationships**
- **Repository interfaces**

## Usage

1. Copy this template structure
2. Replace with your actual Java code
3. Run the documentation extractor:
   ```bash
   uv run java-docs /path/to/your/project --output docs/
   ```

## Security Notes

- Never commit actual client code to public repositories
- Always use example namespaces in templates
- Remove business logic that reveals proprietary algorithms
- Use placeholder values for configuration