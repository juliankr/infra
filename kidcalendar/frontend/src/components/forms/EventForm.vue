<template>
  <form @submit.prevent="handleSubmit" class="event-form">
    <div class="form-group">
      <label for="title">Titel *</label>
      <input
        id="title"
        v-model="formData.title"
        type="text"
        required
        class="form-input"
        placeholder="Event-Titel eingeben..."
      />
    </div>

    <div class="form-group">
      <label for="date">Datum *</label>
      <input
        id="date"
        v-model="formData.date"
        type="date"
        required
        class="form-input"
      />
    </div>

    <div class="form-group">
      <label for="description">Beschreibung</label>
      <textarea
        id="description"
        v-model="formData.description"
        class="form-textarea"
        rows="3"
        placeholder="Zusätzliche Informationen..."
      ></textarea>
    </div>

    <div class="form-group">
      <label class="checkbox-label">
        <input
          type="checkbox"
          v-model="showRecurringOptions"
        />
        Wiederkehrendes Event
      </label>
    </div>

    <div v-if="showRecurringOptions" class="recurring-section">
      <div class="form-group">
        <label for="recurring-type">Wiederholung</label>
        <select
          id="recurring-type"
          v-model="formData.recurringPattern.type"
          class="form-select"
        >
          <option value="daily">Täglich</option>
          <option value="weekly">Wöchentlich</option>
          <option value="interval">Alle X Tage</option>
          <option value="monthly">Monatlich</option>
          <option value="yearly">Jährlich</option>
        </select>
      </div>

      <!-- Weekly pattern: select days -->
      <div v-if="formData.recurringPattern.type === 'weekly'" class="form-group">
        <label>Wochentage:</label>
        <div class="weekdays-selector">
          <label v-for="day in weekdays" :key="day.value" class="weekday-option">
            <input 
              type="checkbox" 
              :value="day.value" 
              v-model="formData.recurringPattern.daysOfWeek"
              class="weekday-checkbox"
            />
            <span class="weekday-label">{{ day.label }}</span>
          </label>
        </div>
      </div>

      <!-- Interval pattern: specify days -->
      <div v-if="formData.recurringPattern.type === 'interval'" class="form-group">
        <label for="interval-days">Alle wieviele Tage:</label>
        <input
          id="interval-days"
          v-model.number="formData.recurringPattern.intervalDays"
          type="number"
          min="1"
          max="365"
          class="form-input"
          placeholder="z.B. 2 für alle 2 Tage"
        />
      </div>

      <div class="form-group">
        <label for="recurring-end">Enddatum (optional):</label>
        <input
          id="recurring-end"
          v-model="formData.recurringPattern.endDate"
          type="date"
          class="form-input"
        />
      </div>
    </div>

    <div class="form-group">
      <label for="image">Bild</label>
      
      <!-- Current image preview -->
      <div v-if="currentImageUrl && !selectedImagePreview" class="current-image-preview">
        <img :src="currentImageUrl" :alt="formData.title" class="image-preview" />
        <p class="image-label">Aktuelles Bild</p>
        <button type="button" @click="removeCurrentImage" class="remove-image-btn">
          🗑️ Bild entfernen
        </button>
      </div>
      
      <!-- New image preview -->
      <div v-if="selectedImagePreview" class="new-image-preview">
        <img :src="selectedImagePreview" :alt="formData.title" class="image-preview" />
        <p class="image-label">Neues Bild</p>
        <button type="button" @click="cancelImageSelection" class="remove-image-btn">
          ❌ Auswahl entfernen
        </button>
      </div>
      
      <!-- Image selection options -->
      <div class="image-selection">
        <div class="form-row">
          <div>
            <label for="existing-image">Vorhandenes Bild wählen</label>
            <select 
              id="existing-image"
              v-model="selectedExistingImageName"
              @change="selectExistingImage"
              class="form-input"
            >
              <option value="">-- Vorhandenes Bild wählen --</option>
              <option v-for="image in availableImages" :key="image.name" :value="image.name">
                {{ image.name }}
              </option>
            </select>
          </div>
          
          <div>
            <label for="new-image">Oder neues Bild hochladen</label>
            <input
              id="new-image"
              type="file"
              accept="image/*"
              class="form-input"
              @change="handleImageChange"
            />
          </div>
        </div>
      </div>
    </div>

    <div class="form-actions">
      <button 
        type="button" 
        class="btn btn-secondary"
        @click="$emit('cancel')"
      >
        Abbrechen
      </button>
      <button 
        type="submit" 
        class="btn btn-primary"
        :disabled="!isFormValid"
      >
        {{ isNew ? 'Erstellen' : 'Speichern' }}
      </button>
    </div>
  </form>
</template>

<script>
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { formatDateDisplay } from '../../utils/date'
import { recurringEventsApi, imagesApi } from '../../services/api'

export default {
  name: 'EventForm',
  props: {
    event: {
      type: Object,
      default: null
    },
    defaultDate: {
      type: String,
      default: ''
    }
  },
  emits: ['submit', 'cancel'],
  setup(props, { emit }) {
    const showRecurringOptions = ref(false)
    const selectedImage = ref(null)
    const currentImageUrl = ref('')
    const selectedImagePreview = ref('')
    const availableImages = ref([])
    const selectedExistingImageName = ref('')

    const weekdays = [
      { value: 'monday', label: 'Mo' },
      { value: 'tuesday', label: 'Di' },
      { value: 'wednesday', label: 'Mi' },
      { value: 'thursday', label: 'Do' },
      { value: 'friday', label: 'Fr' },
      { value: 'saturday', label: 'Sa' },
      { value: 'sunday', label: 'So' }
    ]

    const formData = reactive({
      title: '',
      date: '',
      description: '',
      recurringPattern: {
        type: 'weekly',
        daysOfWeek: [],
        intervalDays: 1,
        endDate: ''
      }
    })

    const isNew = computed(() => !props.event?.id)
    
    const isFormValid = computed(() => {
      return formData.title.trim() && formData.date
    })

    // Initialize form data
    const initializeForm = async () => {
      if (props.event) {
        // Set basic event data
        Object.assign(formData, {
          title: props.event.title || '',
          date: props.event.date || '',
          description: props.event.description || ''
        })

        // Set current image URL
        currentImageUrl.value = props.event.image || ''
        selectedImagePreview.value = ''
        selectedImage.value = null

        // If this is a recurring event, fetch the recurring pattern
        if (props.event.recurring_id) {
          try {
            const response = await recurringEventsApi.getRecurringEvent(props.event.recurring_id)
            if (response.success && response.recurring_event) {
              const recurringData = response.recurring_event
              formData.recurringPattern = {
                type: recurringData.pattern?.type || 'weekly',
                daysOfWeek: recurringData.pattern?.days || [],
                intervalDays: recurringData.pattern?.interval_days || 1,
                endDate: recurringData.pattern?.end_date || ''
              }
              showRecurringOptions.value = true
            }
          } catch (error) {
            console.error('Failed to fetch recurring pattern:', error)
            // Fallback to default recurring pattern
            formData.recurringPattern = {
              type: 'weekly',
              daysOfWeek: [],
              intervalDays: 1,
              endDate: ''
            }
          }
        } else {
          // Reset recurring pattern for non-recurring events
          formData.recurringPattern = {
            type: 'weekly',
            daysOfWeek: [],
            intervalDays: 1,
            endDate: ''
          }
          showRecurringOptions.value = false
        }
      } else {
        // Reset form for new event
        currentImageUrl.value = ''
        selectedImagePreview.value = ''
        selectedImage.value = null
        if (props.defaultDate) {
          formData.date = props.defaultDate
        }
      }
    }

    const handleImageChange = (event) => {
      const file = event.target.files[0]
      selectedImage.value = file || null
      
      if (file) {
        // Create preview URL for the selected image
        const reader = new FileReader()
        reader.onload = (e) => {
          selectedImagePreview.value = e.target.result
        }
        reader.readAsDataURL(file)
      } else {
        selectedImagePreview.value = ''
      }
    }

    const removeCurrentImage = () => {
      currentImageUrl.value = ''
      selectedImagePreview.value = ''
      selectedImage.value = null
      // Clear the file input
      const fileInput = document.getElementById('image')
      if (fileInput) fileInput.value = ''
    }

    const cancelImageSelection = () => {
      selectedImagePreview.value = ''
      selectedImage.value = null
      selectedExistingImageName.value = ''
      // Clear the file input
      const fileInput = document.getElementById('new-image')
      if (fileInput) fileInput.value = ''
    }

    const selectExistingImage = () => {
      if (selectedExistingImageName.value) {
        const selectedImg = availableImages.value.find(img => img.name === selectedExistingImageName.value)
        if (selectedImg) {
          selectedImagePreview.value = selectedImg.url
          selectedImage.value = null // Clear file upload
          // Clear the file input
          const fileInput = document.getElementById('new-image')
          if (fileInput) fileInput.value = ''
        }
      }
    }

    const loadAvailableImages = async () => {
      try {
        const response = await fetch('/api/images')
        if (response.ok) {
          const data = await response.json()
          availableImages.value = data.images || []
        }
      } catch (error) {
        console.error('Error loading available images:', error)
      }
    }

    const handleSubmit = async () => {
      let imagePath = currentImageUrl.value // Start with current image
      
      // Upload new image if one is selected
      if (selectedImage.value) {
        try {
          const uploadResponse = await imagesApi.uploadImage(selectedImage.value)
          if (uploadResponse.success) {
            imagePath = uploadResponse.file.url
          }
        } catch (error) {
          console.error('Failed to upload image:', error)
          // Keep current image if upload fails
        }
      }
      // Use existing image if one is selected from dropdown
      else if (selectedExistingImageName.value) {
        const selectedImg = availableImages.value.find(img => img.name === selectedExistingImageName.value)
        if (selectedImg) {
          imagePath = selectedImg.url
        }
      }

      const eventData = {
        title: formData.title.trim(),
        date: formData.date,
        description: formData.description.trim(),
        recurring: showRecurringOptions.value ? {
          frequency: formData.recurringPattern.type,
          daysOfWeek: formData.recurringPattern.daysOfWeek,
          intervalDays: formData.recurringPattern.intervalDays,
          endDate: formData.recurringPattern.endDate
        } : null,
        image: imagePath || null // Use existing image, new image, or null if removed
      }

      if (props.event?.id) {
        eventData.id = props.event.id
      }

      emit('submit', eventData)
    }

    // Watch for prop changes
    watch(() => props.event, () => {
      initializeForm()
    }, { immediate: true })
    
    watch(() => props.defaultDate, (newDate) => {
      if (newDate && !props.event) {
        formData.date = newDate
      }
    })

    // Load available images when component mounts
    onMounted(() => {
      loadAvailableImages()
    })

    return {
      formData,
      showRecurringOptions,
      weekdays,
      isNew,
      isFormValid,
      currentImageUrl,
      selectedImagePreview,
      availableImages,
      selectedExistingImageName,
      handleImageChange,
      removeCurrentImage,
      cancelImageSelection,
      selectExistingImage,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.event-form {
  max-width: 500px;
}

.form-group {
  margin-bottom: 1rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--color-text);
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.form-input,
.form-textarea,
.form-select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--color-gray-300);
  border-radius: 0.375rem;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-input:focus,
.form-textarea:focus,
.form-select:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(var(--color-primary-rgb), 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 3rem;
}

.recurring-section {
  background-color: var(--color-gray-50);
  padding: 1rem;
  border-radius: 0.375rem;
  margin-bottom: 1rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: var(--color-gray-300);
  color: var(--color-text);
}

.btn-secondary:hover:not(:disabled) {
  background-color: var(--color-gray-400);
}

.btn-primary {
  background-color: var(--color-primary);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: var(--color-primary-dark);
}

.weekdays-selector {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 8px;
}

.weekday-option {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  border: 1px solid var(--color-gray-300);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  background: white;
}

.weekday-option:hover {
  background-color: var(--color-gray-50);
}

.weekday-checkbox {
  margin: 0;
}

.weekday-checkbox:checked + .weekday-label {
  font-weight: 600;
  color: var(--color-primary);
}

.weekday-label {
  font-size: 14px;
  user-select: none;
}

@media (max-width: 640px) {
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column;
  }
}

/* Image preview styles */
.current-image-preview,
.new-image-preview {
  margin: 8px 0;
  text-align: center;
}

.image-preview {
  max-width: 200px;
  max-height: 150px;
  width: auto;
  height: auto;
  border-radius: 8px;
  border: 2px solid var(--color-gray-200);
  object-fit: cover;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.image-label {
  margin: 4px 0 0 0;
  font-size: 12px;
  color: var(--color-gray-600);
  font-style: italic;
}

.new-image-preview .image-label {
  color: var(--color-primary);
  font-weight: 500;
}

.remove-image-btn {
  margin-top: 8px;
  padding: 4px 8px;
  font-size: 12px;
  background-color: var(--color-gray-200);
  border: 1px solid var(--color-gray-300);
  border-radius: 4px;
  color: var(--color-gray-700);
  cursor: pointer;
  transition: all 0.2s;
}

.remove-image-btn:hover {
  background-color: var(--color-gray-300);
  border-color: var(--color-gray-400);
}

/* Image selection layout */
.image-selection {
  margin-top: 1rem;
}

.image-selection .form-row {
  gap: 1rem;
}

.image-selection label {
  font-size: 0.875rem;
  color: var(--color-gray-600);
  font-weight: 500;
}
</style>
