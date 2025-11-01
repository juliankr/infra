<template>
  <div 
    class="day-column"
    :class="{ 
      'today': day.isToday,
      'past': day.isPast,
      'future': day.isFuture
    }"
  >
    <DayHeader :day="day" />
    
    <div class="day-events">
      <EventCard
        v-for="event in events"
        :key="event.id"
        :event="event"
        :edit-mode="editMode"
        @edit="$emit('edit-event', event)"
        @delete="$emit('delete-event', event)"
      />
    </div>
  </div>
</template>

<script>
import DayHeader from './DayHeader.vue'
import EventCard from './EventCard.vue'

export default {
  name: 'DayColumn',
  components: {
    DayHeader,
    EventCard
  },
  props: {
    day: {
      type: Object,
      required: true
    },
    events: {
      type: Array,
      default: () => []
    },
    editMode: {
      type: Boolean,
      default: false
    }
  },
  emits: ['edit-event', 'delete-event']
}
</script>

<style scoped>
.day-column {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 15px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.day-column:hover {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.15);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.day-column.today {
  background: rgba(255, 255, 255, 0.25);
  border: 2px solid rgba(255, 255, 255, 0.5);
}

.day-column.today::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #ff6b6b, #ffa500);
}

.day-column.past {
  opacity: 0.7;
}

.day-column.future {
  opacity: 0.9;
}

.day-events {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
  overflow-y: auto;
  padding-top: 10px;
}

@media (max-width: 768px) {
  .day-column {
    padding: 10px;
    border-radius: 15px;
  }
}
</style>
