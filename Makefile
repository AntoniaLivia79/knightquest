.PHONY: test lint run

# Set up virtual environment
venv:
	python3 -m venv venv
	@echo "Virtual environment created. Now activate it using 'source venv/bin/activate'"

# Install project dependencies
install:
	@pip install -r requirements.txt

# Run unit tests
test:
	@cd src && python3 -m pytest

# Run unit tests with coverage
test-coverage:
	@cd src && coverage run -m pytest && coverage report -m

# Run unit tests with tox
test-tox:
	@tox -e test

# Run linting with flake8
lint:
	@flake8 src

# Run the project
run:
	cd src && python3 Knightquest.py

# Clean up generated files
clean:
	@rm -rf __pycache__ .pytest_cache ./src/tests/.pytest_cache .coverage ./src/.coverage .tox

# Remove the virtual environment
clean-venv:
	@rm -rf venv

# Run the project within the virtual environment
run-venv: venv
	. venv/bin/activate && $(MAKE) run

# Show this help message
help:
	@echo "Available targets:"
	@echo "  venv           Create a virtual environment"
	@echo "  install        Install project dependencies"
	@echo "  test           Run unit tests"
	@echo "  test-coverage  Run unit tests with coverage"
	@echo "  test-tox       Run tox automation for unit tests"
	@echo "  lint           Run linting with flake8"
	@echo "  run            Run the project"
	@echo "  clean          Clean up generated files"
	@echo "  clean-venv     Remove the virtual environment"
	@echo "  run-venv       Run the project within the virtual environment"
	@echo "  help           Show this help message"
