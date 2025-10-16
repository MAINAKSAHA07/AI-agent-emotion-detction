#!/bin/bash

# AWS Deployment Script for Emotion Detection App
# This script deploys the app to AWS using various services

set -e

echo "🚀 AWS Emotion Detection App Deployment"
echo "======================================"

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Please install it first:"
    echo "   pip install awscli"
    echo "   aws configure"
    exit 1
fi

# Check if AWS credentials are configured
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS credentials not configured. Please run:"
    echo "   aws configure"
    exit 1
fi

echo "✅ AWS CLI configured"

# Get deployment option
echo ""
echo "Choose deployment option:"
echo "1) AWS Lambda (Serverless)"
echo "2) AWS Elastic Beanstalk (Container)"
echo "3) AWS EC2 (Virtual Machine)"
echo "4) AWS ECS (Container Service)"
echo "5) Local Development (SQLite)"

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo "🚀 Deploying to AWS Lambda..."
        ./aws/lambda_deploy.sh
        ;;
    2)
        echo "🚀 Deploying to AWS Elastic Beanstalk..."
        ./aws/eb_deploy.sh
        ;;
    3)
        echo "🚀 Deploying to AWS EC2..."
        ./aws/ec2_deploy.sh
        ;;
    4)
        echo "🚀 Deploying to AWS ECS..."
        ./aws/ecs_deploy.sh
        ;;
    5)
        echo "🚀 Starting local development..."
        ./scripts/setup.sh
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo "✅ Deployment completed!"
