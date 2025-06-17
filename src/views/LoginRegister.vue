<template>
  <div class="auth-container">
    <div class="row justify-content-center">
      <div class="col-md-6 col-lg-5">
        <div class="card shadow">
          <div class="card-header">
            <ul class="nav nav-tabs card-header-tabs" role="tablist">
              <li class="nav-item" role="presentation">
                <button 
                  class="nav-link" 
                  :class="{ active: activeTab === 'login' }"
                  @click="activeTab = 'login'"
                  type="button"
                >
                  <i class="fas fa-sign-in-alt me-2"></i>{{ t('auth.login') }}
                </button>
              </li>
              <li class="nav-item" role="presentation">
                <button 
                  class="nav-link" 
                  :class="{ active: activeTab === 'register' }"
                  @click="activeTab = 'register'"
                  type="button"
                >
                  <i class="fas fa-user-plus me-2"></i>{{ t('auth.register') }}
                </button>
              </li>
            </ul>
          </div>
          
          <div class="card-body">
            <!-- Login Form -->
            <div v-show="activeTab === 'login'" class="tab-pane">
              <h4 class="mb-4">{{ t('auth.welcomeBack') }}</h4>
              <form @submit.prevent="handleLogin">
                <div class="mb-3">
                  <label for="loginEmail" class="form-label">{{ t('auth.email') }}</label>
                  <input 
                    type="email" 
                    class="form-control" 
                    id="loginEmail" 
                    v-model="loginForm.email"
                    :class="{ 'is-invalid': loginErrors.email }"
                    required
                  >
                  <div v-if="loginErrors.email" class="invalid-feedback">
                    {{ loginErrors.email }}
                  </div>
                </div>
                
                <div class="mb-3">
                  <label for="loginPassword" class="form-label">Password</label>
                  <input 
                    type="password" 
                    class="form-control" 
                    id="loginPassword" 
                    v-model="loginForm.password"
                    :class="{ 'is-invalid': loginErrors.password }"
                    required
                  >
                  <div v-if="loginErrors.password" class="invalid-feedback">
                    {{ loginErrors.password }}
                  </div>
                </div>
                
                <button 
                  type="submit" 
                  class="btn btn-primary w-100 mb-3"
                  :disabled="loginLoading"
                >
                  <span v-if="loginLoading" class="spinner-border spinner-border-sm me-2"></span>
                  {{ loginLoading ? 'Signing in...' : 'Login' }}
                </button>
              </form>
              
              <div class="text-center">
                <button 
                  @click="signInWithGoogle" 
                  class="btn btn-danger w-100"
                  :disabled="googleLoading"
                >
                  <i class="fab fa-google me-2"></i>
                  {{ googleLoading ? 'Signing in...' : 'Sign in with Google' }}
                </button>
              </div>
            </div>
            
            <!-- Register Form -->
            <div v-show="activeTab === 'register'" class="tab-pane">
              <h4 class="mb-4">Create Account</h4>
              <form @submit.prevent="handleRegister">
                <div class="mb-3">
                  <label for="registerUsername" class="form-label">Username</label>
                  <input 
                    type="text" 
                    class="form-control" 
                    id="registerUsername" 
                    v-model="registerForm.username"
                    :class="{ 'is-invalid': registerErrors.username }"
                    required
                  >
                  <div v-if="registerErrors.username" class="invalid-feedback">
                    {{ registerErrors.username }}
                  </div>
                </div>
                
                <div class="mb-3">
                  <label for="registerEmail" class="form-label">Email address</label>
                  <input 
                    type="email" 
                    class="form-control" 
                    id="registerEmail" 
                    v-model="registerForm.email"
                    :class="{ 'is-invalid': registerErrors.email }"
                    required
                  >
                  <div v-if="registerErrors.email" class="invalid-feedback">
                    {{ registerErrors.email }}
                  </div>
                </div>
                
                <div class="mb-3">
                  <label for="registerPassword" class="form-label">Password</label>
                  <input 
                    type="password" 
                    class="form-control" 
                    id="registerPassword" 
                    v-model="registerForm.password"
                    :class="{ 'is-invalid': registerErrors.password }"
                    required
                  >
                  <div v-if="registerErrors.password" class="invalid-feedback">
                    {{ registerErrors.password }}
                  </div>
                </div>
                
                <button 
                  type="submit" 
                  class="btn btn-primary w-100 mb-3"
                  :disabled="registerLoading"
                >
                  <span v-if="registerLoading" class="spinner-border spinner-border-sm me-2"></span>
                  {{ registerLoading ? 'Creating account...' : 'Register' }}
                </button>
              </form>
              
              <div class="text-center">
                <button 
                  @click="signInWithGoogle" 
                  class="btn btn-danger w-100"
                  :disabled="googleLoading"
                >
                  <i class="fab fa-google me-2"></i>
                  {{ googleLoading ? 'Signing up...' : 'Sign up with Google' }}
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
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useAppStore } from '../stores/app'
import { useTranslation } from '../composables/useTranslation'

const router = useRouter()
const authStore = useAuthStore()
const appStore = useAppStore()
const { t } = useTranslation()

const activeTab = ref('login')
const loginLoading = ref(false)
const registerLoading = ref(false)
const googleLoading = ref(false)

const loginForm = reactive({
  email: '',
  password: ''
})

const registerForm = reactive({
  username: '',
  email: '',
  password: ''
})

const loginErrors = reactive({})
const registerErrors = reactive({})

const clearErrors = () => {
  Object.keys(loginErrors).forEach(key => delete loginErrors[key])
  Object.keys(registerErrors).forEach(key => delete registerErrors[key])
}

const handleLogin = async () => {
  clearErrors()
  loginLoading.value = true
  
  try {
    await authStore.login(loginForm.email, loginForm.password)
    appStore.showAlert('Login successful!', 'success')
    router.push('/')
  } catch (error) {
    const errorData = error.response?.data
    if (errorData?.errors) {
      Object.assign(loginErrors, errorData.errors)
    } else {
      appStore.showAlert(errorData?.error || 'Login failed', 'error')
    }
  } finally {
    loginLoading.value = false
  }
}

const handleRegister = async () => {
  clearErrors()
  registerLoading.value = true
  
  try {
    await authStore.register(registerForm.username, registerForm.email, registerForm.password)
    appStore.showAlert('Registration successful!', 'success')
    router.push('/')
  } catch (error) {
    const errorData = error.response?.data
    if (errorData?.errors) {
      Object.assign(registerErrors, errorData.errors)
    } else {
      appStore.showAlert(errorData?.error || 'Registration failed', 'error')
    }
  } finally {
    registerLoading.value = false
  }
}

const signInWithGoogle = async () => {
  googleLoading.value = true
  
  try {
    await authStore.googleSignIn()
    appStore.showAlert('Google sign-in successful!', 'success')
    router.push('/')
  } catch (error) {
    appStore.showAlert(error.message || 'Google sign-in failed', 'error')
  } finally {
    googleLoading.value = false
  }
}
</script>

<style scoped>
.auth-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem 0;
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

.card {
  border: none;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}
</style>
