
<template>
  <div class="min-vh-100" style="padding-top: 100px">
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

              <h6
                class="card-text fw-bold text-danger"
                v-if="category.category_approval == -2 || category.category_approval == 0"
              >
                Waiting for Admin's Approval…
              </h6>

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
                      <button
                        :disabled="category.category_approval === -2"
                        @click="showEditProductForm(product)"
                        class="btn btn-outline-warning"
                      >
                        <i class="bi bi-pencil-square"></i>Edit
                      </button>
                      <span style="flex-grow: 0.5"></span>
                      <button
                        :disabled="category.category_approval === -2"
                        @click="deleteProduct(product)"
                        class="btn btn-outline-danger"
                      >
                        <i class="bi bi-trash"></i>Delete
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <div>
                <br />
                <div class="d-flex justify-content-between">
                  <button
                    :disabled="
                      category.category_approval === -2 || category.category_approval === 0
                    "
                    @click="showAddProductForm(category.category_id)"
                    class="btn btn-outline-primary"
                  >
                    <i class="fa fa-plus-circle"></i>Add Items
                  </button>
                  <span style="flex-grow: 1"></span>
                  <button
                    :disabled="
                      category.category_approval === -2 || category.category_approval === 0
                    "
                    @click="showEditCategoryForm(category)"
                    class="btn btn-outline-warning"
                  >
                    <i class="bi bi-pencil-square"></i>
                  </button>
                  <span style="flex-grow: 0.3"></span>
                  <button
                    :disabled="
                      category.category_approval === -2 || category.category_approval === 0
                    "
                    @click="deleteCategory(category)"
                    class="btn btn-outline-danger"
                  >
                    <i class="bi bi-trash"></i>
                  </button>
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
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

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
      const categoryId = category.category_id
      // Initial confirmation
      const confirmDelete = window.confirm('Are you sure you want to delete this category?')

      if (confirmDelete) {
        // Prompt for category name confirmation
        const categoryNameConfirmation = window.prompt(
          'Please type the name of the category to confirm deletion:'
        )

        if (categoryNameConfirmation === category.name) {
          try {
            // Fetch categories from the API
            const response = await fetch(
              `http://127.0.0.1:5000/api/category/delete/${categoryId}`,
              {
                method: 'DELETE',
                headers: {
                  'Content-type': 'application/json',
                  Authorization: 'Bearer ' + localStorage.getItem('accessToken')
                }
              }
            )

            if (response.ok) {
              this.categories = this.categories.filter(
                (category) => category.category_id !== categoryId
              )
              toast.info('Category Deleted Successfully!')
            } else {
              toast.danger('Oops! Something Went Wrong. Cannot Delete the Category.')
            }
          } catch (error) {
            console.error('Error deleting the category ', error)
          }
        } else if (categoryNameConfirmation === null) {
          // User clicked Cancel on the category name prompt
          toast.warning('Deletion Canceled. Category Name is not Provided.')
        } else {
          // User typed-in the wrong category name
          toast.warning('Deletion Canceled. Category Name is Wrong.')
        }
      } else {
        // User clicked Cancel on the initial confirmation
        toast.warning('Deletion Canceled.')
      }
    },
    async deleteProduct(product) {
      const productId = product.product_id
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
            const response = await fetch(`http://127.0.0.1:5000/delete_product/${productId}`, {
              method: 'DELETE',
              headers: {
                'Content-type': 'application/json',
                Authorization: 'Bearer ' + localStorage.getItem('accessToken')
              }
            })

            if (response.ok) {
              this.productsByCategory[product.category_id] = this.productsByCategory[
                product.category_id
              ].filter((p) => p.product_id !== productId)
              toast.info('Product Deleted Successfully!')
            } else {
              toast.danger('Oops! Something Went Wrong. Cannot Delete the Product.')
            }
          } catch (error) {
            console.error('Error deleting the product ', error)
          }
        } else if (productNameConfirmation === null) {
          // User clicked Cancel on the product name prompt
          toast.warning('Deletion Canceled. Product Name is not Provided.')
        } else {
          // User typed-in the wrong product name
          toast.warning('Deletion Canceled. Product Name is Wrong.')
        }
      } else {
        // User clicked Cancel on the initial confirmation
        toast.warning('Deletion Canceled.')
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
            apiUrl = `http://127.0.0.1:5000/api/category/edit/${this.form.category_id}`
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
            toast.success('Update Form Submitted Successfully!')
          } else {
            toast.danger('Update Form Submission Failed')
          }
        } else {
          if (this.formType === 'Product') {
            // Add product API with category_id as a parameter
            apiUrl = `http://127.0.0.1:5000/api/${this.form.category_id}/add_product`
          } else {
            // Add category API
            apiUrl = 'http://127.0.0.1:5000/api/category/add'
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
            toast.success('Add Form Submitted Successfully!')
          } else {
            toast.danger('Add Form Submission Failed')
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
  backdrop-filter: blur(80px);
  z-index: 2;
}

.center-form {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}
</style>