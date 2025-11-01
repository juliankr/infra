/**
 * Edit mode management composable
 */

import { ref, onMounted } from 'vue'
import { checkEditModeFromUrl, exitEditMode as exitEditModeUtil } from '../utils/url'

export function useEditMode() {
  const isEditMode = ref(false)

  function checkEditMode() {
    isEditMode.value = checkEditModeFromUrl()
    
    if (isEditMode.value) {
      console.log('Edit mode enabled via URL parameter')
    }
  }

  function exitEditMode() {
    isEditMode.value = false
    exitEditModeUtil()
  }

  function toggleEditMode() {
    if (isEditMode.value) {
      exitEditMode()
    } else {
      isEditMode.value = true
    }
  }

  onMounted(checkEditMode)

  return {
    isEditMode,
    exitEditMode,
    toggleEditMode
  }
}
