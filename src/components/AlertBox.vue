<template>
  <Teleport to="body">
    <div v-if="appStore.alert" class="custom-alert-container">
      <div 
        class="custom-alert"
        :class="appStore.alert.type"
        role="alert"
      >
        <div class="alert-content">
          <i 
            class="fas"
            :class="getAlertIcon(appStore.alert.type)"
          ></i>
          <span class="ms-2">{{ appStore.alert.message }}</span>
        </div>
        <button 
          @click="appStore.hideAlert"
          type="button" 
          class="btn-close btn-close-sm"
          aria-label="Close"
        ></button>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { useAppStore } from '../stores/app'

const appStore = useAppStore()

const getAlertIcon = (type) => {
  const icons = {
    success: 'fa-check-circle',
    error: 'fa-exclamation-circle',
    warning: 'fa-exclamation-triangle',
    info: 'fa-info-circle'
  }
  return icons[type] || 'fa-info-circle'
}
</script>

<style scoped>
.custom-alert-container {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 9999;
  min-width: 300px;
  max-width: 80%;
}

.custom-alert {
  padding: 15px 20px;
  border-radius: 8px;
  margin-bottom: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
  animation: alertFadeInOut 5s forwards;
  background: white;
  border: 1px solid #ddd;
}

.custom-alert.success {
  background-color: #d4edda;
  border-color: #c3e6cb;
  color: #155724;
}

.custom-alert.error {
  background-color: #f8d7da;
  border-color: #f5c6cb;
  color: #721c24;
}

.custom-alert.warning {
  background-color: #fff3cd;
  border-color: #ffeeba;
  color: #856404;
}

.custom-alert.info {
  background-color: #cce5ff;
  border-color: #b8daff;
  color: #004085;
}

.alert-content {
  display: flex;
  align-items: center;
  flex: 1;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.2em;
  cursor: pointer;
  opacity: 0.7;
  margin-left: 1rem;
}

.btn-close:hover {
  opacity: 1;
}

@keyframes alertFadeInOut {
  0% { opacity: 0; transform: translateY(-20px); }
  10% { opacity: 1; transform: translateY(0); }
  90% { opacity: 1; transform: translateY(0); }
  100% { opacity: 0; transform: translateY(-20px); }
}
</style>
