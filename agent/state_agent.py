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
            self.openai_client = openai.OpenAI(api_key=openai_api_key)
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
        Enhanced with more granular emotional state detection and conversation context awareness.
        
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
        confidence = emotion_data.get('confidence', 0.5)
        
        # Enhanced strategy determination with more granular emotional states
        
        # HIGH CONFIDENCE EMOTIONAL STATES (confidence > 0.7)
        if confidence > 0.7:
            # Very Positive and Energetic (Valence: 0.6 to 1, Arousal: 0.6 to 1)
            if 0.6 <= valence <= 1 and 0.6 <= arousal <= 1:
                return "HIGHLY_EXCITED_DETAILED_EXPLORATION"
            
            # Very Negative and Stressed (Valence: -1 to -0.6, Arousal: 0.6 to 1)
            elif -1 <= valence <= -0.6 and 0.6 <= arousal <= 1:
                return "HIGHLY_STRESSED_URGENT_SUPPORT"
            
            # Very Negative and Low Energy (Valence: -1 to -0.6, Arousal: 0 to 0.4)
            elif -1 <= valence <= -0.6 and 0 <= arousal <= 0.4:
                return "HIGHLY_DEPRESSED_GENTLE_SUPPORT"
            
            # Very Positive and Calm (Valence: 0.6 to 1, Arousal: 0 to 0.4)
            elif 0.6 <= valence <= 1 and 0 <= arousal <= 0.4:
                return "HIGHLY_CONTENT_DEEP_CONVERSATION"
        
        # MODERATE CONFIDENCE EMOTIONAL STATES (confidence 0.4 to 0.7)
        elif confidence > 0.4:
            # Positive and Energetic (Valence: 0.2 to 0.8, Arousal: 0.5 to 0.9)
            if 0.2 <= valence <= 0.8 and 0.5 <= arousal <= 0.9:
                return "EXCITED_DETAILED_SEARCH"
            
            # Negative and Stressed (Valence: -0.8 to -0.2, Arousal: 0.5 to 0.9)
            elif -0.8 <= valence <= -0.2 and 0.5 <= arousal <= 0.9:
                return "STRESSED_URGENT_CLEAR"
            
            # Negative and Low Energy (Valence: -0.8 to -0.2, Arousal: 0.1 to 0.5)
            elif -0.8 <= valence <= -0.2 and 0.1 <= arousal <= 0.5:
                return "BORED_SIMPLE_CLEAR"
            
            # Positive and Calm (Valence: 0.2 to 0.8, Arousal: 0.1 to 0.5)
            elif 0.2 <= valence <= 0.8 and 0.1 <= arousal <= 0.5:
                return "CALM_ENGAGING_CONVERSATION"
        
        # LOW CONFIDENCE OR NEUTRAL STATES (confidence <= 0.4)
        else:
            # Neutral with high arousal (Valence: -0.2 to 0.2, Arousal: 0.6 to 1)
            if -0.2 <= valence <= 0.2 and 0.6 <= arousal <= 1:
                return "UNCERTAIN_BUT_ENERGETIC_EXPLORATION"
            
            # Neutral with low arousal (Valence: -0.2 to 0.2, Arousal: 0 to 0.4)
            elif -0.2 <= valence <= 0.2 and 0 <= arousal <= 0.4:
                return "UNCERTAIN_CALM_GUIDANCE"
            
            # Mixed emotions (any valence, moderate arousal)
            else:
                return "MIXED_EMOTIONS_ADAPTIVE_SUPPORT"
        
        # Fallback for edge cases
        return "ADAPTIVE_CONTEXTUAL"
    
    def _detect_feedback_and_adjust_strategy(self, text: str, emotion_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect user feedback and adjust response strategy accordingly.
        
        Args:
            text: User input text
            emotion_data: Current emotion analysis
            
        Returns:
            Adjusted emotion data with feedback handling
        """
        feedback_indicators = [
            "didn't like", "don't like", "hate", "terrible", "awful", "bad",
            "make it shorter", "make it better", "too long", "too short",
            "not helpful", "useless", "waste of time", "stupid",
            "give me", "I want", "I need", "show me", "tell me"
        ]
        
        text_lower = text.lower()
        is_feedback = any(indicator in text_lower for indicator in feedback_indicators)
        
        if is_feedback:
            # Adjust strategy to be more direct and helpful
            emotion_data['feedback_detected'] = True
            emotion_data['response_priority'] = 'SOLVE_PROBLEM'
            
            # Increase arousal slightly for more energetic responses
            emotion_data['arousal'] = min(1.0, emotion_data.get('arousal', 0.5) + 0.2)
            
            # Adjust confidence to be more assertive
            emotion_data['confidence'] = max(0.7, emotion_data.get('confidence', 0.5))
        
        return emotion_data
    
    def _calculate_response_temperature(self, emotion_data: Dict[str, Any]) -> float:
        """
        Calculate appropriate temperature for ChatGPT based on emotional state.
        Enhanced to be more responsive to arousal and valence values.
        
        Args:
            emotion_data: Emotion analysis results
            
        Returns:
            Temperature value (0.0 to 1.0)
        """
        arousal = emotion_data.get('arousal', 0.0)
        valence = emotion_data.get('valence', 0.0)
        confidence = emotion_data.get('confidence', 0.5)
        
        # Base temperature - more dynamic based on emotional state
        base_temp = 0.5
        
        # Arousal-based adjustment (higher arousal = more creative/energetic)
        # Scale: 0.0 to 0.4 adjustment based on arousal
        arousal_adjustment = arousal * 0.4
        
        # Valence-based adjustment (extreme emotions = more creative)
        # Scale: 0.0 to 0.3 adjustment based on valence magnitude
        valence_adjustment = abs(valence) * 0.3
        
        # Confidence-based adjustment (higher confidence = more focused, lower = more exploratory)
        # Scale: -0.2 to 0.2 adjustment based on confidence
        confidence_adjustment = (confidence - 0.5) * 0.4
        
        # Emotional intensity bonus (very high or very low emotions get more creative)
        emotional_intensity = abs(valence) + arousal
        intensity_bonus = 0.0
        if emotional_intensity > 1.2:  # Very intense emotions
            intensity_bonus = 0.1
        elif emotional_intensity < 0.3:  # Very calm emotions
            intensity_bonus = -0.1
        
        temperature = base_temp + arousal_adjustment + valence_adjustment + confidence_adjustment + intensity_bonus
        
        # Clamp between 0.2 and 0.95 for more dynamic range
        return max(0.2, min(0.95, temperature))

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
    
    def _enhance_text_with_context(self, text: str, conversation_history: Optional[List[Dict]] = None) -> str:
        """
        Enhance the input text with comprehensive conversation history context for better emotion analysis.
        Now considers the entire conversation history with intelligent summarization.
        
        Args:
            text: Current input text
            conversation_history: Previous conversation context
            
        Returns:
            Enhanced text with comprehensive conversation context
        """
        if not conversation_history or len(conversation_history) == 0:
            return text
        
        # Analyze conversation history for emotional patterns
        emotional_context = self._analyze_conversation_emotional_patterns(conversation_history)
        
        # Get comprehensive conversation context (up to 10 exchanges for better context)
        context_exchanges = conversation_history[-10:] if len(conversation_history) > 10 else conversation_history
        
        # Build enhanced context string with emotional insights
        context_parts = []
        
        # Add emotional pattern summary
        if emotional_context:
            context_parts.append(f"CONVERSATION EMOTIONAL PATTERN: {emotional_context['pattern']}")
            context_parts.append(f"EMOTIONAL TREND: {emotional_context['trend']}")
            context_parts.append(f"AVERAGE VALENCE: {emotional_context['avg_valence']:.2f}")
            context_parts.append(f"AVERAGE AROUSAL: {emotional_context['avg_arousal']:.2f}")
            context_parts.append("")
        
        # Add recent conversation context
        context_parts.append("RECENT CONVERSATION HISTORY:")
        for i, exchange in enumerate(context_exchanges):
            if 'user' in exchange and 'assistant' in exchange:
                context_parts.append(f"Exchange {i+1}:")
                context_parts.append(f"  User: {exchange['user']}")
                context_parts.append(f"  Assistant: {exchange['assistant']}")
                # Add emotional context if available
                if 'emotion' in exchange:
                    context_parts.append(f"  [Emotional Context: {exchange['emotion']}]")
                context_parts.append("")
        
        if context_parts:
            context_string = "\n".join(context_parts)
            # Enhance the current text with comprehensive conversation context
            enhanced_text = f"COMPREHENSIVE CONVERSATION CONTEXT:\n{context_string}\n\nCURRENT MESSAGE: {text}"
            return enhanced_text
        
        return text
    
    def _analyze_conversation_emotional_patterns(self, conversation_history: List[Dict]) -> Optional[Dict[str, Any]]:
        """
        Analyze the entire conversation history for emotional patterns and trends.
        
        Args:
            conversation_history: Complete conversation history
            
        Returns:
            Dictionary containing emotional pattern analysis
        """
        if not conversation_history or len(conversation_history) == 0:
            return None
        
        # Extract emotional data from conversation history
        emotional_data = []
        for exchange in conversation_history:
            if 'emotion' in exchange and 'valence' in exchange and 'arousal' in exchange:
                emotional_data.append({
                    'emotion': exchange['emotion'],
                    'valence': exchange.get('valence', 0.0),
                    'arousal': exchange.get('arousal', 0.0),
                    'confidence': exchange.get('confidence', 0.5)
                })
        
        if not emotional_data:
            return None
        
        # Calculate patterns
        valences = [item['valence'] for item in emotional_data]
        arousals = [item['arousal'] for item in emotional_data]
        confidences = [item['confidence'] for item in emotional_data]
        
        avg_valence = sum(valences) / len(valences)
        avg_arousal = sum(arousals) / len(arousals)
        avg_confidence = sum(confidences) / len(confidences)
        
        # Determine emotional pattern
        if avg_valence > 0.3 and avg_arousal > 0.5:
            pattern = "Consistently Positive and Energetic"
        elif avg_valence > 0.3 and avg_arousal <= 0.5:
            pattern = "Consistently Positive and Calm"
        elif avg_valence < -0.3 and avg_arousal > 0.5:
            pattern = "Consistently Negative and Stressed"
        elif avg_valence < -0.3 and avg_arousal <= 0.5:
            pattern = "Consistently Negative and Low Energy"
        else:
            pattern = "Mixed Emotional States"
        
        # Determine trend (comparing first half vs second half)
        if len(emotional_data) >= 4:
            mid_point = len(emotional_data) // 2
            first_half_valence = sum(valences[:mid_point]) / mid_point
            second_half_valence = sum(valences[mid_point:]) / (len(valences) - mid_point)
            
            if second_half_valence > first_half_valence + 0.2:
                trend = "Improving Emotional State"
            elif second_half_valence < first_half_valence - 0.2:
                trend = "Declining Emotional State"
            else:
                trend = "Stable Emotional State"
        else:
            trend = "Insufficient Data for Trend Analysis"
        
        return {
            'pattern': pattern,
            'trend': trend,
            'avg_valence': avg_valence,
            'avg_arousal': avg_arousal,
            'avg_confidence': avg_confidence,
            'total_exchanges': len(emotional_data)
        }
    
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
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
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
            # Return original text with basic enhancement if ChatGPT fails
            return f"I'm feeling {text.lower()}" if not any(word in text.lower() for word in ['feeling', 'feel', 'emotion', 'emotional']) else text
    
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
            
            # Check if feedback was detected and adjust strategy
            if emotion_data.get('feedback_detected', False):
                response_strategy = "FEEDBACK_PROBLEM_SOLVING"
                emotional_intensity = "High"  # More assertive for feedback
            
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

ENHANCED RESPONSE STRATEGIES BASED ON VALENCE AND AROUSAL:

**STRATEGY: {response_strategy}**

1. **HIGHLY_EXCITED_DETAILED_EXPLORATION** (Valence: 0.6-1, Arousal: 0.6-1):
   - User is HIGHLY ENTHUSIASTIC and seeking COMPREHENSIVE, DETAILED answers
   - Provide EXTENSIVE, well-researched responses with multiple examples
   - Include data, statistics, and supporting evidence
   - Use VERY ENTHUSIASTIC language that matches their high energy
   - Ask multiple follow-up questions to explore topics deeply
   - Provide comprehensive explanations with multiple perspectives
   - Match their excitement level

2. **HIGHLY_STRESSED_URGENT_SUPPORT** (Valence: -1 to -0.6, Arousal: 0.6-1):
   - User is HIGHLY DISTRESSED and needs IMMEDIATE, CRITICAL support
   - Keep responses EXTREMELY SHORT and DIRECT
   - Provide immediate, actionable solutions
   - Use calm, reassuring language
   - Focus on urgent, practical help
   - Avoid any unnecessary details or tangents
   - Be supportive and understanding

3. **HIGHLY_DEPRESSED_GENTLE_SUPPORT** (Valence: -1 to -0.6, Arousal: 0-0.4):
   - User is HIGHLY DEPRESSED and needs GENTLE, COMPASSIONATE support
   - Use warm, gentle, and encouraging language
   - Provide simple, positive reinforcement
   - Avoid overwhelming them with information
   - Focus on small, achievable steps
   - Be patient and understanding
   - Offer emotional support and validation

4. **HIGHLY_CONTENT_DEEP_CONVERSATION** (Valence: 0.6-1, Arousal: 0-0.4):
   - User is HIGHLY CONTENT and seeking MEANINGFUL, DEEP conversation
   - Engage in thoughtful, philosophical discussions
   - Ask profound, reflective questions
   - Share insights and personal experiences
   - Create a warm, intimate conversational tone
   - Encourage deep thinking and self-reflection
   - Build on their positive emotional state

5. **EXCITED_DETAILED_SEARCH** (Valence: 0.2-0.8, Arousal: 0.5-0.9):
   - User is seeking DETAILED, COMPREHENSIVE answers
   - Provide thorough, well-researched responses with supporting evidence
   - Include specific examples, data, and backing information
   - Use engaging, enthusiastic language that matches their energy
   - Ask follow-up questions to dive deeper into topics
   - Provide multiple perspectives and detailed explanations

6. **STRESSED_URGENT_CLEAR** (Valence: -0.8 to -0.2, Arousal: 0.5-0.9):
   - User needs URGENT, CLEAR, TO-THE-POINT answers
   - Keep responses SHORT and DIRECT - no rambling or unnecessary details
   - Provide immediate, actionable solutions
   - Use clear, concise language
   - Focus on practical, urgent help
   - Avoid lengthy explanations or tangents

7. **BORED_SIMPLE_CLEAR** (Valence: -0.8 to -0.2, Arousal: 0.1-0.5):
   - User needs SIMPLE, CLEAR answers
   - Use straightforward, easy-to-understand language
   - Keep responses concise but complete
   - Avoid complex jargon or lengthy explanations
   - Make information digestible and engaging
   - Use simple, direct communication

8. **CALM_ENGAGING_CONVERSATION** (Valence: 0.2-0.8, Arousal: 0.1-0.5):
   - User needs ENGAGING, TWO-WAY conversation
   - Ask thoughtful questions to encourage dialogue
   - Share personal insights and experiences
   - Create a conversational, friendly tone
   - Encourage back-and-forth discussion
   - Make the interaction feel like a natural conversation

9. **UNCERTAIN_BUT_ENERGETIC_EXPLORATION** (Valence: -0.2-0.2, Arousal: 0.6-1):
   - User is uncertain but energetic - needs GUIDANCE and DIRECTION
   - Provide clear, structured information
   - Help them explore options and possibilities
   - Use encouraging, supportive language
   - Offer multiple approaches to their question
   - Help them clarify their needs

10. **UNCERTAIN_CALM_GUIDANCE** (Valence: -0.2-0.2, Arousal: 0-0.4):
    - User is uncertain and calm - needs GENTLE GUIDANCE
    - Provide clear, simple explanations
    - Use patient, understanding language
    - Offer step-by-step guidance
    - Help them build confidence
    - Be supportive and encouraging

11. **MIXED_EMOTIONS_ADAPTIVE_SUPPORT** (Any valence, moderate arousal):
    - User has mixed emotions - needs ADAPTIVE, FLEXIBLE support
    - Acknowledge the complexity of their situation
    - Provide balanced, nuanced responses
    - Use empathetic, understanding language
    - Help them sort through their feelings
    - Be patient and non-judgmental

12. **FEEDBACK_PROBLEM_SOLVING** (User gave negative feedback):
    - User is frustrated with previous response - needs IMMEDIATE BETTER ANSWER
    - DO NOT apologize or be defensive
    - IMMEDIATELY provide what they asked for
    - Be DIRECT and ACTIONABLE
    - Focus on SOLVING their problem, not explaining
    - Give them exactly what they need, better than before
    - Ask SPECIFIC follow-up questions to get better information
    - Be HELPFUL, not apologetic

CRITICAL RULES:
- Your response MUST match the specific strategy for their emotional state
- Adjust your response length and complexity based on their arousal level
- Match their energy level (high arousal = energetic, low arousal = calm)
- Provide the type of answer they're seeking based on their emotional state
- Use emotional intelligence in every interaction WITHOUT explicitly mentioning their mood
- Respond naturally and conversationally
- PRIORITIZE their emotional state over generic responses
- When users give feedback (like "make it shorter" or "I didn't like that"), IMMEDIATELY provide a better response
- Focus on SOLVING their problem, not apologizing
- Be ACTIONABLE and HELPFUL, not defensive
- Ask SPECIFIC follow-up questions to get better information
- Provide CONCRETE, USEFUL information they can actually use

AVOID:
- Generic responses that ignore emotional context
- Being emotionally tone-deaf to their state
- Overwhelming someone who's already distressed
- Being dismissive of their feelings
- Providing the wrong type of response for their emotional state
- Explicitly mentioning their detected mood or emotional state
- Clinical or analytical language about their emotions
- Defensive responses when users give feedback
- Vague "I'm sorry" responses that don't solve the problem
- Asking "How can I help?" without providing actual help first
- Wasting time with apologies instead of better answers"""
            
            # Create emotionally-aware user prompt with comprehensive conversation context
            history_context = ""
            emotional_trend_context = ""
            
            if conversation_history:
                # Get more comprehensive conversation history (up to 5 exchanges)
                recent_history = conversation_history[-5:] if len(conversation_history) > 5 else conversation_history
                
                # Build detailed conversation context
                history_context = f"\n\nCOMPREHENSIVE CONVERSATION CONTEXT:\n"
                for i, exchange in enumerate(recent_history):
                    history_context += f"Exchange {i+1}:\n"
                    history_context += f"  User: {exchange.get('user', '')}\n"
                    history_context += f"  Assistant: {exchange.get('assistant', '')}\n"
                    
                    # Add emotional context if available
                    if 'emotion' in exchange:
                        history_context += f"  [Previous Emotional State: {exchange.get('emotion', 'Unknown')}]\n"
                    if 'valence' in exchange and 'arousal' in exchange:
                        history_context += f"  [Previous Valence: {exchange.get('valence', 0):.2f}, Arousal: {exchange.get('arousal', 0):.2f}]\n"
                    history_context += "\n"
                
                # Analyze emotional trends from conversation history
                emotional_trends = self._analyze_conversation_emotional_patterns(conversation_history)
                if emotional_trends:
                    emotional_trend_context = f"""
EMOTIONAL TREND ANALYSIS:
- Overall Pattern: {emotional_trends['pattern']}
- Emotional Trend: {emotional_trends['trend']}
- Average Valence: {emotional_trends['avg_valence']:.2f}
- Average Arousal: {emotional_trends['avg_arousal']:.2f}
- Total Exchanges: {emotional_trends['total_exchanges']}
"""
            
            user_prompt = f"""User's message: "{original_text}"

CURRENT EMOTIONAL ANALYSIS (CRITICAL - USE THIS TO SHAPE YOUR RESPONSE):
- Sentiment: {sentiment} (confidence: {confidence:.2f})
- Emotional intensity: {emotional_intensity}
- Valence: {valence:.2f} (positive/negative)
- Arousal: {arousal:.2f} (calm/excited)
- Response Strategy: {response_strategy}

{emotional_trend_context}
{history_context}

FEEDBACK HANDLING RULES:
- If user says "I didn't like that" or "make it shorter/better" - IMMEDIATELY provide a better response
- If user gives negative feedback - SOLVE their problem, don't apologize
- If user asks for something specific - GIVE them exactly what they asked for
- If user seems frustrated - Be DIRECT and HELPFUL, not defensive
- Focus on ACTIONABLE solutions, not explanations

Generate a natural, conversational response that is emotionally appropriate for their current state. Your response should feel like it's coming from someone who truly understands their situation and the emotional journey they've been on. DO NOT explicitly mention their mood or emotional state. Respond naturally and helpfully, taking into account both their current emotional state and the emotional patterns from our conversation history."""
            
            # Adjust temperature based on emotional state
            temperature = self._calculate_response_temperature(emotion_data)
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
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
            # Enhanced fallback with conversation context
            fallback_response = self.generate_adaptive_response(emotion_data)
            
            # Add conversation context to fallback if available
            if conversation_history and len(conversation_history) > 0:
                recent_context = conversation_history[-1].get('user', '') if conversation_history else ''
                if recent_context:
                    fallback_response += f" I understand you mentioned '{recent_context[:50]}...' earlier."
            
            return fallback_response

    def process_text(self, text: str, session_id: Optional[str] = None,
                    context: Optional[str] = None, conversation_history: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Main processing method that handles the complete emotion detection pipeline.
        Now considers conversation history for better context-aware responses.
        
        Args:
            text: Input text to analyze
            session_id: Optional session identifier
            context: Optional context for personalized responses
            conversation_history: Previous conversation context for better responses
            
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
        
        # Enhanced text processing with comprehensive conversation context
        enhanced_text = self._enhance_text_with_context(cleaned_text, conversation_history)
        
        # Rephrase with ChatGPT for better analysis (using enhanced text)
        rephrased_text = self.rephrase_with_chatgpt(enhanced_text)
        
        # Detect language
        language = self.detect_language(rephrased_text)
        
        # Analyze sentiment using rephrased text
        sentiment_result = self.analyze_sentiment(rephrased_text, language or 'en')
        sentiment = sentiment_result['Sentiment']
        scores = sentiment_result['SentimentScore']
        
        # Map to emotion
        emotion_data = self.map_sentiment_to_emotion(sentiment, scores)
        
        # Add conversation context to emotion data for better responses
        emotion_data['sentiment_scores'] = scores
        emotion_data['sentiment'] = sentiment
        
        # Detect feedback and adjust strategy accordingly
        emotion_data = self._detect_feedback_and_adjust_strategy(cleaned_text, emotion_data)
        
        # Analyze conversation history for emotional trends and patterns
        if conversation_history:
            emotional_trends = self._analyze_conversation_emotional_patterns(conversation_history)
            if emotional_trends:
                # Adjust current emotion based on conversation trends
                emotion_data['conversation_trend'] = emotional_trends['trend']
                emotion_data['conversation_pattern'] = emotional_trends['pattern']
                
                # Slightly adjust valence based on conversation trend
                if emotional_trends['trend'] == 'Improving Emotional State':
                    emotion_data['valence'] = min(1.0, emotion_data['valence'] + 0.1)
                elif emotional_trends['trend'] == 'Declining Emotional State':
                    emotion_data['valence'] = max(-1.0, emotion_data['valence'] - 0.1)
        
        # Generate conversational response with ChatGPT (now with full conversation history and trends)
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
