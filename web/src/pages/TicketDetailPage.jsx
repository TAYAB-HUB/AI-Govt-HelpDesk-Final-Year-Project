import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import Layout from '../components/Layout';
import toast from 'react-hot-toast';
import { 
  ArrowLeft, 
  Send, 
  Clock, 
  CheckCircle2, 
  AlertCircle, 
  User, 
  Building2, 
  Tag, 
  ShieldCheck,
  MessageSquare
} from 'lucide-react';

const STATUS_OPTIONS = [
  { value: 'Open', label: 'Open', color: 'bg-blue-100 text-blue-800' },
  { value: 'InProgress', label: 'In Progress', color: 'bg-yellow-100 text-yellow-800' },
  { value: 'Resolved', label: 'Resolved', color: 'bg-green-100 text-green-800' },
  { value: 'Closed', label: 'Closed', color: 'bg-gray-100 text-gray-800' },
];

export default function TicketDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const queryClient = useQueryClient();

  const [commentText, setCommentText] = useState('');
  const [newStatus, setNewStatus] = useState('');

  const isStaff = user && ['Officer', 'DeptAdmin', 'SuperAdmin'].includes(user.role);

  // Fetch ticket details
  const { 
    data: ticket, 
    isLoading: ticketLoading, 
    error: ticketError 
  } = useQuery({
    queryKey: ['ticket', id],
    queryFn: async () => {
      const res = await api.get(`/tickets/${id}`);
      return res.data;
    },
  });

  // Fetch comments/answers
  const { 
    data: comments, 
    isLoading: commentsLoading 
  } = useQuery({
    queryKey: ['ticketComments', id],
    queryFn: async () => {
      const res = await api.get(`/tickets/${id}/comments`);
      return res.data;
    },
  });

  // Initialize status selector once ticket loads
  useEffect(() => {
    if (ticket?.status) {
      setNewStatus(ticket.status);
    }
  }, [ticket?.status]);

  // Submit comment / answer mutation
  const commentMutation = useMutation({
    mutationFn: async ({ comment, status }) => {
      const payload = {
        comment,
        status: isStaff && status !== ticket?.status ? status : null,
      };
      const res = await api.post(`/tickets/${id}/comments`, payload);
      return res.data;
    },
    onSuccess: () => {
      toast.success(isStaff ? 'Response and status recorded!' : 'Reply submitted!');
      setCommentText('');
      queryClient.invalidateQueries(['ticket', id]);
      queryClient.invalidateQueries(['ticketComments', id]);
      queryClient.invalidateQueries(['tickets']);
    },
    onError: (err) => {
      toast.error(err.response?.data?.detail || 'Failed to submit response');
    },
  });

  // Direct status update mutation (without comment)
  const statusMutation = useMutation({
    mutationFn: async (updatedStatus) => {
      const res = await api.patch(`/tickets/${id}`, { status: updatedStatus });
      return res.data;
    },
    onSuccess: () => {
      toast.success('Ticket status updated!');
      queryClient.invalidateQueries(['ticket', id]);
      queryClient.invalidateQueries(['tickets']);
    },
    onError: (err) => {
      toast.error(err.response?.data?.detail || 'Failed to update status');
    },
  });

  const handlePostAnswer = (e) => {
    e.preventDefault();
    if (!commentText.trim() && (!isStaff || newStatus === ticket?.status)) {
      toast.error('Please enter a response message.');
      return;
    }
    commentMutation.mutate({
      comment: commentText.trim() || `Status updated to ${newStatus}`,
      status: newStatus,
    });
  };

  const getStatusColor = (status) => {
    const found = STATUS_OPTIONS.find((s) => s.value === status);
    return found ? found.color : 'bg-gray-100 text-gray-800';
  };

  const getPriorityColor = (priority) => {
    const colors = {
      Low: 'bg-gray-100 text-gray-800',
      Medium: 'bg-blue-100 text-blue-800',
      High: 'bg-orange-100 text-orange-800',
      Urgent: 'bg-red-100 text-red-800',
    };
    return colors[priority] || 'bg-gray-100 text-gray-800';
  };

  if (ticketLoading) {
    return (
      <Layout>
        <div className="flex flex-col items-center justify-center min-h-[50vh]">
          <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600 mb-4"></div>
          <p className="text-gray-500">Loading ticket #{id}...</p>
        </div>
      </Layout>
    );
  }

  if (ticketError || !ticket) {
    return (
      <Layout>
        <div className="max-w-3xl mx-auto py-12 px-4 text-center">
          <AlertCircle size={48} className="mx-auto text-red-500 mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Ticket Not Found</h2>
          <p className="text-gray-600 mb-6">
            {ticketError?.response?.data?.detail || 'The requested ticket could not be loaded or you do not have permission to view it.'}
          </p>
          <Link
            to="/tickets"
            className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
          >
            <ArrowLeft size={18} />
            Back to Tickets
          </Link>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-4xl mx-auto pb-12">
        {/* Top Back Navigation */}
        <div className="mb-6 flex items-center justify-between">
          <button
            onClick={() => navigate('/tickets')}
            className="inline-flex items-center gap-2 text-sm font-medium text-gray-600 hover:text-blue-600 transition"
          >
            <ArrowLeft size={16} />
            Back to Tickets
          </button>
          <span className="text-sm font-mono text-gray-500">
            Ticket ID: #{ticket.id}
          </span>
        </div>

        {/* Main Ticket Card */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden mb-6">
          <div className="p-6">
            <div className="flex flex-wrap items-center gap-2 mb-3">
              <span className="font-mono text-sm px-2.5 py-1 bg-gray-100 rounded text-gray-700 font-semibold">
                {ticket.ticket_number}
              </span>
              <span className={`text-xs font-semibold px-2.5 py-1 rounded-full ${getStatusColor(ticket.status)}`}>
                {ticket.status}
              </span>
              <span className={`text-xs font-semibold px-2.5 py-1 rounded-full ${getPriorityColor(ticket.priority)}`}>
                {ticket.priority} Priority
              </span>
            </div>

            <h1 className="text-2xl font-bold text-gray-900 mb-3">{ticket.title}</h1>

            <div className="flex flex-wrap items-center gap-4 text-xs text-gray-500 mb-6 pb-4 border-b border-gray-100">
              <span className="flex items-center gap-1.5">
                <Tag size={14} className="text-gray-400" />
                Category: <strong>{ticket.category}</strong>
              </span>
              <span className="flex items-center gap-1.5">
                <Clock size={14} className="text-gray-400" />
                Created: {new Date(ticket.created_at).toLocaleString()}
              </span>
              {ticket.department_name && (
                <span className="flex items-center gap-1.5">
                  <Building2 size={14} className="text-gray-400" />
                  Dept: {ticket.department_name}
                </span>
              )}
            </div>

            <div className="prose max-w-none text-gray-800 text-sm whitespace-pre-wrap leading-relaxed bg-slate-50 p-4 rounded-lg border border-slate-100">
              {ticket.description}
            </div>
          </div>

          {/* Quick Status Control for Staff / HR */}
          {isStaff && (
            <div className="bg-blue-50/60 px-6 py-4 border-t border-blue-100 flex flex-wrap items-center justify-between gap-4">
              <div className="flex items-center gap-2 text-sm text-blue-900 font-medium">
                <ShieldCheck size={18} className="text-blue-700" />
                Officer Actions: Update Ticket Status
              </div>
              <div className="flex items-center gap-2">
                {STATUS_OPTIONS.map((opt) => (
                  <button
                    key={opt.value}
                    onClick={() => statusMutation.mutate(opt.value)}
                    disabled={statusMutation.isPending || ticket.status === opt.value}
                    className={`text-xs font-semibold px-3 py-1.5 rounded-lg border transition ${
                      ticket.status === opt.value
                        ? 'bg-blue-600 text-white border-blue-600 shadow-sm'
                        : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
                    } disabled:opacity-70`}
                  >
                    {opt.label}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Conversation / Answers Timeline */}
        <div className="mb-6">
          <div className="flex items-center gap-2 mb-4">
            <MessageSquare size={20} className="text-gray-700" />
            <h2 className="text-lg font-bold text-gray-900">
              Official Responses & Updates ({comments?.length || 0})
            </h2>
          </div>

          {commentsLoading ? (
            <div className="text-center py-6 text-gray-500 text-sm">Loading responses...</div>
          ) : comments?.length === 0 ? (
            <div className="bg-white rounded-xl p-8 text-center border border-gray-200 text-gray-500">
              <p>No answers or responses posted yet.</p>
              {isStaff ? (
                <p className="text-xs text-blue-600 mt-1">
                  As an Officer/HR, you can answer this ticket below.
                </p>
              ) : (
                <p className="text-xs text-gray-400 mt-1">
                  An assigned officer or HR will respond to your ticket soon.
                </p>
              )}
            </div>
          ) : (
            <div className="space-y-4">
              {comments.map((c) => {
                const isCommentFromStaff = ['Officer', 'DeptAdmin', 'SuperAdmin'].includes(c.user_role);
                return (
                  <div
                    key={c.id}
                    className={`rounded-xl p-5 border shadow-sm transition ${
                      isCommentFromStaff
                        ? 'bg-blue-50/40 border-blue-200'
                        : 'bg-white border-gray-200'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <div
                          className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold ${
                            isCommentFromStaff
                              ? 'bg-blue-600 text-white'
                              : 'bg-gray-200 text-gray-700'
                          }`}
                        >
                          <User size={14} />
                        </div>
                        <div>
                          <span className="text-sm font-semibold text-gray-900 mr-2">
                            {c.user_name || (isCommentFromStaff ? 'Officer Response' : 'Employee')}
                          </span>
                          <span
                            className={`text-[11px] font-semibold px-2 py-0.5 rounded-full ${
                              isCommentFromStaff
                                ? 'bg-blue-100 text-blue-800'
                                : 'bg-gray-100 text-gray-700'
                            }`}
                          >
                            {c.user_role || (isCommentFromStaff ? 'Officer' : 'Employee')}
                          </span>
                        </div>
                      </div>
                      <span className="text-xs text-gray-400 font-mono">
                        {new Date(c.created_at).toLocaleString()}
                      </span>
                    </div>

                    <div className="text-sm text-gray-800 whitespace-pre-wrap pl-9 leading-relaxed">
                      {c.comment}
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Answer / Reply Box */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-base font-bold text-gray-900 mb-2 flex items-center gap-2">
            <Send size={16} className="text-blue-600" />
            {isStaff ? 'Post Official Answer / Resolution' : 'Reply to Ticket'}
          </h3>
          <p className="text-xs text-gray-500 mb-4">
            {isStaff
              ? 'Provide guidance, answer employee queries, or resolve this request. You can also update the ticket status.'
              : 'Add additional details or follow up with the officer.'}
          </p>

          <form onSubmit={handlePostAnswer} className="space-y-4">
            <div>
              <textarea
                value={commentText}
                onChange={(e) => setCommentText(e.target.value)}
                rows={4}
                placeholder={
                  isStaff
                    ? 'Write official answer or resolution details here...'
                    : 'Write your reply or additional comments here...'
                }
                className="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
              />
            </div>

            {isStaff && (
              <div className="flex flex-wrap items-center gap-3">
                <label className="text-xs font-semibold text-gray-700">
                  Update Status to:
                </label>
                <select
                  value={newStatus}
                  onChange={(e) => setNewStatus(e.target.value)}
                  className="px-3 py-1.5 border border-gray-300 rounded-lg text-sm bg-white focus:ring-2 focus:ring-blue-500"
                >
                  {STATUS_OPTIONS.map((opt) => (
                    <option key={opt.value} value={opt.value}>
                      {opt.label}
                    </option>
                  ))}
                </select>
              </div>
            )}

            <div className="flex justify-end">
              <button
                type="submit"
                disabled={commentMutation.isPending}
                className="inline-flex items-center gap-2 bg-blue-600 text-white font-medium py-2.5 px-5 rounded-lg hover:bg-blue-700 transition disabled:opacity-50 text-sm shadow-sm"
              >
                <Send size={15} />
                {commentMutation.isPending
                  ? 'Submitting...'
                  : isStaff
                  ? 'Post Official Answer'
                  : 'Send Reply'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Layout>
  );
}
