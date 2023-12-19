<script setup>
import AppNavbar from './AppNavbar.vue'
import AppFooter from './AppFooter.vue'
</script>

<template>
  <div>
    <AppNavbar :role="role" v-show="!isHome || role"/>
    <router-view />
    <AppFooter v-show="!isHome || role"/>
  </div>
</template>

<script>
export default {
  components: { AppFooter, AppNavbar },
  data() {
    return {
      role: localStorage.getItem('role')
    }
  },
  computed: {
  isHome() {
     return this.$route.name === 'home'
  }
}
}
</script>
