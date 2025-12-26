# Plugin Examples

This directory contains example plugins demonstrating how to extend the MCP system without modifying core code.

## WeatherTool Plugin

**File**: `weather_plugin.py`

A complete working example showing:
- How to create an external plugin extending `BaseTool`
- How plugins register with the system via `ToolRegistry`
- Why no core code modifications are needed
- How clean architecture enables extensibility

### Running the Demo

```bash
cd ../..  # Navigate to project root
export PYTHONPATH=.
python3 examples/plugins/plugin_demo.py
```

### What You'll See

```
MCP Plugin Demo - System Extensibility

1. Initializing MCP Server...
   ✓ Server initialized with built-in tools + weather plugin

2. Listing All Available Tools (Built-in + Plugin)...
   • [Built-in] calculator
   • [Built-in] echo
   • [Built-in] batch_processor
   • [Built-in] concurrent_fetcher
   • [PLUGIN  ] weather <-- External plugin!

4. Testing Plugin Tool (weather)...
   City: Tel Aviv
   Temperature: 22°C
   Condition: Rainy
```

### Key Architectural Points

1. **Extension Point**: `BaseTool` provides the contract
2. **Registration**: `ToolRegistry` manages discovery
3. **No Core Changes**: Plugin is completely external
4. **Dependency Inversion**: Plugin depends on abstraction, not implementation

### Creating Your Own Plugin

Follow the same pattern:

```python
from src.mcp.tools.base_tool import BaseTool
from src.mcp.schemas.tool_schemas import ToolSchema

class MyPlugin(BaseTool):
    def _define_schema(self) -> ToolSchema:
        return ToolSchema(
            name='my_plugin',
            description='What my plugin does',
            input_schema={...},
            output_schema={...}
        )
    
    def _execute_impl(self, params):
        # Your plugin logic here
        return {...}
```

Then register it:

```python
from src.mcp.server import MCPServer
from examples.plugins.my_plugin import MyPlugin

server = MCPServer()
server.initialize(tools=[..., MyPlugin()])
```

### Production Considerations

For production plugins, consider adding:
- **Plugin discovery**: Auto-load from plugin directory
- **Plugin validation**: Schema and signature verification
- **Plugin isolation**: Sandboxing for security
- **Plugin versioning**: Compatibility management
- **Error handling**: Graceful degradation

But the fundamental pattern remains the same as demonstrated here.

## Documentation

For complete documentation on the plugin architecture:
- **Architecture**: [../../docs/architecture.md](../../docs/architecture.md) (Section 9.4.3)
- **Main README**: [../../README.md](../../README.md) (Plugin Example section)
