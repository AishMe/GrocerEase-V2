<template>
  <div>
    <div class="row">
      <div class="card my-2 col-4" v-for="product in products" :key="product.id">
        <div class="card-body">
          <h5 class="card-title">Product Name : {{ product.title }}</h5>
          <h6 class="card-subtitle mb-2 text-body-secondary">
            Product Price : {{ product.price }}
          </h6>
          <input type="number" v-model.number="count[product.id]" />
          <button class="card-link my-3" @click="update_store(count[product.id], product.price)">
            Add to Cart
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      count: {}
    }
  },
  computed: {
    products() {
      return this.$store.getters.getProducts
    }
  },
  methods: {
    updateStore(count, price) {
      this.$store.commit('updateCount', count)
      this.$store.commit('updateTotal', { count, price })
    }
  }
}
</script>
