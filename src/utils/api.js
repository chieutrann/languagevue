import axios from 'axios'

// Create axios instance with base configuration
// We'll try to connect to the primary port (5000) first, and if it fails, 
// the error handler will switch to the fallback port (5001)
const BASE_API_URL = 'http://localhost:5000/api';
const FALLBACK_API_URL = 'http://localhost:5001/api';

let currentBaseUrl = BASE_API_URL;

const api = axios.create({
  baseURL: process.env.NODE_ENV === 'production' ? '' : currentBaseUrl,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response?.status === 401) {
      // Clear auth data and redirect to login
      localStorage.removeItem('authToken')
      localStorage.removeItem('userData')
      window.location.href = '/auth'
    }
    
    // Handle connection errors by trying the fallback URL
    if (!error.response && error.code === 'ERR_NETWORK' && api.defaults.baseURL === BASE_API_URL) {
      console.log('Network error with primary API URL, trying fallback...')
      // Switch to fallback URL
      api.defaults.baseURL = FALLBACK_API_URL
      // Retry the original request with the new baseURL
      const originalRequest = error.config
      return api(originalRequest)
    }
    
    return Promise.reject(error)
  }
)

//Get word function from dictionary
export const getWord = async (word, src_lang = 'de', lang_dest = 'en') => {
  try {
    const response = await api.post('/dictionary/get-word', { word, src_lang, lang_dest })
    return response.data
  } catch (error) {
    console.error('Error fetching word:', error)
    throw error
  }
}




// Export the configured axios instance 


export { api }
