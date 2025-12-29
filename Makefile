.PHONY: help install dev test clean run-api run-streamlit run-gui run-demo docker-build docker-up docker-down lint format

# Default target
help:
	@echo "AEON Development Commands"
	@echo "========================="
	@echo "install       - Install dependencies"
	@echo "dev           - Install dev dependencies"
	@echo "test          - Run tests"
	@echo "clean         - Clean build artifacts"
	@echo "run-api       - Run API server"
	@echo "run-streamlit - Run Streamlit dashboard"
	@echo "run-gui       - Run Tkinter GUI"
	@echo "run-demo      - Run demonstration"
	@echo "docker-build  - Build Docker images"
	@echo "docker-up     - Start Docker containers"
	@echo "docker-down   - Stop Docker containers"
	@echo "lint          - Run linters"
	@echo "format        - Format code with black"

# Installation
install:
	pip install -r requirements.txt
	pip install -e .

dev:
	pip install -r requirements.txt
	pip install -e ".[dev,llm]"

# Testing
test:
	pytest tests/ -v --cov=aeon --cov-report=html

test-quick:
	pytest tests/ -v

# Cleaning
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +

# Running
run-api:
	python run.py api

run-streamlit:
	python run.py streamlit

run-gui:
	python run.py gui

run-demo:
	python run.py demo

# Docker
docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

# Code Quality
lint:
	flake8 aeon/ --max-line-length=100
	mypy aeon/ --ignore-missing-imports

format:
	black aeon/ tests/ --line-length=100

# Development
watch-api:
	uvicorn aeon.api.main:app --reload --host 127.0.0.1 --port 8000
