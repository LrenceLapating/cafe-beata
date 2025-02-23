<template>
  <div :class="['notifications-container', { 'dark-mode': isDarkMode }]">
    <!-- Back Button -->
    <router-link to="/dashboard" class="back-button">
      <i class="fas fa-arrow-left"></i> Back
    </router-link>

    <!-- Title -->
    <h2 class="notifications-title">Notifications</h2>

    <!-- Clear Notifications Button -->
    <button class="clear-btn" @click="clearNotifications">Clear Notifications</button>

    <!-- Notifications List -->
    <div class="notifications-list">
      <!-- Check if there are no notifications -->
      <p v-if="notifications.length === 0" class="no-notifications">
        No notifications at the moment.
      </p>

      <!-- Render notifications if there are any -->
      <div v-for="(notification, index) in notifications" :key="index" class="notification-item">
        <p class="order-id">Order ID: {{ notification.orderId }}</p>
        <!-- Render message with highlighted details -->
        <p class="notification-message" v-html="formatHighlightedMessage(notification.message)"></p>
        <hr />
      </div>
    </div>
  </div>
</template>


<script>
export default {  
  data() {
    return {
      notifications: [],  // Will hold notifications fetched from localStorage
      refreshInterval: null, // To store the interval ID for clearing later
      isDarkMode: localStorage.getItem("darkMode") === "true", // Fetch dark mode setting from localStorage
    };
  },
  methods: {
    // Fetch notifications specific to the current user
    fetchNotifications() {
      const userName = localStorage.getItem("userName");  // Get the logged-in user's name
      if (userName) {
        const userNotificationsKey = `user_notifications_${userName}`;  // Use the user-specific key
        const storedNotifications = JSON.parse(localStorage.getItem(userNotificationsKey)) || [];
        this.notifications = storedNotifications;  // Only display notifications for the current user
      } else {
        this.notifications = [];
      }
    },

    // Method to format and highlight the "Order details" and "Total"
    formatHighlightedMessage(message) {
      return message.replace(
        /(Order details:.*?Total:.*?)/,
        `<br/><br/><span class="highlighted-order-details">$1</span>`  
      );
    },

    // Clear all notifications (optional, if you want to give the user this option)
    clearNotifications() {
      const userName = localStorage.getItem("userName"); // Get the logged-in user's name
      if (userName) {
        const userNotificationsKey = `user_notifications_${userName}`;  // Use the user-specific key
        localStorage.removeItem(userNotificationsKey);  // Clear notifications for this specific user
        this.notifications = []; 
      }
    },

    // Set up auto-refresh every 5 seconds to check for updates
    startAutoRefresh() {
      this.refreshInterval = setInterval(() => {
        this.fetchNotifications();
      }, 5000); // 5000 ms = 5 seconds
    },

    // Stop auto-refresh (for cleanup, if necessary)
    stopAutoRefresh() {
      if (this.refreshInterval) {
        clearInterval(this.refreshInterval);
      }
    }
  },
  created() {
    // Fetch notifications when the component is created
    this.fetchNotifications();
    this.startAutoRefresh();
  },
  beforeUnmount() {
    // Stop the auto-refresh interval when the component is destroyed
    this.stopAutoRefresh();
  }
};
</script>





<style scoped>
/* Highlighted Order Details */
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

/* Dark Mode Styles */
.dark-mode .notifications-container {
  background-color: #333;
  color: white;  /* Light text for dark mode */
}

.dark-mode .notification-item {
  background-color: #444;
  color: white; /* Light text color for dark background */
}

.dark-mode .order-id,
.dark-mode .notification-message {
   color: white; /* Lighter text color in dark mode */
}

.dark-mode .back-button {
   color: white; /* White text for the back button */
}

.dark-mode .highlighted-order-details {
  background-color: #555;
  color: #ffcc00;
  border: 2px solid #ffcc00;
}

/* Default Light Mode Styles */
.notifications-container {
  padding: 20px;
  background-color: #fce6e6;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.back-button {
  font-size: 18px;
  color: #333;
  margin-bottom: 10px;
  text-decoration: none;
}

.notifications-title {
  font-size: 24px;
  font-weight: bold;
  color: #white;
  margin-bottom: 20px;
  text-align: center;
}

.clear-btn {
  background-color:rgb(66, 47, 56);
  color: white;
  padding: 8px 16px;
  border: none;
  font-size: 16px;
  border-radius: 5px;
  cursor: pointer;
  align-self: flex-end;
  margin-bottom: 20px;
}

.clear-btn:hover {
  background-color: #b82d67;
}

.notifications-list {
  flex-grow: 1;
  overflow-y: auto;
}

.notification-item {
  background-color: #e6e6e6;
  margin-bottom: 10px;
  padding: 15px;
  border-radius: 10px;
}

.order-id {
  font-weight: bold;
  color: #333;
}

.notification-message {
  color: #333;
}

hr {
  margin: 10px 0;
  border-color: #ccc;
}

.no-notifications {
  font-size: 18px;
  color: #d12f7a;
  font-weight: bold;
  text-align: center;
  margin-top: 20px;
  padding: 15px;
  border-radius: 5px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
