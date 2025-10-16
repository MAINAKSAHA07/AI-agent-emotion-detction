import React from 'react';
import { Clock, TrendingUp, TrendingDown, Minus, AlertCircle } from 'lucide-react';

const EmotionHistory = ({ analyses, onRefresh }) => {
  const getEmotionIcon = (emotion) => {
    if (emotion?.toLowerCase().includes('joy') || emotion?.toLowerCase().includes('optimism')) {
      return <TrendingUp className="h-4 w-4 text-emotion-positive" />;
    } else if (emotion?.toLowerCase().includes('sadness') || emotion?.toLowerCase().includes('anger') || emotion?.toLowerCase().includes('fear')) {
      return <TrendingDown className="h-4 w-4 text-emotion-negative" />;
    } else if (emotion?.toLowerCase().includes('calm') || emotion?.toLowerCase().includes('indifference')) {
      return <Minus className="h-4 w-4 text-emotion-neutral" />;
    } else if (emotion?.toLowerCase().includes('conflicted') || emotion?.toLowerCase().includes('uncertain')) {
      return <AlertCircle className="h-4 w-4 text-emotion-mixed" />;
    }
    return <Minus className="h-4 w-4 text-gray-400" />;
  };

  const getEmotionColor = (emotion) => {
    if (emotion?.toLowerCase().includes('joy') || emotion?.toLowerCase().includes('optimism')) {
      return 'emotion-positive';
    } else if (emotion?.toLowerCase().includes('sadness') || emotion?.toLowerCase().includes('anger') || emotion?.toLowerCase().includes('fear')) {
      return 'emotion-negative';
    } else if (emotion?.toLowerCase().includes('calm') || emotion?.toLowerCase().includes('indifference')) {
      return 'emotion-neutral';
    } else if (emotion?.toLowerCase().includes('conflicted') || emotion?.toLowerCase().includes('uncertain')) {
      return 'emotion-mixed';
    }
    return 'border-gray-300';
  };

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleString();
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return 'text-green-600';
    if (confidence >= 0.6) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold text-gray-900">
          Analysis History
        </h2>
        <span className="text-sm text-gray-500">
          {analyses.length} analyses
        </span>
      </div>
      
      {analyses.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          <Clock className="h-12 w-12 mx-auto mb-4 text-gray-300" />
          <p>No analyses yet. Start by analyzing some text above!</p>
        </div>
      ) : (
        <div className="space-y-4 max-h-96 overflow-y-auto">
          {analyses.map((analysis, index) => (
            <div
              key={index}
              className={`emotion-card ${getEmotionColor(analysis.emotion)}`}
            >
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center space-x-2">
                  {getEmotionIcon(analysis.emotion)}
                  <span className="font-medium text-gray-900">
                    {analysis.emotion}
                  </span>
                </div>
                <div className="flex items-center space-x-2 text-sm text-gray-500">
                  <Clock className="h-3 w-3" />
                  <span>{formatTimestamp(analysis.timestamp)}</span>
                </div>
              </div>
              
              <p className="text-gray-700 mb-3 line-clamp-2">
                "{analysis.input_text}"
              </p>
              
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-gray-500">Sentiment:</span>
                  <span className={`ml-2 font-medium ${
                    analysis.sentiment === 'POSITIVE' ? 'text-emotion-positive' :
                    analysis.sentiment === 'NEGATIVE' ? 'text-emotion-negative' :
                    analysis.sentiment === 'NEUTRAL' ? 'text-emotion-neutral' :
                    'text-emotion-mixed'
                  }`}>
                    {analysis.sentiment}
                  </span>
                </div>
                <div>
                  <span className="text-gray-500">Confidence:</span>
                  <span className={`ml-2 font-medium ${getConfidenceColor(analysis.confidence)}`}>
                    {(analysis.confidence * 100).toFixed(1)}%
                  </span>
                </div>
                <div>
                  <span className="text-gray-500">Valence:</span>
                  <span className="ml-2 font-medium">
                    {analysis.valence > 0 ? '+' : ''}{analysis.valence}
                  </span>
                </div>
                <div>
                  <span className="text-gray-500">Arousal:</span>
                  <span className="ml-2 font-medium">
                    {analysis.arousal}
                  </span>
                </div>
              </div>
              
              {analysis.adaptive_response && (
                <div className="mt-3 p-3 bg-gray-50 rounded-lg">
                  <p className="text-sm text-gray-600">
                    <span className="font-medium">AI Response:</span> {analysis.adaptive_response}
                  </p>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default EmotionHistory;
