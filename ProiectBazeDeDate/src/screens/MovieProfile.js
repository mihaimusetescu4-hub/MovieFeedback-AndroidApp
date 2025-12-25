import React, { useEffect, useState } from 'react';
import {
  View, Text, ScrollView, StyleSheet, ActivityIndicator,
  TextInput, TouchableOpacity, Alert, Modal
} from 'react-native';
import axios from 'axios';

const API_URL = 'http://10.0.2.2:8000/api/filme/';
const FEEDBACK_URL = 'http://10.0.2.2:8000/api/feedback/';

const FilmDetailScreen = ({ route, navigation, user, userId }) => {
  const { filmId } = route.params || {};

  const [film, setFilm] = useState(null);
  const [loading, setLoading] = useState(true);
  const [modalVisible, setModalVisible] = useState(false);

  const [titlu, setTitlu] = useState('');
  const [descriere, setDescriere] = useState('');
  const [rating, setRating] = useState('');

  const loadFilmDetails = async () => {
    try {
      const res = await axios.get(`${API_URL}${filmId}/`);
      setFilm(res.data);
    } catch (e) {
      console.log("Eroare la incarcare:", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadFilmDetails();
  }, [filmId]);

  const handlePlusPress = () => {
    if (user) {
      setModalVisible(true);
    } else {
      Alert.alert(
        "Autentificare",
        "Trebuie să fii logat pentru a lăsa o recenzie.",
        [
          { text: "Anulează", style: "cancel" },
          { text: "Login", onPress: () => navigation.navigate("Login") }
        ]
      );
    }
  };

  const handleTrimiteRecenzie = async () => {
    if (!titlu.trim() || !descriere.trim()) {
      Alert.alert("Eroare", "Completează titlul și descrierea!");
      return;
    }

    try {
      await axios.post(FEEDBACK_URL, {
        id_utilizator: userId,
        id_film: filmId,
        nume_comentariu: titlu,
        descriere_comentariu: descriere,
        rating_comentariu: parseFloat(rating) || 0,
      });

      Alert.alert("Succes", "Recenzia a fost adăugată!");
      setModalVisible(false);
      setTitlu(''); setDescriere(''); setRating('');
      loadFilmDetails(); 
    } catch (e) {
      Alert.alert("Eroare", "Nu s-a putut salva recenzia.");
    }
  };

  if (loading) return <View style={styles.center}><ActivityIndicator size="large" color="#007AFF" /></View>;

  return (
    <View style={{ flex: 1, backgroundColor: '#fff' }}>
      <ScrollView style={styles.container}>
        <Text style={styles.mainTitle}>{film?.nume_film}</Text>
        <Text style={styles.infoText}>Durata: {film?.durata} min | Rating: {film?.rating}/10</Text>

        <View style={styles.separator} />
        <Text style={styles.sectionTitle}>Detalii Producție</Text>
        <Text><Text style={styles.bold}>Regizor:</Text> {film?.regizor?.prenume_regizor} {film?.regizor?.nume_regizor}</Text>
        <Text><Text style={styles.bold}>Studio:</Text> {film?.studio?.nume_studio}</Text>

        <View style={styles.separator} />
        <Text style={styles.sectionTitle}>Distribuție</Text>
        {film?.actori?.map((a, i) => (
          <Text key={i}>• {a.prenume_actor} {a.nume_actor}</Text>
        ))}

        <View style={styles.separator} />
        <Text style={styles.sectionTitle}>Recenzii ({film?.feedback?.length || 0})</Text>
        {film?.feedback?.map((fb, i) => (
          <View key={i} style={styles.feedbackCard}>
            <Text style={styles.fbUser}>{fb.username}</Text>
            <Text style={styles.fbTitle}>{fb.nume_comentariu}</Text>
            <Text>{fb.descriere_comentariu}</Text>
            <Text style={styles.fbRating}>Nota: {fb.rating_comentariu}/10</Text>
          </View>
        ))}
        <View style={{ height: 80 }} />
      </ScrollView>

      {/* BUTONUL + CU REDIRECȚIONARE */}
      <TouchableOpacity style={styles.fab} onPress={handlePlusPress}>
        <Text style={styles.fabIcon}>+</Text>
      </TouchableOpacity>

      <Modal visible={modalVisible} animationType="slide" transparent={true}>
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <Text style={styles.modalHeader}>Adaugă Recenzie</Text>
            <TextInput style={styles.input} placeholder="Titlu" value={titlu} onChangeText={setTitlu} />
            <TextInput style={[styles.input, { height: 70 }]} placeholder="Părerea ta..." multiline value={descriere} onChangeText={setDescriere} />
            <TextInput style={styles.input} placeholder="Nota (1-10)" keyboardType="numeric" value={rating} onChangeText={setRating} />
            <View style={styles.modalActions}>
              <TouchableOpacity onPress={() => setModalVisible(false)}><Text style={{ color: 'red' }}>Anulează</Text></TouchableOpacity>
              <TouchableOpacity style={styles.sendBtn} onPress={handleTrimiteRecenzie}><Text style={{ color: '#fff' }}>Trimite</Text></TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { padding: 20 },
  center: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  mainTitle: { fontSize: 26, fontWeight: 'bold' },
  infoText: { fontSize: 14, color: '#666' },
  separator: { height: 1, backgroundColor: '#eee', marginVertical: 15 },
  sectionTitle: { fontSize: 18, fontWeight: 'bold', marginBottom: 5 },
  bold: { fontWeight: 'bold' },
  feedbackCard: { backgroundColor: '#f9f9f9', padding: 12, borderRadius: 8, marginBottom: 10, borderLeftWidth: 4, borderLeftColor: '#007AFF' },
  fbUser: { fontWeight: 'bold', color: '#007AFF' },
  fbTitle: { fontWeight: '700', marginVertical: 2 },
  fbRating: { fontSize: 11, color: '#999', marginTop: 5 },
  fab: { position: 'absolute', bottom: 25, right: 25, width: 60, height: 60, borderRadius: 30, backgroundColor: '#007AFF', justifyContent: 'center', alignItems: 'center', elevation: 5 },
  fabIcon: { fontSize: 30, color: '#fff', fontWeight: 'bold' },
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.5)', justifyContent: 'center', padding: 20 },
  modalContent: { backgroundColor: '#fff', borderRadius: 15, padding: 20 },
  modalHeader: { fontSize: 20, fontWeight: 'bold', marginBottom: 15, textAlign: 'center' },
  input: { borderBottomWidth: 1, borderColor: '#ddd', marginBottom: 15, padding: 8 },
  modalActions: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  sendBtn: { backgroundColor: '#007AFF', padding: 10, borderRadius: 8, paddingHorizontal: 20 }
});

export default FilmDetailScreen;