import { defineStore } from 'pinia'
import { ref } from 'vue'
import { api, authApi } from '../utils/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const isAuthenticated = ref(false)
  const loading = ref(false)

  const checkAuth = async () => {
    // Optionally, implement a /me endpoint to check session
    // For now, just check if user is set
    isAuthenticated.value = !!user.value
  }

  const login = async (email, password) => {
    loading.value = true
    try {
      const response = await authApi.post('/login', { email, password })
      const userData = response.data.user
      user.value = userData
      isAuthenticated.value = true
      return userData
    } catch (error) {
      throw error
    } finally {
      loading.value = false
    }
  }

  const register = async (username, email, password, confirmPassword) => {
    loading.value = true
    try {
      const response = await authApi.post('/register', { username, email, password, confirm_password: confirmPassword })
      const userData = response.data.user
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
      await authApi.post('/logout')
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
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
