/**
 * Events management composable
 */

import { ref, computed } from 'vue'
import { eventsApi, recurringEventsApi } from '../services/api'
import { getEventsForDate, isRecurringInstance, sortEvents } from '../utils/events'

export function useEvents() {
  // State
  const events = ref([])
  const loading = ref(false)
  const error = ref(null)

  // Computed
  const sortedEvents = computed(() => sortEvents(events.value))

  // Methods
  async function loadEvents(offset = null) {
    loading.value = true
    error.value = null
    
    try {
      const response = await eventsApi.getEvents(null, offset)
      events.value = response.events || response
    } catch (err) {
      error.value = err.message
      console.error('Failed to load events:', err)
      
      // Fallback to mock data if available
      try {
        const mockResponse = await fetch('/mock-events.json')
        if (mockResponse.ok) {
          const mockData = await mockResponse.json()
          events.value = mockData.events || mockData
        }
      } catch (mockError) {
        console.error('Failed to load mock data:', mockError)
        events.value = []
      }
    } finally {
      loading.value = false
    }
  }

  async function createEvent(eventData) {
    try {
      await eventsApi.createEvent(eventData)
      await loadEvents() // Refresh events
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  async function updateEvent(eventId, eventData) {
    try {
      await eventsApi.updateEvent(eventId, eventData)
      await loadEvents() // Refresh events
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  async function deleteEvent(eventId, deleteType = 'single') {
    try {
      await eventsApi.deleteEvent(eventId, deleteType)
      await loadEvents() // Refresh events
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  async function getRecurringEventData(recurringId) {
    try {
      const response = await recurringEventsApi.getRecurringEvent(recurringId)
      return response.recurring_event
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  function getEventsForDay(date) {
    return getEventsForDate(events.value, date)
  }

  function isRecurringEventInstance(event) {
    return isRecurringInstance(event)
  }

  return {
    // State
    events: sortedEvents,
    loading,
    error,
    
    // Methods
    loadEvents,
    createEvent,
    updateEvent,
    deleteEvent,
    getRecurringEventData,
    getEventsForDay,
    isRecurringEventInstance
  }
}
