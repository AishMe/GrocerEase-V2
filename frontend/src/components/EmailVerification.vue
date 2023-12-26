<script setup>
import ConfettiExplosion from 'vue-confetti-explosion'
</script>

<template>
  <div class="min-vh-100 email-verification-container">
    <div class="email-verification-content">
      <ConfettiExplosion :duration="5000" class="text-center" />
      <h1 style="color: green">{{ message }}</h1>
      <hr />
      <button type="button" class="btn btn-primary fw-bold" @click="goToLogin">
        Go to Login Page
      </button>
    </div>
  </div>
</template>
  
  <script>
export default {
  data() {
    return {
      message: ''
    }
  },
  methods: {
    goToLogin() {
      this.$router.push('/login')
    }
  },
  mounted() {
    // Trigger confetti effect
  },
  created() {
    this.message = decodeURIComponent(this.$route.query.message || 'No Result. Please Try Again...')
  }
}
</script>

<style scoped>
.email-verification-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.email-verification-content {
  text-align: center;
  background-color: #fff;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}
</style>
