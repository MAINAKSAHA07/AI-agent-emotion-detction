"""
Database service for handling both SQL and DynamoDB operations.
Provides a unified interface for database operations.
"""

import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from models.database import (
    EmotionAnalysis, UserSession, get_db, get_dynamodb_table, 
    USE_DYNAMODB
)


class DatabaseService:
    """Unified database service for SQL and DynamoDB operations."""
    
    def __init__(self):
        self.use_dynamodb = USE_DYNAMODB
        if self.use_dynamodb:
            self.emotion_table = get_dynamodb_table('emotion_analyses')
            self.sessions_table = get_dynamodb_table('user_sessions')
    
    def save_emotion_analysis(self, analysis_data: Dict[str, Any]) -> str:
        """Save emotion analysis to database."""
        if self.use_dynamodb:
            return self._save_emotion_analysis_dynamodb(analysis_data)
        else:
            return self._save_emotion_analysis_sql(analysis_data)
    
    def _save_emotion_analysis_dynamodb(self, analysis_data: Dict[str, Any]) -> str:
        """Save emotion analysis to DynamoDB."""
        analysis_id = str(uuid.uuid4())
        
        item = {
            'id': analysis_id,
            'session_id': analysis_data.get('session_id'),
            'input_text': analysis_data.get('input_text'),
            'original_text': analysis_data.get('original_text'),
            'language': analysis_data.get('language'),
            'sentiment': analysis_data.get('sentiment'),
            'sentiment_scores': analysis_data.get('sentiment_scores'),
            'emotion': analysis_data.get('emotion'),
            'valence': analysis_data.get('valence'),
            'arousal': analysis_data.get('arousal'),
            'confidence': analysis_data.get('confidence'),
            'adaptive_response': analysis_data.get('adaptive_response'),
            'timestamp': datetime.utcnow().isoformat()
        }
        
        self.emotion_table.put_item(Item=item)
        return analysis_id
    
    def _save_emotion_analysis_sql(self, analysis_data: Dict[str, Any]) -> str:
        """Save emotion analysis to SQL database."""
        db = next(get_db())
        try:
            analysis = EmotionAnalysis(
                session_id=analysis_data.get('session_id'),
                input_text=analysis_data.get('input_text'),
                original_text=analysis_data.get('original_text'),
                language=analysis_data.get('language'),
                sentiment=analysis_data.get('sentiment'),
                sentiment_scores=analysis_data.get('sentiment_scores'),
                emotion=analysis_data.get('emotion'),
                valence=analysis_data.get('valence'),
                arousal=analysis_data.get('arousal'),
                confidence=analysis_data.get('confidence'),
                adaptive_response=analysis_data.get('adaptive_response')
            )
            
            db.add(analysis)
            db.commit()
            db.refresh(analysis)
            return str(analysis.id)
        finally:
            db.close()
    
    def get_session_history(self, session_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get analysis history for a session."""
        if self.use_dynamodb:
            return self._get_session_history_dynamodb(session_id, limit)
        else:
            return self._get_session_history_sql(session_id, limit)
    
    def _get_session_history_dynamodb(self, session_id: str, limit: int) -> List[Dict[str, Any]]:
        """Get session history from DynamoDB."""
        response = self.emotion_table.query(
            IndexName='session-index',
            KeyConditionExpression='session_id = :session_id',
            ExpressionAttributeValues={':session_id': session_id},
            ScanIndexForward=False,  # Sort by timestamp descending
            Limit=limit
        )
        
        return [item for item in response.get('Items', [])]
    
    def _get_session_history_sql(self, session_id: str, limit: int) -> List[Dict[str, Any]]:
        """Get session history from SQL database."""
        db = next(get_db())
        try:
            analyses = db.query(EmotionAnalysis).filter(
                EmotionAnalysis.session_id == session_id
            ).order_by(EmotionAnalysis.timestamp.desc()).limit(limit).all()
            
            return [analysis.to_dict() for analysis in analyses]
        finally:
            db.close()
    
    def update_session(self, session_id: str, total_analyses: int = None):
        """Update or create user session."""
        if self.use_dynamodb:
            self._update_session_dynamodb(session_id, total_analyses)
        else:
            self._update_session_sql(session_id, total_analyses)
    
    def _update_session_dynamodb(self, session_id: str, total_analyses: int = None):
        """Update session in DynamoDB."""
        try:
            # Try to get existing session
            response = self.sessions_table.get_item(Key={'session_id': session_id})
            
            if 'Item' in response:
                # Update existing session
                update_expression = "SET last_activity = :timestamp"
                expression_values = {':timestamp': datetime.utcnow().isoformat()}
                
                if total_analyses is not None:
                    update_expression += ", total_analyses = :total"
                    expression_values[':total'] = total_analyses
                
                self.sessions_table.update_item(
                    Key={'session_id': session_id},
                    UpdateExpression=update_expression,
                    ExpressionAttributeValues=expression_values
                )
            else:
                # Create new session
                self.sessions_table.put_item(Item={
                    'session_id': session_id,
                    'created_at': datetime.utcnow().isoformat(),
                    'last_activity': datetime.utcnow().isoformat(),
                    'total_analyses': total_analyses or 1,
                    'emotional_trend': None
                })
        except Exception as e:
            print(f"Error updating session in DynamoDB: {e}")
    
    def _update_session_sql(self, session_id: str, total_analyses: int = None):
        """Update session in SQL database."""
        db = next(get_db())
        try:
            session = db.query(UserSession).filter(UserSession.session_id == session_id).first()
            
            if session:
                session.last_activity = datetime.utcnow()
                if total_analyses is not None:
                    session.total_analyses = total_analyses
            else:
                session = UserSession(
                    session_id=session_id,
                    total_analyses=total_analyses or 1
                )
                db.add(session)
            
            db.commit()
        finally:
            db.close()
    
    def get_all_sessions(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get all user sessions."""
        if self.use_dynamodb:
            return self._get_all_sessions_dynamodb(limit)
        else:
            return self._get_all_sessions_sql(limit)
    
    def _get_all_sessions_dynamodb(self, limit: int) -> List[Dict[str, Any]]:
        """Get all sessions from DynamoDB."""
        response = self.sessions_table.scan(Limit=limit)
        return response.get('Items', [])
    
    def _get_all_sessions_sql(self, limit: int) -> List[Dict[str, Any]]:
        """Get all sessions from SQL database."""
        db = next(get_db())
        try:
            sessions = db.query(UserSession).order_by(
                UserSession.last_activity.desc()
            ).limit(limit).all()
            
            return [session.to_dict() for session in sessions]
        finally:
            db.close()
    
    def delete_session(self, session_id: str):
        """Delete a session and all its analyses."""
        if self.use_dynamodb:
            self._delete_session_dynamodb(session_id)
        else:
            self._delete_session_sql(session_id)
    
    def _delete_session_dynamodb(self, session_id: str):
        """Delete session from DynamoDB."""
        # Delete all analyses for the session
        response = self.emotion_table.query(
            IndexName='session-index',
            KeyConditionExpression='session_id = :session_id',
            ExpressionAttributeValues={':session_id': session_id}
        )
        
        for item in response.get('Items', []):
            self.emotion_table.delete_item(Key={'id': item['id']})
        
        # Delete the session
        self.sessions_table.delete_item(Key={'session_id': session_id})
    
    def _delete_session_sql(self, session_id: str):
        """Delete session from SQL database."""
        db = next(get_db())
        try:
            # Delete all analyses for the session
            db.query(EmotionAnalysis).filter(
                EmotionAnalysis.session_id == session_id
            ).delete()
            
            # Delete the session
            db.query(UserSession).filter(
                UserSession.session_id == session_id
            ).delete()
            
            db.commit()
        finally:
            db.close()
