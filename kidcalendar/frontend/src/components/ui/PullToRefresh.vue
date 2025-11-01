<template>
  <div 
    class="pull-to-refresh-container"
    @touchstart="handleTouchStart"
    @touchmove="handleTouchMove"
    @touchend="handleTouchEnd"
  >
    <!-- Pull-to-refresh indicator -->
    <div 
      v-if="pullToRefreshActive" 
      class="pull-to-refresh-indicator" 
      :style="{ transform: `translateY(${pullDistance}px)` }"
    >
      <div class="refresh-spinner" :class="{ spinning: isRefreshing }">
        {{ isRefreshing ? '🔄' : '⬇️' }}
      </div>
      <span class="refresh-text">
        {{ isRefreshing ? 'Aktualisiere...' : 'Zum Aktualisieren ziehen' }}
      </span>
    </div>

    <!-- Content slot -->
    <div class="content">
      <slot />
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { usePullToRefresh } from '../../composables/usePullToRefresh'

export default {
  name: 'PullToRefresh',
  props: {
    disabled: {
      type: Boolean,
      default: false
    }
  },
  emits: ['refresh'],
  setup(props, { emit }) {
    const {
      isActive: pullToRefreshActive,
      pullDistance,
      isRefreshing
    } = usePullToRefresh(() => emit('refresh'))

    // Simple touch handlers for basic functionality
    const handleTouchStart = (event) => {
      if (props.disabled) return
      // Touch handling will be managed by the composable
    }

    const handleTouchMove = (event) => {
      if (props.disabled) return
      // Touch handling will be managed by the composable
    }

    const handleTouchEnd = (event) => {
      if (props.disabled) return
      // Touch handling will be managed by the composable
    }

    return {
      pullToRefreshActive,
      pullDistance,
      isRefreshing,
      handleTouchStart,
      handleTouchMove,
      handleTouchEnd
    }
  }
}
</script>

<style scoped>
.pull-to-refresh-container {
  position: relative;
  overflow: hidden;
}

.pull-to-refresh-indicator {
  position: fixed;
  top: -80px;
  left: 0;
  right: 0;
  height: 80px;
  background: var(--color-primary);
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  transition: transform 0.3s ease;
}

.refresh-spinner {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  transition: transform 0.3s ease;
}

.refresh-spinner.spinning {
  animation: spin 1s linear infinite;
}

.refresh-text {
  font-size: 0.875rem;
  opacity: 0.9;
}

.content {
  min-height: 100vh;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
