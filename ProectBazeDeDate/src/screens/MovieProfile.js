// // src/screens/MovieProfile.js
// import React from 'react';
// import { View, Text, ScrollView, StyleSheet } from 'react-native';

// const FilmDetailScreen = ({ route }) => {
//   // 1. Extragem 'film' cu protecție în caz că params e gol
//   const { film } = route.params || {};

//   // 2. Dacă obiectul film nu există deloc, afișăm un mesaj de eroare general
//   if (!film) {
//     return (
//       <View style={[styles.container, { justifyContent: 'center', alignItems: 'center' }]}>
//         <Text style={{ color: 'red', fontSize: 18 }}>Eroare: Datele filmului nu au fost găsite.</Text>
//       </View>
//     );
//   }

//   return (
//     <ScrollView style={styles.container}>
//       {/* Titlu și info principal */}
//       <Text style={styles.title}>{film?.nume_film || "Titlu Indisponibil"}</Text>
      
//       <Text>
//         Durata: {film?.durata ? `${film.durata} min` : "-"} | 
//         Rating: {film?.rating || "N/A"}
//       </Text>
      
//       <View style={styles.separator} />

//       {/* Regizor si Studio */}
//       <Text style={styles.subtitle}>Detalii Producție</Text>
      
//       <Text>
//         Regizor: {film?.regizor?.prenume_regizor || ""} {film?.regizor?.nume_regizor || "Necunoscut"}
//       </Text>
      
//       <Text>
//         Studio: {film?.studio?.nume_studio || "Studio Necunoscut"}
//       </Text>

//       <View style={styles.separator} />

//       {/* Lista Actori */}
//       <Text style={styles.subtitle}>Distribuție</Text>
//       {/* Verificăm dacă există lista de actori și dacă are elemente */}
//       {film?.actori && film.actori.length > 0 ? (
//         film.actori.map((actor, index) => (
//           <Text key={actor?.id_actor || index}>
//             • {actor?.prenume_actor || ""} {actor?.nume_actor || "Actor Necunoscut"}
//           </Text>
//         ))
//       ) : (
//         <Text style={{ fontStyle: 'italic', color: '#666' }}>Nu există informații despre actori.</Text>
//       )}

//       <View style={styles.separator} />

//       {/* Lista Comentarii */}
//       <Text style={styles.subtitle}>
//         Recenzii ({film?.feedbackuri?.length || 0})
//       </Text>

//       {film?.feedbackuri && film.feedbackuri.length > 0 ? (
//         film.feedbackuri.map((feedback, index) => (
//           <View key={feedback?.id_feedback || index} style={styles.feedbackCard}>
//              {/* Protecție pt user, nume comentariu, rating */}
//              <Text style={{fontWeight: 'bold'}}>
//                {feedback?.utilizator?.username || "Utilizator Anonim"}
//              </Text>
             
//              <Text>
//                "{feedback?.nume_comentariu || "Fără titlu"}" - {feedback?.rating_comentariu || "?"}/10
//              </Text>
             
//              <Text>{feedback?.descriere_comentariu || "Fără descriere."}</Text>
//           </View>
//         ))
//       ) : (
//         <Text style={{ fontStyle: 'italic', color: '#666' }}>Nu există recenzii pentru acest film.</Text>
//       )}
//     </ScrollView>
//   );
// };

// const styles = StyleSheet.create({
//   container: { padding: 20, flex: 1 }, // flex: 1 ajută la layout
//   title: { fontSize: 24, fontWeight: 'bold', marginBottom: 10 },
//   subtitle: { fontSize: 18, fontWeight: 'bold', marginTop: 15, marginBottom: 5 },
//   separator: { height: 1, backgroundColor: '#ccc', marginVertical: 10 },
//   feedbackCard: { backgroundColor: '#f0f0f0', padding: 10, marginBottom: 10, borderRadius: 5 }
// });

// export default FilmDetailScreen;

// src/screens/MovieProfile.js
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
  // luam id-ul filmului si, optional, titlul din lista ca fallback
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

        // doar debug, poti comenta linia asta
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

  // loading
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

  // eroare
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

  // fallback final
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

  // EXACT layout-ul tau de mai sus, dar folosind film-ul încărcat
  return (
    <ScrollView style={styles.container}>
      {/* Titlu și info principal */}
      <Text style={styles.title}>
        {film?.nume_film || initialTitle || 'Titlu Indisponibil'}
      </Text>

      <Text>
        Durata: {film?.durata ? `${film.durata} min` : '-'} | Rating:{' '}
        {film?.rating || 'N/A'}
      </Text>

      <View style={styles.separator} />

      {/* Regizor si Studio */}
      <Text style={styles.subtitle}>Detalii Producție</Text>

      <Text>
        Regizor: {film?.regizor?.prenume_regizor || ''}{' '}
        {film?.regizor?.nume_regizor || 'Necunoscut'}
      </Text>

      <Text>
        Studio: {film?.studio?.nume_studio || 'Studio Necunoscut'}
      </Text>

      <View style={styles.separator} />

      {/* Lista Actori */}
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

      {/* Lista Comentarii */}
      <Text style={styles.subtitle}>
        Recenzii ({film?.feedbackuri?.length || 0})
      </Text>

      {film?.feedbackuri && film.feedbackuri.length > 0 ? (
        film.feedbackuri.map((feedback, index) => (
          <View
            key={feedback?.id_feedback || index}
            style={styles.feedbackCard}
          >
            <Text style={{ fontWeight: 'bold' }}>
              {feedback?.utilizator?.username || 'Utilizator Anonim'}
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
  container: { padding: 20, flex: 1 }, // flex: 1 ajută la layout
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
