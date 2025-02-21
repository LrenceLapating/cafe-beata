<template>
  <div id="app">
    <router-view></router-view> <!-- This is where the routed component will be displayed -->
  </div>
</template>

<script>
export default {
  data() {
    return {
      isDarkMode: localStorage.getItem("darkMode") === "true" && localStorage.getItem("loggedIn") === "true", 
    };
  },
  watch: {
    isDarkMode(newValue) {
      localStorage.setItem("darkMode", newValue); // Save preference
      document.body.classList.toggle("dark-mode", newValue);
    }
  },
  created() {
    // Check if the user is logged in before applying dark mode
    const isLoggedIn = localStorage.getItem("loggedIn") === "true";
    if (this.isDarkMode && isLoggedIn) {
      document.body.classList.add("dark-mode");
    } else {
      document.body.classList.remove("dark-mode"); // Ensure light mode on public pages
    }
  },
  methods: {
    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode;
    }
  }
};
</script>

<style>
/* Default Light Mode */
body {
  background-color: #ffffff;
  color: #000000;
}

/* 🌙 Dark Mode */
.dark-mode {
  background-color: #121212;
  color: #ffffff;
}

/* 🌙 Dark Mode - Buttons */
.dark-mode button {
  background-color: #333;
  color: #fff;
  border: 1px solid #555;
}

/* 🌙 Dark Mode - Input Fields */
.dark-mode input {
  background-color: #222;
  color: #fff;
  border: 1px solid #555;
}

/* 🌙 Dark Mode - Sidebar & Time */
.dark-mode .sidebar,
.dark-mode .sidebar-category h3,
.dark-mode .sidebar-category ul li {
  color: #ffffff;
}

.dark-mode .live-time {
  color: #ffffff;
}
</style>