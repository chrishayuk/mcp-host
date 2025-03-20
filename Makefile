# Enhanced clean and build targets for your Makefile

# Thoroughly clean the project, removing all build artifacts and virtual environments
clean-all:
	@echo "Performing complete cleanup..."
	rm -rf .venv
	find . -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -delete
	find . -name ".coverage" -delete
	find . -name ".pytest_cache" -exec rm -rf {} +
	@echo "Complete cleanup done."

# Remove python egg-info directories and cached bytecode
clean:
	@echo "Cleaning build artifacts and caches..."
	find . -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "__pycache__" -exec rm -rf {} + | wc -l | xargs -I {} echo "Files removed: {}"

# Setup a fresh virtual environment
venv:
	@echo "Setting up a fresh virtual environment..."
	uv venv .venv

# Install the project in development mode
install: clean
	@echo "Installing project in development mode..."
	uv pip install -e .
	@echo "Installation complete."

# Rebuild the entire project from scratch
rebuild: clean-all venv install
	@echo "Project rebuilt successfully."

# Run the server
run-server:
	@echo "Running the server..."
	PYTHONPATH=. uv run python runtime/src/mcp_server/main.py

# Run tests
test:
	@echo "Running tests..."
	uv run pytest

# Check project structure and package integrity
check-structure:
	@echo "Checking project structure..."
	@echo "Package directories:"
	find . -name "__init__.py" | sort
	@echo "\nPython modules:"
	find . -name "*.py" | grep -v "__pycache__" | sort
	@echo "\nInstalled packages:"
	uv pip list | grep -E 'time-server|echo-server|mcp-host'