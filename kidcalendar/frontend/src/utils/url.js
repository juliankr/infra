/**
 * URL and navigation utilities
 */

/**
 * Check if edit mode is enabled via URL parameters
 */
export function checkEditModeFromUrl() {
  const urlParams = new URLSearchParams(window.location.search)
  return urlParams.get('admin') === 'true' || urlParams.get('edit') === '1'
}

/**
 * Exit edit mode by removing URL parameters
 */
export function exitEditMode() {
  const url = new URL(window.location)
  url.searchParams.delete('admin')
  url.searchParams.delete('edit')
  window.history.replaceState({}, document.title, url.pathname)
}

/**
 * Create query string from object
 */
export function createQueryString(params) {
  return new URLSearchParams(params).toString()
}
