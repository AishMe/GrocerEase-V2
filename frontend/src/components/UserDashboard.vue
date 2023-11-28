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
              placeholder="Search by product name..."
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
              <h6
                class="card-text fw-bold"
                :style="getStockMessageStyle(product.stock, product.manufacturing_date)"
              >
                {{ getStockMessage(product) }}
              </h6>
              <p class="card-text">
                Manufacturing Date: {{ product.manufacturing_date }}<br />
                Rate per unit: Rs.{{ product.price }}/{{ product.unit }}<br />
                Stock: {{ product.stock }}
              </p>

              <div class="row align-items-center justify-content-center">
                <form>
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
                      @click.prevent="addToCart(product)"
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
                      @click.prevent="showCheckoutForm(product)"
                      class="btn btn-outline-success"
                      name="action"
                      value="purchase"
                      data-product-id="{{ product.product_id }}"
                      data-section-id="{{ product.section_id }}"
                    >
                    <i class="bi bi-basket2-fill"></i>
                  </button>
                    <button
                      :disabled="product.stock === 0"
                      @click.prevent="showCheckoutForm(product)"
                      class="btn btn-outline-danger"
                      name="action"
                      value="purchase"
                      data-product-id="{{ product.product_id }}"
                      data-section-id="{{ product.section_id }}"
                    >
                      <i class="bi bi-heart-fill"></i>
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- Checkout form -->
    <div v-if="showCheckoutFormBool" class="form-container">
      <div class="form card">
        <div class="card-header">
          <h5 class="mb-0">Payment Options</h5>
        </div>
        <form @submit.prevent="checkout(selectedProduct)">
          <div class="card-body">
            <!-- Payment options radio buttons -->
            <div class="form-check">
              <input
                class="form-check-input"
                type="radio"
                name="paymentOption"
                id="creditCardRadio"
                value="creditCard"
                v-model="selectedPaymentOption"
              />
              <label class="form-check-label" for="creditCardRadio"> Credit Card </label>
            </div>
            <div class="form-check">
              <input
                class="form-check-input"
                type="radio"
                name="paymentOption"
                id="debitCardRadio"
                value="debitCard"
                v-model="selectedPaymentOption"
                required
              />
              <label class="form-check-label" for="debitCardRadio"> Debit Card </label>
            </div>
            <div class="form-check">
              <input
                class="form-check-input"
                type="radio"
                name="paymentOption"
                id="googlePayRadio"
                value="googlePay"
                v-model="selectedPaymentOption"
                required
              />
              <label class="form-check-label" for="googlePayRadio"> Google Pay </label>
            </div>
            <br />

            <!-- Credit/Debit Card Fields -->
            <div
              v-if="selectedPaymentOption === 'creditCard' || selectedPaymentOption === 'debitCard'"
            >
              <div class="mb-3">
                <label for="cardName" class="form-label">Name on Card</label>
                <input type="text" class="form-control" id="cardName" v-model="cardName" required />
              </div>
              <div class="mb-3">
                <label for="cardNumber" class="form-label"
                  >{{
                    selectedPaymentOption === 'creditCard' ? 'Credit Card' : 'Debit Card'
                  }}
                  Number</label
                >
                <input
                  type="number"
                  class="form-control"
                  id="cardNumber"
                  v-model="cardNumber"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="cardExpiration" class="form-label">Expiration</label>
                <input
                  type="text"
                  class="form-control"
                  id="cardExpiration"
                  v-model="cardExpiration"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="cVV" class="form-label">CVV</label>
                <input type="number" class="form-control" id="cVV" v-model="cVV" required />
              </div>
            </div>

            <!-- Google Pay Field -->
            <div v-if="selectedPaymentOption === 'googlePay'">
              <div class="mb-3">
                <label for="upiId" class="form-label">UPI ID</label>
                <input type="text" class="form-control" id="upiId" v-model="upiId" required />
              </div>
            </div>

            <!-- Checkout and Cancel Buttons -->
            <div class="d-flex justify-content-between">
              <button type="submit" class="btn btn-success">Checkout</button>
              <button @click.prevent="cancelCheckout" class="btn btn-secondary">Cancel</button>
            </div>
          </div>
        </form>
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
      nameSortOrder: 'asc',

      showCheckoutFormBool: false,
      selectedProduct: null,
      selectedPaymentOption: null,
      cardName: '',
      cardNumber: '',
      cardExpiration: '',
      cVV: '',
      upiId: ''
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

    async addToCart(product) {
      const showToast = (message, type = 'info') => {
        toast[type](message)
      }
      console.log('Product Quantity:', this.qty)
      console.log('Product Stock:', product.stock)

      // Implement your logic for adding to cart
      if (this.qty > product.stock) {
        showToast(`Sorry, we have only ${product.stock} in stock.`, 'error')
      } else if (this.qty === undefined) {
        showToast('Please specify the quantity.', 'error')
      } else if (this.qty < 0) {
        showToast('Please specify a valid quantity.', 'error')
      }  else if (this.qty > 0) { 

      try {
        const response = await fetch('http://127.0.0.1:5000/api/add_to_cart', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + localStorage.getItem('accessToken')
          },
          body: JSON.stringify({
            product_id: product.id,
            quantity: 1 // You can modify this based on user input
          })
        });

        if (response.ok) {
          const responseData = await response.json();
          // Show a success message to the user
          toast.success(responseData.message);
        } else {
          const errorData = await response.json();
          // Show an error message to the user
          toast.error(errorData.message);
        }
      } catch (error) {
        console.error('Error adding to cart:', error);
      }
    }},
    async checkout(product) {
      const showToast = (message, type = 'info') => {
        toast[type](message)
      }
      // Create the cart array based on the provided format
      const cartItem = {
        ...product,
        qty: this.qty
      }

      const cart = [cartItem]

      const confirmCheckout = window.confirm('Are you sure you want to buy this product?')

      if (confirmCheckout) {
        await fetch('http://127.0.0.1:5000/api/checkout', {
          method: 'POST',
          headers: {
            'Content-type': 'application/json',
            Authorization: 'Bearer ' + localStorage.getItem('accessToken')
          },
          body: JSON.stringify({ cart: cart })
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error('Checkout failed')
            }
            return response.json()
          })
          .then((data) => {
            // Handle successful checkout
            console.log('Checkout successful:', data.message)
            window.location.reload()
            showToast(
              `Checkout Successful! You bought ${this.qty} ${product.unit}s of ${product.name}.`,
              'success'
            )
            console.log('Selected Payment Option:', this.selectedPaymentOption)
          })
          .catch((error) => {
            // Handle checkout failure
            console.error('Error during checkout:', error)
          })
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
    },
    // Cancel checkout
    cancelCheckout() {
      this.showCheckoutFormBool = false
      // Reset form fields or take other necessary actions
      this.selectedPaymentOption = null
      this.cardName = ''
      // Reset other credit/debit card fields similarly
      this.upiId = ''
    },
    showCheckoutForm(product) {
      const showToast = (message, type = 'info') => {
        toast[type](message)
      }
      if (this.qty === undefined) {
        showToast('Please specify the quantity.', 'error')
      } else if (this.qty < 0) {
        showToast('Please specify a valid quantity.', 'error')
      } else if (this.qty > product.stock) {
        showToast(`Sorry, we have only ${product.stock} in stock.`, 'error')
      } else if (this.qty > 0) {
        this.selectedProduct = product
        this.showCheckoutFormBool = true
      }
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
.form-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(50px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.form {
  width: 400px;
  background-color: #fff;
  border-radius: 10px;
  overflow: hidden;
}
</style>
