import React, { useState } from 'react';
import { Send, Loader2, AlertCircle } from 'lucide-react';

const EmotionAnalyzer = ({ onAnalyze, loading, error }) => {
  const [text, setText] = useState('');
  const [context, setContext] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onAnalyze(text, context);
    setText('');
    setContext('');
  };

  // const getEmotionColor = (emotion) => {
  //   if (emotion?.toLowerCase().includes('joy') || emotion?.toLowerCase().includes('optimism')) {
  //     return 'text-emotion-positive';
  //   } else if (emotion?.toLowerCase().includes('sadness') || emotion?.toLowerCase().includes('anger') || emotion?.toLowerCase().includes('fear')) {
  //     return 'text-emotion-negative';
  //   } else if (emotion?.toLowerCase().includes('calm') || emotion?.toLowerCase().includes('indifference')) {
  //     return 'text-emotion-neutral';
  //   } else if (emotion?.toLowerCase().includes('conflicted') || emotion?.toLowerCase().includes('uncertain')) {
  //     return 'text-emotion-mixed';
  //   }
  //   return 'text-gray-600';
  // };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-4">
        Analyze Your Emotions
      </h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="text" className="block text-sm font-medium text-gray-700 mb-2">
            What's on your mind?
          </label>
          <textarea
            id="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Share your thoughts, feelings, or experiences..."
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 resize-none"
            rows={4}
            disabled={loading}
          />
        </div>
        
        <div>
          <label htmlFor="context" className="block text-sm font-medium text-gray-700 mb-2">
            Additional Context (Optional)
          </label>
          <input
            id="context"
            type="text"
            value={context}
            onChange={(e) => setContext(e.target.value)}
            placeholder="e.g., work, relationships, health..."
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            disabled={loading}
          />
        </div>
        
        {error && (
          <div className="flex items-center space-x-2 text-red-600 bg-red-50 p-3 rounded-lg">
            <AlertCircle className="h-4 w-4" />
            <span className="text-sm">{error}</span>
          </div>
        )}
        
        <button
          type="submit"
          disabled={loading || !text.trim()}
          className="w-full btn-primary flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin" />
              <span>Analyzing...</span>
            </>
          ) : (
            <>
              <Send className="h-4 w-4" />
              <span>Analyze Emotion</span>
            </>
          )}
        </button>
      </form>
      
      <div className="mt-6 p-4 bg-gray-50 rounded-lg">
        <h3 className="text-sm font-medium text-gray-700 mb-2">How it works:</h3>
        <ul className="text-xs text-gray-600 space-y-1">
          <li>• Your text is analyzed using Amazon Comprehend</li>
          <li>• An AI agent interprets the sentiment and maps it to emotions</li>
          <li>• You receive personalized insights and adaptive responses</li>
        </ul>
      </div>
    </div>
  );
};

export default EmotionAnalyzer;
