<template>
  <div id="app">
    <router-view></router-view> <!-- This is where the routed component will be displayed -->
  </div>
</template>

<script>
export default {
  data() {
    return {
      isDarkMode: localStorage.getItem('darkMode') === 'true' // Load saved Dark Mode state
    };
  },
  watch: {
    isDarkMode(newValue) {
      localStorage.setItem('darkMode', newValue); // Save to localStorage
      document.body.classList.toggle('dark-mode', newValue);
    }
  },
  created() {
    document.body.classList.toggle('dark-mode', this.isDarkMode);
  },
  methods: {
    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode;
    }
  }
};
</script>


<style>
.dark-mode {
  background-color: #121212;
  color: #ffffff;
}

/* Style Buttons in Dark Mode */
.dark-mode button {
  background-color: #333;
  color: #fff;
  border: 1px solid #555;
}

.dark-mode input {
  background-color: #222;
  color: #fff;
  border: 1px solid #555;
}

/* Sidebar & Time in Dark Mode */
.dark-mode .sidebar,
.dark-mode .sidebar-category h3,
.dark-mode .sidebar-category ul li {
  color: #ffffff;
}

.dark-mode .live-time {
  color: #ffffff;
}

</style>
