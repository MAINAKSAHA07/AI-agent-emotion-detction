"""
Database models and configuration for emotion detection app.
Supports AWS RDS (PostgreSQL) and DynamoDB.
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

# Database configuration - AWS RDS or local SQLite
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./emotion_detection.db')
USE_DYNAMODB = os.getenv('USE_DYNAMODB', 'false').lower() == 'true'

# Create engine for SQL databases with proper connection pool settings
if not USE_DYNAMODB:
    engine = create_engine(
        DATABASE_URL,
        pool_size=5,           # Number of connections to maintain in pool
        max_overflow=10,        # Additional connections beyond pool_size
        pool_timeout=30,        # Seconds to wait for connection from pool
        pool_recycle=3600,      # Recycle connections after 1 hour
        pool_pre_ping=True     # Validate connections before use
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
else:
    # DynamoDB configuration
    dynamodb = boto3.resource('dynamodb', region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-1'))
    engine = None
    SessionLocal = None

Base = declarative_base()


class EmotionAnalysis(Base):
    """Model for storing emotion analysis results."""
    
    __tablename__ = "emotion_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    input_text = Column(Text)
    original_text = Column(Text)
    language = Column(String)
    sentiment = Column(String)
    sentiment_scores = Column(JSON)
    emotion = Column(String)
    valence = Column(Float)
    arousal = Column(Float)
    confidence = Column(Float)
    adaptive_response = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'input_text': self.input_text,
            'original_text': self.original_text,
            'language': self.language,
            'sentiment': self.sentiment,
            'sentiment_scores': self.sentiment_scores,
            'emotion': self.emotion,
            'valence': self.valence,
            'arousal': self.arousal,
            'confidence': self.confidence,
            'adaptive_response': self.adaptive_response,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }


class UserSession(Base):
    """Model for tracking user sessions."""
    
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)
    total_analyses = Column(Integer, default=0)
    emotional_trend = Column(String)
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_activity': self.last_activity.isoformat() if self.last_activity else None,
            'total_analyses': self.total_analyses,
            'emotional_trend': self.emotional_trend
        }


def get_db():
    """Get database session."""
    if USE_DYNAMODB:
        return None  # DynamoDB doesn't use sessions
    else:
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()


def create_tables():
    """Create all database tables."""
    if USE_DYNAMODB:
        create_dynamodb_tables()
    else:
        Base.metadata.create_all(bind=engine)


def create_dynamodb_tables():
    """Create DynamoDB tables."""
    try:
        # Create emotion_analyses table
        table_name = 'emotion_analyses'
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'session_id',
                    'AttributeType': 'S'
                }
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'session-index',
                    'KeySchema': [
                        {
                            'AttributeName': 'session_id',
                            'KeyType': 'HASH'
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    }
                }
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        print(f"✅ Created DynamoDB table: {table_name}")
        
        # Create user_sessions table
        sessions_table_name = 'user_sessions'
        sessions_table = dynamodb.create_table(
            TableName=sessions_table_name,
            KeySchema=[
                {
                    'AttributeName': 'session_id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'session_id',
                    'AttributeType': 'S'
                }
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        print(f"✅ Created DynamoDB table: {sessions_table_name}")
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print("✅ DynamoDB tables already exist")
        else:
            print(f"❌ Error creating DynamoDB tables: {e}")


def get_dynamodb_table(table_name):
    """Get DynamoDB table resource."""
    if USE_DYNAMODB:
        return dynamodb.Table(table_name)
    return None
