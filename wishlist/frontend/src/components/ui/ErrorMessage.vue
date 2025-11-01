<template>
  <div class="error">
    <div class="error-icon">⚠️</div>
    <div class="error-message">
      <slot>{{ message }}</slot>
    </div>
    <button v-if="showRetry" @click="$emit('retry')" class="btn btn-secondary retry-btn">
      Try Again
    </button>
  </div>
</template>

<script>
export default {
  name: 'ErrorMessage',
  props: {
    message: {
      type: String,
      default: 'Something went wrong'
    },
    showRetry: {
      type: Boolean,
      default: false
    }
  },
  emits: ['retry']
}
</script>

<style scoped>
.error {
  text-align: center;
  padding: 50px 20px;
  color: #e74c3c;
  background: rgba(231, 76, 60, 0.1);
  border-radius: 15px;
  margin: 20px 0;
}

.error-icon {
  font-size: 3em;
  margin-bottom: 15px;
}

.error-message {
  font-size: 1.1em;
  margin-bottom: 20px;
  line-height: 1.5;
}

.retry-btn {
  padding: 12px 25px;
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #f8f9fa;
  color: #6c757d;
  border: 1px solid #dee2e6;
}

.retry-btn:hover {
  background: #e9ecef;
  color: #495057;
  transform: translateY(-2px);
}
</style>