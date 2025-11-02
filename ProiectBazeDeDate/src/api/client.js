import axios from 'axios';

// IMPORTANT: Pentru emulatorul Android, 'localhost' este accesat prin IP-ul '10.0.2.2'
const apiClient = axios.create({
  baseURL: 'http://10.0.2.2:8000/api',
});


export default apiClient;