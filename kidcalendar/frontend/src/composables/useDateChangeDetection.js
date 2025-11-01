/**
 * Composable for handling date change detection
 * Automatically refreshes the app when the date changes (e.g., at midnight)
 */

import { ref, onMounted, onUnmounted } from 'vue'

export function useDateChangeDetection(onDateChange) {
  const currentDate = ref(new Date().toDateString())
  let intervalId = null
  let midnightTimeoutId = null

  const checkDateChange = () => {
    const newDate = new Date().toDateString()
    if (newDate !== currentDate.value) {
      console.log('Date changed detected:', currentDate.value, '->', newDate)
      currentDate.value = newDate
      if (onDateChange) {
        onDateChange()
      }
      scheduleNextMidnightCheck()
    }
  }

  const scheduleNextMidnightCheck = () => {
    // Clear existing timeout
    if (midnightTimeoutId) {
      clearTimeout(midnightTimeoutId)
    }

    // Calculate milliseconds until next midnight
    const now = new Date()
    const midnight = new Date(now)
    midnight.setHours(24, 0, 0, 0) // Next midnight
    
    const msUntilMidnight = midnight.getTime() - now.getTime()
    
    console.log(`Scheduling date change check in ${Math.round(msUntilMidnight / 1000 / 60)} minutes`)
    
    // Set timeout for midnight + 1 second to ensure date has changed
    midnightTimeoutId = setTimeout(() => {
      checkDateChange()
    }, msUntilMidnight + 1000)
  }

  const startDateMonitoring = () => {
    // Check every minute for date changes (backup)
    intervalId = setInterval(checkDateChange, 60 * 1000)
    
    // Schedule precise midnight check
    scheduleNextMidnightCheck()
  }

  const stopDateMonitoring = () => {
    if (intervalId) {
      clearInterval(intervalId)
      intervalId = null
    }
    if (midnightTimeoutId) {
      clearTimeout(midnightTimeoutId)
      midnightTimeoutId = null
    }
  }

  onMounted(() => {
    startDateMonitoring()
  })

  onUnmounted(() => {
    stopDateMonitoring()
  })

  return {
    currentDate,
    checkDateChange,
    startDateMonitoring,
    stopDateMonitoring
  }
}
