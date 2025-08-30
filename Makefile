# Makefile for NessHash

# Variables
PYTHON := python3
PIP := pip3
DOCKER := docker
DOCKER_COMPOSE := docker-compose
PYTEST := pytest
PRE_COMMIT := pre-commit

# Default target
.DEFAULT_GOAL := help

# Help target to show all available commands
help:
	@echo "NessHash - Development Commands"
	@echo ""
	@echo "Available targets:"
	@echo "  help           Show this help message"
	@echo "  setup          Set up development environment"
	@echo "  test           Run tests"
	@echo "  lint           Run all linters"
	@echo "  format         Format code"
	@echo "  check-types    Run type checking"
	@echo "  docs           Build documentation"
	@echo "  serve-docs     Serve documentation locally"
	@echo "  clean          Clean up temporary files"
	@echo "  docker-build   Build Docker images"
	@echo "  docker-up      Start services with Docker Compose"
	@echo "  docker-down    Stop and remove containers"

# Set up development environment
setup:
	$(PIP) install -r requirements.txt
	$(PIP) install -e .
	$(PIP) install pre-commit
	pre-commit install

# Run tests
test:
	$(PYTEST) tests/ -v --cov=src --cov-report=term-missing

# Run all linters
lint:
	pre-commit run --all-files

# Format code
format:
	black .
	isort .

# Run type checking
check-types:
	mypy .

# Build documentation
docs:
	mkdocs build --clean

# Serve documentation locally
serve-docs:
	mkdocs serve

# Clean up temporary files
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".mypy_cache" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	rm -rf .coverage htmlcov/ build/ dist/ *.egg-info/

# Docker commands
docker-build:
	$(DOCKER_COMPOSE) build

docker-up:
	$(DOCKER_COMPOSE) up -d

docker-down:
	$(DOCKER_COMPOSE) down

.PHONY: help setup test lint format check-types docs serve-docs clean docker-build docker-up docker-down
