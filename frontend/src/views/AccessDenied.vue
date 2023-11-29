<template>
  <div class="access-denied-container">
    <div class="access-denied-content">
      <h1>Access Denied</h1>
      <p>Sorry, you don't have permission to access this page.</p>
      <router-link to="/dashboard" class="back-button">Back to My Dashboard</router-link>
    </div>
  </div>
</template>
  
  <script>
export default {
  name: 'AccessDenied'
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
  color: #ff6347; /* Tomato Red */
}

p {
  font-size: 1.2rem;
  color: #333;
  margin: 20px 0;
}

.back-button {
  display: inline-block;
  padding: 10px 20px;
  background-color: #007bff; /* Blue */
  color: #fff;
  text-decoration: none;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.back-button:hover {
  background-color: #0056b3; /* Darker Blue */
}
</style>
  