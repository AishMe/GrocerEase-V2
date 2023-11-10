<template>
  <section class="h-100 h-custom min-h-content">
    <div class="container py-5 h-100">
      <br /><br /><br />
      <div class="row d-flex justify-content-center align-items-center h-100">
        <div class="col">
          <div class="card border-0">
            <div class="card-body p-4 rounded-5" style="background-color: #f4f7f3">
              <h3 class="mb-4">My Orders</h3>
              <hr />

              <!-- Display orders here -->
              <div v-for="order in orders" :key="order.order_id" class="mb-4">
                <h5>Order #{{ order.order_id }}</h5>
                <p>Order Date: {{ formatDate(order.order_date) }}</p>
                <div v-for="category in order.categories" :key="category.category_name">
                  <h6>{{ category.category_name }}</h6>
                  <ul class="list-group">
                    <li
                      v-for="item in category.items"
                      :key="item.order_item_id"
                      class="list-group-item d-flex justify-content-between align-items-center"
                    >
                      {{ item.product_name }} - {{ item.quantity }} items
                      <span class="badge bg-primary rounded-pill">{{
                        formatCurrency(item.total_price)
                      }}</span>
                    </li>
                  </ul>
                </div>
              </div>

              <!-- Show a message if no orders are available -->
              <div v-if="orders.length === 0">
                <p>No orders available.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
  
  <script>
export default {
  data() {
    return {
      orders: [] // Fetch orders from the API
    }
  },
  methods: {
    // Fetch orders from the API
    async fetchOrders() {
      try {
        // Send a request to your Flask backend to get the user's orders
        // const response = await this.$axios.get('/api/orders')
        const response = await fetch('http://127.0.0.1:5000/api/orders', {
          method: 'GET',
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('accessToken')
          }
        })

        if (response.ok) {
          const responseData = await response.json()
          this.orders = responseData.orders
          console.log(this.orders)
        } else {
          alert('Oops! Something went wrong. Cannot fetch the orders.')
        }
      } catch (error) {
        console.error('Error fetching orders:', error)
        // Handle error, show a message, etc.
      }
    },
    // Format date to a readable format
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' }
      return new Date(dateString).toLocaleDateString(undefined, options)
    },
    // Format currency to a readable format
    formatCurrency(value) {
      return `$${value.toFixed(2)}`
    }
  },
  mounted() {
    // Fetch orders when the component is mounted
    this.fetchOrders()
  }
}
</script>
  <style>
/* Add custom styles if needed */
</style>
  