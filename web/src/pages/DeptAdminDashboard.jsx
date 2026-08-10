import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../services/api';
import toast from 'react-hot-toast';
import { Upload, FileText, Users, BarChart3 } from 'lucide-react';
import Layout from '../components/Layout';
import { useAuth } from '../context/AuthContext';

export default function DeptAdminDashboard() {
  const { user } = useAuth();
  const queryClient = useQueryClient();
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadTitle, setUploadTitle] = useState('');

  // Fetch analytics
  const { data: analytics } = useQuery({
    queryKey: ['analytics', user.department_id],
    queryFn: async () => {
      const res = await api.get(`/analytics/dashboard?department_id=${user.department_id}`);
      return res.data;
    }
  });

  // Fetch documents
  const { data: documents } = useQuery({
    queryKey: ['documents', user.department_id],
    queryFn: async () => {
      const res = await api.get(`/documents/department/${user.department_id}`);
      return res.data;
    }
  });

  // Upload mutation
  const uploadMutation = useMutation({
    mutationFn: async (formData) => {
      const res = await api.post('/documents/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      return res.data;
    },
    onSuccess: () => {
      toast.success('Document uploaded and indexed successfully!');
      queryClient.invalidateQueries(['documents']);
      setSelectedFile(null);
      setUploadTitle('');
    },
    onError: (error) => {
      toast.error(error.response?.data?.detail || 'Upload failed');
    }
  });

  const handleUpload = (e) => {
    e.preventDefault();
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('title', uploadTitle || selectedFile.name);
    formData.append('department_id', user.department_id);

    uploadMutation.mutate(formData);
  };

  return (
    <Layout>
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Department Admin Dashboard</h1>
          <p className="text-gray-600 mt-2">Manage documents and view analytics</p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Total Tickets</p>
                <p className="text-3xl font-bold text-blue-600 mt-1">{analytics?.tickets.total || 0}</p>
              </div>
              <div className="bg-blue-100 p-3 rounded-full">
                <BarChart3 className="text-blue-600" size={24} />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Documents</p>
                <p className="text-3xl font-bold text-green-600 mt-1">{documents?.length || 0}</p>
              </div>
              <div className="bg-green-100 p-3 rounded-full">
                <FileText className="text-green-600" size={24} />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Chat Interactions</p>
                <p className="text-3xl font-bold text-purple-600 mt-1">{analytics?.chat.total_interactions || 0}</p>
              </div>
              <div className="bg-purple-100 p-3 rounded-full">
                <Users className="text-purple-600" size={24} />
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Upload Document */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <Upload size={24} />
              Upload Document
            </h2>
            <form onSubmit={handleUpload} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Document Title (Optional)
                </label>
                <input
                  type="text"
                  value={uploadTitle}
                  onChange={(e) => setUploadTitle(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  placeholder="Leave as blank to use filename"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Select File (PDF or TXT) *
                </label>
                <input
                  type="file"
                  accept=".pdf,.txt"
                  onChange={(e) => setSelectedFile(e.target.files[0])}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>

              <button
                type="submit"
                disabled={!selectedFile || uploadMutation.isPending}
                className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
              >
                {uploadMutation.isPending ? 'Uploading...' : 'Upload & Index Document'}
              </button>
            </form>
          </div>

          {/* Department Documents */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <FileText size={24} />
              Department Documents
            </h2>
            {documents?.length > 0 ? (
              <div className="space-y-2 max-h-96 overflow-y-auto">
                {documents.map(doc => (
                  <div key={doc.id} className="p-3 border border-gray-200 rounded-lg">
                    <p className="font-medium text-gray-900">{doc.title}</p>
                    <div className="flex items-center gap-3 mt-1 text-xs text-gray-500">
                      <span>{doc.file_type.toUpperCase()}</span>
                      <span>{(doc.file_size / 1024).toFixed(1)} KB</span>
                      <span>{new Date(doc.created_at).toLocaleDateString()}</span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500 text-sm">No documents uploaded yet</p>
            )}
          </div>
        </div>
      </div>
    </Layout>
  );
}