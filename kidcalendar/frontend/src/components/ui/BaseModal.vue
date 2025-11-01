<template>
  <Teleport to="body">
    <div 
      v-if="show" 
      class="modal-overlay"
      @click="handleOverlayClick"
    >
      <div 
        class="modal-container"
        @click.stop
      >
        <div class="modal-header">
          <h3 class="modal-title">{{ title }}</h3>
          <button 
            class="modal-close"
            @click="$emit('close')"
            aria-label="Schließen"
          >
            ×
          </button>
        </div>
        <div class="modal-body">
          <slot />
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script>
import { onMounted, onUnmounted } from 'vue'

export default {
  name: 'BaseModal',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: ''
    },
    closeOnOverlay: {
      type: Boolean,
      default: true
    }
  },
  emits: ['close'],
  setup(props, { emit }) {
    const handleOverlayClick = () => {
      if (props.closeOnOverlay) {
        emit('close')
      }
    }

    const handleEscape = (event) => {
      if (event.key === 'Escape' && props.show) {
        emit('close')
      }
    }

    onMounted(() => {
      document.addEventListener('keydown', handleEscape)
      if (props.show) {
        document.body.style.overflow = 'hidden'
      }
    })

    onUnmounted(() => {
      document.removeEventListener('keydown', handleEscape)
      document.body.style.overflow = ''
    })

    return {
      handleOverlayClick
    }
  },
  watch: {
    show(newValue) {
      document.body.style.overflow = newValue ? 'hidden' : ''
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
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-container {
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  max-width: 90vw;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--color-gray-200);
}

.modal-title {
  margin: 0;
  color: var(--color-text);
  font-size: 1.25rem;
  font-weight: 600;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--color-gray-500);
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.25rem;
  transition: all 0.2s;
}

.modal-close:hover {
  background-color: var(--color-gray-100);
  color: var(--color-text);
}

.modal-body {
  padding: 1.5rem;
  overflow-y: auto;
  flex: 1;
}

@media (max-width: 640px) {
  .modal-container {
    max-width: 95vw;
    margin: 0.5rem;
  }
  
  .modal-header {
    padding: 1rem;
  }
  
  .modal-body {
    padding: 1rem;
  }
}
</style>
