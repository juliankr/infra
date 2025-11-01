<template>
  <div v-if="show" class="form-overlay" @click.self="$emit('cancel')">
    <div class="tab-form">
      <h2>{{ isEditing ? 'Rename Tab' : 'Add New Tab' }}</h2>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="tab-name">Tab Name *</label>
          <input 
            type="text" 
            id="tab-name"
            v-model="localTabName" 
            required 
            maxlength="50"
            placeholder="Enter tab name (e.g., Emma's List)"
            ref="tabNameInput"
          />
        </div>
        
        <div class="form-actions">
          <button type="button" @click="$emit('cancel')" class="btn btn-secondary">
            Cancel
          </button>
          <button type="submit" :disabled="!localTabName.trim()" class="btn btn-primary">
            {{ isEditing ? 'Rename' : 'Create' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, watch, nextTick } from 'vue'

export default {
  name: 'TabForm',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    isEditing: {
      type: Boolean,
      default: false
    },
    tabName: {
      type: String,
      default: ''
    }
  },
  emits: ['submit', 'cancel'],
  setup(props, { emit }) {
    const localTabName = ref('')
    const tabNameInput = ref(null)

    // Watch for changes in props to update local state
    watch([() => props.show, () => props.tabName], async ([show, tabName]) => {
      if (show) {
        localTabName.value = tabName
        await nextTick()
        if (tabNameInput.value) {
          tabNameInput.value.focus()
        }
      }
    }, { immediate: true })

    const handleSubmit = () => {
      if (localTabName.value.trim()) {
        emit('submit', localTabName.value.trim())
      }
    }

    return {
      localTabName,
      tabNameInput,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.form-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 20px;
}

.tab-form {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 30px;
  width: 100%;
  max-width: 400px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 25px 45px rgba(0, 0, 0, 0.1);
}

.tab-form h2 {
  margin: 0 0 25px 0;
  color: #333;
  text-align: center;
  font-size: 1.3em;
}

.form-group {
  margin-bottom: 25px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #555;
  font-weight: 500;
  font-size: 0.95em;
}

.form-group input {
  width: 100%;
  padding: 12px 15px;
  border: 2px solid #e1e5e9;
  border-radius: 12px;
  font-size: 16px;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.form-group input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.form-actions {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
  margin-top: 30px;
}

.btn {
  padding: 12px 25px;
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 80px;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
}

.btn-secondary {
  background: #f8f9fa;
  color: #6c757d;
  border: 1px solid #dee2e6;
}

.btn-secondary:hover:not(:disabled) {
  background: #e9ecef;
  color: #495057;
}
</style>