import React from 'react';
import { TrendingUp, TrendingDown, Minus, RefreshCw, BarChart3 } from 'lucide-react';

const EmotionTrends = ({ trends, sessionId, onRefresh }) => {
  const getTrendIcon = (trend) => {
    if (trend?.toLowerCase().includes('positive')) {
      return <TrendingUp className="h-5 w-5 text-emotion-positive" />;
    } else if (trend?.toLowerCase().includes('negative')) {
      return <TrendingDown className="h-5 w-5 text-emotion-negative" />;
    } else {
      return <Minus className="h-5 w-5 text-emotion-neutral" />;
    }
  };

  const getTrendColor = (trend) => {
    if (trend?.toLowerCase().includes('positive')) {
      return 'text-emotion-positive';
    } else if (trend?.toLowerCase().includes('negative')) {
      return 'text-emotion-negative';
    } else {
      return 'text-emotion-neutral';
    }
  };

  const getValenceColor = (valence) => {
    if (valence > 0.3) return 'text-emotion-positive';
    if (valence < -0.3) return 'text-emotion-negative';
    return 'text-emotion-neutral';
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return 'text-green-600';
    if (confidence >= 0.6) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="space-y-6">
      {/* Trends Overview */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900 flex items-center space-x-2">
            <BarChart3 className="h-5 w-5" />
            <span>Emotional Trends</span>
          </h3>
          <button
            onClick={onRefresh}
            className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors duration-200"
          >
            <RefreshCw className="h-4 w-4" />
          </button>
        </div>
        
        {trends ? (
          <div className="space-y-4">
            <div className="flex items-center space-x-3">
              {getTrendIcon(trends.trend)}
              <span className={`font-medium ${getTrendColor(trends.trend)}`}>
                {trends.trend}
              </span>
            </div>
            
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div className="bg-gray-50 p-3 rounded-lg">
                <div className="text-gray-500 mb-1">Average Valence</div>
                <div className={`text-lg font-semibold ${getValenceColor(trends.average_valence)}`}>
                  {trends.average_valence > 0 ? '+' : ''}{trends.average_valence}
                </div>
              </div>
              
              <div className="bg-gray-50 p-3 rounded-lg">
                <div className="text-gray-500 mb-1">Avg Confidence</div>
                <div className={`text-lg font-semibold ${getConfidenceColor(trends.average_confidence)}`}>
                  {(trends.average_confidence * 100).toFixed(1)}%
                </div>
              </div>
            </div>
            
            <div className="bg-gray-50 p-3 rounded-lg">
              <div className="text-gray-500 text-sm mb-1">Total Analyses</div>
              <div className="text-lg font-semibold text-gray-900">
                {trends.total_analyses}
              </div>
            </div>
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">
            <BarChart3 className="h-12 w-12 mx-auto mb-4 text-gray-300" />
            <p>No trend data available yet.</p>
            <p className="text-sm">Analyze some emotions to see trends!</p>
          </div>
        )}
      </div>
      
      {/* Session Info */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Session Information
        </h3>
        
        <div className="space-y-3 text-sm">
          <div className="flex justify-between">
            <span className="text-gray-500">Session ID:</span>
            <span className="font-mono text-gray-700">
              {sessionId?.slice(-8)}
            </span>
          </div>
          
          <div className="flex justify-between">
            <span className="text-gray-500">Status:</span>
            <span className="text-green-600 font-medium">Active</span>
          </div>
        </div>
      </div>
      
      {/* Quick Stats */}
      {trends && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Quick Insights
          </h3>
          
          <div className="space-y-3 text-sm">
            {trends.average_valence > 0.3 && (
              <div className="flex items-center space-x-2 text-emotion-positive">
                <TrendingUp className="h-4 w-4" />
                <span>You've been feeling more positive overall</span>
              </div>
            )}
            
            {trends.average_valence < -0.3 && (
              <div className="flex items-center space-x-2 text-emotion-negative">
                <TrendingDown className="h-4 w-4" />
                <span>You've been experiencing more negative emotions</span>
              </div>
            )}
            
            {trends.average_valence >= -0.3 && trends.average_valence <= 0.3 && (
              <div className="flex items-center space-x-2 text-emotion-neutral">
                <Minus className="h-4 w-4" />
                <span>Your emotional state has been relatively balanced</span>
              </div>
            )}
            
            {trends.average_confidence >= 0.8 && (
              <div className="flex items-center space-x-2 text-green-600">
                <div className="w-2 h-2 bg-green-600 rounded-full"></div>
                <span>High confidence in emotion detection</span>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default EmotionTrends;
