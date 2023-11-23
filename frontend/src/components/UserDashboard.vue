<!-- <template>
  <div class="container min-h-content text-center">
    
    <div class="row mb-3">
      <div class="col-md-4">
        <select v-model="selectedCategory" class="form-select" id="categoryDropdown">
          <option value="">All Categories</option>
          <option v-for="category in categories" :key="category.id" :value="category.id">{{ category.name }}</option>
        </select>
      </div>
      <div class="col-md-4">
        <input v-model="searchTerm" @input="updateFilteredProducts" type="text" class="form-control" id="searchInput" placeholder="Enter product name">
      </div>
      <div class="col-md-4">
        <select v-model="sortOrder" @change="updateFilteredProducts" class="form-select" id="sortDropdown">
          <option value="asc">Oldest first</option>
          <option value="desc">Newest first</option>
        </select>
      </div>
    </div>
      <div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 g-3">
        <div class="col" v-for="product in filteredProducts" :key="product.id">
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
    <br /><br />
  </div>
</template>

<script>
import CartButton from '../components/CartButton.vue'

export default {
  layout: null,
  components: { CartButton },
  data() {
    return {
      products: [],
      categories: [],
      filteredProducts: [],
      selectedCategory: '',
      searchTerm: '',
      sortOrder: 'asc',
    }
  },
  mounted() {
    this.fetchCategories();
    this.fetchProducts();
    this.fetchData();
  },
  methods: {
    async fetchCategories() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/categories');
        if (response.ok) {
          const responseData = await response.json();
          this.categories = responseData.categories;
        } else {
          console.error('Error fetching categories:', response.statusText);
        }
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    },
    async fetchProducts() {
  try {
    const url = this.selectedCategory
      ? `http://127.0.0.1:5000/api/products?category_id=${this.selectedCategory.id}`
      : 'http://127.0.0.1:5000/api/products';

    const response = await fetch(url);
    if (response.ok) {
      const responseData = await response.json();

      // Ensure all products have the manufacturing_date property
      this.products = responseData.products.map(product => ({
        ...product,
        manufacturing_date: product.manufacturing_date || null,
      }));
    } else {
      alert('Oops! Something went wrong. Cannot fetch the products.');
    }
  } catch (error) {
    console.error('Error fetching products:', error);
  }
},
    async fetchData() {
      try {
        const productResponse = await fetch('http://127.0.0.1:5000/api/products');
        const categoryResponse = await fetch('http://127.0.0.1:5000/api/categories');

        if (productResponse.ok && categoryResponse.ok) {
          const productData = await productResponse.json();
          const categoryData = await categoryResponse.json();

          this.products = productData.products;
          this.categories = categoryData.categories;
          this.updateFilteredProducts();
        } else {
          console.error('Error fetching products or categories:', productResponse.statusText, categoryResponse.statusText);
        }
      } catch (error) {
        console.error('Error fetching products or categories:', error);
      }
    },
    updateFilteredProducts() {
  // Filter products based on selected options
  this.filteredProducts = this.products.filter(product =>
    (this.selectedCategory === '' || product.category_id === this.selectedCategory || this.selectedCategory === 'All Categories') &&
    (product.product_name && product.product_name.toLowerCase().includes(this.searchTerm.toLowerCase())) &&
    (product.manufacturing_date !== undefined)
  );

  // Sort filtered products
  this.sortProducts();
},
sortProducts() {
  // Sort filtered products based on selected order
  if (this.sortOrder === 'asc') {
    this.filteredProducts.sort((a, b) => {
      if (a.manufacturing_date && b.manufacturing_date) {
        return new Date(a.manufacturing_date) - new Date(b.manufacturing_date);
      } else {
        return 0; // Handle the case where manufacturing_date is missing
      }
    });
  } else {
    this.filteredProducts.sort((a, b) => {
      if (a.manufacturing_date && b.manufacturing_date) {
        return new Date(b.manufacturing_date) - new Date(a.manufacturing_date);
      } else {
        return 0; // Handle the case where manufacturing_date is missing
      }
    });
  }
},

  }
}
</script>

<style scoped>
.container {
  backdrop-filter: blur(15px);
}
</style> -->

<template>
  <div class="container min-h-content py-5 text-center">
    <h1 class="mb-5" style="font-size: 5rem; color: #c1e1c1">
      <strong>Categories & Products</strong>
    </h1>
    <div class="row row-cols-1 row-cols-md-4 g-4">
      <div v-for="(product, index) in products" :key="index" class="col">
        <div class="card shadow-sm">
          <img
            v-if="product.image === ''"
            class="bd-placeholder-img card-img-top"
            :src="`{{ url_for('static', filename='images/Logo.png') }}`"
            alt="{{ product.name }} Image"
          />
          <img
            v-else
            class="bd-placeholder-img card-img-top"
            :src="product.image"
            alt="{{ product.name }} Image"
          />
          <div class="card-body">
            <h5 class="card-title" style="color: black">{{ product.name }}</h5>
            <h6 class="card-text" style="color: black">Vendor</h6>
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
                  <!-- <input
                    type="number"
                    class="form-control"
                    name="quantity"
                    placeholder="Qtn(kg)"
                    min="1"
                    :max="product.stock"
                    required
                  /> -->
                  <input
                    type="number"
                    class="form-control"
                    name="quantity"
                    placeholder="Qtn(kg)"
                    v-model="qty"
                    min="1"
                    required
                  />
                  <button
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
            <!-- <div class="row align-items-center justify-content-center">
              <form >
                <input type="hidden" name="section_id" :value="product.section_id">
                <input type="number" class="form-control" name="quantity" placeholder="Qtn(kg)" min="0" :max="product.stock" required v-model="product.quantity">
                <button type="submit" class="btn btn-outline-primary"><i class="fa fa-shopping-cart"></i></button>
                <button type="submit" class="btn btn-outline-success"><i class="fa fa-shopping-bag"></i></button>
              </form>
            </div> -->
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
        const response = await fetch('http://127.0.0.1:5000/api/products')
        // if (response.ok) {
        //   const responseData = await response.json()
        //   this.products = responseData.products
        //   this.products.qty = this.qty

          if (response.ok) {
      const responseData = await response.json();
      this.products = responseData.products.map(product => ({
        ...product,
        manufacturing_date: product.manufacturing_date || null,
        qty: this.qty || 1, // Set the initial quantity to 1
      }));
        } else {
          alert('Oops! Something went wrong. Cannot fetch the products.')
        }
      } catch (error) {
        console.error('Error fetching products:', error)
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
          this.$store.commit('addRemoveCart', { product: { ...product, qty: this.qty }, toAdd: true })
        }

        // Show success toast
        showToast('Added to Cart', 'success')
      }
    },
  }
}
</script>

<style>
/* Add custom styles if needed */
</style>
