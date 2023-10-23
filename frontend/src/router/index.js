import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../components/LoginView.vue'
import HomeView from '../components/HomeView.vue'
import ProfilePage from '../components/ProfilePage.vue'
import DashBoard from '../views/DashBoard.vue'
import RegisterView from '../components/RegisterView.vue'

const routes = [
  { path: '/login', name: 'login', component: LoginView },
  { path: '/home', name: 'home', component: HomeView },
  { path: '/profile', name: 'profile', component: ProfilePage },
  { path: '/dashboard', name: 'dashboard', component: DashBoard },
  { path: '/register', name: 'register', component: RegisterView }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
