<template>
  <div class="app">
    <!-- Pull to Refresh Indicator -->
    <div class="pull-refresh-indicator" :class="{ 'visible': pullRefreshVisible, 'refreshing': isRefreshing }">
      <div class="refresh-icon">
        <span v-if="!isRefreshing">↓</span>
        <div v-else class="spinner"></div>
      </div>
      <span class="refresh-text">
        {{ isRefreshing ? 'Refreshing...' : (pullRefreshVisible ? 'Release to refresh' : 'Pull to refresh') }}
      </span>
    </div>

    <div 
      class="main-content"
      @touchstart="handleTouchStart"
      @touchmove="handleTouchMove"
      @touchend="handleTouchEnd"
    >
      <!-- Loading State -->
      <LoadingSpinner v-if="loading" message="Loading your wishlist..." />

      <!-- Error State -->
      <ErrorMessage 
        v-else-if="error" 
        :message="error"
        :show-retry="true"
        @retry="loadData"
      />

      <!-- Main Content -->
      <div v-else>
        <!-- Tab Navigation -->
        <TabNavigation 
          :tabs="tabs"
          :current-tab="currentTab"
          :edit-mode="isEditMode"
          :show-add-form="showAddForm"
          :editing-item="editingItem"
          :show-add-tab-form="showAddTabForm"
          @switch-tab="switchTab"
          @edit-tab="startEditTab"
          @delete-tab="deleteTab"
          @add-tab="showAddTabForm = true"
          @add-item="showAddForm = true"
        />

        <!-- Wishlist Content -->
        <div class="wishlist-container">
          <!-- Empty State -->
          <div v-if="!currentTab" class="empty-state">
            <div class="empty-icon">📝</div>
            <h3>No tabs yet!</h3>
            <p>Create your first tab to start building your wishlist</p>
          </div>

          <div v-else-if="wishlist.length === 0" class="empty-state">
            <div class="empty-icon">🎁</div>
            <h3>{{ currentTab.name }} is empty</h3>
            <p>Add your first item to start building this wishlist</p>
          </div>

          <!-- Wishlist Items -->
          <WishlistGrid 
            v-else
            v-model:wishlist="wishlist"
            @edit-item="startEdit"
            @delete-item="deleteItem"
            @reorder="onDragEnd"
          />
        </div>
      </div>
    </div>

    <!-- Forms -->
    <TabForm 
      :show="showAddTabForm"
      :is-editing="!!editingTab"
      :tab-name="newTabName"
      @submit="handleTabSubmit"
      @cancel="cancelTabForm"
    />

    <AddItemForm 
      :show="showAddForm"
      @submit="addItem"
      @cancel="cancelAdd"
    />

    <EditItemForm 
      :show="!!editingItem"
      :item="editingItem"
      @submit="updateItem"
      @cancel="cancelEdit"
    />
  </div>
</template>
<script>
import { ref, reactive, onMounted } from 'vue'
import api from './api.js'

// Import components
import TabForm from './components/forms/TabForm.vue'
import AddItemForm from './components/forms/AddItemForm.vue'
import EditItemForm from './components/forms/EditItemForm.vue'
import TabNavigation from './components/ui/TabNavigation.vue'
import LoadingSpinner from './components/ui/LoadingSpinner.vue'
import ErrorMessage from './components/ui/ErrorMessage.vue'
import WishlistGrid from './components/wishlist/WishlistGrid.vue'

export default {
  name: 'WishlistApp',
  components: {
    TabForm,
    AddItemForm,
    EditItemForm,
    TabNavigation,
    LoadingSpinner,
    ErrorMessage,
    WishlistGrid
  },
  setup() {
    const tabs = ref([])
    const currentTab = ref(null)
    const wishlist = ref([])
    const loading = ref(true)
    const error = ref(null)
    const showAddForm = ref(false)
    const showAddTabForm = ref(false)
    const editingItem = ref(null)
    const editingTab = ref(null)
    const newTabName = ref('')

    // Pull to refresh variables
    const pullRefreshVisible = ref(false)
    const isRefreshing = ref(false)
    const touchStartY = ref(0)
    const pullDistance = ref(0)
    const PULL_THRESHOLD = 60

    // Editing mode variable
    const isEditMode = ref(false)

    onMounted(() => {
      // Check for edit mode from URL parameters
      const urlParams = new URLSearchParams(window.location.search)
      isEditMode.value = urlParams.get('edit') === '1'
      
      loadData()
    })

    const loadData = async () => {
      try {
        loading.value = true
        error.value = null
        
        const tabsResponse = await api.getTabs()
        if (tabsResponse.success) {
          tabs.value = tabsResponse.data
          
          if (tabs.value.length > 0 && !currentTab.value) {
            currentTab.value = tabs.value[0]
          }
          
          if (currentTab.value) {
            await loadWishlist()
          }
        } else {
          throw new Error(tabsResponse.error || 'Failed to load tabs')
        }
      } catch (err) {
        error.value = 'Failed to load data. Please try again.'
        console.error('Error loading data:', err)
      } finally {
        loading.value = false
      }
    }

    const loadWishlist = async () => {
      if (!currentTab.value) return
      
      try {
        const response = await api.getTabWishlist(currentTab.value.id)
        if (response.success) {
          wishlist.value = response.data
        } else {
          throw new Error(response.error || 'Failed to load wishlist')
        }
      } catch (err) {
        error.value = 'Failed to load wishlist. Please try again.'
        console.error('Error loading wishlist:', err)
      }
    }

    const switchTab = async (tab) => {
      if (currentTab.value?.id === tab.id) return
      
      currentTab.value = tab
      await loadWishlist()
    }

    const createTab = async (tabName) => {
      try {
        const response = await api.createTab(tabName)
        
        if (response.success) {
          tabs.value.push(response.data)
          currentTab.value = response.data
          wishlist.value = []
          cancelTabForm()
        } else {
          throw new Error(response.error || 'Failed to create tab')
        }
      } catch (err) {
        alert('Failed to create tab: ' + err.message)
      }
    }

    const handleTabSubmit = async (tabName) => {
      if (editingTab.value) {
        await updateTab(tabName)
      } else {
        await createTab(tabName)
      }
    }

    const startEditTab = (tab) => {
      editingTab.value = tab
      newTabName.value = tab.name
      showAddTabForm.value = true
    }

    const updateTab = async (tabName) => {
      try {
        const response = await api.renameTab(editingTab.value.id, tabName)
        
        if (response.success) {
          editingTab.value.name = tabName
          cancelTabForm()
        } else {
          throw new Error(response.error || 'Failed to rename tab')
        }
      } catch (err) {
        alert('Failed to rename tab: ' + err.message)
      }
    }

    const deleteTab = async (tab) => {
      if (tabs.value.length <= 1) {
        alert('Cannot delete the last tab.')
        return
      }
      
      if (!confirm(`Are you sure you want to delete "${tab.name}" and all its items?`)) {
        return
      }

      try {
        const response = await api.deleteTab(tab.id)
        
        if (response.success) {
          const tabIndex = tabs.value.findIndex(t => t.id === tab.id)
          tabs.value.splice(tabIndex, 1)
          
          if (currentTab.value?.id === tab.id) {
            currentTab.value = tabs.value[0] || null
            if (currentTab.value) {
              await loadWishlist()
            } else {
              wishlist.value = []
            }
          }
        } else {
          throw new Error(response.error || 'Failed to delete tab')
        }
      } catch (err) {
        alert('Failed to delete tab: ' + err.message)
      }
    }

    const cancelTabForm = () => {
      showAddTabForm.value = false
      editingTab.value = null
      newTabName.value = ''
    }

    const addItem = async (itemData) => {
      if (!currentTab.value) return
      
      try {
        // Determine if image is a URL or a filename
        const isImageUrl = typeof itemData.image === 'string' && itemData.image.startsWith('http')
        
        const response = await api.addTabItem(currentTab.value.id, {
          title: itemData.name,
          weblink: itemData.link || null,
          image: isImageUrl ? null : (itemData.image || null),
          image_url: isImageUrl ? itemData.image : null
        })

        if (response.success) {
          wishlist.value.push(response.data)
          showAddForm.value = false
        } else {
          throw new Error(response.error || 'Failed to add item')
        }
      } catch (err) {
        alert('Failed to add item: ' + err.message)
      }
    }

    const startEdit = (item) => {
      editingItem.value = item
      editForm.title = item.title
      editForm.weblink = item.weblink || ''
      editForm.image = item.image || ''
      editForm.imageUrl = ''
    }

    const updateItem = async (itemData) => {
      if (!currentTab.value) return
      
      try {
        // Determine if image is a URL or a filename
        const isImageUrl = typeof itemData.image === 'string' && itemData.image.startsWith('http')
        
        const response = await api.updateTabItem(currentTab.value.id, editingItem.value.id, {
          title: itemData.name,
          weblink: itemData.link || null,
          image: isImageUrl ? null : (itemData.image || null),
          image_url: isImageUrl ? itemData.image : null
        })

        if (response.success) {
          const index = wishlist.value.findIndex(item => item.id === editingItem.value.id)
          if (index !== -1) {
            wishlist.value[index] = response.data
          }
          cancelEdit()
        } else {
          throw new Error(response.error || 'Failed to update item')
        }
      } catch (err) {
        alert('Failed to update item: ' + err.message)
      }
    }
    const deleteItem = async (item) => {
      if (!currentTab.value) return
      
      if (!confirm(`Are you sure you want to delete "${item.title}"?`)) {
        return
      }

      try {
        const response = await api.deleteTabItem(currentTab.value.id, item.id)
        
        if (response.success) {
          wishlist.value = wishlist.value.filter(i => i.id !== item.id)
        } else {
          throw new Error(response.error || 'Failed to delete item')
        }
      } catch (err) {
        alert('Failed to delete item: ' + err.message)
      }
    }

    const onDragEnd = async () => {
      if (!currentTab.value) return
      
      const itemIds = wishlist.value.map(item => item.id)
      
      try {
        const response = await api.reorderTabItems(currentTab.value.id, itemIds)
        
        if (!response.success) {
          await loadWishlist()
          alert('Failed to save new order: ' + response.error)
        }
      } catch (err) {
        await loadWishlist()
        alert('Failed to save new order: ' + err.message)
      }
    }

    const cancelAdd = () => {
      showAddForm.value = false
    }

    const cancelEdit = () => {
      editingItem.value = null
    }

    // Pull to refresh functions
    const handleTouchStart = (e) => {
      if (window.scrollY === 0 && !isRefreshing.value) {
        touchStartY.value = e.touches[0].clientY
      }
    }

    const handleTouchMove = (e) => {
      if (window.scrollY === 0 && !isRefreshing.value && touchStartY.value > 0) {
        const currentY = e.touches[0].clientY
        pullDistance.value = Math.max(0, currentY - touchStartY.value)
        
        if (pullDistance.value > 30) {
          pullRefreshVisible.value = true
          e.preventDefault() // Prevent default scroll behavior
        }
        
        // Update the visual feedback based on pull distance
        const mainContent = e.currentTarget
        if (pullDistance.value > 0) {
          mainContent.style.transform = `translateY(${Math.min(pullDistance.value * 0.5, 50)}px)`
        }
      }
    }

    const handleTouchEnd = async () => {
      if (pullRefreshVisible.value && pullDistance.value > PULL_THRESHOLD && !isRefreshing.value) {
        isRefreshing.value = true
        
        try {
          // Perform the refresh
          await loadData()
        } catch (err) {
          console.error('Refresh failed:', err)
        } finally {
          // Reset everything
          setTimeout(() => {
            isRefreshing.value = false
            pullRefreshVisible.value = false
            pullDistance.value = 0
            touchStartY.value = 0
            
            // Reset transform
            const mainContent = document.querySelector('.main-content')
            if (mainContent) {
              mainContent.style.transform = ''
            }
          }, 500)
        }
      } else {
        // Reset if not enough pull distance
        pullRefreshVisible.value = false
        pullDistance.value = 0
        touchStartY.value = 0
        
        // Reset transform
        const mainContent = document.querySelector('.main-content')
        if (mainContent) {
          mainContent.style.transform = ''
        }
      }
    }

    return {
      tabs,
      currentTab,
      wishlist,
      loading,
      error,
      showAddForm,
      showAddTabForm,
      editingItem,
      editingTab,
      newTabName,
      loadData,
      switchTab,
      handleTabSubmit,
      startEditTab,
      deleteTab,
      cancelTabForm,
      addItem,
      startEdit,
      updateItem,
      deleteItem,
      onDragEnd,
      cancelAdd,
      cancelEdit,
      // Edit mode
      isEditMode,
      // Pull to refresh
      pullRefreshVisible,
      isRefreshing,
      handleTouchStart,
      handleTouchMove,
      handleTouchEnd
    }
  }
}
</script>

<style scoped>
.app {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
  color: white;
  position: relative;
}

/* Pull to Refresh Styles */
.pull-refresh-indicator {
  position: fixed;
  top: -80px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(255, 255, 255, 0.95);
  color: #333;
  padding: 15px 20px;
  border-radius: 25px;
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  z-index: 1000;
  transition: all 0.3s ease;
  font-weight: 500;
}

.pull-refresh-indicator.visible {
  top: 20px;
}

.pull-refresh-indicator.refreshing {
  top: 20px;
}

.refresh-icon {
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  transition: transform 0.3s ease;
}

.pull-refresh-indicator.visible .refresh-icon {
  transform: rotate(180deg);
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid #ddd;
  border-top: 2px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.refresh-text {
  font-size: 14px;
  white-space: nowrap;
}

.main-content {
  transition: transform 0.2s ease;
  position: relative;
  z-index: 1;
}

.tabs-container {
  width: 100%;
  margin: 0 auto 30px auto;
  padding: 0 20px;
}

.tabs-nav {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  overflow-x: auto;
  padding: 10px 0;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.tabs-nav::-webkit-scrollbar {
  display: none;
}

.tab-button {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 20px;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
  white-space: nowrap;
  font-size: 16px;
  min-width: 120px;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  backdrop-filter: blur(10px);
}

.tab-button.active {
  background: linear-gradient(45deg, #FE6B8B 30%, #FF8E53 90%);
  box-shadow: 0 4px 15px rgba(255, 105, 135, .4);
  transform: translateY(-2px);
}

.tab-button:hover:not(.active) {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-1px);
}

.tab-name {
  flex: 1;
}

.tab-actions {
  display: flex;
  gap: 5px;
}

.tab-action-btn {
  width: 24px;
  height: 24px;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  font-size: 12px;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.tab-edit-btn {
  background: #2196F3;
  color: white;
}

.tab-delete-btn {
  background: #f44336;
  color: white;
}

.tab-action-btn:hover {
  transform: scale(1.1);
}

.tab-action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn {
  padding: 15px 30px;
  font-size: 18px;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.btn-primary {
  background: linear-gradient(45deg, #FE6B8B 30%, #FF8E53 90%);
  color: white;
  box-shadow: 0 3px 5px 2px rgba(255, 105, 135, .3);
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 10px 4px rgba(255, 105, 135, .3);
}

.btn-secondary {
  background: linear-gradient(45deg, #2196F3 30%, #21CBF3 90%);
  color: white;
  box-shadow: 0 3px 5px 2px rgba(33, 203, 243, .3);
}

.btn-secondary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 10px 4px rgba(33, 203, 243, .3);
}

.btn-danger {
  background: linear-gradient(45deg, #f44336 30%, #ff9800 90%);
  color: white;
  box-shadow: 0 3px 5px 2px rgba(244, 67, 54, .3);
}

.btn-danger:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 10px 4px rgba(244, 67, 54, .3);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loading {
  text-align: center;
  font-size: 1.5rem;
  margin: 50px 0;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top: 4px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error {
  background: rgba(244, 67, 54, 0.9);
  color: white;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 20px;
  text-align: center;
  font-size: 1.2rem;
}

.wishlist-container {
  width: 100%;
  margin: 0 auto;
  padding: 0 20px;
}

.wishlist-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.wishlist-item {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
  padding: 20px;
  color: #333;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
  cursor: grab;
  position: relative;
}

.wishlist-item:active {
  cursor: grabbing;
}

.wishlist-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
}

.drag-handle {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(0, 0, 0, 0.1);
  color: rgba(0, 0, 0, 0.5);
  padding: 5px 8px;
  border-radius: 8px;
  font-size: 1.2rem;
  cursor: grab;
  transition: all 0.3s ease;
}

.drag-handle:hover {
  background: rgba(0, 0, 0, 0.2);
  color: rgba(0, 0, 0, 0.7);
}

.item-image {
  width: 100%;
  height: 200px;
  border-radius: 10px;
  margin-bottom: 15px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.item-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.item-image:hover img {
  transform: scale(1.05);
}

.placeholder-image {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  color: #999;
}

.item-content h3 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 1.4rem;
  font-weight: bold;
}

.item-link {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
  word-break: break-all;
  margin-bottom: 15px;
  display: block;
}

.item-link:hover {
  text-decoration: underline;
}

.item-actions {
  margin-top: 15px;
  display: flex;
  gap: 10px;
  justify-content: center;
}

.btn-small {
  padding: 8px 16px;
  font-size: 14px;
  border-radius: 25px;
}

.form-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 20px;
}

.add-form, .edit-form, .tab-form {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 30px;
  margin: 20px auto;
  max-width: 500px;
  color: #333;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(10px);
  max-height: 90vh;
  overflow-y: auto;
  width: 100%;
}

.add-form h2, .edit-form h2, .tab-form h2 {
  color: #333;
  margin-bottom: 20px;
  text-align: center;
  font-size: 1.8rem;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: #555;
}

.form-group input[type="text"],
.form-group input[type="url"] {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #ddd;
  border-radius: 25px;
  font-size: 16px;
  transition: border-color 0.3s ease;
  box-sizing: border-box;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.file-input-container {
  position: relative;
  display: inline-block;
  width: 100%;
}

.file-input {
  width: 100%;
  padding: 12px 16px;
  border: 2px dashed #ddd;
  border-radius: 15px;
  background: #f9f9f9;
  cursor: pointer;
  text-align: center;
  transition: all 0.3s ease;
  display: block;
}

.file-input:hover {
  border-color: #667eea;
  background: #f0f2ff;
}

.file-input input[type="file"] {
  position: absolute;
  left: -9999px;
}

.form-actions {
  display: flex;
  gap: 15px;
  justify-content: center;
  margin-top: 25px;
}

.empty-state {
  text-align: center;
  padding: 50px 20px;
  color: rgba(255, 255, 255, 0.8);
}

.empty-state h3 {
  font-size: 1.5rem;
  margin-bottom: 10px;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

/* Drag and Drop States */
.ghost {
  opacity: 0.5;
  background: #e3f2fd;
  transform: rotate(5deg);
}

.chosen {
  cursor: grabbing;
}

.drag {
  transform: rotate(5deg);
  opacity: 0.8;
  z-index: 999;
}

/* iPad specific styles */
@media (max-width: 768px) {
  .app {
    padding: 15px;
  }
  
  .btn {
    padding: 12px 25px;
    font-size: 16px;
    width: 100%;
    max-width: 250px;
  }
  
  .tabs-nav {
    gap: 8px;
    padding: 5px 0;
    flex-direction: column;
  }
  
  .tab-button {
    padding: 10px 16px;
    font-size: 14px;
    min-width: 100px;
    justify-content: space-between;
    width: 100%;
  }
  
  .tab-actions {
    display: flex !important;
  }
  
  .wishlist-grid {
    grid-template-columns: 1fr;
    gap: 15px;
  }
  
  .wishlist-item {
    padding: 15px;
  }
  
  .add-form, .edit-form, .tab-form {
    margin: 15px;
    padding: 20px;
  }
}

/* Touch-friendly interactions */
@media (hover: none) and (pointer: coarse) {
  .btn:hover {
    transform: none;
  }
  
  .tab-button:hover:not(.active) {
    background: rgba(255, 255, 255, 0.2);
    transform: none;
  }
  
  .wishlist-item:hover {
    transform: none;
  }
  
  .item-image:hover img {
    transform: none;
  }
  
  .btn:active {
    transform: scale(0.95);
  }
  
  .tab-button:active {
    transform: scale(0.95);
  }
  
  .wishlist-item:active {
    transform: scale(0.98);
  }
  
  .tab-actions {
    display: flex !important;
  }
  
  .tab-action-btn {
    width: 32px;
    height: 32px;
    font-size: 14px;
  }
}
</style>
