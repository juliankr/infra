/**
 * Date utility functions for the Kids Calendar application
 */

/**
 * Check if two dates are the same day
 */
export function isSameDay(date1, date2) {
  return date1.toDateString() === date2.toDateString()
}

/**
 * Format date to YYYY-MM-DD string
 */
export function formatDateISO(date) {
  return date.toISOString().split('T')[0]
}

/**
 * Generate week days array for calendar display
 */
export function generateWeekDays(daysBefore = 2, totalDays = 7, settings = null, referenceDate = null) {
  let actualDaysBefore = daysBefore;
  let actualTotalDays = totalDays;
  
  // Use settings if provided
  if (settings) {
    actualTotalDays = settings.week_view_days || totalDays;
    // week_start_offset: 0 means start from today
    // week_start_offset: -1 means start 1 day ago 
    // week_start_offset: -2 means start 2 days ago (current default)
    if (typeof settings.week_start_offset === 'number') {
      actualDaysBefore = Math.abs(settings.week_start_offset);
    }
  }
  
  const today = new Date()
  const baseDate = referenceDate || today
  const days = []
  
  // Calculate the start date
  const startDate = new Date(baseDate)
  startDate.setDate(baseDate.getDate() - actualDaysBefore)
  
  // Generate days
  for (let i = 0; i < actualTotalDays; i++) {
    const currentDate = new Date(startDate)
    currentDate.setDate(startDate.getDate() + i)
    
    const isToday = isSameDay(currentDate, today)
    const isPast = currentDate < today && !isToday
    const isFuture = currentDate > today
    
    days.push({
      dayName: currentDate.toLocaleDateString('de-DE', { weekday: 'short' }),
      date: currentDate.toLocaleDateString('de-DE', { month: 'short' }),
      dayNumber: currentDate.getDate(),
      fullDate: formatDateISO(currentDate),
      isToday,
      isPast,
      isFuture,
      dateObject: new Date(currentDate)
    })
  }
  
  return days
}

/**
 * Get today's date in YYYY-MM-DD format
 */
export function getTodayISO() {
  return formatDateISO(new Date())
}

/**
 * Parse date string to Date object
 */
export function parseDate(dateString) {
  return new Date(dateString)
}

/**
 * Format date for display
 */
export function formatDateDisplay(date, options = {}) {
  const defaultOptions = {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }
  
  return date.toLocaleDateString('de-DE', { ...defaultOptions, ...options })
}
