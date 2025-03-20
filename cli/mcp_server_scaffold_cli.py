# mcp-host/cli/mcp_server_scaffold_cli.py
"""
MCP Server Scaffolding CLI

A tool for generating new MCP (Messaging Control Protocol) server templates
and managing server component creation.
"""
import os
import typer
import importlib.util
from typing import Optional
from pathlib import Path

app = typer.Typer(help="MCP Server Scaffolding CLI")

def validate_server_name(name: str) -> str:
    """
    Validate and normalize server name.
    
    Ensures the name is:
    - Lowercase
    - Uses only alphanumeric characters and underscores
    - Does not start with a number
    """
    # Convert to lowercase and replace non-alphanumeric chars with underscores
    normalized = ''.join(c if c.isalnum() or c == '_' else '_' for c in name.lower())
    
    # Ensure it doesn't start with a number
    if normalized[0].isdigit():
        normalized = f"server_{normalized}"
    
    return normalized

@app.command()
def scaffold(
    name: str = typer.Option(..., help="Name of the new MCP server"),
    location: Optional[str] = typer.Option(None, help="Location to create the server"),
    template: str = typer.Option("weather", help="Template to use for the server"),
    verbose: bool = typer.Option(False, help="Enable verbose output")
):
    """
    Scaffold a new MCP server with the specified name and template.
    
    This command creates a new server directory with the necessary 
    structure and example tools based on the chosen template.
    """
    # Validate and normalize server name
    server_name = validate_server_name(name)
    
    # Determine server location
    if location is None:
        location = os.path.join("servers", f"{server_name}_server")
    
    # Ensure the location is an absolute path
    full_location = os.path.abspath(location)
    
    # Create server directory structure
    src_dir = os.path.join(full_location, "src", f"{server_name}_server")
    os.makedirs(src_dir, exist_ok=True)
    
    # Select template
    if template == "weather":
        create_weather_server(server_name, src_dir, verbose)
    else:
        typer.echo(f"Unknown template: {template}")
        raise typer.Abort()
    
    typer.echo(f"Successfully scaffolded MCP server '{server_name}' at {full_location}")
    if verbose:
        typer.echo("Server structure:")
        print_directory_structure(full_location)

def create_weather_server(server_name: str, src_dir: str, verbose: bool = False):
    """
    Create a Weather Forecast MCP Server template
    """
    # Create __init__.py
    init_path = os.path.join(src_dir, "__init__.py")
    with open(init_path, "w") as f:
        f.write("# Weather Forecast MCP Server\n")
    if verbose:
        typer.echo(f"Created {init_path}")
    
    # Create tools.py with weather-related tools
    tools_path = os.path.join(src_dir, "tools.py")
    with open(tools_path, "w") as f:
        f.write("""\"\"\"
Weather Forecast Tools for MCP Server
\"\"\"
import random
from common.mcp_tool_decorator import tool

# Simulated weather data
WEATHER_CONDITIONS = [
    "Sunny", "Partly Cloudy", "Cloudy", 
    "Rainy", "Thunderstorms", "Snowy"
]

LOCATIONS = [
    "New York", "London", "Tokyo", 
    "Sydney", "Paris", "Cairo"
]

@tool(name="get_current_weather", description="Get current weather for a location")
def get_current_weather(location: str = "New York") -> dict:
    \"\"\"
    Retrieve current weather for a given location.
    
    Args:
        location (str, optional): Location to get weather for. Defaults to "New York".
    
    Returns:
        dict: Weather information for the specified location.
    \"\"\"
    if location not in LOCATIONS:
        raise ValueError(f"Weather data not available for {location}")
    
    return {
        "location": location,
        "condition": random.choice(WEATHER_CONDITIONS),
        "temperature": round(random.uniform(0, 35), 1),
        "humidity": round(random.uniform(20, 90), 1),
        "wind_speed": round(random.uniform(0, 50), 1)
    }

@tool(name="get_forecast", description="Get weather forecast for multiple days")
def get_forecast(location: str = "New York", days: int = 3) -> dict:
    \"\"\"
    Get multi-day weather forecast for a location.
    
    Args:
        location (str, optional): Location to get forecast for. Defaults to "New York".
        days (int, optional): Number of forecast days. Defaults to 3.
    
    Returns:
        dict: Multi-day weather forecast.
    \"\"\"
    if location not in LOCATIONS:
        raise ValueError(f"Forecast data not available for {location}")
    
    if days < 1 or days > 7:
        raise ValueError("Forecast days must be between 1 and 7")
    
    forecast = {
        "location": location,
        "days": []
    }
    
    for _ in range(days):
        forecast["days"].append({
            "condition": random.choice(WEATHER_CONDITIONS),
            "temperature_high": round(random.uniform(10, 40), 1),
            "temperature_low": round(random.uniform(-5, 25), 1),
            "precipitation_chance": round(random.uniform(0, 100), 1)
        })
    
    return forecast
""")
    if verbose:
        typer.echo(f"Created {tools_path}")
    
    # Create README for the server
    readme_path = os.path.join(src_dir, "..", "README.md")
    with open(readme_path, "w") as f:
        f.write(f"""# {server_name.replace('_', ' ').title()} MCP Server

## Overview

This MCP server provides weather-related tools for retrieving current weather and forecasts.

## Available Tools

1. `get_current_weather`: Retrieve current weather for a specified location
2. `get_forecast`: Get multi-day weather forecast

## Usage Examples

### Get Current Weather
```python
result = client.call_tool('get_current_weather', {{'location': 'New York'}})
```

### Get Weather Forecast
```python
result = client.call_tool('get_forecast', {{'location': 'London', 'days': 3}})
```
""")
    if verbose:
        typer.echo(f"Created {readme_path}")

def print_directory_structure(startpath):
    """
    Print the directory structure with indentation
    """
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        typer.echo(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            typer.echo(f"{subindent}{f}")

def main():
    app()

if __name__ == "__main__":
    main()