/**
 * Event management utilities
 */

/**
 * Filter events by date
 */
export function getEventsForDate(events, targetDate) {
  return events.filter(event => event.date === targetDate)
}

/**
 * Check if event is recurring
 */
export function isRecurringEvent(event) {
  return event.recurring_id || event.id.includes('recurring_')
}

/**
 * Check if event is recurring instance (has date suffix)
 */
export function isRecurringInstance(event) {
  return event.id.includes('recurring_') && event.id.match(/-\d{8}$/)
}

/**
 * Sort events by position and title
 */
export function sortEvents(events) {
  return events.sort((a, b) => {
    // First by position
    const positionA = a.position || 1
    const positionB = b.position || 1
    
    if (positionA !== positionB) {
      return positionA - positionB
    }
    
    // Then by title
    return a.title.localeCompare(b.title)
  })
}

/**
 * Create default event data with optional settings
 */
export function createDefaultEvent(date = null, settings = null) {
  const defaultColor = settings?.default_color || '#FF6B6B';
  const defaultPosition = settings?.default_position || 1;
  
  return {
    id: null,
    title: '',
    date: date || new Date().toISOString().split('T')[0],
    color: defaultColor,
    image: null,
    position: defaultPosition,
    description: '',
    isRecurring: false,
    recurring: {
      frequency: 'weekly',
      daysOfWeek: [],
      intervalDays: 2,
      endDate: ''
    }
  }
}

/**
 * Transform event data for API
 */
export function transformEventForApi(eventData) {
  const apiEvent = {
    title: eventData.title,
    date: eventData.date,
    color: eventData.color,
    image: eventData.image,
    position: eventData.position,
    description: eventData.description
  }
  
  // Add recurring data if needed
  if (eventData.isRecurring) {
    apiEvent.recurring = eventData.recurring
  }
  
  return apiEvent
}
