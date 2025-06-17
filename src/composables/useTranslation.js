import { computed } from 'vue'
import { useAppStore } from '../stores/app'

// Import translation files
import enTranslations from '../locales/en.json'
import viTranslations from '../locales/vi.json'

const translations = {
  en: enTranslations,
  vi: viTranslations
}

export function useTranslation() {
  const appStore = useAppStore()
  
  const t = (key) => {
    const currentLang = appStore.currentLanguage
    const keys = key.split('.')
    
    let translation = translations[currentLang] || translations.en
    
    for (const k of keys) {
      translation = translation?.[k]
      if (!translation) break
    }
    
    // Fallback to English if translation not found
    if (!translation && currentLang !== 'en') {
      translation = translations.en
      for (const k of keys) {
        translation = translation?.[k]
        if (!translation) break
      }
    }
    
    return translation || key
  }

  const locale = computed(() => appStore.currentLanguage)

  return {
    t,
    locale
  }
}