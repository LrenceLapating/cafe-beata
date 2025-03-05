<template>
  <div class="dashboard">
    <!-- Sidebar Toggle Button (For Mobile) -->
    <button class="menu-button" @click="toggleSidebar">
      <div class="menu-icon-container">
        ≡
        <span v-if="unreadNotificationsCount > 0" class="menu-notification-badge">{{ unreadNotificationsCount }}</span>
      </div>
    </button>

    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    
    <div v-if="isSidebarOpen" class="overlay" @click="closeSidebar"></div>
    
    <!-- Sidebar -->
    <div :class="['sidebar', { 
      'open': isSidebarOpen, 
      'light-mode': !isDarkMode,
      'dark-mode': isDarkMode 
    }]" @click.stop>
      <button class="close-sidebar" @click="toggleSidebar">✕</button>
      
      <!-- User Profile Section -->
      <div class="user-profile-section">
        <div class="profile-image">
          <img :src="userProfileImage || require('@/assets/default.png')" alt="Profile Picture">
        </div>
        <div class="profile-info">
          <span class="user-name">{{ userName }}</span>
        </div>
      </div>

      <!-- Dark Mode Toggle beside profile -->
      <button class="theme-toggle" @click="toggleDarkMode">
        <i :class="['fas', isDarkMode ? 'fa-sun' : 'fa-moon', { 'light-icon': !isDarkMode, 'dark-icon': isDarkMode }]"></i>
      </button>

      <!-- Profile Section -->
      <button class="profile-section" @click="handleProfile">
        <i class="fas fa-user"></i>
        <span>Profile</span>
      </button>

      <!-- Utility Buttons (Removed Dark Mode from here) -->
      <div class="utility-section">
        <router-link to="/user-notifications" class="utility-button notification-link">
          <div class="notification-icon">
            <i class="fas fa-bell"></i>
            <span v-if="unreadNotificationsCount > 0" class="notification-badge">{{ unreadNotificationsCount }}</span>
          </div>
          <span>Notifications</span>
        </router-link>

        <button class="utility-button" @click="handleOrderHistory">
          <i class="fas fa-history"></i>
          <span>Order History</span>
        </button>
      </div>

      <!-- Categories -->
      <div class="menu-section">
        <h3>Drinks</h3>
        <div class="menu-items">
          <button class="menu-item" @click="filterCategory('Ice Coffee')">
            <i class="fas fa-coffee"></i>
            <span>Ice Coffees</span>
          </button>
          <button class="menu-item" @click="filterCategory('Hot Coffee')">
            <i class="fas fa-mug-hot"></i>
            <span>Hot Coffees</span>
          </button>
          <button class="menu-item" @click="filterCategory('Juice Drinks')">
            <i class="fas fa-glass-martini"></i>
            <span>Juice Drinks</span>
          </button>
          <button class="menu-item" @click="filterCategory('Milkteas')">
            <i class="fas fa-glass-whiskey"></i>
            <span>Milkteas</span>
          </button>
          <button class="menu-item" @click="filterCategory('Chocolate Drinks')">
            <i class="fas fa-circle"></i>
            <span>Chocolate Drinks</span>
          </button>
          <button class="menu-item" @click="filterCategory('Blended Frappes')">
            <i class="fas fa-blender"></i>
            <span>Blended Frappes</span>
          </button>
        </div>

        <h3>Food</h3>
        <div class="menu-items">
          <button class="menu-item" @click="filterCategory('Pasta & Dishes')">
            <i class="fas fa-utensils"></i>
            <span>Pasta & Dishes</span>
          </button>
        </div>
      </div>

      <!-- Logout Button -->
      <div class="logout-container">
        <button class="utility-button logout" @click="handleLogout">
          <i class="fas fa-sign-out-alt"></i>
          <span>Logout</span>
        </button>
      </div>
    </div>

    <!-- Main content area -->
    <div :class="['content', { 'close': isSidebarOpen }]" @click="closeSidebar">
      <!-- Top Bar -->
      <div class="top-bar">
        <div class="logo-time-container">
          <div class="logo-container">
            <img src="@/assets/cafe-logo.png" alt="University Logo" class="logo" />
          </div>
          <div class="live-time">
            <p>{{ currentTime }}</p>
          </div>
        </div>

        <div class="search-container">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Search our Drinks and Food"
            @input="filterItems"
          />
        </div>
      </div>

      <!-- Dashboard Title -->
      <h1 class="dashboard-title">Cafe Beata</h1>

      <!-- Display category title dynamically -->
      <h2>{{ currentCategory }}</h2>

      <!-- Display filtered items based on the current category -->
      <div v-if="filteredItems.length" class="items">
        <div
          v-for="item in filteredItems"
          :key="item.name"
          class="item"
          @click="navigateToConfirmOrder(item)"
        >
          <img :src="getImagePath(item.image)" :alt="item.name" />
          <div class="item-details">
            <span>{{ item.name }}</span>
            <span class="item-price">₱{{ item.price.toFixed(2) }}</span> <!-- Display price with Peso sign -->
          </div>
        </div>
      </div>
    </div>
  </div>
</template>



<script>
import { eventBus } from "@/utils/eventBus"; // Correct the path if needed
export default {
  data() {
    return {
        userName: '',
      userProfileImage: '',
      userEmail: localStorage.getItem('userEmail'),
      unreadNotificationsCount: 0,   
      refreshInterval: null,  
      searchQuery: '',
      isDarkMode: localStorage.getItem("darkMode") === "enabled",
      currentCategory: 'Ice Coffee', // Default category
      currentTime: new Date().toLocaleTimeString(),
      isSidebarOpen: false, // Sidebar starts closed
      iceCoffees: [
        { name: 'Ice Peppermint Latte', price: 115.00, image: 'peppermint-latte.png' },
        { name: 'Ice Matcha Cafe Latte', price: 115.00, image: 'matcha-cafe-latte.png' },
        { name: 'Ice Cafe Latte', price: 80.00, image: 'ice-cafe-latte.png' },
        { name: 'Ice Caramel Macchiato', price: 115.00, image: 'caramel-macchiato.png' },
        { name: 'Ice Angel Affogato', price: 115.00, image: 'angel-affogato.png' },
        { name: 'Ice Spanish Latte', price: 115.00, image: 'spanish-latte.png' },
        { name: 'Ice Cappuccino', price: 115.00, image: 'ice-cappuccino.png' },
        { name: 'Ice Cafe Mocha', price: 115.00, image: 'cafe-mocha.png' },
        { name: 'Ice Salted Caramel Macchiato', price: 115.00, image: 'salted-caramel-macchiato.png' },
        { name: 'Ice White Choco Mocha', price: 115.00, image: 'white-choco-mocha.png' },
        { name: 'Ice Vanilla Latte', price: 115.00, image: 'vanilla-latte.png' },
        { name: 'Ice Hazelnut Latte', price: 115.00, image: 'hazelnut-latte.png' },
        { name: 'Ice Cafe Frizzy', price: 80.00, image: 'cafe-frizzy.png' },
        { name: 'Ice Americano Lemon', price: 90.00, image: 'americano-lemon.png' },
        { name: 'Ice Cafe Americano', price: 75.00, image: 'ice-cafe-americano.png' }
      ],
      hotCoffees: [
        { name: 'Hot Cafe Americano', price: 70.00, image: 'cafe-americano.png' },
        { name: 'Hot Peppermint Latte', price: 90.00, image: 'hot-peppermint-latte.png' },
        { name: 'Hot Matcha Cafe Latte', price: 90.00, image: 'hot-matcha-cafe-latte.png' },
        { name: 'Hot Cafe Latte', price: 85.00, image: 'cafe-latte.png' },
        { name: 'Hot Cafe Latte Macchiato', price: 85.00, image: 'hot-cafelattemacc.png' },
        { name: 'Hot Caramel Macchiato', price: 90.00, image: 'hot-caramel-macchiato.png' },
        { name: 'Hot Spanish Latte', price: 90.00, image: 'hot-spanish-latte.png' },
        { name: 'Hot Ice Cappuccino', price: 75.00, image: 'hot-cappuccino.png' },
        { name: 'Hot Cafe Mocha', price: 90.00, image: 'hot-cafe-mocha.png' },
        { name: 'Hot Salted Caramel Macchiato', price: 90.00, image: 'hot-salted-caramel-macchiato.png' },
        { name: 'Hot Vanilla Latte', price: 90.00, image: 'hot-vanilla-latte.png' },
        { name: 'Hot Hazelnut Latte', price: 90.00, image: 'hot-hazelnut-latte.png' },
        { name: 'Hot Tea Pot', price: 60.00, image: 'hotea-pot.png' }
      ],
      juiceDrinks: [
        { name: 'Apple Juice', price: 55.00, image: 'apple.png' },
        { name: 'Carrot Juice', price: 60.00, image: 'carrot.png' },
        { name: 'Mango Juice', price: 55.00, image: 'mango.png' },
        { name: 'Yakult Lemonade', price: 55.00, image: 'yakult-lemonade.png' },
        { name: 'Yakult Honey Lemonade', price: 75.00, image: 'yakult-honey-lemonade.png' },
        { name: 'Yakult Apple Lemonade', price: 75.00, image: 'yakult-apple-lemonade.png' },
        { name: 'Yakult Orange Lemonade', price: 75.00, image: 'yakult-orange-lemonade.png' },
        { name: 'Yakult Sprite Lemonade', price: 75.00, image: 'yakult-sprite-lemonade.png' },
        { name: 'Yakult Mango Lemonade', price: 75.00, image: 'yakult-mango-lemonade.png' },
        { name: 'Yakult Caramel Lemonade', price: 75.00, image: 'yakult-caramel-lemonade.png' },
        { name: 'Yakult Strawberry Lemonade', price: 75.00, image: 'yakult-strawberry-lemonade.png' },
        { name: 'Strawberry Lemonade', price: 75.00, image: 'strawberry-lemonade.png' },
        { name: 'Strawberry Mango Blue Lemonade', price: 75.00, image: 'strawberry-mango-blue-lemonade.png' },
        { name: 'Strawberry Orange Blue Lemonade', price: 75.00, image: 'strawberry-orange-blue-lemonade.png' },
        { name: 'Strawberry Apple Lemonade', price: 75.00, image: 'strawberry-apple-lemonade.png' },
        { name: 'Orange Juice', price: 75.00, image: 'orange.png' },
        { name: 'Apple Carrot Juice', price: 75.00, image: 'apple-carrot.png' },
        { name: 'Fresh Lemon Juice', price: 60.00, image: 'fresh-lemon.png' },
        { name: 'Mogu-Mogu Yakult', price: 55.00, image: 'mogu-mogu-yakult.png' },
        { name: 'Mogu-Mogu Yakult w/ Lemon', price: 55.00, image: 'mogu-mogu-yakult-with-lemon.png' },
        { name: 'Mogu-Mogu Yakult with Honey', price: 75.00, image: 'mogu-mogu-yakult-with-honey.png' },
        { name: 'Mango Matcha Latte', price: 75.00, image: 'mango-matcha-latte.png' },
        { name: 'Mango Strawberry Latte', price: 75.00, image: 'mango-strawberry-latte.png' }
      ],
      milkteas: [
        { name: 'Avocado Milktea', price: 60.00, image: 'avocado-milktea.png' },
        { name: 'Wintermelon Milktea', price: 60.00, image: 'wintermelon-milktea.png' },
        { name: 'Okinawa Milktea', price: 60.00, image: 'okinawa-milktea.png' },
        { name: 'Mango Milktea', price: 60.00, image: 'mango-milktea.png' },
        { name: 'Oreo Milktea', price: 60.00, image: 'oreo-milktea.png' },
        { name: 'Caramel Milktea', price: 60.00, image: 'caramel-milktea.png' },
        { name: 'Chocolate Milktea', price: 60.00, image: 'chocolate-milktea.png' },
        { name: 'Mocha Milktea', price: 60.00, image: 'mocha-milktea.png' },
        { name: 'Matcha Milktea', price: 60.00, image: 'matcha-milktea.png' },
        { name: 'Taro Milktea', price: 60.00, image: 'taro-milktea.png' },
        { name: 'Red Velvet Milktea', price: 60.00, image: 'red-velvet-milktea.png' },
        { name: 'Ube Milktea', price: 60.00, image: 'ube-milktea.png' },
        { name: 'Pandan Milktea', price: 60.00, image: 'pandan-milktea.png' },
        { name: 'Strawberry Milktea', price: 60.00, image: 'strawberry-milktea.png' },
        { name: 'Melon Milktea', price: 60.00, image: 'melon-milktea.png' },
        { name: 'Ube Taro Milktea', price: 60.00, image: 'ube-taro-milktea.png' }
      ],
      chocolateDrinks: [
        { name: 'Hot Chocolate', price: 75.00, image: 'hot-chocolate.png' },
        { name: 'Cold Chocolate', price: 85.00, image: 'cold-chocolate.png' },
      ],
      blendedFrappes: [
        { name: 'Cookies & Cream Frappe', price: 90.00, image: 'cookies-and-cream.png' },
        { name: 'Ube Frappe', price: 90.00, image: 'ube.png' },
        { name: 'Mocha Frappe', price: 135.00, image: 'mocha.png' },
        { name: 'Matcha Frappe', price: 90.00, image: 'matcha.png' },
        { name: 'Mango Frappe', price: 90.00, image: 'mango-frappe.png' },
        { name: 'Chocolate Frappe', price: 90.00, image: 'chocolate.png' },
        { name: 'Strawberry Frappe', price: 90.00, image: 'strawberry.png' },
        { name: 'Pandan Frappe', price: 90.00, image: 'pandan.png' },
        { name: 'Avocado Frappe', price: 90.00, image: 'avocado.png' },
        { name: 'Melon Frappe', price: 90.00, image: 'melon.png' },
        { name: 'Cookies & Coffee Frappe', price: 135.00, image: 'cookies-and-coffee.png' }
      ],
      pastaAndDishes: [
        { name: 'Carbonara', price: 70.00, image: 'carbonara.png' },
        { name: 'Baked Mac', price: 70.00, image: 'bakemac.png' },
        { name: 'Tuna Pasta', price: 70.00, image: 'tunapasta.png' },
      ],
      filteredItems: [], // List to display filtered items
    };
  },

  

  created() {
      this.updateNotificationCount();
    window.addEventListener("notificationUpdated", this.updateNotificationCount); // Listen for changes
   this.startPollingForNewNotifications();
  },
beforeUnmount() {
      window.removeEventListener("notificationUpdated", this.updateNotificationCount);
       this.stopPollingForNewNotifications();
  },
  
  async mounted() {
   


     this.$watch(
      () => eventBus.notificationsCount,
      (newCount) => {
        this.unreadNotificationsCount = newCount;
      }
    );
    this.filterCategory('Drinks');
    this.updateTime();
    this.applyDarkMode(this.isDarkMode);
    this.startPollingForNewNotifications();
    await this.loadUserProfile();
     
  },
    
 
  methods: {


 async loadUserProfile() {
      try {
        if (!this.userEmail) return;
        
        const response = await fetch(`http://127.0.0.1:8000/profile/${this.userEmail}`);
        const data = await response.json();
        
        if (response.ok) {
          this.userName = data.username;
          this.userProfileImage = data.avatar ? `http://127.0.0.1:8000${data.avatar}` : require('@/assets/default.png');
        }
      } catch (error) {
        console.error('Error loading profile:', error);
      }
    },


  updateNotificationCount() {
      const userName = localStorage.getItem("userName");
      if (userName) {
        const userNotificationsKey = `user_notifications_${userName}`;
        const notifications = JSON.parse(localStorage.getItem(userNotificationsKey)) || [];
          const unreadCount = notifications.filter(notification => !notification.read).length;
        // Manually trigger a reactivity update for unreadNotificationsCount
        this.unreadNotificationsCount = unreadCount;
  }
  },
    
       startPollingForNewNotifications() {
      this.refreshInterval = setInterval(() => {
        this.updateNotificationCount(); // Check for new notifications
      }, 5000); // Update every 5 seconds (you can adjust this interval)
    },
    
      stopPollingForNewNotifications() {
      clearInterval(this.refreshInterval);
    },

 toggleDarkMode() {
    this.isDarkMode = !this.isDarkMode;
    localStorage.setItem("darkMode", this.isDarkMode ? "enabled" : "disabled");
    this.applyDarkMode(this.isDarkMode);
  },
  applyDarkMode(isDark) {
    if (isDark) {
      document.body.classList.add('dark-mode');
    } else {
      document.body.classList.remove('dark-mode');
    }
  },


 updateTime() {
  setInterval(() => {
    const now = new Date();
    let hours = now.getHours();
    let minutes = now.getMinutes();
    let seconds = now.getSeconds();
    let ampm = hours >= 12 ? 'PM' : 'AM';

    hours = hours % 12 || 12; // Convert 24-hour time to 12-hour format
    minutes = minutes < 10 ? '0' + minutes : minutes; // Ensure two digits for minutes
    seconds = seconds < 10 ? '0' + seconds : seconds; // Ensure two digits for seconds

    this.currentTime = `${hours}:${minutes}:${seconds} ${ampm}`; // Example: 2:03:11 PM
  }, 1000); // Update every second
    },

    filterCategory(category) {
      this.currentCategory = category;
      this.filterItems();
    },

    getImagePath(image) {
      return require(`@/assets/${image}`);
    },

    filterItems() {
      const query = this.searchQuery.toLowerCase();

      if (this.currentCategory === 'Drinks') {
        this.filteredItems = [
          ...this.iceCoffees,
          ...this.hotCoffees,
          ...this.juiceDrinks,
          ...this.milkteas,
          ...this.chocolateDrinks,
          ...this.blendedFrappes,
        ];
      } else if (this.currentCategory === 'Ice Coffee') {
        this.filteredItems = this.iceCoffees;
      } else if (this.currentCategory === 'Hot Coffee') {
        this.filteredItems = this.hotCoffees;
      } else if (this.currentCategory === 'Juice Drinks') {
        this.filteredItems = this.juiceDrinks;
      } else if (this.currentCategory === 'Milkteas') {
        this.filteredItems = this.milkteas;
      } else if (this.currentCategory === 'Chocolate Drinks') {
        this.filteredItems = this.chocolateDrinks;
      } else if (this.currentCategory === 'Blended Frappes') {
        this.filteredItems = this.blendedFrappes;
      } else if (this.currentCategory === 'Pasta & Dishes') {
        this.filteredItems = this.pastaAndDishes;
      } else {
        this.filteredItems = [];
      }

      // Apply search filtering
      this.filteredItems = this.filteredItems.filter(item =>
        item.name.toLowerCase().includes(query)
      );
    },

   navigateToConfirmOrder(item) {
      this.$router.push({
        name: "ConfirmOrder",
        query: {
          name: item.name,
          price: item.price || "N/A", // Avoid errors if price is missing
          image: item.image,
        },
      });
    },
    handleLogout() {
      localStorage.removeItem('loggedIn');
      this.$router.push({ name: 'Login' });
    },
    handleOrderHistory() {
      this.$router.push({ name: 'OrderHistory' });
    },
    handleProfile() {
      this.$router.push({ name: 'UserProfileCafe' }); // Navigate to the Profile page
    },
    toggleSidebar() {
      this.isSidebarOpen = !this.isSidebarOpen; // Toggle sidebar open/close
    },
    closeSidebar() {
      if (window.innerWidth <= 768) {
        this.isSidebarOpen = false; // Close sidebar when clicking outside on mobile
      }
    },
  },
  watch: {
    isDarkMode: {
      handler(newValue) {
        if (newValue) {
          document.body.classList.add('dark-mode');
        } else {
          document.body.classList.remove('dark-mode');
        }
      },
      immediate: true
    }
  },
};
</script>


<style scoped>


.user-profile-section {
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}


.profile-image {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid rgba(255, 255, 255, 0.2);
}

.profile-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-name {
  font-size: 1.1rem;
  font-weight: 500;
  color: #222;
}

.theme-toggle {
  position: absolute;
  top: 20px;
  left: 20px;
  background: transparent;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.theme-toggle:hover {
  background: rgba(255, 255, 255, 0.1);
}

.theme-toggle .light-icon {
  color: #333;
}

.theme-toggle .dark-icon {
  color: #fff;
}

.light-mode 

.theme-toggle {
  color: #333;
}

.light-mode 
.user-name {
  color: #333;
}
.dark-mode .user-name {
  color: #fff;
}
.dark-mode .theme-toggle {
  color: #fff;
}
.dark-mode .item {
  background-color: #555555; /* Light grey background for dark mode */
  color: #ffffff; /* Light text color */
  box-shadow: 0px 4px 6px rgba(255, 255, 255, 0.1); /* Lighter box shadow */
}

.dark-mode .item span {
  color: #ffffff; /* Light text for item span */
}

.dark-mode .item-price {
  background-color: #6e6e6e; /* Lighter background for price */
  color: #ffffff; /* Light text color for price */
}

.dark-mode .item-price:hover {
  background-color: #888888; /* Darker price background on hover */
  cursor: pointer;
}


.dark-mode-button, 
.notification-button {
  position: relative;
  background-color: rgb(48, 41, 44);
  color: white;
  padding: 8px 12px;
  font-size: 14px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s ease-in-out;
}

.notification-badge {
  position: absolute;
  top: -5px;
  right: -5px;
  background-color: red;
  color: white;
  border-radius: 50%; /* This ensures it’s fully circular */
  font-size: 12px;
  width: 20px; /* Set a fixed width */
  height: 20px; /* Set a fixed height to ensure it's circular */
  display: flex;
  justify-content: center; /* Centers the content horizontally */
  align-items: center; /* Centers the content vertically */
}

.dark-mode-button i, 
.notification-button i {
  font-size: 18px; /* Adjust icon size */
}

.top-bar-buttons {
  display: flex;
  gap: 10px; /* Space between buttons */
}

.notification-button {
  background-color: rgb(48, 41, 44); /* Same background as dark mode */
  color: white;
  padding: 8px 12px;
  font-size: 14px;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s ease-in-out;
}

.notification-button:hover {
  background-color: #b82d67; /* Same hover effect as dark mode button */
}

.notification-button i {
  font-size: 18px; /* Adjust the icon size */
}

.dark-mode {
  background-color: #121212;
  color: #ffffff;
}

/* Buttons and Sidebar in Dark Mode */
.dark-mode .sidebar,
.dark-mode .dashboard,
.dark-mode .top-bar,
.dark-mode .content {
  background-color: #1e1e1e;
  color: #ffffff;
}


/* Dark Mode Button Styling */
.dark-mode-button {
  background-color: rgb(48, 41, 44);
  color: white;
  padding: 8px 12px;
  font-size: 14px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s ease-in-out;
}

.dark-mode .sidebar,
.dark-mode .sidebar-category h3,
.dark-mode .sidebar-category ul li {
  color: #ffffff !important;
}

/* Dark Mode for Live Time */
.dark-mode .live-time {
  color: #ffffff !important;
}


   .item-details {
    display: flex;
    flex-direction: column; /* Stack the name and price vertically */
    align-items: center;
    margin-top: 10px;
  }

  /* Style the price to highlight it */
  .item-price {
    font-size: 18px;
    font-weight: bold;
    color: #d12f7a; /* Pink color for the price */
    transition: all 0.3s ease;
    margin-top: 5px; /* Add some space between the name and price */
  }

  /* Glowing effect on hover */
  .item-price:hover {
    color: #fff; /* White text color on hover */
    text-shadow: 0 0 10px rgba(209, 47, 122, 1), 0 0 20px rgba(209, 47, 122, 0.7); /* Glowing text effect */
  }

  /* Glowing Button Styles */
  .profile-button,
  .order-history-button,
  .logout-button {
    padding: 15px 40px;
    border: none;
    outline: none;
    color: #FFF;
    cursor: pointer;
    position: relative;
    z-index: 0;
    border-radius: 12px;
    background-color: transparent;
    border: 2px solid #d12f7a; /* Adjust border color */
    font-size: 14px;
   
  }

  /* Glowing effect */
  .profile-button::after,
  .order-history-button::after,
  .logout-button::after {
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

  /* Animation for glowing */
  .profile-button::before,
  .order-history-button::before,
  .logout-button::before {
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
  .profile-button:hover::before,
  .order-history-button:hover::before,
  .logout-button:hover::before {
    opacity: 1;
  }

  /* Active button state */
  .profile-button:active:after,
  .order-history-button:active:after,
  .logout-button:active:after {
    background: transparent;
  }

  .profile-button:active,
  .order-history-button:active,
  .logout-button:active {
    color: #000;
    font-weight: bold;
    background-color: #d12f7a; /* Active background color */
    border-color: #d12f7a; /* Border color */
  }

  /* Glow Animation */
  @keyframes glowing {
    0% {background-position: 0 0;}
    50% {background-position: 400% 0;}
    100% {background-position: 0 0;}
  }

/* Existing styles (unchanged) */
.profile-button {
  background-color: rgb(100, 14, 51);
  color: white;
  padding: 10px;
  font-size: 18px;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.3s ease-in-out;
  width: 40px; /* Adjust width and height for round button */
  height: 40px; /* Adjust width and height for round button */
}

.profile-button i {
  font-size: 24px; /* Adjust icon size */
}

.profile-button:hover {
  background-color: #b82d67;

}

.dashboard {
  display: flex;
  height: 100vh;
  flex-direction: column;
  background-color: #fce6e6;
}


/* Sidebar */
.sidebar {
  position: fixed;
  top: 0;
  left: -280px;
  height: 100vh;
  width: 280px;
  background-color: white;
  transition: all 0.3s ease;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  padding: 20px 0 20px 0; /* Add bottom padding */
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.sidebar.light-mode {
  background-color: #fce6e6;
}

.sidebar.dark-mode {
  background-color: #333;
  color: #fff;
}

.sidebar.dark-mode .utility-button,
.sidebar.dark-mode .menu-item,
.sidebar.dark-mode .profile-section,
.sidebar.dark-mode h3 {
  color: #fff;
}

.sidebar.dark-mode .utility-button:hover,
.sidebar.dark-mode .menu-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.sidebar.dark-mode .profile-section,
.sidebar.dark-mode .utility-section,
.sidebar.dark-mode .logout {
  border-color: rgba(255, 255, 255, 0.1);
}

.sidebar.open {
  left: 0;
}

.close-sidebar {
  position: absolute;
  top: 15px;
  right: 15px;
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: inherit;
  padding: 5px;
}

.profile-section {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px 20px;
  color: inherit;
  font-size: 15px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  background: none;
  border: none;
  width: 100%;
  cursor: pointer;
  text-align: left;
}

.profile-section:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.utility-section {
  padding: 10px 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.utility-button {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 20px;
  background: none;
  border: none;
  cursor: pointer;
  color: inherit;
  font-size: 15px;
  text-decoration: none;
  transition: background-color 0.2s;
}

.utility-button:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.notification-link {
  position: relative;
  text-decoration: none;
  color: inherit;
}

.notification-icon {
  position: relative;
  display: inline-block;
  width: 20px;
}

.notification-badge {
  position: absolute;
  top: -8px;
  right: -8px;
  background-color: red;
  color: white;
  border-radius: 50%; /* This ensures it’s fully circular */
  font-size: 11px;
  min-width: 15px;
  height: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.menu-section {
  flex: 1;
  padding: 15px 0 0 0;
  overflow-y: auto;
  margin-bottom: 0;
}

.menu-section h3 {
  padding: 0 20px;
  margin: 10px 0 5px;
  font-size: 16px;
  color: inherit;
  font-weight: 500;
}

.menu-items {
  display: flex;
  flex-direction: column;
  margin-bottom: 15px;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 20px;
  background: none;
  border: none;
  cursor: pointer;
  color: inherit;
  font-size: 15px;
  text-align: left;
  transition: background-color 0.2s;
}

.menu-item:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.menu-item i {
  width: 20px;
  text-align: center;
  font-size: 14px;
}

.logout-container {
  border-top: 1px solid rgba(0, 0, 0, 0.1);
  padding: 0;
  background-color: #fce6e6;
  margin-bottom: 20px; /* Add space after logout button */
}

.dark-mode .logout-container {
  background-color: #333;
  border-top-color: rgba(255, 255, 255, 0.1);
}

.logout {
  color: inherit;
  padding: 10px 20px;
  width: 100%;
  display: flex;
  align-items: center;
  gap: 10px;
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .content {
    margin-left: 0;
    padding: 15px;
  }
  
  .menu-button {
    display: block;
  }
}

/* Desktop Responsive */
@media (min-width: 769px) {
  .content {
    margin-left: 0; /* Remove default margin to match mobile behavior */
  }
  
  .menu-button {
    display: block; /* Show menu button on desktop */
    background: rgb(255, 255, 255);
    color: black;
    padding: 10px 15px;
    font-size: 18px;
    border-radius: 15px;
    transition: background 0.3s ease-in-out;
  }

  /* When sidebar is open */
  .sidebar.open + .content {
    margin-left: 270px;
  }
}

/* Update menu button base styles */
.menu-button {
  position: fixed;
  top: 15px;
  left: 15px;
  z-index: 300;
  background: rgb(255, 255, 255);
  color: black;
  padding: 10px 15px;
  font-size: 18px;
  border: none;
  border-radius: 15px;
  cursor: pointer;
  transition: background 0.3s ease-in-out;
  display: block; /* Always show the menu button */
}

.menu-icon-container {
  position: relative;
  display: inline-block;
}

.menu-notification-badge {
  position: absolute;
  top: -8px;
  right: -20px;
  background-color: red;
  color: white;
  border-radius: 50%;
  font-size: 12px;
  min-width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

/* Add overlay styles */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 299;
  display: none;
}

.overlay.show {
  display: block;
}

/* Update content transition */
.content {
  transition: margin-left 0.3s ease;
}

/* Style the container for both logo and live time */
.logo-time-container {
  display: flex;
  align-items: center;
  gap: 0px;
}

.search-container { 

  display: flex;
  justify-content: center; 
  padding: 10px;
  border-radius: 15px;
  width: 80%;
  max-width: 300px;
} 

/* Style for the live time text */
.live-time {
  font-weight: bold;
  font-size: 15px;
  color: #333;
  margin-top: 0; 
  font-style: italic; 
  background: transparent; 
  padding: 0;
  margin:  20px 0 0 0;
}

/* Add other necessary styling if needed */
.top-bar {
  display: flex;
   border-radius: 50px;
  background-color:rgb(255, 239, 239);
  flex-direction: column;
  text-align: center;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
 
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  flex-wrap: nowrap; 
  gap: 10px;
}

.logo-container img {
  width: 80px;
}

.content {
  flex: 1;
  margin-left: 0;
  padding: 20px;
  overflow-y: auto;
  transition: margin-left 0.3s ease;
}

.content.shifted {
  margin-left: 270px;
}

/* Menu button styles */
.menu-button {
  position: fixed;
  top: 15px;
  left: 15px;
  z-index: 300;
  background: rgb(255, 255, 255);
  color: black;
  padding: 10px 15px;
  font-size: 18px;
  border: none;
  border-radius: 15px;
  cursor: pointer;
  transition: background 0.3s ease-in-out;
  display: block;
}

/* Sidebar styles */
.sidebar {
  position: fixed;
  top: 0;
  left: -280px;
  height: 100vh;
  width: 280px;
  background-color: white;
  transition: all 0.3s ease;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  padding: 20px 0 20px 0;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.sidebar.open {
  left: 0;
}

@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    top: 0;
    left: -250px; 
    width: 250px;
    height: 100vh;
    background-color: #fce6e6;
    transition: left 0.3s ease-in-out;
    z-index: 1000;
    box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
    overflow-y: auto; 
  }

  .sidebar.open {
   left: 0; 

  }

  .content {
    margin-left: 0; 
  }
}

/* Dashboard Title */
.dashboard-title {
   font-size: 30px;
  }


.logo-container img {
  width: 80px;
}

.search-container input {
  padding: 10px;
  border-radius: 20px;
  border: 1px solid #ccc;
  width: 100%;
  max-width: 300px;
} 

/* Top Bar Buttons */
.top-bar-buttons {
  display: flex;
  gap: 5px;
}

.order-history-button,
.logout-button {
  background-color: rgb(77, 24, 48);
  color: white;
  padding: 8px 12px;
  font-size: 14px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.order-history-button:hover,
.logout-button:hover {
  background-color: #b82d67;
}

/* Dashboard Title */
.dashboard-title {
   font-size: 40px;
  font-weight: bold;
   color: #d12f7a;
  margin-top: 15px;
  margin-bottom: 15px;
  text-align: center;
  font-style: italic; 
  font-family: "Merriweather", serif; 
  letter-spacing: 1px; 
 
}

 .dashboard-title:hover {
    color: #fff; 
    text-shadow: 0 0 10px rgba(209, 47, 122, 1), 0 0 20px rgba(209, 47, 122, 0.7); 

 }
 
 .logo-container {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 10px;
}

/* Live Time container */
.live-time-container {
  display: flex;
  justify-content: center;
  align-items: center;
  color: #fff;
  font-weight: bold;
  font-size: 20px;
}

/* Style the search bar */
.search-container input {
  padding: 12px;
  border-radius: 20px;
  border: 1px solid #ccc;
  width: 100%;
  max-width: 300px;
}

.order-history-button,
  .logout-button {
    font-size: 12px;
    padding: 6px 10px;
  }
/* Categories Section */
.categories {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.category {
  width: 48%;
}

.category h2 {
  font-size: 24px;
  font-weight: bold;
  color: #d12f7a;
  text-align: center;
  margin-top: 20px;
  margin-bottom: 10px;
}

/* Items Section */
.items {
  display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
   gap: 20px;
  padding: 20px;
  justify-content: center;
  align-items: center;
}
@media (min-width: 1024px) {
  .items {
    grid-template-columns: repeat(4, 1fr);
  }
}

/* Adjust for smaller screens */
@media (max-width: 1023px) {
  .items {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .items {
     display: flex;
    grid-template-columns: repeat(2, 1fr);
       flex-direction: column;
    align-items: center;
  }
}

@media (max-width: 480px) {
  .items {
    grid-template-columns: 1fr;
  }
}

/* Item styling */
.item {
  text-align: center;
  background-color: #f8d1d1;
  border-radius: 15px;
  padding: 15px;
  cursor: pointer;
  transition: transform 0.3s ease;
  height: auto;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  max-width: 200px;
  margin: 0 auto;
  position: relative;
  overflow: hidden;
   box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

.item img {
  width: 100px;
  height: 100px;
  object-fit: contain;
}

.item:hover img {
  transform: scale(1.05);
}

.item span {
  font-weight: bold;
  color: #333;
  font-size: 16px;
  text-align: center;
  display: block;
  line-height: 1.3;
  margin-top: 8px;
}

/* Responsive Text Adjustments */
@media (max-width: 768px) {
  .dashboard-title {
    font-size: 35px;
  }

}
 .item-details {
    display: flex;
    justify-content: space-between;
   flex-direction: column;
  align-items: center;
  margin-top: 10px;
  }

  .item-price {
    font-size: 18px;
    font-weight: bold;
    color: #d12f7a; 
    background-color: #f8e1e6; 
    padding: 5px 10px;
    border-radius: 5px;
    margin-top: 5px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  .item-price:hover {
    background-color: #f8c6d0; 
    cursor: pointer;
  }

  .category h2 {
    font-size: 20px;
  }

  .item span {
    font-size: 14px;
  }

 

@media (max-width: 480px) {
  .dashboard-title {
    font-size: 30px;
  }

  .category h2 {
    font-size: 18px;
  }


  .order-history-button,
  .logout-button {
     font-size: 10px;
    padding: 5px 8px;
  }
}

</style>
