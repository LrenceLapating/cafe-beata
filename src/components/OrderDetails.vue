<template>
  <div class="order-container">
    <div class="order-card">
      <h1>Order Details</h1>
      
      <div class="order-info">
        <div class="order-header">
          <div class="order-header-item">
            <span class="label">Order ID:</span>
            <span class="value">{{ orderId }}</span>
          </div>
          <div class="order-header-item">
            <span class="label">Customer:</span>
            <span class="value">{{ customerName }}</span>
          </div>
        </div>
        
        <div class="order-items-list">
          <h2>Items</h2>
          <table class="items-table">
            <thead>
              <tr>
                <th>Image</th>
                <th>Item</th>
                <th>Quantity</th>
                <th>Price</th>
                <th>Subtotal</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in items" :key="index">
                <td class="item-image-cell">
                  <img :src="getImagePath(item)" :alt="item.name" class="item-image"/>
                </td>
                <td>{{ item.name }}</td>
                <td>{{ item.quantity }}</td>
                <td>₱{{ item.price.toFixed(2) }}</td>
                <td>₱{{ (item.price * item.quantity).toFixed(2) }}</td>
              </tr>
            </tbody>
            <tfoot>
              <tr>
                <td colspan="4" class="total-label">Total</td>
                <td class="total-value">₱{{ calculateTotal() }}</td>
              </tr>
            </tfoot>
          </table>
        </div>
      </div>

      <div class="button-container">
        <button @click="goBackToHistory" class="back-button">Back to Order History</button>
        <button @click="orderAgain" class="order-again-button">Order Again</button>
      </div>
      
      <!-- Success Message -->
      <div v-if="showSuccessMessage" class="success-message">
        <p>Items added to cart successfully!</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'OrderDetails',
  data() {
    return {
      items: this.parseItems(this.$route.query.items),
      orderId: this.$route.query.orderId,
      customerName: this.$route.query.customerName,
      showSuccessMessage: false
    };
  },
  methods: {
    parseItems(items) {
      try {
        return JSON.parse(items) || [];
      } catch (error) {
        console.error("Error parsing order items:", error);
        return [];
      }
    },
    
    goBackToHistory() {
      this.$router.push({ name: "OrderHistory" });
    },

    calculateTotal() {
      if (!Array.isArray(this.items)) return "0";
      return this.items.reduce((sum, item) => sum + item.price * item.quantity, 0).toFixed(2);
    },

    getImagePath(item) {
      try {
        // If no item or no image path, return default image
        if (!item || !item.image) {
          return require('@/assets/default.png');
        }

        // If it's already a full URL (including localhost:8000)
        if (item.image.startsWith('http://') || item.image.startsWith('https://')) {
          return item.image;
        }

        // If it's a backend upload path
        if (item.image.startsWith('/uploads/')) {
          return `http://localhost:8000${item.image}`;
        }

        // If it's just a filename, try to load from assets
        try {
          return require(`@/assets/${item.image}`);
        } catch (error) {
          console.error('Failed to load image from assets:', error);
          // If not found in assets, try backend uploads
          return `http://localhost:8000/uploads/avatars/${item.image}`;
        }
      } catch (error) {
        console.error('Error in getImagePath:', error);
        return require('@/assets/default.png');
      }
    },

    orderAgain() {
      const userName = localStorage.getItem('userName') || 'Guest';
      const userCartKey = `cart_${userName}`;
      
      // Get existing cart from localStorage or initialize empty array
      let cart = JSON.parse(localStorage.getItem(userCartKey) || '[]');
      
      // Add all items from this order to the cart
      this.items.forEach(item => {
        // Check if item already exists in cart
        const existingItemIndex = cart.findIndex(cartItem => 
          cartItem.name === item.name && 
          cartItem.price === item.price
        );
        
        if (existingItemIndex !== -1) {
          // If item exists, increase quantity
          cart[existingItemIndex].quantity += item.quantity;
        } else {
          // If item doesn't exist, add it to cart
          cart.push({...item});
        }
      });
      
      // Save updated cart to localStorage with user-specific key
      localStorage.setItem(userCartKey, JSON.stringify(cart));
      
      // Show success message
      this.showSuccessMessage = true;
      
      // Hide success message after 3 seconds
      setTimeout(() => {
        this.showSuccessMessage = false;
        // Navigate to the ConfirmOrder page
        this.$router.push({ name: 'ConfirmOrder' });
      }, 1500);
    }
  },
};
</script>

<style scoped>
.order-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #1e1e2f, #3a3a52);
  color: white;
  padding: 20px;
}

.order-card {
  background: rgba(255, 255, 255, 0.1);
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  text-align: center;
  width: 90%;
  max-width: 800px;
  backdrop-filter: blur(10px);
  position: relative;
}

h1 {
  font-size: 28px;
  margin-bottom: 20px;
  color: rgb(216, 144, 178);
}

h2 {
  font-size: 22px;
  margin-bottom: 15px;
  color: rgb(216, 144, 178);
  text-align: left;
}

.order-header {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  margin-bottom: 20px;
  padding: 15px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
}

.order-header-item {
  margin: 5px 10px;
  text-align: left;
}

.label {
  font-weight: bold;
  color: #aaa;
  margin-right: 5px;
}

.value {
  color: rgb(236, 155, 225);
  font-weight: bold;
}

.order-items-list {
  margin-top: 20px;
  text-align: left;
}

.items-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
  margin-bottom: 20px;
}

.items-table th,
.items-table td {
  padding: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  text-align: left;
  vertical-align: middle;
}

.items-table th {
  background: rgba(216, 144, 178, 0.2);
  color: rgb(236, 155, 225);
}

.item-image-cell {
  width: 80px;
  text-align: center;
}

.item-image {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 8px;
}

.total-label {
  text-align: right;
  font-weight: bold;
  color: #fff;
}

.total-value {
  font-weight: bold;
  color: #ff9800;
}

.button-container {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.back-button, .order-again-button {
  padding: 12px 25px;
  font-size: 14px;
  font-weight: bold;
  background: transparent;
  color: #fff;
  border: 2px solid rgb(235, 172, 216);
  cursor: pointer;
  position: relative;
  overflow: hidden;
  border-radius: 8px;
  transition: 0.3s;
  width: 48%;
}

.back-button::before, .order-again-button::before {
  content: "";
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, #ffeb3b, #ff9800, #ffeb3b);
  transition: 0.3s;
  z-index: -1;
}

.back-button:hover::before, .order-again-button:hover::before {
  left: 0;
}

.back-button:hover, .order-again-button:hover {
  background: rgba(255, 235, 59, 0.3);
  border-color: #ff9800;
}

.order-again-button {
  background-color: rgba(216, 144, 178, 0.2);
  border-color: rgb(216, 144, 178);
}

.order-again-button::before {
  background: linear-gradient(90deg, #ff9800, #ff5722, #ff9800);
}

.success-message {
  position: absolute;
  bottom: 20px;
  left: 0;
  right: 0;
  background-color: rgba(76, 175, 80, 0.8);
  color: white;
  padding: 10px;
  border-radius: 5px;
  margin: 0 auto;
  width: 80%;
  animation: fadeIn 0.5s;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Mobile responsiveness */
@media (max-width: 768px) {
  .order-card {
    padding: 20px;
    width: 95%;
  }
  
  .items-table th,
  .items-table td {
    padding: 8px;
    font-size: 14px;
  }
  
  .item-image {
    width: 40px;
    height: 40px;
  }
  
  h1 {
    font-size: 24px;
  }
  
  h2 {
    font-size: 20px;
  }
  
  .button-container {
    flex-direction: column;
  }
  
  .back-button, .order-again-button {
    width: 100%;
    margin-bottom: 10px;
  }
}

@media (max-width: 480px) {
  .items-table {
    font-size: 12px;
  }
  
  .items-table th,
  .items-table td {
    padding: 6px;
  }
  
  .item-image {
    width: 30px;
    height: 30px;
  }
}
</style>
