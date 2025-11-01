<template>
  <div 
    ref="calendarElement"
    class="week-calendar" 
    :class="{ 'navigating': isNavigating }"
  >
    <!-- Left arrow for previous day -->
    <button @click="goToPreviousDay" class="nav-arrow nav-arrow-left" :disabled="isNavigating">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M15 18L9 12L15 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>

    <!-- Right arrow for next day -->
    <button @click="goToNextDay" class="nav-arrow nav-arrow-right" :disabled="isNavigating">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M9 18L15 12L9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>

    <!-- Navigation indicator -->
    <div v-if="currentOffset !== 0" class="navigation-indicator">
      <button @click="goToToday" class="today-btn">
        📅 Zurück zu heute
      </button>
      <span class="offset-display">
        {{ currentOffset > 0 ? `+${currentOffset}` : currentOffset }} Tag{{ Math.abs(currentOffset) !== 1 ? 'e' : '' }}
      </span>
    </div>

    <div 
      class="calendar-grid"
      :style="{ '--week-days': weekDays.length, 'grid-template-columns': `repeat(${weekDays.length}, 1fr)` }"
    >
      <DayColumn 
        v-for="(day, index) in weekDays" 
        :key="`${day.fullDate}-${currentOffset}`"
        :day="day"
        :events="getEventsForDay(day.fullDate)"
        :edit-mode="editMode"
        @edit-event="$emit('edit-event', $event)"
        @delete-event="$emit('delete-event', $event)"
      />
    </div>

    <!-- Swipe instructions -->
    <div v-if="showSwipeHint" class="swipe-hint">
      <span class="desktop-hint">← → Pfeile oder Wischen für andere Tage</span>
      <span class="mobile-hint">← Wischen für andere Tage →</span>
    </div>
  </div>
</template>

<script>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import DayColumn from './DayColumn.vue'
import { formatDateDisplay, generateWeekDays } from '../../utils/date'
import { UI_CONFIG } from '../../config'
import { useSettings } from '../../composables/useSettings'
import { useDayNavigation } from '../../composables/useDayNavigation'

export default {
  name: 'WeekCalendar',
  components: {
    DayColumn
  },
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
  emits: ['edit-event', 'delete-event', 'date-changed'],
  setup(props, { emit }) {
    const { settings, loadSettings } = useSettings()
    const { 
      currentOffset, 
      currentDate, 
      isNavigating, 
      goToToday,
      goToPreviousDay,
      goToNextDay,
      setupGestureListeners, 
      removeGestureListeners 
    } = useDayNavigation()
    
    const calendarElement = ref(null)
    const showSwipeHint = ref(false)
    
    // Load settings when component is mounted
    onMounted(() => {
      loadSettings()
      
      // Setup gesture listeners
      if (calendarElement.value) {
        setupGestureListeners(calendarElement.value)
      }
      
      // Show swipe hint briefly on first load
      setTimeout(() => {
        showSwipeHint.value = true
        setTimeout(() => {
          showSwipeHint.value = false
        }, 3000)
      }, 1000)
    })
    
    onUnmounted(() => {
      if (calendarElement.value) {
        removeGestureListeners(calendarElement.value)
      }
    })
    
    // Watch for date changes and emit to parent with offset
    watch(currentDate, (newDate) => {
      emit('date-changed', newDate, currentOffset.value)
    })
    
    const weekDays = computed(() => 
      generateWeekDays(
        undefined, // Let generateWeekDays use settings defaults
        undefined, // Let generateWeekDays use settings defaults
        settings.value,
        currentDate.value // Use the navigation date as reference
      )
    )

    function getEventsForDay(date) {
      return props.events.filter(event => event.date === date)
    }

    return {
      calendarElement,
      weekDays,
      getEventsForDay,
      currentOffset,
      isNavigating,
      goToToday,
      goToPreviousDay,
      goToNextDay,
      showSwipeHint
    }
  },
  
  // Expose methods to parent component
  expose: ['goToToday']
}
</script>

<style scoped>
.week-calendar {
  width: 100%;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
  box-sizing: border-box;
  transition: transform 0.3s ease;
  position: relative;
}

.week-calendar.navigating {
  transform: scale(0.98);
}

.nav-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 48px;
  height: 48px;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  z-index: 10;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.nav-arrow:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.25);
  transform: translateY(-50%) scale(1.1);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
}

.nav-arrow:active:not(:disabled) {
  transform: translateY(-50%) scale(0.95);
}

.nav-arrow:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.nav-arrow-left {
  left: 10px;
}

.nav-arrow-right {
  right: 10px;
}

.nav-arrow svg {
  width: 24px;
  height: 24px;
}

.navigation-indicator {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding: 10px 15px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  backdrop-filter: blur(10px);
}

.today-btn {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.today-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-1px);
}

.offset-display {
  color: white;
  font-weight: 600;
  font-size: 14px;
  opacity: 0.9;
}

.calendar-grid {
  display: grid;
  gap: 15px;
  height: calc(100% - 60px);
  max-width: 1200px;
  margin: 0 auto;
}

/* Dynamic grid columns based on number of days */
.calendar-grid:where(*) {
  grid-template-columns: repeat(var(--week-days, 7), 1fr);
}

@supports not (selector(:where(*))) {
  /* Fallback for older browsers */
  .calendar-grid {
    grid-template-columns: repeat(7, 1fr);
  }
}

.swipe-hint {
  position: absolute;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
  text-align: center;
  padding: 8px 16px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 20px;
  backdrop-filter: blur(5px);
  animation: fadeInOut 3s ease-in-out;
}

.mobile-hint {
  display: none;
}

.desktop-hint {
  display: inline;
}

@keyframes fadeInOut {
  0% { opacity: 0; transform: translateX(-50%) translateY(10px); }
  20% { opacity: 1; transform: translateX(-50%) translateY(0); }
  80% { opacity: 1; transform: translateX(-50%) translateY(0); }
  100% { opacity: 0; transform: translateX(-50%) translateY(-10px); }
}

@media (max-width: 768px) {
  .week-calendar {
    padding: 10px;
  }
  
  .calendar-grid {
    gap: 8px;
    height: calc(100% - 50px);
  }
  
  .navigation-indicator {
    margin-bottom: 10px;
    padding: 8px 12px;
  }
  
  .today-btn {
    padding: 6px 12px;
    font-size: 12px;
  }
  
  .offset-display {
    font-size: 12px;
  }

  /* Hide navigation arrows on mobile - use swipe instead */
  .nav-arrow {
    display: none;
  }

  /* Show mobile-specific hint text */
  .mobile-hint {
    display: inline;
  }

  .desktop-hint {
    display: none;
  }
}
</style>
