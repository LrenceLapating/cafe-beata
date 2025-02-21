<template>
  <div class="notifications-page">
    <div class="header">
      <h1>Admin Dashboard</h1>
      <button @click="goToOrderRecord" class="order-record-button">View Order History</button>
    </div>

    <div v-if="isLoading" class="loading">Loading...</div>

    <div v-if="orders.length && !isLoading" class="orders-list">
      <h2>Pending Orders</h2>
      <div class="order-item" v-for="order in orders" :key="order.id">
        <div class="order-details">
          <h3>Order ID: {{ order.id }}</h3>
          <p><strong>Customer:</strong> {{ order.customer_name }}</p>
          <p><strong>Status:</strong> {{ order.status }}</p>
          <div>
            <strong>Items:</strong>
            <ul>
              <li v-for="item in order.items" :key="item.name">
                {{ item.name }} - ₱{{ item.price }} x {{ item.quantity }}
              </li>
            </ul>
          </div>
        </div>

        <!-- Mark as Completed button (small version) -->
        <button @click="markAsCompleted(order.id, order.customer_name)" class="mark-completed-btn small-btn">
          Mark as Completed
        </button>

        <!-- Decline button -->
        <button @click="openDeclineDialog(order)" class="decline-btn">
          Decline
        </button>

        <!-- Custom message input for decline -->
        <div v-if="order.id === activeDeclineOrderId">
          <textarea v-model="customDeclineMessage" placeholder="Customize your message here..." rows="3"></textarea>
          <button @click="declineOrder(order.id, order.customer_name)" class="decline-submit-btn">
            Submit Decline
          </button>
        </div>
      </div>
    </div>

    <div v-else-if="!isLoading">
      <p>No pending orders at the moment.</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      orders: [], // Store pending orders
      isLoading: false, // For loading state
      refreshInterval: null, // Interval reference for auto-refresh
      activeDeclineOrderId: null, // Track the order for which decline message is being customized
      customDeclineMessage: "", // Store the custom decline message
    };
  },
  methods: {
    // Fetch orders from API
    fetchOrders() {
      this.isLoading = true;
      fetch("http://127.0.0.1:8000/orders")
        .then(response => response.json())
        .then((data) => {
          if (data.orders && Array.isArray(data.orders)) {
            // Only show pending orders
            this.orders = data.orders.filter(order => order.status === "pending");
          } else {
            console.error("Invalid data format", data);
            this.orders = [];
          }
        })
        .catch(error => console.error("Error fetching orders:", error))
        .finally(() => {
          this.isLoading = false;
        });
    },

    // Mark an order as completed and send notification
    markAsCompleted(orderId, customerName) {
      fetch(`http://127.0.0.1:8000/orders/${orderId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: "completed" }) // Properly formatted JSON
      })
        .then(response => {
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          return response.json();
        })
        .then(() => {
          // Immediately remove from pending orders
          this.orders = this.orders.filter(order => order.id !== orderId);

          // Prepare the notification
          const notification = {
            orderId,
            customerName,
            message: "Your order is now ready! Proceed to the cashier for payment and pickup.",
            timestamp: new Date().toISOString(),
          };

          // Save the notification in localStorage for the specific user
          const userNotificationsKey = `user_notifications_${customerName}`;
          let notifications = JSON.parse(localStorage.getItem(userNotificationsKey)) || [];
          notifications.push(notification);
          localStorage.setItem(userNotificationsKey, JSON.stringify(notifications));

          // Emit an event to notify other components (optional)
          window.dispatchEvent(new Event("orderCompleted"));

          alert("Order marked as completed!");
        })
        .catch(error => console.error("Error marking order as completed:", error));
    },

    // Open the custom decline message input for a specific order
    openDeclineDialog(order) {
      this.activeDeclineOrderId = order.id;
      this.customDeclineMessage = localStorage.getItem(`customDeclineMessage_${order.id}`) || ""; // Get saved message from localStorage
    },

    // Decline an order and send notification with custom message
    declineOrder(orderId, customerName) {
      const message = this.customDeclineMessage || "Unfortunately, this item is temporarily out of stock. We apologize for the inconvenience and appreciate your patience.";

      fetch(`http://127.0.0.1:8000/orders/${orderId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: "declined" }) // Properly formatted JSON
      })
        .then(response => {
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          return response.json();
        })
        .then(() => {
          // Immediately remove from pending orders
          this.orders = this.orders.filter(order => order.id !== orderId);

          // Prepare the notification with the custom message
          const notification = {
            orderId,
            customerName,
            message,
            timestamp: new Date().toISOString(),
          };

          // Save the notification in localStorage for the specific user
          const userNotificationsKey = `user_notifications_${customerName}`;
          let notifications = JSON.parse(localStorage.getItem(userNotificationsKey)) || [];
          notifications.push(notification);
          localStorage.setItem(userNotificationsKey, JSON.stringify(notifications));

          // Emit an event to notify other components (optional)
          window.dispatchEvent(new Event("orderDeclined"));

          alert("Order has been declined!");
        })
        .catch(error => console.error("Error declining order:", error));
      
      // Reset after submission
      this.activeDeclineOrderId = null;
      this.customDeclineMessage = "";
      localStorage.removeItem(`customDeclineMessage_${orderId}`); // Clear message from localStorage after submission
    },

    // Save the decline message to localStorage whenever it's updated
    updateDeclineMessage() {
      if (this.activeDeclineOrderId !== null) {
        localStorage.setItem(`customDeclineMessage_${this.activeDeclineOrderId}`, this.customDeclineMessage);
      }
    },

    // Start auto-refresh for pending orders every 10 seconds (instead of 1 second)
    startAutoRefresh() {
      this.refreshInterval = setInterval(() => {
        this.fetchOrders();
      }, 10000); // Set to 10000ms (10 seconds)
    },

    // Stop auto-refresh
    stopAutoRefresh() {
      if (this.refreshInterval) {
        clearInterval(this.refreshInterval);
        this.refreshInterval = null;
      }
    }
  },

  mounted() {
    this.fetchOrders();
    this.startAutoRefresh(); // Start auto-fetching every 10 seconds
  },

  beforeUnmount() {
    this.stopAutoRefresh(); // Stop fetching when leaving the page
  }
};
</script>


<style scoped>
/* Header styles */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.order-record-button {
  background-color: #f8d2e4;
  color: #d12f7a;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}

.order-record-button:hover {
  background-color: #d12f7a;
  color: white;
}

.notifications-page {
  padding: 20px;
}

h1 {
  color: #d12f7a;
  font-size: 28px;
}

.orders-list {
  display: flex;
  flex-wrap: wrap;
  gap: 50px;  /* Adjust the gap for better spacing */
  justify-content: flex-start;  /* Align items to the left */
}

.order-item {
  background-color: #f8d2e4; /* Light pink background */
  padding: 15px; /* Adjust padding for uniform size */
  width: calc(23.66% - 25px); /* Adjust width for 6 items per row */
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;  
  flex-direction: column;
  justify-content: space-between;
  height: 250px; /* Fixed height for all items to ensure consistency */
  box-sizing: border-box; /* Ensure padding is included in width/height */
}

.order-details h3 {
  color: #d12f7a;
}

.order-details p {
  margin: 5px 0;
}

ul {
  list-style-type: none;
  padding-left: 20px;
}

button.mark-completed-btn {
  background-color: #d12f7a;
  color: white;
  border: none;
  padding: 5px 10px; /* Smaller size */
  border-radius: 5px;
  cursor: pointer;
  margin-top: auto;
}

button.mark-completed-btn:hover {
  background-color: #b82d67;
}


button.decline-btn {
  background-color: #f5a5a5;
  color: white;
  border: none;
  padding: 5px 10px; /* Smaller size */
  border-radius: 5px;
  cursor: pointer;
  margin-top: 10px;
}

button.decline-btn:hover {
  background-color: #f17b7b;
}


.decline-submit-btn {
  background-color: #f17b7b;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 10px;
}
.decline-submit-btn:hover {
  background-color: #d05e5e;
}

textarea {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  border-radius: 5px;
  border: 1px solid #ccc;
}


.loading {
  text-align: center;
  color: #d12f7a;
  font-size: 20px;
  margin-top: 20px;
}

p {
  text-align: center;
}
</style>