#!/usr/bin/env python3
"""
Weather Plugin - Demonstrates MCP System Extensibility

This is a concrete example of how to extend the MCP system without modifying
core code. It demonstrates the plugin/extension architecture using the existing
extension points provided by the system.

PLUGIN ARCHITECTURE PRINCIPLES:

1. **Extension Point**: BaseTool provides the contract for tools
2. **Registration**: ToolRegistry manages tool discovery
3. **No Core Changes**: This plugin is completely external to core MCP code
4. **Clean Architecture**: Dependency inversion - plugin depends on abstractions

HOW THIS WORKS:

1. Import the base classes (abstractions, not implementations)
2. Define your tool by extending BaseTool
3. Register the tool with ToolRegistry.get_instance()
4. Use the tool like any other MCP tool

This pattern demonstrates the Open/Closed Principle:
- System is OPEN for extension (new tools can be added)
- System is CLOSED for modification (no changes to core MCP code)

USAGE:

    # Option 1: Direct usage in Python
    from examples.plugins.weather_plugin import WeatherTool
    from src.mcp.tool_registry import ToolRegistry
    
    registry = ToolRegistry.get_instance()
    registry.register(WeatherTool())
    
    # Option 2: See plugin_demo.py for full server example
    python3 examples/plugins/plugin_demo.py
"""

from typing import Any, Dict
import random
from datetime import datetime

from src.mcp.tools.base_tool import BaseTool
from src.mcp.schemas.tool_schemas import ToolSchema
from src.core.errors.exceptions import ValidationError


class WeatherTool(BaseTool):
    """
    Weather information tool - Plugin example.
    
    **This is a PLUGIN/EXTENSION example** demonstrating how to extend
    the MCP system without modifying core code.
    
    Features:
    - Extends BaseTool (extension point)
    - Registers via ToolRegistry (registry pattern)
    - No modifications to MCP server code required
    - Works alongside built-in tools
    
    **Data Source**: Simulated (for demo purposes, no external APIs)
    
    **Use Case**: Get current weather for a given city
    """

    def _define_schema(self) -> ToolSchema:
        """Define the weather tool schema."""
        return ToolSchema(
            name='weather',
            description='Get current weather information for a city (simulated data)',
            input_schema={
                'type': 'object',
                'properties': {
                    'city': {
                        'type': 'string',
                        'description': 'City name (e.g., "New York", "London", "Tokyo")',
                        'minLength': 1
                    },
                    'units': {
                        'type': 'string',
                        'description': 'Temperature units: "celsius" or "fahrenheit"',
                        'enum': ['celsius', 'fahrenheit'],
                        'default': 'celsius'
                    }
                },
                'required': ['city']
            },
            output_schema={
                'type': 'object',
                'properties': {
                    'city': {
                        'type': 'string',
                        'description': 'City name'
                    },
                    'temperature': {
                        'type': 'number',
                        'description': 'Current temperature'
                    },
                    'units': {
                        'type': 'string',
                        'description': 'Temperature units'
                    },
                    'condition': {
                        'type': 'string',
                        'description': 'Weather condition'
                    },
                    'humidity': {
                        'type': 'integer',
                        'description': 'Humidity percentage'
                    },
                    'timestamp': {
                        'type': 'string',
                        'description': 'Timestamp of weather data'
                    }
                }
            }
        )

    def _execute_impl(self, params: Dict[str, Any]) -> Any:
        """
        Execute weather lookup (simulated).
        
        Args:
            params: Must contain 'city' (string), optional 'units' (string)
            
        Returns:
            Dictionary with weather information
            
        Raises:
            ValidationError: If city parameter is missing or invalid
        """
        city = params.get('city', '').strip()
        units = params.get('units', 'celsius')

        # Validate city
        if not city:
            raise ValidationError(
                "City name is required",
                {'city': city}
            )

        self.logger.info(f"Fetching weather for: {city} (units: {units})")

        # Simulate weather data (deterministic based on city name for demo)
        # In a real plugin, this would call an external API
        weather_data = self._simulate_weather(city, units)

        self.logger.info(
            f"Weather retrieved: {weather_data['temperature']}° {weather_data['condition']}"
        )

        return weather_data

    def _simulate_weather(self, city: str, units: str) -> Dict[str, Any]:
        """
        Simulate weather data.
        
        In a production plugin, this would:
        - Call an external weather API (e.g., OpenWeatherMap)
        - Handle API errors and rate limiting
        - Cache results to avoid excessive API calls
        - Validate API responses
        
        For this demo, we simulate data based on city name hash
        to keep it deterministic and require no external dependencies.
        
        Args:
            city: City name
            units: Temperature units
            
        Returns:
            Simulated weather data
        """
        # Use city name to seed random (deterministic for same city)
        seed = sum(ord(c) for c in city.lower())
        random.seed(seed)

        # Generate simulated temperature
        base_temp_celsius = random.randint(10, 30)
        
        if units == 'fahrenheit':
            temperature = (base_temp_celsius * 9/5) + 32
        else:
            temperature = base_temp_celsius

        # Simulated weather conditions
        conditions = [
            'Sunny',
            'Partly Cloudy',
            'Cloudy',
            'Rainy',
            'Clear',
            'Overcast'
        ]
        condition = random.choice(conditions)

        # Simulated humidity
        humidity = random.randint(30, 90)

        return {
            'city': city,
            'temperature': round(temperature, 1),
            'units': units,
            'condition': condition,
            'humidity': humidity,
            'timestamp': datetime.now().isoformat(),
            'note': 'Simulated data for demo purposes'
        }


# Plugin registration example
# This shows how the plugin can self-register when imported
if __name__ == "__main__":
    print("=" * 60)
    print("Weather Plugin - Extension Example")
    print("=" * 60)
    print()
    print("This plugin demonstrates MCP system extensibility:")
    print("1. Extends BaseTool (extension point)")
    print("2. No core MCP code modifications required")
    print("3. Clean architecture - depends on abstractions")
    print()
    print("To use this plugin:")
    print("  python3 examples/plugins/plugin_demo.py")
    print()
    print("Or import and register manually:")
    print("  from examples.plugins.weather_plugin import WeatherTool")
    print("  from src.mcp.tool_registry import ToolRegistry")
    print()
    print("  registry = ToolRegistry.get_instance()")
    print("  registry.register(WeatherTool())")
    print()
    print("=" * 60)
