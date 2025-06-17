<template>
  <div class="language-selector">
    <select 
      v-model="selectedLanguage" 
      @change="changeLanguage"
      class="form-select form-select-sm"
    >
      <option value="en">🇺🇸 English</option>
      <option value="vi">🇻🇳 Vietnamese</option>
    </select>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAppStore } from '../stores/app'

const appStore = useAppStore()
const selectedLanguage = ref('en')

const changeLanguage = () => {
  appStore.setLanguage(selectedLanguage.value)
  localStorage.setItem('preferredLanguage', selectedLanguage.value)
}

onMounted(() => {
  const savedLang = localStorage.getItem('preferredLanguage')
  if (savedLang) {
    selectedLanguage.value = savedLang
    appStore.setLanguage(savedLang)
  }
})
</script>

<style scoped>
.language-selector {
  position: absolute;
  top: 20px;
  right: 20px;
  z-index: 100;
}

.form-select {
  border: 2px solid #667eea;
  background: white;
  color: #333;
  font-size: 14px;
  cursor: pointer;
  outline: none;
  transition: border-color 0.3s;
}

.form-select:hover {
  border-color: #764ba2;
}

.form-select:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}
</style>
