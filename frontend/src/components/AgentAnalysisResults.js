import React from 'react';
import { 
  Brain, 
  Heart, 
  TrendingUp, 
  TrendingDown, 
  Minus, 
  AlertCircle,
  MessageCircle,
  Zap,
  Target,
  BarChart3
} from 'lucide-react';

const AgentAnalysisResults = ({ analysis, onNewAnalysis }) => {
  if (!analysis) return null;

  const getEmotionIcon = (emotion) => {
    if (!emotion) return <Brain className="h-5 w-5 text-purple-500" />;
    
    if (emotion.toLowerCase().includes('joy') || emotion.toLowerCase().includes('optimism')) {
      return <TrendingUp className="h-5 w-5 text-green-500" />;
    } else if (emotion.toLowerCase().includes('sadness') || emotion.toLowerCase().includes('anger') || emotion.toLowerCase().includes('fear')) {
      return <TrendingDown className="h-5 w-5 text-red-500" />;
    } else if (emotion.toLowerCase().includes('calm') || emotion.toLowerCase().includes('indifference')) {
      return <Minus className="h-5 w-5 text-blue-500" />;
    } else if (emotion.toLowerCase().includes('conflicted') || emotion.toLowerCase().includes('uncertain')) {
      return <AlertCircle className="h-5 w-5 text-yellow-500" />;
    }
    return <Heart className="h-5 w-5 text-purple-500" />;
  };

  const getEmotionColor = (emotion) => {
    if (!emotion) return 'border-purple-200 bg-purple-50';
    
    if (emotion.toLowerCase().includes('joy') || emotion.toLowerCase().includes('optimism')) {
      return 'border-green-200 bg-green-50';
    } else if (emotion.toLowerCase().includes('sadness') || emotion.toLowerCase().includes('anger') || emotion.toLowerCase().includes('fear')) {
      return 'border-red-200 bg-red-50';
    } else if (emotion.toLowerCase().includes('calm') || emotion.toLowerCase().includes('indifference')) {
      return 'border-blue-200 bg-blue-50';
    } else if (emotion.toLowerCase().includes('conflicted') || emotion.toLowerCase().includes('uncertain')) {
      return 'border-yellow-200 bg-yellow-50';
    }
    return 'border-purple-200 bg-purple-50';
  };

  const getSentimentColor = (sentiment) => {
    switch (sentiment) {
      case 'POSITIVE': return 'text-green-600 bg-green-100';
      case 'NEGATIVE': return 'text-red-600 bg-red-100';
      case 'NEUTRAL': return 'text-blue-600 bg-blue-100';
      case 'MIXED': return 'text-yellow-600 bg-yellow-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getConfidenceLevel = (confidence) => {
    if (confidence >= 0.8) return { level: 'High', color: 'text-green-600' };
    if (confidence >= 0.6) return { level: 'Medium', color: 'text-yellow-600' };
    return { level: 'Low', color: 'text-red-600' };
  };

  const getValenceDescription = (valence) => {
    if (valence > 0.5) return 'Very Positive';
    if (valence > 0.1) return 'Positive';
    if (valence > -0.1) return 'Neutral';
    if (valence > -0.5) return 'Negative';
    return 'Very Negative';
  };

  const getArousalDescription = (arousal) => {
    if (arousal > 0.7) return 'High Energy';
    if (arousal > 0.3) return 'Moderate Energy';
    if (arousal > -0.3) return 'Calm';
    return 'Low Energy';
  };

  const confidence = getConfidenceLevel(analysis.confidence);

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="bg-gradient-to-r from-purple-500 to-blue-500 p-2 rounded-full">
            <Brain className="h-5 w-5 text-white" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">Agent Analysis</h3>
            <p className="text-sm text-gray-500">AI-powered emotional intelligence insights</p>
          </div>
        </div>
        <button
          onClick={onNewAnalysis}
          className="text-purple-600 hover:text-purple-700 text-sm font-medium"
        >
          New Analysis
        </button>
      </div>

      {/* Main Emotion Card */}
      <div className={`rounded-lg border-2 p-4 ${getEmotionColor(analysis.emotion)}`}>
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center space-x-2">
            {getEmotionIcon(analysis.emotion)}
            <span className="text-lg font-semibold text-gray-900">
              {analysis.emotion || 'Processing...'}
            </span>
          </div>
          <div className="flex items-center space-x-2">
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSentimentColor(analysis.sentiment)}`}>
              {analysis.sentiment}
            </span>
            <span className={`text-xs font-medium ${confidence.color}`}>
              {confidence.level} Confidence
            </span>
          </div>
        </div>
        
        <p className="text-gray-700 text-sm mb-3">
          "{analysis.input_text}"
        </p>
        
        {analysis.adaptive_response && (
          <div className="bg-white/50 rounded-lg p-3 border border-gray-200">
            <div className="flex items-start space-x-2">
              <MessageCircle className="h-4 w-4 text-purple-500 mt-0.5 flex-shrink-0" />
              <div>
                <p className="text-sm font-medium text-gray-700 mb-1">Agent Response:</p>
                <p className="text-sm text-gray-600">{analysis.adaptive_response}</p>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Detailed Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Sentiment Scores */}
        <div className="bg-gray-50 rounded-lg p-4">
          <div className="flex items-center space-x-2 mb-3">
            <BarChart3 className="h-4 w-4 text-gray-600" />
            <h4 className="font-medium text-gray-900">Sentiment Breakdown</h4>
          </div>
          <div className="space-y-2">
            {analysis.sentiment_scores && Object.entries(analysis.sentiment_scores).map(([key, value]) => (
              <div key={key} className="flex justify-between items-center">
                <span className="text-sm text-gray-600 capitalize">{key.toLowerCase()}</span>
                <div className="flex items-center space-x-2">
                  <div className="w-16 bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-purple-500 h-2 rounded-full" 
                      style={{ width: `${value * 100}%` }}
                    ></div>
                  </div>
                  <span className="text-xs text-gray-500 w-8">
                    {(value * 100).toFixed(1)}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Emotional Dimensions */}
        <div className="bg-gray-50 rounded-lg p-4">
          <div className="flex items-center space-x-2 mb-3">
            <Target className="h-4 w-4 text-gray-600" />
            <h4 className="font-medium text-gray-900">Emotional Dimensions</h4>
          </div>
          <div className="space-y-3">
            <div>
              <div className="flex justify-between items-center mb-1">
                <span className="text-sm text-gray-600">Valence</span>
                <span className="text-xs text-gray-500">
                  {getValenceDescription(analysis.valence)}
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className={`h-2 rounded-full ${
                    analysis.valence > 0 ? 'bg-green-500' : 'bg-red-500'
                  }`}
                  style={{ 
                    width: `${Math.abs(analysis.valence) * 100}%`,
                    marginLeft: analysis.valence < 0 ? `${100 - Math.abs(analysis.valence) * 100}%` : '0'
                  }}
                ></div>
              </div>
              <span className="text-xs text-gray-500">
                {analysis.valence > 0 ? '+' : ''}{analysis.valence.toFixed(2)}
              </span>
            </div>
            
            <div>
              <div className="flex justify-between items-center mb-1">
                <span className="text-sm text-gray-600">Arousal</span>
                <span className="text-xs text-gray-500">
                  {getArousalDescription(analysis.arousal)}
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-blue-500 h-2 rounded-full"
                  style={{ width: `${analysis.arousal * 100}%` }}
                ></div>
              </div>
              <span className="text-xs text-gray-500">
                {analysis.arousal.toFixed(2)}
              </span>
            </div>
          </div>
        </div>

        {/* Language & Confidence */}
        <div className="bg-gray-50 rounded-lg p-4">
          <div className="flex items-center space-x-2 mb-3">
            <Zap className="h-4 w-4 text-gray-600" />
            <h4 className="font-medium text-gray-900">Analysis Details</h4>
          </div>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">Language</span>
              <span className="text-sm font-medium text-gray-900 uppercase">
                {analysis.language || 'en'}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">Confidence</span>
              <span className={`text-sm font-medium ${confidence.color}`}>
                {(analysis.confidence * 100).toFixed(1)}%
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">Processing</span>
              <span className="text-sm font-medium text-green-600">
                Amazon Comprehend
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Insights */}
      <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg p-4 border border-purple-200">
        <div className="flex items-start space-x-2">
          <Brain className="h-5 w-5 text-purple-600 mt-0.5 flex-shrink-0" />
          <div>
            <h4 className="font-medium text-gray-900 mb-2">AI Agent Insights</h4>
            <p className="text-sm text-gray-700">
              Based on the emotional analysis, your current state shows{' '}
              <span className="font-medium text-purple-600">
                {analysis.emotion?.toLowerCase() || 'complex emotional patterns'}
              </span>
              {' '}with a {analysis.sentiment?.toLowerCase() || 'mixed'} sentiment. 
              The AI agent has processed your emotional state and provided personalized insights 
              to help you better understand your feelings.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AgentAnalysisResults;
