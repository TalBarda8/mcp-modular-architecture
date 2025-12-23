# MCP Modular Architecture - Stage 1: Foundation

This project implements **Stage 1 (Foundation)** of an MCP-based system as part of an academic software architecture assignment. The focus is on creating a clean, maintainable infrastructure layer with proper architectural principles.

## Stage 1 Goals

Stage 1 establishes the foundational infrastructure without implementing MCP functionality, networking, SDK, or UI components. The goals are:

1. **Clean Architecture**: Modular, well-organized codebase following OOP principles
2. **Configuration Management**: Centralized, environment-aware configuration system
3. **Logging Infrastructure**: Comprehensive logging with file and console output
4. **Error Handling**: Robust exception hierarchy and error handling mechanisms
5. **Testing Foundation**: Unit testing infrastructure with example test cases
6. **Code Quality**: Short, focused files (max ~150 lines) with clear responsibilities

## Project Structure

```
mcp-modular-architecture/
├── config/                      # Configuration files
│   ├── base.yaml               # Base configuration
│   ├── development.yaml        # Development environment config
│   └── production.yaml         # Production environment config
│
├── src/                        # Source code
│   ├── core/                   # Core infrastructure
│   │   ├── config/            # Configuration management
│   │   │   └── config_manager.py
│   │   ├── logging/           # Logging system
│   │   │   └── logger.py
│   │   └── errors/            # Error handling
│   │       ├── exceptions.py
│   │       └── error_handler.py
│   │
│   ├── models/                 # Domain models
│   │   ├── base_model.py
│   │   └── resource.py
│   │
│   ├── services/               # Service layer
│   │   └── resource_service.py
│   │
│   └── utils/                  # Utility functions
│       └── validators.py
│
├── tests/                      # Unit tests (mirrors src structure)
│   ├── core/
│   │   ├── config/
│   │   │   └── test_config_manager.py
│   │   └── errors/
│   │       └── test_exceptions.py
│   ├── models/
│   │   └── test_resource.py
│   ├── services/
│   │   └── test_resource_service.py
│   └── utils/
│       └── test_validators.py
│
├── logs/                       # Application logs (gitignored)
├── .gitignore
├── pytest.ini                  # Pytest configuration
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Important Note: Illustrative Domain Layer

**The domain entities (`Resource`, `ResourceService`, CRUD operations) are illustrative placeholders only.**

These components exist solely to demonstrate how the core architectural infrastructure (configuration, logging, error handling, testing) works in practice. They do **not** represent the final system domain or chosen business logic.

In subsequent stages, when the actual MCP-based domain is defined, these placeholder entities can be completely replaced or removed without any impact on the core infrastructure layer. The architectural foundation (`src/core/`) is domain-agnostic and designed to support any application built on top of it.

## Key Components

### Configuration Layer (`src/core/config/`)

- **ConfigManager**: Singleton configuration manager
  - Loads YAML configuration files
  - Supports environment-specific configs (development, production)
  - Enables local overrides (local.yaml)
  - Provides dot-notation access to nested values
  - **No hard-coded values** in the codebase

### Logging System (`src/core/logging/`)

- **Logger**: Centralized logging mechanism
  - Configurable log levels
  - File rotation (size-based)
  - Console and file output
  - Structured log formatting
  - Configuration-driven setup

### Error Handling (`src/core/errors/`)

- **Custom Exception Hierarchy**:
  - `BaseApplicationError`: Base class for all exceptions
  - `ConfigurationError`: Configuration-related errors
  - `ValidationError`: Data validation failures
  - `ServiceError`: Service operation failures
  - `ResourceNotFoundError`: Missing resource errors
  - `ResourceAlreadyExistsError`: Duplicate resource errors

- **ErrorHandler**: Centralized error handling
  - Logging integration
  - Traceback management
  - Safe execution wrapper

### Domain Models (`src/models/`) - **Illustrative Only**

- **BaseModel**: Abstract base class with common functionality
  - Validation interface
  - Serialization (to_dict)
  - Timestamp management

- **Resource**: Example concrete model (placeholder)
  - Demonstrates validation patterns
  - Shows OOP principles
  - Includes business methods
  - **Can be replaced with actual domain entities in later stages**

### Service Layer (`src/services/`) - **Illustrative Only**

- **ResourceService**: Example service implementation (placeholder)
  - CRUD operations for demonstration
  - Business logic separation pattern
  - Error handling integration
  - Logging integration
  - **Can be replaced with actual MCP services in later stages**

### Utilities (`src/utils/`)

- **Validators**: Common validation helpers
  - String validation
  - ID format validation
  - Range checking
  - Dictionary key validation

## Setup and Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/TalBarda8/mcp-modular-architecture.git
   cd mcp-modular-architecture
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running Tests

Run all unit tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=src --cov-report=html
```

Run specific test file:
```bash
pytest tests/models/test_resource.py
```

## Configuration

Set the environment using the `APP_ENV` environment variable:

```bash
# Development (default)
export APP_ENV=development

# Production
export APP_ENV=production
```

Create a `config/local.yaml` file for local overrides (gitignored):
```yaml
logging:
  level: "DEBUG"
```

## Example Usage

```python
from src.core.config.config_manager import ConfigManager
from src.core.logging.logger import Logger
from src.services.resource_service import ResourceService

# Get configuration
config = ConfigManager()
app_name = config.get('app.name')

# Get logger
logger = Logger.get_logger(__name__)
logger.info("Application started")

# Use service
service = ResourceService()
resource = service.create_resource(
    resource_id='user-123',
    name='Example Resource',
    status='active'
)

logger.info(f"Created resource: {resource.resource_id}")
```

## Architecture Principles

This Stage 1 implementation follows key software architecture principles:

1. **Separation of Concerns**: Clear separation between configuration, logging, models, and services
2. **Single Responsibility**: Each class has one well-defined responsibility
3. **Dependency Injection**: Components receive dependencies rather than creating them
4. **DRY (Don't Repeat Yourself)**: Common functionality extracted to base classes and utilities
5. **SOLID Principles**: Especially evident in the base model abstraction and error hierarchy
6. **Configuration Over Code**: All configurable values in YAML files, not hard-coded

## Next Stages

This is **Stage 1 (Foundation)** of a multi-stage architecture. Future stages will build upon this foundation:

- **Stage 2: MCP + Tools** - Implement MCP protocol and tool capabilities
- **Stage 3: Tools, Resources, and Prompts** - Extend with resources and prompts
- **Stage 4: Transport / Communication Layer** - Implement networking and transport mechanisms
- **Stage 5: SDK and User Interface** - Develop SDK and user-facing interface components

The core infrastructure established in Stage 1 (configuration, logging, error handling, testing) will remain unchanged and support all subsequent stages.

## License

This project is created for academic purposes as part of a software architecture course.

## Author

Tal Barda
