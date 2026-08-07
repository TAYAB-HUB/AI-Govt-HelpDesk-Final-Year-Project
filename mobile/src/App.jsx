import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { View, ActivityIndicator, TouchableOpacity, Text } from "react-native";
import { AuthProvider, useAuth } from "./context/AuthContext";
import LoginScreen from "./screens/LoginScreen";
import ChatScreen from "./screens/ChatScreen";
import TicketsScreen from "./screens/TicketsScreen";
import TicketDetailScreen from "./screens/TicketDetailScreen";
import NewTicketScreen from "./screens/NewTicketScreen";

const Stack = createNativeStackNavigator();

function LogoutButton() {
  const { logout } = useAuth();
  return (
    <TouchableOpacity onPress={logout} style={{ paddingHorizontal: 8 }}>
      <Text style={{ color: "#fff", fontWeight: "600" }}>Log out</Text>
    </TouchableOpacity>
  );
}

function NavButton({ label, onPress }) {
  return (
    <TouchableOpacity onPress={onPress} style={{ paddingHorizontal: 8 }}>
      <Text style={{ color: "#fff", fontWeight: "600" }}>{label}</Text>
    </TouchableOpacity>
  );
}

function AuthenticatedNavigator() {
  return (
    <Stack.Navigator
      screenOptions={{
        headerStyle: { backgroundColor: "#17233f" },
        headerTintColor: "#fff",
        headerTitleStyle: { fontWeight: "600" },
      }}
    >
      <Stack.Screen
        name="Chat"
        component={ChatScreen}
        options={({ navigation }) => ({
          title: "Ask a question",
          headerLeft: () => <NavButton label="Tickets" onPress={() => navigation.navigate("Tickets")} />,
          headerRight: LogoutButton,
        })}
      />
      <Stack.Screen
        name="Tickets"
        component={TicketsScreen}
        options={({ navigation }) => ({
          title: "My tickets",
          headerLeft: () => <NavButton label="Chat" onPress={() => navigation.navigate("Chat")} />,
          headerRight: LogoutButton,
        })}
      />
      <Stack.Screen name="TicketDetail" component={TicketDetailScreen} options={{ title: "Ticket" }} />
      <Stack.Screen name="NewTicket" component={NewTicketScreen} options={{ title: "Raise a ticket" }} />
    </Stack.Navigator>
  );
}

function Root() {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <View style={{ flex: 1, justifyContent: "center", alignItems: "center", backgroundColor: "#f6f4ef" }}>
        <ActivityIndicator color="#17233f" size="large" />
      </View>
    );
  }

  return (
    <NavigationContainer>
      {user ? <AuthenticatedNavigator /> : <LoginScreen />}
    </NavigationContainer>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <Root />
    </AuthProvider>
  );
}
