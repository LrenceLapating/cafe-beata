<template>
  <div class="create-account-page">
    <div class="form-container">
      <h1>Create Account</h1>

      <!-- Sign-Up Form -->
      <form @submit.prevent="handleSignUp" class="signup-form">
        <!-- Name Field -->
        <div class="input-container">
          <input 
            type="text" 
            v-model="name" 
            placeholder="Name" 
            required 
          />
        </div>

        <!-- Email Field -->
        <div class="input-container">
          <input 
            type="email" 
            v-model="email" 
            placeholder="E-mail" 
            required 
          />
        </div>

        <!-- Password Field -->
        <div class="input-container">
          <input 
            type="password" 
            v-model="password" 
            placeholder="Password" 
            required 
          />
        </div>

        <!-- Secret Question -->
        <div class="input-container">
          <label for="secretQuestion">Choose a secret question:</label>
          <select v-model="secretQuestion" required>
            <option value="What is your favorite food?">What is your favorite food?</option>
            <option value="What is the name of your pet?">What is the name of your pet?</option>
            <option value="What is your mother’s maiden name?">What is your mother’s maiden name?</option>
            <option value="What city were you born in?">What city were you born in?</option>
          </select>
        </div>

        <!-- Secret Answer -->
        <div class="input-container">
          <input 
            type="text" 
            v-model="secretAnswer" 
            placeholder="Answer to secret question" 
            required 
          />
        </div>

        <!-- Error Message -->
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

        <!-- Sign Up Button -->
        <button type="submit" class="sign-up-button">Sign Up</button>
      </form>

      <!-- Sign In Link -->
      <div class="sign-in-link">
        <p>Already have an account? <router-link to="/login" @click="goToLogin">Sign In</router-link></p>
      </div>
    </div>

    <!-- Success Popup -->
    <div v-if="showSuccessPopup" class="success-popup">
      <p>Successfully Created Account!</p>
      <button @click="closePopup">Close</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      name: "",
      email: "",
      password: "",
      secretQuestion: "What is your favorite food?",  // Default question
      secretAnswer: "",
      errorMessage: "",
      showSuccessPopup: false,
    };
  },
  methods: {
    async handleSignUp() {
      // Updated regex: allows any characters before the 12 digits
      const emailRegex = /^[a-zA-Z]+_\d{12}@uic\.edu\.ph$/;

      if (!emailRegex.test(this.email)) {
        this.errorMessage = "Email must be the UIC Email";
        return;
      }

      // Automatically set username from the name field
      const username = this.name.trim(); // Username will be the name the user enters

      try {
        const response = await fetch("http://127.0.0.1:8000/register", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: this.email,
            password: this.password,
            secret_answer: this.secretAnswer,  // Send the user's secret answer here
            username: username,  // Send the username
          }),
        });

        const data = await response.json();

        if (response.ok) {
          this.showSuccessPopup = true;
          // Store the name and email in localStorage or in a global state
          localStorage.setItem('userName', this.name);
          localStorage.setItem('userEmail', this.email);
          setTimeout(() => {
            this.$router.push({ name: "Login" });  // Redirect to Profile page
          }, 2000);
        } else {
          this.errorMessage = data.detail;
        }
      } catch (error) {
        console.error("Error during account creation:", error);
        this.errorMessage = "An error occurred. Please try again.";
      }
    },

    goToLogin() {
      this.$router.push({ name: "Login" });
    },
  },
};
</script>



<style scoped>
/* Styling for Create Account Page */
.create-account-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #ff9a9e, #fad0c4);
}

.form-container {
  background: rgba(255, 255, 255, 0.95);
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 0 20px rgba(255, 105, 180, 0.8);
  width: 100%;
  max-width: 400px;
  text-align: center;
  backdrop-filter: blur(10px);
}

h1 {
  font-size: 26px;
  color: #d63384;
  margin-bottom: 20px;
  font-weight: bold;
  text-shadow: 0 0 8px rgba(255, 105, 180, 0.6);
}

/* Input fields with glowing effect */
.input-container {
  margin-bottom: 20px;
}

input, select {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  border: 2px solid #ff69b4;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(255, 105, 180, 0.5);
  transition: all 0.3s ease;
  max-width: 320px; /* Adjust the max width for the inputs */
}

input:focus, select:focus {
  outline: none;
  border-color: #d63384;
  box-shadow: 0 0 15px rgba(255, 20, 147, 0.8);
}

/* Sign Up Button with glowing pink effect */
.sign-up-button {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  background: linear-gradient(135deg, #ff1493, #ff69b4);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  box-shadow: 0 0 15px rgba(255, 20, 147, 0.8);
  transition: all 0.3s ease;
  max-width: 320px;
}

.sign-up-button:hover {
  background: linear-gradient(135deg, #d63384, #ff1493);
  box-shadow: 0 0 20px rgba(255, 20, 147, 1);
}

/* Error message */
.error {
  color: red;
  font-size: 14px;
  margin-top: 10px;
}

/* Sign In Link */
.sign-in-link {
  margin-top: 20px;
  font-size: 14px;
}

.sign-in-link a {
  color: #ff1493;
  text-decoration: none;
  font-weight: bold;
}

.sign-in-link a:hover {
  text-decoration: underline;
  text-shadow: 0 0 5px rgba(255, 20, 147, 0.8);
}

/* Success Popup */
.success-popup {
  position: absolute;
  top: 20%;
  left: 50%;
  transform: translateX(-50%);
  padding: 20px;
  background-color: rgba(255, 0, 106, 0.7);
  color: white;
  border-radius: 10px;
  font-size: 18px;
  font-weight: bold;
  text-align: center;
}

.success-popup button {
  margin-top: 10px;
  padding: 10px 20px;
  background-color: #d63384;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

/* Mobile Responsive Adjustments */
@media (max-width: 768px) {
  .form-container {
    width: 85%;
    padding: 20px;
  }

  h1 {
    font-size: 24px;
  }

  input {
    font-size: 14px;
  }

  .sign-up-button {
    font-size: 14px;
    padding: 10px;
  }
}
</style>
