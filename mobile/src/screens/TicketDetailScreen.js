import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, ScrollView, ActivityIndicator, TextInput, TouchableOpacity } from 'react-native';
import api from '../services/api';

export default function TicketDetailScreen({ route }) {
  const { ticketId } = route.params;
  const [ticket, setTicket] = useState(null);
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTicketDetails();
    fetchComments();
  }, []);

  const fetchTicketDetails = async () => {
    try {
      const response = await api.get(`/tickets/${ticketId}`);
      setTicket(response.data);
    } catch (error) {
      console.error('Failed to fetch ticket', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchComments = async () => {
    try {
      const response = await api.get(`/tickets/${ticketId}/comments`);
      setComments(response.data);
    } catch (error) {
      console.error('Failed to fetch comments', error);
    }
  };

  const addComment = async () => {
    if (!newComment.trim()) return;

    try {
      await api.post(`/tickets/${ticketId}/comments`, {
        comment: newComment,
        is_internal: false
      });
      setNewComment('');
      fetchComments();
    } catch (error) {
      console.error('Failed to add comment', error);
    }
  };

  if (loading) {
    return (
      <View style={styles.loading}>
        <ActivityIndicator size="large" color="#2563eb" />
      </View>
    );
  }

  if (!ticket) {
    return (
      <View style={styles.loading}>
        <Text>Ticket not found</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <ScrollView style={styles.content}>
        <View style={styles.header}>
          <Text style={styles.ticketNumber}>{ticket.ticket_number}</Text>
          <View style={styles.badges}>
            <View style={[styles.badge, styles.statusBadge]}>
              <Text style={styles.badgeText}>{ticket.status}</Text>
            </View>
            <View style={[styles.badge, styles.priorityBadge]}>
              <Text style={styles.badgeText}>{ticket.priority}</Text>
            </View>
          </View>
        </View>

        <Text style={styles.title}>{ticket.title}</Text>
        <Text style={styles.description}>{ticket.description}</Text>

        <View style={styles.meta}>
          <Text style={styles.metaText}>Category: {ticket.category}</Text>
          <Text style={styles.metaText}>
            Created: {new Date(ticket.created_at).toLocaleString()}
          </Text>
        </View>

        <View style={styles.commentsSection}>
          <Text style={styles.sectionTitle}>Comments</Text>
          {comments.map(comment => (
            <View key={comment.id} style={styles.comment}>
              <Text style={styles.commentText}>{comment.comment}</Text>
              <Text style={styles.commentDate}>
                {new Date(comment.created_at).toLocaleString()}
              </Text>
            </View>
          ))}
        </View>
      </ScrollView>

      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          placeholder="Add a comment..."
          value={newComment}
          onChangeText={setNewComment}
          multiline
        />
        <TouchableOpacity style={styles.sendButton} onPress={addComment}>
          <Text style={styles.sendButtonText}>Send</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f0f4f8',
  },
  loading: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  content: {
    flex: 1,
    padding: 20,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 15,
  },
  ticketNumber: {
    fontSize: 14,
    color: '#64748b',
    fontFamily: 'monospace',
  },
  badges: {
    flexDirection: 'row',
    gap: 8,
  },
  badge: {
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 4,
  },
  statusBadge: {
    backgroundColor: '#3b82f6',
  },
  priorityBadge: {
    backgroundColor: '#eab308',
  },
  badgeText: {
    color: 'white',
    fontSize: 12,
    fontWeight: '600',
  },
  title: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#1e293b',
    marginBottom: 10,
  },
  description: {
    fontSize: 16,
    color: '#475569',
    marginBottom: 15,
    lineHeight: 24,
  },
  meta: {
    marginBottom: 20,
  },
  metaText: {
    fontSize: 14,
    color: '#64748b',
    marginBottom: 5,
  },
  commentsSection: {
    marginTop: 20,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1e293b',
    marginBottom: 10,
  },
  comment: {
    backgroundColor: 'white',
    padding: 12,
    borderRadius: 8,
    marginBottom: 10,
  },
  commentText: {
    fontSize: 14,
    color: '#1e293b',
    marginBottom: 5,
  },
  commentDate: {
    fontSize: 12,
    color: '#94a3b8',
  },
  inputContainer: {
    flexDirection: 'row',
    padding: 15,
    backgroundColor: 'white',
    borderTopWidth: 1,
    borderTopColor: '#e2e8f0',
  },
  input: {
    flex: 1,
    backgroundColor: '#f0f4f8',
    borderRadius: 20,
    paddingHorizontal: 15,
    paddingVertical: 10,
    marginRight: 10,
    maxHeight: 100,
  },
  sendButton: {
    backgroundColor: '#2563eb',
    borderRadius: 20,
    paddingHorizontal: 20,
    justifyContent: 'center',
  },
  sendButtonText: {
    color: 'white',
    fontWeight: '600',
  },
});