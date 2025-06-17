<template>
  <div id="app">
    <div class="main-container">
      <LanguageSelector />
      
      <header class="text-center py-4 border-bottom mb-4" style="border-color: #667eea !important; border-width: 3px !important;">
        <h1 class="text-primary mb-3" style="color: #667eea !important; font-size: 2.5em;">
          🇩🇪 German Learning App
        </h1>
        <p class="subtitle text-muted" style="font-size: 1.2em;">
          Learn German through current events
        </p>
        
        <div class="auth-section mt-3" v-if="authStore.isAuthenticated">
          <span class="welcome-text me-3">{{ t('auth.welcome') }}, {{ authStore.user?.email || 'User' }}!</span>
          <button @click="logout" class="btn btn-outline-danger btn-sm">{{ t('auth.logout') }}</button>
        </div>
        <div class="auth-section mt-3" v-else>
          <router-link to="/auth" class="btn btn-outline-primary btn-sm me-2">{{ t('auth.login') }}</router-link>
          <router-link to="/auth" class="btn btn-primary btn-sm">{{ t('auth.register') }}</router-link>
        </div>
      </header>

      <NavigationTabs />
      
      <AlertBox />
      
      <main class="mt-4">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from './stores/auth'
import NavigationTabs from './components/NavigationTabs.vue'
import LanguageSelector from './components/LanguageSelector.vue'
import AlertBox from './components/AlertBox.vue'

const authStore = useAuthStore()

const logout = async () => {
  await authStore.logout()
}

onMounted(() => {
  authStore.checkAuth()
})
</script>
