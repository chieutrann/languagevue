<template>
  <div class="container mt-4">

    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>
    <div v-else>
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h1 class="h2">{{ folder.name }}</h1>
        <div>
          <button id="saveAllBtn" class="btn btn-primary me-2" @click="saveAllVocabularies" v-if="isDirty">
            <i class="fas fa-save me-2"></i>{{ t('folder.saveAll') }}
          </button>
          <button id="addVocabularyBtn" class="btn btn-success" @click="addNewVocabulary">
            <i class="fas fa-plus me-2"></i>{{ t('folder.addVocabulary') }}
          </button>
                <router-link 
                  v-if="folder.vocabularies && folder.vocabularies.length > 0" 
                  :to="{ name: 'Game', params: { id: folder.id } }" 
                  class="btn btn-sm btn-outline-success">
                  <i class="fas fa-gamepad me-1"></i>{{ t('folders.play') }}
                </router-link>

        </div>
      </div>
      <p>{{ folder.description }}</p>

      <div class="vocabulary-list">
        <div v-if="vocabularies.length === 0 && !isDirty" id="emptyState" class="text-center p-5 border rounded">
            <h2>This folder is empty</h2>
            <p>Add your first vocabulary word by clicking the "Add Vocabulary" button.</p>
        </div>
        <div v-for="(vocab, index) in vocabularies" :key="vocab.id || `new-${index}`" class="vocabulary-item" :data-vocab-id="vocab.id">
          <div class="row align-items-center">
            <div class="col-auto">
              <span class="vocabulary-number">{{ index + 1 }}</span>
            </div>
            <div class="col-2">
                <div class="image-placeholder" @click="showImageSearchModal(vocab)">
                    <img v-if="vocab.image_url" :src="vocab.image_url" class="img-fluid rounded" alt="Vocabulary image">
                    <i v-else class="fas fa-image"></i>
                </div>
            </div>
            <div class="col">
              <input type="text" class="form-control term-input" v-model="vocab.word" @focus="makeEditable($event, vocab)" @input="markAsModified(vocab)" :readonly="!vocab.isNew" placeholder="Term">
            </div>
            <div class="col">
              
              <input type="text" class="form-control definition-input" v-model="vocab.definition" @focus="makeEditable($event, vocab)" @input="markAsModified(vocab)" :readonly="!vocab.isNew" placeholder="Definition">
            </div>
            <div class="col-auto">
                <button class="btn btn-sm btn-outline-info me-1" @click="searchAudio(vocab)" title="Search for audio">
                  <i class="fas fa-volume-up"></i>{{ t('folder.searchAudio') }}
                </button>
                <button v-if="vocab.audio_url" class="btn btn-sm btn-outline-success me-1" @click="playAudio(vocab.audio_url)" title="Play audio">
                  <i class="fas fa-play"></i>{{ t('folder.playAudio') }}
                </button>
                <button class="btn btn-sm btn-outline-danger delete-vocabulary" @click="confirmDeleteVocabulary(vocab, index)">
                  <i class="fas fa-trash"></i>{{ t('folder.deleteVocabulary') }}
                </button>
            </div>
          </div>
        </div>
        <div ref="bottomRef"></div>
      </div>

      <div class="mt-3 d-flex justify-content-between" v-if="vocabularies.length > 0">
        <button class="btn btn-secondary" @click="switchAllTermsAndDefinitions">
          <i class="fas fa-exchange-alt me-2"></i>{{ t('folder.switchAll') }}
        </button>

        <button id="saveAllBtn" class="btn btn-primary me-2" @click="saveAllVocabularies" v-if="isDirty">
            <i class="fas fa-save me-2"></i>{{ t('folder.saveAll') }}
          </button>
        <button id="addMoreVocabularyBtn" class="btn btn-success" @click="addNewVocabulary">
          <i class="fas fa-plus me-2"></i>{{ t('folder.addMore') }}
        </button>
      </div>
    </div>

    <!-- Modals -->
    <div class="modal fade" id="deleteConfirmModal" tabindex="-1">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Confirm Deletion</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
              <p>Are you sure you want to delete this vocabulary item?</p>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">{{ t('folder.cancel') }}</button>
              <button type="button" class="btn btn-danger" @click="deleteVocabulary">{{ t('folder.confirmDelete') }}</button>
            </div>
          </div>
        </div>
    </div>
    <div class="modal fade" id="imageSearchModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Select an Image for "{{ vocabForImageSearch?.word }}"</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div v-if="imageSearchLoading" class="text-center">
                <div class="spinner-border"></div>
            </div>
            <div v-else-if="imageSearchResults.length > 0" class="row g-3">
                <div class="col-4" v-for="imageUrl in imageSearchResults" :key="imageUrl">
                    <div class="image-option" @click="selectImage(imageUrl)">
                        <img :src="imageUrl" class="img-fluid rounded" style="cursor: pointer;">
                    </div>
                </div>
            </div>
            <div v-else>
                <p>No images found.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, nextTick } from 'vue';
import { useRoute } from 'vue-router';
import { api } from '@/utils/api';
import { Modal } from 'bootstrap';
import { useTranslation } from '../composables/useTranslation';

const route = useRoute();
const folder = ref({});
const vocabularies = ref([]);
const loading = ref(true);
const error = ref(null);
const originalVocabularies = ref([]);
const vocabToDelete = ref(null);
let deleteModal = null;
let imageSearchModal = null;

const alert = ref({ message: '', type: 'info' });

const imageSearchLoading = ref(false);
const imageSearchResults = ref([]);
const vocabForImageSearch = ref(null);
let currentAudio = null;

const bottomRef = ref(null);

const { t } = useTranslation()

const isDirty = computed(() => {
  if (vocabularies.value.some(v => v.isNew && (v.word || v.definition))) return true;
  if (vocabularies.value.filter(v => !v.isNew && v.isModified).length > 0) return true;
  if (vocabularies.value.length !== originalVocabularies.value.length) return true;
  return false;
});

function showAlert(message, type = 'info', duration = 5000) {
    alert.value = { message, type };
    if (duration) {
        setTimeout(() => { alert.value.message = '' }, duration);
    }
}

onMounted(async () => {
  const folderId = route.params.id;
  try {
    const folderResponse = await api.get(`/folders/${folderId}`);
    folder.value = folderResponse.data;

    const vocabResponse = await api.get(`/folders/${folderId}/vocabularies`);
    vocabularies.value = vocabResponse.data.map(v => ({ ...v, isNew: false, isModified: false }));
    originalVocabularies.value = JSON.parse(JSON.stringify(vocabularies.value));

  } catch (err) {
    error.value = 'Failed to load folder data. ' + (err.response?.data?.error || err.message);
    showAlert(error.value, 'danger');
  } finally {
    loading.value = false;
    deleteModal = new Modal(document.getElementById('deleteConfirmModal'));
    imageSearchModal = new Modal(document.getElementById('imageSearchModal'));
  }
});

function addNewVocabulary() {
  vocabularies.value.push({ id: null, word: '', definition: '', audio_url: '', image_url: '', isNew: true, isModified: false });
  nextTick(() => {
    if (bottomRef.value) {
      bottomRef.value.scrollIntoView({ behavior: 'smooth' });
    }
  });
}

function makeEditable(event, vocab) {
  event.target.removeAttribute('readonly');
  markAsModified(vocab);
}

function markAsModified(vocab) {
  if (!vocab.isNew) {
    vocab.isModified = true;
  }
}

function switchTermDefinition(vocab) {
  [vocab.word, vocab.definition] = [vocab.definition, vocab.word];
  markAsModified(vocab);
}

function switchAllTermsAndDefinitions() {
  vocabularies.value.forEach(v => {
    if (v.word || v.definition) switchTermDefinition(v);
  });
}

function confirmDeleteVocabulary(vocab, index) {
    vocabToDelete.value = { vocab, index };
    deleteModal.show();
}

async function deleteVocabulary() {
  if (!vocabToDelete.value) return;
  const { vocab, index } = vocabToDelete.value;

  if (vocab.isNew) {
    vocabularies.value.splice(index, 1);
  } else {
    try {
      await api.delete(`/folders/${folder.value.id}/vocabularies/${vocab.id}`);
      vocabularies.value.splice(index, 1);
      const originalIndex = originalVocabularies.value.findIndex(v => v.id === vocab.id);
      if (originalIndex > -1) originalVocabularies.value.splice(originalIndex, 1);
      showAlert('Vocabulary deleted', 'success');
    } catch (err) {
      const message = 'Failed to delete vocabulary. ' + (err.response?.data?.error || err.message);
      showAlert(message, 'danger');
    }
  }
  deleteModal.hide();
  vocabToDelete.value = null;
}

async function saveAllVocabularies() {
  const newItems = vocabularies.value.filter(v => v.isNew && v.word && v.definition);
  const modifiedItems = vocabularies.value.filter(v => !v.isNew && v.isModified);

  const batchData = {
    new_items: newItems.map(v => ({ ...v, folder_id: folder.value.id })),
    modified_items: modifiedItems
  };

  if (batchData.new_items.length === 0 && batchData.modified_items.length === 0) {
      originalVocabularies.value = JSON.parse(JSON.stringify(vocabularies.value));
      showAlert('No changes to save.', 'info');
      return;
  }

  try {
    const response = await api.post('/vocabulary/batch-save', batchData);
    if (response.data.success) {
      showAlert('All changes saved successfully!', 'success');
      const vocabResponse = await api.get(`/folders/${folder.value.id}/vocabularies`);
      vocabularies.value = vocabResponse.data.map(v => ({ ...v, isNew: false, isModified: false }));
      originalVocabularies.value = JSON.parse(JSON.stringify(vocabularies.value));
    } else {
      throw new Error(response.data.message || 'Batch save failed');
    }
  } catch (err) {
    const message = 'Failed to save vocabularies. ' + (err.response?.data?.error || err.message);
    showAlert(message, 'danger');
  }
}

async function showImageSearchModal(vocab) {
    if (!vocab.word) {
        showAlert('Please enter a word before searching for an image.', 'warning');
        return;
    }
    vocabForImageSearch.value = vocab;
    imageSearchResults.value = [];
    imageSearchLoading.value = true;
    imageSearchModal.show();
    try {
        const response = await api.get(`/search-images/${vocab.word}`);
        imageSearchResults.value = response.data.images;
    } catch (err) {
        showAlert('Failed to search for images.', 'danger');
    } finally {
        imageSearchLoading.value = false;
    }
}

function selectImage(imageUrl) {
    if (vocabForImageSearch.value) {
        vocabForImageSearch.value.image_url = imageUrl;
        markAsModified(vocabForImageSearch.value);
    }
    imageSearchModal.hide();
}

async function searchAudio(vocab) {
    if (!vocab.word) {
        showAlert('Please enter a word before searching for audio.', 'warning');
        return;
    }
    try {
        const response = await api.get(`/search-audio/${vocab.word}`);
        if (response.data.audio_url) {
            vocab.audio_url = response.data.audio_url;
            markAsModified(vocab);
            showAlert('Audio found and added!', 'success');
        } else {
            showAlert('No audio found for this word.', 'info');
        }
    } catch (err) {
        showAlert('Failed to search for audio.', 'danger');
    }
}

function playAudio(audioUrl) {
    if (currentAudio) {
        currentAudio.pause();
    }
    if (audioUrl) {
        currentAudio = new Audio(audioUrl);
        currentAudio.play().catch(err => {
            showAlert('Could not play audio.', 'danger');
            console.error("Error playing audio:", err);
        });
    }
}

</script>

<style scoped>
.vocabulary-item {
  padding: 10px;
  border-bottom: 1px solid #eee;
}
.image-placeholder {
    width: 100px;
    height: 75px;
    border: 1px dashed #ccc;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
}
.image-placeholder img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
.term-input, .definition-input {
  border: 1px solid transparent;
  background-color: transparent;
}
.term-input:focus, .definition-input:focus,
.term-input:not([readonly]), .definition-input:not([readonly]) {
  border: 1px solid #ced4da;
  background-color: #fff;
}
</style>
