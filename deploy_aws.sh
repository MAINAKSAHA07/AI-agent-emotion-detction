#!/bin/bash

# Simple AWS EC2 Deployment Script
# Deploys all files with minimal output

set -e

# Configuration
SERVER_IP="3.144.160.219"
SSH_KEY="./emotion.pem"
SERVER_USER="ubuntu"
APP_DIR="/home/ubuntu/app"

echo "🚀 Deploying to AWS EC2..."

# Check SSH key
if [ ! -f "$SSH_KEY" ]; then
    echo "❌ SSH key not found: $SSH_KEY"
    exit 1
fi

# Upload all files
echo "📤 Uploading files..."
scp -i "$SSH_KEY" -q agent/state_agent.py "$SERVER_USER@$SERVER_IP:$APP_DIR/agent/"
scp -i "$SSH_KEY" -q backend/main.py "$SERVER_USER@$SERVER_IP:$APP_DIR/backend/"
scp -i "$SSH_KEY" -q models/database.py "$SERVER_USER@$SERVER_IP:$APP_DIR/models/"
scp -i "$SSH_KEY" -q services/database_service.py "$SERVER_USER@$SERVER_IP:$APP_DIR/services/"
scp -i "$SSH_KEY" -q requirements.txt "$SERVER_USER@$SERVER_IP:$APP_DIR/"

# Deploy frontend if exists
if [ -d "frontend/build" ]; then
    echo "📁 Deploying frontend..."
    ssh -i "$SSH_KEY" -q "$SERVER_USER@$SERVER_IP" "sudo mkdir -p /var/www/html"
    scp -i "$SSH_KEY" -q -r frontend/build/* "$SERVER_USER@$SERVER_IP:/tmp/frontend_build/"
    ssh -i "$SSH_KEY" -q "$SERVER_USER@$SERVER_IP" "sudo cp -r /tmp/frontend_build/* /var/www/html/ && sudo chown -R www-data:www-data /var/www/html"
fi

# Update dependencies and restart service
echo "🔧 Updating service..."
ssh -i "$SSH_KEY" -q "$SERVER_USER@$SERVER_IP" "
    cd $APP_DIR
    source venv/bin/activate 2>/dev/null || python3 -m venv venv && source venv/bin/activate
    pip install -q -r requirements.txt
    sudo systemctl restart emotion-detection
    sleep 3
"

# Test deployment
echo "🧪 Testing deployment..."
if curl -s -f "http://$SERVER_IP:8000/health" > /dev/null; then
    echo "✅ Deployment successful!"
    echo "🌐 App running at: http://$SERVER_IP:8000"
    echo "🧠 Enhanced agent with conversation history deployed!"
else
    echo "⚠️  Service may still be starting..."
    echo "🔍 Check status: ssh -i $SSH_KEY $SERVER_USER@$SERVER_IP 'sudo systemctl status emotion-detection'"
fi