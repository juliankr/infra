<template>
  <BaseModal 
    :show="show" 
    @close="$emit('close')"
    title="Event löschen"
  >
    <div class="delete-confirmation">
      <p class="warning-text">
        Möchtest du das Event "{{ eventTitle }}" wirklich löschen?
      </p>
      
      <div v-if="isRecurring" class="recurring-options">
        <h4>Wiederkehrendes Event</h4>
        <div class="radio-group">
          <label>
            <input 
              type="radio" 
              v-model="deleteOption" 
              value="single"
            />
            Nur dieses Event löschen
          </label>
          <label>
            <input 
              type="radio" 
              v-model="deleteOption" 
              value="future"
            />
            Dieses und alle zukünftigen Events löschen
          </label>
          <label>
            <input 
              type="radio" 
              v-model="deleteOption" 
              value="series"
            />
            Alle Events dieser Serie löschen
          </label>
        </div>
      </div>

      <div class="actions">
        <button 
          type="button" 
          class="btn btn-secondary"
          @click="$emit('close')"
        >
          Abbrechen
        </button>
        <button 
          type="button" 
          class="btn btn-danger"
          @click="handleDelete"
        >
          Löschen
        </button>
      </div>
    </div>
  </BaseModal>
</template>

<script>
import { ref, computed } from 'vue'
import BaseModal from '../ui/BaseModal.vue'

export default {
  name: 'EventDeleteModal',
  components: {
    BaseModal
  },
  props: {
    show: {
      type: Boolean,
      default: false
    },
    event: {
      type: Object,
      required: true
    }
  },
  emits: ['close', 'delete'],
  setup(props, { emit }) {
    const deleteOption = ref('single')

    const eventTitle = computed(() => props.event?.title || '')
    const isRecurring = computed(() => {
      // Check if this is a recurring event by looking at the ID pattern or recurring_id property
      return props.event?.recurring_id || 
             (props.event?.id && props.event.id.includes('recurring_'))
    })

    const handleDelete = () => {
      emit('delete', {
        eventId: props.event.id,
        option: deleteOption.value
      })
    }

    return {
      deleteOption,
      eventTitle,
      isRecurring,
      handleDelete
    }
  }
}
</script>

<style scoped>
.delete-confirmation {
  padding: 1rem 0;
}

.warning-text {
  color: var(--color-danger);
  font-weight: 500;
  margin-bottom: 1.5rem;
}

.recurring-options {
  margin-bottom: 2rem;
}

.recurring-options h4 {
  margin-bottom: 1rem;
  color: var(--color-text);
}

.radio-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.radio-group label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 0.375rem;
  transition: background-color 0.2s;
}

.radio-group label:hover {
  background-color: var(--color-gray-100);
}

.radio-group input[type="radio"] {
  margin: 0;
}

.actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-secondary {
  background-color: var(--color-gray-300);
  color: var(--color-text);
}

.btn-secondary:hover {
  background-color: var(--color-gray-400);
}

.btn-danger {
  background-color: var(--color-danger);
  color: white;
}

.btn-danger:hover {
  background-color: var(--color-danger-dark);
}
</style>
