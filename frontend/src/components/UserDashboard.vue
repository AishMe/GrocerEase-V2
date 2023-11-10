<template>
  <div class="container min-h-content py-5 text-center">
    <div class="row py-lg-5 mb-5">
      <div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 g-3">
        <div class="col" v-for="product in products" :key="product.id">
          <div class="card shadow-sm">
            <img class="bd-placeholder-img card-img-top" width="100%" :src="product.image" alt="" />
            <div class="card-body">
              <p class="card-text">{{ product.name }}</p>
              <div class="d-flex justify-content-between align-items-center">
                <div class="btn-group">
                  <CartButton :product="product" />
                </div>
                <small class="text-muted"
                  ><i class="bi bi-currency-dollar"></i>{{ product.price }}</small
                >
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <br /><br />
  </div>
</template>

<script>
import CartButton from '../components/CartButton.vue'

export default {
  components: { CartButton },
  data() {
    return {
      products: []
    }
  },
  mounted() {
    this.fetchProducts()
  },
  methods: {
    async fetchProducts() {
      try {
        //const response = await this.$axios.get('/api/products');
        const response = await fetch('http://127.0.0.1:5000/api/products')
        if (response.ok) {
          const responseData = await response.json()
          this.products = responseData.products
          console.log(this.products)
        } else {
          alert('Oops! Something went wrong. Cannot fetch the products.')
        }
      } catch (error) {
        console.error('Error fetching products:', error)
      }
    }
  }
}
</script>