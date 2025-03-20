# runtime/src/mcp_server/main.py
import asyncio

# imports
from runtime.src.mcp_server.config import load_config, configure_logging
from runtime.src.mcp_server.server import ServerRegistry, serve, get_project_root
from runtime.src.mcp_server.logging_config import logger

def main() -> None:
    # Determine the project root directory
    project_root = get_project_root()
    
    # Load configuration and configure logging (using the common logger)
    config = load_config(project_root)
    configure_logging(config)
    
    # Set up the server registry and load server components
    registry = ServerRegistry(project_root, config)
    registry.load_server_components()
    
    try:
        # Run the asynchronous server
        asyncio.run(serve())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)

if __name__ == "__main__":
    # call it
    main()
