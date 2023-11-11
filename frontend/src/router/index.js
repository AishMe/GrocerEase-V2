import { createRouter, createWebHistory } from 'vue-router'
import DefaultLayout from '../layouts/DefaultLayout.vue'
import LoginView from '../components/LoginView.vue'
import HomeView from '../components/HomeView.vue'
import ProfilePage from '../components/ProfilePage.vue'
import DashBoard from '../views/DashBoard.vue'
import RegisterView from '../components/RegisterView.vue'
import ShoppingCart from '../views/ShoppingCart.vue'
import OrdersView from '../views/OrdersView.vue'
import AccessDenied from '../views/AccessDenied.vue'
import AdminDashboard from '../components/AdminDashboard.vue'
import ManagerPending from '../components/ManagerPending.vue'
import ManagerAccepted from '../components/ManagerAccepted.vue'
import ManagerRejected from '../components/ManagerRejected.vue'

const routes = [
  {
    path:'/home',
        name:'Public',
        component:DefaultLayout,
        redirect: '/home',
        children:[
  { path: '/login', name: 'login', component: LoginView },
  { path: '/home', name: 'home', component: HomeView },
  { path: '/profile', name: 'profile', component: ProfilePage },
  { path: '/dashboard', name: 'dashboard', component: DashBoard },
  { path: '/register', name: 'register', component: RegisterView },
  { path: '/cart', name: 'cart', component: ShoppingCart, meta: {
    allowedRoles: ['user'],
  }, },
  { path: '/orders', name: 'orders', component: OrdersView, meta: {
    allowedRoles: ['user'],
  }, },
  { path: '/access_denied', name: 'access_denied', component: AccessDenied },
  { path: '/admin_dashboard', name: 'admin_dashboard', component: AdminDashboard, meta: {
    allowedRoles: ['admin'],
  }, },
  { path: '/manager_pending', name: 'manager_pending', component: ManagerPending, meta: {
    allowedRoles: ['admin'],
  }, },
  { path: '/manager_accepted', name: 'manager_accepted', component: ManagerAccepted, meta: {
    allowedRoles: ['admin'],
  }, },
  { path: '/manager_rejected', name: 'manager_rejected', component: ManagerRejected, meta: {
    allowedRoles: ['admin'],
  }, },

]
  }]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Define a navigation guard
router.beforeEach((to, from, next) => {
  const userRole = localStorage.getItem('role');

  // Define the route meta fields indicating which roles are allowed
  const allowedRoles = to.meta.allowedRoles;

  // Check if the user's role is allowed for the current route
  if (!allowedRoles || allowedRoles.includes(userRole)) {
    next();

  } else {
    next({ name: 'access_denied' });
  }

});


export default router
