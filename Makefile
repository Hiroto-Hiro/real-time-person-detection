.PHONY: help app app-down app-build app-restart app-logs app-shell clean build-size install run run-bot lint format check

help:
	@echo Available commands:
	@echo   app               Run the production application
	@echo   app-build         Build the production Docker image  
	@echo   app-down          Stop the production application
	@echo   app-logs          Show production application logs
	@echo   app-restart       Restart the production application
	@echo   app-shell         Get a shell inside the production container
	@echo   build-size        Show Docker image sizes
	@echo   clean             Remove all containers and images
	@echo   install           Install dependencies locally
	@echo   run               Run locally without Docker
	@echo   run-bot           Run bot locally without Docker
	@echo   lint              Run code linting with ruff
	@echo   format            Format code with black
	@echo   check             Run all code quality checks

app:
	docker compose -f docker-compose.yml up -d

app-down:
	docker compose -f docker-compose.yml down

app-build:
	docker compose -f docker-compose.yml build

app-restart:
	docker compose -f docker-compose.yml restart

app-logs:
	docker compose -f docker-compose.yml logs -f cam-analyser

app-shell:
	docker compose -f docker-compose.yml exec cam-analyser /bin/bash

install:
	uv sync

run:
	uv run python -m src.main

run-bot:
	uv run python -m src.bot.main

lint:
	uv run ruff check

format:
	uv run black .

check:
	@echo "🔍 Running code quality checks..."
	@echo "1. Running Ruff linter..."
	uv run ruff check
	@echo "2. Checking Black formatting..."
	uv run black . --check
	@echo "✅ All checks passed!"

clean:
	docker compose -f docker-compose.yml down --volumes --remove-orphans
	docker system prune -f

build-size:
	@echo Image sizes:
	@docker images cam-analyser* 2>nul || echo No cam-analyser images found
