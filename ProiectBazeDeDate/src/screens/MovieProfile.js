// src/screens/MovieProfile.js
import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  ActivityIndicator,
} from 'react-native';
import axios from 'axios';

const API_URL = 'http://10.0.2.2:8000/api/filme/';

const FilmDetailScreen = ({ route }) => {
  const { filmId, initialTitle } = route.params || {};

  const [film, setFilm] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const load = async () => {
      try {
        setError('');
        setLoading(true);

        if (!filmId) {
          setError('Nu am primit ID-ul filmului.');
          setLoading(false);
          return;
        }

        const res = await axios.get(`${API_URL}${filmId}/`);
        setFilm(res.data);

        console.log('DETALIU FILM:', JSON.stringify(res.data, null, 2));
      } catch (e) {
        console.log('ERR detaliu film:', e.message);
        setError('Nu pot încărca detaliile filmului.');
      } finally {
        setLoading(false);
      }
    };

    load();
  }, [filmId]);

  if (loading) {
    return (
      <View
        style={[
          styles.container,
          { justifyContent: 'center', alignItems: 'center' },
        ]}
      >
        <ActivityIndicator size="large" />
        <Text style={{ marginTop: 8 }}>Se încarcă detaliile filmului...</Text>
      </View>
    );
  }

  if (error) {
    return (
      <View
        style={[
          styles.container,
          { justifyContent: 'center', alignItems: 'center' },
        ]}
      >
        <Text style={{ color: 'red' }}>{error}</Text>
      </View>
    );
  }

  if (!film) {
    return (
      <View
        style={[
          styles.container,
          { justifyContent: 'center', alignItems: 'center' },
        ]}
      >
        <Text style={{ color: 'red', fontSize: 18 }}>
          Eroare: Datele filmului nu au fost găsite.
        </Text>
      </View>
    );
  }

  const feedbackuri = film.feedback || film.recenzii || [];

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>
        {film?.nume_film || initialTitle || 'Titlu Indisponibil'}
      </Text>

      <Text>
        Durata: {film?.durata ? `${film.durata} min` : '-'} | Rating:{' '}
        {film?.rating || 'N/A'}
      </Text>

      <View style={styles.separator} />

      <Text style={styles.subtitle}>Detalii Producție</Text>

      <Text>
        Regizor: {film?.regizor?.prenume_regizor || ''}{' '}
        {film?.regizor?.nume_regizor || 'Necunoscut'}
      </Text>

      <Text>
        Studio: {film?.studio?.nume_studio || 'Studio Necunoscut'}
      </Text>

      <View style={styles.separator} />

      <Text style={styles.subtitle}>Distribuție</Text>
      {film?.actori && film.actori.length > 0 ? (
        film.actori.map((actor, index) => (
          <Text key={actor?.id_actor || index}>
            • {actor?.prenume_actor || ''}{' '}
            {actor?.nume_actor || 'Actor Necunoscut'}
          </Text>
        ))
      ) : (
        <Text style={{ fontStyle: 'italic', color: '#666' }}>
          Nu există informații despre actori.
        </Text>
      )}

      <View style={styles.separator} />

      <Text style={styles.subtitle}>
        Recenzii ({feedbackuri.length})
      </Text>

      {feedbackuri.length > 0 ? (
        feedbackuri.map((feedback, index) => (
          <View
            key={feedback?.id_feedback || index}
            style={styles.feedbackCard}
          >
            <Text style={{ fontWeight: 'bold' }}>
              {feedback?.username || 'Utilizator Anonim'}
            </Text>

            <Text>
              "{feedback?.nume_comentariu || 'Fără titlu'}" -{' '}
              {feedback?.rating_comentariu || '?'}
              /10
            </Text>

            <Text>
              {feedback?.descriere_comentariu || 'Fără descriere.'}
            </Text>
          </View>
        ))
      ) : (
        <Text style={{ fontStyle: 'italic', color: '#666' }}>
          Nu există recenzii pentru acest film.
        </Text>
      )}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: { padding: 20, flex: 1 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 10 },
  subtitle: { fontSize: 18, fontWeight: 'bold', marginTop: 15, marginBottom: 5 },
  separator: { height: 1, backgroundColor: '#ccc', marginVertical: 10 },
  feedbackCard: {
    backgroundColor: '#f0f0f0',
    padding: 10,
    marginBottom: 10,
    borderRadius: 5,
  },
});

export default FilmDetailScreen;
