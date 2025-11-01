/**
 * API service layer for the Kids Calendar application
 */

import { API_CONFIG } from '../config'

class ApiService {
  constructor() {
    this.baseUrl = API_CONFIG.BASE_URL
  }

  /**
   * Generic API request method
   */
  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`
    
    const defaultOptions = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      }
    }

    const requestOptions = { ...defaultOptions, ...options }

    try {
      const response = await fetch(url, requestOptions)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      return await response.json()
    } catch (error) {
      console.error(`API request failed for ${endpoint}:`, error)
      throw error
    }
  }

  /**
   * Upload file (multipart/form-data)
   */
  async uploadFile(endpoint, file) {
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        method: 'POST',
        body: formData
      })

      if (!response.ok) {
        throw new Error(`Upload failed! status: ${response.status}`)
      }

      return await response.json()
    } catch (error) {
      console.error(`File upload failed for ${endpoint}:`, error)
      throw error
    }
  }
}

// Create singleton instance
const apiService = new ApiService()

/**
 * Events API
 */
export const eventsApi = {
  // Get all events (current week, specific date, or with offset)
  async getEvents(date = null, offset = null) {
    let endpoint = API_CONFIG.ENDPOINTS.EVENTS
    
    if (date) {
      endpoint += `?date=${date}`
    } else if (offset !== null) {
      endpoint += `?offset=${offset}`
    }
    
    return apiService.request(endpoint)
  },

  // Get events for date range
  async getEventsRange(startDate, endDate) {
    const endpoint = `${API_CONFIG.ENDPOINTS.EVENTS}/range?start_date=${startDate}&end_date=${endDate}`
    return apiService.request(endpoint)
  },

  // Get single event by ID
  async getEvent(eventId) {
    return apiService.request(`${API_CONFIG.ENDPOINTS.EVENTS}/${eventId}`)
  },

  // Create new event
  async createEvent(eventData) {
    return apiService.request(API_CONFIG.ENDPOINTS.EVENTS, {
      method: 'POST',
      body: JSON.stringify(eventData)
    })
  },

  // Update existing event
  async updateEvent(eventId, eventData) {
    return apiService.request(`${API_CONFIG.ENDPOINTS.EVENTS}/${eventId}`, {
      method: 'PUT',
      body: JSON.stringify(eventData)
    })
  },

  // Delete event
  async deleteEvent(eventId, deleteType = 'single') {
    // Handle recurring events - extract recurring ID and date
    if (eventId.includes('-') && eventId.match(/recurring_.*-\d{8}$/)) {
      // This is a generated recurring event ID (e.g., recurring_abc-123-20250911)
      const parts = eventId.split('-')
      const dateStr = parts[parts.length - 1] // Get the date part (20250911)
      const recurringId = parts.slice(0, -1).join('-') // Get the recurring ID part
      
      // Convert YYYYMMDD to YYYY-MM-DD
      const formattedDate = `${dateStr.substring(0, 4)}-${dateStr.substring(4, 6)}-${dateStr.substring(6, 8)}`
      
      const endpoint = `${API_CONFIG.ENDPOINTS.EVENTS}/${recurringId}?delete_type=${deleteType}&event_date=${formattedDate}`
      return apiService.request(endpoint, {
        method: 'DELETE'
      })
    } else {
      // Regular one-time event
      const endpoint = `${API_CONFIG.ENDPOINTS.EVENTS}/${eventId}?delete_type=${deleteType}`
      return apiService.request(endpoint, {
        method: 'DELETE'
      })
    }
  }
}

/**
 * Recurring Events API
 */
export const recurringEventsApi = {
  // Get all recurring event patterns
  async getRecurringEvents() {
    return apiService.request(API_CONFIG.ENDPOINTS.RECURRING_EVENTS)
  },

  // Get specific recurring event pattern
  async getRecurringEvent(recurringId) {
    return apiService.request(`${API_CONFIG.ENDPOINTS.RECURRING_EVENTS}/${recurringId}`)
  }
}

/**
 * Images API
 */
export const imagesApi = {
  // Get all available images
  async getImages() {
    return apiService.request(API_CONFIG.ENDPOINTS.IMAGES)
  },

  // Upload new image
  async uploadImage(file) {
    return apiService.uploadFile(`${API_CONFIG.ENDPOINTS.IMAGES}/upload`, file)
  },

  // Delete image
  async deleteImage(filename) {
    return apiService.request(`${API_CONFIG.ENDPOINTS.IMAGES}/${filename}`, {
      method: 'DELETE'
    })
  }
}

/**
 * Configuration API
 */
export const configApi = {
  // Get current configuration
  async getConfig() {
    return apiService.request(API_CONFIG.ENDPOINTS.CONFIG)
  },

  // Get settings with defaults
  async getSettings() {
    return apiService.request(API_CONFIG.ENDPOINTS.SETTINGS)
  },

  // Get raw YAML configuration
  async getYamlConfig() {
    return apiService.request(`${API_CONFIG.ENDPOINTS.CONFIG}/yaml`)
  },

  // Update YAML configuration
  async updateYamlConfig(yamlContent) {
    return apiService.request(`${API_CONFIG.ENDPOINTS.CONFIG}/yaml`, {
      method: 'PUT',
      body: JSON.stringify({ yaml_content: yamlContent })
    })
  },

  // Trigger data cleanup
  async cleanup() {
    return apiService.request(`${API_CONFIG.ENDPOINTS.CONFIG}/cleanup`, {
      method: 'POST'
    })
  }
}

/**
 * Health API
 */
export const healthApi = {
  // Get health status
  async getHealth() {
    return apiService.request(API_CONFIG.ENDPOINTS.HEALTH)
  }
}
