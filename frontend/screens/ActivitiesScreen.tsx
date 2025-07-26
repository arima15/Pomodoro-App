import React, { useEffect, useState } from 'react';
import { View, Text, TextInput, Button, FlatList, StyleSheet, Alert } from 'react-native';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { API_BASE_URL } from '../api';

// Define Activity type
interface Activity {
  id: number;
  name: string;
  color?: string;
}

export default function ActivitiesScreen() {
  const [activities, setActivities] = useState<Activity[]>([]);
  const [name, setName] = useState('');
  const [color, setColor] = useState('');
  const [loading, setLoading] = useState(false);

  // Fetch activities from backend
  const fetchActivities = async () => {
    setLoading(true);
    try {
      const token = await AsyncStorage.getItem('access_token');
      const response = await axios.get(`${API_BASE_URL}/activities`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setActivities(response.data);
    } catch (error: any) {
      Alert.alert('Error', error?.response?.data?.msg || 'Failed to fetch activities');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchActivities();
  }, []);

  // Add a new activity
  const addActivity = async () => {
    if (!name) {
      Alert.alert('Validation', 'Activity name is required');
      return;
    }
    setLoading(true);
    try {
      const token = await AsyncStorage.getItem('access_token');
      await axios.post(
        `${API_BASE_URL}/activities`,
        { name, color },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setName('');
      setColor('');
      fetchActivities();
    } catch (error: any) {
      Alert.alert('Error', error?.response?.data?.msg || 'Failed to add activity');
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Your Activities</Text>
      <FlatList
        data={activities}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <View style={styles.activityItem}>
            <Text>{item.name} {item.color ? `(${item.color})` : ''}</Text>
          </View>
        )}
        refreshing={loading}
        onRefresh={fetchActivities}
        ListEmptyComponent={<Text>No activities found.</Text>}
      />
      <Text style={styles.subtitle}>Add Activity</Text>
      <TextInput
        style={styles.input}
        placeholder="Activity Name"
        value={name}
        onChangeText={setName}
      />
      <TextInput
        style={styles.input}
        placeholder="Color (optional)"
        value={color}
        onChangeText={setColor}
      />
      <Button title={loading ? 'Adding...' : 'Add Activity'} onPress={addActivity} disabled={loading} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    marginBottom: 16,
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 18,
    marginTop: 24,
    marginBottom: 8,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 4,
    padding: 8,
    marginBottom: 12,
  },
  activityItem: {
    padding: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
}); 