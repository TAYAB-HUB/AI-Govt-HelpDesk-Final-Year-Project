import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useNavigate, useSearchParams } from 'react-router-dom';
import api from '../services/api';
import toast from 'react-hot-toast';
import { Ticket, Plus, X, Building2, User, Filter } from 'lucide-react';
import Layout from '../components/Layout';
import { useAuth } from '../context/AuthContext';

export default function TicketsPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [searchParams] = useSearchParams();
  const [showCreateModal, setShowCreateModal] = useState(searchParams.get('action') === 'create');
  const [filterTab, setFilterTab] = useState('all'); // 'all' or 'assigned'
  const [statusFilter, setStatusFilter] = useState('all');

  const isStaff = user && ['Officer', 'DeptAdmin', 'SuperAdmin'].includes(user.role);

  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category: '',
    priority: 'Medium',
    department_id: user.department_id || ''
  });

  // Fetch tickets based on role and active tab
  const { data: tickets, isLoading } = useQuery({
    queryKey: ['tickets', user?.role, filterTab, statusFilter],
    queryFn: async () => {
      let endpoint = '/tickets/';
      if (user.role === 'Employee') {
        endpoint = '/tickets/my-tickets';
      } else if (filterTab === 'assigned') {
        endpoint = '/tickets/assigned';
      } else {
        endpoint = '/tickets/';
      }
      
      const res = await api.get(endpoint);
      let list = res.data;

      if (statusFilter !== 'all') {
        list = list.filter((t) => t.status === statusFilter);
      }
      return list;
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
      <div className="max-w-6xl mx-auto pb-12">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Support Tickets</h1>
            <p className="text-sm text-gray-500 mt-1">
              {isStaff 
                ? 'Review, answer, and manage support tickets submitted by employees' 
                : 'Track and follow up on your requests'}
            </p>
          </div>
          <button
            onClick={() => setShowCreateModal(true)}
            className="bg-blue-600 text-white px-4 py-2.5 rounded-lg hover:bg-blue-700 transition flex items-center justify-center gap-2 font-medium shadow-sm"
          >
            <Plus size={18} />
            Create Ticket
          </button>
        </div>

        {/* Staff Filter Bar */}
        {isStaff && (
          <div className="flex flex-wrap items-center justify-between gap-4 bg-white p-4 rounded-xl border border-gray-200 mb-6 shadow-sm">
            <div className="flex items-center gap-2">
              <button
                onClick={() => setFilterTab('all')}
                className={`px-3 py-1.5 rounded-lg text-sm font-medium transition ${
                  filterTab === 'all'
                    ? 'bg-blue-600 text-white shadow-sm'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                All Tickets
              </button>
              <button
                onClick={() => setFilterTab('assigned')}
                className={`px-3 py-1.5 rounded-lg text-sm font-medium transition ${
                  filterTab === 'assigned'
                    ? 'bg-blue-600 text-white shadow-sm'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                Assigned to Me
              </button>
            </div>

            <div className="flex items-center gap-2">
              <Filter size={16} className="text-gray-400" />
              <span className="text-xs font-semibold text-gray-600">Status:</span>
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="text-xs px-2.5 py-1.5 border border-gray-300 rounded-lg bg-white focus:ring-2 focus:ring-blue-500"
              >
                <option value="all">All Statuses</option>
                <option value="Open">Open</option>
                <option value="InProgress">In Progress</option>
                <option value="Resolved">Resolved</option>
                <option value="Closed">Closed</option>
              </select>
            </div>
          </div>
        )}

        {/* Tickets List */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          {isLoading ? (
            <div className="p-12 text-center text-gray-500">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-3"></div>
              <p className="text-sm">Loading tickets...</p>
            </div>
          ) : tickets?.length === 0 ? (
            <div className="p-12 text-center text-gray-500">
              <Ticket size={48} className="mx-auto mb-4 opacity-40 text-gray-400" />
              <p className="text-base font-semibold text-gray-800">No tickets found</p>
              <p className="text-sm text-gray-500 mt-1">
                {isStaff 
                  ? 'There are currently no tickets matching this filter.'
                  : 'You have not submitted any tickets yet.'}
              </p>
            </div>
          ) : (
            <div className="divide-y divide-gray-100">
              {tickets?.map(ticket => (
                <div
                  key={ticket.id}
                  onClick={() => navigate(`/tickets/${ticket.id}`)}
                  className="p-5 hover:bg-slate-50 cursor-pointer transition group"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1">
                      <div className="flex flex-wrap items-center gap-2 mb-2">
                        <span className="text-xs font-mono font-semibold px-2 py-0.5 bg-gray-100 rounded text-gray-600">
                          {ticket.ticket_number}
                        </span>
                        <span className={`text-xs px-2.5 py-0.5 rounded-full font-semibold ${getStatusColor(ticket.status)}`}>
                          {ticket.status}
                        </span>
                        <span className={`text-xs px-2.5 py-0.5 rounded-full font-semibold ${getPriorityColor(ticket.priority)}`}>
                          {ticket.priority}
                        </span>
                        {ticket.department_name && (
                          <span className="text-xs text-gray-500 flex items-center gap-1">
                            <Building2 size={13} className="text-gray-400" />
                            {ticket.department_name}
                          </span>
                        )}
                      </div>
                      <h3 className="font-semibold text-gray-900 group-hover:text-blue-600 transition mb-1 text-base">
                        {ticket.title}
                      </h3>
                      <p className="text-sm text-gray-600 line-clamp-2 mb-3 leading-relaxed">
                        {ticket.description}
                      </p>
                      <div className="flex flex-wrap items-center gap-4 text-xs text-gray-400">
                        <span>Category: <strong className="text-gray-600">{ticket.category}</strong></span>
                        <span>Created: {new Date(ticket.created_at).toLocaleDateString()}</span>
                        {isStaff && (
                          <span className="text-blue-600 font-medium">Click to answer / resolve →</span>
                        )}
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
          <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-2xl shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto border border-gray-100">
              <div className="flex items-center justify-between p-6 border-b border-gray-100">
                <h2 className="text-xl font-bold text-gray-900">Create Support Ticket</h2>
                <button
                  onClick={() => setShowCreateModal(false)}
                  className="text-gray-400 hover:text-gray-600 p-1 rounded-lg hover:bg-gray-100 transition"
                >
                  <X size={20} />
                </button>
              </div>

              <form onSubmit={handleSubmit} className="p-6 space-y-4">
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-1.5">
                    Department *
                  </label>
                  <select
                    value={formData.department_id}
                    onChange={(e) => setFormData({ ...formData, department_id: parseInt(e.target.value) })}
                    className="w-full px-3.5 py-2.5 border border-gray-300 rounded-lg text-sm bg-white focus:ring-2 focus:ring-blue-500"
                    required
                  >
                    <option value="">Select Department</option>
                    {departments?.map(dept => (
                      <option key={dept.id} value={dept.id}>{dept.name}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-1.5">
                    Title / Subject *
                  </label>
                  <input
                    type="text"
                    value={formData.title}
                    onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                    className="w-full px-3.5 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500"
                    placeholder="Brief description of the issue"
                    required
                  />
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-1.5">
                      Category *
                    </label>
                    <input
                      type="text"
                      value={formData.category}
                      onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                      className="w-full px-3.5 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500"
                      placeholder="e.g., Leave, Salary, System Access"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-1.5">
                      Priority *
                    </label>
                    <select
                      value={formData.priority}
                      onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
                      className="w-full px-3.5 py-2.5 border border-gray-300 rounded-lg text-sm bg-white focus:ring-2 focus:ring-blue-500"
                      required
                    >
                      <option value="Low">Low</option>
                      <option value="Medium">Medium</option>
                      <option value="High">High</option>
                      <option value="Urgent">Urgent</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-1.5">
                    Description *
                  </label>
                  <textarea
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                    className="w-full px-3.5 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500"
                    rows={5}
                    placeholder="Provide complete details about your issue or question..."
                    required
                  />
                </div>

                <div className="flex gap-3 pt-4 border-t border-gray-100">
                  <button
                    type="submit"
                    disabled={createMutation.isPending}
                    className="flex-1 bg-blue-600 text-white py-2.5 px-4 rounded-lg hover:bg-blue-700 font-medium transition disabled:opacity-50 text-sm shadow-sm"
                  >
                    {createMutation.isPending ? 'Creating...' : 'Submit Ticket'}
                  </button>
                  <button
                    type="button"
                    onClick={() => setShowCreateModal(false)}
                    className="px-4 py-2.5 border border-gray-300 rounded-lg hover:bg-gray-50 font-medium text-gray-700 transition text-sm"
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
