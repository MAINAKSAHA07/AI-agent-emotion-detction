#!/bin/bash

# Application Setup Script for Emotion Detection App
# Sets up Python environment, installs dependencies, and configures services

set -e

echo "🚀 Setting up Emotion Detection Application..."

# Navigate to app directory
cd ~/app

# Create Python virtual environment
echo "🐍 Creating Python virtual environment..."
python3.11 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Test AWS connection
echo "☁️ Testing AWS Comprehend connection..."
python test_aws.py

# Test database connection
echo "🐘 Testing database connection..."
python -c "
from models.database import create_tables, engine
from sqlalchemy import text
import os
from dotenv import load_dotenv

load_dotenv()

try:
    # Create tables
    create_tables()
    print('✅ Database tables created successfully')
    
    # Test connection
    with engine.connect() as conn:
        result = conn.execute(text('SELECT 1'))
        print('✅ Database connection successful')
        
except Exception as e:
    print(f'❌ Database error: {e}')
    exit(1)
"

# Build frontend
echo "🎨 Building React frontend..."
cd frontend
npm install
npm run build

# Copy build to web directory
echo "📁 Copying frontend build to web directory..."
sudo cp -r build/* /var/www/emotion-detection/
sudo chown -R www-data:www-data /var/www/emotion-detection
sudo chmod -R 755 /var/www/emotion-detection

cd ~/app

# Create systemd service
echo "⚙️ Creating systemd service..."
sudo tee /etc/systemd/system/emotion-detection.service > /dev/null << EOF
[Unit]
Description=Emotion Detection Backend API
After=network.target postgresql.service

[Service]
Type=simple
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/app
Environment="PATH=/home/ubuntu/app/venv/bin"
EnvironmentFile=/home/ubuntu/app/.env
ExecStart=/home/ubuntu/app/venv/bin/python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Configure Nginx
echo "🌐 Configuring Nginx..."
sudo tee /etc/nginx/sites-available/emotion-detection > /dev/null << 'EOF'
server {
    listen 80;
    server_name _;
    
    # Serve React frontend
    location / {
        root /var/www/emotion-detection;
        index index.html;
        try_files $uri $uri/ /index.html;
        
        # Enable gzip compression
        gzip on;
        gzip_vary on;
        gzip_min_length 1024;
        gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
    }
    
    # Proxy API requests to backend
    location /analyze {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
    
    location /history/ {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
    
    location /trends/ {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
    
    location /sessions {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
    
    location /health {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Enable Nginx site
sudo ln -sf /etc/nginx/sites-available/emotion-detection /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
echo "🧪 Testing Nginx configuration..."
sudo nginx -t

# Start services
echo "🚀 Starting all services..."
sudo systemctl daemon-reload
sudo systemctl enable postgresql emotion-detection nginx
sudo systemctl start postgresql
sudo systemctl start emotion-detection
sudo systemctl start nginx

# Check service status
echo "📊 Checking service status..."
sudo systemctl status postgresql --no-pager
sudo systemctl status emotion-detection --no-pager
sudo systemctl status nginx --no-pager

echo "✅ Application setup completed successfully!"
echo ""
echo "🌐 Application is now running at:"
echo "   Frontend: http://3.144.160.219"
echo "   API: http://3.144.160.219:8000"
echo ""
echo "📋 Service Management:"
echo "   View logs: sudo journalctl -u emotion-detection -f"
echo "   Restart app: sudo systemctl restart emotion-detection"
echo "   Restart nginx: sudo systemctl restart nginx"
echo "   Restart postgresql: sudo systemctl restart postgresql"
echo ""
echo "🧪 Test the deployment:"
echo "   curl http://3.144.160.219/health"
