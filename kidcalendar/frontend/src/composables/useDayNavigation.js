/**
 * Composable for day-by-day navigation with swipe gestures
 * Allows users to navigate through days by swiping left/right
 */

import { ref, computed, onMounted, onUnmounted } from 'vue'
import { formatDateISO } from '../utils/date'

export function useDayNavigation() {
  const currentOffset = ref(0) // Days offset from today
  const isNavigating = ref(false)
  
  // Touch/swipe handling
  let touchStartX = 0
  let touchStartY = 0
  let touchStartTime = 0
  const minSwipeDistance = 50
  const maxSwipeTime = 300
  const maxVerticalDistance = 100

  // Computed current date based on offset
  const currentDate = computed(() => {
    const date = new Date()
    date.setDate(date.getDate() + currentOffset.value)
    return date
  })

  // Navigation functions
  const goToPreviousDay = () => {
    isNavigating.value = true
    currentOffset.value -= 1
    setTimeout(() => {
      isNavigating.value = false
    }, 300)
  }

  const goToNextDay = () => {
    isNavigating.value = true
    currentOffset.value += 1
    setTimeout(() => {
      isNavigating.value = false
    }, 300)
  }

  const goToToday = () => {
    isNavigating.value = true
    currentOffset.value = 0
    setTimeout(() => {
      isNavigating.value = false
    }, 300)
  }

  // Touch event handlers
  const handleTouchStart = (event) => {
    if (event.touches.length !== 1) return
    
    const touch = event.touches[0]
    touchStartX = touch.clientX
    touchStartY = touch.clientY
    touchStartTime = Date.now()
  }

  const handleTouchEnd = (event) => {
    if (event.changedTouches.length !== 1) return
    
    const touch = event.changedTouches[0]
    const touchEndX = touch.clientX
    const touchEndY = touch.clientY
    const touchEndTime = Date.now()
    
    const deltaX = touchEndX - touchStartX
    const deltaY = touchEndY - touchStartY
    const deltaTime = touchEndTime - touchStartTime
    
    // Check if it's a valid swipe
    if (
      Math.abs(deltaX) > minSwipeDistance && // Minimum horizontal distance
      Math.abs(deltaY) < maxVerticalDistance && // Maximum vertical distance (to avoid conflicting with pull-to-refresh)
      deltaTime < maxSwipeTime && // Maximum time
      Math.abs(deltaX) > Math.abs(deltaY) // More horizontal than vertical
    ) {
      if (deltaX > 0) {
        // Swipe right - go to previous day
        goToPreviousDay()
      } else {
        // Swipe left - go to next day
        goToNextDay()
      }
    }
  }

  // Mouse event handlers for desktop testing
  let mouseStartX = 0
  let mouseStartY = 0
  let mouseStartTime = 0
  let isMouseDown = false

  const handleMouseDown = (event) => {
    isMouseDown = true
    mouseStartX = event.clientX
    mouseStartY = event.clientY
    mouseStartTime = Date.now()
  }

  const handleMouseUp = (event) => {
    if (!isMouseDown) return
    isMouseDown = false
    
    const deltaX = event.clientX - mouseStartX
    const deltaY = event.clientY - mouseStartY
    const deltaTime = Date.now() - mouseStartTime
    
    // Check if it's a valid swipe
    if (
      Math.abs(deltaX) > minSwipeDistance &&
      Math.abs(deltaY) < maxVerticalDistance &&
      deltaTime < maxSwipeTime &&
      Math.abs(deltaX) > Math.abs(deltaY)
    ) {
      if (deltaX > 0) {
        goToPreviousDay()
      } else {
        goToNextDay()
      }
    }
  }

  // Setup event listeners
  const setupGestureListeners = (element) => {
    if (!element) return

    // Touch events for mobile
    element.addEventListener('touchstart', handleTouchStart, { passive: true })
    element.addEventListener('touchend', handleTouchEnd, { passive: true })
    
    // Mouse events for desktop testing
    element.addEventListener('mousedown', handleMouseDown)
    element.addEventListener('mouseup', handleMouseUp)
  }

  const removeGestureListeners = (element) => {
    if (!element) return

    element.removeEventListener('touchstart', handleTouchStart)
    element.removeEventListener('touchend', handleTouchEnd)
    element.removeEventListener('mousedown', handleMouseDown)
    element.removeEventListener('mouseup', handleMouseUp)
  }

  // Keyboard navigation
  const handleKeydown = (event) => {
    if (event.key === 'ArrowLeft') {
      event.preventDefault()
      goToPreviousDay()
    } else if (event.key === 'ArrowRight') {
      event.preventDefault()
      goToNextDay()
    } else if (event.key === 'Home' || (event.key === 't' && event.ctrlKey)) {
      event.preventDefault()
      goToToday()
    }
  }

  onMounted(() => {
    document.addEventListener('keydown', handleKeydown)
  })

  onUnmounted(() => {
    document.removeEventListener('keydown', handleKeydown)
  })

  return {
    currentOffset,
    currentDate,
    isNavigating,
    goToPreviousDay,
    goToNextDay,
    goToToday,
    setupGestureListeners,
    removeGestureListeners
  }
}
