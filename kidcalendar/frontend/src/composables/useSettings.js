/**
 * Composable for managing application settings
 */

import { ref, computed } from 'vue'
import { configApi } from '../services/api'

const settings = ref({
  default_position: 1,
  default_color: '#FF6B6B',
  week_view_days: 7,
  week_start_offset: -1
})

const loading = ref(false)
const error = ref(null)

export function useSettings() {
  
  const loadSettings = async () => {
    loading.value = true
    error.value = null
    
    try {
      const response = await configApi.getSettings()
      settings.value = response.settings || response
    } catch (err) {
      error.value = err.message
      console.error('Failed to load settings:', err)
    } finally {
      loading.value = false
    }
  }

  // Computed getters for individual settings
  const defaultColor = computed(() => settings.value.default_color)
  const defaultPosition = computed(() => settings.value.default_position)
  const weekViewDays = computed(() => settings.value.week_view_days)
  const weekStartOffset = computed(() => settings.value.week_start_offset)

  return {
    // State
    settings,
    loading,
    error,
    
    // Methods
    loadSettings,
    
    // Computed settings
    defaultColor,
    defaultPosition,
    weekViewDays,
    weekStartOffset
  }
}
