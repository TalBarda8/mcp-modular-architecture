# MCP Modular Architecture

A production-ready reference implementation of the Model Context Protocol (MCP) with a clean, layered architecture designed for extensibility and maintainability.

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-190%20passing-brightgreen)](tests/)
[![Coverage](https://img.shields.io/badge/coverage-95%25%2B-brightgreen)](docs/TESTING.md)

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Key Concepts](#key-concepts)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [CLI Usage](#cli-usage)
- [SDK Usage](#sdk-usage)
- [Running Tests](#running-tests)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

**MCP Modular Architecture** is a reference implementation demonstrating best practices for building MCP-based systems with:

- **Clean layered architecture** with strict separation of concerns
- **Transport abstraction** enabling protocol-agnostic server implementations
- **SDK-first design** for easy client integration
- **Comprehensive testing** with >95% code coverage of core business logic
- **Zero hard-coded configuration** using YAML-based config management

### What is MCP?

The Model Context Protocol (MCP) is a protocol for AI agents to interact with external tools, resources, and prompt templates. This project implements a complete MCP server with all three primitive types:

1. **Tools** — Executable functions (e.g., calculator, file operations)
2. **Resources** — Data sources that can be read (e.g., configuration, system status)
3. **Prompts** — Pre-defined prompt templates for LLM interactions

### Who is this for?

- **Developers** building MCP servers or clients
- **Architects** seeking a reference implementation of clean architecture patterns
- **Teams** looking for a modular, testable foundation for AI agent systems

---

## Architecture

The system follows a strict **layered architecture** with unidirectional dependencies:

```
┌─────────────────────────────────────────┐
│          User Interface (CLI)            │
│     ↓ uses                              │
├─────────────────────────────────────────┤
│            Client SDK                    │
│     ↓ uses                              │
├─────────────────────────────────────────┤
│         Transport Layer                  │
│     (STDIO, HTTP, WebSocket)            │
│     ↓ uses                              │
├─────────────────────────────────────────┤
│           MCP Server                     │
│  (Tools, Resources, Prompts)            │
│     ↓ uses                              │
├─────────────────────────────────────────┤
│       Core Infrastructure                │
│  (Config, Logging, Errors)              │
└─────────────────────────────────────────┘
```

### Layer Responsibilities

#### **1. Core Infrastructure**
Foundation services used throughout the application:
- **Configuration Management** — YAML-based, environment-aware configuration
- **Logging** — Structured logging with file rotation and console output
- **Error Handling** — Custom exception hierarchy and centralized error handling

#### **2. MCP Server Layer**
Business logic implementing the Model Context Protocol:
- **Server** — Manages lifecycle and coordinates primitives
- **Tool Registry** — Centralized tool registration and discovery
- **Resource Registry** — URI-based resource management
- **Prompt Registry** — Template-based prompt management

#### **3. Transport Layer**
Protocol-agnostic communication:
- **Base Transport** — Abstract interface for all transport implementations
- **STDIO Transport** — Standard input/output communication (recommended for MCP)
- **Transport Handler** — Routes messages between transport and MCP server

#### **4. SDK Layer**
Client library for MCP server integration:
- **MCP Client** — High-level API wrapping transport communication
- Context manager support for connection lifecycle
- Automatic request/response handling with error detection

#### **5. User Interface**
End-user interaction:
- **CLI** — Command-line interface using the SDK
- User-friendly commands for all MCP operations
- JSON parameter support and formatted output

---

## Key Concepts

### Tools

**Tools** are executable functions that perform actions. Each tool:
- Defines a JSON schema for input parameters
- Implements an `execute()` method
- Returns a standardized result format

**Example Tools:**
- `calculator` — Perform arithmetic operations (add, subtract, multiply, divide)
- `echo` — Simple echo functionality

### Resources

**Resources** are data sources identified by URI. Resources can be:
- **Static** — Content remains constant (e.g., configuration files)
- **Dynamic** — Content changes with each read (e.g., system status)

**Example Resources:**
- `config://app` — Application configuration
- `status://system` — System status with timestamp

### Prompts

**Prompts** are templates for LLM interactions. Each prompt:
- Accepts arguments (required and optional)
- Returns an array of messages (system, user, assistant)
- Supports template-based message generation

**Example Prompts:**
- `code_review` — Guide model to review code for quality
- `summarize` — Guide model to summarize text

### Transport Abstraction

The transport layer is **completely decoupled** from MCP logic:
- MCP server has zero knowledge of transport mechanism
- Swap STDIO for HTTP/WebSocket without changing MCP code
- Transport handler bridges the two layers

### SDK-First Design

The client SDK provides a **clean, high-level API**:
- UI components use SDK exclusively (never transport or MCP directly)
- SDK works with any transport implementation
- No business logic duplication

---

## Project Structure

```
mcp-modular-architecture/
├── config/                      # Configuration files
│   ├── base.yaml                # Base configuration
│   ├── development.yaml         # Development environment
│   └── production.yaml          # Production environment
│
├── src/                         # Source code
│   ├── core/                    # Core infrastructure
│   │   ├── config/              # Configuration management
│   │   ├── logging/             # Logging system
│   │   └── errors/              # Error handling
│   │
│   ├── mcp/                     # MCP server layer
│   │   ├── server.py            # MCP server
│   │   ├── tool_registry.py     # Tool registry
│   │   ├── resource_registry.py # Resource registry
│   │   ├── prompt_registry.py   # Prompt registry
│   │   ├── tools/               # Tool implementations
│   │   ├── resources/           # Resource implementations
│   │   ├── prompts/             # Prompt implementations
│   │   └── schemas/             # JSON schemas
│   │
│   ├── transport/               # Transport layer
│   │   ├── base_transport.py    # Abstract transport
│   │   ├── stdio_transport.py   # STDIO transport
│   │   └── transport_handler.py # Message routing
│   │
│   ├── sdk/                     # Client SDK
│   │   └── mcp_client.py        # MCP client
│   │
│   ├── ui/                      # User interface
│   │   └── cli.py               # CLI interface
│   │
│   ├── models/                  # Domain models
│   ├── services/                # Service layer
│   └── utils/                   # Utilities
│
├── tests/                       # Unit tests (165 tests)
│   ├── core/
│   ├── mcp/
│   ├── transport/
│   ├── sdk/
│   └── ...
│
├── docs/                        # Documentation
├── pyproject.toml               # Project metadata
└── requirements.txt             # Dependencies
```

---

## Installation

### Prerequisites

- **Python 3.10** or higher
- **pip** (Python package manager)

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/TalBarda8/mcp-modular-architecture.git
   cd mcp-modular-architecture
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   Or install with dev dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

---

## Running the Project

### Configuration

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

### Using the MCP Server Programmatically

```python
from src.mcp.server import MCPServer
from src.mcp.tools.calculator_tool import CalculatorTool
from src.mcp.tools.echo_tool import EchoTool
from src.mcp.resources.config_resource import ConfigResource
from src.mcp.resources.status_resource import StatusResource
from src.mcp.prompts.code_review_prompt import CodeReviewPrompt
from src.mcp.prompts.summarize_prompt import SummarizePrompt

# Initialize server
server = MCPServer()

# Register primitives
server.initialize(
    tools=[CalculatorTool(), EchoTool()],
    resources=[ConfigResource(), StatusResource()],
    prompts=[CodeReviewPrompt(), SummarizePrompt()]
)

# Execute a tool
result = server.execute_tool('calculator', {
    'operation': 'add',
    'a': 10,
    'b': 5
})
print(result)  # {'success': True, 'result': {'result': 15}}

# Read a resource
config = server.read_resource('config://app')
print(config)

# Get prompt messages
messages = server.get_prompt_messages('code_review', {
    'code': 'def foo(): pass',
    'language': 'python'
})
print(messages)
```

---

## CLI Usage

The CLI provides a user-friendly interface to interact with the MCP server.

### Available Commands

```bash
# Show server information
python -m src.ui.cli info

# List all tools
python -m src.ui.cli tools

# Execute a tool
python -m src.ui.cli tool calculator --params '{"operation": "add", "a": 10, "b": 5}'

# List all resources
python -m src.ui.cli resources

# Read a resource
python -m src.ui.cli resource config://app

# List all prompts
python -m src.ui.cli prompts

# Get prompt messages
python -m src.ui.cli prompt code_review --args '{"code": "def foo(): pass", "language": "python"}'
```

### Example Session

```bash
$ python -m src.ui.cli info
Server: MCP Modular Server v1.0.0
Capabilities: tools, resources, prompts

$ python -m src.ui.cli tools
Available tools:
- calculator: Perform basic arithmetic operations
- echo: Echo input message

$ python -m src.ui.cli tool calculator --params '{"operation": "multiply", "a": 7, "b": 6}'
Result: 42
```

---

## SDK Usage

The SDK provides a clean, high-level API for integrating with MCP servers.

### Basic Usage

```python
from src.sdk.mcp_client import MCPClient
from src.transport.stdio_transport import STDIOTransport

# Create client with STDIO transport
transport = STDIOTransport()
client = MCPClient(transport)

# Use context manager for automatic connection lifecycle
with client:
    # Get server info
    info = client.get_server_info()
    print(f"Connected to {info['name']} v{info['version']}")

    # List available tools
    tools = client.list_tools()
    print(f"Available tools: {tools}")

    # Execute a tool
    result = client.execute_tool('calculator', {
        'operation': 'add',
        'a': 5,
        'b': 3
    })
    print(f"Result: {result['result']['result']}")

    # Read a resource
    config = client.read_resource('config://app')
    print(f"Config: {config['content']}")

    # Get prompt messages
    messages = client.get_prompt_messages('summarize', {
        'text': 'Long text to summarize...',
        'length': 'short'
    })
    print(f"Prompt: {messages}")
```

### SDK Methods

**Server Methods:**
- `get_server_info()` — Get server information
- `initialize_server()` — Initialize server

**Tool Methods:**
- `list_tools()` — List available tools
- `execute_tool(name, parameters)` — Execute a tool

**Resource Methods:**
- `list_resources()` — List available resources
- `read_resource(uri)` — Read a resource by URI

**Prompt Methods:**
- `list_prompts()` — List available prompts
- `get_prompt_messages(name, arguments)` — Get prompt messages

---

## Running Tests

The project includes comprehensive unit tests with **>95% code coverage** of core business logic.

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=src --cov-report=html --cov-report=term-missing
```

View coverage report: `open htmlcov/index.html`

### Run Specific Tests

```bash
# Run tests for a specific module
pytest tests/mcp/test_server.py

# Run tests for SDK
pytest tests/sdk/

# Run tests with verbose output
pytest -v

# Run tests matching a pattern
pytest -k "test_calculator"
```

### Test Statistics

- **Total Tests:** 190
- **Pass Rate:** 100%
- **Coverage:** 95.12% (core business logic, excluding UI layer)
- **Test Organization:** Tests mirror source structure

### Coverage Details

The project maintains >95% unit test coverage for all core business logic:

- ✅ **Core Infrastructure** (config, logging, errors): 93%+
- ✅ **MCP Server** (tools, resources, prompts): 95%+
- ✅ **Transport Layer**: 85%+
- ✅ **SDK** (MCP Client): 100%
- ✅ **Models & Utilities**: 100%

**Note:** The UI layer (`src/ui/`) is intentionally excluded from unit test coverage. CLI/UI code is best tested through integration tests, E2E tests, or manual testing. See [docs/TESTING.md](docs/TESTING.md) for detailed testing strategy and rationale.

---

## Development

### Adding a New Tool

1. **Create tool class** inheriting from `BaseTool`:

```python
from src.mcp.tools.base_tool import BaseTool

class MyTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="my_tool",
            description="Description of my tool",
            input_schema={
                "type": "object",
                "properties": {
                    "param1": {"type": "string"}
                },
                "required": ["param1"]
            }
        )

    def execute(self, parameters: dict) -> dict:
        # Implementation
        return {"result": "some value"}
```

2. **Register tool** with the server:

```python
from src.mcp.server import MCPServer
from my_tool import MyTool

server = MCPServer()
server.initialize(tools=[MyTool()])
```

### Adding a New Transport

1. **Create transport class** inheriting from `BaseTransport`:

```python
from src.transport.base_transport import BaseTransport

class HTTPTransport(BaseTransport):
    def start(self) -> None:
        # Start HTTP server
        pass

    def stop(self) -> None:
        # Stop HTTP server
        pass

    def send_message(self, message: dict) -> None:
        # Send HTTP response
        pass

    def receive_message(self) -> dict:
        # Receive HTTP request
        pass
```

2. **Use the transport** with the SDK:

```python
from src.sdk.mcp_client import MCPClient
from my_transport import HTTPTransport

transport = HTTPTransport()
client = MCPClient(transport)
```

### Adding a New Resource

1. **Create resource class** inheriting from `BaseResource`:

```python
from src.mcp.resources.base_resource import BaseResource

class MyResource(BaseResource):
    def __init__(self):
        super().__init__(
            uri="custom://my-resource",
            name="My Resource",
            description="Description of resource",
            mime_type="application/json"
        )

    def read(self) -> dict:
        return {
            "uri": self.uri,
            "content": {"key": "value"}
        }

    def is_dynamic(self) -> bool:
        return False  # True if content changes
```

2. **Register resource** with the server:

```python
server.initialize(resources=[MyResource()])
```

### Extending the CLI

Edit `src/ui/cli.py` to add new commands. The CLI uses the SDK exclusively.

---

## Architecture Principles

This implementation demonstrates:

- **SOLID Principles** — Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- **Separation of Concerns** — Clear boundaries between layers
- **Dependency Injection** — Components receive dependencies rather than creating them
- **DRY (Don't Repeat Yourself)** — Common functionality extracted to base classes
- **Configuration Over Code** — All configurable values in YAML, not hard-coded
- **Testability** — Each layer independently testable with comprehensive test coverage

### Architectural Highlights

**Replaceability:**
- Swap STDIO for HTTP transport → only transport layer changes
- Replace CLI with Web UI → only UI layer changes
- Add new tools/resources/prompts → only MCP layer changes

**Independence:**
- Each layer has zero knowledge of higher layers
- MCP server doesn't know about transport mechanism
- SDK doesn't know about MCP server internals
- CLI doesn't know about transport or MCP

**Extensibility:**
- Add new transports by implementing `BaseTransport`
- Add new tools by implementing `BaseTool`
- Add new resources by implementing `BaseResource`
- Add new prompts by implementing `BasePrompt`

---

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Quality Standards

- Maintain >70% test coverage
- Follow PEP 8 style guidelines
- Keep files under 150 lines
- Add type hints to all functions
- Document all public APIs

---

## Documentation

Additional documentation available in the `docs/` directory:

- **[Architecture Documentation](docs/architecture.md)** — Detailed architecture overview with diagrams
- **[Product Requirements](docs/PRD.md)** — Complete requirements specification
- **[Architecture Decision Records](docs/adr/)** — Key architectural decisions with rationale
- **[Prompts Book](docs/prompts.md)** — AI-assisted development methodology
- **[Research Scope](docs/research_scope.md)** — Evaluation methodology

---

## License

This project is licensed under the MIT License. See `pyproject.toml` for details.

---

## Author

**Tal Barda**

GitHub: [@TalBarda8](https://github.com/TalBarda8)

---

## Acknowledgments

Built with:
- **Python 3.10+**
- **pytest** for testing
- **pyyaml** for configuration
- **python-dotenv** for environment management

---

**⭐ If you find this project useful, please consider giving it a star!**
