<template>
  <div class="order-record">
    <div class="header">
      <button @click="goBack" class="back-button">← Back to Notifications</button>
    </div>
    
    <div :class="{ 'dark-mode': isDarkMode }">
      <h1>Order Record</h1>
    </div>

    <!-- Search Bar -->
    <div class="search-container">
      <input
        v-model="searchQuery"
        @input="filterOrders"
        type="text"
        placeholder="Search by Order ID, Customer Name, or Item"
        class="search-bar"
      />
    </div>

    <!-- Display Orders only when orders array is available -->
    <table class="order-table" v-if="filteredOrders.length">
      <thead>
        <tr>
          <th>Order No. (ID)</th>
          <th>Order Date</th>
          <th>Bill Name</th>
          <th>Total</th>
          <th>Item Details</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="order in filteredOrders" :key="order.id">
          <td>{{ order.id }}</td>
          <td>{{ order.created_at }}</td>
          <td>{{ order.customer_name }}</td>
          <td>{{ calculateTotal(order.items) }}</td>
          <td>
            <span v-if="order.items.length">
              {{ formatItems(order.items) }}
            </span>
            <span v-else>No items found</span>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- No Orders Message -->
    <div v-else>
      <p>No matching orders found.</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isDarkMode: localStorage.getItem('darkMode') === 'true',
      orders: [],
      filteredOrders: [], // This will store filtered results
      searchQuery: "", // Search input field
    };
  },
  methods: {
    goBack() {
      this.$router.push({ name: "Notifications" });
    },

   fetchOrders() {
  fetch("http://127.0.0.1:8000/orders?status=completed") // Fetch only completed orders
    .then(response => response.json())
    .then(data => {
      console.log("Fetched orders:", data); // Debugging
      if (data.orders) {
        this.orders = data.orders;
        this.filteredOrders = data.orders;
      } else {
        this.orders = [];
        this.filteredOrders = [];
        console.error("No orders found.");
      }
    })
    .catch(error => console.error("Error fetching orders:", error));
    },

    filterOrders() {
      const query = this.searchQuery.toLowerCase();

      this.filteredOrders = this.orders.filter((order) => {
        return (
          order.id.toString().includes(query) || // Match Order ID
          order.customer_name.toLowerCase().includes(query) || // Match Customer Name
          order.items.some(item => item.name.toLowerCase().includes(query)) // Match Items
        );
      });
    },

    formatItems(items) {
      if (!Array.isArray(items)) {
        console.error("Invalid item format:", items);
        return "Invalid item data";
      }
      return items.map((item) => `${item.name} x${item.quantity}`).join(", ");
    },

    calculateTotal(items) {
      if (!Array.isArray(items)) return "₱0";
      return "₱" + items.reduce((sum, item) => sum + item.price * item.quantity, 0).toFixed(2);
    },
  },
  mounted() {
    this.fetchOrders();
  },
  watch: {
    isDarkMode(newValue) {
      document.body.classList.toggle('dark-mode', newValue);
    },
  },
};
</script>

<style scoped>
.order-record {
  padding: 20px;
}

h1 {
  color: #d12f7a;
  font-size: 28px;
  margin-bottom: 20px;
}

.search-container {
  margin-bottom: 15px;
  text-align: center;
}

.search-bar {
  width: 50%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #d12f7a;
  border-radius: 5px;
  outline: none;
}

.order-table {
  width: 100%;
  border-collapse: collapse;
}

.order-table th,
.order-table td {
  padding: 10px;
  border: 1px solid #ddd;
  text-align: center;
}

.order-table th {
  background-color: #f8d2e4;
  color: #d12f7a;
}

.back-button {
  background-color: #f8d2e4;
  border: none;
  padding: 8px 15px;
  border-radius: 5px;
  cursor: pointer;
}

.back-button:hover {
  background-color: #d12f7a;
}

.dark-mode {
  background-color: #2d2d2d;
  color: #fff;
}
</style>
