<template>
  <div>
    <!-- Confirm Modal -->
    <div v-if="showModal" class="custom-modal">
      <div class="modal-content">
        <span class="close" @click="closeModal">&times;</span>
        <h2>📢 Hey, Wait!!</h2>
        <p>Are you sure, that this is all you want to order?</p>
        <div class="modal-buttons">
          <button @click="confirmOrder" class="yes-btn">Yes, I'm sure</button>
          <button @click="stayOnPage" class="no-btn">No, I want to order more</button>
        </div>
      </div>
    </div>

    <!-- Main content -->
    <div class="confirm-order">
      <!-- Processing Order Section (centered) -->
      <div v-show="isProcessingOrder" class="loading-spinner-container">
        <button class="close-processing" @click="cancelProcessing">&times;</button>
        <h1 class="wedding-text">Café Beàta</h1>
        <h1 class="loading-text">Processing your order...</h1>
        <div class="progress-bar-container">
          <div class="progress-bar" :style="{ width: progressBarWidth + '%' }"></div>
        </div>
      </div>

      <!-- Order Closed Message -->
      <div v-if="!isCafeOpen" class="closed-message">
        <p>We apologize for the inconvenience. Café Beàta is currently closed. Our operating hours are Monday to Saturday, from 6:00 AM to 9:30 PM. </p>
      </div>

      <!-- Confirm Order Content -->
      <h1>Confirm Your Order</h1>

      <div v-if="cart.length">
        <h2>Your Order:</h2>
        <ul>
          <li v-for="(order, index) in cart" :key="index">
            <img :src="getImagePath(order)" :alt="order.name" class="order-image"/>
            <span>{{ order.name }} - ₱{{ order.price * order.quantity }}</span>

            <!-- Quantity Controls -->
            <div class="quantity-controls">
              <button @click="decreaseQuantity(index)">-</button>
              <span>{{ order.quantity }}</span>
              <button @click="increaseQuantity(index)">+</button>
            </div>

            <button class="remove-btn" @click="removeFromCart(index)">Remove</button>
          </li>
        </ul>

        <!-- Total Price -->
        <h2>Total: ₱{{ totalPrice }}</h2>
      </div>

      <!-- No items in cart -->
      <p v-else>No items in cart. Add some from the dashboard.</p>

      <!-- Separate Buttons -->
      <div class="buttons">
        <div class="add-more-button">
          <button @click="addMoreOrder" class="glowing-btn">Add More Order</button>
        </div>
        <div class="confirm-button">
          <button @click="openModal" class="glowing-btn" :disabled="cart.length === 0 || isProcessingOrder || !isCafeOpen">
            Confirm Order
          </button>
        </div>
      </div>
    </div>
  </div>
</template>



<script>
export default {
  data() {
    return {
      cart: [], // Store multiple selected items
      userName: localStorage.getItem('userName') || "Guest", // Fetch the logged-in user's name
      isProcessingOrder: false,  // Track the order processing state
      showModal: false, // Track the modal visibility
      countdown: 3, // Countdown timer for the processing
      progressBarWidth: 0, // Progress bar width
      showOrderClosedMessage: false,
      progressInterval: null, // Store the interval reference
      isItemAdded: false, // New flag to track if item has been added
      isCafeOpen: true, // Add this line to define isCafeOpen
      // Map of product names to their image paths
      productImages: {
        // Ice Coffees
        'Ice Peppermint Latte': 'peppermint-latte.png',
        'Ice Matcha Cafe Latte': 'matcha-cafe-latte.png',
        'Ice Cafe Latte': 'ice-cafe-latte.png',
        'Ice Caramel Macchiato': 'caramel-macchiato.png',
        'Ice Angel Affogato': 'angel-affogato.png',
        'Ice Spanish Latte': 'spanish-latte.png',
        'Ice Cappuccino': 'ice-cappuccino.png',
        'Ice Cafe Mocha': 'cafe-mocha.png',
        'Ice Salted Caramel Macchiato': 'salted-caramel-macchiato.png',
        'Ice White Choco Mocha': 'white-choco-mocha.png',
        'Ice Vanilla Latte': 'vanilla-latte.png',
        'Ice Hazelnut Latte': 'hazelnut-latte.png',
        'Ice Cafe Frizzy': 'cafe-frizzy.png',
        'Ice Americano Lemon': 'americano-lemon.png',
        'Ice Cafe Americano': 'ice-cafe-americano.png',
        
        // Hot Coffees
        'Hot Cafe Americano': 'cafe-americano.png',
        'Hot Peppermint Latte': 'hot-peppermint-latte.png',
        'Hot Matcha Cafe Latte': 'hot-matcha-cafe-latte.png',
        'Hot Cafe Latte': 'cafe-latte.png',
        'Hot Cafe Latte Macchiato': 'hot-cafelattemacc.png',
        'Hot Caramel Macchiato': 'hot-caramel-macchiato.png',
        'Hot Spanish Latte': 'hot-spanish-latte.png',
        'Hot Cappuccino': 'hot-cappuccino.png',
        'Hot Cafe Mocha': 'hot-cafe-mocha.png',
        'Hot Salted Caramel Macchiato': 'hot-salted-caramel-macchiato.png',
        'Hot Vanilla Latte': 'hot-vanilla-latte.png',
        'Hot Hazelnut Latte': 'hot-hazelnut-latte.png',
        'Hot Tea Pot': 'hotea-pot.png',
        
        // Juice Drinks
        'Apple Juice': 'apple.png',
        'Carrot Juice': 'carrot.png',
        'Mango Juice': 'mango.png',
        'Orange Juice': 'orange.png',
        'Fresh Lemon Juice': 'fresh-lemon.png',
        'Strawberry Lemonade': 'strawberry-lemonade.png',
        'Yakult Lemonade': 'yakult-lemonade.png',
        'Yakult Honey Lemonade': 'yakult-honey-lemonade.png',
        'Yakult Apple Lemonade': 'yakult-apple-lemonade.png',
        'Yakult Orange Lemonade': 'yakult-orange-lemonade.png',
        'Yakult Sprite Lemonade': 'yakult-sprite-lemonade.png',
        'Yakult Mango Lemonade': 'yakult-mango-lemonade.png',
        'Yakult Caramel Lemonade': 'yakult-caramel-lemonade.png',
        'Yakult Strawberry Lemonade': 'yakult-strawberry-lemonade.png',
        'Strawberry Mango Blue Lemonade': 'strawberry-mango-blue-lemonade.png',
        'Strawberry Orange Blue Lemonade': 'strawberry-orange-blue-lemonade.png',
        'Strawberry Apple Lemonade': 'strawberry-apple-lemonade.png',
        'Apple Carrot Juice': 'apple-carrot.png',
        'Mogu-Mogu Yakult': 'mogu-mogu-yakult.png',
        'Mogu-Mogu Yakult w/ Lemon': 'mogu-mogu-yakult-with-lemon.png',
        'Mogu-Mogu Yakult with Honey': 'mogu-mogu-yakult-with-honey.png',
        'Mango Matcha Latte': 'mango-matcha-latte.png',
        'Mango Strawberry Latte': 'mango-strawberry-latte.png',
        
        // Milkteas
        'Avocado Milktea': 'avocado-milktea.png',
        'Wintermelon Milktea': 'wintermelon-milktea.png',
        'Okinawa Milktea': 'okinawa-milktea.png',
        'Mango Milktea': 'mango-milktea.png',
        'Oreo Milktea': 'oreo-milktea.png',
        'Caramel Milktea': 'caramel-milktea.png',
        'Chocolate Milktea': 'chocolate-milktea.png',
        'Mocha Milktea': 'mocha-milktea.png',
        'Matcha Milktea': 'matcha-milktea.png',
        'Taro Milktea': 'taro-milktea.png',
        'Red Velvet Milktea': 'red-velvet-milktea.png',
        'Ube Milktea': 'ube-milktea.png',
        'Pandan Milktea': 'pandan-milktea.png',
        'Strawberry Milktea': 'strawberry-milktea.png',
        'Melon Milktea': 'melon-milktea.png',
        'Ube Taro Milktea': 'ube-taro-milktea.png',
        
        // Chocolate Drinks
        'Hot Chocolate': 'hot-chocolate.png',
        'Cold Chocolate': 'cold-chocolate.png',
        
        // Blended Frappes
        'Cookies & Cream Frappe': 'cookies-and-cream.png',
        'Ube Frappe': 'ube.png',
        'Mocha Frappe': 'mocha.png',
        'Matcha Frappe': 'matcha.png',
        'Mango Frappe': 'mango-frappe.png',
        'Chocolate Frappe': 'chocolate.png',
        'Strawberry Frappe': 'strawberry.png',
        'Pandan Frappe': 'pandan.png',
        'Avocado Frappe': 'avocado.png',
        'Melon Frappe': 'melon.png',
        'Cookies & Coffee Frappe': 'cookies-and-coffee.png',
        
        // Pasta and Dishes
        'Carbonara': 'carbonara.png',
        'Baked Mac': 'bakemac.png',
        'Tuna Pasta': 'tunapasta.png'
      }
    };
  },
  computed: {
    totalPrice() {
      return this.cart.reduce((total, item) => total + item.price * item.quantity, 0);
    },
  },
  mounted() {
    // Initialize isCafeOpen from localStorage
    const savedCafeStatus = localStorage.getItem('isCafeOpen');
    if (savedCafeStatus !== null) {
      this.isCafeOpen = JSON.parse(savedCafeStatus);
    }
    
    // Load existing cart first
    this.loadCart();
    
    // Check URL parameters and add item only if not already done
    const itemFromUrl = this.$route.query.name && this.$route.query.price;
    if (itemFromUrl && !this.isItemAdded) {
      this.handleNewItem();
    }
    
    console.log('Customer Name:', this.userName);
    
    // Dynamically adjust the background color and height of the confirm order container
    this.adjustContainerHeight();

    // Check if the cafe is open, if not show the closed message
    if (!this.isCafeOpen) {
      this.openOrderClosedMessage();
    }
  },
  methods: {
    isCafeOpenMethod() {
      const now = new Date();
      const dayOfWeek = now.getDay(); // 0 is Sunday, 1 is Monday, ..., 6 is Saturday
      const hour = now.getHours();
      const minute = now.getMinutes();

      // The cafe is open Monday to Saturday, from 6:00 AM to 9:30 PM
      if (dayOfWeek === 0 || // Closed on Sunday
          hour < 6 || // Before 6 AM
          (hour === 9 && minute > 30) || // After 9:30 PM
          hour > 21) { // After 9 PM
        return false; // Cafe is closed
      }
      return true; // Cafe is open
    },

    openOrderClosedMessage() {
      this.showOrderClosedMessage = true;
      this.showModal = false; // Close the modal if it's open
    },

    closeOrderClosedMessage() {
      this.showOrderClosedMessage = false;
    },

    loadCart() {
      const userCartKey = `cart_${this.userName}`; // Create user-specific cart key
      const storedCart = localStorage.getItem(userCartKey);
      if (storedCart) {
        this.cart = JSON.parse(storedCart);
        // Check if we have items from URL in the cart
        if (this.$route.query.name) {
          const urlItemExists = this.cart.some(item => item.name === this.$route.query.name);
          this.isItemAdded = urlItemExists;
        }
      }
    },

    handleNewItem() {
      const itemName = this.$route.query.name;
      const newItem = {
        name: itemName,
        price: Number(this.$route.query.price) || 0,
        quantity: 1
      };
      
      // Set image path - use provided image from URL parameters
      if (this.$route.query.image) {
        newItem.image = this.$route.query.image;
        
        // If the image is a backend path without the full URL, ensure it's properly formatted
        if (newItem.image.startsWith('/uploads')) {
          // The image path is already in the correct format for getImagePath to handle
          console.log('Using backend image path:', newItem.image);
        }
      } else if (this.productImages[itemName]) {
        // Fallback to the product mapping for predefined items
        newItem.image = this.productImages[itemName];
      } else {
        // If no image is provided and no mapping exists, set a flag to use default image
        console.log('No image found for item:', itemName);
        newItem.image = 'default.png';
      }

      // Check if item exists in cart
      const existingItemIndex = this.cart.findIndex(item => item.name === newItem.name);
      
      if (existingItemIndex === -1) {
        // Item doesn't exist, add it
        this.cart.push(newItem);
        this.isItemAdded = true;
        this.saveCart();
      }
    },

    saveCart() {
      const userCartKey = `cart_${this.userName}`; // Use the same user-specific cart key
      localStorage.setItem(userCartKey, JSON.stringify(this.cart));
    },

    startProcessingOrder() {
      this.isProcessingOrder = true;  // This will display the loading section
      this.progressBarWidth = 0;  // Reset the progress bar to 0%
      this.updateProgressBar();   // Example method to update progress
    },

    updateProgressBar() {
      let width = 0;
      const interval = setInterval(() => {
        if (width < 100) {
          width += 10;
          this.progressBarWidth = width;
        } else {
          clearInterval(interval);
        }
      }, 1000);  // Update every second
    },

    stopProcessingOrder() {
      this.isProcessingOrder = false;  // Stop the loading process
    },

    increaseQuantity(index) {
      this.cart[index].quantity += 1;
      this.saveCart();
    },

    decreaseQuantity(index) {
      if (this.cart[index].quantity > 1) {
        this.cart[index].quantity -= 1;
        this.saveCart();
      }
    },

    removeFromCart(index) {
      this.cart.splice(index, 1);
      this.saveCart();
    },

    addMoreOrder() {
      // Get the last category from localStorage
      const lastCategory = localStorage.getItem('lastCategory');
      
      // Navigate back to Dashboard with the category as a query parameter if available
      if (lastCategory) {
        this.$router.push({ 
          name: 'Dashboard',
          query: { category: lastCategory }
        });
      } else {
        this.$router.push({ name: 'Dashboard' });
      }
    },

    openModal() {
      this.showModal = true;
    },

    closeModal() {
      this.showModal = false;
    },

    confirmOrder() {
      this.showModal = false; // Close the modal

      // Show loading spinner and start countdown
      this.isProcessingOrder = true;
      this.progressBarWidth = 0;
      this.countdown = 2;

      // Store the interval reference so we can clear it when canceling
      this.progressInterval = setInterval(() => {
        if (this.countdown > 0 && this.isProcessingOrder) { // Check if still processing
          this.countdown--;
          this.progressBarWidth += 33.33; // Update the progress bar width
        } else if (this.isProcessingOrder) { // Only process if not cancelled
          clearInterval(this.progressInterval);
          this.processOrder(); // Call the function to send the order
        } else {
          clearInterval(this.progressInterval);
        }
      }, 1000); // Update every second
    },

    processOrder() {
      const customerName = localStorage.getItem('userName') || "Unknown";  // Fetch the correct username
      console.log('Customer Name:', customerName);  // Debugging

      const orderData = {
        customer_name: customerName,  // Use username here
        items: this.cart.map(item => ({
          name: item.name,
          quantity: item.quantity,
          price: item.price,
          image: item.image // Include the image path
        })),
        status: 'pending'
      };

      // Proceed to send the order data to the backend
      fetch('http://127.0.0.1:8000/orders', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(orderData)
      })
      .then(response => response.json())
      .then((data) => {
        this.isProcessingOrder = false; // Hide the loading spinner
        const orderID = data.order_id; // Use the specific order ID returned from the server

        // Navigate to the Order ID page after the delay
        this.$router.push({
          name: 'OrderIDPage',
          query: {
            orderID: orderID,
            customerName: customerName,
            items: JSON.stringify(this.cart),
            totalPrice: this.totalPrice
          }
        });

        // Clear cart data after the order is placed - use user-specific key
        const userCartKey = `cart_${this.userName}`;
        localStorage.removeItem(userCartKey);
        this.cart = [];
      })
      .catch(error => {
        this.isProcessingOrder = false; // Hide the loading spinner
        console.error("Error creating order:", error);
      });
    },

    stayOnPage() {
      this.showModal = false; // Close the modal and stay on the page
    },

    adjustContainerHeight() {
      const orderItems = document.querySelectorAll('.order-details li'); // Get all items in the order list
      const confirmOrderContainer = document.querySelector('.confirm-order'); // Get the confirm-order container

      const totalItems = orderItems.length;  // Calculate the number of items

      // Dynamically adjust padding based on the number of items
      if (totalItems <= 3) {
        confirmOrderContainer.style.padding = '20px';  // For fewer items, keep normal padding
      } else if (totalItems <= 6) {
        confirmOrderContainer.style.padding = '25px';  // For moderate items, add more padding
      } else {
        confirmOrderContainer.style.padding = '30px';  // For many items, add more padding
      }
    },

    getImagePath(item) {
      // If item has a direct image path and it's a URL or starts with /uploads, use it directly
      if (item.image) {
        if (item.image.startsWith('http://') || item.image.startsWith('https://') || item.image.startsWith('/uploads')) {
          return item.image;
        }
        // Try to load the image from assets using the direct path
        try {
          return require(`@/assets/${item.image}`);
        } catch (error) {
          console.log(`Failed to load direct image path: ${item.image}, trying product map...`);
        }
      }
      
      // Try to find the image by product name in the productImages map
      if (this.productImages[item.name]) {
        try {
          return require(`@/assets/${this.productImages[item.name]}`);
        } catch (error) {
          console.error(`Failed to load mapped image for: ${item.name}`, error);
        }
      }
      
      // If all else fails, return the default image
      return require('@/assets/default.png');
    },
    cancelProcessing() {
      this.isProcessingOrder = false;
      this.progressBarWidth = 0;
      this.showModal = false;
      if (this.progressInterval) {
        clearInterval(this.progressInterval);
      }
    },
  },
};
</script>





<style scoped>


.closed-message {
  background-color: rgba(0, 0, 0, 0.7); /* Semi-transparent background */
  color: #fff; /* White text color */
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  font-size: 24px; /* Larger text size */
  font-family: 'Dancing Script', cursive; /* Match font family */
  position: fixed;
  top: 30%;
  left: 50%;
  transform: translateX(-50%); /* Center the popup */
  width: 80%;
  max-width: 600px; /* Limit the width */
  z-index: 9999; /* Make sure it's on top of everything else */
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3); /* Shadow for the popup */
}

.closed-message p {
  margin: 0;
  font-size: 22px; /* Larger font size for the message text */
  font-weight: bold; /* Make the message text bold */
}

.closed-message .close-btn {
  background-color: #FF5C5C;
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  margin-top: 20px;
  font-size: 18px;
  transition: background-color 0.3s ease;
}

.closed-message .close-btn:hover {
  background-color: #FF3B3B; /* Darker red on hover */
}

.wedding-text {
  font-size: 36px; /* Larger size for emphasis */
  font-weight: bold;
  color: #d12f7a; /* Dark pink */
  font-family: 'Dancing Script', cursive; /* Cursive font like in the image */
  margin-bottom: 10px; /* Space below the Wedding text */
}

/* Normal Loading Text */
.loading-text {
  font-size: 24px;  /* Adjust the size of the text */
  font-weight: normal;  /* Regular weight for the text */
  color: black;  /* White color to contrast with the background */
  font-family: Arial, sans-serif; /* A simple font for "loading..." */
  margin-top: 10px; /* Space between Wedding text and loading text */
}

/* Progress Bar Container with Dark Pink Background */
.progress-bar-container {
  margin-top: 20px;
  width: 100%; /* Full width of container */
  max-width: 400px;  /* Limit the max width of the progress bar */
  height: 30px;
  background-color: #d85d7f; /* Dark Pink background color */
  border-radius: 20px;
  overflow: hidden;
}

/* Striped Red Progress Bar */
.progress-bar {
  height: 100%;
  background: repeating-linear-gradient(
    45deg,
    red 0%,
    red 10%,
    #d85d7f 10%,
    #d85d7f 20%
  );
  border-radius: 20px;
  animation: progressAnimation 3s linear infinite;
}

@keyframes progressAnimation {
  0% { width: 0%; }
  100% { width: 100%; }
}

.loading-spinner-container {
  position: fixed;  /* Fixed position so it's always visible on the screen */
  top: 50%;  /* Center vertically */
  left: 50%;  /* Center horizontally */
  transform: translate(-50%, -50%);  /* Adjust for perfect centering */
  z-index: 1000;  /* Ensure it stays on top */
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  text-align: center;
  padding: 20px;
  background-color:#f8d2e4; /* Dark Pink background */
  border-radius: 35px;  /* Rounded corners */
  width: 80%;  /* Ensure the container width is sufficient */
  max-width: 600px;  /* Set a max width for the container */
  min-height: 200px; /* Set a minimum height to ensure visibility */
  margin: 0 auto;  /* Center the container */
  overflow: visible;  /* Ensure nothing is clipped */
}

/* Mobile adjustments */
@media (max-width: 768px) {
  .loading-spinner-container {
    width: 80%;  /* Reduce width to 80% for smaller screens */
    padding: 12px;  /* Reduce padding for a more compact container */
    max-height: 250px;  /* Limit the height for medium-sized screens */
    overflow: hidden;  /* Prevent overflow if content exceeds max height */
  }
  .progress-bar-container {
    max-width: 250px;  /* Adjust progress bar width for smaller screens */
  }
}

@media (max-width: 480px) {
  .loading-spinner-container {
    width: 75%;  /* Reduce width to 75% for very small screens */
    padding: 10px;  /* Further reduce padding */
    max-height: 200px;  /* Set a smaller height for very small screens */
    height: auto;  /* Allow height to adjust automatically */
    overflow: hidden;  /* Prevent content from overflowing */
  }
  .progress-bar-container {
    max-width: 220px;  /* Make the progress bar smaller for very small screens */
  }
}


.custom-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal-content {
  background-color: #fce6e6;
  padding: 30px;
  border-radius: 10px;
  text-align: center;
  width: 80%;
  max-width: 600px;
}


.close {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 24px;
  color: #333;
  cursor: pointer;
}

.modal-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.modal-buttons button {
  padding: 10px 15px;
  font-size: 14px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.yes-btn {
  background-color:rgb(136, 132, 136);
  color: white;
}

.no-btn {
  background-color:rgb(255, 0, 128);
  color: white;
}

.yes-btn:hover {
  background-color: #ff9a29;
}

.no-btn:hover {
  background-color: #b82d67;
}

/* Dark Mode for the Loading Spinner Container */
.dark-mode .loading-spinner-container {
  background-color: #333;  /* Dark background color for dark mode */
  color: #fff;  /* White text color for dark mode */
  border-radius: 35px;  /* Keep the rounded corners */
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3); /* Lighter shadow for dark mode */
}

.dark-mode .loading-text {
  color: #fff;  /* White color for the loading text */
}

.dark-mode .progress-bar-container {
  background-color: #444;  /* Dark background for progress bar container */
}

.dark-mode .progress-bar {
  background: repeating-linear-gradient(
    45deg,
    #555 0%, 
    #555 10%, 
    #333 10%, 
    #333 20%  /* Darker stripes for progress bar in dark mode */
  );
  animation: progressAnimation 3s linear infinite;
}

.dark-mode .loading-spinner-container .progress-bar-container {
  background-color: #555;  /* Slightly lighter background for the progress bar container */
}

.dark-mode .spinner {
  border-top: 4px solid #3498db; /* Blue color for the spinner */
  border-color: #555; /* Darker border for spinner */
}

/* Adjust the progress bar text color in dark mode */
.dark-mode .loading-text {
  color: #ddd;  /* Light gray for text in dark mode */
}

/* Optional: Apply shadow to make text and progress bar stand out more */
.dark-mode .loading-spinner-container {
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.7);  /* Stronger shadow for dark mode */
}



.dark-mode .loading-spinner {
  background-color: #333333; /* Dark background */
  color: white; /* White text */
  box-shadow: 0px 4px 6px rgba(255, 255, 255, 0.1); /* Lighter shadow */
}

/* Dark Mode for Spinner Circle */
.dark-mode .spinner {
  border-top: 4px solid #3498db; /* Keep blue color for spinner */
  border-color: #555555; /* Darker border for spinner */
}

/* Dark Mode for Loading Bar */
.dark-mode .loading-bar {
  background-color: #444444; /* Darker background for loading bar */
}

.dark-mode .progress {
  background-color: #2ecc71; /* Light green progress bar */
}


/* Dark Mode for Quantity Controls Button */
.dark-mode .quantity-controls button {
  background-color: #555555; /* Darker background for quantity buttons */
  color: white; /* White text color */
  border: 1px solid #777777; /* Darker border for quantity buttons */
  border-radius: 50%; /* Keep the circular shape */
  padding: 5px;
  font-size: 18px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

/* Dark Mode Hover Effect for Quantity Controls Button */
.dark-mode .quantity-controls button:hover {
  background-color: #666666; /* Slightly lighter background on hover */
}

/* Dark Mode Active State for Quantity Controls Button */
.dark-mode .quantity-controls button:active {
  background-color: #777777; /* Darker background when active */
}


/* Dark Mode for Modal Content */
.dark-mode .modal-content {
  background-color: #222222; /* Dark background for modal content */
  color: #ffffff; /* White text */
  box-shadow: 0px 4px 6px rgba(255, 255, 255, 0.2); /* Lighter shadow for modal */
  border-radius: 10px; /* Rounded corners */
  padding: 30px;
  width: 80%;
  max-width: 600px;
  text-align: center;
}

/* Dark Mode for Modal Buttons inside Modal */
.dark-mode .modal-buttons button {
  background-color: #444444; /* Dark buttons */
  color: white; /* White text for buttons */
  border: 1px solid #666666; /* Darker borders for buttons */
}

.dark-mode .modal-buttons button:hover {
  background-color: #555555; /* Darker button on hover */
}

/* Dark Mode for Close Button inside Modal */
.dark-mode .close {
  color: #ffffff; /* White color for close button */
}


/* Dark Mode for "No" Button with Light Pink */
.dark-mode .no-btn {
  background-color: #f8c6d0 !important; /* Light pink color */
  color: black !important; /* White text */
  border: 1px solid #f8a1b2 !important; /* Lighter border for pink */
}

.dark-mode .no-btn:hover {
  background-color: #f7a3b1 !important; /* Darker pink when hovered */
}


.dark-mode li {
  background-color: #444444; /* Darker background for list items */
  color: #ffffff; /* White text for list items */
  border-radius: 10px; /* Optional: to match rounded corners */
  padding: 10px; /* Add some padding for better spacing */
  margin-bottom: 10px; /* Space between list items */
}
.dark-mode li h3,
.dark-mode li span {
  color: #ffffff; /* White text for headings and spans */
}


.dark-mode ul {
  background-color: #333333; /* Dark background */
  color: #ffffff; /* White text color */
}
.dark-mode li:hover {
  background-color: #555555; /* Lighter background on hover */
}

/* 🕶 Dark Mode - Lighten Text */
.dark-mode .confirm-order {
  color: white;
  background-color: #222; /* Dark background */
}

/* 🕶 Dark Mode - Cart Items */
.dark-mode .cart-item {
  background-color: #333; /* Darker container */
    color: black !important; /* Ensure text is black */
  border: 1px solid #555; /* Darker borders */
}

.dark-mode .cart-item span {
  color: black !important;
}

/* 🕶 Dark Mode - Buttons */
.dark-mode .cart-item button {
  background-color: #444; /* Dark button */
  color: white !important; /* Keep button text white */
  border: 1px solid #666;
}

.dark-mode .cart-item button:hover {
  background-color: #666;
}

/* 🕶 Dark Mode - Price Text */
.dark-mode .total-price {
  color: #ddd; /* Light gray for visibility */
}



/* Confirm Order Page */
.confirm-order {
  text-align: center;
  padding: 20px;
  background-color: #fce6e6;
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  height: 100vh; /* Auto height to fit the content */
  max-height: 95vh; /* Maximum height to avoid overflowing */
  overflow-y: auto; /* Enable scrolling if content exceeds the height */
  transition: height 0.3s ease;  /* Smooth transition when height changes */
}

/* Order Image */
.order-image {
  width: 70px; /* Increased for better visibility */
  height: 70px;
  margin-right: 15px;
  border-radius: 8px;
  object-fit: cover;
}

ul {
  list-style-type: none;
  padding: 0;
  
   border-radius: 30px;
}

/* Order List Items */
li {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 15px 0;
  padding: 15px;
  background-color: #f8d1d1;
  border-radius: 30px;
  flex-wrap: wrap; /* Ensures content wraps properly on small screens */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Quantity Controls */
.quantity-controls {
  display: flex;
  align-items: center;
  gap: 12px;
}

.quantity-controls button {
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  background-color:rgb(219, 144, 144);
  color: white;
  font-size: 18px;
  transition: background 0.3s;
}

.quantity-controls button:hover {
  background-color: #b82d67;
}

/* Remove Button */
.remove-btn {
  background-color: red;
  color: white;
  padding: 5px 5px;
  font-size: 14px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s;
}

.remove-btn:hover {
  background-color: darkred;
}
@media (max-width: 480px) {
    button[data-v-77d1959e] {
        font-size: 13px;
        padding: 8px;
        max-width: 260px;
    }
}

/* Buttons Container */
.buttons {
  margin-top: 30px;
  display: flex;
  justify-content: space-between;  /* Distribute buttons to far left and right */
  width: 100%;  /* Ensure buttons take up the full width */
}

/* Glowing effect for the "Add More Order" and "Confirm Order" buttons */
.glowing-btn {
  padding: 8px 20px;  /* Smaller padding */
  font-size: 12px;     /* Smaller font size */
  background-color: #333; /* Black background */
  color: #FFF;
  border: 2px solid #d12f7a; /* Adjust border color */
  cursor: pointer;
  position: relative;
  z-index: 0;
  border-radius: 5px;
  text-transform: uppercase;
}

.glowing-btn::after {
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

.glowing-btn::before {
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
.glowing-btn:hover::before {
  opacity: 1;
}

/* Active button state */
.glowing-btn:active:after {
  background: transparent;
}

.glowing-btn:active {
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

/* 📱 Mobile Responsive Adjustments */
@media (max-width: 768px) {
  .confirm-order {
    padding: 15px;
  }

  .order-image {
    width: 55px;
    height: 55px;
  }

  li {
    flex-direction: column; /* Stack items vertically */
    align-items: center;
    text-align: center;
    padding: 20px;
  }

  .quantity-controls {
    gap: 8px;
    margin-top: 10px;
  }

  .quantity-controls button {
    width: 35px;
    height: 35px;
    font-size: 16px;
  }

  .remove-btn {
    font-size: 12px;
    padding: 6px 10px;
  }

  button {
    font-size: 14px;
    padding: 12px;
    max-width: 280px;
  }
}



@media (max-width: 480px) {
    .remove-btn[data-v-77d1959e] {
        font-size: 12px;
        padding: 5px 8px;
        margin-top: 10px; /* Adjust this value to move the button down */
    }
} 

@media (max-width: 768px) {
    .remove-btn[data-v-77d1959e] {
        font-size: 12px;
        padding: 6px 10px;
        margin-top: 12px; /* Adjust this value to move the button down */
    }
}


/* Extra Small Screens (iPhone SE, very small phones) */
@media (max-width: 480px) {
  .order-image {
    width: 45px;
    height: 45px;
  }

  .quantity-controls button {
    width: 32px;
    height: 32px;
    font-size: 14px;
  }

  .remove-btn {
    font-size: 12px;
    padding: 5px 8px;
  }

  button {
    font-size: 13px;
    padding: 10px;
    max-width: 260px;
  }
}

.close-processing {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 32px;
  cursor: pointer;
  color: #333;
  padding: 5px 10px;
  border-radius: 50%;
  transition: all 0.3s ease;
  z-index: 1001;
}

@media (max-width: 768px) {
  .close-processing {
    font-size: 28px; /* Adjust size for mobile */
  }
}

@media (max-width: 480px) {
  .close-processing {
    font-size: 24px; /* Further adjust size for very small screens */
  }
}

.dark-mode .close-processing {
  color: #fff;
}

.dark-mode .close-processing:hover {
  background-color: rgba(255, 255, 255, 0.1);
}
</style>
