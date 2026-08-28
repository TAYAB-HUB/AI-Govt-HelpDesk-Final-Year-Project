import React, { useState, useRef, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useQuery, useMutation } from '@tanstack/react-query';
import api from '../services/api';
import toast from 'react-hot-toast';
import { Send, ThumbsUp, ThumbsDown, FileText, Ticket } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import Layout from '../components/Layout';

export default function ChatPage() {
  const { user } = useAuth();
  const [selectedDepartment, setSelectedDepartment] = useState(null);
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState([]);
  const messagesEndRef = useRef(null);
  const navigate = useNavigate();

  // Fetch departments
  const { data: departments } = useQuery({
    queryKey: ['departments'],
    queryFn: async () => {
      const res = await api.get('/departments/');
      return res.data;
    }
  });

  // Fetch chat history
  const { data: history } = useQuery({
    queryKey: ['chatHistory', selectedDepartment],
    queryFn: async () => {
      if (!selectedDepartment) return [];
      const res = await api.get(`/chat/history?department_id=${selectedDepartment}&limit=20`);
      return res.data;
    },
    enabled: !!selectedDepartment
  });

  // Ask question mutation
  const askMutation = useMutation({
    mutationFn: async (data) => {
      const res = await api.post('/chat/ask', data);
      return res.data;
    },
    onSuccess: (data) => {
      const assistantMessage = {
        type: 'assistant',
        content: data.answer,
        sources: data.sources,
        confidence: data.confidence_score,
        suggestTicket: data.suggest_ticket,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, assistantMessage]);
    },
    onError: (error) => {
      toast.error(error.response?.data?.detail || 'Failed to get answer');
    }
  });

  // Submit feedback mutation
  const feedbackMutation = useMutation({
    mutationFn: async ({ chatId, feedbackType }) => {
      const res = await api.post(`/chat/feedback/${chatId}`, { feedback_type: feedbackType });
      return res.data;
    },
    onSuccess: () => {
      toast.success('Thank you for your feedback!');
    }
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!question.trim() || !selectedDepartment) return;

    const userMessage = {
      type: 'user',
      content: question,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    askMutation.mutate({
      question,
      department_id: selectedDepartment
    });

    setQuestion('');
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <Layout>
      <div className="max-w-6xl mx-auto h-[calc(100vh-200px)] flex flex-col">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-sm p-4 mb-4">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">AI Helpdesk Chat</h1>
          
          {/* Department Selector */}
          <div className="flex gap-2 overflow-x-auto pb-2">
            {departments?.map(dept => (
              <button
                key={dept.id}
                onClick={() => {
                  setSelectedDepartment(dept.id);
                  setMessages([]);
                }}
                className={`px-4 py-2 rounded-lg whitespace-nowrap transition ${
                  selectedDepartment === dept.id
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {dept.name}
              </button>
            ))}
          </div>
        </div>

        {/* Chat Messages */}
        <div className="flex-1 bg-white rounded-lg shadow-sm p-4 overflow-y-auto mb-4">
          {!selectedDepartment ? (
            <div className="flex items-center justify-center h-full text-gray-500">
              <p>Please select a department to start chatting</p>
            </div>
          ) : messages.length === 0 ? (
            <div className="flex items-center justify-center h-full text-gray-500">
              <div className="text-center">
                <p className="text-lg mb-2">👋 Hello! How can I help you today?</p>
                <p className="text-sm">Ask me anything about {departments?.find(d => d.id === selectedDepartment)?.name}</p>
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              {messages.map((msg, idx) => (
                <div key={idx} className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`max-w-3xl ${msg.type === 'user' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-900'} rounded-lg p-4`}>
                    <p className="whitespace-pre-wrap">{msg.content}</p>
                    
                    {/* Sources */}
                    {msg.sources && msg.sources.length > 0 && (
                      <div className="mt-3 pt-3 border-t border-gray-300">
                        <p className="text-xs font-semibold mb-2 flex items-center gap-1">
                          <FileText size={14} /> Sources:
                        </p>
                        {msg.sources.map((source, sidx) => (
                          <div key={sidx} className="text-xs bg-white bg-opacity-20 rounded p-2 mb-1">
                            <p className="font-medium">{source.document_title}</p>
                            <p className="text-xs opacity-75 mt-1">{source.snippet}</p>
                          </div>
                        ))}
                      </div>
                    )}

                    {/* Confidence & Actions */}
                    {msg.type === 'assistant' && (
                      <div className="mt-3 pt-3 border-t border-gray-300 flex items-center justify-between">
                        <div className="flex gap-2">
                          <button
                            onClick={() => feedbackMutation.mutate({ chatId: idx, feedbackType: 'thumbs_up' })}
                            className="p-1 hover:bg-gray-200 rounded transition"
                            title="Helpful"
                          >
                            <ThumbsUp size={16} />
                          </button>
                          <button
                            onClick={() => feedbackMutation.mutate({ chatId: idx, feedbackType: 'thumbs_down' })}
                            className="p-1 hover:bg-gray-200 rounded transition"
                            title="Not helpful"
                          >
                            <ThumbsDown size={16} />
                          </button>
                        </div>
                        <div className="text-xs">
                          Confidence: {(msg.confidence * 100).toFixed(0)}%
                        </div>
                      </div>
                    )}

                    {/* Suggest Ticket */}
                    {msg.suggestTicket && (
                      <div className="mt-3 pt-3 border-t border-gray-300">
                        <button
                          onClick={() => navigate('/tickets?action=create')}
                          className="text-xs bg-yellow-500 text-white px-3 py-1 rounded hover:bg-yellow-600 transition flex items-center gap-1"
                        >
                          <Ticket size={14} />
                          I couldn't find a good answer. Create a support ticket?
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>
          )}

          {askMutation.isPending && (
            <div className="flex justify-start">
              <div className="bg-gray-100 rounded-lg p-4">
                <div className="flex gap-2">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0s' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Input Form */}
        <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-sm p-4">
          <div className="flex gap-2">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder={selectedDepartment ? "Ask your question..." : "Select a department first"}
              disabled={!selectedDepartment || askMutation.isPending}
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100"
            />
            <button
              type="submit"
              disabled={!selectedDepartment || !question.trim() || askMutation.isPending}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              <Send size={18} />
              Send
            </button>
          </div>
        </form>
      </div>
    </Layout>
  );
}