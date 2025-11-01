import { ref } from 'vue'

export function useErrorHandling() {
  const error = ref('')

  const handleError = (message) => {
    error.value = message
    console.error('Error:', message)
  }

  const clearError = () => {
    error.value = ''
  }

  return {
    error,
    handleError,
    clearError
  }
}
