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

        <!-- Terms and Conditions with Checkbox -->
        <div class="terms-container">
          <input type="checkbox" v-model="agreeToTerms" id="termsCheckbox" required />
          <label for="termsCheckbox">
            By continuing, you agree to UIC Cafe Beàta's 
            <router-link to="/privacy-policy" class="terms-link">Privacy Policy</router-link>.
          </label>
        </div>

        <!-- Error Message -->
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

        <!-- Sign Up Button (Disabled Until Checkbox is Checked) -->
        <button type="submit" class="sign-up-button" :disabled="!agreeToTerms">Sign Up</button>
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
      secretQuestion: "What is your favorite food?",
      secretAnswer: "",
      errorMessage: "",
      showSuccessPopup: false,
      agreeToTerms: false, // Checkbox value
    };
  },
  methods: {
  async handleSignUp() {
    if (!this.agreeToTerms) {
      this.errorMessage = "You must agree to the Privacy Policy to continue.";
      return;
    }

    // Updated email regex
    const emailRegex = /^[a-zA-Z0-9]+(_\d{12})?@uic\.edu\.ph$/;


    if (!emailRegex.test(this.email)) {
      this.errorMessage = "Email must be a valid UIC Email.";
      return;
    }

    const username = this.name.trim();

    try {
      const response = await fetch("http://127.0.0.1:8000/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: this.email,
          password: this.password,
          secret_answer: this.secretAnswer,
          username: username,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        this.showSuccessPopup = true;
        localStorage.setItem('userName', this.name);
        localStorage.setItem('userEmail', this.email);
        setTimeout(() => {
          this.$router.push({ name: "Login" });
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

.terms-container {
  display: flex;
  align-items: center;
  font-size: 14px;
  margin-top: -10px; /* Adjust position slightly higher */
}

.terms-container input {
  margin-right: 4px;
  width: 14px;
  height: 14px;
}

.terms-link {
  color: #ff1493;
  text-decoration: none;
  font-weight: bold;
}

.terms-link:hover {
  text-decoration: underline;
}

/* Add more space below terms & conditions */
.terms-container {
  margin-bottom: 15px; /* Increase spacing between Terms and Sign In */
}

/* Disabled button style */
button:disabled {
  background: gray;
  cursor: not-allowed;
}

.create-account-page {
  background-image: url("@/assets/Uicbackroundblur.png"); /* Same as LoginPage.vue */
  background-size: cover;
  background-position: center;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
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
  width: 85%;
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