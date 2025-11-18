#!/bin/bash

# Money Marketing Tool - Setup Script

set -e

echo "================================"
echo "Money Marketing Tool - Setup"
echo "================================"
echo ""

# Check for required commands
command -v docker >/dev/null 2>&1 || { echo "❌ Docker is required but not installed. Aborting." >&2; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "❌ Docker Compose is required but not installed. Aborting." >&2; exit 1; }

echo "✓ Docker and Docker Compose are installed"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env file and add your API keys before continuing!"
    echo ""
    read -p "Press Enter to continue after updating .env file..."
fi

echo "Starting services with Docker Compose..."
docker-compose up -d

echo ""
echo "Waiting for database to be ready..."
sleep 5

echo ""
echo "Initializing database..."
docker-compose exec -T backend python scripts/init_db.py

echo ""
echo "================================"
echo "✓ Setup Complete!"
echo "================================"
echo ""
echo "Services are running:"
echo "  - Frontend: http://localhost:3000"
echo "  - Backend API: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo "  - Flower (Celery): http://localhost:5555"
echo ""
echo "To create an admin user, run:"
echo "  docker-compose exec backend python scripts/create_admin.py"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f"
echo ""
echo "To stop services:"
echo "  docker-compose down"
echo ""
