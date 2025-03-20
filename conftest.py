# conftest.py (project root)
import os
import sys

# Set an environment variable to disable bootstrapping in modules that check for it.
os.environ["NO_BOOTSTRAP"] = "1"

# Determine the project root directory.
project_root = os.path.abspath(os.path.dirname(__file__))

# Define the absolute paths to your source directories.
# We use the parent directory of the package directories to ensure proper imports
common_src = os.path.join(project_root, "common", "src")
runtime_src = os.path.join(project_root, "runtime", "src")
time_server_src = os.path.join(project_root, "servers", "time_server", "src")
echo_server_src = os.path.join(project_root, "servers", "mcp_echo_server", "src")

# Insert them into sys.path (if they're not already present).
# We reverse the order to ensure the first path is highest priority
paths = [common_src, runtime_src, time_server_src, echo_server_src]
for path in reversed(paths):
    if os.path.exists(path) and path not in sys.path:
        sys.path.insert(0, path)

# Print sys.path for debugging (commented out for production use)
# print("Python path for imports:", "\n".join(sys.path))