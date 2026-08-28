import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useNavigate, useSearchParams } from 'react-router-dom';
import api from '../services/api';
import toast from 'react-hot-toast';
import { Ticket, Plus, X } from 'lucide-react';
import Layout from '../components/Layout';
import { useAuth } from '../context/AuthContext';

export default function TicketsPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [searchParams] = useSearchParams();
  const [showCreateModal, setShowCreateModal] = useState(searchParams.get('action') === 'create');
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category: '',
    priority: 'Medium',
    department_id: user.department_id || ''
  });

  // Fetch tickets based on role
  const { data: tickets, isLoading } = useQuery({
    queryKey: ['tickets', user.role],
    queryFn: async () => {
      const endpoint = user.role === 'Employee' 
        ? '/tickets/my-tickets'
        : user.role === 'Officer'
        ? '/tickets/assigned'
        : `/tickets/department/${user.department_id}`;
      const res = await api.get(endpoint);
      return res.data;
    }
  });

  // Fetch departments for create form
  const { data: departments } = useQuery({
    queryKey: ['departments'],
    queryFn: async () => {
      const res = await api.get('/departments/');
      return res.data;
    }
  });

  // Create ticket mutation
  const createMutation = useMutation({
    mutationFn: async (data) => {
      const res = await api.post('/tickets/', data);
      return res.data;
    },
    onSuccess: () => {
      toast.success('Ticket created successfully!');
      queryClient.invalidateQueries(['tickets']);
      setShowCreateModal(false);
      setFormData({
        title: '',
        description: '',
        category: '',
        priority: 'Medium',
        department_id: user.department_id || ''
      });
    },
    onError: (error) => {
      toast.error(error.response?.data?.detail || 'Failed to create ticket');
    }
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    createMutation.mutate(formData);
  };

  const getStatusColor = (status) => {
    const colors = {
      Open: 'bg-blue-100 text-blue-800',
      InProgress: 'bg-yellow-100 text-yellow-800',
      Resolved: 'bg-green-100 text-green-800',
      Closed: 'bg-gray-100 text-gray-800'
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  const getPriorityColor = (priority) => {
    const colors = {
      Low: 'bg-gray-100 text-gray-800',
      Medium: 'bg-blue-100 text-blue-800',
      High: 'bg-orange-100 text-orange-800',
      Urgent: 'bg-red-100 text-red-800'
    };
    return colors[priority] || 'bg-gray-100 text-gray-800';
  };

  return (
    <Layout>
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Support Tickets</h1>
          <button
            onClick={() => setShowCreateModal(true)}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition flex items-center gap-2"
          >
            <Plus size={20} />
            Create Ticket
          </button>
        </div>

        {/* Tickets List */}
        <div className="bg-white rounded-lg shadow-sm">
          {isLoading ? (
            <div className="p-8 text-center text-gray-500">Loading tickets...</div>
          ) : tickets?.length === 0 ? (
            <div className="p-8 text-center text-gray-500">
              <Ticket size={48} className="mx-auto mb-4 opacity-50" />
              <p>No tickets found</p>
            </div>
          ) : (
            <div className="divide-y">
              {tickets?.map(ticket => (
                <div
                  key={ticket.id}
                  onClick={() => navigate(`/tickets/${ticket.id}`)}
                  className="p-4 hover:bg-gray-50 cursor-pointer transition"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <span className="text-sm font-mono text-gray-500">{ticket.ticket_number}</span>
                        <span className={`text-xs px-2 py-1 rounded ${getStatusColor(ticket.status)}`}>
                          {ticket.status}
                        </span>
                        <span className={`text-xs px-2 py-1 rounded ${getPriorityColor(ticket.priority)}`}>
                          {ticket.priority}
                        </span>
                      </div>
                      <h3 className="font-semibold text-gray-900 mb-1">{ticket.title}</h3>
                      <p className="text-sm text-gray-600 line-clamp-2">{ticket.description}</p>
                      <div className="flex items-center gap-4 mt-2 text-xs text-gray-500">
                        <span>Category: {ticket.category}</span>
                        <span>Created: {new Date(ticket.created_at).toLocaleDateString()}</span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Create Ticket Modal */}
        {showCreateModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
              <div className="flex items-center justify-between p-6 border-b">
                <h2 className="text-2xl font-bold text-gray-900">Create Support Ticket</h2>
                <button
                  onClick={() => setShowCreateModal(false)}
                  className="text-gray-500 hover:text-gray-700"
                >
                  <X size={24} />
                </button>
              </div>

              <form onSubmit={handleSubmit} className="p-6 space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Department *
                  </label>
                  <select
                    value={formData.department_id}
                    onChange={(e) => setFormData({ ...formData, department_id: parseInt(e.target.value) })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    required
                  >
                    <option value="">Select Department</option>
                    {departments?.map(dept => (
                      <option key={dept.id} value={dept.id}>{dept.name}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Title *
                  </label>
                  <input
                    type="text"
                    value={formData.title}
                    onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    placeholder="Brief description of the issue"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Category *
                  </label>
                  <input
                    type="text"
                    value={formData.category}
                    onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    placeholder="e.g., Leave, Salary, System Access"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Priority *
                  </label>
                  <select
                    value={formData.priority}
                    onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    required
                  >
                    <option value="Low">Low</option>
                    <option value="Medium">Medium</option>
                    <option value="High">High</option>
                    <option value="Urgent">Urgent</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Description *
                  </label>
                  <textarea
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    rows={6}
                    placeholder="Provide detailed information about your issue..."
                    required
                  />
                </div>

                <div className="flex gap-3 pt-4">
                  <button
                    type="submit"
                    disabled={createMutation.isPending}
                    className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
                  >
                    {createMutation.isPending ? 'Creating...' : 'Create Ticket'}
                  </button>
                  <button
                    type="button"
                    onClick={() => setShowCreateModal(false)}
                    className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}