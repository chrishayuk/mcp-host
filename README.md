# MCP Host Framework

## Overview

This project provides a flexible, extensible Messaging Control Protocol (MCP) Host framework designed for building modular, distributed tool and service ecosystems.

## Features

- Dynamic server and tool discovery
- Configurable component registration
- Asynchronous tool execution
- Flexible logging and configuration management
- Extensible architecture

## Prerequisites

- Python 3.11+
- `uv` (Universal Python Package Manager)
- Virtual environment support

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/chrishayuk/mcp-host.git
cd mcp-host
```

### 2. Create Virtual Environment

```bash
make venv
```

### 3. Install Dependencies

```bash
make rebuild
```

## Running the Server

### Start the MCP Server

```bash
# Using uv
uv run python runtime/src/mcp_server/main.py

# Or directly with Python
python runtime/src/mcp_server/main.py

# Or with makefile
make run-server
```

### Using MCP CLI

```bash
# Chat with the generic server
uv run mcp-cli chat --server generic

# List available tools
uv run mcp-cli list-tools
```

## Development

### Running Tests

```bash
# Run all tests
make test

# Run specific test suite
pytest runtime/tests/
```

### Code Quality

```bash
# Run linters and formatters
make lint
make format
```

## Project Structure

```
mcp-host/
│
├── common/           # Shared utilities and decorators
│   └── src/
│
├── runtime/          # Core runtime components
│   └── src/
│       └── mcp_server/
│           ├── main.py
│           ├── config_loader.py
│           ├── logging_config.py
│           └── server_registry.py
│
├── servers/          # Individual server implementations
│   ├── time_server/
│   └── echo_server/
│
├── tests/            # Test suites
│
├── requirements.txt
├── requirements-dev.txt
└── pyproject.toml
```

## Configuration

Configuration is managed through YAML files. The default configuration is located at `config.yaml` in the project root.

Example configuration:
```yaml
host:
  name: generic-mcp
  log_level: INFO

core:
  common: common/src
  runtime: runtime/src

mcp_servers:
  time_server:
    location: servers/mcp_time_server/src
    enabled: true
    tools:
      module: time_server.tools
      enabled: true

auto_discover: true
```

## Extending the Framework

### Adding New Servers

1. Create a new directory under `servers/`
2. Implement your server tools using the `@tool` decorator
3. Configure the server in `config.yaml`

### Tool Registration

Use the `@tool` decorator to register new tools:

```python
from common.mcp_tool_decorator import tool

@tool(name="my_tool", description="A custom tool")
def my_custom_tool(arg1: str, arg2: int) -> dict:
    # Tool implementation
    return {"result": f"Processed {arg1} with {arg2}"}
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact
Project Link: [https://github.com/chrishayuk/mcp-host](https://github.com/chrishayuk/mcp-host)
```