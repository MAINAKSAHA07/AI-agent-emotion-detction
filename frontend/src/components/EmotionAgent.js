import React, { useState, useEffect, useRef } from 'react';
import { Send, Bot, User, Loader2, Brain, Heart, TrendingUp, MessageCircle } from 'lucide-react';

const EmotionAgent = ({ onAnalyze, loading, error, sessionId }) => {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [conversationHistory, setConversationHistory] = useState([]);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Initialize with welcome message
  useEffect(() => {
    if (messages.length === 0) {
      setMessages([
        {
          id: 'welcome',
          type: 'agent',
          content: "Hello! I'm your emotional intelligence agent.",
          timestamp: new Date(),
          emotion: null
        }
      ]);
    }
  }, [messages.length]);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputText.trim() || loading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputText,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsTyping(true);

    try {
      // Call the analysis function with conversation history
      const result = await onAnalyze(inputText, 'agent_conversation', conversationHistory);
      
      // Add the user message to conversation history
      const newHistory = [...conversationHistory, { user: inputText }];
      
      // Wait for the analysis to complete and get the response
      setTimeout(() => {
        if (result && result.adaptive_response) {
          const agentResponse = {
            id: Date.now(),
            type: 'agent',
            content: result.adaptive_response,
            timestamp: new Date(),
            emotion: result.emotion
          };
          setMessages(prev => [...prev, agentResponse]);
          
          // Add the agent response to conversation history
          setConversationHistory([...newHistory, { assistant: result.adaptive_response }]);
        } else {
          const fallbackResponse = {
            id: Date.now(),
            type: 'agent',
            content: "I understand what you're expressing. Let me provide some insights...",
            timestamp: new Date(),
            emotion: null
          };
          setMessages(prev => [...prev, fallbackResponse]);
        }
        setIsTyping(false);
      }, 1500);

    } catch (err) {
      const errorMessage = {
        id: Date.now() + 1,
        type: 'agent',
        content: "I'm sorry, I encountered an error while analyzing your message. Please try again.",
        timestamp: new Date(),
        emotion: null
      };
      setMessages(prev => [...prev, errorMessage]);
      setIsTyping(false);
    }
  };


  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const getEmotionIcon = (emotion) => {
    if (!emotion) return <Brain className="h-4 w-4" />;
    
    if (emotion.toLowerCase().includes('joy') || emotion.toLowerCase().includes('optimism')) {
      return <TrendingUp className="h-4 w-4 text-green-500" />;
    } else if (emotion.toLowerCase().includes('sadness') || emotion.toLowerCase().includes('anger')) {
      return <Heart className="h-4 w-4 text-red-500" />;
    } else if (emotion.toLowerCase().includes('calm') || emotion.toLowerCase().includes('neutral')) {
      return <MessageCircle className="h-4 w-4 text-blue-500" />;
    }
    return <Brain className="h-4 w-4 text-purple-500" />;
  };

  const clearConversation = () => {
    setMessages([
      {
        id: 'welcome',
        type: 'agent',
        content: "Hello! I'm your emotional intelligence agent.",
        timestamp: new Date(),
        emotion: null
      }
    ]);
    setConversationHistory([]);
  };

  return (
    <div className="bg-white rounded-lg shadow-lg h-[600px] flex flex-col">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white p-4 rounded-t-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-white/20 p-2 rounded-full">
              <Bot className="h-5 w-5" />
            </div>
            <div>
              <h3 className="font-semibold">Emotion Intelligence Agent</h3>
              <p className="text-sm text-white/80">Powered by Advanced AI</p>
            </div>
          </div>
          <button
            onClick={clearConversation}
            className="text-white/80 hover:text-white text-sm px-3 py-1 rounded-full hover:bg-white/20 transition-colors"
          >
            Clear Chat
          </button>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div className={`flex items-start space-x-2 max-w-[80%] ${
              message.type === 'user' ? 'flex-row-reverse space-x-reverse' : ''
            }`}>
              <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                message.type === 'user' 
                  ? 'bg-blue-500 text-white' 
                  : 'bg-purple-100 text-purple-600'
              }`}>
                {message.type === 'user' ? (
                  <User className="h-4 w-4" />
                ) : (
                  getEmotionIcon(message.emotion)
                )}
              </div>
              
              <div className={`rounded-lg px-4 py-2 ${
                message.type === 'user'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-100 text-gray-800'
              }`}>
                <p className="text-sm">{message.content}</p>
                <p className={`text-xs mt-1 ${
                  message.type === 'user' ? 'text-blue-100' : 'text-gray-500'
                }`}>
                  {formatTime(message.timestamp)}
                </p>
              </div>
            </div>
          </div>
        ))}
        
        {isTyping && (
          <div className="flex justify-start">
            <div className="flex items-start space-x-2">
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-purple-100 text-purple-600 flex items-center justify-center">
                <Bot className="h-4 w-4" />
              </div>
              <div className="bg-gray-100 rounded-lg px-4 py-2">
                <div className="flex items-center space-x-1">
                  <Loader2 className="h-3 w-3 animate-spin" />
                  <span className="text-sm text-gray-600">Analyzing emotions...</span>
                </div>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Error Display */}
      {error && (
        <div className="mx-4 mb-2 p-3 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-600">{error}</p>
        </div>
      )}

      {/* Input */}
      <div className="border-t p-4">
        <form onSubmit={handleSubmit} className="flex space-x-2">
          <input
            ref={inputRef}
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Share your thoughts and feelings..."
            className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 outline-none"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading || !inputText.trim()}
            className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2 transition-colors"
          >
            {loading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Send className="h-4 w-4" />
            )}
          </button>
        </form>
        
        <div className="mt-2 text-xs text-gray-500 text-center">
          Session: {sessionId?.substring(0, 8)}...
        </div>
      </div>
    </div>
  );
};

export default EmotionAgent;
