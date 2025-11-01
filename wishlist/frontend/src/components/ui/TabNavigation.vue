<template>
  <div class="tabs-container" v-if="tabs.length > 0">
    <div class="tabs-nav">
      <div class="tabs-left">
        <div 
          v-for="tab in tabs" 
          :key="tab.id"
          class="tab-button"
          :class="{ active: currentTab?.id === tab.id }"
          @click="$emit('switch-tab', tab)"
        >
          <span class="tab-name">{{ tab.name }}</span>
          <div v-if="editMode" class="tab-actions">
            <button 
              @click.stop="$emit('edit-tab', tab)"
              class="tab-action-btn edit-btn"
              title="Rename tab"
            >
              ✏️
            </button>
            <button 
              @click.stop="$emit('delete-tab', tab)"
              class="tab-action-btn delete-btn"
              title="Delete tab"
              v-if="tabs.length > 1"
            >
              🗑️
            </button>
          </div>
        </div>
      </div>
      
      <div class="tabs-right">
        <button 
          v-if="editMode"
          class="btn btn-secondary" 
          @click="$emit('add-tab')"
          :disabled="showAddForm || editingItem || showAddTabForm"
        >
          + Tab
        </button>
        <button 
          class="btn btn-primary" 
          @click="$emit('add-item')"
          :disabled="showAddForm || editingItem || showAddTabForm || !currentTab"
        >
          + Item
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TabNavigation',
  props: {
    tabs: {
      type: Array,
      default: () => []
    },
    currentTab: {
      type: Object,
      default: null
    },
    editMode: {
      type: Boolean,
      default: false
    },
    showAddForm: {
      type: Boolean,
      default: false
    },
    editingItem: {
      type: [Object, Boolean],
      default: false
    },
    showAddTabForm: {
      type: Boolean,
      default: false
    }
  },
  emits: ['switch-tab', 'edit-tab', 'delete-tab', 'add-tab', 'add-item']
}
</script>

<style scoped>
.tabs-container {
  margin-bottom: 25px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 15px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.tabs-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 15px;
  flex-wrap: wrap;
}

.tabs-left {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  justify-content: flex-start;
  flex: 1;
}

.tabs-right {
  display: flex;
  gap: 10px;
  align-items: center;
}

.tab-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 18px;
  background: rgba(255, 255, 255, 0.2);
  color: rgba(255, 255, 255, 0.85);
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 25px;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 120px;
  position: relative;
  backdrop-filter: blur(10px);
}

.tab-button:hover {
  background: rgba(255, 255, 255, 0.3);
  color: rgba(255, 255, 255, 0.95);
  border-color: rgba(255, 255, 255, 0.4);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.tab-button.active {
  background: rgba(255, 255, 255, 0.95);
  color: #333;
  border-color: rgba(255, 255, 255, 0.8);
  box-shadow: 0 8px 25px rgba(255, 255, 255, 0.3);
}

.tab-name {
  flex: 1;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 150px;
}

.tab-actions {
  display: flex;
  gap: 4px;
  margin-left: 8px;
}

.tab-action-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  border-radius: 50%;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  font-size: 12px;
}

.tab-button:not(.active) .tab-action-btn {
  background: rgba(0, 0, 0, 0.15);
  color: #555;
}

.tab-button.active .tab-action-btn {
  background: rgba(255, 255, 255, 0.2);
}

.tab-action-btn:hover {
  background: rgba(0, 0, 0, 0.2) !important;
  transform: scale(1.1);
}

.tab-button.active .tab-action-btn:hover {
  background: rgba(255, 255, 255, 0.3) !important;
}

/* Button styles */
.btn {
  padding: 12px 20px;
  font-size: 14px;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  white-space: nowrap;
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

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

@media (max-width: 768px) {
  .tabs-nav {
    flex-direction: column;
    gap: 15px;
  }
  
  .tabs-left {
    order: 1;
    justify-content: center;
  }
  
  .tabs-right {
    order: 2;
    justify-content: center;
    width: 100%;
  }
  
  .tab-button {
    width: 100%;
    min-width: auto;
  }
  
  .tab-name {
    max-width: none;
  }
  
  .btn {
    padding: 10px 16px;
    font-size: 12px;
  }
}
</style>