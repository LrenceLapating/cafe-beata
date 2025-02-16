<template>
  <div class="forgot-password-page">
    <div class="form-container">
      <h1>Change Password</h1>

      <!-- Forgot Password Form -->
      <form @submit.prevent="handleResetPassword" class="forgot-password-form">
        <!-- Email Field -->
        <div class="input-container">
          <input 
            type="email" 
            v-model="email" 
            placeholder="E-mail" 
            required 
          />
        </div>

        <!-- Secret Question Answer Field -->
        <div class="input-container">
          <input 
            type="text" 
            v-model="secretAnswer" 
            placeholder="Answer to secret question" 
            required 
          />
        </div>

        <!-- New Password Field -->
        <div class="input-container">
          <input 
            type="password" 
            v-model="newPassword" 
            placeholder="New Password" 
            required 
          />
        </div>

        <!-- Confirm Password Field -->
        <div class="input-container">
          <input 
            type="password" 
            v-model="confirmPassword" 
            placeholder="Confirm Password" 
            required 
          />
        </div>

        <!-- Error Message -->
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

        <!-- Success Message -->
        <p v-if="successMessage" class="success">{{ successMessage }}</p>

        <!-- Reset Password Button -->
        <button type="submit" class="reset-password-button">Reset Password</button>
      </form>

      <!-- Link to go back to Sign In -->
      <div class="back-to-signin">
        <p>Back to <router-link to="/login">Sign In</router-link></p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: "",
      secretAnswer: "",
      newPassword: "",
      confirmPassword: "",
      errorMessage: "",
      successMessage: "", // Store success message
    };
  },
  methods: {
    async handleResetPassword() {
      if (this.newPassword !== this.confirmPassword) {
        this.errorMessage = "Passwords do not match";
        return;
      }

      try {
        const response = await fetch("http://127.0.0.1:8000/reset-password", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: this.email,
            secret_answer: this.secretAnswer.trim().toLowerCase(),
            newPassword: this.newPassword,
          }),
        });

        const data = await response.json();

        if (response.ok) {
          this.successMessage = "Password change successful! Redirecting...";
          this.errorMessage = ""; // Clear error message

          // Redirect after 3 seconds
          setTimeout(() => {
            this.$router.push({ name: "Login" });
          }, 3000);
        } else {
          this.errorMessage = data.detail || "An error occurred. Please try again.";
          this.successMessage = ""; // Clear success message
        }
      } catch (error) {
        console.error("Error during password reset:", error);
        this.errorMessage = "An unexpected error occurred. Please try again.";
        this.successMessage = ""; // Clear success message
      }
    },
  },
};
</script>


<style scoped>
/* Styling for Forgot Password Page */



.success {
  color: green;
  font-size: 14px;
  margin-top: 10px;
}

.forgot-password-page {
  background-image: url("@/assets/Uicbackroundblur.png"); /* Same as LoginPage.vue */
  background-size: cover;
  background-position: center;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  
}

.form-container {
  background: rgba(255, 255, 255, 0.95);
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 0 20px rgba(255, 105, 180, 0.8);
  width: 85%;
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

input {
  width: 85%;
  padding: 12px;
  font-size: 16px;
  border: 2px solid #ff69b4;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(255, 105, 180, 0.5);
  transition: all 0.3s ease;
  max-width: 320px; /* Adjust the max width for the inputs */
}

input:focus {
  outline: none;
  border-color: #d63384;
  box-shadow: 0 0 15px rgba(255, 20, 147, 0.8);
}

/* Reset Password Button with glowing pink effect */
.reset-password-button {
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

.reset-password-button:hover {
  background: linear-gradient(135deg, #d63384, #ff1493);
  box-shadow: 0 0 20px rgba(255, 20, 147, 1);
}

/* Error message */
.error {
  color: red;
  font-size: 14px;
  margin-top: 10px;
}

/* Back to Sign In Link */
.back-to-signin {
  margin-top: 20px;
  font-size: 14px;
}

.back-to-signin a {
  color: #ff1493;
  text-decoration: none;
  font-weight: bold;
}

.back-to-signin a:hover {
  text-decoration: underline;
  text-shadow: 0 0 5px rgba(255, 20, 147, 0.8);
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

  .reset-password-button {
    font-size: 14px;
    padding: 10px;
  }
}
</style>
