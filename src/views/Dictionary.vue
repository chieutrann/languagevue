<template>
  <div class="dictionary-section">
    <div class="function-box lookup-box mb-4">
      <div class="box-header">
        <h3>🔍 German Dictionary Search</h3>
        <p>Get comprehensive word data from Digital Dictionary of German</p>
      </div>
      <div class="function-content">
        <div class="search-box">
          <div class="input-wrapper position-relative">
            <AutocompleteInput
              v-model="searchQuery"
              placeholder="Enter a German word to search..."
              :suggestions="suggestions"
              @search="lookupWord"
              @input="fetchSuggestions"
            />
            <GermanCharacterHelper target-input="dictionary-search" />
          </div>
          <button @click="lookupWord" class="btn btn-danger ms-2" :disabled="loading">
            <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
            {{ loading ? 'Searching...' : 'Search Word' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Search Results -->
    <div v-if="searchResults" class="results-section">
      <div class="card">
        <div class="card-header">
          <h4 class="mb-0">
            <i class="fas fa-book me-2"></i>
            Search Results for "{{ searchResults.word }}"
          </h4>
        </div>
        <div class="card-body">
          <div v-if="searchResults.definitions?.length" class="definitions">
            <h5>Definitions</h5>
            <div v-for="(def, index) in searchResults.definitions" :key="index" class="definition-item mb-3">
              <div class="d-flex justify-content-between align-items-start">
                <div>
                  <strong>{{ def.word_type }}</strong>
                  <p class="mb-1">{{ def.definition }}</p>
                  <small class="text-muted">{{ def.translation }}</small>
                </div>
                <button 
                  @click="addToVocabulary(def)" 
                  class="btn btn-outline-primary btn-sm"
                  title="Add to vocabulary"
                >
                  <i class="fas fa-plus"></i>
                </button>
              </div>
            </div>
          </div>
          
          <div v-if="searchResults.examples?.length" class="examples mt-4">
            <h5>Example Sentences</h5>
            <div v-for="(example, index) in searchResults.examples" :key="index" class="example-item mb-2">
              <p class="mb-1">{{ example.german }}</p>
              <small class="text-muted">{{ example.english }}</small>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Additional Features -->
    <div class="additional-features mt-5">
      <h3>Additional Features</h3>
      
      <!-- Feature Tabs -->
      <ul class="nav nav-tabs" role="tablist">
        <li class="nav-item">
          <button 
            class="nav-link" 
            :class="{ active: activeFeature === 'conjugation' }"
            @click="activeFeature = 'conjugation'"
          >
            ⚡ Conjugation
          </button>
        </li>
        <li class="nav-item">
          <button 
            class="nav-link" 
            :class="{ active: activeFeature === 'examples' }"
            @click="activeFeature = 'examples'"
          >
            💡 Examples
          </button>
        </li>
        <li class="nav-item">
          <button 
            class="nav-link" 
            :class="{ active: activeFeature === 'browse' }"
            @click="activeFeature = 'browse'"
          >
            📚 Browse
          </button>
        </li>
      </ul>

      <!-- Tab Contents -->
      <div class="tab-content mt-3">
        <!-- Conjugation Tab -->
        <div v-show="activeFeature === 'conjugation'" class="tab-pane">
          <div class="function-box">
            <div class="box-header">
              <h4>⚡ Verb Conjugation</h4>
              <p>Get complete conjugation forms for any German verb</p>
            </div>
            <div class="function-content">
              <div class="d-flex gap-2 mb-3">
                <input 
                  v-model="conjugationQuery" 
                  type="text" 
                  class="form-control" 
                  placeholder="Enter a German verb..."
                  @keyup.enter="getConjugation"
                >
                <button @click="getConjugation" class="btn btn-success" :disabled="conjugationLoading">
                  {{ conjugationLoading ? 'Loading...' : 'Conjugate' }}
                </button>
              </div>
              
              <div v-if="conjugationResults" class="conjugation-results">
                <div class="row">
                  <div v-for="(tense, tenseKey) in conjugationResults" :key="tenseKey" class="col-md-6 mb-3">
                    <div class="card">
                      <div class="card-header">
                        <h6 class="mb-0">{{ formatTenseName(tenseKey) }}</h6>
                      </div>
                      <div class="card-body">
                        <div v-for="(form, pronoun) in tense" :key="pronoun" class="d-flex justify-content-between">
                          <span>{{ pronoun }}</span>
                          <strong>{{ form }}</strong>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Examples Tab -->
        <div v-show="activeFeature === 'examples'" class="tab-pane">
          <div class="function-box">
            <div class="box-header">
              <h4>💡 Word Examples</h4>
              <p>Get practical examples and usage patterns</p>
            </div>
            <div class="function-content">
              <div class="d-flex gap-2 mb-3">
                <input 
                  v-model="examplesQuery" 
                  type="text" 
                  class="form-control" 
                  placeholder="Enter a German word..."
                  @keyup.enter="getExamples"
                >
                <button @click="getExamples" class="btn btn-warning" :disabled="examplesLoading">
                  {{ examplesLoading ? 'Loading...' : 'Get Examples' }}
                </button>
              </div>
              
              <div v-if="exampleResults?.length" class="examples-results">
                <div v-for="(example, index) in exampleResults" :key="index" class="example-card mb-3">
                  <div class="card">
                    <div class="card-body">
                      <p class="mb-2">{{ example.german }}</p>
                      <small class="text-muted">{{ example.english }}</small>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Browse Tab -->
        <div v-show="activeFeature === 'browse'" class="tab-pane">
          <div class="function-box">
            <div class="box-header">
              <h4>📚 Browse Dictionary</h4>
              <p>Explore words by type, difficulty, or get random selections</p>
            </div>
            <div class="function-content">
              <div class="row">
                <div class="col-md-6">
                  <h5>Word Types</h5>
                  <div class="d-grid gap-2">
                    <button @click="browseByType('noun')" class="btn btn-outline-primary">Nouns</button>
                    <button @click="browseByType('verb')" class="btn btn-outline-success">Verbs</button>
                    <button @click="browseByType('adjective')" class="btn btn-outline-info">Adjectives</button>
                  </div>
                </div>
                <div class="col-md-6">
                  <h5>Difficulty Levels</h5>
                  <div class="d-grid gap-2">
                    <button @click="browseByDifficulty('beginner')" class="btn btn-outline-success">Beginner</button>
                    <button @click="browseByDifficulty('intermediate')" class="btn btn-outline-warning">Intermediate</button>
                    <button @click="browseByDifficulty('advanced')" class="btn btn-outline-danger">Advanced</button>
                  </div>
                </div>
              </div>
              
              <div class="text-center mt-4">
                <button @click="getRandomWords" class="btn btn-primary me-2" :disabled="randomLoading">
                  🎲 {{ randomLoading ? 'Loading...' : 'Random Words' }}
                </button>
                <button @click="showStats" class="btn btn-info">📊 Statistics</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Browse Results -->
    <div v-if="browseResults?.length" class="browse-results mt-4">
      <h4>Browse Results</h4>
      <div class="row">
        <div v-for="word in browseResults" :key="word.id" class="col-md-4 mb-3">
          <div class="card">
            <div class="card-body">
              <h6 class="card-title">{{ word.german }}</h6>
              <p class="card-text">{{ word.english }}</p>
              <small class="text-muted">{{ word.word_type }}</small>
              <div class="mt-2">
                <button @click="addToVocabulary(word)" class="btn btn-sm btn-outline-primary">
                  Add to Vocabulary
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useAppStore } from '../stores/app'
import { api } from '../utils/api'
import AutocompleteInput from '../components/AutocompleteInput.vue'
import GermanCharacterHelper from '../components/GermanCharacterHelper.vue'

const appStore = useAppStore()

// Search functionality
const searchQuery = ref('')
const suggestions = ref([])
const searchResults = ref(null)
const loading = ref(false)

// Feature tabs
const activeFeature = ref('conjugation')

// Conjugation
const conjugationQuery = ref('')
const conjugationResults = ref(null)
const conjugationLoading = ref(false)

// Examples
const examplesQuery = ref('')
const exampleResults = ref([])
const examplesLoading = ref(false)

// Browse
const browseResults = ref([])
const randomLoading = ref(false)

const fetchSuggestions = async (query) => {
  if (!query || query.length < 2) {
    suggestions.value = []
    return
  }
  
  try {
    const response = await api.get(`/api/dictionary/suggestions?q=${encodeURIComponent(query)}`)
    suggestions.value = response.data.suggestions || []
  } catch (error) {
    console.error('Failed to fetch suggestions:', error)
  }
}

const lookupWord = async () => {
  if (!searchQuery.value.trim()) {
    appStore.showAlert('Please enter a word to search', 'warning')
    return
  }
  
  loading.value = true
  
  try {
    const response = await api.get(`/api/dictionary/lookup?word=${encodeURIComponent(searchQuery.value)}`)
    searchResults.value = response.data
  } catch (error) {
    appStore.showAlert(error.response?.data?.error || 'Failed to lookup word', 'error')
  } finally {
    loading.value = false
  }
}

const getConjugation = async () => {
  if (!conjugationQuery.value.trim()) return
  
  conjugationLoading.value = true
  
  try {
    const response = await api.get(`/api/dictionary/conjugation?verb=${encodeURIComponent(conjugationQuery.value)}`)
    conjugationResults.value = response.data.conjugation
  } catch (error) {
    appStore.showAlert(error.response?.data?.error || 'Failed to get conjugation', 'error')
  } finally {
    conjugationLoading.value = false
  }
}

const getExamples = async () => {
  if (!examplesQuery.value.trim()) return
  
  examplesLoading.value = true
  
  try {
    const response = await api.get(`/api/dictionary/examples?word=${encodeURIComponent(examplesQuery.value)}`)
    exampleResults.value = response.data.examples || []
  } catch (error) {
    appStore.showAlert(error.response?.data?.error || 'Failed to get examples', 'error')
  } finally {
    examplesLoading.value = false
  }
}

const browseByType = async (type) => {
  try {
    const response = await api.get(`/api/dictionary/browse/type/${type}`)
    browseResults.value = response.data.words || []
  } catch (error) {
    appStore.showAlert(error.response?.data?.error || 'Failed to browse words', 'error')
  }
}

const browseByDifficulty = async (difficulty) => {
  try {
    const response = await api.get(`/api/dictionary/browse/difficulty/${difficulty}`)
    browseResults.value = response.data.words || []
  } catch (error) {
    appStore.showAlert(error.response?.data?.error || 'Failed to browse words', 'error')
  }
}

const getRandomWords = async () => {
  randomLoading.value = true
  
  try {
    const response = await api.get('/api/dictionary/random')
    browseResults.value = response.data.words || []
  } catch (error) {
    appStore.showAlert(error.response?.data?.error || 'Failed to get random words', 'error')
  } finally {
    randomLoading.value = false
  }
}

const showStats = async () => {
  try {
    const response = await api.get('/api/dictionary/stats')
    const stats = response.data
    appStore.showAlert(`Dictionary contains ${stats.total_words} words`, 'info')
  } catch (error) {
    appStore.showAlert('Failed to load statistics', 'error')
  }
}

const addToVocabulary = async (word) => {
  try {
    await api.post('/api/vocabulary', {
      german: word.german || word.word,
      english: word.english || word.translation,
      word_type: word.word_type
    })
    appStore.showAlert('Added to vocabulary!', 'success')
  } catch (error) {
    appStore.showAlert(error.response?.data?.error || 'Failed to add to vocabulary', 'error')
  }
}

const formatTenseName = (tenseKey) => {
  return tenseKey.charAt(0).toUpperCase() + tenseKey.slice(1).replace('_', ' ')
}
</script>

<style scoped>
.function-box {
  background: white;
  border: 1px solid #e1e5e9;
  border-radius: 12px;
  margin-bottom: 25px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  overflow: hidden;
}

.lookup-box {
  border-left: 4px solid #dc3545;
}

.box-header {
  background: #f8f9fa;
  padding: 20px;
  border-bottom: 1px solid #e1e5e9;
}

.box-header h3, .box-header h4 {
  margin: 0 0 5px 0;
  color: #333;
  font-size: 1.3em;
  font-weight: 600;
}

.box-header p {
  margin: 0;
  color: #666;
  font-size: 0.95em;
}

.function-content {
  padding: 20px;
}

.search-box {
  display: flex;
  gap: 10px;
  align-items: start;
}

.input-wrapper {
  flex: 1;
}

.definition-item {
  padding: 1rem;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  background: #f8f9fa;
}

.example-item, .example-card {
  padding: 0.75rem;
  border-left: 3px solid #667eea;
  background: #f8f9fa;
  border-radius: 4px;
}

.nav-tabs .nav-link {
  border: none;
  color: #666;
}

.nav-tabs .nav-link.active {
  background-color: transparent;
  border-bottom: 2px solid #667eea;
  color: #667eea;
}
</style>
