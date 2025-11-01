<template>
  <BaseModal 
    :show="show" 
    @close="$emit('close')"
    :title="isNew ? 'Neues Event' : 'Event bearbeiten'"
  >
    <EventForm
      :event="event"
      :default-date="defaultDate"
      @submit="$emit('save', $event)"
      @cancel="$emit('close')"
    />
  </BaseModal>
</template>

<script>
import { computed } from 'vue'
import BaseModal from '../ui/BaseModal.vue'
import EventForm from '../forms/EventForm.vue'

export default {
  name: 'EventEditModal',
  components: {
    BaseModal,
    EventForm
  },
  props: {
    show: {
      type: Boolean,
      default: false
    },
    event: {
      type: Object,
      default: null
    },
    defaultDate: {
      type: String,
      default: ''
    }
  },
  emits: ['close', 'save'],
  setup(props) {
    const isNew = computed(() => !props.event?.id)

    return {
      isNew
    }
  }
}
</script>
