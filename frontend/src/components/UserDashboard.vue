<template>
  <div>
    <!-- Toggle button for filter box -->
    <div class="fab">
      <a
        href="#"
        @click="toggleFilterBox"
        data-bs-toggle="tooltip"
        data-bs-placement="top"
        title="Filter"
      >
        <i class="bi bi-funnel-fill"></i>
      </a>
    </div>
    <div class="container min-h-content py-5 text-center">
      <h1 class="mb-3" style="font-size: 5rem; color: #c1e1c1">
        <strong>Products</strong>
      </h1>

      <!-- Filter box (hidden by default) -->
      <div
        v-show="showFilterBox"
        class="my-3 p-2"
        style="border: 2px solid #c1e1c1; border-radius: 10px"
      >
        <div class="d-flex align-items-center justify-content-center">
          <div class="mb-3 p-1">
            <label for="category" class="form-label text-white">Category</label>
            <select
              class="form-select"
              style="width: 300px"
              id="category"
              name="category"
              v-model="selectedCategory"
            >
              <option value="">All</option>
              <option
                v-for="category in categories"
                :key="category.category_id"
                :value="category.category_id"
              >
                {{ category.name }}
              </option>
            </select>
          </div>
          <div class="mb-3 p-1">
            <label for="min_rate" class="form-label text-white">Min Rate</label>
            <input
              type="number"
              style="width: 100px"
              class="form-control"
              min="0"
              max="10000"
              id="min_rate"
              name="min_rate"
              v-model="minRate"
            />
          </div>
          <div class="mb-3 p-1">
            <label for="max_rate" class="form-label text-white">Max Rate</label>
            <input
              type="number"
              style="width: 100px"
              class="form-control"
              min="0"
              max="10000"
              id="max_rate"
              name="max_rate"
              v-model="maxRate"
            />
          </div>
          <div class="mb-3 p-1">
            <label for="search" class="form-label text-white">Search</label>
            <input
              type="text"
              class="form-control"
              style="width: 300px"
              id="search"
              name="search"
              v-model="search"
              placeholder="Search by name..."
            />
          </div>
          <div class="mb-3 p-1">
            <button
              @click="toggleManufactureSorting"
              class="btn mt-4"
              style="background-color: #c1e1c1"
            >
              <i v-if="manufactureSortOrder === 'asc'" class="bi bi-sort-down-alt"></i>
              <i v-else class="bi bi-sort-down"></i>
            </button>
          </div>
          <div class="mb-3 p-1">
            <button @click="toggleNameSorting" class="btn mt-4" style="background-color: #c1e1c1">
              <i v-if="nameSortOrder === 'asc'" class="bi bi-sort-alpha-down"></i>
              <i v-else class="bi bi-sort-alpha-up"></i>
            </button>
          </div>
          <div class="mb-3 p-1">
            <button @click="resetFilters" class="btn mt-4" style="background-color: #c1e1c1">
              <i class="bi bi-arrow-counterclockwise"></i>
              Reset
            </button>
          </div>
        </div>
      </div>

      <div class="row row-cols-1 row-cols-md-4 g-4 mt-4">
        <div v-for="(product, index) in filteredProducts" :key="index" class="col">
          <div class="card shadow-sm">
            <img
              v-if="product.image === ''"
              class="bd-placeholder-img card-img-top"
              :src="`{{ url_for('assets', filename='FrontPageDesign.png') }}`"
              style="width: 100%; height: 14vw"
              alt="{{ product.name }} Image"
            />
            <img
              v-else
              class="bd-placeholder-img card-img-top"
              :src="product.image"
              style="width: 100%; height: 14vw"
              alt="{{ product.name }} Image"
            />
            <div class="card-body">
              <h4 class="card-title text-capitalize fw-bold text-black">{{ product.name }}</h4>
              <hr style="margin-top: 1rem; border: 1px solid black" />
              <h6 class="card-text fw-bold" :style="getStockMessageStyle(product.stock, product.manufacturing_date)">
                {{ getStockMessage(product) }}
              </h6>
              <p class="card-text">
                Manufacturing Date: {{ product.manufacturing_date }}<br />
                Rate per unit: Rs.{{ product.price }}/{{ product.unit }}<br />
                Stock: {{ product.stock }}
              </p>

              <div class="row align-items-center justify-content-center">
                <form @submit.prevent="addToCartOrPurchase(product)">
                  <div class="input-group">
                    <input type="hidden" name="product_id" value="{{ product.product_id }}" />
                    <input type="hidden" name="section_id" value="{{ product.section_id }}" />
                    <input
                      :disabled="product.stock === 0"
                      type="number"
                      class="form-control"
                      name="quantity"
                      placeholder="Qtn(kg)"
                      v-model="qty"
                      min="1"
                      required
                    />
                    <button
                      :disabled="product.stock === 0"
                      type="submit"
                      class="btn btn-outline-primary"
                      name="action"
                      value="cart"
                      data-product-id="{{ product.product_id }}"
                      data-section-id="{{ product.section_id }}"
                    >
                      <i class="bi bi-cart-fill"></i>
                    </button>
                    <button
                      :disabled="product.stock === 0"
                      type="submit"
                      class="btn btn-outline-success"
                      name="action"
                      value="purchase"
                      data-product-id="{{ product.product_id }}"
                      data-section-id="{{ product.section_id }}"
                    >
                      <i class="bi bi-basket2-fill"></i>
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

export default {
  data() {
    return {
      products: [],
      categories: [],
      showFilterBox: false,
      minRate: null,
      maxRate: null,
      selectedCategory: '',
      search: '',
      manufactureSortOrder: 'asc',
      nameSortOrder: 'asc'
    }
  },
  mounted() {
    this.fetchProducts()
    this.fetchCategories()
  },

  methods: {
    async fetchProducts() {
      try {
        // Fetch products from the API
        const response = await fetch('http://127.0.0.1:5000/api/products')

        if (response.ok) {
          const responseData = await response.json()
          this.products = responseData.products.map((product) => ({
            ...product,
            manufacturing_date: product.manufacturing_date || null,
            qty: this.qty || 1 // Set the initial quantity to 1
          }))
        } else {
          alert('Oops! Something went wrong. Cannot fetch the products.')
        }
      } catch (error) {
        console.error('Error fetching products:', error)
      }
    },
    async fetchCategories() {
      try {
        // Fetch products from the API
        const response = await fetch('http://127.0.0.1:5000/api/categories')

        if (response.ok) {
          const responseData = await response.json()
          this.categories = responseData.categories
        } else {
          alert('Oops! Something went wrong. Cannot fetch the categories.')
        }
      } catch (error) {
        console.error('Error fetching categories:', error)
      }
    },

    async addToCartOrPurchase(product) {
      const showToast = (message, type = 'info') => {
        toast[type](message)
      }
      console.log('Product Quantity:', this.qty)
      console.log('Product Stock:', product.stock)

      // Implement your logic for adding to cart
      if (this.qty > product.stock) {
        showToast(`Sorry, we have only ${product.stock} in stock.`, 'error')
      } else {
        // Implement your logic for adding to cart
        const existingCartItem = this.$store.state.cart.find((item) => item.id === product.id)

        if (existingCartItem) {
          // If the item is already in the cart, update the quantity
          this.$store.commit('updateCart', {
            product: { id: product.id, qty: this.qty }
          })
        } else {
          // If the item is not in the cart, add it
          this.$store.commit('addRemoveCart', {
            product: { ...product, qty: this.qty },
            toAdd: true
          })
        }

        // Show success toast
        showToast('Added to Cart', 'success')
      }
    },
    resetFilters() {
      this.selectedCategory = ''
      this.minRate = null
      this.maxRate = null
      this.search = ''
      this.nameSortOrder = 'asc'
      this.manufactureSortOrder = 'asc'
    },
    toggleFilterBox() {
      this.showFilterBox = !this.showFilterBox
    },
    toggleManufactureSorting() {
      this.manufactureSortOrder = this.manufactureSortOrder === 'asc' ? 'desc' : 'asc'
    },
    toggleNameSorting() {
      this.nameSortOrder = this.nameSortOrder === 'asc' ? 'desc' : 'asc'
    },
    getStockMessage(product) {
      if (product.stock === 0) {
        return 'Out of Stock'
      } else if (product.stock <= 10) {
        return 'HURRY! Limited Stock Available.'
      } else if (this.isNewProduct(product.manufacturing_date)) {
        return 'RECENTLY ADDED'
      } else {
        return 'In Stock'
      }
    },
    getStockMessageStyle(stock, manufacturingDate) {
      if (this.isNewProduct(manufacturingDate)) {
        return 'color: #4CAF50;' // Bright green -> fresh
      } else if (stock === 0) {
        return 'color: red;'
      } else if (stock <= 10) {
        return 'color: #FF9800;' // orange -> urgency
      } else {
        return 'color: darkblue;'
      }
    },
    isNewProduct(manufacturingDate) {
      // Compare the manufacturing date with the current date and check if it's within a week
      const manufacturingDateObject = new Date(manufacturingDate)
      const oneWeekAgo = new Date()
      oneWeekAgo.setDate(oneWeekAgo.getDate() - 7)
      return manufacturingDateObject > oneWeekAgo
    }
  },
  computed: {
    filteredProducts() {
      let filtered = this.products.filter((product) => {
        const meetsCategoryCriteria =
          !this.selectedCategory || product.category_id === this.selectedCategory
        const meetsMinRateCriteria = !this.minRate || product.price >= this.minRate
        const meetsMaxRateCriteria = !this.maxRate || product.price <= this.maxRate

        return meetsCategoryCriteria && meetsMinRateCriteria && meetsMaxRateCriteria
      })

      // Filter by search text
      if (this.search) {
        filtered = filtered.filter((product) =>
          product.name.toLowerCase().includes(this.search.toLowerCase())
        )
      }

      // Sorting
      if (this.manufactureSortOrder === 'asc') {
        filtered.sort((a, b) =>
          a.manufacturing_date > b.manufacturing_date
            ? 1
            : a.manufacturing_date < b.manufacturing_date
            ? -1
            : 0
        )
      } else {
        filtered.sort((a, b) =>
          a.manufacturing_date < b.manufacturing_date
            ? 1
            : a.manufacturing_date > b.manufacturing_date
            ? -1
            : 0
        )
      }

      if (this.nameSortOrder === 'asc') {
        filtered.sort((a, b) => a.name.localeCompare(b.name))
      } else {
        filtered.sort((a, b) => b.name.localeCompare(a.name))
      }

      return filtered
    }
  }
}
</script>

<style scoped>
.fab {
  width: 90px;
  height: 90px;
  background-color: #023020;
}
</style>
