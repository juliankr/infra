import axios from 'axios'

const API_BASE_URL = '/api'

class WishlistAPI {
  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json'
      }
    })
  }

  // Tab management
  async getTabs() {
    try {
      const response = await this.api.get('/tabs')
      return response.data
    } catch (error) {
      console.error('Error fetching tabs:', error)
      throw error
    }
  }

  async createTab(name) {
    try {
      const response = await this.api.post('/tabs', { name })
      return response.data
    } catch (error) {
      console.error('Error creating tab:', error)
      throw error
    }
  }

  async renameTab(tabId, name) {
    try {
      const response = await this.api.put(`/tabs/${tabId}`, { name })
      return response.data
    } catch (error) {
      console.error('Error renaming tab:', error)
      throw error
    }
  }

  async deleteTab(tabId) {
    try {
      const response = await this.api.delete(`/tabs/${tabId}`)
      return response.data
    } catch (error) {
      console.error('Error deleting tab:', error)
      throw error
    }
  }

  // Multi-tab wishlist operations
  async getTabWishlist(tabId) {
    try {
      const response = await this.api.get(`/tabs/${tabId}/wishlist`)
      return response.data
    } catch (error) {
      console.error('Error fetching tab wishlist:', error)
      throw error
    }
  }

  async addTabItem(tabId, itemData) {
    try {
      const response = await this.api.post(`/tabs/${tabId}/wishlist`, itemData)
      return response.data
    } catch (error) {
      console.error('Error adding tab item:', error)
      throw error
    }
  }

  async updateTabItem(tabId, itemId, itemData) {
    try {
      const response = await this.api.put(`/tabs/${tabId}/wishlist/${itemId}`, itemData)
      return response.data
    } catch (error) {
      console.error('Error updating tab item:', error)
      throw error
    }
  }

  async deleteTabItem(tabId, itemId) {
    try {
      const response = await this.api.delete(`/tabs/${tabId}/wishlist/${itemId}`)
      return response.data
    } catch (error) {
      console.error('Error deleting tab item:', error)
      throw error
    }
  }

  async reorderTabItems(tabId, itemIds) {
    try {
      const response = await this.api.post(`/tabs/${tabId}/wishlist/reorder`, { item_ids: itemIds })
      return response.data
    } catch (error) {
      console.error('Error reordering tab items:', error)
      throw error
    }
  }

  // Upload an image
  async uploadImage(file) {
    try {
      const formData = new FormData()
      formData.append('file', file)
      
      const response = await this.api.post('/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      return response.data
    } catch (error) {
      console.error('Error uploading image:', error)
      throw error
    }
  }

  // Download an image from URL
  async downloadImage(imageUrl) {
    try {
      const response = await this.api.post('/download-image', { url: imageUrl })
      return response.data
    } catch (error) {
      console.error('Error downloading image:', error)
      throw error
    }
  }

  // Get image URL
  getImageUrl(filename) {
    if (!filename) return null
    return `${API_BASE_URL}/images/${filename}`
  }

  // Health check
  async healthCheck() {
    try {
      const response = await this.api.get('/health')
      return response.data
    } catch (error) {
      console.error('Error checking health:', error)
      throw error
    }
  }
}

export default new WishlistAPI()