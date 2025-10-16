#!/bin/bash

# Emotion Detection App Setup Script
# This script sets up the development environment

set -e

echo "🚀 Setting up Emotion Detection App..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed."
    exit 1
fi

# Check if Docker is installed (optional)
if ! command -v docker &> /dev/null; then
    echo "⚠️  Docker not found. Docker is recommended for easy deployment."
fi

echo "✅ Prerequisites check passed"

# Create virtual environment
echo "📦 Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Setup frontend
echo "📦 Setting up frontend..."
cd frontend
npm install
cd ..

# Create environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating environment file..."
    cp env.example .env
    echo "⚠️  Please edit .env file with your AWS credentials"
fi

# Create logs directory
mkdir -p logs

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your AWS credentials"
echo "2. Start the backend: python -m uvicorn backend.main:app --reload"
echo "3. Start the frontend: cd frontend && npm start"
echo "4. Or use Docker: docker-compose up -d"
echo ""
echo "🌐 App will be available at:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
