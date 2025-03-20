# conftest.py (project root)
import os
import sys

# Set an environment variable to disable bootstrapping in modules that check for it.
os.environ["NO_BOOTSTRAP"] = "1"

# Determine the project root directory.
project_root = os.path.abspath(os.path.dirname(__file__))

# Define the absolute paths to your source directories.
common_src = os.path.join(project_root, "common", "src")
runtime_src = os.path.join(project_root, "runtime", "src")
time_server_src = os.path.join(project_root, "servers", "time_server", "src")
echo_server_src = os.path.join(project_root, "servers", "echo_server", "src")

# Insert them into sys.path (if they’re not already present).
for path in (common_src, runtime_src, time_server_src, echo_server_src):
    if path not in sys.path:
        sys.path.insert(0, path)

# (Optional) Print sys.path for debugging:
# print("sys.path:", sys.path)
