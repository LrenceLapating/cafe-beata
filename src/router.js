import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from './components/LoginPage.vue';
import DashboardPage from './components/DashboardPage.vue';
import ConfirmOrder from './components/ConfirmOrder.vue'; // Import the ConfirmOrder component
import OrderIDPage from './components/OrderIDPage.vue'; // Import the OrderIDPage component
import OrderHistory from './components/OrderHistory.vue'; // Import OrderHistory component
import OrderDetails from './components/OrderDetails.vue'; // Import OrderDetails component
import UserProfileCafe from './components/UserProfileCafe.vue'; // Import the renamed UserProfileCafe component
import CreateAccountPage from './components/CreateAccountPage.vue'; 

const routes = [
  {
    path: '/',
    name: 'Login',
    component: LoginPage,
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardPage,
    beforeEnter: (to, from, next) => {
      if (localStorage.getItem('loggedIn') === 'true') {
        next();
      } else {
        next({ name: 'Login' });
      }
    },
  },
  {
    path: '/confirm-order',
    name: 'ConfirmOrder',
    component: ConfirmOrder,
    props: route => ({
      name: route.query.name,   // Pass name as a prop
      price: route.query.price, // Pass price as a prop
      image: route.query.image, // Pass image as a prop
    }),
  },
  {
    path: '/order-id',
    name: 'OrderIDPage',
    component: OrderIDPage,
    props: true,
  },

  {
    path: '/create-account',  // New route for creating an account
    name: 'CreateAccount',
    component: CreateAccountPage,
  },


  {
    path: '/order-history',
    name: 'OrderHistory',
    component: OrderHistory,
  },
  {
    path: '/order-details',
    name: 'OrderDetails',
    component: OrderDetails,
    props: true,
  },
  {
    path: '/user-profile-cafe', // New path for the profile page
    name: 'UserProfileCafe',
    component: UserProfileCafe,  // Use the UserProfileCafe component
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
