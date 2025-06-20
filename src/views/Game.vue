<template>
  <div class="container">
    <!-- Flash messages -->
    <div v-if="flashMessage" class="flash-message-container">
      <div :class="['alert', `alert-${flashMessage.type}`, 'alert-dismissible', 'fade', 'show', 'flash-message']" role="alert">
        {{ flashMessage.text }}
        <button type="button" class="btn-close" @click="clearFlashMessage"></button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center my-5">
      <div class="spinner-border text-primary" role="status">      <span class="visually-hidden">{{ t('common.loading') }}</span>
      </div>
      <p class="mt-3">{{ t('game.loading') }}</p>
    </div>
    
    <!-- Game Selection -->
    <div v-else-if="gameState === 'selection'" id="gameSelection" class="row mb-4">
      <div class="col-12">        <div class="d-flex justify-content-between align-items-center mb-4">
          <h1>{{ folder.name }} - {{ t('game.title') }}</h1>
          <router-link :to="{ name: 'Folder', params: { id } }" class="btn btn-secondary">
            <i class="fas fa-arrow-left me-2"></i>{{ t('game.backToFolder') }}
          </router-link>
        </div>
        
        <h2 class="mb-4">{{ t('game.chooseGame') }}</h2>
        <div class="row">
          <div class="col-md-6 mb-3">
            <div class="card h-100">
              <div class="card-body text-center">                <i class="fas fa-question-circle fa-4x text-primary mb-3"></i>
                <h4>{{ t('game.defQuiz') }}</h4>
                <p class="card-text">{{ t('game.defQuizDesc') }}</p>
                <div class="mb-3">
                  <div class="form-floating">
                    <select class="form-select" id="quizQuestionCount" v-model="quizSettings.questionCount">
                      <option v-for="n in 10" :key="`quiz-${n}`" :value="n">{{ n }}</option>
                    </select>
                    <label for="quizQuestionCount">{{ t('game.numQuestions') }}</label>
                  </div>
                </div>
                <button class="btn btn-primary" @click="startQuiz" :disabled="!hasEnoughWords">
                  <i class="fas fa-play me-2"></i>{{ t('game.startQuiz') }}
                </button>
              </div>
            </div>
          </div>
          
          <div class="col-md-6 mb-3">
            <div class="card h-100">
              <div class="card-body text-center">                <i class="fas fa-list-ul fa-4x text-success mb-3"></i>
                <h4>{{ t('game.multiChoice') }}</h4>
                <p class="card-text">{{ t('game.multiChoiceDesc') }}</p>
                <div class="mb-3">
                  <div class="form-floating">
                    <select class="form-select" id="mcQuestionCount" v-model="mcSettings.questionCount">
                      <option v-for="n in 10" :key="`mc-${n}`" :value="n">{{ n }}</option>
                    </select>
                    <label for="mcQuestionCount">{{ t('game.numQuestions') }}</label>
                  </div>
                </div>
                <button 
                  class="btn btn-success" 
                  @click="startMultipleChoice" 
                  :disabled="vocabularyCount < 4"
                >
                  <i class="fas fa-play me-2"></i>{{ t('game.startGame') }}
                </button>
                <small v-if="vocabularyCount < 4" class="text-muted d-block mt-2">
                  {{ t('game.minVocab') }}
                </small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Quiz Game -->
    <div v-else-if="gameState === 'quiz'" id="quizGame" class="row">
      <div class="col-12">        <div class="d-flex justify-content-between align-items-center mb-4">
          <h2>{{ t('game.defQuiz') }}</h2>
          <button class="btn btn-secondary" @click="endGame">
            <i class="fas fa-times me-2"></i>{{ t('game.endGame') }}
          </button>
        </div>
        
        <div class="progress mb-4">
          <div 
            id="quizProgress" 
            class="progress-bar" 
            role="progressbar" 
            :style="`width: ${(currentQuestionIndex / gameData.questions.length) * 100}%`"
          ></div>
        </div>

        <div v-if="!showingResult" id="quizQuestion" class="card">
          <div class="card-body">
            <div class="text-center mb-4">
              <h4 id="quizQuestionText">{{ currentQuestion.question }}</h4>
              <div v-if="currentQuestion.audio_url" id="quizAudioContainer" class="mt-2">                <button class="btn btn-outline-primary" id="playQuizAudio" @click="playAudio(currentQuestion.audio_url)">
                  <i class="fas fa-volume-up me-2"></i>{{ t('game.playPronunciation') }}
                </button>
              </div>
            </div>
            <div class="mb-3">              <label for="quizAnswer" class="form-label">{{ t('game.yourAnswer') }}</label>
              <textarea 
                class="form-control" 
                id="quizAnswer" 
                v-model="userAnswer" 
                rows="3" 
                :placeholder="t('game.enterDefinition')"
                @keydown.enter="submitQuizAnswer"
              ></textarea>
            </div>
            <div class="text-center">
              <button class="btn btn-primary" id="submitQuizAnswer" @click="submitQuizAnswer">
                <i class="fas fa-check me-2"></i>{{ t('game.submitAnswer') }}
              </button>
            </div>
          </div>
        </div>

        <div v-else id="quizResult" class="card mt-3">
          <div class="card-body">            <h5 id="quizResultTitle" class="mb-3">
              <span v-if="isCorrect" class="text-success">
                <i class="fas fa-check-circle me-2"></i>{{ t('game.correct') }}
              </span>
              <span v-else class="text-danger">
                <i class="fas fa-times-circle me-2"></i>{{ t('game.notQuite') }}
              </span>
            </h5>
            <p><strong>{{ t('game.correctAnswer') }}</strong> <span id="quizCorrectAnswer">{{ currentQuestion.correct_answer }}</span></p>
            <p><strong>{{ t('game.yourAnswerLabel') }}</strong> <span id="quizUserAnswer">{{ userAnswer }}</span></p>
            <button class="btn btn-primary" id="nextQuizQuestion" @click="nextQuestion">
              <i class="fas fa-arrow-right me-2"></i>{{ t('game.nextQuestion') }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Multiple Choice Game -->
    <div v-else-if="gameState === 'multipleChoice'" id="mcGame" class="row">
      <div class="col-12">        <div class="d-flex justify-content-between align-items-center mb-4">
          <h2>{{ t('game.multiChoice') }}</h2>
          <button class="btn btn-secondary" @click="endGame">
            <i class="fas fa-times me-2"></i>{{ t('game.endGame') }}
          </button>
        </div>
        
        <div class="progress mb-4">
          <div 
            id="mcProgress" 
            class="progress-bar" 
            role="progressbar" 
            :style="`width: ${(currentQuestionIndex / gameData.questions.length) * 100}%`"
          ></div>
        </div>

        <div v-if="!showingResult" id="mcQuestion" class="card">
          <div class="card-body">
            <div class="text-center mb-4">
              <h4 id="mcQuestionText">{{ currentQuestion.question }}</h4>
              <div v-if="currentQuestion.audio_url" id="mcAudioContainer" class="mt-2">                <button class="btn btn-outline-primary" id="playMcAudio" @click="playAudio(currentQuestion.audio_url)">
                  <i class="fas fa-volume-up me-2"></i>{{ t('game.playPronunciation') }}
                </button>
              </div>
            </div>
            <div id="mcChoices" class="d-grid gap-2">
              <button 
                v-for="(choice, index) in currentQuestion.choices" 
                :key="index"
                class="btn btn-outline-primary text-start p-3"
                @click="submitMcAnswer(index)"
              >
                {{ index + 1 }}. {{ choice }}
              </button>
            </div>
          </div>
        </div>

        <div v-else id="mcResult" class="card mt-3">
          <div class="card-body">            <h5 id="mcResultTitle" class="mb-3">
              <span v-if="isCorrect" class="text-success">
                <i class="fas fa-check-circle me-2"></i>{{ t('game.correct') }}
              </span>
              <span v-else class="text-danger">
                <i class="fas fa-times-circle me-2"></i>{{ t('game.incorrect') }}
              </span>
            </h5>            <p><strong>{{ t('game.correctAnswer') }}</strong> <span id="mcCorrectAnswer">
              {{ currentQuestion.choices[currentQuestion.correct_index] }}
            </span></p>
            <p><strong>{{ t('game.yourAnswerLabel') }}</strong> <span id="mcUserAnswer">
              {{ selectedAnswer !== null ? currentQuestion.choices[selectedAnswer] : t('game.noAnswer') }}
            </span></p>
            <button class="btn btn-primary" id="nextMcQuestion" @click="nextQuestion">
              <i class="fas fa-arrow-right me-2"></i>{{ t('game.nextQuestion') }}
            </button>
          </div>
        </div>
      </div>
    </div>    <!-- Game Results -->
    <div v-else-if="gameState === 'results'" id="gameResults" class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-body text-center">
            <i class="fas fa-trophy fa-4x text-warning mb-3"></i>
            <h2>{{ t('game.gameComplete') }}</h2>
            <h3 id="finalScore" class="text-primary">
              {{ t('game.yourScore') }} {{ gameScore }} / {{ gameData.questions.length }}
            </h3>
            <p id="finalMessage" class="text-muted mb-4">
              {{ getFinalMessage() }}
            </p>
              <!-- Question Results Summary -->
            <div class="question-results mb-4">
              <h4 class="mb-3">{{ t('game.questionSummary') }}</h4>
              <div class="accordion" id="questionResultsAccordion">
                <div v-for="(result, index) in questionResults" :key="index" class="accordion-item">
                  <h2 class="accordion-header">                      <button 
                      class="accordion-button collapsed" 
                      :class="{'bg-success bg-opacity-10': result.isCorrect, 'bg-danger bg-opacity-10': !result.isCorrect}"
                      type="button" 
                      data-bs-toggle="collapse" 
                      :data-bs-target="'#questionResult' + index"
                      @click="toggleAccordion(index)"
                    >
                      <i :class="result.isCorrect ? 'fas fa-check-circle text-success me-2' : 'fas fa-times-circle text-danger me-2'"></i>
                      {{ t('game.question') }} {{ index + 1 }}: {{ result.question }}
                    </button>
                  </h2>
                  <div :id="'questionResult' + index" class="accordion-collapse collapse" data-bs-parent="#questionResultsAccordion">
                    <div class="accordion-body">
                      <div class="row">
                        <div class="col-md-6">
                          <div class="mb-3">
                            <strong>{{ t('game.correctAnswer') }}</strong>
                            <div class="p-2 border rounded mt-1">{{ result.correctAnswer }}</div>
                          </div>
                        </div>
                        <div class="col-md-6">
                          <div class="mb-3">
                            <strong>{{ t('game.yourAnswerLabel') }}</strong>
                            <div 
                              class="p-2 border rounded mt-1" 
                              :class="{'border-success': result.isCorrect, 'border-danger': !result.isCorrect}"
                            >
                              {{ result.userAnswer || t('game.noAnswer') }}
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="btn-group">
              <button class="btn btn-primary" @click="gameState = 'selection'">
                <i class="fas fa-redo me-2"></i>{{ t('game.playAgain') }}
              </button>
              <router-link :to="{ name: 'Folder', params: { id } }" class="btn btn-secondary">
                <i class="fas fa-arrow-left me-2"></i>{{ t('game.backToFolder') }}
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useRoute } from 'vue-router'
import { api } from '../utils/api'
import { useTranslation } from '../composables/useTranslation'
import { Collapse } from 'bootstrap'

const route = useRoute()
const id = route.params.id
const { t } = useTranslation()

// States
const loading = ref(true)
const folder = ref({})
const gameState = ref('selection')
const gameData = ref({ questions: [] })
const currentQuestionIndex = ref(0)
const userAnswer = ref('')
const selectedAnswer = ref(null)
const showingResult = ref(false)
const isCorrect = ref(false)
const gameScore = ref(0)
const currentAudio = ref(null)
const flashMessage = ref(null)
const questionResults = ref([]) // Track results for each question

// Settings
const quizSettings = ref({
  questionCount: 5
})

const mcSettings = ref({
  questionCount: 5
})

// Computed properties
const vocabularyCount = computed(() => {
  return folder.value.vocabularies?.length || 0
})

const hasEnoughWords = computed(() => {
  return vocabularyCount.value > 0
})

const currentQuestion = computed(() => {
  if (!gameData.value.questions || gameData.value.questions.length === 0) {
    return {}
  }
  return gameData.value.questions[currentQuestionIndex.value] || {}
})

// Methods
const fetchFolder = async () => {
  loading.value = true
  try {
    const response = await api.get(`/folders/${id}`)
    folder.value = response.data
  } catch (error) {
    showFlashMessage('Failed to load folder data.', 'danger')
    console.error('Error fetching folder:', error)
  } finally {
    loading.value = false
  }
}

const startQuiz = async () => {
  try {
    loading.value = true
    const response = await api.post(`/folders/${id}/generate-quiz`, {
      question_count: quizSettings.value.questionCount
    })
    
    gameData.value = response.data
    currentQuestionIndex.value = 0
    gameScore.value = 0
    gameState.value = 'quiz'
    showingResult.value = false
    userAnswer.value = ''
    questionResults.value = [] // Reset question results
  } catch (error) {
    showFlashMessage('Failed to start quiz.', 'danger')
    console.error('Error starting quiz:', error)
  } finally {
    loading.value = false
  }
}

const startMultipleChoice = async () => {
  if (vocabularyCount.value < 4) {
    showFlashMessage('You need at least 4 vocabulary words for multiple choice.', 'warning')
    return
  }
  
  try {
    loading.value = true
    const response = await api.post(`/folders/${id}/generate-multiple-choice`, {
      question_count: mcSettings.value.questionCount
    })
    
    gameData.value = response.data
    currentQuestionIndex.value = 0
    gameScore.value = 0
    gameState.value = 'multipleChoice'
    showingResult.value = false
    selectedAnswer.value = null
    questionResults.value = [] // Reset question results
  } catch (error) {
    showFlashMessage('Failed to start multiple choice game.', 'danger')
    console.error('Error starting multiple choice:', error)
  } finally {
    loading.value = false
  }
}

const submitQuizAnswer = () => {
  if (showingResult.value) return
  
  // Simple check for similarity - could be improved
  const correctAnswer = currentQuestion.value.correct_answer.toLowerCase().trim()
  const userSubmitted = userAnswer.value.toLowerCase().trim()
  
  // Check if the answer is correct (simple check)
  isCorrect.value = userSubmitted === correctAnswer || 
                  correctAnswer.includes(userSubmitted) || 
                  userSubmitted.includes(correctAnswer)
  
  if (isCorrect.value) {
    gameScore.value++
  }
  
  // Store the result for this question
  questionResults.value.push({
    question: currentQuestion.value.question,
    userAnswer: userAnswer.value,
    correctAnswer: currentQuestion.value.correct_answer,
    isCorrect: isCorrect.value
  })
  
  showingResult.value = true
}

const submitMcAnswer = (index) => {
  if (showingResult.value) return
  
  selectedAnswer.value = index
  isCorrect.value = index === currentQuestion.value.correct_index
  
  if (isCorrect.value) {
    gameScore.value++
  }
  
  // Store the result for this question
  questionResults.value.push({
    question: currentQuestion.value.question,
    userAnswer: currentQuestion.value.choices[index],
    correctAnswer: currentQuestion.value.choices[currentQuestion.value.correct_index],
    isCorrect: isCorrect.value
  })
  
  showingResult.value = true
}

const nextQuestion = () => {
  showingResult.value = false
  userAnswer.value = ''
  selectedAnswer.value = null
  
  if (currentQuestionIndex.value < gameData.value.questions.length - 1) {
    currentQuestionIndex.value++
  } else {
    // Game is over
    gameState.value = 'results'
    // Initialize accordion when showing results
    initializeAccordion()
  }
}

const endGame = () => {
  gameState.value = 'selection'
}

const playAudio = (url) => {
  if (currentAudio.value) {
    currentAudio.value.pause()
  }
  
  currentAudio.value = new Audio(url)
  currentAudio.value.play()
}

const initializeAccordion = () => {
  if (gameState.value === 'results') {
    nextTick(() => {
      // Initialize all Bootstrap collapse elements
      const accordionItems = document.querySelectorAll('.accordion-collapse')
      accordionItems.forEach(item => {
        new Collapse(item, { toggle: false })
      })
    })
  }
}

const getFinalMessage = () => {
  const totalQuestions = gameData.value.questions.length
  const percentage = (gameScore.value / totalQuestions) * 100
  
  if (percentage === 100) {
    return t('game.perfectScore')
  } else if (percentage >= 80) {
    return t('game.greatJob')
  } else if (percentage >= 60) {
    return t('game.goodWork')
  } else if (percentage >= 40) {
    return t('game.niceEffort')
  } else {
    return t('game.keepPracticing')
  }
}

const showFlashMessage = (text, type = 'info') => {
  flashMessage.value = { text, type }
  setTimeout(() => {
    clearFlashMessage()
  }, 5000)
}

const clearFlashMessage = () => {
  flashMessage.value = null
}

// Load folder data on component mount
onMounted(() => {
  fetchFolder()
  
  // Add event listener for keyboard shortcuts
  document.addEventListener('keydown', handleKeydown)
  
  // Clean up event listener on unmount
  return () => {
    document.removeEventListener('keydown', handleKeydown)
    
    // Stop audio if playing
    if (currentAudio.value) {
      currentAudio.value.pause()
      currentAudio.value = null
    }
  }
})

watch(gameState, (newValue) => {
  if (newValue === 'results') {
    initializeAccordion()
  }
})

const handleKeydown = (e) => {
  if (gameState.value === 'multipleChoice' && !showingResult.value) {
    // Allow number keys 1-4 for multiple choice
    const num = parseInt(e.key)
    if (num >= 1 && num <= currentQuestion.value.choices.length) {
      submitMcAnswer(num - 1)
    }
  } else if (showingResult.value && e.key === 'Enter') {
    // Enter to proceed to next question when viewing result
    nextQuestion()
  }
}

// Function to manually toggle accordion collapse
const toggleAccordion = (index) => {
  const collapseElement = document.getElementById(`questionResult${index}`)
  if (collapseElement) {
    const bsCollapse = Collapse.getInstance(collapseElement) || new Collapse(collapseElement, { toggle: false })
    bsCollapse.toggle()
  }
}
</script>

<style scoped>
.flash-message-container {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 9999;
  width: auto;
  min-width: 300px;
  max-width: 80%;
}

.flash-message {
  text-align: center;
  margin-bottom: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  animation: fadeInOut 5s forwards;
}

@keyframes fadeInOut {
  0% { opacity: 0; transform: translateY(-20px); }
  10% { opacity: 1; transform: translateY(0); }
  90% { opacity: 1; transform: translateY(0); }
  100% { opacity: 0; transform: translateY(-20px); }
}

.progress {
  height: 10px;
}

#mcChoices .btn {
  position: relative;
}

#mcChoices .btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.card:hover {
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.question-results {
  max-width: 800px;
  margin: 0 auto;
}

.accordion-button:not(.collapsed) {
  color: var(--bs-body-color);
}

.accordion-button.bg-success.bg-opacity-10:not(.collapsed) {
  background-color: rgba(var(--bs-success-rgb), 0.2) !important;
}

.accordion-button.bg-danger.bg-opacity-10:not(.collapsed) {
  background-color: rgba(var(--bs-danger-rgb), 0.2) !important;
}

.accordion-button:focus {
  box-shadow: none;
}
</style>
