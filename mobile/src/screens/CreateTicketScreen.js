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

const PRIORITIES = ["low", "medium", "high", "urgent"];

export default function NewTicketScreen({ route, navigation }) {
  const { departmentId, prefillSubject, prefillDescription, originChatLogId } = route.params || {};

  const [departments, setDepartments] = useState([]);
  const [selectedDept, setSelectedDept] = useState(departmentId || null);
  const [category, setCategory] = useState("");
  const [subject, setSubject] = useState(prefillSubject || "");
  const [description, setDescription] = useState(prefillDescription || "");
  const [priority, setPriority] = useState("medium");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    api.listDepartments().then((depts) => {
      setDepartments(depts);
      if (!selectedDept && depts.length) setSelectedDept(depts[0].id);
    });
  }, []);

  async function handleSubmit() {
    if (!selectedDept || !category.trim() || !subject.trim() || !description.trim()) {
      Alert.alert("Missing info", "Please fill in department, category, subject, and description.");
      return;
    }
    setSubmitting(true);
    try {
      await api.createTicket({
        department_id: selectedDept,
        category: category.trim(),
        subject: subject.trim(),
        description: description.trim(),
        priority,
        origin_chat_log_id: originChatLogId,
      });
      Alert.alert("Ticket raised", "An officer will follow up soon.");
      navigation.navigate("Tickets");
    } catch (e) {
      Alert.alert("Couldn't create ticket", e.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <ScrollView style={styles.container} contentContainerStyle={{ padding: 16, paddingBottom: 40 }}>
      <Text style={styles.title}>Raise a ticket</Text>

      <Text style={styles.label}>Department</Text>
      <ScrollView horizontal showsHorizontalScrollIndicator={false} style={{ marginBottom: 12 }}>
        {departments.map((d) => (
          <TouchableOpacity
            key={d.id}
            onPress={() => setSelectedDept(d.id)}
            style={[styles.chip, selectedDept === d.id && styles.chipActive]}
          >
            <Text style={[styles.chipText, selectedDept === d.id && styles.chipTextActive]}>{d.code}</Text>
          </TouchableOpacity>
        ))}
      </ScrollView>

      <Text style={styles.label}>Category</Text>
      <TextInput style={styles.input} placeholder="e.g. HR - Leave" value={category} onChangeText={setCategory} />

      <Text style={styles.label}>Priority</Text>
      <View style={{ flexDirection: "row", gap: 8, marginBottom: 12 }}>
        {PRIORITIES.map((p) => (
          <TouchableOpacity
            key={p}
            onPress={() => setPriority(p)}
            style={[styles.chip, priority === p && styles.chipActive]}
          >
            <Text style={[styles.chipText, priority === p && styles.chipTextActive]}>{p}</Text>
          </TouchableOpacity>
        ))}
      </View>

      <Text style={styles.label}>Subject</Text>
      <TextInput style={styles.input} value={subject} onChangeText={setSubject} />

      <Text style={styles.label}>Description</Text>
      <TextInput
        style={styles.textarea}
        multiline
        value={description}
        onChangeText={setDescription}
      />

      <TouchableOpacity style={styles.button} onPress={handleSubmit} disabled={submitting}>
        {submitting ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>Submit ticket</Text>}
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#f6f4ef" },
  title: { fontSize: 22, fontWeight: "600", color: "#17233f", marginBottom: 16 },
  label: { fontSize: 13, color: "#4b5261", marginBottom: 6, marginTop: 4 },
  input: {
    borderWidth: 1,
    borderColor: "#dcd7cc",
    borderRadius: 6,
    paddingHorizontal: 12,
    paddingVertical: 10,
    backgroundColor: "#fff",
    fontSize: 15,
    marginBottom: 12,
  },
  textarea: {
    borderWidth: 1,
    borderColor: "#dcd7cc",
    borderRadius: 8,
    backgroundColor: "#fff",
    padding: 12,
    minHeight: 100,
    fontSize: 15,
    textAlignVertical: "top",
    marginBottom: 16,
  },
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
  button: { backgroundColor: "#17233f", borderRadius: 6, paddingVertical: 14, alignItems: "center" },
  buttonText: { color: "#fff", fontWeight: "600", fontSize: 15 },
});
