
<template>
  <div class="min-vh-100">
    <div class="fab">
      <a
        @click="showAddCategoryForm"
        data-bs-toggle="tooltip"
        data-bs-placement="top"
        title="Add Category"
      >
        <i class="bi bi-bag-plus-fill"></i>
      </a>
    </div>
    <div class="text-center">
      <h1 class="my-5" style="font-size: 5rem; color: #c1e1c1">
        <strong>Products & Categories</strong>
      </h1>
      <div v-if="isLoading" class="row">
        <div
          v-for="(category, index) in categories"
          :key="index"
          class="col-md-4 d-flex justify-content-center"
        >
          <div class="card bg-light mb-4 shadow-lg p-3 mb-5 bg-body rounded" style="width: 25rem">
            <img
              :src="category.image ? category.image : require('../assets/FrontPageDesign.png')"
              :alt="category.name + ' Image'"
              style="width: 100%; height: 10vw; object-fit: cover"
              class="card-img-top"
            />
            <div class="card-body">
              <center>
                <h3 class="fw-bold text-black">{{ category.name }}</h3>
              </center>

              <div class="overflow-auto" style="height: 400px">
                <div
                  v-for="product in productsByCategory[category.category_id]"
                  :key="product.product_id"
                  class="card mb-2 shadow p-3 mb-5 rounded"
                  style="width: 310px"
                >
                  <img
                    :src="product.image ? product.image : require('../assets/FrontPageDesign.png')"
                    :alt="product.name + ' Image'"
                    style="width: 100%; height: 7vw; object-fit: cover"
                    class="card-img-top"
                  />
                  <div class="card-body">
                    <center>
                      <h5 class="card-title text-black">{{ product.name }}</h5>
                    </center>
                    <hr style="margin-top: 1rem; border: 1px solid black" />
                    <p class="card-text">
                      Manufacturing Date: {{ product.manufacture_date }}<br />
                      Rate per unit: Rs.{{ product.price }}/{{ product.unit }}<br />
                      Stock: {{ product.stock }}
                    </p>
                    <div class="d-flex justify-content-center align-items-center">
                      <a @click="showEditProductForm(product)"
                        ><button class="btn btn-outline-warning">
                          <i class="bi bi-pencil-square"></i>Edit
                        </button></a
                      >
                      <span style="flex-grow: 0.5"></span>
                      <a @click="deleteProduct(product)"
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
                  <a @click="showAddProductForm(category.category_id)"
                    ><button class="btn btn-outline-primary">
                      <i class="fa fa-plus-circle"></i>Add Items
                    </button></a
                  >
                  <span style="flex-grow: 1"></span>
                  <a @click="showEditCategoryForm(category)"
                    ><button class="btn btn-outline-warning">
                      <i class="bi bi-pencil-square"></i></button
                  ></a>
                  <span style="flex-grow: 0.3"></span>
                  <a @click="deleteCategory(category)"
                    ><button class="btn btn-outline-danger"><i class="bi bi-trash"></i></button
                  ></a>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- Add/Edit Category Form -->
        <div v-if="showAddEditForm" class="blur-background">
          <div class="center-form">
            <div class="card bg-light mb-4 shadow-lg p-3 mb-5 bg-body rounded" style="width: 25rem">
              <div class="card-body">
                <h5 class="card-title text-center">
                  {{ editMode ? 'Edit' : 'Add' }} {{ formType }}
                </h5>
                <!-- Category/ Product Form Fields -->
                <form @submit.prevent="submitForm">
                  <div class="mb-3">
                    <label class="form-label">Category ID</label>
                    <input v-model="form.category_id" type="number" class="form-control" disabled />
                  </div>
                  <div class="mb-3">
                    <label class="form-label">Name</label>
                    <input v-model="form.name" type="text" class="form-control" required />
                  </div>
                  <div class="mb-3">
                    <label class="form-label">Image URL</label>
                    <input v-model="form.image" type="url" class="form-control" />
                  </div>
                  <div class="mb-3" v-if="formType === 'Product'">
                    <label class="form-label">Price</label>
                    <input v-model="form.price" type="number" class="form-control" required />
                  </div>
                  <div class="mb-3" v-if="formType === 'Product'">
                    <label class="form-label">Unit</label>
                    <input v-model="form.unit" type="text" class="form-control" required />
                  </div>
                  <div class="mb-3" v-if="formType === 'Product'">
                    <label class="form-label">Stock</label>
                    <input v-model="form.stock" type="number" class="form-control" required />
                  </div>
                  <!-- Add/Edit and Cancel Buttons -->
                  <div class="d-flex justify-content-end">
                    <button type="submit" class="btn btn-primary">
                      {{ editMode ? 'Edit' : 'Add' }} {{ formType }}
                    </button>
                    <button type="button" class="btn btn-secondary" @click="cancelForm">
                      Cancel
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
export default {
  data() {
    return {
      isLoading: false,
      categories: [],
      productsByCategory: {},

      showAddEditForm: false,
      editMode: false,
      formType: '', // 'Category' or 'Product'
      form: {
        category_id: '',
        name: '',
        image: '',
        price: '',
        unit: '',
        stock: ''
      }
    }
  },
  mounted() {
    this.fetchCategories()
    this.fetchProductsbyCategories()
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
        const response = await fetch('http://127.0.0.1:5000/api/manager_admin_dashboard', {
          method: 'GET',
          headers: {
            'Content-type': 'application/json',
            Authorization: 'Bearer ' + localStorage.getItem('accessToken')
          }
        })

        if (response.ok) {
          const responseData = await response.json()
          this.productsByCategory = responseData.productsByCategory
          this.isLoading = true
        } else {
          alert('Oops! Something went wrong. Cannot fetch the products by categories.')
        }
      } catch (error) {
        console.error('Error fetching products by categories:', error)
      }
    },

    async deleteCategory(category) {
      // Initial confirmation
      const confirmDelete = window.confirm('Are you sure you want to delete this category?')

      if (confirmDelete) {
        try {
          // Fetch categories from the API
          const response = await fetch(
            `http://127.0.0.1:5000/api/edit_category_request/${category.category_id}`,
            {
              method: 'PUT',
              headers: {
                'Content-type': 'application/json',
                Authorization: 'Bearer ' + localStorage.getItem('accessToken')
              },
              body: JSON.stringify({
                name: category.name,
                image: category.image,
                category_approval: -2
              })
            }
          )

          if (response.ok) {
            alert('Category Deletion Request Sent to the Admin.')
            window.location.reload()
          } else {
            alert('Oops! Something Went Wrong. Could Not Send Deletion Request to the Admin')
          }
        } catch (error) {
          console.error('Error deleting the category ', error)
        }
      } else {
        // User clicked Cancel on the initial confirmation
        alert('Deletion Canceled.')
      }
    },
    async deleteProduct(product) {
      // Initial confirmation
      const confirmDelete = window.confirm('Are you sure you want to delete this product?')

      if (confirmDelete) {
        // Prompt for product name confirmation
        const productNameConfirmation = window.prompt(
          'Please type the name of the product to confirm deletion:'
        )

        if (productNameConfirmation === product.name) {
          try {
            // Fetch products from the API
            const response = await fetch(
              `http://127.0.0.1:5000/delete_product/${product.product_id}`,
              {
                method: 'DELETE',
                headers: {
                  'Content-type': 'application/json',
                  Authorization: 'Bearer ' + localStorage.getItem('accessToken')
                }
              }
            )

            if (response.ok) {
              alert('Product Deleted Successfully!')
              window.location.reload()
            } else {
              alert('Oops! Something Went Wrong. Cannot Delete the Product.')
            }
          } catch (error) {
            console.error('Error deleting the product ', error)
          }
        } else if (productNameConfirmation === null) {
          // User clicked Cancel on the product name prompt
          alert('Deletion Canceled. Product Name is not Provided.')
        } else {
          // User typed-in the wrong product name
          alert('Deletion Canceled. Product Name is Wrong.')
        }
      } else {
        // User clicked Cancel on the initial confirmation
        alert('Deletion Canceled.')
      }
    },
    showAddCategoryForm() {
      this.showForm('Category')
    },
    showAddProductForm(categoryId) {
      this.showForm('Product')
      this.form.category_id = categoryId
    },
    showEditCategoryForm(category) {
      this.showForm('Category', true, category)
    },
    showEditProductForm(product) {
      this.showForm('Product', true, product)
    },
    showForm(formType, editMode = false, data = null) {
      this.formType = formType
      this.editMode = editMode

      if (editMode) {
        // Pre-fill form fields when editing
        this.form = { ...data }
        console.log('DATA EDIT FORM: ', { ...data })
        console.log('DATA EDIT FORM2: ', this.form)
      } else {
        // Clear form fields when adding
        this.form = {
          name: '',
          image: '',
          price: '',
          unit: '',
          stock: ''
        }
      }

      this.showAddEditForm = true
    },
    cancelForm() {
      this.showAddEditForm = false
      // Optionally clear the form fields
      this.form = {
        name: '',
        image: '',
        price: '',
        unit: '',
        stock: ''
      }
    },
    async submitForm() {
      try {
        // Determine which API to call based on formType and editMode
        let apiUrl

        if (this.editMode) {
          if (this.formType === 'Product') {
            // Edit product API with category_id as a parameter
            apiUrl = `http://127.0.0.1:5000/api/edit_product/${this.form.product_id}`
          } else {
            // Edit category API
            apiUrl = `http://127.0.0.1:5000/api/edit_category/${this.form.category_id}`
          }

          // Make the API call with the form data
          const response = await fetch(apiUrl, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
              Authorization: 'Bearer ' + localStorage.getItem('accessToken')
            },
            body: JSON.stringify(this.form)
          })

          if (response.ok) {
            alert('Update Form Submitted Successfully!')
            window.location.reload()
          } else {
            alert('Update Form Submission Failed')
          }
        } else {
          if (this.formType === 'Product') {
            // Add product API with category_id as a parameter
            apiUrl = `http://127.0.0.1:5000/api/${this.form.category_id}/add_product`
          } else {
            // Add category API
            apiUrl = 'http://127.0.0.1:5000/api/add_category'
          }

          // Make the API call with the form data
          const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              Authorization: 'Bearer ' + localStorage.getItem('accessToken')
            },
            body: JSON.stringify(this.form)
          })

          console.log('THIS FORM: ', this.form)
          if (response.ok) {
            alert('Add Form Submitted Successfully!')
            window.location.reload()
          } else {
            alert('Add Form Submission Failed')
          }
        }
      } catch (error) {
        console.error('Error submitting form:', error)
      } finally {
        // Close the form whether the submission succeeds or fails
        this.cancelForm()
      }
    }
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