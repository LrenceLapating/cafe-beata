<template>
  <div class="stock-indicator" :class="{ 'out-of-stock': isOutOfStock }">
    <span v-if="isOutOfStock" class="stock-status">
      Out of Stock
    </span>
    <span v-else-if="isLowStock" class="stock-status low-stock">
      Low Stock
    </span>
  </div>
</template>

<script>
export default {
  name: 'StockIndicator',
  props: {
    itemId: {
      type: Number,
      required: true
    },
    quantity: {
      type: Number,
      required: true
    },
    minStockLevel: {
      type: Number,
      default: 10
    }
  },
  computed: {
    isOutOfStock() {
      return this.quantity === 0;
    },
    isLowStock() {
      return !this.isOutOfStock && this.quantity <= this.minStockLevel;
    }
  }
};
</script>

<style scoped>
.stock-indicator {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 2;
}

.stock-status {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: bold;
  background-color: rgba(255, 255, 255, 0.9);
}

.out-of-stock .stock-status {
  color: #f44336;
  border: 1px solid #f44336;
}

.low-stock {
  color: #ff9800;
  border: 1px solid #ff9800;
}
</style> 