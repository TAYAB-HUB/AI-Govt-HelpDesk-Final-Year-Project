import { useCallback, useState } from "react";
import { View, Text, FlatList, TouchableOpacity, StyleSheet, RefreshControl } from "react-native";
import { useFocusEffect } from "@react-navigation/native";
import { api } from "../api/client";

const STATUS_COLORS = {
  open: "#b8791e",
  in_progress: "#127a6b",
  resolved: "#17233f",
  closed: "#4b5261",
};

export default function TicketsScreen({ navigation }) {
  const [tickets, setTickets] = useState([]);
  const [refreshing, setRefreshing] = useState(false);

  const load = useCallback(async () => {
    try {
      const data = await api.listTickets();
      setTickets(data);
    } catch {
      // silently ignore - user will see an empty list, not worth blocking the UI
    }
  }, []);

  useFocusEffect(
    useCallback(() => {
      load();
    }, [load])
  );

  async function onRefresh() {
    setRefreshing(true);
    await load();
    setRefreshing(false);
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>My tickets</Text>
        <TouchableOpacity style={styles.newButton} onPress={() => navigation.navigate("NewTicket", {})}>
          <Text style={styles.newButtonText}>+ New</Text>
        </TouchableOpacity>
      </View>

      <FlatList
        data={tickets}
        keyExtractor={(t) => String(t.id)}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
        contentContainerStyle={{ padding: 16, gap: 10 }}
        ListEmptyComponent={<Text style={styles.empty}>No tickets yet. Ask a question in Chat, or create one here.</Text>}
        renderItem={({ item }) => (
          <TouchableOpacity style={styles.card} onPress={() => navigation.navigate("TicketDetail", { ticketId: item.id })}>
            <View style={styles.cardTop}>
              <Text style={styles.subject} numberOfLines={1}>{item.subject}</Text>
              <View style={[styles.stamp, { borderColor: STATUS_COLORS[item.status] }]}>
                <Text style={[styles.stampText, { color: STATUS_COLORS[item.status] }]}>
                  {item.status.replace("_", " ")}
                </Text>
              </View>
            </View>
            <Text style={styles.category}>{item.category}</Text>
          </TouchableOpacity>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#f6f4ef" },
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    padding: 16,
    paddingBottom: 0,
  },
  title: { fontSize: 22, fontWeight: "600", color: "#17233f" },
  newButton: { backgroundColor: "#17233f", borderRadius: 6, paddingHorizontal: 12, paddingVertical: 8 },
  newButtonText: { color: "#fff", fontWeight: "600", fontSize: 13 },
  empty: { color: "#4b5261", textAlign: "center", marginTop: 40, fontSize: 14 },
  card: {
    backgroundColor: "#fff",
    borderRadius: 8,
    borderWidth: 1,
    borderColor: "#dcd7cc",
    padding: 14,
  },
  cardTop: { flexDirection: "row", justifyContent: "space-between", alignItems: "flex-start", gap: 8 },
  subject: { fontSize: 15, fontWeight: "600", color: "#21262d", flex: 1 },
  category: { fontSize: 12, color: "#4b5261", marginTop: 4 },
  stamp: { borderWidth: 1.5, borderRadius: 3, paddingHorizontal: 8, paddingVertical: 2, transform: [{ rotate: "-2deg" }] },
  stampText: { fontSize: 10, fontWeight: "600", textTransform: "uppercase", letterSpacing: 0.5 },
});
