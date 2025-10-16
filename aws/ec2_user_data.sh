#!/bin/bash

# EC2 User Data Script
# Installs and configures the emotion detection app on EC2

# Update system
yum update -y

# Install Python 3.11
yum install -y python3.11 python3.11-pip git

# Install Node.js
curl -fsSL https://rpm.nodesource.com/setup_18.x | bash -
yum install -y nodejs

# Clone and setup application
cd /home/ec2-user
git clone <your-repo-url> emotion-detection-app
cd emotion-detection-app

# Setup Python environment
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup frontend
cd frontend
npm install
npm run build
cd ..

# Create systemd service
cat > /etc/systemd/system/emotion-detection.service << 'EOF'
[Unit]
Description=Emotion Detection App
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/emotion-detection-app
Environment=PATH=/home/ec2-user/emotion-detection-app/venv/bin
ExecStart=/home/ec2-user/emotion-detection-app/venv/bin/python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Start service
systemctl daemon-reload
systemctl enable emotion-detection
systemctl start emotion-detection

# Configure nginx (optional)
yum install -y nginx
systemctl enable nginx
systemctl start nginx
