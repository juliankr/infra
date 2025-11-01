<template>
  <div v-if="show" class="form-overlay" @click.self="$emit('cancel')">
    <div class="add-form">
      <h2>Add New Item</h2>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="item-name">Item Name *</label>
          <input 
            type="text" 
            id="item-name"
            v-model="formData.name" 
            required 
            maxlength="100"
            placeholder="What would you like?"
            ref="itemNameInput"
          />
        </div>
        
        <div class="form-group">
          <label for="item-link">Link (optional)</label>
          <input 
            type="url" 
            id="item-link"
            v-model="formData.link"
            placeholder="https://..."
          />
        </div>
        
        <div class="form-group">
          <label for="item-image">Image</label>
          <div class="image-input-container">
            <input 
              type="file" 
              id="item-image"
              @change="handleImageChange"
              accept="image/*"
              ref="fileInput"
            />
            <div class="url-input-container">
              <input 
                type="url" 
                v-model="imageUrl"
                placeholder="Or paste image URL here..."
                class="url-input"
                @input="handleImageUrlChange"
              />
            </div>
          </div>
          <div v-if="imagePreview" class="image-preview">
            <img :src="imagePreview" alt="Preview" />
            <button type="button" @click="clearImage" class="clear-image">×</button>
          </div>
        </div>
        
        <div class="form-actions">
          <button type="button" @click="$emit('cancel')" class="btn btn-secondary">
            Cancel
          </button>
          <button type="submit" :disabled="!formData.name.trim() || uploading" class="btn btn-primary">
            {{ uploading ? 'Adding...' : 'Add Item' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, reactive, watch, nextTick } from 'vue'

export default {
  name: 'AddItemForm',
  props: {
    show: {
      type: Boolean,
      default: false
    }
  },
  emits: ['submit', 'cancel'],
  setup(props, { emit }) {
    const formData = reactive({
      name: '',
      link: '',
      image: null
    })
    
    const imageUrl = ref('')
    const imagePreview = ref(null)
    const uploading = ref(false)
    const itemNameInput = ref(null)
    const fileInput = ref(null)

    // Watch for show prop to reset form and focus input
    watch(() => props.show, async (show) => {
      if (show) {
        resetForm()
        await nextTick()
        if (itemNameInput.value) {
          itemNameInput.value.focus()
        }
      }
    })

    const resetForm = () => {
      formData.name = ''
      formData.link = ''
      formData.image = null
      imageUrl.value = ''
      imagePreview.value = null
      uploading.value = false
      if (fileInput.value) {
        fileInput.value.value = ''
      }
    }

    const handleImageChange = async (event) => {
      const file = event.target.files[0]
      if (file) {
        try {
          uploading.value = true
          
          // Import api dynamically to avoid circular dependency
          const { default: api } = await import('../../api.js')
          const response = await api.uploadImage(file)
          
          if (response.success) {
            formData.image = response.data.filename
            imageUrl.value = '' // Clear URL input when file is uploaded
            
            // Create preview
            const reader = new FileReader()
            reader.onload = (e) => {
              imagePreview.value = e.target.result
            }
            reader.readAsDataURL(file)
          } else {
            throw new Error(response.error || 'Failed to upload image')
          }
        } catch (error) {
          alert('Failed to upload image: ' + error.message)
          // Clear the file input
          if (fileInput.value) {
            fileInput.value.value = ''
          }
        } finally {
          uploading.value = false
        }
      }
    }

    const handleImageUrlChange = () => {
      if (imageUrl.value.trim()) {
        formData.image = imageUrl.value.trim()
        imagePreview.value = imageUrl.value.trim()
        // Clear file input when URL is entered
        if (fileInput.value) {
          fileInput.value.value = ''
        }
      }
    }

    const clearImage = () => {
      formData.image = null
      imageUrl.value = ''
      imagePreview.value = null
      if (fileInput.value) {
        fileInput.value.value = ''
      }
    }

    const handleSubmit = async () => {
      if (!formData.name.trim()) return
      
      uploading.value = true
      try {
        await emit('submit', { ...formData })
      } finally {
        uploading.value = false
      }
    }

    return {
      formData,
      imageUrl,
      imagePreview,
      uploading,
      itemNameInput,
      fileInput,
      handleImageChange,
      handleImageUrlChange,
      clearImage,
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
  overflow-y: auto;
}

.add-form {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 30px;
  width: 100%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 25px 45px rgba(0, 0, 0, 0.1);
}

.add-form h2 {
  margin: 0 0 25px 0;
  color: #333;
  text-align: center;
  font-size: 1.3em;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #555;
  font-weight: 500;
  font-size: 0.95em;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 12px 15px;
  border: 2px solid #e1e5e9;
  border-radius: 12px;
  font-size: 16px;
  transition: all 0.3s ease;
  box-sizing: border-box;
  font-family: inherit;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

.image-input-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.url-input-container {
  display: flex;
  gap: 10px;
  align-items: center;
}

.url-input {
  font-size: 14px;
  flex: 1;
}

.image-preview {
  position: relative;
  margin-top: 15px;
  display: inline-block;
}

.image-preview img {
  max-width: 200px;
  max-height: 150px;
  border-radius: 8px;
  border: 2px solid #e1e5e9;
}

.clear-image {
  position: absolute;
  top: -8px;
  right: -8px;
  background: #ff4757;
  color: white;
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  cursor: pointer;
  font-size: 16px;
  line-height: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.form-actions {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #e1e5e9;
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
  min-width: 100px;
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