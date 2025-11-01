<template>
  <div class="wishlist-item" @click="$emit('edit', item)">
    <div class="item-image">
      <img 
        v-if="imageUrl" 
        :src="imageUrl" 
        :alt="item.title"
        @error="handleImageError"
      />
      <div v-else class="placeholder-image">
        📦
      </div>
    </div>
    
    <div class="item-content">
      <h3 class="item-name">{{ item.title }}</h3>
      <div class="item-meta">
        <a 
          v-if="item.weblink" 
          :href="item.weblink" 
          target="_blank" 
          rel="noopener noreferrer"
          class="buy-button"
          @click.stop
        >
          Buy Now
        </a>
      </div>
    </div>
    
    <div class="item-actions">
      <button 
        @click.stop="$emit('edit', item)"
        class="action-btn edit-btn"
        title="Edit item"
      >
        ✏️
      </button>
      <button 
        @click.stop="$emit('delete', item)"
        class="action-btn delete-btn"
        title="Delete item"
      >
        🗑️
      </button>
    </div>
  </div>
</template>

<script>
import { computed, ref } from 'vue'

export default {
  name: 'WishlistItem',
  props: {
    item: {
      type: Object,
      required: true
    }
  },
  emits: ['edit', 'delete'],
  setup(props) {
    const imageError = ref(false)
    
    const imageUrl = computed(() => {
      if (imageError.value) return null
      if (!props.item.image) return null
      
      // Handle URL images
      if (typeof props.item.image === 'string' && props.item.image.startsWith('http')) {
        return props.item.image
      }
      
      // Handle uploaded files
      if (props.item.image) {
        return `/api/images/${props.item.image}`
      }
      
      return null
    })
    
    const handleImageError = () => {
      imageError.value = true
    }
    
    return {
      imageUrl,
      handleImageError
    }
  }
}
</script>

<style scoped>
.wishlist-item {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 20px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  box-sizing: border-box;
}

.wishlist-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
  background: rgba(255, 255, 255, 0.95);
}

.item-image {
  width: 100%;
  height: 60%; /* Use percentage for consistent proportions */
  margin-bottom: 15px;
  border-radius: 15px;
  overflow: hidden;
  background: #f8f9fa;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0; /* Prevent shrinking */
  max-height: 240px; /* Fixed maximum height */
}

.item-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.wishlist-item:hover .item-image img {
  transform: scale(1.05);
}

.placeholder-image {
  font-size: 3em;
  color: #dee2e6;
}

.item-content {
  flex: 1;
  margin-bottom: 15px;
  display: flex;
  flex-direction: column;
  min-height: 0; /* Allow shrinking */
}

.item-name {
  font-size: 1.1em;
  font-weight: 600;
  margin: 0 0 8px 0;
  color: #333;
  line-height: 1.3;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.item-description {
  color: #666;
  font-size: 0.9em;
  line-height: 1.4;
  margin: 0 0 12px 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.item-meta {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-top: 15px;
}

.item-price {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 4px 12px;
  border-radius: 15px;
  font-size: 0.9em;
  font-weight: 500;
}

.buy-button {
  display: inline-block;
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
  color: white;
  text-decoration: none;
  padding: 12px 20px;
  border-radius: 25px;
  font-size: 1.1em;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
  text-align: center;
  min-width: 120px;
}

.buy-button:hover {
  background: linear-gradient(135deg, #218838 0%, #1aa085 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(40, 167, 69, 0.4);
  color: white;
}

.item-link {
  color: #007bff;
  text-decoration: none;
  font-size: 1.2em;
  transition: transform 0.3s ease;
}

.item-link:hover {
  transform: scale(1.2);
}

.item-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
  margin-top: auto;
  padding-top: 15px;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
}

.action-btn {
  background: rgba(0, 0, 0, 0.1);
  border: none;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
}

.action-btn:hover {
  background: rgba(0, 0, 0, 0.2);
  transform: scale(1.1);
}

.delete-btn:hover {
  background: rgba(231, 76, 60, 0.2);
}

.edit-btn:hover {
  background: rgba(0, 123, 255, 0.2);
}

@media (min-width: 768px) and (orientation: landscape) {
  .wishlist-item {
    padding: 18px;
  }
  
  .item-image {
    height: 65%;
  }
  
  .item-name {
    font-size: 1.0em;
    -webkit-line-clamp: 1; /* Single line in landscape for more cards */
  }
  
  .action-btn {
    width: 32px;
    height: 32px;
    font-size: 12px;
  }
}

@media (max-width: 768px) {
  .wishlist-item {
    padding: 15px;
  }
  
  .item-image {
    height: 55%;
  }
  
  .item-name {
    font-size: 1.1em;
  }
  
  .action-btn {
    width: 32px;
    height: 32px;
    font-size: 12px;
  }
}
</style>