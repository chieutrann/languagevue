import axios from 'axios'

// Create axios instance with base configuration
const api = axios.create({
  baseURL: process.env.NODE_ENV === 'production' ? '' : 'http://localhost:5000/api',
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
