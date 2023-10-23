<script setup>
import UserDashboard from '../components/UserDashboard.vue'
import ManagerDashboard from '../components/ManagerDashboard.vue'
import AdminDashboard from '../components/AdminDashboard.vue'
</script>

<template>
  <main>
    <UserDashboard v-if="role === 'user'"/>
    <ManagerDashboard v-else-if="role === 'manager'"/>
    <AdminDashboard v-else-if="role === 'admin'"/>
  </main>
</template>

<script>
export default {
  data() {
    return {
      name: '',
      user: '',
      role: localStorage.getItem('role')
    }
  },
  async mounted() {
    const res = await fetch('http://127.0.0.1:5000/protected', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + localStorage.getItem('accessToken')
      }
    })

    const d = await res.json()
    if (res.ok) {
      console.log(d)
      this.name = d.name
    } else {
      //alert(d.message)
      this.$router.push({ path: '/login' })
      console.log(d.msg)
    }
  }
}
</script>
