#!/usr/bin/env python3
"""
Test script to verify AWS Comprehend connection and functionality
"""

import boto3
import os
import sys
from dotenv import load_dotenv

def test_aws_connection():
    """Test AWS Comprehend connection and basic functionality"""
    
    print("🧪 Testing AWS Comprehend Connection...")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check if AWS credentials are set
    access_key = os.getenv('AWS_ACCESS_KEY_ID')
    secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    region = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    
    if not access_key or not secret_key:
        print("❌ AWS credentials not found!")
        print("Please set the following in your .env file:")
        print("AWS_ACCESS_KEY_ID=your_access_key")
        print("AWS_SECRET_ACCESS_KEY=your_secret_key")
        print("AWS_DEFAULT_REGION=us-east-1")
        return False
    
    print(f"✅ AWS credentials found")
    print(f"📍 Region: {region}")
    
    try:
        # Initialize Comprehend client
        print("\n🔗 Connecting to AWS Comprehend...")
        comprehend = boto3.client(
            'comprehend',
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
        
        # Test basic sentiment analysis
        print("📝 Testing sentiment analysis...")
        test_texts = [
            "I am so happy and excited about this new project!",
            "I feel really disappointed and frustrated with the results.",
            "The weather is okay today, nothing special.",
            "I'm happy but also a bit nervous about the presentation."
        ]
        
        for i, text in enumerate(test_texts, 1):
            print(f"\n📄 Test {i}: \"{text}\"")
            
            try:
                response = comprehend.detect_sentiment(
                    Text=text,
                    LanguageCode='en'
                )
                
                sentiment = response['Sentiment']
                scores = response['SentimentScore']
                confidence = max(scores.values())
                
                print(f"   🎯 Sentiment: {sentiment}")
                print(f"   📊 Confidence: {confidence:.2f}")
                print(f"   📈 Scores: {scores}")
                
            except Exception as e:
                print(f"   ❌ Error analyzing text: {e}")
                return False
        
        # Test language detection
        print(f"\n🌍 Testing language detection...")
        try:
            lang_response = comprehend.detect_dominant_language(
                Text="Hello, how are you today?"
            )
            languages = lang_response['Languages']
            if languages:
                dominant_lang = languages[0]
                print(f"   🗣️  Detected language: {dominant_lang['LanguageCode']}")
                print(f"   📊 Confidence: {dominant_lang['Score']:.2f}")
        except Exception as e:
            print(f"   ⚠️  Language detection failed: {e}")
        
        print("\n✅ AWS Comprehend connection successful!")
        print("🎉 Your emotion detection app is ready to use!")
        return True
        
    except Exception as e:
        print(f"\n❌ AWS connection failed: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Check your AWS credentials in .env file")
        print("2. Verify your AWS account has Comprehend access")
        print("3. Ensure your IAM user has 'AmazonComprehendFullAccess' policy")
        print("4. Check if you're in the correct AWS region")
        return False

def test_state_agent():
    """Test the State Agent integration"""
    
    print("\n" + "=" * 50)
    print("🤖 Testing State Agent Integration...")
    
    try:
        from agent.state_agent import StateAgent
        
        # Initialize State Agent
        agent = StateAgent()
        
        # Test emotion processing
        test_text = "I am feeling really excited about this new opportunity!"
        print(f"📝 Testing with: \"{test_text}\"")
        
        result = agent.process_text(test_text, session_id="test_session")
        
        if "error" in result:
            print(f"❌ State Agent error: {result['error']}")
            return False
        
        print("✅ State Agent processing successful!")
        print(f"   🎯 Sentiment: {result['sentiment']}")
        print(f"   😊 Emotion: {result['emotion']}")
        print(f"   📊 Valence: {result['valence']}")
        print(f"   🔥 Arousal: {result['arousal']}")
        print(f"   📈 Confidence: {result['confidence']}")
        print(f"   💬 Response: {result['adaptive_response']}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Cannot import State Agent: {e}")
        return False
    except Exception as e:
        print(f"❌ State Agent error: {e}")
        return False

def main():
    """Main test function"""
    
    print("🧠 Emotion Detection App - AWS Connection Test")
    print("=" * 60)
    
    # Test AWS connection
    aws_success = test_aws_connection()
    
    if aws_success:
        # Test State Agent
        agent_success = test_state_agent()
        
        if agent_success:
            print("\n🎉 All tests passed! Your app is ready to run.")
            print("\n🚀 Next steps:")
            print("1. Start the backend: python -m uvicorn backend.main:app --reload")
            print("2. Test the API: curl http://localhost:8000/health")
            print("3. Start Streamlit: streamlit run streamlit_app.py")
        else:
            print("\n⚠️  AWS connection works, but State Agent has issues.")
    else:
        print("\n❌ AWS connection failed. Please fix credentials first.")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
