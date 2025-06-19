<template>
  <div class="dictionary-container">
    <!-- Flex container for search, result, and features -->
    <div class="lookup-flex-row" style="display: flex; gap: 32px; align-items: flex-start;">
      <!-- Top Search Bar -->
      <div class="top-search-bar" style="flex: 1; min-width: 320px;">
        <div class="function-box lookup-box">
          <div class="box-header">
            <h3>🔍 German Dictionary Search</h3>
            <p>Get comprehensive word data from Digital Dictionary of German</p>
            </div>
          </div>
          <div class="function-content">
            <div class="search-box-group">
              <div class="search-box">
                <div class="input-wrapper" style="position:relative;" ref="inputWrapperRef">
                  <input
                    type="text"
                    v-model="searchQuery"
                    id="lookupInput"
                    placeholder="Enter a German word to search..."
                    @keydown.enter="lookupWord"
                    @input="handleInput"
                    autocomplete="off"/>
                  <div class="german-chars">
                    <button type="button" @click="insertChar('ä')" class="char-btn">ä</button>
                    <button type="button" @click="insertChar('ö')" class="char-btn">ö</button>
                    <button type="button" @click="insertChar('ü')" class="char-btn">ü</button>
                    <button type="button" @click="insertChar('ß')" class="char-btn">ß</button>
                    <button type="button" @click="toggleSearchDirection" class="direction-btn" title="Toggle search direction">🔄</button>
                  </div>
                  <div v-if="showSuggestions" class="suggestions-container" id="suggestions">
                    <div
                      v-for="suggestion in suggestions"
                      :key="suggestion.word"
                      class="suggestion-item"
                      @click="selectSuggestion(suggestion.word)"
                      :class="{ 'exact-match': suggestion.type === 'starts_with', 'contains-match': suggestion.type === 'contains', 'similar-match': suggestion.type === 'similar' }"
                    >
                      <div class="suggestion-word">{{ suggestion.word }}</div>
                      <div class="suggestion-info">
                        <span v-if="suggestion.type === 'noun'" class="suggestion-badge noun-badge">{{ suggestion.article }}</span>
                        <span v-else-if="suggestion.type === 'verb'" class="suggestion-badge verb-badge">verb</span>
                        <span v-else-if="suggestion.type === 'adjective'" class="suggestion-badge adjective-badge">adj</span>
                      </div>
                    </div>
                  </div>
                </div>
                <button class="danger-btn" @click="lookupWord">Search Word</button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- Dictionary Results Section -->
      <div style="display: flex; flex-direction: column; flex: 2; min-width: 400px; gap: 16px;">
        <div id="lookup-results" class="results-section" style="flex: 1; min-width: 320px;">
          <div v-if="loading" class="loading-box">
            <div class="loading-spinner">⏳</div>
            <div class="loading-message">Loading...</div>
          </div>
          <div v-else-if="error" class="error-box">
            <div class="error-icon">❌</div>
            <div class="error-message">{{ error }}</div>
          </div>
          <div v-else-if="lookupResult" class="word-info-box">
            <div class="box-header-result">
              Result Lookup
              <span v-if="lookupResult.cached" class="cache-badge" title="Result from cache">⚡</span>
            </div>
            <div class="word-title">
              🇩🇪 {{ lookupResult.word }}
              <span v-if="lookupResult.article" class="article-badge">{{ lookupResult.article }}</span>
              <span v-if="lookupResult.word_type" class="type-badge">{{ lookupResult.word_type }}</span>
              <button
                v-if="lookupResult.audio_url"
                @click="playWordAudio(lookupResult.word)"
                class="audio-btn"
                title="Listen to pronunciation"
              >🔊</button>
              <button
                v-if="authStore.isAuthenticated"
                @click="openSaveToFolderModal"
                class="star-btn"
                :title="t('dictionary.addToVocabulary')"
                style="margin-left: 4px; font-size: 20px; color: gold; background: none; border: none; cursor: pointer; vertical-align: middle; display: flex; align-items: center; gap: 4px;"
              >
                ★
                <span style="font-size: 14px;">
                  {{ t('dictionary.addToVocabulary') }}
                </span>
              </button>
            </div>
            
            <div class="word-translation">
              <span v-if="appStore.currentLanguage === 'en'">🇬🇧</span>
              <span v-else-if="appStore.currentLanguage === 'vi'">🇻🇳</span>
              {{ lookupResult.definition }}
            </div>
          </div>
        </div>
        <!-- Additional Features Tabs (moved here) -->
        <div class="additional-features">
          <div class="function-tabs">
            <button class="tab-btn" :class="{active: activeTab==='conjugation'}" @click="showTab('conjugation')">⚡ Conjugation</button>
            <button class="tab-btn" :class="{active: activeTab==='examples'}" @click="showTab('examples')">💡 Examples</button>
            <button class="tab-btn" :class="{active: activeTab==='browse'}" @click="showTab('browse')">📚 Browse</button>
          </div>
          <div class="tab-contents">
            <div v-show="activeTab==='conjugation'" class="tab-content active">
              <div class="function-box conjugation-box">
                <div class="box-header">
                  <h3>⚡ Verb Conjugation</h3>
                  <p>Get complete conjugation forms for any German verb</p>
                </div>
                <div class="function-content">
                  <button class="success-btn" @click="getConjugation" :disabled="conjugationLoading">Show Conjugation</button>
                  <div v-if="conjugationLoading" class="loading-box">Loading...</div>
                  <div v-if="conjugationResult">
                    <div class="conjugation-result-box">
                      <div class="box-header-result">Conjugation: {{ searchQuery }}</div>
                      <div class="conjugation-grid">
                        <div v-for="(forms, tense) in conjugationResult" :key="tense" class="tense-section">
                          <div class="tense-title">{{ tense }}</div>
                          <div class="conjugation-table">
                            <div v-for="(form, pronoun) in forms" :key="pronoun" class="conjugation-item">
                              <span class="pronoun">{{ pronoun }}</span>
                              <span class="form">{{ form }}</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="tab-content" :style="activeTab==='examples' ? 'display:block;' : 'display:none;'">
              <div class="function-box examples-box">
                <div class="box-header">
                  <h3>💡 Word Examples</h3>
                  <p>Get practical examples and usage patterns</p>
                </div>
                <div class="function-content">
                  <button class="warning-btn" @click="getExamples" :disabled="examplesLoading">Show Examples</button>
                  <div v-if="examplesLoading" class="loading-box">Loading...</div>
                  <div v-if="exampleResults.length">
                    <div class="examples-result-box">
                      <div class="box-header-result">Examples: {{ searchQuery }}</div>
                      <div v-for="section in exampleResults" :key="section.heading || section.german || section.sentence" class="example-section">
                        <h4 class="example-heading" v-if="section.heading">{{ section.heading }}</h4>
                        <div class="examples-list">
                          <div v-for="example in (section.examples || [section])" :key="example.sentence || example.german" class="example">
                            <div class="german">🇩🇪 {{ example.sentence || example.german }}</div>
                            <div class="translation">{{ example.translation }}</div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-show="activeTab==='browse'" class="tab-content">
              <div class="function-box browse-box">
                <div class="box-header">
                  <h3>📚 Browse Dictionary</h3>
                  <p>Explore words by type, difficulty, or get random selections</p>
                </div>
                <div class="function-content">
                  <div class="function-grid">
                    <div class="function-category">
                      <h4>Word Types</h4>
                      <div class="button-group">
                        <button class="category-btn noun-btn" @click="browseByType('noun')">Nouns</button>
                        <button class="category-btn verb-btn" @click="browseByType('verb')">Verbs</button>
                        <button class="category-btn adj-btn" @click="browseByType('adjective')">Adjectives</button>
                      </div>
                    </div>
                    <div class="function-category">
                      <h4>Difficulty Levels</h4>
                      <div class="button-group">
                        <button class="category-btn beginner-btn" @click="browseByDifficulty('beginner')">Beginner</button>
                        <button class="category-btn intermediate-btn" @click="browseByDifficulty('intermediate')">Intermediate</button>
                        <button class="category-btn advanced-btn" @click="browseByDifficulty('advanced')">Advanced</button>
                      </div>
                    </div>
                  </div>
                  <div style="text-align: center; margin-top: 20px;">
                    <button class="action-btn random-btn" @click="getRandomWords" :disabled="randomLoading">🎲 Random Words</button>
                  </div>
                  <div v-if="browseResults.length" class="browse-results mt-4">
                    <div v-for="word in browseResults" :key="word.id || word.german || word.word" class="word-card">
                      <div class="word-title">{{ word.german || word.word }}</div>
                      <div class="word-translation">{{ word.english || word.translation }}</div>
                      <div class="word-type">{{ word.word_type }}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- Back to Top Button -->
    <button id="backToTopBtn" title="Back to top" style="display:none;position:fixed;bottom:40px;right:40px;z-index:9999;padding:10px 16px;font-size:18px;border:none;border-radius:50%;background:#667eea;color:#fff;box-shadow:0 2px 8px rgba(0,0,0,0.15);cursor:pointer;transition:background 0.2s;" @click="scrollToTop">
      ↑
    </button>

    <!-- Save to Folder Modal -->
    <div v-if="showSaveModal" class="modal-backdrop">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ t('dictionary.saveToFolderTitle') }}</h5>
            <button type="button" class="btn-close" @click="closeSaveToFolderModal"></button>
          </div>
          <div class="modal-body">
            <div v-if="foldersLoading" class="text-center">{{ t('dictionary.loadingFolders') }}</div>
            <div v-else>
              <label for="folderSelect">{{ t('dictionary.selectFolder') }}</label>
              <select id="folderSelect" v-model="selectedFolderId" class="form-select mb-2">
                <option v-for="folder in folders" :key="folder.id" :value="folder.id">{{ folder.name }}</option>
              </select>
              <div class="mb-2">{{ t('dictionary.orCreateNew') }}</div>
              <input v-model="newFolderName" class="form-control mb-2" :placeholder="t('dictionary.newFolderName')" />
              <input v-model="newFolderDesc" class="form-control mb-2" :placeholder="t('dictionary.newFolderDesc')" />
              <button class="btn btn-secondary btn-sm mb-2" @click="createFolder" :disabled="creatingFolder">{{ t('dictionary.createFolder') }}</button>
            </div>
            <div v-if="saveError" class="alert alert-danger mt-2">{{ saveError }}</div>
            <div v-if="saveSuccess" class="alert alert-success mt-2">{{ saveSuccess }}</div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeSaveToFolderModal">{{ t('dictionary.cancel') }}</button>
            <button class="btn btn-primary" @click="saveToFolder" :disabled="savingWord || !selectedFolderId">{{ t('dictionary.save') }}</button>
          </div>
        </div>
      </div>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { getWord, api } from '../utils/api'
import { useAppStore } from '../stores/app'
import { useAuthStore } from '../stores/auth'
import { useTranslation } from '../composables/useTranslation'
const appStore = useAppStore()
const authStore = useAuthStore()
const { t } = useTranslation()

const searchQuery = ref('')
const suggestions = ref([])
const showSuggestions = ref(false)
const loading = ref(false)
const error = ref('')
const lookupResult = ref(null)
const activeTab = ref('conjugation')
const isReverseSearch = ref(false)
let suggestionTimeout = null // changed from const ref(null)

// Conjugation
const conjugationLoading = ref(false)
const conjugationResult = ref(null)

// Examples
const examplesLoading = ref(false)
const exampleResults = ref([])

// Browse
const browseResults = ref([])
const randomLoading = ref(false)

// Save to folder modal state
const showSaveModal = ref(false)
const folders = ref([])
const foldersLoading = ref(false)
const selectedFolderId = ref(null)
const newFolderName = ref('')
const newFolderDesc = ref('')
const creatingFolder = ref(false)
const savingWord = ref(false)
const saveError = ref('')
const saveSuccess = ref('')

const inputWrapperRef = ref(null)

onMounted(() => {
  window.addEventListener('scroll', () => {
    const btn = document.getElementById('backToTopBtn')
    if (!btn) return
    btn.style.display = window.scrollY > 200 ? 'block' : 'none'
  })

  // Click outside to close suggestions
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})

function handleClickOutside(event) {
  if (!inputWrapperRef.value) return
  if (!inputWrapperRef.value.contains(event.target)) {
    showSuggestions.value = false
  }
}

function insertChar(char) {
  nextTick(() => {
    const input = document.getElementById('lookupInput')
    if (!input) return
    const start = input.selectionStart
    const end = input.selectionEnd
    const value = input.value
    input.value = value.substring(0, start) + char + value.substring(end)
    input.focus()
    input.setSelectionRange(start + 1, start + 1)
    searchQuery.value = input.value
  })
}

function toggleSearchDirection() {
  isReverseSearch.value = !isReverseSearch.value
  searchQuery.value = ''
  suggestions.value = []
  showSuggestions.value = false
}

async function fetchSuggestions(query) {
  console.log("fetchSuggestions called with:", query);

  if (!query || query.length < 2 || isReverseSearch.value) {
    console.log("Skipping suggestion fetch - empty query or reverse search mode");
    showSuggestions.value = false;
    suggestions.value = [];
    return;
  }

  showSuggestions.value = true;
  suggestions.value = [{ word: 'Loading suggestions...', type: 'loading' }];

  try {
    // Use the correct API endpoint with /api prefix
    const endpoint = `/dictionary/autocomplete?query=${encodeURIComponent(query)}&limit=10`;
    console.log("Fetching suggestions from:", endpoint);
    
    const res = await api.get(endpoint);
    console.log("Suggestions response:", res.data);

    if (res.data && res.data.suggestions && res.data.suggestions.length > 0) {
      // API returns {suggestions: [...]}
      suggestions.value = res.data.suggestions;
      showSuggestions.value = true;
    } else {
      console.log("No suggestions found in response, displaying 'not found' message.");
      suggestions.value = [{ word: 'No matches found', type: 'info' }];
      // Keep the suggestions box open to show the message
      showSuggestions.value = true; 
    }
  } catch (error) {
    console.error("Error fetching suggestions:", error);
    suggestions.value = [{ word: 'Error loading suggestions', type: 'error' }];
    // Keep the suggestions box open to show the error
    showSuggestions.value = true; 
    // Optionally, hide after a delay
    setTimeout(() => {
      if (suggestions.value.length > 0 && suggestions.value[0].type === 'error') {
          showSuggestions.value = false;
          suggestions.value = [];
      }
    }, 3000);
  }
}

function selectSuggestion(word) {
  searchQuery.value = word;
  showSuggestions.value = false;
  lookupWord();
}

async function lookupWord() {
  const word = searchQuery.value.trim()
  if (!word) return
  loading.value = true
  error.value = ''
  lookupResult.value = null
  try {
    // Use appStore.currentLanguage for translation direction (no .value needed)
    const srcLang = isReverseSearch.value ? appStore.currentLanguage : 'de'
    const destLang = isReverseSearch.value ? 'de' : appStore.currentLanguage
    console.log('Language settings:', { 
      currentLanguage: appStore.currentLanguage,
      srcLang, 
      destLang
    })
    const data = await getWord(word, srcLang, destLang)
    if (data.error) {
      error.value = data.error
      lookupResult.value = null
    } else {
      lookupResult.value = data
    }
  } catch (e) {
    error.value = 'Lookup failed.'
    lookupResult.value = null
  } finally {
    loading.value = false
  }
}




function playWordAudio(word) {
  if (!lookupResult.value || !lookupResult.value.audio_url) {
    alert('No audio available for this word.')
    return
  }
  const audio = new Audio(lookupResult.value.audio_url)
  audio.play()
}

function showTab(tab) {
  activeTab.value = tab
}

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// Conjugation Feature
async function getConjugation() {
  const word = searchQuery.value.trim()
  if (!word) return
  conjugationLoading.value = true
  conjugationResult.value = null
  try {
    // Pass language to backend if supported
    const res = await api.get(`/dictionary/conjugate?verb=${encodeURIComponent(word)}`)
    conjugationResult.value = res.data.conjugation
  } catch (e) {
    conjugationResult.value = null
  } finally {
    conjugationLoading.value = false
  }
}

// Examples Feature
async function getExamples() {
  const word = searchQuery.value.trim();
  const lang = appStore.currentLanguage || 'en';

  if (!word) {
    error.value = 'Please enter a word to get examples.';
    exampleResults.value = [];
    return;
  }

  examplesLoading.value = true;
  exampleResults.value = [];
  error.value = '';

  try {
    let res;
    if (lang === 'en') {
      res = await api.get(`/dictionary/examples?word=${encodeURIComponent(word)}`);
      if (res.data && res.data.examples && res.data.examples.length > 0) {
        exampleResults.value = res.data.examples;
      } else {
        error.value = 'No examples found.';
        exampleResults.value = [];
      }
    } else {
      res = await api.get(`/dictionary/examples-other?word=${encodeURIComponent(word)}&language=de&target_language=${lang}`);
      if (res.data && Array.isArray(res.data) && res.data.length > 0) {
        exampleResults.value = [{ heading: 'Examples', examples: res.data }];
      } else {
        error.value = 'No examples found.';
        exampleResults.value = [];
      }
    }
  } catch (e) {
    error.value = 'Failed to fetch examples.';
    exampleResults.value = [];
  } finally {
    examplesLoading.value = false;
  }
}

// Browse Feature
async function browseByType(type) {
  try {
    const lang = appStore.currentLanguage
    const res = await api.get(`/dictionary/type/${type}?lang=${lang}`)
    browseResults.value = res.data.words || []
  } catch (e) {
    browseResults.value = []
  }
}

async function browseByDifficulty(difficulty) {
  try {
    const lang = appStore.currentLanguage
    const res = await api.get(`/dictionary/difficulty/${difficulty}?lang=${lang}`)
    browseResults.value = res.data.words || []
  } catch (e) {
    browseResults.value = []
  }
}

async function getRandomWords() {
  randomLoading.value = true
  try {
    const lang = appStore.currentLanguage
    const res = await api.get(`/dictionary/random?lang=${lang}`)
    browseResults.value = res.data.words || []
  } catch (e) {
    browseResults.value = []
  } finally {
    randomLoading.value = false
  }
}

function openSaveToFolderModal() {
  saveError.value = ''
  saveSuccess.value = ''
  showSaveModal.value = true
  fetchFolders()
}
function closeSaveToFolderModal() {
  showSaveModal.value = false
  selectedFolderId.value = null
  newFolderName.value = ''
  newFolderDesc.value = ''
  saveError.value = ''
  saveSuccess.value = ''
}
async function fetchFolders() {
  foldersLoading.value = true
  try {
    const res = await api.get('/folders')
    // folders is an object, convert to array
    folders.value = Object.entries(res.data).map(([id, folder]) => ({ id, ...folder }))
    if (folders.value.length > 0) selectedFolderId.value = folders.value[0].id
  } catch (e) {
    saveError.value = 'Failed to load folders.'
  } finally {
    foldersLoading.value = false
  }
}
async function createFolder() {
  if (!newFolderName.value.trim()) {
    saveError.value = 'Folder name required.'
    return
  }
  creatingFolder.value = true
  saveError.value = ''
  try {
    const res = await api.post('/folders', { name: newFolderName.value, description: newFolderDesc.value })
    if (res.data.folder) {
      folders.value.push({ id: res.data.id, ...res.data.folder })
      selectedFolderId.value = res.data.id
      newFolderName.value = ''
      newFolderDesc.value = ''
      saveSuccess.value = 'Folder created!'
    }
  } catch (e) {
    saveError.value = e.response?.data?.error === 'already_exists' ? 'Folder already exists.' : 'Failed to create folder.'
  } finally {
    creatingFolder.value = false
  }
}
async function saveToFolder() {
  if (!selectedFolderId.value || !lookupResult.value) return
  savingWord.value = true
  saveError.value = ''
  saveSuccess.value = ''
  try {
    // Check if word already exists in the folder
    const checkRes = await api.post(`/folders/${selectedFolderId.value}/check-word`, {
      word: lookupResult.value.word
    })
    if (checkRes.data && checkRes.data.exists) {
      saveError.value = t('dictionary.saveErrorExists')
      savingWord.value = false
      return
    }
    // If not exists, add the word
    const res = await api.post(`/folders/${selectedFolderId.value}/vocabularies`, {
      word: lookupResult.value.word,
      definition: lookupResult.value.definition
    })
    if (res.data && res.data.id) {
      saveSuccess.value = t('dictionary.saveSuccess')
      setTimeout(() => closeSaveToFolderModal(), 1200)
    } else {
      saveError.value = t('dictionary.saveErrorFailed')
    }
  } catch (e) {
    if (e.response?.data?.error === 'already_exists' || e.response?.data?.error === 'Word already exists in this folder.') {
      saveError.value = t('dictionary.saveErrorExists')
    } else {
      saveError.value = t('dictionary.saveErrorFailed')
    }
  } finally {
    savingWord.value = false
  }
}

function handleInput() {
  console.log('Input handled. Current query:', searchQuery.value);

  if (suggestionTimeout) {
    clearTimeout(suggestionTimeout);
  }

  suggestionTimeout = setTimeout(() => {
    fetchSuggestions(searchQuery.value);
  }, 300);
}
</script>

<style src="../utils/dictionary.css"></style>
<style scoped>
.suggestions-container {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #ddd;
  border-radius: 0 0 8px 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  max-height: 300px;
  overflow-y: auto;
  z-index: 100;
}

.suggestion-item {
  padding: 8px 16px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #f0f0f0;
  font-size: 16px;
}

.suggestion-item:last-child {
  border-bottom: none;
}

.suggestion-item:hover {
  background-color: #f5f8ff;
}

.suggestion-indicator {
  color: #888;
  font-size: 14px;
}

.input-wrapper {
  position: relative;
  width: 100%;
}

/* To ensure the input has the proper styling */
input[type="text"] {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
}

.german-chars {
  margin-top: 8px;
  display: flex;
  gap: 5px;
}

.char-btn {
  padding: 4px 8px;
  border: 1px solid #ddd;
  background: #f8f9fa;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.2s;
}

.char-btn:hover {
  background: #eaeaea;
}

.modal-backdrop {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.3);
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal-dialog {
  max-width: 400px;
  width: 100%;
}
.star-btn {
  color: gold;
  font-size: 22px;
  background: none;
  border: none;
  cursor: pointer;
  vertical-align: middle;
}
</style>