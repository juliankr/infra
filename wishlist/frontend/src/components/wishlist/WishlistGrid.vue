<template>
  <draggable 
    v-model="localWishlist"
    :disabled="false"
    item-key="id"
    class="main-grid"
    :animation="200"
    ghost-class="ghost"
    @end="handleDragEnd"
    tag="div"
  >
    <template #item="{ element: item }">
      <div class="item-card">
        <WishlistItem
          :item="item"
          @edit="$emit('edit-item', item)"
          @delete="$emit('delete-item', item)"
        />
      </div>
    </template>
  </draggable>
</template>

<script>
import { computed } from 'vue'
import draggable from 'vuedraggable'
import WishlistItem from './WishlistItem.vue'

export default {
  name: 'WishlistGrid',
  components: {
    draggable,
    WishlistItem
  },
  props: {
    wishlist: {
      type: Array,
      default: () => []
    }
  },
  emits: ['update:wishlist', 'edit-item', 'delete-item', 'reorder'],
  setup(props, { emit }) {
    const localWishlist = computed({
      get: () => props.wishlist,
      set: (value) => {
        emit('update:wishlist', value)
      }
    })
    
    const handleDragEnd = () => {
      emit('reorder', localWishlist.value)
    }
    
    return {
      localWishlist,
      handleDragEnd
    }
  }
}
</script>

<style scoped>
.main-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  width: 100%;
  padding: 20px;
  box-sizing: border-box;
}

.item-card {
  width: 350px;
  height: 400px;
  box-sizing: border-box;
  flex-shrink: 0;
}

.ghost {
  opacity: 0.5;
  background: rgba(0, 123, 255, 0.1);
  border: 2px dashed #007bff;
}

/* Landscape tablet optimization */
@media (min-width: 768px) and (max-width: 1024px) and (orientation: landscape) {
  .main-grid {
    gap: 15px;
    padding: 15px;
  }
  
  .item-card {
    width: calc(33.333% - 10px);
    min-width: 300px;
    height: 350px;
  }
}

/* Large landscape screens */
@media (min-width: 1025px) and (orientation: landscape) {
  .main-grid {
    gap: 25px;
    padding: 25px;
  }
  
  .item-card {
    width: calc(25% - 19px);
    min-width: 320px;
    height: 420px;
  }
}

/* Portrait tablet */
@media (max-width: 768px) and (orientation: portrait) {
  .main-grid {
    gap: 15px;
    padding: 15px;
  }
  
  .item-card {
    width: calc(50% - 8px);
    min-width: 300px;
    height: 380px;
  }
}

/* Mobile portrait */
@media (max-width: 480px) {
  .main-grid {
    gap: 15px;
    padding: 15px;
  }
  
  .item-card {
    width: 100%;
    height: 350px;
  }
}
</style>