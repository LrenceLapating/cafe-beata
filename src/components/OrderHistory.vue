<template>
  <div class="order-history">
    <div class="header">
      <button @click="goToOrderHistory" class="back-button">← Back To Menu</button>
    </div>
    <div :class="{ 'dark-mode': isDarkMode }">
      <h1>Order History</h1>
    </div>

    <!-- Display Orders only when orders array is available -->
    <table class="order-table" v-if="orders && orders.length">
      <thead>
        <tr>
          <th>Order No. (ID)</th>
          <th>Order Date</th>
          <th>Bill Name</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="order in orders" :key="order.id">
          <td>{{ order.id }}</td>
          <td>{{ order.created_at }}</td>
          <td>{{ order.customer_name }}</td>
          
          <td>
            <button @click="viewOrderDetails(order)" class="view-details-button">View Details</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- No Orders Message -->
    <div v-else>
      <p>No orders found. Add some orders from the dashboard.</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isDarkMode: localStorage.getItem('darkMode') === 'true', // Detects dark mode
      orders: [], // Store the fetched orders
    };
  },
  methods: {
    goToOrderHistory() {
      this.$router.push({ name: 'Dashboard' });
    },

   fetchOrders() {
  const userName = localStorage.getItem('userName'); 

  if (!userName) {
    console.error("User name not found in localStorage.");
    return;
  }

  fetch(`http://127.0.0.1:8000/orders?customer_name=${userName}&status=completed`) // Fetch completed orders
    .then(response => response.json())
    .then(data => {
      if (data.orders) {
        this.orders = data.orders; 
      } else {
        this.orders = [];
        console.error("No completed orders found for this user.");
      }
    })
    .catch(error => console.error("Error fetching orders:", error));
    },

 viewOrderDetails(order) {
  this.$router.push({
    name: "OrderDetails",
    query: {
      orderId: order.id,
      customerName: order.customer_name,
      items: JSON.stringify(order.items) 
        },
      });
    },
  },
  mounted() {
    this.fetchOrders(); // Fetch orders when the component is mounted
  },
  watch: {
    isDarkMode(newValue) {
      document.body.classList.toggle('dark-mode', newValue);
    },
  },
};
</script>


<style scoped>

.dark-mode .order-table td {
  color: white; /* Make text visible */
  border-color: #666; /* Darker borders */
}


.dark-mode .order-table th {
  background-color: #444; /* Dark gray for better visibility */
  color: white; /* Make text visible */
  border-color: #666; /* Darker borders */
}

.dark-mode .order-history {
  color: white;
}
.dark-mode h1,
.dark-mode .order-table th,
.dark-mode .order-table td {
  color: white;
}


/* Basic styling for the order history page */
.order-history {
  padding: 20px;
  font-family: Arial, sans-serif;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Glowing effect for the "Back To Menu" button */
.back-button {
  padding: 10px 20px;  /* Adjust padding */
  font-size: 14px;     /* Adjust font size */
  background-color: transparent;
  color: #FFF;
  cursor: pointer;
  border-radius: 5px;
  text-transform: uppercase;
  position: relative;
  z-index: 0;
  border: none; /* Removed border */
}

.back-button::after {
  content: "";
  z-index: -1;
  position: absolute;
  width: 100%;
  height: 100%;
  background-color: #333;
  left: 0;
  top: 0;
  border-radius: 10px;
}

.back-button::before {
  content: "";
  background: linear-gradient(
    45deg,
    #FF0000, #FF7300, #FFFB00, #48FF00,
    #00FFD5, #002BFF, #FF00C8, #FF0000
  );
  position: absolute;
  top: -2px;
  left: -2px;
  background-size: 600%;
  z-index: -1;
  width: calc(100% + 4px);
  height: calc(100% + 4px);
  filter: blur(8px);
  animation: glowing 20s linear infinite;
  transition: opacity .3s ease-in-out;
  border-radius: 10px;
  opacity: 0;
}

/* Hover effect for glowing */
.back-button:hover::before {
  opacity: 1;
}

/* Active button state */
.back-button:active:after {
  background: transparent;
}

.back-button:active {
  color: #000;
  font-weight: bold;
  background-color: #d12f7a;
}

/* Glowing effect for the "View Details" button */
.view-details-button {
  padding: 10px 20px;  /* Adjust padding */
  font-size: 14px;     /* Adjust font size */
  background-color: transparent;
  color: #FFF;
  cursor: pointer;
  position: relative;
  z-index: 0;
  border-radius: 5px;
  text-transform: uppercase;
  border: none; /* Removed border */
}

.view-details-button::after {
  content: "";
  z-index: -1;
  position: absolute;
  width: 100%;
  height: 100%;
  background-color: #333;
  left: 0;
  top: 0;
  border-radius: 10px;
}

.view-details-button::before {
  content: "";
  background: linear-gradient(
    45deg,
    #FF0000, #FF7300, #FFFB00, #48FF00,
    #00FFD5, #002BFF, #FF00C8, #FF0000
  );
  position: absolute;
  top: -2px;
  left: -2px;
  background-size: 600%;
  z-index: -1;
  width: calc(100% + 4px);
  height: calc(100% + 4px);
  filter: blur(8px);
  animation: glowing 20s linear infinite;
  transition: opacity .3s ease-in-out;
  border-radius: 10px;
  opacity: 0;
}

/* Hover effect for glowing */
.view-details-button:hover::before {
  opacity: 1;
}

/* Active button state */
.view-details-button:active:after {
  background: transparent;
}

.view-details-button:active {
  color: #000;
  font-weight: bold;
  background-color: #d12f7a;
}

/* Glow Animation */
@keyframes glowing {
  0% {background-position: 0 0;}
  50% {background-position: 400% 0;}
  100% {background-position: 0 0;}
}

h1 {
  font-size: 28px;
  color: #333;
}

.order-table {
  width: 100%;
  margin-top: 20px;
  border-collapse: collapse;
}

.order-table th, .order-table td {
  padding: 10px;
  border: 1px solid #ddd;
  text-align: center;
}

.order-table th {
  background-color: #f2f2f2;
}

.order-table td button {
  background-color: #d12f7a;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.order-table td button:hover {
  background-color: #b82d67;
}

/* 📱 Mobile Responsive Adjustments */
@media (max-width: 768px) {
  .order-table th, .order-table td {
    padding: 8px;
    font-size: 14px;
  }

  .order-table td button {
    font-size: 12px;
  }
}

</style>
