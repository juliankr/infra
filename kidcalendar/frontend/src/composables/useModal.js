/**
 * Modal management composable
 */

import { ref } from 'vue'

export function useModal() {
  const isVisible = ref(false)
  const data = ref(null)

  function open(modalData = null) {
    data.value = modalData
    isVisible.value = true
  }

  function close() {
    isVisible.value = false
    data.value = null
  }

  function toggle() {
    if (isVisible.value) {
      close()
    } else {
      open()
    }
  }

  return {
    isVisible,
    data,
    open,
    close,
    toggle
  }
}

/**
 * Delete confirmation modal composable
 */
export function useDeleteModal() {
  const modal = useModal()
  const deleteType = ref('single')
  const isRecurring = ref(false)

  function openDeleteModal(event) {
    isRecurring.value = event.recurring_id || event.id.includes('recurring_')
    modal.open(event)
  }

  function setDeleteType(type) {
    deleteType.value = type
  }

  return {
    ...modal,
    deleteType,
    isRecurring,
    openDeleteModal,
    setDeleteType
  }
}
