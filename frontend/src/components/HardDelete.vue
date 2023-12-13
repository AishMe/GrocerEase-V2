<template>
  <div class="min-vh-100" style="padding-top: 100px">
    <!-- Button for deleting all temporarily deleted products -->
    <div class="fab bg-danger" style="width: 90px; height: 90px">
      <a
        @click="hardDeleteAll(products)"
        data-bs-toggle="tooltip"
        data-bs-placement="top"
        title="Hard Delete All"
      >
        <i class="bi bi-trash-fill"></i>
      </a>
    </div>

    <div v-if="isLoading" class="container min-h-content py-5 text-center">
      <h1 class="mb-3" style="font-size: 5rem; color: #c1e1c1">
        <strong>Dustbin</strong>
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
              <p class="card-text">
                Manufacturing Date: {{ product.manufacturing_date }}<br />
                Rate per unit: Rs.{{ product.price }}/{{ product.unit }}<br />
                Stock: {{ product.stock }}
              </p>

              <button
                @click.prevent="hardDeleteProduct(product.id)"
                class="btn btn-danger"
                name="action"
                value="purchase"
                data-product-id="{{ product.product_id }}"
                data-section-id="{{ product.section_id }}"
              >
                <span class="fw-bold px-3">HARD DELETE</span>
              </button>
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
      isLoading: false,
      products: []
    }
  },
  mounted() {
    this.fetchProducts()
  },

  methods: {
    async fetchProducts() {
      try {
        // Fetch products from the API
        const response = await fetch('http://127.0.0.1:5000/admin/hard_delete_item', {
          method: 'GET',
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('accessToken')
          }
        })

        if (response.ok) {
          const responseData = await response.json()
          this.products = responseData.tempDeletedProducts
          this.isLoading = true
        } else {
          alert('Oops! Something went wrong. Cannot fetch the products.')
        }
      } catch (error) {
        console.error('Error fetching products:', error)
      }
    },

    async hardDeleteProduct(productId) {
      // Initial confirmation
      const confirmDelete = window.confirm(`
        Are you sure you want to delete this product entirely.
        NOTE: This would also delete the product from history.
      `)

      if (confirmDelete) {
        try {
          // Call the new API endpoint for hard deleting a single product and its connections
          const response = await fetch(
            'http://127.0.0.1:5000/admin/delete_products_and_connections',
            {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                Authorization: 'Bearer ' + localStorage.getItem('accessToken')
              },
              body: JSON.stringify({
                product_ids: [productId]
              })
            }
          )
          const resJSON = await response.json()

          if (response.ok) {
            // Update the products array after successful hard delete
            this.products = this.products.filter((product) => product.id !== productId)
            console.log(`Product with ID ${productId} successfully hard deleted.`)
            toast.success(resJSON.message, {
              autoClose: 2000
            })
          } else {
            toast.error(resJSON.message, {
              autoClose: 2000
            })
          }
        } catch (error) {
          console.error('Error hard deleting product:', error)
        }
      }
    },

    async hardDeleteAll(products) {
      // Initial confirmation
      const confirmDeleteAll = window.confirm(
        'Are you sure you want to delete all these product entirely. NOTE: This would also delete the products from history.'
      )

      if (confirmDeleteAll) {
        try {
          // Call the new API endpoint for hard deleting all products and their connections
          const response = await fetch(
            'http://127.0.0.1:5000/admin/delete_products_and_connections',
            {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                Authorization: 'Bearer ' + localStorage.getItem('accessToken')
              },
              body: JSON.stringify({
                product_ids: products.map((product) => product.id)
              })
            }
          )
          const resJSON = await response.json()

          if (response.ok) {
            // Clear the products array after successful hard delete
            this.products = []
            console.log('All products successfully hard deleted.', {
              autoClose: 2000
            })
            toast.success(resJSON.message)
          } else {
            toast.error(resJSON.message, {
              autoClose: 2000
            })
          }
        } catch (error) {
          console.error('Error hard deleting all products:', error)
        }
      }
    }
  }
}
</script>
