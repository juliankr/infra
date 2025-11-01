/**
 * Configuration constants for the Kids Calendar frontend
 */

export const API_CONFIG = {
  BASE_URL: '/api',
  ENDPOINTS: {
    EVENTS: '/events',
    IMAGES: '/images',
    CONFIG: '/config',
    SETTINGS: '/config/settings',
    RECURRING_EVENTS: '/recurring-events',
    HEALTH: '/health'
  }
}

export const UI_CONFIG = {
  PULL_TO_REFRESH: {
    THRESHOLD: 80,
    MAX_DISTANCE: 120,
    DAMPING: 0.5
  },
  CALENDAR: {
    DAYS_TO_SHOW: 7,  // This will be overridden by settings
    DAYS_BEFORE_TODAY: 2  // This will be calculated from week_start_offset
  },
  COLORS: {
    DEFAULT_EVENT: '#FF6B6B',  // This will be overridden by settings
    EDIT_MODE_GRADIENT: 'linear-gradient(135deg, #ff6b6b 0%, #ffa500 100%)',
    ADD_BUTTON: 'linear-gradient(135deg, #4CAF50 0%, #45a049 100%)',
    YAML_BUTTON: 'linear-gradient(135deg, #2196F3 0%, #1976D2 100%)'
  }
}

export const ANIMATION_CONFIG = {
  TRANSITION_DURATION: '0.3s',
  HOVER_SCALE: 1.1,
  ACTIVE_SCALE: 0.95
}

export const LANGUAGE = {
  LOCALE: 'de-DE',
  MESSAGES: {
    PULL_TO_REFRESH: 'Pull to refresh',
    REFRESHING: 'Refreshing events...',
    EDIT_MODE_ACTIVE: '✏️ Edit Mode Active',
    DELETE_CONFIRMATION: 'Event löschen?',
    DELETE_RECURRING_TITLE: 'Wiederkehrendes Event löschen',
    SAVE_ERROR: 'Fehler beim Speichern des Events',
    DELETE_ERROR: 'Fehler beim Löschen des Events',
    YAML_SAVE_SUCCESS: 'YAML-Konfiguration erfolgreich gespeichert!'
  }
}
