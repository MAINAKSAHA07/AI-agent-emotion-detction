#!/bin/bash

# EC2 Setup Script for Emotion Detection App
# Installs all system dependencies on Ubuntu 22.04

set -e

echo "🚀 Setting up EC2 instance for Emotion Detection App..."

# Update system
echo "🔄 Updating system packages..."
sudo apt update -y
sudo apt install -y git curl wget unzip

# Install Python 3.11
echo "🐍 Installing Python 3.11..."
sudo apt install -y software-properties-common
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.11 python3.11-venv

# Install PostgreSQL
echo "🐘 Installing PostgreSQL..."
sudo apt install -y postgresql postgresql-contrib
sudo systemctl enable postgresql
sudo systemctl start postgresql

# Install Node.js 18
echo "📦 Installing Node.js 18..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install Nginx
echo "🌐 Installing Nginx..."
sudo apt install -y nginx

# Install AWS CLI
echo "☁️ Installing AWS CLI..."
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
rm -rf aws awscliv2.zip

# Create application directory
echo "📁 Creating application directory..."
sudo mkdir -p /var/www/emotion-detection
sudo chown ubuntu:ubuntu /var/www/emotion-detection

# Create app directory in home
mkdir -p ~/app
cd ~/app

echo "✅ System dependencies installed successfully!"
echo ""
echo "Next steps:"
echo "1. Configure PostgreSQL database"
echo "2. Upload application code"
echo "3. Setup Python environment"
echo "4. Configure Nginx"
echo "5. Start services"
echo ""
echo "Run: sudo ./deployment/postgresql_setup.sh"
