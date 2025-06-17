<template>
  <div class="folders-section">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>{{ t('folders.title') }}</h2>
      <button @click="showCreateForm = true" class="btn btn-primary">
        <i class="fas fa-plus me-2"></i>{{ t('folders.createNew') }}
      </button>
    </div>

    <!-- Create/Edit Folder Modal -->
    <div v-if="showCreateForm || editingFolder" class="modal d-block" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              {{ editingFolder ? 'Edit Folder' : 'Create New Folder' }}
            </h5>
            <button @click="closeForm" type="button" class="btn-close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveFolder">
              <div class="mb-3">
                <label for="folderName" class="form-label">Folder Name</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="folderName" 
                  v-model="folderForm.name"
                  :class="{ 'is-invalid': formErrors.name }"
                  required
                >
                <div v-if="formErrors.name" class="invalid-feedback">
                  {{ formErrors.name }}
                </div>
              </div>
              
              <div class="mb-3">
                <label for="folderDescription" class="form-label">Description (Optional)</label>
                <textarea 
                  class="form-control" 
                  id="folderDescription" 
                  v-model="folderForm.description"
                  rows="3"
                ></textarea>
              </div>
              
              <div class="d-flex justify-content-end gap-2">
                <button @click="closeForm" type="button" class="btn btn-secondary">Cancel</button>
                <button type="submit" class="btn btn-primary" :disabled="saveLoading">
                  <span v-if="saveLoading" class="spinner-border spinner-border-sm me-2"></span>
                  {{ saveLoading ? 'Saving...' : 'Save Folder' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Search -->
    <div class="row mb-4">
      <div class="col-md-6">
        <div class="input-group">
          <input 
            type="text" 
            class="form-control" 
            placeholder="Search folders..." 
            v-model="searchQuery"
          >
          <button class="btn btn-outline-secondary" @click="searchQuery = ''">
            <i class="fas fa-times"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- Folders Grid -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-2">Loading folders...</p>
    </div>
    
    <div v-else-if="filteredFolders.length === 0" class="text-center py-5">
      <i class="fas fa-folder fa-3x text-muted mb-3"></i>
      <h5>No folders found</h5>
      <p class="text-muted">
        {{ searchQuery ? 'Try adjusting your search.' : 'Create your first vocabulary folder to get started.' }}
      </p>
    </div>
    
    <div v-else class="row">
      <div v-for="folder in filteredFolders" :key="folder.id" class="col-md-4 col-lg-3 mb-4">
        <div class="card folder-card h-100">
          <div class="card-body d-flex flex-column">
            <div class="d-flex justify-content-between align-items-start mb-3">
              <div class="folder-icon">
                <i class="fas fa-folder fa-2x text-primary"></i>
              </div>
              <div class="dropdown">
                <button 
                  class="btn btn-sm btn-outline-secondary dropdown-toggle" 
                  type="button" 
                  :id="`dropdown-${folder.id}`"
                  data-bs-toggle="dropdown"
                >
                  <i class="fas fa-ellipsis-v"></i>
                </button>
                <ul class="dropdown-menu">
                  <li>
                    <button @click="editFolder(folder)" class="dropdown-item">
                      <i class="fas fa-edit me-2"></i>Edit
                    </button>
                  </li>
                  <li>
                    <button @click="confirmDelete(folder)" class="dropdown-item text-danger">
                      <i class="fas fa-trash me-2"></i>Delete
                    </button>
                  </li>
                </ul>
              </div>
            </div>
            
            <h6 class="card-title">{{ folder.name }}</h6>
            <p class="card-text text-muted small mb-3" v-if="folder.description">
              {{ folder.description }}
            </p>
            
            <div class="mt-auto">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <small class="text-muted">
                  <i class="fas fa-book me-1"></i>
                  {{ folder.word_count || 0 }} words
                </small>
                <small class="text-muted">
                  {{ formatDate(folder.created_at) }}
                </small>
              </div>
              
              <button @click="openFolder(folder)" class="btn btn-primary btn-sm w-100">
                <i class="fas fa-folder-open me-2"></i>Open Folder
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Folder Detail Modal -->
    <div v-if="selectedFolder" class="modal d-block" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="fas fa-folder-open me-2"></i>{{ selectedFolder.name }}
            </h5>
            <button @click="selectedFolder = null" type="button" class="btn-close"></button>
          </div>
          <div class="modal-body">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <p class="text-muted mb-0" v-if="selectedFolder.description">
                {{ selectedFolder.description }}
              </p>
              <button @click="showAddWordForm = true" class="btn btn-primary btn-sm">
                <i class="fas fa-plus me-2"></i>Add Word
              </button>
            </div>

            <!-- Add Word Form -->
            <div v-if="showAddWordForm" class="card mb-3">
              <div class="card-body">
                <h6>Add New Word</h6>
                <form @submit.prevent="addWordToFolder">
                  <div class="row">
                    <div class="col-md-6">
                      <div class="mb-3">
                        <label class="form-label">German Word</label>
                        <div class="position-relative">
                          <input 
                            type="text" 
                            class="form-control" 
                            v-model="wordForm.german"
                            required
                          >
                          <GermanCharacterHelper target-input="german" />
                        </div>
                      </div>
                    </div>
                    <div class="col-md-6">
                      <div class="mb-3">
                        <label class="form-label">English Translation</label>
                        <input 
                          type="text" 
                          class="form-control" 
                          v-model="wordForm.english"
                          required
                        >
                      </div>
                    </div>
                  </div>
                  <div class="d-flex justify-content-end gap-2">
                    <button @click="cancelAddWord" type="button" class="btn btn-secondary btn-sm">Cancel</button>
                    <button type="submit" class="btn btn-primary btn-sm" :disabled="addWordLoading">
                      {{ addWordLoading ? 'Adding...' : 'Add Word' }}
                    </button>
                  </div>
                </form>
              </div>
            </div>

            <!-- Folder Words -->
            <div v-if="folderWords.length === 0" class="text-center py-4">
              <i class="fas fa-book fa-2x text-muted mb-2"></i>
              <p class="text-muted">No words in this folder yet.</p>
            </div>
            
            <div v-else class="folder-words">
              <div v-for="word in folderWords" :key="word.id" class="word-item mb-2">
                <div class="card">
                  <div class="card-body py-2">
                    <div class="row align-items-center">
                      <div class="col-md-4">
                        <strong>{{ word.german }}</strong>
                      </div>
                      <div class="col-md-6">
                        {{ word.english }}
                      </div>
                      <div class="col-md-2 text-end">
                        <button 
                          @click="removeWordFromFolder(word)"
                          class="btn btn-sm btn-outline-danger"
                          title="Remove from folder"
                        >
                          <i class="fas fa-times"></i>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useAppStore } from '../stores/app'
import { useTranslation } from '../composables/useTranslation'
import { api } from '../utils/api'
import GermanCharacterHelper from '../components/GermanCharacterHelper.vue'

const appStore = useAppStore()
const { t } = useTranslation()

// Data
const folders = ref([])
const loading = ref(false)
const showCreateForm = ref(false)
const editingFolder = ref(null)
const saveLoading = ref(false)
const searchQuery = ref('')

// Folder detail
const selectedFolder = ref(null)
const folderWords = ref([])
const showAddWordForm = ref(false)
const addWordLoading = ref(false)

// Forms
const folderForm = reactive({
  name: '',
  description: ''
})

const wordForm = reactive({
  german: '',
  english: ''
})

const formErrors = reactive({})

// Computed
const filteredFolders = computed(() => {
  if (!searchQuery.value) return folders.value
  
  const query = searchQuery.value.toLowerCase()
  return folders.value.filter(folder => 
    folder.name.toLowerCase().includes(query) ||
    (folder.description && folder.description.toLowerCase().includes(query))
  )
})

// Methods
const loadFolders = async () => {
  loading.value = true
  
  try {
    const response = await api.get('/api/folders')
    folders.value = response.data.folders || []
  } catch (error) {
    appStore.showAlert(error.response?.data?.error || 'Failed to load folders', 'error')
  } finally {
    loading.value = false
  }
}

const saveFolder = async () => {
  clearFormErrors()
  saveLoading.value = true
  
  try {
    if (editingFolder.value) {
      await api.put(`/api/folders/${editingFolder.value.id}`, folderForm)
      appStore.showAlert('Folder updated successfully!', 'success')
    } else {
      await api.post('/api/folders', folderForm)
      appStore.showAlert('Folder created successfully!', 'success')
    }
    
    closeForm()
    loadFolders()
  } catch (error) {
    const errorData = error.response?.data
    if (errorData?.errors) {
      Object.assign(formErrors, errorData.errors)
    } else {
      appStore.showAlert(errorData?.error || 'Failed to save folder', 'error')
    }
  } finally {
    saveLoading.value = false
  }
}

const editFolder = (folder) => {
  editingFolder.value = folder
  Object.assign(folderForm, {
    name: folder.name,
    description: folder.description || ''
  })
}

const confirmDelete = (folder) => {
  if (confirm(`Are you sure you want to delete "${folder.name}"? This will also remove all words in this folder.`)) {
    deleteFolder(folder)
  }
}

const deleteFolder = async (folder) => {
  try {
    await api.delete(`/api/folders/${folder.id}`)
    appStore.showAlert('Folder deleted successfully!', 'success')
    loadFolders()
  } catch (error) {
    appStore.showAlert(error.response?.data?.error || 'Failed to delete folder', 'error')
  }
}

const openFolder = async (folder) => {
  selectedFolder.value = folder
  
  try {
    const response = await api.get(`/api/folders/${folder.id}/words`)
    folderWords.value = response.data.words || []
  } catch (error) {
    appStore.showAlert('Failed to load folder words', 'error')
  }
}

const addWordToFolder = async () => {
  addWordLoading.value = true
  
  try {
    await api.post(`/api/folders/${selectedFolder.value.id}/words`, wordForm)
    appStore.showAlert('Word added to folder!', 'success')
    
    // Refresh folder words
    const response = await api.get(`/api/folders/${selectedFolder.value.id}/words`)
    folderWords.value = response.data.words || []
    
    cancelAddWord()
  } catch (error) {
    appStore.showAlert(error.response?.data?.error || 'Failed to add word', 'error')
  } finally {
    addWordLoading.value = false
  }
}

const removeWordFromFolder = async (word) => {
  if (confirm(`Remove "${word.german}" from this folder?`)) {
    try {
      await api.delete(`/api/folders/${selectedFolder.value.id}/words/${word.id}`)
      appStore.showAlert('Word removed from folder!', 'success')
      
      // Remove from local array
      folderWords.value = folderWords.value.filter(w => w.id !== word.id)
    } catch (error) {
      appStore.showAlert('Failed to remove word', 'error')
    }
  }
}

const closeForm = () => {
  showCreateForm.value = false
  editingFolder.value = null
  clearFormErrors()
  Object.assign(folderForm, {
    name: '',
    description: ''
  })
}

const cancelAddWord = () => {
  showAddWordForm.value = false
  Object.assign(wordForm, {
    german: '',
    english: ''
  })
}

const clearFormErrors = () => {
  Object.keys(formErrors).forEach(key => delete formErrors[key])
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString()
}

onMounted(() => {
  loadFolders()
})
</script>

<style scoped>
.folder-card {
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
  cursor: pointer;
}

.folder-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.folder-icon {
  opacity: 0.8;
}

.word-item .card {
  border-left: 3px solid #667eea;
}

.modal {
  background-color: rgba(0, 0, 0, 0.5);
}
</style>
