#!/bin/bash

# Emotion Detection App Startup Script
# Choose between React frontend or Streamlit MVP

echo "🧠 Emotion Detection App Startup"
echo "Choose your frontend option:"
echo "1) React Frontend (Full-featured)"
echo "2) Streamlit MVP (Quick demo)"
echo "3) Docker Compose (All services)"
echo "4) Backend only (API only)"

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo "🚀 Starting React frontend..."
        echo "Make sure to run the backend first:"
        echo "python -m uvicorn backend.main:app --reload"
        echo ""
        echo "Then start the frontend:"
        echo "cd frontend && npm start"
        ;;
    2)
        echo "🚀 Starting Streamlit MVP..."
        echo "Make sure the backend is running first:"
        echo "python -m uvicorn backend.main:app --reload"
        echo ""
        echo "Then start Streamlit:"
        echo "streamlit run streamlit_app.py"
        ;;
    3)
        echo "🚀 Starting with Docker Compose..."
        docker-compose up -d
        echo "✅ Services started!"
        echo "Frontend: http://localhost:3000"
        echo "Backend: http://localhost:8000"
        echo "API Docs: http://localhost:8000/docs"
        ;;
    4)
        echo "🚀 Starting backend only..."
        python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac
