<template>
  <div>
    <h1 class="text-white">Pending Requests</h1>
    <br />
    <div class="row">
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
            <p class="card-title text-center">{{ user.role }}</p>
            <hr />
            <p class="card-text">Email: {{ user.email }}</p>
            <p class="card-text">Phone No: +91-9172554355</p>
            <p class="card-text">Address: I-603, Wonder City, Katraj, Pune-46</p>
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
  </div>
</template>
  

<script>
export default {
  data() {
    return {
      pendingManagers: []
    }
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
        }
      } catch (error) {
        console.error('Error fetching pending managers:', error)
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
          this.pendingManagers = this.pendingManagers.filter((user) => user.userId !== userId)
          window.location.reload()
          alert('Manager Accepted!!')
        }
      } catch (error) {
        console.error('Error approving request:', error)
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
          this.pendingManagers = this.pendingManagers.filter((user) => user.userId !== userId)
          window.location.reload()
          alert('Manager Rejected.')
        }
      } catch (error) {
        console.error('Error declining request:', error)
      }
    }
  },
  created() {
    this.fetchPendingManagers()
  }
}
</script>
