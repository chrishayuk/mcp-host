.PHONY: clean install test

clean:
	@echo "Cleaning build artifacts and caches..."
	-find . -name "*.egg-info" -exec rm -rf {} +
	@rm -rf build dist
	-find . -type d -name "__pycache__" -exec rm -rf {} +
	@pip cache purge

install:
	@echo "Installing project in editable mode..."
	uv run pip install -e .

test:
	@echo "Running tests..."
	uv run pytest
