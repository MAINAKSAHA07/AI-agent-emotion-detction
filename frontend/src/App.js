import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { Brain } from 'lucide-react';
import API_BASE_URL from './config';
import EmotionAnalyzer from './components/EmotionAnalyzer';
import EmotionAgent from './components/EmotionAgent';
import AgentAnalysisResults from './components/AgentAnalysisResults';
import EmotionHistory from './components/EmotionHistory';
import EmotionTrends from './components/EmotionTrends';
import Header from './components/Header';
import './index.css';

function App() {
  const [currentSession, setCurrentSession] = useState(null);
  const [analyses, setAnalyses] = useState([]);
  const [trends, setTrends] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentAnalysis, setCurrentAnalysis] = useState(null);
  const [viewMode, setViewMode] = useState('agent'); // 'agent' or 'classic'

  // Generate or retrieve session ID
  useEffect(() => {
    const sessionId = localStorage.getItem('emotionSessionId') || generateSessionId();
    localStorage.setItem('emotionSessionId', sessionId);
    setCurrentSession(sessionId);
  }, []);

  const generateSessionId = () => {
    return 'session_' + Math.random().toString(36).substr(2, 9);
  };

  const analyzeEmotion = async (text, context = '') => {
    if (!text.trim()) {
      setError('Please enter some text to analyze');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/analyze`, {
        text: text,
        session_id: currentSession,
        context: context
      });

      const analysis = response.data.analysis;
      setAnalyses(prev => [analysis, ...prev]);
      setCurrentAnalysis(analysis);
      
      // Refresh trends after new analysis
      await loadTrends();
      
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to analyze emotion');
    } finally {
      setLoading(false);
    }
  };

  const loadHistory = useCallback(async () => {
    if (!currentSession) return;

    try {
      const response = await axios.get(`${API_BASE_URL}/history/${currentSession}`);
      setAnalyses(response.data.history);
    } catch (err) {
      console.error('Failed to load history:', err);
    }
  }, [currentSession]);

  const loadTrends = useCallback(async () => {
    if (!currentSession) return;

    try {
      const response = await axios.get(`${API_BASE_URL}/trends/${currentSession}`);
      setTrends(response.data.trends);
    } catch (err) {
      console.error('Failed to load trends:', err);
    }
  }, [currentSession]);

  const clearSession = () => {
    setAnalyses([]);
    setTrends(null);
    setCurrentAnalysis(null);
    const newSessionId = generateSessionId();
    localStorage.setItem('emotionSessionId', newSessionId);
    setCurrentSession(newSessionId);
  };

  const startNewAnalysis = () => {
    setCurrentAnalysis(null);
  };

  useEffect(() => {
    if (currentSession) {
      loadHistory();
      loadTrends();
    }
  }, [currentSession, loadHistory, loadTrends]);

  return (
    <div className="min-h-screen bg-gray-50">
      <Header 
        sessionId={currentSession}
        onClearSession={clearSession}
        viewMode={viewMode}
        onViewModeChange={setViewMode}
      />
      
      <main className="container mx-auto px-4 py-8">
        {viewMode === 'agent' ? (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Agent Chat Interface */}
            <div>
              <EmotionAgent 
                onAnalyze={analyzeEmotion}
                loading={loading}
                error={error}
                sessionId={currentSession}
              />
            </div>
            
            {/* Analysis Results */}
            <div>
              {currentAnalysis ? (
                <AgentAnalysisResults 
                  analysis={currentAnalysis}
                  onNewAnalysis={startNewAnalysis}
                />
              ) : (
                <div className="bg-white rounded-lg shadow-lg p-8 text-center">
                  <div className="bg-gradient-to-r from-purple-100 to-blue-100 rounded-full w-16 h-16 mx-auto mb-4 flex items-center justify-center">
                    <Brain className="h-8 w-8 text-purple-600" />
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    Ready to Analyze
                  </h3>
                  <p className="text-gray-600">
                    Start a conversation with the AI agent to analyze your emotions and get personalized insights.
                  </p>
                </div>
              )}
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Main Analysis Section */}
            <div className="lg:col-span-2">
              <EmotionAnalyzer 
                onAnalyze={analyzeEmotion}
                loading={loading}
                error={error}
              />
              
              {analyses.length > 0 && (
                <div className="mt-8">
                  <EmotionHistory 
                    analyses={analyses}
                    onRefresh={loadHistory}
                  />
                </div>
              )}
            </div>
            
            {/* Trends Sidebar */}
            <div className="lg:col-span-1">
              <EmotionTrends 
                trends={trends}
                sessionId={currentSession}
                onRefresh={loadTrends}
              />
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
