<template>
  <div class="notifications-page">
    <div class="header">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">

      <button @click="goToOrderRecord" class="order-record-button">View Order Record</button>
      <h1>Admin Dashboard</h1>
      <button @click="logout" class="logout-button">
        <i class="fa-solid fa-right-from-bracket"></i>
      </button>
    </div>

    <div v-if="isLoading" class="loading">Loading...</div>

    <div v-if="orders.length && !isLoading" class="orders-list">
      <h2>Pending Orders</h2>
      <div class="order-item" v-for="order in orders" :key="order.id">
        <div class="order-details">
          <h3>Order ID: {{ order.id }}</h3>
          <p><strong>Customer:</strong> {{ order.customer_name }}</p>
          <p><strong>Status:</strong> {{ order.status }}</p>
          <div class="items-section">
            <strong>Items:</strong>
            <ul>
              <li v-for="item in order.items" :key="item.name">
                {{ item.name }} - ₱{{ item.price }} x {{ item.quantity }}
              </li>
            </ul>
          </div>

          <!-- Total Amount below items -->
          <div class="order-total">
            <p><strong>Total Amount: ₱{{ calculateOrderTotal(order.items) }}</strong></p>
          </div>
        </div>

        <!-- Mark as Completed button -->
        <button @click="markAsCompleted(order.id, order.customer_name, order.items)" class="mark-completed-btn small-btn">
          Mark as Completed
        </button>

        <!-- Decline button -->
        <button @click="openDeclineDialog(order)" class="decline-btn">
          Decline
        </button>

        <!-- Custom message input for decline -->
        <div v-if="order.id === activeDeclineOrderId" class="decline-container">
          <textarea v-model="customDeclineMessage" placeholder="Customize your message here..." rows="3" ref="declineText"></textarea>
          
          <!-- Button Container -->
          <div class="decline-buttons">
            <button @click="declineOrder(order.id, order.customer_name, order.items)" class="decline-submit-btn">
              Submit
            </button>
            <button @click="activeDeclineOrderId = null" class="decline-cancel-btn">
              Cancel
            </button>
          </div>
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

    // Method to format the order date in the required format
    formatDate(dateString) {
      const date = new Date(dateString);
      const hours = date.getHours();
      const minutes = date.getMinutes();
      const seconds = date.getSeconds();
      const period = hours >= 12 ? 'PM' : 'AM';
      const formattedDate = `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')} ${period}${(hours % 12 || 12)}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
      return formattedDate;
    },

    cancelDecline() {
      this.activeDeclineOrderId = null; // Hide decline input
      this.customDeclineMessage = ""; // Clear text
    },

    // Navigate to the Order Record page
    goToOrderRecord() {
      this.$router.push({ name: "OrderRecord" });  // Ensure this matches the name of the route
    },

    logout() {
     
      this.$router.push({ name: "Login" });  // Redirect the user to the Login page (adjust the route as needed)
    },

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

    // Format ordered items for notification message
    formatItems(items) {
      if (!Array.isArray(items)) {
        console.error("Invalid item format:", items);
        return "Invalid item data";
      }
      return items.map(item => `${item.name} x${item.quantity}`).join(", ");
    },

    // Calculate the total price for a single order
    calculateOrderTotal(items) {
      if (!Array.isArray(items)) return "₱0";
      return items.reduce((sum, item) => sum + item.price * item.quantity, 0).toFixed(2);
    },

    // Mark an order as completed and send notification
    markAsCompleted(orderId, customerName, items) {
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

          // Calculate the total price
          const total = items.reduce((sum, item) => sum + item.price * item.quantity, 0).toFixed(2);

          // Prepare the notification with highlighted order details (HTML added)
          const notification = {
            orderId,
            customerName,
            message: `Your order is now ready! Proceed to the cashier for payment and pickup. <span class="highlighted-order-details">Order details: ${this.formatItems(items)}. Total: ₱${total}</span>`,
            timestamp: new Date().toISOString(),
            items,  // Include items in the notification
            total,  // Include total in the notification
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
    declineOrder(orderId, customerName, items) {
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

          // Calculate the total price
          const total = items.reduce((sum, item) => sum + item.price * item.quantity, 0).toFixed(2);

          // Prepare the notification with the custom message and order details
          const notification = {
            orderId,
            customerName,
            message: `${message} Order details: ${this.formatItems(items)}. Total: ₱${total}`,
            timestamp: new Date().toISOString(),
            items,  // Include items in the notification
            total,  // Include total in the notification
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


.decline-container {
  width: 100%; 
  max-width: 400px; /* Set maximum width */
  padding: 15px;
  box-sizing: border-box; 
  background: rgba(255, 255, 255, 0.95);
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  text-align: center;
  display: flex;
  flex-direction: column; /* Stack textarea and buttons vertically */
}

.decline-container textarea {
  width: 100%;
  height: 80px; /* Set the height as per requirement */
  border-radius: 5px;
  border: 1px solid #ccc;
  padding: 10px;
  font-size: 14px;
  margin-bottom: 10px; /* Space between textarea and buttons */
}




.decline-buttons {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  margin-top: 10px;
}

.highlighted-order-details {
  display: inline-block;
  background-color: #f8d2e4;  /* Light pink background */
  color: #d12f7a;  /* Bold color for text */
  padding: 10px;
  border-radius: 5px;
  margin-top: 10px;
  font-weight: bold;
  border: 2px solid #d12f7a;  /* Adding a border to make it stand out */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  text-align: center;
}

/* Optional: Adding an underline to make it more prominent */
.highlighted-order-details::before {
  content: "——— ";
  font-size: 24px;
  font-weight: bold;
  color: #d12f7a;
}

.logout-button i {
  font-size: 18px;
}

/* Header styles */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  gap: 10px;
}
.header-buttons {
  display: flex;
  gap: 10px;
}

.logout-button {
  background-color: #f8d2e4;
  color: #d12f7a;
  padding: 10px 20px;
  border-radius: 10px;
  cursor: pointer;
}

.logout-button:hover {
  background-color: #b82d67;
}

.order-record-button {
  background-color: #f8d2e4;
  color: #d12f7a;
  padding: 8px 20px;
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

.order-total {
  margin-top: 10px;
  font-weight: bold;
  color: #d12f7a;
  text-align: center; /* Ensure it aligns nicely with the rest of the content */
}

.order-item {
  background-color: #f8d2e4; /* Light pink background */
  padding: 15px;
  width: auto; /* Make the width flexible to adapt to content */
  min-width: 200px; /* Minimum width to maintain design */
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: auto; /* Let height adjust based on content */
  box-sizing: border-box;
  margin-bottom: 20px;
}

.order-details h3 {
  color: #d12f7a;
}

.order-details p {
  margin: 5px 0;
}

.items-section {
  margin-top: 10px; 
  flex-grow: 1; /* Allow the items section to expand and adapt */
}


ul {
  list-style-type: none;
  padding-left: 20px;
  margin: 0;
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

.decline-submit-btn,
.decline-cancel-btn {
  background-color: #f17b7b;
  color: white;
  border: none;
  padding: 8px 14px;
  border-radius: 5px;
  cursor: pointer;
  width: 48%; /* Adjust button width to fit both buttons */
}

.decline-submit-btn:hover,
.decline-cancel-btn:hover {
  background-color: #d05e5e;
}

.decline-submit-btn {
  background-color: #f17b7b;
  color: white;
  border: none;
  padding: 8px 14px;
  border-radius: 5px;
  cursor: pointer;
  flex: 1; /* Makes both buttons the same size */
}
.decline-submit-btn:hover {
  background-color: #d05e5e;
}


.decline-cancel-btn {
  background-color: #cccccc;
  color: black;
  border: none;
  padding: 6px 10px;
  border-radius: 5px;
  cursor: pointer;
  flex: 1;
}

.decline-cancel-btn:hover {
  background-color: #999999;
}

.order-item {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-sizing: border-box;
}
.decline-actions {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  margin-top: 10px;
}

textarea {
  width: 100%; /* Make it fill the container width */
  height: 80px; /* Adjust the height to your desired size */
  border: 1px solid #ccc; /* Gray border */
  border-radius: 5px; /* Rounded corners */
  padding: 10px;
  font-size: 14px;
  box-sizing: border-box; /* Ensures padding is included within the width/height */
  resize: none; /* Disable resizing */
  margin-bottom: 10px; /* Space between textarea and buttons */
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
