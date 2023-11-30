<template>
  <div class="container min-vh-100">
    <br />
    <h1 class="mb-5 text-center" style="font-size: 5rem; color: #c1e1c1">
      <strong>Orders</strong>
    </h1>
    <hr />
    <div v-if="isLoading">
      <div
        v-for="(order, index) in orders"
        :key="order.order_id"
        class="card mb-4 shadow-lg rounded"
      >
        <div class="card-header">
          <h4>Order Number: {{ index + 1 }}</h4>
        </div>
        <div class="card-body">
          <table class="table table-bordered">
            <thead>
              <tr>
                <th>Product</th>
                <th>Category</th>
                <th>Quantity</th>
                <th>Total Price</th>
              </tr>
            </thead>
            <tbody>
              <template v-for="category in order.categories" :key="category.category_name">
                <tr v-for="item in category.items" :key="item.order_item_id">
                  <template v-if="category.items.length > 1">
                    <td>{{ item.product_name }}</td>
                    <td>{{ category.name }}</td>
                    <td>{{ item.quantity }}</td>
                    <td>{{ item.total_price }}</td>
                  </template>
                  <template v-else>
                    <td>{{ item.product_name }}</td>
                    <td>{{ category.category_name }}</td>
                    <td>{{ category.items[0].quantity }}</td>
                    <td>{{ category.items[0].total_price }}</td>
                  </template>
                </tr>
              </template>
            </tbody>
          </table>
        </div>
        <div class="card-footer">
          <strong
            >Total Cost:
            {{
              Math.round(
                order.categories.reduce(
                  (acc, category) =>
                    acc + category.items.reduce((acc, item) => acc + item.total_price, 0),
                  0
                )
              )
            }}</strong
          >
        </div>
      </div>
    </div>

    <div v-if="orders.length === 0">
      <p>No orders available.</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isLoading: false,
      orders: [] // Fetch orders from the API
    }
  },
  methods: {
    // Fetch orders from the API
    async fetchOrders() {
      try {
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
          this.isLoading = true
        } else {
          alert('Oops! Something went wrong. Cannot fetch the orders.')
        }
      } catch (error) {
        console.error('Error fetching orders:', error)
        // Handle error, show a message, etc.
      }
    }
  },
  mounted() {
    // Fetch orders when the component is mounted
    this.fetchOrders().then(() => {
      // Sort orders by order_id in ascending order
      this.orders.sort((a, b) => a.order_id - b.order_id)
    })
  }
}
</script>

