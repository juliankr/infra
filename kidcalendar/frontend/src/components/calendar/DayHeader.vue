<template>
  <div class="day-header">
    <div class="day-name">{{ day.dayName }}</div>
    <div class="day-date">{{ day.date }}</div>
    <div class="day-number">{{ day.dayNumber }}</div>
  </div>
</template>

<script>
export default {
  name: 'DayHeader',
  props: {
    day: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>
.day-header {
  text-align: center;
  color: white;
  margin-bottom: 15px;
}

.day-name {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  opacity: 0.8;
}

.day-date {
  font-size: 10px;
  opacity: 0.6;
  margin: 2px 0;
}

.day-number {
  font-size: 24px;
  font-weight: bold;
  margin-top: 5px;
}

@media (max-width: 768px) {
  .day-number {
    font-size: 20px;
  }
  
  .day-name {
    font-size: 11px;
  }
  
  .day-date {
    font-size: 9px;
  }
}
</style>
