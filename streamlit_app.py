"""
Streamlit MVP for Emotion Detection App
Quick alternative to the React frontend for testing and demos
"""

import streamlit as st
import requests
import json
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configure page
st.set_page_config(
    page_title="Emotion Detection App",
    page_icon="🧠",
    layout="wide"
)

# API base URL
API_BASE = "http://localhost:8000"

def analyze_emotion(text, context=""):
    """Analyze emotion using the API"""
    try:
        response = requests.post(
            f"{API_BASE}/analyze",
            json={"text": text, "context": context}
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to API. Make sure the backend is running on port 8000.")
        return None

def get_session_history(session_id):
    """Get analysis history for session"""
    try:
        response = requests.get(f"{API_BASE}/history/{session_id}")
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def get_emotional_trends(session_id):
    """Get emotional trends for session"""
    try:
        response = requests.get(f"{API_BASE}/trends/{session_id}")
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

# Initialize session state
if 'session_id' not in st.session_state:
    st.session_state.session_id = f"streamlit_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

if 'analyses' not in st.session_state:
    st.session_state.analyses = []

# Main app
st.title("🧠 Emotion Detection App")
st.markdown("**Powered by Amazon Comprehend & AI Agent**")

# Sidebar
with st.sidebar:
    st.header("Session Info")
    st.write(f"Session: {st.session_state.session_id}")
    
    if st.button("🔄 Refresh Data"):
        history = get_session_history(st.session_state.session_id)
        if history:
            st.session_state.analyses = history.get('history', [])
        st.rerun()
    
    if st.button("🗑️ Clear Session"):
        st.session_state.analyses = []
        st.session_state.session_id = f"streamlit_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        st.rerun()

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📝 Analyze Your Emotions")
    
    # Input form
    with st.form("emotion_form"):
        text_input = st.text_area(
            "What's on your mind?",
            placeholder="Share your thoughts, feelings, or experiences...",
            height=100
        )
        
        context_input = st.text_input(
            "Additional Context (Optional)",
            placeholder="e.g., work, relationships, health..."
        )
        
        submitted = st.form_submit_button("🔍 Analyze Emotion", use_container_width=True)
        
        if submitted and text_input:
            with st.spinner("Analyzing emotion..."):
                result = analyze_emotion(text_input, context_input)
                
                if result and result.get('success'):
                    analysis = result['analysis']
                    st.session_state.analyses.insert(0, analysis)
                    st.success("Analysis complete!")
                    st.rerun()
                elif result:
                    st.error(f"Analysis failed: {result.get('detail', 'Unknown error')}")

    # Display recent analysis
    if st.session_state.analyses:
        st.header("📊 Recent Analysis")
        
        latest = st.session_state.analyses[0]
        
        # Emotion card
        emotion_color = {
            'POSITIVE': '🟢',
            'NEGATIVE': '🔴', 
            'NEUTRAL': '🟡',
            'MIXED': '🟠'
        }.get(latest.get('sentiment', 'NEUTRAL'), '⚪')
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.metric(
                "Sentiment",
                f"{emotion_color} {latest.get('sentiment', 'Unknown')}",
                f"{latest.get('confidence', 0)*100:.1f}% confidence"
            )
        
        with col_b:
            st.metric(
                "Emotion",
                latest.get('emotion', 'Unknown'),
                f"Valence: {latest.get('valence', 0):.2f}"
            )
        
        with col_c:
            st.metric(
                "Arousal",
                f"{latest.get('arousal', 0):.2f}",
                f"Language: {latest.get('language', 'Unknown')}"
            )
        
        # Adaptive response
        if latest.get('adaptive_response'):
            st.info(f"💬 **AI Response:** {latest['adaptive_response']}")

with col2:
    st.header("📈 Trends & Insights")
    
    if st.session_state.analyses:
        # Convert to DataFrame for visualization
        df = pd.DataFrame(st.session_state.analyses)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Valence over time
        fig_valence = px.line(
            df, 
            x='timestamp', 
            y='valence',
            title='Emotional Valence Over Time',
            labels={'valence': 'Valence', 'timestamp': 'Time'}
        )
        fig_valence.add_hline(y=0, line_dash="dash", line_color="gray")
        st.plotly_chart(fig_valence, use_container_width=True)
        
        # Confidence distribution
        fig_confidence = px.histogram(
            df,
            x='confidence',
            title='Confidence Distribution',
            labels={'confidence': 'Confidence Score', 'count': 'Frequency'}
        )
        st.plotly_chart(fig_confidence, use_container_width=True)
        
        # Sentiment pie chart
        sentiment_counts = df['sentiment'].value_counts()
        fig_sentiment = px.pie(
            values=sentiment_counts.values,
            names=sentiment_counts.index,
            title='Sentiment Distribution'
        )
        st.plotly_chart(fig_sentiment, use_container_width=True)
        
        # Summary stats
        st.subheader("📊 Summary")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total Analyses", len(df))
            st.metric("Avg Valence", f"{df['valence'].mean():.2f}")
        
        with col2:
            st.metric("Avg Confidence", f"{df['confidence'].mean()*100:.1f}%")
            st.metric("Most Common", df['sentiment'].mode().iloc[0] if not df.empty else "N/A")
    
    else:
        st.info("No analyses yet. Start by analyzing some text above!")

# Footer
st.markdown("---")
st.markdown(
    "**Emotion Detection App** | Built with Streamlit, FastAPI, and Amazon Comprehend | "
    f"Session: {st.session_state.session_id}"
)
