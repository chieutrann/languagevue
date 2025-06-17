<template>
  <div class="german-chars">
    <button 
      v-for="char in germanChars"
      :key="char"
      type="button" 
      @click="insertChar(char)"
      class="char-btn"
      :title="`Insert ${char}`"
    >
      {{ char }}
    </button>
    <button 
      type="button" 
      @click="toggleSearchDirection" 
      class="direction-btn" 
      title="Toggle search direction"
    >
      🔄
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  targetInput: {
    type: String,
    default: ''
  }
})

const germanChars = ['ä', 'ö', 'ü', 'ß']
const isReverseSearch = ref(false)

const insertChar = (char) => {
  let targetElement = null
  
  if (props.targetInput) {
    targetElement = document.getElementById(props.targetInput)
  }
  
  if (!targetElement) {
    // Find the closest input element
    const container = document.querySelector('.german-chars').closest('.input-wrapper') || 
                     document.querySelector('.german-chars').closest('.form-group') ||
                     document.querySelector('.german-chars').closest('.search-box')
    
    if (container) {
      targetElement = container.querySelector('input[type="text"]') || 
                     container.querySelector('input') ||
                     container.querySelector('textarea')
    }
  }
  
  if (targetElement) {
    const start = targetElement.selectionStart
    const end = targetElement.selectionEnd
    const value = targetElement.value
    
    const newValue = value.substring(0, start) + char + value.substring(end)
    targetElement.value = newValue
    
    // Trigger input event for Vue reactivity
    const event = new Event('input', { bubbles: true })
    targetElement.dispatchEvent(event)
    
    // Set cursor position after inserted character
    targetElement.focus()
    targetElement.selectionStart = targetElement.selectionEnd = start + 1
  }
}

const toggleSearchDirection = () => {
  isReverseSearch.value = !isReverseSearch.value
  // You can emit an event here if needed for parent components
}
</script>

<style scoped>
.german-chars {
  position: absolute;
  top: -35px;
  right: 0;
  display: flex;
  gap: 4px;
  z-index: 10;
}

.char-btn, .direction-btn {
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  color: #495057;
  padding: 4px 8px;
  font-size: 0.875em;
  min-width: 28px;
  height: 28px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.char-btn:hover, .direction-btn:hover {
  background: #667eea;
  color: white;
  border-color: #667eea;
  transform: translateY(-1px);
}

.char-btn:active, .direction-btn:active {
  transform: translateY(0);
}

.direction-btn {
  font-size: 0.75em;
}

/* Responsive positioning */
@media (max-width: 768px) {
  .german-chars {
    position: static;
    justify-content: center;
    margin-top: 8px;
    margin-bottom: 8px;
  }
}
</style>
