<template>
  <div 
    v-if="show"
    class="error-message"
    :class="{ 'is-dismissible': dismissible }"
  >
    <div class="error-content">
      <span class="error-icon">⚠️</span>
      <div class="error-text">
        <strong v-if="title">{{ title }}</strong>
        <p>{{ message }}</p>
      </div>
    </div>
    <button 
      v-if="dismissible"
      class="dismiss-button"
      @click="$emit('dismiss')"
      aria-label="Fehler schließen"
    >
      ×
    </button>
  </div>
</template>

<script>
export default {
  name: 'ErrorMessage',
  props: {
    show: {
      type: Boolean,
      default: true
    },
    title: {
      type: String,
      default: ''
    },
    message: {
      type: String,
      required: true
    },
    dismissible: {
      type: Boolean,
      default: true
    }
  },
  emits: ['dismiss']
}
</script>

<style scoped>
.error-message {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  background-color: var(--color-danger-light);
  border: 1px solid var(--color-danger);
  border-radius: 0.375rem;
  padding: 1rem;
  margin-bottom: 1rem;
  color: var(--color-danger-dark);
}

.error-content {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  flex: 1;
}

.error-icon {
  font-size: 1.25rem;
  flex-shrink: 0;
  margin-top: 0.125rem;
}

.error-text {
  flex: 1;
}

.error-text strong {
  display: block;
  margin-bottom: 0.25rem;
  font-weight: 600;
}

.error-text p {
  margin: 0;
  line-height: 1.4;
}

.dismiss-button {
  background: none;
  border: none;
  color: var(--color-danger);
  cursor: pointer;
  font-size: 1.25rem;
  line-height: 1;
  padding: 0;
  margin-left: 0.5rem;
  flex-shrink: 0;
  width: 1.5rem;
  height: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.25rem;
  transition: background-color 0.2s;
}

.dismiss-button:hover {
  background-color: rgba(var(--color-danger-rgb), 0.1);
}
</style>
