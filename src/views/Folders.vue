<template>
  <div class="container">
    <!-- Flash messages container -->
    <div v-if="flashMessage" class="flash-messages-container">
      <div :class="['alert', `alert-${flashMessage.type}`, 'alert-dismissible', 'fade', 'show', 'flash-message']" role="alert">
        {{ flashMessage.text }}
        <button type="button" class="btn-close" @click="clearFlashMessage"></button>
      </div>
    </div>

    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1>{{ t('folders.title') }}</h1>
      <button v-if="authStore.isAuthenticated" type="button" class="btn btn-primary" @click="showNewFolderModal">
        <i class="fas fa-plus me-2"></i>{{ t('folders.createNew') }}
      </button>
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
            <i class="fas fa-times"></i>{{ t('folders.clearSearch') }}
          </button>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center my-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-3">Loading folders...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="filteredFolders.length === 0" class="text-center my-5">
      <i class="fas fa-folder-open fa-4x text-muted mb-3"></i>
      <h3>No folders found</h3>
      <p class="text-muted">{{ searchQuery ? t('folders.adjustSearch') : t('folders.createFirst') }}</p>
      <button v-if="authStore.isAuthenticated" class="btn btn-primary" @click="showNewFolderModal">
        <i class="fas fa-plus me-2"></i>{{ t('folders.createFolder') }}
      </button>
    </div>

    <!-- Folders Grid -->
    <div v-else class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4" id="foldersContainer">
      <div v-for="folder in filteredFolders" :key="folder.id" class="col">
        <div class="card h-100">
          <div class="card-body">
            <h5 class="card-title">
              <router-link :to="{ name: 'Folder', params: { id: folder.id } }" class="text-decoration-none">
                {{ folder.name }}
              </router-link>
            </h5>
            <p class="card-text text-muted">{{ folder.description || 'No description' }}</p>
            <div class="d-flex justify-content-between align-items-center">
              <span class="badge bg-primary">
                <i class="fas fa-list me-1"></i>{{ folder.vocabularies ? folder.vocabularies.length : 0 }} terms
              </span>
              <div class="btn-group">
                <router-link v-if="authStore.isAuthenticated" :to="{ name: 'Folder', params: { id: folder.id } }" class="btn btn-sm btn-outline-primary">
                  <i class="fas fa-edit me-1"></i>{{ t('folders.edit') }}
                </router-link>
                <router-link 
                  v-if="folder.vocabularies && folder.vocabularies.length > 0" 
                  :to="{ name: 'Game', params: { id: folder.id } }" 
                  class="btn btn-sm btn-outline-success">
                  <i class="fas fa-gamepad me-1"></i>{{ t('folders.play') }}
                </router-link>
                <button v-if="authStore.isAuthenticated" @click="confirmDeleteFolder(folder.id)" class="btn btn-sm btn-outline-danger">
                  <i class="fas fa-trash"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- New Folder Modal -->
    <div class="modal fade" id="newFolderModal" tabindex="-1" ref="folderModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ isEditing ? t('folders.editFolder') : t('folders.createNewFolder') }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <form @submit.prevent="handleFolderSubmit">
            <div class="modal-body">
              <div class="mb-3">
                <label for="folderName" class="form-label">{{ t('folders.folderName') }}</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="folderName" 
                  v-model="folderForm.name"
                  required
                >
              </div>
              <div class="mb-3">
                <label for="folderDescription" class="form-label">{{ t('folders.folderDescription') }}</label>
                <textarea 
                  class="form-control" 
                  id="folderDescription" 
                  v-model="folderForm.description" 
                  rows="3"
                ></textarea>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">{{ t('folders.cancel') }}</button>
              <button type="submit" class="btn btn-primary" :disabled="folderSubmitting">
                <span v-if="folderSubmitting" class="spinner-border spinner-border-sm me-2"></span>
                {{ isEditing ? t('folders.saveChanges') : t('folders.create') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div class="modal fade" id="deleteFolderModal" tabindex="-1" ref="deleteModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Confirm Delete</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <p>{{ t('folders.confirmDelete') }}</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">{{ t('folders.cancel') }}</button>
            <button 
              @click="deleteFolder" 
              type="button" 
              class="btn btn-danger"
              :disabled="deleteSubmitting">
              {{ deleteSubmitting ? t('folders.deleting') : t('folders.delete') }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted } from 'vue'
import { useTranslation } from '../composables/useTranslation'
import { api } from '../utils/api'
import Modal from 'bootstrap/js/dist/modal'
import { useAuthStore } from '../stores/auth'

const { t } = useTranslation()
const authStore = useAuthStore()

const folders = ref({})
const loading = ref(true)
const folderModal = ref(null)
const deleteModal = ref(null)
const folderSubmitting = ref(false)
const deleteSubmitting = ref(false)
const isEditing = ref(false)
const folderToDeleteId = ref(null)
const flashMessage = ref(null)
const searchQuery = ref('')

const folderForm = reactive({
  name: '',
  description: ''
})

let modalInstance = null
let deleteModalInstance = null

const fetchFolders = async () => {
  loading.value = true
  try {
    const response = await api.get('/folders')
    folders.value = response.data || {}
  } catch (error) {
    showFlashMessage('Failed to load folders. Please try again.', 'danger')
    console.error('Error fetching folders:', error)
  } finally {
    loading.value = false
  }
}

const filteredFolders = computed(() => {
  const allFolders = Object.entries(folders.value).map(([id, folderData]) => ({
    id: id,
    ...folderData
  }));

  if (!searchQuery.value) {
    return allFolders;
  }

  const query = searchQuery.value.toLowerCase();
  return allFolders.filter(folder =>
    folder.name.toLowerCase().includes(query) ||
    (folder.description && folder.description.toLowerCase().includes(query))
  );
});

const showNewFolderModal = () => {
  isEditing.value = false
  folderForm.name = ''
  folderForm.description = ''
  if (!modalInstance) {
    modalInstance = new Modal(folderModal.value)
  }
  modalInstance.show()
}

const handleFolderSubmit = async () => {
  if (!folderForm.name.trim()) {
    showFlashMessage('Folder name is required.', 'danger')
    return
  }
  folderSubmitting.value = true
  try {
    const response = await api.post('/folders', folderForm)
    if (response.data.folder) {
      folders.value[response.data.id] = response.data.folder
      modalInstance.hide()
      showFlashMessage('Folder created successfully!', 'success')
    }
  } catch (error) {
    let errorMsg = 'Failed to create folder.'
    if (error.response?.data?.error === 'already_exists') {
      errorMsg = 'A folder with this name already exists.'
    }
    showFlashMessage(errorMsg, 'danger')
  } finally {
    folderSubmitting.value = false
  }
}

const confirmDeleteFolder = (folderId) => {
  folderToDeleteId.value = folderId
  if (!deleteModalInstance) {
    deleteModalInstance = new Modal(deleteModal.value)
  }
  deleteModalInstance.show()
}

const deleteFolder = async () => {
  if (!folderToDeleteId.value) return
  deleteSubmitting.value = true
  try {
    await api.delete(`/folders/${folderToDeleteId.value}`)
    delete folders.value[folderToDeleteId.value]
    deleteModalInstance.hide()
    showFlashMessage('Folder deleted successfully!', 'success')
  } catch (error) {
    showFlashMessage('Failed to delete folder.', 'danger')
    console.error('Error deleting folder:', error)
  } finally {
    deleteSubmitting.value = false
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

onMounted(() => {
  fetchFolders()
})
</script>

<style scoped>
.flash-messages-container {
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

.card {
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}
</style>
