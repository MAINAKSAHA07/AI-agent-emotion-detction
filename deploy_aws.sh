#!/bin/bash

# AWS EC2 Deployment Script for Updated Model
# Deploys the latest changes to the EC2 server

set -e

echo "🚀 Deploying updated model to AWS EC2..."

# Server details
SERVER_IP="3.144.160.219"
SSH_KEY="./emotion.pem"
SERVER_USER="ubuntu"
APP_DIR="/home/ubuntu/app"

echo "📤 Uploading updated files to EC2..."
scp -i "$SSH_KEY" agent/state_agent.py "$SERVER_USER@$SERVER_IP:$APP_DIR/agent/"
scp -i "$SSH_KEY" models/database.py "$SERVER_USER@$SERVER_IP:$APP_DIR/models/"

echo "🔄 Restarting backend service on EC2..."
ssh -i "$SSH_KEY" "$SERVER_USER@$SERVER_IP" "sudo systemctl restart emotion-detection"

echo "✅ Deployment completed successfully!"
echo "🎉 AWS deployment completed!"
echo "🌐 Your updated app is now running at:"
echo "   Frontend: https://aiemotion.netlify.app/"
echo "   API: http://$SERVER_IP:8000"
echo ""
echo "🧪 Test the updated model:"
echo "   curl -X POST 'http://$SERVER_IP:8000/analyze' -H 'Content-Type: application/json' -d '{\"text\": \"I am testing the updated model\", \"session_id\": \"test_update\"}'"