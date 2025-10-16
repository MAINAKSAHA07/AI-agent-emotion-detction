import React from 'react';
import { Brain, Activity, Trash2, Bot, BarChart3 } from 'lucide-react';

const Header = ({ sessionId, onClearSession, viewMode, onViewModeChange }) => {
  return (
    <header className="bg-white shadow-sm border-b">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-primary-100 p-2 rounded-lg">
              <Brain className="h-6 w-6 text-primary-600" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                Emotion Detection
              </h1>
              <p className="text-sm text-gray-600">
                Powered by Amazon Comprehend & AI Agent
              </p>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            {/* View Mode Toggle */}
            <div className="flex items-center bg-gray-100 rounded-lg p-1">
              <button
                onClick={() => onViewModeChange('agent')}
                className={`flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  viewMode === 'agent'
                    ? 'bg-white text-purple-600 shadow-sm'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                <Bot className="h-4 w-4" />
                <span>AI Agent</span>
              </button>
              <button
                onClick={() => onViewModeChange('classic')}
                className={`flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  viewMode === 'classic'
                    ? 'bg-white text-purple-600 shadow-sm'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                <BarChart3 className="h-4 w-4" />
                <span>Classic</span>
              </button>
            </div>

            <div className="flex items-center space-x-2 text-sm text-gray-600">
              <Activity className="h-4 w-4" />
              <span>Session: {sessionId?.slice(-8)}</span>
            </div>
            
            <button
              onClick={onClearSession}
              className="flex items-center space-x-2 px-3 py-2 text-sm text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors duration-200"
            >
              <Trash2 className="h-4 w-4" />
              <span>Clear Session</span>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
