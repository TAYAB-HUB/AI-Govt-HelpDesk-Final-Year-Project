import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import { Ticket, Clock, CheckCircle, AlertCircle } from 'lucide-react';
import Layout from '../components/Layout';

export default function OfficerDashboard() {
  const navigate = useNavigate();

  // Fetch assigned tickets
  const { data: tickets } = useQuery({
    queryKey: ['assignedTickets'],
    queryFn: async () => {
      const res = await api.get('/tickets/assigned');
      return res.data;
    }
  });

  const openTickets = tickets?.filter(t => t.status === 'Open').length || 0;
  const inProgressTickets = tickets?.filter(t => t.status === 'InProgress').length || 0;
  const resolvedTickets = tickets?.filter(t => t.status === 'Resolved').length || 0;
  const urgentTickets = tickets?.filter(t => t.priority === 'Urgent' && t.status !== 'Closed').length || 0;

  return (
    <Layout>
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Officer Dashboard</h1>
          <p className="text-gray-600 mt-2">Manage assigned support tickets</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Open</p>
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
                <Clock className="text-yellow-600" size={24} />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Resolved</p>
                <p className="text-3xl font-bold text-green-600 mt-1">{resolvedTickets}</p>
              </div>
              <div className="bg-green-100 p-3 rounded-full">
                <CheckCircle className="text-green-600" size={24} />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Urgent</p>
                <p className="text-3xl font-bold text-red-600 mt-1">{urgentTickets}</p>
              </div>
              <div className="bg-red-100 p-3 rounded-full">
                <AlertCircle className="text-red-600" size={24} />
              </div>
            </div>
          </div>
        </div>

        {/* Tickets Queue */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Assigned Tickets</h2>
          {tickets?.length > 0 ? (
            <div className="divide-y">
              {tickets.map(ticket => (
                <div
                  key={ticket.id}
                  onClick={() => navigate(`/tickets/${ticket.id}`)}
                  className="py-4 hover:bg-gray-50 cursor-pointer transition"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <span className="text-sm font-mono text-gray-500">{ticket.ticket_number}</span>
                        <span className={`text-xs px-2 py-1 rounded ${
                          ticket.status === 'Open' ? 'bg-blue-100 text-blue-800' :
                          ticket.status === 'InProgress' ? 'bg-yellow-100 text-yellow-800' :
                          ticket.status === 'Resolved' ? 'bg-green-100 text-green-800' :
                          'bg-gray-100 text-gray-800'
                        }`}>
                          {ticket.status}
                        </span>
                        <span className={`text-xs px-2 py-1 rounded ${
                          ticket.priority === 'Urgent' ? 'bg-red-100 text-red-800' :
                          ticket.priority === 'High' ? 'bg-orange-100 text-orange-800' :
                          ticket.priority === 'Medium' ? 'bg-blue-100 text-blue-800' :
                          'bg-gray-100 text-gray-800'
                        }`}>
                          {ticket.priority}
                        </span>
                      </div>
                      <h3 className="font-semibold text-gray-900 mb-1">{ticket.title}</h3>
                      <p className="text-sm text-gray-600 line-clamp-1">{ticket.description}</p>
                      <div className="flex items-center gap-4 mt-2 text-xs text-gray-500">
                        <span>Category: {ticket.category}</span>
                        <span>Created: {new Date(ticket.created_at).toLocaleDateString()}</span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500 text-center py-8">No tickets assigned</p>
          )}
        </div>
      </div>
    </Layout>
  );
}