#!/usr/bin/env python3
"""
Test script for ChatGPT 4 Mini integration with Amazon Comprehend
"""

import os
import sys
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.state_agent import StateAgent

def test_chatgpt_integration():
    """Test the ChatGPT integration with emotion analysis."""
    
    # Load environment variables
    load_dotenv()
    
    # Check if ChatGPT API key is available
    if not os.getenv('chatgptapi'):
        print("❌ chatgptapi not found in environment variables")
        print("Please add your ChatGPT API key to the .env file")
        return False
    
    # Initialize the State Agent
    print("🤖 Initializing State Agent with ChatGPT integration...")
    agent = StateAgent()
    
    # Enhanced test cases for better response testing
    test_cases = [
        "I'm feeling really stressed about work",
        "I had an amazing day today!",
        "I don't know what to do anymore",
        "Everything is going wrong in my life",
        "I'm so excited about my new project",
        "I feel lost and confused",
        "I'm worried about my future",
        "I'm proud of what I accomplished",
        "I feel alone and isolated",
        "I'm grateful for my friends"
    ]
    
    print("\n🧪 Testing ChatGPT integration with emotion analysis...\n")
    
    for i, test_text in enumerate(test_cases, 1):
        print(f"Test {i}: '{test_text}'")
        print("-" * 50)
        
        try:
            # Process the text
            result = agent.process_text(test_text, session_id=f"test_{i}")
            
            # Display results with better formatting
            print(f"✅ Original: {result['original_text']}")
            print(f"🔄 Enhanced: {result.get('rephrased_text', 'N/A')}")
            print(f"😊 Emotion: {result['emotion']}")
            print(f"📊 Sentiment: {result['sentiment']} (confidence: {result['confidence']:.2f})")
            print(f"💬 Intelligent Response:")
            print(f"   {result['adaptive_response']}")
            print("=" * 60)
            print()
            
        except Exception as e:
            print(f"❌ Error processing text: {e}")
            print()
    
    print("✅ ChatGPT integration test completed!")
    return True

if __name__ == "__main__":
    test_chatgpt_integration()
