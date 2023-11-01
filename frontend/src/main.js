import './assets/main.css'
import 'bootstrap'
import "bootstrap/dist/css/bootstrap.min.css"
import * as bootstrap from 'bootstrap'
import "bootstrap-icons/font/bootstrap-icons.css"
import 'fa-icons'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from "./store"
import { createHead } from '@vueuse/head'

const head = createHead()
createApp(App).use(head).use(router).use(store).use(bootstrap).mount('#app')
