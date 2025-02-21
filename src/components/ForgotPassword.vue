<template>
  <div class="forgot-password-page">
    <div class="form-container">
      <h1>Reset Password</h1>

      <form @submit.prevent="handleRequestReset">
        <div class="input-container">
          <input 
            type="email" 
            v-model="email" 
            placeholder="Enter your email" 
            required 
          />
        </div>
        
        <p v-if="successMessage" class="success">{{ successMessage }}</p>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
        
        <button type="submit">Request Reset</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: "",
      errorMessage: "",
      successMessage: ""
    };
  },
  methods: {
    async handleRequestReset() {
      try {
        const response = await fetch("http://127.0.0.1:8000/request-password-reset", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ email: this.email })
        });
        
        const data = await response.json();
        
        if (response.ok) {
          this.successMessage = "Password reset link sent to your email!";
          this.errorMessage = "";
        } else {
          this.errorMessage = data.detail || "An error occurred. Please try again.";
          this.successMessage = "";
        }
      } catch (error) {
        console.error("Error:", error);
        this.errorMessage = "An unexpected error occurred.";
        this.successMessage = "";
      }
    }
  }
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
  background-image: url("@/assets/Uicbackroundblur.png");
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
}

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
}

button {
  background-color: #ff69b4;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
}
</style>
