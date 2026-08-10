import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import { MessageSquare, Ticket, History, TrendingUp } from 'lucide-react';
import Layout from '../components/Layout';
import { useAuth } from '../context/AuthContext';

export default function EmployeeDashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();

  // Fetch my tickets
  const { data: tickets } = useQuery({
    queryKey: ['myTickets'],
    queryFn: async () => {
      const res = await api.get('/tickets/my-tickets');
      return res.data;
    }
  });

  // Fetch recent chat history
  const { data: chatHistory } = useQuery({
    queryKey: ['recentChats'],
    queryFn: async () => {
      const res = await api.get('/chat/history?limit=5');
      return res.data;
    }
  });

  const openTickets = tickets?.filter(t => t.status === 'Open').length || 0;
  const inProgressTickets = tickets?.filter(t => t.status === 'InProgress').length || 0;

  return (
    <Layout>
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Welcome, {user.full_name}!</h1>
          <p className="text-gray-600 mt-2">Employee Dashboard</p>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Open Tickets</p>
                <p className="text-3xl font-bold text-blue-600 mt-1">{openTickets}</p>
              </div>
              <div className="bg-blue-100 p-3 rounded-full">
                <Ticket className="text-blue-600" size={24} />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">In Progress</p>
                <p className="text-3xl font-bold text-yellow-600 mt-1">{inProgressTickets}</p>
              </div>
              <div className="bg-yellow-100 p-3 rounded-full">
                <TrendingUp className="text-yellow-600" size={24} />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Chat History</p>
                <p className="text-3xl font-bold text-green-600 mt-1">{chatHistory?.length || 0}</p>
              </div>
              <div className="bg-green-100 p-3 rounded-full">
                <History className="text-green-600" size={24} />
              </div>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <button
            onClick={() => navigate('/chat')}
            className="bg-gradient-to-r from-blue-600 to-blue-700 text-white p-6 rounded-lg shadow-lg hover:shadow-xl transition text-left"
          >
            <MessageSquare size={32} className="mb-3" />
            <h3 className="text-xl font-bold mb-2">Ask AI Assistant</h3>
            <p className="text-blue-100">Get instant answers from department documents</p>
          </button>

          <button
            onClick={() => navigate('/tickets?action=create')}
            className="bg-gradient-to-r from-green-600 to-green-700 text-white p-6 rounded-lg shadow-lg hover:shadow-xl transition text-left"
          >
            <Ticket size={32} className="mb-3" />
            <h3 className="text-xl font-bold mb-2">Create Support Ticket</h3>
            <p className="text-green-100">Need human help? Raise a support ticket</p>
          </button>
        </div>

        {/* Recent Activity */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Recent Tickets */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Recent Tickets</h2>
            {tickets?.slice(0, 3).length > 0 ? (
              <div className="space-y-3">
                {tickets.slice(0, 3).map(ticket => (
                  <div
                    key={ticket.id}
                    onClick={() => navigate(`/tickets/${ticket.id}`)}
                    className="p-3 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer transition"
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-xs font-mono text-gray-500">{ticket.ticket_number}</span>
                      <span className={`text-xs px-2 py-1 rounded ${
                        ticket.status === 'Open' ? 'bg-blue-100 text-blue-800' :
                        ticket.status === 'InProgress' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-green-100 text-green-800'
                      }`}>
                        {ticket.status}
                      </span>
                    </div>
                    <p className="text-sm font-medium text-gray-900">{ticket.title}</p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500 text-sm">No tickets yet</p>
            )}
          </div>

          {/* Recent Chats */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Recent Questions</h2>
            {chatHistory?.length > 0 ? (
              <div className="space-y-3">
                {chatHistory.map(chat => (
                  <div key={chat.id} className="p-3 border border-gray-200 rounded-lg">
                    <p className="text-sm font-medium text-gray-900 mb-1">{chat.question}</p>
                    <p className="text-xs text-gray-500">
                      {new Date(chat.created_at).toLocaleDateString()} • 
                      Confidence: {(chat.confidence_score * 100).toFixed(0)}%
                    </p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500 text-sm">No chat history yet</p>
            )}
          </div>
        </div>
      </div>
    </Layout>
  );
}