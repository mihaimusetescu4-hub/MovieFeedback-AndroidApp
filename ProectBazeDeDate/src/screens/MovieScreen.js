// src/screens/MoviesScreen.js
import React, { useEffect, useState, useCallback } from "react";
import {
  View,
  Text,
  FlatList,
  ActivityIndicator,
  RefreshControl,
  TextInput,
  TouchableOpacity,
} from "react-native";
import axios from "axios";

const API_URL = "http://10.0.2.2:8000/api/filme/";

export default function MoviesScreen({ navigation }) {
  const [data, setData] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState("");
  const [q, setQ] = useState("");

  const load = useCallback(async () => {
    try {
      setError("");
      const res = await axios.get(API_URL);
      const items = Array.isArray(res.data)
        ? res.data
        : res.data.results || [];
      setData(items);
      setFiltered(items);
    } catch (e) {
      console.log("ERR", e.message);
      setError("Nu pot incarca filmele.");
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  useEffect(() => {
    const s = q.toLowerCase();
    if (!s) {
      setFiltered(data);
      return;
    }
    setFiltered(
      data.filter((it) => {
        const title = String(it.nume_film || "").toLowerCase();
        const year = String(it.an_aparitie || "");
        return title.includes(s) || year.includes(s);
      })
    );
  }, [q, data]);

  if (loading) {
    return (
      <View style={{ flex: 1, alignItems: "center", justifyContent: "center" }}>
        <ActivityIndicator size="large" />
        <Text style={{ marginTop: 8 }}>Se incarca...</Text>
      </View>
    );
  }

  return (
    <View style={{ flex: 1, padding: 16, gap: 12 }}>
      <Text style={{ fontSize: 22, fontWeight: "700", marginBottom: 6 }}>
        Filme
      </Text>

      <TextInput
        placeholder="Cauta film..."
        value={q}
        onChangeText={setQ}
        style={{
          borderWidth: 1,
          borderColor: "#ddd",
          borderRadius: 10,
          paddingHorizontal: 12,
          height: 40,
          marginBottom: 8,
          backgroundColor: "white",
        }}
      />

      {error ? (
        <View
          style={{
            backgroundColor: "#fee",
            borderRadius: 10,
            padding: 10,
            marginBottom: 8,
          }}
        >
          <Text style={{ color: "#900" }}>{error}</Text>
        </View>
      ) : null}

      <FlatList
        data={filtered}
        keyExtractor={(item, index) =>
          String(item.id_film || item.id || index)
        }
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={() => {
              setRefreshing(true);
              load();
            }}
          />
        }
        ItemSeparatorComponent={() => <View style={{ height: 8 }} />}
        renderItem={({ item }) => (
          <View
            style={{
              backgroundColor: "white",
              borderRadius: 14,
              padding: 14,
              elevation: 2,
              shadowColor: "#000",
              shadowOpacity: 0.1,
              shadowRadius: 6,
            }}
          >
            <Text style={{ fontSize: 16, fontWeight: "700" }}>
              {item.nume_film || "-"}
            </Text>
            <Text style={{ marginTop: 4 }}>
              An: {item.an_aparitie ?? "—"} • Durata: {item.durata ?? "—"} min
            </Text>
            <Text style={{ marginTop: 4 }}>
              Rating: {item.rating ?? "—"} • Varsta:{" "}
              {item.varsta_necesara ?? "—"}
            </Text>
            <TouchableOpacity
              onPress={() =>
                navigation.navigate('MovieProfile', {
                  filmId: item.id_film,
                  initialTitle: item.nume_film, // optional
                })
              }
              style={{ marginTop: 8 }}
            >
              <Text style={{ color: "#06f" }}>Detalii</Text>
            </TouchableOpacity>
          </View>
        )}
        ListEmptyComponent={<Text>Nu exista filme.</Text>}
      />
    </View>
  );
}
