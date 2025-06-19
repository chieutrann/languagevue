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
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-3">Loading games...</p>
    </div>
    
    <!-- Game Selection -->
    <div v-else-if="gameState === 'selection'" id="gameSelection" class="row mb-4">
      <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h1>{{ folder.name }} - Games</h1>
          <router-link :to="{ name: 'Folder', params: { id } }" class="btn btn-secondary">
            <i class="fas fa-arrow-left me-2"></i>Back to Folder
          </router-link>
        </div>
        
        <h2 class="mb-4">Choose a Game</h2>
        <div class="row">
          <div class="col-md-6 mb-3">
            <div class="card h-100">
              <div class="card-body text-center">
                <i class="fas fa-question-circle fa-4x text-primary mb-3"></i>
                <h4>Definition Quiz</h4>
                <p class="card-text">Test your knowledge by providing definitions for words</p>
                <div class="mb-3">
                  <div class="form-floating">
                    <select class="form-select" id="quizQuestionCount" v-model="quizSettings.questionCount">
                      <option v-for="n in 10" :key="`quiz-${n}`" :value="n">{{ n }}</option>
                    </select>
                    <label for="quizQuestionCount">Number of Questions</label>
                  </div>
                </div>
                <button class="btn btn-primary" @click="startQuiz" :disabled="!hasEnoughWords">
                  <i class="fas fa-play me-2"></i>Start Quiz
                </button>
              </div>
            </div>
          </div>
          
          <div class="col-md-6 mb-3">
            <div class="card h-100">
              <div class="card-body text-center">
                <i class="fas fa-list-ul fa-4x text-success mb-3"></i>
                <h4>Multiple Choice</h4>
                <p class="card-text">Choose the correct definition from multiple options</p>
                <div class="mb-3">
                  <div class="form-floating">
                    <select class="form-select" id="mcQuestionCount" v-model="mcSettings.questionCount">
                      <option v-for="n in 10" :key="`mc-${n}`" :value="n">{{ n }}</option>
                    </select>
                    <label for="mcQuestionCount">Number of Questions</label>
                  </div>
                </div>
                <button 
                  class="btn btn-success" 
                  @click="startMultipleChoice" 
                  :disabled="vocabularyCount < 4"
                >
                  <i class="fas fa-play me-2"></i>Start Game
                </button>
                <small v-if="vocabularyCount < 4" class="text-muted d-block mt-2">
                  At least 4 vocabularies required
                </small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Quiz Game -->
    <div v-else-if="gameState === 'quiz'" id="quizGame" class="row">
      <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h2>Definition Quiz</h2>
          <button class="btn btn-secondary" @click="endGame">
            <i class="fas fa-times me-2"></i>End Game
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
              <div v-if="currentQuestion.audio_url" id="quizAudioContainer" class="mt-2">
                <button class="btn btn-outline-primary" id="playQuizAudio" @click="playAudio(currentQuestion.audio_url)">
                  <i class="fas fa-volume-up me-2"></i>Play Pronunciation
                </button>
              </div>
            </div>
            <div class="mb-3">
              <label for="quizAnswer" class="form-label">Your Answer:</label>
              <textarea 
                class="form-control" 
                id="quizAnswer" 
                v-model="userAnswer" 
                rows="3" 
                placeholder="Enter the definition..."
                @keydown.enter="submitQuizAnswer"
              ></textarea>
            </div>
            <div class="text-center">
              <button class="btn btn-primary" id="submitQuizAnswer" @click="submitQuizAnswer">
                <i class="fas fa-check me-2"></i>Submit Answer
              </button>
            </div>
          </div>
        </div>

        <div v-else id="quizResult" class="card mt-3">
          <div class="card-body">
            <h5 id="quizResultTitle" class="mb-3">
              <span v-if="isCorrect" class="text-success">
                <i class="fas fa-check-circle me-2"></i>Correct!
              </span>
              <span v-else class="text-danger">
                <i class="fas fa-times-circle me-2"></i>Not Quite
              </span>
            </h5>
            <p><strong>Correct Answer:</strong> <span id="quizCorrectAnswer">{{ currentQuestion.correct_answer }}</span></p>
            <p><strong>Your Answer:</strong> <span id="quizUserAnswer">{{ userAnswer }}</span></p>
            <button class="btn btn-primary" id="nextQuizQuestion" @click="nextQuestion">
              <i class="fas fa-arrow-right me-2"></i>Next Question
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Multiple Choice Game -->
    <div v-else-if="gameState === 'multipleChoice'" id="mcGame" class="row">
      <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h2>Multiple Choice</h2>
          <button class="btn btn-secondary" @click="endGame">
            <i class="fas fa-times me-2"></i>End Game
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
              <div v-if="currentQuestion.audio_url" id="mcAudioContainer" class="mt-2">
                <button class="btn btn-outline-primary" id="playMcAudio" @click="playAudio(currentQuestion.audio_url)">
                  <i class="fas fa-volume-up me-2"></i>Play Pronunciation
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
          <div class="card-body">
            <h5 id="mcResultTitle" class="mb-3">
              <span v-if="isCorrect" class="text-success">
                <i class="fas fa-check-circle me-2"></i>Correct!
              </span>
              <span v-else class="text-danger">
                <i class="fas fa-times-circle me-2"></i>Incorrect
              </span>
            </h5>
            <p><strong>Correct Answer:</strong> <span id="mcCorrectAnswer">
              {{ currentQuestion.choices[currentQuestion.correct_index] }}
            </span></p>
            <p><strong>Your Answer:</strong> <span id="mcUserAnswer">
              {{ selectedAnswer !== null ? currentQuestion.choices[selectedAnswer] : 'No answer' }}
            </span></p>
            <button class="btn btn-primary" id="nextMcQuestion" @click="nextQuestion">
              <i class="fas fa-arrow-right me-2"></i>Next Question
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Game Results -->
    <div v-else-if="gameState === 'results'" id="gameResults" class="row">
      <div class="col-12">
        <div class="card text-center">
          <div class="card-body">
            <i class="fas fa-trophy fa-4x text-warning mb-3"></i>
            <h2>Game Complete!</h2>
            <h3 id="finalScore" class="text-primary">
              Your Score: {{ gameScore }} / {{ gameData.questions.length }}
            </h3>
            <p id="finalMessage" class="text-muted mb-4">
              {{ getFinalMessage() }}
            </p>
            <div class="btn-group">
              <button class="btn btn-primary" @click="gameState = 'selection'">
                <i class="fas fa-redo me-2"></i>Play Again
              </button>
              <router-link :to="{ name: 'Folder', params: { id } }" class="btn btn-secondary">
                <i class="fas fa-arrow-left me-2"></i>Back to Folder
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { api } from '../utils/api'

const route = useRoute()
const id = route.params.id

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
  
  showingResult.value = true
}

const submitMcAnswer = (index) => {
  if (showingResult.value) return
  
  selectedAnswer.value = index
  isCorrect.value = index === currentQuestion.value.correct_index
  
  if (isCorrect.value) {
    gameScore.value++
  }
  
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

const getFinalMessage = () => {
  const totalQuestions = gameData.value.questions.length
  const percentage = (gameScore.value / totalQuestions) * 100
  
  if (percentage === 100) {
    return 'Perfect score! Amazing job!'
  } else if (percentage >= 80) {
    return 'Great job! You really know these words!'
  } else if (percentage >= 60) {
    return 'Good work! Keep practicing!'
  } else if (percentage >= 40) {
    return 'Nice effort! Try reviewing the words again.'
  } else {
    return 'Keep practicing! You\'ll get better with time.'
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
</style>
