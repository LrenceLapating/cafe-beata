<template>
  <div :class="['notifications-container', { 'dark-mode': isDarkMode }]">
    <!-- Back Button -->
    <router-link to="/dashboard" class="back-button">
      ← Back
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
        
        <!-- Time Ago -->
        <p class="notification-time">{{ formatTimeAgo(notification.timestamp) }}</p>
        
        <hr />
      </div>
    </div>
  </div>
</template>


<script>
import { eventBus } from "@/utils/eventBus"; // Correct the path if needed

export default {
  data() {
    return {
      notifications: [],  // Will hold notifications fetched from localStorage
      refreshInterval: null, // To store the interval ID for clearing later
      isDarkMode: localStorage.getItem("darkMode") === "true", // Fetch dark mode setting from localStorage
    };
  },
  methods: {
    // Method to get time ago in a human-readable format
    formatTimeAgo(timestamp) {
      const now = new Date();
      const diff = now - new Date(timestamp); // Difference in milliseconds
      const minutes = Math.floor(diff / 1000 / 60);
      const hours = Math.floor(diff / 1000 / 60 / 60);
      const days = Math.floor(diff / 1000 / 60 / 60 / 24);

      if (days > 0) return `${days} day${days > 1 ? "s" : ""} ago`;
      if (hours > 0) return `${hours} hour${hours > 1 ? "s" : ""} ago`;
      if (minutes > 0) return `${minutes} minute${minutes > 1 ? "s" : ""} ago`;
      return "Just now";
    },

    updateNotificationCount() {
      const unreadCount = this.notifications.filter(notification => !notification.read).length;
      eventBus.notificationsCount = unreadCount; 
    },

    fetchNotifications() {
      const userName = localStorage.getItem("userName"); 
      if (userName) {
        const userNotificationsKey = `user_notifications_${userName}`;
        const storedNotifications = JSON.parse(localStorage.getItem(userNotificationsKey)) || [];
        this.notifications = storedNotifications.reverse();  // Reverse the notifications array to display newest first
        this.updateNotificationCount(); // Call to update the count
      } else {
        this.notifications = [];
      }
    },

    addNewNotification(notification) {
      const userName = localStorage.getItem("userName");
      const userNotificationsKey = `user_notifications_${userName}`;
      let notifications = JSON.parse(localStorage.getItem(userNotificationsKey)) || [];
      
      // Add the new notification at the start of the array (newest first)
      notifications.unshift(notification);
      localStorage.setItem(userNotificationsKey, JSON.stringify(notifications));

      // Emit event to update the Dashboard's notification count
      window.dispatchEvent(new Event("notificationUpdated"));
    },

    formatHighlightedMessage(message) {
      return message.replace(
        /(Order details:.*?Total:.*?)/,
        `<br/><br/><span class="highlighted-order-details">$1</span>`  
      );
    },

    clearNotifications() {
      const userName = localStorage.getItem("userName");
      if (userName) {
        const userNotificationsKey = `user_notifications_${userName}`;
        localStorage.removeItem(userNotificationsKey);  // Clear notifications for this specific user
        this.notifications = [];
        localStorage.setItem("unread_notifications", 0);

        // Emit event to update Dashboard's notification count
        window.dispatchEvent(new Event("notificationUpdated"));
      }
    },

    startAutoRefresh() {
      this.refreshInterval = setInterval(() => {
        this.fetchNotifications();
      }, 5000); // 5000 ms = 5 seconds
    },

    stopAutoRefresh() {
      if (this.refreshInterval) {
        clearInterval(this.refreshInterval);
      }
    }
  },
  created() {
    this.fetchNotifications();
    this.startAutoRefresh();
    window.addEventListener("notificationUpdated", this.fetchNotifications);
  },
  beforeUnmount() {
    window.removeEventListener("notificationUpdated", this.fetchNotifications);
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
.dark-mode .notification-time {
  color: #ccc;
}



.dark-mode .notification-item {
  background-color: #444;
  color: white; /* Light text color for dark background */
}

.dark-mode .order-id,
.dark-mode .no-notifications,
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
  background-color: rgb(66, 47, 56);
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
  margin-bottom: 20px;
  padding: 15px;
  border-radius: 10px;
}

.order-id {
  font-weight: bold;
  color: #333;
  font-size: 20px;
}

.notification-message {
  color: #333;
  font-size: 19px;
}

.notification-time {
  font-size: 14px;
  color: #222; /* Lighter color for the time ago text */
  margin-top: 10px;
  font-style: italic;
  text-align: right; /* Align time to the right */
}

hr {
  margin: 10px 0;
  border-color: #ccc;
}

.no-notifications {
  font-size: 18px;
  color: rgb(68, 68, 68);
  font-weight: bold;
  text-align: center;
  margin-top: 20px;
  padding: 15px;
  border-radius: 5px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
