import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../components/LoginView.vue'
import HomeView from '../components/HomeView.vue'
import ProtectedPage from '../components/ProtectedPage.vue'

const routes = [
  { path: '/login', name: 'login', component: LoginView },
  { path: '/home', name: 'home', component: HomeView },
  { path: '/prot', name: 'prot', component: ProtectedPage },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
