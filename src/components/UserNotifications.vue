<template>
  <div class="notifications-container">
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
      <div v-for="(notification, index) in notifications" :key="index" class="notification-item">
        <p class="order-id">Order ID: {{ notification.orderId }}</p>
        <p class="notification-message">{{ notification.message }}</p>
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
    };
  },
  methods: {
    // Fetch notifications specific to the current user
    fetchNotifications() {
      const userName = localStorage.getItem("userName");  // Get the logged-in user's name
      if (userName) {
        const userNotificationsKey = `user_notifications_${userName}`;  // Key specific to the user
        const storedNotifications = JSON.parse(localStorage.getItem(userNotificationsKey)) || [];
        this.notifications = storedNotifications;
      }
    },

    // Clear all notifications (optional, if you want to give the user this option)
    clearNotifications() {
      const userName = localStorage.getItem("userName"); // Get the logged-in user's name
      if (userName) {
        const userNotificationsKey = `user_notifications_${userName}`;
        localStorage.removeItem(userNotificationsKey);
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
.notifications-container {
  padding: 20px;
  background-color: #f6f6f6;
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

.back-button i {
  margin-right: 5px;
}

.notifications-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
  text-align: center;
}

.clear-btn {
  background-color: #d12f7a;
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
</style>
