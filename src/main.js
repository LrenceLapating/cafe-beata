import { createApp } from 'vue';
import App from './App.vue';
import router from './router';  // Make sure you're using the correct router

createApp(App).use(router).mount('#app'); // Mounting the router here
