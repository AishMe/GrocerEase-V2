<template>
  <div class="min-vh-100" style="padding-top: 100px">
    <h1 class="my-5 text-center" style="font-size: 5rem; color: #c1e1c1">
      <strong>All Pending Requests</strong>
    </h1>
    <br />
    <h3 v-if="pendingManagers[0]" class="text-white">Add Manager Requests</h3>
    <div v-if="isLoading" class="row">
      <div class="col-md-3" v-for="user in pendingManagers" :key="user.user_id">
        <div class="card mb-4" style="width: 18rem">
          <div class="text-center">
            <img
              :src="user.avatar"
              class="rounded-circle mt-3"
              style="width: 100px; height: 100px"
              alt="Circle Image"
            />
          </div>
          <div class="card-body">
            <h5 class="card-title text-center">{{ user.name }}</h5>
            <!-- <p class="card-title text-center">{{ user.role }}</p> -->
            <hr />
            <p class="card-text">Email: {{ user.email }}</p>
            <p class="card-text">Phone No: +91-9876543210</p>
            <p class="card-text">Address: L-101, XYZ Housing Society, Bangalore, Karnataka</p>
          </div>
          <div class="d-flex justify-content-between card-footer">
            <a @click="approveRequest(user.user_id)" class="btn btn-success text-white px-4"
              >Accept</a
            >
            <a @click="declineRequest(user.user_id)" class="btn btn-danger text-white px-4"
              >Reject</a
            >
          </div>
        </div>
      </div>
    </div>
    <h3 v-if="pendingCategories[0]" class="text-white">Add Category Requests</h3>
    <div class="row">
      <div class="col-md-3" v-for="category in pendingCategories" :key="category.category_id">
        <div class="card mb-4" style="width: 18rem">
          <!-- Add category-specific content here -->
          <img
            class="bd-placeholder-img card-img-top"
            :src="category.image"
            style="width: 100%; height: 14vw"
            alt="{{ category.name }} Image"
          />
          <div class="card-body">
            <h3 class="card-title text-center">{{ category.name }}</h3>

            <!-- Buttons for category approval/rejection -->
            <div class="d-flex justify-content-between card-footer">
              <a
                @click="approveCategory(category.category_id)"
                class="btn btn-success text-white px-4"
                >Accept</a
              >
              <a
                @click="declineCategory(category.category_id)"
                class="btn btn-danger text-white px-4"
                >Reject</a
              >
            </div>
          </div>
        </div>
      </div>
    </div>
    <h3 v-if="deleteCategories[0]" class="text-white">Delete Category Requests</h3>
    <div class="row">
      <div class="col-md-3" v-for="category in deleteCategories" :key="category.category_id">
        <div class="card mb-4" style="width: 18rem">
          <!-- Add category-specific content here -->
          <img
            class="bd-placeholder-img card-img-top"
            :src="category.image"
            style="width: 100%; height: 14vw"
            alt="{{ category.name }} Image"
          />
          <div class="card-body">
            <h3 class="card-title text-center">{{ category.name }}</h3>

            <!-- Buttons for category approval/rejection -->
            <div class="d-flex justify-content-between card-footer">
              <a @click="deleteCategory(category)" class="btn btn-danger text-white px-4">Delete</a>
              <a @click="keepCategory(category.category_id)" class="btn btn-primary text-white px-4"
                >Keep</a
              >
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
      pendingManagers: [],
      pendingCategories: [],
      deleteCategories: []
    }
  },
  mounted() {
    this.fetchPendingManagers()
    this.fetchPendingCategories()
    this.fetchCategoryDeletionRequests()
  },
  methods: {
    async fetchPendingManagers() {
      try {
        const response = await fetch('http://127.0.0.1:5000/admin/pending/managers', {
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('accessToken')
          }
        })

        if (response.ok) {
          const data = await response.json()
          console.log('PENDING MANAGERS: ', data)
          this.pendingManagers = data.pendingManagers
          this.isLoading = true
        }
      } catch (error) {
        console.error('Error fetching pending managers:', error)
      }
    },
    async fetchPendingCategories() {
      try {
        const response = await fetch('http://127.0.0.1:5000/admin/pending_categories', {
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('accessToken')
          }
        })

        if (response.ok) {
          const data = await response.json()
          console.log('PENDING CATEGORIES: ', data)
          this.pendingCategories = data.pendingCategories
        }
      } catch (error) {
        console.error('Error fetching pending categories:', error)
      }
    },
    async fetchCategoryDeletionRequests() {
      try {
        const response = await fetch('http://127.0.0.1:5000/admin/category_deletion_request', {
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('accessToken')
          }
        })

        if (response.ok) {
          const data = await response.json()
          console.log('DELETE CATEGORIES: ', data)
          this.deleteCategories = data.deleteCategories
        }
      } catch (error) {
        console.error('Error fetching delete category requests:', error)
      }
    },
    async approveRequest(userId) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/admin/approve/${userId}`, {
          method: 'PUT',
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('accessToken'),
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ request_approval: 1 }) // Change request_approval status
        })

        if (response.ok) {
          // Update the list by filtering out the user that was approved
          this.pendingManagers = this.pendingManagers.filter((user) => user.user_id !== userId)
          toast.success('Manager Accepted!')
        }
      } catch (error) {
        console.error('Error approving manager request:', error)
      }
    },
    async declineRequest(userId) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/admin/decline/${userId}`, {
          method: 'PUT',
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('accessToken'),
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ request_approval: -1 }) // Change request_approval status
        })

        if (response.ok) {
          // Update the list by filtering out the user that was declined
          this.pendingManagers = this.pendingManagers.filter((user) => user.user_id !== userId)
          toast.warning('Manager Rejected.')
        }
      } catch (error) {
        console.error('Error declining manager request:', error)
      }
    },
    async approveCategory(categoryId) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/admin/approve_category/${categoryId}`, {
          method: 'PUT',
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('accessToken'),
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ category_approval: 1 }) // Change category_approval status
        })

        if (response.ok) {
          // Update the list by filtering out the category that was approved
          this.pendingCategories = this.pendingCategories.filter(
            (category) => category.category_id !== categoryId
          )
          toast.success('Category Accepted!')
        }
      } catch (error) {
        console.error('Error approving category request:', error)
      }
    },
    async declineCategory(categoryId) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/admin/decline_category/${categoryId}`, {
          method: 'PUT',
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('accessToken'),
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ category_approval: -1 }) // Change category_approval status
        })

        if (response.ok) {
          // Update the list by filtering out the category that was declined
          this.pendingCategories = this.pendingCategories.filter(
            (category) => category.category_id !== categoryId
          )
          toast.warning('Category Rejected.')
        }
      } catch (error) {
        console.error('Error declining category request:', error)
      }
    },
    async keepCategory(categoryId) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/admin/keep_category/${categoryId}`, {
          method: 'PUT',
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('accessToken'),
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ category_approval: 1 }) // Change request_approval status
        })

        if (response.ok) {
          // Update the list by filtering out the category that was not deleted
          this.deleteCategories = this.deleteCategories.filter(
            (category) => category.category_id !== categoryId
          )
          toast.info('Category Not Deleted!')
        }
      } catch (error) {
        console.error('Error keeping the category:', error)
      }
    },
    async deleteCategory(category) {
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
              `http://127.0.0.1:5000/api/category/delete/${category.category_id}`,
              {
                method: 'DELETE',
                headers: {
                  'Content-type': 'application/json',
                  Authorization: 'Bearer ' + localStorage.getItem('accessToken')
                }
              }
            )

            if (response.ok) {
              // Update the list by filtering out the user that was approved
              this.deleteCategories = this.deleteCategories.filter(
                (category) => category.category_id !== category.category_id
              )
              toast.success('Category Deleted Successfully!')
            } else {
              toast.danger('Oops! Something Went Wrong. Cannot Delete the Category.')
            }
          } catch (error) {
            console.error('Error deleting the category ', error)
          }
        } else if (categoryNameConfirmation === null) {
          // User clicked Cancel on the category name prompt
          toast.danger('Deletion Canceled. Category Name is not Provided.')
        } else {
          // User typed-in the wrong category name
          toast.danger('Deletion Canceled. Category Name is Wrong.')
        }
      } else {
        // User clicked Cancel on the initial confirmation
        toast.danger('Deletion Canceled.')
      }
    }
  }
}
</script>
  