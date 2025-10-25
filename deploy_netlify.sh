#!/bin/bash

# Netlify Deployment Script for Updated Emotion Detection App
# Deploys frontend with conversation history and improved agent features

echo "🚀 Deploying Updated Emotion Detection App to Netlify..."

# Check if we're in the right directory
if [ ! -d "frontend" ]; then
    echo "❌ Frontend directory not found. Please run from project root."
    exit 1
fi

# Navigate to frontend directory
cd frontend

# Check if package.json exists
if [ ! -f "package.json" ]; then
    echo "❌ package.json not found in frontend directory"
    exit 1
fi

# Install/update dependencies
echo "📦 Installing/updating frontend dependencies..."
npm install

# Build with correct API URL and updated features
echo "🏗️ Building for production with updated features..."
echo "  🔧 API URL: /api (using Netlify proxy)"
echo "  🆕 Features: Conversation history, enhanced error handling, improved CORS"

REACT_APP_API_URL=/api npm run build

# Check if build was successful
if [ ! -d "build" ]; then
    echo "❌ Build failed - build directory not found"
    exit 1
fi

echo "✅ Build completed successfully!"

# Check if Netlify CLI is installed
if ! command -v netlify &> /dev/null; then
    echo "📦 Installing Netlify CLI..."
    npm install -g netlify-cli
fi

# Deploy to Netlify
echo "🌐 Deploying to Netlify..."
netlify deploy --prod --dir=build

echo ""
echo "✅ Netlify deployment completed!"
echo ""
echo "🌐 Your updated app is now live on Netlify!"
echo "   Frontend: https://aiemotion.netlify.app/"
echo "   Backend API: http://3.144.160.219:8000"
echo ""
echo "🆕 New Frontend Features:"
echo "   ✅ Conversation history support in agent interface"
echo "   ✅ Enhanced error handling and user feedback"
echo "   ✅ Improved CORS configuration for production"
echo "   ✅ Better session management and context awareness"
echo ""
echo "🧪 Test the updated frontend:"
echo "   1. Visit: https://aiemotion.netlify.app/"
echo "   2. Try the Agent mode for conversation history"
echo "   3. Test emotion analysis with context"
echo ""
echo "🔧 Environment Variables for Netlify:"
echo "   REACT_APP_API_URL = http://3.144.160.219:8000"
echo ""
echo "📋 Monitor deployment:"
echo "   netlify status"
echo "   netlify logs"