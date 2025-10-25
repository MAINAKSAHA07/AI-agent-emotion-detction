# 🧠 AI-Powered Emotion Detection & Intelligence Platform

A sophisticated web application that leverages **advanced AI technology** to detect and analyze emotions from text input, featuring an **intelligent conversational agent** that provides adaptive emotional support and insights.

## 🎯 Core Features

### 🧠 Intelligent Emotion Analysis

- **Advanced AI Processing**: Real-time emotion detection using cutting-edge AI technology
- **Multi-dimensional Analysis**: Sentiment, valence, arousal, and confidence scoring
- **Context-Aware Processing**: Considers conversation history for enhanced accuracy
- **Adaptive Response Generation**: Personalized responses based on emotional state

### 🤖 Conversational AI Agent

- **Interactive Chat Interface**: Natural conversation flow with emotional intelligence
- **Contextual Understanding**: Maintains conversation history for better responses
- **Emotional Support**: Provides empathetic and supportive responses
- **Dual Interface Modes**: Agent chat and traditional analysis views

### 📊 Session Management & Analytics

- **Session Tracking**: Persistent user sessions with emotional history
- **Trend Analysis**: Visual representation of emotional patterns over time
- **Historical Insights**: Complete analysis history with detailed metrics
- **Data Export**: Comprehensive session data for further analysis

### 🎨 Modern User Interface

- **Responsive Design**: Optimized for desktop and mobile devices
- **Real-time Updates**: Live emotion analysis with instant feedback
- **Interactive Dashboards**: Rich visualizations and trend displays
- **Accessibility**: User-friendly interface with clear emotional indicators

### 🏗️ Enterprise-Grade Architecture

- **Multi-Database Support**: SQLite, PostgreSQL, and DynamoDB compatibility
- **Cloud-Native**: Built for AWS with Lambda, EC2, and Elastic Beanstalk support
- **Scalable Infrastructure**: Handles high-volume emotion analysis requests
- **Security-First**: Secure API endpoints with proper authentication

## 🚀 Current Deployment Status

### ✅ Production Environment

- **Frontend**: Deployed on Netlify with custom domain
- **Backend**: Running on AWS EC2 with advanced AI integration
- **Database**: PostgreSQL configured and operational
- **API**: Fully functional with comprehensive error handling
- **Performance**: Optimized for high-throughput emotion analysis

### 🌐 Live Application URLs

- **Production Frontend**: `https://aiemotion.netlify.app`
- **API Health Check**: `http://3.144.160.219:8000/health`
- **Emotion Analysis Endpoint**: `http://3.144.160.219:8000/analyze`
- **Session Management**: `http://3.144.160.219:8000/sessions`

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Browser  │    │  Netlify CDN    │    │   AWS EC2       │
│                 │◄──►│   Frontend      │◄──►│   Backend API   │
│  React SPA      │    │   (Static)      │    │   (FastAPI)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                       ┌─────────────────┐             │
                       │  AI Processing  │◄────────────┘
                       │                 │
                       │ • State Agent   │
                       │ • Emotion AI    │
                       │ • Response Gen  │
                       │ • Trend Analysis│
                       └─────────────────┘
                                │
                       ┌─────────────────┐
                       │   Database      │
                       │                 │
                       │ • PostgreSQL    │
                       │ • Session Mgmt  │
                       │ • Analytics     │
                       └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** with pip
- **Node.js 18+** with npm
- **AWS Account** with appropriate permissions
- **Git** for version control

### 1. Clone and Setup

```bash
git clone https://github.com/MAINAKSAHA07/AI-agent-emotion-detction.git
cd AI-agent-emotion-detction
```

### 2. Environment Configuration

Create a `.env` file in the root directory:

```env
# AWS Configuration
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_DEFAULT_REGION=us-east-1

# Database Configuration (choose one)
# Development (SQLite)
DATABASE_URL=sqlite:///./emotion_detection.db

# Production (PostgreSQL)
# DATABASE_URL=postgresql://username:password@your-rds-endpoint:5432/emotion_detection

# Serverless (DynamoDB)
# USE_DYNAMODB=true
```

### 3. Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Start the backend server
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

### 5. Production Deployment

```bash
# Deploy to AWS EC2
./deploy_aws.sh

# Deploy to Netlify
./deploy_netlify.sh
```

## 📊 API Documentation

### Core Endpoints

| Endpoint                   | Method | Description                                        |
| -------------------------- | ------ | -------------------------------------------------- |
| `/analyze`               | POST   | Analyze emotion from text input with AI processing |
| `/history/{session_id}`  | GET    | Retrieve analysis history for a session            |
| `/trends/{session_id}`   | GET    | Get emotional trends and patterns                  |
| `/sessions`              | GET    | List all user sessions with metadata               |
| `/sessions/{session_id}` | DELETE | Delete a session and all associated data           |
| `/health`                | GET    | System health check and status                     |

### Request/Response Examples

#### Emotion Analysis

```bash
curl -X POST "https://aiemotion.netlify.app/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I am feeling overwhelmed with work today",
    "session_id": "session_123",
    "context": "work_stress"
  }'
```

#### Session History

```bash
curl "https://aiemotion.netlify.app/api/history/session_123"
```

#### Emotional Trends

```bash
curl "https://aiemotion.netlify.app/api/trends/session_123"
```

## 🧠 AI Agent Capabilities

### Emotion Processing Pipeline

| Input Type   | Processing Stage    | Output                   |
| ------------ | ------------------- | ------------------------ |
| Text Input   | Sentiment Analysis  | Emotional Classification |
| Context Data | Pattern Recognition | Adaptive Response        |
| History      | Trend Analysis      | Personalized Insights    |

### Intelligent Response System

- **Contextual Understanding**: Analyzes conversation history for better responses
- **Emotional Intelligence**: Provides empathetic and supportive interactions
- **Adaptive Learning**: Improves responses based on user patterns
- **Multi-modal Support**: Handles various emotional states and contexts

## 🎨 Frontend Architecture

### React Components

| Component                      | Purpose                         | Features                                                   |
| ------------------------------ | ------------------------------- | ---------------------------------------------------------- |
| **EmotionAgent**         | Conversational AI interface     | Real-time chat, emotion detection, adaptive responses      |
| **EmotionAnalyzer**      | Text analysis interface         | Input validation, real-time processing, error handling     |
| **EmotionHistory**       | Analysis history display        | Visual indicators, chronological sorting, detailed metrics |
| **EmotionTrends**        | Analytics dashboard             | Trend visualization, pattern recognition, insights         |
| **AgentAnalysisResults** | Results presentation            | Detailed analysis display, response formatting             |
| **Header**               | Navigation & session management | Session controls, view switching, user interface           |

### User Interface Features

- **Dual Mode Interface**: Switch between conversational agent and traditional analysis
- **Real-time Updates**: Live emotion analysis with instant feedback
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Accessibility**: Clear visual indicators and user-friendly navigation

## 🗄️ Data Architecture

### Database Support

| Database Type        | Use Case              | Features                                      |
| -------------------- | --------------------- | --------------------------------------------- |
| **SQLite**     | Development & Testing | Local storage, easy setup                     |
| **PostgreSQL** | Production            | ACID compliance, complex queries, scalability |
| **DynamoDB**   | Serverless            | NoSQL, auto-scaling, AWS integration          |

### Data Models

#### Emotion Analysis

- **Session Tracking**: Links analyses to user sessions
- **Multi-dimensional Data**: Sentiment, emotion, valence, arousal, confidence
- **Contextual Information**: Language detection, conversation history
- **Timestamps**: Precise analysis timing and session management

#### Session Management

- **User Sessions**: Persistent session tracking with metadata
- **Activity Monitoring**: Last activity timestamps and usage patterns
- **Analytics**: Total analyses, emotional trends, session insights

## 🔧 Configuration & Security

### AWS Permissions

The application requires specific AWS permissions for AI processing:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "comprehend:DetectSentiment",
                "comprehend:DetectDominantLanguage"
            ],
            "Resource": "*"
        }
    ]
}
```

### Environment Configuration

| Variable                  | Description                | Required | Default                          |
| ------------------------- | -------------------------- | -------- | -------------------------------- |
| `AWS_ACCESS_KEY_ID`     | AWS access credentials     | Yes      | -                                |
| `AWS_SECRET_ACCESS_KEY` | AWS secret credentials     | Yes      | -                                |
| `AWS_DEFAULT_REGION`    | AWS service region         | No       | us-east-1                        |
| `DATABASE_URL`          | Database connection string | No       | sqlite:///./emotion_detection.db |
| `USE_DYNAMODB`          | Enable DynamoDB mode       | No       | false                            |

## 🚀 Deployment Strategies

### Production Deployment (Current)

#### Frontend - Netlify

- **CDN Distribution**: Global content delivery for optimal performance
- **Automatic Deployments**: Git-based continuous deployment
- **Custom Domain**: Professional domain with SSL certificates
- **API Proxy**: Secure backend communication

#### Backend - AWS EC2

- **Scalable Infrastructure**: Auto-scaling EC2 instances
- **Load Balancing**: High availability and performance
- **Database Integration**: PostgreSQL with connection pooling
- **Security**: VPC configuration and security groups

### Alternative Deployment Options

| Platform                        | Use Case          | Benefits                         |
| ------------------------------- | ----------------- | -------------------------------- |
| **AWS Lambda**            | Serverless        | Pay-per-use, auto-scaling        |
| **AWS ECS**               | Containerized     | Docker containers, orchestration |
| **AWS Elastic Beanstalk** | Managed Platform  | Easy deployment, monitoring      |
| **Docker**                | Local/Development | Consistent environments          |

## 📈 Monitoring & Analytics

### Performance Monitoring

- **API Response Times**: Real-time performance tracking
- **Error Rate Monitoring**: Automated error detection and alerting
- **Usage Analytics**: User engagement and feature utilization
- **Cost Optimization**: AWS service usage and cost monitoring

### Logging & Debugging

- **Structured Logging**: Comprehensive application logs
- **Error Tracking**: Detailed error reporting and debugging
- **Session Analytics**: User behavior and emotional pattern analysis
- **Performance Metrics**: System health and optimization insights

## 🔒 Security & Privacy

### Data Protection

- **Encryption**: End-to-end data encryption in transit and at rest
- **Access Control**: Role-based access control and authentication
- **Input Validation**: Comprehensive input sanitization and validation
- **Rate Limiting**: API protection against abuse and overuse

### Compliance

- **Data Privacy**: GDPR-compliant data handling practices
- **Secure Storage**: Encrypted database connections and storage
- **Audit Logging**: Comprehensive audit trails for all operations

## 🤝 Contributing

We welcome contributions to improve the emotion detection platform:

1. **Fork the Repository**: Create your own fork of the project
2. **Create Feature Branch**: Use descriptive branch names for new features
3. **Follow Coding Standards**: Maintain code quality and documentation
4. **Add Tests**: Include appropriate tests for new functionality
5. **Submit Pull Request**: Provide detailed descriptions of changes

### Development Guidelines

- **Code Quality**: Follow PEP 8 for Python and ESLint for JavaScript
- **Documentation**: Update README and code comments for new features
- **Testing**: Ensure all tests pass before submitting PRs
- **Security**: Review security implications of any changes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**🧠 Built with ❤️ for advancing emotional intelligence through AI technology**
