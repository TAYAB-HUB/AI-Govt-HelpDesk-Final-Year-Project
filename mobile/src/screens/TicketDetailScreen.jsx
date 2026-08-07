import { useCallback, useState } from "react";
import { View, Text, StyleSheet, ScrollView, ActivityIndicator } from "react-native";
import { useFocusEffect } from "@react-navigation/native";
import { api } from "../api/client";

const STATUS_COLORS = {
  open: "#b8791e",
  in_progress: "#127a6b",
  resolved: "#17233f",
  closed: "#4b5261",
};

export default function TicketDetailScreen({ route }) {
  const { ticketId } = route.params;
  const [ticket, setTicket] = useState(null);
  const [loading, setLoading] = useState(true);

  useFocusEffect(
    useCallback(() => {
      setLoading(true);
      api
        .getTicket(ticketId)
        .then(setTicket)
        .finally(() => setLoading(false));
    }, [ticketId])
  );

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator color="#17233f" />
      </View>
    );
  }
  if (!ticket) {
    return (
      <View style={styles.center}>
        <Text>Ticket not found.</Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container} contentContainerStyle={{ padding: 16 }}>
      <View style={[styles.stamp, { borderColor: STATUS_COLORS[ticket.status] }]}>
        <Text style={[styles.stampText, { color: STATUS_COLORS[ticket.status] }]}>
          {ticket.status.replace("_", " ")}
        </Text>
      </View>

      <Text style={styles.subject}>{ticket.subject}</Text>
      <Text style={styles.meta}>{ticket.category} · Priority: {ticket.priority}</Text>
      <Text style={styles.description}>{ticket.description}</Text>

      <Text style={styles.timelineHeader}>Timeline</Text>
      {ticket.comments.length === 0 && <Text style={styles.empty}>No updates yet.</Text>}
      {ticket.comments.map((c) => (
        <View key={c.id} style={styles.commentRow}>
          <Text style={styles.commentBody}>{c.body}</Text>
          {c.status_change_to && (
            <Text style={styles.commentStatus}>Status changed to: {c.status_change_to.replace("_", " ")}</Text>
          )}
          <Text style={styles.commentDate}>{new Date(c.created_at).toLocaleString()}</Text>
        </View>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#f6f4ef" },
  center: { flex: 1, justifyContent: "center", alignItems: "center", backgroundColor: "#f6f4ef" },
  stamp: {
    alignSelf: "flex-start",
    borderWidth: 1.5,
    borderRadius: 3,
    paddingHorizontal: 10,
    paddingVertical: 3,
    transform: [{ rotate: "-2deg" }],
    marginBottom: 12,
  },
  stampText: { fontSize: 11, fontWeight: "600", textTransform: "uppercase", letterSpacing: 0.5 },
  subject: { fontSize: 20, fontWeight: "600", color: "#21262d" },
  meta: { fontSize: 13, color: "#4b5261", marginTop: 4, marginBottom: 12 },
  description: { fontSize: 15, color: "#21262d", lineHeight: 22, marginBottom: 20 },
  timelineHeader: { fontSize: 13, fontWeight: "600", color: "#4b5261", marginBottom: 8, textTransform: "uppercase" },
  empty: { color: "#4b5261", fontSize: 13 },
  commentRow: { borderTopWidth: 1, borderColor: "#dcd7cc", borderStyle: "dashed", paddingTop: 10, marginTop: 10 },
  commentBody: { fontSize: 14, color: "#21262d" },
  commentStatus: { fontSize: 12, color: "#127a6b", fontWeight: "600", marginTop: 4 },
  commentDate: { fontSize: 11, color: "#4b5261", marginTop: 4 },
});
