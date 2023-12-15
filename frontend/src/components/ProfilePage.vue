<template>
  <div class="d-flex justify-content-center align-items-center min-vh-100">
    <div class="card" style="min-width: 40%; height: 32%">
      <div class="row g-0">
        <div class="col-md-4">
          <img
            :src="avatar"
            class="img-fluid rounded-start"
            alt="Profile Photo"
            style="width: 250px; height: 250px; object-fit: cover; overflow: hidden"
          />
        </div>
        <div class="col-md-8">
          <div class="card-body">
            <h1 class="card-title mb-3">MY PROFILE</h1>

            <!-- Display Mode -->
            <div v-if="!isEditing">
              <h4>Email: {{ email }}</h4>
              <h4>Name: {{ name }}</h4>
              <h4>Role: {{ role }}</h4>
              <div class="d-flex justify-content-between mt-4">
                <button class="btn btn-warning" @click="startEditing">Edit Info</button>
                <button class="btn btn-danger" @click="confirmDeleteAccount">Delete Account</button>
              </div>
            </div>

            <!-- Edit Mode -->
            <div v-else>
              <form @submit.prevent="saveInfo">
                <div class="mb-3">
                  <label for="editedName" class="form-label">Name</label>
                  <input type="text" class="form-control" id="editedName" v-model="editedName" />
                </div>
                <div class="mb-3">
                  <label for="editedEmail" class="form-label">Email</label>
                  <input type="email" class="form-control" id="editedEmail" v-model="editedEmail" />
                </div>
                <div class="d-flex justify-content-between mt-5">
                  <button class="btn btn-success">Save Info</button>
                  <button class="btn btn-danger" @click="cancelEditing">Cancel</button>
                </div>
              </form>
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
      name: '',
      email: '',
      role: localStorage.getItem('role'),
      profile: '',
      isEditing: false,
      editedName: '',
      editedEmail: ''
    }
  },
  async mounted() {
    const res = await fetch('http://127.0.0.1:5000/api/user/profile', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + localStorage.getItem('accessToken')
      }
    })

    const d = await res.json()
    if (res.ok) {
      this.name = d.name
      this.email = d.email
      this.avatar = d.avatar
      this.editedName = d.name // Initialize edited values with the current values
      this.editedEmail = d.email
    } else {
      this.$router.push({ path: '/login' })
    }
  },
  methods: {
    startEditing() {
      this.isEditing = true
    },
    cancelEditing() {
      this.isEditing = false
    },
    saveInfo: async function () {
      const updatedData = {
        name: this.editedName,
        email: this.editedEmail
      }

      // Make a PUT request to update user information
      const req = await fetch(`http://127.0.0.1:5000/api/user/edit_profile`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + localStorage.getItem('accessToken')
        },
        body: JSON.stringify(updatedData)
      })

      const res = await req.json()
      if (req.ok) {
        // Update the displayed name and email with edited values
        this.name = this.editedName
        this.email = this.editedEmail
        this.isEditing = false // Exit edit mode
      } else {
        // Handle the case when the update fails (e.g., show an error message)
        console.error('Update failed:', res.message)
      }
    },

    confirmDeleteAccount: async function () {
      // Show a confirmation dialog
      const confirmed = confirm('Are you sure you want to delete your account?')

      if (confirmed) {
        // Ask for email verification
        const userEmail = prompt('To confirm, please enter your email:')

        if (userEmail === this.email) {
          // Perform the account deletion (you can make a DELETE request here)
          const req = await fetch(`http://127.0.0.1:5000/api/user/delete_account`, {
            method: 'DELETE',
            headers: {
              'Content-Type': 'application/json',
              Authorization: 'Bearer ' + localStorage.getItem('accessToken')
            }
          })
          if (req.ok) {
            // Show a confirmation alert
            alert('Your account has been deleted.')
            localStorage.removeItem('accessToken')
            localStorage.removeItem('role')
            this.$router.push({ path: '/' }).then(() => {
              this.$router.go()
            })
          }
        } else {
          // Show an error alert if the email doesn't match
          alert('Email verification failed. Your account was not deleted.')
        }
      }
    }
  }
}
</script>
