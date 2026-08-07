import { useState } from "react";
import { View, Text, TextInput, TouchableOpacity, StyleSheet, ActivityIndicator, Alert } from "react-native";
import { useAuth } from "../context/AuthContext";

export default function LoginScreen() {
  const { login } = useAuth();
  const [email, setEmail] = useState("employee@demo.gov.in");
  const [password, setPassword] = useState("Demo@1234");
  const [loading, setLoading] = useState(false);

  async function handleLogin() {
    setLoading(true);
    try {
      await login(email.trim(), password);
    } catch (e) {
      Alert.alert("Login failed", e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <View style={styles.container}>
      <Text style={styles.eyebrow}>ACADEMIC PROTOTYPE</Text>
      <Text style={styles.title}>Government{"\n"}Helpdesk</Text>
      <Text style={styles.subtitle}>Employee sign in</Text>

      <View style={styles.form}>
        <Text style={styles.label}>Email</Text>
        <TextInput
          style={styles.input}
          value={email}
          onChangeText={setEmail}
          autoCapitalize="none"
          keyboardType="email-address"
        />
        <Text style={styles.label}>Password</Text>
        <TextInput style={styles.input} value={password} onChangeText={setPassword} secureTextEntry />

        <TouchableOpacity style={styles.button} onPress={handleLogin} disabled={loading}>
          {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>Sign in</Text>}
        </TouchableOpacity>

        <Text style={styles.hint}>
          Demo password for every seeded account: Demo@1234{"\n"}
          (e.g. employee@demo.gov.in)
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#f6f4ef", padding: 24, paddingTop: 80 },
  eyebrow: { fontFamily: "monospace", fontSize: 11, letterSpacing: 1, color: "#4b5261", marginBottom: 6 },
  title: { fontSize: 32, fontWeight: "600", color: "#17233f", lineHeight: 36 },
  subtitle: { fontSize: 14, color: "#4b5261", marginTop: 8, marginBottom: 32 },
  form: { gap: 4 },
  label: { fontSize: 13, color: "#4b5261", marginBottom: 4, marginTop: 12 },
  input: {
    borderWidth: 1,
    borderColor: "#dcd7cc",
    borderRadius: 6,
    paddingHorizontal: 12,
    paddingVertical: 10,
    backgroundColor: "#fff",
    fontSize: 15,
  },
  button: {
    backgroundColor: "#17233f",
    borderRadius: 6,
    paddingVertical: 14,
    alignItems: "center",
    marginTop: 24,
  },
  buttonText: { color: "#fff", fontWeight: "600", fontSize: 15 },
  hint: { fontSize: 12, color: "#4b5261", marginTop: 20, textAlign: "center", lineHeight: 18 },
});
