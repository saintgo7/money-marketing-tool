#!/bin/bash

# Money Marketing Tool - Development Setup Script

set -e

echo "================================"
echo "Money Marketing Tool - Dev Setup"
echo "================================"
echo ""

# Backend setup
echo "Setting up backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install -r requirements.txt

if [ ! -f ".env" ]; then
    echo "Creating backend .env file..."
    cp .env.example .env
fi

cd ..

# Frontend setup
echo ""
echo "Setting up frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
fi

if [ ! -f ".env.local" ]; then
    echo "Creating frontend .env.local file..."
    cp .env.example .env.local
fi

cd ..

echo ""
echo "================================"
echo "✓ Development Setup Complete!"
echo "================================"
echo ""
echo "To start development:"
echo ""
echo "Backend:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  uvicorn src.main:app --reload"
echo ""
echo "Frontend:"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Celery Worker:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  celery -A src.scheduler.auto_scheduler:celery_app worker --loglevel=info"
echo ""
