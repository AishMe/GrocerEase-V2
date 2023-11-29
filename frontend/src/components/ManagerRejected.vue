<template>
  <div class="min-vh-100">
    <h1 class="my-5 text-center" style="font-size: 5rem; color: #c1e1c1">
      <strong>Requests Rejected</strong>
    </h1>
    <br />
    <div v-if="isLoading" class="row">
      <div class="col-md-3" v-for="user in rejectedManagers" :key="user.user_id">
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
            <p class="card-title text-center">{{ user.role }}</p>
            <hr />
            <p class="card-text">Email: {{ user.email }}</p>
            <p class="card-text">Phone No: +91-9172554355</p>
            <p class="card-text">Address: I-603, Wonder City, Katraj, Pune-46</p>
          </div>
          <div class="d-flex justify-content-center card-footer">
            <a @click="revertRequest(user.user_id)" class="btn btn-warning text-black px-4"
              >Revert Back</a
            >
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
      rejectedManagers: []
    }
  },
  methods: {
    async fetchRejectedManagers() {
      try {
        const response = await fetch('http://127.0.0.1:5000/admin/rejected/managers', {
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('accessToken')
          }
        })

        if (response.ok) {
          const data = await response.json()
          console.log('REJECTED MANAGERS: ', data)
          this.rejectedManagers = data.rejectedManagers
          this.isLoading = true
        }
      } catch (error) {
        console.error('Error fetching rejected managers:', error)
      }
    },
    async revertRequest(userId) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/admin/revert/${userId}`, {
          method: 'PUT',
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('accessToken'),
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ request_approval: 0 }) // Change request_approval status
        })

        if (response.ok) {
          // Update the list by filtering out the user that was approved
          this.rejectedManagers = this.rejectedManagers.filter((user) => user.user_id !== userId)
          window.location.reload()
          alert('Manager Status Reverted Back to Pending.')
        }
      } catch (error) {
        console.error('Error approving request:', error)
      }
    }
  },
  created() {
    this.fetchRejectedManagers()
  }
}
</script>
