#!/bin/bash

# Upload Code Script for Emotion Detection App
# Uploads application code to EC2 instance

set -e

EC2_IP="3.144.160.219"
KEY_FILE="emotion.pem"

echo "🚀 Uploading code to EC2 instance: $EC2_IP"

# Check if SSH key exists
if [ ! -f "$KEY_FILE" ]; then
    echo "❌ SSH key file not found: $KEY_FILE"
    exit 1
fi

# Set correct permissions for key file
chmod 400 "$KEY_FILE"

# Create app directory on EC2
echo "📁 Creating application directory on EC2..."
ssh -i "$KEY_FILE" ubuntu@$EC2_IP "mkdir -p ~/app"

# Upload backend code
echo "📤 Uploading backend code..."
scp -i "$KEY_FILE" -r agent/ ubuntu@$EC2_IP:~/app/
scp -i "$KEY_FILE" -r models/ ubuntu@$EC2_IP:~/app/
scp -i "$KEY_FILE" -r services/ ubuntu@$EC2_IP:~/app/
scp -i "$KEY_FILE" -r backend/ ubuntu@$EC2_IP:~/app/
scp -i "$KEY_FILE" requirements.txt ubuntu@$EC2_IP:~/app/
scp -i "$KEY_FILE" test_aws.py ubuntu@$EC2_IP:~/app/

# Upload frontend code
echo "📤 Uploading frontend code..."
scp -i "$KEY_FILE" -r frontend/ ubuntu@$EC2_IP:~/app/

# Upload deployment scripts
echo "📤 Uploading deployment scripts..."
scp -i "$KEY_FILE" -r deployment/ ubuntu@$EC2_IP:~/app/

# Set permissions
echo "🔧 Setting file permissions..."
ssh -i "$KEY_FILE" ubuntu@$EC2_IP "chmod +x ~/app/deployment/*.sh"

echo "✅ Code upload completed successfully!"
echo ""
echo "Next steps on EC2:"
echo "1. ssh -i emotion.pem ubuntu@3.144.160.219"
echo "2. cd ~/app"
echo "3. ./deployment/setup_app.sh"
echo ""
echo "Or run: ssh -i emotion.pem ubuntu@3.144.160.219 'cd ~/app && ./deployment/setup_app.sh'"
