#!/usr/bin/env python3
"""
Plugin Demo - Shows how to extend MCP with external plugins

This script demonstrates:
1. Loading built-in tools
2. Loading external plugin (WeatherTool)
3. Using both seamlessly via the same MCP server

NO CORE CODE MODIFICATIONS REQUIRED - this is the key demonstration
of extensibility through clean architecture.
"""

from src.mcp.server import MCPServer
from src.mcp.tools.calculator_tool import CalculatorTool
from src.mcp.tools.echo_tool import EchoTool
from src.mcp.tools.batch_processor_tool import BatchProcessorTool
from src.mcp.tools.concurrent_fetcher_tool import ConcurrentFetcherTool
from src.mcp.resources.config_resource import ConfigResource
from src.mcp.resources.status_resource import StatusResource
from src.mcp.prompts.code_review_prompt import CodeReviewPrompt
from src.mcp.prompts.summarize_prompt import SummarizePrompt

# PLUGIN: Import external plugin (not part of core MCP)
from examples.plugins.weather_plugin import WeatherTool


def main():
    """Demonstrate MCP server with external plugin."""
    print("=" * 70)
    print("MCP Plugin Demo - System Extensibility")
    print("=" * 70)
    print()

    print("Demonstrating clean architecture extensibility:")
    print("• Built-in tools: calculator, echo, batch_processor, concurrent_fetcher")
    print("• Plugin tool: weather (external, not part of core MCP)")
    print()

    # Initialize MCP server
    print("1. Initializing MCP Server...")
    server = MCPServer()

    # Register built-in tools + external plugin
    # NOTE: WeatherTool is treated exactly like built-in tools!
    # This demonstrates the Open/Closed Principle in action.
    server.initialize(
        tools=[
            # Built-in tools
            CalculatorTool(),
            EchoTool(),
            BatchProcessorTool(),
            ConcurrentFetcherTool(),
            # PLUGIN: External tool (no core code changes needed!)
            WeatherTool()
        ],
        resources=[ConfigResource(), StatusResource()],
        prompts=[CodeReviewPrompt(), SummarizePrompt()]
    )
    print("   ✓ Server initialized with built-in tools + weather plugin")
    print()

    # List all tools (built-in + plugin)
    print("2. Listing All Available Tools (Built-in + Plugin)...")
    tools = server.get_tools_metadata()
    
    for tool in tools:
        tool_type = "PLUGIN" if tool['name'] == 'weather' else "Built-in"
        print(f"   • [{tool_type:8}] {tool['name']}: {tool['description'][:50]}...")
    print()

    # Execute built-in tool
    print("3. Testing Built-in Tool (calculator)...")
    result = server.execute_tool(
        'calculator',
        {'operation': 'add', 'a': 15, 'b': 27}
    )
    if result['success']:
        print(f"   Input: 15 + 27")
        print(f"   Result: {result['result']['result']}")
    print()

    # Execute PLUGIN tool (weather)
    print("4. Testing Plugin Tool (weather)...")
    
    # Test with Celsius
    result = server.execute_tool(
        'weather',
        {'city': 'Tel Aviv', 'units': 'celsius'}
    )
    if result['success']:
        weather = result['result']
        print(f"   City: {weather['city']}")
        print(f"   Temperature: {weather['temperature']}°C")
        print(f"   Condition: {weather['condition']}")
        print(f"   Humidity: {weather['humidity']}%")
        print(f"   Note: {weather.get('note', '')}")
    print()

    # Test with Fahrenheit
    result = server.execute_tool(
        'weather',
        {'city': 'New York', 'units': 'fahrenheit'}
    )
    if result['success']:
        weather = result['result']
        print(f"   City: {weather['city']}")
        print(f"   Temperature: {weather['temperature']}°F")
        print(f"   Condition: {weather['condition']}")
        print(f"   Humidity: {weather['humidity']}%")
    print()

    print("=" * 70)
    print("Key Takeaways:")
    print("=" * 70)
    print()
    print("✓ Plugin loaded without modifying core MCP code")
    print("✓ Plugin tool works exactly like built-in tools")
    print("✓ Clean architecture enables extensibility")
    print("✓ Open/Closed Principle in action:")
    print("  - System OPEN for extension (new tools)")
    print("  - System CLOSED for modification (no core changes)")
    print()
    print("Extension Points Used:")
    print("  • BaseTool: Abstract base class (dependency inversion)")
    print("  • ToolRegistry: Central registration (registry pattern)")
    print("  • MCPServer.initialize(): Accepts any BaseTool implementation")
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
