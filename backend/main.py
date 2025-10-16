"""
FastAPI backend for emotion detection web app.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
import logging
import uuid
from datetime import datetime

from agent.state_agent import StateAgent
from services.database_service import DatabaseService
from models.database import create_tables

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Emotion Detection API",
    description="API for emotion detection using Amazon Comprehend and intelligent agent",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize State Agent and Database Service
state_agent = StateAgent()
db_service = DatabaseService()


@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup."""
    create_tables()
    logger.info("Database tables created successfully")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Emotion Detection API",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "/analyze",
            "history": "/history/{session_id}",
            "trends": "/trends/{session_id}",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.post("/analyze")
async def analyze_emotion(request: Request):
    """
    Analyze emotion from text input using Amazon Comprehend and State Agent.
    
    Request body:
    - text: string (required) - Text to analyze
    - session_id: string (optional) - Session identifier
    - context: string (optional) - Additional context for analysis
    - conversation_history: array (optional) - Previous conversation context
    """
    try:
        data = await request.json()
        text = data.get("text", "").strip()
        session_id = data.get("session_id")
        context = data.get("context")
        conversation_history = data.get("conversation_history", [])
        
        if not text:
            raise HTTPException(status_code=400, detail="Text input is required")
        
        # Generate session ID if not provided
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Process text through State Agent with conversation history
        result = state_agent.process_text(text, session_id, context, conversation_history)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        # Store analysis in database using unified service
        analysis_id = db_service.save_emotion_analysis(result)
        
        # Update session
        db_service.update_session(session_id, 1)  # Increment by 1
        
        # Return analysis result
        return {
            "success": True,
            "analysis": result,
            "session_id": session_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in analyze_emotion: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/history/{session_id}")
async def get_session_history(session_id: str, limit: int = 50):
    """
    Get analysis history for a specific session.
    
    Args:
        session_id: Session identifier
        limit: Maximum number of results to return
    """
    try:
        analyses = db_service.get_session_history(session_id, limit)
        
        return {
            "session_id": session_id,
            "total_analyses": len(analyses),
            "history": analyses
        }
        
    except Exception as e:
        logger.error(f"Error getting session history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving history: {str(e)}")


@app.get("/trends/{session_id}")
async def get_emotional_trends(session_id: str):
    """
    Get emotional trends for a specific session.
    
    Args:
        session_id: Session identifier
    """
    try:
        # Get all analyses for the session
        analyses = db_service.get_session_history(session_id, 1000)  # Get more for trend analysis
        
        # Get trends from State Agent
        trends = state_agent.get_emotional_trends(analyses)
        
        return {
            "session_id": session_id,
            "trends": trends,
            "total_analyses": len(analyses)
        }
        
    except Exception as e:
        logger.error(f"Error getting emotional trends: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving trends: {str(e)}")


@app.get("/sessions")
async def get_all_sessions(limit: int = 20):
    """
    Get all user sessions with summary information.
    
    Args:
        limit: Maximum number of sessions to return
    """
    try:
        sessions = db_service.get_all_sessions(limit)
        
        return {
            "total_sessions": len(sessions),
            "sessions": sessions
        }
        
    except Exception as e:
        logger.error(f"Error getting sessions: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving sessions: {str(e)}")


@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """
    Delete a session and all its analyses.
    
    Args:
        session_id: Session identifier to delete
    """
    try:
        # Delete session and all analyses using unified service
        db_service.delete_session(session_id)
        
        return {"message": f"Session {session_id} and all analyses deleted successfully"}
        
    except Exception as e:
        logger.error(f"Error deleting session: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting session: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
