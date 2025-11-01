<template>
  <div 
    class="event-card"
    :class="{ 'edit-mode': editMode }"
    :style="{ backgroundColor: event.color || '#FF6B6B' }"
  >
    <div class="event-content">
      <div class="event-title">{{ event.title }}</div>
      <img 
        v-if="event.image" 
        :src="event.image" 
        :alt="event.title"
        class="event-image"
      />
    </div>
    
    <!-- Edit mode buttons -->
    <div v-if="editMode" class="event-actions">
      <button 
        class="action-btn edit-btn"
        @click="$emit('edit')"
        title="Event bearbeiten"
      >
        ✏️
      </button>
      <button 
        class="action-btn delete-btn"
        @click="$emit('delete')"
        title="Event löschen"
      >
        🗑️
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EventCard',
  props: {
    event: {
      type: Object,
      required: true
    },
    editMode: {
      type: Boolean,
      default: false
    }
  },
  emits: ['edit', 'delete']
}
</script>

<style scoped>
.event-card {
  position: relative;
  padding: 12px;
  border-radius: 12px;
  color: white;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  min-height: 80px;
  display: flex;
  flex-direction: column;
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.event-card:hover {
  transform: scale(1.02);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.event-card.edit-mode {
  padding-right: 80px; /* Make room for buttons */
}

.event-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
}

.event-image {
  width: 100%;
  aspect-ratio: 4/3;
  border-radius: 8px;
  object-fit: cover;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.event-title {
  font-weight: 600;
  line-height: 1.2;
  flex: 1;
}

.event-actions {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  gap: 4px;
}

.action-btn {
  width: 28px;
  height: 28px;
  border: none;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.1);
}

.edit-btn:hover {
  background: rgba(52, 152, 219, 0.8);
}

.delete-btn:hover {
  background: rgba(231, 76, 60, 0.8);
}

@media (max-width: 768px) {
  .event-card {
    padding: 10px;
    font-size: 13px;
    min-height: 70px;
  }
  
  .event-card.edit-mode {
    padding-right: 70px;
  }
  
  .event-image {
    border-radius: 6px;
  }
  
  .action-btn {
    width: 24px;
    height: 24px;
    font-size: 11px;
  }
}
</style>
