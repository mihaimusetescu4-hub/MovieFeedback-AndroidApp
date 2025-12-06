// src/navigation/AppNavigator.js
import React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

import MoviesScreen from "../screens/MovieScreen";
import MovieProfile from "../screens/MovieProfile";

const Stack = createNativeStackNavigator();

export default function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Movies" component={MoviesScreen} />
        <Stack.Screen name="MovieProfile" component={MovieProfile} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
