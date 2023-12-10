<template>
  <div>
    <nav class="navbar navbar-expand-lg bg-dark" data-bs-theme="dark" style="min-height: 5rem">
      <div class="container-fluid">
        <a class="navbar-brand" href="/" style="padding: 0 15px; font-size: x-large"
          >Grocer<span style="font-weight: 600; color: #c1e1c1">Ease</span></a
        >
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div
          class="collapse navbar-collapse"
          id="navbarSupportedContent"
          style="font-size: larger; font-weight: 500"
        >
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item" v-if="this.role">
              <a class="nav-link active" href="/dashboard">Dashboard</a>
            </li>
            <li class="nav-item" v-if="!this.role">
              <a class="nav-link active" href="/register">Register</a>
            </li>
            <li class="nav-item" v-if="!this.role">
              <a class="nav-link active" href="/login">Login</a>
            </li>
            <a
              class="mx-5 mt-1"
              v-if="this.role === 'admin'"
              href="http://127.0.0.1:5000/download_csv"
              target="_blank"
            >
              <button class="btn btn-primary" type="button">Download CSV</button>
            </a>
          </ul>

          <a
            href="/pending_requests"
            v-if="this.role === 'admin'"
            class="text-white mt-2 mx-3 position-relative"
          >
            <i class="bi bi-bell-fill" style="font-size: 22px">
              <span
                v-if="$store.state.notificationCount > 0"
                class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger"
                style="font-size: 12px; transform: scale(0.8)"
              >
                {{ $store.state.notificationCount }}
                <span class="visually-hidden">pending requests</span>
              </span>
            </i>
          </a>

          <a
            href="/summary_dashboard"
            v-if="this.role === 'manager' || this.role === 'admin'"
            class="text-white mt-1 mx-5"
            ><i class="bi bi-clipboard-data-fill" style="font-size: 30px"></i
          ></a>

          <a href="/fav_items" v-if="this.role === 'user'" class="text-white mt-1 mx-2"
            ><i class="bi bi-bag-heart-fill" style="font-size: 30px"></i
          ></a>

          <a
            href="/cart"
            v-if="this.role === 'user'"
            class="text-white mt-2 mx-5 position-relative"
          >
            <i class="bi bi-cart4" style="font-size: 30px">
              <span
                v-if="$store.state.cart.length > 0"
                class="position-absolute top-0 start-80 mt-2 translate-middle badge rounded-pill bg-warning text-black"
                style="font-size: 11px; transform: scale(0.8)"
              >
                {{ $store.state.cart.length }}
                <span class="visually-hidden">cart items</span>
              </span>
            </i>
          </a>

          <ul v-if="this.role" class="navbar-nav" style="margin-right: 3rem">
            <li class="nav-item">
              <div class="dropdown">
                <button
                  class="btn dropdown-toggle"
                  type="button"
                  id="dropdownMenuButton1"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                  <img
                    src="https://creazilla-store.fra1.digitaloceanspaces.com/icons/7914927/man-icon-md.png"
                    alt="avatar"
                    style="height: 2.5rem; width: 2.5rem; border-radius: 50%"
                  />
                </button>
                <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
                  <li><a v-if="this.role" class="dropdown-item" href="/profile">Profile</a></li>
                  <li>
                    <a v-if="this.role === 'admin'" class="dropdown-item" href="/manager_pending"
                      >Pending</a
                    >
                  </li>
                  <li>
                    <a v-if="this.role === 'admin'" class="dropdown-item" href="/manager_accepted"
                      >Accepted</a
                    >
                  </li>
                  <li>
                    <a v-if="this.role === 'admin'" class="dropdown-item" href="/manager_rejected"
                      >Rejected</a
                    >
                  </li>
                  <li>
                    <a v-if="this.role === 'user'" class="dropdown-item" href="/fav_items"
                      >Favourites</a
                    >
                  </li>
                  <li>
                    <a v-if="this.role === 'user'" class="dropdown-item" href="/cart">Cart</a>
                  </li>
                  <li>
                    <a v-if="this.role === 'user'" class="dropdown-item" href="/orders">Orders</a>
                  </li>
                  <li>
                    <a
                      v-if="this.role"
                      class="dropdown-item"
                      style="cursor: pointer"
                      @click="logout"
                      >Logout</a
                    >
                  </li>
                </ul>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </div>
</template>
    
    <script>
export default {
  props: ['role'],
  methods: {
    logout: function () {
      localStorage.removeItem('accessToken')
      localStorage.removeItem('role')
      //this.$router.push({ path: '/' })
      this.$router.push({ path: '/' }).then(() => {
        this.$router.go()
      })
      alert('Successfully Logged Out!')
    },
    async fetchNotificationCount() {
      try {
        const response = await fetch('http://127.0.0.1:5000/notification_count', {
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('accessToken')
          }
        })

        if (response.ok) {
          const data = await response.json()
          this.$store.commit('setNotificationCount', data.notificationCount)
        }
      } catch (error) {
        console.error('Error fetching notification count:', error)
      }
    }
  },
  created() {
    // Fetch initial notification count
    this.fetchNotificationCount()

    // Example: Periodically fetch notification count (adjust as needed)
    setInterval(() => {
      this.fetchNotificationCount()
    }, 60000) // Every 1 minute
  }
}
</script>

