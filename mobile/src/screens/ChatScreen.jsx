import { useEffect, useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  ActivityIndicator,
  Alert,
} from "react-native";
import { api } from "../api/client";

export default function ChatScreen({ navigation }) {
  const [departments, setDepartments] = useState([]);
  const [departmentId, setDepartmentId] = useState(null);
  const [question, setQuestion] = useState("");
  const [asking, setAsking] = useState(false);
  const [result, setResult] = useState(null);

  useEffect(() => {
    api.listDepartments().then((depts) => {
      setDepartments(depts);
      if (depts.length) setDepartmentId(depts[0].id);
    });
  }, []);

  async function handleAsk() {
    if (!question.trim() || !departmentId) return;
    setAsking(true);
    setResult(null);
    try {
      const resp = await api.askChat(departmentId, question.trim());
      setResult(resp);
    } catch (e) {
      Alert.alert("Couldn't get an answer", e.message);
    } finally {
      setAsking(false);
    }
  }

  function goRaiseTicket() {
    navigation.navigate("NewTicket", {
      departmentId,
      prefillSubject: question.slice(0, 80),
      prefillDescription: question,
      originChatLogId: result?.chat_log_id,
    });
  }

  return (
    <ScrollView style={styles.container} contentContainerStyle={{ padding: 16, paddingBottom: 40 }}>
      <Text style={styles.title}>Ask a question</Text>

      <Text style={styles.label}>Department</Text>
      <ScrollView horizontal showsHorizontalScrollIndicator={false} style={{ marginBottom: 12 }}>
        {departments.map((d) => (
          <TouchableOpacity
            key={d.id}
            onPress={() => setDepartmentId(d.id)}
            style={[styles.chip, departmentId === d.id && styles.chipActive]}
          >
            <Text style={[styles.chipText, departmentId === d.id && styles.chipTextActive]}>{d.code}</Text>
          </TouchableOpacity>
        ))}
      </ScrollView>

      <TextInput
        style={styles.textarea}
        multiline
        placeholder="e.g. How many days of earned leave am I entitled to?"
        value={question}
        onChangeText={setQuestion}
      />

      <TouchableOpacity style={styles.button} onPress={handleAsk} disabled={asking}>
        {asking ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>Ask</Text>}
      </TouchableOpacity>

      {result && (
        <View style={styles.resultCard}>
          <Text style={styles.answer}>{result.answer}</Text>

          {result.sources?.length > 0 && (
            <View style={{ marginTop: 12 }}>
              <Text style={styles.sourcesLabel}>SOURCES</Text>
              {result.sources.map((s, i) => (
                <View key={i} style={styles.sourceRow}>
                  <Text style={styles.sourceTitle}>{s.document_title}</Text>
                  <Text style={styles.sourceSnippet}>{s.snippet}</Text>
                </View>
              ))}
            </View>
          )}

          {result.suggest_ticket && (
            <TouchableOpacity style={styles.ticketButton} onPress={goRaiseTicket}>
              <Text style={styles.ticketButtonText}>This didn't fully answer it — raise a ticket</Text>
            </TouchableOpacity>
          )}
        </View>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#f6f4ef" },
  title: { fontSize: 22, fontWeight: "600", color: "#17233f", marginBottom: 16 },
  label: { fontSize: 13, color: "#4b5261", marginBottom: 6 },
  chip: {
    borderWidth: 1,
    borderColor: "#dcd7cc",
    borderRadius: 20,
    paddingHorizontal: 14,
    paddingVertical: 6,
    marginRight: 8,
    backgroundColor: "#fff",
  },
  chipActive: { backgroundColor: "#127a6b", borderColor: "#127a6b" },
  chipText: { fontSize: 13, color: "#4b5261", fontWeight: "500" },
  chipTextActive: { color: "#fff" },
  textarea: {
    borderWidth: 1,
    borderColor: "#dcd7cc",
    borderRadius: 8,
    backgroundColor: "#fff",
    padding: 12,
    minHeight: 90,
    fontSize: 15,
    textAlignVertical: "top",
  },
  button: {
    backgroundColor: "#17233f",
    borderRadius: 6,
    paddingVertical: 12,
    alignItems: "center",
    marginTop: 12,
  },
  buttonText: { color: "#fff", fontWeight: "600" },
  resultCard: {
    marginTop: 20,
    backgroundColor: "#fff",
    borderRadius: 8,
    borderWidth: 1,
    borderColor: "#dcd7cc",
    padding: 16,
  },
  answer: { fontSize: 15, color: "#21262d", lineHeight: 22 },
  sourcesLabel: { fontSize: 11, color: "#4b5261", letterSpacing: 1, marginBottom: 6 },
  sourceRow: { borderTopWidth: 1, borderColor: "#dcd7cc", borderStyle: "dashed", paddingTop: 8, marginTop: 8 },
  sourceTitle: { fontSize: 13, fontWeight: "600", color: "#127a6b" },
  sourceSnippet: { fontSize: 12, color: "#4b5261", marginTop: 2 },
  ticketButton: {
    marginTop: 16,
    backgroundColor: "#b8791e",
    borderRadius: 6,
    paddingVertical: 10,
    alignItems: "center",
  },
  ticketButtonText: { color: "#fff", fontWeight: "600", fontSize: 13 },
});
