<template>
  <div class="app">
    <!-- Pull-to-refresh functionality -->
    <PullToRefresh 
      @refresh="handleRefresh"
      :disabled="isLoading"
    >
      <!-- Edit mode indicator -->
      <div v-if="editMode" class="edit-mode-header">
        <span class="edit-mode-title">✏️ Edit Mode Active</span>
        <button @click="exitEditMode" class="exit-edit-btn">❌ Exit</button>
      </div>

      <!-- Error display -->
      <ErrorMessage
        v-if="error"
        :message="error"
        @dismiss="clearError"
      />
      
      <!-- Main content -->
      <LoadingSpinner 
        v-if="isLoading && events.length === 0" 
        text="Lade Events..." 
      />
      
      <WeekCalendar 
        ref="weekCalendarRef"
        v-else
        :events="events" 
        :edit-mode="editMode"
        :loading="isLoading"
        @edit-event="handleEditEvent"
        @delete-event="handleDeleteEvent"
        @add-event="handleAddEvent"
        @date-changed="handleDateChanged"
      />
    </PullToRefresh>
    
    <!-- Modals -->
    <EventEditModal
      :show="showEditModal"
      :event="currentEditEvent"
      :default-date="defaultEventDate"
      @close="closeEditModal"
      @save="saveEvent"
    />
    
    <EventDeleteModal
      :show="showDeleteModal"
      :event="currentDeleteEvent"
      @close="closeDeleteModal"
      @delete="handleDeleteConfirm"
    />

    <!-- Floating buttons (edit mode only) -->
    <div v-if="editMode" class="floating-buttons">
      <button @click="handleAddEvent" class="floating-btn floating-add-btn">
        ➕
      </button>
      <button @click="openYamlEditor" class="floating-btn floating-yaml-btn">
        📝
      </button>
    </div>

    <!-- YAML Editor Modal -->
    <YamlEditor
      :show="showYamlEditor"
      @close="closeYamlEditor"
      @save="saveYamlConfig"
    />
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import WeekCalendar from './components/calendar/WeekCalendar.vue'
import EventEditModal from './components/modals/EventEditModal.vue'
import EventDeleteModal from './components/modals/EventDeleteModal.vue'
import LoadingSpinner from './components/ui/LoadingSpinner.vue'
import ErrorMessage from './components/ui/ErrorMessage.vue'
import PullToRefresh from './components/ui/PullToRefresh.vue'
import YamlEditor from './components/modals/YamlEditor.vue'

import { useEvents } from './composables/useEvents'
import { useEditMode } from './composables/useEditMode'
import { useModals } from './composables/useModals'
import { useErrorHandling } from './composables/useErrorHandling'
import { useSettings } from './composables/useSettings'
import { useDateChangeDetection } from './composables/useDateChangeDetection'
import { usePageVisibility } from './composables/usePageVisibility'

export default {
  name: 'App',
  components: {
    WeekCalendar,
    EventEditModal,
    EventDeleteModal,
    LoadingSpinner,
    ErrorMessage,
    PullToRefresh,
    YamlEditor
  },
  setup() {
    // Refs
    const weekCalendarRef = ref(null)
    
    // Composables
    const { 
      events, 
      loading: isLoading, 
      loadEvents, 
      createEvent, 
      updateEvent, 
      deleteEvent: deleteEventFromAPI 
    } = useEvents()
    
    const { 
      isEditMode: editMode, 
      exitEditMode,
      toggleEditMode
    } = useEditMode()
    const { error, clearError, handleError } = useErrorHandling()
    const { loadSettings } = useSettings()
    
    // Date change detection - refresh when new day starts
    useDateChangeDetection(() => {
      console.log('New day detected - refreshing events and settings')
      loadSettings()
      loadEvents()
    })
    
    // Page visibility detection - refresh when returning to app
    usePageVisibility((timeAway) => {
      console.log('App became visible after being away - refreshing')
      loadSettings()
      loadEvents()
    })
    
    const {
      showEditModal,
      showDeleteModal,
      showYamlEditor,
      currentEditEvent,
      currentDeleteEvent,
      defaultEventDate,
      closeEditModal,
      closeDeleteModal,
      closeYamlEditor,
      openYamlEditor
    } = useModals()

    // Event handlers
    const handleRefresh = async () => {
      try {
        // Reset navigation to today
        if (weekCalendarRef.value) {
          weekCalendarRef.value.goToToday()
        }
        // Refresh data for current day (offset 0)
        await loadEvents(0)
        await loadSettings()
      } catch (err) {
        handleError('Fehler beim Laden der Events')
      }
    }

    const handleDateChanged = (newDate, offset) => {
      // When date changes due to navigation, load events for the new offset
      console.log('Date navigation changed to:', newDate, 'with offset:', offset)
      loadEvents(offset)
    }

    const handleEditEvent = (event) => {
      currentEditEvent.value = event
      showEditModal.value = true
    }

    const handleDeleteEvent = (event) => {
      currentDeleteEvent.value = event
      showDeleteModal.value = true
    }

    const handleAddEvent = (date = null) => {
      currentEditEvent.value = null
      defaultEventDate.value = date || new Date().toISOString().split('T')[0]
      showEditModal.value = true
    }

    const saveEvent = async (eventData) => {
      try {
        if (eventData.id) {
          await updateEvent(eventData.id, eventData)
        } else {
          await createEvent(eventData)
        }
        closeEditModal()
        await loadEvents() // Refresh events
      } catch (err) {
        handleError('Fehler beim Speichern des Events')
      }
    }

    const handleDeleteConfirm = async ({ eventId, option }) => {
      try {
        await deleteEventFromAPI(eventId, option)
        closeDeleteModal()
        await loadEvents() // Refresh events
      } catch (err) {
        handleError('Fehler beim Löschen des Events')
      }
    }

    const saveYamlConfig = async (yamlContent) => {
      try {
        const response = await fetch('/api/config/yaml', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ yaml_content: yamlContent })
        })
        
        if (!response.ok) {
          throw new Error('Fehler beim Speichern der Konfiguration')
        }
        
        closeYamlEditor()
        await loadEvents() // Refresh events
      } catch (err) {
        handleError(err.message || 'Fehler beim Speichern der YAML-Konfiguration')
      }
    }

    // Lifecycle
    onMounted(() => {
      loadSettings()
      loadEvents()
    })

    return {
      // Refs
      weekCalendarRef,
      
      // State
      events,
      isLoading,
      editMode,
      error,
      showEditModal,
      showDeleteModal,
      showYamlEditor,
      currentEditEvent,
      currentDeleteEvent,
      defaultEventDate,
      
      // Methods
      handleRefresh,
      handleEditEvent,
      handleDeleteEvent,
      handleAddEvent,
      handleDateChanged,
      saveEvent,
      handleDeleteConfirm,
      saveYamlConfig,
      exitEditMode,
      clearError,
      closeEditModal,
      closeDeleteModal,
      closeYamlEditor,
      openYamlEditor
    }
  }
}
</script>

<style scoped>
.app {
  min-height: 100vh;
  background-color: var(--color-gray-50);
}

.edit-mode-header {
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-dark));
  color: white;
  padding: 0.75rem 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.edit-mode-title {
  font-weight: 600;
  font-size: 0.875rem;
}

.exit-edit-btn {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 0.375rem 0.75rem;
  border-radius: 0.375rem;
  cursor: pointer;
  font-size: 0.75rem;
  font-weight: 500;
  transition: all 0.2s;
}

.exit-edit-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.5);
}

.floating-buttons {
  position: fixed;
  right: 1rem;
  bottom: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  z-index: 200;
}

.floating-btn {
  width: 3.5rem;
  height: 3.5rem;
  border-radius: 50%;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.floating-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
}

.floating-add-btn {
  background: var(--color-primary);
  color: white;
}

.floating-yaml-btn {
  background: var(--color-secondary);
  color: white;
}

@media (max-width: 640px) {
  .floating-buttons {
    right: 0.75rem;
    bottom: 0.75rem;
  }
  
  .floating-btn {
    width: 3rem;
    height: 3rem;
    font-size: 1.25rem;
  }
}
</style>
