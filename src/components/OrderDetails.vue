<template>
  <div class="order-container">
    <div class="order-card">
      <h1>Order Details</h1>
      
      <div class="order-items">
        <h2>Items:</h2>
        <ul v-if="items.length">
          <li v-for="item in items" :key="item.name">
            <span>{{ item.name }} x {{ item.quantity }} - ₱{{ (item.price * item.quantity).toFixed(2) }}</span>
          </li>
        </ul>
        <p v-else>No items found.</p>
      </div>

      <button @click="goBackToHistory" class="back-button">Back to Order History</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      items: this.parseItems(this.$route.query.items),
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
  },
};
</script>



<style scoped>
.order-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #1e1e2f, #3a3a52);
  color: white;
}

.order-card {
  background: rgba(255, 255, 255, 0.1);
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  text-align: center;
  width: 350px;
  backdrop-filter: blur(10px);
}

h1 {
  font-size: 28px;
  margin-bottom: 15px;
  color:rgb(216, 144, 178);
}

.order-info p {
  font-size: 18px;
  margin: 8px 0;
}

.order-info span {
  font-weight: bold;
  color:rgb(236, 155, 225);
}

.total {
  font-size: 22px;
  font-weight: bold;
  color: #ff5722;
}

.order-items {
  margin-top: 20px;
  text-align: left;
}

.item-details {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 15px;
}

.item-details img {
  width: 50px;
  height: 50px;
  object-fit: contain;
  margin-right: 15px;
}

.item-details div {
  flex: 1;
  text-align: left;
}



.back-button {
  padding: 12px 25px;
  font-size: 14px;
  font-weight: bold;
  background: transparent;
  color: #fff;
  border: 2px solidrgb(235, 172, 216);
  cursor: pointer;
  position: relative;
  overflow: hidden;
  border-radius: 8px;
  transition: 0.3s;
}



.back-button::before {
  content: "";
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, #ffeb3b, #ff9800, #ffeb3b);
  transition: 0.3s;
}

.back-button:hover::before {
  left: 0;
}

.back-button:hover {
  background: rgba(255, 235, 59, 0.3);
  border-color: #ff9800;
}
</style>
