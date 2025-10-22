#!/bin/bash

# Netlify Deployment Script for Emotion Detection App
echo "🚀 Deploying Emotion Detection App to Netlify..."

# Navigate to frontend directory
cd frontend

# Build with correct API URL
echo "🏗️ Building for production..."
REACT_APP_API_URL=http://3.144.160.219:8000 npm run build

# Check if Netlify CLI is installed
if ! command -v netlify &> /dev/null; then
    echo "📦 Installing Netlify CLI..."
    npm install -g netlify-cli
fi

# Deploy to Netlify
echo "🌐 Deploying to Netlify..."
netlify deploy --prod --dir=build

echo "✅ Deployment completed!"
echo ""
echo "🌐 Your app is now live on Netlify!"
echo "📊 Backend API: http://3.144.160.219:8000"
echo ""
echo "🔧 Environment Variables for Netlify:"
echo "   REACT_APP_API_URL = http://3.144.160.219:8000"