# MCP Modular Architecture - Stage 2: MCP + Tools

This project implements an MCP-based system as part of an academic software architecture assignment, following a structured multi-stage progression as defined in assignment8.

**Current Stage: Stage 2 - MCP + Tools**

This stage adds MCP server functionality with tool support, building upon the Stage 1 foundation without modifying the core infrastructure.

## Stage Progression (per assignment8)

### Stage 1: Foundation ✅ Completed

Stage 1 established the foundational infrastructure:

1. **Clean Architecture**: Modular, well-organized codebase following OOP principles
2. **Configuration Management**: Centralized, environment-aware configuration system
3. **Logging Infrastructure**: Comprehensive logging with file and console output
4. **Error Handling**: Robust exception hierarchy and error handling mechanisms
5. **Testing Foundation**: Unit testing infrastructure with example test cases
6. **Code Quality**: Short, focused files (max ~150 lines) with clear responsibilities

### Stage 2: MCP + Tools ✅ Current Stage

**Goal**: Build minimal MCP server with Tools support as a modular layer.

Stage 2 adds MCP functionality without modifying Stage 1 infrastructure:

1. **MCP Server Bootstrap**: Minimal server implementation using core infrastructure
2. **Tool Registry**: Centralized tool registration and discovery
3. **Tool Abstraction**: Base class for all tools with JSON schema support
4. **Example Tools**: Calculator and Echo tools demonstrating the architecture
5. **Tool Execution**: Parameter validation and execution pipeline
6. **JSON Schemas**: Schema definition and validation for tool inputs/outputs

**Important**: Stage 2 focuses ONLY on Tools. Resources and Prompts are in Stage 3. Transport layer is in Stage 4.

## Project Structure

```
mcp-modular-architecture/
├── config/                      # Configuration files
│   ├── base.yaml               # Base configuration (now includes MCP config)
│   ├── development.yaml        # Development environment config
│   └── production.yaml         # Production environment config
│
├── src/                        # Source code
│   ├── core/                   # Core infrastructure (Stage 1)
│   │   ├── config/            # Configuration management
│   │   │   └── config_manager.py
│   │   ├── logging/           # Logging system
│   │   │   └── logger.py
│   │   └── errors/            # Error handling
│   │       ├── exceptions.py
│   │       └── error_handler.py
│   │
│   ├── mcp/                    # MCP Layer (Stage 2) **NEW**
│   │   ├── server.py          # MCP server bootstrap
│   │   ├── tool_registry.py   # Tool registry
│   │   ├── tools/             # Tool implementations
│   │   │   ├── base_tool.py   # Abstract base tool
│   │   │   ├── calculator_tool.py
│   │   │   └── echo_tool.py
│   │   └── schemas/           # JSON schema definitions
│   │       └── tool_schemas.py
│   │
│   ├── models/                 # Domain models (Illustrative - Stage 1)
│   │   ├── base_model.py
│   │   └── resource.py
│   │
│   ├── services/               # Service layer (Illustrative - Stage 1)
│   │   └── resource_service.py
│   │
│   └── utils/                  # Utility functions
│       └── validators.py
│
├── tests/                      # Unit tests (mirrors src structure)
│   ├── core/                  # Stage 1 tests
│   │   ├── config/
│   │   └── errors/
│   ├── mcp/                   # Stage 2 tests **NEW**
│   │   ├── test_server.py
│   │   ├── test_tool_registry.py
│   │   └── tools/
│   │       ├── test_calculator_tool.py
│   │       └── test_echo_tool.py
│   ├── models/
│   ├── services/
│   └── utils/
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

## Stage 2: MCP Layer Components

### MCP Server (`src/mcp/server.py`)

- **MCPServer**: Minimal MCP server bootstrap
  - Server initialization and lifecycle management
  - Tool registration interface
  - Tool execution pipeline
  - Uses ConfigManager for server configuration
  - Uses Logger for all server operations
  - Uses ErrorHandler for robust error handling
  - **No hard-coded values** - all configuration from YAML
  - **Stage 2 capabilities**: Tools only (no Resources/Prompts yet)

### Tool Registry (`src/mcp/tool_registry.py`)

- **ToolRegistry**: Centralized tool management
  - Singleton pattern for single source of truth
  - Tool registration and unregistration
  - Tool discovery by name
  - List all available tools
  - Get tool metadata (schemas, descriptions)
  - Integrates with logging and error handling

### Tool Abstraction (`src/mcp/tools/base_tool.py`)

- **BaseTool**: Abstract base class for all tools
  - Defines tool interface contract
  - Automatic parameter validation using JSON schema
  - Execution pipeline with logging and error handling
  - Schema definition requirement
  - Result standardization (success/failure format)
  - All concrete tools must inherit from BaseTool

### JSON Schema Support (`src/mcp/schemas/tool_schemas.py`)

- **ToolSchema**: Tool schema representation
  - JSON schema for input parameters
  - JSON schema for output values
  - Schema validation logic
  - Schema serialization (to_dict)
  - Type checking for parameters

### Example Tools (Illustrative)

**Note**: These tools are placeholder examples demonstrating the architecture.

- **CalculatorTool** (`src/mcp/tools/calculator_tool.py`)
  - Performs basic arithmetic operations (add, subtract, multiply, divide)
  - Demonstrates multi-parameter tools
  - Shows validation (division by zero)
  - Example of tool with enumerated operations

- **EchoTool** (`src/mcp/tools/echo_tool.py`)
  - Simple echo functionality
  - Demonstrates minimal tool implementation
  - Single parameter handling
  - Baseline for understanding tool architecture

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

### Stage 1: Core Infrastructure

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

# Use service (illustrative placeholder)
service = ResourceService()
resource = service.create_resource(
    resource_id='user-123',
    name='Example Resource',
    status='active'
)

logger.info(f"Created resource: {resource.resource_id}")
```

### Stage 2: MCP Server with Tools

```python
from src.mcp.server import MCPServer
from src.mcp.tools.calculator_tool import CalculatorTool
from src.mcp.tools.echo_tool import EchoTool

# Initialize MCP server
server = MCPServer()

# Register tools
calculator = CalculatorTool()
echo = EchoTool()

server.initialize(tools=[calculator, echo])

# Get server info
info = server.get_info()
print(f"Server: {info['name']} v{info['version']}")
print(f"Stage: {info['stage']}")
print(f"Available tools: {server.list_tools()}")

# Execute calculator tool
result = server.execute_tool('calculator', {
    'operation': 'add',
    'a': 10,
    'b': 5
})

if result['success']:
    print(f"Result: {result['result']['result']}")  # Output: 15

# Execute echo tool
result = server.execute_tool('echo', {
    'message': 'Hello from MCP!'
})

if result['success']:
    print(f"Echo: {result['result']['echo']}")

# Get tool metadata
metadata = server.get_tools_metadata()
for tool_meta in metadata:
    print(f"Tool: {tool_meta['name']} - {tool_meta['description']}")

# Shutdown server
server.shutdown()
```

## Architecture Principles

This implementation follows key software architecture principles (as required by assignment8):

1. **Separation of Concerns**: Clear separation between configuration, logging, models, and services
2. **Single Responsibility**: Each class has one well-defined responsibility
3. **Dependency Injection**: Components receive dependencies rather than creating them
4. **DRY (Don't Repeat Yourself)**: Common functionality extracted to base classes and utilities
5. **SOLID Principles**: Especially evident in the base model abstraction and error hierarchy
6. **Configuration Over Code**: All configurable values in YAML files, not hard-coded

## Stage 2 Architectural Highlights

### How Stage 2 Builds on Stage 1

1. **Zero Modification to Core**: Stage 1 infrastructure (`src/core/`) remains untouched
2. **Modular Addition**: MCP layer (`src/mcp/`) is a completely independent module
3. **Seamless Integration**: MCP components consume Stage 1 services (config, logging, errors)
4. **No Hard-coded Values**: All MCP configuration in `config/base.yaml`
5. **Complete Test Coverage**: 39 new tests added (76 tests total, all passing)

### What Stage 2 Does NOT Include (per assignment8)

- **No Resources**: Resource primitives are in Stage 3
- **No Prompts**: Prompt templates are in Stage 3
- **No Transport Layer**: HTTP/SSE/STDIO are in Stage 4
- **No SDK**: SDK abstraction is in Stage 5
- **No UI**: User interface is in Stage 5

## Next Stages (per assignment8)

**Completed:**
- ✅ **Stage 1: Foundation** - Core infrastructure (config, logging, errors, testing)
- ✅ **Stage 2: MCP + Tools** - MCP server with tool registry and example tools

**Remaining:**
- **Stage 3: Tools, Resources, and Prompts** - Add all three MCP primitives
- **Stage 4: Transport / Communication Layer** - Add networking (HTTP/SSE/STDIO)
- **Stage 5: SDK and User Interface** - Client SDK and user-facing interface

Each stage builds upon the previous without breaking existing functionality. The modular architecture enables independent development and testing of each layer.

## License

This project is created for academic purposes as part of a software architecture course.

## Author

Tal Barda
