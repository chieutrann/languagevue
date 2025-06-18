<template>
  <div class="dictionary-container">
    <!-- Top Search Bar -->
    <div class="top-search-bar">
      <div class="function-box lookup-box">
        <div class="box-header">
          <h3>🔍 German Dictionary Search</h3>
          <p>Get comprehensive word data from Digital Dictionary of German</p>
          </div>
        </div>
        <div class="function-content">
          <div class="search-box-group">
            <div class="search-box">
              <div class="input-wrapper" style="position:relative;">
                <input
                  type="text"
                  v-model="searchQuery"
                  id="lookupInput"
                  placeholder="Enter a German word to search..."
                  @keydown.enter="lookupWord"
                  @input="() => { if (suggestionTimeout) clearTimeout(suggestionTimeout); suggestionTimeout = setTimeout(() => fetchSuggestions(searchQuery), 300) }"
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
                  >
                    <span class="suggestion-word">{{ suggestion.word }}</span>
                    <span class="suggestion-type">{{ suggestion.type === 'starts_with' ? '🎯' : '🔍' }}</span>
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
    <div id="lookup-results" class="results-section">
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
        </div>
        <div class="word-translation">{{ lookupResult.definition }}</div>
      </div>
    </div>

    <!-- Additional Features Section -->
    <div class="additional-features">
      <h3>Additional Features</h3>
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
      <!-- Back to Top Button -->
      <button id="backToTopBtn" title="Back to top" style="display:none;position:fixed;bottom:40px;right:40px;z-index:9999;padding:10px 16px;font-size:18px;border:none;border-radius:50%;background:#667eea;color:#fff;box-shadow:0 2px 8px rgba(0,0,0,0.15);cursor:pointer;transition:background 0.2s;" @click="scrollToTop">
        ↑
      </button>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue'
import { getWord, api } from '../utils/api'
import { useAppStore } from '../stores/app'
const appStore = useAppStore()

const searchQuery = ref('')
const suggestions = ref([])
const showSuggestions = ref(false)
const loading = ref(false)
const error = ref('')
const lookupResult = ref(null)
const activeTab = ref('conjugation')
const isReverseSearch = ref(false)
const suggestionTimeout = ref(null)

// Conjugation
const conjugationLoading = ref(false)
const conjugationResult = ref(null)

// Examples
const examplesLoading = ref(false)
const exampleResults = ref([])

// Browse
const browseResults = ref([])
const randomLoading = ref(false)

onMounted(() => {
  window.addEventListener('scroll', () => {
    const btn = document.getElementById('backToTopBtn')
    if (!btn) return
    btn.style.display = window.scrollY > 200 ? 'block' : 'none'
  })
})

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

function fetchSuggestions(query) {
  if (!query || isReverseSearch.value) {
    showSuggestions.value = false
    return
  }
  showSuggestions.value = true
  suggestions.value = [{ word: 'Loading...', type: '' }]
  api.get(`/dictionary/autocomplete?query=${encodeURIComponent(query)}&lang=${appStore.currentLanguage}`)
    .then(res => {
      suggestions.value = res.data.suggestions || []
      showSuggestions.value = suggestions.value.length > 0
    })
    .catch(() => {
      suggestions.value = []
      showSuggestions.value = false
    })
}

function selectSuggestion(word) {
  searchQuery.value = word
  showSuggestions.value = false
  lookupWord()
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

  // Choose endpoint based on language
  const endpoint = lang === 'en'
    ? `/api/dictionary/examples?word=${encodeURIComponent(word)}`
    : `/api/dictionary/examples-other?word=${encodeURIComponent(word)}&language=de&target_language=${lang}`;

  try {
    const res = await fetch(endpoint);
    const data = await res.json();
    if (data && ((data.examples && data.examples.length > 0) || (Array.isArray(data) && data.length > 0))) {
      // Format data to match expected structure for display
      exampleResults.value = lang === 'en'
        ? data.examples
        : [{ heading: 'Examples', examples: data }];
    } else {
      error.value = 'No examples found.';
      exampleResults.value = [];
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
</script>

<style src="../utils/dictionary.css"></style>