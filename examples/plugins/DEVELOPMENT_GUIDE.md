# Plugin Development Guide

A comprehensive guide to creating plugins for the MCP Modular Architecture.

---

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Step-by-Step Guide](#step-by-step-guide)
4. [Required Interfaces](#required-interfaces)
5. [Extension Points](#extension-points)
6. [Common Mistakes](#common-mistakes)
7. [Best Practices](#best-practices)
8. [Testing Plugins](#testing-plugins)
9. [Complete Examples](#complete-examples)
10. [Advanced Topics](#advanced-topics)

---

## Overview

The MCP Modular Architecture is designed for extensibility through clean architecture patterns. Plugins allow you to add new tools, resources, and prompts **without modifying core code**.

### Why Plugins?

- ✅ **Zero core modifications**: Extend functionality without touching MCP source code
- ✅ **Clean architecture**: Dependency inversion - plugins depend on abstractions
- ✅ **Open/Closed Principle**: System open for extension, closed for modification
- ✅ **Same interface**: Plugins work exactly like built-in components

### What Can Be Extended?

1. **Tools**: Executable functions (most common)
2. **Resources**: Data sources with URIs
3. **Prompts**: LLM prompt templates

This guide focuses on **tool plugins** (the most common use case).

---

## Quick Start

### Minimal Working Plugin (5 Minutes)

```python
# my_plugin.py
from src.mcp.tools.base_tool import BaseTool
from src.mcp.schemas.tool_schemas import ToolSchema

class MyPlugin(BaseTool):
    def _define_schema(self) -> ToolSchema:
        return ToolSchema(
            name='my_plugin',
            description='My custom plugin that does X',
            input_schema={
                'type': 'object',
                'properties': {
                    'input': {'type': 'string'}
                },
                'required': ['input']
            }
        )

    def _execute_impl(self, params):
        return {'result': f"Processed: {params['input']}"}
```

### Using Your Plugin

```python
from src.mcp.server import MCPServer
from my_plugin import MyPlugin

server = MCPServer()
server.initialize(tools=[MyPlugin()])
result = server.execute_tool('my_plugin', {'input': 'hello'})
print(result)  # {'success': True, 'result': {'result': 'Processed: hello'}}
```

---

## Step-by-Step Guide

### Step 1: Create Plugin File

Create a new Python file in `examples/plugins/` or your own plugin directory:

```bash
touch examples/plugins/my_awesome_plugin.py
```

### Step 2: Import Required Base Classes

```python
from src.mcp.tools.base_tool import BaseTool
from src.mcp.schemas.tool_schemas import ToolSchema
from typing import Any, Dict
```

**Optional imports** (for advanced features):

```python
from src.core.errors.exceptions import ValidationError  # For custom validation
from datetime import datetime  # For timestamps
```

### Step 3: Define Your Plugin Class

```python
class MyAwesomeTool(BaseTool):
    """
    Brief description of what your tool does.

    This tool demonstrates [specific functionality].

    Use Case: [When should users use this tool?]
    """
    pass
```

**Naming Convention**: `<Name>Tool` (e.g., `WeatherTool`, `DatabaseTool`)

### Step 4: Implement `_define_schema()`

This method defines your tool's interface:

```python
def _define_schema(self) -> ToolSchema:
    return ToolSchema(
        name='my_awesome_tool',           # Tool identifier (snake_case)
        description='Does awesome things', # User-facing description

        # Input parameters
        input_schema={
            'type': 'object',
            'properties': {
                'param1': {
                    'type': 'string',
                    'description': 'First parameter',
                    'minLength': 1
                },
                'param2': {
                    'type': 'integer',
                    'description': 'Second parameter',
                    'minimum': 0,
                    'default': 10
                }
            },
            'required': ['param1']  # Required parameters
        },

        # Output schema (optional but recommended)
        output_schema={
            'type': 'object',
            'properties': {
                'result': {'type': 'string'}
            }
        }
    )
```

### Step 5: Implement `_execute_impl()`

This method contains your tool's core logic:

```python
def _execute_impl(self, params: Dict[str, Any]) -> Any:
    """
    Execute the tool logic.

    Args:
        params: Validated input parameters (already validated by BaseTool)

    Returns:
        Tool result (any JSON-serializable type)

    Raises:
        ValidationError: For custom validation failures
        RuntimeError: For execution failures
    """
    # Extract parameters
    param1 = params.get('param1')
    param2 = params.get('param2', 10)  # Default value

    # Custom validation (if needed beyond schema)
    if param1 == 'forbidden':
        raise ValidationError(
            "Invalid input value",
            {'param1': param1}
        )

    # Log important operations
    self.logger.info(f"Processing with param1={param1}")

    # Your core logic here
    result = self._do_awesome_thing(param1, param2)

    # Return result
    return {'result': result}

def _do_awesome_thing(self, param1: str, param2: int) -> str:
    """Helper method for core logic."""
    return f"{param1} processed {param2} times"
```

### Step 6: Register Your Plugin

```python
from src.mcp.server import MCPServer
from examples.plugins.my_awesome_plugin import MyAwesomeTool

# Initialize server
server = MCPServer()

# Register your plugin alongside built-in tools
server.initialize(
    tools=[
        # Built-in tools
        CalculatorTool(),
        EchoTool(),
        # Your plugin
        MyAwesomeTool()
    ]
)
```

### Step 7: Test Your Plugin

```python
# Execute your plugin
result = server.execute_tool(
    'my_awesome_tool',
    {'param1': 'test', 'param2': 5}
)

if result['success']:
    print(f"Success: {result['result']}")
else:
    print(f"Error: {result['error']}")
```

---

## Required Interfaces

### BaseTool Interface

All tool plugins **must** implement:

```python
class YourTool(BaseTool):
    def _define_schema(self) -> ToolSchema:
        """Define tool interface (name, description, schemas)."""
        pass  # REQUIRED

    def _execute_impl(self, params: Dict[str, Any]) -> Any:
        """Implement core logic."""
        pass  # REQUIRED
```

### Inherited Features (No Implementation Needed)

These are provided by `BaseTool`:

```python
# Automatic features:
- self.logger        # Pre-configured logger
- self.error_handler # Error handling utilities
- self.name          # Tool name from schema
- self.description   # Tool description from schema
- self.schema        # Full ToolSchema object
- self.execute()     # Public execution method (handles validation/errors)
- self.to_dict()     # Dictionary representation
```

### ToolSchema Structure

```python
ToolSchema(
    name: str,              # REQUIRED: Tool identifier
    description: str,       # REQUIRED: User-facing description
    input_schema: dict,     # REQUIRED: JSON Schema for input
    output_schema: dict     # OPTIONAL: JSON Schema for output
)
```

---

## Extension Points

### 1. Tool Extension Point

**Interface**: `BaseTool` (abstract base class)

**Registration**: Via `ToolRegistry` or `MCPServer.initialize()`

**Contract**:
- Implement `_define_schema()` → Returns `ToolSchema`
- Implement `_execute_impl()` → Returns result

### 2. Resource Extension Point

**Interface**: `BaseResource` (abstract base class)

**Example**:

```python
from src.mcp.resources.base_resource import BaseResource

class CustomResource(BaseResource):
    def __init__(self):
        super().__init__(
            uri="custom://my-resource",
            name="My Resource",
            description="Custom resource description",
            mime_type="application/json"
        )

    def read(self) -> dict:
        return {
            "uri": self.uri,
            "content": {"key": "value"}
        }

    def is_dynamic(self) -> bool:
        return False  # True if content changes on each read
```

### 3. Prompt Extension Point

**Interface**: `BasePrompt` (abstract base class)

**Example**:

```python
from src.mcp.prompts.base_prompt import BasePrompt

class CustomPrompt(BasePrompt):
    def _define_schema(self):
        return PromptSchema(
            name='custom_prompt',
            description='Custom prompt template',
            arguments_schema={...}
        )

    def _generate_messages_impl(self, args):
        return [
            {"role": "system", "content": "System message"},
            {"role": "user", "content": f"User: {args['input']}"}
        ]
```

---

## Common Mistakes

### ❌ Mistake 1: Forgetting to Call `super().__init__()`

```python
# WRONG
class MyTool(BaseTool):
    def __init__(self):
        self.custom_attr = "value"  # Missing super().__init__()
```

```python
# CORRECT
class MyTool(BaseTool):
    def __init__(self):
        super().__init__()  # Always call parent constructor
        self.custom_attr = "value"
```

**Why**: `BaseTool.__init__()` sets up logger, error handler, and schema.

---

### ❌ Mistake 2: Not Validating Custom Logic

```python
# WRONG - Schema validation only
def _execute_impl(self, params):
    # Assumes param1 is always valid
    return process(params['param1'])
```

```python
# CORRECT - Additional validation
def _execute_impl(self, params):
    value = params.get('param1')

    # Custom validation beyond schema
    if value == 'forbidden':
        raise ValidationError("Invalid value", {'param1': value})

    return process(value)
```

**Why**: JSON Schema handles type/format, but not business logic validation.

---

### ❌ Mistake 3: Modifying `params` Dictionary

```python
# WRONG - Mutating input
def _execute_impl(self, params):
    params['new_key'] = 'value'  # Don't modify params!
    return params
```

```python
# CORRECT - Create new dictionary
def _execute_impl(self, params):
    result = params.copy()
    result['new_key'] = 'value'
    return result
```

**Why**: Params may be reused or logged; mutation causes side effects.

---

### ❌ Mistake 4: Returning Non-JSON-Serializable Types

```python
# WRONG
def _execute_impl(self, params):
    return datetime.now()  # Not JSON-serializable!
```

```python
# CORRECT
def _execute_impl(self, params):
    return {'timestamp': datetime.now().isoformat()}
```

**Why**: Results must be JSON-serializable for transport layer.

---

### ❌ Mistake 5: Ignoring Error Handling

```python
# WRONG - Uncaught exceptions
def _execute_impl(self, params):
    data = fetch_external_api()  # May fail!
    return process(data)
```

```python
# CORRECT - Handle errors gracefully
def _execute_impl(self, params):
    try:
        data = fetch_external_api()
        return process(data)
    except requests.RequestException as e:
        self.logger.error(f"API call failed: {e}")
        raise RuntimeError(f"External API error: {e}")
```

**Why**: `BaseTool.execute()` catches exceptions, but specific errors should be logged.

---

### ❌ Mistake 6: Using `execute()` Instead of `_execute_impl()`

```python
# WRONG - Overriding public method
class MyTool(BaseTool):
    def execute(self, params):  # Don't override this!
        return {"result": "value"}
```

```python
# CORRECT - Implement abstract method
class MyTool(BaseTool):
    def _execute_impl(self, params):  # Implement this
        return {"result": "value"}
```

**Why**: `execute()` provides validation/error handling wrapper. Override `_execute_impl()`.

---

## Best Practices

### 1. Naming Conventions

**Tool Names** (in schema):
- Use `snake_case`
- Descriptive and concise
- Verb-based for actions

```python
# Good
name='fetch_weather'
name='calculate_distance'
name='send_email'

# Avoid
name='FetchWeather'  # Not snake_case
name='tool1'         # Not descriptive
name='weather'       # Missing verb
```

**Class Names**:
- Use `PascalCase`
- End with `Tool`

```python
# Good
class WeatherFetcherTool(BaseTool):
class EmailSenderTool(BaseTool):

# Avoid
class weather_tool(BaseTool):  # Not PascalCase
class Weather(BaseTool):       # Missing 'Tool' suffix
```

---

### 2. Schema Design

**Clear Descriptions**:

```python
# Good
description='Fetch current weather information for a specified city'

# Avoid
description='Weather tool'  # Too vague
```

**Comprehensive Input Schema**:

```python
input_schema={
    'type': 'object',
    'properties': {
        'city': {
            'type': 'string',
            'description': 'City name (e.g., "London", "Tokyo")',  # Examples!
            'minLength': 1
        },
        'units': {
            'type': 'string',
            'enum': ['celsius', 'fahrenheit'],  # Explicit options
            'default': 'celsius',               # Default values
            'description': 'Temperature units'
        }
    },
    'required': ['city']
}
```

**Output Schema** (recommended):

```python
output_schema={
    'type': 'object',
    'properties': {
        'temperature': {'type': 'number'},
        'condition': {'type': 'string'},
        'timestamp': {'type': 'string', 'format': 'date-time'}
    }
}
```

---

### 3. Logging

**Use Appropriate Log Levels**:

```python
def _execute_impl(self, params):
    # DEBUG: Detailed diagnostic info
    self.logger.debug(f"Input params: {params}")

    # INFO: Important operations
    self.logger.info(f"Fetching data for city: {params['city']}")

    # WARNING: Unexpected but handled
    if retry_count > 0:
        self.logger.warning(f"Retrying after failure (attempt {retry_count})")

    # ERROR: Operation failed
    if not data:
        self.logger.error("Failed to retrieve data from API")

    return result
```

---

### 4. Error Messages

**Be Specific**:

```python
# Good
raise ValidationError(
    "City name cannot be empty",
    {'city': params.get('city')}
)

# Avoid
raise ValidationError("Invalid input")  # Too vague
```

**Include Context**:

```python
try:
    result = external_api_call()
except APIError as e:
    raise RuntimeError(
        f"Weather API returned error: {e.status_code} - {e.message}"
    )
```

---

### 5. Documentation

**Comprehensive Docstrings**:

```python
class WeatherTool(BaseTool):
    """
    Weather information retrieval tool.

    Fetches current weather data for a specified city using an external
    weather API. Supports both Celsius and Fahrenheit temperature units.

    Use Cases:
        - Get current weather conditions
        - Temperature checks for automation
        - Weather-based decision making

    Data Source:
        OpenWeatherMap API (https://openweathermap.org/)

    Rate Limits:
        60 requests per minute (free tier)

    Examples:
        >>> tool = WeatherTool()
        >>> result = tool.execute({'city': 'London', 'units': 'celsius'})
        >>> print(result['result']['temperature'])
        18.5
    """
```

---

### 6. Testing (See [Testing Plugins](#testing-plugins))

Always include:
- Unit tests for `_execute_impl()`
- Integration tests with `MCPServer`
- Error case tests
- Schema validation tests

---

## Testing Plugins

### Unit Tests

**Test File Structure**: `tests/plugins/test_my_plugin.py`

```python
import pytest
from examples.plugins.my_plugin import MyAwesomeTool

class TestMyAwesomeTool:
    """Unit tests for MyAwesomeTool plugin."""

    @pytest.fixture
    def tool(self):
        """Create tool instance for testing."""
        return MyAwesomeTool()

    def test_schema_definition(self, tool):
        """Test that schema is properly defined."""
        assert tool.name == 'my_awesome_tool'
        assert tool.description != ''
        assert 'properties' in tool.schema.input_schema

    def test_successful_execution(self, tool):
        """Test successful tool execution."""
        result = tool.execute({
            'param1': 'test',
            'param2': 5
        })

        assert result['success'] is True
        assert 'result' in result['result']

    def test_missing_required_parameter(self, tool):
        """Test error handling for missing required parameter."""
        result = tool.execute({})  # Missing 'param1'

        assert result['success'] is False
        assert 'error' in result

    def test_invalid_parameter_type(self, tool):
        """Test validation of parameter types."""
        result = tool.execute({
            'param1': 123,  # Should be string
            'param2': 'invalid'  # Should be integer
        })

        assert result['success'] is False

    def test_custom_validation(self, tool):
        """Test custom business logic validation."""
        result = tool.execute({
            'param1': 'forbidden',  # Custom validation should reject this
            'param2': 5
        })

        assert result['success'] is False
        assert 'forbidden' in result['error'].lower()
```

### Integration Tests

```python
def test_plugin_registration():
    """Test plugin registration with MCP server."""
    from src.mcp.server import MCPServer
    from examples.plugins.my_plugin import MyAwesomeTool

    server = MCPServer()
    server.initialize(tools=[MyAwesomeTool()])

    # Verify tool is registered
    tools = server.get_tools_metadata()
    tool_names = [t['name'] for t in tools]
    assert 'my_awesome_tool' in tool_names

def test_plugin_execution_via_server():
    """Test plugin execution through MCP server."""
    from src.mcp.server import MCPServer
    from examples.plugins.my_plugin import MyAwesomeTool

    server = MCPServer()
    server.initialize(tools=[MyAwesomeTool()])

    result = server.execute_tool(
        'my_awesome_tool',
        {'param1': 'test', 'param2': 10}
    )

    assert result['success'] is True
```

### Running Tests

```bash
# Run all plugin tests
pytest tests/plugins/

# Run specific test file
pytest tests/plugins/test_my_plugin.py

# Run with coverage
pytest tests/plugins/ --cov=examples.plugins --cov-report=term-missing

# Run specific test
pytest tests/plugins/test_my_plugin.py::TestMyAwesomeTool::test_successful_execution -v
```

---

## Complete Examples

### Example 1: Text Processing Tool

```python
from src.mcp.tools.base_tool import BaseTool
from src.mcp.schemas.tool_schemas import ToolSchema
from typing import Any, Dict

class TextProcessorTool(BaseTool):
    """Tool for basic text processing operations."""

    def _define_schema(self) -> ToolSchema:
        return ToolSchema(
            name='text_processor',
            description='Perform text processing operations (uppercase, lowercase, reverse)',
            input_schema={
                'type': 'object',
                'properties': {
                    'text': {
                        'type': 'string',
                        'description': 'Input text to process',
                        'minLength': 1
                    },
                    'operation': {
                        'type': 'string',
                        'enum': ['uppercase', 'lowercase', 'reverse', 'count'],
                        'description': 'Operation to perform on text'
                    }
                },
                'required': ['text', 'operation']
            },
            output_schema={
                'type': 'object',
                'properties': {
                    'original': {'type': 'string'},
                    'result': {'type': ['string', 'integer']},
                    'operation': {'type': 'string'}
                }
            }
        )

    def _execute_impl(self, params: Dict[str, Any]) -> Any:
        text = params['text']
        operation = params['operation']

        self.logger.info(f"Processing text with operation: {operation}")

        # Perform operation
        if operation == 'uppercase':
            result = text.upper()
        elif operation == 'lowercase':
            result = text.lower()
        elif operation == 'reverse':
            result = text[::-1]
        elif operation == 'count':
            result = len(text)
        else:
            raise ValueError(f"Unknown operation: {operation}")

        return {
            'original': text,
            'result': result,
            'operation': operation
        }
```

**Usage**:

```python
tool = TextProcessorTool()
result = tool.execute({'text': 'Hello World', 'operation': 'uppercase'})
print(result)
# {'success': True, 'result': {'original': 'Hello World', 'result': 'HELLO WORLD', 'operation': 'uppercase'}}
```

---

### Example 2: File Information Tool

```python
import os
from pathlib import Path
from src.mcp.tools.base_tool import BaseTool
from src.mcp.schemas.tool_schemas import ToolSchema
from src.core.errors.exceptions import ValidationError
from typing import Any, Dict

class FileInfoTool(BaseTool):
    """Tool to get information about files."""

    def _define_schema(self) -> ToolSchema:
        return ToolSchema(
            name='file_info',
            description='Get information about a file (size, type, modification time)',
            input_schema={
                'type': 'object',
                'properties': {
                    'filepath': {
                        'type': 'string',
                        'description': 'Path to the file',
                        'minLength': 1
                    }
                },
                'required': ['filepath']
            },
            output_schema={
                'type': 'object',
                'properties': {
                    'exists': {'type': 'boolean'},
                    'size_bytes': {'type': 'integer'},
                    'is_file': {'type': 'boolean'},
                    'is_directory': {'type': 'boolean'},
                    'extension': {'type': 'string'},
                    'modified_time': {'type': 'string'}
                }
            }
        )

    def _execute_impl(self, params: Dict[str, Any]) -> Any:
        filepath = params['filepath']
        path = Path(filepath)

        self.logger.info(f"Getting info for: {filepath}")

        # Check if path exists
        if not path.exists():
            raise ValidationError(
                f"File does not exist: {filepath}",
                {'filepath': filepath}
            )

        # Get file stats
        stats = path.stat()

        return {
            'exists': True,
            'size_bytes': stats.st_size,
            'is_file': path.is_file(),
            'is_directory': path.is_dir(),
            'extension': path.suffix,
            'modified_time': datetime.fromtimestamp(stats.st_mtime).isoformat()
        }
```

---

### Example 3: HTTP Request Tool

```python
import requests
from src.mcp.tools.base_tool import BaseTool
from src.mcp.schemas.tool_schemas import ToolSchema
from typing import Any, Dict

class HTTPRequestTool(BaseTool):
    """Tool for making HTTP requests."""

    def _define_schema(self) -> ToolSchema:
        return ToolSchema(
            name='http_request',
            description='Make HTTP GET requests to URLs',
            input_schema={
                'type': 'object',
                'properties': {
                    'url': {
                        'type': 'string',
                        'description': 'URL to fetch',
                        'format': 'uri'
                    },
                    'timeout': {
                        'type': 'integer',
                        'description': 'Request timeout in seconds',
                        'minimum': 1,
                        'maximum': 60,
                        'default': 10
                    }
                },
                'required': ['url']
            },
            output_schema={
                'type': 'object',
                'properties': {
                    'status_code': {'type': 'integer'},
                    'content_type': {'type': 'string'},
                    'content_length': {'type': 'integer'},
                    'response_time_ms': {'type': 'number'}
                }
            }
        )

    def _execute_impl(self, params: Dict[str, Any]) -> Any:
        url = params['url']
        timeout = params.get('timeout', 10)

        self.logger.info(f"Making HTTP request to: {url}")

        try:
            import time
            start_time = time.time()

            response = requests.get(url, timeout=timeout)

            elapsed_ms = (time.time() - start_time) * 1000

            self.logger.info(f"Request completed: {response.status_code}")

            return {
                'status_code': response.status_code,
                'content_type': response.headers.get('Content-Type', 'unknown'),
                'content_length': len(response.content),
                'response_time_ms': round(elapsed_ms, 2)
            }

        except requests.Timeout:
            raise RuntimeError(f"Request timed out after {timeout} seconds")
        except requests.RequestException as e:
            raise RuntimeError(f"HTTP request failed: {str(e)}")
```

---

## Advanced Topics

### 1. Plugin with Configuration

```python
class ConfigurablePlugin(BaseTool):
    def __init__(self, api_key: str, base_url: str = "https://api.example.com"):
        super().__init__()
        self.api_key = api_key
        self.base_url = base_url

    def _execute_impl(self, params):
        # Use self.api_key and self.base_url
        pass
```

**Usage**:

```python
plugin = ConfigurablePlugin(api_key="your-key-here")
server.initialize(tools=[plugin])
```

---

### 2. Plugin with State

```python
class StatefulPlugin(BaseTool):
    def __init__(self):
        super().__init__()
        self._call_count = 0
        self._cache = {}

    def _execute_impl(self, params):
        self._call_count += 1

        # Use cache
        cache_key = str(params)
        if cache_key in self._cache:
            self.logger.info(f"Cache hit (call #{self._call_count})")
            return self._cache[cache_key]

        # Compute and cache
        result = self._compute(params)
        self._cache[cache_key] = result
        return result
```

---

### 3. Async Plugin (Future Enhancement)

Currently, plugins are synchronous. For async operations:

```python
def _execute_impl(self, params):
    # Run async code in executor
    import asyncio

    async def async_operation():
        # Your async code here
        await asyncio.sleep(1)
        return "result"

    # Run in event loop
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(async_operation())
    return result
```

---

### 4. Plugin Discovery (Future Enhancement)

For automatic plugin loading:

```python
# plugins/__init__.py
import importlib
import pkgutil

def discover_plugins():
    """Auto-discover plugins in plugins directory."""
    plugins = []
    for _, name, _ in pkgutil.iter_modules([__path__[0]]):
        module = importlib.import_module(f'plugins.{name}')
        # Find classes that inherit from BaseTool
        for attr in dir(module):
            cls = getattr(module, attr)
            if isinstance(cls, type) and issubclass(cls, BaseTool) and cls != BaseTool:
                plugins.append(cls())
    return plugins
```

---

## Checklist for Plugin Development

Before considering your plugin complete:

- [ ] **Class inherits from `BaseTool`**
- [ ] **`_define_schema()` implemented with complete schema**
- [ ] **`_execute_impl()` implemented with core logic**
- [ ] **Tool name uses `snake_case`**
- [ ] **Class name ends with `Tool` (PascalCase)**
- [ ] **Comprehensive docstring on class**
- [ ] **Input schema includes descriptions and constraints**
- [ ] **Required parameters specified in schema**
- [ ] **Custom validation for business logic**
- [ ] **Error handling for external calls**
- [ ] **Logging at appropriate levels**
- [ ] **Unit tests written and passing**
- [ ] **Integration tests with MCPServer**
- [ ] **Error cases tested**
- [ ] **No modification of core MCP code**
- [ ] **Returns JSON-serializable data**

---

## Additional Resources

- **Weather Plugin Example**: [`weather_plugin.py`](weather_plugin.py)
- **Plugin Demo**: [`plugin_demo.py`](plugin_demo.py)
- **Architecture Documentation**: [`../../docs/architecture.md`](../../docs/architecture.md) (Section 9.4)
- **Base Tool Source**: [`../../src/mcp/tools/base_tool.py`](../../src/mcp/tools/base_tool.py)
- **Tool Schema**: [`../../src/mcp/schemas/tool_schemas.py`](../../src/mcp/schemas/tool_schemas.py)

---

## Getting Help

If you encounter issues:

1. **Check existing plugins**: Review `weather_plugin.py` for patterns
2. **Read base classes**: Study `BaseTool` implementation
3. **Run examples**: Execute `plugin_demo.py` to see working example
4. **Open an issue**: [GitHub Issues](https://github.com/TalBarda8/mcp-modular-architecture/issues)

---

**Happy Plugin Development!** 🔌
