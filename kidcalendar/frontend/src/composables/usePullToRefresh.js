/**
 * Pull-to-refresh composable
 */

import { ref, onMounted, onUnmounted } from 'vue'
import { PullToRefreshHandler } from '../utils/touch'
import { UI_CONFIG } from '../config'

export function usePullToRefresh(onRefresh) {
  const isActive = ref(false)
  const isRefreshing = ref(false)
  const pullDistance = ref(0)
  const canRefresh = ref(false)
  
  let handler = null

  function handleStateChange(state) {
    if (state.isActive !== undefined) isActive.value = state.isActive
    if (state.isRefreshing !== undefined) isRefreshing.value = state.isRefreshing
    if (state.pullDistance !== undefined) pullDistance.value = state.pullDistance
    if (state.canRefresh !== undefined) canRefresh.value = state.canRefresh
  }

  function setupPullToRefresh() {
    handler = new PullToRefreshHandler({
      threshold: UI_CONFIG.PULL_TO_REFRESH.THRESHOLD,
      maxDistance: UI_CONFIG.PULL_TO_REFRESH.MAX_DISTANCE,
      damping: UI_CONFIG.PULL_TO_REFRESH.DAMPING,
      onRefresh,
      onStateChange: handleStateChange
    })

    // Add event listeners
    document.addEventListener('touchstart', handler.handleStart.bind(handler))
    document.addEventListener('touchmove', handler.handleMove.bind(handler))
    document.addEventListener('touchend', handler.handleEnd.bind(handler))
  }

  function cleanup() {
    if (handler) {
      document.removeEventListener('touchstart', handler.handleStart.bind(handler))
      document.removeEventListener('touchmove', handler.handleMove.bind(handler))
      document.removeEventListener('touchend', handler.handleEnd.bind(handler))
      handler = null
    }
  }

  onMounted(setupPullToRefresh)
  onUnmounted(cleanup)

  return {
    isActive,
    isRefreshing,
    pullDistance,
    canRefresh
  }
}
