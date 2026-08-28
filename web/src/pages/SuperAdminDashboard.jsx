import React from 'react';
import { useQuery } from '@tanstack/react-query';
import api from '../services/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Database, Users, FileText, Ticket } from 'lucide-react';
import Layout from '../components/Layout';

export default function SuperAdminDashboard() {
  // Fetch global analytics
  const { data: analytics } = useQuery({
    queryKey: ['globalAnalytics'],
    queryFn: async () => {
      const res = await api.get('/analytics/dashboard');
      return res.data;
    }
  });

  const ticketsByPriority = analytics?.tickets.by_priority ? 
    Object.entries(analytics.tickets.by_priority).map(([priority, count]) => ({
      priority,
      count
    })) : [];

  return (
    <Layout>
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Super Admin Dashboard</h1>
          <p className="text-gray-600 mt-2">System-wide overview and analytics</p>
        </div>

        {/* Global Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Total Tickets</p>
                <p className="text-3xl font-bold text-blue-600 mt-1">{analytics?.tickets.total || 0}</p>
              </div>
              <div className="bg-blue-100 p-3 rounded-full">
                <Ticket className="text-blue-600" size={24} />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Open Tickets</p>
                <p className="text-3xl font-bold text-yellow-600 mt-1">{analytics?.tickets.open || 0}</p>
              </div>
              <div className="bg-yellow-100 p-3 rounded-full">
                <Database className="text-yellow-600" size={24} />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Chat Interactions</p>
                <p className="text-3xl font-bold text-green-600 mt-1">{analytics?.chat.total_interactions || 0}</p>
              </div>
              <div className="bg-green-100 p-3 rounded-full">
                <FileText className="text-green-600" size={24} />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Avg Confidence</p>
                <p className="text-3xl font-bold text-purple-600 mt-1">{analytics?.chat.avg_confidence || 0}%</p>
              </div>
              <div className="bg-purple-100 p-3 rounded-full">
                <Users className="text-purple-600" size={24} />
              </div>
            </div>
          </div>
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Tickets by Priority</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={ticketsByPriority}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="priority" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="count" fill="#3b82f6" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Ticket Status Distribution</h2>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-gray-700">Open</span>
                <span className="font-semibold text-blue-600">{analytics?.tickets.open || 0}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-700">In Progress</span>
                <span className="font-semibold text-yellow-600">{analytics?.tickets.in_progress || 0}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-700">Resolved</span>
                <span className="font-semibold text-green-600">{analytics?.tickets.resolved || 0}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-700">Closed</span>
                <span className="font-semibold text-gray-600">{analytics?.tickets.closed || 0}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}