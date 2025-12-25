import React, { useState } from "react";
import { StatusBar, SafeAreaView } from "react-native";
import AppNavigator from "./src/navigation/AppNavigator";

export default function App() {
  const [user, setUser] = useState<string | null>(null);
  const [userId, setUserId] = useState<number | null>(null); // Adăugăm ID-ul utilizatorului

  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: "#f6f6f6" }}>
      <StatusBar barStyle="dark-content" />
      {/* Pasăm totul către navigator */}
      <AppNavigator 
        user={user} 
        setUser={setUser} 
        userId={userId} 
        setUserId={setUserId} 
      />
    </SafeAreaView>
  );
}