<template>
  <div class="confirm-order">
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
        <button @click="confirmOrder" class="glowing-btn" :disabled="cart.length === 0">Confirm Order</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isDarkMode: localStorage.getItem('darkMode') === 'true', // Load Dark Mode preference
      cart: [], // Store multiple selected items
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
    
    // ✅ Fix: Always check and apply dark mode on page load
    if (localStorage.getItem('darkMode') === 'true') {
      this.isDarkMode = true; // Ensure reactivity
      document.body.classList.add('dark-mode');
    }
  },
  methods: {
    // 🌓 Toggle Dark Mode and save preference
    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode; // Toggle dark mode state
      localStorage.setItem('darkMode', this.isDarkMode); // Save preference

      // ✅ Apply or remove dark mode class dynamically
      if (this.isDarkMode) {
        document.body.classList.add('dark-mode');
      } else {
        document.body.classList.remove('dark-mode');
      }
    },

    // Load previous cart items (from localStorage)
    loadCart() {
      const storedCart = localStorage.getItem('cart');
      if (storedCart) {
        this.cart = JSON.parse(storedCart);
      }
    },

    // Add the newly selected item to the cart
    addToCart() {
      const newItem = {
        name: this.$route.query.name,
        price: Number(this.$route.query.price) || 0,
        image: this.$route.query.image,
        quantity: 1, // Default quantity
      };

      if (newItem.name && newItem.price) {
        // Check if item already exists in cart, just increase quantity
        const existingItem = this.cart.find(item => item.name === newItem.name);
        if (existingItem) {
          existingItem.quantity += 1;
        } else {
          this.cart.push(newItem);
        }
        this.saveCart();
      }
    },

    // Increase item quantity
    increaseQuantity(index) {
      this.cart[index].quantity += 1;
      this.saveCart();
    },

    // Decrease item quantity but not below 1
    decreaseQuantity(index) {
      if (this.cart[index].quantity > 1) {
        this.cart[index].quantity -= 1;
        this.saveCart();
      }
    },

    // Remove an item from the cart
    removeFromCart(index) {
      this.cart.splice(index, 1);
      this.saveCart();
    },

    // Save cart to localStorage
    saveCart() {
      localStorage.setItem('cart', JSON.stringify(this.cart));
    },

    // Go back to dashboard to add more orders
    addMoreOrder() {
      this.$router.push({ name: 'Dashboard' });
    },

    // Generate a sequential order ID and confirm the order
    confirmOrder() {
      // Show confirmation dialog
      const isConfirmed = window.confirm("Are you sure this is everything you want to order?");

      if (isConfirmed) {
        // Get the current order ID from localStorage, or set to 1 if it doesn't exist
        let orderID = localStorage.getItem('currentOrderID') || 1;

        // Increment the order ID by 1 for the next order
        orderID = parseInt(orderID) + 1;

        // Save the updated order ID back to localStorage
        localStorage.setItem('currentOrderID', orderID);

        // Pass the order details to the Order ID Page
        this.$router.push({
          name: 'OrderIDPage', // Ensure this matches the name in the router
          query: {
            orderID: orderID,  // New sequential Order ID
            items: JSON.stringify(this.cart),  // Cart items as JSON
            totalPrice: this.totalPrice,  // Total price
          },
        });

        // Clear the cart after confirming the order
        localStorage.removeItem('cart');
        this.cart = [];
      } else {
        // If the user cancels, do nothing
        return;
      }
    },

    // Helper function to load images properly
    getImagePath(image) {
      return require(`@/assets/${image}`);
    },
  },
};
</script>



<style scoped>


.dark-mode li {
  background-color: #f8d2e4 !important; /* Keep pink background */
  color: black !important; /* Make text dark for readability */
}
.dark-mode li h3,
.dark-mode li span {
  color: black !important;
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
  background-color: #fff;
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
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
}

/* Order List Items */
li {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 15px 0;
  padding: 15px;
  background-color: #f8d2e4;
  border-radius: 12px;
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
  background-color: #d12f7a;
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
