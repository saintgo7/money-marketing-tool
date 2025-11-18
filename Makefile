.PHONY: help install dev build up down logs clean test

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

dev: ## Run development servers
	docker-compose up

build: ## Build Docker images
	docker-compose build

up: ## Start all services
	docker-compose up -d

down: ## Stop all services
	docker-compose down

logs: ## View logs
	docker-compose logs -f

clean: ## Clean up containers, volumes, and images
	docker-compose down -v
	docker system prune -f

test-backend: ## Run backend tests
	cd backend && pytest tests/ -v --cov=src

test-frontend: ## Run frontend tests
	cd frontend && npm test

lint-backend: ## Lint backend code
	cd backend && black src/ && isort src/

lint-frontend: ## Lint frontend code
	cd frontend && npm run lint

db-init: ## Initialize database
	docker-compose exec backend python -c "from src.models.database import init_db; init_db()"

db-migrate: ## Run database migrations
	docker-compose exec backend alembic upgrade head

db-shell: ## Open database shell
	docker-compose exec postgres psql -U marketing_user -d marketing_db

redis-cli: ## Open Redis CLI
	docker-compose exec redis redis-cli

restart: down up ## Restart all services
