# MCP Modular Architecture - Stage 4: Transport / Communication Layer

This project implements an MCP-based system as part of an academic software architecture assignment, following a structured multi-stage progression as defined in assignment8.

**Current Stage: Stage 4 - Transport / Communication Layer**

This stage adds a modular transport layer that enables communication with the MCP server while keeping the MCP core completely transport-agnostic.

## Stage Progression (per assignment8)

### Stage 1: Foundation ✅ Completed

Stage 1 established the foundational infrastructure:

1. **Clean Architecture**: Modular, well-organized codebase following OOP principles
2. **Configuration Management**: Centralized, environment-aware configuration system
3. **Logging Infrastructure**: Comprehensive logging with file and console output
4. **Error Handling**: Robust exception hierarchy and error handling mechanisms
5. **Testing Foundation**: Unit testing infrastructure with example test cases
6. **Code Quality**: Short, focused files (max ~150 lines) with clear responsibilities

### Stage 2: MCP + Tools ✅ Completed

**Goal**: Build minimal MCP server with Tools support as a modular layer.

Stage 2 adds MCP functionality without modifying Stage 1 infrastructure:

1. **MCP Server Bootstrap**: Minimal server implementation using core infrastructure
2. **Tool Registry**: Centralized tool registration and discovery
3. **Tool Abstraction**: Base class for all tools with JSON schema support
4. **Example Tools**: Calculator and Echo tools demonstrating the architecture
5. **Tool Execution**: Parameter validation and execution pipeline
6. **JSON Schemas**: Schema definition and validation for tool inputs/outputs

### Stage 3: Tools, Resources, and Prompts ✅ Completed

**Goal**: Extend MCP server to support all three MCP primitives.

Stage 3 adds Resources and Prompts while keeping Tools unchanged:

1. **Resource Abstraction**: Base class for all resources with static/dynamic support
2. **Resource Registry**: Centralized resource registration and discovery
3. **Example Resources**: ConfigResource (static) and StatusResource (dynamic)
4. **Resource Read Interface**: URI-based resource access
5. **Prompt Abstraction**: Base class for prompts with argument validation
6. **Prompt Registry**: Centralized prompt registration and discovery
7. **Example Prompts**: CodeReviewPrompt and SummarizePrompt
8. **Prompt Message Generation**: Template-based message creation with arguments

### Stage 4: Transport / Communication Layer ✅ Current Stage

**Goal**: Add modular transport layer for server communication.

Stage 4 introduces the transport layer while keeping MCP logic transport-agnostic:

1. **Transport Abstraction**: BaseTransport class defining transport interface
2. **STDIO Transport**: Standard input/output transport implementation
3. **Transport Handler**: Message routing and protocol translation
4. **JSON-RPC Style Protocol**: Request/response message format
5. **Complete Decoupling**: MCP server has no knowledge of transport mechanism
6. **Replaceable Transport**: Ability to swap transports without changing MCP code

**Important**: Stage 4 focuses on the communication layer. SDK and UI are in Stage 5.

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
│   ├── mcp/                    # MCP Layer (Stages 2-3)
│   │   ├── server.py          # MCP server (updated for Stage 3)
│   │   ├── tool_registry.py   # Tool registry (Stage 2)
│   │   ├── resource_registry.py  # Resource registry (Stage 3) **NEW**
│   │   ├── prompt_registry.py    # Prompt registry (Stage 3) **NEW**
│   │   ├── tools/             # Tool implementations (Stage 2)
│   │   │   ├── base_tool.py   # Abstract base tool
│   │   │   ├── calculator_tool.py
│   │   │   └── echo_tool.py
│   │   ├── resources/         # Resource implementations (Stage 3) **NEW**
│   │   │   ├── base_resource.py   # Abstract base resource
│   │   │   ├── config_resource.py # Static resource example
│   │   │   └── status_resource.py # Dynamic resource example
│   │   ├── prompts/           # Prompt implementations (Stage 3) **NEW**
│   │   │   ├── base_prompt.py     # Abstract base prompt
│   │   │   ├── code_review_prompt.py
│   │   │   └── summarize_prompt.py
│   │   └── schemas/           # JSON schema definitions (Stage 2)
│   │       └── tool_schemas.py
│   │
│   ├── transport/              # Transport Layer (Stage 4) **NEW**
│   │   ├── base_transport.py  # Abstract base transport
│   │   ├── stdio_transport.py # STDIO transport implementation
│   │   └── transport_handler.py # Message routing and protocol
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
│   ├── mcp/                   # Stage 2-3 tests
│   │   ├── test_server.py     # Updated for Stage 3
│   │   ├── test_tool_registry.py  # Stage 2
│   │   ├── test_resource_registry.py  # Stage 3 **NEW**
│   │   ├── test_prompt_registry.py    # Stage 3 **NEW**
│   │   ├── tools/             # Stage 2 tests
│   │   │   ├── test_calculator_tool.py
│   │   │   └── test_echo_tool.py
│   │   ├── resources/         # Stage 3 tests **NEW**
│   │   │   ├── test_config_resource.py
│   │   │   └── test_status_resource.py
│   │   └── prompts/           # Stage 3 tests **NEW**
│   │       ├── test_code_review_prompt.py
│   │       └── test_summarize_prompt.py
│   ├── transport/              # Stage 4 tests **NEW**
│   │   ├── test_stdio_transport.py
│   │   └── test_transport_handler.py
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

## Stage 2-3: MCP Layer Components

### MCP Server (`src/mcp/server.py`)

- **MCPServer**: MCP server with full primitive support
  - Server initialization and lifecycle management
  - Tool, Resource, and Prompt registration interfaces
  - Tool execution pipeline
  - Resource read interface
  - Prompt message generation interface
  - Uses ConfigManager for server configuration
  - Uses Logger for all server operations
  - Uses ErrorHandler for robust error handling
  - **No hard-coded values** - all configuration from YAML
  - **Stage 3 capabilities**: Tools, Resources, and Prompts

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

### Resource Registry (`src/mcp/resource_registry.py`)

- **ResourceRegistry**: Centralized resource management (Stage 3)
  - Singleton pattern for single source of truth
  - Resource registration and unregistration by URI
  - Resource discovery by URI
  - List all available resources
  - Get resource metadata (name, description, MIME type, dynamic status)
  - Integrates with logging and error handling

### Resource Abstraction (`src/mcp/resources/base_resource.py`)

- **BaseResource**: Abstract base class for all resources (Stage 3)
  - Defines resource interface contract
  - URI-based identification
  - MIME type support
  - Dynamic vs. static resource differentiation
  - read() method returns standardized format
  - Automatic logging and error handling
  - All concrete resources must inherit from BaseResource

### Example Resources (Illustrative)

**Note**: These resources are placeholder examples demonstrating the architecture.

- **ConfigResource** (`src/mcp/resources/config_resource.py`)
  - Static resource providing application configuration
  - Returns current ConfigManager state
  - Demonstrates static resource pattern (is_dynamic() returns False)
  - Content remains consistent across reads

- **StatusResource** (`src/mcp/resources/status_resource.py`)
  - Dynamic resource providing system status
  - Returns timestamp and read count
  - Demonstrates dynamic resource pattern (is_dynamic() returns True)
  - Content changes with each read

### Prompt Registry (`src/mcp/prompt_registry.py`)

- **PromptRegistry**: Centralized prompt management (Stage 3)
  - Singleton pattern for single source of truth
  - Prompt registration and unregistration by name
  - Prompt discovery by name
  - List all available prompts
  - Get prompt metadata (name, description, arguments)
  - Integrates with logging and error handling

### Prompt Abstraction (`src/mcp/prompts/base_prompt.py`)

- **BasePrompt**: Abstract base class for all prompts (Stage 3)
  - Defines prompt interface contract
  - Argument definition with required/optional support
  - Automatic argument validation
  - get_messages() returns list of message dicts (role + content)
  - Template-based message generation
  - All concrete prompts must inherit from BasePrompt

### Example Prompts (Illustrative)

**Note**: These prompts are placeholder examples demonstrating the architecture.

- **CodeReviewPrompt** (`src/mcp/prompts/code_review_prompt.py`)
  - Guides model to review code for quality
  - 3 arguments: code (required), language (optional), focus (optional)
  - Demonstrates multi-argument prompts
  - Returns system and user messages

- **SummarizePrompt** (`src/mcp/prompts/summarize_prompt.py`)
  - Guides model to summarize text
  - 2 arguments: text (required), length (optional)
  - Demonstrates simpler prompt structure
  - Template-based message construction

## Stage 4: Transport Layer Components

### Base Transport (`src/transport/base_transport.py`)

- **BaseTransport**: Abstract base class for all transport implementations (Stage 4)
  - Defines transport interface contract
  - Message transmission and reception abstraction
  - Message handler callback mechanism
  - Transport lifecycle management (start/stop)
  - Completely independent of MCP logic
  - All concrete transports must inherit from BaseTransport

### STDIO Transport (`src/transport/stdio_transport.py`)

- **STDIOTransport**: Standard input/output transport (Stage 4)
  - Communicates via stdin and stdout
  - Newline-delimited JSON messages
  - Non-blocking message reception
  - Automatic JSON serialization/deserialization
  - Server loop for continuous message processing
  - Recommended transport for MCP servers

### Transport Handler (`src/transport/transport_handler.py`)

- **TransportHandler**: Bridges transport and MCP server (Stage 4)
  - Translates transport messages to MCP operations
  - JSON-RPC style message protocol
  - Method routing (server.*, tool.*, resource.*, prompt.*)
  - Request/response formatting
  - Error handling and response generation
  - Keeps transport and MCP completely decoupled

### Transport Architecture

The transport layer is designed with complete separation from MCP logic:

**Key Principles:**
1. **Abstraction**: BaseTransport defines the contract
2. **Independence**: Transport has no knowledge of MCP primitives
3. **Adaptability**: TransportHandler translates between layers
4. **Replaceability**: Swap transports without changing MCP code
5. **Extensibility**: Add new transports (HTTP, SSE, WebSocket) easily

**Message Flow:**
```
Client → Transport (STDIO) → TransportHandler → MCP Server → Response
        ↑                                                         ↓
        ←─────────────────────────────────────────────────────────┘
```

**Supported Methods:**
- `server.info`: Get server information
- `server.initialize`: Initialize server
- `tool.list`: List available tools
- `tool.execute`: Execute a tool
- `resource.list`: List available resources
- `resource.read`: Read a resource
- `prompt.list`: List available prompts
- `prompt.get_messages`: Get prompt messages

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

### Stage 2-3: MCP Server with Tools, Resources, and Prompts

```python
from src.mcp.server import MCPServer
from src.mcp.tools.calculator_tool import CalculatorTool
from src.mcp.tools.echo_tool import EchoTool
from src.mcp.resources.config_resource import ConfigResource
from src.mcp.resources.status_resource import StatusResource
from src.mcp.prompts.code_review_prompt import CodeReviewPrompt
from src.mcp.prompts.summarize_prompt import SummarizePrompt

# Initialize MCP server with all three primitives
server = MCPServer()

# Create instances
calculator = CalculatorTool()
echo = EchoTool()
config_resource = ConfigResource()
status_resource = StatusResource()
code_review_prompt = CodeReviewPrompt()
summarize_prompt = SummarizePrompt()

server.initialize(
    tools=[calculator, echo],
    resources=[config_resource, status_resource],
    prompts=[code_review_prompt, summarize_prompt]
)

# Get server info
info = server.get_info()
print(f"Server: {info['name']} v{info['version']}")
print(f"Stage: {info['stage']}")
print(f"Capabilities: {info['capabilities']}")
print(f"Tools: {info['tool_count']}, Resources: {info['resource_count']}, Prompts: {info['prompt_count']}")

# ===== Working with Tools =====
print("\n--- Tools ---")
result = server.execute_tool('calculator', {
    'operation': 'add',
    'a': 10,
    'b': 5
})
if result['success']:
    print(f"Calculator result: {result['result']['result']}")  # Output: 15

# ===== Working with Resources =====
print("\n--- Resources ---")
# Read static resource (config)
config_data = server.read_resource('config://app')
print(f"Config resource: {config_data['uri']}")

# Read dynamic resource (status)
status_data1 = server.read_resource('status://system')
status_data2 = server.read_resource('status://system')
print(f"Status read count changed: {status_data1['content']['read_count']} -> {status_data2['content']['read_count']}")

# List all resources
resources = server.list_resources()
print(f"Available resources: {resources}")

# ===== Working with Prompts =====
print("\n--- Prompts ---")
# Get prompt messages for code review
messages = server.get_prompt_messages('code_review', {
    'code': 'def foo(): pass',
    'language': 'python',
    'focus': 'best practices'
})
print(f"Code review prompt generated {len(messages)} messages")
print(f"System message: {messages[0]['content'][:50]}...")

# Get prompt messages for summarization
messages = server.get_prompt_messages('summarize', {
    'text': 'This is a long text to summarize.',
    'length': 'short'
})
print(f"Summarize prompt generated {len(messages)} messages")

# List all prompts
prompts = server.list_prompts()
print(f"Available prompts: {prompts}")

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

## Stage 2-4 Architectural Highlights

### How Stage 4 Builds on Stages 1-3

1. **Zero Modification to Core**: Stage 1 infrastructure (`src/core/`) remains untouched
2. **Zero Modification to MCP**: MCP server and primitives completely unchanged
3. **Complete Decoupling**: Transport layer has no knowledge of MCP internals
4. **Adapter Pattern**: TransportHandler bridges transport and MCP without coupling
5. **Seamless Integration**: Transport uses Stage 1 services (config, logging, errors)
6. **No Hard-coded Values**: All configuration in `config/base.yaml`
7. **Complete Test Coverage**: 25 new tests added for Stage 4 (147 tests total, all passing)
8. **Consistent Patterns**: Transport follows same patterns as other layers (base class, implementation)

### What Stage 4 Demonstrates

**Transport Abstraction Benefits:**
- Swap STDIO for HTTP/SSE/WebSocket without changing MCP code
- MCP server is completely transport-agnostic
- Transport implementations are independent and replaceable
- Message protocol is standardized (JSON-RPC style)

**Clean Architecture:**
- Each layer communicates through well-defined interfaces
- No circular dependencies between layers
- Transport → Handler → MCP Server (one-way dependency flow)

### What Stage 4 Does NOT Include (per assignment8)

- **No SDK**: SDK abstraction is in Stage 5
- **No UI**: User interface is in Stage 5
- **No Client Library**: Client-side SDK comes in Stage 5

## Next Stages (per assignment8)

**Completed:**
- ✅ **Stage 1: Foundation** - Core infrastructure (config, logging, errors, testing)
- ✅ **Stage 2: MCP + Tools** - MCP server with tool registry and example tools
- ✅ **Stage 3: Tools, Resources, and Prompts** - All three MCP primitives with registries and examples
- ✅ **Stage 4: Transport / Communication Layer** - Modular transport layer with STDIO implementation

**Remaining:**
- **Stage 5: SDK and User Interface** - Client SDK and user-facing interface

Each stage builds upon the previous without breaking existing functionality. The modular architecture enables independent development and testing of each layer.

## License

This project is created for academic purposes as part of a software architecture course.

## Author

Tal Barda
