"""
State Agent for Emotion Detection using Amazon Comprehend
Handles text analysis, emotion mapping, and intelligent responses
"""

import boto3
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import re
import os
import openai
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class StateAgent:
    """
    Intelligent agent that processes text input through Amazon Comprehend
    and provides emotion detection with adaptive responses.
    """
    
    def __init__(self, region_name: str = 'us-east-1'):
        """
        Initialize the State Agent with AWS Comprehend client and OpenAI client.
        
        Args:
            region_name: AWS region for Comprehend service
        """
        load_dotenv()
        
        # Initialize AWS Comprehend
        self.comprehend = boto3.client('comprehend', region_name=region_name)
        
        # Initialize OpenAI client
        openai_api_key = os.getenv('chatgptapi')
        if openai_api_key:
            import openai
            openai.api_key = openai_api_key
            self.openai_client = openai
        else:
            self.openai_client = None
            logger.warning("ChatGPT API key not found. ChatGPT features will be disabled.")
        
        self.emotion_mapping = self._initialize_emotion_mapping()
        
    def _initialize_emotion_mapping(self) -> Dict[str, Dict[str, Any]]:
        """
        Initialize the emotion mapping from Comprehend sentiments to emotions.
        
        Returns:
            Dictionary mapping sentiments to emotion details
        """
        return {
            "POSITIVE": {
                "emotion": "Joy / Optimism / Excitement",
                "valence": 0.8,
                "arousal": 0.6,
                "response_template": "That sounds great! I'd love to hear more about what's going well for you.",
                "emotional_indicators": ["happy", "excited", "optimistic", "enthusiastic", "grateful"],
                "response_style": "enthusiastic and celebratory"
            },
            "NEGATIVE": {
                "emotion": "Sadness / Anger / Fear / Frustration",
                "valence": -0.8,
                "arousal": 0.7,
                "response_template": "I can hear that this is really difficult for you. I'm here to listen and help however I can.",
                "emotional_indicators": ["sad", "angry", "frustrated", "worried", "disappointed"],
                "response_style": "empathetic and supportive"
            },
            "NEUTRAL": {
                "emotion": "Calm / Indifference / Contemplative",
                "valence": 0.0,
                "arousal": 0.2,
                "response_template": "I appreciate you sharing that with me. How can I help you today?",
                "emotional_indicators": ["calm", "neutral", "thoughtful", "balanced", "content"],
                "response_style": "gentle and exploratory"
            },
            "MIXED": {
                "emotion": "Conflicted / Uncertain / Ambivalent",
                "valence": 0.2,
                "arousal": 0.5,
                "response_template": "It sounds like you're working through some complex thoughts. I'm here to help you sort through things.",
                "emotional_indicators": ["conflicted", "uncertain", "torn", "ambivalent", "confused"],
                "response_style": "patient and understanding"
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
    
    def _calculate_emotional_intensity(self, emotion_data: Dict[str, Any]) -> str:
        """
        Calculate emotional intensity based on Comprehend analysis.
        
        Args:
            emotion_data: Emotion analysis results
            
        Returns:
            String describing emotional intensity
        """
        confidence = emotion_data.get('confidence', 0.5)
        valence = abs(emotion_data.get('valence', 0.0))
        arousal = emotion_data.get('arousal', 0.0)
        
        # Calculate intensity based on confidence, valence magnitude, and arousal
        intensity_score = (confidence * 0.4) + (valence * 0.3) + (arousal * 0.3)
        
        if intensity_score > 0.7:
            return "Very High"
        elif intensity_score > 0.5:
            return "High"
        elif intensity_score > 0.3:
            return "Moderate"
        else:
            return "Low"
    
    def _determine_response_strategy(self, emotion_data: Dict[str, Any]) -> str:
        """
        Determine the appropriate response strategy based on valence and arousal ranges.
        
        Ground Rules:
        - Valence: -1 to 1 (0 is midpoint)
        - Arousal: 0 to 1 (0.5 is midpoint)
        
        Args:
            emotion_data: Emotion analysis results
            
        Returns:
            String describing response strategy
        """
        valence = emotion_data.get('valence', 0.0)
        arousal = emotion_data.get('arousal', 0.0)
        
        # Rule 1: Valence 0 to 1, Arousal 0.5 to 1 - EXCITED & SEEKING DETAILED ANSWERS
        if 0 <= valence <= 1 and 0.5 <= arousal <= 1:
            return "EXCITED_DETAILED_SEARCH"
        
        # Rule 2: Valence 0 to -1, Arousal 0.5 to 1 - STRESSED & NEEDS URGENT CLEAR ANSWERS
        elif -1 <= valence <= 0 and 0.5 <= arousal <= 1:
            return "STRESSED_URGENT_CLEAR"
        
        # Rule 3: Valence 0 to -1, Arousal 0 to 0.5 - BORED & NEEDS SIMPLE CLEAR ANSWERS
        elif -1 <= valence <= 0 and 0 <= arousal <= 0.5:
            return "BORED_SIMPLE_CLEAR"
        
        # Rule 4: Valence 0 to 1, Arousal 0 to 0.5 - CALM & NEEDS ENGAGING TWO-WAY CONVERSATION
        elif 0 <= valence <= 1 and 0 <= arousal <= 0.5:
            return "CALM_ENGAGING_CONVERSATION"
        
        # Fallback for edge cases
        else:
            return "ADAPTIVE_CONTEXTUAL"
    
    def _calculate_response_temperature(self, emotion_data: Dict[str, Any]) -> float:
        """
        Calculate appropriate temperature for ChatGPT based on emotional state.
        
        Args:
            emotion_data: Emotion analysis results
            
        Returns:
            Temperature value (0.0 to 1.0)
        """
        arousal = emotion_data.get('arousal', 0.0)
        valence = emotion_data.get('valence', 0.0)
        confidence = emotion_data.get('confidence', 0.5)
        
        # Base temperature
        base_temp = 0.6
        
        # Adjust based on arousal (higher arousal = more creative/energetic)
        arousal_adjustment = arousal * 0.2
        
        # Adjust based on valence (extreme emotions = more creative)
        valence_adjustment = abs(valence) * 0.1
        
        # Adjust based on confidence (higher confidence = more focused)
        confidence_adjustment = (1 - confidence) * 0.1
        
        temperature = base_temp + arousal_adjustment + valence_adjustment + confidence_adjustment
        
        # Clamp between 0.3 and 0.9
        return max(0.3, min(0.9, temperature))

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
        
        # Add context-aware modifications without explicit mood mentions
        if context:
            if emotion_data['valence'] > 0.5:
                base_response += f" I can see {context} is important to you."
            elif emotion_data['valence'] < -0.5:
                base_response += f" It sounds like {context} is really challenging for you."
        
        return base_response
    
    def rephrase_with_chatgpt(self, text: str) -> str:
        """
        Use ChatGPT 4 Mini to enhance user input for better emotion analysis.
        
        Args:
            text: Original user input
            
        Returns:
            Enhanced text optimized for emotion analysis
        """
        if not self.openai_client:
            return text  # Return original if ChatGPT not available
        
        try:
            response = self.openai_client.ChatCompletion.create(
                model="gpt-4.1-nano",
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert in emotional intelligence and text analysis. Your task is to enhance user input to make their emotional state more explicit and analyzable while preserving their original meaning and intent.

ENHANCEMENT GUIDELINES:
1. **Preserve Original Meaning**: Keep the core message intact
2. **Clarify Emotional Context**: Make implicit emotions more explicit
3. **Maintain Authenticity**: Don't add emotions that aren't implied
4. **Improve Clarity**: Make the emotional undertones clearer
5. **Keep Natural**: Ensure the enhanced text sounds natural

EXAMPLES:
- "I'm tired" → "I'm feeling exhausted and drained"
- "Work is hard" → "I'm feeling overwhelmed and stressed about work"
- "I'm excited!" → "I'm feeling enthusiastic and excited about this opportunity"

Focus on making the emotional content more analyzable while keeping it authentic."""
                    },
                    {
                        "role": "user",
                        "content": f"Enhance this text for better emotion analysis while keeping it authentic: {text}"
                    }
                ],
                max_tokens=200,
                temperature=0.4
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error enhancing text with ChatGPT: {e}")
            return text  # Return original on error
    
    def generate_conversational_response_with_chatgpt(self, emotion_data: Dict[str, Any], 
                                                     original_text: str, 
                                                     conversation_history: Optional[List[Dict]] = None) -> str:
        """
        Use ChatGPT to generate conversational responses that are heavily dependent on Comprehend emotional analysis.
        
        Args:
            emotion_data: Emotion analysis results from Comprehend
            original_text: Original user input
            conversation_history: Previous conversation context
            
        Returns:
            Emotionally-aware conversational response
        """
        if not self.openai_client:
            return self.generate_adaptive_response(emotion_data)  # Fallback to original method
        
        try:
            emotion = emotion_data.get('emotion', 'Unknown')
            sentiment = emotion_data.get('sentiment', 'NEUTRAL')
            confidence = emotion_data.get('confidence', 0.5)
            valence = emotion_data.get('valence', 0.0)
            arousal = emotion_data.get('arousal', 0.0)
            sentiment_scores = emotion_data.get('sentiment_scores', {})
            
            # Determine emotional intensity and response strategy
            emotional_intensity = self._calculate_emotional_intensity(emotion_data)
            response_strategy = self._determine_response_strategy(emotion_data)
            
            # Create fine-tuned system prompt based on valence and arousal ranges
            system_prompt = f"""You are an emotionally intelligent AI assistant whose responses are PRIMARILY driven by the user's emotional state detected by Amazon Comprehend. Your response style, tone, and content must adapt based on their emotional analysis.

CURRENT EMOTIONAL ANALYSIS (CRITICAL - USE THIS TO SHAPE YOUR RESPONSE):
- Sentiment: {sentiment} (confidence: {confidence:.2f})
- Emotional Valence: {valence:.2f} (positive/negative intensity)
- Emotional Arousal: {arousal:.2f} (calm/excited intensity)
- Emotional Intensity: {emotional_intensity}
- Response Strategy: {response_strategy}

SENTIMENT BREAKDOWN:
- Positive: {sentiment_scores.get('Positive', 0):.2f}
- Negative: {sentiment_scores.get('Negative', 0):.2f}
- Neutral: {sentiment_scores.get('Neutral', 0):.2f}
- Mixed: {sentiment_scores.get('Mixed', 0):.2f}

FINE-TUNED RESPONSE STRATEGIES BASED ON VALENCE AND AROUSAL:

**STRATEGY: {response_strategy}**

1. **EXCITED_DETAILED_SEARCH** (Valence: 0 to 1, Arousal: 0.5 to 1):
   - User is seeking DETAILED, COMPREHENSIVE answers
   - Provide thorough, well-researched responses with supporting evidence
   - Include specific examples, data, and backing information
   - Use engaging, enthusiastic language that matches their energy
   - Ask follow-up questions to dive deeper into topics
   - Provide multiple perspectives and detailed explanations

2. **STRESSED_URGENT_CLEAR** (Valence: 0 to -1, Arousal: 0.5 to 1):
   - User needs URGENT, CLEAR, TO-THE-POINT answers
   - Keep responses SHORT and DIRECT - no rambling or unnecessary details
   - Provide immediate, actionable solutions
   - Use clear, concise language
   - Focus on practical, urgent help
   - Avoid lengthy explanations or tangents

3. **BORED_SIMPLE_CLEAR** (Valence: 0 to -1, Arousal: 0 to 0.5):
   - User needs SIMPLE, CLEAR answers
   - Use straightforward, easy-to-understand language
   - Keep responses concise but complete
   - Avoid complex jargon or lengthy explanations
   - Make information digestible and engaging
   - Use simple, direct communication

4. **CALM_ENGAGING_CONVERSATION** (Valence: 0 to 1, Arousal: 0 to 0.5):
   - User needs ENGAGING, TWO-WAY conversation
   - Ask thoughtful questions to encourage dialogue
   - Share personal insights and experiences
   - Create a conversational, friendly tone
   - Encourage back-and-forth discussion
   - Make the interaction feel like a natural conversation

CRITICAL RULES:
- Your response MUST match the specific strategy for their emotional state
- Adjust your response length and complexity based on their arousal level
- Match their energy level (high arousal = energetic, low arousal = calm)
- Provide the type of answer they're seeking based on their emotional state
- Use emotional intelligence in every interaction WITHOUT explicitly mentioning their mood
- Respond naturally and conversationally

AVOID:
- Generic responses that ignore emotional context
- Being emotionally tone-deaf to their state
- Overwhelming someone who's already distressed
- Being dismissive of their feelings
- Providing the wrong type of response for their emotional state
- Explicitly mentioning their detected mood or emotional state
- Clinical or analytical language about their emotions"""
            
            # Create emotionally-aware user prompt
            history_context = ""
            if conversation_history:
                recent_history = conversation_history[-3:]  # Last 3 exchanges
                history_context = f"\n\nRecent conversation context:\n"
                for exchange in recent_history:
                    history_context += f"User: {exchange.get('user', '')}\nAssistant: {exchange.get('assistant', '')}\n"
            
            user_prompt = f"""User's message: "{original_text}"

EMOTIONAL CONTEXT (MUST INFLUENCE YOUR RESPONSE):
- Sentiment: {sentiment} (confidence: {confidence:.2f})
- Emotional intensity: {emotional_intensity}
- Valence: {valence:.2f} (positive/negative)
- Arousal: {arousal:.2f} (calm/excited)
{history_context}

Generate a natural, conversational response that is emotionally appropriate for their current state. Your response should feel like it's coming from someone who truly understands their situation, but DO NOT explicitly mention their mood or emotional state. Respond naturally and helpfully."""
            
            # Adjust temperature based on emotional state
            temperature = self._calculate_response_temperature(emotion_data)
            
            response = self.openai_client.ChatCompletion.create(
                model="gpt-4.1-nano",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=300,
                temperature=temperature
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating intelligent response with ChatGPT: {e}")
            return self.generate_adaptive_response(emotion_data)  # Fallback to original method

    def process_text(self, text: str, session_id: Optional[str] = None,
                    context: Optional[str] = None, conversation_history: Optional[List[Dict]] = None) -> Dict[str, Any]:
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
        
        # Rephrase with ChatGPT for better analysis
        rephrased_text = self.rephrase_with_chatgpt(cleaned_text)
        
        # Detect language
        language = self.detect_language(rephrased_text)
        
        # Analyze sentiment using rephrased text
        sentiment_result = self.analyze_sentiment(rephrased_text, language or 'en')
        sentiment = sentiment_result['Sentiment']
        scores = sentiment_result['SentimentScore']
        
        # Map to emotion
        emotion_data = self.map_sentiment_to_emotion(sentiment, scores)
        
        # Generate conversational response with ChatGPT
        response = self.generate_conversational_response_with_chatgpt(emotion_data, text, conversation_history)
        
        # Compile results
        result = {
            'input_text': cleaned_text,
            'rephrased_text': rephrased_text,
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
