<template>
  <BaseModal 
    :show="show" 
    @close="$emit('close')"
    title="YAML Konfiguration bearbeiten"
  >
    <div class="yaml-editor">
      <div class="yaml-editor-toolbar">
        <button 
          @click="loadYamlConfig" 
          :disabled="loading"
          class="btn btn-secondary"
        >
          {{ loading ? 'Lade...' : 'Neu laden' }}
        </button>
      </div>
      
      <textarea 
        v-model="yamlContent" 
        class="yaml-textarea"
        spellcheck="false"
        :disabled="loading"
        placeholder="YAML Konfiguration hier eingeben..."
      ></textarea>
      
      <div v-if="error" class="yaml-error">
        {{ error }}
      </div>
      
      <div class="yaml-actions">
        <button 
          @click="handleSave" 
          :disabled="loading || !yamlContent.trim()"
          class="btn btn-primary"
        >
          {{ loading ? 'Speichere...' : 'Speichern' }}
        </button>
        <button 
          @click="$emit('close')" 
          class="btn btn-secondary"
        >
          Abbrechen
        </button>
      </div>
    </div>
  </BaseModal>
</template>

<script>
import { ref, watch } from 'vue'
import BaseModal from '../ui/BaseModal.vue'

export default {
  name: 'YamlEditor',
  components: {
    BaseModal
  },
  props: {
    show: {
      type: Boolean,
      default: false
    }
  },
  emits: ['close', 'save'],
  setup(props, { emit }) {
    const yamlContent = ref('')
    const loading = ref(false)
    const error = ref('')

    const loadYamlConfig = async () => {
      loading.value = true
      error.value = ''
      
      try {
        const response = await fetch('/api/config/yaml')
        if (!response.ok) {
          throw new Error('Fehler beim Laden der Konfiguration')
        }
        
        const data = await response.json()
        yamlContent.value = data.yaml_content
      } catch (err) {
        error.value = err.message || 'Fehler beim Laden der YAML-Konfiguration'
        console.error('Error loading YAML config:', err)
      } finally {
        loading.value = false
      }
    }

    const handleSave = async () => {
      loading.value = true
      error.value = ''
      
      try {
        // Validate YAML syntax (basic check)
        if (!yamlContent.value.trim()) {
          throw new Error('YAML Inhalt darf nicht leer sein')
        }
        
        emit('save', yamlContent.value)
      } catch (err) {
        error.value = err.message || 'Fehler beim Speichern der YAML-Konfiguration'
      } finally {
        loading.value = false
      }
    }

    // Load YAML when modal opens
    watch(() => props.show, (newValue) => {
      if (newValue) {
        loadYamlConfig()
      }
    })

    return {
      yamlContent,
      loading,
      error,
      loadYamlConfig,
      handleSave
    }
  }
}
</script>

<style scoped>
.yaml-editor {
  width: 100%;
  max-width: 800px;
}

.yaml-editor-toolbar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1rem;
}

.yaml-textarea {
  width: 100%;
  height: 400px;
  font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
  font-size: 0.875rem;
  line-height: 1.5;
  padding: 1rem;
  border: 1px solid var(--color-gray-300);
  border-radius: 0.375rem;
  resize: vertical;
  background-color: var(--color-gray-50);
}

.yaml-textarea:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(var(--color-primary-rgb), 0.1);
}

.yaml-textarea:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.yaml-error {
  background-color: var(--color-danger-light);
  color: var(--color-danger-dark);
  padding: 0.75rem;
  border-radius: 0.375rem;
  margin: 1rem 0;
  font-size: 0.875rem;
  border: 1px solid var(--color-danger);
}

.yaml-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
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

.btn-primary {
  background-color: var(--color-primary);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: var(--color-primary-dark);
}

.btn-secondary {
  background-color: var(--color-gray-300);
  color: var(--color-text);
}

.btn-secondary:hover:not(:disabled) {
  background-color: var(--color-gray-400);
}

@media (max-width: 640px) {
  .yaml-textarea {
    height: 300px;
    font-size: 0.8rem;
  }
  
  .yaml-actions {
    flex-direction: column;
  }
}
</style>
