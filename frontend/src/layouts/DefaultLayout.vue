<script setup>
import AppNavbar from './AppNavbar.vue'
import AppFooter from './AppFooter.vue'
</script>

<template>
  <div>
    <AppNavbar />
    <router-view />
    <AppFooter v-if="role !== undefined" />
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
  async mounted() {
    if (this.role === undefined) {
      this.$router.push({ path: '/login' })
    }
  }
}
</script>
