import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
  const currentLanguage = ref('en')
  const alert = ref(null)

  const setLanguage = (lang) => {
    currentLanguage.value = lang
  }

  const showAlert = (message, type = 'info') => {
    alert.value = { message, type }
    
    // Auto-hide alert after 5 seconds
    setTimeout(() => {
      hideAlert()
    }, 5000)
  }

  const hideAlert = () => {
    alert.value = null
  }

  return {
    currentLanguage,
    alert,
    setLanguage,
    showAlert,
    hideAlert
  }
})
