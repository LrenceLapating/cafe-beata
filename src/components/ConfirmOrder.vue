<template>
  <div>
    <link href="https://fonts.googleapis.com/css2?family=Dancing+Script&display=swap" rel="stylesheet">

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
        <h1 class="wedding-text">Café Beàta</h1>
        <h1 class="loading-text">Processing your order...</h1>
        <div class="progress-bar-container">
          <div class="progress-bar" :style="{ width: progressBarWidth + '%' }"></div>
        </div>
      </div>

      <!-- Confirm Order Content -->
      <h1>Confirm Your Order</h1>

      <div v-if="cart.length">
        <h2>Orders:</h2>
        <ul>
          <li v-for="(order, index) in cart" :key="index">
            <img :src="getImagePath(order.image)" :alt="order.name" class="order-image"/>
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
          <button @click="openModal" class="glowing-btn" :disabled="cart.length === 0 || isProcessingOrder">Confirm Order</button>
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
    };
  },
  computed: {
    totalPrice() {
      return this.cart.reduce((total, item) => total + item.price * item.quantity, 0);
    },
  },
  mounted() {
    this.loadCart();
    this.addToCart();
    console.log('Customer Name:', this.userName);  // Debug to check if userName is fetched correctly
    
    // Dynamically adjust the background color and height of the confirm order container
    this.adjustContainerHeight();
  },
  methods: {
    loadCart() {
      const storedCart = localStorage.getItem('cart');
      if (storedCart) {
        this.cart = JSON.parse(storedCart);
      }
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


    addToCart() {
      const newItem = {
        name: this.$route.query.name,
        price: Number(this.$route.query.price) || 0,
        image: this.$route.query.image,
        quantity: 1, // Default quantity
      };

      if (newItem.name && newItem.price) {
        const existingItem = this.cart.find(item => item.name === newItem.name);
        if (existingItem) {
          existingItem.quantity += 1;
        } else {
          this.cart.push(newItem);
        }
        this.saveCart();
      }
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
    saveCart() {
      localStorage.setItem('cart', JSON.stringify(this.cart));
    },
    addMoreOrder() {
      this.$router.push({ name: 'Dashboard' });
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

      // Interval for countdown and progress bar
      const interval = setInterval(() => {
        if (this.countdown > 0) {
          this.countdown--;
          this.progressBarWidth += 33.33; // Update the progress bar width
        } else {
          clearInterval(interval); // Stop the interval
          this.processOrder(); // Call the function to send the order
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
          price: item.price
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

        // Clear cart data after the order is placed
        localStorage.removeItem('cart');
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

    getImagePath(image) {
      return require(`@/assets/${image}`);
    }
  },
};
</script>




<style scoped>

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
  background-color:#f8d1d1; /* Dark Pink background */
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
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3); /* Lighter shadow for dark mode */
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
   background-color: #f8d1d1;
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
</style>
