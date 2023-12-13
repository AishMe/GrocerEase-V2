<template>
  <div class="min-vh-100" style="padding-top: 100px">
    <div v-if="isLoading" class="container min-h-content py-5 text-center">
      <h1 class="mb-3" style="font-size: 5rem; color: #c1e1c1">
        <strong>My Favourites</strong>
      </h1>

      <div class="row row-cols-1 row-cols-md-4 g-4 mt-4">
        <div v-for="(product, index) in products" :key="index" class="col">
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
              <h6 class="card-text fw-bold" :style="getStockMessageStyle(product)">
                {{ getStockMessage(product) }}
              </h6>
              <p class="card-text">
                Manufacturing Date: {{ product.manufacturing_date }}<br />
                Rate per unit: Rs.{{ product.price }}/{{ product.unit }}<br />
                Stock: {{ product.stock }}
              </p>

              <div class="d-flex flex-column align-items-center">
                <!-- Quantity input and heart button with spacing -->
                <div class="mb-2 input-group" v-if="product.product_status">
                  <input
                    :disabled="product.stock === 0"
                    type="number"
                    class="form-control"
                    name="quantity"
                    :placeholder="product.unit"
                    v-model="qty"
                    min="1"
                  />
                  <button
                    @click.prevent="removeFromFavorites(product.id)"
                    class="btn btn-outline-danger ms-2"
                    name="action"
                    value="purchase"
                  >
                    <i class="bi bi-trash-fill"></i>
                  </button>
                </div>

                <div class="mb-1 d-grid" v-if="!product.product_status">
                  <button
                    @click.prevent="removeFromFavorites(product.id)"
                    class="btn btn-danger ms-2"
                    name="action"
                    value="purchase"
                  >
                    Remove from Favourites
                  </button>
                </div>

                <!-- Buy Now and Add to Cart buttons with the same width as Quantity + Heart -->
                <div class="d-grid gap-2" v-if="product.product_status">
                  <button
                    :disabled="product.stock === 0"
                    @click.prevent="showCheckoutForm(product)"
                    class="btn btn-success"
                    style="padding: 8px 100px"
                    name="action"
                    value="purchase"
                    data-product-id="{{ product.product_id }}"
                    data-section-id="{{ product.section_id }}"
                  >
                    Buy Now
                  </button>

                  <button
                    :disabled="product.stock === 0"
                    @click.prevent="addToCart(product)"
                    class="btn btn-primary w-100"
                    style="padding: 8px"
                    name="action"
                    value="cart"
                    data-product-id="{{ product.product_id }}"
                    data-section-id="{{ product.section_id }}"
                  >
                    Add to Cart
                  </button>
                </div>
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
      isLoading: false,
      products: [],
      categories: [],

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
        const response = await fetch('http://127.0.0.1:5000/api/favourites', {
          method: 'GET',
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('accessToken')
          }
        })

        if (response.ok) {
          const responseData = await response.json()
          this.products = responseData.fav_products.map((product) => ({
            ...product,
            manufacturing_date: product.manufacturing_date || null,
            qty: this.qty || 1 // Set the initial quantity to 1
          }))
          this.isLoading = true
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
      console.log('Product Quantity:', this.qty)
      console.log('Product Stock:', product.stock)

      // Implement your logic for adding to cart
      if (this.qty > product.stock) {
        toast.danger(`Sorry, we have only ${product.stock} in stock.`, {
          autoClose: 2000
        })
      } else if (this.qty === undefined) {
        toast.danger('Please specify the quantity.', {
          autoClose: 2000
        })
      } else if (this.qty < 0) {
        toast.danger('Please specify a valid quantity.', {
          autoClose: 2000
        })
      } else if (this.qty > 0) {
        try {
          const productId = product.id
          const response = await fetch('http://127.0.0.1:5000/api/add_to_cart', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              Authorization: 'Bearer ' + localStorage.getItem('accessToken')
            },
            body: JSON.stringify({
              product_id: productId,
              quantity: 1 // You can modify this based on user input
            })
          })

          if (response.ok) {
            await fetch('http://127.0.0.1:5000/api/remove_from_fav', {
              method: 'DELETE',
              headers: {
                'Content-Type': 'application/json',
                Authorization: 'Bearer ' + localStorage.getItem('accessToken')
              },
              body: JSON.stringify({ product_id: productId })
            })
              .then((response) => {
                if (!response.ok) {
                  throw new Error('Failed to add to cart.')
                }
                return response.json()
              })
              .then((data) => {
                // Handle successful checkout
                console.log('Add to cart successful:', data.message)
                toast.success(`${product.name} added to cart!`, {
                  autoClose: 2000
                })
                this.products = this.products.filter((product) => product.id !== productId)
              })
          } else {
            const errorData = await response.json()
            // Show an error message to the user
            toast.error(errorData.message, {
              autoClose: 2000
            })
          }
        } catch (error) {
          console.error('Error adding to cart:', error)
        }
      }
    },
    async removeFromFavorites(productId) {
      try {
        const confirmDelete = window.confirm(
          'Are you sure you want to remove this product from favourites?'
        )

        if (confirmDelete) {
          // Make a POST request to the backend API for removing from favourites
          const response = await fetch('http://127.0.0.1:5000/api/remove_from_fav', {
            method: 'DELETE',
            headers: {
              'Content-Type': 'application/json',
              Authorization: 'Bearer ' + localStorage.getItem('accessToken')
            },
            body: JSON.stringify({ product_id: productId })
          })

          if (response.ok) {
            toast.success('Product removed from favourites!', {
              autoClose: 2000
            })
            this.products = this.products.filter((product) => product.id !== productId)
          } else {
            toast.error('Couldn not remove this product from favourites. Sorry', {
              autoClose: 2000
            })
          }
        }
      } catch (error) {
        console.error('Error removing from favourites:', error)
      }
    },
    async checkout(product) {
      // Create the cart array based on the provided format
      const cartItem = {
        ...product,
        qty: this.qty
      }

      const cart = [cartItem]

      const confirmCheckout = window.confirm('Are you sure you want to buy this product?')

      if (confirmCheckout) {
        const res = await fetch('http://127.0.0.1:5000/api/checkout', {
          method: 'POST',
          headers: {
            'Content-type': 'application/json',
            Authorization: 'Bearer ' + localStorage.getItem('accessToken')
          },
          body: JSON.stringify({ cart: cart })
        })

        if (res.ok) {
          const productId = product.id
          await fetch('http://127.0.0.1:5000/api/remove_from_fav', {
            method: 'DELETE',
            headers: {
              'Content-Type': 'application/json',
              Authorization: 'Bearer ' + localStorage.getItem('accessToken')
            },
            body: JSON.stringify({ product_id: productId })
          })
            .then((response) => {
              if (!response.ok) {
                throw new Error('Failed to checkout.')
              }
              return response.json()
            })
            .then(() => {
              // Handle successful checkout
              toast.success(
                `Checkout Successful! You bought ${this.qty} ${product.unit}s of ${product.name}.`,
                {
                  autoClose: 2000
                }
              )
              this.products = this.products.filter((product) => product.id !== productId)
            })
        } else {
          toast.error('Checkout unsuccessful. Please try again...', {
            autoClose: 2000
          })
        }
      }
    },
    getStockMessage(product) {
      if (!product.product_status) {
        return 'UNAVAILABLE'
      } else if (product.stock === 0) {
        return 'Out of Stock'
      } else if (product.stock <= 10) {
        return 'HURRY! Limited Stock Available.'
      } else if (this.isNewProduct(product.manufacturing_date)) {
        return 'RECENTLY ADDED'
      } else {
        return 'In Stock'
      }
    },
    getStockMessageStyle(product) {
      if (product.product_status === 0) {
        return 'color: red;'
      } else if (this.isNewProduct(product.manufacturing_date)) {
        return 'color: #4CAF50;' // Bright green -> fresh
      } else if (product.stock === 0) {
        return 'color: red;'
      } else if (product.stock <= 10) {
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
      if (this.qty === undefined) {
        toast.danger('Please specify the quantity.')
      } else if (this.qty < 0) {
        toast.danger('Please specify a valid quantity.')
      } else if (this.qty > product.stock) {
        toast.danger(`Sorry, we have only ${product.stock} in stock.`)
      } else if (this.qty > 0) {
        this.selectedProduct = product
        this.showCheckoutFormBool = true
      }
    }
  }
}
</script>
  
  <style scoped>
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
  