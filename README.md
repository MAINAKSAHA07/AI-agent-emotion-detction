# 🌐 Emotion Detection Web App

A professional web application that uses **advanced AI technology** to detect emotions from user input and runs through an **intelligent agent layer** for adaptive responses.

## 🎯 Features

- **Real-time Emotion Detection**: Analyze text sentiment and emotions using advanced AI technology
- **Intelligent Agent Layer**: AI agent that maps sentiments to emotions and provides adaptive responses
- **Session Management**: Track emotional trends and history per user session
- **Responsive Dashboard**: Modern React frontend with real-time updates
- **Database Integration**: SQLite, PostgreSQL, or DynamoDB for persistent storage
- **AWS Native**: Built for AWS deployment with Lambda, EC2, Elastic Beanstalk support

## 🚀 Current Deployment Status

### ✅ What's Working:
- **Frontend**: Deployed to EC2 nginx root (`/var/www/html/`)
- **Backend**: Running on EC2 with advanced AI integration
- **Database**: PostgreSQL configured and running
- **API**: Working locally on EC2 (tested successfully)
- **Emotion Analysis**: Working with 99.78% confidence

### 🔧 Final Step Required:
**Open AWS Security Group for Port 80**

1. Go to AWS Console → EC2 → Security Groups
2. Find your instance's security group
3. Add inbound rule:
   - **Type**: HTTP
   - **Port**: 80
   - **Source**: 0.0.0.0/0 (or your IP for security)

### 🌐 Test URLs (after opening port 80):
- **Frontend**: `http://3.144.160.219/`
- **API Health**: `http://3.144.160.219/api/health`
- **Emotion Analysis**: `http://3.144.160.219/api/analyze`

## 🏗️ Architecture

```
User (Browser)
   ↓
React Frontend
   ↓
FastAPI Backend
   ↓
State Agent (Python)
   ├── Amazon Comprehend Integration
   ├── Emotion Mapping Logic
   ├── Adaptive Response Generation
   └── Trend Analysis
   ↓
AWS Database (RDS/DynamoDB)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- AWS Account with Comprehend access
- AWS CLI configured

### 1. Clone and Setup

```bash
git clone https://github.com/MAINAKSAHA07/AI-agent-emotion-detction.git
cd AI-agent-emotion-detction
```

### 2. Environment Configuration

```bash
# Copy environment template
cp env.example .env

# Edit .env with your AWS credentials
nano .env
```

Required environment variables:
```env
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_DEFAULT_REGION=us-east-1

# Choose your database option:
# Option 1: SQLite (Development)
DATABASE_URL=sqlite:///./emotion_detection.db

# Option 2: AWS RDS PostgreSQL (Production)
# DATABASE_URL=postgresql://username:password@your-rds-endpoint:5432/emotion_detection

# Option 3: DynamoDB (Serverless)
# USE_DYNAMODB=true
```

### 3. Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run database migrations (if using PostgreSQL)
# The app will create tables automatically on first run

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

### 5. AWS Deployment

```bash
# Deploy to AWS (choose your option)
./aws/deploy.sh

# Options available:
# 1) AWS Lambda (Serverless)
# 2) AWS Elastic Beanstalk (Container)
# 3) AWS EC2 (Virtual Machine)
# 4) AWS ECS (Container Service)
# 5) Local Development (SQLite)
```

## 📊 API Endpoints

### Core Endpoints

- `POST /analyze` - Analyze emotion from text input
- `GET /history/{session_id}` - Get analysis history for a session
- `GET /trends/{session_id}` - Get emotional trends for a session
- `GET /sessions` - List all user sessions
- `DELETE /sessions/{session_id}` - Delete a session

### Example API Usage

```bash
# Analyze emotion
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "I am so happy today!", "session_id": "session_123"}'

# Get session history
curl "http://localhost:8000/history/session_123"
```

## 🧠 State Agent Features

### Emotion Mapping

| Comprehend Sentiment | Mapped Emotion | Valence | Arousal |
|---------------------|----------------|---------|---------|
| POSITIVE | Joy / Optimism | +0.8 | Medium-High |
| NEGATIVE | Sadness / Anger / Fear | -0.8 | Medium-High |
| NEUTRAL | Calm / Indifference | 0.0 | Low |
| MIXED | Conflicted / Uncertain | ±0.2 | Medium |

### Adaptive Responses

- **Positive**: Encouraging responses to continue positive emotions
- **Negative**: Empathetic responses with support suggestions
- **Neutral**: Balanced responses to maintain calm state
- **Mixed**: Clarifying questions to understand conflicting emotions

## 🎨 Frontend Components

- **EmotionAnalyzer**: Main input interface for text analysis
- **EmotionHistory**: Display of past analyses with visual indicators
- **EmotionTrends**: Real-time trend analysis and insights
- **Header**: Session management and navigation

## 🗄️ Database Schema

### Tables

- `emotion_analyses`: Stores individual emotion analysis results
- `user_sessions`: Tracks user sessions and metadata

### Key Fields

- `sentiment`: Comprehend sentiment (POSITIVE, NEGATIVE, NEUTRAL, MIXED)
- `emotion`: Mapped emotion from agent
- `valence`: Emotional valence (-1 to +1)
- `arousal`: Emotional arousal (0 to 1)
- `confidence`: Analysis confidence score

## 🔧 Configuration

### AWS IAM Permissions

Your AWS user/role needs the following permissions:

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

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AWS_ACCESS_KEY_ID` | AWS access key | Required |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | Required |
| `AWS_DEFAULT_REGION` | AWS region | us-east-1 |
| `DATABASE_URL` | Database connection string | sqlite:///./emotion_detection.db |
| `DEBUG` | Debug mode | False |

## 🚀 Deployment Options

### 1. AWS Elastic Beanstalk

```bash
# Install EB CLI
pip install awsebcli

# Initialize EB application
eb init

# Deploy
eb deploy
```

### 2. AWS Lambda + API Gateway

```bash
# Package for Lambda
zip -r emotion-detection.zip . -x "frontend/node_modules/*" "*.git*"

# Deploy with AWS CLI or Serverless Framework
```

### 3. Docker on EC2

```bash
# Build and run on EC2
docker build -t emotion-detection .
docker run -p 8000:8000 -e AWS_ACCESS_KEY_ID=xxx -e AWS_SECRET_ACCESS_KEY=xxx emotion-detection
```

## 📈 Monitoring & Logging

### CloudWatch Integration

- API request/response logging
- Error tracking and alerting
- Performance metrics
- Cost monitoring for Comprehend usage

### Application Logs

```python
# Configure logging in your environment
import logging
logging.basicConfig(level=logging.INFO)
```

## 🔒 Security Considerations

- **AWS IAM**: Use least-privilege IAM roles
- **HTTPS**: Enable SSL/TLS for production
- **Rate Limiting**: Implement API rate limiting
- **Input Validation**: Sanitize all user inputs
- **Database Security**: Use encrypted connections

## 🧪 Testing

```bash
# Backend tests
python -m pytest tests/

# Frontend tests
cd frontend && npm test

# Integration tests
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

## 📚 Development Roadmap

### Phase 1 (Current)
- ✅ Text input → Comprehend → emotion output
- ✅ Session management and history
- ✅ Trend analysis and insights

### Phase 2 (Planned)
- 🔄 Voice input (speech-to-text)
- 🔄 Real-time emotion visualization
- 🔄 Multi-language support

### Phase 3 (Future)
- 🔄 Personalization and user profiles
- 🔄 LLM integration for advanced responses
- 🔄 Mobile app development

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:

1. Check the [Issues](https://github.com/your-repo/issues) page
2. Review the documentation
3. Contact the development team

## 🙏 Acknowledgments

- Amazon Comprehend for sentiment analysis
- FastAPI for the robust backend framework
- React for the modern frontend
- The open-source community for various dependencies

---

**Built with ❤️ for emotional intelligence and AI-powered insights**
