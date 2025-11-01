<template>
  <div class="week-calendar">
    <div class="calendar-grid">
      <div 
        v-for="(day, index) in weekDays" 
        :key="index"
        class="day-column"
        :class="{ 
          'today': day.isToday,
          'past': day.isPast,
          'future': day.isFuture
        }"
      >
        <div class="day-header">
          <div class="day-name">{{ day.dayName }}</div>
          <div class="day-date">{{ day.date }}</div>
          <div class="day-number">{{ day.dayNumber }}</div>
        </div>
        
        <div class="day-events">
          <div 
            v-for="event in getDayEvents(day.fullDate)"
            :key="event.id"
            class="event"
            :class="{ 'edit-mode': editMode }"
            :style="{ backgroundColor: event.color || '#FF6B6B' }"
          >
            <div class="event-content">
              <img 
                v-if="event.image" 
                :src="event.image" 
                :alt="event.title"
                class="event-image"
              />
              <div class="event-title">{{ event.title }}</div>
            </div>
            
            <!-- Edit mode buttons -->
            <div v-if="editMode" class="event-edit-buttons">
              <button 
                class="edit-btn"
                @click="handleEditEvent(event)"
                title="Event bearbeiten"
              >
                ✏️
              </button>
              <button 
                class="delete-btn"
                @click="handleDeleteEvent(event)"
                title="Event löschen"
              >
                🗑️
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { generateWeekDays } from '../utils/date';
import { useSettings } from '../composables/useSettings';

export default {
  name: 'WeekCalendar',
  props: {
    events: {
      type: Array,
      default: () => []
    },
    editMode: {
      type: Boolean,
      default: false
    }
  },
  setup() {
    const { settings, loadSettings } = useSettings();
    
    // Load settings when component is set up
    loadSettings();
    
    return {
      settings
    };
  },
  data() {
    return {}
  },
  computed: {
    weekDays() {
      // Use settings-based week generation - let function use settings defaults
      return generateWeekDays(undefined, undefined, this.settings);
    }
  },
  methods: {
    isSameDay(date1, date2) {
      return date1.toDateString() === date2.toDateString()
    },
    getDayEvents(date) {
      return this.events
        .filter(event => event.date === date)
        .sort((a, b) => (a.position || 0) - (b.position || 0))
    },
    handleEditEvent(event) {
      this.$emit('edit-event', event);
    },
    handleDeleteEvent(event) {
      this.$emit('delete-event', event);
    }
  }
}
</script>

<style scoped>
.week-calendar {
  width: 100vw;
  height: 100vh;
  padding: 1rem;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 0.5rem;
  flex: 1;
  width: 100%;
}

.day-column {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 16px;
  padding: 1rem;
  height: 100%;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  position: relative;
}

.day-column:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
}

.day-column.today {
  background: rgba(255, 255, 255, 1);
  border: 4px solid #FF6B6B;
  box-shadow: 0 8px 30px rgba(255, 107, 107, 0.4);
  transform: scale(1.02);
}

.day-column.today .day-header {
  background: linear-gradient(135deg, #FF6B6B, #FF8E53);
  color: white;
  border-radius: 8px;
  padding: 0.5rem;
  margin: -0.5rem -0.5rem 1rem -0.5rem;
}

.day-column.today .day-number {
  color: white;
  font-weight: bold;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.day-column.today .day-name,
.day-column.today .day-date {
  color: rgba(255, 255, 255, 0.9);
}

.day-column.past {
  opacity: 0.7;
  background: rgba(255, 255, 255, 0.6);
}

.day-header {
  text-align: center;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid rgba(0, 0, 0, 0.1);
}

.day-name {
  font-size: 0.9rem;
  color: #666;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.day-date {
  font-size: 0.8rem;
  color: #888;
  margin: 0.2rem 0;
}

.day-number {
  font-size: 2rem;
  font-weight: bold;
  color: #333;
}

.today .day-number {
  color: #FF6B6B;
}

.day-events {
  flex: 1;
  margin-bottom: 1rem;
}

.event {
  background: #FF6B6B;
  color: white;
  padding: 0.5rem;
  margin-bottom: 0.5rem;
  border-radius: 8px;
  font-size: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  min-height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  transition: all 0.2s ease;
}

.event.edit-mode {
  border: 2px dashed rgba(255, 255, 255, 0.5);
  transform: scale(0.98);
}

.event-edit-buttons {
  position: absolute;
  top: 4px;
  right: 4px;
  display: flex;
  gap: 4px;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.event:hover .event-edit-buttons {
  opacity: 1;
}

.edit-btn, .delete-btn {
  width: 24px;
  height: 24px;
  border: none;
  border-radius: 50%;
  font-size: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.edit-btn {
  background: rgba(255, 255, 255, 0.9);
}

.edit-btn:hover {
  background: white;
  transform: scale(1.1);
}

.delete-btn {
  background: rgba(255, 69, 58, 0.9);
}

.delete-btn:hover {
  background: rgb(255, 69, 58);
  transform: scale(1.1);
}

.event-title {
  font-weight: 500;
  text-align: center;
}

.event-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  width: 100%;
}

.event-image {
  width: 80px;
  max-height: 60px;
  object-fit: contain;
  border-radius: 8px;
}

@media (max-width: 768px) {
  .week-calendar {
    padding: 0.5rem;
  }
  
  .calendar-grid {
    gap: 0.25rem;
  }
  
  .day-column {
    padding: 0.5rem;
  }
  
  .day-number {
    font-size: 1.5rem;
  }
  
  .event-image {
    width: 53px;
    max-height: 40px;
  }
  
  .event {
    padding: 0.5rem;
    min-height: 60px;
  }
  
  /* Always show edit buttons on mobile for better usability */
  .event-edit-buttons {
    opacity: 1;
  }
  
  .edit-btn, .delete-btn {
    width: 20px;
    height: 20px;
    font-size: 8px;
  }
}

@media (max-width: 1024px) and (orientation: landscape) {
  .week-calendar {
    padding: 0.75rem;
  }
  
  .calendar-grid {
    gap: 0.5rem;
  }
}

@media (min-width: 1025px) {
  .week-calendar {
    padding: 1.5rem;
  }
  
  .calendar-grid {
    gap: 1rem;
  }
  
  .event-image {
    width: 107px;
    max-height: 80px;
  }
  
  .event {
    padding: 0.75rem;
    min-height: 100px;
  }
}
</style>
