<template>
  <div class="min-vh-100 access-denied-container">
    <div class="access-denied-content">
      <h1>Access Denied</h1>
      <p>Sorry, you don't have permission to access this page.</p>
      <router-link v-if="role" to="/dashboard" class="back-button">Back to My Dashboard</router-link>
    </div>
  </div>
</template>
  
  <script>
export default {
  name: 'AccessDenied', 
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
  
  <style scoped>
.access-denied-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.access-denied-content {
  text-align: center;
  background-color: #fff;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

h1 {
  font-size: 2rem;
  color: #ff6347;
}

p {
  font-size: 1.2rem;
  color: #333;
  margin: 20px 0;
}

.back-button {
  display: inline-block;
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  text-decoration: none;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.back-button:hover {
  background-color: #0056b3;
}
</style>
  