import React, { useState, useEffect } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { AuthContext } from './src/context/AuthContext';

// Screens
import LoginScreen from './src/screens/LoginScreen';
import DepartmentSelectScreen from './src/screens/DepartmentSelectScreen';
import ChatScreen from './src/screens/ChatScreen';
import TicketsListScreen from './src/screens/TicketsListScreen';
import TicketDetailScreen from './src/screens/TicketDetailScreen';
import CreateTicketScreen from './src/screens/CreateTicketScreen';

const Stack = createStackNavigator();

export default function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check for existing session
    AsyncStorage.getItem('user').then(userData => {
      if (userData) {
        setUser(JSON.parse(userData));
      }
      setLoading(false);
    });
  }, []);

  const authContext = {
    user,
    login: async (userData, token) => {
      await AsyncStorage.setItem('user', JSON.stringify(userData));
      await AsyncStorage.setItem('token', token);
      setUser(userData);
    },
    logout: async () => {
      await AsyncStorage.removeItem('user');
      await AsyncStorage.removeItem('token');
      setUser(null);
    }
  };

  if (loading) {
    return null; // Or a splash screen
  }

  return (
    <AuthContext.Provider value={authContext}>
      <NavigationContainer>
        <Stack.Navigator>
          {!user ? (
            <Stack.Screen 
              name="Login" 
              component={LoginScreen}
              options={{ headerShown: false }}
            />
          ) : (
            <>
              <Stack.Screen 
                name="DepartmentSelect" 
                component={DepartmentSelectScreen}
                options={{ title: 'Select Department' }}
              />
              <Stack.Screen 
                name="Chat" 
                component={ChatScreen}
                options={{ title: 'AI Assistant' }}
              />
              <Stack.Screen 
                name="TicketsList" 
                component={TicketsListScreen}
                options={{ title: 'My Tickets' }}
              />
              <Stack.Screen 
                name="TicketDetail" 
                component={TicketDetailScreen}
                options={{ title: 'Ticket Details' }}
              />
              <Stack.Screen 
                name="CreateTicket" 
                component={CreateTicketScreen}
                options={{ title: 'Create Ticket' }}
              />
            </>
          )}
        </Stack.Navigator>
      </NavigationContainer>
    </AuthContext.Provider>
  );
}