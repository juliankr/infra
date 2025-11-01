/**
 * Touch and gesture utilities
 */

/**
 * Touch event handler for pull-to-refresh
 */
export class PullToRefreshHandler {
  constructor(options = {}) {
    this.threshold = options.threshold || 80
    this.maxDistance = options.maxDistance || 120
    this.damping = options.damping || 0.5
    
    this.isActive = false
    this.startY = 0
    this.pullDistance = 0
    this.isRefreshing = false
    
    this.onRefresh = options.onRefresh || (() => {})
    this.onStateChange = options.onStateChange || (() => {})
  }

  handleStart(event) {
    if (window.scrollY === 0) {
      this.startY = event.touches[0].clientY
      this.isActive = true
      this.onStateChange({ isActive: this.isActive })
    }
  }

  handleMove(event) {
    if (!this.isActive || this.isRefreshing) return

    const currentY = event.touches[0].clientY
    const pullDistance = Math.max(0, currentY - this.startY)
    
    if (pullDistance > 0 && window.scrollY === 0) {
      event.preventDefault() // Prevent scrolling
      this.pullDistance = Math.min(pullDistance * this.damping, this.maxDistance)
      this.onStateChange({ 
        pullDistance: this.pullDistance,
        canRefresh: this.pullDistance >= this.threshold
      })
    }
  }

  async handleEnd() {
    if (!this.isActive || this.isRefreshing) return

    if (this.pullDistance >= this.threshold) {
      await this.performRefresh()
    } else {
      this.reset()
    }
  }

  async performRefresh() {
    this.isRefreshing = true
    this.pullDistance = this.threshold
    
    this.onStateChange({ 
      isRefreshing: this.isRefreshing,
      pullDistance: this.pullDistance
    })
    
    try {
      await this.onRefresh()
      // Brief delay for user feedback
      await new Promise(resolve => setTimeout(resolve, 500))
    } catch (error) {
      console.error('Refresh failed:', error)
    } finally {
      this.reset()
    }
  }

  reset() {
    this.isRefreshing = false
    this.isActive = false
    this.pullDistance = 0
    this.startY = 0
    
    this.onStateChange({
      isActive: this.isActive,
      isRefreshing: this.isRefreshing,
      pullDistance: this.pullDistance
    })
  }
}
