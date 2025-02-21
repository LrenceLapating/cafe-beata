<template>
  <div class="profile-container">
    <div class="profile-card">
      <!-- Back Button -->
      <button @click="goToDashboard" class="back-to-dashboard-button">
        <i class="fa fa-arrow-left"></i> Back
      </button>

      <h2>PROFILE</h2>

      <!-- Avatar Selection -->
      <div class="avatar-container">
        <!-- Dynamically load the avatar URL -->
        <img :src="getAvatarUrl(user.avatar)" alt="Avatar" class="avatar-img" />
        <div class="avatar-picker">
        
          <input type="file" ref="fileInput" @change="uploadAvatar" style="display: none;" />
          <button @click="triggerFileInput">Upload Profile</button>
        </div>
      </div>

      <!-- Profile Edit Section -->
      <div v-if="isEditing">
        <div class="form-group">
          <label>Username:</label>
          <input v-model="user.username" type="text" disabled />
        </div>
        <div class="form-group">
          <label>E-mail:</label>
          <input v-model="user.email" type="email" disabled />
        </div>
        <div class="form-group">
          <label>Course:</label>
          <input v-model="user.course" type="text" />
        </div>
        <div class="form-group">
          <label>Gender:</label>
          <select v-model="user.gender">
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Other">Other</option>
          </select>
        </div>
        <button @click="saveChanges" class="save-button">Update Information</button>
        <button @click="cancelEdit" class="cancel-button">Cancel</button>
      </div>

      <div v-else>
        <div class="profile-info">
          <p><strong>Username:</strong> {{ user.username }}</p>
          <p><strong>E-mail:</strong> {{ user.email }}</p>
          <p><strong>Course:</strong> {{ user.course }}</p>
          <p><strong>Gender:</strong> {{ user.gender }}</p>
        </div>
        <button @click="toggleEdit" class="edit-button">Edit Profile</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      user: {
        avatar: '/assets/default.png', // Default avatar
        username: '',
        email: '',
        course: '',
        gender: '',
      },
      isEditing: false,
      isDarkMode: localStorage.getItem('darkMode') === 'true', // Load Dark Mode preference
    };
  },
  mounted() {
    const userEmail = localStorage.getItem('userEmail');
    if (userEmail) {
      this.user.email = userEmail;
      this.loadProfile(); // Load profile on mount
    }

    // ✅ Ensure dark mode is applied when page loads
    if (localStorage.getItem('darkMode') === 'true') {
      this.isDarkMode = true; 
      document.body.classList.add('dark-mode');
    }
  },
  methods: {
    // 🌓 Toggle Dark Mode and save preference
    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode;
      localStorage.setItem('darkMode', this.isDarkMode);

      // Apply or remove dark mode class
      if (this.isDarkMode) {
        document.body.classList.add('dark-mode');
      } else {
        document.body.classList.remove('dark-mode');
      }
    },

   getAvatarUrl(avatar) {
  return avatar ? `http://127.0.0.1:8000${avatar}` : '/assets/default.png';


    },

    toggleEdit() {
      this.isEditing = !this.isEditing;
    },

    async saveChanges() {
  try {
    const formData = new FormData();
    formData.append('username', this.user.username);
    formData.append('email', this.user.email);
    formData.append('course', this.user.course);
    formData.append('gender', this.user.gender);
    formData.append('avatar', this.user.avatar);

    const response = await fetch(`http://127.0.0.1:8000/profile/${this.user.email}`, {
      method: 'PUT',
      body: formData,
    });

    const data = await response.json();
    if (response.ok) {
      this.isEditing = false;
      alert('Profile updated successfully');
    } else {
      alert(data.detail);
    }
  } catch (error) {
    console.error('Error:', error);
    alert('An error occurred while saving your profile.');
      }
    },

    cancelEdit() {
      this.isEditing = false;
    },

    async loadProfile() {
  try {
    const response = await fetch(`http://127.0.0.1:8000/profile/${this.user.email}`);
    const data = await response.json();
    if (response.ok) {
      this.user = data;
      if (!this.user.avatar) {
        this.user.avatar = '/assets/default.png';
      }
    } else {
      alert(data.detail);
    }
  } catch (error) {
    console.error('Error:', error);
    alert('Failed to load profile.');

      }
    },

    uploadAvatar(event) {
  const file = event.target.files[0];
  if (file) {
    const formData = new FormData();
    formData.append("avatar", file);

    fetch(`http://127.0.0.1:8000/profile/upload-avatar/${this.user.email}`, {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.message === "Avatar uploaded successfully") {
          this.user.avatar = data.avatar_url || "/assets/default.png";
          this.saveChanges();
        } else {
          alert(data.detail || "Failed to upload avatar.");
        }
      })
      .catch((error) => {
        console.error("Error uploading avatar:", error);
        alert("An error occurred while uploading the avatar.");
          });
      }
    },

    triggerFileInput() {
      this.$refs.fileInput.click();
    },

    goToDashboard() {
      this.$router.push({ name: 'Dashboard' });
    },
  },
};
</script>



.dark-mode .profile-container {
  background-color: #222 !important; /* Dark background */
}

.dark-mode .profile-card {
  background-color: #333 !important; /* Dark profile card */
  color: white !important; /* Light text */
}

/* 🌙 Dark Mode - Text Adjustments */
.dark-mode h2,
.dark-mode label,
.dark-mode .profile-info p,
.dark-mode .about-me p {
  color: white !important; /* Ensure text is light */
}

/* 🌙 Dark Mode - Avatar Border */
.dark-mode .avatar-img {
  border: 3px solid white !important;
}

/* 🌙 Dark Mode - Input Fields */
.dark-mode input,
.dark-mode select,
.dark-mode textarea {
  background-color: #444 !important;
  color: white !important;
  border: 1px solid #666 !important;
}

/* 🌙 Dark Mode - Buttons */
.dark-mode button {
  background-color: #666 !important;
  color: white !important;
}

.dark-mode button:hover {
  background-color: #777 !important;
}

/* 🌙 Dark Mode - Profile Info Highlight */
.dark-mode .profile-info strong {
  color: #ffcc00 !important; /* Make the strong text more visible */
}


<style scoped> 
.profile-container {
  padding: 30px;
  background-color: #f9f9f9;
}

h2 {
  font-size: 28px;
  color: #333;
  text-align: center;
}

.profile-card {
  position: relative;  /* Ensure the button is positioned relative to this container */
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  margin: 20px auto;
}

/* Back Button */
.back-to-dashboard-button {
  background-color: transparent;
  color: #3498db;
  padding: 2px;
  font-size: 20px;
  border: none;
  cursor: pointer;
  border-radius: 20%;
  position: absolute;
  top: 10px;
  left: 0;  /* Ensure it is aligned with the left edge */
  z-index: 1;
}

.back-to-dashboard-button i {
  font-size: 20px;
}

.avatar-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
}

.avatar-img {
  width: 100px;
  height: 100px;
  border-radius: 50%; 
  border: 3px solid #ddd;
}

.upload-button,
.edit-button {
  padding: 8px 20px;
  font-size: 12px;
  background-color: transparent;
  color: #FFF;
  border: 2px solid #d12f7a;
  cursor: pointer;
  position: relative;
  z-index: 0;
  border-radius: 5px;
  text-transform: uppercase;
}

.upload-button::after,
.edit-button::after {
  content: "";
  z-index: -1;
  position: absolute;
  width: 100%;
  height: 100%;
  background-color: #333;
  left: 0;
  top: 0;
  border-radius: 10px;
}

.upload-button::before,
.edit-button::before {
  content: "";
  background: linear-gradient(
    45deg,
    #FF0000, #FF7300, #FFFB00, #48FF00,
    #00FFD5, #002BFF, #FF00C8, #FF0000
  );
  position: absolute;
  top: -2px;
  left: -2px;
  background-size: 600%;
  z-index: -1;
  width: calc(100% + 4px);
  height: calc(100% + 4px);
  filter: blur(8px);
  animation: glowing 20s linear infinite;
  transition: opacity .3s ease-in-out;
  border-radius: 10px;
  opacity: 0;
}

.upload-button:hover::before,
.edit-button:hover::before {
  opacity: 1;
}

.upload-button {
  background-color: #007bff;
  color: white;
  padding: 10px;
  font-size: 14px;
  border-radius: 5px;
  border: none;
  cursor: pointer;
}

.upload-button:hover {
  background-color: #0056b3;
}

.avatar-upload-input {
  display: none;
}

.form-group {
  margin-top: 15px;
}

label {
  font-size: 16px;
  color: #555;
}

input,
select,
textarea {
  margin-top: 5px;
  padding: 12px;
  font-size: 16px;
  width: 100%;
  border-radius: 6px;
  border: 1px solid #ccc;
}

textarea {
  resize: vertical;
}

button {
  margin-top: 1px;
  padding: 12px;
  font-size: 16px;
  background-color:rgb(53, 42, 47);
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  width: 100%;
}


button:hover {
  background-color:rgb(68, 63, 57);
}

.save-button,
.cancel-button {
  background-color:rgb(31, 32, 31);
}

.save-button:hover,
.cancel-button:hover {
  background-color:rgb(26, 27, 27);
}

.edit-button {
  background-color: #f1c40f;
}

.edit-button:hover {
  background-color: #f39c12;
}

.profile-info {
  margin-bottom: 20px;
}

.profile-info p {
  font-size: 18px;
  color: #333;
}

.profile-info strong {
  color: #007bff;
}

.about-me {
  margin-top: 30px;
  text-align: center;
}

.about-me p {
  font-size: 16px;
  color: #555;
}
</style>
