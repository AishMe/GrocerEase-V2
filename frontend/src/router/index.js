import { createRouter, createWebHistory } from 'vue-router'
import DefaultLayout from '../layouts/DefaultLayout.vue'
import LoginView from '../components/LoginView.vue'
import HomeView from '../components/HomeView.vue'
import ProfilePage from '../components/ProfilePage.vue'
import DashBoard from '../views/DashBoard.vue'
import FavouriteItems from '../components/FavouriteItems.vue'
import UserOrderedItems from '../components/UserOrderedItems.vue'
import RegisterView from '../components/RegisterView.vue'
import ShoppingCart from '../views/ShoppingCart.vue'
import OrdersView from '../views/OrdersView.vue'
import AccessDenied from '../views/AccessDenied.vue'
import AdminDashboard from '../components/AdminDashboard.vue'
import PendingRequests from '../components/PendingRequests.vue'
import ManagerAccepted from '../components/ManagerAccepted.vue'
import ManagerRejected from '../components/ManagerRejected.vue'
import HardDelete from '../components/HardDelete.vue'
import SummaryDashboard from '../components/SummaryDashboard.vue'

const routes = [
  {
    path:'/',
        name:'Public',
        component:DefaultLayout,
        redirect: '/',
        children:[
  { path: '/login', name: 'login', component: LoginView },
  { path: '/', name: 'home', component: HomeView },
  { path: '/profile', name: 'profile', component: ProfilePage, meta: {
    allowedRoles: ['user', 'admin', 'manager'],
  }, },
  { path: '/dashboard', name: 'dashboard', component: DashBoard, meta: {
    allowedRoles: ['user', 'admin', 'manager'],
  }, },
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
  { path: '/pending_requests', name: 'pending_requests', component: PendingRequests, meta: {
    allowedRoles: ['admin'],
  }, },
  { path: '/manager_accepted', name: 'manager_accepted', component: ManagerAccepted, meta: {
    allowedRoles: ['admin'],
  }, },
  { path: '/manager_rejected', name: 'manager_rejected', component: ManagerRejected, meta: {
    allowedRoles: ['admin'],
  }, },
  { path: '/summary_dashboard', name: 'summary_dashboard', component: SummaryDashboard, meta: {
    allowedRoles: ['admin', 'manager'],
  }, },
  { path: '/fav_items', name: 'fav_items', component: FavouriteItems, meta: {
    allowedRoles: ['user'],
  }, },
  { path: '/ordered_items', name: 'ordered_items', component: UserOrderedItems, meta: {
    allowedRoles: ['user'],
  }, },
  { path: '/hard_delete', name: 'hard_delete', component: HardDelete, meta: {
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
