import { defineStore } from 'pinia'
import { ref } from 'vue'
import { api } from '../utils/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const isAuthenticated = ref(false)
  const loading = ref(false)

  const checkAuth = async () => {
    const token = localStorage.getItem('authToken')
    const userData = localStorage.getItem('userData')
    
    if (token && userData) {
      try {
        user.value = JSON.parse(userData)
        isAuthenticated.value = true
      } catch (error) {
        logout()
      }
    }
  }

  const login = async (email, password) => {
    loading.value = true
    
    try {
      const response = await api.post('/api/login', { email, password })
      const { token, user: userData } = response.data
      
      localStorage.setItem('authToken', token)
      localStorage.setItem('userData', JSON.stringify(userData))
      
      user.value = userData
      isAuthenticated.value = true
      
      return userData
    } catch (error) {
      throw error
    } finally {
      loading.value = false
    }
  }

  const register = async (username, email, password) => {
    loading.value = true
    
    try {
      const response = await api.post('/api/register', { username, email, password })
      const { token, user: userData } = response.data
      
      localStorage.setItem('authToken', token)
      localStorage.setItem('userData', JSON.stringify(userData))
      
      user.value = userData
      isAuthenticated.value = true
      
      return userData
    } catch (error) {
      throw error
    } finally {
      loading.value = false
    }
  }

  const googleSignIn = async () => {
    // This would integrate with Firebase Auth or other Google Sign-In service
    throw new Error('Google Sign-In not implemented yet')
  }

  const logout = async () => {
    try {
      await api.post('/api/logout')
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      localStorage.removeItem('authToken')
      localStorage.removeItem('userData')
      user.value = null
      isAuthenticated.value = false
    }
  }

  return {
    user,
    isAuthenticated,
    loading,
    checkAuth,
    login,
    register,
    googleSignIn,
    logout
  }
})
