<script setup>
import UserNavbar from '../components/UserNavbar.vue'
import AdminNavbar from '../components/AdminNavbar.vue'
import AppFooter from '../components/AppFooter.vue'
</script>

<template>
    <div>
        <UserNavbar v-if="role === 'user'"/>
        <AdminNavbar v-if="role === 'admin'"/>
         <router-view/>
        <AppFooter/>
    </div>
</template>

<script>
export default {
    components:{UserNavbar, AppFooter, AdminNavbar},
  data() {
    return {
      role: localStorage.getItem('role')
    }
  },
  async mounted() {
    const res = await fetch('http://127.0.0.1:5000/profile', {
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
      //alert(d.message)
      this.$router.push({ path: '/login' })
      console.log(d.msg)
    }
  }
}

</script>
