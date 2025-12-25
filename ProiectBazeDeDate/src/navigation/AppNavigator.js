import React from "react";
import { TouchableOpacity, Text } from "react-native";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

import MoviesScreen from "../screens/MovieScreen";
import MovieProfile from "../screens/MovieProfile";
import LoginScreen from "../screens/LoginScreen";

const Stack = createNativeStackNavigator();

export default function AppNavigator({ user, setUser, userId, setUserId }) {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen
          name="Movies"
          options={({ navigation }) => ({
            title: "Filme",
            headerRight: () => (
              <TouchableOpacity onPress={() => !user && navigation.navigate("Login")}>
                <Text style={{ fontWeight: "700", paddingRight: 15 }}>
                  {user ? user : "Login"}
                </Text>
              </TouchableOpacity>
            ),
          })}
        >
          {(props) => <MoviesScreen {...props} user={user} />}
        </Stack.Screen>

        <Stack.Screen name="MovieProfile">
          {(props) => <MovieProfile {...props} user={user} userId={userId} />}
        </Stack.Screen>

        <Stack.Screen name="Login">
          {(props) => <LoginScreen {...props} setUser={setUser} setUserId={setUserId} />}
        </Stack.Screen>
      </Stack.Navigator>
    </NavigationContainer>
  );
}