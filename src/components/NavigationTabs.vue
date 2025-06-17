<template>
  <nav class="navigation-tabs">
    <div class="nav-tabs-container">
      <router-link 
        v-for="tab in tabs" 
        :key="tab.name"
        :to="tab.path"
        class="nav-tab"
        :class="{ active: $route.name === tab.name }"
      >
        {{ t(tab.labelKey) }}
      </router-link>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useTranslation } from '../composables/useTranslation'

const route = useRoute()
const { t } = useTranslation()

const tabs = [
  { name: 'Home', path: '/', labelKey: 'nav.news' },
  { name: 'Vocabulary', path: '/vocabulary', labelKey: 'nav.vocabulary' },
  { name: 'Dictionary', path: '/dictionary', labelKey: 'nav.dictionary' },
  { name: 'Folders', path: '/folders', labelKey: 'nav.folders' }
]
</script>

<style scoped>
.navigation-tabs {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 5px;
  margin-bottom: 30px;
}

.nav-tabs-container {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.nav-tab {
  color: #667eea;
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 5px;
  transition: all 0.3s;
  font-family: 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji', 'Apple Color Emoji', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  font-weight: 500;
}

.nav-tab:hover {
  background: #667eea;
  color: white;
  transform: translateY(-1px);
}

.nav-tab.active {
  background: #667eea;
  color: white;
  box-shadow: 0 2px 4px rgba(102, 126, 234, 0.3);
}

@media (max-width: 768px) {
  .nav-tabs-container {
    justify-content: center;
  }
  
  .nav-tab {
    flex: 1;
    text-align: center;
    min-width: 120px;
  }
}
</style>
