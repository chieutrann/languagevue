<template>
  <div class="news-section">
    <h2 class="mb-4">{{ t('news.title') }}</h2>
    
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-2">{{ t('news.loading') }}</p>
    </div>
    
    <div v-else-if="error" class="alert alert-danger">
      <h5>Error loading news</h5>
      <p>{{ error }}</p>
      <button @click="loadNews" class="btn btn-outline-danger">Try Again</button>
    </div>
    
    <div v-else-if="articles.length === 0" class="text-center py-5">
      <i class="fas fa-newspaper fa-3x text-muted mb-3"></i>
      <h5>No news articles available</h5>
      <p class="text-muted">Check back later for new content.</p>
    </div>
    
    <div v-else class="row">
      <div v-for="article in articles" :key="article.id" class="col-md-6 col-lg-4 mb-4">
        <div class="card h-100 shadow-sm">
          <div class="card-body">
            <h5 class="card-title">{{ article.title }}</h5>
            <p class="card-text" v-html="highlightVocab(article.content)"></p>
            <div class="d-flex justify-content-between align-items-center">
              <small class="text-muted">{{ formatDate(article.date) }}</small>
              <span 
                :class="`difficulty-badge difficulty-${article.difficulty}`"
                v-if="article.difficulty"
              >
                {{ article.difficulty }}
              </span>
            </div>
          </div>
          <div class="card-footer bg-transparent">
            <button @click="readArticle(article)" class="btn btn-primary btn-sm">
              <i class="fas fa-book-open me-1"></i>Read Article
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAppStore } from '../stores/app'
import { useTranslation } from '../composables/useTranslation'
import { api } from '../utils/api'

const appStore = useAppStore()
const { t } = useTranslation()
const articles = ref([])
const loading = ref(false)
const error = ref(null)

const loadNews = async () => {
  loading.value = true
  error.value = null
  
  try {
    const response = await api.get('/news')
    articles.value = response.data.articles || []
  } catch (err) {
    error.value = err.response?.data?.error || 'Failed to load news articles'
  } finally {
    loading.value = false
  }
}

const highlightVocab = (content) => {
  // Simple vocab highlighting - could be enhanced with actual vocab list
  if (!content) return ''
  
  const vocabWords = ['der', 'die', 'das', 'und', 'ist', 'haben', 'werden', 'sein']
  let highlighted = content
  
  vocabWords.forEach(word => {
    const regex = new RegExp(`\\b${word}\\b`, 'gi')
    highlighted = highlighted.replace(regex, `<span class="vocab-word" data-word="${word}">${word}</span>`)
  })
  
  return highlighted
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString()
}

const readArticle = (article) => {
  // Open article in modal or navigate to detail view
  appStore.showAlert('Article opened!', 'success')
}

onMounted(() => {
  loadNews()
})
</script>

<style scoped>
.card {
  transition: transform 0.2s ease-in-out;
}

.card:hover {
  transform: translateY(-2px);
}
</style>
