<template>
  <div :class="['order-id-page', { 'dark-mode': isDarkMode }]">
    <h4>Please Screenshot Your OrderID Number!</h4>
    <h1>Order Confirmation</h1>

    <!-- Display Generated Order ID -->
    <div class="order-id">
      <h2>Order ID: {{ orderID }}</h2>
    </div>

    <!-- Display Order Details -->
    <div class="order-details">
      <h3></h3>
      <ul>
        <li v-for="(item, index) in orderItems" :key="index">
          <span>{{ item.name }} - ₱{{ item.price * item.quantity }}</span>
          <span> x {{ item.quantity }}</span>
        </li>
      </ul>
    </div>

    <!-- Estimated Delivery Time -->
    <div class="delivery-time">
      <h3>Estimated Pickup Time: {{ estimatedTime }} minutes</h3>
    </div>

    <div class="buttons">
      <button @click="goBackToDashboard" class="back-button">Back to Dashboard</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      orderID: this.generateOrderID(),
      orderItems: [],
      estimatedTime: 0,
      isDarkMode: localStorage.getItem("darkMode") === "true",
    };
  },
  created() {
    this.loadOrderItems();
  },
  mounted() {
    // ✅ Apply dark mode if stored in localStorage
    if (this.isDarkMode) {
      document.body.classList.add("dark-mode");
    }
  },
  methods: {
    generateOrderID() {
      let lastOrderID = parseInt(localStorage.getItem("lastOrderID")) || 100;
      lastOrderID = lastOrderID >= 999 ? 101 : lastOrderID + 1;
      localStorage.setItem("lastOrderID", lastOrderID);
      return lastOrderID;
    },
    loadOrderItems() {
      try {
        this.orderItems = JSON.parse(this.$route.query.items || "[]");
        this.addCategoriesToItems();
        this.estimatedTime = this.calculateEstimatedTime();
      } catch (error) {
        console.error("Error parsing order items:", error);
        this.orderItems = [];
      }
    },
    addCategoriesToItems() {
      this.orderItems.forEach((item) => {
        if (!item.category) {
          if (item.name.includes("Coffee")) item.category = "Hot Coffee";
          else if (item.name.includes("Juice")) item.category = "Juice Drinks";
          else if (item.name.includes("Milktea")) item.category = "Milktea";
          else if (item.name.includes("Frappe")) item.category = "Blended Frappes";
          else item.category = "Food";
        }
      });
    },
    calculateEstimatedTime() {
      let maxTime = 5;
      if (this.orderItems.length === 0) return maxTime;

      this.orderItems.forEach((item) => {
        if (item.category === "Hot Coffee" || item.category === "Juice Drinks") {
          maxTime = Math.max(maxTime, 7);
        } else if (item.category === "Ice Coffee" || item.category === "Chocolate Drinks") {
          maxTime = Math.max(maxTime, 8);
        } else if (item.category === "Milktea" || item.category === "Blended Frappes") {
          maxTime = Math.max(maxTime, 10);
        } else if (item.category === "Food") {
          maxTime = Math.max(maxTime, 10);
        }
      });

      return maxTime;
    },
    goBackToDashboard() {
      this.$router.push({ name: "Dashboard" });
    },
  },
};
</script>





<style scoped>

/* 🌙 Dark Mode - Dark Outer Background */
.dark-mode .order-id-page {
  background-color: #222 !important; /* Dark background */
  color: white !important; /* Light text for everything outside the boxes */
}

/* 🌙 Dark Mode - Keep Order ID Box Light */
.dark-mode .order-id {
  background: #f8d2e4 !important; /* Light pink background */
  color: black !important; /* Make text inside the box dark */
  border: 1px solid #ccc !important;
}

/* 🌙 Dark Mode - Keep Order Details Box Light */
.dark-mode .order-details li {
  background: #f8d2e4 !important; /* Light pink background */
  color: black !important; /* Dark text inside */
  border: 1px solid #ccc !important;
}

/* 🌙 Dark Mode - Keep Delivery Time Box Light */
.dark-mode .delivery-time {
  background: #ffebcd !important; /* Light yellow background */
  color: black !important; /* Make text inside the box dark */
  border: 1px solid #ccc !important;
}

.dark-mode h1,
.dark-mode h3,
.dark-mode h4,
.dark-mode .order-details h3,
.dark-mode .order-id-page h1,
.dark-mode .order-id-page h3,
.dark-mode .order-id-page h4 {
  color: white !important; /* Ensure all main texts are visible in dark mode */
}

/* 🌙 Dark Mode - Buttons */
.dark-mode .back-button {
  background-color: #444 !important; /* Dark button */
  color: white !important; /* Light text */
  border: 1px solid #666 !important;
}

.dark-mode .back-button:hover {
  background-color: #666 !important; /* Slightly lighter on hover */
}

/* 🌙 Dark Mode - Ensure Text Inside Boxes is Dark */
.dark-mode .order-id h2,
.dark-mode .order-details h3,
.dark-mode .order-details span,
.dark-mode .delivery-time h3 {
  color: black !important; /* Dark text inside the boxes */
}


/* Order ID Page */
.order-id-page {
  text-align: center;
  padding: 30px;
  background-color: #fff;
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 700px;
  margin: 0 auto; /* Centers the content */
}

/* Order ID Display */
.order-id {
  font-size: 28px;
  font-weight: bold;
  margin: 20px 0;
  background: #ffe4ec;
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Order Details */
.order-details {
  text-align: center;
  margin-bottom: 30px;
}

.order-details ul {
  list-style-type: none;
  padding: 0;
  font-size: 18px;
}

.order-details li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 12px 0;
  padding: 15px;
  background: #f8d2e4;
  border-radius: 10px;
  font-size: 18px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Delivery Time */
.delivery-time {
  font-size: 24px;
  font-weight: bold;
  background: #ffebcd;
  padding: 12px;
  border-radius: 10px;
  margin-bottom: 30px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Glowing effect for the "Back to Dashboard" button */
.back-button {
  padding: 12px 25px; /* Increased padding to fit the glowing effect */
  font-size: 16px; /* Adjusted font size */
  background-color: transparent;
  color: #FFF;
  border: none; /* Remove the border */
  cursor: pointer;
  position: relative;
  z-index: 0;
  border-radius: 5px;
  text-transform: uppercase;
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
  background-color: #d12f7a; /* Active background color */
  border-color: #d12f7a; /* Active border color (optional, can be removed too) */
}

/* Glow Animation */
@keyframes glowing {
  0% {background-position: 0 0;}
  50% {background-position: 400% 0;}
  100% {background-position: 0 0;}
}

/* 📱 Mobile Responsive Adjustments */
@media (max-width: 768px) {
  .order-id {
    font-size: 22px;
    padding: 10px;
  }

  .order-details li {
    flex-direction: column;
    font-size: 16px;
    padding: 14px;
    text-align: center;
  }

  .delivery-time {
    font-size: 20px;
    padding: 10px;
  }

  button {
    font-size: 14px;
    padding: 12px;
  }
}

/* Extra Small Screens (iPhone SE, very small phones) */
@media (max-width: 480px) {
  .order-id {
    font-size: 20px;
    padding: 8px;
  }

  .order-details li {
    font-size: 14px;
    padding: 10px;
  }

  .delivery-time {
    font-size: 18px;
  }

  button {
    font-size: 13px;
    padding: 10px;
    width: 100%;
  }
}
</style>
