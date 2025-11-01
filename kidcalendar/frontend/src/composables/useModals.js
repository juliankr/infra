import { ref } from 'vue'

export function useModals() {
  const showEditModal = ref(false)
  const showDeleteModal = ref(false)
  const showYamlEditor = ref(false)
  
  const currentEditEvent = ref(null)
  const currentDeleteEvent = ref(null)
  const defaultEventDate = ref('')

  const closeEditModal = () => {
    showEditModal.value = false
    currentEditEvent.value = null
    defaultEventDate.value = ''
  }

  const closeDeleteModal = () => {
    showDeleteModal.value = false
    currentDeleteEvent.value = null
  }

  const closeYamlEditor = () => {
    showYamlEditor.value = false
  }

  const openYamlEditor = () => {
    showYamlEditor.value = true
  }

  return {
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
  }
}
