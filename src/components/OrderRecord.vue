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
          <div class="date-input-wrapper" @click="focusDateInput">
            <input 
              type="date" 
              :value="formatDateForInput(selectedDate)" 
              @input="handleDateChange"
              class="date-input"
              ref="dateInput"
            >
            <div class="calendar-icon">
              <img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNiIgaGVpZ2h0PSIxNiIgdmlld0JveD0iMCAwIDE2IDE2Ij48cGF0aCBmaWxsPSIjNjY2IiBkPSJNNSAyVjFoMnYxaDJ2MEg1ek0xMyAzdjEwSDNWM2gxMHpNMyAyYTEgMSAwIDAwLTEgMXYxMGExIDEgMCAwMDEgMWgxMGExIDEgMCAwMDEtMVYzYTEgMSAwIDAwLTEtMWgtMVYxYTEgMSAwIDAwLTEtMUg1YTEgMSAwIDAwLTEgMXYxSDNhMSAxIDAgMDAtMSAxeiIvPjwvc3ZnPg==" alt="calendar" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Search Bar -->
    <div class="search-container">
      <input
        v-model="searchQuery"
        @input="filterOrders"
        type="text"
        placeholder="Search by Order ID, Order Date, or Bill Name"
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
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="order in filteredOrders" :key="order.id">
          <td>{{ order.id }}</td>
          <td v-html="formatDate(order.created_at)"></td>
          <td>{{ order.customer_name }}</td>
          <td>
            <button @click="viewOrderDetails(order)" class="view-details-btn">View Details</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- No Orders Message -->
    <div v-else>
      <p>No matching orders found.</p>
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

    <!-- Order Details Modal -->
    <div class="modal" v-if="showOrderDetailsModal">
      <div class="modal-content order-details-modal">
        <span class="close" @click="showOrderDetailsModal = false">&times;</span>
        <h2>Order Details</h2>
        
        <div class="order-info" v-if="selectedOrder">
          <div class="order-header">
            <div class="order-header-item">
              <span class="label">Order ID:</span>
              <span class="value">{{ selectedOrder.id }}</span>
            </div>
            <div class="order-header-item">
              <span class="label">Customer:</span>
              <span class="value">{{ selectedOrder.customer_name }}</span>
            </div>
            <div class="order-header-item">
              <span class="label">Date:</span>
              <span class="value" v-html="formatDate(selectedOrder.created_at)"></span>
            </div>
          </div>
          
          <div class="order-items-list">
            <h3>Items</h3>
            <table class="items-table">
              <thead>
                <tr>
                  <th>Item</th>
                  <th>Quantity</th>
                  <th>Price</th>
                  <th>Subtotal</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, index) in selectedOrder.items" :key="index">
                  <td>{{ item.name }}</td>
                  <td>{{ item.quantity }}</td>
                  <td>₱{{ item.price.toFixed(2) }}</td>
                  <td>₱{{ (item.price * item.quantity).toFixed(2) }}</td>
                </tr>
              </tbody>
              <tfoot>
                <tr>
                  <td colspan="3" class="total-label">Total</td>
                  <td class="total-value">{{ calculateTotal(selectedOrder.items) }}</td>
                </tr>
              </tfoot>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  components: {
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
      },
      showOrderDetailsModal: false,
      selectedOrder: null
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
            // Sort orders by date (newest to oldest) before assigning
            const sortedOrders = data.orders.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
            this.orders = sortedOrders;
            this.filteredOrders = sortedOrders;
          } else {
            this.orders = [];
            this.filteredOrders = [];
            console.error("No orders found.");
          }
        })
        .catch(error => console.error("Error fetching orders:", error));
    },

    filterOrders() {
      if (this.searchQuery === '') {
        this.filteredOrders = this.orders;
      } else {
        const query = this.searchQuery.toLowerCase();
        this.filteredOrders = this.orders.filter(order => {
          return (
            order.id.toString().includes(query) || 
            order.customer_name.toLowerCase().includes(query) ||
            order.created_at.toLowerCase().includes(query)
          );
        }).sort((a, b) => {
          // Prioritize orders that start with the search query
          const aStartsWith = a.id.toString().startsWith(query) ? 1 : 0;
          const bStartsWith = b.id.toString().startsWith(query) ? 1 : 0;
          const aIncludes = a.id.toString().includes(query) ? 1 : 0;
          const bIncludes = b.id.toString().includes(query) ? 1 : 0;
          return (bStartsWith - aStartsWith) || (bIncludes - aIncludes) || (a.id - b.id);
        });
      }
    },

    // Method to format the order date
    formatDate(dateString) {
      const date = new Date(dateString);
      const month = (date.getMonth() + 1).toString().padStart(2, '0');
      const day = date.getDate().toString().padStart(2, '0');
      const year = date.getFullYear();
      const hours = date.getHours();
      const minutes = date.getMinutes().toString().padStart(2, '0');
      const period = hours >= 12 ? 'PM' : 'AM';
      const hour12 = (hours % 12 || 12).toString().padStart(2, '0');
      
      // Format date and time separately
      const datePart = `${month}-${day}-${year}`;
      const timePart = `${hour12}:${minutes} ${period}`;
      
      return `${datePart} <span class="highlighted-time">${timePart}</span>`;
    },

    formatDateForDisplay(date) {
      if (!date) return '';
      
      // Format date as MM-DD-YYYY
      const month = (date.getMonth() + 1).toString().padStart(2, '0');
      const day = date.getDate().toString().padStart(2, '0');
      const year = date.getFullYear();
      
      return `${month}-${day}-${year}`;
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

    focusDateInput() {
      this.$refs.dateInput.showPicker();
    },
    
    handleDateChange(event) {
      const newDate = new Date(event.target.value + 'T00:00:00');
      if (!isNaN(newDate.getTime())) {
        this.selectedDate = newDate;
        this.fetchSalesForDate();
      }
    },
    
    fetchSalesForDate() {
      const startOfDay = new Date(this.selectedDate);
      startOfDay.setHours(0, 0, 0, 0);
      
      const endOfDay = new Date(this.selectedDate);
      endOfDay.setHours(23, 59, 59, 999);
      
      // Filter completed orders for the selected date
      const ordersForDate = this.orders.filter(order => {
        const orderDate = new Date(order.created_at);
        return orderDate >= startOfDay && orderDate <= endOfDay;
      });
      
      // Calculate total sales
      let total = 0;
      ordersForDate.forEach(order => {
        const orderTotal = parseFloat(this.calculateTotal(order.items).substring(1));
        total += orderTotal;
      });
      
      // Update dailySales object
      this.dailySales = {
        total: total,
        orderCount: ordersForDate.length,
        orders: ordersForDate
      };
      
      this.showSalesModal = true;
    },
    
    formatDateYYYYMMDD(date) {
      const d = new Date(date);
      return `${d.getFullYear()}-${(d.getMonth() + 1).toString().padStart(2, '0')}-${d.getDate().toString().padStart(2, '0')}`;
    },
    
    formatDateMMDDYYYY(date) {
      const d = new Date(date);
      const month = (d.getMonth() + 1).toString().padStart(2, '0');
      const day = d.getDate().toString().padStart(2, '0');
      const year = d.getFullYear();
      return `${month}-${day}-${year}`;
    },

    // New method to view order details
    viewOrderDetails(order) {
      this.selectedOrder = order;
      this.showOrderDetailsModal = true;
    }
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
}

.calendar-container {
  display: flex;
  justify-content: center;
  margin: 15px 0;
}

.date-field {
  width: 200px;
  position: relative;
}

.date-input-wrapper {
  position: relative;
  width: 100%;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.date-input {
  width: 100%;
  padding: 4px 30px 4px 4px;
  border: 1px solid #ccc;
  border-radius: 0;
  font-size: 14px;
  cursor: pointer;
}

.calendar-icon {
  position: absolute;
  right: 5px;
  top: 50%;
  transform: translateY(-50%);
  pointer-events: none;
  display: flex;
  align-items: center;
}

.calendar-icon img {
  width: 16px;
  height: 16px;
  display: block;
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

.dark-mode .date-input {
  background-color: #2d2d2d;
  border-color: #444;
  color: #fff;
}

.dark-mode .calendar-icon img {
  filter: invert(1);
}

/* View Details Button Styles */
.view-details-btn {
  background-color: #d12f7a;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.view-details-btn:hover {
  background-color: #a82563;
}

/* Order Details Modal Styles */
.order-details-modal {
  max-width: 600px;
}

.order-header {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  margin-bottom: 20px;
  padding: 10px;
  background-color: #f8f8f8;
  border-radius: 5px;
}

.order-header-item {
  margin: 5px 10px;
}

.label {
  font-weight: bold;
  color: #666;
  margin-right: 5px;
}

.value {
  color: #d12f7a;
}

.order-items-list {
  margin-top: 20px;
}

.items-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.items-table th,
.items-table td {
  padding: 10px;
  border: 1px solid #ddd;
  text-align: left;
}

.items-table th {
  background-color: #f8d2e4;
  color: #d12f7a;
}

.total-label {
  text-align: right;
  font-weight: bold;
}

.total-value {
  font-weight: bold;
  color: #d12f7a;
}

/* Dark mode adjustments for order details */
.dark-mode .order-header {
  background-color: #3d3d3d;
}

.dark-mode .label {
  color: #bbb;
}

.dark-mode .value {
  color: #f8d2e4;
}

.dark-mode .items-table th {
  background-color: #444;
}

.dark-mode .items-table td {
  border-color: #444;
}

.dark-mode .total-value {
  color: #f8d2e4;
}

/* Add this at the end of your style section */
.highlighted-time {
  color: #d12f7a;
  font-weight: bold;
  background-color: #f8d2e4;
  padding: 2px 6px;
  border-radius: 4px;
  margin-left: 4px;
}

.dark-mode .highlighted-time {
  color: #f8d2e4;
}
</style>
