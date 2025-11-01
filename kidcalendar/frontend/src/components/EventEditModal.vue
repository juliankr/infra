<template>
  <div v-if="show" class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2>{{ isNew ? 'Neues Event' : 'Event bearbeiten' }}</h2>
        <button class="close-btn" @click="closeModal">×</button>
      </div>
      
      <form @submit.prevent="saveEvent" class="event-form">
        <div class="form-group">
          <label for="title">Titel:</label>
          <input 
            id="title"
            v-model="eventData.title" 
            type="text" 
            required 
            class="form-input"
            placeholder="Event-Titel eingeben"
          />
        </div>
        
        <div class="form-group">
          <label for="date">Datum:</label>
          <input 
            id="date"
            v-model="eventData.date" 
            type="date" 
            required 
            class="form-input"
          />
        </div>
        
        <div class="form-group">
          <label for="color">Farbe:</label>
          <div class="color-picker">
            <input 
              id="color"
              v-model="eventData.color" 
              type="color" 
              class="color-input"
            />
            <span class="color-preview" :style="{ backgroundColor: eventData.color }"></span>
          </div>
        </div>
        
        <div class="form-group">
          <label for="position">Position:</label>
          <input 
            id="position"
            v-model.number="eventData.position" 
            type="number" 
            min="1" 
            max="10"
            class="form-input"
            placeholder="Reihenfolge (1-10)"
          />
        </div>
        
        <div class="form-group">
          <label for="description">Beschreibung (optional):</label>
          <textarea 
            id="description"
            v-model="eventData.description" 
            class="form-input"
            rows="2"
            placeholder="Zusätzliche Beschreibung"
          ></textarea>
        </div>
        
        <div class="form-group">
          <label for="image">Bild hochladen:</label>
          <input 
            id="image"
            type="file" 
            accept="image/*"
            @change="handleImageUpload"
            class="form-input"
          />
          <div v-if="eventData.image" class="image-preview">
            <img :src="eventData.image" alt="Event Vorschau" class="preview-image" />
          </div>
        </div>
        
        <div class="form-group">
          <label>
            <input 
              v-model="eventData.isRecurring" 
              type="checkbox"
              class="checkbox-input"
            />
            Wiederkehrendes Event
          </label>
        </div>
        
        <div v-if="eventData.isRecurring" class="recurring-options">
          <div class="form-group">
            <label for="frequency">Häufigkeit:</label>
            <select id="frequency" v-model="eventData.frequency" class="form-select">
              <option value="daily">Täglich</option>
              <option value="weekly">Wöchentlich</option>
              <option value="interval">Alle X Tage</option>
              <option value="monthly">Monatlich</option>
              <option value="yearly">Jährlich</option>
            </select>
          </div>
          
          <!-- Weekly pattern: select days -->
          <div v-if="eventData.frequency === 'weekly'" class="form-group">
            <label>Wochentage:</label>
            <div class="weekdays-selector">
              <label v-for="day in weekdays" :key="day.value" class="weekday-option">
                <input 
                  type="checkbox" 
                  :value="day.value" 
                  v-model="eventData.daysOfWeek"
                  class="weekday-checkbox"
                />
                <span class="weekday-label">{{ day.label }}</span>
              </label>
            </div>
          </div>
          
          <!-- Interval pattern: specify days -->
          <div v-if="eventData.frequency === 'interval'" class="form-group">
            <label for="intervalDays">Alle wieviele Tage:</label>
            <input 
              id="intervalDays"
              v-model.number="eventData.intervalDays" 
              type="number" 
              min="1" 
              max="365"
              class="form-input"
              placeholder="z.B. 2 für alle 2 Tage"
            />
          </div>
          
          <div class="form-group">
            <label for="endDate">Enddatum (optional):</label>
            <input 
              id="endDate"
              v-model="eventData.endDate" 
              type="date" 
              class="form-input"
            />
          </div>
        </div>
        
        <div class="form-actions">
          <button type="button" @click="closeModal" class="cancel-btn">
            Abbrechen
          </button>
          <button type="submit" class="save-btn" :disabled="!eventData.title">
            {{ isNew ? 'Erstellen' : 'Speichern' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { configApi } from '../services/api';
import { useSettings } from '../composables/useSettings';

export default {
  name: 'EventEditModal',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    event: {
      type: Object,
      default: null
    },
    defaultDate: {
      type: String,
      default: () => new Date().toISOString().split('T')[0]
    }
  },
  emits: ['close', 'save'],
  setup() {
    const { defaultColor, defaultPosition, loadSettings } = useSettings();
    
    // Load settings when component is set up
    loadSettings();
    
    return {
      defaultColor,
      defaultPosition
    };
  },
  data() {
    return {
      eventData: {
        title: '',
        date: '',
        color: '#FF6B6B',
        image: '',
        position: 1,
        description: '',
        isRecurring: false,
        frequency: 'weekly',
        daysOfWeek: [],
        intervalDays: 2,
        endDate: ''
      },
      uploadedFile: null,
      availableImages: []
    }
  },
  computed: {
    isNew() {
      return !this.event || !this.event.id;
    }
  },
  watch: {
    show(newVal) {
      if (newVal) {
        this.resetForm();
      }
    },
    event: {
      handler(newEvent) {
        if (newEvent) {
          this.eventData = {
            title: newEvent.title || '',
            date: newEvent.date || this.defaultDate,
            color: newEvent.color || this.defaultColor || '#FF6B6B',
            image: newEvent.image || '',
            position: newEvent.position || this.defaultPosition || 1,
            description: newEvent.description || '',
            isRecurring: !!newEvent.recurring,
            frequency: newEvent.recurring?.frequency || 'weekly',
            daysOfWeek: newEvent.recurring?.daysOfWeek || [],
            intervalDays: newEvent.recurring?.intervalDays || 2,
            endDate: newEvent.recurring?.endDate || ''
          };
        }
      },
      immediate: true
    }
  },
  methods: {
    resetForm() {
      if (this.event) {
        this.eventData = {
          title: this.event.title || '',
          date: this.event.date || this.defaultDate,
          color: this.event.color || this.defaultColor || '#FF6B6B',
          image: this.event.image || '',
          position: this.event.position || this.defaultPosition || 1,
          description: this.event.description || '',
          isRecurring: !!this.event.recurring,
          frequency: this.event.recurring?.frequency || 'weekly',
          daysOfWeek: this.event.recurring?.daysOfWeek || [],
          intervalDays: this.event.recurring?.intervalDays || 2,
          endDate: this.event.recurring?.endDate || ''
        };
      } else {
        this.eventData = {
          title: '',
          date: this.defaultDate,
          color: this.defaultColor || '#FF6B6B',
          image: '',
          position: this.defaultPosition || 1,
          description: '',
          isRecurring: false,
          frequency: 'weekly',
          daysOfWeek: [],
          intervalDays: 2,
          endDate: ''
        };
      }
      this.uploadedFile = null;
    },
    
    async handleImageUpload(event) {
      const file = event.target.files[0];
      if (!file) return;
      
      this.uploadedFile = file;
      
      // Create preview URL
      const reader = new FileReader();
      reader.onload = (e) => {
        this.eventData.image = e.target.result;
      };
      reader.readAsDataURL(file);
    },
    
    closeModal() {
      this.$emit('close');
    },
    
    async saveEvent() {
      try {
        const eventToSave = {
          title: this.eventData.title,
          date: this.eventData.date,
          color: this.eventData.color,
          image: this.eventData.image,
          position: this.eventData.position,
          description: this.eventData.description
        };
        
        // Add recurring data if needed
        if (this.eventData.isRecurring) {
          eventToSave.recurring = {
            frequency: this.eventData.frequency,
            endDate: this.eventData.endDate || null
          };
          
          // Add specific fields based on frequency
          if (this.eventData.frequency === 'weekly') {
            eventToSave.recurring.daysOfWeek = this.eventData.daysOfWeek;
          } else if (this.eventData.frequency === 'interval') {
            eventToSave.recurring.intervalDays = this.eventData.intervalDays;
          }
        }
        
        // If we have an uploaded file, include it
        if (this.uploadedFile) {
          eventToSave.imageFile = this.uploadedFile;
        }
        
        // Include original event data for updates
        if (this.event && this.event.id) {
          eventToSave.id = this.event.id;
        }
        
        this.$emit('save', eventToSave);
        this.closeModal();
      } catch (error) {
        console.error('Error saving event:', error);
        alert('Fehler beim Speichern des Events');
      }
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 16px;
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #eee;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5rem;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: #f5f5f5;
  color: #333;
}

.event-form {
  padding: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #333;
}

.form-input, .form-select {
  width: 100%;
  padding: 12px;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 0.2s ease;
  box-sizing: border-box;
}

.form-input:focus, .form-select:focus {
  outline: none;
  border-color: #FF6B6B;
}

.color-picker {
  display: flex;
  align-items: center;
  gap: 12px;
}

.color-input {
  width: 60px;
  height: 40px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.color-preview {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  border: 2px solid #ddd;
}

.checkbox-input {
  margin-right: 8px;
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
  padding: 6px 12px;
  border: 2px solid #e1e5e9;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 14px;
}

.weekday-option:hover {
  border-color: #FF6B6B;
  background: rgba(255, 107, 107, 0.1);
}

.weekday-checkbox {
  margin-right: 6px;
}

.weekday-checkbox:checked + .weekday-label {
  font-weight: bold;
}

.weekday-option:has(.weekday-checkbox:checked) {
  background: #FF6B6B;
  border-color: #FF6B6B;
  color: white;
}

.form-input[type="number"] {
  width: 120px;
}

textarea.form-input {
  resize: vertical;
  min-height: 60px;
}

.image-preview {
  margin-top: 12px;
}

.preview-image {
  max-width: 100px;
  max-height: 80px;
  object-fit: contain;
  border-radius: 8px;
  border: 2px solid #eee;
}

.recurring-options {
  background: #f8f9fa;
  padding: 16px;
  border-radius: 8px;
  margin-top: 12px;
}

.form-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.cancel-btn, .save-btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.cancel-btn {
  background: #f5f5f5;
  color: #666;
}

.cancel-btn:hover {
  background: #e9ecef;
}

.save-btn {
  background: #FF6B6B;
  color: white;
}

.save-btn:hover:not(:disabled) {
  background: #ff5252;
  transform: translateY(-1px);
}

.save-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .modal-overlay {
    padding: 10px;
  }
  
  .modal-content {
    max-height: 95vh;
  }
  
  .modal-header {
    padding: 16px 20px;
  }
  
  .event-form {
    padding: 20px;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .cancel-btn, .save-btn {
    width: 100%;
  }
}
</style>
