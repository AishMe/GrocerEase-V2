<script setup>
import UserDashboard from '../components/UserDashboard.vue'
import ManagerDashboard from '../components/ManagerDashboard.vue'
import AdminDashboard from '../components/AdminDashboard.vue'
</script>

<template>
  <main>
    <UserDashboard v-if="role === 'user'" />
    <ManagerDashboard v-else-if="role === 'manager'" />
    <AdminDashboard v-else-if="role === 'admin'" />
  </main>
</template>

<script>
export default {
  data() {
    return {
      role: localStorage.getItem('role')
    }
  },
  methods: {
    async logout() {
      localStorage.removeItem('accessToken')
      localStorage.removeItem('role')
      this.$router.push({ path: '/' }).then(() => {
        this.$router.go()
      })
      alert('User Session Expired. Please Login Again.')
    },
  },
  async mounted() {
    const res = await fetch('http://127.0.0.1:5000/api/user/profile', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + localStorage.getItem('accessToken')
      }
    })

    const d = await res.json()
    if (res.ok) {
      console.log(d)
    } else {
      this.logout()
      console.log(d.msg)
    }
  }
}
</script>
