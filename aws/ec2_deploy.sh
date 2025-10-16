#!/bin/bash

# AWS EC2 Deployment Script
# Deploys the emotion detection app to EC2 instance

set -e

echo "🚀 Deploying to AWS EC2..."

# Create EC2 instance
echo "🖥️  Creating EC2 instance..."
INSTANCE_ID=$(aws ec2 run-instances \
    --image-id ami-0c02fb55956c7d316 \
    --instance-type t3.micro \
    --key-name your-key-pair \
    --security-group-ids sg-12345678 \
    --user-data file://aws/ec2_user_data.sh \
    --query 'Instances[0].InstanceId' \
    --output text)

echo "✅ EC2 instance created: $INSTANCE_ID"

# Wait for instance to be running
echo "⏳ Waiting for instance to be running..."
aws ec2 wait instance-running --instance-ids $INSTANCE_ID

# Get public IP
PUBLIC_IP=$(aws ec2 describe-instances \
    --instance-ids $INSTANCE_ID \
    --query 'Reservations[0].Instances[0].PublicIpAddress' \
    --output text)

echo "🌐 Instance public IP: $PUBLIC_IP"
echo "🔗 Application will be available at: http://$PUBLIC_IP:8000"

echo "✅ EC2 deployment completed!"
