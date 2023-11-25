
<template>
  <div>
    <div class="fab">
      <a
        @click="showCategoryForm"
        data-bs-toggle="tooltip"
        data-bs-placement="top"
        title="Add Category"
      >
        <i class="bi bi-bag-plus-fill"></i>
      </a>
    </div>

    <div class="row">
      <div
        v-for="(category, index) in categories"
        :key="index"
        class="col-md-4 d-flex justify-content-center"
      >
        <div class="card bg-light mb-4 shadow-lg p-3 mb-5 bg-body rounded" style="width: 25rem">
          <img
            :src="
              category.category_image
                ? category.category_image
                : require('@/assets/images/Logo.png')
            "
            :alt="category.category_name + ' Image'"
            style="width: 100%; height: 10vw; object-fit: cover"
            class="card-img-top"
          />
          <div class="card-body">
            <center>
              <h3 style="color: black">{{ category.category_name }}</h3>
            </center>

            <div class="overflow-auto" style="height: 400px">
              <div
                v-for="product in productsByCategory[category.category_id]"
                :key="product.product_id"
                class="card mb-2 shadow p-3 mb-5 rounded"
                style="width: 310px"
              >
                <img
                  :src="product.image ? product.image : require('@/assets/images/Logo.png')"
                  :alt="product.name + ' Image'"
                  style="width: 100%; height: 7vw; object-fit: cover"
                  class="card-img-top"
                />
                <div class="card-body">
                  <center>
                    <h5 class="card-title" style="color: black">{{ product.name }}</h5>
                  </center>
                  <hr style="margin-top: 1rem; border: 1px solid black" />
                  <p class="card-text">
                    Manufacturing Date: {{ product.manufacture_date }}<br />
                    Rate per unit: Rs.{{ product.rate_per_unit }}/{{ product.unit }}<br />
                    Stock: {{ product.stock }}
                  </p>
                  <div class="d-flex justify-content-center align-items-center">
                    <a @click="openProductForm('Update Product', 'Update')"
                      ><button class="btn btn-outline-warning">
                        <i class="bi bi-pencil-square"></i>Edit
                      </button></a
                    >
                    <span style="flex-grow: 0.5"></span>
                    <a href="#" @click="deleteProduct(product.product_id)"
                      ><button class="btn btn-outline-danger">
                        <i class="bi bi-trash"></i>Delete
                      </button></a
                    >
                  </div>
                </div>
              </div>
            </div>

            <div>
              <br />
              <div class="d-flex justify-content-between">
                <a @click="showProductForm"
                  ><button class="btn btn-outline-primary">
                    <i class="fa fa-plus-circle"></i>Add Items
                  </button></a
                >
                <span style="flex-grow: 1"></span>
                <a @click="openCategoryForm('Update Category', 'Update')"
                  ><button class="btn btn-outline-warning">
                    <i class="bi bi-pencil-square"></i></button
                ></a>
                <span style="flex-grow: 0.3"></span>
                <a href="#" @click="deleteCategory(category.category_id)"
                  ><button class="btn btn-outline-danger"><i class="bi bi-trash"></i></button
                ></a>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- Blurred Background -->
    <div v-if="showAddCategoryForm || showAddProductForm" class="blur-background">
      <div class="center-form">
      <!-- Add Category Form -->
      <div v-if="showAddCategoryForm">
        <div class="card bg-light mb-4 shadow-lg p-3 mb-5 bg-body rounded" style="width: 25rem;">
          <div class="card-body">
            <h5 class="card-title">Add Category</h5>
            <!-- Category Form Fields -->
            <form @submit.prevent="addCategory">
              <div class="mb-3">
                <label for="categoryName" class="form-label">Category Name</label>
                <input type="text" class="form-control" id="categoryName" v-model="newCategory.name" required>
              </div>
              <div class="mb-3">
                <label for="categoryImage" class="form-label">Category Image URL</label>
                <input type="text" class="form-control" id="categoryImage" v-model="newCategory.image" required>
              </div>
              <!-- Add Category and Cancel Buttons -->
              <div class="d-flex justify-content-end">
                <button type="submit" class="btn btn-primary">Add Category</button>
                <button type="button" class="btn btn-secondary" @click="cancelCategoryForm">Cancel</button>
              </div>
            </form>
          </div>
        </div>
      </div>

      <!-- Add Product Form -->
      <div v-if="showAddProductForm" class="col-md-4 d-flex justify-content-center">
        <div class="card bg-light mb-4 shadow-lg p-3 mb-5 bg-body rounded" style="width: 25rem;">
          <div class="card-body">
            <h5 class="card-title">Add Product</h5>
            <!-- Product Form Fields -->
            <form @submit.prevent="addProduct">
              <div class="mb-3">
                <label for="productName" class="form-label">Product Name</label>
                <input type="text" class="form-control" id="productName" v-model="newProduct.name" required>
              </div>
              <div class="mb-3">
                <label for="productImage" class="form-label">Product Image URL</label>
                <input type="text" class="form-control" id="productImage" v-model="newProduct.image" required>
              </div>
              <div class="mb-3">
                <label for="productPrice" class="form-label">Product Price</label>
                <input type="number" class="form-control" id="productPrice" v-model="newProduct.price" required>
              </div>
              <div class="mb-3">
                <label for="productUnit" class="form-label">Product Unit</label>
                <input type="text" class="form-control" id="productUnit" v-model="newProduct.unit" required>
              </div>
              <div class="mb-3">
                <label for="productStock" class="form-label">Product Stock</label>
                <input type="number" class="form-control" id="productStock" v-model="newProduct.stock" required>
              </div>
              <!-- Add Product and Cancel Buttons -->
              <div class="d-flex justify-content-end">
                <button type="submit" class="btn btn-primary">Add Product</button>
                <button type="button" class="btn btn-secondary" @click="cancelProductForm">Cancel</button>
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
export default {
  data() {
    return {
      categories: [],
      productsByCategory: {},

      showAddCategoryForm: false,
      showAddProductForm: false,
      newCategory: { name: '', image: '' },
      newProduct: { name: '', image: '', price: 0, unit: '', stock: 0 },
    }
  },
  mounted() {
    this.fetchCategories();
    this.fetchProductsbyCategories();
  },
  methods: {
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
    async fetchProductsbyCategories() {
      try {
        // Fetch products from the API
        const response = await fetch('http://127.0.0.1:5000/api/manager_admin_dashboard')

        if (response.ok) {
          const responseData = await response.json()
          this.productsByCategory = responseData.productsByCategory
        } else {
          alert('Oops! Something went wrong. Cannot fetch the products by categories.')
        }
      } catch (error) {
        console.error('Error fetching products by categories:', error)
      }
    },

    async deleteCategory(categoryId) {
      // Logic to delete the category based on sectionId
      try {
        // Fetch products from the API
        const response = await fetch(`http://127.0.0.1:5000/delete_category/${categoryId}`)

        if (response.ok) {
          alert("Category Deleted Successfully!")

        } else {
          alert('Oops! Something went wrong. Cannot delete the category.')
        }
      } catch (error) {
        console.error('Error deleting the category', error)
      }
    },
    async deleteProduct(productId) {
      // Logic to delete the product based on productId
      try {
        // Fetch products from the API
        const response = await fetch(`http://127.0.0.1:5000/delete_product/${productId}`)

        if (response.ok) {
          alert("Product Deleted Successfully!")

        } else {
          alert('Oops! Something went wrong. Cannot delete the product.')
        }
      } catch (error) {
        console.error('Error deleting the product ', error)
      }
    },
    showCategoryForm() {
      this.showAddCategoryForm = true;
    },

    cancelCategoryForm() {
      this.showAddCategoryForm = false;
    },

    showProductForm() {
      this.showAddProductForm = true;
    },

    cancelProductForm() {
      this.showAddProductForm = false;
    },

    // Additional methods for submitting category and product forms
    addCategory() {
      // Logic to add a new category
      // After adding, refresh categories and hide the form
      // You need to implement the actual API call to add a category here
      this.fetchCategories();
      this.showAddCategoryForm = false;
    },

    addProduct() {
      // Logic to add a new product
      // After adding, refresh products and hide the form
      // You need to implement the actual API call to add a product here
      this.fetchProductsbyCategories();
      this.showAddProductForm = false;
    },
  }
}
</script>

<style scoped>
.blur-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: inherit;
  backdrop-filter: blur(50px); /* Adjust the blur intensity as needed */
  z-index: 2; /* Ensure it's above other elements */
}

.center-form {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

/* ... other existing styles ... */
</style>