<template>
  <div class="order-record">
    <div class="header">
      <button @click="goBack" class="back-button">← Back to Notifications</button>
    </div>
    
    <div :class="{ 'dark-mode': isDarkMode }">
      <h1>Order Record</h1>
    </div>

    <!-- Calendar Section -->
    <div class="calendar-section">
      <h2>Sales by Date</h2>
      <div class="calendar-container">
        <div class="date-field">
          <label for="date-picker">Sales date</label>
          <div class="date-input-container">
            <Datepicker
              v-model="selectedDate"
              @update:model-value="fetchSalesForDate"
              :enable-time-picker="false"
              class="custom-datepicker clickable-datepicker"
              :format="formatDateYYYYMMDD"
              :input-class-name="'date-input'"
            />
            <button class="calendar-button" @click="openDatepicker">
              <img src="data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24'%3E%3Cpath fill='%23000' d='M20 3h-1V1h-2v2H7V1H5v2H4c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 18H4V8h16v13z'/%3E%3C/svg%3E" 
                alt="calendar" 
                width="16" 
                height="16"
              />
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Sales Modal -->
    <div class="modal" v-if="showSalesModal">
      <div class="modal-content">
        <span class="close" @click="showSalesModal = false">&times;</span>
        <h2>Sales Summary for {{ formatDateForDisplay(selectedDate) }}</h2>
        <div class="sales-info">
          <div class="sales-card">
            <h3>Total Sales</h3>
            <p class="sales-amount">₱{{ dailySales.total.toFixed(2) }}</p>
          </div>
          <div class="sales-card">
            <h3>Orders Completed</h3>
            <p class="sales-count">{{ dailySales.orderCount }}</p>
          </div>
        </div>
        
        <div class="sales-details" v-if="dailySales.orderCount > 0">
          <h3>Order Details</h3>
          <table class="sales-table">
            <thead>
              <tr>
                <th>Order ID</th>
                <th>Customer</th>
                <th>Items</th>
                <th>Amount</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="order in dailySales.orders" :key="order.id">
                <td>{{ order.id }}</td>
                <td>{{ order.customer_name }}</td>
                <td>{{ formatItems(order.items) }}</td>
                <td>₱{{ calculateTotal(order.items).substring(1) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div class="no-sales" v-else>
          <p>No sales recorded for this date.</p>
        </div>
      </div>
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
          <td>{{ formatDate(order.created_at) }}</td> <!-- Format Order Date -->
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
import Datepicker from 'vue3-datepicker'

export default {
  components: {
    Datepicker
  },
  data() {
    return {
      isDarkMode: localStorage.getItem('darkMode') === 'true',
      orders: [],
      filteredOrders: [], // This will store filtered results
      searchQuery: "", // Search input field
      selectedDate: new Date(), // Default to today
      showSalesModal: false,
      dailySales: {
        total: 0,
        orderCount: 0,
        orders: []
      }
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
            this.filteredOrders = data.orders.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
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
      }).sort((a, b) => {
        const aStartsWith = a.id.toString().startsWith(query) ? 1 : 0;
        const bStartsWith = b.id.toString().startsWith(query) ? 1 : 0;
        const aIncludes = a.id.toString().includes(query) ? 1 : 0;
        const bIncludes = b.id.toString().includes(query) ? 1 : 0;
        return (bStartsWith - aStartsWith) || (bIncludes - aIncludes) || (a.id - b.id);
      });
    },

    // Method to format the order date
    formatDate(dateString) {
      const date = new Date(dateString);
      const hours = date.getHours();
      const minutes = date.getMinutes();
      const seconds = date.getSeconds();
      const period = hours >= 12 ? 'PM' : 'AM';
      const formattedDate = `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')} ${period}${(hours % 12 || 12)}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
      return formattedDate;
    },

    formatDateForDisplay(date) {
      if (!date) return '';
      return date.toLocaleDateString('en-US', { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
      });
    },

    formatDateForInput(date) {
      if (!date) return '';
      const d = new Date(date);
      return d.toISOString().split('T')[0];
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

    fetchSalesForDate() {
      // Reset sales data
      this.dailySales = {
        total: 0,
        orderCount: 0,
        orders: []
      };

      // Format date to YYYY-MM-DD for comparison
      const selectedDateStr = this.formatDateYYYYMMDD(this.selectedDate);
      
      // Filter orders for the selected date
      const ordersOnDate = this.orders.filter(order => {
        const orderDate = this.formatDateYYYYMMDD(new Date(order.created_at));
        return orderDate === selectedDateStr;
      });
      
      // Calculate total sales
      let totalSales = 0;
      ordersOnDate.forEach(order => {
        const orderTotal = order.items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        totalSales += orderTotal;
      });
      
      // Update daily sales data
      this.dailySales = {
        total: totalSales,
        orderCount: ordersOnDate.length,
        orders: ordersOnDate
      };
      
      // Show the modal
      this.showSalesModal = true;
    },
    
    formatDateYYYYMMDD(date) {
      const d = new Date(date);
      return `${d.getFullYear()}-${(d.getMonth() + 1).toString().padStart(2, '0')}-${d.getDate().toString().padStart(2, '0')}`;
    },
    
    openDatepicker() {
      document.querySelector('.custom-datepicker').click();
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

h2 {
  color: #d12f7a;
  font-size: 22px;
  margin-bottom: 15px;
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

/* Calendar Section Styles */
.calendar-section {
  margin: 20px 0;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.calendar-container {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 15px 0;
}

.date-field {
  width: 280px;
}

.date-field label {
  display: block;
  margin-bottom: 4px;
  font-size: 13px;
  color: #000;
}

.date-input-container {
  position: relative;
  display: inline-flex;
  align-items: center;
}

.custom-datepicker {
  width: 150px;
}

.clickable-datepicker {
  cursor: pointer;
}

:deep(.date-input) {
  padding: 2px 4px;
  border: 1px solid #ccc;
  border-radius: 2px;
  font-size: 13px;
  cursor: pointer;
  width: 150px;
  background: white;
}

:deep(.dp__input_icon) {
  display: none !important;
}

.calendar-button {
  position: absolute;
  right: -24px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.calendar-button img {
  width: 16px;
  height: 16px;
}

/* Hide the default calendar icon */
:deep(.dp__input_wrap) {
  width: 100%;
}

:deep(.dp__main) {
  width: max-content;
}

:deep(.dp__input_icon) {
  display: none;
}

/* Dark mode adjustments for new elements */
.dark-mode .calendar-section {
  background-color: #3d3d3d;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.dark-mode .date-field label {
  color: #ddd;
}

.dark-mode .custom-datepicker {
  background-color: #333;
  color: #fff;
  border-color: #555;
}

.dark-mode .custom-datepicker:hover {
  border-color: #777;
}

.dark-mode .custom-datepicker:focus {
  border-color: #3e9eff;
  box-shadow: 0 0 0 3px rgba(62, 158, 255, 0.2);
}

/* Modal Styles */
.modal {
  position: fixed;
  z-index: 1000;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  background-color: #fefefe;
  margin: auto;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  width: 80%;
  max-width: 800px;
  max-height: 80vh;
  overflow-y: auto;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
  cursor: pointer;
}

.close:hover,
.close:focus {
  color: #d12f7a;
  text-decoration: none;
}

/* Sales Info Styles */
.sales-info {
  display: flex;
  justify-content: space-around;
  margin: 20px 0;
}

.sales-card {
  background-color: #f8f8f8;
  border-radius: 8px;
  padding: 15px;
  width: 45%;
  text-align: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.sales-amount {
  font-size: 28px;
  font-weight: bold;
  color: #d12f7a;
  margin: 10px 0;
}

.sales-count {
  font-size: 28px;
  font-weight: bold;
  color: #5a67d8;
  margin: 10px 0;
}

.sales-details {
  margin-top: 20px;
}

.sales-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.sales-table th,
.sales-table td {
  padding: 10px;
  border: 1px solid #ddd;
  text-align: left;
}

.sales-table th {
  background-color: #f8d2e4;
  color: #d12f7a;
}

.no-sales {
  text-align: center;
  padding: 20px;
  color: #666;
}

/* Dark mode adjustments for new elements */
.dark-mode .calendar-section {
  background-color: #3d3d3d;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.dark-mode .modal-content {
  background-color: #2d2d2d;
  color: #fff;
}

.dark-mode .sales-card {
  background-color: #3d3d3d;
}

.dark-mode .close {
  color: #ddd;
}

.dark-mode .close:hover,
.dark-mode .close:focus {
  color: #f8d2e4;
}

.dark-mode .sales-table th {
  background-color: #444;
}

.dark-mode .sales-table td {
  border-color: #444;
}

.dark-mode .no-sales {
  color: #bbb;
}
</style>
