<template>
  <section class="h-100 h-custom min-h-content" style="padding-top: 100px">
    <div class="container py-5 h-100">
      <br /><br /><br />
      <div class="row d-flex justify-content-center align-items-center h-100">
        <div class="col">
          <div class="card border-0">
            <div class="card-body p-4 rounded-5" style="background-color: #f4f7f3">
              <div class="row">
                <div class="col-lg-7">
                  <div class="d-flex justify-content-between">
                    <h5 class="mb-3">
                      <router-link :to="{ name: 'dashboard' }" class="text-body"
                        ><i class="fas fa-long-arrow-alt-left me-2"></i>Continue
                        shopping</router-link
                      >
                    </h5>
                    <div class="d-flex justify-content-center">
                      <input
                        type="text"
                        placeholder="Discount Coupon"
                        v-model="discountCode"
                        class="form-control"
                      />
                      <button
                        name="action"
                        class="btn btn-outline-primary"
                        @click.prevent="applyDiscount"
                      >
                        Apply
                      </button>
                    </div>
                  </div>
                  <hr />

                  <div class="d-flex justify-content-between align-items-center mb-4">
                    <div>
                      <p class="mb-0">You have {{ $store.state.cart.length }} items in your cart</p>
                    </div>
                  </div>

                  <div
                    v-for="item in $store.state.cart"
                    class="card mb-3 shadow-sm border-0"
                    :key="item.id"
                  >
                    <div class="card-body">
                      <div class="d-flex justify-content-between">
                        <div class="d-flex flex-row align-items-center">
                          <div>
                            <img
                              :src="item.image"
                              class="img-fluid rounded-3"
                              alt="Shopping item"
                              style="width: 65px"
                            />
                          </div>
                          <div class="ms-3">
                            <p>{{ item.name }}</p>
                          </div>
                        </div>

                        <div class="d-flex flex-row align-items-center">
                          <div>
                            <CartAddRemove :product="item" />
                          </div>
                        </div>
                        <div class="d-flex flex-row align-items-center">
                          <div>
                            <h5 class="mb-0" v-if="item.price">
                              <i class="bi bi-currency-rupee"></i>{{ item.price * (item.qty || 0) }}
                            </h5>
                          </div>
                          <a
                            role="button"
                            @click="removeItem(item)"
                            class="ms-4"
                            style="color: #cecece"
                            ><i class="bi bi-trash3 h4"></i
                          ></a>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="col-lg-5">
                  <div class="card text-white rounded-0 border-0" style="background-color: #3a915d">
                    <div class="card-body">
                      <div class="d-flex justify-content-between align-items-center mb-4">
                        <h5 class="mb-0">Cart details</h5>
                        <i class="bi bi-cart3 h1"></i>
                      </div>
                      <hr class="my-4" />
                      <div class="d-flex justify-content-between">
                        <p class="mb-2">Initial Price</p>
                        <p class="mb-2">
                          <i class="bi bi-currency-rupee"></i>{{ $store.state.cartTotal }}
                        </p>
                      </div>
                      <div class="d-flex justify-content-between mb-4">
                        <p class="mb-2">Final Discounted Price</p>
                        <p class="mb-2" v-if="finalTotalPrice">
                          <i class="bi bi-currency-rupee"></i>{{ finalTotalPrice }}
                        </p>
                        <p class="mb-2" v-else>
                          <i class="bi bi-currency-rupee"></i>{{ $store.state.cartTotal }}
                        </p>
                      </div>

                      <button
                        @click.prevent="showCheckoutForm"
                        type="button"
                        class="btn btn-block btn-lg"
                        style="background-color: #c1e1c1"
                      >
                        Checkout
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <br /><br /><br /><br />
      <br /><br /><br />
    </div>
    <!-- Checkout form -->
    <div v-if="showCheckoutFormBool" class="form-container">
      <div class="form card">
        <div class="card-header">
          <h5 class="mb-0">Payment Options</h5>
        </div>
        <form @submit.prevent="checkout">
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
  </section>
</template>
<script>
import CartAddRemove from '../components/CartAddRemove.vue'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'
export default {
  data() {
    return {
      showCheckoutFormBool: false,
      selectedPaymentOption: null,
      cardName: '',
      cardNumber: '',
      cardExpiration: '',
      cVV: '',
      upiId: '',
      discountCode: '', // Discount code entered by the user
      discountedPrices: {}, // Object to store discounted prices for each product
      finalTotalPrice: 0 // Final total price after discounts
    }
  },
  components: { CartAddRemove },
  methods: {
    async logout() {
      localStorage.removeItem('accessToken')
      localStorage.removeItem('role')
      this.$router.push({ path: '/' }).then(() => {
        this.$router.go()
      })
      alert('User Session Expired. Please Login Again.')
    },
    async removeItem(item) {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/cart/remove', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + localStorage.getItem('accessToken')
          },
          body: JSON.stringify({
            product_id: item.id
          })
        })

        if (response.ok) {
          // Update the cart state in the Vuex store with the fetched data
          this.$store.dispatch('fetchCart')
          this.$store.commit('addRemoveCart', { product: item, toAdd: false })
          toast.success('Cart item removed', {
            autoClose: 2000
          })
        } else {
          toast.error('Failed to remove cart item', {
            autoClose: 2000
          })
        }
      } catch (error) {
        console.error('Error removing cart item:', error)
      }
    },
    applyDiscount() {
      const { productName, discountPercent } = this.parseDiscountCode(this.discountCode)
      this.discountedPrices = {} // Reset discounted prices

      this.$store.state.cart.forEach((item) => {
        if (
          productName === 'ALLPRODUCT' ||
          item.name.replace(' ', '').toLowerCase().includes(productName.toLowerCase())
        ) {
          const discountAmount = item.price * (item.qty || 0) * (discountPercent / 100)
          this.discountedPrices[item.name] = item.price * (item.qty || 0) - discountAmount
          this.updateDiscountPercent()
        } else {
          this.discountedPrices[item.name] = item.price * (item.qty || 0) // No discount applied
        }
      })
      this.calculateFinalTotal()
      // toast.success('Discount Applied Successfully!', {
      //       autoClose: 2000
      //     })
    },

    calculateFinalTotal() {
      this.finalTotalPrice = Object.values(this.discountedPrices).reduce(
        (acc, curr) => acc + curr,
        0
      )
    },

    parseDiscountCode(code) {
      const pattern = /([A-Za-z]+)(\d+)/
      const match = code.match(pattern)
      return {
        productName: match[1].toUpperCase(),
        discountPercent: parseInt(match[2], 10)
      }
    },
    async checkout() {
      try {
        // Send a request to your Flask backend to save the items in the database
        const confirmCheckout = window.confirm('Are you sure you want to buy this product?')

        if (confirmCheckout) {
          const res = await fetch('http://127.0.0.1:5000/api/checkout', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              Authorization: 'Bearer ' + localStorage.getItem('accessToken')
            },
            body: JSON.stringify({ cart: this.$store.state.cart })
          })

          console.log(this.$store.state.cart)
          if (res.ok) {
            // Clear the cart in the Vuex store and update the total
            this.$store.dispatch('clearCart')
            // Redirect to the orders page after successful checkout
            this.$router.push({ name: 'orders' })
          } else {
            alert('OOPS! Something Went Wrong. Please Try Again.')
          }
        }
      } catch (error) {
        console.log(this.$store.state.cart)
        console.error('Error during checkout:', error)
      }
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
    showCheckoutForm() {
      this.showCheckoutFormBool = true
    },
    async fetchCart() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/cart', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + localStorage.getItem('accessToken')
          }
        })

        if (response.ok) {
          const responseData = await response.json()
          // Update the cart state in the Vuex store with the fetched data
          this.$store.commit('setCart', responseData.cart)
        } else if (response.status === 401) {
          this.logout()
        } else {
          // Handle the case where fetching the cart data fails
          console.error('Failed to fetch cart data')
        }
      } catch (error) {
        console.error('Error fetching cart data:', error)
      }
    },
    async updateDiscountPercent() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/cart/update/discount', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + localStorage.getItem('accessToken')
          },
          body: JSON.stringify({ discount: this.discountCode })
        })

        if (response.ok) {
          this.fetchCart()
        } else {
          // Handle the case where updating the cart data fails
          console.error('Failed to update cart data')
        }
      } catch (error) {
        console.error('Error during updating cart data:', error)
      }
    }
  },
  mounted() {
    this.fetchCart()
  },
  watch: {
    '$store.state.cartTotal': {
      handler() {
        this.applyDiscount()
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