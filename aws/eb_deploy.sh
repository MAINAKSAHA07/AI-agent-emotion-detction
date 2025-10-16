#!/bin/bash

# AWS Elastic Beanstalk Deployment Script
# Deploys the emotion detection app to Elastic Beanstalk

set -e

echo "🚀 Deploying to AWS Elastic Beanstalk..."

# Check if EB CLI is installed
if ! command -v eb &> /dev/null; then
    echo "📦 Installing EB CLI..."
    pip install awsebcli
fi

# Initialize EB application
if [ ! -f ".elasticbeanstalk/config.yml" ]; then
    echo "🔧 Initializing Elastic Beanstalk application..."
    eb init emotion-detection-app --platform python-3.11 --region us-east-1
fi

# Create application version
echo "📦 Creating application version..."
eb create production --instance-type t3.micro --single-instance

# Set environment variables
echo "🔧 Setting environment variables..."
eb setenv AWS_DEFAULT_REGION=us-east-1 USE_DYNAMODB=true

# Deploy
echo "🚀 Deploying application..."
eb deploy

echo "✅ Elastic Beanstalk deployment completed!"
echo "🌐 Application URL:"
eb status | grep "CNAME"
