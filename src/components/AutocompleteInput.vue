<template>
  <div class="autocomplete-container">
    <input 
      ref="inputRef"
      type="text"
      class="form-control"
      :placeholder="placeholder"
      v-model="inputValue"
      @input="handleInput"
      @keydown="handleKeydown"
      @blur="handleBlur"
      @focus="handleFocus"
    >
    
    <div 
      v-if="showSuggestions && filteredSuggestions.length > 0"
      class="suggestions-dropdown"
    >
      <div 
        v-for="(suggestion, index) in filteredSuggestions"
        :key="index"
        class="suggestion-item"
        :class="{ active: index === selectedIndex }"
        @mousedown="selectSuggestion(suggestion)"
        @mouseenter="selectedIndex = index"
      >
        <div class="suggestion-content">
          <span class="suggestion-word">{{ suggestion.word || suggestion }}</span>
          <span v-if="suggestion.type" class="suggestion-type">{{ suggestion.type }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: 'Type to search...'
  },
  suggestions: {
    type: Array,
    default: () => []
  },
  minLength: {
    type: Number,
    default: 2
  }
})

const emit = defineEmits(['update:modelValue', 'search', 'input'])

const inputRef = ref(null)
const inputValue = ref(props.modelValue)
const showSuggestions = ref(false)
const selectedIndex = ref(-1)

const filteredSuggestions = computed(() => {
  if (!inputValue.value || inputValue.value.length < props.minLength) {
    return []
  }
  
  return props.suggestions.slice(0, 10) // Limit to 10 suggestions
})

watch(() => props.modelValue, (newValue) => {
  inputValue.value = newValue
})

watch(inputValue, (newValue) => {
  emit('update:modelValue', newValue)
})

const handleInput = (event) => {
  const value = event.target.value
  inputValue.value = value
  selectedIndex.value = -1
  
  if (value.length >= props.minLength) {
    showSuggestions.value = true
    emit('input', value)
  } else {
    showSuggestions.value = false
  }
}

const handleKeydown = (event) => {
  if (!showSuggestions.value || filteredSuggestions.value.length === 0) {
    if (event.key === 'Enter') {
      event.preventDefault()
      emit('search', inputValue.value)
    }
    return
  }
  
  switch (event.key) {
    case 'ArrowDown':
      event.preventDefault()
      selectedIndex.value = Math.min(
        selectedIndex.value + 1,
        filteredSuggestions.value.length - 1
      )
      break
      
    case 'ArrowUp':
      event.preventDefault()
      selectedIndex.value = Math.max(selectedIndex.value - 1, -1)
      break
      
    case 'Enter':
      event.preventDefault()
      if (selectedIndex.value >= 0) {
        selectSuggestion(filteredSuggestions.value[selectedIndex.value])
      } else {
        emit('search', inputValue.value)
      }
      break
      
    case 'Escape':
      showSuggestions.value = false
      selectedIndex.value = -1
      inputRef.value?.blur()
      break
  }
}

const handleFocus = () => {
  if (inputValue.value.length >= props.minLength && filteredSuggestions.value.length > 0) {
    showSuggestions.value = true
  }
}

const handleBlur = () => {
  // Delay hiding suggestions to allow for click events
  setTimeout(() => {
    showSuggestions.value = false
    selectedIndex.value = -1
  }, 150)
}

const selectSuggestion = (suggestion) => {
  const value = suggestion.word || suggestion
  inputValue.value = value
  showSuggestions.value = false
  selectedIndex.value = -1
  
  nextTick(() => {
    emit('search', value)
  })
}
</script>

<style scoped>
.autocomplete-container {
  position: relative;
  width: 100%;
}

.suggestions-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  max-height: 200px;
  overflow-y: auto;
  background: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  z-index: 1000;
  margin-top: 2px;
}

.suggestion-item {
  padding: 8px 12px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #eee;
  transition: background-color 0.2s;
}

.suggestion-item:last-child {
  border-bottom: none;
}

.suggestion-item:hover,
.suggestion-item.active {
  background-color: #f5f5f5;
}

.suggestion-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.suggestion-word {
  font-weight: 500;
}

.suggestion-type {
  color: #666;
  font-size: 0.9em;
  margin-left: 8px;
}
</style>
