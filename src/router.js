import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from './components/LoginPage.vue';
import DashboardPage from './components/DashboardPage.vue';
import ConfirmOrder from './components/ConfirmOrder.vue'; // Import the ConfirmOrder component
import OrderIDPage from './components/OrderIDPage.vue'; // Import the OrderIDPage component
import OrderHistory from './components/OrderHistory.vue'; // Import OrderHistory component
import OrderDetails from './components/OrderDetails.vue'; // Import OrderDetails component
import UserProfileCafe from './components/UserProfileCafe.vue'; // Import the renamed UserProfileCafe component
import CreateAccountPage from './components/CreateAccountPage.vue'; 
import ForgotPassword from '@/components/ForgotPassword.vue'; // Make sure the path is correct
import PrivacyAndPolicy from './components/PrivacyAndPolicy.vue'; // Import PrivacyAndPolicy component
import AdminPage from './components/AdminPage.vue'; 
import NotificationsPage from './components/NotificationsPage.vue';
import ChangePassword from './components/ChangePassword.vue';
import OrderRecord from './components/OrderRecord.vue';
import UserNotifications from './components/UserNotifications.vue';


const routes = [  

  {
    path: '/user-notifications',
    name: 'UserNotifications',
    component: UserNotifications,// Adjust path accordingly
  },

  
  {
    path: '/',
    redirect: '/login',  // Set this to redirect to login as default
  },

  {
    path: '/order-record',
    name: 'OrderRecord',
    component: OrderRecord,
  },
  

{
  path: '/reset-password/:token',
  name: 'reset-password',
  component: ChangePassword,
},
  {
    path: '/login',  // Explicitly set to /login for login page
    name: 'Login',
    component: LoginPage,
  },
  {
    path: '/forgot-password',
    name: 'ForgotPassword',
    component: ForgotPassword,
  },

  {
    path: '/notifications', // Route for Notifications Page
    name: 'Notifications',
    component: NotificationsPage, // Ensure you create NotificationsPage.vue
  },

  {
    path: '/admin', // This path is where the admin login will be handled
    name: 'AdminPage',
    component: AdminPage,
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
    props: route => ({
      orderId: route.query.orderId,
      date: route.query.date,
      billName: route.query.billName,
      total: route.query.total,
      items: JSON.parse(route.query.items || '[]'), // Ensure items are parsed as an array
    }),
  },
  {
    path: '/user-profile-cafe', // New path for the profile page
    name: 'UserProfileCafe',
    component: UserProfileCafe,  // Use the UserProfileCafe component
  },
  {
    path: '/privacy-policy', // New path for Privacy and Policy
    name: 'PrivacyPolicy',
    component: PrivacyAndPolicy,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,


});
  router.beforeEach((to, from, next) => {
    const publicPages = ["Login", "CreateAccount", "ForgotPassword", "PrivacyPolicy"];
  
    if (publicPages.includes(to.name)) {
      document.body.classList.remove("dark-mode"); // Ensure dark mode is removed on public pages
    }
  
    next();


});

export default router;
