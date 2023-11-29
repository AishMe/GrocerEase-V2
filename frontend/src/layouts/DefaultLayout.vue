<script setup>
import AppNavbar from './AppNavbar.vue'
import AppFooter from './AppFooter.vue'
</script>

<template>
  <div>
    <AppNavbar :role="role" />
    <router-view />
    <AppFooter :role="role" />
  </div>
</template>

<script>
export default {
  components: { AppFooter, AppNavbar },
  data() {
    return {
      role: localStorage.getItem('role')
    }
  }
}
</script>
