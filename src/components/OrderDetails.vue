<template>
  <div class="order-details">
    <h1>Order Details</h1>
    <div>
      <h3>Order ID: {{ orderId }}</h3>
      <h3>Order Date: {{ date }}</h3>
      <h3>Bill Name: {{ billName }}</h3>
      <h3>Total: ₱{{ total }}</h3>
    </div>
    <button @click="goBackToHistory" class="back-button">Back to Order History</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      orderId: this.$route.query.orderId,
      date: this.$route.query.date,
      billName: this.$route.query.billName,
      total: this.$route.query.total,
    };
  },
  methods: {
    goBackToHistory() {
      this.$router.push({ name: 'OrderHistory' });
    },
  },
};
</script>

<style scoped>
.order-details {
  padding: 20px;
  font-family: Arial, sans-serif;
}

h1 {
  font-size: 28px;
  color: #333;
}

h3 {
  font-size: 20px;
  color: #555;
}

/* Glowing effect for the "Back to Order History" button */
.back-button {
  padding: 8px 20px;  /* Smaller padding */
  font-size: 12px;     /* Smaller font size */
  background-color: transparent;
  color: #FFF;
  border: none;        /* Remove the border */
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
</style>
