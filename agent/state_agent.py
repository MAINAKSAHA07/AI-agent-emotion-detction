"""
State Agent for Emotion Detection using Amazon Comprehend
Handles text analysis, emotion mapping, and intelligent responses
"""

import boto3
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import re

logger = logging.getLogger(__name__)


class StateAgent:
    """
    Intelligent agent that processes text input through Amazon Comprehend
    and provides emotion detection with adaptive responses.
    """
    
    def __init__(self, region_name: str = 'us-east-1'):
        """
        Initialize the State Agent with AWS Comprehend client.
        
        Args:
            region_name: AWS region for Comprehend service
        """
        self.comprehend = boto3.client('comprehend', region_name=region_name)
        self.emotion_mapping = self._initialize_emotion_mapping()
        
    def _initialize_emotion_mapping(self) -> Dict[str, Dict[str, Any]]:
        """
        Initialize the emotion mapping from Comprehend sentiments to emotions.
        
        Returns:
            Dictionary mapping sentiments to emotion details
        """
        return {
            "POSITIVE": {
                "emotion": "Joy / Optimism",
                "valence": 0.8,
                "arousal": 0.6,
                "response_template": "That's wonderful! What made you feel so positive about this?"
            },
            "NEGATIVE": {
                "emotion": "Sadness / Anger / Fear",
                "valence": -0.8,
                "arousal": 0.7,
                "response_template": "I'm sorry to hear that. Would you like to talk about what's troubling you?"
            },
            "NEUTRAL": {
                "emotion": "Calm / Indifference",
                "valence": 0.0,
                "arousal": 0.2,
                "response_template": "It sounds like you're in a balanced state. How are you feeling overall?"
            },
            "MIXED": {
                "emotion": "Conflicted / Uncertain",
                "valence": 0.2,
                "arousal": 0.5,
                "response_template": "You seem to have mixed feelings about this. Can you tell me more about what's on your mind?"
            }
        }
    
    def preprocess_text(self, text: str) -> str:
        """
        Clean and preprocess input text.
        
        Args:
            text: Raw input text
            
        Returns:
            Cleaned text ready for analysis
        """
        if not text or not text.strip():
            return ""
            
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?;:\'-]', '', text)
        
        return text
    
    def detect_language(self, text: str) -> Optional[str]:
        """
        Detect the dominant language of the input text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Language code or None if detection fails
        """
        try:
            response = self.comprehend.detect_dominant_language(Text=text)
            languages = response['Languages']
            if languages:
                return languages[0]['LanguageCode']
        except Exception as e:
            logger.warning(f"Language detection failed: {e}")
        return None
    
    def analyze_sentiment(self, text: str, language_code: str = 'en') -> Dict[str, Any]:
        """
        Analyze sentiment of the input text using Amazon Comprehend.
        
        Args:
            text: Text to analyze
            language_code: Language code for analysis
            
        Returns:
            Sentiment analysis results
        """
        try:
            response = self.comprehend.detect_sentiment(
                Text=text,
                LanguageCode=language_code
            )
            return response
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            return {
                'Sentiment': 'NEUTRAL',
                'SentimentScore': {
                    'Positive': 0.25,
                    'Negative': 0.25,
                    'Neutral': 0.5,
                    'Mixed': 0.0
                }
            }
    
    def map_sentiment_to_emotion(self, sentiment: str, scores: Dict[str, float]) -> Dict[str, Any]:
        """
        Map Comprehend sentiment to emotional state with valence and arousal.
        
        Args:
            sentiment: Sentiment from Comprehend
            scores: Sentiment scores from Comprehend
            
        Returns:
            Emotion mapping with valence, arousal, and confidence
        """
        emotion_data = self.emotion_mapping.get(sentiment, self.emotion_mapping['NEUTRAL'])
        
        # Calculate confidence as the maximum score
        confidence = max(scores.values())
        
        # Adjust valence and arousal based on confidence
        valence = emotion_data['valence'] * confidence
        arousal = emotion_data['arousal'] * confidence
        
        return {
            'emotion': emotion_data['emotion'],
            'valence': round(valence, 2),
            'arousal': round(arousal, 2),
            'confidence': round(confidence, 2),
            'response_template': emotion_data['response_template']
        }
    
    def generate_adaptive_response(self, emotion_data: Dict[str, Any], 
                                 context: Optional[str] = None) -> str:
        """
        Generate an adaptive response based on detected emotion.
        
        Args:
            emotion_data: Emotion analysis results
            context: Optional context for more personalized responses
            
        Returns:
            Adaptive response string
        """
        base_response = emotion_data.get('response_template', 'Thank you for sharing.')
        
        # Add context-aware modifications
        if context:
            if emotion_data['valence'] > 0.5:
                base_response += f" I can see you're feeling positive about {context}."
            elif emotion_data['valence'] < -0.5:
                base_response += f" It sounds like {context} is really affecting you."
        
        return base_response
    
    def process_text(self, text: str, session_id: Optional[str] = None, 
                    context: Optional[str] = None) -> Dict[str, Any]:
        """
        Main processing method that handles the complete emotion detection pipeline.
        
        Args:
            text: Input text to analyze
            session_id: Optional session identifier
            context: Optional context for personalized responses
            
        Returns:
            Complete analysis results with emotion, sentiment, and response
        """
        # Preprocess text
        cleaned_text = self.preprocess_text(text)
        if not cleaned_text:
            return {
                'error': 'Empty or invalid input text',
                'timestamp': datetime.utcnow().isoformat()
            }
        
        # Detect language
        language = self.detect_language(cleaned_text)
        
        # Analyze sentiment
        sentiment_result = self.analyze_sentiment(cleaned_text, language or 'en')
        sentiment = sentiment_result['Sentiment']
        scores = sentiment_result['SentimentScore']
        
        # Map to emotion
        emotion_data = self.map_sentiment_to_emotion(sentiment, scores)
        
        # Generate adaptive response
        response = self.generate_adaptive_response(emotion_data, context)
        
        # Compile results
        result = {
            'input_text': cleaned_text,
            'original_text': text,
            'language': language,
            'sentiment': sentiment,
            'sentiment_scores': scores,
            'emotion': emotion_data['emotion'],
            'valence': emotion_data['valence'],
            'arousal': emotion_data['arousal'],
            'confidence': emotion_data['confidence'],
            'adaptive_response': response,
            'session_id': session_id,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Processed text analysis: {sentiment} -> {emotion_data['emotion']} (confidence: {emotion_data['confidence']})")
        
        return result
    
    def get_emotional_trends(self, session_data: list) -> Dict[str, Any]:
        """
        Analyze emotional trends from session data.
        
        Args:
            session_data: List of previous analysis results
            
        Returns:
            Trend analysis with emotional patterns
        """
        if not session_data:
            return {'trend': 'No data available'}
        
        valences = [item.get('valence', 0) for item in session_data]
        confidences = [item.get('confidence', 0) for item in session_data]
        
        avg_valence = sum(valences) / len(valences)
        avg_confidence = sum(confidences) / len(confidences)
        
        # Determine trend
        if avg_valence > 0.3:
            trend = 'Positive emotional trend'
        elif avg_valence < -0.3:
            trend = 'Negative emotional trend'
        else:
            trend = 'Stable emotional state'
        
        return {
            'trend': trend,
            'average_valence': round(avg_valence, 2),
            'average_confidence': round(avg_confidence, 2),
            'total_analyses': len(session_data)
        }
