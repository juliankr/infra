/**
 * Composable for handling page visibility changes
 * Refreshes the app when user returns from background/other tabs
 */

import { ref, onMounted, onUnmounted } from 'vue'

export function usePageVisibility(onVisibilityChange) {
  const isVisible = ref(!document.hidden)
  const lastVisibleTime = ref(Date.now())

  const handleVisibilityChange = () => {
    const wasVisible = isVisible.value
    isVisible.value = !document.hidden
    
    if (!wasVisible && isVisible.value) {
      // App became visible again
      const timeSinceLastVisible = Date.now() - lastVisibleTime.value
      const minutesAway = timeSinceLastVisible / (1000 * 60)
      
      console.log(`App became visible after ${Math.round(minutesAway)} minutes`)
      
      // Refresh if user was away for more than 5 minutes or if date might have changed
      if (minutesAway > 5 || timeSinceLastVisible > 1000 * 60 * 60) { // 1 hour
        if (onVisibilityChange) {
          onVisibilityChange(timeSinceLastVisible)
        }
      }
    }
    
    if (isVisible.value) {
      lastVisibleTime.value = Date.now()
    }
  }

  onMounted(() => {
    document.addEventListener('visibilitychange', handleVisibilityChange)
    // Also listen for focus events as backup
    window.addEventListener('focus', handleVisibilityChange)
  })

  onUnmounted(() => {
    document.removeEventListener('visibilitychange', handleVisibilityChange)
    window.removeEventListener('focus', handleVisibilityChange)
  })

  return {
    isVisible,
    lastVisibleTime
  }
}
