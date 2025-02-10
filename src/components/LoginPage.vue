<template>
  <div class="login-page">
    <div class="login-container">
      <div class="logo-container">
        <img src="@/assets/uic-logo.png" alt="University Logo" class="logo" />
      </div>
      <h1 class="title">University of the Immaculate Conception</h1>
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="input-container">
          <label for="username"></label>
          <input 
            type="text" 
            v-model="username" 
            id="username" 
            placeholder="Uic Email" 
            required 
          />
        </div>
        <div class="input-container">
          <label for="password"></label>
          <input 
            type="password" 
            v-model="password" 
            id="password" 
            placeholder="Password" 
            required 
          />
        </div>
        <button type="submit" class="login-button">Login</button>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      </form>
      <p class="create-account-link">
        Don't have an account? <router-link to="/create-account">Create one</router-link>
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "LoginPage",
  data() {
    return {
      username: "",
      password: "",
      errorMessage: "", // To store error messages
    };
  },
  methods: {
    handleLogin() {
      // Check for valid email format
      const isValidEmail = this.username.endsWith("@uic.edu.ph");

      // Dummy password for now
      const validPassword = "123"; // Replace this with your actual backend validation

      console.log(`Username: ${this.username}, Password: ${this.password}`);
      console.log(`Is valid email: ${isValidEmail}`);

      if (isValidEmail && this.password === validPassword) {
        // Save login session to localStorage
        localStorage.setItem("loggedIn", "true"); // Store user login status

        // Debugging: Check if router.push() is triggered
        console.log("Login successful, redirecting to dashboard");

        // Redirect to dashboard page after successful login
        this.$router.push({ name: 'Dashboard' });
      } else {
        // Show error message if login fails
        if (!isValidEmail) {
          this.errorMessage = "Invalid Uic Email";
        } else {
          this.errorMessage = "Invalid password. Please try again.";
        }
      }
    },
  },
};
</script>

<style scoped>
/* Main background image for the login page */

.login-page {
  background-image: url("@/assets/Uicbackround.png"); /* Background image path */
  background-size: cover;
  background-position: center;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px; /* Prevents content from touching screen edges */
}

/* Login Container */
.login-container {
  background: rgba(255, 255, 255, 0.9); /* Slightly more opaque for better contrast */
  padding: 30px;
  border-radius: 12px;
  width: 90%;
  max-width: 400px;
  text-align: center;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); /* Adds subtle shadow */
}

/* Logo */
.logo {
  width: 60%;
  max-width: 220px;
  height: auto;
  margin-bottom: 20px;
}

/* Title */
.title {
  font-family: "Arial", sans-serif;
  color: #d12f7a;
  font-size: 24px;
  margin-bottom: 15px;
  font-weight: bold;
  text-shadow: 0 0 8px rgba(255, 105, 180, 0.6);
}

/* Input Fields */
.input-container {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 15px;
}

input {
  width: 100%;
  max-width: 320px;
  padding: 12px;
  margin-top: 5px;
  border: 2px solid #ff1493;
  border-radius: 8px;
  text-align: center;
  font-size: 16px;
  transition: all 0.3s ease;
}

/* Glowing effect when focused */
input:focus {
  outline: none;
  border-color: #ff1493; /* Pink border when focused */
  box-shadow: 0 0 15px rgba(255, 20, 147, 0.8); /* Glowing pink effect */
}

/* Button with glowing effect */
button {
  width: 78%;
  background-color: #d12f7a;
  color: white;
  padding: 12px;
  font-size: 16px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: background 0.3s;
  max-width: 320px;
}

button:hover {
  background-color: #b82d67;
}

/* Glowing effect for the "Login" button */
button {
  width: 100%; /* Ensures it aligns with the input fields */
  max-width: 320px;
  background: linear-gradient(135deg, #ff1493, #ff69b4);
  color: white;
  border: none;
  padding: 12px;
  font-size: 16px;
  border-radius: 15px;
  cursor: pointer;
  box-shadow: 0 0 15px rgba(255, 20, 147, 0.8);
  transition: all 0.3s ease;
}

button:hover {
  background: linear-gradient(135deg, #d63384, #ff1493);
  box-shadow: 0 0 20px rgba(255, 20, 147, 1);
}

/* Error message */
.error {
  color: red;
  font-size: 14px;
  margin-top: 10px;
}

/* Create Account Link */
.create-account-link {
  margin-top: 20px;
  font-size: 14px;
}

.create-account-link a {
  color: #ff1493;
  text-decoration: none;
  font-weight: bold;
}

.create-account-link a:hover {
  text-decoration: underline;
  text-shadow: 0 0 5px rgba(255, 20, 147, 0.8);
}

/* 📱 Mobile Responsive Adjustments */
@media (max-width: 768px) {
  .logo {
    width: 50%;
    max-width: 180px;
  }

  .title {
    font-size: 22px;
  }

  .login-container {
    width: 85%;
    padding: 20px;
  }

  input {
    font-size: 14px;
  }

  button {
    font-size: 14px;
  }
}

/* Extra Small Screens (iPhone SE, very small phones) */
@media (max-width: 480px) {
  .logo {
    width: 45%;
    max-width: 150px;
  }

  .title {
    font-size: 20px;
  }

  .login-container {
    width: 90%;
    padding: 15px;
  }

  input {
    font-size: 14px;
    padding: 10px;
  }

  button {
    font-size: 14px;
    padding: 10px;
  }
}
</style>
