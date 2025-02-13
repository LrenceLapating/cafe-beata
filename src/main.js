import { createApp } from 'vue';
import App from './App.vue';
import router from './router';  // Import router.js

const app = createApp(App);

app.use(router);  // Make sure the router is used
app.mount('#app');
