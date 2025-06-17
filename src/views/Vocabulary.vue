<template>
  <div class="vocabulary-section">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>📚 Vocabulary List</h2>
      <button @click="showAddForm = true" class="btn btn-primary">
        <i class="fas fa-plus me-2"></i>Add New Word
      </button>
    </div>

    <!-- Add/Edit Form Modal -->
    <div v-if="showAddForm || editingWord" class="modal d-block" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              {{ editingWord ? 'Edit Word' : 'Add New Word' }}
            </h5>
            <button @click="closeForm" type="button" class="btn-close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveWord">
              <div class="mb-3">
                <label for="german" class="form-label">German Word</label>
                <div class="position-relative">
                  <input 
                    type="text" 
                    class="form-control" 
                    id="german" 
                    v-model="wordForm.german"
                    :class="{ 'is-invalid': formErrors.german }"
                    required
                  >
                  <GermanCharacterHelper target-input="german" />
                </div>
                <div v-if="formErrors.german" class="invalid-feedback">
                  {{ formErrors.german }}
                </div>
              </div>
              
              <div class="mb-3">
                <label for="english" class="form-label">English Translation</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="english" 
                  v-model="wordForm.english"
                  :class="{ 'is-invalid': formErrors.english }"
                  required
                >
                <div v-if="formErrors.english" class="invalid-feedback">
                  {{ formErrors.english }}
                </div>
              </div>
              
              <div class="mb-3">
                <label for="wordType" class="form-label">Word Type</label>
                <select 
                  class="form-select" 
                  id="wordType" 
                  v-model="wordForm.word_type"
                >
                  <option value="">Select type...</option>
                  <option value="noun">Noun</option>
                  <option value="verb">Verb</option>
                  <option value="adjective">Adjective</option>
                  <option value="adverb">Adverb</option>
                  <option value="preposition">Preposition</option>
                </select>
              </div>
              
              <div class="mb-3">
                <label for="difficulty" class="form-label">Difficulty</label>
                <select 
                  class="form-select" 
                  id="difficulty" 
                  v-model="wordForm.difficulty"
                >
                  <option value="">Select difficulty...</option>
                  <option value="beginner">Beginner</option>
                  <option value="intermediate">Intermediate</option>
                  <option value="advanced">Advanced</option>
                </select>
              </div>
              
              <div class="mb-3">
                <label for="notes" class="form-label">Notes (Optional)</label>
                <textarea 
                  class="form-control" 
                  id="notes" 
                  v-model="wordForm.notes"
                  rows="3"
                ></textarea>
              </div>
              
              <div class="d-flex justify-content-end gap-2">
                <button @click="closeForm" type="button" class="btn btn-secondary">Cancel</button>
                <button type="submit" class="btn btn-primary" :disabled="saveLoading">
                  <span v-if="saveLoading" class="spinner-border spinner-border-sm me-2"></span>
                  {{ saveLoading ? 'Saving...' : 'Save Word' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Search and Filter -->
    <div class="row mb-4">
      <div class="col-md-6">
        <div class="input-group">
          <input 
            type="text" 
            class="form-control" 
            placeholder="Search vocabulary..." 
            v-model="searchQuery"
            @input="debouncedSearch"
          >
          <button class="btn btn-outline-secondary" @click="clearSearch">
            <i class="fas fa-times"></i>
          </button>
        </div>
      </div>
      <div class="col-md-6">
        <div class="d-flex gap-2">
          <select v-model="filterType" class="form-select" @change="filterVocabulary">
            <option value="">All Types</option>
            <option value="noun">Nouns</option>
            <option value="verb">Verbs</option>
            <option value="adjective">Adjectives</option>
            <option value="adverb">Adverbs</option>
          </select>
          <select v-model="filterDifficulty" class="form-select" @change="filterVocabulary">
            <option value="">All Difficulties</option>
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Vocabulary List -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-2">Loading vocabulary...</p>
    </div>
    
    <div v-else-if="filteredVocabulary.length === 0" class="text-center py-5">
      <i class="fas fa-book fa-3x text-muted mb-3"></i>
      <h5>No vocabulary words found</h5>
      <p class="text-muted">
        {{ searchQuery || filterType || filterDifficulty ? 'Try adjusting your search or filters.' : 'Start building your vocabulary by adding new words.' }}
      </p>
    </div>
    
    <div v-else class="vocabulary-list">
      <div v-for="(word, index) in filteredVocabulary" :key="word.id" class="vocabulary-item mb-3">
        <div class="card">
          <div class="card-body">
            <div class="row align-items-center">
              <div class="col-md-3">
                <div class="vocabulary-number">{{ index + 1 }}</div>
                <h6 class="card-title mb-1">{{ word.german }}</h6>
                <small class="text-muted">{{ word.word_type }}</small>
              </div>
              <div class="col-md-4">
                <p class="card-text mb-1">{{ word.english }}</p>
                <span 
                  v-if="word.difficulty" 
                  :class="`badge difficulty-${word.difficulty}`"
                >
                  {{ word.difficulty }}
                </span>
              </div>
              <div class="col-md-3">
                <small class="text-muted" v-if="word.notes">{{ word.notes }}</small>
                <small class="text-muted" v-if="word.created_at">
                  Added: {{ formatDate(word.created_at) }}
                </small>
              </div>
              <div class="col-md-2 text-end">
                <div class="btn-group">
                  <button 
                    @click="playAudio(word.german)" 
                    class="btn btn-sm btn-outline-primary"
                    title="Play pronunciation"
                  >
                    <i class="fas fa-volume-up"></i>
                  </button>
                  <button 
                    @click="editWord(word)" 
                    class="btn btn-sm btn-outline-secondary"
                    title="Edit word"
                  >
                    <i class="fas fa-edit"></i>
                  </button>
                  <button 
                    @click="confirmDelete(word)" 
                    class="btn btn-sm btn-outline-danger"
                    title="Delete word"
                  >
                    <i class="fas fa-trash"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <nav v-if="totalPages > 1" class="mt-4">
      <ul class="pagination justify-content-center">
        <li class="page-item" :class="{ disabled: currentPage === 1 }">
          <button class="page-link" @click="changePage(currentPage - 1)">Previous</button>
        </li>
        <li 
          v-for="page in visiblePages" 
          :key="page" 
          class="page-item" 
          :class="{ active: page === currentPage }"
        >
          <button class="page-link" @click="changePage(page)">{{ page }}</button>
        </li>
        <li class="page-item" :class="{ disabled: currentPage === totalPages }">
          <button class="page-link" @click="changePage(currentPage + 1)">Next</button>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useAppStore } from '../stores/app'
import { api } from '../utils/api'
import GermanCharacterHelper from '../components/GermanCharacterHelper.vue'

const appStore = useAppStore()

// Data
const vocabulary = ref([])
const loading = ref(false)
const showAddForm = ref(false)
const editingWord = ref(null)
const saveLoading = ref(false)

// Search and filter
const searchQuery = ref('')
const filterType = ref('')
const filterDifficulty = ref('')

// Pagination
const currentPage = ref(1)
const itemsPerPage = 10

// Form
const wordForm = reactive({
  german: '',
  english: '',
  word_type: '',
  difficulty: '',
  notes: ''
})

const formErrors = reactive({})

// Computed
const filteredVocabulary = computed(() => {
  let filtered = vocabulary.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(word => 
      word.german.toLowerCase().includes(query) ||
      word.english.toLowerCase().includes(query)
    )
  }

  if (filterType.value) {
    filtered = filtered.filter(word => word.word_type === filterType.value)
  }

  if (filterDifficulty.value) {
    filtered = filtered.filter(word => word.difficulty === filterDifficulty.value)
  }

  return filtered
})

const totalPages = computed(() => {
  return Math.ceil(filteredVocabulary.value.length / itemsPerPage)
})

const visiblePages = computed(() => {
  const pages = []
  const start = Math.max(1, currentPage.value - 2)
  const end = Math.min(totalPages.value, start + 4)
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  
  return pages
})

// Methods
const loadVocabulary = async () => {
  loading.value = true
  
  try {
    const response = await api.get('/api/vocabulary')
    vocabulary.value = response.data.vocabulary || []
  } catch (error) {
    appStore.showAlert(error.response?.data?.error || 'Failed to load vocabulary', 'error')
  } finally {
        loading.value = false
  }
}

const saveWord = async () => {
  clearFormErrors()
  saveLoading.value = true
  
  try {
    if (editingWord.value) {
      await api.put(`/api/vocabulary/${editingWord.value.id}`, wordForm)
      appStore.showAlert('Word updated successfully!', 'success')
    } else {
      await api.post('/api/vocabulary', wordForm)
      appStore.showAlert('Word added successfully!', 'success')
    }
    
    closeForm()
    loadVocabulary()
  } catch (error) {
    const errorData = error.response?.data
    if (errorData?.errors) {
      Object.assign(formErrors, errorData.errors)
    } else {
      appStore.showAlert(errorData?.error || 'Failed to save word', 'error')
    }
  } finally {
    saveLoading.value = false
  }
}

const editWord = (word) => {
  editingWord.value = word
  Object.assign(wordForm, {
    german: word.german,
    english: word.english,
    word_type: word.word_type || '',
    difficulty: word.difficulty || '',
    notes: word.notes || ''
  })
}

const confirmDelete = (word) => {
  if (confirm(`Are you sure you want to delete "${word.german}"?`)) {
    deleteWord(word)
  }
}

const deleteWord = async (word) => {
  try {
    await api.delete(`/api/vocabulary/${word.id}`)
    appStore.showAlert('Word deleted successfully!', 'success')
    loadVocabulary()
  } catch (error) {
    appStore.showAlert(error.response?.data?.error || 'Failed to delete word', 'error')
  }
}

const closeForm = () => {
  showAddForm.value = false
  editingWord.value = null
  clearFormErrors()
  Object.assign(wordForm, {
    german: '',
    english: '',
    word_type: '',
    difficulty: '',
    notes: ''
  })
}

const clearFormErrors = () => {
  Object.keys(formErrors).forEach(key => delete formErrors[key])
}

const clearSearch = () => {
  searchQuery.value = ''
  currentPage.value = 1
}

const filterVocabulary = () => {
  currentPage.value = 1
}

const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}

const playAudio = async (word) => {
  try {
    const response = await api.get(`/api/audio/tts?text=${encodeURIComponent(word)}&lang=de`)
    if (response.data.audio_url) {
      const audio = new Audio(response.data.audio_url)
      audio.play()
    } else {
      appStore.showAlert('Audio not available for this word', 'warning')
    }
  } catch (error) {
    appStore.showAlert('Failed to play audio', 'error')
  }
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString()
}

// Debounced search
let searchTimeout = null
const debouncedSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    currentPage.value = 1
  }, 300)
}

onMounted(() => {
  loadVocabulary()
})
</script>

<style scoped>
.vocabulary-item .card {
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.vocabulary-item .card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.vocabulary-number {
  background: #667eea;
  color: white;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

.badge.difficulty-beginner {
  background-color: #28a745;
  color: white;
}

.badge.difficulty-intermediate {
  background-color: #ffc107;
  color: #212529;
}

.badge.difficulty-advanced {
  background-color: #dc3545;
  color: white;
}

.modal {
  background-color: rgba(0, 0, 0, 0.5);
}
</style>
