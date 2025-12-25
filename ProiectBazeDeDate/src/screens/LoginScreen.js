import React, { useState } from 'react';
import {
  StyleSheet,
  View,
  Text,
  TextInput,
  TouchableOpacity,
  Alert,
  ActivityIndicator
} from 'react-native';

// 1. AICI ERA GREȘEALA: Trebuie să adaugi setUserId în paranteze!
const LoginScreen = ({ navigation, setUser, setUserId }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);

  const handleAuth = async () => {
    if (!username || !password) {
      Alert.alert("Eroare", "Introdu username și parola.");
      return;
    }

    setLoading(true);
    const API_URL = 'http://10.0.2.2:8000/api/utilizatori/';

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(isLogin ? { username, parola: password } : { username, email, parola: password, varsta: 20 }),
      });

      const data = await response.json();

      // 2. DEBUG: Vedem exact ce primim de la server
      console.log("====================================");
      console.log("LOGIN DATA:", JSON.stringify(data, null, 2));
      console.log("====================================");

      if (response.ok) {
        // PASUL 1: Salvăm datele
        setUser(data.username);

        // 3. Aici facem salvarea ID-ului.
        // Verificăm în consolă dacă câmpul se numește "id_utilizator", "id" sau "pk"
        // și folosim varianta corectă:
        if (setUserId) {
             // Dacă în consolă vezi "id": 5, schimbă mai jos în data.id
             setUserId(data.id_utilizator); 
             console.log("ID SALVAT:", data.id_utilizator);
        }

        // PASUL 2: Navigăm
        navigation.navigate("Movies");
      } else {
        Alert.alert("Eroare", data.error || "Date incorecte.");
      }
    } catch (error) {
      console.log("LOGIN ERROR:", error);
      Alert.alert("Eroare", "Conexiunea a eșuat. Verifică serverul.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>{isLogin ? 'Login' : 'Inregistrare'}</Text>

      <TextInput
        style={styles.input}
        placeholder="Username"
        value={username}
        onChangeText={setUsername}
        autoCapitalize="none"
      />

      {!isLogin && (
        <TextInput
          style={styles.input}
          placeholder="Email"
          value={email}
          onChangeText={setEmail}
          keyboardType="email-address"
          autoCapitalize="none"
        />
      )}

      <TextInput
        style={styles.input}
        placeholder="Parola"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />

      <TouchableOpacity
        style={[styles.button, loading && { backgroundColor: '#ccc' }]}
        onPress={handleAuth}
        disabled={loading}
      >
        {loading ? (
          <ActivityIndicator color="#fff" />
        ) : (
          <Text style={styles.buttonText}>{isLogin ? 'Intra in cont' : 'Creeaza cont'}</Text>
        )}
      </TouchableOpacity>

      <TouchableOpacity onPress={() => setIsLogin(!isLogin)} style={styles.switchContainer}>
        <Text style={styles.switchText}>
          {isLogin ? 'Nu ai cont? Inregistreaza-te' : 'Ai deja cont? Logheaza-te'}
        </Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', padding: 20, backgroundColor: '#f5f5f5' },
  title: { fontSize: 28, fontWeight: 'bold', marginBottom: 30, textAlign: 'center', color: '#333' },
  input: { backgroundColor: '#fff', padding: 15, borderRadius: 10, marginBottom: 15, borderWidth: 1, borderColor: '#ddd' },
  button: { backgroundColor: '#007AFF', padding: 15, borderRadius: 10, alignItems: 'center', marginTop: 10 },
  buttonText: { color: '#fff', fontWeight: 'bold', fontSize: 16 },
  switchContainer: { marginTop: 20 },
  switchText: { color: '#007AFF', textAlign: 'center', fontSize: 14 }
});

export default LoginScreen;