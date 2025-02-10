<template>
  <div class="profile-container">
    <!-- User Profile Content -->
    <div class="profile-card">
      <!-- Back to Dashboard Icon -->
      <button @click="goToDashboard" class="back-to-dashboard-button">
        <i class="fa fa-arrow-left"></i> <!-- FontAwesome arrow icon -->
      </button>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">

      <h2>PROFILE</h2>

      <!-- Avatar and Upload Picture -->
      <div class="avatar-container">
        <img :src="user.avatar" alt="Avatar" class="avatar-img" />
        <input type="file" ref="fileInput" @change="uploadAvatar" class="avatar-upload-input" />
        <button @click="triggerFileInput" class="upload-button">Upload Picture</button>
      </div>

      <!-- Profile Edit Section -->
      <div v-if="isEditing">
        <div class="form-group">
          <label>Username:</label>
          <input v-model="user.username" type="text" />
        </div>
        <div class="form-group">
          <label>E-mail:</label>
          <input v-model="user.email" type="email" />
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
        <div class="form-group">
          <label>About Me:</label>
          <textarea v-model="user.aboutMe" rows="4"></textarea>
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
          <p><strong>About Me:</strong> {{ user.aboutMe }}</p>
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
        avatar: '/path/to/avatar.png',  // Default avatar path
        username: 'Asenkrekmanov',
        email: 'azkrekmanov@gmail.com',
        course: 'UV/UX Design',
        gender: 'Male',
        aboutMe: 'I am Asen Krekmakov and I am dedicated UV/UX Designer from Sofia, Bulgaria.',
      },
      isEditing: false,  // Whether the user is editing the profile
    };
  },
  methods: {
    // Toggle edit mode
    toggleEdit() {
      this.isEditing = !this.isEditing;
    },

    // Save the changes
    saveChanges() {
      // Handle saving updated profile info
      console.log('Profile updated:', this.user);
      this.isEditing = false;  // Exit edit mode after saving changes
    },

    // Cancel editing and revert to previous values
    cancelEdit() {
      this.isEditing = false;
    },

    // Handle Avatar Upload
    uploadAvatar(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = () => {
          this.user.avatar = reader.result;  // Update avatar image
        };
        reader.readAsDataURL(file);  // Convert image to base64
      }
    },

    // Trigger file input for avatar upload
    triggerFileInput() {
      this.$refs.fileInput.click();  // Trigger file input click event
    },

    // Navigate back to the Dashboard
    goToDashboard() {
      this.$router.push({ name: 'Dashboard' });  // Redirect to the Dashboard page
    },
  },
};
</script>

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
  position: relative;
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  margin: 20px auto;
}

.back-to-dashboard-button {
  background-color: transparent;
  color: #3498db;
  padding: 2px;  /* Smaller padding */
  font-size: 20px;  /* Smaller icon size */
  border: none;
  cursor: pointer;
  border-radius: 10%;
  position: absolute;
  top: 10px;  /* Position the icon within the container */
  right: 300px;  /* Position the icon within the container */
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
  border-radius: 50%; /* Circular Avatar */
  border: 3px solid #ddd;
}

/* Glowing effect for the Upload Picture and Edit Profile buttons */
.upload-button,
.edit-button {
  padding: 8px 20px;  /* Reduced padding */
  font-size: 12px;     /* Reduced font size */
  background-color: transparent;
  color: #FFF;
  border: 2px solid #d12f7a; /* Adjust border color */
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

/* Animation for glowing */
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

/* Hover effect for glowing */
.upload-button:hover::before,
.edit-button:hover::before {
  opacity: 1;
}

/* Active button state */
.upload-button:active:after,
.edit-button:active:after {
  background: transparent;
}

.upload-button:active,
.edit-button:active {
  color: #000;
  font-weight: bold;
  background-color: #d12f7a; /* Active background color */
  border-color: #d12f7a; /* Border color */
}

/* Glow Animation */
@keyframes glowing {
  0% {background-position: 0 0;}
  50% {background-position: 400% 0;}
  100% {background-position: 0 0;}
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
  background-color: #d12f7a;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  width: 100%;
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
